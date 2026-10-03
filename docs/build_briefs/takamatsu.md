# Takamatsu — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live; downloads are the city's own files, MHLW's file and MLIT's ISJ zips).
**Run `python scripts/brief_check.py takamatsu` before writing any code.** Then
the `japan-city` skill. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from a scratch script
(`scripts/screen_japan_join.py` has no Takamatsu entry; its table is shared
code).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none in the city); (2) **lines served only by limited expresses
DO count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27), and an URBAN line cut to a stub goes back to
the owner; (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**: where
the trade name IS the operator's own name, the pin shows its permit type
(2026-09-27); (6) **no page says "currently operating"**; sightseeing
funiculars are left out; fault-based cost clauses are accepted (2026-09-24).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).**
Takamatsu carries `label_tier: "minor"`: dot and tooltip in every view, pill
only in its own region. It joins the Japan sub-region the 2026-10-01 batch
creates (one region or a split, by `check_macro_labels.py`, PROBLEMS 0 at 375,
768 and 1200; `REGION_LABELS_ALSO["East Asia"]` gains it).

**✅ `mode`: `metro`** (owner's rule, 2026-10-02). JR is not the largest
network inside the city (13 stations against Kotoden's 33), and no subway or
tram is drawn, so the mode follows the backbone: Kotoden's three lines are
railways (N02 class 12, 普通鉄道), not trams or light rail.

---

## The one-line summary

**Three buckets from the city's own open data (オープンデータたかまつ, CC BY
4.0): a full food-permit list as of 2026-08-31 (7,372 permits; 5,558
restaurant permits, 102% of the official 5,439) and standing registers of
barbers (371), beauty salons (1,188) and laundries (332), each 99-104% of the
official count. Every row carries an address; block-level join 87.1% (food) /
83-84% (registers), 88.7% / 85.7-87.3% with one new shared rule (字甲), and
under 1% unplaced with it. 46 stations inside the city: Kotoden 33 and JR 13.
Band A.**

---

## Business leg

The city publishes on オープンデータたかまつ (`https://opendata.takamatsu-fact.com/`,
footer "Copyright © 2023 Takamatsu City"; catalogue
`https://opendata.smartcity-takamatsu.jp/ckan/`, every dataset `license_id:
cc-by`). The files are generated from the city's GitHub repository
(`github.com/takamatsu-city/opendata`, `data/<dataset>/`, uploaded by
保健所 生活衛生課 about the 10th of each month). Fetch from
opendata.takamatsu-fact.com only.

| Dataset (CKAN title) | File | Bytes | Rows | As of |
|---|---|---|---|---|
| 食品等営業許可施設一覧 (0108) | `https://opendata.takamatsu-fact.com/licensed_food_business_facility_list/data.csv` | **2,030,146** | **7,372** | **2026-08-31** (the source workbook 食品関係事業者一覧（2026.8.31時点）.xlsx) |
| 理容所新規開設一覧 (0100) | `https://opendata.takamatsu-fact.com/new_barber_shops/data.csv` | **61,609** | **371** | 2026-08 (`0100_202608.xlsx`) |
| 美容所新規開設一覧 (0101) | `https://opendata.takamatsu-fact.com/new_beauty_salons/data.csv` | **215,281** | **1,188** | 2026-08 (`0101_202608.xlsx`) |
| クリーニング所新規開設一覧 (0102) | `https://opendata.takamatsu-fact.com/new_cleanings/data.csv` | **78,459** | **332** | 2026-08 (`0102_202608.xlsx`) |

- Encoding UTF-8, comma CSV, header on line 1. Last-Modified 2026-09-30 on all
  four. **Cadence monthly** (the repository replaces the month-end workbook
  each month and deletes the previous one).
- **"新規開設" is a misnomer: the registers are standing registers.** 開設確認日
  runs from 1948 (beauty) and 1953 (barbers) to 2026-08, and the counts match
  the official year-end count (below).
- **Food columns**: 施設名称１, 施設名称２, 施設名称かな, 施設郵便番号,
  **施設所在地１**, 施設所在地２, 施設電話番号, **営業者名**, 営業者名かな, **業種**,
  **業態**, 許可番号, 初回許可年月日, 許可開始日, **許可終了日**. Dates are wareki
  `R08.08.31` (`wareki_date` reads all 7,372). Every permit is in term on
  2026-08-31 (earliest expiry that day): the list is a current register, not a
  stream; pin `as_of` 2026-08-31 and drop nothing.
- **Register columns**: 業務種別 (理容所 / 美容所 / クリーニング所), 施設名称１,
  施設郵便番号, **施設所在地１**, 施設所在地２, 開設者申請者名, 開設者役職名,
  開設者代表者名, **開設者都道府県名称, 開設者住所１, 開設者住所２ (the
  operator's own address, filled on 59 / 288 rows)**, 開設確認番号, 開設確認日;
  the laundry file spells them 営業者申請者名 / 営業者代表者名 / 営業者住所１.
- **Against `japan_register`'s tuples (shared code, not edited here):**
  `ADDR_COLS` covers 施設所在地１, `NAME_COLS` 施設名称１, `TYPE_COLS` 業種 and
  業務種別, `OPERATOR_COLS` 営業者名 (food). **`OPERATOR_COLS` does NOT cover
  the registers' 開設者申請者名, 開設者代表者名, 営業者申請者名 or
  営業者代表者名**: add them, or the rule compares nothing there.
- **Name-rule hits, in memory**: food **25**; barbers 0, beauty 0, laundries
  **2** (with the four register columns emulated).

**Counts against the official year-end count** (衛生行政報告例 FY2024, row
香川県高松市; restaurants from `japan_official.estat()`, the registers from
第10表 / 第11表, the e-Stat files Hakodate's brief fetched,
`statInfId=000040359178` / `000040359179`):

| | Official (2025-03-31) | The city's files (2026-08) | Share |
|---|---|---|---|
| 飲食店営業 permits | **5,439** (old law 1,421, revised 4,018) | **5,558** | **102%** |
| 理容所 | 373 | 371 | 99% |
| 美容所 | 1,142 | 1,188 | 104% |
| クリーニング所 | 335 (取次所 282) | 332 | 99% |

**Through `japan_eigyo` (food list)**: 620 rows are not premises by their
address (業態 車 338, 露店：仮設 279, 露店：引車 3: `permits_from_rows`
catches every one), then out by rule 924 (manufacturing types 422, 給食 258,
旅館・ホテル 103, 露店 62, vending machines 56, 仕出し 23). **Storefronts:
Food service 4,502, Retail 1,326** (菓子 738 and そうざい 252 among the
permits). Personal services 1,891.

- ⚠️ **露店：定置 (57 rows, a stall at a fixed spot)** is out under the
  temporary rule's 露店 (owner, 2026-09-29). Fukuoka's 定置屋台 count as yatai,
  but that rule reads ろ店 / 屋台 only. Recommend the written rule (out); a
  departure would go to the owner with the Fukuoka precedent beside it.
- **MHLW's file (37201)** holds the online filings only: 56 open restaurant
  permits (1% of the official count, the scope's figure reproduced), 3,347
  notifications (届出), 2,298 of them without an address. The city list
  carries every permit, so MHLW's permits add nothing (24 of its 65 addressed
  permits match a list row on block and name exactly; spellings differ for the
  rest). ⚠️ **Recommend Matsuyama's shape**: MHLW's NOTIFICATIONS as a partial,
  opt-in food-retail bucket (651 storefront rows, disclosed), its permits
  under `SUPERSEDES`. `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=37201_food_business_all.csv`:
  887,971 B, 3,450 rows, permits to 2026-08-24.

## Coordinates — a JOIN to MLIT 位置参照情報

Takamatsu is one municipality (37201, **no wards**: `"wardless": True`, the
2026-10-01 batch's flag). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/37201-24.0a.zip` (461,083 B,
54,484 block keys), town-chōme `.../19.0b/37201-19.0b.zip` (235 keys).

| Tier | Food service (4,502) | Retail (1,326) | Barbers (371) | Beauty (1,188) | Laundries (332) |
|---|---|---|---|---|---|
| Block | **89.3%** | 79.5% | 83.6% | 83.5% | 83.4% |
| Town-chōme / 大字 centroid | 8.9% | 16.1% | 11.6% | 13.3% | 13.0% |
| Unplaced | 1.8% | 4.4% | 4.9% | 3.2% | 3.6% |

- ⚠️ **Shared rule needed (字甲)**: the unplaced are mostly 地番 addresses
  written `仏生山町甲123`, `新田町甲…`, `国分寺町福家甲…`, where MLIT keys the
  blocks under `仏生山町字甲`. Read 字甲 / 字乙 / 字丙 as 甲 / 乙 / 丙 on both
  sides in `norm_town`, measured in memory: **food 88.7% block / 11.1% /
  0.2% unplaced**; barbers 87.3 / 11.9 / 0.8; beauty 85.7 / 14.0 / 0.3;
  laundries 86.1 / 13.6 / 0.3. Re-run the Minato control and the built cities'
  screens with it.
- The chōme share is high because much of the city outside the centre has no
  住居表示: a 大字 centroid there. **No publisher coordinates** in the city's
  files: the independent check is a GSI sample at build
  (`screen_japan_join.gsi_check`'s method). MHLW's notifications carry their
  own point (median **46 m** from the block point, 91.4% within 250 m, 522
  rows).
- A handful of register rows name another municipality (坂出市 2, さぬき市 1,
  徳島 1): they stay unplaced, as they should.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_37_GML.zip` (the
shared cache), N03 code 37201 (375 km², extent W 133.920, S 34.111, E 134.176,
N 34.434; the 2005-06 mergers brought in 塩江, 牟礼, 庵治, 香川, 香南 and
国分寺). Use **N02-25** (`"n02": "25"`).

| N02 line (operator) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 琴平線 (高松琴平電気鉄道) | Kotoden Kotohira Line | **12 / 23** | 高松築港, 片原町, 瓦町, 栗林公園, 三条, 太田, 伏石, 仏生山, 空港通り, 一宮, 円座, 岡本 (11 beyond the line, to 琴電琴平) |
| 長尾線 (高松琴平電気鉄道) | Kotoden Nagao Line | **8 / 16** | 瓦町, 花園, 林道, 木太東口, 元山, 水田, 西前田, 高田 (8 beyond, in 三木町 and さぬき市) |
| 志度線 (高松琴平電気鉄道) | Kotoden Shido Line | **15 / 16** | 瓦町 … 原 (琴電志度 beyond, in さぬき市) |
| 予讃線 (四国旅客鉄道) | JR Yosan Line | 5 / 95 | 高松, 香西, 鬼無, 端岡, 国分 |
| 高徳線 (四国旅客鉄道) | JR Kōtoku Line | 9 / 29 | 高松, 昭和町, 栗林公園北口, 栗林, 木太町, 屋島, 古高松南, 八栗口, 讃岐牟礼 |
| 八栗ケーブル (四国ケーブル) | Yakuri Cable | 2 / 2 | **left out**: a sightseeing funicular (standing call); not in `excluded_stations.csv` |

- **46 stations inside the city** (N02 station groups; Kotoden 33, JR 13).
  Widest group 瓦町 (130 m, three Kotoden lines); no name falls in two groups.
  Median gap to the nearest station **703 m**: standard rings.
- **Stub test passes**: the two Kotoden lines cut at the line keep 12 of 23
  and 8 of 16; no urban line is cut to a stub.
- **Gate 3 (Kotoden), read 2026-10-02**: the operator's station-number index
  (`https://www.kotoden.co.jp/publichtm/kotoden/station/`) lists K00-K21 plus
  K04a (23, 琴平線), N02-N17 (16, 長尾線 from 瓦町) and S00-S15 (16, 志度線):
  **53 stations, exactly N02's 23 / 16 / 16**. JR Shikoku's counts at build.
- ⚠️ **長尾線 runs through to 高松築港** over 琴平線 track (片原町, 高松築港; the
  operator numbers them K00/N00 and K01/N01). N02 files the legal line from
  瓦町. Draw the public line from 高松築港 with Tokyo's `route`, or say why not.
- **Frequency**: urban lines throughout (Kotoden and JR Shikoku both run
  half-hourly or better at the centre); nothing rural to flag.
- ⚠️ **OSM `name:en`** for every station is a build-time read (one Overpass
  query, the lead's slot; not run for this brief). Read every name.

## Scope

**Takamatsu City.** Kotoden and JR run on to 綾川町, 三木町, さぬき市 and
坂出市; cut at the line, the stations beyond named by N03 municipality.

## Licences — read 2026-10-02

- **オープンデータたかまつ — PERMITTED WITH CONDITIONS (CC BY 4.0).**
  - Grant: 高松市オープンデータ利用規約 (`https://opendata.smartcity-takamatsu.jp/odp/tos/`)
    第１条, 「…クリエイティブ・コモンズ・ライセンス表示4.0国際 ライセンス…によるものとします。」;
    第７条, 「本市のデータを利用していることを表示すれば、商用・非商用を問わず自由に
    データを利用して二次著作物を作成・配布することが可能です。」 The hosting site's
    `/about/` points to these terms. CKAN `license_id: cc-by` on all four
    datasets; the GitHub repository is CC-BY-4.0.
  - The city website's 「無断で転用・引用することはできません」 (`/homepage/thissite.html`)
    covers the website's own text and images, not this data; the city's
    open-data page restates CC BY 4.0 for the data.
  - **MUST DISPLAY** (no wording prescribed; CC BY 4.0's attribution,
    modification and licence link):
    `出典：「食品等営業許可施設一覧」「理容所新規開設一覧」「美容所新規開設一覧」「クリーニング所新規開設一覧」（高松市）（https://opendata.smartcity-takamatsu.jp/odp/）を加工して作成`,
    with the CC BY 4.0 link.
  - **MUST NOT**: claim completeness or accuracy (第４条(1)); third-party
    rights are the user's (第２条). No logo or endorsement clause.
  - **Cost**: 第４条(3), the user's own cost for a breach or an infringement:
    fault-based, accepted for all of Japan.
- **MHLW open data (notifications)** — PERMITTED WITH CONDITIONS (PDL 1.0), as
  in `okayama.md`: `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; no completeness claim, no logo.
- **MLIT 位置参照情報 and N02**: PDL 1.0 (the skill's notice lines). **N03**:
  CC BY 4.0, ⛔ never drawn.

## Privacy

The food list carries **営業者名, 営業者名かな and 施設電話番号**; the registers
carry **開設者申請者名 / 営業者申請者名, 開設者代表者名 / 営業者代表者名 and the
operator's own address (開設者都道府県名称, 開設者住所１, 開設者住所２)**. Select
施設名称１, 施設所在地１, 業種 / 業務種別, 業態 and the dates; read the name
columns in memory for the name rule only; **never select an operator address
column**. Run `check_personal_exposure.py` (`japan=True`).

## Region

East Asia today, the Japan sub-region with the batch. Project to **UTM 53N
(EPSG:32653)**.

## Still open

- No 🚨 owner item: every call above follows a standing call or a built
  precedent (Matsuyama's three-bucket shape with MHLW's notifications).
- ⚠️ **Shared code** (each re-runs the Minato control and the city screens):
  `OPERATOR_COLS` + 開設者申請者名, 開設者代表者名, 営業者申請者名, 営業者代表者名;
  `norm_town` reads 字甲 / 字乙 / 字丙 as 甲 / 乙 / 丙.
- ⚠️ **Economic Census join control** (`scripts/japan_census_control.py`): the
  2021 census counts **2,071** 飲食店 establishments in 37201; the list's
  4,299 distinct placed Food-service premises (address, trade name) are
  **2.08 per establishment**, above the built cities' 1.56-1.92 (Matsuyama's
  2.78 was flagged). The list is 102% of the official permit count, so the
  ratio reads as many permits per establishment, not duplicates; check the
  業態 飲み屋 (875) and その他 (412) rows at build before reporting it.
- ⚠️ 露店：定置 (above); MHLW's notifications as partial retail; the 長尾線
  route; OSM `name:en`; line colours on both basemaps; a GSI sample.

```brief-checks
[
  {
    "id": "takamatsu-food-live",
    "claim": "Takamatsu's full food-permit list (CSV) is keyless and live on the city's open-data host",
    "kind": "http_ok",
    "url": "https://opendata.takamatsu-fact.com/licensed_food_business_facility_list/data.csv",
    "min_bytes": 1500000
  },
  {
    "id": "takamatsu-food-asof",
    "claim": "The food list's source workbook in the city's repository is the 2026-08-31 edition",
    "kind": "http_contains",
    "url": "https://api.github.com/repos/takamatsu-city/opendata/contents/data/licensed_food_business_facility_list",
    "present": ["2026.8.31"]
  },
  {
    "id": "takamatsu-barber-live",
    "claim": "Takamatsu's barber register (CSV) is keyless and live",
    "kind": "http_ok",
    "url": "https://opendata.takamatsu-fact.com/new_barber_shops/data.csv",
    "min_bytes": 40000
  },
  {
    "id": "takamatsu-beauty-live",
    "claim": "Takamatsu's beauty-salon register (CSV) is keyless and live",
    "kind": "http_ok",
    "url": "https://opendata.takamatsu-fact.com/new_beauty_salons/data.csv",
    "min_bytes": 150000
  },
  {
    "id": "takamatsu-laundry-live",
    "claim": "Takamatsu's laundry register (CSV) is keyless and live",
    "kind": "http_ok",
    "url": "https://opendata.takamatsu-fact.com/new_cleanings/data.csv",
    "min_bytes": 50000
  },
  {
    "id": "takamatsu-ckan-barber",
    "claim": "The city's CKAN catalogue lists the barber dataset with the open-data host's CSV as its resource",
    "kind": "http_contains",
    "url": "https://opendata.smartcity-takamatsu.jp/ckan/dataset/new_barber_shops",
    "present": ["opendata.takamatsu-fact.com/new_barber_shops/data.csv"]
  },
  {
    "id": "takamatsu-about-terms",
    "claim": "The open-data host's about page points to the city's open-data terms",
    "kind": "http_contains",
    "url": "https://opendata.takamatsu-fact.com/about/",
    "present": ["smartcity-takamatsu.jp/odp/tos/"]
  },
  {
    "id": "takamatsu-terms-ccby",
    "claim": "The city's open-data terms grant CC BY 4.0 (第１条) and free reuse with attribution (第７条)",
    "kind": "http_contains",
    "url": "https://opendata.smartcity-takamatsu.jp/odp/tos/",
    "present": ["表示4.0国際", "第７条"]
  },
  {
    "id": "takamatsu-mhlw-live",
    "claim": "MHLW's open-data file for Takamatsu (37201) answers a plain keyless GET - the notifications",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=37201_food_business_all.csv",
    "min_bytes": 500000
  },
  {
    "id": "takamatsu-kotoden-53",
    "claim": "Kotoden's station-number index lists K00-K21 with K04a, N02-N17 and S00-S15 (53 stations, N02's 23/16/16) - gate 3",
    "kind": "http_contains",
    "url": "https://www.kotoden.co.jp/publichtm/kotoden/station/",
    "present": ["all_stations/k04a.html", "all_stations/k21.html", "all_stations/n17.html", "all_stations/s15.html"],
    "absent": ["all_stations/k22.html", "all_stations/n18.html", "all_stations/s16.html"]
  },
  {
    "id": "takamatsu-estat-riyo-biyo",
    "claim": "e-Stat's 衛生行政報告例 FY2024 第10表 (barbers and beauty salons by core city) answers keyless - the registers' control",
    "kind": "http_ok",
    "url": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359178&fileKind=1",
    "min_bytes": 5000
  },
  {
    "id": "takamatsu-estat-cleaning",
    "claim": "e-Stat's 衛生行政報告例 FY2024 第11表 (laundries by core city) answers keyless - the registers' control",
    "kind": "http_ok",
    "url": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359179&fileKind=1",
    "min_bytes": 5000
  },
  {
    "id": "takamatsu-isj-live",
    "claim": "MLIT's block-level address file for Takamatsu (37201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/37201-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "takamatsu-projected-crs",
    "claim": "Takamatsu projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 134.05,
    "expect": "EPSG:32653"
  }
]
```
