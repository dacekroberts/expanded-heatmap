# Suita — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, call 118: "Amagasaki,
Suita, Itami, Kakogawa (call 118: 101-106% with old-law permits)";
`docs/decisions_drafts/staging.md`, "Wave 5, second half"). Banded C first
with its files approved to measure (call 90; the same file's "Wave 5"
entry), the block join approved with call 106. **Step 0 measured
2026-10-06** (staging). In `data/suita/raw/` (gitignored), each from its
publisher's own host with the project user-agent, each HTTP 200, under each
URL's own file name:

- From `www.city.suita.osaka.jp` (staging's call-90 measurement, 2026-10-06):
  the food lists `20260331new.xlsx` (295,586 B, permits under the revised
  law) and `20260331old.xlsx` (73,931 B, permits under the old law), both as
  of 2026-03-31; the barber, beauty and laundry registers `2026090301.xlsx`
  (26,907 B), `2026090302.xlsx` (81,870 B) and `2026090303.xlsx` (25,354 B),
  as of 2026-08-31.
- From `nlftp.mlit.go.jp` (call 106): `isj/27205-24.0a.zip` (107,157 B) and
  `isj/27205-19.0b.zip` (7,661 B).
- From `i2fas.mhlw.go.jp` (this brief, the control approved for round 3):
  `27205_food_business_all.csv` (460,403 B).

**1,078,869 B in all.** Nothing else was downloaded (the same page's
興行場, 旅館業, 公衆浴場 and 住宅宿泊 lists are out of scope and were not
fetched).

**Run `python scripts/brief_check.py suita` before writing any code.** Then
the `japan-city` skill, **Akita's shape** for a city list of every permit in
term on its date (`docs/build_briefs/akita.md`), here in **two files, one
per law, read together**; Hamamatsu's for one register file per kind;
**Toyonaka's** for its neighbour's rail and MHLW's notifications beside a
city list (`docs/build_briefs/toyonaka.md`). Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` has no Suita
entry; its table is shared code and was not edited). Rail: MLIT N02-25 cut
at the N03 city line, through `pipeline/countries/japan.py` with a scratch
`CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none in N02 inside the city); (2) **lines served only by
limited expresses DO count** (2026-09-28); (3) **the city line only**: only
stations inside the city get rings, JR and the private lines are cut at the
line, **a one-station stub stays as cut** (2026-09-27); an URBAN line cut to
ONE station is left out, its station kept through the other lines, and drawn
cut only where no other line serves that station (owner, 2026-10-06, calls
54 and 92); (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**,
version 2 (2026-10-06): 法人名 is an operator column (2026-10-05) and a bare
personal name is withheld whatever it holds; (6) **no page says "currently
operating"**. Also: no frequency floor for JR or private lines in Japan
(owner, 2026-10-06, call 46), any stretch at about 11 trains a day or fewer
named and drawn (call 86; none here); fault-based cost clauses accepted for
all of Japan (2026-09-24); English station names from OSM `name:en`; every
Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Applied from today's precedents (2026-10-06; do not re-ask):**
**Esaka (江坂), the Midōsuji Line's one station in the city, is drawn cut**
(call 92; but see open call 1); **MHLW's notifications as a partial
Food-shops layer** (call 127b: 679 addressed rows) with **MHLW's own point
where the block join misses** (127c); **MHLW's permits out** (call 126);
**the food snapshot disclosed as an upper bound** (half its old-law permits
expire during 2026; Kyoto's disclosure); the one-station rules (54, 92).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02, 2026-10-04).**
Suita carries `label_tier: "minor"` and goes in the **Japan West** view
today; wave 4's first city to land retags Japan into the eight regions, and
Suita goes into **Osaka Prefecture**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye; its
dot sits about 4 km east of Toyonaka's (the two N03 centroids).

**✅ `mode`: `metro`.** Kita-Osaka Kyuko and the Midōsuji are subway lines,
the Osaka Monorail urban rapid transit, Hankyu and JR West railways (N02
classes 11, 12, 21, 23); nothing reads as tram or light rail. Toyonaka's
precedent.

---

## The one-line summary

**All three buckets from the city's own XLSX files (CC BY 4.0 as stated; the
licence read is pending, staging records it), plus MHLW's notifications as
partial Food shops.** The two food lists of permits in term on
**2026-03-31** hold **4,076 rows, 3,330 restaurants (飲食店営業) = 101.1% of
e-Stat's 3,294 in force** (revised law 2,771, old law 559), an **upper bound**
for any later date: 241 of those restaurant permits (204 old-law) reached
their end by 2026-08-31, and 307 of the 559 old-law ones (55%) end between
April and December 2026. Barbers 155, beauty salons 558, laundries 137 as of
2026-08-31: **93.9%, 102.2%, 91.9% of official**. Through `japan_eigyo`:
**Food service 2,430 rows (2,301 pins), Retail 630 (488)**, plus **444 Retail
rows (428 pins) from MHLW's notifications**. Block join **98.5%** (food
98.3%, registers 98.5-99.6%), **0 unplaced**. **Rail: 15 `N02_005g`
groups** on eight N02 lines (Hankyu 8, the Monorail 3, JR West 3,
Kita-Osaka Kyuko 2 with the Midōsuji's 江坂 shared), read from the
operators' own timetables: **4.0 to 8.0 trains an hour midday, the thinnest
67 a day one way**.

---

## Business leg — the city's 衛生管理課 open data

Page `https://www.city.suita.osaka.jp/shisei/1018811/1017120/1017164/1017170.html`
(衛生管理課 オープンデータ, 更新日 2026-09-07); every file a plain GET under
`/_res/projects/default_project/_page_/001/017/170/`. All five XLSX read
with `japan_register.city_rows` as they stand.

### Food: 食品営業許可施設一覧 (令和8年3月31日時点), two files

| File | Bytes | Rows | What it is |
|---|---|---|---|
| `20260331new.xlsx` …（改正後の食品衛生法の許可（令和3年6月1日以降の許可）） | **295,586** | **3,353** | revised-law permits in term on 2026-03-31 (許可年月日 2021-06-02 to 2026-03-31; 許可満了日 2026-06-30 to 2032-03-31) |
| `20260331old.xlsx` …（改正前の食品衛生法の許可（令和3年5月31日までの許可）） | **73,931** | **723** | old-law permits in term on 2026-03-31 (許可年月日 2020-02-28 to 2021-05-31; 許可満了日 2026-03-31 to 2027-05-31) |

- **Columns, both files**: No., **申請者氏名** (the operator), **屋号** (the
  trade name), an unnamed column (66 and 9 rows, no building words), **施設住所**,
  **業種**, **種目** (露店, 自動車, 自動販売機), 許可年月日, **許可満了日**,
  当初許可年月日. No phone, no operator address, no permit number (No. is a
  row number).
- **Against the shared tuples**: 施設住所 is in `ADDR_COLS`, 屋号 in
  `NAME_COLS`, 業種 in `TYPE_COLS`, 種目 in `FORM_COLS` (read under
  `WAVE2_RULES`' `form_cols`), 申請者氏名 in `OPERATOR_COLS`. **No shared-code
  change.**
- **The food lists are not monthly**: still 2026-03-31 on a page updated
  2026-09-07 whose registers are 2026-08-31. The page states two dates
  (Fukuoka's several-dates precedent). File names carry the date
  (`YYYYMMDDnew/old.xlsx`): a `SOURCE_LINKS` regex for each, `as_of` from the
  link title, never today.
- **Types**: revised law 飲食店営業 **2,771** (種目 blank 1,927, 露店 539,
  自動車 305), 菓子製造業 298, 食肉販売業 87, そうざい製造業 66, 魚介類販売業 53,
  調理機能付き自動販売機 27, … (22 types); old law 飲食店営業 **559** (blank 503,
  自動車 30, 露店 26), 菓子 69, 食肉販売 32, 魚介類 17, そうざい 14, 喫茶店営業 11,
  … (14 types; 種目 自動販売機 4).

### Old-law coverage (Kurashiki's trap) and the upper bound

- **Both laws are published, in two files**; the build reads both (Kurashiki's
  trap would be reading `new` alone: 2,771 restaurants, 84%).
- **e-Stat 衛生行政報告例 FY2024** (`japan_official.estat()`), 大阪府吹田市,
  飲食店営業 in force 2025-03-31: **3,294** (old law 995, revised 2,299). The
  lists' **3,330 restaurants are 101.1%**, vehicles and stalls on both sides,
  the lists a year later (old law 559 against 995: a year of expiries; e-Stat's
  old-law count fell from 2,001 in FY2022 to 1,465 and 995).
- **The upper bound, measured.** Old-law restaurants by end: 77 on
  2026-03-31 (the list's own date), **204 from April to August 2026**, 103
  from September to December, 175 in 2027. With 37 revised-law restaurants
  ending by 2026-08-31, **241 of the 3,330 permits had reached their end by
  the registers' date**; a renewed one carries a new permit only a later
  edition shows, a lapsed one is gone, and openings since April are missing.
  The page discloses the food list as of 2026-03-31, an upper bound (Kyoto's
  disclosure; Fukushima's and Ichihara's briefs word it).

### Duplicates and closed premises

- **61 (address, trade name, type) appear in both files** (a premises holding
  an old and a new permit); over both, 227 rows repeat in 167 groups. One pin
  per premises and bucket (trap 7): **2,301 Food-service and 488 Retail pins**
  from 2,430 and 630 rows.
- **Closures are not marked**; the lists hold permits in term on their date.
  The page keeps "may include closed premises".

### Counts through `japan_eigyo` (fixed premises)

Stalls and vehicles: 796 rows are addressed 大阪府吹田市内一円, which
`permits_from_rows` marks not a premises; 110 more carry a street address and
種目 露店 or 自動車, which `FORM_RULES` take out as temporary or mobile. **No
city rule is needed.** **Food service 2,430, Retail 630** (菓子 359, butcher
119, deli 82, fishmonger 70). Left out: not a premises 801, temporary by 種目
114, no rule 70 (manufacturing types), vending 31.

**No 業態**, so canteens, konbini, supermarkets and snack bars holding
飲食店営業 stay in Food service (Toyonaka's, Kobe's and Osaka's lists the
same). **Economic Census control** (`scripts/japan_census_control.py` at
build): the 2021 census counts **1,018** 飲食店 establishments in 27205;
**2,301** placed Food-service premises is **2.26 per establishment**, above
the built cities' 1.56-1.92 and beside Toyonaka's 2.27, for the same reason.
Factory words (工場 / センター) in 51 bucketed names: measured and kept.

### MHLW's file (27205): notifications in, permits out

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27205_food_business_all.csv`:
**460,403 B, 1,391 rows** (届出 1,299, 許可 88, 許可(廃業) 3, 届出(廃業) 1),
the national schema.

- **Permits out (call 126)**: 88 open (71 restaurants), against the city's
  3,330; 62 carry a trade name in the city's lists, 43 at the same (address,
  trade name). 12 were granted after 2026-03-31, the new permits the city's
  snapshot lacks; out with the rest on the precedent (the upper bound
  disclosure covers openings).
- **Notifications in, as a partial Food-shops layer (call 127b)**: **1,299
  open, 679 addressed**. Through `japan_eigyo`: **Retail 444 rows, 428 pins**
  (その他の食料・飲料販売業 340, 百貨店・総合スーパー 64, コンビニエンスストア
  13, 乳類 9, 野菜果物 7, butcher 3, bento 3, rice 2). Out: not a premises 677
  (no address, or 一円), vending 84, 集団給食施設 35, no rule 30, temporary 26,
  mail order 3. Disclosed as partial: MHLW publishes an address only where
  the filer agreed (Matsuyama's `ADDRESS_BY_CONSENT`).
- **Its points (call 127c)**: the 444 join at block 422, chōme 16, unplaced 6,
  which take MHLW's own point (`OWN_POINT_FALLBACK`). Block point against
  MHLW's own point over its open fixed rows: median **40 m**, 94.2% within
  250 m (638 rows), 13 over 1 km.
- A premises in both (a konbini with a city restaurant permit and an MHLW
  notification): `SUPERSEDES` on Matsuyama's pattern, measured at build.

### Personal services: 確認施設一覧 (令和8年8月31日時点)

| File | Bytes | Rows with an address | Official (e-Stat FY2024 第10表 / 第11表) | Share |
|---|---|---|---|---|
| `2026090301.xlsx` 理容所確認施設一覧 | **26,907** | **155** | barbers 165 | **93.9%** |
| `2026090302.xlsx` 美容所確認施設一覧 | **81,870** | **558** | beauty salons 546 | **102.2%** |
| `2026090303.xlsx` クリーニング所確認施設一覧 | **25,354** | **137** (136 after linen) | laundries 149 (取次所 125; 無店舗 92 not premises) | **91.9%** (91.3%) |

(Official from `data/hakodate/raw/estat_eisei_r6_*_by_city.csv`, 大阪府吹田市.)

- **Columns**: No., 確認年月日 (older dates in Shōwa with spaces, 21 to 43 rows
  per file that `wareki_date` does not read; not needed), 確認番号, laundries'
  **種別** (取次のみ 115, ドライ、ランドリー 12, ランドリー 4, ドライ、ランドリー、仕上げ
  4, 仕上げ 1, **リネンサプライ 1**, blank 1), **施設_名称**, **施設所在地**,
  施設_TEL, **申請者_氏名**, **代表者名**, 申請者住所. Each file ends in one row
  with no address (dropped).
- **Shared code reads them**: 施設所在地 in `ADDR_COLS`, 施設_名称 in
  `NAME_COLS`, 種別 in `TYPE_COLS`, 申請者_氏名 and 代表者名 in `OPERATOR_COLS`.
  `japan_eigyo`'s linen rule takes リネンサプライ out (Osaka's 2026-09-27
  precedent). No type column for barbers and beauty: the config names the
  kind per file.
- Repeats of (address, name): barber 0, beauty 1, laundry 0; **17 addresses
  in both the barber and the beauty register** (one pin per premises and
  bucket). Standing registers, no closure marker.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27205-24.0a.zip` (107,157 B,
**4,679 block keys**), town-chōme `.../19.0b/27205-19.0b.zip` (7,661 B,
**191**). `japan.CITIES` entry at build: `"suita": {"name": "吹田市", "pref":
"27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
"wards": ["27205"]}`.

| Tier, today's shared code (`WAVE2_RULES`) | Block | Town-chōme | Unplaced |
|---|---|---|---|
| City lists, bucketed (3,909) | **98.5%** | 1.5% | **0** |
| … Food service (2,430) / Retail (630) | 98.4% / 97.9% | 1.6 / 2.1 | 0 / 0 |
| Barbers (155) / beauty (558) / laundry (136) | 98.7 / 99.6 / 98.5% | 1.3 / 0.4 / 1.5 | 0 |
| MHLW notifications, Retail (444) | 95.0% | 3.6% | 6 (MHLW's own point) |

**The misses, read** (towns only, scratch `measure.py` and the
`isj_measure` scratch): **岸部新町 23 rows** at the chōme tier, a number not
among the town's blocks in 24.0a (the redeveloped district around the city
hospital, likely numbered after MLIT's edition: read at build; the chōme
centroid stands, or MHLW's point for a premises in both); 原町2丁目 5, 津雲台7丁目 2; 千里万博公園 and
山田丘 with no number after the town. Nothing unplaced.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_27_GML.zip`, N03 code 27205
(**36.1 km²**, extent W 135.487, S 34.745, E 135.555, N 34.831). Read with
`stub_test()` and an in-memory `CITIES` entry (scratch `rail_suita.py`).
English names on Osaka's built config (`pipeline/osaka/config.py`: 東海道線
here is the JR Kyoto Line) and Toyonaka's brief.

| N02 line (operator, class) | Public name | Inside / N02 records | Stations inside |
|---|---|---|---|
| 千里線 (阪急電鉄, 12) | Hankyu Senri Line | **7 / 11** | 吹田, 豊津, 関大前, 千里山, 南千里, 山田, 北千里 |
| 京都線 (阪急電鉄, 12) | Hankyu Kyoto Line | **1 / 27** | 正雀 |
| 東海道線 (西日本旅客鉄道, 11) | JR Kyoto Line | **2 / 59** | 吹田, 岸辺 |
| おおさか東線 (西日本旅客鉄道, 11) | Osaka Higashi Line | **1 / 14** | 南吹田 |
| 大阪モノレール線 (大阪モノレール, 23) | Osaka Monorail Main Line | **2 / 14** | 山田, 万博記念公園 |
| 国際文化公園都市モノレール線(彩都線) (大阪モノレール, 23) | Osaka Monorail Saito Line | **2 / 5** | 万博記念公園, 公園東口 |
| 南北線 (北大阪急行電鉄, 12) | Kita-Osaka Kyuko Namboku Line | **2 / 6** | 江坂, 桃山台 |
| 1号線(御堂筋線) (大阪市高速電気軌道, 21) | Midōsuji Line | **1 / 20** | 江坂 |

- **18 station records, 15 `N02_005g` groups.** Interchanges: 山田 (006604:
  Hankyu and the Monorail, 197 m), 万博記念公園 (006601: the Monorail's two
  lines), **江坂 (006800: the Midōsuji and Kita-Osaka Kyuko, 0 m)**. **吹田 is
  two groups** (JR 006779, Hankyu 006798), separate stations at least 600 m
  apart: they stay apart, named with the operator where OSM's `name:en`
  does not tell them apart (Kobe's 御影 precedent, trap 1). The closest pair,
  **岸辺 (JR) and 正雀 (Hankyu), 427 m**, are two stations with two rings.
  Median nearest-group gap **961 m** (427 to 1,731): rings by the spacing
  rule at build.
- **Shinkansen**: no Shinkansen station inside the city.
- **Cut at the line** (named by N03 municipality at build): Hankyu Senri 4
  beyond (Osaka 4), Hankyu Kyoto 26 (Osaka 6, Ibaraki 3, Takatsuki 3, Settsu
  1, Shimamoto 1, Kyoto Prefecture 12), JR Kyoto 57 (Osaka 10, Takatsuki 2,
  Ibaraki 2, Settsu 1, Shimamoto 1, beyond Osaka Prefecture 41), Osaka
  Higashi 13 (Osaka 7, Higashiōsaka 5, Yao 1), the Monorail Main Line 12
  (Toyonaka 4, Ibaraki 3, Settsu 2, Moriguchi 1, Kadoma 1, Hyōgo 1), Saito 3
  (Ibaraki 3), Kita-Osaka Kyuko 4 (Toyonaka 2, Minoh 2), the Midōsuji 19
  (Osaka 16, Sakai 3).
- **The stub test.** **The Hankyu Kyoto Line keeps one station of 27, 正雀**,
  whose N02 point lies **14 m inside the city line** (the station sits on the
  Suita-Settsu boundary; N03 decides, and it is inside), and **the Osaka
  Higashi Line one of 14, 南吹田** (217 m from the line). Both are JR or
  private lines: drawn as cut under the standing call, **no owner question**
  (Kobe's JR Takarazuka Line). The Monorail's two lines and Kita-Osaka Kyuko
  keep 2 each: drawn cut. **The Midōsuji keeps one, 江坂**: drawn cut by call
  92 (open call 1 below).
- **The light-rail / rail test**: Hankyu, JR and Kita-Osaka Kyuko are
  railways (N02 classes 11 and 12), the Midōsuji a subway (21), the Monorail a
  straddle monorail (23); no tram or light rail.
- **Frequency, READ 2026-10-06 from the operators' own timetables** by the
  wave-5 probe (plain GET), re-counted here from its cached pages
  (`wave5/japan_j5/pages`, scratch `tt_read.py`, `kitakyu.py`), weekday,
  every departure a page lists:

  | Line, station (page) | Direction | All day | Per hour 10-16 |
  |---|---|---|---|
  | Hankyu Senri: all 7 (`hankyu.co.jp/station/html/HK-89`…`HK-95_se_1_w.html`) | to 天下茶屋・大阪梅田 | 138 | **6.2** (locals) |
  | Hankyu Kyoto: 正雀 (`HK-66_ky_1_w.html`) | to 大阪梅田 | 135 | **6.0** (locals) |
  | JR Kyoto Line: 吹田, 岸辺 (`timetable.jr-odekake.net/station-timetable/2794011002`, `2793011002`) | to 大阪・神戸 | 151 / 150 | **8.0** |
  | **Osaka Higashi Line: 南吹田** (`11142073001`) | to 放出・久宝寺 | **67** | **4.0** |
  | Osaka Monorail: 山田, 万博記念公園 (the operator's `/timetable/16`, `/17` JSON) | each way | 116-167 | **6** |
  | Osaka Monorail Saito: 公園東口 (`/timetable/51`) | each way | 109 / 112 | **6** |
  | Kita-Osaka Kyuko: 桃山台 (`kita-kyu.co.jp/train/traffic/momoyamadai/`) | each way | 165 / 165 | **7.7** |

  **No stretch near 11 trains a day** (call 86). **The Midōsuji at 江坂**:
  Osaka Metro's own page was not read; the 165 Kita-Osaka Kyuko trains a
  weekday toward なかもず all run through 江坂 onto it (7.7 an hour), a floor
  (READ through its neighbour). Only counts are recorded, never a timetable
  on the page.
- **OSM `name:en`**: one Overpass query at build (the CLAUDE.md rule); not
  queried here. ⚠️ **Gate 3** at build: Hankyu's, JR West's, the Monorail's,
  Kita-Osaka Kyuko's and Osaka Metro's per-line counts; line colours from
  Osaka's config and Toyonaka's build on both basemaps.

## Scope

**Suita City.** Hankyu runs on to Osaka (south) and Ibaraki, Takatsuki and
Kyoto (the Kyoto Line), JR to Osaka and Takatsuki, the Osaka Higashi Line to
Osaka and Higashiōsaka, the Monorail west to Toyonaka and the airport and
east to Ibaraki and Kadoma, the Saito Line to Ibaraki, Kita-Osaka Kyuko to
Toyonaka and Minoh, the Midōsuji into Osaka; cut at the line.

## Licences — as stated; the read is pending

**As stated on the page**: each group of files (生活衛生 registers, food lists)
carries 「クリエイティブ・コモンズ 表示 4.0 国際 ライセンス」, linked to
`https://creativecommons.org/licenses/by/4.0/`, and the section ends
「本セクションで公開しているデータは、クリエイティブ・コモンズ・ライセンスのもとで提供しております。…各ライセンスの利用許諾条項に則ってご利用ください。」
**No read of Suita's terms is recorded in `docs/decisions_drafts/staging.md`:
a licence-read agent reads them separately; staging records its verdict and
the credit wording.** No verdict is written in this brief.

- **MHLW open data** (the notifications, call 127b): PDL 1.0 as recorded in
  `docs/data_sources/japan.md`:
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; no completeness claim.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **Operators' timetables**: read for counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **Food: 申請者氏名 is the operator column** on every row, with **no company
  marker on 1,844 of 4,076** (where a sole trader's own name sits). Read IN
  MEMORY for the name rule only (`OPERATOR_COLS` has it); never selected. The
  food lists carry no phone and no operator address.
- **The name rule, v2, measured in memory** (answers only, never a value):
  food **1 row withheld, 0 bare personal names, none bucketed**; barbers,
  beauty and laundries **0**; MHLW's notifications 0.
- **Registers**: 申請者_氏名 (no company marker on 131, 370 and 37 rows) and
  代表者名 read for the rule in memory; **施設_TEL and 申請者住所 (the
  operator's own address) never selected**. Select 施設_名称, 施設所在地 and
  種別 only.
- MHLW's 法人名 joins the rule (2026-10-05); 法人番号, 法人住所 and phones are
  never selected.
- Run `check_personal_exposure.py suita` (`japan=True`) after step 2: it must
  print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Osaka Prefecture after the retag),
`label_tier: "minor"`, `"country": "Japan"`. Project to **UTM 53N
(EPSG:32653)**: the N03 centroid lies at longitude 135.519, the extent
135.487-135.555, inside the 132-138 band (computed here, never copied). OSM
box from the N03 extent, rounded out: (34.74, 135.48, 34.84, 135.56).

**Scaffold**: `scaffold_city.py --slug suita --name Suita --system-name
"Hankyu, JR West, Osaka Monorail, Kita-Osaka Kyuko and Osaka Metro"
--taxonomy japan_eigyo --lat 34.786 --lon 135.519 --region "Japan West"
--country Japan --mode metro --page-number <N>` (`--dry-run` first), the
number claimed in `docs/session_roles.md` at build (Suita is not in
`docs/staged_cities.json`).

## Owner calls

**Made (do not re-ask):** Band A (call 118); the downloads (calls 90, 106,
and MHLW's control for round 3); the standing Japanese calls above; the food
lists' upper bound disclosed (Kyoto's); MHLW's notifications as partial Food
shops with its own points (127b, 127c), its permits out (126); `mode: metro`;
the minor tier, Japan West now and Osaka Prefecture after the retag; the
Hankyu Kyoto and Osaka Higashi one-station stubs drawn as cut (standing call);
the Monorail's two lines and Kita-Osaka Kyuko drawn cut (two stations each);
linen supply out (Osaka, 2026-09-27); no 業態, Food service taken whole
(Toyonaka's, Kobe's and Osaka's lists); the two 吹田 kept apart (trap 1).

**Open, with a recommendation:**

1. **Call 92's premise, measured.** The owner drew the Midōsuji cut at 江坂
   "because no other line keeps the station's ring". **In N02 the 江坂 group
   (006800) holds Kita-Osaka Kyuko's record as well as the Midōsuji's**, 0 m
   apart: Kita-Osaka Kyuko ends there and its trains run through onto the
   Midōsuji. Under the rule's letter the Midōsuji would be left out, 江坂 kept
   through Kita-Osaka Kyuko (Toei Shinjuku at 本八幡). *Recommend keeping the
   call (drawn cut; 江坂 lies 826 m from the city line)*, now resting on the
   through service: the station is known by the Midōsuji, and the cut line
   shows where the trains go. Tradeoff: a second exception to the one-station
   rule within a day of it, on different grounds from Urayasu's Tōzai.
   Staging decides whether to raise it with the owner.
2. **`KNOWN_STACKED`.** Suita's dot sits 4 km from Toyonaka's; if
   `check_macro_labels.py` cannot place both, *recommend adding Suita on the
   Itami and Toyonaka precedent* (the `japan-city` skill, accepted
   2026-10-04). Tradeoff: one more label the overview stacks rather than
   places.

## What the build must still measure

- ⚠️ **Both food files** as one food source (or two keys under
  `SOURCE_KIND`, Matsuyama's `food_old` / `food_new`), pinned at
  **2026-03-31** (`SOURCE_AS_OF`), never today; the registers at 2026-08-31.
  Expect 3,330 restaurants, Food service 2,430 and Retail 630 rows.
- MHLW's notifications as `mhlw` (`source_rows` yielding 届出 only,
  `ADDRESS_BY_CONSENT`, `OWN_POINT_FALLBACK`, `SUPERSEDES` over the food
  lists, Matsuyama's config); expect Retail 444.
- A newer food edition before building (the file names carry the date); if
  one appears, re-measure the old-law count and the upper bound.
- The 岸部新町 rows at the chōme tier; gate 3; OSM `name:en` and the 吹田
  operator suffixes; line colours on both basemaps; the opening view
  (`map-view`); the factory share; the Economic Census control (expected
  2.26); `check_provenance.py`; `check_scope_disclosure.py`;
  `check_macro_labels.py` with Toyonaka and Osaka.

```brief-checks
[
  {
    "id": "suita-open-data-page",
    "claim": "The 衛生管理課 open-data page offers both food lists (2026-03-31), the three registers (2026-08-31) and CC BY 4.0. ASCII anchors only: the host sends no charset, so the Japanese text does not decode here; a failure on a file name means a new edition: re-measure",
    "kind": "http_contains",
    "url": "https://www.city.suita.osaka.jp/shisei/1018811/1017120/1017164/1017170.html",
    "present": ["20260331new.xlsx", "20260331old.xlsx", "2026090301.xlsx", "2026090302.xlsx", "2026090303.xlsx", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "suita-food-new-file",
    "claim": "The revised-law food list (295,586 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.suita.osaka.jp/_res/projects/default_project/_page_/001/017/170/20260331new.xlsx",
    "min_bytes": 250000
  },
  {
    "id": "suita-food-old-file",
    "claim": "The old-law food list (73,931 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.suita.osaka.jp/_res/projects/default_project/_page_/001/017/170/20260331old.xlsx",
    "min_bytes": 60000
  },
  {
    "id": "suita-barber-file",
    "claim": "The barber register (26,907 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.suita.osaka.jp/_res/projects/default_project/_page_/001/017/170/2026090301.xlsx",
    "min_bytes": 20000
  },
  {
    "id": "suita-beauty-file",
    "claim": "The beauty register (81,870 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.suita.osaka.jp/_res/projects/default_project/_page_/001/017/170/2026090302.xlsx",
    "min_bytes": 65000
  },
  {
    "id": "suita-laundry-file",
    "claim": "The laundry register (25,354 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.suita.osaka.jp/_res/projects/default_project/_page_/001/017/170/2026090303.xlsx",
    "min_bytes": 20000
  },
  {
    "id": "suita-mhlw-live",
    "claim": "MHLW's open-data file for Suita (27205) answers a plain keyless GET (460,403 B on 2026-10-06; its notifications are the partial Food-shops layer)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27205_food_business_all.csv",
    "min_bytes": 400000
  },
  {
    "id": "suita-isj-block-live",
    "claim": "MLIT's block-level address file for Suita (27205) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27205-24.0a.zip",
    "min_bytes": 90000
  },
  {
    "id": "suita-isj-chome-live",
    "claim": "MLIT's town-chōme file for Suita (27205) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/27205-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "suita-hankyu-kitasenri-timetable",
    "claim": "Hankyu's weekday timetable for 北千里 on the Senri Line toward 大阪梅田 - the frequency source",
    "kind": "http_contains",
    "url": "https://www.hankyu.co.jp/station/html/HK-95_se_1_w.html?no_redirect",
    "present": ["北千里駅", "大阪梅田方面"]
  },
  {
    "id": "suita-jr-minamisuita-timetable",
    "claim": "JR West's station timetable for 南吹田 (Osaka Higashi Line), the thinnest station (4.0 an hour), lists its departures",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/station-timetable/11142073001",
    "present": ["minute-item", "南吹田駅"]
  },
  {
    "id": "suita-monorail-koenhigashiguchi-timetable",
    "claim": "The Osaka Monorail's timetable data for 公園東口 (station 51, the Saito Line) answers",
    "kind": "http_ok",
    "url": "https://www.osaka-monorail.co.jp/timetable/51",
    "min_bytes": 2000
  },
  {
    "id": "suita-kitakyu-momoyamadai-timetable",
    "claim": "Kita-Osaka Kyuko's station page for 桃山台 carries its weekday timetable tables (ASCII markers: the page sends no charset)",
    "kind": "http_contains",
    "url": "https://www.kita-kyu.co.jp/train/traffic/momoyamadai/",
    "present": ["table_weekdays", "tt_momoyamadai_up.pdf", "minohkayano"]
  },
  {
    "id": "suita-projected-crs",
    "claim": "Suita projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.519,
    "expect": "EPSG:32653"
  }
]
```
