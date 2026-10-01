"""Download Zurich's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/zurich/fetch_sources.py

Keyless downloads, each re-taken on every run (the register is kept current;
OSM is a rolling source): the Stadt Zürich's Gastwirtschaftsbetriebe through
its WFS (CC0) with the dataset's CKAN record for its dates, OSM's tram and
light-rail relations, and the Gemeinde boundaries around them (OSM,
admin_level 8). Overpass queries run one at a time.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.zurich import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch_register():
    r = requests.get(config.WFS_URL, params=config.WFS_PARAMS, headers=HEADERS, timeout=300)
    r.raise_for_status()
    ctype = r.headers.get("Content-Type", "")
    if "json" not in ctype:
        sys.exit(f"  register: Content-Type {ctype!r}, not GeoJSON - the CKAN page's Angular "
                 f"shell, or a WFS error. Nothing written")
    feats = r.json().get("features", [])
    if len(feats) < config.REGISTER_MIN_ROWS:
        sys.exit(f"  register: {len(feats):,} features - a failed fetch, nothing written")
    cols = set(feats[0]["properties"])
    if cols != config.REGISTER_COLUMNS:
        sys.exit(f"  register: columns changed - added {sorted(cols - config.REGISTER_COLUMNS)}, "
                 f"gone {sorted(config.REGISTER_COLUMNS - cols)}. Re-read the layer")
    config.REGISTER_JSON.write_bytes(r.content)
    print(f"  register: {len(feats):,} features ({len(r.content):,} bytes)")

    meta = requests.get(config.CKAN_PACKAGE, headers=HEADERS, timeout=60)
    meta.raise_for_status()
    m = meta.json()["result"]
    if m.get("license_id") != "cc-zero":
        sys.exit(f"  register: CKAN licence is now {m.get('license_id')!r}, not cc-zero - "
                 f"re-read the terms before building")
    print(f"  CKAN: licence {m['license_id']}, dateLastUpdated {m.get('dateLastUpdated')}")
    return {"url": config.WFS_URL, "layer": config.WFS_LAYER, "features": len(feats),
            "licence": m.get("license_id"), "date_last_updated": m.get("dateLastUpdated"),
            "metadata_modified": m.get("metadata_modified")}


def fetch_osm():
    s, w, n, e = config.RAIL_BBOX
    rail = ("[out:json][timeout:240];"
            f'relation["type"="route"]["route"~"^(tram|light_rail)$"]({s},{w},{n},{e})->.r;'
            ".r out geom;"
            f'(node(r.r);node["railway"="tram_stop"]({s},{w},{n},{e}););out body;')
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON, force=True)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels or any(not r.get("members") for r in rels):
        sys.exit("  rail: no relations, or one without members - a FAILED fetch")
    print(f"  rail: {len(rels)} relations via {host}")
    gem = ("[out:json][timeout:240];"
           f'relation["boundary"="administrative"]["admin_level"="8"]({s},{w},{n},{e});out geom;')
    els2, host2 = osm.fetch(gem, config.OSM_GEMEINDEN_JSON, force=True)
    ids = {x["id"] for x in els2}
    if config.ZURICH_RELATION not in ids:
        sys.exit(f"  Gemeinden: the Stadt Zürich (relation {config.ZURICH_RELATION}) missing")
    print(f"  Gemeinden: {len(els2)} boundary relations via {host2}")
    return host, host2


def main():
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Stadt Zürich, Gastwirtschaftsbetriebe (CC0):")
    register = fetch_register()
    print("\nOpenStreetMap (keyless):")
    host, host2 = fetch_osm()

    def stamp(p):
        return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")

    prov = {"written_utc": _now(), "register": register,
            "osm": {"rail_host": host, "gemeinden_host": host2, "bbox": config.RAIL_BBOX},
            "files_utc": {p.name: stamp(p) for p in (
                config.REGISTER_JSON, config.OSM_ROUTES_JSON, config.OSM_GEMEINDEN_JSON)}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
