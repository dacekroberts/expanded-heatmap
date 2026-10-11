# Handoff: session hygiene pilot (transit-globe)

From the expanded-heatmap Cleanup session, 2026-10-09, for the owner to start
in transit-globe after the weekly reset of 2026-10-11. The owner measured where
Claude Code usage goes across their projects (the private "Claude usage review"
page) and wants seven habits tried in a real project before they go into a
personal `~/.claude/CLAUDE.md` for every project. This is one of two pilots;
the other is hydrowhiplash-elnino26.

## What to do

1. Copy this file into this repo as `docs/handoff_session_hygiene_pilot.md`.
2. Add the Block below to `CLAUDE.md` as its own section, unchanged.
3. Commit both. Then work as usual, following the block.
4. Each time a block rule fires (a new session suggested, a `/compact`
   suggested, four or more sessions mentioned), add one line to the Pilot log
   below: date, context size, what was suggested, what the owner did. Commit
   it with the next commit; do not make a commit for the log alone.
5. At the end, the owner asks for the Questions to be answered from the log.

## Block

```markdown
## Session hygiene (pilot from 2026-10-12, see docs/handoff_session_hygiene_pilot.md)
- Small, related tasks can share a session. At the first task boundary past about 150k of context, or when switching to unrelated work, suggest a new session.
- Mid-task past about 200-250k of context, suggest /compact with a focus line.
- Suggest a new session rather than /clear, so the old history stays scrollable.
- Before suggesting a switch, write the state to files (handoff note, plan, memory).
- Keep command output short: counts, head, tail, grep or quiet flags; read files by line range.
- Send wide reading to a purpose-built subagent with a tight scope and one short report; prefer named agents to general-purpose ones.
- Measure usage with the usage meter before quoting a percentage or deferring work on usage grounds; never estimate it.
- Mention it when four or more sessions are running at once: they share one allowance.
```

## Baseline (2026-10-07 to 2026-10-09, before the pilot)

Measured from this project's transcripts with expanded-heatmap's
`scripts/usage_report.py`; weights are API price ratios, not plan percentages.

- 2 sessions, 866 model turns, 1 subagent run, about 10M weighted a day.
- Both sessions passed 500k of context (peaks 576k and 508k) within a day.
- Re-reading the conversation was 78% of usage; turns at 300k+ context were
  62% of the input side.
- Clearing past 120k would have saved about 45%, before re-reads.
- Bash output was 59% of what tools added; Artifact results averaged 10k
  characters each.
- A fresh session starts at about 62k.

The pilot works here if sessions stop passing 500k and the clear-past-120k
what-if falls well below 45%.

## Pilot log

| Date | Context | Suggested | Owner did |
|---|---|---|---|

## Questions for the end

1. Did the 150k task-boundary suggestions come at sensible moments, or too
   early or too late for this project's work?
2. Did "small, related tasks can share a session" hold, or did unrelated work
   creep in without a suggestion?
3. Was any rule annoying, ignored, or never relevant here?
4. Did the handoff-before-switching habit make new sessions start well?
5. Anything this project needed that the block does not say?
