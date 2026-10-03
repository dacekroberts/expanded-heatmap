# Toyota — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live; the downloads are the city's BODIK files, MHLW's file and MLIT's ISJ
zips, each from its publisher). **Run `python scripts/brief_check.py toyota`
before writing any code.** Then the `japan-city` skill. Proposed **Band A:
all three buckets** from the city's own lists. Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from a scratch script (`scripts/screen_japan_join.py` has no Toyota entry; its
table is shared code and was not edited).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none in the city); (2) **lines served only by limited expresses
DO count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, lines are cut at the line, **a one-station stub stays as cut**
(2026-09-27), and an URBAN line cut to a stub goes back to the owner (below);
(4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory share
measured and kept; (5) **the name rule** (2026-09-27); (6) **no page says
"currently operating"**; fault-based cost clauses accepted (2026-09-24).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Toyota
joins the 2026-10-01 batch's precedent: `label_tier: "minor"`, in the Japan
sub-region (by `check_macro_labels.py`, PROBLEMS 0 at 375, 768 and 1200).

**`mode`: `metro`** by the owner's rule of 2026-10-02. No subway, no tram and
no JR station inside the city; the backbone is two heavy-rail commuter
networks (Meitetsu, the Aichi Loop Railway). Linimo (an urban maglev, 2
stations here) does not change it.

---

## The one-line summary

**One standing food-permit list (3,667 rows as of 2026-08-31, 2,922
restaurants and cafés, 594 food shops) and three standing registers (barbers
282, beauty salons 634, laundries 144, 2026-08-31), all CC BY 4.0 on the
city's BODIK catalogue.** The block join places 80.2% of the 4,575 kept
premises at the block and 12.8% at the town or 大字 centroid; 7.0% stay
unplaced. **Rail: 25 station groups inside the city (Aichi Loop 12 of 23,
Meitetsu Mikawa 10 of 23, Meitetsu Toyota 3 of 8, Linimo 2 of 9).**

---

## Business leg — the city's BODIK catalogue (organisation 232114)

| | Food (`232114_permit_food_facility`) | Barbers | Beauty | Laundries |
|---|---|---|---|---|
| **Dataset** | 「オープンデータ　食品営業許可施設一覧（2026年8月31日現在）」 | `232114_environmental_health_service_facility` 「環境衛生営業施設一覧」, resource 理容所施設一覧.xlsx | same dataset, 美容所施設一覧.xlsx | same dataset, クリーニング所施設一覧.xlsx |
| **File** | `https://data.bodik.jp/dataset/385d18b1-7493-4a82-8b0d-b00d2996da69/resource/91fe2bf3-0a1a-4daa-acf4-5737ca31ab83/download/20260907_0800.xlsx`: **405,542 B**, one sheet `EXCEL_情報公開リスト` | `https://data.bodik.jp/dataset/57c36023-1519-4f73-9bd6-ca6dd4df7493/resource/cec8cb27-29e7-4b29-8995-36f51ac36abd/download/_20268.xlsx`: **36,363 B** | `…/resource/4019ebe4-d8e2-4bf2-a890-0beba402e732/download/_20268.xlsx`: **80,074 B** | `…/resource/39c48071-845b-471b-9d10-bebc78a05bfd/download/_20268.xlsx`: **27,432 B**, two sheets (洗場 34, 取次店 110) |
| **Rows** | **3,667** | **282** | **634** | **144** |
| **As of** | **2026-08-31** (title; uploaded 2026-09-09; newest 許可年月日 2026-08-31) | 2026-08-31 (「原則毎月10日頃に前月末時点の情報に更新」; uploaded 2026-09-14) | same | same |
| **Cadence** | monthly, 「毎月5日を目処」 | monthly | monthly | monthly |
| **Columns** | 許可番号, 営業の種類, **施設の名称**, **施設所在地**, 施設所在地ビル名, **営業者氏名**, 代表者肩書き, **代表者氏名**, 営業者住所, 営業者住所ビル名, 施設電話番号, 有効期間始期, 有効期間終期, 許可年月日, 初回許可日 | No., **施設名称**, **施設所在地**, 施設TEL, **開設者氏名（法人）**, 開設者住所（法人）, 確認年月日, 確認番号 | as barbers | as barbers; the 取次店 sheet names the shop **施設名称１** and its branch 施設名称２（営業所名） |

- ⚠️ **Every resource of the register dataset is named `_20268.xlsx`**: fetch
  by resource id and save under distinct names (`riyo_202608.xlsx` and so on).
  The food file's name changes each month (`20260907_0800.xlsx`); read the
  resource URL from `package_show`, never a fixed name (Fukuoka's lesson).
- **Columns against `japan_register` (shared code, not edited here)**:
  `ADDR_COLS` covers 施設所在地; `NAME_COLS` covers 施設の名称, 施設名称 and
  施設名称１; `TYPE_COLS` covers 営業の種類. `OPERATOR_COLS` covers 営業者氏名 and
  代表者氏名; ⚠️ it lacks the registers' **開設者氏名（法人）** (companies only,
  below): add it so a renamed column stops the build. `xlsx_rows` already reads
  both laundry sheets (each has the address column).
- **Food: a standing register, not a stream.** 有効期間終期 runs 2026-08-31 to
  2033-03-31 and no row ends before the as-of date; 初回許可日 runs back to 1983;
  許可年月日 starts 2020-03-16 because every permit is renewed within its term
  (at most about seven years). The catalogue record says what it leaves out:
  「（臨時営業や露店等を除く）」, so no row is a vehicle or a stall (0 measured).
  Toyohashi's 12-month stream is not this shape.
- **Food by type**: 飲食店営業 2,921 and 喫茶店営業 1 = **2,922 Food service**;
  菓子製造業 361, 魚介類販売業 89, 食肉販売業 78, そうざい製造業 66 = **594
  Retail**; out by `japan_eigyo` ("no rule": manufacturing, 食肉処理業 and the
  like) 151. ⚠️ 164 restaurant permits end later in 2026 (after the as-of
  date); the next monthly edition renews or drops them, so pin `as_of` to the
  list's own date (Kyoto's rule).
- **Registers: standing**, 確認年月日 from 1957 (barbers) to 2026. One beauty
  row is a 一円 (citywide) salon, not a premises. One beauty row's 確認年月日
  reads 1900-01-07, an Excel zero-date artefact.
- **Completeness against the official counts** (e-Stat 衛生行政報告例 FY2024,
  year end 2025-03-31, row 愛知県豊田市):

| | Official | The city's lists (2026-08-31) | Share |
|---|---|---|---|
| 飲食店営業 (old law 1,099 + revised 2,799) | 3,898 | 2,921 | **74.9%** |
| 理容所 | 295 | 282 | 95.6% |
| 美容所 | 627 | 634 | 101.1% |
| クリーニング所 (取次所 134) | 170 | 144 (取次 110, 洗場 34) | 84.7% |

  The restaurant gap is the list's own exclusion of temporary and stall
  permits, which the official count includes (Toyota's old-law
  「その他」 is 714 of 1,099, against Hamamatsu's 439 of 2,337) and which
  `japan_eigyo` drops anyway; the Economic Census control below says the list
  is not thin. The laundry gap is 24 pick-up counters; read 取次所 closures at
  build.

### MHLW's file

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=23211_food_business_all.csv`:
260,438 B, 880 rows (届出 812, 許可 61, closed 7): the city enters only the
online filings there. **Not used**: the city's own list is complete for
permits, and its notifications are opt-in filings. Toyama's precedent for a
city with a complete own list is to leave MHLW's notifications out and say so
in the standing bullet.

### Operator columns and the name rule

- **Food**: 営業者氏名 is filled on all 3,667 rows, **1,800 without a company
  marker**, so the city publishes sole traders' names; 代表者氏名 (2,014) names
  a company's representative. The rule runs: **14 food rows flagged** (counted
  in memory, nothing kept).
- **Registers**: 開設者氏名（法人） is filled only for companies (21 of 282
  barbers, 155 of 634 beauty salons, 111 of 144 laundries, every one with a
  company marker); the catalogue says 「個人の営業者の住所や電話番号等については公開の対象としておりません」.
  The rule compares nothing there: Toyama's position (owner, 2026-10-02:
  Hiroshima's MHLW-style bullet for the rows it cannot check).

---

## ⚠️ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 23211)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/23211-24.0a.zip` (577,418 B) and
`…/19.0b/23211-19.0b.zip` (23,334 B): 106,154 block keys, 1,206 town-chōme.
Ward-less (`"wardless": True`).

| Tier | Food service (2,922) | Food retail (594) | Personal services (1,059) | All (4,575) |
|---|---|---|---|---|
| Block | 80.3% | 69.7% | 85.6% | **80.2%** |
| Town-chōme / 大字 centroid | 13.6% | 20.0% | 6.7% | 12.8% |
| Unplaced | 6.1% | 10.3% | 7.6% | **7.0%** |

- **What misses (321 rows)**: (a) **浄水町1–5丁目, 52 rows**, a 区画整理 town
  around 浄水 station whose 丁目 MLIT's 24.0a file does not have (it keys 浄水町
  only as a 大字 with 小字); `join_city` tries the 小字 lookup and stops. (b)
  Rural addresses that write the 小字 without 字 (四郷町森前南, 上原町一丁田):
  left unplaced by design (`join_city`'s has_koaza rule, measured on
  Hiroshima). The chōme tier is mostly the mountain towns (足助町 97 rows).
- ⚠️ **Recommended at build (shared code)**: a 丁目 the ISJ edition does not
  know falls to its 大字's centroid instead of the 小字 lookup (52 rows near a
  station). Re-run the Minato control.
- **No publisher coordinates** (the list has none; MHLW's 61 permits are too
  few to serve as Fukuoka's fallback). The independent check is GSI's address
  search on a sample at build (`screen_japan_join.gsi_check`'s method).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (23211)

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_23_GML.zip`. N03
extent W 137.0397, S 34.9906, E 137.5811, N 35.2912 (the 2005 merger reached
the mountains of 足助 and 稲武). **27 station records, 25 N02_005g groups.**

| N02 line (operator) | Public name | In the city / total | Reading |
|---|---|---|---|
| 愛知環状鉄道線 (愛知環状鉄道) | Aichi Loop Line | **12 / 23** | cut at the line (on to 岡崎 and 瀬戸); operator's station index lists **23** (gate 3 exact) |
| 三河線 (名古屋鉄道) | Meitetsu Mikawa Line | **10 / 23** | cut at the line (on to 知立 and 碧南) |
| 豊田線 (名古屋鉄道) | Meitetsu Toyota Line | **3 / 8** (梅坪, 上豊田, 浄水) | 🚨 an urban line (through trains to the Nagoya subway's Tsurumai Line) cut to 3 stations |
| 東部丘陵線 (愛知高速交通) | Linimo | **2 / 9** (八草, 陶磁資料館南) | 🚨 an urban line cut to 2 stations; 八草 is also the Aichi Loop's |

- **Interchanges** (one group each): 梅坪 (Mikawa and Toyota lines, 191 m
  apart in N02), 八草 (Aichi Loop and Linimo). **Close pairs kept apart**:
  新豊田 (Aichi Loop) and 豊田市 (Meitetsu) 255 m; 新上挙母 and 上挙母 319 m.
- **Median nearest-station gap 966 m**: standard rings.
- ⚠️ **Gate 3** for Meitetsu (Mikawa 23, Toyota 8) and Linimo (9) from the
  operators at build.
- ⚠️ **OSM `name:en`** for 25 groups at build (not queried for this brief).

## Scope

**Toyota City (23211), one municipality, no wards.** Every line runs on to a
neighbor (岡崎, 瀬戸, 長久手, 日進, みよし, 知立); cut at the line.

## Licences — read 2026-10-02 (`licence-read`)

- **The food list — PERMITTED WITH CONDITIONS (CC BY 4.0).** `package_show`
  records `license_id: cc-by-40-intl`. The city's terms, 豊田市オープンデータカタログページ利用規約
  (on the catalogue, `https://odcs.bodik.jp/232114/tos/`, and the city's copy,
  `https://www.city.toyota.aichi.jp/shisei/tokei/1018965/1019046.html`, updated
  2021-12-07), apply to 「ページタイトルに『オープンデータ』を含むページの集合」 and
  license their content 「注があるものを除いて、クリエイティブ・コモンズ・ライセンス 表示4.0国際のもとで」;
  the city's site copyright page gives way (「…著作権の表記…にかかわらず本規約に従って」).
  The food dataset's title begins オープンデータ and is listed on the city's
  catalogue page.
  - **MUST DISPLAY** (3(2), the form for a modified work):
    `この地図は、以下の著作物を改変して利用しています。 オープンデータ　食品営業許可施設一覧（2026年8月31日現在）、環境衛生営業施設一覧、豊田市、クリエイティブ・コモンズ・ライセンス 表示4.0国際（https://creativecommons.org/licenses/by/4.0/deed.ja）`;
    the URL may be a link on the licence words. The food title carries its
    month: the credit follows the edition used.
  - **MUST NOT**: present the edited data as if the city made it (3(1)).
  - **Cost**: 4(6) puts claims from the user's own breach at the user's cost;
    **5 豊田市への補償** asks the user to repay the city's costs (damages
    included) from claims arising from the user's breach or infringement. That
    is Matsuyama's 第5条 (弁償), breach-triggered: ✅ the fault-based class,
    accepted for every Japanese source (2026-09-24). Japanese law; Nagoya
    District Court (7).
- **The registers — the same terms, one reading to confirm (🚨 below).** Their
  dataset, 「環境衛生営業施設一覧」, also records `cc-by-40-intl` in the city's
  own catalogue, but its title does not contain オープンデータ, which is how the
  terms define their scope.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**: CC
  BY 4.0, picks stations, ⛔ never drawn.

## Privacy

Food: read 施設の名称, 施設所在地, 施設所在地ビル名, 営業の種類 and the dates;
営業者氏名 and 代表者氏名 are read in memory by the name rule and never kept;
**営業者住所 and 営業者住所ビル名 are an operator's own address: never
selected**, nor 施設電話番号 or 代表者肩書き. Registers: never select
開設者住所（法人） or 施設TEL. Run `check_personal_exposure.py` with `japan=True`.

## Region

The Japan sub-region (minor tier, above); until it lands, `"region": "East
Asia"`. `"country": "Japan"`. Project to **UTM 53N (EPSG:32653)**.

## Open items

- 🚨 **Two urban lines cut to stubs: recommend DRAW THEM AS CUT**, Sakai's
  Midōsuji precedent (owner, 2026-10-02: 3 of 20 stations drawn cut). The
  Meitetsu Toyota Line keeps 3 of 8 (梅坪, 上豊田, 浄水; the rest are in みよし
  and 日進) and Linimo 2 of 9 (八草, an Aichi Loop interchange, and
  陶磁資料館南). Leaving them out would drop 3 rings (梅坪 and 八草 stay on
  other lines).
- 🚨 **The registers' licence scope: recommend ACCEPT the permitting
  reading.** The dataset declares CC BY 4.0 in the city's own catalogue, and
  its sheets are titled 「オープンデータ_理容所」 and so on; only its dataset
  title lacks the word the terms use to define their scope. Hiroshima's
  dataset-level licence was accepted on the same kind of reading (owner,
  2026-09-24). Without it the page is food only.
- ⚠️ **The food list holds 74.9% of the official restaurant count**; the
  catalogue says temporary and stall permits are left out, and the census
  control (below) reads normal. Page wording: the standing bullets suffice
  (stalls and vehicles are off every Japanese map); no Osaka-style share
  bullet is proposed.
- ⚠️ **Shared code**: `OPERATOR_COLS` + 開設者氏名（法人）; the 浄水町 丁目
  fallback; Toyota's `japan.CITIES` entry (`"wardless": True`, `"n02": "25"`,
  EPSG 32653). Each re-runs the Minato control.
- ⚠️ **The Economic Census join control** (`scripts/japan_census_control.py`,
  after step 2): the 2021 census counts **1,364** 飲食店 establishments in 23211;
  2,692 distinct placed Food-service premises (one per address and trade name)
  is **1.97 per establishment**, just above the built cities' 1.56–1.92
  (Okayama's brief). Run it on the built pins.
- ⚠️ The 菓子 / そうざい factory share, printed by step 2 (Toyota is a
  manufacturing city; read the 工場 names).
- ⚠️ Gate 3 (Meitetsu, Linimo), OSM names, line colours on both basemaps, the
  opening view (the N03 box reaches the mountains).

```brief-checks
[
  {
    "id": "toyota-food-live",
    "claim": "Toyota City's food-permit workbook (as of 2026-08-31) is keyless and live on BODIK",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/385d18b1-7493-4a82-8b0d-b00d2996da69/resource/91fe2bf3-0a1a-4daa-acf4-5737ca31ab83/download/20260907_0800.xlsx",
    "min_bytes": 300000
  },
  {
    "id": "toyota-barber-live",
    "claim": "Toyota City's barber register (resource cec8cb27, 2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/57c36023-1519-4f73-9bd6-ca6dd4df7493/resource/cec8cb27-29e7-4b29-8995-36f51ac36abd/download/_20268.xlsx",
    "min_bytes": 20000
  },
  {
    "id": "toyota-beauty-live",
    "claim": "Toyota City's beauty-salon register (resource 4019ebe4) is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/57c36023-1519-4f73-9bd6-ca6dd4df7493/resource/4019ebe4-d8e2-4bf2-a890-0beba402e732/download/_20268.xlsx",
    "min_bytes": 50000
  },
  {
    "id": "toyota-laundry-live",
    "claim": "Toyota City's laundry register (resource 39c48071, two sheets) is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/57c36023-1519-4f73-9bd6-ca6dd4df7493/resource/39c48071-845b-471b-9d10-bebc78a05bfd/download/_20268.xlsx",
    "min_bytes": 15000
  },
  {
    "id": "toyota-food-ckan",
    "claim": "The food dataset's record says CC BY 4.0 and points at the 2026-08-31 file",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=232114_permit_food_facility",
    "present": ["\"license_id\": \"cc-by-40-intl\"", "20260907_0800.xlsx"]
  },
  {
    "id": "toyota-registers-ckan",
    "claim": "The 環境衛生営業施設一覧 record says CC BY 4.0 and still holds the three register resources",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=232114_environmental_health_service_facility",
    "present": ["\"license_id\": \"cc-by-40-intl\"", "cec8cb27-29e7-4b29-8995-36f51ac36abd", "4019ebe4-d8e2-4bf2-a890-0beba402e732", "39c48071-845b-471b-9d10-bebc78a05bfd"]
  },
  {
    "id": "toyota-catalogue-terms",
    "claim": "The city's catalogue terms license CC BY 4.0 (deed.ja linked)",
    "kind": "http_contains",
    "url": "https://odcs.bodik.jp/232114/tos/",
    "present": ["creativecommons.org/licenses/by/4.0/deed.ja"]
  },
  {
    "id": "toyota-city-terms-copy",
    "claim": "The city's own copy of the terms (page 1019046) still links CC BY 4.0",
    "kind": "http_contains",
    "url": "https://www.city.toyota.aichi.jp/shisei/tokei/1018965/1019046.html",
    "present": ["licenses/by/4.0/deed.ja"]
  },
  {
    "id": "toyota-city-catalogue-lists-food",
    "claim": "The city's open-data catalogue page links the food dataset",
    "kind": "http_contains",
    "url": "https://www.city.toyota.aichi.jp/shisei/tokei/1018965/index.html",
    "present": ["232114_permit_food_facility"]
  },
  {
    "id": "toyota-mhlw-live",
    "claim": "MHLW's open-data file for Toyota (23211) answers keyless - online filings only, not used",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=23211_food_business_all.csv",
    "min_bytes": 100000
  },
  {
    "id": "toyota-isj-live",
    "claim": "MLIT's block-level address file for Toyota (23211) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/23211-24.0a.zip",
    "min_bytes": 300000
  },
  {
    "id": "toyota-estat-riyo-biyo",
    "claim": "e-Stat's 衛生行政報告例 FY2024 第10表 (barbers and beauty salons by core city) answers keyless - the completeness control",
    "kind": "http_ok",
    "url": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359178&fileKind=1",
    "min_bytes": 5000
  },
  {
    "id": "toyota-aikan-23-stations",
    "claim": "The Aichi Loop Railway's station index lists its 23 stations, 岡崎 to 高蔵寺 (gate 3)",
    "kind": "http_contains",
    "url": "https://www.aikanrailway.co.jp/station/",
    "present": ["okazaki.html", "kouzouji.html", "shintoyota.html", "yakusa.html"]
  },
  {
    "id": "toyota-projected-crs",
    "claim": "Toyota projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 137.16,
    "expect": "EPSG:32653"
  }
]
```
