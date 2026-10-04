# Process review, 2026-10-04

Second round after `docs/efficiency_review_2026-09-27.md`. Window: 2026-09-27 to
10-04 (8 days, today partial), `origin/master` at `34920ef1`. Conflicts were
counted by re-merging every merge's two parents with `git merge-tree` (exact,
not inferred from messages). Read-only; no tracked file changed.

## efficiency_metrics.py --baseline

| Measure | 09-21..25 (5 days) | 09-27..10-04 (8 days) | Per day, then -> now |
|---|---|---|---|
| Non-merge commits | 645 | 1,133 | 129 -> 142 |
| Merges | 155 | 336 | 31 -> 42 |
| Catch-up merges | 107 | 227 | 21 -> 28 |
| `app/` landings | 76 | 105 | 15.2 -> 13.1 |
| Mass re-renders (20+ maps) | 13 | 9 | 2.6 -> 1.1 |
| Owner-tagged commits | 32 | 274 | 6 -> 34 |
| `.md`-only share | 55% | 49% | |

Words now: CLAUDE.md 2,797; PLAN.md 12,565; DECISIONS.md 10,103; city_master_list.md
29,733 (33,891 on master); project_context.md 13,344; data_sources.md 33,818.

Two columns no longer measure what they say. "App landings" counts first-parent
commits, which a fast-forwarded review branch inflates (09-30: 32, nearly all one
mega-review); 15-minute deploy windows are the better figure (below).
"Owner-tagged" rose mostly because tagging became the convention.

## Ranked findings

| # | Finding | Evidence | Estimated saving | Whose habit |
|---|---|---|---|---|
| 1 | Generated and counted files conflict on every build merge | Conflicted merges this week: master list 57, `app/cities.py` 33, `ring_shares.json` 33, `macro_facts.json` 14. Since 10-01, 27 of 106 merges conflicted, nearly all in these four; all 7 conflicted merges today include the master list. All four are written by scripts or checked by `check_*`, so a hand resolution is redone work. | ~35-45 conflict resolutions a week (~150 session turns) | Structure |
| 2 | Catch-up merges rose, not fell | 28 a day against 21; 103 of 176 conflicted merges were catch-ups. 6-51 branches named in merges per day (51 on 09-30); 9 sessions used the memory gate on 10-03/04. "Re-check origin/master in the same breath as the push" turns every push into a catch-up for everyone else. | Halving: ~100 merges a week | Owner (session count) and structure |
| 3 | The 09-27 trims are regrowing | CLAUDE.md 1,685 -> 2,797 words (+66%, 36 commits). PLAN.md 3,136 -> 12,565 (4x; 59 done items still in it). `session_roles.md` 2,643 -> 4,748. `data_sources.md` 15.9k -> 33.8k since the country split. Fixed load per session: CLAUDE.md + MEMORY index (763) + 22 skill descriptions (1,765) + 3 agent descriptions (325) = ~5,650 words; with project_context and PLAN read first, ~31,600 words (~42k tokens). | ~12k tokens off every call if CLAUDE.md returns to 2,000 and PLAN to 5,000 | Session and structure |
| 4 | Full re-renders grew fourfold and came in pairs | 6 renders of 124-158 maps in 8 days; two on 10-02 (touch gestures, 144 each), two on 10-03 (credits in a new tab, touch tap fix, 158 each). ~1,150 `heatmap.html` rewrites against 509. Machine cost is small (render-only all: 4-6 min, 2.1 GB measured) but each needs a drift check, review and a push of ~158 rewritten maps into a 297 MB pack. A chrome change now costs 158 maps, not 40. | ~3 full renders a week | Owner (one fix approved at a time) and session |
| 5 | Downstream notices fire per push | Since 10-03 every push to master messages Visuals and Analytics. ~106 push windows in 8 days (13 a day) means up to ~26 messages a day, each waking a session on its full context. | ~150 session turns a week if sent once per review time | Owner rule |
| 6 | DECISIONS writing volume did not fall | Week of 09-27 archive: 505 entries, 204k words (prior week 381, 209k). Median entry fell 424 -> 308 words; p90 687; one entry 8,301. The drafts rule removed the conflicts but not the writing. | ~100k words of output a week with a ~150-word cap (detail in the commit) | Session |
| 7 | Owner approvals still come one at a time between review times | 34 owner-cited commits a day; PLAN "Now" names the owner 46 times. Review time worked for landings (8 named batches) but judgment calls under "recommend, then confirm" still stop a session each. | Not measurable from git | Owner |
| 8 | The memory gate wraps small jobs | 182 gated jobs in 2 days: 155 measured under 1 GB, 121 under 0.3 GB, median 10 s. Declared 136.9 GB against 67.8 GB measured. | A wrapper call per small job; low | Session |
| 9 | The pre-push hook doubled | 48 checks in 57.4 s (measured today) against 21 in 29.1 s; `check_*` scripts 23 -> 39. | Small; ~1 min a push | Structure |

## The top three changes

1. **Regenerate, never merge, the generated files.** A `.gitattributes` merge
   driver (or a post-merge step) for `app/cities.py`, `ring_shares.json`,
   `macro_facts.json` that takes either side and re-runs the generator, and the
   master list's count cells generated from its evidence file rather than
   typed. Weekly: ~35-45 fewer conflicted merges, ~150 session turns.
2. **Decide the session count, and batch what every push fans out.** At most
   three build sessions plus cleanup; branches merge `origin/master` only
   before their own push, not after others'; downstream notices once per
   review time (`downstream_changes.py` already takes any old SHA). Weekly:
   ~100 catch-up merges and ~150 downstream turns.
3. **Word budgets as a check, trimmed at the weekly archive.** CLAUDE.md
   2,000, PLAN.md 5,000 with done items moved out in the archive sitting,
   `session_roles.md` 3,000, enforced in `check_all.py`. Weekly: ~12k tokens
   off every call; at an assumed 10 sessions x 200 calls a day, ~170M cached
   input tokens.

Finding 4 (re-render batching) is what is left of the 09-27 finding 4: one map
chrome render per review time would fold into change 2's batch.

## What improved since 2026-09-27

- **DECISIONS conflicts are gone.** 144 merges conflicted on DECISIONS.md
  09-27..30, zero since 10-01 (drafts files, 09-30). Overall conflict rate fell
  from 65% of merges (149 of 231) to 25% (27 of 106).
- **DECISIONS.md is small.** 222,930 -> 10,103 words; the weekly archive ran.
- **Deploys are batched.** 15-minute deploy windows on master fell from 9.6 to
  5.9 a day; commits mentioning a reboot 38 in 5 days -> 13 in 8; 59 of 102
  first-parent `app/` commits are now merges (20 of 66 before).
- **Fewer, if larger, re-renders**: 2.6 -> 1.1 a day.
- **Checks run themselves**: `check_all.py` is the pre-push hook (finding 6 of
  09-27 closed).
- **Memory is gated with measured peaks**, and entries are shorter (median
  424 -> 308 words).

## For the session-count decision

Per day, commits and merges rose with more sessions; conflicts fell only
because of the drafts rule. Change 1 removes most of what remains, so the
session count now buys mainly catch-ups and notices, not conflicts.

## Limits

Pushes, approval waits, `check_*` runs and messages are not logged; they are
inferred from commit times and rules. Word sizes come from the cleanup
worktree, whose DECISIONS.md holds uncommitted entries.
