"""Step 2 - Clean San Francisco's Registered Business Locations export.

Input:  data/san_francisco/raw/sf_business_locations.csv
Output: data/san_francisco/processed/businesses_clean.csv

Like San Diego's, this export ships pre-geocoded (a WKT `location` point
column), so there is no separate geocoding step - this step's output
already has usable coordinates, filtered for validity. The raw CSV was
downloaded pre-filtered to city='San Francisco' (see
pipeline/san_francisco/config.py's BUSINESSES_RAW_CSV) rather than the full
~356k-row dataset that includes out-of-city registrants - DataSF's API
supports server-side filtering - unlike San Diego's raw export, which
includes out-of-city rows for step 2 itself to filter.

Run:  python pipeline/san_francisco/step2_clean_businesses.py
"""

import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.residence import (  # noqa: E402
    flag_home_based,
    has_residential_unit,
    report,
)
from pipeline.san_francisco.config import (  # noqa: E402
    ASSESSOR_ROLL_CSV,
    BUSINESSES_RAW_CSV,
    BUSINESSES_CLEAN_CSV,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    PARCEL_RESIDENTIAL,
    PARCEL_TOLERANCE_M,
    SAN_FRANCISCO_BBOX,
    NAICS_EXCLUDE_CODES,
    TAXONOMY_SYSTEM,
    RAW_CLASSIFICATION_COLUMN,
    SOURCE_ENCODING,
)
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

POINT_PATTERN = re.compile(r"POINT \(([-\d.]+) ([-\d.]+)\)")
# the_geom arrives as a string in the roll's CSV export; pull the pair out
# rather than depending on which of WKT or GeoJSON Socrata emits.
COORD_PATTERN = re.compile(r"(-?\d+\.\d+)[ ,]+(-?\d+\.\d+)")


def parcel_points():
    """The Assessor roll as projected points, one row per block+lot.

    Where an address carries several roll rows (condominiums), the one with
    the largest homeowner's exemption is kept, so the join errs toward
    FINDING an owner-occupied home rather than hiding one.
    """
    roll = pd.read_csv(ASSESSOR_ROLL_CSV, dtype=str, low_memory=False, encoding=SOURCE_ENCODING)
    coord = roll["the_geom"].astype(str).str.extract(COORD_PATTERN)
    roll["lon"] = pd.to_numeric(coord[0], errors="coerce")
    roll["lat"] = pd.to_numeric(coord[1], errors="coerce")
    roll = roll.dropna(subset=["lon", "lat"])
    roll["exemption"] = pd.to_numeric(
        roll["homeowner_exemption_value"], errors="coerce").fillna(0)
    roll = roll.sort_values("exemption", ascending=False).drop_duplicates(
        subset=["block", "lot"])
    print(f"  assessor roll: {len(roll):,} parcels with a point")
    return gpd.GeoDataFrame(
        roll[["use_definition", "number_of_units", "exemption"]],
        geometry=gpd.points_from_xy(roll["lon"], roll["lat"]),
        crs=CRS_GEOGRAPHIC,
    ).to_crs(CRS_PROJECTED)


def parse_point(value):
    """WKT 'POINT (lon lat)' -> (latitude, longitude), or (None, None)."""
    if not isinstance(value, str):
        return None, None
    m = POINT_PATTERN.match(value)
    if not m:
        return None, None
    lon, lat = float(m.group(1)), float(m.group(2))
    return lat, lon


def main():
    if not BUSINESSES_RAW_CSV.exists():
        sys.exit(
            f"No file at {BUSINESSES_RAW_CSV}.\n"
            "Download from https://data.sf.gov/resource/g8m3-pdis.csv"
            "?$where=city='San Francisco'&$limit=400000"
        )

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, low_memory=False, encoding=SOURCE_ENCODING)
    print(f"Loaded {len(df):,} rows (already filtered to San Francisco at download time)")

    # Name the classification column the way the city's taxonomy expects,
    # so everything below is taxonomy-agnostic.
    value_column = load_taxonomy_module(TAXONOMY_SYSTEM).VALUE_COLUMN
    df = df.rename(columns={RAW_CLASSIFICATION_COLUMN: value_column})

    # --- Active only --------------------------------------------------------
    # administratively_closed is populated (non-null) for closed
    # businesses, blank for active ones.
    before = len(df)
    df = df[df["administratively_closed"].isna()]
    print(f"Active-only filter: {before:,} -> {len(df):,} rows")

    # --- Filter to storefront categories --------------------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"Storefront filter ({TAXONOMY_SYSTEM}): {before:,} -> {len(df):,} rows")

    # --- Excluded catch-all codes (per-city verdict; see config.py) ----------
    if NAICS_EXCLUDE_CODES:
        before = len(df)
        df = df[~df[value_column].astype(str).isin(NAICS_EXCLUDE_CODES)]
        print(f"Excluded catch-all codes {sorted(NAICS_EXCLUDE_CODES)}: "
              f"{before:,} -> {len(df):,} rows")

    # --- Parse coordinates, drop rows without usable ones -------------------
    before = len(df)
    lat_lon = df["location"].apply(parse_point)
    df["latitude"] = [ll[0] for ll in lat_lon]
    df["longitude"] = [ll[1] for ll in lat_lon]
    df = df.dropna(subset=["latitude", "longitude"])
    print(f"Coordinate presence: {before:,} -> {len(df):,} rows")

    before = len(df)
    b = SAN_FRANCISCO_BBOX
    df = df[
        df["latitude"].between(b["lat_min"], b["lat_max"])
        & df["longitude"].between(b["lon_min"], b["lon_max"])
    ]
    print(f"Coordinate sanity bounds: {before:,} -> {len(df):,} rows")

    # --- Deduplicate --------------------------------------------------------
    # uniqueid is this export's own primary key (certificate + location
    # id combined) - the direct equivalent of San Diego's account_key.
    before = len(df)
    df = df.drop_duplicates(subset=["uniqueid"])
    print(f"Deduplication: {before:,} -> {len(df):,} rows")

    # --- Rename to the shared column names the map step expects -------------
    df = df.rename(columns={
        "dba_name": "business_name",
    })
    blank_name = df["business_name"].fillna("").str.strip() == ""
    if blank_name.any():
        print(f"Filling {blank_name.sum()} blank dba_name(s) from ownership_name")
        df.loc[blank_name, "business_name"] = df.loc[blank_name, "ownership_name"]

    # --- Home-based businesses, against the Assessor's own classification ----
    # A scope filter first: a caterer or hairdresser working from the house
    # they own is not a storefront. That it also removes this city's largest
    # personal-name exposure is the second reason, not the first - the same
    # framing as the 812990 exclusion above.
    #
    # Both conditions are required. Land use alone flags 12.4% of person-like
    # pins here, and this city's largest category under its pins is
    # Multi-Family Residential (5,733) because San Francisco puts ground-floor
    # retail in residential buildings. See pipeline/residence.py.
    if ASSESSOR_ROLL_CSV.exists():
        before = len(df)
        pts = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
            crs=CRS_GEOGRAPHIC).to_crs(CRS_PROJECTED)
        joined = gpd.sjoin_nearest(
            pts, parcel_points(), how="left",
            max_distance=PARCEL_TOLERANCE_M, distance_col="parcel_dist_m")
        # sjoin_nearest emits a row per tie; keep one per business.
        joined = joined[~joined.index.duplicated(keep="first")]
        matched = joined["use_definition"].notna()
        print(f"  parcel match within {PARCEL_TOLERANCE_M:.0f} m: "
              f"{int(matched.sum()):,} of {len(joined):,} "
              f"({100 * matched.mean():.1f}%), median "
              f"{joined['parcel_dist_m'].median():.1f} m")

        # Rule 1 - a house. Owner occupancy is required: a single-family parcel
        # alone does not establish that the business IS the home.
        at_house = flag_home_based(
            joined["business_name"],
            residential=joined["use_definition"].isin(PARCEL_RESIDENTIAL),
            owner_occupied=joined["exemption"].fillna(0) > 0,
        )
        report("person-like name + single-family parcel + homeowner's exemption",
               at_house, before,
               extra={"NAICS": joined[value_column],
                      "use_definition": joined["use_definition"]})

        # Rule 2 - a flat, which rule 1 cannot reach: a block of flats is
        # classified multi-family whether or not a shop occupies its ground
        # floor, so the parcel says nothing on its own. Here the DWELLING-UNIT
        # DESIGNATOR in the business's own address is the evidence, and no
        # owner-occupancy test is needed - a rented flat is still someone's
        # home.
        #
        # The building check is what makes it safe, and it is not optional: of
        # 272 person-like pins at an apartment address, 188 sit on a purely
        # residential building but **51 sit on a commercial or industrial
        # one** - real tenancies in a unit-numbered commercial building.
        # Filtering on the address designator alone would have deleted those 51.
        at_flat = flag_home_based(
            joined["business_name"],
            residential=(
                joined["full_business_address"].map(has_residential_unit)
                & joined["use_definition"].fillna("").str.contains(
                    "Residential|Dwelling", case=False, na=False)
            ),
        )
        report("person-like name + dwelling-unit address + residential "
               "building", at_flat, before,
               extra={"NAICS": joined[value_column],
                      "use_definition": joined["use_definition"]})

        at_home = at_house | at_flat
        print(f"  combined: {int(at_home.sum()):,} removed "
              f"({int((at_house & at_flat).sum()):,} matched both rules)")
        df = df[~at_home.reindex(df.index, fill_value=False)]
    else:
        print(f"  WARNING: no assessor roll at {ASSESSOR_ROLL_CSV.name}; the "
              f"home-business filter did NOT run. Run "
              f"pipeline/san_francisco/fetch_sources.py")

    df = df.reset_index(drop=True)
    df["record_id"] = df.index.astype(str)

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
