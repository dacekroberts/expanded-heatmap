"""Download San Francisco's Assessor property roll.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline, and step 2 must therefore
never fetch anything itself.

Scope: this fetches the Assessor roll only, which is the source added on
2026-09-21 for the home-business filter. San Francisco's three older raw
inputs (the business export, the Muni GTFS feed and the county boundary) were
downloaded before this script existed; their endpoints and download filters
are recorded in docs/data_sources.md and they are not re-fetched here, because
re-downloading a business export changes every count in DECISIONS.md and
should be a deliberate act.

    python pipeline/san_francisco/fetch_sources.py [--force]
"""

import argparse
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.san_francisco.config import (  # noqa: E402
    ASSESSOR_ROLL_CSV,
    ASSESSOR_ROLL_PARAMS,
    ASSESSOR_ROLL_URL,
    ASSESSOR_ROLL_YEAR,
    DATA_RAW,
)

TIMEOUT = 900
HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true",
                    help="re-download even if the file already exists")
    args = ap.parse_args()

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    if ASSESSOR_ROLL_CSV.exists() and not args.force:
        print(f"assessor roll: already have {ASSESSOR_ROLL_CSV.name} "
              f"({ASSESSOR_ROLL_CSV.stat().st_size:,} bytes) - skipping "
              f"(--force to refresh)")
        return

    print(f"assessor roll {ASSESSOR_ROLL_YEAR}: downloading -> "
          f"{ASSESSOR_ROLL_CSV.name}")
    with requests.get(ASSESSOR_ROLL_URL, params=ASSESSOR_ROLL_PARAMS,
                      stream=True, timeout=TIMEOUT, headers=HEADERS) as r:
        r.raise_for_status()
        written = 0
        with open(ASSESSOR_ROLL_CSV, "wb") as fh:
            for chunk in r.iter_content(1 << 20):
                fh.write(chunk)
                written += len(chunk)
    print(f"   {written:,} bytes")
    print("\nDone. Next: step2_clean_businesses.py, step3_map.py")


if __name__ == "__main__":
    main()
