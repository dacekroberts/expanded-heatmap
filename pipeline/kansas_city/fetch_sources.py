"""Download Kansas City's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/kansas_city/fetch_sources.py [--force]

Four keyless downloads: KCMO's Business License Holders (by an explicit
column list, every row - step 2 filters), the Census Bureau's 2022 NAICS
titles, the Census Bureau's TIGER place polygon, and OSM's tram relations.
The register is frozen (2026-01-15), so it is cached and re-taken only with
--force; its `rowsUpdatedAt` is checked on every run, and a moved date stops
the script - the page's data-date sentence would then be wrong. OSM is
always re-fetched (the tram-city skill: rail is rolling).

RIDEKC'S GTFS IS NEVER FETCHED (owner, 2026-09-30): ridekc.org's site terms
restrict schedules and require written consent (docs/build_briefs/kansas_city.md).
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
from pipeline.kansas_city import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
PAGE = 50000


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def register_meta():
    v = requests.get(config.REGISTER_META_URL, headers=HEADERS, timeout=120).json()
    licence = (v.get("license") or {}).get("name")
    if licence != "Public Domain":
        sys.exit(f"  register: the dataset now declares {licence!r}, not Public Domain - "
                 f"re-read the licence before using it")
    if v.get("rowsUpdatedAt") != config.REGISTER_ROWS_UPDATED:
        sys.exit(f"  register: rowsUpdatedAt is {v.get('rowsUpdatedAt')}, not "
                 f"{config.REGISTER_ROWS_UPDATED} (2026-01-15) - the data date on the page "
                 f"and the 2025/2026 filter must be re-taken")
    return {"name": v.get("name"), "license": licence, "rowsUpdatedAt": v["rowsUpdatedAt"]}


def fetch_register(force):
    dest = config.REGISTER_CSV
    if dest.exists() and not force:
        print(f"  register: cached ({dest.stat().st_size:,} bytes)")
        return
    rows, offset = [], 0
    while True:
        r = requests.get(config.REGISTER_URL, headers=HEADERS, timeout=300, params={
            "$select": ",".join(config.REGISTER_FIELDS), "$order": "id",
            "$limit": PAGE, "$offset": offset})
        r.raise_for_status()
        page = r.json()
        for a in page:
            loc = a.get("location") or {}
            lon, lat = (loc.get("coordinates") or ["", ""])[:2]
            row = {k: a.get(k, "") for k in config.REGISTER_FIELDS if k != "location"}
            row.update(longitude=lon, latitude=lat)
            rows.append(row)
        print(f"    offset {offset:,}: {len(page):,} rows")
        if len(page) < PAGE:
            break
        offset += len(page)
    if len(rows) < 10000:
        sys.exit(f"  register: {len(rows)} rows - a failed fetch, not a negative")
    fields = [k for k in config.REGISTER_FIELDS if k != "location"] + ["longitude", "latitude"]
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"  register: {len(rows):,} rows -> {dest.name}")


def fetch_file(url, dest, label, force, min_bytes):
    if dest.exists() and not force:
        print(f"  {label}: cached ({dest.stat().st_size:,} bytes)")
        return
    r = requests.get(url, headers=HEADERS, timeout=180)
    r.raise_for_status()
    if len(r.content) < min_bytes:
        sys.exit(f"  {label}: {len(r.content):,} bytes - a failed fetch, nothing written")
    dest.write_bytes(r.content)
    print(f"  {label}: {len(r.content):,} bytes -> {dest.name}")


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
    # `out geom` on the relations (members for step 1, way geometry for the
    # render), then their stop nodes and every tram stop in the box.
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
    print("Register (Public Domain):")
    meta = register_meta()
    fetch_register(args.force)
    print("\nNAICS 2022 titles (Census Bureau, public domain):")
    fetch_file(config.NAICS_TITLES_URL, config.NAICS_TITLES_XLSX, "titles", args.force, 50000)
    print("\nCity boundary (TIGER, public domain):")
    fetch_boundary(args.force)
    # Overpass last: its 504s come in waves, and a re-run skips what is cached.
    print("\nOpenStreetMap (keyless):")
    host = fetch_osm()

    def stamp(p):
        return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")

    prov = {"written_utc": _now(), "register": {"url": config.REGISTER_URL, **meta,
                                                "data_date": config.REGISTER_DATA_DATE,
                                                "fields": config.REGISTER_FIELDS},
            "naics_titles": config.NAICS_TITLES_URL,
            "boundary": {"url": config.CITY_BOUNDARY_URL, "query": config.CITY_BOUNDARY_QUERY},
            "osm_host": host, "osm_bbox": config.RAIL_BBOX,
            "files_utc": {p.name: stamp(p) for p in (
                config.REGISTER_CSV, config.NAICS_TITLES_XLSX, config.CITY_BOUNDARY_GEOJSON,
                config.OSM_ROUTES_JSON)}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    main()
