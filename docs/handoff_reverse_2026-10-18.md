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
- Next commit: lane 4's drops and keeps, every index rebuilt, the DECISIONS
  entry. Then one 237-map render. Nothing pushed.

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
  and Osaka first), the per-city sights pass, the nine held lane 4 rows.
- Still owed: lane 5 tram re-checks on their dates; agent worktrees to
  remove after the merge (owner approved).
