"""Step 2 - Clean San Diego's business tax certificate export.

Input:  data/san_diego/raw/sd_businesses_active_datasd.csv
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

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.residence import flag_home_based, report  # noqa: E402
from pipeline.san_diego.config import (  # noqa: E402
    BUSINESSES_RAW_CSV,
    BUSINESSES_CLEAN_CSV,
    BUSINESSES_PREFILTER_CSV,
    CITY_KEEP,
    PARCEL_RESIDENTIAL_CODES,
    PARCELS_CENTROIDS_CSV,
    SAN_DIEGO_BBOX,
    SOLE_OWNERSHIP_TYPE,
    TAXONOMY_SYSTEM,
    RAW_CLASSIFICATION_COLUMN,
    SOURCE_ENCODING,
)
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402


def main():
    if not BUSINESSES_RAW_CSV.exists():
        sys.exit(
            f"No file at {BUSINESSES_RAW_CSV}.\n"
            "Download from https://seshat.datasd.org/business_tax_certificates/"
            "sd_businesses_active_datasd.csv"
        )

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, low_memory=False, encoding=SOURCE_ENCODING)
    print(f"Loaded {len(df):,} rows")

    # Name the classification column the way the city's taxonomy expects,
    # so everything below is taxonomy-agnostic.
    value_column = load_taxonomy_module(TAXONOMY_SYSTEM).VALUE_COLUMN
    df = df.rename(columns={RAW_CLASSIFICATION_COLUMN: value_column})

    # --- Restrict to San Diego ---------------------------------------------
    # Do this before any other filter so drop counts below describe the
    # population this project is actually about. Known limitation - see config.py's CITY_KEEP comment:
    # this is an exact match on the raw address_city field, which
    # undercounts neighborhoods (La Jolla foremost) recorded under their
    # own name rather than "San Diego."
    before = len(df)
    df = df[df["address_city"].str.upper().str.strip() == CITY_KEEP]
    print(f"San Diego filter: {before:,} -> {len(df):,} rows")

    # --- Filter to storefront categories -----------------------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"Storefront filter ({TAXONOMY_SYSTEM}): {before:,} -> {len(df):,} rows")

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
        df = df[~at_home.reindex(df.index, fill_value=False)].reset_index(drop=True)
        df["record_id"] = df.index.astype(str)
    else:
        print(f"NOTE: no {PARCELS_CENTROIDS_CSV.name}, so the home-business "
              f"filter did NOT run. Build it with "
              f"pipeline/san_diego/fetch_parcels.py, then re-run.")

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
