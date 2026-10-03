# DECISIONS drafts - visuals (`visual-handoff`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - Presentation visuals: OpenStreetMap credit where its data is drawn, walking minutes at 3 mph (owner)

- **A presentation visual carries the OpenStreetMap credit only where
  OpenStreetMap data is drawn** (a basemap, or rail or stations built from
  OSM). The owner's call, on a station schematic with no basemap whose lines
  and stations come from San Diego's MTS GTFS. Rejected: the credit on every
  map regardless, which would credit OSM for data it did not supply. Every
  source that IS drawn keeps its own credit. Live maps are unchanged:
  `pipeline/map_common.py` still emits the credit on every committed map.
- **Walking minutes may accompany ring distances, at 3 mph (20 minutes per
  mile), with the metric and its rationale listed beside the visuals.**
  - 3 mph matches the transit-planning convention that a quarter mile is a
    five-minute walk.
  - Rings are straight-line distance, so minutes understate a walk along
    streets.
  - Miles stay the unit; minutes are a reading aid. Set A's edges read 2 / 4 /
    6 / 12 min, Set B's 1 / 2 / 4 / 6 min.
  - The owner asked for every visual metric to be listed with its rationale;
    the list lives on the drill sheet for now and moves to the visuals index
    (handoff Phase 7).
- **The visuals handoff moved from the main checkout's root to its inbox,
  `data/_handoff/visual/`** (owner's OK), so `check_stray_downloads.py` stops
  flagging it.

### 2026-10-02 - AI-driven deep analysis permitted, private, with an acknowledgement on every analysis (owner)

- **The invariant "Ridership and deep analysis are out of scope until asked"
  was split: ridership stays out of scope; AI-driven deep analysis is
  permitted.** The owner approved the replacement text in chat, as written,
  in the visuals session (handoff from the owner's other project, section
  0a).
  - The hard line, in the owner's words: "every analysis must always be
    accompanied by an AI-driven acknowledgement."
  - Analyses are private: shown only to the owner, never in `app/`,
    `outputs/` or any deployed page, and never in public-facing material
    unless the owner says otherwise for a specific piece.
  - Analysis stays correlational, and cross-city comparisons keep the
    comparability limits (ring sets, record kinds, vintages) disclosed.
  - Supersedes the inbox README's broader note (`data/_handoff/README.md`,
    2026-10-02) that set the invariant aside for the analytics and visual
    handoffs without the acknowledgement or privacy conditions.
  - Rejected: dropping the rule outright (ridership was not asked about),
    and leaving `docs/project_context.md`'s scope line unchanged (it would
    have contradicted `CLAUDE.md`).
  - Files: `CLAUDE.md` (Invariants), `docs/project_context.md` (Scope).
  - The acknowledgement's wording is still to be drafted in chat and
    approved once, then used unchanged on every analytic output.
