"""One switch that forbids the network, for the fetching a step cannot move out.

Most downloading belongs in `pipeline/<city>/fetch_sources.py`, which is
deliberately not named `step*.py` so `drift_check.py` never runs it. Four
cities were moved there on 2026-09-22 and `scripts/check_no_fetch_in_steps.py`
keeps the rest honest.

THE CASE THIS EXISTS FOR IS THE ONE THAT CANNOT MOVE. `census_geocoder.py`
POSTs a batch of addresses that the step itself computes - the batch is
derived from the step's own filtering, not a fixed upstream URL - so there is
no URL to hoist into a fetch script without hoisting the address preparation
with it. Fetching on a cache miss is the intended workflow there.

What is NOT intended is `drift_check.py` participating in it. A drift check
asks whether the COMMITTED CODE still produces the COMMITTED OUTPUT; a run
that geocodes 9% of Los Angeles over the network first is answering about the
current US Census geocoder instead. So the guard is at the boundary that is
actually wrong: `drift_check.py` sets this variable for every step it runs,
and a fetch under it refuses instead of reaching out.

The distinction this draws, and it is the point: **a step may fetch when a
person runs it. A drift check may never fetch.** Anything that narrows the
first to salvage the second - moving derived-input fetching into a fetch
script, or pretending a cache-guarded download is offline - trades a real
workflow for a tidier rule.
"""

import os

# Set by pipeline/drift_check.py around every step it runs. Also usable by
# hand: HEATMAP_NO_NETWORK=1 python pipeline/<city>/step2_clean_businesses.py
# answers "would this step work on a fresh checkout?" without unplugging
# anything.
NO_NETWORK_ENV = "HEATMAP_NO_NETWORK"


def no_network() -> bool:
    return bool(os.environ.get(NO_NETWORK_ENV))


def refuse_if_offline(what: str, hint: str = "") -> None:
    """Raise rather than fetch, when the caller has been told not to.

    Call this immediately before the request, not at import time: the point is
    to allow a cached run and forbid only the request that would actually go
    out.
    """
    if not no_network():
        return
    raise SystemExit(
        f"{NO_NETWORK_ENV} is set, and {what} is not cached.\n"
        f"  A drift check must not reach the network - it would be asking "
        f"whether the CURRENT UPSTREAM still produces the committed output, "
        f"not whether the committed code does.\n"
        + (f"  {hint}\n" if hint else "")
    )
