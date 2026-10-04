"""Step 2 - Clean San Diego's business tax certificate export.

Input:  data/san_diego/raw/sd_businesses_active_datasd.csv
        data/san_diego/raw/municipal_boundaries.geojson  (city limits)
        data/san_diego/raw/parcels_centroids.csv  (fetch_parcels.py)
Output: data/san_diego/processed/businesses_clean.csv

San Diego's export ships pre-geocoded (`lat`/`lng` columns, 98.4% populated - checked
directly against the live file, 2026-09-18) - there is no
separate geocoding step in this city's pipeline (steps are 1 stations,
2 clean businesses, 3 map); this step's output already has usable
coordinates, filtered for validity.

Run:  python pipeline/san_diego/step2_clean_businesses.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd
import shapely

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.residence import flag_home_based, looks_personal, report  # noqa: E402
from pipeline.san_diego.config import (  # noqa: E402
    BUSINESSES_RAW_CSV,
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_PREFILTER_CSV,
    CITY_BOUNDARY_NAME,
    CITY_KEEP,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    MUNICIPAL_BOUNDARIES_GEOJSON,
    NAICS_EXCLUDE_CODES,
    PARCEL_RESIDENTIAL_CODES,
    PARCELS_CENTROIDS_CSV,
    SAN_DIEGO_BBOX,
    SOLE_OWNERSHIP_TYPE,
    TAXONOMY_SYSTEM,
    RAW_CLASSIFICATION_COLUMN,
    SOURCE_ENCODING,
)
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402


def within_city(lon, lat):
    """True where a point lies inside San Diego's city limits, as a boolean
    array aligned with the inputs. Both sides are projected to UTM first."""
    boundary = gpd.read_file(MUNICIPAL_BOUNDARIES_GEOJSON)
    boundary = (boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None
                else boundary.to_crs(CRS_GEOGRAPHIC))
    city = boundary[boundary["Name"] == CITY_BOUNDARY_NAME]
    if city.empty:
        sys.exit(f"No {CITY_BOUNDARY_NAME!r} feature in {MUNICIPAL_BOUNDARIES_GEOJSON}")
    polygon = city.to_crs(CRS_PROJECTED).geometry.union_all()
    shapely.prepare(polygon)
    points = gpd.GeoSeries(gpd.points_from_xy(lon, lat), crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
    return points.within(polygon).to_numpy()


def main():
    if not BUSINESSES_RAW_CSV.exists():
        sys.exit(
            f"No file at {BUSINESSES_RAW_CSV}.\n"
            "Download from https://seshat.datasd.org/business_tax_certificates/"
            "sd_businesses_active_datasd.csv"
        )
    if not MUNICIPAL_BOUNDARIES_GEOJSON.exists():
        sys.exit(
            f"No boundary file at {MUNICIPAL_BOUNDARIES_GEOJSON}.\n"
            "Download it from "
            "https://geo.sandag.org/server/rest/directories/downloads/Municipal_Boundaries.geojson"
        )

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, low_memory=False, encoding=SOURCE_ENCODING)
    print(f"Loaded {len(df):,} rows")

    # Name the classification column the way the city's taxonomy expects,
    # so everything below is taxonomy-agnostic.
    value_column = load_taxonomy_module(TAXONOMY_SYSTEM).VALUE_COLUMN
    df = df.rename(columns={RAW_CLASSIFICATION_COLUMN: value_column})

    # --- Filter to storefront categories -----------------------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"Storefront filter ({TAXONOMY_SYSTEM}): {before:,} -> {len(df):,} rows")

    # --- Excluded codes (per-city verdict; see config.py) --------------------
    # EXACT match: "8129" must not take 81291 pet care or 81292 photofinishing.
    before = len(df)
    df = df[~df[value_column].astype(str).str.strip().isin(NAICS_EXCLUDE_CODES)]
    print(f"Excluded codes {sorted(NAICS_EXCLUDE_CODES)} (owner, 2026-09-29; "
          f"booth rental 2026-10-04): "
          f"{before:,} -> {len(df):,} rows")

    # --- Drop rows without usable coordinates -------------------------------
    before = len(df)
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lng"] = pd.to_numeric(df["lng"], errors="coerce")
    df = df.dropna(subset=["lat", "lng"])
    print(f"Coordinate presence: {before:,} -> {len(df):,} rows")

    before = len(df)
    b = SAN_DIEGO_BBOX
    df = df[
        df["lat"].between(b["lat_min"], b["lat_max"])
        & df["lng"].between(b["lon_min"], b["lon_max"])
    ]
    print(f"Coordinate sanity bounds: {before:,} -> {len(df):,} rows "
          f"(catches swapped lat/lng and wild mismatches)")

    # --- Restrict to San Diego city limits ----------------------------------
    # A point-in-polygon test against the city's own boundary, the polygon
    # step 1 keeps stations by (owner, 2026-10-04). It replaced an exact match
    # on address_city, which dropped storefronts inside the city whose address
    # names the neighborhood (La Jolla, San Ysidro, Del Mar and stray
    # spellings) and kept a few outside it; see config.CITY_KEEP. Tested in
    # UTM metres (CRS_PROJECTED), never in degrees. After the coordinate
    # checks, because the test needs a usable point.
    before = len(df)
    df = df[within_city(df["lng"], df["lat"])]
    print(f"San Diego city limits ({CITY_BOUNDARY_NAME}, "
          f"{MUNICIPAL_BOUNDARIES_GEOJSON.name}): {before:,} -> {len(df):,} rows")
    named = df["address_city"].fillna("").str.upper().str.strip()
    print("  kept with an address city other than San Diego: "
          f"{int((named != CITY_KEEP).sum()):,} "
          f"{named[named != CITY_KEEP].value_counts().head(5).to_dict()}")

    # --- Deduplicate --------------------------------------------------------
    # account_key is this export's primary key (per the data dictionary),
    # the dataset's own account identifier.
    before = len(df)
    df = df.drop_duplicates(subset=["account_key"])
    print(f"Deduplication: {before:,} -> {len(df):,} rows")

    # --- Rename to the shared column names the map step expects -------------
    df = df.rename(columns={
        "dba_name": "business_name",
        "lat": "latitude",
        "lng": "longitude",
    })
    blank_name = df["business_name"].fillna("").str.strip() == ""
    if blank_name.any():
        print(f"Filling {blank_name.sum()} blank dba_name(s) from business_owner_name")
        df.loc[blank_name, "business_name"] = df.loc[blank_name, "business_owner_name"]

    df = df.reset_index(drop=True)
    df["record_id"] = df.index.astype(str)

    # The unfiltered population, for fetch_parcels.py to look up. Written
    # before the filter below, and it must stay that way - see
    # config.BUSINESSES_PREFILTER_CSV.
    BUSINESSES_PREFILTER_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_PREFILTER_CSV, index=False)

    # --- Home-based businesses, against SanGIS's own classification ----------
    # This city had NO residence signal before: its address_suite holds bare
    # values ("A", "101") with no APT/STE token, so its old 0.03% reading was a
    # measurement gap rather than a clean result.
    #
    # Four conditions, the most conservative filter of the three cities that
    # needed one: a person-like displayed name, a sole proprietorship in the
    # registry's own ownership_type, a single-family parcel, and owner
    # occupancy. `asr_landuse` 17 (condominium) is deliberately not in
    # PARCEL_RESIDENTIAL_CODES - see config.py, and pipeline/residence.py for
    # why land use alone is not a signal.
    #
    # NO apartment rule here, unlike San Francisco and Los Angeles: that rule
    # reads a dwelling-unit designator out of the address, and this registry's
    # address_suite holds bare values ("A", "101") with no APT/UNIT token to
    # read. Measured residual: 1 pin (0.04%).
    #
    # NEAREST parcel, not containing parcel, and that is specific to this city:
    # its coordinates sit 5-15 m outside their own lot, so a point-in-parcel
    # test matched 1 of 30 sampled pins. fetch_parcels.py resolves the nearest
    # parcel per pin and caches the result; this step only reads it, so the
    # pipeline stays offline and deterministic.
    if PARCELS_CENTROIDS_CSV.exists():
        before = len(df)
        parcels = pd.read_csv(PARCELS_CENTROIDS_CSV, dtype=str)
        m = df.merge(parcels, on="account_key", how="left")
        looked_up = m["apn"].notna()
        found = m["asr_landuse"].fillna("").ne("")
        dist = pd.to_numeric(m["dist_m"], errors="coerce")
        print(f"Parcel lookups available for {int(looked_up.sum()):,} "
              f"person-like rows; nearest parcel found for "
              f"{int(found.sum()):,} "
              f"({100 * found.sum() / max(int(looked_up.sum()), 1):.1f}%), "
              f"median distance {dist.median():.1f} m")
        # A person-like row with no cache row cannot be flagged. Non-zero means
        # the cache predates rows step 2 now keeps: re-run fetch_parcels.py.
        unlooked = m["business_name"].map(looks_personal) & ~looked_up
        print(f"Person-like rows with NO parcel lookup (not testable): "
              f"{int(unlooked.sum()):,}, sole proprietorships "
              f"{int((unlooked & m['ownership_type'].fillna('').str.strip().eq(SOLE_OWNERSHIP_TYPE)).sum()):,}")

        landuse = pd.to_numeric(m["asr_landuse"], errors="coerce")
        at_home = flag_home_based(
            m["business_name"],
            residential=landuse.isin(PARCEL_RESIDENTIAL_CODES),
            owner_occupied=m["ownerocc"].fillna("").str.strip().str.upper()
                            .eq("Y"),
            individual=m["ownership_type"].fillna("").str.strip()
                        .eq(SOLE_OWNERSHIP_TYPE),
        )
        report("person-like name + sole proprietorship + single-family parcel "
               "+ owner-occupied", at_home, before,
               extra={"NAICS": m["naics"], "asr_landuse": m["asr_landuse"]})
        # UNTESTED, LEFT OFF (owner's privacy rule; 2026-10-04): a person-like
        # sole proprietorship the parcel cache has no row for cannot be tested
        # for a home, so it is dropped as a home would be, never shown with a
        # name or a street address. 85 rows (29 pins) when the city-limits test
        # replaced the address_city match; re-running fetch_parcels.py covers
        # them and this then drops nothing.
        untested = unlooked & m["ownership_type"].fillna("").str.strip().eq(SOLE_OWNERSHIP_TYPE)
        report("person-like sole proprietorship with no parcel lookup (untested)",
               untested, before, extra={"NAICS": m["naics"]})
        at_home = at_home | untested
        df = df[~at_home.reindex(df.index, fill_value=False)].reset_index(drop=True)
        df["record_id"] = df.index.astype(str)
    else:
        print(f"NOTE: no {PARCELS_CENTROIDS_CSV.name}, so the home-business "
              f"filter did NOT run. Build it with "
              f"pipeline/san_diego/fetch_parcels.py, then re-run.")

    # --- A registrant's own name shows the street address --------------------
    # Kansas City's rule as Los Angeles applies it (owner, 2026-10-01), widened
    # to a trade name that IS the registrant's own name (owner, 2026-10-03;
    # DECISIONS "San Diego and Los Angeles: a trade name that is the
    # registrant's own name"): dba_name repeating business_owner_name verbatim
    # gives no trade name, so where it reads as a person (the exposure check's
    # looks_personal) the pin keeps its place and shows its street address,
    # without the suite. Measured before the change: 128 of 423 person-like
    # names on the map, 120 of them sole proprietorships. HERE, AFTER the home
    # filter, which tests the displayed name.
    #
    # In any word order (owner, 2026-10-04): the two names match when their
    # sorted whitespace tokens do, so a trade name that reorders the owner's
    # own name counts as the same name. Measured before the change: 6 to 7
    # pins. Punctuation is NOT stripped, which leaves one more row a
    # punctuation-blind test would catch (2026-10-04).
    names = df["business_name"].fillna("").astype(str).str.strip()
    owner = df["business_owner_name"].fillna("").astype(str).str.strip()

    def tokens(s):
        return s.str.upper().str.split().map(lambda t: tuple(sorted(t)))

    own = (names != "") & (tokens(names) == tokens(owner)) & names.map(looks_personal)
    verbatim = own & (names.str.upper() == owner.str.upper())
    street = (df[["address_no", "address_no_fraction", "address_pd", "address_road", "address_sfx"]]
              .fillna("").astype(str).agg(" ".join, axis=1)
              .str.split().str.join(" "))
    if (own & ~street.str.contains(r"\d", regex=True)).any():
        sys.exit("a registrant's own name has no street number to show in its place")
    df["name_is_address"] = own
    df.loc[own, "business_name"] = street[own]
    print(f"A registrant's own name shows the street address instead (pins kept): "
          f"{int(own.sum()):,} ({int(verbatim.sum()):,} verbatim, "
          f"{int((own & ~verbatim).sum()):,} in another word order)")

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
