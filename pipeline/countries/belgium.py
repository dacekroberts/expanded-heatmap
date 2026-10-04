"""Belgium: the facts shared by the Belgian cities, and the commune polygons.

Belgium is bespoke per region, not one national register (Spain's shape, not
France's): the City of Brussels has hub.brussels's shop inventory, Antwerp and
Ghent FAVV-AFSCA's food list placed on Flanders' VKBO, Charleroi and Liege
Wallonia's LoGIC survey, and Brussels (Regional) KBO on BeST-Address. What the
cities do share is cached once, in `data/belgium/raw/` (the FAVV list, the
LoGIC GeoPackage, the KBO file, BeST-Address Brussels), and the way a commune
polygon is read from OpenStreetMap.

Commune polygons outside Brussels come from OpenStreetMap: every Belgian
municipality is an `admin_level` 8 relation carrying its NIS (INS) code as
`ref:INS`. One Overpass query per city fetches every municipality in the
city's rail box, so a stop outside the city can be named. The query lives in
`pipeline/countries/belgium_fetch.py`; this module only reads the cache.
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent
SHARED_RAW = _ROOT / "data" / "belgium" / "raw"

FAVV_CSV = SHARED_RAW / "inter_actieve_actoren_EN.csv"
LOGIC_GPKG = SHARED_RAW / "logic" / "LOGIC_2024.gpkg"
KBO_ZIP = SHARED_RAW / "KboOpenData_0501_2026_10_03_Full.zip"
BEST_BRUSSELS_ZIP = SHARED_RAW / "openaddress-bebru.zip"

# Every Belgian city projects to UTM 31N: the country runs from 2.5 to 6.4
# degrees E and every built or planned city lies west of 6 degrees E.
CRS_GEOGRAPHIC = "EPSG:4326"
CRS_PROJECTED = "EPSG:32631"

# The OSM tag that carries a municipality's NIS code.
NIS_TAG = "ref:INS"


def _rings(rel, role):
    from shapely.geometry import MultiLineString
    from shapely.ops import linemerge, polygonize, unary_union
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    if not lines:
        return None
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def commune_polygons(cache_json, fetch_script, own_nis, area_km2, label, verbose=True):
    """GeoDataFrame of every commune in an OSM cache: nis, name, geometry.

    `own_nis` is the city's NIS code (a string); `area_km2` a (low, high) gate
    on its polygon, so rings that assembled wrong stop the build. Reads the
    cache only; a missing cache exits naming `fetch_script`.
    """
    import json

    import geopandas as gpd

    if not cache_json.exists():
        sys.exit(f"{cache_json} missing: run python {fetch_script}")
    elements = json.loads(cache_json.read_text(encoding="utf-8"))["elements"]
    rows = []
    for rel in elements:
        t = rel.get("tags", {})
        if rel.get("type") != "relation" or not t.get(NIS_TAG):
            continue
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')}: outer ways did not close into a polygon")
        geom = outer.difference(inner) if inner is not None else outer
        rows.append({"nis": t[NIS_TAG], "name": t.get("name", t[NIS_TAG]),
                     "geometry": geom})
    gdf = gpd.GeoDataFrame(rows, crs=CRS_GEOGRAPHIC)
    mine = gdf[gdf["nis"] == own_nis]
    if len(mine) != 1:
        sys.exit(f"expected one commune {own_nis}, got {len(mine)}")
    a = float(mine.to_crs(CRS_PROJECTED).area.sum() / 1e6)
    lo, hi = area_km2
    if verbose:
        print(f"    {label} ({own_nis}): {a:.1f} km2; {len(gdf)} communes in the box")
    if not lo <= a <= hi:
        sys.exit(f"{label} is {a:.1f} km2, outside {lo}-{hi}: the rings assembled wrong")
    return gdf


def brussels_region_communes(geojson_path, fetch_script):
    """The Brussels-Capital Region's 19 communes (PARADIGM's commune limits,
    CC0 1.0, opendata.brussels.be): GeoDataFrame nis, name_fr, name_nl,
    geometry in EPSG:4326. The City and Brussels (Regional) both read it."""
    import geopandas as gpd

    if not geojson_path.exists():
        sys.exit(f"{geojson_path} missing: run python {fetch_script}")
    gdf = gpd.read_file(geojson_path)
    gdf = gdf.set_crs(CRS_GEOGRAPHIC) if gdf.crs is None else gdf.to_crs(CRS_GEOGRAPHIC)
    gdf = gdf.rename(columns={"national_code": "nis"})[["nis", "name_fr", "name_nl", "geometry"]]
    if len(gdf) != 19 or gdf["nis"].nunique() != 19:
        sys.exit(f"{geojson_path.name}: {len(gdf)} features, expected the Region's 19 communes")
    return gdf


def commune_geometry(cache_json, fetch_script, own_nis, area_km2, label):
    """The city's own commune polygon (EPSG:4326): scope and label focus."""
    from shapely.ops import unary_union
    gdf = commune_polygons(cache_json, fetch_script, own_nis, area_km2, label,
                           verbose=False)
    return unary_union(list(gdf[gdf["nis"] == own_nis].geometry))
