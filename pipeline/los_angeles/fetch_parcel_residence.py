"""Look up the Assessor's land use and homeowner's-exemption status for the
Los Angeles pins whose displayed name reads as a person's.

Deliberately NOT named step*.py, so pipeline/drift_check.py never re-runs it -
a drift check must be deterministic and offline. It writes a cache that
step3_geocode.py reads to apply the home-business filter, so the network work
happens here and the pipeline stays offline.

Two-phase by necessity: the filter needs FINAL coordinates (9% of LA's are
recovered by Census geocoding), which only exist after step 3. So the order is
step3 -> this script -> step3 again. It reads
`businesses_geocoded_prefilter.csv`, the unfiltered snapshot step 3 writes
every run, never the filtered output - reading the latter would build a cache
missing the rows already removed, and they would come back silently.
Coordinates are deterministic, so the cache stays valid afterwards.

Only person-like names are queried - about a quarter of the rows - because the
filter cannot fire on anything else, and the county service is a shared public
resource. Rows absent from the cache are simply not flagged.

Two queries per point, exact then buffered, and the order is load-bearing. An
exact point-in-parcel test asks the precise question but matches only ~49% of
these pins, because Census-geocoded coordinates land on street centrelines
rather than inside a parcel. A 25 m buffer matches ~100%, but it is a
DIFFERENT question: it returns several parcels, and requiring all of them to be
owner-occupied means one rental next door clears a genuine home. Answering the
buffered question instead of the exact one made the filter under-remove
tenfold (95 rows where the exact test implied ~1,000).

So: use the containing parcel where there is one; fall back to the buffer only
for points inside no parcel at all, where requiring every nearby parcel to be
residential and owner-occupied IS the right conservative test. `source`
records which answered.

    python pipeline/los_angeles/fetch_parcel_residence.py [--force] [--workers N]
"""

import argparse
import csv
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline.los_angeles.config import (  # noqa: E402
    BUSINESSES_PREFILTER_CSV,
    PARCEL_BUFFER_M,
    PARCEL_RESIDENCE_CSV,
    PARCEL_SERVICE_URL,
)
from pipeline.residence import looks_personal  # noqa: E402

HEADERS = {"User-Agent": "expanded-heatmap (github.com/dacekroberts/expanded-heatmap)"}
OUT_FIELDS = "UseType,UseDescription,Roll_HomeOwnersExemp"


def _query(session, lon, lat, distance=None):
    data = {
        "f": "json",
        "geometry": f"{lon},{lat}",
        "geometryType": "esriGeometryPoint",
        "spatialRel": "esriSpatialRelIntersects",
        "inSR": "4326",
        "outFields": OUT_FIELDS,
        "returnGeometry": "false",
    }
    if distance:
        data["distance"] = str(distance)
        data["units"] = "esriSRUnit_Meter"
    r = session.post(PARCEL_SERVICE_URL, data=data, timeout=90, headers=HEADERS)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}")
    return [f.get("attributes", {}) for f in r.json().get("features", [])]


def lookup(session, key, lon, lat):
    """The parcel this point sits in, or - only when it sits in none - the
    parcels within the buffer, reduced to flags.

    The order matters and getting it wrong changed the answer tenfold. An
    exact point-in-parcel query is the precise question, but it misses ~51% of
    LA's pins because Census-geocoded coordinates land on street centrelines.
    Answering the buffered question INSTEAD is not the same question: with a
    25 m buffer typically catching several parcels, requiring all of them to be
    owner-occupied means one rental next door clears a genuine home, and the
    filter under-removed by 10x. So: exact first, buffer only as a fallback.
    `source` records which answered, so the distinction stays visible in the
    cache rather than being lost.
    """
    try:
        feats = _query(session, lon, lat)
        source = "exact"
        if not feats:
            feats = _query(session, lon, lat, PARCEL_BUFFER_M)
            source = "buffer"
    except Exception:
        return None
    if not feats:
        return {"location_account": key, "n_parcels": 0, "source": "none",
                "all_residential": "", "all_owner_occupied": "",
                "use_types": ""}

    def resid(a):
        return str(a.get("UseType") or "").strip().lower() == "residential"

    def occupied(a):
        try:
            return float(a.get("Roll_HomeOwnersExemp") or 0) > 0
        except (TypeError, ValueError):
            return False

    return {
        "location_account": key,
        "n_parcels": len(feats),
        "source": source,
        "all_residential": "true" if all(resid(a) for a in feats) else "false",
        "all_owner_occupied": "true" if all(occupied(a) for a in feats) else "false",
        "use_types": "|".join(sorted({str(a.get("UseType") or "?")
                                      for a in feats})),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", type=int, default=8,
                    help="concurrent requests (default 8; be polite)")
    args = ap.parse_args()

    if PARCEL_RESIDENCE_CSV.exists() and not args.force:
        print(f"already have {PARCEL_RESIDENCE_CSV.name} "
              f"({PARCEL_RESIDENCE_CSV.stat().st_size:,} bytes) - skipping "
              f"(--force to refresh)")
        return
    if not BUSINESSES_PREFILTER_CSV.exists():
        sys.exit(f"No {BUSINESSES_PREFILTER_CSV}. Run step3_geocode.py first; "
                 "it writes that unfiltered snapshot every run, and the filter "
                 "is simply skipped while this cache is absent.")

    # The PRE-FILTER snapshot on purpose: reading step 3's filtered output
    # would build a cache missing the rows it already removed, and they would
    # silently return on the next run.
    d = pd.read_csv(BUSINESSES_PREFILTER_CSV, dtype=str, low_memory=False)
    d["lat"] = pd.to_numeric(d["latitude"], errors="coerce")
    d["lon"] = pd.to_numeric(d["longitude"], errors="coerce")
    d = d.dropna(subset=["lat", "lon"])
    cand = d[d["business_name"].map(looks_personal)]
    print(f"{len(d):,} geocoded rows; {len(cand):,} with a person-like name "
          f"to look up ({PARCEL_BUFFER_M:.0f} m buffer, {args.workers} workers)")

    rows = []
    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(lookup, session, r.location_account,
                                   r.lon, r.lat)
                       for r in cand.itertuples()]
            for i, fut in enumerate(futures, 1):
                got = fut.result()
                if got:
                    rows.append(got)
                if i % 1000 == 0:
                    print(f"  ...{i:,}/{len(futures):,}", flush=True)

    failed = len(cand) - len(rows)
    PARCEL_RESIDENCE_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(PARCEL_RESIDENCE_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["location_account", "n_parcels",
                                            "source", "all_residential",
                                            "all_owner_occupied", "use_types"])
        w.writeheader()
        w.writerows(rows)
    matched = sum(1 for r in rows if r["n_parcels"])
    by_source = {}
    for r in rows:
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1
    print(f"\nWrote {len(rows):,} rows to {PARCEL_RESIDENCE_CSV}")
    print(f"  matched a parcel: {matched:,} ({100 * matched / max(len(rows), 1):.1f}%)"
          f"; request failures: {failed:,}")
    print(f"  answered by: {by_source}   (exact = the containing parcel; "
          f"buffer = every parcel within {PARCEL_BUFFER_M:.0f} m, unanimity "
          f"required)")
    if failed:
        print("  re-run with --force to retry the failures before filtering")


if __name__ == "__main__":
    main()
