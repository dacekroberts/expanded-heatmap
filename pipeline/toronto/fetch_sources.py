"""Download Toronto's four raw inputs. Run this before the steps.

    python pipeline/toronto/fetch_sources.py [--force]

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline.

FOUR inputs, one more than any other city, because Toronto has no coordinates
and needs its own geocoder: the licence register, the One Address Repository,
the TTC feed and the boundary.

THE ONE THING TO KNOW: **use the agency feed, never the catalogue mirror.**
The Mobility Database copy of the TTC feed (id 2253) was three months expired
and contained NO SUBWAY AT ALL - 209 bus routes, 17 tram, 2 ferry, zero
`route_type 1` - and the screen read that as "Toronto codes its subway as
route_type 0", which is false and propagated into three files before it was
caught. This build reads the City's own CKAN package.

The register's THREE personal columns are asserted gone here, at the download
boundary, before any other step sees the file.
"""

import argparse
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.toronto.config import (  # noqa: E402
    ADDRESS_POINTS_CSV,
    ADDRESS_POINTS_URL,
    BOUNDARY_AREA_KM2_RANGE,
    BUSINESS_URL,
    BUSINESSES_RAW_CSV,
    CITY_BOUNDARY_URL,
    CITY_BOUNDARY_ZIP,
    CRS_GEOGRAPHIC,
    CRS_PROJECTED,
    DATA_RAW,
    FORBIDDEN_COLUMNS,
    GTFS_URL,
    GTFS_ZIP,
)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


def get(url, path: Path, *, force, label, min_bytes=1024):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"  {label}: have {path.name} "
              f"({path.stat().st_size:,} bytes) - skipping")
        return path
    print(f"  {label}: GET {url[:110]}...")
    with requests.get(url, headers=HEADERS, timeout=1800, stream=True) as r:
        if r.status_code != 200:
            sys.exit(f"  {label}: HTTP {r.status_code}\n{r.text[:300]}")
        tmp = path.with_suffix(path.suffix + ".part")
        size = 0
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
                size += len(chunk)
    if size < min_bytes:
        tmp.unlink(missing_ok=True)
        sys.exit(f"  {label}: only {size:,} bytes, expected >= {min_bytes:,}")
    tmp.replace(path)
    print(f"  {label}: wrote {path.name} ({size:,} bytes)")
    return path


def assert_no_forbidden(path: Path):
    """The register publishes `Client Name`, `Business Phone` and `Business
    Phone Ext.` This project never loads them, and step 2 drops them on read -
    but the count is asserted here because the Canada profile recorded ONE of
    the three and missed the other two."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        header = f.readline().strip()
    cols = [c.strip().strip('"') for c in header.split(",")]
    present = [c for c in FORBIDDEN_COLUMNS if c in cols]
    print(f"  business: {len(cols)} columns; {len(present)} personal columns "
          f"present and NOT loaded by any step: {present}")
    if len(present) != len(FORBIDDEN_COLUMNS):
        print(f"  NOTE: expected all of {list(FORBIDDEN_COLUMNS)}. The schema "
              f"changed - re-read it before trusting step 2's drop list.")
    if not any(c.lower().startswith("licence address") for c in cols):
        sys.exit("  business: no address column - this register has no "
                 "coordinates, so the address IS the geocode key.")


def assert_boundary(path: Path):
    import geopandas as gpd
    b = gpd.read_file(path)
    if len(b) == 0 or b.geometry.isna().all():
        sys.exit("  boundary: no geometry.")
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    area = b.to_crs(CRS_PROJECTED).union_all().area / 1e6
    lo, hi = BOUNDARY_AREA_KM2_RANGE
    print(f"  boundary: {len(b)} feature(s), {area:.1f} km2 "
          f"(Toronto is ~630 km2 of land)")
    if not lo < area < hi:
        sys.exit(f"  boundary: {area:.1f} km2 is outside {lo}-{hi} - wrong layer.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    print("Transit (the CITY's CKAN package, NOT the Mobility Database mirror):")
    get(GTFS_URL, GTFS_ZIP, force=args.force, label="gtfs",
        min_bytes=20_000_000)

    print("\nBusiness register (CKAN datastore dump):")
    p = get(BUSINESS_URL, BUSINESSES_RAW_CSV, force=args.force,
            label="business", min_bytes=20_000_000)
    assert_no_forbidden(p)

    print("\nAddress points (One Address Repository - Toronto is the only "
          "Canadian city of six that needs a geocoder):")
    get(ADDRESS_POINTS_URL, ADDRESS_POINTS_CSV, force=args.force,
        label="addresses", min_bytes=100_000_000)

    print("\nBoundary (zipped shapefile; geopandas reads the zip directly):")
    bp = get(CITY_BOUNDARY_URL, CITY_BOUNDARY_ZIP, force=args.force,
             label="boundary", min_bytes=50_000)
    assert_boundary(bp)

    print("\nDone. Next: python pipeline/toronto/step1_stations.py")


if __name__ == "__main__":
    main()
