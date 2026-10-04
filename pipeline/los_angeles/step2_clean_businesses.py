"""Step 2 - Clean Los Angeles's active-business export.

Input:  data/los_angeles/raw/la_active_businesses.csv
        data/los_angeles/raw/la_county_incorporated_cities.geojson  (cross-check only)
Output: data/los_angeles/processed/businesses_clean.csv  (all in-city storefront rows;
        rows with unusable source coordinates are flagged, not dropped)

The export ships with coordinates (a `location_1` cell holding "(lat, lon)"),
rounded to 4 decimals (~11 m) - fine for ring bands of 160 m and up. But about
9% of storefront rows carry corrupt coordinates: longitude duplicated from
latitude, (0, 0), whole-degree placeholders, or points in the wrong county.
The damage is heavily skewed to recent registrations (22% of businesses that
started in 2020 or later, vs ~1% of older ones), so dropping them would
under-count new openings. This step therefore FLAGS them (coord_status =
needs_geocode, coordinates blanked) rather than dropping them, and step 3
recovers them by street address with the Census geocoder.

In-city rows are identified by the dataset's own `council_district` (1-15 =
inside the City of LA; 0 = registered with LA's Office of Finance but
located elsewhere), NOT by the `city` field, which holds postal community
names (Van Nuys, San Pedro, ...) that are all part of the city. See
config.py. As an independent check, this step prints how many of the kept
points also fall inside the City of LA boundary polygon.

Run:  python pipeline/los_angeles/step2_clean_businesses.py
"""

import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.los_angeles import config  # noqa: E402
from pipeline.los_angeles.config import (  # noqa: E402
    BUSINESSES_RAW_CSV,
    BUSINESSES_CLEAN_CSV,
    CITIES_BOUNDARY_GEOJSON,
    CITY_BOUNDARY_FIELD,
    CITY_BOUNDARY_NAME,
    CRS_GEOGRAPHIC,
    IN_CITY_COUNCIL_DISTRICTS,
    LOS_ANGELES_BBOX,
    NAICS_EXCLUDE_CODES,
    TAXONOMY_SYSTEM,
    RAW_CLASSIFICATION_COLUMN,
    SOURCE_ENCODING,
)
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

# "\n,  \n(34.0425, -118.3295)" - the location cell's actual text.
LATLON_PATTERN = re.compile(r"\(\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\)")


def parse_latlon(value):
    if not isinstance(value, str):
        return None, None
    m = LATLON_PATTERN.search(value)
    if not m:
        return None, None
    return float(m.group(1)), float(m.group(2))


def long_beach_rows():
    """Long Beach's storefront licences (regional only), in the shared columns
    step 3 reads. Every row already carries a point, so coord_status is
    `source` and the geocoder never sees it. FULLNAME is never loaded."""
    if not config.LONG_BEACH_CSV.exists():
        sys.exit(f"No file at {config.LONG_BEACH_CSV}. Run: python pipeline/los_angeles/fetch_long_beach.py")
    lb = pd.read_csv(config.LONG_BEACH_CSV, dtype=str, encoding="utf-8")
    leaked = set(lb.columns) & set(config.LONG_BEACH_FORBIDDEN)
    if leaked:
        sys.exit(f"{config.LONG_BEACH_CSV.name} carries {sorted(leaked)} - never load the holder's name")
    print(f"\nLong Beach: {len(lb):,} licences (active, in-city, not home-based, filtered at download)")
    tax = load_taxonomy_module(TAXONOMY_SYSTEM)
    lb["source"] = "long_beach"
    lb["category"] = lb["LICCATDESC"].fillna("").str.strip()
    lb["bucket"] = [tax.classify({"source": "long_beach", "category": c}) for c in lb["category"]]
    print("  buckets: " + ", ".join(f"{k} {v:,}" for k, v in
                                     lb["bucket"].value_counts(dropna=False).items()))
    lb = lb[lb["bucket"].notna()].copy()
    # A licence listed twice: keep one row, the higher-priority bucket first.
    rank = {b: i for i, b in enumerate(tax.BUCKET_PRIORITY)}
    before = len(lb)
    lb = (lb.assign(_r=lb["bucket"].map(rank)).sort_values(["LICENSENO", "_r"])
          .drop_duplicates("LICENSENO").drop(columns="_r"))
    print(f"  one row per licence: {before:,} -> {len(lb):,}")
    # Inside the City of Long Beach only: drops the layer's placeholder points
    # in the Pacific (as far as 27.2 N, -138.2 W on 2026-10-03).
    cities = gpd.read_file(CITIES_BOUNDARY_GEOJSON)
    cities = cities.set_crs(CRS_GEOGRAPHIC) if cities.crs is None else cities.to_crs(CRS_GEOGRAPHIC)
    poly = cities[cities[CITY_BOUNDARY_FIELD] == config.LONG_BEACH_BOUNDARY_NAME].geometry.union_all()
    pts = gpd.points_from_xy(pd.to_numeric(lb["longitude"]), pd.to_numeric(lb["latitude"]))
    inside = gpd.GeoSeries(pts, crs=CRS_GEOGRAPHIC).within(poly).to_numpy()
    print(f"  inside the City of Long Beach: {int(inside.sum()):,} of {len(lb):,} "
          f"({int((~inside).sum()):,} placeholder or outside points dropped)")
    lb = lb[inside]
    issued = pd.to_datetime(pd.to_numeric(lb["ISSDTTM"], errors="coerce"), unit="ms", errors="coerce")
    out = pd.DataFrame({
        "location_account": "LB-" + lb["LICENSENO"],
        # The trade name only; a blank one shows the street address (step 3).
        "business_name": lb["DBANAME"].fillna("").str.strip(),
        "dba_name": lb["DBANAME"].fillna("").str.strip(),
        "street_address": lb["SITELOCATION"].fillna("").str.strip(),
        "zip_code": lb["ZIP"],
        "location_start_date": issued.dt.strftime("%Y-%m-%d"),
        "naics": "", "category": lb["category"], "source": "long_beach",
        "latitude": pd.to_numeric(lb["latitude"]), "longitude": pd.to_numeric(lb["longitude"]),
        "coord_status": "source",
    })
    for b in tax.BUCKET_PRIORITY:
        print(f"      {b:<20} {int((lb['bucket'] == b).sum()):>6,}")
    return out


def main():
    if not BUSINESSES_RAW_CSV.exists():
        sys.exit(f"No file at {BUSINESSES_RAW_CSV}; see config.py for the download command.")

    df = pd.read_csv(BUSINESSES_RAW_CSV, dtype=str, low_memory=False, encoding=SOURCE_ENCODING)
    print(f"Loaded {len(df):,} rows (already filtered to rows with coordinates at download time)")

    # Name the classification column the way the city's taxonomy expects,
    # so everything below is taxonomy-agnostic. Regional: LA's code stays in
    # `naics` (the dispatching taxonomy reads it there) and `category` shows it.
    value_column = load_taxonomy_module(TAXONOMY_SYSTEM).VALUE_COLUMN
    if config.REGIONAL:
        df["source"] = "los_angeles"
        df["category"] = "NAICS " + df[RAW_CLASSIFICATION_COLUMN].fillna("").str.strip()
        value_column = RAW_CLASSIFICATION_COLUMN
    else:
        df = df.rename(columns={RAW_CLASSIFICATION_COLUMN: value_column})

    # --- Restrict to the City of Los Angeles --------------------------------
    before = len(df)
    district = pd.to_numeric(df["council_district"], errors="coerce")
    df = df[district.isin(list(IN_CITY_COUNCIL_DISTRICTS))]
    print(f"In-city filter (council_district 1-15): {before:,} -> {len(df):,} rows")

    # --- Filter to storefront categories ------------------------------------
    before = len(df)
    df = filter_to_storefront(df, TAXONOMY_SYSTEM)
    print(f"Storefront filter ({TAXONOMY_SYSTEM}): {before:,} -> {len(df):,} rows")

    # --- Excluded catch-all codes (per-city verdict; see config.py) ----------
    if NAICS_EXCLUDE_CODES:
        before = len(df)
        df = df[~df[value_column].astype(str).isin(NAICS_EXCLUDE_CODES)]
        print(f"Excluded catch-all codes {sorted(NAICS_EXCLUDE_CODES)}: "
              f"{before:,} -> {len(df):,} rows")

    # --- Parse coordinates; FLAG (don't drop) unusable ones -----------------
    lat_lon = df["location_1"].map(parse_latlon)
    df["latitude"] = [ll[0] for ll in lat_lon]
    df["longitude"] = [ll[1] for ll in lat_lon]
    b = LOS_ANGELES_BBOX
    usable = (
        df["latitude"].between(b["lat_min"], b["lat_max"])
        & df["longitude"].between(b["lon_min"], b["lon_max"])
    )
    lat, lon = df["latitude"], df["longitude"]
    zero_or_whole = ~usable & ((lat == 0) | (lon == 0) | ((lat % 1 == 0) & (lon % 1 == 0)))
    lon_copies_lat = ~usable & ~zero_or_whole & (lat == lon)
    print(f"Source coordinates: {int(usable.sum()):,} usable; {int((~usable).sum()):,} "
          f"({(~usable).mean():.1%}) need geocoding "
          f"[(0,0)/whole-degree {int(zero_or_whole.sum()):,}; longitude copied from latitude "
          f"{int(lon_copies_lat.sum()):,}; other outside the city's bounds "
          f"{int((~usable & ~zero_or_whole & ~lon_copies_lat).sum()):,}]")
    df["coord_status"] = usable.map({True: "source", False: "needs_geocode"})
    df.loc[~usable, ["latitude", "longitude"]] = float("nan")

    # --- Deduplicate --------------------------------------------------------
    # location_account is the dataset's own per-location identifier.
    before = len(df)
    df = df.drop_duplicates(subset=["location_account"])
    print(f"Deduplication: {before:,} -> {len(df):,} rows")

    # --- Display name --------------------------------------------------------
    # Trade name (dba_name) when there is one, else the registrant's name.
    dba = df["dba_name"].fillna("").str.strip()
    df["business_name"] = df["business_name"].where(dba == "", dba)
    blank = df["business_name"].fillna("").str.strip() == ""
    if blank.any():
        print(f"WARNING: {blank.sum()} row(s) still have no name")

    # --- Independent cross-check against the boundary polygon ----------------
    if CITIES_BOUNDARY_GEOJSON.exists():
        cities = gpd.read_file(CITIES_BOUNDARY_GEOJSON)
        cities = cities.set_crs(CRS_GEOGRAPHIC) if cities.crs is None else cities.to_crs(CRS_GEOGRAPHIC)
        la = cities[cities[CITY_BOUNDARY_FIELD] == CITY_BOUNDARY_NAME]
        have = df.dropna(subset=["latitude", "longitude"])
        pts = gpd.GeoDataFrame(
            have[["location_account"]],
            geometry=gpd.points_from_xy(have["longitude"], have["latitude"]),
            crs=CRS_GEOGRAPHIC,
        )
        inside = gpd.sjoin(pts, la[["geometry"]], predicate="within", how="left")["index_right"].notna()
        print(f"Cross-check: {int(inside.sum()):,} of {len(have):,} source-coordinate points "
              f"({inside.mean():.1%}) also fall inside the City of Los Angeles polygon "
              "(the rest sit on the boundary, in enclaves, or are 4-decimal rounding).")

    if config.REGIONAL:
        lb = long_beach_rows()
        df = pd.concat([df, lb], ignore_index=True)
        print(f"\nLos Angeles (Regional): {len(df) - len(lb):,} City of LA rows + {len(lb):,} Long Beach")

    df = df.reset_index(drop=True)
    df["record_id"] = df.index.astype(str)

    BUSINESSES_CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(BUSINESSES_CLEAN_CSV, index=False)
    print(f"\nWrote {len(df):,} rows to {BUSINESSES_CLEAN_CSV}")


if __name__ == "__main__":
    main()
