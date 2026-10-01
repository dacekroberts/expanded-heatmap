"""Download Göteborg's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py.

    python pipeline/goteborg/fetch_sources.py

Keyless downloads, each re-taken on every run: the register is refreshed daily
and carries no dates, so the fetch date IS its date (the page says so), and the
tram relations are rolling. Three sources:

  * Göteborgs Stad's `Livsmedelsverksamheter`, the CSV distribution (CC0, the
    licence re-read on the distribution's own metadata node every run). Never
    the rowstore JSON: it drops the rows with a blank `typ`, swaps x and y and
    BOM-mangles `namn` (the brief);
  * OSM's tram relations in the network's box, with their nodes;
  * OSM's kommun boundaries (admin_level 7) around them.

Overpass queries run one at a time.
"""
import csv
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.goteborg import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def register_licence():
    r = requests.get(config.REGISTER_META_URL, headers=HEADERS, timeout=120)
    r.raise_for_status()
    if config.REGISTER_LICENCE_MARK not in r.text:
        sys.exit(f"  register: the distribution's metadata no longer names CC0 "
                 f"({config.REGISTER_META_URL}) - re-read the licence before using it")
    print("  register: CC0 1.0 on the distribution node")
    return "CC0 1.0"


def fetch_register():
    r = requests.get(config.REGISTER_URL, headers=HEADERS, timeout=300)
    r.raise_for_status()
    text = r.content.decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(text), delimiter=";"))
    header, body = rows[0], [x for x in rows[1:] if any(c.strip() for c in x)]
    if tuple(header) != config.REGISTER_COLUMNS:
        sys.exit(f"  register: columns changed upstream: {header} - nothing written")
    if len(body) < config.REGISTER_MIN_ROWS:
        sys.exit(f"  register: {len(body):,} rows - a failed fetch, nothing written")
    config.REGISTER_CSV.write_bytes(r.content)
    print(f"  register: {len(body):,} rows (Last-Modified {r.headers.get('Last-Modified')}) "
          f"-> {config.REGISTER_CSV.name}")
    return {"url": config.REGISTER_URL, "rows": len(body),
            "last_modified": r.headers.get("Last-Modified")}


def fetch_osm():
    s, w, n, e = config.RAIL_BBOX
    rail = ("[out:json][timeout:240];"
            f'relation["type"="route"]["route"="tram"]({s},{w},{n},{e})->.r;'
            ".r out geom;"
            f'(node(r.r);node["railway"="tram_stop"]({s},{w},{n},{e}););out body;')
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON, force=True)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels or any(not r.get("members") for r in rels):
        sys.exit("  rail: no relations, or one without members - a FAILED fetch")
    print(f"  rail: {len(rels)} relations via {host}")
    # Göteborgs Stad by id, and the kommuner in a small box round the lines'
    # southern ends (Mölndal). Every admin_level 7 relation in the network's
    # whole box, out geom, drew 504s from both mirrors twice (2026-09-30): the
    # coastal kommuner are large. A stop in neither polygon stops step 1.
    ks, kw, kn, ke = config.KOMMUNER_BBOX
    kom = ("[out:json][timeout:240];"
           f"(relation({config.GOTEBORG_RELATION});"
           f'relation["boundary"="administrative"]["admin_level"="7"]({ks},{kw},{kn},{ke}););'
           "out geom;")
    els2, host2 = osm.fetch(kom, config.OSM_KOMMUNER_JSON, force=True)
    ids = {x["id"] for x in els2 if x["type"] == "relation"}
    if config.GOTEBORG_RELATION not in ids:
        sys.exit(f"  kommuner: Göteborgs Stad ({config.GOTEBORG_RELATION}) missing - a FAILED fetch")
    print(f"  kommuner: {len(ids)} boundary relations via {host2}")
    return host, host2


def main():
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    print("Göteborgs Stad, Livsmedelsverksamheter:")
    licence = register_licence()
    register = fetch_register()
    print("\nOpenStreetMap (keyless):")
    host, host2 = fetch_osm()

    def stamp(p):
        return datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")

    prov = {"written_utc": _now(),
            "register": {**register, "licence": licence, "metadata": config.REGISTER_META_URL},
            "osm": {"rail_host": host, "kommuner_host": host2, "bbox": config.RAIL_BBOX},
            "files_utc": {p.name: stamp(p) for p in (
                config.REGISTER_CSV, config.OSM_ROUTES_JSON, config.OSM_KOMMUNER_JSON)}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
