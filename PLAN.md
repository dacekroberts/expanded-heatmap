# Plan


Open work only. Completed work and the reasoning behind it live in
[`DECISIONS.md`](DECISIONS.md); the settled state is in
[`docs/project_context.md`](docs/project_context.md). Done items moved out at a
weekly archive are kept verbatim in [`docs/plan_done/`](docs/plan_done/).

Rules that make the rest work:

- **Commit after every green step.** A commit is the baseline
  `pipeline/drift_check.py` diffs against.
- **Log every judgment call in `DECISIONS.md` as it's made** (see the
  `decisions-entry` skill).
- **Live-verify a city's data before building it** (`add-city` Step 0).
- **Run `python pipeline/drift_check.py` after any pipeline change.**

Legend: `[ ]` open, `[x]` done (a done item stays only until its
`DECISIONS.md` entry exists), `[~]` in progress.

---

## Now

- [ ] **Owner: the iPhone check of the 2026-10-07 and 2026-10-08 landings.**

- [ ] **Next landing:**
  - Phase 2 Japanese cities (East-2, Kansai-2, Regional-2) and Cluj-Napoca,
    on the owner's go (Cluj-Napoca waits on call 215, the placement bar).
  - Place search, if the Kyoto pilot reports well.
  - Follow-ups: Ostrava's Tram 14 label 2 px under the button row at 854 (the
    button row is not an obstacle in `_layout_labels`); Osaka's Nagahori,
    JR Yumesaki and Nankai Shiomibashi labels overlapping at 375; a full UK
    line-colour search (Piccadilly can be blue again); about 25 older
    notices that write the day first; about 30 configs still claiming "45
    from every pin" from before olive and violet; East-1's drafts "ten"
    blank names to correct at the fold; caterers that also name a counter
    form (Fukushima's 161), the shared FORM_RULES question.
  - **Branch `legend-dot-georgia` (19551960, Cleanup's, local), lands at
    review time:** legend dots 10 px that never shrink (the owner's iPhone
    check), Tbilisi in Europe East (DECISIONS, 2026-10-08, both), and the
    phone's region dropdowns take no typing (`filter_mode=None`, owner). All
    206 maps re-render once at the landing; app reboot (`app/cities.py`).
  - `scripts/stress_overview.py` stops on master: 23 Japanese cities of the
    last batch missing from `BUILT_PREF`.
  - From Analytics (2026-10-08, measured at 5507a4cb): `map_common._LETTER`
    has no full-width Latin, so a "?" between full-width letters still
    renders (Higashiyamato 6, Tachikawa 4, Ichinomiya 3; one Tachikawa Food
    service pin labelled "?"); Saitama's new-law food types show their layer
    code and padding ("01:飲食店営業 ") as the pin category, withheld names
    too, in Ageo (Regional), Kasukabe, Sōka and Tokorozawa (`japan_eigyo`
    has no `display_value()`); Ōita's "? そうざい製造業" category (a lost
    circled numeral?); Ōita's page does not say publisher-masked names (306
    before set-asides) show the permit type.
  - Kept from the drafts' notes at the 2026-10-08 fold (the files are in
    `git show d121b2cc:docs/decisions_drafts/<name>.md`):
    - **Owner, review time: re-render the 34 built Japanese cities on
      `WAVE5_RULES`** (with `default_joined`), Toyota first (+177
      storefronts, the rest about 20 or fewer), each with a pinned
      `TERM_AS_OF`; call 158's reading goes to the owner with it
      (japan-foundation, "Review-time re-render proposal").
    - Japanese shared-code fixes (worktree-japan-regional-1, "Shared-code
      findings"): line labels anchored on in-city segments in `map_common`
      (retire Gifu's, Mito's and Morioka's `in_city_first` copies; Akita's
      Oga label), `wareki_date` YYYYMMDD, `rebuilt_register`'s ranking and
      種目 folding (re-measure Higashiōsaka), `city_rows` by magic bytes,
      the `oaza_cut` 大字 fallback, `SOURCE_LINKS` link text, Akita's yatai
      form, two `japan-city` skill lines, the `CLOSED_STATIONS` docstring.
    - Confirm five Japanese credits against their licence reads: notices
      157, 161, 178, 184, 186.
    - Correct three Kansai-1 briefs: Kakogawa (3 一円 vehicle rows name
      加古川市), Uji (the guard tests 宇治市), Toyonaka (files from June 2026
      drop 廃業年月日).

- [ ] **This week (to the 2026-10-11 reset): refinements, not builds** (owner,
  2026-10-08, weekly near its ceiling; the 10% check-ins ended). Place search,
  possibly the basemap, and the site infrastructure they need. The wave 2
  builds above wait for the reset.

- [ ] **A site-wide code audit after the reset and the final city builds**
  (owner, 2026-10-08). The last whole-project audit was 2026-09-21 at four
  cities (`docs/passover_opus5.md`, sections 9 and D); the shared code has
  grown since (`pipeline/map_common.py`, `pipeline/line_registry.py`,
  `pipeline/taxonomies/`, the national step modules, `app/`). Scope and lanes
  to be set with the owner before it starts (`docs/review_lane_kit.md`).

- [ ] **Macro-map regions:** the Europe split and Japan's views landed with
  the review (2026-10-07). Still to come: Brăila and Galați, Nagakute and
  Nisshin, Itami and Toyonaka into `KNOWN_STACKED`.

- [ ] **Review time: the Japanese pages' name-rule bullet gains the sign rule**
  (owner, 2026-10-06; DECISIONS, "the name rule's version 2"). Proposal, every
  Japanese page's variant alike: "Where a business's trade name is its
  operator's own name, or is written as a bare personal name, the dot shows its
  permit type instead." The rule itself landed 2026-10-06.

- [ ] São Paulo's Linha 6-Laranja stays out until full service (sentence
  OK'd); re-check when it leaves trial operation.

- [ ] **Overview at phone width (2026-10-03 review landing):**
  - **Split Japan West in two (owner-approved 2026-10-03).** Its zoom is
    pinned at 6.0 (REGION_ZOOM), so at 375 px 16 of its 22 dots fall off the
    canvas. Zoom is set server-side, so the fix is two views, Kansai and
    Chugoku-Shikoku-Kyushu, each placed and scored at 375, 768 and 1200
    (`check_macro_labels.py`), menu order updated.
  - **`check_macro_labels.py` assumes a 343 px canvas at 375**
    (`CANVAS = {375: 343}`); deploy-verify measured 333. Re-measure, correct,
    re-score every region.
  - **Clipped at 375:** "Los Angeles (Regional)" about 43% in Global and
    United States (no clean position) and 15% in United States West; "Rio de
    Janeiro (Regional)" about 24% in South America since the rename. Re-place
    both once the scorer canvas is corrected.

- [ ] **Heavy-job gate follow-ups (2026-10-03):**
  - **Why does a multi-city Japanese drift run measure 4.5-4.7 GB?** On a
    quiet machine, run each Japanese city's drift alone through the gate
    (`drift <city>`) and compare with `drift japan --jobs 2`.
  - **Orphans:** stopping a shell that wraps `heavy_job.py run` calls can
    leave a child running and in the ledger. Either the gate ends its child
    when its parent dies, or `status` flags entries whose gate is gone.

- [ ] **Left by the 2026-10-03 lanes batch, each needing a fresh pull:**
  - **Rome's tram 3 is back in service** (ATAC, 2026-09-07), but the cached
    GTFS has no route-3 trips and no tram 3 relation is cached: a feed and an
    Overpass re-pull (one query), steps 1-3, drift check.
  - **Oslo's tram 13 stops west of Thune** are not yet listed as left out
    (Sollerud is missing from the cached `stops.txt`; Lilleaker's tram quays
    cannot be told from its bus quays). A fresh Ruter feed settles both.
  - **SFMTA's clause 4:** notice 3 displays its disclaimer on the cautious
    reading. Owner's call to keep or drop; kept until then.

- [ ] **The UK six's watch items** (built 2026-10-02 on `uk-six-build`):
  - **Birmingham (Regional): Metro Line 2 (Wednesbury - Dudley)**, due about
    1 November 2026. In service: take relation 17248967 out of `NOT_DRAWN`,
    add Dudley (FSA 409) as a fourth authority (pre-approved 2026-10-01), drop
    Line 2's five Sandwell stops from `NAPTAN_EXPLAINED`.
  - **Birmingham's Eastside stops** (Curzon Street, Meriden Street, Digbeth
    High Street): in NaPTAN, not yet open. Add them when they open.
  - **Sheffield's Shalesmoor** (NaPTAN: "Kelham Island") keeps its name
    (owner); re-read the operator's name if its site ever answers a script.
  - **Sheffield's business-rates list**, a later second bucket (owner,
    2026-10-01): a licence read, an address join and a call on "Shop And
    Premises".

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
  - [ ] **Japanese cities onto N02-25 (Band B session, 2026-09-30)**, one
    drift check per city. Hiroshima reads the 2025 edition because N02-24
    still draws Hiroden to the closed 猿猴橋町 stop; the six earlier cities
    stay on N02-24 (stations identical). `japan.n02(slug)` and
    `N02_EDITIONS` make it a per-city switch.
  - [ ] **City-map legend model (2026-09-30).** The label solver's open
    legend, `178 + 19 x lines`, is -32 to +114 px off across 75 cities (Oslo
    and Fukuoka fixed per city; Osaka's "JR Gakkentoshi Line" not). Fix: the
    obstacle becomes max(model, a content-based estimate). A full drift check
    (heavy) and review time.
  - [ ] **Macro-map dots: colour is network type, fill is completeness
    (owner 2026-09-28, revised 2026-09-29 and 2026-09-30; building on branch
    `macro-legend`; DECISIONS "Yes to trams-only maps").** Colour: teal metro
    (#0D9488), a new hue each for light rail and tram; mode is the
    highest-order drawn mode, a `cities.py` field backed by a check (Dublin
    is tram). Fill: solid = full, BOTTOM half filled = narrowed, hollow ring
    with a pale centre = one category (Ottawa ships it). SVG icons (3 modes x
    3 fills); two-key legend; no sizing (owner); the tooltip carries
    storefront count, placement precision and data age. Tier and mode are
    `cities.py` fields backed by checks, and go to the owner before landing.
    Re-run `validate_palette.js`; re-measure the east-coast cluster if the
    dot grows. Review time, `map-chrome` deploy-verify, reboot.
  - [ ] **Buffalo's macro label: HELD (owner 2026-09-30).** In United States
    East its pill reads as Toronto's; branch `buffalo-label` collides with
    Minneapolis. Revisit once `macro-legend`, Ottawa and Minneapolis are
    live; per-region label offsets (about 40 lines) are the likely fix.
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
  - [ ] **Toulouse and Rennes: did step 1's name-level fallback fire?** The
    pure-extract rule (owner 2026-09-29) forbids a station at the MEAN of
    same-named platforms (`step1_stations.py`, "collapsing N name(s)").
    Re-run step 1 read-only or read its drift log; if it fired, take the
    first platform's coordinates, drift-check, review time.
  - [ ] **Groundwork before the tram batch (staging, 2026-09-29)**; (1) the
    France kit is done, and the French pages exist. Left, unticked: (2)
    licence reads up front (Bordeaux LO 1.0, four ODbL feeds, Plzeň and
    Olomouc GTFS, Tucson, RideKC, Florence), each notice recorded before a
    page exists; (3) page text by template; (4) the macro-map items here; (5)
    re-measure Streamlit Community Cloud (memory, clone time, the Overview
    list; `docs/scaling_thresholds.md` dates from 9 cities); (6) scoped
    `city-added` deploy-verifies per landing group.
  - [ ] **Macro-map label tiers (owner 2026-09-29):** minor cities get no
    pill outside their own region, only the tooltip; anchors keep theirs.
    Europe and East Asia become composites of their sub-regions. Pilot: the
    Seoul Capital Area (minor: Incheon, Goyang, Seongnam, Yongin); France and
    Czechia after their first tram builds, once `check_macro_labels.py` has
    scored a placeholder France view at 375, 768 and 1200 px. Review time.

- [ ] ⏰ **Prague: Flora reopens** (about the end of February 2027 per the
  re-check calendar): when PID's feed serves it again, step 1 STOPS on
  purpose; remove the override then and Flora is drawn from the trips
  (listed as closed for works until then, owner 2026-09-29).

- [ ] Optional label follow-ups (DECISIONS, "Phone-width label placer
  verified and pushed"): a few re-placed labels sit ~54 px from their tip
  (Amsterdam's Metro 51), and labels may sit on cluster bubbles, which the
  placer does not avoid.

- [ ] **"Vancouver (Regional)" is clipped at the left edge at 375 px** in
  Canada and the US region (desktop fine). Options, by cost: shorten it to
  "Vancouver"; a right-side anchor; or `REGIONS[i]["zoom"]` for Canada,
  re-measuring that region's `label_offset` values.

- [~] **Evaluate the map-only navigation pilot** (started 2026-09-20;
  `docs/navigation_sidebar_and_city_links.md`). The Overview's fallback link
  list stays; each map has a "Cities" dropdown. Open: the final go/no-go. To
  revert, set `MAP_ONLY_NAV = False` in `app/cities.py`.
- [ ] **Overview page colours: the numeric contrast check was never run.**
  The macro map's marker and label colours come from `pipeline/theme.py`;
  measure them against the dark page (`#0B1220`) numerically.

- [ ] **The category fix batch (owner-approved 2026-09-29).**
  `scripts/check_category_continuity.py` found 45 departures from
  `docs/category_rules.md`; work list `docs/handoff_category_fixes_2026-09-29.md`.
  - Coded and re-run on branch `category-continuity` (DECISIONS, "Category
    fix batch re-run"; 32 maps moved, wording owner-approved). Left for
    review time: `app/macro_facts.json` from the processed files in
    `data/_review_category-continuity_2026-09-29/`, then landing.
  - Stockholm's torghandel stall waits for `stockholm-catering` to land.
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

- [ ] **Monterrey (Regional):** retire the `data/` junction and the
  `monterrey-static-tmp` launch entry.

## Next cities, in ease order

- [ ] **Second-city screens (Staging, 2026-09-27).** Waves 1 and 2 are done
  and banded (`docs/city_master_list.md`, DECISIONS). Open:
  - [ ] **Busan:** the sub-item "page prose, blurb and credit notice 49
    (Busan), drafted in chat, and Line 4's darkened blue (#144B7A)" was never
    ticked, though Busan went live 2026-09-27. Confirm and close.
  - [ ] ⏸ **Band T's group decision, DEFERRED by the owner 2026-09-27** until
    the full tram list exists and the second-wave screens are done: which
    trams-only cities to build, and in what order (Nice, Montpellier, Brno
    and Bergen are the cheapest strong ones). Load and per-category
    recommendations: `docs/tram_rescope_estimate.md`.
  - [ ] **Wave-2 follow-ups** (run 2026-09-30; DECISIONS "Wave-2
    follow-ups"; Dallas to Band A, St. Louis discarded). Still open:
    - **Richmond (Vancouver's rescope): NOT PERMITTED as it stands**; its
      site allows "research purposes and private use only". Written
      permission (buslic@richmond.ca) is an owner call; out unless the owner
      asks.
    - **Reads from the owner's own browser:** Tempe; Arlington's "Active
      Business Licenses" (a D.C. add-on: 11 of D.C.'s 32 excluded Virginia
      stations); Zaragoza (`zaragoza.es`), Brescia, Catania, Cagliari,
      Alicante, Alcobendas (any could reopen a city).
    - **Watch from group 2:** Bologna's Linea Rossa (spring 2027), Jaén's
      tram ("autumn 2026"), Florence's T3 (end of 2026).
  - [ ] **Vancouver (Regional):** built 2026-10-03 without Richmond (above)
    and Port Moody.
  - **Watch items from group 1:** Salvador's VLT (draw it once in revenue
    service); Teresina (all-day 15-minute service); the Hazel McCallion Line
    (early 2028); Luas Cork (after 2028); ION Stage 2 to Cambridge.
  - [ ] **Tram rescopes of built cities held by the owner**; Cleanup's
    case-by-case list is in DECISIONS (2026-09-27).

- [ ] Idea (Washington D.C.): make `drift_check.py` say plainly when a
  key-gated city's raw input is missing (`WMATA_API_KEY`, an expiring feed).
- [ ] Idea (Miami, ring coverage 12.6%): scope the all-businesses toggle to
  the station municipalities rather than the whole county.
- [ ] **New Orleans** (deferred 2026-09-21): built since
  (`app/pages/135_New_Orleans_Heatmap.py`); the item's screening findings are
  in `docs/plan_done/2026-09-27.md`. Confirm and close.
- [ ] **Fifteen rail cities were screened shallowly; nothing surfacing is NOT
  a disqualification.** Atlanta, Baltimore, Portland OR, Phoenix,
  Minneapolis, St. Louis, Cleveland, Pittsburgh, Detroit, Jersey City,
  Tucson, Sacramento, Salt Lake City, Honolulu, Buffalo. Twelve were "not a
  Socrata domain" and the ArcGIS pass searched titles only (Seattle was
  missed that way). Each needs a per-portal check before being written off.

### 🇯🇵 Japan — the plan (2026-09-24; evidence in `docs/global_country_shortlist.md`)

JR and private railways INCLUDED (owner, 2026-09-24). Measurement:
`scripts/screen_japan_join.py`. Re-run the census join control
(`scripts/japan_census_control.py`) with each new Japanese city.

- [ ] **Unticked publish steps** (the pages exist on master; confirm and
  tick): Osaka's reboot and live check (pushed 2026-09-28); from the
  2026-09-28 builds, `publish-city` with deploy-verify `city-added` and a
  reboot for Buenos Aires (page 58, notice 60 (Buenos Aires), Fortaleza's
  and Porto Alegre's labels moved), Sapporo (notice 53 (Sapporo), Osaka's
  label right), Fukuoka (notice 54 (Fukuoka), Busan's label lower left) and
  Kyoto (notice 55 (Kyoto), its label far above its dot).
- [ ] **Madrid's 343 px touch** ("Línea 5" / "Ramal Ópera–Príncipe Pío", ~0.5
  px at one corner, both readable; predates the tram batch): clears with
  Osaka's `DENSE_LABEL_SCRIPT` (measured by injection), but needs the
  trigger widened and Madrid re-rendered. Oslo's "T-bane 2" under the
  legend at 1024x768 is a different cause (the open legend).
- [ ] **Berlin:** when the U6 reopens to Alt-Tegel (about August 2027), step
  1 stops on the refetch; take the five stations out of
  `config.CLOSED_FOR_WORKS`, re-run steps 1-3. Monthly: IHK updates the
  register on the 1st; VBB's calendar ends 2026-12-12, so refetch before.
- [ ] **London:** refetch before the FSA extracts age (`fetch_sources.py
  --force`); if OSM starts carrying one of the eight added stations, step 1
  stops and says so.
- [ ] **Buenos Aires:** `docs/map_inconsistencies.md`'s prose lists (street
  surveys, modes not drawn, in-ring shares, pin labels) to name it
  (cleanup's `city-landed buenos_aires`); refetch SBASE's layers (dated
  2026-09-01) with `fetch_sources.py --force` when BA Data updates them.
- [ ] **When `macro-tiers` merges:** `scripts/check_macro_facts.py` checks
  Fukuoka's, Kyoto's and Sapporo's `coverage` / `placement` / `data_age`
  keys (owner-approved 2026-09-28, in `cities.py`); run `--write` for their
  counts in `app/macro_facts.json` (Fukuoka 30,062, Kyoto 32,355, Sapporo
  28,674).
- [ ] **Kyoto:** when the city publishes its August 2026 list, add it to
  `config.PORTAL_RESOURCES`, move `AS_OF` to 2026-08-31, re-run (a rebuilt
  register goes stale a month a month).
- [ ] **Osaka's Umekita → 福島 stretch** (lines served only by limited
  expresses count, owner 2026-09-28): no station, so only the line changes;
  a re-render for review time.

### ▶ Handoff to main — the Band A candidates, 2026-09-24

Each Band A city has a brief whose checks pass live and its licences read;
decisions inside a build are named in its brief.

- [ ] Owner, minor: アイスクリーム類製造業 (692 rows; many gelato counters) is
  OUT for now; the owner's call named 菓子 and そうざい.
- [ ] **Kyoto:** pin `as_of` to the fetch date; before publishing, measure
  same-address successors and the factory share of 菓子 and そうざい (brief,
  "Still unknown").
- [ ] **Tokyo: the missing wards** (built 2026-09-28 with 8 of 23). Chiyoda
  lifts urban station coverage from 45% to 56%; with Toshima and Bunkyō 67%;
  all 23 wards 98% (`tokyo.md`). Routes: Chiyoda's ledger (owner, gated item
  22); extract Ōta's, Kita's and Arakawa's PDF lists; Shinagawa's and
  Itabashi's partial files; requests to Toshima, Nerima and Edogawa.
  - [ ] ⏸ **PARKED, the last resort (owner, 2026-09-24): four requests**
    (`docs/gated_access.md` items 29–32), not sent and not the next step.
- [ ] ⏸ **Trams left off built maps: PARKED (owner, 2026-09-27); the owner
  decides case by case.** Estimate and recommendations:
  `docs/tram_rescope_estimate.md` (light batch yes, REM first; Paris T3 yes;
  Toronto, Milan, Prague not yet, a label and legend rule then a Toronto
  pilot; Barcelona likely yes; Hong Kong Tramways out; Cablebús yes; about
  55–85% of one 5-hour window). ▶ In progress: specs for REM, Rome 8, Madrid
  ML1, Paris T3a/T3b and SF F Market (`docs/tram_rescope_specs.md`), with
  Main Build on a branch for review time. Rescoping is main's work, city by
  city.
  - **Candidates (stops in scope):** Toronto streetcars (476); Milan (323 of
    341; no ATM colours); Prague (285); Paris T3a/T3b and edges of T2/T9
    (62); Barcelona TRAM T1-T6 (9–10 each; one OSM colour, so a colour rule);
    Rome tram 8 (40); Madrid ML1 (9); SF F Market (46); Fortaleza's VLT (11,
    failed the rail test); Montreal's REM. D.C. Streetcar ended 2026-03-31.
  - **Seoul's Wirye Line is not open:** re-check in January 2027; if open,
    count its stops inside Seoul for the rescope.
  - **Cablebús:** L1 6, L2 7 and L3 6 stations, all in CDMX; no official
    list or coordinates yet, so the build retries CDMX's GTFS (`mdb-3126`)
    before placing any. L4 is under construction: out.
  - **Reason still stands:** heritage (SF cable cars, Santa Teresa, Santos,
    Amitram); no stop in scope (Copenhagen Letbane, Aubagne, Philadelphia
    NHSL/D1/D2); Amsterdam tram 3; Rotterdam 12/14/18; Gimpo Goldline;
    Recife VLTs; the Aeromovel.
  - **Blind spots:** Hong Kong's and Barcelona's caches hold no tram
    relations; Cablebús is unstated (Toulouse's Téléo is the precedent);
    `docs/map_inconsistencies.md` shows D.C. as "—", which is incomplete.
- [ ] **Efficiency review follow-ups** (`docs/efficiency_review_2026-09-27.md`):
  - [ ] **Run `python scripts/archive_decisions.py` at the start of each
    week** (cleanup, after the Sunday reset; next 2026-10-04), and in the same
    sitting `python scripts/efficiency_metrics.py --baseline`, showing the
    owner the table: the session-count decision waits on it.
  - [ ] **The session count**, a separate owner decision.
  - [ ] **The remaining findings, walked through with the owner** (asked
    2026-09-27): 5 (hand-kept documents that churn), what is left of 4
    (re-render batching), then 7.

**Not ready for main:**
- **Band C (7)**: one owner decision moves all seven: does a single-bucket
  page belong beside three-bucket cities? Yokohama (personal services only)
  has no page for now whatever the answer (owner, 2026-09-24).
- **Band D (7)**, each waiting on an owner act or access: Sendai's request
  (drafted) and Kaohsiung's; reads from inside Poland, India, Finland
  (Helsinki) and Estonia (Tallinn) by a person there, never a proxy;
  Lisbon's DGAE account (item 28); Tallinn's EHR order (item 23).

**Owner's outside actions**, tracked in `docs/gated_access.md`:
- [ ] Item 21: send Sendai's request (`docs/communications/sendai-permission-request.md`).
- [ ] Item 22: request Chiyoda's ledger.
- [ ] Item 23: place the Tallinn building-register orders (two reports).
- Items 25–27 (Hiroshima, MHLW, Osaka) are optional confirmations, not gates.

## Structure

- [ ] Idea: a smoke check that re-fetches every recorded endpoint and asserts a
  plausible content type - an endpoint recorded but never re-run is not verified
  (San Francisco's `data.sfgov.org` redirect wrote a 654-byte HTML stub, 2026-09-21).

## Before deploying

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
- **If the repo ever goes private** (it stays PUBLIC; DECISIONS, "Pre-deploy
  gate"): Streamlit Community Cloud's free tier needs the `repo` OAuth scope
  and a deploy key; check its one-private-app limit; `outputs/` stays
  committed.

## Data quality follow-ups

- [ ] **Three code problems from the comment pass (owner, 2026-10-01: do
  later)**, each a small change with a drift check of its city:
  - **Barcelona's closed list is never checked:** a new `Nom_Activitat`
    value falls through `classify()` and silently leaves the map. Step 2
    should exit naming any active-premises value outside
    `UNMAPPED_IS_AN_ERROR` (as France's NAF module asserts at import).
  - **Norway's "unmatched by bucket" print reports a row count**
    (`norway_register.py`, about lines 207-211). Group by bucket.
  - **`check_deploy_imports.py`'s probe keeps unused code** (`_MARKERS`,
    `_box`, `DEFAULT_OFFSET`, `CHAR_W` / `PAD_W` / `PILL_H`) now that it
    imports `app/label_competition.py`. Delete it and its comment.
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
- [ ] **`scaffold_city.py` has only the GTFS map template** (found at the UK
  six landing): an OSM-rail city that drops `GTFS_ZIP` fails at import until
  its map step is replaced. Add a `--rail-source osm` template.
- [ ] ⏸ **After the prose and UI pass lands (owner, 2026-10-01):**
  - **Neutral comments, phase 2: `pipeline/<city>/`** (held until the
    landing and the city-skill rework). About 25,000 comment and docstring
    lines in 785 files across 124 city folders; phase 1's kit (agent 1's
    spec, the comments-only AST verifier, `check_no_em_dashes.py`, a
    render-only drift check).
  - **Comments inside the maps' embedded CSS and JS**
    (`pipeline/map_common.py`'s strings): rewording one changes every
    committed map, so a full re-render and drift check at review time.

- [ ] ⏰ **Zurich: rebuild after 2026-12-12** (owner, 2026-09-30, call C1):
  VBZ's temporary trams 50 and 51 are drawn until then; when they stop,
  re-run step 1 and step 3 and drift-check.
- [ ] **Deferred from the mega-review (owner, 2026-09-30, call C2)**, each
  with a drift check of Stockholm too: Göteborg's
  `sweden_livsmedel.layer_label` (both Swedish menus say "Food shops");
  "24sju" and vending words in the Swedish name rules; the template's "ratio
  to OpenStreetMap" clause for Odense and Liepāja (an Overpass count per
  city, or drop it).
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
- [ ] **What Is Excluded's opening generalisations (review lane 4,
  2026-09-30)** no longer hold: light rail only at 15-minute headways
  (Daugavpils's hourly routes are drawn); the commuter-rail list (missing
  Zurich's S-Bahn, NS at Den Haag, Göteborg's and Odense's regional trains);
  ring sizes at :118 and :135; Florence's not-drawn list (T2.2). Rewrite by
  category.
- [ ] ⏰ **Philadelphia: 11th St back on 2027-08-30** (SEPTA, 2026-08-06).
  Closed for works since 2026-09-05 and listed in `excluded_stations.csv`
  (`config.CLOSED_FOR_WORKS`; step 1 stops if the feed serves it again).
  When it reopens: clear the entry, re-run the city, drop the page's 11th St
  sentence.

- [ ] **Sacramento's Green Line: add it back when SacRT reopens it (due by
  mid-October 2026; check from 2026-10-15).** Suspended since 2025-06-16;
  7th & Richards/Township 9 is listed as closed for works
  (`docs/category_rules.md`, "Station scope"). When SacRT's schedule pages
  list it again: move "Green" from `config.NOT_DRAWN_REFS` to `LINE_REFS`
  and clear `CLOSED_FOR_WORKS`; add 7th & Railyards if OSM carries it; read
  its frequency against the 15-minute test; re-run the city and update the
  page's sentence. OSM cannot signal the reopening, so this date is the
  guard. When OSM catches up, retire `config.ADDED_STATIONS` (Dos Rios) and
  `UNNAMED_STOP_NAMES` (Morrison Creek); step 1 stops on its own then.

- [ ] **Gambling is bucketed inconsistently** (owner, 2026-09-28): Buenos
  Aires, Brazil and Berlin exclude lottery and betting premises (NAICS 7132,
  WZ 92), but `dublin_uses` counts BETTING SHOP as Retail. Decide one rule
  and sweep every taxonomy, with a drift measurement per city changed.


## Later / maybe

- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
