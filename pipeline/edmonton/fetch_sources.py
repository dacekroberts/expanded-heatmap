"""Download Edmonton's three raw inputs. Run this before the steps.

    python pipeline/edmonton/fetch_sources.py [--force]

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline.

THREE THINGS HERE ARE UNLIKE THE OTHER CITIES.

**The GTFS URL is not published as a link anywhere you can read.** The
catalogue's entry for the feed (`urjq-fvmq`) is an `href`-type asset, so it has
no rows and no download button in the usual place; the real URL lives in its
metadata under `accessPoints.DOWNLOAD`. Two plausible guesses 404'd during the
Canada profile, which is why the feed stayed ASSERTED until 2026-09-21.

**Edmonton publishes GTFS twice, and the more convenient copy is stale.** The
eight individual Socrata tables (Routes `d577-xky7`, Stops `4vt2-8zrq`, Trips
`ctwr-tvrd`, Stop Times `greh-g7ac`, Route Shapes `7f8n-igfx`, Calendar Dates
`f2sy-bth7`, Agency `isug-45sj`, Transfers `hnhf-yaps`) look like the better
path - no zip, and each exposes its own `updatedAt`. **They are expired.**
Measured 2026-09-21: their `calendar_dates` run 2026-06-18 to **2026-08-29**,
and the Stops table had not been written since April. The Mobility Database
mirror is worse still (`feed_end_date` 20260620). Only the agency zip is
current, and this script proves it every run by reading `feed_info.txt`.

**The boundary has FOUR same-named layers and two are the wrong polygon.**
`qqvh-dp5m` and `a62q-eaea` dissolve to 783.1 km2; `3trg-p57p` and `gtx5-kghy`
to 699.8 km2. The 83.3 km2 difference is Edmonton's 2019 annexation from Leduc
County, so the smaller pair predates it. This is Calgary's two-boundary trap
with twice the ways to get it wrong, so the area is asserted, not eyeballed.
"""

import argparse
import datetime as dt
import io
import sys
import zipfile
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.edmonton.config import (  # noqa: E402
    BOUNDARY_AREA_KM2_MIN,
    BUSINESS_LIMIT,
    BUSINESS_URL,
    BUSINESS_VIEW,
    BUSINESSES_RAW_CSV,
    CITY_BOUNDARY_GEOJSON,
    CITY_BOUNDARY_URL,
    DATA_RAW,
    FORBIDDEN_COLUMNS,
    GTFS_CHECK_FEED_WINDOW,
    GTFS_URL,
    GTFS_ZIP,
)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}


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
        sys.exit(f"  {label}: only {len(r.content)} bytes.\n{r.text[:300]}")
    path.write_bytes(r.content)
    print(f"  {label}: wrote {path.name} ({len(r.content):,} bytes)")
    return path


def check_feed_window(zip_path: Path):
    """Edmonton's feed DOES declare a validity window, and this is the check
    that the agency copy is being used rather than either stale republication.
    """
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        print(f"  files: {', '.join(sorted(names))}")
        if "feed_info.txt" not in names:
            sys.exit("  no feed_info.txt. The AGENCY feed has one (this is how "
                     "Edmonton differs from Calgary and Toronto) - if it is "
                     "missing, GTFS_URL is pointing at a republication.")
        import pandas as pd
        fi = pd.read_csv(io.BytesIO(z.read("feed_info.txt")), dtype=str)
    start = str(fi.iloc[0].get("feed_start_date", "") or "")
    end = str(fi.iloc[0].get("feed_end_date", "") or "")
    ver = str(fi.iloc[0].get("feed_version", "") or "")
    print(f"  feed_version {ver}  valid {start} to {end}")
    if end and end != "nan":
        ed = dt.date(int(end[:4]), int(end[4:6]), int(end[6:8]))
        days = (ed - dt.date.today()).days
        if days < 0:
            sys.exit(
                f"  feed EXPIRED {-days} days ago ({end}). The agency feed "
                f"should be current; an expired one here means this URL is now "
                f"serving a stale file. Do NOT fall back to the Socrata tables "
                f"or the Mobility Database mirror - both were already more "
                f"stale than this on 2026-09-21. The Valley Line is actively "
                f"extending, so a stale feed can be missing stations outright."
            )
        print(f"  current: {days} days of validity remaining")


def report_freshness():
    try:
        r = requests.get(f"https://data.edmonton.ca/api/views/{BUSINESS_VIEW}.json",
                         headers=HEADERS, timeout=120)
        if r.status_code == 200:
            d = r.json()
            for key in ("rowsUpdatedAt", "viewLastModified", "createdAt"):
                if d.get(key):
                    when = dt.datetime.fromtimestamp(d[key], dt.timezone.utc)
                    age = (dt.datetime.now(dt.timezone.utc) - when).days
                    print(f"  business register {key}: {when:%Y-%m-%d} "
                          f"({age} days ago)")
            lic = d.get("license") or {}
            if lic:
                print(f"  declared licence: {lic.get('name')} "
                      f"(= the Open Data Terms of Use; "
                      f"docs/licenses/edmonton-open-data-terms-of-use.pdf)")
    except Exception as exc:
        print(f"  freshness probe failed ({type(exc).__name__}) - not fatal")


def assert_no_forbidden(path: Path):
    """Edmonton publishes ONE name column and it is the business's. Asserted so
    the structural privacy claim stays true rather than merely recorded."""
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        header = f.readline().strip()
    cols = [c.strip().strip('"').lower() for c in header.split(",")]
    leaked = sorted(set(cols) & {c.lower() for c in FORBIDDEN_COLUMNS})
    if leaked:
        sys.exit(f"  business: the register now carries {leaked}, which it did "
                 f"not on 2026-09-21. Edmonton's privacy position is that no "
                 f"pin CAN be a person's name because there is no name to fall "
                 f"back to - a column like that ends it. Decide explicitly "
                 f"before building on this file.")
    print(f"  business: {len(cols)} columns, one name column and it is the "
          f"business's (asserted)")


def assert_boundary_is_current(path: Path):
    import geopandas as gpd
    from pipeline.edmonton.config import CRS_GEOGRAPHIC, CRS_PROJECTED
    b = gpd.read_file(path)
    if len(b) == 0 or b.geometry.isna().all():
        sys.exit("  boundary has no geometry.")
    b = b.set_crs(CRS_GEOGRAPHIC) if b.crs is None else b.to_crs(CRS_GEOGRAPHIC)
    area = b.to_crs(CRS_PROJECTED).union_all().area / 1e6
    print(f"  boundary: {len(b)} feature(s), {area:.1f} km2")
    if area < BOUNDARY_AREA_KM2_MIN:
        sys.exit(f"  {area:.1f} km2 is the PRE-2019 boundary (699.8 km2), not "
                 f"the current one (783.1). Four layers on this portal are "
                 f"named 'Corporate Boundary'; use qqvh-dp5m.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    DATA_RAW.mkdir(parents=True, exist_ok=True)

    print("Transit (ETS's own feed - NOT the Socrata tables, NOT the mirror):")
    zp = get(GTFS_URL, GTFS_ZIP, force=args.force, label="gtfs",
             min_bytes=1_000_000)
    if GTFS_CHECK_FEED_WINDOW:
        check_feed_window(zp)

    print("\nBusiness register (Socrata):")
    path = get(BUSINESS_URL, BUSINESSES_RAW_CSV, force=args.force,
               label="business", params={"$limit": str(BUSINESS_LIMIT)},
               min_bytes=1_000_000)
    assert_no_forbidden(path)
    report_freshness()

    print("\nBoundary (qqvh-dp5m, the CURRENT corporate boundary of four):")
    bp = get(CITY_BOUNDARY_URL, CITY_BOUNDARY_GEOJSON, force=args.force,
             label="boundary", min_bytes=10_000)
    assert_boundary_is_current(bp)

    print("\nDone. Next: python pipeline/edmonton/step1_stations.py")


if __name__ == "__main__":
    main()
