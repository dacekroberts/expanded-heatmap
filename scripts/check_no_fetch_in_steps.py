"""No pipeline step may reach the network. Run it; it fails if one can.

    python scripts/check_no_fetch_in_steps.py [--list]

WHY THIS IS A SCRIPT AND NOT A PARAGRAPH
----------------------------------------
`pipeline/drift_check.py` asks whether the COMMITTED CODE still produces the
COMMITTED OUTPUT. A step that downloads its own input first asks whether the
CURRENT UPSTREAM does - a different question, and one that passes or fails for
reasons no commit here caused.

The defect is invisible on a developer machine, because every such step guards
its download with `if cache.exists()`, and the cache is `data/<city>/raw/`,
which is gitignored. So it is offline exactly when someone has already run it,
and reaches the network on every fresh checkout - including in CI, and
including inside a drift check that then reports "zero drift" about a file it
just re-downloaded. Demonstrated 2026-09-22: a drift check in a fresh worktree
pulled a 39 MB DENUE zip and three Overpass responses before reporting no
drift, while Toronto - which keeps fetching in `fetch_sources.py` - stopped
correctly with "no data/<city>/raw/ - nothing to run against".

Toronto also proved the hazard is not theoretical the same day: re-fetching its
register produced a map missing a storefront that is in the committed one,
while the row-count baseline reported identical because the counts matched.

THE RULE. Downloading lives in `pipeline/<city>/fetch_sources.py`, which is
deliberately not named `step*.py` so `drift_check.py` never runs it. A step
reads the cache and exits non-zero naming that script if it is missing.

WHAT THIS CHECKS THAT A GREP WOULD NOT
--------------------------------------
Transitive reach. `pipeline/census_geocoder.py` imports `requests` and is
imported by three cities' `step3_geocode.py`, so those steps fetch without any
HTTP client appearing in them - the same defect one import deeper, and the
reason this walks the shared `pipeline/*.py` modules too. It was found by
writing this check, not before it.

GUARDED IS A THIRD ANSWER, NOT A PASS IN DISGUISE. The geocoder cannot move to
a fetch script: its input is a batch of addresses the step computes, so there
is no URL to hoist. What was actually wrong there was narrower - a DRIFT CHECK
must never fetch, while a person running the step may - so the fix is a guard
at that boundary (`pipeline/offline.py`), and this check reports such a module
as guarded rather than either failing it or pretending it is offline. A guard
nobody arms is worse than none, so the last limb below reads
`pipeline/drift_check.py` and fails if it does not set the variable.
"""

import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPELINE = ROOT / "pipeline"


def _use_root(root):
    """Point the check at another tree. Only --root does this, and only the
    self-test passes it: a check that silently examined somewhere other than
    the repository it lives in would be worse than no check."""
    global ROOT, PIPELINE
    ROOT = Path(root).resolve()
    PIPELINE = ROOT / "pipeline"

# `urllib.parse` is deliberately absent: building a URL is not fetching one,
# and several steps quote query parameters for a URL that fetch_sources.py
# will later request.
HTTP_MODULES = {
    "requests", "httpx", "aiohttp", "urllib3", "pycurl",
    "urllib.request", "urllib.error", "http.client", "ftplib", "socket",
}

# Dated defects, not passes. Each entry says what is wrong and where the fix
# is; an entry that has stopped being true fails this check as loudly as a new
# violation, so the list cannot rot into a permanent exemption.
KNOWN_GAPS = {
    "pipeline/madrid/step1_stations.py":
        "fetching still in the step on master; already moved to "
        "pipeline/madrid/fetch_sources.py on the unmerged spain-app-wiring "
        "branch (2026-09-22). Remove this entry when that branch lands.",
    "pipeline/madrid/step2_clean_businesses.py":
        "same as step1 - fixed on spain-app-wiring, not yet on master.",
}

# A shared module is GUARDED if it calls this before requesting. See
# pipeline/offline.py: the three step3_geocode.py files reach the network
# through census_geocoder.py by design, and what makes that acceptable is
# that a drift check cannot follow them there.
GUARD_CALL = "refuse_if_offline"


def imported_modules(path):
    """Every module name this file imports, dotted and fully qualified."""
    names = set()
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:            # a relative import, never an HTTP client
                continue
            if node.module:
                names.add(node.module)
                for a in node.names:
                    names.add(f"{node.module}.{a.name}")
    return names


def calls_guard(path):
    """Does this module call refuse_if_offline() anywhere?"""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = getattr(f, "id", None) or getattr(f, "attr", None)
            if name == GUARD_CALL:
                return True
    return False


def drift_check_arms_the_guard():
    """The guard is inert unless drift_check.py sets the variable.

    Read as text rather than imported, because the failure being guarded
    against is exactly that someone deletes the line.
    """
    p = PIPELINE / "drift_check.py"
    if not p.exists():
        return "pipeline/drift_check.py does not exist"
    src = p.read_text(encoding="utf-8")
    if "NO_NETWORK_ENV" not in src:
        return ("pipeline/drift_check.py never mentions NO_NETWORK_ENV, so "
                "the offline guard is never armed and every guarded module "
                "below is free to fetch inside a drift check")
    return None


def http_clients(names):
    """Which banned modules a set of imported names reaches.

    Matches a prefix, so `urllib.request` is caught by `import
    urllib.request` and by `from urllib.request import urlopen` alike, while
    `urllib.parse` is not caught by either.
    """
    hits = set()
    for n in names:
        for banned in HTTP_MODULES:
            if n == banned or n.startswith(banned + "."):
                hits.add(banned)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true",
                    help="print every step and what it reaches, then exit 0")
    ap.add_argument("--root", default=None,
                    help="check this tree instead of the repository "
                         "(used by check_no_fetch_in_steps_selftest.py)")
    args = ap.parse_args()
    if args.root:
        _use_root(args.root)
        print(f"(checking {ROOT})\n")

    # Shared pipeline modules first: a step that imports one of these inherits
    # whatever it reaches.
    shared = {}
    for p in sorted(PIPELINE.glob("*.py")):
        hits = http_clients(imported_modules(p))
        if hits:
            shared[f"pipeline.{p.stem}"] = (p, hits, calls_guard(p))
    if shared:
        print("Shared pipeline modules that reach the network:")
        for mod, (p, hits, guarded) in sorted(shared.items()):
            state = "GUARDED" if guarded else "UNGUARDED"
            print(f"  {state:9s} {p.relative_to(ROOT).as_posix()}  ->  "
                  f"{', '.join(sorted(hits))}")
        print()

    steps = sorted(PIPELINE.glob("*/step*.py"))
    if not steps:
        raise SystemExit("Found no pipeline/*/step*.py at all - this check "
                         "would pass vacuously, which is worse than failing.")

    violations = {}                       # rel path -> (kind, detail)
    guarded = {}                          # reaches the network, but not
                                          # from inside a drift check
    for p in steps:
        rel = p.relative_to(ROOT).as_posix()
        names = imported_modules(p)
        direct = http_clients(names)
        if direct:
            violations[rel] = ("imports", ", ".join(sorted(direct)))
            continue
        via = sorted(m for m in names if m in shared)
        if via:
            reached = sorted(set().union(*(shared[m][1] for m in via)))
            if all(shared[m][2] for m in via):
                guarded[rel] = ("reaches via " + ", ".join(via),
                                ", ".join(reached))
            else:
                violations[rel] = ("reaches via " + ", ".join(via),
                                   ", ".join(reached))

    if args.list:
        for p in steps:
            rel = p.relative_to(ROOT).as_posix()
            mark = ("FETCHES" if rel in violations
                    else "guarded" if rel in guarded else "offline")
            print(f"  {mark:8s} {rel}")
        return 0

    failures = []

    arming = drift_check_arms_the_guard()
    if guarded:
        print("Guarded - reaches the network when a person runs the step, "
              "never inside a drift check:")
        for rel, (kind, detail) in sorted(guarded.items()):
            print(f"  {rel}\n      {kind}: {detail}")
        print()
        if arming:
            failures.append(f"the offline guard is not armed\n    {arming}")

    for rel, (kind, detail) in sorted(violations.items()):
        if rel in KNOWN_GAPS:
            print(f"KNOWN GAP  {rel}\n           {kind}: {detail}\n"
                  f"           {KNOWN_GAPS[rel]}")
        else:
            failures.append(f"{rel}\n    {kind}: {detail}")

    # A gap that has been fixed must be deleted from the list, or the list
    # becomes a place where a defect goes to be forgotten.
    stale = [rel for rel in KNOWN_GAPS if rel not in violations]
    for rel in sorted(stale):
        if not (ROOT / rel).exists():
            failures.append(f"{rel}\n    listed under KNOWN_GAPS but the file "
                            f"does not exist - the entry is stale.")
        else:
            failures.append(f"{rel}\n    listed under KNOWN_GAPS but no longer "
                            f"reaches the network. Delete the entry.")

    print(f"\n{len(steps)} step files checked: "
          f"{len(violations)} reach the network unguarded "
          f"({len(KNOWN_GAPS)} known and dated), "
          f"{len(guarded)} reach it only outside a drift check.")

    if failures:
        print("\nFAIL - a step must not fetch its own input:")
        for f in failures:
            print(f"  {f}")
        print("\n  Move the download to pipeline/<city>/fetch_sources.py and "
              "have the step read the cache, exiting non-zero and naming that "
              "script when it is missing. pipeline/guadalajara/ is the worked "
              "pattern.")
        return 1

    print("OK - no step fetches inside a drift check, except the gaps "
          "listed above.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
