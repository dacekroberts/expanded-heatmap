# Higashiyamato — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 109: `docs/decisions_drafts/staging.md`, "Wave 5, second half":
"Higashiyamato, Nishitōkyō, Tama and Higashimurayama on Tokyo's Tama ledgers
(call 109: the skew disclosed)"). The ledgers were approved and fetched for the
Tama measurement (wave 5, the Tama cities' call), MLIT's address blocks for the
block join (call 106), MHLW's file as a control (calls 106, 141, 147). **Step 0
measured 2026-10-06** (staging). Into `data/higashiyamato/raw/` (gitignored),
each from its publisher's own host with the project user-agent, each HTTP 200:

- From `www.hokeniryo.metro.tokyo.lg.jp` (東京都保健医療局, the Tokyo
  Metropolitan Government's health centres for Tama), fetched 2026-10-06 into
  `data/tokyo_tama/raw/` and **copied unchanged** into `data/higashiyamato/raw/`
  (and `data/nishitokyo/raw/`), because a Japanese build reads
  `data/<slug>/raw/` (Itami's precedent): `shokuhin-kyoka-7.csv`
  (**4,486,267 B**, food permits), `shokuhin-todokede-1-7.csv` (**1,956,304
  B**, food notifications), `kankyo-riyoujo-5.csv` (**165,277 B**, barbers),
  `kankyo-biyoujo-5.csv` (**608,582 B**, beauty salons), `kankyo-cleaning-5.csv`
  (**173,591 B**, laundries). All as of **2026-08-31**.
- From `i2fas.mhlw.go.jp`: `13000_food_business_all.csv`, **Tokyo
  Prefecture's file** (**3,606,399 B**, fetched 2026-10-06), the control. The
  city-code file (`13220_food_business_all.csv`) answers **HTTP 404** (MHLW
  publishes the Tokyo Metropolitan Government's area as one prefecture file).
- From `nlftp.mlit.go.jp` (cached by the block-join measurement):
  `isj/13220-24.0a.zip` (43,084 B) and `isj/13220-19.0b.zip` (5,760 B), copied
  into `data/higashiyamato/raw/isj/`.

**11,045,264 B in all; the only new download for this brief was MHLW's
prefecture file** (the 404 page answered for 13220 sits in the scratchpad
only). Nothing else was downloaded.

**Run `python scripts/brief_check.py higashiyamato` before writing any code.**
Then the `japan-city` skill, **Itami's shape** (`docs/build_briefs/itami.md`:
a prefecture's standing lists, every row assigned to the city by its address),
with **Nishitōkyō as its twin on the same five files**
(`docs/build_briefs/nishitokyo.md`; Tama and Higashimurayama are briefed
separately on them too). Read the `tokyo-ward` skill for how Tokyo's catalogue
sources and credits were handled. Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py`'s own functions from
scratch scripts (`scripts/screen_japan_join.py` has no entry; its table is
shared code and was not edited). Rail: MLIT N02-25 cut at the N03 city line,
through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

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
share is 58-75% across the Tama cities, **75.2% here**); laundry about half;
opt-outs and closures left out. **法人代表者氏名, the operator's address and
the phones are dropped at read** (call 109).

**✅ The licence (owner, call 108): the catalogue route, relied on** (Taitō's
precedent). The page links the Tokyo catalogue entries `t000055d0000000361`
and `t000055d0000000614`, **never the 保健医療局 page or files** (that site's
link policy). Below, "Licences".

**✅ The notifications ledger in Retail, disclosed as partial** (Ichinomiya's
call 127b applied: notifications in as a partial Food-shops layer where they
have hundreds of addressed rows). Here the Tokyo Metropolitan Government's own
届出 ledger is that layer (269 rows in the city, since 2021-06).

**✅ The Seibu Haijima Line's one station, 東大和市, stays as cut** (standing
call 3: a private one-station stub). Below, "Rail".

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).**
Higashiyamato carries `label_tier: "minor"` and `"region": "Japan East"`
(`app/cities.py`); wave 4's first city to land retags Japan into the eight
regions, Higashiyamato into **Kanto**. Its dot sits beside Higashimurayama's
(Band A, briefed, not yet built) and the other Tama cities': its label offset from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

---

## The one-line summary

**All three buckets from the Tokyo Metropolitan Government's monthly Tama
ledgers (CC BY 4.0 through the catalogue route, relied on, call 108), cut to
Higashiyamato by address, as of 2026-08-31: 603 food permits (505 restaurants),
269 food notifications, 44 barbers, 86 beauty salons and 19 laundries.** The
restaurants are **95.6% of the 528 in force** (Tokyo's statistical yearbook,
table 19-8, FY2024), flattered: **108 (21.4%) were first permitted after the
control date**, so the share at the control date is **75.2%** (disclosed,
call 109). Barbers about 87%, beauty salons about 77%, laundry counters about
43% of census-scaled estimates (no official per-city count). Through
`japan_eigyo`: **Food service 420 rows (410 pins), Retail 116 permit rows (83
pins) plus 218 notification rows** once the shared `自動車以外` trap is fixed
(192 before it); Personal services 149. **Block join 98.0%** (permits and
registers; 95.8% with the notifications), 1 row unplaced. **Rail: 4 N02
station groups**: the Tama Toshi Monorail 3 (120 weekday departures each way,
6-10 an hour 07-18) and the Seibu Haijima Line 1 (東大和市, 113 each way, 5-8
an hour), read from the operators' own timetables; nothing at or under 11
trains a day.

---

## Business leg — the Tokyo Metropolitan Government's Tama ledgers

Page `https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho`
(東京都が設置している保健所等で保有する台帳一覧, 更新日 2026-09-14; UTF-8). The
ledgers cover the health centres the Metropolitan Government runs: Tama less
Hachiōji and Machida, plus the islands. **Higashiyamato is 多摩立川保健所's**
(立川市, 昭島市, 国分寺市, 国立市, 東大和市, 武蔵村山市). The page: 「ホームページへの公表を希望しない施設、廃止・休止している施設は除いて公表しています」
(opt-outs and closed or suspended premises are left out) and, for food,
「移動販売、臨時販売、自動車販売、自動販売機、行商、催事等期間短縮申請があったもの、届出が不要な施設及び廃業した施設は除いています」.
Items an applicant asked MHLW to withhold are withheld here too (「厚生労働省のオープンデータにて、申請者が非公表を希望した項目については東京都のオープンデータでも非公表としています」).

| Ledger (CSV, cp932) | Edition line on the page | Rows (all areas) | Rows in Higashiyamato |
|---|---|---|---|
| `shokuhin-kyoka-7` 食品関係営業台帳（許可） | 「平成29年1月から令和8年8月までの新規許可施設及び平成29年4月から令和8年8月までの許可更新施設（令和8年8月31日現在）」 | 28,093 | **603** |
| `shokuhin-todokede-1-7` 食品関係営業台帳（届出） | 「令和3年6月から令和8年8月までの届出施設（令和8年8月31日現在）」 | 12,502 | **269** |
| `kankyo-riyoujo-5` 理容所台帳 | 「令和8年8月31日現在、台帳に掲載されている施設」 | 1,427 | **44** |
| `kankyo-biyoujo-5` 美容所台帳 | as above | 4,319 | **86** |
| `kankyo-cleaning-5` クリーニング所台帳 | as above | 1,040 | **19** |

Files at `https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/<name>`
(each also offered as Excel; the CSV is read). ⚠️ **The slugs carry a
revision suffix** (`-7`, `-1-7`, `-5`) that may move with a monthly edition:
`fetch_sources.py` takes them from the page's links (a `SOURCE_LINKS` regex,
Akita's and Kawasaki's precedent) and pins `SOURCE_AS_OF` to the page's
「令和8年8月31日現在」, never the fetch date. The edition check below fails
when a new month lands: re-measure then.

- **Assigning a row to the city**: the address starts 東京都東大和市 (the
  prefecture is written on every row). Every one of the city's rows has an
  address; 251 permit rows across the ledger are blank and 2,032 belong to
  other municipalities. `permits_from_rows(rows, "東京都", "東大和市",
  wardless=True)` strips both.
- **Columns** (permits): 屋号, **営業所所在地**, 営業者氏名, 営業者住所 (never),
  **営業の種類**, **申請区分** (新規 / 更新), 営業所電話番号 (never),
  **初回許可日**, 営業者電話番号 (never), 法人代表者氏名 (dropped at read, call
  109). Notifications: the same less 申請区分, with **届出年月日**. Registers:
  確認番号, **施設名称**, 施設TEL (never), **施設所在地**, 施設ビル名, 営業者氏名,
  法人代表者氏名 (dropped), 営業者住所 (never), 営業者ビル名 (never), 営業者TEL
  (never), 確認年月日; the laundry ledger adds **営業形態**.
- **Against the shared tuples**: 営業所所在地 and 施設所在地 are in `ADDR_COLS`,
  屋号 and 施設名称 in `NAME_COLS`, 営業の種類 and 営業形態 in `TYPE_COLS`,
  営業者氏名 in `OPERATOR_COLS`. ⚠️ **`OPERATOR_COLS` also holds
  法人代表者氏名**, so the read must drop it before rows reach the name rule
  (measured: the rule withholds 0 rows with it or without it). **No 業態
  column**: the permit ledger's sub-type in brackets carries the form
  (`飲食店営業(集団給食)`, `(仕出し屋)`, `(旅館・ホテル)`, `(バー・キャバレー)`),
  and `japan_eigyo` reads it from the type. Vehicles, stalls and vending are
  left out at source.

### The food permit ledger (603 rows in the city)

- **申請区分**: 新規 525, 更新 78. **Kinds**: 飲食店営業 505, 菓子製造業 48,
  食肉販売業 22, 魚介類販売業 15, 乳製品製造業 4, 麺類製造業 2, 喫茶店営業 2,
  others 1 each. Restaurant sub-types: 一般飲食店 367, 集団給食 32, そうざい店 30,
  弁当屋 25, バー・キャバレー 15, そば屋 14, すし屋 9, 仕出し屋 8, 旅館・ホテル 2,
  喫茶店 2, 簡易な営業 1.
- **Against the yearbook** (table 19-8, FY2024, 東大和市; `japan_official`):
  **飲食店営業 505 of 528, 95.6%**. 菓子 48 of 59, 食肉販売 22 of 34, 魚介類販売
  15 of 22, そうざい製造 1 of 5, 麺類 2 of 2, 豆腐 1 of 1.
- **The dates (the skew, disclosed, call 109)**: restaurant 新規 rows were
  first permitted **2020-07-07 to 2026-08-26** (ledger-wide the earliest 新規 is
  **2019-08**, not the 2017-01 the edition line names); 更新 rows carry first
  permits from 1977 to 2015-05. By first-permit year: 74 rows before 2021, then
  80, 75, 74, 75 a year (2021-2024), 64 in 2025 and 63 to 2026-08. **108
  restaurant rows (21.4%) were first permitted after 2025-03-31**, so at the
  yearbook's control date the ledger holds **397, 75.2%** of the 528: the
  share above is flattered by new openings, and premises permitted before
  2019-08 that were not renewed since 2017-04 are missing.
- **Old-law permits are in the ledger** (not Kurashiki's trap): 喫茶店営業 (an
  old-law type only) 2 rows, and 更新 rows first permitted 1977-2015. The gap is
  the ledger's own window, above, not the law change.
- **Duplicates**: 14 exact repeats of (address, trade name, kind); 75 rows
  repeat an (address, trade name) under another kind; **528 distinct
  premises**. One pin per premises and bucket (trap 7).
- **Closures are left out at source** (the page); no closure column. The page
  keeps "may include closed premises" all the same (the monthly edition lags).

### The food notification ledger (269 rows)

- 届出年月日 1968-10-31 to 2026-07-27 (103 in 2021, then 20 to 50 a year);
  types: その他の食料・飲料販売業 111, 集団給食施設 35, コンビニエンスストア 31,
  百貨店、総合スーパー 24, 野菜果物販売業 14, 弁当販売業 12, 乳類販売業 11, 米穀類販売業
  6, …
- **Against the yearbook's columns**: コンビニエンスストア 31 of 34, 百貨店・総合スーパー
  24 of 24, 野菜果物販売業 14 of 11, 乳類販売業 **11 of 42**, 弁当販売業 12 of 6,
  米穀類販売業 6 of 6, 集団給食施設 35 of 37. Partial where the old-law permit
  holders were never re-filed (dairy above), disclosed as partial (call 127b).
- ⚠️ **The `自動車以外` trap (shared code)**: 野菜果物販売業(自動車以外) 14 and
  弁当販売業(自動車以外) 12 ("other than a vehicle") are read as **mobile** by
  `permits_from_rows` (its vehicle test is a bare `自動車` in the type) and as
  temporary or mobile by `japan_eigyo`. Ledger-wide 1,063 rows (626 + 437), in
  every Tama city. The build changes both tests to skip `自動車以外` (a
  lookahead, `自動車(?!以外)`), then re-runs the Minato control and every city
  screen; the 26 rows here become greengrocers and bento shops in Retail.

### Counts through `japan_eigyo` (fixed premises, today's shared code)

**Food service 420** (一般飲食店 367, 弁当屋 25, そば屋 14, すし屋 9, 喫茶店 2 and
喫茶店営業 2, 簡易 1; **410 pins**). **Retail from the permits 116** (そうざい店 30,
食肉 22, 菓子 48, 魚介 15, そうざい製造 1; **83 pins**). **Retail from the
notifications 192** (165 pins; **218 rows after the `自動車以外` fix**): other
food and drink sales 111, konbini 31, supermarkets 24, dairy 11, rice 6, butcher
5, fishmonger 4. Left out: institutional catering 32 + 35, hostess venues
(バー・キャバレー, `docs/category_rules.md` R3) 15, event catering 8, inside
accommodation 2, mail order 1, a non-business stall 1, and 24 manufacturing
types with no rule (乳製品, 麺類, コーヒー製造, …), as in every built city.

**Economic Census control** (`scripts/japan_census_control.py` at build): the
2021 census counts **240** 飲食店 establishments in 13220
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 409 distinct placed
Food-service premises is **1.70 per establishment**, inside the built cities'
1.56-1.92.

### Personal services: the three registers

| Register | Rows | Census 2021 | Estimate (census x Hachiōji's licensed-to-census ratio) | Share |
|---|---|---|---|---|
| 理容所台帳 (barbers) | **44** | 45 | 50 | **87%** (82% on all Tokyo's ratio) |
| 美容所台帳 (beauty) | **86** | 71 | 111 | **77%** (57%) |
| クリーニング所台帳 (laundry) | **19** (一般 8, 取次所 10, 一般＋リネン 1) | 25 | 44 | **43%** (48%) |

No official per-city count exists for a Tama city (e-Stat's 衛生行政報告例
lists Hachiōji alone), so the shares are estimates (the band row's figures,
reproduced). 確認年月日 run from 1962 to 2023-03 (barbers), 2026-07
(beauty) and 2024-11 (laundry): **standing registers**, not a stream. No
repeats of (address, name); 2 addresses carry both a barber and a beauty
salon. No 無店舗取次店 in the city (that kind reads as not a premises through
`無店舗`).

### MHLW's Tokyo file (13000), a control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv`:
**3,606,399 B, 10,003 rows**, UTF-8 with BOM, the national schema. ⚠️
**市区町村名 reads 新宿区 on every row** (the registering office); the premises'
city is in 営業施設所在地, so the build filters by address, never by 市区町村名.

- **140 rows in Higashiyamato** (届出 103, 許可 36, 許可(廃業) 1), dated 2021-10
  to 2026-07, every one with its own point. Open restaurant permits 30.
- **Against the ledgers**: of 36 open permits, 24 are in a ledger by (town,
  number, trade name) and by (town, number); **12 are not** (6 would be Food
  service, 5 Retail, 1 out). The 10 restaurant permits missing by trade name
  were first permitted 2024-2026. Of 103 open notifications, 36 are in the
  ledger by (town, number); **67 are not** (45 would be Retail, 22 out:
  vending, catering, peddling).
- **Its own coordinates against the block point**: median **50 m**, 97.4%
  within 250 m (114 rows).
- Whether to add MHLW's rows the ledgers lack: open call 1.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13220-24.0a.zip` (43,084 B,
**3,509 block keys**), town-chōme `.../19.0b/13220-19.0b.zip` (5,760 B,
**76**). ⚠️ **`data/tokyo_tama/raw/isj/` holds four municipalities' pairs**,
all keyed under ward "" by `load_city_isj`, which globs its directory: the
build's `ISJ_DIR` must hold only 13220's pair (`data/higashiyamato/raw/isj/`,
as copied here). `japan.CITIES` entry at build: `"higashiyamato": {"name":
"東大和市", "pref": "13", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES,
"wardless": True, "wards": ["13220"]}`.

| Tier, today's shared code | Rows | Block | Town-chōme | Unplaced |
|---|---|---|---|---|
| **Permits and registers (the band row's measure)** | 685 | **98.0%** | 1.9% | 0.1% (1) |
| … Food service / Retail (permits) | 420 / 116 | 97.6% / 98.3% | 2.1 / 1.7 | 0.2 / 0 |
| … Barbers / beauty / laundry | 44 / 86 / 19 | 100% / 97.7% / 100% | 0 / 2.3 / 0 | 0 |
| Notifications, Retail | 192 | 88.0% | 12.0% | 0 |
| **All, with the notifications** | 877 | **95.8%** | 4.1% | 0.1% (1) |

**The misses, read** (towns only, by `measure.py` in the scratchpad):
- **Chōme tier (36)**: `N番地のN` addresses in towns whose number MLIT's block
  file does not hold (清原1丁目 11, 立野1丁目 6, 桜が丘1丁目 5, 桜が丘4丁目 2, 高木3丁目
  2, 立野3丁目 2, …): they take the chōme's centroid. 23 of the 36 are
  notifications.
- **Unplaced (1)**: 桜ケ丘3丁目 written with ケ, where MLIT writes 桜が丘. One
  row: no shared rule proposed (a city-local alias at most, with the Minato
  control).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_13_GML.zip`, N03 code 13220
(**13.42 km²**, extent W 139.392, S 35.730, E 139.452, N 35.770). Read with
`stub_test()`'s method and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Stations inside / on the line | Stations inside |
|---|---|---|---|
| 多摩都市モノレール線 (多摩都市モノレール, 5) | Tama Toshi Monorail | **3 / 19** | 上北台 (the northern terminus), 桜街道, 玉川上水 |
| 拝島線 (西武鉄道, 4) | Seibu Haijima Line | **1 / 8** | 東大和市 |

- **4 station records, 4 N02_005g groups**, no name in two groups, no pair
  closer than 600 m. **Median nearest-station gap 769 m** (749 to 1,500): rings
  by the spacing rule at build.
- **Near the line, outside**: Seibu's own 玉川上水 platform is **32 m outside**
  (立川市; the monorail's 玉川上水, 16 m inside, keeps the ring); Seibu Tamako
  Line's 武蔵大和 26 m and the Seibu Yamaguchi Line's 西武園ゆうえんち 43 m
  outside. None gets a ring here (standing call 3); a business near
  them goes to its nearest station inside the city.
- **Cut at the line**: the monorail's 16 stations beyond (立川市 7, 日野市 5,
  八王子市 3, 多摩市 1); the Haijima Line's 7 (立川市 3, 小平市 2, 東村山市 1,
  昭島市 1).
- **The light-rail/rail test**: the monorail is N02 class 5, a straddle
  monorail on its own viaduct (rail, as the Maihama Resort Line, call 53); the
  Haijima Line is private heavy rail (class 4). No tram.
- **The stub test.** The monorail keeps 3 of 19, an urban line with three
  stations: not a stub. **The Haijima Line keeps one station of 8, 東大和市**
  (19 m from the city line), a private line: drawn as cut by the standing call,
  **no owner question** (Kobe's JR Takarazuka Line, Akita's Oga Line). Its
  permanent label and legend entry on the short in-city stretch: measure
  placement in a scratch render.
- **Frequency, read 2026-10-06 from the operators' own timetables** by plain
  GET with the project user-agent; every departure on each page counted, marked
  ones included:

  | Station (line, direction) | Weekday departures | Per hour 07-18 |
  |---|---|---|
  | 上北台 (monorail, to 多摩センター; the terminus) | 120 | 6-9 |
  | 桜街道 (monorail, to 多摩センター / to 上北台) | 120 / 120 | 6-10 |
  | 玉川上水 (monorail, to 多摩センター / to 上北台) | 120 / 120 | 5-10 |
  | 東大和市 (Seibu Haijima, to 萩山・小平・西武新宿 / to 拝島) | 113 / 113 | 5-8 |

  Monorail: the station PDFs `TT17`-`TT19` linked from each station's
  timetable page (`tama-monorail.co.jp/monorail/station/<station>/timetable.html`),
  read with `pdftotext`; their header carries the revision dates 2022-03-12 and
  2023-03-20; every 10 minutes midday, every 6 to 9 minutes at the peaks.
  Seibu: `seibu.ekitan.com/norikae/timetable/station/234-9/d1` and `/d2`
  (`?dw=0`, weekday; the service date 2026-10-07), counted from each train's
  own entry, which includes trains starting there. **No stretch is at or under
  about 11 trains a day** (call 86). Counts only; no timetable on the page.
- ⚠️ **Gate 3** at build: the operators' station counts inside the city
  (monorail 3, Seibu 1). **OSM `name:en`** for 4 groups (one Overpass query at
  build, in the box below; not queried here).

## Scope

**Higashiyamato City.** The monorail runs on south through 立川 to 多摩センター,
the Haijima Line east to 小平 and west to 拝島; cut at the line. The Tokyo page
covers the 23 special wards only; Higashiyamato is its own page (the band).

## Licences

**Read 2026-10-06 by staging's licence-read agent and recorded in
`docs/decisions_drafts/staging.md` ("Wave 5, second half"): PERMITTED WITH
CONDITIONS through the catalogue route, relied on (owner, call 108, Taitō's
precedent).** No verdict is written in this brief; take the credit from
staging's record. What it rests on:

- **The catalogue entries** (`catalog.data.metro.tokyo.lg.jp`):
  `t000055d0000000361` 食品関係営業台帳 and `t000055d0000000614` 環境衛生施設台帳,
  each `license_id: CC-BY-4.0`, organisation 東京都保健医療局, maintainer
  保健政策部保健政策課, each resource pointing at the 保健医療局 page above.
- **The Tokyo Open Data Terms** (`https://portal.data.metro.tokyo.lg.jp/terms/`,
  2017-03-24) §2: CC BY 4.0, 「商用利用も可能です」; §2(1)イ, for modified use,
  the credit 「この【作品・アプリ・データベース等】は、以下の著作物を改変して利用しています。【タイトル】、東京都・【その他の著作権者】、クリエイティブ・コモンズ・ライセンス 表示4.0国際（link）」
  and **never presenting the result as made by Tokyo or a municipality**.
  Tokyo's own catalogue notice (`pipeline/tokyo/credits.py`, the "catalogue"
  form: title, publisher, the entry's URL, the catalogue's name, the date of
  use, CC BY 4.0, 加工して作成) is the built precedent; confirm the wording
  against staging's record.
- **The host site's own policy** (保健医療局) bars reuse and links below its
  top page: **the page links the two catalogue entries, never the 保健医療局 page
  or files.** `fetch_sources.py` downloads from that host (an automated GET,
  not a link); the provenance file may name the file URLs, the rendered page
  may not.
- **MHLW open data** (only if open call 1 is taken): PDL 1.0 as recorded in
  `docs/data_sources/japan.md`, its 出典 line and who processed it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **The yearbook and the census**:
  measurement sources, not drawn. **The operators' timetables**: read for
  counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here. A new row in
  `docs/data_sources/japan.md` for the Tama ledgers at build.

## Privacy

- **Dropped at read (call 109)**: 法人代表者氏名, 営業者住所 and 営業者ビル名 (the
  operator's own address), and every phone column (営業所電話番号, 営業者電話番号,
  施設TEL, 営業者TEL). Only 屋号 / 施設名称, the premises address and the type
  are ever selected; 営業者氏名 is read IN MEMORY for the name rule and never
  written.
- **The operator column, measured** (counts only): food permits 603, 営業者氏名
  filled on 295 (a company marker on 287, none on 8), **blank on 308**;
  notifications 269, filled 173 (167 / 6), blank 96; barbers 44, filled 6 (all
  companies), blank 38; beauty 86, filled 26 (all companies), blank 60;
  laundry 19, filled 13 (all companies), blank 6. The operator is published
  almost only for companies: the blanks are the shape of individuals withheld
  at source.
- **The name rule, version 2, measured in memory**: the sign rule 0, the
  operator comparison 0, **0 rows withheld** in any ledger, with or without
  法人代表者氏名.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; if open call 1
  brings its rows in, its 法人名 joins the name rule (owner, 2026-10-05).
- Run `check_personal_exposure.py higashiyamato` (`japan=True`) after step 2:
  it must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.392-139.452 E, centroid 139.427:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded out:
(35.72, 139.39, 35.78, 139.46). Scaffold with `scripts/scaffold_city.py ...
--page-number <N>`, the number claimed at build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band A with the
skew disclosed and the three columns dropped at read (call 109); the catalogue
route and its credit (call 108); the notifications in as partial Retail (call
127b); the Haijima Line drawn as cut from 東大和市 (standing call, a private
stub); the minor tier and Japan East (Kanto after the retag); no frequency
floor.

**Answered by the owner on 2026-10-06:** call 169, **MHLW's rows the ledgers lack added** for all four Tama cities (Tokyo wards' precedent of 2026-09-24: the ledger's row kept where both hold a premises, `SUPERSEDES`; MHLW's PDL 1.0 notice line added; the share the page states stays without MHLW's rows); call 170, **`mode` is `metro`**. The recommendations below are kept as the record.

**Weighed, with a recommendation:**

1. **MHLW's rows the ledgers lack** (12 open permits, 67 open notifications
   here; 45 of them would be Retail). Two precedents point opposite ways:
   Tokyo's wards (2026-09-24: MHLW's slice added to the partial ward lists,
   the ward's row kept where both hold a premises, `SUPERSEDES`) and
   Ichinomiya's call 127 (MHLW's extra permits left out beside a full city
   list). *Recommend Tokyo's*, for all four Tama cities alike: the ledgers are
   partial like Chūō's and Kōtō's, and MHLW's rows are the same health
   centres' own electronic filings, each with its own point (median 50 m from
   the block point). The share the page states stays WITHOUT MHLW's rows
   (Tokyo's rule). Tradeoff: a second source, its PDL notice line and a
   de-duplication pass, for about 6 restaurants and 50 shops here.
2. **`mode`**: `metro` recommended. No built page has a monorail as its main
   line (3 of 4 groups); Kitakyushu's monorail-and-JR map reads `metro`, and
   the owner's rule (2026-10-02) reads private heavy rail as `metro`. No tram
   or light rail. Tradeoff: none measurable; the macro map's mode key only.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): the `自動車以外` lookahead in `permits_from_rows`' vehicle test and
  in `japan_eigyo`'s temporary or mobile rule (26 rows here, 1,063 across the
  Tama ledgers). Nothing else: the columns are all known.
- The read: drop 法人代表者氏名, 営業者住所, 営業者ビル名 and the phones before
  `city_rows` hands rows on; `SOURCE_KIND` per register file (no type column
  in the barber and beauty ledgers); the city cut by address; `SOURCE_LINKS`
  for the slugs; `SOURCE_AS_OF` 2026-08-31 from the page.
- `ISJ_DIR` holding only 13220's pair; the share and its control-date figure
  from `official_shares` (the yearbook's 528), and the page's disclosure
  sentence from the approved template (call 109); the census ratio (1.70).
- The Haijima Line's label on its short stretch; gate 3; OSM `name:en`; line
  colors on both basemaps; the opening view (`map-view`); the factory share;
  `check_provenance.py`; `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "higashiyamato-ledger-page",
    "claim": "The Tama ledgers page names the five ledgers, their windows, the opt-out and closure rule, and Higashiyamato under 多摩立川保健所",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["平成29年1月から令和8年8月までの新規許可施設", "令和3年6月から令和8年8月までの届出施設", "公表を希望しない施設", "多摩立川保健所", "東大和市", "shokuhin-kyoka-7", "shokuhin-todokede-1-7", "kankyo-riyoujo-5", "kankyo-biyoujo-5", "kankyo-cleaning-5"]
  },
  {
    "id": "higashiyamato-ledger-edition",
    "claim": "The edition measured here: the ledgers as of 2026-08-31 (a failure here means a new monthly edition: re-measure)",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["令和8年8月31日現在"]
  },
  {
    "id": "higashiyamato-food-permits-file",
    "claim": "The food permit ledger (4,486,267 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-kyoka-7",
    "min_bytes": 2000000
  },
  {
    "id": "higashiyamato-food-notifications-file",
    "claim": "The food notification ledger (1,956,304 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-todokede-1-7",
    "min_bytes": 1500000
  },
  {
    "id": "higashiyamato-barber-file",
    "claim": "The barber ledger (165,277 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-riyoujo-5",
    "min_bytes": 100000
  },
  {
    "id": "higashiyamato-beauty-file",
    "claim": "The beauty-salon ledger (608,582 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-biyoujo-5",
    "min_bytes": 400000
  },
  {
    "id": "higashiyamato-laundry-file",
    "claim": "The laundry ledger (173,591 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-cleaning-5",
    "min_bytes": 100000
  },
  {
    "id": "higashiyamato-catalogue-food",
    "claim": "Tokyo's catalogue entry t000055d0000000361 (食品関係営業台帳) declares CC BY 4.0 and points at the 保健医療局 ledger page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000361",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "higashiyamato-catalogue-registers",
    "claim": "Tokyo's catalogue entry t000055d0000000614 (環境衛生施設台帳) declares CC BY 4.0 and points at the same page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000614",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "higashiyamato-tokyo-terms",
    "claim": "The Tokyo Open Data Terms allow commercial use and prescribe a modified-use credit",
    "kind": "http_contains",
    "url": "https://portal.data.metro.tokyo.lg.jp/terms/",
    "present": ["商用利用も可能", "改変して利用", "編集・加工等を行った旨"]
  },
  {
    "id": "higashiyamato-mhlw-tokyo",
    "claim": "MHLW's Tokyo Prefecture file (13000, 3,606,399 B) answers a plain keyless GET (a control; the 13220 file answers 404)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "higashiyamato-isj-block-live",
    "claim": "MLIT's block-level address file for Higashiyamato (13220) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13220-24.0a.zip",
    "min_bytes": 30000
  },
  {
    "id": "higashiyamato-isj-chome-live",
    "claim": "MLIT's town-chōme file for Higashiyamato (13220) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/13220-19.0b.zip",
    "min_bytes": 4000
  },
  {
    "id": "higashiyamato-seibu-timetable",
    "claim": "Seibu's weekday timetable for 東大和市 (station 234-9, toward 萩山・小平・西武新宿) is live and lists each train",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/234-9/d1?dw=0",
    "present": ["東大和市の時刻表", "openOneTrainTimetable"]
  },
  {
    "id": "higashiyamato-monorail-timetable-page",
    "claim": "The monorail's 上北台 timetable page links its station PDF TT19 (ASCII anchors: the host sends no charset)",
    "kind": "http_contains",
    "url": "https://www.tama-monorail.co.jp/monorail/station/kamikitadai/timetable.html",
    "present": ["station/TT19.pdf"]
  },
  {
    "id": "higashiyamato-monorail-timetable-pdf",
    "claim": "The monorail's 桜街道 timetable PDF (TT18) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.tama-monorail.co.jp/monorail/station/TT18.pdf",
    "min_bytes": 200000
  },
  {
    "id": "higashiyamato-projected-crs",
    "claim": "Higashiyamato projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.43,
    "expect": "EPSG:32654"
  }
]
```
