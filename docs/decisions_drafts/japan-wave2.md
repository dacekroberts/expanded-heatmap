# DECISIONS drafts - Japan wave 2 (`japan-wave2-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

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
