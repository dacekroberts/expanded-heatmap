"""Watch scripts/check_conflict_markers.py catch a conflict, and pass look-alikes.

    python scripts/check_conflict_markers_selftest.py

WHY. The check is only worth having if it fails on the shape that reached a
commit on 2026-09-30 (DECISIONS.md with all three markers, see the check's
docstring) and passes the shapes that merely resemble it, above all a Markdown
heading underlined with `=======`, which this repository's docs are free to
use. So each case is a small file with a known answer, checked for
its EXPECTED MESSAGE and not just its exit code; one case splices a conflict
into a copy of the live DECISIONS.md; and the positive control runs the real
scope, which must pass.

NOTHING IN THE REPOSITORY IS MODIFIED: every case is a temporary file.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "check_conflict_markers.py"
LIVE = ROOT / "DECISIONS.md"

# Built from pieces so that no line of THIS file starts with a marker.
O, B, S, C = "<" * 7, "|" * 7, "=" * 7, ">" * 7
CLEAN = "OK - no conflict markers"


def lines(*rows):
    return "".join(r + "\n" for r in rows)


# (label, file text, expected flagged line numbers; empty means it passes)
CASES = [
    ("a whole conflict, as committed on 2026-09-30",
     lines("### A", O + " HEAD", "### ours", S, "### theirs", C + " origin/master", "end"),
     [2, 4, 6]),
    ("a diff3 conflict with its base section",
     lines(O + " HEAD", "x = 1", B + " merged common ancestors", "x = 0", S, "x = 2", C + " topic"),
     [1, 3, 5, 7]),
    ("half a conflict: the closing marker left behind",
     lines("kept", S, "also kept", C + " origin/master"),
     [4]),
    ("half a conflict: the opening marker left behind",
     lines(O + " HEAD", "kept"),
     [1]),
    ("a CRLF file",
     (lines(O + " HEAD", "a", S, "b", C + " x")).replace("\n", "\r\n"),
     [1, 3, 5]),
    ("a Markdown heading underlined with =======",
     lines("Title", S, "", "Body."), []),
    ("a marker indented, as in a doc that quotes one",
     lines("    " + O + " HEAD", "    " + S, "    " + C + " x"), []),
    ("a marker mid-line, as in a docstring",
     lines('OURS = "' + O + ' "', 'THEIRS = "' + C + ' "'), []),
    ("eight angle brackets are not git's seven",
     lines(O + "< not a marker", C + "> nor this"), []),
]


def run(*args):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, str(CHECK), *args], cwd=ROOT,
                       capture_output=True, env=env)
    return r.returncode, ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8", "replace")


def check_case(tmp, label, text, want):
    path = Path(tmp) / "case.md"
    path.write_bytes(text.encode("utf-8"))
    rc, out = run("--file", str(path))
    got = sorted(int(line.split(":")[-2]) for line in out.splitlines()
                 if ": conflict marker " in line)
    if want:
        ok = rc == 1 and got == want and "FAIL - " in out
    else:
        ok = rc == 0 and not got and CLEAN in out
    print(f"{'ok  ' if ok else 'FAIL'} {label}")
    if not ok:
        print(f"     want lines {want}, exit {1 if want else 0}; got {got}, exit {rc}")
        print("     " + out.strip().replace("\n", "\n     "))
    return ok


def main():
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        for label, text, want in CASES:
            results.append(check_case(tmp, label, text, want))

        live = LIVE.read_text(encoding="utf-8").splitlines(keepends=True)
        at = len(live) // 2
        spliced = "".join(live[:at] + [lines(O + " HEAD", "### ours", S, "### theirs",
                                              C + " origin/master")] + live[at:])
        results.append(check_case(tmp, "a conflict spliced into the live DECISIONS.md",
                                  spliced, [at + 1, at + 3, at + 5]))

    rc, out = run()
    ok = rc == 0 and CLEAN in out
    print(f"{'ok  ' if ok else 'FAIL'} positive control: the real tracked files pass")
    if not ok:
        print("     " + out.strip().replace("\n", "\n     "))
    results.append(ok)

    passed = sum(results)
    print(f"\n{passed} of {len(results)} cases as expected.")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
