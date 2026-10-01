"""Watch scripts/check_stray_bullets.py catch a stray bullet, and pass real lists.

    python scripts/check_stray_bullets_selftest.py

WHY. The check decides by the shape of the line before a dash, and a rule
like that is easy to get wrong in either direction: too loose and it passes
the wrap found on 2026-09-27, too tight and it fails every list that follows
a lead-in sentence. So each case is a small
document with a known answer, checked for its EXPECTED MESSAGE and not just
its exit code; one case re-creates the real defect in a copy of the live
docs/excluded_categories.md; and the positive control runs the real scope.

NOTHING IN THE REPOSITORY IS MODIFIED: every case is a temporary file.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "check_stray_bullets.py"
LIVE = ROOT / "docs" / "excluded_categories.md"

FLAGGED = "renders as a stray bullet"
CLEAN = "OK - no stray bullet"

# (label, document, expected text) - a flagged case names its line number.
CASES = [
    ("a sentence wrapped just before its dash",
     "Intro.\n\nThe city counts its shops\n- and its cafes, by address.\n",
     f"md:4: this line {FLAGGED}"),
    ("the same wrap inside a blockquote",
     "> The city counts its shops\n> - and its cafes, by address.\n",
     f"md:2: this line {FLAGGED}"),
    ("a '* ' dash after a line ending on a comma",
     "It keeps shops, cafes,\n* and salons.\n",
     f"md:2: this line {FLAGGED}"),
    ("a list after a blank line",
     "The buckets are these.\n\n- Retail\n- Food\n", CLEAN),
    ("a list after a lead-in ending ':'",
     "Three buckets are counted:\n- Retail\n- Food\n", CLEAN),
    ("a list after a bold lead-in",
     "**What they say**\n- Retail\n- Food\n", CLEAN),
    ("a list item's wrapped continuation, then the next item",
     "- Retail, which counts\n  every shop\n- Food\n", CLEAN),
    ("a dash inside a fenced block",
     "Run it like this\n```\n- not a list\n```\n", CLEAN),
    ("a dash indented four spaces (a continuation, not a list)",
     "The city counts its shops\n    - and its cafes.\n", CLEAN),
]


def run(*args):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, str(CHECK), *args], cwd=ROOT,
                       capture_output=True, env=env)
    return r.returncode, ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8", "replace")


def verdict(label, code, out, expect):
    want = 1 if expect != CLEAN else 0
    hit = [ln for ln in out.splitlines() if expect in ln]
    ok = code == want and bool(hit)
    print(f"{'PASS' if ok else 'WRONG'}  {label}")
    print(f"      exit {code} (wanted {want}); "
          f"{hit[0].strip()[:120] if hit else 'expected text not found: ' + expect!r}")
    return ok


def live_wrap(text):
    """The 2026-09-27 defect re-created: the first line in the live doc with a
    spaced dash mid-line, in a paragraph that opens as prose, wrapped so the
    dash starts the next line. Returns (document, number of the dash line) or None."""
    lines = text.split("\n")
    fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        first = i
        while first and lines[first - 1].strip():
            first -= 1
        if fence or not line[:1].isalpha() or not lines[first][:1].isalpha():
            continue
        m = re.search(r"\w - \w", line)
        if m:
            head, tail = line[:m.start() + 1], line[m.start() + 2:]
            return "\n".join(lines[:i] + [head, tail] + lines[i + 1:]), i + 2
    return None


def main():
    print(f"Self-test for {CHECK.relative_to(ROOT).as_posix()}\n")
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        for k, (label, doc, expect) in enumerate(CASES):
            path = Path(tmp) / f"case{k}.md"
            path.write_text(doc, encoding="utf-8", newline="\n")
            results.append(verdict(label, *run("--file", str(path)), expect))

        wrapped = live_wrap(LIVE.read_text(encoding="utf-8"))
        label = "the real defect, re-created in a copy of excluded_categories.md"
        if wrapped is None:
            print(f"BROKEN TEST  {label}\n      no prose line with a spaced dash found - "
                  "re-aim live_wrap()")
            results.append(False)
        else:
            path = Path(tmp) / "excluded_categories.md"
            path.write_text(wrapped[0], encoding="utf-8", newline="\n")
            results.append(verdict(label, *run("--file", str(path)),
                                   f"md:{wrapped[1]}: this line {FLAGGED}"))

    # The scope is derived from app/, so check it still finds the two pages' docs.
    code, out = run("--list")
    scope = code == 0 and all(d in out.splitlines() for d in
                              ("docs/data_sources.md", "docs/excluded_categories.md"))
    print(f"{'PASS' if scope else 'WRONG'}  the scope read from app/ holds the About "
          f"and What Is Excluded docs (exit {code})")
    results.append(scope)

    # THE POSITIVE CONTROL: the real scope passes. Without it, a check that
    # failed on everything would pass every flagged case above.
    code, out = run()
    clean = code == 0 and CLEAN in out
    print(f"\n{'PASS' if clean else 'FAIL'}  the documents the app renders pass (exit {code})")
    if not clean:
        print("      " + " | ".join(out.strip().splitlines()[:3]))

    failed = results.count(False) + (0 if clean else 1)
    print(f"\n{len(results) + 1 - failed} of {len(results) + 1} cases behaved as intended.")
    if failed and not clean:
        print("\nIf only the positive control failed, a rendered doc has a stray bullet: "
              "run check_stray_bullets.py and move the dash up a line.")
    return 1 if failed else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
