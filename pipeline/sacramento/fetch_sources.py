"""Download Sacramento's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/sacramento/fetch_sources.py [--force]

Three keyless downloads: the City's Business Operation Tax register (Active
rows, by an explicit column list - never the owner, phone or mailing columns),
OSM's light-rail relations, and OSM's city and county boundaries. The Census
geocoder is reached by step 3, not here: it is keyed on step 2's output.
SacRT's GTFS is not fetched: its host serves an expired certificate.
"""
import argparse
import csv
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.sacramento import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
DATE_FIELDS = ("Business_Start_Date", "Business_Close_Date", "Current_Expire_Date")


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _iso(ms):
    if ms is None:
        return ""
    # From the epoch by arithmetic: Windows' fromtimestamp raises on dates
    # before 1970, and the register holds businesses started decades earlier.
    return (datetime(1970, 1, 1, tzinfo=timezone.utc)
            + timedelta(milliseconds=ms)).strftime("%Y-%m-%d")


def fetch_register(force):
    dest = config.REGISTER_CSV
    if dest.exists() and not force:
        print(f"  register: cached ({dest.stat().st_size:,} bytes)")
        return
    rows, offset = [], 0
    while True:
        r = requests.get(config.REGISTER_URL, headers=HEADERS, timeout=300, params={
            "where": config.REGISTER_WHERE, "outFields": ",".join(config.REGISTER_FIELDS),
            "orderByFields": "OBJECTID", "resultOffset": offset,
            "resultRecordCount": 2000, "f": "json"})
        r.raise_for_status()
        d = r.json()
        if "error" in d:
            sys.exit(f"  register: {d['error']}")
        feats = d.get("features", [])
        for f in feats:
            a = f["attributes"]
            leaked = [k for k in a if k in config.FORBIDDEN_COLUMNS]
            if leaked:
                sys.exit(f"  register: forbidden columns arrived {leaked} - nothing written")
            rows.append({k: (_iso(a.get(k)) if k in DATE_FIELDS else a.get(k))
                         for k in config.REGISTER_FIELDS})
        print(f"    offset {offset:,}: {len(feats):,} rows")
        if not feats or not d.get("exceededTransferLimit") and len(feats) < 2000:
            break
        offset += len(feats)
    if len(rows) < 1000:
        sys.exit(f"  register: {len(rows)} rows - a failed fetch, not a negative")
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=config.REGISTER_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"  register: {len(rows):,} Active rows -> {dest.name}")


def fetch_osm():
    s, w, n, e = config.RAIL_BBOX
    rail = ("[out:json][timeout:120];"
            f'(relation["type"="route"]["route"~"^(light_rail|tram|subway)$"]({s},{w},{n},{e}););'
            "out geom;node(r);out tags center;")
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON)
    if not [x for x in els if x["type"] == "relation"]:
        sys.exit("  no route relations - a FAILED fetch, not a negative")
    print(f"  rail: {sum(x['type'] == 'relation' for x in els)} relations via {host}")
    bnd = ('[out:json][timeout:180];'
           f'relation["boundary"="administrative"]["admin_level"~"^(6|8)$"]({s},{w},{n},{e});'
           "out geom;")
    els2, host2 = osm.fetch(bnd, config.OSM_BOUNDARIES_JSON)
    if not any(x["id"] == config.OSM_CITY_RELATION for x in els2):
        sys.exit(f"  the city's relation {config.OSM_CITY_RELATION} is not in the answer")
    print(f"  boundaries: {len(els2)} relations via {host2}")
    return host, host2


def fetch_added_stations(force):
    """Wikidata's entity JSON for each station config adds by id (CC0)."""
    for name, spec in config.ADDED_STATIONS.items():
        dest = config.DATA_RAW / f"wikidata_{spec['wikidata']}.json"
        if dest.exists() and not force:
            print(f"  {name}: cached {dest.name}")
            continue
        r = requests.get(f"https://www.wikidata.org/wiki/Special:EntityData/{spec['wikidata']}.json",
                         headers=HEADERS, timeout=60)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"  {name}: {len(r.content):,} bytes -> {dest.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Register:")
    fetch_register(args.force)
    print("\nOpenStreetMap (keyless):")
    host, host2 = fetch_osm()
    print("\nWikidata (CC0), stations OSM has not mapped yet:")
    fetch_added_stations(args.force)

    def stamp(p):
        return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")

    prov = {"written_utc": _now(), "as_of_date": config.AS_OF_DATE,
            "register": {"url": config.REGISTER_URL, "where": config.REGISTER_WHERE,
                         "fields": config.REGISTER_FIELDS},
            "osm_hosts": [host, host2], "osm_bbox": config.RAIL_BBOX,
            "files_utc": {p.name: stamp(p) for p in (config.REGISTER_CSV, config.OSM_ROUTES_JSON,
                                                     config.OSM_BOUNDARIES_JSON)}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    main()
