"""Download Prague's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/prague/fetch_sources.py [--force]

Every source is keyless. A cached file is kept and recorded, never silently
refreshed - `--force` re-downloads. Magic bytes are checked on every download.

Two things here are unlike the other cities:

  * **RUIAN comes through ČÚZK's ATOM service**, which names the current
    month's file, rather than from a hard-coded `vymenny_format` path - the
    date in that path goes stale on the 1st of every month, and the ATOM
    service is the channel ČÚZK intends for machines.
  * **PID's feed self-attests a two-week window**, so the window is printed on
    every run and an expired copy is refused (WMATA's rule): a stale feed
    still parses and still builds a map.
"""
import argparse
import hashlib
import json
import re
import sys
import urllib.request
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.countries import czechia as CZ  # noqa: E402
from pipeline.prague import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def _get(url, dest, label, magic, timeout=1800):
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
    print(f"  {label:26s} {dest.stat().st_size:13,} bytes downloaded")


def _record(prov, key, path, url, fetched):
    prov[key] = {"file": path.name, "url": url, "bytes": path.stat().st_size,
                 "sha256": _sha256(path), "retrieved": fetched}


def fetch(url, dest, label, magic, prov, key, force):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not force:
        print(f"  {label:26s} cached ({dest.stat().st_size:,} bytes)")
        old = prov.get(key, {})
        if old.get("sha256") == _sha256(dest):
            return
        _record(prov, key, dest, url, old.get("retrieved") or "cached before provenance")
        return
    _get(url, dest, label, magic)
    _record(prov, key, dest, url, datetime.now(timezone.utc).isoformat(timespec="seconds"))


def ruian_url():
    """The current Praha address file, as ČÚZK's ATOM feed names it."""
    atom = CZ.RUIAN_ATOM_TEMPLATE.format(obec=config.OBEC)
    with urllib.request.urlopen(urllib.request.Request(atom, headers=HEADERS),
                                timeout=120) as r:
        text = r.read().decode("utf-8")
    links = re.findall(r'href="([^"]+_ADR\.csv\.zip)"', text)
    if len(links) != 1:
        sys.exit(f"  ATOM feed for obec {config.OBEC}: expected one ADR zip link, "
                 f"found {links}")
    return links[0]


def feed_window(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        head, row = z.read("feed_info.txt").decode("utf-8-sig").splitlines()[:2]
    info = dict(zip(head.split(","), row.split(",")))
    start, end = info.get("feed_start_date", ""), info.get("feed_end_date", "")
    end_date = date(int(end[:4]), int(end[4:6]), int(end[6:8]))
    print(f"  PID feed window {start} to {end} "
          f"({(end_date - date.today()).days:+d} days from today)")
    if end_date < date.today():
        sys.exit("  PID's feed has expired - re-run with --force for the current one")
    return {"feed_start_date": start, "feed_end_date": end,
            "publisher": info.get("feed_publisher_name")}


def fetch_osm(force):
    s, w, n, e = 49.90, 14.20, 50.20, 14.75
    boundary = (f"[out:json][timeout:180];rel({config.OSM_BOUNDARY_RELATION});out geom;")
    els, host = osm.fetch(boundary, config.OSM_BOUNDARY_JSON, force=force)
    print(f"  {'osm_boundary':26s} {len(els)} relation via {host}")
    rail = ('[out:json][timeout:180];'
            f'(relation["type"="route"]["route"="subway"]({s},{w},{n},{e}););'
            'out geom;node(r);out tags center;')
    els, host = osm.fetch(rail, config.OSM_RAIL_JSON, force=force)
    rels = sum(1 for x in els if x["type"] == "relation")
    print(f"  {'osm_rail (cross-check)':26s} {rels} subway relations via {host}")
    return host


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS, CZ.SHARED_RAW, CZ.NACE_DIR):
        d.mkdir(parents=True, exist_ok=True)
    prov = (json.loads(config.PROVENANCE_JSON.read_text(encoding="utf-8"))
            if config.PROVENANCE_JSON.exists() else {})

    print("National (shared by every Czech city):")
    fetch(CZ.ROS02_URL, CZ.ROS02_CSV, "ros02_data.csv", b'"ICP"', prov, "ros02", args.force)
    # ROS02 dates itself: every row carries the file's DATPLAT, which the page
    # shows and step 2 judges "active" against.
    import pandas as pd
    prov["ros02_snapshot"] = str(pd.read_csv(CZ.ROS02_CSV, dtype=str,
                                             usecols=["DATPLAT"])["DATPLAT"].max())
    print(f"  {'':26s} ROS02 snapshot {prov['ros02_snapshot']}")
    fetch(CZ.RES_URL, CZ.RES_CSV, "res_data.csv", b"ICO,", prov, "res", args.force)
    for level, kodcis in CZ.NACE_LEVEL_CODEBOOKS.items():
        fetch(CZ.NACE_CODEBOOK_URL.format(kodcis=kodcis),
              CZ.NACE_DIR / f"cz_nace_2025_level{level}.csv",
              f"CZ-NACE 2025 level {level}", b"", prov, f"nace_level{level}", args.force)

    print("\nPrague:")
    # Resolved on every run - one small ATOM response - so the record names the
    # month's file even when the cached copy is kept.
    url = ruian_url()
    print(f"  ATOM names the current RUIAN file: {url.rsplit('/', 1)[-1]}")
    fetch(url, config.RUIAN_ZIP, "ruian_adr (RUIAN)", b"PK", prov, "ruian", args.force)
    fetch(config.GTFS_URL, config.GTFS_ZIP, "pid_gtfs.zip", b"PK\x03\x04", prov,
          "gtfs", args.force)
    prov["gtfs_feed_info"] = feed_window(config.GTFS_ZIP)
    prov["osm_host"] = fetch_osm(args.force)

    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these files "
          f"and never fetch.")
