# Place search: the site-wide rollout plan

Written 2026-10-11 by the place search session, at the owner's request, for
Cleanup. A proposal: the owner approves the order and the gates before any
of it runs. The recipe for one city is the `place-search-city` skill; the
reasoning trail is `docs/decisions_drafts/place-search.md`.

## Where things stand

- Branch `place-search` (worktree `.claude/worktrees/place-search`), tip
  `08393468` or later, nothing pushed, not merged with master. Nineteen
  cities searched: the Kyoto pilot, batches 1, 2a and 2b, and batch 3's size
  tests (Tokyo, London, Paris, São Paulo, Mexico City).
- The owner's phone test of the largest index (São Paulo, 1,229 KB gzipped
  first open, 785 KB intersections, 3.2 times Seoul's) passed 2026-10-11. The
  reserve intersection cut is unused.
- Languages built: ja, en, fr, ca, es, cs, nl, zh, ko, ka, pt.
- The branch is behind master: it holds 163 map steps, master has more. Read
  the counts from `app/cities.py` on master when the rollout starts; none are
  repeated here.

## Stage 0: land what exists (review time, Cleanup)

1. The owner's review of the branch: the drafts file's entries of 2026-10-08
   to 2026-10-11, newest first, and the open items in "Open with the owner"
   below.
2. Merge master into `place-search` in the worktree. Expect conflicts in
   `pipeline/map_common.py` (the basemap pilot touches it too),
   `scripts/check_all.py` and the append-only docs
   (`scripts/merge_append_only.py`). After the merge every searched map is
   stale against master's `map_common`: re-render the nineteen once, through
   the gate, then `check_place_search.py`, `check_place_index_drift.py`,
   `check_all.py`.
3. Fold the drafts file into `DECISIONS.md`; add the data-source rows the
   drafts name (OpenStreetMap as a search index, ODbL, per city).
4. One `deploy-verify` (`scope: map-chrome`) on the merged branch, then land.
   Landing `app/` is deploying: `check_deploy_imports.py`, and the reboot
   question from the whole push.
5. Repository size: `app/static/places/` is 38 MB for nineteen cities,
   of which the five size tests are most. Measure it at the merge and put the
   projected total for the whole site to the owner before stage 2 (it was one
   of the two top-line concerns, with iPhone memory).

## Stage 1: the script change every map gets

The search script ships only in searched maps. Two behaviours live in it
that the owner wants on every map, **landing with the rollout, not before**
(owner, 2026-10-11): the picked line's fade, casing and boxed label on a
legend pick, and nothing else. No unsearched map is re-rendered for them;
each gets them when its own search lands.

## Stage 2: the remaining cities, in waves by language

A new language costs most (word lists, matcher words, a first eye read that
finds the language's own traps), so a wave is one language or one country,
and the first city of a new language is built alone and read before the rest.

Proposed order, cheapest proof first:

1. **English** (US, Canada, UK, Australia and the rest): no new language,
   the 90-word bare-type list and the estate rule are measured on London.
   The largest wave by count; split it into batches of about ten.
2. **Japanese** (the `japan-city` set): ja is built; Tokyo and Kyoto are the
   precedents. Ward relations per city.
3. **French, Spanish, Portuguese** (France, Mexico, Spain, Brazil and the
   rest of Latin America): built languages, each with one large city read.
   Barcelona's pattern (ca with es searched as well) covers the other
   Catalan cities; a Basque or Galician city is a new language.
4. **Korean, Chinese** (Korea; Taiwan and Hong Kong's pattern): built.
   Taiwan's names are zh with no English forced; measure, as everywhere.
5. **Czech, Dutch** (the Czech batch, Belgium, the Netherlands): built.
6. **New languages, one first city each**: German, Italian, Polish and the
   rest of the list on master. Each needs the "A new language" section of the
   skill before its first fetch.

## Per batch (about ten cities, one session)

- One build session, in the place-search worktree or a fresh branch off the
  landed master; at most three build sessions at once machine-wide.
- Fetch: two Overpass queries a city, one in flight, 60 s after a 504 or
  429; a city whose boundary query times out takes `PLACE_SPLIT` (tiles).
  Caches under new dated names in the shared `data/`.
- Build, then the `place-read` agent, one city per call, in the background.
  A class a rule can catch goes in `place_index.py` under the rule-change
  protocol (rebuild every index, `check_place_index_drift.py --against`,
  list every row moved in a built city for the owner). A single row goes in
  the city's config by id, after `place_search_review.py ids`.
- Render once at the end of the batch, every city in it, through
  `heavy_job.py`. A matcher or script change in the batch means every
  searched map, so hold script changes for the batch's end.
- Checks green, commit, drafts entry with the sizes and the numbered owner
  questions, hold. Cleanup lands batches at review time.

## Gates

- **Size:** any city whose first open passes São Paulo's 1,229 KB gzipped is
  named to the owner before it lands; past about 1.5 times that, a phone
  test first, with the reserve intersection cut as the fallback.
- **Personal information:** the eye read is not optional for any city; a
  home, a person's own name or a business's driveway found after landing is
  removed first and logged after.
- **Rule changes** that move rows in a built city go to the owner with the
  rows listed, never applied on a say-so (the monument and gallery rules
  would have removed about 420 rows including Seoul's King Sejong statue).
- **Usage:** the 5-hour window's 90% ceiling; `get_usage` between cities.

## After the rollout: the audits the owner asked for

- The **unopened-stations watch file** (`docs/place_search_unopened_stations.json`,
  `scripts/check_place_unopened.py`): re-read after the rollout; stations
  that have opened come back in.
- **Slips** in the rules the owner accepted with "audit several times after
  the rollout is complete" (2026-10-11, answer 4), and the **closure cases**
  like Hong Kong's (answer 5): revisit once all cities are in.
- **Lesser rebuilt streets** (answer 6): `PLACE_REBUILT` holds only the ones
  named so far; audit highway=construction ways with names city by city.
- **`PLACE_VISITABLE`** entries expire after 365 days (check G).
- Whether unfindable lines are listed on city pages or handled another way
  (answer 1).

## Open with the owner

- The WIP suggestion tuning, the corner credit test, the Cities menu move,
  and whether "Download this index" also links the intersections file
  (earlier batches, still open).
- The projected repository size for the whole site (stage 0, item 5).
- The wave order above.
