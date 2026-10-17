# Reverse handoff: Cleanup on the Teams account, back to Max (2026-10-18)

A running list, kept as the work happens (owner, 2026-10-16, relayed by
portfolio-ops), so nothing is lost if a session ends early. The forward
note, `docs/handoff_account_switch_2026-10-16.md`, stays unedited;
corrections to it go here.

## Commits
- 37b81439, 581155e4: the forward handoff (written on Max). Not pushed.
- b3ca4b08: this file. Not pushed.
- b5d35b81: A0 credit (option B) and the legend clamp for a wrapped credit.
  Not pushed.
- f95e1af5: the rights-tag wording, the no-match note. 65351d01: the
  rename (A1). 3259357e: this file.
- 9db63dca, 7d28ed26, 0ac4e4bc: lanes 3, 1 and 2 merged (with the Japan
  hold on the worship branch tag, the 150 m first-word radius and the search
  control above the layer control). e5345211: search-scope-check merged.
- fc6ec797: lane 4's drops and keeps, every index rebuilt, the DECISIONS
  entry. 559bf919: all 237 maps re-rendered.
- PUSHED 2026-10-16: origin/master dd621ee3 -> 559bf919 (73 of 73 checks);
  the owner rebooted the app.
- After the push (not yet pushed): the README header redrawn with the new
  name (Visuals' generator at 559bf919).

## Artifact changes
None yet.

## Owner's new calls (2026-10-16)
- The Sunday hold is lifted: it was a Max usage issue only. The queue can
  start now, each item still on the owner's go.
- The scheduled task `place-search-post-landing` is NOT recreated on Teams;
  the owner starts the queue by hand. The Max account's copy may still fire
  on 2026-10-18 12:05; recommended: disable it from Max.
- Shared artifacts read as "writer" from Teams, and a change MAY land in
  the original: snapshots of the previous versions exist. Each change still
  needs the owner's yes, artifact by artifact. Relayed to the transit-globe,
  climate-whiplash-prediction and portfolio-ops sessions; Visuals and
  Analytics were not open on Teams and still need it.
- The owned opener artifact (AMA6fUisnkixBSwXZPj3mP, Teams) is edited only
  on the owner's ask; snapshot `snapshot-atlas-opener-2026-10-16.zip`.
- Usage limit on Teams lifted until 4 pm 2026-10-17 (memory updated).
- A0 option B: standard layer "Heatmap and overlays (c) Dace Roberts",
  Travel keeps "Map design"; keep that wording, fix the legend clamp
  instead; rights-tag wording approved.
- Renders and reboots wait until the smaller changes are in: one pass.
- A misdirected transit-globe pricing message was withdrawn; nothing from
  it is recorded.
- The post-landing batch: "All 15 as recommended" (DECISIONS, 2026-10-16,
  "the post-landing batch"). Held back for the owner: four lane 4 drops that
  reverse 2026-10-13 rulings: four drops, five keeps (DECISIONS).
- Transit-globe asked for the search boundaries (owner's ask, as a
  build-time check only). Answered: they are the "area" key of each
  app/static/places/<slug>.json, unchanged by this push, readable from
  master now.
- The heavy-job gate's 161 "measured peaks" lines are history, not holds;
  kept (owner: "good catch").

## Assumptions in the forward note, as tested
- Memory loads: TRUE.
- The scheduled task fires on Teams: FALSE (no tasks on Teams).
- Cross-session messages arrive: TRUE for sessions open on Teams;
  Visuals and Analytics were not open, so untested for them.
- Shared artifacts read as "writer": TRUE.

## Corrections to the forward note
- HEAD at the switch was 581155e4, one commit after the 37b81439 the
  opening prompt named.
- The storyboard link UboKrruPJwRAinCdi92Y2a does not open on Teams; the
  owner's link DcNUJToiEeQ6PYAsFbxtNP does (out of date, history only).
- The Visuals notes live in the main checkout's `visuals/` (current to
  2026-10-14), not in the `visual` worktree.
- A0 removes the project's "Map design" credit from the standard
  OpenStreetMap layer; it does not add one.
- Memory's opener description (third draft, 2:59, Calgary first) is out of
  date: the film is 3:35, 23 scenes, Rome, Seoul, Taipei, Paris, Sao Paulo,
  Mexico City, already titled Global Transit-Business Atlas.

## Queue progress
- LANDED 2026-10-16 in 559bf919: A0, A1, lanes 1 to 4, the scope check.
- Post-push: the social preview (visuals/repo/social-preview.png) is for
  the owner to upload on GitHub, along with the About text. The downstream
  note for Visuals and Analytics is at data/_handoffs/downstream_2026-10-16.md.
  Transit-globe got the boundaries answer and a senior-to-junior note
  (data/_handoffs/transit_globe/).
- A0: code done 2026-10-16 (option B; legend clamp; rights tag approved).
  Render deferred (owner): one pass after A1 and lanes 1 to 3.
- Lane 2's no-match wording: code done, rides the same render.
- A1: committed 65351d01 (SITE_NAME, README, 237 city page titles,
  scaffold). Owed after the push: header and social images (Visuals'
  generator reads master), GitHub About text, share-link preview check.
- Lanes 1 to 4 reported and are merged or applied (branches
  search-stations-2 b88c5abf, search-script-2 c6978521,
  search-landmarks-2 310df837; lane 4's lists in
  data/_search_rollout/lane4/). A item 1 (scope check) merged.
- Parked: Dos Rios (Sacramento, no station object in the cache), New York's
  ranking warnings, the worship branch tag on Japanese maps (eye-read Tokyo
  and Osaka first), the per-city sights pass, the nine held lane 4 rows (four decided 2026-10-16: DECISIONS).
- Still owed: lane 5 tram re-checks on their dates; agent worktrees to
  remove after the merge (owner approved).

## Hand-back to Max (2026-10-17, Cleanup on Teams)

The owner asked for this once Cleanup, Visuals and Analytics were all idle;
all three were (Visuals' child session `carousels-republish` too). The
sections above are history as of 2026-10-16; where they disagree with this
one, this one is current.

### State
- **origin/master = 2509f33a**, every Cleanup commit pushed, the cleanup
  worktree clean. 73 of 73 pre-push checks on the last push.
- The owner rebooted the app after a6ff41fa (the Last Global Sweep). Every
  later push was docs only: no reboot owed.
- Worktrees left: cleanup, analytics, visual. GitHub has only master.
- **The owner is away until 2026-11-05.** Nothing is due before then.

### Pushed since 559bf919
- b70d4c8c README header with the new name. 3bfc131c four held lane 4 rows
  decided. df61e14d Sacramento's Dos Rios in place search.
- 5b8aecb1, c3685e16: the close-out to maintenance (PLAN rewritten to
  maintenance, handoffs moved to `docs/handoffs/`, CLAUDE.md and
  project_context status).
- ff29d056: Streamlit usage metrics off (config.toml and deploy-verify).
- 5a439ff7, 567d91fc: the worship branch tag lifted on Japanese maps (25
  maps re-rendered, 4 Tokyo drops); the place_index selftest path fix.
- 156cd4d4: Sacramento's Green Line (every 30 minutes, not drawn).
- a6ff41fa, 3ab4c506: "Last Global Sweep" on the front page, read from
  `app/global_sweep.json`, written only by a complete drift run.
- 31a2ec4a: four retrospectives committed (project, place search, transit
  layer, East Asia); all 13 retrospective titles start "GTBA | ".
- b3081848, b5680951: re-checks parked to 2026-11-05; Yamagata kept on its
  August list.
- bc296750, f5e7853e, 2509f33a: the search-outline teal, ruled exempt from
  line colour rules (the middle commit misread the owner and is withdrawn
  by the last).

### Owner's calls since 2026-10-16 (each in DECISIONS.md)
- No more cities; the project is in maintenance; the nine wind-down calls.
- New York's phone search ranking stays a known fault.
- The worship branch tag lifted on Japanese maps; Sacramento's Green Line
  wording approved; usage metrics off.
- Last Global Sweep: "the last time every map was re-rendered and checked;
  the full run writes the stamp and the front page reads it".
- Retrospectives committed with "GTBA |" titles.
- Re-checks parked until 2026-11-05.
- **Yamagata stays on the August list.** The September edition dropped
  about 75 restaurant permits that expired 2026-09-30 before their renewals
  reached it. Next: the October edition (about 2026-11-10), after checking
  it carries those renewals. `fetch_sources.py --force` writes under
  config's current file name: change config's names first.
- **Philadelphia's permission request: no response** as of 2026-10-17; it
  stays held.
- **The search-area outline is not a transit line**: the line colour rules
  do not bind it; Seoul's outline stays.

### For Max to do
- **Disable or delete the scheduled task `place-search-post-landing`.** It
  may fire 2026-10-18 12:05. Max could not be reached, so two notes stand
  it down meanwhile: `data/_search_rollout/CANCELLED_place-search-post-landing.md`
  and a banner on `data/_search_rollout/post_landing_queue.md` (gitignored,
  shared data). Delete both once the task is gone.
- Typed artifacts (Slides, Design, Docs) could not be edited from Teams
  (portfolio-ops' rule of 2026-10-17: HTML "before" export, a plain HTML
  checklist of exact old and new text, applied by Max or the owner). Cleanup
  changed no artifact on Teams, so no checklist is owed from here. **Visuals
  owes one:** 25 edits to the canvas, the deck and the brand book, its
  checklist at JHTgVhyNYN36qAkRcE9euS (Visuals' summary below; share the
  checklist to Max before opening it there).
- The owner's outside actions still open: the GitHub social preview
  (`visuals/repo/social-preview.png`) and About text.

### Waiting on the owner (from 2026-11-05)
- PLAN.md "Due now" and the dated re-checks: Milan, Prague, Toronto,
  Birmingham, Philadelphia's date re-read, São Paulo's lines, the weekly
  `archive_decisions.py` run (first pass will take about three weeks).
- Visuals: the typed-artifact checklist and three deletions after it (its
  summary below). Nothing from Analytics (the share card is live, the
  Food service chart closed at 167 cities).

### Analytics' summary (GTBA Analytics, 2026-10-17, as sent)
1. **State.** Branch analytics-handoff, HEAD 3bfc131c, clean, never pushed;
   by standing rule it never merges into master. Behind master (2509f33a),
   which does not matter: Analytics reads committed files through git show.
   `data/_analysis/` is gitignored as a whole (`data/_*/`), by design, in
   the shared data/ folder: the scripts (build_dashboard.py, build_share.py,
   search_stats.py, map_lines.py, cross_city_share.py and others),
   results/, register/ (swept_keys.json gained 7 keys on 2026-10-16 from
   the Toronto sweep, keys only), artifacts/dashboard.html and share.html,
   skill/SKILL.md and PENDING.md (current). The analysis is pinned at
   559bf919 (storefront and map inputs identical through 2509f33a, checked
   by decoding pins and map layers); the search stats and map lines at
   31a2ec4a.
2. **Artifacts changed from Teams** (both Max-owned, Teams as Editor):
   - Dashboard https://claude.ai/artifact/5Miq5KXeo3JVZtV1rSa8Du: version 6
     (1792223256-ce5a), published 2026-10-17 on the owner's yes; matches
     the local artifacts/dashboard.html.
   - Share page https://claude.ai/artifact/Dc87nkRqv1FktunF2Qnxaq: version
     9 (1792222890-5bfe), published 2026-10-17 on the owner's yes; matches
     the local artifacts/share.html. It carries the searchable-places card
     and the Lines column, leaves out the 10 held cities, recomputes the
     association over the 227 kept cities, and credits OpenStreetMap on
     the card.
   - The builders set the live titles, "GTBA Dashboard" and "GTBA Analysis
     (Share-Ready)", so a rebuild keeps them. The pilot pages are retired
     (owner, 2026-10-16): never rebuild them.
3. **Decisions waiting on the owner: none.** The share card is done:
   recounted at 31a2ec4a, and 2509f33a changes no outputs. The Food service
   chart is closed at 167 cities; the other 21 have no Food service source
   and are described as "no Food service source", never "pending".
   Recommendation: leave the chart as it is.
4. **For Max first.** Each artifact republish needs the owner's yes,
   artifact by artifact: read the URL first, then publish with url. The
   builders use fixed paths (REGISTRY points at
   `visuals/data/restrictions.json` in the main checkout). Rerun recipe:
   `data/_analysis/skill/SKILL.md`; rerun only after a change to pins or
   map layers on master (a search-only change needs search_stats.py and
   map_lines.py, then the two builders). Hard lines: correlational wording
   only, the AI-driven acknowledgement exactly twice per page, no
   ridership, withheld-name lists hold keys never names, analyses private
   unless the owner says so per piece.

### Visuals' summary (GTBA Visuals, 2026-10-17, as sent)
1. **State.** Worktree `.claude/worktrees/visual`, branch visual-handoff,
   HEAD c6221927 (a local merge of master b70d4c8c), 45 ahead and 16 behind
   origin/master, never pushed or merged: by the owner's rule (2026-10-04)
   it stays local and nothing from visuals lands on master.
   - One uncommitted file, `app/ring_shares.json`: modified before the
     session started, only map_blob hashes on all 237 entries (regenerated
     churn), not visuals work. Recommendation: discard it with
     `git checkout -- app/ring_shares.json`, the owner's call.
   - Visuals work is in the main checkout's `visuals/` folder (git
     excluded); the working folder is the session scratchpad
     (scratchpad/work), with copies of the generators in
     `visuals/generators/`.
   - Child session carousels-republish (local_2278ff91), in the same
     worktree with no branch of its own: published the carousels (v8) only,
     no file changes, idle.
2. **Artifacts changed from Teams.**
   - Max-owned, shared to Teams as editor (plain HTML), all titled "Global
     Transit-Business Atlas" now: city cards
     https://claude.ai/artifact/SxtgpB9t2VQtAFvnZJPSfe v24; country cards
     https://claude.ai/artifact/Bq1SVz7yEGTc2gJNUZiT1T v14; carousels
     https://claude.ai/artifact/7L5KrkABezN4GCsWJYBCy5 v8; sampler
     https://claude.ai/artifact/Dvtfz5BBiCchdHhmr5XHxq v17; chain page
     https://claude.ai/artifact/EP8PivGCT8ag7AoS9d5nPX v18. The sampler and
     chain page are dated four-city samples (2026-10-16).
   - Multi-city views: renamed by the owner by hand, "GTBA multi-city
     views"; its generator template carries the title now.
   - Teams-owned: the motion film
     https://claude.ai/artifact/AMA6fUisnkixBSwXZPj3mP (Paris search
     outline made teal #5eead4; cfg.json v5, shared.js v22); the rename
     checklist https://claude.ai/artifact/JHTgVhyNYN36qAkRcE9euS v2,
     private.
   - **Typed artifacts with a change owed:** the canvas
     (JAfMAqXo92uWN9wCUwsBRu), the deck (GtXL6Q1sQtqBFwV29dijY7) and the
     brand book (LipZedN2vU1GFQsbGe4s2P). 25 edits: 20 for the rename, 5
     for Toronto's tram-rescope figures and two commit stamps. Before
     export: `visuals/generators/before_snapshots_2026-10-17/` (51 files,
     the live project files as of 2026-10-17). Checklist:
     JHTgVhyNYN36qAkRcE9euS. Renamed sources:
     `visuals/generators/pending_rename_2026-10-16/`.
3. **Decisions waiting on the owner.**
   - After Max applies the checklist: delete the pending_rename folder, the
     before snapshots and the checklist, each confirmed at the time.
     Recommendation: yes, once a Max session has compared the applied
     edits with the checklist.
   - `app/ring_shares.json` churn: recommendation, discard it.
   - Drill sheet: its template is renamed; whether it was ever published
     is unknown. Recommendation: nothing unless the owner has a link.

   **The owner's reading (2026-10-17, to Cleanup): "The better assumption is
   those files are from main acct."** So the uncommitted
   `app/ring_shares.json` in the visual worktree, already modified when the
   Teams session began, is taken as left by a Max-account session, and the
   drill sheet as a Max artifact, if it was published. For Max: look at the
   ring_shares change from that side before discarding it, and look for the
   drill sheet in Max's own artifact list. If it is there, it is a typed or
   plain page to rename like the others.
4. **For Max first.**
   - The checklist is private to Teams: share it to the Max account before
     opening it there.
   - A shared link returns 404 on an account until the owner opens it there
     once while signed in; repeated 404s make the tool drop the link for
     the session.
   - Typed artifacts refuse publishes from the non-owning account (deploy
     422); plain HTML can be republished by an editor on either account.
   - Toronto's figures on Carousel 4, the Funnel board and deck slide 08
     are real data changes, not wording: apply them exactly as listed
     (11,803 near a station, 64.8% of 18,215, rings 28/35/19/17%).
   - No scheduled tasks or wakeups from Visuals.

### Messages answered on Teams (no repo change)
- Transit-globe's main session is now "Transit Globe phase 2 kickoff"
  (local_2e91dca6); earlier ones are retired. Answered on 2026-10-17:
  assigned line colours, Kyoto station lists, per-country rules. The rail
  handoff for it is in `data/_handoffs/transit_globe/`
  (`rail_cities_unbuilt_2026-10-16.*`, `rail_verdicts_text_pass_2026-10-17.*`).
- Visuals: told the Seoul outline ruling. Analytics: answered the Food
  service and share card questions.

### Corrections to the sections above
- "Parked" there is settled: Dos Rios fixed in search (df61e14d); New
  York's ranking is a known fault in PLAN; the worship branch tag is lifted.
  The agent worktrees were removed.
- "The scheduled task fires on Teams: FALSE" still holds; the Max copy is
  handled above.

### Memory written on Teams
Notes in the project memory (shared on this machine): Teams artifact
editing and the typed-artifact checklist rule; the maintenance state
(retrospectives landed, away to 2026-11-05, the cancelled task); the new
transit-globe contact.
