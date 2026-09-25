"""Download everything Taichung's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/taichung/fetch_sources.py [register|doorplates|stations|osm|all]

  * the national business tax register (FIA, daily) into the SHARED cache
    data/taiwan/raw/ - every Taiwanese city reads the same file;
  * Taichung's door-plate file, the NEWEST month its portal index lists (a
    Google Drive link; Drive answers a large file with its standard
    "can't scan for viruses" confirmation form, which is submitted as a
    browser would - it is not a CAPTCHA);
  * Taichung Metro's Green Line station table;
  * OpenStreetMap: the city's rail route relations (no boundary: see config).

Certificates come from the OS store (truststore): Python's bundle lacks
Taiwan's government root. Verification is never switched off.

Each file is recorded in outputs/taichung/provenance.json.
"""
import csv
import hashlib
import html
import io
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import truststore

truststore.inject_into_ssl()
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.countries import taiwan  # noqa: E402
from pipeline.taichung import config  # noqa: E402

S = requests.Session()
S.headers["User-Agent"] = "expanded-heatmap (open-data portfolio map)"


def record(key, **fields):
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    prov = {}
    if config.PROVENANCE_JSON.exists():
        prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
    prov[key] = fields
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stream(url, dest, **kw):
    for attempt in range(4):
        try:
            with S.get(url, timeout=900, stream=True, **kw) as r:
                r.raise_for_status()
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        f.write(chunk)
                return r
        except requests.RequestException as e:
            if attempt == 3:
                raise
            print(f"  retry {attempt + 1} after {e}")
            time.sleep(10 * (attempt + 1))


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fetch_register():
    taiwan.SHARED_RAW.mkdir(parents=True, exist_ok=True)
    stream(taiwan.REGISTER_URL, taiwan.REGISTER_ZIP)
    head = taiwan.REGISTER_ZIP.read_bytes()[:4]
    if head[:2] != b"PK":
        sys.exit(f"{taiwan.REGISTER_ZIP.name}: not a zip (first bytes {head.hex()})")
    first = next(taiwan.register_rows(("",)))
    size = taiwan.REGISTER_ZIP.stat().st_size
    date = taiwan.register_date()
    print(f"  {taiwan.REGISTER_ZIP.name}  {size:,} bytes  data date {date}  columns {list(first)[:6]}...")
    record("fia_register", file=taiwan.REGISTER_ZIP.name, url=taiwan.REGISTER_URL, bytes=size,
           data_date=date, sha256=sha256(taiwan.REGISTER_ZIP), retrieved=now())


def drive_download(file_id, dest):
    """Google Drive: the uc endpoint, then - for a large file - the confirmation
    form's own action and hidden fields, exactly as a browser submits them."""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    r = stream(url, dest)
    with open(dest, "rb") as f:
        head = f.read(2048)
    if b"<html" not in head.lower() and b"<!doctype" not in head.lower():
        return url
    page = dest.read_text(encoding="utf-8", errors="replace")
    form = re.search(r'<form[^>]+id="download-form"[^>]+action="([^"]+)"', page)
    if not form:
        sys.exit(f"Drive returned a page with no download form for {file_id} - read it; "
                 f"do not work around it")
    fields = dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', page))
    action = html.unescape(form.group(1))
    r = stream(action, dest, params=fields)
    return r.url


def fetch_doorplates():
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    stream(config.PORTAL + config.DOORPLATE_INDEX_RID, config.DOORPLATE_INDEX_CSV)
    rows = list(csv.DictReader(io.StringIO(
        config.DOORPLATE_INDEX_CSV.read_bytes().decode("utf-8-sig").lstrip("﻿"))))
    files = []
    for r in rows:
        name = r.get("檔案名稱", "")
        m = re.search(r"(\d+)年(\d+)月", name)
        fid = re.search(r"/d/([^/]+)/", r.get("地圖網址", ""))
        if m and fid:
            files.append(((int(m.group(1)), int(m.group(2))), name, fid.group(1)))
    if not files:
        sys.exit("the door-plate index lists no monthly file - read it")
    (roc_year, month), name, fid = max(files)
    url = drive_download(fid, config.DOORPLATE_CSV)
    with open(config.DOORPLATE_CSV, encoding="utf-8-sig", errors="replace") as f:
        header = f.readline()
    for col in config.PLATE_COLS.values():
        if col not in header:
            sys.exit(f"{config.DOORPLATE_CSV.name}: header lacks {col} - not the file the brief read")
    size = config.DOORPLATE_CSV.stat().st_size
    print(f"  {name}  {size:,} bytes  (ROC {roc_year}-{month:02d}, Drive id {fid})")
    record("doorplates", file=config.DOORPLATE_CSV.name, edition=name, drive_id=fid,
           index=config.PORTAL + config.DOORPLATE_INDEX_RID, url=url.split("&confirm")[0],
           bytes=size, sha256=sha256(config.DOORPLATE_CSV), retrieved=now())


def fetch_stations():
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    url = config.PORTAL + config.STATIONS_RID
    stream(url, config.STATIONS_RAW_CSV)
    text = config.STATIONS_RAW_CSV.read_bytes().decode("utf-8-sig")
    if "車站英文" not in text or "北屯總站" not in text:
        sys.exit("the station table is not the one the brief read")
    n = len(text.strip().splitlines()) - 1
    print(f"  {config.STATIONS_RAW_CSV.name}  {n} stations")
    record("stations", file=config.STATIONS_RAW_CSV.name, url=url, rows=n,
           sha256=sha256(config.STATIONS_RAW_CSV), retrieved=now())


def fetch_osm():
    s, w, n, e = config.OSM_BBOX
    box = f"({s},{w},{n},{e})"
    rail_q = (f'[out:json][timeout:300];'
              f'relation["type"="route"]["route"~"^(subway|light_rail|train|monorail)$"]{box}->.r;'
              f'.r out geom;node(r.r);out body;')
    overpass(rail_q, config.RAIL_OSM_JSON, "osm_rail")


def overpass(query, dest, key):
    last = None
    for url in config.OVERPASS_URLS:
        try:
            r = S.post(url, data={"data": query}, timeout=900)
            r.raise_for_status()
            els = r.json().get("elements", [])
        except (requests.RequestException, ValueError) as e:
            last = f"{url}: {e}"
            print(f"  overpass {url} failed: {e}")
            continue
        if not els:
            last = f"{url}: 0 elements"
            print(f"  overpass {url} returned 0 elements - trying the next host")
            continue
        dest.write_bytes(r.content)
        kinds = {}
        for el in els:
            kinds[el["type"]] = kinds.get(el["type"], 0) + 1
        print(f"  {dest.name:24s} {len(r.content):>11,} bytes  {kinds}  via {url}")
        record(key, file=dest.name, url=url, query=query, bytes=len(r.content),
               sha256=hashlib.sha256(r.content).hexdigest(), elements=kinds,
               osm_base=r.json().get("osm3s", {}).get("timestamp_osm_base"), retrieved=now())
        return
    sys.exit(f"every Overpass host failed for {dest.name}; last: {last}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("register", "all"):
        fetch_register()
    if what in ("doorplates", "all"):
        fetch_doorplates()
    if what in ("stations", "all"):
        fetch_stations()
    if what in ("osm", "all"):
        fetch_osm()
