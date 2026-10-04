"""Download Tacoma's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/tacoma/fetch_sources.py [--force] [--no-osm]

Three keyless downloads: the City's business-license point layer (by an
explicit column list that leaves every mailing field out, every row - step 2
filters), the Census Bureau's TIGER place polygon, and OSM's T Line relations.
The register is refreshed daily, so it is cached and re-taken only with
--force, and the layer's own last-edit date is recorded as the data date.

SOUND TRANSIT'S GTFS IS NEVER FETCHED (owner, 2026-10-02, for Seattle: its
Transit Data Terms; docs/build_briefs/tacoma.md).
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
from pipeline.tacoma import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def register_meta():
    """The layer's geometry type, row count and last edit (its data date)."""
    lyr = requests.get(config.REGISTER_URL, params={"f": "json"}, headers=HEADERS,
                       timeout=120).json()
    if lyr.get("geometryType") != "esriGeometryPoint":
        sys.exit(f"  register: the layer is {lyr.get('geometryType')!r}, not points - "
                 f"the table item is not the source")
    names = {f["name"] for f in lyr.get("fields", [])}
    missing = sorted(set(config.REGISTER_FIELDS) - names)
    if missing:
        sys.exit(f"  register: fields renamed or gone: {missing}")
    edited = (lyr.get("editingInfo") or {}).get("dataLastEditDate")
    when = (datetime.fromtimestamp(edited / 1000, timezone.utc).date().isoformat()
            if edited else None)
    return {"name": lyr.get("name"), "max_record_count": lyr.get("maxRecordCount"),
            "data_last_edit": when}


def fetch_register(force, page_size):
    dest = config.REGISTER_CSV
    if dest.exists() and not force:
        print(f"  register: cached ({dest.stat().st_size:,} bytes)")
        return
    n = requests.get(config.REGISTER_URL + "/query", headers=HEADERS, timeout=120,
                     params={"where": "1=1", "returnCountOnly": "true", "f": "json"}).json()["count"]
    rows, offset = [], 0
    while offset < n:
        r = requests.get(config.REGISTER_URL + "/query", headers=HEADERS, timeout=300, params={
            "where": "1=1", "outFields": ",".join(config.REGISTER_FIELDS),
            "orderByFields": "objectid", "resultOffset": offset,
            "resultRecordCount": page_size, "outSR": "4326", "f": "json"})
        r.raise_for_status()
        feats = r.json().get("features", [])
        if not feats:
            sys.exit(f"  register: an empty page at offset {offset:,} of {n:,} - a failed fetch")
        for f in feats:
            row = {k: f["attributes"].get(k) for k in config.REGISTER_FIELDS}
            g = f.get("geometry") or {}
            row.update(longitude=g.get("x"), latitude=g.get("y"))
            rows.append(row)
        offset += len(feats)
    if len(rows) != n:
        sys.exit(f"  register: {len(rows):,} rows read, the layer counts {n:,}")
    fields = list(config.REGISTER_FIELDS) + ["longitude", "latitude"]
    with open(dest, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
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


def fetch_osm(force):
    s, w, n, e = config.RAIL_BBOX
    routes = "".join(f'relation["type"="route"]["route"="{m}"]({s},{w},{n},{e});'
                     for m in config.ROUTES)
    # `out geom` on the relations (members for step 1, way geometry for the
    # render), then their stop nodes and every tram stop in the box.
    rail = ("[out:json][timeout:240];"
            f"({routes})->.r;"
            ".r out geom;"
            f'(node(r.r);node["railway"="tram_stop"]({s},{w},{n},{e}););out body;')
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON, force=force)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels:
        sys.exit("  no tram or light-rail relations came back - a FAILED fetch, not a negative")
    if any(not r.get("members") for r in rels):
        sys.exit("  a route relation came back without members - `out geom` is required")
    print(f"  rail: {len(rels)} relations via {host}")
    return host


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-osm", action="store_true", help="skip the Overpass query")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Register (City of Tacoma, Tax & License; data.tacoma.gov):")
    meta = register_meta()
    print(f"  layer {meta['name']!r}, last edited {meta['data_last_edit']}")
    fetch_register(args.force, min(meta.get("max_record_count") or 1000, 2000))
    print("\nCity boundary (TIGER, public domain):")
    fetch_boundary(args.force)
    # Overpass last: its 504s come in waves, and a re-run skips what is cached.
    host = None
    if not args.no_osm:
        print("\nOpenStreetMap (keyless):")
        host = fetch_osm(args.force)

    old = (json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
           if config.PROVENANCE_JSON.exists() else {})

    def stamp(p):
        return (datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")
                if p.exists() else None)

    # The register's metadata is the download's: kept from the last fetch
    # unless the register was fetched again.
    reg_meta = old.get("register")
    if args.force or not reg_meta:
        reg_meta = {"url": config.REGISTER_URL, "item": config.REGISTER_ITEM,
                    "fields": list(config.REGISTER_FIELDS), **meta}
    prov = {"written_utc": _now(), "register": reg_meta,
            "boundary": {"url": config.CITY_BOUNDARY_URL, "query": config.CITY_BOUNDARY_QUERY},
            "osm_host": host or old.get("osm_host"), "osm_bbox": config.RAIL_BBOX,
            "files_utc": {p.name: stamp(p) for p in (
                config.REGISTER_CSV, config.CITY_BOUNDARY_GEOJSON, config.OSM_ROUTES_JSON)}}
    config.PROVENANCE_JSON.write_bytes((json.dumps(prov, indent=2) + "\n").encode("utf-8"))
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
