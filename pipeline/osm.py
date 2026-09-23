"""Fetching from OpenStreetMap, shared - because a mirror can lie in THREE
ways and each one was learned separately, in a different city.

WHY THIS IS A MODULE
--------------------
`pipeline/countries/mexico.py` already carries the host list and two of the
three rules, written when Mexico City and Guadalajara were built. It is the
wrong home: Overpass is not Mexican, and Barcelona is the third city to need
it. The meta-rule in `osm-rail` is that a lesson written in one city's config
does not reach the next city - so the fetching rules live here, where the next
OSM city passes through them.

(Mexico's own constants are deliberately left in place rather than re-pointed
at this module: both cities are built, their outputs are committed, and
`drift_check.py` compares against those. Consolidating them is a separate
change with its own drift run, not a side effect of adding a city.)

THE THREE WAYS A MIRROR LIES WITH HTTP 200
------------------------------------------
1. **An EMPTY elements list.** `overpass.osm.ch` returned 272 bytes over an
   empty set during the Mexico build, and a caller reported it as "every ref
   has exactly 2 direction relations" - a confident statement about nothing.
   Measured again 2026-09-22: the same host, twice, no error field.

2. **A `remark`.** Overpass signals an aborted query - timeout, out of memory -
   in a top-level `remark` field, alongside whatever partial data it managed.
   HTTP is still 200.

3. **A PARTIAL answer with NO remark, which is the dangerous one.** Measured
   2026-09-22 on `overpass-api.de`: the same query returned 54 elements and
   then 34 within one minute, with no remark either time. A partial answer is
   shaped exactly like a real decrease in the data, so nothing downstream can
   tell them apart.

(1) and (2) are detectable here and are treated as host failures. **(3) is
not**, which is why `fetch()` CACHES and why anything comparing a count
against an expectation must confirm across two mirrors before believing a
disagreement - see `scripts/brief_check.py`'s `osm_route_refs`.

AND THE MIRRORS DISAGREE WITH EACH OTHER, which is not a failure mode but a
fact. Measured on the Barcelona bbox: `overpass-api.de` returns 20 tram and 6
funicular relations and calls the northern L10 segment `L10N`;
`overpass.kumi.systems` returns 22 and 4 and calls it `L10 Nord`. Neither is
corrupt - they run different planet extracts. So a build must not key anything
on a live tag value, and a cached fetch is the only reproducible one.
"""

import json
import time
import urllib.request

from pipeline.osm_cache import NEVER_A_STATION, load  # noqa: F401

# `load` and `NEVER_A_STATION` live in `pipeline/osm_cache.py` and are
# re-exported here for callers that already fetch. THIS MODULE MUST STAY
# UNGUARDED: it holds `urllib.request`, so any `step*.py` that imports it is a
# real violation and `scripts/check_no_fetch_in_steps.py` fails loudly on one.
# A step that needs to read a cached result imports `osm_cache` instead, which
# has no HTTP client to reach.

# More than one host, tried in order. A failure is a fact about that host, not
# about the city.
OVERPASS_HOSTS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
)
OVERPASS_USER_AGENT = (
    "expanded-heatmap city profiling (github.com/dacekroberts/expanded-heatmap)"
)


def fetch(query, cache_path, *, force=False, timeout=300, retries=2):
    """Overpass elements for `query`, cached at `cache_path`.

    The cache is not an optimisation. A rebuild has to produce the same map as
    the commit it is compared against, and the live answer demonstrably does
    not - two mirrors return different data for the same bbox on the same day.
    So the JSON is written once, committed as the city's raw input is not, and
    re-read thereafter; `force=True` re-fetches deliberately.
    """
    if cache_path.exists() and not force:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        return payload["elements"], payload.get("_fetched_from", "cache")

    problems = []
    for attempt in range(retries):
        for host in OVERPASS_HOSTS:
            name = host.split("/")[2]
            try:
                req = urllib.request.Request(
                    host, data=query.encode("utf-8"),
                    headers={"User-Agent": OVERPASS_USER_AGENT})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    payload = json.loads(r.read().decode("utf-8"))
            except Exception as exc:
                problems.append(f"{name}: {type(exc).__name__}")
                continue
            if payload.get("remark"):
                problems.append(f"{name}: remark {payload['remark']!r}")
                continue
            if not (payload.get("elements") or []):
                problems.append(f"{name}: empty 200")
                continue
            payload["_fetched_from"] = name
            payload["_query"] = query
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(payload, ensure_ascii=False),
                                  encoding="utf-8")
            return payload["elements"], name
        if attempt + 1 < retries:
            time.sleep(5)

    raise RuntimeError(
        "every Overpass mirror failed, which is a HOST problem and not a fact "
        "about this city - " + "; ".join(problems))
