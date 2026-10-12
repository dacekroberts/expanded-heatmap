# Decisions drafts: worktree-japan-naha (Naha, phase 2 of the A/B build plan)

Entries in the `decisions-entry` format, newest first, each as it should land.
Cleanup folds this file into `DECISIONS.md` when the owner hands it off.

## Parked calls

Named by city and letter; Staging assigns the S numbers when it relays them.

- **Naha A, B, C: ANSWERED by the owner in Cleanup's chat, 2026-10-12 (S39,
  S40, S41; relayed by Staging, logged in DECISIONS on master): "yes with
  conditions for s39, s40 left as is, s41 maybe a small line appears on the
  kyushu-okinawa regional view stating (naha below) a temporary item".**
  S39: `rebuilt_register` reads a row filling both 業種 and 営業の種類 by 業種
  as the type (b9ad4096, zero drift on the seven built cities that call the
  stitch); this branch merged master and re-ran steps 2 and 3 (the entry
  below, "after S39"). S40: the October 2016 file is left as is;
  `config.TYPE_UNREAD` still guards it. S41: Cleanup's at the landing (Naha
  held out of the Kyushu-Okinawa view's zoom fit, a temporary "Naha below"
  line worded for the owner first); no view was touched here, so
  `check_macro_labels.py` still reports PROBLEMS 4 on this branch.
- **Naha D: page and notice sentences no template covers (proposals, flagged
  for review time; S36).** On the page: (1) "The map shows an upper bound:
  the rebuilt list holds 8,785 restaurant permits, against 8,530 in force in
  the national count of March 2025." (S32's measured figure, inside Kyoto's
  sentence); (2) "The city publishes no list of laundries, so the Personal
  services layer has none."; (3) "Stalls licensed for the whole city (769)
  and vehicles licensed across the prefecture (171) have no fixed address and
  are left out."; (4) "Bars with hostess service are left out where the
  permit names its form of business, which about one restaurant permit in
  five does."; (5) "A street block is one point on the map, so dense blocks
  stack many dots on one spot. The densest is the Sakaemachi market block in
  Asato, with about 250."; (6) "One line is drawn, labeled on the map and in
  the legend: the Yui Rail, Okinawa's monorail." In What Is Excluded: "Three
  months are published twice; where an address, trade name and permit type
  repeat, the permit ending latest is kept, so a repeat or a renewal counts
  once." Notice 217's
  wording (no wording is prescribed by the city's terms): Sasebo's edited-use
  form naming the three datasets, with the three package links and "rebuilt
  the city's food permits from its monthly lists of new and renewed permits,
  kept those still in term at the end of August 2026".
- **Naha E: ANSWERED by the owner, twice, 2026-10-12.** First "operator's
  english for E": the four overrides were removed, since OSM's `name:en`
  matches the operator's English site (www.yui-rail.co.jp/en/, the timetable
  menu's text) on all 16 stations. Then "i mainly wanted the change for
  naha's airport, we can revert to precedent since it covers city-wide":
  **the precedent stands for station names, except 那覇空港, which is "Naha
  Airport".** Onoyama-koen, Kencho-mae and Shiritsu-byoin-mae are romanised
  again in Hiroshima's style (three cited overrides); the airport keeps OSM's
  and the operator's English, a departure from Itami's Osaka-kuko for this
  station alone (this session's reading of the owner's sentence; a full
  revert to Naha-kuko is one line in `OSM_NAME_EN_OVERRIDES`). The line
  stays "Yui Rail". **A correction to this call as first put**: it gave the
  operator's English as "Kenchomae" and "Shiritsubyouin-mae", which were the
  site's URL slugs, not its printed names (Prefectural Office, Naha City
  Hospital).
- **Naha F: an idea for later, not built (owner, 2026-10-12; passed to
  Cleanup).** "potential future implementation would be an english-language
  switch for cities that have the option": a map control that swaps station
  names between the romanised form and the operator's own English where an
  operator publishes one (Naha's four, Itami's Osaka Airport). Under the
  feature freeze of 2026-10-08 it is recorded, not started.

## Entries

### 2026-10-12 - Naha after S39: the August 2020 renewals read by the shared rule; 10,153 pins and 8,785 restaurant permits, the brief's figure to one row

- **Decided by the owner (S39, in Cleanup's chat, relayed by Staging).**
  Master's b9ad4096 merged into this branch; steps 2 and 3 re-run, the
  baseline recorded, and the two disclosure phrases dropped (the "About 20
  restaurants" bullet of What Is Excluded and the "unread" clause of table
  C).
- **Counts, replacing the build entry's.** 10,514 permits in term (two keys
  that differed only by the misread type now fold); 8,785 of type 飲食店
  against 8,530 (103.0%; the brief's 8,786). Set aside: 769 and 171 as
  before; 410 not storefronts (215 no rule, 122 hostess venues, 60 vending,
  10 caterers, 2 inside inns, 1 temporary). Storefront rows 10,520 (Food
  service 7,657, Food shops 1,507, Personal services 1,356); 359 repeats
  folded; **10,153 pins** (Food service 7,650, Food shops 1,150, barbers 287,
  beauty salons 1,066), 18 more than before, all Food service. This build's
  earlier estimate of 20 missing rows was before the one-pin-per-premises
  step.
- **Unchanged or re-measured.** Join: block 10,359 (98.5%), town-chōme 153,
  unplaced 8. In a ring: 8,598 of 10,153 (84.7%). Census control 2.87 per
  establishment. Privacy: the Japan pass prints 0 of 10,153 rows, 4 pins
  show their permit type; verdict publish. The densest block still holds
  250. Station names as call E left them.
- **Checks.** Drift zero against the new commit; `check_all.py` as before,
  failing only on the master list's counts (Staging's) and the
  Kyushu-Okinawa view (S41, Cleanup's).

### 2026-10-12 - Naha built, a food register rebuilt from the city's monthly new-permit and renewal lists, with its barber and beauty registers (page 307, notice 217)

- **Decided by precedent and the owner's calls S13, S15 and S29 to S38
  (the brief); nothing re-asked.** Band B, Food plus Personal services
  without laundries; both food packages; in term on 2026-08-31; Kyoto's
  upper-bound sentence with the measured figure, no trimming; mode
  `light_rail`; region Kyushu-Okinawa with the view left to Cleanup; BODIK
  copies only; one notice for the three packages.
- **Why this shape.** Naha publishes no full food-permit list, so the
  register is stitched by `japan_register.rebuilt_register` from 140 monthly
  new-permit workbooks and 73 renewal workbooks through the shared reader
  (`city_rows` with `unnamed_after` on all four type spellings), never a
  city-local stitch. The rejected alternative, the new-permit files alone,
  loses 329 pins of long-standing premises (S31).
- **Counts, this build's own.** 10,516 permits in term (the brief's 10,515);
  8,744 of type 飲食店 against e-Stat's 8,530 (102.5%; the brief's 8,786 and
  103.0% differ by parked call A's 42 rows). Set aside: 769 citywide stalls,
  171 area-wide vehicles, 431 not storefronts (235 no rule, 123 hostess
  venues, 60 vending, 10 caterers, 2 inside inns, 1 temporary). Storefront
  rows 10,501 (Food service 7,640, Food shops 1,505, Personal services
  1,356); 358 repeat permits folded; **10,135 pins** (Food service 7,632,
  Food shops 1,150, barbers 287, beauty salons 1,066). The new-permit files
  alone reproduce the brief to one row (10,001 in term, 8,430 restaurants,
  7,391 and 1,358 storefront rows, the same 312 not-storefront rows by
  rule), which is the control.
- **The join.** Block 10,340 (98.5%), town-chōme 153 (1.5%), unplaced 8
  (0.1%): 鏡水崎原地先 3, and one each at 字金城, 字旭町, 上間東原, 首里当蔵,
  字古波蔵. The brief's two 壼屋 rows now place (the shared 壼 variant). No
  independent check: the files carry no coordinates, and the GSI sample the
  brief suggests was not run (a source outside the brief).
- **Dense blocks.** 1,893 distinct points; 24 hold 50 or more pins (1,697
  pins). The densest holds 250: 安里388, the lot of the Sakaemachi market
  (one address names 栄町市場内), 247 food pins and 3 salons. Honest at block
  precision; the page says so.
- **Census control.** `japan_census_control.py naha`: 7,632 Food service
  pins against 2,669 establishments in the 2021 Economic Census, 2.86 per
  establishment (the brief's 2.77 was the new-permit files alone), far over
  the built cities' 1.56 to 1.92. The official in-force count is as high,
  so the register matches it and both run ahead of the census; published
  with the upper-bound sentence, no trimming (S32). Same-address successors
  were not re-measured (the brief's Step 0 figure, 693 rows of the
  new-permit files, stands).
- **Rail.** N02-25, 沖縄都市モノレール線: 16 of 19 station groups inside
  47201, median gap 733 m, standard rings; 経塚, 浦添前田 and てだこ浦西
  written to `excluded_stations.csv` under 浦添市. **Gate 3**: the operator's
  home page (www.yui-rail.co.jp, 駅情報) lists 19 stations, the same names in
  N02's order. OSM `name:en`: one Overpass query (the first attempt met 504s
  on both mirrors; retried after more than 60 s), 20 objects, 3 overrides (call E).
  Frequency: not re-read; the operator's timetable page is not named in the
  brief, so the master list's read (every 7 to 9 minutes) stands.
- **Colour.** `line_colour_search.py naha`: #E84028 from the red of the
  trains' stripe, 3:1 on both pages (4.63 dark, 4.04 light), CIE76 45.0 from
  the nearest pin (Food service). Registered in `pipeline/line_registry.py`
  for the Urasoe add-on; `check_line_identity.py` PROBLEMS 0.
- **Opening view and attribution.** `check_map_view.js` on the standalone
  map: zoom 13.75 = expected at 1024 px on two fresh loads, 12.5 = expected
  at 375 px, 0 corrections, no problems. `check_map_attribution.js` at
  1024x768 and 375x812: the credit clear at all five points, legend forced
  open.
- **Privacy verdict: publish.** `check_personal_exposure.py naha`: the Japan
  pass prints 0 of 10,135 rows; 4 pins show their permit type. Applicant,
  representative and opener columns are read in memory by the name rule
  only; no address or phone column of theirs is selected.
- **Shared code touched, each opt-in and inert for built cities.**
  `japan_fetch.fetch_city`: `config.FETCH_PAUSE_S` (a wait after each file
  actually downloaded; BODIK's spacing for 215 files) and a `None` URL in
  `SOURCE_FILES` resolved by `config.source_url` (so 215 URLs are one
  template plus pinned ids, as Kyoto's 79). `japan.CITIES["naha"]`, the
  registry entry, the privacy check's entry, the two notice lists and
  `TEXT_WIDTH["Naha"]` = 34.1 (local app, canvas; Hino, Hirakata, Nara and
  Tama reproduced).
- **Left failing on purpose.** `check_provenance.py`: the master list's
  counts (Staging's, plan rule 4). `check_macro_labels.py`: parked call C.
- **If this turns out wrong.** A newer monthly file moves `AS_OF` and every
  count; the registers are replaced whole each month. Parked call A's fix
  adds about 20 pins.
