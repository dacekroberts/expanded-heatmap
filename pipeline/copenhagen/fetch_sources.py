"""Download Copenhagen's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    $env:DATAFORDELER_API_KEY = "..."        (PowerShell; bash: export ...)
    python pipeline/copenhagen/fetch_sources.py [--yes] [--refresh-cvr]

    python pipeline/copenhagen/fetch_sources.py --seed-cvr <dir>

THREE THINGS HERE ARE UNLIKE EVERY OTHER CITY.

**Datafordeler needs a key, and the key travels in the URL.** It is the
owner's, read from the environment, and nothing here prints a URL, a request
or an exception that could carry it; an error body is scrubbed before it is
shown. The OSM half is keyless and runs without it.

**The downloads are listed, sized and CONFIRMED before any is taken.** CVR's
entities are national files of hundreds of megabytes each, so the script asks
Datafordeler what it has (GetAvailableFileDownloads), prints each file's name,
generation and size, and waits for a yes - `--yes` skips the question.

**CVR must be ONE generation.** Datafordeler builds a new generation every
week and keeps each for seven days, and the join runs across six entity files;
two generations would silently lose every unit created or closed in between.
So a set that would mix generations is refused, and `--refresh-cvr`
re-downloads all six together. `--seed-cvr` registers CVR files that were
downloaded earlier (their generation is read from Datafordeler's own file
name) instead of fetching them again.
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.copenhagen import config  # noqa: E402
from pipeline.countries import denmark as DK  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
# Datafordeler's own file names: CVR_V2_Adressering_TotalDownload_csv_Current_505
FILENAME_RE = re.compile(
    r"^(?P<register>[A-Z]+)_V(?P<version>\d+)_(?P<entity>[A-Za-z]+)_TotalDownload_"
    r"(?P<fmt>csv)_(?P<type>Current)_(?P<gen>\d+)", re.IGNORECASE)


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _scrub(text, key):
    text = str(text)
    return text.replace(key, "<key>") if key else text


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest():
    if DK.MANIFEST_JSON.exists():
        return json.loads(DK.MANIFEST_JSON.read_text(encoding="utf-8"))
    return {"files": {}}


def save_manifest(man):
    DK.MANIFEST_JSON.write_text(json.dumps(man, ensure_ascii=False, indent=2),
                                encoding="utf-8")


def target(register, entity, kommune=None):
    if register == DK.CVR_REGISTER:
        return DK.CVR_DIR / f"{entity}.csv"
    return DK.DAR_DIR / f"{entity}_{kommune}.csv"


def rel(path):
    return path.relative_to(DK.SHARED_RAW).as_posix()


# --- Seeding: CVR files already downloaded -----------------------------------

def seed_cvr(src_dir, man):
    """Copy Datafordeler-named CVR CSVs into the country cache, recording the
    generation their own file name carries. The originals are only read."""
    DK.CVR_DIR.mkdir(parents=True, exist_ok=True)
    found = 0
    for src in sorted(Path(src_dir).glob("CVR_V*_*_TotalDownload_csv_Current_*.csv")):
        m = FILENAME_RE.match(src.name)
        if not m or m["entity"] not in DK.CVR_ENTITIES:
            continue
        dest = target(DK.CVR_REGISTER, m["entity"])
        if dest.exists():
            print(f"  {m['entity']:18s} already cached - not overwritten")
        else:
            print(f"  {m['entity']:18s} copying {src.stat().st_size:,} bytes ...", flush=True)
            shutil.copyfile(src, dest)
        man["files"][rel(dest)] = {
            "register": DK.CVR_REGISTER, "entity": m["entity"], "kommune": None,
            "filename": src.name, "version": int(m["version"]),
            "generation": int(m["gen"]), "generation_time": None,
            "zip_md5": None, "csv_bytes": dest.stat().st_size,
            "csv_sha256": _sha256(dest), "fetched_utc": _now(),
            "source": "seeded from an earlier Datafordeler download"}
        found += 1
    if not found:
        sys.exit(f"--seed-cvr: no Datafordeler-named CVR CSVs in {src_dir}")
    save_manifest(man)
    print(f"  seeded {found} file(s); manifest -> {DK.MANIFEST_JSON}")


# --- Datafordeler -----------------------------------------------------------

def _entries(payload):
    """GetAvailableFileDownloads returns a list, or an object holding one."""
    if isinstance(payload, list):
        rows = payload
    else:
        rows = next((v for v in payload.values() if isinstance(v, list)), [])
    return [{k.lower(): v for k, v in r.items()} for r in rows if isinstance(r, dict)]


def list_files(register, entity, key):
    rows, page = [], 1
    while page <= 30:
        try:
            r = requests.get(DK.LIST_URL, timeout=120, headers=HEADERS, params={
                "Register": register, "Entity": entity, "PageNumber": page,
                "apiKey": key})
        except requests.RequestException as exc:
            sys.exit(f"  listing {register}/{entity}: {_scrub(type(exc).__name__, key)}")
        if r.status_code == 401:
            sys.exit(f"  listing {register}/{entity}: HTTP 401. A key younger than "
                     f"about 15 minutes 401s exactly like a wrong one (DAF-AUTH-0005) - "
                     f"wait and retry the SAME key rather than making a new one.")
        # PAGING ENDS WITH AN ERROR, NOT AN EMPTY PAGE. Measured 2026-09-24:
        # the page after the last answers HTTP 400, "'pageNumber' is greater
        # than the total amount of pages." On page 1 it means nothing is
        # listed at all, which `pick` then reports.
        if r.status_code == 400 and "greater than the total amount of pages" in r.text:
            break
        if r.status_code != 200:
            sys.exit(f"  listing {register}/{entity}: HTTP {r.status_code}: "
                     f"{_scrub(r.text[:300], key)}")
        got = _entries(r.json())
        if not got:
            break
        rows += got
        page += 1
    return rows


def pick(rows, entity, kommune):
    def is_mine(e):
        muni = str(e.get("municipalitycode") or "").strip()
        muni_ok = (muni in ("", "0", "0000", "None") if kommune is None
                   else muni.zfill(4) == kommune)
        fmt = {str(e.get("containedfileformat") or "").lower(),
               str(e.get("outputfileformat") or "").lower()}
        return (str(e.get("entityname") or "").lower() == entity.lower()
                and "total" in str(e.get("typeofdownload") or "").lower()
                and str(e.get("typeofdata") or "").lower() == "current"
                and "csv" in fmt and muni_ok)
    mine = [e for e in rows if is_mine(e)]
    if not mine:
        combos = sorted({(str(e.get("entityname")), str(e.get("typeofdownload")),
                          str(e.get("typeofdata")), str(e.get("containedfileformat")),
                          str(e.get("municipalitycode"))) for e in rows})
        print(f"  no current CSV total download for {entity} kommune={kommune}. "
              f"What the listing holds ({len(rows)} rows):")
        for c in combos[:40]:
            print(f"    {c}")
        return None
    return max(mine, key=lambda e: (int(e.get("version") or 0),
                                    int(e.get("generationnumber") or 0)))


def download(entry, dest, key):
    fn = entry["filename"]
    tmp = dest.with_suffix(".zip.part")
    try:
        with requests.get(DK.GET_URL, timeout=3600, stream=True, headers=HEADERS,
                          params={"Filename": fn, "apiKey": key}) as r:
            if r.status_code != 200:
                sys.exit(f"  {fn}: HTTP {r.status_code}: {_scrub(r.text[:300], key)}")
            md5 = hashlib.md5()
            done = 0
            with open(tmp, "wb") as fh:
                for chunk in r.iter_content(1 << 22):
                    fh.write(chunk)
                    md5.update(chunk)
                    done += len(chunk)
    except requests.RequestException as exc:
        sys.exit(f"  {fn}: download failed ({_scrub(type(exc).__name__, key)})")
    if tmp.read_bytes()[:4] != b"PK\x03\x04":
        tmp.unlink()
        sys.exit(f"  {fn}: not a zip - not the file asked for")
    want = str(entry.get("md5hash") or "").lower()
    if want and want != md5.hexdigest():
        tmp.unlink()
        sys.exit(f"  {fn}: MD5 {md5.hexdigest()} does not match the listing's {want}")
    with zipfile.ZipFile(tmp) as z:
        csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if len(csvs) != 1:
            sys.exit(f"  {fn}: expected one CSV inside, found {csvs}")
        with z.open(csvs[0]) as src, open(dest, "wb") as out:
            shutil.copyfileobj(src, out, 1 << 22)
    tmp.unlink()
    print(f"  {fn:62s} {done:13,} bytes zipped -> {dest.name}")
    return md5.hexdigest()


def fetch_datafordeler(man, key, assume_yes, refresh_cvr):
    wanted = [(DK.CVR_REGISTER, e, None) for e in DK.CVR_ENTITIES]
    wanted += [(DK.DAR_REGISTER, e, k) for e in DK.DAR_ENTITIES for k in config.DAR_KOMMUNER]
    plan, listings = [], {}
    for register, entity, kommune in wanted:
        dest = target(register, entity, kommune)
        cached = dest.exists() and rel(dest) in man["files"]
        if cached and not (refresh_cvr and register == DK.CVR_REGISTER):
            continue
        if (register, entity) not in listings:
            listings[(register, entity)] = list_files(register, entity, key)
        entry = pick(listings[(register, entity)], entity, kommune)
        if entry is None:
            sys.exit(f"  cannot plan {register}/{entity}; see the listing above")
        plan.append((register, entity, kommune, dest, entry))

    # ONE CVR GENERATION: what is cached and what would be fetched must agree.
    gens = {v["generation"] for p, v in man["files"].items()
            if v["register"] == DK.CVR_REGISTER
            and not refresh_cvr}
    gens |= {int(e["generationnumber"]) for r_, *_ , e in plan if r_ == DK.CVR_REGISTER}
    if len(gens) > 1:
        sys.exit(f"  CVR would mix generations {sorted(gens)}: the cached files are "
                 f"one week's and Datafordeler now serves another. Re-run with "
                 f"--refresh-cvr to download all {len(DK.CVR_ENTITIES)} together.")

    if not plan:
        print("  everything cached")
        return
    total = sum(int(e.get("filesizeinbytes") or 0) for *_, e in plan)
    print(f"\n  {'file':62s} {'generated':20s} {'size':>13s}")
    for *_, e in plan:
        print(f"  {e['filename']:62s} {str(e.get('generationtime'))[:19]:20s} "
              f"{int(e.get('filesizeinbytes') or 0):13,}")
    print(f"  {len(plan)} file(s), {total:,} bytes zipped, from api.datafordeler.dk")
    if not assume_yes:
        if not sys.stdin.isatty():
            sys.exit("  not a terminal - re-run with --yes to download")
        if input("  Download these? [y/N] ").strip().lower() != "y":
            sys.exit("  nothing downloaded")
    for register, entity, kommune, dest, e in plan:
        dest.parent.mkdir(parents=True, exist_ok=True)
        md5 = download(e, dest, key)
        man["files"][rel(dest)] = {
            "register": register, "entity": entity, "kommune": kommune,
            "filename": e["filename"], "version": int(e.get("version") or 0),
            "generation": int(e["generationnumber"]),
            "generation_time": e.get("generationtime"),
            "expiration": e.get("expirationdate"), "zip_md5": md5,
            "csv_bytes": dest.stat().st_size, "csv_sha256": _sha256(dest),
            "fetched_utc": _now(), "source": "api.datafordeler.dk GetFile"}
        save_manifest(man)


# --- OpenStreetMap (keyless) -------------------------------------------------

def fetch_osm():
    s, w, n, e = config.RAIL_BBOX
    # `out geom` on the relations: step 1 needs the member lists (station
    # membership) and map_common.load_osm_line_shapes the way geometry.
    # route=train is left out AT QUERY TIME - regional and InterCity trains
    # are out of scope and their national-length geometry is the costliest
    # part of any such query.
    rail = ("[out:json][timeout:240];"
            '(relation["type"="route"]["route"~"^(subway|light_rail)$"]'
            f"({s},{w},{n},{e}););"
            "out geom;node(r);out tags center;")
    els, host = osm.fetch(rail, config.OSM_ROUTES_JSON)
    rels = [x for x in els if x["type"] == "relation"]
    if any(not r.get("members") for r in rels):
        sys.exit("  a route relation came back without members - `out geom` is required")
    print(f"  rail: {len(rels)} relations via {host}")
    kom = ('[out:json][timeout:240];'
           f'relation["boundary"="administrative"]["admin_level"="{DK.OSM_KOMMUNE_LEVEL}"]'
           f"({s},{w},{n},{e});out geom;")
    els, host = osm.fetch(kom, config.OSM_KOMMUNER_JSON)
    refs = {x.get("tags", {}).get("ref") for x in els}
    missing = set(config.KOMMUNER) - refs
    if missing:
        sys.exit(f"  kommune boundaries missing refs {sorted(missing)}")
    print(f"  kommuner: {len(els)} boundary relations via {host}")
    return host


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--yes", action="store_true", help="download without asking")
    ap.add_argument("--refresh-cvr", action="store_true",
                    help="re-download all six CVR entities as one generation")
    ap.add_argument("--seed-cvr", metavar="DIR",
                    help="register Datafordeler-named CVR CSVs already on disk, then stop")
    ap.add_argument("--osm-only", action="store_true", help="the keyless OSM half only")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS, DK.CVR_DIR, DK.DAR_DIR):
        d.mkdir(parents=True, exist_ok=True)
    man = load_manifest()

    if args.seed_cvr:
        print("Seeding CVR:")
        seed_cvr(args.seed_cvr, man)
        sys.exit(0)

    print("OpenStreetMap (keyless):")
    osm_host = fetch_osm()

    if not args.osm_only:
        import os
        key = os.environ.get(DK.API_KEY_ENV, "").strip()
        if not key:
            sys.exit(f"\n{DK.API_KEY_ENV} is not set. Datafordeler needs the owner's "
                     f"API key for CVR and DAR (both free data, neither access-"
                     f"restricted). The key is never written anywhere by this script.")
        print("\nDatafordeler (CVR, DAR):")
        fetch_datafordeler(man, key, args.yes, args.refresh_cvr)

    prov = {"written_utc": _now(), "osm_bbox": config.RAIL_BBOX, "osm_host": osm_host,
            "datafordeler": man["files"]}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these "
          f"files and never fetch.")
