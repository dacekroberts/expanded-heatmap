"""Fetching from OpenStreetMap, shared: a mirror can lie in THREE ways, and
each one was learned separately, in a different city.

WHY THIS IS A MODULE
--------------------
`pipeline/countries/mexico.py` also carries the host list and two of the
three rules, written when Mexico City and Guadalajara were built. It is the
wrong home: Overpass is not Mexican, and Barcelona was the third city to need
it. The meta-rule in `osm-rail` is that a lesson written in one city's config
does not reach the next city, so the fetching rules live here, where the next
OSM city passes through them.

(Mexico's own constants are deliberately left in place rather than re-pointed
at this module: both cities are built, their outputs are committed, and
`drift_check.py` compares against those. Consolidating them is a separate
change with its own drift run, not a side effect of adding a city.)

THE THREE WAYS A MIRROR LIES WITH HTTP 200
------------------------------------------
1. **An EMPTY elements list.** `overpass.osm.ch` returned 272 bytes over an
   empty set during the Mexico build, and a caller reported it as "every ref
   has exactly 2 direction relations": a confident statement about nothing.
   Measured again 2026-09-22: the same host, twice, no error field.

2. **A `remark`.** Overpass signals an aborted query (timeout, out of memory)
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
disagreement; see `scripts/brief_check.py`'s `osm_route_refs`.

AND THE MIRRORS DISAGREE WITH EACH OTHER, which is not a failure mode but a
fact. Measured on the Barcelona bbox: `overpass-api.de` returns 20 tram and 6
funicular relations and calls the northern L10 segment `L10N`;
`overpass.kumi.systems` returns 22 and 4 and calls it `L10 Nord`. Neither is
corrupt; they run different planet extracts. So a build must not key anything
on a live tag value, and a cached fetch is the only reproducible one.

A 504 IS EITHER THE QUERY OR THE HOST - CHECK THE QUERY FIRST
-------------------------------------------------------------
(2026-09-23.) A 504 is sometimes the host and nothing else: a TAGS-ONLY
relation query, the cheapest query there is with no geometry at all, drew a
504 from overpass-api.de and a read timeout from kumi.systems, twice in a row
(Lille). But query cost is the half the caller CONTROLS, so rule it out
first, then treat what is left as a fact about the host.

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
   node+way count must never be compared with each other: that measures the
   query, not the city.
3. **Keep `[timeout:N]` inside the query low** (90 is plenty for a city bbox).
   The HTTP timeout is a ceiling on waiting; the in-query one is what lets
   Overpass give up and say so.

⚠ AND A BARE CLIENT SIGNATURE DRAWS HTTP 406 from `overpass-api.de`: the
client-signature refusal `add-country` describes, not an IP block. This module
always sends `OVERPASS_USER_AGENT`, so callers that go through `fetch()` are
covered; an ad-hoc probe written with plain `requests` is not (the Toulouse
probe drew a 406 that way).

⚠ FINALLY, A SLOW RUN MUST NOT BE A SILENT ONE. Without a deadline `fetch()`
could spend `retries x hosts x timeout` (up to half an hour) printing nothing,
so a throttled run was indistinguishable from a hung one. It prints each
attempt and honours a total `deadline`.

⚠ AND A 504, A 429 OR A TIMEOUT MEANS WAIT A MINUTE. The owner's rule
(CLAUDE.md, 2026-09-30): after a 504 or 429, wait at least 60 s before a
retry, never in a tight loop. Both public mirrors were 504ing under several
sessions' load, and `fetch()` was backing off 5 s after the first round (seen
on Tucson's fetch). So a round whose failures include one of those waits
`OVERLOAD_WAIT_S` or more (escalating), a deadline too short for the wait
gives up instead of retrying early, and a
host that refused is not asked again within the minute by a later `fetch()`
in the same run. Other failures (an empty 200, a remark, all-zero counts) are
not load, and keep the short backoff.
"""

import json
import time
import urllib.error
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
#
# GLOBAL MIRRORS ONLY. overpass.osm.ch was removed 2026-09-27: it serves a
# Swiss-only extract, so for anywhere else it answers HTTP 200 with nothing
# (or zero counts). scripts/check_overpass_hosts.py fails if it, or any host
# that is not global, appears in any Overpass host list in the repository.
OVERPASS_HOSTS = (
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
)
OVERPASS_USER_AGENT = (
    "expanded-heatmap city profiling (github.com/dacekroberts/expanded-heatmap)"
)

# The owner's floor after a 504, a 429 or a timeout (see the docstring).
OVERLOAD_WAIT_S = 60
OVERLOAD_HTTP_CODES = (429, 504)

# Host name -> time.monotonic() of its last 504, 429 or timeout in this
# process, so a second fetch() does not ask a host that refused seconds ago.
_overloaded_at = {}


def is_overload(exc):
    """True for a 504, a 429 or a timeout - the failures the 60 s rule covers."""
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code in OVERLOAD_HTTP_CODES
    return isinstance(exc, TimeoutError) or "timed out" in str(exc).lower()


def overload_wait_left(name):
    """Seconds before host `name` may be asked again; 0 if it has not refused."""
    at = _overloaded_at.get(name)
    if at is None:
        return 0.0
    return max(0.0, OVERLOAD_WAIT_S - (time.monotonic() - at))


def fetch(query, cache_path, *, force=False, timeout=180, retries=2,
          deadline=900, verbose=True):
    """Return the Overpass elements for `query`, cached at `cache_path`.

    The cache is not an optimisation. A rebuild has to produce the same map as
    the commit it is compared against, and the live answer does not: two
    mirrors return different data for the same bbox on the same day. So the
    JSON is written once, committed as the city's raw input is not, and
    re-read thereafter; `force=True` re-fetches deliberately.

    `deadline` is a TOTAL wall-clock budget in seconds across every host and
    retry, so a run cannot burn `retries x hosts x timeout` in silence. Pass
    None to wait as long as it takes.

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
        overloaded = False
        for host in OVERPASS_HOSTS:
            name = host.split("/")[2]
            left = _left()
            if left is not None and left <= 0:
                problems.append(f"deadline of {deadline}s exhausted")
                break
            wait = overload_wait_left(name)
            if wait > 0:
                # Refused by an earlier fetch() in this run. Wait out the
                # owner's minute, or skip the host if the deadline cannot.
                if left is not None and left < wait + 10:
                    problems.append(f"{name}: refused under {OVERLOAD_WAIT_S}s "
                                    f"ago and the deadline leaves {left:.0f}s")
                    _say(f"[{attempt}] {name} -> skipped, refused under "
                         f"{OVERLOAD_WAIT_S}s ago")
                    continue
                _say(f"[{attempt}] {name} refused under {OVERLOAD_WAIT_S}s "
                     f"ago, waiting {wait:.0f}s")
                time.sleep(wait)
                left = _left()
            per = timeout if left is None else max(10, min(timeout, left))
            _say(f"[{attempt}] {name} (timeout {per:.0f}s)")
            try:
                req = urllib.request.Request(
                    host, data=query.encode("utf-8"),
                    headers={"User-Agent": OVERPASS_USER_AGENT})
                with urllib.request.urlopen(req, timeout=per) as r:
                    payload = json.loads(r.read().decode("utf-8"))
            except Exception as exc:
                # An HTTP 504 here may be the QUERY or the host - see the
                # docstring. Named in the message so the next person rules out
                # cost before reading it as an outage. Either way it is load,
                # and the owner's minute applies before this host is asked again.
                hint = ""
                if is_overload(exc):
                    overloaded = True
                    _overloaded_at[name] = time.monotonic()
                    hint = " (504/429/timeout - try nodes-only, drop `out center`)"
                problems.append(f"{name}: {type(exc).__name__}{hint}")
                _say(f"[{attempt}] {name} -> {type(exc).__name__}{hint}")
                continue
            if payload.get("remark"):
                # "Query timed out" in a remark is the server's own timeout,
                # which is load in the same way as a 504.
                if "timed out" in str(payload["remark"]).lower():
                    overloaded = True
                    _overloaded_at[name] = time.monotonic()
                problems.append(f"{name}: remark {payload['remark']!r}")
                _say(f"[{attempt}] {name} -> remark")
                continue
            if not (payload.get("elements") or []):
                problems.append(f"{name}: empty 200")
                _say(f"[{attempt}] {name} -> empty 200 (not trusted)")
                continue
            # An `out count` answer is never empty (it is one `count` element),
            # so a host holding no data for this area answers with zeros and
            # passes the check above. overpass.osm.ch (a Swiss-only extract)
            # did exactly that for Daugavpils, Aarhus, Zoetermeer and
            # Amstelveen (2026-09-27). All-zero counts are treated
            # like an empty 200: a real "none here" is confirmed by another
            # mirror answering the same.
            els = payload["elements"]
            if all(e.get("type") == "count" for e in els) and not any(
                    str(v) not in ("0", "") for e in els
                    for v in (e.get("tags") or {}).values()):
                problems.append(f"{name}: all-zero count")
                _say(f"[{attempt}] {name} -> all-zero count (not trusted)")
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
            if overloaded:
                # The owner's floor, escalating above it: 60 s, 120 s, ... A
                # deadline that cannot fit the wait plus a 10 s request gives
                # up here rather than retrying early.
                nap = max(nap, OVERLOAD_WAIT_S * (attempt + 1))
                if left is not None and left < nap + 10:
                    problems.append(f"a 504/429/timeout needs {nap}s before a "
                                    f"retry and the deadline leaves {left:.0f}s")
                    _say(f"all hosts failed, {nap}s backoff does not fit the "
                         "deadline - giving up")
                    break
            elif left is not None:
                nap = min(nap, max(0, left))
            _say(f"all hosts failed, backing off {nap:.0f}s")
            time.sleep(nap)

    raise RuntimeError(
        "every Overpass mirror failed, which is a HOST problem or an "
        "over-expensive QUERY and not a fact about this city - "
        + "; ".join(problems))
