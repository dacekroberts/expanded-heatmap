# Context review, 2026-10-08: what /clear would have saved

A lesson for the owner, kept to compare against after the 2026-10-11 reset.
The owner had never used `/clear` on this project and asked what it would have
saved. Measured from every local session transcript with
`python scripts/context_usage.py` (re-run it with `--since <date>` to see
whether the habits below changed anything). Usage is weighted by API price
ratios (input 1, cache write 1.25, cache read 0.1, output 5) as a proxy; plan
usage is not published per token, so treat the shares as estimates.

## The numbers

All history to 2026-10-08: 69 sessions, 807 subagent runs, 99,642 model turns,
269 automatic compactions.

| Where usage went | All history | Since 2026-10-05 |
|---|---|---|
| Re-reading the conversation on every turn (cache reads) | **81%** | 77% |
| New context (cache writes) | 12% | 17% |
| Output | 7% | 6% |
| Subagents, of all usage | 24% | 40% |

| Context at each turn | Turns | Share of input-side usage |
|---|---|---|
| under 100k | 21,026 | 7% |
| 100k-300k | 42,738 | 29% |
| 300k-600k | 23,975 | 35% |
| 600k-1M | 11,903 | 29% |

- **Half the input-side cost came from turns carrying more than 300k tokens of
  context.** Sessions routinely reached 700-900k before compacting on their own.
- **Three sessions were 39% of all usage:** monterrey (15.5%, 9,487 turns),
  riga (15.3%, 9,337 turns) and staging (8.4%). Each was a long-running
  session that kept working through task after task.
- **What-if, all history:** clearing every session once its context passed 60k
  would have saved about 54%, past 120k about 45%, past 200k about 35%, before
  counting the re-reads a fresh session needs (CLAUDE.md, the handoff note,
  the files in hand). **Net, about 30-40%: roughly a third of all usage.**
- **Since 2026-10-05 it was already better:** fewer turns over 600k, and the
  what-if saving falls to about 30% past 120k (20-25% net). Fresh sessions per
  batch and subagents did part of what `/clear` would have done; subagents
  rose to 40% of usage, which is the cost of that habit.

## Why it costs this much

Every turn re-reads the whole conversation so far. A cache read is cheap per
token, but at 500k of context a one-line reply still re-reads 500k. The cost
of a session grows with its length squared, not with the work done in it;
compaction only fires near the ceiling, after the expensive turns.

## The lesson: habits to keep

1. **`/clear` at every task boundary**: once a task is pushed and its handoff
   note or memory is written. The handoff notes, `PLAN.md` and memory are what
   make a clear cheap here; a fresh start re-reads perhaps 30-60k, against
   hundreds of thousands carried forward.
2. **`/compact` early** when a task cannot be cleared mid-way, at about
   150-200k, rather than waiting for the automatic one near the ceiling.
3. **One session per batch, never one session for a week of batches**:
   monterrey and riga show what a session that never ends costs.
4. **Subagents for reading, not for chatting**: they keep file dumps out of
   the main context, but each one rebuilds its own context; give each a tight
   scope and one report.
5. **Re-measure after the reset**:
   `python scripts/context_usage.py --since 2026-10-11`. The target is most
   input-side usage under 200k of context.
