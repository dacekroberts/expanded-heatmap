# Kumamoto — build brief

**Step 0 measured 2026-10-02.** Run `python scripts/brief_check.py kumamoto`
before writing any code. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py`'s own functions from a scratch config
(`scripts/screen_japan_join.py`'s table is shared code and was not edited).
Band A on the master list (screened 2026-10-01); every figure below is
re-measured, not copied from the screen.

**✅ The owner's standing calls for every Japanese city (the `japan-city`
skill) are DECIDED:** (1) **the Shinkansen does not count**; (2) **lines served
only by limited expresses DO count**; (3) **the city line only**, a per-line
stub test at build, a one-station stub stays as cut, an urban line cut to a
stub goes back to the owner; (4) **菓子製造業 and そうざい製造業 count, in
Retail**, the factory share measured and kept; (5) **the name rule**: where the
trade name IS the operator's own name, the pin shows its permit type; (6) **no
page says "currently operating"**. **Kumamoto is the minor label tier (owner,
2026-10-02)**: a Japan sub-region per the skill's standing calls, every
Japanese city moved into it, `REGION_LABELS_ALSO["East Asia"]` naming it; the
eight built Japanese cities stay eligible.

---

## The one-line summary

**Hiroshima's two-source shape, plus personal services.** The city's own
restaurant list (counter applications, 6,793 rows at 2026-03-31) and MHLW's
食品衛生申請等システム file (online filings, 258 open restaurant permits) overlap
by 6.0% at block level and together hold about 76% of the 9,229 restaurants in
force (FY2024). The city's 理容 / 美容 / クリーニング lists (2,714 premises,
2026-03-31) complete the third bucket. Everything joins to MLIT's block file at
**96-97% block**. ⚠️ Food retail is MHLW's opt-in slice only. Rail: the city
tram (35 stops), Kumamoto Electric Railway and JR Kyushu, 61 station groups.

---

## Business leg — the city's lists plus MHLW's online filings

| | City's restaurant list | MHLW open data (43100) |
|---|---|---|
| **File** | `https://www.city.kumamoto.jp/dynamic/opendata/pub/Insyokutenneigyoukyoka.csv`: **1,105,867 B**, UTF-8 with BOM, comma, **6,793 rows**, "令和8年（2026年）3月31日現在で許可のある施設". Page `https://www.city.kumamoto.jp/dynamic/opendata/pub/detail.aspx?c_id=38&id=60` (最終更新日 2026-09-14), catalogued on BODIK as `431001_seisaku20` (frequency 不定期) | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=43100_food_business_all.csv`: **708,143 B**, UTF-8 with BOM, **1,978 rows** (329 permits, 1,636 notifications, 13 closed notifications), latest permit **2026-08-28**, updated monthly |
| **What it holds** | **Counter (窓口) applications**: restaurants only; vehicles, temporary and event permits and vending machines excluded; **「※非公開希望を除いています」** (opt-outs left out). The page sends online filings to MHLW: 「【電子申請】…食品衛生申請等システムに申請された施設情報については、下記の専用ページからご確認ください」 | **Online filings where the filer agreed to publication**, field by field |
| Columns | `No.`, **`業種`**, **`屋号`**, **`営業所所在地`** (`熊本市中央区…`, ward first), **`申請者氏名`** (operator), `申請日`, `許可日`, `期限開始日`, `期限満了日` (`YYYY/M/D`), `備考` | the national MHLW schema: `営業施設名称、屋号又は商号`, `営業の種類` (circled-number prefix, `① 飲食店営業`), `業態`, `営業施設所在地`, `営業施設方書`, **`緯度` / `経度`**, `法人名`, `法人番号`, `法人住所`, `営業施設電話番号`, permit dates, `廃業年月日`, `申請区分` |
| Restaurants | **6,793** (`飲食店営業` 4,775; `飲食店営業（一般食堂）` 1,624, `（弁当屋）` 137, `（その他）` 104, `（そうざい調理）` 75, `（旅館）` 29, and six smaller sub-types). Through `japan_eigyo`: **Food service 6,753**; out 40 (旅館 29, 仕出し屋 10, バー・キャバレー 1) | **258** open 飲食店営業 permits (2021-06-21 to 2026-08-28), **218 (84.5%) with an address** |
| Food retail | none: the list is restaurants only | permits 菓子 17, そうざい 9, 魚介類 10, 食肉 8; plus notifications (その他の食料・飲料販売業 444, 百貨店・総合スーパー 180, 野菜果物 95, コンビニ 87, 乳類 68, …). Through `japan_eigyo`, addressed fixed rows: **Retail 784, Food service 184** |

- **Overlap, measured at block level** (same ward, town and block AND the same
  normalised trade name): **12 of MHLW's 199 block-placed restaurants (6.0%)**
  are in the city's list; 141 share a block only (the centre is dense).
  Disjoint by filing channel, as Hiroshima's (1.2%).
- **Against the official count**: e-Stat's 衛生行政報告例 FY2024 gives
  **9,229** restaurants in force (`japan_official.estat()`, cached). The city
  list is **73.6%** of it; with MHLW's 258 less the overlap, **about 76%**. The
  gap is the list's own exclusions (vehicles and event stalls, which the
  official count includes, and the opt-outs) - not measured further.
- **A monthly new-permit workbook** sits beside the full list
  (`ShinnkiInsyokutenneigyoukyoka.xlsx`, 67,596 B, five sheets 4月-8月, 554 rows,
  with a `情報公開` column). Hiroshima's precedent is to read the annual full
  list only; the June sheet (356 rows) is mostly renewals.
- ⚠️ **Permit terms are extended on the page**: 「令和８年熊本地震に係る特定非常災害の指定に伴い、許可期限が令和8年（2026年）8月31日または11月30日の営業許可の期限満了日は令和9年（2027年）1月27日まで延長されます」.
  Never drop a row of this list on `期限満了日`.
- **Personal services** (pages `detail.aspx?c_id=38&id=50` / `51` / `52`, each
  最終更新日 2026-09-14, "令和8年（2026年）3月31日現在"; BODIK `431001_riyousyo`,
  `431001_biyousyo`, `431001_seisaku18-1`):

  | File | Bytes | Rows | Note |
  |---|---|---|---|
  | `https://www.city.kumamoto.jp/dynamic/opendata/pub/riyoujo_list.xlsx` | 73,985 | **616** 理容所 | |
  | `https://www.city.kumamoto.jp/dynamic/opendata/pub/biyoujo_list.xlsx` | 199,093 | **1,728** 美容所 | |
  | `https://www.city.kumamoto.jp/dynamic/opendata/pub/kurininngujyo-list.xlsx` | 51,713 | **370** クリーニング所 (受渡所 271, 処理所 99) | `クリーニング所形態` column |

  **2,714 premises.** Columns: `施設名称`, **`営業所所在地1`** (`熊本市中央区…`)
  and `営業所所在地2` (spelled `営業所所在地２` in the barber file), then
  `営業所電話番号`, **`開設者氏名`**, `確認番号`, `確認日`, **`開設者住所1（法人のみ）`**,
  `開設者住所2（法人のみ）`, `開設者電話番号（法人のみ）`, **`代表者氏名（法人のみ）`**,
  `役職（法人のみ）`. Monthly new-opening workbooks (`…_list2.xlsx`, 4月-8月)
  hold 1, 19 and 1 rows.
- **What is missing**: non-food retail (Japan's ceiling); food retail beyond
  MHLW's opt-in online slice; the city list's opt-outs.

### Column coverage in the shared code (`japan_register`)

| Column | Covered? |
|---|---|
| Food `申請者氏名` (operator) | ✅ in `OPERATOR_COLS` |
| Food `営業所所在地`, `屋号`, `業種` | ✅ `ADDR_COLS`, `NAME_COLS`, `TYPE_COLS` |
| Personal `営業所所在地1` | ❌ **not in `ADDR_COLS`**: `city_rows()` reads **0 rows** from all three workbooks today. Add it (Kumamoto named in the comment), with `営業所所在地2` / `２` as the building |
| Personal `開設者氏名`, `代表者氏名（法人のみ）` (operators) | ❌ **not in `OPERATOR_COLS`**: add both, or the name rule compares nothing there; then re-run the Minato control |
| MHLW | as Fukuoka's and Hiroshima's: no individual operator column (name rule cannot run, accepted) |

**The name rule, counted in memory** (yes/no only): food 1 of 6,793; 理容 0 of
616; 美容 0 of 1,728; クリーニング 2 of 370.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files for the **5 wards** (43101 中央, 43102 東, 43103 西, 43104 南,
43105 北): block `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/<code>-24.0a.zip`
(43101: 68,986 B), town-chōme `.../19.0b/<code>-19.0b.zip`. 62,942 block keys,
918 town-chōme keys.

| Tier | City list (6,793) | New permits 4-8月 (554) | MHLW, addressed restaurants (214 fixed) | Personal services (2,714) |
|---|---|---|---|---|
| Block | **97.0%** | 97.5% | **93.0%** | **96.8%** |
| Town-chōme / 大字 centroid | 2.4% | 2.0% | 5.1% | 2.5% |
| Unplaced | 0.6% | 0.5% | 1.9% | 0.7% |

Personal services by file: 理容 94.6 / 4.5 / 0.8, 美容 97.4 / 1.8 / 0.8,
クリーニング 97.6 / 2.2 / 0.3. MHLW's addressed food-retail rows (菓子 /
そうざい / 食肉 / 魚介類): 95.5% block.

**Independent check**: MHLW's own coordinates against the block point, a
**median 33 m** apart, **99.0% within 250 m** (199 restaurants; retail 35 m,
98.8%).

## 🚇 Rail — MLIT N02 cut at the N03 city line

Read from **N02-25** (N02-24 gives the same table here). N03:
`N03-20250101_43_GML.zip` (8,387,903 B), the 5 ward codes. 69 station records
inside, **61 `N02_005g` groups**. The Shinkansen is dropped (熊本 is also a JR
conventional station).

| Line (N02 legal name) | Operator | Inside / network | Stub test |
|---|---|---|---|
| 幹線 | 熊本市 (tram, class 21) | 10 / 10 | whole |
| 水前寺線 | 熊本市 | 7 / 7 | whole |
| 健軍線 | 熊本市 | 9 / 9 | whole |
| 田崎線 | 熊本市 | 3 / 3 | whole |
| 上熊本線 | 熊本市 | 10 / 10 | whole |
| 菊池線 | 熊本電気鉄道 | 9 / 16 | passes (56%; 御代志 end in 合志市) |
| 藤崎線 | 熊本電気鉄道 | 3 / 3 | whole |
| 鹿児島線 | 九州旅客鉄道 | 9 / 99 | a trunk cut at the line (Fukuoka kept 10 of 99) |
| 豊肥線 | 九州旅客鉄道 | 9 / 37 | cut at the line (肥後大津 beyond) |

- **The tram: 35 distinct stops** (39 records; 辛島町, 水道町, 水前寺公園 and
  熊本駅前 shared between legal lines). The public routes are **A系統**
  (田崎橋-健軍町, 26 stops) and **B系統** (上熊本-健軍町, 28 stops), 19 shared:
  35, matching the screen's operator count. ⚠️ Gate 3 at build against
  熊本市交通局's own stop list.
- Interchanges N02 groups: 上熊本 ×3 (JR, Kumamoto Electric, tram; 151 m), 熊本,
  北熊本, and the four shared tram stops.
- ⚠️ **光の森 sits 41 m inside the N03 line**: read its address at build before
  trusting the cut (豊肥線 is 8 or 9 inside). 堀川 is 298 m inside; 新須屋 152 m
  outside.
- ⚠️ **Labels**: the tram's legal lines (幹線, 水前寺線…) are not what riders
  read; A and B are. Tokyo's `route` mechanism draws a public service over legal
  lines; Hiroshima drew Hiroden by legal line. Choose at build, with
  `stub_test()`'s table in hand.
- English names: OSM `name:en` (station and `tram_stop` queries) at build.
  **No Overpass query was run for this brief**; checking name:en is a build
  item.

## Scope

**Kumamoto City (5 wards).** Kumamoto Electric runs on to 合志市; JR to 宇土
(246 m outside), 肥後大津 and beyond.

## Licences — read 2026-10-02

- **The city's restaurant list — PERMITTED WITH CONDITIONS (PDL 1.0).** The
  page's licence badge is alt-texted 「公共データ利用規約へのリンク」; BODIK's
  `431001_seisaku20` carries `PDL1.0`; the city's catalogue terms
  (`https://odcs.bodik.jp/431001/tos/`, linked from the city's open-data page)
  apply 「公共データ利用規約（第1.0 版）（PDL1.0）」 by default. **MUST DISPLAY**
  the catalogue's prescribed form, filled in:
  `「熊本市_食品衛生法に基づく飲食店営業許可施設一覧」（熊本市オープンデータカタログサイト）をもとに<processor>作成`,
  and that it was processed. **MUST NOT** present the processed data as the
  city's own.
- **The 理容 / 美容 / クリーニング lists — PERMITTED WITH CONDITIONS.** Each
  page states 「ライセンスはCC-BYです。」 with a 「クリエイティブ・コモンズ　表示　4.0　国際」
  badge; BODIK lists the same datasets as PDL 1.0. Both permit this use and one
  credit can satisfy both (title, 熊本市, the licence, processed). ⚠️ Name both
  in the data-sources row.
- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, re-read 2026-10-02
  (`https://i2fas.mhlw.go.jp/termsofuse.htm`): **MUST DISPLAY**
  `「食品衛生申請等システム」（厚生労働省）（<page URL>）を加工して作成` and who
  processed it; no completeness or accuracy claim; no logo. The minor open point
  (免責 2) ウ) stands, as in `docs/data_sources/japan.md`.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **N03**: CC BY 4.0, never drawn.
- Fault-based cost clauses: accepted for all of Japan (2026-09-24).

## Privacy

Read only `屋号` / `施設名称`, `業種` / `営業の種類`, `業態` and the premises
address. `申請者氏名`, `開設者氏名` and `代表者氏名（法人のみ）` are read in
memory for the name rule only. **Never select** `開設者住所1/2（法人のみ）` (an
operator's address; 155 of the 370 laundry rows, 402 beauty, 58 barber),
phones, `役職`, or MHLW's `法人名` / `法人番号` / `法人住所`. **The food list's
`備考` describes the glyphs of operators' names: never select or print it.**
Run `check_personal_exposure.py` with `japan=True`.

## Region

Japan sub-region (minor tier, above). Project to **UTM 52N (EPSG:32652)**.

## Open items

- ✅ **`mode`: `tram` (owner, 2026-10-02).** JR about 17 stations (Kagoshima and Hōhi, sharing 熊本) against the tram's 35. The owner's rule (2026-10-02): Dublin's precedent, so commuter rail drawn beside a tram does not make a city `metro`, "unless there is substantial JR, JR reads as metro". Staging read substantial as JR being the city's largest rail network by stations inside the city line..
- ⚠️ **Food retail is MHLW's opt-in online slice only** (784 addressed rows,
  mostly notifications); the page says so, as Hiroshima's and Fukuoka's.
- ⚠️ **The two shared-code additions** (`ADDR_COLS` 営業所所在地1;
  `OPERATOR_COLS` 開設者氏名, 代表者氏名（法人のみ）), then the Minato control
  (98.0 / 0.2 / 1.8) and every city screen, old against new.
- ⚠️ **About 76% of restaurants in force** are in the two lists; the page
  states the share as Osaka's and Tokyo's do.
- ⚠️ **The Economic Census join control** at build
  (`scripts/japan_census_control.py`): the 2021 census holds **2,893** 飲食店
  establishments (中央 1,780, 東 453, 西 197, 南 222, 北 241). About 6,940
  food-service pins would be **about 2.4 per establishment**, above
  Hiroshima's 1.80: read the per-ward ratios before publishing.
- ⚠️ Tram labels (A / B or legal lines), 光の森, gate 3 against the operator,
  OSM `name:en`.

```brief-checks
[
  {
    "id": "kumamoto-food-list-live",
    "claim": "Kumamoto City's restaurant list (counter applications, CSV, as of 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kumamoto.jp/dynamic/opendata/pub/Insyokutenneigyoukyoka.csv",
    "min_bytes": 900000
  },
  {
    "id": "kumamoto-food-page-pdl",
    "claim": "The list's page carries the PDL 1.0 badge, the 2026-03-31 date, the opt-out note and the pointer to MHLW for online filings",
    "kind": "http_contains",
    "url": "https://www.city.kumamoto.jp/dynamic/opendata/pub/detail.aspx?c_id=38&id=60",
    "present": ["公共データ利用規約へのリンク", "令和8年（2026年）3月31日現在で許可のある施設です", "非公開希望を除いています", "食品衛生申請等システム"]
  },
  {
    "id": "kumamoto-bodik-pdl",
    "claim": "BODIK lists the restaurant dataset under PDL 1.0",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=431001_seisaku20",
    "present": ["PDL1.0"]
  },
  {
    "id": "kumamoto-mhlw-live",
    "claim": "MHLW's open-data file for Kumamoto City (43100) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=43100_food_business_all.csv",
    "min_bytes": 400000
  },
  {
    "id": "kumamoto-mhlw-terms-pdl",
    "claim": "MHLW's system site applies PDL 1.0 (ASCII only: the page declares no charset the check reads, so its Japanese text is not matchable here)",
    "kind": "http_contains",
    "url": "https://i2fas.mhlw.go.jp/termsofuse.htm",
    "present": ["PDL1.0"]
  },
  {
    "id": "kumamoto-barber-live",
    "claim": "Kumamoto City's barber list (理容所, 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kumamoto.jp/dynamic/opendata/pub/riyoujo_list.xlsx",
    "min_bytes": 40000
  },
  {
    "id": "kumamoto-beauty-live",
    "claim": "Kumamoto City's beauty-salon list (美容所, 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kumamoto.jp/dynamic/opendata/pub/biyoujo_list.xlsx",
    "min_bytes": 100000
  },
  {
    "id": "kumamoto-laundry-live",
    "claim": "Kumamoto City's laundry list (クリーニング所, 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kumamoto.jp/dynamic/opendata/pub/kurininngujyo-list.xlsx",
    "min_bytes": 30000
  },
  {
    "id": "kumamoto-barber-page-ccby",
    "claim": "The personal-services pages state CC BY (4.0 International badge)",
    "kind": "http_contains",
    "url": "https://www.city.kumamoto.jp/dynamic/opendata/pub/detail.aspx?c_id=38&id=50",
    "present": ["ライセンスはCC-BYです", "クリエイティブ・コモンズ"]
  },
  {
    "id": "kumamoto-catalogue-terms",
    "claim": "The city's open-data catalogue terms apply PDL 1.0 by default and prescribe the 熊本市オープンデータカタログサイト credit",
    "kind": "http_contains",
    "url": "https://odcs.bodik.jp/431001/tos/",
    "present": ["PDL1.0", "熊本市オープンデータカタログサイト"]
  },
  {
    "id": "kumamoto-isj-chuo-live",
    "claim": "MLIT's block-level address file for Chuo ward (43101) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/43101-24.0a.zip",
    "min_bytes": 30000
  },
  {
    "id": "kumamoto-projected-crs",
    "claim": "Kumamoto projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 130.71,
    "expect": "EPSG:32652"
  }
]
```
