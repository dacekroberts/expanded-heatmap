# Ageo (Regional) — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5: `docs/decisions_drafts/staging.md`, "Wave 5, second half: calls 95 to
141", calls 101 and **102: Ina too thin alone, so one page**). **Ageo
(Regional) is Ageo City (上尾市, 11219) plus Ina Town (伊奈町, 11301) on one
page**: the same source (Saitama Prefecture's lists) and the same line (the
New Shuttle runs through both). Ina alone holds 155 restaurants, under
Settsu's "too thin". **This is NOT an extension of a built page**: Ageo is not
built, so this is a first build of a two-municipality page (`add-city`, as
Seattle (Regional)); only the `regional-extension` skill's naming and scope
pattern applies (the "(Regional)" label, codes not names, the second
municipality named in What Is Excluded).

The Step 0 downloads were approved by the owner 2026-10-06 (calls 106, 141,
147). **Step 0 measured 2026-10-06** (staging), each from its publisher's own
host with the project user-agent, each HTTP 200:

- Into the **shared** `data/saitama_pref/raw/` (gitignored; also read by
  Tokorozawa's and Kasukabe's briefs), from Saitama Prefecture:
  - the two live food layers on `services9.arcgis.com/n65w8AXGaYPTqFYI`
    (the prefecture's ArcGIS Online organisation), queried whole with
    `where=1=1`, `outSR=4326`, paged by `OBJECTID`, **the phone field never
    requested**: `food_shinpo_layer_20261006.geojson` (食品営業施設_新法_公開,
    **52,706** rows, 28,581,348 B) and `food_kyuho_layer_20261006.geojson`
    (食品営業施設_旧法_公開, **2,627** rows, 1,418,680 B). Both layers were
    last edited 2026-10-06 (`editingInfo.lastEditDate`).
  - from `www.pref.saitama.lg.jp/documents/232288/` (生活衛生課): the
    FY-end list `r7nenndo.zip` (1,203,694 B, every 生活衛生 premises
    holding a permit or confirmation on 2026-03-31, one XLSX per health
    centre) and the twelve monthly new-premises files `0709.xlsx` to
    `r808.xlsx` (2025-09 to 2026-08, 219,844 B together).
- Into `data/ageo_regional/raw/`: MHLW's `11000_food_business_all.csv`
  (5,456,396 B, `i2fas.mhlw.go.jp`), a control only; and MLIT's ISJ in
  `isj/`: `11219-24.0a.zip` (166,720 B), `11219-19.0b.zip` (6,876 B),
  `11301-24.0a.zip` (70,626 B), `11301-19.0b.zip` (5,294 B).

**32,929,282 B in all** (the shared prefecture files 31,423,566 B). Nothing
else was downloaded. Timetable pages were read for counts only (Rail).

**Run `python scripts/brief_check.py ageo_regional` before writing any code.**
Then the `japan-city` skill: **Fukuyama's shape** (one complete source per
bucket, MHLW a control) with **Ichinomiya's stated food share** (call 125);
Hamamatsu's for the registers (one sheet per kind). Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` was not edited).
Rail: MLIT N02-25 cut at the N03 line of the two municipalities, through
`pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; the Tōhoku and Jōetsu Shinkansen cross both towns with no
station); (2) **lines served only by limited expresses DO count**
(2026-09-28); (3) **the city line only**: only stations inside the scope get
rings, JR and the private lines are cut at the line, **a one-station stub
stays as cut** (2026-09-27); an URBAN line cut to ONE station is left out,
its station kept through the other lines, and drawn cut only where no other
line serves that station (owner, 2026-10-06, calls 54 and 92); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor
for JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at
about 11 trains a day or fewer named and drawn (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); food-retail notifications
count where a list publishes them, disclosed (the `japan_eigyo` docstring,
Tokyo's rule); English station names from OSM `name:en`; every Japanese city
reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The precedents set 2026-10-06, applied here (do not re-ask):** a stated
food share where a list is incomplete (call 125, Ichinomiya: the layer holds
about seven restaurants in ten, below); the publisher's own point where the
block join misses (127c: the layer carries points, `OWN_POINT_FALLBACK`);
MHLW's permits missing from the city source left out (126-127, Ichinomiya:
they would undo the publisher's own opt-outs); tiers disclosed where the
block share is low (145: Ina's beauty salons 78.6%); low-frequency stretches
drawn and named (86: none here).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Ageo
(Regional) carries `label_tier: "minor"` and goes in the **Japan East** view
with the other Kantō cities (`app/cities.py`; wave 4's first city to land
retags Japan into the eight regions, this page into **Kanto**). Its label
offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200),
never by eye; "(Regional)" widens the pill, so measure it.

**✅ `mode`: `metro`** on Sakura's precedent (owner, 2026-10-06, call 121:
"i think metro is safe due to it having significant presence"): the New
Shuttle, an automated guideway (N02 class 16), holds 7 of the 9 station
groups, JR the other 2; no subway or tram.

---

## The one-line summary

**All three buckets from Saitama Prefecture's own lists, one source each,
cut to the two municipalities by address and checked against N03.** Food:
the prefecture's live point layers (new law and old law, permits AND
notifications), **1,141 restaurants in term** (Ageo 987, Ina 154), **about
69% of the official count estimated from the census** (stated on the page,
call 125; the layer omits operators who asked, and Saitama publishes no
per-town official count). Through `japan_eigyo` (the layer's `NN:` type code
stripped, below): **Food service 1,141, Retail 797**. Personal services from
the FY-end 生活衛生 list plus the months: **barbers 167, beauty salons 413,
laundries 54** (linen supply out); the lists hold **98.2%, 100.4% and 94.9%**
of e-Stat's counts across the prefecture's jurisdiction. Block join **93.1%**
for food, the rest at the town-chōme centroid, **none unplaced**, and the
layer's own point takes every food miss. **Rail: 9 station groups**: the New
Shuttle 7 (Ageo 2, Ina 5; 4 to 6 an hour, READ) and the JR Takasaki Line 2
(4 to 5 an hour, READ); nothing at or under 11 trains a day.

---

## Business leg — Saitama Prefecture's lists

Saitama Prefecture publishes for the municipalities its own health centres
serve: every city and town but Saitama City, Kawagoe, Kawaguchi and Koshigaya
(each a health-centre city with its own lists). **Ageo and Ina are both in
the 鴻巣保健所 area.** MHLW's national file covers about 7% of their permits
(a control).

### Food: 食品営業施設一覧 (two live ArcGIS layers)

Page `https://www.pref.saitama.lg.jp/a0708/syokuhini-ichiran/ichiran-top.html`
(食品安全課): the full list of permits and notifications 「は、埼玉県GIS上の
オープンデータカタログに掲載」; the GIS 「その時点の食品営業施設の全業種一覧を
リアルタイムで更新」, so the monthly new-premises files stopped in 2025-04;
「※事業者の要望により、一部の施設情報は掲載されないことがあります。」

| Layer (hub item) | Service | Rows (prefecture) | Ageo | Ina |
|---|---|---|---|---|
| 新法 (`746f76d1a1844464999a87554d59b6bb`): permits and notifications since 2021-06-01 | `食品営業施設_新法_公開/FeatureServer/0` | **52,706** | 1,900 | 360 |
| 旧法 (`a0b8fc89c3894763b1b1eb07a2fc95fb`): permits before 2021-05-31 | `食品営業施設_旧法_公開/FeatureServer/0` | **2,627** | 46 | 4 |

- **Fields**: 施設_名称, 施設所在地, 所在地建物名付 (the address with the
  building, filled on every row), 電話番号 (**never requested**), 業種名,
  **申請者_氏名** (the applicant), 有効開始年月日, 有効終了年月日, 許可番号.
  Point geometry (Web Mercator, read as 4326): 5 of 52,706 new-law rows at
  (0, 0), none in Ageo or Ina. 業種名 carries a code: `01:飲食店営業 ` (a
  trailing space), 61 values across the two layers.
- **Against the shared tuples:** 施設所在地 is in `ADDR_COLS`, 業種名 in
  `TYPE_COLS`, 施設_名称 in `NAME_COLS`, 申請者_氏名 in `OPERATOR_COLS`. No
  shared-tuple change is needed. **But `japan_eigyo.normalise` leaves the
  colon** (`01:` becomes `:`), so every anchored Retail rule misses: Ageo's
  Retail reads **369** rows with the raw value and **658** with the code
  stripped (Ina 78 against 139). The build strips `^\d+:` (a city-local
  `source_rows`, or `normalise` taking `^\d+[:：]?`, followed by the
  taxonomy's import-time checks and the Minato control).
- **Cut to the two towns by the address's municipality** (the layer has no
  municipality code). Every Ageo address starts at 上尾市, every Ina address
  at 北足立郡伊奈町; none names 埼玉県. Checked against N03 by each row's own
  point: of 1,943 Ageo rows in term, 1,933 fall in Ageo, 6 in 桶川市, 2 in
  Ina and 2 in Saitama City (geocoding slips; the block join places them);
  362 of 363 Ina rows fall in Ina. Key the scope on the N03 codes (11219,
  11301) and ASSERT the address names against them at build.
- **Types in the two towns (new law)**: 飲食店営業 957 + 152, その他の食料・
  飲料販売業 229 + 46, 菓子製造業 101 + 28, コンビニエンスストア 86 + 25,
  集団給食施設 85 + 21, コップ式自動販売機 69 + 11, 百貨店、総合スーパー 54 + 7,
  乳類販売業 40 + 11, … 40 types. Old law: 飲食店営業 32 + 3, 菓子製造業 8 + 1,
  a handful of shops.
- **No 業態 column**: vehicles and stalls cannot be told from restaurants
  (no address reads 一円, 管内 or 県内: a vehicle is filed at a street
  address), nor snack bars; they stay in Food service as `docs/category_rules.md`
  R3 allows ("wherever the register names them"). The official count
  includes vehicles too.

### In term, old law, and closures

- **The new-law layer is live**: 20 of its 52,706 rows ended before
  2026-10-06 (1 in Ina, none in Ageo). The 20,831 rows with no end date are
  notifications (届出), which carry no term.
- **⚠️ The old-law layer keeps lapsed permits**: 752 of its 2,627 rows ended
  before 2026-10-06 (284 in 2025). In the two towns 3 Ageo rows (2
  restaurants) and none in Ina; the old-law permits in term end in 2026-11
  to 2027 (Ageo 46: 11 in 2026, 35 in 2027; Ina 4, all 2027). **Step 2
  drops rows by 有効終了年月日 against the pinned as-of** (`in_term`,
  Kitakyushu's precedent). Old law is in the source (not Kurashiki's trap).
- **Restaurants**: Ageo **989 rows, 987 in term** (957 new law, 30 old law);
  Ina **155, 154 in term** (one new-law permit ended 2026-02). **1,141 in
  term together.** The master list's 989 and 155 count before the term filter.
- **Old and new law at one premises**: 16 Ageo old-law rows share (address,
  trade name) with a new-law row (another type, or a renewal the old layer
  has not dropped); one pin per premises and bucket keeps one.

### Coverage: the layer against the official counts

Saitama publishes no restaurant count for Ageo or Ina: e-Stat's 衛生行政報告例
counts the prefecture (再掲 rows only for the four health-centre cities).

- **Prefecture-wide**: e-Stat FY2024 (`japan_official.estat()`), 埼玉県
  53,636 less Saitama City 9,798, Kawaguchi 4,259, Kawagoe 2,992 and Koshigaya
  2,690 = **33,897** 飲食店営業 in force on 2025-03-31 in the prefecture's
  jurisdiction. The two layers hold **26,057** restaurant permits in term
  (new 24,766, old 1,291): **76.9%**, against a baseline 18 months older.
- **Per town, by the census** (`scripts/japan_census_control.py` at build;
  2021 Economic Census, `docs/coverage_sweep/japan_universe_mhlw.csv`):
  上尾市 **548** 飲食店 establishments, 伊奈町 **85**. The jurisdiction's
  official-to-census ratio is 33,897 / 13,019 = **2.60** (the four
  health-centre cities 2.46 to 3.08). Restaurants in term per establishment:
  **Ageo 1.80, Ina 1.81**, so the layer holds an estimated **69%** of the
  restaurants (Ageo 987 of about 1,427, Ina 154 of about 221; **58% to 73%**
  across the four cities' ratios).
- **Why**: the publisher's own note ("some premises are not listed at the
  operator's request"), and the census's establishments are counted on the
  ground in 2021. Ichinomiya's 67.7% (withheld on request) was kept in A with
  the share stated (call 125): **the page states the share as an estimate**.
  The sentence is a proposal at review time (no template covers an estimated
  share): drafted in the drafts file at build.

### Duplicates and keys

- 許可番号 is not unique: the 2,310 rows of the two towns carry 1,367
  distinct numbers; (number, start, type) still repeats 17 times. Never a key.
- **(address, trade name, type) repeats**: 17 groups (38 rows) in Ageo, 1 in
  Ina. One pin per premises and bucket (trap 7): **1,526 Ageo and 275 Ina
  pins** from 1,645 and 293 bucketed rows; 979 Ageo and 154 Ina Food-service
  premises.
- **Closures are not marked** (no status column); the live layer drops a
  closed premises when the prefecture edits it, as far as the 20 lapsed
  new-law rows show. The page keeps "may include closed premises".

### Counts through `japan_eigyo` (code stripped, in term)

| | Ageo | Ina | Together |
|---|---|---|---|
| Food service (restaurant) | **987** | **154** | **1,141** |
| Retail | **658** | **139** | **797** |
| … other food and drink sales / 菓子 / konbini | 229 / 109 / 86 | 46 / 29 / 25 | |
| … supermarket / dairy / butcher / deli | 54 / 41 / 37 / 33 | 7 / 11 / 3 / 9 | |
| … greengrocer / fishmonger / rice / bento | 30 / 28 / 8 / 3 | 2 / 2 / 2 / 3 | |
| Left out: vending, catering, no rule, mail order | 115, 85, 97, 1 | 24, 21, 25, 0 | |

**Retail includes the notifications** (465 Ageo and 97 Ina rows with no
term: konbini, supermarkets, greengrocers, 包装済み meat and fish), by the
module's standing rule; unlike MHLW's partial notifications elsewhere
(Akita's open call 1), these are the prefecture's own register, opt-outs
aside. The page still says no general retail is published.

### MHLW's file (11000), a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11000_food_business_all.csv`:
**5,456,396 B, 15,335 rows** (届出 12,229, 許可 3,064, 許可(廃業) 24,
届出(廃業) 18), the national schema; 6,747 rows have no address. Ageo **346**
rows (69 open restaurant permits, all with a point), Ina **69** (11): **cover
about 0.07**. Matched to the layer by (address after the municipality, trade
name): Ageo 195 of 346 (29 of 69 restaurants), Ina 45 of 69. The rest are
spelling differences or premises the prefecture leaves out at the operator's
request; adding them would undo those opt-outs (Ichinomiya's call 2a,
126-127). **MHLW adds nothing the map needs.**

### Personal services: 生活衛生営業施設一覧

Page `https://www.pref.saitama.lg.jp/a0706/6hou/ichiran.html` (生活衛生課):
the FY-end list 「令和8年3月31日時点で許可・確認を受けている生活衛生営業施設の
全業種一覧」 (`r7nenndo.zip`, one XLSX per health centre: **05鴻巣保健所管内.xlsx**
holds Ageo and Ina) and the months' new premises (2025-09 to 2026-08,
「翌月の10日～15日頃に更新」); the same opt-out note.

- **Sheets** 理容所, 美容所, クリーニング (and inns, baths, theatres, not
  used). Header on row 1: 業種, (クリーニング: 営業の種類), 施設名称,
  施設所在地, 施設電話番号, **申請者名**, 確認年月日; the monthly files add
  確認番号. `city_rows` reads them; 施設所在地 and 施設名称 are in the shared
  tuples, 申請者名 in `OPERATOR_COLS`. The config names the kind per sheet.
- **確認年月日 is written `H31/04/30` or `S60/04/01` (Shōwa)**:
  `wareki_date` reads neither (slashes, and no S era). No date is needed (the
  registers carry no term); a note only.
- **The months**: every 2025-09 to 2026-03 row is already in the FY-end list
  (10 of 10 barbers, 132 of 132 salons, 14 of 14 laundries), so the list is
  complete to its date; 2026-04 to 2026-08 add **Ageo 2 barbers and 1 salon,
  Ina none**. The build merges the list whole plus the months after it
  (Ichinomiya's call 126), de-duplicated on (address, trade name).

| Kind | Ageo (list + months) | Ina | Prefecture jurisdiction, list | e-Stat FY2024, jurisdiction | Share |
|---|---|---|---|---|---|
| Barbers (理容所) | 143 + 2 = **145** | **22** | 3,127 | 4,719 − 1,535 = 3,184 | **98.2%** |
| Beauty salons (美容所) | 356 + 1 = **357** | **56** | 7,585 | 11,894 − 4,340 = 7,554 | **100.4%** |
| Laundries (クリーニング) | **51** (47 in a bucket) | **8** (7) | 1,637 | 2,888 − 1,163 = 1,725 | **94.9%** |

(e-Stat from `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
`…_cleaning_by_city.csv`, the 埼玉県 row less the four cities' 再掲 rows;
laundry 施設数 includes 取次所.)

- **Laundry kinds** (営業の種類): Ageo 取次所 (受取及び引渡しのみ) 35, full
  (受取、処理及び引渡し) 12, **リネンサプライ 4 (out**, the module's linen
  rule); Ina 3, 4 and 1. 205 prefecture rows (other health centres) leave the
  kind blank; none here.
- **Repeats**: none on (address, trade name). **Premises in both barber and
  beauty lists**: Ageo 1, Ina 0.
- **Standing registers**: no closure column; the page keeps "may include
  closed premises".

## Coordinates — a JOIN to MLIT 位置参照情報 (two municipalities)

Block `isj/11219-24.0a.zip` (23,736 rows) and `isj/11301-24.0a.zip` (14,209),
town-chōme `…-19.0b.zip` (141 and 41 towns). MLIT keys **上尾市** under the
ward "" (its 市区町村名 split at 市) and **伊奈町 under "北足立郡伊奈町"** (no 市
to split at). **The two towns share three town names** (本町一丁目 to 三丁目).

⚠️ **Shared code: no built Japanese page spans two municipalities.** With
today's wardless key ("") Ina's 363 food rows join **30 block, 14 chōme,
319 unplaced**, and its 14 本町 rows would take Ageo's 本町 points. Keyed by
municipality (Ina's rows under "北足立郡伊奈町"), they join 323 block, 40
chōme, 0 unplaced. The build gives each row its municipality's ISJ ward key
(a per-municipality key in `japan.CITIES`, e.g. `"municipalities":
{"11219": "上尾市", "11301": "北足立郡伊奈町"}`, read by `permits_from_rows`
and `load_city_isj`), followed by the Minato control
(`screen_japan_join.py minato` 98.0 / 0.2 / 1.8) and every city screen.
Measured here by setting the ward key in memory.

| Tier, municipality-keyed | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| **Food, in a bucket (1,938)** | **93.1%** | 6.9% | **0** |
| … Ageo food (1,645): Food service / Retail | 94.0% (94.4 / 93.3) | 6.0 | 0 |
| … Ina food (293): Food service / Retail | 88.1% (87.7 / 88.5) | 11.9 | 0 |
| Barbers: Ageo 145 / Ina 22 | 95.9% / 86.4% | 3.4 / 13.6 | 0.7 / 0 |
| Beauty salons: Ageo 357 / Ina 56 | 94.7% / **78.6%** | 5.0 / 19.6 | 0.3 / 1.8 |
| Laundries: Ageo 47 / Ina 7 | 100% / 85.7% | 0 / 14.3 | 0 |

**The layer's own point** (`OWN_POINT_FALLBACK`, 127c): against the block
point, **median 45 m (Ageo) and 46 m (Ina)**, 96.2% and 94.6% within 250 m
(9 and 8 over 1 km). Under `datum_guard`'s threshold, so it places every
food row the block join leaves at the chōme tier: **food 100% at block or
own point**. The registers carry no point: their chōme rows stay at the
centroid, **disclosed by tier** (145; Ina's beauty salons 78.6% block).

**The misses, read** (towns and block numbers only, `misses.py`):
- **Ageo 壱丁目北, block 29: 50 food rows at one address** (a shopping
  centre): MLIT's 壱丁目北 holds blocks 1 to 24. The layer's point places
  them.
- **Ina 中央一丁目 to 五丁目**: the addresses' block numbers (21 to 184) are
  the post-readjustment 街区; MLIT still keys the old 地番 (729 to 10,047).
  **Ina 小室**: 6 rows at 780 (one facility) and rural 地番 MLIT lacks.
- Ageo 藤波三丁目, 宮本町 1100, 上野本郷 568 and 573: numbers MLIT lacks.
- Registers: 平方領領家 and 上堤 (Ageo), 小室新田 (Ina), one row each unplaced.

## 🚇 Rail — MLIT N02-25 cut at the two towns' N03 line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_11_GML.zip`, N03 codes 11219
and 11301 (**60.3 km²**: Ageo 45.5, Ina 14.8; extent W 139.534, S 35.926, E
139.650, N 36.027). Read with `stub_test()` and an in-memory `CITIES` entry
(scratch `rail.py`, `track.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 伊奈線 (埼玉新都市交通, 16, third sector) | **New Shuttle** | **7 / 13** | Ageo: 原市, 沼南; Ina: 丸山, 志久, 伊奈中央, 羽貫, 内宿 |
| 高崎線 (東日本旅客鉄道, 11) | **JR Takasaki Line** | **2 / 19** | 上尾, 北上尾 (Ageo) |

- **9 station records, 9 N02_005g groups** (Ageo 4, Ina 5); no shared group,
  no two groups under 700 m apart. **Median nearest-station gap 1,045 m**
  (806 to 1,684): rings by the spacing rule at build.
- **⚠️ Correction to the master list row ("the New Shuttle drawn cut at both
  towns' edges")**: on one page the New Shuttle is cut **once**, at the
  Saitama City line south of 原市 (next 吉野原, 北区); its north end, **内宿,
  is the line's terminus**, in Ina. Its 6.81 km inside (Ageo 1.72, Ina 5.09)
  is one piece. The row's wording fits two separate pages; staging corrects it.
- **JR Takasaki Line**: a main line cut at the line (宮原 south, 桶川 north),
  3.56 km inside; not a stub.
- **The light-rail/rail test**: the New Shuttle is an automated guideway
  (N02 class 16) on its own viaduct beside the Shinkansen, every 10 to 15
  minutes: rail, as Tokorozawa's Leo Liner (AGT) and Sakura's Yamaman line.
  Seven stations: no one-station question.
- **Shinkansen**: the Tōhoku and Jōetsu Shinkansen cross both towns (7.6 km)
  with no station; out (standing call 1). **The JR Tōhoku (Utsunomiya)
  Line crosses Ageo's eastern edge for 1.44 km with no station** (東大宮 and
  蓮田 are outside): not in `LINES`, as no station of it is in scope.
- **Frequency, read 2026-10-06 from the operators** by plain GET with the
  project user-agent; only counts are recorded, never a timetable:

  | Station (line, direction) | Weekday departures | Per hour 10-15 |
  |---|---|---|
  | 上尾 (Takasaki, to 熊谷・高崎 / to 大宮・上野) | 114 / 115 | 5 (6 at 10 toward 高崎) |
  | 北上尾 (Takasaki, to 熊谷・高崎 / to 大宮・上野) | 96 / 104 | 4 |
  | 伊奈中央 (New Shuttle, to 大宮) | 103 | 4 at 11-13, 5 at 10 and 14; 5 to 9 an hour 06-21 otherwise |

  JR East's station timetables (`timetables.jreast.co.jp`, `list0042` and
  `list0549`, the weekday pages under `2610/timetable/`) counted whole, every
  departure including marked trains (`katsurane.py`'s whole-page reader). The
  New Shuttle's weekday timetable at 伊奈中央 is an image on the operator's
  page (`new-shuttle.jp/station/inachuo/inachuo_timetable/`, file
  `11_inamachi_nobori.gif`), saved by the wave-5 probe and counted by eye
  here; every train leaving 伊奈中央 for 大宮 passes 丸山, 沼南 and 原市, so
  Ageo's two stations see at least as many (not read separately).
  **Nothing at or under about 11 trains a day** (call 86).
- ⚠️ **Gate 3** at build: JR East's 2 and the New Shuttle's 7 stations inside.
  **OSM `name:en`** for 9 groups (one Overpass query at build; not queried
  here). The New Shuttle's label is its public name, **New Shuttle**
  (the operator's own English on its timetable).

## Scope

**Ageo City and Ina Town, one page named "Ageo (Regional)".** The page names
Ina in its page text (`docs/city_page_format.md`) and in What Is Excluded
(`### Ageo (Regional) - ...`, Ina named with its counts, the stations line:
"The New Shuttle's five stations in Ina are drawn and ringed"), so the scope
reaches the reader (`check_scope_disclosure.py`). The JR Takasaki Line runs on
to Ōmiya and Takasaki, the New Shuttle to Ōmiya: cut at the line. Not a
regional extension: no built page changes name.

## Licences — read 2026-10-06 (staging records)

- **The food layers: PERMITTED WITH CONDITIONS** (licence read 2026-10-06,
  `docs/decisions_drafts/staging.md`, "Wave 5, second half"): the GIS
  catalogue (`portal-pref-saitama.hub.arcgis.com/pages/opendatacatalog`)
  applies the prefecture portal's terms 「埼玉県オープンデータ利用規約を準用」,
  which apply PDL 1.0 (`opendata.pref.saitama.lg.jp/pages/terms`).
- **The 生活衛生 files: the 2024 PDL record for the page relied on** (owner,
  call 143): the portal's dataset 1343 「【埼玉県】生活衛生営業施設一覧」
  (2024-05-09) links the page, against the site's copyright page.
- **One credit**: the portal's prescribed processed-use credit; take the
  wording from staging's record, not from this brief.
- **MHLW** (control only): PDL 1.0, `docs/data_sources/japan.md`.
  **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census:
  measurement only. **JR East's and the New Shuttle's timetables**: counts
  only, never reproduced.
- The notice number is claimed at build (`docs/session_roles.md`), not here.

## Privacy

- **The food layers carry 申請者_氏名** (filled on every row): a company or
  cooperative marker on **1,242 of 1,946** Ageo rows and **259 of 364** Ina
  rows; the rest (704 and 105) have the shape of a sole trader's own name.
  The shared cache holds it (as every Japanese list's raw file holds its
  operator column); step 2 reads it IN MEMORY for the name rule only and
  never writes it. **電話番号 was never requested**; a build's fetch must
  request the same field list.
- **The name rule, measured in memory** (answers only): Ageo **2 rows**
  whose trade name equals the operator's own name, **1 among fixed premises
  in a bucket**; no bare personal name (sign test 2). Ina 0.
- **The 生活衛生 lists carry 申請者名**: without a company marker on Ageo
  124 of 145 barbers, 254 of 357 salons, 9 of 51 laundries; Ina 21, 49, 3.
  **0 flagged** (no trade name equals its applicant; no bare personal
  name). **施設電話番号 is never selected**; select 施設名称 and 施設所在地.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected (control).
- Run `check_personal_exposure.py ageo_regional` (`japan=True`) after step 2:
  it must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The two towns run 139.534-139.650 E, centroid 139.591:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded
out: (35.92, 139.53, 36.03, 139.65). `japan.CITIES` at build:
`"ageo_regional": {"name": "上尾市", "pref": "11", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["11219", "11301"]}` plus the
per-municipality ward key above. Scaffold with `scripts/scaffold_city.py ...
--page-number <N>`, the number claimed at build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls; Band A (call 101); Ina
joins Ageo as one page (call 102); the 生活衛生 record relied on (call 143);
the food layers' terms as read; `mode: metro` (Sakura's call 121); the minor
tier and Japan East (Kanto); the stated food share (125), the layer's own
point (127c), MHLW's extra permits left out (126-127), tiers disclosed (145);
notifications in Retail (the module's standing rule); no frequency floor.

**Answered by the owner on 2026-10-06:** call 171, **the R8.3.31 old-law list added to the food source** for the four Saitama pages (Ageo (Regional), Sōka, Tokorozawa, Kasukabe), with the live new-law and old-law layers, in term on the as-of, de-duplicated, renewals dropped, **and disclosed** on the page: the old-law rows are an upper bound as of 2026-03-31, closures since unseen (Kyoto's disclosure); the build measures the list's rows for Ageo and Ina and restates the counts above. Also call 172, **rows that start after the as-of are dropped** until they are in term (`in_term`'s mirror); call 173, **no food-share sentence**: the publisher's withholding note is disclosed with no number (Matsudo's precedent), with the old-law upper bound; the review-time proposal (a) above, the census estimate sentence, is withdrawn by call 173.

**Open, with a recommendation:** none for the owner. **For review time
(proposals, drafted at build):** (a) the page's food-share sentence, an
estimate from the census ("about seven restaurants in ten"), with the reason
named (operators who asked not to be listed); *recommend* Ichinomiya's
wording once approved. (b) **The master list row's "cut at both towns'
edges"**: staging corrects it to one cut (the Saitama City line), 内宿 being
the terminus.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): the per-municipality ISJ ward key (two municipalities, one page,
  three shared town names); the `NN:` type code stripped before
  `japan_eigyo`; optionally `wareki_date` reading `H31/04/30` and the Shōwa
  `S` (not needed for this page).
- The fetch: the two layers paged (new law by up to 16,000, old law by 2,000),
  `outFields` without 電話番号, pinned `as_of` = the retrieval date
  (2026-10-06 here); the 生活衛生 FY-end list plus months after 2026-03-31.
- The old-law term filter against the as-of (752 lapsed rows prefecture-wide);
  the census ratio (1.80 / 1.81) and the share sentence; the 10 Ageo points
  in other municipalities (none used where the block join holds).
- Gate 3 (JR East 2, New Shuttle 7); OSM `name:en`; line colours on both
  basemaps; the opening view (`map-view`); the factory share;
  `check_provenance.py`; `check_scope_disclosure.py` (Ina named).

```brief-checks
[
  {
    "id": "saitama-food-page",
    "claim": "The prefecture's food page points to the two GIS layers (new law 746f76d1..., old law a0b8fc89...). ASCII anchors only: the host sends no charset",
    "kind": "http_contains",
    "url": "https://www.pref.saitama.lg.jp/a0708/syokuhini-ichiran/ichiran-top.html",
    "present": ["746f76d1a1844464999a87554d59b6bb", "a0b8fc89c3894763b1b1eb07a2fc95fb", "portal-pref-saitama.hub.arcgis.com"]
  },
  {
    "id": "saitama-food-newlaw-layer",
    "claim": "The new-law food layer: points, about 52,706 rows prefecture-wide, the fields read here, edited live (2026-10-06)",
    "kind": "arcgis_layer",
    "url": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/%E9%A3%9F%E5%93%81%E5%96%B6%E6%A5%AD%E6%96%BD%E8%A8%AD_%E6%96%B0%E6%B3%95_%E5%85%AC%E9%96%8B/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 52706,
    "tolerance": 4000,
    "present": ["施設_名称", "施設所在地", "業種名", "申請者_氏名", "有効開始年月日", "有効終了年月日", "許可番号"],
    "max_age_days": 60
  },
  {
    "id": "saitama-food-oldlaw-layer",
    "claim": "The old-law food layer: points, about 2,627 rows (lapsed permits kept), edited live",
    "kind": "arcgis_layer",
    "url": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/%E9%A3%9F%E5%93%81%E5%96%B6%E6%A5%AD%E6%96%BD%E8%A8%AD_%E6%97%A7%E6%B3%95_%E5%85%AC%E9%96%8B/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 2627,
    "tolerance": 600,
    "present": ["施設_名称", "施設所在地", "業種名", "有効終了年月日"],
    "max_age_days": 120
  },
  {
    "id": "saitama-gis-catalogue-terms",
    "claim": "The prefecture portal's terms apply PDL 1.0 (the GIS catalogue applies them)",
    "kind": "http_contains",
    "url": "https://opendata.pref.saitama.lg.jp/pages/terms",
    "present": ["public_data_license_v1.0", "PDL1.0"]
  },
  {
    "id": "saitama-env-page",
    "claim": "The 生活衛生 page offers the FY-end list (r7nenndo.zip) and the monthly files to 2026-08 (r0804 to r808). A failure on r808 means a newer month: re-measure",
    "kind": "http_contains",
    "url": "https://www.pref.saitama.lg.jp/a0706/6hou/ichiran.html",
    "present": ["r7nenndo.zip", "r0804.xlsx", "r808.xlsx"]
  },
  {
    "id": "saitama-env-zip",
    "claim": "The FY-end 生活衛生 list (1,203,694 B, 2026-03-31) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.pref.saitama.lg.jp/documents/232288/r7nenndo.zip",
    "min_bytes": 1000000
  },
  {
    "id": "ageo-mhlw-live",
    "claim": "MHLW's open-data file for Saitama Prefecture's jurisdiction (11000) answers a plain keyless GET (a control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11000_food_business_all.csv",
    "min_bytes": 4000000
  },
  {
    "id": "ageo-isj-block-live",
    "claim": "MLIT's block-level address file for Ageo (11219) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11219-24.0a.zip",
    "min_bytes": 120000
  },
  {
    "id": "ageo-isj-chome-live",
    "claim": "MLIT's town-chōme file for Ageo (11219) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/11219-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "ina-isj-block-live",
    "claim": "MLIT's block-level address file for Ina (11301) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11301-24.0a.zip",
    "min_bytes": 50000
  },
  {
    "id": "ina-isj-chome-live",
    "claim": "MLIT's town-chōme file for Ina (11301) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/11301-19.0b.zip",
    "min_bytes": 4000
  },
  {
    "id": "ageo-jr-ageo-timetable",
    "claim": "JR East's timetable index for 上尾 (list0042) links the two weekday Takasaki Line pages read (0042010, 0042020). ASCII ids only",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0042.html",
    "present": ["tt0042/0042010.html", "tt0042/0042020.html"]
  },
  {
    "id": "ageo-jr-kitaageo-timetable",
    "claim": "JR East's timetable index for 北上尾 (list0549) links its two weekday pages (0549010, 0549020)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0549.html",
    "present": ["tt0549/0549010.html", "tt0549/0549020.html"]
  },
  {
    "id": "ina-new-shuttle-timetable",
    "claim": "The New Shuttle's 伊奈中央 timetable page carries the weekday timetable images counted here (toward 大宮: inamachi_nobori)",
    "kind": "http_contains",
    "url": "https://www.new-shuttle.jp/station/inachuo/inachuo_timetable/",
    "present": ["inamachi_nobori.gif", "inamachi_kudari.gif"]
  },
  {
    "id": "ageo-projected-crs",
    "claim": "Ageo (Regional) projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.59,
    "expect": "EPSG:32654"
  }
]
```
