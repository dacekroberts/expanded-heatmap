# Process efficiency review (2026-09-27)

A snapshot, not a living document. This is the PLAN.md item "An honest
efficiency review of the whole PROCESS", run as one `cleanup-sweep` agent
(`scope: review`, read-only) on `origin/master` at `8f9d118`. Its window is
2026-09-21 to 09-25: 593 non-merge commits and 160 merges. The owner's
decision on it is in DECISIONS.md (2026-09-27).

## The seven findings

| # | Finding | Evidence | Rough weekly saving | Whose habit |
|---|---|---|---|---|
| 1 | Parallel sessions spend a lot catching up with each other | Most merges since 09-21 were catch-ups rather than landings: 104 by the agent's count, and 110-129 of 159 by a re-count that counts them more broadly. 59 landing merges touched DECISIONS.md, and 23 commits were handoff edits. | ~75M token-reads if catch-ups are halved | Structure and owner |
| 2 | Approvals and deploys happen one change at a time | 69 commit messages since 09-21 cite owner approval. `app/` landed on master (each landing a deploy) 25, 16, 12, 14 and 9 times a day on 09-21 to 09-25. 38 commit messages mention a reboot. | ~60 deploys and reboots, 2-3 owner-hours, ~40M token-reads | Owner |
| 3 | Every call carries a lot of fixed text | CLAUDE.md grew from 1,396 words (09-21) to 4,345 and was rewritten 45 times; much of it is incident history. `docs/project_context.md` is about 17k tokens and the DECISIONS index about 18k. | ~15M token-reads | Structure |
| 4 | Shared map controls were re-rendered in small increments | 14 commits re-rendered 20 or more maps each, seven of them on 09-24. Three of those chased the same line-label contrast problem. | ~20M token-reads | Session and structure |
| 5 | Hand-kept documents churn heavily | 57% of non-merge commits touch no code. `docs/city_master_list.md` is about 62k tokens and was rewritten 148 times. PLAN.md had 97 done items against 79 open. | Not measured | Structure |
| 6 | None of the 24 `check_*` scripts runs automatically | No git hook and no CI; the only hook is the heredoc guard. A city landing needs five checks, each run by hand. | Small in tokens; the gain is that nobody has to remember | Structure |
| 7 | The weekly limit ran out early | DECISIONS records 93% used on 09-22 and 87% on 09-24. There were no commits on 09-26, which suggests the limit ran out; nothing records that directly. | Covered by 1-4 | Owner and structure |

## The agent's top three changes

1. **Fewer sessions, and a DECISIONS.md that cannot conflict.** At most two
   sessions at once, landing in batches. Either one file per entry with a
   generated index, or archive by month.
2. **One owner approval review a day and one `app/` push per batch.** Wording,
   labels and renderer changes all wait for that review, so there is one
   reboot instead of many. This absorbs finding 4.
3. **Trim what every session loads.** CLAUDE.md to about 1,500 words, with the
   incident history moved into skills and DECISIONS. A DECISIONS index of the
   last 7 days, a PLAN.md trim, and `check_all.py` as a pre-push hook.

## What the owner chose

Change 2 first, because it costs no code and has the largest saving the owner
controls directly. Change 3 second. For change 1, only the archive-by-month
half; how many sessions run at once is a separate decision. One file per entry
was not chosen, because `merge_append_only.py`, `decisions_index.py` and the
`decisions-entry` skill all depend on the single file.

## Reading the numbers

- **A "token-read" is one full re-read of a session's context, assumed at
  about 300k tokens.** The unit overstates cost, because cached context is
  much cheaper than fresh input. The figures rank the findings against each
  other; they do not predict usage percentages.
- The agent could not measure `get_usage` history, approval wait times or
  calls per session, so those parts of the estimates are assumptions.

## Figures as of this review

| Measure | PLAN.md said (2026-09-24) | 2026-09-27 |
|---|---|---|
| DECISIONS.md | ~210k words | 222,930 words, about 300k tokens, 412 entries (118 written on 09-24) |
| CLAUDE.md | ~4,200 words | 4,345 words |
| `docs/data_sources.md` | ~52k words | 55,129 words |
| PLAN.md | ~16.7k words | 20,502 words |
| Commits on 09-24 | 179 | 191 by committer date |
| `heatmap.html` rewrites on 09-24 | 286 | 288 |
| Skills / agents / `check_*` scripts | 16 / 2 / 17 | 17 / 3 / 24 |

PLAN.md's claim that DECISIONS.md "conflicts on every two-session push" is
only partly supported. 59 landing merges touched it, but only 8 merge
messages mention a conflict.
