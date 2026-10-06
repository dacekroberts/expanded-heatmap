# Gifu — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, a pre-verdict converted
in staging's wave 5, calls 97 and 147: `docs/decisions_drafts/staging.md`,
"Wave 5, second half" and "Wave 5, the briefs"). The Step 0 downloads were
approved by the owner 2026-10-06 (call 147). **Step 0 measured 2026-10-06**
(staging). Into `data/gifu/raw/` (gitignored), each from its publisher's own
host with the project user-agent, each HTTP 200, under each URL's own file
name as `japan_fetch.get` saves:

- From `gifu-opendata.pref.gifu.lg.jp` (Gifu Prefecture's CKAN, **Gifu City's
  own packages**, organization `40010` 岐阜市): from **c212016-072**
  【岐阜市】食品等営業許可・届出一覧（2025）, the permit list
  `gifushisyokuhinkyokar7.6.1.csv` (920,447 B) and the notification list
  `gifushisyokuhintodokeder7.6.1.csv` (229,863 B), both as of **2025-06-01**;
  from **c212016-075** 【岐阜市】理容所・美容所届出施設一覧表（2024年度）, the
  barber and beauty registers `20250331riyo.xlsx` (47,980 B) and
  `20250331biyousho.xlsx` (89,934 B), as of **2025-03-31**.
- From `i2fas.mhlw.go.jp`: `21201_food_business_all.csv` (323,055 B), a
  control only.
- From `nlftp.mlit.go.jp`: `isj/21201-24.0a.zip` (729,522 B) and
  `isj/21201-19.0b.zip` (36,931 B).

**2,377,732 B in all.** Nothing else was downloaded. **Not requested** (owner,
2026-10-06): the city page's newer food list
(`https://www.city.gifu.lg.jp/kurashi/seikatukankyo/1002661/1002702.html`,
as of 2026-03-31 with monthly files to 2026-08), which the city's site terms
put behind the food hygiene section's permission (Shinjuku's and Chūō's
precedent). The XLSX twins of the two food CSVs were not fetched (the same
rows). **No laundry list exists** on the portal (below).

**Run `python scripts/brief_check.py gifu` before writing any code.** Then the
`japan-city` skill, **Akita's shape** (`docs/build_briefs/akita.md`: one
standing food list of every permit in term on its date, no
`rebuilt_register`, no months to merge) with **Toyota's precedent** for a
city list that leaves rows out by design (vending, vehicle, stall and
temporary permits; `docs/data_sources/japan.md`), Hamamatsu's for the
registers (one file per kind). Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py` from scratch scripts
only (`scripts/screen_japan_join.py` has no Gifu entry; its table is shared
code and was not edited). Rail: MLIT N02-25 cut at the N03 city line,
measured through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none stops in the city: 岐阜羽島 is in 羽島市); (2) **lines
served only by limited expresses DO count** (2026-09-28); (3) **the city line
only**: only stations inside the city get rings, JR and the private lines are
cut at the line, **a one-station stub stays as cut** (2026-09-27); an URBAN
line cut to ONE station is left out, its station kept through the other
lines, and drawn cut only where no other line serves that station (owner,
2026-10-06, calls 54 and 92); (4) **菓子製造業 and そうざい製造業 count, in
Retail**, the factory share measured and kept (2026-09-24, 2026-09-27); (5)
**the name rule**, version 2 (2026-10-06): a bare personal name is withheld
whatever the operator column holds; (6) **no page says "currently
operating"**. Also: no frequency floor for JR or private lines in Japan
(owner, 2026-10-06, call 46), any stretch at about 11 trains a day or fewer
named and drawn (call 86); fault-based cost clauses accepted for all of
Japan (2026-09-24); English station names from OSM `name:en`; every Japanese
city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Currency (owner, 2026-10-06, the band row):** built on the CKAN editions
with **their dates on the page** (food 2025-06-01, registers 2025-03-31);
the food edition is inside the five-year clock.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Gifu
carries `label_tier: "minor"` and goes in the **Japan East** view, as Toyota
and Ichinomiya do (`app/cities.py`); wave 4's first city to land retags Japan
into the eight regions, Gifu into **Chubu**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.
Gifu's dot sits about 14 km north of Ichinomiya's: measure the pair at build.

**`mode`: `metro`** (the owner's rule of 2026-10-02, applied as for
Ichinomiya, Kurume and Maebashi): JR is not the largest network inside the
city (3 station groups against Meitetsu's 9), and no subway or tram is drawn,
so the mode follows the backbone: Meitetsu's railways (N02 class 12).

---

## The one-line summary

**Two of three buckets from Gifu City's own CKAN packages (CC BY 2.0 as
declared; read 2026-10-06, staging records it).** The permit list of
**2025-06-01** holds **4,453 rows, 3,382 restaurants and cafés (飲食店営業
3,366 + 喫茶店営業 16), 66.7% of e-Stat's 5,070 in force** on 2025-03-31: the
city leaves out vending, vehicle, stall and temporary permits by design, and
old-law permits are present in proportion (not Kurashiki's trap); **the food
share is stated on the page** (call 125's precedent, Ichinomiya's 67.7%). The
city's own notification list adds **787 food-shop rows** (konbini,
greengrocers, dairies, supermarkets). Barbers 362 and beauty salons 1,177 as
of 2025-03-31: **100.0% and 100.0% of official**, the same date; **no laundry
list** (open call 2). Through `japan_eigyo`: **Food service 3,382, Retail 887
from permits + 787 from notifications**. Block join **95.4%** (permits),
93.6% (notifications), 94.5% / 94.7% (registers); unplaced 0.2-1.8%. MHLW's
file holds 40 open permits: a control, not a source. **Rail: 12 station
groups** (Meitetsu 9, JR Central 3), read from both operators' own
timetables: the thinnest is the Takayama Line at 長森, **37 and 40 trains a
day**; nothing near 11.

---

## Business leg — Gifu City's packages on the prefecture's CKAN

Host `https://gifu-opendata.pref.gifu.lg.jp` (CKAN, API
`/api/3/action/`). Every file is a plain GET under
`/dataset/<id>/resource/<id>/download/<name>`. **Read only these two
packages**: the older editions of the same lists under organization `40010`
(c212016-004, -042, -050, -055, -062, -065) carry other licences (`cc-by`,
`other-at`, `CC-BY-SA-2.1-JP`) and older dates; the prefecture's own
lists (c11222-0xx) cover the prefecture's health centres and exclude Gifu
City.

### Food: c212016-072, 食品等営業許可・届出一覧（2025）

Dataset `https://gifu-opendata.pref.gifu.lg.jp/dataset/c212016-072`
(registered 2026-01-14): 「2025年6月1日時点における営業許可・営業届出施設情報の一覧
・営業許可施設（自動販売機、自動車、露店、臨時営業を除く）・営業届出施設（自動販売機、自動車、露店、臨時営業を除く）」

| Resource | Bytes | Rows | What it is |
|---|---|---|---|
| 許可施設一覧(CSV) `gifushisyokuhinkyokar7.6.1.csv` (resource `16ef7794-d2b6-4d7d-8353-f55193432530`) | **920,447** | **4,453** | every permit in term on 2025-06-01, vending, vehicle, stall and temporary permits left out |
| 届出施設一覧(CSV) `gifushisyokuhintodokeder7.6.1.csv` (resource `6c758a77-694e-46bd-8d08-f67530532d5a`) | **229,863** | **1,093** | every notification on 2025-06-01, the same kinds left out |

- **UTF-8 with BOM, CRLF, header on row 1.** `japan_register.city_rows`
  reads every row as it stands. Dates are `YYYYMMDD` strings.
- **Permit columns**: 許可番号 (7 digits, **4,453 distinct**: a key on its
  own), **営業所名称**, **営業所在地**, 営業所電話番号, **営業種別**, **営業者名**,
  **代表者名**, 営業者住所, **許可開始日**, **許可満了日**, 初回許可開始年月日.
  **Notification columns**: 営業所名称, 営業所在地, 営業所電話番号, 営業種別,
  営業者名, 代表者名, 営業者住所, 届出年月日. No 業態 column in either.
- ⚠️ **Against the shared tuples:** 営業所名称 is in `NAME_COLS` and 営業者名 /
  代表者名 in `OPERATOR_COLS`, but **`ADDR_COLS` lacks 営業所在地** (without it
  `permits_from_rows` reads every address empty and every row as not a
  premises) and **`TYPE_COLS` lacks 営業種別** (without it every type reads
  empty and nothing is bucketed). The scratch measurement renamed both in
  memory (to 営業所所在地 and 営業の種類); the build adds them to the shared
  tuples, after every older spelling, or reads them through a `source_rows`
  in the config, and re-runs the Minato control.
- **Every address begins 岐阜市**; none reads 一円 or 市内 (vehicles and stalls
  are not in the list).
- **Permit types** (33): 飲食店営業 3,366, 菓子製造業 498, そうざい製造業 135,
  食肉販売業 134, 魚介類販売業 117, 麺類製造業 23, 食肉処理業 22, 漬物製造業 20,
  アイスクリーム類製造業 18, **喫茶店営業 16** (an old-law type), 密封包装食品製造業
  16, …, 複合型そうざい製造業 3.
- **Notification types** (22): 乳類販売業 203, 集団給食施設 201, その他の食料・飲料販売業
  141, 食肉販売業（包装済みの食肉のみの販売）134, 魚介類販売業（包装済みの魚介類のみの販売）
  91, コンビニエンスストア 80, 野菜果物販売業 78, その他の食料品製造・加工業 51, 米穀類販売業
  25, 百貨店、総合スーパー 20, コーヒー製造・加工業 18, 弁当販売業 15, ….
  届出年月日 2021-06-01 to 2025-05-19 (808 in 2021, the transition's filings).

### Coverage and old-law permits (Kurashiki's trap): not this list's problem

- **Old-law permits are in the file.** 1,626 rows (1,202 restaurants, 14
  cafés) began before 2021-06-01, from 2018-06-07, each ending 2025-08 to
  2029; old-law terms run 5.0 to 8.2 years (6.0 for 752). Starts per year:
  2018 21, 2019 463, 2020 806, 2021 872, 2022 542, 2023 644, 2024 760,
  2025 (to June) 345. 初回許可開始年月日 (the premises' first permit) is before
  2021-06-01 on 1,829 rows, back to 1951.
- **Every permit in term on its date**: no 許可満了日 before 2025-06-01 (the
  earliest is 2025-08-31); one permit begins after it (2025-06-20).
- **e-Stat 衛生行政報告例 FY2024** (`japan_official.estat()`), 岐阜県岐阜市,
  飲食店営業 in force 2025-03-31: **5,070** (old law 1,688, revised 3,382).
  The list's **3,382 restaurants and cafés are 66.7%** of it: the old-law
  starts 1,216 against 1,688 (72.0%), the later ones 2,166 against 3,382
  (64.0%), so the shortfall falls on both laws alike, as left-out vehicle,
  stall and temporary permits would. Retail types against the same tables
  (old + revised): 菓子 498 of 648 (76.9%), 食肉販売 134 of 152 (88.2%),
  魚介類販売 117 of 138 (84.8%), そうざい 138 (+ 複合型) of 178 (77.5%).
- **The share is stated on the page** (call 125's precedent: Ichinomiya,
  67.7%, the same left-out kinds; Toyota's 75%). The Economic Census control
  below says the fixed restaurants are not short.

### Currency

The edition is **2025-06-01**, 16 months before this brief. **1,223 permits
(933 restaurants) reached the end of their term between 2025-06-01 and
2026-10-06**: each was renewed or closed, which this edition cannot show. The
page carries the edition's date (the owner's currency call) and keeps "may
include closed premises". The newer city-page edition is not used (owner,
2026-10-06).

### Duplicates and closed premises

- **Unique by 許可番号** (4,453). **One premises, several permits**: 205 rows
  repeat an (address, trade name, type) in 78 groups (63 of them
  restaurants; 31 groups share one start date, 47 differ); 3,690 distinct
  (address, trade name). One pin per premises and bucket (trap 7) leaves
  **4,021 pins from 4,269** bucketed permit rows.
- **Closures are not marked** (no status column, no closure list); the page
  keeps "may include closed premises".
- **274 notified premises also hold a permit** at the same (address, trade
  name) (supermarkets and konbini with a butcher, deli or restaurant permit);
  one pin per premises and bucket keeps one.

### Counts through `japan_eigyo` (fixed premises)

- **Permits: Food service 3,382** (3,366 restaurants + 16 cafés), **Retail
  887** (菓子 498, deli 138, butcher 134, fishmonger 117). Left out: 184
  manufacturing types with no rule (麺類 23, 食肉処理 22, 漬物 20, アイスクリーム類
  18, 密封包装 16, …), as in every built city. No row is not a premises.
- ⚠️ **No 業態 column, so `FORM_RULES` sees nothing**: konbini,
  supermarkets, canteens and hotel restaurants holding 飲食店営業 stay in Food
  service, Kobe's, Osaka's, Toyonaka's, Aomori's and Hirakata's way. By
  trade-name word (counts only): konbini chains 129 (3.8% of 3,366),
  supermarkets 78, canteen, school, hospital or care words 81, hotels and inns
  52; snack, bar, lounge or club 86 (no hostess marker in the list:
  `docs/category_rules.md` R3, "wherever the register names them"). Factory
  words (工場 / センター) in 70 bucketed names: measured and kept.
- **Notifications: Retail 787** (dairy 203, other food and drink sales 141,
  butcher (packaged meat) 134, fishmonger (packaged fish) 91, konbini 80,
  greengrocer 78, rice 25, supermarket 20, bento 15). Left out: institutional
  catering 201, 102 manufacturing and processing types with no rule, mail
  order 3. One pin per premises and bucket: **609**, of which **489** are not
  already a Retail pin from the permits. Konbini appear under several
  notification types (by brand word: コンビニエンスストア 75, 乳類販売 51, packaged
  meat 49, packaged fish 49); the pin rule keeps one each. **In, as the
  Food-shops layer** (call 127b's precedent, here from the city's own list
  under the same licence and date, so not partial in MHLW's sense).

**Economic Census control** (`scripts/japan_census_control.py` at build):
the 2021 census counts **2,165** 飲食店 establishments in 21201
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 3,268 distinct placed
Food-service premises is **1.51 per establishment**, just under the built
cities' 1.56-1.92. The list's left-out kinds are not establishments in the
census either, so the 66.7% share is not a shortfall of fixed restaurants.
Record the figure at build.

### MHLW's file (21201), a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=21201_food_business_all.csv`:
**323,055 B, 989 rows** (届出 944, 許可 40, 届出(廃業) 3, 許可(廃業) 2), the
national schema. **40 open permits** (飲食店 32, 魚介類販売 4, 菓子 2, 食肉販売
2), **32 of them begun after 2025-06-01**: newer than the city's edition, 0.6%
of e-Stat's restaurants; 4 carry a city permit number, 8 match a city row by
(address, trade name). MHLW's extra permits stay out (Ichinomiya's call 126).
- **944 open notifications**, 494 addressed: vending 426, その他の食料・飲料販売業
  230, 乳類販売業 89, 百貨店、総合スーパー 79, …; **322 addressed in a bucket,
  57 at an address in the city's lists; the other 265 are all その他の食料・飲料販売業**,
  with no notification date in the file (open call 1).
- **Its own coordinates against the block point**: median **32 m**, 97.6%
  within 250 m (41 rows). With the block join at 95%, no own-point fallback
  is needed (call 127c applies only where MHLW holds the missed row).

### Personal services: c212016-075, 理容所・美容所届出施設一覧表（2024年度）

Dataset `https://gifu-opendata.pref.gifu.lg.jp/dataset/c212016-075`
(registered 2026-01-14): 「岐阜市内における理容所・美容所届出施設一覧表（令和7年3月31日現在）」

| Resource | Bytes | Rows | Official (e-Stat FY2024 第10表, 2025-03-31) | Share |
|---|---|---|---|---|
| `20250331riyo.xlsx` 理容所全届出施設一覧表 (resource `fe88c7c1-3bbe-42ed-aa77-525f940ed6fe`) | **47,980** | **362** | barbers 362 | **100.0%** |
| `20250331biyousho.xlsx` 美容所全届出施設一覧表 (resource `0030e554-51b5-47ca-9bec-5724fb0dc617`) | **89,934** | **1,177** | beauty salons 1,177 | **100.0%** |

(Official from `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv`,
岐阜県岐阜市, the same date as the lists.)

- **Columns**: 確認日, **施設名称**, **施設住所**, 施設ＴＥＬ, **申請者氏名**. 施設住所
  is in `ADDR_COLS`, 施設名称 in `NAME_COLS`, 申請者氏名 in `OPERATOR_COLS`: no
  shared-code change for the registers. **No type column**: one file per
  kind, so the config names the kind per file (`source_rows` or
  `SOURCE_KIND`, Hamamatsu's registers).
- **確認日 is a wareki string** (`H 1. 1.10`, `R 6. 4. 1`, `S63. 9.12`);
  `japan_register.wareki_date` reads the Heisei and Reiwa ones (211 of 362
  barbers, 935 of 1,177 beauty) and **none written in Shōwa**. The map shows
  no date, so nothing depends on it; a shared-code fix is optional.
- **Every address is in 岐阜市.** Beauty: **4 rows read 一円** (a visiting
  service, not a premises: `permits_from_rows`' test drops them). Repeats:
  barber 0, beauty 1 (address, name); **13 premises are in both registers**
  (one pin per premises and bucket keeps one per bucket).
- **Standing registers** (one 確認日 per premises, back to the Shōwa era);
  closures are not marked, so the page keeps "may include closed premises".

### No laundry list (open call 2)

Organization `40010` holds 72 packages on the portal; **none is a laundry
list** (package_search under the organization for クリーニング: count 0; the
hygiene packages are food, barber and beauty, and inns). The portal's
クリーニング hits are the prefecture's statistical yearbooks and its
pre-2012 counts. e-Stat FY2024 第11表 counts 276 クリーニング所 in Gifu City,
182 of them 取次所, with no list to measure. Personal services is barbers and
beauty salons only, disclosed on the page and in What Is Excluded (Akita's
precedent; open call 2 confirms it for Gifu).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/21201-24.0a.zip` (729,522 B,
130,124 rows, **129,307 block keys** with the 小字 aliases), town-chōme
`.../19.0b/21201-19.0b.zip` (36,931 B, **2,143**). `japan.CITIES` entry at
build: `"gifu": {"name": "岐阜市", "pref": "21", "epsg": 32653, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["21201"]}`.

| Tier, today's shared code | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| Permits, fixed premises in a bucket (4,269) | **95.4%** | 4.4% | **0.2%** |
| … Food service (3,382) / Retail (887) | 95.6% / 94.6% | 4.2 / 5.3 | 0.2 / 0.1 |
| Notifications in a bucket (787) | **93.6%** | 5.7% | 0.6% |
| Barbers (362) | **94.5%** | 3.9% | 1.7% |
| Beauty salons (1,173 fixed) | **94.7%** | 3.5% | 1.8% |

**The misses, read** (towns only, scratch `measure.py` and `more.py`):
- **Chōme tier**: **長良福光 48 rows**, a town MLIT's town file knows but
  whose block edition holds no number at all (also 古市場神田 8, 長良志段見 7,
  長良井田, 太郎丸北郷): they take the town's centroid, which is the best MLIT
  offers. A few in towns MLIT does number (美殿町 5, 柳津町蓮池2丁目 4) are numbers
  the edition lacks.
- **Unplaced (about 7 permit rows, 5 notifications, 6 barbers, 21 beauty
  salons)**: (a) **鷺山(向井町)**, a 字 written in brackets where MLIT keys
  鷺山字向井町 (and 鷺山向井町 without either): a bracket-as-字 rule would take
  them; (b) **鷺山南**, 鏡島三軒屋 and 南鏡島3丁目, names MLIT's 2025 files do not
  hold (newer names or common names). Each rule is shared code: follow it with
  the Minato control (`screen_japan_join.py minato`) and every city screen.
  At 0.2% unplaced for the permits, none is needed to build.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_21_GML.zip`, N03 code 21201
(**203.6 km²**, extent W 136.679, S 35.351, E 136.886, N 35.543; the 2006
merger brought in 柳津町). Read with `stub_test()`'s method and an in-memory
`CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 各務原線 (名古屋鉄道, 12) | Meitetsu Kakamigahara Line | **6 / 18** | 名鉄岐阜, 田神, 細畑, 切通, 手力, 高田橋 |
| 名古屋本線 (名古屋鉄道, 12) | Meitetsu Nagoya Main Line | **3 / 60** | 名鉄岐阜, 加納, 茶所 |
| 竹鼻線 (名古屋鉄道, 12) | Meitetsu Takehana Line | **1 / 9** | 柳津 |
| 東海道線 (東海旅客鉄道, 11) | JR Tōkaidō Line | **2 / 89** | 岐阜, 西岐阜 |
| 高山線 (東海旅客鉄道, 11) | JR Takayama Line | **2 / 36** | 岐阜, 長森 |

- **14 station records, 12 N02_005g groups** (名鉄岐阜 Main Line +
  Kakamigahara Line, 102 m; 岐阜 Tōkaidō + Takayama, 0 m). No name in two
  groups.
- **Close pairs** (trap 1: MLIT keeps them apart, and so does step 1):
  **名鉄岐阜 / 岐阜 418 m** (Meitetsu's and JR's terminals, two names, two
  groups: Ichinomiya's 名鉄一宮 / 尾張一宮 kept apart at 38 m, not Toyonaka's
  same-name join), 加納 / 茶所 428 m, 長森 / 手力 449 m. **Median
  nearest-station gap 641 m** (418 to 4,635): rings by the spacing rule at
  build.
- **Shinkansen**: none in N02 inside the city.
- **Cut at the line** (named by N03 municipality at build): the Tōkaidō Line
  87 beyond (other prefectures 81, 大垣市 3, 瑞穂市, 垂井町, 関ケ原町 1 each),
  the Takayama Line 34 (下呂市 8, 飛騨市 7, 高山市 6, 各務原市 4, …), the Main
  Line 57 (other prefectures 55, 岐南町 1, 笠松町 1), the Kakamigahara Line 12
  (各務原市 12), the Takehana Line 8 (羽島市 6, 笠松町 2).
- **The light-rail/rail test**: all five are heavy rail (N02 class 12,
  Meitetsu's railways; class 11, JR conventional). No tram or light rail
  (the Gifu tramway closed in 2005 and is not in N02).
- **The stub test.** The **Takehana Line keeps one station of 9, 柳津**, 453 m
  from the city line: a private one-station stub, **kept as cut** by the
  standing call (no owner question; Kobe's precedent). 柳津 has no other line,
  so its ring comes from the Takehana Line itself. ⚠️ At build: the line's
  permanent label and legend entry on a short stub (measure placement in a
  scratch render; Akita's Oga Line note). The Main Line's 3 of 60 and the
  Kakamigahara Line's 6 of 18 end at their own terminus, 名鉄岐阜, inside the
  city; the Tōkaidō Line's 2 of 89 and the Takayama Line's 2 of 36 are main
  lines cut at the line, not stubs.
- **Frequency, read 2026-10-06 from both operators' own timetables** by
  plain GET with the project user-agent, every request HTTP 200, none
  refused. Counts are weekday departures per direction; only counts are
  recorded, never a timetable on the page.
  - **JR Central** (`railway.jr-central.co.jp/time-schedule/`, the station
    index `search/ResultControl?st=<code>` (岐阜 h1, 長森 h2, 西岐阜 b72) and
    its March 2026 PDFs under `srch/_pdf/data/202603/`), counted from
    `pdftotext -table` by the scratch `jrc.py` (each departure once; track
    and destination marks skipped; checked by hand against 長森's and
    西岐阜's up pages). `[平休]` pages carry one timetable for every day.
  - **Meitetsu** (`trainbus.meitetsu.co.jp`,
    `meitetsu-transfer/pc/diagram/TrainDiagram?startId=<node>&linkId=<line>&direction=<up|down>`,
    the weekday column, Wednesday 2026-10-07), counted by the scratch
    `mtday.py` (Ichinomiya's method).

  | Station (line, direction) | Weekday departures | Per hour 10-15 |
  |---|---|---|
  | 岐阜 (Tōkaidō, to 名古屋 / to 大垣) | 173 / 92 | 9-10 / 4-5 |
  | 岐阜 (Takayama, to 美濃太田・高山; the line's terminus) | 47 | 2-3 |
  | 西岐阜 (Tōkaidō, to 岐阜 / to 大垣) | 87 / 81 | 4 / 4 |
  | **長森 (Takayama, to 岐阜 / to 美濃太田)** | **40 / 37** | 2 / 2 |
  | 名鉄岐阜 (Main Line, to 名鉄一宮・名古屋 / via 笠松 to 竹鼻・新羽島) | 151 / 48 | 8-12 / 2-4 (07-19) |
  | 名鉄岐阜 (Kakamigahara, to 犬山) | 72 | 4 |
  | 加納, 茶所 (Main Line, to 名古屋 / to 名鉄岐阜) | 68 / 65 each, all 普通 | 4 |
  | 田神, 高田橋 (Kakamigahara, to 犬山 / to 名鉄岐阜) | 72 / 73, all 普通 | 4 |
  | 細畑, 切通, 手力 (Kakamigahara, to 犬山) | 72, all 普通 | 3-5 (07-19) |
  | 柳津 (Takehana, to 笠松・名鉄岐阜 / to 竹鼻・新羽島) | 48 / 49, all 普通 | 2-4 (07-19) |

  **The thinnest stretch is the Takayama Line at 長森, 37 and 40 trains a
  day; the Takehana Line at 柳津 runs 48 and 49. Nothing here is at or near
  11 a day**, so call 86 names no stretch. Counts at 岐阜 include limited
  expresses (the Takayama Line's Hida); the master list row's hourly figures
  agree (Tōkaidō 9-10 an hour at 岐阜, 4 at 西岐阜, Takayama 2, Meitetsu 4).
- ⚠️ **Gate 3** at build: JR Central's station counts inside the city
  (Tōkaidō 2, Takayama 2) and Meitetsu's (Main Line NH58-NH60, 3;
  Kakamigahara Line KG12-KG16 plus 名鉄岐阜, 6; Takehana Line TH02, 1).
  **OSM `name:en`** for 12 groups (one Overpass query at build, in the box
  below; not queried here). Line colors from Toyota's and Ichinomiya's
  Meitetsu precedent, on both basemaps.

## Scope

**Gifu City.** The Tōkaidō Line runs on to Nagoya and Ōgaki, the Takayama
Line to 各務原 and 高山, the Main Line to 笠松 and Nagoya, the Kakamigahara Line
to 各務原 and 犬山, the Takehana Line to 羽島; cut at the line.

## Licences — read 2026-10-06 (`licence-read`, recorded by staging)

**As declared on each dataset page**: ライセンス `CC-BY-2.0` (the CKAN
`license_id`, no licence URL), author 岐阜市. The full read ran separately on
2026-10-06 and is done; **staging records its verdict and conditions** in
`docs/decisions_drafts/staging.md` ("Wave 5, second half"): CC BY 2.0 as
declared (the version taken from the free-text field), the portal's
prescribed credit for a modified work naming 岐阜市, and the portal's §5 cost
clause read as fault-based (Tokyo's class). Take the credit wording from
staging's record, not from here; no verdict is written in this brief. The
city page's newer edition is a different source whose site terms need the
food hygiene section's permission (not used).

- **MHLW open data** (a control; only if open call 1 is taken): PDL 1.0 as
  recorded in `docs/data_sources/japan.md`, its 出典 line and who processed
  it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **JR Central's and Meitetsu's timetables**: read for counts only,
  never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The food lists carry the operator block**: **営業者名** (no company marker
  on 2,098 of 4,453 permit rows and 414 of 1,093 notifications: the shape of
  a sole trader's own name; 57 permit rows without a marker carry a
  representative, other legal persons), **代表者名** (a person, filled on
  2,412 permit rows), **営業者住所** (the operator's own address, filled on the
  same 2,412) and 営業所電話番号. Step 2 drops 営業者住所 and both phone columns
  at read and reads 営業者名 and 代表者名 IN MEMORY for the name rule only
  (both already in `OPERATOR_COLS`); none reaches an output.
- **The registers carry 申請者氏名**: no company marker on 328 of 362 barbers
  and 885 of 1,177 beauty salons. Select 施設名称 and 施設住所 only; 施設ＴＥＬ is
  never selected.
- **The name rule, version 2, measured in memory** (answers only, never a
  value): permits **2 rows** whose trade name is the operator's own name,
  **both among fixed premises in a bucket**, **0 bare personal names**;
  notifications 2 (none in a bucket), 0 bare; barbers 0; beauty salons 0.
  MHLW 1 (法人名), only if open call 1 brings its rows in. No value was printed
  or stored.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected.
- Run `check_personal_exposure.py gifu` (`japan=True`) after step 2: the rows
  that matter are the sole traders' trade names; it must print 0. Record the
  verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Chubu after the retag), `label_tier: "minor"`,
`"country": "Japan"`. Project to **UTM 53N (EPSG:32653)**: the N03 centroid
lies at longitude 136.765, the extent 136.679 to 136.886, all inside the
132-138 band (computed here, never copied). OSM box from the N03 extent,
rounded out: (35.35, 136.67, 35.55, 136.89).

**Scaffold**: `scaffold_city.py --slug gifu --name Gifu --system-name
"Meitetsu and JR Central" --taxonomy japan_eigyo --lat 35.448 --lon 136.765
--region "Japan East" --country Japan --mode metro --page-number <N>`
(`--dry-run` first), with the page number claimed in `docs/session_roles.md`
at build, not here.

## Owner calls

**Made (do not re-ask):** Band A on Gifu City's CKAN packages c212016-072
and -075 (owner, 2026-10-06, call 97); the Step 0 downloads (call 147); the
city page's newer edition not requested; the editions' dates on the page
(currency); the standing Japanese calls above; `mode: metro`; the minor tier
and Japan East (Chubu after the retag); the Takehana Line drawn as cut from
柳津 (standing call, a private stub); no frequency floor (call 46).

**Precedents applied (not re-asked):** the food share stated on the page
(call 125, Ichinomiya); the city's notification list in as the Food-shops
layer (call 127b, here the city's own list); MHLW's extra permits out (call
126); no own-point fallback (127c: the join misses 0.2%); konbini on a
restaurant permit stay in Food service where no 業態 column exists (Aomori,
Hirakata).

**Open, with a recommendation:**

1. **MHLW's 265 unmatched addressed notifications** (all その他の食料・飲料販売業,
   no notification date in the file; the other 57 sit at an address the
   city's lists already hold). *Recommend leaving them out, MHLW a control
   only*: the city's own notification list already supplies the Food-shops
   layer at one date and one licence; the 265 are a single catch-all type of
   unknown date and nature (not measured against the city's list beyond the
   address). The tradeoff is up to 265 more food-shop pins, possibly newer
   than 2025-06-01, against a layer that mixes two publishers and two dates.
2. **The laundry gap**: no laundry list anywhere on the portal under
   organization 40010. *Recommend building with Personal services as
   barbers and beauty salons only, the gap disclosed on the page and in What
   Is Excluded* (Akita's precedent, 2026-10-06). The tradeoff is a thinner
   Personal-services bucket (1,535 rows) against waiting for a list the city
   does not publish.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `ADDR_COLS` + 営業所在地; `TYPE_COLS` + 営業種別 (or a `source_rows`
  for the two food files); optionally a bracket-as-字 rule for 鷺山(向井町) and
  Shōwa dates in `wareki_date`; nothing for the registers.
- `SOURCE_AS_OF`: food and notifications 2025-06-01, registers 2025-03-31;
  the pinned CKAN resource URLs (the editions do not roll; a new edition is a
  new package, c212016-0xx, to re-measure and re-read).
- The census ratio (1.51) recorded; the food share (66.7%) as stated on the
  page; one pin per premises and bucket across permits and notifications.
- The Takehana Line's label on its stub; gate 3 (JR Central, Meitetsu); OSM
  `name:en`; line colors on both basemaps; the opening view (`map-view`);
  the factory share; `check_provenance.py`; `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "gifu-food-dataset-page",
    "claim": "Gifu City's food package c212016-072: permits and notifications as of 2025-06-01, vending, vehicle, stall and temporary permits left out, CC-BY-2.0 as declared, both CSVs listed",
    "kind": "http_contains",
    "url": "https://gifu-opendata.pref.gifu.lg.jp/dataset/c212016-072",
    "present": ["食品等営業許可・届出一覧（2025）", "2025年6月1日", "自動販売機、自動車、露店、臨時営業を除く", "CC-BY-2.0", "gifushisyokuhinkyokar7.6.1.csv", "gifushisyokuhintodokeder7.6.1.csv"]
  },
  {
    "id": "gifu-food-package-api",
    "claim": "The package's API record: organization 40010, CC-BY-2.0, the permit CSV 920,447 B and the notification CSV 229,863 B (ASCII anchors: the API escapes Japanese)",
    "kind": "http_contains",
    "url": "https://gifu-opendata.pref.gifu.lg.jp/api/3/action/package_show?id=c212016-072",
    "present": ["\"name\": \"40010\"", "CC-BY-2.0", "920447", "229863", "gifushisyokuhinkyokar7.6.1.csv"]
  },
  {
    "id": "gifu-food-permits-file",
    "claim": "The 2025-06-01 permit list (920,447 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://gifu-opendata.pref.gifu.lg.jp/dataset/2f9f1b1c-be25-4a27-96c6-47b597f1a0bd/resource/16ef7794-d2b6-4d7d-8353-f55193432530/download/gifushisyokuhinkyokar7.6.1.csv",
    "min_bytes": 900000
  },
  {
    "id": "gifu-food-notifications-file",
    "claim": "The 2025-06-01 notification list (229,863 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://gifu-opendata.pref.gifu.lg.jp/dataset/2f9f1b1c-be25-4a27-96c6-47b597f1a0bd/resource/6c758a77-694e-46bd-8d08-f67530532d5a/download/gifushisyokuhintodokeder7.6.1.csv",
    "min_bytes": 200000
  },
  {
    "id": "gifu-registers-dataset-page",
    "claim": "Gifu City's barber and beauty package c212016-075, as of 2025-03-31 (令和7年3月31日), CC-BY-2.0 as declared",
    "kind": "http_contains",
    "url": "https://gifu-opendata.pref.gifu.lg.jp/dataset/c212016-075",
    "present": ["理容所・美容所届出施設一覧表（2024年度）", "令和7年3月31日", "20250331riyo.xlsx", "20250331biyousho.xlsx", "CC-BY-2.0"]
  },
  {
    "id": "gifu-barber-file",
    "claim": "The barber register (47,980 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://gifu-opendata.pref.gifu.lg.jp/dataset/0e989e17-7093-4cbd-b931-6a24cf93fdb2/resource/fe88c7c1-3bbe-42ed-aa77-525f940ed6fe/download/20250331riyo.xlsx",
    "min_bytes": 40000
  },
  {
    "id": "gifu-beauty-file",
    "claim": "The beauty register (89,934 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://gifu-opendata.pref.gifu.lg.jp/dataset/0e989e17-7093-4cbd-b931-6a24cf93fdb2/resource/0030e554-51b5-47ca-9bec-5724fb0dc617/download/20250331biyousho.xlsx",
    "min_bytes": 80000
  },
  {
    "id": "gifu-no-laundry-list",
    "claim": "No laundry list under Gifu City's organization (40010): a package search for クリーニング returns count 0 (open call 2)",
    "kind": "http_contains",
    "url": "https://gifu-opendata.pref.gifu.lg.jp/api/3/action/package_search?q=%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0&fq=organization:40010&rows=0",
    "present": ["\"count\": 0"]
  },
  {
    "id": "gifu-mhlw-live",
    "claim": "MHLW's open-data file for Gifu (21201) answers a plain keyless GET (a control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=21201_food_business_all.csv",
    "min_bytes": 250000
  },
  {
    "id": "gifu-isj-block-live",
    "claim": "MLIT's block-level address file for Gifu (21201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/21201-24.0a.zip",
    "min_bytes": 600000
  },
  {
    "id": "gifu-isj-chome-live",
    "claim": "MLIT's town-chōme file for Gifu (21201) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/21201-19.0b.zip",
    "min_bytes": 30000
  },
  {
    "id": "gifu-jrc-gifu-index",
    "claim": "JR Central's timetable index for 岐阜 (st=h1) links the weekday Tōkaidō pages and the Takayama page read (ASCII file names)",
    "kind": "http_contains",
    "url": "https://railway.jr-central.co.jp/time-schedule/search/ResultControl?st=h1",
    "present": ["tokaido_Gifu_A_w_u.pdf", "tokaido_Gifu_A_w_d.pdf", "takayama_Gifu_B_wh_d.pdf"]
  },
  {
    "id": "gifu-jrc-nagamori-index",
    "claim": "JR Central's timetable index for 長森 (st=h2), the thinnest station (37 and 40 a day), links its two Takayama Line pages",
    "kind": "http_contains",
    "url": "https://railway.jr-central.co.jp/time-schedule/search/ResultControl?st=h2",
    "present": ["takayama_Nagamori_B_wh_u.pdf", "takayama_Nagamori_B_wh_d.pdf"]
  },
  {
    "id": "gifu-meitetsu-yanaizu-timetable",
    "claim": "Meitetsu's timetable for 柳津 (TH02), the Takehana Line's one station in the city, toward 笠松・名鉄岐阜",
    "kind": "http_contains",
    "url": "https://trainbus.meitetsu.co.jp/meitetsu-transfer/pc/diagram/TrainDiagram?startId=00008812&linkId=00000876&direction=up",
    "present": ["柳津", "TH02", "竹鼻線"]
  },
  {
    "id": "gifu-meitetsu-kakamigahara-timetable",
    "claim": "Meitetsu's timetable for 名鉄岐阜 (NH60) lists the Kakamigahara Line toward 犬山",
    "kind": "http_contains",
    "url": "https://trainbus.meitetsu.co.jp/meitetsu-transfer/pc/diagram/TrainDiagram?startId=00004202&linkId=00000863&direction=up",
    "present": ["名鉄岐阜", "各務原線"]
  },
  {
    "id": "gifu-projected-crs",
    "claim": "Gifu projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 136.765,
    "expect": "EPSG:32653"
  }
]
```
