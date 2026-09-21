"""Look up SanGIS parcel land use and owner occupancy for the San Diego pins
whose displayed name reads as a person's.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline. It writes a cache that
step2_clean_businesses.py reads, so all network work happens here.

It reads `businesses_clean_prefilter.csv`, the unfiltered snapshot step 2
writes every run, never step 2's filtered output: reading the latter would
build a cache missing the rows already removed, and they would silently come
back on the next run.

Same two-query shape as Los Angeles - the containing parcel where the point
sits in one, and only otherwise every parcel within the buffer, where
requiring all of them to be residential and owner-occupied is the right
conservative test. Answering the buffered question for points that DO sit
inside a parcel made LA's filter under-remove tenfold.

This city's fields differ from LA's: `asr_landuse` is a numeric code with no
published domain (11 = single-family detached, verified empirically) and
`ownerocc` is 'Y' or null.

    python pipeline/san_diego/fetch_parcel_residence.py [--force] [--workers N]
"""

import argparse
import csv
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.residence import looks_personal  # noqa: E402
from pipeline.san_diego.config import (  # noqa: E402
    BUSINESSES_PREFILTER_CSV,
    PARCEL_BUFFER_M,
    PARCEL_RESIDENCE_CSV,
    PARCEL_RESIDENTIAL_CODES,
    PARCEL_SERVICE_URL,
)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
OUT_FIELDS = "asr_landuse,ownerocc,nucleus_use_cd,unitqty"


class Blocked(Exception):
    """The service is refusing us, as opposed to one request failing."""


def _query(session, lon, lat, distance=None, delay=0.0):
    params = {
        "f": "json",
        "geometry": f"{lon},{lat}",
        "geometryType": "esriGeometryPoint",
        "spatialRel": "esriSpatialRelIntersects",
        "inSR": "4326",
        "outFields": OUT_FIELDS,
        "returnGeometry": "false",
    }
    if distance:
        params["distance"] = str(distance)
        params["units"] = "esriSRUnit_Meter"
    if delay:
        time.sleep(delay)
    r = session.get(PARCEL_SERVICE_URL, params=params, timeout=90,
                    headers=HEADERS)
    # SANDAG sits behind an Azure Application Gateway that rate-limits bursts.
    # A first attempt at 8 concurrent workers was blocked after ~750 requests,
    # and because the caller swallowed every exception alike it reported 1,706
    # "failures" rather than "we are blocked" - and wrote a 31%-coverage cache
    # that would have produced a partial, arbitrary filter. 403 is now its own
    # signal, and main() aborts on a run of them instead of grinding through.
    if r.status_code in (403, 429):
        raise Blocked(f"HTTP {r.status_code} - rate-limited or blocked")
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}")
    return [f.get("attributes", {}) for f in r.json().get("features", [])]


def lookup(session, key, lon, lat, delay=0.0):
    try:
        feats = _query(session, lon, lat, delay=delay)
        source = "exact"
        if not feats:
            feats = _query(session, lon, lat, PARCEL_BUFFER_M, delay=delay)
            source = "buffer"
    except Blocked:
        raise
    except Exception:
        return None
    if not feats:
        return {"account_key": key, "n_parcels": 0, "source": "none",
                "all_residential": "", "all_owner_occupied": "",
                "land_uses": ""}

    def resid(a):
        try:
            return int(a.get("asr_landuse")) in PARCEL_RESIDENTIAL_CODES
        except (TypeError, ValueError):
            return False

    def occupied(a):
        return str(a.get("ownerocc") or "").strip().upper() == "Y"

    return {
        "account_key": key,
        "n_parcels": len(feats),
        "source": source,
        "all_residential": "true" if all(resid(a) for a in feats) else "false",
        "all_owner_occupied": "true" if all(occupied(a) for a in feats) else "false",
        "land_uses": "|".join(sorted({str(a.get("asr_landuse")) for a in feats})),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    # Two workers and a small delay by default: this service blocked an
    # 8-worker run. Raise it only if you have reason to think the limit moved.
    ap.add_argument("--workers", type=int, default=2,
                    help="concurrent requests (default 2 - this service "
                         "rate-limits bursts)")
    ap.add_argument("--delay", type=float, default=0.15,
                    help="seconds to pause before each request (default 0.15)")
    args = ap.parse_args()

    if PARCEL_RESIDENCE_CSV.exists() and not args.force:
        print(f"already have {PARCEL_RESIDENCE_CSV.name} "
              f"({PARCEL_RESIDENCE_CSV.stat().st_size:,} bytes) - skipping "
              f"(--force to refresh)")
        return
    if not BUSINESSES_PREFILTER_CSV.exists():
        sys.exit(f"No {BUSINESSES_PREFILTER_CSV}. Run step2_clean_businesses.py "
                 "first; it writes that unfiltered snapshot every run, and the "
                 "filter is simply skipped while this cache is absent.")

    d = pd.read_csv(BUSINESSES_PREFILTER_CSV, dtype=str, low_memory=False)
    d["lat"] = pd.to_numeric(d["latitude"], errors="coerce")
    d["lon"] = pd.to_numeric(d["longitude"], errors="coerce")
    d = d.dropna(subset=["lat", "lon"])
    cand = d[d["business_name"].map(looks_personal)]
    print(f"{len(d):,} clean rows; {len(cand):,} with a person-like name to "
          f"look up ({PARCEL_BUFFER_M:.0f} m fallback buffer, "
          f"{args.workers} workers)")

    rows = []
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(lookup, session, r.account_key, r.lon,
                                   r.lat, args.delay)
                       for r in cand.itertuples()]
            blocked = 0
            for i, fut in enumerate(futures, 1):
                try:
                    got = fut.result()
                except Blocked as e:
                    blocked += 1
                    if blocked >= 25:
                        for f in futures[i:]:
                            f.cancel()
                        sys.exit(
                            f"\nABORTED after {blocked} refusals ({e}). The "
                            f"service is rate-limiting, not failing. NOTHING "
                            f"was written: a partial cache would produce a "
                            f"filter that removes home businesses only where "
                            f"the lookup happened to succeed.\nWait for the "
                            f"block to lift and retry, or switch to a bulk "
                            f"parcel download - see PLAN.md.")
                    continue
                if got:
                    rows.append(got)
                if i % 500 == 0:
                    print(f"  ...{i:,}/{len(futures):,}", flush=True)

    failed = len(cand) - len(rows)
    PARCEL_RESIDENCE_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(PARCEL_RESIDENCE_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["account_key", "n_parcels", "source",
                                            "all_residential",
                                            "all_owner_occupied", "land_uses"])
        w.writeheader()
        w.writerows(rows)
    matched = sum(1 for r in rows if r["n_parcels"])
    by_source = {}
    for r in rows:
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1
    print(f"\nWrote {len(rows):,} rows to {PARCEL_RESIDENCE_CSV}")
    print(f"  matched a parcel: {matched:,} "
          f"({100 * matched / max(len(rows), 1):.1f}%); "
          f"request failures: {failed:,}")
    print(f"  answered by: {by_source}")


if __name__ == "__main__":
    main()
