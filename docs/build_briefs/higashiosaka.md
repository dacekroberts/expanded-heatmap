# Higashiōsaka — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live; the downloads are the city's BODIK files, MHLW's file and MLIT's ISJ
zips). **Run `python scripts/brief_check.py higashiosaka` before writing any
code.** Then the `japan-city` skill. **Band B, food only** (Hiroshima's and
Sakai's page: "**This map shows food businesses only.**"): the city publishes
no barber, beauty or laundry list. Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py` from a scratch script
(`scripts/screen_japan_join.py` has no Higashiōsaka entry; its table is shared
code).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27), and an URBAN line cut to a stub goes back to
the owner; (4) **菓子製造業 and そうざい製造業 count, in Retail**, factory share
measured and kept (2026-09-24, 2026-09-27); (5) **the name rule** where an
operator column exists: this list has none (法人名 only), so **Okayama's call
applies (owner, 2026-10-02): the whole page without the rule, Hiroshima's
MHLW-style bullet**; (6) **no page says "currently operating"**; fault-based
cost clauses are accepted (2026-09-24).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).**
Higashiōsaka carries `label_tier: "minor"`, in the Japan sub-region the
2026-10-02 batch creates. It borders built Osaka: its dot sits about 10 km
east of Osaka's, so `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200)
decides, never the eye.

**`mode`: `metro`.** Osaka Metro's Chūō Line is drawn (the owner's rule: a
subway drawn makes it `metro`).

---

## The one-line summary

**Food from the city's own national-schema list on BODIK: every permit in
force on 2026-04-01 (6,521 rows, old- and new-law), plus each month's new
permits to 2026-08-31 (546 rows), rebuilt to 6,521 in term on 2026-08-31;
5,505 restaurant permits against the official 5,534 (99.5%).** 5,086 fixed
Food service premises and 691 food shops, **99.6% at the block**, nothing
unplaced. The list's own coordinates are in the **old Tokyo Datum** (median
448 m off; 37 m once shifted). No personal-services list exists. Rail:
Kintetsu (18), JR (7) and Osaka Metro (2): **26 station groups inside**.

---

## Business leg — the city's BODIK dataset `272272_15` (食品等営業許可一覧)

| | Full list (全許可) | New permits, monthly (新規許可) | MHLW (27227), not used |
|---|---|---|---|
| **File** | `https://data.bodik.jp/dataset/b5eeed4c-cec0-4eef-8513-b4882d6a18ec/resource/a0416f70-bda0-46fe-a684-b22a95135c32/download/272272_food_business_all_20260401.csv` | `…/resource/981be3b9-1f13-457f-b62e-7a6fb5be92cd/download/272272_food_business_new_20260401_20260430.csv`, and `881ae94f-…` (05), `efb9b81f-…` (06), `99f4b033-…` (07), `10698d75-c301-4c25-84e4-55fc4cf39aa6/download/272272_food_business_new_20260801_20260831.csv` (08) | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27227_food_business_all.csv` |
| Bytes | **1,741,808** | 36,760 · 30,883 · 27,354 · 30,944 · 19,349 | 426,205 |
| Rows | **6,521** | 139 · 116 · 103 · 115 · 73 = **546** | 1,333 (届出 1,331, 届出(廃業) 2): **no permits** |
| As of | **2026-04-01** (「（全許可）（令和8年4月1日現在）」; uploaded 2026-07-16) | through **2026-08-31** (August's uploaded 2026-09-23) | 2026-08 end |
| Cadence | yearly (one 全許可 resource, replaced) | monthly, about three weeks after the month | monthly |
| Encoding | UTF-8 CSV, BOM | as the full list | UTF-8 CSV, BOM |

The dataset also carries each list as PDF, and February and March 2026's new
permits (before the full list's date: not needed). Licence `cc-by-40-intl`,
maintainer 健康部食品衛生課.

**Columns** (the Digital Agency's 食品等営業許可 standard schema, all files):
全国地方公共団体コード, ID, 地方公共団体名, **施設名称**, 施設名称_カナ, 施設名称_英字,
**営業の種類**, 業態 (empty), 所在地_全国地方公共団体コード, 町字ID (empty),
**所在地_連結表記**, 施設所在地_都道府県 / _市区町村 / _町字 / _番地以下, 施設方書,
**緯度, 経度**, 施設電話番号, 連絡先メールアドレス, 連絡先FormURL, 連絡先備考_その他SNSなど,
郵便番号, 法人名, 法人番号, 許可番号, 初回許可年月日, 許可年月日, 許可開始日,
**許可満了日**, 廃業年月日 (empty), 申請区分 (empty), 許可条件, 備考.

**Against `japan_register`'s column tuples:** covered (`ADDR_COLS`
所在地_連結表記, `NAME_COLS` 施設名称, `TYPE_COLS` 営業の種類). **No operator
column**: 法人名 is a company's, so `OPERATOR_COLS` has nothing to compare (0
hits). The types carry the old law in their own spelling, **（旧）飲食店営業**
(1,080), and the form in brackets, 飲食店営業（露店） (272), 飲食店営業（自動車）
(139): `japan_eigyo` reads all three as they are (restaurant; temporary /
mobile out).

**The register, rebuilt** (Kyoto's method, `config.source_rows`): the full
list, then each month oldest first; where (address, trade name, type without
（旧）) repeats, the permit ending latest wins; kept while 許可満了日 is on or
after the pinned `as_of` (2026-08-31, never today). **7,067 rows read, 6,709
after de-duplication, 6,521 in term.** Closures after 2026-04-01 are
invisible (廃業年月日 is empty in every file), so it is an upper bound for five
months; the page says so (Kyoto's wording).

**Counts that matter** (rebuilt, in term on 2026-08-31).

| Bucket | Rows | Note |
|---|---|---|
| Restaurant permits (飲食店営業, （旧）, 喫茶店) | **5,505** | e-Stat 衛生行政報告例 FY2024 in force **5,534**: **99.5%** |
| Food service, fixed | **5,086** | out: stalls and vehicles 419 |
| Food retail | **691**: 菓子 342 · 食肉 161 · 魚介 104 · そうざい 84 | out: manufacturing 273 ("no rule"), vending 52 |
| Personal services | **none** | below |

- **MHLW's file holds notifications only** (the city files its permits in
  its own system): 662 of 1,331 carry an address. The city's list is complete,
  so on Toyama's precedent they are left out and the page's standing bullet
  covers them.
- **What is missing: personal services.** Enumerated the city's own
  環境衛生 pages (`/category/19-5-2-0-…`: 届出 procedures for barbers, salons
  and laundries, no list of premises) and BODIK org 272272 (27 datasets, one
  food; a search for 理容, 美容 and クリーニング finds none).

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 27227)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27227-24.0a.zip` (178,806 B) and
`…/19.0b/27227-19.0b.zip` (12,288 B): 7,045 block keys, 500 town-chōme. No
wards: `"wardless": True`.

| Tier | Rebuilt list, in a bucket, fixed (5,777) |
|---|---|
| Block | **99.6%** |
| Town-chōme / 大字 centroid | 0.4% (21) |
| Unplaced | 0.0% |

**Independent check — and a trap.** The list's own 緯度 / 経度 sit a **median
448 m** from the block point, **0.0% within 250 m and none over 1 km**: one
consistent offset (median Δlat −0.00324°, Δlon +0.00287°). Shifted from the
Tokyo Datum (EPSG:4301) to JGD2000 (EPSG:4612) with pyproj, the same 6,069
rows sit a **median 37 m** away, **99.5% within 250 m**. **The city's points
are in the old Tokyo Datum.** 431 rows carry a zero point. ⚠️ So
**`OWN_POINT_FALLBACK` stays off** (21 chōme rows do not need it); a build
that wants the points must shift them first, with a check that fails on an
unshifted file.

---

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (27227)

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_27_GML.zip`. N03
extent W 135.5570, S 34.6322, E 135.6787, N 34.7044. No Shinkansen.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 奈良線 (近畿日本鉄道, 12) | Kintetsu Nara Line | **11 / 19** | 布施, 河内永和, 河内小阪, 八戸ノ里, 若江岩田, 河内花園, 東花園, 瓢箪山, 枚岡, 額田, 石切 |
| 大阪線 (近畿日本鉄道, 12) | Kintetsu Osaka Line | **4 / 49** | 布施, 俊徳道, 長瀬, 弥刀 |
| けいはんな線 (近畿日本鉄道, 21) | Kintetsu Keihanna Line | **4 / 4** (N02's class-21 section, 長田 to 生駒's edge) | 長田, 荒本, 吉田, 新石切 |
| 4号線(中央線) (大阪市高速電気軌道, 21) | Osaka Metro Chūō Line | **2 / 12** | 高井田, 長田 |
| おおさか東線 (JR西日本, 11) | JR Osaka Higashi Line | **5 / 14** | 高井田中央, JR河内永和, JR俊徳道, JR長瀬, 衣摺加美北 |
| 片町線 (JR西日本, 11) | JR Gakkentoshi Line (学研都市線) | **2 / 24** | 鴻池新田, 徳庵 |

- **26 station groups inside** (Kintetsu 18, JR 7, Metro 2; 長田 and 布施 are
  each one group over two lines). Median nearest-group gap **767 m** (min
  39 m): **standard rings**.
- **Stub test**: no line is cut to one station. **The Chūō Line, an URBAN
  subway, keeps 2 of 12** (🚨 below; Sakai's Midōsuji kept 3 and was drawn
  cut). The Gakkentoshi Line keeps 2 of 24.
- ⚠️ **The Keihanna Line runs through onto the Chūō Line at 長田**; N02 files
  it in two legal sections (the class-21 part here). Draw each under its
  public name (trap 2), the Keihanna Line from 長田 to the city line.
- ⚠️ **Names**: 片町線 is the Gakkentoshi Line, 4号線(中央線) the Chūō Line.
- ⚠️ **Gate 3** against Kintetsu's, JR West's and Osaka Metro's station lists
  at build; **OSM `name:en`** a build-time read (no Overpass for this brief).

## Scope

**Higashiōsaka City (27227), one municipality.** Every line runs on into
Osaka City (built), Yao, Daitō or Ikoma; cut at the line. Osaka's own map
cuts the same lines at its side of the boundary, so the two maps meet there.

## Licences — read 2026-10-02

- **The city's BODIK dataset — PERMITTED WITH CONDITIONS (CC BY 4.0).** The
  dataset records `license_id: cc-by-40-intl`; the catalogue's terms
  (`https://odcs.bodik.jp/272272/tos/`, 東大阪市オープンデータ利用規約 ２) grant
  「クリエイティブ・コモンズ・ライセンス 表示4.0 国際」 unless a dataset sets its own.
  - **MUST DISPLAY** (２, for edited works):
    `この地図は以下の著作物を改変して利用しています。食品等営業許可一覧、東大阪市、クリエイティブ・コモンズ・ライセンス 表示 4.0（https://creativecommons.org/licenses/by/4.0/deed.ja）`.
  - **Cost** (３(4), ４): claims from our own breach at our own cost; the
    fault-based class, accepted for all of Japan (2026-09-24). Japanese law,
    大阪地方裁判所 (６).
- **MLIT 位置参照情報 and N02**: PDL 1.0. **MLIT N03**: CC BY 4.0, ⛔ never drawn.
- MHLW: not used.

## Privacy

The list carries **施設電話番号, 連絡先メールアドレス, 連絡先FormURL, 連絡先備考,
法人名 and 法人番号**: never select them. Select 施設名称, 営業の種類,
所在地_連結表記 and the dates. No individual operator's name is published, so
the name rule has nothing to compare (Okayama's call). Run
`check_personal_exposure.py` (`japan=True`). No row value was printed for this
brief.

## Region

The Japan sub-region (minor tier, above); `"country": "Japan"`. Project to
**UTM 53N (EPSG:32653)**.

## Open items

- 🚨 **The Chūō Line cut to 2 stations** (高井田, 長田). Recommendation: **draw
  it as cut**, on Sakai's precedent (the Midōsuji Line, 3 stations, drawn cut;
  owner, 2026-10-02): both stations are real interchanges (長田 with the
  Keihanna Line, 高井田 beside JR's 高井田中央), and the line goes on into
  built Osaka. Leaving it out would also take the city's `metro` mode with it.
- ⚠️ **The Tokyo Datum** (above): no own-point fallback; record it in the
  config's comment and the drafts file.
- ⚠️ **The rebuilt register** (`config.source_rows`: the full list plus its
  months, Kyoto's shape; Tokyo's per-ward files fit it too) and its upper-bound
  wording; pin `as_of` to the newest month's end. A new 全許可 (each April)
  replaces the base.
- ⚠️ **Shared code**: none for columns. `japan.CITIES` gains
  `"higashiosaka": {"name": "東大阪市", "pref": "27", "epsg": 32653, "n02": "25",
  "wardless": True, "wards": ["27227"]}`.
- ⚠️ **Economic Census join control** (`scripts/japan_census_control.py`): the
  2021 census counts **1,910** 飲食店 establishments in 27227; 5,086 fixed Food
  service rows is **about 2.7 per establishment**, above the built cities'
  1.56-1.92 (Matsuyama's 2.78 was flagged). One pin per premises first
  (5,662 distinct town, block, name and bucket), then read it.
- ⚠️ The macro label beside Osaka's; gate 3; OSM `name:en`; line colours on
  both basemaps (Osaka's palette for the shared lines); the 菓子 / そうざい
  factory share printed by step 2.

```brief-checks
[
  {
    "id": "higashiosaka-full-list-live",
    "claim": "The city's full food-permit list (in force 2026-04-01) is keyless and live on BODIK",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/b5eeed4c-cec0-4eef-8513-b4882d6a18ec/resource/a0416f70-bda0-46fe-a684-b22a95135c32/download/272272_food_business_all_20260401.csv",
    "min_bytes": 1200000
  },
  {
    "id": "higashiosaka-full-list-rows",
    "claim": "The full list of 2026-04-01 holds 6,521 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "a0416f70-bda0-46fe-a684-b22a95135c32",
    "expect": 6521
  },
  {
    "id": "higashiosaka-august-new-permits",
    "claim": "August 2026's new-permit list (the newest month) is live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/b5eeed4c-cec0-4eef-8513-b4882d6a18ec/resource/10698d75-c301-4c25-84e4-55fc4cf39aa6/download/272272_food_business_new_20260801_20260831.csv",
    "min_bytes": 10000
  },
  {
    "id": "higashiosaka-august-rows",
    "claim": "August 2026's new-permit list holds 73 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "10698d75-c301-4c25-84e4-55fc4cf39aa6",
    "expect": 73
  },
  {
    "id": "higashiosaka-dataset-record",
    "claim": "The dataset is CC BY 4.0 and lists the 2026-04-01 full list and the 2026-04 to 2026-08 months",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=b5eeed4c-cec0-4eef-8513-b4882d6a18ec",
    "present": ["\"license_id\": \"cc-by-40-intl\"", "272272_food_business_all_20260401.csv", "272272_food_business_new_20260401_20260430.csv", "272272_food_business_new_20260801_20260831.csv"]
  },
  {
    "id": "higashiosaka-terms-cc-by-4",
    "claim": "Higashiōsaka's catalogue terms grant CC BY 4.0",
    "kind": "http_contains",
    "url": "https://odcs.bodik.jp/272272/tos/",
    "present": ["表示4.0 国際", "creativecommons.org/licenses/by/4.0/legalcode.ja"]
  },
  {
    "id": "higashiosaka-no-barber-list",
    "claim": "BODIK org 272272 has no barber (理容) dataset",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=organization:272272&q=%E7%90%86%E5%AE%B9&rows=0",
    "present": ["\"count\": 0"]
  },
  {
    "id": "higashiosaka-no-beauty-list",
    "claim": "BODIK org 272272 has no beauty-salon (美容) dataset",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=organization:272272&q=%E7%BE%8E%E5%AE%B9&rows=0",
    "present": ["\"count\": 0"]
  },
  {
    "id": "higashiosaka-no-laundry-list",
    "claim": "BODIK org 272272 has no laundry (クリーニング) dataset",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=organization:272272&q=%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0&rows=0",
    "present": ["\"count\": 0"]
  },
  {
    "id": "higashiosaka-mhlw-live",
    "claim": "MHLW's open-data file for Higashiōsaka (27227) answers keyless (notifications only; not a source)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27227_food_business_all.csv",
    "min_bytes": 200000
  },
  {
    "id": "higashiosaka-isj-live",
    "claim": "MLIT's block-level address file for Higashiōsaka (27227) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27227-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "higashiosaka-projected-crs",
    "claim": "Higashiōsaka projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.60,
    "expect": "EPSG:32653"
  }
]
```
