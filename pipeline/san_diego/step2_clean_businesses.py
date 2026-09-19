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
from pipeline.san_diego.config import (  # noqa: E402
    BUSINESSES_RAW_CSV,
    BUSINESSES_CLEAN_CSV,
    CITY_KEEP,
    SAN_DIEGO_BBOX,
    TAXONOMY_SYSTEM,
    RAW_CLASSIFICATION_COLUMN,
)
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402


def main():
    if not BUSINESSES_RAW_CSV.exists():
        sys.exit(
            f"No file at {BUSINESSES_RAW_CSV}.\n"
            "Download from https://seshat.datasd.org/business_tax_certificates/"
            "sd_businesses_active_datasd.csv"
        )

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, low_memory=False)
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

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
