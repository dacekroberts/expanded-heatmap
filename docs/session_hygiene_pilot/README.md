# Session hygiene pilot

The seven habits proposed for the owner's personal `~/.claude/CLAUDE.md`
(the "Claude usage review" page, https://claude.ai/artifact/98TEtjLTvpxutTBcMHq9BU)
are piloted in two other projects first, as a project-level CLAUDE.md block,
before anything goes into the personal file (owner, 2026-10-09). Two projects
because they work differently: transit-globe is new, with a few long sessions;
hydrowhiplash-elnino26 has many sessions and large file reads.

Drafted here; nothing is written into either project until the owner starts the
pilot, after the weekly reset of Sunday 2026-10-11 19:00 UTC.

| File | What it is |
|---|---|
| `handoff_transit-globe.md` | The handoff for transit-globe: the block, its baseline, the log, the questions |
| `handoff_hydrowhiplash-elnino26.md` | The same for hydrowhiplash-elnino26 |

## Commands

From this repo's checkout. Measuring reads only the local transcripts under
`~/.claude/projects/`, never the other projects' files.

Re-measure each baseline the day the pilot starts, so it runs up to the start:

```bash
python scripts/usage_report.py --out data/_usage/transit-globe-baseline --prefix C--Users-dacek-Documents-Portfolio-transit-globe
python scripts/usage_report.py --out data/_usage/hydrowhiplash-baseline --prefix C--Users-dacek-Documents-Portfolio-hydrowhiplash-elnino26
```

At the review, the pilot's own row (`plan_periods.json`, the last row) comes
from `--baseline <start date>`:

```bash
python scripts/usage_report.py --out data/_usage/transit-globe-pilot --prefix C--Users-dacek-Documents-Portfolio-transit-globe --baseline 2026-10-12
python scripts/usage_report.py --out data/_usage/hydrowhiplash-pilot --prefix C--Users-dacek-Documents-Portfolio-hydrowhiplash-elnino26 --baseline 2026-10-12
```

`data/` is gitignored. Change `2026-10-12` if the pilot starts on another day.

## Starting it, in each project

Open a session in the project and give it:

> Start the session hygiene pilot. Read
> C:\Users\dacek\Documents\Portfolio\expanded-heatmap\docs\session_hygiene_pilot\handoff_<project>.md,
> copy it into this repo as docs/handoff_session_hygiene_pilot.md, and add its
> "Block" section to CLAUDE.md as it says. Commit both. Then carry on with the
> work I give you, following the block.

(Use the main checkout's path, which has this folder once it is pushed.)

## The review, about two weeks in

1. Run the two pilot commands above.
2. Compare each project's pilot row with its baseline: the clear-past-120k
   what-if, usage a day and the subagent share. Sessions by peak context
   (`session_peaks.json`) should move out of 500k+.
3. Read each project's pilot log and its answers to the questions.
4. Decide, habit by habit, what goes into `~/.claude/CLAUDE.md`
   (the deferred note in Claude's memory), then take the pilot blocks out
   of both projects.
