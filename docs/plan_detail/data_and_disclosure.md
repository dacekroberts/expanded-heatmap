# Data-age, disclosure, category and license work

Detail moved verbatim from `PLAN.md` on 2026-10-08 (commit c75f4802); `PLAN.md` holds each item's one-line status and points here by heading.
This is open work, not a record: update an item here as it moves, and send a finished one to `docs/plan_done/`.

## Per-city restriction disclosures

- [ ] ⏸ **Per-city restriction disclosures on every city's page (owner,
  2026-09-28).** **Before any drafting, the owner looks over the live pages
  and gives general advice: ask, then wait.** Prose is drafted in chat. Four
  facts per city (the macro tooltip may carry them too): placement precision
  (register coordinates, geocode, block-level join, or road interpolation);
  data age (the rows' own newest date, not the edition's label: Busan frozen
  at 2026-04-15, Daegu's rows end 2025-08-31, Kyoto a rebuilt upper bound);
  scope (city or "(Regional)"); network type (metro, trams only, or EDGE).
  - **Borderline "Full" caveats (owner 2026-09-28)**, each on its own page,
    each staying Full: Brazil's nine (a third to half of plausible
    storefronts unreadable and dropped); New York (retail thinner, four
    registers); San Francisco and Los Angeles (9-37% of rows without an
    industry code); Taichung and Taoyuan (12-19% of storefronts in a ring).

## Per-city wait times as data

  - [ ] **Per-city wait times as data: TABLED (owner, 2026-09-30) until the
    owner is back at a desktop.** Pages state waits in hand-written prose
    (Buffalo, Houston, Sacramento, Aarhus) that nothing checks. Proposed
    (cleanup, 2026-09-30): drawn lines only; a per-line `SERVICE` config
    value (daytime minutes, optional evening/weekend range, source, as-of)
    copied to provenance and rendered by one shared helper in one approved
    sentence; a no-fetch check measuring headways from cached GTFS (OSM
    cities: source and date only). About 150-200 lines, an `app/` change.
    Open: build it, and evening/weekend waits when they differ or daytime
    only.

## Published-city date fixes

  - [ ] **Published-city date fixes (DECISIONS "Published cities' data dates
    checked", 2026-09-29):** (a) San Francisco: drop rows with a
    `location_end_date` in step 2 (4,677 of 16,495 mapped rows), re-render,
    drift-check; (b) Dublin: owner call, disclose that the valuation list
    includes vacant units, or another source; (c) NYS Retail Food Stores,
    Milan and Surrey: owner call on stating an undatable source; (d)
    Philadelphia: re-read around 2026-10-13 (frozen since 2026-08-17?); (e)
    expiry dates where a status filter leaks expired licences (Philadelphia,
    DCWP, San Diego, D.C., Calgary); (f) each source's newest row date,
    capped at the fetch date, into `data_age`. Review time.

## The category fix batch

- [ ] **The category fix batch (owner-approved 2026-09-29).**
  `scripts/check_category_continuity.py` found 45 departures from
  `docs/category_rules.md`; work list `docs/handoff_category_fixes_2026-09-29.md`.
  - Stockholm's torghandel stall waits for `stockholm-catering` to land.

## Next cross-city discrepancy audits

- [ ] **Next cross-city discrepancy audits (owner, 2026-09-29).** Read-only,
  one at a time, each ending in rules for the owner: (1) the same trade in
  different buckets (about 10 common trades through every taxonomy); (2)
  records that may not be trading (each source active-only, with closing
  dates, or neither; estimate inflation where a sample allows: Kyoto, Rome,
  the permit registers); (3) home-based and one-person registrations (share
  of pins with no employees and no premises name; privacy too). Then, as
  disclosures in `docs/map_inconsistencies.md`: (4) placement precision and
  stacking; (5) one premises counted once or several times (Milan twice,
  Calgary merged); (6) upper-floor and office premises.

## Philadelphia's permission request

- [ ] **Philadelphia's permission request** (`docs/gated_access.md` item 12;
  DECISIONS, "Philadelphia: ask for permission, stay up on a reasoned
  position meanwhile"). Sent 2026-09-21; no chase (owner, 2026-10-04); checked
  at the batch check-ins (`docs/communications/`). The footer
  (`components._UNSETTLED_TERMS`) discloses it. **Silence is not consent**,
  and must never harden into a claim that permission was given.
  - [ ] On a reply, follow the branch in that file: on permission the footer
    clause comes out entirely; on refusal Philadelphia comes off the site,
    and the eastern cities' macro label offsets need re-checking at 854 and
    1200 px (removing a marker moves `fit_view`'s bounds).

## From the prose pass's deploy check

- [ ] **From the prose pass's deploy check (2026-10-02), on master, not
  blocking:**
  - **Label crowding** (each reproduces with `scripts/check_map_labels.js`;
    all legible): Pittsburgh at 375 and 343 ("PRT Silver Line" touches the
    collapsed legend); Yokohama at 343 ("Tokyu Kodomonokuni Line" x "Tokyu
    Shin-yokohama Line"); Osaka at 1000x650 with the legend open ("JR
    Gakkentoshi Line" ~14 px under it).
  - **San Diego's page is thin:** one bullet of its own, no businesses
    section (5-22 elsewhere).
  - **Toronto's step 2 depends on the run date:** it compares future-dated
    Cancel Dates with today (18,218 -> 18,215 on 2026-10-02). Measure
    against the fetch date, or record it (date fix (f) above).

## License gaps

- [ ] **Licence gaps from staging's ranking** (`docs/licence_positions.md`,
  5813011a; its notice numbers were stripped as unreliable, so verify each
  against the code first). Done: the repository link and header icons;
  Dublin's and SFMTA's credits. Open:
  - **Credits:** Milan's ATM rail ("cc-by" never read to standard); STM's
    modification sentence; MLIT's credit, incomplete for the 20 Japanese
    cities; French operator credits render only if provenance.json parses.
  - brazil.md:177 claims an ODbL notice on station CSVs; no committed
    station CSV carries one.
  - **Missing licence rows:** Tokyo statistical yearbook, e-Stat,
    bbga/Locatus, Chitetsu and MTR figures and names; nine municipal
    boundaries (listed in the ranking).
  - **Pending positions with no recorded acceptance:** Barcelona's
    notification was never sent; SIRENE's opt-out refresh cadence; MHLW's
    open clause; four indemnities (named in the ranking).

## Deferred from the mega-review

- [ ] **Deferred from the mega-review (owner, 2026-09-30, call C2)**, each
  with a drift check of Stockholm too: Göteborg's
  `sweden_livsmedel.layer_label` (both Swedish menus say "Food shops");
  "24sju" and vending words in the Swedish name rules; the template's "ratio
  to OpenStreetMap" clause for Odense and Liepāja (an Overpass count per
  city, or drop it).

## What Is Excluded's opening claims

- [ ] **What Is Excluded's opening generalisations (review lane 4,
  2026-09-30)** no longer hold: light rail only at 15-minute headways
  (Daugavpils's hourly routes are drawn); the commuter-rail list (missing
  Zurich's S-Bahn, NS at Den Haag, Göteborg's and Odense's regional trains);
  ring sizes at :118 and :135; Florence's not-drawn list (T2.2). Rewrite by
  category.

## Gambling

- [ ] **Gambling is bucketed inconsistently** (owner, 2026-09-28): Buenos
  Aires, Brazil and Berlin exclude lottery and betting premises (NAICS 7132,
  WZ 92), but `dublin_uses` counts BETTING SHOP as Retail. Decide one rule
  and sweep every taxonomy, with a drift measurement per city changed.
