"""Berlin step 2: IHK Berlin's Gewerbedaten -> the storefronts inside the Land.

    python pipeline/berlin/step2_clean_businesses.py

Reads the cached register (pipeline/berlin/fetch_sources.py downloads it).
What a reader should know before trusting the counts printed below:

  * a row is an IHK MEMBER'S premises point; the register has no name and no
    street address, so a pin's title is IHK's own branch label (São Paulo's
    precedent: the register's descriptor, not a business's name);
  * crafts businesses (hairdressers, laundries, many bakers) are Handwerks-
    kammer members and are not in it (the taxonomy module's docstring);
  * the employee band, business age and business type are read to MEASURE
    and never written out (config.MEASURE_ONLY_COLUMNS).
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.berlin import config  # noqa: E402
from pipeline.taxonomies import filter_to_storefront, load_taxonomy_module  # noqa: E402

TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)

READ_COLUMNS = ["opendata_id", "city", "latitude", "longitude", "ihk_branch_id",
                "ihk_branch_desc", "nace_id", "nace_desc", "branch_top_level_id",
                "Bezirk", *config.MEASURE_ONLY_COLUMNS]
OUT_COLUMNS = ["opendata_id", "business_name", "latitude", "longitude",
               TAX.VALUE_COLUMN, "nace_id", "ihk_branch_id", "bezirk"]


def main():
    if not config.BUSINESSES_RAW_CSV.exists():
        sys.exit(f"Missing {config.BUSINESSES_RAW_CSV.name}: run "
                 f"python pipeline/berlin/fetch_sources.py first.")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    head = pd.read_csv(config.BUSINESSES_RAW_CSV, nrows=0, encoding=config.SOURCE_ENCODING)
    nameish = [c for c in head.columns
               if any(f in c.lower() for f in ("name", "firma", "inhaber", "strasse",
                                              "straße", "street", "hausnummer"))]
    if nameish:
        sys.exit(f"  the register now carries name-like column(s) {nameish} - "
                 f"read the source before building on it")

    df = pd.read_csv(config.BUSINESSES_RAW_CSV, dtype=str, usecols=READ_COLUMNS,
                     encoding=config.SOURCE_ENCODING)
    print(f"  {len(df):,} register rows")
    if df["opendata_id"].duplicated().any():
        sys.exit(f"  {df['opendata_id'].duplicated().sum()} duplicate opendata_id")
    other = df[df["city"] != config.CITY_KEEP]
    if len(other):
        sys.exit(f"  {len(other)} rows with city != {config.CITY_KEEP!r}: {other['city'].unique()[:5]}")

    df = filter_to_storefront(df, config.TAXONOMY_SYSTEM)
    df = df.assign(bucket=[TAX.classify({"nace_id": c, "ihk_branch_id": b})
                           for c, b in zip(df["nace_id"], df["ihk_branch_id"])])
    print(f"  {len(df):,} storefront rows after filter_to_storefront()")
    print("    " + ", ".join(f"{b} {n:,}" for b, n in df["bucket"].value_counts().items()))

    print("\n  catch-all codes (per-city call, config.CATCH_ALL_EXCLUDE):")
    for code in sorted(TAX.CATCH_ALL_CODES):
        n = int(df["nace_id"].eq(code).sum())
        mark = "DROP" if any(code.startswith(p) for p in config.CATCH_ALL_EXCLUDE["nace_id"]) \
            else "keep"
        print(f"    {mark} nace {code}: {n:,}")
    drop = pd.Series(False, index=df.index)
    for p in config.CATCH_ALL_EXCLUDE["nace_id"]:
        hit = df["nace_id"].fillna("").str.startswith(p)
        print(f"    DROP nace_id {p}* (prefix): {int(hit.sum()):,}")
        drop |= hit
    for code in config.CATCH_ALL_EXCLUDE["ihk_branch_id"]:
        hit = df["ihk_branch_id"].eq(code)
        kept = df["ihk_branch_id"].fillna("").str.startswith(code) & ~hit
        print(f"    DROP ihk_branch_id {code} (exact): {int(hit.sum()):,}; "
              f"its IHK children kept: {int(kept.sum()):,}")
        drop |= hit
    df = df[~drop]
    print(f"  {len(df):,} after the catch-all verdicts")

    lat = pd.to_numeric(df["latitude"], errors="coerce")
    lon = pd.to_numeric(df["longitude"], errors="coerce")
    df = df.assign(latitude=lat, longitude=lon)
    bad = df["latitude"].isna() | df["longitude"].isna()
    print(f"  {int(bad.sum()):,} without a coordinate, dropped")
    df = df[~bad]
    box = config.BERLIN_BBOX
    in_box = df["latitude"].between(box["lat_min"], box["lat_max"]) & \
        df["longitude"].between(box["lon_min"], box["lon_max"])
    print(f"  {int((~in_box).sum()):,} outside the sanity box, dropped")
    df = df[in_box]

    land = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_PROJECTED).union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]),
                        index=df.index, crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    inside = pts.within(land)
    print(f"  {int((~inside).sum()):,} outside the Land polygon, dropped")
    df = df[inside]

    # Measured, never written out.
    zero = df["employees_range"].eq("0 Beschäftigte")
    klein = df["business_type"].eq("Kleingewerbetreibender")
    print(f"\n  measured only: {zero.mean():.1%} report 0 employees, "
          f"{klein.mean():.1%} are Kleingewerbe")
    for b, g in df.groupby("bucket"):
        print(f"    {b}: 0 employees {g['employees_range'].eq('0 Beschäftigte').mean():.1%}")

    out = df.assign(business_name=df["ihk_branch_desc"].fillna(df[TAX.VALUE_COLUMN]),
                    bezirk=df["Bezirk"])[OUT_COLUMNS]
    leaked = set(out.columns) & set(config.MEASURE_ONLY_COLUMNS)
    assert not leaked, f"measure-only column(s) {leaked} reached the output"
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")
    print("    " + ", ".join(f"{b} {n:,}" for b, n in df["bucket"].value_counts().items()))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
