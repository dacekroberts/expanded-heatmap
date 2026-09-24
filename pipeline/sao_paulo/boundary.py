"""São Paulo's município boundary, from the cached OSM relation.

Reads the cache only. The relation is found by its IBGE code
(`IBGE:GEOCODIGO` 3550308) inside a bbox - never by name, which is shared by
the state - polygonised from outer AND inner ways and gated on area.
"""
import json
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline.sao_paulo import config


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    return unary_union(list(polygonize(linemerge(MultiLineString(lines))))) if lines else None


def city_polygon(verbose=True):
    if not config.OSM_BOUNDARY_JSON.exists():
        sys.exit(f"missing {config.OSM_BOUNDARY_JSON}\nRun: python pipeline/sao_paulo/fetch_sources.py")
    rels = [e for e in json.loads(config.OSM_BOUNDARY_JSON.read_text(encoding="utf-8"))["elements"]
            if e["type"] == "relation"]
    if len(rels) != 1 or rels[0]["tags"].get("IBGE:GEOCODIGO") != config.IBGE_MUNICIPIO:
        sys.exit(f"expected exactly the município {config.IBGE_MUNICIPIO}, got "
                 f"{[(r['id'], r['tags'].get('name')) for r in rels]}")
    outer, inner = _rings(rels[0], "outer"), _rings(rels[0], "inner")
    if outer is None or outer.is_empty:
        sys.exit("São Paulo's outer ways did not close into a polygon")
    geom = outer.difference(inner) if inner is not None else outer
    area = gpd.GeoSeries([geom], crs=config.CRS_GEOGRAPHIC).to_crs(
        config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    if verbose:
        print(f"  São Paulo boundary (OSM {rels[0]['id']}): {area:.1f} km2")
    if not lo <= area <= hi:
        sys.exit(f"São Paulo's polygon is {area:.1f} km2, outside {lo}-{hi}")
    return geom


def neighbour_polygons():
    """Every município in the rail bbox, to NAME an excluded station (naming
    only - Line 9's two stations in Osasco)."""
    from pipeline.countries.brazil_boundary import municipios
    return municipios(config.OSM_MUNICIPIOS_JSON, config.CRS_GEOGRAPHIC)
