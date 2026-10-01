"""Florence's comune polygons, assembled from the cached OSM boundaries.

Shared by step 1 (which stops are in the comune, and where the others lie),
step 2 (which points are in the comune) and step 3 (the label focus). Reads the
cache only. Odense's reader, keyed on `ref:ISTAT`.
"""
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline import osm_tram
from pipeline.florence import config

FETCH = "pipeline/florence/fetch_sources.py"


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    if not lines:
        return None
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def comune_polygons(verbose=True):
    """GeoDataFrame of every comune in the cache: ref (ISTAT), name, geometry."""
    rows = []
    for rel in osm_tram.read_elements(config.OSM_COMUNI_JSON, "comune boundaries", FETCH):
        t = rel.get("tags", {})
        if not t.get("ref:ISTAT"):
            continue
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')}: outer ways did not close into a polygon")
        geom = outer.difference(inner) if inner is not None else outer
        rows.append({"ref": t["ref:ISTAT"], "name": t["name"], "geometry": geom})
    gdf = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    a = float(gdf[gdf["ref"] == config.ISTAT_FIRENZE].to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    lo, hi = config.COMUNE_AREA_KM2
    if verbose:
        print(f"    Comune di Firenze ({config.ISTAT_FIRENZE}): {a:.1f} km2; "
              f"{len(gdf)} comuni in the box")
    if not lo <= a <= hi:
        sys.exit(f"Firenze is {a:.1f} km2, outside {lo}-{hi}: the rings assembled wrong")
    return gdf


def comune_geometry():
    """The Comune di Firenze - scope and label focus."""
    gdf = comune_polygons(verbose=False)
    return unary_union(list(gdf[gdf["ref"] == config.ISTAT_FIRENZE].geometry))
