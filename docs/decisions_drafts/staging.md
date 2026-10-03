# DECISIONS drafts - staging (`worktree-staging`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-02 - Licence reads for the zero-reading sources: D.C. register and boundary, geo.api.gouv.fr, Dublin's NTA GTFS (owner)

- **D.C. Basic Business License: PERMITTED WITH CONDITIONS (CC BY 4.0).**
  - ArcGIS item `85bf98d3915f412c8a4de706f2d13513`. Its `licenseInfo` and
    metadata `useLimit` say CC BY 4.0.
  - The District's data terms and Mayor's Order 2017-115 §X say CC0
    "unless otherwise noted". The item does note otherwise, so comply with
    CC BY 4.0, which satisfies both.
  - Credit the Department of Licensing and Consumer Protection, link the
    licence, and say the data was modified. Nothing is owed. No owner call.
- **DC Boundary: PERMITTED WITH CONDITIONS (CC BY 4.0).** Item
  `7241f6d500b44288ad983f0942b39663` has the same CC0 note. Credit the Office
  of the Chief Technology Officer (DC GIS), link the licence and say
  "reprojected". It is not drawn. No owner call.
- **geo.api.gouv.fr (26 French cities): PERMITTED WITH CONDITIONS, the
  licence unclear.**
  - The API declares none. The dataset it is built from ("Contours
    administratifs", data.gouv `683424e996857155175d4f68`) says ODbL; IGN's
    ADMIN EXPRESS says Licence Ouverte.
  - A 2025-10-15 question to the publisher is unanswered.
  - **Owner: show both credits:** an ODbL §4.3 notice naming "Contours
    administratifs", and the Licence Ouverte source-and-date line. The
    repository link discharges ODbL §4.6.
- **Dublin's NTA GTFS: PERMITTED WITH CONDITIONS (CC BY 4.0).**
  - The download page and data.gov.ie (`nta-gtfs`) say CC BY 4.0 and
    prescribe: "This data is licensed under CC BY 4.0 and is attributed to
    the National Transport Authority."
  - The developer portal's Fair Usage Policy also claims GTFS data, with an
    uncapped indemnity for any claim resulting from use. The download page
    never links it.
  - **Owner: "plain CC BY for dublin"**: the indemnity is not accepted. The
    credit still meets the Policy's §7 as well:
    - the NTA's sentence;
    - the licence link;
    - "three routes extracted and redrawn, colours this map's own";
    - "as is";
    - no endorsement.
  - Link data.gov.ie rather than nationaltransport.ie (its website terms'
    clause 5 on linking).
- **Still running:** the CARTO basemap, and the LA County, MassGIS and
  SANDAG boundaries. Cleanup gets every verdict's row and credit together.

### 2026-10-02 - Japan wave 2's calls settled; Chiba to R; zero-reading licences sent for reads; gaps to Cleanup (owner)

- **The owner: "approve all recommendations, for 4 mark chiba to R, run the
  licence reads and send gaps to cleanup".**
- **Wave 2's calls**, recorded in each brief's header block:
  - **Drawn as cut:** the urban lines cut to stubs in Kawasaki, Nishinomiya,
    Toyota and Higashiōsaka (Sakai's precedent).
  - **Shimonoseki:** the 7 San'in stations beyond 小串 are LEFT OUT, which
    was staging's recommendation (the agent's had been to draw them), so 14
    stations get rings.
  - **Nara** is built despite thin rail. **Hamamatsu** gets no MHLW
    notifications layer.
  - **Accepted:** Kawasaki's two CC BY versions (both named), Toyota's
    register scope, Ōtsu's city-site food file.
  - **Modes and laundry:** Yokosuka `metro`, Ōtsu `light_rail`;
    Nishinomiya's laundry at 62% kept and disclosed.
- **Chiba to Band R:** its complete city lists sit under all-rights-reserved.
  The way through is the owner's permission request; the MHLW-only food page
  is not built. Candidates: A 9 · B 5 · R 26 = 40.
- **Licence reads started for the zero-reading entries** in
  `docs/licence_positions.md`: Dublin's NTA GTFS, D.C.'s Basic Business
  License, the DC Boundary, the CARTO basemap, geo.api.gouv.fr, and the LA
  County, MassGIS and SANDAG boundaries.
- **The repository link.** The owner asked whether LinkedIn or GitHub icons
  were already in the page headers. They are not, on master or on any
  branch. The repository (github.com/dacekroberts/expanded-heatmap) is public
  to a logged-out visitor, so a GitHub link in the header would discharge
  IDFM Art. 5.8 and ODbL §4.6. A LinkedIn link needs the owner's profile URL.
  Passed to Cleanup with the other gaps.

### 2026-10-02 - Japan wave 2: 15 briefed, Wakayama discarded; licence positions ranked

- **The owner: "brief now, hold on builds".** Five agents briefed the scope's
  16 cities by region. Staging re-ran every brief: 15 pass all their checks.
  - **Band A (9):** Kawasaki, Yokosuka, Himeji, Nishinomiya, Takamatsu,
    Toyota, Yokkaichi, Ōtsu, Nara.
  - **Band B (6):** Chiba (food, MHLW alone), Hamamatsu (personal services),
    Higashiōsaka (food), Kurume, Sasebo and Shimonoseki (food, MHLW).
  - **Wakayama is discarded on coverage.** Its only list is opt-in, 51% of
    the restaurants in force, with no personal-services list.
  - Candidates are now A 9 · B 6 · R 25 = 40, with 122 discards. Builds are
    held.
- **Open with the owner (🚨 in the briefs):**
  - urban lines cut to stubs, recommended drawn as cut (Sakai's
    precedent): Kawasaki, Nishinomiya, Toyota, Higashiōsaka;
  - Shimonoseki's seven San'in stations beyond 小串, at about 8–10 trains
    a day. The agent says draw them; staging leans to leaving them out
    (Brazil's frequency discards);
  - Nara's thin rail (14 groups; recommended build);
  - Chiba's all-rights-reserved city lists (a permission request would
    open three buckets);
  - Hamamatsu's MHLW notifications as partial food (recommended no);
  - Kawasaki's two CC BY versions; Toyota's register title; Ōtsu's food
    file on the city's site only (all recommended accept);
  - modes for Yokosuka (metro) and Ōtsu (light_rail);
  - Nishinomiya's laundry list at 62% (keep, disclose).
- **New shared code** (each brief lists it): more column spellings; a
  `wareki_date` form; `norm_town` rules for 大字 and 字甲/乙/丙; addresses of
  only "<city>内" treated as not premises; Nara's old-law restaurant types;
  month-renamed fetches.
- **Licence positions ranked** (owner: "list our weakest to strongest notice
  positions"): `docs/licence_positions.md`.
  - **142 grouped entries:** tier 1 (weakest) 28, tier 2 (conditional) 48,
    tier 3 (open licence) 44, tier 4 (public domain) 22.
  - **The weakest:** Philadelphia (an unanswered permission request), King
    County food, Dublin's NTA GTFS (no reading), D.C.'s register (no
    reading), Snohomish, Bellevue, Daegu, Den Haag, Bucharest, CNEFE.
  - **Flags:** missing licence rows (D.C., NTA, CARTO, several boundaries,
    geo.api.gouv.fr); no public-repository link in the app (IDFM Art. 5.8,
    ODbL §4.6); missing credits (NTA, Milan rail, SFMTA's disclaimer,
    STM's modification sentence, MLIT for all 20 Japanese cities).

### 2026-10-02 - A re-check calendar for every built city; Vancouver's extension probed; Arlington measured

- **`docs/recheck_calendar.md`** (owner: "let's update this calendar across
  all currently-built cities").
  - Four research agents covered the 144 built cities by region. Staging
    merged them, with an action list for the next 120 days and the doc
    corrections found, which go to Cleanup.
  - **Owner calls it raises:** São Paulo's Linha 17, in passenger service
    since 2026-03-31, and Linha 6's assisted operation; Rome's returning
    trams; Taoyuan's Green Line.
  - **Build fixes it raises:** Osaka's missing Yumeshima (N02-25);
    Hiroshima's Hiroden loop; Sacramento's Green Line reopening.
  - **High priority:** SIRENE switches to NAF 2025 on 2027-01-05/06, so a
    French re-run on a new file would empty every French map without a
    mapping.
  - **Stated gaps:** rail news was not searched for 14 American cities;
    Tbilisi is in no share.
- **Vancouver (Regional) probed and ready** (`docs/build_briefs/vancouver_regional.md`).
  - Burnaby now answers scripted REST queries: 20,054 approved licences,
    every row a point, 2,143 in the buckets.
  - New Westminster and Coquitlam were already measured.
  - 20 stations come in. Richmond (R) and Port Moody (no addresses) stay
    out.
  - Three small owner items, each with a recommendation.
- **Arlington measured before it went to R**: 2,399 bucket premises, 94.3%
  joined exactly to the County's address points. Recorded on its R row.
- **The extensions are now probed:**
  - ready together: Rio + Duque de Caxias, Belo Horizonte + Contagem, Los
    Angeles + Long Beach, Vancouver (Regional);
  - out: Washington D.C. + Arlington (R).

### 2026-10-02 - Arlington left out of Washington D.C., to Band R as Richmond was (owner)

- **The licence read (2026-10-02): not permitted as it stands.**
  - Arlington County's "Active Business Licenses" (data.arlingtonva.us
    dataset 30) carry no licence.
  - The only terms the portal links, the County website's Terms &
    Conditions, allow "non commercial, personal use only" and forbid
    reposting or derivative works "without the written permission in each
    instance".
  - The 2016 Open Data Public Use Notice granted share-and-adapt for any
    purpose. It has redirected to the A-Z index since the 2023 relaunch,
    while the portal's guide still cites it.
  - The GIS hub's address points are SILENT on reuse and assert copyright.
- **The owner: "leave arlington out for now, like richmond".** Richmond (BC)
  went to R on 2026-10-01 on site terms of "research and private use only".
  Arlington joins Band R as D.C.'s add-on.
  - Its way through is a written question to the County, which is the
    owner's to send; nothing is drafted.
  - Candidates are now R 25.
- **The extensions now ready to build together:** Rio + Duque de Caxias,
  Belo Horizonte + Contagem and Los Angeles + Long Beach. Vancouver
  (Regional) waits on the Burnaby probe.

### 2026-10-02 - The UK six built on their branch; brief corrections received; numbers ledger

- **The UK lead reports all six built on `uk-six-build`,** pushed and held
  for review time. Its brief corrections, each in its city's entry in
  `docs/decisions_drafts/uk-six.md`:
  - **Placement on the full files, below the briefs' samples:** Edinburgh
    95.4% placed (93.9% at a point) against the brief's 96.6%; Sheffield
    95.3% against 96.4%; Wyre 83.2% against 84.5% (its private addresses
    arrive with an EMPTY postcode); Rushcliffe 79.6% against 80.2%.
  - **Nottingham:** each OSM relation is one direction end to end; NET lists
    50 stops, not about 51; Rushcliffe holds 4.
  - **Edinburgh:** the Newhaven stops are under NaPTAN's 9400ZZTW prefix.
    "23 stops" is the timetables page's map; its table lists 13.
  - **Birmingham:** every 4 to 11 minutes by day, not 8 to 12. Line 2 is
    still not open (due about 1 November), so Dudley stays out.
  - **Sheffield:** OSM's 52 names are 51 stops, one spelled two ways. NaPTAN
    renamed Shalesmoor "Kelham Island" in 2025.
  - **Blackpool:** 26 stops in Blackpool and 14 in Wyre.
- **The master list's Band B rows are left as they are on master.** The UK
  branch's own master-list step (gate 5) moves the six to Built at landing.
  Editing the same rows here would only make that merge conflict. The
  corrected figures land with them.
- **The lead's open items for the owner:** Edinburgh's centroid tier, and
  Sheffield's stop name (Shalesmoor or Kelham Island).
- **The numbers ledger (2026-10-02):**

  | Session | Pages | Notices |
  |---|---|---|
  | UK six | 156–161 | 84–96 |
  | Japan batch | 162–173 | 97–108 |
  | Seattle (Regional) | 174 | 109–113 |
  | Tbilisi | 175 | 114–116 |

  Each block is claimed on its own branch's `docs/session_roles.md`.
  Seattle's brief passes 16 of 16, and Seattle (Regional) is scaffolded at
  page 174.

### 2026-10-02 - Tbilisi's three calls, all as recommended (owner)

- **The owner: "approve all three tbilisi recommendations".**
  1. **Placeholder coordinates: drop and disclose** (Madrid's zero
     coordinates). 1,295 kept rows sit on ten district-centroid points, 805
     of them on four metro stations, which would have inflated Isani,
     Didube, Samgori and Liberty Square by 164 to 255 dots each.
  2. **Division 45: the precedent (R4).** Keep 45.11.2 vehicle retail
     (435), 45.19.0 (21) and 45.32.0 parts retail (1,060). Leave out
     45.11.1 "wholesale and retail" (117) and all repair.
  3. **Region `Europe`, measured, approved and then REOPENED the same day.**
     The owner: "actually tbilisi is quite far away from other cities".
     Dublin to Tbilisi is about 3,700 km, past the 3,300 km at which Canada
     was split. Fitted into Europe, Europe's centre would move about 9
     degrees east.
     - **Settled: a new leaf region, "West Asia".** The owner: "west asia
       could work too", "if georgia is officially in asia … we don't need to
       modify europe".
     - The UN M49 geoscheme puts Georgia in Western Asia. The name pairs with
       East Asia and is named for the area, so a later Baku, Yerevan or
       Ankara joins it. Europe is not modified.
     - The owner first floated Europe West and East regions, with a look by
       Cleanup. The first message to Cleanup failed to send. The owner then
       asked that Cleanup be told every option, and it was.
     - **Closed: Europe is NOT split** (owner, 2026-10-02, after Cleanup's
       measurement with `fit_view` and `label_competition.compete` at 375,
       768 and 1200).
       - Europe today: 26 cities, zoom 2.81, all labelled.
       - Without the UK: 23 cities, zoom 2.81, all labelled.
       - A West/North-East split: zoom 2.91 and 2.76, no gain.
       - A North/South split: zoom 2.24 and 2.10, with only 6 of 8 and 9 of
         15 labelled.
       - The only crowding is Den Haag, Rotterdam and Amsterdam (3-8 px). It
         stays on the stacked-dots review list.
- **Tbilisi now waits only on Seattle being green** (`docs/handoff_seattle_tbilisi_2026-10-02.md`).

### 2026-10-02 - Seattle (Regional) released to its own session, Tbilisi queued behind it (owner)

- **The owner: "should we pass the seattle regional brief to a new session?
  and queue Tbilisi after?"**, then "yes" to staging's plan.
- **One lead, with agents only for clean splits.** Seattle (Regional) is one
  page from five sources across 11 cities, meeting in one step 2, so it does
  not split by city the way the UK and Japan batches do. The Liquor Board
  layer and the Snohomish filter are the agent-able legs.
- **Tbilisi waits on three conditions:**
  - Seattle is green;
  - the owner answers its three calls (placeholder coordinates, division
    45, region);
  - the UK session's region pass has landed, since that pass changes
    Europe's frame and Tbilisi's label is measured there.
- **Numbers:** pages 174 (Seattle) and 175 (Tbilisi); notices from 109.
- **Set up:**
  - `.claude/worktrees/seattle-tbilisi` on `seattle-tbilisi-build`, with
    the junctions and no upstream;
  - the kit `docs/handoff_seattle_tbilisi_2026-10-02.md`;
  - the prompt, given in chat.

### 2026-10-02 - Georgia profiled, Tbilisi briefed; Geostat's terms stored

- **`add-country` for Georgia** (`docs/georgia_step0_endpoints.md`). There
  is no disqualifier: one national register, Geostat's Statistical Business
  Register, on a keyless API with a factual address separate from the legal
  one. Its traps:
  - `X` is latitude and `Y` is longitude.
  - The API has no column selection, so personal columns are dropped in
    memory.
  - It allows about 50 requests a window (HTTP 429 with `retryAfter`). A
    brief re-run straight after another one fails on 429; that is a RETRY,
    not a brief to correct.
  - Names return in Georgian script whatever the language, so
    `check_personal_exposure.py` needs a Georgian pass.
  - `Activity_2_Code` is NACE Rev.2; `Activity_Code` is the old scheme.
- **Tbilisi's brief** (`docs/build_briefs/tbilisi.md`):
  - 14,806 storefronts after the standing exclusions: Retail 12,194, Food
    1,343, Personal 1,269. The catch-all share is 9.6%.
  - 64.4% are individual entrepreneurs, shown as unnamed dots (owner,
    2026-10-01).
  - **Real coordinates 81.3%, not the screen's 91%:** 1,295 rows sit on ten
    district-centroid placeholders.
  - Metro: 2 lines and 23 stations (OSM 16 + 7), matching the operator's
    "23 stations on two lines".
  - Geostat's terms are PERMITTED WITH CONDITIONS (credit Geostat, no
    logo), stored unaltered in `docs/licenses/` with SHA-256.
- **Open for the owner:**
  - the placeholder coordinates;
  - division 45 (motor vehicles);
  - the region.

### 2026-10-02 - Seattle (Regional): rail from OSM, Snohomish read permissively, HQ rows with the head-office rule, lapsed food cross-referenced to King County, Bellevue food from King County (owner)

- **Sound Transit's GTFS is not used** (owner: "we can use openstreetmap
  here"). Its Transit Data Terms add a "No Changes" clause, a duty to pass
  the terms on, an open indemnity, an email registration and usage metrics.
  Rail comes from OSM. Gate 3's count comes from Sound Transit's station
  pages.
- **Snohomish County's food layer: "permissive read".**
  - The layer's own terms are SILENT. Item
    `75bf161b46ba484a97e6d7f1c63f21a4` was published by Public Works Solid
    Waste and is not in the open-data catalogue.
  - The county's GIS data disclaimer is read as governing, with its
    hold-harmless for errors in the data.
  - Credit "Snohomish County, Food Service Establishments (2025)", never the
    health department. The removal rule is the safety net.
- **Snohomish permit types: "keep only those points"**, Restaurant and
  Grocery. That is R1 (2026-09-29): school kitchens, donated-food
  distributors, food trucks, caterers, vending and concessions are out.
  Lynnwood keeps 310 facilities and Mountlake Terrace 56.
- **Seattle's lapsed licences: the alternative** (owner: "we can try the
  alternative for 4", replacing "drop 2023-2024" the same day).
  - Staging had reported the year-drop's loss as not small. By trade name,
    35 to 38% of the 2023 and 2024 food rows match a currently inspected
    business, against 65% for 2026.
  - **Every licence year stays.** A lapsed food row (licence year 2025 or
    earlier) stays only if it matches a business King County inspected in
    2025 or 2026, by name or street address.
  - Lapsed retail and personal-service rows stay, disclosed as possibly
    closed.
- **Bellevue confirmed** (owner: "king county food cross reference for 2
  sounds good").
- **Seattle's `HEADER QUARTER` rows: "keep, use head-office rule".** Both
  location types are kept, and Taipei's and Taichung's head-office rule
  applies to headquarters rows. It flags 9 rows.
- **Bellevue: King County food plus the cutoff.** The owner's reply
  ("makes more sense now check") was read back. The owner chose Bellevue's
  food from King County's inspections, current by construction, and the
  2010 issue-date cutoff for Bellevue's retail and personal services only.
  Before 2010, only 42% of Bellevue's food rows had a currently inspected
  business at their address.

### 2026-10-02 - Seattle (Regional): the Liquor Board's lists PERMITTED WITH CONDITIONS; non-commercial holds for a portfolio project (owner)

- **The `licence-read` verdict (2026-10-02): PERMITTED WITH CONDITIONS.**
  - The Washington State Liquor and Cannabis Board publishes no licence and
    no terms of use, and the list file (`Off Premise09292026.xlsx`, 8,795
    rows) carries none.
  - The only rule on reuse is the lists page's note: "Per RCW 42.56.070(8),
    records received through the Public Records Act may not be used for
    commercial purposes." The statute itself restricts the agency's
    disclosure of "lists of individuals".
  - The published layer drops `Licensee`, phone and mailing columns, so it
    shows trade names at premises.
  - No wording is prescribed and nothing is owed. The removal contact is
    publicrecords@lcb.wa.gov.
- **The owner's calls:**
  1. **"yes non-commercial"**: a free map in a personal portfolio, with
     nothing sold, no ads, no paid tier and no client use, meets the
     condition. The agent's lean was the same: MRSC's summary of SEIU 925
     treats publicizing one's work as too remote to be commercial. The same
     condition covers Seattle's own register.
  2. **"yes"**: the city page discloses the Board's notice that its list
     reports "contain possible errors due to a known data transfer issue",
     if it is still on the lists page at build. The page also states the
     list's date and never calls it complete, accurate or current (the
     privacy policy's accuracy disclaimer).

### 2026-10-02 - UK six briefs corrected from the UK lead's report

- **The UK lead's report, after Manchester's build on page 156:**
  - **CRS.** Every brief said "EPSG:27700, as London". London's, Glasgow's
    and Newcastle's `CRS_PROJECTED` is UTM 30N (EPSG:32630). EPSG:27700 is
    only Code-Point Open's source CRS. Corrected in all six, together with
    each CRS check's claim text.
  - **Metrolink.** TfGM's network map now names nine colour lines, and five
    have no OSM relation since the 14 September change. Manchester's brief
    is marked corrected and points to `docs/decisions_drafts/uk-six.md`.
  - **NaPTAN** files every tram stop under ATCO area 940. Added to all six.
- **Each brief's region line** now names the UK region and the minor tier
  (owner, 2026-10-02), which superseded "Europe".
- **Numbers.** The UK six hold notices 84–96, so the Japan batch starts at
  97 or later. Pages: UK 156–161, Japan 162–173.

### 2026-10-02 - The Japan batch released to one build session with agents; page numbers pre-assigned (owner)

- **The owner: "yes, write the kit, worktree and prompt"**, after staging's
  call: one Japan session with agents, beside the UK session.
  - All twelve go through `japan_register` and `japan_eigyo`, so a second
    Japan session would edit the same module.
  - The UK and Japan batches share almost no code, and each session gets
    its own Overpass slot.
- **The shape:**
  - Phase 0 is setup.
  - Phase 1: every brief's shared-code item in one pass, proven on the
    Minato control and the eight built cities.
  - Phase 2: Matsuyama as the pilot.
  - Phase 3: three agents by shape (MHLW-led four; city lists with personal
    services, four; one-bucket pages, three). They own only their cities'
    files and never query Overpass, commit or edit shared code.
  - Phase 4: integration, then the Japan sub-region and the minor-tier
    pass.
- **Page numbers are pre-assigned** so the two batches cannot take the same
  "next free" number: UK 156–161, Japan 162–173. Recorded in
  `docs/session_roles.md` and both kits.
- **Set up:**
  - `.claude/worktrees/japan-batch` on `japan-batch-build`, with the
    `data/` and `.venv-lean` junctions and no upstream;
  - the kit `docs/handoff_japan_batch_2026-10-02.md`;
  - the prompt, given in chat.

### 2026-10-02 - Twelve Japanese briefs written; the owner's calls on Matsuyama, Okayama, Sakai, Hakodate and Nagasaki (owner)

- **The owner: "start the japan briefs, 12 as one batch okay".** There are
  four agents with three cities each, every one writing only its own brief
  files. None queried Overpass, edited shared code or committed. All 12
  briefs are in `docs/build_briefs/`. Staging re-ran every check: 122 of 122
  claims hold (http, CKAN and UTM only).
- **The owner's calls ("approve all recommendations", then "nagasaki b,
  download ok"):**
  - **Matsuyama:** MHLW is a second source. Its own points go where the
    block join misses (81.9% to 92.7%), and its notifications become a
    partial food-retail bucket, disclosed (Fukuoka and Hiroshima).
  - **Okayama:** with MHLW as its only source, the name rule cannot run. The
    precedent extends: Hiroshima's MHLW bullet covers the whole page.
  - **Sakai:**
    - The Midōsuji Line is drawn cut at the city line (3 stations, not 2).
    - The monthly new and closure files are covered by the page's
      open-data notice (Hiroshima's precedent).
  - **Hakodate:** the e-Stat download was approved. The FY2024 counts total
    1,122 against the excerpt's 1,100 (98.0%), so 抜粋 means columns, not
    rows.
  - **Nagasaki: (b)**, the 2023 BODIK snapshot plus MHLW's current filings
    (Tokyo's precedent). One agent downloaded the city's current list, which
    needs the city's permission, to measure it only. The owner approved that
    after the fact. It is not a source.
- **Master-list corrections from the briefs (2026-10-02):**
  - Matsuyama's and Nagasaki's coordinate columns are empty.
  - Nagasaki's lists date from 2023-06-30 and 2023-03-31; 2025-03 is the
    upload. Its tram has 38 stops.
  - Kōchi has 1,415 premises (barbers 321 were missing).
  - Toyama's tram has 39 stops with the Port line.
  - Fukui's Fukubu Line has 15 stations in the city.
  - Sakai has 15 Hankai stops.
  - No band changes.
- **Build-time shared-code items, listed in each brief:**
  - column spellings for `japan_register` (address, name, operator);
  - Sakai's 1丁 rule;
  - Fukui's 飲食店 / 喫茶店 old-law types (93 rows);
  - Kagoshima and Fukui on the 2025 N02 edition.

  Each is followed by the Minato control.
- **Slips, logged as before:** two agents printed register rows to their
  consoles. One showed a shop name and address, plus two operator names; the
  other showed an operator's own name and phone number. Nothing reached a
  file. Separately, N03 boundary zips (the skill's own source) were saved
  under each city's `data/<slug>/raw/`.
- **Settled the same day (owner: "approve 1, approve 2 unless there is
  substantial JR, JR reads as metro"):**
  - Toyama's and Fukui's company-only operator names are accepted, as
    MHLW's rows were.
  - Each city's `mode` follows Dublin's precedent unless JR is substantial.
    Staging read "substantial" as JR being the city's largest network by
    stations inside the city line:
    - `metro`: Okayama (JR about 33 against Okaden's 16), Kitakyushu (JR
      about 28 against the monorail's 13) and Sakai (the Midōsuji);
    - `light_rail`: Utsunomiya;
    - `tram`: Matsuyama, Toyama, Kumamoto, Fukui, Nagasaki, Kagoshima,
      Hakodate and Kōchi.
  - Kagoshima is the nearest call: JR about 20 against the tram's 35.
  - Recorded in each brief and in the `japan-city` skill's standing calls.

### 2026-10-02 - The UK six released to one build session with agents; the UK takes the minor label tier (owner)

- **The owner released the builds:** "send off the uk six to either two
  separate sessions to build or one session using multiple agents",
  leaving the choice to staging ("whichever you think is more efficient").
- **Staging's choice: one lead session, with agents for five cities.**
  - Manchester pilots the shared code, so a second session would wait on
    the first.
  - All six write the same shared files: `cities.py`, the notices, What Is
    Excluded, the macro facts and the labels. A single integrator avoids
    merging the same lines five times.
  - Agents own only their city's files, never query Overpass (they share the
    session's one slot) and never commit. The lead integrates in build
    order.
- **The owner:** "implement the high-density cluster rule to UK, like
  Japan, France, Czechia".
  - The UK gets a region of its own, and every UK city moves into it.
  - The six (all tram or light rail) carry `label_tier: "minor"`, on
    France's line between metro and the rest.
  - London, Glasgow and Newcastle stay eligible.
  - `REGION_LABELS_ALSO["Europe"]` gains the region.
  - The region shape is decided by `check_macro_labels.py`.
  - Japan takes the same rule when its batch is built ("japan coming up,
    not currently implemented").
- **Set up:**
  - the worktree `.claude/worktrees/uk-six` on `uk-six-build`, with the
    `data/` and `.venv-lean` junctions;
  - a row in `docs/session_roles.md`;
  - the kit's new sections;
  - the session prompt, given in chat.

### 2026-10-02 - The UK six's prose hold lifted: page text to the new format (owner, via Cleanup)

- **The owner asked staging to message Cleanup about the new prose
  guidelines.** Cleanup confirmed that nothing pending keeps the hold. The
  builds stay held until the owner releases them.
- **The kit's prose hold is replaced** by a "Page text" section
  (`docs/handoff_uk_six_2026-10-01.md`). Each of the six briefs' banners and
  final bullets is replaced the same way. The pointers:
  - `docs/city_page_format.md`;
  - `add-city` step 8, then `scaffold-city`, `publish-city` (step 5a),
    `premises-taxonomy` step 8 and `read-licence` step 9;
  - `scaffold_city.py`'s template, which is the new format and is run for
    real.
- **Cleanup's corrections to the old hold:**
  - London's, Glasgow's and Newcastle's converted bullets are now the
    approved FSA and FHIS wording.
  - A city-specific sentence is a proposal, and does not stop the build.
  - The template pre-permission applies again.
  - What Is Excluded has a section per city, with its stations "listed on
    <City>'s page".
  - The OGL title, the FSA's and FHIS's business-type names and line and
    station names stay as published.
- **The Japan batch's minor-tier bullet stays where it is** (Cleanup, after
  its rework).
- **For the record (Cleanup):** city pages' maps are now centered on wide
  screens (`components.py`, 33f2a379, owner; rebooted and checked live).
  The builds have nothing to do; `render_city_title` applies it.

### 2026-10-02 - Takaoka's licence is CC BY 4.0, but its food list can no longer be reached; to Band R (owner)

- **The owner asked for a faster re-check by new methods** after the agent
  stalled ("go ahead with the takaoka"). It was run in the main session,
  with sites and executes permitted.
- **Licence: PERMITTED WITH CONDITIONS, CC BY 4.0.**
  - The old portal's dataset page (`opendata.pref.toyama.jp/dataset/syokuhin`,
    Wayback Machine 2026-05-21) gives the licence as 「クリエイティブ・コモンズ
    表示」. The creator is 生活衛生課, the list was last updated 2026-03-02,
    and the frequency is given as 月単位.
  - The portal's terms (Wayback Machine 2026-03-16) apply CC BY 4.0 to all
    content. The exceptions are logos and content marked with other rules,
    and the food list carries no such mark. The 出典 example is
    「出典：[データタイトル]富山県ホームページ（当該ページのURL）」, with
    「を加工して作成」 added for edited data.
  - The new platform's public front page (`ckan-front.tdcp.pref.toyama.jp`)
    says all its data is under CC BY 4.0, with credit.
  - The first screen's API read (2026-09-30) recorded `cc-by` on the
    barber, beauty-salon and laundry lists too.
  - The archive was read only because the old portal was retired: its host
    no longer resolves. Archived copies of the blocked platform were not
    looked for.
- **Access is the blocker now.**
  - The 2026-03-01 CSV on `toyama-pref.box.com` answers 404. It was read on
    2026-09-30.
  - The new platform's catalogue (`ckan.tdcp.pref.toyama.jp`) answers 403 to
    the built-in browser as well as to the fetchers, while its front page
    answers 200. The likeliest cause is a block on access from outside Japan.
    It was not worked around.
  - The national catalogue has ministry data only. A search found no other
    public link to the list.
- **Staging's recommendation is R, by the Kraków, Brescia, Catania and
  Alicante precedent** (portals that refuse the built-in browser). It would
  reopen when the platform answers or the prefecture publishes a public link.
- **Owner: "yes move takaoka to R"** (2026-10-02). The list holds
  A 7 · B 12 · C 1 · D 0 · R 24 = 44 candidates, with 121 discards.

### 2026-10-02 - The Japan batch goes to the minor label tier, as France and Czechia did (owner)

- **The owner:** "for this new batch of japanese cities, carry over an item
  to eventual build session that these need to be implemented like france
  and czechia where the smallest cities lose their macro-view pills to
  reduce clutter".
- **The batch:**
  - Band A's seven: Matsuyama, Toyama, Kumamoto, Fukui, Nagasaki,
    Utsunomiya, Kitakyushu.
  - Band B's five: Sakai, Hakodate, Kagoshima, Okayama, Kōchi.
  - Takaoka, if it leaves R.
  - Each carries `label_tier: "minor"`. The eight built Japanese cities stay
    eligible.
- **The precedent is the whole France and Czechia mechanism, not the tag
  alone.** The tag removes a pill only outside the city's own region, and
  every Japanese city is tagged East Asia today. So:
  - a Japan sub-region, one or split, measured by `check_macro_labels.py`;
  - every Japanese city moved into it, as Prague moved with Czechia;
  - `REGION_LABELS_ALSO["East Asia"]` gains it, so the anchors keep their
    pills there (Seoul's case).
- **Recorded for the build session** in the `japan-city` skill's standing
  calls and in the master list's "Before building". Nothing in `app/`
  changes now: it lands with the batch's first city at review time.

### 2026-10-01 - Brisbane to the discards on rail; a commuter-rail revisit group of twelve (owner)

- **The owner: "stays in discard, create commuter rail discard group to
  revisit (considering they are fully buildable)".**
- **Brisbane's only rail is Citytrain.**
  - **Spacing passes:** 83 stations in the city, median gap 1,012 m.
  - **Frequency fails:** 30 minutes off-peak on every line under the 2026
    reduced timetable. The normal one is at best 15 minutes, on five trunk
    sections, weekdays 7am–7pm.
- **The owner asked whether Buffalo's precedent applies. It does not.**
  - Buffalo's slower timetable was disclosed because its track is
    purpose-built.
  - On railway track the frequency gate holds: Aarhus L1, and Sheffield's
    Tram-Train the same week.
  - Commuter rail must also run at metro frequency to be drawn.
- **Brisbane's discard row:** kind `rail`, reopening when Cross River Rail
  opens (2029). The Council's food permits (8,050, CC BY 4.0) are recorded
  on it.
- **New section, "Commuter-rail revisit group"**, after the discard table
  (a view, not a band). It holds twelve discards whose only blocker is
  commuter or suburban rail and whose business leg is buildable:
  - Brisbane;
  - Tainan and Hsinchu (TRA locals);
  - Austin (the Red Line) and Fort Worth (TEXRail), both on the
    Comptroller file;
  - Cork (Luas Cork pending);
  - Teresina, Maceió, João Pessoa and Natal (CBTU suburban);
  - Sobral and Juazeiro do Norte / Crato (diesel VLTs on railway).
- **Left out of the group, because their blocker is not commuter rail:**
  - Cincinnati (a streetcar, food only);
  - Brampton and Bologna (lines not yet open);
  - the guided buses (Clermont-Ferrand, Padua, Venice-Mestre);
  - the one-to-three-station cases (Longueuil, Brossard, Vaughan,
    Berkeley, Saint-Louis);
  - Trondheim and Aubagne (reach and size);
  - Bogotá (BRT);
  - Jaén (no register).
- **The list now holds A 7 · B 12 · C 2 · D 0 · R 23 = 44 candidates, with
  121 discards.** The count, evidence, self-test and provenance checks pass.

### 2026-10-01 - Tempe to the discards: its licence list has no address (owner)

- **The owner: "save evidence, delete root, discard".**
- **The evidence is saved** at
  `data/tempe/raw/Tempe_General_Business_License_List_2026-09-03.pdf`
  (gitignored, so local and never committed). It is byte-identical to the
  owner's browser download.
- **The owner's root copy is deleted** (`expanded-heatmap/tempe.pdf`, at
  the main checkout's root).
- **Tempe moves from Band D to the discards**, a `measured` row. The list
  carries licence number, business name, business activity and website,
  and no address, so nothing can be placed. The City's ArcGIS app covers
  short-term rentals and tobacco only. It would reopen with a list that has
  premises addresses.
- **Band D is empty.** The list now holds **A 7 · B 12 · C 3 · D 0 · R 23 =
  45 candidates, with 120 discards.** The count, discard-evidence and
  self-test checks pass.

### 2026-10-01 - Fukui takes the CC BY-SA 4.0 offer (owner); Tempe's licence list has no address

- **Fukui (owner: "use the SA 4.0").** The current lists are used: food,
  2026-08, with closures; and 理容/美容/クリーニング. The site default is
  CC BY-SA.
- **What the Fukui build owes:**
  - **The share-alike offer itself:** a line in `LICENSE` and in the
    data-sources entry, offering `outputs/fukui/` (the map and any derived
    Fukui data) under CC BY-SA 4.0. It is the project's first share-alike
    licence on its own output.
  - **The credit:** 福井市, the list titles and page URLs, CC BY-SA (with no
    version claimed for the city's licence), and a statement that the data
    was processed.
  - **What never appears:** no endorsement, no claim of accuracy on the
    city's authority.
  - **The site policy's open-ended prohibited acts (§4) are accepted
    knowingly**, Taoyuan's pattern.
  - **Privacy:** `check_personal_exposure.py` covers the policy's privacy
    clause (6).
- **Tempe's General Business License List was read.**
  - The owner fetched it in their browser (`tempe.pdf`, at the main
    checkout's root). Staging copied it to its scratchpad.
  - It is a 33-page PDF, as of 2026-09-03, with four columns: licence
    number, business name, business activity and website. **There is no
    address**, so nothing can be placed (Denver's original failure).
  - The City's ArcGIS app covers short-term rentals and tobacco only.
  - **Staging recommends the discards on a measured negative**, the owner
    to confirm. The row stays in Band D until then.

### 2026-10-01 - Seattle regional: the Liquor Board's off-premise licences become a partial retail layer (owner)

- **The owner said "yes"** to staging's recommendation.
- **The layer:** the active off-premise rows (grocery stores, spirits
  retailers, beer/wine and wine shops) become a partial retail layer in
  every city outside Seattle and Bellevue. They are disclosed as shops
  licensed to sell alcohol only (Zurich's precedent).
- **On premise** is a check on the Snohomish food layer, not a layer.
- **Recorded in `docs/build_briefs/seattle.md`**, "What the build has to
  pull", items 4–7.

### 2026-10-01 - Seattle regional: the 2025 Snohomish layer approved for Lynnwood and Mountlake Terrace food (owner, 4a); the Liquor Board lists screened (4b)

- **4a approved (owner: "use").** Lynnwood's and Mountlake Terrace's food
  comes from Snohomish County's "Food Service Establishments (2025)" layer
  (598 and 92 points), under the currency rule's "a frozen part may sit
  beside a current whole, its date on the page" (Tokyo's precedent).
  Conditional on two build-time checks:
  - **It is a complete snapshot.** Check it against the county's published
    count of permitted establishments, and against the Liquor Board's
    on-premise rows (Lynnwood 113, Mountlake Terrace 24).
  - **Its date comes from more than the catalogue's "(2025)" label.**

  If it proves partial, those stations are drawn hollow.
- **4b probing (owner: "ok to fetch and screen")**: the Washington Liquor
  and Cannabis Board's Off Premise and On Premise lists, dated 2026-09-29,
  1.5 and 1.9 MB, kept in the staging scratchpad.
  - **Off premise:** 8,793 rows statewide (7,791 active), mostly grocery
    stores (beer/wine), spirits retailers, beer/wine specialty shops and
    wine resellers.
  - **On premise:** 9,993 rows (9,511 active), mostly restaurants, lounges,
    taverns and nightclubs.
  - **Both** carry status, expiry, a premises address and city (no
    coordinates), plus `Licensee`, phone and mailing columns that are never
    published.
  - **Terms:** the page says records "may not be used for commercial
    purposes" (RCW 42.56.070(8)), which the owner's non-commercial
    confirmation meets. A formal licence read is owed at build.
- **The finding: a partial retail layer exists in every suburb**: shops
  licensed to sell alcohol, in both counties (Lynnwood 133, Kent 134,
  Federal Way 106, Shoreline 66, Redmond 64, Tukwila 48, SeaTac 40,
  Mountlake Terrace 25, Des Moines 24, Mercer Island 16, all statuses).
  That is Zurich's precedent: alcohol-licensed shops as a partial layer
  beside a full food register, disclosed.
- **Staging recommends** adding the active off-premise rows as that partial
  layer, and using on-premise only as a check on the Snohomish layer.
  **The owner's call is pending.**
- **Personal services remain unpublished outside Seattle and Bellevue**,
  disclosed per city (4b).

### 2026-10-01 - Five licence reads: Seattle and Geostat permitted; Bellevue and King County ambiguous and read as permitted (owner, option 1); Fukui's share-alike to the owner

- **Seattle's business register: PERMITTED WITH CONDITIONS.**
  - The layer is federated on data.seattle.gov (`wmtg-dzy4`). Its Open Data
    Terms of Use ("by using data made available through this site the user
    agrees…") and Open Data Policy V1.0 support reuse.
  - No attribution is required, and nothing is owed.
  - The condition: data configurable as "a list of individuals" may not be
    used "for a commercial purpose". The owner confirmed the project is
    non-commercial ("no commercial, nothing sold", 2026-10-01), and it must
    stay so.
- **Bellevue's licences (all): ambiguous.**
  - The data's licence field bars only commercial use or sale without
    written authorization.
  - The portal's linked Terms of Use allow only "own personal,
    non-commercial use", with all other rights reserved.
- **King County food inspections: ambiguous.**
  - The Socrata dataset is declared Public Domain. The portal's own data
    terms granted reuse, but they are now a 404 (last archived 2023).
  - The live site-wide terms forbid publishing without written permission.
- **The owner chose option 1 for both, "defensible": read as permitted.**
  - The data's own declarations govern.
  - King County: display "Public Health – Seattle & King County" and the
    legend "Data provided by permission of King County"; no marks, no
    implied endorsement; no USPS-derived fields (`CTYNAME`,
    `POSTALCTYNAME`, ZIP+4) from the address points.
  - Bellevue: credit the City of Bellevue.
  - The removal rule is the safety net for both.
  - The owner also noted a **separate Seattle-only build already exists**.
- **Geostat's Business Register: PERMITTED WITH CONDITIONS.**
  - The terms allow any use "without prior permission". The condition is
    to name Geostat as the source, which the statistics law also requires
    (Art. 43(6)). No logo.
  - Two points stand, neither a prohibition:
    - statistical confidentiality: public-registry data is exempt under
      Art. 34(4);
    - Georgia's personal-data law: processing public data is lawful, and a
      restriction request is honoured, as the removal rule already does.
  - Tbilisi needs `add-country` for Georgia next.
- **Fukui's site-default CC BY-SA: PERMITTED WITH CONDITIONS.**
  - Share-alike would oblige offering `outputs/fukui/` under CC BY-SA 4.0
    (in `LICENSE`), the project's first share-alike licence on its own
    output.
  - The personal-services lists exist only under BY-SA, so only a food-only
    page on the older CC BY copy avoids it.
  - **The owner's call.**
- **Recorded in `docs/build_briefs/seattle.md`** ("What the build has to
  pull") and on the master list's Seattle, Tbilisi and Fukui rows.

### 2026-10-01 - The owner's calls 5-10: downloads approved, NaPTAN for the UK six, Dudley pre-approved, Atlanta's note filed, Richmond to R (owner)

- **5. Downloads approved:**
  - **Tempe's business licence list**: staging fetches and screens it.
  - **Burnaby's licence layer and Arlington's licence list**: for main's
    Vancouver (Regional) and D.C. + Arlington add-on builds. Recorded in the
    master list's add-ons note.
- **6. NaPTAN** (the Department for Transport's stop register, OGL) is gate
  3's independent source in all six UK briefs. It is the only one for
  Sheffield and Blackpool, whose operators refuse scripts. It needs a
  licence row and its notice at build.
- **7. Birmingham:** if West Midlands Metro's Line 2 is in passenger service
  at build, **Dudley (FSA 409) joins as a fourth authority**, pre-approved.
  It is written into the brief and the handoff.
- **8. Atlanta:** a note telling the City its 2024 licence layer exposes
  reported revenue is **drafted and filed, not to be sent**
  (`docs/notifications/atlanta-revenue-exposure.md`). The owner: "unlikely
  to send". It quotes no revenue value.
- **9. Dublin's vacant premises and the three undatable sources** (NYS food
  stores, Milan, Surrey): "disclose the lack of info where we need".
  - That is page text, so under the prose hold it goes to the prose pass,
    not to staging.
  - Cleanup was told the same day.
- **10. Richmond (BC) is in Band R, request only** (owner: "is request
  required? if so put into R").
  - It is: the City's business directory carries no open-data licence, and
    its copyright notice allows "research purposes and private use only",
    with written permission required.
  - The request (`buslic@richmond.ca`) is the owner's to send. Nothing is
    drafted.
  - **The list now holds A 7 · B 12 · C 3 · D 1 · R 23 = 46.**
- **Approved to run, and started the same day:**
  - licence reads of Seattle's register, King County's food inspections,
    Bellevue's licences and Geostat's register (plus Fukui's, from call 2);
  - the four UK brief re-runs that printed RETRY;
  - Brisbane's commuter-rail test;
  - a re-check of Takaoka's licence page.

### 2026-10-01 - The owner's calls on the fresh list: discards confirmed, Tbilisi to B, Fukui and Seattle conditional (owner)

- **1. The 19 new discards are confirmed** (owner: "confirm all"). The
  master list's notes now read "confirmed by the owner the same day".
- **2. Fukui uses the current CC BY-SA list, if a licence read clears
  share-alike for the map.** Otherwise it uses the older CC BY 2.1 JP copy.
  The `licence-read` agent was started the same day.
- **3. Tbilisi moves from C to B.**
  - The owner accepts Geostat's business register as the source, with the
    undercount disclosed: it lists enterprises, not premises, so a chain
    appears once.
  - Individual entrepreneurs are shown as **unnamed dots, category only**,
    on Taichung's precedent.
  - Personal ID columns are dropped at fetch.
  - The next steps are a licence read of Geostat's terms and `add-country`
    for Georgia.
- **4b. Seattle's retail and personal services outside Seattle and
  Bellevue** are accepted as unpublished and disclosed per city, **if
  further probing finds no further bucket**.
- **4c. Bellevue's never-expiring licences** get an issue-date cutoff,
  measured at build and brought to the owner.
- **4a is still open.** The owner asked whether the 2025 Snohomish layer is
  acceptable with its currency disclosed. Staging's answer: yes, under the
  rule "a frozen part may sit beside a current whole, its date on the page"
  (Tokyo's precedent), provided two things measure true at build:
  - it is a complete snapshot, checked against the county's published
    count of permitted establishments;
  - its date comes from more than the catalogue's "(2025)" label.

  The owner's yes is pending.
- **The list now holds A 7 · B 12 · C 3 · D 1 · R 22 = 45, with 119
  discards.** The count, discard and provenance checks pass.

### 2026-10-01 - The UK six briefed, with a prose hold; builds held (owner)

- **The owner (2026-10-01)**: "no, I want to wait on builds. generate the
  briefs now". And: "have the sessions wait on drafting prose. I'm currently
  in the middle of reworking site prose and want that to complete before
  these builds resort to generating the old prose."
- **Six briefs** are in `docs/build_briefs/`: `manchester.md`,
  `birmingham.md`, `edinburgh.md`, `sheffield.md`, `nottingham.md` and
  `blackpool.md`. **The handoff** is `docs/handoff_uk_six_2026-10-01.md`.
- **Every brief and the handoff open with the prose hold.**
  - Draft no page text: no description, scope sentence, What Is Excluded
    entries, notice wording beyond the licensor's attribution, or
    README/Overview copy.
  - Do not copy London's, Glasgow's or Newcastle's page text.
  - Leave `TODO(prose-hold)` markers and do not scaffold `app/pages` text.
  - The 2026-09-30 approved-template pre-permission is suspended for this
    round.
- **Measured for the briefs, 2026-10-01**: FSA per-authority counts and
  file sizes (HEAD); one Overpass query per city, run in sequence (tram
  relations, stop names, council boundaries with GSS codes); and which
  operator pages answer scripts.
- **Each brief carries the checks the tram kit's retrospective said
  briefs lacked**:
  - every authority's FSA file is listed;
  - the FHRS terms still name the OGL;
  - the operator's own stop list, where it answers scripts (TfGM, West
    Midlands Metro, Edinburgh Trams, NET);
  - OSM relations and refs;
  - the CRS fallback.
- **Found while briefing:**
  - **Nottingham (Regional) is 3,702 storefronts, not 4,723**, an addition
    error at the screen. The master list and the approval entry above are
    corrected.
  - **West Midlands Metro's Line 2 (Wednesbury–Dudley) is in OSM**, its
    stops marked "[Aug 2026]". Whether it is open is a Step 0 check, and
    adding Dudley is the owner's call.
  - **Sheffield's and Blackpool's operator sites refuse scripts** (a
    Radware CAPTCHA; 403). Gate 3's proposed source is NaPTAN (DfT, OGL),
    a new source that needs the owner's OK.
  - **Blackpool:** select Wyre (207), not Wyre Forest (153).
  - **Nottingham:** the city is a unitary authority at admin_level 6 beside
    three admin_level 8 districts. Union the four, never the county.
  - **Colours:** Sheffield's Yellow (`#FFFF00`) will need darkening. NET's
    two lines share one colour. Blackpool and Edinburgh carry none in OSM.

### 2026-10-01 - The UK six approved with their scopes: four regional pages, two city pages (owner)

- **The owner: "yes to the set"**, on staging's recommendations. All six
  are food-only pages on the FSA register, London's filter and Glasgow's
  privacy rules.

  | # | Page | Scope | Storefronts | Why |
  |---|---|---|---|---|
  | 1 | **Manchester (Regional)** | the 7 Metrolink districts | 12,451 | Manchester alone holds 42 of 99 stops, a stub |
  | 2 | **Birmingham (Regional)** | Birmingham, Sandwell and Wolverhampton, built now | 9,827 | Birmingham alone holds 16 of 35 stops |
  | 3 | **Edinburgh** | the city | 3,933 | Every stop is inside it |
  | 4 | **Sheffield** | the city, without the Rotherham Tram-Train | 3,447 | The Tram-Train runs every 30 minutes on converted railway (Aarhus L1's precedent); food first, the city's rates list a later screen |
  | 5 | **Nottingham (Regional)** | the city, Broxtowe, Rushcliffe and Ashfield | 3,702 (first written 4,723, an addition error; corrected the same day) | Beeston's 9 stops and the line ends draw filled rings |
  | 6 | **Blackpool (Regional)** | Blackpool and Wyre | 1,744 | Keeps Cleveleys and Fleetwood, the terminus |

- **The Dudley branch** (West Midlands Metro, about late 2026) becomes a
  dated watch item, not a reason to wait.
- **The build order is largest first**, so the first city pilots the shared
  code and the rest become configs.
- **Recorded in the master list's Band B** (the rows reordered, two renamed
  "(Regional)"). `check_master_list_counts.py` passes.

### 2026-10-01 - MHLW's food file counted for five Japanese cities: Utsunomiya and Kitakyushu to A; Kagoshima, Okayama and Kōchi to B (owner approved the downloads)

- **The owner approved the five downloads (2026-10-01).** Each is from
  `i2fas.mhlw.go.jp` (PDL 1.0, read for Fukuoka), 2.9–7.2 MB, and is kept
  in the staging scratchpad, never in the repo.
- **MHLW's file carries 85–91% of each city's restaurant permits in force.**
  - The rows are permits from 2021-06 on, all 許可.
  - Each city appears to enter every new permit there, not only the online
    filings.
  - The counts are open 飲食店営業 rows against the FY2024 in-force count.

  | City | Open permits | In force | Share | With an address |
  |---|---|---|---|---|
  | Utsunomiya | 4,901 | 5,761 | 85% | 99% |
  | Kitakyushu | 10,760 | 12,733 | 85% | 86% |
  | Kagoshima | 5,914 | 6,823 | 87% | 76% |
  | Okayama | 7,582 | 8,409 | 90% | 74% |
  | Kōchi | 4,564 | 4,999 | 91% | 54% |

  MHLW publishes an address only by consent (Fukuoka's precedent).
- **The verdicts**, on the reduced-bucket bar's placement rule (about 70%):
  - **Utsunomiya to A.** Food plus the CC BY personal-services lists.
  - **Kitakyushu to A.** Personal services have no laundry list, which is
    disclosed.
  - **Kagoshima to B, food only.** Its personal lists are a new-openings
    stream.
  - **Okayama to B, food only.** Its personal lists need the city's
    permission.
  - **Kōchi to B, personal services only.** Its food places 54%, under the
    bar.
- **The list now holds A 7 · B 11 · C 4 · D 1 · R 22 = 45.**
  `check_master_list_counts.py` passes.
- **No row values were printed.** The counting script printed counts,
  column names and years only.

### 2026-10-01 - The master list rebuilt fresh: 45 candidates from the post-review screens; Band R and the discards carried over (owner)

- **The owner's ask (2026-10-01)**: run the Job 2 probes, then "generate a
  fully fresh master list", since the review had emptied the old one, and
  carry over Band R and the discards.
- **The old list is archived word for word** at
  `docs/city_master_list_2026-09-30.md`. The new one carries these over
  verbatim:
  - the Built table (124);
  - Band R, with four new rows;
  - the discards, with a new table of 19 rows;
  - Countries ruled out, the Five rules, and Before building.
- **New: A 5 · B 8 · C 9 · D 1 · R 22 = 45 candidates; 119 discards.**
  - **A:** Matsuyama, Toyama, Kumamoto, Fukui, Nagasaki.
  - **B:**
    - the UK six, food only on the FSA register: Manchester (Regional),
      Birmingham (Regional), Sheffield, Nottingham, Edinburgh, Blackpool;
    - Sakai, food only;
    - Hakodate, personal services only.
  - **C:**
    - Seattle (Regional);
    - five Japanese cities hinging on one count of MHLW's file:
      Utsunomiya, Kitakyushu, Kagoshima, Kōchi, Okayama;
    - Takaoka (its licence);
    - Tbilisi (enterprise rows and individual entrepreneurs);
    - Brisbane (found in passing; the commuter-rail test).
  - **D:** Tempe (one download to approve).
  - **R:** the 18 carried, plus Kraków, Brescia, Catania and Alicante, whose
    portals refuse the built-in browser too.
- **The 19 new discards are staging's recommendations, for the owner to
  confirm**:
  - Toyohashi;
  - Dresden, Leipzig, Graz, Luxembourg City, Wrocław, Adelaide, the Gold
    Coast, Canberra;
  - Belgrade, Sarajevo, Santo Domingo, Casablanca, Rabat–Salé, Tunis, Lagos,
    Addis Ababa;
  - Cagliari, Alcobendas.

  Each row passes `check_discard_evidence.py`.
- **Band T is retired, not deleted.** Its section stays at 0 and names the
  tram list. That keeps `check_master_list_counts.py` reading the tram
  list's counts, and keeps the self-test's tram cases live: 24 of 24.
- **Japan's Kōchi is spelled with its macron.** "Kochi" is already a discard
  row: India's, in Kerala. The count check caught the collision.
- **The per-city screens behind each row** are in this session's report to
  the owner, and in the subagent notes in the staging scratchpad. The Seattle
  regional screen is in `docs/build_briefs/seattle.md`.

### 2026-10-01 - Probe slips during the post-review screens: one Overpass query, three console prints of personal data

- **One Overpass query beyond the session's own.**
  - The UK screen's agent ran `brief_check.py newcastle`, whose
    `osm_route_refs` claim queries Overpass. It passed 4/4.
  - Staging's own Link query had finished, so only one query was ever in
    flight.
  - Lesson: a screening agent's rules should name `brief_check.py` as an
    Overpass client.
- **Personal data printed to agents' consoles; nothing was saved or
  repeated:**
  - the UK screen's group-by on Birmingham's Gambling Act register printed
    licence holders' names and addresses;
  - the pattern screen's group-by on ACT's licence table printed its
    `Licensees` column;
  - a Japan helper's header reader printed one Toyama row (a business name
    and address).
- **Band B's retrospective lesson stands**: select columns before printing
  anything from a register with personal columns. The screening prompts
  said so, and the slips came from group-bys on a column the agent had not
  inspected first.
- **A looping REPL from the north-end Seattle agent** left about 290 MB of
  error output in this session's temp folders. Its process is stopped. The
  files are left for the owner to clear.

### 2026-10-01 - Seattle's regional screen: 37 stations in 11 cities; only Seattle and Bellevue publish all three buckets (owner's scope)

- **The owner (2026-10-01)**: Seattle stays held for a regional build with
  multiple city registers. Research every city along the 1 and 2 Lines.
- **Stations (OSM, one query)**: 37 stations in 11 cities.
  - Seattle 17, Bellevue 6, Redmond 4, Shoreline 2, SeaTac 2, Kent 2, and
    one each in Lynnwood, Mountlake Terrace, Tukwila, Federal Way and
    Mercer Island.
  - The cross-lake 2 Line opened 2026-03-28.
  - The rings also reach Des Moines (42% of Kent Des Moines' ring) and
    unincorporated King County.
- **What is published**:
  - Seattle and Bellevue each have their own register with all buckets.
  - Redmond's layer is frozen at about 2020, and Federal Way's is a 2024
    shopping-centre extract.
  - Nothing is published for Shoreline, Kent, Des Moines, Tukwila, SeaTac,
    Mercer Island, Lynnwood or Mountlake Terrace.
- **Food everywhere in King County**: Public Health – Seattle & King
  County's inspections (12,296 businesses, parcel-joinable). Its licence
  conflicts between the two published copies.
- **Snohomish food fails currency**: the only layer is a 2025 snapshot with
  no dates.
- **Retail and personal services outside Seattle and Bellevue**: only by
  public-records requests. That is outreach, the owner's last resort.
- **Recorded in full** in `docs/build_briefs/seattle.md`, "The regional
  screen". Seattle sits in Band C of the fresh list.
