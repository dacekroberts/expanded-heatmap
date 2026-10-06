# Akita — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 81: `docs/decisions_drafts/staging.md`, "Wave 5: the ranked queue and
the pre-verdicts screened"). The Step 0 downloads were approved by the owner
2026-10-06 (call 106). **Step 0 measured 2026-10-06** (staging). Into
`data/akita/raw/` (gitignored), each from its publisher's own host with the
project user-agent, each HTTP 200, under each URL's own file name as
`japan_fetch.get` saves:

- From `www.city.akita.lg.jp` (秋田市保健所 衛生検査課): the food list
  `r081001.xlsx` (357,939 B, as of 2026-10-01); the barber and beauty
  registers `riyou260831_2.xlsx` (43,530 B) and `biyou260831_2.xlsx`
  (370,732 B), as of 2026-08-31.
- From `i2fas.mhlw.go.jp`: `05201_food_business_all.csv` (545,307 B), a
  control only.
- From `nlftp.mlit.go.jp`: `isj/05201-24.0a.zip` (319,917 B) and
  `isj/05201-19.0b.zip` (13,214 B).

**1,650,639 B in all.** Nothing else was downloaded. **No laundry list
exists** (below): the page discloses the gap.

**Run `python scripts/brief_check.py akita` before writing any code.** Then
the `japan-city` skill, **Fukuyama's shape** for a complete city list with
MHLW as a control (`docs/build_briefs/fukuyama.md`), but simpler: Akita's
food list is ONE file of every permit in term on its date, refreshed monthly,
so no `rebuilt_register` and no months to merge. Hamamatsu's for the
registers (one file per kind). Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py` from scratch scripts
only (`scripts/screen_japan_join.py` has no Akita entry; its table is shared
code and was not edited). Rail: MLIT N02-25 cut at the N03 city line,
measured through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; the Akita Shinkansen runs over the Ōu Line's track and N02 files
it as 奥羽線, so no station drops: 秋田 stays as a conventional station); (2)
**lines served only by limited expresses DO count** (2026-09-28); (3) **the
city line only**: only stations inside the city get rings, JR and the private
lines are cut at the line, **a one-station stub stays as cut** (2026-09-27);
an URBAN line cut to ONE station is left out, its station kept through the
other lines, and drawn cut only where no other line serves that station
(owner, 2026-10-06, calls 54 and 92); (4) **菓子製造業 and そうざい製造業
count, in Retail**, the factory share measured and kept (2026-09-24,
2026-09-27); (5) **the name rule**, version 2 (2026-10-06): a bare personal
name is withheld whatever the operator column holds; (6) **no page says
"currently operating"**. Also: no frequency floor for JR or private lines in
Japan (owner, 2026-10-06, call 46), any stretch at about 11 trains a day or
fewer named and drawn (call 86); fault-based cost clauses accepted for all of
Japan (2026-09-24); English station names from OSM `name:en`; every Japanese
city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The laundry gap (owner, 2026-10-06, the band row):** the city publishes
no laundry list, so Personal services is barbers and beauty salons only,
disclosed on the page and in What Is Excluded (the master list row: "Laundry
a disclosed gap").

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Akita
carries `label_tier: "minor"` and goes in the **Japan East** view (`app/cities.py`);
wave 4's first city to land retags Japan into the eight regions, Akita into
**Tohoku**. Its label offset comes from `check_macro_labels.py` (PROBLEMS 0
at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 ("unless there is
substantial JR, JR reads as metro"): JR East has all 12 station groups inside
the city line; no subway, tram or private railway. Fukuyama's, Okayama's and
Kitakyushu's precedent.

---

## The one-line summary

**Two of three buckets from the city's own XLSX files (CC BY 4.0 as stated;
the licence read is pending, staging records it).** The food list of every
permit in term on **2026-10-01** holds **4,041 rows, 3,139 restaurants
(飲食店営業), 98.2% of e-Stat's 3,195 in force**, old-law permits included
(not Kurashiki's trap). Barbers 420 and beauty salons 850 as of 2026-08-31:
**97.4% and 101.1% of official**; **no laundry list** (disclosed). Through
`japan_eigyo`: **Food service 2,764, Retail 720** fixed premises. Block join
**95.0%** (food), 91.7% (barbers), 96.2% (beauty); unplaced 1.0-1.4%.
MHLW's file holds about 5% of the city's permits: a control, not a source.
**Rail: 12 station groups**, all JR East (Ōu Main Line 8, Uetsu Main Line 5,
秋田 shared; the Oga Line's 追分 a JR one-station stub kept as cut), read from
JR East's own timetables: **never less than hourly 07-18, nothing at or
under 11 trains a day** (the thinnest, 桂根, 13 and 14).

---

## Business leg — the city's 衛生検査課 lists

Host `https://www.city.akita.lg.jp` (the city's own CMS; no catalogue API).
Every file is a plain GET under `/_res/projects/default_project/_page_/001/`.

### Food: 食品営業許可施設一覧, page 1017339

Page `https://www.city.akita.lg.jp/kurashi/kenko/1005368/1010019/1017339.html`
(更新日 2026-10-06): 「秋田市内における食品営業許可施設をオープンデータとして公開し、毎月更新しています。」

| File (under `…/001/017/339/`) | Bytes | Rows | What it is |
|---|---|---|---|
| `r081001.xlsx` 食品営業許可施設一覧（令和8年10月1日現在） | **357,939** | **4,041** | every permit in term on 2026-10-01; **monthly**, the file renamed each month (`r08MMDD.xlsx`) |

- **One sheet (`LICDATA`), header on row 1, no empty rows.**
  `japan_register.city_rows` reads all 4,041 as they stand. Dates are Excel
  serial integers (all 4,041 read; 許可期間（開始） 2020-02-14 to 2026-10-01,
  許可期間（満了） 2026-10-01 to 2033-09-30).
- **Columns**: **営業所名**, **営業所住所**, 営業所電話番号, **申請者名**,
  **申請区分** (継続 2,329 · 新規 1,712), **指令番号**, **業種名**, **業態名**,
  許可年月日, **許可期間（開始）**, **許可期間（満了）**. No operator address.
- **Against the shared tuples:** 営業所住所 is in `ADDR_COLS`, 業種名 in
  `TYPE_COLS`, 申請者名 in `OPERATOR_COLS`. **`NAME_COLS` lacks 営業所名**
  (without it every trade name reads empty and the name rule compares
  nothing) and **`FORM_COLS` lacks 業態名** (without it 16 temporary and
  vehicle permits at a street address read as restaurants). The scratch
  measurement renamed both in memory; the build adds them to the shared
  tuples (or a `source_rows` in the config) and re-runs the Minato control.
- **The month's file replaces the last.** `japan_fetch.current_url` takes a
  `SOURCE_LINKS` regex for the food key (`r08\d{4}\.xlsx`, Kawasaki's and
  Otsu's precedent), so a later build reads the current edition and pins
  `as_of` to the date in its title, never today.
- **Types**: 飲食店営業 3,139, 菓子製造業 312, そうざい製造業 206, 魚介類販売業
  123, 食肉販売業 77, 食肉処理業 36, 漬物製造業 36, 麺類製造業 16, … 29 types.
- **業態名** has six values: 一般 3,549, 仮設 216, 移動 145, 簡易 79, その他 36,
  仕出し・弁当 16. **No hostess-venue marker**: snack bars cannot be told
  apart and stay in Food service, as `docs/category_rules.md` R3 allows
  ("wherever the register names them").

### Old-law coverage (Kurashiki's trap) — not this list's problem

- **Old-law permits are in the file.** 206 rows (151 restaurants) began
  before 2021-06-01, from 2020-02-14, each ending 2026-10 to 2028-04. Old-law
  terms run 5.4 to 7.0 years (6.0 for 107 of 206), so every 6-year permit
  begun before 2020-10 has ended; the old-law starts thin out before
  2020-11 (2 to 4 a month) and run 27 and 32 in November and December 2020,
  then 35 to 69 a month after the law change.
- **The file is every permit in term on its date, under either law**: no
  許可期間（満了） before 2026-10-01 (184 end in 2026, 724 in 2027 …).
  継続 (renewal) is 2,329 of 4,041 rows: a renewed old-law premises carries a
  revised-law permit, as e-Stat counts it.
- **e-Stat 衛生行政報告例 FY2024** (`japan_official.estat()`), 秋田県秋田市,
  飲食店営業 in force 2025-03-31: **3,195** (old law 988, revised 2,207).
  The list's **3,139 restaurants are 98.2%** of it, vehicles and stalls
  included on both sides. Retail types against the same tables: 菓子 312 of
  316 (98.7%), 魚介類販売 123 of 128, 食肉販売 77 of 91, そうざい 206 (+4
  複合型) against 168.

### Duplicates and closed premises

- **Unique by (指令番号, 許可期間（開始）)**: 4,041 distinct. The number alone
  repeats (1,370 distinct): it restarts each year, so it is never a key on
  its own.
- **One premises, several permits**: 101 rows repeat an (address, trade
  name, type) in 65 groups; 3,503 distinct (address, trade name). One pin per
  premises and bucket (trap 7) leaves **3,337 pins from 3,484** bucketed
  fixed rows.
- **Closures are not marked** (no status column, no closure list), and the
  page does not say whether a closed premises leaves the monthly file. MHLW
  holds about 5% of the city's permits, too few for Fukuyama's closure
  filter. Its one closed permit (closed 2026-08) is not in the 2026-10-01
  file under its own start date. The page keeps "may include closed
  premises".

### Counts through `japan_eigyo` (fixed premises)

**Food service 2,764, Retail 720** (菓子 312, deli 210, fishmonger 121,
butcher 77; 3,484 storefront rows). Left out: **not a premises 345** (every
address reading 秋田市内 or 一円: vehicles and stalls licensed citywide, all
but 2 of them 業態 仮設 or 移動), temporary or mobile by 業態 361 (the same rows plus 16 at a
street address), event catering (仕出し) by 業態 16, vending 1, and 179
manufacturing types with no rule (食肉処理業 36, 漬物製造業 36, 麺類製造業 16,
…), as in every built city. **No konbini or supermarket**: their
notifications are not in the city's list (Toyota's "Retail thin").

**Economic Census control** (`scripts/japan_census_control.py` at build):
the 2021 census counts **1,283** 飲食店 establishments in 05201
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 2,705 distinct placed
Food-service premises is **2.11 per establishment**, ⚠️ **above the built
cities' 1.56-1.92**. Likely readings, for the build to test: premises that
closed without their permit lapsing (the list keeps a permit to its term),
and one premises under two trade names. Record the figure and the reading.

### MHLW's file (05201), a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=05201_food_business_all.csv`:
**545,307 B, 1,473 rows** (届出 1,225, 許可 245, 届出(廃業) 2, 許可(廃業) 1),
UTF-8 with BOM, the national schema (営業施設名称、屋号又は商号, 営業の種類,
業態, 営業施設所在地, 方書, 緯度 / 経度, 法人名, 法人番号, 法人住所, phones,
permit dates, 廃業年月日, 申請区分). **Cover 0.05**: 174 open restaurant
permits (169 addressed) of 3,195; permits 2020-07-28 to 2026-08-31.

- **Against the city's list**: 203 of its 245 open permits match a city row
  by number and start date (142 of 174 restaurants), 170 by (address, trade
  name). Of the rest, 11 ended before 2026-10-01 (MHLW keeps them open) and
  31 are in term, 21 of them granted in 2021: read them at build (renewed
  under another number, or closed). MHLW adds nothing the map needs.
- **Its own coordinates against the block point**: median **48 m**, 97.4%
  within 250 m (151 rows). With the block join at 95%, an own-point fallback
  would move a handful of rows.
- **1,225 open notifications, 977 addressed** (その他の食料・飲料販売業 373,
  集団給食施設 183, vending 162, コンビニエンスストア 55, 野菜果物販売業 52, …):
  the partial Food-shops layer of Matsuyama's and Fukuyama's precedent, if
  the owner wants it (open call 1).

### Personal services: 理容師法および美容師法に基づく営業施設一覧, page 1027245

Page `https://www.city.akita.lg.jp/kurashi/kenko/1005367/1012953/1027245.html`
(更新日 2026-09-08).

| File (under `…/001/027/245/`) | Bytes | Rows | Official (e-Stat FY2024 第10表) | Share |
|---|---|---|---|---|
| `riyou260831_2.xlsx` 理容所台帳（令和８年８月３１日現在） | **43,530** | **420** | barbers 431 | **97.4%** |
| `biyou260831_2.xlsx` 美容所台帳（令和８年８月３１日現在） | **370,732** | **850** | beauty salons 841 | **101.1%** |

(Official from `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv`,
秋田県秋田市; laundries 159, 取次所 94, in `…_cleaning_by_city.csv`, have no
list to measure.)

- **One sheet each; a title row, then the header on row 2.** Columns: No.,
  **施設名称**, **施設所在地**, an unnamed column (a building or floor, 22 and
  120 rows), 施設電話, 確認年月日 (dates), 確認番号. `city_rows` finds the
  header by 施設所在地; the unnamed column collides with an empty one under
  the key "" and is lost, which the join does not need. The barber file has
  3 empty rows (dropped by `city_rows`). The beauty file's sheet reports
  16,353 columns (empty formatting); `city_rows` reads it in seconds.
- **No operator column at all**: the name rule has only its version 2 sign
  test here. **No type column**: one file per kind, so the config names the
  kind per file (`source_rows` or `SOURCE_KIND`, Hamamatsu's registers).
  施設所在地 is in `ADDR_COLS` and 施設名称 in `NAME_COLS`; no shared-code
  change is needed for the registers.
- **Every address is in 秋田市.** Beauty: 2 rows not a premises by their
  address (`permits_from_rows`' mobile test), and 1 trade name contains 移動
  (a salon in a vehicle? read it at build). Repeats: barber 2, beauty 1 (address,
  name); **25 premises are in both registers** (one pin per premises and
  bucket keeps one per bucket).
- **Standing registers** (one 確認年月日 per premises, not a stream); the
  page says nothing about closed premises, so the page keeps "may include closed
  premises".

### No laundry list (disclosed)

The 生活衛生 section's notices (`…/1005367/1012953/index.html`) list the
barber and beauty list and an inn list, no laundry list; the laundry page
(`…/1005367/1005515.html`, クリーニング所について, 更新日 2026-08-28) carries
procedures and PDFs only, no XLSX or CSV. The build discloses it in the
page's businesses bullet and in What Is Excluded.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/05201-24.0a.zip` (319,917 B,
35,170 rows, **43,315 block keys** with the 小字 aliases), town-chōme
`.../19.0b/05201-19.0b.zip` (13,214 B, **510**). `japan.CITIES` entry at
build: `"akita": {"name": "秋田市", "pref": "05", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["05201"]}`.

| Tier, today's shared code | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| Food, fixed premises in a bucket (3,484) | **95.0%** | 4.0% | **1.0%** |
| … Food service (2,764) / Retail (720) | 95.5% / 92.9% | 3.6 / 5.7 | 0.9 / 1.4 |
| Barbers (420) | **91.7%** | 6.9% | 1.4% |
| Beauty salons (848 fixed) | **96.2%** | 2.7% | 1.1% |

**The misses, read** (towns only, by `measure.py` and `isjcheck.py` in the
scratchpad):
- **Chōme tier**: 大字 + 字 addresses whose 字 MLIT has but whose number it
  lacks (下新城中野字琵琶沼 8, 浜田字境川 5, 広面字昼寝 4, 手形字西谷地 4, and the
  雄和 and 河辺 towns of the 2005 merger): they take the 大字's centroid.
- **Unplaced (about 35 food rows)**: (a) the lists drop the 字 that MLIT keeps
  after a 1- or 2-character 大字 (`手形蛇野` for MLIT's 手形 + 小字 蛇野, and
  泉登木, 寺内イサノ, 寺内三千刈, 広面土手下): Ichinomiya's short-大字 rule
  (its brief, "The misses, read") would take them; (b) 御所野堤台3丁目, where
  MLIT's files hold 一丁目 and 二丁目 only; (c) `仁井田二ッ屋` with a small ッ
  where MLIT writes 二ツ屋, a kana-size rule. All three are shared code:
  follow each with the Minato control (`screen_japan_join.py minato` 98.0 /
  0.2 / 1.8) and every city screen.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_05_GML.zip`, N03 code 05201
(**905.4 km²**, extent W 140.005, S 39.449, E 140.516, N 39.865; the 2005
merger brought in 河辺町 and 雄和町). Read with `stub_test()`'s method and an
in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 奥羽線 (東日本旅客鉄道, 11) | JR Ōu Main Line | **10 / 105** records (8 stations) | 大張野, 和田, 四ツ小屋, 秋田, 泉外旭川, 土崎, 上飯島, 追分 |
| 羽越線 (東日本旅客鉄道, 11) | JR Uetsu Main Line | **5 / 60** | 秋田, 羽後牛島, 新屋, 桂根, 下浜 |
| 男鹿線 (東日本旅客鉄道, 11) | JR Oga Line | **1 / 9** | 追分 |

- **16 station records, 12 N02_005g groups** (秋田 Ōu + Uetsu, 35 m; 追分 Ōu
  + Oga, 0 m; 泉外旭川's two Ōu records, 55 m). No name in two groups; no
  separate stations closer than 600 m. **Median nearest-station gap 3,093
  m** (2,308 to 4,956): rings by the spacing rule at build.
- **Shinkansen**: none in N02 inside the city. JR East lists the Akita
  Shinkansen at 秋田 (18 weekday departures toward 大曲), but it runs over
  the Ōu Line's track and N02 files that track as 奥羽線; no other station in
  the city lists it (JR East's pages for 四ツ小屋, 和田 and 大張野 carry the
  Ōu Line only). Not counted (standing call 1); 秋田 keeps its
  ring through the conventional lines.
- **Cut at the line** (named by N03 municipality at build): the Ōu Line 95
  beyond (other prefectures 58, 湯沢市 6, 大館市 5, 大仙市 5, 能代市 4, 三種町
  4, 横手市 4, …), the Uetsu Line 55 (other prefectures 43, 由利本荘市 7,
  にかほ市 5), the Oga Line 8 (潟上市 4, 男鹿市 4).
- **The light-rail/rail test**: all three are heavy rail (N02 class 11, JR
  conventional). No tram or light rail.
- **The stub test.** The Oga Line keeps **one station of 9, 追分, its legal
  junction** with the Ōu Line, 184 m from the city line; **0.92 km** of its
  track lies inside the city. It is a JR line, so the standing call draws it
  as cut and **no owner question arises** (Kobe's JR Takarazuka Line, 1 of
  30); 追分 keeps its ring through the Ōu Line in any case. Its trains run
  through from 秋田 over the Ōu Line (they call at 泉外旭川, 土崎 and 上飯島).
  ⚠️ At build: the line's permanent label and legend entry on a 0.9 km stub
  (measure placement in a scratch render; Tokyo's `route` mechanism could
  draw the service from 秋田 if the stub cannot carry a label, a taste call
  for the owner only if it comes to that). The Ōu Line's 8 of 105 and the
  Uetsu Line's 5 of 60 are main lines cut at the line, not stubs.
- **Frequency, read 2026-10-06 from JR East's own station timetables** by
  plain GET with the project user-agent (`timetables.jreast.co.jp`, the index
  `timetable/list<code>.html` and its weekday pages under `2610/timetable/`,
  the October 2026 timetable; each page's departures counted whole):

  | Station (line, direction) | Weekday departures | Per hour 07-18 |
  |---|---|---|
  | 秋田 (Ōu, to 東能代・弘前) | 34 | 1-3 |
  | 秋田 (Ōu, to 大曲・湯沢) | 20 | 1 |
  | 秋田 (Uetsu, to 酒田・鶴岡) | 24 | 1-2 |
  | 秋田 (Oga, to 男鹿) | 18 | 1 |
  | 追分 (Ōu, to 東能代 / to 秋田; Oga, to 男鹿) | 27 / 46 / 19 | 1-6 |
  | 大張野 (Ōu, to 秋田 / to 大曲) | 24 / 20 | 1-2 |
  | 四ツ小屋 (Ōu, to 秋田 / to 大曲) | 23 / 20 | 1-3 |
  | 下浜 (Uetsu, to 秋田 / to 酒田) | 18 / 18 | 1-2 |
  | **桂根 (Uetsu, to 秋田 / to 酒田)** | **13 / 14** | 1-2 (some trains pass it) |

  **No stretch is at or under about 11 trains a day** (call 86): the
  thinnest is 桂根 on the Uetsu Line, 13 and 14, hourly 07-18; 新屋 and 羽後牛島
  beside it have 19 to 23. Counts are every departure a page lists,
  limited expresses included where they stop; the Akita Shinkansen is not
  in them. ⚠️ **The wave-5 probe's timetable reader
  (`jre.py` in the `japan_j4` scratch) undercounts**: it skips any departure
  whose minute is wrapped in a mark span (`<span class="sp">`, the ◆ trains),
  and read the Oga Line at 秋田 as 11 a day where the page holds 18. Counts
  above are from a whole-page reader (`katsurane.py`). Only counts are
  recorded, never a timetable on the page.
- ⚠️ **Gate 3** at build: JR East's station counts inside the city (Ōu 8,
  Uetsu 5, Oga 1). **OSM `name:en`** for 12 groups (one Overpass query at
  build, in the box below; not queried here).

## Scope

**Akita City.** The Ōu Line runs on to 大曲 and 湯沢 south and to 東能代 and
弘前 north, the Uetsu Line to 由利本荘 and 酒田, the Oga Line to 男鹿; cut at
the line.

## Licences — as stated; the read is pending

**As stated on each page**: each XLSX under オープンデータ carries 「この 作品
は クリエイティブ・コモンズ 表示 4.0 国際 ライセンスの下に提供されています。」
(link `creativecommons.org/licenses/by/4.0/deed.ja`), and each section ends
「本セクションで公開しているデータは、クリエイティブ・コモンズ・ライセンスのもとで提供しております。…各ライセンスの利用許諾条項に則ってご利用ください。」
**A licence-read agent reads the city's terms separately; staging records its
verdict and the credit wording.** No verdict is written in this brief; take
the credit from staging's record.

- **MHLW open data** (a control; only if open call 1 is taken): PDL 1.0 as
  recorded in `docs/data_sources/japan.md`, its 出典 line and who processed
  it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **JR East's timetables**: read for counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The food list carries 申請者名** (the operator): a company marker on
  1,886 of 4,041 rows, **none on 2,155**, the shape of a sole trader's own
  name. Step 2 reads it IN MEMORY for the name rule only (`OPERATOR_COLS`
  already holds 申請者名) and never writes it. **営業所電話番号** (filled on
  2,663) is never selected. No operator address column.
- **The name rule, measured in memory** (answers only, never a value): **5
  food rows** whose trade name is the operator's own name or a bare personal
  name (version 2's sign test 2, the operator comparison 3), **2 of them
  among fixed premises in a bucket**. The registers: **0** bare personal
  names, and no operator column to compare.
- **施設電話** in the registers is never selected; select 施設名称 and
  施設所在地 only.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; if open
  call 1 brings its rows in, its 法人名 joins the name rule (owner,
  2026-10-05).
- Run `check_personal_exposure.py akita` (`japan=True`) after step 2: it must
  print 0. Record the verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Tohoku after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 140.005-140.516 E, centroid 140.232:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded
out: (39.44, 140.00, 39.87, 140.52). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at build
from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band A with the
laundry gap disclosed; `mode: metro`; the minor tier and Japan East (Tohoku
after the retag); the Oga Line drawn as cut from 追分 (standing call, a JR
stub); the Akita Shinkansen not counted; no frequency floor.

**Open, with a recommendation:**

1. **MHLW's 977 addressed notifications as a partial, opt-in Food-shops
   layer** (konbini, drugstores, greengrocers; Matsuyama's and Fukuyama's
   precedent, disclosed as partial). *Recommend deciding it with
   Ichinomiya's open call 2b*, the same shape (MHLW holding a few percent
   of the city's permits but its notifications in full); the tradeoff is a
   bucket the page must call partial against a Food-shops layer of permits
   only (720 rows, no konbini). MHLW's permits and own points add nothing
   the map needs, so no other MHLW use is proposed.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `NAME_COLS` + 営業所名; `FORM_COLS` + 業態名; optionally the
  short-大字 rule (with Ichinomiya), 二ッ屋 / 二ツ屋, and nothing for the
  registers.
- `SOURCE_LINKS` for the monthly food file; `as_of` = the date in the
  file's title (2026-10-01 for `r081001.xlsx`), never today; the registers'
  `SOURCE_AS_OF` 2026-08-31.
- The census ratio (2.11, above the built range) and its reading; the 31
  in-term MHLW permits not in the city's file.
- The Oga Line's label on its 0.9 km stub; gate 3 (JR East); OSM `name:en`;
  line colours on both basemaps; the opening view (`map-view`); the factory
  share; `check_provenance.py`; `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "akita-food-page",
    "claim": "The food page says the list is refreshed monthly and offers it under CC BY 4.0",
    "kind": "http_contains",
    "url": "https://www.city.akita.lg.jp/kurashi/kenko/1005368/1010019/1017339.html",
    "present": ["食品営業許可施設一覧", "毎月更新しています", "creativecommons.org/licenses/by/4.0", "衛生検査課"]
  },
  {
    "id": "akita-food-edition",
    "claim": "The edition measured here: the list as of 2026-10-01, r081001.xlsx (renamed monthly, so a failure here means a new edition: re-measure)",
    "kind": "http_contains",
    "url": "https://www.city.akita.lg.jp/kurashi/kenko/1005368/1010019/1017339.html",
    "present": ["令和8年10月1日現在", "r081001.xlsx"]
  },
  {
    "id": "akita-food-file",
    "claim": "The 2026-10-01 food list (357,939 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.akita.lg.jp/_res/projects/default_project/_page_/001/017/339/r081001.xlsx",
    "min_bytes": 300000
  },
  {
    "id": "akita-registers-page",
    "claim": "The barber and beauty lists as of 2026-08-31, under CC BY 4.0",
    "kind": "http_contains",
    "url": "https://www.city.akita.lg.jp/kurashi/kenko/1005367/1012953/1027245.html",
    "present": ["令和8年8月31日現在", "riyou260831_2.xlsx", "biyou260831_2.xlsx", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "akita-barber-file",
    "claim": "The barber register (43,530 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.akita.lg.jp/_res/projects/default_project/_page_/001/027/245/riyou260831_2.xlsx",
    "min_bytes": 30000
  },
  {
    "id": "akita-beauty-file",
    "claim": "The beauty register (370,732 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.akita.lg.jp/_res/projects/default_project/_page_/001/027/245/biyou260831_2.xlsx",
    "min_bytes": 300000
  },
  {
    "id": "akita-no-laundry-list",
    "claim": "The laundry page offers no list file (no XLSX or CSV): the disclosed gap",
    "kind": "http_contains",
    "url": "https://www.city.akita.lg.jp/kurashi/kenko/1005367/1005515.html",
    "present": ["クリーニング所について"],
    "absent": [".xlsx", ".csv"]
  },
  {
    "id": "akita-mhlw-live",
    "claim": "MHLW's open-data file for Akita (05201) answers a plain keyless GET (a control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=05201_food_business_all.csv",
    "min_bytes": 400000
  },
  {
    "id": "akita-isj-block-live",
    "claim": "MLIT's block-level address file for Akita (05201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/05201-24.0a.zip",
    "min_bytes": 250000
  },
  {
    "id": "akita-isj-chome-live",
    "claim": "MLIT's town-chōme file for Akita (05201) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/05201-19.0b.zip",
    "min_bytes": 10000
  },
  {
    "id": "akita-jr-akita-timetable",
    "claim": "JR East's timetable index for 秋田 (list0039) links the weekday pages read: Ōu to 東能代 (0039010), Uetsu (0039030), Oga (0039040), Ōu to 大曲 (0039050). ASCII ids only: the host sends no charset, so the Japanese text does not decode here",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0039.html",
    "present": ["tt0039/0039010.html", "tt0039/0039030.html", "tt0039/0039040.html", "tt0039/0039050.html"]
  },
  {
    "id": "akita-jr-katsurane-timetable",
    "claim": "JR East's timetable index for 桂根 (list0455), the thinnest station, links its two Uetsu weekday pages (to 秋田 0455010, to 酒田 0455020)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0455.html",
    "present": ["tt0455/0455010.html", "tt0455/0455020.html"]
  },
  {
    "id": "akita-projected-crs",
    "claim": "Akita projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.23,
    "expect": "EPSG:32654"
  }
]
```
