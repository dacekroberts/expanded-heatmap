"""A Czech tram city's boundary: one OSM obec relation per obec, from the cache.

Shared by every Czech tram city's step 1 (which stations are inside) and step 3
(the label focus). Reads the cache only - `fetch_sources.py` downloads - so a
step may import it. Prague's `pipeline/prague/boundary.py` is the model and
stays as it is (its relation is the region, admin_level 4).

Two checks, because a boundary is the one input that can be confidently wrong:

  * **the relation's `ref` must END in the RUIAN obec code** - OSM tags a Czech
    obec with the district code plus the obec code (Brno is `CZ0642582786`) -
    so a relation id typed wrong, or a same-named place, cannot pass;
  * **the union's area must fall in the config's range**, taken from the Czech
    Statistical Office's figure, as Prague's is gated on ČÚZK's.

Businesses are never scoped by this polygon: RUIAN's address list per obec
does that. It scopes stations and anchors labels only.
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


def obec_polygons(cfg, verbose=True):
    """{obec code: WGS84 polygon}, each checked on its ref; the union gated on area."""
    if not cfg.OSM_BOUNDARY_JSON.exists():
        sys.exit(f"missing {cfg.OSM_BOUNDARY_JSON}\n"
                 f"Run: python pipeline/{cfg.SLUG}/fetch_sources.py")
    els = json.loads(cfg.OSM_BOUNDARY_JSON.read_text(encoding="utf-8"))["elements"]
    rels = {e["id"]: e for e in els if e["type"] == "relation"}
    out = {}
    for obec, rel_id in cfg.OSM_BOUNDARY_RELATIONS.items():
        rel = rels.get(rel_id)
        if rel is None:
            sys.exit(f"OSM relation {rel_id} (obec {obec}) is not in "
                     f"{cfg.OSM_BOUNDARY_JSON.name}: got {sorted(rels)}")
        ref = rel.get("tags", {}).get("ref", "")
        if not ref.endswith(obec):
            sys.exit(f"OSM relation {rel_id} has ref {ref!r}, which does not end in obec "
                     f"{obec} - the wrong relation")
        outer, inner = _rings(rel, "outer"), _rings(rel, "inner")
        if outer is None or outer.is_empty:
            sys.exit(f"relation {rel_id}'s outer ways did not close into a polygon")
        out[obec] = outer.difference(inner) if inner is not None and not inner.is_empty else outer
    areas = gpd.GeoSeries(list(out.values()), index=list(out),
                          crs=cfg.CRS_GEOGRAPHIC).to_crs(cfg.CRS_PROJECTED).area / 1e6
    total = float(areas.sum())
    lo, hi = cfg.BOUNDARY_AREA_KM2
    if verbose:
        parts = ", ".join(f"{o} {a:.1f}" for o, a in areas.items())
        print(f"  boundary (OSM, {parts} km2): {total:.1f} km2")
    if not lo <= total <= hi:
        sys.exit(f"the boundary is {total:.1f} km2, outside {lo}-{hi}: the rings "
                 f"assembled wrong or these are not the obce")
    return out


def city_polygon(cfg, verbose=True):
    """The union of the city's obce - the map's boundary."""
    return unary_union(list(obec_polygons(cfg, verbose).values()))
