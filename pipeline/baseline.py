"""Per-step row counts as data, so `drift_check` can diff them instead of
telling you to find them by eye.

WHY
---
`drift_check` compares the rendered OUTPUT FILES byte for byte, which catches a
map that changed and says nothing about a count that changed. Its own closing
line has been: *"Compare the step row counts above against the latest baseline
entry in DECISIONS.md."* By hand. Against a file that is now 5,400 lines and 103
entries.

That is the wrong shape of work, and it hides the exact failure this project
keeps having: **a count can move without an output file looking wrong.** A
filter that silently starts dropping 2,000 more rows still renders a plausible
map.

HOW
---
A step emits one line per figure worth watching:

    from pipeline.baseline import emit
    emit("storefront_rows", len(df))
    emit("stations", len(kept))

which prints `##BASELINE storefront_rows=19575`. `drift_check` collects those,
compares them against `outputs/<city>/baseline.json`, and reports any that
moved. `--update-baseline` rewrites the file, which is what to run when a
change to the counts is intended.

The marker is a printed line rather than a return value because steps are run
as subprocesses and their stdout is already captured - nothing else has to
change, and a step that never calls `emit()` simply has no baseline, which is
reported rather than treated as passing.

**Emit the figures a reader of the city page would care about**, not every
intermediate: rows in, rows after the storefront filter, per-bucket counts,
stations, geocode matches, pins plotted. Six to ten per city. A baseline with
forty entries is one nobody reads when it moves.
"""

import json
from pathlib import Path

MARKER = "##BASELINE"
ROOT = Path(__file__).parent.parent


def emit(key: str, value):
    """Record one figure for `drift_check` to watch. Prints, by design."""
    if not key or " " in key or "=" in key:
        raise ValueError(f"baseline key must be a bare identifier, got {key!r}")
    print(f"{MARKER} {key}={value}")


def parse(stdout: str) -> dict:
    """Pull every emitted figure out of a step's captured stdout."""
    found = {}
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith(MARKER):
            continue
        body = line[len(MARKER):].strip()
        if "=" not in body:
            continue
        key, _, value = body.partition("=")
        try:
            found[key.strip()] = int(value)
        except ValueError:
            found[key.strip()] = value.strip()
    return found


def path_for(city: str) -> Path:
    return ROOT / "outputs" / city / "baseline.json"


def load(city: str) -> dict | None:
    p = path_for(city)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def save(city: str, counts: dict) -> Path:
    p = path_for(city)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(counts, indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    return p


def compare(city: str, measured: dict):
    """Returns (ok, lines_to_print). Missing baseline is reported, not failed -
    a city that has never emitted one is a gap to fill, not a regression."""
    if not measured:
        return True, [f"  baseline: {city} emits none "
                      f"(add pipeline.baseline.emit() calls to its steps)"]
    stored = load(city)
    if stored is None:
        return True, [f"  baseline: none recorded for {city} yet - run "
                      f"drift_check --update-baseline to write "
                      f"outputs/{city}/baseline.json"]
    out, ok = [], True
    moved = {k: (stored.get(k), v) for k, v in measured.items()
             if k in stored and stored[k] != v}
    added = sorted(set(measured) - set(stored))
    gone = sorted(set(stored) - set(measured))
    if moved:
        ok = False
        out.append(f"  BASELINE MOVED ({len(moved)} of {len(measured)}):")
        for k, (was, now) in sorted(moved.items()):
            try:
                delta = f"  ({now - was:+,})"
            except TypeError:
                delta = ""
            out.append(f"     {k}: {was:,} -> {now:,}{delta}"
                       if isinstance(was, int) and isinstance(now, int)
                       else f"     {k}: {was} -> {now}{delta}")
    if added:
        out.append(f"  baseline: {len(added)} new figure(s) not yet recorded: "
                   f"{', '.join(added)}")
    if gone:
        ok = False
        out.append(f"  BASELINE FIGURE(S) NO LONGER EMITTED: {', '.join(gone)}")
    if ok and not out:
        out.append(f"  baseline: {len(measured)} figure(s) unchanged")
    return ok, out
