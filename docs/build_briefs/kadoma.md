# Kadoma — build brief

**Band B, owner-approved 2026-10-06** (Japan wave 4, staging's wave 5, call
115: `docs/decisions_drafts/staging.md`, "Wave 5, second half": "Moriguchi
and Kadoma (counted first: under Minoh's roughly 350 premises they come back
as too thin)"; rail, call 116). **Counted first: 339 premises.** That is under
the floor's stated figure (about 350) and **above Minoh's measured 294**, the
page the floor names: written on that reading, **open call 1**. The Step 0
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
- From `nlftp.mlit.go.jp`, into `data/kadoma/raw/isj/`: `27223-24.0a.zip`
  (55,932 B) and `27223-19.0b.zip` (5,993 B).

Nothing else was downloaded. **MHLW has no file for a prefecture-licensed
town's code** (27211 answers HTTP 404): its files follow the licensing
authority, here the prefecture (`27000` in
`docs/coverage_sweep/japan_universe_mhlw.csv`), not named in the approval
and not fetched.

**Run `python scripts/brief_check.py kadoma` before writing any code.** Then
the `japan-city` skill, **Kōchi's shape** (`docs/build_briefs/kochi.md`,
personal services only: a full list plus monthly additions) with Akita's
registers (one file per kind, no type column). **Ibaraki's, Minoh's and
Moriguchi's briefs read the same two lists**: build the prefecture's reader
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

**✅ Barbers and beauty salons only (owner, 2026-10-06, the band row):** no
laundry list and no food list exists for the prefecture-licensed towns, so
Personal services is barbers and beauty salons, the laundry gap and the
missing Food buckets disclosed on the page and in What Is Excluded (Kōchi's
and Akita's precedent). **Thinner than any published page**: 339 premises
against Hakodate's 1,077 storefronts and Kōchi's 1,406.

**⚠️ The one-station lines (owner, 2026-10-06, call 116, as the band row
words it: "the Osaka Monorail's two stations (門真市, 門真南) drawn cut"):**
**N02-25 does not file 門真南 under the Monorail.** 門真南 is the terminus of
the **Osaka Metro Nagahori Tsurumi-ryokuchi Line** (N02 7号線, class 21); the
Monorail's one station in the city is **門真市**, its terminus, grouped with
Keihan's 門真市 (94 m). Open call 2 asks which reading the call meant.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
`label_tier: "minor"`, the **Japan West** view today and **Osaka Prefecture**
after wave 4's retag. Its dot sits about 2.5 km east-southeast of
Moriguchi's: expect `KNOWN_STACKED` with Moriguchi. The offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`.** Keihan (N02 class 12), the Osaka Monorail and an
Osaka Metro subway terminus; no JR.

---

## The one-line summary

**One bucket from Ōsaka Prefecture's own lists on BODIK (CC BY 4.0 as stated;
the licence read is pending, staging records it): 93 barbers and 247 beauty
salons in Kadoma (the full lists as of 2026-03-31 plus 3 beauty openings to
2026-08-31), 339 premises.** The prefecture-wide lists hold **96.2% and
99.9%** of e-Stat's in-force counts for the prefecture's own area. **Block
join 95.9%, 2.9% unplaced** (old 大字 + 地番 addresses MLIT does not carry).
No laundry list, no food list (MHLW's prefecture file holds 23 addressed
restaurants against 621 in the census). **Rail: 5 station groups**, not the
row's 6 (Keihan 4; the Monorail's 門真市 shares Keihan's group; 門真南 is the
Nagahori Tsurumi-ryokuchi Line's), read from the operators' own timetables:
**about 6 to 9 an hour 10:00-16:00, more than 100 a day each.**

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

| File | Bytes | Prefecture rows | Kadoma rows |
|---|---|---|---|
| `riyou-ichiran-0803.xlsx` | 154,572 | **1,576** | **93** |
| `biyou-ichiran-0803.xlsx` | 435,585 | **4,774** | **244** |

- **Layout**: title rows, a municipality index, the header on row 18: three
  unnamed columns (a health-centre label, a municipality section label),
  then **理容所名称 / 美容所名称**, **所在地**, **開設者**, 電話番号,
  **確認年月日** (an Excel serial). `japan_register.city_rows` finds the header
  by 所在地; all three named columns are in the shared tuples: **no
  shared-code change**. One file per kind: the config names the kind per
  file.
- **The section label agrees with the address** on every Kadoma row (93 and
  244 in the 門真市 section). Filter by the address prefix 門真市.
- **確認年月日**: barbers 1953-06-29 .. **2020-09-30** (56 of 93 before 2000,
  **none since 2021**); beauty 1958-04-09 .. 2026-03-24 (56 before 2000, 74
  since 2021).

### The monthly files (new premises only)

Prefecture-wide **10 barbers and 102 beauty salons** opened 2026-04 to
2026-08. **Kadoma: 0 barbers, 3 beauty salons** (2 in April, 1 in August),
none already in the full list.

- **No closure files.** Closures after 2026-03-31 are invisible, so the
  register is an upper bound. Pin `as_of` to **2026-08-31**, never the
  download date.

### Coverage against the official counts

- **e-Stat 衛生行政報告例 FY2024, 第10表** publishes the prefecture, Ōsaka,
  Sakai and the seven core cities, never a prefecture-licensed town. **The
  prefecture's own area** (大阪府 less those nine): **barbers 1,639, beauty
  salons 4,779**; the full lists hold **1,576 (96.2%) and 4,774 (99.9%)**.
- **The 2021 Economic Census** (27223): **理容業 88, 美容業 149
  establishments**; the lists hold **1.06 and 1.66 per establishment**. The
  page keeps "may include closed premises".

### Duplicates and closed premises

- **Repeats**: 1 beauty (address, trade name) twice; 7 beauty addresses carry
  two salons. **No premises is in both lists** by (address, name); 1 address
  holds a barber and a beauty salon under different names. One pin per
  premises and bucket leaves **339 pins from 340 rows**.
- **Closures are not marked**. Not a premises: **0**.

### No laundry list, no food list (disclosed)

- **Laundry**: the wave-5 probes listed all **81** BODIK packages of
  organisation 270008 and the city's own **17** (organisation 272230): no
  クリーニング list. The census counts 32 洗濯業 establishments; the page
  discloses the gap.
- **Food**: no food permit list. MHLW's prefecture file holds **23 addressed
  restaurants** in the city against **621** 飲食店 establishments in the
  census: Food service and Retail stay off (open call 3).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards**. Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27223-24.0a.zip` (55,932 B,
**2,232 block keys**), town-chōme `.../19.0b/27223-19.0b.zip` (5,993 B,
**86**). `japan.CITIES` entry at build: `"kadoma": {"name": "門真市", "pref":
"27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
"wards": ["27223"]}`.

| Tier, today's shared code | Block | Town-chōme | Unplaced |
|---|---|---|---|
| Barbers (93) | **97.8%** | 1.1% | 1.1% |
| Beauty salons (247) | **95.1%** | 1.2% | 3.6% |
| Both (340) | **95.9%** | 1.2% | **2.9%** |

**The misses, read** (towns and address shapes only, by `miss.py` in the
scratchpad):
- **Unplaced, 10 rows, all written 大字 + 地番**: 大字三ツ島 (5), 大字上島頭 (4),
  大字上馬伏 (1). MLIT's block file has no 地番 under these 大字, and its
  town-chōme file names only 三ツ島一丁目 to 六丁目 (the 住居表示 area) and
  nothing for 上島頭 or 上馬伏: the 地番 areas are outside 位置参照情報's block
  coverage, or the register keeps the address from before 住居表示.
- **Chōme tier, 4 rows**: 大字下馬伏 (2) and 大字巣本 (2) + 地番, where MLIT
  has the 町 (下馬伏町, 巣本町) but not the number; they take the town's
  centroid.
- A fix is shared code or a per-row geocode (GSI's address search on the 10
  rows, `screen_japan_join.py`'s `gsi_check`), each followed by the Minato
  control (`screen_japan_join.py minato` 98.0 / 0.2 / 1.8). *The brief
  proposes no rule*: 10 rows, disclosed as unplaced, is Akita's and Kōchi's
  practice.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

N03 code 27223 (**12.3 km²**, extent W 135.571, S 34.711, E 135.624, N
34.750).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | Drawn |
|---|---|---|---|---|
| 京阪本線 (京阪電気鉄道, 12) | Keihan Main Line | **4 / 41** | 西三荘, 門真市, 古川橋, 大和田 | yes |
| 大阪モノレール線 (大阪モノレール, 23) | Osaka Monorail Main Line | **1 / 14** | 門真市 (terminus) | cut, per call 116 (open call 2) |
| 7号線(長堀鶴見緑地線) (大阪市高速電気軌道, 21) | Osaka Metro Nagahori Tsurumi-ryokuchi Line | **1 / 17** | 門真南 (terminus) | cut (open call 2) |

- **6 station records, 5 N02_005g groups**: 門真市 is one group (Keihan and
  the Monorail, 94 m). The band row's "6" counts 門真市 twice. No name in two
  groups; no two groups closer than 600 m (nearest 635 m); **median
  nearest-station gap 824 m**.
- **Cut at the line**: Keihan 37 beyond (Kyoto Prefecture 17, Ōsaka City 8,
  Hirakata 6, Moriguchi 3, Neyagawa 3); the Monorail 13 (Settsu, Ibaraki,
  Suita, Toyonaka, Moriguchi's 大日, Itami); the Nagahori Tsurumi-ryokuchi
  Line 16 (Ōsaka City). Just outside: 萱島 (Keihan, 67 m, Neyagawa), 大日
  (Moriguchi, 228 m).
- **The stub test**: the Monorail and the Nagahori Tsurumi-ryokuchi Line are
  each cut to one station, each its terminus. Under the rule of calls 54 and
  92 alone, the Monorail would be **left out** (Keihan keeps 門真市's ring)
  and the Nagahori Tsurumi-ryokuchi Line **drawn cut** (no other line serves
  門真南). Call 116, as worded, draws both cut: open call 2.
- **The light-rail/rail test**: Keihan heavy rail, the Monorail a straddle
  monorail, the subway class 21. No tram or light rail.
- **Frequency, READ** (weekday departures; counts only, never a timetable on
  the page):

  | Station (line, direction) | All day | 10:00-16:00 | Source |
  |---|---|---|---|
  | 西三荘, 門真市, 古川橋, 大和田 (Keihan, toward 出町柳) | about 127 | **about 6 an hour** | Keihan's weekday line timetable `time01-1.pdf` (2026-08-24 edition), the wave-5 probe's layout-text parse; ⚠️ re-count at build |
  | 門真市 (Monorail, terminus, toward 大阪空港) | 112 | **6** | the operator's `/timetable/24` JSON |
  | 門真南 (Nagahori Tsurumi-ryokuchi, terminus, toward 大正) | 200 | **9** | Osaka Metro's kensaku timetable `station/29193/1025/2/`, read 2026-10-06 |

  **No stretch is at or under about 11 trains a day** (call 86).
- ⚠️ **Gate 3** at build: Keihan's station count inside the city (4) and the
  two termini. **OSM `name:en`** for 5 groups (one Overpass query at build).

## Scope

**Kadoma City (27223).** Keihan runs on to Moriguchi, Ōsaka City, Neyagawa
and beyond, the Monorail west and north to Moriguchi, Settsu and the
airport, the Nagahori Tsurumi-ryokuchi Line into Ōsaka City; cut at the line.

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

- **開設者** (the operator): a company marker on **48** of 340 rows, **none
  on 292**. Read IN MEMORY for the name rule only (`OPERATOR_COLS` holds
  開設者), never written. **電話番号** is never selected.
- **The name rule, measured in memory**: **0** bare personal names, **0**
  trade names equal to the operator's own name.
- Run `check_personal_exposure.py kadoma` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Osaka Prefecture after the retag),
`label_tier: "minor"`, `"country": "Japan"`. The city runs 135.571-135.624 E,
centroid 135.599: project to **UTM 53N (EPSG:32653)**. OSM box from the N03
extent, rounded out: (34.71, 135.57, 34.75, 135.63).

**Scaffold**: `scaffold_city.py --slug kadoma --name Kadoma --system-name
"Keihan, Osaka Monorail and Osaka Metro" --taxonomy japan_eigyo --lat 34.732
--lon 135.599 --region "Japan West" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), the number claimed in
`docs/session_roles.md` at build.

## Owner calls

**Made (do not re-ask):** Band B, barbers and beauty only, counted first
(call 115); the downloads (calls 106, 147); the standing Japanese calls;
`mode: metro`; the minor tier; no frequency floor (call 46); the laundry gap
disclosed.

**Answered by the owner on 2026-10-06:** call 166, the floor is Minoh's page (294), so Kadoma (339) is built; call 167, **the one-station rule applied as written**: the Nagahori Tsurumi-ryokuchi Line's one station (門真南) **drawn cut** (no other line keeps its ring), and the Osaka Monorail at 門真市 **left out** (Keihan keeps the ring), as Moriguchi's 大日. The recommendations below are kept as the record.

**Weighed, with a recommendation:**

1. **The floor.** Kadoma counts **339 premises** (93 barbers, 247 beauty
   salons): under the "roughly 350" the floor was stated in, above **Minoh's
   measured 294**, which is the page the floor names. *Recommend building
   it*: the floor is Minoh's page, and Kadoma is thicker than Minoh by 45
   premises on the same lists. The tradeoff: read literally at 350, Kadoma
   is too thin by 11 and goes the way of Settsu (135); then Minoh (294)
   would fail its own floor too.
2. **Which lines call 116 draws.** The row words it as "the Osaka
   Monorail's two stations (門真市, 門真南)", but 門真南 is the Nagahori
   Tsurumi-ryokuchi Line's terminus in N02-25 (the Monorail's southern
   extension, under construction, is not in the file). *Recommend drawing both
   one-station lines cut*: the Nagahori Tsurumi-ryokuchi Line at 門真南 by
   the rule of calls 54 and 92 (no other line keeps its ring), and the
   Monorail at 門真市 as call 116 says (Keihan keeps the ring, so the rule
   alone would leave it out; the owner's call is an explicit exception).
   The tradeoff: the rule alone gives one drawn cut stub, not two, and
   Moriguchi's 大日 (the same Monorail, call 116) is left out.
3. **No Food layer from MHLW.** 23 addressed restaurants against 621 census
   establishments (4%), a very thin set (call 127b leaves it open).
   *Recommend leaving food off*; the tradeoff is one bucket against a few
   dozen unrepresentative pins.

## What the build must still measure

- `config.source_rows`: the full list plus the five monthly files per kind,
  filtered by the address prefix 門真市, de-duplicated by (address, trade
  name), kind by file; `as_of` 2026-08-31. Expect 93 and 246 (one repeat
  dropped).
- The 10 unplaced 大字 rows (GSI's check, or disclosed as unplaced) and the 4
  chōme-tier rows; Keihan's frequencies by a whole-page reader; gate 3; OSM
  `name:en`; labels and legend entries on the one-station cuts (measure
  placement in a scratch render); line colours on both basemaps; the opening
  view (`map-view`); `check_macro_labels.py` with Moriguchi;
  `check_provenance.py`; `check_scope_disclosure.py`.
- The page's businesses bullet and What Is Excluded: barbers and beauty
  salons only, no laundry or food list, the register an upper bound.

```brief-checks
[
  {
    "id": "kadoma-bodik-lists",
    "claim": "Osaka Prefecture's barber and beauty packages on BODIK carry the 2026-03-31 full lists and the 2026-08 monthly files under CC BY 4.0 (one BODIK call)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=name%3A%28270008_riyou-ichiran%20OR%20270008_biyou-ichiran%29&rows=5",
    "present": ["riyou-ichiran-0803.xlsx", "biyou-ichiran-0803.xlsx", "0808-riyou-.xlsx", "0808-biyou.xlsx", "cc-by-40-intl"]
  },
  {
    "id": "kadoma-isj-block-live",
    "claim": "MLIT's block-level address file for Kadoma (27223) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27223-24.0a.zip",
    "min_bytes": 40000
  },
  {
    "id": "kadoma-isj-chome-live",
    "claim": "MLIT's town-chome file for Kadoma (27223) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/27223-19.0b.zip",
    "min_bytes": 4000
  },
  {
    "id": "kadoma-keihan-timetable",
    "claim": "Keihan's weekday Main Line timetable PDF (time01-1.pdf) answers - a frequency source",
    "kind": "http_ok",
    "url": "https://www.keihan.co.jp/traffic/time-fare/pdf/time01-1.pdf",
    "min_bytes": 500000,
    "content_type_contains": "pdf"
  },
  {
    "id": "kadoma-monorail-timetable",
    "claim": "The Osaka Monorail's timetable data for 門真市 (station 24, its terminus) answers with a weekday table",
    "kind": "http_contains",
    "url": "https://www.osaka-monorail.co.jp/timetable/24",
    "present": ["up_weekday"]
  },
  {
    "id": "kadoma-nagahori-timetable",
    "claim": "Osaka Metro's timetable for 門真南, the Nagahori Tsurumi-ryokuchi Line's terminus (not the Monorail's), answers",
    "kind": "http_contains",
    "url": "https://kensaku.osakametro.co.jp/timetable/ja/subway/dia/station/29193/1025/2/",
    "present": ["門真南", "長堀鶴見緑地線"]
  },
  {
    "id": "kadoma-projected-crs",
    "claim": "Kadoma projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.599,
    "expect": "EPSG:32653"
  }
]
```
