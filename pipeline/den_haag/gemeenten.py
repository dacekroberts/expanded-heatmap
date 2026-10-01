"""Den Haag's gemeente polygons, assembled from the cached OSM boundaries.

Shared by step 1 (which stops are in the gemeente, and where the others lie),
step 2 (which points are in the gemeente) and step 3 (the label focus). Reads
the cache only. Florence's reader (`pipeline/florence/comuni.py`), keyed on
`ref:gemeentecode` as Rotterdam's boundary is.
"""
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline import osm_tram
from pipeline.den_haag import config

FETCH = "pipeline/den_haag/fetch_sources.py"


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    if not lines:
        return None
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def gemeente_polygons(verbose=True):
    """GeoDataFrame of every gemeente in the cache: ref (CBS code), name, geometry."""
    rows = []
    for rel in osm_tram.read_elements(config.OSM_GEMEENTEN_JSON, "gemeente boundaries", FETCH):
        t = rel.get("tags", {})
        if not t.get("ref:gemeentecode"):
            continue
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')}: outer ways did not close into a polygon")
        geom = outer.difference(inner) if inner is not None else outer
        rows.append({"ref": t["ref:gemeentecode"], "name": t["name"], "geometry": geom})
    gdf = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    mine = gdf[gdf["ref"] == config.GEMEENTE_CODE]
    if len(mine) != 1:
        sys.exit(f"expected one gemeente {config.GEMEENTE_CODE}, got {len(mine)}")
    a = float(mine.to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    lo, hi = config.GEMEENTE_AREA_KM2
    if verbose:
        print(f"    Gemeente Den Haag ({config.GEMEENTE_CODE}): {a:.1f} km2; "
              f"{len(gdf)} gemeenten in the box")
    if not lo <= a <= hi:
        sys.exit(f"Den Haag is {a:.1f} km2, outside {lo}-{hi}: the rings assembled wrong")
    return gdf


def gemeente_geometry():
    """The Gemeente Den Haag - scope and label focus."""
    gdf = gemeente_polygons(verbose=False)
    return unary_union(list(gdf[gdf["ref"] == config.GEMEENTE_CODE].geometry))
