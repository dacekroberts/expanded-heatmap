# Nishitōkyō — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 109: `docs/decisions_drafts/staging.md`, "Wave 5, second half":
"Higashiyamato, Nishitōkyō, Tama and Higashimurayama on Tokyo's Tama ledgers
(call 109: the skew disclosed)"). The ledgers were approved and fetched for the
Tama measurement (wave 5, the Tama cities' call), MLIT's address blocks for the
block join (call 106), MHLW's file as a control (calls 106, 141, 147). **Step 0
measured 2026-10-06** (staging). Into `data/nishitokyo/raw/` (gitignored), each
from its publisher's own host with the project user-agent, each HTTP 200:

- From `www.hokeniryo.metro.tokyo.lg.jp` (東京都保健医療局, the Tokyo
  Metropolitan Government's health centres for Tama), fetched 2026-10-06 into
  `data/tokyo_tama/raw/` and **copied unchanged** into `data/nishitokyo/raw/`
  (and `data/higashiyamato/raw/`), because a Japanese build reads
  `data/<slug>/raw/` (Itami's precedent): `shokuhin-kyoka-7.csv`
  (**4,486,267 B**, food permits), `shokuhin-todokede-1-7.csv` (**1,956,304
  B**, food notifications), `kankyo-riyoujo-5.csv` (**165,277 B**, barbers),
  `kankyo-biyoujo-5.csv` (**608,582 B**, beauty salons), `kankyo-cleaning-5.csv`
  (**173,591 B**, laundries). All as of **2026-08-31**.
- From `i2fas.mhlw.go.jp`: `13000_food_business_all.csv`, **Tokyo
  Prefecture's file** (**3,606,399 B**, fetched 2026-10-06), the control. The
  city-code file (`13229_food_business_all.csv`) answers **HTTP 404** (MHLW
  publishes the Tokyo Metropolitan Government's area as one prefecture file).
- From `nlftp.mlit.go.jp` (cached by the block-join measurement):
  `isj/13229-24.0a.zip` (58,077 B) and `isj/13229-19.0b.zip` (6,298 B), copied
  into `data/nishitokyo/raw/isj/`.

**11,060,795 B in all; the only new download for the Tama briefs was MHLW's
prefecture file** (the 404 page answered for 13229 sits in the scratchpad
only). Nothing else was downloaded.

**Run `python scripts/brief_check.py nishitokyo` before writing any code.**
Then the `japan-city` skill, **Itami's shape** (`docs/build_briefs/itami.md`:
a prefecture's standing lists, every row assigned to the city by its address),
with **Higashiyamato as its twin on the same five files**
(`docs/build_briefs/higashiyamato.md`, which carries the ledgers' full
description; Tama and Higashimurayama are briefed separately on them too).
Read the `tokyo-ward` skill for how Tokyo's catalogue sources and credits were
handled. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py`'s own functions from scratch scripts
(`scripts/screen_japan_join.py` has no entry; its table is shared code and was
not edited). Rail: MLIT N02-25 cut at the N03 city line, through
`pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left
out, its station kept through the other lines, and drawn cut only where no
other line serves that station (owner, 2026-10-06, calls 54 and 92); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor for
JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at about
11 trains a day or fewer **named and drawn** (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The ledgers' skew is DISCLOSED on the page (owner, call 109, the band
row):** about 20% of rows opened after the control date, and the ledger misses
long-standing premises (new permits only from 2019-08; at the control date the
share is 58-75% across the Tama cities, **72.7% here**); laundry about half;
opt-outs and closures left out. **法人代表者氏名, the operator's address and
the phones are dropped at read** (call 109).

**✅ The licence (owner, call 108): the catalogue route, relied on** (Taitō's
precedent). The page links the Tokyo catalogue entries `t000055d0000000361`
and `t000055d0000000614`, **never the 保健医療局 page or files** (that site's
link policy). Below, "Licences".

**✅ The notifications ledger in Retail, disclosed as partial** (Ichinomiya's
call 127b applied: notifications in as a partial Food-shops layer where they
have hundreds of addressed rows). Here the Tokyo Metropolitan Government's own
届出 ledger is that layer (511 rows in the city, since 2021-06).

**✅ `mode`: `metro`.** The owner's rule (2026-10-02): no tram or light rail;
Seibu's two private heavy-rail lines make the whole network, which reads
`metro` (Kurume's, Higashiōsaka's and Itami's precedent).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).**
Nishitōkyō carries `label_tier: "minor"` and `"region": "Japan East"`
(`app/cities.py`); wave 4's first city to land retags Japan into the eight
regions, Nishitōkyō into **Kanto**. The city borders Tokyo's 練馬区 (the Tokyo
page's ward area) and sits near the other Tama cities: its label offset from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye. ⚠️
The page name carries "Tōkyō" inside it: the label and the page title must not
read as the Tokyo page.

---

## The one-line summary

**All three buckets from the Tokyo Metropolitan Government's monthly Tama
ledgers (CC BY 4.0 through the catalogue route, relied on, call 108), cut to
Nishitōkyō by address, as of 2026-08-31: 1,446 food permits (1,171
restaurants), 511 food notifications, 80 barbers, 236 beauty salons and 75
laundries.** The restaurants are **91.2% of the 1,284 in force** (Tokyo's
statistical yearbook, table 19-8, FY2024), flattered: **238 (20.3%) were first
permitted after the control date**, so the share at the control date is
**72.7%** (disclosed, call 109). Barbers about 82%, beauty salons about 97%,
laundries about 49% of census-scaled estimates (no official per-city count).
Through `japan_eigyo`: **Food service 987 rows (974 pins), Retail 288 permit
rows (233 pins) plus 380 notification rows** once the shared `自動車以外` trap
is fixed (336 before it); Personal services 388. **Block join 100.0%**, every
row in every ledger. **Rail: 5 N02 station groups**, all Seibu: the Shinjuku
Line 3 (6-20 an hour 07-18), the Ikebukuro Line 2 (8-20 an hour), read from
the operator's own timetables; nothing at or under 11 trains a day.

---

## Business leg — the Tokyo Metropolitan Government's Tama ledgers

Page `https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho`
(東京都が設置している保健所等で保有する台帳一覧, 更新日 2026-09-14; UTF-8), as
described in Higashiyamato's brief: the ledgers of the health centres the
Metropolitan Government runs (Tama less Hachiōji and Machida, plus the
islands), opt-outs and closed or suspended premises left out, vehicles, stalls
and vending left out of the food ledgers, items an applicant asked MHLW to
withhold withheld here too. **Nishitōkyō is 多摩小平保健所's** (小平市, 東村山市,
清瀬市, 東久留米市, 西東京市).

| Ledger (CSV, cp932) | Edition line on the page | Rows (all areas) | Rows in Nishitōkyō |
|---|---|---|---|
| `shokuhin-kyoka-7` 食品関係営業台帳（許可） | 「平成29年1月から令和8年8月までの新規許可施設及び平成29年4月から令和8年8月までの許可更新施設（令和8年8月31日現在）」 | 28,093 | **1,446** |
| `shokuhin-todokede-1-7` 食品関係営業台帳（届出） | 「令和3年6月から令和8年8月までの届出施設（令和8年8月31日現在）」 | 12,502 | **511** |
| `kankyo-riyoujo-5` 理容所台帳 | 「令和8年8月31日現在、台帳に掲載されている施設」 | 1,427 | **80** |
| `kankyo-biyoujo-5` 美容所台帳 | as above | 4,319 | **236** |
| `kankyo-cleaning-5` クリーニング所台帳 | as above | 1,040 | **75** |

Files at `https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/<name>`.
⚠️ **The slugs carry a revision suffix** (`-7`, `-1-7`, `-5`) that may move
with a monthly edition: `fetch_sources.py` takes them from the page's links (a
`SOURCE_LINKS` regex) and pins `SOURCE_AS_OF` to the page's
「令和8年8月31日現在」, never the fetch date.

- **Assigning a row to the city**: the address starts 東京都西東京市. ⚠️ **The
  city's name contains 東京**: strip the prefecture only as a leading
  `^東京都` (as `permits_from_rows` does), never by a bare replace of 東京, and
  match the city before any shorter Tama name (the measurement matched the
  longest name first). Every one of the city's rows has an address.
- **Columns, the shared tuples and the dropped columns**: as Higashiyamato's
  brief ("Business leg"): 屋号 / 施設名称, 営業所所在地 / 施設所在地, 営業の種類,
  営業形態 and 営業者氏名 are all known to `japan_register`; ⚠️
  `OPERATOR_COLS` also holds 法人代表者氏名, so the read drops it first (call
  109; measured: 0 rows withheld with it or without it). No 業態 column: the
  permit ledger's sub-type in brackets carries the form.

### The food permit ledger (1,446 rows in the city)

- **申請区分**: 新規 1,294, 更新 152. **Kinds**: 飲食店営業 1,171, 菓子製造業 147,
  魚介類販売業 37, 食肉販売業 35, そうざい製造業 18, アイスクリーム類製造業 7,
  麺類製造業 6, 漬物製造業 5, 豆腐製造業 4, 喫茶店営業 2, … Restaurant sub-types:
  一般飲食店 865, 集団給食 91, 弁当屋 73, そうざい店 51, バー・キャバレー 29, そば屋 20,
  すし屋 18, 仕出し屋 13, 喫茶店 6, 簡易な営業 3, 旅館・ホテル 2.
- **Against the yearbook** (table 19-8, FY2024, 西東京市; `japan_official`):
  **飲食店営業 1,171 of 1,284, 91.2%**. 菓子 147 of 165, 食肉販売 35 of 53,
  魚介類販売 37 of 55, そうざい製造 18 of 22, 麺類 6 of 6, 豆腐 4 of 5.
- **The dates (the skew, disclosed, call 109)**: restaurant 新規 rows were
  first permitted **2019-08-30 to 2026-08-26** (the ledger's earliest 新規
  month, not the 2017-01 the edition line names); 更新 rows carry first permits
  from 1970 to 2015-05. By first-permit year: 162 rows before 2021, then 198,
  168, 192, 167 a year (2021-2024), 190 in 2025 and 94 to 2026-08. **238
  restaurant rows (20.3%) were first permitted after 2025-03-31**, so at the
  yearbook's control date the ledger holds **933, 72.7%** of the 1,284.
- **Old-law permits are in the ledger** (not Kurashiki's trap): 喫茶店営業 2
  rows, and 更新 rows first permitted 1970-2015.
- **Duplicates**: 18 exact repeats of (address, trade name, kind); 173 rows
  repeat an (address, trade name) under another kind; **1,273 distinct
  premises**; one trade name blank. One pin per premises and bucket (trap 7).
- **Closures are left out at source**; no closure column. The page keeps "may
  include closed premises".

### The food notification ledger (511 rows)

- 届出年月日 1962-08-29 to 2026-08-24 (252 in 2021, then 31 to 58 a year);
  types: その他の食料・飲料販売業 169, 集団給食施設 89, コンビニエンスストア 81,
  百貨店、総合スーパー 44, 野菜果物販売業 32, 乳類販売業 23, 弁当販売業 12, …
- **Against the yearbook's columns**: コンビニエンスストア 81 of 82, 百貨店・総合スーパー
  44 of 46, 野菜果物販売業 32 of 37, 乳類販売業 **23 of 80**, 弁当販売業 12 of 16,
  米穀類販売業 8 of 4, 集団給食施設 89 of 93. Partial where the old-law permit
  holders were never re-filed (dairy), disclosed as partial (call 127b).
- ⚠️ **The `自動車以外` trap (shared code)**: 野菜果物販売業(自動車以外) 32 and
  弁当販売業(自動車以外) 12 are read as **mobile** by `permits_from_rows` (a bare
  `自動車` in the type) and as temporary or mobile by `japan_eigyo`. The build
  changes both tests to skip `自動車以外` (`自動車(?!以外)`), then re-runs the
  Minato control and every city screen; the 44 rows here become greengrocers
  and bento shops in Retail (Higashiyamato's brief has the ledger-wide count).

### Counts through `japan_eigyo` (fixed premises, today's shared code)

**Food service 987** (一般飲食店 865, 弁当屋 73, そば屋 20, すし屋 18, 喫茶店 6 and
喫茶店営業 2, 簡易 3; **974 pins**). **Retail from the permits 288** (菓子 147,
そうざい店 51, 魚介 37, 食肉 35, そうざい製造 18; **233 pins**). **Retail from the
notifications 336** (277 pins; **380 rows after the `自動車以外` fix**): other
food and drink sales 169, konbini 81, supermarkets 44, dairy 23, rice 8,
butcher 7, fishmonger 4. Left out: institutional catering 91 + 89, hostess
venues (バー・キャバレー, `docs/category_rules.md` R3) 29, event catering 13,
inside accommodation 2, linen supply 3, and 78 manufacturing types with no rule
(アイスクリーム, 調味料, コーヒー製造, 精穀, …), as in every built city.

**Economic Census control** (`scripts/japan_census_control.py` at build): the
2021 census counts **440** 飲食店 establishments in 13229
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 974 distinct placed
Food-service premises is **2.21 per establishment**, ⚠️ **above the built
cities' 1.56-1.92** (Akita's brief measured 2.11). Readings for the build to
test: 弁当屋 counted as Food service (73), several kinds per premises not
collapsed by trade-name spelling, and premises that closed without leaving the
ledger. Record the figure and the reading.

### Personal services: the three registers

| Register | Rows | Census 2021 | Estimate (census x Hachiōji's licensed-to-census ratio) | Share |
|---|---|---|---|---|
| 理容所台帳 (barbers) | **80** | 87 | 98 | **82%** (77% on all Tokyo's ratio) |
| 美容所台帳 (beauty) | **236** | 155 | 243 | **97%** (72%) |
| クリーニング所台帳 (laundry) | **75** (一般 33, 取次所 39, リネン 3) | 87 | 152 | **49%** (54%) |

Estimates, as Higashiyamato's (no official per-city count for a Tama city; the
band row's figures, reproduced). 確認年月日 run from 1964 to 2026-08
(barbers), 2026-06 (beauty) and 2025-06 (laundry): standing registers. No
repeats of (address, name); 12 addresses carry both a barber and a beauty
salon. The 3 リネン rows are linen supply, out by rule (72 laundry
storefronts).

### MHLW's Tokyo file (13000), a control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv`:
**3,606,399 B, 10,003 rows**, UTF-8 with BOM, the national schema. ⚠️
**市区町村名 reads 新宿区 on every row** (the registering office); filter by
営業施設所在地, never by 市区町村名.

- **326 rows in Nishitōkyō** (届出 226, 許可 100), dated 2021-07 to 2026-08,
  325 with their own point. Open restaurant permits 76.
- **Against the ledgers**: of 100 open permits, 59 are in a ledger by (town,
  number, trade name) and 90 by (town, number); **10 are not** (8 would be
  Food service, 2 Retail). Of 226 open notifications, 198 are in the ledger by
  (town, number); **28 are not** (8 would be Retail, 20 out: vending,
  catering).
- **Its own coordinates against the block point**: median **48 m**, 95.9%
  within 250 m (315 rows).
- Whether to add MHLW's rows the ledgers lack: open call 1.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13229-24.0a.zip` (58,077 B,
**1,679 block keys**), town-chōme `.../19.0b/13229-19.0b.zip` (6,298 B,
**114**). ⚠️ **`data/tokyo_tama/raw/isj/` holds four municipalities' pairs**,
all keyed under ward "" by `load_city_isj`, which globs its directory: the
build's `ISJ_DIR` must hold only 13229's pair (`data/nishitokyo/raw/isj/`, as
copied here). `japan.CITIES` entry at build: `"nishitokyo": {"name": "西東京市",
"pref": "13", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["13229"]}`.

| Tier, today's shared code | Rows | Block | Town-chōme | Unplaced |
|---|---|---|---|---|
| **Permits and registers (the band row's measure)** | 1,663 | **100.0%** | 0 | 0 |
| … Food service / Retail (permits) | 987 / 288 | 100% / 100% | 0 | 0 |
| … Barbers / beauty / laundry | 80 / 236 / 72 | 100% | 0 | 0 |
| Notifications, Retail | 336 | 100% | 0 | 0 |
| **All, with the notifications** | 1,999 | **100.0%** | 0 | 0 |

No miss to read: every row of every ledger finds its block.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_13_GML.zip`, N03 code 13229
(**15.75 km²**, extent W 139.517, S 35.711, E 139.569, N 35.762). Read with
`stub_test()`'s method and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Stations inside / on the line | Stations inside |
|---|---|---|---|
| 新宿線 (西武鉄道, 4) | Seibu Shinjuku Line | **3 / 29** | 田無, 西武柳沢, 東伏見 |
| 池袋線 (西武鉄道, 4) | Seibu Ikebukuro Line | **2 / 31** | ひばりヶ丘, 保谷 |

- **5 station records, 5 N02_005g groups**, no name in two groups, no pair
  closer than 600 m. **Median nearest-station gap 1,223 m** (1,011 to 2,044):
  rings by the spacing rule at build. 保谷 sits 51 m from the city line (練馬区
  beyond), ひばりヶ丘 250 m and 東伏見 267 m: their rings reach past it, but only
  businesses inside the city are counted (standing call 3).
- **Cut at the line**: the Shinjuku Line's 26 stations beyond (中野区 5, 新宿区 4,
  杉並区 3, 練馬区 2, 小平市 2, 東村山市 2, Saitama 8), the Ikebukuro Line's 29
  (練馬区 8, 豊島区 3, 清瀬市 2, 東久留米市 1, Saitama 15). Main lines cut at the
  line, not stubs.
- **The light-rail/rail test**: both are private heavy rail (N02 class 4). No
  tram, monorail or light rail.
- **Frequency, read 2026-10-06 from Seibu's own timetables**
  (`seibu.ekitan.com/norikae/timetable/station/<id>/d1` and `/d2`, `?dw=0`,
  weekday, the service date 2026-10-07) by plain GET with the project
  user-agent; every train's own entry counted, so trains starting at a
  station (田無 and 保谷 have many) are included:

  | Station (line, direction) | Weekday departures | Per hour 07-18 |
  |---|---|---|
  | 田無 238-16 (Shinjuku, to 高田馬場・西武新宿 / to 所沢・本川越・拝島) | 244 / 213 | 12-20 / 9-17 |
  | 西武柳沢 238-15 (Shinjuku, same) | 139 / 147 | 6-12 / 6-14 |
  | 東伏見 238-14 (Shinjuku, same) | 139 / 147 | 6-12 / 6-13 |
  | 保谷 235-11 (Ikebukuro, to 練馬・池袋 / to 所沢・飯能) | 220 / 164 | 9-18 / 8-13 |
  | ひばりヶ丘 235-12 (Ikebukuro, same) | 247 / 256 | 12-18 / 11-20 |

  **No stretch is at or under about 11 trains a day** (call 86): the
  thinnest, 西武柳沢 and 東伏見, have 139 and 147, six an hour midday. The band
  row's "9-13 and 12-14 an hour"
  was the probe's reader, which skipped trains starting at a station (marked
  `ekptime underline`); the counts above replace it. Counts only; no
  timetable on the page.
- ⚠️ **Gate 3** at build: Seibu's station counts inside the city (Shinjuku 3,
  Ikebukuro 2). **OSM `name:en`** for 5 groups (one Overpass query at build,
  in the box below; not queried here).

## Scope

**Nishitōkyō City.** The Shinjuku Line runs on to 高田馬場 and 西武新宿 east and
to 小平 and 所沢 west, the Ikebukuro Line to 池袋 and to 所沢 and 飯能; cut at the
line. The Tokyo page covers the 23 special wards only; Nishitōkyō is its own
page (the band).

## Licences

**Read 2026-10-06 by staging's licence-read agent and recorded in
`docs/decisions_drafts/staging.md` ("Wave 5, second half"): PERMITTED WITH
CONDITIONS through the catalogue route, relied on (owner, call 108, Taitō's
precedent).** No verdict is written in this brief; take the credit from
staging's record. What it rests on, as Higashiyamato's brief sets out:

- **The catalogue entries** `t000055d0000000361` 食品関係営業台帳 and
  `t000055d0000000614` 環境衛生施設台帳 (`catalog.data.metro.tokyo.lg.jp`), each
  `license_id: CC-BY-4.0`, organisation 東京都保健医療局.
- **The Tokyo Open Data Terms** (`https://portal.data.metro.tokyo.lg.jp/terms/`,
  2017-03-24) §2: CC BY 4.0, 「商用利用も可能です」; §2(1)イ's modified-use
  credit (the title, 東京都, the CC BY 4.0 link, and that the data was edited),
  and never presenting the result as made by Tokyo or a municipality. Tokyo's
  own catalogue notice (`pipeline/tokyo/credits.py`, the "catalogue" form) is
  the built precedent; confirm the wording against staging's record.
- **The host site's own policy** (保健医療局) bars reuse and links below its
  top page: **the page links the two catalogue entries, never the 保健医療局 page
  or files.** `fetch_sources.py` downloads from that host (an automated GET,
  not a link).
- **MHLW open data** (only if open call 1 is taken): PDL 1.0 as recorded in
  `docs/data_sources/japan.md`.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **The yearbook and the census**:
  measurement sources, not drawn. **Seibu's timetables**: read for counts only.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here; one row in `docs/data_sources/japan.md`
  serves the Tama ledgers for every Tama city.

## Privacy

- **Dropped at read (call 109)**: 法人代表者氏名, 営業者住所 and 営業者ビル名 (the
  operator's own address), and every phone column. Only 屋号 / 施設名称, the
  premises address and the type are ever selected; 営業者氏名 is read IN MEMORY
  for the name rule and never written.
- **The operator column, measured** (counts only): food permits 1,446,
  営業者氏名 filled on 764 (a company marker on 739, none on 25), **blank on
  682**; notifications 511, filled 377 (366 / 11), blank 134; barbers 80,
  filled 16 (all companies), blank 64; beauty 236, filled 84 (all companies),
  blank 152; laundry 75, filled 44 (all companies), blank 31. The operator is
  published almost only for companies: the blanks are the shape of individuals
  withheld at source.
- **The name rule, version 2, measured in memory**: the sign rule 0, the
  operator comparison 0, **0 rows withheld** in any ledger, with or without
  法人代表者氏名.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; if open call 1
  brings its rows in, its 法人名 joins the name rule (owner, 2026-10-05).
- Run `check_personal_exposure.py nishitokyo` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.517-139.569 E, centroid 139.546:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded out:
(35.71, 139.51, 35.77, 139.57). Slug `nishitokyo`, page name "Nishitōkyō".
Scaffold with `scripts/scaffold_city.py ... --page-number <N>`, the number
claimed at build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band A with the
skew disclosed and the three columns dropped at read (call 109); the catalogue
route and its credit (call 108); the notifications in as partial Retail (call
127b); `mode: metro`; the minor tier and Japan East (Kanto after the retag);
no frequency floor.

**Answered by the owner on 2026-10-06:** call 169, **MHLW's rows the ledgers lack added** for all four Tama cities (Tokyo wards' precedent of 2026-09-24: the ledger's row kept where both hold a premises, `SUPERSEDES`; MHLW's PDL 1.0 notice line added; the share the page states stays without MHLW's rows). The recommendations below are kept as the record.

**Weighed, with a recommendation:**

1. **MHLW's rows the ledgers lack** (10 open permits, 28 open notifications
   here; 8 permits would be Food service). Tokyo's wards (2026-09-24: MHLW's
   slice added to the partial ward lists, the ward's row kept, `SUPERSEDES`)
   against Ichinomiya's call 127 (MHLW's extra permits left out). *Recommend
   Tokyo's*, decided once for all four Tama cities (Higashiyamato's brief, open
   call 1); the share the page states stays WITHOUT MHLW's rows. Tradeoff: a
   second source and its PDL notice line for about 18 premises here.

## Personal services against Tokyo's yearbook table 19-7 (owner, call 189)

**Answered by the owner on 2026-10-06:** call 189, "fetch at once": Tokyo's statistical yearbook table 19-7 (環境衛生営業施設数, `https://www.toukei.metro.tokyo.lg.jp/tnenkan/2024/tn24qv190700.csv`, 6,876 B, HTTP 200, into `data/tokyo/raw/`; the publisher of table 19-8) gives the official count of each register at the end of FY2024 (2025-03-31). **It supersedes the census-scaled estimates above** for these three registers; the estimates are kept as the record.

| Register | Ledger rows (2026-08-31) | Confirmed on or before 2025-03-31 (確認年月日) | Yearbook FY2024 | Share, all rows | Share at the yearbook's date |
|---|---|---|---|---|---|
| Barbers (理容所) | 80 | 78 | 84 | 95.2% | **92.9%** |
| Beauty salons (美容所) | 236 | 226 | 256 | 92.2% | **88.3%** |
| Laundries (クリーニング所, storeless counters out) | 75 | 73 | 87 | 86.2% | **83.9%** |

The share at the yearbook's date is the one the page states, as the food share is (calls 187-188); it is a lower bound, since 確認年月日 is the confirmation date, which a change of operator renews. Measured by staging's scratch script `t197_measure.py` (counts only; operator, address and phone columns dropped at read); the build re-measures it in step 2.

## What the build must still measure

- ⚠️ **Shared code** (followed by the Minato control and every city screen):
  the `自動車以外` lookahead in `permits_from_rows` and `japan_eigyo` (44 rows
  here).
- The read: drop 法人代表者氏名, 営業者住所, 営業者ビル名 and the phones first;
  `SOURCE_KIND` per register file; the city cut by a leading 東京都西東京市;
  `SOURCE_LINKS` for the slugs; `SOURCE_AS_OF` 2026-08-31 from the page.
- `ISJ_DIR` holding only 13229's pair; the share and its control-date figure
  (the yearbook's 1,284) and the page's disclosure sentence from the approved
  template (call 109); the census ratio (2.21, above the built range) and its
  reading.
- Gate 3; OSM `name:en`; line colors on both basemaps; the opening view
  (`map-view`); the factory share; `check_provenance.py`;
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "nishitokyo-ledger-page",
    "claim": "The Tama ledgers page names the five ledgers, their windows, the opt-out and closure rule, and Nishitōkyō under 多摩小平保健所",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["平成29年1月から令和8年8月までの新規許可施設", "令和3年6月から令和8年8月までの届出施設", "公表を希望しない施設", "多摩小平保健所", "西東京市", "shokuhin-kyoka-7", "shokuhin-todokede-1-7", "kankyo-riyoujo-5", "kankyo-biyoujo-5", "kankyo-cleaning-5"]
  },
  {
    "id": "nishitokyo-ledger-edition",
    "claim": "The edition measured here: the ledgers as of 2026-08-31 (a failure here means a new monthly edition: re-measure)",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["令和8年8月31日現在"]
  },
  {
    "id": "nishitokyo-food-permits-file",
    "claim": "The food permit ledger (4,486,267 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-kyoka-7",
    "min_bytes": 2000000
  },
  {
    "id": "nishitokyo-food-notifications-file",
    "claim": "The food notification ledger (1,956,304 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-todokede-1-7",
    "min_bytes": 1500000
  },
  {
    "id": "nishitokyo-barber-file",
    "claim": "The barber ledger (165,277 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-riyoujo-5",
    "min_bytes": 100000
  },
  {
    "id": "nishitokyo-beauty-file",
    "claim": "The beauty-salon ledger (608,582 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-biyoujo-5",
    "min_bytes": 400000
  },
  {
    "id": "nishitokyo-laundry-file",
    "claim": "The laundry ledger (173,591 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-cleaning-5",
    "min_bytes": 100000
  },
  {
    "id": "nishitokyo-catalogue-food",
    "claim": "Tokyo's catalogue entry t000055d0000000361 (食品関係営業台帳) declares CC BY 4.0 and points at the 保健医療局 ledger page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000361",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "nishitokyo-catalogue-registers",
    "claim": "Tokyo's catalogue entry t000055d0000000614 (環境衛生施設台帳) declares CC BY 4.0 and points at the same page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000614",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "nishitokyo-tokyo-terms",
    "claim": "The Tokyo Open Data Terms allow commercial use and prescribe a modified-use credit",
    "kind": "http_contains",
    "url": "https://portal.data.metro.tokyo.lg.jp/terms/",
    "present": ["商用利用も可能", "改変して利用", "編集・加工等を行った旨"]
  },
  {
    "id": "nishitokyo-mhlw-tokyo",
    "claim": "MHLW's Tokyo Prefecture file (13000, 3,606,399 B) answers a plain keyless GET (a control; the 13229 file answers 404)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "nishitokyo-isj-block-live",
    "claim": "MLIT's block-level address file for Nishitōkyō (13229) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13229-24.0a.zip",
    "min_bytes": 40000
  },
  {
    "id": "nishitokyo-isj-chome-live",
    "claim": "MLIT's town-chōme file for Nishitōkyō (13229) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/13229-19.0b.zip",
    "min_bytes": 4000
  },
  {
    "id": "nishitokyo-seibu-tanashi",
    "claim": "Seibu's weekday timetable for 田無 (Shinjuku Line, station 238-16) is live and lists each train",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/238-16/d1?dw=0",
    "present": ["田無の時刻表", "openOneTrainTimetable"]
  },
  {
    "id": "nishitokyo-seibu-higashifushimi",
    "claim": "Seibu's weekday timetable for 東伏見 (238-14), one of the two thinnest stations, is live",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/238-14/d1?dw=0",
    "present": ["東伏見の時刻表", "openOneTrainTimetable"]
  },
  {
    "id": "nishitokyo-seibu-hoya",
    "claim": "Seibu's weekday timetable for 保谷 (Ikebukuro Line, station 235-11) is live",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/235-11/d1?dw=0",
    "present": ["保谷の時刻表", "openOneTrainTimetable"]
  },
  {
    "id": "nishitokyo-projected-crs",
    "claim": "Nishitōkyō projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.55,
    "expect": "EPSG:32654"
  }
]
```
