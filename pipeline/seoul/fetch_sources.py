"""Download everything Seoul's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/seoul/fetch_sources.py [registers|osm|all] [--copy-from <dir>] [--resume]

  * seventeen citywide permit registers from data.seoul.go.kr (cp949 CSV);
  * OpenStreetMap: the rail route relations around Seoul, and Seoul's boundary.

--copy-from takes register files already downloaded by the same endpoint into
another checkout's data/seoul/raw instead of fetching them again; provenance
says so and dates each by the file's own modification time.

Each file is recorded in outputs/seoul/provenance.json (bytes, sha256, retrieval
time, rows, and the newest 데이터갱신일자 the register carries).
"""
import hashlib
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline.seoul import config  # noqa: E402

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


def check_register(path):
    """The file must be the LOCALDATA register the brief read: a cp949 CSV whose
    header carries the status and the coordinate columns. Returns (rows,
    newest 데이터갱신일자)."""
    with open(path, "rb") as f:
        head = f.read(4000)
    try:
        # The header line only: a fixed-size read can end mid-character.
        text = head.split(b"\n")[0].decode(config.REGISTER_ENCODING, errors="strict")
    except (UnicodeDecodeError, IndexError):
        sys.exit(f"{path.name}: not a cp949 CSV (first bytes {head[:8].hex()})")
    for col in ("영업상태명", "좌표정보(X)", "사업장명", "데이터갱신일자"):
        if col not in text:
            sys.exit(f"{path.name}: header lacks {col} - not the register the brief read")
    # A handful of rows carry a byte cp949 cannot decode (4 of 538,115 in the
    # restaurant file, 2026-09-24: three trade names and one empty-ish field);
    # they are replaced, and step 2 counts them.
    df = pd.read_csv(path, encoding=config.REGISTER_ENCODING, dtype=str,
                     usecols=["데이터갱신일자"], keep_default_na=False,
                     encoding_errors="replace")
    return len(df), max(df["데이터갱신일자"])


def fetch_registers(copy_from=None, resume=False):
    for oa, kind in config.REGISTERS.items():
        dest = config.register_csv(oa)
        src = Path(copy_from) / dest.name if copy_from else None
        if resume and dest.exists():
            got = datetime.fromtimestamp(dest.stat().st_mtime, timezone.utc)
            prior = {}
            if config.PROVENANCE_JSON.exists():
                prior = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8")).get(oa, {})
            how = prior.get("how", "downloaded")
        elif src is not None and src.exists():
            shutil.copy2(src, dest)
            got = datetime.fromtimestamp(src.stat().st_mtime, timezone.utc)
            # No local path: provenance.json is committed to a public repo.
            how = "copied from another checkout's cache (downloaded there by this endpoint)"
        else:
            data = {"srvType": "S", "infId": oa, "serviceKind": "1", "pageNo": "1",
                    "gridTotalCnt": "999999", "ssUserId": "SAMPLE_VIEW",
                    "strWhere": "", "strOrderby": ""}
            for attempt in range(4):
                try:
                    with S.post(config.SHEET_EXPORT_URL, data=data, timeout=900,
                                stream=True) as r:
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
        rows, updated = check_register(dest)
        size = dest.stat().st_size
        print(f"  {dest.name:14s} {kind:14s} {size:>12,} bytes {rows:>8,} rows  "
              f"newest update {updated}  ({how})")
        record(oa, file=dest.name, permit_type=kind, url=config.SHEET_EXPORT_URL,
               method=f"POST infId={oa} srvType=S serviceKind=1 gridTotalCnt=999999 "
                      f"ssUserId=SAMPLE_VIEW", dataset_page=config.DATASET_PAGE.format(oa=oa),
               bytes=size, sha256=sha256(dest), rows=rows, newest_update=updated,
               retrieved=got.isoformat(timespec="seconds"), how=how)


def fetch_osm():
    s, w, n, e = config.OSM_BBOX
    # The metropolitan network's relations (every drawn line, and the undrawn
    # ones whose Seoul stations must be accounted for), plus 우이신설선, whose
    # relations carry no network tag. Intercity (KTX, 코레일) and AREX express
    # are left out of the download: their geometry runs to Busan and Mokpo.
    box = f"({s},{w},{n},{e})"
    rail_q = (f'[out:json][timeout:600];'
              f'(relation["type"="route"]["route"~"^(subway|light_rail|train)$"]'
              f'["network"~"{config.METRO_NETWORK}"]{box};'
              f'relation["type"="route"]["route"="light_rail"]["ref"="W"]{box};)->.r;'
              f'.r out geom;node(r.r);out body;')
    overpass(rail_q, config.RAIL_OSM_JSON, "osm_rail")
    # The station objects themselves: 386 of 1,353 route stop nodes carry no
    # name:en (2026-09-24), and the station node beside them usually does.
    # Used for NAMES only - which stations exist is still route membership.
    st_q = (f'[out:json][timeout:240];'
            f'(node["railway"="station"]{box};way["railway"="station"]{box};);out tags center;')
    overpass(st_q, config.STATION_OSM_JSON, "osm_station_names")
    bnd_q = (f'[out:json][timeout:240];'
             f'relation({config.BOUNDARY_RELATION})["name"="{config.BOUNDARY_NAME}"];out geom;')
    overpass(bnd_q, config.BOUNDARY_OSM_JSON, "osm_boundary")


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
            # An empty result is not an empty city (osm-rail); never cache it.
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
               osm_base=r.json().get("osm3s", {}).get("timestamp_osm_base"),
               retrieved=datetime.now(timezone.utc).isoformat(timespec="seconds"))
        return
    sys.exit(f"every Overpass host failed for {dest.name}; last: {last}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    args = sys.argv[1:]
    copy_from = None
    if "--copy-from" in args:
        i = args.index("--copy-from")
        copy_from = args[i + 1]
        del args[i:i + 2]
    resume = "--resume" in args      # keep register files already in raw/
    args = [a for a in args if a != "--resume"]
    what = args[0] if args else "all"
    if what in ("registers", "all"):
        fetch_registers(copy_from, resume)
    if what in ("osm", "all"):
        fetch_osm()
