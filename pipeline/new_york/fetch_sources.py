"""Download New York's raw inputs: four business registries, the GTFS feed and
the borough boundaries.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline. Run it by hand when the raw
data is missing or is being refreshed, then run the steps.

Every endpoint and server-side filter lives in config.SOURCES, so this script
holds no URLs of its own. See docs/data_sources.md.

    python pipeline/new_york/fetch_sources.py [--force]
"""

import argparse
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.new_york.config import (  # noqa: E402
    CITY_BOUNDARY_GEOJSON,
    CITY_BOUNDARY_URL,
    DATA_RAW,
    GTFS_URL,
    GTFS_ZIP,
    SOURCES,
)

TIMEOUT = 600


def get(url, dest: Path, force: bool, label: str, params=None):
    if dest.exists() and not force:
        print(f"  {label}: already have {dest.name} "
              f"({dest.stat().st_size:,} bytes) - skipping (--force to refresh)")
        return
    print(f"  {label}: downloading -> {dest.name}")
    with requests.get(url, params=params, stream=True, timeout=TIMEOUT) as r:
        r.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        written = 0
        with open(dest, "wb") as fh:
            for chunk in r.iter_content(1 << 20):
                fh.write(chunk)
                written += len(chunk)
    print(f"     {written:,} bytes")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="re-download files that already exist")
    args = ap.parse_args()

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    print(f"Raw inputs -> {DATA_RAW}")

    print("\nBusiness registries:")
    for source, spec in SOURCES.items():
        # The filter string is a ready-made SoQL query; pass it through as-is
        # rather than re-encoding it, so what downloads is exactly what
        # config.py documents.
        url = f"{spec['endpoint']}?{spec['filter']}"
        get(url, spec["file"], args.force, source)

    print("\nTransit and boundary:")
    get(GTFS_URL, GTFS_ZIP, args.force, "gtfs")
    get(CITY_BOUNDARY_URL, CITY_BOUNDARY_GEOJSON, args.force, "boundary")

    print("\nDone. Next: step1_stations.py, step2_clean_businesses.py, "
          "step3_geocode.py, step4_map.py")


if __name__ == "__main__":
    main()
