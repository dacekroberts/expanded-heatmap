"""Download Seattle (Regional)'s raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/seattle/fetch_sources.py [--force] [--only NAME ...]

Keyless downloads: two boundary layers, two address-point layers, four
business sources (config.SOURCES) and OSM's rail relations (one Overpass
query, last). The Liquor Board's off-premise list is fetched by
`pipeline/seattle/lcb_offpremise.py`'s own `fetch()`, called here.
Sound Transit's GTFS is NOT fetched - see config.

ArcGIS layers are paged by objectid with only the requested fields; a field
the server returns that was not requested stops the run, so a contact or
mailing column can never reach the disk by a schema change.
"""
import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.seattle import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get(url, dest, force, label, params=None):
    if dest.exists() and not force:
        print(f"  {label}: cached {dest.name} ({dest.stat().st_size:,} bytes)")
        return
    r = requests.get(url, params=params, timeout=600, headers=HEADERS)
    r.raise_for_status()
    if len(r.content) < 100:
        sys.exit(f"  {label}: a {len(r.content)}-byte answer - a failed fetch, not a negative")
    dest.write_bytes(r.content)
    print(f"  {label}: {len(r.content):,} bytes -> {dest.name}")


def arcgis_csv(url, fields, dest, force, label, where="1=1", bbox=None):
    """Page an ArcGIS layer into a CSV of the requested fields plus the point
    as latitude/longitude (outSR 4326). `bbox` (s, w, n, e) bounds it."""
    if dest.exists() and not force:
        print(f"  {label}: cached {dest.name} ({dest.stat().st_size:,} bytes)")
        return
    wanted = fields.split(",")
    oid = wanted[0]
    params = {"where": where, "outFields": fields, "outSR": "4326", "f": "json",
              "returnGeometry": "true", "orderByFields": oid,
              "resultRecordCount": str(config.ARCGIS_PAGE)}
    if bbox:
        s, w, n, e = bbox
        params |= {"geometry": f"{w},{s},{e},{n}", "geometryType": "esriGeometryEnvelope",
                   "inSR": "4326", "spatialRel": "esriSpatialRelIntersects"}
    count = requests.get(url + "/query", params={**params, "returnCountOnly": "true"},
                         headers=HEADERS, timeout=120).json()["count"]
    rows, offset = [], 0
    while offset < count:
        for attempt in range(3):
            try:
                j = requests.get(url + "/query", params={**params, "resultOffset": str(offset)},
                                 headers=HEADERS, timeout=180).json()
                if "error" in j:
                    raise RuntimeError(j["error"])
                break
            except Exception as exc:  # noqa: BLE001 - a page is retried, then the run stops
                if attempt == 2:
                    sys.exit(f"  {label}: page at {offset} failed: {exc}")
        feats = j.get("features", [])
        if not feats:
            sys.exit(f"  {label}: an empty page at {offset} of {count} - a failed fetch")
        for f in feats:
            a = f["attributes"]
            extra = set(a) - set(wanted)
            if extra:
                sys.exit(f"  {label}: the server returned unrequested fields {sorted(extra)}")
            g = f.get("geometry") or {}
            a["latitude"], a["longitude"] = g.get("y"), g.get("x")
            rows.append(a)
        offset += len(feats)
        if offset % 50000 < len(feats):
            print(f"    {label}: {offset:,} of {count:,}")
    if len(rows) != count:
        sys.exit(f"  {label}: {len(rows):,} rows against a count of {count:,}")
    with dest.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=wanted + ["latitude", "longitude"])
        w.writeheader()
        w.writerows(rows)
    print(f"  {label}: {len(rows):,} rows -> {dest.name}")


def fetch_rail():
    s, w, n, e = config.RAIL_BBOX
    modes = "|".join(config.ROUTE_TYPES)
    q = ("[out:json][timeout:120];"
         f'(relation["type"="route"]["route"~"^({modes})$"]({s},{w},{n},{e}););'
         "out geom;node(r);out tags center;")
    els, host = osm.fetch(q, config.OSM_ROUTES_JSON)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels:
        sys.exit("  no route relations came back - a FAILED fetch, not a negative")
    print(f"  rail: {len(rels)} relations via {host}")
    return host


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download cached files")
    ap.add_argument("--only", nargs="*", help="boundaries, addresses, business, lcb, rail")
    args = ap.parse_args()
    only = set(args.only or ["boundaries", "addresses", "business", "lcb", "rail"])
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    if "boundaries" in only:
        print("Boundaries:")
        get(config.KC_CITIES_URL, config.KC_CITIES_GEOJSON, args.force, "King County cities",
            params=config.KC_CITIES_QUERY)
        get(config.SNO_CITIES_URL, config.SNO_CITIES_GEOJSON, args.force,
            "Lynnwood and Mountlake Terrace", params=config.SNO_CITIES_QUERY)
    if "addresses" in only:
        print("\nAddress points:")
        arcgis_csv(config.KC_ADDRESS_URL, config.KC_ADDRESS_FIELDS, config.KC_ADDRESS_CSV,
                   args.force, "King County address points")
        arcgis_csv(config.SNO_ADDRESS_URL, config.SNO_ADDRESS_FIELDS, config.SNO_ADDRESS_CSV,
                   args.force, "Snohomish address points", bbox=config.SNO_ADDRESS_BBOX)
    if "business" in only:
        print("\nBusiness sources:")
        for source, spec in config.SOURCES.items():
            if "query" in spec:
                get(spec["endpoint"], spec["file"], args.force, source, params=spec["query"])
            else:
                arcgis_csv(spec["endpoint"], spec["fields"], spec["file"], args.force, source,
                           where=spec.get("where", "1=1"))
    if "lcb" in only:
        print("\nLiquor Board off-premise list:")
        from pipeline.seattle import lcb_offpremise
        lcb_offpremise.fetch(args.force)
    host = None
    if "rail" in only:
        # Overpass last: its 504s come in waves, and a re-run skips what is cached.
        print("\nOpenStreetMap (keyless):")
        host = fetch_rail()

    def stamp(path):
        return (datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(
            timespec="seconds") if path.exists() else None)

    paths = [config.OSM_ROUTES_JSON, config.KC_CITIES_GEOJSON, config.SNO_CITIES_GEOJSON,
             config.KC_ADDRESS_CSV, config.SNO_ADDRESS_CSV]
    paths += [spec["file"] for spec in config.SOURCES.values()]
    prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8")) \
        if config.PROVENANCE_JSON.exists() else {}
    prov |= {"written_utc": _now(), "osm_bbox": config.RAIL_BBOX,
             "as_of_date": config.AS_OF_DATE,
             "files_utc": {p.name: stamp(p) for p in paths if p.exists()},
             "sources": {k: {"endpoint": v["endpoint"],
                             "query": v.get("query") or {"where": v.get("where", "1=1"),
                                                         "outFields": v["fields"]}}
                         for k, v in config.SOURCES.items()}}
    if host:
        prov["osm_host"] = host
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these "
          f"files and never fetch.")


if __name__ == "__main__":
    main()
