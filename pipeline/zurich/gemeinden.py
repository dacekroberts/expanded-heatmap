"""Zurich's Gemeinde polygons, assembled from the cached OSM boundaries.

Shared by step 1 (which stops are in the Stadt, and which Gemeinde the others
lie in), step 2 (which register points are in the Stadt) and step 3 (the label
focus). Reads the cache only. Florence's `comuni.py`, keyed on swisstopo's BFS
number (`swisstopo:BFS_NUMMER`) instead of ISTAT's code.
"""
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline import osm_tram
from pipeline.zurich import config

FETCH = "pipeline/zurich/fetch_sources.py"


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    if not lines:
        return None
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def gemeinde_polygons(verbose=True):
    """GeoDataFrame of every Gemeinde in the cache: ref (BFS number), name, geometry."""
    rows = []
    for rel in osm_tram.read_elements(config.OSM_GEMEINDEN_JSON, "Gemeinde boundaries", FETCH):
        t = rel.get("tags", {})
        if not t.get(config.BFS_TAG):
            continue
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')}: outer ways did not close into a polygon")
        geom = outer.difference(inner) if inner is not None else outer
        rows.append({"ref": t[config.BFS_TAG], "name": t["name"], "relation": rel["id"],
                     "geometry": geom})
    gdf = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    z = gdf[gdf["ref"] == config.BFS_ZURICH]
    if list(z["relation"]) != [config.ZURICH_RELATION]:
        sys.exit(f"BFS {config.BFS_ZURICH} is relation(s) {list(z['relation'])}, not "
                 f"{config.ZURICH_RELATION} - re-read the boundary")
    a = float(z.to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    lo, hi = config.CITY_AREA_KM2
    if verbose:
        print(f"    Stadt Zürich (BFS {config.BFS_ZURICH}): {a:.1f} km2; "
              f"{len(gdf)} Gemeinden in the box")
    if not lo <= a <= hi:
        sys.exit(f"the Stadt is {a:.1f} km2, outside {lo}-{hi}: the rings assembled wrong")
    return gdf


def city_geometry():
    """The Stadt Zürich - scope and label focus."""
    gdf = gemeinde_polygons(verbose=False)
    return unary_union(list(gdf[gdf["ref"] == config.BFS_ZURICH].geometry))
