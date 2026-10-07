# Hino — build brief

**Band B, owner-approved 2026-10-06** (Japan wave 4, measured from cached
files and moved from C to B by the owner, call 187: "187 and 188: B sounds
good"; `docs/decisions_drafts/staging.md`, "The last four Tama cities"): **all
three buckets, with the food share stated at the yearbook's date** (61.2%;
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
  `fetch_sources.py` places them in `data/hino/raw/`.
- **Downloaded for this brief** (the only download approved), from
  `nlftp.mlit.go.jp` by `japan_fetch.get` into `data/hino/raw/isj/`:
  `13212-24.0a.zip` (**84,446 B**) and `13212-19.0b.zip` (**6,345 B**).
  **90,791 B in all.**
- Read, not kept as data: the operators' timetable pages (counts only), and
  Tokyo's statistical-yearbook chapter page (`tn24q3i019.htm`, a page read; no
  table downloaded).

**Run `python scripts/brief_check.py hino` before writing any code.** Then the
`japan-city` skill, **Higashiyamato's shape**
(`docs/build_briefs/higashiyamato.md`: the same five ledgers cut by address,
MHLW's Tokyo file beside them), with `tama.md` (the same health centre,
南多摩保健所), `nishitokyo.md` and `higashimurayama.md` on the same files. Read the
`tokyo-ward` skill for Tokyo's catalogue sources and credits. Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`'s
own functions from a scratch script (`scripts/screen_japan_join.py` has no
entry; its table is shared code and was not edited). Rail: MLIT N02-25 cut at
the N03 city line, through `pipeline/countries/japan.py` with a scratch
`CITIES` entry.

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
the page states **61.2%** (633 restaurant permits first granted by 2025-03-31,
of the yearbook's 1,035), never the raw 77.7%. The ledgers' skew is disclosed
as for the four Tama cities in A (call 109): about a fifth of the rows opened
after the control date, the ledger misses long-standing premises (new permits
only from 2019-08), laundry about half, opt-outs and closures left out.
**法人代表者氏名, the operator's address and the phones are dropped at read**
(call 109).

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

**✅ `mode`: `metro`** (Tama's and Higashiyamato's precedent, call 170: private
heavy rail and a monorail read `metro`). **✅ Minor label tier and the Japan
sub-region (owner, 2026-10-02):** `label_tier: "minor"`, `"region": "Japan
East"` (`app/cities.py`); wave 4's first city to land retags Japan into the
eight regions, Hino into **Kanto**. Its dot sits among the other Tama cities:
the label offset from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and
1200), never by eye.

---

## The one-line summary

**All three buckets from the Tokyo Metropolitan Government's monthly Tama
ledgers (CC BY 4.0 through the catalogue route, relied on, call 108), cut to
Hino by address, as of 2026-08-31: 981 food permits (804 restaurants), 466
food notifications, 65 barbers, 171 beauty salons and 42 laundries.** The
restaurants are **77.7% of the 1,035 in force** (Tokyo's statistical
yearbook, table 19-8, FY2024), flattered: **171 (21.3%) were first permitted
after the control date**, so the share the page states is **61.2%** (call
187). Barbers about 88%, beauty salons about 78%, laundry counters about 60%
of census-scaled estimates (no official per-city count in hand). Through
`japan_eigyo`: **Food service 624 rows (618 pins), Retail 211 permit rows
(177 pins) plus 318 notification rows** (352 once the shared `自動車以外` trap
is fixed), **Personal services 277**; MHLW adds **8 Food-service and 32 Retail
rows** (call 169). **Block join 96.9%** of 1,430 bucketed rows, 1 unplaced.
**Rail: 10 N02 station groups**: Keiō 5 stations on two lines (the Keiō Line
4, the Dōbutsuen Line 2, 高幡不動 on both), the Tama Toshi Monorail 5 (two of
them shared with Keiō in one group each), JR Chūō 2; JR and the monorail READ
(nothing at or under 11 trains a day), Keiō ASSERTED (its timetables need
scripts).

---

## Business leg — the Tokyo Metropolitan Government's Tama ledgers

Page `https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho`
(東京都が設置している保健所等で保有する台帳一覧, 更新日 2026-09-14; UTF-8).
**Hino is 南多摩保健所's** (日野市, 多摩市, 稲城市; Tama's health centre). The
page: 「ホームページへの公表を希望しない施設、廃止・休止している施設は除いて公表しています」
and, for food,
「移動販売、臨時販売、自動車販売、自動販売機、行商、催事等期間短縮申請があったもの、届出が不要な施設及び廃業した施設は除いています」.

| Ledger (CSV, cp932) | Edition line on the page | Rows (all areas) | Rows in Hino |
|---|---|---|---|
| `shokuhin-kyoka-7` 食品関係営業台帳（許可） | 「平成29年1月から令和8年8月までの新規許可施設及び平成29年4月から令和8年8月までの許可更新施設（令和8年8月31日現在）」 | 28,093 | **981** |
| `shokuhin-todokede-1-7` 食品関係営業台帳（届出） | 「令和3年6月から令和8年8月までの届出施設（令和8年8月31日現在）」 | 12,502 | **466** |
| `kankyo-riyoujo-5` 理容所台帳 | 「令和8年8月31日現在、台帳に掲載されている施設」 | 1,427 | **65** |
| `kankyo-biyoujo-5` 美容所台帳 | as above | 4,319 | **171** |
| `kankyo-cleaning-5` クリーニング所台帳 | as above | 1,040 | **42** |

Files at `https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/<name>`.
⚠️ **The slugs carry a revision suffix** (`-7`, `-1-7`, `-5`) that may move
with a monthly edition: `fetch_sources.py` takes them from the page's links (a
`SOURCE_LINKS` regex) and pins `SOURCE_AS_OF` to 「令和8年8月31日現在」, never the
fetch date.

- **Assigning a row to the city**: the address starts 東京都日野市 (every row of
  the city's has an address). `permits_from_rows(rows, "東京都", "日野市",
  wardless=True)`.
- **Columns, and the shared tuples**: as Higashiyamato's brief lists them.
  **No shared-code change for the columns**; ⚠️ `OPERATOR_COLS` holds
  法人代表者氏名, so the read drops it before the name rule (measured cost: 0
  rows). No 業態 column: the bracketed sub-type carries the form, and
  `japan_eigyo` reads it.

### The food permit ledger (981 rows)

- **申請区分**: 新規 875, 更新 106. **Kinds**: 飲食店営業 804, 菓子製造業 83,
  食肉販売業 24, 魚介類販売業 23, そうざい製造業 13, 漬物 5, アイスクリーム類 5,
  密封包装 4, 喫茶店営業 3, 食肉処理 3, 豆腐 3, 麺類 2, … Restaurant sub-types:
  一般飲食店 541, 集団給食 96, そうざい店 66, 弁当屋 42, すし屋 17, そば屋 16, 仕出し屋 12,
  バー・キャバレー 7, 喫茶店 5, コンビニエンスストア等 2.
- **Against the yearbook** (table 19-8, FY2024, 日野市; `japan_official`):
  **飲食店営業 804 of 1,035, 77.7%**. 菓子 83 of 113, 食肉販売 24 of 46, 魚介類販売
  23 of 43, そうざい製造 13 of 12, 麺類 2 of 3, 豆腐 3 of 3.
- **The dates (the skew)**: restaurant 新規 rows were first permitted
  **2019-08-08 to 2026-08-28**; 更新 rows carry first permits from 1971-03 to
  2015-05. By first-permit year: 99 rows before 2021, then 145, 152, 135, 92
  (2021-2024), 102 in 2025 and 79 to 2026-08. **171 restaurant rows (21.3%)
  were first permitted after 2025-03-31**, so at the yearbook's control date
  the ledger holds **633, 61.2%** of the 1,035: **the share the page states**
  (call 187). Premises permitted before 2019-08 and not renewed since 2017-04
  are missing (Tama's brief reads the ledger-wide windows).
- **Old-law permits are in the ledger** (not Kurashiki's trap): 喫茶店営業 3
  rows and 更新 rows first permitted 1971-2015.
- **Duplicates**: 8 exact repeats of (address, trade name, kind); 114 rows
  repeat an (address, trade name) under another kind; **867 distinct
  premises**. One pin per premises and bucket (trap 7). No blank 屋号.
- **Closures are left out at source**; the page keeps "may include closed
  premises".

### The food notification ledger (466 rows)

- 届出年月日 1974-04-20 to 2026-08-24 (41 before 2021, 213 in 2021, then 56,
  55, 43, 35 and 23 to 2026-08); types: その他の食料・飲料販売業 152 (店舗 82, 包装
  44, 電子申請 26), 集団給食施設 79, コンビニエンスストア 75, 百貨店、総合スーパー 32,
  乳類販売業 31, 野菜果物販売業(自動車以外) 18, 弁当販売業(自動車以外) 16, packaged
  meat 13 and fish 11, コーヒー製造 10, …
- **Against the yearbook's columns**: コンビニエンスストア **75 of 75**,
  百貨店・総合スーパー **32 of 34**, 野菜果物販売業 18 of 20, 弁当販売業 16 of 17,
  米穀類 4 of 7, 集団給食施設 79 of 88, 乳類販売業 **31 of 89** (old-law dairy
  permits never re-filed). Near complete for the shops a reader sees, partial
  for dairy: disclosed as partial.
- ⚠️ **The `自動車以外` trap (shared code)**: 野菜果物販売業(自動車以外) 18 and
  弁当販売業(自動車以外) 16 are read as **mobile** by `permits_from_rows` (a bare
  `自動車` test) and by `japan_eigyo`. Measured here: **34 rows**, all Retail
  once fixed (33 block, 1 chōme). The fix is Higashiyamato's (`自動車(?!以外)` in
  both tests, then the Minato control and every city screen).

### Counts through `japan_eigyo` (fixed premises, today's shared code)

**Food service 624** (一般飲食店 541, 弁当屋 42, すし屋 17, そば屋 16, 喫茶店 5,
喫茶店営業 3; **618 pins**). **Retail from the permits 211** (菓子 83, そうざい店
66, 食肉 24, 魚介 23, そうざい製造 13, コンビニエンスストア等 2; **177 pins**). **Retail
from the notifications 318** (227 pins; **352 rows after the `自動車以外`
fix**). Left out: institutional catering 96 + 79, event catering 12, hostess
venues 7 (バー・キャバレー, `docs/category_rules.md` R3), not a premises 34
(the trap above), mail order 1, and 31 + 34 types with no rule (漬物,
アイスクリーム, 密封包装, コーヒー製造, 調味料, …), as in every built city.

**Economic Census control** (`scripts/japan_census_control.py` at build): the
2021 census counts **366** 飲食店 establishments in 13212
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 617 distinct placed
Food-service premises is **1.69 per establishment**, inside the built cities'
1.56-1.92.

### Personal services: the three registers

| Register | Rows | Census 2021 | Estimate (census x Hachiōji's licensed-to-census ratio) | Share |
|---|---|---|---|---|
| 理容所台帳 (barbers) | **65** | 66 | 74 | **88%** (82% on all Tokyo's ratio) |
| 美容所台帳 (beauty) | **171** | 139 | 218 | **78%** (58%) |
| クリーニング所台帳 (laundry) | **42** (取次所 29, 一般 12, リネン 1); 41 bucketed | 40 | 70 | **60%** (66%) |

No official per-city count is in hand for a Tama city (e-Stat's 衛生行政報告例
lists Hachiōji alone), so the shares are estimates (the band row's figures,
reproduced). Tokyo's yearbook does list a table **19-7 環境衛生営業施設数**
(`/tnenkan/2024/tn24qv190700.csv`, 6.7 KB, the same size and publisher as
19-8's per-municipality CSV), likely per municipality; **not downloaded** (not
named in the approval): open call 1. 確認年月日 run from 1966 (barbers), 1968
(beauty) and 1966 (laundry) to 2023-2026: **standing registers**, not a
stream. No repeats of (address, name); 13 addresses carry both a barber and a
beauty salon. The beauty register is ordinary in shape: 159 distinct
addresses for 171 salons, 40 confirmed since 2020. The リネン row is left out
by `japan_eigyo`.

### MHLW's Tokyo file (13000): the control, and call 169's rows

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv`
(**3,606,399 B, 10,003 rows**, UTF-8 with BOM). ⚠️ **市区町村名 reads 新宿区 on
every row** (Higashiyamato's finding): the build filters by 営業施設所在地,
never by 市区町村名. The city-code file (`13212_food_business_all.csv`) answers
**HTTP 404** (brief check below).

- **285 rows in Hino** (届出 207, 許可 78), dated 2021-10 to 2026-06, every one
  with its own point. Open restaurant permits 54.
- **Against the ledgers** (Higashiyamato's match: parsed town, number and
  trade name; notifications on town and number): of 78 open permits, 62 are in
  a ledger by (town, number, trade name), 70 by (town, number). Of 207 open
  notifications, 161 are in a ledger by (town, number).
- **The rows the ledgers lack, by bucket (call 169)**: permits **Food service
  8, Retail 7**, out 1; notifications **Retail 25**, out 21 (vending,
  catering, manufacturing). **40 rows bucketed**; their own point against the
  block point: **median 38 m, 88.2% within 250 m** (34 rows). The build keeps
  the ledger's row where both hold a premises (`SUPERSEDES`), takes MHLW's own
  point where the join misses (call 127c), and leaves them out of the stated
  share.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13212-24.0a.zip` (84,446 B,
**4,718 block keys**), town-chōme `.../19.0b/13212-19.0b.zip` (6,345 B,
**112**), in `data/hino/raw/isj/` and nothing else there (`load_city_isj`
globs its directory: one ISJ directory per city). `japan.CITIES` entry at
build: `"hino": {"name": "日野市", "pref": "13", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["13212"]}`.

| Tier, today's shared code | Rows | Block | Town-chōme | Unplaced |
|---|---|---|---|---|
| **Permits and registers** | 1,112 | **97.3%** | 2.6% | 0.1% (1) |
| … Food service / Retail (permits) | 624 / 211 | 97.9% / 95.7% | 1.9 / 4.3 | 0.2 (1) / 0 |
| … Barbers / beauty / laundry | 65 / 171 / 41 | 98.5% / 96.5% / 97.6% | 1.5 / 3.5 / 2.4 | 0 |
| Notifications, Retail | 318 | 95.6% | 4.4% | 0 |
| **All, with the notifications** | 1,430 | **96.9%** | 3.0% | **0.1% (1)** |
| All after the `自動車以外` fix | 1,464 | 96.9% | 3.0% | 1 |
| MHLW's extra rows (call 169) | 40 | 85.0% | 10.0% | 2 (own point) |

**The misses, read** (towns only): the 43 chōme-tier rows are `N番地のN` /
`N番地` addresses in Hino's 地番 towns, whose numbers MLIT's block file does
not hold: 日野 13, 落川 9, 高幡 9, 宮 4, 新井 2, 豊田2丁目 2, 川辺堀之内 2, 上田 1,
万願寺4丁目 1. Each takes its town's centroid. **Unplaced (1)**: an address
written 高幡3丁目, a chōme MLIT's files do not hold. No rule is proposed (one
row; a city-local alias at most, with the Minato control).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_13_GML.zip`, N03 code 13212
(**27.54 km²**, extent W 139.357, S 35.639, E 139.442, N 35.692; centroid
139.399, 35.663). Read with `stub_test()`'s method and an in-memory `CITIES`
entry (scratch `rail.py`).

| N02 line (operator, N02_002 class) | Public name | Stations inside / on the line | Stations inside |
|---|---|---|---|
| 京王線 (京王電鉄, 4) | Keiō Line | **4 / 35** | 百草園, 高幡不動, 南平, 平山城址公園 |
| 動物園線 (京王電鉄, 4) | Keiō Dōbutsuen Line | **2 / 2** (the whole line) | 高幡不動, 多摩動物公園 |
| 多摩都市モノレール線 (多摩都市モノレール, 5) | Tama Toshi Monorail | **5 / 19** | 甲州街道, 万願寺, 高幡不動, 程久保, 多摩動物公園 |
| 中央線 (JR East, 2) | JR Chūō Line | **2 / 75** | 日野, 豊田 |

- **13 station records, 10 N02_005g groups**: **高幡不動** is one group across
  the Keiō Line, the Dōbutsuen Line and the monorail (222 m spread), and
  **多摩動物公園** one across the Dōbutsuen Line and the monorail (190 m). No pair
  of groups is closer than 600 m (median nearest-station gap **1,176 m**, 790
  to 1,633): rings by the spacing rule at build. No Shinkansen.
- **The one-station rule (calls 54, 92, 163, 165, 167)**: **no line has one
  station in the city.** The Keiō Line keeps 4 of 35, the monorail 5 of 19,
  the Chūō Line 2 of 75; the **Dōbutsuen Line lies wholly inside** (2 of 2,
  高幡不動 to 多摩動物公園) and is drawn whole, with its own permanent label and
  legend entry (a 2 km branch: measure the label in a scratch render).
- **Near the line, outside**: Keiō's 長沼 **287 m outside** and the monorail's
  中央大学・明星大学 **312 m outside**, both in 八王子市. Neither gets a ring here
  (standing call 3).
- **Cut at the line**: the Keiō Line's 31 beyond (調布市 8, 世田谷区 7, 府中市 6,
  八王子市 3, 渋谷区 3, 新宿区 2, 杉並区 1, 多摩市 1); the monorail's 14 (立川市 7,
  八王子市 3, 東大和市 3, 多摩市 1); the Chūō Line's 73 (立川市 2, 八王子市 3, … to
  東京 and 大月).
- **The light-rail/rail test**: the monorail is N02 class 5, a straddle
  monorail on its own viaduct (rail, as the Maihama Resort Line, call 53); Keiō
  (class 4) and JR (class 2) are heavy rail. No tram.
- **Frequency, read 2026-10-06 from the operators' own timetables** by plain
  GET with the project user-agent; every departure on each page counted,
  marked ones included:

  | Station (line, direction) | Weekday departures | Per hour 07-18 |
  |---|---|---|
  | 日野 (JR Chūō, to 八王子・大月 / to 新宿・東京) | 197 / 187 | 8-16 / 8-15 |
  | 豊田 (JR Chūō, to 八王子・大月 / to 新宿・東京) | 161 / 187 | 6-11 / 7-15 |
  | Monorail, each of the 5 stations, each way | 123-128 | 6-10 |
  | Keiō Line (4 stations), Dōbutsuen Line (2) | **ASSERTED** | several an hour |

  JR East: `timetables.jreast.co.jp/2610/timetable/tt1328/…` (日野) and
  `tt1069/…` (豊田), the October 2026 edition, counted from each
  `timetable_time` cell (豊田's up count includes trains starting from its
  depot). Monorail: the station PDFs `TT5`-`TT9` linked from each station's
  timetable page, read with `pdftotext`; their header carries the revision
  dates 2022-03-12 and 2023-03-20; one PDF's 10:00 row runs together in the
  text, so its 07-18 minimum is read from the others. **Keiō: ASSERTED, not
  read**: its timetables are a NAVITIME app (`transfer-train.navitime.biz/keio/…`)
  that renders in the browser, so curl gets no departures (Tama's brief; the
  wave-5 probe's saved page is a 2.7 KB shell). As stated by the probe: Keiō
  at every station here several trains an hour all day, the Dōbutsuen Line a
  shuttle; **no stretch is expected at or under about 11 trains a day** (call
  86). ⚠️ The build reads the counts (a whole-page reader, counting marked
  trains: the jre.py trap) or records them as ASSERTED on the page's internal
  notes. Counts only; no timetable on the page.
- ⚠️ **Gate 3** at build: the operators' station counts inside the city (Keiō
  5 distinct stations, monorail 5, JR 2). **OSM `name:en`** for 10 groups (one
  Overpass query at build; not queried here).

## Scope

**Hino City.** The Keiō Line runs on to 新宿 and 京王八王子, the monorail north
over the Tama River to 立川 and 上北台 and south to 多摩センター, the Chūō Line to
東京 and 大月; all cut at the line. The Dōbutsuen Line is wholly inside. Hino
is its own page (the band).

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
- **The operator column, measured** (counts only): food permits 981, 営業者氏名
  filled on 603 (a company marker on 592, none on 11), blank on 378;
  notifications 466, filled 346 (330 / 16), blank 120; barbers 65, filled 11,
  beauty 171, filled 60, laundry 42, filled 29 (all companies). The operator is
  published almost only for companies.
- **The name rule, version 2, measured in memory**: **3 rows withheld** (food
  permits 2, by the operator comparison; notifications 1, by the sign rule),
  the same with or without 法人代表者氏名 (dropping it costs 0). The registers
  withhold none.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; its 法人名 joins
  the name rule for the rows call 169 brings in (owner, 2026-10-05).
- Run `check_personal_exposure.py hino` (`japan=True`) after step 2: it must
  print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.357-139.442 E, centroid 139.399:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded out:
(35.63, 139.35, 35.70, 139.45). Scaffold with `scripts/scaffold_city.py ...
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
buckets, with the food share stated at the yearbook's date**; Hino's is
**61.2%** (raw 77.7%); Kure's 58.5% of the in-force count is the precedent.
Not to be re-opened.

**Decided by precedent here (no owner question):** 高幡不動 and 多摩動物公園 each
one station across their lines (N02's own groups); the Dōbutsuen Line drawn
whole.

**Open, with a recommendation:**

1. **Fetch Tokyo's yearbook table 19-7 (環境衛生営業施設数).**
   `https://www.toukei.metro.tokyo.lg.jp/tnenkan/2024/tn24qv190700.csv`
   (6.7 KB), the same publisher and terms as table 19-8. *Recommend yes*, once
   for every Tama city (Tachikawa's beauty count needs it most): if it holds
   理容所, 美容所 and クリーニング所 per municipality, Hino's personal-services
   shares become official counts rather than census-scaled estimates. Tradeoff:
   one more measurement-only file and re-stated shares for the Tama cities;
   without it, Hino's estimates (88%, 78%, 60%) stand as the band row has them.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): the `自動車以外` lookahead in `permits_from_rows`' vehicle test and
  in `japan_eigyo`'s temporary or mobile rule (34 rows here). Nothing else: the
  columns are all known.
- The read: drop 法人代表者氏名, 営業者住所, 営業者ビル名 and the phones before
  `city_rows` hands rows on; `SOURCE_KIND` per register file; the city cut by
  address; `SOURCE_LINKS` for the slugs; `SOURCE_AS_OF` 2026-08-31 from the
  page.
- MHLW's rows (call 169): the `SUPERSEDES` match, MHLW's own point where the
  join misses, its 法人名 in the name rule, its notice line; the stated share
  without them.
- `ISJ_DIR` holding only 13212's pair; the share and its control-date figure
  from `official_shares` (the yearbook's 1,035: **61.2% stated**, measured,
  never typed); the census ratio (1.69).
- Keiō's frequencies (or ASSERTED on the internal notes); the Dōbutsuen Line's
  label; gate 3; OSM `name:en`; line colors on both basemaps; the opening view
  (`map-view`); the factory share; `check_provenance.py`;
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "hino-ledger-page",
    "claim": "The Tama ledgers page names the five ledgers, their windows, the opt-out rule, and Hino under 南多摩保健所",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["平成29年1月から令和8年8月までの新規許可施設", "令和3年6月から令和8年8月までの届出施設", "公表を希望しない施設", "南多摩保健所（日野市、多摩市、稲城市）", "shokuhin-kyoka-7", "shokuhin-todokede-1-7", "kankyo-riyoujo-5", "kankyo-biyoujo-5", "kankyo-cleaning-5"]
  },
  {
    "id": "hino-ledger-edition",
    "claim": "The edition measured here: the ledgers as of 2026-08-31 (a failure means a new monthly edition: re-measure)",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["令和8年8月31日現在"]
  },
  {
    "id": "hino-food-permits-file",
    "claim": "The food permit ledger (4,486,267 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-kyoka-7",
    "min_bytes": 2000000
  },
  {
    "id": "hino-food-notifications-file",
    "claim": "The food notification ledger (1,956,304 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-todokede-1-7",
    "min_bytes": 1500000
  },
  {
    "id": "hino-barber-file",
    "claim": "The barber ledger (165,277 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-riyoujo-5",
    "min_bytes": 100000
  },
  {
    "id": "hino-beauty-file",
    "claim": "The beauty-salon ledger (608,582 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-biyoujo-5",
    "min_bytes": 400000
  },
  {
    "id": "hino-laundry-file",
    "claim": "The laundry ledger (173,591 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-cleaning-5",
    "min_bytes": 100000
  },
  {
    "id": "hino-catalogue-food",
    "claim": "Tokyo's catalogue entry t000055d0000000361 (食品関係営業台帳) declares CC BY 4.0 and points at the 保健医療局 ledger page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000361",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "hino-catalogue-registers",
    "claim": "Tokyo's catalogue entry t000055d0000000614 (環境衛生施設台帳) declares CC BY 4.0 and points at the same page",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000614",
    "present": ["CC-BY-4.0", "hokenjo_daicho"]
  },
  {
    "id": "hino-tokyo-terms",
    "claim": "The Tokyo Open Data Terms allow commercial use and prescribe a modified-use credit",
    "kind": "http_contains",
    "url": "https://portal.data.metro.tokyo.lg.jp/terms/",
    "present": ["商用利用も可能", "改変して利用", "編集・加工等を行った旨"]
  },
  {
    "id": "hino-mhlw-tokyo",
    "claim": "MHLW's Tokyo Prefecture file (13000, 3,606,399 B) answers a plain keyless GET: the control and call 169's rows",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13000_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "hino-no-mhlw-city-file",
    "claim": "MHLW has no per-city file for 13212 (HTTP 404): the prefecture licenses Hino",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13212_food_business_all.csv",
    "expect_status": 404
  },
  {
    "id": "hino-isj-block-live",
    "claim": "MLIT's block-level address file for Hino (13212, 84,446 B) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13212-24.0a.zip",
    "min_bytes": 60000
  },
  {
    "id": "hino-isj-chome-live",
    "claim": "MLIT's town-chōme file for Hino (13212) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/13212-19.0b.zip",
    "min_bytes": 4000
  },
  {
    "id": "hino-yearbook-19-7",
    "claim": "Tokyo's yearbook chapter 19 lists table 19-7 (環境衛生営業施設数) as a CSV beside 19-8: the source open call 1 asks for (ASCII anchors)",
    "kind": "http_contains",
    "url": "https://www.toukei.metro.tokyo.lg.jp/tnenkan/2024/tn24q3i019.htm",
    "present": ["tn24qv190700.csv", "tn24qv190800.csv"]
  },
  {
    "id": "hino-jr-timetables",
    "claim": "JR East's 日野 station list links the two weekday timetables counted here, the October 2026 edition (a failure means a new edition: re-count)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1328.html",
    "present": ["2610/timetable/tt1328/1328010.html", "2610/timetable/tt1328/1328020.html"]
  },
  {
    "id": "hino-monorail-timetable-page",
    "claim": "The monorail's 高幡不動 timetable page links its station PDF TT7 (ASCII anchors: the host sends no charset)",
    "kind": "http_contains",
    "url": "https://www.tama-monorail.co.jp/monorail/station/takahatafudo/timetable.html",
    "present": ["station/TT7.pdf"]
  },
  {
    "id": "hino-monorail-timetable-pdf",
    "claim": "The monorail's 高幡不動 timetable PDF (TT7, 346,118 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.tama-monorail.co.jp/monorail/station/TT7.pdf",
    "min_bytes": 200000
  },
  {
    "id": "hino-projected-crs",
    "claim": "Hino projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.399,
    "expect": "EPSG:32654"
  }
]
```
