"""Download Philadelphia's raw inputs: the L&I business licences, SEPTA's
GTFS feed and the city boundary.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline. Run it by hand when the raw
data is missing or is being refreshed, then run the steps.

Every endpoint and filter lives in config.py, so this script holds no URLs of
its own. See docs/data_sources.md.

    python pipeline/philadelphia/fetch_sources.py [--force]
"""

import argparse
import io
import sys
import zipfile
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.philadelphia.config import (  # noqa: E402
    BUSINESSES_ENDPOINT,
    BUSINESSES_FROM,
    BUSINESSES_RAW_CSV,
    BUSINESSES_SELECT,
    CITY_BOUNDARY_GEOJSON,
    CITY_BOUNDARY_PARAMS,
    CITY_BOUNDARY_URL,
    DATA_RAW,
    GTFS_INNER_ZIP,
    GTFS_URL,
    GTFS_ZIP,
    KEPT_LICENSETYPES,
)

TIMEOUT = 600
# GitHub's release CDN rejects requests with no User-Agent.
HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def get(url, dest: Path, force: bool, label: str, params=None) -> bool:
    if dest.exists() and not force:
        print(f"  {label}: already have {dest.name} "
              f"({dest.stat().st_size:,} bytes) - skipping (--force to refresh)")
        return False
    print(f"  {label}: downloading -> {dest.name}")
    with requests.get(url, params=params, stream=True, timeout=TIMEOUT,
                      headers=HEADERS) as r:
        r.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        written = 0
        with open(dest, "wb") as fh:
            for chunk in r.iter_content(1 << 20):
                fh.write(chunk)
                written += len(chunk)
    print(f"     {written:,} bytes")
    return True


def business_query() -> str:
    """The server-side filter, built from the taxonomy's kept licence types so
    the two can never drift apart. The FROM clause joins the City's property
    register for the residence check - see config.BUSINESSES_SELECT."""
    quoted = ", ".join("'" + t.replace("'", "''") + "'" for t in KEPT_LICENSETYPES)
    return (f"SELECT {BUSINESSES_SELECT} FROM {BUSINESSES_FROM} "
            f"WHERE b.licensestatus = 'Active' AND b.licensetype IN ({quoted})")


def fetch_gtfs(force: bool):
    """SEPTA ships a zip of zips; extract the inner feed the map needs so
    step 1 reads an ordinary GTFS zip (see config.GTFS_INNER_ZIP)."""
    if GTFS_ZIP.exists() and not force:
        print(f"  gtfs: already have {GTFS_ZIP.name} "
              f"({GTFS_ZIP.stat().st_size:,} bytes) - skipping (--force to refresh)")
        return
    print(f"  gtfs: downloading {GTFS_URL.rsplit('/', 1)[-1]}")
    r = requests.get(GTFS_URL, timeout=TIMEOUT, headers=HEADERS,
                     allow_redirects=True)
    r.raise_for_status()
    print(f"     {len(r.content):,} bytes; extracting {GTFS_INNER_ZIP}")
    with zipfile.ZipFile(io.BytesIO(r.content)) as outer:
        names = outer.namelist()
        if GTFS_INNER_ZIP not in names:
            sys.exit(f"{GTFS_INNER_ZIP} not in the SEPTA feed (found {names}). "
                     "SEPTA may have restructured it; see config.GTFS_INNER_ZIP.")
        inner = outer.read(GTFS_INNER_ZIP)
    GTFS_ZIP.parent.mkdir(parents=True, exist_ok=True)
    GTFS_ZIP.write_bytes(inner)
    print(f"     wrote {GTFS_ZIP.name} ({len(inner):,} bytes)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="re-download files that already exist")
    args = ap.parse_args()

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    print(f"Raw inputs -> {DATA_RAW}")

    print("\nBusiness licences (Carto SQL API, filtered server-side):")
    get(BUSINESSES_ENDPOINT, BUSINESSES_RAW_CSV, args.force, "licences",
        params={"q": business_query(), "format": "csv"})

    print("\nTransit and boundary:")
    fetch_gtfs(args.force)
    get(CITY_BOUNDARY_URL, CITY_BOUNDARY_GEOJSON, args.force, "boundary",
        params=CITY_BOUNDARY_PARAMS)

    print("\nDone. Next: step1_stations.py, step2_clean_businesses.py, "
          "step3_map.py")


if __name__ == "__main__":
    main()
