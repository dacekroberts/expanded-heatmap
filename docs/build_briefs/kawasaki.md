# Kawasaki — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live). Run `python scripts/brief_check.py kawasaki` before writing any code.
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

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Kawasaki
carries `label_tier: "minor"` and joins the Japan sub-region the 2026-10-01
batch creates (one region or a split, by `check_macro_labels.py`).

**✅ `mode`: `metro`.** By the owner's rule (2026-10-02): JR East is the
city's largest rail network by stations inside the city line (25 groups,
against Odakyū 11, Tōkyū 10, Keikyū 8, Keiō 2).

---

## The one-line summary

**All three buckets from the city's own monthly CC BY lists: every food permit
in force at 2026-08-31 (14,022 rows; 12,266 restaurant rows, 101.6% of the
official 12,073), and full barber, beauty and laundry lists (2,854 rows).**
The block join places 98.7% of fixed food premises and 98.7-99.1% of the
registers. Rail: 53 station groups on JR East and four private railways, every
line a radial cut by a long, narrow city. Kawasaki sits between built Tokyo and
built Yokohama. **Band A.** MHLW's file is opt-in here (10% of the official
count) and is used only as a control.

---

## Business leg — the city's own lists (`www.city.kawasaki.jp`)

Published by 健康福祉局保健医療政策部生活衛生課 on two pages, each with a CC
licence block (below). No catalogue API: the checks are `http_ok` and
`http_contains`.

| | Food (食品営業許可施設一覧) | Barbers (理容所一覧) | Beauty (美容所一覧) | Laundries (クリーニング所一覧) |
|---|---|---|---|---|
| **Page** | `https://www.city.kawasaki.jp/350/page/0000093741.html` (updated 2026-09-09) | `https://www.city.kawasaki.jp/350/page/0000120745.html` (updated 2026-09-14) | same | same |
| **File** | `https://www.city.kawasaki.jp/350/cmsfiles/contents/0000093/93741/080803(UTF-8).csv`: **2,846,254 B** | `…/cmsfiles/contents/0000120/120745/01riyoujo202608.csv`: **93,757 B** | `…/120745/02biyoujo202608.csv`: **394,980 B** | `…/120745/03cleaning202608.csv`: **129,147 B** |
| Rows | **14,022** | **558** | **1,763** | **533** (取次店 354, 一般 170, リネンサプライ 9) |
| As of | **2026-08-31** (「令和8年8月末時点」; the page: 前月末において許可を取得している施設) | 2026-08-31 | 2026-08-31 | 2026-08-31 |
| Cadence | monthly; the file is RENAMED each month (`080803` = R8, month 08) | monthly, by the 15th; renamed (`…202608`) | monthly | monthly |
| Encoding | UTF-8 with BOM, comma CSV | UTF-8 with BOM | UTF-8 with BOM | UTF-8 with BOM |
| Columns | **営業所の名称**, **営業所の所在地**, 営業所の所在地方書, 営業所の電話番号, 営業者氏名（法人のみ）, 代表者役職（法人のみ）, 代表者氏名（法人のみ）, 営業者住所（法人のみ）, 営業者住所方書（法人のみ）, 許可番号, 許可年月日, **営業種目** | **施設名称**, **施設所在地**, 施設方書, 施設電話番号, 確認日, 確認番号, 開設者名, 代表者名, **開設者住所**, 開設者方書, 営業所面積 | as barbers | as barbers, with 営業者名 / 代表者名 / **営業者住所** / 営業者方書, and **施設（種別）** |

The page also lists twelve monthly new-permit files (2025-09 to 2026-08); the
full list makes them unnecessary.

**Counts that matter** (`japan_eigyo` with the respelling below):

| Bucket | Rows (fixed, addressed) |
|---|---|
| Food service | **8,195** (restaurant 8,180, café 15) |
| Food retail (permit types) | **1,294**: 菓子 651, 魚介類販売 266, 食肉販売 207, そうざい 170 |
| Personal services | **2,845**: barbers 558, beauty 1,763, laundries 524 (リネンサプライ 9 out) |
| Out (fixed) | institutional catering 621, 仕出し 155, inside accommodation 53, vending 44, manufacturing ("no rule") 256 |

- **Restaurants against the official count**: 12,266 飲食店 rows against
  e-Stat's FY2024 in force **12,073** (`japan_official.restaurants`): **101.6%**.
- **Not a premises**: 2,454 restaurant rows are 屋台型臨時営業 (1,389) or
  自動車 (1,065). The page says their address is blank by design (licensed for
  all of Kanagawa since 2021-06), and every one is blank, so
  `permits_from_rows` sets them aside as `mobile`.
- **Withheld addresses**: 798 fixed restaurant rows carry no address
  (「令和3年6月1日以降…申請者の希望により一部、非公開」). On fixed premises,
  **9,014 of 9,812 restaurants (91.9%) publish an address.**
- **One premises, several permits**: 8,195 fixed Food service rows are 8,063
  distinct (address, trade name) pairs.

### MHLW's file — a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=14130_food_business_all.csv`:
**2,061,002 B, 5,509 rows** (届出 4,001, 許可 1,439, 届出(廃業) 44, 許可(廃業)
25), newest 許可年月日 2026-08-31. **1,207 open restaurant permits, 10.0% of
the official count** (opt-in), 961 with an address. **83.8% of MHLW's
block-tier named restaurant permits (753 of 899) are in the city's list** with
the same ward, town, block and trade name. The city's list is the food source
(Toyama's shape); leave MHLW's notifications out and say so in the page's
standing bullet (Toyama's precedent).

### Against the shared code (Phase 1 is on master; what is still missing)

- ⚠️ **`TYPE_COLS` lacks 営業種目**: without it every food row reads type ""
  and nothing reaches a bucket. Add it.
- ⚠️ **`japan_eigyo` does not read Kawasaki's spelling 飲食店（sub-type）**
  (`飲食店（一般食堂）` 3,577, `飲食店（大衆酒場）` 989, …): today 0 restaurants
  bucket. Measured here with a scratch respelling to 飲食店営業（…）; at build,
  a RULES pattern `^飲食店\(` with these carve-outs above it:
  `飲食店（給食施設）` 153 and `飲食店（学校給食炊飯）` 3 (institutional:
  `^給食` misses them), `飲食店（まあじゃん屋等）` 16 (entertainment: `麻雀`
  misses the kana), `飲食店（短期営業）` 4 (temporary). Already caught:
  屋台型臨時営業, 自動車, 集団給食施設, 旅館飲食店, 仕出し屋, 屋形船, キャバレー.
- ⚠️ **`飲食店（そうざい店）` (301) and `飲食店（弁当屋）` (528)**: a deli and a
  bento shop on a restaurant permit. The existing deli rule takes `そう菜店` to
  Retail, so the precedent puts `そうざい店` in Retail; 弁当屋 has no rule and
  stays Food service. Measured above as Food service (both); a
  `docs/category_rules.md` read at build.
- `ADDR_COLS` (営業所の所在地, 施設所在地), `NAME_COLS` (営業所の名称,
  施設名称) and the laundry kind (施設（種別）) are already covered.
- `OPERATOR_COLS`: the registers' 開設者名, 代表者名 and 営業者名 and the food
  list's 代表者氏名（法人のみ） are covered; add **営業者氏名（法人のみ）** for
  completeness (companies only).
- Reuses unchanged: the join, `OWN_POINT_FALLBACK` is not needed (block 98.7%),
  N02-25, the ward parse (seven wards; not ward-less).

### The name rule

- **The food list publishes operators' names for companies only** (「個人事業主の
  営業者氏名及び営業者住所は公開しません」): the name rule flags **0** food rows
  and cannot see a sole trader. This is Toyama's position, accepted by the
  owner (2026-10-02): the page carries the MHLW-style bullet for the food
  layer.
- **The registers name every operator** (開設者名 on all 558 barber and 1,763
  beauty rows; 営業者名 on all laundry rows): the rule runs and flags **0**
  barber, beauty or laundry rows (measured in memory).

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files for the **7 wards** (14131 川崎, 14132 幸, 14133 中原, 14134 高津,
14135 多摩, 14136 宮前, 14137 麻生): block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/<code>-24.0a.zip` and town-chōme
`…/19.0b/<code>-19.0b.zip`. 31,607 block keys, 673 town-chōme. The lists'
addresses name the ward (川崎市川崎区…), so the shared parser finds it.

| Tier | Food, fixed in a bucket (9,489) | Barbers (558) | Beauty (1,763) | Laundries (524) |
|---|---|---|---|---|
| Block | **98.7%** | **99.1%** | **99.1%** | **98.7%** |
| Town-chōme / 大字 centroid | 1.3% | 0.9% | 0.8% | 1.3% |
| Unplaced | 0.0% (1) | 0.0% | 0.1% | 0.0% |

Food by ward, block: 川崎 99.8% (2,951), 幸 97.7% (980), 中原 95.7% (1,961),
高津 99.7% (1,178), 多摩 99.3% (1,082), 宮前 100.0% (750), 麻生 99.7% (587).

**Independent check**: for the 753 restaurants in both lists, the city row's
block point against MHLW's own coordinates: **median 38 m, 96.1% within
250 m**. MHLW's own rows against their block point: median 41 m (2,152 rows).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_14_GML.zip` (the
shared cache), the 7 wards above (142.9 km²; extent S 35.470, W 139.449,
N 35.643, E 139.836). **60 station records, 53 `N02_005g` groups.** No
Shinkansen station inside (the Tōkaidō Shinkansen passes through without one).
Median gap to the nearest station group **683 m**.

| Operator | N02 line | Inside / N02 total | Stations inside |
|---|---|---|---|
| 東日本旅客鉄道 | 南武線 | **19 / 30** | 川崎 … 登戸, 稲田堤 (and the branch 尻手–浜川崎: 八丁畷, 川崎新町, 小田栄, 浜川崎) |
| 東日本旅客鉄道 | 鶴見線 | 5 / 14 | 武蔵白石, 浜川崎, 昭和, 扇町, 大川 |
| 東日本旅客鉄道 | 東海道線 | 3 / 46 | 川崎, 新川崎, 武蔵小杉 |
| 京浜急行電鉄 | 大師線 | **7 / 7** | 京急川崎 … 小島新田 |
| 京浜急行電鉄 | 本線 | **2 / 50** | 京急川崎, 八丁畷 |
| 東急電鉄 | 東横線 | 3 / 22 | 新丸子, 武蔵小杉, 元住吉 |
| 東急電鉄 | 田園都市線 | 7 / 27 | 二子新地, 高津, 溝の口, 梶が谷, 宮崎台, 宮前平, 鷺沼 |
| 小田急電鉄 | 小田原線 | 7 / 47 | 登戸, 向ヶ丘遊園, 生田, 読売ランド前, 百合ヶ丘, 新百合ヶ丘, 柿生 |
| 小田急電鉄 | 多摩線 | 5 / 8 | 新百合ヶ丘, 五月台, 栗平, 黒川, はるひ野 |
| 京王電鉄 | 相模原線 | **2 / 12** | 京王稲田堤, 若葉台 |

- **Groups by operator**: JR East 25, Odakyū 11, Tōkyū 10, Keikyū 8, Keiō 2.
- **A line a radial cut**: the city is a strip along the Tama River, so every
  private line crosses it briefly. **Keikyū Main (2 of 50) and Keiō
  Sagamihara (2 of 12)** are urban lines cut to two stations (see 🚨 below).
  No line is cut to one station.
- ⚠️ **武蔵小杉 is two N02 groups 377 m apart**: JR Nambu with Tōkyū (104 m
  wide), and JR's 東海道線 (Yokosuka Line) platform. One station by name and
  by passage: Tokyo's `GROUP_JOIN` (Keiyō platforms, 424 m) joins them.
- ⚠️ **Services over N02's legal lines (trap 2, Tokyo's `route`)**: N02's
  東海道線 here is the 品鶴線 freight-passenger line (新川崎, 武蔵小杉: the JR
  Yokosuka and Shōnan-Shinjuku Lines, and the Sōtetsu through service) plus
  川崎 on the Tōkaidō and Keihin-Tōhoku Lines. **Yokohama built these as four
  routes over 東海道線; reuse its definitions.** Tōkyū's Meguro Line runs
  over 東横線 (新丸子, 武蔵小杉, 元住吉) and its Ōimachi Line over 田園都市線
  (二子新地, 高津, 溝の口): routes, or a page bullet.
- ⚠️ **Branches (trap 3)**: the 南武支線 (尻手–浜川崎, publicly the Nambu
  Branch Line) hides inside 南武線, and 鶴見線's 大川 branch (武蔵白石–大川)
  inside 鶴見線: `BRANCHES`.
- ⚠️ **Gate 3**: the operators' own station counts were not read at Step 0;
  read them at build (JR East, Keikyū, Tōkyū, Odakyū, Keiō).
- ⚠️ **OSM `name:en`**: not queried (no Overpass at Step 0). One station query
  in the N03 box above at build; no tram stops.

## Scope

**Kawasaki City (7 wards).** Every line runs on into Tokyo (大田, 世田谷,
狛江, 稲城, 町田) or Yokohama; their stations are excluded and named by N03
municipality at build. Yokohama is built: its rings stop at its own line.

## Licences — read 2026-10-02

- **Kawasaki City's lists — PERMITTED WITH CONDITIONS (CC BY).** The grant:
  川崎市オープンデータ利用規約 (`https://www.city.kawasaki.jp/170/cmsfiles/contents/0000057/57493/kawasakiod_rules.pdf`)
  §2, 「本サイトのデータの著作権は、注があるものを除いて、クリエイティブ・コモンズ・ライセンス
  表示 2.1 のもとでライセンスされています」, and both datasets are in the city's
  open-data catalogue (`dataset20250930.csv`: 食品営業許可施設一覧 and
  環境衛生関係営業に関する情報). The file pages' badge links CC BY **4.0**; the
  規約 and the policy page (`/170/page/0000057493.html`) say **2.1 JP**. Both
  are CC BY, so reuse is permitted either way (the version question is 🚨
  below).
  - **MUST DISPLAY** (the 規約's form for modified use):
    `この地図は以下の著作物を改変して利用しています。食品営業許可施設一覧、川崎市、クリエイティブ・コモンズ・ライセンス 表示 2.1（http://creativecommons.org/licenses/by/2.1/jp/）`
    and likewise `環境衛生関係営業に関する情報、川崎市、…`. A link on the licence
    name may replace the printed URL.
  - **MUST NOT**: imply endorsement (CC). No logo clause; no accuracy or
    completeness claim (§3①).
  - **Cost** (§3③): claims from the user's breach or a third party's rights
    are settled 「利用者自身の責任と利用者の費用負担で」. The fault-based class,
    ✅ accepted for every Japanese source (2026-09-24). Japanese law, Yokohama
    District Court.
  - The site footer's all-rights-reserved and the site policy cover web
    content, not catalogue data.
- **MHLW open data** (control only): PDL 1.0, as recorded in
  `docs/data_sources/japan.md`; no notice needed unless a row or point is used.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**:
  CC BY 4.0, picks stations, ⛔ never drawn.

## Privacy

Read only 営業所の名称 / 施設名称, 営業種目 / 施設（種別） and the premises
address. **開設者住所 and 営業者住所 in the registers are operators' own
addresses, individuals included: never select them**; the food list's
営業者住所（法人のみ） and every 電話番号 likewise. 開設者名 / 営業者名 / 代表者名
are read in memory by the name rule only. Run `check_personal_exposure.py`
with `japan=True`. No row value was printed for this brief.

## Region

The Japan sub-region (minor tier, above); `"country": "Japan"`. Project to
**UTM 54N (EPSG:32654)**.

## Open items

- 🚨 **Two urban lines cut to two stations: Keikyū Main (京急川崎, 八丁畷) and
  Keiō Sagamihara (京王稲田堤, 若葉台)**, with Tōkyū Tōyoko and JR's 東海道線 at
  three. **Recommendation: draw all as cut**, on Sakai's precedent (the
  Midōsuji, 3 of 20, drawn as cut, owner 2026-10-02): the business data stops
  at the city line, and both stations are busy interchanges (京急川崎 with JR
  川崎).
- 🚨 **Which CC BY version the credit names**: the 規約 says 表示 2.1 (JP), the
  files' badge links 4.0. **Recommendation: name both** ("表示 2.1 / 4.0", each
  linked): it meets either reading at no cost. The alternative is one question
  to 40syoku@ / 40seiei@city.kawasaki.jp.
- ⚠️ `TYPE_COLS` + 営業種目, the `飲食店（…）` rule with its four carve-outs, and
  `OPERATOR_COLS` + 営業者氏名（法人のみ） (shared code; each re-runs the Minato
  control).
- ⚠️ `飲食店（そうざい店）` 301 (Retail by the そう菜店 precedent) and
  `飲食店（弁当屋）` 528 (Food service): read `docs/category_rules.md`.
- ⚠️ 武蔵小杉 `GROUP_JOIN` (377 m); Yokohama's four 東海道線 routes reused;
  Tōkyū's Meguro and Ōimachi services; the Nambu and Tsurumi branches; gate 3;
  OSM `name:en`.
- ⚠️ **The files are renamed every month** (`080803(UTF-8).csv`,
  `…202608.csv`): the fetch reads the current link from each page, and the
  checks below pin the 2026-08 editions (update them with the build).
- ⚠️ **Economic Census join control** (`scripts/japan_census_control.py`): the
  2021 census counts **4,212** 飲食店 establishments (川崎 1,168, 幸 463, 中原
  959, 高津 537, 多摩 499, 宮前 302, 麻生 284); 8,063 distinct placed premises is
  **1.91 per establishment**, at the top of the built cities' 1.56–1.92. Run it
  per ward at build (中原 has the lowest block rate).
- ⚠️ The 菓子 / そうざい factory share, printed by step 2.
- Note: Kawasaki (about 1.5 million people) takes the minor tier as decided; its
  pill would sit between Tokyo's and Yokohama's in any case.

```brief-checks
[
  {
    "id": "kawasaki-food-live",
    "claim": "Kawasaki's full food-permit list (as of 2026-08-31, UTF-8 CSV) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kawasaki.jp/350/cmsfiles/contents/0000093/93741/080803(UTF-8).csv",
    "min_bytes": 2000000
  },
  {
    "id": "kawasaki-food-page",
    "claim": "The food page links the 2026-08 full list (080803) under a CC BY 4.0 badge (ASCII only: the page is read without its charset)",
    "kind": "http_contains",
    "url": "https://www.city.kawasaki.jp/350/page/0000093741.html",
    "present": ["080803(UTF-8).csv", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "kawasaki-barber-live",
    "claim": "Kawasaki's barber list (2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kawasaki.jp/350/cmsfiles/contents/0000120/120745/01riyoujo202608.csv",
    "min_bytes": 50000
  },
  {
    "id": "kawasaki-beauty-live",
    "claim": "Kawasaki's beauty-salon list (2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kawasaki.jp/350/cmsfiles/contents/0000120/120745/02biyoujo202608.csv",
    "min_bytes": 200000
  },
  {
    "id": "kawasaki-laundry-live",
    "claim": "Kawasaki's laundry list (2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kawasaki.jp/350/cmsfiles/contents/0000120/120745/03cleaning202608.csv",
    "min_bytes": 60000
  },
  {
    "id": "kawasaki-env-page",
    "claim": "The environmental-hygiene page links the three 2026-08 lists under a CC BY 4.0 badge",
    "kind": "http_contains",
    "url": "https://www.city.kawasaki.jp/350/page/0000120745.html",
    "present": ["01riyoujo202608.csv", "02biyoujo202608.csv", "03cleaning202608.csv", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "kawasaki-od-terms",
    "claim": "The city's open-data page names CC BY 2.1 JP and links the 利用規約 PDF",
    "kind": "http_contains",
    "url": "https://www.city.kawasaki.jp/170/page/0000057493.html",
    "present": ["creativecommons.org/licenses/by/2.1/jp", "kawasakiod_rules.pdf"]
  },
  {
    "id": "kawasaki-mhlw-live",
    "claim": "MHLW's open-data file for Kawasaki (14130) answers a plain keyless GET (the control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=14130_food_business_all.csv",
    "min_bytes": 1000000
  },
  {
    "id": "kawasaki-isj-nakahara-live",
    "claim": "MLIT's block-level address file for Nakahara ward (14133) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/14133-24.0a.zip",
    "min_bytes": 30000
  },
  {
    "id": "kawasaki-projected-crs",
    "claim": "Kawasaki projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.65,
    "expect": "EPSG:32654"
  }
]
```
