# Mito — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 129: `docs/decisions_drafts/staging.md`, "Wave 5, second half"; the
master list's row: "One under the smallest built page (7 stations): the
smallest page if built"). The Step 0 downloads were approved by the owner
2026-10-06 (call 147). **Step 0 measured 2026-10-06** (staging). Into
`data/mito/raw/` (gitignored), each from its publisher's own host with the
project user-agent, each HTTP 200:

- From `www.city.mito.lg.jp` (水戸市 保健衛生課, page 生活衛生関係施設一覧): the
  four personal-services lists as of 2026-07-02, `71286.csv` **barbers**
  (23,221 B), `71287.csv` **beauty salons** (84,749 B), `71288.csv`
  **laundries, general** (クリーニング所・一般; 4,959 B), `71289.csv`
  **laundry pick-up counters** (クリーニング所・取次店; 8,000 B).
- From `i2fas.mhlw.go.jp`: `08201_food_business_all.csv` (2,138,515 B),
  **the food source**.
- From `nlftp.mlit.go.jp`: `isj/08201-24.0a.zip` (494,740 B) and
  `isj/08201-19.0b.zip` (8,386 B).

**2,763,050 B in all.** Nothing else was downloaded: not the page's fifth
laundry file (`71290.csv`, 無店舗取次店, storeless pick-ups, not premises), nor
its inn, bath, theatre or building lists.

**Run `python scripts/brief_check.py mito` before writing any code.** Then the
`japan-city` skill, **Kurume's shape for food** (`docs/build_briefs/kurume.md`:
MHLW's open data alone, the city's own food page pointing to it) and
**Hamamatsu's for the registers** (one file per kind). Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` has no Mito entry;
its table is shared code and was not edited). Rail: MLIT N02-25 cut at the
N03 city line, measured through `pipeline/countries/japan.py` with a scratch
`CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs through Mito); (2) **lines served only by limited
expresses DO count** (2026-09-28); (3) **the city line only**: only stations
inside the city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27); an URBAN line cut to ONE station
is left out, its station kept through the other lines, and drawn cut only
where no other line serves that station (owner, 2026-10-06, calls 54 and 92);
(4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory share
measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds, and MHLW's 法人名 joins it (2026-10-05); (6) **no page says "currently
operating"**. Also: no frequency floor for JR or private lines in Japan
(owner, 2026-10-06, call 46), any stretch at about 11 trains a day or fewer
named and drawn (call 86); fault-based cost clauses accepted for all of Japan
(2026-09-24); English station names from OSM `name:en`; every Japanese city
reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Precedents set 2026-10-06, applied here (do not re-ask):** MHLW's
notifications as a partial Food-shops layer where they hold hundreds of
addressed rows (call 127b: 1,003 storefront rows here); MHLW's own point
where the block join misses (call 127c, `OWN_POINT_FALLBACK`); a stated food
share where the food source is incomplete (call 125, Ichinomiya's 67.7%).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Mito
carries `label_tier: "minor"` and goes in the **Japan East** view
(`app/cities.py`); wave 4's first city to land retags Japan into the eight
regions, Mito into **Kantō**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02: no subway, tram or
monorail; JR East and Kashima Rinkai are both railways (N02 class 11 and 12).
Kurume's and Akita's precedent.

---

## The one-line summary

**All three buckets.** Food from **MHLW's file alone** (PDL 1.0 as recorded):
**2,887 open restaurant permits, 90.6% of e-Stat's 3,188 in force**; the
probe's "80.7% addressed" counts 252 rows that read 市内一円 or 県内一円
(vehicles and stalls), so **2,077 carry a real address, and on fixed premises
2,077 of 2,549 (81.5%) can be placed**. Barbers 258, beauty salons 821 and
laundries 117 from the city's CSVs as of 2026-07-02 (CC-BY as stated; the
read is pending): **100.0%, 101.0% and 96.7% of official**. Through
`japan_eigyo`: **Food service 1,714, Retail 1,586** (583 permits, 1,003
notifications, partial). Block join **90.9%** of storefronts (Food service
94.2%), 0.2% unplaced after MHLW's own points; registers 91.3-95.8% block.
**Rail: 6 N02 station groups**, JR East 4 (Jōban Line 4, the Suigun Line's
水戸) and Kashima Rinkai 3, 水戸 shared: **one under the smallest built page
(7)**. ⚠️ **One of the six, 偕楽園, is a seasonal station** with no departure in
JR East's October 2026 timetable: **open call 1** (leaving it out makes 5).
Frequencies READ from both operators: the Jōban at 赤塚 and 内原 2-5 an hour
each way plus the Mito Line's 1-2, the Suigun 26 a day from 水戸, Kashima
Rinkai 36 a day each way.

---

## Business leg — food from MHLW's open data, alone

### The city's food page points to MHLW

Page `https://www.city.mito.lg.jp/site/open-data/3745.html` (食品営業許可施設一覧,
更新日 2025-09-17) holds no file of its own: 「※最新のデータが厚生労働省のホームページにて公開されております。」
with a link to MHLW's per-municipality download page. The city enters its
permits into MHLW's 食品衛生申請等システム; MHLW's file is the city's food list,
as in Kurume.

### MHLW's file (08201)

| | MHLW open data (08201) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=08201_food_business_all.csv`: **2,138,515 B, 6,308 rows** (許可 3,638, 届出 2,663, 許可(廃業) 7). UTF-8 with BOM, the national schema |
| As of / cadence | 許可年月日 2020-09-30 to **2026-08-31**; closures dated 2026-08-01 to 08-14. Monthly (MHLW) |
| Columns | 自治体コード, 行番号, 都道府県名, 市区町村名, **営業施設名称、屋号又は商号** (+ フリガナ), **営業の種類**, **業態**, **営業施設所在地**, 営業施設方書, **緯度 / 経度**, 営業施設電話番号, **法人名**, 法人番号, 法人住所, 許可番号, 初回許可年月日, 許可年月日, 許可開始日, **許可満了日**, **廃業年月日**, **申請区分**, 許可条件, 備考 |
| Operator column | **法人名** (a company's name, or a sole trader's own: the name rule reads it in memory, owner 2026-10-05) |

- **Types carry a circled number** (`① 飲食店営業`, `⑪ 菓子製造業`,
  `⑩ コンビニエンスストア`); `japan_eigyo.normalise` strips it as in the built
  MHLW cities.
- **業態 is free text** with many spellings of one form (`スナック`,
  `飲食店営業（スナック）`, `飲食店営業(スナック)`, `飲食店営業　スナック`; `自動車営業`,
  `飲食店営業（自動車）`, `飲食店営業（自動車営業）`): the shared 業態 rules
  caught every vehicle and stall spelling in this file (0 real-address rows
  with a vehicle or stall 業態 left over), and 117 hostess-venue rows (below).

### Counts that matter

Open restaurant permits: 許可, no 廃業年月日, 許可満了日 not past on
2026-10-06.

- **2,887 open 飲食店営業 permits = 90.6% of e-Stat's FY2024 in force**
  (`japan_official.estat()`, 茨城県水戸市, 2025-03-31: **3,188**, old law 878,
  revised 2,310). By first-permit year: 2020 5 · 2021 228 · 2022 569 · 2023
  688 · 2024 528 · 2025 594 · 2026 275. **Only 5 first permits predate
  2021-06-01**: the gap is old-law permits still in term, which enter MHLW only
  when renewed (Kurume's reading; Kurashiki's trap, here on the source itself).
- 🔎 **The probe's 80.7% "with an address" overstates it.** 2,329 rows carry
  something in 営業施設所在地, but **252 read only 水戸市内一円 / 茨城県内一円 /
  市内一円** (業態 自動車営業 68, 飲食店営業（自動車） 58, 飲食店営業（露店営業） 31,
  露店営業 21, …): vehicles and stalls licensed area-wide. **A real address:
  2,077, 71.9% of open restaurant permits.** No row reads only `水戸市内`
  (Kurume's `citywide` case does not arise; `一円` is already "not a premises"
  in `permits_from_rows`).
- **On fixed premises** (Kurume's measure: every 一円 row and every vehicle or
  stall 業態 set aside): **2,077 of 2,549, 81.5%** (Kurume 79.6%). 業態 is
  published even where the address is withheld; only 25 fixed, unaddressed
  permits lack it. **Placeable against the official count: 2,077 of 3,188,
  65.2%.**
- **Lapsed permits MHLW still lists as open**: 106 restaurant permits whose
  許可満了日 had passed by 2026-10-06 (34 addressed), **80 by the file's own
  2026-08-31** (16 addressed). The counts above leave them out; `japan_step2`
  today has no 許可満了日 filter for an MHLW source (below, the build).
- **Repeats**: 11 permit numbers occur twice among 許可 rows. One pin per
  premises and bucket leaves **2,893 pins from 3,300** storefront rows.
- **Closures**: 7 rows 許可(廃業) (closed 2026-08); step 2 drops them.

### Counts through `japan_eigyo` (step 2's order, all open rows)

Of 6,301 rows not closed: **no address published 1,826** (MHLW publishes an
address only by consent: `ADDRESS_BY_CONSENT`), **not a premises 310**
(addressed 一円 rows and vehicles). Of the rest:

- **Storefronts: Food service 1,714, Retail 1,586.** Retail is **583
  permits** (菓子製造業 238, 飲食店営業 moved to Retail by 業態 (konbini, supermarket,
  deli) 141, そうざい製造業 83, 魚介類販売業 66, 食肉販売業 55) and **1,003
  notifications** (その他の食料・飲料販売業 449, コンビニエンスストア 151, 百貨店・総合スーパー
  81, 野菜果物販売業 80, 乳類販売業 70, 弁当販売業 69, packaged meat 45 and fish 34,
  米穀類販売業 24): **the partial Food-shops layer of call 127b**, disclosed as
  partial on the page.
- **Out by rule**: no rule 296 (manufacturing: その他の食料品製造・加工業 103,
  農産保存食料品 26, コーヒー 25, 漬物 24, 麺類 17, 調味料 14, 食肉処理 7, …),
  vending 144, institutional catering 199, **hostess venues 117** by 業態
  (スナック 45, 飲食店営業（スナック） 37, キャバクラ 10, 飲食店営業(スナック) 6, …;
  `docs/category_rules.md`, adult and hostess venues), temporary or mobile
  49, inside accommodation 25, entertainment venue 19, mail order 9, event
  catering 7.
- **Economic Census control** (`scripts/japan_census_control.py` at build):
  the 2021 census counts **1,214** 飲食店 establishments in 08201; 1,700
  distinct placed Food-service premises is **1.40 per establishment**, below
  the built cities' 1.56-1.92, as Kurume's 1.37: a file holding 91% of
  permits and withholding a fifth of fixed addresses. Record it with that
  reason.

## Personal services — the city's 生活衛生関係施設一覧

Page `https://www.city.mito.lg.jp/site/open-data/4496.html` (更新日
2026-07-15; ライセンス CC-BY; コピーライト 水戸市役所; 担当課 保健衛生課). Two
notes on the page: 「※1：営業所の電話番号が個人の携帯電話番号の場合は、個人情報保護の観点から公開しておりません。」
and 「※2：すでに営業していない施設も含まれている場合があります。」 The page keeps
"may include closed premises".

| File (`/uploaded/attachment/`) | Link text | Bytes | Rows | Official (e-Stat FY2024) | Share |
|---|---|---|---|---|---|
| `71286.csv` | 施設一覧（理容所）（令和８年７月２日現在） | **23,221** | **258** | barbers 258 | **100.0%** |
| `71287.csv` | 施設一覧（美容所）（令和８年７月２日現在） | **84,749** | **821** | beauty salons 813 | **101.0%** |
| `71288.csv` | 施設一覧（クリーニング所・一般）（令和８年７月２日現在） | **4,959** | **48** | general 49 (121 laundries less 72 取次所) | 98.0% |
| `71289.csv` | 施設一覧（クリーニング所・取次店）（令和８年７月２日現在） | **8,000** | **69** | 取次所 72 | 95.8% |

Laundries together **117 of 121, 96.7%**. Official from
`data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` (第10表) and
`…_cleaning_by_city.csv` (第11表), 茨城県水戸市; e-Stat also counts 7 無店舗取次店
operators, whose list (`71290.csv`, 590 B) was not downloaded: not premises
(`japan_eigyo`, Fukushima's).

- **Shift_JIS (cp932), CRLF, header on row 1**, no empty rows; the same seven
  columns in all four: **屋号**, **施設所在地**, 施設電話番号, 許可番号,
  許可決裁年月日, **営業者氏名**, **代表者氏名**. `japan_register.city_rows`
  reads all four as they stand (258, 821, 48, 69).
- **No kind column**: one file per kind, so the config names the kind per
  file (`SOURCE_KIND`, Hamamatsu's and Fukushima's registers): `barber`,
  `beauty`, and `laundry` for both laundry files (a `laundry_toritsugi` key of
  kind `laundry`). 施設所在地 is in `ADDR_COLS`, 屋号 in `NAME_COLS`, 営業者氏名
  and 代表者氏名 in `OPERATOR_COLS`: no shared-code change for the registers.
- **Every address starts 水戸市** (one beauty row starts 茨城県水戸市); none is
  outside the city, none a vehicle. 許可決裁年月日 is wareki text (昭和 to 令和8年7月1日);
  standing registers, not a stream (beauty 270 of 722 parsed dates since
  2020). 許可番号 repeats across its series (barbers 207 distinct of 258): never
  a key.
- **Repeats**: beauty 1 (address, name); **13 premises in both the barber and
  beauty lists** (one pin per premises and bucket keeps one per bucket); none
  in both laundry files.
- **File names are attachment ids** (`71286` …): a refresh posts new ids, so
  the build reads the page and takes each file by its link text
  (`japan_fetch.current_url` with a `SOURCE_LINKS` regex per key, e.g.
  `施設一覧（理容所）`), and pins `SOURCE_AS_OF` to the date in the link text
  (2026-07-02), never today.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/08201-24.0a.zip` (494,740 B,
94,113 rows, **86,490 block keys** with the 小字 aliases, 246 towns),
town-chōme `.../19.0b/08201-19.0b.zip` (8,386 B, **231**). `japan.CITIES`
entry at build: `"mito": {"name": "水戸市", "pref": "08", "epsg": 32654,
"n02": "25", "rules": WAVE2_RULES, "wardless": True, "wards": ["08201"]}`.

| Tier, today's shared code | All storefronts (3,300) | Food service (1,714) | Retail (1,586) |
|---|---|---|---|
| Block | **90.9%** | 94.2% | 87.4% |
| Town-chōme / 大字 centroid | 8.0% | 5.3% | 10.9% |
| Unplaced | 1.1% | 0.6% | 1.7% |
| **After MHLW's own point** (`OWN_POINT_FALLBACK`, call 127c): block / own / centroid / unplaced | **90.9 / 6.5 / 2.3 / 0.2** | 94.2 / 4.7 / 1.1 / 0.1 | 87.4 / 8.6 / 3.6 / 0.4 |

| Registers | Barbers (258) | Beauty (821) | Laundry, general (48) | Pick-up counters (69) |
|---|---|---|---|---|
| Block / chōme / unplaced | 94.2 / 4.3 / 1.6 | 95.5 / 4.1 / 0.4 | 95.8 / 4.2 / 0.0 | 91.3 / 8.7 / 0.0 |

Kakogawa's tiers disclosure (call 145, 86.5% block, 13.3% at a centroid) is
not triggered on that shape: 2.3% of storefronts stay at a centroid after the
fallback. The build re-measures and applies call 145 only if that changes.

- **MHLW's own coordinates against the block point** (the independent
  check): **median 64 m, 88.3% within 250 m** (2,998 rows; 52 over 1 km, most
  in 鯉渕町 9, 河和田町 4, 東台1丁目 4, 内原町 4). With the default points
  removed: median 62 m, 88.4%, 47 over 1 km. Wider than Kurume's 48 m and
  93.7%; under `datum_guard`'s 200 m.
- **Default points** (`shared_points`, 3+ towns): MHLW's stand-in point for
  area-wide filings carries **291 rows** (市内一円 198, 県内一円 50, 茨城県内一円
  23, …); 9 storefront rows sit on it (two at a festival venue address,
  水戸まちなかフェティバル会場内) and are refused, as designed.
- **The 内原 cluster** (AEON Mall Mito Uchihara at 内原2丁目1): **108
  storefront rows take the 内原2丁目 centroid**, because MLIT's block file holds
  only blocks 59 and 135 under 内原2丁目. MHLW's point for the mall is refused
  as a default: its 60 rows spell the town 内原2丁目, 内原町 and 内原1丁目, three
  "towns" to `shared_points`. **Harmless here**: the centroid sits a median 52
  m from MHLW's point (114 rows, max 406 m). ⚠️ A shared-code note, not a Mito
  change: `shared_points` counts spelling variants of one 大字 as distinct
  towns, so a large single premises can read as a default point.

**The misses, read** (towns only, by `measure.py` and `more.py` in the
scratchpad):
- **Chōme tier**: 内原2丁目 114 (above), 内原町 18, 河和田1丁目 15 (地番 such as
  1584-1699 and 2424, which MLIT's block list lacks), 堀町字新田 and
  渡里町字前原 6 each, 石川町 5: they take the town or 大字 centroid, or MHLW's
  own point where it has one (261 chōme-tier rows have one).
- **Unplaced (37 storefront rows; 19 with a usable own point)**: (a) **大字 +
  小字 without the 字** where MLIT keys the 小字 with it or not at all:
  千波町北葉山 8, 千波町東久保 3, 大塚町成就院下 2, 河和田町中道 2, 元吉田町岡崎 2,
  元吉田町荒谷 2, 堀町新田 2 (MLIT holds 千波町 with 字かち道, 字中山, 字千波山 and
  字海道付 only; 元吉田町 with 字一本松 and 字上千束). A "3-character 大字, then a
  小字" fallback to the 大字 is the same family as Ichinomiya's short-大字 rule
  (its brief, "The misses, read"); (b) 宮町 and 泉町 with no 丁目 (MLIT keys
  宮町1丁目 to 3丁目): the `chome_missing` rule did not take them; (c) one
  `水戸市泉町` with the city written twice, and the two festival-venue rows.
  All are shared code: follow any change with the Minato control
  (`screen_japan_join.py minato` 98.0 / 0.2 / 1.8) and every city screen.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_08_GML.zip`, N03 code 08201
(**217.0 km²**, extent W 140.322, S 36.301, E 140.587, N 36.464; 内原町 merged
in 2005). Read with `stub_test()`'s method and an in-memory `CITIES` entry
(scratch `rail.py`, `track.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Track inside | Stations inside |
|---|---|---|---|---|
| 常磐線 (東日本旅客鉄道, 11) | JR Jōban Line | **4 / 81** | 16.9 km | 内原, 赤塚, 偕楽園 ⚠️, 水戸 |
| 大洗鹿島線 (鹿島臨海鉄道, 12; third sector) | Kashima Rinkai Ōarai Kashima Line | **3 / 15** | 11.0 km | 水戸, 東水戸, 常澄 |
| 水郡線 (東日本旅客鉄道, 11) | JR Suigun Line | **1 / 45** | 3.8 km | 水戸 |

- **8 station records, 6 N02_005g groups** (水戸's three records, 68 m). No
  name in two groups; no stations closer than 600 m. **Median nearest-station
  gap 3,818 m** (1,854 to 5,757): rings by the spacing rule at build.
  **Six groups is one under the smallest built page (7)**, as the band row
  says; with 偕楽園 left out (open call 1) it is **five, two under**.
- **Shinkansen**: none in the city.
- **The Mito Line (水戸線)**: N02 files it 小山 to 友部, 0 km inside the city,
  but its 19 weekday trains run through over the Jōban to 水戸, calling at 内原
  and 赤塚. Not a drawn line; its trains count in the Jōban stretch's service.
- **Cut at the line** (named by N03 municipality at build): the Jōban 77
  beyond (other prefectures 51, 日立市 5, 北茨城市 3, 取手市 3, 土浦市 3, …), the
  Suigun 44 (other prefectures 19, 那珂市 9, 常陸大宮市 6, 大子町 5, 常陸太田市 3,
  ひたちなか市 2), the Ōarai Kashima Line 12 (鉾田市 6, 鹿嶋市 5, 大洗町 1).
- **The light-rail/rail test**: all three are heavy rail (N02 class 11 and
  12). No tram, monorail or light rail.
- **The stub test.** The Suigun Line keeps **one station of 45, 水戸, its
  terminus**, with 3.8 km of track inside the city before it crosses the Naka
  River into ひたちなか市. It is a JR line, so the standing call draws it as cut
  and **no owner question arises** (Akita's Oga Line); 水戸 keeps its ring
  through the Jōban and Kashima Rinkai in any case. ⚠️ At build: its permanent
  label and legend entry on a 3.8 km stretch (measure placement in a scratch
  render). The Jōban's 4 of 81 is a main line cut at the line; the Ōarai
  Kashima Line keeps 3 of 15.
- **偕楽園 (Kairakuen) is a seasonal station.** JR East's timetable index for
  it (`timetables.jreast.co.jp/timetable/list0415.html`, read 2026-10-06)
  lists its six direction rows with **every day-type cell inactive and no
  timetable page**: no train stops there in the October 2026 timetable. It is
  JR's temporary station for the plum season at the Kairakuen garden
  (ASSERTED: JR East's station page `www.jreast.co.jp/estation/stations/415.html`
  and its `info.aspx` both answered **HTTP 403** to the project user-agent, a
  refusal recorded and not retried). N02 files it as an ordinary 常磐線
  station 1.9 km west of 水戸: **open call 1**.
- **Frequency, READ 2026-10-06** by plain GET with the project user-agent,
  every departure counted (marked trains included, the whole-page reader
  `jre_read.py`; the probe's reader in `japan_j10` matches minutes only):

  JR East, October 2026 timetable (`timetables.jreast.co.jp`, weekday pages):

  | Station (line, direction) | Weekday departures | Per hour 07-18 |
  |---|---|---|
  | 水戸 (Jōban, to いわき) | 107 | 4-8 |
  | 水戸 (Jōban, to 土浦・上野) | 76 | 4-6 |
  | 水戸 (Mito Line, to 下館・小山, over the Jōban) | 19 | 1 |
  | 水戸 (Suigun, to 常陸太田・郡山) | 26 | 1-2 |
  | 赤塚 (Jōban, to 水戸 / to 土浦; Mito Line, to 小山) | 56 / 44 / 19 | 2-5 / 2-4 / 1-2 |
  | 内原 (Jōban, to 水戸 / to 土浦; Mito Line, to 小山) | 53 / 41 / 19 | 2-5 / 2-3 / 1-2 |
  | **偕楽園** | **0** (no timetable in October) | 0 |

  Kashima Rinkai, the 2026-03-14 timetable (`www.rintetsu.co.jp/timetable`,
  one table per direction, no day-type split):

  | Station | Trains toward 水戸 / toward 鹿島神宮 | Per hour 07-18 |
  |---|---|---|
  | 水戸 | 36 (arrivals) / 36 | 2-3 / 1-3 |
  | 東水戸 | 36 / 36 | 1-3 |
  | 常澄 | 36 / 36 | 1-3 |

  **No stretch in service is at or under about 11 trains a day** (call 86):
  the thinnest is the Suigun from 水戸, 26. The master row's "Jōban every
  11-15 minutes" holds at 水戸 only: at 赤塚 and 内原 the Jōban and Mito Line
  together give 39-40 departures toward 友部 and 35 toward 水戸 in 07-18,
  about every 18-21 minutes. **Kashima Rinkai was ASSERTED in the band row;
  it is READ here** (about two an hour all day). Only counts are recorded,
  never a timetable on the page.
- ⚠️ **Gate 3** at build: JR East's and Kashima Rinkai's station lists inside
  the city (Jōban 4 or 3, Suigun 1, Ōarai Kashima 3). **OSM `name:en`** for the
  groups (one Overpass query at build, in the box below; not queried here).

## Scope

**Mito City.** The Jōban runs on to 日立 and いわき north and 土浦 and 上野
south, the Suigun to 常陸大宮 and 郡山, the Ōarai Kashima Line to 大洗 and 鹿島神宮;
cut at the line.

## Licences — as stated; the city's read is pending

- **The city's lists**: the dataset page states 「ライセンス CC-BY」 and 「コピーライト
  水戸市役所」, **no version number**; the site's terms page is リンク・著作権・免責事項
  (`/page/18265.html`). **A licence-read agent reads the city's terms
  separately; staging records its verdict and the credit wording.** No
  verdict is written in this brief.
- **MHLW open data** (the food source): **PDL 1.0 as recorded** in
  `docs/data_sources/japan.md` (Kurume's and Okayama's rows). **MUST
  DISPLAY**:
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; link the top page only. **MUST NOT**: present it as
  MHLW's own; MHLW's logo; claim completeness or accuracy.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **JR East's and Kashima Rinkai's timetables**: read for counts only,
  never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **MHLW's 法人名** is filled on 4,341 of 6,301 open rows, a company marker on
  2,621: the rest hold a sole trader's own name. Step 2 reads it IN MEMORY for
  the name rule only (`REQUIRED_COLUMNS`, Kurume's config) and never writes
  it. **法人番号, 法人住所 and 営業施設電話番号 are never selected.**
- **The registers carry 営業者氏名 on every row** (no company marker: barbers
  234 of 258, beauty 606 of 821, general laundries 28 of 48, pick-ups 27 of
  69) and **代表者氏名** on 26, 215, 20 and 43: both read IN MEMORY by the name
  rule, never written. **施設電話番号** (filled on 41, 322, 16, 18; the city
  already withholds personal mobiles) is never selected: select 屋号 and
  施設所在地 only.
- **The name rule, measured in memory** (answers only, never a value): MHLW
  **14 rows** whose trade name is the 法人名's own name (version 2's
  operator comparison), **1 of them a placeable storefront**, 0 bare
  personal names; beauty **1** row by the operator comparison, 0 bare; barbers
  and laundries 0. `japan_step2` spreads a flag to every row sharing its block
  and trade name.
- Run `check_personal_exposure.py mito` (`japan=True`) after step 2: it must
  print 0. Record the verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kantō after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 140.322-140.587 E, centroid 140.436:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded
out: (36.29, 140.31, 36.47, 140.60). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at build
from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band A with six
station groups, one under the smallest built page (call 129); food from MHLW
alone (Kurume's shape; downloads call 147); MHLW's notifications as partial
Food shops (127b), its own point where the join misses (127c), the food share
stated (125); `mode: metro`; the minor tier and Japan East (Kantō after the
retag); the Suigun Line drawn as cut from 水戸 (standing call, a JR stub); no
frequency floor.

**Answered by the owner on 2026-10-06:** call 156, **偕楽園 left out** (a seasonal station, the Sagano and Mojikō Retro precedents), so 5 station groups; call 157, **the food share in two figures together**: MHLW holds about 91% of permits, and about one fixed restaurant in five withholds its address. The recommendations below are kept as the record.

**Weighed, with a recommendation:**

1. **偕楽園, the seasonal station.** (a) **Leave it out** (recommended): no
   train stops there in the October 2026 timetable, so a ring would mark
   access that exists only in the plum season; the project already leaves
   seasonal service out (Kyoto's Sagano scenic line; Kitakyushu's Mojikō
   Retro trolley, "left out on Kyoto's Sagano precedent"). The page says so
   in its stations bullet. The map then has **5 station groups, two under the
   smallest built page**. (b) Keep it, with a note that it opens in the plum
   season only: 6 groups, as the band row was approved. *Tradeoff*: a smaller
   page against a ring that misstates year-round service; the Jōban is drawn
   through 偕楽園 either way.
2. **The food share, worded** (call 125 applies; the figure is the owner's
   to see): *recommend* stating that MHLW's file holds about 91% of the
   city's restaurant permits and that about one fixed restaurant in five
   withholds its address (Kurume's and Hiroshima's wording), against the
   alternative of the single figure 65% (placed of official). The tradeoff is
   two numbers that explain the gap against one that is shorter.

## What the build must still measure

- ⚠️ **Lapsed permits** (a shared-code proposal, not a Mito edit): MHLW keeps
  a permit open past its 許可満了日 for a while (80 permits ended before the
  file's 2026-08-31, 16 of them addressed restaurants). Propose that step 2
  drop an MHLW row whose 許可満了日 is before the file's as-of
  (`japan_register.in_term` exists), then re-run every MHLW-sourced city
  (Kurume, Okayama, …) under `drift_check.py`.
- ⚠️ **Shared code, optional** (each followed by the Minato control and every
  city screen): the 3-character-大字-plus-小字 fallback (with Ichinomiya's
  short-大字 rule); 宮町 / 泉町 without 丁目; `shared_points` and spelling
  variants of one 大字. None changes Mito's page much (0.2% unplaced after the
  fallback).
- `SOURCE_LINKS` for the four registers by link text; `SOURCE_AS_OF`
  2026-07-02; `SOURCE_ENCODING` `cp932` for the city files, `utf-8-sig` for
  MHLW; `SOURCE_KIND` for the two laundry files; `ADDRESS_BY_CONSENT` and
  `OWN_POINT_FALLBACK` = {"mhlw"}; MHLW's `as_of` from provenance (no date in
  the file; newest 許可年月日 2026-08-31).
- The census ratio (1.40) and its reading; the factory share; open call 1
  before step 1 (`LEFT_OUT_STATIONS` or the line's station list, whichever
  the shared step 1 offers; Kitakyushu's config is the nearest precedent for
  a seasonal leave-out).
- The Suigun label on its 3.8 km stretch; gate 3; OSM `name:en`; line
  colours on both basemaps; the opening view (`map-view`);
  `check_provenance.py`; `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "mito-registers-page",
    "claim": "The city's 生活衛生関係施設一覧 page lists the barber, beauty, general-laundry and pick-up-counter files as of 2026-07-02 (71286-71289), says closed premises may remain, and states CC-BY",
    "kind": "http_contains",
    "url": "https://www.city.mito.lg.jp/site/open-data/4496.html",
    "present": ["施設一覧（理容所）（令和８年７月２日現在）", "施設一覧（美容所）（令和８年７月２日現在）", "施設一覧（クリーニング所・一般）（令和８年７月２日現在）", "施設一覧（クリーニング所・取次店）（令和８年７月２日現在）", "71286.csv", "71287.csv", "71288.csv", "71289.csv", "すでに営業していない施設も含まれている場合があります", "CC-BY"]
  },
  {
    "id": "mito-barber-file",
    "claim": "The barber list (23,221 B, 258 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.mito.lg.jp/uploaded/attachment/71286.csv",
    "min_bytes": 18000
  },
  {
    "id": "mito-beauty-file",
    "claim": "The beauty-salon list (84,749 B, 821 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.mito.lg.jp/uploaded/attachment/71287.csv",
    "min_bytes": 70000
  },
  {
    "id": "mito-laundry-file",
    "claim": "The general-laundry list (4,959 B, 48 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.mito.lg.jp/uploaded/attachment/71288.csv",
    "min_bytes": 4000
  },
  {
    "id": "mito-pickup-file",
    "claim": "The laundry pick-up-counter list (8,000 B, 69 rows) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.mito.lg.jp/uploaded/attachment/71289.csv",
    "min_bytes": 6500
  },
  {
    "id": "mito-food-page-points-to-mhlw",
    "claim": "The city's food page holds no file and sends readers to MHLW's newer data (Kurume's shape)",
    "kind": "http_contains",
    "url": "https://www.city.mito.lg.jp/site/open-data/3745.html",
    "present": ["食品営業許可施設一覧", "最新のデータが厚生労働省のホームページにて公開されております"]
  },
  {
    "id": "mito-mhlw-live",
    "claim": "MHLW's open-data file for Mito (08201), the food source (2,138,515 B), answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=08201_food_business_all.csv",
    "min_bytes": 1800000
  },
  {
    "id": "mito-isj-block-live",
    "claim": "MLIT's block-level address file for Mito (08201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/08201-24.0a.zip",
    "min_bytes": 400000
  },
  {
    "id": "mito-isj-chome-live",
    "claim": "MLIT's town-chōme file for Mito (08201) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/08201-19.0b.zip",
    "min_bytes": 6000
  },
  {
    "id": "mito-jr-mito-timetable",
    "claim": "JR East's timetable index for 水戸 (list1471) links the weekday pages read: Jōban down (1471010) and up (1471020), Mito Line (1471030), Suigun (1471040). ASCII ids only: the host sends no charset",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1471.html",
    "present": ["tt1471/1471010.html", "tt1471/1471020.html", "tt1471/1471030.html", "tt1471/1471040.html"]
  },
  {
    "id": "mito-jr-akatsuka-timetable",
    "claim": "JR East's timetable index for 赤塚 (list0033) links its Jōban down (0033010) and up (0033020) and Mito Line (0033030) weekday pages",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0033.html",
    "present": ["tt0033/0033010.html", "tt0033/0033020.html", "tt0033/0033030.html"]
  },
  {
    "id": "mito-jr-kairakuen-no-service",
    "claim": "JR East's timetable index for 偕楽園 (list0415) has every day-type cell inactive and links no timetable page in the current timetable: the seasonal station (open call 1). A failure here may mean the plum season's timetable is live: re-read",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0415.html",
    "present": ["class=\"inactive\""],
    "absent": ["tt0415/"]
  },
  {
    "id": "mito-rintetsu-timetable",
    "claim": "Kashima Rinkai's timetable page carries the 2026-03-14 timetable with 水戸, 東水戸 and 常澄 (36 trains each way, read 2026-10-06)",
    "kind": "http_contains",
    "url": "https://www.rintetsu.co.jp/timetable",
    "present": ["2026年3月14日改正", "東水戸", "常澄"]
  },
  {
    "id": "mito-projected-crs",
    "claim": "Mito projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.44,
    "expect": "EPSG:32654"
  }
]
```
