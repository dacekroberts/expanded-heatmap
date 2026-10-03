# DECISIONS drafts - Japan wave 2 (`japan-wave2-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-03 - Higashiōsaka built, food only, on a register rebuilt to August 2026

- **Higashiōsaka built (page 186, notice 125): 5,775 storefronts (Food
  service 5,085, Food shops 690) around 26 stations on 6 lines, 90.4% in a
  ring (5,218).** The city's BODIK food list (CC BY 4.0) of 2026-04-01 plus
  the monthly new permits to 2026-08-31, rebuilt through `config.source_rows`
  (`japan_register.rebuilt_register`: 7,067 read, 358 de-duplicated across
  the lists, 6,709 kept, 188 past their expiry, 6,521 in term), joined to
  MLIT's block file for 27227: 5,864 of 5,885 storefront rows at the block
  (99.6%), 21 at a town centroid, 0 unplaced. Out: 419 stalls and vehicles,
  165 manufacturing and other types, 52 vending. 110 repeat permits shown
  once. The old-law retail types (（旧）菓子 59, 食肉 19, 魚介 15, そうざい 15)
  count since the shared fix of 7b220d40. Factory share 21 of 455 (4.6%),
  kept. No `OWN_POINT_FALLBACK`: the list's points are in the old Tokyo Datum
  (the brief: 448 m, 37 m shifted) and the 21 chōme rows do not need them.
- **Held calls, counts touched:** 複合型そうざい製造業 3 rows (and 1
  複合型冷凍食品製造業) stay out; 業態 is empty in this list, so the
  deli-by-業態 call touches none.
- **Privacy verdict: publish.** The Japan pass prints 0; no individual
  operator column (法人名 only), so the whole page runs without the name rule
  (Okayama's call, owner 2026-10-02).
- **Economic Census control: 2.66** (5,085 / 1,910), above 1.56-1.92, the
  brief's expected about 2.7. The list is complete (5,505 restaurant permits
  in term against 5,534 official, 99.5%), so it is permits per census
  establishment. With no 業態 column nothing leaves Food service by form
  (trade-name keywords: 360 bar / snack / lounge names, about 130
  institutional ones); 1,271 Food service pins share an exact address with
  another; closures since April are invisible. The rebuilt registers built
  before run high the same way: Kyoto 2.62, Sakai 2.18 (Matsuyama 2.73).
- **Rail:** N02-25, Kintetsu Nara (11), Osaka (4) and Keihanna (4, its
  class-21 section, drawn under its own name though it runs through onto the
  Chuo Line), Osaka Metro's Chuo Line (2, drawn cut, owner 2026-10-02), JR
  Osaka Higashi (5) and Gakkentoshi (片町線, 2). 17 stations excluded (Osaka
  City 9, Yao 5, Daito 2, Ikoma 1 through `N03_NEIGHBOR_PREFS`). 高井田中央 /
  高井田, JR河内永和 / 河内永和 and JR俊徳道 / 俊徳道 (39-79 m) are separate
  groups of different names, kept apart. No line wholly inside, so no gate 3.
  2 name overrides. Colours: Osaka's four shared lines started from Osaka's
  colours and came back within one grid step; closest pair 20.7. Median
  station gap 767 m: standard rings.
- **Prose proposals for review time:** on the page, "Higashiōsaka City
  publishes no list of barbers, beauty salons or laundries, so personal
  services are not on this map." and "The list names an operator only where
  it is a company, so a trade name that is its operator's own name cannot be
  checked here." (Kawasaki's clause, for the whole list); in What Is Excluded,
  "The list records no form of business, so snack bars, staff canteens and
  shop counters that hold a restaurant permit stay in Food service.", the
  de-duplication sentence, the Names not shown sentence, and the Chuo Line
  station bullet.

### 2026-10-03 - Hamamatsu built, personal services only

- **Hamamatsu built (page 185, notice 124): 3,187 storefronts, all Personal
  services (barbers 718, beauty salons 2,082, laundries 387), around 54
  stations on 4 lines, 33.9% of them in a ring (1,080).** The city's four CC
  BY 2.1 JP registers published 2026-08-18 (barbers 718, beauty 2,107, laundry
  pick-up counters 239, general laundries 148: 3,212 against e-Stat FY2024's
  3,164, 101.5%), joined to MLIT's address blocks for the 3 wards of 2024
  (22138-22140): 3,047 at the block (94.9%); the 165 the block join placed
  only at a town-chōme or 大字 centroid take the city's own 緯度 / 経度
  (`OWN_POINT_FALLBACK` on all four registers, the brief's grounds: block-tier
  points a median 40 m off, the centroids a median 741 m); 0 unplaced, 0
  default points refused, datum_guard passed. 25 repeat registrations shown
  once (21 barber-and-beauty premises, 4 beauty duplicates). MHLW's 6,033
  notifications not added (owner, 2026-10-02).
- **Privacy verdict: publish.** `check_personal_exposure.py hamamatsu`: the
  Japan pass prints 0; the registers have no operator column, so the name
  rule cannot run (Okayama's precedent) and the page takes the MHLW-style
  bullet. The Latin heuristic flags 14 in-ring pins (9 美容所, 5 理容所), not a
  finding for Japanese names.
- **Rail:** N02-25, 4 lines: the Enshu Railway (18 of 18, gate 3 exact
  against entetsu.co.jp/tetsudou/), Tenhama (19 of 39), JR Tokaido (5 of 89)
  and JR Iida (13 of 94, its mountain stretch, drawn by the standing call).
  9 stations excluded (湖西市 3, 磐田市 3, 東栄町 2, 天龍村 1; Aichi and
  Nagano through `N03_NEIGHBOR_PREFS`). Median station gap 1,158 m, standard
  rings. English names: 12 cited overrides (Hiroshima's style), and 浜北 /
  天竜二俣, which have no OSM name:en (天竜二俣 carries only a wrong
  name:ja_rm), from the operators' station pages. Colours from
  `line_colour_search.py` (closest pair 31.4, Enshu / Tokaido).
- **Opening view:** BOUNDS 34.686-35.217 N, 137.526-137.871 E bake zoom 10.0
  (the stations from the coast to 大嵐); `check_map_view.js` to run at review.
- **No Economic Census control** (no food leg); the e-Stat table and the
  city's own points are the checks.
- **Prose proposals for review time:** on the page, "The city reaches from
  the coast far into the mountains: 32 of its 54 stations are on the Tenryu
  Hamanako Line and on the Iida Line's mountain stretch through Tenryu Ward.";
  "The registers were published on 18 August 2026 and record no closures, so
  a dot is a premises on the register then, not necessarily one open today."
  (Hakodate's sentence, its date as the registers' publication date); "where
  only the district can be found, the dot sits at the city's own coordinates
  for the premises." (Okayama's ministry-coordinates clause for a city
  source); "The registers do not say who the operator is, so a trade name
  that is its operator's own name cannot be checked here." (Okayama's, for
  registers); in What Is Excluded, the Not placed and Names not shown
  sentences above.

### 2026-10-03 - Nara built, MHLW's filings, the old-law list and three registers

- **Nara built (page 184, notice 123): 4,813 storefronts (Food service
  2,428, Food shops 1,169, Personal services 1,216) around 14 stations on 5
  lines, 68.7% of them in a ring (3,305).** MHLW's filings (7,157 rows), the
  city's old-law list as of 2025-11-01 (1,341 rows, 820 in term on 2026-08-31
  by 許可有効期限 through `in_term`, 521 dropped) and its three registers as of
  2026-04-01 (barbers 213, beauty 837, laundries 213; cp932), joined to MLIT's
  address blocks for 29201: of 5,268 storefront rows, 4,718 at the block
  (89.6%), 347 at MHLW's own point (6.6%; 345 from chōme, 2 from none), 169 at
  a town centre (3.2%), 34 unplaced (0.6%). By source: MHLW 89.6% block
  (10.3% own point), old-law list 89.2 / 10.8 / 0.0, registers 89.5 / 7.8 /
  2.6 (barber 85.4, beauty 92.0, laundry 84.0 block) - the lead's screen
  exactly. MHLW's own point against the block point: median 40 m, 95.1%
  within 250 m (3,008 rows). 90 old-law rows dropped for their MHLW row
  (`SUPERSEDES`); 331 repeat permits shown once. Closed 22; no address
  published 1,978 (896 open restaurant permits of 4,074, 22.0%: "one in
  five"); not a premises 788 (760 MHLW 一円, 28 old-law 一円). Out by rule:
  421 manufacturing and other non-counter types, 246 canteens, 139 vending,
  119 snack bars and cabarets, 100 caterers, 93 inside hotels and inns, 36
  entertainment venues, 19 temporary, 11 mail order.
- **そうざい屋 leading an old-law sub-type is Retail** (the そう菜店 precedent,
  in the shared taxonomy): 27 in-term rows. The brief counted them as
  restaurants (its 472 old-law Food service against the build's 439). One
  in-term old-law row, ビアガーデン, falls to "no rule" (out).
- **Held items touched (owner call pending):** 40 MHLW restaurant rows whose
  業態 names a deli (そうざい屋 10, そうざい屋、弁当屋 5, そうざい 4, and 21
  other spellings) stay Food service.
- The 菓子 / そうざい factory share: 6 of 535 (1.1%), kept (owner,
  2026-09-24).
- **Privacy verdict: publish.** `check_personal_exposure.py nara`: the Japan
  pass prints 0; 0 trade names that are an operator's own name in the raw
  files, none withheld; MHLW names no individual (Fukuoka's precedent).
- **Rail:** N02-25; 14 stations (Kintetsu 10: Nara 6, Kyoto 3, Kashihara 3,
  大和西大寺 shared by all three; JR 4: Yamatoji 2, Man-yo Mahoroba 3, 奈良
  shared). Thin rail, built anyway (owner, 2026-10-02). Median nearest-station
  gap 1,108 m (min 879): standard rings. 10 excluded: 大和郡山市 3, 木津川市 2,
  生駒市 2, 天理市 1, 笠置町 1, 精華町 1 (Kyoto's named through
  `N03_NEIGHBOR_PREFS` = 26). Gate 3: Kintetsu's station index read against
  the city line gives Nara 6, Kyoto 3, Kashihara 3, exact. English names:
  OSM's 75 objects, 4 cited overrides (Gakuen-mae, Kintetsu-Nara, Kyobate,
  Nishinokyo). Colours from `line_colour_search.py` (Kintetsu's three reds
  part into red, coral and orange; closest pair 18.2).
- **Economic Census control: 1.93** (2,428 Food service pins against 1,258),
  0.01 above the built cities' 1.56-1.92, as the brief predicted ("about 2.0").
- **Three dates on one page**: the old-law list 2025-11-01 (filtered to
  2026-08-31), the registers 2026-04-01, MHLW downloaded 2026-10-02.
- **Prose proposals for review time**: none on the page beyond the template
  and Kitakyushu's approved sentences (the registers sentence reworded for
  three registers); in What Is Excluded, "The city's old-law delis filed as
  そうざい屋 are Food shops."

### 2026-10-03 - Ōtsu built, the city's food list and three registers

- **Ōtsu built (page 183, notice 122): 4,508 storefronts (Food service
  2,645, Food shops 868, Personal services 995) around 40 stations on 4
  lines, 74.7% of them in a ring (3,367).** The city's monthly food list as
  of 2026-08-31 (`od_2608.csv`, 4,499 rows, read from its page's current link)
  and its BODIK barber, beauty and laundry lists of the same date (187, 618,
  202), joined to MLIT's address blocks for 25201: of 4,658 storefront rows,
  4,437 at the block (95.3%), 220 at a town centre (4.7%), 1 unplaced (the
  brief's screen 94.7 / 5.3 / 0.0). 149 repeat permits shown once. Out by
  rule: 176 manufacturing and other non-counter types (1 of them
  複合型そうざい製造業, held out), 26 cooking vending machines. Not a premises:
  646 市内一円 food rows (641 restaurants).
- The 菓子 / そうざい factory share: 15 of 605 (2.5%), kept (owner,
  2026-09-24). No 業態 column, so no deli-by-form row is touched.
- **Privacy verdict: publish.** `check_personal_exposure.py otsu`: the Japan
  pass prints 0; 3 pins show their permit type (3 flagged rows: food 1, barber
  1, beauty 1; the check counts 2 trade names). Without the `coop` rule it was
  5 rows and 5 pins: 2 food rows are a cooperative's own name.
- **Rail:** N02-25; 40 stations (Keihan 24 by line: Ishiyama-Sakamoto 21,
  Keishin 4, びわ湖浜大津 shared; JR 16: Kosei 12, Biwako 4). The Sakamoto
  Cable left out (Kobe's funicular rule), not in `excluded_stations.csv`.
  **Median nearest-station gap on the 40 drawn stations: 577 m**, as the brief
  measured, outside the 540-570 m band: standard rings. Keihan-zeze / Zeze (54
  m) and Keihan-ishiyama / Ishiyama (95 m) are separate N02 groups of
  different names, kept apart. 5 excluded: 京都市山科区 4 (named through
  `N03_NEIGHBOR_PREFS` = Kyoto, 26), 草津市 1. Gate 3: Keihan's station index
  gives the Ishiyama-Sakamoto Line 21, exact. English names: OSM's 70 objects
  name every Keihan stop as railway=station, so no tram-stop file is declared;
  4 cited overrides (Horai, Omi-Maiko, Otsu: macrons; Ogoto-onsen). Colours
  from `line_colour_search.py` (closest pair 26.7; the Keishin and Biwako
  lines come out as Kyoto's own colours for them).
- **Independent check (GSI address search, 100 block hits):** median 39 m
  from the block point, 91 within 100 m, 99 within 250 m, max 797 m.
- **Economic Census control: 2.59** (2,645 Food service pins against 1,021
  飲食店 establishments), above the built cities' 1.56-1.92, as the brief
  predicted (2.6). The official FY2024 in-force count (3,115) is itself 3.05
  per census establishment; the pins are 85% of it. Built on the brief's
  reading.
- **Prose proposals for review time**: on the page, "The Shinkansen is not
  drawn; it crosses the city without a station." (Kawasaki's proposal again);
  "The Sakamoto cable car, which is a sightseeing line, is not drawn." (the
  template's sentence in the singular); the same two in What Is Excluded.

### 2026-10-03 - Yokkaichi built, the city's five lists

- **Yokkaichi built (page 182, notice 121): 4,308 storefronts (Food service
  1,995, Food shops 1,298, Personal services 1,015) around 35 stations on 7
  lines, 73.9% of them in a ring (3,185).** The city's five CC BY 4.0 BODIK
  lists as of 2026-08-31 (food permits 3,725 rows, food notifications 1,247,
  barbers 216, beauty 737, laundries 106), joined to MLIT's address blocks for
  24202: of 4,687 storefront rows, 4,170 at the block (89.0%), 407 at a town
  centre (8.7%), 110 unplaced (2.3%; the brief's screen 88.8 / 8.9 / 2.4).
  269 repeat permits shown once. Out by rule: 548 バー、キャバレー by 業態
  (Tokyo's R3 precedent, the national form list's one class), 392
  manufacturing and other non-counter types (199 permit, 193 notification),
  261 canteens (157 集団給食施設 notifications, 104 委託給食 by 業態), 88
  caterers (仕出屋、弁当屋 by 業態), 41 inside hotels and inns, 3 mail order, 1
  行商. Not a premises: 10 (5 無店舗取次店 read from the laundry list's 区分; 5
  一円 rows: 1 notification, 1 barber, 3 beauty).
- **The notification list counts as Food shops** (japan_eigyo's rule: a list
  that publishes its notifications; it is the city's complete list): 892 rows,
  so the template's standing "notify" bullet is replaced on the page (a
  proposal, below). The laundry 区分 工場 (31) kept as laundries (Hakodate's
  一般, Toyota's 洗場).
- **Held items touched (owner call pending, read at the built cities'
  reading):** 82 restaurant permits whose 業態 is 飲食店営業（惣菜店） (75, and
  7 old-law) stay Food service; 3 複合型そうざい製造業 stay out. The
  shared-code entry's list of touched wave-2 rows does not name Yokkaichi's 82.
- The 菓子 / そうざい factory share: 26 of 400 (6.5%), kept (owner,
  2026-09-24).
- **Privacy verdict: publish.** `check_personal_exposure.py yokkaichi`: the
  Japan pass prints 0; 3 pins show their permit type. 5 rows in the raw files
  are flagged by the name rule (3 permit, 2 notification; the check counts 4
  trade names); the registers flag none. Without the `coop` rule (commit
  13b2c280) it was 10 rows and 5 pins:
  5 rows are a cooperative's own name. The food lists name sole traders as
  well as companies.
- **Rail:** N02-25; 35 stations (Kintetsu 15 by line-membership: Nagoya 10,
  Yunoyama 6, 近鉄四日市 shared; Asunarou 9; Sangi 7; JR 5; Ise Railway 1). The
  Sangi Line's 近鉄連絡線 drawn with 三岐線 as one public line; the Ise Railway's
  one station (河原田, shared with JR) kept as cut (standing call: a regional
  third-sector line, not urban). Kintetsu-Yokkaichi and Asunarou Yokkaichi are
  separate N02 groups 33 m apart, kept apart (Kobe's Tarumi case). Median
  nearest-station gap 1,133 m: standard rings. 12 excluded: 菰野町 4, 鈴鹿市 3,
  いなべ市 2, 朝日町 2, 川越町 1. Gate 3: the Asunarou Railway's own route map
  (yar.co.jp/route/, read 2026-10-03) gives the Utsube Line 8 and the
  Hachioji Line 2, exact. English names: OSM's 61 objects, 7 cited overrides
  in Hiroshima's style (macrons, Shinshyo -> Shinsho, Kintetsu-Tomida's
  hyphen, -mae / -koenguchi). Colours from `line_colour_search.py` (closest
  pair 18.2, Asunarou's two lines; the Ise Railway purple, as no blue clears
  Retail's pin).
- **Independent check (GSI address search, 100 block hits, 1 req/s):** median
  32 m from the block point, 83 within 100 m, 91 within 250 m, 99 within 500
  m, max 1,025 m.
- **Economic Census control:** 1,995 Food service pins against 1,074 飲食店
  establishments, 1.86, inside the built cities' 1.56-1.92.
- **Prose proposals for review time** (no approved template covers them): on
  the page, "Food shops that only notify the city rather than hold a permit,
  such as convenience stores, supermarkets and greengrocers, are included: the
  city publishes its list of notifications too." (replaces the template's
  notify bullet), "From Yokkaichi City's lists of food-business permits and
  food-business notifications ..." (the template's source bullet with the
  notification list added), and the template's Food shops bullet shortened
  to "the Food shops layer is food retail only." (its bracketed list no longer
  covers what the layer holds); in What Is Excluded, "548 restaurant permits
  filed as bars and cabarets (バー、キャバレー): the national form list puts both
  in one class." and the Counted paragraph's notification and 工場 sentences.

### 2026-10-03 - Toyota built, the city's food list and three registers

- **Toyota built (page 181, notice 120): 4,203 storefronts (Food service
  2,729, Food shops 466, Personal services 1,008) around 25 stations on 4
  lines, 51.5% of them in a ring.** The city's CC BY 4.0 lists on BODIK as of
  2026-08-31 (food 3,667 rows; barbers 282, beauty 634, laundries 144 over
  the workbook's two sheets), each fetched through its CKAN resource's
  current URL (`SOURCE_RESOURCES`; every register resource is named
  `_20268.xlsx`), joined to MLIT's address blocks for the one municipality:
  3,667 rows at the block (80.2%, the brief's), 676 at a town or 大字 centre,
  232 unplaced (5.1%, the brief's 7.0% before `chome_missing` put 浄水町's
  丁目 at the 大字 centroid; 84 pins in 浄水町 sit there now). Per bucket the
  block share is the brief's: Food service 80.3%, Food shops 69.7%, Personal
  services 85.6%. 140 repeat permits shown once. Out by rule: 151
  manufacturing and other non-counter types ("no rule"). Not a premises: 1
  beauty salon registered 一円 (citywide). The list holds 2,921 restaurant
  permits against e-Stat's FY2024 3,898 (74.9%): the city leaves temporary and
  stall permits out (its catalogue record says so), which every Japanese map
  drops anyway. Laundries 144 of 170 (84.7%).
- **Held calls, counts touched:** none (no 複合型そうざい製造業 row; no 業態
  column). The 菓子 / そうざい factory share: 14 of 355 (3.9%), kept (owner,
  2026-09-24).
- **Privacy verdict: publish.** `check_personal_exposure.py toyota`: the
  Japan pass prints 0; 1 pin shows its permit type (4 raw rows; 10 of the
  brief's 14 are a cooperative's own name, shown, a cooperative (組合) is no person for the name rule, 13b2c280). The
  food list names every operator; the registers name company operators only
  (Toyama's accepted position, the page's bullet).
- **Rail:** N02-25: the Aichi Loop Line (12 of 23) and Meitetsu's Mikawa Line
  (10 of 23) cut at the city line; the Meitetsu Toyota Line (3 of 8) and
  Linimo (2 of 9) drawn as cut (owner, 2026-10-02). 八草 (Aichi Loop and
  Linimo, 191 m) and 梅坪 (Mikawa and Toyota lines) are one group each;
  新豊田 / 豊田市 (255 m, the closest pair) and 新上挙母 / 上挙母 stay apart.
  Gate 3: the Aichi Loop Railway's station index lists 23 stations in order,
  三河上郷 to 八草 (12) inside the city, exact. 11 stations excluded: 3 in
  Okazaki, 3 in Chiryu, 2 in Miyoshi, 2 in Nagakute, 1 in Seto. English names
  in Hiroshima's style: 7 cited overrides (浄水, 三河上郷, 四郷, 陶磁資料館南
  without OSM's macrons; 上豊田, 三河八橋 hyphenated and 上挙母 as one word, as
  the Aichi Loop signs 新上挙母 Shin-Uwagoromo); the other 18 as OSM has them.
  Colours from `line_colour_search.py` (closest pair 18.1, Meitetsu's two
  lines at 梅坪). Median gap 966 m: standard rings. The opening view frames
  the stations and track (S 35.011 to N 35.179), not the mountain towns.
- **GSI sample (the brief's independent check):** `screen_japan_join.py
  toyota --gsi 50`: 50 answered, median 0 m from the block point, all 50
  within 100 m (max 1 m).
- **Economic Census control: 2.00** Food service pins per 2021 census 飲食店
  establishment (2,729 against 1,364), above the built cities' 1.56-1.92,
  **explained** by Matsuyama's benchmark with Kumamoto's adjustment: official
  / census is 2.86 (3,898 against 1,364), and the list holds 74.9% of the
  official count (2.86 x 0.749 is about 2.14); the placed, de-duplicated pins
  sit below that.
- **Prose proposals for review time:** on the page, "Where a trade name is
  its operator's own name, the dot shows its permit type instead; the barber,
  beauty and laundry registers name an operator only where it is a company,
  so this cannot be checked for the rest." (Kawasaki's sentence with the
  registers in place of the food list); in What Is Excluded, "Temporary and
  stall permits: the city leaves them out of its list, which is why it holds
  about three in four of the restaurant permits the city reports." and "mostly
  rural addresses that name a sub-district without its marker".

### 2026-10-03 - Takamatsu built, the city's food list and three registers with MHLW's notifications

- **Takamatsu built (page 180, notice 119): 7,820 storefronts (Food service
  4,371, Food shops 1,582, Personal services 1,867) around 46 stations on 5
  lines, 71.7% of them in a ring.** Matsuyama's shape: the city's CC BY 4.0
  lists on オープンデータたかまつ as of 2026-08-31 (food 7,372 rows, barbers
  371, beauty 1,188, laundries 332; the registers titled 新規開設 but
  standing), plus MHLW's open data for its 3,349 notifications only (its
  permits add nothing to a city list at 102% of the official count), joined to
  MLIT's address blocks: 7,281 rows at the block (87.4%), 908 at a town
  centre, 125 at MHLW's own point (116 from the chōme tier, 9 from none; one
  default point refused), 19 unplaced; the city's food list fixed in a bucket
  88.7 / 11.1 / 0.2 with the 字甲 rule (`aza_letter`), the brief's figure.
  MHLW's points against the block point: median 46 m, 91.4% within 250 m
  (490 rows), the brief's. 459 repeat permits shown once; 35 city food rows
  dropped for the MHLW notification of the same premises (`SUPERSEDES`).
  MHLW: 2 closed, 2,262 without an address (not placeable), 65 not a
  premises; 532 notification pins (Food shops: konbini, drugstores,
  supermarkets...). City food: 620 not a premises (車 338, 露店：仮設 279,
  露店：引車 3); out by rule 924 (manufacturing 422, 給食 258, 旅館・ホテル
  103 and ラブホ・カプセル 5 (love and capsule hotels, 13b2c280), 露店 62 of which 露店：定置 57 by the written temporary rule (owner,
  2026-09-29), cooking vending 56, 仕出し 23). Kept by 業態 (MHLW's rows): 65
  konbini and 21 supermarkets, to Retail.
- **Held calls, counts touched:** 業態 おかず (181 restaurant permits, 134
  pins) is a deli recognised only by its form and stays Food service;
  複合型そうざい製造業 (1) and 複合型冷凍食品製造業 (4) stay out. The 菓子 /
  そうざい factory share: 28 of 820 (3.4%), kept (owner, 2026-09-24).
- **Two items the build stopped on, resolved in shared code (13b2c280):**
  the privacy check printed 1, the trade name of a cooperative (協同組合)
  that runs two food vehicles under its own name, which the name rule read
  as a person; and 業態 ラブホ・カプセル (5 restaurant permits in love and
  capsule hotels) escaped the inside-accommodation rule. Re-run by the lead:
  the check prints 0, Food service 4,376 -> 4,371.
- **Privacy verdict: publish.** The Japan pass prints 0; 1 pin shows its
  permit type (2 raw rows); 25 raw rows whose trade name is a cooperative's
  own name show it (13b2c280).
- **Rail:** N02-25: Kotoden's 琴平線 (12 of 23), 長尾線 (8 of 16 legally; drawn
  through to 高松築港 over 琴平線's track by a `route` (高松築港, 片原町, 瓦町),
  as its trains run and Kotoden numbers K00/N00 and K01/N01, so 10 in the
  city) and 志度線 (15 of 16), JR Shikoku's 予讃線 (5 of 95) and 高徳線 (9 of 29),
  cut at the city line; no stub. The Yakuri Cable (四国ケーブル 八栗ケーブル, 2
  stations) left out by the funicular rule, a bullet under The lines, not in
  `excluded_stations.csv`. 瓦町's three platforms collapse within 130 m;
  Kotoden's 八栗新道 and JR's 讃岐牟礼, 61 m apart, are separate N02 groups of
  different names and stay apart. Gate 3: Kotoden's station index, in line
  order, gives the Kotohira Line 12, the Nagao Line 10 and the Shido Line 15
  inside the city, exact (53 stations in all, N02's 23 / 16 / 16). 13 stations
  excluded: 4 in Miki, 4 in Ayagawa, 3 in Sanuki, 2 in Sakaide. English
  names: OSM has no object for five Nagao Line stations (花園, 林道, 木太東口,
  西前田, 高田), romanised from the readings in Kotoden's index
  (`OSM_NAME_EN_MISSING`); 5 cited overrides (松島二丁目 to Matsushima-2-Chome,
  the 丁目 rule; 栗林公園 and 栗林公園北口 to -koen; 香西 without the macron;
  琴電屋島 hyphenated as OSM writes 琴電志度). Colours from
  `line_colour_search.py` (closest pair 39.6). Median gap 703 m: standard
  rings.
- **GSI sample (the brief's independent check):** `screen_japan_join.py
  takamatsu --gsi 50`: 50 answered, median 1 m from the block point, 47 within
  100 m, 48 within 500 m, max 1,439 m.
- **Economic Census control: 2.11** Food service pins per 2021 census 飲食店
  establishment (4,371 against 2,071), above the built cities' 1.56-1.92,
  **explained** by Matsuyama's benchmark: the list is 102% of the official
  5,439 permits, official / census 2.63, and the map ratio sits below it. The
  業態 the brief asked to read: 飲み屋 (875 rows, 871 pins) and その他 (412
  rows, 398 pins) are ordinary 飲食店営業 permits at fixed premises (bars and
  unclassified restaurants), counted; repeat permits at one premises are
  already shown once, so neither inflates the map with duplicates.
- **Prose proposals for review time:** on the page, "The Nagao Line's trains
  run on to Takamatsu-Chikko over the Kotohira Line's track, and it is drawn
  along it."; "...station names in English are from OpenStreetMap and the
  railway's own station list." (Toyama's form); "...where that fails for a
  ministry filing, the dot sits at the ministry's own coordinates, and
  otherwise at its district's center." (Kitakyushu's and the template's
  joined). In What Is Excluded, "(much of the city outside the center has no
  block addresses)".

### 2026-10-03 - Nishinomiya built, the city's food list and three registers

- **Nishinomiya built (page 179, notice 118): 5,527 storefronts (Food service
  3,645, Food shops 664, Personal services 1,218) around 22 stations on 7
  lines, 89.3% of them in a ring.** The city's PDL 1.0 lists on its portal
  (food 5,648 rows as of 2026-08-31; barbers 204, beauty 875, laundries 40
  general and 107 pick-up as of 2026-09, each register read from its sheet of
  the shared workbook through `config.source_rows`), joined to MLIT's address
  blocks for the one municipality: 5,647 rows at the block (99.1%), 49 at a
  town centre, 1 unplaced; food fixed in a bucket 99.0 / 1.0 / 0.0, the
  shared-code pass's figure. 169 repeat permits shown once. Not a premises:
  977 (901 西宮市内一円 vehicles and stalls, whose addresses carry plates and
  never reach the map; 76 with no address). Out by rule: 166 manufacturing and
  other non-counter types, 34 cooking vending machines. Restaurants against
  the official count: 4,677 rows against e-Stat's FY2024 4,505, 104% (the
  brief's).
- **Laundries kept and disclosed (owner, 2026-10-02):** 147 of the official
  237 (62%), the page's bullet the brief's sentence.
- **Held calls, counts touched:** 複合型そうざい製造業 (3 rows) stays out. No
  deli by its form alone (the food list has no 業態 column). The 菓子 /
  そうざい factory share: 22 of 495 (4.4%), kept (owner, 2026-09-24).
- **Privacy verdict: publish.** `check_personal_exposure.py nishinomiya`: the
  Japan pass prints 0; 1 pin shows its permit type (2 raw food rows, the
  brief's). 開設者住所 and 開設者電話番号 never selected.
- **Rail:** N02-25: Hanshin's 本線 (7 of 33) and 武庫川線 (4 of 4), Hankyu's
  神戸線 (2 of 17), 今津線 (5 stations; its two services, 宝塚-西宮北口 and
  西宮北口-今津, drawn as the one public line as N02 files it) and 甲陽線 (3 of
  3), JR's 東海道線 (the JR Kobe Line, 3 of 59) and 福知山線 (the JR Takarazuka
  Line, 2 of 30), cut at the city line; the three short urban stretches drawn
  as cut (owner, 2026-10-02). Interchanges collapsed: 武庫川 140 m, 今津 117 m,
  西宮北口 76 m, 夙川 45 m. JR's and Hanshin's 西宮 are separate stations, so
  step 1 appends their operators. Gate 3: Hanshin's station index gives the
  Mukogawa Line 4, Hankyu's the Koyo Line 3, exact. 17 stations excluded: 6
  in Takarazuka, 4 in Amagasaki, 4 in Ashiya, 2 in Kobe's Higashinada Ward, 1
  in its Kita Ward. English names in Hiroshima's style: 5 cited overrides
  (阪神国道, 甲子園口, 甲東園 without OSM's macrons; 武庫川団地前 and
  鳴尾・武庫川女子大前 with -mae); the other 17 as OSM has them. Colours from
  `line_colour_search.py` (closest pair within 500 m 19.0, Hanshin Main / JR
  Kobe; anywhere 15.6). Median gap 684 m: standard rings.
- **Economic Census control: 2.33** Food service pins per 2021 census 飲食店
  establishment (3,645 against 1,567), above the built cities' 1.56-1.92 and
  explained as the brief explains it (2.32 there): a complete list, inside the
  complete lists' band (Kobe 2.38), below official / census (4,505 against
  1,567, 2.87).
- **Prose proposals for review time:** none beyond the brief's laundry
  sentence, which the owner's call approved with it. The notice's
  "Processed by this project, which selected ..." follows Toyama's approved
  notice form (PDL's "by whom").

### 2026-10-03 - Himeji built, the city's food list and three registers

- **Himeji built (page 178, notice 117): 8,482 storefronts (Food service
  5,601, Food shops 1,008, Personal services 1,873) around 31 stations on 6
  lines, 67.2% of them in a ring.** The city's CC BY 4.0 lists on its CKAN
  as of 2026-09-10 (food 8,347 rows, barbers 380, beauty 1,336, laundries
  189), joined to MLIT's address blocks for the one municipality: 7,167 rows
  at the block (81.7%), 1,583 at a town centre (18.1%), 18 unplaced; food
  fixed in a bucket 81.6 / 18.3 / 0.2, the shared-code pass's figure with
  the 甲乙丙 rule (`kou_bare`; the brief's 79.4 / 17.9 / 2.7 before it). 268
  repeat permits shown once. Not a premises: 1,164 (市内一円: 773 露店
  stalls, 388 restaurant vehicles, 3 fish vans); out by rule: 298
  manufacturing and other non-counter types ("no rule"), 22 露店 stalls at a
  listed address (temporary / mobile). 飲食店営業（住宅宿泊事業） (1) reads
  Food service, as the brief says. Restaurants against the official count:
  6,893 restaurant rows against e-Stat's FY2024 6,706, 103% (the brief's).
- **「市条例第３条第２項該当」 (4 barbers, 182 beauty salons) counted as ordinary
  shops.** The ordinance's text is behind g-reiki, which refuses this machine,
  WebFetch and the browser pane (403). The city's own facility standards
  (美容所の開設手続きについて, R7.4.24) carry one exception: a hot-water
  hair-washing basin is not required where a premises does no hair work and
  there is no hygiene obstacle. The flagged salons' trade names fit it
  (keyword counts: 49 eyelash, 9 makeup, 7 nail and 23 hair words among
  182, against 10, 21, 1 and 624 among the 1,154 unflagged). Each is a
  美容所 / 理容所 inspected and confirmed at a fixed address.
- **Held calls, counts touched:** 複合型そうざい製造業 (3 rows) stays out
  ("no rule"), and 複合型冷凍食品製造業 (2) with it. No deli recognised only by
  its form: the list has no 業態 column. The 菓子 / そうざい factory share: 26
  of 684 (3.8%), kept (owner, 2026-09-24). クリーニング所 一般 / 取次所
  指定洗たく物取扱施設 (17 and 7, laundries also cleared for designated items
  such as bedding) counted as laundries.
- **Privacy verdict: publish.** `check_personal_exposure.py himeji`: the
  Japan pass prints 0; 3 pins show their permit type (11 raw food rows; 7
  of the brief's 18 are cooperatives' own names, shown, a cooperative (組合) is no person for the name rule, 13b2c280; the rest
  stalls, vehicles or repeats). 氏名, every row's
  operator, read in memory by the name rule only.
- **Rail:** N02-25, cut at the city line: JR West's 山陽線 drawn as two
  routes meeting at 姫路, the JR Kobe Line (東姫路, 御着, ひめじ別所, to 曽根 in
  Takasago) and the Sanyo Line (英賀保, はりま勝原, 網干), as JR West signs
  them; the Sanyo Line's route ends at 網干 because the next station, 竜野, is
  beyond the 3 km step 1 draws past the city line (`DRAW_BEYOND_M`); the
  播但線 (7 of 18 inside) and 姫新線 (4 of 36); Sanyo Electric's 本線 (9 of 43)
  and 網干線 (7 of 7, wholly inside). The Shinkansen's 姫路 dropped. 飾磨 one N02
  group for both Sanyo lines; JR 姫路 and 山陽姫路 apart (separate groups).
  Gate 3: Sanyo Electric Railway's station index names all 15 in-city
  stations, Main Line 9 and Aboshi Line 7, exact. 10 stations excluded: 4 in
  Takasago, 3 in Tatsuno, 2 in Kamikawa, 1 in Fukusaki. English names in
  Hiroshima's style: 5 cited overrides (京口, 香呂, 太市, 大塩 without OSM's
  macrons; 山陽姫路 hyphenated as OSM writes 山陽網干 and 山陽天満); the other 26
  as OSM has them. Colours from `line_colour_search.py` (closest pair 18.9,
  Sanyo's two lines at 飾磨). Median gap 1,377 m: standard rings.
- **Economic Census control: 2.44** Food service pins per 2021 census 飲食店
  establishment (5,601 against 2,297), above the built cities' 1.56-1.92 and
  explained as the brief explains it (2.41 there): a complete list, inside
  the complete lists' band (Kobe 2.38), and below official / census (6,706
  against 2,297, 2.92), Matsuyama's benchmark.
- **Prose proposals for review time:** none on the page (every sentence is
  the skill's template or Kitakyushu's Shinkansen form). In What Is Excluded:
  "among them 186 salons confirmed without a hair-washing basin because they
  do no hair work"; "the central district's towns are a few blocks each, and
  rural 大字 have no block data."

### 2026-10-03 - Yokosuka built, the city's food list and four registers

- **Yokosuka built (page 177, notice 116): 4,544 storefronts (Food service
  2,919, Food shops 497, Personal services 1,128) around 21 stations on 3
  lines, 77.8% of them in a ring.** The city's CC BY 4.0 lists on BODIK as of
  2026-08-31 (food 4,172 rows, barbers 251, beauty 745, laundries 49 general
  and 95 pick-up), each fetched through its CKAN resource's current URL
  (`SOURCE_RESOURCES`), joined to MLIT's address blocks for the one
  municipality: 4,516 rows at the block (97.0%), 132 at a town centre, 6
  unplaced; food fixed in a bucket 96.5 / 3.4 / 0.1, the brief's figures.
  104 repeat permits shown once. Out by rule (詳細業種 read as the form,
  `form_cols`): 129 canteens (給食), 57 snack bars and cabarets, 44 caterers
  (仕出し屋), 35 inside inns, 20 vending, 133 manufacturing and other
  non-counter types ("no rule"). Not a premises: 240 (103 vehicles, 89
  屋台型臨時営業 stalls, 48 with no address or a citywide one). Restaurants
  against the official count: 3,448 飲食店営業 rows against e-Stat's FY2024
  3,461 in force, 99.6% (the brief's).
- **Held calls, counts touched:** 詳細業種 総菜屋 (29 restaurant permits) stays
  Food service and 複合型そうざい製造業 (5 rows, 1 a 食肉処理 form) stays out,
  at the built cities' reading pending the owner's cross-city call. The one
  クラブ又はナイトクラブ is Food service: the hostess rule (スナック 55,
  キャバレー 2) does not take it, and nightclubs are kept (category_rules R5).
  The 菓子 / そうざい factory share: 12 of 367 (3.3%), kept (owner,
  2026-09-24).
- **Privacy verdict: publish.** `check_personal_exposure.py yokosuka`: the
  Japan pass prints 0; 1 pin shows its permit type (a beauty salon); the
  brief's second, a laundry pick-up shop, is run by a cooperative under its
  own name and shows it (a cooperative (組合) is no person for the name rule, 13b2c280). The food list names company
  operators only (申請者氏名 beside 申請者法人名称; Toyama's accepted position);
  the registers name every operator (営業者氏名・法人名称).
- **Rail:** N02-25, Keikyu's 本線 (11 of 50 inside) and 久里浜線 (7 of 9) and
  JR's 横須賀線 (4 of 9), cut at the city line; no Shinkansen, no stub. 堀ノ内
  is one N02 group for both Keikyu lines; 京急久里浜 and JR's 久里浜 (224 m, the
  closest pair) stay apart. Gate 3: Keikyu's station list gives the Main
  Line's 追浜-浦賀 11 and the Kurihama Line's 堀ノ内-津久井浜 7 inside the
  city, exact. 5 stations excluded: 2 in Yokohama's Kanazawa Ward, 2 in Miura,
  1 in Zushi. English names: OSM's 21 as they stand (signage style, no
  macron, no override; OSM's own hyphenation, as Yokohama's and Kawasaki's
  Keikyu names). Colours from `line_colour_search.py` (closest pair 18.1,
  Keikyu's two lines at 堀ノ内). Median station gap 840 m: standard rings.
- **Economic Census control: 2.13** Food service pins per 2021 census 飲食店
  establishment (2,919 against 1,373), above the built cities' 1.56-1.92,
  **explained by Matsuyama's benchmark** (official / census): e-Stat's 3,461
  permits in force against the census's 1,373 is 2.52, and the list is 99.6%
  of the official count; the map's 2,919 pins (fixed, placed, one per
  premises) are 84% of it, so the map ratio sits below official / census, as
  in every complete list. The ratio is the permit structure, not the join.
- **Prose proposals for review time** (no approved template covers them): on
  the page, "Where a trade name is its operator's own name, the dot shows its
  permit type instead; the food list names an operator only where it is a
  company, so this cannot be checked for the rest." (Kawasaki's proposal,
  reused); in What Is Excluded, "The one nightclub (クラブ又はナイトクラブ) is
  Food service, as nightclubs are elsewhere."

### 2026-10-03 - The name rule treats a cooperative as no person (opt-in); love and capsule hotels are accommodation

- **A cooperative or union operator (組合) is not a person for the name
  rule, on the wave-2 cities (`WAVE2_RULES` gains "coop").** Takamatsu's
  privacy check printed 1: a 協同組合 runs two food vehicles under its own
  name, the rule read the cooperative as an individual (KYOTO_CORP lists
  companies only), and its trade name, on an MHLW notification elsewhere,
  counted as an operator's own name shown. Measured on the built cities, the
  same gap withholds co-op shops' real trade names as if they were people's:
  Kobe 7 (生活協同組合 6, 漁業協同組合 3, one more), Kyoto 5, Fukui 5, Toyama
  4, Sapporo 3, Fukuoka 3, Osaka 1, Hiroshima 1. Withholding a business name
  is the safe direction, and changing it moves eight built maps, so it is
  opt-in like the join rules: an option for the owner at review time.
  `same_person` reads `NOT_A_PERSON` (KYOTO_CORP plus 組合) only with "coop",
  so Kyoto's de-duplication key never moves; `check_personal_exposure.py`
  reads the city's rules too. Takamatsu: names withheld 12 -> 1, the check
  prints 0.
- **`japan_eigyo`'s "inside accommodation" reads ラブホ and カプセル** (love
  and capsule hotels), as type and as 業態: Takamatsu's 業態 「ラブホ・カプセル」
  (5 restaurant permits) had read as Food service. No built city moved.
- **Proven:** the 20 built Japanese cities' step 2 byte-identical, baselines
  included.

### 2026-10-03 - Two more shared-code items from the agents: old-law （旧） types, and a left-out branch's stations counted

- **`japan_eigyo.normalise()` drops a leading （旧）**, Higashiosaka's spelling
  of an old-law permit (（旧）菓子製造業): the anchored Retail rules missed it,
  and 108 rows in term (菓子 59, 食肉販売 19, 魚介類販売 15, そうざい 15) fell
  to "no rule" though （旧）飲食店営業 was already read as a restaurant.
  Agent C found it; the brief's "Food retail 691" missed them too.
- **`japan_step1` writes a left-out branch's in-city stations to
  `excluded_stations.csv`** where the branch carries `excluded_reason` (and
  `excluded_lines`): Shimonoseki's San'in Line beyond 小串, left out by the
  owner on 2026-10-02 for frequency (JR West's timetable, revised
  2026-10-03: 11 trains a day each way on weekdays, 12 at weekends, gaps up
  to 2 h 16 min). The reason names the 15-minute test, so What Is Excluded
  counts them as too infrequent, as Aarhus's; whether a JR stretch left out
  for frequency becomes a row of `docs/category_rules.md`'s station scope is
  for the owner (staging's recommendation was made for Shimonoseki alone).
  Sightseeing lines left out whole are still not written there.
- **Proven:** a step-2 snapshot of the 20 built Japanese cities is
  byte-identical, baselines included; the step-1 change is opt-in (no built
  branch carries `excluded_reason`).

### 2026-10-03 - Kawasaki built, the city's food list and three registers

- **Kawasaki built as wave 2's pilot (page 176, notice 115): 11,894
  storefronts (Food service 7,811, Food shops 1,252, Personal services 2,831)
  around 52 stations on 16 lines, 83.5% of them in a ring.** The city's
  monthly CC BY lists as of 2026-08-31 (food 14,022 rows, barbers 558, beauty
  1,763, laundries 533), joined to MLIT's address blocks for the 7 wards:
  12,160 rows at the block (98.7%), 152 at a town centre, 2 unplaced. 418
  repeat permits shown once. Out by rule: 621 canteens, 256 manufacturing and
  other non-counter types, 155 caterers, 53 inside hotels, 44 vending, 15
  mahjong parlors, 10 temporary, 9 linen suppliers. Not a premises: 2,455
  trucks and temporary stalls (licensed for all of Kanagawa, no address) and
  944 permits whose holders had their address withheld (625 fixed
  restaurants of 8,516, 7.3%, "one in fourteen" on the page; the brief's 798
  of 9,812 counted every restaurant-type row).
- **The 301 delis on a restaurant permit (飲食店（そうざい店）) are Food shops**,
  the kit's call on the そう菜店 precedent; 弁当屋 (528) stays Food service.
  The 菓子 / そうざい factory share: 45 of 975 (4.6%), kept (owner,
  2026-09-24).
- **Privacy verdict: publish.** `check_personal_exposure.py kawasaki`: the
  Japan pass prints 0, no pin shows its permit type; 5 rows in the raw files
  have a trade name that is the operator's own name and none reaches a pin.
  The food list names company operators only (Toyama's accepted position);
  the registers name every operator.
- **Rail:** N02-25 with JR East's 東海道線 drawn as Yokohama's four services
  (Keihin-Tohoku, Tokaido, Yokosuka, Sotetsu-JR Link; each a route, its next
  station outside the city as an end), and Tokyu's Meguro and Oimachi Lines
  as routes over 東横線 and 田園都市線 (Tokyo draws both; here their trains
  run on their own pairs of tracks beside the Toyoko and Den-en-toshi
  lines), the brief's alternative being one page bullet. The Nambu Branch
  (尻手-浜川崎) split off 南武線 by a branch walk (5,028 m); the Tsurumi Line's
  大川 branch drawn with its line, as Yokohama draws the Tsurumi Line whole.
  武蔵小杉's Yokosuka Line platform joined to its station (`GROUP_JOIN`; the
  group spreads 397 m, `COLLAPSE_MAX_SPREAD_M` 450). 尻手's platform lies
  inside the city line, so it is ringed. Keikyu Main (2 of 50) and Keio
  Sagamihara (2 of 12) drawn as cut (owner, 2026-10-02). Gate 3: Keikyu's
  list gives the Daishi Line 7, exact. 49 stations excluded: 22 in Yokohama,
  27 in Tokyo (named through `N03_NEIGHBOR_PREFS`). Mizonokuchi (Tokyu) and
  Musashi-Mizonokuchi (JR) are 132 m apart and separate N02 groups of
  different names: kept apart. English names: OSM's 52 as they stand,
  signage style with no macron, so no override. Colours from
  `line_colour_search.py` (closest pair within 500 m 18.1).
- **Economic Census control:** 7,811 Food service pins against 4,212 飲食店
  establishments, 1.85 (川崎区 2.22, 麻生区 1.55), inside the built cities'
  1.56-1.92.
- **Prose proposals for review time** (no approved template covers them):
  on the page, "Where two services share one route (...), each is drawn
  along it."; "About one restaurant in fourteen in Kawasaki chose not to
  have its address published in the city's list and is not on this map.
  Where they are is not known." (the MHLW template's sentence, reworded for
  a city list); "The Shinkansen is not drawn; it crosses the city without a
  station."; in What Is Excluded, "The 301 delis that hold a restaurant
  permit (飲食店（そうざい店）) are Food shops." and the same Shinkansen
  sentence.

### 2026-10-03 - Japan wave 2: the shared-code pass, gated so no built city moves

- **Every wave-2 brief's shared-code item landed in one pass, and the new
  join rules are switched on per city: the fourteen wave-2 cities opt in
  (`japan.CITIES[...]["rules"] = japan_register.WAVE2_RULES`), the 20 built
  Japanese cities do not.** Measured first with every rule global: the rules
  moved nine built cities, mostly for the better (unplaced rows: Fukuoka
  92 -> 29, Hiroshima 152 -> 7, Kumamoto 62 -> 14, Matsuyama 84 -> 63;
  Kōchi 13 rows chōme -> block), and Fukuoka's "福岡市内" rows (3) became
  "not a premises". The kit requires the built cities' drift checks to stay
  clean, and a built city's output changes only at a review time that
  re-renders it, so each rule is named and opt-in: `oaza` (a 大字 dropped on
  both sides: Yokkaichi, Shimonoseki), `aza_letter` (字甲 read as 甲:
  Takamatsu), `kou_bare` (Himeji's 甲 / 乙 / 丙 地番, the bare town's number
  where MLIT gives it one place, its centroid where the number's rows lie
  over 500 m apart), `chome_missing` (Toyota's 浄水町1-5丁目 at the 大字
  centroid), `machi` (Nara's 宝来町一丁目 / 宝来1丁目 and 北京終 / 北京終町),
  `citywide` (Kurume's 「久留米市内」 rows are not premises) and `form_cols`
  (業態 read from 業態, Yokosuka's 詳細業種 or Sasebo's 種目). Turning them
  on for the built cities is a separate, measured option for review time.
- **Unconditional (they moved no built city):** column spellings
  (`ADDR_COLS` +6, `NAME_COLS` +5, `TYPE_COLS` + 営業種目 and 区分,
  `OPERATOR_COLS` +11); `wareki_date` reads Sasebo's `R 8. 5.31`;
  `japan_eigyo` reads Kawasaki's 飲食店（sub-type） with its carve-outs
  (給食施設, 学校給食炊飯, まあじゃん屋等, 短期営業), takes そうざい店 and a
  leading そうざい屋 to Retail (the そう菜店 precedent), reads Nara's old-law
  restaurant sub-types (軽飲食, 一般食堂, 居酒屋 and ten more; the first
  listed decides a combination) and 簡易菓子製造業; `rebuilt_register()`
  (Higashiōsaka's full list plus months: 7,067 rows read, 6,709 after
  de-duplication, 6,521 in term on 2026-08-31, the brief's figures exactly);
  `japan_step2.datum_guard()` stops `OWN_POINT_FALLBACK` on a publisher whose
  points sit a median over 200 m from the block point (Higashiōsaka's Tokyo
  Datum, 448 m); `japan_fetch.current_url()` reads a renamed file's current
  link from its page (`SOURCE_LINKS`: Kawasaki, Ōtsu) or a CKAN resource's
  current URL (`SOURCE_RESOURCES`: Yokosuka, Toyota);
  `japan_step1.n03_municipalities()` also reads `config.N03_NEIGHBOR_PREFS`'
  N03 files, so a station beyond the prefecture line is named, not filed as
  "another prefecture" (Kawasaki's 27 in Tokyo; opt-in, so Kitakyushu's
  Shimonoseki row is unchanged).
- **Proven:** `drift_check.py` on the 20 built Japanese cities, run through
  the heavy-job gate on this code: **zero drift**, every baseline unchanged
  (measured peak 4.54 GB). A step-2 snapshot of the same 20 cities, old code
  against new, was byte-identical too.
- **Two kit items held at the built cities' reading, a cross-city call for
  the owner at review time:** `複合型そうざい製造業` stays out (the import-time
  pin) and a deli by its 業態 alone (総菜屋, 惣菜店, そうざい屋 as the form of a
  restaurant permit) stays Food service. Counting them moved eight built
  cities (Kobe 8, Kyoto 6, Osaka 12, Sapporo 10, Sakai 12 and 4, Kagoshima 2,
  Okayama 1, Fukui 1; about 55 pins). The wave-2 rows they touch: Himeji 3,
  Kawasaki 6, Yokosuka 5 and its 総菜屋 29, Sasebo's 飲食店惣菜 5.
- **Nara's ケ/ヶ fix needed nothing new**: `VARIANTS` already reads ヶ as ケ;
  the brief's examples (杉ケ中町, 秋篠梅ケ丘町) are towns MLIT's file lacks.
- **The Minato control reproduces** (block 98.0 / chōme 0.2 / none 1.8), and
  each wave-2 city's tiers on fixed premises in a bucket
  (`screen_japan_join.py <slug> --bucketed`, new) match or beat its brief:
  Kawasaki 98.7 / 1.3 / 0.0, Yokosuka 96.5 / 3.4 / 0.1, Himeji 81.6 / 18.3 /
  0.2 (brief 79.4 / 17.9 / 2.7 before its rule), Nishinomiya 99.0 / 1.0 /
  0.0, Takamatsu 88.7 / 11.1 / 0.2, Toyota 78.5 / 16.2 / 5.3, Yokkaichi
  88.8 / 8.9 / 2.4, Ōtsu 94.7 / 5.3 / 0.0, Nara 89.2 (old-law) and 89.5
  (registers, brief 88.6), Hamamatsu 94.9 / 5.1 / 0.0, Higashiōsaka 99.6 /
  0.4 / 0.0, Kurume 87.5, Sasebo 88.5 (MHLW) and 90.5 (old law), Shimonoseki
  88.1 / 11.3 / 0.6.
