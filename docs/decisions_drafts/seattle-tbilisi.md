# DECISIONS drafts - Seattle and Tbilisi build (`seattle-tbilisi-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

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
