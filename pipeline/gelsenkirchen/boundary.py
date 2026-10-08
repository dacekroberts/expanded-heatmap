"""Gelsenkirchen's city polygon and its neighbours', assembled from the cached
OpenStreetMap boundaries (owner, 2026-10-05, call 2: the OSM boundary from
the build's one Overpass query).

Shared by step 1 (which stops are in the city, and which city the others lie
in), step 2 (which survey points are in scope) and step 3 (the label focus).
Reads the cache only. Geneva's `communes.py`, keyed on the official
municipality key (de:amtlicher_gemeindeschluessel) rather than a name.
"""
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline import osm_tram
from pipeline.gelsenkirchen import config


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    if not lines:
        return None
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def place_polygons(verbose=True):
    """GeoDataFrame of every municipality in the cache: ref (the 8-digit
    municipality key), name, relation, admin_level, geometry. A district
    (Kreis) carries no 8-digit key and is skipped, so its municipalities
    alone stand for it; one key at two levels is kept once. The city itself
    is checked by key and area."""
    rows = []
    for rel in osm_tram.read_elements(config.OSM_BOUNDARIES_JSON, "boundaries", config.FETCH):
        t = rel.get("tags", {})
        ags = t.get(config.AGS_TAG, "")
        if len(ags) != 8 or not ags.isdigit():
            continue
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')}: outer ways did not close into a polygon")
        geom = outer.difference(inner) if inner is not None else outer
        rows.append({"ref": ags, "name": t.get("name"), "relation": rel["id"],
                     "admin_level": t.get("admin_level"), "geometry": geom})
    gdf = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    gdf = gdf.sort_values(["ref", "admin_level"]).drop_duplicates("ref").reset_index(drop=True)
    city = gdf[gdf["ref"] == config.CITY_AGS]
    if len(city) != 1 or city.iloc[0]["name"] != config.NAME:
        sys.exit(f"no single polygon keyed {config.CITY_AGS} named {config.NAME!r} in the cache")
    a = float(city.to_crs(config.CRS_PROJECTED).area.sum() / 1e6)
    lo, hi = config.CITY_AREA_KM2
    if verbose:
        print(f"    {config.NAME}: relation {int(city.iloc[0]['relation'])}, {a:.1f} km2; "
              f"{len(gdf)} municipalities in the cache: "
              + ", ".join(sorted(gdf["name"])))
    if not lo <= a <= hi:
        sys.exit(f"{config.NAME}'s polygon is {a:.1f} km2, outside {lo}-{hi}: the rings "
                 f"assembled wrong")
    return gdf


def city_geometry():
    """The city as one shape (EPSG:4326): scope and label focus."""
    gdf = place_polygons(verbose=False)
    return unary_union(list(gdf[gdf["ref"] == config.CITY_AGS].geometry))
