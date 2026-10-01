"""Göteborg's kommun polygons, assembled from the cached OSM boundaries.

Shared by step 1 (which stops are in Göteborgs Stad, and where the others lie),
step 2 (which premises are in it) and step 3 (the label focus). Reads the cache
only. Florence's `comuni.py`, keyed on `ref:scb`.
"""
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline import osm_tram
from pipeline.goteborg import config

FETCH = "pipeline/goteborg/fetch_sources.py"


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    if not lines:
        return None
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def kommun_polygons(verbose=True):
    """GeoDataFrame of every kommun in the cache: ref (SCB code), name, geometry."""
    rows = []
    for rel in osm_tram.read_elements(config.OSM_KOMMUNER_JSON, "kommun boundaries", FETCH):
        t = rel.get("tags", {})
        if rel.get("type") != "relation" or not t.get("ref:scb"):
            continue
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')}: outer ways did not close into a polygon")
        geom = outer.difference(inner) if inner is not None else outer
        rows.append({"ref": t["ref:scb"], "name": t["name"], "osm_id": rel["id"],
                     "geometry": geom})
    gdf = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    gbg = gdf[gdf["ref"] == config.GOTEBORG_SCB]
    if len(gbg) != 1 or int(gbg["osm_id"].iloc[0]) != config.GOTEBORG_RELATION:
        sys.exit(f"Göteborgs Stad (ref:scb {config.GOTEBORG_SCB}, relation "
                 f"{config.GOTEBORG_RELATION}) is not exactly one polygon in the cache")
    a = float(gbg.to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    lo, hi = config.KOMMUN_AREA_KM2
    if verbose:
        print(f"    Göteborgs Stad ({config.GOTEBORG_SCB}): {a:.1f} km2; "
              f"{len(gdf)} kommuner in the cache ({', '.join(sorted(gdf['name']))})")
    if not lo <= a <= hi:
        sys.exit(f"Göteborgs Stad is {a:.1f} km2, outside {lo}-{hi}: the rings assembled wrong")
    return gdf


def goteborg_geometry():
    """Göteborgs Stad - scope and label focus."""
    gdf = kommun_polygons(verbose=False)
    return unary_union(list(gdf[gdf["ref"] == config.GOTEBORG_SCB].geometry))
