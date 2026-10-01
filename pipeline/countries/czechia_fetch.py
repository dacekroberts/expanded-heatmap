"""Downloads shared by every Czech tram city's `fetch_sources.py`.

⚠ **ONLY `fetch_sources.py` IMPORTS THIS.** It downloads, and a step never
fetches (`scripts/check_no_fetch_in_steps.py` follows imports into shared
modules). Written for the Czech tram batch (`czech-tram-city`), from Prague's
`fetch_sources.py`, which stays as it is.

What differs from Prague's, and why:

  * **The national files are checked, never fetched.** ROS02, RES and the
    CZ-NACE codebooks live once in the shared `data/czechia/raw/`, and a new
    edition fetched from a city branch would move Prague too. A refresh is its
    own job.
  * **Rolling sources are always downloaded** (the owner's rule: feeds are
    fetched at build, never cached across weeks) - KORDIS's GTFS, the OSM
    queries - and so is each obec's RUIAN file, which ATOM names by month.
  * **One Overpass query at a time, one per city for the trams**, and a
    60-second wait after a failed round before the one retry (the owner's
    staggering rule, 2026-09-30).
"""
import csv
import hashlib
import io
import re
import sys
import time
import urllib.request
import zipfile
from datetime import date, datetime, timezone

from pipeline import osm
from pipeline.countries import czechia as CZ

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def record(prov, key, path, url, retrieved):
    prov[key] = {"file": path.name, "url": url, "bytes": path.stat().st_size,
                 "sha256": sha256(path), "retrieved": retrieved}


def download(url, dest, label, magic, timeout=600):
    """Always a fresh copy; magic bytes checked; written through a .part."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as fh:
        while True:
            chunk = r.read(1 << 22)
            if not chunk:
                break
            fh.write(chunk)
    head = tmp.read_bytes()[:len(magic) or 1]
    if magic and not head.startswith(magic):
        tmp.unlink()
        sys.exit(f"  {label}: wrong magic bytes {head!r} - not the file asked for")
    tmp.replace(dest)
    print(f"  {label:28s} {dest.stat().st_size:13,} bytes downloaded")


def national(prov):
    """Check the shared national files and record them; never fetch them."""
    need = [(CZ.ROS02_CSV, "ros02"), (CZ.RES_CSV, "res")] + [
        (CZ.NACE_DIR / f"cz_nace_2025_level{lv}.csv", f"nace_level{lv}")
        for lv in CZ.NACE_LEVEL_CODEBOOKS]
    for path, key in need:
        if not path.exists():
            sys.exit(f"  missing the shared national file {path}. It is fetched once, "
                     f"for every Czech city, by pipeline/prague/fetch_sources.py - never "
                     f"from a city branch.")
        old = prov.get(key, {})
        if old.get("sha256") != sha256(path):
            record(prov, key, path, old.get("url", ""), old.get("retrieved") or
                   "shared national cache (data/czechia/raw), checked " + now())
        print(f"  {path.name:28s} {path.stat().st_size:13,} bytes (shared national cache)")
    # ROS02 dates itself: every row carries DATPLAT, which the page shows and
    # step 2 judges "active" against. Read one column, streamed.
    snap = ""
    with open(CZ.ROS02_CSV, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            snap = max(snap, row["DATPLAT"] or "")
    prov["ros02_snapshot"] = snap
    print(f"  {'':28s} ROS02 snapshot {snap}")


def ruian(cfg, prov):
    """Each obec's current RUIAN address file, as ČÚZK's ATOM feed names it."""
    prov["ruian"] = {}
    for obec in cfg.OBEC_CODES:
        atom = CZ.RUIAN_ATOM_TEMPLATE.format(obec=obec)
        with urllib.request.urlopen(urllib.request.Request(atom, headers=HEADERS),
                                    timeout=120) as r:
            text = r.read().decode("utf-8")
        links = re.findall(r'href="([^"]+_ADR\.csv\.zip)"', text)
        if len(links) != 1:
            sys.exit(f"  ATOM feed for obec {obec}: expected one ADR zip link, found {links}")
        name = links[0].rsplit("/", 1)[-1]
        print(f"  ATOM names obec {obec}'s RUIAN file: {name}")
        download(links[0], cfg.RUIAN_ZIPS[obec], f"ruian_adr_{obec}", b"PK")
        record(prov["ruian"], obec, cfg.RUIAN_ZIPS[obec], links[0], now())
        prov["ruian"][obec]["edition"] = name


def gtfs_calendar_window(zip_path):
    """The window a feed with no feed_info.txt covers: the earliest start and
    latest end across calendar.txt and calendar_dates.txt."""
    with zipfile.ZipFile(zip_path) as z:
        names = set(z.namelist())
        starts, ends = [], []
        if "calendar.txt" in names:
            for row in csv.DictReader(io.TextIOWrapper(z.open("calendar.txt"), "utf-8-sig")):
                starts.append(row["start_date"])
                ends.append(row["end_date"])
        if "calendar_dates.txt" in names:
            for row in csv.DictReader(io.TextIOWrapper(z.open("calendar_dates.txt"), "utf-8-sig")):
                starts.append(row["date"])
                ends.append(row["date"])
    if not ends:
        sys.exit(f"  {zip_path.name}: no calendar.txt or calendar_dates.txt")
    start, end = min(starts), max(ends)
    end_date = date(int(end[:4]), int(end[4:6]), int(end[6:8]))
    print(f"  feed calendar window {start} to {end} "
          f"({(end_date - date.today()).days:+d} days from today)")
    if end_date < date.today():
        sys.exit("  the feed has expired - its publisher has not republished it")
    return {"calendar_start": start, "calendar_end": end}


def overpass(query, dest, label):
    """One query, always fresh; a failed round waits 60 s before its one retry."""
    for attempt in (1, 2):
        try:
            els, host = osm.fetch(query, dest, force=True, retries=1)
            print(f"  {label:28s} {len(els):,} elements via {host}")
            return host
        except Exception as exc:  # every mirror failed this round
            if attempt == 2:
                raise
            print(f"  {label}: {exc} - waiting 60 s before the one retry")
            time.sleep(60)


def osm_boundaries(cfg):
    ids = ",".join(str(r) for r in cfg.OSM_BOUNDARY_RELATIONS.values())
    return overpass(f"[out:json][timeout:120];rel(id:{ids});out geom;",
                    cfg.OSM_BOUNDARY_JSON, "osm_boundary")


def osm_trams(cfg):
    """Every route=tram relation in the box, with way geometry, and its nodes -
    plus every tagged tram stop in the box, which a STATION_ADD needs: such a
    stop is on no relation (Plzeň's Jízdecká and U Synagogy, 2026-09-30), so
    node(r) alone never fetches it. Steps read relation members only, so the
    extra nodes move no one's stations."""
    s, w, n, e = cfg.OSM_TRAM_BBOX
    q = ("[out:json][timeout:120];"
         f'relation["type"="route"]["route"="tram"]({s},{w},{n},{e});'
         "out geom;"
         f'(node(r);node["railway"="tram_stop"]({s},{w},{n},{e}););out body;')
    return overpass(q, cfg.OSM_TRAM_JSON, "osm_tram")


def utf8_console():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
