# Ichikawa — build brief

**Band B, personal services only, owner-approved 2026-10-04** (Japan's third
wave; the Step 0 downloads approved 2026-10-05, staging's call 10,
`docs/decisions_drafts/staging.md`, "Band B's licence terms accepted, the
briefs' calls made, the Japanese Band B briefs and a Hamburg re-check
approved"); the monthly beauty and laundry files approved 2026-10-05 (call
34, "The Japanese Band B briefs' calls made (owner)"). **Step 0 measured
2026-10-05; the monthly files 2026-10-06** (staging). Into
`data/ichikawa/raw/` (gitignored), each from its publisher's own host:

- Chiba Prefecture's three lists, **one download serving Matsudo and
  Ichikawa**: fetched once into `data/matsudo/raw/` from
  `opendata.pref.chiba.lg.jp` (resource 79 → `ichiran-riyou202503.xlsx`,
  328,249 B; 80 → `ichiran-biyou202603.xlsx`, 765,694 B; 81 →
  `ichiran-clean202603.xlsx`, 254,290 B; each HTTP 200) and copied here
  byte for byte, as a build's `fetch_sources.py` would fetch them into each
  city's own `raw/`. The fetch is recorded in `docs/build_briefs/matsudo.md`.
- From `nlftp.mlit.go.jp`: `isj/12203-24.0a.zip` (160,791 B) and
  `isj/12203-19.0b.zip` (8,256 B).
- 2026-10-06, the ten approved monthly files, fetched once into
  `data/matsudo/raw/` (each title read by `resource_show` first; 3 s apart,
  each HTTP 200, each the catalogue's size) and copied here: **beauty**
  美容所新規施設 令和8年4月-8月, resources 103-99 → `shinki-biyou2604.xlsx`
  (72,493 B), `shinki-biyou2605.xlsx` (71,517 B), `shinki-biyou2606.xlsx`
  (72,316 B), `shinki-biyou2607.xlsx` (71,818 B), `shinki-biyou2608-2.xlsx`
  (70,264 B; the publisher's own `-2`, a second upload); **laundry**
  クリーニング所新規施設 令和8年4月-8月, resources 115-111 →
  `shinki-clean2604.xlsx` (46,248 B), `shinki-clean2605.xlsx` (46,093 B),
  `shinki-clean2606.xlsx` (45,239 B), `shinki-clean2607.xlsx` (46,503 B),
  `shinki-clean2608.xlsx` (45,519 B).
- Not fetched: MHLW's prefecture file (12000), since food is off and no
  control needed it; the barber months and every month before 2026-04 (not
  approved: barbers get no months, owner call 34).

**Run `python scripts/brief_check.py ichikawa` before writing any code.** Then
the `japan-city` skill, **Kōchi's shape** (personal services only, a full
list per kind; `docs/build_briefs/kochi.md`, `pipeline/kochi/config.py`), with
one difference that is new: **the publisher is the prefecture, not the city**,
so every row is assigned to Ichikawa by its address (below). Coordinates: the
`address-join` skill, measured with the shared
`pipeline/countries/japan_register.py` functions from scratch scripts
(`scripts/screen_japan_join.py` has no Ichikawa entry; add one at build).
Rail: MLIT N02-25 cut at the N03 city line, measured through
`pipeline/countries/japan.py` with a scratch `CITIES` entry (none was added to
the shared module).

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27), and an URBAN line cut to a stub goes back to
the owner (answered for Ichikawa 2026-10-06, below: one station left out,
two or more drawn cut); (4) **菓子製造業 and そうざい製造業 count, in Retail**
(2026-09-24; moot on a personal-services page); (5) **the name rule**: where
the trade name IS the operator's own name, the pin shows its permit type, the
operator column read in memory only (2026-09-27); MHLW's 法人名 joins it for
every MHLW city (2026-10-05; moot here, no MHLW source); (6) **no page says
"currently operating"**. Also: fault-based cost clauses accepted for all of
Japan (2026-09-24); English station names from OSM `name:en`, numerals as
figures before 丁目; every Japanese city reads `WAVE2_RULES` (owner,
2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Ichikawa
carries `label_tier: "minor"` and goes in the **Japan East** view, as
Utsunomiya, Maebashi and the other Kantō cities do (`app/cities.py`; wave 4's
first city retags Japan into the eight regions, Ichikawa into Kanto). Its
label offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and
1200), never by eye. Ichikawa sits about 9 km from Matsudo and borders Tokyo's
wards: measure its label against Tokyo's and Matsudo's.

**`mode`: `metro`.** Tokyo Metro's Tōzai Line (3 station groups) is drawn
inside the city, so the city is `metro` without the JR test. (The Toei
Shinjuku Line, the second subway, is left out: owner, 2026-10-06, below.)

---

## The one-line summary

**Personal services only, from Chiba Prefecture's open-data lists of barbers,
beauty salons and laundries (dataset 6, PDL 1.0), cut to Ichikawa by address:
223 barbers (⚠️ the list is as of 2025-03-31, not 2026-03-31 as the catalogue
title says, built as published with its own date, owner call 33), and beauty
salons and laundries rebuilt to **2026-08-31** from the 2026-03-31 lists and
five months of new premises (an upper bound: closures are not published;
owner call 34): **646 beauty salons and 148 laundries; 1,017 storefronts and
pins, placed at the block 99.5%, none unplaced.** No per-city official
count exists (e-Stat counts the prefecture's jurisdiction as one);
prefecture-wide, the barber list is 99.6% of the official count on the same
date. Food stays off (the master list: the prefecture's food set is old-law
only; MHLW's prefecture file is 62.7% addressed, 904 addressed rows here).
Rail: 15 N02 station groups (JR 5, Keisei 5, Tōzai 3, Hokusō 2, Toei
Shinjuku 1), six lines drawn: the Toei Shinjuku Line is left out (owner,
2026-10-06), 本八幡 keeping its ring through JR.

---

## Business leg — Chiba Prefecture's 環境衛生関係施設一覧 (dataset 6)

| | |
|---|---|
| **Dataset** | `https://opendata.pref.chiba.lg.jp/datasets/6`, 「【千葉県】環境衛生関係施設一覧」, organisation 衛生指導課 (contact 健康福祉部衛生指導課：生活衛生推進班), 「毎月」; `package_show` (`/ckan_api/package_show?id=6`, not `/api/3/`) metadata modified 2026-09-29; 52 resources, every one `resource_license_id: pdl` |
| **Its notes** | 「施設一覧は令和7年3月末時点の情報について掲載されています。」 (as of 2025-03-31: right for the barber file only, below); new premises added monthly around the 20th-25th; **only applicants who agreed to open publication are listed** (「申請者にオープンデータ掲載に賛同いただいているものに限定して掲載」); **Chiba, Funabashi and Kashiwa are not included** |
| **Files used** | resource 79 「【千葉県】理容所施設一覧（令和8年3月末時点）」, 80 美容所, 81 クリーニング所 (`https://opendata.pref.chiba.lg.jp/resource_download/<id>`); 82 (旅館・ホテル) is out of scope |
| **Monthly files** | 新規施設 for each kind, 令和7年9月 to 令和8年8月: barbers 83-94, beauty 95-106, laundries 107-118. **Used: beauty 99-103 and laundry 111-115 (2026-04 to 2026-08)**, owner call 34; the rebuild below. No closure files |
| **Layout** | One workbook per kind, **one sheet per health centre** (13 sheets); header in row 1, no title rows |
| **Columns** | barber, beauty: **開設者名** (the operator), **施設名称１**, 施設名称２, **施設所在地１**, 施設所在地２, 施設電話番号, **業務種別**, 検査確認番号, 検査確認日. Laundry: **営業者名** in place of 開設者名, plus **クリーニング種別１** (取次所, 洗い+仕上場, 仕上場, 洗い場, 無店舗取次店) and クリーニング種別２ |
| **Dates** | 検査確認日 in the era-letter dot form (`H01.04.25`, `R06.11.21`, `S63.…`); `japan_register.wareki_date` returns None for every S (Shōwa) date. Nothing in the build reads it |

### ⚠️ The barber file is the 2025-03-31 list

Settled from inside the files (the master list's check at build; the full
table is in `matsudo.md`, the same three files): the barber file is served as
`ichiran-riyou202503.xlsx`, **328,249 B against the catalogue's 378,797**,
saved 2025-04-23 (`docProps/core.xml`), uploaded 2026-03-04 (HTTP
Last-Modified), and **its newest 検査確認日 in any of its 13 sheets is
2025-03-07; none falls after 2025-03-31.** The beauty and laundry files are
the 2026-03-31 lists (`…202603.xlsx`, sizes as catalogued, saved 2026-04-27
and 2026-04-30; 221 and 14 rows confirmed after 2025-03-31). So the barber
layer carries its own as-of, **2025-03-31**, unless resource 79 is replaced by
build time (the brief check pins the catalogue's size).

### Assigning rows to Ichikawa (the address filter)

- **Ichikawa's rows sit in the 市川 sheet**, the 市川健康福祉センター's area:
  **市川市 and 浦安市**. Each row's 施設所在地１ starts with its municipality,
  with no prefecture (`市川市…`): barbers 223 Ichikawa / 76 Urayasu (299),
  beauty 638 / 192 (830), laundries 148 / 58 (211, with 5 more below). **No row
  naming 市川市 sits in any other sheet** (all 13 read), so the filter is
  exact: sheet 市川 and 施設所在地１ starting `市川市`. No ward exists.
- **Five laundry rows name no municipality**: 4 無店舗取次店 (no shop: not
  premises in any case) and 1 取次所. None of their towns is one of Ichikawa's
  in MLIT's files, so none is Ichikawa's; they stay out. Nothing straddles the
  city line.
- `japan_register` today reads every sheet and keeps every row: **step 2 needs
  a `source_rows`** (Kōchi's hook) that reads `city_rows(path, sheet="市川")`
  and keeps the rows starting `市川市`, failing if the count drifts from the
  brief's without a new file. Without it Urayasu's rows reach the join.
- The address is 施設所在地１ (`ADDR_COLS` has it); 施設所在地２ is the
  building (73 / 398 / 28 rows of the sheet). **No Ichikawa row keeps its
  number in 所在地２.**

### Counts that matter (Ichikawa's rows)

| Kind | Rows | Not a premises | Storefronts | Newest 検査確認日 (市川 sheet) | 検査確認番号 repeated in Ichikawa's rows |
|---|---|---|---|---|---|
| 理容所 (barbers) | **223** | 0 | 223 | 2024-11-21 | 0 |
| 美容所 (beauty) | **638** | 0 | 638 | 2026-02-27 | 0 |
| クリーニング所 (laundries) | **148** | 0 | **148** (取次所 92, 洗い+仕上場 53, 仕上場 3) | 2026-03-30 | 0 |
| **Personal services** | **1,009** | 0 | **1,009** | | |

- **One pin per premises**: no (address, trade name) pair repeats inside a
  list or across the three, so **step 2 draws 1,009 pins** from the 2026-03-31 lists (1,017 with the months, below).
- **No closed rows** (no closure column; each list is a snapshot at its date)
  and **no mobile salons** (no 移動, 一円 or 訪問 in any address or name).
- ⚠️ **The laundry kind is in クリーニング種別１**, which `TYPE_COLS` does not
  read (the type reads `クリーニング所` from 業務種別). No Ichikawa laundry row is
  a 無店舗取次店 on these files, but a later edition may carry one: map
  クリーニング種別１ into the type in `source_rows`, or add it to `TYPE_COLS`
  ahead of 業務種別 (then the Minato control).
- `japan_eigyo` buckets every type here as Personal services; nothing falls
  out by rule.

### The rebuild to 2026-08-31 (owner call 34; measured 2026-10-06)

The monthly 新規施設 files have the base lists' layout (13 health-centre
sheets, the same columns in the 市川 sheet). A centre with nothing that month
has a sheet holding only a title cell (「7月新規なし」) and no header, which
`xlsx_rows` already passes over.

| Month | Beauty: 市川 sheet rows | Ichikawa's | 検査確認日 range | Repeats a base row | Laundry: Ichikawa's |
|---|---|---|---|---|---|
| 2026-04 | 2 | **2** | 04-07 .. 04-15 | 0 | 0 (「４月新規なし」) |
| 2026-05 | 3 | **1** | 05-29 | 0 | 0 |
| 2026-06 | 5 | **4** | 06-05 .. 06-29 | 0 | 0 |
| 2026-07 | 0 (「7月新規なし」) | **0** | | | 0 |
| 2026-08 | 1 | **1** | 08-05 | 0 | 0 |
| **Total** | 11 | **8** | | **0** | **0** |

- **No new laundry in Ichikawa in any month** (the 市川 sheet reads
  「…新規なし」 in all five): laundries stay **148**, now dated 2026-08-31.
- **Beauty: 638 + 8 = 646.** No added row repeats a base 検査確認番号 or a base
  (address, trade name), nor another added row. 開設者名 filled on all 8, 6
  with a company marker; the name rule flags 0; none a vehicle or 無店舗; all
  8 join at the block.
- **Rebuilt totals at 2026-08-31**: barbers 223 (their own 2025-03-31), beauty
  646, laundries 148; **1,017 storefronts and 1,017 pins**.
- **An upper bound**: openings are added, closures are not published. Pin
  `as_of` to 2026-08-31 for beauty and laundry (`SOURCE_AS_OF`); the barber
  list keeps 2025-03-31.

### Coverage — against e-Stat and the Economic Census

**e-Stat has no Ichikawa row.** 衛生行政報告例 FY2024 第10表 and 第11表
(`data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
`…_cleaning_by_city.csv`, on disk, read here) list prefectures, 指定都市 and
中核市 only. Ichikawa is in the prefecture's own jurisdiction (千葉県 less
千葉市, 船橋市 and 柏市), exactly the lists' coverage:

| Kind | Official FY2024 (2025-03-31), prefecture's jurisdiction | The prefecture's list, every sheet | Share | Same date? |
|---|---|---|---|---|
| 理容所 | 4,350 − 600 − 331 − 238 = **3,181** | **3,168** (2025-03-31) | **99.6%** | yes |
| 美容所 | 10,486 − 1,701 − 960 − 758 = **7,067** | **7,607** (2026-03-31) | 107.6% | a year later |
| クリーニング所 (施設) | 2,366 − 428 − 220 − 129 = **1,589** | **1,509** premises + 22 無店舗 | 95.0% | a year later |

- **The consent filter is thin** prefecture-wide (barbers 99.6% on the same
  date). Disclose it as the coverage reason (the licence read's condition),
  with no number, since none is published.
- **Per-city, an estimate**: the 2021 Economic Census
  (`data/japan/raw/estat_census_r3_b1_009_1a.xlsx`, 第9-1A表; 理容業 200, 美容業
  387, 洗濯業 144 in 12203), scaled by the jurisdiction's licensed to census
  ratio (barbers 1.118, beauty 1.595, laundries 1.294), gives about **224
  barbers, 617 salons and 186 laundries**: the lists hold **223 (100%), 638
  (103%) and 148 (80%)**; rebuilt to 2026-08-31, **beauty 646 (105%)**,
  laundries unchanged at **148 (80%)** (no Ichikawa laundry opened in the five
  months). ⚠️ **Laundries look thin here** (about 38 short of the model),
  where Matsudo's read 97%; the cause is not known (consent, closures since
  2021, or what the census counts as 洗濯業). **Owner call 32: built, and the
  share stated on the page.** Since no official per-city count exists, the
  page must say it is an estimate from the census, not an official count (a
  review-time proposal: "The prefecture's register lists 148 laundries in
  Ichikawa, about four in five of the number the 2021 Economic Census
  suggests; the reason is not known.").

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 12203)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12203-24.0a.zip` and
`…/19.0b/12203-19.0b.zip`: **12,222 block keys, 238 town-chōme keys.** One
municipality, no wards (`"wardless": True`). Measured with `japan_register`
and `WAVE2_RULES` unchanged (no Minato re-run needed):

| Tier | Barbers (223) | Beauty (638) | Laundries (148) | All (1,009) |
|---|---|---|---|---|
| Block | **99.1%** | **99.7%** | **99.3%** | **99.5%** |
| Town-chōme / 大字 centroid | 0.9% (2) | 0.3% (2) | 0.7% (1) | 0.5% (5) |
| Unplaced | 0 | 0 | 0 | **0** |
| **With the 8 beauty additions (1,017)** | | block 644, chōme 2 (646) | | **block 99.5% (1,012), chōme 0.5% (5), none 0** |

- **The shifted-chōme rule carries most of it**: the lists write `町名1-2-3`
  without 丁目 (870 of 1,009 rows take `join_city`'s chōme shift); no affix
  rule was needed.
- **Chōme tier**: 柏井町1丁目 (3), 大野町1丁目, 原木: 地番 areas MLIT's block
  edition does not number.
- **Independent check**: the lists carry no coordinates and MHLW has no
  salons. GSI's address search on a sample at build (`screen_japan_join.py`'s
  `gsi_check`, 150 rows, one request per second).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (12203)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_12_GML.zip`, N03 code 12203
(56.9 km²; extent W 139.8855, S 35.6555, E 139.9768, N 35.7757). **16 station
records inside, 15 `N02_005g` groups**; no name in two groups. N02-24 and
N02-25 agree on every station here; use N02-25.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | First beyond the line |
|---|---|---|---|---|
| 本線 (京成電鉄, 12) | Keisei Main Line | **5 / 42** | 国府台, 市川真間, 菅野, 京成八幡, 鬼越 | 京成中山 (船橋市, 0.1 km), 江戸川 (Tokyo, 0.5 km) |
| 5号線東西線 (東京地下鉄, 12) | Tokyo Metro Tōzai Line | **3 / 23** | 南行徳, 行徳, 妙典 | 原木中山 (船橋市, 0.1 km), 浦安 (浦安市, 0.6 km) |
| 総武線 (東日本旅客鉄道, 11) | JR Sōbu Line | 2 / 48 | 市川, 本八幡 | 下総中山 (船橋市, 0.1 km), 小岩 (Tokyo, 1.5 km) |
| 京葉線 (東日本旅客鉄道, 11) | JR Keiyō Line | 2 / 19 | 市川塩浜, 二俣新町 | 西船橋 (船橋市, 0.4 km), 新浦安 (浦安市, 0.8 km) |
| 北総線 (北総鉄道, 12) | Hokusō Line | 2 / 15 | 北国分, 大町 | 矢切, 松飛台 (松戸市, 0.1 / 0.0 km) |
| 10号線新宿線 (東京都, 12) | Toei Shinjuku Line: ⛔ **left out** (`LEFT_OUT_LINES`, owner 2026-10-06) | **1 / 21** | 本八幡 (its terminus; the ring stays, through JR) | 篠崎 (Tokyo, 0.9 km) |
| 武蔵野線 (東日本旅客鉄道, 11) | JR Musashino Line | **1 / 27** | 市川大野 | 船橋法典 (船橋市, 0.4 km), 東松戸 (松戸市, 0.5 km) |

- **15 groups by operator**: JR 5, Keisei 5, Tokyo Metro 3, Hokusō 2, Toei 1
  (本八幡, one group with JR's 本八幡, 281 m apart: MLIT's interchange).
  **Kept apart, as N02 keeps them** (trap 1): Keisei's 京成八幡 and 本八幡, and
  Keisei's 市川真間 and JR's 市川, each a walking interchange under two names.
  Median gap to the nearest group **1,305 m** (closest pair 216 m): standard
  rings, by the spacing rule at build.
- ✅ **Two subway lines cut at the line, answered by the owner (2026-10-06;
  drafts, "Toei Shinjuku left out, the Tōzai drawn cut")**: **the Tōzai Line
  is drawn cut at the city line** (3 of 23; Sakai's Midōsuji and
  Higashiōsaka's Chūō Line the precedent), and **the Toei Shinjuku Line is
  left out** (`config.LEFT_OUT_LINES`, 1 of 21: 本八幡, its eastern terminus).
  The owner's rule from here: an urban line cut to one station in its city is
  left out, its station kept through the other lines; two or more are drawn
  cut. **Six lines are drawn.** At build: the page carries the owner's note (a
  review-time proposal), and `check_scope_disclosure.py` decides whether the
  Shinjuku Line's stations beyond the line belong in `excluded_stations.csv`
  (a left-out line is not a drawn network; Kobe's funiculars were kept out of
  it).
- ⚠️ **The proposed page sentence needs one word checked**: "the station is
  shown on the JR and Keisei lines". In N02, **本八幡's group holds JR's Sōbu
  Line and the Toei line only**; Keisei's 京成八幡 is a separate station and
  group (its own ring, a few hundred metres away, kept apart by trap 1).
  Suggested: "The Toei Shinjuku Line, which ends at Motoyawata just inside the
  city, is not drawn; the station is shown on the JR Sobu Line, and Keisei's
  Keisei-Yawata station is nearby." (or drop "and Keisei"). For review time.
- **One-station stub, kept as cut (standing call)**: **JR's Musashino Line at
  市川大野 (1 of 27), which the master list did not name**: a commuter railway,
  not an urban line.
- ⚠️ **A branch inside N02's 京葉線 (trap 3)**: 市川塩浜 is on the main line
  toward 新浦安, 二俣新町 on the Futamata branch toward 西船橋, both filed under
  京葉線. Read the sections at build and split the branch (`config.BRANCHES`,
  Kobe's) or draw it as Tokyo's Keiyō route did; the Musashino Line's through
  trains on the branch need no line of their own.
- ⚠️ **Services over N02's legal lines (trap 2)**: N02's 総武線 carries the
  Chūō-Sōbu local (市川, 本八幡) and the Sōbu Rapid (市川 only). **Tokyo built
  JR East's Sōbu services as routes; reuse them.** Tokyo's map also draws the
  Tōzai Line: reuse its public name.
- **The Shinkansen**: no station inside.
- **The light-rail / rail test**: the Tōzai Line (a subway, drawn) makes the
  city `metro`; the rest are railways (classes 11 and 12).
- **Frequency**: no floor applies to JR or private lines in Japan; **ASSERTED,
  not read**: every line here runs several trains an hour (the Tōzai and JR's
  Sōbu local every few minutes at the peaks). No operator's timetable was
  read for this brief.
- **Gate 3** against JR East's, Keisei's, Hokusō's and Tokyo Metro's station
  lists at build (Toei's is not needed: its line is not drawn).
- ⚠️ **OSM `name:en`** for the 15 groups at build (no Overpass at Step 0): one
  station query in the N03 box. Read every name: 国府台 (Kōnodai), 鬼越, 菅野,
  市川真間, 妙典, 二俣新町.

## Scope

**Ichikawa City (12203), one municipality, no wards.** The lines run on into
Funabashi, Urayasu, Matsudo and Tokyo's Edogawa and Katsushika; cut at the
line, the stations beyond named by N03 municipality at build
(`excluded_stations.csv`). Matsudo is its own page (`matsudo.md`): the Hokusō
Line's 矢切 and 松飛台 and JR's 東松戸 belong there.

## Licences — as read (the full read is recorded)

- **Chiba Prefecture, dataset 6**: read 2026-10-05 (`docs/decisions_drafts/
  staging.md`, "Band B's Japanese sources read: Kanazawa, Chiba Prefecture and
  Shizuoka permitted with conditions", the Chiba Prefecture bullet; that entry
  is the verdict, this brief only cites it). As declared: every resource
  `resource_license_id: pdl`; the catalogue's terms page
  (`https://opendata.pref.chiba.lg.jp/pages/terms`) applies 公共データ利用規約
  （第1.0版） (PDL 1.0) where no other note is given. What it requires of the
  build, as recorded there:
  - **Cite and build from `opendata.pref.chiba.lg.jp` only**, never a
    `pref.chiba.lg.jp` page.
  - **MUST DISPLAY** the catalogue's 加工 form,
    `「…」（千葉県オープンデータサイト）（URL）を加工して作成`, naming this project as
    the processor, as PDL 1.0 requires. Proposed, for the notice (the same
    words as Matsudo's):
    `出典：「【千葉県】環境衛生関係施設一覧」（千葉県オープンデータサイト）（https://opendata.pref.chiba.lg.jp/datasets/6）を加工して作成`.
  - **MUST NOT** present it as the prefecture's own or use its logos. No
    indemnity.
  - **The lists hold only applicants who agreed to open publication**:
    disclosed as a coverage reason.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**: CC
  BY 4.0, picks stations, ⛔ never drawn.
- **MHLW open data**: not used (food is off).

## Privacy

Read only the trade name, the type, the laundry kind and the premises address.
**No row value was printed or stored for this brief**: every count comes from
in-memory comparisons.

- **Operator columns**: **開設者名** (barber, beauty) and **営業者名** (laundry),
  both in `japan_register.OPERATOR_COLS`, filled on every row. In the 市川
  sheet, 245 of 299 barber operators, 508 of 830 beauty and 63 of 211 laundry
  carry no company or cooperative marker: mostly people's own names.
- **The name rule (version 1) flags 0 rows** in Ichikawa's 1,009, whether it
  compares 施設名称１ alone (what `NAME_COLS` reads) or 施設名称１ + 施設名称２
  (filled on 5 / 26 / 14 rows of the sheet), and 0 of the 8 beauty additions.
- **The name rule's version 2 is coming from Cleanup** (owner call 45,
  2026-10-06; drafts, "Toei Shinjuku left out, the Tōzai drawn cut; bare
  personal names measured; the Japanese name rule's version 2"): **a trade
  name written as a bare personal name (a common surname, a space, then 1-3
  kanji or kana, nothing else) shows its category**, whatever the operator
  column holds. Counted here with staging's patterns (counts only, no name
  printed): **4 of Ichikawa's 1,017 rows** take the strict form (barbers 3,
  beauty 1, laundries 0), every one with an operator name that differs; the
  loose shape, which version 2 does not use, matches 2 more. Build on the
  shared rule once it lands (never a city copy), and check that
  `check_personal_exposure.py` sees the 4.
- **Never selected**: 施設電話番号; the operator columns beyond the rule's
  in-memory comparison. No operator address is published.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map:
  it must print 0.

## Region

`"region": "Japan East"`, `"country": "Japan"`, `label_tier: "minor"`.
Project to **UTM 54N (EPSG:32654)**: the city's centroid lies at longitude
139.933 and its western edge at 139.8855, both inside the 138-144 band
(computed here, never copied).

**Scaffold**: `scaffold_city.py --slug ichikawa --name Ichikawa --system-name
"JR East, Keisei, Tokyo Metro and Hokusō" --taxonomy japan_eigyo --lat
35.719 --lon 139.933 --region "Japan East" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), with the page number claimed in
`docs/session_roles.md` at build, not here. A `japan.CITIES` entry:
`"ichikawa": {"name": "市川市", "pref": "12", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["12203"]}`.

## Owner calls

**Made:** Band B, personal services only (owner, 2026-10-04); the Step 0
downloads (owner, 2026-10-05, call 10); the prefecture's licence read
(2026-10-05); the standing Japanese calls above; the minor label tier and the
Japan sub-region (owner, 2026-10-02); `metro` (the Tōzai Line); JR's
Musashino Line at 市川大野 kept as cut by the standing call.

**✅ Answered by the owner, 2026-10-05 and 2026-10-06** (`docs/decisions_drafts/
staging.md`, "The Japanese Band B briefs' calls made (owner); two asked back
for precedent", calls 32-35, and "Toei Shinjuku left out, the Tōzai drawn cut;
bare personal names measured; the Japanese name rule's version 2", calls 31
and 45):

1. **The subway stubs** (calls 31, 41): **the Tōzai Line is drawn cut** (3 of
   23); **the Toei Shinjuku Line is left out** (`LEFT_OUT_LINES`), 本八幡
   keeping its ring, and the page says so, a proposal for review time: "The
   Toei Shinjuku Line, which ends at Motoyawata just inside the city, is not
   drawn; the station is shown on the JR Sobu Line, and Keisei's
   Keisei-Yawata station is nearby." (Corrected by staging 2026-10-06: in N02
   本八幡's group is JR's and Toei's only; Keisei's 京成八幡 is a separate
   group with its own ring, the rail section's note.)
2. **Laundries built and the share stated** (call 32): 148 against about 186
   from the census, about 80%, stated on the page as an estimate (the
   coverage section's proposed sentence).
3. **The barber list (2025-03-31) built as published, with its own date**
   (call 33). Re-check resource 79 at build in case it is replaced.
4. **The monthly beauty and laundry files, 2026-04 to 2026-08, approved**
   (call 34): fetched 2026-10-06 and measured above (beauty +8, laundries +0).
   The map is dated **2026-08-31 as an upper bound**; **barbers get no
   months**.
5. **The two-date source sentence is a proposal for review time** (call 35),
   the same sentence as Matsudo's: "From Chiba Prefecture's open-data
   registers of barbers (as of March 31, 2025) and of beauty salons and
   laundries (as of March 31, 2026, with openings to August 31, 2026), which
   list only premises whose operators agreed to publication."

Also: **the name rule's version 2** (call 45), in the privacy section.

**Open:** none (the Keisei word in item 1 is a wording fix for review time,
not a call).

## What the build must still measure

- The Kōchi config shape: `SOURCE_FILES` for the three lists and the ten
  monthly files (fetched into `data/ichikawa/raw/` by the city's own
  `fetch_sources.py`, under the publisher's file names above), `SOURCE_AS_OF`
  per kind (barbers 2025-03-31; beauty and laundry 2026-08-31), `MONTHLY` as
  Kōchi's, `REQUIRED_COLUMNS` naming 施設名称１, 施設所在地１, 業務種別 and
  開設者名 / 営業者名 (and クリーニング種別１ for laundries; a monthly sheet
  holding only 「…新規なし」 has no header and must not stop the check), and a
  **`source_rows`** that reads sheet 市川 of each list and month, keeps rows
  whose 施設所在地１ starts `市川市` (223 / 646 / 148), and carries
  クリーニング種別１ as the laundry type.
- `LEFT_OUT_LINES` for N02's 東京都 10号線新宿線, with the page's bullet;
  step 1 must still stop on any other in-city line the config does not name.
- ⚠️ **Shared code**, if preferred to `source_rows`: `TYPE_COLS` +=
  クリーニング種別１ ahead of 業務種別, then the Minato control
  (`screen_japan_join.py minato`, 98.0 / 0.2 / 1.8) and every city screen.
- Resource 79's served name and bytes; the newest edition of each file.
- The 5 chōme-tier rows; GSI on a sample.
- Gate 3 for four operators; the Keiyō branch; JR's Sōbu services as Tokyo's
  routes; OSM `name:en` for 15 groups; line colours on both basemaps (6
  lines).
- ⚠️ **The Economic Census control** (`scripts/japan_census_control.py`)
  measures 飲食店, which this page does not carry: the personal-services
  comparison above is the control; record it at build.
- FY2025's 衛生行政報告例 tables, when e-Stat publishes them, as the exact
  prefecture-level control for the 2026-03-31 beauty and laundry lists.

```brief-checks
[
  {
    "id": "ichikawa-dataset6-package",
    "claim": "Chiba Prefecture's dataset 6 still declares PDL on its resources, still excludes Chiba, Funabashi and Kashiwa, still lists only consenting applicants, and still points at resources 79-81 under their 2026-03-31 titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["\"resource_license_id\":\"pdl\"", "千葉市、船橋市及び柏市の施設情報は含まれていません", "オープンデータ掲載に賛同", "【千葉県】理容所施設一覧（令和8年3月末時点）", "【千葉県】美容所施設一覧（令和8年3月末時点）", "【千葉県】クリーニング所施設一覧（令和8年3月末時点）", "resource_download/79", "resource_download/80", "resource_download/81"]
  },
  {
    "id": "ichikawa-barber-size-mismatch",
    "claim": "The catalogue still declares 378,797 B for resource 79 while serving the 328,249 B 2025-03-31 file (ichiran-riyou202503.xlsx); if this size changes, the prefecture has touched the barber file: re-read it and re-measure",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=79",
    "present": ["\"size\":\"378797\"", "令和8年3月末時点"]
  },
  {
    "id": "ichikawa-barber-live",
    "claim": "Resource 79 (barbers) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/79",
    "min_bytes": 300000
  },
  {
    "id": "ichikawa-beauty-live",
    "claim": "Resource 80 (beauty salons, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/80",
    "min_bytes": 700000
  },
  {
    "id": "ichikawa-monthly-package",
    "claim": "Dataset 6 still lists the ten approved monthly files (beauty 99-103, laundry 111-115: 新規施設 令和8年4月 to 8月) under those titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["【千葉県】美容所新規施設（令和8年4月）", "【千葉県】美容所新規施設（令和8年8月）", "【千葉県】クリーニング所新規施設（令和8年4月）", "【千葉県】クリーニング所新規施設（令和8年8月）", "resource_download/99", "resource_download/103", "resource_download/111", "resource_download/115"]
  },
  {
    "id": "ichikawa-beauty-aug-size",
    "claim": "The August beauty file (resource 99, served as shinki-biyou2608-2.xlsx, a second upload) still declares 70,264 B; a new size means a third upload: re-fetch and re-measure the month",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=99",
    "present": ["\"size\":\"70264\"", "美容所新規施設（令和8年8月）"]
  },
  {
    "id": "ichikawa-beauty-aug-live",
    "claim": "The newest beauty month (resource 99, 2026-08) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/99",
    "min_bytes": 40000
  },
  {
    "id": "ichikawa-laundry-aug-live",
    "claim": "The newest laundry month (resource 111, 2026-08) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/111",
    "min_bytes": 30000
  },
  {
    "id": "ichikawa-laundry-live",
    "claim": "Resource 81 (laundries, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/81",
    "min_bytes": 200000
  },
  {
    "id": "ichikawa-terms-pdl",
    "claim": "The catalogue's terms page still applies PDL 1.0 and prescribes the 加工 credit form",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/pages/terms",
    "present": ["PDL1.0", "千葉県オープンデータサイト", "を加工して作成"]
  },
  {
    "id": "ichikawa-isj-live",
    "claim": "MLIT's block-level address file for Ichikawa (12203) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12203-24.0a.zip",
    "min_bytes": 120000
  },
  {
    "id": "ichikawa-projected-crs",
    "claim": "Ichikawa projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.933,
    "expect": "EPSG:32654"
  }
]
```
