# Ibaraki (Ōsaka) — build brief

**Band B, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 91: `docs/decisions_drafts/staging.md`, "Wave 5: the ranked queue and
the pre-verdicts screened": "Ibaraki and Minoh (barbers and beauty only,
thinner than any page published, measured against Hakodate's 1,077 and
Kōchi's 1,406 storefronts)"). The Step 0 downloads were approved by the owner
2026-10-06 (calls 106 and 147). **Step 0 measured 2026-10-06** (staging). The
slug is `ibaraki_osaka`: the name alone is the prefecture of Ibaraki, whose
Tsukuba row sits on the master list. Each file from its publisher's own host
with the project user-agent, each HTTP 200, under each URL's own file name as
`japan_fetch.get` saves:

- From `data.bodik.jp` (Ōsaka Prefecture's organisation `270008`), **saved
  once under `data/osaka_pref/raw/`** for every prefecture-licensed town (the
  data folder is one shared junction), 22 s between calls: the barber list
  `riyou-ichiran-0803.xlsx` (154,572 B) and the beauty list
  `biyou-ichiran-0803.xlsx` (435,585 B), both as of 2026-03-31, and their
  monthly new-premises files to 2026-08: `0804-riyou.xlsx`, `0805-riyou.xlsx`,
  `0806-riyou-.xlsx`, `0807-riyou-.xlsx`, `0808-riyou-.xlsx`,
  `0804-biyou.xlsx` .. `0808-biyou.xlsx` (11,484 to 14,445 B each). **717,206
  B for the twelve.**
- From `nlftp.mlit.go.jp`, into `data/ibaraki_osaka/raw/isj/`:
  `27211-24.0a.zip` (143,530 B) and `27211-19.0b.zip` (9,623 B).

Nothing else was downloaded. **MHLW has no file for 27211**:
`opendatadownload.jsp?param=27211_food_business_all.csv` answers HTTP 404
(nothing saved). MHLW keys its files by the licensing authority, and the
prefecture's health centres license these towns (`27000` in
`docs/coverage_sweep/japan_universe_mhlw.csv`); that file was not named in
the approval and was not fetched.

**Run `python scripts/brief_check.py ibaraki_osaka` before writing any code.**
Then the `japan-city` skill, **Kōchi's shape** (`docs/build_briefs/kochi.md`,
personal services only: a full list plus monthly additions) with Akita's
registers (one file per kind, no type column). Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` was not edited).
Rail: MLIT N02-25 cut at the N03 city line, through `pipeline/countries/japan.py`
with an in-memory `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; it passes through without a station); (2) **lines served only by
limited expresses DO count** (2026-09-28); (3) **the city line only**: only
stations inside the city get rings, JR and the private lines are cut at the
line, **a one-station stub stays as cut** (2026-09-27); an URBAN line cut to
ONE station is left out, its station kept through the other lines, and drawn
cut only where no other line serves that station (owner, 2026-10-06, calls 54
and 92); (4) **菓子製造業 and そうざい製造業 count, in Retail** (moot on a
personal-services page); (5) **the name rule**, version 2 (2026-10-06): a bare
personal name is withheld whatever the operator column holds; (6) **no page
says "currently operating"**. Also: no frequency floor for JR or private
lines in Japan (owner, 2026-10-06, call 46), any stretch at about 11 trains a
day or fewer named and drawn (call 86; none here); fault-based cost clauses
accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Barbers and beauty salons only (owner, 2026-10-06, the band row):** no
laundry list and no food list exists for the prefecture-licensed towns
(below), so Personal services is barbers and beauty salons, the laundry gap
and the missing Food buckets disclosed on the page and in What Is Excluded
(Kōchi's and Akita's precedent for the laundry gap).

**✅ Thinner than any published page (owner, 2026-10-06, call 91):** 621
premises against Hakodate's 1,077 storefronts, the thinnest page published,
and Kōchi's 1,406. The owner banded it B on that measurement.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
`label_tier: "minor"`, the **Japan West** view today and **Osaka Prefecture**
after wave 4's retag. Its label offset comes from `check_macro_labels.py`
(PROBLEMS 0 at 375, 768 and 1200), never by eye; its dot sits about 19 km
north-northeast of Osaka's, between Suita and Takatsuki.

**✅ `mode`: `metro`.** The Osaka Monorail (6 of the 10 station groups,
N02 class 23) is urban rapid transit, Hankyu a conventional railway (class
12), JR West 2 of 10 groups, not the city's largest network (the owner's JR
test, 2026-10-02, does not make it rail). Toyonaka's precedent.

---

## The one-line summary

**One bucket from Ōsaka Prefecture's own lists on BODIK (CC BY 4.0 as stated;
the licence read is pending, staging records it): 142 barbers and 484 beauty
salons in Ibaraki (the full lists as of 2026-03-31 plus 10 beauty openings to
2026-08-31), 621 premises.** The prefecture-wide lists hold **96.2% and
99.9%** of e-Stat's in-force counts for the prefecture's own area. **Block
join 99.8%**, nothing unplaced. No laundry list, no food list (MHLW's
prefecture file holds 33 addressed restaurants in the city against 830 in the
census). **Rail: 10 station groups** (Osaka Monorail 6 on two lines, Hankyu
Kyoto Line 3, JR Kyoto Line 2; 南茨木 is Hankyu's and the Monorail's), read
from the operators' own timetables: **never under 6 an hour 10:00-16:00,
nothing near 11 a day.**

---

## Business leg — Ōsaka Prefecture's 生活衛生 lists on BODIK

Two CKAN packages of organisation `270008` (大阪府), each `license_id`
`cc-by-40-intl`, licence URL `creativecommons.org/licenses/by/4.0/deed.ja`,
last modified 2026-09-11:

| Package | Title | Resources |
|---|---|---|
| `270008_riyou-ichiran` | 理容所届出施設一覧 (frequency 1カ月) | 全施設一覧（R8.03） + 新規施設一覧 R8.04 .. R08.08 |
| `270008_biyou-ichiran` | 美容所届出施設一覧 | the same six |

The packages' notes say only 「大阪府内の理容所届出施設一覧です。」 / 「…美容所…」.
The full lists cover the **32 municipalities the prefecture licenses**
(Ōsaka, Sakai and the seven core cities license their own); every address
starts with the municipality, never 大阪府.

### The full lists (as of 2026-03-31)

| File | Bytes | Prefecture rows | Ibaraki rows |
|---|---|---|---|
| `riyou-ichiran-0803.xlsx` (sheet 令和８年３月末施設一覧) | 154,572 | **1,576** | **142** |
| `biyou-ichiran-0803.xlsx` (sheet 令和８年３月末美容所一覧) | 435,585 | **4,774** | **474** |

- **Layout**: title rows (理容所届出施設一覧, 令和８年３月31日現在, a
  municipality index of hyperlinks), the header on row 18: three unnamed
  columns (a health-centre label on 9 rows, a municipality section label on
  34), then **理容所名称 / 美容所名称**, **所在地**, **開設者**, 電話番号,
  **確認年月日** (an Excel serial). `japan_register.city_rows` finds the header
  by 所在地 and reads every row; the unnamed columns collide under the key ""
  and are not needed. All three named columns are in the shared tuples
  (`ADDR_COLS`, `NAME_COLS`, `OPERATOR_COLS`): **no shared-code change**.
- **One file per kind, no type column**: the config names the kind per file
  (Akita's and Hamamatsu's registers).
- **The section label agrees with the address** on every Ibaraki row (142 and
  474 in the 茨木市 section; the only prefecture rows whose address does not
  parse to a municipality are 南河内郡's three towns, written with the 郡).
  Filter by the address prefix 茨木市, never by the section label.
- **確認年月日**: barbers 1952-01-08 .. 2025-12-08 (72 of 142 before 2000);
  beauty 1957-01-01 .. 2026-03-17 (106 before 2000, 133 since 2021).

### The monthly files (new premises only)

Each 新規施設一覧 has the same columns (the 2026-08 barber file names its phone
column 施設電話番号) under a title row: prefecture-wide **10 barbers and 102
beauty salons** opened 2026-04 to 2026-08. **Ibaraki: 0 barbers, 11 beauty
salons** (2, 2, 3, 2, 2 by month), one of them already in the full list under
the same (address, name), so **10 added**.

- **No closure files.** The packages publish openings only; closures after
  2026-03-31 are invisible, so the register is an upper bound. Pin `as_of` to
  **2026-08-31** (the last month read), never the download date (Kyoto's and
  Kōchi's call).

### Coverage against the official counts

- **e-Stat 衛生行政報告例 FY2024, 第10表** (施設数, 2025-03-31;
  `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv`) publishes the
  prefecture, Ōsaka, Sakai and the seven core cities, never a
  prefecture-licensed town. **The prefecture's own area** (大阪府 less those
  nine): **barbers 1,639, beauty salons 4,779**. The full lists, a year later,
  hold **1,576 (96.2%) and 4,774 (99.9%)**.
- **The 2021 Economic Census** (`data/japan/raw/estat_census_r3_b1_009_1a.xlsx`,
  27211): **理容業 116, 美容業 284 establishments**. The lists hold **1.22 and
  1.70 per establishment**: a notified premises stays on the list until a
  closure is notified, and the census misses one-chair salons at home. The
  page keeps "may include closed premises".

### Duplicates and closed premises

- **Repeats**: none by (address, trade name) within either kind; 4 beauty
  addresses carry two salons (a building with two tenants). **5 premises are
  in both lists** (same address and name): one pin per premises and bucket
  leaves **621 pins from 626 rows**.
- **Closures are not marked** (no status column, no closure list); the
  prefecture's in-force count (e-Stat) is matched, so the lists keep what the
  prefecture keeps. Not a premises: **0** (no 一円, no vehicle).

### No laundry list, no food list (disclosed)

- **Laundry**: the wave-5 probe listed all **81** BODIK packages of
  organisation 270008 (and the city's own **134**, organisation 272116) in one
  catalogue call: barber, beauty and hot-spring lists, no クリーニング list. The
  census counts 65 洗濯業 establishments in the city; the page discloses the
  gap.
- **Food**: no food permit list in either catalogue. MHLW's prefecture file
  holds **33 addressed restaurants** in the city against **830** 飲食店
  establishments in the census (`japan_universe_mhlw.csv`): Food service and
  Retail stay off (open call 1).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27211-24.0a.zip` (143,530 B,
**10,587 block keys** with the 小字 aliases), town-chōme
`.../19.0b/27211-19.0b.zip` (9,623 B, **305**). `japan.CITIES` entry at build:
`"ibaraki_osaka": {"name": "茨木市", "pref": "27", "epsg": 32653, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["27211"]}`.

| Tier, today's shared code | Block | Town-chōme | Unplaced |
|---|---|---|---|
| Barbers (142) | **100.0%** | 0.0% | 0.0% |
| Beauty salons (485 rows, the repeat included) | **99.8%** | 0.2% | 0.0% |
| Both (627) | **99.8%** | 0.2% | **0.0%** |

The one chōme-tier row is at 西中条町, whose block MLIT lacks. **No shared-code
change is needed.** Independent check at build: GSI's address search on a
sample (`screen_japan_join.py`'s `gsi_check`, 1 request per second), since
the lists carry no coordinates.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_27_GML.zip`, N03 code 27211
(**76.4 km²**, extent W 135.496, S 34.775, E 135.606, N 34.929; the north is
the hill country of the 彩都 new town and beyond).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 大阪モノレール線 (大阪モノレール, 23) | Osaka Monorail Main Line | **3 / 14** | 宇野辺, 南茨木, 沢良宜 |
| 国際文化公園都市モノレール線(彩都線) (大阪モノレール, 23) | Osaka Monorail Saito Line | **3 / 5** | 阪大病院前, 豊川, 彩都西 |
| 京都線 (阪急電鉄, 12) | Hankyu Kyoto Line | **3 / 27** | 総持寺, 茨木市, 南茨木 |
| 東海道線 (西日本旅客鉄道, 11) | JR Kyoto Line | **2 / 59** | JR総持寺, 茨木 |

- **11 station records, 10 N02_005g groups**: 南茨木 is one group (Hankyu and
  the Monorail, 114 m). The master-list row's "11" counts 南茨木 twice. No
  name in two groups; no two groups closer than 600 m (nearest 668 m);
  **median nearest-station gap 1,048 m**: rings by the spacing rule.
- **Shinkansen**: the Tōkaidō Shinkansen crosses the city without a station;
  N02 has none inside. Not counted (standing call 1).
- **Near the line**: 阪大病院前 51 m, 豊川 55 m (the Saito Line runs along the
  Minoh boundary) and 宇野辺 68 m from the city line; their rings spill into
  Suita and Minoh, as every edge station's does.
- **Cut at the line** (named by N03 municipality at build): the Monorail Main
  Line 11 beyond (Toyonaka 4, Suita 2, Settsu 2, Moriguchi 1, Kadoma 1, Itami
  1), the Saito Line 2 (Suita: 万博記念公園, 公園東口), Hankyu 24 (Kyoto
  Prefecture 12, Ōsaka City 6, Takatsuki 3, Suita, Settsu, Shimamoto), JR 57.
- **The stub test passes**: no line is cut to one station (the Saito Line
  keeps 3 of 5, the Main Line 3 of 14). No owner question.
- **The light-rail/rail test**: the Monorail is a straddle monorail (class
  23), Hankyu and JR heavy rail. No tram or light rail.
- **Frequency, READ** (weekday departures; only counts are recorded, never a
  timetable on the page). Hankyu and JR West read by the wave-5 probe from
  the operators' pages (cached copies re-counted 2026-10-06); the Monorail
  from the operator's own `/timetable/<id>` JSON:

  | Station (line, direction) | All day | 10:00-16:00 |
  |---|---|---|
  | 茨木市 (Hankyu, to 大阪梅田; `HK-69_ky_1_w.html`) | 309 | **18 an hour** (特急 6, 準急 6, 普通 6) |
  | 南茨木 (Hankyu, to 大阪梅田) | 208 | **12** (準急 6, 普通 6) |
  | 総持寺 (Hankyu, to 大阪梅田) | 124 | **6** (locals) |
  | 茨木 (JR, toward Ōsaka; `station-timetable/2791011002`) | 224 | **12** |
  | JR総持寺 (JR, toward Ōsaka; `11129011002`) | 150 | **8** |
  | 宇野辺, 南茨木, 沢良宜 (Monorail Main, ids 18-20) | 112 / 116 | **6** each way |
  | 阪大病院前, 豊川 (Saito, ids 52-53); 彩都西 (54, terminus) | 109 / 112 | **6** each way |

  **No stretch is at or under about 11 trains a day** (call 86); the
  thinnest is the Saito Line, every 10 minutes.
- ⚠️ **Gate 3** at build: the operators' station counts inside the city
  (Monorail 6, Hankyu 3, JR 2). **OSM `name:en`** for 10 groups (one
  Overpass query at build; not queried here).

## Scope

**Ibaraki City (27211).** The Monorail runs on to Suita, Settsu, Toyonaka and
Kadoma, the Saito Line to Suita, Hankyu to Takatsuki, Kyoto and Ōsaka, JR to
Takatsuki and Suita; cut at the line.

## Licences — as stated; the read is pending

**As stated on BODIK**: both packages carry `license_id` `cc-by-40-intl`
("Creative Commons Attribution 4.0 International", licence URL
`https://creativecommons.org/licenses/by/4.0/deed.ja`), organisation 大阪府.
**A licence-read agent reads the terms separately; staging records its
verdict and the credit wording.** No verdict is written in this brief; take
the credit from staging's record.

- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census: measurement
  sources, not drawn. **Operators' timetables**: read for counts only, never
  reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **開設者** (the operator) is on every row but one: a company marker on
  **138** of the 627 rows read (626 after the repeat), **none on 488** (where
  an individual's own name can sit), 1 empty. Step 2 reads it IN MEMORY for the name rule only
  (`OPERATOR_COLS` holds 開設者) and never writes it. **電話番号** is never
  selected; select the trade name and 所在地 only.
- **The name rule, measured in memory** (answers only, never a value): **2
  beauty rows** are bare personal names under the sign rule (withheld, shown
  by kind); no other trade name equals its operator's own name; barbers 0.
- Run `check_personal_exposure.py ibaraki_osaka` (`japan=True`) after step 2:
  it must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Osaka Prefecture after the retag),
`label_tier: "minor"`, `"country": "Japan"`. The city runs 135.496-135.606 E,
centroid 135.550: project to **UTM 53N (EPSG:32653)** (computed here, never
copied). OSM box from the N03 extent, rounded out: (34.77, 135.49, 34.93,
135.61).

**Scaffold**: `scaffold_city.py --slug ibaraki_osaka --name "Ibaraki"
--system-name "Osaka Monorail, Hankyu and JR West" --taxonomy japan_eigyo
--lat 34.856 --lon 135.550 --region "Japan West" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), the number claimed in
`docs/session_roles.md` at build. The page's display name is the owner's at
build ("Ibaraki" alone collides with the prefecture in a reader's mind;
"Ibaraki (Osaka)" is the master list's).

## Owner calls

**Made (do not re-ask):** Band B, barbers and beauty only, thinner than any
page published (call 91); the downloads (calls 106, 147); the standing
Japanese calls above; `mode: metro`; the minor tier, Japan West now and
Osaka Prefecture after the retag; no frequency floor (call 46); the laundry
gap disclosed.

**Open, with a recommendation:**

1. **No Food layer from MHLW.** MHLW's prefecture file holds 33 addressed
   restaurants in the city against 830 census establishments (4%), a very
   thin set (call 127b leaves a thin set open). *Recommend leaving food off*
   and saying so; the tradeoff is a page of one bucket against a few dozen
   unrepresentative pins, and fetching the prefecture's MHLW file (not
   approved) to measure its notifications first.
2. **The page's name** ("Ibaraki" or "Ibaraki (Osaka)"). *Recommend "Ibaraki
   (Osaka)"* on the master list's own row, since Ibaraki is also a
   prefecture; the tradeoff is a parenthesis on a single-city page.

## What the build must still measure

- `config.source_rows`: the full list plus the five monthly files per kind,
  filtered by the address prefix 茨木市, de-duplicated by (address, trade
  name), kind by file; `as_of` 2026-08-31. Expect 142 and 484.
- The one chōme-tier row (西中条町); GSI's sample check; gate 3; OSM
  `name:en`; line colours on both basemaps (two Monorail lines); the opening
  view (`map-view`); `check_provenance.py`; `check_scope_disclosure.py`.
- The page's businesses bullet and What Is Excluded: barbers and beauty
  salons only, no laundry or food list, the register an upper bound
  (openings to 2026-08-31, closures since 2026-03-31 not shown).

```brief-checks
[
  {
    "id": "ibaraki-osaka-bodik-lists",
    "claim": "Osaka Prefecture's barber and beauty packages on BODIK carry the 2026-03-31 full lists and the 2026-08 monthly files under CC BY 4.0 (one BODIK call)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=name%3A%28270008_riyou-ichiran%20OR%20270008_biyou-ichiran%29&rows=5",
    "present": ["riyou-ichiran-0803.xlsx", "biyou-ichiran-0803.xlsx", "0808-riyou-.xlsx", "0808-biyou.xlsx", "cc-by-40-intl"]
  },
  {
    "id": "ibaraki-osaka-isj-block-live",
    "claim": "MLIT's block-level address file for Ibaraki (27211) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27211-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "ibaraki-osaka-isj-chome-live",
    "claim": "MLIT's town-chome file for Ibaraki (27211) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/27211-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "ibaraki-osaka-hankyu-timetable",
    "claim": "Hankyu's weekday timetable page for 茨木市 (HK-69, toward 大阪梅田) answers with departure links - a frequency source",
    "kind": "http_contains",
    "url": "https://www.hankyu.co.jp/station/html/HK-69_ky_1_w.html?no_redirect",
    "present": ["HK-69", "TM="]
  },
  {
    "id": "ibaraki-osaka-monorail-timetable",
    "claim": "The Osaka Monorail's timetable data for 豊川 (station 53, Saito Line) answers with weekday tables - a frequency source",
    "kind": "http_contains",
    "url": "https://www.osaka-monorail.co.jp/timetable/53",
    "present": ["up_weekday", "down_weekday"]
  },
  {
    "id": "ibaraki-osaka-jr-timetable",
    "claim": "JR West's station timetable for 茨木 (2791011002) answers with departure items - a frequency source",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/station-timetable/2791011002",
    "present": ["minute-item"]
  },
  {
    "id": "ibaraki-osaka-projected-crs",
    "claim": "Ibaraki projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.55,
    "expect": "EPSG:32653"
  }
]
```
