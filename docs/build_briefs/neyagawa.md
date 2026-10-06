# Neyagawa — build brief

**Band B, owner-approved 2026-10-06** (Japan wave 4, staging's wave 5, call
114: `docs/decisions_drafts/staging.md`, "Wave 5, second half", and the
master list's row: "Personal services only (Kōchi's shape)"). **Counted
first: 630 premises** (566 barbers and beauty salons, 64 laundries), **over
the floor** the owner set at Minoh's page (about 294 premises, calls 115 and
166): Neyagawa is not under it. The Step 0 downloads were approved by the
owner 2026-10-06 (calls 106 and 147). **Step 0 measured 2026-10-06**
(staging). Each file from its publisher's own host with the project
user-agent, each HTTP 200, under each URL's own file name as `japan_fetch.get`
saves:

- From `data.bodik.jp` (the city's organization `272159`), into
  `data/neyagawa/raw/`, 22 s between calls: `272159_barber_20260831.csv`
  (19,507 B), `272159_hair_dressing_20260831.csv` (57,980 B) and
  `272159_cleaning_20260831.csv` (10,176 B), each as of 2026-08-31.
- From `nlftp.mlit.go.jp`, into `data/neyagawa/raw/isj/`: `27215-24.0a.zip`
  (106,271 B) and `27215-19.0b.zip` (7,487 B).

Nothing else was downloaded. **No monthly companion exists**: each package
holds one FULL list per month (令和4年2月 to 令和8年8月), never an additions
file, so the newest edition is the whole register (Funabashi's shape, not
Kōchi's or Ōsaka Prefecture's). MHLW's file for 27215 was not fetched: food
is off (below), and `docs/coverage_sweep/japan_universe_mhlw.csv` already
holds its counts.

**Run `python scripts/brief_check.py neyagawa` before writing any code.** Then
the `japan-city` skill, **Kōchi's page shape** (`docs/build_briefs/kochi.md`,
personal services only) with **Funabashi's reader** (`docs/build_briefs/funabashi.md`:
a city's own BODIK lists, three kinds, one snapshot per kind). Coordinates:
the `address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only. Rail: MLIT N02-25 cut at the N03 city line,
through `pipeline/countries/japan.py` with an in-memory `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left
out, its station kept through the other lines, and drawn cut only where no
other line serves that station (owner, 2026-10-06, calls 54 and 92); (4)
**菓子製造業 and そうざい製造業 count, in Retail** (moot on a personal-services
page); (5) **the name rule**, version 2 (2026-10-06): a bare personal name is
withheld whatever the operator column holds; (6) **no page says "currently
operating"**. Also: no frequency floor for JR or private lines in Japan
(owner, 2026-10-06, call 46), any stretch at about 11 trains a day or fewer
named and drawn (call 86; none here); fault-based cost clauses accepted for
all of Japan (2026-09-24); English station names from OSM `name:en`; every
Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Personal services only (owner, 2026-10-06, call 114, the band row):**
barbers, beauty salons and laundries, the city's three BODIK lists; no food
list (below). Yokohama's approved one-bucket line ("barbers, beauty salons
and laundries") fits word for word: **no new page sentence**. Thinner than
Hakodate (1,077 storefronts) and Kōchi (1,406), thicker than Minoh (294) and
Kadoma (339).

**✅ JR's 寝屋川公園 kept as cut (owner, 2026-10-06, the band row):** the
Gakkentoshi Line has one station in the city and no other line serves it;
JR and private one-station stubs stay as cut (standing call 3).

**✅ Four station groups (owner, 2026-10-06, the band row states 4).** The
fewest of any Japanese page so far (Minoh and Kadoma 5); above call 130's
discard line (fewer than 3).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
`label_tier: "minor"`, the **Japan West** view today and **Osaka Prefecture**
after wave 4's retag. Its dot sits about 4.5 km north-northeast of Kadoma's
and 7.7 km southwest of Hirakata's: whether it joins `KNOWN_STACKED` with
either is `check_macro_labels.py`'s answer (PROBLEMS 0 at 375, 768 and 1200),
never by eye.

**✅ `mode`: `metro`.** Keihan 3 station groups against JR's 1: Hirakata's
precedent (owner's rule of 2026-10-02, "unless there is substantial JR, JR
reads as metro"); Keihan's Main Line is a railway (N02 class 12), not a tram.

---

## The one-line summary

**One bucket from the city's own lists on BODIK (CC BY 4.0 as stated; the
licence read is pending, staging records it): 155 barbers, 419 beauty salons
and 64 laundries as of 2026-08-31, 638 rows, 630 premises.** Against e-Stat's
FY2024 in-force counts for the city (a core city, so its own row): **97.5%,
102.7% and 90.1%**. **Block join 99.7%, 0 unplaced.** No food list (MHLW's
file for the city: 30 open restaurant permits, 23 addressed, against 783
restaurants in the 2021 census). **Rail: 4 station groups**: Keihan Main Line
3 (萱島, 寝屋川市, 香里園), JR Gakkentoshi Line 1 (寝屋川公園, cut); every one
well over 11 trains a day.

---

## Business leg — the city's 生活衛生 lists (BODIK organization 272159)

| | Barbers | Beauty salons | Laundries |
|---|---|---|---|
| **Dataset** | `https://data.bodik.jp/dataset/272159_barber` | `…/272159_hair_dressing` | `…/272159_cleaning` |
| **Title** | 理容所確認施設一覧 | 美容所確認施設一覧 | クリーニング所確認施設一覧 |
| **Resource name** | 理容所確認施設一覧（令和8年8月31日時点） | 美容所確認施設一覧（同） | クリーニング所確認施設一覧（同） |
| **File** | `…/dataset/d7f05be4-01d8-4150-8b9b-c5146a906187/resource/1eea6cda-ffbd-4d7a-9b3b-f740ad231aca/download/272159_barber_20260831.csv` | `…/dataset/aa79fd70-d439-4bbf-b393-b94e2f7fa385/resource/19110291-e84f-44fe-814f-d26f1cd70cd9/download/272159_hair_dressing_20260831.csv` | `…/dataset/71f93e97-3a93-479c-a634-106367c70b85/resource/3824bb1f-7b7b-4fba-9481-cf954a955caf/download/272159_cleaning_20260831.csv` |
| **Bytes** (catalogue = served) | 19,507 | 57,980 | 10,176 |
| **Rows** | **155** | **419** | **64** |
| **As of** (resource name) | **2026-08-31** | **2026-08-31** | **2026-08-31** |
| 確認年月日 | 1960-11-17 .. 2025-12-17 | 1963-11-21 .. 2026-08-27 | 1960-12-23 .. 2026-03-27 |
| Before 2000 / since 2021 / since 2026-04 | 91 / 15 / 0 | 95 / 135 / 7 | 24 / 7 / 0 |
| Resource added | 2026-09-04 | 2026-09-04 | 2026-09-04 |

- **The city's own catalogue** (`https://www.city.neyagawa.osaka.jp/material/files/group/79/272159_open_data_list.csv`,
  76 entries, linked from the オープンデータ一覧 page): all three lists,
  分類 商業・サービス業, 更新頻度 **月次**, ライセンス **CC-BY4.0**, last updated
  2026/9/4. BODIK's `frequency` extra is blank.
- **Format**: cp932, comma-separated, CRLF, one header row; `city_rows` reads
  all three as they are (`decode` takes cp932).
- **Columns** (the same fourteen): 都道府県コード又は市区町村コード (272159),
  NO, 都道府県名, 市区町村名, **施設名称**, 名称_カナ (empty), **施設所在地**
  (from the city: 寝屋川市…), 方書 (empty), 施設電話番号, 法人営業者名称,
  **営業者名称（法人の場合は代表者氏名）**, 営業者所在地（法人のみ）,
  **確認年月日** (era kanji: 昭和/平成/令和), **営業種別**. ⚠️ The beauty
  file's first header cell is blank, and it adds a fifteenth unnamed column
  holding one note on one row (a character outside the code page written ※,
  in that row's operator column, never selected). `city_rows` keys both
  blank headers as `""`, so the code column is lost there: harmless, nothing
  reads it.
- **営業種別 is the kind**: 理容所 155; 美容所 411 and **化粧・結髪等の業 8**
  (美容所 confirmed for make-up and hair-arranging only, kept: a beauty
  register counts whole except mobile and welfare-facility salons,
  `japan_eigyo`); 取次 38, 一般 21, 一般(特定洗濯) 5. ⚠️ `TYPE_COLS` has no
  営業種別, so every row reads type ""; the bucket is still right
  (`japan_eigyo` decides by source) and nothing falls out. The name rule's pin
  shows the TYPE: map 営業種別 in `source_rows` (Funabashi's route).
- **No storeless pick-ups, linen plants or mobile salons** (no 無店舗, リネン or
  移動 kind). e-Stat counts **90 無店舗取次店 operators** in the city: not
  premises, not in the list.
- **Dates**: `japan_register.wareki_date` reads 平成 and 令和 and returns None
  for every 昭和 date (67 barber, 64 beauty, 17 laundry rows). Nothing in the
  build reads it (a 生活衛生 confirmation has no expiry); the ranges above
  come from a scratch parser.

### Snapshot, not rebuild

Each package keeps **one full list per month** since 2022 (55-57 resources),
not a full list plus additions. The newest edition is the register; older
editions are superseded, not merged (Ichinomiya's call 126 does not apply:
there is no addition file to merge). The files **shrink as well as grow**
(the beauty list 57,753 B in April, 57,407 B in May, 57,980 B in August), so
closures leave the list between editions: a snapshot, not an upper bound in
Kyoto's or Kōchi's sense. **No dataset states that any premises are
withheld.** Pin `as_of` to **2026-08-31**, never the download date.

### Coverage against the official counts

Neyagawa is a 中核市 (since 2019), so 衛生行政報告例 FY2024 第10表 and 第11表
carry its own row, 大阪府寝屋川市
(`data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
`…_cleaning_by_city.csv`, on disk, read here, not downloaded):

| Kind | Official FY2024 (2025-03-31) | The city's list (2026-08-31) | Share | 2021 census establishments (27215) | Per establishment |
|---|---|---|---|---|---|
| 理容所 | **159** | **155** | **97.5%** | 理容業 154 | 1.01 |
| 美容所 | **408** (重複開設 none) | **419** (美容所 411) | **102.7%** (100.7%) | 美容業 246 | 1.70 |
| クリーニング所 | **71** (取次所 46, 指定洗濯物 5) | **64** (取次 38, 特定洗濯 5) | **90.1%** (取次 82.6%) | 洗濯業 64 | 1.00 |

- Lists 17 months younger than the count. Barbers 4 fewer is a shrinking
  trade, beauty slightly over: complete registers. Laundries 7 fewer, all
  取次 (pick-up counters, the most transient kind); well above Maebashi's 82%
  (built and stated, owner 2026-10-05) and Ichihara's 81% (call 123): no call.
- FY2025's tables, when e-Stat publishes them, are a closer control.

### Duplicates and closed premises

- **Repeats**: 1 beauty (address, trade name) twice; 7 beauty addresses and 1
  laundry address carry two premises under different names. **7 premises are
  in both the barber and the beauty list** by (address, trade name) (e-Stat
  reports no 重複開設 for the city), and 16 addresses hold both kinds. One pin
  per premises and bucket leaves **566 barber and beauty pins from 574 rows**
  and **630 pins in all** (laundries: 64 from 64).
- **Closures are not marked** (no closure field; see the snapshot note). Not
  a premises: **0**.

### No food list (disclosed)

- The wave-5 probe enumerated the city's catalogue (76 entries) and its
  health-centre food pages: **no food permit list**.
- **MHLW** (`docs/coverage_sweep/japan_universe_mhlw.csv`, the 27215 row):
  **30 open restaurant permits, 23 with an address** (latest 2026-08-24)
  against **2,189 in force** and **783** 飲食店 establishments in the 2021
  census: cover **0.01**. Food service and Retail stay off (open call 1).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards**. Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27215-24.0a.zip` (106,271 B,
**4,764 block keys**), town-chōme `.../19.0b/27215-19.0b.zip` (7,487 B,
**177**). `japan.CITIES` entry at build: `"neyagawa": {"name": "寝屋川市",
"pref": "27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["27215"]}`.

| Tier, today's shared code | Block | Town-chōme | Unplaced |
|---|---|---|---|
| Barbers (155) | **100.0%** | 0 | 0 |
| Beauty salons (419) | **99.5%** | 0.5% (2) | 0 |
| Laundries (64) | **100.0%** | 0 | 0 |
| All (638) | **99.7%** | 0.3% | **0** |

- **The two chōme-tier rows, read** (towns and address shapes only):
  明徳1丁目 and 上神田1丁目, each written 丁目 + number, where MLIT has the
  chōme (15 and 39 block keys) but not that block number. They take the
  chōme's centroid. 3 rows were placed by the shared code's 丁目 shift (town
  + number read as the chōme).
- Addresses: full-width digits on 607 rows, building names after the number
  on 158; neither blocks the join. **No shared-code rule is proposed for the
  join.**
- **Independent check**: the lists carry no coordinates and MHLW has no
  salons. Run GSI's address search on a sample at build
  (`screen_japan_join.py`'s `gsi_check`, 150 rows, 1 request per second).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

N03 code 27215 (**24.7 km²**, extent W 135.587, S 34.728, E 135.663, N
34.792; centroid 135.627, 34.765).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | Drawn |
|---|---|---|---|---|
| 京阪本線 (京阪電気鉄道, 12) | Keihan Main Line | **3 / 41** | 萱島, 寝屋川市, 香里園 | yes |
| 片町線 (西日本旅客鉄道, 11) | JR Gakkentoshi Line (片町線) | **1 / 24** | 寝屋川公園 | cut (a one-station stub, no other line) |

- **4 station records, 4 N02_005g groups**, each one record; no name in two
  groups. **Nearest-station gaps 2.0 to 3.1 km** (萱島–寝屋川市 2,024 m,
  寝屋川市–香里園 2,467 m, 寝屋川公園–寝屋川市 3,129 m): a sparse page.
- **Close to the line**: 萱島 67 m and 香里園 127 m inside it. Just outside,
  not ringed: 星田 (JR, Katano, 127 m), 忍ヶ丘 (JR, Shijōnawate, 396 m),
  四条畷 (JR, 510 m), 大和田 (Keihan, Kadoma, 670 m).
- **Cut at the line**: Keihan 38 beyond (Kyoto Prefecture 17, Ōsaka City 8,
  Hirakata 6, Kadoma 4, Moriguchi 3); the Gakkentoshi Line 23 (Kyoto
  Prefecture 9, Daitō 3, Hirakata 3, Ōsaka City 3, Katano 2, Higashiōsaka 2,
  Shijōnawate 1). No Shinkansen.
- **The stub test** (`japan.stub_test`): Keihan keeps 7% of its line (3 of
  41), the Gakkentoshi Line 4% (1 of 24). Neither is an urban line (subway,
  monorail, AGT): Keihan is drawn, 寝屋川公園 stays as cut (the row's call).
- **The light-rail/rail test**: Keihan heavy rail (class 12), JR class 11.
  No tram or light rail.
- **Frequency** (weekday departures, counts only, never a timetable on the
  page):

  | Station (line, direction) | All day | 10:00-16:00 | Source |
  |---|---|---|---|
  | 寝屋川公園 (JR Gakkentoshi, toward 京橋) | **84** | **24 (4.0 an hour, every 15 min)** | JR West's `timetable.jr-odekake.net/station-timetable/2898067001?date=20261007`, READ |
  | 寝屋川公園 (JR Gakkentoshi, toward 木津) | **86** | **24 (4.0 an hour)** | `…/2898067002?date=20261007`, READ |
  | 萱島, 寝屋川市, 香里園 (Keihan, toward 出町柳) | at least 94, 104, 113 | at least 28, 29, 34 (about 5 an hour) | Keihan's weekday line timetable `time01-1.pdf` (2026-08-24 edition), the wave-5 probe's layout-text parse; ⚠️ a floor, not a count (the layout splits rows): re-count at build |

  **No stretch is at or under about 11 trains a day** (call 86).
- ⚠️ **Gate 3** at build: Keihan's station count inside the city (3) and
  寝屋川公園. **OSM `name:en`** for 4 groups (one Overpass query at build).

## Scope

**Neyagawa City (27215).** Keihan runs on to Hirakata and Kyoto Prefecture
north and to Kadoma, Moriguchi and Ōsaka City south; the Gakkentoshi Line to
Katano and Kyoto Prefecture east and to Shijōnawate, Daitō and Ōsaka City
south: cut at the line.

## Licences — as stated; the read is pending

**As stated on BODIK**: all three packages carry `license_id` `cc-by-40-intl`
("Creative Commons Attribution 4.0 International", licence URL
`https://creativecommons.org/licenses/by/4.0/deed.ja`), organization 寝屋川市;
**the city's own catalogue CSV** states **CC-BY4.0** for each. No city terms
page was found at Step 0 (the オープンデータ一覧 page carries the catalogue,
no terms text). **A licence-read agent reads the terms separately; staging
records its verdict and the credit wording.** No verdict is written in this
brief.

- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census:
  measurement sources. **Operators' timetables**: counts only.
- The notice number is claimed at build, not here.

## Privacy

- **The operator columns, read IN MEMORY only, never written**:
  **営業者名称（法人の場合は代表者氏名）** (a sole trader's own name, or a
  company's representative: a person on every row, filled on 155, 419 and
  62 rows), **法人営業者名称** (a company's name, filled on 7, 69 and 34
  rows; 109 of 110 carry a company marker), **営業者所在地（法人のみ）** and
  **施設電話番号** (never selected).
- **The name rule, measured in memory with these two columns**: **0** bare
  personal names; trade name equal to the operator's own name: **0**
  barbers, **0** beauty, **1** laundry.
- ⚠️ **Neither operator column is in `OPERATOR_COLS`**, so the shared rule
  compares nothing here today (0 by construction, the 1 laundry row missed).
  Shared code at build: `OPERATOR_COLS` gains
  `営業者名称（法人の場合は代表者氏名）` and `法人営業者名称`, each list's own
  spelling, followed by the Minato control (`screen_japan_join.py minato`,
  98.0 / 0.2 / 1.8) and every built Japanese city's drift check; or the city
  maps them in `source_rows`.
- Run `check_personal_exposure.py neyagawa` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Osaka Prefecture after the retag),
`label_tier: "minor"`, `"country": "Japan"`. The city runs 135.587-135.663 E,
centroid 135.627: project to **UTM 53N (EPSG:32653)** (computed here, never
copied). OSM box from the N03 extent, rounded out: (34.72, 135.58, 34.80,
135.67).

**Scaffold**: `scaffold_city.py --slug neyagawa --name Neyagawa --system-name
"Keihan and JR West" --taxonomy japan_eigyo --lat 34.765 --lon 135.627
--region "Japan West" --country Japan --mode metro --page-number <N>`
(`--dry-run` first), the number claimed in `docs/session_roles.md` at build.

## Owner calls

**Made (do not re-ask):** Band B, personal services only (call 114); the
downloads (calls 106, 147); the floor at Minoh's page (calls 115, 166),
which Neyagawa clears at 630 premises; 寝屋川公園 kept as cut; 4 station
groups; the standing Japanese calls; `mode: metro`; the minor tier; no
frequency floor (call 46).

**Open, with a recommendation:**

1. **No Food layer from MHLW.** 23 addressed restaurants against 783 census
   establishments (3%), a very thin set (call 127b leaves it open; the band
   row already says food off). *Recommend leaving food off*; the tradeoff is
   one bucket against two dozen unrepresentative pins.

## What the build must still measure

- `config.source_rows`: the three 20260831 files, kind by file, 営業種別
  mapped to the type, de-duplicated by (address, trade name) per bucket;
  `as_of` 2026-08-31. Expect 155, 418 and 64 rows, **630 pins** (the 7
  barber-and-beauty premises one pin each).
- The `OPERATOR_COLS` change (Privacy), with its controls; GSI's sample
  check; Keihan's frequencies by a whole-page reader; gate 3; OSM
  `name:en`; the label and legend entry on the 寝屋川公園 cut (measure
  placement in a scratch render); line colors on both basemaps; the opening
  view (`map-view`); `check_macro_labels.py` with Kadoma, Moriguchi and
  Hirakata; `check_provenance.py`; `check_scope_disclosure.py`.
- The page's businesses bullet (Yokohama's line) and What Is Excluded: no
  food list, storeless pick-ups not premises.

```brief-checks
[
  {
    "id": "neyagawa-bodik-lists",
    "claim": "Neyagawa's barber, beauty and laundry packages on BODIK carry the 2026-08-31 full lists under CC BY 4.0 (one BODIK call)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=name%3A%28272159_barber%20OR%20272159_hair_dressing%20OR%20272159_cleaning%29&rows=5",
    "present": ["272159_barber_20260831.csv", "272159_hair_dressing_20260831.csv", "272159_cleaning_20260831.csv", "cc-by-40-intl"]
  },
  {
    "id": "neyagawa-catalogue-cc-by",
    "claim": "The city's own open-data catalogue CSV (cp932, no charset: ASCII anchors) lists its datasets under CC-BY4.0",
    "kind": "http_contains",
    "url": "https://www.city.neyagawa.osaka.jp/material/files/group/79/272159_open_data_list.csv",
    "present": ["272159", "CC-BY4.0"]
  },
  {
    "id": "neyagawa-isj-block-live",
    "claim": "MLIT's block-level address file for Neyagawa (27215) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27215-24.0a.zip",
    "min_bytes": 80000
  },
  {
    "id": "neyagawa-isj-chome-live",
    "claim": "MLIT's town-chome file for Neyagawa (27215) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/27215-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "neyagawa-keihan-timetable",
    "claim": "Keihan's weekday Main Line timetable PDF (time01-1.pdf) answers - a frequency source",
    "kind": "http_ok",
    "url": "https://www.keihan.co.jp/traffic/time-fare/pdf/time01-1.pdf",
    "min_bytes": 500000,
    "content_type_contains": "pdf"
  },
  {
    "id": "neyagawa-jr-timetable",
    "claim": "JR West's station timetable for 寝屋川公園 (Gakkentoshi Line, toward 京橋) answers",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/station-timetable/2898067001",
    "present": ["寝屋川公園", "学研都市線"]
  },
  {
    "id": "neyagawa-projected-crs",
    "claim": "Neyagawa projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.627,
    "expect": "EPSG:32653"
  }
]
```
