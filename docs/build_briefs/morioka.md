# Morioka — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4's pre-verdicts converted,
call 136: `docs/decisions_drafts/staging.md`, "Wave 5, second half"). The Step
0 downloads were approved by the owner 2026-10-06 (call 141). **Step 0
measured 2026-10-06** (staging). Into `data/morioka/raw/` (gitignored), each
from its publisher's own host with the project user-agent, each HTTP 200,
under each URL's own file name as `japan_fetch.get` saves:

- From `www.city.morioka.iwate.jp` (盛岡市保健所 生活衛生課; the site was
  renewed 2026-10-01, every path now under `/kenko_fukushi/hokenjo/` and
  `/_res/projects/default_project/_page_/001/`): the food list
  `20260831.csv` (802,229 B, as of 2026-08-31); the barber, beauty and
  laundry lists `032018_riyou_202609.csv` (44,638 B),
  `032018_biyou_202609.csv` (110,776 B) and `032018_cleaning_202609.csv`
  (50,521 B), as of 2026-09-30.
- From `i2fas.mhlw.go.jp`: `03201_food_business_all.csv` (2,395,512 B).
- From `nlftp.mlit.go.jp`: `isj/03201-24.0a.zip` (279,750 B) and
  `isj/03201-19.0b.zip` (11,368 B).

**3,694,794 B in all, 7 files.** Nothing else was downloaded (not the XLSX
or PDF twins, not the 興行場, 旅館, 公衆浴場 or 特定建築物 CSVs on the same
page). All three buckets have a list.

**Run `python scripts/brief_check.py morioka` before writing any code.** Then
the `japan-city` skill, **Akita's shape** (`docs/build_briefs/akita.md`: one
city food list of every permit in term on its date, refreshed monthly, so no
`rebuilt_register` and no months to merge) and Hamamatsu's for the registers
(one file per kind). Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Morioka entry; its table is shared code
and was not edited). Rail: MLIT N02-25 cut at the N03 city line, measured
through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24: the Tōhoku Shinkansen's 盛岡 drops from N02's Shinkansen
records; the Akita Shinkansen runs over the Tazawako Line's track, filed as
田沢湖線, and stops at 盛岡 only, so 盛岡 keeps its ring through the
conventional lines and 前潟 through its local trains); (2) **lines served only
by limited expresses DO count** (2026-09-28); (3) **the city line only**:
only stations inside the city get rings, JR and the private lines are cut at
the line, **a one-station stub stays as cut** (2026-09-27); an URBAN line cut
to ONE station is left out, its station kept through the other lines, and
drawn cut only where no other line serves that station (owner, 2026-10-06,
calls 54 and 92); (4) **菓子製造業 and そうざい製造業 count, in Retail**, the
factory share measured and kept (2026-09-24, 2026-09-27); (5) **the name
rule**, version 2 (2026-10-06): a bare personal name is withheld whatever the
operator column holds; (6) **no page says "currently operating"**. Also: no
frequency floor for JR or private lines in Japan (owner, 2026-10-06, call
46), any stretch at about 11 trains a day or fewer named and drawn (call 86);
fault-based cost clauses accepted for all of Japan (2026-09-24); English
station names from OSM `name:en`; every Japanese city reads `WAVE2_RULES`
(owner, 2026-10-04).

**✅ Precedents set 2026-10-06, applied here without a new call:** a stated
food share where a list is incomplete (call 125, Ichinomiya; here the city
withholds premises whose operators asked, below); MHLW's notifications as a
partial Food-shops layer where they run to hundreds of addressed rows (127b;
Akita, Toyonaka; Iwaki's 164 and Aomori's 248 were too thin, call 150);
MHLW's own point where the block join misses (127c); low-frequency stretches
drawn and named (86).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Morioka
carries `label_tier: "minor"` and goes in the **Japan East** view
(`app/cities.py`); wave 4's first city to land retags Japan into the eight
regions, Morioka into **Tohoku**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 ("unless there is
substantial JR, JR reads as metro"): JR East has 8 of the 11 station groups,
and the other line is IGR, the third-sector successor of the Tōhoku Main
Line, heavy rail on the same alignment; no subway or tram. Akita's,
Fukuyama's and Kitakyushu's precedent.

---

## The one-line summary

**All three buckets from the city's own monthly CSVs (CC BY 4.0 as stated;
the licence read is pending, staging records it).** The food list of every
permit in term on **2026-08-31** holds **4,379 rows, 3,350 restaurants,
103.6% of e-Stat's 3,233 in force**, old-law permits included (not
Kurashiki's trap). ⚠️ **The city leaves out every permit whose operator asked
not to be listed** (the page says so): **796 rows (18.2%) carry no name and
no address**, 649 of them restaurants, so the **published restaurants are
2,701, 83.5% of e-Stat's in force**: the share the page states (call 125).
Through `japan_eigyo`: **Food service 2,169, Retail 874** fixed premises.
Barbers 328, beauty salons 756, laundries 286 as of 2026-09-30: **98.2%,
102.0% and 97.6% of official**. Block join **97.4%** (food), 95.4% (barbers),
97.3% (beauty), 95.4% (laundries); unplaced 0.2-1.8%. MHLW's file holds the
same new-law permits with the same rows withheld: it adds **609 addressed
notifications** (partial Food shops, precedent) and nothing else. **Rail: 11
station groups** (JR East 8, IGR 5, 盛岡 and 好摩 shared), read from JR
East's and IGR's own timetables: the Tōhoku Line 40-43 a day, IGR 33-43, the
Tazawako Line 13; **the Yamada Line (10 a day to 上米内, 3 beyond) and the
Hanawa Line (7 and 9) are named and drawn** (call 86).

---

## Business leg — the city's 保健所 lists

Host `https://www.city.morioka.iwate.jp` (the city's own CMS; no catalogue
API). Every file is a plain GET under `/_res/projects/default_project/_page_/001/`.
**The host sends no charset** (`Content-Type: text/html`): the checks below
use ASCII anchors.

### Food: 食品営業許可施設一覧, page 1006689

Page `https://www.city.morioka.iwate.jp/kenko_fukushi/hokenjo/shokuhineisei/1017014/1006689.html`
(更新日 2026-09-09): 「食品営業許可施設一覧（令和8年8月末時点）」, 「この施設一覧は、毎月10日頃までに前月末時点の内容に更新します。」
and 「公開している施設情報からは、以下の内容を除外しています。臨時営業に関する情報 営業者が非公開を希望している情報」.

| File (under `…/001/006/689/`) | Bytes | Rows | What it is |
|---|---|---|---|
| `20260831.csv` 食品営業許可施設一覧（CSV） | **802,229** | **4,379** | every permit in term on 2026-08-31, temporary permits left out; **monthly**, the file renamed for each month-end (`YYYYMMDD.csv`) |

- **UTF-8 with BOM, CRLF, 14 columns, one header row.**
  `japan_register.city_rows` reads all 4,379. Dates are `YYYY/M/D` strings
  (all parse): 許可年月日 2018-12-07 to 2026-08-28, 満了年月日 2024-06-23 to
  2034-08-25.
- **Columns**: **業種**, **種目**, **屋号商号**, 市町村名, **営業所所在地**,
  ビル名称, 営業所電話番号, **営業者**, **代表者**, **許可年月日**,
  **満了年月日**, 許可期間, **許可番号**, 登録の種類. 営業所所在地 starts at the
  town (盛岡市 is in 市町村名), which `permits_from_rows` takes as it stands.
- **Against the shared tuples:** 営業所所在地 is in `ADDR_COLS`, 業種 in
  `TYPE_COLS` (its circled numbers, `① 飲食店営業`, are what
  `japan_eigyo.normalise` already strips), 種目 in `FORM_COLS` (read under
  `WAVE2_RULES`' `form_cols`), 代表者 in `OPERATOR_COLS`. **`NAME_COLS` lacks
  屋号商号** (without it every trade name reads empty and the name rule
  compares nothing) and **`OPERATOR_COLS` lacks 営業者** (filled on 3,550
  rows; 代表者 only on 2,090). The scratch measurement renamed both in
  memory; the build adds them to the shared tuples (or a `source_rows` in the
  config) and re-runs the Minato control.
- **The month's file replaces the last.** `japan_fetch.current_url` takes a
  `SOURCE_LINKS` regex for the food key (`\d{8}\.csv`, Kawasaki's and Otsu's
  precedent), so a later build reads the current edition and pins `as_of` to
  the date in the page's title, never today.
- **Types**: 飲食店営業 3,350 (543 under the old law), 菓子製造業 324,
  そうざい製造業 215, 食肉販売業 132, 魚介類販売業 130, 乳類販売業 57, 漬物製造業
  34, 麺類製造業 31, 喫茶店営業 24 (old law), … 32 types once the circled
  numbers are stripped. One vending machine with a cooking function
  (調理機能を有する自動販売機) is the list's only vending row.
- **種目** (free text, 432 values) is the form: 食堂 843 of the restaurants,
  バー 342, 移動食品 228, 居酒屋 109, 軽飲食 106, コンビニエンスストア 96, カフェ
  56, 喫茶店 48, **スナック 46**, … `japan_eigyo`'s form rules decide (below):
  スナック out as a hostess venue, バー kept in Food service as in every built
  city (`docs/category_rules.md` R3); unlike Iwaki's combined
  バー・スナック等, the two are separate values here.

### The withheld rows (operators who asked) — the page's own exclusion

- **796 rows carry no 屋号商号, no 営業所所在地 and no 市町村名** (2 more lack
  a name only); 794 carry no operator either. Every one is a new-law permit
  (2021-06 onward), 15% to 28% of each year's grants (2021 100 of 356, 2022
  176 of 678, … 2026 77 of 540); **no old-law row is withheld** (all 821 carry
  an address). By type: restaurants 649, 菓子 60, そうざい 47, 魚介 13, … and
  by 種目 the ordinary mix (食堂 88, バー 90, 移動食品 70, 居酒屋 28).
- **They cannot be placed and are not**: `permits_from_rows` reads an empty
  address as not a premises. The build counts them, states them, and never
  fills them from another source: **MHLW withholds the same rows** (790 of
  the 796 numbers are in MHLW's file, with an address on none; a trade name
  on 2). ⚠️ A raising check at build: no city row with an empty address ends
  with a point.
- **The stated share (call 125)**: restaurants with a published address
  **2,701 of e-Stat's 3,233 in force, 83.5%** (the list's 3,350 including the
  withheld are 103.6%). The page's businesses bullet states it with the
  reason; the sentence is drafted at build from the city-page template, and
  is a proposal in the drafts file if no template covers it.

### Old-law coverage (Kurashiki's trap) — not this list's problem

- **Old-law permits are in the file**: **821 rows** (543 restaurants, 24
  喫茶店営業), numbered `N―NNN` where the new law's read `盛岡市指令…`, granted
  2018-12-07 to 2021-05-26 with terms of 7 years (592), 6 (211) and 8 (18),
  ending 2026-09-25 to 2029-06-25. The old-law grants run 25 to 71 a month
  from 2019-09 on and thin before it (2019-06 to 08: 5, 15, 6), exactly
  where 7-year terms have ended; new-law grants start 2021-06-02.
- **e-Stat 衛生行政報告例 FY2024** (`japan_official.estat()`), 岩手県盛岡市,
  飲食店営業 in force 2025-03-31: **3,233** (old law 1,153, revised 2,080). The
  list's 3,350 restaurants are **103.6%** (seventeen months later, with
  old-law premises renewed under the new law), vehicles and stalls included
  on both sides. Retail types against the same tables (list, withheld
  included / e-Stat): 菓子 324 / 309, そうざい 215 / 185, 魚介類販売 130 / 102,
  食肉販売 132 / 95; old-law 喫茶店営業 24 / 65.
- **The list keeps 18 permits past their term** (満了年月日 2024-06 to
  2026-08: 17 restaurants and 1 noodle maker, all new-law, 6 of them
  withheld): a lapse the list has not caught up with, or a renewal not yet
  entered (open call 2).

### Duplicates and closed premises

- **Unique by (許可番号, 許可年月日)**: 4,379 distinct. The number alone
  repeats (4,220 distinct): the old-law numbers restart each year (316 rows),
  so it is never a key on its own.
- **One premises, several permits**: 42 addressed rows repeat an (address,
  trade name, type) in 25 groups; 3,135 distinct (address, trade name). One
  pin per premises and bucket (trap 7) leaves **2,827 pins from 3,043**
  bucketed fixed rows.
- **Closures**: no status column. The list is permits in term on its date,
  so a premises that closed without returning its permit stays to the end of
  the term; the page keeps "may include closed premises".

### Counts through `japan_eigyo` (fixed premises)

Of the 3,583 addressed rows: **Food service 2,169, Retail 874** (菓子 264,
deli 167 + 59 by 種目, konbini and supermarkets holding a restaurant permit
148, butcher 125, fishmonger 113, dairy 57; 3,043 storefront rows). Left out:
**not a premises 204** (every address reading …一円: vehicles licensed
citywide), temporary or mobile by 種目 177, event catering (仕出し) 81,
institutional catering 46, inside accommodation 41, **hostess venues 31**
(スナック), entertainment venues 8, and 127 manufacturing types with no rule
(漬物, 麺類, 酒類, …), as in every built city. **No konbini notifications in
the city's list** (they come from MHLW, below).

**Economic Census control** (`scripts/japan_census_control.py` at build):
the 2021 census counts **1,406** 飲食店 establishments in 03201
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 2,152 distinct placed
Food-service premises is **1.53 per establishment**, just under the built
cities' 1.56-1.92, as the withheld fifth would predict. Record the figure.

### MHLW's file (03201): the same permits, plus notifications

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=03201_food_business_all.csv`:
**2,395,512 B, 6,495 rows** (許可 3,966, 届出 2,505, 許可(廃業) 19,
届出(廃業) 5), UTF-8 with BOM, the national schema (営業施設名称、屋号又は商号,
営業の種類, 業態, 営業施設所在地, 方書, 緯度 / 経度, 法人名, 法人番号, 法人住所,
phones, permit dates, 廃業年月日, 申請区分). Open permits granted 2021-06-02
to 2026-08-31 (**new law only**); 3,216 restaurants, 2,450 addressed (the
sweep's 0.97 cover, 76.3% addressed).

- **Against the city's list, by permit number**: 3,531 of MHLW's 3,966 open
  permits are city rows; every city row MHLW lacks is old-law (663) or one of
  26 new-law rows. **MHLW's other 435 are all 臨時営業** (temporary, granted
  2025-2026), which the city leaves out by design and the form rule drops:
  **MHLW adds no permit**.
- **Withheld alike**: MHLW gives an address for every addressed city row it
  holds (2,741) and for none of the city's withheld rows (above).
- **Its own coordinates against the block point**: median **37 m**, 89.4%
  within 250 m (2,217 rows). Precedent 127c: MHLW's point where the block
  join misses, keyed by the number's digits AND the grant date; with the join
  at 0.2% unplaced it reaches about 6 food rows.
- **Notifications (precedent 127b, in)**: **2,505, 1,100 addressed**
  (その他の食料・飲料販売業 282, 集団給食施設 215, コンビニエンスストア 99,
  野菜果物販売業 83, 百貨店・総合スーパー 43, …). Through `japan_eigyo`, **609
  fixed Retail rows**, block join **94.9%** (chōme 4.4, unplaced 0.7). The
  partial Food-shops layer of Matsuyama's, Fukuyama's, Ichinomiya's and
  Akita's precedent, disclosed as partial, MHLW credited on the notice.

### Personal services: 生活衛生営業施設等一覧, page 1034998

Page `https://www.city.morioka.iwate.jp/kenko_fukushi/hokenjo/shokuhineisei/seikatsueisei/1034998.html`
(更新日 2026-10-05): 「…一覧（令和8年9月末時点）」, monthly (「毎月10日頃までに前月末時点の内容に更新します」),
and 「営業実態が確認できない施設は除いています。」 (premises whose operation
cannot be confirmed are left out: a closure filter of the city's own).

| File (under `…/001/034/998/R8/`) | Bytes | Rows | Official (e-Stat FY2024 第10・11表) | Share |
|---|---|---|---|---|
| `032018_riyou_202609.csv` 理容所一覧 | **44,638** | **328** | barbers 334 | **98.2%** |
| `032018_biyou_202609.csv` 美容所一覧 | **110,776** | **756** | beauty salons 741 | **102.0%** |
| `032018_cleaning_202609.csv` クリーニング所等一覧 | **50,521** | **286** | laundries 265 + storeless 28 = 293 | **97.6%** |

(Official from `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
`…_cleaning_by_city.csv`, 岩手県盛岡市; the laundries' 265 include 227
取次所.)

- **UTF-8 with BOM, CRLF, one header row, 9 columns**: 全国地方公共団体コード,
  No, 業種 / 種別, **施設名称**, **開設者名** / **営業者名**, **施設所在地** /
  **所在地**, 施設電話番号, 確認番号, 確認年月日. Every column the build needs is
  in the shared tuples (所在地 and 施設所在地 in `ADDR_COLS`, 施設名称 in
  `NAME_COLS`, 開設者名 and 営業者名 in `OPERATOR_COLS`, 業種 and 種別 in
  `TYPE_COLS`); no shared-code change for the registers. Every address
  starts 盛岡市.
- ⚠️ **Never filter on 全国地方公共団体コード**: 750 beauty rows read 032018,
  and 6 read 032019 to 032024 (a fill-down that counted up), every one at a
  盛岡市 address.
- **The laundry list includes storeless pick-ups**, as the page says
  (「クリーニング所等の一覧は無店舗取次店を含む」, the kind renamed クリーニング所等
  from the 2026-06 list): **27 rows have an address of 盛岡市 alone and no
  確認年月日**, e-Stat's 28 無店舗取次店 exactly. The kind column reads
  クリーニング所等 on every row, so the kind cannot drop them: the address
  does (open call 3). The registers also hold **6 beauty rows and 1 barber
  row at 盛岡市 alone** (5 of the 6 with a 確認年月日): no premises to place,
  dropped by the same rule. Without them: **barbers 327, beauty 750,
  laundries 259** (97.7% of e-Stat's 265 laundries).
- **Standing registers** (one 確認年月日 per premises, 1946 to 2026-09-30);
  repeats: beauty 1 (address, name); **16 premises are in both the barber and
  beauty lists** (one pin per premises and bucket keeps one per bucket).
- **No type column beyond the kind**: one file per kind, so the config names
  the kind per file (`source_rows` or `SOURCE_KIND`, Hamamatsu's registers).
- The registers' file names carry the month (`_202609`) and the folder the
  year (`R8/`): `SOURCE_LINKS` regexes (`032018_riyou_\d{6}\.csv`, …), with
  `SOURCE_AS_OF` 2026-09-30.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`; the 玉山区 of the 2006
merger is gone from the addresses). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/03201-24.0a.zip` (279,750 B,
**28,948 block keys** with the 小字 aliases), town-chōme
`.../19.0b/03201-19.0b.zip` (11,368 B, **413**). `japan.CITIES` entry at
build: `"morioka": {"name": "盛岡市", "pref": "03", "epsg": 32654, "n02":
"25", "rules": WAVE2_RULES, "wardless": True, "wards": ["03201"]}`.

| Tier, today's shared code | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| Food, fixed premises in a bucket (3,043) | **97.4%** | 2.4% | **0.2%** |
| … Food service (2,169) / Retail (874) | 97.8% / 96.3% | 2.0 / 3.4 | 0.2 / 0.2 |
| MHLW notifications, fixed Retail (609) | 94.9% | 4.4% | 0.7% |
| Barbers (327, without the 盛岡市-only row) | **95.4%** | 2.8% | 1.8% |
| Beauty salons (750, without the 6) | **97.3%** | 1.9% | 0.8% |
| Laundries (259, without the 27 storeless) | **95.4%** | 3.5% | 1.2% |

**The misses, read** (towns only, by `measure.py` and `join2.py` in the
scratchpad):
- **Chōme tier**: 大字 + 字 addresses whose 字 MLIT has but whose number it
  lacks (藪川字外山 9, 本宮字荒屋 7, 渋民字渋民 6, 繋字塗沢 4, 向中野字道明 4),
  and the 玉山 towns: they take the 大字's centroid.
- **Unplaced (6 food rows)**: 川目第N地割 (4; Iwate's 地割 numbering, cut at
  第 by today's parse, a rule for shared code with the Minato control only if
  another Iwate city needs it); 渋民鶴飼 and 上太田上河原 with the 字 dropped
  (Ichinomiya's short-大字 rule would take them). Registers: a parenthesised
  old village name (旧玉山村) 2, the same dropped 字 (好摩夏間木), and a
  parenthesis before the town (`(青山町`) on 2 beauty rows.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_03_GML.zip`, N03 code 03201
(**885.8 km²**, extent W 140.995, S 39.564, E 141.527, N 39.930; the 2006
merger brought in 玉山村). Read with `stub_test()`'s method and an in-memory
`CITIES` entry (scratch `rail.py`, `track.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | Track inside |
|---|---|---|---|---|
| 東北線 (東日本旅客鉄道, 11) | JR Tōhoku Main Line | **3 / 155** | 盛岡, 仙北町, 岩手飯岡 | 7.3 km |
| 田沢湖線 (東日本旅客鉄道, 11) | JR Tazawako Line | **2 / 18** | 盛岡, 前潟 | 5.6 km |
| 山田線 (東日本旅客鉄道, 11) | JR Yamada Line | **4 / 15** | 盛岡, 上盛岡, 山岸, 上米内 | 34.4 km |
| 花輪線 (東日本旅客鉄道, 11) | JR Hanawa Line | **1 / 27** | 好摩 | 4.0 km |
| いわて銀河鉄道線 (アイジーアールいわて銀河鉄道, 12, third sector) | IGR Iwate Galaxy Railway Line | **5 / 18** | 盛岡, 青山, 厨川, 渋民, 好摩 | 19.7 km, **two pieces** |

- **15 station records, 11 N02_005g groups** (盛岡 IGR + Tōhoku + Tazawako +
  Yamada, 42 m; 好摩 IGR + Hanawa, 0 m). No name in two groups; no separate
  stations closer than 600 m. **Median nearest-station gap 2,074 m** (1,496
  to 4,680): rings by the spacing rule at build.
- **Shinkansen**: 盛岡's Tōhoku Shinkansen record drops (standing call 1).
  The Akita Shinkansen's 26 weekday departures at 盛岡 are on its own JR East
  page and not counted; 前潟 is served by locals only.
- ⚠️ **IGR leaves the city and comes back**: 巣子 and 滝沢 lie in 滝沢市
  between 厨川 and 渋民, so the city line cuts IGR into **9.0 km
  (盛岡-青山-厨川) and 10.7 km (渋民-好摩)**. The standing call (city line
  only) draws both pieces and nothing in 滝沢市. At build: the permanent
  label on each piece, or on one with the legend carrying the line (render it
  in a scratch map; a taste call for the owner only if the render is
  ambiguous). The Hanawa Line's trains run through the gap over IGR's track.
- **Cut at the line** (named by N03 municipality at build): IGR 13 beyond
  (滝沢市 2, 岩手町 3, 一戸町 4, 二戸市 3, other prefectures 1); Yamada 11
  (宮古市 11); Tōhoku 152 (矢巾町 1, 紫波町 3, 花巻市 3, …, other prefectures
  132); Tazawako 16 (滝沢市 2, 雫石町 3, other prefectures 11); Hanawa 26
  (八幡平市 12, other prefectures 14).
- **The light-rail/rail test**: all heavy rail (JR conventional, class 11;
  IGR class 12, 普通鉄道). No tram or light rail.
- **The stub test.** The Hanawa Line keeps **one station of 27, 好摩, its
  junction** with IGR, and 4.0 km of its own track to the city line. A JR
  line, so the standing call draws it as cut and **no owner question
  arises** (Akita's Oga Line, Kobe's Takarazuka Line); 好摩 keeps its ring
  through IGR in any case. Its 4 km carries a label more easily than Akita's
  0.9 km stub. The Tazawako Line keeps 2 of 18 and the Yamada Line 4 of 15:
  cut at the line, not stubs.
- **Frequency, read 2026-10-06 from the operators' own timetables** by plain
  GET with the project user-agent: JR East (`timetables.jreast.co.jp`, each
  station's `timetable/list<code>.html` and its weekday pages under
  `2610/timetable/`, the October 2026 timetable) and IGR
  (`www.igr.jp/timetable/station-timetable`, every station's table on one
  page, no weekday/holiday split: 5 trains a day carry a day note, counted).
  **Every departure counted**: JR East's pages by each departure block
  (`<div class="timetable_time" data-train=…>`), marked trains (◆, ●, ■)
  included, cross-checked against the minute digits.

  | Station (line, direction) | Weekday departures | Per hour 07-18 |
  |---|---|---|
  | 盛岡 (Tōhoku, to 花巻・一ノ関) | 43 | 1-5 |
  | 仙北町 / 岩手飯岡 (Tōhoku, to 盛岡 / to 一ノ関) | 41 / 40 each | 0-8 / 1-4 |
  | 盛岡, 青山, 厨川 (IGR's page, up / down) | 42 / 43 (8 / 7 of them Hanawa trains) | 1-5 |
  | 渋民, 好摩 (IGR's page, up / down) | 34 / 33 (8 / 7 Hanawa) | 0-5 |
  | 盛岡 (JR East's IGR page, to いわて沼宮内) | 36 (10 turn at 滝沢) | 1-3 |
  | 前潟 (Tazawako, to 田沢湖 / to 盛岡) | 13 / 13 | 0-2 |
  | **盛岡, 上盛岡, 山岸 (Yamada, to 宮古 / to 盛岡)** | **10 / 10** (7 turn at 上米内) | 0-2 |
  | **上米内 (Yamada, to 宮古 / to 盛岡)** | **3 / 10** (7 of the 10 start there) | 0-1 |
  | 区界 (Yamada, in 宮古市, beyond the line) | 1 train + 5 buses / 2 trains + 5 buses (the rapids pass) | – |
  | **好摩 (Hanawa, to 大館)** | **7** | 0-1 |
  | **東大更 (Hanawa, in 八幡平市, beyond the line; to 大館 / to 盛岡)** | **7 / 9** | 0-2 |

  **Named and drawn (call 86)**: the **Yamada Line**, 10 trains a day each
  way 盛岡-上米内 and **3 each way** from 上米内 to the city line (the whole
  in-city line is at or under about 11, not only the far stretch); the
  **Hanawa Line**, **7 down and 9 up** on its 4 km from 好摩. The Tazawako
  Line's 13 a day is above the mark (Akita's 下浜, 15 and 13, was not named).
  ⚠️ **JR East's 盛岡 page for the Yamada Line lists 12 buses** among its 22
  departures (its legend: 無印=バス): only trains are counted. ⚠️ **The
  wave-5 probe undercounted** (Tōhoku 30-35, IGR 31, Hanawa 5-7): its reader
  skipped minutes wrapped in a mark span. ⚠️ **A reader that counts
  `<span class="minute">` overcounts**: every empty hour holds an empty one
  (Akita's `katsurane.py`; see the report). Only counts are recorded, never
  a timetable on the page.
- ⚠️ **Gate 3** at build: JR East's station counts inside the city (Tōhoku 3,
  Tazawako 2, Yamada 4, Hanawa 1) and IGR's station list (盛岡, 青山, 厨川,
  渋民, 好摩 inside; 巣子 and 滝沢 in 滝沢市). **OSM `name:en`** for 11 groups
  (one Overpass query at build, in the box below; not queried here).

## Scope

**Morioka City.** The Tōhoku Line runs on south to 矢幅 and 花巻, IGR north
through 滝沢 (between its two pieces) to いわて沼宮内 and 二戸, the Tazawako Line
west to 雫石, the Yamada Line east to 区界 and 宮古, the Hanawa Line north-west
to 八幡平 and 大館; cut at the line. Ridership is out of scope.

## Licences — as stated; the read is pending

**As stated on each page**: the food page, 「このページで公開しているデータはオープンデータとして提供しており、クリエイティブ・コモンズ・ライセンス表示4.0国際（CC BY）に基づき利用できるものとします。また、掲載しているデータを利用する際は「盛岡市オープンデータサイト」を参照してください。」;
the registers' page, the same with 「データの一部」, the CSVs sitting under its
オープンデータ heading (the XLSX and PDF above it are not said to be open; the
build reads the CSVs only). Both point to the city's open-data site
(`/shisei/johokokai/opendata/index.html`), which the read follows. **A
licence-read agent reads the city's terms separately; staging records its
verdict and the credit wording.** No verdict is written in this brief.

- **MHLW open data** (notifications in, by precedent; its points where the
  join misses): PDL 1.0 as recorded in `docs/data_sources/japan.md`, its
  出典 line and who processed it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **JR East's and IGR's timetables**: read for counts only, never
  reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The city withholds 796 food rows at the operators' request**; nothing in
  the build may restore them (MHLW does not either). The page never names or
  counts them by place.
- **The food list carries 営業者 and 代表者** (operator and representative):
  on the addressed rows a company marker on 2,037, none on 1,511, the shape
  of a sole trader's own name. Step 2 reads them IN MEMORY for the name rule
  only (once 営業者 joins `OPERATOR_COLS`) and never writes them.
  **営業所電話番号** (filled on 3,009) and **ビル名称** are never selected.
- **The name rule, measured in memory** (answers only, never a value): **0
  food rows** whose trade name is the operator's own name or a bare personal
  name (version 2's sign test and the operator comparison, with 屋号商号 and
  営業者 renamed). Registers: **0** bare personal names; **1** beauty row whose
  name is its 開設者名. Operators: barbers 50 with a company marker, 278
  without; beauty 231 / 525; laundries 183 / 103 (the 27 storeless all
  without, and dropped).
- **施設電話番号** in the registers is never selected; select 施設名称 and the
  address only.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; its 法人名
  joins the name rule (owner, 2026-10-05): **20** of its 1,100 addressed
  notifications have a name equal to it, withheld.
- Run `check_personal_exposure.py morioka` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Tohoku after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 140.995-141.527 E, centroid 141.269:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded
out: (39.56, 140.99, 39.94, 141.53). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at build
from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band A (call
136); the downloads (call 141); `mode: metro`; the minor tier and Japan East
(Tohoku after the retag); the Hanawa Line drawn as cut from 好摩 (standing
call, a JR stub); IGR drawn in two pieces (the city line only); the
Shinkansen not counted; no frequency floor; the Yamada and Hanawa stretches
named (call 86); MHLW's notifications in as partial Food shops (127b) and its
points where the join misses (127c); the food share stated (125).

**Open, with a recommendation:**

1. **The stated share's reason.** The withheld fifth is an operator opt-out,
   not a gap in the list (Ichinomiya's 67.7% was a list that stopped short).
   *Recommend stating both numbers with the city's own reason*: "2,701
   restaurants with a published address, 83.5% of those licensed; the city
   leaves out premises whose operators asked not to be listed". The tradeoff
   is a sentence no template carries yet (a proposal in the drafts file at
   build) against a bare percentage a reader would take for missing data.
2. **The 18 permits past their term** (12 addressed). *Recommend dropping a
   row whose 満了年月日 precedes `as_of`* (Fukuyama's "kept while in term"):
   the map shows permits in term on its date, which is what the page says.
   Tradeoff: a renewal the list has not yet entered drops for a month.
3. **An address of the city's name alone is not a premises** (27 storeless
   laundry pick-ups, 6 beauty rows, 1 barber row). *Recommend a shared rule
   in `permits_from_rows`* (an empty remainder after the prefecture and city
   are stripped, beside Kurume's 市内 rule), followed by the Minato control
   and every city screen; a city-local filter otherwise. Tradeoff: shared
   code touched for 34 rows, against the next city's register carrying the
   same shape unnoticed (unplaced rows at one centroid).

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `NAME_COLS` + 屋号商号; `OPERATOR_COLS` + 営業者; open call 3's
  city-name-only rule; optionally the short-大字 rule (with Ichinomiya) and
  地割 (4 rows).
- `SOURCE_LINKS` for the monthly food file and the three registers; `as_of`
  = the date in the page's title (2026-08-31 for `20260831.csv`), never
  today; the registers' `SOURCE_AS_OF` 2026-09-30.
- The raising check that no withheld row gets a point; the stated share
  recomputed on the build's edition.
- MHLW: notifications through `japan_eigyo` (609 fixed Retail rows here),
  its points keyed by number and grant date, 臨時営業 dropped.
- IGR's label on two pieces; the Hanawa label on its 4 km; gate 3 (JR East,
  IGR); OSM `name:en`; line colours on both basemaps; the opening view
  (`map-view`); the factory share; `check_provenance.py`;
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "morioka-food-page",
    "claim": "The food page links the 2026-08-31 CSV, offers it under CC BY and points to the city's open-data site. ASCII anchors only: the host sends no charset, so the Japanese text does not decode here",
    "kind": "http_contains",
    "url": "https://www.city.morioka.iwate.jp/kenko_fukushi/hokenjo/shokuhineisei/1017014/1006689.html",
    "present": ["20260831.csv", "CC BY", "opendata/index.html"]
  },
  {
    "id": "morioka-food-file",
    "claim": "The 2026-08-31 food list (802,229 B) answers a plain GET (renamed monthly, so a failure here means a new edition: re-measure)",
    "kind": "http_ok",
    "url": "https://www.city.morioka.iwate.jp/_res/projects/default_project/_page_/001/006/689/20260831.csv",
    "min_bytes": 700000
  },
  {
    "id": "morioka-registers-page",
    "claim": "The registers' page links the 2026-09 barber, beauty and laundry CSVs under CC BY (ASCII anchors only)",
    "kind": "http_contains",
    "url": "https://www.city.morioka.iwate.jp/kenko_fukushi/hokenjo/shokuhineisei/seikatsueisei/1034998.html",
    "present": ["032018_riyou_202609.csv", "032018_biyou_202609.csv", "032018_cleaning_202609.csv", "CC BY", "opendata/index.html"]
  },
  {
    "id": "morioka-barber-file",
    "claim": "The barber list (44,638 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.morioka.iwate.jp/_res/projects/default_project/_page_/001/034/998/R8/032018_riyou_202609.csv",
    "min_bytes": 35000
  },
  {
    "id": "morioka-beauty-file",
    "claim": "The beauty list (110,776 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.morioka.iwate.jp/_res/projects/default_project/_page_/001/034/998/R8/032018_biyou_202609.csv",
    "min_bytes": 90000
  },
  {
    "id": "morioka-laundry-file",
    "claim": "The laundry list (50,521 B, storeless pick-ups included) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.morioka.iwate.jp/_res/projects/default_project/_page_/001/034/998/R8/032018_cleaning_202609.csv",
    "min_bytes": 40000
  },
  {
    "id": "morioka-mhlw-live",
    "claim": "MHLW's open-data file for Morioka (03201) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=03201_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "morioka-isj-block-live",
    "claim": "MLIT's block-level address file for Morioka (03201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/03201-24.0a.zip",
    "min_bytes": 250000
  },
  {
    "id": "morioka-isj-chome-live",
    "claim": "MLIT's town-chōme file for Morioka (03201) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/03201-19.0b.zip",
    "min_bytes": 10000
  },
  {
    "id": "morioka-jr-kamiyonai-timetable",
    "claim": "JR East's timetable index for 上米内 (list0504) links its two Yamada weekday pages read (to 宮古 0504010: 3 trains; to 盛岡 0504020: 10)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0504.html",
    "present": ["tt0504/0504010.html", "tt0504/0504020.html"]
  },
  {
    "id": "morioka-jr-koma-timetable",
    "claim": "JR East's timetable index for 好摩 (list0672) links the Hanawa weekday page read (to 大館 0672010: 7 trains)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0672.html",
    "present": ["tt0672/0672010.html"]
  },
  {
    "id": "morioka-jr-higashiobuke-timetable",
    "claim": "JR East's timetable index for 東大更 (list1272), the Hanawa Line's first station beyond the line, links both weekday pages read (7 down, 9 up)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1272.html",
    "present": ["tt1272/1272010.html", "tt1272/1272020.html"]
  },
  {
    "id": "morioka-igr-timetable",
    "claim": "IGR's station timetable page carries the tables read for 厨川 and 渋民, either side of the 滝沢市 gap",
    "kind": "http_contains",
    "url": "https://www.igr.jp/timetable/station-timetable",
    "present": ["厨川駅時刻表", "渋民駅時刻表", "igr-eki-diaup6"]
  },
  {
    "id": "morioka-projected-crs",
    "claim": "Morioka projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 141.27,
    "expect": "EPSG:32654"
  }
]
```
