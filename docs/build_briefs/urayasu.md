# Urayasu — build brief

**Band B, personal services only, owner-approved 2026-10-06** (Japan wave 4,
banded in wave 5: `docs/decisions_drafts/staging.md`, "Wave 5: the ranked
queue and the pre-verdicts screened; Japan's lines carry no frequency floor
(owner)", Bands, B: "Urayasu, Sakura, Yachiyo and Ichihara (personal services,
Matsudo's shape …)"). **Step 0 measured 2026-10-06** (staging's brief agent).
**Nothing was downloaded for this brief**: every count below reads the files
already cached for Matsudo, read in place, never written to:

- `data/matsudo/raw/`: Chiba Prefecture's three lists (resource 79 →
  `ichiran-riyou202503.xlsx`, 328,249 B; 80 → `ichiran-biyou202603.xlsx`,
  765,694 B; 81 → `ichiran-clean202603.xlsx`, 254,290 B) and the ten approved
  monthly files (beauty 103-99 → `shinki-biyou2604.xlsx` … `shinki-biyou2608-2.xlsx`;
  laundry 115-111 → `shinki-clean2604.xlsx` … `shinki-clean2608.xlsx`), each
  fetched once from `opendata.pref.chiba.lg.jp` (2026-10-05 and 2026-10-06;
  URLs, bytes and the title checks in `docs/build_briefs/matsudo.md`).
- `data/japan/raw/`: N02-25 and N02-24, N03 (`N03-20250101_12_GML.zip`), and
  the 2021 Economic Census table (`estat_census_r3_b1_009_1a.xlsx`).
- **MLIT's address blocks for Urayasu (12227)**: approved by the owner on
  2026-10-06 (call 106) and fetched that day by staging's measurement agent,
  as `pipeline/countries/japan_fetch.py` fetches them, into
  `data/urayasu/raw/isj/`: `12227-24.0a.zip` (39,441 B) and `12227-19.0b.zip`
  (5,882 B) from `nlftp.mlit.go.jp`. **The block join is measured: 99.1%**
  (below, "Coordinates").
- **The build's own copies**: `fetch_sources.py` fetches the three lists and
  the ten months into `data/urayasu/raw/` under the publisher's file names, or
  the build copies the cached files byte for byte from `data/matsudo/raw/`
  (allowed; never write into another city's folder).

**Run `python scripts/brief_check.py urayasu` before writing any code.** Then
the `japan-city` skill, **Matsudo's shape** (`docs/build_briefs/matsudo.md`:
personal services only, the prefecture's lists cut to the city by sheet and
address, Kōchi's config with a `source_rows` hook). Coordinates: the
`address-join` skill with the shared `pipeline/countries/japan_register.py`
(`scripts/screen_japan_join.py` has no Urayasu entry; add one at build). Rail:
MLIT N02-25 cut at the N03 city line, measured through
`pipeline/countries/japan.py` with a scratch `CITIES` entry (none was added to
the shared module).

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to one station is left out,
its station kept through other lines (2026-10-06), **except where no other line
serves that station: then it is drawn cut** (calls 54 and 92, 2026-10-06:
Urayasu's Tōzai, below); (4) **菓子製造業 and そうざい製造業 count, in Retail**
(2026-09-24; moot on a personal-services page); (5) **the name rule, version
2** (2026-09-27; 2026-10-06): where the trade name IS the operator's own name,
or is written as a bare personal name, the pin shows its permit type, the
operator column read in memory only; (6) **no page says "currently
operating"**; (7) **no frequency floor for JR or private lines in Japan**
(call 46), every stretch with about 11 trains a day or fewer named and drawn
(call 86). Also: fault-based cost clauses accepted for all of Japan
(2026-09-24); English station names from OSM `name:en`, numerals as figures
before 丁目; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Urayasu
carries `label_tier: "minor"` and goes in the **Japan East** view with the
other Kantō cities (`app/cities.py`; wave 4's first city retags Japan into the
eight regions, Urayasu into Kanto). Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.
Urayasu borders Ichikawa and Tokyo's Edogawa, about 4 km from Ichikawa's
centre: measure its label against Tokyo's, Ichikawa's and Funabashi's.

**`mode`: `metro`.** Tokyo Metro's Tōzai Line is drawn inside the city (one
station, drawn cut by the owner's exception), as Ichikawa's `metro` rests on
the same line.

---

## The one-line summary

**Personal services only, from Chiba Prefecture's open-data lists of barbers,
beauty salons and laundries (dataset 6, PDL 1.0), the 市川 sheet cut to
Urayasu by address: 76 barbers (the 2025-03-31 list, built with its own date,
owner call 33), and beauty salons and laundries rebuilt to 2026-08-31 from the
2026-03-31 lists and five months of new premises (an upper bound, owner call
34): 195 beauty rows (194 premises) and 58 laundries; 329 storefronts, 326
pins.** Against a census-based estimate: about 119%, 113% and 121%. **The
block join places 99.1% at the block** (326 of 329; 1 chōme, 2 unplaced). Food stays off (the
prefecture's food set is old-law only). Rail: **7 N02 station groups**: the
Disney Resort Line 4 (counted as rail, owner call 53), JR Keiyō 2, and the
Tōzai Line's one station, 浦安, **drawn cut** (owner calls 54 and 92).

---

## Business leg — Chiba Prefecture's 環境衛生関係施設一覧 (dataset 6)

The dataset, its notes, the files, the monthly files, the layout, the columns
and the dates are Matsudo's, read once (`matsudo.md`, "Business leg"), and
hold here unchanged: dataset 6 at `https://opendata.pref.chiba.lg.jp/datasets/6`,
every resource `resource_license_id: pdl`, **only applicants who agreed to open
publication are listed**, Chiba, Funabashi and Kashiwa not included, one
workbook per kind with one sheet per health centre (13), header in row 1.
Columns: barber, beauty **開設者名**, **施設名称１**, 施設名称２,
**施設所在地１**, 施設所在地２, 施設電話番号, **業務種別**, 検査確認番号,
検査確認日; laundry **営業者名** in place of 開設者名, plus **クリーニング種別１**
and クリーニング種別２. The 市川 sheet uses the full-width spelling in all three
lists and in every month that has rows.

- **⚠️ The barber file is the 2025-03-31 list** (settled in `matsudo.md`: served
  as `ichiran-riyou202503.xlsx`, 328,249 B against the catalogue's 378,797,
  newest 検査確認日 in any sheet 2025-03-07). Urayasu's barber layer carries its
  own as-of, 2025-03-31, unless resource 79 is replaced by build time (the
  brief check pins the catalogue's size).
- **The beauty workbook's 海匝 sheet repeats 印旛** (staging, 2026-10-06):
  irrelevant to the 市川 sheet, but **never sum sheets**; filter on the
  city's own sheet and its address.

### Assigning rows to Urayasu (the address filter)

- **Urayasu's rows sit in the 市川 sheet**, the 市川健康福祉センター's area:
  市川市 and 浦安市. Each row's 施設所在地１ starts with its municipality, no
  prefecture: barbers 76 Urayasu / 223 Ichikawa (299), beauty 192 / 638 (830),
  laundries 58 / 148 (211, with 5 below). **No row naming 浦安市 sits in any
  other sheet** of the three lists (all 13 read; the 市原 barber sheet through
  a header fix, see `ichihara.md`), so the filter is exact: sheet 市川 and
  施設所在地１ starting `浦安市`.
- **Five laundry rows of the sheet name no municipality** (4 無店舗取次店, not
  premises in any case, and 1 取次所). **None starts with a town Urayasu's own
  rows use** (16 town names seen), so none is taken as Urayasu's. Re-read the
  取次所 against Urayasu's ISJ town list at build (it is Ichikawa's question
  otherwise, not this page's).
- **Step 2 needs a `source_rows`** (Kōchi's hook, as Matsudo's): read
  `city_rows(path, sheet="市川")`, keep the rows starting `浦安市`, fail if the
  count drifts from this brief's without a new file. Without it Ichikawa's
  rows reach the join.
- The address is 施設所在地１ (`ADDR_COLS` has it); 施設所在地２ (the building)
  is filled on 27 barber, 98 beauty and 9 laundry rows of Urayasu's. **Every
  所在地１ carries a digit**, so reading 所在地１ alone loses no placement.

### Counts that matter (Urayasu's rows)

| Kind | Rows (2026-03-31 lists; barbers 2025-03-31) | Not a premises | Storefronts | Newest 検査確認日 | 検査確認番号 repeated |
|---|---|---|---|---|---|
| 理容所 (barbers) | **76** | 0 | 76 | 2024-10-03 | 0 |
| 美容所 (beauty) | **192** | 0 | 192 | 2026-01-06 | 0 |
| クリーニング所 (laundries) | **58** | 0 | **58** (取次所 45, 洗い+仕上場 13) | 2024-11-27 | 0 |
| **Personal services** | **326** | 0 | **326** | | |

- **検査確認日** reads on 59 of 76 barber, 178 of 192 beauty and 56 of 58
  laundry rows; the rest are Shōwa (S) dates, which `wareki_date` returns as
  None. Nothing in the build reads it.
- **No closed rows** (no closure column) and **no mobile salons** (no 移動,
  一円 or 訪問 in any address or name).
- ⚠️ **The laundry kind is in クリーニング種別１**, which `TYPE_COLS` does not
  read. No Urayasu laundry row is a 無店舗取次店 on these files; map
  クリーニング種別１ into the type in `source_rows` anyway (Matsudo's build
  item), since a later edition may carry one.
- `japan_eigyo` buckets every type here as Personal services; nothing falls
  out by rule.

### The rebuild to 2026-08-31 (owner call 34)

| Month | Beauty: 市川 sheet rows | Urayasu's | 検査確認日 | Repeats a base row | Laundry: Urayasu's |
|---|---|---|---|---|---|
| 2026-04 | 2 | **0** | | | 0 (「…新規なし」) |
| 2026-05 | 3 | **2** | 05-12 .. 05-26 | 0 | 0 |
| 2026-06 | 5 | **1** | 06-12 | 0 | 0 |
| 2026-07 | 0 (「7月新規なし」) | **0** | | | 0 |
| 2026-08 | 1 | **0** | | | 0 |
| **Total** | 11 | **3** | | **0** | **0** |

- **Beauty: 192 + 3 = 195 rows.** No addition repeats a base 検査確認番号 or a
  base (address, trade name), nor another addition. 開設者名 filled on all 3,
  2 with a company marker; the name rule flags 0.
- **No new laundry in Urayasu in any month** (the 市川 laundry sheet reads
  「…新規なし」 in all five): laundries stay **58**, now dated 2026-08-31.
- **Rebuilt totals**: barbers 76 (their own 2025-03-31), beauty 195, laundries
  58: **329 storefronts. One pin per premises and bucket: 326 pins**: two
  (address, trade name) pairs are a barber and a salon at one premises
  (e-Stat's 重複開設), one repeats inside the beauty list.
- **An upper bound**: openings added, closures not published. `SOURCE_AS_OF`
  2026-08-31 for beauty and laundry, 2025-03-31 for barbers.

### Coverage — against e-Stat and the Economic Census

**e-Stat has no Urayasu row** (衛生行政報告例 lists prefectures, 指定都市 and
中核市 only); Urayasu is in the prefecture's own jurisdiction, whose controls
are in `matsudo.md` (barbers 99.6% of the official count on the same date;
beauty 92.3%, 海匝's own salons missing; laundries 95.0%).

**Per-city, an estimate only** (never for the page unless the owner says so,
Ichikawa's call 32): the 2021 Economic Census
(`data/japan/raw/estat_census_r3_b1_009_1a.xlsx`, 第9-1A表; 12227: 理容業 57,
美容業 108, 洗濯業 37), scaled by the jurisdiction's licensed to census ratio
(barbers 1.118, beauty 1.595, laundries 1.294; Matsudo's 274 / 461 / 147 and
Ichikawa's 200 / 387 / 144 reproduce), gives about **64 barbers, 172 salons
and 48 laundries**. The lists hold **76 (119%), 192 (112%) and 58 (121%)**;
rebuilt, **beauty 194 premises (113%)**. Urayasu is not thin in any kind; the
excess is in the census side (establishments, 2021) and is not a defect.

## Coordinates — a JOIN to MLIT 位置参照情報 (12227): ✅ 99.1% at the block

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12227-24.0a.zip` and
`…/19.0b/12227-19.0b.zip` (39,441 B and 5,882 B), approved by the owner on
2026-10-06 (call 106) and saved in `data/urayasu/raw/isj/`. One municipality,
no wards (`"wardless": True`); 1,654 block keys, 83 town-chōme keys.

**Measured 2026-10-06** (staging's measurement agent, a scratch script only:
`japan_register.permits_from_rows`, `load_city_isj` and `join_city` with
`WAVE2_RULES` unchanged, no normalisation changed, so no Minato re-run was
needed), on the 329 storefronts with the months:

| Kind | Storefronts | Block | Chōme | Unplaced |
|---|---|---|---|---|
| Barbers | 76 | 98.7% | 0 | 1 |
| Beauty | 195 | 100.0% | 0 | 0 |
| Laundries | 58 | 96.6% | 1 | 1 |
| **All** | **329** | **326 (99.1%)** | **1 (0.3%)** | **2 (0.6%)** |

- The chōme shift (`町名1-2-3` read as 町名一丁目 2番) placed 267 rows. No
  affix, 甲乙, 町, 大字 or twin rule fired.
- **The misses**: the chōme row is a block number MLIT's 24.0a lacks in a
  chōme it has (日の出); **the 2 unplaced rows are written in the dashed form
  with a first number no chōme carries** (北栄 has chōme 1-4, 日の出 1-8; the
  rows read 11 and 22), most likely a dropped hyphen or chōme in the source.
  A row error, not a rule to add; the build leaves them unplaced or reads
  them by hand.
- Still at build: GSI's address search on a sample (`screen_japan_join.py`'s
  `gsi_check`, 150 rows, one request per second).

What the address shapes said before the join (329 storefronts with the
months, shapes counted after the city prefix, no value printed):

| Shape | Rows | Share |
|---|---|---|
| `町名1-2-3` (no 丁目: `join_city`'s chōme shift) | 261 | 79.3% |
| `町名1丁目2-3` | 34 | 10.3% |
| `町名12-3` (地番 or block-number, two parts) | 34 | 10.3% |

- 36 distinct towns parsed. Urayasu is almost wholly under 住居表示, and the
  join bore out the expectation of a share near Ichikawa's (99.5%) and
  Matsudo's (98.3%).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (12227)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_12_GML.zip`, N03 code 12227
(18.8 km²; extent W 139.8715, S 35.6167, E 139.9395, N 35.6727). **7 station
records inside, 7 `N02_005g` groups**; no name in two groups. N02-24 and N02-25
agree on every station here; use N02-25.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | First beyond the line |
|---|---|---|---|---|
| ディズニーリゾートライン (舞浜リゾートライン, 15: straddle monorail) | **Disney Resort Line** | **4 / 4** | リゾートゲートウェイ･ステーション, 東京ディズニーランド･ステーション, ベイサイド･ステーション, 東京ディズニーシー･ステーション | none: a loop wholly inside |
| 京葉線 (東日本旅客鉄道, 11) | JR Keiyō Line | 2 / 19 | 舞浜, 新浦安 | 葛西臨海公園 (Tokyo, 1.1 km), 市川塩浜 (市川市, 1.3 km) |
| 5号線東西線 (東京地下鉄, 12) | Tokyo Metro Tōzai Line | **1 / 23** | 浦安 | 南行徳 (市川市, 0.4 km), 葛西 (Tokyo, 1.3 km) |

- **7 groups by operator**: Maihama Resort Line 4, JR 2, Tokyo Metro 1. No
  group holds two operators. **Kept apart, as N02 keeps them** (trap 1): JR's
  舞浜 and リゾートゲートウェイ･ステーション (**161 m**, the closest pair), a
  walking interchange under two names. Median gap to the nearest group
  **906 m** (largest 2,520 m): rings by the spacing rule at build; the two
  舞浜 rings will overlap almost wholly.
- ✅ **The Disney Resort Line counts as rail** (owner, call 53, 2026-10-06, on
  the Chiba Urban Monorail's precedent). N02 class 15 (跨座式鉄道);
  `japan_step1` reads every class but the Shinkansen, so nothing filters it.
  An URBAN line by the japan-city reading (a monorail), but wholly inside
  (4 of 4), so no stub question. Its label: open call 2.
- ✅ **The Tōzai Line at 浦安 is drawn cut** (owner, calls 54 and 92,
  2026-10-06): one station of 23, an urban line, which the one-station rule
  would leave out; **浦安 has no other line, so leaving the line out would drop
  the station**, and the owner made it the exception (Suita's Esaka the
  other). At build: the line is a `LINES` entry like Ichikawa's Tōzai
  (Tokyo's map draws it: reuse its public name and colour), not in
  `LEFT_OUT_LINES`; 南行徳 and 葛西 go to `excluded_stations.csv` by N03
  municipality. A page sentence is a proposal for review time: "The Tokyo
  Metro Tozai Line is shown only at Urayasu station, the one stop it makes in
  the city, because no other line serves that station."
- **JR Keiyō**: both stations on the main line (the Futamata branch is
  Ichikawa's, `ichikawa.md`); the Musashino Line's through trains run on N02's
  京葉線 here and need no line of their own. Tokyo's map built JR East's Keiyō
  services as routes: reuse them.
- **The Shinkansen**: no station inside.
- **The light-rail / rail test**: the Tōzai (a subway, drawn) makes the city
  `metro`; the Disney Resort Line is a monorail (Chiba's precedent counts it
  as rail); JR is a railway.
- **Frequency** (no floor applies; call 86 names stretches of about 11 trains
  a day or fewer): **JR Keiyō, READ** by staging's probe from JR East's own
  新浦安 timetable page (`https://timetables.jreast.co.jp/timetable/list0856.html`,
  HTTP 200, Last-Modified 2026-09-14): 10-11 trains an hour. **ASSERTED, not
  read**: the Disney Resort Line every 4-13 minutes (the probe's request to its
  host timed out) and the Tōzai every few minutes. No stretch here comes near
  11 trains a day.
- **Gate 3**: the Disney Resort Line's 4 stations (N02 has 4), JR East's Keiyō
  list and Tokyo Metro's Tōzai list at build.
- ⚠️ **OSM `name:en`** for the 7 groups at build (no Overpass at Step 0): one
  station query in the N03 box. N02 writes the monorail's names with a
  half-width middle dot (`･`): read OSM's English (Resort Gateway Station,
  Tokyo Disneyland Station, Bayside Station, Tokyo DisneySea Station) and keep
  the dot out of the English label; 新浦安 (Shin-Urayasu), 舞浜 (Maihama).

## Scope

**Urayasu City (12227), one municipality, no wards.** The Keiyō and Tōzai
lines run on into Ichikawa and Tokyo's Edogawa; cut at the line, the stations
beyond named by N03 municipality at build (`excluded_stations.csv`). Ichikawa
is its own page (`ichikawa.md`): 南行徳 and 市川塩浜 belong there.

## Licences — as read (the full read is recorded)

- **Chiba Prefecture, dataset 6**: read 2026-10-05 (`docs/decisions_drafts/
  staging.md`, "Band B's Japanese sources read: Kanazawa, Chiba Prefecture and
  Shizuoka permitted with conditions", the Chiba Prefecture bullet; that entry
  is the verdict, this brief only cites it, and no new source is added here).
  As declared: every resource `resource_license_id: pdl`; the catalogue's terms
  page (`https://opendata.pref.chiba.lg.jp/pages/terms`) applies 公共データ利用規約
  （第1.0版） (PDL 1.0). What it requires, as recorded there: cite and build from
  `opendata.pref.chiba.lg.jp` only; **MUST DISPLAY** the 加工 form, the same
  words as Matsudo's and Ichikawa's:
  `出典：「【千葉県】環境衛生関係施設一覧」（千葉県オープンデータサイト）（https://opendata.pref.chiba.lg.jp/datasets/6）を加工して作成`;
  **MUST NOT** present it as the prefecture's own or use its logos; the
  consent filter disclosed as a coverage reason.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**: CC
  BY 4.0, picks stations, ⛔ never drawn.
- **MHLW open data**: not used (food is off).

## Privacy

Read only the trade name, the type, the laundry kind and the premises address.
**No row value was printed or stored for this brief**: every count comes from
in-memory comparisons.

- **Operator columns**: **開設者名** (barber, beauty) and **営業者名** (laundry),
  both in `japan_register.OPERATOR_COLS`, filled on every Urayasu row. With no
  company or cooperative marker: 58 of 76 barber operators, 99 of 192 beauty, 7
  of 58 laundry (mostly people's own names).
- **The name rule, version 2** (`japan_register.name_is_operator` with
  `bare_personal_name`, on master): **0 of Urayasu's 329 rows** flagged, base
  lists and months alike, by either branch (the operator comparison or the
  bare-name form).
- **Never selected**: 施設電話番号; the operator columns beyond the rule's
  in-memory comparison. No operator address is published.
- 施設名称２ is filled on 3 barber, 9 beauty and 13 laundry rows; if the pin
  shows 名称１ + 名称２, the rule must compare what is shown.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map:
  it must print 0.

## Region

`"region": "Japan East"`, `"country": "Japan"`, `label_tier: "minor"`.
Project to **UTM 54N (EPSG:32654)**: the city's centroid lies at longitude
139.902 and its western edge at 139.8715, both inside the 138-144 band
(computed here, never copied).

**Scaffold**: `scaffold_city.py --slug urayasu --name Urayasu --system-name
"JR East, the Disney Resort Line and Tokyo Metro" --taxonomy japan_eigyo --lat
35.643 --lon 139.902 --region "Japan East" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), with the page number claimed in
`docs/session_roles.md` at build, not here. A `japan.CITIES` entry:
`"urayasu": {"name": "浦安市", "pref": "12", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["12227"]}`.

## Owner calls

**Made:** Band B, personal services only (owner, 2026-10-06, wave 5); the
prefecture's licence read (2026-10-05); the standing Japanese calls above; the
minor label tier and the Japan sub-region (owner, 2026-10-02); `metro` (the
Tōzai Line); **the Disney Resort Line counted as rail** (call 53); **the Tōzai
at 浦安 drawn cut** (calls 54 and 92); and, by Matsudo's and Ichikawa's calls
(2026-10-05), the barber list built as published with its own date (call 33),
the beauty and laundry months to 2026-08 (call 34; barbers get no months), and
the two-date source sentence as a review-time proposal (call 35): "From Chiba
Prefecture's open-data registers of barbers (as of March 31, 2025) and of
beauty salons and laundries (as of March 31, 2026, with openings to August 31,
2026), which list only premises whose operators agreed to publication."

**Open:**

1. ✅ **MLIT ISJ 12227: approved by the owner (call 106, 2026-10-06)**,
   fetched and measured: 99.1% at the block (see "Coordinates"). Kept here so
   the numbering holds.
2. **The monorail's on-map label.** N02 and the line's own name say
   ディズニーリゾートライン; Maihama Resort Line is the operator (the master
   list's wording). **Recommendation: label and legend "Disney Resort Line"**,
   the real public name the invariant asks for, with the operator in the
   page's system line. Tradeoff: a brand name on the map (a trade name, which
   the project shows; no logo or colour of the brand is used).

## What the build must still measure

- **The block join** (measured at 99.1%, call 106): re-run it on the build's
  own rows, GSI on a sample, the 2 dashed-form misses read; the 取次所 with no
  municipality against Urayasu's town list.
- Matsudo's config shape: `SOURCE_FILES` (three lists, ten months),
  `SOURCE_AS_OF` per kind, `MONTHLY`, `REQUIRED_COLUMNS` (a month holding only
  「…新規なし」 has no header and must not stop the check), and the
  `source_rows` above (sheet 市川, prefix `浦安市`: 76 / 195 / 58, クリーニング種別１
  as the laundry type).
- Resource 79's served name and bytes; the newest edition of each file.
- Gate 3 for the three operators; OSM `name:en` for 7 groups; the Tōzai and
  Keiyō reused from Tokyo's map; line colours on both basemaps (3 lines).
- The Disney Resort Line's frequency from its operator's own page if it
  answers (ASSERTED here).
- ⚠️ **The Economic Census control** (`scripts/japan_census_control.py`)
  measures 飲食店, which this page does not carry: the personal-services
  comparison above is the control; record it at build.

```brief-checks
[
  {
    "id": "urayasu-dataset6-package",
    "claim": "Chiba Prefecture's dataset 6 still declares PDL on its resources, still excludes Chiba, Funabashi and Kashiwa, still lists only consenting applicants, and still points at resources 79-81 under their 2026-03-31 titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["\"resource_license_id\":\"pdl\"", "千葉市、船橋市及び柏市の施設情報は含まれていません", "オープンデータ掲載に賛同", "【千葉県】理容所施設一覧（令和8年3月末時点）", "【千葉県】美容所施設一覧（令和8年3月末時点）", "【千葉県】クリーニング所施設一覧（令和8年3月末時点）", "resource_download/79", "resource_download/80", "resource_download/81"]
  },
  {
    "id": "urayasu-barber-size-mismatch",
    "claim": "The catalogue still declares 378,797 B for resource 79 while serving the 328,249 B 2025-03-31 file; a new size means the prefecture touched the barber file: re-read it and re-measure",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=79",
    "present": ["\"size\":\"378797\"", "令和8年3月末時点"]
  },
  {
    "id": "urayasu-barber-live",
    "claim": "Resource 79 (barbers) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/79",
    "min_bytes": 300000
  },
  {
    "id": "urayasu-beauty-live",
    "claim": "Resource 80 (beauty salons, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/80",
    "min_bytes": 700000
  },
  {
    "id": "urayasu-laundry-live",
    "claim": "Resource 81 (laundries, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/81",
    "min_bytes": 200000
  },
  {
    "id": "urayasu-monthly-package",
    "claim": "Dataset 6 still lists the ten approved monthly files (beauty 99-103, laundry 111-115: 新規施設 令和8年4月 to 8月) under those titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["【千葉県】美容所新規施設（令和8年4月）", "【千葉県】美容所新規施設（令和8年8月）", "【千葉県】クリーニング所新規施設（令和8年4月）", "【千葉県】クリーニング所新規施設（令和8年8月）", "resource_download/99", "resource_download/103", "resource_download/111", "resource_download/115"]
  },
  {
    "id": "urayasu-beauty-aug-size",
    "claim": "The August beauty file (resource 99, shinki-biyou2608-2.xlsx, a second upload) still declares 70,264 B; a new size means a third upload: re-fetch and re-measure the month",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=99",
    "present": ["\"size\":\"70264\"", "美容所新規施設（令和8年8月）"]
  },
  {
    "id": "urayasu-terms-pdl",
    "claim": "The catalogue's terms page still applies PDL 1.0 and prescribes the 加工 credit form",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/pages/terms",
    "present": ["PDL1.0", "千葉県オープンデータサイト", "を加工して作成"]
  },
  {
    "id": "urayasu-isj-block-live",
    "claim": "MLIT's block-level address file for Urayasu (12227, 24.0a, 39,441 B on 2026-10-06) answers keyless - the join target, fetched into data/urayasu/raw/isj/ on 2026-10-06 (owner call 106)",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12227-24.0a.zip",
    "min_bytes": 35000
  },
  {
    "id": "urayasu-isj-chome-live",
    "claim": "MLIT's town-chome address file for Urayasu (12227, 19.0b, 5,882 B on 2026-10-06) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/12227-19.0b.zip",
    "min_bytes": 2000
  },
  {
    "id": "urayasu-projected-crs",
    "claim": "Urayasu projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.902,
    "expect": "EPSG:32654"
  }
]
```
