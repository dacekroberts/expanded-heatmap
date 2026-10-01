"""Download New Orleans's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/new_orleans/fetch_sources.py [--force]

Three keyless downloads: the City's Active Occupational Licenses (by an
explicit column list - never `ownername` or `businessphone`), the Census
Bureau's TIGER place polygon, and OSM's tram relations. The register is
updated daily, so it is cached and re-taken with --force; its licence is
checked on every run. OSM is always re-fetched (rail is rolling). RTA's GTFS
is not fetched.
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
from pipeline.new_orleans import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
PAGE = 50000
CC0 = "Creative Commons 1.0 Universal (Public Domain Dedication)"


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def register_meta():
    v = requests.get(config.REGISTER_META_URL, headers=HEADERS, timeout=120).json()
    licence = (v.get("license") or {}).get("name")
    if licence != CC0:
        sys.exit(f"  register: the dataset now declares {licence!r}, not CC0 - re-read the "
                 f"licence before using it")
    updated = datetime.fromtimestamp(v["rowsUpdatedAt"], timezone.utc).date().isoformat()
    print(f"  register: CC0, rows updated {updated}")
    return {"name": v.get("name"), "license": licence, "rowsUpdatedAt": v["rowsUpdatedAt"],
            "rows_updated": updated}


def fetch_register(force):
    dest = config.REGISTER_CSV
    if dest.exists() and not force:
        print(f"  register: cached ({dest.stat().st_size:,} bytes)")
        return
    rows, offset = [], 0
    fields = [k for k in config.REGISTER_FIELDS if k != "the_geom"]
    while True:
        r = requests.get(config.REGISTER_URL, headers=HEADERS, timeout=300, params={
            "$select": ",".join(config.REGISTER_FIELDS), "$order": "businesslicensenumber",
            "$limit": PAGE, "$offset": offset})
        r.raise_for_status()
        page = r.json()
        for a in page:
            leaked = [k for k in a if k in config.FORBIDDEN_COLUMNS]
            if leaked:
                sys.exit(f"  register: forbidden columns arrived {leaked} - nothing written")
            g = a.get("the_geom") or {}
            lon, lat = (g.get("coordinates") or ["", ""])[:2]
            row = {k: a.get(k, "") for k in fields}
            row.update(longitude=lon, latitude=lat)
            rows.append(row)
        print(f"    offset {offset:,}: {len(page):,} rows")
        if len(page) < PAGE:
            break
        offset += len(page)
    if len(rows) < 10000:
        sys.exit(f"  register: {len(rows)} rows - a failed fetch, not a negative")
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields + ["longitude", "latitude"])
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
    print("Register (CC0):")
    meta = register_meta()
    fetch_register(args.force)
    print("\nCity boundary (TIGER, public domain):")
    fetch_boundary(args.force)
    print("\nOpenStreetMap (keyless):")
    host = fetch_osm()

    def stamp(p):
        return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")

    prov = {"written_utc": _now(),
            "register": {"url": config.REGISTER_URL, **meta, "fields": config.REGISTER_FIELDS},
            "boundary": {"url": config.CITY_BOUNDARY_URL, "query": config.CITY_BOUNDARY_QUERY},
            "osm_host": host, "osm_bbox": config.RAIL_BBOX,
            "files_utc": {p.name: stamp(p) for p in (
                config.REGISTER_CSV, config.CITY_BOUNDARY_GEOJSON, config.OSM_ROUTES_JSON)}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    main()
