# Chōfu — build brief

**Band B, owner-approved 2026-10-06 (call 187)**: all three buckets, **the
food share stated at the yearbook's date** (`docs/decisions_drafts/staging.md`,
"Wave 5, the last briefs": "The last four Tama cities (calls 187, 188, '187
and 188: B sounds good')"). Kure's 58.5% of the in-force count is the
precedent; Chōfu's 68.0% sits above it. Page name **"Chōfu"**, slug `chofu`,
N03 code **13208**. The ledgers were approved and fetched for the Tama
measurement, MHLW's Tokyo file as a control (calls 106, 141, 147), MLIT's
address blocks for the block join (call 106). **Step 0 measured 2026-10-06**
(staging), from cached files and Tama's own method (`wave5/tama_c4`, which
reproduced Tama's brief exactly):

- In `data/tokyo_tama/raw/` (gitignored), from `www.hokeniryo.metro.tokyo.lg.jp`
  (東京都保健医療局, the Tokyo Metropolitan Government's health centres for
  Tama), all as of **2026-08-31**: `shokuhin-kyoka-7.csv` (**4,486,267 B**,
  food permits), `shokuhin-todokede-1-7.csv` (**1,956,304 B**, food
  notifications), `kankyo-riyoujo-5.csv` (**165,277 B**, barbers),
  `kankyo-biyoujo-5.csv` (**608,582 B**, beauty salons), `kankyo-cleaning-5.csv`
  (**173,591 B**, laundries). From `i2fas.mhlw.go.jp`:
  `13000_food_business_all.csv` (**3,606,399 B**, Tokyo Prefecture's file).
  The build's `fetch_sources.py` fetches them into `data/chofu/raw/` (a
  Japanese build reads `data/<slug>/raw/`, Itami's precedent).
- **Downloaded for this brief** (2026-10-06, `japan_fetch.get`, the project
  user-agent, each HTTP 200, into `data/chofu/raw/isj/`): `13208-24.0a.zip`
  (**101,071 B**) and `13208-19.0b.zip` (**6,292 B**) from `nlftp.mlit.go.jp`.
  Nothing else was downloaded.

**Run `python scripts/brief_check.py chofu` before writing any code.** Then
the `japan-city` skill, **Itami's shape** (`docs/build_briefs/itami.md`: a
prefecture's standing lists, every row assigned to the city by its address),
with **Higashiyamato as its model on the same five files**
(`docs/build_briefs/higashiyamato.md`; Nishitōkyō, Tama, Higashimurayama,
Fuchū (Tokyo), Tachikawa and Hino are briefed on them too). Read the
`tokyo-ward` skill for Tokyo's catalogue sources and credits, and for the MHLW
slice beside a partial list (`SUPERSEDES`). Coordinates: the `address-join`
skill, measured with `pipeline/countries/japan_register.py`'s own functions
from scratch scripts (`scripts/screen_japan_join.py` has no entry; its table
is shared code and was not edited). Rail: MLIT N02-25 cut at the N03 city
line, through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

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
holds; (6) **no page says "currently operating"**. Also: no frequency floor
for JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at
about 11 trains a day or fewer **named and drawn** (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from
OSM `name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The food share is STATED at the yearbook's date (owner, call 187)**:
**68.0%** (1,170 of the 1,721 restaurants in force at 2025-03-31); the raw
share, 85.2%, is flattered by the 20.2% of rows first permitted after that
date. The ledgers' skew is disclosed as for the four Tama cities in A (call
109): new permits only from 2019-08, so long-standing premises not renewed
since 2017-04 are missing; laundry about half; opt-outs and closures left
out. **法人代表者氏名, the operator's address and the phones are dropped at
read** (call 109).

**✅ The licence (owner, call 108): the catalogue route, relied on** (Taitō's
precedent). The page links the Tokyo catalogue entries `t000055d0000000361`
and `t000055d0000000614`, **never the 保健医療局 page or files** (that site's
link policy). Below, "Licences".

**✅ MHLW's rows the ledgers lack are added (owner, call 169, for all Tama
cities)**: the Tokyo wards' precedent of 2026-09-24, the ledger's row kept
where both hold a premises (`SUPERSEDES`), MHLW's PDL 1.0 notice line added,
**the stated share WITHOUT MHLW's rows**. **The notification ledger is read
into Retail** (decided for the Tama cities in A; Ichinomiya's call 127b,
partial, disclosed). **The 2024 snapshot stays a cross-check only** (call
147).

**✅ `mode`: `metro`** (Yokosuka's precedent, the owner's rule of 2026-10-02:
a private heavy railway, no subway, tram or light rail; call 170 read
Higashiyamato the same way).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Chōfu
carries `label_tier: "minor"` and `"region": "Japan East"` (`app/cities.py`);
wave 4's first city to land retags Japan into the eight regions, Chōfu into
**Kanto**. Its dot sits between Fuchū (Tokyo)'s and the Tokyo page's 世田谷区
edge: its label offset from `check_macro_labels.py` (PROBLEMS 0 at 375, 768
and 1200), never by eye.

---

## The one-line summary

**All three buckets from the Tokyo Metropolitan Government's monthly Tama
ledgers (CC BY 4.0 through the catalogue route, relied on, call 108), cut to
Chōfu by address, as of 2026-08-31: 1,803 food permits (1,467 restaurants),
796 food notifications, 78 barbers, 314 beauty salons and 92 laundries**,
plus MHLW's rows the ledgers lack (call 169). The restaurants are **85.2% of
the 1,721 in force** (Tokyo's statistical yearbook, table 19-8, FY2024),
flattered: **297 (20.2%) were first permitted after the control date**, so
**the share the page states is 68.0%** (call 187). Barbers about 86%, beauty
salons about 105%, laundries about 59% of census-scaled estimates (no official
per-city count). Through `japan_eigyo`: **Food service 1,278 rows (1,260
pins), Retail 316 permit rows (250 pins) plus 608 notification rows (489
pins)** once the shared `自動車以外` trap is fixed (539 and 428 before it);
Personal services 481 (475 pins). **Block join 99.6%** (permits and
registers; 99.5% with the notifications), 2 rows unplaced. **Rail: 9 N02
station groups, Keiō only** (Keiō Line 8, Sagamihara Line 2, 調布 on both);
frequencies ASSERTED (Keiō's timetables need scripts). No one-station line.

---

## Business leg — the Tokyo Metropolitan Government's Tama ledgers

Page `https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho`
(東京都が設置している保健所等で保有する台帳一覧, 更新日 2026-09; UTF-8). The
ledgers cover the health centres the Metropolitan Government runs: Tama less
Hachiōji and Machida, plus the islands. **Chōfu is 多摩府中保健所's**
(武蔵野市, 三鷹市, 府中市, 調布市, 小金井市, 狛江市). The page:
「ホームページへの公表を希望しない施設、廃止・休止している施設は除いて公表しています」
(opt-outs and closed or suspended premises are left out) and, for food,
「移動販売、臨時販売、自動車販売、自動販売機、行商、催事等期間短縮申請があったもの、届出が不要な施設及び廃業した施設は除いています」.
Items an applicant asked MHLW to withhold are withheld here too.

| Ledger (CSV, cp932) | Edition line on the page | Rows (all areas) | Rows in Chōfu |
|---|---|---|---|
| `shokuhin-kyoka-7` 食品関係営業台帳（許可） | 「平成29年1月から令和8年8月までの新規許可施設及び平成29年4月から令和8年8月までの許可更新施設（令和8年8月31日現在）」 | 28,093 | **1,803** |
| `shokuhin-todokede-1-7` 食品関係営業台帳（届出） | 「令和3年6月から令和8年8月までの届出施設（令和8年8月31日現在）」 | 12,502 | **796** |
| `kankyo-riyoujo-5` 理容所台帳 | 「令和8年8月31日現在、台帳に掲載されている施設」 | 1,427 | **78** |
| `kankyo-biyoujo-5` 美容所台帳 | as above | 4,319 | **314** |
| `kankyo-cleaning-5` クリーニング所台帳 | as above | 1,040 | **92** |

Files at `https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/<name>`
(each also offered as Excel; the CSV is read). ⚠️ **The slugs carry a
revision suffix** (`-7`, `-1-7`, `-5`) that may move with a monthly edition:
`fetch_sources.py` takes them from the page's links (a `SOURCE_LINKS` regex,
Akita's and Kawasaki's precedent) and pins `SOURCE_AS_OF` to the page's
「令和8年8月31日現在」, never the fetch date. The edition check below fails
when a new month lands: re-measure then.

- **Assigning a row to the city**: the address starts 東京都調布市 (the
  prefecture is written on every row). Every one of the city's rows has an
  address. `permits_from_rows(rows, "東京都", "調布市", wardless=True)` strips
  both.
- **Columns** (permits): 屋号, **営業所所在地**, 営業者氏名, 営業者住所 (never),
  **営業の種類**, **申請区分** (新規 / 更新), 営業所電話番号 (never),
  **初回許可日**, 営業者電話番号 (never), 法人代表者氏名 (dropped at read, call
  109). Notifications: the same less 申請区分 and 初回許可日, with
  **届出年月日**. Registers: 確認番号, **施設名称**, 施設TEL (never),
  **施設所在地**, 施設ビル名, 営業者氏名, 法人代表者氏名 (dropped), 営業者住所
  (never), 営業者ビル名 (never), 営業者TEL (never), 確認年月日; the laundry
  ledger adds **営業形態**.
- **Against the shared tuples**: 営業所所在地 and 施設所在地 are in `ADDR_COLS`,
  屋号 and 施設名称 in `NAME_COLS`, 営業の種類 and 営業形態 in `TYPE_COLS`,
  営業者氏名 in `OPERATOR_COLS`. ⚠️ **`OPERATOR_COLS` also holds
  法人代表者氏名**, so the read drops it before rows reach the name rule
  (measured: the rule withholds 0 rows with it or without it). **No 業態
  column**: the permit type's bracket carries the form (`飲食店営業(集団給食)`,
  `(仕出し屋)`, `(旅館・ホテル)`, `(バー・キャバレー)`), and `japan_eigyo` reads
  it from the type.

### The food permit ledger (1,803 rows in the city)

- **申請区分**: 新規 1,668, 更新 135. **Kinds**: 飲食店営業 1,467, 菓子製造業
  154, 食肉販売業 41, 魚介類販売業 40, そうざい製造業 36, 麺類製造業 13,
  密封包装食品製造業 8, 漬物製造業 7, 水産製品製造業 5, アイスクリーム類製造業 5,
  食肉処理業 4, 喫茶店営業 4, others 3 or fewer each. Restaurant sub-types:
  一般飲食店 1,106, 集団給食 92, 弁当屋 62, すし屋 47, そうざい店 45, そば屋 44,
  バー・キャバレー 32, 仕出し屋 22, 喫茶店 13, 簡易な営業 2, 旅館・ホテル 2.
- **Against the yearbook** (table 19-8, FY2024, 調布市; `japan_official`):
  **飲食店営業 1,467 of 1,721, 85.2%**. 菓子 154 of 215, 食肉販売 41 of 94, 魚介類販売
  40 of 81, そうざい製造 36 of 39, 麺類 13 of 18, 豆腐 2 of 3.
- **The dates (the skew)**: restaurant 新規 rows were first permitted
  **2019-09-18 to 2026-08-27** (ledger-wide the earliest 新規 is 2019-08, not
  the 2017-01 the edition line names); 更新 rows carry first permits from
  1971-04 to 2015-06. By first-permit year: 118 rows before 2020, 29 in 2020,
  then 227, 214, 290, 243 a year (2021-2024), 218 in 2025 and 128 to 2026-08.
  **297 restaurant rows (20.2%) were first permitted after 2025-03-31**, so at
  the yearbook's control date the ledger holds **1,170, 68.0%** of the 1,721:
  **the figure the page states** (call 187), measured each build, never typed.
- **Old-law permits are in the ledger** (not Kurashiki's trap): 喫茶店営業 (an
  old-law type only) 4 rows, and 更新 rows first permitted 1971-2015. The gap
  is the ledger's own window, above, not the law change.
- **Duplicates**: 18 exact repeats of (address, trade name, kind); 230 rows
  repeat an (address, trade name) under another kind; **1,573 distinct
  premises**. One pin per premises and bucket (trap 7).
- **Closures are left out at source** (the page); no closure column. The page
  keeps "may include closed premises" all the same (the monthly edition lags).

### The food notification ledger (796 rows)

- 届出年月日 1968-07 to 2026-08 (337 in 2021, the law change, then 118, 96, 79,
  59 and 37 to 2026-08; 70 rows dated before 2021). Types: その他の食料・飲料販売業
  286, 集団給食施設 117, コンビニエンスストア 101, 乳類販売業 47, 百貨店、総合スーパー 46,
  野菜果物販売業 35, 弁当販売業 34, 食肉販売業（包装済み） 32, 調味料製造・加工業 25,
  コーヒー製造・加工業 21, 魚介類販売業（包装済み） 19, 米穀類販売業 8, …
- **Against the yearbook's columns**: コンビニエンスストア **101 of 103**,
  百貨店・総合スーパー **46 of 48**, 野菜果物販売業 35 of 41, 乳類販売業 **47 of 132**,
  弁当販売業 34 of 47, 米穀類販売業 8 of 8, 集団給食施設 117 of 125. Partial where
  old-law permit holders were never re-filed (dairy above), disclosed as
  partial (call 127b).
- ⚠️ **The `自動車以外` trap (shared code)**: 野菜果物販売業(自動車以外) **35** and
  弁当販売業(自動車以外) **34** ("other than a vehicle") are read as **mobile** by
  `permits_from_rows` (its vehicle test is a bare `自動車` in the type) and as
  temporary or mobile by `japan_eigyo`. No permit row carries it. The build
  changes both tests to skip `自動車以外` (a lookahead, `自動車(?!以外)`; the
  drafts entry for calls 154-184 names it), then re-runs the Minato control
  and every city screen; the **69 rows** here become greengrocers and bento
  shops in Retail.

### Counts through `japan_eigyo` (fixed premises)

**Food service 1,278** (**1,260 pins**). **Retail from the permits 316**
(そうざい店, 菓子, 食肉, 魚介, そうざい製造; **250 pins**). **Retail from the
notifications 539** today (428 pins), **608 after the `自動車以外` fix (489
pins)**. **Personal services 481** (barbers 78, beauty 314, laundry 89; 475
pins). Left out: institutional catering 92 + 117, hostess venues
(バー・キャバレー, `docs/category_rules.md` R3) 32, event catering 22, inside
accommodation 2, mail order 1, a linen supplier 1, and 61 + 70 manufacturing
types with no rule (麺類, 密封包装食品, 調味料, コーヒー製造, …), as in every built
city. Not a premises: 71 today (the 69 above and 2 more), 2 after the fix.

**Economic Census control** (`scripts/japan_census_control.py` at build): the
2021 census counts **752** 飲食店 establishments in 13208
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 1,260 distinct placed
Food-service premises is **1.68 per establishment**, inside the built cities'
1.56-1.92.

### Personal services: the three registers

| Register | Rows | Census 2021 (9-1A) | Estimate (census x Hachiōji's licensed-to-census ratio) | Share |
|---|---|---|---|---|
| 理容所台帳 (barbers) | **78** | 81 | 91 | **86%** (80% on all Tokyo's ratio) |
| 美容所台帳 (beauty) | **314** | 191 | 300 | **105%** (77%) |
| クリーニング所台帳 (laundry) | **90** of 92 (取次所 63, 一般 24, 一般＋リネン 1, リネン 1, 消毒 1; 無店舗取次店 2 left out) | 87 | 152 | **59%** (65%) |

No official per-city count exists for a Tama city (e-Stat's 衛生行政報告例
lists Hachiōji alone), so the shares are estimates: the census count times
Hachiōji's ratio of licensed premises to census establishments (277/247,
807/514, 264/151), Tokyo's (7,328/6,122, 28,589/13,455, 8,147/5,137) beside
it. Beauty at 105% of the estimate is an estimate's overshoot, not a duplicate
problem (1 repeat of (address, name)). 確認年月日 run from 1964, 1965 and 1963
to 2025-2026: **standing registers**, not a stream, so the permits' skew does
not reach them. 17 addresses carry both a barber and a beauty salon. The
リネン row is left out by `japan_eigyo` (89 bucketed); the two 無店舗取次店 rows
read as not a premises through `無店舗`.

### MHLW's Tokyo file (13000): the rows the ledgers lack (call 169)

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv`:
**3,606,399 B, 10,003 rows**, UTF-8 with BOM, the national schema. ⚠️
**市区町村名 reads 新宿区 on every row** (the registering office); the premises'
city is in 営業施設所在地, so the build filters by address, never by 市区町村名.
MHLW publishes no per-city file for 13208 (the check below expects HTTP 404).

- **550 rows in Chōfu** (届出 376, 許可 169, 許可(廃業) 5), 許可年月日 2021-10 to
  2026-07, 549 with their own point. Open restaurant permits 140.
- **Against the ledgers** (parsed town and first number, then the trade name,
  NFKC): of **169 open permits**, 96 are in a ledger by (town, number), 92 also
  by trade name; **73 are not** (**Food service 37, Retail 26**, out 9, mobile
  1; 77 by the stricter trade-name match: 39, 28, 9, 1). The 63 restaurant
  permits missing by trade name were permitted 2021-2026 (24 in 2025). Of
  **376 open notifications**, 137 are in a ledger by (town, number); **239 are
  not** (**Retail 131**, out 108: vending, catering, manufacturing). The 5
  closed rows are left out.
- **So call 169 adds about 37 restaurants and 157 shops here** (by (town,
  number); up to 39 and 165 by the trade-name match), more than in Fuchū (16
  and 74). The build's `SUPERSEDES` pass decides the exact figure; the stated
  68.0% excludes them.
- **Its own coordinates against the block point**: median **31 m**, 92.9%
  within 250 m (534 rows). MHLW's own point is used where the block join
  misses (Ichinomiya's call 127c).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13208-24.0a.zip` (101,071 B,
**4,237 block keys**), town-chōme `.../19.0b/13208-19.0b.zip` (6,292 B,
**108**), both in `data/chofu/raw/isj/` and nothing else there (⚠️
`load_city_isj` globs its directory, and `data/tokyo_tama/raw/isj/` holds four
other municipalities' pairs all keyed under ward ""). `japan.CITIES` entry at
build: `"chofu": {"name": "調布市", "pref": "13", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["13208"]}`.

| Tier, today's shared code | Rows | Block | Town-chōme | Unplaced |
|---|---|---|---|---|
| **Permits and registers** | 2,075 | **99.6%** | 0.4% | 0 |
| … Food service / Retail (permits) | 1,278 / 316 | 99.6% / 99.7% | 0.4 / 0.3 | 0 |
| … Barbers / beauty / laundry | 78 / 314 / 89 | 98.7% / 100% / 98.9% | 1.3 / 0 / 1.1 | 0 |
| Notifications, Retail (after the `自動車以外` fix) | 608 | 99.2% | 0.5% | 0.3% (2) |
| **All, with the notifications** | 2,683 | **99.5%** | 0.4% | 0.1% (2) |

**The misses, read** (towns only, by `misses.py` over every ledger row of the
city: 3,083 rows, 99.5% block):
- **Chōme tier (12 of all rows)**: 小島町2丁目 5 (a shopping complex by 調布
  station whose number MLIT's block file lacks), 国領町3丁目 3, 富士見町3丁目 2,
  国領町4丁目 1, 西町 1: each takes its chōme's centroid.
- **Unplaced (4 of all rows, 2 bucketed)**: one hyphen-form address the parser
  reads as 西町37丁目, one written "…周辺" (near), and two with a blank town. No
  shared rule is proposed.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_13_GML.zip`, N03 code 13208
(**21.57 km²**, extent W 139.517, S 35.633, E 139.593, N 35.688; centroid
139.552, 35.658). Read with `stub_test()`'s method and an in-memory `CITIES`
entry (scratch `rail.py`, `near_line.py`).

| N02 line (operator, class) | Public name | Stations inside / on the line | Stations inside |
|---|---|---|---|
| 京王線 (京王電鉄, 12) | Keiō Line | **8 / 35** | 仙川, つつじヶ丘, 柴崎, 国領, 布田, 調布, 西調布, 飛田給 |
| 相模原線 (京王電鉄, 12) | Keiō Sagamihara Line | **2 / 12** | 調布 (its junction), 京王多摩川 |

- **10 station records, 9 N02_005g groups**: 調布 is one group for both lines
  (0 m span). **Median nearest-group gap 667 m** (606 to 1,141; 飛田給 and
  西調布 606 m, 国領 and 布田 609 m): rings by the spacing rule at build.
- **The one-station rule (calls 54, 92, 163, 165, 167): no line has one
  station in the city.** The Sagamihara Line keeps 2 (調布, its junction with
  the Keiō Line, and 京王多摩川); no stub, no left-out line, no owner question.
- **Near the line, outside**: no N02 station lies within 300 m of the city
  line outside it.
- **Cut at the line**: the Keiō Line 27 beyond (世田谷区 7, 府中市 6, 日野市 4,
  渋谷区 3, 八王子市 3, 新宿区 2, 杉並区 1, 多摩市 1); the Sagamihara Line 10
  (Kanagawa 3, 稲城市 2, 八王子市 2, 多摩市 2, 町田市 1).
- **The light-rail/rail test**: both lines are private heavy rail (class 12).
  No JR, subway, monorail, tram or light rail.
- **Frequency: ASSERTED, not read.** Keiō's timetables are a NAVITIME app: the
  調布 station page (`www.keio.co.jp/train/station/ko18_chofu/`) links
  `transfer-train.navitime.biz/keio/directions/timetable?...`, which renders
  in the browser, so curl gets a 2.7 KB shell with no departures (the J6
  probe's page). As stated by the probe: the Keiō Line and the Sagamihara
  Line run several trains an hour at every station here; **no stretch is
  expected at or under about 11 trains a day** (call 86). ⚠️ The build reads
  the counts (a whole-page reader, counting marked trains: the jre.py trap) or
  records them as ASSERTED on the page's internal notes.
- ⚠️ **Gate 3** at build: Keiō's own station counts inside the city (Keiō Line
  8, Sagamihara Line 2, 9 places). **OSM `name:en`** for 9 groups (one
  Overpass query at build, in the box below; not queried here).

## Scope

**Chōfu City.** The Keiō Line runs on to 新宿 and 八王子, the Sagamihara Line
to 橋本; cut at the line. The Tokyo page covers the 23 special wards only;
Chōfu is its own page (the band).

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
  form) is the built precedent; confirm the wording against staging's record.
- **The host site's own policy** (保健医療局) bars reuse and links below its
  top page: **the page links the two catalogue entries, never the 保健医療局 page
  or files.** `fetch_sources.py` downloads from that host (an automated GET,
  not a link); the provenance file may name the file URLs, the rendered page
  may not.
- **MHLW open data** (call 169: its rows are added): PDL 1.0 as recorded in
  `docs/data_sources/japan.md`, its 出典 line and who processed it, as the
  Tokyo wards' MHLW slice.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **The yearbook and the census**:
  measurement sources, not drawn.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here. The Tama ledgers' row in
  `docs/data_sources/japan.md` is shared with the other Tama cities.

## Privacy

- **Dropped at read (call 109)**: 法人代表者氏名, 営業者住所 and 営業者ビル名 (the
  operator's own address), and every phone column (営業所電話番号, 営業者電話番号,
  施設TEL, 営業者TEL). Only 屋号 / 施設名称, the premises address and the type
  are ever selected; 営業者氏名 is read IN MEMORY for the name rule and never
  written.
- **The operator column, measured** (counts only): food permits 1,803,
  営業者氏名 filled on 1,100 (a company marker on 1,081, none on 19), blank on
  703; notifications 796, filled 609 (578 / 31), blank 187; barbers 78, filled
  10 (all companies), blank 68; beauty 314, filled 146 (all companies), blank
  168; laundry 92, filled 59 (all companies), blank 33. The operator is
  published almost only for companies: the blanks are the shape of
  individuals withheld at source.
- **The name rule, version 2, measured in memory** (answers only, never a
  value): the sign rule 0, the operator comparison 0, **0 rows withheld** in
  any ledger, with or without 法人代表者氏名.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; its 法人名 joins
  the name rule for the rows call 169 brings in (owner, 2026-10-05).
- Run `check_personal_exposure.py chofu` (`japan=True`) after step 2: it must
  print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.517-139.593 E, centroid 139.552:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded out:
(35.63, 139.51, 35.69, 139.60). Scaffold with `scripts/scaffold_city.py ...
--page-number <N>`, the number claimed at build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band B with the
food share stated at the yearbook's date (call 187); the skew disclosed and
the three columns dropped at read (call 109, as the Tama cities in A); the
catalogue route and its credit (call 108); the notifications in as partial
Retail (call 127b, the Tama cities in A); `mode: metro` (precedent, call 170);
the minor tier and Japan East (Kanto after the retag); no frequency floor
(call 46); the `自動車以外` lookahead (named in the drafts entry for calls
154-184, Minato control at build).

**Answered by the owner on 2026-10-06:** call 187, **Band B, all three
buckets, the food share stated at the yearbook's date** (68.0%; raw 85.2%;
Kure's 58.5% of the in-force count the precedent; "187 and 188: B sounds
good"). Call 169, **MHLW's rows the ledgers lack added** for all Tama cities
(the Tokyo wards' precedent: the ledger's row kept where both hold a premises,
`SUPERSEDES`; MHLW's PDL 1.0 notice line; the stated share WITHOUT MHLW's
rows). The notification ledger read into Retail (decided for the four Tama
cities in A). The 2024 snapshot a cross-check only (call 147). Not re-opened.

**Open:** none.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): the `自動車以外` lookahead in `permits_from_rows`' vehicle test and
  in `japan_eigyo`'s temporary or mobile rule (69 rows here, 1,063 across the
  Tama ledgers). Nothing else: the columns are all known.
- The read: drop 法人代表者氏名, 営業者住所, 営業者ビル名 and the phones before
  `city_rows` hands rows on; `SOURCE_KIND` per register file (no type column
  in the barber and beauty ledgers); the city cut by address; `SOURCE_LINKS`
  for the slugs; `SOURCE_AS_OF` 2026-08-31 from the page.
- MHLW's slice: the 13000 file cut by 営業施設所在地, `SUPERSEDES` against the
  ledgers, its 法人名 through the name rule, its own point where the block join
  misses; the count it adds (about 37 restaurants and 157 shops here).
- `ISJ_DIR` holding only 13208's pair; the share and its control-date figure
  from `official_shares` (the yearbook's 1,721; 68.0% stated, measured, never
  typed), and the page's sentence from the approved template (calls 109,
  187); the census ratio (1.68).
- Keiō's frequencies (or ASSERTED); gate 3; OSM `name:en`; the label at 調布
  (two lines); line colors on both basemaps; the opening view (`map-view`);
  the factory share; `check_provenance.py`; `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "chofu-ledger-page",
    "claim": "The Tama ledgers page names the five ledgers, their windows, the opt-out rule, and Chofu under 多摩府中保健所",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["平成29年1月から令和8年8月までの新規許可施設", "令和3年6月から令和8年8月までの届出施設", "公表を希望しない施設", "多摩府中保健所（武蔵野市、三鷹市、府中市、調布市", "shokuhin-kyoka-7", "shokuhin-todokede-1-7", "kankyo-riyoujo-5", "kankyo-biyoujo-5", "kankyo-cleaning-5"]
  },
  {
    "id": "chofu-ledger-edition",
    "claim": "The edition measured here: the ledgers as of 2026-08-31 (a failure here means a new monthly edition: re-measure)",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["令和8年8月31日現在"]
  },
  {
    "id": "chofu-food-permits-file",
    "claim": "The food permit ledger (4,486,267 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-kyoka-7",
    "min_bytes": 2000000
  },
  {
    "id": "chofu-food-notifications-file",
    "claim": "The food notification ledger (1,956,304 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-todokede-1-7",
    "min_bytes": 1500000
  },
  {
    "id": "chofu-barber-file",
    "claim": "The barber ledger (165,277 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-riyoujo-5",
    "min_bytes": 100000
  },
  {
    "id": "chofu-beauty-file",
    "claim": "The beauty-salon ledger (608,582 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-biyoujo-5",
    "min_bytes": 400000
  },
  {
    "id": "chofu-laundry-file",
    "claim": "The laundry ledger (173,591 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-cleaning-5",
    "min_bytes": 100000
  },
  {
    "id": "chofu-catalogue-food",
    "claim": "Tokyo's catalogue entry t000055d0000000361 (食品関係営業台帳) declares CC BY 4.0 and points at the 保健医療局 ledger page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000361",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "chofu-catalogue-registers",
    "claim": "Tokyo's catalogue entry t000055d0000000614 (環境衛生施設台帳) declares CC BY 4.0 and points at the same page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000614",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "chofu-tokyo-terms",
    "claim": "The Tokyo Open Data Terms allow commercial use and prescribe a modified-use credit",
    "kind": "http_contains",
    "url": "https://portal.data.metro.tokyo.lg.jp/terms/",
    "present": ["商用利用も可能", "改変して利用", "編集・加工等を行った旨"]
  },
  {
    "id": "chofu-mhlw-tokyo",
    "claim": "MHLW's Tokyo Prefecture file (13000, 3,606,399 B) answers a plain keyless GET (call 169's rows)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "chofu-no-mhlw-city-file",
    "claim": "MHLW has no per-city file for 13208 (HTTP 404): the prefecture licenses Chofu, so its rows sit in 13000",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13208_food_business_all.csv",
    "expect_status": 404
  },
  {
    "id": "chofu-isj-block-live",
    "claim": "MLIT's block-level address file for Chofu (13208) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13208-24.0a.zip",
    "min_bytes": 80000
  },
  {
    "id": "chofu-isj-chome-live",
    "claim": "MLIT's town-chōme file for Chofu (13208) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/13208-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "chofu-keio-timetable-navitime",
    "claim": "Keio's 調布 station page links its timetables to NAVITIME's app (why the frequencies are ASSERTED: the app renders in the browser)",
    "kind": "http_contains",
    "url": "https://www.keio.co.jp/train/station/ko18_chofu/",
    "present": ["transfer-train.navitime.biz/keio/directions/timetable"]
  },
  {
    "id": "chofu-projected-crs",
    "claim": "Chofu projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.55,
    "expect": "EPSG:32654"
  }
]
```
