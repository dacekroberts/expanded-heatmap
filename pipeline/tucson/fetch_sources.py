"""Download Tucson's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/tucson/fetch_sources.py [--force]

Three keyless downloads: the City's BUSLIC layer (active licences that are not
home occupations, by an explicit field list, paged at the layer's 2,000), the
Census Bureau's TIGER place polygon, and OSM's tram relations. BUSLIC is
rebuilt daily, so it is cached and re-taken with --force; OSM is always
re-fetched (the tram-city skill: rail is rolling).
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
from pipeline.tucson import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
PAGE = 2000


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch_register(force):
    dest = config.REGISTER_CSV
    if dest.exists() and not force:
        print(f"  register: cached ({dest.stat().st_size:,} bytes)")
        return
    url = config.REGISTER_LAYER + "/query"
    want = requests.get(url, headers=HEADERS, timeout=120, params={
        "where": config.REGISTER_WHERE, "returnCountOnly": "true", "f": "json"}).json()["count"]
    rows, offset = [], 0
    while True:
        r = requests.get(url, headers=HEADERS, timeout=300, params={
            "where": config.REGISTER_WHERE, "outFields": ",".join(config.REGISTER_FIELDS),
            "orderByFields": "OBJECTID", "resultOffset": offset, "resultRecordCount": PAGE,
            "outSR": "4326", "f": "json"})
        r.raise_for_status()
        page = r.json()
        if "error" in page:
            sys.exit(f"  register: {page['error']}")
        for f in page.get("features", []):
            row = {k: f["attributes"].get(k) for k in config.REGISTER_FIELDS}
            g = f.get("geometry") or {}
            row.update(longitude=g.get("x", ""), latitude=g.get("y", ""))
            rows.append(row)
        print(f"    offset {offset:,}: {len(page.get('features', [])):,} rows")
        if not page.get("exceededTransferLimit") and len(page.get("features", [])) < PAGE:
            break
        offset += PAGE
    if len(rows) != want:
        sys.exit(f"  register: {len(rows):,} rows of {want:,} counted - a failed fetch, "
                 f"nothing written")
    fields = list(config.REGISTER_FIELDS) + ["longitude", "latitude"]
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"  register: {len(rows):,} rows -> {dest.name}")


def fetch_boundary(force):
    dest = config.CITY_BOUNDARY_GEOJSON
    if dest.exists() and not force:
        print(f"  boundary: cached ({dest.stat().st_size:,} bytes)")
        return
    r = requests.get(config.CITY_BOUNDARY_URL, params=config.CITY_BOUNDARY_QUERY,
                     headers=HEADERS, timeout=180)
    r.raise_for_status()
    feats = r.json().get("features", [])
    if len(feats) != 1:
        sys.exit(f"  boundary: {len(feats)} features for GEOID {config.CITY_GEOID} - a failed fetch")
    dest.write_bytes(r.content)
    print(f"  boundary: {len(r.content):,} bytes -> {dest.name}")


def fetch_osm():
    s, w, n, e = config.RAIL_BBOX
    rail = ("[out:json][timeout:240];"
            f'relation["type"="route"]["route"="tram"]({s},{w},{n},{e})->.r;'
            ".r out geom;"
            f'(node(r.r);node["railway"="tram_stop"]({s},{w},{n},{e}););out body;')
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels:
        sys.exit("  no tram relations came back - a FAILED fetch, not a negative")
    if any(not r.get("members") for r in rels):
        sys.exit("  a route relation came back without members - `out geom` is required")
    print(f"  rail: {len(rels)} relations via {host}")
    return host


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Register (City of Tucson, BUSLIC):")
    fetch_register(args.force)
    print("\nCity boundary (TIGER, public domain):")
    fetch_boundary(args.force)
    print("\nOpenStreetMap (keyless):")
    host = fetch_osm()

    def stamp(p):
        return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")

    prov = {"written_utc": _now(),
            "register": {"layer": config.REGISTER_LAYER, "where": config.REGISTER_WHERE,
                         "fields": config.REGISTER_FIELDS},
            "boundary": {"url": config.CITY_BOUNDARY_URL, "query": config.CITY_BOUNDARY_QUERY},
            "osm_host": host, "osm_bbox": config.RAIL_BBOX,
            "files_utc": {p.name: stamp(p) for p in (
                config.REGISTER_CSV, config.CITY_BOUNDARY_GEOJSON, config.OSM_ROUTES_JSON)}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    main()
