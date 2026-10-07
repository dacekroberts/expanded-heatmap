# DECISIONS drafts - East-1 (`worktree-japan-east-1`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30). The build
plan is `docs/build_plan_2026-10-07.md`; pages 210-221, notices 157-168.

## Parked calls

1. **Higashimurayama's line colours (taste; the city is built and committed with set A).** Five Seibu lines meet in the city. Seeded with Seibu's one corporate blue, the colour search lands three of them near grey (Seibuen #7898A8, Tamako #788090, Haijima #506860): it passes the project's thresholds, but only just (closest pair 18.3 within 500 m against a floor of 18, 11.2 anywhere against 10). Set B seeds each line apart (Shinjuku #08A0C0, Kokubunji #C88800, Seibuen #9040C0, Tamako #A06030, Haijima #805878, Musashino #F05820): closest pair 33.2, dark labels 6 of 6. *Recommend B*, unless Seibu's own per-line colours can be read from its site, in which case seed from those and re-run. Tradeoff: B separates the lines far better on the map; its hues are not the operator's (the page already says the colours are the project's own). The same choice applies to Nishitōkyō's Ikebukuro Line seed (#F5A200, a seed chosen at build, not read from Seibu).

## Page-text proposals (review time)

Sentences on the East-1 pages that no approved template covers
(`docs/city_page_format.md` section 6), each drafted from the brief's owner
calls:

- **Higashiyamato, the ledgers' window and the shares (calls 109, 187-189):**
  "The ledgers hold new permits only since August 2019 and leave out premises
  whose operators asked not to be published, so they are not complete.
  Against Tokyo's official counts for the end of March 2025, they hold 397 of
  528 (75%) of the city's restaurants, 44 of 45 (98%) of its barbers, 80 of 88
  (91%) of its beauty salons and 19 of 21 (90%) of its laundries." The figures
  are read from `outputs/higashiyamato/official_shares.json`, never typed.
- **Higashiyamato, the sources line:** "From the Tokyo Metropolitan
  Government's ledgers of food-business permits and notifications, barbers,
  beauty salons and laundries for the Tama area (as of August 31, 2026), and
  the Ministry of Health, Labour and Welfare's open data for the premises the
  ledgers lack (downloaded October 6, 2026). A premises in both lists appears
  once." (Sasebo's two-list wording, adapted.)
- **Higashiyamato, the notifications:** "Shops that only notify rather than
  hold a permit, such as supermarkets, convenience stores and greengrocers,
  appear where they notified since June 2021, so that part of the layer is
  partial." (call 127b's partial layer, Ichinomiya's precedent.)
- **Higashiyamato, the Seibu Haijima Line:** "The Seibu Haijima Line has one
  station of its own in the city, Higashiyamatoshi, and meets the monorail at
  Tamagawa-Josui on the city line."
- **Nishitōkyō (page 211, notice 158) and each Tama city after it** carry the
  same sentences with the city's own figures, read from its
  `official_shares.json`; only the Seibu Haijima sentence is Higashiyamato's
  alone.
- **Notice 157's processing sentence:** "The ledgers hold new permits since
  August 2019 and leave out premises whose operators asked not to be
  published; the ministry's list holds only filings whose applicants agreed
  to publish them. Neither is complete." The credit itself follows the Tokyo
  Open Data Terms' §2(1)イ form the brief quotes; staging's record holds the
  verdict but no exact wording, so the wording is flagged for confirmation.

### 2026-10-07 - Higashimurayama built

- **Higashimurayama built on the Tama ledgers and MHLW's Tokyo filings, cut by address: 1,432 storefronts (Food service 772, Retail 409, Personal services 251) at 8 stations, 1,153 within a ring (80.5%).** The brief's 15 checks held. Page 213, notice 160. Rows in the city: food permits 1,113, notifications 371, barbers 54, beauty 148, laundry 50, MHLW 211. Out before the buckets: 15 area-wide addresses, 1 closed MHLW row; not a storefront 289 (institutional catering 149, no rule 82, hostess venues 31, 仕出し 12, vending 12, inside accommodation 3). The join: block 1,641, MHLW's own point 1, unplaced 0; MHLW's points a median 37 m from the block point (156 rows). 149 MHLW rows repeat a ledger premises (56 permits, 93 notifications); 78 repeat permits shown once. On the map 99.9% at the block. 菓子 / そうざい 128 rows, 14 factory-like (10.9%), kept. MHLW adds 24 pins (15 restaurants), so the buckets differ from the brief's ledger-only 771 / 416 / 252.
- **The shares reproduce the brief exactly:** restaurants 916 of 1,023 (89.5%), 705 at 2025-03-31 (68.9%); barbers 54 of 62 (87.1% at the date too); beauty 148 of 162, 139 at the date (85.8%); laundry 50 of 54 (92.6%).
- **Rail: six lines drawn**, the Seibu Shinjuku (2 stations inside), Kokubunji (1), Seibuen (2, wholly inside), Tamako (4) and Haijima (1) lines and JR East's Musashino Line (1, 新秋津); the three one-station lines are JR or private stubs, drawn as cut (the standing call). **The Seibu Yamaguchi Line (the Leo Liner, AGT, N02 class 16) is left out** (calls 54 and 92): its one station, 多摩湖, shares an N02 group with the Tamako Line's, which keeps the ring; nothing goes to `excluded_stations.csv`. The Seibu Ikebukuro Line is not drawn: 秋津 is 12 m outside the city line (清瀬市). `N03_NEIGHBOR_PREFS = ("11",)` names 所沢市's stations. Gate 3 exact on all six (Seibu 7, JR East 1). 13 stations beyond the line (小平市 7, 所沢市 3, 国分寺市 1, 東大和市 1, 立川市 1). Median gap 810 m, standard rings. English names from OSM `name:en`, no override. Colours: parked call 1.
- **Census control 1.91**, inside the built range (772 of 404).
- **Privacy verdict: publish.** The Japan pass prints 0 of 1,432; the 1 trade name equal to its operator's own name is withheld and its pin shows its permit type.
- **Page proposal:** "The Seibu Yamaguchi Line (the Leo Liner) is not drawn: its one station in the city, Tamako, is a station of the Tamako Line, which keeps the ring." (Fukuoka's and Toyama's left-out-line bullet, adapted.)

### 2026-10-07 - Tama built

- **Tama built on the Tama ledgers and MHLW's Tokyo filings, cut by address: 1,419 storefronts (Food service 664, Retail 504, Personal services 251) at 6 stations, 1,162 within a ring (81.9%).** The brief's 13 checks held. Page 212, notice 159. Rows in the city: food permits 1,005, notifications 496, barbers 53, beauty 164, laundry 38, MHLW 316. Out before the buckets: 8 area-wide addresses, 1 permit whose condition names a vehicle, 2 not a premises; not a storefront 255 (institutional catering 137, no rule 47, vending 22, hostess venues 21, temporary or mobile 12, 仕出し 10, inside accommodation 4, mail order 1, linen supply 1). The join: block 1,745, town-chōme 48, own point 12, unplaced 1 (落川 2丁目 35, written for 多摩中央公園, which stands in 落合: likely the publisher's slip, left unplaced). MHLW's points a median 34 m from the block point. 267 MHLW rows repeat a ledger premises (82 permits, 185 notifications); 156 repeat permits shown once. On the map: block 1,371, town-chōme 46, own 2 (96.6% at the block). 菓子 / そうざい 157 rows, 23 factory-like (14.6%), kept.
- **The shares reproduce the brief exactly:** restaurants 839 of 931 (90.1%), 667 at 2025-03-31 (71.6%); barbers 53 of 56 (94.6%); beauty 164 of 169, 154 at the date (91.1%); laundry 38 of 40, 36 at the date (90.0%).
- **The shared Tama cut corrected** (`tokyo_tama.city_rows`): it raised on two rows naming 多摩市 after other cities, both areas rather than premises (the notification 「稲城市周辺、多摩市周辺、日野市周辺」 and MHLW's 「稲城市、及び、日野市、多摩市内一円」). An address with the area words step 2 already reads (AREA_WORDS, 一円, 市内) is now skipped; any other mention still raises. Higashiyamato's and Nishitōkyō's maps are unchanged: neither holds such a row, and both re-run at zero drift.
- **Rail: three lines drawn**, the Odakyu Tama Line (3 stations inside), the Keio Sagamihara Line (2) and the Keio Line (1, 聖蹟桜ヶ丘, a private one-station stub drawn as cut). **The Tama Toshi Monorail is left out** (calls 54 and 92): its one station, 多摩センター, is its own N02 group 187-197 m from the Keio and Odakyu stations, which keep the ring. The Keio and Odakyu stations at 永山 and 多摩センター stand 38 m apart and are kept apart, as the brief decided. **Gate 1 then reads a 38 m median**, so `SPACING_MIN_M = 30` is set (Tbilisi's precedent of a floor under real stations close together, both in the operators' counts), and the spacing rule is read by place: the nearest other place is a median 1,856 m away, so standard rings. Gate 3 exact (3, 2, 1). `N03_NEIGHBOR_PREFS = ("14",)` names Kawasaki's stations. 15 stations beyond the line within the drawing window (府中市 4, 川崎市麻生区 4, 日野市 3, 八王子市 2, 町田市 1, 稲城市 1). One cited override: 京王永山 as "Keio-nagayama" (OSM's "Keio-Nagayama"), the style of Keio's own names here and Kawasaki's Keio-inadazutsumi. Colours: Odakyu Tama #08A0C0 (45.1 against Retail), Keio Sagamihara #F000B8, Keio #F848D0; closest pair within 500 m 110.1, anywhere 11.1 (the two Keio lines, which meet only beyond the city).
- **Census control 1.98**, above the built range; without the 40 弁当屋 pins 1.87, by distinct address 1.72 (141 pins share an address). As Nishitōkyō's: takeaway counters and buildings of several restaurants; recorded.
- **Privacy verdict: publish.** The Japan pass prints 0 of 1,419; the raw files' 1 trade name equal to an operator's own name is not among the storefronts.
- **Page proposal:** "The Tama Toshi Monorail is not drawn: its one station in the city, Tama Center, stands beside the Keio and Odakyu stations of the same name, which keep the rings."

### 2026-10-07 - Nishitōkyō built

- **Nishitōkyō built on the same Tama ledgers and MHLW's Tokyo filings as Higashiyamato, cut by address: 1,936 storefronts (Food service 982, Retail 566, Personal services 388) at 5 stations, 1,619 within a ring (83.6%).** The brief's 17 checks held (2026-10-07). Page 211, notice 158. Rows in the city: food permits 1,446, notifications 511, barbers 80, beauty 236, laundry 75, MHLW 326. Out before the buckets: 8 area-wide addresses; not a storefront 400 (institutional catering 233, no rule 86, vending 30, hostess venues 29, 仕出し 13, temporary or mobile 4, linen supply 3, inside accommodation 2). The join: block 2,264, MHLW's own point 2, unplaced 0; MHLW's points a median 48 m from the block point (221 rows, 94.6% within 250 m). 239 MHLW rows repeat a ledger premises (101 permits, 138 notifications); 134 repeat permits shown once. On the map: block 1,934, own 2 (99.9%). 菓子 / そうざい 194 rows, 5 factory-like (2.6%), kept.
- **The shares, read by the page, reproduce the brief exactly:** restaurants 1,171 of 1,284 (91.2%), 933 at 2025-03-31 (72.7%); barbers 80 of 84, 78 at the date (92.9%); beauty 236 of 256, 226 (88.3%); laundry 75 of 87, 73 (83.9%).
- **Rail:** the Seibu Shinjuku Line (3 of 29) and Seibu Ikebukuro Line (2 of 31), N02-25, main lines cut at the city line. Gate 3 exact against Seibu's counts (3, 2). 7 stations beyond the line (練馬区 3, 小平市 2, 東久留米市 1, 清瀬市 1). Median gap 1,223 m, standard rings. Colours: Shinjuku #08A0C0 (45.1 against Retail), Ikebukuro #D08000; pair 104.1. OSM `name:en` for all 5, no override.
- **Census control 2.23, above the built cities' 1.56-1.92 (the brief: 2.21), and the brief's readings tested:** without the 67 弁当屋 pins it reads 2.09; counting distinct addresses rather than premises, 1.98 (196 pins share an exact address with another restaurant pin: food halls and buildings of several restaurants). Higashiyamato reads 1.62 and 1.59 the same ways. So the excess is mostly takeaway bento counters, which the census files outside 飲食店 and the permit law inside it, and buildings of several premises; recorded, no change made.
- **Privacy verdict: publish.** The Japan pass prints 0 of 1,936; 0 trade names equal an operator's own name; no pin shows its permit type.

### 2026-10-07 - Higashiyamato built

- **Higashiyamato built on the Tokyo Metropolitan Government's five Tama ledgers, cut to the city by address, with MHLW's Tokyo filings the ledgers lack (call 169): 835 storefronts (Food service 410, Retail 276, Personal services 149) at 4 stations, 548 within a ring (65.6%).** The brief's 17 checks held (2026-10-07). Page 210, notice 157. Rows in the city: food permits 603, notifications 269, barbers 44, beauty 86, laundry 19, MHLW 140. Out before the buckets: 2 area-wide addresses, 1 closed MHLW row, 1 vehicle or stall; not a storefront 148 (institutional catering 79, no rule 26, hostess venues 15, vending 9, 仕出し 8, temporary or mobile 7, inside accommodation 2, mail order 2). The join: block 952, town-chōme 44, MHLW's own point 13, unplaced 0; MHLW's points sit a median 48 m from the block point (93 rows, 98.9% within 250 m). 111 MHLW rows repeat a ledger premises (36 permits, 75 notifications) and are shown as the ledger's; 70 repeat permits shown once. On the map: block 793, town-chōme 42 (95.0% at the block). 菓子 / そうざい 70 rows, 1 factory-like (1.4%), kept.
- **The brief's MHLW match was narrower than step 2's.** The brief matched MHLW to the ledgers by (town, number) and found 24 of 36 open permits and 36 of 103 notifications in both. Step 2's `SUPERSEDES` key (town, block, trade name, bucket) finds 111 of 140 rows in both, since the two lists write the same house number differently (1213-6 against 1213番地の6). After it, MHLW adds 2 premises to the map. Rejected: matching on the full house number, which would show the same shop twice.
- **The shares, measured by the build and read by the page (calls 109, 187-189):** restaurants 505 of the yearbook's 528 (95.6%), 397 at its date, 2025-03-31 (75.2%; 108 first permitted after it); barbers 44 of 45 (97.8% at the date too); beauty 86 of 88 (97.7%), 80 at the date (90.9%); laundry 19 of 21 (90.5%). Each reproduces the brief exactly. The notification ledger is left out of the restaurant share (`SHARE_SKIP`): its one row typed 飲食 is a stall 営業とみなされない, which the share's 飲食 test would count (506).
- **Rail:** the Tama Toshi Monorail (3 of 19 stations inside) and the Seibu Haijima Line (1 of 8, 東大和市, a private stub drawn as cut, the standing call), N02-25. 玉川上水's two platforms (107 m) collapse on `N02_005g` to one station inside the city, so step 1 counts it on both lines. Gate 3: the monorail 3 against its own station pages, exact; Seibu's 1 cannot be gated, since the collapsed interchange counts on both lines. 7 stations beyond the line (立川市 5, 小平市 1, 東村山市 1). Median station gap 775 m, so standard rings. Colours from `line_colour_search.py`: monorail #E07800, Seibu #08A0C0 (45.1 against Retail), pair 110.6. English names from OSM `name:en`, no override needed.
- **Census control 1.71** placed Food-service premises per 2021 Economic Census 飲食店 establishment (410 of 240), inside the built cities' 1.56-1.92.
- **Privacy verdict: publish.** `check_personal_exposure.py higashiyamato` with step 2's rules (`japan.city_rules`, Regional-1's one-line fix applied identically): the Japan pass prints 0 of 835; 0 trade names equal an operator's own name in the raw files; no pin shows its permit type. 法人代表者氏名, the operator's address and every phone are dropped at read (call 109).
- **Corrected in the brief's plan, not the brief:** `SOURCE_LINKS` cannot pick the ledgers' CSVs, since the page links each ledger as CSV and Excel and only the link text says which (`shokuhin-todokede-1-7` is the CSV, `shokuhin-kyoka-1-7` the Excel). The five URLs are pinned in `pipeline/countries/tokyo_tama.py`; a new edition is a re-measure.
- **Per call 198, no label tier, region view or label offset was set**; the entry keeps the scaffold's starting offset and region "Japan East" for Cleanup's Japan regions.

### 2026-10-07 - Shared code for the Tama cities: the yearbook's Tama rows, table 19-7, the share at the yearbook's date, and one Tama module (flagged for review)

- **`japan_official.yearbook()` now reads the Tama cities' rows (132xx) as well as the wards', `restaurants()` answers any Tokyo municipality from the yearbook first, and a new `registers()` reads table 19-7 (call 189).** The brief named `official_shares` as where the share is measured (the yearbook's 528), but the reader took wards only and would have stopped the build. A ward reads exactly as before; Hachiōji, built nowhere, now reads 4,898 from the yearbook rather than e-Stat.
- **`japan_step2` gained two opt-in measures: `config.SHARE_DATES` (the share at the official count's date, calls 187-189) and `config.REGISTER_SHARES` (each register against table 19-7).** Both write into `official_shares.json` for the page; off unless a config sets them. Rejected: a city-local calculation in each of eight Tama configs, which the japan-city skill rules out ("anything a second city would also need goes into the shared module"); and parking all eight Tama cities, since the prompt's parked-call rule covers a brief's missing "Shared code" item, and this one was not flagged as one. Flagged here for the owner's review rather than parked.
- **`pipeline/countries/tokyo_tama.py`, new:** the five ledgers and MHLW's Tokyo file, their columns, the call-109 drop, the cut by address prefix that raises on the city's name elsewhere (Itami's and Tsu's rule), the shares' date columns and the catalogue credit, shared by the eight Tama cities.
- **Zero effect on built cities, proved read-only:** each of the 34 cities in `japan.BUILT_BEFORE_FOUNDATION` ran step 2 with `write=False`, its storefronts compared byte for byte with its processed file in the shared `data/` (master's). Not `drift_check.py`, which would rewrite master's processed files from a branch (the shared-data rule). **Result: all 34 identical** (Tokyo 61,317, Osaka 73,011, Kyoto 32,370 storefronts among them; peak 0.66 GB, through `heavy_job.py`). The Tama-only paths run in Higashiyamato's build, which reproduced its brief's shares exactly.
