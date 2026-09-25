"""Download everything Taipei (Regional)'s pipeline reads. NOT a step:
drift_check.py never runs this file, and every step exits naming it when its
cache is missing.

    python pipeline/taipei/fetch_sources.py [register|doorplates|metro|osm|all] [--refetch]

  * the national business tax register - the SHARED cache (fetched only with
    --refetch or when missing);
  * Taipei's and New Taipei's door-plate files;
  * Taipei Metro's station list (gate 3);
  * OpenStreetMap: the metro and light-rail route relations across the two
    cities, and their stop nodes. The national 捷運車站 layer is the shared
    cache in data/taiwan/raw/ (fetched by Taoyuan).

Certificates come from the OS store (truststore). Each file is recorded in
outputs/taipei/provenance.json.
"""
import hashlib
import json
import sys
from pathlib import Path

import requests
import truststore

truststore.inject_into_ssl()
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import taiwan  # noqa: E402
from pipeline.taipei import config  # noqa: E402
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


def fetch(key, url, dest, check=None):
    dest.parent.mkdir(parents=True, exist_ok=True)
    shared.stream(url, dest)
    size = dest.stat().st_size
    head = dest.read_bytes()[:4000].decode("utf-8", errors="replace")
    if check and check not in head:
        sys.exit(f"{dest.name}: {check!r} not in its first bytes - not the file the brief read")
    print(f"  {dest.name}  {size:,} bytes")
    record(key, file=dest.name, url=url, bytes=size, sha256=shared.sha256(dest),
           retrieved=shared.now())


def register():
    if "--refetch" in sys.argv or not taiwan.REGISTER_ZIP.exists():
        shared.stream(taiwan.REGISTER_URL, taiwan.REGISTER_ZIP)
    size = taiwan.REGISTER_ZIP.stat().st_size
    record("fia_register", file=taiwan.REGISTER_ZIP.name, url=taiwan.REGISTER_URL, bytes=size,
           data_date=taiwan.register_date(), sha256=shared.sha256(taiwan.REGISTER_ZIP),
           retrieved=shared.now())
    print(f"  {taiwan.REGISTER_ZIP.name}  {size:,} bytes  data date {taiwan.register_date()}")


def osm():
    s, w, n, e = config.OSM_BBOX
    q = (f'[out:json][timeout:600];'
         f'relation["type"="route"]["route"~"^(subway|light_rail|monorail)$"]({s},{w},{n},{e})->.r;'
         f'.r out geom;node(r.r);out body;')
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
    if what in ("metro", "all"):
        fetch("metro_list", config.METRO_LIST_URL, config.METRO_LIST_CSV)
    if what in ("osm", "all"):
        osm()
    if what in ("doorplates", "all"):
        fetch("taipei_doorplates", config.TAIPEI_DOORPLATE_URL, config.TAIPEI_DOORPLATE_CSV, "號")
        fetch("new_taipei_doorplates", config.NEW_TAIPEI_DOORPLATE_URL,
              config.NEW_TAIPEI_DOORPLATE_CSV, "number")
        # The editions the page's caption names; update them with each refresh.
        prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
        prov["taipei_doorplates"]["edition"] = config.TAIPEI_DOORPLATE_EDITION
        prov["new_taipei_doorplates"]["edition"] = config.NEW_TAIPEI_DOORPLATE_EDITION
        config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8")
