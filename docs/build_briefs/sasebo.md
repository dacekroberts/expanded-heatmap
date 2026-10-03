# Sasebo — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live; downloads are MHLW's file, the city's BODIK lists and MLIT's ISJ zips).
**Run `python scripts/brief_check.py sasebo` before writing any code.** Then
the `japan-city` skill: **Kitakyushu's food shape, MHLW's filings plus the
city's own list of pre-2021-law permits still in term, food only.**
Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from a scratch script
(`scripts/screen_japan_join.py` has no Sasebo entry; its table is shared
code).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none in the city); (2) **lines served only by limited expresses
DO count** (2026-09-28: the みどり / ハウステンボス run on JR here); (3) **the
city line only**: only stations inside the city get rings, JR and the private
lines are cut at the line, **a one-station stub stays as cut** (2026-09-27),
and an URBAN line cut to a stub goes back to the owner; (4) **菓子製造業 and
そうざい製造業 count, in Retail**, the factory share measured and kept; (5)
**the name rule** where an operator column exists (the city's old-law list;
MHLW's rows have none, Fukuoka's precedent); (6) **no page says "currently
operating"**. Fault-based cost clauses are accepted for all of Japan.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Sasebo
carries `label_tier: "minor"` and joins the Japan sub-region the 2026-10-01
batch creates.

**✅ `mode`: `metro`** (owner's rule, 2026-10-02). JR is not the largest
network inside the city (6 stations of its own and 佐世保 shared, against
Matsuura Railway's 21 and 佐世保), and no subway or tram is drawn, so the mode
follows the backbone: Matsuura Railway's 西九州線 is a railway (N02 class 12, a
third-sector diesel line), not a tram or light rail.

---

## The one-line summary

**Food only, from TWO lists split by permit law: MHLW's file (every permit
since 2021-06; 2,316 open restaurant permits, 92% of the 2,518 in force) and
the city's own BODIK list of pre-2021-law permits (607 rows at 2026-04-30;
346 restaurants and cafés still in term on 2026-08-31). Together about 2,640
restaurants, ~105% of the official count (an older year-end).** On fixed
premises 79.1% of MHLW's restaurants publish an address. Block join 88.6%
(MHLW) / 90.3% (old-law list), unplaced under 0.5%. **No personal-services
register.** 28 stations: Matsuura Railway 22 groups, JR 7 (佐世保 shared).
**Band B, food only.**

---

## Business leg

| | MHLW open data (42202) | City's old-law list (BODIK) |
|---|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=42202_food_business_all.csv` | `https://data.bodik.jp/dataset/571df2fc-f781-4a2c-b9d7-09e1637b15fe/resource/f7fa490e-026d-4330-8c34-10e7c367c13d/download/dataset_kaiseimaer8.4.csv` |
| Bytes | **1,533,046** (same as the scope's fetch) | **104,877** |
| Rows | **4,461** (許可 3,111 · 届出 1,343 · 許可(廃業) 4 · 届出(廃業) 3) | **607** (飲食店営業 446, 菓子 39, 魚介類販売 37, 食肉販売 29, 喫茶店営業 25, そうざい 14, other 17) |
| As of | permits to **2026-08-28**; closures 2026-08-01 .. 08-31 | **2026-04-30** (「(令和8年4月末時点)法改正前食品営業許可施設一覧」, uploaded 2026-06-01) |
| Cadence | monthly (MHLW) | yearly at the year end (the previous edition is 2025-04-30); the list only shrinks as old-law permits expire |
| Dataset | i2fas オープンデータ閲覧 | `422029_syokuhineigyoukyoka` 「［佐世保市］食品営業許可施設一覧」 (生活衛生課, `cc-by-40-intl`), which also holds monthly new-permit CSVs since 2020-06 |
| Encoding | UTF-8 CSV | UTF-8 (BOM) CSV, header on line 1 |

**Columns.**
- MHLW: the national schema (as Okayama's). No individual operator column, so
  **the name rule cannot run on MHLW rows** (Fukuoka's precedent).
- Old-law list: **施設_名称**, **業種**, 種目, **施設_所在地**, 施設_マンション名等,
  施設_電話番号(固定), **申請者_氏名** (filled on 343 of 607; the notes say a sole
  trader's own name is removed), 許可番号, 初回許可年月日, 開始年月日,
  **終了年月日**.

**Against `japan_register` (shared code, not edited here):**
- **`ADDR_COLS` lacks 施設_所在地 and `NAME_COLS` lacks 施設_名称** (the
  underscore spelling): without them `city_rows` finds no address column and
  step 2 reads nothing. Add both.
- **`OPERATOR_COLS` lacks 申請者_氏名**: add it. Name-rule hits measured in
  memory with it emulated: **2**.
- **`wareki_date` reads 0 of 607 dates**: the list writes `R 8. 5.31`
  (single-letter era, space-padded). Teach it that form, or `in_term` keeps
  every expired permit. Read by hand: **452 rows in term on 2026-08-31**
  (飲食店 326, 喫茶店 20); 311 on 2026-10-02. Pin `as_of` at MHLW's date,
  never today (Kyoto's rule).

**Counts that matter.**

- **MHLW: 2,316 open restaurant permits = 92% of e-Stat's FY2024 in force
  (2,518: old law 789, revised 1,729).** By first-permit year: 2021 205 · 2022
  411 · 2023 424 · 2024 422 · 2025 451 · 2026 403: the city enters every
  permit.
- **Overlap**: 20 of the 346 old-law restaurants in term share a block and
  trade name with an MHLW restaurant permit (`SUPERSEDES` / one pin per
  premises). **Together ~2,642, about 105% of 2,518** (the official count is
  2025-03-31, when 789 old-law permits were in force).
- **Placement (MHLW)**: 1,787 of 2,316 carry an address (77.2%, the scope's
  figure); 176 of those are citywide (一円, caught by `permits_from_rows`) and
  276 permits are vehicles or stalls by 業態. **On fixed premises: 1,611 of
  2,037, 79.1%** (Okayama's measure); 1,593 distinct (address, trade name).
  The old-law list publishes an address on every row.
- **Through `japan_eigyo`**: MHLW storefronts **Food service 1,386, Retail
  827** (Retail includes the notifications, partial and opt-in, as in Fukuoka);
  out by 業態 弁当総菜・仕出し屋 (仕出し) 163, institutional 189, vending 73,
  accommodation 65. Old-law list: Food service 470, Retail 119 before the
  in-term cut.
- **The city's revised-law list** (`dataset_kaiseigor8.4.csv`, 440,265 B,
  2,931 rows, 2026-04-30) duplicates MHLW's permits with the same consent
  blanks (2,254 addressed) and carries 申請者名 (6 name-rule hits), but it is
  four months older and has no coordinates. ⚠️ Recommend MHLW (Kitakyushu's
  precedent); the city list is the fallback if MHLW's file fails.

**Personal services: none.** BODIK org 422029 publishes no 理容 / 美容 /
クリーニング dataset, and the city's 生活衛生 pages
(`/anzen/shokuhin/seikatsu/index.html`) carry guidance only. **A food-only
page, Hiroshima's precedent.**

## Coordinates — a JOIN to MLIT 位置参照情報

One municipality (42202, **no wards**, `"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/42202-24.0a.zip` (495,303 B,
79,138 block keys), town-chōme `.../19.0b/42202-19.0b.zip` (310).

| Tier | MHLW storefronts, addressed, fixed (2,213) | Food service | Old-law list storefronts (589) |
|---|---|---|---|
| Block | **88.6%** | 91.6% | **90.3%** |
| Town-chōme / 大字 centroid | 11.0% | 8.3% | 9.5% |
| Unplaced | 0.4% (ひうみ町 7, not in MLIT's file) | 0.1% | 0.2% |

**Independent check**: MHLW's own coordinates against the block point,
**median 41 m, 90.6% within 250 m** (1,960 rows; 35 over 1 km).
`OWN_POINT_FALLBACK` places MHLW's few misses.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_42_GML.zip`, N03 code 42202
(426 km²; extent W 129.056, S 33.050, E 129.873, N 33.343: the western edge is
宇久島, merged 2006, so check the opening view with `map-view`). Use
**N02-25**.

| N02 line (operator) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 西九州線 (松浦鉄道) | Matsuura Railway Nishi-Kyūshū Line | **22 / 57** | 佐世保, 佐世保中央, 中佐世保, 北佐世保, 山の田, 泉福寺, 左石, 野中, 皆瀬, 中里, 本山, 上相浦, 大学, 相浦, 棚方, 真申, 高岩, すえたちばな, 吉井, いのつき, 潜竜ヶ滝, 江迎鹿町 |
| 佐世保線 (JR九州) | JR Sasebo Line | 5 / 14 | 佐世保, 日宇, 大塔, 早岐, 三河内 |
| 大村線 (JR九州) | JR Ōmura Line | 3 / 15 | 早岐, ハウステンボス, 南風崎 |

- **28 stations inside the city** (N02 station groups; 佐世保 is one group for
  JR and MR, 早岐 one for both JR lines). Median gap to the nearest station
  **851 m**: standard rings.
- ⚠️ **MR's line leaves the city and comes back**: 佐々町's four stations
  (小浦, 神田, 佐々, 清峰高校前) sit between the city's southern stretch and
  吉井-江迎鹿町 (the former 吉井 and 江迎 / 鹿町 towns), so the in-city line is
  two pieces; confirm the order of the sections at build. Draw both; the 佐々町 stations go to `excluded_stations.csv`
  under N03 佐々町, with the 35 beyond in 伊万里, 有田, 平戸 and 松浦.
- **Stub test passes**: no line is cut to a stub (MR 22 of 57, JR 5 and 3).
- **Frequency** (general knowledge, not read from the operators at Step 0):
  MR's 佐世保-佐々 section is the city's commuter line (several trains an
  hour at peak); 吉井-江迎鹿町 beyond 佐々 is roughly hourly. JR's 佐世保線
  carries locals and the みどり limited expresses (they count). Nothing below
  an hourly service; read MR's and JR Kyushu's timetables at build.
- ⚠️ **Gate 3**: MR's own station count (N02 57) and JR Kyushu's per-line
  counts at build; MR's site was not read for a station list at Step 0.
- ⚠️ **OSM `name:en`** at build (MR's hiragana names: すえたちばな, いのつき).

## Scope

**Sasebo City.** MR runs on through 佐々町 to 松浦, 平戸, 伊万里 and 有田; JR
to 有田 (佐賀県) and 川棚. Cut at the line.

## Licences — read 2026-10-02

- **The city's BODIK list — PERMITTED WITH CONDITIONS (CC BY 4.0).**
  佐世保市オープンデータ利用規約 (`https://odcs.bodik.jp/422029/tos/`) 第3条(1):
  「本市で提供している対象データは、クリエイティブ・コモンズ・ライセンス表示4.0国際…によりライセンスされています。」;
  第1条, 「対象データの利用をもって本規約の内容を承諾したものとみなします。」; 第8条, these
  terms prevail over another site's. CKAN `license_id: cc-by-40-intl`. The
  city website's copyright page covers its own pages, not this data.
  - **MUST DISPLAY** (第3条(2)(イ), the edited-use template, filled in):
    「この地図は、以下の著作物を改変して利用しています。(令和8年4月末時点)法改正前食品営業許可施設一覧、佐世保市、CCライセンス（http://creativecommons.org/licenses/by/4.0/deed.ja）」
    (the licence URL may be a link). Add the 法改正後 line only if that list is
    used.
  - **MUST NOT**: 「編集・加工した情報をあたかも本市が作成したかのような態様で公表・利用してはいけません。」
    (第3条(イ)); CC BY 4.0's no-endorsement clause; no completeness claim
    (第5条(1)).
  - **Cost**: 第5条(2) and 第6条, the user's cost for the user's own breach:
    fault-based, accepted for all of Japan.
- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as in
  `okayama.md` and `kitakyushu.md`: the prescribed 出典 line, who processed
  it, no completeness claim, no logo; 免責 2)ウ the minor open point.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **N03**: CC BY 4.0, ⛔ never drawn.

## Privacy

MHLW's file carries 法人名, 法人番号, 法人住所 and phones: never selected. The
old-law list carries **申請者_氏名** and **施設_電話番号(固定)**: read 申請者_氏名 in
memory for the name rule only, never select the phone. Run
`check_personal_exposure.py` (`japan=True`).

## Region

East Asia today, the Japan sub-region with the batch. Project to **UTM 52N
(EPSG:32652)**.

## Still open

- No 🚨 owner item: the two-list shape is Kitakyushu's, food only is
  Hiroshima's, and the page carries the MHLW name-rule bullet.
- ⚠️ **Shared code** (each re-runs the Minato control and the city screens):
  `ADDR_COLS` + 施設_所在地; `NAME_COLS` + 施設_名称; `OPERATOR_COLS` +
  申請者_氏名; `wareki_date` reads `R 8. 5.31`.
- ⚠️ **Old-law expiries** dropped by 終了年月日 against the pinned `as_of`;
  `SUPERSEDES` / one pin per premises for the 20 in both lists.
- ⚠️ **Placement disclosure**: about one fixed restaurant in five withholds
  its address in MHLW's file (Hiroshima's wording).
- ⚠️ **Economic Census join control**: the 2021 census counts **1,003** 飲食店
  establishments in 42202; MHLW's 1,383 distinct placed Food-service premises
  plus the old-law list's in-term restaurants less the overlap is about
  **1.7 per establishment**, inside the built cities' 1.56-1.92. Run it at
  build.
- ⚠️ MR's two in-city pieces; the 宇久島 extent and the opening view; gate 3;
  OSM `name:en`; line colours on both basemaps.

```brief-checks
[
  {
    "id": "sasebo-mhlw-live",
    "claim": "MHLW's open-data file for Sasebo (42202) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=42202_food_business_all.csv",
    "min_bytes": 1000000
  },
  {
    "id": "sasebo-oldlaw-live",
    "claim": "The city's old-law food list (2026-04-30 CSV) is live on BODIK",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/571df2fc-f781-4a2c-b9d7-09e1637b15fe/resource/f7fa490e-026d-4330-8c34-10e7c367c13d/download/dataset_kaiseimaer8.4.csv",
    "min_bytes": 80000
  },
  {
    "id": "sasebo-oldlaw-rows",
    "claim": "The old-law list of 2026-04-30 holds 607 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "f7fa490e-026d-4330-8c34-10e7c367c13d",
    "expect": 607
  },
  {
    "id": "sasebo-oldlaw-columns",
    "claim": "The old-law list spells its address, name and operator columns with an underscore (施設_所在地, 施設_名称, 申請者_氏名) - the shared-code additions",
    "kind": "ckan_fields",
    "domain": "data.bodik.jp",
    "resource_id": "f7fa490e-026d-4330-8c34-10e7c367c13d",
    "present": ["施設_所在地", "施設_名称", "申請者_氏名", "終了年月日"]
  },
  {
    "id": "sasebo-dataset-editions",
    "claim": "The city's food dataset holds the 2026-04-30 old-law edition and monthly files to August 2026",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/dataset/422029_syokuhineigyoukyoka",
    "present": ["令和8年4月末時点", "法改正前食品営業許可施設一覧", "令和8年8月分"]
  },
  {
    "id": "sasebo-bodik-terms",
    "claim": "Sasebo's catalogue terms grant CC BY 4.0 (第3条)",
    "kind": "http_contains",
    "url": "https://odcs.bodik.jp/422029/tos/",
    "present": ["表示4.0国際", "第３条"]
  },
  {
    "id": "sasebo-no-personal-lists",
    "claim": "BODIK org 422029 has no barber (理容) dataset",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=organization:422029&q=%E7%90%86%E5%AE%B9&rows=0",
    "present": ["\"count\": 0"]
  },
  {
    "id": "sasebo-isj-live",
    "claim": "MLIT's block-level address file for Sasebo (42202) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/42202-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "sasebo-projected-crs",
    "claim": "Sasebo projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 129.72,
    "expect": "EPSG:32652"
  }
]
```
