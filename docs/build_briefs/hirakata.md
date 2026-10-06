# Hirakata — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 112: `docs/decisions_drafts/staging.md`, "Wave 5, second half: calls
95 to 141"). The Step 0 downloads were approved by the owner 2026-10-06
(call 147). **Step 0 measured 2026-10-06** (staging). Into
`data/hirakata/raw/` (gitignored), each from its publisher's own host with the
project user-agent, each HTTP 200, under each URL's own file name as
`japan_fetch.get` saves:

- From `www.city.hirakata.osaka.jp` (枚方市保健所 保健衛生課), under
  `/cmsfiles/contents/0000023/23479/`: the food list
  `272108_food_business_all_202603_end.csv` (409,683 B, every permit in term
  at the end of March 2026) and the five monthly new-permit files
  `272108_food_business_new_202604.csv` … `_202608.csv` (6,257 + 6,389 +
  6,865 + 6,948 + 2,858 B); under `/cmsfiles/contents/0000025/25284/`: the
  barber, beauty and laundry registers `riyouall.xlsx` (29,419 B),
  `biyouall.xlsx` (69,664 B) and `cleaningall.xlsx` (26,636 B), as of the end
  of March 2026.
- From `i2fas.mhlw.go.jp`: `27210_food_business_all.csv` (383,368 B), the
  control.
- From `nlftp.mlit.go.jp`: `isj/27210-24.0a.zip` (208,806 B) and
  `isj/27210-19.0b.zip` (10,990 B).

**1,167,883 B in all.** Nothing else was downloaded. **Not fetched**: the
registers' five monthly XLSX files (beauty 2026-04 to 07, barber 2026-07),
which the approval did not name (open call 2), and the page's PDF twins,
lodging, 興行場, public-bath, minpaku and hot-spring lists (out of scope).

**Run `python scripts/brief_check.py hirakata` before writing any code.** Then
the `japan-city` skill, **Higashiōsaka's and Ichinomiya's shape**: a full list
plus monthly new permits merged by `rebuilt_register` with the full list kept
whole (`docs/build_briefs/ichinomiya.md`, call 126), Hamamatsu's for the
registers (one file per kind), Ichinomiya's for MHLW's notifications beside a
city list (call 127). Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Hirakata entry; its table is shared
code and was not edited). Rail: MLIT N02-25 cut at the N03 city line, through
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
holds, and 法人名 is an operator column (2026-10-05); (6) **no page says
"currently operating"**. Also: no frequency floor for JR or private lines in
Japan (owner, 2026-10-06, call 46), any stretch at about 11 trains a day or
fewer named and drawn (call 86; none here); fault-based cost clauses accepted
for all of Japan (2026-09-24); English station names from OSM `name:en`;
every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Applied from the precedents of 2026-10-06 (do not re-ask):** the March
list **kept whole plus the monthly files** (Ichinomiya, call 126); **MHLW's
notifications as a partial Food-shops layer** (call 127b: 495 addressed rows,
hundreds, not a thin set); **MHLW's own point where the block join misses**
(127c); MHLW's permits not in the city's files left out (126).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).**
Hirakata carries `label_tier: "minor"` and goes in the **Japan West** view
today; wave 4's first city to land retags Japan into the eight regions with
**Osaka Prefecture** a view of its own, and Hirakata goes there. Its label
offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200),
never by eye; whether it joins `KNOWN_STACKED` (with Neyagawa, if built) is
that script's answer.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 ("unless there is
substantial JR, JR reads as metro"): JR has 3 station groups against Keihan's
9, so the backbone decides, and Keihan's Main and Katano lines are railways
(N02 class 12), not trams. Nara's (Kintetsu) and Kurume's (Nishitetsu)
precedent; Ōtsu's `light_rail` rests on Keihan's class-21 Ōtsu lines, which
do not run here.

---

## The one-line summary

**All three buckets from the city's own files (CC BY 2.1 JP as stated; the
licence read is pending).** The food list of every permit in term at the end
of March 2026 holds **3,175 rows, 2,528 restaurants (飲食店営業 2,054 plus
（旧）飲食店営業 474) = 84.7% of e-Stat's 2,984 in force**; the five monthly
files add 236 new permits, and the merge (the March list kept whole, call
126) gives **3,221 permits, 2,560 restaurants (85.8%)**. **The list leaves out
stalls, vehicles and vending by its own note** (露店、自動車、自動販売機), which
e-Stat counts: on Toyonaka's vehicle share the fixed premises would be about
98-99% covered (an estimate, open call 1). Old-law permits are in (not
Kurashiki's trap). Barbers 237, beauty salons 814, laundries 206 as of
2026-03-31: **99.2%, 102.8%, 100.0% of official**. Through `japan_eigyo`:
**Food service 2,562, Retail 579** fixed premises. Block join **97.2%**
(food), **99.2-99.5%** (barbers, beauty), 96.6% (laundry); 2 food rows
unplaced. **Rail: 12 N02 station groups** (Keihan Main Line 6, Katano Line 4,
枚方市 shared; JR Gakkentoshi Line 3), read from the operators' own
timetables: Keihan every 11-12 minutes at its local stations, JR every 15.

---

## Business leg — the city's 保健衛生課 lists

Host `https://www.city.hirakata.osaka.jp` (the city's own CMS; no catalogue
API). The host sends no charset (`Content-Type: text/html`), so the checks
below use ASCII anchors.

### Food: 食品等営業許可施設について, page 0000023479

Page `https://www.city.hirakata.osaka.jp/0000023479.html` (更新日 2026-09-29),
titled 食品等営業許可施設について（露店、自動車及び自動販売機による営業を除く）.
Its notes: stalls, vehicles, vending machines and unattended automatic
cooking machines are left out; 許可番号 `101-…` is a new permit, `102-…` a
renewal; a variant character shows as 「・」 or 「？」; the address may run to
a second line (building, room); **the full list is updated twice a year**, the
monthly new permits around the 15th of the next month.

| File (under `…/0000023/23479/`) | Bytes | Rows | What it is |
|---|---|---|---|
| `272108_food_business_all_202603_end.csv` 2026年3月末日時点 全ての許可施設 | **409,683** | **3,175** | every permit in term at 2026-03-31 (許可年月日 2020-03-04 to 2026-03-31; 許可満了年月日 2026-03-31 to 2032-03-31) |
| `272108_food_business_new_202604.csv` … `_202608.csv` 新規許可施設 | 29,317 | **236** (50, 52, 56, 55, 23) | each month's NEW permits (`101-` only), 2026-04-01 to 2026-08-31 |

- **cp932, CRLF, header on line 1**; `japan_register.city_rows` reads all of
  them. Dates are ISO in the full list and the April file, `2026/5/14` from
  May; `wareki_date` reads both.
- **Columns**: No., **許可番号**, **営業所名称**, **営業所所在地①**,
  **営業所所在地②** (the building line, filled on 803 of 3,411 rows),
  **営業者氏名** (the operator), 施設電話番号, **営業の種類**, **許可年月日**,
  **許可満了年月日**. **No 業態 column and no coordinates.**
- ⚠️ **Against the shared tuples:** `NAME_COLS` has 営業所名称,
  `TYPE_COLS` 営業の種類, `OPERATOR_COLS` 営業者氏名, but **`ADDR_COLS` lacks
  営業所所在地①** (the circled digit): without it every row reads an empty
  address, `permits_from_rows` calls every row "not a premises" and
  `rebuilt_register` collapses every permit of one name and type into one
  key. The scratch measurement renamed it in memory; the build adds it to
  `ADDR_COLS` after every older spelling (or renames it in `source_rows`) and
  re-runs the Minato control. ② is not needed for the join.
- **Types** (full list): 飲食店営業 2,054, （旧）飲食店営業 474, 菓子製造業 261,
  食肉販売業 80, （旧）菓子製造業 63, 魚介類販売業 63, （旧）食肉販売業 37,
  そうざい製造業 37, … 34 spellings; `japan_eigyo`'s normaliser strips the
  （旧） mark (Higashiōsaka's precedent).
- **No address is citywide** (0 rows with 一円 or 市内; 3,173 begin 枚方市):
  vehicles and stalls are not in the list at all, as its title says.
- 17 trade names carry the 「？」 placeholder for a variant character (the
  page's own note): shown as the city writes them.

### Old-law coverage (Kurashiki's trap) — not this list's problem

- **Old-law permits are in the file**: 623 rows (474 restaurants), every one
  begun 2020-03-04 to 2021-05-31 on a 6-year term, ending 2026-03-31 to
  2027-05-31; 24 to 55 a month across 2020-03 to 2021-05. 340 of them are
  old-law renewals (`102-`, begun 2020-21); every `101-` row is a new permit.
  A permit begun before 2020-03 had ended by the list's date.
- **e-Stat 衛生行政報告例 FY2024** (`japan_official.estat()`), 大阪府枚方市,
  飲食店営業 in force 2025-03-31: **2,984** (old law 954, revised 2,030). A
  year later the list holds 474 old-law and 2,054 revised-law restaurants:
  the old-law stock converting, as e-Stat shows elsewhere.
- **Retail types against the same tables**: 菓子 324 of 334 (97.0%), そうざい
  42 of 44 (95.5%), 魚介類販売 85 of 87 (97.7%), 食肉販売 117 of 122 (95.9%).
  Retail types run from vehicles far less often than restaurants, so the
  95-98% here is close to the list's coverage of fixed premises a year on.

### The food share (the key measurement)

| | Restaurants | Share of 2,984 |
|---|---|---|
| March list alone (2026-03-31) | **2,528** | **84.7%** |
| **March list kept whole + the months** (call 126) | **2,560** | **85.8%** |
| Rebuilt, in term on 2026-08-31 | 2,503 | 83.9% |
| March list alone, in term on 2026-08-31 | 2,360 | 79.1% |
| MHLW's open restaurant permits (control) | 81 | 2.7% |

**Reading.** The list excludes stalls, vehicles and vending by design; e-Stat
counts them. Hirakata's own share of those is not published anywhere this
brief could read. **Toyonaka's list**, the same prefecture, keeps them and
measured 496 of 3,515 restaurants (14.1%) addressed citywide
(`docs/build_briefs/toyonaka.md`); at that share Hirakata's fixed restaurants
would be about 2,563, and the list's 2,528 about **98.6%** of them. The
retail types' 95-98% (few vehicles) point the same way. **An estimate,
not a measurement**: open call 1.

### The months, renewals and closures (the merge)

- **Unique by (許可番号, 許可年月日)**: 3,175 distinct; the number alone
  repeats (1,050 distinct; it restarts each year). No monthly row is in the
  March list by number and date.
- **The months carry the old-law conversions.** 232 March permits (179
  restaurants), every one old-law, end 2026-04 to 08; **143 of them reappear
  in a month at the same (address, trade name, type)**, the new permit
  granted within 59 days before the old one ends (140) or earlier (4). 92
  monthly rows (73 restaurants) are new premises. About 566 new permits a
  year at this rate.
- **No closure list, no status column**: closed premises are invisible until
  the next full list (twice a year). The 89 old-law permits ending by
  2026-08-31 with no monthly row are kept, as call 126 keeps them (closed,
  lapsed or re-permitted unseen); the page keeps "may include closed
  premises".
- **The merge** (`rebuilt_register` with `as_of` 2026-03-31,
  `end_col="許可満了年月日"`, after the `ADDR_COLS` fix): latest end per
  (address, trade name, type without （旧）), **3,221 permits, 2,560
  restaurants**. 44 premises keys repeat within the March list (46 rows); the
  merge takes them.

### Counts through `japan_eigyo` (merged, fixed premises)

**Food service 2,562, Retail 579** (菓子 326, butcher 122, fishmonger 85, deli
46; 3,141 storefront rows; one pin per (address, name, bucket): 2,562 and
484). Left out: 80 manufacturing types with no rule (添加物 9, アイスクリーム類
12, 麺類 7, 豆腐 6, …), as in every built city; no mobile row. **No 業態, so
`FORM_RULES` sees nothing**: konbini, supermarkets, canteens and bars holding
飲食店営業 stay in Food service (by trade-name word, counts only: konbini
chains 124, supermarkets 69, canteen, school or hospital words 129, snack,
bar, lounge or club 67), Kobe's, Osaka's, Toyonaka's and Aomori's way.
Factory words (工場 / センター) in 45 bucketed names: measured and kept.

**Economic Census control** (`scripts/japan_census_control.py` at build):
the 2021 census counts **966** 飲食店 establishments in 27210
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 2,560 placed Food-service
premises is **2.65 per establishment**, ⚠️ **above the built cities'
1.56-1.92** and above Toyonaka's 2.27 and Aomori's 2.33. Likely readings, for
the build to test: no 業態 (konbini, supermarkets and canteens counted as
restaurants), premises that closed without their permit lapsing, and one
premises under two permits. Record the figure and the reading.

### MHLW's file (27210): a control, and notifications

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27210_food_business_all.csv`:
**383,368 B, 1,203 rows** (届出 1,107, 許可 94, 届出(廃業) 1, 許可(廃業) 1),
UTF-8 with BOM, the national schema.

- **Permits: 94 open (81 restaurants, 62 addressed)**, granted 2021-10-04 to
  2026-08-26; **88 match a city row by (許可番号, 許可年月日)**. The other 6
  stay out (call 126). No closure control (2 closed rows).
- **Notifications: 1,107 open, 495 addressed** (その他の食料・飲料販売業 253,
  百貨店・総合スーパー 68, vending 47, 集団給食施設 23, 行商 15, 乳類販売業 13,
  コンビニエンスストア 13, 野菜果物販売業 12, …; 業態 ドラッグストア 30,
  食品スーパー 9). Of 472 fixed addressed rows, `japan_eigyo` buckets **361
  as Retail**, 111 none: **the partial Food-shops layer (call 127b,
  applied)**, disclosed as partial.
- **Its own point**: the notifications join at block 91.5%, chōme 6.6%,
  unplaced 1.9% (9 rows); block point against MHLW's own point **median 39 m,
  94.2% within 250 m** (432 rows, 2 over 1 km). Its point serves where the
  join misses (127c).

### Personal services: 環境衛生営業施設について, page 0000025284

Page `https://www.city.hirakata.osaka.jp/0000025284.html` (更新日 2026-08-20):
every permitted or confirmed premises as of the end of March 2026, **premises
already closed at publication left out** (「掲載時点で廃業している施設は除きます。」),
plus monthly new-premises files for 2026-04 to 07.

| File (under `…/0000025/25284/`) | Bytes | Rows | Official (e-Stat FY2024 第10表 / 第11表) | Share |
|---|---|---|---|---|
| `riyouall.xlsx` 理容所施設一覧（令和8年3月末） | **29,419** | **237** | barbers 239 | **99.2%** |
| `biyouall.xlsx` 美容所施設一覧（令和8年3月末） | **69,664** | **814** | beauty salons 792 | **102.8%** |
| `cleaningall.xlsx` クリーニング所施設一覧（令和8年3月末） | **26,636** | **206** | laundries 206 (取次所 161, 指定洗濯物 11) | **100.0%** |

(Official from `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
`…_cleaning_by_city.csv`, 大阪府枚方市; 無店舗取次店 operators 7, not premises.)

- **One sheet each** (【環境】台帳一覧（理容所） and its twins); columns
  **施設名称**, **施設所在地**, 施設ビル名, **開設者(申請者)** (the operator),
  開始年月日 (ISO), 確認番号. **No type column and no phone column.**
  `city_rows` finds the header; `ADDR_COLS` has 施設所在地 and `NAME_COLS`
  施設名称. ⚠️ **`OPERATOR_COLS` lacks 開設者(申請者)**: the name rule's
  operator comparison sees nothing without it (measured 0 hits either way,
  renamed in memory); the build adds it to the shared tuple or renames it in
  `source_rows`. One file per kind, so the config names the kind per file
  (Hamamatsu's registers).
- Every address is in 枚方市; no mobile, 一円 or 無店舗 row; 3 laundry names
  contain 取次 (pick-up shops, in Laundry as everywhere). Repeats: beauty 8
  (address, name); **6 premises are in both the barber and beauty
  registers** (one pin per premises and bucket keeps one per bucket).
- **Standing registers**: 開始年月日 from 1949 (beauty) and the 1960s; beauty
  2010s 248 and 2020s 244.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27210-24.0a.zip` (208,806 B,
**10,962 block keys** with the 小字 aliases), town-chōme
`.../19.0b/27210-19.0b.zip` (10,990 B, **395**). `japan.CITIES` entry at
build: `"hirakata": {"name": "枚方市", "pref": "27", "epsg": 32653, "n02":
"25", "rules": WAVE2_RULES, "wardless": True, "wards": ["27210"]}`.

| Tier, today's shared code (address renamed) | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| Food, merged, fixed premises in a bucket (3,141) | **97.2%** | 2.7% | **0.1%** (2 rows) |
| … Food service (2,562) / Retail (579) | 97.4% / 96.5% | 2.5 / 3.5 | 0.1 / 0 |
| Barbers (237) | **99.2%** | 0.8% | 0 |
| Beauty salons (814) | **99.5%** | 0.5% | 0 |
| Laundries (206) | **96.6%** | 3.4% | 0 |

**The misses, read** (towns only): the chōme tier is spread thin, 高塚町 10,
長尾荒阪1丁目 7, 招提東町2丁目 5, then 1 to 3 a town (長尾播磨谷, 御殿山南町,
岡本町, 尊延寺, 禁野本町1丁目, …), addresses whose block number MLIT lacks.
**Unplaced**: 2 food rows whose parsed town is a bare number (the address
carries a lot number where the town should be): read them at build.
Nothing calls for a shared rule, and the block share is far above call 145's
tier disclosure.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_27_GML.zip`, N03 code 27210
(**65.1 km²**, extent W 135.614, S 34.773, E 135.747, N 34.881). Read with
`stub_test()` and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 records | Stations inside |
|---|---|---|---|
| 京阪本線 (京阪電気鉄道, 12) | Keihan Main Line | **6 / 41** | 光善寺, 枚方公園, 枚方市, 御殿山, 牧野, 樟葉 |
| 交野線 (京阪電気鉄道, 12) | Keihan Katano Line | **4 / 8** | 枚方市, 宮之阪, 星ヶ丘, 村野 |
| 片町線 (西日本旅客鉄道, 11) | JR Gakkentoshi Line (片町線) | **3 / 24** | 長尾, 藤阪, 津田 |

- **13 station records, 12 `N02_005g` groups**: **枚方市** is one group
  (006563, Main + Katano, 15 m). No name in two groups; no stations closer
  than 600 m (closest 733 m). **Median nearest-group gap 1,510 m** (733 to
  2,206): rings by the spacing rule at build.
- **Shinkansen**: none in the city.
- **Cut at the line** (by N03 municipality): the Main Line 35 beyond (Kyoto
  Prefecture 17, Osaka City 8, Kadoma 4, Neyagawa 3, Moriguchi 3), the Katano
  Line 4 (Katano 4: 郡津 to 私市), the Gakkentoshi Line 21 (other prefectures
  9, Daitō 3, Osaka City 3, Katano 2, Higashiōsaka 2, Neyagawa 1, Shijōnawate
  1).
- **The stub test passes**: the Katano Line keeps 4 of 8, the Main Line 6 of
  41, the Gakkentoshi Line 3 of 24; no one-station stub, no owner question.
- **The light-rail / rail test**: Keihan's two lines are railways (N02 class
  12), JR conventional (11); no tram or light rail.
- **Frequency, READ 2026-10-06 from the operators' own timetables** by the
  wave-5 probe (plain GET, project agent), re-counted here from its cached
  copies, weekday departures 10:00-15:59:

  | Line, stations | Source | Direction | Per hour (all day) |
  |---|---|---|---|
  | Keihan Main: 光善寺, 枚方公園 | `keihan.co.jp/traffic/time-fare/pdf/time01-1.pdf` (2026-08-24 timetable) | toward 出町柳 | **5.3** (128, 133) |
  | Keihan Main: 御殿山, 牧野 | the same | toward 出町柳 | **5.0, every 12 min** (110 each) |
  | Keihan Main: 枚方市 / 樟葉 | the same | toward 出町柳 | 13.2 / 10.3 (267 / 227) |
  | Keihan Katano: 村野, 星ヶ丘, 宮之阪 → 枚方市 | `…/time02-1.pdf` | toward 枚方市 | **4.7-4.8, every 12-13 min** (95) |
  | JR Gakkentoshi: 津田, 藤阪 | `timetable.jr-odekake.net/station-timetable/2886067001`, `…/2897067001` | toward 京橋 | **4.0, every 15 min** (84) |
  | JR Gakkentoshi: 長尾 | `…/2885067001`, `…/2885067002` | toward 京橋 | 4.3-4.7 (122-125) |

  No stretch near 11 trains a day; no floor applies (call 46). Only counts
  are recorded, never a timetable on the page.
- ⚠️ **Gate 3** at build: Keihan's and JR West's per-line station counts
  inside the city (Main 6, Katano 4, Gakkentoshi 3); **OSM `name:en`** for
  12 groups (one Overpass query at build, in the box below; not queried
  here); line colors on both basemaps. The JR line's label is its public
  name, 学研都市線 (Gakkentoshi Line), not N02's 片町線.

## Scope

**Hirakata City.** The Keihan Main Line runs on to Osaka City and to Kyoto
Prefecture, the Katano Line to Katano, the Gakkentoshi Line to Kyōtanabe and
to Osaka City; cut at the line.

## Licences — as stated; the read is pending

**As stated on each page**: the food and 環境衛生 pages and the city's open-data
page (`https://www.city.hirakata.osaka.jp/0000017270.html`) carry the same
利用条件: free use and adaptation, derivative works allowed, and a statement
that the city's data was used, linked to `creativecommons.org/licenses/by/2.1/jp/`,
with 表示例 (an unaltered copy: 「[データのタイトル]、枚方市、クリエイティブ・コモンズ・ライセンス 表示 2.1」;
an adaptation: its own wording). **CC BY 2.1 JP, claims settled by the owner
on Sagamihara's precedent** (the master list's band row, call 112). **A
licence-read agent reads the city's terms separately; staging records its
verdict and the credit wording.** No verdict is written in this brief.

- **MHLW open data** (notifications and own points, calls 127b and 127c):
  PDL 1.0 as recorded in `docs/data_sources/japan.md`, its 出典 line and who
  processed it; no completeness claim.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **Keihan's and JR West's timetables**: read for counts only, never
  reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **Food: 営業者氏名 is the operator column**, a company or cooperative marker
  on 1,621 of 3,175 full-list rows and **none on 1,554** (where an
  individual's own name sits). Read IN MEMORY for the name rule only
  (`OPERATOR_COLS` has it); never selected. **施設電話番号** (2,461 filled) is
  never selected. No operator address column.
- **The name rule, measured in memory** (answers only, never a value): **1
  food row**, a fixed restaurant, whose trade name is a bare personal name
  (version 2's sign test); no further row where the trade name equals an
  individual operator's name; the merged register the same (1).
- **Registers: 開設者(申請者)** (no company marker on 214 of 237 barbers, 627
  of 814 beauty salons, 105 of 206 laundries); select 施設名称 and 施設所在地
  (and 施設ビル名 only if the join needs it, which it does not). Name rule:
  **0** bare personal names, 0 operator matches.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; its 法人名
  joins the name rule (2026-10-05): **0** flags on the 495 addressed
  notifications.
- Run `check_personal_exposure.py hirakata` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Osaka Prefecture after the retag),
`label_tier: "minor"`, `"country": "Japan"`. Project to **UTM 53N
(EPSG:32653)**: the N03 centroid lies at longitude 135.682, the extent
135.614-135.747, inside the 132-138 band (computed here, never copied). OSM
box from the N03 extent, rounded out: (34.77, 135.61, 34.89, 135.75).

**Scaffold**: `scaffold_city.py --slug hirakata --name Hirakata --system-name
"Keihan and JR West" --taxonomy japan_eigyo --lat 34.818 --lon 135.682
--region "Japan West" --country Japan --mode metro --page-number <N>`
(`--dry-run` first), the number claimed in `docs/session_roles.md` at build.

## Owner calls

**Made (do not re-ask):** Band A (owner, 2026-10-06, call 112); the Step 0
downloads (call 147); the standing Japanese calls above; CC BY 2.1 JP's
claims settled on Sagamihara's precedent; `mode: metro`; the minor tier,
Japan West now and Osaka Prefecture after the retag; the March list kept
whole plus the months (126); MHLW's notifications as a partial Food-shops
layer (127b) and its own point where the join misses (127c); MHLW's 6 extra
permits out (126); no frequency floor (call 46); no stub.

**Open, each with a recommendation:**

1. **The food share on the page** (call 125's question for a list below
   about 90%). The list holds 85.8% of e-Stat's restaurants, and the gap is
   the list's own stated exclusion of stalls, vehicles and vending, which
   every built Japanese page leaves out anyway. *Recommend no share
   sentence*: name the exclusion in the businesses bullet and What Is
   Excluded, as for vehicles and stalls elsewhere; Band A stands. Tradeoff:
   the "about 98.6% of fixed premises" reading leans on Toyonaka's 14.1%
   vehicle share, not on a Hirakata count; if the owner wants the figure
   stated, Ichinomiya's sentence shape (call 125) carries "about six
   restaurants in seven of the official count".
2. **The registers' monthly files** (page 0000025284: `biyouapr.xlsx`
   11.6 KB, `beautymay.xlsx` 11.8 KB, `beauty6.xlsx` 11.9 KB, `btjul.xlsx`
   11.7 KB, `bbjul.xlsx` 11.5 KB; no laundry month; same publisher, same
   licence statement; not in call 147's approval, not fetched). *Recommend
   approving them at build*, on Ichinomiya's call 128, so the registers take
   their new premises to 2026-07 with the food months. Tradeoff: one more
   approval for a few dozen salons; without them the registers' date is
   2026-03-31 (`SOURCE_AS_OF` per source, Fukuoka's several-dates
   precedent).

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `ADDR_COLS` + 営業所所在地① (or a `source_rows` rename; without
  it the food list reads no premises); `OPERATOR_COLS` + 開設者(申請者).
- ⚠️ **`config.source_rows`** for food: `rebuilt_register` over the March
  list and the five months, `end_col="許可満了年月日"`, `as_of` 2026-03-31
  (call 126); expect 3,221 permits, 2,560 restaurants. The page's date reads
  "permits in term on 2026-03-31, with new permits to 2026-08-31", never
  today. A later full list (twice a year) replaces the March one: re-measure.
- The census ratio (2.65, above the built range) and its reading; the 2
  unplaced food rows; MHLW's notifications as the partial layer with its own
  points.
- Gate 3, OSM `name:en`, line colors on both basemaps, the opening view
  (`map-view`), the factory share, `check_provenance.py`,
  `check_scope_disclosure.py`, `check_macro_labels.py`.

```brief-checks
[
  {
    "id": "hirakata-food-page",
    "claim": "The food page offers the full list at the end of March 2026 and the five monthly new-permit CSVs (2026-04 to 08) under CC BY 2.1 JP. ASCII anchors only: the host sends no charset",
    "kind": "http_contains",
    "url": "https://www.city.hirakata.osaka.jp/0000023479.html",
    "present": ["272108_food_business_all_202603_end.csv", "272108_food_business_new_202604.csv", "272108_food_business_new_202608.csv", "creativecommons.org/licenses/by/2.1/jp"]
  },
  {
    "id": "hirakata-food-file",
    "claim": "The full food list (409,683 B, 3,175 permits) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.hirakata.osaka.jp/cmsfiles/contents/0000023/23479/272108_food_business_all_202603_end.csv",
    "min_bytes": 350000
  },
  {
    "id": "hirakata-food-aug-file",
    "claim": "The August 2026 new-permit file (2,858 B, 23 permits) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.hirakata.osaka.jp/cmsfiles/contents/0000023/23479/272108_food_business_new_202608.csv",
    "min_bytes": 2000
  },
  {
    "id": "hirakata-registers-page",
    "claim": "The environmental-hygiene page offers the barber, beauty and laundry lists and the registers' monthly files (beauty 2026-04 to 07, barber 2026-07) under CC BY 2.1 JP",
    "kind": "http_contains",
    "url": "https://www.city.hirakata.osaka.jp/0000025284.html",
    "present": ["riyouall.xlsx", "biyouall.xlsx", "cleaningall.xlsx", "biyouapr.xlsx", "bbjul.xlsx", "btjul.xlsx", "creativecommons.org/licenses/by/2.1/jp"]
  },
  {
    "id": "hirakata-barber-file",
    "claim": "The barber register (29,419 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.hirakata.osaka.jp/cmsfiles/contents/0000025/25284/riyouall.xlsx",
    "min_bytes": 20000
  },
  {
    "id": "hirakata-beauty-file",
    "claim": "The beauty register (69,664 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.hirakata.osaka.jp/cmsfiles/contents/0000025/25284/biyouall.xlsx",
    "min_bytes": 50000
  },
  {
    "id": "hirakata-laundry-file",
    "claim": "The laundry register (26,636 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.hirakata.osaka.jp/cmsfiles/contents/0000025/25284/cleaningall.xlsx",
    "min_bytes": 20000
  },
  {
    "id": "hirakata-opendata-terms",
    "claim": "The city's open-data page states the terms linked to CC BY 2.1 JP",
    "kind": "http_contains",
    "url": "https://www.city.hirakata.osaka.jp/0000017270.html",
    "present": ["creativecommons.org/licenses/by/2.1/jp"]
  },
  {
    "id": "hirakata-mhlw-live",
    "claim": "MHLW's open-data file for Hirakata (27210) answers a plain keyless GET (383,368 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27210_food_business_all.csv",
    "min_bytes": 300000
  },
  {
    "id": "hirakata-isj-block-live",
    "claim": "MLIT's block-level address file for Hirakata (27210) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27210-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "hirakata-isj-chome-live",
    "claim": "MLIT's town-chōme file for Hirakata (27210) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/27210-19.0b.zip",
    "min_bytes": 8000
  },
  {
    "id": "hirakata-keihan-main-timetable",
    "claim": "Keihan's weekday Main Line timetable PDF (toward 出町柳), the frequency source for the six Main Line stations",
    "kind": "http_ok",
    "url": "https://www.keihan.co.jp/traffic/time-fare/pdf/time01-1.pdf",
    "min_bytes": 500000
  },
  {
    "id": "hirakata-keihan-katano-timetable",
    "claim": "Keihan's weekday Katano Line timetable PDF, the frequency source for 村野, 星ヶ丘 and 宮之阪",
    "kind": "http_ok",
    "url": "https://www.keihan.co.jp/traffic/time-fare/pdf/time02-1.pdf",
    "min_bytes": 300000
  },
  {
    "id": "hirakata-jr-tsuda-timetable",
    "claim": "JR West's station timetable for 津田 toward 京橋 (2886067001) answers, the Gakkentoshi Line's frequency source",
    "kind": "http_ok",
    "url": "https://timetable.jr-odekake.net/station-timetable/2886067001",
    "min_bytes": 20000
  },
  {
    "id": "hirakata-projected-crs",
    "claim": "Hirakata projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.682,
    "expect": "EPSG:32653"
  }
]
```
