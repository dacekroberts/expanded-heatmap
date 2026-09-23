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

WHAT A 504 USUALLY MEANS: YOUR QUERY IS TOO EXPENSIVE, NOT THE HOST IS DOWN
--------------------------------------------------------------------------
Added 2026-09-23 after the Toulouse build lost ten minutes to it, and it is
the cheapest fix in this file.

`out center` on **ways** is the expensive part of a typical POI query. Overpass
has to resolve every way's member nodes to compute a centroid, so a combined
node+way query costs far more than the node half alone. Measured that day on
the Toulouse commune bbox, same tag, same hosts, minutes apart:

    node+way + `out center`   ->  504 on overpass-api.de, read timeout on kumi
    node only + `out body`    ->  answered in SECONDS on the first host tried

Both queries were for `amenity=fast_food` over the same bbox. Nothing about
the hosts changed; the query did.

So, in order:

1. **Ask for nodes first.** `node[...](bbox); out body;` For POI counting this
   is usually 90%+ of the answer - restaurant nodes were 827 of the 889
   node+way total in Toulouse, 93.0%.
2. **Add ways only if the node answer is not enough**, as a SECOND query, and
   say in the caller which shape produced the number. A node-only count and a
   node+way count must never be compared with each other - that measures the
   query, not the city.
3. **Keep `[timeout:N]` inside the query low** (90 is plenty for a city bbox).
   The HTTP timeout is a ceiling on waiting; the in-query one is what lets
   Overpass give up and tell you so.

⚠ AND A BARE CLIENT SIGNATURE DRAWS HTTP 406 from `overpass-api.de` - the
client-signature refusal `add-country` describes, not an IP block. This module
always sends `OVERPASS_USER_AGENT`, so callers that go through `fetch()` are
covered; an ad-hoc probe written with plain `requests` is not, and that is
exactly how the Toulouse probe earned its first 406.

⚠ FINALLY, A SLOW RUN MUST NOT BE A SILENT ONE. `fetch()` used to be able to
spend `retries x hosts x timeout` - up to half an hour - printing nothing, so
a throttled run was indistinguishable from a hung one. It now prints each
attempt and honours a total `deadline`.
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


def fetch(query, cache_path, *, force=False, timeout=180, retries=2,
          deadline=900, verbose=True):
    """Overpass elements for `query`, cached at `cache_path`.

    The cache is not an optimisation. A rebuild has to produce the same map as
    the commit it is compared against, and the live answer demonstrably does
    not - two mirrors return different data for the same bbox on the same day.
    So the JSON is written once, committed as the city's raw input is not, and
    re-read thereafter; `force=True` re-fetches deliberately.

    `deadline` is a TOTAL wall-clock budget in seconds across every host and
    retry, and it exists because the old shape could burn `retries x hosts x
    timeout` in silence. Pass None to wait as long as it takes.

    `timeout` is per request and defaults to 180 rather than 300: a city-bbox
    query that has not answered in three minutes is an expensive query, and
    the fix is to make it cheaper (see this module's docstring on `out
    center`), not to wait longer.
    """
    if cache_path.exists() and not force:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        return payload["elements"], payload.get("_fetched_from", "cache")

    started = time.monotonic()

    def _left():
        return None if deadline is None else deadline - (time.monotonic() - started)

    def _say(msg):
        if verbose:
            print(f"    overpass {msg}", flush=True)

    problems = []
    for attempt in range(retries):
        for host in OVERPASS_HOSTS:
            name = host.split("/")[2]
            left = _left()
            if left is not None and left <= 0:
                problems.append(f"deadline of {deadline}s exhausted")
                break
            per = timeout if left is None else max(10, min(timeout, left))
            _say(f"[{attempt}] {name} (timeout {per:.0f}s)")
            try:
                req = urllib.request.Request(
                    host, data=query.encode("utf-8"),
                    headers={"User-Agent": OVERPASS_USER_AGENT})
                with urllib.request.urlopen(req, timeout=per) as r:
                    payload = json.loads(r.read().decode("utf-8"))
            except Exception as exc:
                # An HTTP 504 here is nearly always the QUERY, not the host -
                # see the docstring. Named in the message so the next person
                # reads it as a cost problem rather than an outage.
                hint = ""
                if "504" in str(exc) or "timed out" in str(exc).lower():
                    hint = " (504/timeout - try nodes-only, drop `out center`)"
                problems.append(f"{name}: {type(exc).__name__}{hint}")
                _say(f"[{attempt}] {name} -> {type(exc).__name__}{hint}")
                continue
            if payload.get("remark"):
                problems.append(f"{name}: remark {payload['remark']!r}")
                _say(f"[{attempt}] {name} -> remark")
                continue
            if not (payload.get("elements") or []):
                problems.append(f"{name}: empty 200")
                _say(f"[{attempt}] {name} -> empty 200 (not trusted)")
                continue
            payload["_fetched_from"] = name
            payload["_query"] = query
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(payload, ensure_ascii=False),
                                  encoding="utf-8")
            _say(f"[{attempt}] {name} -> {len(payload['elements'])} elements")
            return payload["elements"], name
        left = _left()
        if left is not None and left <= 0:
            break
        if attempt + 1 < retries:
            # Escalating rather than flat: a throttling host that refused a
            # moment ago is unlikely to have changed its mind in 5 seconds.
            nap = 5 * (attempt + 1) ** 2
            if left is not None:
                nap = min(nap, max(0, left))
            _say(f"all hosts failed, backing off {nap:.0f}s")
            time.sleep(nap)

    raise RuntimeError(
        "every Overpass mirror failed, which is a HOST problem or an "
        "over-expensive QUERY and not a fact about this city - "
        + "; ".join(problems))
