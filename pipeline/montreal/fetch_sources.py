"""Download Montréal's three raw inputs. Run this before the steps.

    python pipeline/montreal/fetch_sources.py [--force]

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline.

TWO THINGS HERE ARE UNLIKE THE OTHER CITIES.

**The portal refuses a plain client.** `donnees.montreal.ca` answers
`RBAC: access denied` unless the request carries a browser User-Agent. It is
portal-wide, not dataset-specific, and it is the reason Montréal was nearly
ruled out of the Canada screen.

**The transit feed comes from STM, not the catalogue - and this city is the
proof that matters.** Measured 2026-09-21: the agency feed was valid to
20261025 (+34 days) while the Mobility Database mirror (id 2126) was 29 days
EXPIRED. The station counts happened to agree, so the ranking was safe, but
Toronto's mirror was three months stale AND missing its entire subway. The
window is therefore re-checked on every run, including runs that skip the
download.
"""

import argparse
import csv
import io
import sys
import zipfile
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.montreal.config import (  # noqa: E402
    BUSINESS_NEEDS_BROWSER_HEADERS,
    BUSINESS_PACKAGE,
    BUSINESS_URL,
    BUSINESSES_RAW_CSV,
    CITY_BOUNDARY_GEOJSON,
    CITY_BOUNDARY_URL,
    DATA_RAW,
    FORBIDDEN_COLUMNS,
    GTFS_CHECK_FEED_WINDOW,
    GTFS_FEED_INFO_MEMBER,
    GTFS_URL,
    GTFS_ZIP,
    SOURCE_DELIMITER,
)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0 Safari/537.36"),
    "Accept": "text/csv,application/json,*/*",
}


def get(url, path: Path, *, force, label, browser=False, min_bytes=1024):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"  {label}: have {path.name} "
              f"({path.stat().st_size:,} bytes) - skipping")
        return path
    print(f"  {label}: GET {url}")
    r = requests.get(url, headers=BROWSER_HEADERS if browser else HEADERS,
                     timeout=900)
    if r.status_code != 200:
        extra = ""
        if browser is False and "RBAC" in r.text[:200]:
            extra = ("\n  This is the RBAC refusal - the request needs browser "
                     "headers (config.BUSINESS_NEEDS_BROWSER_HEADERS).")
        sys.exit(f"  {label}: HTTP {r.status_code}{extra}\n{r.text[:400]}")
    if len(r.content) < min_bytes:
        sys.exit(f"  {label}: only {len(r.content)} bytes - refusing to store "
                 f"a body this small.\n{r.text[:300]}")
    path.write_bytes(r.content)
    print(f"  {label}: wrote {path.name} ({len(r.content):,} bytes)")
    return path


def check_feed_window(zip_path: Path):
    """Refuse an expired feed. An expired one still parses, still has 68
    stations, and still builds a map - so this is an error, not a warning."""
    if not GTFS_CHECK_FEED_WINDOW:
        return
    with zipfile.ZipFile(zip_path) as z:
        if GTFS_FEED_INFO_MEMBER not in z.namelist():
            sys.exit(f"{zip_path.name}: no {GTFS_FEED_INFO_MEMBER}. STM's own "
                     f"feed publishes one; the Mobility Database mirror is the "
                     f"copy that would not. Check which host this came from.")
        text = z.read(GTFS_FEED_INFO_MEMBER).decode("utf-8-sig")
    row = next(csv.DictReader(io.StringIO(text)))
    start, end = row.get("feed_start_date"), row.get("feed_end_date")
    if not end:
        sys.exit(f"{zip_path.name}: feed_info.txt has no feed_end_date.")
    end_date = date(int(end[:4]), int(end[4:6]), int(end[6:8]))
    print(f"  GTFS validity: {start} to {end} (version "
          f"{row.get('feed_version', '?')}) - "
          f"{(end_date - date.today()).days:+d} days from today")
    if end_date < date.today():
        sys.exit(f"  GTFS feed EXPIRED on {end}. Re-run with --force. An "
                 f"expired feed still parses and still builds a map, which is "
                 f"why this stops the run.")


def check_no_personal_columns(path: Path):
    """The download boundary is this project's privacy control. This survey
    publishes no personal column at all, which is a stronger position than
    filtering one out - so the absence is asserted rather than assumed."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        header = f.readline().strip()
    cols = [c.strip().strip('"') for c in header.split(SOURCE_DELIMITER)]
    leaked = sorted(set(cols) & set(FORBIDDEN_COLUMNS))
    if leaked:
        sys.exit(f"  business: the survey now carries {leaked}, which it did "
                 f"not on 2026-09-21. This project publishes commercial, not "
                 f"personal, information - decide explicitly before building "
                 f"on a column like this rather than letting step 2 drop it.")
    print(f"  business: {len(cols)} columns, none personal (asserted)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    print("Transit (STM's own host, not the catalogue mirror):")
    get(GTFS_URL, GTFS_ZIP, force=args.force, label="gtfs",
        min_bytes=1_000_000)
    check_feed_window(GTFS_ZIP)

    print(f"\nBusiness (CKAN package {BUSINESS_PACKAGE!r}):")
    path = get(BUSINESS_URL, BUSINESSES_RAW_CSV, force=args.force,
               label="business", browser=BUSINESS_NEEDS_BROWSER_HEADERS,
               min_bytes=1_000_000)
    check_no_personal_columns(path)

    print("\nBoundary (the WGS 84 resource, not the NAD83/MTM one):")
    get(CITY_BOUNDARY_URL, CITY_BOUNDARY_GEOJSON, force=args.force,
        label="agglomeration", browser=BUSINESS_NEEDS_BROWSER_HEADERS,
        min_bytes=100_000)

    print("\nDone. Next: python pipeline/montreal/step1_stations.py")


if __name__ == "__main__":
    main()
