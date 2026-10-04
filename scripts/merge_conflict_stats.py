"""Count which merges on origin/master conflicted, and on which files, by
re-merging each merge's two parents with `git merge-tree` (exact, not read
from commit messages).

    python scripts/merge_conflict_stats.py                 # the last 7 days
    python scripts/merge_conflict_stats.py --since 2026-09-27 [--until 2026-10-04]

Read-only (merge-tree writes no ref and touches no working tree); run
`git fetch` first. The efficiency review's evidence for its first finding
(docs/efficiency_review_2026-10-04.md: the generated files conflicted on
every build merge); the `efficiency-review` skill runs it each round.

A merge whose subject names origin/master counts as a catch-up (a branch
taking master in), as scripts/efficiency_metrics.py counts it.
"""
import argparse
import collections
import datetime as dt
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCH = ("DECISIONS.md", "docs/city_master_list.md", "app/cities.py",
         "app/ring_shares.json", "app/macro_facts.json")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def main():
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default=(dt.date.today() - dt.timedelta(days=7)).isoformat())
    ap.add_argument("--until", default=None)
    args = ap.parse_args()
    cmd = ["log", "origin/master", "--merges", "--date=short",
           "--format=%h|%cd|%p|%s", f"--since={args.since}T00:00"]
    if args.until:
        cmd.append(f"--until={args.until}T23:59")
    rows = git(*cmd).stdout.splitlines()

    by_file, by_day, merges_day, by_day_file = (collections.Counter() for _ in range(4))
    conflicted = catch_up = 0
    for row in rows:
        sha, day, parents, subject = row.split("|", 3)
        merges_day[day] += 1
        ps = parents.split()
        if len(ps) != 2:
            continue
        res = git("merge-tree", "--write-tree", "--name-only", "--no-messages", *ps)
        if res.returncode != 1:     # 0 clean; anything else is not a conflict
            continue
        conflicted += 1
        by_day[day] += 1
        catch_up += "origin/master" in subject
        for f in {l for l in res.stdout.splitlines()[1:] if l.strip()}:
            by_file[f] += 1
            by_day_file[(day, f)] += 1

    print(f"merges {len(rows)}, conflicted {conflicted} "
          f"({100 * conflicted / max(1, len(rows)):.0f}%), of them catch-ups {catch_up}")
    print("\nconflicted / merges, by day:")
    for day in sorted(merges_day):
        print(f"  {day}  {by_day[day]:3} / {merges_day[day]}")
    print("\nfiles, by conflicted merges:")
    for f, n in by_file.most_common(15):
        print(f"  {n:4}  {f}")
    print("\nwatched files by day: " + ", ".join(WATCH))
    for day in sorted(merges_day):
        print(f"  {day}  " + " ".join(f"{by_day_file[(day, k)]:3}" for k in WATCH))


if __name__ == "__main__":
    main()
