# Sagamihara — build brief

**Band A, owner-approved 2026-10-04** (Sagamihara from C to A on its licence
read, "late": `docs/decisions_drafts/staging.md`, "2026-10-04 - Central
Europe, Germany north and Sagamihara banded (owner)"; the Step 0 downloads
approved in "2026-10-04 - Band A's Japanese briefs: Step 0 downloads and
licence reads approved…", item 1). **Step 0 measured 2026-10-04** (staging):
the city's four 生活衛生課 datasets from its own CKAN catalogue
(`opendata.city.sagamihara.kanagawa.jp`: the food-permit, barber and beauty
FY-end zips with their 令和8年度 monthly zips, the laundry zip, and the food
dataset's April correction sheet), MHLW's file for 14150 and MLIT's ISJ block
and town-chōme zips for the three wards, all into `data/sagamihara/raw/`
(gitignored), as a build's `fetch_sources.py` would; the terms PDF was read
into the scratchpad, not kept. **Run `python scripts/brief_check.py
sagamihara` before writing any code.** Then the `japan-city` skill.
Coordinates: the `address-join` skill, measured with `japan_register.py`'s own
functions from a scratch script (`scripts/screen_japan_join.py` was not
edited). Kanagawa siblings: `kawasaki.md`, `yokosuka.md`; the rebuild is
Sakai's (`pipeline/sakai/config.py`), not Higashiōsaka's.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; no station here); (2) **lines served only by limited expresses
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27), and an URBAN line cut to a stub
goes back to the owner; (4) **菓子製造業 and そうざい製造業 count, in Retail**,
the factory share measured and kept (2026-09-24, 2026-09-27); (5) **the name
rule** where an operator column exists; every list here names an operator
only where it is a company, so Kawasaki's food-layer position (Toyama's,
accepted 2026-10-02) covers the whole page (below); (6) **no page says
"currently operating"**. Fault-based cost clauses are accepted for all of
Japan (2026-09-24), and Sagamihara's own §4 and §5 by the owner on Sakai's
precedent (2026-10-04).

**Minor label tier and the Japan East view, on precedent** (owner,
2026-10-02, for every Japanese batch city): `label_tier: "minor"`, region
`"Japan East"` as Kawasaki and Yokosuka. Sagamihara's dot sits about 13 km
west of Kawasaki's: `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200)
decides the offset, never the eye.

**`mode`: `metro`** by the owner's rule (2026-10-02): JR East is the city's
largest network inside the city line (13 of 16 station groups); no subway,
tram or light rail (N02 classes 11 and 12 only).

---

## The one-line summary

**All three buckets from the city's own lists: food permits in force on
2026-08-31, rebuilt from the FY-end list (2026-03-31, 5,563 fixed permits)
with five monthly files of new permits AND closures (447 new, 442 matched
closures) to 5,549 in term; restaurant permits 101.0% of the official 5,100.
Barber and beauty registers rebuilt the same way to 2026-08-31 (470, 1,080:
98.5% and 100.7% of official), laundries as of 2026-03-31 (237, 99.6%).**
About one fixed restaurant in nine withheld its address at the operator's
request. The block join places 97.6% of fixed food premises in a bucket and
98.9-99.2% of the registers, none unplaced. Rail: 16 N02 station groups on JR
East's Sagami, Yokohama and Chūō lines, Odakyū's Odawara and Enoshima lines
and Keiō's Sagamihara Line. MHLW's file is opt-in here (7%) and is a control
only.

---

## Business leg — the city's catalogue (生活衛生課, CKAN)

Four datasets, each `license_id: ""` (the dataset page reads
「ライセンスが提示されていません」; the site terms cover them, below). The
resources are zips of CSV plus PDF, **not datastore-backed**, so the checks
are `http_ok` and `http_contains`. Cadence in each dataset's notes:
「年度末現在の施設一覧は年1回（次年度4月）、各月の施設一覧は月1回（当該月の翌月）」
(the laundry dataset: the yearly list only).

| | Food permits (`eigyo_kyoka`, 食品衛生関係施設一覧（食品衛生法：営業許可）) | Barbers (`riyosho`, 理容所施設一覧) | Beauty (`biyosho`, 美容所施設一覧) | Laundries (`cleaning`, クリーニング所一覧) |
|---|---|---|---|---|
| **FY-end list** | resource `1be0eb65-0348-4668-a440-0ce10cad1063`, `…/download/04.zip`: **5,182,542 B** | `a2a1ed31-2e2d-44db-8ddc-d14eb9bdc578`, `…/09.zip`: **400,330 B** | `09e7aa6d-483e-4fa8-8e03-9e9a0575829e`, `…/06.zip`: **656,532 B** | `ddf60c52-d90c-4996-9dd3-2bd508347bad`, `…/12.zip`: **394,944 B** |
| Rows (FY-end) | **5,563 fixed** (自動車による営業を除く, CSV 876,813 B, cp932) + **585 vehicles** (CSV 67,035 B) | **468** (UTF-8 BOM) | **1,082** (UTF-8 BOM) | **237** (cp932): 取次所 135, 一般クリーニング所 96, 無店舗取次店 6 |
| **Monthly, 令和8年度** | `007f1def-2b10-4e5d-81de-18a3e78ec51c` (新規廃業営業許可施設一覧（令和8年度）, `…/download/.zip`): **2,106,061 B**; new AND closed permits in one file per month, told apart by 廃業年月日 | new `2cfb7cf7-b129-457d-a8e3-85110761d8cb` (204,403 B), closed `99a7afc9-a7a3-4f26-b701-89e72e87aeff` (193,688 B) | new `3703be3f-53b9-4824-a103-124834dedf41` (226,811 B), closed `58b2d04d-f3f9-4e25-80e3-d9f5f6fe8c91` (220,900 B) | none |
| Monthly rows | fixed 225 · 177 · 98 · 286 · 123 (Apr-Aug); vehicles 13 · 11 · 22 · 20 · 14 | new: 2 real rows; closed: none (the other files hold one 「該当なし」 row) | new 11 real, closed 8 real | — |
| As of | **2026-03-31** (「令和8年3月31日現在」, uploaded 2026-04-27) + months to **2026-08-31** (August's CSV dated 2026-09-17; resource 2026-09-28) | 2026-03-31 + months to 2026-08-31 | same | **2026-03-31** |

The food dataset also carries 令和7年度 monthly zips (before the base: not
needed) and three correction notices; the one after the base, 「営業許可施設
情報の訂正について（令和8年4月分)」 (`3d62de4a-7e79-4ae1-9835-2ee518ee80f5`,
20,797 B XLSX, fetched), is a 正誤表 of April's 廃業年月日 (11 non-empty rows);
April's CSV in the monthly zip is already the 「R8.6修正版」. Read it at build
to confirm it is applied. **Not fetched, not approved**: the city's food
NOTIFICATION dataset `todokede_eigyo` (届出営業, 2,466,818 B zip plus monthly
files; open call 2).

**Columns.** Food (fixed): **営業所所在地**, 営業所所在地方書, **営業所名称**,
営業所電話番号, 営業者都道府県, 営業者住所, 営業者住所方書, **営業者名**,
営業者役職名, 営業者代表者氏名, 営業者電話番号, 許可年月日, **許可終了日**,
**許可指令番号**, **営業の種類**, **業態**; the monthly files add 許可開始日 and
**廃業年月日**; the vehicle files have 営業区域 (市内一円 on 581 of 585) in
place of the premises address. The header cells carry line breaks
(`許可\n終了日`); `_head` strips them. Barbers and beauty: **施設名称**,
**施設所在地**, 施設所在地方書, 施設電話番号, 検査確認日, 開設者名称,
開設者役職名, 開設者氏名, 開設者住所, 開設者住所方書, 開設者電話番号 (the
closure files add 廃止届出年月日 / 廃止届年月日). Laundries: as barbers with
**種別** and 営業者名称 / 営業者役職名 / 営業者氏名 / 営業者住所 / … .

**Against `japan_register`'s tuples:** `ADDR_COLS` (営業所所在地, 施設所在地),
`NAME_COLS` (営業所名称, 施設名称), `TYPE_COLS` (営業の種類, 種別) and
`FORM_COLS` (業態) are covered. `OPERATOR_COLS` holds 営業者名, 開設者氏名 and
営業者氏名, not 開設者名称, 営業者名称 or 営業者代表者氏名 (below: nothing
measured changes).

### ✅ The rebuild reaches 2026-08-31 — by permit number, with closures (Sakai's shape)

Measured month by month (each month's new permits added, then its closures
removed, by **許可指令番号**, unique on all 5,563 base rows and 447 new rows):

| Step | Fixed permits |
|---|---|
| FY-end list, 2026-03-31 | **5,563** (all in term on that day; newest 許可年月日 2026-03-31) |
| + new permits Apr-Aug (109 · 86 · 49 · 140 · 63; each 許可年月日 inside its month) | **+447** |
| − closures (116 · 91 · 49 · 146 · 60 = 462 rows, 461 numbers; 442 found in the register, the base's or a month's new permit; 19 found nowhere) | **−442** |
| Register | 5,568 |
| − past 許可終了日 on 2026-08-31 with no closure row | −19 |
| **In term on 2026-08-31** | **5,549** |

- **Renewals are a closure plus a new permit**: 301 new rows repeat a base
  row's (address, trade name, type), and 294 of those base permits are closed
  in the months. Of the 211 base permits ending before 2026-08-31, 195 are
  closed in a monthly file; the in-term filter drops the rest. 70 of the 462
  closures are dated on or after their own 許可終了日 (expiries filed as 廃業).
- **Not an upper bound** in Kyoto's or Higashiōsaka's sense: closures are
  published. The page's standing "may include premises that have closed"
  bullet covers late filings (Sakai's page).
- ⚠️ **Do not use `japan_register.rebuilt_register`**: it keys on (address,
  trade name, type) and reads no closures, and the 559 withheld rows (below)
  have a blank address AND a blank name, so they collapse to a handful of keys
  (a first measurement that fell back to that key lost about 445 rows). Copy
  Sakai's `rebuilt_register()` (base + new − closures by 許可番号, then
  `in_term`), with one change: the new and closed rows share a file.
- **Vehicles** rebuilt the same way: 585 → **592** in term (586 restaurant
  permits), all 市内一円: not premises.

### Counts that matter (rebuilt, 2026-08-31)

| Bucket | Rows | Note |
|---|---|---|
| Restaurant permits (飲食店営業, 喫茶店営業), fixed + vehicles | **5,150** (4,564 + 586) | e-Stat 衛生行政報告例 FY2024 in force **5,100** (`japan_official.restaurants`): **101.0%** (FY-end list alone: 5,166, 101.3%) |
| Food service (fixed, addressed) | **2,909** (restaurant 2,906, café 3) | 2,883 distinct (address, trade name) |
| Food retail | **1,063**: 菓子 371 · konbini on a restaurant permit (業態) 248 · supermarket (業態) 156 · deli 97 + 54 by 業態 · fishmonger 69 · butcher 68 | |
| Out (fixed, addressed) | **668**: institutional (業態) 196 · snack bars and cabarets (業態) 173 · manufacturing and other types with no rule 163 · entertainment 41 · inside accommodation 36 · 仕出し 28 · vending 28 · temporary 2 · mail order 1 | |
| Personal services | **barbers 470, beauty 1,078, laundries 231** (in a bucket) | e-Stat FY2024 (第10表, 第11表; the cached `data/hamamatsu/raw/estat_eisei_r6_*_by_city.csv`, row 神奈川県相模原市): 理容所 **477**, 美容所 **1,073**, クリーニング所 **238** (取次所 138): **98.5%**, **100.7%**, **99.6%** of the city's rows (470, 1,080, 237) |

- **Withheld at the operator's request.** 559 FY-end fixed rows (455
  restaurant permits) carry only type, 業態, dates and permit number: every
  premises and operator cell is blank. The list's own PDF says why:
  「営業者が施設情報の非公開を希望した場合は、「営業所所在地」「営業所名称」…を非公開としています」.
  The monthly files carry the same (14 · 26 · 11 · 21 · 12 rows). Of the
  rebuilt fixed restaurant permits (stalls and 一円 rows out) **3,763 of 4,231
  (88.9%) publish an address: about one in nine withholds it.**
  `ADDRESS_BY_CONSENT = {"food"}` counts them apart from not-a-premises
  (Kawasaki's bullet, "About one restaurant in <n> in <City> chose not to have
  its address published in the city's list…").
- **Not a premises**: 283 FY-end rows give 「市内一円」 (業態 屋台型臨時営業 267,
  屋台 and テント variants 16), one address string; `permits_from_rows`
  flags 一円. The vehicle list (営業区域 市内一円) likewise.
- **One premises, several permits**: 55 (address, trade name, type) keys
  repeat in the addressed list (67 rows; 29 differ in 業態): step 2's one pin
  per premises and bucket.
- **Census control** (`japan_official.census()`): the 2021 Economic Census
  counts **1,850** 飲食店 establishments in 14150 (緑区 428, 中央区 750, 南区
  672); 2,883 distinct Food service premises is **1.56 per establishment**,
  the bottom of the built cities' 1.56-1.92. Run
  `scripts/japan_census_control.py` per ward at build.

### MHLW's file — a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=14150_food_business_all.csv`:
**706,831 B, 1,809 rows** (届出 1,318, 許可 478, 許可(廃業) 10, 届出(廃業) 3),
newest 許可年月日 2026-08-31. **380 open restaurant permits, 7.5% of the
official count** (opt-in; the scope's 379), 301 with an address. Of MHLW's
379 addressed open permits, 234 match the rebuilt city list on the exact
normalised address and trade name (256 on the address alone). The city's list
is the source (Toyama's, Kawasaki's and Yokosuka's shape); MHLW's
notifications stay out and the page's standing bullet covers them.

### Against the shared code

- ⚠️ **`city_rows` reads only XLSX members of a zip**; Sagamihara's zips hold
  CSV (and PDF). Either `city_rows` learns CSV members (shared code: re-run the
  Minato control) or the city's `file_rows` reads them; the encodings differ
  inside one dataset (FY-end food, laundry and all monthly CSVs cp932; FY-end
  barber and beauty UTF-8 with BOM: `decode` sniffs both).
- ⚠️ **The rebuild** (above): a `source_rows("food")` on Sakai's pattern, and
  the same for barbers and beauty (new and closed files, keyed on address and
  name: their rows carry no permit number; 該当なし rows skipped).
- `OPERATOR_COLS` + 開設者名称, 営業者名称, 営業者代表者氏名 for completeness
  (companies only; 0 flags either way, measured): re-run the Minato control.
- `REQUIRED_COLUMNS` per source, so a renamed column stops the build.
- Reuses unchanged: the ward parse (addresses start at the ward, 中央区…; not
  ward-less), the 一円 rule, `FORM_RULES` on 業態, the 無店舗 rule on 種別,
  `WAVE2_RULES`, N02-25. `OWN_POINT_FALLBACK` is not available (no own
  coordinates) and not needed (none unplaced).

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

Three wards (14151 緑区, 14152 中央区, 14153 南区): block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/<code>-24.0a.zip` (231,414 ·
120,141 · 118,279 B) and town-chōme `…/19.0b/<code>-19.0b.zip` (6,216 · 6,967
· 6,546 B). **61,517 block keys, 376 town-chōme.**

| Tier | Food, fixed in a bucket (3,972) | Barbers (470) | Beauty (1,078) | Laundries (231) |
|---|---|---|---|---|
| Block | **97.6%** | **98.9%** | **99.2%** | **99.1%** |
| Town-chōme / 大字 centroid | 2.4% (94) | 1.1% | 0.8% | 0.9% |
| Unplaced | **0** | 0 | 0 | 0 |

Food by ward, block: 中央区 **99.9%** (1,511), 南区 **99.4%** (1,405), 緑区
**92.0%** (1,056). Of the 94 chōme-tier food rows, 75 are in 緑区's 大字 (the
former Tsukui towns: 牧野 18, 佐野川 11, 若柳 8, 青根 7, 鳥屋 6, 名倉 5, …),
where MLIT's block edition has few 地番 points; 19 are in 丁目 towns (向原4丁目
14, 相武台1丁目 2): read those misses at build.

**Independent check**: the city's lists carry no coordinates; MHLW's own
points against the block point of their own rows: **median 37 m, 97.8% within
250 m** (361 rows; 2 over 1 km).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (14151-14153)

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_14_GML.zip` (the
shared cache; no Overpass). N03 extent **W 139.066, S 35.475, E 139.459,
N 35.673**; 328.9 km². **19 station records, 16 `N02_005g` groups.** No
Shinkansen station (the Chūō Shinkansen is not in N02).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | Nearest beyond |
|---|---|---|---|---|
| 相模線 (東日本旅客鉄道, 11) | JR Sagami Line | **7 / 18** | 橋本, 南橋本, 上溝, 番田, 原当麻, 下溝, 相武台下 | 入谷 (Zama), 1.7 km |
| 横浜線 (東日本旅客鉄道, 11) | JR Yokohama Line | **5 / 20** | 橋本, 相模原, 矢部, 淵野辺, 古淵 | 相原 (Machida), 1.8 km |
| 中央線 (東日本旅客鉄道, 11) | JR Chūō Main Line | **2 / 75** | 相模湖, 藤野 | 上野原 (Yamanashi), 3.3 km; 高尾 (Hachiōji), 9.0 km |
| 小田原線 (小田急電鉄, 12) | Odakyū Odawara Line | **2 / 47** | 相模大野, 小田急相模原 | 町田, 1.5 km |
| 江ノ島線 (小田急電鉄, 12) | Odakyū Enoshima Line | **2 / 17** | 相模大野, 東林間 | 中央林間 (Yamato), 1.4 km |
| 相模原線 (京王電鉄, 12) | Keiō Sagamihara Line | **1 / 12** | 橋本 (the terminus) | 多摩境 (Machida), 2.2 km |

- **Groups by operator**: JR East 13, Odakyū 3, Keiō 1 (the master list's
  "JR 14, Odakyū 4" counts line-station records: 橋本 is on two JR lines,
  相模大野 on two Odakyū lines). **橋本** is ONE group for JR's two lines and
  Keiō (147 m wide); **相模大野** one group for both Odakyū lines. No name in two
  groups. Median nearest-group gap **1,542 m** (min 975 m, 矢部-淵野辺):
  **standard rings**.
- **Stub test.** **Keiō Sagamihara, 1 of 12: the one-station stub rule
  applies, and it stays as cut** (standing call; Kobe's JR Takarazuka Line,
  1 of 30, an urban line too, stayed cut). Its only station, 橋本, is a JR
  interchange in the same group, so the ring exists either way; the drawn
  stub runs from 橋本 to the city line. **Three lines are cut to two
  stations: the Chūō Main Line (2 of 75), Odakyū Odawara (2 of 47) and Odakyū
  Enoshima (2 of 17)**: not one-station stubs, so the urban-stub clause sends
  them to the owner (open call 1). The Sagami (7 of 18) and Yokohama (5 of 20)
  lines are not stubs.
- **The Chūō Line's two stations are the city's rural far west** (相模湖 at
  139.19 E, 藤野 at 139.15 E, about 15 km west of 橋本, the former Sagamiko and
  Fujino towns, merged 2007): the JR section west of 高尾, local trains only.
- **Frequencies: ASSERTED, not read from a timetable at Step 0**: the
  Yokohama Line and both Odakyū lines are frequent urban lines; the Sagami
  Line is single-track at roughly 3 trains an hour; the Chūō Line at 相模湖 and
  藤野 roughly 2 to 4 an hour (Takao-Ōtsuki locals). Read JR East's station
  timetables for 相模湖 and 番田 at build.
- **The light-rail / rail test** (`japan-city`, owner 2026-10-02): no subway,
  tram or light rail; JR is the largest network (13 of 16 groups), so JR
  reads as metro: **`mode: "metro"`**.
- ⚠️ **Names**: 中央線 here is the Chūō Main Line (中央本線), not Tokyo's Chūō
  Rapid route; Kawasaki already labels "Keio Sagamihara Line" and "Odakyu
  Odawara Line" (reuse its spelling and, where both maps show a line, a
  matching colour).
- ⚠️ **Gate 3** (JR East, Odakyū, Keiō station lists) and **OSM `name:en`**
  (one Overpass station query in the box 35.47-35.68 N, 139.06-139.46 E) at
  build; no tram stops.

## Scope

**Sagamihara City (3 wards).** Every line runs on into Machida and Hachiōji
(Tokyo), Zama, Ebina or Yamato (Kanagawa), or Uenohara (Yamanashi); cut at the
line, the stations beyond named by N03 municipality at build. None of those
is built (Tokyo's map is the 23 wards). Built Kawasaki lies east beyond
Machida, built Yokohama south-east.

## Licences — read 2026-10-04 (cited, not re-run)

- **The city's catalogue — PERMITTED WITH CONDITIONS (CC BY 4.0)**, the
  licence read of 2026-10-04 recorded in the master list row (Band A) and
  `docs/decisions_drafts/staging.md` ("Sagamihara to A"); **no row in
  `docs/data_sources/japan.md` yet** (staging records it). As read on the
  dataset pages today: 「ライセンスが提示されていません」 on all four
  (`license_id: ""`); the city's open-data page
  (`https://www.city.sagamihara.kanagawa.jp/shisei/toukei/opendata/index.html`):
  「本サイトで公開されているデータはクリエイティブ・コモンズ 表示 4.0 国際 ライセンスの下で提供されています。」,
  linking 相模原市オープンデータ利用規約 (`…/_res/projects/default_project/_page_/001/005/928/opendata_kiyaku_20180328.pdf`,
  12,027 B, 「最終更新日：平成30年3月28日」).
- **The quotes checked against the terms PDF (2026-10-04).** The PDF's text
  layer does not extract here (pdftotext lacks the Adobe-Japan1 CMap; pypdf
  is not installed), so its three pages were rendered with Windows' own PDF
  renderer and read; the text-layer fragments (the URL, 「相模」, 「4.0」,
  「[ データベ ]」, 「著作物を」) agree. Every point the read recorded holds:
  - §1: 「サービスのご利用をもって本規約の内容を承諾したものとみなします。」;
    「本規約の内容は、必要に応じて予告なしに変更することがあります」: **re-read
    before each refresh.**
  - §2: 「本サイトが他のホームページ中に組み込まれるような設定はしないでください。」
    (no framing of the catalogue).
  - §3(2): 「本サイトで公開しているデータの著作権は、クリエイティブ・コモンズ・ライセンス
    表示 4.0のもとでライセンスされています。」 (the terms say 表示 4.0; the web
    page adds 国際).
  - §4: claims from the user's breach or a third party's rights are settled
    「利用者自身の費用と責任で」; §5: costs the city incurs from them
    (賠償金の支払を含む) are reimbursed by the user: **accepted by the owner on
    Sakai's precedent (2026-10-04).** §7: Japanese law, 横浜地方裁判所.
  - **§3(3), the credit forms, exactly as the PDF gives them.** Unmodified:
    `[ライセンスされている著作物のタイトル]、相模原市、クリエイティブ・コモンズ・ライセンス 表示 4.0（http://creativecommons.org/licenses/by/4.0）`.
    **Modified (改変), which a map is:**
    `この[作品・アプリ・データベース等]は以下の著作物を改変して利用しています。`
    then `[ライセンスされている著作物のタイトル]、相模原市、クリエイティブ・コモンズ・ライセンス 表示 4.0（http://creativecommons.org/licenses/by/4.0）`.
    And: 「なお、ライセンスの URL は文字で記載するのではなく、「クリエイティブ・コモンズ・ライセンス
    表示 4.0」の文字部分などにハイパーリンクを貼る方法で提供することも可能です。」
    (bracket widths as rendered.)
- **MUST DISPLAY** (the 改変 form, filled as Kawasaki's and Higashiōsaka's):
  `この地図は以下の著作物を改変して利用しています。食品衛生関係施設一覧（食品衛生法：営業許可）、相模原市、クリエイティブ・コモンズ・ライセンス 表示 4.0（http://creativecommons.org/licenses/by/4.0）`,
  and likewise `理容所施設一覧`, `美容所施設一覧`, `クリーニング所一覧`.
- **MUST NOT**: frame the catalogue (§2); claim completeness or accuracy (§4);
  imply endorsement (CC).
- **MHLW open data** (control only): PDL 1.0 (`docs/data_sources/japan.md`);
  no notice unless a row or point is used.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**:
  CC BY 4.0, picks stations, ⛔ never drawn.

## Privacy

Select only 営業所名称 / 施設名称, 営業の種類 / 種別, 業態, the premises address
and the dates. **Never select** 営業所電話番号, 施設電話番号, 営業者住所,
開設者住所, 営業者電話番号, 開設者電話番号 or the representatives' names
(営業者代表者氏名, 開設者氏名, 営業者氏名: a company representative's own name).

**The name rule has nothing to compare for an individual.** Every list names
an operator only where it is a company: the food list's 営業者名 is filled on
2,791 of 5,004 addressed FY-end rows, each with a company marker (2,769), a
組合 (13) or a public body (9), and blank with every other operator cell on
the rest; the registers' 開設者名称 / 営業者名称 are filled on 54 of 468
barbers, 306 of 1,082 salons and 134 of 237 laundries, every one a company.
The rule flags **2** food rows (a 組合 and a public body: neither a person;
`"coop"` takes the first) and **0** register rows. A sole trader's trade
name cannot be checked: **Kawasaki's bullet, "…names an operator only where
it is a company, so this cannot be checked for the rest", for every layer**
(Toyama's position, accepted 2026-10-02). Run `check_personal_exposure.py`
with `japan=True`. No row value went into this brief.

## Region

Japan East (minor tier, above); `"country": "Japan"`. Project to **UTM 54N
(EPSG:32654)** (longitude 139.07 to 139.46, all in zone 54).

**Scaffold** (a page number claimed in `docs/session_roles.md` at build, not
here): `scaffold_city.py --slug sagamihara --name Sagamihara --system-name
"JR East, Odakyu and Keio" --taxonomy japan_eigyo --lat 35.5815 --lon
139.3706 --region "Japan East" --country Japan --mode metro --page-number <N>`
(`--dry-run` first; the marker is 相模原 station's N02 point). `japan.CITIES`
gains `"sagamihara": {"name": "相模原市", "pref": "14", "epsg": 32654, "n02":
"25", "rules": WAVE2_RULES, "wards": ["14151", "14152", "14153"]}`.

## Owner calls

**Made** (standing or on precedent): the six Japanese calls above; the
Keiō Sagamihara Line's one-station stub stays as cut; Kawasaki's name-rule
bullet for every layer; MHLW as a control only; the minor tier and Japan
East; `mode` metro; §4 and §5 accepted (2026-10-04).

✅ **Both answered as recommended (owner, 2026-10-05, "7 yes, 8 yes";
`docs/decisions_drafts/staging.md`):** the Chūō Line and both Odakyū lines
are drawn as cut, the Chūō Line's timetable read at the build and recorded;
the notification list stays out, and nothing of it is downloaded.

**Were open:**

1. **Three lines cut to two stations: JR's Chūō Main Line (相模湖, 藤野; 2 of
   75), Odakyū Odawara (相模大野, 小田急相模原; 2 of 47), Odakyū Enoshima
   (相模大野, 東林間; 2 of 17).** **Recommendation: draw all three as cut**,
   on Kawasaki's (Keikyū Main 2 of 50, Keiō 2 of 12), Higashiōsaka's (Chūō
   Line 2 of 12) and Nishinomiya's precedent: each station is a real centre
   with business data, 相模大野 is the city's busiest interchange, and the
   lines run on into unbuilt Machida and Zama. Tradeoff for the Chūō Line:
   its two stations are rural and 15 km from the rest, which widens the map
   westward; leaving it out (`LEFT_OUT_LINES`, Shimonoseki's San'in precedent)
   would cost two rings and the far west's only stations, and Shimonoseki's
   was 8 to 10 trains a day against an ASSERTED 2 to 4 an hour here (read the
   timetable before the owner answers).
2. **The city's food NOTIFICATION list** (`todokede_eigyo`, 届出営業: 2.47 MB
   FY-end zip and monthly files, same publisher and site terms).
   **Recommendation: leave it out** (Kawasaki's, Yokosuka's and
   Higashiōsaka's shape; the page's standing bullet says notification-only
   businesses are not shown). Tradeoff: Yokkaichi took its own notifications
   as partial food retail (greengrocers, konbini without a permit); taking it
   is a new download for the owner to approve and a partial bucket to
   disclose.

## What the build must still measure

- The rebuild through step 2 (5,549 in term; 5,150 restaurants, 101.0%),
  pinned `as_of = 2026-08-31` (the newest month's end, never today); the April
  正誤表 against the R8.6 April file; `SOURCE_AS_OF` (food, barbers, beauty
  2026-08-31; laundries 2026-03-31).
- The withheld share through `ADDRESS_BY_CONSENT` (one in nine measured here)
  and the 緑区 chōme-tier misses (向原4丁目, 相武台1丁目).
- The census control per ward; the 菓子 / そうざい factory share (step 2
  prints it); `docs/category_rules.md` for anything new in 業態.
- Gate 3, OSM `name:en`, line colours on both basemaps (Kawasaki's for the
  shared Keiō and Odakyū lines), JR timetables for 相模湖 and 番田, the macro
  label beside Kawasaki's.
- The `docs/data_sources/japan.md` row and notice (staging records the
  licence read; the build writes the notice with the 改変 credit above).
- ⚠️ The files are replaced in place (the monthly zips grow each month under
  the same resource id, the FY-end zip each April): the fetch reads each
  resource's current URL from `package_show` (Yokosuka's `SOURCE_RESOURCES`),
  and the checks below pin today's sizes as floors.

```brief-checks
[
  {
    "id": "sagamihara-food-fyend-live",
    "claim": "The FY-end food-permit zip (2026-03-31) is keyless and live on the city's catalogue",
    "kind": "http_ok",
    "url": "https://opendata.city.sagamihara.kanagawa.jp/dataset/3bd39977-a8cd-49d5-8160-48c0620acf11/resource/1be0eb65-0348-4668-a440-0ce10cad1063/download/04.zip",
    "min_bytes": 5000000
  },
  {
    "id": "sagamihara-food-monthly-live",
    "claim": "The 令和8年度 monthly food zip (new and closed permits, April to August 2026) is live",
    "kind": "http_ok",
    "url": "https://opendata.city.sagamihara.kanagawa.jp/dataset/3bd39977-a8cd-49d5-8160-48c0620acf11/resource/007f1def-2b10-4e5d-81de-18a3e78ec51c/download/.zip",
    "min_bytes": 2000000
  },
  {
    "id": "sagamihara-food-record",
    "claim": "The food dataset declares no licence and lists the FY-end and 令和8年度 monthly resources (package_show escapes Japanese, so ASCII only)",
    "kind": "http_contains",
    "url": "https://opendata.city.sagamihara.kanagawa.jp/api/3/action/package_show?id=eigyo_kyoka",
    "present": ["\"license_id\": \"\"", "1be0eb65-0348-4668-a440-0ce10cad1063", "007f1def-2b10-4e5d-81de-18a3e78ec51c", "3d62de4a-7e79-4ae1-9835-2ee518ee80f5"]
  },
  {
    "id": "sagamihara-food-page-no-licence",
    "claim": "The food dataset page states no licence and the yearly-plus-monthly cadence",
    "kind": "http_contains",
    "url": "https://opendata.city.sagamihara.kanagawa.jp/dataset/eigyo_kyoka",
    "present": ["ライセンスが提示されていません", "各月の施設一覧は月1回", "新規廃業営業許可施設一覧（令和8年度）"]
  },
  {
    "id": "sagamihara-barber-fyend-live",
    "claim": "The FY-end barber zip (2026-03-31) is live",
    "kind": "http_ok",
    "url": "https://opendata.city.sagamihara.kanagawa.jp/dataset/a8a6040a-dfff-430c-a66c-a345f40d3c9d/resource/a2a1ed31-2e2d-44db-8ddc-d14eb9bdc578/download/09.zip",
    "min_bytes": 300000
  },
  {
    "id": "sagamihara-barber-record",
    "claim": "The barber dataset declares no licence and lists the FY-end, 令和8年度 new and 令和8年度 closed resources",
    "kind": "http_contains",
    "url": "https://opendata.city.sagamihara.kanagawa.jp/api/3/action/package_show?id=riyosho",
    "present": ["\"license_id\": \"\"", "a2a1ed31-2e2d-44db-8ddc-d14eb9bdc578", "2cfb7cf7-b129-457d-a8e3-85110761d8cb", "99a7afc9-a7a3-4f26-b701-89e72e87aeff"]
  },
  {
    "id": "sagamihara-beauty-fyend-live",
    "claim": "The FY-end beauty-salon zip (2026-03-31) is live",
    "kind": "http_ok",
    "url": "https://opendata.city.sagamihara.kanagawa.jp/dataset/7b1f33cd-f485-4065-8eaa-f7df440b09a8/resource/09e7aa6d-483e-4fa8-8e03-9e9a0575829e/download/06.zip",
    "min_bytes": 500000
  },
  {
    "id": "sagamihara-beauty-record",
    "claim": "The beauty dataset declares no licence and lists the FY-end, 令和8年度 new and 令和8年度 closed resources",
    "kind": "http_contains",
    "url": "https://opendata.city.sagamihara.kanagawa.jp/api/3/action/package_show?id=biyosho",
    "present": ["\"license_id\": \"\"", "09e7aa6d-483e-4fa8-8e03-9e9a0575829e", "3703be3f-53b9-4824-a103-124834dedf41", "58b2d04d-f3f9-4e25-80e3-d9f5f6fe8c91"]
  },
  {
    "id": "sagamihara-laundry-fyend-live",
    "claim": "The laundry zip (2026-03-31, yearly only) is live",
    "kind": "http_ok",
    "url": "https://opendata.city.sagamihara.kanagawa.jp/dataset/e9b089bf-540a-4337-b5b2-ac3140ee2eb9/resource/ddf60c52-d90c-4996-9dd3-2bd508347bad/download/12.zip",
    "min_bytes": 300000
  },
  {
    "id": "sagamihara-laundry-record",
    "claim": "The laundry dataset declares no licence and lists its yearly list",
    "kind": "http_contains",
    "url": "https://opendata.city.sagamihara.kanagawa.jp/api/3/action/package_show?id=cleaning",
    "present": ["\"license_id\": \"\"", "ddf60c52-d90c-4996-9dd3-2bd508347bad"]
  },
  {
    "id": "sagamihara-od-page-cc-by",
    "claim": "The city's open-data page grants CC BY 4.0 and links the 2018-03-28 terms PDF (ASCII only: the page is served without a charset)",
    "kind": "http_contains",
    "url": "https://www.city.sagamihara.kanagawa.jp/shisei/toukei/opendata/index.html",
    "present": ["opendata_kiyaku_20180328.pdf", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "sagamihara-terms-pdf-live",
    "claim": "The terms PDF of 2018-03-28 (相模原市オープンデータ利用規約) still answers at its dated name",
    "kind": "http_ok",
    "url": "https://www.city.sagamihara.kanagawa.jp/_res/projects/default_project/_page_/001/005/928/opendata_kiyaku_20180328.pdf",
    "min_bytes": 10000,
    "content_type_contains": "pdf"
  },
  {
    "id": "sagamihara-mhlw-live",
    "claim": "MHLW's open-data file for Sagamihara (14150) answers a plain keyless GET (the control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=14150_food_business_all.csv",
    "min_bytes": 500000
  },
  {
    "id": "sagamihara-isj-midori-live",
    "claim": "MLIT's block-level address file for 緑区 (14151) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/14151-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "sagamihara-isj-chuo-live",
    "claim": "MLIT's block-level address file for 中央区 (14152) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/14152-24.0a.zip",
    "min_bytes": 80000
  },
  {
    "id": "sagamihara-isj-minami-live",
    "claim": "MLIT's block-level address file for 南区 (14153) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/14153-24.0a.zip",
    "min_bytes": 80000
  },
  {
    "id": "sagamihara-projected-crs",
    "claim": "Sagamihara projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.37,
    "expect": "EPSG:32654"
  }
]
```
