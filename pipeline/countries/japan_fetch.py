"""Every Japanese city's downloads, shared. NOT a step: a city's
pipeline/<slug>/fetch_sources.py calls main() with its config, and
drift_check.py never runs it.

Kobe's fetch was copied once, for Osaka, with a per-source URL map; Sapporo
would have been the third copy (PLAN, "Japan"), so it lives here. What a city
declares in its config:

  * SOURCE_FILES  {key: (file, URL, dataset page)} - the city's own lists, one
                  entry per register; SOURCES ({key: file}) and source_csv()
                  as japan_step2 reads them; REQUIRED_COLUMNS per key;
  * FOOD_AS_OF    the food list's as-of date, and REGISTERS_AS_OF for the
                  others where the city states one (Kobe's do not); or
                  SOURCE_AS_OF {key: date} where each list has its own;
  * ISJ_DIR, STATION_OSM_JSON, OSM_BBOX, OUTPUTS, PROVENANCE_JSON;
  * TRAM_OSM_JSON only if N02 draws a tram there: OSM tags its stops
    railway=tram_stop, which the station query does not take (Osaka's Hankai
    line; Sapporo's streetcar and Tokyo's Arakawa Line will need it).

A file already on disk is kept and recorded, dated by its modification time;
--force re-downloads. Each file goes into outputs/<slug>/provenance.json
(bytes, sha256, when). A city whose list needs more than a GET (Kyoto's
resource page and session POST) adds its own function and calls the rest.
"""
import hashlib
import json
import sys
import time
import zipfile
from datetime import datetime, timezone

import requests

from pipeline import osm
from pipeline.countries import japan
from pipeline.countries import japan_register

S = requests.Session()
S.headers["User-Agent"] = osm.OVERPASS_USER_AGENT


def record(config, key, **fields):
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


def as_of(config, key):
    """A source's as-of date: config.SOURCE_AS_OF where a city's lists each
    state their own (Fukuoka's four carry three dates), else FOOD_AS_OF for the
    food list and REGISTERS_AS_OF for the rest."""
    per = getattr(config, "SOURCE_AS_OF", {})
    if key in per:
        return per[key]
    return config.FOOD_AS_OF if key == "food" else getattr(config, "REGISTERS_AS_OF", None)


PORTAL_MAGIC = (b"PK\x03\x04", b"\xd0\xcf\x11\xe0")  # XLSX (zip), XLS (OLE2)


def portal_file(portal, dataset, rid, raw_dir, force):
    """One file from a portal with no API (Kyoto's, data.city.kyoto.lg.jp): GET
    the resource page, which sets a session cookie and names the file in a hidden
    `upload_file` field, then POST that form back - the page's own download
    button (the owner approved it as equivalent to a GET). Kept as
    <dataset>_<id>_<upload_file>; a file already on disk under that id is kept.
    The body must be a spreadsheet by its magic bytes: an HTML page is refused."""
    import re
    page = f"{portal}/resource/?id={rid}"
    have = sorted((raw_dir / dataset).glob(f"{dataset}_{rid}_*"))
    if have and not force:
        return have[0], page, "kept (on disk from an earlier run or the 2026-09-24 screen)"
    s = requests.Session()
    s.headers["User-Agent"] = osm.OVERPASS_USER_AGENT
    r = s.get(page, timeout=120)
    r.raise_for_status()
    fields = dict(re.findall(r'<input name="(upload_file|upload_url)" type="hidden" value="([^"]*)"', r.text))
    if not fields.get("upload_file"):
        sys.exit(f"{page}: no download form (the portal changed?)")
    body = s.post(page, data={**fields, "download": "このデータをダウンロード"}, timeout=300).content
    if not body.startswith(PORTAL_MAGIC):
        sys.exit(f"{page}: the download is not a spreadsheet (starts {body[:16]!r}) - refused")
    dest = raw_dir / dataset / f"{dataset}_{rid}_{fields['upload_file']}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(body)
    return dest, page, "downloaded"


def fetch_portal(config, force):
    """Kyoto's: every pinned resource in config.PORTAL_RESOURCES
    ({dataset: (id, ...)}), recorded one by one."""
    n = 0
    for dataset, rids in config.PORTAL_RESOURCES.items():
        for rid in rids:
            dest, page, how = portal_file(config.PORTAL, dataset, rid, config.DATA_RAW, force)
            record(config, f"city_{dataset}_{rid}", file=f"{dataset}/{dest.name}", url=page,
                   dataset_page=f"{config.PORTAL}/dataset/{dataset}/", bytes=dest.stat().st_size,
                   sha256=sha256(dest), retrieved=when(dest), how=how)
            n += 1
    print(f"  {n} portal files recorded ({', '.join(f'{d}: {len(r)}' for d, r in config.PORTAL_RESOURCES.items())})")


def fetch_city(config, force):
    if hasattr(config, "PORTAL_RESOURCES"):
        return fetch_portal(config, force)
    for key, (name, url, page) in config.SOURCE_FILES.items():
        dest = config.source_csv(key)
        how = get(url, dest, force)
        rows = list(japan_register.city_rows(dest))
        missing = [c for c in config.REQUIRED_COLUMNS[key] if c not in rows[0]]
        if missing:
            sys.exit(f"{dest.name}: header lacks {missing} - not the file the brief read")
        print(f"  {dest.name:22s} {dest.stat().st_size:>10,} bytes {len(rows):>7,} rows  ({how})")
        record(config, f"city_{key}", file=dest.name, url=url, dataset_page=page,
               bytes=dest.stat().st_size, sha256=sha256(dest), rows=len(rows),
               as_of=as_of(config, key),
               retrieved=when(dest), how=how)


def fetch_isj(config, force):
    for code in japan.CITIES[config.SLUG]["wards"]:
        for kind, template in (("block", japan.ISJ_BLOCK_URL_TEMPLATE), ("chome", japan.ISJ_CHOME_URL_TEMPLATE)):
            url = template.format(code=code)
            dest = config.ISJ_DIR / url.rsplit("/", 1)[-1]
            how = get(url, dest, force)
            if not zipfile.is_zipfile(dest):
                sys.exit(f"{dest.name}: not a zip (an error page?)")
            record(config, f"isj_{code}_{kind}", file=dest.name, url=url, bytes=dest.stat().st_size,
                   sha256=sha256(dest), retrieved=when(dest), how=how)
        print(f"  ISJ {code}: block + town-chōme")


def fetch_mlit(config, force):
    pref = japan.CITIES[config.SLUG]["pref"]
    for key, url, dest in (("n02", japan.N02_URL, japan.N02_ZIP),
                           ("n03", japan.N03_URL_TEMPLATE.format(pref=pref),
                            japan.SHARED_RAW / japan.N03_ZIP_TEMPLATE.format(pref=pref))):
        how = get(url, dest, force)
        if not zipfile.is_zipfile(dest):
            sys.exit(f"{dest.name}: not a zip (an error page?)")
        print(f"  {dest.name:28s} {dest.stat().st_size:>12,} bytes  ({how})")
        record(config, key, file=f"data/japan/raw/{dest.name}", url=url, bytes=dest.stat().st_size,
               sha256=sha256(dest), retrieved=when(dest), how=how)


def fetch_osm(config, force):
    # Names only: which stations exist is N02's. Stations and halts always;
    # tram stops in their own file where the city declares one.
    queries = [("osm_station_names", japan.osm_station_query, config.STATION_OSM_JSON)]
    if hasattr(config, "TRAM_OSM_JSON"):
        queries.append(("osm_tram_stop_names", japan.osm_tram_stop_query, config.TRAM_OSM_JSON))
    for key, query, path in queries:
        q = query(config.OSM_BBOX)
        els, host = osm.fetch(q, path, force=force, timeout=180)
        payload = json.loads(path.read_text(encoding="utf-8"))
        with_en = sum(1 for el in els if (el.get("tags") or {}).get("name:en"))
        print(f"  {path.name:26s} {path.stat().st_size:>10,} bytes  {len(els)} objects, {with_en} with name:en  "
              f"via {host}")
        record(config, key, file=path.name, host=host, query=q, bytes=path.stat().st_size, sha256=sha256(path),
               elements=len(els), osm_base=payload.get("osm3s", {}).get("timestamp_osm_base"),
               retrieved=when(path))


def fetch_control(config, force):
    """The Economic Census control table (japan.ESTAT_CENSUS_URL), one national
    XLSX into the shared cache; a spreadsheet by its magic bytes or refused."""
    dest = japan.ESTAT_CENSUS_XLSX
    how = get(japan.ESTAT_CENSUS_URL, dest, force)
    if not zipfile.is_zipfile(dest):
        sys.exit(f"{dest.name}: not an XLSX (an error page?)")
    print(f"  {dest.name:28s} {dest.stat().st_size:>12,} bytes  ({how})")
    record(config, "estat_census", file=f"data/japan/raw/{dest.name}", url=japan.ESTAT_CENSUS_URL,
           bytes=dest.stat().st_size, sha256=sha256(dest), retrieved=when(dest), how=how)


PARTS = {"city": fetch_city, "isj": fetch_isj, "mlit": fetch_mlit, "osm": fetch_osm, "control": fetch_control}


def main(config, doc):
    """A city's fetch_sources.py entry point: [city|isj|mlit|osm|all] [--force]."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    what = args[0] if args else "all"
    if what not in (*PARTS, "all"):
        sys.exit(doc)
    for part, fn in PARTS.items():
        if what in (part, "all"):
            fn(config, force)
