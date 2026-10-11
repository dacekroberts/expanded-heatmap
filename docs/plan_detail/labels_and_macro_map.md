# Label, legend and macro-map work

Detail moved verbatim from `PLAN.md` on 2026-10-08 (commit c75f4802); `PLAN.md` holds each item's one-line status and points here by heading.
This is open work, not a record: update an item here as it moves, and send a finished one to `docs/plan_done/`.

## After the reset, one label batch

  - **After the reset, one label batch:** Ostrava's Tram 14 label 2.1 px
    under the button row at 854 (measured 2026-10-08: the line's tip sits at
    y 37 under the row, bottom 45, boxed in by Tram 1, 2 and 18, so the
    runtime placer's least-bad spot is under the row; the fix is the row as
    an obstacle in `_layout_labels`, which moves `_choose_view` on any map
    with a tip there: measure how many of the 206 reframe first); Osaka's
    Nagahori, JR Yumesaki and Nankai Shiomibashi labels at 375; the
    Overview's 343-vs-333 scorer canvas, then Los Angeles (Regional) and
    Rio de Janeiro (Regional) re-placed.

## Overview at phone width

- [ ] **Overview at phone width (2026-10-03 review landing):**
  - **`check_macro_labels.py` assumes a 343 px canvas at 375**
    (`CANVAS = {375: 343}`); deploy-verify measured 333. Re-measure, correct,
    re-score every region.
  - **Clipped at 375:** "Los Angeles (Regional)" about 43% in Global and
    United States (no clean position) and 15% in United States West; "Rio de
    Janeiro (Regional)" about 24% in South America since the rename. Re-place
    both once the scorer canvas is corrected.

## City-map legend model

  - [ ] **City-map legend model (2026-09-30).** The label solver's open
    legend, `178 + 19 x lines`, is -32 to +114 px off across 75 cities (Oslo
    and Fukuoka fixed per city; Osaka's "JR Gakkentoshi Line" not). Fix: the
    obstacle becomes max(model, a content-based estimate). A full drift check
    (heavy) and review time.

## Macro-map label tiers

  - [ ] **Macro-map label tiers (owner 2026-09-29):** minor cities get no
    pill outside their own region, only the tooltip; anchors keep theirs.
    Europe and East Asia become composites of their sub-regions. Pilot: the
    Seoul Capital Area (minor: Incheon, Goyang, Seongnam, Yongin); France and
    Czechia after their first tram builds, once `check_macro_labels.py` has
    scored a placeholder France view at 375, 768 and 1200 px. Review time.

## Optional label follow-ups

- [ ] Optional label follow-ups (DECISIONS, "Phone-width label placer
  verified and pushed"): a few re-placed labels sit ~54 px from their tip
  (Amsterdam's Metro 51), and labels may sit on cluster bubbles, which the
  placer does not avoid.

## Vancouver (Regional) clipped

- [ ] **"Vancouver (Regional)" is clipped at the left edge at 375 px** in
  Canada and the US region (desktop fine). Options, by cost: shorten it to
  "Vancouver"; a right-side anchor; or `REGIONS[i]["zoom"]` for Canada,
  re-measuring that region's `label_offset` values.

## Map-only navigation pilot

- [~] **Evaluate the map-only navigation pilot** (started 2026-09-20;
  `docs/navigation_sidebar_and_city_links.md`). The Overview's fallback link
  list stays; each map has a "Cities" dropdown. Open: the final go/no-go. To
  revert, set `MAP_ONLY_NAV = False` in `app/cities.py`.

## Madrid's 343 px touch

- [ ] **Madrid's 343 px touch** ("Línea 5" / "Ramal Ópera–Príncipe Pío", ~0.5
  px at one corner, both readable; predates the tram batch): clears with
  Osaka's `DENSE_LABEL_SCRIPT` (measured by injection), but needs the
  trigger widened and Madrid re-rendered. Oslo's "T-bane 2" under the
  legend at 1024x768 is a different cause (the open legend).

## For the site-wide prose and UI pass

- [ ] **For the site-wide prose and UI pass (owner, 2026-09-30, calls A3,
  A6, A7, B6):** dots on top of dots (Yokohama on Tokyo,
  Kitchener–Waterloo on Toronto: older city on top, or a regional view; the
  seven pairs are `check_macro_labels.py`'s `KNOWN_STACKED`, removed as
  fixed); hide a pill whose dot is off the canvas (Bordeaux, Nice,
  Daugavpils at 375 px, as Dublin and Bucharest); a short label for a long
  regional name (Most shows "(Regional)" at 375 px); and the Korean
  nightclub difference on What Is Excluded (SEMAS satellites leave out
  dance halls, Seoul keeps nightclubs), correcting the two "as in every
  other city" sentences.
