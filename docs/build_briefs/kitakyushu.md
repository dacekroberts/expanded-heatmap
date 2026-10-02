# Kitakyushu — build brief

**Step 0 measured 2026-10-02** (the 2026-10-01 screen's figures re-verified
live; the downloads are the master list's named sources, MHLW's file and MLIT's
ISJ zips). **Run `python scripts/brief_check.py kitakyushu` before writing any
code.** Then the `japan-city` skill: this is a Japanese city on the shared
modules, Fukuoka's two-source shape (MHLW's filings plus the city's own BODIK
list) with personal services added. Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py` from a scratch script
(`scripts/screen_japan_join.py` has no Kitakyushu entry; its table is shared
code).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24); (2) **lines served only by limited expresses DO count**
(2026-09-28); (3) **the city line only**: only stations inside the city get
rings, JR and the private lines are cut at the line, **a one-station stub
stays as cut** (2026-09-27), and an URBAN line cut to a stub goes back to the
owner; (4) **菓子製造業 and そうざい製造業 count, in Retail**, factory share
measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**: where the
trade name IS the operator's own name, the pin shows its permit type
(2026-09-27); (6) **no page says "currently operating"**: the lists keep
closed premises; sightseeing funiculars are left out; fault-based cost clauses
are accepted (2026-09-24).

**✅ Minor label tier (owner, 2026-10-02).** Kitakyushu carries
`label_tier: "minor"`: dot and tooltip in every view, pill only in its own
region. Per the `japan-city` skill: a Japan sub-region (one or split, by
`check_macro_labels.py`, PROBLEMS 0 at 375, 768 and 1200), every Japanese city
moved into it, `REGION_LABELS_ALSO["East Asia"]` gaining it. **The eight built
Japanese cities stay eligible.** If Kitakyushu is the batch's first city to
build, that change lands with its `app/` diff at review time.

---

## The one-line summary

**Food from TWO lists split by permit law: MHLW's 食品衛生申請等システム file
(every permit since 2021-06; 10,760 open restaurant permits, 86.2% with a
published address) and the city's own BODIK list of pre-2021-law permits still
in term (1,582 restaurants at 2026-08-31). Together about 12,270 restaurants,
96% of the official in-force count (12,733).** Personal services from the
city's BODIK barber (817) and beauty (2,282) registers. Block-level join 98.6%
(MHLW) / 98.8% (own list) / 99.0-99.8% (registers). **No laundry list**:
disclosed, Berlin's gap. 53 stations inside the city (N02-25).

---

## Business leg

| | MHLW open data (40100) | City's old-law list (BODIK) | Barbers (BODIK) | Beauty salons (BODIK) |
|---|---|---|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=40100_food_business_all.csv` | `https://data.bodik.jp/dataset/822fb681-346a-444e-b482-33c67b50cac3/resource/afce5cb5-8582-4295-8a98-494db2e25466/download/401005_shokuhineiseihotokyokashisetsuichiran_20260331.xlsx` | `https://data.bodik.jp/dataset/8be510bd-5f67-4570-a250-b34ffdac8d37/resource/c0503e76-86d9-4f14-a052-f17ac06951d0/download/401005_riyosyoichiran_20260831.csv` | `https://data.bodik.jp/dataset/c8266fc8-5d1f-4d3b-93aa-44486f5187ea/resource/e958d9fd-6e3d-47bf-b557-96af0c3a44ca/download/401005_biyosyoichiran_20260831.csv` |
| Bytes | **7,159,229** | **288,167** | **49,563** | **161,313** |
| Rows | **19,754** (許可 13,170 · 届出 6,519 · 許可(廃業) 61 · 届出(廃業) 4) | **3,383** (one sheet, header on row 1) | **817** | **2,282** |
| As of | **2026-08 end** (the viewer's 「2026年08月末現在」) | **2026-03-31** (sheet title 「2026(令和8)年3月末時点」; uploaded 2026-08-14) | **2026-08-31** | **2026-08-31** |
| Cadence | monthly (MHLW) | yearly; holds only permits issued under the pre-2021 law, so it shrinks as they expire | monthly snapshot, a new resource each month (uploaded 2026-09-25) | monthly, as barbers |
| Dataset | i2fas オープンデータ閲覧 | `401005_shokuhineiseihotokyokashisetsuichiran` (保健福祉局 保健衛生課) | `401005_riyosyoichian` (保健福祉局 東部・西部生活衛生課; the id's spelling) | `401005_biyosyoichiran` (same) |
| Encoding | UTF-8 CSV | XLSX | cp932 CSV | cp932 CSV |

**Columns.**
- MHLW (the national schema, as Fukuoka's and Hiroshima's): 自治体コード, 行番号,
  都道府県名, 市区町村名, **営業施設名称、屋号又は商号**, フリガナ, **営業の種類**, **業態**,
  **営業施設所在地**, 営業施設方書, **緯度 / 経度**, 営業施設電話番号, 法人名, 法人番号,
  法人住所, 許可番号, 初回許可年月日, 許可年月日, 許可開始日, 許可満了日, 廃業年月日,
  **申請区分**, 許可条件, 備考. No individual operator's name column (法人名 is a
  company's), so **the name rule cannot run on MHLW rows** (Fukuoka's
  precedent, accepted).
- Old-law list: **屋号名称**, **営業所所在地**, 営業者氏名, 代表者肩書, 代表者氏名,
  **営業の種類**, 営業許可の番号, 営業許可年月日, 許可開始日, **許可終了日**.
- Barbers / beauty: **施設所在地**, **施設名称**, 営業者氏名, 肩書, 代表者氏名,
  **業種**, 許可（確認）年月日 (a line break inside the header cell).

**Against `japan_register`'s column tuples (shared code, not edited here):**
- `OPERATOR_COLS` covers **営業者氏名** (all three city files). It does NOT cover
  **代表者氏名** (all three): add it, or a representative named as the trade
  name passes the rule. Re-run the Minato control after.
- `NAME_COLS` does NOT cover the old-law list's **屋号名称**: without it step 2
  reads no trade name for 3,383 rows. Add it.
- Name-rule hits measured in memory: old-law list 2, barbers 0, beauty 0.

**Counts that matter.**

| Bucket | MHLW (open permits) | Old-law list | Note |
|---|---|---|---|
| Restaurants (飲食店営業) | **10,760**, of which **9,276 (86.2%)** carry an address | **2,183** in the list; **1,582** still in term on 2026-08-31 (1,348 on 2026-10-02) | 71 of the 1,582 share a block and trade name with an MHLW restaurant permit |
| Restaurants by first-permit year (MHLW) | 2021 1,271 · 2022 2,017 · 2023 1,855 · 2024 2,026 · 2025 2,110 · 2026 1,481 | | the city enters every new permit, not only online filings |
| 菓子 / そうざい / 食肉販売 / 魚介類販売 (open) | 951 / 320 / 273 / 314 | 191 / 65 / 221 / 194 (with 乳類販売 211) | |
| After `japan_eigyo`, fixed with an address | Food service **6,637**, Retail **1,999** (permits only); Retail 4,185 with MHLW's notifications | Food service 2,136, Retail 882 | before the old list's expired rows are dropped |
| 理容 / 美容 / クリーニング | | | **817 / 2,282 / none** |

- **Official count**: e-Stat 衛生行政報告例 FY2024, 飲食店営業 in force **12,733**
  (`japan_official.estat()`). MHLW plus the old list in term, less the overlap:
  about **12,270, 96%**. Placeable (an address published): about **10,790,
  88%** of that.
- **MHLW's 業態** carries the forms `FORM_RULES` reads: 自動車営業 819, 仮設 303 +
  仮設営業 289, スナック 582 among restaurant permits. After the taxonomy, of the
  10,760: Food service 7,678, Retail 409 (konbini and supermarket forms), out
  2,673.
- **Old-law list: drop rows past 許可終了日** (the list is as of 2026-03-31;
  1,373 of 3,383 end before 2026-10-02; renewals move to MHLW). Pin `as_of`
  at MHLW's date, never today (Kyoto's rule). The list excludes stalls,
  vehicles and vending machines by its own notes. Its 食品販売業 (242, the
  prefecture's ordinance permit) takes no rule and stays out.
- **MHLW's notifications (届出)** as a partial food-retail bucket, disclosed:
  Fukuoka's and Hiroshima's precedent.

**What is missing**: a laundry list (none among BODIK org 401005's 720
datasets, none on the division pages): personal services without laundries,
disclosed (Berlin's gap). About 14% of MHLW's restaurant permits withhold their
address (MHLW publishes an address only by consent; the page wording is the
skill's MHLW bullet).

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files for the **7 wards** (40101 門司, 40103 若松, 40105 戸畑, 40106 小倉北,
40107 小倉南, 40108 八幡東, 40109 八幡西): block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/<code>-24.0a.zip`, town-chōme
`.../19.0b/<code>-19.0b.zip`. 50,005 block keys, 1,564 town-chōme.

| Tier | MHLW permits, in a bucket, addressed (8,636) | Old-law list, in a bucket (3,018) | Barbers (817) | Beauty (2,282) |
|---|---|---|---|---|
| Block | **98.6%** | **98.8%** | **99.0%** | **99.8%** |
| Town-chōme / 大字 centroid | 0.7% | 1.2% | 0.9% | 0.2% |
| Unplaced | 0.7% | 0.0% | 0.1% | 0.0% |

**Independent check**: MHLW's own 緯度 / 経度 against the block point, 8,513
block hits: **median 32 m, 97.6% within 250 m**, 24 over 1 km. Measured with
the shared `load_city_isj` / `permits_from_rows` / `join_city`, unchanged.

---

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_40_GML.zip` (the
shared cache), with `stub_test()`'s method and the 7 wards above (492 km²).
Use **N02-25** (`"n02": "25"` in `japan.CITIES`): the newest edition. The
Shinkansen is dropped: **小倉 appears as a JR and Monorail station**.

| N02 line (operator) | Public name | In the city / N02 total | Note |
|---|---|---|---|
| 小倉線 (北九州高速鉄道) | Kitakyushu Monorail | **13 / 13** | Operator: 13 stations (its station pages) |
| 筑豊電気鉄道線 (筑豊電気鉄道) | Chikuho Electric Railroad | **14 / 21** in N02; **13 / 20** today | ⚠️ **西黒崎 closed 2026-07-31** (operator notice `/data/topics/408_20260528nishikurosakihaishi.pdf`; its front page's stop list comments it out); N02-25 still has it. Drop it at build |
| 鹿児島線 (JR九州) | JR Kagoshima Line | 16 records / 99 (13 stations: 門司港 to 折尾) | suburban, cut at the line |
| 日豊線 (JR九州) | JR Nippō Line | 7 / 113 | cut at the line |
| 日田彦山線 (JR九州) | JR Hitahikosan Line | 6 / 24 | cut at the line |
| 筑豊線 (JR九州) | JR Wakamatsu Line (筑豊本線 若松–折尾) | 6 / 26 | ⚠️ N02 files the Wakamatsu Line inside 筑豊線; the in-city part is exactly 若松–折尾. Name it from `stub_test()`'s table (trap 2) |
| 山陽線 (JR九州) | JR Sanyō Line (門司–下関) | **1 / 2** (門司) | a one-station stub: **stays as cut** (standing call); 門司 is also on the Kagoshima Line |
| 帆柱ケーブル線 (皿倉登山鉄道) | Sarakurayama Cable Car | 2 / 2 | **left out**: a sightseeing funicular (standing call); not in `excluded_stations.csv` |
| 門司港レトロ観光線 (平成筑豊鉄道) | Mojikō Retro Sightseeing Line | 4 / 4 | ⚠️ a seasonal, weekend sightseeing trolley: **left out on Kyoto's Sagano precedent**, said in a bullet under **The lines** |

- **53 stations inside the city** (N02 station groups, `N02_005g`), after the
  funicular, the retro line and 西黒崎 are out (60 groups before). Median gap to
  the nearest station **780 m**: standard rings (0.1 / 0.2 / 0.3 / 0.6 mi).
- **Gate 3**: Monorail 13 (operator) = N02 13; Chikuho 20 on the operator's
  current list (黒崎駅前 to 筑豊直方, 西黒崎 gone). JR Kyushu's per-line counts
  at build.
- ⚠️ **OSM `name:en`** for every in-city station is a build-time read (one
  Overpass query, the session's single slot; not run for this brief). Read
  every name, as Fukuoka's translated three.

## Scope

**Kitakyushu City (7 wards).** JR and Chikutetsu run on to Nakama, Nōgata,
Mizumaki, Kanda and Shimonoseki; cut at the line.

## Licences — read 2026-10-02

- **The city's BODIK lists — PERMITTED WITH CONDITIONS (CC BY 4.0).** Each
  dataset carries `license_id: cc-by`; the catalogue's terms
  (`https://odcs.bodik.jp/401005/tos/`, 北九州市オープンデータ利用規約 第1条) grant
  「クリエイティブ・コモンズ・ライセンス…の表示4.0国際」. The city site's default
  reserves reuse but does not govern catalogue items (the screen, 2026-10-01).
  - **MUST DISPLAY**: per 第6条 and CC BY 4.0, each dataset's organisation
    (北九州市 保健福祉局 保健衛生課 / 東部・西部生活衛生課), the resource name, its
    URL, the licence link, and that it was processed.
  - **Cost**: 第3条, claims from our own breach at our own cost; fault-based,
    accepted for all of Japan (2026-09-24).
- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, exactly as in
  `fukuoka.md`: a processed-by credit naming the processor, no completeness
  claim, no logo; the open minor point 2)ウ.
- **MLIT 位置参照情報 and N02**: PDL 1.0 (copy the skill's notice lines).
- **MLIT N03**: CC BY 4.0, ⛔ never drawn.

## Privacy

MHLW's file carries 法人名, 法人住所 and phones: never select them. The city's
three files carry 営業者氏名, 代表者肩書 / 肩書 and 代表者氏名: read in memory for the
name rule only, never kept. Run `check_personal_exposure.py` (`japan=True`).

## Region

East Asia today, moving to the Japan sub-region with the batch. Project to
**UTM 52N (EPSG:32652)**.

## Still open

- ⚠️ **Shared code** (each re-runs the Minato control and the city screens):
  `NAME_COLS` + 屋号名称; `OPERATOR_COLS` + 代表者氏名.
- ⚠️ **Old-law expiries** dropped by 許可終了日 against the pinned `as_of`;
  `SUPERSEDES` / one pin per premises for the 71 restaurants in both lists.
- ⚠️ **西黒崎** out of the Chikuho line (closed 2026-07-31); the Wakamatsu
  Line named inside N02's 筑豊線; the retro line left out with a page bullet.
- ⚠️ **Economic Census join control at build** (`scripts/japan_census_control.py`):
  the 2021 census counts **4,129** 飲食店 establishments in the city (門司 406,
  若松 252, 戸畑 236, 小倉北 1,565, 小倉南 405, 八幡東 263, 八幡西 1,002), the
  denominator for pins per establishment per ward.
- ⚠️ OSM `name:en` (build), and line colours on both basemaps.
- No owner item open: every call above follows a standing call or a built
  precedent.

```brief-checks
[
  {
    "id": "kitakyushu-mhlw-live",
    "claim": "MHLW's open-data file for Kitakyushu (40100) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=40100_food_business_all.csv",
    "min_bytes": 5000000
  },
  {
    "id": "kitakyushu-oldlaw-live",
    "claim": "The city's old-law food list (2026-03-31 XLSX) is live on BODIK",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/822fb681-346a-444e-b482-33c67b50cac3/resource/afce5cb5-8582-4295-8a98-494db2e25466/download/401005_shokuhineiseihotokyokashisetsuichiran_20260331.xlsx",
    "min_bytes": 200000
  },
  {
    "id": "kitakyushu-barber-live",
    "claim": "The barber register of 2026-08-31 is live on BODIK",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/8be510bd-5f67-4570-a250-b34ffdac8d37/resource/c0503e76-86d9-4f14-a052-f17ac06951d0/download/401005_riyosyoichiran_20260831.csv",
    "min_bytes": 30000
  },
  {
    "id": "kitakyushu-barber-rows",
    "claim": "The barber register of 2026-08-31 holds 817 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "c0503e76-86d9-4f14-a052-f17ac06951d0",
    "expect": 817
  },
  {
    "id": "kitakyushu-beauty-live",
    "claim": "The beauty-salon register of 2026-08-31 is live on BODIK",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/c8266fc8-5d1f-4d3b-93aa-44486f5187ea/resource/e958d9fd-6e3d-47bf-b557-96af0c3a44ca/download/401005_biyosyoichiran_20260831.csv",
    "min_bytes": 100000
  },
  {
    "id": "kitakyushu-beauty-rows",
    "claim": "The beauty-salon register of 2026-08-31 holds 2,282 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "e958d9fd-6e3d-47bf-b557-96af0c3a44ca",
    "expect": 2282
  },
  {
    "id": "kitakyushu-bodik-terms",
    "claim": "Kitakyushu's catalogue terms grant CC BY 4.0",
    "kind": "http_contains",
    "url": "https://odcs.bodik.jp/401005/tos/",
    "present": ["表示4.0国際", "第６条"]
  },
  {
    "id": "kitakyushu-no-laundry-list",
    "claim": "BODIK org 401005 has no laundry (クリーニング) dataset",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=organization:401005&q=%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0&rows=0",
    "present": ["\"count\": 0"]
  },
  {
    "id": "kitakyushu-nishikurosaki-closed",
    "claim": "Chikuho Electric Railroad's notice closing 西黒崎 on 2026-07-31 is live (its front page, UTF-8 served without a charset, lists it); N02-25 predates it",
    "kind": "http_ok",
    "url": "https://www.chikutetsu.co.jp/data/topics/408_20260528nishikurosakihaishi.pdf",
    "min_bytes": 100000,
    "content_type_contains": "pdf"
  },
  {
    "id": "kitakyushu-isj-kokurakita-live",
    "claim": "MLIT's block-level address file for Kokurakita ward (40106) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/40106-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "kitakyushu-projected-crs",
    "claim": "Kitakyushu projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 130.88,
    "expect": "EPSG:32652"
  }
]
```
