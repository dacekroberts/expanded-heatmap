"""Download everything Osaka's pipeline reads. NOT a step: drift_check.py never
runs this file, and every step exits naming it when its cache is missing.

    python pipeline/osaka/fetch_sources.py [city|isj|mlit|osm|all] [--force]

  * city  - Osaka City's food-permit list (食品営業許可施設一覧) and its barber,
            beauty and laundry registers, each from the city's own page
            (CC BY 4.0);
  * isj   - MLIT 位置参照情報 for the 24 wards, block (24.0a) and town-chōme
            (19.0b) (PDL 1.0);
  * mlit  - MLIT N02 railways and N03 Osaka-prefecture administrative areas,
            into the country's shared cache data/japan/raw/ (N02 PDL 1.0, N03
            CC BY 4.0);
  * osm   - OpenStreetMap station names in the city's box (ODbL), through
            pipeline/osm.py.

A file already on disk is kept (most were downloaded during screening,
2026-09-24) and recorded, dated by its modification time; --force re-downloads.
Each file is recorded in outputs/osaka/provenance.json (bytes, sha256, when).
"""
import hashlib
import json
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from pipeline import osm  # noqa: E402
from pipeline.countries import japan  # noqa: E402
from pipeline.countries import japan_register  # noqa: E402
from pipeline.osaka import config  # noqa: E402

S = requests.Session()
S.headers["User-Agent"] = osm.OVERPASS_USER_AGENT


def record(key, **fields):
    config.OUTPUTS.mkdir(parents=True, exist_ok=True)
    prov = {}
    if config.PROVENANCE_JSON.exists():
        prov = json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
    prov[key] = fields
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                                      encoding="utf-8")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def get(url, dest, force):
    """Download url to dest unless it is already there. Returns how."""
    if dest.exists() and not force:
        return "kept (on disk from an earlier run or the 2026-09-24 screen)"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(4):
        try:
            with S.get(url, timeout=300, stream=True) as r:
                r.raise_for_status()
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        f.write(chunk)
            break
        except requests.RequestException as e:
            if attempt == 3:
                raise
            print(f"  retry {attempt + 1} after {e}")
            time.sleep(10 * (attempt + 1))
    tmp.replace(dest)
    return "downloaded"


def when(path):
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(timespec="seconds")


def fetch_city(force):
    for key, (name, url, page) in config.SOURCE_FILES.items():
        dest = config.source_csv(key)
        how = get(url, dest, force)
        rows = list(japan_register.city_rows(dest))
        missing = [c for c in config.REQUIRED_COLUMNS[key] if c not in rows[0]]
        if missing:
            sys.exit(f"{dest.name}: header lacks {missing} - not the file the brief read")
        print(f"  {dest.name:22s} {dest.stat().st_size:>10,} bytes {len(rows):>7,} rows  ({how})")
        record(f"city_{key}", file=dest.name, url=url, dataset_page=page,
               bytes=dest.stat().st_size, sha256=sha256(dest), rows=len(rows),
               as_of=config.FOOD_AS_OF if key == "food" else config.REGISTERS_AS_OF,
               retrieved=when(dest), how=how)


def fetch_isj(force):
    for code in japan.CITIES[config.SLUG]["wards"]:
        for kind, template in (("block", japan.ISJ_BLOCK_URL_TEMPLATE), ("chome", japan.ISJ_CHOME_URL_TEMPLATE)):
            url = template.format(code=code)
            dest = config.ISJ_DIR / url.rsplit("/", 1)[-1]
            how = get(url, dest, force)
            if not zipfile.is_zipfile(dest):
                sys.exit(f"{dest.name}: not a zip (an error page?)")
            record(f"isj_{code}_{kind}", file=dest.name, url=url, bytes=dest.stat().st_size,
                   sha256=sha256(dest), retrieved=when(dest), how=how)
        print(f"  ISJ {code}: block + town-chōme")


def fetch_mlit(force):
    pref = japan.CITIES[config.SLUG]["pref"]
    for key, url, dest in (("n02", japan.N02_URL, japan.N02_ZIP),
                           ("n03", japan.N03_URL_TEMPLATE.format(pref=pref),
                            japan.SHARED_RAW / japan.N03_ZIP_TEMPLATE.format(pref=pref))):
        how = get(url, dest, force)
        if not zipfile.is_zipfile(dest):
            sys.exit(f"{dest.name}: not a zip (an error page?)")
        print(f"  {dest.name:28s} {dest.stat().st_size:>12,} bytes  ({how})")
        record(key, file=f"data/japan/raw/{dest.name}", url=url, bytes=dest.stat().st_size,
               sha256=sha256(dest), retrieved=when(dest), how=how)


def fetch_osm(force):
    # Names only: which stations exist is N02's. Two queries, one file each:
    # stations and halts, then tram stops (the Hankai tram's; OSM tags them
    # railway=tram_stop).
    for key, query, path in (("osm_station_names", japan.osm_station_query, config.STATION_OSM_JSON),
                             ("osm_tram_stop_names", japan.osm_tram_stop_query, config.TRAM_OSM_JSON)):
        q = query(config.OSM_BBOX)
        els, host = osm.fetch(q, path, force=force, timeout=180)
        payload = json.loads(path.read_text(encoding="utf-8"))
        with_en = sum(1 for el in els if (el.get("tags") or {}).get("name:en"))
        print(f"  {path.name:26s} {path.stat().st_size:>10,} bytes  {len(els)} objects, {with_en} with name:en  "
              f"via {host}")
        record(key, file=path.name, host=host, query=q, bytes=path.stat().st_size, sha256=sha256(path),
               elements=len(els), osm_base=payload.get("osm3s", {}).get("timestamp_osm_base"),
               retrieved=when(path))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    what = args[0] if args else "all"
    if what not in ("city", "isj", "mlit", "osm", "all"):
        sys.exit(__doc__)
    if what in ("city", "all"):
        fetch_city(force)
    if what in ("isj", "all"):
        fetch_isj(force)
    if what in ("mlit", "all"):
        fetch_mlit(force)
    if what in ("osm", "all"):
        fetch_osm(force)
