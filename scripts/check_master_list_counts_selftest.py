"""Watch scripts/check_master_list_counts.py fail, thirteen ways.

    python scripts/check_master_list_counts_selftest.py

WHY THIS FILE EXISTS. The check reads a document that sessions rewrite every
day, through heuristics about its shape (which tables are city tables, which
headings are city write-ups). A check like that fails in the quiet direction:
a reshaped band stops being recognised, its members count as zero, and - if the
heading's count happened to be edited the same way - nothing is reported. The
only evidence that it still decides anything is watching it refuse a file that
is wrong in each way it claims to catch, and pass the real one.

NOTHING IN THE REPOSITORY IS MODIFIED. Every case copies the live
`docs/city_master_list.md` into a temporary file, breaks the copy with one
exact text replacement, and runs the check there with `--file`. A replacement
that matches nothing is reported as a BROKEN TEST rather than a pass: the live
file has moved on and the case must be re-aimed, or it proves nothing.

The child's output is BYTES, forced to UTF-8 and decoded with
`errors="replace"` - city names such as "Liepāja" and "Göteborg" otherwise come
back empty through a Windows console codepage and read as "expected text not
found" (the trap check_scope_disclosure_selftest.py met twice).
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "check_master_list_counts.py"
LIST = ROOT / "docs" / "city_master_list.md"


def run(path):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, str(CHECK), "--file", str(path)],
                       cwd=ROOT, capture_output=True, env=env)
    out = ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8", errors="replace")
    return r.returncode, out


def swap(old, new):
    """A mutation replacing the FIRST occurrence of `old`, refusing a no-op."""
    def apply(text):
        return text.replace(old, new, 1) if old in text else None
    return apply


def drop_bands(text):
    """Every band heading renamed: an unrecognised file must not pass."""
    out = text.replace("## 🟢 Band A", "## 🟢 Group A").replace("## 🟣 Band C", "## 🟣 Group C")
    out = out.replace("## 🟤 Band T", "## 🟤 Group T").replace("## 🔴 Band D", "## 🔴 Group D")
    return out if out != text else None


CASES = [
    ("a band heading's count drifted (C 13 -> 14)",
     swap("(13 cities)", "(14 cities)"), "Band C holds"),

    ("the summary box's band count drifted (C 13 -> 12)",
     swap("· C 13 ·", "· C 12 ·"), "summary says C 12"),

    ("the summary box's discard count drifted",
     swap("| **Discarded** | **33**", "| **Discarded** | **34**"), "summary says discarded 34"),

    ("the summary box's country count drifted",
     swap("across 16 countries", "across 15 countries"), "across 15 countries"),

    ("Band A's built figure drifted in its heading",
     swap("ready + 32 ✅ BUILT", "ready + 31 ✅ BUILT"), "says 31 built"),

    ("the band table's count drifted (T 32 -> 33)",
     swap("| **32** *(the 2026-09-27 second-city screens)*",
          "| **33** *(the 2026-09-27 second-city screens)*"), "band table says T 33"),

    ("the candidate total drifted in its heading",
     swap("## Candidates — 64", "## Candidates — 65"), "but the bands hold 64"),

    ("the Built heading drifted",
     swap("## Built — 46", "## Built — 47"), "the Built table lists 46"),

    ("a Built row's per-country count drifted",
     swap("**Canada** (5, complete)", "**Canada** (6, complete)"), "lists 5 cities"),

    ("a sub-group count drifted (France 21 -> 22)",
     swap("**🇫🇷 France (21)**", "**🇫🇷 France (22)**"), "the table below it has 21 rows"),

    ("a city in two bands (a Band D row renamed to Band T's Brno)",
     swap("| **Gimhae** 🇰🇷 |", "| **Brno** 🇰🇷 |"), "Brno is in Band D AND Band T"),

    ("a built city still listed in a band (Band T's Avignon renamed Rennes)",
     swap("| Avignon |", "| Rennes |"), "is in Built AND Band T"),

    ("no band recognised at all - the vacuous pass",
     drop_bands, "no '## ... Band X' sections"),
]


def case(label, mutate, expect_in, text, tmp):
    changed = mutate(text)
    if changed is None or changed == text:
        print(f"BROKEN TEST  {label}\n      the mutation matched nothing in the live "
              f"file, so this case proves nothing - re-aim it")
        return False
    path = Path(tmp) / "city_master_list.md"
    path.write_text(changed, encoding="utf-8", newline="\n")
    code, out = run(path)
    hit = [ln for ln in out.splitlines() if expect_in in ln]
    ok = code == 1 and bool(hit)
    print(f"{'PASS' if ok else 'DID NOT FAIL'}  {label}")
    print(f"      exit {code} (wanted 1); "
          f"{hit[0].strip()[:150] if hit else 'expected text not found: ' + expect_in!r}")
    return ok


def main():
    print(f"Self-test for {CHECK.relative_to(ROOT).as_posix()}\n")
    text = LIST.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        results = [case(*c, text, tmp) for c in CASES]

        # THE POSITIVE CONTROL: an unmodified copy must pass. Without it, a
        # check that fails on everything would pass every case above.
        path = Path(tmp) / "city_master_list.md"
        path.write_text(text, encoding="utf-8", newline="\n")
        code, out = run(path)
    clean = code == 0
    print(f"\n{'PASS' if clean else 'FAIL'}  an unmodified copy passes (exit {code})")
    if not clean:
        print("      " + " | ".join(out.strip().splitlines()[:3]))

    failed = results.count(False) + (0 if clean else 1)
    print(f"\n{len(results) + 1 - failed} of {len(results) + 1} cases behaved as intended.")
    if failed:
        print("\nA case that did not fail means the check does not decide what it claims "
              "to, OR the live file changed so the case's text no longer exists. If the "
              "positive control failed, the live file itself has a drifted count: run "
              "check_master_list_counts.py and fix the file first.")
    return 1 if failed else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
