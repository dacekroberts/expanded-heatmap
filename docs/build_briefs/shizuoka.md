# Shizuoka — build brief

**Band B, personal services only, owner-approved 2026-10-04** (Japan's third
wave; the Step 0 downloads approved 2026-10-05 as staging's call 10, the
city's BODIK copy as the source as call 11,
`docs/decisions_drafts/staging.md`, "Band B's licence terms accepted, the
briefs' calls made, the Japanese Band B briefs and a Hamburg re-check
approved"). **Step 0 measured 2026-10-05** (staging). Downloaded, each from
its publisher's own host, into `data/shizuoka/raw/` (gitignored), named
`<dataset>_<file>` because the three datasets reuse monthly file names
(`r8.4.csv` is both a beauty and a laundry file):

- From `data.bodik.jp` (organization 221007, 静岡市; one `package_search` of
  the organization, three `package_show`, then each file once, every request
  at least 15 s after the previous BODIK request of any agent; **every one
  answered 200**): the beauty list `biyoujo_biyosyo20260331.csv` (295,430 B)
  and its monthly files R8.4 to R8.8 (1,156 / 845 / 956 / 1,117 / 837 B); the
  laundry list `cleaning_cleaning20260331.csv` (48,470 B) and R8.4, R8.7
  (400 / 246 B); the barber list `riyoujo_riyosyo.csv` (96,799 B) and R8.6,
  R8.8 (339 / 190 B). For the churn measurement only: the 2025-03-31 lists
  (`biyoujo_biyojo070331.csv` 244,021 B, `cleaning_cleaning20250331.csv`
  59,196 B), beauty's twelve monthly files R7.4 to R8.3 and laundry's R7.5,
  R7.6, R7.7, R8.3. 30 files in all.
- From `nlftp.mlit.go.jp`: `isj/22101-24.0a.zip` (172,980 B),
  `22102-24.0a.zip` (166,295 B), `22103-24.0a.zip` (218,642 B) and the
  town-chōme `19.0b` files (11,376 / 7,664 / 9,598 B).
- Not downloaded: MHLW's food file (food is off; the figures below are the
  screening's), the city's food list (a `datastore_search` with `limit=0`
  read its row count and column names only).

**Run `python scripts/brief_check.py shizuoka` before writing any code.** Then
the `japan-city` skill, **Kōchi's shape** (full lists plus monthly openings,
`pipeline/kochi/config.py`'s `source_rows` and `MONTHLY`), on Hamamatsu's
three-ward precedent. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py`'s own functions from scratch scripts
(no shared file was edited; `scripts/screen_japan_join.py` has no Shizuoka
entry). Rail: MLIT N02-25 cut at the N03 city line through
`pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; 静岡 on the Tōkaidō Shinkansen is dropped, JR Tōkaidō Line's
静岡 stays); (2) **lines served only by limited expresses DO count**
(2026-09-28); (3) **the city line only**: only stations inside the city get
rings, JR is cut at the line, **a one-station stub stays as cut**
(2026-09-27), and an URBAN line cut to a stub goes back to the owner; (4)
**菓子製造業 and そうざい製造業 count, in Retail** (moot: no food leg); (5)
**the name rule**: where the trade name IS the operator's own name, the pin
shows its permit type, the operator column read in memory only (2026-09-27);
(6) **no page says "currently operating"**. Also: fault-based cost clauses
accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`, numerals as figures before 丁目; every Japanese city reads
`WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Shizuoka carries `label_tier: "minor"` and goes in the **Japan East** view,
as Hamamatsu, the built Shizuoka-prefecture city, does (`app/cities.py`). If
the wave-4 retag (the `japan-city` skill, owner 2026-10-04) has landed by the
build, it goes in **Chubu** instead. Label offset from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**`mode`: `metro`** (the owner's rule of 2026-10-02, applied as for Kurume and
Maebashi): no subway or tram, and JR is not the largest network inside the
city (10 station groups against the Shizuoka Railway's 15), so the mode
follows the backbone, the Shizuoka–Shimizu Line, an electrified railway
(N02 class 12).

---

## Finding, recorded before any download of it

**A barber list exists on the city's own BODIK catalogue**, against the
master list's "no barber list was found". Organization 221007 (静岡市),
dataset `221007_riyoujo-20160331`, 「理容所台帳」, author 生活衛生課,
declared `cc-by` ("Creative Commons Attribution", no version), 49 resources:
yearly full lists 2020-03-31 to 2026-03-31 (the newest
「理容所全施設（Ｒ8.3.31現在)」, `riyosyo.csv`, 96,799 B) and monthly
new-permit files (newest R8.8, uploaded 2026-09-14). Found by one
`package_search` of the organization (233 datasets) and one `package_show`.
It sits in the same city catalogue as the two approved datasets, so its full
list and post-base monthly files were fetched under the task's condition and
are measured below. **Its licence was not part of the 2026-10-05 read**
(open call 1).

Also found, not fetched: `221007_shokuhin20151023-001`, 「食品衛生関係営業許可台帳」
(食品衛生課, `cc-by`): one file, 「営業許可施設一覧（R3.5.31までに許可を取得した施設）R8.9.1時点」,
**375 rows** (`datastore_search` total), the permits granted under the old law
and still in term at 2026-09-01, the city's twin of the prefecture's list
12489. Columns 施設_名称, 施設_所在地, 施設_建物名, 施設_電話番号, 業種,
**申請者_氏名**, 初回許可年月日, 許可年月日, 終了年月日, 許可番号. It does not
change the food verdict (below).

---

## The one-line summary

**Personal services from the city's three 生活衛生 registers on BODIK, each a
full list as of 2026-03-31 plus the monthly openings since: barbers 689
(to 2026-08-31), beauty salons 1,784 (to 2026-08-31), laundries 307 premises
(to 2026-07-31), 2,780 rows and 101.7% of e-Stat's FY2024 count of 2,733,
joined to MLIT's blocks at 97.3%, 4 rows unplaced.** The annual lists ARE the
official register: the 2025-03-31 beauty list holds 1,732 against e-Stat's
1,731 at the same date, and the laundry list 312 premises against 312.
Closures between annual lists are not published, so the monthly rebuild is an
upper bound (about 2.4% to 4.4% of premises close in a year). **Food stays
off.** **Rail: 24 N02 station groups drawn** (Shizuoka Railway 15 of 15, JR
Tōkaidō 10 of 89, 草薙 shared), the Ikawa Line's 2 left out (owner); the
Shizuoka–Shimizu Line every 8 minutes at midday by its own timetable.

---

## Business leg — the city's 生活衛生 registers (BODIK, organization 221007)

| Dataset (`data.bodik.jp/dataset/…`) | Title | `package_show` modified | Resources |
|---|---|---|---|
| `221007_riyoujo-20160331` | 理容所台帳 | 2026-09-14 | 49 (7 full lists, 42 monthly) |
| `221007_biyoujo-20160331` | 美容所台帳 | 2026-09-14 | 87 |
| `221007_cleaning-20160331` | クリーニング所台帳 | 2026-08-10 | 24 |

Each record: author 生活衛生課, `license_id: cc-by`, notes
「台帳登録されている<kind>の一覧です。」, no frequency field. Every file is a
CSV; the monthly files are **new permits only** (「新規許可施設」 /
「新規開設施設」); no closure (廃止) file exists in any of the three.

### The files read

| File (resource) | Bytes | Encoding | Rows | As of |
|---|---|---|---|---|
| `riyosyo.csv` (`247daa58-9b6e-41db-9887-356f12eb4bd4`) 理容所全施設 | 96,799 | UTF-8 BOM | **686** | 2026-03-31 |
| barber `r8.6.csv` (`01e4b295-…`), `r8.8.csv` (`495b4f14-256c-4a31-86a8-ebd1b3286400`) | 339 / 190 | cp932 | 2 / 1 | 2026-06, 2026-08 |
| `biyosyo20260331.csv` (`ad3911f5-a842-4325-b890-36f4931d2103`) 美容所全施設 | 295,430 | UTF-8 BOM | **1,752** | 2026-03-31 |
| beauty `r8.4.csv` … `r8.8.csv` (newest `410dabe5-742b-4c74-ab94-d5a57341e9a9`) | 1,156 / 845 / 956 / 1,117 / 837 | mixed | 6 / 5 / 7 / 8 / 6 | 2026-04 … 2026-08 |
| `cleaning20260331.csv` (`e3d76212-bdc1-455c-b343-4ac0cb825b1a`) クリーニング所許可全施設 | 48,470 | **cp932** | **306** | 2026-03-31 (the prefecture's resource 105882 is its twin) |
| laundry `r8.4.csv` (`91d74981-…`), `-r8.7.csv` (`9b65adee-94d2-4c25-9bce-9ea7b9a1da9d`) | 400 / 246 | mixed | 1 / 1 | 2026-04, 2026-07 |

- **Encodings differ file by file** (UTF-8 BOM or cp932, even within one
  dataset); `city_rows` sniffs both. Declare them in `SOURCE_ENCODING` anyway
  (Kobe's trap 8).
- **Months with no file**: barbers R8.4, R8.5, R8.7; laundry R8.5, R8.6, R8.8.
  The city uploads a trade's month only when it has openings (beauty's twelve
  months R7.4 to R8.3 are unbroken; laundry had 4 of 12): none opened, or
  none published. Uploads land about 5 to 6 weeks after the month (R8.8 on
  2026-09-14).
- **Columns, full lists** (all three the same): 確認年月日 (wareki, `H 1. 3. 4`
  form), **施設所在地** (from 静岡県 in the 2026 lists, from the ward in the
  2025 ones), 施設電話番号, **施設名称**, **開設者住所**, **開設者氏名**,
  **開設者法人**, 業種 (理容所 / 美容所 / 取次所, クリーニング所, 無店舗).
- **Columns, monthly files**: the same, but the kind is **業種名称** (理容,
  美容, 取次所, クリーニング所) and the address starts at 静岡市; laundry's
  monthly files name the operator **営業者氏名**, **営業者住所** and
  **法人代表者**.
- **No permit number or ID column in any file.** The matching key is the
  normalised (施設所在地, 施設名称) pair.

### The rebuild (full list + monthly openings; closures not published)

| Trade | Full list 2026-03-31 | New since (months) | Already in the full list | **Rebuilt** | Official FY2024 (2025-03-31) | Share |
|---|---|---|---|---|---|---|
| 理容所 | 686 | 3 (R8.6, R8.8) | 0 | **689** (to 2026-08-31) | 690 | 99.9% |
| 美容所 | 1,752 | 32 (R8.4-R8.8) | 0 | **1,784** (to 2026-08-31) | 1,731 | 103.1% |
| クリーニング所 | 306 (取次所 201, クリーニング所 104, 無店舗 1) | 2 (R8.4, R8.7) | 0 | **307 premises** + 1 無店舗 (to 2026-07-31) | 312 (取次所 200) + 無店舗取次店 2 | 98.4% |
| **Personal services** | 2,743 | 37 | 0 | **2,780** | **2,733** | **101.7%** |

- **Official counts**: e-Stat 衛生行政報告例 FY2024, 生活衛生 第10表 and
  第11表, row 静岡県静岡市 (the national per-city files already on disk,
  `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
  `…_cleaning_by_city.csv`, read here, not downloaded): 理容所 690, 美容所
  1,731 (重複開設 `-`), クリーニング所 312 (取次所 200), 無店舗取次店 2.
  `japan_official.restaurants` gives the food figure, 8,647 restaurant permits.
- **The annual list is the register itself, measured**: the 2025-03-31 beauty
  list has 1,732 rows against e-Stat's 1,731 at the same date; the
  2025-03-31 laundry list 314 rows, of which 2 無店舗取次店, so 312 premises
  against 312. (The barbers' 2025 list was not fetched.)
- **The full list includes its last month**: every R8.3 new row is in the
  2026-03-31 list (beauty 7 of 7, laundry 1 of 1), and **no monthly row from
  R8.4 on repeats a full-list key** (0 of 37).
- **Closures are invisible between annual lists, measured on 2025 → 2026**:
  of the 2025-03-31 beauty list plus its year of openings (1,732 + 68), **60
  keys are gone from the 2026 list (43 by address alone)**; laundry, 14 of
  314 + 5 (13 by address). So about **2.4% to 3.3% of salons and 4.1% to
  4.4% of laundries close in a year**; the 2026-08 rebuild overstates by about
  five months of that (some 20 to 25 salons, 5 or 6 laundries). The template's
  "may include premises that have closed" bullet covers it; pin `as_of` per
  list to its newest month, never the download date (Kyoto's call).
- **Duplicates**: (address, name) repeats inside a list: barbers 1, beauty 3,
  laundry 0. **26 premises hold both a barber and a beauty registration** under
  one address and name (43 addresses in both lists); step 2's one pin per
  (address, trade name, bucket) makes those one Personal-services pin:
  **2,750 distinct pins** from the 2,780 rows.
- **Not a premises**: the laundry list's one 無店舗 row (`japan_eigyo` drops
  無店舗). No 移動, 一円 or 厚生施設 row in any list.
- **Standing registers**: readable 確認年月日 (the Heisei and Reiwa rows; the
  Shōwa rows, `S63.12.21` form, read as None in `wareki_date`, moot here)
  run from 1989; beauty by decade from the 1990s 201 · 259 · 513 · 469.
- **Against the 2021 Economic Census** (第9-1A表, the shared cached XLSX;
  establishments at 2021-06-01): 静岡市 理容業 567, 美容業 1,138, 洗濯業 273,
  so the registers read **1.22, 1.57 and 1.12 per establishment** (Maebashi's
  1.07, 1.59, 1.07; registered home salons the census misses explain beauty's
  excess). Per ward: 葵区 1.31 / 1.74 / 1.24, 駿河区 1.22 / 1.53 / 1.07,
  清水区 1.12 / 1.38 / 1.04.

### Food stays off (owner, 2026-10-04)

The screening's figures, not re-measured here: **MHLW's file holds 8,121 open
restaurant permits, 94% of the 8,647 in force, but only 60.3% publish an
address**. The city's own old-law list (375 rows, above) cannot close that
gap: even if all 375 were addressed and new, the placeable share would be
about (8,121 × 0.603 + 375) / 8,647 = **61%**, under the bar's ~70%.

---

## Coordinates — a JOIN to MLIT 位置参照情報 (3 wards)

MLIT files for **22101 葵区, 22102 駿河区, 22103 清水区** (each file's
市区町村名 静岡市<ward>): **70,892 block keys, 895 town-chōme keys** (葵区 409,
駿河区 187, 清水区 299). The ward parsed from every row is one of the three
(no row without a ward). Measured with `japan_register` and `WAVE2_RULES`
unchanged; storefronts after `japan_eigyo` (the 無店舗 row out).

| Tier | Barbers (689) | Beauty (1,784) | Laundries (307) | **All (2,780)** |
|---|---|---|---|---|
| Block | 97.0% | 97.5% | 97.4% | **97.3%** (2,706) |
| Town-chōme / 大字 centroid | 2.9% | 2.4% | 2.3% | 2.5% (70) |
| Unplaced | 0.1% (1) | 0.1% (2) | 0.3% (1) | 0.1% (4) |

| Ward | Rows | Block | Chōme | Unplaced |
|---|---|---|---|---|
| 葵区 | 1,217 | **97.8%** | 2.2% | 0 |
| 駿河区 | 711 | **99.7%** | 0.3% | 0 |
| 清水区 | 852 | **94.7%** | 4.8% | 4 |

- **Unplaced (4)**: **清水区 七ッ新屋 2丁目, 3 rows** (one per trade): the
  lists write a small ッ, MLIT writes 七ツ新屋 (七ツ新屋一丁目, 二丁目 exist in
  both 22103 files). One cited variant rule in `japan_register` places them.
  The fourth, 清水区 三保 + 宮方: MLIT has the 大字 三保 but no 宮方 (no 小字
  under 三保); the 大字 centroid is a candidate, read it at build.
- **The chōme tier** is mostly 清水区's 大字 with 地番 (中河内, 小河内, 茂畑,
  吉原, 宍原, 和田島, 横砂字御林脇) and, in 葵区, **柚木 (5 beauty rows)**, an
  urban district near the Shizuoka Railway; read why its blocks miss at build.
- **Independent check**: the registers carry no coordinates and MHLW has no
  salons. Run GSI's address search on a sample at build
  (`screen_japan_join.py`'s `gsi_check`, as Sendai and Kōchi: 150 rows, 1
  request per second).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_22_GML.zip`, wards
22101-22103 (1,413 km², the Southern Alps to the coast; extent W 138.0830,
S 34.8985, E 138.6385, N 35.6460). **27 station records inside, 26
`N02_005g` groups**; N02-24 gives the same stations. Shinkansen: 静岡,
dropped.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside, west to east |
|---|---|---|---|
| 静岡清水線 (静岡鉄道, 12) | Shizuoka–Shimizu Line (Shizuoka Railway) | **15 / 15** | 新静岡, 日吉町, 音羽町, 春日町, 柚木, 長沼, 古庄, 県総合運動場, 県立美術館前, 草薙, 御門台, 狐ヶ崎, 桜橋, 入江岡, 新清水 |
| 東海道線 (東海旅客鉄道, 11) | JR Tōkaidō Line | 10 / 89 | 用宗, 安倍川, 静岡, 東静岡, 草薙, 清水, 興津, 由比, 蒲原, 新蒲原 |
| 井川線 (大井川鐵道, 12) | Ōigawa Railway Ikawa Line | 2 / 14 | 閑蔵, 井川 (the terminus): **left out (owner)** |

- **24 station groups drawn** (Shizuoka Railway 15, JR 10, 草薙 one group on
  both lines, its two records 176 m apart); no name falls in two groups.
  Ward split of the 24: 葵区 9, 駿河区 3, 清水区 12.
- **Stub test passes**: the Shizuoka Railway is wholly inside; JR Tōkaidō is
  cut at the line as intended (the first stations beyond: 富士川, 1.0 km out
  to the east, and 焼津, 3.9 km out to the west; the build's N03 lookup names
  their municipalities). No urban line is cut to a stub.
- **The Ikawa Line (owner: leave it out, a mountain scenic line)**: its 2
  in-city stations sit in 葵区's far north, about 30 km from 静岡; the other
  12 are in 川根本町. On Kobe's and Kyoto's sightseeing precedent, a
  `LEFT_OUT_LINES` entry (Fukuoka's), its stations NOT written to
  `excluded_stations.csv` (`check_scope_disclosure.py` refuses a reason other
  than the city line), and a bullet under **The lines** (below).
- **Rings: standard** (0.1 / 0.2 / 0.3 / 0.6 mi). Median nearest-group gap
  **624 m** over the 24 drawn groups, above the ~550 m halving threshold
  (`docs/ring_rules.md`); the Shizuoka Railway's own median is 595 m, close
  to it, so record the measurement in the config. Closest pair 新静岡 – 日吉町
  348 m.
- **The light-rail / rail test** (the `japan-city` skill's mode rule): no
  subway, tram or light rail; both drawn lines are railways (classes 11 and
  12). JR is not the largest network by in-city groups (10 against 15):
  `metro`, on Kurume's and Maebashi's precedent.

**Frequency and gate 3, read from the operator's own pages by curl
(2026-10-05):**

- **Shizuoka Railway** (`https://train.shizutetsu.co.jp/timetable/timetable-station`):
  the station index lists **15 stations, S01 新静岡 to S15 新清水**, as N02 has
  15 (gate 3 exact). The weekday timetable from 新静岡 toward 新清水
  (`https://train.shizutetsu.co.jp/timetables/shin-shizuoka/down-weekdays`):
  **132 departures, 6:00 to 23:30; every 8 minutes from 10:00 to 16:56**,
  every 6 to 7 minutes in the peaks, every 15 minutes after 21:00. Some
  morning trains run to 柚木 only.
- **JR Tōkaidō Line**: **not read.** JR Central's station timetables
  (`railway.jr-central.co.jp/time-schedule/search/`) are a search form, not
  pages; the frequency is unrecorded here. No frequency floor applies to JR in
  Japan (Maebashi's brief).
- ⚠️ **Gate 3 for JR** (the 10 in-city stations against JR Central's own list)
  and **OSM `name:en`** for the 24 groups at build (one station query, no
  tram stops; no Overpass at Step 0). The operator writes **狐ケ崎** where N02
  writes 狐ヶ崎, and its English is "Pref. Sports Park" / "Pref. Art Museum":
  OSM may abbreviate or translate (Fukuoka's trap); read every name.

## Scope

**Shizuoka City (3 wards: 葵区, 駿河区, 清水区).** JR Tōkaidō runs on to Fuji
and Yaizu, cut at the line; the Ikawa Line is left out whole (owner).

## Licences

- **Read 2026-10-05** (`docs/decisions_drafts/staging.md`, "Band B's
  Japanese sources read", the Shizuoka bullet): **the 美容所台帳 and
  クリーニング所台帳 are PERMITTED WITH CONDITIONS**: CC BY 4.0 under the
  city's terms, which prevail where the same data sits elsewhere (第4条); the
  CC BY 4.0 改変 credit; the city's 「できれば御一報」 is a courtesy, not a
  condition, and is not sent. Fetched from the city's BODIK copy, not the
  prefecture's portal (owner, call 11), so the prefecture's §6 reimbursement
  clause does not bind. Build the notice from that entry.
- **As declared on BODIK** (2026-10-05): all three records, the barber list's
  included, `license_id: cc-by`, "Creative Commons Attribution", no version.
- ⚠️ **The 理容所台帳 was not in the 2026-10-05 read** (open call 1).
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**: CC
  BY 4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source,
  not drawn.

## Privacy

Read only 施設名称, 施設所在地 and the kind (業種 / 業種名称). **No row value
was printed or stored for this brief**: every count comes from in-memory
comparisons.

- **開設者氏名** (full lists, barber and beauty monthly) holds a company's
  name or a person's own: company markers on 41 of 686 barber rows, 373 of
  1,752 beauty, 204 of 306 laundry. Already in `OPERATOR_COLS`.
- **開設者法人** is NOT a company name: on every filled row (40 / 368 / 196)
  the 開設者氏名 is the company, and 開設者法人 holds its **representative's
  title and name** (a title word on 36 / 358 / 174). Laundry's monthly files
  call it **法人代表者**. **Neither is in `OPERATOR_COLS`**: add both at build
  (a person's name), then the Minato control.
- **The name rule flags 0 rows** in the rebuilt registers (barbers, beauty,
  laundries); no trade name equals 開設者法人 either. The page still takes the
  standard name-rule bullet.
- **開設者住所 / 営業者住所** (the operator's address; filled 42 / 383 / 204 in
  the rebuilt lists, of which 1 / 5 / 8 have no 開設者法人 value, so possibly a
  sole trader's home) and **施設電話番号**: never selected.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map
  (must print 0).

## Region

`"region": "Japan East"` (or Chubu after the wave-4 retag), `"country":
"Japan"`, `label_tier: "minor"`. Project to **UTM 54N (EPSG:32654)**: the
city's western edge lies at longitude 138.083 and 静岡 at 138.389, both inside
the 138-144 band (computed here; Hamamatsu, 50 km west, is 53N, never
copied).

**Scaffold**: `scaffold_city.py --slug shizuoka --name Shizuoka
--system-name "Shizuoka Railway and JR Central" --taxonomy japan_eigyo
--lat 34.972 --lon 138.389 --region "Japan East" --country Japan --mode
metro --page-number <N>` (`--dry-run` first), the page number claimed in
`docs/session_roles.md` at build, not here. A `japan.CITIES` entry:
`"shizuoka": {"name": "静岡市", "pref": "22", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wards": ["22101", "22102", "22103"]}`.

## Page text (`docs/city_page_format.md`)

- **The lines**: "2 lines are drawn, …: the Shizuoka Railway's
  Shizuoka–Shimizu Line and JR Central's Tōkaidō Line."; the MLIT/OSM bullet;
  "Only stations inside Shizuoka City get rings, … lines running on to Fuji
  and Yaizu are cut at the city line. The stations left out are listed
  below."; "The Shinkansen is not drawn (Shizuoka appears as a JR Tōkaidō Line
  station)."; and the sightseeing slot: "The Ōigawa Railway's Ikawa Line,
  which is a sightseeing line, is not drawn." (the template's slot; "a
  mountain scenic line", if preferred, is a proposal for the drafts file).
- **The businesses**: "**This map shows personal services only: barbers,
  beauty salons and laundries.**" (Yokohama's approved line; it fits only if
  barbers are built, open call 1). The owner asked for **each list's date on
  the page**: "From Shizuoka City's registers of barbers and beauty salons (as
  of 2026-08-31) and laundries (as of 2026-07-31)." is a three-date fill of
  the one-date template sentence: a proposal for the drafts file. Then the
  closed-premises bullet.
- **Reading the map**: the MLIT join bullet; the name-rule bullet; the
  Japanese-names bullet. No own-point or consent bullet applies.

## Owner calls

**Made:** Band B, personal services only (owner, 2026-10-04); food off (the
same); leave out the Ikawa Line (owner, 2026-10-04); each list's date on the
page (owner, 2026-10-04); the Step 0 downloads (call 10) and the city's BODIK
copy as the source (call 11, 2026-10-05); the licence terms of the beauty and
laundry lists accepted (2026-10-05); the standing Japanese calls above; the
minor label tier and the Japan sub-region (2026-10-02); `metro` by the mode
rule of 2026-10-02 (staging's reading, as Kurume's); standard rings by the
spacing rule (measured, 624 m).

**Open:**

1. **Build the barbers from the city's 理容所台帳 (found at Step 0).**
   Recommendation: yes, and run one `licence-read` on
   `221007_riyoujo-20160331` first (same publisher 生活衛生課, same catalogue,
   same `cc-by` label as the two read lists, so the city's terms most likely
   cover it, but that is not evidence). It adds 689 barbers (99.9% of the
   official 690, 25% of the page's premises) and lets the page use Yokohama's
   approved one-bucket line instead of a new "beauty salons and laundries"
   sentence. Tradeoff: one more source and a licence read before the build,
   against a page that leaves a whole trade off when its list is public. The
   master list row ("no barber list was found") then needs staging's
   correction.
2. **The three-date businesses sentence** (above): a proposal for the drafts
   file, flagged at review time, as the owner asked for each list's date.

## What the build must still measure

- Kōchi's config shape: `SOURCES` (barber, beauty, laundry), `MONTHLY` per
  trade, `source_rows` (full list + monthly files, the premises columns
  only), `SOURCE_AS_OF` per list (barbers and beauty 2026-08-31, laundries
  2026-07-31), `SOURCE_ENCODING` per file. Fetch the newest monthly files at
  build (R8.9 is due mid-October) and re-pin each `as_of`.
- ⚠️ **Shared code**, each followed by the Minato control
  (`screen_japan_join.py minato`, 98.0 / 0.2 / 1.8) and every city screen:
  `TYPE_COLS` += **業種名称** (the monthly files' kind; without it their type
  reads "" and a 無店舗 monthly row would not be caught); `OPERATOR_COLS` +=
  **開設者法人**, **法人代表者**; the **七ッ新屋 / 七ツ新屋** variant (3 rows).
- `japan_fetch` file names must keep the dataset prefix (three `r8.4.csv`).
- Gate 3 for JR Central's 10 stations; OSM `name:en` for 24 groups (狐ケ崎 /
  狐ヶ崎, the "Pref." names); line colours on both basemaps.
- **The opening view**: the N03 box reaches 35.65 N in the Southern Alps,
  while every drawn station lies south of 35.13 N; check `CITY_BBOX` and the
  fit with `map-view` and `scripts/check_map_view.js`.
- The GSI sample check (150 rows); 三保宮方 and 柚木's chōme rows read.
- The 26 barber-and-beauty premises collapse to one pin each (step 2 prints
  the one-pin count; 2,750 expected).
- FY2025's 衛生行政報告例 tables, when e-Stat publishes them, as the exact
  control for the 2026-03-31 lists.

```brief-checks
[
  {
    "id": "shizuoka-bodik-three-registers",
    "claim": "One BODIK search returns the city's three 生活衛生 datasets, each labelled cc-by, still pointing at the 2026-03-31 full lists (by resource id and byte size) and the newest monthly files read (beauty and barber R8.8, laundry R8.7). One request, so BODIK is never hit twice in a row by this brief",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=organization:221007%20AND%20name:(221007_biyoujo-20160331%20OR%20221007_cleaning-20160331%20OR%20221007_riyoujo-20160331)&rows=3",
    "present": ["\"count\": 3", "\"license_id\": \"cc-by\"", "221007_riyoujo-20160331", "221007_biyoujo-20160331", "221007_cleaning-20160331", "247daa58-9b6e-41db-9887-356f12eb4bd4", "riyosyo.csv", "\"size\": 96799", "ad3911f5-a842-4325-b890-36f4931d2103", "biyosyo20260331.csv", "\"size\": 295430", "e3d76212-bdc1-455c-b343-4ac0cb825b1a", "cleaning20260331.csv", "\"size\": 48470", "410dabe5-742b-4c74-ab94-d5a57341e9a9", "495b4f14-256c-4a31-86a8-ebd1b3286400", "9b65adee-94d2-4c25-9bce-9ea7b9a1da9d"]
  },
  {
    "id": "shizuoka-isj-aoi-live",
    "claim": "MLIT's block file for 葵区 (22101) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/22101-24.0a.zip",
    "min_bytes": 120000
  },
  {
    "id": "shizuoka-isj-suruga-live",
    "claim": "MLIT's block file for 駿河区 (22102) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/22102-24.0a.zip",
    "min_bytes": 120000
  },
  {
    "id": "shizuoka-isj-shimizu-live",
    "claim": "MLIT's block file for 清水区 (22103) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/22103-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "shizuoka-estat-riyo-biyo",
    "claim": "e-Stat's 衛生行政報告例 FY2024 第10表 (barbers and beauty salons by designated city: 静岡市 690 and 1,731) answers keyless - the completeness control",
    "kind": "http_ok",
    "url": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359178&fileKind=1",
    "min_bytes": 5000
  },
  {
    "id": "shizuoka-estat-cleaning",
    "claim": "e-Stat's 衛生行政報告例 FY2024 第11表 (laundries by designated city: 静岡市 312) answers keyless",
    "kind": "http_ok",
    "url": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359179&fileKind=1",
    "min_bytes": 5000
  },
  {
    "id": "shizuoka-shizutetsu-15-stations",
    "claim": "The Shizuoka Railway's station index links all 15 station timetables, 新静岡 (shin-shizuoka) to 新清水 (shin-shimizu), as N02 has 15 (gate 3). ASCII slugs only",
    "kind": "http_contains",
    "url": "https://train.shizutetsu.co.jp/timetable/timetable-station",
    "present": ["/station/shin-shizuoka", "/station/hiyoshicho", "/station/otowacho", "/station/kasugacho", "/station/yunoki", "/station/naganuma", "/station/furusho", "/station/prefsportspark", "/station/prefartmuseum", "/station/kusanagi", "/station/mikadodai", "/station/kitsunegasaki", "/station/sakurabashi", "/station/irieoka", "/station/shin-shimizu"]
  },
  {
    "id": "shizuoka-shizutetsu-8-minutes",
    "claim": "新静岡's weekday timetable toward 新清水 has seven departures in the 10 o'clock hour (anchors wd1001 to wd1013, :04 to :52), every 8 minutes, and no eighth",
    "kind": "http_contains",
    "url": "https://train.shizutetsu.co.jp/timetables/shin-shizuoka/down-weekdays",
    "present": ["wd1001", "wd1003", "wd1005", "wd1007", "wd1009", "wd1011", "wd1013"],
    "absent": ["wd1015"]
  },
  {
    "id": "shizuoka-projected-crs-west-edge",
    "claim": "Shizuoka's western edge (138.083 E, the N03 extent) still projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 138.083,
    "expect": "EPSG:32654"
  },
  {
    "id": "shizuoka-projected-crs",
    "claim": "Shizuoka (静岡 station, 138.389 E) projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 138.389,
    "expect": "EPSG:32654"
  }
]
```
