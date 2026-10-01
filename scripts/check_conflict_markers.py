"""Find a git conflict marker left in a tracked file.

    python scripts/check_conflict_markers.py                     # every tracked text file
    python scripts/check_conflict_markers.py --file PATH [PATH ...]

WHY THIS FILE EXISTS. On 2026-09-30, on branch kitchener-waterloo,
`scripts/merge_append_only.py DECISIONS.md` failed on a Windows file lock
(OSError, Errno 22) and the merge was committed anyway, with `<<<<<<< HEAD`,
`=======` and `>>>>>>> origin/master` still in DECISIONS.md. The pre-push hook
passed it 26 of 26: no check read for markers, and `decisions_index.py --check`
only compares headings to the index, which a conflict leaves intact. It was
found by eye and removed in 3d93d29. A marker breaks whatever reads the file -
a Python module will not import, a JSON or CSV will not parse, a doc renders
both sides - and an append-only log gives no other sign of it.

THE SHAPE. git writes a conflict as a line starting `<<<<<<< ` (ours), an
optional `||||||| ` (the base, under merge.conflictStyle=diff3), a bare
`=======`, and a line starting `>>>>>>> ` (theirs). An opening or closing
marker fails wherever it is, so half of a conflict left behind still fails. A
bare `=======` fails only between an opening and a closing marker, because
outside one it is a Markdown heading underline.

SCOPE. Every file `git ls-files` names, except under data/ (gitignored apart
from a few seeds, and not text this project writes by hand), read from the
WORKING TREE as check_all.py does. A file with a NUL byte in its first 8 KB is
binary and skipped. Documenting a marker? Indent it or put it mid-line; only a
marker at the start of a line counts.

Exit 1 naming each file and line, 0 otherwise.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = ("data/",)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OPEN = re.compile(r"<{7}(?: |$)")
BASE = re.compile(r"\|{7}(?: |$)")
SEP = re.compile(r"={7}$")
CLOSE = re.compile(r">{7}(?: |$)")


def markers(text):
    """-> [(line number, line)] for every conflict-marker line in text."""
    found, inside = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if OPEN.match(line):
            found.append((n, line))
            inside = True
        elif CLOSE.match(line):
            found.append((n, line))
            inside = False
        elif inside and (BASE.match(line) or SEP.match(line)):
            found.append((n, line))
    return found


def tracked():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True)
    if out.returncode:
        raise SystemExit(f"git ls-files failed: {out.stderr.decode(errors='replace').strip()}")
    names = [n for n in out.stdout.decode("utf-8", "replace").split("\0") if n]
    return [n for n in names if not n.startswith(EXCLUDE)]


def scan(path):
    try:
        raw = path.read_bytes()
    except FileNotFoundError:        # tracked but deleted in the working tree
        return None
    if b"\0" in raw[:8192]:
        return None
    if b"<<<<<<<" not in raw and b">>>>>>>" not in raw:
        return []                    # the fast path for 200 MB of rendered maps
    return markers(raw.decode("utf-8", "replace"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--file", nargs="+", metavar="PATH",
                    help="check these files instead of every tracked one")
    args = ap.parse_args()

    names = args.file or tracked()
    if not names:
        print("FAIL - git ls-files named no files; nothing was checked")
        return 1

    checked, bad = 0, {}
    for name in names:
        path = Path(name) if args.file else ROOT / name
        found = scan(path)
        if found is None:
            continue
        checked += 1
        if found:
            bad[name] = found

    for name, found in bad.items():
        for n, line in found:
            print(f"{Path(name).as_posix()}:{n}: conflict marker {line[:60]!r}")
    if bad:
        total = sum(len(f) for f in bad.values())
        print(f"FAIL - {total} conflict-marker line(s) in {len(bad)} file(s). "
              f"Finish the merge (DECISIONS.md: scripts/merge_append_only.py) "
              f"before committing.")
        return 1
    print(f"OK - no conflict markers in {checked} tracked text file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
