"""The owner's build check for Rome's 2.60x food-and-drink control.

    python pipeline/rome/build_check.py

NOT a step (drift_check never runs it) - a measurement for the owner's call,
reading only cached files: step 2's output and OSM's food places.

The brief found SUAP's food-and-drink establishments at 2.60x OpenStreetMap's,
above France's 1.26-1.80x and Prague's 1.63x. Two readings: the register has
no closure date, so ceased premises may linger; or OSM under-maps Rome's bars.
The owner asked for SUAP compared with OSM street by street and the excess
split by start year, then either an age cut-off or a stated over-count.

What this measures, since a register row and an OSM node never share a key:
for each SUAP food premises, whether an OSM food place lies within MATCH_M.
If lingering closures drive the excess, the OLDEST registrations should match
far less often than recent ones; if OSM simply under-maps, the match rate
should be flat across start years and low everywhere.
"""
import json
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.rome import config  # noqa: E402

MATCH_M = 30
BANDS = [(0, 1979), (1980, 1989), (1990, 1999), (2000, 2009), (2010, 2014), (2015, 2019),
         (2020, 2022), (2023, 2025)]


def main():
    b = pd.read_csv(config.BUSINESSES_CLEAN_CSV)
    food = b[b["activity"].isin(["Restaurant, bar or café", "Bar or club with entertainment",
                                 "Bookshop café"])].copy()
    osm = json.loads(config.OSM_FOOD_JSON.read_text(encoding="utf-8"))["elements"]
    pts = [(e.get("lat") or e.get("center", {}).get("lat"), e.get("lon") or e.get("center", {}).get("lon"),
            e["tags"].get("amenity")) for e in osm]
    o = pd.DataFrame(pts, columns=["lat", "lon", "amenity"]).dropna()
    print(f"SUAP food-and-drink premises (Somministrazione), placed: {len(food):,}")
    print(f"OSM food-and-drink places in the comune: {len(o):,}  "
          f"({', '.join(f'{k} {v:,}' for k, v in o['amenity'].value_counts().items())})")
    print(f"ratio {len(food) / len(o):.2f}x")

    g = gpd.GeoDataFrame(food, geometry=gpd.points_from_xy(food["longitude"], food["latitude"]),
                         crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    og = gpd.GeoDataFrame(o, geometry=gpd.points_from_xy(o["lon"], o["lat"]),
                          crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    near = gpd.sjoin_nearest(g, og[["geometry"]], how="left", distance_col="d", max_distance=MATCH_M)
    near = near[~near.index.duplicated()]
    food["matched"] = near["d"].notna().reindex(food.index).fillna(False).values
    print(f"\nshare of SUAP food premises with an OSM food place within {MATCH_M} m: "
          f"{food['matched'].mean():.1%}")

    print("\nby start year (DATA_INIZIO):")
    print(f"  {'band':<11} {'premises':>9} {'matched':>8} {'share of all':>13}")
    rows = []
    for lo, hi in BANDS:
        m = food["start_year"].between(lo, hi)
        n = int(m.sum())
        rows.append((lo, hi, n, food.loc[m, "matched"].mean() if n else np.nan))
        print(f"  {lo if lo else '<':>4}-{hi:<6} {n:>9,} {food.loc[m, 'matched'].mean():>8.1%} "
              f"{n / len(food):>13.1%}")
    unk = food["start_year"].isna()
    if unk.any():
        print(f"  no start date {int(unk.sum()):>6,} {food.loc[unk, 'matched'].mean():>8.1%}")

    print("\nwhat an age cut-off would leave (food premises started in or after the year):")
    for cut in (1980, 1990, 2000, 2005, 2010):
        kept = food["start_year"] >= cut
        print(f"  from {cut}: {int(kept.sum()):>7,}  ratio to OSM {kept.sum() / len(o):.2f}x")

    # street by street: the streets with the most SUAP food premises
    food["via"] = food["business_name"].str.replace(r"\s+\d.*$", "", regex=True)
    top = food.groupby("via").agg(n=("matched", "size"), matched=("matched", "mean")).sort_values(
        "n", ascending=False).head(12)
    print("\nthe twelve streets with the most SUAP food premises:")
    for via, r in top.iterrows():
        print(f"  {via[:34]:<34} {int(r['n']):>4}  matched {r['matched']:.0%}")


if __name__ == "__main__":
    main()
