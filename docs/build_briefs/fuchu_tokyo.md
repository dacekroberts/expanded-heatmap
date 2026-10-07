# Fuchū (Tokyo) — build brief

**Band B, owner-approved 2026-10-06 (call 188)**: all three buckets, **the
food share stated at the yearbook's date** (`docs/decisions_drafts/staging.md`,
"Wave 5, the last briefs": "The last four Tama cities (calls 187, 188, '187
and 188: B sounds good')"). Kure's 58.5% of the in-force count is the
precedent; Fuchū's 57.6% sits 0.9 points under it, **the lowest food share on
any page**. Page name **"Fuchū (Tokyo)"**, slug `fuchu_tokyo`, N03 code
**13206** (not Hiroshima's 府中市, 34208: the `CITIES` entry's `"pref": "13"`
keeps them apart). The ledgers were approved and fetched for the Tama
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
  The build's `fetch_sources.py` fetches them into `data/fuchu_tokyo/raw/` (a
  Japanese build reads `data/<slug>/raw/`, Itami's precedent).
- **Downloaded for this brief** (2026-10-06, `japan_fetch.get`, the project
  user-agent, each HTTP 200, into `data/fuchu_tokyo/raw/isj/`):
  `13206-24.0a.zip` (**124,713 B**) and `13206-19.0b.zip` (**6,841 B**) from
  `nlftp.mlit.go.jp`. Nothing else was downloaded. The operators' timetable
  pages were read for counts only (below), never saved into `data/`.

**Run `python scripts/brief_check.py fuchu_tokyo` before writing any code.**
Then the `japan-city` skill, **Itami's shape** (`docs/build_briefs/itami.md`: a
prefecture's standing lists, every row assigned to the city by its address),
with **Higashiyamato as its model on the same five files**
(`docs/build_briefs/higashiyamato.md`; Nishitōkyō, Tama, Higashimurayama,
Chōfu, Tachikawa and Hino are briefed on them too). Read the `tokyo-ward`
skill for Tokyo's catalogue sources and credits, and for the MHLW slice beside
a partial list (`SUPERSEDES`). Coordinates: the `address-join` skill, measured
with `pipeline/countries/japan_register.py`'s own functions from scratch
scripts (`scripts/screen_japan_join.py` has no entry; its table is shared code
and was not edited). Rail: MLIT N02-25 cut at the N03 city line, through
`pipeline/countries/japan.py` with a scratch `CITIES` entry.

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

**✅ The food share is STATED at the yearbook's date (owner, call 188)**:
**57.6%** (1,261 of the 2,188 restaurants in force at 2025-03-31); the raw
share, 70.7%, is flattered by the 18.5% of rows first permitted after that
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
private and JR heavy railways, no subway, tram or light rail; call 170 read
Higashiyamato the same way).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Fuchū
carries `label_tier: "minor"` and `"region": "Japan East"` (`app/cities.py`);
wave 4's first city to land retags Japan into the eight regions, Fuchū into
**Kanto**. Its dot sits between Chōfu's and Tama's (both briefed, not yet
built): its label offset from `check_macro_labels.py` (PROBLEMS 0 at 375, 768
and 1200), never by eye.

---

## The one-line summary

**All three buckets from the Tokyo Metropolitan Government's monthly Tama
ledgers (CC BY 4.0 through the catalogue route, relied on, call 108), cut to
Fuchū by address, as of 2026-08-31: 1,909 food permits (1,547 restaurants),
799 food notifications, 101 barbers, 263 beauty salons and 88 laundries**,
plus MHLW's rows the ledgers lack (call 169). The restaurants are **70.7% of
the 2,188 in force** (Tokyo's statistical yearbook, table 19-8, FY2024),
flattered: **286 (18.5%) were first permitted after the control date**, so
**the share the page states is 57.6%** (call 188). Barbers about 86%, beauty
salons about 88%, laundries about 52% of census-scaled estimates (no official
per-city count). Through `japan_eigyo`: **Food service 1,318 rows (1,297
pins), Retail 357 permit rows (284 pins) plus 630 notification rows (530
pins)** once the shared `自動車以外` trap is fixed (576 and 480 before it);
Personal services 451 (445 pins). **Block join 97.3%** (permits and
registers; 96.6% with the notifications), 2 rows unplaced. **Rail: 14 N02
station groups**: Keiō 7 (Keiō Line 6, Keibajō Line 2, 東府中 on both;
ASSERTED), JR East 4 (Nambu Line 3, Musashino Line 2, 府中本町 on both;
125-138 weekday departures each way), Seibu Tamagawa Line 4 (87-90 each way,
every 12 minutes), JR and Seibu read from the operators' own timetables. No
one-station line; nothing read at or under 11 trains a day (the Keibajō Line
is not read).

---

## Business leg — the Tokyo Metropolitan Government's Tama ledgers

Page `https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho`
(東京都が設置している保健所等で保有する台帳一覧, 更新日 2026-09; UTF-8). The
ledgers cover the health centres the Metropolitan Government runs: Tama less
Hachiōji and Machida, plus the islands. **Fuchū is 多摩府中保健所's**
(武蔵野市, 三鷹市, 府中市, 調布市, 小金井市, 狛江市). The page:
「ホームページへの公表を希望しない施設、廃止・休止している施設は除いて公表しています」
(opt-outs and closed or suspended premises are left out) and, for food,
「移動販売、臨時販売、自動車販売、自動販売機、行商、催事等期間短縮申請があったもの、届出が不要な施設及び廃業した施設は除いています」.
Items an applicant asked MHLW to withhold are withheld here too.

| Ledger (CSV, cp932) | Edition line on the page | Rows (all areas) | Rows in Fuchū |
|---|---|---|---|
| `shokuhin-kyoka-7` 食品関係営業台帳（許可） | 「平成29年1月から令和8年8月までの新規許可施設及び平成29年4月から令和8年8月までの許可更新施設（令和8年8月31日現在）」 | 28,093 | **1,909** |
| `shokuhin-todokede-1-7` 食品関係営業台帳（届出） | 「令和3年6月から令和8年8月までの届出施設（令和8年8月31日現在）」 | 12,502 | **799** |
| `kankyo-riyoujo-5` 理容所台帳 | 「令和8年8月31日現在、台帳に掲載されている施設」 | 1,427 | **101** |
| `kankyo-biyoujo-5` 美容所台帳 | as above | 4,319 | **263** |
| `kankyo-cleaning-5` クリーニング所台帳 | as above | 1,040 | **88** |

Files at `https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/<name>`
(each also offered as Excel; the CSV is read). ⚠️ **The slugs carry a
revision suffix** (`-7`, `-1-7`, `-5`) that may move with a monthly edition:
`fetch_sources.py` takes them from the page's links (a `SOURCE_LINKS` regex,
Akita's and Kawasaki's precedent) and pins `SOURCE_AS_OF` to the page's
「令和8年8月31日現在」, never the fetch date. The edition check below fails
when a new month lands: re-measure then.

- **Assigning a row to the city**: the address starts 東京都府中市 (the
  prefecture is written on every row). Every one of the city's rows has an
  address. `permits_from_rows(rows, "東京都", "府中市", wardless=True)` strips
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
  (measured: the rule withholds the same 4 rows with it or without it). **No
  業態 column**: the permit type's bracket carries the form
  (`飲食店営業(集団給食)`, `(仕出し屋)`, `(旅館・ホテル)`, `(バー・キャバレー)`),
  and `japan_eigyo` reads it from the type.

### The food permit ledger (1,909 rows in the city)

- **申請区分**: 新規 1,737, 更新 172. **Kinds**: 飲食店営業 1,547, 菓子製造業
  156, 食肉販売業 47, そうざい製造業 45, 魚介類販売業 44, アイスクリーム類製造業 12,
  密封包装食品製造業 8, 豆腐製造業 6, 麺類製造業 6, others 5 or fewer each.
  Restaurant sub-types: 一般飲食店 1,190, 集団給食 97, そうざい店 64, 弁当屋 54,
  バー・キャバレー 49, そば屋 36, すし屋 27, 旅館・ホテル 12, 仕出し屋 8, 喫茶店 7,
  簡易な営業 2, コンビニエンスストア等 1.
- **Against the yearbook** (table 19-8, FY2024, 府中市; `japan_official`):
  **飲食店営業 1,547 of 2,188, 70.7%**. 菓子 156 of 236, 食肉販売 47 of 86, 魚介類販売
  44 of 80, そうざい製造 45 of 51, 麺類 6 of 7, 豆腐 6 of 8.
- **The dates (the skew)**: restaurant 新規 rows were first permitted
  **2019-08-09 to 2026-08-31** (ledger-wide the earliest 新規 is 2019-08, not
  the 2017-01 the edition line names); 更新 rows carry first permits from
  1970-10 to 2015-05. By first-permit year: 141 rows before 2020, 39 in 2020,
  then 232, 276, 294, 222 a year (2021-2024), 196 in 2025 and 147 to 2026-08.
  **286 restaurant rows (18.5%) were first permitted after 2025-03-31**, so at
  the yearbook's control date the ledger holds **1,261, 57.6%** of the 2,188:
  **the figure the page states** (call 188), measured each build, never typed.
- **Old-law permits are in the ledger** (not Kurashiki's trap): 喫茶店営業 (an
  old-law type only) 2 rows, and 更新 rows first permitted 1970-2015. The gap
  is the ledger's own window, above, not the law change.
- **Duplicates**: 26 exact repeats of (address, trade name, kind); 229 rows
  repeat an (address, trade name) under another kind; **1,680 distinct
  premises**. One pin per premises and bucket (trap 7).
- **Closures are left out at source** (the page); no closure column. The page
  keeps "may include closed premises" all the same (the monthly edition lags).

### The food notification ledger (799 rows)

- 届出年月日 1963-04 to 2026-07 (361 in 2021, the law change, then 93, 84, 75,
  63 and 52 to 2026-07; 71 rows dated before 2021). Types: その他の食料・飲料販売業
  300, コンビニエンスストア 132, 集団給食施設 102, 乳類販売業 54, 百貨店、総合スーパー 46,
  野菜果物販売業 39, 食肉販売業（包装済み） 24, コーヒー製造・加工業 19, 弁当販売業 15,
  魚介類販売業（包装済み） 12, 米穀類販売業 8, …
- **Against the yearbook's columns**: コンビニエンスストア **132 of 138**,
  百貨店・総合スーパー **46 of 46**, 野菜果物販売業 39 of 48, 乳類販売業 **54 of 164**,
  弁当販売業 15 of 19, 米穀類販売業 8 of 8, 集団給食施設 102 of 124. Partial where
  old-law permit holders were never re-filed (dairy above), disclosed as
  partial (call 127b).
- ⚠️ **The `自動車以外` trap (shared code)**: 野菜果物販売業(自動車以外) **39** and
  弁当販売業(自動車以外) **15** ("other than a vehicle") are read as **mobile** by
  `permits_from_rows` (its vehicle test is a bare `自動車` in the type) and as
  temporary or mobile by `japan_eigyo`. No permit row carries it. The build
  changes both tests to skip `自動車以外` (a lookahead, `自動車(?!以外)`; the
  drafts entry for calls 154-184 names it), then re-runs the Minato control
  and every city screen; the **54 rows** here become greengrocers and bento
  shops in Retail.

### Counts through `japan_eigyo` (fixed premises)

**Food service 1,318** (**1,297 pins**). **Retail from the permits 357**
(そうざい店, 菓子, 食肉, 魚介, そうざい製造; **284 pins**). **Retail from the
notifications 576** today (480 pins), **630 after the `自動車以外` fix (530
pins)**. **Personal services 451** (barbers 101, beauty 263, laundry 87; 445
pins). Left out: institutional catering 97 + 102, hostess venues
(バー・キャバレー, `docs/category_rules.md` R3) 49, inside accommodation 12,
event catering 8, mail order 3, and 68 + 63 manufacturing types with no rule
(アイスクリーム類, 密封包装食品, コーヒー製造, 調味料, …), as in every built city. Not
a premises: 56 today (the 54 above and 2 more), 2 after the fix.

**Economic Census control** (`scripts/japan_census_control.py` at build): the
2021 census counts **723** 飲食店 establishments in 13206
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 1,297 distinct placed
Food-service premises is **1.79 per establishment**, inside the built cities'
1.56-1.92.

### Personal services: the three registers

| Register | Rows | Census 2021 (9-1A) | Estimate (census x Hachiōji's licensed-to-census ratio) | Share |
|---|---|---|---|---|
| 理容所台帳 (barbers) | **101** | 105 | 118 | **86%** (80% on all Tokyo's ratio) |
| 美容所台帳 (beauty) | **263** | 190 | 298 | **88%** (65%) |
| クリーニング所台帳 (laundry) | **87** of 88 (取次所 56, 一般 31; 無店舗取次店 1 left out) | 96 | 168 | **52%** (57%) |

No official per-city count exists for a Tama city (e-Stat's 衛生行政報告例
lists Hachiōji alone), so the shares are estimates: the census count times
Hachiōji's ratio of licensed premises to census establishments (277/247,
807/514, 264/151), Tokyo's (7,328/6,122, 28,589/13,455, 8,147/5,137) beside
it. 確認年月日 run from 1964, 1973 and 1964 to 2026: **standing registers**,
not a stream, so the permits' skew does not reach them. 1 repeat of
(address, name) in the beauty register; 13 addresses carry both a barber and a
beauty salon. The 無店舗取次店 row reads as not a premises through `無店舗`.

### MHLW's Tokyo file (13000): the rows the ledgers lack (call 169)

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv`:
**3,606,399 B, 10,003 rows**, UTF-8 with BOM, the national schema. ⚠️
**市区町村名 reads 新宿区 on every row** (the registering office); the premises'
city is in 営業施設所在地, so the build filters by address, never by 市区町村名.
MHLW publishes no per-city file for 13206 (the check below expects HTTP 404).

- **462 rows in Fuchū** (届出 326, 許可 132, 許可(廃業) 4), 許可年月日 2021-08 to
  2026-08, 460 with their own point. Open restaurant permits 102.
- **Against the ledgers** (parsed town and first number, then the trade name,
  NFKC): of **132 open permits**, 98 are in a ledger by (town, number), 80 also
  by trade name; **34 are not** (**Food service 16, Retail 13**, out 4, mobile
  1; 52 by the stricter trade-name match: 27, 18, 5, 2). The 43 restaurant
  permits missing by trade name were permitted 2021-2026. Of **326 open
  notifications**, 192 are in a ledger by (town, number); **134 are not**
  (**Retail 61**, out 72: vending, catering, manufacturing; mobile 1). The 4
  closed rows are left out.
- **So call 169 adds about 16 restaurants and 74 shops here** (by (town,
  number); up to 27 and 116 by the trade-name match). The build's
  `SUPERSEDES` pass decides the exact figure; the stated 57.6% excludes them.
- **Its own coordinates against the block point**: median **33 m**, 94.6%
  within 250 m (406 rows). MHLW's own point is used where the block join
  misses (Ichinomiya's call 127c).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13206-24.0a.zip` (124,713 B,
**5,158 block keys**), town-chōme `.../19.0b/13206-19.0b.zip` (6,841 B,
**147**), both in `data/fuchu_tokyo/raw/isj/` and nothing else there (⚠️
`load_city_isj` globs its directory, and `data/tokyo_tama/raw/isj/` holds four
other municipalities' pairs all keyed under ward ""). `japan.CITIES` entry at
build: `"fuchu_tokyo": {"name": "府中市", "pref": "13", "epsg": 32654, "n02":
"25", "rules": WAVE2_RULES, "wardless": True, "wards": ["13206"]}`.

| Tier, today's shared code | Rows | Block | Town-chōme | Unplaced |
|---|---|---|---|---|
| **Permits and registers** | 2,126 | **97.3%** | 2.7% | 0 |
| … Food service / Retail (permits) | 1,318 / 357 | 96.9% / 96.9% | 3.1 / 3.1 | 0 |
| … Barbers / beauty / laundry | 101 / 263 / 87 | 99.0% / 98.9% / 98.9% | 1.0 / 1.1 / 1.1 | 0 |
| Notifications, Retail (after the `自動車以外` fix) | 630 | 94.0% | 5.7% | 0.3% (2) |
| **All, with the notifications** | 2,756 | **96.6%** | 3.4% | 0.1% (2) |

**The misses, read** (towns only, by `misses.py` over every ledger row of the
city: 3,160 rows, 96.8% block):
- **Chōme tier (95 of all rows)**: **宮町1丁目 79**, a large mixed-use complex
  beside 府中 station whose 番地 MLIT's block file does not hold, so its shops
  take the chōme's centroid (the build checks that distance in a scratch
  render); 本宿町1丁目 10 and 西府町1丁目 5 (`N番地のN` numbers the file
  lacks); 白糸台1丁目 1.
- **Unplaced (5 of all rows, 2 bucketed)**: one university-campus address the
  parser reads as 幸町35丁目 (a hyphen form with no chōme in the file), one
  written "…周辺" (near), and three area-wide rows (都内一円, a list of
  neighbouring cities, a blank town) that are not premises. No shared rule is
  proposed.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_13_GML.zip`, N03 code 13206
(**29.42 km²**, extent W 139.430, S 35.646, E 139.526, N 35.700; centroid
139.483, 35.671). Read with `stub_test()`'s method and an in-memory `CITIES`
entry (scratch `rail.py`, `near_line.py`).

| N02 line (operator, class) | Public name | Stations inside / on the line | Stations inside |
|---|---|---|---|
| 京王線 (京王電鉄, 12) | Keiō Line | **6 / 35** | 中河原, 分倍河原, 府中, 東府中, 多磨霊園, 武蔵野台 |
| 競馬場線 (京王電鉄, 12) | Keiō Keibajō Line | **2 / 2** (the whole line) | 東府中, 府中競馬正門前 |
| 南武線 (東日本旅客鉄道, 11) | JR Nambu Line | **3 / 30** | 西府, 分倍河原, 府中本町 |
| 武蔵野線 (東日本旅客鉄道, 11) | JR Musashino Line | **2 / 27** | 府中本町 (its terminus), 北府中 |
| 多摩川線 (西武鉄道, 12) | Seibu Tamagawa Line | **4 / 6** | 多磨, 白糸台, 競艇場前, 是政 (its terminus) |

- **17 station records, 14 N02_005g groups**: 分倍河原 (Keiō and JR, 61 m
  span), 府中本町 (Nambu and Musashino, 17 m) and 東府中 (Keiō Line and Keibajō
  Line) are one group each; every other group is one line's station. **No pair
  of distinct names closer than 290 m** (白糸台, Seibu, and 武蔵野台, Keiō: two
  names, two groups, kept apart by the group-code rule, no owner question).
  **Median nearest-group gap 784 m** (290 to 1,356): rings by the spacing rule
  at build.
- **The one-station rule (calls 54, 92, 163, 165, 167): no line has one
  station in the city.** The Keibajō Line lies wholly inside (2 of 2); every
  other line keeps 2 to 6. No stub, no left-out line, no owner question.
- **Near the line, outside**: 西国分寺 (JR Chūō and Musashino lines, 国分寺市)
  248-258 m outside and 南多摩 (JR Nambu, 稲城市) 258 m outside. Neither gets a
  ring (standing call 3); the Chūō Line is not drawn (no station inside). A
  business near them goes to its nearest station inside the city.
- **Cut at the line**: the Keiō Line 29 beyond (調布市 8, 世田谷区 7, 日野市 4,
  渋谷区 3, 八王子市 3, 新宿区 2, 杉並区 1, 多摩市 1); the Nambu Line 27 (Kanagawa 20,
  稲城市 3, 国立市 2, 立川市 2); the Musashino Line 25 (other prefectures 22,
  東村山市 1, 小平市 1, 国分寺市 1); the Tamagawa Line 2 (武蔵野市 1, 小金井市 1).
- **The light-rail/rail test**: every drawn line is heavy rail (JR class 11,
  private class 12). No subway, monorail, tram or light rail.
- **Frequency, read 2026-10-06 from the operators' own timetables** by plain
  GET with the project user-agent; every departure on each page counted, marked
  ones included:

  | Station (line, direction) | Weekday departures | Per hour 07-18 | 10-16, longest gap |
  |---|---|---|---|
  | 府中本町 (Nambu, to 立川 / to 登戸・川崎) | 137 / 138 | 5-12 | 10 min |
  | 分倍河原 (Nambu, to 立川 / to 登戸・川崎) | 137 / 138 | 5-12 | 10 min |
  | 西府 (Nambu, to 立川 / to 登戸・川崎; rapids pass) | 125 / 126 | 5-12 | 12-13 min |
  | 府中本町 (Musashino, to 西船橋; the terminus) | 120 | 5-9 | 13 min |
  | 北府中 (Musashino, to 西船橋 / to 府中本町) | 120 / 124 | 5-12 | 12-13 min |
  | 多磨, 白糸台 (Tamagawa, to 武蔵境 / to 是政) | 89 / 89-90 | 5 | every 12 min |
  | 是政 (Tamagawa, to 武蔵境; the terminus) | 87 | 5 | every 12 min |

  JR East: `timetables.jreast.co.jp/timetable/list1374.html` (府中本町),
  `list1385.html` (分倍河原), `list1724.html` (西府), `list0585.html` (北府中),
  weekday pages `2610/timetable/tt<code>/<code>010.html`, `…020.html` and
  `…030.html`, counted per `timetable_time` cell (the jre.py trap). The Nambu
  Line's station codes came from the host's own station search by line
  (`cgi-bin/st_search.cgi?mode=0&rosen=53`, a plain GET). Seibu:
  `seibu.ekitan.com/norikae/timetable/station/236-2|236-3|236-5/d1|d2?dw=0`
  (the station-line codes from Seibu's timetable script, as Higashimurayama's
  brief found them), each train counted once per service date
  (`openOneTrainTimetable`, 2026-10-07).
- **Keiō: ASSERTED, not read.** Keiō's timetables are a NAVITIME app
  (`transfer-train.navitime.biz/keio/…`) that renders in the browser; curl
  gets a 2.7 KB shell with no departures (the J6 probe's page). The Keiō Line
  runs several trains an hour at every station here (the probe). ⚠️ **The
  Keibajō Line (東府中 to 府中競馬正門前, a racecourse branch) is the one drawn
  line whose weekday count is not known**: the build reads it (a whole-page
  reader, every marked train counted) or records it as ASSERTED on the page's
  internal notes; if it runs at about 11 trains a day or fewer, the page names
  that stretch (call 86). It is drawn either way.
- **No stretch read is at or under about 11 trains a day** (call 86). Counts
  only; no timetable on the page.
- ⚠️ **Gate 3** at build: the operators' station counts inside the city (Keiō
  8 records in 7 groups, JR East 5 records in 4, Seibu 4). **OSM `name:en`**
  for 14 groups (one Overpass query at build, in the box below; not queried
  here).

## Scope

**Fuchū City (Tokyo).** The Keiō Line runs on to 新宿 and 八王子, the Nambu
Line to 川崎 and 立川, the Musashino Line to 西船橋, the Tamagawa Line to 武蔵境;
cut at the line. The Tokyo page covers the 23 special wards only; Fuchū is its
own page (the band).

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
  measurement sources, not drawn. **The operators' timetables**: read for
  counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here. The Tama ledgers' row in
  `docs/data_sources/japan.md` is shared with the other Tama cities.

## Privacy

- **Dropped at read (call 109)**: 法人代表者氏名, 営業者住所 and 営業者ビル名 (the
  operator's own address), and every phone column (営業所電話番号, 営業者電話番号,
  施設TEL, 営業者TEL). Only 屋号 / 施設名称, the premises address and the type
  are ever selected; 営業者氏名 is read IN MEMORY for the name rule and never
  written.
- **The operator column, measured** (counts only): food permits 1,909,
  営業者氏名 filled on 1,227 (a company marker on 1,185, none on 42), blank on
  682; notifications 799, filled 633 (597 / 36), blank 166; barbers 101,
  filled 14 (13 / 1), blank 87; beauty 263, filled 93 (all companies), blank
  170; laundry 88, filled 58 (all companies), blank 30. The operator is
  published almost only for companies: the blanks are the shape of
  individuals withheld at source.
- **The name rule, version 2, measured in memory** (answers only, never a
  value): **4 rows withheld**, the same with or without 法人代表者氏名: in the
  permits 1 by the operator comparison (a type with no bucket, so off the map
  anyway); in the notifications **2 by the sign rule (both Retail)** and 1 by
  the operator comparison (no bucket). The registers 0. So **2 mapped rows are
  withheld**; the build confirms the count after step 2.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; its 法人名 joins
  the name rule for the rows call 169 brings in (owner, 2026-10-05).
- Run `check_personal_exposure.py fuchu_tokyo` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.430-139.526 E, centroid 139.483:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded out:
(35.64, 139.43, 35.71, 139.53). Scaffold with `scripts/scaffold_city.py ...
--page-number <N>`, the number claimed at build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band B with the
food share stated at the yearbook's date (call 188); the skew disclosed and
the three columns dropped at read (call 109, as the Tama cities in A); the
catalogue route and its credit (call 108); the notifications in as partial
Retail (call 127b, the Tama cities in A); `mode: metro` (precedent, call 170);
the minor tier and Japan East (Kanto after the retag); no frequency floor
(call 46); the `自動車以外` lookahead (named in the drafts entry for calls
154-184, Minato control at build).

**Answered by the owner on 2026-10-06:** call 188, **Band B, all three
buckets, the food share stated at the yearbook's date** (57.6%; raw 70.7%;
Kure's 58.5% of the in-force count the precedent; "187 and 188: B sounds
good"). Call 169, **MHLW's rows the ledgers lack added** for all Tama cities
(the Tokyo wards' precedent: the ledger's row kept where both hold a premises,
`SUPERSEDES`; MHLW's PDL 1.0 notice line; the stated share WITHOUT MHLW's
rows). The notification ledger read into Retail (decided for the four Tama
cities in A). The 2024 snapshot a cross-check only (call 147). Not re-opened.

**Open:** none. The one unknown is the Keibajō Line's weekday count, which
needs no owner call: the line is drawn either way, and named only if it reads
at about 11 trains a day or fewer (call 86).

## Personal services against Tokyo's yearbook table 19-7 (owner, call 189)

**Answered by the owner on 2026-10-06:** call 189, "fetch at once": Tokyo's statistical yearbook table 19-7 (環境衛生営業施設数, `https://www.toukei.metro.tokyo.lg.jp/tnenkan/2024/tn24qv190700.csv`, 6,876 B, HTTP 200, into `data/tokyo/raw/`; the publisher of table 19-8) gives the official count of each register at the end of FY2024 (2025-03-31). **It supersedes the census-scaled estimates above** for these three registers; the estimates are kept as the record.

| Register | Ledger rows (2026-08-31) | Confirmed on or before 2025-03-31 (確認年月日) | Yearbook FY2024 | Share, all rows | Share at the yearbook's date |
|---|---|---|---|---|---|
| Barbers (理容所) | 101 | 100 | 105 | 96.2% | **95.2%** |
| Beauty salons (美容所) | 263 | 240 | 270 | 97.4% | **88.9%** |
| Laundries (クリーニング所, storeless counters out) | 87 | 84 | 96 | 90.6% | **87.5%** |

The share at the yearbook's date is the one the page states, as the food share is (calls 187-188); it is a lower bound, since 確認年月日 is the confirmation date, which a change of operator renews. Measured by staging's scratch script `t197_measure.py` (counts only; operator, address and phone columns dropped at read); the build re-measures it in step 2.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): the `自動車以外` lookahead in `permits_from_rows`' vehicle test and
  in `japan_eigyo`'s temporary or mobile rule (54 rows here, 1,063 across the
  Tama ledgers). Nothing else: the columns are all known.
- The read: drop 法人代表者氏名, 営業者住所, 営業者ビル名 and the phones before
  `city_rows` hands rows on; `SOURCE_KIND` per register file (no type column
  in the barber and beauty ledgers); the city cut by address; `SOURCE_LINKS`
  for the slugs; `SOURCE_AS_OF` 2026-08-31 from the page.
- MHLW's slice: the 13000 file cut by 営業施設所在地, `SUPERSEDES` against the
  ledgers, its 法人名 through the name rule, its own point where the block join
  misses; the count it adds (about 16 restaurants and 74 shops here).
- `ISJ_DIR` holding only 13206's pair; the share and its control-date figure
  from `official_shares` (the yearbook's 2,188; 57.6% stated, measured, never
  typed), and the page's sentence from the approved template (calls 109,
  188); the census ratio (1.79).
- The Keibajō Line's weekday count (or ASSERTED); Keiō's frequencies (or
  ASSERTED); gate 3; OSM `name:en`; the labels at 分倍河原 and 府中本町 (two
  lines each) and on the two-station Keibajō Line; line colors on both
  basemaps; the opening view (`map-view`); the factory share;
  `check_provenance.py`; `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "fuchu_tokyo-ledger-page",
    "claim": "The Tama ledgers page names the five ledgers, their windows, the opt-out rule, and Fuchu under 多摩府中保健所",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["平成29年1月から令和8年8月までの新規許可施設", "令和3年6月から令和8年8月までの届出施設", "公表を希望しない施設", "多摩府中保健所（武蔵野市、三鷹市、府中市、調布市", "shokuhin-kyoka-7", "shokuhin-todokede-1-7", "kankyo-riyoujo-5", "kankyo-biyoujo-5", "kankyo-cleaning-5"]
  },
  {
    "id": "fuchu_tokyo-ledger-edition",
    "claim": "The edition measured here: the ledgers as of 2026-08-31 (a failure here means a new monthly edition: re-measure)",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["令和8年8月31日現在"]
  },
  {
    "id": "fuchu_tokyo-food-permits-file",
    "claim": "The food permit ledger (4,486,267 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-kyoka-7",
    "min_bytes": 2000000
  },
  {
    "id": "fuchu_tokyo-food-notifications-file",
    "claim": "The food notification ledger (1,956,304 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-todokede-1-7",
    "min_bytes": 1500000
  },
  {
    "id": "fuchu_tokyo-barber-file",
    "claim": "The barber ledger (165,277 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-riyoujo-5",
    "min_bytes": 100000
  },
  {
    "id": "fuchu_tokyo-beauty-file",
    "claim": "The beauty-salon ledger (608,582 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-biyoujo-5",
    "min_bytes": 400000
  },
  {
    "id": "fuchu_tokyo-laundry-file",
    "claim": "The laundry ledger (173,591 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-cleaning-5",
    "min_bytes": 100000
  },
  {
    "id": "fuchu_tokyo-catalogue-food",
    "claim": "Tokyo's catalogue entry t000055d0000000361 (食品関係営業台帳) declares CC BY 4.0 and points at the 保健医療局 ledger page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000361",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "fuchu_tokyo-catalogue-registers",
    "claim": "Tokyo's catalogue entry t000055d0000000614 (環境衛生施設台帳) declares CC BY 4.0 and points at the same page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000614",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "fuchu_tokyo-tokyo-terms",
    "claim": "The Tokyo Open Data Terms allow commercial use and prescribe a modified-use credit",
    "kind": "http_contains",
    "url": "https://portal.data.metro.tokyo.lg.jp/terms/",
    "present": ["商用利用も可能", "改変して利用", "編集・加工等を行った旨"]
  },
  {
    "id": "fuchu_tokyo-mhlw-tokyo",
    "claim": "MHLW's Tokyo Prefecture file (13000, 3,606,399 B) answers a plain keyless GET (call 169's rows)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "fuchu_tokyo-no-mhlw-city-file",
    "claim": "MHLW has no per-city file for 13206 (HTTP 404): the prefecture licenses Fuchu, so its rows sit in 13000",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13206_food_business_all.csv",
    "expect_status": 404
  },
  {
    "id": "fuchu_tokyo-isj-block-live",
    "claim": "MLIT's block-level address file for Fuchu (13206) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13206-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "fuchu_tokyo-isj-chome-live",
    "claim": "MLIT's town-chōme file for Fuchu (13206) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/13206-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "fuchu_tokyo-jr-fuchuhommachi-timetable",
    "claim": "JR East's timetable index for 府中本町 (list1374) links the three weekday pages counted (Musashino, Nambu both ways). ASCII ids only: the host sends no charset",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1374.html",
    "present": ["tt1374/1374010.html", "tt1374/1374020.html", "tt1374/1374030.html"]
  },
  {
    "id": "fuchu_tokyo-jr-nishifu-timetable",
    "claim": "JR East's timetable index for 西府 (list1724) links its two weekday Nambu Line pages (the thinnest JR station here, rapids pass)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1724.html",
    "present": ["tt1724/1724010.html", "tt1724/1724020.html"]
  },
  {
    "id": "fuchu_tokyo-jr-kitafuchu-timetable",
    "claim": "JR East's timetable index for 北府中 (list0585) links its two weekday Musashino Line pages",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0585.html",
    "present": ["tt0585/0585010.html", "tt0585/0585020.html"]
  },
  {
    "id": "fuchu_tokyo-seibu-tamagawa-timetable",
    "claim": "Seibu's weekday timetable for 多磨 on the Tamagawa Line toward 武蔵境 (236-2/d1), one of the pages counted",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/236-2/d1?dw=0",
    "present": ["多磨", "多摩川線", "平日", "ekptime"]
  },
  {
    "id": "fuchu_tokyo-seibu-koremasa-timetable",
    "claim": "Seibu's weekday timetable for 是政, the Tamagawa Line's terminus (236-5/d1)",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/236-5/d1?dw=0",
    "present": ["是政", "多摩川線", "ekptime"]
  },
  {
    "id": "fuchu_tokyo-projected-crs",
    "claim": "Fuchu (Tokyo) projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.48,
    "expect": "EPSG:32654"
  }
]
```
