# Okayama — build brief

**Step 0 measured 2026-10-02.** Run `python scripts/brief_check.py okayama`
before writing any code. Coordinates: the `address-join` skill, measured with
`japan_register.py`'s own functions from a scratch config (the shared
`scripts/screen_japan_join.py` table was not edited). Build with the
`japan-city` skill.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls):** (1) **the Shinkansen does not count** (2026-09-24); (2)
**lines served only by limited expresses count** (2026-09-28); (3) **the city
line only**: only stations inside the city get rings, a one-station stub stays
as cut, and an URBAN line cut to a stub goes back to the owner (2026-09-24,
2026-09-27); (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule** where
an operator column exists (2026-09-27; MHLW's rows have none, below); (6) **no
page says "currently operating"**. Fault-based cost clauses are accepted for
all of Japan (2026-09-24).

**✅ Minor label tier (owner, 2026-10-02):** Okayama carries
`label_tier: "minor"`, in a Japan sub-region per the `japan-city` skill's
standing calls (one region or a split, decided by `check_macro_labels.py`;
every Japanese city moves into it; `REGION_LABELS_ALSO["East Asia"]` gains
it). The eight built Japanese cities stay eligible for pills.

---

## The one-line summary

**Food only, from ONE source: MHLW's 食品衛生申請等システム open data for
Okayama City (7,582 open restaurant permits, 90% of the 8,409 in force), of
which 5,606 (73.9%) publish an address.** Set aside 581 addressed rows
licensed 市内一円 (vehicles and stalls) and 5,025 fixed premises remain, every
one placed (block 93.1%, the rest at chōme or MHLW's own point). **Band B,
food only, confirmed** (Hiroshima's page, with no city list beside it). The
city's own food lists stop at 2021-05 and point to MHLW; its personal-services
lists are PDFs under the site's all-rights-reserved default.

---

## Business leg — MHLW's open data, alone

| | MHLW open data (33100) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=33100_food_business_all.csv`: **4,390,195 B, 12,335 rows** (許可 9,221, 届出 3,082, 許可(廃業) 25, 届出(廃業) 7). UTF-8 CSV. Same bytes as the 2026-10-01 screen |
| As of / cadence | Permits to **2026-08-28**; closures dated 2026-08-01 .. 08-31 only (MHLW keeps a closure about a month). MHLW refreshes monthly ("前月までに公開された…情報") |
| What it holds | Every permit and notification since 2021-06-01 that the city entered; **each field published only with the filer's consent**, so an address or a name can be blank |
| Columns | 自治体コード, 行番号, 都道府県名, 市区町村名, **営業施設名称、屋号又は商号**, …（フリガナ）, **営業の種類**, **業態**, **営業施設所在地**, 営業施設方書, **緯度, 経度**, 営業施設電話番号, 法人名, 法人番号, 法人住所, 許可番号, 初回許可年月日, 許可年月日, 許可開始日, 許可満了日, 廃業年月日, 申請区分, 許可条件, 備考 |
| Operator column | **None for an individual**: 法人名 is a company's. `OPERATOR_COLS` has nothing to compare, so the name rule cannot run (Fukuoka's precedent for MHLW rows) |

**Counts that matter** (open rows):

| Bucket | Types | Rows |
|---|---|---|
| Food service | ① 飲食店営業 (permits) | **7,582** = 90% of e-Stat's FY2024 in force (**8,409**); 5,606 with an address, 5,605 with MHLW's point, 5,778 with a trade name |
| Food retail (permits) | ⑪ 菓子製造業 680, ③ 食肉販売業 207, ④ 魚介類販売業 177, ㉕ そうざい製造業 170 | 1,234 |
| Food retail (notifications, partial and opt-in) | 届出: konbini, supermarkets, greengrocers, packaged meat and fish | 3,082 open, **2,058 with an address** |
| Personal services | none usable (below) | 0 |

- **First-permit years of the open restaurants**: 2021 704 · 2022 1,529 · 2023
  1,461 · 2024 1,325 · 2025 1,405 · 2026 1,158. Unlike Hiroshima's, Okayama's
  entries did not fall away after 2023: the city appears to enter every new
  permit.
- **What is missing**: permits from before 2021-06 still in force (the gap to
  8,409, about 827), which the city published only as PDFs to 2021-05
  (`/kurashi/0000016508.html`: 令和2年度 to 2021-03, then monthly to 2021-05).
- ⚠️ **Not a premises**: 581 addressed restaurants are licensed `…一円`
  (caught by `permits_from_rows`); 業態 marks 338 addressed and 145 unaddressed
  as vehicles or stalls (キッチンカー, 移動, 屋台), for `FORM_RULES`.
- **Placement against the bar**: 73.9% of open restaurant permits carry an
  address (the screen's measure); on fixed premises only (every 一円 row and
  every vehicle or stall 業態 set aside), **5,023 of 6,854, 73.3%**. Both
  clear the reduced-bucket bar's ~70%, narrowly.
- **One premises, several permits**: 5,025 fixed addressed restaurants are
  4,948 distinct (address, trade name) pairs.
- **Personal services: none usable.** 理容所 / 美容所 (`/kurashi/0000019715.html`)
  and クリーニング所 (`/kurashi/0000042557.html`) are full lists at 2026-03-31
  plus this year's new ones, **as PDFs only**, under the city's default terms
  (below).

## Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files for the **4 wards** (33101 北, 33102 中, 33103 東, 33104 南): block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/<code>-24.0a.zip` (66,725 block
keys) and town-chōme `…/19.0b/<code>-19.0b.zip` (786). MHLW's addresses name
the ward (`岡山市北区…`), so the shared parser finds it on every row.

| Tier | MHLW restaurants, addressed and fixed (5,025) |
|---|---|
| Block | **93.1%** |
| Town-chōme / 大字 centroid | 6.8% |
| Unplaced | 0.1% (5: 穝 and 穝東町 3, 幸町2丁目 1, and 下石井ニ丁目 with a katakana ニ) |
| **Block or MHLW's own point** (`OWN_POINT_FALLBACK`) | **100%** |

By ward, block: 北 95.0% (3,662), 南 93.7% (585), 東 84.4% (334), 中 83.6% (444).

**Independent check**: MHLW's own coordinates against the block point,
**median 39 m, 97.7% within 250 m** (4,678 rows; 19 over 1 km).

## 🚇 Rail — MLIT N02 cut at the N03 city line

Read from N02-25 (N02-24 gives the same stations), cut at N03's union of the
four wards (extent S 34.519, W 133.740, N 34.949, E 134.123). **49 stations
inside** (N02_005g groups; widest 岡山, 78 m). **The Shinkansen's 岡山** is
dropped; 岡山 stays as a JR station.

| Operator | N02 line | Inside / N02 total | Stations inside |
|---|---|---|---|
| 岡山電気軌道 | 東山本線 | 10 / 10 | 岡山駅前 … 東山・おかでんミュージアム |
| 岡山電気軌道 | 清輝橋線 | 7 / 7 | 柳川 … 清輝橋 |
| 西日本旅客鉄道 | 山陽線 | 9 / 131 | 瀬戸, 万富, 上道, 東岡山, 高島, 岡山, 北長瀬, 庭瀬, 西川原 |
| 西日本旅客鉄道 | 赤穂線 | 3 / 19 | 東岡山, 大多羅, 西大寺 |
| 西日本旅客鉄道 | 吉備線 | 7 / 10 | 岡山 … 足守 (3 beyond, in Sōja) |
| 西日本旅客鉄道 | 津山線 | 9 / 17 | 岡山 … 福渡 (8 beyond) |
| 西日本旅客鉄道 | 宇野線 | 8 / 15 | 岡山 … 彦崎 (茶屋町 and beyond in Kurashiki and Tamano) |
| 西日本旅客鉄道 | 本四備讃線 | **1 / 5** | 植松 |

- **Okaden is 16 distinct stops** (柳川 shared). The operator runs it as two
  routes from 岡山駅前: 東山線 and 清輝橋線 (the 清輝橋 route uses 東山本線 to
  柳川).
- **Stub test**: 本四備讃線 is cut to **one station** (植松), and by the
  standing call it stays as cut. ⚠️ But it is not a line the public knows by
  that name: the 瀬戸大橋線 service runs 岡山 → 茶屋町 on 宇野線, then 本四備讃線;
  N02 files 宇野線 whole (the 宇野みなと線 beyond 茶屋町 included). Build
  `config.LINES` from `stub_test()`'s table with a `route` or `BRANCHES`
  (trap 3); if 瀬戸大橋線 becomes one public line, 植松 is no longer a stub.
- ⚠️ **Watch item**: Okaden's tracks into the station plaza (about 0.1 km,
  the 岡山駅前 stop moving) are reported for March 2027. Neither N02 edition
  has them; a build after that date needs a newer N02 or a cited override.
- ⚠️ **Gate 3**: Okaden's own stop counts were not read at Step 0; read them
  from the operator at build.
- ⚠️ **OSM `name:en`**: not queried (no Overpass at Step 0). At build: one
  station query and one `railway=tram_stop` query (`TRAM_OSM_JSON`) in the N03
  box above. Okaden's long names (`西大寺町・岡山芸術創造劇場ハレノワ前`) need a
  readable English form; any override is cited.

## Scope

**Okayama City (4 wards).** Every JR line runs on into neighboring
municipalities (倉敷, 総社 and 玉野 among them); their stations are excluded and
named by N03 municipality at build.

## Licences — read 2026-10-02

- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as recorded in
  `docs/data_sources/japan.md` (site terms `https://i2fas.mhlw.go.jp/termsofuse.htm`
  §2). **MUST DISPLAY**: `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; link the top page only. **MUST NOT**: present it as
  MHLW's own; MHLW's logo; claim completeness (the fields are opt-in) or
  accuracy. Cost 免責 1) エ, accepted; 免責 2) ウ (commercial reuse) the minor
  open point, fine while the site is non-commercial.
- **Okayama City's own pages — NOT PERMITTED without permission** (not used):
  the copyright page (`https://www.city.okayama.jp/0000016716.html`) is the
  default, 「…著作権法上認められた場合を除き、無断で複製・転用することはできない」,
  with permission sought from the page's section. The food and
  personal-services pages carry no licence of their own. Sendai's position.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**:
  CC BY 4.0, picks stations, ⛔ never drawn.

## Privacy

MHLW's file carries **法人名, 法人番号, 法人住所 and 営業施設電話番号**: never
selected. No individual's name is published, so the name rule has nothing to
compare (MHLW's FAQ lets a sole trader file their own name as 屋号; that
residual is the reason for the open item below). Run
`check_personal_exposure.py` with `japan=True`.

## Region

`"region": "East Asia"` until the Japan sub-region lands (minor tier, above).
Project to **UTM 53N (EPSG:32653)**.

## Open items

- ✅ **`mode`: `metro` (owner, 2026-10-02).** JR about 33 stations on six lines against Okaden's 16: JR is the backbone. The owner's rule (2026-10-02): Dublin's precedent, so commuter rail drawn beside a tram does not make a city `metro`, "unless there is substantial JR, JR reads as metro". Staging read substantial as JR being the city's largest rail network by stations inside the city line..
- ✅ **A whole city without the name rule: DECIDED, the precedent extends
  (owner, 2026-10-02, "approve all recommendations").** Fukuoka's and Hiroshima's MHLW
  rows were accepted without it beside a city list that had it; here MHLW is
  the only source, so no pin can be checked. The page bullet would be
  Hiroshima's MHLW wording ("the ministry's list does not say who the operator
  is, so this cannot be checked"), applied to the whole page.
- ⚠️ **Placement sits near the bar**: 73.9% addressed, 73.3% on fixed premises.
  The page states the share ("About one restaurant in four … chose not to
  publish its address"), Hiroshima's wording.
- ⚠️ Notifications as a partial food-retail bucket (Fukuoka, Hiroshima):
  2,058 addressed; disclosed as partial.
- ⚠️ **Economic Census join control** (`scripts/japan_census_control.py`): the
  2021 census counts **3,017** 飲食店 establishments in 33100 (北 2,221, 中
  243, 東 205, 南 348); 4,948 distinct placed premises is **1.64 per
  establishment**, inside the built cities' 1.56–1.92. Run it per ward at
  build (中 and 東 have the lowest block rates).
- ⚠️ 本四備讃線 / 瀬戸大橋線 (above), the March 2027 station-plaza tracks, gate 3,
  OSM names.

```brief-checks
[
  {
    "id": "okayama-mhlw-live",
    "claim": "MHLW's open-data file for Okayama City (33100) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=33100_food_business_all.csv",
    "min_bytes": 3000000
  },
  {
    "id": "okayama-own-food-points-to-mhlw",
    "claim": "The city's food-permit page sends readers to MHLW's system, and its own lists stop at May 2021 (PDFs)",
    "kind": "http_contains",
    "url": "https://www.city.okayama.jp/kurashi/0000016508.html",
    "present": ["i2fas.mhlw.go.jp", "betten5gatsu.pdf"]
  },
  {
    "id": "okayama-personal-lists-pdf",
    "claim": "The city's barber and beauty lists (2026-03-31) are PDFs",
    "kind": "http_contains",
    "url": "https://www.city.okayama.jp/kurashi/0000019715.html",
    "present": ["R7riyou.pdf", "R7biyou.pdf"]
  },
  {
    "id": "okayama-isj-kita-live",
    "claim": "MLIT's block-level address file for Kita ward (33101) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/33101-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "okayama-projected-crs",
    "claim": "Okayama projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 133.92,
    "expect": "EPSG:32653"
  }
]
```
