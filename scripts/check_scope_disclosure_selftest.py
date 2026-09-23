"""Watch scripts/check_scope_disclosure.py fail, eight ways.

    python scripts/check_scope_disclosure_selftest.py

WHY THIS FILE EXISTS, when five of the six checks here have no self-test. This
one's vocabulary is DESIGNED to be edited by a later session: every city that
arrives with an unfamiliar exclusion shape widens it. Marseille forced exactly
that within an hour of the check existing - `commune` added to the boundary
columns, and a new reason pattern for "Aubagne's tram, not Marseille's". The
edits land in `app/station_scope.py`, which the LIVE PAGE imports to build its
station table, so a session widening the classifier to make the check pass can
quietly change what readers are shown. An edit is when a silent break happens,
and this check has a predictable future editor.

NOTHING IN THE REPOSITORY IS MODIFIED. Every case copies what the check reads
into a temporary tree, breaks the copy, and runs the check there with `--root`.

TWO TRAPS THIS FILE IS BUILT AROUND, both met for real on 2026-09-23:

  * **The fixture must be complete, or every case fails for the wrong reason.**
    The scratchpad ancestor of this file copied `app/cities.py` and not
    `app/station_scope.py`, so all eight cases died on an ImportError. It read
    as a strict check rather than a broken harness, and only the positive
    control at the end said otherwise. Hence `app/*.py` wholesale below: a
    third module must not be able to repeat it.
  * **A subprocess's output is BYTES.** This check prints city names, and
    "Montréal" leaves a piped Python on Windows in the console codepage; a
    strict UTF-8 decode raises and hands back an EMPTY stdout, which reads as
    "the expected text was not found". That produced two false failures in one
    session, so the child is forced to UTF-8 AND decoded with
    `errors="replace"`.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "check_scope_disclosure.py"
DOC = "docs/excluded_categories.md"


def build_tree(dest):
    """Everything the check reads: itself, the app modules it imports, the
    document, and every city's outputs directory."""
    (dest / "scripts").mkdir(parents=True)
    shutil.copy2(CHECK, dest / "scripts" / CHECK.name)

    # EVERY top-level app module, not a named list - see the fixture trap above.
    (dest / "app").mkdir()
    for src in sorted((ROOT / "app").glob("*.py")):
        shutil.copy2(src, dest / "app" / src.name)

    (dest / "docs").mkdir()
    shutil.copy2(ROOT / DOC, dest / DOC)

    # The directory has to exist even where there is no file: its absence is
    # what property C fails on, so a missing one would pass every case.
    for city_dir in sorted(p for p in (ROOT / "outputs").iterdir() if p.is_dir()):
        out = dest / "outputs" / city_dir.name
        out.mkdir(parents=True)
        csv_path = city_dir / "excluded_stations.csv"
        if csv_path.exists():
            shutil.copy2(csv_path, out / csv_path.name)
    return dest


def run(root):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run(
        [sys.executable, str(root / "scripts" / CHECK.name), "--root", str(root)],
        cwd=ROOT, capture_output=True, env=env)          # bytes, decoded below
    out = ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8",
                                                        errors="replace")
    return r.returncode, out


def edit(rel, mutate):
    """A case that rewrites one file's text, refusing a no-op mutation."""
    def apply(root):
        path = root / rel
        text = path.read_text(encoding="utf-8")     # normalises CRLF
        changed = mutate(text)
        if changed == text:
            return False
        path.write_text(changed, encoding="utf-8")
        return True
    return apply


def append(rel, line):
    def apply(root):
        path = root / rel
        path.write_text(path.read_text(encoding="utf-8") + line,
                        encoding="utf-8")
        return True
    return apply


def rename_outputs(name, to):
    def apply(root):
        (root / "outputs" / name).rename(root / "outputs" / to)
        return True
    return apply


def drop_from_business_half(city):
    """Remove a city's name only AFTER the business heading.

    Editing the whole document would also strip it from the station half, and
    the case is specifically that being named in the transit half is not
    enough - "Cercanías in Madrid" says nothing about Madrid's businesses.
    """
    def apply(root):
        path = root / DOC
        head, marker, tail = path.read_text(encoding="utf-8").partition(
            "## Which businesses are counted")
        if not marker or city not in tail:
            return False
        path.write_text(head + marker + tail.replace(city, "that city"),
                        encoding="utf-8")
        return True
    return apply


def stale_known_gap(city):
    """A city that IS documented, still listed as a dated gap, must fail."""
    def apply(root):
        path = root / "scripts" / CHECK.name
        text = path.read_text(encoding="utf-8")
        if "KNOWN_GAPS = {}" not in text:
            return False
        path.write_text(
            text.replace("KNOWN_GAPS = {}",
                         "KNOWN_GAPS = {" + repr(city) + ": '2026-09-23'}", 1),
            encoding="utf-8")
        return True
    return apply


def no_cities_at_all(root):
    """An empty city list must not pass vacuously.

    The sibling self-test's best case is a glob narrowed to match nothing,
    which "passes every assertion ever written". The same hole exists here:
    with no cities, properties C, D and E examine nothing at all.
    """
    path = root / "app" / "cities.py"
    text = path.read_text(encoding="utf-8")
    if "\nCITIES = [" not in text:
        return False
    path.write_text(text + "\n\nCITIES = []\n", encoding="utf-8")
    return True


CASES = [
    ("the heading the station table splices at, removed",
     edit(DOC, lambda t: t.replace("## Which businesses are counted",
                                   "## Businesses", 1)),
     "spliced at appears 0"),

    ("that heading duplicated, so the split is ambiguous",
     append(DOC, "\n\n## Which businesses are counted\n"),
     "appears 2 times"),

    ("the station-scope section removed entirely",
     edit(DOC, lambda t: t.replace(
         "## Which stations these maps are drawn around", "## Some notes", 1)),
     "Transit scope would be undisclosed"),

    ("a city's outputs/ directory renamed, emptying its table row",
     rename_outputs("san_francisco", "sf"),
     "renders empty"),

    ("a city named only in the transit half, not the business half",
     drop_from_business_half("Milan"),
     "named nowhere in the business half"),

    ("a station excluded for a reason neither reader understands",
     append("outputs/san_francisco/excluded_stations.csv",
            "Somewhere,J,37.7,-122.4,a brand new kind of reason,X,0.1\n"),
     "neither a spacing filter nor a boundary"),

    ("a documented city left stale in KNOWN_GAPS",
     stale_known_gap("Milan"),
     "Remove it from KNOWN_GAPS"),

    ("no cities at all - the vacuous pass",
     no_cities_at_all,
     "no cities"),
]


def case(label, mutate, expect_in, expect_code=1):
    with tempfile.TemporaryDirectory() as tmp:
        root = build_tree(Path(tmp))
        if not mutate(root):
            print(f"BROKEN TEST  {label}\n      the mutation matched nothing, "
                  f"so this case proves nothing about the check")
            return False
        code, out = run(root)
        hit = [ln for ln in out.splitlines() if expect_in in ln]
        ok = code == expect_code and hit
        print(f"{'PASS' if ok else 'DID NOT FAIL'}  {label}")
        print(f"      exit {code} (wanted {expect_code}); "
              f"{hit[0].strip() if hit else 'expected text not found'}")
        return bool(ok)


def main():
    print(f"Self-test for {CHECK.relative_to(ROOT).as_posix()}\n")
    results = [case(*c) for c in CASES]

    # THE POSITIVE CONTROL, and it is not a formality: it is what distinguishes
    # "the check fires on everything" from "the harness is broken".
    with tempfile.TemporaryDirectory() as tmp:
        code, out = run(build_tree(Path(tmp)))
    clean = code == 0
    print(f"\n{'PASS' if clean else 'FAIL'}  an unmodified copy passes "
          f"(exit {code})")
    if not clean:
        print("      " + " | ".join(out.strip().splitlines()[:3]))

    failed = len([r for r in results if not r]) + (0 if clean else 1)
    print(f"\n{len(results) + 1 - failed} of {len(results) + 1} cases behaved "
          f"as intended.")
    if failed:
        print("\nA case that did not fail means the check does not decide what "
              "it claims to, OR that this self-test's expectation went stale "
              "when the check legitimately changed. Read which before 'fixing' "
              "either. If EVERY case failed, suspect this harness first - an "
              "incomplete fixture fails them all identically.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
