# UK, tram and city watch items

Detail moved verbatim from `PLAN.md` on 2026-10-08 (commit c75f4802); `PLAN.md` holds each item's one-line status and points here by heading.
This is open work, not a record: update an item here as it moves, and send a finished one to `docs/plan_done/`.

## Left by the 2026-10-03 lanes batch

- [ ] **Left by the 2026-10-03 lanes batch, each needing a fresh pull:**
  - **Rome's tram 3 is back in service** (ATAC, 2026-09-07), but the cached
    GTFS has no route-3 trips and no tram 3 relation is cached: a feed and an
    Overpass re-pull (one query), steps 1-3, drift check.
  - **Oslo's tram 13 stops west of Thune** are not yet listed as left out
    (Sollerud is missing from the cached `stops.txt`; Lilleaker's tram quays
    cannot be told from its bus quays). A fresh Ruter feed settles both.
  - **SFMTA's clause 4:** notice 3 displays its disclaimer on the cautious
    reading. Owner's call to keep or drop; kept until then.

## The UK six's watch items

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

## Toulouse and Rennes

  - [ ] **Toulouse and Rennes: did step 1's name-level fallback fire?** The
    pure-extract rule (owner 2026-09-29) forbids a station at the MEAN of
    same-named platforms (`step1_stations.py`, "collapsing N name(s)").
    Re-run step 1 read-only or read its drift log; if it fired, take the
    first platform's coordinates, drift-check, review time.

## Groundwork before the tram batch

  - [ ] **Groundwork before the tram batch (staging, 2026-09-29)**; (1) the
    France kit is done, and the French pages exist. Left, unticked: (2)
    licence reads up front (Bordeaux LO 1.0, four ODbL feeds, Plzeň and
    Olomouc GTFS, Tucson, RideKC, Florence), each notice recorded before a
    page exists; (3) page text by template; (4) the macro-map items here; (5)
    re-measure Streamlit Community Cloud (memory, clone time, the Overview
    list; `docs/scaling_thresholds.md` dates from 9 cities); (6) scoped
    `city-added` deploy-verifies per landing group.

## Prague: Flora reopens

- [ ] ⏰ **Prague: Flora reopens** (about the end of February 2027 per the
  re-check calendar): when PID's feed serves it again, step 1 STOPS on
  purpose; remove the override then and Flora is drawn from the trips
  (listed as closed for works until then, owner 2026-09-29).

## Band T's group decision

  - [ ] ⏸ **Band T's group decision, DEFERRED by the owner 2026-09-27** until
    the full tram list exists and the second-wave screens are done: which
    trams-only cities to build, and in what order (Nice, Montpellier, Brno
    and Bergen are the cheapest strong ones). Load and per-category
    recommendations: `docs/tram_rescope_estimate.md`.

## Wave-2 follow-ups

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

## Watch items from group 1

  - **Watch items from group 1:** Salvador's VLT (draw it once in revenue
    service); Teresina (all-day 15-minute service); the Hazel McCallion Line
    (early 2028); Luas Cork (after 2028); ION Stage 2 to Cambridge.

## Fifteen rail cities

- [ ] **Fifteen rail cities were screened shallowly; nothing surfacing is NOT
  a disqualification.** Atlanta, Baltimore, Portland OR, Phoenix,
  Minneapolis, St. Louis, Cleveland, Pittsburgh, Detroit, Jersey City,
  Tucson, Sacramento, Salt Lake City, Honolulu, Buffalo. Twelve were "not a
  Socrata domain" and the ArcGIS pass searched titles only (Seattle was
  missed that way). Each needs a per-portal check before being written off.

## Berlin

- [ ] **Berlin:** when the U6 reopens to Alt-Tegel (about August 2027), step
  1 stops on the refetch; take the five stations out of
  `config.CLOSED_FOR_WORKS`, re-run steps 1-3. Monthly: IHK updates the
  register on the 1st; VBB's calendar ends 2026-12-12, so refetch before.

## London

- [ ] **London:** refetch before the FSA extracts age (`fetch_sources.py
  --force`); if OSM starts carrying one of the eight added stations, step 1
  stops and says so.

## Buenos Aires

- [ ] **Buenos Aires:** `docs/map_inconsistencies.md`'s prose lists (street
  surveys, modes not drawn, in-ring shares, pin labels) to name it
  (cleanup's `city-landed buenos_aires`); refetch SBASE's layers (dated
  2026-09-01) with `fetch_sources.py --force` when BA Data updates them.

## Trams left off built maps

- [ ] **Trams left off built maps: the rest is in its own session since
  2026-10-13 (branch `tram-rescope`); the owner decides case by case.**
  **Built and on master since 2026-09-27** (merge be2e3713): Montreal's REM,
  Rome's tram 8, Madrid's ML1, Paris T3a and T3b, San Francisco's F Market &
  Wharves. Mexico City's Cablebús and Mexicable are built on the branch (2026-10-13). Toronto's eight running streetcar lines are built on the branch (2026-10-13; 503, 507 and 508 wait on the TTC's timetable after 10-31, `docs/recheck_calendar.md`). Milan's 17 tram lines are built on the branch (2026-10-13, on ATM's timetable to 10-02; re-read when AMAT republishes, `docs/recheck_calendar.md`). **Left:** Prague, on the per-route label
  and legend rule. Hong Kong Tramways is out (owner).
  Estimate as first written: `docs/tram_rescope_estimate.md`.
  - **Barcelona TRAM: OUT (owner, 2026-10-13).** Measured that day: none of
    its 28 stops inside the city is beyond the 0.6 mile ring of a drawn
    station, and rings on them add no storefront. The page's "not drawn"
    wording is owed, for the owner's approval.
  - **Cablebús, measured 2026-10-13:** all 19 stations now carry
    coordinates in OSM, and 15 are beyond the 0.6 mile ring of drawn rail;
    17,783 storefronts would gain a ring. Mexicable (out, owner 2026-10-04)
    is the open question beside it.
  - **Rome's other trams (2, 3, 5, 14, 19):** tram 3 runs Trastevere - Porta
    Maggiore since 2026-09-07; the whole network is due back by 2026-11-23
    (`docs/recheck_calendar.md`). ⏸ **Parked by the owner 2026-10-13 as ONE
    decision for all five after 2026-11-23**; none drawn before.
  - **Candidate still open (stops in scope):** Prague (285). Toronto's
    streetcars and Milan's trams are built on the branch; Barcelona TRAM is out.
    Fortaleza's VLT failed the rail test. D.C. Streetcar ended 2026-03-31.
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

## Not ready for main

**Not ready for main:**
- **Band C (7)**: one owner decision moves all seven: does a single-bucket
  page belong beside three-bucket cities? Yokohama (personal services only)
  has no page for now whatever the answer (owner, 2026-09-24).
- **Band D (7)**, each waiting on an owner act or access: Sendai's request
  (drafted) and Kaohsiung's; reads from inside Poland, India, Finland
  (Helsinki) and Estonia (Tallinn) by a person there, never a proxy;
  Lisbon's DGAE account (item 28); Tallinn's EHR order (item 23).

## Zurich

- [ ] ⏰ **Zurich: rebuild after 2026-12-12** (owner, 2026-09-30, call C1):
  VBZ's temporary trams 50 and 51 are drawn until then; when they stop,
  re-run step 1 and step 3 and drift-check.

## Philadelphia: 11th St

- [ ] ⏰ **Philadelphia: 11th St back on 2027-08-30** (SEPTA, 2026-08-06).
  Closed for works since 2026-09-05 and listed in `excluded_stations.csv`
  (`config.CLOSED_FOR_WORKS`; step 1 stops if the feed serves it again).
  When it reopens: clear the entry, re-run the city, drop the page's 11th St
  sentence.

## Sacramento's Green Line

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

## Yamagata: the September food list

- [ ] **Yamagata: rebuild on the city's newer food list (owner, 2026-10-11:
  "let's add to the list of cities scheduled for updates").** The map is
  built on the list of 2026-08-31, the edition its brief measured. On
  2026-10-10 the city replaced it with `062014_syokuhin_list_20260930.csv`
  and the August URL answers 404; the city renames the file every month. To
  update: `python pipeline/yamagata/fetch_sources.py city --force` reads the
  current link from the dataset page (`config.SOURCE_LINKS`), under a new
  file name; then a new `FOOD_AS_OF` and `TERM_AS_OF`, every figure in the
  config, page, notice and docs rows re-measured, the privacy check and the
  drift baseline again. MHLW's file is re-pulled with it, so both lists
  carry one month.
