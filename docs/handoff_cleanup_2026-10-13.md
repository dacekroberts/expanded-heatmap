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

## State after the last place-search landing (2026-10-13, night)

**HOLD until Sunday 2026-10-18, 12:05.** Place search is on all 237 maps, pushed in one push at master 3e16745d (2026-10-13, about 23:52 by the remote-tracking reflog; pre-push `check_all.py` 73 of 73). The owner said to hold after the last landing, and the queue below is tabled for that week (usage ran out). The scheduled task `place-search-post-landing` fires at that time and starts it; it is enabled and set for 2026-10-18 12:05. Until then: no new build, no rule change, no push. Only a removal request (honored at once) or the owner's own word moves anything.

---

- **master = 3e16745d**, pushed on the owner's go. The remote master before it was e0138000, so the push also carried d6effbef (heavy-job cap to eight) and 42c2feb8 (the extract run's decisions). App reboot: started by the owner right after the push; a live check is the owner's.
- **Every slice carries the shared rules of `search-rules-8`** (station commits 8d45eae5 and 0321cbb0, landmark patch a4718e28, brand and shop rulings 1a0fedba). Every slice passed deploy-verify in the app, and `check_map_search.js` found every drawn station and line on all 237 maps.

| Order | Slice | Branch head | Cities | Landing commit | Pushed maps rendered by it |
|---|---|---|---|---|---|
| 1 | Wave 1 | search-wave1 07bb58b9 | 34 indexes (33 English-language cities and Toronto's search) | 5e5b5f37 | 34 (Toronto's pushed map is this render, streetcars included) |
| 2 | First slice | tram-rescope 94506837 | the 17 cities searched before, Mexico City (Regional), Prague, Milan | 9736df8b | 20 |
| 3 | Final group | search-final e26eef10 (worktree `xenodochial-sammet-fdb8c0`) | 32 | 77103203 | 32, re-rendered on the merged tree |
| 4 | Extract run | search-rollout 08c8c3a0 | 151 | 3e16745d | 151, re-rendered on the merged tree |

- **The tram rescope landed with the push:** Toronto (eight streetcar lines; 108 to 174 stations, 8,749 to 11,803 storefronts in rings), Milan (17 tram lines; 193 stations drawn, 41,510 to 45,999 in rings), Prague (28 tram routes; 196 stations drawn, 17,528 to 21,462 in rings), Mexico City (Regional) (Cablebús, Mexicable, Tlalnepantla de Baz; 407,628 to 427,121 storefronts, 149,980 to 175,939 in rings). Barcelona's page says why its trams are not drawn. Its dated re-checks are item E below.
- **What went out after the push** (tick each, with the time; drafts and final texts in `data/_search_rollout/notes_drafts/`):
  - [x] (sent 2026-10-14, just after midnight) Visuals and Analytics: the downstream note (`downstream_visuals_analytics.final.md`; `python scripts/downstream_changes.py 1b5f4df8 origin/master` output pasted in), with the four rescoped cities marked for review. "Last noted" in `docs/session_roles.md` is now 3e16745d.
  - [x] (sent, to the session "Transit-globe phase 1") transit-globe main-checkout session: the search handoff and "rollout complete" (`transit_globe_search_handoff.final.md`). It says the indexes are final and that the start of the app's own search build is the owner's call; the message itself does not end that hold.
  - [x] (sent with the downstream note) Visuals: the motion opener's search-name re-check (`motion_opener_recheck.final.md`); all five names hold on 3e16745d, and Mexico City's figures changed.
- **Open on the landed master, for the week of 2026-10-18:** check H has no known gap left (`KNOWN_GAPS` is empty; Mexico City's closed with its rebuild over Tlalnepantla de Baz). `app/ring_shares.json` is current: every map_blob matches its pushed `heatmap.html`, and in_ring changed for the four rescoped cities only. No check failed or was skipped at the push. The deploy-verify checks of the app pages ran per slice before landing; a live check after the reboot is the owner's.
- **Heavy-job cap:** already back to four on master (`MAX_JOBS = 4` in `scripts/heavy_job.py` at 3e16745d), so that part of A3 is done; the queue's "at most eight" line no longer applies.
- **Worktrees now finished, for item A3 (none removed tonight):** `tram-rescope`, `search-wave1`, `xenodochial-sammet-fdb8c0`, `search-rollout`, `search-rules-8` and the other search lanes. Unlink each `data` junction with `cmd /c rmdir` first.

### Next week's queue (a full copy of `data/_search_rollout/post_landing_queue.md` as of 2026-10-13 23:52, owner-approved)

#### Place search: work queued for after the last landing

Owner, 2026-10-13: hold after the last landing; these items are tabled for
the week of 2026-10-18 (usage ran out). Queued to start Sunday 2026-10-18,
12:05. Nothing here is approved to push: each item that changes `app/` or a
rule comes to the owner with a recommendation first.

Before starting: read `git log origin/master` to see which slices landed
(first slice, wave 1, final group, extract run). A slice that did NOT land
is finished first, in that order, each on the owner's go.

##### Lanes (who does what; Cleanup coordinates and keeps every merge and push)

Start A at once. Run lanes 1 to 5 in parallel as subagents, each in its own
worktree and branch off the landed master, each prompt forbidding network
use and any email address or personal data in a request. Lane 6 waits for
the owner. At most eight heavy jobs through `scripts/heavy_job.py` until
the cap goes back to four at the end of A.

| Lane | Branch | Items | Output |
|---|---|---|---|
| Cleanup (this session) | worktree-cleanup | all of A; folds drafts; brings B to the owner in one batch | pushes on the owner's go |
| 1 Station rows | search-stations-2 | C: one stop in several rows (Berlin, Brussels Regional, Geneva, Cluj, Gelsenkirchen, Barcelona, Taipei, Tokyo Ryogoku) | reach measured, a rules commit, a fold check by a second agent |
| 2 Search script | search-script-2 | C: "Station not on this map" beside a pin, fused "str.", kanji numerals and variant pairs, Czech dotted abbreviations, the check that reads index rows | one script commit, browser-confirmed; all maps re-render ONCE after lanes 1 to 3 land |
| 3 Landmark rules | search-landmarks-2 | C: branch tag on worship rows, Porto Alegre numbered squares, entry equal to the operator's, the way-geometry twin test in shared code | reach measured, a rules commit |
| 4 Candidate lists | none (read-only) | B: the A/B/C/D sights list for the cities with no sights file; the borderline rows of wave 1 and the final group gathered into ONE table by class | two files for the owner, a recommendation per row |
| 5 Tram re-checks | none (read-only until a fault) | E, each on or after its date | a line in the handoff note per city |
| 6 Wider fetch | search-fetch-2 | D, only after the owner approves the source and the query plan (Overpass: one query per mirror; the owner prefers the extract route) | new cache files under new names, then rebuild |

Order of landing next week: lane 3, lane 1, lane 2, then the single render
pass and one deploy-verify per group of cities, then lane 6 if approved.

**LANDED 2026-10-13 ~23:30: all four slices in ONE push, master 3e16745d
(check_all 73/73). Done the same night: heavy-job cap back to four; notes
to Visuals, Analytics, transit-globe and the motion opener (check the
handoff note for what was sent); retrospective drafted
(`notes_drafts/retrospective.md`, see A2). Left in A: item 1 (scope check),
item 3 except the cap and the retrospective.**

##### A. Close out the landing
1. Land the scope check (branch `search-scope-check`, 45f8480d): 25 km reach
   limit with the recorded `PLACE_SCOPE_REACH_REASON` strings.
2. Notes to Visuals and Analytics (`scripts/downstream_changes.py`); the
   transit-globe search handoff (main-checkout session); the motion opener's
   search-name re-check. The owner moved the notes and the handoff to the
   night of 2026-10-13, right after the last landing, so those sessions have
   the information: check the handoff note for whether they went, and send
   only what is still owed.
3. Housekeeping: remove finished worktrees (unlink each `data` junction with
   `cmd /c rmdir` first, then `git worktree remove`) and branch-only data
   folders; heavy-job cap back to four; repo-size check; phone test;
   retrospectives; update the Cleanup handoff note and memory.

##### A2. Retrospective lessons (proposals, owner first)
Eleven lessons in `data/_search_rollout/notes_drafts/retrospective.md`, each
naming where it should live. Bring them to the owner as one batch; the
twin test in shared code and the kept-id check fit lane 3, the offline
browser checks lane 2.

Also: a deploy-verify run on 2026-10-13 sent Streamlit's anonymous usage
metrics to webhooks.fivetran.com (no personal data) because the launcher
did not read `.streamlit/config.toml`. Proposal: set
`browser.gatherUsageStats = false` in `.streamlit/config.toml` and have
the deploy-verify agent always pass the flag.

##### B. Owner calls still open (each has a recommendation in the named file)
- Wave 1 borderline rows: `data/_search_rollout/wave1_rules56/helper_applied.md`.
- Final group borderline rows: `final_rules56/screen_helper/*.tsv` (borderline),
  and the 312 helper borderlines in `final_rules56/pattern_screen_borderline.tsv`
  (by class in `pattern_screen.md`: body halls 60, plaza names 35, one object
  labeled many times 33, near-duplicates 24).
- Keep list group D, 20 rows: `keep_candidates_wave1_final.tsv`.
- Sights named only in helper reports (14 wave 1 cities Minneapolis to
  Tucson, most final-group cities): build the same A/B/C/D list for them.
- Goteborg Kemigarden and Brasilia Galeria dos Estados (bare park outlines
  under a dropped name).
- Rows admitted by the brand/shop rule (1a0fedba) that sit close to a chain
  branch, let in on 2026-10-13 for a second look: Harvey Nichols (London;
  its article is the company's), Ahlens (Stockholm flagship), Legoland
  Discovery Center (Tokyo), and Tokyo's デハ268号 (a preserved railcar
  under its class's article) and 新宿眼科画廊 (a dealer's gallery; the
  2026-10-11 precedent counts it as the business). Detail: `search-rules-8` worktree,
  `data/_search_rollout/reads_rules56/part9_landmarks.md`.
- Historic houses held out by the home rule (Lougheed, Rutherford, Dalmeny,
  Fort Pitt Block House): keep by id or not.

##### C. Rule work (measure reach first, then recommend)
- Kept-id admission refuses a kept id as `same_name_near` against a row an
  earlier rule already removed: Chicago's Pullman Administration Building
  (way/210701534, in `PLACE_KEPT`) has no row. Fix in
  `pipeline/place_index.py` (lane 3), rebuild Chicago, confirm the row.
- Stations: one stop in several rows that the map draws as one point. Berlin
  55 sets (S, U, tram), Brussels Regional 17, Geneva 14 (bracketed platform
  letters), Cluj 10 (Nord/Sud), Gelsenkirchen 2, Barcelona-Placa Catalunya
  and Espanya, Taipei's three spellings, Tokyo Toei Ryogoku folded into JR's
  row 417 m away. File: `final_rules56/station_pairs.md`. Also Sacramento's
  Dos Rios: drawn, no station row within 300 m (nearest 1,047 m).
- Search script: an index station row within 150 m of a drawn pin shown as
  "Station not on this map" (Berlin 42, Toronto 40, Marseille 3); fused
  "str." for Strasse. Confirm in a browser first.
  File: `tram_rules56/drawn_without_row.md`.
- Search script: kanji numeral before chome and four variant character
  pairs (34 stations in 9 cities). File:
  `extract_rules56/drawn_cjk_without_row.md`.
- `check_map_search.js` never looks at index station rows: add a test that does.
- Czech trailing-dot abbreviations ("sv.", "ul.").
- Link radius of an index stop to the nearest drawn pin: Philadelphia's
  "Girard Avenue & 5th Street" opens "Girard Av & 7th St", 243 m away
  (deploy-verify, 2026-10-13). New York: "86 St", "Canal St", "Fulton St"
  stations rank past a phone's four results (warnings).
- Worship rows named by a denomination with the real name in a `branch` tag
  (22 in the final group): read the branch tag.
- Porto Alegre's about 60 "Praca N" squares.
- National Archives (Washington): entry equal to `operator:wikidata`
  defeats the own-article test; six more government buildings of that shape.
- Twin test in every lane must place ways from cached nodes (63% of dropped
  ids could not be placed by the first script).

##### D. Wider fetch (a source question: owner first)
Famous places not in the caches at all: Chrysler Building, Yokohama
Landmark Tower, Sapporo Dome, Erasmusbrug, Casa Rosada, Dogo Onsen,
European Parliament, Mito's Kodokan, Albert Dock, West Edmonton Mall,
Glasgow Necropolis, Tidal Basin, Copenhagen's Little Mermaid, Rome's
Colonna Traiana, Guadalajara's Templo Expiatorio, Brasilia's Palacio do
Planalto and Itamaraty, Stockholm's Kaknastornet, Ostermalms saluhall and
Hagaparken, Taipei's arena (小巨蛋); cemeteries (`landuse=cemetery`: Glasnevin,
Greyfriars); nine drawn stations with no rail object nearby (Takamatsu 5,
Aomori, Suita, Nagasaki, Tokyo Shibaura-futo); Paris Chateau de Vincennes;
and the "not in the cache" lists in the helpers' reports.

##### E. Dated tram re-checks
Milan from 2026-10-19; Prague after 2026-10-26; Toronto after 2026-10-31;
Rome after 2026-11-23.
