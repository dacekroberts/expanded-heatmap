"""Sydney step 2: the City of Sydney's FES 2022 establishments -> the
storefronts inside the City of Sydney LGA.

    python pipeline/sydney/step2_clean_businesses.py

Reads the cache only (pipeline/sydney/fetch_sources.py downloads). What a
reader should know before trusting the counts printed below:

  * the survey carries NO names or addresses: a pin is titled by its ANZSIC
    class (Berlin's precedent), so no person's name can reach the map;
  * points are the publisher's own, one per establishment but often stacked
    per building (a shopping centre is one coordinate): ring counts are
    unaffected, the stacking is printed;
  * the class list is pipeline/taxonomies/anzsic_fes.py's; an undecided class
    in a storefront division stops the step.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.sydney import config  # noqa: E402
from pipeline.taxonomies import load_taxonomy_module  # noqa: E402

TAX = load_taxonomy_module(config.TAXONOMY_SYSTEM)


def main():
    if not config.FES_JSON.exists():
        sys.exit(f"missing {config.FES_JSON}: run python pipeline/sydney/fetch_sources.py")
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(json.loads(config.FES_JSON.read_text(encoding="utf-8")))
    print(f"  {len(df):,} FES {config.FES_YEAR} establishments")
    if set(df["Year"]) != {config.FES_YEAR}:
        sys.exit(f"  years {sorted(set(df['Year']))} in the cache, expected {config.FES_YEAR} only")

    new = sorted(set(df.loc[df["ClassificationCode"].map(TAX.undecided), "ClassificationCode"]))
    if new:
        sys.exit(f"  storefront-division class(es) the taxonomy has not decided: {new}")
    excl = df[df["ClassificationCode"].isin(TAX.EXCLUDED)]
    print("  excluded by class:")
    for code, n in excl["ClassificationCode"].value_counts().items():
        print(f"    {code} {TAX.EXCLUDED[code]:<62} {n:>4}")

    df = df.assign(bucket=df.apply(lambda r: TAX.classify(r.to_dict()), axis=1))
    df = df[df["bucket"].notna()]
    print(f"  {len(df):,} storefronts; " + ", ".join(f"{b} {n:,}" for b, n in df["bucket"].value_counts().items()))
    for code in sorted(TAX.CATCH_ALL_CODES):
        n = int((df["ClassificationCode"] == code).sum())
        print(f"    catch-all {code}: {n:,}")

    box = config.SYDNEY_BBOX
    in_box = df["latitude"].between(box["lat_min"], box["lat_max"]) & \
        df["longitude"].between(box["lon_min"], box["lon_max"])
    print(f"  {int((~in_box).sum()):,} outside the sanity box, dropped")
    df = df[in_box]
    area = gpd.read_file(config.CITY_BOUNDARY_GEOJSON).to_crs(config.CRS_PROJECTED).union_all()
    pts = gpd.GeoSeries(gpd.points_from_xy(df["longitude"], df["latitude"]), index=df.index,
                        crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    inside = pts.within(area)
    print(f"  {int((~inside).sum()):,} outside the City of Sydney (OSM relation "
          f"{config.BOUNDARY_OSM_RELATION}), dropped")
    df = df[inside]

    xy = pts[inside].map(lambda p: (round(p.x), round(p.y)))
    stack = xy.map(xy.value_counts())
    print(f"  {xy.nunique():,} distinct points (1 m); {(stack == 1).mean():.1%} alone, "
          f"{(stack >= 10).mean():.1%} in stacks of 10 or more, the largest {int(stack.max())}")

    out = df.rename(columns={"OBJECTID": "fes_id"}).assign(
        business_name=df[TAX.VALUE_COLUMN])[
        ["fes_id", "business_name", "latitude", "longitude", TAX.VALUE_COLUMN,
         "ClassificationCode", "Village"]]
    out.to_csv(config.BUSINESSES_CLEAN_CSV, index=False, encoding="utf-8")
    print(f"\n  {len(out):,} storefronts -> {config.BUSINESSES_CLEAN_CSV.relative_to(config.ROOT)}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
