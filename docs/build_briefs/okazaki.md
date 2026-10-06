# Okazaki — build brief

**Band B, food only (Hiroshima's shape), owner-approved 2026-10-06** (Japan
wave 4, banded in staging's wave 5, call 49: `docs/decisions_drafts/staging.md`,
"Wave 5: the ranked queue and the pre-verdicts screened"). The Step 0
downloads were approved by the owner 2026-10-06 (call 67). **Step 0 measured
2026-10-06** (staging). Into `data/okazaki/raw/` (gitignored), each from its
publisher's own host with the project user-agent, each HTTP 200, under the
names a build's `fetch_sources.py` would use:

- From `data.bodik.jp` (one request; BODIK spacing kept): the city's food list
  `232025_food_business_all.csv` (**1,097,449 B**; resource
  `a893c7d6-5c10-4fb4-b9fa-cb48edd81565`, modified 2026-09-11; BODIK serves it
  as `232025_food_business_al.csv`, the city's own truncation).
- From `i2fas.mhlw.go.jp`: `23202_food_business_all.csv` (281,861 B), a
  control, and the source of open-call-free layers under calls 127b and 127c.
- From `nlftp.mlit.go.jp`: `isj/23202-24.0a.zip` (590,537 B) and
  `isj/23202-19.0b.zip` (10,553 B).

**1,980,400 B in all.** Nothing else was downloaded. Pages read by plain GET
for frequency (pages, not data files): the Aichi Loop Railway's timetable
index and 北野桝塚 station page, and that station's timetable PDF (57,627 B,
into the scratchpad); three Meitetsu timetable pages, which did not reach an
Okazaki station (the Meitetsu figures below are the probe's).

**Run `python scripts/brief_check.py okazaki` before writing any code.** Then
the `japan-city` skill, **Hiroshima's shape** for a food-only page
(`docs/build_briefs/hiroshima.md`: Food service and Food shops, no personal
services) on **one complete city list** in the national 自治体標準 schema
(Matsuyama's columns), Toyota's layout for an Aichi city on Meitetsu and the
Aichi Loop (`docs/build_briefs/toyota.md`). Coordinates: the `address-join`
skill, measured with `pipeline/countries/japan_register.py` from scratch
scripts only (`scripts/screen_japan_join.py` has no Okazaki entry; its table
is shared code and was not edited). Rail: MLIT N02-25 cut at the N03 city
line, measured through `pipeline/countries/japan.py` with a scratch `CITIES`
entry. Read `cjk-text` too: the list carries a Hangul code point standing in
for a place-name character (below).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none in the city); (2) **lines served only by limited expresses
DO count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27); an URBAN line cut to ONE
station is left out (owner, 2026-10-06, calls 54 and 92; none here); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor
for JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at
about 11 trains a day or fewer drawn and named (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from
OSM `name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04);
**市内一円 rows are not premises** (Kobe's trap 6, 2026-09-27).

**✅ Applied from today's precedents (do not re-ask):** **the food share
stated on the page** (Ichinomiya, call 125): 3,023 restaurant permits,
**80.5%** of e-Stat's 3,755 in force; **MHLW's notifications as a partial
Food-shops layer** (call 127b: 349 addressed, hundreds, unlike Iwaki's 164);
**MHLW's own point where the block join misses** (call 127c); **tiers
disclosed where the block share is low** (call 145, Kakogawa's way) if the
build ends near the 87.1% measured as is.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Okazaki
carries `label_tier: "minor"` and goes in the **Japan East** view, as Toyota
and Ichinomiya do (`app/cities.py`); wave 4's first city to land retags Japan
into the eight regions, Okazaki into **Chubu**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye:
Toyota's dot is its neighbour to the north, so measure the two together.

**`mode`: `metro`** (the owner's rule of 2026-10-02, applied as for Toyota and
Ichinomiya): JR is not the largest network inside the city (2 station groups
against Meitetsu's 9 and the Aichi Loop's 6), and no subway or tram is drawn;
the backbone is two heavy-rail networks (N02 class 12).

---

## The one-line summary

**Food only, from one city CSV on BODIK (CC BY 4.0 as stated; the licence
read is pending, staging records it): every food permit in term on
2026-08-31, 4,022 rows, 3,023 飲食店営業 = 80.5% of e-Stat's 3,755 in force**
(vehicles included, the Tokyo brief's measure). **210 restaurant permits are
kitchen cars** (許可条件 「自動車による営業に限る（愛知県内有効）」), listed at a
base address: at fixed premises **2,813 restaurants (74.9%)** plus 2 old-law
喫茶店, and 819 food-shop permits. **The address is in `所在地_連結表記`**
(4,022 filled); 緯度, 経度, 廃業年月日, 申請区分 and the split address columns
(都道府県, 市区町村, 町字, 番地以下) are empty on every row, as the probe saw in
20. Old-law permits are IN (378 granted 2020-08-03 to 2021-05-31), so
Kurashiki's trap does not apply. MHLW holds 126 open permits, **123 in the
city's list by number and date**. Block join **87.1%** as is, **92.7%** with
two proposed rules (unplaced 3.8% to 1.2%). **Rail: 16 station groups**
(Meitetsu 9, Aichi Loop 6, JR 2, 岡崎 shared by JR and the Aichi Loop); no
stretch near 11 trains a day.

---

## Business leg — 食品等営業許可・届出一覧 (BODIK organisation 232025)

Dataset `https://data.bodik.jp/dataset/232025_food_business_all`
(「食品等営業許可・届出一覧（自治体標準オープンデータセット）」; author and
maintainer 岡崎市保健部生活衛生課; `license_id` `cc-by-40-intl`; metadata
modified 2026-09-11; BODIK lists 11 datasets for the city, none of them
personal services). The city's own dashboard
(`https://odcs.bodik.jp/232025/dashboard/`) visualises the same file.

| File | Bytes | Rows | What it is |
|---|---|---|---|
| `232025_food_business_all.csv` (resource `a893c7d6-…`) | **1,097,449** | **4,022** | every permit in term on 2026-08-31 (newest grant 2026-08-31); replaced in place |

- **Encoding UTF-8 with BOM, CRLF**, header on line 1; `city_rows` reads it
  as it stands. Dates ISO `2026-08-31`.
- **Columns (34, the 自治体標準 schema)**: 全国地方公共団体コード, ID, 地方公共団体名,
  **施設名称**, 施設名称_カナ, 施設名称_英字, **営業の種類**, 業態,
  所在地_全国地方公共団体コード, 町字ID, **所在地_連結表記**, 施設所在地_都道府県,
  施設所在地_市区町村, 施設所在地_町字, 施設所在地_番地以下, 施設方書 (992 filled),
  緯度, 経度, 施設電話番号 (2,957), 連絡先メールアドレス, 連絡先FormURL,
  連絡先備考, 郵便番号, **法人名** (2,121), 法人番号, **許可番号**, 初回許可年月日,
  **許可年月日**, 許可開始日, **許可満了日**, 廃業年月日, 申請区分, **許可条件**
  (234), 備考. **Empty on every row**: ID, 施設名称_英字, 業態,
  所在地_全国地方公共団体コード, 町字ID, the four split address columns, 緯度,
  経度, the three contact columns, 郵便番号, 法人番号, 廃業年月日, 申請区分, 備考.
- **The address column**: 所在地_連結表記 holds the whole address, `愛知県岡崎市…`
  on all 4,022 (4,010 exactly so; 12 differ in spacing or form), the building or unit
  in 施設方書. Already in the shared `ADDR_COLS`; `NAME_COLS` has 施設名称,
  `TYPE_COLS` 営業の種類, `OPERATOR_COLS` 法人名. No shared tuple needs a name.
- **Types (31)**: 飲食店営業 3,023; 菓子製造業 486; そうざい製造業 138; 食肉販売業 94;
  魚介類販売業 89; 調理の機能を有する自動販売機… 48; 漬物製造業 20; 食肉処理業 19;
  アイスクリーム類製造業 18; 食品の小分け業 13; 麺類製造業 12; 密封包装食品製造業 11;
  乳類販売業 9; 複合型そうざい製造業 3; 喫茶店営業 2; and 16 smaller manufacturing
  types. Old-law-only names present: 乳類販売業 9, 喫茶店営業 2, 食肉製品製造業 2,
  缶詰又は瓶詰食品製造業 1.
- **許可条件 (234 rows)**: 「自動車による営業に限る（愛知県内有効）」 210 (all
  飲食店営業), 「自動販売機による営業に限る」 13 (the cooking vending machines),
  「ソフトアイスクリーム類の製造に限る」 10, 「簡易な営業に限る」 1.

### Kitchen cars: listed at a base, not premises

**The 210 vehicle permits** carry a base address (192 with a street number;
33 read `…(主たる営業場所)` at a riverbank or park, e.g. 康生町乙川左岸, all 33
vehicles). All run 5 years (fixed restaurants run 6). `permits_from_rows`
does not read 許可条件, and 業態 is empty, so they would be pinned at their
bases. **Hiroshima's hook takes them out** (`pipeline/hiroshima/config.py`,
`source_rows`): carry 許可条件 into 業態, where `japan_eigyo`'s FORM_RULES
already read 自動車 as "temporary / mobile" (measured: 210 out) and
自動販売機 as vending (13, already out by type); the other two conditions
match no form rule and change nothing. City-local, as Hiroshima's.

### Counts against the official stock

e-Stat 衛生行政報告例 FY2024 (`japan_official.estat()`), 愛知県岡崎市, in force
2025-03-31. The share is the list's rows against old law plus revised law.

| Type | The list (2026-08-31) | e-Stat (old + revised) | Share |
|---|---|---|---|
| **飲食店営業, every row (vehicles included, the Tokyo brief's measure)** | **3,023** | **3,755** (1,082 + 2,673) | **80.5%** |
| … at fixed premises (vehicles out) | 2,813 | 3,755 | 74.9% |
| 菓子製造業 | 486 | 541 (219 + 322) | 89.8% |
| そうざい製造業 + 複合型 | 141 | 131 (15 + 115 + 1) | 107.6% |
| 食肉販売業 | 94 | 106 (52 + 54) | 88.7% |
| 魚介類販売業 | 89 | 110 (57 + 53) | 80.9% |
| 喫茶店営業 (old law only) | 2 | 109 (105 of them vending machines) | n/a |
| Every permit type | 4,022 | 4,944 (1,599 + 3,345) | 81.4% |

- **The restaurant stock is growing**, so the gap is not a shrinking city:
  3,466, 3,447, 3,572, 3,755 at FY2021 to FY2024 (old law 2,869, 2,185,
  1,603, 1,082; revised 597, 1,262, 1,969, 2,673).
- **Old-law coverage (Kurashiki's trap): present.** 378 permits (263
  restaurants) were granted 2020-08-03 to 2021-05-31, every one for 6 years,
  ending 2026-08-31 to 2027-05. An old-law permit granted before 2020-08 on
  the same term had lapsed by the list's date, so the old law's stock
  (1,082 restaurants at 2025-03-31) converting into revised-law permits
  explains why few remain; nothing suggests old-law permits are left out.
- **The list does not hold every revised-law permit.** e-Stat's FY2024 flow
  table (第３表－２) records **1,126 revised-law permits granted** (継続 2,
  新規 1,124, every type) and **238 closures**, and its stock moves by exactly
  that (2,459 + 1,126 - 238 = 3,347 against 3,345): permits do not leave the
  stock by lapsing. The list holds **693 permits granted in FY2024** (503
  restaurants), **61.7%** of the grants, an upper bound on what it misses
  since some closed after 2025-03-31. Revised-law grants from 2021-06-01 to
  2025-03-31 still listed: 2,506 against e-Stat's 3,345 at 2025-03-31. The
  dataset page gives no reason. MHLW's sample cannot test it: its permits
  are filed online by operators who opt into publication, and the city
  lists 123 of its 126. **So the share is stated (call 125)**: about four
  restaurant permits in five of the official count.
- **Closed premises: no column, and the list holds only permits in term**
  (no 許可満了日 before 2026-08-31; 28 end on it; 29 begin on 2026-09-01).
  Unreported closures stay invisible, so the page keeps the standing "may
  include premises that have closed" bullet. MHLW holds no closure row
  (no 廃業 of either kind) to test it.
- **Duplicates**: no exact repeats; 許可番号 (shape `NNN-NN-NNN-NNNN`) is
  unique on all 4,022 rows. 75 groups (174 rows, 64 restaurant groups) repeat
  an (address, trade name, type), 71 of them with the same 方書 too; 19 groups
  are handovers (the older permit ends within about 4 months of the newer
  grant). One pin per premises (trap 7) takes them: **2,936 distinct
  (address, trade name) restaurants**. 55 addresses hold five or more
  restaurant rows (490 rows).
- **Through `japan_eigyo`** (with the vehicle hook): **Food service 2,815**
  (2,813 restaurants + 2 喫茶店), **Retail 819** (菓子 486, そうざい 141, 食肉販売
  94, 魚介類販売 89, 乳類販売 9); out: vehicles 210, vending 48, "no rule" 130
  (manufacturing types, as everywhere).
- ⚠️ **No 業態, so `FORM_RULES` sees only 許可条件**: konbini, supermarkets,
  kitchens and hotel restaurants holding 飲食店営業 stay in Food service. By
  trade-name word among fixed restaurants (counts only): konbini 174 (6.2% of
  2,813), supermarkets 100, kitchens 25, hotels and inns 21; bars and snacks
  71. Kobe's, Osaka's and Aomori's lists have no 業態 either; the build
  follows them.
- ⚠️ **Economic Census control** (`scripts/japan_census_control.py` at build):
  the 2021 census counts **1,257** 飲食店 establishments in 23202; 2,642
  distinct placed food-service premises (as-is join) is **2.10 per
  establishment**, above the built cities' 1.56-1.92, beside Akita's 2.11 and
  Aomori's 2.33. Read at build; not a blocker on precedent, but the page
  must not imply one dot is one establishment.

### MHLW's file (23202): control, partial food shops and points

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=23202_food_business_all.csv`:
**281,861 B, 799 rows** (届出 673, 許可 126; no 廃業 row), UTF-8 with BOM, the
national schema (営業施設名称、屋号又は商号, 営業の種類, 業態, 営業施設所在地,
営業施設方書, 緯度 / 経度, 法人名, 法人番号, 法人住所, phones, permit dates,
廃業年月日, 申請区分, 許可条件). Permits granted 2021 to 2026 (34 in 2026).

- **The city enters every online permit**: 123 of MHLW's 126 open permits are
  in the city's list by the number's last digits and the grant date (MHLW
  writes a one-digit prefix, 第, the number and 号); 3 match a number under another date (2 of them
  restaurants), most likely the same permits: nothing added (Ichinomiya's
  127a).
- **Notifications (call 127b, applied): 673 open, 349 addressed** (348 with a
  point): その他の食料・飲料販売業 183, cup vending 164, other vending 145,
  百貨店・総合スーパー 83, コーヒー製造・加工業 17, コンビニエンスストア 11, 集団給食施設
  11, 野菜果物販売業 10 (業態 ドラッグストア 66, スーパーマーケット 13 among the
  addressed). Through `japan_eigyo`, **250 addressed rows reach Retail**
  (other food and drink sales 145, department store / supermarket 79,
  greengrocer 8, konbini 7, rice 3 …); out: vending 57, no rule 21, catering
  9, mobile 6. They join at block 86.4%, chōme 4.4%, unplaced 9.2%. **A
  partial, opt-in Food-shops layer**, Matsuyama's, Akita's and Ichinomiya's
  precedent; the page calls it partial and MHLW's credit goes on the notice.
- **Its own coordinates (call 127c, applied)**: block point against MHLW's
  point for 379 addressed open rows at block, **median 47 m, 93.4% within
  250 m**, 5 over 1 km. Of the city's 264 non-block rows in a bucket, **14**
  have an MHLW permit twin (same number and grant date) with a point.

### Personal services: none published

BODIK's 11 datasets for the city carry no barber, beauty or laundry list,
and the city's 理容・美容・クリーニング page (`/business/eigyo/1005587/index.html`,
page 1005587) carries procedures and forms only. The master list's row
records that the beauty list appears to be given only on request; **no
outreach** (owner). So the page is **food only**, Hiroshima's shape: "**This
map shows food businesses only.**"

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/23202-24.0a.zip` (590,537 B,
**102,947 block keys**), town-chōme `.../19.0b/23202-19.0b.zip` (10,553 B,
**362**). `japan.CITIES` entry at build: `"okazaki": {"name": "岡崎市", "pref":
"23", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
"wards": ["23202"]}`.

| Tier (fixed premises in a bucket, vehicles out) | As is (3,634) | Food service (2,815) | Retail (819) | **With O1 + O2** (3,634) |
|---|---|---|---|---|
| Block | **87.1%** | 86.9% | 87.7% | **92.7%** |
| Town-chōme / 大字 centroid | 9.1% | 9.3% | 8.7% | 6.0% |
| Unplaced | **3.8%** (138) | 3.8% | 3.7% | **1.2%** (45) |

**The misses, read** (town names and masked shapes only), and two proposed
rules, measured in a scratch copy (shared code not edited):

- **O1: MLIT keys central towns as 大字 + 小字** (`康生通字西4丁目`,
  `稲熊町字3丁目`, `伊賀町字5丁目`), where the list writes `康生通西4-5-6` and
  `稲熊町字3-4-5`. Where `<stem>字<rest><n>丁目` is a block town and the parsed
  town is `<stem><rest>` (or ends in 字), read the first number as the 丁目.
  Rewrote 202 rows (康生通 106, 稲熊町 49, 伊賀町 17, 井田町 9, 梅園町 8, 小呂町
  7, 六供町 6): 康生通's 90 unplaced, the city's central shopping street,
  reach a block. **Shared code** (`join_city` or `norm_town`), followed by
  the Minato control and every city screen.
- **O2: U+B743, a Hangul code point, stands in 20 addresses** at
  `戸崎町字<U+B743>山` (17 at the chōme tier, 3 unplaced), and in 2 trade
  names. MLIT's block file and MHLW's own rows (3) write the place
  `戸崎町字ばら山`; read the code point as ばら there and the 20 reach a block.
  The city's file has substituted a character its system could not encode
  (the `cjk-text` skill's territory). **City-local**, in `source_rows`, as
  Ichihara's half-width fix (call 124).
- **Still unplaced after both (45)**: new 住居表示 towns south of JR 岡崎 that
  MLIT's 24.0a edition does not know: 針崎西 17, 岡崎駅前 11, 若松西 4, 柱西 1,
  and 3 rows addressed by a 土地区画整理事業 block (MHLW's own points there lie
  0.7 to 1.5 km from 岡崎); 3 riverbank or `地内` rows; a few rural 小字. Open
  call 2.
- **Still at the chōme tier (219)**: **舞木町字金森 46** (one site, open call 1),
  宮石町字六ツ田 18, and rural 小字 of the old 額田町 (merged 2006: 桜形町, 鍛埜町,
  保久町, 夏山町 …) whose 地番 MLIT's block file does not key.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_23_GML.zip`, N03 code 23202
(**387.3 km²**, extent W 137.103, S 34.860, E 137.421, N 35.042; centroid
137.258 E, 34.951 N; 額田町 merged 2006). Read with `stub_test()`'s method and
an in-memory `CITIES` entry (scratch `rail.py`). N02-24 gives the same 17
records.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside (north to south) |
|---|---|---|---|
| 名古屋本線 (名古屋鉄道, 12) | Meitetsu Nagoya Line | **9 / 60** | 宇頭, 矢作橋, 岡崎公園前, 東岡崎, 男川, 美合, 藤川, 名電山中, 本宿 |
| 愛知環状鉄道線 (愛知環状鉄道, 12) | Aichi Loop Line | **6 / 23** | 北野桝塚, 大門, 北岡崎, 中岡崎, 六名, 岡崎 |
| 東海道線 (東海旅客鉄道, 11) | JR Tōkaidō Line | **2 / 89** | 西岡崎, 岡崎 |

- **17 station records, 16 N02_005g groups** (岡崎 is one group for JR and the
  Aichi Loop, spread 0 m). No name in two groups. **One close pair of
  separate groups**: 中岡崎 (Aichi Loop) and 岡崎公園前 (Meitetsu), **168 m**,
  different names: kept apart, as MLIT keeps them (Kobe's trap 1;
  Kanazawa's 北鉄金沢 / 金沢 at 135 m); their rings overlap. **Median
  nearest-station gap 1,741 m** (168 to 2,340): standard rings by the
  spacing rule.
- **Shinkansen**: no Shinkansen station inside the city line.
- **Cut at the line** (nearest stations beyond, named by N03 municipality at
  build): Meitetsu toward 新安城 (Anjō) and 名電長沢 / 名電赤坂 (Toyokawa); the
  Aichi Loop toward 三河上郷 (Toyota); JR toward 安城 / 三河安城 (Anjō) and 相見
  (Kōta).
- **The light-rail/rail test**: all three are heavy rail (N02 class 11, JR
  conventional; class 12, Meitetsu and the third-sector Aichi Loop Railway).
  No tram, light rail or subway.
- **The stub test passes.** No line is cut to one station and none is urban.
  JR's 2 of 89 is a main line crossing the city; both stations are inside.
- **Frequency** (call 86 needs any stretch at about 11 a day or fewer named;
  there is none):
  - **Meitetsu Nagoya Line**: 東岡崎 about 10 an hour; locals about 4 an
    hour west of it and about 2 east (READ by staging's probe from
    Meitetsu's own timetable site, `trainbus.meitetsu.co.jp`, weekday
    10:00-15:59; master-list row).
  - **Aichi Loop Line**: about 3 to 4 an hour each way (READ, the operator's
    station timetable PDFs: 中岡崎 by the probe, 北野桝塚 here, edition
    `timetable_UD260314`, from `https://www.aikanrailway.co.jp/timetable/`).
  - **JR Tōkaidō Line**: ASSERTED (locals through 西岡崎 and 岡崎, several an
    hour); read JR Central's timetable at build for the record.
- ⚠️ **Gate 3** at build: Meitetsu's 9 stations in the city, the Aichi Loop's
  6 (岡崎 to 北野桝塚), JR's 2. **OSM `name:en`** for 16 groups (one Overpass
  query at build; not queried here).

## Scope

**Okazaki City** (including 額田, merged 2006). Meitetsu runs on to Anjō and
Toyokawa, the Aichi Loop to Toyota, JR to Anjō and Kōta; cut at the line.

## Licences — CC BY 4.0 as stated; the read is pending

- **The food list, as stated on BODIK**: `license_id` `cc-by-40-intl`,
  "Creative Commons Attribution 4.0 International",
  `https://creativecommons.org/licenses/by/4.0/deed.ja`; the city's portal
  links its own terms at `https://odcs.bodik.jp/232025/tos/` (利用規約), the
  page Funabashi's and Fukuoka's reads turned on. **The full read is a
  separate `licence-read` agent's; staging records it.** No verdict is
  written here. The prescribed credit and any terms the city's page adds come
  from that read.
- **MHLW open data**: PDL 1.0 as recorded in `docs/data_sources/japan.md`.
  **It reaches the map** (the partial Food-shops layer, call 127b, and its
  points, call 127c), so its credit goes on the notice.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The list carries no individual's name column.** 法人名 is filled on 2,121
  rows, **every one with a company or cooperative marker** (company 2,108,
  cooperative or union 13); the other 1,901 leave it blank (sole traders,
  most likely; no operator's own name is published for them). 施設電話番号 on 2,957;
  法人番号 empty. Step 2 never reads the phone or 施設名称_カナ into an output;
  法人名 is read IN MEMORY for the name rule only (already in
  `OPERATOR_COLS`).
- **The name rule, version 2, measured in memory** (answers only, never a
  value): **0** rows whose trade name is the operator's own name, **0** bare
  personal names. MHLW: 法人名 on 448 rows (29 with no company marker); its
  notifications flag **2** (1 a bare personal name), withheld by the rule at
  build.
- Select 施設名称, 営業の種類, 許可条件 (into 業態), 所在地_連結表記, 施設方書 (if
  the join wants it), 許可番号 and the two dates only.
- Run `check_personal_exposure.py okazaki` (`japan=True`) after step 2; it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Chubu after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city's centroid is 137.258 E (extent 137.10-137.42):
project to **UTM 53N (EPSG:32653)**, Toyota's and Nagoya's zone. OSM box from
the N03 extent, rounded out: (34.85, 137.10, 35.05, 137.43). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at build
from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band B, food
only, Hiroshima's shape (call 49); the downloads (call 67); no outreach for
the beauty list; the food share stated (call 125: 80.5%); MHLW's
notifications in as partial food shops (127b), its extra permits out (127a),
its points where the join misses (127c); tiers disclosed if the block share
stays low (145); `mode: metro`; the minor tier and Japan East; the three lines
drawn as cut (standing call, no stub); 中岡崎 and 岡崎公園前 kept apart (Kobe's
trap 1); the vehicles out as not premises (Kobe's trap 6, Hiroshima's hook).

**Open, each with a recommendation:**

1. **舞木町字金森: 47 permits at one site** (41 restaurants; two address
   strings; 45 with a unit in 方書; two trade names carry a service-area
   word; MHLW's 15 points there lie within about 80 m of each other). Whether
   it is an expressway service area is for the build to read; both MHLW's
   cluster (785 m) and the 舞木町 centroid the join gives (735 m) lie the same
   distance band from 名電山中. *Recommend keeping them*, at MHLW's point
   for the twins (127c) and the chōme centroid for the rest, as every built
   city keeps premises inside a site (station buildings, malls). Tradeoff:
   名電山中's ring would show about 45 food permits that few riders can walk
   to; dropping them would be the first site-based exclusion in Japan, with
   no precedent.
2. **The new towns south of JR 岡崎** (針崎西, 岡崎駅前, 若松西, 柱西 and 土地区画整理
   blocks; 36 rows, 1.0% of the bucketed premises) are absent from MLIT's
   24.0a edition. *Recommend leaving them unplaced* (MHLW's point for any
   twin, 127c), disclosed with the tiers. Tradeoff: about 30 premises near
   the city's busiest interchange stay off the map until MLIT's next edition;
   another address source (the Digital Agency's address base registry, say)
   would be a new source and a new licence, not in this brief, so it is not
   proposed.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control, `screen_japan_join.py
  minato` 98.0 / 0.2 / 1.8, and every city screen): **O1**, the 大字 + 小字
  丁目 rule. City-local in `source_rows`: 許可条件 into 業態 (Hiroshima's
  hook) and **O2** (U+B743 as ばら in 戸崎町字…山).
- `as_of` pinned to **2026-08-31** (the newest grant; the resource modified
  2026-09-11), never today.
- The share sentence for the page (about four restaurant permits in five),
  drafted on Ichinomiya's proposal (its open item 3) and flagged at review
  time; the Food-shops layer called partial.
- The Economic Census control (estimated 2.10, above the built range); the
  factory share; gate 3 (Meitetsu, Aichi Loop, JR); JR Central's frequency
  read; OSM `name:en`; line colours on both basemaps; the opening view
  (`map-view`); `check_provenance.py`; `check_scope_disclosure.py`.
- The licence read's credit wording, from staging's record.

```brief-checks
[
  {
    "id": "okazaki-bodik-package",
    "claim": "The one BODIK request (20 s spacing): the city's food dataset still declares cc-by-40-intl and still serves resource a893c7d6 (232025_food_business_al.csv, 1,097,449 B on 2026-10-06); ASCII anchors only, as CKAN escapes Japanese",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=232025_food_business_all",
    "present": ["cc-by-40-intl", "a893c7d6-5c10-4fb4-b9fa-cb48edd81565", "232025_food_business_al.csv"]
  },
  {
    "id": "okazaki-mhlw-live",
    "claim": "MHLW's open-data file for Okazaki (23202), the control and the partial food-shops layer, answers a plain keyless GET (281,861 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=23202_food_business_all.csv",
    "min_bytes": 200000
  },
  {
    "id": "okazaki-isj-block-live",
    "claim": "MLIT's block-level address file for Okazaki (23202) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/23202-24.0a.zip",
    "min_bytes": 400000
  },
  {
    "id": "okazaki-isj-chome-live",
    "claim": "MLIT's town-chōme file for Okazaki (23202) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/23202-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "okazaki-aikan-timetable",
    "claim": "The Aichi Loop Railway's 北野桝塚 station page links its station timetable PDF and the network timetable edition read (UD260314) - the frequency source; ASCII anchors only",
    "kind": "http_contains",
    "url": "https://www.aikanrailway.co.jp/timetable/kitanomasuzuka.html",
    "present": ["06kitanomasuduka_timetable.pdf", "timetable_UD260314.pdf"]
  },
  {
    "id": "okazaki-projected-crs",
    "claim": "Okazaki projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 137.26,
    "expect": "EPSG:32653"
  }
]
```
