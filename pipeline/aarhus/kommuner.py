"""Aarhus's kommune polygons, assembled from the cached OSM boundaries.

Shared by step 1 (which stations are in the kommune, and where each other one
is) and step 3 (the label focus). Reads the cache only. Copenhagen's reader,
with Aarhus's area bound and no enclave check (Aarhus Kommune encloses none).
"""
import json
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline.aarhus import config

# Aarhus Kommune as OSM draws it: 471.2 km2 (the brief, 2026-09-29). A polygon
# outside these bounds assembled wrong or is a different kommune.
AREA_KM2 = {"751": (460.0, 480.0)}


def read_cached(path, label):
    if not path.exists():
        sys.exit(f"missing {label}: {path}\nRun: python pipeline/aarhus/fetch_sources.py")
    print(f"  {label}: {path.name} ({path.stat().st_size:,} bytes)")
    return json.loads(path.read_text(encoding="utf-8"))["elements"]


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    if not lines:
        return None
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def kommune_polygons(verbose=True):
    """GeoDataFrame of every kommune in the cache: ref, kommune, geometry."""
    rows = []
    for rel in read_cached(config.OSM_KOMMUNER_JSON, "kommune boundaries"):
        t = rel.get("tags", {})
        if not t.get("ref"):
            continue
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')}: outer ways did not close into a polygon")
        geom = outer.difference(inner) if inner is not None else outer
        rows.append({"ref": t["ref"], "kommune": t["name"], "geometry": geom})
    gdf = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    area = gdf.to_crs(config.CRS_PROJECTED).area / 1e6
    for ref, (lo, hi) in AREA_KM2.items():
        a = float(area[gdf["ref"] == ref].sum())
        name = gdf.loc[gdf["ref"] == ref, "kommune"].iloc[0]
        if verbose:
            print(f"    {ref} {name:<24} {a:6.1f} km2")
        if not lo <= a <= hi:
            sys.exit(f"{name} is {a:.1f} km2, outside {lo}-{hi}: the rings assembled "
                     f"wrong or this is not the kommune")
    return gdf


def scope_geometry():
    """Aarhus Kommune - the map's label focus."""
    gdf = kommune_polygons(verbose=False)
    return unary_union(list(gdf[gdf["ref"].isin(config.KOMMUNER)].geometry))
