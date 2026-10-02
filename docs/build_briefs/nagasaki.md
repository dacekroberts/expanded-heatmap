# Nagasaki — build brief

**Step 0 measured 2026-10-02.** Run `python scripts/brief_check.py nagasaki`
before writing any code. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py`'s own functions from a scratch config
(`scripts/screen_japan_join.py`'s table is shared code and was not edited).
Band A on the master list (screened 2026-10-01); every figure below is
re-measured, and **two of the screen's claims do not hold** (next section).

**✅ The owner's standing calls for every Japanese city (the `japan-city`
skill) are DECIDED:** (1) **the Shinkansen does not count**; (2) **lines served
only by limited expresses DO count**; (3) **the city line only**, a per-line
stub test at build, a one-station stub stays as cut, an urban line cut to a
stub goes back to the owner; (4) **菓子製造業 and そうざい製造業 count, in
Retail**, the factory share measured and kept; (5) **the name rule**: where the
trade name IS the operator's own name, the pin shows its permit type; (6) **no
page says "currently operating"**. **Nagasaki is the minor label tier (owner,
2026-10-02)**: a Japan sub-region per the skill's standing calls, every
Japanese city moved into it, `REGION_LABELS_ALSO["East Asia"]` naming it; the
eight built Japanese cities stay eligible.

---

## The one-line summary

**All three buckets from the city's BODIK lists (CC BY 4.0), but they are a
2023 snapshot, not 2025**: the food list's newest permit is **2023-06-30** and
the personal lists' newest is **2023-03-31**; BODIK's 2025-03-27 is the upload
date. **The files carry no coordinates** (`緯度` / `経度` empty on all 6,138
rows), but they join to MLIT's block file at **90.9% block, nothing unplaced**.
MHLW's current file (4,005 open restaurant permits, 84% of the 4,777 in force)
publishes an address for only 47.8%. The city's own current list (2026-06)
needs its permission. Rail: Nagasaki Electric Tramway (38 stops) and JR's
Nagasaki Line, 43 station groups.

### ⚠️ What the screen got wrong (master list row, 2026-10-01; corrected 2026-10-02)

| The row says | Measured 2026-10-02 |
|---|---|
| "6,138 rows **with 緯度/経度**" | The columns exist and are **empty on all 6,138 rows**: the address join does the placing |
| "loaded 2025-03-27 … **The page states the 2025-03 date**" | 2025-03-27 is BODIK's upload stamp. **Every row dates to 2023-06-30 or before** (`許可年月日` max 2023-06-30; every `許可満了日` ≥ 2023-06-30): a snapshot of permits in force on **2023-06-30**. Five rules, rule 2: date it from the rows. The personal lists' newest `確認年月日`: 2023-02-06 / 2023-03-31 / 2023-03-29 |
| "about 41 stops" | N02 has **38** distinct tram stops (below) |

Both dates are inside the five-year ceiling (rule 3) until 2028-03 / 2028-06.

---

## Business leg

| | BODIK `food_all` (the city's, CC BY 4.0) | MHLW open data (42201) |
|---|---|---|
| **File** | `https://data.bodik.jp/dataset/4d70b9d1-9885-4045-9f59-9d1b99e02910/resource/1125a70b-ac9d-49f6-ba87-1011d0db4f1a/download/422011_food_business_all.csv`: **1,339,785 B**, UTF-8, comma, **6,138 rows** (one quoted field holds a line break). Dataset `422011_food_business_all`, "食品等営業許可・届出一覧（全許可・届出一覧）（長崎市）", frequency 1年, uploaded 2025-03-27, **not updated since** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=42201_food_business_all.csv`: **2,339,833 B**, UTF-8 with BOM, **7,755 rows** (5,251 permits, 2,492 notifications, 12 closed), latest permit **2026-08-31**, monthly |
| **As of** | **2023-06-30** (permits 2017-04-03 to 2023-06-30) | 2026-08-31 (permits 2021-06-08 on) |
| Columns | the national 推奨データセット schema: `施設名称`, `営業の種類`, **`業態`**, `所在地_連結表記` (`長崎県長崎市…`, filled on every row; `施設所在地_町字` / `_番地以下` empty), `施設方書`, `緯度` / `経度` (**empty**), `施設電話番号`, `連絡先メールアドレス`, `法人名`, `法人番号`, `許可番号`, permit dates, `申請区分` (新規 3,975 / 継続 2,163) | the MHLW schema, as Kumamoto's and Kagoshima's: `営業施設名称、屋号又は商号`, `営業の種類`, `業態`, `営業施設所在地`, `緯度` / `経度`, `法人名`, permit dates, `申請区分` |
| Restaurants | **4,598** 飲食店営業 rows (old law 2,809, new law 1,789). Through `japan_eigyo` with `業態`: **Food service 3,389**; out: **スナック 716** (the hostess rule, read from `業態`), temporary and mobile 292 (移動車, 仮設1-3号), institutional catering 202, inside accommodation 97, 仕出し 26 | **4,005** open 飲食店営業 permits, **1,915 (47.8%) with an address**; vehicles and stalls by `業態` about 190 |
| Food retail | **Retail 1,093** (菓子 497, 魚介類 317, そうざい 166, 食肉 147, …) | permits 菓子 449, そうざい 160, 魚介類 185, 食肉 112, plus notifications |

- **Personal services** (BODIK, CC BY 4.0, uploaded 2025-03-27, newest row
  2023-03-31; UTF-8):

  | File | Bytes | Rows |
  |---|---|---|
  | `https://data.bodik.jp/dataset/ab4e452b-c72a-49f4-9b25-0379893cce3f/resource/6ccea115-9386-462c-b581-d1d959f16744/download/422011_riyosho_all.csv` | 43,306 | **380** 理容所 (`業務種別` 床屋) |
  | `https://data.bodik.jp/dataset/9508163b-44a6-4356-abb3-b631b1e4ef72/resource/7d5b0ea8-048e-4534-a8ed-bf9f772c958f/download/422011_biyosho_all.csv` | 126,003 | **999** 美容所 |
  | `https://data.bodik.jp/dataset/ea649bea-a49f-4ddc-b1a1-2f55f6f6e8c0/resource/fb933c7e-f41a-4b52-8582-039390d66865/download/422011_cleners_all.csv` | 43,178 | **262** クリーニング所 (`業態等` 取次 184 / 洗い 78) |

  **1,641 premises.** Columns: `施設名称`, `所在地_連結表記`, `施設電話番号`,
  `業務種別`, (`業態等`), `法人名`, `確認年月日`, `確認番号`, `備考`. Each
  dataset's monthly "新規" twin holds one month (2025-01) only, so the gap
  2023-07 to 2024-12 cannot be filled from BODIK.
- **The official count**: e-Stat FY2024, **4,777** restaurants in force. The
  snapshot held 4,598 restaurant rows at 2023-06-30 (96% of that figure);
  by its own expiry dates, 2,231 are still unexpired today (470 old law, 1,761
  new law).
- **MHLW appears to carry every new permit** (as Kagoshima's and
  Kitakyushu's): 4,005 open restaurant permits since 2021-06, against the city's
  own 4,087 new-law restaurant rows at 2026-06. **Overlap with BODIK, measured
  at block level**: 1,145 of MHLW's 1,654 block-placed restaurants (69.2%)
  share a block AND a normalised trade name with the snapshot, as they should:
  the snapshot's new-law rows are the same filings.
- **What MHLW adds beyond the snapshot**: 2,566 open restaurant permits
  granted after 2023-06-30; 2,168 Food service after the taxonomy, **889
  (41.0%) with an address**. Some are renewals of premises already in the
  snapshot (`SUPERSEDES` takes the pair once).
- **The city's own current list — measured, not usable without permission**:
  `https://www.city.nagasaki.lg.jp/uploaded/attachment/64426.xlsx` (575,437 B;
  page `https://www.city.nagasaki.lg.jp/page/6755.html`, 更新日 2026-07-21),
  sheet `営業者一覧表`, **6,412 rows**, as of 2026-06; 4,869 restaurant rows
  (`新飲食店営業` 4,087 + `飲食店営業` 782); columns `許可番号`, **`営業者名`**,
  `屋号`, `営業所住所`, `営業所固定電話番号`, `業種名`, `種別名`, `許可日`,
  `許可開始日`, `許可終了日`, `許可区分`. It joins at 91.2% block. The page:
  「一覧にはすでに廃業している施設が含まれている場合があります」.
- **What is missing**: non-food retail (Japan's ceiling); everything since
  2023-06 / 2023-03 unless MHLW is layered on; personal services since
  2023-03 (no current source without the city's permission).

### Column coverage in the shared code (`japan_register`)

| Column | Covered? |
|---|---|
| BODIK `所在地_連結表記`, `施設名称`, `営業の種類`, `業態` | ✅ (`業態` read as `form`) |
| BODIK personal `業務種別` | ✅ `TYPE_COLS` (the source decides the bucket) |
| An individual operator column | **none**: BODIK's lists carry `法人名` only, as MHLW's and Tokyo's national-schema lists do. **The name rule cannot run on any Nagasaki row**; Tokyo's and Fukuoka's precedent is to accept that and say so on the page |
| City's current list `営業者名` | ✅ `OPERATOR_COLS` (only if permission comes) |

⚠️ Some new-law rows carry trailing spaces in `営業の種類` and `業態`
(`移動車 `); `japan_eigyo.normalise()` strips them, but a filter written with
`==` will not (measured: 1,789 restaurant rows missed by an exact match).

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, no wards)

MLIT files for **42201**: block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/42201-24.0a.zip` (325,444 B),
town-chōme `.../19.0b/42201-19.0b.zip` (12,464 B). 29,762 block keys, 477
town-chōme keys. The ward key is empty on both sides (`長崎市` has no wards).

| Tier | BODIK food, all (5,862 fixed) | BODIK restaurants (4,375 fixed) | Personal services (1,639) | MHLW, addressed restaurants (1,879 fixed) |
|---|---|---|---|---|
| Block | **88.6%** | **90.9%** | **90.1%** | **88.0%** |
| Town-chōme / 大字 centroid | 11.3% | 9.1% | 9.7% | 11.9% |
| Unplaced | 0.1% | 0.0% | 0.2% | 0.1% |

Personal services by file: 理容 86.3 / 13.2 / 0.5, 美容 91.7 / 8.1 / 0.2,
クリーニング 89.3 / 10.7 / 0.0. The chōme tier is wider than Kumamoto's
(2.4%): read the misses at build (`--misses`), as Sendai's 字 rule came from
its misses.

**Independent check**: MHLW's own coordinates against the block point, a
**median 33 m** apart, **95.9% within 250 m**, 4 beyond 1 km (1,654
restaurants). BODIK has no coordinates of its own to check against.

## 🚇 Rail — MLIT N02 cut at the N03 city line

N02-25 and N02-24 give the same table. N03: `N03-20250101_42_GML.zip`
(23,891,588 B), code 42201. 48 station records inside, **43 `N02_005g`
groups**. The Shinkansen is dropped (長崎 is also a JR conventional station).

| Line (N02 legal name) | Operator | Inside / network | Stub test |
|---|---|---|---|
| 本線 | 長崎電気軌道 (class 21) | 25 / 25 | whole |
| 赤迫支線 | 長崎電気軌道 | 2 / 2 | whole |
| 桜町支線 | 長崎電気軌道 | 3 / 3 | whole |
| 蛍茶屋支線 | 長崎電気軌道 | 8 / 8 | whole |
| 大浦支線 | 長崎電気軌道 | 5 / 5 | whole |
| 長崎線 | 九州旅客鉄道 | 5 / 41 (長崎, 浦上, 西浦上, 現川, 肥前古賀) | a trunk cut at the line; 道ノ尾 is 33 m outside, in 長与町 |

- **The tram: 38 distinct stops** (43 records; 住吉, 長崎駅前, 市役所, 西浜町,
  新地中華街 shared between legal lines). N02-25 already names
  スタジアムシティノース and スタジアムシティサウス. The operator runs routes
  **1** (赤迫-崇福寺), **3** (赤迫-蛍茶屋) and **5** (石橋-蛍茶屋); its route page
  says 「４号系統の運行を休止させていただきます」. ⚠️ **Gate 3**: the operator's
  route page (`https://www.naga-den.com/pages/9/`) links 36 distinct stop
  names (市役所 twice) and none of the two Stadium City names, so reconcile
  its list with N02's 38 at build.
- ⚠️ **Labels**: legal lines or the operator's routes 1 / 3 / 5 (Tokyo's
  `route`), as Kumamoto's A / B: choose at build.
- English names: OSM `name:en` (station and `tram_stop` queries) at build.
  **No Overpass query was run for this brief.**

## Scope

**Nagasaki City (one municipality, no wards).** JR runs on to 長与町 and
諫早市.

## Licences — read 2026-10-02

- **BODIK lists (food and the three personal lists) — PERMITTED WITH
  CONDITIONS (CC BY 4.0).** Each dataset's `license_id` is `cc-by-40-intl`;
  the city's catalogue terms (`https://odcs.bodik.jp/422011/tos/`,
  「長崎市オープンデータ利用規約」, in force 2020-03-07) apply
  「クリエイティブ・コモンズ・ライセンス…の表示4.0国際」 and say that where the same
  dataset is on another site, 「当サイトの利用規約が優先する」 for use of this
  site. **No prescribed 出典 form**: CC BY 4.0's own attribution (each
  dataset's title, 長崎市, the licence link, the URL, and that it was
  processed). **MUST NOT** use the city's logo alone without asking. **Cost**:
  第5条 (claims from the user's own breach, at the user's cost): the
  fault-based class accepted for all of Japan.
- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, re-read 2026-10-02:
  `「食品衛生申請等システム」（厚生労働省）（<page URL>）を加工して作成` and who
  processed it; no completeness claim; the minor open point 免責 2) ウ stands.
- **The city's current list (`64426.xlsx`) — NOT PERMITTED without
  permission.** The site default (`https://www.city.nagasaki.lg.jp/page/3214.html`):
  「…著作権法上認められた場合を除き、無断で転用・引用することはできません。」 The
  list page declares no licence of its own. Confirmed as the screen read it.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **N03**: CC BY 4.0, never drawn.

## Privacy

Read only `施設名称`, `営業の種類`, `業態`, `業務種別` / `業態等` and the
address. **Never select** `施設電話番号`, `連絡先メールアドレス`, `連絡先FormURL`,
`法人名`, `法人番号`, `郵便番号`, or MHLW's `法人名` / `法人住所` / phones. The
name rule has no column to read (above). Run `check_personal_exposure.py`
with `japan=True`.

## Region

Japan sub-region (minor tier, above). Project to **UTM 52N (EPSG:32652)**.

## Open items

- ✅ **`mode`: `tram` (owner, 2026-10-02).** JR Nagasaki 5 stations against the tram's 38. The owner's rule (2026-10-02): Dublin's precedent, so commuter rail drawn beside a tram does not make a city `metro`, "unless there is substantial JR, JR reads as metro". Staging read substantial as JR being the city's largest rail network by stations inside the city line..
- ✅ **Which shape: DECIDED (b) (owner, 2026-10-02: "nagasaki b").** Staging
  recommended **(b)**, Tokyo's precedent (Five rules: "A frozen part may sit beside a
  current whole", Kōtō, Chūō and Shinjuku, owner's call at build):
  - **(a) The 2023 snapshot alone**: three buckets, Food service 3,389,
    Retail 1,093, Personal services 1,641; the page states **2023-06-30**
    (food) and **2023-03-31** (personal services). Simplest; the oldest page
    on the Japanese map.
  - **(b) The snapshot plus MHLW's current filings**: adds the 889 addressed
    food-service premises permitted since 2023-07 (less renewals,
    `SUPERSEDES`), and the ADDRESS_BY_CONSENT bullet ("about one restaurant
    in <n> chose not to publish its address"). Personal services stay at
    2023-03-31.
  - **(c) Ask the city for its current lists** (outreach; the owner's, the
    last resort): the 2026-06 food list joins at 91.2% block. Its download,
    for that measurement only, was approved after the fact (owner,
    2026-10-02); it is not a source.
- ✅ **Correct the master list row** (done by staging, 2026-10-02) (Band A stays on the Five rules: CC BY,
  placeable, inside the ceiling): no coordinates; dated 2023-06-30 / 2023-03-31,
  not 2025-03; 38 tram stops, not about 41.
- ⚠️ **The name rule cannot run** (no individual operator column); the page
  carries the MHLW-style bullet for every list.
- ⚠️ **The Economic Census join control** at build: the 2021 census holds
  **1,873** 飲食店 establishments in 42201; the snapshot's 3,389 food-service
  rows are **about 1.8 per establishment**, Hiroshima's 1.80.
- ⚠️ The chōme tier (9-12%): read the misses. Gate 3 against the operator's
  stop list; tram labels; OSM `name:en`.

```brief-checks
[
  {
    "id": "nagasaki-bodik-food-live",
    "claim": "Nagasaki's BODIK food_all CSV (the 2023-06-30 snapshot) is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/4d70b9d1-9885-4045-9f59-9d1b99e02910/resource/1125a70b-ac9d-49f6-ba87-1011d0db4f1a/download/422011_food_business_all.csv",
    "min_bytes": 1000000
  },
  {
    "id": "nagasaki-bodik-food-rows",
    "claim": "The food_all resource holds 6,138 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "1125a70b-ac9d-49f6-ba87-1011d0db4f1a",
    "expect": 6138
  },
  {
    "id": "nagasaki-bodik-food-not-updated",
    "claim": "The dataset is CC BY 4.0 and still the 2025-03-27 upload: a newer copy would change this (the one-clock rule)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=422011_food_business_all",
    "present": ["cc-by-40-intl", "\"metadata_modified\": \"2025-03-27"]
  },
  {
    "id": "nagasaki-bodik-barber-live",
    "claim": "Nagasaki's barber list on BODIK is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/ab4e452b-c72a-49f4-9b25-0379893cce3f/resource/6ccea115-9386-462c-b581-d1d959f16744/download/422011_riyosho_all.csv",
    "min_bytes": 30000
  },
  {
    "id": "nagasaki-bodik-beauty-live",
    "claim": "Nagasaki's beauty-salon list on BODIK is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/9508163b-44a6-4356-abb3-b631b1e4ef72/resource/7d5b0ea8-048e-4534-a8ed-bf9f772c958f/download/422011_biyosho_all.csv",
    "min_bytes": 90000
  },
  {
    "id": "nagasaki-bodik-laundry-live",
    "claim": "Nagasaki's laundry list on BODIK is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/ea649bea-a49f-4ddc-b1a1-2f55f6f6e8c0/resource/fb933c7e-f41a-4b52-8582-039390d66865/download/422011_cleners_all.csv",
    "min_bytes": 30000
  },
  {
    "id": "nagasaki-catalogue-terms-ccby",
    "claim": "The city's open-data terms on its BODIK catalogue apply CC BY 4.0 International",
    "kind": "http_contains",
    "url": "https://odcs.bodik.jp/422011/tos/",
    "present": ["長崎市オープンデータ利用規約", "表示4.0国際"]
  },
  {
    "id": "nagasaki-site-default-reserved",
    "claim": "The city's own list page still links the 2026-06 file and carries no Creative Commons licence (ASCII only: the city's pages declare no charset this check reads; the site default is quoted in the brief)",
    "kind": "http_contains",
    "url": "https://www.city.nagasaki.lg.jp/page/6755.html",
    "present": ["uploaded/attachment/64426.xlsx"],
    "absent": ["creativecommons.org"]
  },
  {
    "id": "nagasaki-mhlw-live",
    "claim": "MHLW's open-data file for Nagasaki City (42201) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=42201_food_business_all.csv",
    "min_bytes": 1500000
  },
  {
    "id": "nagasaki-mhlw-terms-pdl",
    "claim": "MHLW's system site applies PDL 1.0 (ASCII only: the page's Japanese text is not matchable by this check)",
    "kind": "http_contains",
    "url": "https://i2fas.mhlw.go.jp/termsofuse.htm",
    "present": ["PDL1.0"]
  },
  {
    "id": "nagasaki-isj-live",
    "claim": "MLIT's block-level address file for Nagasaki City (42201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/42201-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "nagasaki-projected-crs",
    "claim": "Nagasaki projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 129.87,
    "expect": "EPSG:32652"
  }
]
```
