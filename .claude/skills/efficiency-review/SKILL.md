---
name: efficiency-review
description: Review HOW this project's work gets done - merges and their conflicts, catch-ups, re-renders, approvals, what every session loads, downstream messages - from git history and file sizes, and return a ranked list of findings with evidence, a weekly saving and whose habit each is (owner, session or structure), plus the top three changes. Use when the owner asks for a process or efficiency review, and for the weekly numbers at the archive sitting. Not a code review, and not for auditing the maps (consistency-sweep).
---

# The efficiency review

Distilled from two rounds: `docs/efficiency_review_2026-09-27.md` (by hand)
and `docs/efficiency_review_2026-10-04.md` (one agent, about 8 minutes). The
second round's three changes (owner, 2026-10-04) are in force: generated
files regenerate rather than merge, at most three build sessions with
downstream notes once per review time, and word budgets checked by
`scripts/check_word_budgets.py`.

## Who runs it, and how

- **One agent in its own context**, read-only on tracked files, writing its
  deliverable to the session scratchpad; the caller files it as
  `docs/efficiency_review_<date>.md` and commits it. Light work: stay off the
  heavy-job gate's budget, since builds may be running.
- **Read the previous round first** and report what changed since, rather than
  repeating it. The new findings matter; the old ones matter only where they
  regrew or were fixed.

## Evidence, never impressions

`git fetch` first; everything reads `origin/master`.

1. `python scripts/efficiency_metrics.py --baseline`: commits, merges,
   catch-ups, re-renders and owner-tagged commits per day, against the first
   round's window. Two columns drifted (2026-10-04): "app landings" counts
   first-parent commits, which a fast-forwarded review branch inflates, so
   count 15-minute deploy windows instead; "owner-tagged" rose because
   tagging became the convention.
2. `python scripts/merge_conflict_stats.py --since <date>`: exact conflicts,
   by re-merging each merge's parents with `git merge-tree`, by file and by
   day. The generated files (`merge=regenerate` in `.gitattributes`, rebuilt by
   `scripts/regen_generated.py`) should now show none; a file that conflicts on most build merges is the
   next candidate.
3. **Load per session**: words in CLAUDE.md, the MEMORY index, the skill and
   agent descriptions, plus project_context.md and PLAN.md (read first by
   every session). `python scripts/check_word_budgets.py --report` gives the
   budgeted ones.
4. **Re-renders**: commits rewriting 20 or more `outputs/*/heatmap.html`, and
   whether they came one per review time or in pairs.
5. **DECISIONS volume**: entries and words per week from the archive's index
   (`docs/decisions/<Sunday>.md` headings only; never read a week whole),
   median and p90 entry length.
6. **The gate**: `python scripts/heavy_job.py status`, declared against
   measured peaks.
7. **The pre-push hook**: `python scripts/check_all.py --list`, and its time.
8. **Context growth**: `python scripts/context_usage.py --since <date>`:
   re-reads against output, usage by context size, the costliest sessions.
   Baseline `docs/efficiency_review_2026-10-08_context.md` (re-reads 80%;
   over 60% of the input-side usage past 300k).

What git cannot show (pushes, approval waits, check runs, messages) is
inferred from commit times and rules; say so in a Limits section.

## The deliverable

Under about 1,200 words, plain and specific:

- the metrics table;
- **ranked findings**, as a table: finding, evidence (numbers), estimated
  weekly saving, whose habit (owner, session or structure);
- **the top three changes**, each with a rough weekly saving;
- what improved since the last round;
- anything the owner's open decisions wait on (the session count did);
- Limits.

The owner decides. Record the decision in DECISIONS, and a rule it changes
in CLAUDE.md and `docs/rule_history.md`.

## When

On the owner's request, and the metrics alone at each weekly archive
(`scripts/archive_decisions.py`, Sunday), pasted into that week's note.
