# Toyonaka — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 89: "Toyonaka (99.8% of restaurants in force)";
`docs/decisions_drafts/staging.md`, "Wave 5: the ranked queue and the
pre-verdicts screened"). The Step 0 downloads were approved by the owner
2026-10-06 (call 106). **Step 0 measured 2026-10-06** (staging). Into
`data/toyonaka/raw/` (gitignored), each from its publisher's own host, under
each URL's own file name, project user-agent, every one HTTP 200:

- From `data.bodik.jp` (at least 21 s between calls, no
  `datastore_search_sql`): the city's `272035_food_business` CSVs, **the full
  list** `272035_food_business_all.csv` (911,608 B) and **all 34 monthly
  files**, new (`…_new_YYYYMMDD_YYYYMMDD.csv`) and closed
  (`…_closed_…`), 2025-04 to 2026-08 (460,411 B); and
  `272035_sanitation_business`'s full list `272035_sanitiation_business.csv`
  (the publisher's spelling, 240,384 B). 36 files, 1,612,403 B.
- From `i2fas.mhlw.go.jp`: `27203_food_business_all.csv` (502,614 B), the
  control.
- From `nlftp.mlit.go.jp`: `isj/27203-24.0a.zip` (126,154 B) and
  `isj/27203-19.0b.zip` (9,773 B).
- 2,250,944 B in all. **Not fetched**: the XLSX twins, and the sanitation
  list's monthly files (2026-01 to 2026-08: closed for all eight months, new
  for six), which were not named in the approval (open call 1).

**Run `python scripts/brief_check.py toyonaka` before writing any code**
(its BODIK checks were run here through a wrapper that spaces BODIK requests
21 s apart; `brief_check.py` itself does not space them). Then the
`japan-city` skill, **Maebashi's shape for the rebuild** (base + new −
closed, keyed on the permit number; `docs/build_briefs/maebashi.md`),
Higashiōsaka's and Sakai's for a full list plus months, Ichinomiya's for
MHLW's notifications beside a city list. Coordinates: the `address-join`
skill, measured with `pipeline/countries/japan_register.py` from scratch
scripts only (`scripts/screen_japan_join.py` has no Toyonaka entry; its table
is shared code and was not edited). Rail: MLIT N02-25 cut at the N03 city
line, through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

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
(2026-10-06): 法人名 is an operator column (2026-10-05) and a bare personal
name is withheld whatever it holds; (6) **no page says "currently
operating"**. Also: no frequency floor for JR or private lines in Japan
(owner, 2026-10-06, call 46), any stretch at about 11 trains a day or fewer
named and drawn (call 86; none here); fault-based cost clauses accepted for
all of Japan (2026-09-24); English station names from OSM `name:en`; every
Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).**
Toyonaka carries `label_tier: "minor"` and goes in the **Japan West** view
today; wave 4's first city to land retags Japan into the eight regions with
**Osaka Prefecture** a view of its own, and Toyonaka goes there. **Itami and
Toyonaka go into `KNOWN_STACKED`** (the `japan-city` skill, accepted). Its
label offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and
1200), never by eye; its dot sits about 9 km north of Osaka's.

**✅ `mode`: `metro`.** Kita-Osaka Kyuko is a subway-type line running through
onto the Osaka Metro Midōsuji Line, the Osaka Monorail is urban rapid
transit, and Hankyu is a conventional railway (N02 class 12). No JR runs in
the city, so the JR test (2026-10-02) does not arise; nothing reads as tram or
light rail.

---

## The one-line summary

**All three buckets from the city's own lists on BODIK (CC BY 4.0 as stated;
a licence read pending).** The food list of permits in term on 2026-03-31
(4,420 lines, **4,369 permits, 3,515 飲食店営業 = 99.8% of e-Stat's 3,523 in
force**) plus the monthly new and closed lists since, rebuilt by permit number
to **2026-08-31: 4,318 permits, 3,484 restaurants (98.9%)**. **The city files a
renewal as a closure of the old number plus a new permit under a new
number**, so the closed lists must be applied, by number. Barbers 237, beauty
salons 736, laundries 231 (99.2%, 101.2%, 95.9% of official) in a register
dated about 2025-12-31. Block join **98.1%** (food), **99.2-99.6%**
(registers), **0 unplaced**. **Rail: 12 station records in 11 `N02_005g`
groups** (Hankyu Takarazuka 6, Osaka Monorail 4, Kita-Osaka Kyuko 2; 蛍池
shared; 千里中央 two groups 257 m apart, open call 3), all read from the
operators' own timetables: 6 to 12 trains an hour.

---

## Business leg — the city's lists on BODIK

Organisation 豊中市 (272035) on `https://data.bodik.jp`; both datasets in the
デジタル庁 「自治体標準データセット」 schema (the food dataset's notes say so).
Every CSV here is UTF-8 without a BOM, header on line 1.

### Food: `272035_food_business`, 食品等営業許可一覧（豊中市）

| File (resource) | Bytes | Rows | What it is |
|---|---|---|---|
| `…/dataset/2d6870cc-3db8-4069-841e-2a6deeb173b4/resource/74c6e0d8-9fde-4503-8090-bada26639ae3/download/272035_food_business_all.csv` 全許可施設一覧（csv） | **911,608** | **4,420** (4,369 filled, 51 empty lines) | permits in term on **2026-03-31** (latest 許可年月日 2026-03-31, earliest 許可満了日 2026-04-30); uploaded 2026-05-29 |
| `…_new_20250401_20250430.csv` … `…_new_20260801_20260831.csv` 新規許可一覧, 17 months | 267,566 | 996 filled (2026-04: 89 of 849 lines; the newer files pad with empty lines) | each month's new permits |
| `…_closed_20250401_20250430.csv` … `…_closed_20260801_20260831.csv` 廃業届出一覧, 17 months | 192,845 | 735 filled | each month's closures, 廃業年月日 inside the month in every file |

- **Columns** (full list): 全国地方公共団体コード (272035 on every row),
  ID_全許可施設, 地方公共団体名, **施設名称**, **営業の種類**,
  **所在地_連結表記**, **法人名** (the operator, company or individual),
  **許可番号** (8 digits, unique), 初回許可年月日, **許可年月日**, 許可開始日,
  **許可満了日**, 廃業年月日 (empty on every row). The months carry the same
  columns with ID_新規許可 / ID_廃業届出 in place of the ID; the closed files
  fill 廃業年月日. **No 業態 column and no coordinates.**
- **Dates**: `2026/3/31` throughout, except the full list's 許可開始日, an
  Excel serial (`46112`); `wareki_date` reads both (0 unreadable).
- **Types** (full list): 飲食店営業 **3,515**, 菓子製造業 368, 食肉販売業 130,
  そうざい製造業 103, 魚介類販売業 99, 調理の機能を有する自動販売機営業 19,
  冷凍食品製造業 17, 密封包装食品製造業 15, 食肉処理業 14, 麺類製造業 13,
  水産製品製造業 13, … 喫茶店営業 9 (26 types).
- **Vehicles and stalls**: **496 rows are addressed `大阪府豊中市内一円`**
  (all 飲食店営業); `permits_from_rows` flags them mobile (485 in the rebuilt
  set). Full-list restaurants with a fixed address: 3,023.
- **Old law**: 824 permits started before 2021-06-01 (614 restaurants), all
  expiring by 2027.
- **Shared code reads every column already**: `ADDR_COLS` has
  所在地_連結表記, `NAME_COLS` 施設名称, `TYPE_COLS` 営業の種類,
  `OPERATOR_COLS` 法人名.

### The months, renewals and closures (the merge)

- **The months to 2026-03 are already in the full list**: 645 of their 657
  new permits are in it by number (of the 12 others, 10 closed in a month to
  2026-03 and 1 had expired); none of their 458 closed permits is in it.
  Leave them out.
- **Apr-Aug 2026: 339 new permits, 277 closures.** No new permit reuses a
  full-list number except 8 continuations; 251 of the 277 closures are
  full-list numbers.
- **A renewal is a closure plus a new number**: of 332 full-list permits
  expiring 2026-04 to 08-30 (260 restaurants), **198 appear in a closed list,
  189 of them closed ON their expiry date**, and 153 of those 198 have a new
  permit at the same (address, trade name, type) in the Apr-Aug files. 128 of
  the 339 new rows are at premises not in the full list (genuinely new).
- **The rebuild, by number** (base, plus Apr-Aug new, minus Apr-Aug closed,
  kept while 許可満了日 is on or after the pinned **2026-08-31**): **4,318
  permits, 3,484 restaurants**. 130 base permits (113 restaurants) expired
  2026-04 to 07 with no closure filed and no renewal by number: dropped by the
  in-term test (14 of them have a new permit at the same premises, which
  stands in for them). 76 premises keys still repeat (one pin per premises,
  trap 7, takes them).
- **The shared `rebuilt_register` is not the method here**: keyed on
  (address, trade name, type) and blind to closure files, it gives 4,274 /
  3,435; subtracting closures by premises key gives 4,066 / 3,272, wrong the
  other way (a renewal's closure removes its own new permit). A city
  `source_rows` that rebuilds by 許可番号, Maebashi's 整理番号 rebuild.

### Counts against the official stock

e-Stat 衛生行政報告例 FY2024 (`japan_official.estat()`), 大阪府豊中市, 飲食店営業
in force 2025-03-31: **3,523** (old law 1,093, revised 2,430).

| | Restaurants (飲食店営業) | Share of 3,523 |
|---|---|---|
| Full list, 2026-03-31 | **3,515** | **99.8%** |
| Rebuilt by number to 2026-08-31 | **3,484** | 98.9% |
| Rebuilt, one pin per premises key | 3,413 | 96.9% |
| MHLW's open restaurant permits (control) | 58 | 1.6% |

Through `japan_eigyo` (rebuilt, fixed premises): **Food service 3,004 rows,
Retail 692**; out 137 (119 manufacturing types by "no rule", 18 vending);
**one pin per (address, name, bucket): Food service 2,959, Retail 586.**
**No 業態, so `FORM_RULES` sees nothing**: konbini, supermarkets, canteens
and bars holding 飲食店営業 stay in Food service. By trade-name word (counts
only, of 2,952 fixed restaurant premises): konbini chains 133, supermarkets
77, canteen, hospital, school or staff words 124, snack, bar, lounge or club
156. Kobe's, Osaka's and Aomori's lists have no 業態 either; the build follows
them. **Economic Census control** (`scripts/japan_census_control.py` at
build): the 2021 census counts **1,305** 飲食店 establishments in 27203; 2,959
placed Food-service premises is **2.27 per establishment**, above the built
cities' 1.56-1.92 and beside Aomori's 2.33, for the same reason (no 業態).
Factory words (工場 / センター) in 44 bucketed names: measured and kept.

### MHLW's file (27203): a control, and notifications

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27203_food_business_all.csv`:
**502,614 B, 1,437 rows** (届出 1,363, 許可 67, 届出(廃業) 4, 許可(廃業) 3),
the national schema. **Toyonaka does not enter its permits there**: 67
permits (58 restaurants, granted 2022-02 to 2026-07, numbered `第…号`, one
number in a city file, 20 at a city (address, name)), against 3,515 in the
city's list. It is no closure control (Fukuyama's method does not apply: the
city's own closed lists do that job).

- **Notifications: 1,363 open, 875 addressed**: その他の食料・飲料販売業 697,
  cup vending 144, other vending 98, 百貨店・総合スーパー 73, 乳類販売業 65,
  行商 59, 集団給食施設 40, コンビニエンスストア 24, … (業態 blank on 804;
  無人販売用冷凍庫 81, 置き菓子 56, ドラッグストア 40). The partial Food-shops
  layer of Matsuyama and Ichinomiya (call 128), if the owner follows it (open
  call 2).
- **Its own coordinates**: MHLW's addressed fixed rows (849) join at block
  84.3%, chōme 7.8%, unplaced 7.9%; block point against MHLW's own point
  **median 36 m, 98.2% within 250 m** (716 rows, none over 1 km). Its point
  serves where the join misses.

### Personal services: `272035_sanitation_business`, 生活衛生営業施設一覧（豊中市）

| File (resource) | Bytes | Rows | Kinds |
|---|---|---|---|
| `…/dataset/7e383a56-704b-4c18-ae8c-f30e7e086a60/resource/849e744a-452b-4230-a783-07e1b8a11240/download/272035_sanitiation_business.csv` 全施設一覧（csv） | **240,384** | **1,255** | 美容所 736 · 理容所 237 · クリーニング業(取次のみ) 179 · (ドライ) 28 · 旅館業 26 · 公衆浴場 19 · (ランドリー) 16 · クリーニング業 6 · 興行場 6 · (リネンサプライ) 2 |

- **Six trades**: barber, beauty, laundry (five spellings), lodging, public
  baths, 興行場 (cinemas and theatres). **In scope: barber 237, beauty 736,
  laundry 229** (the two linen-supply rows out, Osaka's 2026-09-27
  precedent). **Out**: 旅館業 26 (lodging, `docs/category_rules.md`), 興行場 6
  (recreation, the same file), 公衆浴場 19 (no row in `category_rules.md`; no
  built Japanese city carries baths and `japan_eigyo`'s personal sources never
  include them, so out on that precedent: open call 4).
- **Columns**: **業種**, 許可（登録）番号 (unique), 許可（登録）日 (ISO),
  **施設名称**, **施設住所**, **施設ＴＥＬ** (filled 775), **申請者氏名** (the
  applicant), **法人代表者氏名** (filled 374), **法人所在地** (the company's own
  address, filled 385).
- **Dated about 2025-12-31**: uploaded 2026-01-08, latest 許可（登録）日
  2025-12-04, no 2025-12 monthly file. The dataset states no date. A standing
  register: 許可日 from 1955 (1950s 3 … 2010s 377, 2020s 283). The months
  2026-01 to 08 exist and were not fetched (open call 1).
- **Official** (e-Stat FY2024 第10表 / 第11表,
  `data/hakodate/raw/estat_eisei_r6_*_by_city.csv`): barbers **239**, beauty
  salons **727**, laundries **241** (取次所 187, 指定洗濯物 7; 無店舗取次店
  operators 13, not premises). **Shares 99.2%, 101.2%, 95.9%** (95.0% after
  linen supply out). No 無店舗, 一円 or 移動 row.
- 3 repeats of (address, name, kind); 6 premises listed as both 理容所 and
  美容所 (one pin per premises and bucket keeps one).
- **Shared code** reads it: `ADDR_COLS` 施設住所, `NAME_COLS` 施設名称,
  `TYPE_COLS` 業種, `OPERATOR_COLS` 申請者氏名 and 法人代表者氏名. One file
  holds every trade, so a `source_rows` sends 理容所 to barber, 美容所 to
  beauty and クリーニング業* to laundry, and passes the parenthesised kind
  (取次のみ, リネンサプライ) as the value: `japan_eigyo`'s linen rule tests
  `startswith("リネン")`, which `クリーニング業(リネンサプライ)` does not.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27203-24.0a.zip` (126,154 B,
**5,110 block keys**), town-chōme `.../19.0b/27203-19.0b.zip` (9,773 B,
**337**). `japan.CITIES` entry at build: `"toyonaka": {"name": "豊中市",
"pref": "27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["27203"]}`.

| Tier (rebuilt by number, fixed premises in a bucket) | All (3,696) | Food service (3,004) | Retail (692) |
|---|---|---|---|
| Block | **98.1%** | 98.0% | 98.3% |
| Town-chōme centroid | 1.9% | 2.0% | 1.7% |
| Unplaced | **0.0%** | 0.0% | 0.0% |

| Registers | Barbers (237) | Beauty (736) | Laundry (231) |
|---|---|---|---|
| Block / chōme / unplaced | 99.2 / 0.8 / 0 | 99.6 / 0.4 / 0 | 99.6 / 0.4 / 0 |

**The misses, read** (towns only): 螢池西町3丁目 **54** of the 70 food
chōme-tier rows, the address of Osaka International Airport's terminal
(a 地番 the block file does not list; read at build), 東寺内町 6,
新千里東町1丁目 4, single rows elsewhere. Nothing unplaced, so MHLW's point
is not needed for the city's rows.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_27_GML.zip`, N03 code 27203
(**36.2 km²**, extent W 135.441, S 34.731, E 135.508, N 34.825). Read with
`stub_test()` and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 records | Stations inside |
|---|---|---|---|
| 宝塚線 (阪急電鉄, 12) | Hankyu Takarazuka Line | **6 / 19** | 庄内, 服部天神, 曽根, 岡町, 豊中, 蛍池 |
| 大阪モノレール線 (大阪モノレール, 23) | Osaka Monorail Main Line | **4 / 14** | 蛍池, 柴原阪大前, 少路, 千里中央 |
| 南北線 (北大阪急行電鉄, 12) | Kita-Osaka Kyuko Namboku Line | **2 / 6** | 緑地公園, 千里中央 |

- **12 station records, 11 `N02_005g` groups.** **蛍池** is one group
  (006656: Hankyu + Monorail, 71 m). **千里中央 is two groups** (Kita-Osaka
  Kyuko 006587, Monorail 006598), **257 m apart**: one interchange station by
  name, as Kawasaki's 武蔵小杉 (377 m) and Tokyo's 池袋 (356 m) were before
  `GROUP_JOIN` joined them (open call 3). Median nearest-group gap **1,085
  m** with the two apart (closest 257 m, the 千里中央 pair; widest 2,264 m):
  ring size by the spacing rule at build.
- **Shinkansen**: none in the city.
- **Cut at the line** (named by N03 municipality at build): Hankyu 13 beyond
  (Osaka City 4, Hyōgo 7, Ikeda 2), the Monorail 10 (Suita 2, Ibaraki 3,
  Settsu 2, Moriguchi 1, Kadoma 1, Hyōgo 1: 大阪空港 in Itami), Kita-Osaka
  Kyuko 4 (Suita 2: 江坂, 桃山台; Minoh 2: the 2024 extension).
- **The stub test passes.** Kita-Osaka Kyuko keeps 2 stations and the
  Monorail 4: neither is a one-station stub, so both are drawn cut under the
  standing call and no owner question arises. Hankyu's Senri Line runs in
  Suita, not here. The Monorail's Saito branch is outside the city.
- **The light-rail / rail test**: Hankyu and Kita-Osaka Kyuko are railways
  (N02 class 12), the Monorail a straddle monorail (class 23); no tram or
  light rail.
- **Frequency, READ 2026-10-06 from the operators' own timetables** by the
  wave-5 probe (plain GET, project agent), re-counted here from its cached
  pages, weekday departures 10:00-15:59:

  | Line, stations | Direction | Per hour |
  |---|---|---|
  | Hankyu Takarazuka: 庄内, 服部天神, 曽根, 岡町 (`hankyu.co.jp/station/html/HK-4x_ta_1_w.html`) | to 大阪梅田 | **6** (locals only) |
  | Hankyu Takarazuka: 豊中, 蛍池 | to 大阪梅田 | **12** (6 express + 6 local) |
  | Osaka Monorail: 蛍池, 柴原阪大前, 少路, 千里中央 (the operator's `/timetable/12`-`15` JSON) | both ways | **5.8-6** |
  | Kita-Osaka Kyuko: 緑地公園 (`kita-kyu.co.jp/train/traffic/ryokuchikoen/`) | to 箕面萱野 / to なかもず | **7.5 / 7.7** |
  | Kita-Osaka Kyuko: 千里中央 | both ways | **7.5** |

  No stretch near 11 trains a day; no floor applies (call 46).
- **OSM `name:en`**: Osaka's cache (`data/osaka/raw/osm_station_names.json`,
  read only) names 7 of the 10 stations (曽根 "Sone", 庄内 "Shōnai", 豊中
  "Toyonaka", 服部天神 "Hattori-tenjin", 岡町 "Okamachi", 蛍池 "Hotarugaike",
  緑地公園 "Ryokuchi-kōen"); 少路, 柴原阪大前 and 千里中央 lie outside its box.
  The build fetches its own (one Overpass query, the CLAUDE.md rule).
- ⚠️ **Gate 3** at build: Hankyu's, the Monorail's and Kita-Osaka Kyuko's
  per-line station counts; line colors on both basemaps.

## Scope

**Toyonaka City.** Hankyu runs on to Osaka City (south) and Ikeda and Hyōgo
(north), the Monorail to Itami's airport and east through Suita, Kita-Osaka
Kyuko to Suita and Minoh; cut at the line.

## Licences — as read on the dataset pages; the full read is pending

- **`272035_food_business` and `272035_sanitation_business`**: BODIK's
  package metadata states **`license_id` `cc-by-40-intl`, "Creative Commons
  Attribution 4.0 International"** on both (read from `package_show` by the
  wave-5 probe); the food dataset page's licence box reads
  「クリエイティブ・コモンズ 表示 4.0 国際」, linked to the CC BY 4.0 deed
  (read here 2026-10-06). **A `licence-read` agent reads the terms separately**
  (BODIK's own terms and anything the city incorporates); staging records the
  verdict and the prescribed credit. No verdict here.
- **MHLW open data** (if used, open call 2): PDL 1.0 as recorded in
  `docs/data_sources/japan.md`:
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; no completeness claim.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **Food: 法人名 is the operator column**, a company on 2,052 of 4,369 rows
  and **no company marker on 2,317** (where an individual's own name can
  sit). Read IN MEMORY for the name rule only (`OPERATOR_COLS` has it); never
  selected for output. **Name rule v2** (answers only, never a value): **1**
  full-list row (a restaurant) whose trade name equals an individual
  operator's name, **0 bare personal names**; the rebuilt set the same (1 / 0).
- **Sanitation: 申請者氏名 is the applicant-name field** (no company marker
  on **877** of 1,255 rows), beside 法人代表者氏名, **法人所在地** and
  **施設ＴＥＬ**. Select 業種, 施設名称, 施設住所 only. **Name rule v2: 2 barber
  rows, both bare personal names under the sign rule** (withheld, shown by
  type); beauty and laundry 0.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; on its
  notifications the name rule flags 2 (0 bare).
- Run `check_personal_exposure.py toyonaka` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Osaka Prefecture after the retag),
`label_tier: "minor"`, `"country": "Japan"`. Project to **UTM 53N
(EPSG:32653)**: the N03 centroid lies at longitude 135.473, the extent
135.441-135.508, inside the 132-138 band (computed here, never copied). OSM
box from the N03 extent, rounded out: (34.72, 135.43, 34.83, 135.52).

**Scaffold**: `scaffold_city.py --slug toyonaka --name Toyonaka --system-name
"Hankyu, Osaka Monorail and Kita-Osaka Kyuko" --taxonomy japan_eigyo --lat
34.782 --lon 135.473 --region "Japan West" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), the number claimed in
`docs/session_roles.md` at build (Toyonaka is not in
`docs/staged_cities.json`).

## Owner calls

**Made (do not re-ask):** Band A (owner, 2026-10-06, call 89); the Step 0
downloads (call 106); the standing Japanese calls above; `mode: metro`; the
minor tier, Japan West now and Osaka Prefecture after the retag,
`KNOWN_STACKED` with Itami; Kita-Osaka Kyuko (2) and the Monorail (4) drawn
cut (not one-station stubs); no frequency floor (call 46); lodging and
興行場 out (`docs/category_rules.md`); linen supply out (Osaka, 2026-09-27);
no 業態, Food service taken whole (Kobe's, Osaka's and Aomori's lists).

**Open, each with a recommendation:**

1. **The sanitation months, 2026-01 to 2026-08** (14 CSVs: closed for all
   eight months, new for 2026-02 and 04 to 08; not in the approval). *Recommend
   approving them*, so the registers rebuild to 2026-08-31 like the food list
   (their numbers are unique, Maebashi's rebuild). Tradeoff: 14 more BODIK
   calls; without them the page states two dates (food 2026-08-31, registers
   about 2025-12-31), Fukuoka's several-dates precedent.
2. **MHLW beside the city's list.** (a) **Its 1,363 open notifications (875
   addressed) as a partial Food-shops layer**, MHLW's own point where the
   join misses. *Recommend yes, on Matsuyama's and Ichinomiya's precedent*
   (call 128); the tradeoff is a bucket the page must call partial. (b)
   **Its 67 permits: out** (Ichinomiya's call 126): the city's list holds
   3,515 restaurants to MHLW's 58, numbered differently. Either adds MHLW's
   PDL credit.
3. **千里中央 as one station** (`GROUP_JOIN` on the Monorail's or Kita-Osaka
   Kyuko's platform, 257 m). *Recommend joining*, on Kawasaki's (377 m) and
   Tokyo's (424 m, 356 m) precedent: one interchange, one ring, one English
   name. Tradeoff: N02 keeps them apart; left apart, two rings 257 m apart and
   names with operator suffixes (Kobe's Mikage).
4. **公衆浴場 (19) out.** `docs/category_rules.md` has no row for public
   baths; no built Japanese city carries them (Maebashi's base list has 42,
   unbuilt). *Recommend out, on that precedent*, listed in What Is Excluded
   with lodging and 興行場. Tradeoff: a first written rule for baths.

## What the build must still measure

- ⚠️ **`config.source_rows`** for food: the full list plus the 2026-04 to 08
  new files, minus the 2026-04 to 08 closed files, **by 許可番号**, kept in
  term on **2026-08-31** (never today); the 2025-04 to 2026-03 months left
  out. Expect 4,318 / 3,484.
- ⚠️ **`config.source_rows`** for the sanitation file: kind by 業種, the
  parenthesised laundry kind as the value (リネンサプライ out), the three
  out-of-scope trades dropped and counted.
- The 螢池西町3丁目 rows (the airport) at the chōme tier: their pins sit at
  the chōme centroid unless a better point is found; read them.
- Gate 3, `GROUP_JOIN` if call 3 is yes, OSM `name:en`, line colors on both
  basemaps, the opening view (`map-view`), the factory share, the Economic
  Census control (estimated 2.27), `check_provenance.py`,
  `check_scope_disclosure.py`, `check_macro_labels.py` with Itami.

```brief-checks
[
  {
    "id": "toyonaka-food-full-list-rows",
    "claim": "The city's full food list (permits in term on 2026-03-31) has 4,420 rows in the BODIK datastore (4,369 permits and 51 empty lines in the CSV)",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "74c6e0d8-9fde-4503-8090-bada26639ae3",
    "expect": 4420
  },
  {
    "id": "toyonaka-food-full-list-fields",
    "claim": "The full list's premises columns and the operator column 法人名, and no 業態 column",
    "kind": "ckan_fields",
    "domain": "data.bodik.jp",
    "resource_id": "74c6e0d8-9fde-4503-8090-bada26639ae3",
    "present": ["施設名称", "営業の種類", "所在地_連結表記", "法人名", "許可番号", "許可年月日", "許可満了日", "廃業年月日"],
    "absent": ["業態"]
  },
  {
    "id": "toyonaka-food-aug-new-rows",
    "claim": "The August 2026 new-permit file holds 46 permits",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "a11ef3d9-9cd0-407e-a24b-c43c2c31d2b4",
    "expect": 46
  },
  {
    "id": "toyonaka-food-aug-closed-rows",
    "claim": "The August 2026 closures file holds 36 closures",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "c822c52e-f618-4555-8073-1c3d6e51978e",
    "expect": 36
  },
  {
    "id": "toyonaka-sanitation-rows",
    "claim": "The sanitation register (six trades, uploaded 2026-01-08) has 1,255 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "849e744a-452b-4230-a783-07e1b8a11240",
    "expect": 1255
  },
  {
    "id": "toyonaka-sanitation-fields",
    "claim": "The register's columns, including the applicant name, the representative, the company address and the phone, never selected",
    "kind": "ckan_fields",
    "domain": "data.bodik.jp",
    "resource_id": "849e744a-452b-4230-a783-07e1b8a11240",
    "present": ["業種", "施設名称", "施設住所", "申請者氏名", "法人代表者氏名", "法人所在地", "施設ＴＥＬ"]
  },
  {
    "id": "toyonaka-food-dataset-page",
    "claim": "The food dataset page states CC BY 4.0 (クリエイティブ・コモンズ 表示 4.0 国際), the 自治体標準データセット schema, and offers the full list and the August 2026 new and closed lists",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/dataset/272035_food_business",
    "present": ["食品等営業許可一覧（豊中市）", "creativecommons.org/licenses/by/4.0", "クリエイティブ・コモンズ 表示 4.0 国際", "自治体標準データセット", "全許可施設一覧", "新規許可一覧（令和8年8月）", "廃業届出一覧（令和8年8月）"]
  },
  {
    "id": "toyonaka-mhlw-live",
    "claim": "MHLW's open-data file for Toyonaka (27203) answers a plain keyless GET (502,614 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27203_food_business_all.csv",
    "min_bytes": 400000
  },
  {
    "id": "toyonaka-isj-block-live",
    "claim": "MLIT's block-level address file for Toyonaka (27203) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27203-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "toyonaka-isj-chome-live",
    "claim": "MLIT's town-chōme file for Toyonaka (27203) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/27203-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "toyonaka-hankyu-timetable",
    "claim": "Hankyu's weekday timetable for 豊中 toward 大阪梅田 lists express and local trains - the frequency source",
    "kind": "http_contains",
    "url": "https://www.hankyu.co.jp/station/html/HK-46_ta_1_w.html?no_redirect",
    "present": ["豊中駅", "大阪梅田方面", "急行"]
  },
  {
    "id": "toyonaka-kitakyu-timetable",
    "claim": "Kita-Osaka Kyuko's station page for 千里中央 carries its weekday timetable tables and the up-direction PDF (ASCII markers: the page sends no charset, so the check's decoding cannot match Japanese text)",
    "kind": "http_contains",
    "url": "https://www.kita-kyu.co.jp/train/traffic/senrichuo/",
    "present": ["table_weekdays", "tt_senrichuo_up.pdf", "minohkayano"]
  },
  {
    "id": "toyonaka-monorail-timetable",
    "claim": "The Osaka Monorail's timetable data for 千里中央 (station 15) answers - the frequency source",
    "kind": "http_ok",
    "url": "https://www.osaka-monorail.co.jp/timetable/15",
    "min_bytes": 2000
  },
  {
    "id": "toyonaka-projected-crs",
    "claim": "Toyonaka projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.473,
    "expect": "EPSG:32653"
  }
]
```
