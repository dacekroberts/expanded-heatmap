"""Download everything Busan's pipeline reads. NOT a step: drift_check.py
never runs this file, and every step exits naming it when its cache is missing.

    python pipeline/busan/fetch_sources.py [registers|osm|all] [--resume] [--only KEY,KEY]

  * fourteen permit types from the keyless LocalDataService Open API
    (data.busan.go.kr), each pulled IN FULL by its opnSvcId, 1,000 rows a page;
  * OpenStreetMap: Busan's rail route relations, station names and boundary,
    through pipeline/osm.py.

The two API traps (docs/build_briefs/busan.md), enforced here:
  * `state` is NEVER sent - rows permitted after 2025-01-31 carry no status
    code, so a state filter drops all of them;
  * `opnSvcId` is ALWAYS sent - an operation's default answer omits types
    (대규모점포 appears only when asked for by id).
A pull must return exactly totalCount rows, every one of the asked-for type,
or the file is not written.

--resume keeps a register already in raw/ and records it, dated by the file's
own modification time (Staging pulled eleven of them on 2026-09-27 with this
same call).

Each file is recorded in outputs/busan/provenance.json (bytes, sha256, retrieval
time, rows, open rows, and the newest updatedt and lastmodts).
"""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import osm  # noqa: E402
from pipeline.busan import config  # noqa: E402

S = requests.Session()
S.headers["User-Agent"] = osm.OVERPASS_USER_AGENT
BACKOFF = (5, 15, 30, 60, 120, 240)


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


def _find(obj, want):
    """The first value under key `want`, anywhere in a nested answer."""
    if isinstance(obj, dict):
        if want in obj:
            return obj[want]
        for v in obj.values():
            hit = _find(v, want)
            if hit is not None:
                return hit
    elif isinstance(obj, list):
        for v in obj:
            hit = _find(v, want)
            if hit is not None:
                return hit
    return None


def _rows(obj):
    """The page's permit rows: the list of dicts that carry mgtno."""
    if isinstance(obj, list) and obj and isinstance(obj[0], dict) and "mgtno" in obj[0]:
        return obj
    if isinstance(obj, dict):
        if "mgtno" in obj:
            return [obj]          # a one-row page can come back unwrapped
        for v in obj.values():
            hit = _rows(v)
            if hit is not None:
                return hit
    if isinstance(obj, list):
        for v in obj:
            hit = _rows(v)
            if hit is not None:
                return hit
    return None


def get_page(op, svc, page):
    params = {"pageIndex": page, "pageSize": config.PAGE_SIZE, "resultType": "json",
              "opnSvcId": svc}
    assert "state" not in params
    last = None
    for wait in (0, *BACKOFF):
        if wait:
            print(f"    retry in {wait}s after {last}")
            time.sleep(wait)
        try:
            r = S.get(config.API_URL.format(op=op), params=params, timeout=180)
            r.raise_for_status()
            body = r.json()
        except (requests.RequestException, ValueError) as e:
            # The host answers non-JSON (an XML error) under load.
            last = f"{type(e).__name__}: {str(e)[:120]}"
            continue
        total = _find(body, "totalCount")
        rows = _rows(body)
        if total is None:
            last = f"no totalCount in the answer: {str(body)[:160]}"
            continue
        return int(total), rows or []
    sys.exit(f"{op} {svc} page {page}: every retry failed; last: {last}")


def pull(key):
    permit_type, op, svc = config.REGISTERS[key]
    total, rows = get_page(op, svc, 1)
    pages = -(-total // config.PAGE_SIZE)
    print(f"  {key:9s} {op}/{svc} {permit_type}: {total:,} rows, {pages} pages")
    for page in range(2, pages + 1):
        t2, more = get_page(op, svc, page)
        if t2 != total:
            sys.exit(f"{key}: totalCount moved from {total} to {t2} mid-pull")
        rows.extend(more)
        if page % 20 == 0:
            print(f"    page {page}/{pages}: {len(rows):,} rows")
    ids = {r.get("mgtno") for r in rows}
    if len(rows) != total or len(ids) != total:
        sys.exit(f"{key}: {len(rows):,} rows ({len(ids):,} distinct mgtno) against totalCount "
                 f"{total:,} - not written")
    wrong = {r.get("opnsvcid") for r in rows} - {svc}
    if wrong:
        sys.exit(f"{key}: rows of other types {wrong} in a pull by opnSvcId {svc}")
    return rows


def fetch_registers(resume=False, only=None):
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    for k, (permit_type, op, svc) in config.REGISTERS.items():
        if only and k not in only:
            continue
        dest = config.register_json(k)
        if resume and dest.exists():
            got = datetime.fromtimestamp(dest.stat().st_mtime, timezone.utc)
            how = "pulled in full by this call (Staging, 2026-09-27; kept, --resume)"
        else:
            rows = pull(k)
            tmp = dest.with_suffix(".part")
            tmp.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
            tmp.replace(dest)
            got, how = datetime.now(timezone.utc), "pulled in full"
        rows = json.loads(dest.read_text(encoding="utf-8"))
        if {r.get("opnsvcid") for r in rows} != {svc}:
            sys.exit(f"{dest.name}: not a pull of {svc} alone")
        open_rows = sum(r.get("trdstatenm") == config.ACTIVE_STATUS for r in rows)
        upd = max((r.get("updatedt") or "") for r in rows)
        mod = max((r.get("lastmodts") or "") for r in rows)
        size = dest.stat().st_size
        print(f"  {dest.name:38s} {permit_type:14s} {size:>12,} bytes {len(rows):>8,} rows "
              f"{open_rows:>7,} open  newest {upd[:10]} / {mod[:10]}  ({how})")
        record(k, file=dest.name, permit_type=permit_type, operation=op, opnSvcId=svc,
               url=config.API_URL.format(op=op),
               method=f"GET pageSize={config.PAGE_SIZE} resultType=json opnSvcId={svc}, no state",
               bytes=size, sha256=sha256(dest), rows=len(rows), open_rows=open_rows,
               newest_update=upd, newest_lastmodts=mod,
               retrieved=got.isoformat(timespec="seconds"), how=how)


def fetch_osm(force=False):
    s, w, n, e = config.OSM_BBOX
    box = f"({s},{w},{n},{e})"
    # Every urban-rail relation in the box by ROUTE TYPE - never by network -
    # including monorail (Line 4) and tram, plus 동해선 by its ref. Step 1
    # refuses any relation it cannot place.
    rail_q = (f'[out:json][timeout:600];'
              f'(relation["type"="route"]["route"~"^(subway|light_rail|monorail|tram)$"]{box};'
              f'relation["type"="route"]["route"="train"]["ref"="동해"]{box};)->.r;'
              f'.r out geom;node(r.r);out body;')
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
    only = None
    if "--only" in args:
        i = args.index("--only")
        only = set(args[i + 1].split(","))
        del args[i:i + 2]
    resume = "--resume" in args
    force = "--force" in args
    args = [a for a in args if a not in ("--resume", "--force")]
    what = args[0] if args else "all"
    if what in ("osm", "all"):
        fetch_osm(force)
    if what in ("registers", "all"):
        fetch_registers(resume, only)
