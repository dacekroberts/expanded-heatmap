"""Step 2 - Clean Chicago's business licenses to storefront businesses with
usable coordinates.

Input:  data/chicago/raw/business_licenses_active.csv  (Socrata r5kz-chrr,
        server-filtered to issued, unexpired licenses; see config.py)
        data/chicago/raw/city_boundary.geojson          (cross-check)
Output: data/chicago/processed/businesses_clean.csv

The source is a license-term history (every term since 2002), so "active" is
status AAI (issued) with an expiration date on or after AS_OF_DATE. One
storefront can hold several licenses (a restaurant's Retail Food
Establishment plus adjunct Consumption on Premises / Tobacco licenses), so
after classification there is one row per site (account_number +
site_number), with the primary license deciding (LICENSE_PRIORITY in
config.py). Chicago's classification is its own license taxonomy, not NAICS;
the two catch-all license types are classified by business_activity (see
pipeline/taxonomies/chicago_license.py).

Run:  python pipeline/chicago/step2_clean_businesses.py
"""

import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.chicago.config import (  # noqa: E402
    BUSINESSES_RAW_CSV,
    BUSINESSES_CLEAN_CSV,
    CITY_BOUNDARY_GEOJSON,
    CRS_GEOGRAPHIC,
    CHICAGO_BBOX,
    AS_OF_DATE,
    CITY_KEEP,
    LICENSE_PRIORITY,
    TAXONOMY_SYSTEM,
    RAW_CLASSIFICATION_COLUMN,
)
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402


def main():
    if not BUSINESSES_RAW_CSV.exists():
        sys.exit(f"No file at {BUSINESSES_RAW_CSV}; see config.py for how to download it.")

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, low_memory=False)
    print(f"Loaded {len(df):,} rows (already filtered to issued, unexpired licenses at download time)")

    value_column = load_taxonomy_module(TAXONOMY_SYSTEM).VALUE_COLUMN
    df = df.rename(columns={RAW_CLASSIFICATION_COLUMN: value_column})

    # --- Active only (re-applied so a re-run is deterministic) ---------------
    before = len(df)
    expiry = pd.to_datetime(df["expiration_date"], errors="coerce")
    df = df[(df["license_status"] == "AAI") & (expiry >= pd.Timestamp(AS_OF_DATE))]
    print(f"Active filter (status AAI, expires on/after {AS_OF_DATE}): {before:,} -> {len(df):,} rows")

    # --- City -----------------------------------------------------------------
    before = len(df)
    df = df[df["city"].str.strip().str.upper() == CITY_KEEP]
    print(f"{CITY_KEEP.title()} filter (city field): {before:,} -> {len(df):,} rows")

    # --- Storefront categories -------------------------------------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"Storefront filter ({TAXONOMY_SYSTEM}): {before:,} -> {len(df):,} rows")

    # --- Coordinates -----------------------------------------------------------
    before = len(df)
    df = df.assign(latitude=pd.to_numeric(df["latitude"], errors="coerce"),
                   longitude=pd.to_numeric(df["longitude"], errors="coerce"))
    missing = df[df["latitude"].isna() | df["longitude"].isna()]
    redacted = missing["address"].fillna("").str.contains("REDACTED", case=False).sum()
    df = df.dropna(subset=["latitude", "longitude"])
    print(f"Coordinate presence: {before:,} -> {len(df):,} rows "
          f"({len(missing):,} without coordinates, {redacted:,} of them with a redacted address)")

    before = len(df)
    b = CHICAGO_BBOX
    df = df[df["latitude"].between(b["lat_min"], b["lat_max"]) & df["longitude"].between(b["lon_min"], b["lon_max"])]
    print(f"Coordinate sanity bounds: {before:,} -> {len(df):,} rows (catches swapped lat/lng and wild mismatches)")

    # --- One row per site, primary license first -----------------------------
    before = len(df)
    rank = {name: i for i, name in enumerate(LICENSE_PRIORITY)}
    df = df.assign(_rank=df[value_column].map(rank).fillna(len(rank)))
    df["site"] = df["account_number"] + "-" + df["site_number"]
    df = df.sort_values(["site", "_rank", "license_id"]).drop_duplicates(subset=["site"])
    print(f"One row per site (account + site number): {before:,} -> {len(df):,} rows")

    # --- Cross-check the city field against the boundary polygon -------------
    boundary = gpd.read_file(CITY_BOUNDARY_GEOJSON)
    boundary = boundary.set_crs(CRS_GEOGRAPHIC) if boundary.crs is None else boundary.to_crs(CRS_GEOGRAPHIC)
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]), crs=CRS_GEOGRAPHIC, index=df.index)
    inside = pts.within(boundary.geometry.union_all())
    print(f"Boundary cross-check: {int(inside.sum()):,} of {len(df):,} rows fall inside the Chicago polygon "
          f"({int((~inside).sum()):,} outside, kept: the polygon edge and the city field can differ slightly)")

    # --- Shared columns the map expects ------------------------------------------
    df["business_name"] = df["doing_business_as_name"].fillna("").str.strip()
    blank = df["business_name"] == ""
    if blank.any():
        print(f"Filling {blank.sum()} blank doing_business_as_name(s) from legal_name")
        df.loc[blank, "business_name"] = df.loc[blank, "legal_name"]

    keep = ["license_id", "business_name", value_column, "business_activity", "address",
            "latitude", "longitude", "site", "community_area_name"]
    df = df[keep].sort_values("license_id").reset_index(drop=True)
    df["record_id"] = df.index.astype(str)

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
