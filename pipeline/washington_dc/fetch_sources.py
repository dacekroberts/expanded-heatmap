"""Download Washington D.C.'s three raw inputs. Run this before the steps.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline.

    set WMATA_API_KEY=...            (PowerShell: $env:WMATA_API_KEY = "...")
    python pipeline/washington_dc/fetch_sources.py [--force]

TWO THINGS HERE ARE UNLIKE EVERY OTHER CITY.

**The transit feed needs a key.** `api.wmata.com` returns 401 unauthenticated,
and it is the only feed in the project that does. The key is the owner's, is
WMATA's property under §5 of its Transit Data Terms of Use, and must never
enter this repo or any output - so it is read from the environment and printed
nowhere, not even in an error message.

**The transit feed EXPIRES.** WMATA declares `feed_start_date` and
`feed_end_date` ten days apart, the shortest window of any feed here. A stored
copy therefore goes stale in under a fortnight, and the failure mode is silent:
an expired feed still parses, still has 98 stations, and still builds a map -
it just may not be the current network. So the window is checked on every run,
including runs that would otherwise skip the download, and an expired copy is
an error rather than a warning.
"""

import argparse
import csv
import io
import json
import os
import sys
import zipfile
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.washington_dc.config import (  # noqa: E402
    BUSINESS_CSV,
    BUSINESS_OUT_FIELDS,
    BUSINESS_RENTAL_ACTIVITIES,
    BUSINESS_SERVICE_URL,
    BUSINESS_WHERE_ACTIVE,
    BOUNDARY_SERVICE_URL,
    CITY_BOUNDARY_GEOJSON,
    DATA_RAW,
    GTFS_API_KEY_ENV,
    GTFS_FEED_INFO_MEMBER,
    GTFS_URL,
    GTFS_ZIP,
    STATES_GEOJSON,
    STATES_NAME_FIELD,
    STATES_SERVICE_URL,
    STATES_WHERE,
)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
PAGE = 2000  # the layer's own maxRecordCount; asking for more is silently capped


def _quote_list(values):
    return ", ".join("'" + v.replace("'", "''") + "'" for v in values)


BUSINESS_WHERE = (
    f"{BUSINESS_WHERE_ACTIVE} AND BUSINESSACTIVITY NOT IN "
    f"({_quote_list(BUSINESS_RENTAL_ACTIVITIES)})"
)


def check_feed_window(zip_path: Path):
    """Read feed_info.txt out of the stored zip and refuse an expired feed."""
    with zipfile.ZipFile(zip_path) as z:
        if GTFS_FEED_INFO_MEMBER not in z.namelist():
            sys.exit(f"{zip_path.name}: no {GTFS_FEED_INFO_MEMBER}. WMATA has "
                     f"always published one; if it is really gone, the "
                     f"ten-day-window check in this file needs rethinking "
                     f"rather than deleting.")
        text = z.read(GTFS_FEED_INFO_MEMBER).decode("utf-8-sig")
    row = next(csv.DictReader(io.StringIO(text)))
    start, end = row.get("feed_start_date"), row.get("feed_end_date")
    if not end:
        sys.exit(f"{zip_path.name}: feed_info.txt has no feed_end_date.")
    end_date = date(int(end[:4]), int(end[4:6]), int(end[6:8]))
    today = date.today()
    print(f"GTFS validity: {start} to {end} "
          f"({(end_date - today).days:+d} days from today)")
    if end_date < today:
        sys.exit(f"GTFS feed expired on {end}. WMATA's window is ten days, so "
                 f"a stored copy goes stale fast and an expired feed would "
                 f"build a quietly outdated map. Re-run with --force to "
                 f"download the current one.")


def fetch_gtfs(force: bool):
    if GTFS_ZIP.exists() and not force:
        print(f"have {GTFS_ZIP.name} ({GTFS_ZIP.stat().st_size:,} bytes) "
              f"- skipping download, still checking the window")
        check_feed_window(GTFS_ZIP)
        return
    key = os.environ.get(GTFS_API_KEY_ENV, "").strip()
    if not key:
        sys.exit(
            f"{GTFS_API_KEY_ENV} is not set. WMATA is the only feed in this "
            f"project behind a key: api.wmata.com returns 401 without one.\n"
            f"  1. register a free developer account at developer.wmata.com\n"
            f"  2. subscribe to the GTFS product\n"
            f"  3. export the primary key as {GTFS_API_KEY_ENV}\n"
            f"The key stays out of this repo - it is WMATA's property under "
            f"§5 of the Transit Data Terms of Use and may be revoked.")
    r = requests.get(GTFS_URL, timeout=900,
                     headers={**HEADERS, "api_key": key})
    if r.status_code == 401:
        # Never echo the key, not even truncated.
        sys.exit(f"GTFS download: HTTP 401. The {GTFS_API_KEY_ENV} value was "
                 f"rejected - check the subscription covers the GTFS product.")
    if r.status_code != 200 or r.content[:2] != b"PK":
        sys.exit(f"GTFS download failed: HTTP {r.status_code}, "
                 f"{len(r.content):,} bytes")
    zipfile.ZipFile(io.BytesIO(r.content)).testzip()
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    GTFS_ZIP.write_bytes(r.content)
    print(f"GTFS: wrote {len(r.content):,} bytes to {GTFS_ZIP}")
    check_feed_window(GTFS_ZIP)


def fetch_boundary(force: bool):
    if CITY_BOUNDARY_GEOJSON.exists() and not force:
        print(f"have {CITY_BOUNDARY_GEOJSON.name} "
              f"({CITY_BOUNDARY_GEOJSON.stat().st_size:,} bytes) - skipping")
        return
    r = requests.get(f"{BOUNDARY_SERVICE_URL}/query", params={
        "where": "1=1", "outFields": "*", "outSR": "4326",
        "f": "geojson"}, timeout=600, headers=HEADERS)
    if r.status_code != 200 or b'"features"' not in r.content:
        sys.exit(f"boundary download failed: HTTP {r.status_code}\n"
                 f"{r.text[:400]}")
    n = len(json.loads(r.content)["features"])
    if n != 1:
        sys.exit(f"boundary: expected 1 polygon, got {n}. Layer 10 of this "
                 f"service has always been the single District outline.")
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    CITY_BOUNDARY_GEOJSON.write_bytes(r.content)
    print(f"boundary: wrote 1 polygon, {len(r.content):,} bytes to "
          f"{CITY_BOUNDARY_GEOJSON}")


def fetch_states(force: bool):
    """Three state polygons, so an excluded station can be NAMED not just
    counted. See config.STATES_SERVICE_URL for why this exists."""
    if STATES_GEOJSON.exists() and not force:
        print(f"have {STATES_GEOJSON.name} "
              f"({STATES_GEOJSON.stat().st_size:,} bytes) - skipping")
        return
    r = requests.get(f"{STATES_SERVICE_URL}/query", params={
        "where": STATES_WHERE, "outFields": STATES_NAME_FIELD,
        "outSR": "4326", "returnGeometry": "true",
        "f": "geojson"}, timeout=600, headers=HEADERS)
    if r.status_code != 200 or b'"features"' not in r.content:
        sys.exit(f"states download failed: HTTP {r.status_code}\n"
                 f"{r.text[:400]}")
    names = sorted(f["properties"][STATES_NAME_FIELD]
                   for f in json.loads(r.content)["features"])
    if len(names) != 3:
        sys.exit(f"states: expected 3 polygons, got {len(names)}: {names}")
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    STATES_GEOJSON.write_bytes(r.content)
    print(f"states: wrote {names}, {len(r.content):,} bytes to "
          f"{STATES_GEOJSON}")


def fetch_businesses(force: bool):
    """Paged ArcGIS download of the active, in-District, non-rental licences.

    The `outFields` list is the privacy control, and it lives here rather than
    in step 2 on purpose: the owner and agent name columns, and the billing
    address, are never requested, so they are never on this machine to leak.
    """
    if BUSINESS_CSV.exists() and not force:
        print(f"have {BUSINESS_CSV.name} ({BUSINESS_CSV.stat().st_size:,} "
              f"bytes) - skipping")
        return
    url = f"{BUSINESS_SERVICE_URL}/query"
    base = {
        "where": BUSINESS_WHERE,
        "outFields": ",".join(BUSINESS_OUT_FIELDS),
        "returnGeometry": "false",
        "orderByFields": "OBJECTID ASC",
        "f": "json",
    }
    r = requests.get(url, params={**base, "returnCountOnly": "true"},
                     timeout=300, headers=HEADERS)
    expected = r.json().get("count")
    if not expected:
        sys.exit(f"business count query returned {r.text[:400]}")
    print(f"business licences to download: {expected:,}")

    rows, offset = [], 0
    while True:
        r = requests.get(url, params={**base, "resultOffset": offset,
                                      "resultRecordCount": PAGE},
                         timeout=300, headers=HEADERS)
        if r.status_code != 200:
            sys.exit(f"business page at offset {offset}: HTTP {r.status_code}")
        payload = r.json()
        if "error" in payload:
            sys.exit(f"business page at offset {offset}: "
                     f"{str(payload['error'])[:400]}")
        page = [f["attributes"] for f in payload.get("features", [])]
        if not page:
            break
        rows.extend(page)
        offset += len(page)
        print(f"  {offset:>7,} / {expected:,}")
        if not payload.get("exceededTransferLimit") and offset >= expected:
            break

    if len(rows) != expected:
        sys.exit(f"downloaded {len(rows):,} rows but the server counted "
                 f"{expected:,} - paging is incomplete, so stopping rather "
                 f"than building on a partial register.")
    leaked = sorted(set().union(*(r.keys() for r in rows))
                    - set(BUSINESS_OUT_FIELDS))
    if leaked:
        sys.exit(f"server returned unrequested columns {leaked} - check them "
                 f"before writing, they may be personal data.")

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    tmp = BUSINESS_CSV.with_suffix(".partial")
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(BUSINESS_OUT_FIELDS),
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    tmp.replace(BUSINESS_CSV)
    print(f"businesses: wrote {len(rows):,} rows to {BUSINESS_CSV}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    fetch_gtfs(args.force)
    fetch_boundary(args.force)
    fetch_states(args.force)
    fetch_businesses(args.force)


if __name__ == "__main__":
    main()
