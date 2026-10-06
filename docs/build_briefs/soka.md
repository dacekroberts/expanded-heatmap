# Sōka — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5: `docs/decisions_drafts/staging.md`, "Wave 5, second half: calls 95 to
141", call 101), on Saitama Prefecture's live food layers and its
personal-services lists, as Tokorozawa, Kasukabe and Ageo (Regional). Sōka
City (草加市, 11221) is in the 草加保健所 area of the prefecture's
jurisdiction.

The Step 0 downloads were approved by the owner 2026-10-06 (calls 106, 141,
147). **Step 0 measured 2026-10-06** (staging), each from its publisher's own
host with the project user-agent, each HTTP 200:

- **The shared prefecture files** in `data/saitama_pref/raw/` (gitignored),
  fetched once for this brief and Ageo (Regional)'s and read by Tokorozawa's
  and Kasukabe's too (`docs/build_briefs/ageo_regional.md` lists them with
  sizes): the new-law and old-law food layers queried whole
  (`food_shinpo_layer_20261006.geojson`, 52,706 rows;
  `food_kyuho_layer_20261006.geojson`, 2,627 rows; **the phone field never
  requested**), the FY-end 生活衛生 list `r7nenndo.zip` (1,203,694 B, as of
  2026-03-31) and the monthly files `0709.xlsx` to `r808.xlsx`. 31,423,566 B.
- Into `data/soka/raw/`: MHLW's `11000_food_business_all.csv` (5,456,396 B, a
  local copy of the file fetched once for Ageo (Regional); a control only);
  MLIT's ISJ `isj/11221-24.0a.zip` (140,089 B) and `isj/11221-19.0b.zip`
  (6,391 B).

**146,480 B fetched for Sōka alone** beside the shared files. Nothing else was
downloaded. Timetable pages were read for counts only (Rail).

**Run `python scripts/brief_check.py soka` before writing any code.** Then
the `japan-city` skill, **Fukuyama's shape** (one complete source per bucket,
MHLW a control) with **Ichinomiya's stated food share** (call 125); Hamamatsu's
for the registers. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` was not edited). Rail: MLIT N02-25 cut at the
N03 city line, through `pipeline/countries/japan.py` with a scratch `CITIES`
entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none in Sōka); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27); an URBAN line cut to ONE
station is left out, its station kept through the other lines, and drawn cut
only where no other line serves that station (owner, 2026-10-06, calls 54
and 92); (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**,
version 2 (2026-10-06): a bare personal name is withheld whatever the
operator column holds; (6) **no page says "currently operating"**. Also: no
frequency floor for JR or private lines in Japan (owner, 2026-10-06, call
46), any stretch at about 11 trains a day or fewer named and drawn (call
86); fault-based cost clauses accepted for all of Japan (2026-09-24);
food-retail notifications count where a list publishes them, disclosed (the
`japan_eigyo` docstring, Tokyo's rule); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The precedents set 2026-10-06, applied here (do not re-ask):** a stated
food share where a list is incomplete (call 125: the layer holds about four
restaurants in five, below); the publisher's own point where the block join
misses (127c, `OWN_POINT_FALLBACK`); MHLW's permits missing from the source
left out (126-127); low-frequency stretches drawn and named (86: none).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Sōka
carries `label_tier: "minor"` and goes in the **Japan East** view with the
other Kantō cities (wave 4's first city to land retags Japan into the eight
regions, Sōka into **Kanto**). Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 and Nishinomiya's and
Kurume's precedent: no JR, no tram or light rail; the backbone is one private
heavy-rail line (Tōbu, N02 class 12), which reads `metro`.

**4 station groups**: fewer than any page built so far (7, Anyang and
Mendoza; staging's count for call 130), and above the 3 at which the owner
discards (Chigasaki, call 130). The owner banded Sōka A on its 4 (call 101),
as Higashiyamato on its 4: **not a call**.

---

## The one-line summary

**All three buckets from Saitama Prefecture's own lists, cut to Sōka by
address and checked against N03.** Food: the live point layers (permits and
notifications), **1,395 restaurants in term**, **about 80% of the official
count estimated from the census** (stated on the page, call 125; the layer
omits operators who asked). Through `japan_eigyo` (the layer's `NN:` type
code stripped): **Food service 1,395, Retail 728**. Personal services from
the FY-end list plus the months: **barbers 127, beauty salons 363,
laundries 80** (linen supply out). Block join **97.5%** for food, 0.5%
unplaced and placed by the layer's own point. **Rail: 4 station groups**, the
Tōbu Skytree Line (frequency ASSERTED, about 6 an hour at the local stations).

---

## Business leg — Saitama Prefecture's lists

The sources, their pages, fields, licences and prefecture-wide coverage are
described once in `docs/build_briefs/ageo_regional.md` ("Business leg"); what
follows is Sōka's own measurement. In short: the food layers 食品営業施設_新法_公開
and _旧法_公開 (fields 施設_名称, 施設所在地, 所在地建物名付, 業種名 with an `NN:`
code, 申請者_氏名, 有効開始年月日, 有効終了年月日, 許可番号; phone never
requested), live (edited 2026-10-06), with the publisher's note that some
premises are left out at the operator's request; the 生活衛生 list complete to
2026-03-31 (one XLSX per health centre: **04草加保健所管内.xlsx** holds Sōka) plus
the months' new premises.

### Food

- **Rows**: 2,541 addressed to 草加市 (new law 2,472, old law 69); every
  address starts at 草加市, none names 埼玉県. Of the 2,529 rows in term with a
  point, **2,524 fall in Sōka's N03 polygon**, 4 in 八潮市 and 1 outside the
  prefecture's polygons (geocoding slips; the block join places them); no row
  addressed elsewhere has its point in Sōka. Key on N03 code 11221 and ASSERT
  the address name against it at build.
- **Types (new law)**: 飲食店営業 1,355, その他の食料・飲料販売業 177, 菓子製造業
  157, コンビニエンスストア 112, コップ式自動販売機 102, 集団給食施設 80,
  自動販売機による販売業 72, 百貨店、総合スーパー 69, 乳類販売業 45, 魚介類販売業
  41, 食肉販売業 38, … 40 types. Old law: 飲食店営業 48, 食肉販売業 8, 菓子製造業 4,
  喫茶店営業 1, a handful of others.
- **⚠️ The old-law layer keeps lapsed permits** (752 of 2,627 prefecture-wide):
  **12 Sōka rows ended before 2026-10-06** (8 restaurants; ends 2026-01 to
  2026-09); the rest end 2026-11 to 2028 (30 in 2026, 37 in 2027, 2 in 2028),
  begun 2020 and 2021. Step 2 drops them against the pinned as-of (`in_term`).
  Old law is in the source (not Kurashiki's trap).
- **Restaurants**: **1,403 rows, 1,395 in term** (new law 1,355, old law 40).
  The master list's 1,403 counts before the term filter.
- **No 業態 column**: vehicles and stalls cannot be told from restaurants (no
  address reads 一円, 管内 or 県内), nor snack bars; they stay in Food service
  (`docs/category_rules.md` R3). The official count includes vehicles too.

### Coverage: the layer against the official counts

No per-town official count is published (e-Stat's 再掲 rows cover only the
four health-centre cities). The prefecture-wide figure (the layers' 26,057
restaurants in term against e-Stat's **33,897** in the jurisdiction on
2025-03-31, **76.9%**) and the jurisdiction's official-to-census ratio
(**2.60**; the four cities 2.46 to 3.08) are measured in Ageo (Regional)'s
brief. Sōka: the 2021 census counts **669** 飲食店 establishments
(`docs/coverage_sweep/japan_universe_mhlw.csv`); **2.09 restaurants in term
per establishment**, so the layer holds an estimated **80%** of the
restaurants (1,395 of about 1,742; **68% to 85%** across the four cities'
ratios). The page states the share as an estimate (call 125); the sentence is
a proposal at review time.

### Duplicates and keys

- 許可番号 is not unique (2,541 rows, 1,250 distinct numbers; (number, start,
  type) repeats 20 times in term): never a key.
- **(address, trade name, type) repeats**: 25 groups (52 rows); 15 old-law
  rows share (address, trade name) with a new-law row. One pin per premises
  and bucket: **2,012 pins** from 2,123 bucketed rows; **1,379 Food-service
  premises**.
- **Closures are not marked**; the page keeps "may include closed premises".

### Counts through `japan_eigyo` (code stripped, in term)

**Food service 1,395** (restaurant). **Retail 728**: other food and drink
sales 177, 菓子 161, konbini 112, supermarket 69, butcher 56, fishmonger 46,
dairy 46, deli 27, greengrocer 23, bento 6, rice 5; **451 of them
notifications** (no term), by the module's standing rule. Left out: vending
180, no rule 141 (manufacturing types), institutional catering 80, mail order
5. **With the raw `NN:` value Retail reads 358**: the colon defeats the
anchored rules (the shared-code item in Ageo (Regional)'s brief).

### MHLW's file (11000), a control only

**389** rows addressed to 草加市 (届出 253, 許可 134, 許可(廃業) 2); **95 open
restaurant permits**, all with a point: **cover about 0.07**. Matched to the
layer by (address after the municipality, trade name): 233 of 389 (53 of 95
restaurants). The rest are spelling differences or premises the prefecture
leaves out at the operator's request; adding them would undo those opt-outs
(126-127). **MHLW adds nothing the map needs.**

### Personal services: 生活衛生営業施設一覧

Sheets 理容所, 美容所, クリーニング of `04草加保健所管内.xlsx` (header on row 1:
業種, (営業の種類), 施設名称, 施設所在地, 施設電話番号, **申請者名**, 確認年月日;
dates written `H31/04/30` and Shōwa `S..`, which `wareki_date` does not
read and the page does not need). The months 2025-09 to 2026-03 are all in
the FY-end list (prefecture-wide), so the list is complete to its date;
**2026-04 to 2026-08 add 1 barber and 9 salons** in Sōka. The build merges
the list whole plus the months after it (Ichinomiya's call 126).

| Kind | List (2026-03-31) + months | In a bucket |
|---|---|---|
| Barbers (理容所) | 126 + 1 = **127** | 127 |
| Beauty salons (美容所) | 354 + 9 = **363** | 363 |
| Laundries (クリーニング) | **84**: 取次所 58, full 22, リネンサプライ 4 | **80** (linen out) |

The prefecture-wide shares against e-Stat (barbers 98.2%, beauty 100.4%,
laundries 94.9%) are in Ageo (Regional)'s brief. **No repeats** on (address,
trade name); **4 premises in both barber and beauty lists**. Standing
registers, no closure column.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11221-24.0a.zip` (18,189 rows),
town-chōme `.../19.0b/11221-19.0b.zip` (115 towns). `japan.CITIES` entry at
build: `"soka": {"name": "草加市", "pref": "11", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["11221"]}`.

| Tier, today's shared code | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| **Food, in a bucket (2,123)** | **97.5%** | 2.0% | **0.5%** (10) |
| … Food service (1,395) / Retail (728) | 98.4% / 95.9% | 1.3 / 3.4 | 0.4 / 0.7 |
| Barbers (127) | **99.2%** | 0.0 | 0.8 |
| Beauty salons (363) | **98.3%** | 0.8 | 0.8 |
| Laundries (80) | **96.2%** | 3.8 | 0 |

**The layer's own point** (`OWN_POINT_FALLBACK`, 127c): against the block
point, **median 35 m**, 92.8% within 100 m, 98.6% within 250 m (1 over 1 km);
it places all 10 unplaced food rows and the chōme-tier ones: **food 100% at
block or own point**. The registers carry no point.

**The misses, read** (towns and block numbers only):
- **高砂 + 地番 468 (8 rows) and 12**: MLIT holds 高砂一丁目 and 二丁目 only
  (住居表示); the rows keep the old 地番 address. Unplaced; the layer's point.
- **松原三丁目 1638 (7 rows)**: MLIT's 松原三丁目 holds blocks 1 to 83 (a 地番
  where the area is 住居表示). **柿木町 1338 (18 rows asked, one facility)**,
  氷川町, 新栄四丁目: numbers MLIT lacks; town centroid, then the layer's point.
- Registers: 手代町 (1 barber, 3 salons) unplaced: read at build.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_11_GML.zip`, N03 code 11221
(**27.4 km²**, extent W 139.764, S 35.805, E 139.841, N 35.872). Read with
`stub_test()` and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside (south to north) |
|---|---|---|---|
| 伊勢崎線 (東武鉄道, 12) | **Tobu Skytree Line** | **4 / 55** | 谷塚, 草加, 獨協大学前, 新田 |

- **4 station records, 4 N02_005g groups**; none shared, none under 700 m
  apart. **Median nearest-station gap 1,510 m** (1,289 to 1,510): rings by the
  spacing rule at build.
- **Cut at the line**: 竹ノ塚 (足立区, Tokyo) south, 蒲生 (越谷市) north; 6.31 km
  inside, one piece. A main line through the city, not a stub. N02 files it
  as 伊勢崎線; the public name inside Sōka is the Tobu Skytree Line (the
  operator's name for 浅草 / 押上 to 東武動物公園).
- **The light-rail/rail test**: heavy rail (N02 class 12). No Shinkansen, JR,
  subway, tram or light rail in Sōka.
- **Frequency: ASSERTED, not read.** The master list row says 6 an hour,
  "READ at 谷塚"; the wave-5 probe saved no 谷塚 timetable (its saved Tōbu pages
  are 草加's station page and 春日部's Noda Line timetable), and Koshigaya's row
  gives the same figure as ASSERTED. Tōbu's timetables are NAVITIME pages keyed
  by a node id (`transfer-internal.navitime.biz/tobu/pc/diagram/BusDiagram?linkId=…&nodeId=…`;
  春日部 is `00003591`, the Skytree Line `linkId=00000798`); 谷塚's and 草加's
  node ids were not found here (Tōbu's station page loads them by script).
  **No frequency floor applies** (call 46), so
  nothing gates on it; the build reads 谷塚's weekday timetable and records
  the count, and names any stretch at about 11 a day or fewer (none expected
  on a Tokyo commuter main line).
- ⚠️ **Gate 3** at build: Tōbu's 4 stations inside. **OSM `name:en`** for 4
  groups (one Overpass query at build; not queried here).

## Scope

**Sōka City.** The Tobu Skytree Line runs on to Kita-Senju and Asakusa south
(through-running to the Hibiya and Hanzōmon lines) and to Koshigaya and
Kasukabe north: cut at the line.

## Licences — read 2026-10-06 (staging records)

As Ageo (Regional)'s brief states them: **the food layers PERMITTED WITH
CONDITIONS** (the GIS catalogue applies the prefecture portal's terms, PDL
1.0); **the 生活衛生 files on the 2024 PDL record for the page, relied on**
(owner, call 143; portal dataset 1343); one credit, the portal's prescribed
processed-use form, worded from staging's record. MHLW (control only) PDL
1.0; MLIT ISJ and N02 PDL 1.0; N03 CC BY 4.0, never drawn; e-Stat and the
census measurement only; Tōbu's timetable read for counts only, if read at
build. The notice number is claimed at build.

## Privacy

- **The food layers carry 申請者_氏名** (filled on all 2,541 Sōka rows): a
  company or cooperative marker on **1,630**, none on 911 (the shape of a sole
  trader's own name). Read IN MEMORY for the name rule only, never written.
  **電話番号 never requested.**
- **The name rule, measured in memory** (answers only): **2 rows** whose
  trade name equals the operator's own name and **1 bare personal name**
  (sign test 2), **1 flagged row among fixed premises in a bucket**.
- **The 生活衛生 list's 申請者名**: no company marker on 114 of 127 barbers,
  236 of 363 salons, 26 of 84 laundries; **0 flagged**. **施設電話番号 never
  selected**.
- MHLW's 法人名, 法人番号, 法人住所 and phones never selected (control).
- Run `check_personal_exposure.py soka` (`japan=True`) after step 2: it must
  print 0. Record the verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.764-139.841 E, centroid 139.802:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded
out: (35.80, 139.76, 35.88, 139.85). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at build
from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls; Band A on 4 station
groups (call 101); the 生活衛生 record relied on (call 143); the food layers'
terms as read; `mode: metro`; the minor tier and Japan East (Kanto); the
stated food share (125), the layer's own point (127c), MHLW's extra permits
left out (126-127); notifications in Retail (the module's standing rule); no
frequency floor.

**Open, with a recommendation:** none for the owner. **For review time:** the
page's food-share sentence, an estimate from the census ("about four
restaurants in five"), with the reason named; *recommend* Ichinomiya's
wording once approved. **Staging's correction**: the master list row's
"READ at 谷塚" is ASSERTED (above).

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): the layer's `NN:` type code stripped before `japan_eigyo` (as Ageo
  (Regional)); optionally `wareki_date` for `H31/04/30` and Shōwa `S` (not
  needed here).
- Tōbu's weekday timetable at 谷塚 (and 草加), counted whole.
- The fetch as Ageo (Regional)'s: two layers paged, `outFields` without
  電話番号, `as_of` = the retrieval date; the 生活衛生 list plus months after
  2026-03-31; the old-law term filter.
- The census ratio (2.09) and the share sentence; 手代町's register misses;
  gate 3; OSM `name:en`; line colour on both basemaps; the opening view
  (`map-view`); the factory share; `check_provenance.py`;
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "soka-food-page",
    "claim": "The prefecture's food page points to the two GIS layers (new law 746f76d1..., old law a0b8fc89...). ASCII anchors only: the host sends no charset",
    "kind": "http_contains",
    "url": "https://www.pref.saitama.lg.jp/a0708/syokuhini-ichiran/ichiran-top.html",
    "present": ["746f76d1a1844464999a87554d59b6bb", "a0b8fc89c3894763b1b1eb07a2fc95fb"]
  },
  {
    "id": "soka-food-newlaw-layer",
    "claim": "The new-law food layer: points, about 52,706 rows prefecture-wide, the fields read here, edited live (2026-10-06)",
    "kind": "arcgis_layer",
    "url": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/%E9%A3%9F%E5%93%81%E5%96%B6%E6%A5%AD%E6%96%BD%E8%A8%AD_%E6%96%B0%E6%B3%95_%E5%85%AC%E9%96%8B/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 52706,
    "tolerance": 4000,
    "present": ["施設_名称", "施設所在地", "業種名", "申請者_氏名", "有効終了年月日", "許可番号"],
    "max_age_days": 60
  },
  {
    "id": "soka-food-oldlaw-layer",
    "claim": "The old-law food layer: points, about 2,627 rows (lapsed permits kept)",
    "kind": "arcgis_layer",
    "url": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/%E9%A3%9F%E5%93%81%E5%96%B6%E6%A5%AD%E6%96%BD%E8%A8%AD_%E6%97%A7%E6%B3%95_%E5%85%AC%E9%96%8B/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 2627,
    "tolerance": 600,
    "present": ["施設_名称", "施設所在地", "業種名", "有効終了年月日"],
    "max_age_days": 120
  },
  {
    "id": "soka-env-page",
    "claim": "The 生活衛生 page offers the FY-end list (r7nenndo.zip) and the monthly files to 2026-08. A failure on r808 means a newer month: re-measure",
    "kind": "http_contains",
    "url": "https://www.pref.saitama.lg.jp/a0706/6hou/ichiran.html",
    "present": ["r7nenndo.zip", "r0804.xlsx", "r808.xlsx"]
  },
  {
    "id": "soka-mhlw-live",
    "claim": "MHLW's open-data file for Saitama Prefecture's jurisdiction (11000) answers a plain keyless GET (a control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11000_food_business_all.csv",
    "min_bytes": 4000000
  },
  {
    "id": "soka-isj-block-live",
    "claim": "MLIT's block-level address file for Sōka (11221) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11221-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "soka-isj-chome-live",
    "claim": "MLIT's town-chōme file for Sōka (11221) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/11221-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "soka-tobu-station-page",
    "claim": "Tōbu's own station page for 草加 answers (the timetable sits behind a NAVITIME widget; frequency ASSERTED)",
    "kind": "http_contains",
    "url": "https://www.tobu.co.jp/railway/guide/station/info/1402.html",
    "present": ["草加駅", "navitime"]
  },
  {
    "id": "soka-projected-crs",
    "claim": "Sōka projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.80,
    "expect": "EPSG:32654"
  }
]
```
