"""Rome's boundary and its neighbours, assembled from the cached OSM relations.

Shared by step 1 (which stations are inside the comune, and which comune the
others are in) and step 3 (the label focus). Reads the cache only. Relation
41485, "Roma", admin_level 8, ref:ISTAT 058091 - polygonised from outer AND
inner ways and gated on area. (The comune surrounds the Vatican, an inner
ring.)
"""
import json
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline.rome import config


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    return unary_union(list(polygonize(linemerge(MultiLineString(lines))))) if lines else None


def _polygon(rel):
    outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
    if outer is None or outer.is_empty:
        return None
    return outer.difference(inner) if inner is not None else outer


def _read(path):
    if not path.exists():
        sys.exit(f"missing {path}\nRun: python pipeline/rome/fetch_sources.py")
    return json.loads(path.read_text(encoding="utf-8"))["elements"]


def city_polygon(verbose=True):
    rels = [e for e in _read(config.OSM_BOUNDARY_JSON) if e["type"] == "relation"
            and e["id"] == config.OSM_BOUNDARY_RELATION]
    if len(rels) != 1:
        sys.exit(f"expected OSM relation {config.OSM_BOUNDARY_RELATION}")
    if rels[0].get("tags", {}).get("ref:ISTAT") != config.ISTAT_COMUNE:
        sys.exit(f"relation {config.OSM_BOUNDARY_RELATION} is not ISTAT {config.ISTAT_COMUNE}")
    geom = _polygon(rels[0])
    if geom is None:
        sys.exit("Roma's outer ways did not close into a polygon")
    area = gpd.GeoSeries([geom], crs=config.CRS_GEOGRAPHIC).to_crs(
        config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    if verbose:
        print(f"  Roma boundary (OSM {config.OSM_BOUNDARY_RELATION}): {area:.1f} km2")
    if not lo <= area <= hi:
        sys.exit(f"Roma's polygon is {area:.1f} km2, outside {lo}-{hi}")
    return geom


def neighbour_polygons():
    """Every comune in the bbox, to NAME an excluded station (naming only)."""
    rows = []
    for rel in _read(config.OSM_NEIGHBOURS_JSON):
        if rel["type"] != "relation":
            continue
        g = _polygon(rel)
        if g is not None:
            rows.append({"name": rel["tags"].get("name"), "istat": rel["tags"].get("ref:ISTAT"),
                         "geometry": g})
    return gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
