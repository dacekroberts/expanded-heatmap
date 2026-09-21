"""Find the NEAREST SanGIS parcel to each San Diego pin whose displayed name
reads as a person's, and record that parcel's land use and owner occupancy.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline.

WHY NEAREST, AND WHY NOT THE OTHER TWO APPROACHES TRIED FIRST
-------------------------------------------------------------
San Diego's business coordinates sit 5-15 m OUTSIDE their own parcel: they are
placed at the street frontage and SanGIS parcels exclude road right-of-way. On
30 sampled pins an exact point-in-parcel test matched 1; a 25 m buffer matched
30. So "which parcel contains this point?" has almost no answers here, and the
question to ask is "which parcel is nearest?".

1. Point-in-parcel with a buffered fallback (first attempt) asked the WRONG
   QUESTION. A buffer returns several parcels, and requiring all of them to be
   residential and owner-occupied clears any home with a rental next door. It
   found 42 rows against San Francisco's 217 and Los Angeles' 1,252 - a floor,
   not a measurement. It also used two requests per point and got us HTTP 403
   from SANDAG's Azure Application Gateway.
2. Bulk-downloading every parcel centroid in the city (second attempt) had the
   right semantics but was unusable in practice: `orderByFields` forces a sort
   over 664,662 rows and `resultOffset` deep-pages through it, costing ~26 s
   per 2,000-row page - about two hours.
3. THIS: one buffered query per point, asking for CENTROIDS
   (`returnCentroid=true`, which this layer supports), then picking the nearest
   centroid locally. True nearest semantics, 2,463 requests rather than ~5,000,
   and no deep paging. Politer than attempt 1 and faster than attempt 2.

SANDAG's gateway rate-limits sustained querying, so this runs slowly on
purpose - see the --workers/--delay defaults. Being refused costs nothing but
time: the abort writes no file at all, because a partial cache would filter
only where the lookup happened to succeed.

Only person-like names are queried - the filter cannot fire on anything else,
and this is a shared public service. Rows absent from the cache are not
flagged.

    python pipeline/san_diego/fetch_parcels.py [--force] [--workers N]
"""

import argparse
import csv
import math
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
    PARCEL_SERVICE_URL,
    PARCEL_TOLERANCE_M,
    PARCELS_CENTROIDS_CSV,
)

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
OUT_FIELDS = "apn,asr_landuse,ownerocc"


class Blocked(Exception):
    """The service is refusing us, as opposed to one request failing."""


def _metres(lon1, lat1, lon2, lat2):
    """Good enough for ranking candidates a few tens of metres apart."""
    mean_lat = math.radians((lat1 + lat2) / 2)
    dx = (lon2 - lon1) * 111_320 * math.cos(mean_lat)
    dy = (lat2 - lat1) * 110_540
    return math.hypot(dx, dy)


def nearest_parcel(session, key, lon, lat, delay):
    """The nearest parcel centroid within the tolerance, as a cache row."""
    if delay:
        time.sleep(delay)
    try:
        r = session.get(PARCEL_SERVICE_URL, params={
            "where": "1=1",
            "geometry": f"{lon},{lat}",
            "geometryType": "esriGeometryPoint",
            "spatialRel": "esriSpatialRelIntersects",
            "inSR": "4326",
            "outSR": "4326",
            "distance": str(PARCEL_TOLERANCE_M),
            "units": "esriSRUnit_Meter",
            "outFields": OUT_FIELDS,
            "returnGeometry": "false",
            "returnCentroid": "true",
            "f": "json",
        }, timeout=90, headers=HEADERS)
        if r.status_code in (403, 429):
            raise Blocked(f"HTTP {r.status_code}")
        if r.status_code != 200:
            return None
        feats = r.json().get("features", [])
    except Blocked:
        raise
    except Exception:
        return None

    best, best_d = None, None
    for f in feats:
        c = f.get("centroid") or {}
        if c.get("x") is None or c.get("y") is None:
            continue
        d = _metres(lon, lat, c["x"], c["y"])
        if best_d is None or d < best_d:
            best, best_d = f.get("attributes", {}), d
    if best is None:
        return {"account_key": key, "apn": "", "asr_landuse": "",
                "ownerocc": "", "dist_m": "", "n_candidates": len(feats)}
    return {
        "account_key": key,
        "apn": best.get("apn") or "",
        "asr_landuse": best.get("asr_landuse") if best.get("asr_landuse") is not None else "",
        "ownerocc": best.get("ownerocc") or "",
        "dist_m": round(best_d, 1),
        "n_candidates": len(feats),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    # Defaults chosen from observed behaviour, not guessed. SANDAG's gateway
    # sustains roughly 2 requests/second for a run of this length: an ~7 req/s
    # run (2 workers, 0.15 s) completed 2,463 lookups once, but a slightly
    # faster one (2 workers, 0.1 s) was refused after ~500. One worker with a
    # 0.4 s delay is ~2 req/s and takes about 20 minutes. Raise it only if you
    # are prepared to be blocked - and note the whole point of the abort below
    # is that being blocked costs nothing except time.
    ap.add_argument("--workers", type=int, default=1,
                    help="concurrent requests (default 1 - this service "
                         "rate-limits sustained querying)")
    ap.add_argument("--delay", type=float, default=0.4,
                    help="seconds before each request (default 0.4)")
    args = ap.parse_args()

    if PARCELS_CENTROIDS_CSV.exists() and not args.force:
        print(f"already have {PARCELS_CENTROIDS_CSV.name} "
              f"({PARCELS_CENTROIDS_CSV.stat().st_size:,} bytes) - skipping "
              f"(--force to refresh)")
        return
    if not BUSINESSES_PREFILTER_CSV.exists():
        sys.exit(f"No {BUSINESSES_PREFILTER_CSV}. Run step2_clean_businesses.py "
                 "first; it writes that unfiltered snapshot every run and skips "
                 "the filter while this cache is absent.")

    # The PREFILTER snapshot, never step 2's filtered output. Reading the
    # filtered file omits the rows the filter already removed, and a row with
    # no cache entry is not flagged - so they would quietly return on the next
    # run. Same trap as Los Angeles, and worth stating twice.
    d = pd.read_csv(BUSINESSES_PREFILTER_CSV, dtype=str, low_memory=False)
    d["lat"] = pd.to_numeric(d["latitude"], errors="coerce")
    d["lon"] = pd.to_numeric(d["longitude"], errors="coerce")
    d = d.dropna(subset=["lat", "lon"])
    cand = d[d["business_name"].map(looks_personal)]
    print(f"{len(d):,} clean rows; {len(cand):,} with a person-like name; "
          f"nearest parcel within {PARCEL_TOLERANCE_M:.0f} m "
          f"({args.workers} workers)")

    rows, blocked = [], 0
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(nearest_parcel, session, r.account_key,
                                   r.lon, r.lat, args.delay)
                       for r in cand.itertuples()]
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
                            f"was written - a partial cache would filter only "
                            f"where the lookup happened to succeed.")
                    continue
                if got:
                    rows.append(got)
                if i % 500 == 0:
                    print(f"  ...{i:,}/{len(futures):,}", flush=True)

    failed = len(cand) - len(rows)
    matched = sum(1 for r in rows if r["asr_landuse"] != "")
    dists = [r["dist_m"] for r in rows if r["dist_m"] != ""]
    PARCELS_CENTROIDS_CSV.parent.mkdir(parents=True, exist_ok=True)
    tmp = PARCELS_CENTROIDS_CSV.with_suffix(".partial")
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["account_key", "apn", "asr_landuse",
                                            "ownerocc", "dist_m",
                                            "n_candidates"])
        w.writeheader()
        w.writerows(rows)
    tmp.replace(PARCELS_CENTROIDS_CSV)
    print(f"\nWrote {len(rows):,} rows to {PARCELS_CENTROIDS_CSV}")
    print(f"  nearest parcel found: {matched:,} "
          f"({100 * matched / max(len(rows), 1):.1f}%); failures: {failed:,}")
    if dists:
        dists.sort()
        print(f"  distance to nearest parcel: median "
              f"{dists[len(dists) // 2]:.1f} m, max {dists[-1]:.1f} m")


if __name__ == "__main__":
    main()
