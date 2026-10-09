# Context review, 2026-10-08: what /clear would have saved

A lesson for the owner, kept to compare against after the 2026-10-11 reset.
The live version is the owner's private "Claude usage review" page
(https://claude.ai/artifact/98TEtjLTvpxutTBcMHq9BU), refreshed from
`python scripts/usage_report.py`; this file is the dated snapshot.
The owner had never used `/clear` on this project and asked what it would have
saved. Measured from every local session transcript with
`python scripts/context_usage.py` (re-run it with `--since` and `--until` to
see whether the habits below changed anything). Usage is weighted by API price
ratios (input 1, cache write 1.25, cache read 0.1, output 5) as a proxy; the
plan's own accounting is not published per token, and these numbers do not
convert into plan percentages (see Limits).

## The numbers

All history to 2026-10-08: 68 sessions, 750 subagent runs, 86,083 model turns,
269 automatic compactions. Each turn counted once: a moved session's transcript
copies its history into a new file (riga's folder held a copy of monterrey's
first 547 turns, about 13% of all turns before the fix).

| Where usage went | All history | Since 2026-10-05 |
|---|---|---|
| Re-reading the conversation on every turn (cache reads) | **80%** | 77% |
| New context (cache writes) | 13% | 17% |
| Output | 7% | 6% |
| Subagents, of all usage | 27% | 40% |

| Context at each turn | Turns | Share of input-side usage |
|---|---|---|
| under 100k | 18,768 | 8% |
| 100k-300k | 38,428 | 31% |
| 300k-600k | 20,045 | 35% |
| 600k-1M | 8,854 | 26% |

- **Over 60% of the input-side cost came from turns carrying more than 300k
  tokens of context.** The window is 1M and auto-compaction starts at 97%, so
  sessions routinely reached 700-900k before compacting.
- **Two sessions were 29% of all usage:** monterrey (18.7%, 9,487 turns) and
  staging (10.1%, 5,207 turns), each a session that kept working through task
  after task.
- **What-if, all history:** clearing each session once its context passed
  120k would have saved about 43%, past 200k about 33%, before counting the
  re-reads a fresh session needs. **Net, roughly a third of all usage.**
- **A fresh session is never empty:** this one started at about 75k (tools
  34k, connector (MCP) tools 17k, skill list 10k, memory 8k, system prompt
  5k). Clearing resets to that floor, not to zero; connectors a project never
  uses raise it for every session.

## By plan

The owner moved from Pro to Max 5x on 2026-09-20 and to Max 20x on
2026-09-30. This project's transcripts start on 2026-09-18.

| Period | Plan | Active days | Weighted usage a day | Clearing past 120k would have saved |
|---|---|---|---|---|
| 09-18 to 09-19 | Pro | 2 | 14M | 57% |
| 09-20 to 09-29 | Max 5x | 9 | 156M | 51% |
| 09-30 to 10-08 | Max 20x | 10 | 144M | 35% |
| 10-05 to 10-08 (part of the above) | Max 20x | 5 | 80M | 30% |

- **The bigger plans bought headroom for the habit, not more work.** Daily
  usage was flat across the move to 20x; what changed is that the upgrades
  came while the sessions ran to the ceiling. On Max 5x, half the usage was
  context a clear would have dropped.
- **The habits that arrived with 20x already helped:** fresh sessions per
  batch, subagents and handoff notes cut the what-if from 51% to 35%, and
  daily usage fell by about half from 2026-10-05.

## What it means for the allowance

The app's usage card is a share of the owner's own account allowance, not
shared with anyone: a rolling 5-hour window and a weekly window (Sunday 19:00
UTC), each counting every project and every surface on the plan, with a
separate weekly limit for Fable inside the all-models one. There is no daily
limit. The percentages above are shares of this project's measured tokens,
not of that allowance.

**Rough guide: clearing at task boundaries would have freed about a quarter
of the weekly allowance this project's work used.** This project was 73% of
all usage measured on this machine in the week from 2026-10-04 (the rest:
hydrowhiplash-elnino26 20%, transit-globe 4%, link-station-commercial 3%);
a third of 73% is about 24%.

**Assumption (unverified):** that the meter weighs tokens roughly as the API
price ratios do. Limits shows it does not track them closely, and the meter
also counts usage outside these transcripts, so the real figure could be
lower or higher. Re-check against the usage card after the reset: a week of
the habits below should show the weekly percentage climbing more slowly for
the same amount of work.

## Why it costs this much

Every turn re-reads the whole conversation so far. A cache read is cheap per
token, but at 500k of context a one-line reply still re-reads 500k, so a
session's total cost grows with the square of its length, not with the work
done in it. Compaction only fires near the ceiling, after the expensive turns.

## The lesson: habits to keep

1. **`/clear` at every task boundary**: once a task is pushed and its handoff
   note or memory is written. The handoff notes, `PLAN.md` and memory are what
   make a clear cheap here.
2. **`/compact` early** when a task cannot be cleared mid-way, at about
   150-200k, rather than waiting for the automatic one near 970k.
3. **One session per batch, never one session for a week of batches**:
   monterrey shows what a session that never ends costs.
4. **Subagents for reading, not for chatting**: they keep file dumps out of
   the main context, but each one rebuilds its own context; give each a tight
   scope and one report.
5. **Keep the floor low**: turn off connectors a project does not use.
6. **Re-measure after the reset**:
   `python scripts/context_usage.py --since 2026-10-11`. The target is most
   input-side usage under 200k of context.

## Limits

- The weights are API price ratios. The plan's meter does not follow them:
  the week from 2026-09-27 measured 1,379M weighted across every project on
  this machine, while the week from 2026-10-04 reached 98% of Max 20x at
  671M. The meter also counts usage these transcripts do not hold (claude.ai
  chats, other devices, cloud sessions), and an upgrade may reset the week.
  So the shares above say where the tokens went; for a plan percentage, read
  the app's usage card.
- The what-if assumes the dropped context was read from cache, and leaves out
  what a fresh session re-reads, hence "roughly a third" net.
- Pro covers only two days of this project; earlier work is in other projects.
