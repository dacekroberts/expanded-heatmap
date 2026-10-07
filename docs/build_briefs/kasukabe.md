# Kasukabe — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5: `docs/decisions_drafts/staging.md`, "Wave 5, second half: calls 95 to 141";
the band row in `docs/city_master_list.md`, "As Tokorozawa", calls 101 and
143). The Step 0 downloads were approved by the owner 2026-10-06 (calls 106
and 147). **Step 0 measured 2026-10-06** (staging), each file from its
publisher's own host with the project user-agent, each HTTP 200:

- **Shared by the four Saitama briefs, in `data/saitama_pref/raw/`**: the two
  live food layers (`food_shinpo_layer_20261006.geojson`, 52,706 features;
  `food_kyuho_layer_20261006.geojson`, 2,627), the R8.3.31 lists
  `shinpo_R080331.xls` and `kyuho_R080331.xls`, the 生活衛生 list
  `r7nenndo.zip` and its twelve monthly files. Hosts, bytes and how each was
  fetched: `docs/build_briefs/tokorozawa.md`, header.
- **Into `data/kasukabe/raw/`**: `11000_food_business_all.csv` (5,456,396 B,
  MHLW, a control only; a copy of the one prefecture file); from
  `nlftp.mlit.go.jp` `isj/11214-24.0a.zip` (245,739 B) and
  `isj/11214-19.0b.zip` (6,927 B).
- Timetables read (counts only): Tōbu's own timetable service
  (`transfer-internal.navitime.biz/tobu/`, 春日部's Skytree Line pages both
  ways and the Urban Park Line to 柏), plus the wave-5 probe's saved page for
  the Urban Park Line to 大宮.

Nothing else was downloaded.

**Run `python scripts/brief_check.py kasukabe` before writing any code.**
Then the `japan-city` skill. **Read `docs/build_briefs/tokorozawa.md` first**:
the prefecture's files, their columns, the shared-code change (the "NN:" type
code), the partial old-law layer and the proposed three-file food source,
the jurisdiction-wide e-Stat and MHLW measurements, the licence and privacy
positions are measured there once and hold here; this brief gives
Kasukabe's own figures. Rows are assigned to Kasukabe by address prefix
(`春日部市…`), Matsudo's method. Coordinates: the `address-join` skill with
`japan_register` from scratch scripts only. Rail: N02-25 cut at the N03 city
line, an in-memory `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left
out, its station kept through the other lines, and drawn cut only where no
other line serves that station (owner, 2026-10-06, calls 54 and 92); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor
for JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at
about 11 trains a day or fewer named and drawn (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Kasukabe carries `label_tier: "minor"` and goes in the **Japan East** view
(`app/cities.py`); wave 4's first city to land retags Japan into the eight
regions, Kasukabe into **Kanto**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.
Kasukabe sits north of Koshigaya and Sōka on the same Skytree Line: measure
the labels together if they land in one batch.

**✅ `mode`: `metro`**, the mode following the backbone (Matsudo's and
Kurume's precedent; Sakura's call 121): Tōbu's two railways (N02 class 12)
hold all 8 station groups; no JR, subway or tram.

---

## The one-line summary

**Two buckets, three kinds, from Saitama Prefecture's own files (PDL 1.0 by
the GIS catalogue; the 生活衛生 files on the 2024 PDL record, relied on, call
143).** The live new-law layer holds **1,266 restaurant permits** in Kasukabe
(1,265 in term); the live old-law layer, a partial load, 137 (112 in term),
where the R8.3.31 old-law list holds 224 in term on 2026-10-06. With the
old-law list (Tokorozawa's open call 1): **1,475 restaurant permits, 2.10 per
2021 census establishment**, about **81%** of the census-scaled estimate
(the jurisdiction's municipalities run 1.87-2.60). Through `japan_eigyo`,
the type code stripped: **Food service 1,483, Retail 844** (553 of them
notifications). Barbers **188**, beauty salons **448**, laundries **79**
(the 2026-03-31 list plus new premises to 2026-08-31): 92%, 98% and 89% of
census-scaled estimates. Block join **96.4%** (food), 94.9-98.9%
(registers). **Rail: 8 station groups**, all Tōbu (Skytree Line 4, Urban Park
Line 5, 春日部 shared), 118 to 240 weekday departures each way at 春日部.

---

## Business leg — food

The prefecture's files, columns, type codes and the partial old-law layer:
`docs/build_briefs/tokorozawa.md`, "Business leg — food". Kasukabe is in the
prefecture's jurisdiction (春日部保健所; permit numbers 指令春保…; the health
centre also covers 松伏町).

| Source | Rows, 春日部市 | Restaurants | In term 2026-10-06 |
|---|---|---|---|
| Live new-law layer | **2,438** (880 notifications, 1,558 permits) | **1,266** | 1,265 |
| Live old-law layer | **204** | 137 | **112** (52 rows, 25 restaurants, ended 2025-03-31 to 2026-09) |
| R8.3.31 old-law list (`kyuho_R080331.xls`) | **513** | 312 | **224**, of them 89 in the live old-law layer |
| R8.3.31 new-law list (`shinpo_R080331.xls`) | 2,299 | 1,138 | 1,137, all but 3 in the live layer |

- **Every address starts with 春日部市**; 4 of 2,438 new-layer rows have their
  point outside the city line, and no point inside it carries another
  municipality's address.
- **The old-law trap, both ways**: the live old-law layer keeps 52 rows whose
  permit had already ended (from 2025-03-31) and 17 old-law rows beside a
  new-law row at the same (address, name, type), the renewal, while missing
  most of the old-law permits still in term. Of the old-law list's 224
  restaurants in term: 89 in the old layer, 11 renewed into the new layer by
  (address, name), 38 with only the address or name in the new layer, **86
  nowhere** (their end dates 2026-11 to 2027-09, 41 of them 2027-03).
- **The proposed set** (Tokorozawa's open call 1, the same rule): new-law
  rows in term, plus old-law rows from the list and the old layer, in term on
  the as-of, one per (address, name, type) and per permit number and type, an
  old-law row dropped where the new layer holds the same (address, name) and
  type: old-law **391 in term, 8 renewed, 383 kept** (210 restaurants, 8
  cafés), all from the list (the old layer's in-term rows are all in it).
  **Restaurants 1,265 + 210 = 1,475.** The old-law rows are an upper bound
  (closures since 2026-03-31 unseen).

### Types, notifications, dates

- **Live new-law layer (2,438)**: 飲食店営業 1,266, その他の食料・飲料販売業 266,
  菓子製造業 125, コップ式自動販売機 124, コンビニエンスストア 99, 百貨店、総合スーパー
  68, 集団給食施設 64, 自動販売機による販売業 52, 乳類販売業 47, その他の食料品製造・加工業
  47, 食肉販売業 39, … 45 types.
- **880 notifications** (no start or end date): その他の食料・飲料販売業 265,
  コップ式自販機 124, コンビニ 99, 百貨店・スーパー 68, 集団給食 64, 自販機 52, 乳類
  販売 47, その他の食料品製造・加工業 47, 野菜果物 29, …: Retail by Tokyo's rule,
  complete as published.
- **Permits (1,558)**: start 2021-06-01 to **2026-12-01**, end 2026-07-31 to
  2033-01-31; 1 ended before 2026-10-06 (a restaurant). **10 rows start after
  2026-10-06** (8 restaurants), 1 with a current twin (Tokorozawa's open call
  2).
- **Old-law list (513)**: 飲食店営業 312, 給食施設 83, その他の製造業 30, 菓子製造業 23,
  食肉販売業 16.
- **No 業態, no vehicle or hostess marker** (0 trade names read as a vehicle):
  snack bars and kitchen cars stay in Food service (R3).

### Duplicates and closed premises

- **47 groups repeat an (address, trade name, type)** across the live layers:
  27 new-law pairs, 15 an expired old-law row beside its new-law renewal, a
  few triples (restaurants 29, 菓子 4, cup vending 3). The proposed set drops
  the expired and renewed rows; one pin per premises and bucket does the rest.
- **1,586 distinct points for 2,642 layer rows** (up to 69 on one point).
- Closures: as Tokorozawa's (the live layers drop them; the old-law rows
  cannot be checked). The page keeps "may include closed premises".

### Counts through `japan_eigyo` (the proposed set, type code stripped)

**Food service 1,483** (new law 1,265, old law 218), **Retail 844** (from
notifications 553: other food and drink sales 265, konbini 99, supermarket
68, dairy 47, greengrocer 29, butcher 20, fishmonger 16, bento 5; from
permits: 菓子 142, butcher 51, fishmonger 45, deli 45): **2,327 storefront
rows, 2,133 pins** (Food service 1,466, Retail 667). Left out: vending 183,
institutional catering 147, mail order 2, and 161 with no rule (その他の食料品製造・
加工業 47, その他の製造業 30, コーヒー製造・加工業 12, 漬物製造業 10, 麺類製造業 7, 食肉処理業
7, …). Not a premises by address: 0. The "other food and drink sales"
catch-all is **31% of Retail** (266 of 844). **Today's shared code** (the
"NN:" code left on) buckets 433 Retail rows of the live layer where the
stripped type gives 843.

**Coverage, a model**: 1,475 restaurant permits on 703 census
establishments, **2.10**, against the jurisdiction's e-Stat 2.60 (33,897 /
13,019) and the core cities' 2.46-3.08: **about 81% of a census-scaled 1,830**
(the live layers alone 1,377, 75%). Kasukabe sits at the jurisdiction's
median (2.10 of 1.87-2.60), so the shortfall is the jurisdiction's, not the
city's: e-Stat's count is eighteen months older and counts permits to their
term, and the publisher withholds some premises at the operator's request.
**MHLW's file** holds **72 open, addressed restaurant permits** with a
Kasukabe address (of 344 rows: 届出 239, 許可 105; granted 2021-11-16 to
2026-08-14): **68 (94.4%)** are in the live layers by permit number, name or
address, **61 (84.7%)** by number or (address and name), the number key weak
here (MHLW writes many of Kasukabe's numbers bare, `3-123`). Open call 1
below.

**Economic Census control**: 1,466 distinct placed Food-service premises on
703 establishments, **2.09**, above the built cities' 1.56-1.92. Record the
figure and the reading (Tokorozawa's).

## Business leg — personal services: 生活衛生営業施設一覧, page 232288

The page, the files and their columns: `docs/build_briefs/tokorozawa.md`.
**Kasukabe is in `03春日部保健所管内.xlsx`** (春日部市 and 北葛飾郡松伏町), sheets
理容所 (202 rows), 美容所 (474), クリーニング (89), 旅館, 公衆浴場, 興行場 (out of
scope); `city_rows` reads it by `r7nenndo.zip::03春日部`.

- **The months**: 2025-09 to 2026-03 hold 4 Kasukabe rows (beauty 3,
  laundry 1), all already in the year-end list; 2026-04 to 2026-08 add
  **beauty 5**, and 1 barber row that is already in the list (a
  re-confirmation at the same address and name). Ichinomiya's precedent (call
  126), an upper bound, `as_of` 2026-08-31.

| Kind | List 2026-03-31 | + months to 2026-08 | Census 2021 | Scaled estimate | Share |
|---|---|---|---|---|---|
| 理容所 | **188** | 188 | 187 | 205 | **92%** |
| 美容所 | **443** | **448** (447 premises) | 305 | 458 | **98%** |
| クリーニング所 | **79** | 79 | 74 (洗濯業) | 89 | **89%** |

(Scaled by the jurisdiction's licensed-to-census ratios, barbers 1.099,
beauty 1.500, laundries 1.200: Tokorozawa's brief. A modelled figure; the
lists are 98.2%, 100.4% and 94.9% of e-Stat across the jurisdiction.)

- **Laundry kinds**: 49 受取及び引渡しのみ (取次所, counted), 30 受取、処理及び引渡し;
  no blank kind and no リネンサプライ in Kasukabe.
- **Repeats**: beauty 1 (address, name). 確認年月日 as Tokorozawa's (slashes and
  Shōwa dates, unread, unused).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards**. Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11214-24.0a.zip` (245,739 B,
**41,105 block keys**), town-chōme `.../19.0b/11214-19.0b.zip` (6,927 B,
**143**). `japan.CITIES` entry at build: `"kasukabe": {"name": "春日部市",
"pref": "11", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["11214"]}`.

| Tier, today's shared code | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| Food, the proposed set (2,327) | **96.4%** | 3.4% | **0.1%** (3) |
| … Food service (1,483) / Retail (844) | 97.0 / 95.4 | 3.0 / 4.3 | 0.0 / 0.4 |
| … old-law list rows, no own point (267) | 95.5 | 4.5 | 0.0 |
| Barbers (188) | **98.9%** | 1.1% | 0.0% |
| Beauty salons (448) | **97.1%** | 1.1% | **1.8%** (8) |
| Laundries (79) | **94.9%** | 3.8% | 1.3% (1) |

- **The layer's own points** against the block point: median **49 m**, 85.9%
  within 100 m, 96.4% within 250 m, 4 over 1 km (2,180 rows); against the
  chōme centroid, median 340 m (78 rows). **The 3 unplaced food rows** are
  addresses in 下柳 naming the AEON Mall with no number; each carries its own
  layer point inside the city (call 127c's precedent).
- **Chōme tier, read** (towns only): the rural 大字 east and north, where MLIT
  lacks the 地番 (増田新田 10, 赤沼 8, 榎 7, 大場 7, 一ノ割 5, 増戸 4, 谷原新田 5,
  不動院野 5, …), and **八丁目**, a 大字 whose name `norm_town` turns into `8丁目`
  (6 food rows at the chōme tier; MLIT keys the town 八丁目, code
  112140069008). Read at build whether its blocks are keyed under the same
  normalised name.
- **The register misses**: 7 rows written `備後東西…` (beauty 6, laundry 1),
  where MLIT holds 備後東 1-8丁目 and 備後西 1-5丁目 only: the register's
  spelling, read at build (the food layers write 備後東 and 備後西). Then
  牛島前田 1 and one 南… address with a building, 1 each. No register row
  has an own point; at 1.8% unplaced, the beauty layer stays above call 145's
  threshold for disclosed tiers.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`N02-25_GML.zip` and `N03-20250101_11_GML.zip`, N03 code 11214 (**66.0 km²**,
extent W 139.708, S 35.936, E 139.833, N 36.043; the 2005 merger brought in
庄和町).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 伊勢崎線 (東武鉄道, 12) | Tōbu Skytree Line | **4 / 55** | 一ノ割, 春日部, 北春日部, 武里 |
| 野田線 (東武鉄道, 12) | Tōbu Urban Park Line | **5 / 35** | 豊春, 八木崎, 春日部, 藤の牛島, 南桜井 |

- **9 station records, 8 N02_005g groups** (春日部 Skytree + Urban Park, 27 m).
  No name in two groups; no pair closer than 600 m. **Median nearest-station
  gap 1,802 m** (935 to 2,734).
- **Shinkansen**: none.
- **Cut at the line**: the Skytree Line 51 beyond (other prefectures 32,
  越谷市 6, 草加市 4, 宮代町 3, …), the Urban Park Line 30 (other prefectures
  23, さいたま市 7). Neither is a stub.
- **The light-rail/rail test**: both heavy rail (class 12).
- **Frequency**, weekday departures at 春日部 counted whole from Tōbu's own
  timetable service (read 2026-10-06; the 2026-03-14 timetable):

  | Station (line, direction) | Weekday departures | Per hour, 07-18 |
  |---|---|---|
  | 春日部 (Skytree, to 浅草) | 240 | 10-22 |
  | 春日部 (Skytree, to 伊勢崎) | 239 | 11-15 |
  | 春日部 (Urban Park, to 大宮) | 148, of them **132 普通** | 8 |
  | 春日部 (Urban Park, to 柏・船橋) | 118 | 5-8 |

  The stations west of 春日部 on the Urban Park Line (八木崎, 豊春) are served
  by the 普通 at least (132 a weekday toward 大宮); 武里 and 一ノ割 by the
  Skytree Line's stopping trains (not read per station). **No stretch comes
  near about 11 trains a day** (call 86). Only counts are recorded.
- ⚠️ **Gate 3** at build: Tōbu's station counts inside the city (Skytree 4,
  Urban Park 5). **OSM `name:en`** for 8 groups (one Overpass query at build).

## Scope

**Kasukabe City.** The Skytree Line runs on to 浅草 (through Koshigaya and
Sōka) and to 伊勢崎, the Urban Park Line to 大宮 and to 柏 and 船橋: cut at the
line.

## Licences — as read by staging (2026-10-06)

As Tokorozawa's: **the food layers and the R8.3.31 lists PERMITTED WITH
CONDITIONS** (the GIS catalogue applies the prefecture's open-data terms,
PDL 1.0); **the 生活衛生 files on the 2024 PDL record, relied on** (owner,
call 143); the portal's processed-use credit as staging recorded it. MHLW
(control), MLIT ISJ and N02 PDL 1.0; N03 CC BY 4.0 (never drawn); e-Stat a
measurement; timetables counts only. The notice number is claimed at build.

## Privacy

- **The food files carry 申請者_氏名**: in the proposed set **1,697 rows with a
  company or co-op marker, 1,123 without** (158 of those from the old-law
  list). Read in memory for the name rule only; phones never selected (the
  shared GeoJSON's 申請者_氏名: Tokorozawa's note).
- **The name rule, measured in memory**: **7 food rows** whose trade name is
  the operator's own name (0 bare personal names), **0 among fixed premises
  in a bucket**. Registers: **0** in every kind. Operators without a company
  marker: barbers 179 of 188, beauty 331 of 443, laundry 30 of 79.
- Run `check_personal_exposure.py kasukabe` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.708-139.833 E, centroid 139.776,
35.983: project to **UTM 54N (EPSG:32654)** (computed here, never copied). OSM
box from the N03 extent, rounded out: (35.93, 139.70, 36.05, 139.84).
**Scaffold**: `scaffold_city.py --slug kasukabe --name Kasukabe --system-name
"Tōbu Railway" --taxonomy japan_eigyo --lat 35.983 --lon 139.776 --region
"Japan East" --country Japan --mode metro --page-number <N>` (`--dry-run`
first), the page number claimed at build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band A on the
prefecture's food layers and personal-services lists; `mode: metro`; the minor
tier and Japan East (Kanto after the retag); no frequency floor; the licence
positions (call 143); the registers' months merged (call 126); notifications
in Retail (Tokyo's rule); the publisher's own point where the block join
misses (call 127c).

**Answered by the owner on 2026-10-06:** call 171, **the R8.3.31 old-law list added to the food source** for the four Saitama pages (Ageo (Regional), Sōka, Tokorozawa, Kasukabe), with the live new-law and old-law layers, in term on the as-of, de-duplicated, renewals dropped, **and disclosed** on the page: the old-law rows are an upper bound as of 2026-03-31, closures since unseen (Kyoto's disclosure). Also call 172, **rows that start after the as-of are dropped** until they are in term (`in_term`'s mirror); call 173, **no food-share sentence**: the publisher's withholding note is disclosed with no number (Matsudo's precedent), with the old-law upper bound. The recommendations below are kept as the record.

**Weighed, with a recommendation** (the same three as Tokorozawa's; decided once for the four Saitama cities):

1. **Add the R8.3.31 old-law list to the food source.** *Recommend it*:
   1,475 restaurants against 1,265 (+210, about 17%), the old-law rows an
   upper bound disclosed as Kyoto's. Tradeoff as Tokorozawa's.
2. **Rows that start after the as-of** (10 here, 8 restaurants). *Recommend
   dropping them* until they are in term.
3. **A stated food share on the page?** Kasukabe's census-scaled estimate is
   about 81%. *Recommend none*: the figure is a model, and Kasukabe sits at
   the jurisdiction's median, so the shortfall is the source's age and the
   publisher's withholding, not the city; disclose the withholding note with
   no number (Matsudo's precedent) and the old-law upper bound. The tradeoff:
   a reader is not told that about a fifth of restaurant permits may be
   missing. If the owner wants a figure, state it the way Ichinomiya's food
   share is stated (call 125), marked as an estimate.

## What the build must still measure

- Everything in Tokorozawa's list (the `normalise` change and its controls,
  `fetch_sources.py` for the shared prefecture files, the as-of dates).
- **八丁目**'s block keys; the 7 `備後東西` register rows; the 3 AEON Mall rows
  on their own points.
- The census ratio (2.09) and its reading; the old-law rows' share (210 of
  1,475) if open call 1 is taken.
- Gate 3; OSM `name:en`; line colours on both basemaps; the opening view
  (`map-view`); the factory share; `check_provenance.py`;
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "kasukabe-food-new-layer",
    "claim": "The live new-law food layer (shared with Tokorozawa): points, 52,706 rows on 2026-10-06, edited within 30 days",
    "kind": "arcgis_layer",
    "url": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/%E9%A3%9F%E5%93%81%E5%96%B6%E6%A5%AD%E6%96%BD%E8%A8%AD_%E6%96%B0%E6%B3%95_%E5%85%AC%E9%96%8B/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 52706,
    "tolerance": 3000,
    "present": ["施設_名称", "施設所在地", "業種名", "有効開始年月日", "有効終了年月日", "許可番号"],
    "max_age_days": 30
  },
  {
    "id": "kasukabe-food-old-layer",
    "claim": "The live old-law food layer: 2,627 rows, the partial load (a jump toward 10,000 means it was reloaded: re-measure open call 1)",
    "kind": "arcgis_layer",
    "url": "https://services9.arcgis.com/n65w8AXGaYPTqFYI/arcgis/rest/services/%E9%A3%9F%E5%93%81%E5%96%B6%E6%A5%AD%E6%96%BD%E8%A8%AD_%E6%97%A7%E6%B3%95_%E5%85%AC%E9%96%8B/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 2627,
    "tolerance": 500,
    "max_age_days": 90
  },
  {
    "id": "kasukabe-kyuho-item",
    "claim": "The edition measured: the R8.3.31 old-law list, kyuho_R080331.xls, 2,542,080 B",
    "kind": "http_contains",
    "url": "https://pref-saitama.maps.arcgis.com/sharing/rest/content/items/7da15c2811db4a55953345b16299d462?f=json",
    "present": ["kyuho_R080331.xls", "\"size\":2542080"]
  },
  {
    "id": "kasukabe-gis-catalogue",
    "claim": "The GIS open-data catalogue page lists the R8.3.31 items and applies the prefecture's open-data terms (準用)",
    "kind": "http_contains",
    "url": "https://pref-saitama.maps.arcgis.com/sharing/rest/content/items/d252024b403d49519b2166f4604a1bed/data?f=json",
    "present": ["7da15c2811db4a55953345b16299d462", "準用"]
  },
  {
    "id": "kasukabe-seikatsu-page",
    "claim": "Page 232288 offers the 2026-03-31 list and the monthly files through 2026-08; ASCII anchors, the host sends no charset",
    "kind": "http_contains",
    "url": "https://www.pref.saitama.lg.jp/a0706/6hou/ichiran.html",
    "present": ["/documents/232288/r7nenndo.zip", "/documents/232288/r808.xlsx"]
  },
  {
    "id": "kasukabe-mhlw-live",
    "claim": "MHLW's open-data file for the prefecture's jurisdiction (11000) answers a plain keyless GET (a control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11000_food_business_all.csv",
    "min_bytes": 4000000
  },
  {
    "id": "kasukabe-isj-block-live",
    "claim": "MLIT's block-level address file for Kasukabe (11214) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11214-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "kasukabe-isj-chome-live",
    "claim": "MLIT's town-chōme file for Kasukabe (11214) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/11214-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "kasukabe-tobu-skytree",
    "claim": "Tōbu's timetable for 春日部, Skytree Line toward 浅草 (240 weekday departures)",
    "kind": "http_contains",
    "url": "https://transfer-internal.navitime.biz/tobu/pc/diagram/BusDiagram?linkId=00000798&nodeId=00003591&updown=0",
    "present": ["春日部", "スカイツリーライン", "浅草"]
  },
  {
    "id": "kasukabe-tobu-urban-park",
    "claim": "Tōbu's timetable for 春日部, Urban Park Line toward 柏・船橋 (118 weekday departures)",
    "kind": "http_contains",
    "url": "https://transfer-internal.navitime.biz/tobu/pc/diagram/BusDiagram?linkId=00000810&nodeId=00003591&updown=1",
    "present": ["春日部", "アーバンパークライン"]
  },
  {
    "id": "kasukabe-projected-crs",
    "claim": "Kasukabe projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.776,
    "expect": "EPSG:32654"
  }
]
```
