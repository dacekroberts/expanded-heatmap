"""Watch scripts/check_master_list_counts.py fail, seventeen ways.

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
import re
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


def bump(pattern, expect):
    """A mutation adding 1 to the count captured by `pattern`, whatever it is now.

    The counts cases used to name the number ("**33**" -> "**34**"), so every
    legitimate change to the list - five discards added, Kansas City moved to
    Band T, both on 2026-09-27 - broke the self-test and with it the pre-push
    hook. Reading the current number keeps each case aimed. `expect` may use
    {old} and {new}.
    """
    rx = re.compile(pattern, re.M)

    def apply(text):
        m = rx.search(text)
        if not m:
            return None
        old = int(m.group(1))
        apply.expect = expect.format(old=old, new=old + 1)
        return text[:m.start(1)] + str(old + 1) + text[m.end(1):]
    return apply


def drop_bands(text):
    """Every band heading renamed: an unrecognised file must not pass."""
    out = text.replace("## 🟢 Band A", "## 🟢 Group A").replace("## 🟣 Band C", "## 🟣 Group C")
    out = out.replace("## 🟤 Band T", "## 🟤 Group T").replace("## 🔴 Band D", "## 🔴 Group D")
    return out if out != text else None


CASES = [
    ("a band heading's count drifted (Band C, +1)",
     bump(r"^## 🟣 Band C —[^\n]*?\((\d+) cities\)", "Band C holds"), None),

    ("the summary box's band count drifted (C, +1)",
     bump(r"· C (\d+) ·", "summary says C {new}"), None),

    ("the summary box's discard count drifted",
     bump(r"\| \*\*Discarded\*\* \| \*\*(\d+)\*\*", "summary says discarded {new}"), None),

    ("the summary box's country count drifted",
     bump(r"across (\d+) countries", "across {new} countries"), None),

    ("Band A's built figure drifted in its heading",
     bump(r"ready \+ (\d+) ✅ BUILT", "says {new} built"), None),

    ("the band table's count drifted (T, +1)",
     bump(r"^\| 🟤 \*\*T\*\* \|.*\| \*\*(\d+)\*\*", "band table says T {new}"), None),

    ("the candidate total drifted in its heading",
     bump(r"^## Candidates — (\d+)", "but the bands hold {old}"), None),

    ("the Built heading drifted",
     bump(r"^## Built — (\d+)", "the Built table lists {old}"), None),

    ("a Built row's per-country count drifted",
     bump(r"\*\*Canada\*\* \((\d+), complete\)", "lists {old} cities"), None),

    ("a sub-group count drifted (France, +1)",
     bump(r"\*\*🇫🇷 France \((\d+)\)\*\*", "the table below it has {old} rows"), None),

    ("by country: a row's Candidates figure drifted",
     bump(r"^\| 🇨🇦 Canada \| \*\*\d+\*\* \| \*\*(\d+)\*\*", "the Candidates column sums to"),
     None),

    ("by country: a row's Built figure disagrees with the Built table",
     bump(r"^\| 🇨🇦 Canada \| \*\*(\d+)\*\*", "says {new} built, the Built table lists {old}"),
     None),

    ("by country: the Total row's band figure drifted",
     bump(r"^\| \*\*Total\*\*.*· C (\d+) ·", "the Total row says C {new}"), None),

    ("by country: a named city is not in the band its row lists",
     swap("| **1** — Ottawa | C |", "| **1** — Ottawa | T |"), "its Bands column says"),

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
    expect_in = getattr(mutate, "expect", None) or expect_in
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
