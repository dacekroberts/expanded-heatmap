# Tottori — build brief

**Band B, food only, owner-approved 2026-10-06** (a Japanese pre-verdict
converted, call 137: `docs/decisions_drafts/staging.md`, "Wave 5, second
half"). The Step 0 downloads were approved by the owner 2026-10-06 (call 141).
**Step 0 measured 2026-10-06** (staging). Into `data/tottori/raw/`
(gitignored), each from its publisher's own host with the project user-agent,
each HTTP 200, under each URL's own file name as `japan_fetch.get` saves:

- From `i2fas.mhlw.go.jp`: `31201_food_business_all.csv` (**1,629,218 B**),
  the food source.
- From `nlftp.mlit.go.jp`: `isj/31201-24.0a.zip` (326,881 B) and
  `isj/31201-19.0b.zip` (13,607 B).

**1,969,706 B in all.** Nothing else was downloaded. JR West's station
timetables were read from the copies staging's probe saved (pages, not data
files); nothing was re-fetched for them.

**Run `python scripts/brief_check.py tottori` before writing any code.** Then
the `japan-city` skill, **Kurume's shape** (`docs/build_briefs/kurume.md`:
MHLW's open data alone, food only, Okayama's decided precedent), with
Aomori's layout for the counts and the rail. Coordinates: the `address-join`
skill, measured with `pipeline/countries/japan_register.py` from scratch
scripts only (`scripts/screen_japan_join.py` has no Tottori entry; its table
is shared code and was not edited). Rail: MLIT N02-25 cut at the N03 city
line, read through `pipeline/countries/japan.py` with a scratch `CITIES`
entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none in Tottori); (2) **lines served only by limited expresses
DO count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27); an URBAN line cut to ONE
station is left out (owner, 2026-10-06, calls 54 and 92; none here); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds, and MHLW's 法人名 is an operator column (2026-10-05); (6) **no page
says "currently operating"**. Also: no frequency floor for JR or private
lines in Japan (owner, 2026-10-06, call 46), any stretch at about 11 trains a
day or fewer drawn and named (call 86); fault-based cost clauses accepted for
all of Japan (2026-09-24); English station names from OSM `name:en`; every
Japanese city reads `WAVE2_RULES` (owner, 2026-10-04); **市内一円 rows are
not premises** (Kobe's trap 6, 2026-09-27). The precedents set 2026-10-06
apply without re-asking: MHLW's own point where the block join misses (call
127c); a stated food share where a list is incomplete (call 125); tiers
disclosed where the block share is low (call 145).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Tottori
carries `label_tier: "minor"` and goes in the **Japan West** view, as Okayama
and Fukuyama do (`app/cities.py`); wave 4's first city to land retags Japan
into the eight regions, Tottori into **Chūgoku**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**`mode`: `metro`** (the owner's rule of 2026-10-02, "unless there is
substantial JR, JR reads as metro"): JR West holds all 13 station groups; no
subway or tram. Aomori's and Fukuyama's precedent.

---

## The one-line summary

**Food only, from MHLW's 食品衛生申請等システム file for 31201 (PDL 1.0, as
recorded): 2,065 open restaurant permits, cover 1.04 against e-Stat's 1,990.
The cover is NOT inflated by closed premises** (no permit past its expiry is
listed, and MHLW shows a closure only in its own month, then drops the row).
**It is inflated by scope: the city's health centre also licenses the four
eastern towns** (岩美町, 八頭町, 若桜町, 智頭町: 185 open restaurant permits),
and **273 permits are area-wide stalls and vehicles** (addressed 鳥取県内,
市内一円 and the like). **Inside the city at a real address: 1,573 restaurant
permits, 79.0% of e-Stat's whole figure.** Old-law permits still in term are
absent (Kurashiki's trap: none granted before 2021-06). Block join **85.1%**
at fixed premises in the city, town-chōme 14.6%, unplaced 0.2% (all with
MHLW's own point). **Rail: 13 station groups** (JR San'in 8, Inbi 6, 鳥取
shared), the Inbi Line inside the city in **two pieces** either side of 八頭町;
its southern piece sees about **12 trains a day** (read from 鳥取's
destinations): named under call 86.

---

## Business leg — MHLW's open data, alone

| | MHLW open data (31201) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=31201_food_business_all.csv`: **1,629,218 B, 4,782 rows** (許可 2,845, 届出 1,932, 許可(廃業) 5). UTF-8 with BOM, CRLF, the national schema |
| As of / cadence | Permits to **2026-08-26**; closures dated 2026-08-18 .. 08-31. Monthly (MHLW); the universe CSV's `latest` 2026-08-26 |
| Columns (25) | 自治体コード, 行番号, 都道府県名, 市区町村名, **営業施設名称、屋号又は商号** (and its フリガナ), **営業の種類**, **業態** (209 filled), **営業施設所在地**, 営業施設方書, **緯度 / 経度**, 営業施設電話番号, **法人名**, 法人番号, 法人住所, **許可番号**, 初回許可年月日, **許可年月日**, 許可開始日, **許可満了日**, **廃業年月日**, **申請区分**, 許可条件, 備考 |
| Operator column | **法人名, filled on 4,404 rows, 2,154 of them with no company marker**: an individual operator's own name in most (below, Privacy) |

### Scope: the health centre's area, not the city

**市区町村名 reads 鳥取市 on every row, but the addresses do not.** By the
address: 鳥取市 3,488 rows, 岩美郡岩美町 205, 八頭郡八頭町 194, 八頭郡智頭町 168,
八頭郡若桜町 77, blank 650. The prefecture's portal says the same of the
city's own notification list (「鳥取市内だけでなく、鳥取県東部４町（岩美町・八頭町・若桜町・智頭町）の情報も含んでいます」,
`odp-pref-tottori.tori-info.co.jp/dataset/1858.html`): Tottori City's health
centre serves the four towns.

- ⚠️ **The build cuts the four towns by the ADDRESS, never by a bounding
  box**: 370 of the four towns' rows carry an MHLW point inside the city's
  N03 extent (八頭町 194 of 194, 岩美町 85, 若桜町 64, 智頭町 27), so
  `CITY_BBOX` lets them through, and `OWN_POINT_FALLBACK` would then place
  them (their towns never match the city's ISJ, so every one reaches the
  fallback). Every such address starts `鳥取県岩美郡` or `鳥取県八頭郡`. A
  shared-code rule (an address that names another 郡 or 町 is out of scope)
  or a city-local filter; point-in-polygon against N03 for any row placed by
  its own point.
- Blank-address rows (650, 34 of them open restaurants) cannot be split
  between the city and the towns; they are unplaceable either way.

### Counts against the official stock

e-Stat 衛生行政報告例 FY2024 (`japan_official.estat()`), 鳥取県鳥取市, 飲食店営業
in force 2025-03-31: **1,990** (old law 611, revised 1,379). The 2021
Economic Census counts **837** 飲食店 establishments in 31201 and 64 in the
four towns (岩美町 18, 若桜町 8, 智頭町 18, 八頭町 20). **Whether e-Stat's
鳥取市 row counts the four towns is not stated**; both readings are given.

| Open restaurant permits (許可, no 廃業, expiry on or after 2026-08-31) | Count | Share of 1,990 |
|---|---|---|
| All (the universe CSV's `open_rest`) | **2,065** | 103.8% (cover 1.04) |
| … in the city at a real address | **1,573** | **79.0%** |
| … in the four towns at a real address | 185 | 9.3% |
| … area-wide (no premises: 鳥取県内 191, 市内一円 42, 鳥取県内一円 17, 県内一円 16, 鳥取市内 7) | 273 | 13.7% |
| … no address | 34 | 1.7% |

- **The city's share, apportioned (ESTIMATED)**: if e-Stat's 1,990 covers the
  health centre's area, the census split (837 of 901 establishments) puts
  about 1,849 in the city, and 1,573 is **about 85%** of it. **79.0% is the
  lower bound**, right if e-Stat counts the city alone.
- **Closed premises do not inflate it.** No restaurant permit past its expiry
  is listed (0); the file's 5 廃業 rows are all dated 2026-08-18 to 08-31, so
  MHLW shows a closure in its month and then drops the row (Kurume's file
  showed 08-10 to 08-28, Yamagata's 08-05 to 08-31: the same habit). Of the
  1,466 restaurant permits granted by 2025-03-31, **1,464 are still listed,
  against e-Stat's 1,379 revised-law in force that day (106.2%)**; without
  the 186 area-wide permits among them, 1,278 (92.7%); in the city at a real
  address, 1,125. Read either way, the excess sits in the area-wide and
  four-town rows, not in closures the city never entered. Unreported closures
  stay invisible, as everywhere: the page keeps the standing "may include
  premises that have closed" bullet.
- **Old-law coverage (Kurashiki's trap): ABSENT.** No open restaurant permit
  was granted before 2021-06-01 (4 carry an earlier 初回許可年月日); the system
  starts in 2021-06 (2021 grants by month: Jun 14, Jul 16, Aug 67, Sep 8, Oct
  17, Nov 91, Dec 6) and an old-law permit enters it only when renewed (every
  later grant's 初回許可年月日 equals its 許可年月日). e-Stat counted 611 old-law
  restaurants in force on 2025-03-31; Yamagata's complete list kept 35% of its
  old-law stock in term to 2026-08-31, which would put **about 215** of
  Tottori's still in term and missing (ESTIMATED, not measured).
- **By grant year** (open restaurants): 2021 217 · 2022 376 · 2023 371 · 2024
  382 · 2025 405 · 2026 314. **Terms**: 6 years 1,577, 7 years 327, 5 years
  160, 8 years 1. Expiry 2026 to 2033.
- **Area-wide permits are stalls and vehicles**: 164 of the 273 carry a stall
  condition (「営業品目は加熱調理品に限る」 and its variants, 海浜仮設) or the
  5-year term; at the city's real addresses only 6 of 1,573 run 5 years and 8
  carry a stall condition. Kobe's trap 6 covers them (below, shared code).
- **Duplicates**: 2 repeated 許可番号 among open restaurants; at real
  addresses 22 (address, trade name) pairs repeat (15 with grants within 13
  months of each other, units or a second permit at one counter); one pin per
  premises (trap 7) takes them: 1,561 distinct in the city.
- **Through `japan_eigyo`** (live rows in the city at a real address, the
  area-wide rows out): **Food service 1,557** (all 飲食店営業), **Retail 934**
  (permits 403: 菓子製造業 205, そうざい製造業 81, 魚介類販売業 67, 食肉販売業 44,
  six 飲食店営業 rows moved by 業態; notifications 531: その他の食料・飲料販売業
  173, 乳類販売業 106, コンビニエンスストア 97, 野菜果物販売業 50, 百貨店、総合スーパー
  50 …). Out: no rule 342, vending machines 171, institutional catering 117,
  temporary or mobile 16, mail order 7.
- **Notifications** (届出 1,932; 1,018 in the city by address, 607 blank)
  are the partial, opt-in Food-shops layer of Kurume, Okayama and Fukuoka,
  disclosed as such.
- **Economic Census control** (`scripts/japan_census_control.py` at build):
  **1,550** distinct food-service premises in the city, all placed (1,548 by
  the join, 2 by MHLW's point), **1.85 per establishment** (837), inside the
  built cities' 1.56-1.92.

### Personal services: none published

No barber, beauty or laundry list from the city or the prefecture: the
prefecture portal's searches for 理容, 美容 and クリーニング return nothing
for Tottori City, and its only Tottori City food dataset (1858,
`312011_food_business_all.csv`, 48.1 KB) is the city's FY2025 notifications
(the master list's row; staging's probe). So the page is **food only**:
"**This map shows food businesses only.**"

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/31201-24.0a.zip` (326,881 B,
**55,450 block keys**, 407 towns), town-chōme `.../19.0b/31201-19.0b.zip`
(13,607 B, **534**). `japan.CITIES` entry at build: `"tottori": {"name":
"鳥取市", "pref": "31", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES,
"wardless": True, "wards": ["31201"]}`.

| Tier (live rows in a bucket, in the city, real address) | All (2,491) | Food service (1,557) | Retail (934) |
|---|---|---|---|
| Block | **85.1%** | 86.1% | 83.6% |
| Town-chōme / 大字 centroid | 14.6% | 13.8% | 16.0% |
| Unplaced | **0.2%** (6) | 0.1% | 0.4% |
| **Block or MHLW's own point** (`OWN_POINT_FALLBACK`, call 127c) | **100%** | | |

With the area-wide rows left in, 218 鳥取県内 and 9 鳥取市内 rows reach the
join as towns and fail (block 77.9%, unplaced 8.8% of 2,727): the
not-a-premises change below must land first.

**Independent check**: MHLW's own coordinates against the block point,
**median 39 m, 96.1% within 250 m** (2,121 rows; 6 over 1 km).

**The misses, read** (towns only):
- **Unplaced (6)**: 鳥取市古海 3 (the city's name repeated inside the
  address), 青谷町鳴滝, 立川町, 南安長, one each; all six carry MHLW's point.
- **Town-chōme tier (364)**: 末広温泉町 55 and 弥生町 25, the downtown bar
  district, whose 地番 runs (100-775 and 101-393 in the block file) have gaps
  the addresses fall in; and the 2004 mergers' 大字 with no block keys at all
  (用瀬町用瀬 15, 鹿野町岡木 10, 鹿野町鹿野 9, 鹿野町今市 6, 青谷町青谷 6, 福部町湯山 6
  …), placed at the 大字 centroid. **Tiers disclosed (call 145)**: about one
  storefront in seven sits at its town's centre, not its block.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_31_GML.zip`, N03 code 31201
(**764.8 km²**, 40 parts with the islets; extent W 133.946, S 35.272, E
134.441, N 35.573; the 2004 mergers brought in 国府, 福部, 河原, 用瀬, 佐治,
気高, 鹿野 and 青谷). Read with `stub_test()`'s method and an in-memory
`CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 山陰線 (西日本旅客鉄道, 11) | JR San'in Line | **8 / 161** | 福部, 鳥取, 湖山, 鳥取大学前, 末恒, 宝木, 浜村, 青谷 |
| 因美線 (西日本旅客鉄道, 11) | JR Inbi Line | **6 / 19** | 鳥取, 津ノ井 · 国英, 鷹狩, 用瀬, 因幡社 |

- **14 station records, 13 N02_005g groups** (鳥取 one group for both
  lines). No name in two groups; no pair closer than 600 m. **Median
  nearest-station gap 2,924 m** (1,237 to 7,954): standard rings by the
  spacing rule.
- **The Inbi Line is inside the city in two pieces**: 鳥取 and 津ノ井, then
  東郡家, 郡家 and 河原 in 八頭町, then 国英, 鷹狩, 用瀬 and 因幡社 back inside
  before 智頭 (智頭町). Cut at the line (standing call 3), it draws as two
  pieces with an 八頭町 gap of about 10 km (open call 1).
- **Shinkansen**: none. The Wakasa Railway (from 郡家) and the Chizu Express
  (from 智頭) have no station in the city.
- **Cut at the line** (named by N03 municipality at build): San'in to 岩美町
  (east) and 湯梨浜町 (west), Inbi to 八頭町 and 智頭町.
- **The light-rail/rail test**: both heavy rail (N02 class 11, JR
  conventional). No tram, light rail or subway.
- **The stub test passes.** No line is cut to one station and none is urban.
- **Frequency, read from JR West's own station timetables**
  (`timetable.jr-odekake.net/station-timetable/<id>?date=20261007`, a
  Wednesday; fetched by staging's probe 2026-10-06 and counted from those
  copies: every departure, by type and printed destination):

  | Station (line, direction) | Departures | Local | Limited express |
  |---|---|---|---|
  | 鳥取 (San'in, to 倉吉・米子) | **33** | 19 (米子 12, 倉吉 7) | 14 |
  | 鳥取 (San'in, to 浜坂・豊岡) | **19** | 18 | 1 |
  | 鳥取 (Inbi, to 郡家・津山) | **32** | 18 (智頭 10, 若桜 6, 上郡 2) | 14 (Super Hakuto, Super Inaba) |
  | 鳥取大学前 (San'in, to 倉吉・米子) | **29** | 20 | 9 |

  **The Inbi Line's southern piece (国英, 鷹狩, 用瀬, 因幡社) sees about 12
  trains a day out of 鳥取**: the 10 locals to 智頭 and the 2 to 上郡 (on to
  the Chizu Express); the 6 to 若桜 leave the Inbi Line at 郡家, and the 14
  limited expresses are ASSERTED not to stop there (their stopping pattern was
  not read). At the edge of "about 11", it is **drawn and named under call
  86**. 津ノ井 sees the 18 locals. Everything on the San'in Line runs 18 or
  more a day; its intermediate stations are ASSERTED to see the locals. Only
  these counts are recorded, never a timetable on the page.
- ⚠️ **Gate 3** at build: JR West's per-line station counts. **OSM
  `name:en`** for 13 groups (one Overpass query at build; not queried here).

## Scope

**Tottori City** (including its 2004 mergers). The San'in Line runs on to
岩美 and 倉吉, the Inbi Line through 八頭町 to 智頭; cut at the line. **The
food file's four eastern towns are out** (above): the page is the city's.

## Licences — MHLW, as recorded

- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as recorded in
  `docs/data_sources/japan.md` and Kurume's brief. **MUST DISPLAY**:
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; link the top page only. **MUST NOT**: present it as
  MHLW's own; MHLW's logo; claim completeness or accuracy. 免責 2)ウ the
  minor open point, fine while the site is non-commercial.
- The prefecture portal's FY2025 notification list is not used.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **法人名 carries individuals here**: 4,404 rows filled, 2,154 with no
  company marker (1,159 of the 2,051 open restaurants' entries), 法人番号 on
  2,321; 法人住所 on 147; phones on 3,212. Step 2 never writes any of them;
  法人名 is read IN MEMORY for the name rule only (already in
  `OPERATOR_COLS`).
- **The name rule, version 2, measured in memory** (answers only, never a
  value): **181 rows** whose trade name is the individual operator's own name
  (169 notifications, mostly 農産保存食料品製造・加工業 91 and その他の食料品製造・加工業
  53; by bucket: 165 out of every bucket, **15 Retail, 1 Food service**), of
  which **5 bare personal names**. Withheld as the rule says.
- Select 営業施設名称、屋号又は商号, 営業の種類, 業態, 営業施設所在地, 緯度 / 経度,
  許可番号, the dates, 廃業年月日 and 申請区分 only.
- Run `check_personal_exposure.py tottori` (`japan=True`) after step 2; it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Chūgoku after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city's centroid is 134.158 E (extent
133.95-134.44): project to **UTM 53N (EPSG:32653)**, Okayama's zone. OSM box
from the N03 extent, rounded out: (35.27, 133.94, 35.58, 134.45). Scaffold
with `scripts/scaffold_city.py ... --page-number <N>`, the number claimed at
build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band B, food
only (call 137); the downloads (call 141); `mode: metro`; the minor tier and
Japan West; the area-wide rows out as not premises (Kobe's trap 6; the
shared-code spelling is the build's); the four towns out (the city line
only); MHLW's point where the join misses (127c); tiers disclosed (145); the
Inbi Line's southern piece drawn and named (call 86).

**Open, each with a recommendation:**

1. **The Inbi Line in two pieces.** *Recommend drawing it as cut, two
   pieces, the label on each* (standing call 3: the line is cut at the city
   line wherever it crosses). Tradeoff: a 10 km gap across 八頭町 where the
   line visibly leaves and re-enters; the alternative, drawing the 八頭町
   stretch unringed, breaks the city-line rule every other page keeps.
2. **The food share to state (call 125).** *Recommend "about 8 in 10"*: the
   city's 1,573 fixed restaurant permits are 79.0% of e-Stat's whole 1,990,
   a lower bound (85% if e-Stat's figure covers the four towns), with the
   missing old-law permits named as the reason. Tradeoff: it may understate
   by a few points; a higher figure would rest on an apportionment, not a
   count.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control,
  `screen_japan_join.py minato` 98.0 / 0.2 / 1.8, and every city screen):
  the not-a-premises test for **鳥取県内, 県内, 鳥取県東部, 鳥取県** and for
  **鳥取市内 after the city's name repeats** (`鳥取県鳥取市鳥取市内` parses to
  town 鳥取市内; `citywide` tests only a bare 内); and the **other-municipality
  cut** (`鳥取県岩美郡…`, `鳥取県八頭郡…`), never left to `CITY_BBOX`.
- `as_of` pinned to MHLW's latest grant date in the file, never today.
- The old-law gap, measured if the city publishes its old-law stock; the
  factory share; gate 3 (JR West), OSM `name:en`, line colours on both
  basemaps, the opening view (`map-view`), `check_provenance.py`,
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "tottori-mhlw-live",
    "claim": "MHLW's open-data file for Tottori (31201), the food source, answers a plain keyless GET (1,629,218 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=31201_food_business_all.csv",
    "min_bytes": 1300000
  },
  {
    "id": "tottori-isj-block-live",
    "claim": "MLIT's block-level address file for Tottori (31201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/31201-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "tottori-isj-chome-live",
    "claim": "MLIT's town-chōme file for Tottori (31201) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/31201-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "tottori-pref-food-dataset",
    "claim": "The prefecture portal's Tottori City food dataset (1858) offers one notification CSV, 312011_food_business_all.csv - not a register; ASCII anchors only, as the host sends no charset",
    "kind": "http_contains",
    "url": "https://odp-pref-tottori.tori-info.co.jp/dataset/1858.html",
    "present": ["312011_food_business_all.csv", "/dataset/1858/resource/"]
  },
  {
    "id": "tottori-jrw-inbi-timetable",
    "claim": "JR West's station timetable for 鳥取 on the Inbi Line (3252057001, towards 郡家・津山) is live for 2026-10-07 - the frequency source for the southern piece",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/station-timetable/3252057001?date=20261007",
    "present": ["鳥取駅", "因美線", "class=\"destination\""]
  },
  {
    "id": "tottori-jrw-sanin-timetable",
    "claim": "JR West's station timetable for 鳥取 on the San'in Line (3252024001, towards 倉吉・米子) is live for 2026-10-07",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/station-timetable/3252024001?date=20261007",
    "present": ["鳥取駅", "山陰本線"]
  },
  {
    "id": "tottori-projected-crs",
    "claim": "Tottori projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 134.16,
    "expect": "EPSG:32653"
  }
]
```
