"""Download Mendoza's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/mendoza/fetch_sources.py [--force] [--no-osm]

Two keyless sources: the Municipalidad's "Listado Comercios por Actividad
2025" JSON (CC BY 4.0), cached and checked against its sha256 (a step never
fetches), and ONE Overpass query for the Metrotranvia's relations and the
departments it crosses.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.mendoza import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch_register(force):
    dest = config.REGISTER_JSON
    if force or not dest.exists():
        r = requests.get(config.REGISTER_URL, headers=HEADERS, timeout=300)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"  register: {len(r.content):,} bytes -> {dest.name}")
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    if digest != config.REGISTER_SHA256:
        sys.exit(f"  register: sha256 {digest} is not the approved file's "
                 f"{config.REGISTER_SHA256} - the publisher changed it; re-read the brief's "
                 f"counts before using it")
    print(f"  register: {dest.stat().st_size:,} bytes, sha256 matches the approved file")
    return digest


def fetch_osm(force):
    s, w, n, e = config.RAIL_BBOX
    routes = "".join(f'relation["type"="route"]["route"="{m}"]({s},{w},{n},{e});'
                     for m in config.OSM_ROUTES)
    query = ("[out:json][timeout:240];"
             f"({routes})->.r;"
             f'relation["boundary"="administrative"]["admin_level"="5"]({s},{w},{n},{e})->.b;'
             "(.r;.b;);out geom;"
             f'(node(r.r);node["railway"="tram_stop"]({s},{w},{n},{e}););out body;')
    els, host = osm.fetch(query, config.OSM_JSON, force=force)
    rels = [x for x in els if x["type"] == "relation"
            and x.get("tags", {}).get("type") == "route"]
    deps = [x for x in els if x["type"] == "relation"
            and x.get("tags", {}).get("boundary") == "administrative"]
    if not rels or any(not r.get("members") for r in rels):
        sys.exit("  rail: no route relations, or one without members - a FAILED fetch")
    if not deps:
        sys.exit("  no department boundaries came back - a FAILED fetch")
    print(f"  rail: {len(rels)} route relations, {len(deps)} departments via {host}")
    return host


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--no-osm", action="store_true", help="skip the Overpass query")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Register (Municipalidad de la Ciudad de Mendoza, CC BY 4.0):")
    digest = fetch_register(args.force)
    host = None
    if not args.no_osm:
        print("\nOpenStreetMap (keyless):")
        host = fetch_osm(args.force)
    old = (json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
           if config.PROVENANCE_JSON.exists() else {})

    def stamp(p):
        return (datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")
                if p.exists() else None)

    prov = {"written_utc": _now(),
            "register": {"page": config.REGISTER_PAGE, "url": config.REGISTER_URL,
                         "sha256": digest, "data_date": config.REGISTER_DATA_DATE,
                         "license": "CC BY 4.0"},
            "osm_host": host or old.get("osm_host"), "osm_bbox": config.RAIL_BBOX,
            "files_utc": {p.name: stamp(p) for p in (config.REGISTER_JSON, config.OSM_JSON)}}
    config.PROVENANCE_JSON.write_bytes((json.dumps(prov, indent=2) + "\n").encode("utf-8"))
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
