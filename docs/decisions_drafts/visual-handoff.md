# DECISIONS drafts - visuals (`visual-handoff`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - Presentation design system drafted (Phase 1): colour by meaning, the overview map's mode colours corrected

- **The visuals design system was drafted as a private Design System
  artifact** for the owner's Phase 1 review. Values come from
  `pipeline/theme.py`, `.streamlit/config.toml`, `pipeline/taxonomies`
  (CATEGORY_BUCKETS), `pipeline/map_common.py` (HEAT_GRADIENT) and
  `app/Overview.py` (MODES, FILLS). Type sizes were measured on the running
  lean app: h1 44px, h2 36px, h3 28px, h4 24px, body 16px, caption 14px,
  notices 12.8px.
- **The overview map's three colours mean MODE, not coverage.** Metro
  `#0d9488`, light rail `#9333EA`, tram `#C2410C` (`app/Overview.py` MODES).
  Coverage is the dot's FILL: solid, the lower half, or a hollow ring. The
  visuals handoff's section 3 had the three colours as coverage tiers, and the
  first drill sheet repeated it; the drill sheet was corrected.
- **Two presentation-only additions, everything else from the site:**
  - a distance-band ramp, `band-1` to `band-4` (slate, light
    `#2c3e50`/`#4a6680`/`#6d87a3`/`#98adc3`, dark
    `#e2eaf5`/`#b4c4dc`/`#8499b9`/`#5b6f91`). It passed the dataviz
    skill's ordinal checks in both themes. Rejected: reusing the heat
    gradient, which already means density.
  - Space Mono for measurements. It is the companion face Space Grotesk was
    drawn from; the site itself has no monospace face.
- **One source value is kept although it misses 4.5:1:** the light teal
  `#0d9488` measures 3.7:1 on white. It stays the site's own colour; the
  design system limits it to marks, focus rings, large text and underlined
  links.

### 2026-10-02 - Presentation visuals: Phase 0 survey approved; public hold-outs, Entur's logo, the sampler cities (owner)

- **The Phase 0 survey was approved.** Read-only, at `766abf81`, from a parse
  of every committed map (scratch scripts, nothing in `outputs/` or `app/`).
  - 144 cities. In every map parsed, pins equalled the first heat layer and
    `app/ring_shares.json` `in_ring`. The second heat layer equalled
    `ring_shares.json` `all` and `app/macro_facts.json`.
  - Ring sets: 84 cities on [0, 0.1, 0.2, 0.3, 0.6] mi, 58 on
    [0, 0.05, 0.1, 0.2, 0.3] mi. `docs/map_inconsistencies.md` section 6 lists
    11, and `pipeline/new_york/config.py` still calls New York the only one.
    Both reported, not changed.
  - The pin row decoded as [lat, lon, name, classification index, nearest
    station index, ring band index] (`pipeline/map_common.py`
    `add_pin_layer`). The analytics session read it the same way.
- **Public presentation pieces leave out every city with an open terms
  question:** Philadelphia, Seattle (Regional), Paris, Barcelona, Dublin,
  Washington D.C., Daegu, Den Haag, Bucharest, the nine Brazilian cities,
  Milan and Miami (Regional). Source: `docs/licence_positions.md` and the
  notices in `app/components.py`. Private pieces may show them. Rejected:
  featuring them with a caveat, which would publish data whose terms are not
  settled.
- **Paris stays out until the site links its public repository.** Licence
  Mobilités Art. 5.8 is discharged by that link, and Art. 11.1 ends the
  licence on breach. Raised with the cleanup session at the owner's request;
  staging had already passed the link to cleanup (`5813011a`).
- **Oslo and Bergen visuals that draw Entur's data may carry Entur's logo**, an
  exception to the no-agency-logo rule. Entur specifies its credit as "Data
  made available by Entur" plus the logo (`docs/data_sources.md` notice 29).
  Its conditions apply: Entur's own unaltered file
  (`app/assets/entur/Enturlogo_Blue_RGB.svg`), on a white chip, at least
  20 px, beside the credit text, and nothing implying endorsement (NLOD §6).
- **The sampler uses San Diego, Toronto and Tokyo** (owner). These are three
  of the analytics session's four pilots; Paris, the fourth, stays private.

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
