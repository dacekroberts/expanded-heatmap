# Hakodate — build brief

**Step 0 measured 2026-10-02** (the 2026-10-01 screen's figures re-verified
live; the downloads are the master list's named sources, MHLW's file and MLIT's
ISJ zips). **Run `python scripts/brief_check.py hakodate` before writing any
code.** Then the `japan-city` skill. Band B (owner, 2026-10-01): **personal
services only, on Yokohama's precedent** ("**This map shows personal services
only: barbers, beauty salons and laundries.**"; the page states that no food
register is published). Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from a scratch script
(`scripts/screen_japan_join.py` has no Hakodate entry; its table is shared
code).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; Shin-Hakodate-Hokuto is outside the city); (2) **lines served
only by limited expresses DO count** (2026-09-28); (3) **the city line
only**: only stations inside the city get rings, JR and the private lines are
cut at the line, **a one-station stub stays as cut** (2026-09-27), and an
URBAN line cut to a stub goes back to the owner; (4) **菓子製造業 and
そうざい製造業 count, in Retail** (no food bucket here); (5) **the name rule**:
where the trade name IS the operator's own name, the pin shows its permit type
(2026-09-27); (6) **no page says "currently operating"**: the lists keep
closed premises; fault-based cost clauses are accepted (2026-09-24).

**✅ Minor label tier (owner, 2026-10-02).** Hakodate carries
`label_tier: "minor"`: dot and tooltip in every view, pill only in its own
region. Per the `japan-city` skill: a Japan sub-region (one or split, by
`check_macro_labels.py`, PROBLEMS 0 at 375, 768 and 1200), every Japanese city
moved into it, `REGION_LABELS_ALSO["East Asia"]` gaining it. **The eight built
Japanese cities stay eligible.**

---

## The one-line summary

**Three standing registers (barbers 283, beauty salons 677, laundries 143) as
of 2026-08-31, CC BY 2.1 JP: 1,100 fixed premises, joined to MLIT's block
files at 94.0% and the rest at the town-chōme centroid, nothing unplaced.**
"抜粋" (excerpt) is the COLUMNS: each file publishes five or six fields of the
register. **The rows are complete**: against MHLW's official count (衛生行政報告例,
FY2024 year-end) the files hold 98% (beauty exactly 677 = 677). **The
Hakodate City Tram's 26 stops plus 3 JR stations: 29 stations, a 363 m median
gap, so halved rings.**

---

## Business leg — the 生活衛生課's registers

Page `https://www.city.hakodate.hokkaido.jp/docs/2019072900024/`
(「環境衛生関係施設等の情報」, 保健所 生活衛生課 環境衛生担当, 公開日 2026-09-10).
Each list is posted as CSV and PDF, labelled 「…施設一覧（抜粋）」 and
「令和8年8月31日時点」.

| File (`…/docs/2019072900024/file_contents/`) | Bytes | Rows | Kind |
|---|---|---|---|
| `202608riyo.csv` | **24,680** | **283** | 理容所 (barbers) |
| `202608biyo.csv` | **62,308** | **677** | 美容所 (beauty salons) |
| `R80831cleaning.csv` | **16,526** | **143** | クリーニング所: 取次 101 · 一般 39 · **無店舗 3** (not premises; `japan_eigyo` drops them) |

- **As of 2026-08-31**, served 2026-09-10 (Last-Modified). The file names
  carry the month; the page states no cadence (its one 「次回の更新掲載は，令和8年10月」
  belongs to the building-hygiene list beside them).
- **Encoding cp932, with title rows ABOVE the header** (two in the barber and
  beauty files, one in the laundry file). ⚠️ `city_rows()` takes a CSV's first
  line as its header, so it reads no address column here. Teach it to find a
  CSV's header by its address column, as `xlsx_rows()` already does (a
  shared-code change; re-run the Minato control and the built cities'
  screens).
- **Columns**: (an unnamed row number), 確認番号, 確認日, 種別 (laundry only),
  **施設名称**, **施設所在地**, 開設者氏名. No type column in the barber and beauty
  files: the source decides the bucket (`japan_eigyo.PERSONAL_SOURCES`).
- **Against `japan_register`'s column tuples (shared code, not edited
  here):** `ADDR_COLS` covers 施設所在地, `NAME_COLS` 施設名称, `TYPE_COLS` 種別.
  **`OPERATOR_COLS` does NOT cover 開設者氏名**: add it, or the name rule
  compares nothing. One hit measured in memory (barbers).

**What 抜粋 cut.** The register under each law holds more than these fields
(the operator's address, the managing barber or beautician, staff); the files
publish five or six of them and no phone or operator address. **The rows**:
確認日 runs from the 1950s (laundries) and 1960s (barbers, beauty) to 2026,
so these are standing registers, not a stream (barbers by decade: 8 · 32 · 51
· 58 · 48 · 49 · 37). Per resident (Hakodate about 240,000) there are 1.2
barbers and 2.8 beauty salons per 1,000, against Kitakyushu's 0.9 and 2.5.

**✅ The official count settles it: 抜粋 dropped no rows (owner approved the
e-Stat download, 2026-10-02).** 衛生行政報告例 FY2024, 生活衛生 第10表 (理容所 /
美容所, `statInfId=000040359178`, 8,126 B) and 第11表 (クリーニング所,
`statInfId=000040359179`, 7,514 B), CSV, cp932, saved under
`data/hakodate/raw/estat_eisei_r6_*_by_city.csv`. Row 北海道函館市, facilities at
the year end (2025-03-31) against the files 17 months later (2026-08-31):

| | Official (FY2024 year end) | The city's files (2026-08-31) | Share |
|---|---|---|---|
| 理容所 | 295 | 283 | 96% |
| 美容所 | 677 | 677 | 100% |
| クリーニング所 | 150 (取次所 108) | 140 (取次 101, 一般 39) | 93% |
| 無店舗取次店 | 3 | 3 (無店舗, set aside) | 100% |
| **Fixed premises** | **1,122** | **1,100** | **98.0%** |

The shortfall (22) is what 17 months of closures among barbers and laundries
would leave; no category is missing.

**What is missing: food.** The city publishes only a rolling 12 months of NEW
food permits (`/docs/2019100700015/`: 「新規許可取得施設等を月ごとに集計し、12ヶ月分公開」;
`202608syokuhin.csv` and eleven others), which cannot rebuild a register.
MHLW's file (`…param=01202_food_business_all.csv`, 335,504 B, 972 rows, as of
2026-08 end) holds only the online filings: **65** open restaurant permits
against **3,548** in force (e-Stat FY2024). No food leg.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報

Hakodate is one municipality (01202, no wards): block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/01202-24.0a.zip`, town-chōme
`.../19.0b/01202-19.0b.zip`. 8,410 block keys, 207 town-chōme. The shared
functions read a ward-less city as is (ward empty on both sides).

| Tier | Barbers (283) | Beauty (677) | Laundries (140 fixed) | All (1,100) |
|---|---|---|---|---|
| Block | 92.9% | 95.3% | 90.0% | **94.0%** |
| Town-chōme / 大字 centroid | 7.1% | 4.7% | 10.0% | 6.0% |
| Unplaced | 0.0% | 0.0% | 0.0% | **0.0%** |

Measured with the CSVs' headers found in a scratch reader. **No publisher
coordinates**: the independent check is GSI's address search on a sample at
build (`screen_japan_join.gsi_check`'s method).

---

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_01_GML.zip` (the
shared cache), with `stub_test()`'s method and N03 code 01202 (677 km²: the
2004 merger brought in 戸井, 恵山, 椴法華 and 南茅部; every station is in the old
city). Use **N02-25** (`"n02": "25"`). No Shinkansen station inside.

| N02 line (operator) | Public name | In the city / total | Note |
|---|---|---|---|
| 本線, 湯の川線, 宝来・谷地頭線, 大森線 (函館市) | Hakodate City Tram (函館市電; routes 2 湯の川–谷地頭 and 5 湯の川–函館どつく前) | **26 stops** (29 records over 4 sections, all 100% inside) | Operator's per-stop timetable index lists **26** (gate 3 exact) |
| 函館線 (JR北海道) | JR Hakodate Line | **3 / 84** (函館, 五稜郭, 桔梗) | cut at the line, as Sapporo's (14 of 84) |
| 道南いさりび鉄道線 | South Hokkaido Railway | **1 / 12** (五稜郭) | a one-station stub: **stays as cut** (standing call); its trains run on to 函館 over JR track |

- **29 stations inside the city** (N02 station groups). Median gap to the
  nearest station **363 m**: **halved rings** (0.05 / 0.1 / 0.2 / 0.3 mi) on
  the spacing rule, as Hiroshima (357 m).
- ⚠️ **Drawing the tram**: N02's four legal sections are not public names.
  Sapporo's precedent draws its streetcar's sections as one line under its
  public name; do the same ("Hakodate City Tram"), or draw routes 2 and 5 with
  Tokyo's `route` if the owner prefers the route numbers.
- ⚠️ **One stop is signed under a naming-rights name**: N02's 函館アリーナ前 is
  the operator's 「アリーナ前（函館サーモン・まるなまアリーナ前）」. Settle the English
  name at build.
- ⚠️ **OSM `name:en`** for every station and tram stop is a build-time read
  (one Overpass query with `osm_tram_stop_query`; not run for this brief).
- ⚠️ The N03 extent is wide (the merged eastern towns): `CITY_BBOX` from it,
  but check the opening view with `map-view` so the map frames the stations.

## Scope

**Hakodate City.** JR and the South Hokkaido Railway run on to Nanae and
Hokuto; cut at the line.

## Licences — read 2026-10-02

- **The city's registers — PERMITTED WITH CONDITIONS (CC BY 2.1 JP).** The
  list page itself says 「このページの本文とデータは クリエイティブ・コモンズ 表示 2.1
  日本ライセンスの下に提供されています」 (linked to
  `http://creativecommons.org/licenses/by/2.1/jp/`), then: show the data's
  source, show that it was edited or processed, never present processed data
  as if the city made it, and clear any third party's rights ourselves. The
  site default (`/docs/2014021000114/`) bars reuse 「オープンデータとして掲載している
  ものを除き」, so it yields.
  - **MUST DISPLAY** (Kobe's form, also CC BY 2.1 JP):
    `出典：「環境衛生関係施設等の情報」（函館市）（https://www.city.hakodate.hokkaido.jp/docs/2019072900024/）を加工して作成`
    with © and the CC BY 2.1 JP link.
  - **MUST NOT** present the map as the city's own. No cost or indemnity
    clause on the page.
- **MLIT 位置参照情報 and N02**: PDL 1.0 (the skill's notice lines). **N03**: CC
  BY 4.0, ⛔ never drawn.

## Privacy

Every file carries **開設者氏名** (individual operators' names). Select 施設名称,
施設所在地, 種別 and the dates; read 開設者氏名 in memory for the name rule only.
Run `check_personal_exposure.py` (`japan=True`).

## Region

East Asia today, moving to the Japan sub-region with the batch. Project to
**UTM 54N (EPSG:32654)**.

## Still open

- ✅ **Whether 抜粋 cut any rows: it did not** (owner, 2026-10-02: the e-Stat
  download approved). The files hold 1,100 of the official 1,122 fixed
  premises (98.0%; beauty 677 of 677), see "What 抜粋 cut" above. 抜粋 is the
  columns. Credit e-Stat (政府統計の総合窓口) as a measurement source in the
  build's provenance notes; it is not drawn.
- ⚠️ **Shared code**: `city_rows()` finds a CSV header below title rows;
  `OPERATOR_COLS` + 開設者氏名. Each re-runs the Minato control.
- ⚠️ The tram drawn as one line (Sapporo's precedent); the naming-rights stop;
  OSM `name:en`; line colours on both basemaps; the opening view.
- ⚠️ **No Economic Census food control applies** (no food leg). A GSI sample
  is the coordinate check.

```brief-checks
[
  {
    "id": "hakodate-barber-live",
    "claim": "Hakodate's barber register (2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.hakodate.hokkaido.jp/docs/2019072900024/file_contents/202608riyo.csv",
    "min_bytes": 15000
  },
  {
    "id": "hakodate-beauty-live",
    "claim": "Hakodate's beauty-salon register (2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.hakodate.hokkaido.jp/docs/2019072900024/file_contents/202608biyo.csv",
    "min_bytes": 40000
  },
  {
    "id": "hakodate-laundry-live",
    "claim": "Hakodate's laundry register (2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.hakodate.hokkaido.jp/docs/2019072900024/file_contents/R80831cleaning.csv",
    "min_bytes": 10000
  },
  {
    "id": "hakodate-page-licence",
    "claim": "The register page links the CC BY 2.1 JP licence and the three August 2026 files (ASCII markers: the server sends no charset, so the checker cannot read the page's Japanese)",
    "kind": "http_contains",
    "url": "https://www.city.hakodate.hokkaido.jp/docs/2019072900024/",
    "present": ["creativecommons.org/licenses/by/2.1/jp", "202608riyo.csv", "202608biyo.csv", "R80831cleaning.csv"]
  },
  {
    "id": "hakodate-food-stream-only",
    "claim": "Hakodate publishes only a rolling 12 months of new food permits: 2025-09 to 2026-08, nothing older",
    "kind": "http_contains",
    "url": "https://www.city.hakodate.hokkaido.jp/docs/2019100700015/",
    "present": ["202509syokuhin.csv", "202608syokuhin.csv"],
    "absent": ["202508syokuhin.csv"]
  },
  {
    "id": "hakodate-tram-26-stops",
    "claim": "The Hakodate City Tram's per-stop timetable index lists 26 stops (gate 3)",
    "kind": "http_contains",
    "url": "https://www.city.hakodate.hokkaido.jp/docs/2014012100939/",
    "present": ["time/T/01.html", "time/T/26.html"],
    "absent": ["time/T/27.html"]
  },
  {
    "id": "hakodate-estat-riyo-biyo",
    "claim": "e-Stat's 衛生行政報告例 FY2024 第10表 (barbers and beauty salons by core city) answers keyless - the 抜粋 control",
    "kind": "http_ok",
    "url": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359178&fileKind=1",
    "min_bytes": 5000
  },
  {
    "id": "hakodate-estat-cleaning",
    "claim": "e-Stat's 衛生行政報告例 FY2024 第11表 (laundries by core city) answers keyless - the 抜粋 control",
    "kind": "http_ok",
    "url": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359179&fileKind=1",
    "min_bytes": 5000
  },
  {
    "id": "hakodate-isj-live",
    "claim": "MLIT's block-level address file for Hakodate (01202) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/01202-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "hakodate-projected-crs",
    "claim": "Hakodate projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.73,
    "expect": "EPSG:32654"
  }
]
```
