"""Download Berlin's raw inputs into data/berlin/raw/ (gitignored).

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/berlin/fetch_sources.py [--force]

Every source is keyless. Checks on every file, because a host can answer with
the wrong thing and HTTP 200:

  * the GTFS by its zip magic bytes;
  * the register by its HEADER, which must be exactly the expected columns -
    an unexpected column (a name, a street) stops the fetch and deletes the
    file, because the CSV channel cannot select columns the way a WFS can;
  * the boundary by its geometry type and feature count.
"""
import argparse
import json
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.berlin import config

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}

# Name-like fragments that must never be in the register's header. The brief's
# check berlin-wfs-schema asserts the same absence on the WFS.
FORBIDDEN_FRAGMENTS = ("name", "firma", "inhaber", "strasse", "straße", "street",
                       "hausnummer", "email", "telefon", "phone")


def _stream(url, dest, label, timeout=1800):
    req = urllib.request.Request(url, headers=HEADERS)
    tmp = dest.with_suffix(dest.suffix + ".part")
    done = 0
    with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as fh:
        while True:
            chunk = r.read(1 << 22)
            if not chunk:
                break
            fh.write(chunk)
            done += len(chunk)
    print(f"  {label:26s} {done:13,} bytes")
    return tmp


def check_register_header(path):
    with open(path, encoding=config.SOURCE_ENCODING) as fh:
        first = fh.readline().lstrip("﻿").strip()
    delim = ";" if first.count(";") > first.count(",") else ","
    cols = [c.strip().strip('"') for c in first.split(delim)]
    bad = [c for c in cols if any(f in c.lower() for f in FORBIDDEN_FRAGMENTS)
           and c not in config.REGISTER_ALLOWED_NAMEISH]
    return cols, delim, bad


def feed_info(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "feed_info.txt" not in names:
            print("  feed_info.txt: absent")
            return {"missing_feed_info": True}
        lines = z.read("feed_info.txt").decode("utf-8-sig").splitlines()
    info = dict(zip(lines[0].split(","), lines[1].split(",")))
    print(f"  feed_info: {info}")
    return info


def fetch_boundary():
    req = urllib.request.Request(config.BOUNDARY_URL, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=300) as r:
        obj = json.loads(r.read())
    feats = obj.get("features") or []
    if len(feats) != 1 or feats[0]["geometry"]["type"] not in ("Polygon", "MultiPolygon"):
        sys.exit(f"  boundary: expected 1 polygon feature, got {len(feats)} "
                 f"({[f['geometry']['type'] for f in feats]})")
    config.CITY_BOUNDARY_GEOJSON.write_text(json.dumps(obj), encoding="utf-8")
    print(f"  {'city_boundary':26s} {feats[0]['geometry']['type']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.DATA_PROCESSED, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)
    prov = {"fetched_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "businesses_url": config.BUSINESSES_URL, "gtfs_url": config.GTFS_URL,
            "boundary_url": config.BOUNDARY_URL}

    dest = config.BUSINESSES_RAW_CSV
    if dest.exists() and not args.force:
        print(f"  {dest.name:26s} cached ({dest.stat().st_size:,} bytes)")
    else:
        tmp = _stream(config.BUSINESSES_URL, dest, dest.name)
        cols, delim, bad = check_register_header(tmp)
        if bad:
            tmp.unlink()
            sys.exit(f"  register header carries name-like column(s) {bad} - "
                     f"deleted, not kept. Read the source before going on.")
        tmp.replace(dest)
    cols, delim, bad = check_register_header(dest)
    if bad:
        sys.exit(f"  cached register carries name-like column(s) {bad}")
    print(f"  register columns ({delim!r}): {cols}")
    prov["register_columns"] = cols

    if config.GTFS_ZIP.exists() and not args.force:
        print(f"  {'gtfs.zip':26s} cached")
    else:
        tmp = _stream(config.GTFS_URL, config.GTFS_ZIP, "gtfs.zip")
        if not tmp.read_bytes()[:4].startswith(b"PK\x03\x04"):
            tmp.unlink()
            sys.exit("  gtfs.zip: wrong magic bytes - not a zip")
        tmp.replace(config.GTFS_ZIP)
    prov["feed_info"] = feed_info(config.GTFS_ZIP)

    if config.CITY_BOUNDARY_GEOJSON.exists() and not args.force:
        print(f"  {'city_boundary':26s} cached")
    else:
        fetch_boundary()

    config.PROVENANCE_JSON.write_text(json.dumps(prov, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}")
