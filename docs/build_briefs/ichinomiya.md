# Ichinomiya — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5: `docs/decisions_drafts/staging.md`, "Wave 5: the ranked queue and the
pre-verdicts screened"). The Step 0 downloads were approved by the owner
2026-10-06 (call 67). **Step 0 measured 2026-10-06** (staging). Into
`data/ichinomiya/raw/` (gitignored), each from its publisher's own host with
the project user-agent, each HTTP 200, under each URL's own file name as
`japan_fetch.get` saves:

- From `www.city.ichinomiya.aichi.jp` (保健衛生課 and 保健予防課): the food
  list `232033_Food_Business_All_20260331.csv` (589,280 B) and the five
  monthly files April to August 2026 (`232033_food_business_new_20260401_20260430.csv`
  … `_20260801_20260831.csv`, 41,406 B together); the barber, beauty and
  laundry lists `2025riyouitiran.csv` (28,270 B), `2025biyoushoichirann.csv`
  (86,155 B), `2025clearningitiran.csv` (30,114 B).
- From `i2fas.mhlw.go.jp`: `23203_food_business_all.csv` (369,670 B), a
  control only.
- From `nlftp.mlit.go.jp`: `isj/23203-24.0a.zip` (724,841 B) and
  `isj/23203-19.0b.zip` (11,430 B).

**1,881,166 B in all.** Nothing else was downloaded. Not fetched (not
approved): the 2026-04 to 08 monthly barber, beauty and laundry files on the
現在 page (open call 4), the PDFs (the same content), the inn, theatre and
bath lists.

**Run `python scripts/brief_check.py ichinomiya` before writing any code.**
Then the `japan-city` skill, **Fukuyama's shape** (a city's own full food
list plus the months since, `rebuilt_register`; `docs/build_briefs/fukuyama.md`)
with **Toyota's precedent** for a city list that leaves rows out by design
(Toyota's food list leaves out temporary and stall permits, 75% of official;
`docs/data_sources/japan.md`), Hamamatsu's for the registers. Coordinates:
the `address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` has no Ichinomiya
entry; its table is shared code and was not edited). Rail: MLIT N02-25 cut at
the N03 city line, measured through `pipeline/countries/japan.py` with a
scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none stops here); (2) **lines served only by limited expresses
DO count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left
out, its station kept through the other lines, and drawn cut only where no
other line serves that station (owner, 2026-10-06, calls 54 and 92); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor
for JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at
about 11 trains a day or fewer named and drawn (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from
OSM `name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Ichinomiya carries `label_tier: "minor"` and goes in the **Japan East** view,
as Toyota does (`app/cities.py`); wave 4's first city to land retags Japan
into the eight regions, Ichinomiya into **Chubu**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.
Ichinomiya's dot sits about 17 km northwest of central Nagoya: measure its
label against Nagoya's neighbours on the map at build.

**`mode`: `metro`** (the owner's rule of 2026-10-02, applied as for Kurume and
Maebashi): JR is not the largest network inside the city (2 station groups
against Meitetsu's 17), and no subway or tram is drawn, so the mode follows
the backbone: Meitetsu's 名古屋本線 and 尾西線 are railways (N02 class 12).

---

## The one-line summary

**All three buckets from the city's own CSVs (CC BY 4.0 as stated; the
licence read is done, staging records it).** The food list of permits in
term on 2026-03-31 holds **2,815 rows, 2,164 restaurants (飲食店営業 2,161 +
喫茶店営業 3), 65.7% of e-Stat's 3,292 in force**: the city leaves out
vending, vehicle, stall and temporary permits, rows "containing personal
information" and operators who asked not to be published. MHLW's small file
is the only sample of what that drops: **47 of its 129 permits (36%; 39 of 99
restaurants) are in no city file, and 22 of the 27 with no company marker
are among them.** With the months since, **2,898 permits, 2,228 restaurants
(67.7%)** if the full list is kept whole (recommended, open call 1), or
2,659 / 2,051 (62.3%) if permits past their expiry with no renewal on record
are dropped. Barbers 300, beauty salons 819, laundries 242 as of
2026-03-31: **100%, 103.5% and 99.6% of official**. Block join **93.1%**
(food), 81-83% (registers; 86-93% with a short-大字 rule the build adds).
**Rail: 19 station groups** (Meitetsu 17, JR 2), Meitetsu read from its own
timetable: nothing near 11 trains a day.

---

## Business leg — the city's 保健所 lists

Host `https://www.city.ichinomiya.aichi.jp` (the city's own CMS; no catalogue
API). Every file is a plain GET under
`/_res/projects/default_project/_page_/001/`; the PDFs beside them carry the
same content (「ファイル形式が異なりますが同じ内容のものです」).

### Food: 食品営業許可台帳（最新）, page ID 1040636

Page `https://www.city.ichinomiya.aichi.jp/hokenjo/hoken-eisei/1044314/1039899/1040636.html`
(更新日 2026-09-15; 保健衛生課).

| File (under `…/001/040/636/`) | Bytes | Rows | What it is |
|---|---|---|---|
| `232033_Food_Business_All_20260331.csv` 食品営業許可台帳（令和8年3月31日時点） | **589,280** | **2,815** | permits in term on 2026-03-31; yearly (年度末時点) |
| `232033_food_business_new_20260401_20260430.csv` … `_20260801_20260831.csv` | 7,351 · 6,026 · 12,672 · 5,969 · 9,388 | 34 · 30 · 55 · 28 · 46 (193) | each month's permits, 「新規又は継続で取得した施設の月ごとの一覧」; posted about the 15th of the next month |

- **Encoding Shift-JIS (cp932), CRLF**, header on line 1, no empty lines;
  `japan_register.city_rows` reads all six as they stand. Dates 和暦
  `R14.4.30`; `wareki_date` reads every 許可開始日 and 許可満了日 (0
  unreadable); 21 初回許可開始日 do not read (no step needs them).
- **One schema in all six files**: **営業所名称**, 営業所名称_カナ, **営業の種類**,
  **業態**, **営業所所在地**, 営業所方書, 営業所電話番号, **営業者名**,
  **営業者所在地**, 営業者方書, 営業者電話番号, 代表者肩書, **代表者名**,
  **許可番号**, 初回許可開始日, **許可開始日**, **許可満了日**. Against the
  shared tuples: 営業所所在地 is in `ADDR_COLS`, 営業所名称 in `NAME_COLS`,
  営業の種類 in `TYPE_COLS`, 業態 in `FORM_COLS`, 営業者名 and 代表者名 in
  `OPERATOR_COLS`; **the grant date is 許可開始日**, so `rebuilt_register`
  takes `granted_col="許可開始日"` (its `end_col` default 許可満了日 fits).
  No shared-code change is needed for the food list.
- **Types (full list)**: 飲食店営業 2,161, 菓子製造業 315, 食肉販売業 92,
  魚介類販売業 78, そうざい製造業 65, 食肉処理業 18, 麺類製造業 15, … 喫茶店営業
  3 (old law). **業態** among restaurants: 一般食堂・レストラン・料理店 930,
  その他 707, 一般食堂・レストラン等 223, カフェー・バー・キャバレー 111,
  集団給食施設 43, 仕出し屋・弁当屋 43, 簡易な営業 30, …
- **What the page leaves out** (「掲載の対象外」): 「自動販売機、自動車、露店、臨時及び短期による営業許可」,
  「個人情報を含むもの」 and 「営業者が公開を希望しないもの」; and
  「その後廃止した施設が含まれている場合があります」. So **no vehicle, stall
  or vending row is in the file** (no address reads 一円 or 市内; 0 rows
  flagged mobile), and closed premises may remain.
- The page also notes that a premises operating before 2021-06-01 shows a
  初回許可開始日 after that date once it re-applied under the revised law.

### What the personal-information exclusion drops (the owner's question)

- **The file is not stripped of sole traders.** 営業者名 is filled on all
  2,815 rows: 1,445 carry a company or cooperative marker (and a 代表者名),
  **1,370 do not** (1,366 with no 代表者名), the shape of a sole trader's own
  name. What is blanked for them is the operator's own address and phone:
  営業者所在地 is filled on 1,449 rows, only 4 of them without a company
  marker. So the exclusion removes fields from every sole trader's row and,
  by the coverage below, whole rows for some.
- **Coverage against e-Stat** (衛生行政報告例 FY2024, `japan_official.estat()`;
  愛知県一宮市, 飲食店営業 in force 2025-03-31: **3,292**, old law 999, revised
  2,293): the full list's **2,164 restaurants are 65.7%**. The stock is
  stable (3,191, 3,245, 3,247, 3,292 at FY2021 to FY2024), so the gap is the
  exclusions, not a shrinking city. e-Stat's count includes the vehicles,
  stalls and temporary permits the page leaves out by design; the split
  between those and the personal-information and opt-out rows cannot be
  measured from the city's side.
- **MHLW's sample** (129 permits filed through the national system, mostly
  chains; below): **82 are in a city file** (78 by permit number, 4 by
  address and trade name), **47 are in none** (36%; 39 of 99 restaurants).
  Of the 47: 5 carry MHLW's vehicle or stall condition (left out by design),
  25 a company marker and a 法人番号, 22 neither; only 29 give an address. Of
  the 82 found, 77 are companies. **So the exclusion falls hardest on sole
  traders (22 of 27 absent) but also takes about a quarter of companies (25
  of 102)**, consistent with the opt-out clause. The sample is small and
  chain-heavy; read it as the direction, not the rate.
- **New permits**: the five monthly files carry 193 rows in five months, about
  460 a year, against e-Stat's **864** revised-law permits granted in FY2024:
  the months show about half of what is granted.

### The months against the March list (merge, duplicates, closures)

- **The full list is clean of repeats by number**: 2,813 distinct 許可番号 of
  2,815; 43 rows repeat an (address, trade name, type) under another number
  (one pin per premises takes them); 2,404 distinct (address, trade name).
- **It holds only permits in term on its date**: no 許可満了日 before
  2026-03-31 (2026: 445 … 2032: 73). 603 rows (431 restaurants) began before
  2021-06-01, old-law permits; 275 permits (207 restaurants) end before
  2026-08-31.
- **No monthly permit number is in the full list** (0 of 193): every monthly
  row is a new number. 182 of 193 carry 初回許可開始日 equal to 許可開始日 (new,
  or an old-law premises re-permitted under the revised law), 11 an earlier
  first permit (continuations). **67 monthly rows sit at a premises (address,
  trade name, type) already in the full list** whose permit ends within two
  months of the new start: renewals under a new number. A plain union counts
  2,898 keys.
- **Renewals are mostly missing from the months.** Of the 275 full-list
  permits ending before 2026-08-31, **only 35 reappear** by premises key (18
  more share an address, 39 a trade name, with a monthly row); 237 of the
  240 that do not are old-law permits. e-Stat says they are not closing at
  that rate: old-law restaurants fell by about 550 a year while revised-law
  ones rose by as many and the total held. So a permit past its expiry with
  no monthly row is, in most cases, renewed and unpublished, not closed (6 of
  the 240 have an MHLW permit at the same address and name).
- **Closures are not marked** in any file, and the city publishes no closure
  list; MHLW's 129 permits are too few to be a closure control (Fukuyama's
  method needs MHLW to hold every revised-law permit; here it holds about 5%).
- **The two ways to merge** (`rebuilt_register`, latest end per address,
  trade name and type; `granted_col="許可開始日"`):

  | Merge | Permits | Restaurants | Share of 3,292 |
  |---|---|---|---|
  | Full list alone, 2026-03-31 | 2,815 | **2,164** (incl. 喫茶店 3) | 65.7% |
  | **Full list kept whole + the months (`as_of` 2026-03-31)** | **2,898** | **2,228** | **67.7%** |
  | Rebuilt, in term on 2026-08-31 | 2,659 | 2,051 | 62.3% |
  | Full list alone, in term on 2026-08-31 | 2,540 | 1,956 | 59.4% |

  Open call 1 chooses. Either way the build reads the five months and pins
  the page's date to what it read, never today.

### Counts through `japan_eigyo` (full list kept whole + months, fixed premises)

**Food service 2,028, Retail 570** (2,598 storefront rows). Retail here is
菓子製造業 (about 300), 食肉販売業, 魚介類販売業 and そうざい: **no konbini or
supermarket**, since their notifications are not in the city's list (Toyota's
"Retail thin"). Left out of the buckets (rebuilt to 08-31, for scale):
hostess venues by 業態 114, 仕出し 40, institutional catering 20, inside
accommodation 8, and 88 manufacturing types with no rule (食肉処理業 17,
麺類製造業 16, アイスクリーム類製造業 8, 食品の小分け業 8, …), as in every
built city.

**Economic Census control** (`scripts/japan_census_control.py` at build): the
2021 census counts **1,434** 飲食店 establishments in 23203
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 1,960 distinct placed
Food-service premises is **1.37 per establishment** (1.26 on the 08-31
rebuild), **below the built cities' 1.56-1.92**, as expected for a list that
holds two restaurants in three. Kurume's 1.37 is the precedent for reporting
it with that reason.

### MHLW's file (23203), a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=23203_food_business_all.csv`:
**369,670 B, 1,124 rows** (届出 992, 許可 129, 届出(廃業) 3), UTF-8 with BOM,
the national schema (営業施設名称、屋号又は商号, 営業の種類, 業態,
営業施設所在地, 方書, 緯度 / 経度, 法人名, 法人番号, 法人住所, phones, permit
dates, 廃業年月日, 申請区分, 許可条件). MHLW's cover is **0.03** (99 open
restaurant permits of 3,292): the city files through its own system, and only
operators who file nationally appear. Its permit numbers share the city's
form (`R一宮保衛第NNNN-NNN号`), so the 78 matches by number are exact.

- **Its own coordinates against the block point**: median **26 m**, 95.3%
  within 250 m (430 rows; 10 over 1 km). Too few permits to be a fallback of
  any size.
- **992 open notifications, 471 addressed** (ドラッグストア 54, 無人販売用冷凍庫
  52, 置き菓子 34, スーパーマーケット 26, …): the partial Food-shops layer of
  Matsuyama's and Fukuyama's precedent, if the owner wants it (open call 2b).

### Personal services: 生活衛生関係営業確認（許可）台帳（2025年度）, page ID 1075449

Page `https://www.city.ichinomiya.aichi.jp/hokenjo/hokenyobou/1044311/1039814/1075449.html`
(更新日 2026-07-14; 保健予防課).

| File (under `…/001/075/449/`) | Bytes | Rows | Official (e-Stat FY2024 第10表 / 第11表) | Share |
|---|---|---|---|---|
| `2025riyouitiran.csv` 理容所一覧（2026年3月31日時点） | **28,270** | **300** | barbers 300 | **100%** |
| `2025biyoushoichirann.csv` 美容所一覧（2026年3月31日時点） | **86,155** | **819** | beauty salons 791 | **103.5%** |
| `2025clearningitiran.csv` クリーニング所一覧（2026年3月31日時点） | **30,114** | **242** | laundries 243 (取次所 180) | **99.6%** |

(Official from `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
`…_cleaning_by_city.csv`, 愛知県一宮市.)

- **cp932, CRLF.** Columns: 確認番号, 確認年月日, **施設名称**, **施設住所**,
  **申請者氏名**, **代表者氏名**; the barber file adds **廃業日** (empty on all
  300). 確認年月日 is 和暦 from Shōwa (`S53.4.1`) on; `wareki_date` reads no
  Shōwa date (151, 188 and 83 rows), and no step needs one.
- **The personal-information clause takes nothing measurable here**: all
  three are at official. The exclusion again blanks fields, not rows (no
  operator address or phone column at all).
- **One file per kind, no type column**: `TYPE_COLS` reads nothing, so the
  build's config names the kind per file (`source_rows` or `SOURCE_KIND`, as
  Hamamatsu's registers). The laundry list does not split 取次所 from 一般 (one
  name carries 取次; e-Stat counts 180 取次所 of 243): all are premises. 施設住所
  is in `ADDR_COLS`, 施設名称 in `NAME_COLS`, 申請者氏名 and 代表者氏名 in
  `OPERATOR_COLS`.
- **Repeats**: beauty 1 (address, name) repeat; 6 premises are both a barber
  and a beauty salon (one pin per premises and bucket keeps one per bucket).
  **5 rows are addressed outside the city** (beauty: 名古屋市 2, みよし市 1;
  laundry: 豊明市 1; one more beauty row): drop any row whose address is not
  in 一宮市.
- **Standing registers, closed premises may remain** (「既に廃止している施設が含まれている場合があります」).
  The page posts each month's NEW confirmations only when there are some;
  the 2026 months sit on the 現在 page (`…/1040689.html`, open call 4).

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/23203-24.0a.zip` (724,841 B,
**156,381 block keys** with the 小字 aliases), town-chōme
`.../19.0b/23203-19.0b.zip` (11,430 B, **420**). `japan.CITIES` entry at
build: `"ichinomiya": {"name": "一宮市", "pref": "23", "epsg": 32653, "n02":
"25", "rules": WAVE2_RULES, "wardless": True, "wards": ["23203"]}`.

| Tier, today's shared code | Block | Town-chōme / 大字 | Unplaced | With the short-大字 rule (block) |
|---|---|---|---|---|
| Food, rebuilt to 08-31, fixed premises in a bucket (2,389) | **93.1%** | 3.7% | 3.1% | **94.8%** |
| … Food service (1,870) / Retail (519) | 93.5% / 91.7% | 3.3 / 5.4 | 3.2 / 2.9 | |
| Food, full list kept whole + months (2,598) | 93.0% | 3.8% | 3.2% | |
| Barbers (300) | **82.3%** | 1.3% | 16.3% | **93.0%** |
| Beauty salons (819) | **82.9%** | 4.2% | 12.9% | **90.1%** |
| Laundries (242) | **81.0%** | 5.8% | 13.2% | **86.0%** |
| MHLW's addressed rows (573) | 80.5% | 8.0% | 11.5% | |

**The misses, read** (towns only, by `analyse2.py` and `joinfix.py` in the
scratchpad):
- **The lists drop the 字 that MLIT keeps**: `起東茜屋…` where MLIT keys
  `起字東茜屋`, `三条郷東藤…` for `3条字郷東藤`, and the same after 奥町, 開明,
  浅野, 丹羽, 明地. `known_town` tries only prefixes of 3 or more characters,
  so these 1- and 2-character 大字 (起, 三条, 奥町, 開明 …, the 尾西 side of the
  2005 merger) never reach the 小字 key. A rule that tries `大字 + 字 + rest`
  for any known 大字 (scratch test: the longest MLIT 大字 that prefixes the
  town, then that 小字 in the block file) recovers the figures in the last
  column.
- **木曽川町's 通り towns**: the lists write `木曽川町黒田八ノ通り` (19 food rows
  among the unplaced, 一ノ通り 14, 二ノ通り 9 …) where MLIT writes
  `木曽川町黒田字八の通り`: the same 字 rule with ノ folded to の takes them.
- What stays unplaced after both is small (food 7 rows, barbers 12, beauty
  30, laundries 17), plus a `town-only` remainder whose 小字 exists but not
  the number (it takes the 小字's centroid, or stays at the 大字's).
- Both rules are **shared code**: follow each with the Minato control
  (`screen_japan_join.py minato` 98.0 / 0.2 / 1.8) and every city screen, so
  no built city's tiers move.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_23_GML.zip`, N03 code 23203
(**113.8 km²**, extent W 136.705, S 35.250, E 136.877, N 35.370). Read with
`stub_test()`'s method and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 尾西線 (名古屋鉄道, 12) | Meitetsu Bisai Line | **10 / 22** | 名鉄一宮, 西一宮, 開明, 奥町, 玉野, 玉ノ井; 苅安賀, 観音寺, 二子, 萩原 |
| 名古屋本線 (名古屋鉄道, 12) | Meitetsu Nagoya Main Line | **8 / 60** | 島氏永, 妙興寺, 名鉄一宮, 今伊勢, 石刀, 新木曽川, 黒田, 木曽川堤 |
| 東海道線 (東海旅客鉄道, 11) | JR Tōkaidō Line | **2 / 89** | 尾張一宮, 木曽川 |

- **20 station records, 19 N02_005g groups**: 名鉄一宮 is one group for both
  Meitetsu lines (spread 0 m). **The master list row's "17 N02 station
  groups" counts Meitetsu's groups only**; with JR's 2 the city has 19, as
  `docs/coverage_sweep/japan_universe_mhlw.csv` says. No name in two groups.
- **Close pairs** (trap 1: MLIT keeps them apart, and so does step 1): **名鉄一宮
  / 尾張一宮 38 m** (Meitetsu and JR, one station building, two groups, two
  rings almost on one spot) and 黒田 / 木曽川 406 m. **Median nearest-station
  gap 935 m** (38 to 1,802): standard rings by the spacing rule.
- **Shinkansen**: none stops in the city (the Tōkaidō Shinkansen passes
  through without a station).
- **Cut at the line** (named by N03 municipality at build): the Main Line 52
  beyond (名古屋市 15, 岡崎市 9, 清須市 6, 豊川市 6, Gifu Prefecture 5, 稲沢市 3,
  …), the Bisai Line 12 (稲沢市 5, 愛西市 4, 弥富市 2, 津島市 1), the Tōkaidō
  Line 87 (other prefectures 54, 名古屋市 9, …).
- **The light-rail/rail test**: all three are heavy rail (N02 class 12,
  Meitetsu's railways; class 11, JR conventional). No tram or light rail.
- **The stub test passes.** No urban line runs here. The Tōkaidō Line's 2 of
  89 is a main line cut at the line (Kurume's Kagoshima Line keeps 2), not a
  stub; the Bisai Line's 玉ノ井 end (玉野 241 m from the city line, 玉ノ井 737
  m) is the line's own terminus inside the city, not a cut.
- **Frequency, read 2026-10-06 from Meitetsu's own timetable** by plain GET
  with the project user-agent (`trainbus.meitetsu.co.jp`,
  `meitetsu-transfer/pc/diagram/TrainDiagram?startId=00004170&linkId=<line>&direction=<up|down>`,
  名鉄一宮 node 00004170, weekday Wednesday 2026-10-07; the probe read the
  same pages):

  | At 名鉄一宮 (line, direction) | Weekday departures | Per hour 07-19 |
  |---|---|---|
  | Bisai Line, to 玉ノ井 (linkId 00000880 down) | **38**, all 普通 | 2 (3 at 07) |
  | Bisai Line, to 森上・津島 (00000880 up) | 69, all 普通 | 3-4 |
  | Main Line, to 名鉄岐阜 (00000885 down) | 150, of which **65 普通** | 8-9 (普通 4) |
  | Main Line, to 名鉄名古屋 (00000885 up) | 203, of which **66 普通** | 10-14 |

  A 10:24 普通 to 名鉄岐阜 stops at 島氏永, 妙興寺, 名鉄一宮, 今伊勢, 石刀,
  新木曽川, 黒田 and 木曽川堤 (its route page), so every Main Line station in
  the city has the locals' 4 an hour. **The thinnest stretch is the Bisai
  Line's 玉ノ井 branch at 38 trains a day: nothing here is near 11 a day.**
  JR's 尾張一宮 and 木曽川 on the Tōkaidō Line: **ASSERTED** frequent (a main
  line with local and rapid services; JR Central's timetable was not read).
  Only counts are recorded, never a timetable on the page.
- ⚠️ **Gate 3** at build: Meitetsu's station counts (Main Line NH01-NH60, 60;
  Bisai Line 22) and JR Central's for the Tōkaidō Line inside the city (2).
  **OSM `name:en`** for 19 groups (one Overpass query at build, in the box
  below; not queried here). Line colours from Toyota's Meitetsu precedent,
  on both basemaps.

## Scope

**Ichinomiya City.** The Main Line runs on to Nagoya and Gifu, the Bisai Line
to 津島 and 弥富, the Tōkaidō Line to Nagoya and Gifu Prefecture; cut at the
line.

## Licences — read 2026-10-06 (`licence-read`, recorded by staging)

**As stated on each dataset page**: every CSV under オープンデータ carries 「この
作品 は クリエイティブ・コモンズ 表示 4.0 国際 ライセンスの下に提供されています。」
(link `creativecommons.org/licenses/by/4.0/`), and the section ends
「本セクションで公開しているデータは、クリエイティブ・コモンズ・ライセンスのもとで提供しております。」
The full read ran separately on 2026-10-06 and is done; **staging records its
verdict and conditions** (the read also covers the city's open-data 利用規約,
`https://www.city.ichinomiya.aichi.jp/opendata/1010817/1010820.html`, which
the catalogue entries link, and its prescribed credit for a modified work,
clause 3(2)(イ), in the city's spacing 「表示4.0 国際」, the laundry dataset
titled クリーニング営業確認台帳). Take the credit wording from staging's
record, not from here; no verdict is written in this brief.

- **MHLW open data** (a control; if any of open call 2 is taken): PDL 1.0 as
  recorded in `docs/data_sources/japan.md`, its 出典 line and who processed
  it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **Meitetsu's timetable**: read for counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The food lists carry the operator block**: **営業者名** (a sole trader's
  own name on about 1,370 of 2,815 full-list rows by the absence of a company
  or cooperative marker; 85 of 193 monthly rows), **代表者名**, 代表者肩書,
  **営業者所在地** / 営業者方書 / 営業者電話番号 (the operator's own address and
  phone, filled almost only for companies) and 営業所電話番号. Step 2 never
  reads any of them into an output; 営業者名 and 代表者名 are read IN MEMORY
  for the name rule only (both already in `OPERATOR_COLS`).
- **The registers carry 申請者氏名 and 代表者氏名**: no company marker on 279
  of 300 barbers, 642 of 819 beauty salons, 82 of 242 laundries. Select
  施設名称 and 施設住所 only.
- **The name rule, version 2, measured in memory** (answers only, never a
  value): food **0** rows whose trade name is the operator's own name (full
  list, months and the rebuilt register), **0 bare personal names**; barbers
  0; **beauty salons 1** (trade name equals the operator's name; 0 bare);
  laundries 0. No value was printed or stored.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected.
- Run `check_personal_exposure.py ichinomiya` (`japan=True`) after step 2:
  the rows that matter are the sole traders' trade names; it must print 0.
  Record the verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Chubu after the retag), `"country": "Japan"`,
`label_tier: "minor"`. Project to **UTM 53N (EPSG:32653)**: the N03 centroid
lies at longitude 136.793, the extent 136.705 to 136.877, all inside the
132-138 band (computed here, never copied). OSM box from the N03 extent,
rounded out: (35.24, 136.70, 35.38, 136.88).

**Scaffold**: `scaffold_city.py --slug ichinomiya --name Ichinomiya
--system-name "Meitetsu and JR Central" --taxonomy japan_eigyo --lat 35.309
--lon 136.793 --region "Japan East" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), with the page number claimed in
`docs/session_roles.md` at build, not here (Ichinomiya is not in
`docs/staged_cities.json`).

## Owner calls

**Made (do not re-ask):** Band A (owner, 2026-10-06); the Step 0 downloads
(call 67); the standing Japanese calls above; `mode: metro`; the minor tier
and Japan East (Chubu after the retag); no frequency floor (call 46); the
Tōkaidō Line drawn as cut (standing call, not a stub).

**Open, each with a recommendation:**

1. **How the months merge with the March list.** (a) **Keep the full list
   whole and add the months** (`rebuilt_register` with `as_of` 2026-03-31:
   every March row stays, a monthly row replaces the same premises' older
   permit or adds a new one): **2,228 restaurants, 67.7%**. (b) Fukuyama's
   method, kept while in term on 2026-08-31: 2,051, 62.3%.
   *Recommend (a)*: 240 of the 275 permits ending before August have no
   monthly row, 237 of them old-law, while e-Stat shows the old-law stock
   converting into revised-law permits one for one; the months publish about
   half of what is granted, so (b) would drop about 180 live restaurants as
   if closed. Tradeoff: the real closures among them stay on the map (the
   upper bound Kyoto's page discloses; the city's own note says closed
   premises may remain), and the page's date reads "permits in term on
   2026-03-31, with new permits to 2026-08-31", not one date.
2. **MHLW beside the city's list** (Fukuyama's three, re-weighed for a
   city that withholds rows on purpose). (a) **Its 47 permits in no city
   file** (39 restaurants, 29 addressed): *recommend no*. They are, by the
   sample above, largely the rows the city leaves out for personal
   information or at the operator's request; adding them from another
   publisher would undo the city's own judgement for at most about 25
   placeable restaurants. (b) **Its 992 notifications as a partial, opt-in
   Food-shops layer** (471 addressed; drugstores, supermarkets, freezer
   vending): *recommend yes, on Matsuyama's and Fukuyama's precedent*,
   disclosed as partial; the tradeoff is a bucket the page must call partial
   and MHLW's credit on the notice. (c) **Its own point** where the block
   join misses, by permit number: *recommend yes* for consistency, though
   it moves almost nothing (78 permits match).
3. **The page's coverage sentence** (a proposal at review time; no template
   covers a list the publisher thins on purpose). *Recommend* Toyota's
   approach with the reason named: the city's list leaves out vehicle,
   stall, vending and temporary permits, rows containing personal
   information and operators who asked not to be listed, so it holds about
   two restaurants in three of the official count. Drafted in the drafts
   file at build, flagged at review time.
4. **The registers' 2026 months** (the 現在 page `…/040/689/`: beauty
   2026-04 to 08, laundry 2026-04; five CSVs of 205 B to 10.1 KB and one of
   542 B; same publisher, same licence statement): not approved, not
   fetched. *Recommend approving them at build* so the registers reach
   2026-08-31 like the food months (Fukuyama's registers carry that date);
   the tradeoff is a few dozen salons for one more approval. Without them
   the registers' date is 2026-03-31 (`SOURCE_AS_OF` per source).

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): the short-大字 字 rule and ノ/の folding in `join_city` (above);
  the registers' kind per file (`source_rows` or `SOURCE_KIND`); drop rows
  addressed outside 一宮市.
- `rebuilt_register(..., granted_col="許可開始日")`, the `as_of` open call 1
  decides, pinned, never today.
- The 67 renewals and 43 same-premises repeats: one pin per premises.
- Gate 3 (Meitetsu, JR Central), OSM `name:en`, line colours on both
  basemaps, the opening view (`map-view`), the factory share (菓子 and そうざい
  in Retail), the Economic Census control (estimated 1.37),
  `check_personal_exposure.py`, `check_provenance.py`,
  `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "ichinomiya-food-page",
    "claim": "The food page offers the 2026-03-31 full list and all five 2026 monthly CSVs and links CC BY 4.0. ASCII strings only: the server sends no charset, so the check reads the page as Latin-1 and cannot match Japanese text; the exclusion sentences (自動販売機、自動車、露店、臨時及び短期による営業許可 / 個人情報を含むもの / 営業者が公開を希望しないもの) and the closed-premises note were read by curl 2026-10-06; re-read them by eye at build",
    "kind": "http_contains",
    "url": "https://www.city.ichinomiya.aichi.jp/hokenjo/hoken-eisei/1044314/1039899/1040636.html",
    "present": ["232033_Food_Business_All_20260331.csv", "232033_food_business_new_20260401_20260430.csv", "232033_food_business_new_20260501_20260531.csv", "232033_food_business_new_20260601_20260630.csv", "232033_food_business_new_20260701_20260731.csv", "232033_food_business_new_20260801_20260831.csv", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "ichinomiya-env-page",
    "claim": "The 2025 environmental-hygiene page offers the three 2026-03-31 lists and links CC BY 4.0. ASCII strings only (no charset sent; see the food check): its 個人情報を含むもの exclusion and closed-premises note were read by curl 2026-10-06; re-read them by eye at build",
    "kind": "http_contains",
    "url": "https://www.city.ichinomiya.aichi.jp/hokenjo/hokenyobou/1044311/1039814/1075449.html",
    "present": ["2025riyouitiran.csv", "2025biyoushoichirann.csv", "2025clearningitiran.csv", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "ichinomiya-env-2026-months",
    "claim": "The current environmental-hygiene page carries the 2026 monthly beauty and laundry files (open call 4, not fetched)",
    "kind": "http_contains",
    "url": "https://www.city.ichinomiya.aichi.jp/hokenjo/hokenyobou/1044311/1039814/1040689.html",
    "present": ["biyou_20260831.csv", "clerning_20260430.csv"]
  },
  {
    "id": "ichinomiya-food-full-list-live",
    "claim": "The full food list (permits in term on 2026-03-31, 589,280 B, 2,815 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.ichinomiya.aichi.jp/_res/projects/default_project/_page_/001/040/636/232033_Food_Business_All_20260331.csv",
    "min_bytes": 550000
  },
  {
    "id": "ichinomiya-food-aug-live",
    "claim": "The August 2026 monthly food file (9,388 B, 46 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.ichinomiya.aichi.jp/_res/projects/default_project/_page_/001/040/636/232033_food_business_new_20260801_20260831.csv",
    "min_bytes": 8000
  },
  {
    "id": "ichinomiya-barber-live",
    "claim": "The barber list as of 2026-03-31 (28,270 B, 300 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.ichinomiya.aichi.jp/_res/projects/default_project/_page_/001/075/449/2025riyouitiran.csv",
    "min_bytes": 25000
  },
  {
    "id": "ichinomiya-beauty-live",
    "claim": "The beauty-salon list as of 2026-03-31 (86,155 B, 819 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.ichinomiya.aichi.jp/_res/projects/default_project/_page_/001/075/449/2025biyoushoichirann.csv",
    "min_bytes": 80000
  },
  {
    "id": "ichinomiya-laundry-live",
    "claim": "The laundry list as of 2026-03-31 (30,114 B, 242 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.ichinomiya.aichi.jp/_res/projects/default_project/_page_/001/075/449/2025clearningitiran.csv",
    "min_bytes": 27000
  },
  {
    "id": "ichinomiya-opendata-terms",
    "claim": "The city's open-data terms page, which the licence read covers, answers",
    "kind": "http_ok",
    "url": "https://www.city.ichinomiya.aichi.jp/opendata/1010817/1010820.html",
    "min_bytes": 5000
  },
  {
    "id": "ichinomiya-mhlw-live",
    "claim": "MHLW's open-data file for Ichinomiya (23203), the control, answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=23203_food_business_all.csv",
    "min_bytes": 300000
  },
  {
    "id": "ichinomiya-isj-block-live",
    "claim": "MLIT's block-level address file for Ichinomiya (23203) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/23203-24.0a.zip",
    "min_bytes": 500000
  },
  {
    "id": "ichinomiya-isj-chome-live",
    "claim": "MLIT's town-chōme file for Ichinomiya (23203) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/23203-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "ichinomiya-meitetsu-bisai-timetable",
    "claim": "Meitetsu's timetable for 名鉄一宮 lists the Bisai Line toward 玉ノ井 - the thinnest stretch's frequency source",
    "kind": "http_contains",
    "url": "https://trainbus.meitetsu.co.jp/meitetsu-transfer/pc/diagram/TrainDiagram?startId=00004170&linkId=00000880&direction=down",
    "present": ["尾西線", "玉ノ井ゆき"]
  },
  {
    "id": "ichinomiya-meitetsu-main-timetable",
    "claim": "Meitetsu's timetable for 名鉄一宮 lists the Nagoya Main Line toward 名鉄岐阜",
    "kind": "http_contains",
    "url": "https://trainbus.meitetsu.co.jp/meitetsu-transfer/pc/diagram/TrainDiagram?startId=00004170&linkId=00000885&direction=down",
    "present": ["名古屋本線", "名鉄岐阜ゆき"]
  },
  {
    "id": "ichinomiya-projected-crs",
    "claim": "Ichinomiya projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 136.793,
    "expect": "EPSG:32653"
  }
]
```
