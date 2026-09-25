"""Download everything Hong Kong's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/hong_kong/fetch_sources.py

  * FEHD's three licence registers (XML, regenerated daily) - what is licensed;
  * the same registers from the CSDI portal (GeoJSON) - FEHD's point per licence;
  * MTR's station lists - gate 3 only, not published;
  * OpenStreetMap: MTR's and the Light Rail's route relations, and the SAR's boundary.

Each download is recorded in outputs/hong_kong/provenance.json (bytes, sha256,
retrieval time, and the file's own generation date where it carries one).
"""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.hong_kong import config  # noqa: E402
from pipeline.hong_kong.register import read_register  # noqa: E402

S = requests.Session()
S.headers["User-Agent"] = "expanded-heatmap (open-data portfolio map)"


def get(url, **kw):
    for attempt in range(4):
        try:
            r = S.get(url, timeout=300, **kw)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if attempt == 3:
                raise
            print(f"  retry {attempt + 1} after {e}")
            time.sleep(5 * (attempt + 1))


def record(key, **fields):
    """Merge one source's provenance into outputs/hong_kong/provenance.json -
    the page's snapshot line and docs/data_sources.md read it."""
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    prov = {}
    if config.PROVENANCE_JSON.exists():
        prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
    prov[key] = fields
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")


def file_fields(path, url, **extra):
    body = path.read_bytes()
    return {"file": path.name, "url": url, "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "retrieved": datetime.now(timezone.utc).isoformat(timespec="seconds"), **extra}


def csdi_path(name):
    return config.DATA_RAW / f"csdi_{config.CSDI_LAYERS[name][1]}.geojson"


def fetch_registers():
    for name, fname in config.FEHD_FILES.items():
        url = config.FEHD_BASE + fname
        body = get(url).content
        if b"GENERATION_DATE" not in body[:4000] or not body.lstrip().startswith(b"<"):
            sys.exit(f"{fname}: not the self-dated XML register the brief read")
        (config.DATA_RAW / fname).write_bytes(body)
        rows, gen, types, _ = read_register(name)
        print(f"  {fname:28s} {len(body):>11,} bytes  {len(rows):>6,} rows  generated {gen}")
        record(f"fehd_{name}", **file_fields(config.DATA_RAW / fname, url, records=len(rows),
                                             generation_date=gen))

        dataset, layer = config.CSDI_LAYERS[name]
        r = get(config.CSDI_FILE_API, params={"dataset_id": dataset, "format": "geojson",
                                             "layer_name": layer})
        feats = r.json().get("features", [])
        if not feats or config.CSDI_LICENCE_NO not in feats[0].get("properties", {}):
            sys.exit(f"CSDI {layer}: no features, or no {config.CSDI_LICENCE_NO} - not the layer read "
                     f"on 2026-09-24")
        csdi_path(name).write_bytes(r.content)
        updated = max((f["properties"].get("LASTUPDATE") or "") for f in feats)
        print(f"  {csdi_path(name).name:28s} {len(r.content):>11,} bytes  {len(feats):>6,} points  "
              f"latest LASTUPDATE {updated}")
        record(f"csdi_{name}", **file_fields(csdi_path(name), r.url, records=len(feats),
                                             latest_record_update=updated))


def fetch_mtr_lists():
    for path in (config.MTR_STATIONS_CSV, config.MTR_LIGHT_RAIL_CSV):
        url = config.MTR_BASE + path.name
        path.write_bytes(get(url).content)
        print(f"  {path.name:28s} {path.stat().st_size:>11,} bytes")
        record(f"mtr_{path.stem}", **file_fields(path, url, use="gate 3 only - not published"))


def fetch_osm():
    s, w, n, e = config.OSM_BBOX
    rail_q = (f'[out:json][timeout:240];'
              f'relation["type"="route"]["route"~"^(subway|light_rail|train|monorail)$"]'
              f'({s},{w},{n},{e})->.r;.r out geom;node(r.r);out body;')
    overpass(rail_q, config.RAIL_OSM_JSON, "osm_rail")
    bnd_q = (f'[out:json][timeout:240];'
             f'relation["boundary"="administrative"]["ISO3166-1"="{config.BOUNDARY_ISO}"]'
             f'({s},{w},{n},{e});out geom;')
    overpass(bnd_q, config.BOUNDARY_OSM_JSON, "osm_boundary")


def overpass(query, dest, key):
    last = None
    for url in config.OVERPASS_URLS:
        try:
            r = S.post(url, data={"data": query}, timeout=300)
            r.raise_for_status()
            els = r.json().get("elements", [])
        except (requests.RequestException, ValueError) as e:
            last = f"{url}: {e}"
            print(f"  overpass {url} failed: {e}")
            continue
        if not els:
            # An empty result is not an empty city (osm-rail); never cache it.
            last = f"{url}: 0 elements"
            print(f"  overpass {url} returned 0 elements - trying the next host")
            continue
        dest.write_bytes(r.content)
        kinds = {}
        for el in els:
            kinds[el["type"]] = kinds.get(el["type"], 0) + 1
        print(f"  {dest.name:28s} {len(r.content):>11,} bytes  {kinds}  via {url}")
        record(key, **file_fields(dest, url, query=query, elements=kinds,
                                  osm_base=r.json().get("osm3s", {}).get("timestamp_osm_base")))
        return
    sys.exit(f"every Overpass host failed for {dest.name}; last: {last}")


if __name__ == "__main__":
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("registers", "all"):
        fetch_registers()
    if what in ("mtr", "all"):
        fetch_mtr_lists()
    if what in ("osm", "all"):
        fetch_osm()
