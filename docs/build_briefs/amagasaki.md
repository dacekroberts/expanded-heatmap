# Amagasaki — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, call 118: "Amagasaki,
Suita, Itami, Kakogawa (call 118: 101-106% with old-law permits)";
`docs/decisions_drafts/staging.md`, "Wave 5, second half"). Banded C first
with its files approved to measure (call 90; the same file's "Wave 5"
entry), the block join approved with call 106. **Step 0 measured
2026-10-06** (staging). In `data/amagasaki/raw/` (gitignored), each from its
publisher's own host with the project user-agent, each HTTP 200, under each
URL's own file name:

- From `www.city.amagasaki.hyogo.jp` (staging's call-90 measurement, 2026-10-06):
  the food permit list `kyoka202608.csv` (1,752,694 B) and the food
  notification list `todoke202608.csv` (467,150 B), both as of 2026-08-31;
  the barber, beauty and laundry registers `riyouR80831.csv` (47,411 B),
  `biyouR80831.csv` (153,760 B) and `cleaningR80831.csv` (75,137 B), as of
  2026-08-31.
- From `nlftp.mlit.go.jp` (call 106): `isj/28202-24.0a.zip` (182,821 B) and
  `isj/28202-19.0b.zip` (11,179 B).
- From `i2fas.mhlw.go.jp` (this brief, the control approved for round 3):
  `28202_food_business_all.csv` (392,239 B).

**3,082,391 B in all.** Nothing else was downloaded. Hyōgo Prefecture's own
lists (fetched for Itami and Kakogawa) hold **no Amagasaki row**: a core
city, Amagasaki licenses through its own health centre.

**Run `python scripts/brief_check.py amagasaki` before writing any code.**
Then the `japan-city` skill, **Akita's shape** for a city list of every
permit in term on its date with MHLW as a control (`docs/build_briefs/akita.md`),
**Yokkaichi's** for the city's own notification list as Food shops
(`docs/build_briefs/yokkaichi.md`), Hamamatsu's for one register file per
kind. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Amagasaki entry; its table is shared
code and was not edited). Rail: MLIT N02-25 cut at the N03 city line,
measured through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

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
version 2 (2026-10-06): a bare personal name is withheld whatever the
operator column holds; (6) **no page says "currently operating"**. Also: no
frequency floor for JR or private lines in Japan (owner, 2026-10-06, call
46), any stretch at about 11 trains a day or fewer named and drawn (call 86;
none here); fault-based cost clauses accepted for all of Japan (2026-09-24);
English station names from OSM `name:en`; every Japanese city reads
`WAVE2_RULES` (owner, 2026-10-04); food-retail notifications count where a
city publishes them (the `japan_eigyo` rule; Tokyo's wards, Yokkaichi).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02, 2026-10-04).**
Amagasaki carries `label_tier: "minor"` and goes in the **Japan West** view
today; wave 4's first city to land retags Japan into the eight regions, and
Amagasaki (Hyōgo) goes into **Kansai**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye; it
borders Osaka (built) and Itami (Band A).

**✅ `mode`: `metro`.** JR West, Hanshin and Hankyu are all heavy rail (N02
classes 11 and 12); no subway, tram or light rail. The owner's rule of
2026-10-02 as Akita's and Toyonaka's briefs apply it; nothing reads as tram.

---

## The one-line summary

**All three buckets, and Food shops, from the city's own CSVs (CC BY 4.0 as
stated; the licence read is pending, staging records it).** The food permit
list of every permit in term on **2026-08-31** holds **6,839 rows, 5,813
restaurants (飲食店営業), 105.8% of e-Stat's 5,495 in force**, old-law permits
included (911: not Kurashiki's trap). The city's **notification list (2,272)
gives 1,295 Retail rows** (konbini, supermarkets, dairies, greengrocers) by
the standing notification rule. Barbers 341, beauty salons 987, laundries
368 premises as of 2026-08-31: **98.3%, 102.5%, 98.9% of official**. Through
`japan_eigyo`: **Food service 3,946 rows (3,828 pins), Retail 893 (695)**
from the permits, **plus 1,295 (1,290) from the notifications**. Block join
**98.9%** over permits and registers (food 98.7%, registers 98.1-99.7%),
notifications 97.5%; **5 rows unplaced in all**. MHLW's file holds 2% of the
city's permits: a control, not a source. **Rail: 12 `N02_005g` groups**
(Hanshin 5, JR West 4, Hankyu 3) on seven N02 lines, read from the
operators' own timetables: **4.0 to 20.5 trains an hour midday, the thinnest
59 a day one way**.

---

## Business leg — the city's 生活衛生課 open data

Host `https://www.city.amagasaki.hyogo.jp` (the city's own CMS, under
`/op_data/1000922/`; no catalogue API). Every file is a plain GET under
`/_res/projects/default_project/_page_/001/001/`. All five CSVs read with
`japan_register.city_rows` as they stand.

### Food: 食品関係営業施設, page 1001025

Page `https://www.city.amagasaki.hyogo.jp/op_data/1000922/1001025.html`
(更新日 2026-09-08).

| File (under `…/001/001/025/`) | Bytes | Rows | What it is |
|---|---|---|---|
| `kyoka202608.csv` 食品営業許可施設【令和8年(2026年）8月31日現在】 | **1,752,694** | **6,839** | every permit in term on 2026-08-31 (許可年月日 2019-06-06 to 2026-08-31; 許可終了日 2026-08-31 to 2033-08-31, none earlier) |
| `todoke202608.csv` 食品営業届出施設【令和8年(2026年）8月31日現在】 | **467,150** | **2,272** | every notification (届出年月日 2021-06-01 to 2026-08-27) |

- **Named by month** (`kyoka202608`, `todoke202608`); the page does not say
  how often it is refreshed. `japan_fetch.current_url` takes a
  `SOURCE_LINKS` regex for each (`kyoka\d{6}\.csv`, `todoke\d{6}\.csv`,
  Akita's and Kawasaki's precedent), and `as_of` is the date in the link's
  title, never today.
- **Permit columns**: **施設名称**, an unnamed column (the permit number's
  `第N-N号`, on every row), **施設所在地**, 施設電話番号, **申請者名**,
  **代表者名**, 申請者住所, 申請者電話番号, 許可年月日, **許可終了日**,
  初回許可年月日, 当初許可日, 許可番号 (only the issuing office's prefix,
  尼崎市指令(生) 6,555 · (尼保生) 284), **業種**, **業態**, **自動車登録番号**
  (445), 給水設備 (40L, 80L, 200L, 準固定施設: the stall classes).
- **Notification columns**: 施設名称, an unnamed column (218), 施設所在地,
  施設電話番号, 申請者名 (1,487), 代表者名, 申請者住所, 申請者電話番号,
  届出年月日, **業態** (the notification type: no 業種 column).
- **Against the shared tuples**: 施設所在地 is in `ADDR_COLS`, 施設名称 in
  `NAME_COLS`, 業種 in `TYPE_COLS`, 業態 in `FORM_COLS`, 申請者名 and 代表者名
  in `OPERATOR_COLS`. No shared-code change for the permits. **The
  notifications carry their type in 業態**, which the shared reader takes as
  the form, so a `source_rows` copies it into the type (Yokkaichi's
  notifications read as types; measured so here).
- **The key**: the number (prefix plus the unnamed column) repeats (1,811
  distinct): it restarts each year. **(number, 許可年月日) is unique on all
  6,839.** MHLW writes the same numbers with a suffix, `第N-N号(N)`.
- **Permit types**: 飲食店営業 **5,813**, 菓子製造業 383, 食肉販売業 170,
  魚介類販売業 132, そうざい製造業 86, 調理機能付き自動販売機 53, 冷凍食品製造業
  30, … 喫茶店営業 11 (29 types).
- **業態 on restaurants** (118 values): 居酒屋 797, 喫茶店 567, **スナック・ラウンジ
  407**, バー 376, **露店飲食店 320**, **普通自動車による飲食店 308**, レストラン
  249, その他 243, **カラオケ 221**, 中華料理店 187, … **総菜屋 122**, 軽自動車による
  飲食店 118, **給食社会福祉施設 103**, 給食事業所 76, 給食学校 47, … ホテルの飲食店
  23, 仕出し屋 12, クラブ又はナイトクラブ 7. `FORM_RULES` read every one of them
  (below). The 7 クラブ又はナイトクラブ match no rule and stay in Food service,
  as plain バー does (`docs/category_rules.md` R3 names hostess venues only).

### Old-law coverage (Kurashiki's trap) — not this list's problem

- **Old-law permits are in the file**: **911 restaurants** granted before
  2021-06-01 (from 2019-06-06), in term on the list's date: **174 end on
  2026-08-31 itself**, 207 on 2026-11-30, 496 in 2027, 34 in 2028. The city
  ends permits at a month's end.
- **e-Stat 衛生行政報告例 FY2024** (`japan_official.estat()`), 兵庫県尼崎市,
  飲食店営業 in force 2025-03-31: **5,495** (old law 1,872, revised 3,623).
  The list's **5,813 restaurants are 105.8%** of it, vehicles (445) and stalls
  (320) on both sides, the list dated 17 months later. The old-law count fell
  from 3,498 (FY2022) to 2,604 and 1,872 as permits lapsed or were renewed;
  911 in term in 2026-08 continues that line.
- **⚠️ The 174 permits ending 2026-08-31** are in term on the list's date and
  lapse the next day unless renewed (a renewal appears as a new permit in the
  next edition). The build reads the current edition (`SOURCE_LINKS`), which
  settles it.

### Duplicates and closed premises

- **One premises, several permits**: 235 rows repeat an (address, trade
  name, type) in 222 groups, 29 of them with the same 許可年月日 too; 6,071
  distinct (address, trade name). One pin per premises and bucket (trap 7)
  leaves **3,828 Food-service and 695 Retail pins** from 3,946 and 893 rows.
- **Closures are not marked** (no status column); the list holds permits in
  term, and the page does not say whether a closed premises leaves it before
  its term ends. The page keeps "may include closed premises". MHLW holds 2%
  of the city's permits, too few for Fukuyama's closure filter.

### Counts through `japan_eigyo` (permits, fixed premises)

Vehicles (自動車登録番号, 445) and stalls are all addressed 尼崎市内一円, so
`permits_from_rows` already marks them not a premises (316 non-vehicle 一円
rows, 306 of them 露店飲食店): **no city rule is needed**. Of 6,394 non-vehicle
rows: **Food service 3,946, Retail 893** (菓子 383, deli 208 of which 204 are
restaurant permits filed 総菜屋 by 業態, butcher 170, fishmonger 132). Left
out: **hostess venue 410** (スナック・ラウンジ, by 業態), **not a premises 316**,
**institutional catering 312** (給食…, by 業態), **entertainment venue 221**
(カラオケ, by 業態), no rule 191 (manufacturing types), vending 53, inside
accommodation 26, temporary 14, event catering 12.

**Economic Census control** (`scripts/japan_census_control.py` at build):
the 2021 census counts **1,988** 飲食店 establishments in 28202; **3,826**
placed Food-service premises is **1.92 per establishment**, at the top of the
built cities' 1.56-1.92 (a list with 業態, so canteens, snack bars and
karaoke are out). Factory words (工場 / センター) in 50 bucketed names:
measured and kept.

### Notifications as Food shops (the standing rule)

The city's own list, not MHLW's opt-in filings: every notification since the
2021 law (届出年月日 2021: 1,345, then 190 to 219 a year). Through
`japan_eigyo` with 業態 as the type: **Retail 1,295 rows, 1,290 pins**
(その他の食料・飲料販売業 604, コンビニエンスストア 210, 乳類販売業 193,
百貨店・総合スーパー 131, 野菜果物販売業 89, butcher 25, rice 18, fishmonger
17, bento 8). Out: vending 433, 集団給食施設 278, no rule 156 (manufacturing
notifications), not a premises 100 (一円 and 行商), mail order 7. No closure
marker; no official count of notifications exists to measure it against.
⚠️ **The template's standing bullet** ("Food businesses that only notify
the city … are not in the list") is wrong for Amagasaki, as for Yokkaichi:
take Yokkaichi's replacement sentence if it has landed, else a proposal in
the drafts file at build.

### MHLW's file (28202), a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=28202_food_business_all.csv`:
**392,239 B, 1,277 rows** (届出 1,138, 許可 137, 届出(廃業) 1, 許可(廃業) 1),
the national schema. **137 open permits (125 restaurants) against the city's
5,813**: 105 carry a trade name in the city's list, 60 at the same (address,
trade name), 14 by number. **1,138 open notifications, 376 addressed**: 215
at a city-notification (address, trade name). The city's own lists cover
everything MHLW holds; **MHLW adds nothing** (Ichinomiya's call 126 for its
permits; its notifications are superseded by the city's). Its own point
against the block point: median **39 m**, 94.2% within 250 m (446 rows).

### Personal services: 検査確認済施設一覧, pages 1001026-1001028

| File (under `…/001/001/`) | Page | Bytes | Rows | Official (e-Stat FY2024 第10表 / 第11表) | Share |
|---|---|---|---|---|---|
| `026/riyouR80831.csv` 理容所 検査確認済施設一覧 | 1001026 | **47,411** | **341** | barbers 347 | **98.3%** |
| `027/biyouR80831.csv` 美容所 検査確認済施設一覧 | 1001027 | **153,760** | **987** | beauty salons 963 | **102.5%** |
| `028/cleaningR80831.csv` クリーニング所 検査確認済施設一覧 | 1001028 | **75,137** | **372** (368 premises) | laundries 372 (取次所 323; 無店舗 4) | **98.9%** |

(Official from `data/hakodate/raw/estat_eisei_r6_*_by_city.csv`, 兵庫県尼崎市.
Pages updated 2026-09-10, each "令和8年8月31日現在".)

- **Columns**: 施設名称 (laundry 施設名称１), 施設所在地 (施設所在地１),
  施設電話番号, **申請者名**, 開設者住所 / 開設者住所１ / 営業者住所１ (the
  operator's own address, 22, 213 and 143 rows), 開設者電話番号 / 営業者電話番号,
  検査確認番号 (repeats: a number per year), 検査確認日 (1936 to 2026), 業務種別
  (理容所, 美容所, クリーニング所 on every row), and for laundries
  **クリーニング種別１** (取次所 322, 一般クリーニング所 46, **無店舗取次店 4**).
- ⚠️ **The laundry kind**: `TYPE_COLS` takes 業務種別 (クリーニング所 on all
  372) and never sees クリーニング種別１, so the 4 無店舗取次店 (pick-up
  without a shop) would be pinned. A `source_rows` passes クリーニング種別１ as
  the type (Hiroshima's and Toyonaka's hook); measured so: **368 premises in
  the bucket**. 施設名称１ / 施設所在地１ are in the shared tuples already.
- One repeat of (address, name) in each register; **14 addresses are in both
  the barber and the beauty register** (one pin per premises and bucket keeps
  one per bucket). Standing registers, no closure marker: the page keeps "may
  include closed premises".

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28202-24.0a.zip` (182,821 B,
**12,748 block keys**), town-chōme `.../19.0b/28202-19.0b.zip` (11,179 B,
**421**). `japan.CITIES` entry at build: `"amagasaki": {"name": "尼崎市",
"pref": "28", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["28202"]}`.

| Tier, today's shared code (`WAVE2_RULES`) | Block | Town-chōme | Unplaced |
|---|---|---|---|
| Permits and registers, bucketed (6,535) | **98.9%** | 1.1% | **3 rows** |
| … Food service (3,946) / Retail (893) | 98.5% / 99.8% | 1.4 / 0.2 | 2 / 0 |
| Barbers (341) / beauty (987) / laundry (368) | 99.7 / 99.4 / 98.1% | 0.3 / 0.6 / 1.6 | 0 / 0 / 1 |
| Notifications, Retail (1,295) | **97.5%** | 2.4% | 2 rows |

**Amagasaki writes its addresses without 丁目** (`昭和通3-95` for 昭和通3丁目95):
only 2 of 5,052 fixed food addresses spell 丁目. The shared `shifted` rule
reads the first number as the chōme (4,653 rows used it); nothing new is
needed.

**The misses, read** (towns only, scratch `measure.py`): chōme tier, a number
not among the town's blocks (昭和南通4丁目 13 rows, 神田北通3丁目, 西向島町,
扇町, 御園町 2 each); unplaced, 塚口本町 written with no 丁目 where MLIT keys
only its 丁目, one address with a house number inside the town name, and
大物町3丁目 (MLIT has none): single rows, read at build.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_28_GML.zip`, N03 code 28202
(**50.7 km²**, extent W 135.369, S 34.677, E 135.460, N 34.781). Read with
`stub_test()` and an in-memory `CITIES` entry (scratch `rail_amagasaki.py`).
English names on Osaka's and Kobe's precedent (`pipeline/osaka/config.py`
splits 東海道線 into the JR Kyoto and JR Kobe Lines by the track graph; this
stretch is the JR Kobe Line).

| N02 line (operator, class) | Public name | Inside / N02 records | Stations inside |
|---|---|---|---|
| 本線 (阪神電気鉄道, 12) | Hanshin Main Line | **5 / 33** | 杭瀬, 大物, 尼崎, 尼崎センタープール前, 出屋敷 |
| 阪神なんば線 (阪神電気鉄道, 12) | Hanshin Namba Line | **2 / 12** | 大物, 尼崎 |
| 東海道線 (西日本旅客鉄道, 11) | JR Kobe Line | **2 / 59** | 尼崎, 立花 |
| 福知山線 (西日本旅客鉄道, 11) | JR Takarazuka Line | **3 / 30** | 尼崎, 塚口, 猪名寺 |
| JR東西線 (西日本旅客鉄道, 11) | JR Tōzai Line | **1 / 9** | 尼崎 |
| 神戸線 (阪急電鉄, 12) | Hankyu Kobe Line | **3 / 17** | 園田, 塚口, 武庫之荘 |
| 伊丹線 (阪急電鉄, 12) | Hankyu Itami Line | **1 / 4** | 塚口 |

- **17 station records, 12 `N02_005g` groups.** Interchanges: JR 尼崎 (006918:
  Kobe, Takarazuka and Tōzai Lines, 0 m), Hanshin 尼崎 (006981: Main and Namba,
  0 m), 大物 (006996, 25 m), Hankyu 塚口 (006820: Kobe and Itami, 32 m).
  **Two names in two groups each**: 尼崎 (JR and Hanshin) and 塚口 (JR and
  Hankyu), separate stations at least 821 m apart (no pair of groups under
  600 m). They stay apart, named with the operator where OSM's `name:en`
  does not tell them apart (Kobe's 御影 precedent, trap 1). Median
  nearest-group gap **1,181 m** (821 to 2,107): rings by the spacing rule at
  build.
- **Shinkansen**: none inside the city.
- **Cut at the line** (named by N03 municipality at build): Hanshin Main 28
  beyond (Kobe 13, Nishinomiya 7, Ashiya 2, Osaka Prefecture 6), the Namba
  Line 10 (Osaka Prefecture), JR Kobe 57 (Kobe 9, Nishinomiya 3, Ashiya 1,
  beyond Hyōgo 44), JR Takarazuka 27 (Itami 2, Takarazuka 3, Sanda 5, …), JR
  Tōzai 8 (Osaka Prefecture), Hankyu Kobe 14 (Kobe 6, Nishinomiya 2, Ashiya
  1, Osaka Prefecture 5), Hankyu Itami 3 (Itami). Hanshin's 武庫川, on the river at the city's western edge, is not
  inside the N03 line.
- **The stub test.** **The JR Tōzai Line keeps one station of 9, 尼崎**, its
  western terminus (1.28 km of track from 尼崎 to the city line), and **the
  Hankyu Itami Line one of 4, 塚口**, its junction (409 m to the line). Both
  are JR or private lines, so the standing call draws them as cut and **no
  owner question arises** (Kobe's JR Takarazuka Line, 1 of 30; Akita's Oga
  Line); each station keeps its ring through the other lines in any case.
  Hanshin Namba keeps 2: drawn cut. No urban line (subway, monorail) runs in
  the city, so the one-station urban rule does not arise.
- **The light-rail / rail test**: every line is a railway (N02 class 11 or
  12); no tram or light rail.
- **Frequency, READ 2026-10-06 from the operators' own timetables** by the
  wave-5 probe (plain GET), re-counted here from its cached pages
  (`wave5/japan_j5/pages`, scratch `tt_read.py`), weekday, every departure a
  page lists:

  | Line, station (page) | Direction | All day | Per hour 10-16 |
  |---|---|---|---|
  | Hanshin Main: 杭瀬, 大物, 出屋敷 (`hanshin.co.jp/search/<station>_u1.pdf`) | to 大阪梅田 | 83-89+ | **5.8-6.0** |
  | Hanshin Main: 尼崎 | to 大阪梅田 | 188+ | **11.8** |
  | **Hanshin Main: 尼崎センタープール前** (`poolmae_u1.pdf`) | to 大阪梅田・大阪難波 | **59+** | **4.2** |
  | JR Kobe Line: 尼崎 (`timetable.jr-odekake.net/station-timetable/2798012002`) | to 大阪 | 363 | **20.5** |
  | JR Kobe Line: 立花 (`2799012002`) | to 大阪 | 147 | **8.0** |
  | JR Takarazuka Line: 尼崎 (`2798025001`) / 塚口 (`2821025001`) | to 宝塚 / to 大阪 | 207 / 112 | **12.7 / 7.7** |
  | **JR Takarazuka Line: 猪名寺** (`2831025001`) | to 尼崎・大阪 | **80** | **4.0** |
  | Hankyu Kobe: 園田, 塚口, 武庫之荘 (`hankyu.co.jp/station/html/HK-0x_ko_1_w.html`) | to 大阪梅田 | 139-208 | **6.0** |
  | Hankyu Itami: 稲野, its trains to 塚口 (`HK-18_it_1_w.html`) | to 塚口 | 125 | **6.2** |

  **No stretch near 11 trains a day** (call 86). The Hanshin PDFs' all-day
  counts are floors ("+"): the reader skips early rows whose hour and first
  minute run together. **The JR Tōzai Line** has no page read at 尼崎; its
  through trains appear on 立花's and 塚口's pages toward 大阪 under the
  destination marks of the Tōzai and Gakkentoshi Lines (松, 四, 同, 木, 京田,
  放: about 100 a weekday between the two pages), so it is frequent (read
  through its neighbours; the marks' reading is this brief's, the build
  confirms it on JR West's 尼崎 Tōzai page). ⚠️ **The Hanshin Namba Line's own
  page** (大物 toward 大阪難波) was not read: frequency ASSERTED; the build
  reads it with gate 3. Only counts are recorded, never a timetable on the
  page.
- ⚠️ **Gate 3** at build: per-line station counts from Hanshin, JR West and
  Hankyu. **OSM `name:en`** for 12 groups (one Overpass query at build; not
  queried here). Line colours from Osaka's and Kobe's configs, checked on
  both basemaps.

## Scope

**Amagasaki City.** Hanshin runs on to Osaka and to Nishinomiya and Kobe, the
JR Kobe Line to Osaka and Kobe, the JR Takarazuka Line to Itami and Sanda,
the JR Tōzai Line into Osaka, Hankyu to Osaka, Kobe and Itami; cut at the
line.

## Licences — as stated; the read is pending

**As stated on each page** (food, barber, beauty and laundry pages alike):
「クリエイティブ・コモンズ 表示 4.0 国際 ライセンスの下に提供されています。」
(link `creativecommons.org/licenses/by/4.0/deed.ja`), and each section ends
「本セクションで公開しているデータは、クリエイティブ・コモンズ・ライセンスのもとで提供しております。…各ライセンスの利用許諾条項に則ってご利用ください。」
Each page also links the city's open-data page
(`/opendata/1000081/1023309.html`, not read here). **No read of Amagasaki's
terms is recorded in `docs/decisions_drafts/staging.md`: a licence-read
agent reads them separately; staging records its verdict and the credit
wording.** No verdict is written in this brief.

- **MHLW open data**: not used (a control only), so no MHLW credit.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **Operators' timetables**: read for counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The permit list carries 申請者名** (the operator) on every row, with no
  company marker on **3,826 of 6,394 fixed rows** (3,788 of 5,813
  restaurants), the shape of a sole trader's own name, and **代表者名** (a
  company's representative, 2,668). Step 2 reads both IN MEMORY for the name
  rule only (`OPERATOR_COLS` holds both) and never writes them. **Never
  selected**: 施設電話番号, **申請者住所** (the operator's own address, 2,668),
  申請者電話番号, 自動車登録番号, the permit number.
- **The name rule, v2, measured in memory** (answers only, never a value):
  permits **3 fixed rows withheld** (5 over all restaurant rows, vehicles
  included), **0 bare personal names**, 1 of them bucketed; notifications 6
  (0 bare, none bucketed); barbers 0, laundries 0; **beauty 1, a bare
  personal name** (withheld, shown by type).
- The registers: select 施設名称, 施設所在地 (and クリーニング種別１) only;
  申請者名 for the rule in memory; 開設者住所 / 営業者住所１ and the phones never.
- Run `check_personal_exposure.py amagasaki` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Kansai after the retag), `label_tier: "minor"`,
`"country": "Japan"`. Project to **UTM 53N (EPSG:32653)**: the N03 centroid
lies at longitude 135.411, the extent 135.369-135.460, inside the 132-138
band (computed here, never copied). OSM box from the N03 extent, rounded out:
(34.67, 135.36, 34.79, 135.47).

**Scaffold**: `scaffold_city.py --slug amagasaki --name Amagasaki
--system-name "JR West, Hanshin and Hankyu" --taxonomy japan_eigyo --lat
34.734 --lon 135.411 --region "Japan West" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), the number claimed in
`docs/session_roles.md` at build (Amagasaki is not in
`docs/staged_cities.json`).

## Owner calls

**Made (do not re-ask):** Band A (call 118); the downloads (calls 90, 106,
and MHLW's control for round 3); the standing Japanese calls above; the
city's notifications as Food shops (the standing `japan_eigyo` rule,
Yokkaichi's shape); MHLW's permits out (call 126); `mode: metro`; the minor
tier, Japan West now and Kansai after the retag; the JR Tōzai and Hankyu Itami
one-station stubs drawn as cut (standing call, JR and private lines); no
frequency floor (call 46); hostess venues, canteens, karaoke and catering
out by 業態 (`docs/category_rules.md`); the two same-named station pairs kept
apart (trap 1, Kobe's 御影).

**Open:** none for the owner. ⚠️ If `check_macro_labels.py` cannot place
Amagasaki's label beside Osaka's and Itami's, `KNOWN_STACKED` on the Itami and
Toyonaka precedent (the `japan-city` skill, accepted 2026-10-04) is a new name
there: list it for review time.

## What the build must still measure

- ⚠️ **`config.source_rows`**: the notifications' 業態 copied into the type;
  the laundry register's クリーニング種別１ passed as the type (無店舗 out).
  Expect Retail 1,295 notification rows and 368 laundries.
- `SOURCE_LINKS` for both monthly food files; `as_of` from the link title
  (2026-08-31 for `kyoka202608.csv`), never today; the registers'
  `SOURCE_AS_OF` 2026-08-31. Re-measure the old-law count on the edition
  read (174 permits ended on 2026-08-31).
- The overlap of notifications and permits at one premises (a konbini with
  both): one pin per premises and bucket, measured.
- The Hanshin Namba Line's frequency (its own page); gate 3; OSM `name:en`
  and the 尼崎 / 塚口 operator suffixes; line colours on both basemaps; the
  opening view (`map-view`); the factory share; the Economic Census control
  (expected 1.92); `check_provenance.py`; `check_scope_disclosure.py`;
  `check_macro_labels.py` with Itami and Osaka.

```brief-checks
[
  {
    "id": "amagasaki-food-page",
    "claim": "The food page offers the 2026-08 permit and notification lists under CC BY 4.0 (a failure on the file names means a new monthly edition: re-measure). ASCII anchors only: the host sends no charset, so the Japanese text does not decode here",
    "kind": "http_contains",
    "url": "https://www.city.amagasaki.hyogo.jp/op_data/1000922/1001025.html",
    "present": ["kyoka202608.csv", "todoke202608.csv", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "amagasaki-food-permits-file",
    "claim": "The 2026-08-31 permit list (1,752,694 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.amagasaki.hyogo.jp/_res/projects/default_project/_page_/001/001/025/kyoka202608.csv",
    "min_bytes": 1500000
  },
  {
    "id": "amagasaki-food-notifications-file",
    "claim": "The 2026-08-31 notification list (467,150 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.amagasaki.hyogo.jp/_res/projects/default_project/_page_/001/001/025/todoke202608.csv",
    "min_bytes": 400000
  },
  {
    "id": "amagasaki-barber-page",
    "claim": "The barber register as of 2026-08-31 (R8 08 31 in its file name), under CC BY 4.0; ASCII anchors (no charset sent)",
    "kind": "http_contains",
    "url": "https://www.city.amagasaki.hyogo.jp/op_data/1000922/1001026.html",
    "present": ["riyouR80831.csv", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "amagasaki-beauty-page",
    "claim": "The beauty register as of 2026-08-31 (R8 08 31 in its file name), under CC BY 4.0; ASCII anchors (no charset sent)",
    "kind": "http_contains",
    "url": "https://www.city.amagasaki.hyogo.jp/op_data/1000922/1001027.html",
    "present": ["biyouR80831.csv", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "amagasaki-laundry-page",
    "claim": "The laundry register as of 2026-08-31 (R8 08 31 in its file name), under CC BY 4.0; ASCII anchors (no charset sent)",
    "kind": "http_contains",
    "url": "https://www.city.amagasaki.hyogo.jp/op_data/1000922/1001028.html",
    "present": ["cleaningR80831.csv", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "amagasaki-barber-file",
    "claim": "The barber register (47,411 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.amagasaki.hyogo.jp/_res/projects/default_project/_page_/001/001/026/riyouR80831.csv",
    "min_bytes": 35000
  },
  {
    "id": "amagasaki-beauty-file",
    "claim": "The beauty register (153,760 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.amagasaki.hyogo.jp/_res/projects/default_project/_page_/001/001/027/biyouR80831.csv",
    "min_bytes": 120000
  },
  {
    "id": "amagasaki-laundry-file",
    "claim": "The laundry register (75,137 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.amagasaki.hyogo.jp/_res/projects/default_project/_page_/001/001/028/cleaningR80831.csv",
    "min_bytes": 60000
  },
  {
    "id": "amagasaki-mhlw-live",
    "claim": "MHLW's open-data file for Amagasaki (28202) answers a plain keyless GET (392,239 B on 2026-10-06; a control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=28202_food_business_all.csv",
    "min_bytes": 300000
  },
  {
    "id": "amagasaki-isj-block-live",
    "claim": "MLIT's block-level address file for Amagasaki (28202) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28202-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "amagasaki-isj-chome-live",
    "claim": "MLIT's town-chōme file for Amagasaki (28202) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/28202-19.0b.zip",
    "min_bytes": 8000
  },
  {
    "id": "amagasaki-hanshin-poolmae-timetable",
    "claim": "Hanshin's weekday timetable PDF for 尼崎センタープール前 toward 大阪梅田, the thinnest station (4.2 an hour), answers",
    "kind": "http_ok",
    "url": "https://www.hanshin.co.jp/search/poolmae_u1.pdf",
    "min_bytes": 300000
  },
  {
    "id": "amagasaki-jr-inadera-timetable",
    "claim": "JR West's station timetable for 猪名寺 (JR Takarazuka Line toward 尼崎・大阪), the thinnest JR station (4.0 an hour), lists its departures",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/station-timetable/2831025001",
    "present": ["minute-item", "猪名寺駅"]
  },
  {
    "id": "amagasaki-hankyu-tsukaguchi-timetable",
    "claim": "Hankyu's weekday timetable for 塚口 on the Kobe Line toward 大阪梅田 - the frequency source",
    "kind": "http_contains",
    "url": "https://www.hankyu.co.jp/station/html/HK-06_ko_1_w.html?no_redirect",
    "present": ["塚口駅", "大阪梅田方面"]
  },
  {
    "id": "amagasaki-projected-crs",
    "claim": "Amagasaki projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.411,
    "expect": "EPSG:32653"
  }
]
```
