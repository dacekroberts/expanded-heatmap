# Reverse handoff: Cleanup on the Teams account, back to Max (2026-10-18)

A running list, kept as the work happens (owner, 2026-10-16, relayed by
portfolio-ops), so nothing is lost if a session ends early. The forward
note, `docs/handoff_account_switch_2026-10-16.md`, stays unedited;
corrections to it go here.

## Commits
- 37b81439, 581155e4: the forward handoff (written on Max). Not pushed.
- This file (local commit). Not pushed.

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
- A misdirected transit-globe pricing message was withdrawn; nothing from
  it is recorded.

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
- A0: started 2026-10-16 (read-only review).
