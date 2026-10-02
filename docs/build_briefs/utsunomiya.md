# Utsunomiya — build brief

**Step 0 measured 2026-10-02.** Run `python scripts/brief_check.py utsunomiya`
before writing any code. Coordinates: the `address-join` skill, measured with
the shared `japan_register` functions under this brief's own column mapping
(the shared `scripts/screen_japan_join.py` table was not edited; add
`utsunomiya` and `utsunomiya-mhlw` entries there at the build). Rail: MLIT
N02-25 cut at the N03 city line, measured the same way.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls):** (1) **the Shinkansen does not count** (2026-09-24);
(2) **lines served only by limited expresses DO count** (2026-09-28);
(3) **the city line only**: only stations inside the city get rings, with a
per-line stub test; a one-station stub stays as cut, an URBAN line cut to a
stub goes back to the owner (2026-09-24, 2026-09-27); (4) **菓子製造業 and
そうざい製造業 count, in Retail**, the factory share measured and kept
(2026-09-24, 2026-09-27); (5) **the name rule**: where the trade name IS the
operator's own name, the pin shows its permit type, the operator column read
in memory only (2026-09-27); MHLW's rows cannot take it (no individual
operator column; accepted for Fukuoka, 2026-09-28); (6) **no page says
"currently operating"**. Also: fault-based cost clauses accepted for all of
Japan (2026-09-24); yatai count but a 露店 form is a street stall
(2026-09-28, 2026-09-29); English station names from OSM `name:en`, numerals
as figures before 丁目.

**✅ Minor label tier (owner, 2026-10-02):** Utsunomiya is in the 2026-10-01
Japanese batch and carries `label_tier: "minor"`, with the whole France and
Czechia precedent: a Japan sub-region (one or a split, by
`check_macro_labels.py`, never by eye), every Japanese city moved into it,
and `REGION_LABELS_ALSO["East Asia"]` gaining it. **The eight built Japanese
cities stay eligible.** The first city of the batch makes the change.

---

## The one-line summary

**Fukuoka's two-source shape: MHLW's 食品衛生申請等システム file carries every
permit granted since 2021-06 (4,901 open restaurant permits, 99.2% with an
address), and the city's own list carries the old-law permits still in term
(1,120 rows, 909 restaurants).** They overlap by 1.1% and together hold
100.9% of the official 5,761 restaurants. Personal services from the city's
CC BY registers (2,002 premises). The block join places 95.1% of MHLW's
addressed rows and 93.5% of the registers at the block. Rail: the Utsunomiya
Light Rail (15 of its 19 stops in the city), JR's Utsunomiya and Nikkō lines
and Tobu's Utsunomiya Line, 23 station groups inside the city.

---

## Business leg — two food sources split by the 2021 law, plus four registers

| | MHLW open data | The city's own list (old law) |
|---|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=09201_food_business_all.csv`: **3,664,411 B, 8,396 rows** (許可 5,986, 届出 2,382, 許可(廃業) 22, 届出(廃業) 6). Newest 許可年月日 2026-08-28. A plain GET | `https://catalog.city.utsunomiya.tochigi.jp/dataset/4b5cae93-4640-4b4e-87bb-a5e18042366c/resource/a53500f2-7ba1-4e77-a906-e17dc5b60714/download/092011_seikatsueisei_shokuhin_shokuhin.csv`: **267,150 B, 1,120 rows**, UTF-8. Dataset `syokuhinneigyoukyoka`, resource 「食品営業許可施設一覧（令和８年７月現在）」, uploaded 2026-08-25, monthly (1か月に1回). Datastore-backed |
| **What it holds** | Every permit since 2021-06-01 (first-permit years 2021 to 2026 only), and notifications. Utsunomiya appears to enter every new permit here, not only online filings. Addresses and fields are published by the filer's consent | **Permits granted under the old law and still in term** (許可年月日1 from 1965; the dataset's note sends everything since 2021-06 to MHLW). Expiries run 2026-08-31 to 2028-04-30, so the list shrinks every month and empties in 2028 |
| Columns | the national schema: 営業施設名称、屋号又は商号, 営業の種類, **業態**, 営業施設所在地, 営業施設方書, **緯度 / 経度**, **法人名, 法人住所**, 営業施設電話番号, permit dates, 廃業年月日, 申請区分 | 施設番号, **営業所名称**, 営業所電話番号, **申請者氏名**, 申請者電話番号, **営業所** (the premises address), **申請者住所**, 台帳番号, **業種名**, 許可年月日1, 許可年月日3, 満了年月日3 |
| Restaurants | **4,901** open 飲食店営業 permits, **4,864 (99.2%) with an address**, 4,790 with MHLW's own point. 業態 among them: 居酒屋 439, キッチンカー 322, スナック 241, バー 228, コンビニエンスストア 203, キャバクラ 191, 露店 133 | **909**: 飲食店営業(レストラン) 759, (仕出し弁当) 61, (その他) 44, (旅館) 19, (自動車) 12, (露店) 3, (自動販売機) 1, 喫茶店営業 10 |
| After `japan_eigyo` (fixed, open) | Food service **3,361**; Retail **2,353** (konbini by 業態 473, other food sales 424, 菓子 362, supermarkets by 業態 257, そうざい 237, …); out 2,228 (vehicles and stalls by 業態 526, hostess venues by 業態 443, manufacturing 498, vending 188, institutional catering 338, …) | Food service **813**; Retail **153** (菓子 74, 食肉 29, 魚介 26, そうざい 17, 乳類 7); out 142 (仕出し 61, manufacturing 58, 旅館 19, …) |

- **Overlap, measured at block level** (same town, block and normalised trade
  name): **54 of MHLW's 4,712 block-tier restaurant permits (1.1%)** are in
  the city's list. Disjoint by law, as Fukuoka's (1.3%): a premises renewing
  after 2021-06 leaves the old-law list for MHLW's. `SUPERSEDES` keeps one.
- **Against the official count** (e-Stat 衛生行政報告例 FY2024: **5,761**):
  4,901 + 909 = **5,810, 100.9%** (5,756 without the overlap). MHLW alone is
  85%.
- ⚠️ **The old-law list lapses monthly**: 207 rows (147 restaurants) carry a
  満了年月日 of 2026-08-31 or 2026-09-30, after the list's as-of date; 42 of
  those restaurants already reappear in MHLW's file. Fetch the newest edition
  at build and pin `as_of` to the month it states (Kyoto's rule).
- **Address by consent**: 37 of MHLW's 4,901 restaurants (0.8%) have no
  published address, so the template's "About one restaurant in <n> … chose
  not to publish its address" bullet reads about one in 130. MHLW's
  notifications are the PARTIAL, opt-in food-retail bucket, disclosed as in
  Fukuoka.

### Personal services — the city's four registers (CKAN, monthly)

| Register | Resource | Bytes | Rows | Datastore |
|---|---|---|---|---|
| 理容所一覧 | `…/dataset/787d42bf-ef7a-4cfb-bfe3-b2d436402253/resource/0aa9d94e-369a-4e7b-8d48-5ab874f3d4da/download/092011_seikatsueisei_kankyo_riyozyo.csv` | 37,085 | **461** | yes |
| 美容所一覧 | `…/dataset/dcb9f255-2a52-4930-90ab-6c1fda354c87/resource/ec507449-b946-4e29-bb6e-e921cdd5bef3/download/092011_seikatsueisei_kankyo_-biyozyo.csv` | 150,428 | **1,367** | no |
| クリ－ニング(取次)一覧 | `…/dataset/467b3c29-17b4-4b38-bd49-55b9bec46670/resource/908957e0-e854-4992-8d7e-a4b0d3556b7a/download/092011_seikatsueisei_kankyo_-kuriningutoritsugi.csv` | 14,614 | **100** | yes |
| クリ－ニング(一般)一覧 | `…/dataset/8004a533-3811-4d56-b103-02f154d3e1f7/resource/6e285563-ece3-4f7b-a0fd-757cf6e93c34/download/092011_seikatsueisei_kankyo_kurininguippan.csv` | 8,337 | **74** | yes |

All on `https://catalog.city.utsunomiya.tochigi.jp`, cp932 (the header opens
with `№`), each titled 「（令和８年７月現在）」; the barber and beauty files were
uploaded 2026-08-25, but **the two laundry files on 2026-04-27**, so their
titles may run ahead of their contents. **2,002 premises**, none mobile.
Columns: №, 確認証番号 / 確認番号, **営業所所在地**, **営業所名称** (barbers) or
**名称**, 電話番号, **開設者**, **代表者**, **開設者住所**, 開設者電話番号,
確認年月日. The general-laundry file's headers carry leading spaces
(` 　名称`, ` 　営業所所在地`): strip them.

### Operator columns and the name rule

- The food list's **申請者氏名** is in `japan_register.OPERATOR_COLS`
  already. The registers' **開設者** and **代表者** are NOT (it has 開設者名,
  代表者名): add both at build, or the rule compares nothing there; then
  re-run the Minato control.
- **Utsunomiya names every operator, individuals included** (filled on all
  rows; company markers on 699 of 1,120 food rows and on 514 of 2,002
  register rows). With the columns mapped, the rule flags **3 food rows and 1
  laundry row**.
- **申請者住所 and 開設者住所 are operators' own addresses**, a sole trader's
  home: never select them. MHLW's 法人名 / 法人住所 are never read.

### What the shared code does not read yet (build-time)

- ⚠️ `ADDR_COLS` lacks the food list's **営業所**; `NAME_COLS` lacks
  **営業所名称**. Add them (never 申請者住所), then the Minato control.
- ⚠️ Address quirks read from the misses: a line break inside an address with
  the building after it (beauty register); an ASCII hyphen for the katakana
  long vowel (`インタ-パ-ク`, MLIT's インターパーク: 8 beauty rows unplaced);
  `新里町丙` / `新里町丁` 地番 prefixes (9 old-law rows, 23 MHLW rows
  unplaced); MHLW's literal `未選択` town (3).

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 09201)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/09201-24.0a.zip` (488,945 B) and
`…/19.0b/09201-19.0b.zip` (12,569 B): 52,217 block keys, 497 town-chōme.

| Tier | MHLW, addressed (7,942) | Old-law list (1,108 fixed) | Registers (2,002) |
|---|---|---|---|
| Block | **95.1%** | **93.2%** | **93.5%** |
| Town-chōme / 大字 centroid | 4.5% | 6.0% | 5.3% |
| Unplaced | 0.4% | 0.8% | 1.2% |

**Independent check**: MHLW's own coordinates against the block point sit a
**median 46 m** apart, **96.0% within 250 m** (7,461 rows, 59 over 1 km).
Old-law block hits against MHLW's point for the same premises: median 53 m
(179 rows). So an MHLW row the join misses can use the publisher's point
(`OWN_POINT_FALLBACK`): 386 of MHLW's non-block rows carry one.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (09201)

City bbox S 36.4640, W 139.7429, N 36.7301, E 140.0108. **24 station records
inside, 23 N02_005g groups.** Shinkansen: 宇都宮 on the 東北新幹線, dropped
(宇都宮 stays as a JR station). N02-24 and N02-25 agree on every line here;
use N02-25.

| Operator | N02 line (class) | Inside / total | Reading |
|---|---|---|---|
| 宇都宮ライトレール | 宇都宮芳賀ライトレール線 (21) | **15/19** | passes (79%); the eastern 4 stops are in Haga (芳賀台, 芳賀町工業団地管理センター前, かしの森公園前, 芳賀・高根沢工業団地) |
| 東武鉄道 | 宇都宮線 (12) | 4/11 | cut at the line (東武宇都宮, 南宇都宮, 江曾島, 西川田) |
| 東日本旅客鉄道 | 東北線 (11) | 3/155 | the Utsunomiya Line, cut at the line (宇都宮, 岡本, 雀宮) |
| 東日本旅客鉄道 | 日光線 (11) | 2/7 | 宇都宮 and 鶴田, cut at the line |

- **The light rail is purpose-built** (opened 2023-08): all 14.6 km is 軌道
  (class 21), none converted, so the light-rail test's frequency gate does
  not apply; a slower timetable would only be disclosed.
- **Gate 3**: the operator's own count is **19 stops** (the master list's
  screen of 2026-10-01; the route map at `https://www.miyarail.co.jp/rail-map`
  is an image, not re-read here). N02 has 19. Re-read at build.
- JR's 烏山線 trains start at Utsunomiya, but N02 files the line from 宝積寺
  (Takanezawa): no in-city station of its own, so it is not drawn.
- ⚠️ OSM `name:en` for every station and stop at build (no OSM was queried for
  this brief). `陽東3丁目` takes the figures rule; the LRT stops need
  `TRAM_OSM_JSON` if OSM tags them railway=tram_stop. `宇都宮駅東口` and JR's
  `宇都宮` are separate groups in N02.

## Scope

**Utsunomiya City (09201), one municipality, no wards.** The light rail runs
on into Haga, JR and Tobu into Kaminokawa, Shimotsuke, Kanuma and Mibu; cut
at the line.

## Licences — read 2026-10-02

- **The city's five datasets — PERMITTED WITH CONDITIONS.**
  - **The grant**: each `package_show` records `license_id: cc-by`
    (「クリエイティブ・コモンズ 表示」, no version). The portal's terms
    (`https://data.city.utsunomiya.tochigi.jp/terms`) apply **PDL 1.0**
    「特段の記載が無い限り」; the dataset's CC BY marking is such a statement,
    and PDL 1.0 is CC BY 4.0-compatible, so both readings permit the map on
    the same conditions.
  - **MUST DISPLAY** (the terms' 1.1, the portal's own pattern for edited
    data): `「食品営業許可施設一覧」（宇都宮市）（<dataset URL>）を加工して作成`,
    and likewise 理容所一覧, 美容所一覧, クリ－ニング(取次)一覧,
    クリ－ニング(一般)一覧; who did the processing; the licence as "CC BY"
    with no version claimed.
  - **MUST NOT**: present edited data as the city's own unprocessed data
    (1.1).
  - **Cost**: none stated; 1.6 is a disclaimer only.
- **MHLW open data — PERMITTED WITH CONDITIONS** (PDL 1.0), exactly as in
  `fukuoka.md`: `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  naming this project as the processor; no completeness or accuracy claim; no
  logo; the minor 免責 2)ウ commercial-use point stays open (fine for a
  non-commercial site).
- **MLIT 位置参照情報 and N02**: PDL 1.0. **MLIT N03**: CC BY 4.0, ⛔ never drawn.

## Privacy

Read only the trade name, the permit type (and MHLW's 業態) and the premises
address, plus MHLW's lat/lon. 申請者氏名, 開設者 and 代表者 are read in
memory by the name rule and never kept; **申請者住所, 開設者住所 and every
phone column are never selected**. Run `check_personal_exposure.py` with
`japan=True`. No row value was printed for this brief.

## Region

`"region"`: the Japan sub-region (minor tier, above); `"country": "Japan"`.
Project to **UTM 54N (EPSG:32654)**.

## Open items

- ✅ **`mode`: `light_rail` (owner, 2026-10-02).** JR about 4 stations against the light rail's 15. The owner's rule (2026-10-02): Dublin's precedent, so commuter rail drawn beside a tram does not make a city `metro`, "unless there is substantial JR, JR reads as metro". Staging read substantial as JR being the city's largest rail network by stations inside the city line..
- ⚠️ The Fukuoka config shape: `SOURCES` (mhlw, food, four registers),
  `SUPERSEDES`, `OWN_POINT_FALLBACK` for MHLW, `ADDRESS_BY_CONSENT`,
  `SOURCE_AS_OF` per source (MHLW's month, the city list's 令和８年７月).
- ⚠️ `ADDR_COLS` (営業所), `NAME_COLS` (営業所名称), `OPERATOR_COLS` (開設者,
  代表者), header stripping and the address quirks; each re-runs the Minato
  control.
- ⚠️ The laundry files' upload date (2026-04-27) against their July titles:
  read the newest at build.
- ⚠️ Gate 3 against the operators' own stop counts; OSM `name:en` for 23
  station groups.
- ⚠️ **The Economic Census join control** (`scripts/japan_census_control.py`,
  after step 2): the census has **2,021** 飲食店 establishments in 09201.
  Before de-duplication 4,159 Food service rows are placed (MHLW 3,352,
  old-law 807), about 2.1 per establishment (Hiroshima's built figure:
  1.80).
- ⚠️ The 菓子 / そうざい factory share, printed by step 2.

```brief-checks
[
  {
    "id": "utsunomiya-mhlw-live",
    "claim": "MHLW's open-data file for Utsunomiya City (09201) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=09201_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "utsunomiya-mhlw-terms-pdl",
    "claim": "MHLW's site terms still apply PDL 1.0 to the open data",
    "kind": "http_contains",
    "url": "https://i2fas.mhlw.go.jp/termsofuse.htm",
    "present": ["PDL1.0"]
  },
  {
    "id": "utsunomiya-oldlaw-food-live",
    "claim": "The city's old-law food list (令和８年７月現在) is keyless and live",
    "kind": "http_ok",
    "url": "https://catalog.city.utsunomiya.tochigi.jp/dataset/4b5cae93-4640-4b4e-87bb-a5e18042366c/resource/a53500f2-7ba1-4e77-a906-e17dc5b60714/download/092011_seikatsueisei_shokuhin_shokuhin.csv",
    "min_bytes": 150000
  },
  {
    "id": "utsunomiya-oldlaw-food-rows",
    "claim": "The old-law food list holds 1,120 rows (it shrinks monthly as old-law permits expire)",
    "kind": "ckan_rows",
    "domain": "catalog.city.utsunomiya.tochigi.jp",
    "resource_id": "a53500f2-7ba1-4e77-a906-e17dc5b60714",
    "expect": 1120
  },
  {
    "id": "utsunomiya-oldlaw-food-fields",
    "claim": "The old-law food list keeps its premises columns and its two operator columns (one an operator's own address)",
    "kind": "ckan_fields",
    "domain": "catalog.city.utsunomiya.tochigi.jp",
    "resource_id": "a53500f2-7ba1-4e77-a906-e17dc5b60714",
    "present": ["営業所", "営業所名称", "業種名", "満了年月日3", "申請者氏名", "申請者住所"]
  },
  {
    "id": "utsunomiya-food-licence",
    "claim": "The food dataset's catalogue record says cc-by and still points at the old-law CSV",
    "kind": "http_contains",
    "url": "https://catalog.city.utsunomiya.tochigi.jp/api/3/action/package_show?id=syokuhinneigyoukyoka",
    "present": ["\"license_id\": \"cc-by\"", "092011_seikatsueisei_shokuhin_shokuhin.csv"]
  },
  {
    "id": "utsunomiya-barber-rows",
    "claim": "The barber register holds 461 rows",
    "kind": "ckan_rows",
    "domain": "catalog.city.utsunomiya.tochigi.jp",
    "resource_id": "0aa9d94e-369a-4e7b-8d48-5ab874f3d4da",
    "expect": 461
  },
  {
    "id": "utsunomiya-barber-fields",
    "claim": "The barber register's operator columns are spelled 開設者 / 代表者 (not yet in OPERATOR_COLS) beside an operator's own address",
    "kind": "ckan_fields",
    "domain": "catalog.city.utsunomiya.tochigi.jp",
    "resource_id": "0aa9d94e-369a-4e7b-8d48-5ab874f3d4da",
    "present": ["営業所所在地", "営業所名称", "開設者", "代表者", "開設者住所"]
  },
  {
    "id": "utsunomiya-beauty-live",
    "claim": "The beauty-salon register (no datastore) is keyless and live",
    "kind": "http_ok",
    "url": "https://catalog.city.utsunomiya.tochigi.jp/dataset/dcb9f255-2a52-4930-90ab-6c1fda354c87/resource/ec507449-b946-4e29-bb6e-e921cdd5bef3/download/092011_seikatsueisei_kankyo_-biyozyo.csv",
    "min_bytes": 100000
  },
  {
    "id": "utsunomiya-laundry-agent-rows",
    "claim": "The laundry pick-up register (取次) holds 100 rows",
    "kind": "ckan_rows",
    "domain": "catalog.city.utsunomiya.tochigi.jp",
    "resource_id": "908957e0-e854-4992-8d7e-a4b0d3556b7a",
    "expect": 100
  },
  {
    "id": "utsunomiya-laundry-general-rows",
    "claim": "The general laundry register (一般) holds 74 rows",
    "kind": "ckan_rows",
    "domain": "catalog.city.utsunomiya.tochigi.jp",
    "resource_id": "6e285563-ece3-4f7b-a0fd-757cf6e93c34",
    "expect": 74
  },
  {
    "id": "utsunomiya-portal-terms-pdl",
    "claim": "The city portal's terms apply PDL 1.0 unless a dataset says otherwise",
    "kind": "http_contains",
    "url": "https://data.city.utsunomiya.tochigi.jp/terms",
    "present": ["PDL1.0", "public_data_license_v1.0"]
  },
  {
    "id": "utsunomiya-isj-live",
    "claim": "MLIT's block-level address file for Utsunomiya City (09201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/09201-24.0a.zip",
    "min_bytes": 300000
  },
  {
    "id": "utsunomiya-projected-crs",
    "claim": "Utsunomiya projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.88,
    "expect": "EPSG:32654"
  }
]
```
