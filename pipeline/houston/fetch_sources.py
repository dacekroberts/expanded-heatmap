"""Download Houston's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/houston/fetch_sources.py [--force]

Four keyless downloads: the Comptroller's sales-tax permits (Houston outlets
inside city limits, by an explicit column list - never a taxpayer's name,
address or number), the City's Site Addresses file geodatabase (~166 MB),
OSM's light-rail relations, and the Census Bureau's TIGER place polygon. The Census
geocoder is reached by step 3, not here: it is keyed on the join's residue.
METRO's GTFS is not fetched (docs/build_briefs/houston.md).
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
from pipeline.houston import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
PAGE = 50000


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch_register(force):
    dest = config.REGISTER_CSV
    if dest.exists() and not force:
        print(f"  register: cached ({dest.stat().st_size:,} bytes)")
        return
    rows, offset = [], 0
    while True:
        r = requests.get(config.REGISTER_URL, headers=HEADERS, timeout=300, params={
            "$select": ",".join(config.REGISTER_FIELDS), "$where": config.REGISTER_WHERE,
            "$order": ":id", "$limit": PAGE, "$offset": offset})
        r.raise_for_status()
        page = r.json()
        for a in page:
            leaked = [k for k in a if k in config.FORBIDDEN_COLUMNS]
            if leaked:
                sys.exit(f"  register: forbidden columns arrived {leaked} - nothing written")
            rows.append({k: a.get(k, "") for k in config.REGISTER_FIELDS})
        print(f"    offset {offset:,}: {len(page):,} rows")
        if len(page) < PAGE:
            break
        offset += len(page)
    if len(rows) < 50000:
        sys.exit(f"  register: {len(rows)} rows - a failed fetch, not a negative")
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=config.REGISTER_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"  register: {len(rows):,} rows -> {dest.name}")


def fetch_site_addresses(force):
    dest = config.SITE_ADDRESSES_ZIP
    if dest.exists() and not force:
        print(f"  site addresses: cached ({dest.stat().st_size:,} bytes)")
        return
    tmp = dest.with_suffix(".part")
    with requests.get(config.SITE_ADDRESSES_URL, headers=HEADERS, timeout=600, stream=True) as r:
        r.raise_for_status()
        want = int(r.headers.get("Content-Length", 0))
        got = 0
        with open(tmp, "wb") as fh:
            for chunk in r.iter_content(1 << 20):
                fh.write(chunk)
                got += len(chunk)
    if want and got != want:
        sys.exit(f"  site addresses: {got:,} of {want:,} bytes - truncated, nothing kept")
    tmp.replace(dest)
    print(f"  site addresses: {got:,} bytes -> {dest.name} "
          f"(Last-Modified {r.headers.get('Last-Modified')})")


def fetch_osm():
    s, w, n, e = config.RAIL_BBOX
    rail = ("[out:json][timeout:120];"
            f'(relation["type"="route"]["route"~"^(light_rail|tram|subway)$"]({s},{w},{n},{e}););'
            "out geom;node(r);out tags center;")
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON)
    if not [x for x in els if x["type"] == "relation"]:
        sys.exit("  no route relations - a FAILED fetch, not a negative")
    print(f"  rail: {sum(x['type'] == 'relation' for x in els)} relations via {host}")
    return host


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
        sys.exit(f"  boundary: {len(feats)} features for GEOID 4835000 - a failed fetch")
    dest.write_bytes(r.content)
    print(f"  boundary: {len(r.content):,} bytes -> {dest.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Register:")
    fetch_register(args.force)
    print("\nSite Addresses (public domain):")
    fetch_site_addresses(args.force)
    print("\nCity boundary (TIGER, public domain):")
    fetch_boundary(args.force)
    # Overpass last: its 504s come in waves, and a re-run skips what is cached.
    print("\nOpenStreetMap (keyless):")
    host = fetch_osm()

    def stamp(p):
        return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")

    prov = {"written_utc": _now(), "as_of_date": config.AS_OF_DATE,
            "register": {"url": config.REGISTER_URL, "where": config.REGISTER_WHERE,
                         "fields": config.REGISTER_FIELDS},
            "site_addresses": config.SITE_ADDRESSES_URL,
            "boundary": {"url": config.CITY_BOUNDARY_URL, "query": config.CITY_BOUNDARY_QUERY},
            "osm_host": host, "osm_bbox": config.RAIL_BBOX,
            "files_utc": {p.name: stamp(p) for p in (
                config.REGISTER_CSV, config.SITE_ADDRESSES_ZIP, config.CITY_BOUNDARY_GEOJSON,
                config.OSM_ROUTES_JSON)}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    main()
