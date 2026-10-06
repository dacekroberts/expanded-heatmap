# Yamagata — build brief

**Band B, food only (Hiroshima's shape), owner-approved 2026-10-06** (a
Japanese pre-verdict converted, call 137: `docs/decisions_drafts/staging.md`,
"Wave 5, second half"; **the city's partial barber, beauty and laundry lists
stay out**, call 138). The Step 0 downloads were approved by the owner
2026-10-06 (call 141). **Step 0 measured 2026-10-06** (staging). Into
`data/yamagata/raw/` (gitignored), each from its publisher's own host with
the project user-agent, each HTTP 200, under each URL's own file name as
`japan_fetch.get` saves:

- From `www.city.yamagata-yamagata.lg.jp` (健康医療部 生活衛生課): the food list
  `062014_syokuhin_list_20260831.csv` (**480,181 B**, Last-Modified
  2026-09-08).
- From `i2fas.mhlw.go.jp`: `06201_food_business_all.csv` (1,963,932 B), the
  control (and, on the 2026-10-06 precedents, the notifications layer and
  the fallback points).
- From `nlftp.mlit.go.jp`: `isj/06201-24.0a.zip` (194,478 B) and
  `isj/06201-19.0b.zip` (13,327 B).

**2,651,918 B in all.** Nothing else was downloaded. Not fetched (not
approved, not needed): the city's own-format workbook of every open permit
and notification at 2026-06-30 (565.9 KB, it carries operator names), its
monthly workbooks and PDFs, and the barber, beauty and laundry lists (call
138). JR East's station timetable index for 山形 was read by plain GET; the
weekday pages were counted from the copies staging's probe saved.

**Run `python scripts/brief_check.py yamagata` before writing any code.**
Then the `japan-city` skill, **Hiroshima's shape** for a food-only page
(`docs/build_briefs/hiroshima.md`: Food service and Food shops, no personal
services) on **one complete city list** republished monthly (Aomori's
layout, `docs/build_briefs/aomori.md`), with MHLW's notifications as a
partial Food-shops layer and MHLW's point where the join misses (the
2026-10-06 precedents, calls 127b and 127c). Coordinates: the `address-join`
skill, measured with `pipeline/countries/japan_register.py` from scratch
scripts only (`scripts/screen_japan_join.py` has no Yamagata entry; its table
is shared code and was not edited). Rail: MLIT N02-25 cut at the N03 city
line, read through `pipeline/countries/japan.py` with a scratch `CITIES`
entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; the Yamagata Shinkansen's つばさ, through trains on the Ōu Line
tracks, are left out of the counts; N02 files no separate Shinkansen station
in the city); (2) **lines served only by limited expresses DO count**
(2026-09-28); (3) **the city line only**: only stations inside the city get
rings, JR and the private lines are cut at the line, **a one-station stub
stays as cut** (2026-09-27); an URBAN line cut to ONE station is left out
(owner, 2026-10-06, calls 54 and 92; none here); (4) **菓子製造業 and
そうざい製造業 count, in Retail**, the factory share measured and kept
(2026-09-24, 2026-09-27); (5) **the name rule**, version 2 (2026-10-06): a
bare personal name is withheld whatever the operator column holds, and
MHLW's 法人名 is an operator column (2026-10-05); (6) **no page says
"currently operating"**. Also: no frequency floor for JR or private lines in
Japan (owner, 2026-10-06, call 46), any stretch at about 11 trains a day or
fewer drawn and named (call 86; none here); fault-based cost clauses accepted
for all of Japan (2026-09-24); English station names from OSM `name:en`;
every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04); **県内一円 rows
are not premises** (Kobe's trap 6, 2026-09-27). The precedents set
2026-10-06 apply without re-asking: a city's full list kept whole, MHLW's
extra permits out (Ichinomiya, calls 126 and 128); MHLW's notifications as a
partial Food-shops layer where they have hundreds of addressed rows (127b);
MHLW's own point where the block join misses (127c).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Yamagata
carries `label_tier: "minor"` and goes in the **Japan East** view
(`app/cities.py`); wave 4's first city to land retags Japan into the eight
regions, Yamagata into **Tohoku**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**`mode`: `metro`** (the owner's rule of 2026-10-02, "unless there is
substantial JR, JR reads as metro"): JR East holds all 11 station groups; no
subway or tram.

---

## The one-line summary

**Food comes from the city's open-data CSV (CC BY 4.0 as stated; the licence
read is pending, staging records it): every food permit in term on
2026-08-31, 3,584 rows, 2,770 飲食店営業 = 99.3% of e-Stat's 2,789 in
force.** Old-law permits are IN (336, marked （旧）), so Kurashiki's trap does
not apply, and the revised-law permits granted by 2025-03-31 still listed are
96.7% of e-Stat's count that day: closures leave the list. **273 restaurant
permits are 県内一円 vehicles and stalls** (not premises) and **222 are
published without a name or an address** (the operator's opt-out, as MHLW's
own file shows): **2,275 restaurants at a real address, 81.6% of
official.** MHLW's file (cover 0.90) holds 3,006 of its 3,357 permits in the
city's list; its **1,923 notifications** (1,408 addressed) become the partial
Food-shops layer. Block join **91.7%** at fixed premises, unplaced 1.4% (35
of the 40 placed by MHLW's point). **Rail: 11 station groups** (JR Ōu 6,
Senzan 5, Aterazawa 2; 北山形 and 羽前千歳 shared), **16 to 19 trains a day**
on every line (read): nothing under call 86.

---

## Business leg — two food files, one register and its source

| | The city's list | MHLW open data (06201) |
|---|---|---|
| **File** | `https://www.city.yamagata-yamagata.lg.jp/_res/projects/default_project/_page_/001/012/802/062014_syokuhin_list_20260831.csv`: **480,181 B, 3,584 rows**, every food permit in term on **2026-08-31**. Page 1012802 (更新日 令和8年9月10日, published each month on the 10th) | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=06201_food_business_all.csv`: **1,963,932 B, 5,287 rows** (許可 3,357, 届出 1,923, 許可(廃業) 5, 届出(廃業) 2). Grants to 2026-08-31; closures dated 2026-08-05 .. 08-31 |
| What it holds | **Every permit in term**, old law and revised, whatever the filing channel | **Online filings and the city's entries**, opt-in field by field; notifications, temporary permits |
| Encoding | **Shift_JIS (cp932), no BOM, CRLF**; `city_rows` reads it as it stands; dates ISO `2026-08-31` (0 unreadable) | UTF-8 with BOM, CRLF, the national schema |
| Columns | **The national 食品等営業許可・届出一覧 schema (34 columns), 6 filled**: **施設名称** (3,319), **営業の種類**, **所在地_連結表記** (3,317), **許可番号**, **許可年月日**, **許可満了日**. 法人名, 法人番号, phone, postcode, 緯度 / 経度, 業態 and 申請区分 are EMPTY on every row | as Kurume's: 営業施設名称、屋号又は商号, 営業の種類, **業態** (2,146 filled), 営業施設所在地, **緯度 / 経度**, **法人名**, 法人番号, **法人住所**, phones, permit dates, 廃業年月日, 申請区分, 許可条件 |

- **Against the shared tuples**: `NAME_COLS` has 施設名称, `ADDR_COLS` has
  所在地_連結表記, `TYPE_COLS` has 営業の種類: no change needed. `japan_eigyo`
  already reads the （旧） type names (（旧）飲食店営業 → Food service, （旧）菓子製造業
  → Retail, measured).

### The city's list: counts against the official stock

e-Stat 衛生行政報告例 FY2024 (`japan_official.estat()`), 山形県山形市, 飲食店営業
in force 2025-03-31: **2,789** (old law 957, revised 1,832). The 2021
Economic Census counts **1,215** 飲食店 establishments in 06201.

| Restaurants (飲食店営業 and （旧）飲食店営業) | Count | Share of 2,789 |
|---|---|---|
| The list, every row (vehicles and withheld rows included, the Tokyo brief's measure) | **2,770** | **99.3%** |
| … at a real address (一円 and blank out) | **2,275** | **81.6%** |
| … 県内一円 / 山形県内一円 (vehicles and stalls) | 273 | 9.8% |
| … no name and no address (withheld) | 222 | 8.0% |

- **Types (39)**: 飲食店営業 2,434 + （旧） 336; 菓子製造業 280 + 33; そうざい製造業
  102 + 6; 魚介類販売業 68 + 14; 食肉販売業 59 + 12; （旧）喫茶店営業 55; 漬物製造業
  32; 麺類製造業 26 (+ （旧）めん類 1); 密封包装食品製造業 20; みそ又はしょうゆ製造業 20;
  and smaller manufacturing types.
- **Old-law coverage (Kurashiki's trap): present.** 336 （旧） restaurant
  permits (333 granted 2019-03-22 to 2021-05-31, 3 after), expiring 2026
  (152), 2027 (178) or 2028 (6): the list keeps the old law's permits in
  term. e-Stat's 957 old-law restaurants at 2025-03-31 against 336 at
  2026-08-31 is the old law expiring into the new.
- **Closed premises: no column, and only permits in term** (every 許可満了日 is
  on or after 2026-09-30). **Revised-law restaurant permits granted by
  2025-03-31 still listed: 1,771, 96.7% of e-Stat's 1,832 that day**, where
  no revised-law permit has yet expired: the city removes closures (Aomori's
  test read 95.5%). Unreported closures stay invisible: the page keeps the
  standing "may include premises that have closed" bullet.
- **Withheld rows (265 in all: 220 飲食店営業, 26 菓子製造業, 10 そうざい製造業
  …)**: blank name AND blank address, granted mostly in 2025 (90) and 2026
  (123). 261 of them are MHLW permits, and MHLW withholds the address on all
  but 6, under all kinds of 業態 (konbini 8, izakaya 7, restaurants 5, 露店飲食店
  14, blank 148): **the operator's opt-out from open-data publication, not
  vehicles.** Hiroshima's placement wording applies ("About one restaurant in
  twelve…" at build).
- **県内一円 rows (275: 県内一円 237, 山形県内一円 38)**: 270 restaurants and 5
  old-law shops; 249 run 5 years (fixed restaurants run 6 or 7: 1,969 of
  2,275); 266 are MHLW permits, whose 業態 reads 露店飲食店 128, キッチンカー 33,
  自動車 and 移動販売 9 (blank 90), with 「簡易な営業に限る」-type conditions on 216
  and a water tank (「80L程度の水を積載する」) on 96. Not premises;
  `permits_from_rows` already flags 一円.
- **Duplicates**: no exact repeats; (許可番号, 許可年月日) is unique on all
  3,584 (numbers `R08-1234` / `H31-…`, the era year first). At real
  addresses 61 rows repeat an (address, trade name, type) (53 restaurants);
  one pin per premises (trap 7) takes them.
- **Through `japan_eigyo`** (real addresses): **Food service 2,330** (2,275
  restaurants + 55 喫茶店), **Retail 535** (菓子製造業, そうざい製造業,
  魚介類販売業, 食肉販売業; 複合型そうざい 2); 177 manufacturing rows out by "no
  rule" (漬物 32, 麺類 26, 密封包装 20, みそ 20, 食肉処理 14 …), 6 vending
  machines.
- ⚠️ **No 業態 column in the city's list, so `FORM_RULES` sees nothing**
  (Aomori's and Kobe's position): konbini, supermarket and hotel restaurants
  holding 飲食店営業 stay in Food service, unless the build borrows MHLW's 業態
  through the permit match (2,334 of the list's 2,770 restaurants are MHLW
  permits; a measurement for the build, not a call).
- **Economic Census control** (`scripts/japan_census_control.py` at build):
  **2,290** distinct food-service premises, **2,254 placed by the join**,
  **1.86 per establishment** (1,215), inside the built cities' 1.56-1.92.

### MHLW's file (06201)

The universe CSV: open restaurants 2,513, addressed 2,268 (90.3%), cover
0.90. Permit numbers here are the digits of the city's (`1234` for
`R08-1234`).

- **The city enters MHLW's permits**: **3,006 of MHLW's 3,357 permits are in
  the city's list** by the number's digits and the grant date (2,994 under
  the same type); 2,334 of the list's 2,770 restaurants are MHLW permits.
- **The 351 not in the list**: 162 temporary or vehicle permits (業態
  臨時飲食店 153 …), 115 of them already expired (terms under two months);
  **189 open, non-temporary** (162 addressed): granted 2021 (43) and 2022
  (52), likely replaced or closed, and 2026 (68, 50 of them in August, after
  the list's cut-off by the look of it). **MHLW's extra permits stay out**
  (Ichinomiya's precedent, call 126); the build re-reads August's against the
  next edition.
- **Notifications as a partial Food-shops layer (127b)**: 1,923 notifications,
  **1,408 addressed**; through `japan_eigyo` 960 Retail (その他の食料・飲料販売業
  343, 乳類販売業 141, コンビニエンスストア 125, 野菜果物販売業 104, 包装済み食肉 77,
  百貨店、総合スーパー 70 …; out: vending machines 485, institutional 158,
  temporary 93); at fixed premises **763 rows, 656 distinct**. Disclosed as
  partial, opt-in, as in Fukuoka and Kurume. MHLW's permits never enter the
  map; the city's list holds them.
- **Its own coordinates**: block point against MHLW's point, **median 43 m,
  95.7% within 250 m** (3,584 rows; 26 over 1 km).

### Personal services: out (call 138)

The city publishes 理容所・美容所 and クリーニング所 lists (page 1004747 and its
siblings) holding only premises opened since 2019-04, with no licence
stated; the owner kept them out (call 138). The page is **food only**,
Hiroshima's shape: "**This map shows food businesses only.**"

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/06201-24.0a.zip` (194,478 B,
**20,608 block keys**, 501 towns), town-chōme `.../19.0b/06201-19.0b.zip`
(13,327 B, **534**). `japan.CITIES` entry at build: `"yamagata": {"name":
"山形市", "pref": "06", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES,
"wardless": True, "wards": ["06201"]}`.

| Tier (fixed premises in a bucket) | City list (2,865) | Food service (2,330) | Retail (535) | MHLW notifications, Retail (763) |
|---|---|---|---|---|
| Block | **91.7%** | 92.0% | 90.3% | 86.0% |
| Town-chōme / 大字 centroid | 6.9% | 6.4% | 9.2% | 11.3% |
| Unplaced | **1.4%** (40) | 1.6% | 0.6% | 2.8% (21) |
| **Block, chōme or MHLW's point (127c)** | 99.8% (35 of the 40 through the permit match) | | | 100% (own point) |

**The misses, read** (towns only):
- **Unplaced (40)**: 蔵王温泉 in its spellings (上ノ台 7, 上ノ代 5, 上の台 2,
  三度川 4, 荒敷 3, 川前 3, 清水坂, 横倉外, 大字上宝沢外, 川原: the spa town's
  小字 written into the town, with ノ / の variants), 壇野前 2, 河原田, 白山,
  菅沢鬼越, 山寺立石寺境内. A rule that cuts 蔵王温泉 at its 小字 (the shared
  大字 rule's form) and folds ノ / の should place most; measure at build
  against the Minato control.
- **Town-chōme tier (198)**: 蔵王温泉 25 (and its 字 forms 13), みはらしの丘
  1-4丁目 21 (a newer subdivision whose blocks the 24.0a file does not key),
  新山 7, 青柳 5, 沼木字下河原 5, 表蔵王 5.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_06_GML.zip`, N03 code 06201
(**382.4 km²**, extent W 140.179, S 38.143, E 140.531, N 38.352). Read with
`stub_test()`'s method and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 奥羽線 (東日本旅客鉄道, 11) | JR Ōu Line | **6 / 105** | 蔵王, 山形, 北山形, 羽前千歳, 南出羽, 漆山 |
| 仙山線 (東日本旅客鉄道, 11) | JR Senzan Line | **5 / 18** | 羽前千歳, 楯山, 高瀬, 山寺, 面白山高原 |
| 左沢線 (東日本旅客鉄道, 11) | JR Aterazawa Line | **2 / 11** | 北山形, 東金井 |

- **13 station records, 11 N02_005g groups** (羽前千歳 shared by the Ōu and
  Senzan lines, 北山形 by the Ōu and Aterazawa lines, spread 63 m). No name
  in two groups; no pair closer than 600 m. **Median nearest-station gap
  2,221 m** (1,344 to 6,048): standard rings by the spacing rule.
- **Shinkansen**: none filed in the city by N02; the つばさ trains at 山形
  (the Yamagata Shinkansen, run over the Ōu Line) are left out of the counts
  below.
- **Cut at the line** (named by N03 municipality at build): Ōu to 上山市
  (south) and 天童市 (north), Senzan to Sendai, Aterazawa to 山辺町.
- **The light-rail/rail test**: all heavy rail (N02 class 11, JR
  conventional). No tram, light rail or subway.
- **The stub test passes.** No line is cut to one station and none is urban
  (the Aterazawa Line's 2 of 11 is a rural JR line cut at the line).
- **Frequency, read from JR East's own station timetables**
  (`timetables.jreast.co.jp/timetable/list<code>.html` and its weekday pages,
  the 2026-10 edition; codes 山形 1600, 蔵王 0723, 山寺 1606, 東金井 1275; the
  weekday pages fetched by staging's probe 2026-10-06, the 山形 index re-read
  by this brief). **Every departure counted, marked ones included** (a marked
  departure nests its minute in a second span; the probe's count missed one
  on the Senzan Line):

  | Station (line, direction) | Weekday departures | 10:00-15:59 | Largest gap 09-17 |
  |---|---|---|---|
  | 山形 (Ōu, to 新庄・横手) | **19** | 7 | 82 min |
  | 山形 (Ōu, to 福島) | **17** | 4 | 125 min |
  | 蔵王 (Ōu, both ways) | 18 / 17 | 6 / 4 | 71 / 125 min |
  | 山形 (Senzan, to 山寺・仙台) | **19** | 7 | 64 min |
  | 山寺 (Senzan, both ways) | 19 / 19 | 8 / 7 | 68 / 65 min |
  | 山形 (Aterazawa, to 寒河江・左沢) | **16** | 5 | 88 min |
  | 東金井 (Aterazawa, both ways) | 16 / 18 | 5 / 5 | 92 / 91 min |

  **Nothing at about 11 trains a day or fewer**: no call-86 naming. The
  Ōu Line's southbound midday gap (125 min) is the thinnest stretch. The
  master list's "Senzan 18" reads 19 with the marked departure. The
  intermediate stations (北山形, 羽前千歳, 南出羽, 漆山, 楯山, 高瀬, 面白山高原) are
  ASSERTED to see the same trains. Only these counts are recorded, never a
  timetable on the page.
- ⚠️ **Gate 3** at build: JR East's per-line station counts. **OSM
  `name:en`** for 11 groups (one Overpass query at build; not queried here).

## Scope

**Yamagata City.** The Ōu Line runs on to 上山 and 天童, the Senzan Line to
Sendai, the Aterazawa Line to 寒河江 and 左沢; cut at the line.

## Licences — CC BY 4.0 as stated; the read is pending

- **The city's food list, as stated on its page**: 「この 作品 は
  クリエイティブ・コモンズ 表示 4.0 国際 ライセンス の下に提供されています。」 beside the
  CSV, and 「オープンデータの利用にあたっては必ず「山形市オープンデータ利用規約」（以下、「利用規約」）をご一読下さい。なお、データの利用をもって当規約の内容を承諾したものとみなします。」
  (the terms are a PDF, `/_res/common/opendeta/1000082/opendeta_riyou.pdf`).
  **No licence read is recorded in staging's drafts for this source; the read
  is pending (a `licence-read` agent, staging records it).** No verdict is
  written here; the prescribed credit and the 利用規約's terms come from that
  read.
- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as recorded in
  `docs/data_sources/japan.md`. It reaches the map here (the notifications
  layer and the fallback points), so its credit is owed: **MUST DISPLAY**
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; **MUST NOT** present it as MHLW's own, use MHLW's logo or
  claim completeness or accuracy.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The city's open-data file carries no operator column**: 法人名, 法人番号,
  phone and postcode are empty on every row (the page: an individual's
  postcode, address and phone are never published; the operator names sit
  only in the own-format workbook, not downloaded). The name rule, version 2,
  on the city's trade names: **0 bare personal names**.
- **Through MHLW's 法人名, in memory** (answers only, never a value): **4**
  city trade names equal the individual operator's 法人名 on the matching MHLW
  permit (open call 1).
- **MHLW's file carries 法人名 on 4,417 rows (1,795 with no company marker),
  法人住所 on 4,414, phones on 3,491.** Never selected; 法人名 read in memory
  for the name rule only (already in `OPERATOR_COLS`): **19 rows** whose
  trade name is the operator's own name (16 of them notifications, withheld
  from the Food-shops layer), 1 bare personal name.
- Select 施設名称, 営業の種類, 所在地_連結表記, 許可番号 and the two dates from
  the city's list; from MHLW's, 営業施設名称、屋号又は商号, 営業の種類, 業態,
  営業施設所在地, 緯度 / 経度, 許可番号, 許可年月日, 廃業年月日 and 申請区分.
- Run `check_personal_exposure.py yamagata` (`japan=True`) after step 2; it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Tohoku after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city's centroid is 140.369 E (extent
140.18-140.53): project to **UTM 54N (EPSG:32654)**. OSM box from the N03
extent, rounded out: (38.14, 140.17, 38.36, 140.54). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at build
from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band B, food
only (call 137); the personal-services lists out (call 138); the downloads
(call 141); `mode: metro`; the minor tier and Japan East; the 一円 rows out as
not premises (Kobe's trap 6); MHLW's extra permits out (126); MHLW's
notifications as partial food shops (127b); MHLW's point where the join
misses (127c).

**Open, each with a recommendation:**

1. **The name rule through the permit match.** The city's list has no
   operator column, but MHLW's 法人名 (an operator column since 2026-10-05)
   names the operator of 2,334 of its restaurants through the permit, and 4
   city trade names equal an individual's 法人名 there. *Recommend reading
   MHLW's 法人名 in memory through the permit match and withholding those 4*,
   as the rule does wherever the column exists. Tradeoff: one more in-memory
   join in step 2 for 4 rows; without it, a few individuals' own names may
   show as shop names.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control,
  `screen_japan_join.py minato` 98.0 / 0.2 / 1.8, and every city screen):
  the 蔵王温泉 小字 rule and the ノ / の fold if they place the 40.
- `as_of` pinned to **2026-08-31** (the list's own date), never today; the
  list is republished monthly under a dated file name, so `fetch_sources.py`
  reads the page for the current CSV link (Aomori's `current_url` pattern).
- MHLW's 189 open non-temporary permits not in the list, re-read against the
  next edition (August's 50 first); the 業態 borrow through the permit match,
  if the build wants `FORM_RULES` on the city's rows.
- The Economic Census control (estimated 1.86), the factory share, gate 3
  (JR East), OSM `name:en`, line colours on both basemaps, the opening view
  (`map-view`), `check_provenance.py`, `check_scope_disclosure.py`.
- The licence read's credit wording and the 利用規約's terms, from staging's
  record.

```brief-checks
[
  {
    "id": "yamagata-food-page",
    "claim": "The city's food open-data page (1012802) links the CC BY 4.0 licence, the August 2026 full list (062014_syokuhin_list_20260831.csv) and the open-data terms PDF; ASCII anchors only, as the host sends no charset",
    "kind": "http_contains",
    "url": "https://www.city.yamagata-yamagata.lg.jp/kenkofukushi/eisei/1006555/1006558/1012802.html",
    "present": ["creativecommons.org/licenses/by/4.0/", "062014_syokuhin_list_20260831.csv", "opendeta_riyou.pdf", "1012802"]
  },
  {
    "id": "yamagata-food-csv-live",
    "claim": "The city's full food list to 2026-08-31 answers a plain keyless GET (480,181 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://www.city.yamagata-yamagata.lg.jp/_res/projects/default_project/_page_/001/012/802/062014_syokuhin_list_20260831.csv",
    "min_bytes": 400000
  },
  {
    "id": "yamagata-mhlw-live",
    "claim": "MHLW's open-data file for Yamagata (06201), the control and the notifications layer, answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=06201_food_business_all.csv",
    "min_bytes": 1500000
  },
  {
    "id": "yamagata-isj-block-live",
    "claim": "MLIT's block-level address file for Yamagata (06201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/06201-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "yamagata-isj-chome-live",
    "claim": "MLIT's town-chōme file for Yamagata (06201) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/06201-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "yamagata-jr-yamagata-timetable",
    "claim": "JR East's timetable index for 山形 (1600) links the weekday pages of the Aterazawa (030), Senzan (040) and both Ōu (050, 060) directions in the 2026-10 edition - the frequency source; ASCII anchors only (no charset sent)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1600.html",
    "present": ["2610/timetable/tt1600/1600030.html", "2610/timetable/tt1600/1600040.html", "2610/timetable/tt1600/1600050.html", "2610/timetable/tt1600/1600060.html", "StationCd=1600"]
  },
  {
    "id": "yamagata-projected-crs",
    "claim": "Yamagata projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.37,
    "expect": "EPSG:32654"
  }
]
```
