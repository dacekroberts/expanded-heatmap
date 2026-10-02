# Plan


Open work only. Completed work and the reasoning behind it live in
[`DECISIONS.md`](DECISIONS.md); the settled state is in
[`docs/project_context.md`](docs/project_context.md).

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

- [ ] Owner: `data/amsterdam/raw/gtfs-nl.zip` (243.8 MB, superseded by
  `gtfs-openov-nl.zip`) and `data/rome/raw/rome_static_gtfs.zip` (46.8 MB,
  downloaded, then not used) may be deleted from the main checkout.

- [x] **Tokyo's page scrolls sideways on a phone** FIXED at review time 2026-09-28 (a table that scrolls inside itself, `components.scroll_table`; deploy-verify: 375 and 343 px pass). (deploy-verify at review
  time, 2026-09-28): at 375 px its ward-share table is 469 px wide in a 343 px
  column, so the "The list" column is off screen until the reader scrolls. A
  layout fix for the next `app/` batch (a table that scrolls inside itself, or
  narrower columns); re-check at 343 and 375.
- [ ] **Port Hong Kong's Light Rail thinning and Riga's inline loop to
  `pipeline/stations.py` `thin()`** (owner, 2026-09-28). Both measure in
  haversine; each port gets its own drift measurement first. Pipeline only,
  on a branch for the next review time. San Francisco, Boston and
  Philadelphia keep their own variant (interchanges added after the spacing
  pass) until the owner decides.

- [ ] ⏸ **Per-city restriction disclosures, on every city's page (owner,
  2026-09-28). UNBLOCKED 2026-09-28: every Japanese city is built** (Tokyo
  landed); the prose edits are drafted in chat for the owner. **Before
  any drafting, the owner looks over the live pages and gives general advice
  first (owner 2026-09-28): ask for it, then wait.** Four
  facts per city, which the macro map's tooltip may also carry:
  - **Placement precision**: the register's own coordinates, a geocode, a
    block-level join (Japan), or interpolated along the road (Incheon, if
    built).
  - **Data age**: the rows' own newest date, not the edition's label (Busan
    frozen at 2026-04-15; Daegu's rows end 2025-08-31; Kyoto a rebuilt upper
    bound).
  - **Scope**: city only or "(Regional)".
  - **Network type**: metro, trams only (Riga today), or EDGE. It could
    become a macro-map tier once Band T builds exist.
  - **The borderline "Full" cities' caveats (owner 2026-09-28)**, each on its
    own page: **Brazil's nine** (a third to half of plausible storefronts
    unreadable and dropped, across every bucket); **New York** (retail thinner
    than its other layers, from four registers); **San Francisco** and **Los
    Angeles** (9-37% of rows without an industry code, a floor on every
    bucket); **Taichung** and **Taoyuan** (only 12-19% of storefronts in a
    ring: one line through a large city). Each stays Full on the macro map.
  - [ ] **Per-city wait times as data: TABLED by the owner (2026-09-30) until
    they are back at a desktop.** The owner's idea, relayed by the tram kit:
    pages state train/tram waits in hand-written prose (Buffalo "about every
    20 minutes", Houston, Sacramento, Aarhus), and nothing checks them.
    Proposed (cleanup, 2026-09-30):
    - drawn lines only; waits that explain an exclusion (Rome, Riga,
      Fortaleza) stay prose;
    - a `SERVICE` value in the city config (per line: a daytime range in
      minutes, an optional evening/weekend range and note, source, as-of);
    - step 3 copies it to provenance, and one shared helper renders a single
      owner-approved template sentence;
    - a no-fetch check measures headways from the cached GTFS (weekday
      10:00-16:00, plus an evening and a weekend window); an OSM-built city
      only needs a source and date;
    - cities: Buffalo, Houston, Sacramento, Aarhus, Palma, and every
      light-rail and tram build.
    About 150-200 lines, an `app/` change. Open: build it, and whether to
    show evening/weekend waits when they differ (suggested) or daytime only.
  - [ ] **Japanese cities onto N02-25 (suggested by the Band B session,
    2026-09-30), one drift check per city.** Hiroshima reads MLIT's 2025
    edition, because N02-24 still draws Hiroden's track to the closed 猿猴橋町
    stop. The six built cities stay on N02-24 (stations checked identical in
    memory). `japan.n02(slug)` and `N02_EDITIONS` make it a per-city switch.
  - [ ] **City-map legend model (found 2026-09-30, not built).** The label
    solver models the open legend as `178 + 19 x lines`; the rendered legend
    is -32 to +114 px off that across 75 cities, which put Oslo's, Fukuoka's
    and Osaka's labels under it at 1000 x 650. Oslo and Fukuoka are fixed per
    city; Osaka's "JR Gakkentoshi Line" (13 x 21 px) is not. The shared fix:
    the obstacle becomes max(model, a content-based estimate) - never smaller
    - so only a label truly under the legend can move. It needs a full drift
    check (heavy) and review time.
  - [ ] **Macro-map completeness tiers: APPROVED (owner 2026-09-28)**, not
    tied to the wait above. Dots coloured **Full #0D9488** (the current teal)
    · **Narrowed #9333EA** · **One bucket #C2410C**, one set for both themes
    (the dots are WebGL, so dark mode filters only the basemap), with a text
    legend. **No sizing** (owner: it would swallow neighbours and break the
    scored labels); the tooltip carries storefront count, placement
    precision and data age. Each city's tier is a `cities.py` field backed by
    a check, never hand-kept. Per-city tiers go to the owner first. An `app/`
    change: review time, `map-chrome` deploy-verify, reboot.
  - [ ] **SUPERSEDED IN PART 2026-09-29 (owner): dot COLOUR becomes network
    type** (teal metro, a new hue each for light rail and tram), and
    completeness moves to the FILL: solid = full, a ring with a pale centre
    (the pill surface colour; ~2 px stroke) = narrowed, a half-filled circle
    = one category (build when the first one ships). Mode = the highest-order
    drawn mode, a new `cities.py` field backed by a check; Dublin is tram.
    Two-key legend; re-run `validate_palette.js`; re-measure the east-coast
    cluster if the dot grows a pixel. Review time, `map-chrome`
    deploy-verify, reboot. (DECISIONS "Yes to trams-only maps".)
  - [ ] **FILL ORDER REVISED, and BUILDING (owner 2026-09-30; branch
    `macro-legend`).** Fill decays linearly with completeness: **solid =
    full, BOTTOM half filled (a level, not a pie) = narrowed, hollow ring
    with a pale centre = one category**. The ring and the half carry the mode
    colour; the pale centre and empty half take the pill surface colour, so
    colour always means mode and fill always means completeness. Drawn as
    SVG icons (3 modes x 3 fills), so the iPhone check runs on it. Two-key
    legend: mode colours as solid dots, fills in a neutral grey (Full,
    Narrowed, One category). **Ottawa is one category** (owner): the hollow
    ring ships with it. Per-city modes go to the owner before landing.
  - [ ] **Buffalo's macro label: HELD (owner 2026-09-30).** In United States
    East its pill reads as Toronto's. Branch `buffalo-label` (Buffalo south,
    Chicago west) passes on master but collides with Minneapolis; the only
    clean three-way layout puts Chicago's label nearer D.C.'s dot in Global.
    Kept OUT of the next review. Revisit once `macro-legend` (12 px dots),
    Ottawa and Minneapolis are live and the east-coast cluster has been
    looked at rendered; per-region label offsets (scoped 2026-09-29, about
    40 lines) are the likely fix.
  - [ ] **Published-city date fixes (the 2026-09-29 date check; DECISIONS
    "Published cities' data dates checked")**: (a) **San Francisco**: drop
    rows with a `location_end_date` in step 2 (4,677 of 16,495 mapped rows
    are closed locations), re-render, drift-check; (b) **Dublin**: owner call,
    disclose that the valuation list includes vacant units, or another
    source; (c) NYS Retail Food Stores (no date column, refreshed
    2025-09-30), Milan (publisher's date 2025-06-30 only) and Surrey: owner
    call on how the page states an undatable source; (d) Philadelphia: re-read
    around 2026-10-13, frozen since 2026-08-17?; (e) apply expiry dates where
    a status filter alone leaks expired licences (Philadelphia, DCWP, San
    Diego, D.C., Calgary); (f) record each source's newest row date at fetch
    time, capped at the fetch date, and write it into `data_age`. Pipeline
    work for the build sessions; review time.
  - [ ] **Toulouse and Rennes: did step 1's name-level fallback fire?** The pure-extract
    rule for French ODbL feeds (owner 2026-09-29) forbids a station point made as the
    MEAN of same-named platforms (`step1_stations.py`, the "collapsing N name(s)"
    branch), which the national portal files under « ajout de coordonnées ». Re-run step 1
    read-only (or read its drift log) for the print; if it fired, take the first
    platform's coordinates instead, drift-check, review time.
  - [ ] **Groundwork before the tram batch (staging's list, 2026-09-29; ~68 →
    ~110 cities)**, in the recommended order: (1) a France batch kit - a
    `france-tram-city` skill and a script writing the 21 configs from the
    screen's station files (Czechia's six likewise, smaller) - **France DONE
    2026-09-30**: the skill, `scripts/scaffold_france_batch.py` and 20 briefs
    (Angers held); feeds are fetched at build, never cached; builds wait for
    the owner's go and the calls in each brief; (2) the licence reads up front (Bordeaux LO 1.0, the
    four ODbL feeds, Plzeň and Olomouc GTFS, Tucson, RideKC, Florence), each
    notice in `docs/data_sources.md` before a page exists; (3) page text by
    template, one French paragraph approved once; (4) the macro-map items
    below before France lands; (5) re-measure Streamlit Community Cloud at
    ~110 (memory, clone time, the Overview list; `docs/scaling_thresholds.md`
    was written at 9 cities); (6) scoped `city-added` deploy-verifies per
    landing group. Ring sizes: `docs/ring_rules.md` (generated).
  - [ ] **Macro-map label tiers (owner 2026-09-29)**: minor cities get no
    name pill outside their own region, only the hover tooltip; anchors keep
    theirs. Europe and East Asia become composites of their sub-regions.
    **Pilot: the Seoul Capital Area** (minor: Incheon, Goyang, Seongnam,
    Yongin). France and Czechia after their first tram builds, once
    `check_macro_labels.py` has scored a placeholder France view at 375, 768
    and 1200 px. Same review-time route.

- [ ] ⏰ **Prague: Flora reopens around December 2026**: when PID's feed serves
  it again, step 1 STOPS the build on purpose - remove the override then, and
  Flora is drawn again from the trips (it is listed as closed for works until
  then, owner 2026-09-29).

- [ ] Optional label follow-ups (DECISIONS, "Phone-width label placer verified
  and pushed"): a few re-placed labels sit ~54 px from their tip (Amsterdam's
  Metro 51), and labels may sit on cluster bubbles, which the placer does not avoid.

- [ ] **"Vancouver (Regional)" is clipped at the left edge at 375px — in the
Canada region as well as the US one.** Found during the run above. NOT a
regression: `fit_view` is byte-identical to the pre-switcher commit and frames
`IN_DEFAULT_VIEW` (US only), so Vancouver was never in the fitted box. But the
switcher makes it newly user-facing, because it now invites a viewer to look at
Canada and Canada still does not frame its own westernmost city. This is the
direct cost of RE-CENTRE-NEVER-RE-ZOOM: centring on Canada's midpoint leaves a
long label 25 degrees west of centre.
Options, in increasing cost: shorten the label to "Vancouver"; give that city a
right-side anchor; or set `REGIONS[i]["zoom"]` for Canada, which exists for
exactly this and costs a re-measure of that region's `label_offset` values.
Desktop is unaffected — the label is fully visible there.


- [~] **Evaluate the map-only navigation pilot** (started 2026-09-20; see
  `DECISIONS.md` and `docs/navigation_sidebar_and_city_links.md`). The
  Overview's fallback link list is kept (decided 2026-09-21). The hop-between-cities
  gap is closed with a "Cities" dropdown on each city map (2026-09-21). Open: the
  final go/no-go. To revert, set `MAP_ONLY_NAV = False` in
  `app/cities.py`.
- [ ] **Overview page colours: the numeric contrast check was never verified.**
  The macro map's marker and label colours now come from `pipeline/theme.py`;
  measure them against the dark page (`#0B1220`) numerically, not by eye.

- [x] **Landed with the 2026-09-29 review batch (41 cities re-rendered; DECISIONS 2026-09-29 "Exclusions batch re-run").** **One exclusions batch: funeral services off every map (owner, 2026-09-28) PLUS the fringe-category rules (owner, 2026-09-29: R1 no-counter food, R2 the other-personal-services catch-all and Mexico 812130, R3 adult/hostess venues (karaoke kept), R5 gambling, Barcelona vets; France's car dealers and the Toronto/Edmonton nightclubs brought in). DECISIONS 2026-09-29.** Funeral code is done (uncommitted); the fringe rules are being coded.
  Cleanup does it AFTER Buenos Aires, Glasgow and Newcastle land:
  - Exclude by code or licence type in 34 cities: NAICS 8122, SCIAN 8123,
    NAF 96.03Z, Rev. 2.1's 96.30 (Oslo, Copenhagen, Prague, Berlin), Madrid's
    pompas fúnebres, Taiwan's 殯葬 service types (NOT the funeral-goods
    retail), Brazil's FUNERARIA keyword, and the local types in Vancouver,
    Edmonton, Miami, D.C. and Dublin. Cemeteries and crematoria go with them.
  - Disclose, don't filter: Chicago, Calgary and Milan (by accident, under
    general licences) and Amsterdam, Rotterdam and Riga (not identifiable).
  - Re-run the affected cities one at a time as announced heavy jobs, then
    drift checks, `check_ring_shares.py --write` and
    `check_macro_facts.py --write`.
  - The `docs/excluded_categories.md` wording goes to the owner first; a
    full `deploy-verify` runs at review time.
- [ ] **The category fix batch (owner-approved 2026-09-29).**
  `scripts/check_category_continuity.py` found 45 departures from
  `docs/category_rules.md`, and the owner approved fixing all of them. The
  work list is `docs/handoff_category_fixes_2026-09-29.md`: 17 taxonomies or
  configs and about 45 cities to re-render, run as the exclusions batch was.
  - Coded and re-run on branch `category-continuity` (2026-09-29): 32 maps
    moved, the privacy check is clean, and `check_all` passes (DECISIONS,
    "Category fix batch re-run"). The per-city wording in
    `docs/excluded_categories.md` is written (owner-approved). Left for review
    time: `app/macro_facts.json`, written from the processed files saved in
    `data/_review_category-continuity_2026-09-29/`, then landing.
  - Stockholm's torghandel stall waits for `stockholm-catering` to land.
  - Still with the owner: Boston's General On Premise licences (measure
    first).
- [ ] **Next cross-city discrepancy audits (owner, 2026-09-29), AFTER the
  exclusions batch lands.** Each is read-only and runs one at a time; each ends in rules
  for the owner to decide, as the fringe-category audit did.
  1. **The same trade in different buckets.** Trace about 10 common trades
     (bakeries, delis, coffee shops, convenience stores, pharmacies, dry
     cleaners...) through every taxonomy.
  2. **Records that may not be trading.** Classify each source as
     active-only, carries closing dates, or neither; estimate the inflation
     where a sample allows (Kyoto, Rome, the permit registers).
  3. **Home-based and one-person registrations.** Measure, per register-based
     city, the share of pins with no employees and no premises name (the
     French car-dealer finding); a privacy risk as well as inflation.
  Then, as disclosures in `docs/map_inconsistencies.md` rather than rules:
  4. placement precision and stacking; 5. one premises counted once or
  several times (Milan twice, Calgary merged); 6. upper-floor and office
  premises.
- [x] **Put the cross-city inconsistency list on the site** (owner, 2026-09-24).
  LIVE 2026-09-28 (checked on the live URL after the owner's reboot): page 92 "Why
  the maps differ", linked from every page's footer; the owner's shape and
  approved text are in DECISIONS (2026-09-28). `docs/map_inconsistencies.md`
  stays internal as its evidence and is still kept current as cities land. A
  new city now also needs `rail_extra`, `record_kind` and `categories` in
  `app/cities.py` and a `check_ring_shares.py --write` (both checks are in the
  hook). Tick this once it is live.

- [ ] **🇲🇽 MONTERREY (REGIONAL) - BUILT 2026-09-27 on branch `worktree-monterrey`, HELD for a
  batch publish with a few smaller cities (owner): 58,565 storefronts, 38 stations, Metrorrey
  Líneas 1–3 across four municipios.** Page 47; text, blurb, notices and the whole-city layer
  approved (owner). Done up to `deploy-verify`: steps 1–3, provenance, scope disclosure,
  inconsistency rows, privacy verdict, label width (144.0) and placement - which moved
  Guadalajara's pill below its dot and Mexico City's 10 px lower. Still to do, at the batch:
  - [x] `deploy-verify` (city-added, plus the Mexico and landing views for the three moved labels) (2026-09-27, one run for the three-city batch: all PASS; DECISIONS)
  - [x] `check_deploy_imports.py` (0 problems) with `.venv-lean` linked, merge master, fetch, push, **reboot**
    (`cities.py` and `components.py` change), live check
  - [x] `city_master_list.md`'s band counts reconciled on the branch, in Staging's wording
    (A 6, Candidates 20, Built 47; 68f656c). **Merge notes from Staging**: if
    `docs/build_briefs/monterrey.md` line 111 conflicts, take master's (the same fix,
    dd3c75a); if Staging's wave-1 rewrite of the band counts lands first, take master's
    numbers and apply the Monterrey move to them - A -1, Candidates -1, Built +1.
  - [x] origin/master merged into the branch early (owner, 2026-09-27): both merge notes
    applied - the brief took master's line, and the band counts are master's with the
    Monterrey move (A 8, Candidates 63, Built 47). The two lines that called Monterrey the
    only Mexican city with a whole-city layer corrected. Merge again before the push.
  - [ ] Retire the `data/` junction and the `monterrey-static-tmp` launch entry

## Next cities, in ease order

- [ ] **Second-city screens, 2026-09-27 (Staging).** Wave 1 done and banded
  (France; Czechia, Norway, Denmark, the Netherlands, Latvia; Korea, Taiwan,
  Hong Kong): see `docs/city_master_list.md` and DECISIONS. Open:
  - [x] **Licence reads for Daegu and Busan** (2026-09-27).
  - [x] **Daegu's brief** (`docs/build_briefs/daegu.md`, 11/11, 2026-09-27,
    corrected the same evening), handed to Main Build. Three owner calls open
    in it (buckets as Seoul's; 대경선 out; stations inside Daegu).
  - [ ] **🇰🇷 DAEGU - BUILT 2026-09-27 on `worktree-daegu` (its own branch, owner), HELD
    for a batch publish: 67,212 storefronts, 86 stations, Lines 1–3.** Page 48. Owner
    calls taken as recommended; the rows end 2025-08-31 (owner: build, date disclosed).
    Done: steps 1–3, drift baseline, provenance rows, inconsistency rows, privacy
    verdict, label width (42.9) and placement (below the dot), DECISIONS. Still to do:
    - [x] Page prose, blurb, credit notice 48, the `excluded_categories.md` section and
      the line colours approved by the owner 2026-09-27, and written.
    - [x] `deploy-verify` (city-added, plus East Asia for the label) - **HELD until at
      least after Busan is built** (owner, 2026-09-27), then run once for both.
    - [x] Publish with the batch (`publish-city`): LIVE 2026-09-27 (pushed 9dc08de, rebooted by the owner, live-checked; DECISIONS). `check_deploy_imports.py` with
      `.venv-lean` linked, merge master, fetch, push, **reboot** (`cities.py`,
      `components.py`), live check. Retire the `data/` junction and the
      `daegu-static-tmp` entry in the monterrey worktree's `.claude/launch.json`.
  - [x] **Busan's brief** (`docs/build_briefs/busan.md`, 8/8, 2026-09-27),
    handed to Main Build. Three owner calls open in it (buckets as Seoul's;
    동해선, recommended out; stations inside Busan with the Busan–Gimhae LRT
    drawn).
  - [ ] **🇰🇷 BUSAN - BUILT 2026-09-27 on `worktree-busan` (its own branch, owner; stacked
    on `worktree-daegu` for the shared Korean module), HELD for the batch: 89,798
    storefronts, 110 stations, Lines 1–4 and the Busan–Gimhae LRT.** Page 49. Owner calls
    taken as recommended. Done: steps 1–3, drift baseline, provenance rows, inconsistency
    rows, privacy verdict, label width (41.9) and placement (below; Daegu's moved to the
    left), DECISIONS. Still to do:
    - [ ] At the owner's review: the page prose, blurb and credit notice 49, drafted in
      chat, and Line 4's darkened blue (#144B7A).
    - [x] Then `deploy-verify` ONCE for Daegu and Busan (city-added x2, plus East Asia). (2026-09-27, one run for the three-city batch: all PASS; DECISIONS)
    - [x] Publish with the batch: LIVE 2026-09-27 (pushed 9dc08de, rebooted by the owner, live-checked; DECISIONS). Pushing `worktree-busan` carried Daegu too. Retire the
      `data/` junction and the `busan-static-tmp` entry.
  - [ ] ⏸ **DEFERRED by the owner 2026-09-27: until the full tram list exists
    AND the second-wave screens are done** (the screens wait for the 10pm
    reset or later; wave 1 was very load-intensive). The tram list's open
    counts are Barcelona's TRAM, Hong Kong Tramways, Seoul's Wirye Line,
    D.C. Streetcar's status and Mexico City's Cablebús (below). **The
    tram-list count runs WITH wave 2** (owner). The rescopes' estimated load
    and a recommendation per category: `docs/tram_rescope_estimate.md`.
    **Band T's group decision**: build trams-only cities, and in what
    order (Nice, Montpellier, Brno and Bergen are the cheapest strong ones).
  - [ ] **Wave 2 of the screens, launched 2026-09-27 after the 10pm reset**
    (the US; Canada, Brazil and Ireland; Spain and Italy). **Its agents use
    `pipeline.osm.fetch`**, not the scratch `ovp.py`: since 2040dfc it refuses
    an all-zero `out count` answer, which the wave-1 scratch fetcher accepted
    (Amstelveen's density is still unmeasured for that reason).
    - **Both load tables, as republished, are saved in
      `docs/load_estimates.md`** (tram rescopes and wave 2).
    - **Estimated load (2026-09-27, judgement; wave 1's cost was never
      recorded)**: about **80–130% of one 5-hour window** (roughly 10–16% of
      the weekly limit), so probably more than one window. The 5-hour window
      is shared by every session, so the anchor may overstate.

      | Group | Estimate |
      |---|---|
      | Tram-list count (read-only, cached OSM) | 5–8% |
      | Canada, Brazil, Ireland (Brazil's national modules exist; Waterloo's ION the one real Canadian lead) | 15–25% |
      | Spain, Italy (registers found city by city; many tram cities) | 30–45% |
      | US (no national register, several sources per city, ~15–20 rail cities) | 30–50% |

    - **Run order, agreed by the owner 2026-09-27**, after the 10pm reset:
      1. The cheapest first: the tram-list count plus Canada, Brazil and
         Ireland.
      2. Read `get_usage` before and after, and rescale the other two
         groups' estimates.
      3. Spain and Italy next. The US waits for a later window if they land
         near the top of their range.
      4. Every screen agent fetches OSM through `pipeline.osm.fetch`.
    - [x] **Group 1 (Canada, Brazil, Ireland) DONE 2026-09-27**, banded on the
      owner's calls (DECISIONS): Kitchener–Waterloo (Regional) to T; eleven
      discards. **Actual load: about 15% of the 5-hour window** (1% → 16%),
      the bottom of its range. Rescaled: Spain and Italy about 25–35%, the US
      about 25–40%.
    - [x] **Group 2 (Spain, Italy) DONE 2026-09-28**, banded on the owner's
      calls (DECISIONS): Florence and Santa Cruz–La Laguna (Regional) to T,
      Palma to C, thirteen discards, five not reached. **Load: about 15%**
      (24% → 39%). Watch: Bologna's Linea Rossa (spring 2027), Jaén's tram
      ("autumn 2026"), Florence's T3 (end of 2026). **Owner's-browser reads
      that could reopen a city**: Zaragoza (`zaragoza.es`), Brescia,
      Catania, Cagliari, Alicante, Alcobendas.
    - [x] **Group 3 (the US) DONE 2026-09-28**, banded on the owner's calls
      (DECISIONS): seven to T, Baltimore to C, sixteen discards. **Load:
      about 14%** (39% → 53%). **Wave 2 in all: about 44% of one window**,
      against the 80–130% estimate.
    - [ ] **Wave-2 follow-ups, handed to the next Staging session (owner,
      2026-09-28)**:
      - **Probes a session can run**: (1) re-screen **Dallas, Fort Worth and
        Austin** on the Texas Comptroller's "Active Sales Tax Permit Holders"
        (`jrea-zgmq`, public domain; `3kx8-uryv` has out-of-business dates) -
        owner-approved; (2) **St. Louis**'s Building Division Commercial
        Occupancy Permits API (live, fields undocumented); (3) a quiet-hour
        **Overpass re-run**: stub tests for Pittsburgh, St. Louis and
        Minneapolis, rail and OSM density for Buffalo and Houston; (4)
        **Richmond**'s licence read and **New Westminster**'s address join
        (Vancouver's rescope); (5) **Rio's Gramacho–Saracuruna shuttle**
        rail test (Duque de Caxias); (6) **Long Beach**'s licence read (its
        terms reserve the right to restrict access) for "Los Angeles
        (Regional)": 8 A Line stations, active licences ~1,590 / 1,464 /
        920, a `FULLNAME` column (privacy).
      - **Run 2026-09-30 (staging; DECISIONS "Wave-2 follow-ups")**: (1)
        **Dallas to Band A** (owner); Fort Worth and Austin stay out on rail.
        (2) **St. Louis to the discards**: a stream of occupancy permits,
        no closures. (3) Moot: Minneapolis and Pittsburgh were measured and
        passed on 2026-09-29, Buffalo and Houston are built, and St. Louis
        is discarded. (4) **New Westminster joins at 99.8%**; **Richmond's
        directory is NOT PERMITTED as it stands** (site-wide "research and
        private use only"; written permission, an owner call). (5) **The
        shuttle fails beyond Gramacho**: SuperVia's own notices (the 12-minute
        peak runs Central–Gramacho only; one notice gave Gramacho–Saracuruna
        a 50-minute average). The three stations the add-on needs, up to
        Gramacho, pass. (6) **Long Beach: PERMITTED WITH CONDITIONS**. Its
        "Business Licenses Public View" (20,264 active, in-city, not home-based)
        carries an express grant in the MapsLB Terms of Use. **The breach-only
        indemnity was accepted by the owner (2026-09-30)**. Never imply
        endorsement. Withhold `FULLNAME` where there is no `DBANAME` (12,854),
        and drop the Pacific placeholder points.
      - **Reads from the owner's own browser**: Burnaby (Vancouver's
        rescope), Tempe, **Arlington** (its "Active Business Licenses" for a
        D.C. add-on: 11 of D.C.'s 32 excluded Virginia stations), Zaragoza,
        Brescia, Catania, Cagliari, Alicante, Alcobendas.
    - [ ] **Regional add-ons to built cities (owner, 2026-09-27)**, main's
      work on a branch held for review time:
      - **Rio + Duque de Caxias**: SuperVia Saracuruna's three excluded
        stations (Duque de Caxias, Corte Oito, Gramacho); CNEFE 18,698
        storefronts. **First a rail test for the Gramacho–Saracuruna shuttle**,
        which the scope would bring in. **Run 2026-09-30**: up to Gramacho
        passes; Campos Elíseos, Jardim Primavera and Saracuruna, beyond it,
        fail (search-level: SuperVia's notices; no timetable feed found), so
        the line is drawn to its end and only those three are left unringed.
      - **Belo Horizonte + Contagem**: Metrô BH L1's Eldorado and Novo
        Eldorado; CNEFE 13,011. Belo Horizonte becomes "(Regional)".
      - Both CNEFE zips are cached in the main checkout's `data/contagem/raw/`
        and `data/duque_de_caxias/raw/` (and the staging worktree's).
    - [ ] **Vancouver (Regional) + Burnaby, New Westminster, Coquitlam,
      Richmond (owner: a PLAN item, probes first)** - 28 SkyTrain stations
      now excluded. Measured: Coquitlam (licences with lat/long, OGL-BC 2.0,
      each listed twice) and New Westminster (NAICS licences, addresses only:
      an address join; drop `RESIDENT_STATUS` = NON-RESIDENT). **Probes
      left**: Burnaby's `gis.burnaby.ca` refuses scripted requests (17,286
      licences per the portal: an owner's browser fetch, as Bucharest);
      Richmond's business directory declares no licence (a `licence-read`).
      **2026-09-30**: New Westminster measured, 907 resident licences in the
      buckets (retail 379, food 303, personal 225; approved 2025–2026),
      **99.8% joined** to the City's Address Points (42,690). **Richmond:
      NOT PERMITTED as it stands**. It has no open-data licence; the site's
      copyright notice allows "research purposes and private use only",
      written permission required (buslic@richmond.ca), so it stays out
      unless the owner asks. Its directory: 11,517 current licences, 4,012
      in the buckets, addresses only.
    - **Watch items from group 1**, each a dated re-check: Salvador's VLT
      (trial running since 2026-06-29; draw it on Salvador's map once in
      revenue service); Teresina (all-day 15-minute service); the Hazel
      McCallion Line (construction to early 2028); Luas Cork (no Railway
      Order before the end of 2028); ION Stage 2 to Cambridge (planning).
    - Kept out (owner, 2026-09-27): Fortaleza's Parangaba–Mucuripe VLT (now
      "Linha Nordeste") under the trams rule, and so Sobral; Osasco (São
      Paulo's L9-only rule stands); Lauro de Freitas (1 station); Québec's
      *Registre des entreprises* (CC BY-NC-SA).
  - [ ] **Tram rescopes of built cities held by the owner**, likely at the
    next reset; Cleanup's case-by-case list is in DECISIONS (2026-09-27).

- [ ] Idea (Washington D.C.): make `drift_check.py` say plainly when a key-gated
  city's raw input is missing (`WMATA_API_KEY`, a feed that expires), rather
  than report it like any other missing raw input.
- [ ] Idea (Miami, ring coverage 12.6%): consider scoping the all-businesses
  toggle to the station municipalities rather than the whole county.
- [ ] **New Orleans - DEFERRED POST-DEPLOY by the owner (2026-09-21),
  alongside Seattle.** The pre-deploy city scope is the nine that are
  built; this and Seattle's multi-municipality build come after. Findings
  kept so returning costs nothing. Screened 2026-09-21, needs a real
  Step 0.** `iqay-p646`
  "Active Occupational Licenses", 16,396 rows, and the **cleanest licence of
  any candidate: CC0 1.0, explicitly declared**. Has `businesstype`,
  `businessaddress`, `the_geom`. Two sibling datasets exist (`abc4-h3u3`, an
  application-workflow file of 20,956 rows that also carries `naics`,
  `category` and an `ishome` flag; `hjcd-grvu`, 37,902 rows) - pick one
  deliberately rather than merging them. Rail is streetcar-only (RTA's 5
  streetcar lines, dense in the core), which is a **scope** question for the
  owner, not a data one. Privacy flags: `ownername` and `businessphone`
  columns, and the name fields are inverted on some rows (blank `businessname`
  with the trade name sitting in `ownername`) - Boston's trap again.
- [ ] **Seattle - deferred by the owner 2026-09-21, and scoped as the project's
  first MULTI-MUNICIPALITY city.** Do not re-probe the Seattle registry itself;
  the findings are in `docs/build_briefs/seattle.md`, with checks
  (`python scripts/brief_check.py seattle`). On that evidence Seattle's own
  data is the best-equipped of any candidate - an official nightly export,
  **active-only by construction**, 54,604 rows with real NAICS (no new taxonomy
  module), a trade name, and point geometry (no geocoding step). It is on
  ArcGIS rather than Socrata, which is why earlier screens missed it.

  **The owner's intent (2026-09-21): full line coverage, not just the city.**
  This is deliberately the first test of merging several jurisdictions'
  business data into one map, and it **supersedes the standing rule that
  stations in another city are a new project rather than a config change** -
  for Seattle specifically, by the owner's decision. The named jurisdictions
  are Seattle, Shoreline, Lynnwood, Tukwila, Federal Way, Bellevue and
  Redmond. What to check before scoping the work:
  - **The station list is wider than seven jurisdictions.** Link also stops in
    **Mountlake Terrace** and **SeaTac** on the 1 Line and **Mercer Island** on
    the 2 Line; if Federal Way is in scope then the extension also runs through
    **Des Moines** and **Kent**. So plan for roughly ten to twelve, and settle
    the list from the real GTFS stop set against a Washington municipal
    boundary layer rather than from memory - the same discipline that caught
    16 Trolley stations in San Diego and 54 in Los Angeles.
  - **Each jurisdiction is an independent Step 0**, with its own registry,
    schema, classification, coordinate quality, licence and privacy profile.
    Seattle's own data says nothing about Lynnwood's. Expect some to have no
    usable registry at all, and decide up front what the map does where data is
    missing - a gap in coverage is the failure mode that made Boston's
    `Business Inventory` unusable, and it would appear here as whole
    suburbs reading as empty rather than as unsurveyed.
  - **The architecture already supports the taxonomy side.** Taxonomy plurality
    means each jurisdiction can carry its own module mapping into the shared
    three buckets, and `map_common.py` never names a taxonomy, so the map layer
    needs no fork. If several use NAICS (likely in Washington), they share
    `naics` and the merge is mostly plumbing.
  - **What genuinely does not exist yet** is multi-polygon scope: `CITY_KEEP`
    and the boundary filter assume one city. A multi-jurisdiction build needs a
    boundary *set*, per-jurisdiction row provenance on every business (so the
    map can say which registry a pin came from, and so a single city's data
    going stale is visible), and a cross-registry dedup rule for businesses
    licensed in more than one jurisdiction.
  - **Naming stays neutral**: this would be a region, and the project is never
    named after a city - so the page name needs deciding too ("Link light rail"
    rather than "Seattle" may be the honest label if it spans twelve cities).
- [ ] **Fifteen further rail cities were screened shallowly and nothing
  surfaced - that is NOT a disqualification.** Atlanta, Baltimore, Portland OR,
  Phoenix, Minneapolis, St. Louis, Cleveland, Pittsburgh, Detroit, Jersey City,
  Tucson, Sacramento, Salt Lake City, Honolulu, Buffalo. Twelve of those
  returned HTTP 404 from Socrata's discovery API, which means "not a Socrata
  domain", and the ArcGIS pass searched titles only. **Seattle proves the
  point**: it came back "no matching datasets" on Socrata and has a 54,604-row
  official layer on ArcGIS. Any of these needs a proper per-portal check before
  being written off. What the shallow screen DID find (from the retired
  `docs/city_shortlist.md`, 2026-09-27): **Baltimore** publishes liquor
  licences only, **Buffalo** contractor licences only (no locations), and
  **Phoenix** has two light-rail lines but no general city business licence.

### 🇯🇵 Japan — the plan (2026-09-24; evidence in `docs/global_country_shortlist.md`)

Ten cities; JR and private railways INCLUDED (owner, 2026-09-24). Measurement:
`scripts/screen_japan_join.py`. Deferred downloads are listed by domain in the
evidence section.

- [x] **Kobe built 2026-09-27, LIVE 2026-09-28** (the owner's reboot;
  Cleanup's live zoom check passed): 27,251 storefronts, 121 stations, on
  the shared Japanese steps.
- [x] **The `japan-city` skill**, written from Kobe 2026-09-27
  (`.claude/skills/japan-city/SKILL.md`): shared modules, standing calls,
  twelve traps, notices, and a sheet per remaining city. Next city
  recommended: Osaka.
- [x] **Osaka built 2026-09-27, pushed at review time 2026-09-28**:
  72,999 storefronts, 216 stations, 34 lines, on the shared steps. Notices 50
  and 52 had their links fixed before the push (DECISIONS).
  - [ ] **Owner: reboot the deployed app** (`cities.py`, `components.py`
    changed), then the live check.
- [x] **Osaka's line labels overlap at phone width** (deploy-verify
  2026-09-28): 22 pairs at 343 px, 12 at 375, none at 854 or desktop;
  "Hankyu Takarazuka Line" starts 11 px under the layer-control button. The
  project total at 343 was 2 (2026-09-20); Kobe has 0. A shared-label-code
  fix, so it batches with a full re-render at a review time.
  - Fixed 2026-09-29 on branch `claude/relaxed-diffie-d6eb1b`, held for review
    time (DECISIONS): `DENSE_LABEL_SCRIPT`, injected only into maps whose labels
    used the wide tier - Osaka alone - so NO full re-render is needed; only
    Osaka's map changed. 0 problems at 343, 375, 854 and 1280.
  - [ ] Unqueued: Madrid's one 343 px touch ("Línea 5" / "Ramal") clears
    with the same block (measured by injection); reaching it needs the trigger
    widened and Madrid re-rendered. Oslo's "T-bane 2" under the legend at
    1024x768 standalone is a different cause (the open legend), not this.
- **Build order (owner, 2026-09-28, after Tokyo landed): the build queue is
  WIPED and two new frontrunners lead it - Berlin, then London** (both Band
  B, each the first city in a new country: `add-country`, then `add-city`).
  The earlier queue - the additions to built cities (Belo Horizonte +
  Contagem, Rio + Duque de Caxias, Vancouver (Regional)), Osaka's two fixes and
  the Hong Kong / Riga `thin()` port - is OFF the queue; its items stay below,
  measured and unqueued, until the owner puts any back. (Before: Sapporo,
  Fukuoka, Kyoto, then Tokyo - all built.)
- [x] **Berlin built 2026-09-28** (`worktree-berlin`, held for review time):
  60,313 storefronts, 275 stations, 25 lines; texts owner-approved (DECISIONS).
  - [x] LANDED at review time 2026-09-28 by cleanup, with London, page 92 and the Tokyo table fix (DECISIONS); deploy-verify `city-added` plus extras passed; LIVE after the owner's reboot, checked on the live URL 2026-09-28.
  - [ ] **When the U6 reopens to Alt-Tegel (about August 2027)**: step 1 stops
    on the refetch that serves it; take the five stations out of
    `config.CLOSED_FOR_WORKS` and re-run steps 1-3.
  - [ ] Monthly: IHK updates the register on the 1st; VBB's calendar ends
    2026-12-12, so refetch before then.
- [x] **London built 2026-09-28** (`worktree-london`, held for review time;
  Berlin is on `worktree-berlin`): 54,241 food storefronts, 387 stations, 19
  lines; texts owner-approved (DECISIONS).
  - [x] LANDED at review time 2026-09-28 by cleanup, with Berlin, page 92 and the Tokyo table fix (DECISIONS); deploy-verify `city-added` plus extras passed; LIVE after the owner's reboot, checked on the live URL 2026-09-28.
    London's notices are 58 (FSA) and 59 (Ordnance Survey); Berlin's VBB is 57.
  - [x] Placed 2026-09-28 (owner): 2,349 of the 5,350 storefronts the FSA
    gives no point sit at their postcode's centroid (OS Code-Point Open, notice
    59); 3,001 (5.0%) stay unplaced; never a private-address record.
  - [ ] Refetch before the FSA extracts age: `fetch_sources.py --force`; if OSM
    starts carrying one of the eight added stations, step 1 stops and says so.
- [x] **Buenos Aires built 2026-09-28** (`worktree-buenos-aires`, held for
  review time): 63,596 storefronts, 89 stations, 6 lines; texts owner-approved
  (DECISIONS).
  - [ ] At review time: `publish-city` (page 58, `cities.py` with Fortaleza's
    and Porto Alegre's labels moved, notice 60), deploy-verify `scope:
    city-added`, reboot.
  - [ ] `docs/map_inconsistencies.md`'s prose lists (street surveys, modes not
    drawn, in-ring shares, pin labels) still to name Buenos Aires: cleanup's
    `city-landed buenos_aires` sweep.
  - [ ] SBASE's layers are dated 2026-09-01; refetch with `fetch_sources.py
    --force` when BA Data updates them (step 1 re-checks the counts).
- [x] **Sapporo built 2026-09-28** (`build-sapporo`, held for review time):
  28,674 storefronts, 95 stations, 7 lines; texts owner-approved (DECISIONS).
  - [ ] At review time: `publish-city` (a new page, `cities.py` with Osaka's
    label moved right, notice 53 "Sapporo City and MLIT"), deploy-verify `scope: city-added`, reboot.
- [x] **Fukuoka built 2026-09-28** (`worktree-japan`, held for review time):
  30,062 storefronts, 71 stations, 9 lines; texts owner-approved (DECISIONS).
  - [ ] At review time: `publish-city` (a new page, `cities.py` with Busan's
    label moved lower left, notice 54 "Fukuoka City, MHLW and MLIT"),
    deploy-verify `scope: city-added`, reboot. `worktree-japan` also carries
    Sapporo's branch, so the two land together.
- [x] **Kyoto built 2026-09-28** (`worktree-japan`, held for review time):
  32,355 storefronts, 117 stations, 18 lines, a register rebuilt as of
  2026-07-31; texts owner-approved (DECISIONS).
  - [ ] At review time: `publish-city` with Sapporo and Fukuoka (a new page,
    `cities.py` with Kyoto's label far above its dot, notice 55 "Kyoto City
    and MLIT"), deploy-verify `scope: city-added`, reboot.
  - [ ] When `macro-tiers` merges: Fukuoka's and Kyoto's `coverage` /
    `placement` / `data_age` keys (owner-approved 2026-09-28, already in
    `cities.py` here) are checked by `scripts/check_macro_facts.py`; run
    `--write` for their storefront counts in `app/macro_facts.json` (Fukuoka
    30,062, Kyoto 32,355, Sapporo 28,674). Sapporo's keys are here too
    (owner-approved 2026-09-28), so staging need not add them at the merge.
  - [ ] When the city publishes its August 2026 list: add its resource to
    `config.PORTAL_RESOURCES`, move `AS_OF` to 2026-08-31, re-run (a rebuilt
    register goes stale by one month a month).
- [x] **Join control** - like-for-like against the Economic Census per-ward
  飲食店 count (the owner's chosen control). **Run 2026-09-28 for all six
  Japanese cities** (`scripts/japan_census_control.py`, peak 0.28 GB): every
  complete list sits at 2.0-3.3 map pins per census establishment in every
  ward (Kobe 2.38, Osaka 2.48, Sapporo 2.65, Fukuoka 2.01, Kyoto 2.62), so no
  ward's pins land in another; Tokyo's complete wards sit in the same band
  (Shibuya 2.49, Shinjuku 2.57, Taito 2.15) and its partial wards fall with
  their measured shares (Chuo and Koto 0.33). DECISIONS 2026-09-28, "Tokyo's
  census control". Re-run with each new Japanese city.
- [x] **Rail: lines served only by limited expresses COUNT** (owner,
  2026-09-28; revertible). The Shinkansen stays out.
  - [ ] **Osaka's Umekita → 福島 stretch**, left out 2026-09-27 under the old
    one-off, is now to be drawn. It has no station, so only the line changes:
    a re-render, held for the next review time.
- [x] **Share `fetch_sources.py` across Japanese cities: DONE 2026-09-28**,
  `pipeline/countries/japan_fetch.py`; Kobe and Osaka call it, provenance
  unchanged, zero drift (DECISIONS).

### ▶ Handoff to main — the Band A candidates, 2026-09-24

**All 20 Band A cities are buildable**: each has a brief whose checks pass live
and its licences read. The items below are what should be settled BEFORE
main starts a city. Everything else is a decision inside the build, which the
brief names.

- [ ] Owner, minor: アイスクリーム類製造業 (692 rows; many are gelato
  counters) is OUT for now, since the owner's call named 菓子 and そうざい.
- [ ] **Kyoto, at build**: pin `as_of` to the fetch date. Before publishing,
  measure same-address successors and the factory share of 菓子 and そうざい
  (brief, "Still unknown").
- [x] **Japanese build order (owner, 2026-09-24): Osaka → Kobe → Sapporo →
  Fukuoka → Kyoto → Tokyo LAST.** (Kyoto was added later the same day, owner.) The stub test cleared the first four: every urban
  line keeps 80–100% of its stations inside the city line. Tokyo failed, with
  Chiyoda missing from the centre of its 8 wards. Tokyo goes last as the
  densest, and it benefits most from a Japan skill written off the first four.
  Kyoto sits after Fukuoka, before Tokyo (owner, 2026-09-24): Japan's first
  rebuilt register benefits from the join being settled on four cities first.
- [ ] **Tokyo — the missing wards as a planned project.** Tokyo was built
  2026-09-28 with 8 of the 23 wards; this item now adds wards to a live map.
  Chiyoda alone lifts urban station coverage from 45% to 56%; Chiyoda,
  Toshima and Bunkyō reach 67%; all 23 wards reach 98% (`tokyo.md`).
  Routes: request Chiyoda's ledger (owner, gated item 22); extract Ōta's,
  Kita's and Arakawa's PDF lists; Shinagawa's and Itabashi's partial files;
  requests to Toshima, Nerima and Edogawa.
  - [ ] ⏸ **PARKED, the last resort (owner, 2026-09-24): four requests**
    (`docs/gated_access.md` items 29–32). Not sent, and not the next step.
    The own-time probe round found nothing that fills the gaps openly (DECISIONS).
- [ ] **PARKED by the owner 2026-09-27 (conserving usage) - come back to it.** **Trams left
  off built maps - owner decides case by case (listed 2026-09-27, after "trams count").**
  **Estimated load and Staging's recommendations, saved for later (owner, 2026-09-27):
  `docs/tram_rescope_estimate.md`**:
  - the tram list first (it runs with wave 2);
  - the light batch yes, REM first, D.C. once its service is verified;
  - Paris T3 yes;
  - the heavy three (Toronto, Milan, Prague) not yet: a label and legend
    rule first, then a Toronto pilot;
  - Barcelona likely yes, Hong Kong Tramways stays out, Cablebús yes;
  - one batch overhead. About 55–85% of one 5-hour window in all.

  Read-only list; nothing rescoped. Stops = distinct stop names in scope,
  from cached GTFS/OSM. Rescoping is main's work, city by city, after the owner decides.
  - **Recorded reason was only "not rapid transit / overlay" (reversed by the rule):**
    Toronto streetcars (18 routes, 476 stops); Milan (17 routes, 323 of 341; ATM publishes
    no colours); Prague (37 routes, 285); Paris T3a/T3b + edges of T2/T9 (62); Barcelona
    TRAM T1-T6 (not counted - cache has no tram relations); Rome tram 8 (40; lines 2, 3, 5,
    14 have no trips in the GTFS); Hong Kong Tramways (not counted - OSM query skipped
    trams; excluded by the owner 2026-09-24).
  - **Mixed or close:** Madrid Metro Ligero ML1 (9, run by Metro de Madrid); SF F Market
    (46, heritage cars on a regular route); Fortaleza diesel VLT (11, every 40 min - failed
    the rail test); D.C. Streetcar and Montreal's REM (both silent omissions). **D.C.
    Streetcar: no longer operating** (DDOT ended it 2026-03-31; checked 2026-09-27).
  - ✅ **Tram list COMPLETE 2026-09-27 (wave 2's first item, run early)**:
    - **Barcelona TRAM** T1–T6: 9–10 stops inside the city each; all six are
      one colour (#007165) in OSM, so a rescope needs a colour rule.
    - **Hong Kong Tramways**: 6 services, up to 54 stops, all in Hong Kong.
      The owner excluded it 2026-09-24; recommended out.
    - **Seoul's Wirye Line: NOT OPEN (confirmed 2026-09-27).** Seoul's own
      page (2026-02-10) puts its pilot running at February–December 2026;
      Newspim (2026-01-21) names the traffic-safety review and signal
      priority as what the opening hangs on; Wikipedia's target is
      2026-12-26. 12 stops, 5.4 km, Macheon (Songpa-gu) to Namwirye and
      Bokjeong - how many stops lie inside Seoul is unmeasured. **Re-check
      in January 2027**; if it opened, count it for Seoul's rescope.
    - **Cablebús**: L1 6 and L2 7 stations, all in CDMX; L3 is incomplete in
      OSM (1 stop). No OSM colours. **L3 = 6 stations (2026-09-27)**, all in
      CDMX (Miguel Hidalgo, Álvaro Obregón): Los Pinos/Constituyentes,
      Panteón de Dolores, Charrería, PARCUR, Cineteca Nacional, Vasco de
      Quiroga; opened 2024-09-24, 5.42 km. Three sources agree (es and en
      Wikipedia, Expansión 2024-09-25), but **no official list or
      coordinates yet**: datos.cdmx.gob.mx, STE and SEMOVI (one IP) refused
      every connection that day. The build retries CDMX's GTFS (`mdb-3126`
      carries Cablebús) before placing any station. L4 (Universidad–San
      Nicolás) under construction, about 20% in August 2026: out.
  - ▶ **IN PROGRESS 2026-09-27 (owner cleared light and medium): specs for REM, Rome 8,
    Madrid ML1, Paris T3a/T3b and SF F Market in `docs/tram_rescope_specs.md`**, handed to
    Main Build to implement on a branch held for review time.
  - **Reason still stands:** SF cable cars, Rio Santa Teresa, Santos, Lille Amitram
    (heritage); Copenhagen Letbane, Marseille Aubagne, Philadelphia NHSL/D1/D2 (no stop in
    scope); Amsterdam tram 3 (no trips until 2026-12-12); Rotterdam 12/14/18 (event or
    works routes); Seoul Gimpo Goldline (1 stop, already drawn); Recife VLTs (fail the rail
    test); Porto Alegre Aeromovel (people mover).
  - **Blind spots:** Seoul's OSM query takes only subway/light_rail/train (Wirye Line
    not open, checked 2026-09-27); Hong Kong's and Barcelona's caches hold no tram relations. Mexico City's
    Cablebús is also unstated (Toulouse's drawn Téléo is the precedent).
    `docs/map_inconsistencies.md` shows D.C. as "—", which is incomplete.
- [x] **An honest efficiency review of the whole PROCESS, the owner's habits included (owner,
  2026-09-24)** DONE 2026-09-27: findings in `docs/efficiency_review_2026-09-27.md`, the
  owner's order in DECISIONS (2026-09-27). Follow-ups, in that order:
  - [x] **Change 2 - batch approvals and deploys.** DONE 2026-09-27: queued for "review time",
    which only the owner calls; `app/` lands in one batch under one reboot. Rule and reminder
    threshold in memory (`batched-review-time`) and the `publish-city` skill.
  - [x] **Change 3 - trim what every session loads.** DONE 2026-09-27 (DECISIONS): CLAUDE.md
    4,345 -> 1,685 words, history verbatim in `docs/rule_history.md`; PLAN.md 20,675 -> 3,136
    words; `scripts/check_all.py` as `.githooks/pre-push`. The 7-day DECISIONS index was
    dropped (owner).
  - [x] **Change 1, half - archive DECISIONS.md.** DONE 2026-09-27, WEEKLY rather than
    monthly (owner; DECISIONS): `scripts/archive_decisions.py` at the start of each week,
    guarded in `merge_append_only.py`, proven by `archive_decisions_selftest.py`.
    DECISIONS.md 222,930 -> 8,490 words.
  - [ ] **Run `python scripts/archive_decisions.py` at the start of each week** (cleanup
    session, after the Sunday reset). Next: 2026-10-04. In the same sitting run
    `python scripts/efficiency_metrics.py --baseline` and show the owner the table: it is what
    the owner's session-count decision waits on (baseline in
    `docs/efficiency_review_2026-09-27.md`).
  - [ ] **The session count** - how many sessions run at once. A separate owner decision.
  - [ ] **The remaining findings, walked through with the owner** (asked 2026-09-27): 5
    (hand-kept documents that churn, e.g. a generated master list), what is left of 4
    (re-render batching beyond change 2), then 7.
  - Original item, kept for its method: only if the week's budget allows, at the start of a week, as ONE agent in
  its own context. Not a code review: how work gets done, verified, approved and shipped.
  - Evidence, not impressions: git history (`git log --since`, merge counts, files rewritten
    per day), the size of what every session loads, DECISIONS' index (never the whole file),
    `get_usage`, `check_*` run counts, approval round-trips per change.
  - Starting figures measured 2026-09-24 - verify, don't trust: DECISIONS.md ~210k words
    (~280k tokens), conflicting on every two-session push (archive older entries by month?);
    CLAUDE.md ~4,200 words loaded every session (how much belongs in skills/docs?);
    `docs/data_sources.md` ~52k words, PLAN.md ~16.7k; 2026-09-24 on master: 179 commits, 43
    merges, 286 `heatmap.html` rewrites (~seven full re-renders - batch renderer changes?);
    16 skills, 2 agents, 17 `check_*` scripts (which earn their keep?).
  - The owner's end, stated plainly: per-change wording approvals vs a batched review;
    batched `app/` pushes under one reboot; whether parallel sessions sharing one weekly
    limit spend more on coordination and merges than they save.
  - Deliverable, drafted for the owner: a ranked list (finding, evidence, estimated saving,
    whose habit - owner, session or structure), the top three changes, and a rough weekly
    saving for each. The owner decides.
- [x] **A check for dashes that render as bullets** (cleanup): a line in an app-rendered doc
  that starts `- ` mid-paragraph renders as a stray bullet. `deploy-verify` found three in
  `docs/excluded_categories.md` on 2026-09-27 (fixed by moving the dash up a line).
  DONE 2026-09-28: `scripts/check_stray_bullets.py` and its self-test, in the hook (DECISIONS).
- [x] **`check_master_list_counts_selftest.py` picks its target row from the live table**
  (cleanup): a fixed target ("Ottawa", then "Bergen") breaks whenever that country's row
  changes; Staging had to re-aim it on 2026-09-27 (e56c471). DONE 2026-09-28: every case
  picks its row by shape through the check's own parsers (DECISIONS).
- [ ] **Madrid at 343 px:** "Línea 5" and "Ramal Ópera–Príncipe Pío" label boxes touch at one
  corner (~0.5 px; both readable). Predates the tram batch. Cosmetic.

**Not ready for main:**
- **Band C (7)** — one owner decision moves all seven: does a single-bucket
  page belong beside three-bucket cities? Yokohama (personal services only)
  has no page for now, whatever the answer (owner, 2026-09-24).
- **Band D (7)** — each waits on an owner act or on access:
  - Sendai's request (drafted) and Kaohsiung's request;
  - reads from inside Poland, India, Finland (Helsinki) and Estonia
    (Tallinn), by a person there, never a proxy;
  - Lisbon's DGAE account (item 28);
  - Tallinn's EHR order (item 23).
- ✅ **The open gap is empty** (2026-09-24): its last eight each got a verdict
  after a final re-probe.

**Owner's outside actions** are tracked in `docs/gated_access.md`, the list of
every key, account and letter:
- [ ] Item 21: send Sendai's request (`docs/notifications/sendai-permission-request.md`).
- [ ] Item 22: request Chiyoda's ledger.
- [ ] Item 23: place the Tallinn building-register orders (two reports).
- Items 25–27 (Hiroshima, MHLW, Osaka) are optional confirmations, not gates.

## Structure

- [ ] Idea: a smoke check that re-fetches every recorded endpoint and asserts a
  plausible content type - an endpoint recorded but never re-run is not verified
  (San Francisco's `data.sfgov.org` redirect wrote a 654-byte HTML stub, 2026-09-21).

## Before deploying

- [ ] **Philadelphia's permission request** (`docs/gated_access.md` item 12;
  DECISIONS, "Philadelphia: ask for permission, stay up on a reasoned position
  meanwhile"). The footer (`components._UNSETTLED_TERMS`) discloses it meanwhile.
    - [x] **Followed up 2026-09-28** (one week), at the owner's request. The
      owner SENT the request on 2026-09-21 to `maps@phila.gov`, copying
      `LIGISTEAM@phila.gov` (text in
      `docs/notifications/philadelphia-permission-request.md`). **No reply as
      of 2026-09-28** (the owner, checked that day).
    - [ ] **Owner to choose the next step:** wait, chase once, or ring the Open
      Data Program. **Silence is not consent** - the interim position holds on
      the reasoned reading and the disclosure, not on the absence of an
      objection, and it does not strengthen with time. Sending it is the owner's to do. **Nothing in this project may
      claim a request is outstanding until it has actually been sent**, and
      silence must never harden into a claim that permission was given.
    - [ ] On a reply, follow the branch already written into that file: on
      permission the footer clause loses its only live subject and comes out
      entirely; on refusal Philadelphia comes off the site, and the remaining
      eastern cities' macro-map label offsets need re-checking at 854 and
      1200 px, because removing a marker moves `fit_view`'s bounds.
- **Reference, if the repo ever goes private** (it stays PUBLIC; DECISIONS, "Pre-deploy
  gate"): Streamlit Community Cloud supports private repos on the free tier, but
  needs the broader `repo` OAuth scope plus a deploy key, and its one-private-app
  limit needs checking; `outputs/` must stay committed either way.
- [ ] Optional: request a free Carto API key and set `CARTO_API_KEY` in the
  Streamlit Cloud secrets (the macro map uses Carto's keyless CDN; DECISIONS,
  "Pre-deploy gate").

## Data quality follow-ups

- [ ] **Three code problems found by the comment pass (owner, 2026-10-01: add,
  do later)**, each its own small change with a drift check of the city it
  touches:
  - **Barcelona's closed list is never checked.** The taxonomy enumerates the
    74 normalised `Nom_Activitat` values of the 2022 census, and
    `UNMAPPED_IS_AN_ERROR` lists them, but nothing reads it: a value a refresh
    adds falls through `classify()` and silently leaves the map. Fix: step 2
    exits naming any active-premises value outside `UNMAPPED_IS_AN_ERROR`
    (France's NAF module asserts its own list at import the same way).
  - **Norway's "unmatched by bucket" print reports a row count**
    (`pipeline/countries/norway_register.py`, about lines 207-211: `str[:1].size`
    is the number of rows, not a breakdown). Console output only; nothing on
    the map is wrong. Fix the print to group by bucket.
  - **`check_deploy_imports.py`'s probe keeps unused code** from its old,
    self-contained collision model (`_MARKERS`, `_box`, `DEFAULT_OFFSET`,
    `CHAR_W` / `PAD_W` / `PILL_H`); the probe imports
    `app/label_competition.py` now. Delete them, and the comment that names
    them.
- [ ] **Found by the prose pass's parallel deploy check (2026-10-02), all
  already on master and not blocking:**
  - **Map label crowding:** Pittsburgh at 375 and 343 ("PRT Silver Line"
    touches the collapsed legend, about 6x4 px); Yokohama at 343 (two overlaps,
    "Tokyu Kodomonokuni Line" x "Tokyu Shin-yokohama Line" about 29x6 px);
    Osaka at 1000x650 with the legend open ("JR Gakkentoshi Line" runs about
    14 px under it). Each reproduces with `scripts/check_map_labels.js`; the
    labels stay legible.
  - **San Diego's page is thin:** one bullet of its own and no businesses
    section, against 5-22 elsewhere.
  - **A step whose output depends on the run date:** Toronto's step 2 drops a
    license once its Cancel Date has passed, measured against today, and the
    register publishes future-dated cancellations, so a re-run days later
    moves the baseline (2026-10-02: 18,218 -> 18,215). Measure against the
    fetch date instead, or record it (the date fixes item (f) above).
- [ ] ⏸ **After the prose and UI pass lands (owner, 2026-10-01):**
  - **The site notices footer**: every city page lists all of the site's
    numbered notices (82) at its foot, inline for now. The owner wants a later
    look at how it is presented (a collapsed list, or only the city's own
    notices with a link to the rest).
  - **Neutral comments, phase 2: `pipeline/<city>/`** (owner's call; held
    until the landing and the city-skill rework, so the reworked skills carry
    the style first). About 25,000 comment and docstring lines in 785 files
    across 124 city folders; the same kit as phase 1 (agent 1's spec, the
    comments-only AST verifier, `check_no_em_dashes.py`, a render-only drift
    check).
  - **Comments inside the maps' embedded CSS and JS**
    (`pipeline/map_common.py`'s strings): left out of phase 1 because
    rewording one changes every committed map, so it needs a full re-render
    and a drift check at review time.


- [ ] ⏰ **Zurich: rebuild after 2026-12-12** (owner, 2026-09-30, call C1): VBZ's
  temporary construction trams 50 and 51 are drawn until then; when they stop,
  re-run Zurich's step 1 and step 3 and drift-check it.
- [ ] **Deferred from the mega-review (owner, 2026-09-30, call C2)**, each with a
  drift check of Stockholm as well: Göteborg's `sweden_livsmedel.layer_label`
  (both Swedish menus saying "Food shops"); "24sju" and vending words in the
  Swedish name rules; and the template's "ratio to OpenStreetMap" clause for
  Odense and Liepāja (fill it with an Overpass count per city, or drop it).
- [ ] **For the site-wide prose and UI pass (owner, 2026-09-30, calls A3, A6, A7,
  B6)**: dots on top of dots (Yokohama on Tokyo, Kitchener–Waterloo on Toronto;
  draw the older city on top or give the pair a regional view - the seven pairs
  stacked in their own region are `check_macro_labels.py`'s `KNOWN_STACKED`,
  measured 2026-10-01; take each out as it is fixed, and a new one fails); hide a pill
  whose own dot is off the canvas (Bordeaux's "Regional)", Nice's "N"; Daugavpils, off Europe's edge at 375 px,
  as Dublin and Bucharest); a short
  label for a long regional name (Most is cut to "(Regional)" at 375 px); and
  the Korean nightclub difference disclosed on What Is Excluded (the SEMAS
  satellites leave out dance halls, Seoul keeps nightclubs), with the two
  "as in every other city" sentences corrected.
- [ ] **What Is Excluded's opening generalisations (review lane 4, 2026-09-30;
  for the prose and UI pass)**: each bets on the next city and the tram kit
  outgrew them - light rail drawn only at 15-minute headways (Daugavpils's
  routes run hourly and are drawn), the commuter-rail list (Zurich's S-Bahn,
  NS at Den Haag, Göteborg's and Odense's regional trains are missing), the
  ring sizes at :118 and :135, and Florence's not-drawn list (T2.2). Rewrite
  them by category rather than as claims about every city.
- [ ] ⏰ **Philadelphia: 11th St back on 2027-08-30** (SEPTA's release of
  2026-08-06). Closed for works since 2026-09-05 and listed in
  `excluded_stations.csv` (`config.CLOSED_FOR_WORKS`; step 1 stops if the feed
  serves it again). When SEPTA reopens it: clear the entry, re-run the city,
  and drop the page's 11th St sentence.

- [ ] **Sacramento's Green Line: add it back when SacRT reopens it (due by
  mid-October 2026; check from 2026-10-15).** Suspended since 2025-06-16 for
  the Railyards works; not drawn, and 7th & Richards/Township 9 is in
  `outputs/sacramento/excluded_stations.csv` as closed for works
  (docs/category_rules.md, "Station scope"). When SacRT's schedule pages list
  the Green Line again, do four things:
  - move "Green" from `config.NOT_DRAWN_REFS` to `LINE_REFS` and clear
    `CLOSED_FOR_WORKS`;
  - add the new 7th & Railyards station, if OSM carries it;
  - read the Green Line's frequency from SacRT's timetable against the
    15-minute test;
  - re-run the city and update the page's Green Line sentence.

  OSM cannot signal the reopening, so this date is the guard. **Also retire,
  when OSM catches up**: `config.ADDED_STATIONS` (Dos Rios, placed from
  Wikidata) and `UNNAMED_STOP_NAMES` (Morrison Creek). Step 1 stops on its
  own once OSM carries either.

- [ ] **Gambling is bucketed inconsistently across taxonomies** (owner,
  2026-09-28, at Buenos Aires' LOTERIA call): Buenos Aires, Brazil and Berlin
  exclude lottery and betting premises (NAICS 7132, WZ 92), but
  `dublin_uses` counts BETTING SHOP as Retail. Decide one rule and sweep
  every taxonomy for it, with a drift measurement per city changed.

- [ ] Los Angeles: ~9% of registry rows have no NAICS code; consider whether
  the caveat needs to be visible on the city page.

- [ ] San Diego: exact `address_city == "SAN DIEGO"` undercounts
  neighbourhoods recorded under their own name (La Jolla foremost); decide
  whether to include them.
- [ ] San Francisco: only ~37% of rows carry a NAICS code; consider whether
  the caveat needs to be visible on the city page.
- These three are the only maps whose lean the city page does not state
  (`docs/map_inconsistencies.md` theme 10). The "Why the maps differ" page
  (page 92) hedges around them: "Where it is known, each city's page says
  which way its map leans." Once all three pages carry their caveat, that
  sentence can drop its hedge (published wording: owner's call).

## Later / maybe

- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
