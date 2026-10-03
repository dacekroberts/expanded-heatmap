# DECISIONS drafts - visuals (`visual-handoff`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - City card layout approved; Tbilisi's card carries თბილისი (owner)

- **The card layout and its new wording were approved** (owner): the
  eyebrow, "X% of N mapped", "Set A rings" / "Set B rings", "Full credits:",
  and the "NOT FOR PUBLIC USE · OPEN TERMS QUESTION" chip.
- **Tbilisi's card shows თბილისი** (owner), set in Noto Sans Georgian with
  `lang="ka"`, since Space Grotesk has no Georgian glyphs. Rejected: the
  Latin name alone.

### 2026-10-02 - Phase 4 city cards: credit placement, OpenStreetMap rule, site address (owner); spot-check set built

- **Phase 3 approved** (owner).
- **Card credits split between the card face and a caption** (cleanup
  session's reading of the terms, 2026-10-02; owner's calls):
  - **On the face:**
    - "© OpenStreetMap contributors · openstreetmap.org/copyright" for every
      city whose rail comes from OpenStreetMap: the 52 cities in `_OSM_RAIL`
      on branch `claude/nice-boyd-51dea8`. The station counts and distance
      bands are computed from OSM's stations, so the credit applies though
      no map is drawn.
    - Taitō ward's own short form on Tokyo's card (owner, through cleanup).
    - Entur's logo and line on Oslo and Bergen.
    - "Full credits:" and the city page's address on the site, which the
      owner allowed to be printed.
  - **In the caption:** every other notice, in full, from that branch's
    `city_notices()` (the approved per-page plan, landing at review time),
    plus the page's own source lines (SIRENE's "Source : Insee").
  - Rejected: the OSM credit on every card. The owner's rule is "only where
    its data is drawn", and a card for a GTFS city draws nothing from OSM.
- **Native-script names** come from each city's config: `MUNICIPALITY`
  (Japan), `BOUNDARY_NAME` (Korea), `CITY_NAME_ZH` and the address
  prefixes (Taiwan). Hong Kong's 香港 is not in its config; it was supplied
  as the city's own name.
- **A spot-check set of 49 cards was built.** It holds every East Asian
  city plus San Diego, Philadelphia, Toronto, Paris, Berlin, Birmingham,
  Oslo, Glasgow, Pittsburgh, Amsterdam and the three smallest networks. In
  every card, pins equal `ring_shares.json` and the layer counts equal the
  bucket counts.
  - Cities with an open terms question carry a "not for public use" chip.
  - Generation of all 144 waits for cleanup's per-notice placement table
    for the non-Japanese cities.

### 2026-10-02 - Phase 3 project-level pieces drafted on a private design canvas

- **Nine artboards, generated from the sampler's data** (built from
  published files at `f3409f4b`, Set A 86 cities and Set B 58 asserted):
  - the title card at 1280x640, the README banner at 1280x320 and a video
    thumbnail at 1280x720;
  - the method explainer and a two-ring-sets slide;
  - "Why the city maps differ" (nine tiles from
    `docs/map_inconsistencies.md`) and the taxonomy explainer (50
    classifications);
  - the coverage overview, with no basemap and Europe and East Asia
    insets;
  - the cut-down data funnel.
- **The funnel uses San Diego, Toronto and Paris; Tokyo waits** for the
  cleanup session's reading of whether its credit may sit in a caption.
- **Nothing on the canvas draws OpenStreetMap data**, so no OSM credit
  appears. The coverage overview shows only city positions and tiers from
  `app/cities.py`.

### 2026-10-02 - Phase 2 sampler approved: no basemap for now, a cut-down funnel, every city labeled (owner)

- **The sampler and all its new wording were approved as written**, and
  Phase 3 (project-level pieces) started.
- **The coverage overview stays without a basemap** until the owner decides
  which map is final. Rejected for now: the CARTO basemap of the site's
  overview, which would add the CARTO and OpenStreetMap credits.
- **The data funnel ships cut down**: storefronts mapped, then near a
  station, with register rows reading "not published". It is replaced
  when raw register counts are published for every city.
- **The distribution view is two scrolling alphabetical columns**, one per
  ring set, every city labeled, never ranked.
- **Tokyo's card credit (a short form on the card, the full notice in a
  caption) went to the cleanup session as a license question** at the
  owner's request. Cards are not generated at scale until it is answered.

### 2026-10-02 - Paris back in public visuals; Phase 2 sampler built; Set A is 86 cities (owner)

- **Paris may appear in public presentation pieces** (owner, in the visuals
  chat, after the cleanup session recorded the owner's ruling on master,
  `9c8ea3ab`, "Paris stays published after the repository-link gap"). The
  repository link landed in `bd23a18e`.
  - A Paris figure carries Île-de-France Mobilités' notice with its two links
    (notice 24, verbatim) and the snapshot line from
    `outputs/paris/provenance.json`.
  - It also carries the INSEE line the Paris page shows.
  - Supersedes the hold-out of Paris in this file's Phase 0 entry. The other
    held-out cities are unchanged.
- **Ring-set counts corrected: Set A is 86 cities, Set B 58.** The Phase 0
  figure of 84 left out Seoul and Mexico City, the two maps the survey parse
  did not reach behind the memory gate. Both are Set A, read from their
  configs. Corrected in the design system's brand book and RingSchematic.
- **The Phase 2 sampler was built as a private artifact** from published
  files at `f3409f4b`: `app/cities.py`, `app/ring_shares.json`, the city
  configs, the committed maps' pin counts, and the site's notices. The
  analytics session's pilot results were read from `data/_analysis/results/`
  at `13dceb1d`, and every panel built from them carries the acknowledgement.
  Its new wording waits for the owner's review.

### 2026-10-02 - Presentation design system approved (Phase 1): dark-first, every ring figure in Set B's proportions (owner)

- **Every ring figure is drawn in Set B's proportions**, rings at 1/6, 1/3,
  2/3 and 1 of the outer radius, whatever the city's ring set (owner, choosing
  among three readings of "drop type A for the more visually favorable B").
  - Set B (0.05/0.1/0.2/0.3 mi) is then to scale. A Set A figure keeps its
    real labels (0.1/0.2/0.3/0.6 mi) and says "not to scale".
  - Replaces the drafted Set A scale break. Set A at its true 1:2:3:6
    proportions let the outer ring dominate.
  - Rejected: showing only Set B diagrams, and featuring only the 58 Set B
    cities, which would change which cities appear rather than how rings are
    drawn.
  - All 144 cities keep their real edges and counts.
- **Presentation pieces are dark-first, on the midnight slate base.** `dark`
  is the design system's first theme; light remains.
- **The brand book was approved, in American spelling.** The comparability
  callout reuses `docs/map_inconsistencies.md` section 1's reader sentence
  with "license".
- **Space Mono and the slate band ramp were approved** as presentation-only
  additions.
- **The analysis acknowledgement was confirmed here, word for word:** "AI-driven analysis. Generated by an AI system (Claude) from this project's published map data, with the same method and rules for every city. It describes associations, not causes. Private: not part of the published site."

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
