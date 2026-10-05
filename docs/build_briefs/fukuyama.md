# Fukuyama — build brief

**Band A, owner-approved 2026-10-04** (Japan's third wave, "53 yes ... 60
yes"; the Step 0 downloads approved the same day: `docs/decisions_drafts/staging.md`,
"Band A's Japanese briefs: Step 0 downloads and licence reads approved").
**Step 0 measured 2026-10-04.** Downloaded, each from its publisher's own
host, into `data/fukuyama/raw/` (gitignored, under each URL's own file name,
as `japan_fetch.get` saves): the city's CKAN `licensed_food` (the full list
and all twelve monthly files, CSV and XLSX: 26 files, 3,207,033 B) and the
barber/beauty and laundry CSVs of `licensed_env` (266,210 B), MHLW's 34207
file (2,981,068 B) and MLIT's ISJ for 34207 (`raw/isj/`, 728,327 B); 7,182,638
B in all. No other host was fetched for data. **Run `python
scripts/brief_check.py fukuyama` before writing any code.** Then the
`japan-city` skill, Sakai's and Higashiōsaka's shape for the food list (a
full list plus the months since, `rebuilt_register`), Matsuyama's for MHLW
beside a complete city list, Hamamatsu's for the registers. Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` has no Fukuyama
entry; its table is shared code and was not edited).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; 福山 on the Sanyō Shinkansen is dropped, JR's conventional 福山
stays); (2) **lines served only by limited expresses DO count** (2026-09-28);
(3) **the city line only**: only stations inside the city get rings, JR and
the private lines are cut at the line, **a one-station stub stays as cut**
(2026-09-27), and an URBAN line cut to a stub goes back to the owner; (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept; (5) **the name rule** (2026-09-27); (6) **no page says "currently
operating"**. Fault-based cost clauses are accepted for all of Japan.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).**
Fukuyama carries `label_tier: "minor"` and `"region": "Japan West"`, as every
wave-2 city (Kurume's entry in `app/cities.py`).

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 ("unless there is
substantial JR, JR reads as metro"): JR West has 16 of the 18 station groups
inside the city line (Ibara Railway 3, one shared at 神辺); no subway or tram.
Okayama's and Kitakyushu's precedent.

---

## The one-line summary

**All three buckets from the city's own CKAN (CC BY, PDL 1.0 by the
catalogue's terms).** The food list of permits in term on 2026-03-31 (5,880
rows, 4,355 飲食店営業, 101% of e-Stat's 4,302 in force) plus the five
monthly files since, rebuilt to **2026-08-31: 5,738 permits, 4,238
restaurants (98.5%)**; the 2025-09 to 2026-03 monthly files are already in
the full list and must not be added. **Closed premises stay in**: no status
column; MHLW's live file lacks **151** of the rebuilt new-law permits (115
restaurants), the closure candidates (open call 2). Barbers 396 and beauty
salons 1,238 (98% and 102% of official), laundries 173 (86.5%), as of
2026-08-31. Block join **90.1%**, block or MHLW's own point **95.9%**,
unplaced 0.4%. **Rail: 18 station groups** (JR Fukuen 12, JR Sanyō 5, Ibara
3), JR read from JR West's own timetables: never less than hourly 07-19.

---

## Business leg — the city's 生活衛生課 lists on CKAN

Host `https://data.city.fukuyama.hiroshima.jp` (CKAN; organisation 生活衛生課).
Every CSV resource is datastore-backed (`datastore_search` totals below).

### Food: `licensed_food`, 営業許認可等施設一覧（食品衛生関係）

| File (resource) | Bytes | Rows | What it is |
|---|---|---|---|
| `…/resource/21fec913-dc08-4344-94d1-ffb0068ab147/download/2026_3all.csv` 食品営業許認可施設一覧（全施設）（2026年3月末時点） | **1,640,035** | **5,880** | permits in term on 2026-03-31; yearly (「年に1回更新予定」); XLSX twin `2026_3all.xlsx` 915,442 B |
| `20259.csv` … `2026_3_new.csv` (2025-09 … 2026-03) | 195,431 | 701 (698 filled) | each month's NEW permits; **693 of the 698 already in the full list by permit number** |
| `20264.csv`, `20265.csv` (新規), `20266.csv`, `20267.csv`, `20268.csv` (新規更新, new and renewed) | 128,431 | 468 (434 filled, 34 empty lines) | the months since; resource ids in the check block for August (`b0a4c098-…`, 67 rows by the datastore) |

- **Encoding UTF-8 with BOM**, header on line 1. Dates 和暦 `R08.03.31` in
  the full list, ISO in the months. `wareki_date` reads every 許可年月日 /
  許可開始日 / 許可終了日; it does NOT read the Shōwa form of 初回許可年月日
  (147 rows) and 当初許可日 (165), `S63.04.01`, which no step needs.
- **Two schemas.** The full list and the 2026-03, 04 and 05 files: 施設番号,
  **施設＿名称（屋号・商号）１** / ２, **所在地１** / ２ (２ the building), **業種**,
  種目（営業の種類）（給食の種類）, **業態**, **形態**, 許可開始日, **許可終了日**,
  許可年月日, 初回許可年月日, 当初許可日. The other months: 許可番号,
  **営業所名称１** / ２, **営業所所在地１** / ２, **営業の種類**, 種目, 業態, 形態,
  **許可満了日**, 当初許可年月日. Both carry the applicant block 申請者＿郵便番号,
  申請者＿都道府県, **申請者＿住所１ / ２** (the operator's own address),
  **申請者＿申請者名**, 申請者＿役職名, **申請者＿代表者**, and 施設＿郵便番号.
- **形態** is the premises' form: 一般 5,533, 移動販売車 191, 露店 88, 自動販売機
  68 (full list). 166 vehicles are addressed `広島県内…` (95 rows contain
  一円), 25 at a fixed 福山市 address (their base).
- **The dataset's notes**: 「施設の一覧からは魚介類等行商業，短期間営業施設を除いています。」
  and 「食品営業許認可施設一覧（全施設）にはすでに廃業している施設も含まれる場合があります。」

**Against `japan_register`'s tuples (shared code, not edited here):**
`ADDR_COLS` lacks **所在地１** and **営業所所在地１**; `NAME_COLS` lacks
**施設＿名称（屋号・商号）１** and **営業所名称１**; `OPERATOR_COLS` has
申請者＿申請者名 but lacks **申請者＿代表者**; `FORM_COLS` does not read **形態**,
and 業態 (filled on most rows) would be read first anyway. `TYPE_COLS` covers
業種 and 営業の種類. `rebuilt_register` takes one `end_col`: the two schemas
spell it 許可終了日 and 許可満了日. The scratch measurement renamed columns in
memory and carried 形態 as the form wherever it is not 一般; with that every
vehicle, stall and vending row leaves the buckets through `FORM_RULES`
(移動 / 露店 / 自動販売機), and none reaches the join.

### Duplicates and closed premises (the owner's question)

- **The full list is clean of repeats by number**: 5,880 distinct 施設番号.
  129 rows repeat an (address, trade name, type) under another number (120
  groups, 100 of them restaurants): one pin per premises (trap 7) takes them.
  4,961 distinct (address, trade name) premises.
- **It holds only permits in term on its date**: every 許可終了日 is on or
  after 2026-03-31 (2026: 924 … 2032: 177). 359 restaurant permits end before
  2026-08-31 (renewed under a new number, or lapsed).
- **Base plus months double-counts two ways.** (a) The seven months before
  the full list's date are already in it (693 of 698 by number): leave them
  out. (b) A renewal arrives under a NEW number (no April-August number is in
  the full list), and 260 of the 434 April-August rows sit at a premises
  already in the full list; 226 match a same-type row whose permit ends by
  2026-10-31. A plain union counts about 244 premises twice.
  **`rebuilt_register` (latest end per address, trade name and type, kept
  while in term on the pinned 2026-08-31) resolves both: 5,738 permits, 4,238
  restaurants.** Base plus all twelve months gives 5,750 / 4,247, the full
  list alone in term on 08-31 5,340 / 3,945.
- **Closures are not marked**, in either list, and the city publishes no
  closure files. MHLW is the control: its file keeps a closed permit only in
  its closure month (14 rows, all dated 2026-08; its 7 closed permits are all
  in the city's full list), so a NEW-LAW permit absent from MHLW's live file
  is a closure candidate. **Of 4,958 new-law base permits in term on
  2026-08-31, 162 are absent (3.3%); 122 of 3,662 restaurants.** None of the
  434 April-August rows is absent. The absent rows skew old (by start year
  2021 73, 2022 21, 2023 12, 2024 7, 2025 8, 2026 1 for restaurants), as
  closures accumulate. Only 26 of the 151 rebuilt candidates carry a trade
  name found anywhere in MHLW's live file, against 1,462 of 2,000 rows that
  ARE in it by number: they are gone, not renumbered (19 share an address
  and name with a live MHLW row; read them at build). **Old-law permits
  cannot be checked** (MHLW starts 2021-06-01): 445 in term on 08-31, 334
  restaurants, all ending 2026-2027.

### Counts against the official stock

e-Stat 衛生行政報告例 FY2024 (`japan_official.estat()`), 広島県福山市, 飲食店営業
in force 2025-03-31: **4,302** (old law 1,475, revised 2,827).

| | Restaurants (飲食店営業) | Share of 4,302 |
|---|---|---|
| Full list, 2026-03-31 | **4,355** | 101.2% |
| Rebuilt to 2026-08-31 | **4,238** | 98.5% |
| Rebuilt, MHLW-absent new-law rows out (open call 2) | 4,123 | 95.8% |
| … plus MHLW's 34 restaurants in no city file (open call 1c) | 4,157 | 96.6% |
| MHLW's open restaurant permits (control) | 3,895 (2,612 addressed, 67.1%) | 90.5% |

(The master list's 3,879 is the scope's count of the same file; 3,895 here
counts 許可 rows with no 廃業年月日 and 許可満了日 on or after 2026-08-31.)

Through `japan_eigyo` (rebuilt register, fixed premises): **Food service
3,009, Retail 1,348** (Retail includes konbini and supermarkets holding a
permit, 菓子 and そうざい); after the closure filter 2,918 / 1,324.
**Economic Census control** (`scripts/japan_census_control.py` at build):
the 2021 census counts **1,737** 飲食店 establishments in 34207; 3,001
distinct placed Food-service premises is **1.73 per establishment** (1.68
after the closure filter), inside the built cities' 1.56-1.92.

### MHLW's file (34207), the control and a second source

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=34207_food_business_all.csv`:
**2,981,068 B, 8,573 rows** (許可 5,277, 届出 3,282, 許可(廃業) 7, 届出(廃業) 7),
UTF-8, the national schema (営業施設名称、屋号又は商号, 営業の種類, 業態,
営業施設所在地, 方書, 緯度 / 経度, 法人名, 法人番号, 法人住所, phones, permit dates,
廃業年月日, 申請区分). Permits 2021-06-01 to 2026-08-31.

- **The city enters every new-law permit**: 5,240 of MHLW's 5,284 permit
  numbers are in the city's files (4,806 in the full list).
- **What MHLW adds: 44 open permits in no city file** (34 restaurants), granted
  2026-06 (7), 07 (25), 08 (10) and two earlier, 41 first permitted in 2021:
  renewals the city's 新規更新 files do not list. 37 sit at an (address, trade
  name) the city lists under its older number. All addressed (42 of 44).
- **Its own coordinates**: block point against MHLW's point for the same
  permit number, **median 38 m, 96.2% within 250 m** (2,476 rows; 31 over 1
  km). For 256 of the 433 rebuilt rows the block join misses, MHLW has a
  point under the same number.
- **3,282 open notifications** (1,854 addressed): Matsuyama's partial
  food-retail bucket, if the owner follows that precedent (open call 1b).

### Personal services: `licensed_env`, 営業許認可等施設一覧（環境衛生関係）

| File (resource) | Bytes | Rows | Kinds |
|---|---|---|---|
| `…/resource/2d640e17-3225-4c59-b2f4-cdc2b104748c/download/riyoushobiyousho.csv` 理容所・美容所確認施設一覧 | **231,248** | **1,634** | 美容 1,238 · 理容 396 |
| `…/resource/bd8b8871-e656-4450-ac0b-92614eeedb3f/download/kuri-ninngu.csv` クリーニング所確認施設一覧 | **34,962** | **173** | 取次 113 · 一般 47 · 特定 10 · blank 3 |

- **As of 2026-08-31** (the dataset's notes, 「2026年8月末時点」; files
  modified 2026-09-07). UTF-8 with BOM. Columns (both): **種類**, **店名**,
  郵便, **所在地**, **営業者**, **営業者住所** (the operator's own address,
  filled on 287 and 132 rows), 確認番号, 確認日 (`H02,04,01`, commas; not
  needed).
- **Standing registers, not a stream**: 確認日 runs from Shōwa (419) through
  Heisei (839) to Reiwa (374). Notes: 「※既に廃止された施設を掲載している場合もあります。」
  So closed premises stay in; there is no control for them.
- **Official** (e-Stat FY2024 第10表 / 第11表, `data/hakodate/raw/estat_eisei_r6_*_by_city.csv`):
  barbers 405, beauty salons 1,209, laundries 200 (取次所 142). **Shares
  97.8%, 102.4%, 86.5%** (all three 1,807 of 1,814, 99.6%).
- Three laundry rows are empty (no name, address or date): drop them. Two
  exact repeats in each file; 14 premises listed as both 理容 and 美容 (one pin
  per premises and bucket keeps one). No 無店舗 or 一円 row.
- **Shared code**: `NAME_COLS` lacks **店名**, `TYPE_COLS` lacks **種類**,
  `OPERATOR_COLS` lacks **営業者** (without it the name rule compares
  nothing). The barber/beauty file mixes both kinds in one file: a
  `source_rows` split by 種類 (or `SOURCE_KIND`) so `japan_eigyo`'s source
  decides each row. 特定 is a laundry handling designated items (e-Stat's
  指定洗濯物 column counts 10, matching).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/34207-24.0a.zip` (716,683 B,
120,641 rows, **113,521 block keys**), town-chōme
`.../19.0b/34207-19.0b.zip` (11,644 B, **430**). `japan.CITIES` entry at
build: `"fukuyama": {"name": "福山市", "pref": "34", "epsg": 32653, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["34207"]}`.

| Tier (rebuilt register, fixed premises in a bucket) | All (4,357) | Food service (3,009) | Retail (1,348) |
|---|---|---|---|
| Block | **90.1%** | 91.4% | 87.2% |
| Town-chōme / 大字 centroid | 9.5% | 8.4% | 11.9% |
| Unplaced | **0.4%** | 0.2% | 0.9% |
| **Block or MHLW's own point** (`OWN_POINT_FALLBACK` by number) | **95.9%** | | |

| Registers | Barbers (396) | Beauty (1,238) | Laundry (173) |
|---|---|---|---|
| Block / chōme / unplaced | 91.9 / 7.6 / 0.5 | 89.9 / 9.1 / 1.0 | 85.5 / 11.6 / 2.9 (the 3 empty rows) |

MHLW's own addressed rows join the same way (3,992 fixed: 89.8 / 9.6 / 0.6),
the block point a median 39 m from MHLW's (3,583 rows, 95.5% within 250 m).

**The misses, read** (towns only, by `misses.py` in the scratchpad):
- **Chōme tier (414)**: 290 sit in towns MLIT's block file does not carry at
  all, the 地番 areas of the merged towns (神辺町川北 52, 内海町 50, 神辺町川南 42,
  神辺町新道上 30, 神辺町新徳田 26, 加茂町下加茂 22 …; MLIT's town file names them
  `神辺町大字川北`, and the shared 大字 rule already maps them). They take the
  大字 centroid, or MHLW's point where the permit is in MHLW.
- **Unplaced (19)**: 水呑町三新田1丁目 (6) and 2丁目 (13), a town MLIT's 24.0a and
  19.0b files lack (they hold 水呑町 and 水呑向丘 only). MHLW's point by number
  covers those it holds.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_34_GML.zip`, N03 code 34207
(**517.6 km²**, extent W 133.211, S 34.310, E 133.471, N 34.712; the
2003-2006 mergers brought in 内海町, 新市町, 沼隈町 and 神辺町). Read with
`stub_test()`'s method and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 福塩線 (西日本旅客鉄道, 11) | JR Fukuen Line | **12 / 27** | 福山, 備後本庄, 横尾, 神辺, 湯田村, 道上, 万能倉, 駅家, 近田, 戸手, 上戸手, 新市 |
| 山陽線 (西日本旅客鉄道, 11) | JR Sanyō Line | **5 / 131** | 東福山, 福山, 備後赤坂, 松永, 大門 |
| 井原線 (井原鉄道, 12) | Ibara Railway Ibara Line | **3 / 15** | 神辺, 湯野, 御領 |

- **20 station records, 18 N02_005g groups** (福山 Sanyō + Fukuen, 神辺 Fukuen
  + Ibara; both share one N02 geometry, spread 0 m). No name in two groups;
  no separate stations closer than 600 m. **Median nearest-station gap 1,531
  m** (946 to 4,927): standard rings by the spacing rule.
- **Shinkansen**: 福山 (山陽新幹線) dropped; the conventional 福山 stays.
- **Cut at the line** (named by N03 municipality at build): Sanyō 126 beyond
  (Okayama Prefecture 91, 広島市 12, 東広島市 7, 廿日市市 6, 三原市 3 …), Fukuen 15
  (府中市 8, 三次市 6, 世羅町 1), Ibara 12 (all in Okayama Prefecture).
- **The light-rail/rail test**: all three are heavy rail (N02 class 11, JR
  conventional; class 12, the Ibara Railway, a third-sector diesel railway).
  No tram or light rail.
- **The stub test passes.** No line is cut to one station. **The Ibara
  Railway's 3 groups are inside the city line**: 湯野 and 御領 are its own,
  神辺 its junction with the Fukuen Line, 2.3 to 5.6 km from the boundary. It
  is a rural third-sector line, not an urban one, and three stations are not
  a one-station stub, so the standing call draws it as cut and **no owner
  question arises**. The Sanyō Line's 5 of 131 is a main line cut at the line
  (Kurume's Kagoshima Line keeps 2), not a stub.
- **Frequency, read 2026-10-04 from JR West's own station timetables** by
  plain GET (`timetable.jr-odekake.net`, the index
  `cgi-bin/mydia_sp.cgi?MD=3&FN=0&EID=<station>` and its
  `station-timetable/<id>` pages, Wednesday 2026-10-07, data 「JR時刻表」
  2026年10月号):

  | Station (line, direction) | Weekday departures | Per hour 07-19 |
  |---|---|---|
  | 神辺 (Fukuen, to 府中) | 28, all 普通 | 1-3, no empty hour |
  | 神辺 (Fukuen, to 福山) | 30 (2 through to 岡山) | 1-3, no empty hour |
  | 神辺 (Ibara Railway, to 井原 / 総社 / 清音; JR West's page) | 26 | 1-3, no empty hour |
  | 東福山 (Sanyō, to 岡山) | 49 | 1-4 |
  | 東福山 (Sanyō, to 福山 / 尾道) | 48 | 1-4 |

  Nothing here is below an hourly service. The Ibara figures come from JR
  West's page for the shared station, not from the Ibara Railway's own site
  (not fetched). JR West's page forbids reproducing its timetable data
  (「この時刻データを無断で転載・複写し…加工することも禁じます」): only these
  counts are recorded, never a timetable on the page.
- ⚠️ **Gate 3** at build: JR West's per-line station counts (Fukuen 27, Sanyō
  inside the city 5) and the Ibara Railway's 15. **OSM `name:en`** for 18
  groups (one Overpass query at build; not queried here).

## Scope

**Fukuyama City.** JR Sanyō runs on to 尾道 and Okayama Prefecture, the
Fukuen Line to 府中 and 三次, the Ibara Railway to 井原 and 総社; cut at the
line.

## Licences — read 2026-10-04 (`licence-read`, recorded by staging)

The full read is staging's (`docs/decisions_drafts/staging.md`, "Fukuyama's
two lists read"); not re-read here.

- **`licensed_food` and `licensed_env` — PERMITTED WITH CONDITIONS.** As
  stated on the catalogue: CKAN `license_id` **cc-by** (クリエイティブ・コモンズ
  表示, no version, an opendefinition link), every resource's licence null.
  The catalogue's `/terms` (= `/about`) applies **PDL 1.0** unless a rights
  notice says otherwise, and PDL 1.0 §1.7 allows use under CC BY 4.0; the
  division pages (`seikatsueisei/108007.html` food, `107599.html` env) send
  users to `/terms`. Either reading permits the map; record both
  (Kumamoto's row shape).
  - **MUST DISPLAY** (the city's 重要情報 §1.1 template, modified form):
    `「営業許認可等施設一覧（食品衛生関係）」（福山市）（https://data.city.fukuyama.hiroshima.jp/dataset/licensed_food）を加工して作成`
    and `「営業許認可等施設一覧（環境衛生関係）」（福山市）（https://data.city.fukuyama.hiroshima.jp/dataset/licensed_env）を加工して作成`,
    who processed it (the project, never a city name), and a CC BY 4.0 link
    if CC BY governs. One combined notice for both is fine.
  - **MUST DO**: none (use is acceptance; no notice, registration or refresh).
  - **MUST NOT**: present the processed data as the city's own; city logos;
    claim completeness or currency (both notes say closed premises may
    remain). Liability fault-based (PDL 1.0 §1.6), no indemnity.
  - The main city site's copyright page (`site/userguide/16651.html`) bars
    copying but governs the city's web pages only, not the catalogue.
- **MHLW open data** (if used, open call 1): PDL 1.0 as recorded in
  `docs/data_sources/japan.md`: `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; no completeness claim; 免責 2)ウ the minor open point.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The food lists carry the applicant block**: 申請者＿申請者名 (an
  individual's own name on 2,902 of the 5,880 full-list rows by the absence
  of a company marker; a company on 2,978), 申請者＿代表者, 申請者＿役職名,
  **申請者＿住所１ / ２** and 申請者＿郵便番号. Step 2 never reads any of them
  into an output; 申請者＿申請者名 and 申請者＿代表者 are read IN MEMORY for the
  name rule only (`OPERATOR_COLS`, add 申請者＿代表者). The trade name is
  施設＿名称（屋号・商号）１ / ２ in the full list and the 2026-03 to 05 files,
  営業所名称１ / ２ in the other months (staging's read names only the second).
- **The name rule, measured in memory** (answers only, never a value): 8
  full-list rows whose trade name is the operator's own name (4 restaurants),
  7 in the rebuilt register. The registers: **0** (営業者: 1,347 of 1,634
  barber/beauty rows and 38 of 173 laundries carry no company marker).
- **営業者住所** (the registers' operator address) is never selected; select
  種類, 店名, 所在地 only.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; its rows
  cannot take the name rule (Fukuoka's precedent).
- Run `check_personal_exposure.py fukuyama` (`japan=True`) after step 2: the
  test that matters is the sole-trader rows, where a trade name can be a
  person's name; it must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"`, `label_tier: "minor"`, `"country": "Japan"`. The
city's ISJ points run 133.224-133.454 E: project to **UTM 53N
(EPSG:32653)**. OSM box from the N03 extent, rounded out: (34.30, 133.20,
34.72, 133.48). Scaffold with `scripts/scaffold_city.py ... --page-number
<N>`, the number claimed at build from `docs/session_roles.md` (Fukuyama is
not in `docs/staged_cities.json`).

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; `mode: metro`;
the minor tier and Japan West; the Ibara Railway and the Sanyō Line drawn as
cut (standing call, no stub); the Shinkansen out.

**Open, each with a recommendation:**

1. **MHLW beside the city's complete list: follow Matsuyama** (owner,
   2026-10-02, "approve all recommendations"). (a) **Its own point** where
   the block join misses, by permit number: block-or-own 90.1% → 95.9%.
   *Recommend yes.* (b) **Its 3,282 notifications as a partial, opt-in
   Food-shops layer** (1,854 addressed; konbini, supermarkets, greengrocers),
   disclosed as partial as in Fukuoka, Hiroshima and Matsuyama. *Recommend
   yes, on Matsuyama's precedent*; the tradeoff is a bucket the page must
   call partial. (c) **Its 44 open permits in no city file** (34
   restaurants, mostly 2026-06 to 08 renewals), with `SUPERSEDES` for the
   duplicates. *Recommend yes*: small, current, and the city's months miss
   them. Any of the three adds MHLW's PDL credit to the notice.
2. **A closure filter from MHLW's live file**: drop a rebuilt NEW-LAW permit
   whose number MHLW no longer holds (151 rows, 115 restaurants; restaurants
   4,238 → 4,123, 95.8% of official). *Recommend yes*: MHLW keeps a closed
   permit only in its closure month, the absent rows skew to older permits,
   and only 26 of 151 carry a trade name anywhere in MHLW against 73% of a
   control. Tradeoff: a new method with no precedent; a permit withheld
   wholly from MHLW's open file would be lost with it; the 334 old-law
   restaurants stay unchecked, so the page still says the list may include
   closed premises. Without it the map is Kyoto's upper bound, disclosed.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control, `screen_japan_join.py
  minato` 98.0 / 0.2 / 1.8, and every city screen): `ADDR_COLS` + 所在地１,
  営業所所在地１; `NAME_COLS` + 施設＿名称（屋号・商号）１, 営業所名称１, 店名;
  `OPERATOR_COLS` + 申請者＿代表者, 営業者; `TYPE_COLS` + 種類 (or a
  `source_rows` that names the kind); 形態 read as the form where not 一般
  (a `source_rows` in the city's config, or a shared reading); the two
  expiry spellings in `rebuilt_register`.
- `as_of` pinned to **2026-08-31** (the last month read), never today; the
  full list's 2025-09 to 2026-03 months left out.
- The 19 closure candidates that share an address and name with a live MHLW
  row (another type, or a renamed permit).
- Gate 3 (JR West, Ibara Railway), OSM `name:en`, line colours on both
  basemaps, the opening view (`map-view`), the factory share, the Economic
  Census control (estimated 1.73), `check_provenance.py`,
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "fukuyama-food-full-list-rows",
    "claim": "The city's full food list (permits in term on 2026-03-31) has 5,880 rows in the CKAN datastore",
    "kind": "ckan_rows",
    "domain": "data.city.fukuyama.hiroshima.jp",
    "resource_id": "21fec913-dc08-4344-94d1-ffb0068ab147",
    "expect": 5880
  },
  {
    "id": "fukuyama-food-full-list-fields",
    "claim": "The full list's premises columns, its 形態 and expiry, and the applicant block step 2 must never output",
    "kind": "ckan_fields",
    "domain": "data.city.fukuyama.hiroshima.jp",
    "resource_id": "21fec913-dc08-4344-94d1-ffb0068ab147",
    "present": ["施設＿名称（屋号・商号）１", "所在地１", "業種", "業態", "形態", "施設番号", "許可終了日", "申請者＿申請者名", "申請者＿代表者", "申請者＿住所１"]
  },
  {
    "id": "fukuyama-food-aug-rows",
    "claim": "The August 2026 new-and-renewed food file has 67 rows (25 of them empty lines) in the datastore",
    "kind": "ckan_rows",
    "domain": "data.city.fukuyama.hiroshima.jp",
    "resource_id": "b0a4c098-d6b3-4a19-b5aa-adee03efd7bc",
    "expect": 67
  },
  {
    "id": "fukuyama-food-aug-fields",
    "claim": "The monthly files use the second schema (営業所名称１, 営業所所在地１, 許可満了日)",
    "kind": "ckan_fields",
    "domain": "data.city.fukuyama.hiroshima.jp",
    "resource_id": "b0a4c098-d6b3-4a19-b5aa-adee03efd7bc",
    "present": ["営業所名称１", "営業所所在地１", "営業の種類", "形態", "許可番号", "許可満了日"]
  },
  {
    "id": "fukuyama-food-dataset-page",
    "claim": "The food dataset states CC BY, a yearly full list, that closed premises may remain, and offers the August 2026 new-and-renewed file",
    "kind": "http_contains",
    "url": "https://data.city.fukuyama.hiroshima.jp/dataset/licensed_food",
    "present": ["クリエイティブ・コモンズ", "年に1回更新予定", "すでに廃業している施設も含まれる場合があります", "2026年8月新規更新食品営業許可施設一覧"]
  },
  {
    "id": "fukuyama-barber-beauty-rows",
    "claim": "The barber and beauty-salon list (as of 2026-08-31) has 1,634 rows",
    "kind": "ckan_rows",
    "domain": "data.city.fukuyama.hiroshima.jp",
    "resource_id": "2d640e17-3225-4c59-b2f4-cdc2b104748c",
    "expect": 1634
  },
  {
    "id": "fukuyama-barber-beauty-fields",
    "claim": "The register's columns, including the operator name and the operator's own address never selected",
    "kind": "ckan_fields",
    "domain": "data.city.fukuyama.hiroshima.jp",
    "resource_id": "2d640e17-3225-4c59-b2f4-cdc2b104748c",
    "present": ["種類", "店名", "所在地", "営業者", "営業者住所"]
  },
  {
    "id": "fukuyama-laundry-rows",
    "claim": "The laundry list (as of 2026-08-31) has 173 rows",
    "kind": "ckan_rows",
    "domain": "data.city.fukuyama.hiroshima.jp",
    "resource_id": "bd8b8871-e656-4450-ac0b-92614eeedb3f",
    "expect": 173
  },
  {
    "id": "fukuyama-env-dataset-page",
    "claim": "The environmental-hygiene dataset states CC BY, its 2026-08-31 date and that closed premises may remain",
    "kind": "http_contains",
    "url": "https://data.city.fukuyama.hiroshima.jp/dataset/licensed_env",
    "present": ["クリエイティブ・コモンズ", "2026年8月末時点", "既に廃止された施設を掲載している場合もあります", "理容所・美容所確認施設一覧"]
  },
  {
    "id": "fukuyama-mhlw-live",
    "claim": "MHLW's open-data file for Fukuyama (34207) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=34207_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "fukuyama-isj-block-live",
    "claim": "MLIT's block-level address file for Fukuyama (34207) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/34207-24.0a.zip",
    "min_bytes": 500000
  },
  {
    "id": "fukuyama-isj-chome-live",
    "claim": "MLIT's town-chōme file for Fukuyama (34207) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/34207-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "fukuyama-jr-kannabe-timetable",
    "claim": "JR West's timetable index for 神辺 (EID 0651703) lists the Fukuen Line both ways and the Ibara Railway - the frequency source",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/cgi-bin/mydia_sp.cgi?MD=3&FN=0&EID=0651703",
    "present": ["神辺駅", "新市・府中方面", "福山方面", "井原・清音方面"]
  },
  {
    "id": "fukuyama-jr-higashifukuyama-timetable",
    "claim": "JR West's timetable index for 東福山 (EID 0650625) lists the Sanyō Line both ways",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/cgi-bin/mydia_sp.cgi?MD=3&FN=0&EID=0650625",
    "present": ["東福山駅", "新倉敷・岡山方面", "福山・尾道方面"]
  },
  {
    "id": "fukuyama-projected-crs",
    "claim": "Fukuyama projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 133.36,
    "expect": "EPSG:32653"
  }
]
```
