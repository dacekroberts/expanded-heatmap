"""Brazilian município polygons from a cached OSM query - shared by every
Brazilian city, for two jobs: the SCOPE polygon (one município, or the union a
regional page covers) and NAMING a station that falls outside it.

The query each city's fetch_sources.py runs is every admin_level-8 relation
carrying `IBGE:GEOCODIGO` inside the city's bbox, `out geom`. Relations are
found by IBGE code, never by name - São Paulo shares its name with its state,
and Guadalajara's name search once returned a Spanish province - and
polygonised from outer AND inner ways.
"""
import json
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    return unary_union(list(polygonize(linemerge(MultiLineString(lines))))) if lines else None


def municipios(path, crs="EPSG:4326"):
    """GeoDataFrame(name, ibge, geometry) of every município in the cache."""
    if not path.exists():
        sys.exit(f"missing {path}\nRun the city's fetch_sources.py first.")
    rows = []
    for rel in json.loads(path.read_text(encoding="utf-8"))["elements"]:
        if rel["type"] != "relation":
            continue
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            continue
        g = outer.difference(inner) if inner is not None else outer
        rows.append({"name": rel["tags"].get("name"), "ibge": rel["tags"].get("IBGE:GEOCODIGO"),
                     "osm_id": rel["id"], "geometry": g})
    return gpd.GeoDataFrame(rows, crs=crs)


def in_codes(code, codes):
    """True when an OSM `IBGE:GEOCODIGO` belongs to one of the scope's codes -
    exactly, or as a sub-unit carrying the município's code as its prefix."""
    code = str(code or "")
    return any(code == c or code.startswith(c) for c in codes)


def scope_polygon(path, codes, area_km2, crs_projected, label, verbose=True):
    """The union of the listed municípios, gated on total area (km2, lo-hi).

    A município OSM maps only as its SUB-UNITS is assembled from them: Brasília
    (5300108) is the whole Federal District, and OSM carries no relation for it
    at admin_level 8 - only its 35 administrative regions, each coded
    5300108xxxx. So an exact code must appear exactly once, or not at all and
    then as one or more prefixed sub-units, printed."""
    m = municipios(path)
    parts = []
    for code in codes:
        hit = m[m["ibge"] == code]
        if len(hit) > 1:
            sys.exit(f"{label}: município {code} appears {len(hit)} times in {path.name}")
        if len(hit) == 0:
            hit = m[m["ibge"].astype(str).str.startswith(code)]
            if len(hit) == 0:
                sys.exit(f"{label}: município {code} is not in {path.name}, whole or in parts")
            if verbose:
                print(f"  {label}: {code} assembled from {len(hit)} sub-units coded {code}...")
            hit = [{"name": f"{code} ({len(hit)} sub-units)",
                    "geometry": unary_union(list(hit["geometry"]))}]
        else:
            hit = [hit.iloc[0]]
        parts.extend(hit)
    geom = unary_union([p["geometry"] for p in parts])
    area = gpd.GeoSeries([geom], crs=m.crs).to_crs(crs_projected).area.iloc[0] / 1e6
    lo, hi = area_km2
    if verbose:
        print(f"  {label} scope: {' + '.join(p['name'] for p in parts)} = {area:.1f} km2")
    if not lo <= area <= hi:
        sys.exit(f"{label}: scope polygon is {area:.1f} km2, outside {lo}-{hi}")
    return geom
