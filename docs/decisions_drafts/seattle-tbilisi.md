# DECISIONS drafts - Seattle and Tbilisi build (`seattle-tbilisi-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - Seattle (Regional): the owner's two calls applied, 14,431 storefronts; both builds' wording and modes approved

- **The owner's calls on Seattle (2026-10-02, relayed by the Cleanup
  session), both as recommended:**
  1. **Lapsed Seattle food is kept only on a TRADE-NAME match** with a King
     County business inspected in 2025 or 2026, never on a street match
     alone. Lapsed food dropped: 331 (2023 60, 2024 102, 2025 169), of them
     the 157 a street match alone had kept.
  2. **The 32 Snohomish facilities with a blank `User_Fld` are placed by the
     place their point falls in**, the rule every other source here follows
     (`sno_food.load(include_blank=True)`). Lynnwood 310 -> 329 and
     Mountlake Terrace 57 -> 70 facilities by point-in-place.
- **Measured, steps 2 and 3 re-run**: storefronts 14,500 -> 14,431 (map
  14,430 after the contact-detail scrub). The Seattle register 9,349 ->
  9,198; King County food 3,193 -> 3,245, because 59 more inspected
  businesses in Seattle are no longer held back by a register row at their
  address that has now dropped out (the current inspected business replaces
  the lapsed licence); Snohomish food 352 -> 382. Food service 5,956 ->
  5,880, Retail 6,010 -> 6,017, Personal services unchanged. In a ring:
  5,589 -> 5,548 (38%); 2,122 / 2,545 / 881. Names shown as the category:
  426, unchanged. Drift check run and the baseline re-recorded; ring share,
  macro facts, the inconsistency rows, the master list, PLAN, About the Data
  and What Is Excluded updated. The page bullet on lapsed food now reads "a
  business of the same name" for "a matching business", to state the rule.
- **Approved by the owner (2026-10-02, relayed by the Cleanup session)**:
  Seattle (Regional)'s mode `light_rail`, coverage `narrowed`, notices 109
  to 113 and the page bullets; Tbilisi's notice 114, page caption and
  bullets, and its What Is Excluded and About the Data sections. The
  proposals flagged above are settled.

### 2026-10-02 - Tbilisi privacy verdict: publish

- **`check_personal_exposure.py tbilisi` gained a Georgian pass**
  (`pipeline/georgian_names.py`): the Latin heuristic cannot read Mkhedruli,
  so its zero was not a finding (the brief's warning).
- **The rule, tested on the processed file**: an individual entrepreneur
  (legal form 30) shown by name: **0** of 8,328 (owner, 2026-10-01: category
  only, Taichung's precedent). Their names and personal numbers never reach
  the disk: the fetch drops them in memory and step 2 asserts it.
- **Company names that read as a person's full name** (the heuristic: two
  Georgian words after the legal form, the second with a surname ending):
  148 of 4,924 company names shown, 147 of them beginning with their
  legal form (`შპს`, an LLC). Kept, on Seattle (Regional)'s precedent: a
  person-like name carrying an organisational marker is a company's
  registered name, public commercial information. Every company name shown
  but 30 begins with its legal form.
- **No residence signal**: the register states none; legal address equal to
  factual on 3.5% of kept individual-entrepreneur rows (Step 0), and those
  pins carry no name. No address is published for any pin.
- **Verdict: publish.** Row in `docs/privacy_verdicts.md`.

### 2026-10-02 - Tbilisi: Geostat's register at the factual address, 13,252 storefronts; district-center placeholders left off by the owner's rule

- **The pull**: 63,511 active entities with a factual address in region 11.
  The API has no column selection, so each page is reduced in memory to the
  kept columns plus three derived ones (a company's name; a placement key per
  factual address; a legal-equals-factual flag) before anything is written.
  On 2026-10-02 a 10,000-row page outlasted the API's gateway (HTTP 502)
  though Step 0 had pulled such pages that morning; 2,000-row pages took
  2-3 minutes each, about 70 minutes for the register.
- **The placeholder rule, re-derived at build** (owner, 2026-10-02): a point
  carrying 50 or more active rows whose commonest company factual address is
  a bare district or settlement name, or blank. The first pull reduced every
  numbered address to one marker, so "commonest" could not be taken (it found
  one point); measured, a share-of-bare-addresses proxy did not separate the
  ten known points from small named places, so the register was pulled again
  with each company's numbered address kept only as a 12-hex hash (no street
  address stored). The re-pull was stopped at page 7 of 32: **the owner chose to skip it for this build and run it before the next review** (2026-10-02). So step 2 runs a BOUNDED check on the build's pull: every point the pull proves qualifies must be listed, and every listed point must still carry 50+ rows. It proved one point Step 0 did not list, **Mtatsminda (41.695863, 44.792928: 27 of its 28 companies give the bare district name; 51 rows, 19 storefronts), added**. **33 other points of 50+ rows could not be settled** (1,629 storefronts): at nearly all, the commonest bare name appears 1 to 4 times against dozens of street addresses, the largest being the Lilo market (486 storefronts, a real address), so the full check is expected to confirm the eleven. The fetch already keeps the per-address hash, so the next pull runs the full check and step 2 exits if the set differs.
- **Taxonomy `georgia_nace`**, NACE Rev. 2 at the national leaf, modelled on
  France's NAF module, with a closed list: every code in divisions 45, 47, 56
  and 96 is named as kept or left out, and step 2 exits on one that is
  neither. Left out on the standing rules: market stalls (R1), nonstore
  retail, event and contract catering (R1), funeral, the 96.09 catch-all
  (R2; its leaves include pet grooming, training and boarding). Division 45
  on the precedent (owner, 2026-10-02): 45.11.2, 45.19.0 and 45.32.0 kept,
  1,516 rows; 45.11.1 (the wholesale half decides it), 45.11.3 (brokerage),
  45.20.0 (repair) and 45.31.0 (wholesale) out. **45.40.0, motorcycle sale
  WITH maintenance and repair in one code (34 rows), which the brief did not
  name, is kept**: R4's "a type that merges fuel with repair or a car wash
  goes whole" (Edmonton, Philadelphia). 45.11.3, also unnamed, is a
  broker, not a dealer, and stays out.
  47.73.1 is a veterinary pharmacy (kept, Retail); 56.10.0 merges restaurants
  with mobile food and is kept whole. Category continuity: a column for
  `georgia_nace`, every rule answered.
- **Counts**: 16,356 storefronts by the taxonomy (Retail 13,744 with division 45's 1,550, Food service 1,343, Personal services 1,269); 1,620 with no coordinate, 1,481 on the eleven placeholder points and 3 outside the city boundary are not shown; **13,252 placed (81.0%)**: Retail 11,114, Food service 1,074, Personal services 1,064. 8,084 (61%) within 0.6 mi of a station: 6,728 / 702 / 654. Company names 4,924; category only 8,328 (individual entrepreneurs).
- **Names**: a company shows its registered name in Georgian (with its legal
  form); an individual entrepreneur shows the category (owner). Fonts: the
  map declares no language; Segoe UI carries Georgian on Windows and the
  browser falls back elsewhere.
- **"Active"**: Geostat's own definition, "an enterprise which is engaged in
  economic activity" (Business Demography metadata, 0519); the
  turnover-or-staff criterion stays a secondary source's (IEM journal), so
  the page says only that a new business may not be shown yet.
- **Line 2's color**: OSM's `green` is a CSS keyword; its value #008000
  measured CIE76 37.2 against the Personal services pins, under the
  preferred 45, so #30A800, the nearest green that clears it (45.5), as
  Seattle's colors were moved.
- **Proposals for review** (no template covers them): the page's credit
  caption and notice 114's wording (the brief's proposed text, plus "Not
  endorsed by Geostat."); the page bullets on the register's limits; the
  What Is Excluded and About the Data sections.

### 2026-10-02 - Tbilisi: the metro from OpenStreetMap, 23 stations, gate 3 exact; a new West Asia region

- **Started after Seattle (Regional) was green and committed** (the kit's
  conditions: the owner had answered the brief's three calls the same day,
  and the move to a West Asia region of its own lifted the wait on the UK
  pass). `brief_check.py tbilisi` passed 12 of 12 before any code.
- **One Overpass query for the city** (overpass-api.de, first attempt, 94
  elements): the subway route relations, their route_masters, member nodes,
  track ways, every `station=subway` node, and the city's administrative
  relation (1996871, admin_level 4). The brief's Step 0 cache lacked the
  boundary, so the build issued this one query instead of reusing it. Four
  relations, two per line, all kept by `ref`; any other subway relation
  exits.
- **23 stations: 16 on the Akhmeteli-Varketili Line, 7 on the Saburtalo
  Line**, the 46 stop positions collapsed by name (widest 20 m) and matched
  one-for-one to the 23 `station=subway` nodes. Gate 3 against Tbilisi
  Transport Company's Stakeholder Engagement Plan (October 2024): "27.3 km
  with 23 stations on two lines"; the drawn track measures 19.6 + 7.9 km.
  Spacing: min 115 m (Station Square-1 and -2, both drawn under their real
  names, as both are in the operator's count), median 1,039 m, max 1,538 m:
  the standard rings. Every station is inside the city (504 km2).
- **"Nadzaledevi" in OSM is labeled Nadzaladevi**, the operator's and the
  register's spelling (`STATION_NAME_FIXES`; step 1 exits once OSM is
  corrected, so the fix cannot outlive the error).
- **Line colors from OSM**: line 1 `#FF0000`; line 2 `colour=green`, a CSS
  keyword, mapped to its CSS value `#008000`.
- **Region "West Asia"** (owner, 2026-10-02), appended to `REGION_ORDER` by
  `scaffold_city.py --new-region` with the reasoning in its comment; a view
  of its own, not in `COUNTRY_VIEWS`. Europe is unchanged.
- **Page 175; notice 114 (Geostat)** from the session's claimed block
  (115 and 116 unused).

### 2026-10-02 - Seattle (Regional) green: every gate run, baseline recorded, held for review time

- **Gates, in Band B's order:** personal exposure (publish; row in
  `docs/privacy_verdicts.md`); `check_provenance.py` names Seattle (Regional)
  OK (slug `seattle`); `check_scope_disclosure.py` OK; the four
  inconsistency rows and the themes it joins (several registers, Personal
  services thin, regional, type for a personal name); the master list
  (Band C to Built, 125 built, 43 candidates); `check_macro_facts.py` OK and
  the macro label measured (Space Grotesk 600, 120.5 px, controls exact) and
  placed west of the dot, PROBLEMS 0 over 15 regions and three widths, out
  of the default frame like Vancouver and Buffalo; the drift check zero
  drift, 40-figure baseline; ring share 5,589 of 14,498 (39%);
  `check_deploy_imports.py` PROBLEMS 0; `check_all.py` 44 of 44 after
  merging master; pushed as `seattle-tbilisi-build`, 0 behind.
- **Only Seattle's entries were added to `app/ring_shares.json` and
  `app/macro_facts.json`.** A full `--write` from this checkout also
  re-hashed twelve other cities' committed maps (line endings in the working
  copies); those entries were left as committed, and `check_ring_shares.py`
  passes on them.
- **Mode `light_rail`, coverage `narrowed` ("Personal services thin"),
  `rail_extra` "Trams" (light rail, the field's rule)** for the owner's
  approval with the build.
- **One quick browser render each** (the day rule): the map (both lines and
  labels, legend, clusters, OSM credit, no console errors) and the page in
  the lean app, in the page format's order. `deploy-verify` waits for review
  time (scope `city-added`).
- **A gap in a shared check, flagged as its own task:**
  `check_no_fetch_in_steps.py` does not follow a step's imports into its own
  city package (`pipeline/seattle/lcb_offpremise.py`, `sno_food.py`).

### 2026-10-02 - Seattle (Regional) privacy verdict: publish

- **Seattle (Regional) privacy verdict: publish.** `check_personal_exposure.py
  seattle` on the rendered map (5,589 pins inside the rings): no registrant
  fallback can exist, because no source's legal-name, contact, phone or
  mailing column is ever downloaded (step 2 asserts it); 0 emails, 0 phone
  numbers, 0 surname-first names; **0 person-like names at a residential
  unit**. The heuristic's 1,117 person-shaped names (20.0%) are shape
  matches on premises names, led by General Food Services (280) and
  restaurants (248); 52 of them sit at a commercial unit (STE, BLDG, FL, RM).
- **What makes it structural rather than lucky:** a Seattle trade name that
  IS the legal name (the server's own column comparison; ids only) and reads
  as a person's (90), a Bellevue sole proprietor's trade name that reads as
  a person's (50), a Bellevue row with no trade name (260), and any
  person-shaped name at a residential unit (26) show the category. The first
  render had shown 13 person-shaped names at a residential unit; the last
  rule took them off.
- **Re-run after any change to step 2 or the taxonomy** (`CLAUDE.md`).

### 2026-10-02 - Seattle (Regional): five sources in one step 2, 14,500 storefronts; the name rule on structural signals; two owner questions

- **Step 2 built on the owner's settled calls; 14,500 storefronts** in 13
  places (Seattle 10,298, Bellevue 2,029, Kent 469, Lynnwood 344, Federal Way
  339, Redmond 295, Tukwila 245, SeaTac 176, Shoreline 164, Mountlake
  Terrace 66, Mercer Island 53, Des Moines 19, the unincorporated slivers 3):
  Retail 6,010, Food service 5,956, Personal services 2,534. 5,589 lie inside
  a ring. (Sources: Seattle 9,349, King County food 3,193, Bellevue 1,415,
  Snohomish food 352, the Liquor Board 191.)
- **Seattle's register:** 54,689 rows; 1,246 exact duplicate rows (an export
  artifact) dropped, then one row per location at its latest licence
  (53,281); 988 outside the city by point-in-polygon dropped
  (unincorporated 816, Burien 139); 9,597 in the buckets. The head-office
  rule, coded as Taipei's (a HEADER QUARTER row on floor 3 or higher, or in
  a room, unless its building holds 20 storefront rows), dropped 1 row; the
  brief's 9 counted `#` suites, which are not floors.
- **Lapsed Seattle food, cross-referenced to King County's 2025-26
  inspections inside Seattle:** by licence year (rows / either match), 2023
  88 / 58, 2024 139 / 94, 2025 281 / 182, 2026 2,474 / 2,019; 30, 45 and 99
  lapsed rows dropped. Lapsed rows kept and disclosed: Retail 992, Personal
  services 435. **The hand sample of 20 lapsed food rows kept on a street
  match alone (157 such rows):** about 5 are the same business under a
  variant name, about 7 are a DIFFERENT food business now at the address
  (a closed predecessor kept by its successor's inspection), and 8 could not
  be read without printing a person-shaped name. Brought to the owner
  (below).
- **King County food is a source in Seattle too**, as the brief's table has
  it ("own register + King County food"): 1,572 of the 5,182 inspected
  businesses in Seattle match no register row by trade name or street
  address, and join as King County rows; 949 are storefronts in the scope after the name layer.
  The first build had read King County as a cross-reference only in Seattle,
  which left a quarter of the city's inspected food premises off the map.
- **King County food placed by parcel** through the County's address points:
  9,372 on the parcel at the business's own address, 2,455 at the parcel's
  primary point, 196 by an address that names one place only, 107 unplaced
  (of 12,130 inspected in 2025 or 2026). R1 classes out (mobile 648, school
  lunch 467, catering 307, nonprofit institution 258, commissary 29,
  donated-food 21, bed and breakfast 4). Grocery stores, meat and fish
  markets and bakeries are Retail (a food register's shops are shops).
- **Bellevue:** 24,566 rows not cancelled; 12,593 inside the city; 1,819
  Retail and Personal services; 322 issued before 2010 dropped (the owner's
  cutoff); 5 with no issue date kept.
- **The name rule rests on each register's structural signal, not on the
  shape test alone.** `looks_personal` by itself read 2,079 of Seattle's
  9,349 rows as people ("BLUE MOON" is two words). Instead:
  - Seattle: the trade name IS the legal name, asked of the server as a
    column comparison (`BUSLIC_TRADE_NAME = BUSLIC_LEGAL_NAME`, 20,519
    location ids, no names downloaded), AND person-shaped AND no
    organisation word: 90 rows show their category.
  - Bellevue: a sole proprietorship whose trade name is person-shaped: 50;
    no trade name: 260 (the owner's rule).
  - Any source: a person-shaped name at a residential unit: 26.
  - The food registers and the Liquor Board name premises, left to
    `check_personal_exposure.py`.
- **Line colours** moved just past the Delta-E 45 floor: the 1 Line
  #3DAE2B (37.8 against Personal services) to #46C831 (46.2), the 2 Line
  #00A0DF (28.6 against Retail) to #00B6DF (45.3).
- **Unincorporated Snohomish County:** 0.34 km2 of Lynnwood City Center's
  ring lies outside the city. By rule 7 it takes the neighbour's data, which
  is the same Snohomish layer (`User_Fld` UNINCORPORATED) and the Liquor
  Board's list: 2 storefronts.
- **Snohomish layer (agent leg):** 310 and 56 facilities reproduced. A
  facility holding Restaurant and Grocery permits (250 county-wide) is a
  Grocery: 249 of the 250 hold a GROCERY permit, and their Restaurant
  permits are the store's deli, meat, bakery and coffee counters. One
  UNINCORPORATED facility lies inside Mountlake Terrace's polygon, so the
  city's count includes it.
- **The Liquor Board's off-premise list (agent leg), dated 2026-09-29:**
  8,793 privilege rows; King and Snohomish 3,151; licence ACTIVE (ISSUED)
  2,010 licences; a current (approved, not terminated) privilege 1,861;
  retail privileges 1,839 licences at 1,837 premises. WINE RETAILER RESELLER
  (an add-on letting a shop sell wine to restaurants; every holder keeps a
  retail privilege) and BEER/WINE GIFT DELIVERY (22 delivery-only licences)
  are not storefronts. A premises is labelled by its grocery licence first,
  then spirits, then specialty. Placed by joining the fixed-width premises
  address (cut at 30 characters, the rest spilling into the room field) to
  the county address points: 1,409 of 1,837 (King 1,312 of 1,367, 96.0%);
  the 336 Snohomish misses lie outside the Lynnwood and Mountlake Terrace
  box, by design. The same matcher reproduces King County food's own parcel
  for 96.6% of rows (within 50 m). Never geocoded, never fuzzy; three
  Mountlake Terrace shops at one spread address and four airport concourse
  shops are left off. 191 premises reach the map, outside Seattle and
  Bellevue. The Board's data-transfer notice is still on its lists page and
  is repeated on the page.
- **Snohomish County's Building Address Points (the Liquor Board join
  target in Lynnwood and Mountlake Terrace) read SILENT, with the food
  layer's conditions** (`licence-read`, 2026-10-02): the item is in the
  County's open-data catalogue and its own `licenseInfo` carries the
  County's disclaimer (no warranty, hold-harmless, no commercial use of lists
  of individuals); nothing to display or do. The owner's permissive reading
  of the sibling food layer extends to it on firmer ground. Its description
  adds "Any other use of these data are not directly supported by Snohomish
  County", read as "no support", not a prohibition.
- **King County food and Snohomish food: a name layer** (Minneapolis's and
  Pittsburgh's precedent, `docs/category_rules.md`): a workplace cafeteria or
  contract caterer (499; Microsoft's campus files its cafes as "BUILDING nn",
  27 in Redmond), a hotel kitchen (152), a vending route or micro-market
  (64), a members' club, theater or airline lounge (36), a pharmacy (11) is
  left out by name. Minneapolis's patterns were adapted, not imported: its
  CHURCH pattern took CHURCH'S CHICKEN and its CAFETERIA pattern a public cafe;
  BOEING FIELD CHEVRON is kept. The total fell from 14,854 to 14,500.
- **Proposals for the owner's review (sentences no template covers):** the
  page's bullets on the five publishers, the lapsed-license sentence, the
  Bellevue cutoff, the Snohomish date, and the name rule; the caption of
  credits under the map; and the five notices' displayed text (109 to 113),
  King County's two prescribed texts word for word, Snohomish's in the
  owner's words, the rest the project's own.
- **For the owner, with recommendations (the build follows the settled
  calls until answered):**
  1. **Street-only matches for lapsed Seattle food.** Recommend keeping a
     lapsed food row only on a trade-name match (drop the 157 kept on a
     street match alone): the sample shows the street match mostly keeps a
     closed predecessor. Precedent: the owner's own warning in the brief
     ("an address match can be a different business at the same address").
  2. **Snohomish rows with a blank `User_Fld` inside the two cities** (32:
     Lynnwood 19, Mountlake Terrace 13). Recommend taking them by
     point-in-place, the rule every other source here follows: the field
     was chosen over the postal city, and a blank is evidence of neither.
     It would move Lynnwood from 310 to 329 facilities and Mountlake
     Terrace from 56 to 69.

### 2026-10-02 - Seattle (Regional): rail from OpenStreetMap, 39 stations in 11 cities, Pinehurst placed from Sound Transit

- **The brief's claims held: `brief_check.py seattle` passed 16 of 16** on
  2026-10-02 before any code was written.
- **Rail from OSM route-relation membership, one Overpass query for the
  corridor box** (47.28 to 47.84 N, -122.42 to -122.08), answered by
  overpass.kumi.systems after a 504 from overpass-api.de. Twelve relations
  came back: Link's four (1 Line 3494092 and 5517060, 2 Line 17499739 and
  17499740; network `Link`, refs `1 Line` and `2 Line`), the Seattle
  Streetcar's four and the airport's SEA Underground four. The streetcar and
  the people mover are named in `NOT_DRAWN`: the owner's scope is Link's 1
  and 2 Lines.
- **OSM carried 38 stations; Pinehurst, opened 2026-09-30, was the 39th.**
  It was placed from Sound Transit's own Pinehurst Station page (13110 5th
  Ave NE), at King County's address point for that address, and step 1
  refuses the addition once OSM's relations carry the station (Taoyuan's
  rule, `osm-rail`). Sound Transit's GTFS was not used for it, per the
  owner's call on its terms.
- **Gate 3 from Sound Transit's own line pages** (read 2026-10-02): the 1
  Line serves 27 stations and the 2 Line 26, 39 distinct, 14 on both. The
  brief's "39 stations in 11 cities" agrees.
- **Notices 109 to 116 claimed** in `docs/session_roles.md` (109 to 113 for
  Seattle (Regional)'s publishers, 114 to 116 for Tbilisi); staging told.
