# Tokorozawa — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5: `docs/decisions_drafts/staging.md`, "Wave 5, second half: calls 95 to 141";
the band row in `docs/city_master_list.md`, calls 101 and 143). The Step 0
downloads were approved by the owner 2026-10-06 (calls 106 and 147). **Step 0
measured 2026-10-06** (staging). Each file from its publisher's own host with
the project user-agent, each HTTP 200:

- **Shared by the four Saitama briefs, in `data/saitama_pref/raw/`**
  (gitignored; never under a city's folder):
  - From `services9.arcgis.com` (the prefecture's ArcGIS organisation
    `n65w8AXGaYPTqFYI`), fetched prefecture-wide by the Ageo/Sōka brief agent
    and reused here: `food_shinpo_layer_20261006.geojson` (28,581,348 B,
    52,706 features, layer 食品営業施設_新法_公開) and
    `food_kyuho_layer_20261006.geojson` (1,418,680 B, 2,627 features,
    食品営業施設_旧法_公開), paged queries, `outSR=4326`, every field but
    電話番号.
  - From `pref-saitama.maps.arcgis.com` (this brief, the approved R8.3.31
    content items): `kyuho_R080331.xls` (2,542,080 B, item
    `7da15c2811db4a55953345b16299d462`) and `shinpo_R080331.xls`
    (11,311,616 B, item `35e39b495baf4832a4e271ae9c6df0b9`), each
    `/sharing/rest/content/items/<id>/data`. They answered the question the
    layers could not (below).
  - From `www.pref.saitama.lg.jp` (fetched by the sibling, reused):
    `r7nenndo.zip` (1,203,694 B) and the twelve monthly files
    `0709.xlsx` … `reiwa0803.xlsx`, `r0804.xlsx` … `r808.xlsx` (15,595 to
    22,838 B each), page 232288.
- **Into `data/tokorozawa/raw/`**: `11000_food_business_all.csv`
  (5,456,396 B, MHLW, a control only; copied from the sibling's download of
  `i2fas.mhlw.go.jp`, one prefecture file); from `nlftp.mlit.go.jp`
  `isj/11208-24.0a.zip` (224,733 B) and `isj/11208-19.0b.zip` (7,238 B).
- Timetables read (counts only, nothing saved but the scratch counts):
  `timetables.jreast.co.jp` (東所沢's two weekday pages), plus the wave-5
  probe's saved Seibu pages (`seibu.ekitan.com`, the operator's own timetable
  service).

Nothing else was downloaded.

**Run `python scripts/brief_check.py tokorozawa` before writing any code.**
Then the `japan-city` skill. Shape: Akita's (`docs/build_briefs/akita.md`) for
the buckets and checks, but **the publisher is the prefecture, not the city**,
so every row is assigned to Tokorozawa by its address, Matsudo's method
(`docs/build_briefs/matsudo.md`). Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Tokorozawa entry; its table is shared
code and was not edited). Rail: MLIT N02-25 cut at the N03 city line,
measured through `pipeline/countries/japan.py` with an in-memory `CITIES`
entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left
out, its station kept through the other lines, and drawn cut only where no
other line serves that station (owner, 2026-10-06, calls 54 and 92); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor
for JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at
about 11 trains a day or fewer named and drawn (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The rail calls in the band row (owner, 2026-10-06):** the Seibu Yamaguchi
Line (Leo Liner, an AGT) has 2 stations inside the city and is **drawn, cut at
the line**; the JR Musashino Line's one station (東所沢) is a JR one-station
stub, **kept as cut**.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Tokorozawa carries `label_tier: "minor"` and goes in the **Japan East** view
(`app/cities.py`); wave 4's first city to land retags Japan into the eight
regions, Tokorozawa into **Kanto**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.
Tokorozawa sits beside Higashiyamato and Higashimurayama (Tokyo's Tama
briefs): measure the labels together if they land in one batch.

**✅ `mode`: `metro`**, the mode following the backbone (Matsudo's and
Kurume's precedent; Sakura's call 121, "metro is safe"): Seibu's railways hold
9 of the 10 station groups (N02 class 12), the Leo Liner AGT 2 of them, JR 1;
no subway or tram.

---

## The one-line summary

**Two buckets, three kinds, from Saitama Prefecture's own files (PDL 1.0 by
the GIS catalogue; the 生活衛生 files on the 2024 PDL record, relied on, call
143).** The live new-law layer holds **1,752 restaurant permits** in
Tokorozawa; **the live old-law layer is a partial load** (61 restaurants,
where the prefecture's own R8.3.31 old-law list holds 350 still in term on
2026-10-06), so the measured source is the live new-law layer **plus the
R8.3.31 old-law list**: **2,077 restaurant permits, 2.60 per 2021 census
establishment, exactly the jurisdiction's e-Stat ratio (2.60)**, about 100% of
the census-scaled estimate (open call 1). Through `japan_eigyo`, with the
layer's "NN:" type code stripped (a shared-code change): **Food service
2,082, Retail 1,182** (856 of them notifications: konbini, supermarkets,
other food sales). Barbers **179**, beauty salons **539**, laundries **98**
(the 2026-03-31 list plus new premises to 2026-08-31): 100%, 115% and 91% of
census-scaled estimates. Block join **99.3%** (food), 99.0-99.4% (registers).
**Rail: 10 station groups** (Seibu Ikebukuro 4, Shinjuku 3, Sayama 3, the Leo
Liner 2, JR Musashino 1), nothing near the 11-a-day line (the thinnest, the
Leo Liner, 42 a weekday each way).

---

## Business leg — food: the prefecture's 食品営業施設 layers and lists

The prefecture's food page (`https://www.pref.saitama.lg.jp/a0708/syokuhini-ichiran/ichiran-top.html`,
page 122166, 掲載日 2026-06-16): 「埼玉県管轄の食品営業施設の一覧を公開しています。（さいたま市、川越市、川口市、越谷市管轄の施設は含まれていません。）」;
the full list as of 2026-03-31 is in the GIS open-data catalogue, and new
permits and notifications since 2025-04-01 are on the GIS; 「※事業者の要望により、一部の施設情報は掲載されないことがあります。」
(some premises are withheld at the operator's request). Tokorozawa is in the
prefecture's jurisdiction (狭山保健所; permit numbers 指令狭保…).

| Source | Rows, prefecture | Rows, 所沢市 | What it is |
|---|---|---|---|
| Layer 食品営業施設_新法_公開 (FeatureServer/0, a view; last edit 2026-10-06; max 16,000 a page) | **52,706** | **3,460** | every new-law permit and notification since 2021-06-01, live; own points |
| Layer 食品営業施設_旧法_公開 (last edit 2026-10-06; max 2,000 a page) | **2,627** | **77** | old-law permits: **partial** (below) |
| `shinpo_R080331.xls` (one sheet, 新法) | 53,220 | 3,269 | the new-law list as of 2026-03-31, no coordinates |
| `kyuho_R080331.xls` (one sheet, 旧法) | **10,526** | **698** | the old-law list as of 2026-03-31, no coordinates |

- **Layer fields**: OBJECTID, **施設_名称**, **施設所在地**, 所在地建物名付 (the
  address with its building), 電話番号, **業種名**, **申請者_氏名**,
  **有効開始年月日**, **有効終了年月日**, **許可番号**; point geometry. The XLS
  items: 管轄保健所, 業種, 施設_名称, 施設_所在地, 施設_電話番号, 申請者_氏名,
  開始年月日, 終了年月日, 許可番号.
- **Against the shared tuples**: 施設所在地 and 施設_所在地 are in `ADDR_COLS`,
  施設_名称 in `NAME_COLS`, 業種名 and 業種 in `TYPE_COLS`, 申請者_氏名 in
  `OPERATOR_COLS`. No 業態 column. Dates are the padded era form
  (`R 8. 3.31`), read by `wareki_date` (Sasebo's rule). **`city_rows` cannot
  read the GeoJSON**: the build writes a `source_rows` that reads its
  properties (premises columns, plus 申請者_氏名 in memory for the name rule)
  and the point as `緯度` / `経度`. The XLS items read through `city_rows`
  (xlrd) as they stand.
- **Every address starts with the municipality** (`所沢市…`, no prefecture):
  the city filter is an address prefix. **9 of 3,460** new-layer rows with a
  Tokorozawa address have their point outside the city line; no point inside
  the line carries another municipality's address.
- **業種名 carries a code**: `01:飲食店営業 ` (with a trailing space),
  `11:菓子製造業`, `42:コンビニエンスストア`. `japan_eigyo.normalise` strips
  leading digits but leaves the colon, so every anchored Retail rule misses:
  **today's shared code buckets 575 Retail rows where the stripped type gives
  1,142** (live layer). The build strips `^\d+:` (a shared-code change to
  `normalise`, followed by the Minato control and every city screen) or in a
  `source_rows`. The XLS types carry no code.

### ⚠️ The live old-law layer is a partial load (the completeness question, answered)

The band row read the layer's shortfall (1.8-2.3 restaurants per census
establishment against 2.5-3.1 in the core cities) as operators withheld on
request. **The R8.3.31 lists show most of it is the old-law layer instead:**

| Old-law restaurants (飲食店営業) in term on 2026-10-06 | Jurisdiction | 所沢市 |
|---|---|---|
| In the R8.3.31 old-law list | **3,894** | **350** |
| … also in the live old-law layer | 1,117 | **51** |
| … not there, but in the new-law layer by (address, name) (renewed) | 338 | 39 |
| … not there; the address or the name alone in the new layer | 687 | 82 |
| … nowhere in either layer | **1,752** | **178** |

- **The new-law layer is complete against its list**: of the R8.3.31 new-law
  list's 25,914 restaurants still in term, all but 305 (1.2%, closures since
  March) are in the live layer, which adds the permits since (Tokorozawa: 2
  of 1,583 missing; 86 granted after 2026-03-31).
- **The old-law layer is not**: it holds 2,627 rows against the list's 10,526
  (6,269 restaurants in term on 2026-03-31), keeps 441 restaurant permits that
  had already ended (from 2025-03-31), and lacks permits running to 2027 and
  2028. The nowhere rows' end dates run 2026-10 to 2027-09 (Tokorozawa: 11 to
  30 a month), not a closure pattern.
- **The withheld share is small.** MHLW's file (a control) holds **114 open,
  addressed restaurant permits** in Tokorozawa (2021-09-28 to 2026-08-17): **110
  (96.5%)** are in the live layers by permit number, name or address, **106
  (93.0%)** by permit number or (address and name). Jurisdiction-wide: 95.8%
  and 87.2% of 1,717. So withheld or closed-but-open permits are about 4 to
  13% of MHLW's recent slice, an upper bound on the withholding.
- **e-Stat 衛生行政報告例** (`japan_official.estat()`), the jurisdiction (埼玉県
  less さいたま市, 川越市, 越谷市, 川口市), restaurants in force: FY2021 34,960,
  FY2022 34,144, FY2023 36,318, **FY2024 (2025-03-31) 33,897** (old law 10,946,
  revised 22,951). The live layers in term: **26,057 (76.9%)**; with the
  R8.3.31 old-law list: **28,457 (84.0%)**, eighteen months later.
- **Per establishment** (2021 Economic Census, 飲食店): the jurisdiction's
  e-Stat count is **2.60** per establishment (33,897 / 13,019); the core
  cities' 2.46-3.08. The live layers give 1.68-2.35 across the 25
  municipalities with 200+ establishments; with the old-law list, **1.87-2.60**
  (median 2.10), **Tokorozawa the highest at 2.60** (1,810 in term on the
  live layers, 2,077 with the old-law list, on 798 establishments).

**So the build reads three food files** (open call 1): the live new-law layer;
the R8.3.31 old-law list; the live old-law layer (in Tokorozawa it adds no row
the list lacks, since its 77 rows are all in the list, but it carries the
prefecture's later edits elsewhere). Each in term on the pinned as-of (an
old-law permit's 終了年月日 on or after it), one row per (address, trade
name, type), one per permit number and type, and **an old-law row dropped
where the new-law layer holds the same (address, name) and type** (a
renewal; 喫茶店営業 counts as 飲食店営業 there). Tokorozawa: old-law **501 in
term, 21 renewed, 480 kept** (325 restaurants, 5 cafés). The old-law rows are
**an upper bound**: closures since 2026-03-31 are not visible for them (the
live old-law layer would show them, if it were complete), Kyoto's
disclosure.

### Types, notifications, dates

- **Live new-law layer, Tokorozawa (3,460)**: 飲食店営業 1,752, その他の食料・飲料販売業
  364, コップ式自動販売機 170, 菓子製造業 161, コンビニエンスストア 136, 乳類販売業
  135, 集団給食施設 116, 自動販売機による販売業 98, 百貨店、総合スーパー 75,
  野菜果物販売業 51, 食肉販売業 46, … 45 types.
- **Notifications are in the layer**: **1,370 rows with no start or end date**,
  every one a notification type (その他の食料・飲料販売業 364, コップ式自販機 170,
  コンビニ 136, 乳類販売 135, 集団給食 116, …). Retail takes them by Tokyo's
  rule (food retail notifications count where a list publishes them); here
  the prefecture publishes them all, so the bucket is not partial.
- **Permits (2,090)**: start 2021-06-01 to **2026-12-01**, end 2026-03-31 to
  2033-02-28; **1 ended before 2026-10-06** (none of the restaurants).
  **19 rows start after 2026-10-06** (2026-11-01 and 2026-12-01; 16
  restaurants), none with a current twin at the same (address, name, type):
  premises permitted ahead of opening (open call 2).
- **Old-law list, Tokorozawa (698)**: 飲食店営業 486 (350 in term on
  2026-10-06), 給食施設 67, 菓子製造業 52, その他の製造業 20, 魚介類販売業 18; start
  2019-02-13 to 2021-09-01 (prefecture), end 2026-03-31 to 2028-08-31; 1,776
  rows prefecture-wide carry no dates (notifications, 給食施設 among them).
- **No 業態, no vehicle or hostess marker**: kitchen cars and snack bars cannot
  be told apart (2 trade names read as a vehicle), and stay in Food service,
  as `docs/category_rules.md` R3 allows ("wherever the register names them").
  Restaurant permits held by school or hospital kitchens are likewise
  invisible (集団給食施設 notifications are excluded by type).

### Duplicates and closed premises

- **39 groups repeat an (address, trade name, type)** in the live layers, all
  new-law pairs (14 restaurants, 7 konbini, 4 cup vending): two permits at
  one premises. Permit numbers repeat across types (a number per premises,
  not per permit). One pin per premises and bucket (trap 7).
- **2,011 distinct points for 3,537 layer rows** (up to 56 rows on one point,
  a station building or mall).
- **Closures**: the live layers drop closed premises (1.2% of the March
  new-law restaurants gone by October); the old-law list's rows cannot be
  checked (above). The page keeps "may include closed premises".

### Counts through `japan_eigyo` (the proposed set, type code stripped)

**Food service 2,082** (new law 1,752, old law 330), **Retail 1,182** (from
notifications 856: other food and drink sales 364, konbini 136, dairy 135,
supermarket 75, greengrocer 51, butcher 43, fishmonger 25, rice 15; from
permits: 菓子 194, butcher 99, fishmonger 70, deli 31, bento 12): **3,264
storefront rows, 3,027 pins** (Food service 2,066, Retail 961). Left out:
vending 280, institutional catering 182, mail order 9, and 204 with no rule
(製茶業 32, コーヒー製造・加工業 26, その他の食料品製造・加工業 24, その他の製造業 20, 麺類
製造業 12, 漬物製造業 12, その他 12, …), as in every built city. Not a premises
by address: 0. The "other food and drink sales" catch-all is **31% of
Retail** (364 of 1,182); it stays Retail by the standing rule.

**Economic Census control**: 2,065 distinct placed Food-service premises on
798 establishments, **2.59**, ⚠️ above the built cities' 1.56-1.92 and
Akita's 2.11. Readings for the build to test: permits kept to their term after
a closure (old-law ones especially), and the prefecture counting two permits
where one premises changed hands. Record the figure and the reading.

### MHLW's file (11000), a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11000_food_business_all.csv`:
**5,456,396 B, 15,335 rows**, the prefecture's jurisdiction; **751 with a
Tokorozawa address** (届出 598, 許可 150, 届出(廃業) 2, 許可(廃業) 1). 150 open
permits, **114 restaurants, all with a point**. Matched above (96.5% / 93.0%).
Its notifications duplicate the layer's, which holds all of them; **no MHLW
use beyond the control is proposed**.

## Business leg — personal services: 生活衛生営業施設一覧, page 232288

Page `https://www.pref.saitama.lg.jp/a0706/6hou/ichiran.html` (掲載日
2026-09-14): 「埼玉県管轄の生活衛生営業施設の一覧を公開しています。（さいたま市、川越市、越谷市、川口市管轄の施設は含まれていません。）」;
「令和8年3月31日時点で許可・確認を受けている生活衛生営業施設の全業種一覧です。」 (ZIP,
1,176 KB, one workbook per health centre); monthly 新規営業施設一覧 from
2025-09 to 2026-08; 「※事業者の要望により、一部の施設情報は掲載されないことがあります。」
No closure files.

- **Tokorozawa is in `08狭山保健所管内.xlsx`** (所沢市, 入間市, 狭山市, 飯能市, 日高市),
  sheets 理容所 (419 rows), 美容所 (1,132), クリーニング (219), 旅館, 公衆浴場, 興行場
  (the last three out of scope). Header on row 1. Columns: **業種**, (laundry)
  **営業の種類**, **施設名称**, **施設所在地**, 施設電話番号, **申請者名**, 確認年月日;
  the monthly files add 確認番号 and sheet names 理容 / 美容 / クリーニング (2025)
  or 理容所 / 美容所 / クリーニング (2026). All in the shared tuples (施設所在地,
  施設名称, 営業の種類 before 業種 in `TYPE_COLS`, 申請者名); `city_rows` reads the
  zip member by `r7nenndo.zip::08狭山`.
- **The months**: 2025-09 to 2026-03 hold 10 Tokorozawa rows (beauty 9,
  laundry 1), **every one already in the year-end list** (it is consistent
  with its months); 2026-04 to 2026-08 add **barbers 2, beauty 14, laundry 0**.
  Ichinomiya's precedent (call 126): the list whole plus the months, an upper
  bound (no closures published), `as_of` 2026-08-31.

| Kind | List 2026-03-31 | + months to 2026-08 | Census 2021 | Scaled estimate | Share |
|---|---|---|---|---|---|
| 理容所 | **177** | **179** | 163 | 179 | **100%** |
| 美容所 | **525** | **539** (538 premises) | 311 | 467 | **115%** |
| クリーニング所 | **98** | 98 | 90 (洗濯業) | 108 | **91%** |

(Scaled by the jurisdiction's licensed-to-census ratio, Matsudo's method:
barbers 3,184 / 2,898 = 1.099, beauty 7,554 / 5,036 = 1.500, laundries
1,725 / 1,438 = 1.200; e-Stat FY2024 第10表 and 第11表,
`data/hakodate/raw/estat_eisei_r6_*_by_city.csv`, 埼玉県 less the four cities.
A modelled figure, recorded as a measurement.)

- **Jurisdiction-wide, the lists are complete**: barbers 3,127 of 3,184
  (98.2%), beauty 7,585 of 7,554 (100.4%), laundries 1,637 of 1,725 (94.9%),
  the lists a year after e-Stat's date. The withholding note is thin, as
  Chiba's consent filter was (Matsudo).
- **Laundry kinds in Tokorozawa**: 58 blank, 24 洗濯物の受取、処理及び引渡し, 16
  受取及び引渡しのみ (取次所, counter premises, counted); **no リネンサプライ**
  (the rule drops it where named; the blank 58 cannot be read for it).
- **Repeats**: beauty 1 (address, name). Every address is in 所沢市 by prefix.
- **確認年月日** is `H12/03/04` with slashes and Shōwa dates (`S64/…`, 51
  barber rows): `wareki_date` reads neither. Nothing in the build reads it
  (no expiry on a 生活衛生 confirmation); say so if a step ever does.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11208-24.0a.zip` (224,733 B,
**28,580 block keys**), town-chōme `.../19.0b/11208-19.0b.zip` (7,238 B,
**160**). `japan.CITIES` entry at build: `"tokorozawa": {"name": "所沢市",
"pref": "11", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["11208"]}`.

| Tier, today's shared code | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| Food, the proposed set (3,264) | **99.3%** | 0.6% | **0.1%** (2) |
| … Food service (2,082) / Retail (1,182) | 99.4 / 99.1 | 0.5 / 0.8 | 0.0 / 0.1 |
| … old-law list rows, no own point (386) | 99.7 | 0.3 | 0.0 |
| Barbers (179) | **99.4%** | 0.6% | 0.0% |
| Beauty salons (539) | **99.4%** | 0.6% | 0.0% |
| Laundries (98) | **99.0%** | 1.0% | 0.0% |

- **The layer's own points** agree with the block point: median **44 m**, 84.0%
  within 100 m, 96.8% within 250 m, 2 over 1 km (2,933 rows); against the
  chōme centroid, median 239 m (21). **The 2 unplaced rows** (an address
  written `西所沢1-7-16` then `1丁目`, a typo) carry their own layer point
  inside the city: MHLW's-own-point precedent (call 127c) applies to the
  publisher's point.
- **Chōme tier**: 大字 addresses whose 地番 MLIT lacks (山口 5, 東所沢5丁目 3,
  東狭山ケ丘3丁目 2, 中富 2, 有楽町 2, …).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_11_GML.zip`, N03 code 11208
(**72.1 km²**, extent W 139.379, S 35.763, E 139.546, N 35.844). Read with
`stub_test()`'s method and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 池袋線 (西武鉄道, 12) | Seibu Ikebukuro Line | **4 / 31** | 所沢, 西所沢, 小手指, 狭山ヶ丘 |
| 新宿線 (西武鉄道, 12) | Seibu Shinjuku Line | **3 / 29** | 所沢, 航空公園, 新所沢 |
| 狭山線 (西武鉄道, 12) | Seibu Sayama Line | **3 / 3** | 西所沢, 下山口, 西武球場前 |
| 山口線 (西武鉄道, 16 AGT) | Seibu Yamaguchi Line (Leo Liner) | **2 / 3** | 西武球場前, 西武園ゆうえんち |
| 武蔵野線 (東日本旅客鉄道, 11) | JR Musashino Line | **1 / 27** | 東所沢 |

- **13 station records, 10 N02_005g groups** (所沢 Ikebukuro + Shinjuku, 21 m;
  西所沢 Ikebukuro + Sayama, 0 m; 西武球場前 Sayama + Yamaguchi, 90 m). No name
  in two groups; no pair closer than 600 m. **Median nearest-station gap 1,465
  m** (1,125 to 3,830): rings by the spacing rule at build.
- **Shinkansen**: none.
- **Cut at the line**: the Ikebukuro Line 27 beyond (Tokyo 16, 飯能市 4, 入間市 4,
  日高市 2, 狭山市 1), the Shinjuku Line 26 (Tokyo 21, 狭山市 3, 川越市 2), the
  Musashino Line 26 (other prefectures 12, さいたま市 5, …), the Yamaguchi Line 1
  (多摩湖, in 東大和市, Tokyo). The Sayama Line lies wholly inside.
- **The Leo Liner** (owner, band row): 2 of 3 stations inside, so not a
  one-station stub; drawn and cut at the city line, 西武園ゆうえんち 43 m from
  it. 西武球場前 keeps its ring through the Sayama Line as well.
- **The Musashino Line's 東所沢** (691 m from the line): a JR one-station
  stub, kept as cut (standing call 3). ⚠️ At build: its permanent label and
  legend entry on a short stretch (measure placement in a scratch render;
  Akita's Oga Line note).
- **The light-rail/rail test**: Seibu's three railways and JR are heavy rail
  (classes 11 and 12); the Yamaguchi Line is an AGT (class 16, rubber-tyred,
  its own guideway), drawn as rail, not tram or light rail.
- **Frequency**, weekday departures counted whole (read 2026-10-06; Seibu from
  the probe's saved pages of `seibu.ekitan.com`, the 2025-03-15 timetable,
  recounted as distinct departures; JR East from `timetables.jreast.co.jp`
  `2610/timetable/tt1291/`, every minute span counted, marked trains
  included):

  | Station (line, direction) | Weekday departures | Per hour, 10-16 |
  |---|---|---|
  | 所沢 (Ikebukuro, to 飯能・小手指・西武秩父) | 219 | 11 |
  | 所沢 (Shinjuku, to 本川越・新所沢) | 154 | 7-8 |
  | 下山口 (Sayama, to 西所沢) | 68 | 3 |
  | **西武園ゆうえんち (Yamaguchi, to 多摩湖)** | **42** | 3 (every 20 min) |
  | 東所沢 (JR Musashino, to 武蔵浦和・西船橋 / to 府中本町) | 134 / 127 | 6 |

  **No stretch is at or under about 11 trains a day** (call 86): the
  thinnest is the Leo Liner, 42 a weekday each way. Only counts are recorded,
  never a timetable on the page.
- ⚠️ **Gate 3** at build: Seibu's and JR East's station counts inside the
  city (Ikebukuro 4, Shinjuku 3, Sayama 3, Yamaguchi 2, Musashino 1). **OSM
  `name:en`** for 10 groups (one Overpass query at build, in the box below;
  not queried here).

## Scope

**Tokorozawa City.** The Seibu lines run on to Tokyo (池袋, 西武新宿) and to
飯能 and 本川越, the Musashino Line to 府中本町 and 西船橋, the Leo Liner to 多摩湖:
cut at the line.

## Licences — as read by staging (2026-10-06)

- **The food layers and the R8.3.31 lists: PERMITTED WITH CONDITIONS**
  (licence-read agent, 2026-10-06; the band row, `docs/decisions_drafts/staging.md`,
  "Wave 5, second half"). The GIS open-data catalogue page (item
  `d252024b403d49519b2166f4604a1bed`) lists the two live layers and the two
  R8.3.31 items, and says 「埼玉県GIS（地理情報システム）の「オープンデータカタログ」サイトに掲載されているデータの利用については、埼玉県オープンデータ利用規約を準用するものとします。」
  (the portal's PDL 1.0 terms). The portal also catalogues the new-law
  layer's export as dataset 2679, 公共データ利用規約第1.0版（PDL1.0）.
- **The 生活衛生 files**: a 2024 PDL record for the page against the site's
  copyright page; **the record relied on** (owner, call 143).
- **Credit**: the portal's processed-use credit, as staging recorded it
  (take the wording from staging's record; none is written here).
- **MHLW open data** (a control): PDL 1.0 as recorded in
  `docs/data_sources/japan.md`. **MLIT 位置参照情報 and N02**: PDL 1.0, the
  shared credits. **N03**: CC BY 4.0, picks stations, ⛔ never drawn.
  **e-Stat**: a measurement source, not drawn. **Timetables**: read for counts
  only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **Every food file carries 申請者_氏名** (the operator) and a phone column
  (電話番号 in the layers, 施設_電話番号 in the XLS items). In the proposed set,
  **2,755 rows carry a company or co-op marker and 1,184 none** (167 of those
  from the old-law list), the shape of a sole trader's own name. Step 2 reads
  申請者_氏名 IN MEMORY for the name rule only (`OPERATOR_COLS` holds it) and
  never writes it; the phones are never selected. ⚠️ **The shared
  `food_*_layer_20261006.geojson` files hold 申請者_氏名** (the sibling's fetch
  selected it; not the phone): raw and gitignored, as every Japanese list's
  raw file is; the build's `fetch_sources.py` selects the premises fields
  plus 申請者_氏名 and never 電話番号.
- **The name rule, measured in memory** (answers only, never a value): **4
  food rows** whose trade name is the operator's own name or a bare personal
  name (2 bare), **0 among fixed premises in a bucket**. Registers: barbers
  **2** (both bare personal names, both the operator's own), beauty 0,
  laundry 0. Operators without a company marker: barbers 153 of 177, beauty
  347 of 525, laundry 30 of 98.
- **施設電話番号** in the registers is never selected; select 施設名称,
  施設所在地, 業種 and 営業の種類 only (申請者名 in memory for the name rule).
- **所在地建物名付** is an address with its building; the build does not need it.
- Run `check_personal_exposure.py tokorozawa` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.379-139.546 E, centroid 139.458,
35.799: project to **UTM 54N (EPSG:32654)** (computed here, never copied).
OSM box from the N03 extent, rounded out: (35.76, 139.37, 35.85, 139.55).
**Scaffold**: `scaffold_city.py --slug tokorozawa --name Tokorozawa
--system-name "Seibu Railway and JR East" --taxonomy japan_eigyo --lat 35.799
--lon 139.458 --region "Japan East" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), the page number claimed at build from
`docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band A on the
prefecture's food layers and personal-services lists; the Leo Liner drawn cut;
the Musashino Line's stub kept as cut; `mode: metro`; the minor tier and Japan
East (Kanto after the retag); no frequency floor; the licence positions (the
GIS catalogue's PDL terms; the 生活衛生 record relied on, call 143); the
registers' months merged (call 126); notifications in Retail (Tokyo's rule);
the publisher's own point where the block join misses (call 127c).

**Open, with a recommendation:**

1. **Add the R8.3.31 old-law list to the food source.** The live old-law layer
   holds 51 of the 350 old-law restaurant permits the prefecture's own list
   shows still in term in Tokorozawa (1,117 of 3,894 jurisdiction-wide).
   *Recommend the three files* (live new-law layer, R8.3.31 old-law list, live
   old-law layer), in term on the as-of, deduplicated, renewals dropped:
   **2,077 restaurants against 1,752**, 2.60 per census establishment, the
   jurisdiction's own e-Stat ratio. The tradeoff: a dated component (the
   old-law rows are an upper bound as of 2026-03-31, closures since unseen,
   disclosed as Kyoto's are, and they expire by 2028) and a second file to
   refresh each year, against a page about 15% short of restaurants with
   the reason misread as withholding. Both lists are from the same publisher
   under the same catalogue terms, and were approved for download (call 147).
2. **Rows that start after the as-of** (19 in Tokorozawa, 16 restaurants;
   permits granted for premises not yet open). *Recommend dropping them*,
   `in_term`'s mirror (a row whose 有効開始年月日 is after the pinned as-of is
   not yet in term); they come in at the next refresh. The tradeoff is
   trivial either way.
3. **A stated food share on the page** (call 125's shape)? *Recommend none*:
   Tokorozawa's census-scaled estimate is about 100%, and the per-city figure
   is a model (the jurisdiction's municipalities run 1.87-2.60). Disclose the
   publisher's withholding note as the coverage reason, with no number
   (Matsudo's precedent), and the old-law rows' upper bound. The tradeoff:
   Kasukabe's estimate is about 81% (its brief), so a reader comparing the
   two pages gets no figure for the gap.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `japan_eigyo.normalise` strips a leading `NN:` code (or a
  city-local type cleanup in `source_rows`). No `ADDR_COLS` / `NAME_COLS` /
  `TYPE_COLS` change is needed.
- **`fetch_sources.py`**: a paged FeatureServer query per layer (the
  sibling's `fetch_pref.py` in the scratchpad is a model; `maxRecordCount`
  16,000 and 2,000; `outSR=4326`; never 電話番号), the two R8.3.31 items by id,
  `r7nenndo.zip` and the months by `SOURCE_LINKS` on page 232288 (each month's
  file is named by hand: `08020.xlsx`, `reiwa0803.xlsx`, `r808.xlsx`), MHLW
  11000 only if a control step reads it. One shared `data/saitama_pref/raw/`
  for the four Saitama cities (never re-pulled from a branch for a city on
  master, the shared-data rule).
- `as_of`: the layers' retrieval date (they are live), never today at render;
  the old-law list 2026-03-31; the registers 2026-08-31.
- The census ratio (2.59, above the built range) and its reading; the
  old-law rows' share of restaurants (325 of 2,077) on the page if open call 1
  is taken.
- 東所沢's label on its stub; gate 3; OSM `name:en`; line colours on both
  basemaps; the opening view (`map-view`); the factory share;
  `check_provenance.py`; `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "saitama-food-page",
    "claim": "The prefecture's food page points to the GIS open-data catalogue for the 2026-03-31 list and to the two live layers (ASCII anchors: the host sends no charset)",
    "kind": "http_contains",
    "url": "https://www.pref.saitama.lg.jp/a0708/syokuhini-ichiran/ichiran-top.html",
    "present": ["portal-pref-saitama.hub.arcgis.com/pages/opendatacatalog", "746f76d1a1844464999a87554d59b6bb", "a0b8fc89c3894763b1b1eb07a2fc95fb"]
  },
  {
    "id": "saitama-food-new-layer",
    "claim": "The live new-law food layer: points, 52,706 rows on 2026-10-06, the fields the build reads (and 申請者_氏名, read in memory only), edited within 30 days",
    "kind": "arcgis_layer",
    "url": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/%E9%A3%9F%E5%93%81%E5%96%B6%E6%A5%AD%E6%96%BD%E8%A8%AD_%E6%96%B0%E6%B3%95_%E5%85%AC%E9%96%8B/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 52706,
    "tolerance": 3000,
    "present": ["施設_名称", "施設所在地", "業種名", "申請者_氏名", "有効開始年月日", "有効終了年月日", "許可番号"],
    "max_age_days": 30
  },
  {
    "id": "saitama-food-old-layer",
    "claim": "The live old-law food layer: 2,627 rows on 2026-10-06, the partial load this brief measured against the R8.3.31 list (a jump toward 10,000 means the prefecture reloaded it: re-measure open call 1)",
    "kind": "arcgis_layer",
    "url": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/%E9%A3%9F%E5%93%81%E5%96%B6%E6%A5%AD%E6%96%BD%E8%A8%AD_%E6%97%A7%E6%B3%95_%E5%85%AC%E9%96%8B/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 2627,
    "tolerance": 500,
    "present": ["施設_名称", "施設所在地", "業種名", "有効終了年月日"],
    "max_age_days": 90
  },
  {
    "id": "saitama-gis-catalogue",
    "claim": "The GIS open-data catalogue page lists both R8.3.31 items and applies the prefecture's open-data terms (準用)",
    "kind": "http_contains",
    "url": "https://pref-saitama.maps.arcgis.com/sharing/rest/content/items/d252024b403d49519b2166f4604a1bed/data?f=json",
    "present": ["7da15c2811db4a55953345b16299d462", "35e39b495baf4832a4e271ae9c6df0b9", "準用", "オープンデータ利用規約"]
  },
  {
    "id": "saitama-kyuho-item",
    "claim": "The edition measured: the R8.3.31 old-law list, kyuho_R080331.xls, 2,542,080 B (a new size means a new edition: re-measure)",
    "kind": "http_contains",
    "url": "https://pref-saitama.maps.arcgis.com/sharing/rest/content/items/7da15c2811db4a55953345b16299d462?f=json",
    "present": ["kyuho_R080331.xls", "\"size\":2542080"]
  },
  {
    "id": "saitama-shinpo-item",
    "claim": "The edition measured: the R8.3.31 new-law list, shinpo_R080331.xls, 11,311,616 B",
    "kind": "http_contains",
    "url": "https://pref-saitama.maps.arcgis.com/sharing/rest/content/items/35e39b495baf4832a4e271ae9c6df0b9?f=json",
    "present": ["shinpo_R080331.xls", "\"size\":11311616"]
  },
  {
    "id": "saitama-kyuho-file",
    "claim": "The old-law list answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://pref-saitama.maps.arcgis.com/sharing/rest/content/items/7da15c2811db4a55953345b16299d462/data",
    "min_bytes": 2000000
  },
  {
    "id": "saitama-seikatsu-page",
    "claim": "Page 232288 offers the 2026-03-31 list (r7nenndo.zip) and the monthly new-premises files through 2026-08 (r808.xlsx); ASCII anchors, the host sends no charset",
    "kind": "http_contains",
    "url": "https://www.pref.saitama.lg.jp/a0706/6hou/ichiran.html",
    "present": ["/documents/232288/r7nenndo.zip", "/documents/232288/r0804.xlsx", "/documents/232288/r808.xlsx"]
  },
  {
    "id": "saitama-seikatsu-zip",
    "claim": "The 2026-03-31 生活衛生 list (1,203,694 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.pref.saitama.lg.jp/documents/232288/r7nenndo.zip",
    "min_bytes": 1000000
  },
  {
    "id": "saitama-seikatsu-r808",
    "claim": "The 2026-08 new-premises file answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.pref.saitama.lg.jp/documents/232288/r808.xlsx",
    "min_bytes": 10000
  },
  {
    "id": "tokorozawa-mhlw-live",
    "claim": "MHLW's open-data file for Saitama Prefecture's jurisdiction (11000) answers a plain keyless GET (a control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11000_food_business_all.csv",
    "min_bytes": 4000000
  },
  {
    "id": "tokorozawa-isj-block-live",
    "claim": "MLIT's block-level address file for Tokorozawa (11208) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11208-24.0a.zip",
    "min_bytes": 180000
  },
  {
    "id": "tokorozawa-isj-chome-live",
    "claim": "MLIT's town-chōme file for Tokorozawa (11208) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/11208-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "tokorozawa-jr-higashi-tokorozawa",
    "claim": "JR East's timetable index for 東所沢 (list1291) links the two weekday Musashino Line pages read (1291010, 1291020); ASCII ids only",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1291.html",
    "present": ["tt1291/1291010.html", "tt1291/1291020.html"]
  },
  {
    "id": "tokorozawa-seibu-leo-liner",
    "claim": "Seibu's timetable for 西武園ゆうえんち (Yamaguchi Line, toward 多摩湖), the thinnest stretch read: 42 weekday departures",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/239-1/d1?dw=0",
    "present": ["西武園ゆうえんち", "多摩湖"]
  },
  {
    "id": "tokorozawa-seibu-sayama",
    "claim": "Seibu's timetable for 下山口 (Sayama Line, toward 西所沢): 68 weekday departures",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/241-1/d1?dw=0",
    "present": ["下山口", "西所沢"]
  },
  {
    "id": "tokorozawa-projected-crs",
    "claim": "Tokorozawa projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.458,
    "expect": "EPSG:32654"
  }
]
```
