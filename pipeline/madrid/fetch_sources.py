"""Download Madrid's raw inputs: two CRTM layers, the boundary, the census.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline, and a step must therefore
never fetch anything itself. This city was one of three exceptions to that
invariant: fetching lived in step1 and step2 behind a cache check, which is
offline only when the gitignored raw directory happens to be populated. Moved
out 2026-09-22 with the outputs unchanged.

TWO CHECKS TRAVEL WITH THE DOWNLOADS RATHER THAN BEING LEFT BEHIND, because
each guards the fetch itself rather than the parsing:

  * `exceededTransferLimit` on the ArcGIS layers. A server-side page cap that
    silently truncates is the same shape of failure as a stale mirror, and
    `resultRecordCount` is deliberately set above the known row count so the
    flag is meaningful.
  * The CKAN resource id is resolved to a URL at download time. The URL rots;
    the id does not, which is why the id is what config.py records.

    python pipeline/madrid/fetch_sources.py            # skips what exists
    python pipeline/madrid/fetch_sources.py --force    # re-download
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.madrid.config import (
    BUSINESSES_CKAN_API,
    BUSINESSES_CKAN_PACKAGE,
    BUSINESSES_CKAN_RESOURCE,
    BUSINESSES_RAW_CSV,
    CITY_BOUNDARY_URL,
    CITY_BOUNDARY_ZIP,
    CRTM_METRO_SERVICE,
    CRTM_STATIONS_LAYER,
    CRTM_TRAMOS_LAYER,
    STATIONS_RAW_JSON,
    TRAMOS_RAW_JSON,
)

UA = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def fetch_layer(layer, cache, force):
    """One ArcGIS layer, cached to the gitignored raw directory."""
    if cache.exists() and not force:
        print(f"  cached {cache.name}")
        return
    url = (f"{CRTM_METRO_SERVICE}/{layer}/query?where=1%3D1&outFields=*"
           f"&returnGeometry=true&outSR=25830&f=json&resultRecordCount=5000")
    print(f"  fetching layer {layer} ...")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                timeout=300) as r:
        payload = json.loads(r.read())
    if payload.get("exceededTransferLimit"):
        raise SystemExit(f"layer {layer}: the server paged the response - "
                         "raise resultRecordCount or page it, do not trust this")
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(payload), encoding="utf-8")
    n = len(payload.get("features", []))
    print(f"  {cache.name}: {n:,} features")


def fetch_boundary(force):
    if CITY_BOUNDARY_ZIP.exists() and not force:
        print(f"  cached {CITY_BOUNDARY_ZIP.name}")
        return
    print("  downloading the término municipal ...")
    CITY_BOUNDARY_ZIP.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(
            urllib.request.Request(CITY_BOUNDARY_URL, headers=UA),
            timeout=300) as r:
        CITY_BOUNDARY_ZIP.write_bytes(r.read())
    print(f"  wrote {CITY_BOUNDARY_ZIP.stat().st_size:,} bytes")


def resolve_download_url():
    """The census resource's current URL, from its stable CKAN id."""
    url = f"{BUSINESSES_CKAN_API}?id={BUSINESSES_CKAN_PACKAGE}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                timeout=180) as r:
        pkg = json.loads(r.read())["result"]
    for res in pkg["resources"]:
        if res["id"] == BUSINESSES_CKAN_RESOURCE:
            return res["url"]
    raise SystemExit(f"resource {BUSINESSES_CKAN_RESOURCE} not in the package")


def fetch_census(force):
    if BUSINESSES_RAW_CSV.exists() and not force:
        print(f"  cached {BUSINESSES_RAW_CSV.name}")
        return
    url = resolve_download_url()
    print(f"  resolved {BUSINESSES_CKAN_RESOURCE} -> {url}")
    BUSINESSES_RAW_CSV.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA),
                                timeout=1800) as r:
        BUSINESSES_RAW_CSV.write_bytes(r.read())
    print(f"  downloaded {BUSINESSES_RAW_CSV.stat().st_size:,} bytes")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    print("=== Madrid: fetch raw sources ===\n")
    print("CRTM feature layers:")
    fetch_layer(CRTM_STATIONS_LAYER, STATIONS_RAW_JSON, args.force)
    fetch_layer(CRTM_TRAMOS_LAYER, TRAMOS_RAW_JSON, args.force)

    print("\nBoundary:")
    fetch_boundary(args.force)

    print("\nAyuntamiento de Madrid, Censo de locales:")
    fetch_census(args.force)

    print("\nDone. The steps read these and never fetch.")


if __name__ == "__main__":
    main()
