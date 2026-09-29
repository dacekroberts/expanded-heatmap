"""Download Stockholm's raw inputs into data/stockholm/raw/ (gitignored).

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/stockholm/fetch_sources.py [--force]

The food inspection register (every row, every field, paged by OBJECTID),
gated on the server's own count and the fields it declares. Then the kommun
boundary and the Tunnelbana from OpenStreetMap.
"""
import argparse
import csv
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.stockholm import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def get_json(url, params=None, timeout=300):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = json.loads(r.read().decode("utf-8"))
    if "error" in body:
        sys.exit(f"  ArcGIS error from {url[:120]}: {body['error']}")
    return body


def fetch_register(force):
    meta = get_json(config.REGISTER_LAYER_URL, {"f": "json"})
    fields = tuple(f["name"] for f in meta["fields"])
    if fields != config.REGISTER_FIELDS:
        sys.exit(f"  the layer's fields changed:\n    now {fields}\n    expected {config.REGISTER_FIELDS}")
    edited = meta.get("editingInfo", {}).get("lastEditDate")
    edited = datetime.fromtimestamp(edited / 1000, timezone.utc).date().isoformat() if edited else ""
    count = get_json(config.REGISTER_LAYER_URL + "/query",
                     {"where": "1=1", "returnCountOnly": "true", "f": "json"})["count"]
    if config.REGISTER_CSV.exists() and not force:
        print(f"  {'register':28} cached ({config.REGISTER_CSV.stat().st_size:,} bytes); "
              f"server holds {count:,} rows, last edited {edited}")
        return count, edited
    rows, offset = [], 0
    while True:
        page = get_json(config.REGISTER_LAYER_URL + "/query", {
            "where": "1=1", "outFields": "*", "orderByFields": "OBJECTID",
            "resultOffset": offset, "resultRecordCount": config.REGISTER_PAGE_SIZE,
            "returnGeometry": "true", "outSR": "4326", "f": "json"})
        feats = page.get("features", [])
        for f in feats:
            a = f["attributes"]
            extra = set(a) - set(config.REGISTER_FIELDS)
            if extra:
                sys.exit(f"  the server returned fields it does not declare: {sorted(extra)}")
            g = f.get("geometry") or {}
            rows.append({**a, "longitude": g.get("x"), "latitude": g.get("y")})
        offset += len(feats)
        if offset % 20000 < config.REGISTER_PAGE_SIZE:
            print(f"    {offset:,} / {count:,}", flush=True)
        if not feats or not page.get("exceededTransferLimit"):
            break
    ids = {r["OBJECTID"] for r in rows}
    if len(rows) != count or len(ids) != count:
        sys.exit(f"  fetched {len(rows):,} rows ({len(ids):,} distinct OBJECTID), server says {count:,}")
    tmp = config.REGISTER_CSV.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(config.REGISTER_FIELDS) + ["longitude", "latitude"])
        w.writeheader()
        w.writerows(rows)
    tmp.replace(config.REGISTER_CSV)
    print(f"  {'register':28} {len(rows):,} rows, {config.REGISTER_CSV.stat().st_size:,} bytes; "
          f"last edited {edited}")
    return count, edited


def fetch_boundary(force):
    """Stockholms kommun (OSM relation 398021), polygonised from its outer
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
    rel = [e for e in els if e.get("type") == "relation"]
    if len(rel) != 1 or rel[0]["tags"].get("name") != "Stockholms kommun":
        sys.exit(f"  relation {config.BOUNDARY_OSM_RELATION} is not Stockholms kommun: "
                 f"{[r['tags'].get('name') for r in rel]}")
    lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
             for e in rel for m in e.get("members", [])
             if m.get("type") == "way" and m.get("role") == "outer"]
    poly = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
    km2 = gpd.GeoSeries([poly], crs=config.CRS_GEOGRAPHIC).to_crs(config.CRS_PROJECTED).area.iloc[0] / 1e6
    lo, hi = config.BOUNDARY_AREA_KM2
    if not lo <= km2 <= hi:
        sys.exit(f"  Stockholms kommun polygon is {km2:.1f} km2, outside {lo}-{hi}: a partial answer?")
    config.CITY_BOUNDARY_GEOJSON.write_text(json.dumps(
        {"type": "Feature", "geometry": mapping(poly),
         "properties": {"osm_relation": config.BOUNDARY_OSM_RELATION}}), encoding="utf-8")
    print(f"  {'city_boundary':28} {km2:.1f} km2 (via {host})")


def fetch_kommuner(force):
    """The naming layer: every kommun touching the rail bbox, one polygon each."""
    from shapely.geometry import LineString, MultiLineString, mapping
    from shapely.ops import linemerge, polygonize, unary_union
    from pipeline import osm

    if config.KOMMUNER_GEOJSON.exists() and not force:
        print(f"  {'kommuner':28} cached")
        return
    els, host = osm.fetch(config.KOMMUNER_QUERY, config.KOMMUNER_OSM_CACHE, force=force)
    feats = []
    for e in (e for e in els if e.get("type") == "relation"):
        lines = [LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
                 for m in e.get("members", [])
                 if m.get("type") == "way" and m.get("role") == "outer" and len(m.get("geometry") or []) >= 2]
        poly = unary_union(list(polygonize(linemerge(MultiLineString(lines)))))
        if poly.is_empty:
            sys.exit(f"  kommun {e['tags'].get('name')} ({e['id']}) did not polygonise")
        feats.append({"type": "Feature", "geometry": mapping(poly),
                      "properties": {"name": e["tags"].get("name"), "osm_relation": e["id"]}})
    config.KOMMUNER_GEOJSON.write_text(json.dumps({"type": "FeatureCollection", "features": feats},
                                                  ensure_ascii=False), encoding="utf-8")
    print(f"  {'kommuner':28} {len(feats)}: {sorted(f['properties']['name'] for f in feats)} (via {host})")


def fetch_additions(force):
    from pipeline import osm
    els, host = osm.fetch(config.OSM_ADDITIONS_QUERY, config.OSM_ADDITIONS_JSON, force=force)
    print(f"  {'osm_station_additions':28} {len(els)} station node(s) (via {host})")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    count, edited = fetch_register(args.force)
    fetch_boundary(args.force)

    from pipeline import osm
    els, host = osm.fetch(config.OSM_ROUTES_QUERY, config.OSM_ROUTES_JSON, force=args.force)
    rels = [e for e in els if e.get("type") == "relation"]
    print(f"  {'osm_rail_routes':28} {len(rels)} route relations (via {host})")
    els, host = osm.fetch(config.OSM_STOPS_QUERY, config.OSM_STOPS_JSON, force=args.force)
    print(f"  {'osm_rail_stops':28} {len(els)} stop and platform members (via {host})")
    fetch_additions(args.force)
    fetch_kommuner(args.force)

    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "register_layer_url": config.REGISTER_LAYER_URL,
            "register_rows": count,
            "register_last_edited": edited}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"provenance -> {config.PROVENANCE_JSON.relative_to(config.ROOT)}")
