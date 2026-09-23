"""Reading a cached OpenStreetMap result - the half of `pipeline/osm.py` that
a `step*.py` is allowed to import.

WHY THIS IS A SEPARATE MODULE FROM `osm.py`, WHICH HOLDS ONE FUNCTION
--------------------------------------------------------------------
`scripts/check_no_fetch_in_steps.py` asks what a step's imports can reach, one
level deep, and a module is either UNGUARDED (a step importing it fails) or
GUARDED (a step importing it passes, because the module refuses to request
while a drift check is running). `pipeline/osm.py` contains `fetch()` and
therefore `urllib.request`, so Barcelona's step 1 - which only ever reads a
cache - failed that check on the strength of an import it never calls.

Neither of the two obvious fixes is honest. Marking `osm.py` GUARDED would say
"this step may fetch, but not during a drift check", when the truth is that it
cannot fetch at all; it would also hand every future city a door through which
a step could fetch and still pass. Suppressing the finding says nothing at all.

So the cache reader moved here, where there is no HTTP client to import, and
`osm.py` stays UNGUARDED on purpose: any `step*.py` that imports it is a real
violation and the check still says so loudly. `fetch_sources.py` files import
`osm.py`; step files import this.
"""

import json

# Entrances are never stations - 447 of them against 184 stations in Mexico
# City, 114 in Guadalajara, 468 against 181 in Barcelona. `prpopsed` is in this
# list because five real OSM nodes are spelled that way: a blacklist misses a
# typo, which is why each city's step 1 WHITELISTS what it wants and this exists
# to be printed as a record of what was dropped.
NEVER_A_STATION = ("subway_entrance", "proposed", "construction", "prpopsed")


def load(cache_path, what):
    """Read a cached Overpass result. NEVER fetches, and cannot.

    This is what a `step*.py` calls. `fetch()` belongs to `fetch_sources.py`
    alone, because `drift_check.py` re-runs every `step*.py` and a drift check
    has to be deterministic and offline - San Francisco's `fetch_sources.py`
    states that as an invariant, and since 2026-09-22 it holds for all
    eighteen cities rather than fifteen of them.
    """
    if not cache_path.exists():
        raise SystemExit(
            f"{cache_path.name} is missing, and a step file must never fetch.\n"
            f"  Run:  python pipeline/{cache_path.parent.parent.name}/"
            f"fetch_sources.py\n"
            f"  ({what})")
    payload = json.loads(cache_path.read_text(encoding="utf-8"))
    return payload["elements"], payload.get("_fetched_from", "cache")
