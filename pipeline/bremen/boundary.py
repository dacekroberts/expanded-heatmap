"""Bremen's place polygons, assembled from the cached OSM boundaries.

Shared by step 1 (which stops are in the City of Bremen, and where the others
lie), step 2 (the cross-check of the survey's Gemeinde field) and step 3 (the
label focus). Reads the cache only. Geneva's `communes.py`, keyed on the
Amtlicher Gemeindeschlüssel: the Stadtgemeinde Bremen (04011000), never the
Land, and Lilienthal, which only names where line 4's outside stops lie.
"""
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline import osm_tram
from pipeline.bremen import config

FETCH = "pipeline/bremen/fetch_sources.py"


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    if not lines:
        return None
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def place_polygons(verbose=True):
    """GeoDataFrame of the places in config.PLACES: ref (AGS), name, relation,
    geometry (EPSG:4326). Each place is checked by name, exactly one relation
    per AGS, and the city's area gated."""
    rows = []
    for rel in osm_tram.read_elements(config.OSM_BOUNDARY_JSON, "boundaries", FETCH):
        t = rel.get("tags", {})
        ref = t.get(config.AGS_TAG)
        if ref not in config.PLACES:
            continue
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')} ({ref}): outer ways did not close into a polygon")
        geom = outer.difference(inner) if inner is not None else outer
        rows.append({"ref": ref, "name": t.get("name"), "relation": rel["id"],
                     "admin_level": t.get("admin_level"), "geometry": geom})
    gdf = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    if gdf.empty or gdf["ref"].duplicated().any():
        sys.exit(f"boundaries: expected one relation per AGS in {sorted(config.PLACES)}, got "
                 f"{gdf[['ref', 'name', 'relation']].to_dict('records') if len(gdf) else 'none'}")
    got = dict(zip(gdf["ref"], gdf["name"]))
    if got != config.PLACES:
        sys.exit(f"the places do not match config.PLACES: OSM has {got}")
    areas = gdf.to_crs(config.CRS_PROJECTED).area / 1e6
    if verbose:
        for (_, r), a in zip(gdf.iterrows(), areas):
            print(f"    {r['name']} (AGS {r['ref']}, relation {r['relation']}, admin_level "
                  f"{r['admin_level']}): {a:.1f} km2")
    city_area = float(areas[gdf["ref"] == config.CITY_AGS].iloc[0])
    lo, hi = config.CITY_AREA_KM2
    if not lo <= city_area <= hi:
        sys.exit(f"the City of Bremen is {city_area:.1f} km2 in OSM, outside {lo}-{hi}: the "
                 f"rings assembled wrong, or the Land was taken for the city")
    return gdf


def city_geometry():
    """The Stadtgemeinde Bremen as one shape (EPSG:4326): scope and label focus."""
    gdf = place_polygons(verbose=False)
    return gdf.loc[gdf["ref"] == config.CITY_AGS, "geometry"].iloc[0]
