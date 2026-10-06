# Aomori — build brief

**Band B, food only (Hiroshima's shape), owner-approved 2026-10-06** (Japan
wave 4, banded in staging's wave 5, call 82: `docs/decisions_drafts/staging.md`,
"Wave 5: the ranked queue and the pre-verdicts screened"). The Step 0
downloads were approved by the owner 2026-10-06 (call 106). **Step 0 measured
2026-10-06** (staging). Into `data/aomori/raw/` (gitignored), each from its
publisher's own host with the project user-agent, each HTTP 200, under each
URL's own file name as `japan_fetch.get` saves:

- From `www.city.aomori.aomori.jp` (保健所生活衛生課): the food list
  `r0808zendate.csv` (**929,390 B**, Last-Modified 2026-09-02).
- From `i2fas.mhlw.go.jp`: `02201_food_business_all.csv` (207,869 B), a
  control only.
- From `nlftp.mlit.go.jp`: `isj/02201-24.0a.zip` (220,479 B) and
  `isj/02201-19.0b.zip` (9,775 B).

**1,367,513 B in all.** Nothing else was downloaded. Not fetched (not
approved, not needed): `r0808shinki.csv` (August's new permits, 10.2 KB),
which the full list already holds. JR East's station timetable pages were
read by plain GET for frequency (pages, not data files).

**Run `python scripts/brief_check.py aomori` before writing any code.** Then
the `japan-city` skill, **Hiroshima's shape** for a food-only page
(`docs/build_briefs/hiroshima.md`: Food service and Food shops, no personal
services) on **one complete city list** (no months to rebuild: the city
republishes the whole list each month), Fukuyama's layout for the rail and
the counts (`docs/build_briefs/fukuyama.md`). Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` has no Aomori
entry; its table is shared code and was not edited). Rail: MLIT N02-25 cut at
the N03 city line, measured through `pipeline/countries/japan.py` with a
scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; 新青森 on the Tōhoku and Hokkaidō Shinkansen is dropped, JR's
conventional 新青森 stays); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27); an URBAN line cut to ONE
station is left out (owner, 2026-10-06, calls 54 and 92; none here); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor
for JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at
about 11 trains a day or fewer drawn and named (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from
OSM `name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04);
**市内一円 rows are not premises** (Kobe's trap 6, 2026-09-27).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Aomori
carries `label_tier: "minor"` and goes in the **Japan East** view, as Hakodate
does (`app/cities.py`); wave 4's first city to land retags Japan into the
eight regions, Aomori into **Tohoku**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye:
Aomori's dot sits about 105 km south of Hakodate's across the Tsugaru Strait.

**`mode`: `metro`** (the owner's rule of 2026-10-02, "unless there is
substantial JR, JR reads as metro"): JR East holds 12 of the 18 station
groups inside the city line (Aoimori Railway 7, one shared at 青森); no
subway or tram. Fukuyama's and Okayama's precedent.

---

## The one-line summary

**Food only, from one city CSV (CC BY 4.0 as stated; the licence read is
pending, staging records it): every food permit in term on 2026-08-31,
5,289 rows, 4,217 飲食店営業 = 106.2% of e-Stat's 3,969 in force.** Old-law
permits are IN (837 restaurants granted 2018-11 to 2021-05), so Kurashiki's
trap does not apply. **1,284 rows are addressed only 「青森市全域」 ("the whole
city")**: 1,271 restaurant permits for event stalls and kitchen cars, not
premises; at fixed premises the list holds **2,937 restaurants (74.0% of
official)** plus 9 old-law 喫茶店, and 749 food-shop permits. No closure
column; every expiry is on or after 2026-08-31. MHLW's file holds 120 permits
(cover 0.02), **119 of them in the city's list**: a control, nothing to add.
Block join **95.1%** at fixed premises, unplaced 0.8%. **Rail: 18 station
groups** (JR Ōu 6, JR Tsugaru 7, Aoimori 7, 青森 shared by all three); **the
JR Tsugaru Line runs 9 trains a day out and 8 back** (read): drawn and named
under call 86.

---

## Business leg — the city's 食品営業許可施設一覧

Host `https://www.city.aomori.aomori.jp` (the city's own CMS; the city also
runs an open-data portal, not needed here). Plain GET under
`/_res/projects/default_project/_page_/001/006/184/`.

### Food: 食品営業許可施設一覧（オープンデータ）, page ID 1006184

Page `https://www.city.aomori.aomori.jp/shisei/jouhokoukai/opendata/1006170/1006184.html`
(更新日 2026-09-15; データ所管課 生活衛生課; 更新頻度 「月1回（毎月15日…）」;
リリース日 令和3年8月20日; 「使用言語 日本語・UTF-8」).

| File | Bytes | Rows | What it is |
|---|---|---|---|
| `r0808zendate.csv` 食品営業許可施設一覧（8月末時点全件） | **929,390** | **5,289** | every permit in term on 2026-08-31; the whole list republished monthly |
| `r0808shinki.csv` 食品営業許可施設一覧（8月新規許可取得分） | 10.2 KB (page) | not read | August's new permits, already in the full list |

- **Encoding UTF-8 with BOM, CRLF**, header on line 1; `city_rows` reads it
  as it stands. Dates ISO `2026/8/31`; `wareki_date` reads every 許可年月日
  and 許可満了日 (0 unreadable).
- **Columns (12)**: **施設の名称、屋号**, **施設の所在地１**, 所在地２ (the
  building, 1,515 filled), 施設の電話番号, **営業許可業種**, **許可番号**,
  **許可年月日**, **許可満了日**, **申請者氏名**, **申請者住所1**, 住所２,
  **代表者氏名**. No 業態, no 廃業 column, no coordinates.
- **Types (31)**: 飲食店営業 4,217; 菓子製造業 389; 魚介類販売業 159; 食肉販売業
  114; そうざい製造業 99; 水産製品製造業 70; 漬物製造業 46; アイスクリーム類製造業
  38; 密封包装食品製造業 27; 麺類製造業 20 and めん類製造業 15 (new and old
  spellings); 喫茶店営業 9; and 19 smaller manufacturing types. Old-law-only
  names still present: 喫茶店営業 9, 食品の冷凍叉は冷蔵業 11, 缶詰叉は瓶詰食品製造業
  10, めん類製造業 15 and eight more (the city's own 叉 for 又).
- **Against the shared tuples** (shared code, not edited here): `ADDR_COLS`
  lacks **施設の所在地１** (it has 施設所在地１, without の); `NAME_COLS` lacks
  **施設の名称、屋号** (it has 施設の名称); `TYPE_COLS` lacks **営業許可業種**;
  `OPERATOR_COLS` already reads **申請者氏名** and **代表者氏名**. The scratch
  measurement renamed the three in memory.

### 青森市全域: event stalls and kitchen cars, not premises

**1,284 rows (24.3%) carry the address 「青森市全域」 and nothing else**:
飲食店営業 1,271, 魚介類販売業 12, 菓子製造業 1. Their permits run 5 or 6 years
(every fixed restaurant runs 7 or 8); 所在地２ holds an address on 211 (a
base). **MHLW's own rows say what they are**: of 13 MHLW permits that are
全域 rows in the city's list, 11 carry 業態 臨時 / 臨時飲食店 / キッチンカー or
許可条件 「臨時飲食店営業等の取扱要領で定めた行事及び食品に限る」 or the city's
「自動車による食品の移動営業に関する取扱要領」. Kobe's trap 6 (市内一円 is not a
premises) covers them, but **`permits_from_rows` tests 一円, not 全域**: the
build adds 全域 to the not-a-premises test in shared code (Kurume's 市内 is
the precedent), then re-runs the Minato control and every city screen.
Separately, 9 restaurant rows read 「青森県内一円」; the shared test already
takes them.

### Counts against the official stock

e-Stat 衛生行政報告例 FY2024 (`japan_official.estat()`), 青森県青森市, 飲食店営業 in
force 2025-03-31: **3,969** (old law 1,478, revised 2,491). Every food type:
5,133 (revised 3,089, old law 2,044); the list holds 5,289 (103.0%).

| | Restaurants (飲食店営業) | Share of 3,969 |
|---|---|---|
| The list, every row (vehicles and stalls included, the Tokyo brief's measure) | **4,217** | **106.2%** |
| … at fixed premises (全域 and 一円 out) | **2,937** | 74.0% |
| MHLW's open restaurant permits (control) | 72 (60 addressed) | 1.8% |

- **Old-law coverage (Kurashiki's trap): present.** 837 restaurant permits
  were granted before 2021-06-01 (2018-11-22 to 2021-05-31), 834 of them
  after 2019-03-31; all run 6 to 8 years and end 2026 (171), 2027 (524) or
  2028 (142). The list keeps the old law's permits in term, unlike Kurashiki's
  (new-law only, 52.6%). e-Stat's 1,478 old-law restaurants at 2025-03-31
  against 837 at 2026-08-31 is the old law expiring into the new.
- **Closed premises: no column, and the list holds only permits in term**
  (every 許可満了日 is on or after 2026-08-31; 264 end in 2026). Whether the
  city removes a permit on a closure notice is not stated on the page. The
  evidence points that way: e-Stat's 2,491 revised-law restaurants at
  2025-03-31 against **2,379** revised-law permits granted by that date still
  in the list (95.5%), where fixed revised-law permits run 7 years and none
  has expired yet; e-Stat counts 63 revised-law closures (all types) in
  FY2024 alone. Unreported closures stay invisible, so the page keeps the
  standing "may include premises that have closed" bullet. MHLW cannot test
  it here: it holds no 許可(廃業) row and only 3 届出(廃業).
- **Duplicates**: no exact repeats; (許可番号, 許可年月日) is unique on all
  5,289 rows (the number alone restarts each year: 1,302 distinct). At fixed
  premises, 73 rows repeat an (address, trade name, type) (51 restaurants; 15
  groups at different 所在地２, units in one building; 13 groups where the
  older permit ends within 3 months of the newer's grant). One pin per
  premises (trap 7) takes them: 2,895 distinct food-service premises.
- **Through `japan_eigyo`** (fixed premises): **Food service 2,946** (2,937
  restaurants + 9 喫茶店), **Retail 749** (菓子 388, 魚介類販売 147, 食肉販売 114,
  そうざい 99, 複合型そうざい 1); 301 manufacturing rows out by "no rule"
  (水産製品 70, 漬物 46, アイスクリーム類 38 …), as everywhere.
- ⚠️ **No 業態 column, so `FORM_RULES` sees nothing**: konbini, supermarkets,
  school and hospital kitchens and hotel restaurants holding 飲食店営業 stay in
  Food service. By trade-name word (counts only): konbini 133 (4.5% of 2,937),
  supermarkets 45, kitchens 75, hotels and inns 71; bars and snacks 268.
  Kobe's and Osaka's lists have no 業態 either; the build follows them.
- ⚠️ **Economic Census control** (`scripts/japan_census_control.py` at build):
  the 2021 census counts **1,235** 飲食店 establishments in 02201; 2,876
  distinct placed food-service premises is **2.33 per establishment**, above
  the built cities' 1.56-1.92 (about 2.07 with the kitchens and hotels out
  and konbini and supermarkets moved). 83 addresses hold five or more
  restaurant rows (772 rows: 本町's bar buildings). Read at build; not a
  blocker on precedent, but the page must not imply one dot is one
  establishment.

### MHLW's file (02201), the control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=02201_food_business_all.csv`:
**207,869 B, 577 rows** (届出 454, 許可 120, 届出(廃業) 3), UTF-8 with BOM, the
national schema (営業施設名称、屋号又は商号, 営業の種類, 業態, 営業施設所在地,
緯度 / 経度, 法人名, 法人番号, 法人住所, phones, permit dates, 廃業年月日, 申請区分,
許可条件). Permits 2021-06-29 to 2026-08-28. The universe CSV's cover 0.02:
opt-in online filings only.

- **The city enters every online permit**: 119 of MHLW's 120 permits are in
  the city's list by the number's digits and the grant date, each under the
  same type (MHLW writes `<保健所>指令第123号`, the city `123`). The one left
  was granted 2022-07-15; its number is in the list under another date.
- **Nothing to add**: no open MHLW permit is missing from the city's list.
  Its 454 notifications (248 addressed) are too thin for Matsuyama's partial
  food-shops layer (open call 1).
- **Its own coordinates**: block point against MHLW's point for 281 addressed
  open rows, **median 52 m, 86.1% within 250 m**, 8 over 1 km.

### Personal services: none published

The city's open-data catalogue page for 福祉・健康 (`1006170`) lists the food
list but no barber, beauty or laundry list; the 理容所及び美容所 page
(`…/1002102`, 更新日 2024-12-23) and the クリーニング所 page (`…/1002106`,
2026-05-29) carry forms only (staging's probe; the master list's row). So the
page is **food only**, Hiroshima's shape: "**This map shows food businesses
only.**"

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/02201-24.0a.zip` (220,479 B,
**33,695 block keys**), town-chōme `.../19.0b/02201-19.0b.zip` (9,775 B,
**318**). `japan.CITIES` entry at build: `"aomori": {"name": "青森市", "pref":
"02", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
"wards": ["02201"]}`.

| Tier (fixed premises in a bucket; 全域 and 一円 out) | All (3,695) | Food service (2,946) | Retail (749) |
|---|---|---|---|
| Block | **95.1%** | 95.6% | 93.3% |
| Town-chōme / 大字 centroid | 4.1% | 3.8% | 5.3% |
| Unplaced | **0.8%** (29) | 0.6% | 1.3% |

With the 全域 rows left in, every one of them is unplaced (block 70.6%,
unplaced 26.4% of 4,979): the not-a-premises change above must land first.
MHLW's addressed open rows join at 81.4 / 2.3 / 16.2 (345 rows).

**The misses, read** (towns only):
- **Unplaced (29)**: 28 are in 浪岡 (the town merged in 2005), written
  `浪岡大字<大字>字<小字>` with a 地番 (浪岡大字浪岡字稲村 5, 浪岡大字大釈迦字沢田 3,
  浪岡大字女鹿沢字西花岡 3 …). MLIT's block file names the town `浪岡大字<大字>`
  (22 such towns) with the 小字 apart, so the parsed town carrying 字<小字>
  matches nothing. A rule that cuts the town at 字 after `浪岡大字<大字>` (as the
  shared 大字 rule does elsewhere) should place most at block or 大字; measure
  at build against the Minato control. One more: 卸町6丁目.
- **Chōme tier (152)**: 字 areas of the old city (浪館字泉川 13, 三内字丸山 12,
  浪館字近野 7, 荒川字寒水沢 7, 新城字平岡 6 …), 地番 the block file does not key.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_02_GML.zip`, N03 code 02201
(**824.0 km²**, extent W 140.520, S 40.606, E 140.981, N 40.970; 浪岡町 merged
2005). Read with `stub_test()`'s method and an in-memory `CITIES` entry
(scratch `rail.py`).

| N02 line (operator, type) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 奥羽線 (東日本旅客鉄道, 2) | JR Ōu Line | **6 / 105** | 青森, 新青森, 津軽新城, 鶴ヶ坂, 大釈迦, 浪岡 |
| 津軽線 (東日本旅客鉄道, 2) | JR Tsugaru Line | **7 / 18** | 青森, 油川, 津軽宮田, 奥内, 左堰, 後潟, 中沢 |
| 青い森鉄道線 (青い森鉄道, 5) | Aoimori Railway Line | **7 / 27** | 青森, 筒井, 東青森, 小柳, 矢田前, 野内, 浅虫温泉 |

- **20 station records, 18 N02_005g groups** (青森 is one group for all three
  lines, spread 0 m). No name in two groups; no separate stations closer than
  600 m. **Median nearest-station gap 1,844 m** (1,289 to 6,330): standard
  rings by the spacing rule.
- **Shinkansen**: 新青森 (東北新幹線, 北海道新幹線) dropped; the conventional 新青森
  stays on the Ōu Line.
- **Cut at the line** (named by N03 municipality at build): Ōu 99 beyond
  (弘前市 3, 大鰐町 2, 平川市 2, 藤崎町 1, 田舎館村 1, 90 in Akita, Yamagata and
  Fukushima), Tsugaru 11 (外ヶ浜町 4, 今別町 4, 蓬田村 3), Aoimori 20 (平内町 4,
  東北町 4, 南部町 4, 八戸市 3, おいらせ町 2, 三沢市 1, 三戸町 1, 野辺地町 1).
- **The light-rail/rail test**: all three are heavy rail (N02 class 11, JR
  conventional; class 12, the Aoimori Railway, the third-sector successor of
  JR's Tōhoku Main Line). No tram, light rail or subway.
- **The stub test passes.** No line is cut to one station and none is urban.
  The Tsugaru Line's 7 of 18 is a rural JR line (its 蟹田 to 三厩 end lies
  outside the city); the Ōu Line's 6 of 105 is a main line cut at the line.
- **Frequency, read 2026-10-06 from JR East's own station timetables** by
  plain GET (`timetables.jreast.co.jp/timetable/list<code>.html` and its
  weekday pages, the 2026-10 edition; codes 青森 0025, 新青森 0854, 鶴ケ坂 1021,
  浪岡 1124, 油川 0073, 中沢 1094):

  | Station (line, direction) | Weekday departures | 10:00-15:59 | Largest gap 09-17 |
  |---|---|---|---|
  | 青森 (Ōu, to 弘前) | 36 | 12 (every 30 min) | 52 min |
  | 新青森 (Ōu, both ways) | 38 / 36 | 11 | 49-51 min |
  | 鶴ケ坂 (Ōu, both ways; local stops only) | 20 / 21 | 7 | 83-101 min |
  | 浪岡 (Ōu, both ways) | 25 / 24 | 7-8 | 82-104 min |
  | 青森 (Aoimori, to 野辺地 / 八戸; JR East's page) | 23 | 6 (hourly) | 81 min |
  | 油川, 中沢 (Tsugaru, to 蟹田) | **9** | 3 | 135 min |
  | 油川, 中沢 (Tsugaru, to 青森) | **8** | 2 | 192-193 min |

  **The JR Tsugaru Line (青森 to 中沢, 6 stations beyond 青森) is at about 11
  trains a day or fewer: drawn and named under call 86.** (The master list's
  row and staging's task call it "the Tsugaru Railway"; that is a different
  company, 津軽鉄道, in Goshogawara, with no station in Aomori City. The line
  here is JR East's 津軽線.) Everything else runs 20 or more a day. The
  Aoimori figure is JR East's page for the shared 青森 station, not the
  Aoimori Railway's own site (not fetched); its intermediate stations are
  ASSERTED to see the same trains. Only these counts are recorded, never a
  timetable on the page.
- ⚠️ **Gate 3** at build: JR East's per-line station counts and the Aoimori
  Railway's 27. **OSM `name:en`** for 18 groups (one Overpass query at build;
  not queried here; 鶴ヶ坂 is 鶴ケ坂 on JR East's pages, so read the OSM form).

## Scope

**Aomori City** (including 浪岡, merged 2005). JR Ōu runs on to 弘前 and
Akita, the Tsugaru Line to 蟹田, the Aoimori Railway to 野辺地 and 八戸; cut at
the line.

## Licences — CC BY 4.0 as stated; the read is pending

- **The food list, as stated on its page**: 「この作品はクリエイティブ・コモンズ
  表示 4.0 国際 ライセンスの下に提供されています」, and 「本セクションで公開しているデータは、
  クリエイティブ・コモンズ・ライセンスのもとで提供しております。対象データのご利用に際しては、
  表示されている各ライセンスの利用許諾条項に則ってご利用ください。」 **The full read is a
  separate `licence-read` agent's, running in parallel; staging records it.**
  No verdict is written here. The prescribed credit and any site-policy
  terms come from that read.
- **MHLW open data** (control only, unless open call 1 changes that): PDL 1.0
  as recorded in `docs/data_sources/japan.md`; nothing of it reaches the map,
  so no credit is owed unless it does.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The list carries the applicant block**: **申請者氏名** on every row (3,080
  with no company marker, an individual's own name in most; 2,209 with one),
  **代表者氏名** and **申請者住所1 / 住所２** (the operator's own address) on 2,221
  rows (always together; 13 of them with no company marker), and
  施設の電話番号 on 3,065. Step 2 never reads any of them into an output;
  申請者氏名 and 代表者氏名 are read IN MEMORY for the name rule only (both
  already in `OPERATOR_COLS`).
- **The name rule, version 2, measured in memory** (answers only, never a
  value): **0** rows whose trade name is the operator's own name, **0** bare
  personal names. MHLW: 法人名 on 334 rows (31 with no company marker); name
  rule 0.
- Select 施設の名称、屋号, 施設の所在地１, 所在地２ (if the join wants it),
  営業許可業種, 許可番号 and the two dates only.
- Run `check_personal_exposure.py aomori` (`japan=True`) after step 2; it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Tohoku after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city's centroid is 140.754 E (extent 140.52-140.98):
project to **UTM 54N (EPSG:32654)**, Hakodate's and Sapporo's zone. OSM box
from the N03 extent, rounded out: (40.60, 140.51, 40.98, 140.99). Scaffold
with `scripts/scaffold_city.py ... --page-number <N>`, the number claimed at
build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band B, food
only, Hiroshima's shape (call 82); the downloads (call 106); `mode: metro`;
the minor tier and Japan East; the JR Tsugaru Line drawn and named at 9
trains a day (call 86); the three lines drawn as cut (standing call, no
stub); the Shinkansen out; the 全域 rows out as not premises (Kobe's trap 6;
the shared-code spelling is the build's).

**Open, each with a recommendation:**

1. **MHLW beside the list.** *Recommend control only*: the city's list
   already holds 119 of its 120 permits, its own points would add little
   (the block join leaves 29 unplaced), and its 454 notifications (248
   addressed) are opt-in and too thin for Matsuyama's partial food-shops
   layer, where Matsuyama's held thousands. Tradeoff: the Food shops layer is
   permits only (bakeries, delis, butchers, fishmongers), which the standing
   bullet already says; MHLW's credit stays off the notice.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control, `screen_japan_join.py
  minato` 98.0 / 0.2 / 1.8, and every city screen): `ADDR_COLS` + 施設の所在地１;
  `NAME_COLS` + 施設の名称、屋号; `TYPE_COLS` + 営業許可業種; **全域** in
  `permits_from_rows`' not-a-premises test; the 浪岡大字…字… town rule if it
  places the 28.
- `as_of` pinned to **2026-08-31** (the list's own date), never today.
- The Economic Census control (estimated 2.33, above the built range): read
  why before publishing; the factory share; gate 3 (JR East, Aoimori), OSM
  `name:en`, line colours on both basemaps, the opening view (`map-view`),
  `check_provenance.py`, `check_scope_disclosure.py`.
- The licence read's credit wording, from staging's record.

```brief-checks
[
  {
    "id": "aomori-food-page",
    "claim": "The food dataset page links the CC BY 4.0 licence and offers the August 2026 full list (r0808zendate.csv) and new permits; ASCII anchors only, as the host sends no charset and requests decodes the page as Latin-1",
    "kind": "http_contains",
    "url": "https://www.city.aomori.aomori.jp/shisei/jouhokoukai/opendata/1006170/1006184.html",
    "present": ["creativecommons.org/licenses/by/4.0/", "r0808zendate.csv", "r0808shinki.csv", "1006184"]
  },
  {
    "id": "aomori-food-csv-live",
    "claim": "The city's full food list to 2026-08-31 answers a plain keyless GET (929,390 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://www.city.aomori.aomori.jp/_res/projects/default_project/_page_/001/006/184/r0808zendate.csv",
    "min_bytes": 800000
  },
  {
    "id": "aomori-mhlw-live",
    "claim": "MHLW's open-data file for Aomori (02201), the control, answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=02201_food_business_all.csv",
    "min_bytes": 150000
  },
  {
    "id": "aomori-isj-block-live",
    "claim": "MLIT's block-level address file for Aomori (02201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/02201-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "aomori-isj-chome-live",
    "claim": "MLIT's town-chōme file for Aomori (02201) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/02201-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "aomori-jr-aomori-timetable",
    "claim": "JR East's timetable index for 青森 (0025) links three lines' weekday pages (010 the Ōu Line, 020 the Aoimori Railway, 030 the Tsugaru Line) - the frequency source; ASCII anchors only (no charset sent), in the 2026-10 edition",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0025.html",
    "present": ["2610/timetable/tt0025/0025010.html", "2610/timetable/tt0025/0025020.html", "2610/timetable/tt0025/0025030.html", "StationCd=25"]
  },
  {
    "id": "aomori-jr-aburakawa-timetable",
    "claim": "JR East's timetable index for 油川 (0073), a Tsugaru Line station inside the city, links both directions' weekday pages (010, 020) in the 2026-10 edition; ASCII anchors only",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0073.html",
    "present": ["2610/timetable/tt0073/0073010.html", "2610/timetable/tt0073/0073020.html"]
  },
  {
    "id": "aomori-projected-crs",
    "claim": "Aomori projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.75,
    "expect": "EPSG:32654"
  }
]
```
