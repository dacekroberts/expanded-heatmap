# Fukushima — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, calls 81, 106 and 110: `docs/decisions_drafts/staging.md`, "Wave 5"). The
Step 0 downloads were approved by the owner the same day. **Step 0 measured
2026-10-06** (staging). First, as the approval asked, the city's open-data
list (`soshiki/2/1005/1/1/2312.html`, ページID 2312, 福島市オープンデータ一覧)
was read: its 保健・医療・福祉 entry (`.../1/1/5/2340.html`) links
**食品営業許可施設、生活衛生関係施設一覧** (`.../1/1/5/1_1/index.html`, ページID
**18472**), which offers every file below. Then, into `data/fukushima/raw/`
(gitignored), each from its publisher's own host with the project user-agent,
each HTTP 200, under each URL's own file name as `japan_fetch.get` saves:

- From `www.city.fukushima.fukushima.jp` (`material/files/group/7/`; 保健所衛生課):
  the food list `r07nendomatsusyokuhin.csv` (812,233 B) and the five monthly
  files `r0804syokuhin.csv` … `r0808syokuhin.csv` (19,831 B together); the
  barber, beauty, laundry and coin-laundry lists `r07nendomatsuriyou.csv`
  (41,499 B), `r07nendomatsubiyou.csv` (115,846 B),
  `r07nendomatsucleaning.csv` (27,115 B) and `r07nendomatsucoincleaning.csv`
  (11,446 B; in scope: coin laundries count as Personal services, owner
  2026-09-28, Sapporo's precedent, `docs/excluded_categories.md`).
- From `i2fas.mhlw.go.jp`: `07201_food_business_all.csv` (162,393 B), a
  control only.
- From `nlftp.mlit.go.jp`: `isj/07201-24.0a.zip` (330,866 B) and
  `isj/07201-19.0b.zip` (7,493 B).

**1,528,722 B in all.** Nothing else was downloaded. Not fetched (not
approved): the registers' 2026 monthly files on the same page
(`r0808riyou.csv`, `r0804biyou.csv` … `r0807biyou.csv`; open call 3), the
inn and theatre lists.

**Run `python scripts/brief_check.py fukushima` before writing any code.**
Then the `japan-city` skill, **Fukuyama's shape** (a city's own full food
list plus the months since, `rebuilt_register`; `docs/build_briefs/fukuyama.md`)
with **Ichinomiya's answered merge** (the full list kept whole, the months
added; `docs/build_briefs/ichinomiya.md`, owner calls 125-128), Hamamatsu's
for the registers. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Fukushima entry; its table is shared
code and was not edited). Rail: MLIT N02-25 cut at the N03 city line,
measured through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; 福島 on the Tōhoku Shinkansen is dropped, the conventional 福島
stays); (2) **lines served only by limited expresses DO count** (2026-09-28);
(3) **the city line only**: only stations inside the city get rings, JR and
the private lines are cut at the line, **a one-station stub stays as cut**
(2026-09-27); an URBAN line cut to ONE station is left out, its station kept
through the other lines, and drawn cut only where no other line serves that
station (owner, 2026-10-06, calls 54 and 92); (4) **菓子製造業 and そうざい製造業
count, in Retail**, the factory share measured and kept (2026-09-24,
2026-09-27); (5) **the name rule**, version 2 (2026-10-06): a bare personal
name is withheld whatever the operator column holds; (6) **no page says
"currently operating"**. Also: no frequency floor for JR or private lines in
Japan (owner, 2026-10-06, call 46), any stretch at about 11 trains a day or
fewer named and drawn (call 86); fault-based cost clauses accepted for all of
Japan (2026-09-24); English station names from OSM `name:en`; every Japanese
city reads `WAVE2_RULES` (owner, 2026-10-04); coin laundries count as
Personal services (owner, 2026-09-28).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Fukushima carries `label_tier: "minor"` and goes in the **Japan East** view;
wave 4's first city to land retags Japan into the eight regions, Fukushima
into **Tohoku** (`docs/staged_cities.json` already says `jp8: "Tohoku"`). Its
label offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and
1200), never by eye.

**✅ `mode`: `metro`** (the owner's rule of 2026-10-02, applied as for Kurume
and Maebashi): JR is not the largest network inside the city (7 station
groups against Fukushima Kōtsū's 12), and no subway or tram is drawn, so the
mode follows the backbone: the Iizaka Line is a railway (N02 class 12, 鉄道,
not a 軌道 tramway), as Maebashi's Jōmō Line is. `docs/staged_cities.json`'s
`light_rail` was a stress-test guess; this brief sets it.

---

## The one-line summary

**All three buckets from the city's own CSVs (CC BY 2.1 JP by the city's
open-data terms; the licence read is done, staging records it).** The food
list of permits in term on 2026-03-31 holds **3,733 rows, 2,854 restaurants
(飲食店営業), 100.3% of e-Stat's 2,846 in force**, old-law permits included
(406 restaurants; Kurashiki's trap does not arise). The five monthly files
add **89 NEW permits** (no renewals). Kept whole plus the months (open call
1, Ichinomiya's answered method): **3,769 rows, 2,883 restaurants (101.3%)**;
in term on 2026-08-31 instead: 3,672 / 2,813 (98.8%). Barbers 278 (98.6% of
282), beauty salons 638 (101.3% of 630), laundries 108 storefronts (92.3% of
117) plus 17 storeless pick-ups (out), coin laundries 52, all as of
2026-03-31. Through `japan_eigyo`: **Food service 1,658, Retail 772**. Block
join **90.1%**, unplaced 0.6%. MHLW's file is opt-in filing (44 permits, every
one already in the city's files): a control only (open call 2). **Rail: 22
station groups** (Fukushima Kōtsū Iizaka Line 12, JR Tōhoku 5, Abukuma
Express 5, JR Ōu 3, 福島 shared by all four); the Ōu Line's **11 trains a
day** at 笹木野 and 庭坂 drawn and named (call 86).

---

## Business leg — the city's 保健所衛生課 lists

Host `https://www.city.fukushima.fukushima.jp`, page ID 18472,
`soshiki/2/1005/1/1/5/1_1/index.html`, linked from the open-data list
(2312) through its 保健・医療・福祉 entry (2340). The page states its scope:
「福島市内で、食品衛生法、理容師法、美容師法、旅館業法、興行場法、クリーニング業法、
福島市コインオペレーションクリーニング営業施設の衛生措置等指導要綱に基づく許可等を受けた
施設の一覧です。」 and 「毎月10日頃を目途に、前月に許可等を受けた施設の一覧を更新します。」
It carries **no licence line and no closed-premises note**; the list page
sends every user to the 利用規約 on page 1696. The server sends no charset
(the checks below match ASCII only).

### Food: 食品営業許可施設一覧

| File | Bytes | Rows | What it is |
|---|---|---|---|
| `r07nendomatsusyokuhin.csv` 食品営業許可施設一覧（令和8年3月31日現在） | **812,233** | **3,733** | permits in term on 2026-03-31 |
| `r0804syokuhin.csv` … `r0808syokuhin.csv` 令和8年N月の新規食品営業許可施設一覧 | 19,831 | 21 · 16 · 27 · 15 · 10 = **89** | each month's NEW permits, start dates in their own month |

- **Encoding UTF-8 with BOM**, CRLF, header on line 1, every row 12 fields,
  no empty lines. Dates `2026/3/31` (`wareki_date` reads every 許可始期 and
  許可終期; none unreadable).
- **Columns** (full list): No., **営業者住所**, **営業者電話番号**, **営業者氏名**,
  **営業所所在地**, 営業所電話番号, **営業所屋号名称**, **業種**, **種目**, **許可始期**,
  **許可終期**, 許可指令書番号. **The months spell four of them differently**:
  営業所屋号 for the trade name (all five), 種目又は業態 (April, May, August),
  種目または業態 (June), 種目 (July); 業種名 for the type (July); 営業者氏名漢字
  for the operator (June).
- **業種** (full list): 飲食店営業 2,854, 菓子製造業 342, そうざい製造業 137,
  魚介類販売業 87, 食肉販売業 59, 漬物製造業 45, 密封包装食品製造業 41,
  麺類製造業 21, 清涼飲料水製造業 16, **喫茶店営業 15** (an old-law-only type),
  and 22 smaller manufacturing types.
- **種目** among restaurants: 一般食堂 675, スナック 261, 軽食喫茶 260, 軽食堂 158,
  露店営業（イベント・祭礼等に限る） 146, 給食食堂 143, 軽料理店 106, バー 104,
  レストラン 70, 自動車による営業 (three spellings) 169, めん類食堂 58, and
  **multi-valued forms separated by a space** (一般食堂 仕出し屋 49, 一般食堂 仕出し屋
  弁当屋 38, 料理店 旅館 …; open call 4).
- **Not a premises**: the 146 露店 permits have an **empty address**; **153
  vehicle permits carry a vehicle code in the address field** (Latin letters
  and digits, all with 種目 自動車による営業). The first are `mobile` in
  `permits_from_rows`; the second are not, and leave only through
  `FORM_RULES` reading 種目 (temporary / mobile), so 種目 must be read on
  every file. No 一円 address.
- **許可指令書番号 is not a row key**: shape `N-N` on every row, 1,843
  distinct over 3,733 rows; (number, start date) is near-unique (3,651). The
  months' numbers all recur in the full list for that reason, not because
  they are the same permits.

### Old-law coverage (Kurashiki's trap)

**Included.** 509 full-list rows started before 2021-06-01 (**406
restaurants**, 342 still in term on 2026-08-31), ending 2026 (301), 2027
(200) and 2028 (8); the old-law type 喫茶店営業 appears 15 times. e-Stat
衛生行政報告例 FY2024 (`japan_official.estat()`), 福島県福島市, 飲食店営業 in force
2025-03-31: **2,846** (old law 861, revised 1,985). The list a year later
holds old law 406 and revised 2,448: the old-law stock converting one for
one (the total moves by 8). Permit terms run 5 to 9 years (6 years on 2,301
rows).

### The months against the March list (merge, duplicates, closures)

- **The full list holds only permits in term on its date**: no 許可終期 falls
  before 2026-03-31 (2026: 348 … 2034: 3). Expiries fall in February, May,
  July, September and November only (the city's renewal cycle).
- **The months are NEW permits only** (their titles say 新規, and every start
  date falls in the file's month). 98 full-list permits (71 restaurants)
  expire in May or July 2026, and **none reappears in a month file**: a
  renewal is never published between editions. Only 7 of the 89 monthly rows
  sit at a premises (address, trade name, type) already in the full list.
- **Repeats**: 44 rows repeat an (address, trade name, type) under another
  number; 3,198 distinct (address, trade name) premises. One pin per premises
  (trap 7) takes them.
- **Closures are not marked**, in either list, and the city publishes no
  closure files. MHLW cannot be the control here (the city files almost
  nothing there, below), so closures between editions are invisible: an upper
  bound, disclosed as Kyoto's is.

| Merge (to 2026-08-31) | Rows | Restaurants | Share of 2,846 |
|---|---|---|---|
| Full list, 2026-03-31 | 3,733 | **2,854** | 100.3% |
| **(a) Kept whole plus the months** (`rebuilt_register`, `as_of` 2026-03-31) | **3,769** | **2,883** | **101.3%** |
| (b) Fukuyama's: in term on 2026-08-31 | 3,672 | 2,813 | 98.8% |

### Counts through `japan_eigyo` (merge (a), fixed premises)

**Food service 1,658, Retail 772** (菓子 344, deli 281 = そうざい製造業 142 +
そうざい by 種目 139, fishmonger 87, butcher 60). Out: temporary or mobile 331
(by 種目), **hostess venues 275** (スナック 265, キャバレー 9), **仕出し 230**,
manufacturing ("no rule") 229, institutional 161 (給食食堂 145), inside
accommodation 106, vending 7. **Economic Census control**
(`scripts/japan_census_control.py` at build): the 2021 census counts **1,226**
飲食店 establishments in 07201; 1,649 distinct placed Food-service premises is
**1.35 per establishment**, under the built cities' 1.56-1.92 (Ichinomiya's
estimate 1.37): the hostess and 仕出し rules take 505 restaurant permits here.

### MHLW's file (07201), a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=07201_food_business_all.csv`:
**162,393 B, 439 rows** (許可 44, 届出 395, nothing closed), UTF-8, the
national schema. The scope's **cover 0.01** (`docs/coverage_sweep/japan_universe_mhlw.csv`):
opt-in filing only, by the skill's own thresholds.

- **Every one of its 44 permits is in the city's files** by number (MHLW
  writes `福島市指令第N-N号`, the city `N-N`; 42 also by start date). It adds
  no permit.
- **Its 395 notifications** (233 addressed): through `japan_eigyo` 144 fixed
  Retail rows (other food sales 79, supermarkets 30, greengrocers 12, konbini
  11, rice 6), the rest vending (156 rows), institutional and packaging.
- **Its own points** check the join: block point against MHLW's point for the
  same premises, **median 45 m, 95.9% within 250 m** (221 rows, 2 over 1 km).

### Personal services: 生活衛生関係施設一覧 (the same page)

| File | Bytes | Rows | Kinds |
|---|---|---|---|
| `r07nendomatsuriyou.csv` 理容所一覧（令和8年3月31日現在） | **41,499** | **278** | barbers (no kind column) |
| `r07nendomatsubiyou.csv` 美容所一覧（令和8年3月31日現在） | **115,846** | **638** | beauty salons (no kind column) |
| `r07nendomatsucleaning.csv` クリーニング所一覧（令和8年3月31日現在） | **27,115** | **125** | 区分: 取次所 81 · 一般 27 · 無店舗取次店 17 |
| `r07nendomatsucoincleaning.csv` コインオペレーションクリーニング一覧（令和8年3月31日現在） | **11,446** | **52** | 区分: ランドリー 52 |

- UTF-8 with BOM, CRLF. Columns: №, (区分), **施設名称**, **施設市町村名** (福島市 on
  every row), **施設住所** (starts at the town, no city name), 施設電話番号,
  検査確認年月日, 検査確認済証, **開設者氏名**, **開設者都道府県名**, **開設者市町村名**,
  **開設者住所**, **開設者電話番号** (the operator's own address and phone).
- **Standing registers, not a stream**: 検査確認年月日 runs from the 1930s to
  2026-03-30 (barbers mostly 1970-2019, beauty salons 162 in the 2010s and 140
  since 2020). No closure column, no closed-premises note.
- **Official** (e-Stat FY2024 第10表 / 第11表, `data/hakodate/raw/estat_eisei_r6_*_by_city.csv`):
  barbers **282**, beauty salons **630**, laundries **117** (取次所 90), storeless
  pick-ups 17. **Shares 98.6%, 101.3%, 92.3%** (一般 27 of 27, 取次所 81 of
  90); 無店舗取次店 17 of 17, out as not premises (`japan_eigyo`; 2 of them
  have no address). Coin laundries sit under a city 指導要綱, not a law: no
  official count.
- No repeats in the barber, beauty or coin files; 8 in the laundry file;
  **10 premises in both the barber and beauty lists** (one pin per premises
  and bucket keeps one).
- **Shared code**: barber and beauty carry no kind column, so the source is
  the file (`source_rows` or `SOURCE_KIND`, as Fukuyama's mixed file); 区分 is
  already in `TYPE_COLS`; the coin file is source `coinlaundry` (Sapporo's).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/07201-24.0a.zip` (330,866 B,
**36,383 block keys**, 3,744 towns), town-chōme `.../19.0b/07201-19.0b.zip`
(7,493 B, **174**). `japan.CITIES` entry at build: `"fukushima": {"name":
"福島市", "pref": "07", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES,
"wardless": True, "wards": ["07201"]}`.

| Tier (merge (a), fixed premises in a bucket) | All (2,430) | Food service (1,658) | Retail (772) |
|---|---|---|---|
| Block | **90.1%** | 91.1% | 87.8% |
| Town-chōme / 大字 centroid | 9.3% | 8.4% | 11.3% |
| Unplaced | **0.6%** | 0.4% | 0.9% |

| Registers | Barbers (278) | Beauty (638) | Laundry (108 premises) | Coin laundry (52) |
|---|---|---|---|---|
| Block / chōme / unplaced | 86.0 / 11.2 / 2.9 | 89.2 / 8.9 / 1.9 | 88.0 / 8.3 / 3.7 | 73.1 / 23.1 / 3.8 |

MHLW's addressed rows join 82.5 / 11.9 / 5.6 (268).

**The misses, read** (towns only, by `misses.py` in the scratchpad; food
under merge (b), registers as listed, 373 rows in all):
- **Chōme tier (333)**: 214 sit in towns the block file carries (the block
  number is missing from it: 荒井北3丁目 11, 西中央5丁目 4 …); 119 in 地番 towns
  it does not carry at block level (飯野町字町 10, 大笹生字月崎 10, 松川町関谷字大窪 5,
  飯野町字境川 4 …: the 2008 merger's 飯野町 and the rural 字). They take the
  town centroid.
- **Unplaced (40)**: two address habits MLIT's keys do not follow. **字
  left out between 大字 and 小字**: 笹谷西谷地 (MLIT `笹谷字西谷地`), 渡利川岸町
  (`渡利字川岸町`), 森合西養山, 御山一本木, 瀬上町東町 (`瀬上町字東町1丁目`), 渡利番匠町 …
  **The 大字 itself left out**: 矢倉下 5, 山居 3, 北中川原 3, 中荒子 2 (each a 小字
  of 五十辺 in MLIT: `五十辺字矢倉下` …), 大明神 2 (`信夫山字大明神`). A rule
  inserting 字, and one resolving a 小字 that exists under one 大字 only, would
  place most of them (shared code, build).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_07_GML.zip`, N03 code 07201
(**767.2 km²**, extent W 140.229, S 37.624, E 140.570, N 37.977; the 2008
merger brought in 飯野町). Read with `stub_test()`'s method and an in-memory
`CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 飯坂線 (福島交通, 12) | Fukushima Kōtsū Iizaka Line | **12 / 12** | 福島, 曽根田, 美術館図書館前, 岩代清水, 泉, 上松川, 笹谷, 桜水, 平野, 医王寺前, 花水坂, 飯坂温泉 |
| 東北線 (東日本旅客鉄道, 11) | JR Tōhoku Line | **5 / 155** (6 records) | 福島, 東福島, 南福島, 金谷川, 松川 |
| 阿武隈急行線 (阿武隈急行, 12) | Abukuma Express Line | **5 / 24** | 福島, 卸町, 福島学院前, 瀬上, 向瀬上 |
| 奥羽線 (東日本旅客鉄道, 11) | JR Ōu Line | **3 / 105** (4 records) | 福島, 笹木野, 庭坂 |

- **27 station records, 22 N02_005g groups** (福島 shared by all four lines,
  spread 129 m). No name in two groups. **Close pairs** (trap 1: kept apart):
  泉 / 岩代清水 332 m, 笹谷 / 上松川 427 m, 飯坂温泉 / 花水坂 482 m (all Iizaka),
  東福島 / 卸町 514 m (JR and Abukuma). **Median nearest-station gap 886 m**
  (332 to 4,142): standard rings by the spacing rule (halved only at about
  550 m or less).
- **Shinkansen**: 福島 (東北新幹線) dropped; the conventional 福島 stays. The
  Yamagata Shinkansen runs through on the Ōu Line but stops at neither 笹木野
  nor 庭坂; N02 files the line as conventional (class 11).
- **Cut at the line** (named by N03 municipality at build): Tōhoku 149
  beyond (other prefectures 129, 郡山市 3, 白河市 3, 二本松市 3, 国見町 2, 本宮市 2 …),
  Ōu 101 (all in other prefectures), Abukuma 19 (伊達市 10, Miyagi 9). The
  Iizaka Line lies wholly inside the city.
- **The light-rail/rail test**: all four are railways (N02 class 11, JR
  conventional; class 12, Fukushima Kōtsū's and Abukuma Express's 鉄道). No
  tram or light rail.
- **The stub test passes.** No urban line runs here. The Ōu Line's 3 of 105
  and the Tōhoku Line's 5 of 155 are main lines cut at the line; the Abukuma
  Express keeps 5 of 24 (向瀬上 228 m from the city line).
- **Frequency, read 2026-10-06** by plain GET with the project user-agent,
  weekday timetables (counts only; no timetable goes on the page). JR East's
  pages were counted per departure cell, marked or not (scratch `jre2.py`,
  not the J4 probe's `jre.py`, which skips ◆-marked minutes), and cross-checked
  by train links per page: every Ōu and Tōhoku departure here is unmarked
  (無印; no ◆ on the 福島, 笹木野 or 庭坂 Ōu pages), so the counts are the
  full counts.

  | Station (line, direction) | Weekday departures | Midday (10-16) |
  |---|---|---|
  | 福島 (Iizaka, to 飯坂温泉; `ii-den.jp/time/station.php?id=1`) | **48** (2 turn at 桜水) | 2-3 an hour; **4 an hour 07-09 and 17-18** |
  | 福島 (Tōhoku, to 白石・仙台; JR East `list1352`) | 20 | 6, largest gap 66 min |
  | 福島 (Tōhoku, to 郡山) | 26 | 6, largest gap 69 min |
  | 東福島 / 南福島 / 松川 (Tōhoku, both ways) | 20-21 / 25-26 / 24-25 | 6 each way |
  | 福島 (Ōu, to 山形・新庄) | **11** | **1**, largest gap 227 min |
  | 笹木野 (Ōu, both ways; `list0744`) | **11** each way | 1 |
  | 庭坂 (Ōu; `list1190`) | **11** to 福島, **6** onward (5 turn here) | 1, largest gap 265 min |

  **The Ōu Line from 福島 to 庭坂 is the stretch at about 11 trains a day:
  drawn and named** (owner, call 86); beyond 庭坂 (6 a day) lies outside the
  city. **Abukuma Express: READ by the probe** (2026-10-06, the operator's
  weekday sheet `abukyu.co.jp/wp-content/themes/abu/dist/img/webp/pdf/2026kudari.pdf`,
  linked from `abukyu.co.jp/station/`): about every 45-60 minutes; 31 down
  train numbers on the sheet. Not re-fetched here (a PDF not on the approved
  list); re-read at build if the page needs a figure.
- ⚠️ **Gate 3** at build: JR East's station counts inside the city (Tōhoku 5,
  Ōu 3), Fukushima Kōtsū's 12 (the operator's own station list, `ii-den.jp`,
  matches) and the Abukuma Express's 24. **OSM `name:en`** for 22 groups (one
  Overpass query at build, in the box below; not queried here).

## Scope

**Fukushima City.** JR Tōhoku runs on to 伊達市, Miyagi and 郡山市, the Ōu Line
to Yamagata Prefecture, the Abukuma Express to 伊達市 and Miyagi; cut at the
line.

## Licences — read 2026-10-06 (`licence-read`, recorded by staging)

**PERMITTED WITH CONDITIONS**: **CC BY 2.1 JP** by the city's open-data
terms (page 1696, `https://www.city.fukushima.fukushima.jp/soshiki/2/1005/1/1/1696.html`,
and the terms PDF `material/files/group/7/opendatariyokiyaku_2.pdf`, 福島市
オープンデータ利用規約), which the list page (2312) tells every user to read;
the dataset page itself carries no licence line. The full read is staging's
(`docs/decisions_drafts/staging.md`); not re-read here.

- **MUST DISPLAY** the terms' prescribed modified-use credit (§2(3)):
  「この[地図]は以下の著作物を改変して利用しています。[title]、福島市、クリエイティブ・コモンズ・ライセンス
  表示 2.1 日本（http://creativecommons.org/licenses/by/2.1/jp/）」, one title per
  list used (食品営業許可施設一覧, 理容所一覧, 美容所一覧, クリーニング所一覧,
  コインオペレーションクリーニング一覧); take the final wording from staging's
  record, not from here.
- **§4 reimbursement clause, uncapped: ACCEPTED by the owner** (2026-10-06,
  call 110; Hong Kong's and SanGIS's precedent). Record it in the city's
  licence row.
- **MHLW open data** (a control; only if open call 2 is taken): PDL 1.0 as
  recorded in `docs/data_sources/japan.md`, its 出典 line and who processed it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **JR East's, Fukushima Kōtsū's and the Abukuma Express's
  timetables**: read for counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The food lists carry the operator block**: **営業者氏名** (営業者氏名漢字 in
  June; no company or cooperative marker on 1,724 of 3,733 full-list rows, 46
  of 89 monthly rows), **営業者住所** and **営業者電話番号** (the operator's own
  address and phone), and 営業所電話番号. The scratch reader **dropped the
  operator address and phone at read** (3,822 rows) and printed no value.
  Step 2 never reads any of them into an output; 営業者氏名 (and 営業者氏名漢字)
  is read IN MEMORY for the name rule only.
- **The registers carry 開設者氏名, 開設者都道府県名, 開設者市町村名, 開設者住所 and
  開設者電話番号**: no company marker on 252 of 278 barbers, 476 of 638 beauty
  salons, 36 of 125 laundries, 20 of 52 coin laundries. Select 区分, 施設名称 and
  施設住所 only.
- **The name rule, version 2, measured in memory** (answers only, never a
  value): food full list **4** rows whose trade name is the operator's own
  name (2 restaurants), **3 of them bare personal names**; months 0; merge
  (a) 4 (3 bare). Barbers, beauty salons, laundries and coin laundries **0**.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected.
- Run `check_personal_exposure.py fukushima` (`japan=True`) after step 2:
  the rows that matter are the sole traders' trade names; it must print 0.
  Record the verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Tohoku after the retag), `"country": "Japan"`,
`label_tier: "minor"`. Project to **UTM 54N (EPSG:32654)**: the N03 centroid
lies at longitude 140.389, the extent 140.229 to 140.570, all inside the
138-144 band (computed here, never copied). OSM box from the N03 extent,
rounded out: (37.62, 140.22, 37.98, 140.58).

**Scaffold**: `scaffold_city.py --slug fukushima --name Fukushima
--system-name "Fukushima Kōtsū, Abukuma Express and JR East" --taxonomy
japan_eigyo --lat 37.786 --lon 140.389 --region "Japan East" --country Japan
--mode metro --page-number <N>` (`--dry-run` first), with the page number
claimed in `docs/session_roles.md` at build, not here (Fukushima is in
`docs/staged_cities.json`, a planning record only). The N03 centroid sits
about 7 km west of 福島 station (the city runs into the Azuma mountains); the
opening view fits the stations (`map-view`).

## Owner calls

**Made (do not re-ask):** Band A (owner, 2026-10-06, calls 81, 106 and 110);
the Step 0 downloads; the §4 reimbursement clause accepted (call 110); the
standing Japanese calls above; `mode: metro`; the minor tier and Japan East
(Tohoku after the retag); no frequency floor (call 46); the Ōu Line's 11 a
day drawn and named (call 86); the Tōhoku, Ōu and Abukuma lines drawn as cut
(standing call, no stub); coin laundries in Personal services.

**Open, each with a recommendation:**

1. **How the months merge with the March list.** (a) **Keep the full list
   whole and add the months** (`rebuilt_register` with `as_of` 2026-03-31):
   **2,883 restaurants, 101.3%**. (b) Fukuyama's method, in term on
   2026-08-31: 2,813, 98.8%. *Recommend (a), Ichinomiya's answered call
   (owner, 2026-10-06)*: the months publish new permits only, so the 98
   permits expiring in May and July (71 restaurants) can never reappear even
   when renewed, and (b) would drop them as if closed. Tradeoff: real
   closures among them stay on the map (the upper bound the page discloses),
   and the page's date reads "permits in term on 2026-03-31, with new permits
   to 2026-08-31".
2. **MHLW beside the city's list.** *Recommend a control only*, which departs
   from Matsuyama's, Fukuyama's and Ichinomiya's precedent of a partial
   Food-shops layer from MHLW's notifications: here the city files almost
   nothing with MHLW (cover 0.01, the skill's "opt-in filing only"), its 44
   permits are all in the city's files already, and the notifications would
   make a layer of 144 shops for a city of about 270,000. Tradeoff: no
   konbini or supermarket layer beyond the permit-holding ones already in
   Retail; MHLW's credit stays off the notice.
3. **The registers' 2026 months** (`r0808riyou.csv` 387 B; `r0804biyou.csv`
   … `r0807biyou.csv`, 360-709 B; the same page, publisher and terms; none for
   laundries): not approved, not fetched. *Recommend approving them at build*
   (Ichinomiya's call 128) so the registers reach 2026-08-31 like the food
   months; the tradeoff is a handful of salons for one more approval. Without
   them the registers' date is 2026-03-31 (`SOURCE_AS_OF` per source).
4. **Multi-valued 種目 with 仕出し or 旅館** (category check, precedent applied):
   of the 230 restaurant permits the shared 仕出し rule takes, **161 also name
   a counter form** (一般食堂 仕出し屋 50, 一般食堂 仕出し屋 弁当屋 39, すし屋 仕出し屋
   弁当屋 8 …), and 25 more go out as inside accommodation beside 料理店 or
   一般食堂. *Recommend the precedent*, the shared `FORM_RULES` as written
   (`docs/category_rules.md`; Sasebo's 弁当総菜・仕出し屋 163, Kanazawa's 仕出し屋
   out): a city-level exception would fork the taxonomy. Tradeoff: about one
   Food-service premises in ten that has a counter is left off; a shared
   change (a counter form beside 仕出し keeps the row) would move built cities
   and needs a drift run.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `NAME_COLS` + **営業所屋号名称** and **営業所屋号** (without them no food
  row has a trade name, and the name rule compares nothing); `FORM_COLS` +
  **種目又は業態** and **種目または業態** (without them four months' vehicles,
  stalls and snack bars are bucketed in); `OPERATOR_COLS` + **営業者氏名漢字**;
  the registers' kind per file (`source_rows` or `SOURCE_KIND`, coin laundry
  as `coinlaundry`); the two 字 rules in `join_city` (above).
- `rebuilt_register(..., end_col="許可終期", granted_col="許可始期")`, the
  `as_of` open call 1 decides, pinned, never today. The page updates around
  the 10th of each month: a September file may exist by the build; take it
  only with the pinned date moved, deliberately.
- One pin per premises: the 44 food repeats, 10 barber-and-beauty premises, 8
  laundry repeats.
- Gate 3 (JR East, Fukushima Kōtsū, Abukuma Express), OSM `name:en`, line
  colours on both basemaps, the opening view (`map-view`), the factory share
  (菓子 and そうざい in Retail), the Economic Census control (estimated 1.35),
  `check_personal_exposure.py`, `check_provenance.py`,
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "fukushima-opendata-list",
    "claim": "The city's open-data list (ページID 2312) links its 保健・医療・福祉 entry (2340) and the terms page (1696). ASCII strings only: the server sends no charset",
    "kind": "http_contains",
    "url": "https://www.city.fukushima.fukushima.jp/soshiki/2/1005/1/1/2312.html",
    "present": ["soshiki/2/1005/1/1/5/2340.html", "soshiki/2/1005/1/1/1696.html"]
  },
  {
    "id": "fukushima-opendata-health-entry",
    "claim": "The list's 保健・医療・福祉 entry (2340) links the food and environmental-hygiene page (18472)",
    "kind": "http_contains",
    "url": "https://www.city.fukushima.fukushima.jp/soshiki/2/1005/1/1/5/2340.html",
    "present": ["soshiki/2/1005/1/1/5/1_1/index.html"]
  },
  {
    "id": "fukushima-food-env-page",
    "claim": "Page 18472 offers the 2026-03-31 food list, the five 2026 monthly food files, the four registers and the unfetched register months (open call 3). ASCII strings only (no charset sent); its scope sentence and monthly-update note were read by curl 2026-10-06",
    "kind": "http_contains",
    "url": "https://www.city.fukushima.fukushima.jp/soshiki/2/1005/1/1/5/1_1/index.html",
    "present": ["r07nendomatsusyokuhin.csv", "r0804syokuhin.csv", "r0805syokuhin.csv", "r0806syokuhin.csv", "r0807syokuhin.csv", "r0808syokuhin.csv", "r07nendomatsuriyou.csv", "r07nendomatsubiyou.csv", "r07nendomatsucleaning.csv", "r07nendomatsucoincleaning.csv", "r0808riyou.csv", "r0807biyou.csv"]
  },
  {
    "id": "fukushima-food-full-list-live",
    "claim": "The full food list (permits in term on 2026-03-31, 812,233 B, 3,733 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.fukushima.fukushima.jp/material/files/group/7/r07nendomatsusyokuhin.csv",
    "min_bytes": 750000
  },
  {
    "id": "fukushima-food-aug-live",
    "claim": "The August 2026 new-permit food file (2,198 B, 10 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.fukushima.fukushima.jp/material/files/group/7/r0808syokuhin.csv",
    "min_bytes": 2000
  },
  {
    "id": "fukushima-barber-live",
    "claim": "The barber list as of 2026-03-31 (41,499 B, 278 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.fukushima.fukushima.jp/material/files/group/7/r07nendomatsuriyou.csv",
    "min_bytes": 38000
  },
  {
    "id": "fukushima-beauty-live",
    "claim": "The beauty-salon list as of 2026-03-31 (115,846 B, 638 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.fukushima.fukushima.jp/material/files/group/7/r07nendomatsubiyou.csv",
    "min_bytes": 110000
  },
  {
    "id": "fukushima-laundry-live",
    "claim": "The laundry list as of 2026-03-31 (27,115 B, 125 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.fukushima.fukushima.jp/material/files/group/7/r07nendomatsucleaning.csv",
    "min_bytes": 25000
  },
  {
    "id": "fukushima-coinlaundry-live",
    "claim": "The coin-laundry list as of 2026-03-31 (11,446 B, 52 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.fukushima.fukushima.jp/material/files/group/7/r07nendomatsucoincleaning.csv",
    "min_bytes": 10000
  },
  {
    "id": "fukushima-opendata-terms",
    "claim": "The city's open-data page (1696), which the licence read covers, offers the terms PDF",
    "kind": "http_contains",
    "url": "https://www.city.fukushima.fukushima.jp/soshiki/2/1005/1/1/1696.html",
    "present": ["opendatariyokiyaku_2.pdf"]
  },
  {
    "id": "fukushima-mhlw-live",
    "claim": "MHLW's open-data file for Fukushima (07201), the control, answers a plain keyless GET (162,393 B, 439 rows)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=07201_food_business_all.csv",
    "min_bytes": 140000
  },
  {
    "id": "fukushima-isj-block-live",
    "claim": "MLIT's block-level address file for Fukushima (07201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/07201-24.0a.zip",
    "min_bytes": 300000
  },
  {
    "id": "fukushima-isj-chome-live",
    "claim": "MLIT's town-chōme file for Fukushima (07201) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/07201-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "fukushima-iizaka-timetable",
    "claim": "Fukushima Kōtsū's timetable for 福島 lists the Iizaka Line toward 飯坂温泉 with its 桜水 short-turns - the frequency source",
    "kind": "http_contains",
    "url": "https://ii-den.jp/time/station.php?id=1",
    "present": ["下り（飯坂駅方面）", "桜水止"]
  },
  {
    "id": "fukushima-jr-fukushima-timetable",
    "claim": "JR East's timetable index for 福島 (1352) links the Ōu Line (060) and both Tōhoku Line directions (040, 050)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1352.html",
    "present": ["tt1352/1352060.html", "tt1352/1352040.html", "tt1352/1352050.html"]
  },
  {
    "id": "fukushima-jr-niwasaka-timetable",
    "claim": "JR East's timetable index for 庭坂 (1190), the Ōu Line's 11-a-day stretch, answers",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1190.html",
    "present": ["tt1190/"]
  },
  {
    "id": "fukushima-abukuma-timetable",
    "claim": "The Abukuma Express's station page links its 2026 weekday timetable sheets (the probe's frequency source)",
    "kind": "http_contains",
    "url": "https://www.abukyu.co.jp/station/",
    "present": ["2026kudari.pdf", "2026nobori.pdf"]
  },
  {
    "id": "fukushima-projected-crs",
    "claim": "Fukushima projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.389,
    "expect": "EPSG:32654"
  }
]
```
