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
and reaches the network on every fresh checkout, including in CI and inside a
drift check that then reports "zero drift" about a file it just re-downloaded.
On 2026-09-22 a drift check in a fresh worktree pulled a 39 MB DENUE zip and
three Overpass responses before reporting no drift, while Toronto (which
fetches in `fetch_sources.py`) stopped correctly with "no data/<city>/raw/ -
nothing to run against".

The hazard is real: the same day, re-fetching Toronto's register produced a
map missing a storefront that is in the committed one, while the row-count
baseline reported identical because the counts matched.

THE RULE. Downloading lives in `pipeline/<city>/fetch_sources.py`, which is
deliberately not named `step*.py` so `drift_check.py` never runs it. A step
reads the cache and exits non-zero naming that script if it is missing.

WHAT THIS CHECKS THAT A GREP WOULD NOT
--------------------------------------
Transitive reach. `pipeline/census_geocoder.py` imports `requests` and is
imported by three cities' `step3_geocode.py`, so those steps fetch without any
HTTP client appearing in them: the same defect one import deeper, and the
reason this follows a step's imports. It follows ALL of them, transitively,
into every module under `pipeline/` (shared ones, `pipeline/countries/`,
`pipeline/taxonomies/`, another city's step, and helpers inside the step's
own city folder, whether imported as `pipeline.<city>.x`, as a bare sibling
name or relatively). Until 2026-10-02 it read only `pipeline/*.py`, one level
deep, so `pipeline/seattle/lcb_offpremise.py` could have fetched at import
unseen (Seattle (Regional) build, docs/decisions_drafts/seattle-tbilisi.md).

FENCED IS THE ONE EXCEPTION. A helper may keep its own download beside its
reader if the HTTP import sits inside a module-level function named exactly
`fetch`, which only `fetch_sources.py` calls. Importing such a module runs no
request; calling `fetch` would. So the check fails a step if anything in its
reach references that `fetch` (`m.fetch`, `from m import fetch`, or the
module calling its own `fetch` outside its `__main__` block). An HTTP import
anywhere else in the module, a `fetch` inside a class, or any HTTP import in a
step file itself is not fenced.

GUARDED IS A THIRD ANSWER, NOT A PASS IN DISGUISE. The geocoder cannot move to
a fetch script: its input is a batch of addresses the step computes, so there
is no URL to hoist. The real rule there is narrower (a DRIFT CHECK must never
fetch, while a person running the step may), so the fix is a guard at that
boundary (`pipeline/offline.py`), and this check reports such a module as
guarded rather than either failing it or pretending it is offline. A guard
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
# EMPTY since 2026-09-22, when the branch carrying the fix for Madrid's step1
# and step2 landed: an entry goes stale in the same commit as its fix, and
# deleting it is part of landing that fix, not a tidy-up afterwards.
KNOWN_GAPS = {}

# A shared module is GUARDED if it calls this before requesting. See
# pipeline/offline.py: the three step3_geocode.py files reach the network
# through census_geocoder.py by design, and what makes that acceptable is
# that a drift check cannot follow them there.
GUARD_CALL = "refuse_if_offline"

# The one function name an HTTP import may hide in. See FENCED in the
# docstring: allowed only while nothing a step reaches references it.
FENCE = "fetch"

# Packages that import their members by name at run time, which no import
# statement shows. `pipeline/taxonomies/__init__.py`'s load_taxonomy_module()
# calls importlib on a TAXONOMY_MODULES entry, so reaching the package counts
# as reaching every module in it: an over-approximation, and the safe side.
DYNAMIC_FANOUT = ("pipeline.taxonomies",)


def module_index():
    """Every module under pipeline/, dotted name -> file. A package's name
    maps to its `__init__.py`."""
    index = {}
    for p in sorted(PIPELINE.rglob("*.py")):
        parts = list(p.relative_to(ROOT).with_suffix("").parts)
        if parts[-1] == "__init__":
            parts = parts[:-1]
        index[".".join(parts)] = p
    return index


def _dotted(node):
    """`a.b.c` for a Name/Attribute chain, else None."""
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if not isinstance(node, ast.Name):
        return None
    parts.append(node.id)
    return ".".join(reversed(parts))


def _is_main_block(stmt):
    """True for `if __name__ == "__main__":`, which an import never runs."""
    t = getattr(stmt, "test", None)
    return (isinstance(stmt, ast.If) and isinstance(t, ast.Compare)
            and isinstance(t.left, ast.Name) and t.left.id == "__name__"
            and len(t.comparators) == 1
            and isinstance(t.comparators[0], ast.Constant)
            and t.comparators[0].value == "__main__")


class Module:
    """What one file imports, which HTTP clients it holds and where, whether
    it calls the offline guard, and whose `fetch` it references."""

    def __init__(self, name, path, index):
        self.name, self.path = name, path
        rel = path.relative_to(ROOT)
        # The package a relative import starts from, and the one a bare
        # sibling import resolves in (a step run as a script has its own
        # folder first on sys.path, so `import lcb_offpremise` works there).
        self.package = ".".join(rel.parent.parts)
        self._index = index
        self.unfenced = set()      # HTTP clients imported outside the fence
        self.fenced = set()        # HTTP clients imported inside `def fetch`
        self.guarded = False
        self.imports = set()       # pipeline modules this one runs on import
        self.aliases = {}          # local name -> dotted module
        self.fetch_refs = set()    # modules whose fetch is referenced
        self.fetch_refs_main = set()   # the same, from the __main__ block
        self._raw_refs = []        # (dotted or None for bare, in __main__)

        tree = ast.parse(path.read_text(encoding="utf-8"))
        for stmt in tree.body:
            if (isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and stmt.name == FENCE):
                self._scan(stmt, fenced=True, main=False)
            else:
                self._scan(stmt, fenced=False, main=_is_main_block(stmt))
        self._resolve_refs()

    def _canonical(self, dotted):
        """A name as written -> the dotted module it means. A bare name that
        is a sibling file resolves into this module's own package. Exact for
        a step and its city's helpers; a shared module's bare import really
        resolves against the running step's folder, which this does not
        model."""
        first = dotted.split(".")[0]
        if self.package and f"{self.package}.{first}" in self._index:
            return f"{self.package}.{dotted}"
        return dotted

    def _relative_base(self, level, module):
        parts = self.package.split(".") if self.package else []
        if level > 1:
            parts = parts[: len(parts) - (level - 1)]
        base = ".".join(parts)
        if module:
            base = f"{base}.{module}" if base else module
        return base

    def _reach(self, dotted):
        """Every indexed module importing `dotted` runs: the module itself
        and each parent package's __init__."""
        parts = dotted.split(".")
        for i in range(1, len(parts) + 1):
            prefix = ".".join(parts[:i])
            if prefix in self._index:
                self.imports.add(prefix)

    def _scan(self, root, fenced, main):
        http = self.fenced if fenced else self.unfenced
        for node in ast.walk(root):
            if isinstance(node, ast.Import):
                for a in node.names:
                    http |= http_clients({a.name})
                    if fenced:
                        continue
                    full = self._canonical(a.name)
                    self._reach(full)
                    if a.asname:
                        self.aliases[a.asname] = full
                    else:
                        head = a.name.split(".")[0]
                        self.aliases[head] = self._canonical(head)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    base = self._relative_base(node.level, node.module)
                else:
                    base = node.module or ""
                    http |= http_clients(
                        {base} | {f"{base}.{a.name}" for a in node.names})
                    base = self._canonical(base)
                if fenced:
                    continue
                self._reach(base)
                for a in node.names:
                    self._reach(f"{base}.{a.name}")
                    self.aliases[a.asname or a.name] = f"{base}.{a.name}"
                    if a.name == FENCE:
                        (self.fetch_refs_main if main
                         else self.fetch_refs).add(base)
            elif fenced:
                continue
            elif isinstance(node, ast.Call):
                f = node.func
                if (getattr(f, "id", None) or getattr(f, "attr", None)) \
                        == GUARD_CALL:
                    self.guarded = True
            if fenced:
                continue
            if isinstance(node, ast.Attribute) and node.attr == FENCE:
                d = _dotted(node.value)
                if d:
                    self._raw_refs.append((d, main))
            elif (isinstance(node, ast.Name) and node.id == FENCE
                  and isinstance(node.ctx, ast.Load)):
                self._raw_refs.append((None, main))

    def _resolve_refs(self):
        """After every alias is known, so source order cannot matter."""
        for d, main in self._raw_refs:
            refs = self.fetch_refs_main if main else self.fetch_refs
            if d is None:
                # A bare `fetch`: this module's own, unless imported.
                if FENCE not in self.aliases:
                    refs.add(self.name)
                continue
            head, _, rest = d.partition(".")
            if head in self.aliases:
                full = self.aliases[head] + ("." + rest if rest else "")
                if full in self._index:
                    refs.add(full)


def closure(start, index, cache):
    """Every pipeline module importing `start` runs, `start` included."""
    seen, todo = set(), [start]
    while todo:
        name = todo.pop()
        if name in seen or name not in index:
            continue
        seen.add(name)
        if name not in cache:
            cache[name] = Module(name, index[name], index)
        todo.extend(cache[name].imports - seen)
        if name in DYNAMIC_FANOUT:
            todo.extend(n for n in index if n.startswith(name + "."))
    return seen


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

    steps = sorted(PIPELINE.glob("*/step*.py"))
    if not steps:
        raise SystemExit("Found no pipeline/*/step*.py at all - this check "
                         "would pass vacuously, which is worse than failing.")

    index = module_index()
    cache = {}
    violations = {}                       # rel path -> [(kind, detail)]
    guarded = {}                          # reaches the network, but not
                                          # from inside a drift check
    reached_http = set()                  # non-step modules worth listing
    for p in steps:
        rel = p.relative_to(ROOT).as_posix()
        me = ".".join(p.relative_to(ROOT).with_suffix("").parts)
        reach = closure(me, index, cache)
        step = cache[me]
        # A step file gets no fence: its own `fetch` would still be a step
        # downloading its input.
        direct = step.unfenced | step.fenced
        if direct:
            violations[rel] = [("imports", ", ".join(sorted(direct)))]
            continue
        others = reach - {me}
        via = sorted(m for m in others if cache[m].unfenced)
        reached_http.update(m for m in others
                            if cache[m].unfenced or cache[m].fenced)
        # Whose `fetch` the step's reach refers to. The step's own __main__
        # block runs; a helper's never does on import.
        refs = step.fetch_refs | step.fetch_refs_main
        for m in others:
            refs |= cache[m].fetch_refs
        called = sorted(m for m in refs
                        if m in cache and m in reach and cache[m].fenced)
        found = []
        if via:
            reached = sorted(set().union(*(cache[m].unfenced for m in via)))
            found.append(("reaches via " + ", ".join(via), ", ".join(reached)))
        if called:
            fenced = sorted(set().union(*(cache[m].fenced for m in called)))
            found.append(("calls " + ", ".join(f"{m}.{FENCE}()"
                                               for m in called),
                          ", ".join(fenced)))
        if called or any(not cache[m].guarded for m in via):
            violations[rel] = found
        elif via:
            guarded[rel] = found[0]

    # What a step can reach: a step that imports one of these inherits it.
    if reached_http:
        print("Pipeline modules a step reaches that hold an HTTP client:")
        for m in sorted(reached_http):
            mod = cache[m]
            state = ("UNGUARDED" if mod.unfenced and not mod.guarded
                     else "GUARDED" if mod.unfenced
                     else "FENCED")
            hits = mod.unfenced or mod.fenced
            where = "" if mod.unfenced else f" (inside {FENCE}() only)"
            print(f"  {state:9s} {mod.path.relative_to(ROOT).as_posix()}  ->  "
                  f"{', '.join(sorted(hits))}{where}")
        print()

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

    for rel, found in sorted(violations.items()):
        if rel in KNOWN_GAPS:
            lines = "".join(f"\n           {k}: {d}" for k, d in found)
            print(f"KNOWN GAP  {rel}{lines}\n           {KNOWN_GAPS[rel]}")
        else:
            lines = "".join(f"\n    {k}: {d}" for k, d in found)
            failures.append(f"{rel}{lines}")

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

    if KNOWN_GAPS:
        print("OK - no step fetches inside a drift check, except the gaps "
              "listed above.")
    else:
        print("OK - no step fetches inside a drift check, and there are no "
              "known gaps left.")
    return 0


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # Hangul, Han and kana, and on Czech and Latvian letters (brief_check.py,
    # on a Korean claim, 2026-09-27). UTF-8 regardless of the console.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
