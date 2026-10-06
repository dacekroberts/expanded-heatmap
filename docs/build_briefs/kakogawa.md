# Kakogawa — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 118: `docs/decisions_drafts/staging.md`, "Wave 5, second half": "Amagasaki,
Suita, Itami, Kakogawa (call 118: 101-106% with old-law permits)"). Hyōgo
Prefecture's files were approved and fetched for the measurement (call 90) and
MLIT's address blocks for the block join (call 106). **The block join's low
share is built with the tiers disclosed** (owner, call 145; the master list's
row). **Step 0 measured 2026-10-06** (staging). Into `data/kakogawa/raw/`
(gitignored), each from its publisher's own host with the project user-agent,
each HTTP 200:

- From `web.pref.hyogo.lg.jp` (保健医療部 生活衛生課), fetched 2026-10-06 into
  `data/hyogo_pref/raw/` and **copied unchanged** into `data/kakogawa/raw/`
  (and `data/itami/raw/`), because a Japanese build reads `data/<slug>/raw/`
  (`config.source_csv`): `000028_food_business_lisence_all.xlsx`
  (**4,519,769 B**, the publisher's spelling), `000028_food_business_notification_all.xlsx`
  (**1,861,708 B**), `000028_barbershop_all.xlsx` (**195,680 B**),
  `000028_beauty_salon_all.xlsx` (**496,756 B**),
  `000028_cleaningbusiness_all.xlsx` (**113,185 B**).
- From `i2fas.mhlw.go.jp`: `28000_food_business_all.csv`, **Hyōgo
  Prefecture's file** (**1,579,737 B**, 2026-10-06; downloaded once into
  `data/itami/raw/` and copied), the control.
- From `nlftp.mlit.go.jp` (already cached): `isj/28210-24.0a.zip`
  (246,924 B) and `isj/28210-19.0b.zip` (7,649 B).

**9,021,408 B in all; the only new download for these two briefs was MHLW's
file.** Nothing else was downloaded.

**Run `python scripts/brief_check.py kakogawa` before writing any code.** Then
the `japan-city` skill, **Tsu's shape** (`docs/build_briefs/tsu.md`: the
prefecture's standing lists, every row assigned to the city by its address),
built on the same files and the same shared-code changes as Itami
(`docs/build_briefs/itami.md`, whose sections on the lists apply here word for
word; this brief repeats what a Kakogawa build needs and gives Kakogawa's own
numbers). Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py`'s own functions from scratch scripts
(`scripts/screen_japan_join.py` has no Kakogawa entry; its table is shared code
and was not edited). Rail: MLIT N02-25 cut at the N03 city line, through
`pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; no Shinkansen station inside); (2)
**lines served only by limited expresses DO count** (2026-09-28); (3) **the
city line only**: only stations inside the city get rings, JR and the private
lines are cut at the line, **a one-station stub stays as cut** (2026-09-27); an
URBAN line cut to ONE station is left out, its station kept through the other
lines, and drawn cut only where no other line serves that station (owner,
2026-10-06, calls 54 and 92); (4) **菓子製造業 and そうざい製造業 count, in
Retail**, the factory share measured and kept (2026-09-24, 2026-09-27); (5)
**the name rule**, version 2 (2026-10-06): a bare personal name is withheld
whatever the operator column holds; (6) **no page says "currently
operating"**. Also: no frequency floor for JR or private lines in Japan
(owner, 2026-10-06, call 46), any stretch at about 11 trains a day or fewer
**named and drawn** (call 86); fault-based cost clauses accepted for all of
Japan (2026-09-24); English station names from OSM `name:en`; every Japanese
city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The tiers disclosed (owner, call 145).** 86.5% of Kakogawa's premises
reach a block and 13.3% the town-chōme centroid (below). The page says so in
its coordinates bullet, Tsu's and Ichihara's way; nothing is dropped for it.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Kakogawa
carries `label_tier: "minor"` and `"region": "Japan West"`, as Himeji and
Nishinomiya do (`app/cities.py`); wave 4's first city to land retags Japan
into the eight regions, Kakogawa into **Kansai**. Its dot (JR 加古川) sits about
15 km east-southeast of Himeji's and 33 km west of Kobe's centre: its label offset from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 ("unless there is
substantial JR, JR reads as metro"): JR West has 5 of the 8 station groups
(the JR Kobe and Kakogawa lines) against Sanyō's 3; no subway, tram or light
rail. Okayama's, Kitakyushu's and Akita's precedent.

---

## The one-line summary

**All three buckets from Hyōgo Prefecture's monthly lists (CC BY 4.0 by the
catalogue's terms as stated; the read is pending), cut to Kakogawa by address:
2,653 food permits (2,061 restaurants, 267 of them old-law) through
2026-08-31, and 170 barbers, 532 beauty salons and 85 laundries as of
2026-08-31.** Prefecture-wide the lists are complete (restaurants **101.4%**
of e-Stat's FY2024 count in the prefecture's jurisdiction, barbers 97.3%,
beauty 100.7%, laundries 94.7%). No per-city count exists; **Kakogawa's
restaurant share is estimated at about 87%** (the list's own density across
the jurisdiction, the 5,176 prefecture-wide 県下一円 stall and vehicle permits
removed). Through `japan_eigyo`: **Food service 1,970 rows (1,949 pins),
Retail 444 (393)**; Personal services 787 rows. Block join **86.5%**, 13.3%
town-chōme centroid, 0.2% unplaced (**tiers disclosed, call 145**). **Rail:
8 N02 station groups** (JR West 5: the JR Kobe Line's 東加古川 and 加古川, the
Kakogawa Line's 日岡, 神野 and 厄神; Sanyō 3), read from the operators' own
timetables, nothing at or under 11 trains a day. ⚠️ **The probe's "7 groups"
is corrected to 8**: it counted 宝殿 (in Takasago by N03 and by JR West's own
station page) and the Kakogawa Line as one station.

---

## Business leg — Hyōgo Prefecture's lists (保健医療部 生活衛生課)

Host `https://web.pref.hyogo.lg.jp`. The pages, files, columns, cadence and
traps are Itami's (`docs/build_briefs/itami.md`, "Business leg"); in short:

| Page | Edition | Files (under `/kf14/documents/`) |
|---|---|---|
| 食品関係営業施設リストの閲覧, `https://web.pref.hyogo.lg.jp/kf14/shokuhineigyoushisetsu_list.html` (更新日 2026-09-24) | 「令和8年8月までのリスト（令和8年9月15日更新）」, updated about the 20th monthly | `000028_food_business_lisence_all.xlsx`, `000028_food_business_notification_all.xlsx` |
| 生活衛生関係営業施設リストの閲覧, `https://web.pref.hyogo.lg.jp/kf14/kankyoueigyoushisetsu_list.html` (更新日 2026-09-10) | 「令和8年8月末時点のリスト（令和8年9月10日更新）」, updated early each month | `000028_barbershop_all.xlsx`, `000028_beauty_salon_all.xlsx`, `000028_cleaningbusiness_all.xlsx` |

- **The jurisdiction is the prefecture less Kobe, Himeji, Amagasaki, Akashi and
  Nishinomiya**, so Kakogawa is in it. ⚠️ **The host sends no charset**:
  brief checks on these pages use ASCII anchors only.
- **The file names never change**: `SOURCE_AS_OF` 2026-08-31 for all five
  from the pages' edition lines, never the fetch date; the edition checks
  below fail when a new edition lands (re-measure then).
- **Food list columns**: 都道府県コード, No, **営業所名称**, 営業所郵便番号,
  **営業所所在地**, 営業所電話番号 (never), **業種**, **形態**, operator
  **営業者法人名称**, 営業者役職, **営業者氏名**, operator address and phone
  (never), **許可番号**, **許可日**, **有効期限**, 初許可日. One sheet, header on
  row 1, 32,433 rows; `city_rows` reads it as it stands. Every row is a permit
  in term (有効期限 2026-11-30 to 2033-05-31).
- ⚠️ **Two shared-code changes, Itami's too**: `FORM_COLS` + **形態** (without
  it Kakogawa's **15 street-stall rows** read as restaurants), and the
  registers' **circled-numeral header** (`①営業所名称`, `②営業所所在地`,
  `③営業の種類` …: `city_rows` reads 0 rows until one leading circled numeral is
  stripped, in `_head` or a config `file_rows`). Each followed by the Minato
  control.
- **Gaiji**: 「Excelファイルでは外字は表示されません」; measured **1 Kakogawa
  address and 1 trade name** with a placeholder.

### Cutting Kakogawa out of the prefecture's lists

- **The rule: an address that begins `加古川市`** (NFKC, spaces removed,
  `兵庫県` stripped first). **0 rows in any file contain 加古川市 anywhere
  else.** The neighbouring towns 稲美町 and 播磨町 are written `加古郡…` and never
  match. `config.source_rows` cuts by the prefix and **raises** on a row
  containing 加古川市 elsewhere (Tsu's rule).
- **The 5,176 prefecture-wide 県下一円 permits** belong to no town (not a
  premises by `一円`) and are not in Kakogawa's count.

### Food by type, through `japan_eigyo` (measured, 形態 read as the form)

| | Rows | Kept | Out (rule) |
|---|---|---|---|
| 飲食店営業 (1) 一般食堂・レストラン等 1,114 · (4) その他 860 · (2) 仕出し屋・弁当屋 71 · (3) 旅館 11 · (5) 簡易な営業 5 | 2,061 | **1,964 Food service** (+ 6 old-type 喫茶店営業: **1,970**) | 71 仕出し (catering) · 15 stalls by 形態 · 11 旅館 |
| Food retail permits (菓子 240, 食肉販売 111, そうざい 50, 魚介類販売 43) | 444 | **444 Retail** | |
| Vending (調理の機能を有する自動販売機 34) | 34 | 0 | vending |
| Manufacturing and other types (食肉処理 20, 食肉製品 12, 密封包装 12, 漬物 12 …) | 108 | 0 | "no rule", as in every built city |

- **形態**: 一般 2,604, 自動販売機 34, 露店200L/直結 7, 露店40L 7, 露店80L 1.
- **(4) その他 is the catch-all, 42% of restaurants** (860 of 2,061). It stays
  in Food service: **no hostess-venue marker exists** (R3 applies "wherever
  the register names them"; here it names none).
- **Key**: (許可番号, 許可日) unique (2,653 of 2,653); the number alone repeats
  (1,148 distinct): `東播(加健)第N-N`, the 加古川健康福祉事務所's series.
  17 (address, trade name, type) groups repeat (40 rows); 2,321 distinct
  (address, trade name). **One pin per (address, trade name, bucket): Food
  service 1,949, Retail 393.**
- **Factory share**: 14 of 290 菓子 / そうざい rows (4.8%) are named 工場 or
  センター, kept (the 2026-09-27 call).

### Old-law coverage (Kurashiki's trap) — not this list's problem

**353 rows granted before 2021-06-01** (restaurants 267: (4) その他 192, (1) 61,
(2) 11; 菓子 35, 食肉 18, 魚介類 8 …), ending 2026 (112), 2027 (228) and 2028
(13). New-law restaurants by grant year: 2021 191 · 2022 356 · 2023 334 · 2024
347 · 2025 313 · 2026 253. The list holds every permit in term under either law.

### Completeness — the prefecture measured, Kakogawa estimated

**No official per-city count** (`docs/coverage_sweep/japan_universe_mhlw.csv`
has none for 28210). The jurisdiction, e-Stat FY2024 against the lists: the
table in Itami's brief (restaurants 23,875 of 23,537, **101.4%**; barbers
97.3%; beauty 100.7%; laundries 94.7%).

**Kakogawa's share, estimated** against the 2021 Economic Census (飲食店 900,
理容業 138, 美容業 332, 洗濯業 73 establishments in 28210):

- **Restaurants about 87%**: 2,061 against 900 × 2.62 (the list's restaurant
  permits per census 飲食店 across the jurisdiction, the 5,176 県下一円 permits
  removed) is **87.5%** (fixed premises only, 2,046: 86.8%). With e-Stat's count
  in place of the list's, 89.1%; with the median ratio of ten Kansai core
  cities (2.85), 80% (range 71-85%). **The page states about 87% as an
  estimate** (call 125's stated share).
- **Barbers 103.0%** (170 against 165 estimated), **beauty 102.9%** (532
  against 517), **laundries 96.6%** (85 against 88).
- **The Economic Census control** (at build): 1,949 Food-service pins against
  900 is **2.17 per establishment**, ⚠️ **above the built cities' 1.56-1.92**
  (as Itami's; the list runs 2.56 jurisdiction-wide, Kakogawa 2.27). Read why
  on the built pins and record the reading.

### Closed premises

No status column. MHLW's one closed permit in the jurisdiction (closed
2026-08-05) is still in the 2026-08 list: the page keeps "may include closed
premises".

### The notification list (`000028_food_business_notification_all.xlsx`)

**Kakogawa: 1,410 rows** (その他の食料・飲料販売業 430, cup vending 214, 乳類販売業
146, 集団給食 106, コンビニエンスストア 94, vending 94, 百貨店、総合スーパー 49 …;
形態 一般 835, 自動販売機 413, 集団給食 108, 露店 30, 自動車 23, 行商 1),
届出番号 and 施行日 from 2021-06-01 (the system's start) to 2026-08-31. Through
`japan_eigyo`: **649 Retail rows, 642 pins** (その他の食料・飲料販売業 381, konbini
94, 乳類 50, supermarkets 49, 野菜果物 28, 食肉 27, 米穀 10, 弁当 6, 魚介類 4); out
414 vending, 166 manufacturing ("no rule"), 123 institutional, 54 not a
premises, 3 temporary, 1 other. The prefecture's own complete list: open call 1.

### Personal services: the three registers (as of 2026-08-31)

| File | **Kakogawa** | Kinds (営業の種類 / 営業の種類２) |
|---|---|---|
| `000028_barbershop_all.xlsx` | **170** | 理容所 / 固定 |
| `000028_beauty_salon_all.xlsx` | **532** | 美容所 / 固定 |
| `000028_cleaningbusiness_all.xlsx` | **85** | 一般 23, 一般(指定洗濯物取扱) 8, **取次 54** |

No repeats by (address, trade name); **13 addresses** hold both a barber and a
beauty salon (one pin per premises and bucket). Standing registers; "may
include closed premises".

### MHLW's file (28000), the control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=28000_food_business_all.csv`:
**1,579,737 B, 5,362 rows**. ⚠️ **Trap: 市区町村名 is `神戸市中央区` on every
row**; assign by address only, never by that column.

- **189 rows addressed to Kakogawa** (届出 154, 許可 35), every one with MHLW's
  own point. Of the **35 open permits (32 restaurants), 29 are in Hyōgo's
  list** by (number digits, grant date); the other 6 to read at build
  (renumbered, or closed). MHLW adds nothing the map needs.
- **Its own point against the block point**: median **53 m**, 93.0% within
  250 m, **2 over 1 km** (142 block-tier rows); its 41 other rows fall to the
  chōme tier, as Kakogawa's own do. An own-point fallback (call 127c) would
  move only MHLW's few rows and is not proposed: Hyōgo's lists carry no point.

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 28210)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28210-24.0a.zip` (246,924 B) and
`…/19.0b/28210-19.0b.zip` (7,649 B): **28,567 block keys** (with the 大字 + 字
keys), **176 town-chōme keys**. Ward-less. Measured with `permits_from_rows`,
`load_city_isj` and `join_city` under `WAVE2_RULES`, unchanged (staging's
`isj_measure`; food rows filtered to 形態 一般, in force).

| Tier (rows in a bucket) | Food (2,414) | Barbers (170) | Beauty (532) | Laundries (85) | **All (3,201)** |
|---|---|---|---|---|---|
| Block | 85.8% | 94.1% | 87.2% | 87.1% | **86.5%** (2,769) |
| Town-chōme / 大字 centroid | 14.0% | 5.9% | 12.8% | 12.9% | **13.3%** (427) |
| Unplaced | 0.2% | 0.0% | 0.0% | 0.0% | **0.2%** (5) |

**The misses, read** (towns only):
- **Chōme tier, 354 in towns MLIT carries whose number it lacks**: 平岡町新在家
  9, 加古川町寺家町 8, 加古川町溝之口 8, 野口町水足 7, 志方町志方町 7, 平岡町つつじ野 7 …,
  across the city. Kakogawa's addresses are mostly 地番 (lot numbers), and
  MLIT's block file keys only some of each town's numbers; the town centroid
  is the honest point. This is what call 145 discloses.
- **Chōme tier, 72 字 addresses** whose 字 MLIT keys without blocks (神野町石守字整理
  5, 加古川町友沢字野田 4, 志方町志方町字馬場田 4, 尾上町今福字中村 2, 東神吉町砂部字出口 2,
  米田町平津字高川原 2 …): the 大字 centroid by design. 1 row has no number.
- **Unplaced (5)**: `東神吉町天ケ原` 2, where MLIT writes 東神吉町天下原 (the
  list spells the reading); `志方町大沢` 1, where MLIT writes 志方町大澤 (a 沢 /
  澤 variant); `志方町上富木` 2, a town MLIT's files do not carry. Five rows: a
  variant-kanji rule is shared code, not worth it for one row; read at build.
- Rules used: 58 shifted, 27 affixes (26 prefix), 72 大字. **No publisher
  coordinates** in Hyōgo's lists.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (28210)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_28_GML.zip`, N03 code 28210
(**138.4 km²**, extent W 134.7636, S 34.6982, E 134.9362, N 34.8672;
centroid 34.792, 134.851). No Shinkansen station inside.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 山陽線 (西日本旅客鉄道, 11) | JR Kobe Line (JR神戸線, the Sanyō Main Line) | **2 / 131** | 東加古川, 加古川 |
| 加古川線 (西日本旅客鉄道, 11) | JR Kakogawa Line | **4 / 21** | 加古川, 日岡, 神野, 厄神 |
| 本線 (山陽電気鉄道, 12) | Sanyo Electric Railway Main Line | **3 / 43** | 別府, 浜の宮, 尾上の松 |

- **9 station records, 8 `N02_005g` groups**: 加古川 (006754) holds the Kobe
  and Kakogawa lines, 36 m apart. No name in two groups; no pair closer than
  600 m. **Median nearest-group gap 2,019 m** (1,472 to 2,564): rings by the
  spacing rule.
- ⚠️ **宝殿 is outside**: its N02 point lies **38 m beyond the N03 line**, and
  JR West's own station page gives its address as 「兵庫県高砂市神爪」 (checked
  below). The wave-5 probe counted it as Kakogawa's (and read its timetable,
  2.2 an hour); the city-line rule and the station's address agree that it is
  Takasago's. **土山** (182 m beyond, 播磨町) is outside too.
- **Cut at the line**: the JR Kobe Line on to 宝殿 (Takasago) and 土山 (Harima)
  and beyond; the Kakogawa Line on to 市場 (Ono, 882 m beyond) and 西脇市; Sanyō
  on to 高砂 (Takasago, 630 m beyond) and 播磨町 (Harima). All three are drawn
  as cut; none is a stub (the Kobe Line's 2 of 131 is a main line cut at the
  line, as Akita's Ōu Line).
- **The light-rail / rail test**: all three are heavy rail (N02 classes 11 and
  12). No tram or light rail.
- **Frequency, READ** (the wave-5 probe's cached operator pages, plain GET,
  counted whole here: every departure listed, marked ones included):

  | Station (line, direction) | Weekday departures | Per hour, 07-18 | Midday (10-16) |
  |---|---|---|---|
  | 加古川 (JR Kobe, to 三ノ宮・大阪) | 151 | 8 to 15 | 8 an hour (新快速 included) |
  | 東加古川 (JR Kobe, to 三ノ宮・大阪) | 77 | 4 to 8 | 4 an hour (新快速 pass) |
  | 加古川 (Kakogawa Line, to 粟生・西脇市) | **37** | 1 to 4 | 1.3 an hour |
  | 別府 (Sanyō, to 神戸・大阪) | 163 | 7 to 14 | 8 an hour |
  | 浜の宮, 尾上の松 (Sanyō, to 神戸・大阪) | 87 each | 4 to 10 | 4 an hour |

  JR West's station timetables (`timetable.jr-odekake.net/station-timetable/<id>?date=20261007`,
  a Wednesday; ids 2859012001, 2858012002, 2859036001), Sanyō's per-station
  weekday PDFs (`www.sanyo-railway.co.jp/tt/index.php?code_station_from=334-26`,
  -27, -28, the timetable of 2025-02-22). **No stretch at or under about 11
  trains a day** (call 86): the thinnest is the Kakogawa Line, 37 a day
  northbound from 加古川, hourly at midday. 日岡, 神野 and 厄神 take the trains that
  leave 加古川 (the line runs local trains only, ASSERTED from the page's single
  train type; read their own pages at build). Only counts are recorded, never
  a timetable on the page.
- ⚠️ **Gate 3** at build: JR West's and Sanyō's station lists (Kobe Line 2,
  Kakogawa Line 4, Sanyō 3 inside). **OSM `name:en`** for 8 groups (one
  Overpass query at build; none queried here).

## Scope

**Kakogawa City (28210), one municipality, no wards.** The JR Kobe Line runs on
to Himeji and Kobe, the Kakogawa Line to Ono and Nishiwaki, Sanyō to Takasago
and Akashi; cut at the line.

## Licences — as stated; the read is pending

As Itami's (`docs/build_briefs/itami.md`, "Licences"): the prefecture's
catalogue lists the five XLSX with the **CC BY** icon, and its terms
(`https://web.pref.hyogo.lg.jp/kk26/johoseisaku/documents/kiyaku_opendata.pdf`)
license the catalogue's works 「CCライセンス表示4.0国際」 unless noted, with a
prescribed credit (`出典：[タイトル]、［兵庫県]`, or for modified data 「この[作品]は、
以下の著作物を改変して利用しています。」 and the titles) and a bar on presenting
edited data as the prefecture's. **A licence-read agent reads the source
separately; staging records it. No verdict here**; take the credit from
staging's record. MHLW (28000) is a control only (PDL 1.0 if ever used); MLIT
位置参照情報 and N02 PDL 1.0 (shared credits); N03 CC BY 4.0, ⛔ never drawn;
e-Stat and the census measurement sources; JR West's and Sanyō's timetables
read for counts only. The notice number is claimed at build.

## Privacy

Select 営業所名称, 営業所所在地, 業種, 形態, 許可番号, 許可日, 有効期限 (food;
届出番号 and 施行日 for notifications) and 営業所名称, 営業所所在地, 営業の種類,
営業の種類２ (registers). **Never select 営業所電話番号, 営業者住所 or
営業者電話番号.** The operator columns are read in memory by the name rule and
never kept:

| | Operator columns | Rows | Company (法人名称 filled) | Sole traders | Flagged (v2) |
|---|---|---|---|---|---|
| Food permits | 営業者法人名称, 営業者氏名, 営業者役職 | 2,653 | 1,177 (1,157 with a company marker) | **1,476** | **10** (trade name equals the operator's name), **1 among kept rows**; 0 bare personal names |
| Notifications (open call 1) | as food | 1,410 | 1,115 | **295** | **18** (trade name = operator) and **3 bare personal names** |
| Barbers / beauty / laundries | 営業者氏名, 代表者氏名 | 170 / 532 / 85 | no company marker on 160 / 423 / 14 | | **0** |

No value was printed or stored. Run `check_personal_exposure.py kakogawa` with
`japan=True` after step 2 (it must print 0) and record the verdict in the
drafts file and `docs/privacy_verdicts.md`.

## Region and CRS

`"region": "Japan West"` (Kansai after the retag), `"country": "Japan"`,
`label_tier: "minor"`. Project to **UTM 53N (EPSG:32653)**: the extent
134.7636 to 134.9362 lies inside the 132-138 band, computed here, never copied.

**Scaffold**: `scaffold_city.py --slug kakogawa --name Kakogawa --system-name
"JR West and Sanyo Electric Railway" --taxonomy japan_eigyo --lat 34.7676 --lon
134.8399 --region "Japan West" --country Japan --mode metro --page-number <N>`
(`--dry-run` first; JR 加古川's N02 point, not N03's centroid in the north),
the page number claimed in `docs/session_roles.md` at build, not here. A
`japan.CITIES` entry: `"kakogawa": {"name": "加古川市", "pref": "28", "epsg":
32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True, "wards":
["28210"]}`. `SOURCE_FILES` under the file names above; `SOURCE_AS_OF`
2026-08-31 for each, never today.

## Owner calls

**Made (do not re-ask):** Band A (call 118); the files (call 90) and MLIT's
blocks (call 106); **the tiers disclosed** (call 145); the standing Japanese
calls; `mode: metro`; the minor tier and Japan West (Kansai after the retag);
the three lines drawn as cut (standing call 3); no frequency floor; a stated
share where a list cannot be measured per city (call 125, as about 87%).

**Open, with a recommendation:**

1. **Hyōgo's own notification list as a Food-shops layer** (642 Retail pins:
   konbini 94, supermarkets 49, other food and drink sales 381, milk, produce,
   butchers …). *Recommend yes*, Yokkaichi's precedent, decided once for both
   cities (Itami's open call 1): the publisher's complete list, already
   approved, cached and under the same terms. Tradeoff: the template's
   notification bullet needs a replacement sentence (a proposal in the drafts
   file at build), 3 bare personal names and 18 operator-name rows are
   withheld; without it Retail is the permit-holding shops only (393 pins).

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control,
  `screen_japan_join.py minato` 98.0 / 0.2 / 1.8, and every city screen): the
  same two changes as Itami's (`FORM_COLS` + 形態; the circled-numeral header),
  landed once for both; Kakogawa's `japan.CITIES` entry.
- ⚠️ **`config.source_rows`**: the `加古川市` prefix cut (strip `兵庫県` first),
  raising on a row that contains 加古川市 elsewhere. Never MHLW's 市区町村名.
- ⚠️ The tier shares as built (the page's coordinates bullet, call 145); the
  Economic Census control (2.17) and its reading; the stated food share (about
  87%) drafted as a review-time proposal.
- The Kakogawa Line's three stations' own timetables; the 6 MHLW permits not
  in Hyōgo's list; gate 3 (JR West, Sanyō); OSM `name:en`; line colours on
  both basemaps; the macro label against Himeji's; the opening view
  (`map-view`); the factory share printed by step 2; `check_provenance.py`;
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "kakogawa-hyogo-food-page",
    "claim": "Hyogo's food list page links both XLSX (permits, notifications) at the sizes of the 2026-08 edition (4,414KB, 1,819KB). ASCII anchors only: the host sends no charset. A failure on the sizes means a new edition: re-measure",
    "kind": "http_contains",
    "url": "https://web.pref.hyogo.lg.jp/kf14/shokuhineigyoushisetsu_list.html",
    "present": ["/kf14/documents/000028_food_business_lisence_all.xlsx", "/kf14/documents/000028_food_business_notification_all.xlsx", "4,414KB", "1,819KB"]
  },
  {
    "id": "kakogawa-hyogo-registers-page",
    "claim": "Hyogo's registers page links the barber, beauty and laundry XLSX at the sizes of the 2026-08-31 edition (192KB, 486KB, 111KB); ASCII anchors only",
    "kind": "http_contains",
    "url": "https://web.pref.hyogo.lg.jp/kf14/kankyoueigyoushisetsu_list.html",
    "present": ["000028_barbershop_all.xlsx", "000028_beauty_salon_all.xlsx", "000028_cleaningbusiness_all.xlsx", "192KB", "486KB", "111KB"]
  },
  {
    "id": "kakogawa-hyogo-food-permits-file",
    "claim": "The food permit list (4,519,769 B on 2026-10-06) answers a plain GET",
    "kind": "http_ok",
    "url": "https://web.pref.hyogo.lg.jp/kf14/documents/000028_food_business_lisence_all.xlsx",
    "min_bytes": 4000000
  },
  {
    "id": "kakogawa-hyogo-beauty-file",
    "claim": "The beauty register (496,756 B) answers a plain GET (the barber and laundry files are checked in Itami's brief, same host and folder)",
    "kind": "http_ok",
    "url": "https://web.pref.hyogo.lg.jp/kf14/documents/000028_beauty_salon_all.xlsx",
    "min_bytes": 400000
  },
  {
    "id": "kakogawa-hyogo-terms",
    "claim": "Hyogo's open-data page links the catalogue terms PDF (kiyaku_opendata.pdf, CC BY 4.0) and the catalogue",
    "kind": "http_contains",
    "url": "https://web.pref.hyogo.lg.jp/kk26/johoseisaku/opendata.html",
    "present": ["/kk26/johoseisaku/documents/kiyaku_opendata.pdf", "opendata/index.php"]
  },
  {
    "id": "kakogawa-mhlw-live",
    "claim": "MHLW's open-data file for Hyogo Prefecture (28000), the control, answers a plain keyless GET (1,579,737 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=28000_food_business_all.csv",
    "min_bytes": 1200000
  },
  {
    "id": "kakogawa-isj-block-live",
    "claim": "MLIT's block-level address file for Kakogawa (28210) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28210-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "kakogawa-isj-chome-live",
    "claim": "MLIT's town-chome address file for Kakogawa (28210) answers keyless - the centroid tier",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/28210-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "kakogawa-hoden-in-takasago",
    "claim": "JR West's station page gives 宝殿's address in Takasago (高砂市神爪), so it is not a Kakogawa station (its N02 point is 38 m beyond the N03 line)",
    "kind": "http_contains",
    "url": "https://www.jr-odekake.net/eki/top?id=0610615",
    "present": ["宝殿", "高砂市神爪"]
  },
  {
    "id": "kakogawa-jr-kakogawa-line-timetable",
    "claim": "JR West's weekday timetable for the Kakogawa Line at 加古川 toward 粟生・西脇市 (id 2859036001), the thinnest service counted (37 departures)",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/station-timetable/2859036001?date=20261007",
    "present": ["粟生・西脇市方面", "minute-item"]
  },
  {
    "id": "kakogawa-sanyo-hamanomiya-timetable",
    "claim": "Sanyo's weekday timetable PDF for 浜の宮 (334-27, toward Kobe and Osaka) answers a plain GET (87 departures counted)",
    "kind": "http_ok",
    "url": "https://www.sanyo-railway.co.jp/tt/index.php?code_station_from=334-27&code_direction=1&weekend=0&version=20200315",
    "min_bytes": 10000
  },
  {
    "id": "kakogawa-projected-crs",
    "claim": "Kakogawa projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 134.851,
    "expect": "EPSG:32653"
  }
]
```
