# Matsumoto — build brief

**Band B, owner-approved 2026-10-06** (a Japanese pre-verdict converted in
staging's wave 5, call 133: `docs/decisions_drafts/staging.md`, "Wave 5,
second half": "Matsumoto (the ledger fill measured at the brief)"; the master
list's row: "Personal services; food if the ledger fills MHLW's gaps"). The
Step 0 downloads were approved by the owner 2026-10-06 (calls 133, 147).
**Step 0 measured 2026-10-06** (staging). Into `data/matsumoto/raw/`
(gitignored), each from its publisher's own host with the project user-agent,
each HTTP 200:

- From `linkdata.org` (the city's own LinkData works, published by 松本市
  DX推進本部): the old-law food ledger `shokuhin_kyoka_eigyo_matsumoto.txt`
  (**112,983 B**, as of 2026-07-02, work `rdf1s8748i`); the barber, beauty and
  laundry registers `matsumoto_barber.txt` (**15,919 B**),
  `matsumoto_beauty.txt` (**74,756 B**) and `matsumoto_cleaning.txt`
  (**17,433 B**), as of 2026-07-01 (work `rdf1s8757i`).
- From `i2fas.mhlw.go.jp`: `20202_food_business_all.csv` (**1,802,564 B**),
  the food base measured for call 133.
- From `nlftp.mlit.go.jp`: `isj/20202-24.0a.zip` (219,215 B) and
  `isj/20202-19.0b.zip` (8,168 B).

**2,251,038 B in all.** Nothing else was downloaded: not the 生活衛生 work's
bath, theatre (興行場) or inn tables, nor any `.xls` or Turtle edition, nor
Alpico's timetable PDF (below).

**Run `python scripts/brief_check.py matsumoto` before writing any code.**
Then the `japan-city` skill, **Kōchi's shape** (`docs/build_briefs/kochi.md`:
personal services only, food off because MHLW withholds most addresses) and
**Hamamatsu's for the registers** (one file per kind). Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` has no Matsumoto
entry; its table is shared code and was not edited). Rail: MLIT N02-25 cut at
the N03 city line, through `pipeline/countries/japan.py` with a scratch
`CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs through Matsumoto); (2) **lines served only by limited
expresses DO count** (2026-09-28); (3) **the city line only**: only stations
inside the city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27); an URBAN line cut to ONE station
is left out, its station kept through the other lines, and drawn cut only
where no other line serves that station (owner, 2026-10-06, calls 54 and 92);
(4) **菓子製造業 and そうざい製造業 count, in Retail** (2026-09-24; moot on a
personal-services page); (5) **the name rule**, version 2 (2026-10-06): a
bare personal name is withheld whatever the operator column holds, and MHLW's
法人名 joins it (2026-10-05); (6) **no page says "currently operating"**.
Also: no frequency floor for JR or private lines in Japan (owner, 2026-10-06,
call 46), any stretch at about 11 trains a day or fewer named and drawn (call
86); fault-based cost clauses accepted for all of Japan (2026-09-24); English
station names from OSM `name:en`; every Japanese city reads `WAVE2_RULES`
(owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Matsumoto carries `label_tier: "minor"` and goes in the **Japan East** view
(`app/cities.py`), as Kanazawa, Toyama and Shizuoka; wave 4's first city to
land retags Japan into the eight regions, Matsumoto into **Chubu**. Its label
offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200),
never by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 and Takamatsu's
precedent: JR is not the largest network inside the city (7 station groups
against Alpico's 14), no subway or tram is drawn, and the Kamikōchi Line is a
railway (N02 class 12), not a tram or light rail, so the mode follows the
backbone.

---

## The one-line summary

**Personal services only, from the city's own LinkData registers (CC BY 3.0
as marked; the read is pending, staging records it): barbers 168, beauty
salons 710 and laundries 117 (43 general, 74 pick-up counters) as of
2026-07-01, 97.7%, 103.5% and 93.6% of official; block join 94.6%, unplaced
0.9%.** **Call 133 answered: the old-law ledger does NOT fill MHLW's gaps.**
MHLW's file holds only revised-law permits (from 2021-06-01): 3,315 open
restaurant permits, 1,175 addressed (35.4%). The ledger holds the old-law
permits MHLW lacks (354 restaurants still in term today, 473 at its date), so
together they count **98.0% of e-Stat's 3,742 in force**, but MHLW's 1,690
unaddressed fixed restaurant permits carry no name, no point and no operator,
so nothing can join them. **MHLW plus the ledger place 1,240 restaurants:
42.2% of fixed premises, 33.1% of e-Stat's count**, under the owner's ~70%
bar (call 133), and the ledger's share falls every quarter as its permits
lapse into MHLW. **Recommendation: B, personal services only, as approved**
(Kōchi's 53.9%, food off). **Rail: 20 N02 station groups**: the Alpico
Kamikōchi Line 14 (the whole line inside the city; about every 40 minutes,
ASSERTED), JR East 7 (Shinonoi Line 4, Ōito Line 4, 松本 shared), read from
JR East's timetables: no station at or under about 11 trains a day.

---

## Business leg — personal services from the city's LinkData registers

### Where the city publishes

The city's open-data page `https://www.city.matsumoto.nagano.jp/soshiki/5/4172.html`
(DX推進本部; the host sends no charset) lists 「松本市の生活衛生施設データ」
(クリーニング場、興行場、公衆浴場、美容所、理容所、旅館業; 食品・生活衛生課) and
「松本市の食品営業許可台帳」 (四半期ごとに更新予定) as external links to
LinkData.org, and says the data it publishes is offered under CC BY 4.0
(below, licences). The files are LinkData's own downloads, plain GETs under
`http://linkdata.org/download/<work>/link/<table>.txt`.

Work page `http://linkdata.org/work/rdf1s8757i` (松本市の生活衛生施設データ,
「クリーニング場、興行場、公衆浴場、美容所、理容所、旅館業の2026年7月1日現在のデータです。」;
last update 2026-07-15).

| Table (`…/rdf1s8757i/link/`) | Bytes | Rows | Official (e-Stat FY2024) | Share |
|---|---|---|---|---|
| `matsumoto_barber.txt` 理容所 | **15,919** | **168** | barbers 172 | **97.7%** |
| `matsumoto_beauty.txt` 美容所 | **74,756** | **710** | beauty salons 686 | **103.5%** |
| `matsumoto_cleaning.txt` クリーニング所, 一般クリーニング所 | **17,433** | **43** | general 43 (125 less 82 取次所) | **100.0%** |
| … 取次所 | (same file) | **74** | 取次所 82 | 90.2% |
| … 無店舗取次店 | (same file) | 1 | 1 operator | not a premises |

Laundries together **117 premises of 125, 93.6%**. Official from
`data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` (第10表) and
`…_cleaning_by_city.csv` (第11表), 長野県松本市 (a core city since 2021, so
e-Stat carries its own row).

- **LinkData's text format, not a CSV**: UTF-8, CRLF, tab-separated, nine
  `#` header lines (`#LINK`, `#lang`, `#attribution_name` 松本市　DX推進本部,
  `#license` `http://creativecommons.org/licenses/by/3.0/deed.ja`,
  `#file_name`, `#download_from`, **`#property`** (the column names),
  `#object_type_xsd`, `#property_context`), then one line per row whose first
  cell is LinkData's row subject (empty) and the rest the properties.
  ⚠️ **`japan_register.city_rows` cannot read it today**: its first line
  `#LINK` has no tab, so it splits on commas, finds no address column in 30
  lines and yields every row as one cell. The build adds a LinkData branch
  (a first line of `#LINK`: skip `#` lines, header from `#property`, drop the
  leading subject cell) as shared code with the Minato control, or a
  city-local `source_rows`. The scratch measurement parsed it so
  (`regs.py`, `fill.py` in the wave-5 scratch `brief_matsumoto/`).
- **Columns**: barber and beauty **施設名称**, 施設郵便番号, **施設所在地**,
  **営業者**, 検査確認日, 検査確認番号; laundry the same plus **種別**
  (一般クリーニング所 43, 取次所 74, 無店舗取次店 1).
- **Against the shared tuples**: 施設所在地 is in `ADDR_COLS`, 施設名称 in
  `NAME_COLS`, 種別 in `TYPE_COLS`; `japan_eigyo` reads the laundry kinds
  (laundry register 117, storeless pick-up not a premises 1) and
  `permits_from_rows` marks the 無店舗 row not a premises. **`OPERATOR_COLS`
  lacks 営業者**: add it (it holds companies only here, so the comparison
  finds 0 either way, below).
- **Every address starts 松本市** but one: **a beauty row whose address
  starts 長野市** (another city; it reaches no block). Read it at build: a
  typo, or a premises outside the city to drop. One beauty address and one
  laundry address contain `市内` only as `松本市内田…` (内田 is a town):
  the shared `citywide` test compares the whole remainder to `内`, so they
  are safe; **any new mobile test must not match the substring 市内**.
- **Dates**: 検査確認日 is **an Excel serial in the barber table** (167 five-
  digit, 1 four-digit: 1926-01-01 to **2024-12-11**) and ISO in the others
  (beauty 1954-06-30 to 2026-07-01; laundry to 2025-04-23, one placeholder
  1900-01-01). The barber table's newest confirmation is 2024-12-11 although
  the work is dated 2026-07-01; its count (97.7%) says it is current enough.
  `SOURCE_AS_OF` 2026-07-01 from the work page, never today.
- **検査確認番号 repeats** (barber 100 distinct of 168, beauty 480 of 710,
  laundry 85 of 118): never a key. Repeats by (address, name): beauty 1.
  **12 premises are in both the barber and beauty registers** (one pin per
  premises and bucket keeps one per bucket).
- **Standing registers**; the work page says nothing about closed premises:
  the page keeps "may include closed premises".

### Food — call 133: does the old-law ledger fill MHLW's gaps? No

**The measurement the owner asked for** (call 133): if MHLW plus the city's
ledger place about 70% or more of the restaurants in force, recommend A
(food plus personal services) as an open call; otherwise B.

#### MHLW's file (20202), the base

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=20202_food_business_all.csv`:
**1,802,564 B, 6,116 rows** (許可 4,044, 届出 2,058, 許可(廃業) 9, 届出(廃業) 5),
the national schema. 許可年月日 and 初回許可年月日 **2021-06-01 to
2026-08-31**: **revised-law permits only**, the city's own note says so (below).

- **3,315 open restaurant permits** (許可, not closed, 許可満了日 not past on
  2026-10-06; 23 open permits had lapsed) = **88.6% of e-Stat's 3,742 in
  force** (`japan_official.estat()`, 長野県松本市, 2025-03-31: old law 1,477,
  revised 2,265). **1,175 carry an address (35.4%)**.
- **On fixed premises** (every 一円 or 市内 row and every vehicle or stall
  業態 set aside: 179 addressed rows read citywide, 露店営業 160): **899 of
  2,589, 34.7%**; against e-Stat, **24.0%**.
- **The unaddressed rows carry nothing to join**: of 3,570 unaddressed rows,
  **30 carry a trade name**, none a point, 2 a phone, 19 a 法人名; of the
  1,690 unaddressed fixed restaurant permits, 1 has a trade name. Addresses
  appear only where MHLW also publishes the operator (法人名 on 2,519 of 2,546
  addressed rows): `ADDRESS_BY_CONSENT`, as every MHLW city.

#### The city's old-law ledger (LinkData `rdf1s8748i`)

Work page `http://linkdata.org/work/rdf1s8748i` (松本市の食品営業許可台帳,
「2026年7月2日時点のデータです。」; last update 2026-07-06) with two notes:
「※１ 食品衛生法改正により、2021年6月1日以降に許可を取得した施設の情報は、厚生労働省のオープンデータサイトに公開されることとなりました。松本市のオープンデータサイトの情報には含まれておりませんので…」
and 「※２ …2021年5月31日までに許可を取得した施設で、届出に移行した一部の施設のデータは除いています。」

| Table | Bytes | Rows | What it is |
|---|---|---|---|
| `shokuhin_kyoka_eigyo_matsumoto.txt` | **112,983** | **616** | every old-law permit in term on 2026-07-02; quarterly (the city page: 四半期ごとに更新予定) |

- **Columns**: 営業所郵便番号, **営業所所在地**, **営業所名称**, **業種**,
  **種目１** to 種目５, 許可番号, 許可開始日, 許可満了日, 許可年月日（最新）,
  初回許可年月日. **No operator column, no phone.** Every address is in
  松本市; none reads 一円 or 市内.
- **Old law only**: 許可年月日（最新） 2018-12-28 to 2021-05-31; 許可満了日
  2026-07-31 to 2028-08-31 (none before its date: the table is in term on
  2026-07-02); terms 6 to 7 years. 許可番号 unique (616).
- **Types**: 飲食店営業 473, 菓子製造業 54, そうざい製造業 20, 魚介類販売業 11,
  食肉販売業 11, 喫茶店営業 6, … 21 types. **種目１ is the form** (一般食堂 295,
  旅館 65, スナック 35, バー 19, 弁当屋 13, 仕出し屋 11, 移動営業車 9, キャバレー 1
  among restaurants); 種目２ to ５ are secondary forms (仕出し屋, 弁当屋,
  そうざい屋) and are not read as the form. **`FORM_COLS` holds 種目, not
  種目１**: the scratch copied 種目１ into 種目; through `japan_eigyo` the
  shared form rules then caught hostess venues 36, inside accommodation 35,
  event catering 6, temporary or mobile 3.
- **The ledger decays fast**: of 473 restaurants, **119 ended in 2026Q3**
  (354 in term on 2026-10-06), 54 more end in 2026Q4, 226 in 2027H1; by
  mid-2028 none is left. Each renewal moves the premises into MHLW, where
  about two in three lose their address.

#### The fill

| | At the ledger's date (2026-07-02) | Today (2026-10-06) |
|---|---|---|
| Restaurants in force, MHLW + ledger | 3,315 + 473 = 3,788 (101.2% of e-Stat) | 3,315 + 354 = **3,669 (98.0%)** |
| Fixed premises, MHLW + ledger | 2,589 + 464 = 3,053 | 2,589 + 351 = **2,940** |
| Placed: MHLW addressed + ledger not already an addressed MHLW row | 899 + 446 = 1,345 | 899 + 341 = **1,240** |
| **Share of fixed premises** | 44.1% | **42.2%** |
| Share of e-Stat's 3,742 | 35.9% | **33.1%** |

- **The ledger fills the old-law gap** (Kurashiki's trap: MHLW lacks every
  old-law permit still in term; the union counts 98.0% of e-Stat), **not the
  unaddressed one** (65% of MHLW's fixed restaurant permits, with no field to
  join on). Overlap between the two: 10 in-term ledger restaurants match an
  addressed MHLW row by (address, trade name); no ledger name matches an
  unaddressed MHLW restaurant (they carry no names).
- **Economic Census control**: the 2021 census counts **1,400** 飲食店
  establishments in 20202; MHLW's and the ledger's placed Food-service
  premises (1,121 distinct) are **0.80 per establishment**, against the built
  cities' 1.56-1.92 and the thinnest built MHLW cities' 1.37-1.40 (Kurume,
  Mito).
- **Verdict: B, personal services only**, as Kōchi (53.9% addressed, 57.1%
  on fixed premises: "food fails placement"). Matsumoto is further under the
  bar (42.2% at best, falling).

For the record only, if the owner ever reopened food: through `japan_eigyo`
MHLW's addressed rows give Food service 894 and Retail 790 storefronts (216
permits, 574 notifications), joined 84.0% block / 13.5% chōme / 2.4%
unplaced (34 of 41 misses with MHLW's own point; its point a median 51 m from
the block point, 93.4% within 250 m); the ledger's in-term rows give Food
service 273 and Retail 68, joined 90.9% block.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/20202-24.0a.zip` (219,215 B,
**22,607 block keys**, 234 towns), town-chōme `.../19.0b/20202-19.0b.zip`
(8,168 B, **219**). `japan.CITIES` entry at build: `"matsumoto": {"name":
"松本市", "pref": "20", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES,
"wardless": True, "wards": ["20202"]}`.

| Tier, today's shared code | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| Barbers (168) | **93.5%** | 6.5% | 0.0% |
| Beauty salons (710) | **95.1%** | 3.8% | 1.1% |
| Laundries (117 premises) | **93.2%** | 6.0% | 0.9% |
| **All personal services (995)** | **94.6%** | 4.5% | **0.9%** |

**The misses, read** (towns only):
- **Chōme tier**: 大字 whose 地番 MLIT lacks, mostly the merged villages and
  rural 大字 (梓川倭 7, 島内 4, 会田 3, 和田 3, 安曇 3, 里山辺 2, 波田 2, 笹賀 2,
  奈川, 神林), plus a few `字` forms (内田字新田山道北, 島立字新田) and four
  chōme whose number MLIT lacks (笹部2丁目, 清水2丁目, 桐3丁目, 並柳2丁目).
- **Unplaced (9)**: (a) the registers drop the 字 after a 2- or 3-character
  大字 (`島立荒井`, `島立堀米`, `波田下波田`, `波田下島`, `波田宮ノ久保` for MLIT's
  大字 + 小字): Ichinomiya's short-大字 rule (its brief, "The misses, read";
  also proposed in Akita's) would take them; (b) `里山辺湯の原` and
  `里山辺湯原` (a の written or not); (c) `蟻々崎` (a laundry, read at build); (d)
  the 長野市 beauty row above. All are shared code: follow each with the
  Minato control (`screen_japan_join.py minato` 98.0 / 0.2 / 1.8) and every
  city screen.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_20_GML.zip`, N03 code 20202
(**979.2 km²**, extent W 137.550, S 36.010, E 138.131, N 36.379; the 2005
and 2010 mergers brought in the mountain villages west to Kamikōchi and
Norikura and the town of 波田). Read with `stub_test()`'s method and an
in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 上高地線 (アルピコ交通, 12) | Alpico Kamikōchi Line | **14 / 14** | 松本, 西松本, 渚, 信濃荒井, 大庭, 下新, 北新・松本大学前, 新村, 三溝, 森口, 下島, 波田, 渕東, 新島々 |
| 篠ノ井線 (東日本旅客鉄道, 11) | JR Shinonoi Line | **4 / 15** | 村井, 平田, 南松本, 松本 |
| 大糸線 (東日本旅客鉄道, 11) | JR Ōito Line | **4 / 33** | 松本, 北松本, 島内, 島高松 |

- **22 station records, 20 N02_005g groups** (松本: JR and Alpico, 116 m).
  No name in two groups. **Closest pair 松本-西松本, 417 m** (the only pair
  under 600 m). **Median nearest-station gap 1,021 m** (417 to 2,014): rings
  by the spacing rule at build.
- **Shinkansen**: none.
- **Cut at the line** (named by N03 municipality at build): the Shinonoi Line
  11 beyond (塩尻市 2, 安曇野市 2, 長野市 2, 筑北村 3, 麻績村 1, 千曲市 1), the
  Ōito Line 29 (安曇野市 9, 大町市 9, 白馬村 5, 松川村 3, 小谷村 3). 村井 sits
  299 m inside the city line. Both are main lines cut at the line, not
  stubs. **The Kamikōchi Line lies wholly inside** (松本 to 新島々).
- **The light-rail/rail test**: all three are heavy rail: JR conventional
  (class 11) and the Kamikōchi Line a private railway (class 12, 普通鉄道). No
  tram or light rail.
- **JR East, read 2026-10-06 from its own station timetables** for all 7 JR
  groups (7 index pages, 14 weekday pages and 6 station searches, every
  request HTTP 200, none refused) by plain GET with the project user-agent
  (`timetables.jreast.co.jp`, `timetable/list<code>.html` and the weekday
  pages under `2610/timetable/`, the October 2026 timetable). **Method**: one
  departure per train entry (each train once, marked trains included, an
  empty hour counting nothing), Akita's recount method (`tt.py`).

  | Station (line, direction) | Weekday departures | Per hour 07-18 |
  |---|---|---|
  | 松本 (Ōito, to 信濃大町・白馬) | 27 | 1-3 |
  | 松本 (Shinonoi, to 篠ノ井 / to 塩尻・甲府) | 35 / 81 | 1-3 / 4-8 |
  | 村井 (to 松本 / to 塩尻) | 50 / 51 | 2-8 / 2-6 |
  | 平田 (to 松本 / to 塩尻) | 50 / 51 | 2-8 / 2-5 |
  | 南松本 (to 松本 / to 塩尻) | 50 / 51 | 2-7 / 2-6 |
  | 北松本 (Ōito, to 信濃大町 / to 松本) | 24 / 24 | 1-3 / 1-3 |
  | 島内 (Ōito, to 信濃大町 / to 松本) | 24 / 24 | 1-2 / 1-3 |
  | 島高松 (Ōito, to 信濃大町 / to 松本) | 24 / 24 | 1-2 / 1-3 |

  **No JR station at or under about 11 trains a day** (call 86): the thinnest
  is the Ōito Line, 24 each way (about hourly). JR East files 村井, 平田 and
  南松本 under 篠ノ井線 and 中央本線 (the Chūō Line's trains run through over
  the Shinonoi Line from 塩尻); N02 files the track as 篠ノ井線, the legal
  line: label it the JR Shinonoi Line (the build may add the Chūō Line in the
  legend text if OSM's route relations carry it). 松本's counts include the
  limited expresses (あずさ 16, しなの 13 toward 塩尻), which stop at no other
  station in the city.
- **Alpico Kamikōchi Line: about every 40 minutes, ASSERTED** (the probe's
  reading). Alpico's rail page (`https://www.alpico.co.jp/traffic/rail/`,
  read 2026-10-06) links its timetable 「鉄道上高地線時刻表（2026年3月14日改正）」
  only as a PDF (`/traffic/datas/files/2026/02/24/a09bf710cb0b34042bedda3cae98632d1d2d669f.pdf`),
  a file not named in the approval, so it was not fetched (open call 2).
- ⚠️ **Gate 3** at build: JR East's station counts inside the city (Shinonoi
  4, Ōito 4, 松本 shared) and Alpico's (14, the whole line). **OSM
  `name:en`** for 20 groups (one Overpass query at build, in the box below;
  not queried here).

## Scope

**Matsumoto City.** The Shinonoi Line runs on to 塩尻 south and 篠ノ井 and
長野 north, the Ōito Line to 安曇野, 大町 and 白馬; cut at the line. The
Kamikōchi Line ends at 新島々 inside the city. ⚠️ The city's extent (979
km², west to the Hida mountains) is far larger than its urban area: the
opening view must fit the stations and premises, not the N03 polygon
(`map-view` at build).

## Licences — as marked; the read is pending

**As marked on each dataset**: both LinkData work pages carry the CC BY
badge linking `http://creativecommons.org/licenses/by/3.0/deed.en`, and each
downloaded table's own header carries `#license
http://creativecommons.org/licenses/by/3.0/deed.ja` and `#attribution_name
松本市　DX推進本部`. ⚠️ **The city's own open-data page says otherwise**:
「公開しているデータについては、クリエイティブ・コモンズ・ライセンス 表示4.0国際(CC-BY4.0）の下に提供されています。」
and points to 「松本市オープンデータ利用規約」 (a PDF, 127 KB, not fetched);
LinkData's own site terms ("Terms of use") also apply to its host. **A
licence-read agent reads these separately (pending); staging records its
verdict and the credit wording.** No verdict is written in this brief.

- **MHLW open data**: measured only; not a source on a personal-services page.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **JR East's timetables**: read for counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The registers' 営業者 is filled only for companies**: 15 of 168 barbers,
  170 of 710 beauty salons and 91 of 118 laundries, **every one with a
  company marker**; a sole trader's own name is never published. Read it in
  memory for the name rule only (once 営業者 is in `OPERATOR_COLS`) and never
  write it.
- **The name rule, measured in memory** (answers only, never a value):
  **0** bare personal names among the 996 register trade names; **0** trade
  names equal to their operator. 施設郵便番号 is never selected (施設名称 and
  施設所在地 only).
- The food ledger (not used) has no operator column and 0 bare personal
  names; MHLW (not used) would add its 法人名 to the rule (16 hits among
  not-closed rows, 6 among storefronts).
- Run `check_personal_exposure.py matsumoto` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Chubu after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 137.550-138.131 E, centroid 137.814, 松本
station about 137.97: project to **UTM 53N (EPSG:32653)**. OSM box from the
N03 extent, rounded out: (36.00, 137.54, 36.38, 138.14). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at build
from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band B
(call 133), with food measured here; `mode: metro`; the minor tier and Japan
East (Chubu after the retag); no frequency floor; downloads (calls 133, 147).

**Answered by the owner on 2026-10-06:** call 176, **Alpico's timetable PDF approved for the build** (one file, the 2026-03-14 timetable; counts only, never reproduced) for gate 3 and the Kamikōchi Line's frequency. The recommendations below are kept as the record.

**Weighed, with a recommendation:**

1. **Call 133's answer: food stays off** (B, personal services only). The
   ledger lifts MHLW's 34.7% of fixed restaurant premises to 42.2% today
   (33.1% of e-Stat), under the ~70% bar, and the ledger empties by mid-2028.
   *Recommend B as approved*, Kōchi's page shape; the tradeoff is a page
   without food against a food layer that would show about two restaurants
   in five, skewed to companies (MHLW publishes an address only with its
   operator) and to old-law premises. A partial Food-shops layer from MHLW's
   notifications (call 127b) is not proposed on a personal-services page.
2. **Alpico's timetable PDF** (one file, about the 2026-03-14 timetable) for
   gate 3's counts and the Kamikōchi Line's frequency. *Recommend approving
   it for the build* (counts only, never reproduced); the tradeoff is one
   more download against a frequency left ASSERTED on the page's notes.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): a LinkData reader in `city_rows` (or a city-local `source_rows`);
  `OPERATOR_COLS` + 営業者; optionally the short-大字 rule (with Ichinomiya
  and Akita) and 湯の原 / 湯原.
- The 長野市 beauty row; the barber table's Excel-serial dates;
  `SOURCE_AS_OF` 2026-07-01 from the work page (a later edition re-measured:
  LinkData overwrites a table in place, so the build pins the work page's
  date).
- Gate 3 (JR East, Alpico); OSM `name:en`; line colours on both basemaps; the
  Shinonoi Line's label (and the Chūō Line's through trains, if anywhere);
  the opening view (`map-view`, the city's polygon far larger than its urban
  area); `check_provenance.py`; `check_scope_disclosure.py` (food out, the
  laundry kinds kept, storeless pick-ups out).

```brief-checks
[
  {
    "id": "matsumoto-opendata-page",
    "claim": "The city's open-data page links both LinkData works and says its data is offered under CC BY 4.0 (ASCII anchors: the host sends no charset)",
    "kind": "http_contains",
    "url": "https://www.city.matsumoto.nagano.jp/soshiki/5/4172.html",
    "present": ["rdf1s8748i", "rdf1s8757i", "CC-BY4.0"]
  },
  {
    "id": "matsumoto-registers-work",
    "claim": "LinkData's 生活衛生 work: data as of 2026-07-01, the barber, beauty and laundry tables, marked CC BY 3.0",
    "kind": "http_contains",
    "url": "http://linkdata.org/work/rdf1s8757i",
    "present": ["2026年7月1日現在", "matsumoto_barber.txt", "matsumoto_beauty.txt", "matsumoto_cleaning.txt", "creativecommons.org/licenses/by/3.0"]
  },
  {
    "id": "matsumoto-barber-file",
    "claim": "The barber register (15,919 B) answers a plain GET",
    "kind": "http_ok",
    "url": "http://linkdata.org/download/rdf1s8757i/link/matsumoto_barber.txt",
    "min_bytes": 12000
  },
  {
    "id": "matsumoto-beauty-file",
    "claim": "The beauty register (74,756 B) answers a plain GET",
    "kind": "http_ok",
    "url": "http://linkdata.org/download/rdf1s8757i/link/matsumoto_beauty.txt",
    "min_bytes": 60000
  },
  {
    "id": "matsumoto-laundry-file",
    "claim": "The laundry register (17,433 B) answers a plain GET",
    "kind": "http_ok",
    "url": "http://linkdata.org/download/rdf1s8757i/link/matsumoto_cleaning.txt",
    "min_bytes": 14000
  },
  {
    "id": "matsumoto-ledger-work",
    "claim": "LinkData's food ledger: data as of 2026-07-02, and the note that permits from 2021-06-01 are on MHLW's site only (the old-law list measured for call 133)",
    "kind": "http_contains",
    "url": "http://linkdata.org/work/rdf1s8748i",
    "present": ["2026年7月2日時点のデータです", "2021年6月1日以降に許可を取得した施設の情報は", "shokuhin_kyoka_eigyo_matsumoto.txt", "creativecommons.org/licenses/by/3.0"]
  },
  {
    "id": "matsumoto-mhlw-live",
    "claim": "MHLW's open-data file for Matsumoto (20202) answers a plain keyless GET (measured, not a source)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=20202_food_business_all.csv",
    "min_bytes": 1500000
  },
  {
    "id": "matsumoto-isj-block-live",
    "claim": "MLIT's block-level address file for Matsumoto (20202) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/20202-24.0a.zip",
    "min_bytes": 180000
  },
  {
    "id": "matsumoto-isj-chome-live",
    "claim": "MLIT's town-chōme file for Matsumoto (20202) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/20202-19.0b.zip",
    "min_bytes": 6000
  },
  {
    "id": "matsumoto-jr-matsumoto-timetable",
    "claim": "JR East's timetable index for 松本 (list1444) links the weekday pages read: Ōito (1444010), Shinonoi to 篠ノ井 (1444020), to 塩尻 (1444030). ASCII ids only: the host sends no charset",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1444.html",
    "present": ["tt1444/1444010.html", "tt1444/1444020.html", "tt1444/1444030.html"]
  },
  {
    "id": "matsumoto-jr-shimakoumatsu-timetable",
    "claim": "JR East's timetable index for 島高松 (list0810), on the Ōito Line, links its two weekday pages (0810010, 0810020)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0810.html",
    "present": ["tt0810/0810010.html", "tt0810/0810020.html"]
  },
  {
    "id": "matsumoto-alpico-timetable-pdf",
    "claim": "Alpico's rail page offers the Kamikōchi Line timetable (2026-03-14 revision) only as the PDF named in open call 2",
    "kind": "http_contains",
    "url": "https://www.alpico.co.jp/traffic/rail/",
    "present": ["鉄道上高地線時刻表", "a09bf710cb0b34042bedda3cae98632d1d2d669f.pdf"]
  },
  {
    "id": "matsumoto-projected-crs",
    "claim": "Matsumoto projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 137.97,
    "expect": "EPSG:32653"
  }
]
```
