# Cleanup handoff, 2026-10-13: the search rules and the night runner

Written by Cleanup for its own next context (the owner clears this session
between tasks). `docs/handoff_cleanup_2026-10-12.md` stays the note for the
phase 2 landing; this one covers what came after. Counts here are dated;
re-measure before repeating one.

## Where things stand

- **master = `4d7cf5f9`** (pushed and rebooted 2026-10-13, verified live on
  Seattle). It carries: rights meta tags and "Map design © Dace Roberts" in
  every map's bottom line; legend rows as buttons; street lines (a side file
  per searched city, `place-street-lines` skill); the Cities menu under
  headers (`cities.MENU_GROUPS`, Japan last); the picked-line look on every
  map; a third credit link, "streets". 68 of 68 checks.
- **`worktree-cleanup` is one commit ahead** (`f1b82c31`, the decisions
  entry with the owner's rulings below). Not pushed; docs only.
- **Nothing of the rule work is built.**

## Next task 1: the night runner (a subagent was building it)

The owner: "yes build the runner, can you scaffold the remaining waves in
advance and allow it to refine the waves based on its wave 1 results and
proceed?" and "bring a list of judgement calls for me in the morning".

- Two NEW scripts were ordered from a background agent, written into this
  working tree, uncommitted: `scripts/place_search_area_lookup.py` (fills a
  plan's missing boundary relations from the map's stations, one light
  query a city, pinned, through `FetchLock`) and
  `scripts/place_search_night.py` (lookup, scaffold, fetch queues per
  mirror, index build through the job gate, per-city checks, refinement of
  later waves, one Markdown morning report; never commits, pushes or
  renders; refuses on `master` and `worktree-cleanup`). Its extras are in
  the session scratchpad, `night_runner/`: lines for `docs/commands.md` and
  `scripts/check_all.py`, and `waves_draft.json` for the 184 cities left.
- **When it reports:** read both scripts, run their selftests and
  `check_all.py`, register them, commit, push only with the owner's yes
  (scripts and docs, no `app/` change, no reboot).
- **Then, with the owner's yes on each:** a rollout worktree and branch of
  its own from master (never this one, never wave 1's); the waves file and
  plan there; the first unattended night. The owner must keep the machine
  awake.
- **Facts the night depends on (2026-10-13):** `overpass-api.de` answered
  its status page but failed queries; `overpass.kumi.systems` serves data
  from May to July 2026, which the place fetch's 7-day guard refuses, so it
  is good for area lookups and boundaries only. Wave 1 has an unpinned
  queue running for its 13 unfetched cities, which holds both mirror locks
  while a city is in flight.
- 184 cities are left after wave 1's 34: Japan 92, France 24, South Korea
  16, Brazil 8, Czechia 6, Belgium 5, and 14 more countries with 1 to 3.
  `place_search_scaffold.py --draft-plan` fills the boundary relation for
  47 of them.

## Next task 2: build the owner's search rules

All rulings, with the owner's words and the measured sizes, are in
`DECISIONS.md`, 2026-10-13, "Place search: the owner's rulings on keep
against drop, personal names, private streets and the typo line". Read that
entry first; it is the specification.

- **The two measures behind it** (read-only, on the 19 built cities): their
  scripts and results are kept in `data/_place_rules_2026-10-13/`
  (`rules_measure/measure.py` holds the exact test for each of wave 1's
  suggestions, `results.json` the counts and examples;
  `rules_precedence/measure.py` and `measure2.py` hold the keep-against-drop
  tests, `summary_out.txt` the tables). The index dumps they read were not
  kept; `rules_measure/dump.py` rebuilds them through the job gate.
- **How to build:** a branch from master (`search-rules`), the rule-change
  protocol in the `place-search-city` skill: build, rebuild the 19, run
  `scripts/place_search_review.py added` and the drift check against master,
  and bring the owner EVERY changed row by class before anything lands. The
  fame test is a `wikipedia` tag of the object's own; an article that is the
  type's (Paris's Édicule Guimard), the person's (a grave) or shared does
  not count, and how to tell those apart from tags is the hard part: start
  from `subject:wikipedia`, `subject:wikidata`, a value shared by other
  rows, and the title against the name.
- **Also owed with it:** the list of what search leaves out (none exists;
  the owner: start one and retrofit the settled classes; where it is shown
  to readers is a wording question for the owner); the typo sentence at the
  end of the search bullet in `app/components.py` `render_map_help`
  ("Place names come from OpenStreetMap as its contributors wrote them, so
  a few are misspelled.", approved in its short form; an `app/` change, so
  a reboot); the second half of that ruling, a typed correct word finding a
  misspelt name, which is a matcher change still to be sized.
- **After it lands:** the 19 searched maps re-render, wave 1 takes master in
  and rebuilds; tell wave 1 at each landing (it holds private residential
  streets, described street names and a few business drops for these
  rules).

## Wave 1 (session "Search rollout wave 1", branch `search-wave1`)

- 14 of 34 indexes built and read; by-id drops applied; it knows the
  street-lines batch is on master and that every index must be rebuilt
  after it merges. It was sent every ruling above.
- Waiting on `overpass-api.de` for its other cities, Buffalo, and five
  refetches of stale caches (kitchener_waterloo, melbourne, new_orleans,
  sacramento, washington_dc).
- Its landing is the owner's: the name net with the owner's yes, the eye
  reads, one render, a push on the owner's word, a reboot, the cut-over
  message to transit-globe.

## Owner's words after this note was first written (2026-10-13)

- The list of what search leaves out goes on the What Is Excluded page as
  a section of its own; wording is a draft for the owner.
- The rollout worktree is `.claude/worktrees/search-rollout`, branch
  `search-rollout` (accepted; dedicated names); the screen may turn off,
  the machine stays awake.
- Pushing the runner's scripts once they pass is approved. The two docs
  commits are pushed (master `89c3ff24`).
- transit-globe was told the id side file is ready; the cut-over message at
  wave 1's landing is still owed.

## State after the owner's "run all open items" (2026-10-13, about 08:15Z)

- **master = `f549e6a8`**: the two runner scripts, registered (70 of 70
  checks). The area lookup's query has still never been answered by a live
  mirror: a two-city trial timed out on `overpass.kumi.systems`, whose
  status page took 79 s; `overpass-api.de` gave no answer.
- **The night runner is running** from `.claude/worktrees/search-rollout`
  (branch `search-rollout`), a background command of the Cleanup session,
  `--max-hours 14`. Its files are in `data/_search_rollout/`: `waves.json`,
  `plan.json`, `night_2026-10-13.md` (the morning report), `.json` (state),
  `.log`. A rerun with the same state file resumes; lookups that failed
  while the mirrors were down are only asked again by a rerun. Open before
  its output is trusted: 36 draft-filled relations nobody confirmed, and
  Japan auto-filled at admin level 7.
- **The rules build is running** in a subagent on
  `.claude/worktrees/search-rules` (branch `search-rules`), with wave 1's
  four new gaps; its changed-row report goes to
  `data/_place_rules_2026-10-13/build/changed_rows.md`, for the owner
  before anything lands.
- Wave 1 was told both (18 of 34 built, 23 fetched).

## Small open items

- London's tile 2 of 12 is May 2026 data; the owner approved a refetch from
  `overpass-api.de` when it answers, then a rebuild with the changed rows
  reported.
- Two phone-width label overlaps already on master (Pittsburgh's "PRT
  Silver Line" against the collapsed legend at 343 and 375 px; two Yokohama
  line names at 343 px): for the parked label batch.
- `outputs/testville/`, an empty folder from September, not in git: the
  owner has not said to delete it.
- Not tested by anyone: the new features on an iPhone and in Safari on a
  Mac (the owner's), and the "street row with no line" branch of the ring
  failsafe (no built city the test used has one).
- Mention whenever the owner asks what is next: the tram rescope stays
  parked.

## Added later on 2026-10-13 (the owner's words; DECISIONS has the entry)

- **Priority: the search-rules landing**, for Visuals' motion opener. When
  the rules agent reports: read `changed_rows.md`, bring the owner every
  changed row by class, and answer Visuals on its five searched names.
- **The extract route** (Geofabrik `.osm.pbf`, filtered here) is proved on
  Tbilisi and Seattle and is being built by an agent on
  `.claude/worktrees/place-extract`; the fetch order between Overpass and
  extracts is the owner's call after its timings. Prototype and comparison
  tools: `data/_osm_extracts/proto/`.
- **Queued for after the rules landing:** keep streets that run along the
  border of two included municipalities (owner approved the queueing, not
  yet the changed rows).
- The night runner is on `overpass.kumi.systems` only until wave 1 says its
  queue on `overpass-api.de` is done; then rerun with `--retry-failed`.
- The owner is running the iPhone and Safari test of the landed features.
- `outputs/testville/` is deleted.
- **The tram rescope is no longer parked** (the owner, 2026-10-13: "tram
  rescope should be another item after the next land"): queued after the
  rules landing, beside the shared-border streets; order between the two
  not decided. Re-check `docs/tram_rescope_estimate.md` and
  `docs/tram_rescope_specs.md` before proposing a first batch.
- **When the tram rescope lands, mark its cities for review downstream**
  (the owner, 2026-10-13: "we should make sure those cities are marked for
  review in analytics/visuals when it is time"). A rescoped city gains
  stations and rings, so its station counts, ring shares and any analysis
  or card built on them are stale: name every rescoped city, with what
  changed, in the downstream note to Analytics and Visuals at that landing
  (`scripts/downstream_changes.py`; `docs/session_roles.md`). Candidates
  today: Montreal, Rome, Madrid, San Francisco, Paris, then Barcelona and
  Mexico City.

## State after the rules landing (2026-10-13)

- Rules landed on master at 86aadced; the owner rebooted; the live Prague
  index matches the committed bytes. Local commits after it (skill text, the
  read-tier call, the ordering entry) ride with the next push.
- Next, in the owner's order: shared-border streets (in the extract route,
  with a changed-row report), the rollout batches on the extract route, the
  tram rescope in parallel. Held out of the waves as the last batch: Madrid,
  Rome, Milan, Toronto. San Francisco (wave 1) is an open question.
- Reads: top model for stations, places and landmarks; Sonnet for the street
  screen (place-search-city skill, step 5).
- Transit-globe's messages go to its main-checkout session now.
