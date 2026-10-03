# Ōtsu — build brief

> ✅ **Owner's calls (owner, 2026-10-02: "approve all recommendations"):** The food list on the city's site is **accepted as CC BY 4.0**; `mode` **`light_rail`**.


**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live; the downloads are the city's own files, MHLW's file and MLIT's ISJ
zips). **Run `python scripts/brief_check.py otsu` before writing any code.**
Then the `japan-city` skill: a Japanese city on the shared modules, Toyama's
shape (one complete city food list plus three registers; MHLW's file is not a
source). Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from a scratch script
(`scripts/screen_japan_join.py` has no Ōtsu entry; its table is shared code).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none inside the city); (2) **lines served only by limited
expresses DO count** (2026-09-28); (3) **the city line only**: only stations
inside the city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27), and an URBAN line cut to a stub
goes back to the owner; (4) **菓子製造業 and そうざい製造業 count, in Retail**,
factory share measured and kept (2026-09-24, 2026-09-27); (5) **the name
rule**: where the trade name IS the operator's own name, the pin shows its
permit type (2026-09-27); (6) **no page says "currently operating"**: the
lists keep closed premises; sightseeing funiculars are left out; fault-based
cost clauses are accepted (2026-09-24).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Ōtsu
carries `label_tier: "minor"`: dot and tooltip in every view, pill only in its
own region, in the Japan sub-region the 2026-10-02 batch creates (wave 2 only
joins it; `check_macro_labels.py` PROBLEMS 0 at 375, 768 and 1200 after it
lands).

**`mode`: `light_rail` recommended, ✅ below.** JR has 16 station groups
inside the city line against Keihan's 24, so JR is not the largest network and
the Dublin precedent applies; no subway. The backbone is Keihan's
Ishiyama-Sakamoto Line: legally a 軌道 (N02 class 21) but two-car trains on
their own right of way at about 700 m spacing.

---

## The one-line summary

**One complete city food list (4,499 permits as of 2026-08-31, 3,300
restaurants: 106% of the official in-force count of 3,115) and three standing
registers (barbers 187, beauty salons 618, laundries 202, as of 2026-08-31,
each within 2 of the official count).** All three buckets. Block join 94.7%
(food) and 96.5-97.7% (registers), nothing unplaced but one row. Rail: Keihan's
Ishiyama-Sakamoto (21 of 21) and Keishin (4 of 7) lines, JR's Kosei (12) and
Biwako (4) lines: **40 station groups inside**, the Sakamoto Cable left out.

---

## Business leg

| | Food (city site) | Barbers (BODIK) | Beauty salons (BODIK) | Laundries (BODIK) |
|---|---|---|---|---|
| **File** | `https://www.city.otsu.lg.jp/material/files/group/4/od_2608.csv` (page `https://www.city.otsu.lg.jp/soshiki/021/1441/od/02594.html`) | `https://data.bodik.jp/dataset/38908ca8-beaa-45f6-b130-8e9ae9f6d97d/resource/53520e16-5488-4d92-b9a1-a7d1365fe595/download/20260831riyo.csv` | `https://data.bodik.jp/dataset/cc0d476f-a5cc-429b-9797-8bb84c3df02f/resource/177df3f3-af8b-4619-aa54-337890a95e51/download/20260831biyo.csv` | `https://data.bodik.jp/dataset/f658266c-2854-4974-8bba-8041a80a391d/resource/8495b105-ce24-4ba7-ab6b-2431f4f60cb1/download/20260831cleaning.csv` |
| Bytes | **857,865** | **22,253** | **78,695** | **27,115** |
| Rows | **4,499** | **187** | **618** | **202** |
| As of | **2026-08-31** (「食品営業許可施設一覧（令和8年8月末時点）」; newest 許可開始年月日 2026-08-31; page updated 2026-09-17) | **2026-08-31** (「2026年8月末現在の理容所一覧」, uploaded 2026-09-09) | 2026-08-31 | 2026-08-31 |
| Cadence | monthly (the page and its catalogue record change each month; **the file name carries the month**, `od_YYMM.csv`) | monthly snapshot | monthly | monthly |
| Dataset | BODIK 252018 `食品営業許可施設一覧` (id `b4dbf726-…`, **no resource: its ソース is the city page**) | `理容所一覧` (大津市衛生課) | `美容所施設一覧` | `クリーニング所一覧` |
| Encoding | UTF-8 with BOM | UTF-8 with BOM | UTF-8 with BOM | UTF-8 with BOM |

**The scope's "food list as of 2025-08: stale" is out of date**: the city
publishes the list monthly on its own site; BODIK carries only a harvested
record of it (the dataset's activity stream: 17 metadata changes since
2025-03-13, never a resource).

**Columns.**
- Food: 許可番号, **申請者名**, **施設名**, **施設所在地**, **業種**, 許可申請年月日,
  許可開始年月日, **許可満了年月日**, 条件. Old- and new-law permits in one list
  (the dataset's notes: 改正前の第52条, 改正後の第55条); every row in term
  (許可満了年月日 from 2026-10-31).
- Registers: **施設名称**, **施設所在地**, 施設電話番号, **営業者氏名**, 確認年月日,
  確認番号. No type column: the source decides the bucket
  (`japan_eigyo.PERSONAL_SOURCES`).

**Against `japan_register`'s column tuples:** every column is already covered
(`ADDR_COLS` 施設所在地, `NAME_COLS` 施設名 / 施設名称, `TYPE_COLS` 業種,
`OPERATOR_COLS` 申請者名 / 営業者氏名). **No new spelling.** Name-rule hits in
memory: food 3, barbers 1, beauty 1, laundries 0.

**Counts that matter.**

| Bucket | Rows | Note |
|---|---|---|
| Restaurants (飲食店営業 3,298 + 喫茶店営業 2) | **3,300**; **2,659 fixed** | 641 are licensed 市内一円 (vehicles; 646 rows of all types). e-Stat 衛生行政報告例 FY2024 in force: **3,115** (106%: 17 months of growth, vehicles included) |
| Food retail | 菓子 526 · そうざい 167 · 食肉 161 · 魚介 143 = **992 fixed** | `japan_eigyo` drops manufacturing (176, "no rule") and vending (26) |
| Personal services | 187 + 618 + 202 = **1,007** | official FY2024 year end (e-Stat 第10表 / 第11表): barbers **189**, beauty **611**, laundries **203** |
| By start year (restaurants) | 2018 4 · 2019 55 · 2020 243 · 2021 490 · 2022 557 · 2023 518 · 2024 518 · 2025 541 · 2026 372 | a standing list, not a stream |

**MHLW's file is not a source.** `…param=25201_food_business_all.csv`
(327,374 B, 936 rows, as of 2026-08 end) holds 838 notifications and only 67
open restaurant permits (opt-in). The city's list is complete, so on Toyama's
precedent MHLW's notifications are left out and the page's standing bullet
covers them.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 25201)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/25201-24.0a.zip` (269,081 B) and
`…/19.0b/25201-19.0b.zip` (13,069 B): 15,716 block keys, 509 town-chōme.
Ōtsu has no wards: `"wardless": True`.

| Tier | Food, in a bucket, fixed (3,651) | Barbers (187) | Beauty (618) | Laundries (202) |
|---|---|---|---|---|
| Block | **94.7%** | **96.8%** | **97.7%** | **96.5%** |
| Town-chōme / 大字 centroid | 5.3% | 3.2% | 2.3% | 3.5% |
| Unplaced | 0.0% (1 row) | 0.0% | 0.0% | 0.0% |

**No publisher coordinates** in any city file: the independent check is
GSI's address search on a sample at build (`screen_japan_join.gsi_check`'s
method, as Hakodate). MHLW's 322 points for its own rows sit a median 39 m
from the block point (295 rows), which says the block file is sound here.

---

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (25201)

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_25_GML.zip` (the
shared cache), with `stub_test()`'s method. N03 extent W 135.8148, S 34.8713,
E 136.0431, N 35.2847 (the city runs 46 km up the lake's west shore).

| N02 line (operator, class) | Public name | Inside / N02 total | Note |
|---|---|---|---|
| 石山坂本線 (京阪電気鉄道, 21) | Keihan Ishiyama-Sakamoto Line | **21 / 21** | Operator: OT01 石山寺 to OT21 坂本比叡山口, **21 (gate 3 exact)** |
| 京津線 (京阪電気鉄道, 21) | Keihan Keishin Line | **4 / 7** (追分, 大谷, 上栄町, びわ湖浜大津) | cut at the line; Kyoto draws its other 3. Operator lists 6 Keihan stations (OT31-35 and OT12; 御陵 is the subway's) |
| 湖西線 (JR西日本, 11) | JR Kosei Line | **12 / 21** (大津京 to 近江舞子, 北小松) | cut at the line |
| 東海道線 (JR西日本, 11) | JR Biwako Line (琵琶湖線) | **4 / 59** (大津, 膳所, 石山, 瀬田) | cut at the line; name it by its public name, not N02's legal one (trap 2) |
| 比叡山鉄道線 (比叡山鉄道, 13) | Sakamoto Cable | 4 / 4 | **left out**: a sightseeing funicular (standing call); not in `excluded_stations.csv`; a bullet under **The lines** |

- **40 station groups inside** (44 with the funicular; びわ湖浜大津 is one group
  over both Keihan lines; 大津京 and 京阪大津京 stay two groups, as N02 keeps
  them). Per operator: Keihan 24, JR 16.
- **Stub test**: no line is cut to one station; the Keishin Line keeps 4 of 7.
  Passes.
- **Median nearest-group gap 577 m** (funicular out; min 54 m, max 3,254 m):
  **standard rings** (0.1 / 0.2 / 0.3 / 0.6 mi), but only 7 m above the
  540-570 m band that goes to the owner. ⚠️ Recompute on the stations drawn.
- ⚠️ **Gate 3 for JR West** per line at build; Keihan's is exact above.
- ⚠️ **OSM `name:en`** for every station is a build-time read (one Overpass
  query, the session's single slot; not run for this brief). The Keihan stops
  are railway=station in OSM by general knowledge; if any is a tram_stop,
  `TRAM_OSM_JSON` as Toyama's.

## Scope

**Ōtsu City (25201), one municipality.** JR runs on to Kusatsu and Takashima,
Keihan to Kyoto (Yamashina); cut at the line.

## Licences — read 2026-10-02

- **The three registers on BODIK — PERMITTED WITH CONDITIONS (CC BY 4.0).**
  Each dataset records `license_id: cc-by`; the catalogue's terms
  (`https://odcs.bodik.jp/252018/tos/`, 大津市オープンデータ利用規約 ４(1)) grant
  「クリエイティブ・コモンズ・ライセンス表示4.0国際」 for data downloaded from the
  portal (２．適用範囲), commercial use not barred (１).
  - **MUST DISPLAY** (４(2), for edited content):
    `この地図は以下の著作物を改変して利用しています。理容所一覧、大津市、クリエイティブ・コモンズ・ライセンス 表示 4.0 国際（https://creativecommons.org/licenses/by/4.0/）`,
    and likewise `美容所施設一覧` and `クリーニング所一覧`.
  - **MUST NOT**: use the city's logos alone without asking (５).
  - **Cost** (６, ８): claims from our own breach at our own cost; the
    fault-based class, accepted for all of Japan (2026-09-24). Japanese law,
    大津地方裁判所 (９).
- **The food list on the city's site — ✅ PERMITTED WITH CONDITIONS (CC BY
  4.0) on a reading the owner should confirm.** The city's copyright page
  (`https://www.city.otsu.lg.jp/shisei/koho/hp/5184.html`) reserves the site
  「法律で認められている場合を除き、無断で複製、転用することはできません」, then
  「ただし、大津市オープンデータポータルサイトについてはこの限りではありません」,
  linking the portal (BODIK 252018) and the terms above. The food list is
  catalogued on that portal under `license_id: cc-by`, but as a record whose
  only content is its ソース, the city page under 「衛生課 オープンデータ」; the
  file itself is served from the city's site, and the terms' ２ applies them to
  data 「当サイトよりダウンロードした」. The credit would be the registers' form
  with the title `食品営業許可施設一覧`.
- **MLIT 位置参照情報 and N02**: PDL 1.0 (copy the skill's notice lines).
- **MLIT N03**: CC BY 4.0, ⛔ never drawn.
- MHLW: not used.

## Privacy

The food list carries **申請者名** (operator, often an individual); the
registers **営業者氏名** and **施設電話番号**. Select 施設名 / 施設名称, 施設所在地,
業種 and the dates; read 申請者名 and 営業者氏名 in memory for the name rule only;
never select 施設電話番号. Run `check_personal_exposure.py` (`japan=True`). No
row value was printed for this brief.

## Region

The Japan sub-region (minor tier, above); `"country": "Japan"`. Project to
**UTM 53N (EPSG:32653)**.

## Open items

- ✅ **The food list's licence.** Recommendation: **accept it as CC BY 4.0**
  on the catalogue record, which licenses the dataset and names the city page
  as its source; the city publishes the page under 「衛生課 オープンデータ」 beside
  the three registers it also uploads to BODIK, and its copyright page exempts
  the portal it catalogues them in. The alternative is the registers alone
  (Band B, personal services only, Yokohama's precedent) until the city
  uploads the file to BODIK. Outreach is the last resort and not recommended.
- ✅ **`mode`.** Recommendation: **`light_rail`** (Utsunomiya's), by the
  backbone: Keihan's Ishiyama-Sakamoto Line runs two-car trains on its own
  right of way at about 700 m spacing, with street running only near
  びわ湖浜大津 (Keishin). The alternative is `tram`, on its 軌道 legal class
  (N02 class 21) and Matsuyama's precedent. Not settled by the standing rule,
  which names only when JR or a subway makes it `metro`.
- ⚠️ **The file name changes monthly** (`od_2608.csv`): the fetch reads the
  page's current link (Kyoto's `portal_file` shape, magic bytes checked) and
  records the as-of; `as_of` is the list's own month end, never today.
- ⚠️ **Shared code**: none for columns. `japan.CITIES` gains
  `"otsu": {"name": "大津市", "pref": "25", "epsg": 32653, "n02": "25",
  "wardless": True, "wards": ["25201"]}` (the ward-less flag on master).
- ⚠️ **Economic Census join control** (`scripts/japan_census_control.py`): the
  2021 census counts **1,021** 飲食店 establishments in 25201; 2,659 fixed Food
  service permits is **about 2.6 per establishment**, above the built cities'
  1.56-1.92 (Matsuyama's 2.78 was flagged, Toyama's 2.4 before
  de-duplication). Run it on the built pins; one pin per premises first.
- ⚠️ The 577 m spacing (above), gate 3 for JR West, OSM `name:en`, line
  colours on both basemaps; the 菓子 / そうざい factory share printed by step 2.
- **Recommended band: A** (three buckets, 40 stations), if the food licence
  reading is accepted.

```brief-checks
[
  {
    "id": "otsu-food-live",
    "claim": "Ōtsu's food-permit list as of 2026-08-31 (od_2608.csv) is keyless and live on the city's site",
    "kind": "http_ok",
    "url": "https://www.city.otsu.lg.jp/material/files/group/4/od_2608.csv",
    "min_bytes": 700000
  },
  {
    "id": "otsu-food-page-links-file",
    "claim": "The city's 衛生課 open-data page links the 2026-08 food file (ASCII marker: the server sends no charset)",
    "kind": "http_contains",
    "url": "https://www.city.otsu.lg.jp/soshiki/021/1441/od/02594.html",
    "present": ["od_2608.csv"]
  },
  {
    "id": "otsu-food-catalogue-record",
    "claim": "BODIK's food dataset is licensed cc-by, has no resource, and names the city page as its source",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=b4dbf726-afc9-4d86-8cdb-5df54c077471",
    "present": ["\"license_id\": \"cc-by\"", "\"num_resources\": 0", "soshiki/021/1441/od/02594.html"]
  },
  {
    "id": "otsu-copyright-exempts-portal",
    "claim": "The city's copyright page points to the open-data portal and its terms as the exception (ASCII markers)",
    "kind": "http_contains",
    "url": "https://www.city.otsu.lg.jp/shisei/koho/hp/5184.html",
    "present": ["data.bodik.jp/organization/252018", "odcs.bodik.jp/252018/tos"]
  },
  {
    "id": "otsu-terms-cc-by-4",
    "claim": "Ōtsu's catalogue terms grant CC BY 4.0 International",
    "kind": "http_contains",
    "url": "https://odcs.bodik.jp/252018/tos/",
    "present": ["表示4.0国際", "当サイトよりダウンロードしたデータに対して適用されます"]
  },
  {
    "id": "otsu-barber-live",
    "claim": "The barber register of 2026-08-31 is live on BODIK",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/38908ca8-beaa-45f6-b130-8e9ae9f6d97d/resource/53520e16-5488-4d92-b9a1-a7d1365fe595/download/20260831riyo.csv",
    "min_bytes": 15000
  },
  {
    "id": "otsu-barber-rows",
    "claim": "The barber register of 2026-08-31 holds 187 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "53520e16-5488-4d92-b9a1-a7d1365fe595",
    "expect": 187
  },
  {
    "id": "otsu-beauty-rows",
    "claim": "The beauty-salon register of 2026-08-31 holds 618 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "177df3f3-af8b-4619-aa54-337890a95e51",
    "expect": 618
  },
  {
    "id": "otsu-laundry-rows",
    "claim": "The laundry register of 2026-08-31 holds 202 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "8495b105-ce24-4ba7-ab6b-2431f4f60cb1",
    "expect": 202
  },
  {
    "id": "otsu-keihan-ishiyama-sakamoto",
    "claim": "Keihan's station index lists the Ishiyama-Sakamoto Line from 石山寺 to 坂本比叡山口 (gate 3: 21 stations)",
    "kind": "http_contains",
    "url": "https://www.keihan.co.jp/traffic/station/",
    "present": ["石山坂本線", "石山寺", "坂本比叡山口", "京津線", "上栄町"]
  },
  {
    "id": "otsu-isj-live",
    "claim": "MLIT's block-level address file for Ōtsu (25201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/25201-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "otsu-projected-crs",
    "claim": "Ōtsu projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.87,
    "expect": "EPSG:32653"
  }
]
```
