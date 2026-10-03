# Chiba — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live). Run `python scripts/brief_check.py chiba` before writing any code.
Coordinates: the `address-join` skill, measured with `japan_register.py`'s own
functions from a scratch script (the shared `scripts/screen_japan_join.py`
table was not edited). Build with the `japan-city` skill. **Okayama's shape**
(`docs/build_briefs/okayama.md`): MHLW's file alone, food only.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls):** (1) **the Shinkansen does not count** (2026-09-24); (2)
**lines served only by limited expresses count** (2026-09-28); (3) **the city
line only**: only stations inside the city get rings, a one-station stub stays
as cut, and an URBAN line cut to a stub goes back to the owner (2026-09-24,
2026-09-27); (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule** where
an operator column exists (MHLW's rows have none; Okayama's precedent, owner
2026-10-02); (6) **no page says "currently operating"**. Fault-based cost
clauses are accepted for all of Japan (2026-09-24).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Chiba
carries `label_tier: "minor"` and joins the Japan sub-region the 2026-10-01
batch creates.

**✅ `mode`: `metro`.** By the owner's rule (2026-10-02): JR East is the
city's largest rail network by stations inside the city line (19 groups,
against the Chiba Urban Monorail's 18 and Keisei's 13).

---

## The one-line summary

**Food only, from ONE source: MHLW's 食品衛生申請等システム open data for
Chiba City (8,290 open restaurant permits, 89.3% of the 9,279 in force), of
which 6,105 (73.6%) publish an address; on fixed premises 74.6%.** Placed at
the block 98.9%. **Band B, food only** (Okayama's page). The city publishes
complete monthly Excel lists of food permits, barbers, beauty salons and
laundries, but **on a page with no open-data grant, under the site's
all-rights-reserved default: not used** (🚨 below). Rail: 47 station groups,
the Chiba Urban Monorail wholly inside, JR East and Keisei cut at the line.

---

## Business leg — MHLW's open data, alone

| | MHLW open data (12100) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=12100_food_business_all.csv`: **5,795,033 B, 14,144 rows** (許可 9,473, 届出 4,635, 許可(廃業) 24, 届出(廃業) 12). UTF-8 CSV |
| As of / cadence | Permits to **2026-08-31**; MHLW refreshes monthly |
| What it holds | Every permit and notification since 2021-06-01 that the city entered; **each field published only with the filer's consent** |
| Columns | the national schema, as Okayama's: 自治体コード, 行番号, 都道府県名, 市区町村名, **営業施設名称、屋号又は商号**, フリガナ, **営業の種類**, **業態**, **営業施設所在地**, 営業施設方書, **緯度, 経度**, 営業施設電話番号, 法人名, 法人番号, 法人住所, 許可番号, 初回許可年月日, 許可年月日, 許可開始日, 許可満了日, 廃業年月日, **申請区分**, 許可条件, 備考 |
| Operator column | **None for an individual** (法人名 is a company's): the name rule cannot run (Okayama's precedent, decided) |

**Counts that matter** (open rows):

| Bucket | Types | Rows |
|---|---|---|
| Food service | ① 飲食店営業 (permits) | **8,290** = 89.3% of e-Stat's FY2024 in force (**9,279**); 6,105 with an address; **only 1,632 with MHLW's point** |
| Food retail (permits) | ⑪ 菓子製造業 500, ④ 魚介類販売業 174, ③ 食肉販売業 157, ㉕ そうざい製造業 156; and restaurant permits whose 業態 is a konbini (351) or supermarket (204) | **1,369** fixed and addressed, after `japan_eigyo` |
| Food retail (notifications, partial and opt-in) | 届出: konbini, supermarkets, greengrocers, packaged meat and fish | 4,635 open, **2,967 with an address** |
| Personal services | none usable (the city's lists are not permitted, below) | 0 |

- **First-permit years of the open restaurants**: 2021 735 · 2022 1,577 · 2023
  1,711 · 2024 1,596 · 2025 1,588 · 2026 1,083. The city enters every new
  permit, not only online filings.
- **What is missing**: the permits from before 2021-06 still in force. The
  city's own list (read here as a COUNT CONTROL only, never as a source) holds
  8,267 new-law restaurant permits, against MHLW's 8,290, and **1,204 old-law
  restaurant permits that MHLW does not have**: the gap to the official count
  is the old law, as in Kitakyushu, but here the old-law list is not usable.
- **Not a premises**: of the 8,290, about 2,250 are licensed `…一円` or carry a
  vehicle or stall 業態. **Chiba licenses festival stalls in bulk**: 1,361
  restaurant permits carry 業態 屋台 (the city's 屋台、露店等での飲食店営業取扱要綱;
  the city list's 許可条件 names 1,409), all without an address.
- **Placement against the bar**: 73.6% of open restaurant permits carry an
  address (the screen's measure); on fixed premises (every 一円 row and every
  vehicle or stall 業態 set aside), **4,505 of 6,038, 74.6%**. Both clear the
  reduced-bucket bar's ~70%.
- **After `japan_eigyo` and `FORM_RULES`**, 3,401 fixed, addressed Food
  service permits: 業態 takes out institutional catering 211, snack bars and
  cabarets 137, hotels 85, karaoke and mahjong 75, temporary 32; and moves
  konbini 351 and supermarkets 204 to Retail.
- **One premises, several permits**: 3,401 are 3,384 distinct (address, trade
  name) pairs.

### Against the shared code

Nothing new: MHLW's national schema is read today (Okayama, Kitakyushu). The
seven wards parse as in every ward city. ⚠️ Two addressed restaurant permits
carry 業態 屋台 and would enter by Fukuoka's yatai rule (a fixed street stall);
in Chiba 屋台 means a festival stall: read the two at build.

## Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files for the **6 wards** (12101 中央, 12102 花見川, 12103 稲毛, 12104
若葉, 12105 緑, 12106 美浜): block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/<code>-24.0a.zip` and town-chōme
`…/19.0b/<code>-19.0b.zip`. 89,163 block keys, 504 town-chōme. MHLW's
addresses name the ward (千葉市中央区…).

| Tier | MHLW permits in a bucket, addressed and fixed (4,770) | Restaurants (3,401) |
|---|---|---|
| Block | **98.8%** | **98.9%** |
| Town-chōme / 大字 centroid | 1.2% | 1.0% |
| Unplaced | 0.0% (2) | 0.1% (2) |
| **Block or MHLW's own point** (`OWN_POINT_FALLBACK`) | | **99.3%** |

Restaurants by ward, block: 中央 99.5% (1,559), 花見川 99.7% (363), 稲毛 99.8%
(405), 若葉 98.8% (344), 緑 98.5% (272), 美浜 96.1% (458). The fallback adds
little here: MHLW carries a point on only 1,632 restaurant permits.

**Independent check**: MHLW's own coordinates against the block point,
**median 46 m, 91.0% within 250 m** (3,360 rows; 6 over 1 km).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

Read from the shared cache (`N02-25_GML.zip`, `N03-20250101_12_GML.zip`), the
6 wards above (271.6 km²; extent S 35.494, W 140.018, N 35.715, E 140.303).
**55 station records, 47 `N02_005g` groups** (widest 千葉, 166 m, four
records). No Shinkansen. Median gap to the nearest station group **621 m**.

| Operator | N02 line | Inside / N02 total | Stations inside |
|---|---|---|---|
| 千葉都市モノレール | 1号線 (class 22) | **6 / 6** | 千葉みなと, 市役所前, 千葉, 栄町, 葭川公園, 県庁前 |
| 千葉都市モノレール | 2号線 (class 22) | **13 / 13** | 千葉 … 千城台 |
| 京成電鉄 | 千葉線 | 9 / 10 | 京成幕張本郷 … 千葉中央 (京成津田沼 beyond, in Narashino) |
| 京成電鉄 | 千原線 | 5 / 6 | 千葉中央, 千葉寺, 大森台, 学園前, おゆみ野 (ちはら台 beyond, in Ichihara) |
| 東日本旅客鉄道 | 総武線 | 8 / 48 | 幕張本郷, 幕張, 新検見川, 稲毛, 西千葉, 千葉, 東千葉, 都賀 |
| 東日本旅客鉄道 | 京葉線 | 6 / 19 | 幕張豊砂, 海浜幕張, 検見川浜, 稲毛海岸, 千葉みなと, 蘇我 |
| 東日本旅客鉄道 | 外房線 | 6 / 27 | 千葉, 本千葉, 蘇我, 鎌取, 誉田, 土気 |
| 東日本旅客鉄道 | 内房線 | **2 / 30** | 蘇我, 浜野 |

- **Groups by operator**: JR East 19, the Monorail 18, Keisei 13.
- **Gate 3**: the Monorail's own station pages list **18** stations (its
  station-information page, 2026-10-02) = N02's 18 groups. JR East and Keisei
  at build.
- **Stub test**: 内房線 keeps 2 (蘇我, shared with the Keiyō and Sotobō
  Lines, and 浜野): a commuter line cut as the city line falls, not a
  one-station stub; drawn as cut by the standing call.
- ⚠️ **Services over N02's legal lines (trap 2, Tokyo's `route`)**: N02's
  総武線 carries both the Chūō-Sōbu local (幕張本郷 … 千葉) and the Sōbu
  Rapid (稲毛, 千葉 …), and beyond 千葉 the Sōbu Main Line (東千葉, 都賀).
  **Tokyo built JR East's 総武線 services as routes; reuse them.** The
  Musashino Line's through trains on the Keiyō Line need no line of their own.
- ⚠️ 幕張豊砂 (opened 2023-03) is in N02-25; check OSM's name at build.
- ⚠️ **OSM `name:en`**: not queried (no Overpass at Step 0). One station query
  in the N03 box at build; the Monorail's stations are railway=station in
  N02 (class 22), so no tram-stop query.

## Scope

**Chiba City (6 wards).** JR and Keisei run on to Narashino, Yotsukaidō,
Ichihara, Ōamishiro and Tōgane; their stations are excluded and named by N03
municipality at build.

## Licences — read 2026-10-02

- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as recorded in
  `docs/data_sources/japan.md` (site terms `https://i2fas.mhlw.go.jp/termsofuse.htm`
  §2). **MUST DISPLAY**: `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; link the top page only. **MUST NOT**: present it as
  MHLW's own; MHLW's logo; claim completeness (the fields are opt-in) or
  accuracy. Cost 免責 1) エ, accepted; 免責 2) ウ the minor open point.
- **Chiba City's 保健所関係台帳・一覧 — NOT PERMITTED without permission** (not
  used). The page (`https://www.city.chiba.jp/somu/somu/seisakuhomu/shisei/hokenjokankei.html`,
  政策法務課市政情報室) states no licence and carries none of the CC BY badges
  the city's open-data pages do. The site default
  (`https://www.city.chiba.jp/front/link_copyright.html`):
  「「私的使用のための複製」や「引用」など著作権法上認められた場合を除き、無断で複製・転用することはできません。」
  The ちばDataポータル terms send data outside the catalogue back to it
  (「オープンデータ以外のデータ　本市ホームページの著作権の取扱いによるものとします」),
  and the catalogue lists none of these files. The city's open-data guideline
  plans release 「原則として」, which is a plan, not a grant. Okayama's and
  Sendai's position. (A list of names, types and addresses may be bare facts
  outside copyright; the project does not resolve that in its own favour.)
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**:
  CC BY 4.0, picks stations, ⛔ never drawn.

## Privacy

MHLW's file carries **法人名, 法人番号, 法人住所 and 営業施設電話番号**: never
selected. The city's workbook (read for the count control only) carries
申請者氏名 and 代表者名: not selected, not kept. Run
`check_personal_exposure.py` with `japan=True`. No row value was printed for
this brief.

## Region

The Japan sub-region (minor tier, above); `"country": "Japan"`. Project to
**UTM 54N (EPSG:32654)**.

## Open items

- 🚨 **The city's own lists are complete and unusable.** Its monthly Excel
  lists (food 2026-08-31: 9,453 new-law and 1,724 old-law rows, every one with
  a split address; barbers 589, beauty 1,766 and laundries 424 at 2026-06-30)
  would make Chiba a three-bucket Band A city, but they sit under the site's
  all-rights-reserved default. **Recommendation: build Band B, food only, on
  MHLW now** (Okayama's precedent; outreach is the last resort), and record
  that one permission request to the page's publisher
  (`seisakuhomu.GEG@city.chiba.lg.jp`) or a catalogue listing would reopen
  three buckets. The owner's call whether to ask.
- ⚠️ **Placement sits near the bar**: 73.6% addressed, 74.6% on fixed
  premises. The page states the share ("About one restaurant in four … chose
  not to publish its address"), Hiroshima's wording.
- ⚠️ **The old-law gap**: 1,204 restaurant permits from before 2021-06 are in
  force but not in MHLW's file (13% of the official count). The page's
  standing bullet covers it as Okayama's does.
- ⚠️ Notifications as a partial food-retail bucket (Fukuoka, Hiroshima,
  Okayama): 2,967 addressed; disclosed as partial.
- ⚠️ **Economic Census join control** (`scripts/japan_census_control.py`): the
  2021 census counts **2,285** 飲食店 establishments (中央 979, 花見川 257, 稲毛
  294, 若葉 274, 緑 189, 美浜 292); 3,384 distinct placed premises is **1.48 per
  establishment, below the built cities' 1.56–1.92** (Okayama 1.64). The
  quarter of permits without an address and the old-law gap account for it in
  direction; run it per ward at build and state the reason before publishing.
- ⚠️ The two addressed 屋台 restaurant permits (Fukuoka's yatai rule); 総武線
  services as Tokyo's routes; gate 3 for JR and Keisei; OSM `name:en`.

```brief-checks
[
  {
    "id": "chiba-mhlw-live",
    "claim": "MHLW's open-data file for Chiba City (12100) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=12100_food_business_all.csv",
    "min_bytes": 4000000
  },
  {
    "id": "chiba-own-lists-exist",
    "claim": "The city's 保健所関係台帳・一覧 page links its own food (2026-08) and barber (2026-06) workbooks - not used: no open-data grant (ASCII markers only)",
    "kind": "http_contains",
    "url": "https://www.city.chiba.jp/somu/somu/seisakuhomu/shisei/hokenjokankei.html",
    "present": ["202608eigyou.xlsx", "r8-1riyou.xlsx", "06r8-1biyou.xlsx", "r8-1clining.xlsx"],
    "absent": ["creativecommons.org"]
  },
  {
    "id": "chiba-monorail-18",
    "claim": "Chiba Urban Monorail's station-information page lists 18 station pages (gate 3 = N02's 18 groups); two stable markers checked",
    "kind": "http_contains",
    "url": "https://chiba-monorail.co.jp/index.php/info-timetable/station-info/",
    "present": ["station-info/chibaminato-station/", "station-info/chishirodai-station/", "station-info/kenchoumae-station/"]
  },
  {
    "id": "chiba-isj-chuo-live",
    "claim": "MLIT's block-level address file for Chūō ward (12101) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12101-24.0a.zip",
    "min_bytes": 80000
  },
  {
    "id": "chiba-projected-crs",
    "claim": "Chiba projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.12,
    "expect": "EPSG:32654"
  }
]
```
