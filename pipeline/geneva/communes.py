"""Geneva (Regional)'s commune polygons, assembled from the cached OSM
boundaries.

Shared by step 1 (which stops are in the 12 tram communes, and which commune
the others lie in), step 2 (which register points are in scope) and step 3
(the label focus). Reads the cache only. Zurich's `gemeinden.py`, keyed on
swisstopo's BFS number for the Swiss communes and on INSEE's code for the
French ones, which only name where an outside stop lies.
"""
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline import osm_tram
from pipeline.geneva import config

FETCH = "pipeline/geneva/fetch_sources.py"


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    if not lines:
        return None
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def commune_polygons(verbose=True):
    """GeoDataFrame of every commune in the cache: ref (BFS number, or
    "FR-" + INSEE code), name, geometry; the 12 in scope checked by name and
    their summed area gated."""
    rows = []
    for rel in osm_tram.read_elements(config.OSM_COMMUNES_JSON, "commune boundaries", FETCH):
        t = rel.get("tags", {})
        ref = t.get(config.BFS_TAG) or (f"FR-{t['ref:INSEE']}" if t.get("ref:INSEE") else None)
        if not ref:
            continue
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')}: outer ways did not close into a polygon")
        geom = outer.difference(inner) if inner is not None else outer
        rows.append({"ref": ref, "name": t["name"], "relation": rel["id"], "geometry": geom})
    gdf = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    scope = gdf[gdf["ref"].isin(config.COMMUNES)]
    got = dict(zip(scope["ref"], scope["name"]))
    if got != config.COMMUNES:
        sys.exit(f"the 12 communes do not match config.COMMUNES: missing "
                 f"{sorted(set(config.COMMUNES) - set(got))}, renamed "
                 f"{sorted(k for k in got if got[k] != config.COMMUNES.get(k))}")
    a = float(scope.to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    lo, hi = config.REGION_AREA_KM2
    if verbose:
        print(f"    the 12 tram communes: {a:.1f} km2; {len(gdf)} communes in the box")
    if not lo <= a <= hi:
        sys.exit(f"the 12 communes sum to {a:.1f} km2, outside {lo}-{hi}: the rings "
                 f"assembled wrong")
    return gdf


def region_geometry():
    """The 12 tram communes as one shape: scope and label focus."""
    gdf = commune_polygons(verbose=False)
    return unary_union(list(gdf[gdf["ref"].isin(config.COMMUNES)].geometry))
