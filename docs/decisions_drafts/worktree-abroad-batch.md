# DECISIONS drafts - Abroad batch (`worktree-abroad-batch`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

## Parked calls

Numbered for Staging's wave list; each with a recommendation and its
tradeoff. A parked call stops only what it names.

**The owner's answers (2026-10-07, relayed by Staging as its calls
191-195):**
- **Call 1 (Bremen's CC BY version):** "191, download approved": fetch the
  Kommunalverbund's 2024 report PDF (3,643,392 bytes) from the publisher's
  own host and read it for the licence terms only. Confirmed by the owner in
  the build's own chat ("yes", 2026-10-07) and read the same day
  (`pdftotext`; 3,643,667 bytes from kommunalverbund.de, 124 pages, kept
  in the session scratchpad only): **it names no licence, no CC version and
  no reuse terms.** Its imprint gives the rights chain: the Kommunalverbund
  commissioned the 2022 survey (Auftraggeber), Dr. Acocella Stadt- und
  Regionalentwicklung GmbH carried it out (Auftragnehmer), and the
  Kommunalverbund is the publisher of the survey guideline (Herausgeber);
  its figures credit the contractor's own drawings. **So the version stays
  open and the call stays parked for the owner** (the owner's instruction:
  if the PDF names no version or says nothing on reuse, park it).
  **Answered (owner, 2026-10-07, in the build's chat: "accept the
  permissive reading"):** the unversioned CC BY is read as permitting the
  map, on the record's "Freie Nutzung" and opendata declaration and its
  link to the 4.0 terms; no outreach. Notice 156 stands as built; a
  removal request is honoured. Bremen lands at review time with the batch.
- **Call 3 (Nezahualcóyotl):** "continue drop, state on page": the 398 rows
  stay dropped; Mexico City (Regional)'s page now says so (a proposal
  sentence, for review time).
- **Call 4 (Gelsenkirchen U11):** "keep it tram mode". Done as built.
- **Call 5 (macro labels):** Europe East is made now, by Cleanup, with
  Thessaloniki; a Germany view only if Cleanup's measurement shows Europe
  West still overlapping, then on Czechia's and Belgium's mechanism. Not
  built here. Cleanup measured it on d278af3a: the split alone leaves the
  12 problems; the split plus a Germany view (Berlin, Gelsenkirchen,
  Bremen) with competition in both Europe halves reaches 0. Cleanup builds
  both on `europe-split`, landing right after this batch; this branch keeps
  the 12 `check_macro_labels.py` problems until then and leaves the region
  tables and the Dutch offsets alone.
- **Call 6 (Greece):** "yes", in Europe East with the split; Cleanup lands it.
- **Copenhagen (Regional):** waits for the owner to set the Datafordeler key
  or fetch the eight Adressepunkt files.

1. **Bremen: the unversioned CC BY and the database right.** The
   licence-read agent (2026-10-07) found the record's "Creative Commons
   Namensnennung (CC-BY)" unresolvable to a version: DCAT-AP.de's
   unversioned `cc-by` concept maps to no version, opendefinition.org lists
   1.0 to 4.0, and Bremen's own portal records use `cc-by/4.0`, so the
   unversioned id was a choice. Every version permits public display and
   adapted maps, no share-alike, no non-commercial term. The gap: CC BY 4.0
   licenses the sui generis database right (§4) and 3.0 is silent on it, so
   under an older reading the survey's German database right (§87a UrhG) is
   neither licensed nor reserved. The owner's call 13 (2026-10-05: "no
   outreach; the title as written, CC BY 4.0's notice terms met") already
   reads the licence as 4.0, but was made without the database-right point,
   so this asks only to confirm it. **Recommendation: accept, on the
   4.0 reading** (opendefinition's overview is 4.0 and it names 4.0 the only
   version for data; the record types the licence "Freie Nutzung"; the map
   publishes aggregated density and a goods group per dot, never the
   database). Tradeoff: if the Kommunalverbund meant 3.0, an objection
   arrives as a removal request, honoured at once; the alternative, asking
   info@kommunalverbund.de, delays Bremen and reverses call 13's
   no-outreach. Stops: Bremen's landing only; the build proceeds on the
   branch.
   **Investigated further on the owner's word (2026-10-07, "yes
   investigate"), pages only:** still unsettled, and the 4.0 reading is
   weaker. Of the Kommunalverbund's 12 GovData records, its 6 boundary
   datasets carry versioned `cc-by/4.0` (from 2019 on) and its 6 own
   planning and survey datasets, this one among them, the unversioned
   `cc-by` (as late as 2024): the publisher selects 4.0 where it means it.
   No DCAT-AP.de or GovData text defines the unversioned id as the newest
   version; Creative Commons' wiki: only 4.0 expressly licenses the sui
   generis right. MetaVer answered 429 twice. Unread, the publisher's own
   PDFs: the 2024 report (3,643,392 bytes) and the survey guideline (2,206,720
   bytes), both on kommunalverbund.de; a download needs the owner's yes.
   Options put to the owner: accept on the permissive reading; read the 2024
   report first; or the owner asks the Kommunalverbund (outreach, reversing
   call 13).
2. ✅ **Answered (owner, 2026-10-07: "keep as built unless personal info
   that is not trade name").** Kept; in those premises a person-shaped name
   now shows the street address whatever the legal form: 37 more names
   withheld (Sàrl 23, SA 11, SNC 2, a branch 1), 1,311 in all; the 131
   office-typed sole traders were already withheld. Was: **Geneva: the 326
   kept establishments typed Bureau/étude/cabinet** (the
   owner's call 3 of 2026-10-04 asked for the count by code at build). In
   the 12 communes, of 5,863 kept: beauty institutes 131, other physical
   well-being 41, hairdressers 25, car dealers 23, computer shops 11,
   watches and jewelry 10, art dealers 9, specialist food 8, and 68 more
   spread over 26 shop codes (none above 6). **Recommendation: keep them**
   (built so): every code is a storefront code, and the personal-services
   ones are mostly a beauty or hair practice in an office building, which
   takes walk-in clients; the page says a few office-typed establishments
   are counted. Tradeoff: some are back offices (a car dealer's
   administration, an online jeweller); out, the map reads 5,537 and
   Personal services loses 202 of 1,104. Stops: nothing; a "drop" answer
   is a one-line config change and a re-run.
3. **Mexico City (Regional): 398 Nezahualcóyotl storefronts outside OSM's
   boundary.** DENUE codes them to Nezahualcóyotl (all locality 0001), but
   they lie 14-823 m east of the municipio's OSM polygon, toward
   Chimalhuacán: a boundary disagreement, not misplaced points. Monterrey's
   polygon test is the precedent, but its 22 dropped rows were genuinely
   misplaced (some 550 km away). **Recommendation: keep dropping them
   (built so) and disclose it** (What Is Excluded says so). Tradeoff: no
   ring changes either way, since the cluster is 5,330 m from the nearest
   station (Peñón Viejo); kept, the total gains 398 and the in-ring share
   falls slightly. Stops: nothing; keeping them is a code-scope change to
   step 2 and a re-run.
4. **Gelsenkirchen's `mode`: U11 is OSM `route=subway`, not light rail.**
   Call 18 kept `tram` "if OSM types U11 light rail"; OSM types it subway.
   **Recommendation: keep `tram`** (built so) on the same principle the
   call rests on (a second mode sets `mode` only where it is the city's main
   network): U11 has 3 of the city's 60 stops, 1 of them its alone.
   Tradeoff: the macro dot's color understates one short Stadtbahn end.
   Stops: nothing; asks only to confirm the call reaches subway.
5. **Macro labels: Gelsenkirchen and Bremen do not clear in Europe's
   view.** The best of ten offsets each (Gelsenkirchen right of its dot,
   Bremen upper right) leave 4 problems at each width (12):
   Rotterdam's pill covers Bremen's marker, Den Haag's covers
   Gelsenkirchen's, and Berlin x Bremen and Den Haag x Gelsenkirchen
   overlap. Rotterdam's and Den Haag's own offsets made no difference
   (their Europe positions come from per-region overrides), and a minor
   tier would not help (their region is Europe itself). **Recommendation: a
   Germany view on Czechia's and Belgium's mechanism** (Berlin, Gelsenkirchen
   and Bremen labelled there, dots only in Europe), or fold it into the
   Europe West/East split the owner approved on 2026-10-04. Tradeoff: a new
   view in the menu; the alternative, re-placing the Dutch and Berlin labels,
   moves four built labels for two new ones. Stops: `check_macro_labels.py`
   (so `check_all.py`) until decided; nothing else.

### 2026-10-07 - Gimpo built: the Gimpo Goldline on SEMAS's register, its own page (abroad-batch)

- **Privacy verdict: publish.** `check_personal_exposure.py gimpo`: PASS, 0
  of 13,398 rows show a Korean personal name at a residential address; 11
  withheld by step 2's Korean pass (9 of them inside a ring). SEMAS has no
  owner or phone column.
- **Gimpo built on SEMAS's register and the Gimpo Goldline, page 202.**
  Gimhae's pipeline (code-keyed register, one Overpass query) with Gimpo's
  config: 시군구코드 41570 picked 25,160 rows -> **13,398 storefronts**
  (Food service 6,112, Retail 5,512, Personal services 1,774), exactly the
  brief's screen; 11 personal names at a residential address withheld; out
  by name: hostess bars 139, staff canteens 44, household fuel dealers 10,
  dance halls 4. OSM boundary relation 2409165 (김포시), **295 km²**, gated
  285-305 (the brief's 277 is the land figure). The Goldline (ref
  `김포 골드라인`, light_rail, OSM's #957326, CIE76 62.9 from the nearest
  pin color) drawn to both ends: **9 stations in Gimpo**, 김포공항 (Seoul)
  in `excluded_stations.csv`. Gate 3 exact on the whole line, 10, against
  English Wikipedia's infobox (secondary, as Ansan and Uijeongbu). Median
  spacing 1,459 m (the brief 1,457), standard rings; the light-rail test
  passes (own underground track, every 6 minutes at midday per the brief's
  timetables, spacing above 550 m). **7,187 of 13,398 (53.6%) in a ring**
  (the brief's 53.4%). Not drawn, each with no station in Gimpo: Lines 3, 5,
  9 and Incheon Lines 1 and 2 (AREX and the Seohae Line are `route=train`
  and never queried). The tunnel share was not measured (the drawn geometry
  carries no tunnel tags); the light-rail test does not need it. Step 2
  measured 0.33 GB. Files: `pipeline/gimpo/`, `app/pages/202_Gimpo_Heatmap.py`,
  `app/cities.py`, notices 68 and 1, `docs/data_sources/south-korea.md`
  (three rows), `docs/excluded_categories.md`, `docs/privacy_verdicts.md`,
  `scripts/check_personal_exposure.py`.

### 2026-10-07 - Siheung built: Line 4, the Suin–Bundang and Seohae lines on SEMAS's register, its own page (abroad-batch)

- **Privacy verdict: publish.** `check_personal_exposure.py siheung`: PASS,
  0 of 15,206 rows show a Korean personal name at a residential address; 11
  withheld by step 2's Korean pass (4 of them inside a ring).
- **Siheung built on SEMAS's register and Ansan's three lines, page 300.**
  Ansan's step 1 with Gimhae's one-query fetch (Ansan's train-ref clause
  added) and code-keyed register: 시군구코드 41390 picked 25,119 rows ->
  **15,206 storefronts** (7,273 / 5,763 / 2,170), exactly the brief's; 11
  withheld; out by name: hostess bars 287, staff canteens 230, household
  fuel dealers 35, dance halls 5. OSM boundary relation 2409181 (시흥시),
  **166 km²** with its tidal flats, gated 158-174. **9 stations**: Line 4 2,
  Suin–Bundang 4, Seohae 5, 오이도 and 정왕 shared; 114 stations of the
  three lines outside, listed. Gate 3 exact on the Suin–Bundang Line, 63
  (Ansan's source); Line 4 and the Seohae Line not gated whole, as Ansan.
  English names: all 9 resolved from a station object or `name:en`
  (시흥능곡 and 달월 included), no override needed. Median spacing 1,332 m,
  standard rings. **6,106 of 15,206 (40.2%) in a ring** (the brief's 41.2%
  on the probe's points). Line colors are Ansan's: Seohae 29.9 and Line 4
  33.6 below the preferred 45, recorded, as in Ansan. Not drawn: Lines 1, 2,
  7 and Incheon Lines 1 and 2, none with a station in Siheung. Step 2
  measured 0.31-0.41 GB.

### 2026-10-07 - Geneva (Regional) built: TPG's five trams on the canton's business register (abroad-batch)

- **Privacy verdict: publish.** `check_personal_exposure.py geneva`: PASS,
  0 person-like names at a residential unit of 4,839 pins. Home-based
  premises are out by type. **The owner's sole-trader rule (call 2,
  2026-10-04) as built:** a sole trader's trade name is withheld, the street
  address shown, where it shares a word of three letters or more with the
  owner's registered name (function words and legal-form tails aside) or is
  person-shaped (`residence.looks_personal`); a name of unknown legal form
  (746 establishments whose firm sits outside the canton) only where it is
  person-shaped; and, on the owner's answer to parked call 2 (2026-10-07), a
  person-shaped name in office-typed premises whatever the legal form (37).
  1,130 of 1,490 sole traders' names withheld (974 share a word, 372
  person-shaped), 144 of unknown form, 37 office-typed: **1,311 in all**. A
  trade-word filter was measured and rejected: the most frequent words in
  sole traders' registered names are given names and surnames (marie,
  jean, silva), so a frequency filter would drop the very words the rule
  needs. The registered name is read in memory only and never written.
  The 682 person-shaped names left are incorporated firms' trade names
  (cafés, salons), commercial information (owner, 2026-10-03).
- **Geneva (Regional) built, page 301, slug `geneva`.** The canton's REG
  (SITG Level A; the cached zip of 04.10.2026, sha256 `45aff219...`):
  establishment rows only; 5,828 home-based, itinerant and market-stand
  rows dropped canton-wide (in the 12 communes, of storefront codes:
  itinerant 70, home 62, stands 22); NOGA 2008 through the new closed list
  `pipeline/taxonomies/geneva_noga.py` (71 kept codes, 15 out, each with
  its rule; Georgia's module applied to NOGA; traiteurs out on R1, owner
  call 3; car washes out as a vehicle service); scope by the 12 OSM commune
  polygons, which the register's `PHYS_COMMUNE` matches on every row.
  **5,863 storefronts** (Food service 1,862, Retail 2,897, Personal
  services 1,104), the brief's 5,885 less the 22 stands. Left out by code in
  scope: vehicle repair 212, other food service 192, the catch-all 112,
  body shops 83, caterers 63, mail order 57, and smaller. **1,847 company
  rows** with a storefront code and no establishment row left out and
  disclosed (call 1; the brief's 1,848). Step 2 measured 0.23 GB.
- **The trams.** One Overpass query (relations, stop nodes, tram stops,
  admin_level 8 communes). 10 relations, two per line, all kept. **OSM
  names many stop positions with TPG's platform letter** ("Bel-Air (A)",
  "(B)"), so the first collapse gave 102 stations and gate 3 failed on
  every line; osm_tram's aliases need the target spelling present, so
  step 1 strips a trailing platform letter for 14 listed stops
  (`config.PLATFORM_LETTER_STOPS`, stale-checked) before the collapse:
  **85 stops, gate 3 exact on all five lines** against TPG's own pages
  (25/30/22/26/31), **81 in the 12 communes** (the brief's figure), tram
  17's 4 in France listed. Median gap **330 m: halved rings.** TPG's colors
  as OSM tags them: tram 18 (26.5), 17 (33.9) and 14 (43.8) below the
  preferred 45, recorded (agency colors, owner 2026-09-21). **4,839 of
  5,863 (83%) in a ring.** No frequency sentence: no operator timetable
  was read.
- **Notice 154 (SITG)**: the CU 5.3.1 source line with the zip's date, a
  derived-use line on CU 5.3.2's example ("Cartographie réalisée sur la
  base de Données du Portail SITG"), the conditions linked (CU 5.5), and
  the project's English modification and no-endorsement sentences (a
  proposal). The indemnity recorded in `docs/data_sources.md` beside Hong
  Kong's, Sacramento's and the rest. `record_kind` "National register" for
  a cantonal business register (the kind CVR and Geostat's are).
- **Page proposals** (no template covers them): the scope bullet's list of
  12 communes; the register bullet ("every establishment of an active
  business, with its activity ..."); "Businesses the register types as run
  from home, itinerant trades and market stands are left out."; "About
  1,800 firms registered with no separate establishment are left out too:
  the register gives them no premises, so a shop cannot be told from a
  home address."; and the density caveat's second clause on office-typed
  establishments.
- **Downstream:** notice 154, **caption**, clearly visible with the card
  (CU: "de manière clairement visible", no place named); a card that
  travels without its caption carries the source line on its face. Notice
  1: rail, communes and stop names from OSM. **Open terms question: none.**
  New inputs: a city, a taxonomy, notice 154, the Swiss licence rows.

### 2026-10-07 - Bremen built: BSAG's eight trams on the 2022 regional retail survey (abroad-batch)

- **Privacy verdict: publish.** `check_personal_exposure.py bremen`: the
  survey's public variant has no name, address or person field (step 2
  stops on any field beyond its six); 2,148 pins show 19 goods-group labels.
- **Bremen built, page 304** (pipeline by a subagent from the brief; calls
  13 and 22-27 applied; its landing waits on parked call 1, the CC BY
  version). The cached survey zip (sha256 checked), through the new closed
  list `pipeline/taxonomies/bremen_einzelhandel.py` (19 goods-group codes,
  all Retail, each with an English pin label; an unknown or relabelled code
  stops step 2): **3,153 shops** with Gemeinde "Bremen", all inside OSM's
  city polygon; one Delmenhorst-labelled row inside the city line stays out
  with its municipality (call 23, the Gemeinde field decides). The catch-all
  "Sonstige EH-Einrichtungen" 94 (3.0%) kept (call 22). `categories`
  "Retail only" (call 24), `coverage` one_bucket.
- **Rail.** One Overpass query (overpass-api.de, osm_base 2026-10-07). 46
  tram relations: 37 kept on refs 1-6, 8, 10 (with short workings), the
  night lines N1, N4 and N10 not drawn. Three fixes in Bremen's own files: an
  untagged stop member on lines 2 and 10 dropped (22 m from Gustavstraße's
  named node; stale-checked); Am Brill (five nodes across 166 m) and Bahnhof
  Walle folded from per-platform names to BSAG's one name each; **line 8's
  five centre-loop stops added by node**, since OSM's line 8 relations
  predate BSAG's timetable change of 2026-08-17 (all five are stations of
  other lines, so the rings are unchanged; the drawn route through the
  centre lags OSM, and the page says so). 352 stop positions -> 164 stops,
  **gate 3 exact on all eight lines** against BSAG's timetable index (call
  25; BSAG_S26C: 44/33/29/49/14/25/27/32), **154 in the city**, tram 4's 10
  in Lilienthal listed outside (call 23). Boundary: relation 62559
  (Stadtgemeinde, AGS 04011000), 326.0 km², gated 310-340 (call 26), never
  the Land. **Median gap 351 m: halved rings.** Headways from BSAG's line
  timetables: lines 1, 4 and 6 every 7-8 minutes, 2, 3 and 10 every 10,
  5 and 8 every 20 (at call 2's floor, drawn). OSM's colors; line 2 is 14.0
  from the Retail pins, recorded, not moved (Göteborg's precedent).
  **2,148 of 3,153 (68.1%) in a ring.** A shared-module fix is noted, not
  made: `osm_tram` could take a "drop this unnamed member" option.
- **Notice 156 (the Kommunalverbund, CC BY, no version)**: the Quellenvermerk
  and the licence title exactly as written, linked to the record's licence
  URL (no CC version claimed), the dataset's title and a link to the file,
  the changes, no endorsement; the English sentences a proposal.
- **Page proposals** (the brief's "The page"): the two-figure frequency
  bullet, the line 8 bullet, "This map shows shops only, not three
  categories. ...", "The survey dates from 2022. ..." and "Read the density
  as a 2022 survey. ...".
- **Downstream:** notice 156, **caption**; a card that travels without its
  caption carries "Quellenvermerk: Kommunalverbund Niedersachsen/Bremen
  e.V." and the licence title on its face, and the survey's date on any card
  (the currency rule). **The CC BY version question is closed** (parked
  call 1, accepted on the permissive reading, owner 2026-10-07). New inputs: a city, a taxonomy, the "Retail only" value, notice
  156, the licence row.

### 2026-10-07 - Gelsenkirchen built: four tram lines on the City's premises survey (abroad-batch)

- **Privacy verdict: publish.** `check_personal_exposure.py gelsenkirchen`:
  no owner, contact or address field reaches the map (the reduced fetch,
  call 19), 0 contact details in a sign. The sign rule (call 15): 22
  person-shaped signs proposed by the German shape test, 4 of them found at
  two or more points and kept as brands, 18 withheld; then **read by eye by
  the lead session** over every displayed services sign (112) and the
  two-or-three-word letters-only signs at one location in the food (197)
  and retail (548) layers: 4 more read as a bare personal name with no trade
  word (one ambiguous, withheld on Zurich's precedent), kept as keys in
  `config.PERSON_NAMED_BY_EYE`. A trade word beside a name stays (Zurich's
  kiosk precedent). **22 signs show the category.** The heuristic's 30%
  "person-like" is its known artifact on German signs.
- **Gelsenkirchen built, page 303** (pipeline by a subagent from the brief;
  calls 15-20 applied). The reduced WFS fetch requests only the fields used
  (the OGC API ignores `properties`); the services layer moved since the
  brief (593 rows, 122 uncategorised; the brief corrected and its check
  green), food and retail identical by id to the 2026-10-04 cache, which is
  kept. **1,776 storefronts** (Retail 1,322 with 4 car dealers, Food
  service 346, Personal services 108); 176 uncategorised and 362 services by
  rule left out; a new services value "Sonstiges" (5) out as the R2
  catch-all, Liège's precedent. New closed list
  `pipeline/taxonomies/gelsenkirchen_gewerbe.py`: 67 (layer, category)
  pairs and 47 retail assortments, raising on an unknown; retail catch-all
  0.6%.
- **Scope: the survey's own points**, the OSM polygon (relation 62522, AGS
  05513000, 104.9 km²) as a check within 100 m (Liège's precedent): 2,313 of
  2,314 inside, one food row 1 m outside kept.
- **Rail.** One Overpass query; overpass-api.de answered 504 and kumi.systems
  answered a bbox form with **OSM data of 2026-06-01** (four months old; the
  caption gives that date; gate 3 still matches the operators' current
  timetables, so the stops are current). 10 relations kept; 101, 106, 108,
  306, 316 and U17 not drawn (no stop or track in the city). 271 stop
  positions -> 133 stops, **60 in the city**, 73 outside, cut at the city
  line (call 17); 107 alone serves seven city stops, so no stub question
  arises. **Gate 3 exact on all four lines** (301 34, 302 54, 107 34, U11
  23), counted on each timetable's line band, which lists every stop (the
  departure tables list timing points only). **Median gap 380 m: halved
  rings.** OSM's colors: 301 and 302 are 15.4 apart (both the operators'
  blues, sharing Hbf to Musiktheater; labels and legend tell them apart),
  each 31-42 from the nearest pin, recorded. **1,160 of 1,776 (65.3%) in a
  ring.**
- **Page proposals**: the two-operator lines bullet, the caption's OSM date,
  "Businesses come from the City of Gelsenkirchen's survey ...", the thin
  personal-services bullet, "176 surveyed businesses with no category are
  left out.", and the survey-date and survey-reading bullets; `data_age`
  "Undated survey (earlier files 2024), fetched 2026-10-07" (the brief's
  proposal).
- **Downstream:** no notice of its own (dl-de/zero-2.0); the caption
  credits the City as a courtesy. Notice 1: rail, boundary and stop names
  from OSM. **Open terms question: none.** BOGESTRA's and Ruhrbahn's
  timetables were read for counts only, their terms unread. New inputs: a
  city, a taxonomy.

### 2026-10-07 - Mexico City (Regional) built: four State of México municipios join on DENUE (abroad-batch)

- **Privacy verdict: publish.** `check_personal_exposure.py mexico_city`
  over 149,980 pins: 0 e-mails and 0 phone numbers in displayed names, no
  registrant-name column loaded; the one "c/o" (new) is a shop-sign
  abbreviation; the flagged sign names read by hand with digits masked:
  one e-mail shape (a veterinary sign the renderer's contact scrub drops)
  and 42 phone-length digit runs, every one a LICONSA milk-outlet number.
  32.6% person-like by the heuristic (32.2% before), the known artifact on
  Spanish shop signs.
- **Built on the regional-extension skill, the owner's calls 68-72
  (2026-10-06): all four municipios, Naucalpan kept, OSM boundaries on
  INEGI codes, the two entidad 15 files approved.** The pipeline by a
  subagent: a `REGIONAL` switch committed off at zero drift (950afe3b);
  `pipeline/countries/mexico.py` reads entidad 15's two parts
  (`DENUE_PARTS`, `denue_urls()`, `denue_members()`; `denue_url("15")` and
  `denue_member("15")` raise), with **zero drift on Mexico City, Guadalajara
  and Monterrey** through the change (heavy_job peak 2.41 GB). The parts'
  members carry no trailing underscore (`denue_inegi_15_1.csv`), against
  the brief's guess.
- **Stations 169 -> 180**, none excluded: Ecatepec 5, Nezahualcóyotl 3, La
  Paz 2, Naucalpan 1 (Cuatro Caminos), each asserted by point in polygon.
  Boundaries: one Overpass query, relations 5605754, 5606086, 5605964 and
  5606080, the union 414.0 km² gated 330-520.
- **Storefronts 280,185 -> 407,628**; the four add 127,443 (Ecatepec
  58,410, Nezahualcóyotl 36,073, La Paz 11,161, Naucalpan 22,216, before
  the polygon test). No storefront SCIAN code is new in entidad 15. **In a
  ring: 135,284 (48.3%) -> 149,980 (36.8%)**; the four municipios 14,379 of
  127,443 (Ecatepec 11.0%, Nezahualcóyotl 11.9%, La Paz 27.7%, Naucalpan
  2.8%). The CDMX side moves exactly as the brief measured: 317 enter a
  ring, 28 change station. Six CDMX rings that cross the city line gain
  storefronts (Canal de San Juan 1,133 -> 2,022, Santa Marta 848 -> 1,373,
  and four more); Politécnico's and El Rosario's (an eighth the brief did
  not list) cross into uncovered municipios.
- **Entidad 15 rows are tested against the scope polygon; CDMX rows keep
  the city-alone sanity box**, so the CDMX side is row for row as before
  (Monterrey's precedent); 21 Naucalpan-coded rows inside CDMX are kept.
- **Page proposals**: the regional-map bullet and its scope bullet, the
  "region's" wording in three places, "Most storefronts in the four
  municipios are beyond a station's reach ...", and notice 8's city
  sentence naming the four municipios. The display name is "Mexico City
  (Regional)"; its label scores clear at 375, 768 and 1200 (153.0 px).
- **Downstream:** an extension always counts: `outputs/mexico_city/`, the
  registry name, notices 8 and 1, macro facts and ring shares. Notice 8 is
  unchanged in kind (every page). Regional processed files are in
  `data/mexico_city/processed/regional/`; fold back on landing.

### 2026-10-07 - Thessaloniki built: Line 1 on the City's active shop licenses (abroad-batch)

- **Privacy verdict: publish.** `check_personal_exposure.py thessaloniki`:
  the layer has no name field; 6,292 pins show 51 distinct activity labels,
  0 contact details, 0 person-like names. Step 2 never reads the address
  fields.
- **Thessaloniki built, page 302, Greece's first city** (pipeline by a
  subagent from the brief; every owner call of 2026-10-04 applied as
  answered). The City's licence layer from the GeoServer WFS only (cached
  2026-10-04, 8,103 rows, EPSG:2100 reprojected to UTM 34N, geometry
  agreeing with the layer's own x/y on all 8,102 rows that carry them),
  through the new closed list `pipeline/taxonomies/thessaloniki_adeies.py`
  (all 79 activity values decided; catch-all "ANEY" 14 of 8,103, 0.17%):
  7,137 kept by activity, **7,132 inside the municipality** (Food service
  3,682, Food shops 2,430, Personal services 1,020). Out: no-counter food
  323 (canteens 246, owner call 1), recreation 280, wholesale 106, vending
  86, funeral 61, non-food retail 39, brothels 30 (R3), workshops 19, no
  activity 15, bicycle rental 7. **5 rows just past the OSM boundary
  (median 18 m, at most 60 m) dropped**, Florence's precedent for a city's
  own layer cut by the OSM polygon. Step 2 measured 0.01 GB.
- **Rail.** One Overpass query (routes, station objects, admin_level 7 and
  8). Four relations, all drawn as one line, **"Line 1"**, the operator's
  (THEMA's) station-list heading (call 4; read with the project's user
  agent, call 8): the base line and the Kalamaria branch, cut at the city
  line (a 1.30 km stub of the branch inside the city drawn, no station on
  it). 36 stop positions -> 18 stations; **gate 3 exact**, 18 on the line
  and 13 in the city, against Elliniko Metro's station pages (call 5) and
  THEMA's list; the branch's 5 (Nomarchia, 4 m past the line, to Mikra)
  listed outside. **Median gap 573 m: standard rings**, the spacing rule
  over the brief's desk 506 m (Palma's 583 m and Buffalo's 594 m kept
  standard rings); step 1 stops outside 550-620 m. Headways read from
  THEMA's FAQ (call 7). Boundary: OSM relation 1770680 (admin_level 7),
  20.82 km² (19.307 official), gated 17.5-21.5. **6,292 of 7,132 (88.2%)
  in a ring.**
- **Line color: OSM's red (#FF0000)**, the colour rule's OSM tag; the
  operator's own map draws the line navy (#0F0A68), 1.13:1 on the dark page
  and so unreadable there. CIE76 62.3 from the nearest pin.
- **Macro map:** Thessaloniki left out of Europe's zoom fit
  (`REGION_ZOOM_WITHOUT`, Bucharest's measurement), its label the default.
  `categories` "Retail thin" and `coverage` narrowed, Matsuyama's values.
- **Notice 155 (City of Thessaloniki, CC BY 4.0)**: the credit, the
  dataset's title linked to its data.gov.gr record, the licence linked, the
  retrieval date, the changes and no endorsement; the build's draft, a
  proposal. New `docs/data_sources/greece.md`.
- **Page proposals** (Matsuyama's shape; no template covers them): the color
  clause, the branch bullet, the frequency bullet ("about every 3 minutes
  between New Railway Station and 25th Martiou ... about every 9 minutes on
  to Nea Elvetia"), the three license-layer bullets and "A dot shows the
  type of business, never its name".
- **Downstream:** notice 155, **caption** (CC BY: credit reasonable to the
  medium; a card that travels without its caption carries the credit and
  licence on its face). Notice 1: rail, boundary and station names from
  OSM. **Open terms question: none** (the owner's reading of the portal
  splash, 2026-10-04, stands; a removal request takes the page down). New
  inputs: a city, a country, a taxonomy, notice 155.

### 2026-10-07 - Anyang (Regional) built: Gunpo and Uiwang join Anyang's page on SEMAS's codes (abroad-batch)

- **Privacy verdict: publish.** `check_personal_exposure.py`'s own check run
  on the regional file (`processed/regional/`, its registry entry's path
  pointed there for the run): PASS, 0 of 23,999 rows show a Korean personal
  name at a residential address; 42 withheld (Anyang 28, Gunpo 5, Uiwang 9).
- **Anyang (Regional), the owner's mark of 2026-10-04, built on the
  regional-extension skill.** A `REGIONAL` switch committed off first and
  proved at zero drift on the city alone (22a215c9); on, SEMAS keys on
  시군구코드 41171, 41173 (Anyang's two 구, the prefix's exact rows), 41410
  (군포시) and 41430 (의왕시): **23,999 storefronts** (Food service 11,331,
  Retail 8,993, Personal services 3,675; Anyang 15,177, Gunpo 5,868, Uiwang
  2,954), the brief's figures exactly; out by name: hostess bars 439, staff
  canteens 89, household fuel dealers 45, dance halls 24. Step 2 measured
  0.42 GB.
- **Stations: 7 -> 14**, 106 -> 99 listed outside: Line 1 eight, Line 4
  seven, Geumjeong shared (Gunpo 6, Uiwang 1), each line's in-scope
  stations agreeing with its line table (Anyang's stand-in for gate 3).
  Boundary: one Overpass query for 안양시, 군포시 and 의왕시 into
  `osm_boundary_regional.json` (relations 2409161, 2409167, 2409184; 59.1,
  35.9 and 53.8 km2), the union 149 km2 gated 142-156; the city's cache
  untouched. Median gap 1,443 m, standard rings. **15,799 of 23,999 (65.8%)
  in a ring**: Anyang 66.1%, Gunpo 86.6%, Uiwang 23.3%.
- **The rename**: "Anyang (Regional)" in `app/cities.py`, the page (same
  file, `87_Anyang_Heatmap.py`), notice 68's title and text (Anyang, Gunpo,
  Uiwang), notice 1, the reference rows. The label widened to 124.6 px and
  moved right of its dot, the one offset of ten that clears the Seoul
  Capital Area at 375, 768 and 1200. **Regional processed files are in
  `data/anyang/processed/regional/`; fold back on landing** (the skill).
- **Page proposals**: "The map covers Anyang with its neighbors Gunpo and
  Uiwang, which the same two lines serve."; "The two lines share one
  station, Geumjeong, in Gunpo."; "Uiwang has one station, at its western
  edge, so about one of its storefronts in four sits within a ring."; and
  notice 68's city list with Gunpo and Uiwang.
- **Downstream:** an extension always counts: `outputs/anyang/`, the
  registry name, notices 68 and 1, macro facts and ring shares. Notice 68:
  caption, and the SEMAS card hold applies as before.

### 2026-10-07 - Abroad batch: page proposals, numbers and downstream (abroad-batch)

- **Page sentences outside a template, proposed for review time.** Gimpo:
  "Not drawn: Lines 5 and 9, the Airport Railroad and the Seohae Line, which
  meet the Goldline at Gimpo International Airport in Seoul. None of them
  has a station in the city." (Gimhae's approved not-drawn bullet with
  Gimpo's lines.) Siheung: "Line 4 and the Suin–Bundang Line share Oido and
  Jeongwang, and the Seohae Line runs on its own track through the east of
  the city." (Ansan's shared-stations bullet, filled) and "The Suin–Bundang
  and Seohae lines run about every 15 minutes by day, less often than Line
  4." (Namyangju's approved wait bullet, filled; the brief's disclosure of
  the borderline lines.)
- **Page and notice numbers claimed for the batch:** pages 202 (Gimpo), 300
  (Siheung), 301 (Geneva), 302 (Thessaloniki), 303 (Gelsenkirchen), 304
  (Bremen); notices 154-156 (Geneva, Thessaloniki, Bremen). Staging recorded
  the claim on master the same day.
- **Downstream (`docs/session_roles.md`).** Gimpo and Siheung: notice 68
  (SEMAS) **caption** (the terms prescribe a source credit with no wording
  or place); notice 1, rail, boundary and station names from OpenStreetMap.
  **Open terms question: the SEMAS card hold** (whether SEMAS's permission
  reaches social posts), inherited, so both stay off cards and public pieces
  until the owner rules. New inputs: two cities, notice 68's and notice 1's
  city lists.
