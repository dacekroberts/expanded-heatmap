"""The Brazilian build check: WHERE the unclassifiable rows sit, by distance
from the nearest station - the share the page states. Shared; each city's
build_check.py calls ring_bands(config). Not a step: it reads step 1's and
step 2's outputs and writes nothing.

São Paulo (2026-09-24): 40.0% of the rows that could be storefronts were
unreadable inside the rings, 30.6% beyond - station areas are commercial
districts of bare trade names, so the map under-draws exactly where it looks.
"""
import sys

import geopandas as gpd
import pandas as pd


def _nearest_m(df, stations, cfg):
    pts = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
                           crs=cfg.CRS_GEOGRAPHIC).to_crs(cfg.CRS_PROJECTED)
    return gpd.sjoin_nearest(pts, stations, distance_col="d_m")["d_m"].groupby(level=0).min()


def ring_bands(cfg):
    for p in (cfg.STATIONS_CSV, cfg.BUSINESSES_CLEAN_CSV, cfg.UNCLASSIFIED_CSV):
        if not p.exists():
            sys.exit(f"Missing {p}. Run steps 1 and 2 first.")
    st = pd.read_csv(cfg.STATIONS_CSV)
    stations = gpd.GeoDataFrame(geometry=gpd.points_from_xy(st["longitude"], st["latitude"]),
                                crs=cfg.CRS_GEOGRAPHIC).to_crs(cfg.CRS_PROJECTED)
    kept = pd.read_csv(cfg.BUSINESSES_CLEAN_CSV, usecols=["latitude", "longitude"])
    dropped = pd.read_csv(cfg.UNCLASSIFIED_CSV, usecols=["latitude", "longitude"])
    kept["d_m"] = _nearest_m(kept, stations, cfg)
    dropped["d_m"] = _nearest_m(dropped, stations, cfg)
    edges = cfg.RING_EDGES_METERS + [float("inf")]
    labels = cfg.RING_LABELS + ["beyond 0.6 mi"]
    print(f"{cfg.NAME}: unclassifiable share of possible storefronts, by distance from the nearest station")
    print(f"  {'band':<14} {'drawn':>9} {'dropped':>9} {'dropped share':>14}")
    for lo, hi, lab in zip(edges[:-1], edges[1:], labels):
        k = int(kept["d_m"].between(lo, hi, inclusive="left").sum())
        d = int(dropped["d_m"].between(lo, hi, inclusive="left").sum())
        print(f"  {lab:<14} {k:>9,} {d:>9,} {d / max(k + d, 1):>13.1%}")
    ring = cfg.RING_EDGES_METERS[-1]
    ki, di = int((kept["d_m"] < ring).sum()), int((dropped["d_m"] < ring).sum())
    ko, do = len(kept) - ki, len(dropped) - di
    print(f"  {'within rings':<14} {ki:>9,} {di:>9,} {di / max(ki + di, 1):>13.1%}")
    print(f"  {'outside rings':<14} {ko:>9,} {do:>9,} {do / max(ko + do, 1):>13.1%}")
    print(f"  {'city-wide':<14} {len(kept):>9,} {len(dropped):>9,} "
          f"{len(dropped) / max(len(kept) + len(dropped), 1):>13.1%}")
    print(f"  storefronts within a ring: {ki:,} of {len(kept):,} ({ki / max(len(kept), 1):.1%})")
