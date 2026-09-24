"""São Paulo build check: WHERE does the unclassifiable fifth sit, measured
by distance from a station - the question the brief left open.

    python pipeline/sao_paulo/build_check.py

The brief measured the dropped share by LOCALITY (13% in Lageado, 31% in
Pinheiros) - affluent commercial districts write bare trade names, so they are
under-drawn. The map shows rings around stations, so the share that matters is
the one inside each ring band. Not a step: it reads step 1's and step 2's
outputs and writes nothing.
"""
import sys
from pathlib import Path

import geopandas as gpd
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.sao_paulo import config  # noqa: E402


def _nearest_m(df, stations):
    pts = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
                           crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    return gpd.sjoin_nearest(pts, stations, distance_col="d_m")["d_m"].groupby(level=0).min()


def main():
    for p in (config.STATIONS_CSV, config.BUSINESSES_CLEAN_CSV, config.UNCLASSIFIED_CSV):
        if not p.exists():
            sys.exit(f"Missing {p}. Run steps 1 and 2 first.")
    st = pd.read_csv(config.STATIONS_CSV)
    stations = gpd.GeoDataFrame(geometry=gpd.points_from_xy(st["longitude"], st["latitude"]),
                                crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED)
    kept = pd.read_csv(config.BUSINESSES_CLEAN_CSV, usecols=["latitude", "longitude"])
    dropped = pd.read_csv(config.UNCLASSIFIED_CSV, usecols=["latitude", "longitude"])
    kept["d_m"] = _nearest_m(kept, stations)
    dropped["d_m"] = _nearest_m(dropped, stations)

    edges = config.RING_EDGES_METERS + [float("inf")]
    labels = config.RING_LABELS + ["beyond 0.6 mi"]
    print("Unclassifiable share of establishment rows, by distance from the nearest station")
    print(f"  {'band':<14} {'drawn':>9} {'dropped':>9} {'dropped share':>14}")
    for lo, hi, lab in zip(edges[:-1], edges[1:], labels):
        k = int(kept["d_m"].between(lo, hi, inclusive="left").sum())
        d = int(dropped["d_m"].between(lo, hi, inclusive="left").sum())
        print(f"  {lab:<14} {k:>9,} {d:>9,} {d / (k + d):>13.1%}")
    ring = config.RING_EDGES_METERS[-1]
    ki, di = int((kept["d_m"] < ring).sum()), int((dropped["d_m"] < ring).sum())
    ko, do = len(kept) - ki, len(dropped) - di
    print(f"  {'within rings':<14} {ki:>9,} {di:>9,} {di / (ki + di):>13.1%}")
    print(f"  {'city-wide':<14} {len(kept):>9,} {len(dropped):>9,} "
          f"{len(dropped) / (len(kept) + len(dropped)):>13.1%}")
    print(f"  {'outside rings':<14} {ko:>9,} {do:>9,} {do / (ko + do):>13.1%}")


if __name__ == "__main__":
    main()
