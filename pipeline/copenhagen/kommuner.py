"""Copenhagen's kommune polygons, assembled from the cached OSM boundaries.

Shared by step 1 (which stations are in scope, and where each excluded one
is) and step 3 (the label focus). Reads the cache only.

⚠ INNER RINGS MATTER HERE. Frederiksberg is an enclave, so Kobenhavn's
relation carries it as an inner ring; a polygon built from the outer ways
alone would put Frederiksberg's stations in Kobenhavn.
"""
import json
import sys

import geopandas as gpd
from shapely.geometry import MultiLineString
from shapely.ops import linemerge, polygonize, unary_union

from pipeline.copenhagen import config

# The two kommuner's areas as OSM draws them, measured 2026-09-24; a polygon
# outside these bounds assembled wrong (the usual Overpass boundary failure)
# or is a different kommune.
AREA_KM2 = {"101": (80.0, 110.0), "147": (8.0, 10.0)}


def read_cached(path, label):
    if not path.exists():
        sys.exit(f"missing {label}: {path}\nRun: python pipeline/copenhagen/fetch_sources.py")
    print(f"  {label}: {path.name} ({path.stat().st_size:,} bytes)")
    return json.loads(path.read_text(encoding="utf-8"))["elements"]


def _rings(rel, role):
    lines = [[(p["lon"], p["lat"]) for p in m["geometry"]]
             for m in rel.get("members", [])
             if m.get("type") == "way" and m.get("role") == role and m.get("geometry")]
    if not lines:
        return None
    return unary_union(list(polygonize(linemerge(MultiLineString(lines)))))


def kommune_polygons(verbose=True):
    """GeoDataFrame of every Danish kommune in the cache: ref, kommune, geometry."""
    rows = []
    for rel in read_cached(config.OSM_KOMMUNER_JSON, "kommune boundaries"):
        t = rel.get("tags", {})
        if "ref:scb" in t or not t.get("ref"):
            continue                      # a Swedish kommun across the Sound
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"{t.get('name')}: outer ways did not close into a polygon")
        geom = outer.difference(inner) if inner is not None else outer
        rows.append({"ref": t["ref"], "kommune": t["name"], "geometry": geom})
    gdf = gpd.GeoDataFrame(rows, crs=config.CRS_GEOGRAPHIC)
    area = gdf.to_crs(config.CRS_PROJECTED).area / 1e6
    for ref, (lo, hi) in AREA_KM2.items():
        a = float(area[gdf["ref"] == ref].sum())
        name = gdf.loc[gdf["ref"] == ref, "kommune"].iloc[0]
        if verbose:
            print(f"    {ref} {name:<24} {a:6.1f} km2")
        if not lo <= a <= hi:
            sys.exit(f"{name} is {a:.1f} km2, outside {lo}-{hi}: the rings assembled "
                     f"wrong or this is not the kommune")
    s101 = gdf.loc[gdf["ref"] == "101"].geometry.iloc[0]
    s147 = gdf.loc[gdf["ref"] == "147"].geometry.iloc[0]
    overlap = gpd.GeoSeries([s101.intersection(s147)], crs=config.CRS_GEOGRAPHIC
                            ).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    if verbose:
        print(f"    Kobenhavn/Frederiksberg overlap {overlap:.3f} km2 (the enclave's hole)")
    if overlap > 0.05:
        sys.exit("Kobenhavn's polygon covers Frederiksberg - its inner ring was lost")
    return gdf


def scope_geometry():
    """Kobenhavn and Frederiksberg as one shape - the map's label focus."""
    gdf = kommune_polygons(verbose=False)
    return unary_union(list(gdf[gdf["ref"].isin(config.KOMMUNER)].geometry))
