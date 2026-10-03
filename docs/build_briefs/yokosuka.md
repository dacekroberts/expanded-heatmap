# Yokosuka — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live). Run `python scripts/brief_check.py yokosuka` before writing any code.
Coordinates: the `address-join` skill, measured with `japan_register.py`'s own
functions from a scratch script (the shared `scripts/screen_japan_join.py`
table was not edited). Build with the `japan-city` skill.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls):** (1) **the Shinkansen does not count** (2026-09-24); (2)
**lines served only by limited expresses count** (2026-09-28); (3) **the city
line only**: only stations inside the city get rings, a one-station stub stays
as cut, and an URBAN line cut to a stub goes back to the owner (2026-09-24,
2026-09-27); (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**
(2026-09-27); (6) **no page says "currently operating"**. Fault-based cost
clauses are accepted for all of Japan (2026-09-24).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Yokosuka carries `label_tier: "minor"` and joins the Japan sub-region the
2026-10-01 batch creates.

**`mode`: `metro` recommended (🚨 below).** No subway, tram or light rail:
the backbone is Keikyū, a private heavy commuter railway (17 station groups
against JR's 4).

---

## The one-line summary

**All three buckets from the city's own CC BY 4.0 lists on BODIK: every food
permit in force at 2026-08-31 (4,172 rows; 3,448 restaurants, 99.6% of the
official 3,461), and full barber, beauty and laundry lists (1,140 rows).**
The block join places 96.5% of fixed food premises and 95.8-99.6% of the
registers. Rail: 21 station groups, Keikyū's Main and Kurihama Lines and JR's
Yokosuka Line. **Band A.** MHLW's file is opt-in here (4%) and is used only
as a control.

---

## Business leg — the city's datasets on BODIK (organization 142018)

Two datasets, both `license_id: cc-by-40-intl`, frequency 毎月, author
民生局健康部保健所生活衛生課. All resources are datastore-backed except the
minpaku file (not used), so the checks below read row counts.

| | Food (`142018_00_18_syokuhin_all`) | Barbers | Beauty | Laundries, general | Laundries, pick-up (取次店) |
|---|---|---|---|---|---|
| **Dataset** | 【横須賀市】食品営業許可施設公開情報 （食品営業許可を取得している全施設） | `142018_00_19_environmental_sanitation_facilities` (【横須賀市】環境衛生関係営業施設公開情報) | same | same | same |
| **File** | `https://data.bodik.jp/dataset/3a1aaf46-e6ca-41fa-8977-3388f3b7e3ba/resource/4c06c4b1-84de-4c4c-af65-fff85a7963e4/download/syoku08.csv`: **1,007,571 B** | `https://data.bodik.jp/dataset/76f9d975-d773-486b-b7ad-48d046a4a696/resource/d888225b-47f9-431a-9fcd-de53153e6eb9/download/riyouzyo_202608.xlsx`: **43,616 B** | `…/resource/0e4a4287-f846-4ba2-aa09-1cbbd554ddba/download/biyouzyo_202608.xlsx`: **105,860 B** | `…/resource/bed0a6b2-683a-46b7-8f39-5ccd9552a97f/download/kuri-ninngu_ippann_202608.xlsx`: **18,576 B** | `…/resource/26c5d72d-91ba-4128-938c-8695f008e54c/download/kuri-ninngu_toritugi_202608.xlsx`: **25,616 B** |
| Rows | **4,172** | **251** | **745** | **49** | **95** |
| As of | **2026-08-31** (resource 「営業許可を取得している全施設　2026年8月末現在」, uploaded 2026-09-16; newest 初施行日 2026-08-07) | 2026-08 (uploaded 2026-09-10) | 2026-08 | 2026-08 | 2026-08 |
| Cadence | monthly; a new file name each month (`syoku08.csv`) | monthly | monthly | monthly | monthly |
| Encoding | UTF-8 with BOM, CSV | XLSX | XLSX | XLSX | XLSX |
| Columns | 許可番号, **申請者住所**, 申請者法人名称, 申請者役職, 申請者氏名, 営業者電話番号, **営業所所在地**, **営業所名称**, 営業所電話番号, **業種**, **詳細業種**, 初施行日 | **営業所名称**, 営業所電話番号, **営業所所在地**, 確認年月日, 確認通知書番号, 営業者氏名・法人名称, 法人代表者, 法人電話番号 | as barbers | as barbers | as barbers |

The food dataset has a twin, `142018_00_18_syokuhin_monthly` (new permits,
the last three months): not needed.

**Counts that matter** (`japan_eigyo`, with 詳細業種 read as the form, below):

| Bucket | Rows (fixed, addressed) |
|---|---|
| Food service | **2,960** (restaurant 2,957, café 3) |
| Food retail (permit types) | **556**: 菓子 311, そうざい 92, 魚介類販売 91, 食肉販売 62 |
| Personal services | **1,138**: barbers 250, beauty 745, laundries 48 + 95 |
| Out (fixed) | institutional catering 129, snack bars and cabarets 57, 仕出し 44, inside accommodation 35, vending 20, manufacturing ("no rule") 133 |

- **Restaurants against the official count**: 3,448 飲食店営業 rows against
  e-Stat's FY2024 in force **3,461**: **99.6%**.
- **Addresses**: 3,222 of 3,448 restaurant rows carry one; the unaddressed are
  mostly stalls and vehicles (詳細業種 屋台型臨時営業 89, 自動車による営業 103).
- **One premises, several permits**: 2,960 fixed Food service rows are 2,927
  distinct (address, trade name) pairs.

### MHLW's file — a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=14201_food_business_all.csv`:
**298,467 B, 803 rows** (届出 623, 許可 175, 許可(廃業) 5), newest 許可年月日
2026-08-21. **133 open restaurant permits, 3.8% of the official count**
(opt-in). **96.2% of MHLW's block-tier named restaurant permits (102 of 106)
are in the city's list** with the same town, block and trade name. The city's
list is the food source (Toyama's shape); leave MHLW's notifications out and
say so in the page's standing bullet.

### Against the shared code (Phase 1 is on master; what is still missing)

- ⚠️ **詳細業種 is the list's 業態** (`給食` 147, `屋台型臨時営業` 89, `自動車による
  営業(…)` 103, `旅館の経営を兼ねる飲食店営業` 35, `スナック` 55, `仕出し屋` 44,
  `キャバレー` 2): `permits_from_rows` reads the form from 業態 only, so today
  every one of them would be Food service. Read 詳細業種 as the form (a column
  alias, or a per-source config); measured here that way. `クラブ又はナイトクラブ`
  (1) is not caught by the hostess rule; read it at build.
- ⚠️ **`OPERATOR_COLS` lacks the registers' 営業者氏名・法人名称** (a sole trader's
  own name or a company's, on every row): add it, or the rule compares nothing
  there. Measured with it: **2** rows flagged (beauty 1, pick-up laundry 1).
- **The food list names operators for companies only** (申請者氏名 and
  申請者法人名称 are filled on the same 1,940 rows): the rule flags **0** food
  rows and cannot see a sole trader. Toyama's position, accepted by the owner
  (2026-10-02): the MHLW-style bullet for the food layer.
- Already covered: `ADDR_COLS` 営業所所在地, `NAME_COLS` 営業所名称, `TYPE_COLS`
  業種, the ward-less flag (Yokosuka has no wards), N02-25, the XLSX reader
  (one sheet each, header on row 1).

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 14201)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/14201-24.0a.zip` (201,228 B) and
`…/19.0b/14201-19.0b.zip` (10,086 B): 11,776 block keys, 348 town-chōme. The
city is ward-less: `japan.CITIES["yokosuka"]` needs `"wardless": True`.

| Tier | Food, fixed in a bucket (3,516) | Barbers (250) | Beauty (745) | Laundries, general (48) | Pick-up (95) |
|---|---|---|---|---|---|
| Block | **96.5%** | **99.6%** | **98.5%** | **95.8%** | **97.9%** |
| Town-chōme / 大字 centroid | 3.4% | 0.0% | 1.3% | 4.2% | 1.1% |
| Unplaced | 0.1% (3) | 0.4% (1) | 0.1% (1) | 0.0% | 1.1% (1) |

**Independent check**: for the 102 restaurants in both lists, the city row's
block point against MHLW's own coordinates: **median 35 m, 91.2% within
250 m**. MHLW's own rows against their block point: median 32 m (325 rows).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (14201)

Read from the shared cache (100.8 km²; extent S 35.168, W 139.576, N 35.330,
E 139.747; the box includes 猿島). **22 station records, 21 `N02_005g`
groups** (堀ノ内 shared by both Keikyū lines). No Shinkansen. Median gap to
the nearest station group **840 m**.

| Operator | N02 line | Inside / N02 total | Stations inside |
|---|---|---|---|
| 京浜急行電鉄 | 本線 | **11 / 50** | 追浜, 京急田浦, 安針塚, 逸見, 汐入, 横須賀中央, 県立大学, 堀ノ内, 京急大津, 馬堀海岸, 浦賀 |
| 京浜急行電鉄 | 久里浜線 | **7 / 9** | 堀ノ内, 新大津, 北久里浜, 京急久里浜, YRP野比, 京急長沢, 津久井浜 (三浦海岸 and 三崎口 beyond, in Miura) |
| 東日本旅客鉄道 | 横須賀線 | 4 / 9 | 田浦, 横須賀, 衣笠, 久里浜 |

- **Groups by operator**: Keikyū 17, JR East 4. No line is cut to a stub.
- ⚠️ **Gate 3**: the operators' own station counts at build.
- ⚠️ **OSM `name:en`**: not queried (no Overpass at Step 0). One station query
  in the N03 box at build; no tram stops.

## Scope

**Yokosuka City (14201), one municipality, no wards.** Keikyū's Main Line and
JR's Yokosuka Line run on to Yokohama and Zushi; the Kurihama Line to Miura.
Cut at the line.

## Licences — read 2026-10-02

- **Yokosuka City's BODIK datasets — PERMITTED WITH CONDITIONS (CC BY 4.0).**
  - **The grant**: the catalogue's terms (`https://odcs.bodik.jp/142018/tos/`)
    第１条, 「本市等が著作権を有する著作物の利用…については、クリエイティブ・コモンズ・ライセンス
    …表示4.0国際…によるものとします」; both `package_show` records say
    `cc-by-40-intl`. The city's own open-data page
    (`https://www.city.yokosuka.kanagawa.jp/shisei/opendata/index.html`):
    「オープンデータカタログサイト（外部サイト）上のデータは、全てクリエイティブ・コモンズ表示4.0国際ライセンス
    …の下に提供されています」, and 「当ライセンスは、上記サイト上のデータのみに適用されます」:
    **fetch from data.bodik.jp only**, never a copy on the city's site (its
    site terms reserve reuse).
  - **MUST DISPLAY** (no wording is prescribed; CC BY 4.0's attribution):
    `「【横須賀市】食品営業許可施設公開情報 （食品営業許可を取得している全施設）」（営業許可を取得している全施設　2026年8月末現在）、横須賀市、クリエイティブ・コモンズ・ライセンス 表示4.0国際（https://creativecommons.org/licenses/by/4.0/deed.ja）を加工して作成`,
    and likewise `「【横須賀市】環境衛生関係営業施設公開情報」の理容所一覧、美容所一覧、クリーニング所（一般店）一覧、クリーニング所（取次店）一覧`.
  - **MUST NOT**: use the city's logo or symbol (第３条); claim completeness or
    accuracy (第４条1).
  - **Cost** (第４条3): complaints from the user's own breach are resolved at
    the user's cost. The fault-based class, ✅ accepted for every Japanese
    source (2026-09-24).
- **MHLW open data** (control only): PDL 1.0, as recorded in
  `docs/data_sources/japan.md`.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **MLIT N03**: CC BY 4.0, ⛔ never
  drawn.

## Privacy

Read only 営業所名称, 業種 / 詳細業種 and 営業所所在地. **申請者住所 (the food
list) is an operator's own address: never select it**, nor any 電話番号.
営業者氏名・法人名称, 法人代表者, 申請者氏名 and 申請者法人名称 are read in memory by
the name rule only. Run `check_personal_exposure.py` with `japan=True`. No row
value was printed for this brief.

## Region

The Japan sub-region (minor tier, above); `"country": "Japan"`. Project to
**UTM 54N (EPSG:32654)**.

## Open items

- 🚨 **`mode` for a city whose backbone is a private heavy railway.** The
  owner's rule (2026-10-02) names JR, trams and subways; Yokosuka has Keikyū
  (17 groups) and JR (4), no subway, tram or light rail. **Recommendation:
  `metro`**, the rule's own reading carried over: "substantial JR reads as
  metro", and Keikyū is the same kind of railway as JR, frequent heavy rail.
- ⚠️ 詳細業種 read as the form, and `OPERATOR_COLS` + 営業者氏名・法人名称
  (shared code; each re-runs the Minato control).
- ⚠️ **Economic Census join control** (`scripts/japan_census_control.py`): the
  2021 census counts **1,373** 飲食店 establishments in 14201; 2,927 distinct
  placed premises is **2.13 per establishment**, above the built cities'
  1.56–1.92 (Matsuyama's 2.78 is flagged too). Explain it at build before
  publishing: the census date (2021-06) against a list of 2026, the permit
  structure, or the join.
- ⚠️ The files are renamed every month (`syoku08.csv`, `…_202608.xlsx`) under
  stable resource ids: the fetch reads each resource's current URL from
  `package_show`.
- ⚠️ Gate 3; OSM `name:en`; the 菓子 / そうざい factory share (step 2 prints it).

```brief-checks
[
  {
    "id": "yokosuka-food-live",
    "claim": "Yokosuka's full food-permit list (2026-08-31) is keyless and live on BODIK",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/3a1aaf46-e6ca-41fa-8977-3388f3b7e3ba/resource/4c06c4b1-84de-4c4c-af65-fff85a7963e4/download/syoku08.csv",
    "min_bytes": 700000
  },
  {
    "id": "yokosuka-food-rows",
    "claim": "The food list of 2026-08-31 holds 4,172 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "4c06c4b1-84de-4c4c-af65-fff85a7963e4",
    "expect": 4172
  },
  {
    "id": "yokosuka-barber-rows",
    "claim": "The barber list of 2026-08 holds 251 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "d888225b-47f9-431a-9fcd-de53153e6eb9",
    "expect": 251
  },
  {
    "id": "yokosuka-beauty-rows",
    "claim": "The beauty-salon list of 2026-08 holds 745 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "0e4a4287-f846-4ba2-aa09-1cbbd554ddba",
    "expect": 745
  },
  {
    "id": "yokosuka-laundry-general-rows",
    "claim": "The general laundry list of 2026-08 holds 49 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "bed0a6b2-683a-46b7-8f39-5ccd9552a97f",
    "expect": 49
  },
  {
    "id": "yokosuka-laundry-pickup-rows",
    "claim": "The laundry pick-up (取次店) list of 2026-08 holds 95 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "26c5d72d-91ba-4128-938c-8695f008e54c",
    "expect": 95
  },
  {
    "id": "yokosuka-food-licence",
    "claim": "The food dataset's catalogue record says cc-by-40-intl and points at syoku08.csv",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=142018_00_18_syokuhin_all",
    "present": ["cc-by-40-intl", "syoku08.csv"]
  },
  {
    "id": "yokosuka-env-licence",
    "claim": "The environmental-hygiene dataset's record says cc-by-40-intl and points at the 2026-08 files",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=142018_00_19_environmental_sanitation_facilities",
    "present": ["cc-by-40-intl", "riyouzyo_202608.xlsx", "biyouzyo_202608.xlsx", "kuri-ninngu_ippann_202608.xlsx", "kuri-ninngu_toritugi_202608.xlsx"]
  },
  {
    "id": "yokosuka-bodik-terms",
    "claim": "Yokosuka's catalogue terms grant CC BY 4.0 International",
    "kind": "http_contains",
    "url": "https://odcs.bodik.jp/142018/tos/",
    "present": ["表示4.0国際"]
  },
  {
    "id": "yokosuka-mhlw-live",
    "claim": "MHLW's open-data file for Yokosuka (14201) answers a plain keyless GET (the control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=14201_food_business_all.csv",
    "min_bytes": 150000
  },
  {
    "id": "yokosuka-isj-live",
    "claim": "MLIT's block-level address file for Yokosuka (14201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/14201-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "yokosuka-projected-crs",
    "claim": "Yokosuka projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.67,
    "expect": "EPSG:32654"
  }
]
```
