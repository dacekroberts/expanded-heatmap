# Tachikawa — build brief

**Band B, owner-approved 2026-10-06** (Japan wave 4, measured from cached
files and moved from C to B by the owner, call 187: "187 and 188: B sounds
good"; `docs/decisions_drafts/staging.md`, "The last four Tama cities"): **all
three buckets, with the food share stated at the yearbook's date** (63.6%;
Kure's 58.5% of the in-force count is the precedent). The ledgers were
approved and fetched for the Tama measurement (wave 5), MLIT's address blocks
for the block join (call 106), MHLW's file as a control and call 169's extra
rows (calls 106, 141, 147, 169). **Step 0 measured 2026-10-06** (staging), each
file from its publisher's own host with the project user-agent, each HTTP 200:

- **Already cached** in `data/tokyo_tama/raw/` (gitignored; one copy for every
  Tama city), from `www.hokeniryo.metro.tokyo.lg.jp` (東京都保健医療局, the
  Tokyo Metropolitan Government's health centres for Tama), as of
  **2026-08-31**: `shokuhin-kyoka-7.csv` (**4,486,267 B**, food permits),
  `shokuhin-todokede-1-7.csv` (**1,956,304 B**, food notifications),
  `kankyo-riyoujo-5.csv` (**165,277 B**, barbers), `kankyo-biyoujo-5.csv`
  (**608,582 B**, beauty salons), `kankyo-cleaning-5.csv` (**173,591 B**,
  laundries); from `i2fas.mhlw.go.jp`, `13000_food_business_all.csv`, **Tokyo
  Prefecture's file** (**3,606,399 B**). Not copied: the build's
  `fetch_sources.py` places them in `data/tachikawa/raw/`.
- **Downloaded for this brief** (the only download approved), from
  `nlftp.mlit.go.jp` by `japan_fetch.get` into `data/tachikawa/raw/isj/`:
  `13202-24.0a.zip` (**84,737 B**) and `13202-19.0b.zip` (**5,802 B**).
  **90,539 B in all.**
- Read, not kept as data: the operators' timetable pages (counts only), and
  Tokyo's statistical-yearbook chapter page (`tn24q3i019.htm`, a page read for
  the beauty question below; no table downloaded).

**Run `python scripts/brief_check.py tachikawa` before writing any code.**
Then the `japan-city` skill, **Higashiyamato's shape**
(`docs/build_briefs/higashiyamato.md`: the same five ledgers cut by address,
MHLW's Tokyo file beside them), with `tama.md`, `nishitokyo.md` and
`higashimurayama.md` on the same files. Read the `tokyo-ward` skill for
Tokyo's catalogue sources and credits. Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py`'s own functions from a
scratch script (`scripts/screen_japan_join.py` has no entry; its table is
shared code and was not edited). Rail: MLIT N02-25 cut at the N03 city line,
through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left
out, its station kept through the other lines, and drawn cut only where no
other line serves that station (owner, 2026-10-06, calls 54, 92, 163, 165,
167); (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory share
measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor for
JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at about
11 trains a day or fewer **named and drawn** (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Band B, the food share stated at the yearbook's date (owner, call 187):**
the page states **63.6%** (1,652 restaurant permits first granted by
2025-03-31, of the yearbook's 2,599), never the raw 85.0%. The ledgers' skew
is disclosed as for the four Tama cities in A (call 109): about a quarter of
the rows opened after the control date, the ledger misses long-standing
premises (new permits only from 2019-08), laundry about half, opt-outs and
closures left out. **法人代表者氏名, the operator's address and the phones are
dropped at read** (call 109).

**✅ The licence (owner, call 108): the catalogue route, relied on** (Taitō's
precedent). The page links the Tokyo catalogue entries `t000055d0000000361`
and `t000055d0000000614`, **never the 保健医療局 page or files** (that site's
link policy). Below, "Licences".

**✅ The notification ledger in Retail** (decided for the four Tama cities in
A; Ichinomiya's call 127b), disclosed as partial. **✅ MHLW's rows the ledgers
lack are added** (owner, call 169, for all Tama cities: the Tokyo wards'
precedent, the ledger's row kept where both hold a premises, `SUPERSEDES`;
MHLW's PDL 1.0 notice line; the stated share stays WITHOUT MHLW's rows). The
2024 snapshot stays a cross-check only (call 147).

**✅ `mode`: `metro`** (Higashiyamato's call 170: a monorail-led map with JR
and private heavy rail reads `metro`; 7 of 12 groups here are the monorail's).
**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
`label_tier: "minor"`, `"region": "Japan East"` (`app/cities.py`); wave 4's
first city to land retags Japan into the eight regions, Tachikawa into
**Kanto**. Its dot sits among the other Tama cities: the label offset from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

---

## The one-line summary

**All three buckets from the Tokyo Metropolitan Government's monthly Tama
ledgers (CC BY 4.0 through the catalogue route, relied on, call 108), cut to
Tachikawa by address, as of 2026-08-31: 2,549 food permits (2,208
restaurants), 933 food notifications, 89 barbers, 501 beauty salons and 63
laundries.** The restaurants are **85.0% of the 2,599 in force** (Tokyo's
statistical yearbook, table 19-8, FY2024), flattered: **556 (25.2%) were first
permitted after the control date**, so the share the page states is **63.6%**
(call 187). Barbers about 89% and laundry counters about 59% of census-scaled
estimates; **beauty is stated as a count, 501, with no share** (the census
estimate of 297 cannot hold it, and the yearbook's own count, table 19-7, is
not in hand: open call 1). Through `japan_eigyo`: **Food service 1,816 rows
(1,790 pins), Retail 333 permit rows (276 pins) plus 689 notification rows**
(783 once the shared `自動車以外` trap is fixed), **Personal services 650**;
MHLW adds **27 Food-service and 82 Retail rows** (call 169). **Block join
97.1%** of 3,488 bucketed rows, none unplaced. **Rail: 12 N02 station
groups**: the Tama Toshi Monorail 7 (120-128 weekday departures each way), JR
立川 (Chūō, Ōme and Nambu, one group), JR Nambu 西国立, Seibu Haijima 3; every
line READ from its operator's timetable; nothing at or under 11 trains a day.

---

## Business leg — the Tokyo Metropolitan Government's Tama ledgers

Page `https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho`
(東京都が設置している保健所等で保有する台帳一覧, 更新日 2026-09-14; UTF-8).
**Tachikawa is 多摩立川保健所's** (立川市, 昭島市, 国分寺市, 国立市, 東大和市,
武蔵村山市). The page: 「ホームページへの公表を希望しない施設、廃止・休止している施設は除いて公表しています」
and, for food,
「移動販売、臨時販売、自動車販売、自動販売機、行商、催事等期間短縮申請があったもの、届出が不要な施設及び廃業した施設は除いています」.

| Ledger (CSV, cp932) | Edition line on the page | Rows (all areas) | Rows in Tachikawa |
|---|---|---|---|
| `shokuhin-kyoka-7` 食品関係営業台帳（許可） | 「平成29年1月から令和8年8月までの新規許可施設及び平成29年4月から令和8年8月までの許可更新施設（令和8年8月31日現在）」 | 28,093 | **2,549** |
| `shokuhin-todokede-1-7` 食品関係営業台帳（届出） | 「令和3年6月から令和8年8月までの届出施設（令和8年8月31日現在）」 | 12,502 | **933** |
| `kankyo-riyoujo-5` 理容所台帳 | 「令和8年8月31日現在、台帳に掲載されている施設」 | 1,427 | **89** |
| `kankyo-biyoujo-5` 美容所台帳 | as above | 4,319 | **501** |
| `kankyo-cleaning-5` クリーニング所台帳 | as above | 1,040 | **63** |

Files at `https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/<name>`.
⚠️ **The slugs carry a revision suffix** (`-7`, `-1-7`, `-5`) that may move
with a monthly edition: `fetch_sources.py` takes them from the page's links (a
`SOURCE_LINKS` regex) and pins `SOURCE_AS_OF` to 「令和8年8月31日現在」, never the
fetch date.

- **Assigning a row to the city**: the address starts 東京都立川市 (every row
  of the city's has an address). `permits_from_rows(rows, "東京都", "立川市",
  wardless=True)`.
- **Columns, and the shared tuples**: as Higashiyamato's brief lists them
  (permits: 屋号, 営業所所在地, 営業者氏名, 営業者住所, 営業の種類, 申請区分,
  営業所電話番号, 初回許可日, 営業者電話番号, 法人代表者氏名; notifications add
  届出年月日 and drop 申請区分 and 初回許可日; registers: 確認番号, 施設名称, 施設TEL,
  施設所在地, 施設ビル名, 営業者氏名, 法人代表者氏名, 営業者住所, 営業者ビル名, 営業者TEL,
  確認年月日, and 営業形態 for laundry). **No shared-code change for the columns**;
  ⚠️ `OPERATOR_COLS` holds 法人代表者氏名, so the read drops it before the name
  rule (measured cost: 0 rows). No 業態 column: the bracketed sub-type carries
  the form, and `japan_eigyo` reads it.

### The food permit ledger (2,549 rows)

- **申請区分**: 新規 2,359, 更新 190. **Kinds**: 飲食店営業 2,208, 菓子製造業 148,
  食肉販売業 48, そうざい製造業 40 (+ 複合型 3), 魚介類販売業 40, 食肉処理業 14,
  アイスクリーム類 7, 麺類 7, 小分け 6, 喫茶店営業 4, … Restaurant sub-types:
  一般飲食店 1,640, **バー・キャバレー 195**, 集団給食 103, 弁当屋 63, そうざい店 53,
  すし屋 39, そば屋 35, 旅館・ホテル 27, 喫茶店 27, 仕出し屋 17, 簡易な営業 8,
  コンビニエンスストア等 1.
- **Against the yearbook** (table 19-8, FY2024, 立川市; `japan_official`):
  **飲食店営業 2,208 of 2,599, 85.0%**. 菓子 148 of 198, 食肉販売 48 of 114, 魚介類販売
  40 of 87, そうざい製造 43 of 47, 麺類 7 of 8, 豆腐 3 of 3.
- **The dates (the skew)**: restaurant 新規 rows were first permitted
  **2019-08-02 to 2026-08-28**; 更新 rows carry first permits from 1966-12 to
  2015-05. By first-permit year: 235 rows before 2021, then 304, 345, 412, 286
  (2021-2024), 354 in 2025 and 272 to 2026-08. **556 restaurant rows (25.2%)
  were first permitted after 2025-03-31**, so at the yearbook's control date
  the ledger holds **1,652, 63.6%** of the 2,599: **the share the page states**
  (call 187). Premises permitted before 2019-08 and not renewed since 2017-04
  are missing (Tama's brief reads the ledger-wide windows).
- **Old-law permits are in the ledger** (not Kurashiki's trap): 喫茶店営業 4
  rows and 更新 rows first permitted 1966-2015.
- **Duplicates**: 49 exact repeats of (address, trade name, kind); 268 rows
  repeat an (address, trade name) under another kind; **2,281 distinct
  premises**. One pin per premises and bucket (trap 7). No blank 屋号.
- **Closures are left out at source**; the page keeps "may include closed
  premises".

### The food notification ledger (933 rows)

- 届出年月日 1982-03-18 to 2026-08-31 (61 before 2021, 365 in 2021, then 90 to
  118 a year); types: その他の食料・飲料販売業 427 (店舗 247, 電子申請 125, 包装 55),
  コンビニエンスストア 109, 集団給食施設 74, 弁当販売業(自動車以外) 54, 百貨店、総合スーパー
  44, 乳類販売業 42, 野菜果物販売業(自動車以外) 40, packaged meat 35 and fish 22,
  コーヒー製造 23, …
- **Against the yearbook's columns**: コンビニエンスストア **109 of 106**,
  百貨店・総合スーパー **44 of 47**, 野菜果物販売業 40 of 49, 弁当販売業 54 of 51,
  米穀類 10 of 15, 集団給食施設 74 of 81, 乳類販売業 **42 of 163** (old-law dairy
  permits never re-filed). Near complete for the shops a reader sees, partial
  for dairy: disclosed as partial.
- ⚠️ **The `自動車以外` trap (shared code)**: 弁当販売業(自動車以外) 54 and
  野菜果物販売業(自動車以外) 40 ("other than a vehicle") are read as **mobile** by
  `permits_from_rows` (a bare `自動車` test) and by `japan_eigyo`. Measured
  here: **94 rows**, all Retail once fixed (76 block, 16 chōme, 2 unplaced).
  The fix is Higashiyamato's (`自動車(?!以外)` in both tests, then the Minato
  control and every city screen).

### Counts through `japan_eigyo` (fixed premises, today's shared code)

**Food service 1,816** (一般飲食店 1,640, 弁当屋 63, すし屋 39, そば屋 35, 喫茶店 27,
簡易 8, 喫茶店営業 4; **1,790 pins**). **Retail from the permits 333** (菓子 148,
そうざい店 53, 食肉 48, そうざい製造 43, 魚介 40, コンビニエンスストア等 1; **276 pins**).
**Retail from the notifications 689** (581 pins; **783 rows after the
`自動車以外` fix**). Left out: **hostess venues 195** (バー・キャバレー,
`docs/category_rules.md` R3), institutional catering 103 + 74, inside
accommodation 27, event catering 17, not a premises 95 (the 94 above and one
無店舗取次店), and 58 + 76 types with no rule (食肉処理, アイスクリーム, 麺類,
小分け, コーヒー製造, 調味料, …), as in every built city.

**Economic Census control** (`scripts/japan_census_control.py` at build): the
2021 census counts **854** 飲食店 establishments in 13202
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 1,790 distinct placed
Food-service premises is **2.10 per establishment**, above the built cities'
1.56-1.92 (Tama's 1.96 too), although the ledger misses premises: a quarter of
the rows opened after 2021, and the large lots north and south of 立川 station
(緑町's and 泉町's commercial complexes) permit each counter separately.
Record the figure and the reading.

### Personal services: the three registers

| Register | Rows | Census 2021 | Estimate (census x Hachiōji's licensed-to-census ratio) | Share |
|---|---|---|---|---|
| 理容所台帳 (barbers) | **89** | 89 | 100 | **89%** (84% on all Tokyo's ratio) |
| 美容所台帳 (beauty) | **501** | 189 | 297 | **no share: a count** (169%; 125% on Tokyo's ratio) |
| クリーニング所台帳 (laundry) | **63** (取次所 39, 一般 21, リネン 2, 無店舗取次店 1); 60 bucketed | 60 | 105 | **59%** (65%) |

No official per-city count is in hand for a Tama city (e-Stat's 衛生行政報告例
lists Hachiōji alone), so barbers and laundry are estimates (the band row's
figures, reproduced). 確認年月日 run from 1948 (barbers), 1972 (beauty) and
1966 (laundry) to 2026: **standing registers**, not a stream. 21 addresses
carry both a barber and a beauty salon.

**Beauty salons: the count, and why there is no share.** The register holds
**501** salons in Tachikawa (2 repeat an address and name). Scaled from the
census (189 美容業 establishments) by Hachiōji's ratio the estimate is 297; on
all Tokyo's ratio, 402: **the estimate cannot hold the register**, so a share
from it would read 169%. The register's own shape, measured (counts only):
**375 distinct addresses; 83 addresses hold two or more salons (209 rows),
the most at one address 9**; **259 of the 501 (52%) were confirmed since 2020**
(114 in 2015-2019, 128 before 2015); and they cluster around 立川 station
(柴崎町三丁目 86, 錦町一丁目 70, 曙町二丁目 66, 柴崎町二丁目 60, 錦町二丁目 49). The
register's ratio to the census is **2.65 here, against 1.23-1.64 in the four
other Tama cities measured with it**. The reading (not a measurement): many
small salon units in station-area buildings, each licensed as its own 美容所
and mostly opened since the census, which counts establishments, not
licences. **The yearbook does carry a per-municipality table**: Tokyo's
statistical yearbook chapter 19 lists **19-7 環境衛生営業施設数**
(`/tnenkan/2024/tn24qv190700.csv`, 6.7 KB, the same size and publisher as
19-8's per-municipality CSV already cached), very likely holding 美容所 per
municipality at FY2024 end. **It was not downloaded** (not named in the
approval): open call 1. Until then the page states beauty as a count, 501,
with no share, and says why.

### MHLW's Tokyo file (13000): the control, and call 169's rows

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv`
(**3,606,399 B, 10,003 rows**, UTF-8 with BOM). ⚠️ **市区町村名 reads 新宿区 on
every row** (Higashiyamato's finding): the build filters by 営業施設所在地,
never by 市区町村名. The city-code file (`13202_food_business_all.csv`) answers
**HTTP 404** (brief check below).

- **532 rows in Tachikawa** (届出 405, 許可 125, 届出(廃業) 2), dated 2021-08 to
  2026-08, every one with its own point. Open restaurant permits 110.
- **Against the ledgers** (Higashiyamato's match: parsed town, number and
  trade name; notifications on town and number): of 125 open permits, 87 are
  in a ledger by (town, number, trade name), 101 by (town, number). Of 405 open
  notifications, 284 are in a ledger by (town, number).
- **The rows the ledgers lack, by bucket (call 169)**: permits **Food service
  27, Retail 8**, out 3; notifications **Retail 74**, out 46 (vending,
  catering, manufacturing), not a premises 1. **109 rows bucketed**; their own
  point against the block point: **median 27 m, 96.0% within 250 m** (101
  rows). The build keeps the ledger's row where both hold a premises
  (`SUPERSEDES`), takes MHLW's own point where the join misses (call 127c),
  and leaves them out of the stated share.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13202-24.0a.zip` (84,737 B,
**3,393 block keys**), town-chōme `.../19.0b/13202-19.0b.zip` (5,802 B,
**79**), in `data/tachikawa/raw/isj/` and nothing else there (`load_city_isj`
globs its directory: one ISJ directory per city). `japan.CITIES` entry at
build: `"tachikawa": {"name": "立川市", "pref": "13", "epsg": 32654, "n02":
"25", "rules": WAVE2_RULES, "wardless": True, "wards": ["13202"]}`.

| Tier, today's shared code | Rows | Block | Town-chōme | Unplaced |
|---|---|---|---|---|
| **Permits and registers** | 2,799 | **97.8%** | 2.2% | 0 |
| … Food service / Retail (permits) | 1,816 / 333 | 97.2% / 97.6% | 2.8 / 2.4 | 0 |
| … Barbers / beauty / laundry | 89 / 501 / 60 | 98.9% / 99.8% / 98.3% | 1.1 / 0.2 / 1.7 | 0 |
| Notifications, Retail | 689 | 94.2% | 5.8% | 0 |
| **All, with the notifications** | 3,488 | **97.1%** | 2.9% | **0** |
| All after the `自動車以外` fix | 3,582 | 96.7% | 3.3% | 2 |
| MHLW's extra rows (call 169) | 109 | 92.7% | 4.6% | 3 (own point) |

**The misses, read** (towns only): **緑町 82 of the 101 chōme-tier rows**, the
地番 addresses (`N番地のN`) of the large lots north of 立川 station, whose
commercial complexes (GREEN SPRINGS, 立川ステージガーデン) hold many counters at
one number MLIT's block file does not have; 泉町 10 (アリーナ立川立飛 among them,
the same shape); 曙町2丁目 5 (four written 「付近」, near); 錦町3丁目
2, 柴崎町6丁目 1, 一番町4丁目 1. Each takes its town's centroid; no rule is
proposed (a complex's counters share one point either way).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_13_GML.zip`, N03 code 13202
(**24.35 km²**, extent W 139.352, S 35.683, E 139.446, N 35.745; centroid
139.405, 35.714). Read with `stub_test()`'s method and an in-memory `CITIES`
entry (scratch `rail.py`).

| N02 line (operator, N02_002 class) | Public name | Stations inside / on the line | Stations inside |
|---|---|---|---|
| 多摩都市モノレール線 (多摩都市モノレール, 5) | Tama Toshi Monorail | **7 / 19** | 砂川七番, 泉体育館, 立飛, 高松, 立川北, 立川南, 柴崎体育館 |
| 中央線 (JR East, 2) | JR Chūō Line | **1 / 75** | 立川 |
| 青梅線 (JR East, 2) | JR Ōme Line | **1 / 26** | 立川 |
| 南武線 (JR East, 2) | JR Nambu Line | **2 / 30** | 立川, 西国立 |
| 拝島線 (西武鉄道, 4) | Seibu Haijima Line | **3 / 8** | 玉川上水, 武蔵砂川, 西武立川 |

- **16 station records, 12 N02_005g groups**: JR's 立川 is ONE group across the
  Chūō, Ōme and Nambu platforms (84 m spread). No Shinkansen.
- **Close pairs, kept apart (precedent, no owner question)**: 立川北 / 立川 217 m,
  立川 / 立川南 231 m, 立川北 / 立川南 372 m. Three names, three N02 groups;
  `GROUP_JOIN` joins only platforms of one name, and the built cities keep
  differently named neighbours apart (Tama's brief: Kyoto's Yamashina and
  Keihan-Yamashina, Osaka's Nippombashi pair). Rings by the spacing rule at
  build (median nearest-station gap **581 m**, 217 to 2,073); the build checks
  the three labels in a scratch render.
- **The one-station rule (calls 54, 92, 163, 165, 167), every line with one
  station in the city**: **the JR Chūō Line (立川, 1 of 75) and the JR Ōme Line
  (立川, 1 of 26) are JR stubs: drawn as cut, no owner question** (standing call
  3: a JR or private one-station stub stays as cut; Kobe's JR Takarazuka Line,
  Higashiyamato's Haijima Line). Neither is an urban line, so the urban-line
  rule does not reach them. The Ōme Line's stretch inside the city is short
  (西立川 is **36 m outside**, in 昭島市): measure its permanent label and legend
  entry in a scratch render. The monorail keeps 7 of 19, the Nambu Line 2, the
  Haijima Line 3: not stubs.
- **Near the line, outside**: the monorail's own 玉川上水 is **16 m outside**
  (東大和市); Seibu's 玉川上水 platform, **32 m inside**, keeps the ring here
  (Higashiyamato's mirror image). 西立川 (Ōme) 36 m outside. None gets a ring
  here (standing call 3).
- **Cut at the line**: the monorail's 12 beyond (日野市 5, 八王子市 3, 東大和市 3,
  多摩市 1); the Chūō Line's 73 (国立市, 日野市, … to 東京 and 大月); the Ōme
  Line's 24 (昭島市 5, 青梅市 10, …); the Nambu Line's 28 (国立市 2, 府中市 3,
  稲城市 3, Kanagawa 20); the Haijima Line's 5 (東大和市 1, 小平市 2, 東村山市 1,
  昭島市 1).
- **The light-rail/rail test**: the monorail is N02 class 5, a straddle
  monorail on its own viaduct (rail, as the Maihama Resort Line, call 53); JR
  (class 2) and Seibu (class 4) are heavy rail. No tram.
- **Frequency, read 2026-10-06 from the operators' own timetables** by plain
  GET with the project user-agent; every departure on each page counted,
  marked ones included:

  | Station (line, direction) | Weekday departures | Per hour 07-18 |
  |---|---|---|
  | 立川 (JR Chūō, to 八王子・大月 / to 新宿・東京) | 227 / 299 | 10-19 / 14-25 |
  | 立川 (JR Ōme, to 拝島・青梅; the terminus) | 136 | 5-10 |
  | 立川 (JR Nambu, to 登戸・川崎; the terminus) | 136 | 6-10 |
  | 西国立 (JR Nambu, to 立川 / to 登戸・川崎) | 125 / 126 | 5-9 / 6-12 |
  | Monorail, each of the 7 stations, each way | 120-128 | 6-10 |
  | 玉川上水 (Seibu Haijima, to 西武新宿 / to 拝島) | 113 / 92 | 5-8 / 3-6 |
  | 武蔵砂川, 西武立川 (Seibu Haijima, each way) | 92-93 | 3-6 |

  JR East: `timetables.jreast.co.jp/2610/timetable/tt0958/0958010-040.html`
  (立川) and `tt1155/…` (西国立), the October 2026 edition, counted from each
  `timetable_time` cell. Monorail: the station PDFs `TT10`-`TT16` linked from
  each station's timetable page, read with `pdftotext`; their header carries
  the revision dates 2022-03-12 and 2023-03-20 (the band row's caveat); two
  PDFs' 10:00 rows run together in the text, so their 07-18 minimum is read
  from the others. Seibu: `seibu.ekitan.com/norikae/timetable/station/234-10`
  (玉川上水), `234-11` (武蔵砂川), `234-12` (西武立川), `/d1` and `/d2`, `?dw=0`,
  service date 2026-10-07, counted from each train's own entry (玉川上水 is a
  terminus for some trains toward 西武新宿). **No stretch is at or under about
  11 trains a day** (call 86). Counts only; no timetable on the page.
- ⚠️ **Gate 3** at build: the operators' station counts inside the city
  (monorail 7, JR 2 stations, Seibu 3). **OSM `name:en`** for 12 groups (one
  Overpass query at build; not queried here).

## Scope

**Tachikawa City.** The monorail runs on north to 上北台 and south over the
Tama River to 多摩センター; the Chūō Line to 東京 and 大月, the Ōme Line to 奥多摩,
the Nambu Line to 川崎, the Haijima Line to 西武新宿 and 拝島; all cut at the
line. Tachikawa is its own page (the band).

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
- **The Tokyo Open Data Terms** (`https://portal.data.metro.tokyo.lg.jp/terms/`)
  §2: CC BY 4.0, 「商用利用も可能です」; §2(1)イ, the modified-use credit (title,
  東京都, CC BY 4.0 linked, and that the work was modified), and **never
  presenting the result as made by Tokyo or a municipality**.
- **The host site's own policy** (保健医療局) bars reuse and links below its
  top page: **the page links the two catalogue entries, never the 保健医療局 page
  or files.** `fetch_sources.py` downloads from that host; the provenance file
  may name the file URLs, the rendered page may not.
- **MHLW open data** (call 169): PDL 1.0 as recorded in
  `docs/data_sources/japan.md`, its 出典 line and who processed it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **The yearbook and the census**:
  measurement sources, not drawn. **The operators' timetables**: read for
  counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **Dropped at read (call 109)**: 法人代表者氏名, 営業者住所 and 営業者ビル名, and
  every phone column. Only 屋号 / 施設名称, the premises address and the type are
  ever selected; 営業者氏名 is read IN MEMORY for the name rule and never
  written.
- **The operator column, measured** (counts only): food permits 2,549,
  営業者氏名 filled on 1,711 (a company marker on 1,701, none on 10), blank on
  838; notifications 933, filled 721 (707 / 14), blank 212; barbers 89, filled
  22, beauty 501, filled 263, laundry 63, filled 38 (all companies). The
  operator is published almost only for companies.
- **The name rule, version 2, measured in memory**: **2 rows withheld** (food
  permits 1, by the sign rule; notifications 1, by the operator comparison),
  the same with or without 法人代表者氏名 (dropping it costs 0). The registers
  withhold none.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; its 法人名 joins
  the name rule for the rows call 169 brings in (owner, 2026-10-05).
- Run `check_personal_exposure.py tachikawa` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.352-139.446 E, centroid 139.405:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded out:
(35.68, 139.35, 35.75, 139.45). Scaffold with `scripts/scaffold_city.py ...
--page-number <N>`, the number claimed at build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band B with the
food share stated at the yearbook's date (call 187); the skew disclosed and the
three columns dropped at read (call 109); the catalogue route and its credit
(call 108); the notifications in Retail as partial (127b, decided for the Tama
cities); MHLW's rows the ledgers lack added (call 169); the 2024 snapshot a
cross-check only (call 147); `mode: metro` (call 170's precedent); the minor
tier and Japan East (Kanto after the retag); no frequency floor.

**Answered by the owner on 2026-10-06:** calls 187 and 188 ("187 and 188: B
sounds good"): Fuchū, Tachikawa, Hino and Chōfu go to **Band B, all three
buckets, with the food share stated at the yearbook's date**; Tachikawa's is
**63.6%** (raw 85.0%); Kure's 58.5% of the in-force count is the precedent.
Not to be re-opened.

**Decided by precedent here (no owner question):** the Chūō and Ōme Lines
drawn as cut from 立川 (JR one-station stubs, standing call 3); 立川北, 立川 and
立川南 kept as three stations (Tama's 38 m pairs precedent).

**Answered by the owner on 2026-10-06:** call 189, table 19-7 fetched and measured (section "Personal services against Tokyo's yearbook table 19-7" above). The recommendation below is kept as the record.

**Weighed, with a recommendation:**

1. **Fetch Tokyo's yearbook table 19-7 (環境衛生営業施設数) for the beauty share.**
   `https://www.toukei.metro.tokyo.lg.jp/tnenkan/2024/tn24qv190700.csv`
   (6.7 KB), the same publisher and terms as table 19-8, which the project
   already reads. *Recommend yes*, at the build or by staging now, for every
   Tama city: if it holds 美容所 (and 理容所, クリーニング所) per municipality, as
   19-8 holds food, the page states **501 against the yearbook's own count**,
   and the barber and laundry shares become official rather than
   census-scaled. Tradeoff: one more measurement-only file and a re-statement
   of the A-band Tama cities' personal-services shares; without it, Tachikawa's
   page states beauty as a count, 501, with no share, and says the census
   estimate cannot hold it (the default wording if the owner declines).

## Personal services against Tokyo's yearbook table 19-7 (owner, call 189)

**Answered by the owner on 2026-10-06:** call 189, "fetch at once": Tokyo's statistical yearbook table 19-7 (環境衛生営業施設数, `https://www.toukei.metro.tokyo.lg.jp/tnenkan/2024/tn24qv190700.csv`, 6,876 B, HTTP 200, into `data/tokyo/raw/`; the publisher of table 19-8) gives the official count of each register at the end of FY2024 (2025-03-31). **It supersedes the census-scaled estimates above** for these three registers; the estimates are kept as the record.

| Register | Ledger rows (2026-08-31) | Confirmed on or before 2025-03-31 (確認年月日) | Yearbook FY2024 | Share, all rows | Share at the yearbook's date |
|---|---|---|---|---|---|
| Barbers (理容所) | 89 | 81 | 91 | 97.8% | **89.0%** |
| Beauty salons (美容所) | 501 | 448 | 504 | 99.4% | **88.9%** |
| Laundries (クリーニング所, storeless counters out) | 62 | 60 | 72 | 86.1% | **83.3%** |

The share at the yearbook's date is the one the page states, as the food share is (calls 187-188); it is a lower bound, since 確認年月日 is the confirmation date, which a change of operator renews. Measured by staging's scratch script `t197_measure.py` (counts only; operator, address and phone columns dropped at read); the build re-measures it in step 2.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): the `自動車以外` lookahead in `permits_from_rows`' vehicle test and
  in `japan_eigyo`'s temporary or mobile rule (94 rows here). Nothing else: the
  columns are all known.
- The read: drop 法人代表者氏名, 営業者住所, 営業者ビル名 and the phones before
  `city_rows` hands rows on; `SOURCE_KIND` per register file; the city cut by
  address; `SOURCE_LINKS` for the slugs; `SOURCE_AS_OF` 2026-08-31 from the
  page.
- MHLW's rows (call 169): the `SUPERSEDES` match, MHLW's own point where the
  join misses, its 法人名 in the name rule, its notice line; the stated share
  without them.
- `ISJ_DIR` holding only 13202's pair; the share and its control-date figure
  from `official_shares` (the yearbook's 2,599: **63.6% stated**, measured,
  never typed); the beauty sentence (count, or count against 19-7 if call 1 is
  taken); the census ratio (2.10) and its reading.
- The Ōme and Chūō Lines' labels on their short in-city stretches; the three
  立川 labels; gate 3; OSM `name:en`; line colors on both basemaps; the opening
  view (`map-view`); the factory share; `check_provenance.py`;
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "tachikawa-ledger-page",
    "claim": "The Tama ledgers page names the five ledgers, their windows, the opt-out rule, and Tachikawa under 多摩立川保健所",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["平成29年1月から令和8年8月までの新規許可施設", "令和3年6月から令和8年8月までの届出施設", "公表を希望しない施設", "多摩立川保健所（立川市", "shokuhin-kyoka-7", "shokuhin-todokede-1-7", "kankyo-riyoujo-5", "kankyo-biyoujo-5", "kankyo-cleaning-5"]
  },
  {
    "id": "tachikawa-ledger-edition",
    "claim": "The edition measured here: the ledgers as of 2026-08-31 (a failure means a new monthly edition: re-measure)",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["令和8年8月31日現在"]
  },
  {
    "id": "tachikawa-food-permits-file",
    "claim": "The food permit ledger (4,486,267 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-kyoka-7",
    "min_bytes": 2000000
  },
  {
    "id": "tachikawa-food-notifications-file",
    "claim": "The food notification ledger (1,956,304 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-todokede-1-7",
    "min_bytes": 1500000
  },
  {
    "id": "tachikawa-barber-file",
    "claim": "The barber ledger (165,277 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-riyoujo-5",
    "min_bytes": 100000
  },
  {
    "id": "tachikawa-beauty-file",
    "claim": "The beauty-salon ledger (608,582 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-biyoujo-5",
    "min_bytes": 400000
  },
  {
    "id": "tachikawa-laundry-file",
    "claim": "The laundry ledger (173,591 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-cleaning-5",
    "min_bytes": 100000
  },
  {
    "id": "tachikawa-catalogue-food",
    "claim": "Tokyo's catalogue entry t000055d0000000361 (食品関係営業台帳) declares CC BY 4.0 and points at the 保健医療局 ledger page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000361",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "tachikawa-catalogue-registers",
    "claim": "Tokyo's catalogue entry t000055d0000000614 (環境衛生施設台帳) declares CC BY 4.0 and points at the same page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000614",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "tachikawa-tokyo-terms",
    "claim": "The Tokyo Open Data Terms allow commercial use and prescribe a modified-use credit",
    "kind": "http_contains",
    "url": "https://portal.data.metro.tokyo.lg.jp/terms/",
    "present": ["商用利用も可能", "改変して利用", "編集・加工等を行った旨"]
  },
  {
    "id": "tachikawa-mhlw-tokyo",
    "claim": "MHLW's Tokyo Prefecture file (13000, 3,606,399 B) answers a plain keyless GET: the control and call 169's rows",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "tachikawa-no-mhlw-city-file",
    "claim": "MHLW has no per-city file for 13202 (HTTP 404): the prefecture licenses Tachikawa",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13202_food_business_all.csv",
    "expect_status": 404
  },
  {
    "id": "tachikawa-isj-block-live",
    "claim": "MLIT's block-level address file for Tachikawa (13202, 84,737 B) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13202-24.0a.zip",
    "min_bytes": 60000
  },
  {
    "id": "tachikawa-isj-chome-live",
    "claim": "MLIT's town-chōme file for Tachikawa (13202) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/13202-19.0b.zip",
    "min_bytes": 4000
  },
  {
    "id": "tachikawa-yearbook-19-7",
    "claim": "Tokyo's yearbook chapter 19 lists table 19-7 (環境衛生営業施設数) as a CSV beside 19-8: the source open call 1 asks for (ASCII anchors)",
    "kind": "http_contains",
    "url": "https://www.toukei.metro.tokyo.lg.jp/tnenkan/2024/tn24q3i019.htm",
    "present": ["tn24qv190700.csv", "tn24qv190800.csv"]
  },
  {
    "id": "tachikawa-jr-timetables",
    "claim": "JR East's 立川 station list links the four weekday timetables counted here, the October 2026 edition (a failure means a new edition: re-count)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0958.html",
    "present": ["2610/timetable/tt0958/0958010.html", "2610/timetable/tt0958/0958020.html", "2610/timetable/tt0958/0958030.html", "2610/timetable/tt0958/0958040.html"]
  },
  {
    "id": "tachikawa-seibu-timetable",
    "claim": "Seibu's weekday timetable for 西武立川 (station 234-12, toward 西武新宿) is live and lists each train",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/234-12/d1?dw=0",
    "present": ["openOneTrainTimetable"]
  },
  {
    "id": "tachikawa-monorail-timetable-page",
    "claim": "The monorail's 立川北 timetable page links its station PDF TT12 (ASCII anchors: the host sends no charset)",
    "kind": "http_contains",
    "url": "https://www.tama-monorail.co.jp/monorail/station/tachikawa-kita/timetable.html",
    "present": ["station/TT12.pdf"]
  },
  {
    "id": "tachikawa-monorail-timetable-pdf",
    "claim": "The monorail's 立川北 timetable PDF (TT12, 343,228 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.tama-monorail.co.jp/monorail/station/TT12.pdf",
    "min_bytes": 200000
  },
  {
    "id": "tachikawa-projected-crs",
    "claim": "Tachikawa projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.405,
    "expect": "EPSG:32654"
  }
]
```
