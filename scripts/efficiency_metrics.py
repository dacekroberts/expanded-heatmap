"""Re-measure the efficiency review's numbers for a window, so its changes can be judged.

    python scripts/efficiency_metrics.py                       # the last 7 days
    python scripts/efficiency_metrics.py --since 2026-09-21 --until 2026-09-26
    python scripts/efficiency_metrics.py --baseline            # side by side with the review's window

Read-only; reads origin/master's history (run `git fetch` first) and the
working tree's file sizes.

WHY. docs/efficiency_review_2026-09-27.md measured 2026-09-21 to 09-25 by hand,
and the owner decides the number of parallel sessions "after seeing the progress
of these other efficiency boosters". Progress is only visible if the same
numbers are taken the same way each week. Run it at the weekly archive
(`scripts/archive_decisions.py`) and paste the table into that week's note.

Counted on origin/master's history:
  commits      non-merge commits
  merges       merge commits; `catch-up` = merging origin/master INTO a branch
  app landings first-parent commits on master that touch app/ (each one a deploy)
  re-renders   commits rewriting 20 or more outputs/*/heatmap.html
  owner        commit subjects tagged "(owner)" - approvals, roughly
  no-code      non-merge commits touching only *.md
Sizes are words in the working tree, now - not at the end of the window.
"""
import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = "origin/master"
BASELINE = ("2026-09-21", "2026-09-26")   # the review's window, 09-21 to 09-25 inclusive
SIZED = ["CLAUDE.md", "PLAN.md", "DECISIONS.md", "docs/city_master_list.md",
         "docs/project_context.md", "docs/data_sources.md"]
CATCH_UP = re.compile(r"origin/master'? into|^Merge origin/master", re.I)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", check=True).stdout


def window(since, until):
    rng = [f"--since={since}T00:00", f"--until={until}T00:00"]
    days = max((dt.date.fromisoformat(until) - dt.date.fromisoformat(since)).days, 1)

    subjects = git("log", REF, "--no-merges", "--format=%s", *rng).splitlines()
    merges = git("log", REF, "--merges", "--format=%s", *rng).splitlines()
    app = git("log", REF, "--first-parent", "--format=%h", *rng, "--", "app/").split()

    rerenders, nocode = 0, 0
    block, files = None, []
    for line in git("log", REF, "--no-merges", "--name-only", "--format=@@%h",
                    *rng).splitlines() + ["@@end"]:
        if line.startswith("@@"):
            if block is not None:
                if sum(f.endswith("heatmap.html") for f in files) >= 20:
                    rerenders += 1
                if files and all(f.endswith(".md") for f in files):
                    nocode += 1
            block, files = line, []
        elif line.strip():
            files.append(line.strip())

    catch = sum(bool(CATCH_UP.search(s)) for s in merges)
    return {
        "days": days,
        "commits": len(subjects),
        "merges": len(merges),
        "catch-up merges": catch,
        "app landings": len(app),
        "app landings / day": round(len(app) / days, 1),
        "mass re-renders": rerenders,
        "owner-tagged commits": sum("(owner)" in s for s in subjects),
        "no-code share": f"{round(100 * nocode / max(len(subjects), 1))}%",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    today = dt.date.today()
    ap.add_argument("--since", default=str(today - dt.timedelta(days=7)))
    ap.add_argument("--until", default=str(today + dt.timedelta(days=1)))
    ap.add_argument("--baseline", action="store_true",
                    help="also show the review's window, 2026-09-21 to 09-25")
    args = ap.parse_args()

    cols = [(f"{args.since}..{args.until}", window(args.since, args.until))]
    if args.baseline:
        cols.insert(0, (f"baseline {BASELINE[0]}..{BASELINE[1]}", window(*BASELINE)))

    keys = list(cols[0][1])
    width = max(len(c[0]) for c in cols) + 2
    print(f"{'':24}" + "".join(f"{name:>{width}}" for name, _ in cols))
    for k in keys:
        print(f"{k:24}" + "".join(f"{str(v[k]):>{width}}" for _, v in cols))

    print("\nwords now (loaded or read by sessions):")
    for rel in SIZED:
        p = ROOT / rel
        n = len(p.read_text(encoding="utf-8").split()) if p.exists() else 0
        print(f"  {rel:32} {n:>8,}")
    print("\nThe review measured 2026-09-21..25: 4,345 / 20,502 / 222,930 / ~37.6k words for the")
    print("first four files. Divide by days before comparing windows of different lengths.")


if __name__ == "__main__":
    main()
