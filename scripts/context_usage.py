"""Measure where this project's Claude usage goes, from the local session transcripts.

Reads every transcript under ~/.claude/projects/ for this project (main checkout and
every worktree, subagents included), counts each model turn once, and reports:
the split between re-reading the conversation (cache reads), new context (cache
writes) and output; how large the context was at each turn; the sessions that cost
most; and what clearing a session once its context passed a cap would have saved.

Usage is weighted by API price ratios (input 1, cache write 1.25, cache read 0.1,
output 5) as a proxy for plan usage, which is not published per token.

Baseline 2026-10-08 (all history): cache reads 81%, cache writes 12%, output 7%;
half the input-side cost at contexts over 300k; clearing past 120k would have
saved about 45% before re-reads. See docs/efficiency_review_2026-10-08_context.md.

    python scripts/context_usage.py [--since YYYY-MM-DD] [--top N]
"""
import argparse
import collections
import glob
import json
import os

WEIGHTS = {"inp": 1.0, "cw": 1.25, "cr": 0.1, "out": 5.0}
CAPS = (60_000, 120_000, 200_000)
PROJECTS = os.path.join(os.path.expanduser("~"), ".claude", "projects")
PREFIX = "C--Users-dacek-Documents-Portfolio-expanded-heatmap"


def turns(path, since):
    """Yield (inp, cw, cr, out) once per model turn in one transcript."""
    seen = set()
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if '"usage"' not in line:
                continue
            try:
                o = json.loads(line)
            except ValueError:
                continue
            if o.get("type") != "assistant":
                continue
            if since and (o.get("timestamp") or "") < since:
                continue
            m = o.get("message") or {}
            u = m.get("usage")
            if not u:
                continue
            # one turn can span several lines that repeat the same usage
            key = (m.get("id"), o.get("requestId"))
            if key in seen:
                continue
            seen.add(key)
            yield (u.get("input_tokens") or 0, u.get("cache_creation_input_tokens") or 0,
                   u.get("cache_read_input_tokens") or 0, u.get("output_tokens") or 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="only turns on or after this date (YYYY-MM-DD)")
    ap.add_argument("--top", type=int, default=8)
    args = ap.parse_args()

    tot = collections.Counter()
    by_ctx = collections.Counter()
    turns_by_ctx = collections.Counter()
    saved = collections.Counter()
    sessions = []
    sub_cost = 0.0
    for d in glob.glob(os.path.join(PROJECTS, PREFIX + "*")):
        name = os.path.basename(d)[len(PREFIX):].replace("--claude-worktrees-", "") or "main"
        for path in glob.glob(os.path.join(d, "**", "*.jsonl"), recursive=True):
            is_sub = "subagents" in path.replace("\\", "/")
            cost = 0.0
            n = 0
            for inp, cw, cr, out in turns(path, args.since):
                ctx = inp + cw + cr
                for k, v in (("inp", inp), ("cw", cw), ("cr", cr), ("out", out)):
                    tot[k] += v
                c = inp * WEIGHTS["inp"] + cw * WEIGHTS["cw"] + cr * WEIGHTS["cr"] + out * WEIGHTS["out"]
                cost += c
                n += 1
                band = min(ctx // 100_000, 9) * 100
                turns_by_ctx[band] += 1
                by_ctx[band] += c - out * WEIGHTS["out"]
                if not is_sub:
                    for cap in CAPS:
                        # context above the cap is history a clear would have dropped,
                        # nearly all of it read from cache
                        saved[cap] += max(0, ctx - cap) * WEIGHTS["cr"]
            if n:
                sessions.append((cost, n, is_sub, name))
                if is_sub:
                    sub_cost += cost

    total = sum(tot[k] * WEIGHTS[k] for k in WEIGHTS)
    if not total:
        raise SystemExit("no turns found")
    main_n = sum(1 for s in sessions if not s[2])
    print(f"sessions {main_n}, subagent runs {len(sessions) - main_n}, turns {sum(turns_by_ctx.values()):,}"
          + (f", since {args.since}" if args.since else ""))
    print("share of usage:")
    for k, label in (("cr", "re-reading the conversation (cache reads)"),
                     ("cw", "new context (cache writes)"),
                     ("out", "output"), ("inp", "uncached input")):
        print(f"  {tot[k] * WEIGHTS[k] / total:6.1%}  {label}")
    print(f"  {sub_cost / total:6.1%}  of all usage was subagents")
    print("context size at each turn: turns, share of input-side usage")
    inside = sum(by_ctx.values())
    for band in sorted(turns_by_ctx):
        print(f"  {band:>3}k+  {turns_by_ctx[band]:>7,}  {by_ctx[band] / inside:6.1%}")
    for cap in CAPS:
        print(f"clearing past {cap // 1000}k would have saved ~{saved[cap] / total:.0%} (before re-reads)")
    print("costliest sessions:")
    for cost, n, is_sub, name in sorted(sessions, reverse=True)[:args.top]:
        print(f"  {cost / total:6.1%}  {n:>6,} turns  {'subagent in ' if is_sub else ''}{name}")


if __name__ == "__main__":
    main()
