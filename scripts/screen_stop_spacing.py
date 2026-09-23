"""Measure tram / light-rail stop density for a city, against two CONTROLS.

WHY THIS EXISTS
---------------
Milan excluded its trams because "stops sit one or two blocks apart: San
Francisco's Muni Metro shape, which needs docs/sub_transit_line_filters.md
rather than a line list". San Diego's Trolley is also route_type 0 and needed
no such file. So the question "does this city's tram network need sub-line
filtering?" is a real, recurring one - and it is asked of every tram-only
candidate (Zurich, Goteborg, Stockholm so far).

READ THIS BEFORE TRUSTING ITS OUTPUT
------------------------------------
**As of 2026-09-23 this script's CONTROLS DO NOT SEPARATE.** San Francisco
(which needed the filters) measured 89 m and San Diego (which needed none)
measured 98 m - nine metres apart. A metric that gives the same answer to
both cannot be measuring what distinguishes them.

What it appears to measure instead is NETWORK CONVERGENCE: both cities' lines
bunch downtown, so nearest-neighbour picks up CROSS-LINE proximity rather
than along-line spacing. That is the same shape as Oslo's
`organisasjonsform` - a field that is fully populated and answers a different
question than the one asked of it.

**So: run it, read the controls FIRST, and do not record a verdict unless the
controls separate.** The controls are not decoration; they are the thing that
tells you whether the run means anything. If you improve the metric, the test
of the improvement is whether SF and San Diego pull apart.

A BETTER METRIC WOULD MEASURE ALONG-LINE SPACING
------------------------------------------------
i.e. consecutive stops within one route relation, which needs each relation's
ordered stop members. That was tried (v2) and abandoned for a reason worth
keeping - see the efficiency note below.

OVERPASS EFFICIENCY - THE RULE THIS SCRIPT ENCODES
--------------------------------------------------
**ONE query per CITY. Never one per route, and never one per station.**

Three versions of this test were written on 2026-09-23:

  v1  used `map_to_area` on a boundary relation. An unindexed relation yields
      an EMPTY area, which then matches nothing - San Francisco returned
      0 route relations and the failure was SILENT. A bbox needs no index.

  v2  fixed that (SF returned 22 relations) but then made ONE ROUND TRIP PER
      ROUTE. Against a load-shedding Overpass that ground for 12 minutes on a
      single city; its worst case was 22 routes x 2 mirrors x 2 retries x a
      300 s timeout.

  v3  one query per city. Five cities, ~5 minutes, done.

The same bottleneck caused a 504 on Bucharest's brief-check and a 10-minute
Seoul probe the same day. **Per-item round trips against a rate-limited
public API is the recurring cost in this project's OSM work.**

Usage:
    python scripts/screen_stop_spacing.py                # controls + all
    python scripts/screen_stop_spacing.py zurich         # controls + one
"""
import json
import math
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from statistics import median

MIRRORS = ["https://overpass-api.de/api/interpreter",
           "https://overpass.kumi.systems/api/interpreter"]
HDR = {"User-Agent": "expanded-heatmap-screening/1.0",
       "Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*"}

# south, west, north, east - a BBOX, deliberately, not an area relation.
CITIES = {
    "san_francisco": ("SAN FRANCISCO  [CONTROL: needed the filters]",
                      (37.70, -122.52, 37.84, -122.35), "tram|light_rail"),
    "san_diego": ("SAN DIEGO      [CONTROL: needed NONE]",
                  (32.53, -117.20, 32.90, -116.90), "tram|light_rail"),
    "zurich": ("ZURICH", (47.32, 8.44, 47.44, 8.63), "tram"),
    "goteborg": ("GOTEBORG", (57.60, 11.80, 57.80, 12.12), "tram|light_rail"),
    "stockholm": ("STOCKHOLM", (59.24, 17.88, 59.42, 18.22),
                  "tram|light_rail"),
}
CONTROLS = ("san_francisco", "san_diego")

# Two stop nodes closer than this are the opposite-direction platforms of ONE
# stop, not two stops.
SAME_STOP_M = 40
FAR_M = 3000


def ask(query):
    payload = urllib.parse.urlencode({"data": query}).encode("utf-8")
    for mirror in MIRRORS:
        for _ in range(2):
            req = urllib.request.Request(mirror, data=payload, headers=HDR)
            try:
                with urllib.request.urlopen(req, timeout=240) as r:
                    return r.status, r.read()
            except urllib.error.HTTPError as e:
                if e.code in (429, 504):
                    time.sleep(20)
                    continue
                return e.code, e.read()[:200]
            except Exception:
                time.sleep(8)
    return None, b"all mirrors failed"


def haversine(a, b):
    radius = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dphi = math.radians(b[0] - a[0])
    dlam = math.radians(b[1] - a[1])
    h = (math.sin(dphi / 2) ** 2
         + math.cos(p1) * math.cos(p2) * math.sin(dlam / 2) ** 2)
    return 2 * radius * math.asin(math.sqrt(h))


def measure(key):
    label, bb, routes = CITIES[key]
    bbox = f"{bb[0]},{bb[1]},{bb[2]},{bb[3]}"
    # ONE query: the route relations in the bbox, and their stop members.
    query = (f'[out:json][timeout:240];'
             f'rel["route"~"^({routes})$"]({bbox})->.r;'
             f'node(r.r:"stop");out qt;')
    status, body = ask(query)
    print("=" * 74)
    print(label)
    print("=" * 74)
    if status != 200:
        print(f"  http {status}: {body[:140]}\n")
        return None
    points = [(e["lat"], e["lon"])
              for e in json.loads(body).get("elements", [])
              if e.get("lat") is not None]
    print(f"  stop nodes: {len(points):,}")
    if len(points) < 20:
        print("  too few to measure - and a low count here is a statement "
              "about the bbox or the route filter, not about the city\n")
        return None

    nearest = []
    for i, p in enumerate(points):
        best = None
        for j, q in enumerate(points):
            if i == j:
                continue
            if abs(p[0] - q[0]) > 0.02 or abs(p[1] - q[1]) > 0.03:
                continue          # cheap prune before the trig
            d = haversine(p, q)
            if d < SAME_STOP_M:
                continue
            if best is None or d < best:
                best = d
        if best is not None and best < FAR_M:
            nearest.append(best)

    if not nearest:
        print("  no usable pairs\n")
        return None
    nearest.sort()
    med = median(nearest)
    under = sum(1 for x in nearest if x < 250) / len(nearest) * 100
    print(f"  measured stops           : {len(nearest):,}")
    print(f"  MEDIAN nearest-neighbour : {med:>6.0f} m")
    print(f"  25th / 75th              : {nearest[len(nearest) // 4]:>6.0f} / "
          f"{nearest[3 * len(nearest) // 4]:.0f} m")
    print(f"  under 250 m              : {under:>6.0f}%")
    print()
    return label, len(nearest), med, under


def main():
    wanted = [a.lower() for a in sys.argv[1:] if a.lower() in CITIES]
    keys = list(CONTROLS) + [k for k in (wanted or CITIES) if k not in CONTROLS]

    rows = []
    for key in keys:
        got = measure(key)
        if got:
            rows.append(got)
        time.sleep(10)

    print("=" * 74)
    print("VERDICT - READ THE TWO CONTROLS FIRST")
    print("=" * 74)
    print(f"  {'city':<44} {'stops':>7} {'median':>8} {'<250m':>7}")
    for label, n, med, under in rows:
        print(f"  {label:<44} {n:>7,} {med:>7.0f}m {under:>6.0f}%")

    ctrl = [r for r in rows if "CONTROL" in r[0]]
    if len(ctrl) == 2:
        gap = abs(ctrl[0][2] - ctrl[1][2])
        print()
        print(f"  CONTROL SEPARATION: {gap:.0f} m")
        if gap < 60:
            print("  ** THE CONTROLS DID NOT SEPARATE. **")
            print("  San Francisco needed sub_transit_line_filters.md and San")
            print("  Diego did not. A metric that cannot tell them apart")
            print("  cannot rank anything else either. DO NOT RECORD A")
            print("  VERDICT from this run - fix the metric first, and the")
            print("  test of the fix is whether these two pull apart.")
        else:
            print("  Controls separate; the candidate rows are comparable.")


if __name__ == "__main__":
    main()
