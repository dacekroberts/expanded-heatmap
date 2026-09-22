"""Download Calgary's three raw inputs. Run this before the steps.

    python pipeline/calgary/fetch_sources.py [--force]

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline.

TWO THINGS HERE ARE UNLIKE THE OTHER CITIES.

**There is NO feed validity window to check, and that is a finding rather than
an omission.** Neither the Mobility Database mirror nor Calgary Transit's own
feed carries `feed_info.txt`, so the `feed_end_date` guard written for D.C.,
Montréal and Vancouver cannot be written here at all. What this script does
instead is print the Socrata resource's own `updatedAt`, which is the only
staleness signal available.

**The boundary has two Socrata views and one of them is empty.** `7t9h-2z9s`
is a `map` view and exports 53 bytes of unreadable GeoJSON; `erra-cqp9` is the
`dataset` view and carries the real MultiPolygon. This script takes the latter
and asserts the geometry is real, because a 53-byte file is a valid HTTP 200.
"""

import argparse
import sys
import zipfile
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.calgary.config import (  # noqa: E402
    BUSINESS_LIMIT,
    BUSINESS_URL,
    BUSINESSES_RAW_CSV,
    CITY_BOUNDARY_GEOJSON,
    CITY_BOUNDARY_URL,
    DATA_RAW,
    FORBIDDEN_COLUMNS,
    GTFS_URL,
    GTFS_ZIP,
)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
# The business register's Socrata id, for the updatedAt probe below.
BUSINESS_VIEW = "vdjc-pybd"


def get(url, path: Path, *, force, label, params=None, min_bytes=1024):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"  {label}: have {path.name} "
              f"({path.stat().st_size:,} bytes) - skipping")
        return path
    print(f"  {label}: GET {url}")
    r = requests.get(url, params=params, headers=HEADERS, timeout=900)
    if r.status_code != 200:
        sys.exit(f"  {label}: HTTP {r.status_code}\n{r.text[:400]}")
    if len(r.content) < min_bytes:
        sys.exit(f"  {label}: only {len(r.content)} bytes. For the boundary "
                 f"this is THE known trap - the `map` view (7t9h-2z9s) returns "
                 f"53 bytes of valid but empty GeoJSON. Use the `dataset` "
                 f"view.\n{r.text[:300]}")
    path.write_bytes(r.content)
    print(f"  {label}: wrote {path.name} ({len(r.content):,} bytes)")
    return path


def report_freshness():
    """The only staleness signal Calgary offers: neither GTFS feed declares a
    validity window, so the register's own updatedAt is what there is."""
    try:
        r = requests.get(f"https://data.calgary.ca/api/views/{BUSINESS_VIEW}.json",
                         headers=HEADERS, timeout=120)
        if r.status_code == 200:
            d = r.json()
            import datetime as _dt
            for key in ("rowsUpdatedAt", "viewLastModified", "createdAt"):
                if d.get(key):
                    when = _dt.datetime.fromtimestamp(d[key], _dt.timezone.utc)
                    age = (_dt.datetime.now(_dt.timezone.utc) - when).days
                    print(f"  business register {key}: {when:%Y-%m-%d} "
                          f"({age} days ago)")
            lic = d.get("license", {})
            if lic:
                print(f"  declared licence: {lic.get('name')}")
    except Exception as exc:
        print(f"  freshness probe failed ({type(exc).__name__}) - not fatal")


def assert_no_forbidden(path: Path):
    """This register publishes no owner or contact column. Asserted rather than
    assumed, so the claim stays true if it ever gains one."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        header = f.readline().strip()
    cols = [c.strip().strip('"').lower() for c in header.split(",")]
    leaked = sorted(set(cols) & {c.lower() for c in FORBIDDEN_COLUMNS})
    if leaked:
        sys.exit(f"  business: the register now carries {leaked}, which it did "
                 f"not on 2026-09-21. This project publishes commercial, not "
                 f"personal, information - decide explicitly before building "
                 f"on a column like that.")
    print(f"  business: {len(cols)} columns, none personal (asserted)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    print("Transit (Calgary Transit's own feed, not the catalogue mirror):")
    zp = get(GTFS_URL, GTFS_ZIP, force=args.force, label="gtfs",
             min_bytes=1_000_000)
    with zipfile.ZipFile(zp) as z:
        names = z.namelist()
    print(f"  files: {', '.join(sorted(names))}")
    if "feed_info.txt" not in names:
        print("  NOTE: no feed_info.txt, so there is NO validity window to "
              "check - expected here, and the reason config."
              "GTFS_CHECK_FEED_WINDOW is False. Only Montréal's STM and "
              "Vancouver's TransLink publish one.")

    print("\nBusiness register (Socrata):")
    path = get(BUSINESS_URL, BUSINESSES_RAW_CSV, force=args.force,
               label="business", params={"$limit": str(BUSINESS_LIMIT)},
               min_bytes=1_000_000)
    assert_no_forbidden(path)
    report_freshness()

    print("\nBoundary (the `dataset` view, NOT the empty `map` view):")
    get(CITY_BOUNDARY_URL, CITY_BOUNDARY_GEOJSON, force=args.force,
        label="boundary", min_bytes=10_000)

    print("\nDone. Next: python pipeline/calgary/step1_stations.py")


if __name__ == "__main__":
    main()
