"""Amsterdam's boundary, assembled from the cached OSM relation.

Shared by step 1 (which stations are inside the gemeente), step 2 (a check
that both layers really are gemeente-only) and step 3 (the label focus).
Reads the cache only. Relation 47811, "Amsterdam", admin_level 8,
ref:gemeentecode 0363 - Weesp included since 2022 - polygonised from outer AND
inner ways and gated on area.
"""
import json
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline.amsterdam import config


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    return unary_union(list(polygonize(linemerge(MultiLineString(lines))))) if lines else None


def city_polygon(verbose=True):
    if not config.OSM_BOUNDARY_JSON.exists():
        sys.exit(f"missing {config.OSM_BOUNDARY_JSON}\n"
                 f"Run: python pipeline/amsterdam/fetch_sources.py")
    els = json.loads(config.OSM_BOUNDARY_JSON.read_text(encoding="utf-8"))["elements"]
    rels = [e for e in els if e["type"] == "relation"
            and e["id"] == config.OSM_BOUNDARY_RELATION]
    if len(rels) != 1:
        sys.exit(f"expected OSM relation {config.OSM_BOUNDARY_RELATION}, got "
                 f"{[e.get('id') for e in els]}")
    tags = rels[0].get("tags", {})
    if tags.get("ref:gemeentecode") != config.GEMEENTE_CODE:
        sys.exit(f"relation {config.OSM_BOUNDARY_RELATION} is gemeentecode "
                 f"{tags.get('ref:gemeentecode')!r}, not {config.GEMEENTE_CODE}")
    outer, inner = _rings(rels[0], "outer"), _rings(rels[0], "inner")
    if outer is None or outer.is_empty:
        sys.exit("Amsterdam's outer ways did not close into a polygon")
    geom = outer.difference(inner) if inner is not None else outer
    area = gpd.GeoSeries([geom], crs=config.CRS_GEOGRAPHIC).to_crs(
        config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    if verbose:
        print(f"  Amsterdam boundary (OSM {config.OSM_BOUNDARY_RELATION}): {area:.1f} km2")
    if not lo <= area <= hi:
        sys.exit(f"Amsterdam's polygon is {area:.1f} km2, outside {lo}-{hi}: the rings "
                 f"assembled wrong or this is not the gemeente")
    return geom
