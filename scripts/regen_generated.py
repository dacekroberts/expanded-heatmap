"""Regenerate every generated file from the merged sources, rather than merging
it by hand (owner, 2026-10-04: the efficiency review's first change).

    python scripts/regen_generated.py              # after any merge; prints what changed
    python scripts/regen_generated.py --install    # once per clone: the merge driver

WHY. In the week of 2026-09-27 the generated and counted files conflicted on
almost every build merge (docs/efficiency_review_2026-10-04.md, finding 1):
docs/city_master_list.md 57 merges, app/ring_shares.json 33,
app/macro_facts.json 14. Each is written by a script from other files, so a
hand resolution is work the script redoes. On 2026-10-04 three build branches
landed in one review time and conflicted on the same set every time.

HOW. `.gitattributes` marks the purely generated files `merge=regenerate`.
`--install` sets that driver to `true` in the repository's config (shared by
every worktree): git keeps the branch's own side and reports no conflict.
Then this script, run after the merge, rewrites each file from the merged
sources. The pre-push hook (check_all) fails any that is left stale, so a
skipped run cannot reach master. Its generators:

  app/macro_facts.json       scripts/check_macro_facts.py --write
  app/ring_shares.json       scripts/check_ring_shares.py --write
  docs/ring_rules.md         scripts/ring_rules_table.py --write
  docs/rendered_surfaces.md  scripts/rendered_surfaces.py --write
  README.md (city list)      scripts/readme_cities.py
  docs/city_master_list.md   scripts/check_master_list_counts.py --write (counts only)
  DECISIONS.md (its index)   scripts/decisions_index.py

The master list and README hold hand-written text too, so they keep normal
merges; only their generated counts and lists are rewritten here. Every
written file is converted to LF (Windows text-mode writes leave CRLF).
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATORS = [
    (["scripts/check_macro_facts.py", "--write"], "app/macro_facts.json"),
    (["scripts/check_ring_shares.py", "--write"], "app/ring_shares.json"),
    (["scripts/ring_rules_table.py", "--write"], "docs/ring_rules.md"),
    (["scripts/rendered_surfaces.py", "--write"], "docs/rendered_surfaces.md"),
    (["scripts/readme_cities.py"], "README.md"),
    (["scripts/check_master_list_counts.py", "--write"], "docs/city_master_list.md"),
    (["scripts/decisions_index.py"], "DECISIONS.md"),
]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def install():
    git("config", "merge.regenerate.name",
        "keep this side; scripts/regen_generated.py rewrites it after the merge")
    git("config", "merge.regenerate.driver", "true")
    print("merge.regenerate driver installed (repository config, every worktree).")


def main():
    if "--install" in sys.argv[1:]:
        install()
        return
    if not git("config", "--get", "merge.regenerate.driver").stdout.strip():
        print("note: the merge.regenerate driver is not installed; "
              "run `python scripts/regen_generated.py --install` once.")
    failed = []
    for cmd, target in GENERATORS:
        before = (ROOT / target).read_bytes() if (ROOT / target).exists() else b""
        res = subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        path = ROOT / target
        if path.exists():
            raw = path.read_bytes()
            if b"\r\n" in raw:
                path.write_bytes(raw.replace(b"\r\n", b"\n"))
        after = path.read_bytes() if path.exists() else b""
        if res.returncode != 0:
            failed.append(target)
            print(f"  FAILED   {target}: {' '.join(cmd)}\n{res.stdout[-600:]}{res.stderr[-600:]}")
        else:
            print(f"  {'rewritten' if after != before else 'current  '}  {target}")
    if failed:
        sys.exit(1)
    print("\nCommit any rewritten file with the merge.")


if __name__ == "__main__":
    main()
