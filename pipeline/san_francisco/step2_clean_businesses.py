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

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.san_francisco.config import (  # noqa: E402
    BUSINESSES_RAW_CSV,
    BUSINESSES_CLEAN_CSV,
    SAN_FRANCISCO_BBOX,
    NAICS_EXCLUDE_CODES,
    TAXONOMY_SYSTEM,
    RAW_CLASSIFICATION_COLUMN,
)
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

POINT_PATTERN = re.compile(r"POINT \(([-\d.]+) ([-\d.]+)\)")


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

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, low_memory=False)
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

    df = df.reset_index(drop=True)
    df["record_id"] = df.index.astype(str)

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
