"""Before a worktree is removed: does its gitignored data/ hold anything the main checkout lacks?

    python scripts/check_worktree_data.py <worktree folder>          # refuses while anything would be lost
    python scripts/check_worktree_data.py <worktree folder> --list   # every such file, not only a summary

Exits non-zero while any file under <worktree>/data/ is missing from the main
checkout's data/, or is there with a different size, and names the folders it
is in. Read-only: it never copies, moves or deletes. Copy first (docs/session_roles.md,
"Before removing a worktree", step 2), then run it again until it passes.

WHY. `git worktree remove` deletes ignored files without asking, and data/ is
ignored. The retirement checklist already said to copy "any data/<city>/ the
main checkout lacks", and on 2026-09-27 a removed worktree took ~1.2 GB that
existed nowhere else: Japan's city registers, the national ISJ/N02/N03/e-Stat
files under data/japan and data/mhlw (not cities, so a per-city reading of the
rule skips them), and caches for unbuilt cities that no fetch_sources.py
re-creates. A sentence in a checklist is read past; a refusal is not. It
follows junctions' TARGETS only to compare sizes, and reports a junction as
such rather than walking into it.
"""

import argparse
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path


def main_checkout():
    """The main working tree: the first entry of `git worktree list`."""
    out = subprocess.run(["git", "worktree", "list", "--porcelain"], capture_output=True,
                         text=True, check=True).stdout
    return Path(out.splitlines()[0].split(" ", 1)[1])


def is_link(p):
    return p.is_symlink() or (hasattr(os.path, "isjunction") and os.path.isjunction(p))


def missing(worktree, main):
    """Yield (relative path, reason) for each data file main lacks or holds at another size."""
    root = worktree / "data"
    for dirpath, dirnames, filenames in os.walk(root):
        d = Path(dirpath)
        for name in list(dirnames):
            if is_link(d / name):
                dirnames.remove(name)  # a junction's target lives elsewhere; never walk into it
        for name in filenames:
            f = d / name
            rel = f.relative_to(worktree)
            other = main / rel
            if not other.exists():
                yield rel, "absent from main"
            elif other.stat().st_size != f.stat().st_size:
                yield rel, "different size in main"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("worktree", type=Path)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    wt, main_ = a.worktree.resolve(), main_checkout().resolve()
    if wt == main_:
        sys.exit("that is the main checkout itself - nothing to compare against")
    if not (wt / "data").is_dir():
        print(f"{wt}: no data/ folder - nothing ignored to lose here")
        return
    lost = list(missing(wt, main_))
    if not lost:
        print(f"OK - every file under {wt / 'data'} is also in {main_ / 'data'} at the same size")
        return
    size = sum((wt / r).stat().st_size for r, _ in lost)
    folders = Counter("/".join(r.parts[:2]) for r, _ in lost)
    print(f"REFUSE - {len(lost):,} file(s), {size / 1e6:,.1f} MB, under {wt / 'data'} would be lost:")
    for folder, n in folders.most_common():
        print(f"  {folder}: {n:,}")
    if a.list:
        for r, why in lost:
            print(f"    {r} ({why})")
    print("Copy them into the main checkout first (cp -rn, then diff -rq), and re-run this.")
    sys.exit(1)


if __name__ == "__main__":
    # A Windows console defaults to cp1252 and raises UnicodeEncodeError on
    # Hangul, Han and kana, and on Czech and Latvian letters (brief_check.py
    # crashed on a Korean claim, 2026-09-27). UTF-8 regardless of the console.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    main()
