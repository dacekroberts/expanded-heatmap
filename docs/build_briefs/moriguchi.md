# Moriguchi — build brief

**Band B, owner-approved 2026-10-06** (Japan wave 4, staging's wave 5, call
115: `docs/decisions_drafts/staging.md`, "Wave 5, second half": "Moriguchi
and Kadoma (counted first: under Minoh's roughly 350 premises they come back
as too thin)"; rail, call 116). **Counted first: 375 premises, above the
floor** (Minoh's estimate of about 350, and Minoh's measured 294). The Step 0
downloads were approved by the owner 2026-10-06 (calls 106 and 147). **Step 0
measured 2026-10-06** (staging). Each file from its publisher's own host with
the project user-agent, each HTTP 200, under each URL's own file name as
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
- From `nlftp.mlit.go.jp`, into `data/moriguchi/raw/isj/`: `27209-24.0a.zip`
  (68,485 B) and `27209-19.0b.zip` (7,298 B).

Nothing else was downloaded. **MHLW has no file for a prefecture-licensed
town's code** (27211 answers HTTP 404): its files follow the licensing
authority, here the prefecture (`27000` in
`docs/coverage_sweep/japan_universe_mhlw.csv`), not named in the approval
and not fetched.

**Run `python scripts/brief_check.py moriguchi` before writing any code.**
Then the `japan-city` skill, **Kōchi's shape** (`docs/build_briefs/kochi.md`,
personal services only: a full list plus monthly additions) with Akita's
registers (one file per kind, no type column). **Ibaraki's, Minoh's and
Kadoma's briefs read the same two lists**: build the prefecture's reader
once. Coordinates: the `address-join` skill, measured with
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

**✅ The two one-station urban lines (owner, 2026-10-06, call 116):** **the
Imazatosuji Line's 太子橋今市 is drawn cut**, since no other line keeps its
ring inside the city (the Tanimachi Line's 太子橋今市 platform lies 30 m
outside, in Ōsaka City's Asahi ward); **the Osaka Monorail's 大日 is left
out**, its station kept through the Tanimachi Line.

**✅ Barbers and beauty salons only (owner, 2026-10-06, the band row):** no
laundry list and no food list exists for the prefecture-licensed towns, so
Personal services is barbers and beauty salons, the laundry gap and the
missing Food buckets disclosed on the page and in What Is Excluded (Kōchi's
and Akita's precedent). **Thinner than any published page**: 375 premises
against Hakodate's 1,077 storefronts and Kōchi's 1,406.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
`label_tier: "minor"`, the **Japan West** view today and **Osaka Prefecture**
after wave 4's retag. Its dot sits about 10 km northeast of Osaka's, between
Ōsaka City, Kadoma and Neyagawa: expect `KNOWN_STACKED` with Kadoma (2.5 km
apart). The offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768
and 1200), never by eye.

**✅ `mode`: `metro`.** Two Osaka Metro subway lines (N02 class 21) and
Keihan (class 12); no JR.

---

## The one-line summary

**One bucket from Ōsaka Prefecture's own lists on BODIK (CC BY 4.0 as stated;
the licence read is pending, staging records it): 112 barbers and 264 beauty
salons in Moriguchi (the full lists as of 2026-03-31 plus 5 beauty openings to
2026-08-31), 375 premises.** The prefecture-wide lists hold **96.2% and
99.9%** of e-Stat's in-force counts for the prefecture's own area. **Block
join 99.7%**, nothing unplaced. No laundry list, no food list (MHLW's
prefecture file holds 27 addressed restaurants against 594 in the census).
**Rail: 6 station groups** on a 12.7 km² city (Keihan 3, Tanimachi 2, the
Imazatosuji Line's 太子橋今市 drawn cut; the Monorail's 大日 kept through the
Tanimachi Line), **median gap 361 m**; read from the operators' own
timetables: **5 to 10 an hour 10:00-16:00, more than 100 a day each.**

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

| File | Bytes | Prefecture rows | Moriguchi rows |
|---|---|---|---|
| `riyou-ichiran-0803.xlsx` | 154,572 | **1,576** | **112** |
| `biyou-ichiran-0803.xlsx` | 435,585 | **4,774** | **259** |

- **Layout**: title rows, a municipality index, the header on row 18: three
  unnamed columns (a health-centre label, a municipality section label),
  then **理容所名称 / 美容所名称**, **所在地**, **開設者**, 電話番号,
  **確認年月日** (an Excel serial). `japan_register.city_rows` finds the header
  by 所在地; all three named columns are in the shared tuples: **no
  shared-code change**. One file per kind: the config names the kind per
  file.
- **The section label agrees with the address** on every Moriguchi row (112
  and 259 in the 守口市 section). Filter by the address prefix 守口市.
- **確認年月日**: barbers **1930-11-09** .. 2024-12-09 (61 of 112 before 2000,
  10 since 2021); beauty 1955-04-02 .. 2026-02-26 (76 before 2000, 62 since
  2021). An old register: a premises stays until a closure is notified.

### The monthly files (new premises only)

Prefecture-wide **10 barbers and 102 beauty salons** opened 2026-04 to
2026-08. **Moriguchi: 0 barbers, 5 beauty salons** (2, 2, 0, 1, 0 by month),
none already in the full list.

- **No closure files.** Closures after 2026-03-31 are invisible, so the
  register is an upper bound. Pin `as_of` to **2026-08-31**, never the
  download date.

### Coverage against the official counts

- **e-Stat 衛生行政報告例 FY2024, 第10表** publishes the prefecture, Ōsaka,
  Sakai and the seven core cities, never a prefecture-licensed town. **The
  prefecture's own area** (大阪府 less those nine): **barbers 1,639, beauty
  salons 4,779**; the full lists hold **1,576 (96.2%) and 4,774 (99.9%)**.
- **The 2021 Economic Census** (27209): **理容業 101, 美容業 166
  establishments**; the lists hold **1.11 and 1.59 per establishment**. The
  page keeps "may include closed premises".

### Duplicates and closed premises

- **Repeats**: 1 beauty (address, trade name) twice; 2 beauty addresses carry
  two salons. **No premises is in both lists** by (address, name); 6 addresses
  hold a barber and a beauty salon under different names (two pins). One pin
  per premises and bucket leaves **375 pins from 376 rows**.
- **Closures are not marked**. Not a premises: **0**.

### No laundry list, no food list (disclosed)

- **Laundry**: the wave-5 probes listed all **81** BODIK packages of
  organisation 270008 and the city's own **10**: no クリーニング list. The
  census counts 52 洗濯業 establishments; the page discloses the gap.
- **Food**: no food permit list. MHLW's prefecture file holds **27 addressed
  restaurants** in the city against **594** 飲食店 establishments in the
  census: Food service and Retail stay off (open call 1).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards**. Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27209-24.0a.zip` (68,485 B,
**3,339 block keys**), town-chōme `.../19.0b/27209-19.0b.zip` (7,298 B,
**172**). `japan.CITIES` entry at build: `"moriguchi": {"name": "守口市",
"pref": "27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["27209"]}`.

| Tier, today's shared code | Block | Town-chōme | Unplaced |
|---|---|---|---|
| Barbers (112) | **100.0%** | 0.0% | 0.0% |
| Beauty salons (264) | **99.6%** | 0.4% | 0.0% |
| Both (376) | **99.7%** | 0.3% | **0.0%** |

The one chōme-tier row is at 大宮通4丁目, whose block MLIT lacks. **No
shared-code change is needed.** GSI's address search on a sample at build.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

N03 code 27209 (**12.7 km²**, extent W 135.553, S 34.709, E 135.607, N
34.768).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | Drawn |
|---|---|---|---|---|
| 京阪本線 (京阪電気鉄道, 12) | Keihan Main Line | **3 / 41** | 滝井, 土居, 守口市 | yes |
| 2号線(谷町線) (大阪市高速電気軌道, 21) | Osaka Metro Tanimachi Line | **2 / 26** | 守口, 大日 (terminus) | yes |
| 8号線(今里筋線) (大阪市高速電気軌道, 21) | Osaka Metro Imazatosuji Line | **1 / 11** | 太子橋今市 | **cut** (call 116) |
| 大阪モノレール線 (大阪モノレール, 23) | Osaka Monorail Main Line | **1 / 14** | 大日 | **left out** (call 116); 大日 kept through the Tanimachi Line |

- **7 station records, 6 N02_005g groups**: 大日 is one group (Tanimachi and
  Monorail, 84 m). No name in two groups.
- **Tight spacing**: **median nearest-station gap 361 m** (355 to 1,771);
  four pairs under 600 m: 太子橋今市-土居 355 m, 守口-守口市 361 m, 土居-滝井
  371 m, 太子橋今市-滝井 419 m. Rings by the spacing rule at build will be
  small (open call 2 on 守口 / 守口市).
- **Cut at the line**: Keihan 38 beyond (Kyoto Prefecture 17, Ōsaka City 8,
  Hirakata 6, Kadoma 4, Neyagawa 3); the Tanimachi Line 24 (Ōsaka City 23,
  Yao 1); the Imazatosuji Line 10 (Ōsaka City). Neighbouring stations just
  outside: 西三荘 (Keihan, 40 m, Kadoma), 千林 (Keihan, 88 m), the Tanimachi
  Line's 太子橋今市 (30 m), 清水 (Imazatosuji, 341 m).
- **The stub test**: the Imazatosuji Line and the Monorail are each cut to
  one station: decided (call 116, above). The Tanimachi Line keeps 2 (its
  terminus 大日 and 守口): not a stub.
- **The light-rail/rail test**: subway (class 21), Keihan heavy rail, the
  Monorail a straddle monorail. No tram or light rail.
- **Frequency, READ** (weekday departures; counts only, never a timetable on
  the page):

  | Station (line, direction) | All day | 10:00-16:00 | Source |
  |---|---|---|---|
  | 土居, 滝井 (Keihan, toward 出町柳) | about 101 | **about 5 an hour** | Keihan's weekday line timetable `time01-1.pdf` (2026-08-24 edition), the wave-5 probe's layout-text parse |
  | 守口市 (Keihan) | more (express and semi-express stops) | ⚠️ re-count at build | the same; the parse of its row is unreliable |
  | 大日 (Tanimachi, to 八尾南) | 175 | **10** | Osaka Metro's kensaku timetable (`station/26040/1020/1/`) |
  | 太子橋今市 (Imazatosuji, to 今里 / to 井高野) | 159 / 157 | **6.2** each way | kensaku `station/26012/1027/1/` and `/2/`, read 2026-10-06 |
  | 大日 (Monorail, left out) | 112 / 116 | 6 | the operator's `/timetable/23` JSON |

  **No stretch is at or under about 11 trains a day** (call 86).
- ⚠️ **Gate 3** at build: Keihan's and Osaka Metro's station counts inside
  the city. **OSM `name:en`** for 6 groups (one Overpass query at build).

## Scope

**Moriguchi City (27209).** Keihan runs on to Ōsaka City, Kadoma, Neyagawa
and beyond, the Tanimachi and Imazatosuji Lines into Ōsaka City; cut at the
line.

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

- **開設者** (the operator): a company marker on **61** of 376 rows, **none
  on 315**. Read IN MEMORY for the name rule only (`OPERATOR_COLS` holds
  開設者), never written. **電話番号** is never selected.
- **The name rule, measured in memory**: **1 beauty row** is a bare personal
  name under the sign rule (withheld, shown by kind); no other trade name
  equals its operator's own name.
- Run `check_personal_exposure.py moriguchi` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Osaka Prefecture after the retag),
`label_tier: "minor"`, `"country": "Japan"`. The city runs 135.553-135.607 E,
centroid 135.576: project to **UTM 53N (EPSG:32653)**. OSM box from the N03
extent, rounded out: (34.70, 135.55, 34.77, 135.61).

**Scaffold**: `scaffold_city.py --slug moriguchi --name Moriguchi
--system-name "Keihan and Osaka Metro" --taxonomy japan_eigyo --lat 34.742
--lon 135.576 --region "Japan West" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), the number claimed in
`docs/session_roles.md` at build.

## Owner calls

**Made (do not re-ask):** Band B, barbers and beauty only, counted first
(call 115: 375, above the floor); the Imazatosuji Line drawn cut at
太子橋今市 and the Monorail's 大日 left out (call 116); the downloads (calls
106, 147); the standing Japanese calls; `mode: metro`; the minor tier; no
frequency floor (call 46); the laundry gap disclosed.

**Open, with a recommendation:**

1. **No Food layer from MHLW.** 27 addressed restaurants against 594 census
   establishments (5%), a very thin set (call 127b leaves it open).
   *Recommend leaving food off*; the tradeoff is one bucket against a few
   dozen unrepresentative pins.
2. **守口 (Tanimachi) and 守口市 (Keihan), 361 m apart, as two stations.**
   N02 keeps them apart and they carry different names. *Recommend keeping
   them apart* (two rings, each named): the joins on precedent (Kawasaki's
   377 m, Toyonaka's 千里中央) were one name at one interchange. Tradeoff: two
   overlapping small rings near the city's centre.

## What the build must still measure

- `config.source_rows`: the full list plus the five monthly files per kind,
  filtered by the address prefix 守口市, de-duplicated by (address, trade
  name), kind by file; `as_of` 2026-08-31. Expect 112 and 263 (one repeat
  dropped).
- Keihan's 守口市 frequency (the PDF's row, by a whole-page reader); gate 3;
  OSM `name:en`; the Imazatosuji Line's label and legend entry on a
  one-station cut (the Akita Oga Line's stub question: measure placement in
  a scratch render); line colours on both basemaps; the opening view
  (`map-view`); `check_macro_labels.py` with Kadoma; `check_provenance.py`;
  `check_scope_disclosure.py`.
- The page's businesses bullet and What Is Excluded: barbers and beauty
  salons only, no laundry or food list, the register an upper bound.

```brief-checks
[
  {
    "id": "moriguchi-bodik-lists",
    "claim": "Osaka Prefecture's barber and beauty packages on BODIK carry the 2026-03-31 full lists and the 2026-08 monthly files under CC BY 4.0 (one BODIK call)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=name%3A%28270008_riyou-ichiran%20OR%20270008_biyou-ichiran%29&rows=5",
    "present": ["riyou-ichiran-0803.xlsx", "biyou-ichiran-0803.xlsx", "0808-riyou-.xlsx", "0808-biyou.xlsx", "cc-by-40-intl"]
  },
  {
    "id": "moriguchi-isj-block-live",
    "claim": "MLIT's block-level address file for Moriguchi (27209) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27209-24.0a.zip",
    "min_bytes": 50000
  },
  {
    "id": "moriguchi-isj-chome-live",
    "claim": "MLIT's town-chome file for Moriguchi (27209) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/27209-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "moriguchi-keihan-timetable",
    "claim": "Keihan's weekday Main Line timetable PDF (time01-1.pdf) answers - a frequency source",
    "kind": "http_ok",
    "url": "https://www.keihan.co.jp/traffic/time-fare/pdf/time01-1.pdf",
    "min_bytes": 500000,
    "content_type_contains": "pdf"
  },
  {
    "id": "moriguchi-imazatosuji-timetable",
    "claim": "Osaka Metro's timetable for 太子橋今市 on the Imazatosuji Line (toward 今里) answers - the drawn-cut station's frequency source",
    "kind": "http_contains",
    "url": "https://kensaku.osakametro.co.jp/timetable/ja/subway/dia/station/26012/1027/1/",
    "present": ["太子橋今市", "今里筋線"]
  },
  {
    "id": "moriguchi-projected-crs",
    "claim": "Moriguchi projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.576,
    "expect": "EPSG:32653"
  }
]
```
