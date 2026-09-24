"""Find files dropped into a checkout's ROOT that nobody meant to put there.

    python scripts/check_stray_downloads.py

Lists every untracked, non-ignored file sitting directly in the root of ANY
checkout of this repository - the main one and every worktree - with its size
and modification time, and exits non-zero if there is one. Read-only.

WHY A CHECK AND NOT A RULE. CLAUDE.md already says probe output goes to the
session scratchpad or a gitignored data/<city>/raw/, and on 2026-09-23 three
PDFs still landed in the main checkout's root: Rio's SIURB decree, data.taipei's
user manual and PID's logo manual. None was written by a shell command a rule
could have caught. They were BROWSER-PANE DOWNLOADS, answered by the owner at a
prompt while away from the desktop, and the pane saves into the main checkout's
root whatever folder the session meant to use (the Staging Session's diagnosis).
No working rule reaches a download dialog, so the only place to catch one is
afterwards. Two of the three had no recorded source URL by the time anyone
looked, which is the cost of finding them late.

WHY ONLY THE ROOT. Untracked files deeper in a worktree are usually a build in
progress - a new city's pipeline before its first commit - and flagging them
would make this cry wolf. New files at the root are almost never intended:
everything the project keeps there is already tracked.

Where a found file belongs is a judgment, not a rule - see
docs/licenses/README.md for terms documents (unaltered, with source URL and
SHA-256), data/<city>/raw/ for reference captures, and ask the session that
downloaded it before moving anything it may still be reading.
"""

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args, cwd=ROOT):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, check=True).stdout


def checkouts():
    """Every checkout of this repository: the main one first, then worktrees."""
    out = git("worktree", "list", "--porcelain").decode("utf-8", "replace")
    return [Path(line[len("worktree "):]) for line in out.splitlines()
            if line.startswith("worktree ")]


def stray_at_root(checkout):
    """Untracked, non-ignored files directly in `checkout`'s root."""
    raw = git("status", "--porcelain=v1", "-z", "--untracked-files=normal", cwd=checkout)
    found = []
    for entry in raw.decode("utf-8", "replace").split("\0"):
        if not entry.startswith("?? "):
            continue
        name = entry[3:]
        # `normal` collapses an untracked directory to "dir/"; a directory at
        # the root is as unexpected as a file, so it is reported too.
        if "/" in name.rstrip("/"):
            continue
        found.append(checkout / name)
    return found


def main():
    total = 0
    for checkout in checkouts():
        if not checkout.exists():
            print(f"  (listed but missing on disk: {checkout} - run `git worktree prune`)")
            continue
        stray = stray_at_root(checkout)
        total += len(stray)
        for p in stray:
            try:
                st = p.stat()
                when = time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))
                size = f"{st.st_size:,} bytes" if p.is_file() else "directory"
            except OSError:
                when, size = "?", "?"
            print(f"  STRAY  {p}  ({size}, {when})")
    if total:
        print(f"\n{total} untracked file(s) at a checkout root. Identify each, find the "
              f"session that saved it, and file it (see this script's docstring).")
        sys.exit(1)
    print(f"OK - no untracked files at the root of any of {len(checkouts())} checkouts.")


if __name__ == "__main__":
    main()
