"""Download Ottawa's raw inputs. Run this before the steps.

DELIBERATELY NOT NAMED step*.py - `drift_check.py` globs step*.py, and a
download in a step would make every drift check a question about the current
upstream rather than the committed code.

    python pipeline/ottawa/fetch_sources.py [--force]

Three keyless downloads: Ottawa Public Health's inspection feed (the LIVES
zip), the City's 2022-2026 wards, and OSM's rail relations (Overpass). The
feed may be retired without notice (see config), so a cached copy is never
replaced without --force.
"""
import argparse
import io
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import osm  # noqa: E402
from pipeline.ottawa import config  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
FEED_MEMBERS = {"businesses.csv", "inspections.csv", "feed_info.csv"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get(url, dest, force, label, params=None, check=None):
    if dest.exists() and not force:
        print(f"  {label}: cached {dest.name} ({dest.stat().st_size:,} bytes)")
        return
    r = requests.get(url, params=params, timeout=600, headers=HEADERS)
    r.raise_for_status()
    if len(r.content) < 100:
        sys.exit(f"  {label}: a {len(r.content)}-byte answer - a failed fetch, not a negative")
    if check:
        check(r.content)
    dest.write_bytes(r.content)
    print(f"  {label}: {len(r.content):,} bytes -> {dest.name}")


def check_feed(content):
    # The bot challenge answers HTTP 200 with HTML; only a real zip is data.
    if content[:2] != b"PK":
        sys.exit(f"  feed: not a zip ({content[:60]!r}) - the host's bot challenge, "
                 "most likely. Not cached")
    names = set(zipfile.ZipFile(io.BytesIO(content)).namelist())
    if not FEED_MEMBERS <= names:
        sys.exit(f"  feed: members {sorted(names)} lack {sorted(FEED_MEMBERS - names)}")


def fetch_rail():
    s, w, n, e = config.RAIL_BBOX
    modes = "|".join(config.ROUTE_TYPES)
    q = ("[out:json][timeout:120];"
         f'(relation["type"="route"]["route"~"^({modes})$"]({s},{w},{n},{e}););'
         "out geom;node(r);out tags center;")
    els, host = osm.fetch(q, config.OSM_ROUTES_JSON)
    rels = [x for x in els if x["type"] == "relation"]
    if not rels:
        sys.exit("  no route relations came back - a FAILED fetch, not a negative")
    print(f"  rail: {len(rels)} relations via {host}")
    return host


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download cached files")
    args = ap.parse_args()
    for d in (config.DATA_RAW, config.OUTPUTS):
        d.mkdir(parents=True, exist_ok=True)

    print("Inspection feed:")
    get(config.FEED_URL, config.FEED_ZIP, args.force, "feed", check=check_feed)
    with zipfile.ZipFile(config.FEED_ZIP) as z:
        feed_info = z.read("feed_info.csv").decode("utf-8").splitlines()
    print(f"  feed_info: {feed_info[-1]}")
    print("\nBoundary:")
    get(config.CITY_BOUNDARY_URL, config.CITY_BOUNDARY_GEOJSON, args.force, "wards",
        params=config.CITY_BOUNDARY_QUERY)
    # Overpass last: its 504s come in waves, and a re-run skips what is cached.
    print("\nOpenStreetMap (keyless):")
    host = fetch_rail()

    def stamp(path):
        return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(
            timespec="seconds")

    files = {p.name: stamp(p) for p in (config.FEED_ZIP, config.CITY_BOUNDARY_GEOJSON,
                                        config.OSM_ROUTES_JSON)}
    prov = {"written_utc": _now(), "osm_host": host, "osm_bbox": config.RAIL_BBOX,
            "as_of_date": config.AS_OF_DATE, "feed_info": feed_info[-1], "files_utc": files,
            "sources": {"feed": config.FEED_URL, "wards": config.CITY_BOUNDARY_URL}}
    config.PROVENANCE_JSON.write_text(json.dumps(prov, indent=2), encoding="utf-8")
    print(f"\nprovenance -> {config.PROVENANCE_JSON.name}. The steps read these "
          f"files and never fetch.")


if __name__ == "__main__":
    main()
