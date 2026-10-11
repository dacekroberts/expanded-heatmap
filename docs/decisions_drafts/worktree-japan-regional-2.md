# Decisions drafts: Regional-2 (branch worktree-japan-regional-2)

The Regional-2 build session of the A and B build plan
(`docs/build_plan_2026-10-07.md`), phase 2: Shizuoka, Kanazawa, Okazaki,
Aomori, Matsue, Fuji, Matsumoto, Tottori, Yamagata, Kure and Kurashiki, on
pages 258-267 and 306 and notices 205-214 and 216. Newest first; Cleanup folds
these into `DECISIONS.md`.

## Parked calls

Each city's own parked calls and proposals are under its entry below
("Parked calls", "Proposals"). The lead's, by city and letter:

- **Okazaki A: Meitetsu's red on two neighbouring maps.** Okazaki's Meitetsu
  Nagoya Main Line takes the registry's `#E80010`; Toyota's built map draws
  the Meitetsu Mikawa Line in the same `#E80010`, and the two lines come
  within 2 km of each other, so `check_line_identity.py` reports 1 problem
  (CIE76 0.0, under 10). Recommended: a `NEIGHBOUR_EXCEPTIONS` entry, as JR
  East's orange for the Musashino and Chuo lines: Meitetsu signs every line
  in the one red, and the two lines never share a map. Tradeoff: a reader
  moving from Toyota's map to Okazaki's sees one red for two lines. The
  alternative moves Toyota's Mikawa Line (a built map: Cleanup's, with a
  re-render). Nothing was changed; Okazaki is committed with the check
  failing on this one pair.
- **Okazaki B: one BODIK request carried the owner's email address.** The
  Okazaki builder's first `package_show` call (one metadata request to
  `data.bodik.jp`, 2026-10-11) went out with a hand-typed user-agent that
  included the owner's email address; every later request used the
  project's own string. It cannot be recalled. The builders' instructions
  now forbid anything personal in a header or URL. For the owner to know;
  no action recommended.

## Proposals for review time (sentences no template covers)

- **Shizuoka, the source bullet** (the owner asked for each list's date on
  the page, 2026-10-04): "From Shizuoka City's registers of barbers, beauty
  salons and laundries: the complete lists as of March 31, 2026 and the new
  premises listed each month since, to August 31, 2026 for barbers and
  September 30, 2026 for beauty salons and laundries."
- **Shizuoka, the food bullet** (Kōchi's sentence with Shizuoka's share):
  "Restaurants, cafés and shops are not on this map: the national list of
  food businesses gives an address for only about six in ten of Shizuoka's
  restaurants."
- **Shizuoka, the sightseeing bullet** fills the template's slot for a line
  rather than cable cars: "The Oigawa Railway's Ikawa Line, which is a
  sightseeing line, is not drawn."

## Downstream inputs this branch changes

- New cities (Visuals, Analytics): Shizuoka (`shizuoka`, notice 205; English
  station names from OpenStreetMap, rail from MLIT N02). Notice 205: caption
  only (CC BY 4.0 asks for attribution with the work, no placement named).
  No open terms question.
- `pipeline/line_registry.py`: `jr-central-tokaido-line` gains Shizuoka.

## Changes

### 2026-10-11 - Okazaki built, the city's food-permit list with MHLW's notifications, food only

- **Okazaki built (page 260, notice 207), Hiroshima's page shape (food only)
  on Ichinomiya's mechanics (a city list, MHLW's notifications and points):
  3,614 storefronts (Food service 2,711, Food shops 903) around 16 stations
  on 3 lines, 50.5% of them in a ring (1,825: Food service 1,456, Food shops
  369) on the standard rings.** Sources: Okazaki City's
  食品等営業許可・届出一覧 on BODIK (organization 232025; CC BY 4.0 under the
  city's terms, read 2026-10-07 by staging, clause 5(5) accepted by the
  owner, call 214), 4,022 rows in term on 2026-08-31, and MHLW's file for
  23202 (799 rows: 673 notifications, 126 permits). Built by a Regional-2
  subagent; the brief passed 6 of 6.
- **The brief's two hooks, one already shared.** The brief asks for
  Hiroshima's hook carrying 許可条件 into 業態 to take the 210 kitchen cars
  out. The foundation's `kyoka_joken` rule already reads 自動車 in 許可条件
  (step 2: "set aside, vehicle (permit condition): 210"), so no hook was
  written. O1 (大字 + 小字 + 丁目) is the shared `koaza_chome` rule. O2 is
  city-local as the brief says: `config.source_rows` reads U+B743 as ばら in
  戸崎町字<U+B743>山 only (20 addresses; every city row at ばら山, 24, now reaches a block,
  where the brief counted 17 of the 20 at the district tier and 3 unplaced). Precedent
  for a cell rewritten in a city's own `source_rows`: Gifu's term dates.
  The brief's "2 trade names" with the code point were not found in 施設名称
  (0 of 4,022); none is on the map.
- **Step 2 against the brief.** Rows 4,022 and 673. Set aside: 210 vehicles,
  1 area-wide address, 2 not a premises, 29 permits starting 2026-09-01
  (call 172: 21 restaurants, 4 菓子, 2 食肉販売, 2 魚介類販売), 324 MHLW
  notifications with no address. Not a storefront 274 (no rule 151, vending
  105, institutional catering 10, temporary or mobile 6, mail order 2).
  Storefront rows 3,855: Food service 2,794 (the brief's 2,815 less the 21
  late restaurants), Retail 1,061 (the brief's 819 less 8 late, plus 250
  MHLW notifications). 38 city rows dropped for MHLW's row of the same
  premises; 164 repeat permits shown once. 0 names withheld. 菓子 / そうざい
  539 rows, 19 factory-like (3.5%), kept.
- **The join (3,855 rows):** block 3,562 (92.4%; the brief 92.7% on the
  city's rows alone), 小字 centre 127 (3.3%), town-chōme centre 84 (2.2%),
  MHLW's own point 43 (1.1%: 30 MHLW rows, 13 city rows through
  `POINT_DONORS`), unplaced 39 (1.0%). The brief's as-is 87.1% is not where
  the build ended, so call 145's tier disclosure is met by the excluded
  section's Not placed paragraph rather than a page bullet.
- **Call 178 (舞木町字金森) applied:** 51 pins at the site (46 city, 5 MHLW;
  40 restaurants): 36 at the 小字's centre (the foundation's
  `koaza_centroid`, finer than the town centre the brief expected) and 15 at
  MHLW's point; all 51 lie 756 to 797 m from 名電山中, inside its outer ring.
- **Call 179 (the new towns south of JR 岡崎) applied:** 32 city rows at
  針崎西 16, 岡崎駅前 11, 若松西 4 and 柱西 1, and 3 at two 土地区画整理 areas,
  stay unplaced (35 of the 39); 8 rows there take MHLW's point (7 MHLW, 1
  city). The other 4 unplaced: 鹿勝川町地内 2 and 久右ヱ門町 2.
- **The share (call 125, Ichinomiya's precedent):** 3,023 restaurant permits
  of e-Stat's 3,755 in force (80.5%, `japan_official.restaurants`), stated on
  the page as about four in five.
- **Census control (`japan_census_control.py okazaki`):** 2,711 Food service
  pins against 1,257 establishments in the 2021 Economic Census, 2.16 per
  establishment (the brief estimated 2.10; Akita 2.11, Aomori 2.33). High
  because the list has no 業態 column: convenience stores (174 by trade-name
  word in the brief), supermarkets (100), hotels and food-court counters
  holding 飲食店営業 stay in Food service, each permit holder a pin, and the
  restaurant stock grew from 3,466 to 3,755 between FY2021 and FY2024.
- **Rail:** step 1 reproduces the brief: 17 station records, 16 groups
  (Meitetsu 9, Aichi Loop 6, JR 2; 岡崎 one group), 9 stations beyond the line
  listed (Toyota 4, Anjō 2, Toyokawa 2, Kōta 1). Median nearest-station gap
  1,741 m, as the brief: standard rings. 中岡崎 and 岡崎公園前 168 m apart,
  kept apart. Gate 3 exact on Meitetsu's 9 (its Nagoya Main Line station
  list, 名電長沢 / 本宿 ... 宇頭 / 新安城) and the Aichi Loop's 6 (its station
  index), both read 2026-10-11 by plain GET. JR Central's timetable was not
  read: JR's 2 are not gated and its frequency stays as the brief asserted.
- **Station names:** 3 overrides in Hiroshima's style (Okazaki-koen-mae for
  OSM's Okazakikōen-mae, Uto for Utō, Meiden-Yamanaka for Meiden Yamanaka,
  Toyota's Mikawa-Yatsuhashi precedent); OSM's other 13 stand, Kitanomasuzuka
  among them (the operator's own sign was not read).
- **Line colours:** Meitetsu's Nagoya Main Line `#E80010` and JR's Tokaido
  Line `#E86810` from `line_registry`; the Aichi Loop Line `#28A800`,
  Toyota's value, repeated as a literal because the registry has no entry.
  Against the pins (step 3): 51.6, 62.6 and 45.7, all over 45. Between
  lines: 31.4 (Main, Tokaido), 105.3 and 134.7.
- **Privacy verdict: publish.** `check_personal_exposure.py okazaki`: the
  Japan pass prints 0 of 3,614; 2 trade names in the raw files are an
  operator's own name (MHLW's file, by the brief) and neither is on the map;
  no pin shows its permit type. Blank or damaged pin names on the rendered
  map: 0.
- **Not run:** the GSI sample (the brief does not ask for it), drift, the
  provenance and scope checks (the lead's). `check_no_em_dashes.py` and
  `check_no_fetch_in_steps.py` OK.
- **One request went out with the wrong user-agent.** The `package_show`
  call for the dataset id (2026-10-11, under the BODIK lock, 20 s held)
  carried a hand-typed user-agent that included the owner's email address
  instead of the project's own string. Nothing else was sent; later requests
  used `osm.OVERPASS_USER_AGENT`.
- Files: `pipeline/okazaki/` (config, fetch_sources, steps 1 to 3),
  `outputs/okazaki/` (heatmap.html, excluded_stations.csv, provenance.json).

#### Parked calls

1. **The registry has no Aichi Loop Line.** Toyota draws it (`AK`,
   `#28A800`) and Okazaki now does. *Recommend* a registry entry
   `aichi-loop-railway-aichi-loop-line` at `#28A800` with `maps: {"toyota":
   "AK", "okazaki": "AK"}`, and both configs reading it. Tradeoff: none for
   the maps (same colour); until then `check_line_identity.py` may flag the
   literal.
2. **U+B743 as a `gaiji` entry instead of the city-local rewrite.**
   `japan.CITIES["okazaki"]["gaiji"] = {0xB743: "ばら"}` would do the same
   through shared code and reach trade names too. *Recommend* leaving the
   city-local rewrite (address only, as the brief decided); tradeoff: one
   more `source_rows` normalisation outside the shared reader.
3. **久右ヱ門町 / 久右ｪ門町 (2 rows unplaced) and 宮石町字六ﾂ田 (17 rows at the
   district tier):** half-width and old kana the shared join does not fold
   for this town. *Recommend* a shared-code look at review time (a
   half-width kana fold); tradeoff: every city screen re-run for 19 rows.
4. **JR Central's frequency is still asserted.** The brief asks for a read
   at build; it needs the station index and PDFs the brief does not name.
   *Recommend* accepting it unread: the Tokaido main line here is nowhere
   near 11 trains a day. Tradeoff: one figure in the record rests on common
   knowledge.
5. **Kitanomasuzuka** stands as OSM writes it; the Aichi Loop Railway's own
   sign may hyphenate it. *Recommend* reading the operator's English station
   page at review time; tradeoff: a possible one-name override and re-render.

#### Proposals

- Page, source bullet: "From Okazaki City's list of food-business permits
  (as of August 31, 2026)." (the template's sentence with the registers
  clause removed, as Hiroshima's)
- Page, coverage bullet: "The city's list holds about four restaurant
  permits in five of the official count, and kitchen cars, which it lists at
  a base address, are left out."
- Notice, completeness sentence: "The city's list holds about four
  restaurant permits in five of the official count, and the ministry's list
  holds only filings whose applicants agreed to publish them; neither is
  complete."
- Excluded section: "Restaurants the city's list does not hold: it has 3,023
  restaurant permits, against 3,755 in the national count a year earlier
  (about four in five). The city does not say why."

#### Registry

- `meitetsu-nagoya-main-line`: add `"okazaki": "NH"` to `maps`.
- `jr-central-tokaido-line`: add `"okazaki": "TK"` to `maps`.
- New entry needed (parked call 1): the Aichi Loop Line, `#28A800`, `maps`
  `{"toyota": "AK", "okazaki": "AK"}`. No other line of this batch's cities
  was checked against it.

#### Downstream

- Notice 207, Okazaki City: the terms' form (4(2)) is a credit line naming
  the work, the city and the licence; it does not say where it must sit, so
  caption only is defensible, card face not required. MHLW (PDL 1.0) and
  MLIT as on every Japanese card. Open terms question: none beyond clause
  5(5), accepted (call 214).

### 2026-10-11 - Aomori built, the city's food-permit list of August 31, 2026, food only

- **Aomori built (page 261, notice 208), Hiroshima's page shape (food only)
  on Akita's source shape (one standing list, nothing rebuilt): 3,528
  storefronts (Food service 2,891, Food shops 637) around 18 stations on 3
  lines, 34.9% of them in a ring (1,231: 964 and 267) on the standard
  rings.** Source: Aomori City's 食品営業許可施設一覧（オープンデータ）,
  `r0808zendate.csv`, 5,289 permits in term on 2026-08-31, CC BY 4.0 through
  青森市オープンデータ利用規約 (read 2026-10-07 by staging). Built by a
  Regional-2 subagent; the brief passed 8 of 8 on 2026-10-11.
- **Step 2 reproduces the brief.** 1,284 rows set aside as area-wide (青森市全域:
  1,271 restaurant permits, 12 fishmongers, 1 confectioner; the foundation's
  rule, not re-implemented), 9 not a premises (青森県内一円), 301 out by "no
  rule" (manufacturing), 0 past term and 0 late starters against
  `TERM_AS_OF` 2026-08-31. Storefront rows 3,695 (Food service 2,946, Retail
  749, the brief's exactly). 164 repeat rows shown once.
- **The join is better than the brief's on unplaced rows.** Block 3,515
  (95.1%, the brief's), 小字 center 121 (3.3%), town-chōme center 56 (1.5%),
  unplaced 3 (0.1%, all restaurants) where the brief left 29: the
  foundation's 大字 and 小字 rules place the 浪岡大字…字… rows the brief read
  as misses. The 3 left: two in 浪岡 and 卸町6丁目.
- **No shared-code change was needed.** The brief's four items (施設の所在地１,
  施設の名称、屋号, 営業許可業種, 全域) are all in shared code already; the
  config has no `source_rows` hook.
- **MHLW stays a control (the brief's open call 1, built on its
  recommendation):** read by no step, not credited; 119 of its 120 permits
  are in the city's list. Gifu's and Toyama's precedent.
- **The name rule flags 3 trade names in the raw file and 1 pin shows its
  permit type**, where the brief measured 0. Not read further (the names are
  never printed); the brief's measure predates the foundation's switches.
  0 blank names on the rendered data.
- **Factory share:** 37 of 439 菓子 / そうざい premises (8.4%) read as a
  factory or central kitchen; kept (owner, 2026-09-24).
- **Economic Census control (`scripts/japan_census_control.py aomori`):**
  2,891 Food service pins against 1,235 establishments (2021), 2.34 per
  establishment (the brief estimated 2.33), above the built range of
  1.56-1.92 and at Toyonaka's and Hirakata's level. The brief's reading
  stands: the list has no 業態 column, so konbini (133 by trade-name word),
  supermarkets (45), kitchens (75) and hotels (71) holding 飲食店営業 count
  as Food service, and 83 addresses hold five or more restaurant permits
  (本町's bar buildings); about 2.07 without them (the brief's estimate, not
  re-measured). Closures the city was not told of stay in the list.
- **Rail:** step 1 reproduces the brief: Ou Line 6 of 105, Tsugaru Line 7 of
  18, Aoimori Railway Line 7 of 27, 青森 one group (0 m), 18 stations, the
  Shinkansen's 新青森 dropped. 2 stations beyond the city line within 3 km
  are listed (蓬田 in 蓬田村, 北常盤 in 藤崎町). Median nearest-station gap
  1,819 m (the brief: 1,844 m): standard rings either way.
- **Gate 3 has no in-city count (Fukui's shape):** no line is wholly inside
  the city and neither operator's station list is named in the brief, so
  none was fetched. `GATE3["lines"]` is empty.
- **Station names stand as OpenStreetMap writes them:** 31 objects, all with
  `name:en`; 18 names read, none translated, no macron, no 丁目. No
  override, alias or tie.
- **Line names:** "JR Ou Line" (the registry's), "JR Tsugaru Line", "Aoimori
  Railway Line" (the operator's own name for its one line).
- **Line colours:** the Ou Line takes `#E07800` from
  `pipeline/line_registry.py`; the Tsugaru Line is `#28A800` and the Aoimori
  Railway Line `#0098E0` (`line_colour_search.py aomori`, 2026-10-11).
  Against the pins (CIE76): 53.6, 45.6 and 75.4; closest pair 94.2; the
  dark-mode labels separate, 3 of 3. None between 20 and 45.
- **Privacy verdict: publish.** `check_personal_exposure.py aomori`: the
  Japan pass prints 0 of 3,528. The name rule compares 申請者氏名 and
  代表者氏名 in memory only; the applicant's address columns and the phone
  column are never selected.
- **The notice's credit** uses the terms' prescribed form (3(2)) with the
  dataset page's own title, 食品営業許可施設一覧（オープンデータ） (a judgment
  call the licence read left to the build: the page whose URL the credit
  carries names itself so; the portal's 青森市における食品営業許可施設一覧 is
  the alternative).
- Files: `pipeline/aomori/` (config, fetch_sources, three steps),
  `outputs/aomori/` (heatmap.html, excluded_stations.csv, provenance.json).

#### Parked calls

1. **Gate 3 against the operators.** Recommend: accept Fukui's shape (no
   in-city count) as built. Tradeoff: a read of JR East's line pages and the
   Aoimori Railway's station list would confirm N02's 18 and 27 whole-line
   totals, but the brief names neither page, so each is a fetch to approve.
2. **MHLW beside the list (the brief's open call 1).** Built control-only,
   the brief's recommendation. Tradeoff: the Food shops layer is permits
   only; adding MHLW's 454 notifications (248 addressed) would add a thin
   partial layer and MHLW's credit to the notice.
3. **Hiranai on the page.** The "running on to" bullet names Yomogita,
   Fujisaki and Hiranai; `excluded_stations.csv` lists only the first two
   (the Aoimori Railway's next station, in 平内町, is over 3 km beyond the
   line). Recommend keeping Hiranai (it is where the line runs on to);
   tradeoff: the bullet names a town the list below does not.
4. **The credit's title** (above): recommend the dataset page's title.

#### Proposals

Sentences adapted from an approved bullet of another page, none in the
japan-city template:

- "The JR Tsugaru Line is infrequent: 9 trains a weekday run toward Kanita
  and 8 toward Aomori." (from Akita's Uetsu Line bullet)
- "Aomori City publishes no list of barbers, beauty salons or laundries, so
  personal services are not on this map." (from Akita's laundries bullet and
  Hiroshima's)
- "About 1,300 permits are registered for the whole city rather than an
  address, which are event stalls and food trucks; they are not on this
  map." (new)
- Notice 208's processing sentence: "(This map modifies Aomori City's list
  of food-business permits as of August 31, 2026: this project selected the
  storefront types, left out permits registered for the whole city rather
  than an address, showed a premises with several permits once, placed each
  by its address, and counted them around stations.) The list is not claimed
  to be complete or current, and it may include premises that have closed."
  (from Gifu's)

#### Registry

- `jr-east-ou-line`: add `"aomori": "OU"` to `maps`.
- No new entry: the JR Tsugaru Line and the Aoimori Railway Line are drawn
  by no other built map and by no other city of this batch.

#### Downstream

- Notice 208 (Aomori City, CC BY 4.0 through the city's terms): the terms
  prescribe a credit wherever the modified work is used, so card face, in
  the prescribed form or the short form Visuals uses for CC BY 4.0 city
  lists; the MLIT credits as for every Japanese card. Open terms question:
  clause 6's bar on acts that "harm or defame the city or others" is
  undefined (raised the way Taoyuan's was); nothing in the map engages it.

### 2026-10-11 - Shizuoka built, the city's barber, beauty-salon and laundry registers with their monthly new permits, personal services only

- **Shizuoka built (page 258, notice 205), Kōchi's shape (full lists plus
  monthly openings) on Hamamatsu's three-ward precedent: 2,752 storefronts,
  all Personal services, around 24 stations on 2 lines, 44.2% of them in a
  ring (1,216) on the standard rings.** Sources: Shizuoka City's three BODIK
  datasets (organization 221007), CC BY 4.0 under the city's terms (read
  2026-10-05 by staging, the barber list the same day; calls 10, 11, 39 and
  40): each full list as of 2026-03-31 (686 barbers, 1,752 beauty salons, 306
  laundry rows) and 41 monthly rows since. Food stays off (owner,
  2026-10-04). Built by the Regional-2 lead; the brief passed 10 of 10.
- **The brief's dates moved forward.** BODIK gained R8.9 files for beauty
  salons (3 rows) and laundries (1 row) on 2026-10-06, after the brief; the
  brief says to fetch the newest monthly files at build and re-pin each date.
  Beauty salons and laundries are as of 2026-09-30, barbers 2026-08-31 (no
  barber file for R8.9). Three BODIK downloads on 2026-10-11, 21 s apart: the
  barber full list (re-fetched under the owner's approval of call 39, as the
  brief says) and the two September files; three `package_show` calls before
  them, 21 s apart.
- **Two laundry vehicles the brief did not see.** Step 2 sets aside 2 rows of
  the laundry list whose address ends 県内全域 after a vehicle's plate number:
  mobile laundry vehicles, caught by the foundation's area-wide rule. With the
  1 無店舗 row out, laundries are 306 premises (the brief counted 307 before
  the September row, vehicles included).
- **Step 2:** rows 689, 1,787 and 309; storefront rows 2,782. The join: block
  2,713 (97.5%), town-chōme 68 (2.4%), unplaced 1 (三保宮方, a beauty salon;
  MLIT has no 宮方 under 三保). The foundation's ッ / ツ rule placed the 3
  七ッ新屋 rows the brief left unplaced. 29 repeat rows shown once, so 2,752
  pins (the brief expected 2,750 before the September files). The name rule
  flags 0 rows.
- **Independent check (GSI's address search, 150 block-tier rows, 1 request a
  second, 2026-10-11):** 150 answered; median 26 m from MLIT's block point,
  148 within 100 m, all within 250 m.
- **Rail:** step 1 reproduces the brief: 15 of 15 on the Shizuoka-Shimizu
  Line (gate 3 exact), 10 of 89 on JR's Tokaido Line, 草薙 one group (176 m),
  the Ikawa Line left out by `LEFT_OUT_LINES` (owner, 2026-10-04), 2 stations
  beyond the city line listed (富士, 富士川, both in Fuji). The median
  nearest-station gap is 610 m, where the brief read 624 m: standard rings
  either way (the halving threshold is about 550 m).
- **Station names stand as OpenStreetMap writes them (a judgment call, on the
  operator's own signs):** "Pref. Art Museum" and "Pref. Sports Park" are the
  Shizuoka Railway's own English names for 県立美術館前 and 県総合運動場, not
  OSM's translation, so Fukuoka's trap does not apply; "Shin-shizuoka" and
  "Shin-shimizu" keep OSM's lowercase beside JR's "Shin-Kambara" (Maebashi's
  precedent: OSM's spellings stand). No override, alias or tie.
- **Line colours:** JR Central's Tokaido Line takes `#E86810` from
  `pipeline/line_registry.py` (the registry's `maps` gains Shizuoka); the
  Shizuoka-Shimizu Line is `#0068B8`, `line_colour_search.py`'s nearest to the
  operator's blue. Against the Personal services pin: 88.5 and 106.4 (CIE76);
  `check_line_identity.py` PROBLEMS 0.
- **Line names:** "Shizuoka-Shimizu Line" (the operator's own name for its
  one line, as "Jomo Line" in Maebashi) and "JR Tokaido Line" (the registry's
  name).
- **Privacy verdict: publish.** `check_personal_exposure.py shizuoka`: the
  Japan pass prints 0 of 2,752; no trade name in the raw files is an
  operator's own name. The name rule compares 開設者氏名, 開設者法人, 営業者氏名
  and 法人代表者 in memory only; the operators' own addresses and the phone
  column are never selected.
- **No Economic Census control was run:** the control measures restaurants
  (industry 76) and this page has no food leg. The brief's census ratios for
  the registers (1.22, 1.57 and 1.12 per establishment) stand as measured at
  Step 0.
- **The notice's credit form** follows the licence read's "CC BY 4.0 改変
  form" in Hamamatsu's wording (the three register titles, 静岡市, the CC BY
  4.0 deed, the three dataset pages linked). The city's own terms were not
  re-read at the build.
- Files: `pipeline/shizuoka/`, `outputs/shizuoka/`,
  `app/pages/258_Shizuoka_Heatmap.py`, `app/cities.py`, `app/components.py`
  (notice 205, `_OSM_STATION_NAMES`), `pipeline/countries/japan.py` (the
  batch's eleven `CITIES` entries), `pipeline/line_registry.py`,
  `scripts/check_personal_exposure.py` (the batch's eleven entries), the
  docs rows.
