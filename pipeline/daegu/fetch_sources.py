"""Download everything Daegu's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/daegu/fetch_sources.py [registers|osm|all] [--resume]

  * eleven permit registers from D-데이터허브 (data.daegu.go.kr), the pinned
    monthly edition, XLSX, by file id through the page's own download button;
  * OpenStreetMap: Daegu's rail route relations, station names and boundary,
    through pipeline/osm.py.

--resume keeps a register already in raw/ and records it, dated by the file's
own modification time (the 2026-09-27 files were downloaded by this endpoint
during screening).

Each file is recorded in outputs/daegu/provenance.json (bytes, sha256, retrieval
time, rows, and the newest 데이터갱신일자 the register carries).
"""
import hashlib
import json
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import osm  # noqa: E402
from pipeline.daegu import config  # noqa: E402

S = requests.Session()
S.headers["User-Agent"] = osm.OVERPASS_USER_AGENT
warnings.filterwarnings("ignore", message="Workbook contains no default style")


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


def check_register(path, permit_type):
    """The file must be the LOCALDATA register the brief read: an XLSX (a zip)
    whose header carries the status and coordinate columns, of the right permit
    type. Returns (rows, newest 데이터갱신일자)."""
    with open(path, "rb") as f:
        if f.read(2) != b"PK":
            sys.exit(f"{path.name}: not an XLSX (a portal error page?)")
    header = pd.read_excel(path, nrows=0).columns
    for col in ("영업상태명", "좌표정보X(EPSG5174)", "사업장명", "데이터갱신일자", "개방서비스명"):
        if col not in header:
            sys.exit(f"{path.name}: header lacks {col} - not the register the brief read")
    df = pd.read_excel(path, dtype=str, usecols=["개방서비스명", "데이터갱신일자"])
    services = set(df["개방서비스명"].dropna())
    if services != {permit_type}:
        sys.exit(f"{path.name}: 개방서비스명 is {services}, expected {permit_type}")
    return len(df), max(df["데이터갱신일자"].dropna())


def fetch_registers(resume=False):
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    for k, (permit_type, dataset, file_id) in config.REGISTERS.items():
        dest = config.register_xlsx(k)
        url = config.FILE_DOWN_URL.format(file_id=file_id)
        if resume and dest.exists():
            got = datetime.fromtimestamp(dest.stat().st_mtime, timezone.utc)
            how = "downloaded by this endpoint during screening (kept, --resume)"
        else:
            for attempt in range(4):
                try:
                    with S.get(url, timeout=600, stream=True) as r:
                        r.raise_for_status()
                        with open(dest, "wb") as f:
                            for chunk in r.iter_content(1 << 20):
                                f.write(chunk)
                    break
                except requests.RequestException as e:
                    if attempt == 3:
                        raise
                    print(f"  retry {attempt + 1} after {e}")
                    time.sleep(10 * (attempt + 1))
            got = datetime.now(timezone.utc)
            how = "downloaded"
        rows, updated = check_register(dest, permit_type)
        size = dest.stat().st_size
        print(f"  {dest.name:26s} {permit_type:14s} {size:>12,} bytes {rows:>8,} rows  "
              f"newest update {updated}  ({how})")
        record(k, file=dest.name, permit_type=permit_type, edition=config.EDITION, url=url,
               dataset_page=config.DATASET_PAGE.format(dataset=dataset), bytes=size,
               sha256=sha256(dest), rows=rows, newest_update=updated,
               retrieved=got.isoformat(timespec="seconds"), how=how)


def fetch_osm(force=False):
    s, w, n, e = config.OSM_BBOX
    box = f"({s},{w},{n},{e})"
    # Every urban-rail relation in the box by ROUTE TYPE - never by network,
    # whose labels disagree here - including monorail (Line 3) and tram, plus
    # 대경선 by its ref. Step 1 refuses any relation it cannot place, so a line
    # this query brings in is either drawn or named as not drawn.
    rail_q = (f'[out:json][timeout:600];'
              f'(relation["type"="route"]["route"~"^(subway|light_rail|monorail|tram)$"]{box};'
              f'relation["type"="route"]["route"="train"]["ref"="대경"]{box};)->.r;'
              f'.r out geom;node(r.r);out body;')
    # The station objects: names only. Which stations exist is route membership.
    st_q = (f'[out:json][timeout:240];'
            f'(node["railway"="station"]{box};way["railway"="station"]{box};);out tags center;')
    bnd_q = (f'[out:json][timeout:240];'
             f'relation({config.BOUNDARY_RELATION})["name"="{config.BOUNDARY_NAME}"];out geom;')
    for key, q, dest in (("osm_rail", rail_q, config.RAIL_OSM_JSON),
                         ("osm_station_names", st_q, config.STATION_OSM_JSON),
                         ("osm_boundary", bnd_q, config.BOUNDARY_OSM_JSON)):
        els, host = osm.fetch(q, dest, force=force, timeout=300)
        kinds = {}
        for el in els:
            kinds[el["type"]] = kinds.get(el["type"], 0) + 1
        payload = json.loads(dest.read_text(encoding="utf-8"))
        print(f"  {dest.name:24s} {dest.stat().st_size:>11,} bytes  {kinds}  via {host}")
        record(key, file=dest.name, host=host, query=q, bytes=dest.stat().st_size,
               sha256=sha256(dest), elements=kinds,
               osm_base=payload.get("osm3s", {}).get("timestamp_osm_base"),
               retrieved=datetime.fromtimestamp(dest.stat().st_mtime, timezone.utc)
               .isoformat(timespec="seconds"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    resume = "--resume" in args
    force = "--force" in args
    args = [a for a in args if a not in ("--resume", "--force")]
    what = args[0] if args else "all"
    if what in ("registers", "all"):
        fetch_registers(resume)
    if what in ("osm", "all"):
        fetch_osm(force)
