"""Rebuild every place-search index from its cached OpenStreetMap places, in
memory, and compare it with the files on disk (or at a git revision). Writes
nothing and never fetches.

    python scripts/check_place_index_drift.py [city ...]            # against the files on disk
    python scripts/check_place_index_drift.py --against REV [city ...]   # what changed since REV
    python scripts/check_place_index_drift.py --selftest

WHY (place search batch 2b, 2026-10-08; docs/decisions_drafts/place-search.md):
a commit held ten indexes built under rules older than the place_index.py it
committed, and nothing noticed. scripts/check_place_search.py proves each map
carries its index's current hash; this proves each index is what the current
code builds from its cache. pipeline/drift_check.py re-runs the index steps
too, but diffs only outputs/ (the indexes live in app/static/places/) and runs
every city's whole pipeline.

Run it after ANY change to pipeline/place_index.py or a city's PLACE_* config:
  * on disk: every index must match (exit 1 names each city that drifts, with
    the rows its rebuild adds and removes); rebuild the drifting cities with
    their step2b_place_index.py, then re-render their maps once.
  * --against REV (the last commit before a rule change, say): lists, per
    city, the rows the current code adds and removes against that revision's
    index. A rule meant for a new city that changes a built city's index is a
    change to reviewed work: list it for the owner (the 2b audit found twelve
    English street words that let 354 driveway and arcade rows into three
    built indexes).

A city whose cache is not on disk (a fresh checkout: data/ is not committed)
is SKIPPED and named, never passed. Measured 2026-10-08: fourteen cities in
78 s, peak 0.56 GB; run it through scripts/heavy_job.py all the same.
"""
import collections
import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def searched_cities():
    return sorted(p.parent.name for p in (ROOT / "pipeline").glob("*/step2b_place_index.py"))


def row_counter(index_bytes):
    ix = json.loads(index_bytes)
    return collections.Counter((ix["kinds"][r[0]], r[3]) for r in ix["rows"])


def row_diff(old_bytes, new_bytes, limit=12):
    """Lines naming the rows `new` adds and removes against `old`, by kind
    and name (a count where a name repeats)."""
    a, b = row_counter(old_bytes), row_counter(new_bytes)
    out = []
    for sign, c in (("+", b - a), ("-", a - b)):
        items = sorted(c.items())
        for (kind, name), n in items[:limit]:
            out.append(f"      {sign} {kind}: {name}" + (f" x{n}" if n > 1 else ""))
        if len(items) > limit:
            out.append(f"      {sign} ... and {len(items) - limit} more")
    return out


def at_rev(rev, path):
    rel = path.relative_to(ROOT).as_posix()
    proc = subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=ROOT, capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def check_city(city, against=None):
    """(status, lines): status is "ok", "drift", "skip" or "new"."""
    from pipeline import place_index
    config = importlib.import_module(f"pipeline.{city}.config")
    missing = [p for p in (config.PLACE_OSM_JSON, config.PLACE_OSM_EXTRA_JSON) if not p.exists()]
    if missing:
        return "skip", [f"      no cache: {', '.join(p.name for p in missing)} "
                        f"(python pipeline/place_index_fetch.py {city})"]
    index, _ = place_index.build_city(config)
    built = place_index.files(index, city)
    lines, drift = [], False
    ipath = place_index.index_path(city)
    for path, data in built.items():
        old = at_rev(against, path) if against else (path.read_bytes() if path.exists() else None)
        if old is None:
            lines.append(f"      {path.relative_to(ROOT).as_posix()}: none "
                         f"{'at ' + against if against else 'on disk'}")
            drift = True
        elif old != data:
            drift = True
            if path == ipath:
                lines += row_diff(old, data) or ["      index bytes differ, rows the same"]
            elif path == place_index.crossings_path(city):
                lines.append(f"      intersections: {len(json.loads(old)['rows']):,} -> "
                             f"{len(json.loads(data)['rows']):,}")
            else:
                lines.append(f"      {path.name} differs")
    if against and all(at_rev(against, p) is None for p in built):
        return "new", [f"      not searched at {against}"]
    return ("drift" if drift else "ok"), lines


def main(argv):
    against = None
    if "--against" in argv:
        i = argv.index("--against")
        against = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    cities = argv or searched_cities()
    unknown = [c for c in cities if c not in searched_cities()]
    if unknown:
        sys.exit(f"no pipeline/<city>/step2b_place_index.py for {unknown}")
    counts = collections.Counter()
    for city in cities:
        status, lines = check_city(city, against)
        counts["changed" if against and status == "drift" else status] += 1
        label = {"ok": "OK   ", "drift": "CHANGED" if against else "DRIFT", "skip": "SKIP ", "new": "NEW  "}[status]
        print(f"  {label} {city}")
        for line in lines:
            print(line)
    summary = ", ".join(f"{n} {k}" for k, n in sorted(counts.items()))
    if against:
        print(f"\n{summary} against {against}. Rows a rule changed in a built city go to the owner.")
        return 0
    if counts["drift"]:
        print(f"\n{summary}. Rebuild each drifting city's index (step2b_place_index.py), "
              f"then re-render its map once.")
        return 1
    print(f"\nOK - {summary}: every index on disk is what the current code builds from its cache.")
    return 0


def selftest():
    def ix(rows):
        return json.dumps({"kinds": ["station", "street"], "rows": rows}).encode("utf-8")
    a = ix([[0, 0, 0, "Gràcia", "", 0], [1, 0, 0, "Rue de Salon", "", 0], [1, 0, 0, "Court A", "", 0]])
    b = ix([[0, 0, 0, "Gràcia", "", 0], [1, 0, 0, "Rue de Salon", "", 0], [1, 0, 0, "Rue de Salon", "", 0]])
    cases = [
        ("identical indexes differ in nothing", row_diff(a, a), []),
        ("a removed row and a repeated name", row_diff(a, b),
         ["      + street: Rue de Salon", "      - street: Court A"]),
        ("the list is cut at the limit", row_diff(ix([]), a, limit=2)[-1], "      + ... and 1 more"),
    ]
    ok = 0
    for name, got, want in cases:
        good = got == want
        ok += good
        print(f"  {'ok ' if good else 'BAD'} {name}" + ("" if good else f": got {got!r}"))
    print(f"{ok} of {len(cases)} cases behaved as intended.")
    return 0 if ok == len(cases) else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1:]))
