# Minoh — build brief

**Band B, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 91: `docs/decisions_drafts/staging.md`, "Wave 5: the ranked queue and
the pre-verdicts screened": "Ibaraki and Minoh (barbers and beauty only,
thinner than any page published, measured against Hakodate's 1,077 and
Kōchi's 1,406 storefronts)"). Minoh is also the floor the owner set for
Moriguchi and Kadoma (call 115, "under Minoh's roughly 350 premises" is too
thin). The Step 0 downloads were approved by the owner 2026-10-06 (calls 106
and 147). **Step 0 measured 2026-10-06** (staging). Each file from its
publisher's own host with the project user-agent, each HTTP 200, under each
URL's own file name as `japan_fetch.get` saves:

- From `data.bodik.jp` (Ōsaka Prefecture's organisation `270008`), **saved
  once under `data/osaka_pref/raw/`** for every prefecture-licensed town (the
  data folder is one shared junction), 22 s between calls: the barber list
  `riyou-ichiran-0803.xlsx` (154,572 B) and the beauty list
  `biyou-ichiran-0803.xlsx` (435,585 B), both as of 2026-03-31, and their
  monthly new-premises files to 2026-08: `0804-riyou.xlsx`, `0805-riyou.xlsx`,
  `0806-riyou-.xlsx`, `0807-riyou-.xlsx`, `0808-riyou-.xlsx`,
  `0804-biyou.xlsx` .. `0808-biyou.xlsx` (11,484 to 14,445 B each). **717,206
  B for the twelve.**
- From `nlftp.mlit.go.jp`, into `data/minoh/raw/isj/`: `27220-24.0a.zip`
  (65,706 B) and `27220-19.0b.zip` (7,202 B).

Nothing else was downloaded. **MHLW has no file for the town's code** (27211,
tried for Ibaraki, answers HTTP 404): MHLW keys its files by the licensing
authority, and the prefecture's health centres license Minoh (`27000` in
`docs/coverage_sweep/japan_universe_mhlw.csv`); that file was not named in
the approval and was not fetched.

**Run `python scripts/brief_check.py minoh` before writing any code.** Then
the `japan-city` skill, **Kōchi's shape** (`docs/build_briefs/kochi.md`,
personal services only: a full list plus monthly additions) with Akita's
registers (one file per kind, no type column). **`docs/build_briefs/ibaraki_osaka.md`
reads the same two lists**: build the prefecture's reader once and share it.
Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only. Rail: MLIT
N02-25 cut at the N03 city line, through `pipeline/countries/japan.py` with
an in-memory `CITIES` entry.

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

**✅ Barbers and beauty salons only (owner, 2026-10-06, the band row):** no
laundry list and no food list exists for the prefecture-licensed towns
(below), so Personal services is barbers and beauty salons, the laundry gap
and the missing Food buckets disclosed on the page and in What Is Excluded
(Kōchi's and Akita's precedent for the laundry gap).

**✅ Thinner than any published page (owner, 2026-10-06, call 91):** the
owner banded Minoh B on an estimate of about 350 premises against Hakodate's
1,077 storefronts, the thinnest page published, and Kōchi's 1,406. **It
measures 294** (open call 1).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
`label_tier: "minor"`, the **Japan West** view today and **Osaka Prefecture**
after wave 4's retag. Its label offset comes from `check_macro_labels.py`
(PROBLEMS 0 at 375, 768 and 1200), never by eye; its dot sits about 8 km
north of Toyonaka's and beside Ikeda's.

**✅ `mode`: `metro`.** Kita-Osaka Kyuko is a subway-type line running
through onto the Osaka Metro Midōsuji Line; Hankyu's Minoh Line is a
conventional railway (N02 class 12). No JR. Toyonaka's precedent.

---

## The one-line summary

**One bucket from Ōsaka Prefecture's own lists on BODIK (CC BY 4.0 as stated;
the licence read is pending, staging records it): 52 barbers and 245 beauty
salons in Minoh (the full lists as of 2026-03-31 plus 5 beauty openings to
2026-08-31), 294 premises, the thinnest page yet.** The prefecture-wide lists
hold **96.2% and 99.9%** of e-Stat's in-force counts for the prefecture's own
area. **Block join 100.0%.** No laundry list, no food list (MHLW's prefecture
file holds 31 addressed restaurants in the city against 361 in the census).
**Rail: 5 station groups** (Hankyu Minoh Line 3, Kita-Osaka Kyuko 2), read
from the operators' own timetables: **6 and 7.5 an hour 10:00-16:00, more
than 100 a day each.**

---

## Business leg — Ōsaka Prefecture's 生活衛生 lists on BODIK

Two CKAN packages of organisation `270008` (大阪府), each `license_id`
`cc-by-40-intl`, licence URL `creativecommons.org/licenses/by/4.0/deed.ja`,
last modified 2026-09-11:

| Package | Title | Resources |
|---|---|---|
| `270008_riyou-ichiran` | 理容所届出施設一覧 (frequency 1カ月) | 全施設一覧（R8.03） + 新規施設一覧 R8.04 .. R08.08 |
| `270008_biyou-ichiran` | 美容所届出施設一覧 | the same six |

The full lists cover the **32 municipalities the prefecture licenses**
(Ōsaka, Sakai and the seven core cities license their own); every address
starts with the municipality, never 大阪府.

### The full lists (as of 2026-03-31)

| File | Bytes | Prefecture rows | Minoh rows |
|---|---|---|---|
| `riyou-ichiran-0803.xlsx` | 154,572 | **1,576** | **52** |
| `biyou-ichiran-0803.xlsx` | 435,585 | **4,774** | **240** |

- **Layout**: title rows (理容所届出施設一覧, 令和８年３月31日現在, a
  municipality index), the header on row 18: three unnamed columns (a
  health-centre label, a municipality section label), then **理容所名称 /
  美容所名称**, **所在地**, **開設者**, 電話番号, **確認年月日** (an Excel serial).
  `japan_register.city_rows` finds the header by 所在地 and reads every row;
  all three named columns are in the shared tuples: **no shared-code
  change**. One file per kind, no type column: the config names the kind per
  file.
- **The section label agrees with the address** on every Minoh row (52 and
  240 in the 箕面市 section). Filter by the address prefix 箕面市.
- **確認年月日**: barbers 1963-10-14 .. 2026-02-16 (25 of 52 before 2000);
  beauty 1963-03-25 .. 2026-03-10 (38 before 2000, 86 since 2021).

### The monthly files (new premises only)

Prefecture-wide **10 barbers and 102 beauty salons** opened 2026-04 to
2026-08. **Minoh: 0 barbers, 5 beauty salons** (1, 1, 2, 1, 0 by month), none
already in the full list.

- **No closure files.** Closures after 2026-03-31 are invisible, so the
  register is an upper bound. Pin `as_of` to **2026-08-31**, never the
  download date (Kyoto's and Kōchi's call).

### Coverage against the official counts

- **e-Stat 衛生行政報告例 FY2024, 第10表** publishes the prefecture, Ōsaka,
  Sakai and the seven core cities, never a prefecture-licensed town. **The
  prefecture's own area** (大阪府 less those nine): **barbers 1,639, beauty
  salons 4,779**; the full lists hold **1,576 (96.2%) and 4,774 (99.9%)**.
- **The 2021 Economic Census** (27220): **理容業 41, 美容業 118
  establishments**. The lists hold **1.27 and 2.08 per establishment**, the
  beauty ratio the highest of the four Ōsaka towns measured (Ibaraki 1.70,
  Moriguchi 1.59, Kadoma 1.66): openings since 2021 (86) and closures never
  notified. The page keeps "may include closed premises".

### Duplicates and closed premises

- **Repeats**: none by (address, trade name); 1 beauty address carries two
  salons. **3 premises are in both lists**: one pin per premises and bucket
  leaves **294 pins from 297 rows**.
- **Closures are not marked**. Not a premises: **0**.

### No laundry list, no food list (disclosed)

- **Laundry**: the wave-5 probe listed all **81** BODIK packages of
  organisation 270008 and the city's own **20** (organisation 272205) in one
  catalogue call: no クリーニング list. The census counts 40 洗濯業
  establishments; the page discloses the gap.
- **Food**: no food permit list in either catalogue. MHLW's prefecture file
  holds **31 addressed restaurants** in the city against **361** 飲食店
  establishments in the census: Food service and Retail stay off (open call
  2).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards**. Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27220-24.0a.zip` (65,706 B,
**2,933 block keys**), town-chōme `.../19.0b/27220-19.0b.zip` (7,202 B,
**170**). `japan.CITIES` entry at build: `"minoh": {"name": "箕面市", "pref":
"27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
"wards": ["27220"]}`.

| Tier, today's shared code | Block | Town-chōme | Unplaced |
|---|---|---|---|
| Barbers (52) | **100.0%** | 0.0% | 0.0% |
| Beauty salons (245) | **100.0%** | 0.0% | 0.0% |

**No shared-code change is needed.** Independent check at build: GSI's
address search on a sample (`screen_japan_join.py`'s `gsi_check`), since the
lists carry no coordinates.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

N03 code 27220 (**47.9 km²**, extent W 135.437, S 34.807, E 135.526, N
34.911; the north is forested hills).

| N02 line (operator, class) | Public name | Inside | Stations inside |
|---|---|---|---|
| 箕面線 (阪急電鉄, 12) | Hankyu Minoh Line | **3 / 4** | 桜井, 牧落, 箕面 (terminus) |
| 南北線 (北大阪急行電鉄; the 2024 extension filed as class 21) | Kita-Osaka Kyuko Namboku Line | **2 / 6** | 箕面船場阪大前, 箕面萱野 (terminus) |

- **5 station records, 5 groups**; no name in two groups; no two closer than
  600 m (nearest 883 m); **median nearest-station gap 1,095 m**: rings by
  the spacing rule.
- **Cut at the line**: the Minoh Line's 石橋阪大前 (Ikeda, 176 m beyond the
  line, its junction with the Takarazuka Line); Kita-Osaka Kyuko 4 beyond
  (Toyonaka 2, Suita 2), running through onto the Midōsuji Line.
- **Near the line but outside**: the Monorail's Saito Line terminus 彩都西
  (228 m, in Ibaraki) and 豊川 (55 m): not drawn here (city line only); they
  are on Ibaraki's page.
- **The stub test passes**: the Minoh Line keeps 3 of 4, Kita-Osaka Kyuko 2;
  neither is a one-station stub. No owner question.
- **The light-rail/rail test**: both heavy rail. No tram or light rail.
- **Frequency, READ** (weekday departures; counts only, never a timetable on
  the page), from the wave-5 probe's cached copies of the operators' pages,
  re-counted 2026-10-06:

  | Station (line, direction) | All day | 10:00-16:00 |
  |---|---|---|
  | 桜井, 牧落, 箕面 (Hankyu, to 石橋阪大前; `HK-57`..`HK-59_mi_1_w.html`) | 111 each | **6 an hour** (locals) |
  | 箕面船場阪大前 (Kita-Osaka Kyuko, both ways; `/train/traffic/minohsemba/`) | 165 / 164 | **7.5** |
  | 箕面萱野 (terminus, to なかもず) | 164 | **7.5** |

  **No stretch is at or under about 11 trains a day** (call 86).
- ⚠️ **Gate 3** at build: Hankyu's and Kita-Osaka Kyuko's station counts
  inside the city (3 and 2). **OSM `name:en`** for 5 groups (one Overpass
  query at build).

## Scope

**Minoh City (27220).** The Minoh Line runs on to 石橋阪大前 in Ikeda,
Kita-Osaka Kyuko to Toyonaka and Suita; cut at the line.

## Licences — as stated; the read is pending

**As stated on BODIK**: both packages carry `license_id` `cc-by-40-intl`
("Creative Commons Attribution 4.0 International", licence URL
`https://creativecommons.org/licenses/by/4.0/deed.ja`), organisation 大阪府.
**A licence-read agent reads the terms separately; staging records its
verdict and the credit wording.** No verdict is written in this brief.

- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census:
  measurement sources. **Operators' timetables**: counts only.
- The notice number is claimed at build, not here.

## Privacy

- **開設者** (the operator): a company marker on **61** of 297 rows, **none
  on 235**, 1 empty. Read IN MEMORY for the name rule only (`OPERATOR_COLS`
  holds 開設者), never written. **電話番号** is never selected.
- **The name rule, measured in memory**: **0** bare personal names, **0**
  trade names equal to the operator's own name.
- Run `check_personal_exposure.py minoh` (`japan=True`) after step 2: it must
  print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Osaka Prefecture after the retag),
`label_tier: "minor"`, `"country": "Japan"`. The city runs 135.437-135.526 E,
centroid 135.479: project to **UTM 53N (EPSG:32653)**. OSM box from the N03
extent, rounded out: (34.80, 135.43, 34.92, 135.53).

**Scaffold**: `scaffold_city.py --slug minoh --name Minoh --system-name
"Hankyu and Kita-Osaka Kyuko" --taxonomy japan_eigyo --lat 34.856 --lon
135.479 --region "Japan West" --country Japan --mode metro --page-number <N>`
(`--dry-run` first), the number claimed in `docs/session_roles.md` at build.

## Owner calls

**Made (do not re-ask):** Band B, barbers and beauty only, thinner than any
page published (call 91); the downloads (calls 106, 147); the standing
Japanese calls; `mode: metro`; the minor tier, Japan West now and Osaka
Prefecture after the retag; no frequency floor (call 46); the laundry gap
disclosed.

**Answered by the owner on 2026-10-06:** call 166, **Minoh stays in B and the floor reads as "Minoh's page"** (294 measured premises), so Moriguchi (375) and Kadoma (339) clear it. The recommendations below are kept as the record.

**Weighed, with a recommendation:**

1. **Minoh measures 294 premises, not about 350.** The band (call 91) and
   the floor for Moriguchi and Kadoma (call 115) both rested on the
   estimate. *Recommend keeping Minoh in B and the floor as "Minoh's page"*:
   the owner approved it knowing it would be the thinnest page, and the
   measured lists are complete against the prefecture's in-force count. The
   tradeoff: a page of under 300 pins on 5 stations is a sparse map; dropping it would make Settsu's test
   (135) the only precedent, and Moriguchi (375) and Kadoma (339) would
   still clear a 294 floor.
2. **No Food layer from MHLW.** 31 addressed restaurants against 361 census
   establishments (9%), a very thin set (call 127b leaves it open).
   *Recommend leaving food off*; the tradeoff is one bucket against a few
   dozen unrepresentative pins.

## What the build must still measure

- `config.source_rows`: the full list plus the five monthly files per kind,
  filtered by the address prefix 箕面市, de-duplicated by (address, trade
  name), kind by file; `as_of` 2026-08-31. Expect 52 and 245 (shared with
  Ibaraki's reader).
- GSI's sample check; gate 3; OSM `name:en`; line colours on both basemaps;
  the opening view (`map-view`: the north is empty hills, so the fit must
  take the stations, not the N03 extent); `check_provenance.py`;
  `check_scope_disclosure.py`.
- The page's businesses bullet and What Is Excluded: barbers and beauty
  salons only, no laundry or food list, the register an upper bound.

```brief-checks
[
  {
    "id": "minoh-bodik-lists",
    "claim": "Osaka Prefecture's barber and beauty packages on BODIK carry the 2026-03-31 full lists and the 2026-08 monthly files under CC BY 4.0 (one BODIK call)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=name%3A%28270008_riyou-ichiran%20OR%20270008_biyou-ichiran%29&rows=5",
    "present": ["riyou-ichiran-0803.xlsx", "biyou-ichiran-0803.xlsx", "0808-riyou-.xlsx", "0808-biyou.xlsx", "cc-by-40-intl"]
  },
  {
    "id": "minoh-isj-block-live",
    "claim": "MLIT's block-level address file for Minoh (27220) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27220-24.0a.zip",
    "min_bytes": 50000
  },
  {
    "id": "minoh-isj-chome-live",
    "claim": "MLIT's town-chome file for Minoh (27220) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/27220-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "minoh-hankyu-timetable",
    "claim": "Hankyu's weekday timetable page for 箕面 (HK-59, Minoh Line) answers with departure links - a frequency source",
    "kind": "http_contains",
    "url": "https://www.hankyu.co.jp/station/html/HK-59_mi_1_w.html?no_redirect",
    "present": ["HK-59", "TM="]
  },
  {
    "id": "minoh-kitakyu-timetable",
    "claim": "Kita-Osaka Kyuko's station page for 箕面船場阪大前 carries its weekday timetable table (ASCII marker: the page sends no charset)",
    "kind": "http_contains",
    "url": "https://www.kita-kyu.co.jp/train/traffic/minohsemba/",
    "present": ["table_weekdays"]
  },
  {
    "id": "minoh-projected-crs",
    "claim": "Minoh projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.479,
    "expect": "EPSG:32653"
  }
]
```
