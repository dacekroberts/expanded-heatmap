"""Download everything Taoyuan's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/taoyuan/fetch_sources.py [register|doorplates|metro|osm|all]

  * the national business tax register - the SHARED cache, fetched by the
    first Taiwanese city (Taichung's fetch script; `register` here re-fetches);
  * Taoyuan's door-plate file (the TGOS edition in config);
  * Taoyuan Metro's network and route-station XMLs, and the national 捷運車站
    layer;
  * OpenStreetMap: the Airport MRT's route relations and their stop nodes.

Certificates come from the OS store (truststore). Verification is never
switched off. Each file is recorded in outputs/taoyuan/provenance.json.
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import requests
import truststore

truststore.inject_into_ssl()
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import taiwan  # noqa: E402
from pipeline.taoyuan import config  # noqa: E402
from pipeline.taichung import fetch_sources as shared  # noqa: E402  (stream, sha256, now)

S = shared.S


def record(key, **fields):
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    prov = {}
    if config.PROVENANCE_JSON.exists():
        prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
    prov[key] = fields
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")


def register():
    if "--refetch" in sys.argv or not taiwan.REGISTER_ZIP.exists():
        shared.stream(taiwan.REGISTER_URL, taiwan.REGISTER_ZIP)
    size = taiwan.REGISTER_ZIP.stat().st_size
    date = taiwan.register_date()
    print(f"  {taiwan.REGISTER_ZIP.name}  {size:,} bytes  data date {date}")
    record("fia_register", file=taiwan.REGISTER_ZIP.name, url=taiwan.REGISTER_URL, bytes=size,
           data_date=date, sha256=shared.sha256(taiwan.REGISTER_ZIP), retrieved=shared.now())


def doorplates():
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    shared.stream(config.DOORPLATE_URL, config.DOORPLATE_CSV)
    head = config.DOORPLATE_CSV.read_bytes()[:3000].decode("utf-8", errors="replace")
    if "號" not in head:
        sys.exit(f"{config.DOORPLATE_CSV.name}: no 號 column in the header - not the file the brief read")
    size = config.DOORPLATE_CSV.stat().st_size
    print(f"  {config.DOORPLATE_EDITION}  {size:,} bytes")
    record("doorplates", file=config.DOORPLATE_CSV.name, edition=config.DOORPLATE_EDITION,
           url=config.DOORPLATE_URL, bytes=size, sha256=shared.sha256(config.DOORPLATE_CSV),
           retrieved=shared.now())


def metro():
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    for key, url, dest in (("metro_network", config.NETWORK_XML_URL, config.NETWORK_XML),
                           ("metro_route_stations", config.ROUTE_XML_URL, config.ROUTE_XML),
                           ("national_stations", config.NATIONAL_STATIONS_URL,
                            config.NATIONAL_STATIONS_ZIP)):
        shared.stream(url, dest)
        size = dest.stat().st_size
        if dest.suffix == ".zip" and not zipfile.is_zipfile(dest):
            sys.exit(f"{dest.name}: not a zip")
        print(f"  {dest.name}  {size:,} bytes")
        record(key, file=dest.name, url=url, bytes=size, sha256=shared.sha256(dest),
               retrieved=shared.now())


def osm():
    s, w, n, e = config.OSM_BBOX
    box = f"({s},{w},{n},{e})"
    # Only the metro modes, and the line by name within the box (taiwan-city:
    # do not pull route=train's intercity geometry).
    q = (f'[out:json][timeout:300];'
         f'relation["type"="route"]["route"~"^(subway|light_rail|train)$"]'
         f'["name"~"{config.LINE_NAME_MATCH}"]{box}->.r;.r out geom;node(r.r);out body;')
    last = None
    for url in config.OVERPASS_URLS:
        try:
            r = S.post(url, data={"data": q}, timeout=900)
            r.raise_for_status()
            els = r.json().get("elements", [])
        except (requests.RequestException, ValueError) as ex:
            last = f"{url}: {ex}"
            print(f"  overpass {url} failed: {ex}")
            continue
        if not els:
            last = f"{url}: 0 elements"
            print(f"  overpass {url} returned 0 elements - trying the next host")
            continue
        config.RAIL_OSM_JSON.write_bytes(r.content)
        kinds = {}
        for el in els:
            kinds[el["type"]] = kinds.get(el["type"], 0) + 1
        print(f"  {config.RAIL_OSM_JSON.name}  {len(r.content):,} bytes  {kinds}  via {url}")
        record("osm_rail", file=config.RAIL_OSM_JSON.name, url=url, query=q, bytes=len(r.content),
               sha256=hashlib.sha256(r.content).hexdigest(), elements=kinds,
               osm_base=r.json().get("osm3s", {}).get("timestamp_osm_base"),
               retrieved=shared.now())
        return
    sys.exit(f"every Overpass host failed; last: {last}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    what = [a for a in sys.argv[1:] if not a.startswith("--")]
    what = what[0] if what else "all"
    if what in ("register", "all"):
        register()
    if what in ("doorplates", "all"):
        doorplates()
    if what in ("metro", "all"):
        metro()
    if what in ("osm", "all"):
        osm()
