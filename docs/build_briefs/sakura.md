# Sakura — build brief

**Band B, personal services only, owner-approved 2026-10-06** (Japan wave 4,
banded in staging's "Wave 5" entry, `docs/decisions_drafts/staging.md`,
"Wave 5: the ranked queue and the pre-verdicts screened; Japan's lines carry
no frequency floor (owner)": "Urayasu, Sakura, Yachiyo and Ichihara (personal
services, Matsudo's shape)"). **Step 0 measured 2026-10-06** (staging's brief
agent), **from files already on disk; nothing was downloaded for this
brief**:

- Chiba Prefecture's three lists and the ten monthly files, fetched once into
  `data/matsudo/raw/` from `opendata.pref.chiba.lg.jp` (2026-10-05 and
  2026-10-06; resources, names and bytes in `docs/build_briefs/matsudo.md`)
  and **copied byte for byte into `data/sakura/raw/`**, as a build's
  `fetch_sources.py` would fetch them into the city's own `raw/`:
  `ichiran-riyou202503.xlsx` (328,249 B), `ichiran-biyou202603.xlsx`
  (765,694 B), `ichiran-clean202603.xlsx` (254,290 B), `shinki-biyou2604.xlsx`
  to `shinki-biyou2608-2.xlsx` and `shinki-clean2604.xlsx` to
  `shinki-clean2608.xlsx`.
- **MLIT's address blocks for Sakura (12212)**: approved by the owner on
  2026-10-06 (call 106) and fetched that day by staging's measurement agent,
  as `pipeline/countries/japan_fetch.py` fetches them, into
  `data/sakura/raw/isj/`: `12212-24.0a.zip` (160,947 B) and `12212-19.0b.zip`
  (7,690 B) from `nlftp.mlit.go.jp`. **The block join is measured: 94.2%**
  (below, "Coordinates").
- Not fetched: MHLW's prefecture file (food is off); the barber months
  (barbers get no months, Matsudo's call 34).

**Run `python scripts/brief_check.py sakura` before writing any code.** Then
the `japan-city` skill in **Matsudo's shape** (`docs/build_briefs/matsudo.md`;
Kōchi's config, `pipeline/kochi/config.py`): personal services only, the
publisher is the prefecture, every row assigned to Sakura by its sheet AND its
address. Coordinates: the `address-join` skill with the shared
`pipeline/countries/japan_register.py` (`scripts/screen_japan_join.py` has no
Sakura entry; add one at build). Rail: MLIT N02-25 cut at the N03 city line,
measured through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a JR or
private one-station stub stays as cut** (2026-09-27; wave 5 restated it,
2026-10-06), and an urban line (subway, monorail, AGT) with one station in the
city is left out (calls 54 and 92 its exceptions); (4) **菓子製造業 and
そうざい製造業 count, in Retail** (moot here); (5) **the name rule, version 2**
(`japan_register.name_is_operator`, on master 2026-10-06): a trade name that
IS the operator's own name, or is written as a bare personal name, shows its
permit type, the operator column read in memory only; (6) **no page says
"currently operating"**. Also: fault-based cost clauses accepted for all of
Japan (2026-09-24); English station names from OSM `name:en`, numerals as
figures before 丁目; every Japanese city reads `WAVE2_RULES` (owner,
2026-10-04); **no frequency floor for JR or private lines** (call 46), and any
stretch with about 11 trains a day or fewer is drawn and named (call 86).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Sakura
carries `label_tier: "minor"` and goes in the **Japan East** view as the other
Kantō cities (wave 4's first city retags Japan into the eight regions, Sakura
into Kanto). Its label offset comes from `check_macro_labels.py` (PROBLEMS 0
at 375, 768 and 1200), never by eye. **Sakura and Yachiyo share a border**
(centroids about 10 km apart; Keisei's 勝田台 sits 0.1 km beyond Sakura's
line): measure their labels together, and with Funabashi's if it lands in the
same batch.

**`mode`: open (call 2; staging recommends `metro`).**

---

## The one-line summary

**Personal services only, from Chiba Prefecture's open-data lists of barbers,
beauty salons and laundries (dataset 6, PDL 1.0), cut to Sakura by the 印旛
sheet and the address: 117 barbers (the 2025-03-31 list, built as published
with its own date, Matsudo's call 33), 256 beauty salons and 79 laundry rows
(78 premises) rebuilt to 2026-08-31 (an upper bound: closures are not
published); 451 storefronts, 446 pins.** ⚠️ **The beauty workbook's 海匝
sheet is an exact copy of 印旛**: filter on the 印旛 sheet AND the address, or
Sakura's 255 salons count twice. **The block join places 94.2% at the block**
(425 of 451; 24 at a chōme or 大字 centroid, 2 unplaced). Against a census-based estimate the lists hold about 104%, 96% and
134%. Rail: **11 N02 station groups** (Yamaman 6, Keisei 5, JR 1; ユーカリが丘 is
Keisei's and Yamaman's), four lines drawn.

---

## Business leg — Chiba Prefecture's 環境衛生関係施設一覧 (dataset 6)

The dataset, its notes, files, layout, columns and dates are recorded in
`matsudo.md` (the same files): resource 79 (barbers, served as the 2025-03-31
list although titled 令和8年3月末), 80 (beauty) and 81 (laundries), both
2026-03-31; the monthly 新規施設 files 99-103 (beauty) and 111-115 (laundry),
2026-04 to 2026-08; one sheet per health centre; only applicants who agreed to
open publication are listed; Chiba, Funabashi and Kashiwa are not included.
What differs for Sakura:

- **Sakura's rows sit in the 印旛 sheet**, the 印旛健康福祉センター's area of nine
  municipalities: 佐倉市, 成田市, 四街道市, 八街市, 印西市, 白井市, 富里市,
  印旛郡酒々井町 and 印旛郡栄町. Every row of that sheet in all three lists names
  its municipality first, with no prefecture (`佐倉市…`): barbers 117 of 475,
  beauty 255 of 1,087, laundries 79 of 301. **No 印旛 row lacks a
  municipality.**
- ⚠️ **BUILD TRAP: the beauty workbook's 海匝 sheet is an exact copy of 印旛**
  (1,087 rows, an identical row multiset by hash; staging, 2026-10-06). So
  **255 rows naming 佐倉市 sit in the 海匝 sheet too**, and a filter on the
  address alone across the workbook returns **510**. The barber and laundry
  workbooks' 海匝 sheets share no row with 印旛 (240 and 65 rows of their own),
  nor does any monthly beauty file's. **Filter on sheet 印旛 AND 施設所在地１
  starting `佐倉市`**, never a sum of sheets and never an address filter alone;
  `source_rows` must fail if the beauty count is not 255 on this file.
- ⚠️ **The 印旛 barber sheet has its own column order** (`業務種別, 開設者名,
  開設者種別, 施設名称１, 施設名称２, 施設所在地１, 施設所在地２, 施設電話番号,
  検査確認番号, 検査確認日`) and **one extra column, 開設者種別**, blank on all
  117 Sakura rows. `xlsx_rows` keys by header, so the order is harmless; read
  columns by name, never by position.
- ⚠️ **The May beauty file's 印旛 sheet adds 開設者役職名 and 開設者代表者名** (a
  representative's own name; no Sakura row that month). 開設者代表者名 is
  already in `OPERATOR_COLS`; never select it.
- The address is 施設所在地１ (`ADDR_COLS`). 施設所在地２ is filled on 10 / 72
  / 2 Sakura rows; every 所在地１ carries a digit, and one beauty row's 所在地２
  begins with a digit (read it at build: a floor or a second number).

### Counts that matter (Sakura's rows)

| Kind | Rows | Not a premises | Storefronts | Newest 検査確認日 | 検査確認番号 repeated | Shōwa (S) dates `wareki_date` cannot read |
|---|---|---|---|---|---|---|
| 理容所 (barbers) | **117** | 0 | 117 | 2024-02-28 | 0 | 36 |
| 美容所 (beauty) | **255** | 0 | 255 | 2026-04-06 | 0 | 28 |
| クリーニング所 (laundries) | **79** | **1 無店舗取次店** | **78** (取次所 58, 洗い+仕上場 19, 仕上場 1) | 2022-02-22 | 0 | 16 |
| **Personal services (2026-03-31 lists)** | **451** | 1 | **450** | | | |

- **One pin per premises**: 5 (address, trade name) pairs repeat, **4 a barber
  and a beauty salon at one premises** under one name and 1 inside the barber
  list (two numbers), so the base lists draw **445 pins**.
- **No closed rows** (no closure column) and **no mobile salons** (no 移動,
  一円, 訪問 or 出張 in any Sakura address or name).
- ⚠️ **The laundry kind is in クリーニング種別１**, which `TYPE_COLS` does not
  read: map it into the type in `source_rows` (Matsudo's build item) so the
  one 無店舗取次店 stays off the map. クリーニング種別２: 無し 72, 特定洗濯物 3,
  リネンサプライ 2, リネン+特定 2.
- `japan_eigyo` buckets every remaining type as Personal services; nothing
  falls out by rule.

### The rebuild to 2026-08-31 (Matsudo's shape: the beauty and laundry months)

| Month | Beauty: 印旛 sheet rows | Sakura's | 検査確認日 | Repeats a base row | Laundry: Sakura's |
|---|---|---|---|---|---|
| 2026-04 | 3 | 1 | 04-06 | ⚠️ **1, by 検査確認番号 AND by address and name** | 0 (no 印旛 header: 「…新規なし」) |
| 2026-05 | 2 | 0 | | | 0 |
| 2026-06 | 5 | 0 | | | 0 |
| 2026-07 | 1 | 1 | 07-01 | 0 | 0 |
| 2026-08 | 1 | 0 | | | 0 |
| **Total** | 12 | **2** | | **1** | **0** |

- ⚠️ **The April addition is already in the base list**: the 2026-03-31 beauty
  file (saved 2026-04-27) carries confirmations up to 2026-04-06, and the April
  row repeats one of them by number. **Step 2 de-duplicates by 検査確認番号
  before anything else**; one pin per premises would also catch it. The
  master list's "+2" is the raw count; **net +1**.
- **Beauty: 255 + 1 = 256 rows and premises.** Neither addition has a company
  marker on its operator; the name rule flags 0; both parse to a block number.
- **No new laundry** in any month: laundries stay 79 rows, 78 premises.
- **Rebuilt totals at 2026-08-31**: barbers 117 (their own 2025-03-31),
  beauty 256, laundries 79 rows; **451 storefronts** (one laundry not a
  premises), **446 pins** (4 barber-and-salon premises, 1 barber repeat).
  Pin `as_of` per kind (`SOURCE_AS_OF`): barbers 2025-03-31, beauty and
  laundry 2026-08-31, an upper bound.

### Coverage — against e-Stat and the Economic Census

**e-Stat has no Sakura row** (衛生行政報告例 lists prefectures, 指定都市 and 中核市
only); the prefecture-level control is `matsudo.md`'s (barbers 99.6% on the
same date; beauty 92.3% with the 海匝 copy taken out; laundries 95.0%).
**Per city, an estimate only** (never for the page unless the owner asks, as
Ichikawa's call 32): the 2021 Economic Census
(`data/japan/raw/estat_census_r3_b1_009_1a.xlsx`, 第9-1A表; 12212: 理容業 101,
美容業 167, 洗濯業 45) scaled by `matsudo.md`'s licensed-to-census ratios
(barbers 1.118, beauty 1.595, laundries 1.294; the script reproduces Matsudo's
306 / 735 / 190):

| Kind | Estimate | The lists | Share |
|---|---|---|---|
| Barbers | about 113 | 117 | **104%** |
| Beauty | about 266 | 255 (256 rebuilt) | **96%** |
| Laundries | about 58 | 78 premises | **134%** |

- Laundries read **thick**, not thin: 78 premises against about 58. The census
  counts establishments by industry; a 取次所 inside another shop (58 of the
  78) may be counted under that shop's industry. A modelled figure; no call
  follows from it.

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 12212): ✅ 94.2% at the block

The join target is `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12212-24.0a.zip`
and `…/19.0b/12212-19.0b.zip`, approved by the owner on 2026-10-06 (call 106)
and saved in `data/sakura/raw/isj/`. One municipality, no wards
(`"wardless": True`); 19,506 block keys, 191 town-chōme keys.

**Measured 2026-10-06** (staging's measurement agent, a scratch script only:
`japan_register.permits_from_rows`, `load_city_isj` and `join_city` with
`WAVE2_RULES` unchanged, no normalisation changed, so no Minato re-run was
needed), on the 451 storefronts (sheet 印旛 and the address, the April
addition de-duplicated by 検査確認番号, the 無店舗取次店 out):

| Kind | Storefronts | Block | Chōme / 大字 centroid | Unplaced |
|---|---|---|---|---|
| Barbers | 117 | 111 (94.9%) | 6 | 0 |
| Beauty | 256 | 242 (94.5%) | 12 | 2 |
| Laundries | 78 | 72 (92.3%) | 6 | 0 |
| **All** | **451** | **425 (94.2%)** | **24 (5.3%)** | **2 (0.4%)** |

- The chōme shift placed 221 rows; 5 字 addresses took their 大字's centroid.
- **The 24 chōme-tier rows, by class**: **19 carry a 地番 MLIT's 24.0a lacks
  in a town it has** (上志津, 江原, 臼井台, 臼井田 and a few 町 such as 城内町
  and 並木町); **5 are 字 addresses** (上志津字…, 城字…, 神門字…, 六崎字…)
  placed at the 大字 centroid, since 24.0a keys no block under those 小字.
- **The 2 unplaced write a 大字 and its 小字 without 字** (井野 + 東作, 城 +
  松ケ丘), where the 大字 has one or two characters, below rule C's
  three-character floor.
- As the shapes below predicted, the chōme tier (5.3%) runs above Matsudo's
  (1.5%), in the 大字 + 地番 areas. Still at build: GSI's address search on a
  sample, with the 24 centroid rows' distance read.

What the lists alone said before the join:

- **Every one of the 452 storefronts (450 + 2 additions) parses to a block
  number** with `permits_from_rows` (`WAVE2_RULES`), across 49 / 56 / 39
  distinct towns.
- **Address shapes** (base rows): `町名1-2-3` 223, `町名1-2` 172, a bare number
  32, written 丁目 17, 番地 7. The dashed three-part form takes `join_city`'s
  shifted-chōme rule, as in Matsudo (571 rows there). The two-part and
  bare-number forms are 大字 + 地番 (and 地番-枝番) in Sakura's large 大字
  areas: MLIT's block edition numbers some 地番 areas and not others, so
  expect a larger chōme / 大字-centroid tier than Matsudo's 1.5% (it is: 5.3%,
  measured above).
- **At build**: the join re-run on the build's own rows; GSI's address search
  on a sample (`screen_japan_join.py`'s `gsi_check`, 150 rows, one request per
  second).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (12212)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_12_GML.zip`, N03 code 12212
(103.6 km²; extent W 140.1263, S 35.6246, E 140.3013, N 35.7662; centroid
140.213, 35.706). **13 station records inside, 11 `N02_005g` groups**; no name
in two groups. N02-24 and N02-25 agree on every station here; use N02-25.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | First beyond the line |
|---|---|---|---|---|
| ユーカリが丘線 (山万, **16: 案内軌条式, AGT**) | Yamaman Yūkarigaoka Line | **6 / 6** | ユーカリが丘, 地区センター, 公園, 女子大, 中学校, 井野 | none: wholly inside |
| 本線 (京成電鉄, 12) | Keisei Main Line | 5 / 42 | 志津, ユーカリが丘, 京成臼井, 京成佐倉, 大佐倉 | 勝田台 (八千代市, 0.1 km), 京成酒々井 (酒々井町, 0.9 km) |
| 総武線 (東日本旅客鉄道, 11) | JR Sōbu Main Line | **1 / 48** | 佐倉 | 物井 (四街道市, 0.2 km), 南酒々井 (酒々井町, 0.3 km) |
| 成田線 (東日本旅客鉄道, 11) | JR Narita Line | **1 / 27** | 佐倉 (its western end) | 酒々井 (酒々井町, 1.2 km) |

- **11 groups by operator**: Yamaman 6, Keisei 5 (ユーカリが丘 one group with
  Yamaman's, 91 m: MLIT's interchange), JR 1 (佐倉, both JR lines). Median gap
  to the nearest group **644 m** (closest 480 m, both on the Yamaman line;
  widest 2,359 m): ring sizes by the spacing rule at build, which may shrink
  them here.
- **JR one-station stubs, kept as cut (standing call, restated for wave 5)**:
  佐倉 on the Sōbu Main Line (1 of 48) **and on the Narita Line (1 of 27),
  which the master list's "JR 1" counts as one station**. Both commuter
  railways (class 11); neither goes back to the owner. Each is drawn as a
  short cut stub at the city line, both meeting at 佐倉.
- **The Yamaman line is an AGT (class 16), an urban line, drawn in full**: all
  6 of its stations are inside, so no stub rule reaches it. ASSERTED, to read
  in N02's sections at build: the line runs 4.1 km as a racket shape, a stem
  from ユーカリが丘 to 公園 and a one-way loop from 公園 through 女子大, 中学校
  and 井野; draw the loop as one line, never a doubled stem.
- **Kept apart, as N02 keeps them** (trap 1): Keisei's 京成佐倉 and JR's 佐倉
  are separate stations about 1.5 km apart, not an interchange.
- **The Shinkansen**: no station inside.
- **The light-rail / rail test**: one AGT (Yamaman, 6 groups), the rest
  railways (classes 11 and 12). JR is not the largest network (1 group), so
  JR does not make the city `metro`; open call 2 decides the mode.
- **Frequency** (no floor applies, call 46), **READ by the wave-5 probe
  (2026-10-06) from the operators' own timetables**: **Keisei** weekday
  10:00-16:00 (`keisei.ekitan.com`, Keisei's timetable service): 志津 and
  ユーカリが丘 6 an hour, 京成臼井 and 京成佐倉 3 to 7, 大佐倉 2 to 4. **Yamaman**:
  every 20 minutes through the day (the line's timetable PDF dated 2026-05-01,
  linked from `https://town.yukarigaoka.jp/yukariline/timetable/`; midday
  departures at :12, :32, :52). **JR: ASSERTED**, several trains an hour at
  佐倉. **No stretch runs about 11 trains a day or fewer** (call 86): the
  thinnest, Keisei at 大佐倉, has 2 to 4 an hour.
- **Gate 3** at build: Yamaman's 6 stations against its own line map, Keisei's
  and JR East's lists.
- ⚠️ **OSM `name:en`** for the 11 groups at build (no Overpass at Step 0; one
  station query in the N03 box): Yamaman's station names are generic words
  (地区センター "Chiku Center", 公園 "Kōen", 女子大 "Joshidai", 中学校
  "Chūgakkō"); read each against the operator's own romanisation and fix in
  `OSM_NAME_EN_OVERRIDES` if OSM differs. Also 大佐倉, 京成臼井, 志津.

## Scope

**Sakura City (12212), one municipality, no wards.** The lines run on into
Yachiyo, Yotsukaidō, Shisui and Yachimata; cut at the line, the stations beyond
named by N03 municipality at build (`excluded_stations.csv`). **Yachiyo is its
own page** (`docs/build_briefs/yachiyo.md`): Keisei's 勝田台, 0.1 km beyond
Sakura's line, belongs there. The 印旛 sheet's other eight municipalities are
not this page.

## Licences — as read (the full read is recorded)

- **Chiba Prefecture, dataset 6**: read 2026-10-05 (`docs/decisions_drafts/
  staging.md`, "Band B's Japanese sources read: Kanazawa, Chiba Prefecture and
  Shizuoka permitted with conditions", the Chiba Prefecture bullet; that entry
  is the verdict, this brief only cites it). **As declared on the dataset page**:
  every resource `resource_license_id: pdl`; the catalogue's terms page
  (`https://opendata.pref.chiba.lg.jp/pages/terms`) applies 公共データ利用規約
  （第1.0版） (PDL 1.0) where no other note is given. No new source here, so no
  new licence read. What it requires of the build, as recorded there:
  - **Cite and build from `opendata.pref.chiba.lg.jp` only**, never a
    `pref.chiba.lg.jp` page.
  - **MUST DISPLAY** the catalogue's 加工 form, the same notice as Matsudo's:
    `出典：「【千葉県】環境衛生関係施設一覧」（千葉県オープンデータサイト）（https://opendata.pref.chiba.lg.jp/datasets/6）を加工して作成`
    (settled with the notice at build).
  - **MUST NOT** present it as the prefecture's own or use its logos. No
    indemnity.
  - **The lists hold only applicants who agreed to open publication**:
    disclosed as a coverage reason.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**: CC
  BY 4.0, picks stations, ⛔ never drawn.
- **MHLW open data**: not used (food is off).

## Privacy

Read only the trade name, the type, the laundry kind and the premises address.
**No row value was printed or stored for this brief**: every count comes from
in-memory comparisons.

- **Operator columns**: **開設者名** (barber, beauty) and **営業者名** (laundry),
  both in `japan_register.OPERATOR_COLS`, filled on every Sakura row. A
  company or cooperative marker on 8 of 117 barber operators, 64 of 255 beauty
  and 34 of 79 laundry: the rest are mostly people's own names. 開設者種別 (the
  印旛 barber sheet's extra column) is blank on every Sakura row.
- **The name rule, version 2, flags 0 of Sakura's 453 rows** (451 base, 2
  additions): `same_person` 0 whether it compares 施設名称１ alone or 名称１ +
  名称２ (filled on 0 / 4 / 1 rows), `bare_personal_name` 0, so
  `name_is_operator` 0.
- **Never selected**: 施設電話番号; 開設者名 / 営業者名 / 開設者代表者名 beyond the
  rule's in-memory comparison. The lists carry no operator address.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map:
  it must print 0.

## Region

`"region": "Japan East"` (Kanto after wave 4's retag), `"country": "Japan"`,
`label_tier: "minor"`. Project to **UTM 54N (EPSG:32654)**: the city's
centroid lies at longitude 140.213, its extent 140.1263 to 140.3013, inside the
138-144 band (computed here, never copied).

**Scaffold**: `scaffold_city.py --slug sakura --name Sakura --system-name
"Keisei, Yamaman and JR East" --taxonomy japan_eigyo --lat 35.706 --lon
140.213 --region "Japan East" --country Japan --mode <call 2> --page-number
<N>` (`--dry-run` first), with the page number claimed in
`docs/session_roles.md` at build, not here. A `japan.CITIES` entry:
`"sakura": {"name": "佐倉市", "pref": "12", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["12212"]}`.

## Owner calls

**Made:** Band B, personal services only (owner, 2026-10-06, "Matsudo's
shape"); the prefecture's licence read (2026-10-05); the standing Japanese
calls above; the minor label tier and the Japan sub-region (2026-10-02); by
Matsudo's shape, which the band names: the barber list built as published with
its own date (Matsudo's call 33), the beauty and laundry months to 2026-08
(call 34's resources 99-103 and 111-115, already on disk), the two-date
source sentence as a review-time proposal (call 35); JR's two one-station
stubs at 佐倉 kept as cut (standing call); the Yamaman AGT drawn in full (no
stub question: 6 of 6 inside).

**Open:**

1. ✅ **MLIT's address blocks for 12212: approved by the owner (call 106,
   2026-10-06)**, fetched and measured: 94.2% at the block, 5.3% at a chōme
   or 大字 centroid (see "Coordinates"). Kept here so the numbering holds.
2. **`mode`**: no subway or tram; the Yamaman AGT is the largest network by
   in-city groups (6 against Keisei's 5), JR has 1. **Recommendation:
   `metro`**, the mode following the backbone as Matsudo's and Kurume's did:
   the Keisei Main Line carries the city's through traffic to Tokyo and Narita,
   and the Yamaman line is a 4.1 km feeder loop that meets it at ユーカリが丘.
   Tradeoff: read literally, the "largest network by stations inside the city
   line" test (written for JR) names the AGT, which would point at
   `light_rail`; no built Japanese city has an AGT as its largest network.

## What the build must still measure

- **The block join** (measured at 94.2%, call 106): re-run on the build's own
  rows; GSI on a sample, with the 24 centroid rows' distance read.
- Matsudo's config shape: `SOURCE_FILES` for the three lists and the ten
  months (the city's own `fetch_sources.py`, the publisher's file names),
  `SOURCE_AS_OF` per kind (barbers 2025-03-31; beauty and laundry
  2026-08-31), `MONTHLY`, `REQUIRED_COLUMNS` (施設名称１ or 施設名称,
  施設所在地１, 業務種別, 開設者名 / 営業者名, クリーニング種別１; a month's sheet
  holding only 「…新規なし」 has no header and must not stop the check), and a
  **`source_rows`** that reads sheet **印旛** of each file, keeps rows whose
  施設所在地１ starts `佐倉市` (117 / 255 / 79 on these files; the beauty count
  fails loudly if it reads 510, the 海匝 copy), de-duplicates by 検査確認番号
  (the April repeat), and carries クリーニング種別１ as the laundry type.
- Resource 79's served name and bytes (the barber file may be replaced); the
  newest edition of each file.
- Gate 3 against Yamaman's, Keisei's and JR East's lists; the Yamaman loop's
  geometry in N02; OSM `name:en` for 11 groups; line colours on both basemaps
  (4 lines, two JR stubs meeting at 佐倉).
- ⚠️ **The Economic Census control** (`scripts/japan_census_control.py`)
  measures 飲食店, which this page does not carry: the personal-services
  estimate above is the control; record it at build.

```brief-checks
[
  {
    "id": "sakura-dataset6-package",
    "claim": "Chiba Prefecture's dataset 6 still declares PDL on its resources, still excludes Chiba, Funabashi and Kashiwa, still lists only consenting applicants, and still points at resources 79-81 under their 2026-03-31 titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["\"resource_license_id\":\"pdl\"", "千葉市、船橋市及び柏市の施設情報は含まれていません", "オープンデータ掲載に賛同", "【千葉県】理容所施設一覧（令和8年3月末時点）", "【千葉県】美容所施設一覧（令和8年3月末時点）", "【千葉県】クリーニング所施設一覧（令和8年3月末時点）", "resource_download/79", "resource_download/80", "resource_download/81"]
  },
  {
    "id": "sakura-barber-size-mismatch",
    "claim": "The catalogue still declares 378,797 B for resource 79 while serving the 328,249 B 2025-03-31 file; if this size changes, the prefecture has touched the barber file: re-read it and re-measure Sakura's 117",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=79",
    "present": ["\"size\":\"378797\"", "令和8年3月末時点"]
  },
  {
    "id": "sakura-beauty-size",
    "claim": "Resource 80 (beauty, 2026-03-31, the workbook whose 海匝 sheet repeats 印旛) still declares 765,694 B; a new size means a new file: re-measure the 印旛 sheet's 255 Sakura rows and whether 海匝 is still a copy",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=80",
    "present": ["\"size\":\"765694\"", "美容所施設一覧（令和8年3月末時点）"]
  },
  {
    "id": "sakura-barber-live",
    "claim": "Resource 79 (barbers) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/79",
    "min_bytes": 300000
  },
  {
    "id": "sakura-beauty-live",
    "claim": "Resource 80 (beauty salons, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/80",
    "min_bytes": 700000
  },
  {
    "id": "sakura-laundry-live",
    "claim": "Resource 81 (laundries, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/81",
    "min_bytes": 200000
  },
  {
    "id": "sakura-monthly-package",
    "claim": "Dataset 6 still lists the ten monthly files of Matsudo's shape (beauty 99-103, laundry 111-115: 新規施設 令和8年4月 to 8月) under those titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["【千葉県】美容所新規施設（令和8年4月）", "【千葉県】美容所新規施設（令和8年7月）", "【千葉県】美容所新規施設（令和8年8月）", "【千葉県】クリーニング所新規施設（令和8年4月）", "【千葉県】クリーニング所新規施設（令和8年8月）", "resource_download/99", "resource_download/100", "resource_download/103", "resource_download/111", "resource_download/115"]
  },
  {
    "id": "sakura-beauty-jul-size",
    "claim": "The July beauty file (resource 100, Sakura's one net addition) still declares 71,818 B; a new size means a new upload: re-fetch and re-measure the month",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=100",
    "present": ["\"size\":\"71818\"", "美容所新規施設（令和8年7月）"]
  },
  {
    "id": "sakura-beauty-aug-size",
    "claim": "The August beauty file (resource 99, a second upload) still declares 70,264 B; a new size means a third upload: re-fetch and re-measure the month",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=99",
    "present": ["\"size\":\"70264\"", "美容所新規施設（令和8年8月）"]
  },
  {
    "id": "sakura-terms-pdl",
    "claim": "The catalogue's terms page still applies PDL 1.0 and prescribes the 加工 credit form",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/pages/terms",
    "present": ["PDL1.0", "千葉県オープンデータサイト", "を加工して作成"]
  },
  {
    "id": "sakura-yamaman-timetable",
    "claim": "The Yamaman Yukarigaoka Line's timetable page still links the timetable PDF (dated 2026-05-01) where the 20-minute service was read; a new PDF means a new timetable: re-read it",
    "kind": "http_contains",
    "url": "https://town.yukarigaoka.jp/yukariline/timetable/",
    "present": ["91db70aaca82c95caf0665a66f809ef1-7.pdf"]
  },
  {
    "id": "sakura-projected-crs",
    "claim": "Sakura projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.213,
    "expect": "EPSG:32654"
  }
]
```
