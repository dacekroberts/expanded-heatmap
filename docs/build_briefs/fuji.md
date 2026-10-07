# Fuji — build brief

**Band B, personal services only, owner-approved 2026-10-06** (call 119; the
master list's row: "Personal services only (Kōchi's shape)"; staging's
`docs/decisions_drafts/staging.md`, "Wave 5, second half": "Fuji (personal
services, a licence read)"). The Step 0 downloads were approved by the owner
2026-10-06 (call 174). **Step 0 measured 2026-10-06** (staging). Into
`data/fuji/raw/` (gitignored), each from the publisher's own host with the
project user-agent, each finally HTTP 200, under `<dataset>_<resource id>_<the
resource's own name>`:

- From `opendata.pref.shizuoka.jp` (静岡県オープンデータ, author 衛生課), datasets
  **11261** 理容所台帳, **11262** 美容所台帳 and **11263** クリーニング所台帳: each
  dataset's **full list as of 2026-03-31** (179,680 B, 506,468 B and 126,395 B)
  and **every monthly new-permit file after it, April to August 2026** (barber
  5, beauty 6, laundry 5; 133 B to 8,316 B each): **19 files, 862,513 B**.
  ⚠️ The portal answered **HTTP 429** to the nineteenth request (the August
  laundry file, about 40 s into a run spaced 2 s apart); one retry more than
  60 s later answered 200. Not a refusal of the agent; the build's fetch spaces
  its requests (5 s or more) and waits 60 s on a 429.
- Already cached, not re-fetched: `22000_food_business_all.csv` (16,196,764 B,
  MHLW, the food measurement below) and `isj/22210-24.0a.zip` (370,149 B) and
  `isj/22210-19.0b.zip` (7,711 B) from `nlftp.mlit.go.jp`.

Nothing else was downloaded. For rail counts, the probe's JR Central station
PDFs and Gakunan's weekday timetable PDF (already in the wave-5 scratch
`japan_j1/`) were read again; no new timetable file was fetched.

**Run `python scripts/brief_check.py fuji` before writing any code.** Then
the `japan-city` skill, **Kōchi's shape** (`docs/build_briefs/kochi.md`:
personal services only, food off), **Matsue's for three registers with the
laundry kinds** (`docs/build_briefs/matsue.md`) and **Ichinomiya's for a full
list plus its months** (call 126). Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Fuji entry; its table is shared code
and was not edited). Rail: MLIT N02-25 cut at the N03 city line, through
`pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; 新富士 is dropped); (2) **lines served only by limited expresses
DO count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left out,
its station kept through the other lines, and drawn cut only where no other
line serves that station (owner, 2026-10-06, calls 54, 92, 163 and 165; moot
here, no line is a stub); (4) **菓子製造業 and そうざい製造業 count, in Retail**
(2026-09-24; moot on a personal-services page); (5) **the name rule**, version
2 (2026-10-06); (6) **no page says "currently operating"**. Also: **no
frequency floor** for JR or private lines in Japan (call 46), any stretch at
about 11 trains a day or fewer named and drawn (call 86; none here); fault-based
cost clauses accepted for all of Japan (2026-09-24); English station names from
OSM `name:en`; every Japanese city reads `WAVE2_RULES` (2026-10-04).

**✅ Rules decided 2026-10-06, applied (do not re-ask):** expired permits
dropped (161; these registers carry no expiry, nothing to drop); an address
that is the city name alone is not a premises (162; 0 rows); a permit that
starts after the as-of is dropped until it is in term (172; 0 rows); tiers
disclosed where the block share is low (145; not needed at 96.0%); the full
list kept whole plus its monthly files (126).

**✅ Food left out (owner, call 119, the band row).** Measured earlier
(staging, 2026-10-06, the master-list row): MHLW's 22000 file places about 41%
of the estimated restaurants in Fuji, at most 67%, under the 70% line. Not
re-opened here.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Fuji
carries `label_tier: "minor"` and goes in the **Japan East** view
(`app/cities.py`), as Shizuoka's brief has it; wave 4's first city to land
retags Japan into the eight regions, Fuji into **Chubu**. Its label offset
comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never
by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 and Matsue's,
Matsumoto's and Takamatsu's precedent: no subway, tram or light rail is drawn;
JR Central (7 station groups) and the Gakunan Railway (10, a railway, N02
class 12) are both heavy rail, so the mode follows the backbone.

---

## The one-line summary

**Personal services only, from Shizuoka Prefecture's three 生活衛生 registers
(CC BY 4.0 by the portal's §4, as read by staging): barbers 212, beauty salons
539 and laundries 92 (31 general, 61 pick-up counters), the 2026-03-31 lists
plus new premises to 2026-08-31. Across the prefecture's jurisdiction the
lists hold 97.1%, 99.6% and 93.4% of e-Stat's in-force counts; for Fuji alone
no official count exists, and a census estimate reads about 100%, 89% and
78%. Block join 96.0%, 2.7% at a town or 大字 centroid, 1.3% unplaced.** No
food (MHLW places at most 67%). **Rail: 17 N02 station groups**: JR Central's
Tōkaidō Line 4 (about 3 an hour) and Minobu Line 5 (about 2 an hour), the
Gakunan Railway 10 (36 to 37 weekday trains each way, about every 30 minutes),
吉原 and 富士 shared; no stretch at or under about 11 a day.

---

## Business leg — Shizuoka Prefecture's 生活衛生 registers (衛生課)

### Where the prefecture publishes

`https://opendata.pref.shizuoka.jp` (静岡県オープンデータ) carries one dataset per
kind, author 衛生課, each holding the **full list as of 31 March** (refreshed
about 30 April each year: 「３月31日時点の…開設届出台帳に掲載されている…全施設
（廃止、みなし廃止施設を除く。）の一覧」) and **one file of the previous month's new
premises** (about the 15th of each month). Every resource is marked
`表示（CC BY）`. Each dataset page states that **政令市 (静岡市, 浜松市) are
excluded**, that the operator column holds **a company's name where the
operator is a company** (「営業者氏名については、法人の場合は法人名を記載しています」),
and that a facility may ask 衛生課 to stop publication of its entry.

| Dataset (`/dataset/<n>.html`) | Full list (resource id) | Bytes | Prefecture rows | Fuji rows | Months Apr-Aug (Fuji) | Fuji, 2026-08-31 |
|---|---|---|---|---|---|---|
| 11261 理容所台帳 | **855060** 理容所施設一覧（令和８年３月31日時点）.csv | **179,680** | 2,009 | **211** | +1 (August) | **212** |
| 11262 美容所台帳 | **855063** 美容所施設一覧（令和８年３月31日時点）.csv | **506,468** | 5,244 | **534** | +5 (June 3, July 1, August 1) | **539** |
| 11263 クリーニング所台帳 | **855059** クリーニング所施設一覧（令和８年３月31日時点）.csv | **126,395** | 1,200 | **93**: 取次所 61, クリーニング所（一般） 31, 無店舗取次所 1 | +0 | **92 premises** |

Monthly resources fetched (ids): barber 854471, 855027, 857430, 857849,
859043; beauty 855979 (April, the 0702 replacement), 855036, 857434, 857848,
857854, 859045; laundry 854473, 855025, 857432, 857850, 859042. The full-list
fs URLs: `/fs/8/5/5/0/6/0/_/__________8_3_31____.csv`,
`/fs/8/5/5/0/6/3/_/__________8_3_31____.csv`,
`/fs/8/5/5/0/5/9/_/______________8_3_31____.csv`.

- **cp932 CSV**, a title row (理容所 / 美容所 / クリーニング所), a blank row, then
  the header. Columns (names only): Ｎｏ．, **理容所名称** / **美容所名称** /
  **クリーニング所名称**, **…所在地**, …電話番号, **開設者氏名**, 業種 (barber and
  beauty: the kind's own name on every row) or **種別** (laundry: 取次所,
  クリーニング所（一般）, 無店舗取次所), 確認年月日, 確認番号, 管轄保健所. Fuji's rows
  are all under 管轄保健所 富士.
- **Against the shared tuples**: 理容所所在地 and 美容所所在地 are in `ADDR_COLS`,
  理容所名称 and 美容所名称 in `NAME_COLS`, 開設者氏名 in `OPERATOR_COLS`, 種別 and
  業種 in `TYPE_COLS`. ⚠️ **`ADDR_COLS` lacks クリーニング所所在地** (it holds
  クリーニング所在地), so `city_rows` finds no header in the laundry list today;
  ⚠️ **`NAME_COLS` lacks クリーニング所名称**. The scratch measurement renamed both
  in memory; the build adds them to the shared tuples (each after every older
  spelling) and re-runs the Minato control.
- ⚠️ **The monthly files are not one shape**: June's barber file puts 確認年月日
  before 業種, May's laundry file names its date and number 届出年月日 and
  届出番号, and the June and July files pad each row to 248 columns. Read by
  header name, never by position. A month with nothing new holds one row
  reading 該当なし (no address): read as no rows.
- ⚠️ **July's beauty file exists twice** (857848 and 857854, same name, 11
  rows each, 9 identical, 2 differing; Fuji's one July row identical in both).
  The portal's API (read 2026-10-06) lists both; **the dataset page links only
  857854**: the build pins 857854. April's beauty file was replaced on 2026-07-02 for a phone-number
  error (phones are never read). De-duplicate across the months by (address,
  trade name).
- **Filter by address, never by health centre**: 富士保健所 covers 富士市 and
  富士宮市 (312 barbers, 831 salons, 133 laundries in all), and one of its beauty
  rows writes 富士宮 with no 市. The filter is an address starting 富士市 (with or
  without 静岡県); no Fuji row names another health centre and no other row
  carries 富士市 later in its address.
- **Dates** (確認年月日): wareki with a one-letter era (S, H, R and y.m.d), Fuji's
  rows from 1989 and earlier to 2026-02-12 in the full lists, and 2026-06-10
  to 2026-08-18 in the months. ⚠️ **`japan_register.wareki_date` reads H and R
  but not S**: 90 barber, 70 beauty and 19 laundry rows read no date. Moot
  today (no expiry column, nothing filtered on the date); proposed for shared
  code if a build filters on it.
- **Closures**: the full list excludes 廃止 and みなし廃止 as of 2026-03-31; the
  months list openings only, so a closure since March is invisible until the
  2027 list (about 2027-04-30). The page keeps "may include closed premises".
- **Expired, empty or city-only addresses**: no expiry (開設確認 has no term,
  call 161 drops nothing); **0** addresses that are 富士市 alone (call 162); 0
  empty addresses; **0** rows starting after their file's as-of (call 172:
  the full lists end 2026-02-12, the months' rows are within their months).
- **Duplicates**: 確認番号 repeats (barbers 202 distinct of 211, 5 empty; beauty
  492 of 534, 4 empty; laundries 93 of 93): never a key alone; (確認番号,
  確認年月日) is unique in every file. 0 repeats by (address, trade name) in any
  list; by address alone barbers 1, beauty 6, laundries 3 (shared buildings).
  **17 beauty addresses are also barber addresses, 5 with the same trade
  name** (理容所美容所重複開設): one pin per premises and bucket keeps one of
  those 5, so the map shows **838 pins** from 843 premises.
- **Not premises**: the 1 無店舗取次所 (`japan_eigyo`: "storeless pick-up (not a
  premises)"); no 移動, 一円 or 保健所管 address and no 移動 trade name.
- **Linen supply**: the 種別 column carries no リネン kind. **2 general laundries
  carry リネン in their trade name and 4 carry 工場**: kept, as the module reads
  the kind, not the name (its 一般リネン兼業 stays; Funabashi kept its 8 工場
  names). **4 trade names name a facility** (barbers 病院 1 and 福祉 1, beauty
  病院 1, laundry 1): read them at build against Sapporo's welfare-facility
  rule (which today reads a type, not a name).

### Coverage — against e-Stat and the Economic Census

**e-Stat has no Fuji row** (衛生行政報告例 第10表 and 第11表 list prefectures,
指定都市 and 中核市 only; Fuji is neither). The prefecture's jurisdiction is
静岡県 less 静岡市 and 浜松市, exactly what the lists cover
(`data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
`…_cleaning_by_city.csv`, in force 2025-03-31; the lists are a year newer):

| Kind | e-Stat FY2024, jurisdiction (静岡県 − 静岡市 − 浜松市) | The prefecture's lists, 2026-03-31 | Share |
|---|---|---|---|
| Barbers | 3,484 − 690 − 726 = **2,068** | **2,009** | **97.1%** |
| Beauty salons | 9,039 − 1,731 − 2,042 = **5,266** | **5,244** | **99.6%** |
| Laundries (premises) | 1,982 − 312 − 396 = **1,274** (取次所 864, general 410) | **1,190** (取次所 803, general 387) | **93.4%** (92.9%, 94.4%) |
| 無店舗取次店 (operators) | 28 − 2 − 5 = 21 | 10 | not premises |

**Per city, an estimate only** (Sakura's and Ichihara's method; never for the
page unless the owner asks, Ichikawa's call 32): the 2021 Economic Census
(`data/japan/raw/estat_census_r3_b1_009_1a.xlsx`; 22210: 782 理容業 **172**,
783 美容業 **382**, 781 洗濯業 **80**), scaled by the jurisdiction's
licensed-to-census ratios (barbers 2,009 / 1,637 = 1.227, beauty 5,244 /
3,296 = 1.591, laundries 1,190 / 811 = 1.467, over the jurisdiction's 33
municipalities):

| Kind | Estimate | The lists, 2026-08-31 | Share |
|---|---|---|---|
| Barbers | about 211 | 212 | **100%** |
| Beauty | about 608 | 539 | **89%** |
| Laundries | about 117 | 92 premises | **78%** |

- A cruder check on the census's whole 78 洗濯・理容・美容・浴場業: Fuji's lists
  hold 1.156 premises per establishment, **11th of the jurisdiction's 33
  municipalities** (range 0.861 to 1.794, median 1.263). Fuji's share of the
  jurisdiction is 10.5% of its barbers and 10.2% of its salons.
- ⚠️ **Laundries look thin, as Ichikawa's (80%) and Ichihara's (81%) did**,
  and beauty somewhat thin; the cause is not known (consent: facilities may
  ask to be left off; closures since 2021; or what the census counts). Open
  call 1.

### Food — left out

- **MHLW's file (22000, the prefecture's jurisdiction)**, cached 2026-10-06,
  `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=22000_food_business_all.csv`
  (16,196,764 B): places about 41% of Fuji's estimated restaurants, at most
  67% (staging's measurement, 2026-10-06, the master-list row), under the 70%
  line. Food stays off this page (call 119); **not proposed**. MHLW lists no
  salons, so call 127c's own-point fallback has nothing to use.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless): ✅ 96.0% at the block

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/22210-24.0a.zip` (370,149 B,
64,772 rows, 1,406 of them 住居表示; **54,682 block keys**, 194 towns),
town-chōme `.../19.0b/22210-19.0b.zip` (7,711 B, **198** towns).
`japan.CITIES` entry at build: `"fuji": {"name": "富士市", "pref": "22",
"epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless": True, "wards":
["22210"]}`.

**Measured 2026-10-06** (scratch `fuji/measure.py`: `permits_from_rows`,
`load_city_isj` and `join_city` with `WAVE2_RULES` unchanged; the two laundry
columns renamed in memory; no normalisation changed, so no Minato re-run was
needed), on the 843 fixed premises (the full lists plus the months, the
無店舗取次所 out):

| Kind | Premises | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|---|
| Barbers | 212 | **207 (97.6%)** | 1 (0.5%) | 4 (1.9%) |
| Beauty salons | 539 | **518 (96.1%)** | 16 (3.0%) | 5 (0.9%) |
| Laundries | 92 | **84 (91.3%)** | 6 (6.5%) | 2 (2.2%) |
| … クリーニング所（一般） (31) / 取次所 (61) | | 87.1% / 93.4% | 9.7 / 4.9 | 3.2 / 1.6 |
| **All personal services** | **843** | **809 (96.0%)** | **23 (2.7%)** | **11 (1.3%)** |

**The misses, read** (towns only; no address or number printed):
- **The chōme shift** (town + first number read as 丁目) placed 72 rows
  (今泉, 国久保 and the other 丁目 towns written as 地番-style numbers).
- **Chōme tier, 18 in towns MLIT keys whose 地番 it lacks** (青島町 3, 大渕 2,
  前田, 南町, 青葉町, 三ツ沢, 鷹岡本町, 宇東川東町, 国久保3丁目, 本市場町, 水戸島本町,
  中之郷, 蓼原, 鮫島, 伝法字久保田): Kakogawa's shape. **5 are 字 addresses**
  (中里字鬼ケ島 2, 原田字滝川, 蓼原字片宿, 松岡字新田) placed at the 大字 centroid,
  since 24.0a keys no block under those 小字.
- **Unplaced (11), each a proposed shared rule** (measured in
  `fuji/measure3.py`, not applied; each change re-runs the Minato control,
  `screen_japan_join.py minato` 98.0 / 0.2 / 1.8, and every city screen):
  (a) **a two-character 大字 followed by a 通称** (岩渕上町, 厚原西, 伝法桜ケ丘,
  今泉水深, 大渕城山, 大野新町): `known_town`'s prefix match needs 3 characters;
  allowing 2 only where the 地番 then hits a block places 5 at the block (大野新町
  would take 大野's centroid); (b) **町 written after a town MLIT names bare**
  (比奈町 → 比奈, 神谷町 → 神谷), the reverse of Nara's `machi` rule: 2 at the
  block; (c) **の for 之** (米の宮町 → 米之宮町): 1 at the block. Together
  **block 817 (96.9%), chōme 24, unplaced 2** (東比奈 and 東比奈2丁目, a town
  absent from both MLIT files: GSI's address search or unplaced).
- **Independent check** at build: GSI's address search on a sample
  (`screen_japan_join.py`'s `gsi_check`, Sendai's way: 150 rows, 1 request a
  second), weighted to the centroid tier and any row rule (a) places.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_22_GML.zip`, N03 code 22210
(**245.0 km²**, extent W 138.558, S 35.116, E 138.812, N 35.359; the 2008
merger brought in 富士川町). Read with `stub_test()`'s method and an in-memory
`CITIES` entry (scratch `fuji/rail.py`, through `heavy_job.py`, peak 0.15 GB).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 東海道線 (東海旅客鉄道, 11) | JR Tōkaidō Line | **4 / 89** | 東田子の浦, 吉原, 富士, 富士川 |
| 身延線 (東海旅客鉄道, 11) | JR Minobu Line | **5 / 39** | 富士, 柚木, 竪堀, 入山瀬, 富士根 |
| 岳南鉄道線 (岳南電車, 12) | Gakunan Railway Line | **10 / 10** | 吉原, ジヤトコ前, 吉原本町, 本吉原, 岳南原田, 比奈, 岳南富士岡, 須津, 神谷, 岳南江尾 |

- **19 station records, 17 N02_005g groups** (富士: Tōkaidō and Minobu, 0 m;
  吉原: JR and Gakunan, 142 m apart, one group). No name in two groups.
  **Median nearest-station gap 1,024 m** (311 to 2,585); pairs closer than
  600 m: 本吉原 / 吉原本町 311 m, 吉原本町 / ジヤトコ前 335 m, 本吉原 / ジヤトコ前 531
  m (Gakunan's town-centre stretch). Rings by the spacing rule at build.
- **Shinkansen**: 新富士 (Tōkaidō Shinkansen), dropped by `japan.stations()`.
- **Cut at the line**: the Tōkaidō Line 85 beyond (静岡市 10, 浜松市 5, 沼津市 3
  and other Shizuoka municipalities, 48 in other prefectures), the Minobu Line
  34 (富士宮市 6, 山梨県 28). The Gakunan Railway runs wholly inside the city.
  富士根 sits 157 m inside the city line, 吉原 177 to 214 m.
- **The light-rail/rail test**: all three are heavy rail: JR conventional
  (class 11) and the Gakunan Railway a private railway (class 12, 普通鉄道).
  No tram or light rail.
- **The stub test**: no line is cut to a stub (Tōkaidō 4 stations, Minobu 5,
  Gakunan whole). No one-station rule applies.
- **Frequencies, READ by the wave-5 probe (2026-10-06) from the operators' own
  timetables**, re-read here from the same files: JR Central's station PDFs
  (`https://railway.jr-central.co.jp/time-schedule/srch/_pdf/data/202603/`
  `tokaido_Fuji_B_wh_u.pdf`, `tokaido_Yoshiwara_B_wh_d.pdf`,
  `minobu_Tatebori_B_wh_u.pdf`; the 2026-03 timetable): **the Tōkaidō Line
  about 3 trains an hour, the Minobu Line about 2**. Gakunan's weekday
  timetable (`https://www.gakutetsu.jp/timetable/`, `2026heijitsu.pdf`,
  revised 2026-03-14): **36 to 37 weekday trains each way, about every 30
  minutes** (counted on its through rows from 6:07 to 22:10). **No stretch at
  or under about 11 a day** (call 86 names none). The JR PDFs' layout text
  interleaves the route diagram with the hour rows, so the JR figures stay as
  the probe read them, per hour, not as daily counts.
- ⚠️ **Gate 3** at build: JR Central's station counts inside the city (Tōkaidō
  4, Minobu 5, 富士 shared) and Gakunan's own station list (10). **OSM
  `name:en`** for 17 groups (one Overpass query at build, in the box below;
  not queried here); ジヤトコ前 is N02's spelling of the station Gakunan signs
  ジヤトコ前 (Jatco-mae).

## Scope

**Fuji City.** The Tōkaidō Line runs on to 沼津 and 静岡, the Minobu Line to
富士宮 and 甲府, cut at the line; the Gakunan Railway is whole. ⚠️ The city's
extent (245 km², north up the slopes of 富士山 to 35.36 N) is larger than its
urban area: the opening view must fit the stations and premises, not the N03
polygon (`map-view` at build). Food is out (above); the laundry kinds are
kept (取次所 and general), the 無店舗取次所 out.

## Licences — as read by staging

**Shizuoka Prefecture's open-data portal (datasets 11261-11263): PERMITTED
WITH CONDITIONS**, read by staging on 2026-10-06 (the master list's row;
staging records it in `docs/decisions_drafts/staging.md`; the build copies the
row into `docs/data_sources/japan.md` from staging's record): **CC BY 4.0 by
the portal's §4**, with the portal's **prescribed modified-use credit**; each
resource is marked `表示（CC BY）`. **The portal's §6 was accepted by the owner**
(call 144): its reimbursement sentence is fault-based, and its own-cost
sentence is Fukushima's class. ⚠️ **The liabilities review flagged §6 as read
two ways in different briefs** (purely fault-based on 2026-10-05, two sentences
on 2026-10-06); Cleanup is reconciling that. No verdict is written in this
brief beyond staging's record; take the exact credit wording from it. Link
`opendata.pref.shizuoka.jp`'s dataset pages.

- **MHLW open data**: measured only; not a source on this page.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the **Economic Census**:
  measurement sources, not drawn. **JR Central's and Gakunan's timetables**:
  read for counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **開設者氏名 holds a person or a company** (the dataset pages: a company's
  name where the operator is a company): a company or cooperative marker on 15
  of 211 barbers, 107 of 534 beauty salons and 60 of 93 laundries in the full
  lists (2 of the 5 new beauty rows); **the rest, 196, 427 and 33 rows, carry
  no marker** (the shape of a sole trader's own name). It is read in memory
  for the name rule only and never written. **The phone columns are dropped at
  read**; the lists carry no operator address. Select the trade name, the
  address and the laundry kind only.
- **The name rule, version 2, measured in memory** (answers only, never a
  value): **0** bare personal names among the 843 trade names; **0** trade
  names equal to their operator.
- A facility may ask 衛生課 to be left off the list (the dataset pages); a
  removal request to this project is honoured as CLAUDE.md says.
- Run `check_personal_exposure.py fuji` (`japan=True`) after step 2: it must
  print 0. Record the verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Chubu after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 138.558-138.812 E, centroid 138.699:
project to **UTM 54N (EPSG:32654)**, computed here (Hamamatsu, west of 138 E,
is 53N; never copied). OSM box from the N03 extent, rounded out: (35.11,
138.55, 35.36, 138.82). Scaffold with `scripts/scaffold_city.py ...
--page-number <N>`, the number claimed at build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band B, personal
services only, food left out (call 119); the downloads (call 174); the full
list plus its months (126); calls 161, 162 and 172 (nothing dropped by them
here); `mode: metro`; the minor tier and Japan East (Chubu after the retag);
no frequency floor; the portal's §6 (144); a kind that reads thin against a
census estimate is still built (Ichikawa's call 32, Ichihara's 123).

**Answered by the owner on 2026-10-06:** call 186, **both shares stated as
estimates**: beauty salons "about nine in ten" and laundries "about four in
five" of what the 2021 Economic Census suggests, the method named and the
reason not known (the sentence itself a review-time proposal, Ichikawa's and
Ichihara's precedent extended to beauty). The recommendation below is kept as
the record.

**Weighed, with a recommendation:**

1. **What the page says about coverage.** No official count exists for Fuji;
   the jurisdiction-wide shares are 97.1%, 99.6% and 93.4%, and the census
   estimate for Fuji alone reads about 100% (barbers), 89% (beauty) and 78%
   (laundries). Ichikawa's call 32 and Ichihara's call 123 stated a thin
   laundry share as an estimate. *Recommend the same here, extended to
   beauty*: one sentence stating that the prefecture's registers list 539
   salons and 92 laundries, about nine in ten and four in five of what the
   2021 Economic Census suggests, the reason not known (a review-time
   proposal). The tradeoff: a modelled figure on the page, against a page
   that implies completeness for two kinds the census reads short; stating
   laundries only would follow the precedent exactly but leave beauty's 89%
   unsaid.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `ADDR_COLS` + クリーニング所所在地; `NAME_COLS` + クリーニング所名称;
  optionally the three join rules above (+8 at the block) and the S era in
  `wareki_date`. City-local: the monthly files read by header name, the two
  July beauty files de-duplicated, 該当なし rows read as none, the filter by
  address (never 富士保健所).
- `SOURCE_FILES` pinned to the three full lists and the sixteen monthly
  resources with `SOURCE_AS_OF` 2026-08-31 (the newest month, never today); a
  new month is a new resource id and a re-measure; the 2027 full list replaces
  the March one.
- The 4 facility-named premises (Sapporo's rule); GSI's sample check; the 5
  barber-and-beauty premises collapsing to one pin each.
- Gate 3 (JR Central, Gakunan); OSM `name:en`; line colours on both basemaps;
  the opening view (`map-view`, the polygon larger than the urban area);
  `check_provenance.py`; `check_scope_disclosure.py` (food out, the laundry
  kinds kept, the 無店舗取次所 out).

```brief-checks
[
  {
    "id": "fuji-barber-dataset",
    "claim": "Shizuoka's portal dataset 11261 lists the barber full list as of 2026-03-31 (fs 855060) and the August 2026 monthly file, under CC BY",
    "kind": "http_contains",
    "url": "https://opendata.pref.shizuoka.jp/dataset/11261.html",
    "present": ["理容所施設一覧（令和８年３月31日時点）.csv", "/fs/8/5/5/0/6/0/", "令和８年８月新規理容所施設一覧.csv", "表示（CC BY）"]
  },
  {
    "id": "fuji-beauty-dataset",
    "claim": "Dataset 11262 lists the beauty full list as of 2026-03-31 (fs 855063), the August 2026 monthly file and the July file the build pins (857854; 857848 is not linked)",
    "kind": "http_contains",
    "url": "https://opendata.pref.shizuoka.jp/dataset/11262.html",
    "present": ["美容所施設一覧（令和８年３月31日時点）.csv", "/fs/8/5/5/0/6/3/", "令和８年８月新規美容所施設一覧.csv", "/fs/8/5/7/8/5/4/"],
    "absent": ["/fs/8/5/7/8/4/8/"]
  },
  {
    "id": "fuji-laundry-dataset",
    "claim": "Dataset 11263 lists the laundry full list as of 2026-03-31 (fs 855059) and the August 2026 monthly file",
    "kind": "http_contains",
    "url": "https://opendata.pref.shizuoka.jp/dataset/11263.html",
    "present": ["クリーニング所施設一覧（令和８年３月31日時点）.csv", "/fs/8/5/5/0/5/9/", "令和８年８月新規クリーニング所施設一覧.csv"]
  },
  {
    "id": "fuji-beauty-full-file",
    "claim": "The beauty full list (506,468 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.shizuoka.jp/fs/8/5/5/0/6/3/_/__________8_3_31____.csv",
    "min_bytes": 450000
  },
  {
    "id": "fuji-isj-block-live",
    "claim": "MLIT's block-level address file for Fuji (22210) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/22210-24.0a.zip",
    "min_bytes": 300000
  },
  {
    "id": "fuji-isj-chome-live",
    "claim": "MLIT's town-chōme file for Fuji (22210) answers keyless - the centroid tier",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/22210-19.0b.zip",
    "min_bytes": 6000
  },
  {
    "id": "fuji-jrc-tokaido-pdf",
    "claim": "JR Central's 2026-03 station timetable PDF for 富士 (Tōkaidō Line, up) answers a plain GET",
    "kind": "http_ok",
    "url": "https://railway.jr-central.co.jp/time-schedule/srch/_pdf/data/202603/tokaido_Fuji_B_wh_u.pdf",
    "min_bytes": 200000
  },
  {
    "id": "fuji-gakunan-timetable",
    "claim": "Gakunan's timetable page links the weekday and holiday PDFs of the 2026-03-14 revision",
    "kind": "http_contains",
    "url": "https://www.gakutetsu.jp/timetable/",
    "present": ["2026heijitsu.pdf", "2026kyujitsu.pdf", "2026年3月14日"]
  },
  {
    "id": "fuji-projected-crs",
    "claim": "Fuji projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 138.70,
    "expect": "EPSG:32654"
  }
]
```
