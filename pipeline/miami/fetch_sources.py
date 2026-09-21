"""Download Miami's three raw inputs. Run this before the steps.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline.

    python pipeline/miami/fetch_sources.py [--force]

Three sources, all public, all recorded in docs/data_sources.md:

1. Miami-Dade "Local Business Tax" (ArcGIS FeatureServer). Filtered
   server-side to ACCSTATUS='Active'; every category is downloaded, so step 2's
   own taxonomy filter still reports a meaningful drop count. ~176k rows at
   2,000 per page, paged on OBJECTID so paging is stable.
2. Miami-Dade Transit GTFS. Note the host: `transitdata.miamidade.gov` does NOT
   resolve, and `www.miamidade.gov` does - the latter is also what the Mobility
   Database lists as the official URL.
3. Miami-Dade municipal boundaries. A MULTI-municipality layer on purpose: this
   map is regional, so the boundary work is naming which municipality each
   station sits in, not filtering to one city. Its MUNICID joins to the
   business file's MUNBUSLOC prefix, and both come from the same publisher.
"""

import argparse
import csv
import io
import sys
import time
import zipfile
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.miami.config import (  # noqa: E402
    BOUNDARY_SERVICE_URL,
    BUSINESSES_RAW_CSV,
    BUSINESS_SERVICE_URL,
    BUSINESS_STATUS_FILTER,
    CITY_BOUNDARY_GEOJSON,
    DATA_RAW,
    DOWNLOAD_FIELDS,
    GTFS_URL,
    GTFS_ZIP,
)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
PAGE = 2000


def fetch_businesses(force: bool):
    if BUSINESSES_RAW_CSV.exists() and not force:
        print(f"have {BUSINESSES_RAW_CSV.name} "
              f"({BUSINESSES_RAW_CSV.stat().st_size:,} bytes) - skipping")
        return
    total = requests.get(f"{BUSINESS_SERVICE_URL}/query", params={
        "where": BUSINESS_STATUS_FILTER, "returnCountOnly": "true",
        "f": "json"}, timeout=180, headers=HEADERS).json().get("count")
    print(f"{total:,} rows match {BUSINESS_STATUS_FILTER!r}; "
          f"paging {PAGE:,} at a time")

    rows, offset = [], 0
    while True:
        r = requests.get(f"{BUSINESS_SERVICE_URL}/query", params={
            "where": BUSINESS_STATUS_FILTER,
            "outFields": ",".join(DOWNLOAD_FIELDS),
            "orderByFields": "OBJECTID",       # stable paging
            "returnGeometry": "false",
            "resultOffset": offset,
            "resultRecordCount": PAGE,
            "f": "json"}, timeout=300, headers=HEADERS)
        if r.status_code != 200:
            sys.exit(f"HTTP {r.status_code} at offset {offset}: {r.text[:300]}")
        j = r.json()
        if "error" in j:
            sys.exit(f"service error at offset {offset}: {j['error']}")
        feats = j.get("features", [])
        if not feats:
            break
        rows.extend(f["attributes"] for f in feats)
        offset += len(feats)
        if offset % 20000 == 0 or len(feats) < PAGE:
            print(f"  ...{offset:,}/{total:,}", flush=True)
        if len(feats) < PAGE:
            break
        time.sleep(0.15)

    if total and abs(len(rows) - total) > PAGE:
        print(f"  WARNING: got {len(rows):,} rows for a reported {total:,}. "
              f"Deep paging can skip rows if the service is edited mid-run; "
              f"re-run with --force before trusting a build.")

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    tmp = BUSINESSES_RAW_CSV.with_suffix(".partial")
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(DOWNLOAD_FIELDS))
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k) for k in DOWNLOAD_FIELDS})
    tmp.replace(BUSINESSES_RAW_CSV)
    print(f"wrote {len(rows):,} rows to {BUSINESSES_RAW_CSV}")


def fetch_gtfs(force: bool):
    if GTFS_ZIP.exists() and not force:
        print(f"have {GTFS_ZIP.name} ({GTFS_ZIP.stat().st_size:,} bytes) - skipping")
        return
    r = requests.get(GTFS_URL, timeout=600, headers=HEADERS)
    if r.status_code != 200 or r.content[:2] != b"PK":
        sys.exit(f"GTFS download failed: HTTP {r.status_code}, "
                 f"{len(r.content):,} bytes, zip={r.content[:2] == b'PK'}")
    zipfile.ZipFile(io.BytesIO(r.content)).testzip()
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    GTFS_ZIP.write_bytes(r.content)
    print(f"wrote {len(r.content):,} bytes to {GTFS_ZIP}")


def fetch_boundary(force: bool):
    if CITY_BOUNDARY_GEOJSON.exists() and not force:
        print(f"have {CITY_BOUNDARY_GEOJSON.name} "
              f"({CITY_BOUNDARY_GEOJSON.stat().st_size:,} bytes) - skipping")
        return
    r = requests.get(f"{BOUNDARY_SERVICE_URL}/query", params={
        "where": "1=1", "outFields": "MUNICID,NAME", "outSR": "4326",
        "f": "geojson"}, timeout=300, headers=HEADERS)
    if r.status_code != 200:
        sys.exit(f"boundary HTTP {r.status_code}: {r.text[:300]}")
    if b'"features"' not in r.content:
        sys.exit(f"boundary response is not GeoJSON: {r.text[:300]}")
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    CITY_BOUNDARY_GEOJSON.write_bytes(r.content)
    print(f"wrote {len(r.content):,} bytes to {CITY_BOUNDARY_GEOJSON}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    fetch_gtfs(args.force)
    fetch_boundary(args.force)
    fetch_businesses(args.force)


if __name__ == "__main__":
    main()
