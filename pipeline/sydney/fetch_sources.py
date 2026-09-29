"""Download Sydney's raw inputs into data/sydney/raw/ (gitignored).

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/sydney/fetch_sources.py [--force]

The City of Sydney's FES "Industry of occupation" layer, the 2022 survey only,
paged out of the feature service in WGS84 and checked against the survey's
own total; the item's licence fields are recorded so a change shows. Then the
LGA boundary and the rail from OpenStreetMap.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.sydney import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def get_json(url, params=None, timeout=300):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        payload = json.loads(r.read())
    if isinstance(payload, dict) and "error" in payload:
        sys.exit(f"  {url[:120]}: {str(payload['error'])[:300]}")
    return payload


def fetch_fes(force):
    if config.FES_JSON.exists() and not force:
        n = len(json.loads(config.FES_JSON.read_text(encoding="utf-8")))
        print(f"  {'fes_2022':28} cached ({n:,} rows)")
        return
    q = config.FES_LAYER_URL + "/query"
    where = f"Year='{config.FES_YEAR}'"
    count = get_json(q, {"where": where, "returnCountOnly": "true", "f": "json"})["count"]
    if count != config.FES_EXPECTED_ROWS:
        sys.exit(f"  FES {config.FES_YEAR} holds {count:,} rows, not {config.FES_EXPECTED_ROWS:,} - "
                 f"a republished survey? read it first")
    rows, offset = [], 0
    while True:
        page = get_json(q, {"where": where, "outFields": "*", "returnGeometry": "true",
                            "outSR": "4326", "orderByFields": "OBJECTID ASC",
                            "resultOffset": offset, "resultRecordCount": config.FES_PAGE,
                            "f": "json"})
        feats = page.get("features", [])
        if not feats:
            break
        for f in feats:
            a = dict(f["attributes"])
            g = f.get("geometry") or {}
            a["longitude"], a["latitude"] = g.get("x"), g.get("y")
            rows.append(a)
        offset += len(feats)
        print(f"    {offset:>7,} / {count:,}")
        if not page.get("exceededTransferLimit") and offset >= count:
            break
    ids = {r["OBJECTID"] for r in rows}
    if len(rows) != count or len(ids) != count:
        sys.exit(f"  paged {len(rows):,} rows ({len(ids):,} distinct), expected {count:,}")
    config.FES_JSON.write_text(json.dumps(rows), encoding="utf-8")
    print(f"  {'fes_2022':28} {len(rows):,} rows")


def fetch_boundary(force):
    """The City of Sydney (OSM relation 1251066), polygonised from its outer
    ways - Prague's method - and gated on its area."""
    from shapely.geometry import LineString, MultiLineString, mapping
    from shapely.ops import linemerge, polygonize, unary_union
    import geopandas as gpd
    from pipeline import osm

    if config.CITY_BOUNDARY_GEOJSON.exists() and not force:
        print(f"  {'city_boundary':28} cached")
        return
    els, host = osm.fetch(f"[out:json][timeout:180];rel({config.BOUNDARY_OSM_RELATION});out geom;",
                          config.BOUNDARY_OSM_CACHE, force=force)
    lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
             for e in els for m in e.get("members", [])
             if m.get("type") == "way" and m.get("role") == "outer"]
    poly = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
    km2 = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    if not lo <= km2 <= hi:
        sys.exit(f"  City of Sydney polygon is {km2:.1f} km2, outside {lo}-{hi}: a partial answer?")
    config.CITY_BOUNDARY_GEOJSON.write_text(json.dumps(
        {"type": "Feature", "geometry": mapping(poly),
         "properties": {"osm_relation": config.BOUNDARY_OSM_RELATION}}), encoding="utf-8")
    print(f"  {'city_boundary':28} {km2:.1f} km2 (via {host})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    fetch_fes(args.force)
    item = get_json(config.FES_ITEM_URL, {"f": "json"})
    layer = get_json(config.FES_LAYER_URL, {"f": "json"})
    edited = (layer.get("editingInfo") or {}).get("lastEditDate")

    fetch_boundary(args.force)

    from pipeline import osm
    els, host = osm.fetch(config.OSM_ROUTES_QUERY, config.OSM_ROUTES_JSON, force=args.force)
    rels = [e for e in els if e.get("type") == "relation"]
    print(f"  {'osm_rail_routes':28} {len(rels)} route relations (via {host})")
    els, host = osm.fetch(config.OSM_STOPS_QUERY, config.OSM_STOPS_JSON, force=args.force)
    print(f"  {'osm_rail_stops':28} {len(els)} stop nodes (via {host})")

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fes_layer_url": config.FES_LAYER_URL,
            "fes_year": config.FES_YEAR,
            "fes_layer_last_edit": (datetime.fromtimestamp(edited / 1000, timezone.utc).date().isoformat()
                                    if edited else None),
            "fes_licence_info": item.get("licenseInfo"),
            "fes_access_information": item.get("accessInformation")}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"  FES layer last edited {prov['fes_layer_last_edit']}")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
