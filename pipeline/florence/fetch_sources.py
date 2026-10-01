"""Download Florence's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/florence/fetch_sources.py

Keyless downloads, each re-taken on every run (the layers are updated daily):
the Comune's four activity layers (CC BY 4.0), OSM's tram relations, and the
comune boundaries around them (OSM, admin_level 8). Overpass queries run one at
a time. GEST's GTFS is not fetched.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.florence import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch_layers():
    out = {}
    for key, name in config.LAYERS.items():
        url = config.LAYER_URL + name
        r = requests.get(url, headers=HEADERS, timeout=300)
        r.raise_for_status()
        feats = r.json().get("features", [])
        if len(feats) < config.LAYER_MIN_ROWS[key]:
            sys.exit(f"  {key}: {len(feats):,} features - a failed fetch, nothing written")
        (config.DATA_RAW / name).write_bytes(r.content)
        out[key] = {"url": url, "features": len(feats),
                    "last_modified": r.headers.get("Last-Modified")}
        print(f"  {key}: {len(feats):,} features (Last-Modified {r.headers.get('Last-Modified')})")
    return out


def fetch_osm():
    s, w, n, e = config.RAIL_BBOX
    rail = ("[out:json][timeout:240];"
            f'relation["type"="route"]["route"="tram"]({s},{w},{n},{e})->.r;'
            ".r out geom;"
            f'(node(r.r);node["railway"="tram_stop"]({s},{w},{n},{e}););out body;')
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels or any(not r.get("members") for r in rels):
        sys.exit("  rail: no relations, or one without members - a FAILED fetch")
    print(f"  rail: {len(rels)} relations via {host}")
    com = ("[out:json][timeout:240];"
           f'relation["boundary"="administrative"]["admin_level"="8"]({s},{w},{n},{e});out geom;')
    els2, host2 = osm.fetch(com, config.OSM_COMUNI_JSON)
    refs = {x.get("tags", {}).get("ref:ISTAT") for x in els2}
    if config.ISTAT_FIRENZE not in refs:
        sys.exit(f"  comuni: Firenze ({config.ISTAT_FIRENZE}) missing")
    print(f"  comuni: {len(els2)} boundary relations via {host2}")
    return host, host2


def main():
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Comune di Firenze (CC BY 4.0):")
    layers = fetch_layers()
    print("\nOpenStreetMap (keyless):")
    host, host2 = fetch_osm()

    def stamp(p):
        return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")

    prov = {"written_utc": _now(), "layers": layers,
            "osm": {"rail_host": host, "comuni_host": host2, "bbox": config.RAIL_BBOX},
            "files_utc": {p.name: stamp(p) for p in (
                [config.DATA_RAW / n for n in config.LAYERS.values()]
                + [config.OSM_ROUTES_JSON, config.OSM_COMUNI_JSON])}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    main()
