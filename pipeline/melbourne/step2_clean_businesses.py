"""Melbourne step 2: the City of Melbourne's CLUE 2024 establishments -> the
storefronts inside the City of Melbourne LGA.

    python pipeline/melbourne/step2_clean_businesses.py

Reads the cache only (pipeline/melbourne/fetch_sources.py downloads). What a
reader should know before trusting the counts printed below:

  * the class list is pipeline/taxonomies/anzsic_fes.py's, shared with Sydney;
    CLUE's columns are renamed to that module's names first, and an undecided
    class in a storefront division stops the step;
  * points are the PROPERTY's, shared by every tenancy in it (a shopping
    centre is one coordinate): ring counts are unaffected, the stacking is
    printed;
  * a pin shows the trading name the census records; the address is read only
    to report upper-floor tenancies and is never written out.
"""
import re
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.melbourne import config  # noqa: E402
from pipeline.taxonomies import load_taxonomy_module  # noqa: E402

TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)
UPPER = r"(?i)\b(?:level|lvl|floor)\s*(?:\d+|[a-z]+)\b|\bsuite\b"
GROUND = r"(?i)\b(?:level|lvl|floor)\s*(?:0|g|ground|lg|lower ground|b\d?|basement|m|mezzanine|1)\b"


def main():
    if not config.CLUE_CSV.exists():
        sys.exit(f"missing {config.CLUE_CSV}: run python pipeline/melbourne/fetch_sources.py")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(config.CLUE_CSV, dtype=str, encoding="utf-8-sig")
    print(f"  {len(df):,} CLUE {config.CLUE_YEAR} establishments")
    if set(df["census_year"].str[:4]) != {config.CLUE_YEAR}:
        sys.exit(f"  census years {sorted(set(df['census_year']))} in the cache, expected {config.CLUE_YEAR}")
    df = df.rename(columns={"industry_anzsic4_code": "ClassificationCode",
                            "industry_anzsic4_description": "ClassificationName"})

    new = sorted(set(df.loc[df["ClassificationCode"].map(TAX.undecided), "ClassificationCode"]))
    if new:
        sys.exit(f"  storefront-division class(es) the taxonomy has not decided: {new}")
    excl = df[df["ClassificationCode"].isin(TAX.EXCLUDED)]
    print("  excluded by class:")
    for code, n in excl["ClassificationCode"].value_counts().items():
        print(f"    {code} {TAX.EXCLUDED[code][:62]:<62} {n:>4}")

    df = df.assign(bucket=df.apply(lambda r: TAX.classify(r.to_dict()), axis=1))
    df = df[df["bucket"].notna()].copy()
    print(f"  {len(df):,} storefronts; " + ", ".join(f"{b} {n:,}" for b, n in df["bucket"].value_counts().items()))
    blank = df["trading_name"].fillna("").str.strip() == ""
    if blank.any():
        sys.exit(f"  {int(blank.sum())} storefronts with no trading name - read them first")
    up = df["business_address"].str.contains(UPPER, regex=True) & \
        ~df["business_address"].str.contains(GROUND, regex=True)
    print(f"  upper-floor or suite tenancies (kept, reported): {int(up.sum()):,} ({up.mean():.1%}); by bucket "
          + ", ".join(f"{b} {int(n)}" for b, n in df[up]["bucket"].value_counts().items()))

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    no_point = df["latitude"].isna() | df["longitude"].isna()
    print(f"  {int(no_point.sum()):,} without a point, dropped")
    df = df[~no_point]
    box = config.MELBOURNE_BBOX
    in_box = df["latitude"].between(box["lat_min"], box["lat_max"]) & \
        df["longitude"].between(box["lon_min"], box["lon_max"])
    print(f"  {int((~in_box).sum()):,} outside the sanity box, dropped")
    df = df[in_box]
    area = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_PROJECTED).union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]), index=df.index,
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    inside = pts.within(area)
    print(f"  {int((~inside).sum()):,} outside the City of Melbourne (OSM relation "
          f"{config.BOUNDARY_OSM_RELATION}), dropped")
    df = df[inside]

    xy = pts[inside].map(lambda p: (round(p.x), round(p.y)))
    stack = xy.map(xy.value_counts())
    print(f"  {xy.nunique():,} distinct points (1 m); {(stack == 1).mean():.1%} alone, "
          f"{(stack >= 10).mean():.1%} in stacks of 10 or more, the largest {int(stack.max())}")

    out = df.assign(business_name=df["trading_name"].str.strip(),
                    clue_id=df["property_id"] + "-" + df.groupby("property_id").cumcount().astype(str))[
        ["clue_id", "business_name", "latitude", "longitude", TAX.VALUE_COLUMN,
         "ClassificationCode", "clue_small_area"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
