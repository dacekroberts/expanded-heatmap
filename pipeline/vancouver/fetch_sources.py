"""Download Vancouver's and Surrey's raw inputs. Run this before the steps.

    python pipeline/vancouver/fetch_sources.py [--force]

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline.

FOUR THINGS HERE ARE UNLIKE THE OTHER CITIES.

**Two publishers, two licences.** This is a regional build (Vancouver AND
Surrey) across two municipal registries, so every download is attributed to the
source that requires its own notice. See docs/data_sources.md.

**The transit feed expires, and the mirror lied about it.** The Canada profile
recorded that TransLink's feed carries no `feed_info.txt`. The Mobility
Database mirror does not; the agency's own feed does, declaring a 118-day
window. So the window is checked on EVERY run, including runs that skip the
download - an expired feed still parses, still has 54 stations, and still
builds a map. Toronto's stale-mirror lesson, one step further on: a mirror can
be missing a file the source publishes, not merely out of date.

**Opendatasoft CSV exports are SEMICOLON-delimited** and the API's `where` and
`select` are applied server-side, which is where this build's column omissions
happen.

**Surrey's export returns `application/octet-stream`, not `text/csv`.** A
content-type check for "csv" rejects a perfectly good 4.4 MB download - which
it did, twelve times, during Step 0.
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

from pipeline.vancouver.config import (  # noqa: E402
    CITY_BOUNDARY_GEOJSON,
    CITY_BOUNDARY_URL,
    DATA_RAW,
    FORBIDDEN_COLUMNS,
    GTFS_CHECK_FEED_WINDOW,
    GTFS_FEED_INFO_MEMBER,
    GTFS_URL,
    GTFS_ZIP,
    MUNICIPALITIES_BBOX,
    MUNICIPALITIES_GEOJSON,
    MUNICIPALITIES_TYPENAME,
    MUNICIPALITIES_URL,
    PARCELS_GEOJSON,
    PARCELS_URL,
    SOURCES,
    SURREY_BOUNDARY_GEOJSON,
    SURREY_BOUNDARY_URL,
    TAX_REPORT_CSV,
    TAX_REPORT_SELECT,
    TAX_REPORT_URL,
    TAX_REPORT_YEAR,
)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def get(url, path, *, params=None, force, label, min_bytes=1024):
    """Download to `path` unless it is already there and --force was not given."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"  {label}: have {path.name} "
              f"({path.stat().st_size:,} bytes) - skipping")
        return path
    print(f"  {label}: GET {url}")
    r = requests.get(url, params=params, headers=HEADERS, timeout=600)
    if r.status_code != 200:
        sys.exit(f"  {label}: HTTP {r.status_code}\n{r.text[:500]}")
    if len(r.content) < min_bytes:
        sys.exit(f"  {label}: only {len(r.content)} bytes - refusing to store "
                 f"a body this small.\n{r.text[:500]}")
    path.write_bytes(r.content)
    print(f"  {label}: wrote {path.name} ({len(r.content):,} bytes)")
    return path


def check_feed_window(zip_path: Path):
    """Read feed_info.txt out of the stored zip and refuse an expired feed."""
    if not GTFS_CHECK_FEED_WINDOW:
        return
    with zipfile.ZipFile(zip_path) as z:
        if GTFS_FEED_INFO_MEMBER not in z.namelist():
            sys.exit(
                f"{zip_path.name}: no {GTFS_FEED_INFO_MEMBER}. The Mobility "
                f"Database MIRROR of this feed has no such file, which is what "
                f"the Canada profile recorded - but TransLink's own host "
                f"publishes one. If this is the agency feed and the file is "
                f"really gone, rethink this check rather than deleting it."
            )
        text = z.read(GTFS_FEED_INFO_MEMBER).decode("utf-8-sig")
    row = next(csv.DictReader(io.StringIO(text)))
    start, end = row.get("feed_start_date"), row.get("feed_end_date")
    version = row.get("feed_version", "?")
    if not end:
        sys.exit(f"{zip_path.name}: feed_info.txt has no feed_end_date.")
    end_date = date(int(end[:4]), int(end[4:6]), int(end[6:8]))
    today = date.today()
    print(f"  GTFS validity: {start} to {end} (version {version}) - "
          f"{(end_date - today).days:+d} days from today")
    if end_date < today:
        sys.exit(
            f"  GTFS feed EXPIRED on {end}. An expired feed still parses and "
            f"still builds a map, so this is an error, not a warning. "
            f"Re-run with --force to fetch the current feed."
        )


def fetch_business(key, force):
    src = SOURCES[key]
    params = None
    if src["endpoint"].endswith("/exports/csv"):
        # Opendatasoft: server-side filter and column selection. `geom` is
        # omitted here, not dropped later.
        params = {"select": src["select"], "where": src["filter"],
                  "delimiter": src["delimiter"], "with_bom": "false"}
    elif "hub.arcgis.com" in src["endpoint"]:
        params = {"layers": "0"}
    path = get(src["endpoint"], src["file"], params=params, force=force,
               label=f"business/{key}", min_bytes=100_000)

    # The download boundary is the privacy control, so prove it held.
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        header = f.readline().strip()
    cols = [c.strip().strip('"') for c in header.split(src["delimiter"])]
    leaked = sorted(set(cols) & set(FORBIDDEN_COLUMNS))
    if leaked:
        print(f"  business/{key}: NOTE - the server returned {leaked}, which "
              f"this project does not use. Step 2 drops it and asserts it is "
              f"gone; it is never written to a processed file or an output.")
    print(f"  business/{key}: {len(cols)} columns")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="re-download even if the file is already present")
    args = ap.parse_args()
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    print("Transit (TransLink, one feed for both cities):")
    get(GTFS_URL, GTFS_ZIP, force=args.force, label="gtfs",
        min_bytes=1_000_000)
    # Checked on EVERY run, including runs that skipped the download above.
    check_feed_window(GTFS_ZIP)

    print("\nBusiness registries:")
    for key in SOURCES:
        fetch_business(key, args.force)

    print("\nBoundaries:")
    get(CITY_BOUNDARY_URL, CITY_BOUNDARY_GEOJSON, force=args.force,
        label="vancouver boundary")
    get(SURREY_BOUNDARY_URL, SURREY_BOUNDARY_GEOJSON,
        params={"where": "1=1", "outFields": "*", "f": "geojson"},
        force=args.force, label="surrey boundary")
    get(MUNICIPALITIES_URL, MUNICIPALITIES_GEOJSON, params={
        "service": "WFS", "version": "2.0.0", "request": "GetFeature",
        "typeName": MUNICIPALITIES_TYPENAME,
        "outputFormat": "application/json", "srsName": "EPSG:4326",
        "count": "500", "bbox": MUNICIPALITIES_BBOX,
    }, force=args.force, label="bc municipalities")

    print("\nResidence filter (Vancouver only - Surrey states it on the licence):")
    get(PARCELS_URL, PARCELS_GEOJSON, force=args.force, label="parcels",
        min_bytes=1_000_000)
    get(TAX_REPORT_URL, TAX_REPORT_CSV, params={
        "select": TAX_REPORT_SELECT,
        "where": f"report_year='{TAX_REPORT_YEAR}'",
        "delimiter": ";", "with_bom": "false",
    }, force=args.force, label="tax report", min_bytes=1_000_000)

    print("\nDone. Next: python pipeline/vancouver/step1_stations.py")


if __name__ == "__main__":
    main()
