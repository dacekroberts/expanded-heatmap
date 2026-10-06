# Ichihara — build brief

**Band B, personal services only, owner-approved 2026-10-06** (Japan wave 4,
banded in wave 5: `docs/decisions_drafts/staging.md`, "Wave 5: the ranked
queue and the pre-verdicts screened; Japan's lines carry no frequency floor
(owner)", Bands, B: "Urayasu, Sakura, Yachiyo and Ichihara (personal services,
Matsudo's shape; the Kominato line drawn)"). **Step 0 measured 2026-10-06**
(staging's brief agent). **Nothing was downloaded for this brief**: every
count below reads the files already cached for Matsudo, read in place, never
written to:

- `data/matsudo/raw/`: Chiba Prefecture's three lists (resource 79 →
  `ichiran-riyou202503.xlsx`, 328,249 B; 80 → `ichiran-biyou202603.xlsx`,
  765,694 B; 81 → `ichiran-clean202603.xlsx`, 254,290 B) and the ten approved
  monthly files (beauty 103-99 → `shinki-biyou2604.xlsx` … `shinki-biyou2608-2.xlsx`;
  laundry 115-111 → `shinki-clean2604.xlsx` … `shinki-clean2608.xlsx`), each
  fetched once from `opendata.pref.chiba.lg.jp` (2026-10-05 and 2026-10-06;
  URLs, bytes and the title checks in `docs/build_briefs/matsudo.md`).
- `data/japan/raw/`: N02-25 and N02-24, N03 (`N03-20250101_12_GML.zip`), and
  the 2021 Economic Census table (`estat_census_r3_b1_009_1a.xlsx`).
- The Kominato Railway's timetable page as staging's wave-5 probe saved it
  (2026-10-06, from `https://www.kominato.co.jp/timetable/`, HTTP 200), read
  from the probe's scratch copy, not re-fetched.
- **MLIT's address blocks for Ichihara (12219)**: approved by the owner on
  2026-10-06 (call 106) and fetched that day by staging's measurement agent,
  as `pipeline/countries/japan_fetch.py` fetches them, into
  `data/ichihara/raw/isj/`: `12219-24.0a.zip` (504,111 B) and
  `12219-19.0b.zip` (11,134 B) from `nlftp.mlit.go.jp`. **The block join is
  measured: 93.2%** (below, "Coordinates").
- **The build's own copies**: `fetch_sources.py` fetches the three lists and
  the ten months into `data/ichihara/raw/` under the publisher's file names,
  or the build copies the cached files byte for byte from `data/matsudo/raw/`
  (allowed; never write into another city's folder).

**Run `python scripts/brief_check.py ichihara` before writing any code.** Then
the `japan-city` skill, **Matsudo's shape** (`docs/build_briefs/matsudo.md`:
personal services only, the prefecture's lists cut to the city by sheet and
address, Kōchi's config with a `source_rows` hook), with **one trap new to
Ichihara: its barber sheet's header defeats `city_rows`** (below).
Coordinates: the `address-join` skill with the shared
`pipeline/countries/japan_register.py` (`scripts/screen_japan_join.py` has no
Ichihara entry; add one at build). Rail: MLIT N02-25 cut at the N03 city line,
measured through `pipeline/countries/japan.py` with a scratch `CITIES` entry
(none was added to the shared module).

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27; Keisei's ちはら台 here); an URBAN line cut to
one station is left out unless no other line serves its station (2026-10-06,
calls 54 and 92; no urban line here); (4) **菓子製造業 and そうざい製造業
count, in Retail** (2026-09-24; moot on a personal-services page); (5) **the
name rule, version 2** (2026-09-27; 2026-10-06): where the trade name IS the
operator's own name, or is written as a bare personal name, the pin shows its
permit type, the operator column read in memory only; (6) **no page says
"currently operating"**; (7) **no frequency floor for JR or private lines in
Japan** (call 46), every stretch with about 11 trains a day or fewer named and
drawn (call 86). Also: fault-based cost clauses accepted for all of Japan
(2026-09-24); English station names from OSM `name:en`, numerals as figures
before 丁目; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Ichihara
carries `label_tier: "minor"` and goes in the **Japan East** view with the
other Kantō cities (`app/cities.py`; wave 4's first city retags Japan into the
eight regions, Ichihara into Kanto). Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**`mode`: `metro`** (the owner's rule of 2026-10-02, applied as for Kurume,
Maebashi and Matsudo): no subway or tram, and JR is not the largest network
inside the city (3 station groups against the Kominato Railway's 17), so the
mode follows the backbone, the Kominato Railway, a railway (N02 class 12).

---

## The one-line summary

**Personal services only, from Chiba Prefecture's open-data lists of barbers,
beauty salons and laundries (dataset 6, PDL 1.0), the 市原 sheet (Ichihara
alone): 218 barbers (the 2025-03-31 list, built with its own date, owner call
33), and beauty salons and laundries rebuilt to 2026-08-31 from the 2026-03-31
lists and five months of new premises (an upper bound, owner call 34): 423
beauty rows (422 premises) and 76 laundries; 717 storefronts, 714 pins.**
Against a census-based estimate: about 100%, 101% and **81%** (laundries thin,
as Ichikawa's: open call 2). **About half the addresses are written in 地番
form, and the block join places 93.2% at the block** (668 of 717; 43 at a
chōme or 大字 centroid, 6 unplaced), five points under Matsudo's. Food stays off (the prefecture's food set
is old-law only). Rail: **20 N02 station groups**: the Kominato Railway 17
(drawn, no frequency floor; 上総牛久-養老渓谷 about 11-12 trains a day, named
under call 86), JR Uchibō 3 (五井 shared with the Kominato), and Keisei's
one-station stub ちはら台, kept as cut.

---

## Business leg — Chiba Prefecture's 環境衛生関係施設一覧 (dataset 6)

The dataset, its notes, the files, the monthly files, the layout, the columns
and the dates are Matsudo's, read once (`matsudo.md`, "Business leg"), and
hold here: dataset 6 at `https://opendata.pref.chiba.lg.jp/datasets/6`, every
resource `resource_license_id: pdl`, **only applicants who agreed to open
publication are listed**, Chiba, Funabashi and Kashiwa not included, one
workbook per kind with one sheet per health centre (13), header in row 1.

- **⚠️ The barber file is the 2025-03-31 list** (settled in `matsudo.md`:
  served as `ichiran-riyou202503.xlsx`, 328,249 B against the catalogue's
  378,797, newest 検査確認日 in any sheet 2025-03-07). Ichihara's barber layer
  carries its own as-of, 2025-03-31, unless resource 79 is replaced by build
  time (the brief check pins the catalogue's size).
- **The beauty workbook's 海匝 sheet repeats 印旛** (staging, 2026-10-06):
  irrelevant to the 市原 sheet, but **never sum sheets**; filter on the
  city's own sheet and its address.

### ⚠️ The 市原 barber sheet writes its header with a half-width 1

| Sheet 市原 | Header (column names) | `city_rows` reads |
|---|---|---|
| Barbers (79) | 開設者名, **施設名称1**, **施設名称2**, **施設所在地1**, **施設所在地2**, 施設電話番号, 業務種別, 検査確認番号, 検査確認日 | **0 of 218** |
| Beauty (80), laundries (81) | the full-width spelling (施設名称１, 施設所在地１ …), laundries with 営業者名 and クリーニング種別１ / ２ | 414 / 75, all |

`xlsx_rows` finds a header by an `ADDR_COLS` name, and `ADDR_COLS` holds
施設所在地１ (full-width, Matsuyama's) and 営業所所在地1 (Kumamoto's) but not
施設所在地1, so **the barber sheet is skipped without an error**. Every count
here read it with the four names mapped to the full-width spelling. Two fixes,
measured on equal terms (a build choice, not an owner call):

- **City-local** (recommended): the `source_rows` reads the 市原 barber sheet
  with the header mapped (施設名称1 → 施設名称１, 施設所在地1 → 施設所在地１, and
  the two 2s), and fails if it reads fewer than 218 rows. No other city moves.
- **Shared**: `ADDR_COLS` += 施設所在地1, after every older spelling, then the
  Minato control (`screen_japan_join.py minato`, 98.0 / 0.2 / 1.8) and every
  city screen; `NAME_COLS` already has 施設名称1.

The monthly 市原 sheets use the full-width address spelling but **vary the
name column**: 2026-05 and 2026-07 have 施設名称１ and no 施設名称２, 2026-08
writes **施設名称** (no number; `NAME_COLS` has it). `REQUIRED_COLUMNS` must
accept either name spelling for the months.

### Assigning rows to Ichihara (the address filter)

- **The 市原 sheet is the 市原健康福祉センター's area, Ichihara alone**: every
  row of all three lists starts its 施設所在地１ with `市原市` (218 / 414 / 75),
  no prefecture written. **No row naming 市原市 sits in any other sheet** (all
  13 read in each list). Keep both filters anyway (sheet 市原 and the prefix
  `市原市`), as Matsudo's, so a later edition that adds a neighbour fails
  loudly.
- **Step 2 needs a `source_rows`** (Kōchi's hook): reads sheet 市原 of each
  list and month, maps the barber header (above), keeps rows starting `市原市`,
  carries クリーニング種別１ as the laundry type, and fails if a count drifts
  from this brief's without a new file.
- The address is 施設所在地１; 施設所在地２ (the building) is filled on 0
  barber, 82 beauty and 6 laundry rows. **Every 所在地１ carries a digit.**

### Counts that matter (Ichihara's rows)

| Kind | Rows (2026-03-31 lists; barbers 2025-03-31) | Not a premises | Storefronts | Newest 検査確認日 | 検査確認番号 repeated |
|---|---|---|---|---|---|
| 理容所 (barbers) | **218** | 0 | 218 | 2024-05-24 | 0 |
| 美容所 (beauty) | **414** | 0 | 414 | 2026-03-04 | 0 |
| クリーニング所 (laundries) | **75** | 0 | **75** (取次所 41, 洗い+仕上場 34) | 2025-03-17 | 0 |
| **Personal services** | **707** | 0 | **707** | | |

- **検査確認日** reads on 144 of 218 barber, 346 of 414 beauty and 64 of 75
  laundry rows; the rest are Shōwa (S) dates (`wareki_date` returns None).
  Nothing in the build reads it.
- **No closed rows** (no closure column) and **no mobile salons** (no 移動,
  一円 or 訪問 in any address or name).
- ⚠️ **The laundry kind is in クリーニング種別１**, which `TYPE_COLS` does not
  read. No Ichihara laundry row is a 無店舗取次店 on these files; map it into
  the type in `source_rows` anyway (Matsudo's build item).
- `japan_eigyo` buckets every type here as Personal services; nothing falls
  out by rule.

### The rebuild to 2026-08-31 (owner call 34)

| Month | Beauty: Ichihara's | 検査確認日 | Laundry: Ichihara's | Repeats a base row |
|---|---|---|---|---|
| 2026-04 | **0** (「…新規なし」) | | 0 | |
| 2026-05 | **5** | 05-01 .. 05-27 | 0 | 0 |
| 2026-06 | **0** (「…新規なし」) | | 0 | |
| 2026-07 | **2** | 07-06 .. 07-07 | **1** (取次所, 07-13) | 0 |
| 2026-08 | **2** | 08-27 .. 08-28 | 0 | 0 |
| **Total** | **9** | | **1** | **0** |

- No addition repeats a base 検査確認番号 or a base (address, trade name), nor
  another addition. Operators: filled on all 10; 4 of the 9 beauty and the 1
  laundry with a company marker; the name rule flags 0.
- **Rebuilt totals**: barbers 218 (their own 2025-03-31), beauty 414 + 9 =
  **423**, laundries 75 + 1 = **76**: **717 storefronts. One pin per premises
  and bucket: 714 pins**: two (address, trade name) pairs are a barber and a
  salon at one premises, one repeats inside the beauty list.
- **An upper bound**: openings added, closures not published. `SOURCE_AS_OF`
  2026-08-31 for beauty and laundry, 2025-03-31 for barbers.

### Coverage — against e-Stat and the Economic Census

**e-Stat has no Ichihara row** (衛生行政報告例 lists prefectures, 指定都市 and
中核市 only; Ichihara is neither); it is in the prefecture's own jurisdiction,
whose controls are in `matsudo.md` (barbers 99.6% of the official count on the
same date; beauty 92.3%, 海匝's own salons missing; laundries 95.0%).

**Per-city, an estimate only**: the 2021 Economic Census
(`data/japan/raw/estat_census_r3_b1_009_1a.xlsx`, 第9-1A表; 12219: 理容業 194,
美容業 263, 洗濯業 73), scaled by the jurisdiction's licensed to census ratio
(barbers 1.118, beauty 1.595, laundries 1.294; Matsudo's 274 / 461 / 147 and
Ichikawa's 200 / 387 / 144 reproduce), gives about **217 barbers, 419 salons
and 94 laundries**. The lists hold **218 (100%), 414 (99%) and 75 (80%)**;
rebuilt, **beauty 422 premises (101%), laundries 76 (81%)**. ⚠️ **Laundries
look thin, as Ichikawa's did** (148, about 80%), where Matsudo's read 97%; the
cause is not known (consent, closures since 2021, or what the census counts as
洗濯業). Open call 2.

## Coordinates — a JOIN to MLIT 位置参照情報 (12219): ⚠️ 93.2% at the block

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12219-24.0a.zip` and
`…/19.0b/12219-19.0b.zip` (504,111 B and 11,134 B), approved by the owner on
2026-10-06 (call 106) and saved in `data/ichihara/raw/isj/`. One municipality,
no wards (`"wardless": True`); 92,360 block keys, 394 town-chōme keys.

**Measured 2026-10-06** (staging's measurement agent, a scratch script only:
`japan_register.permits_from_rows`, `load_city_isj` and `join_city` with
`WAVE2_RULES` unchanged, no normalisation changed, so no Minato re-run was
needed; the barber sheet read with the half-width header mapped locally), on
the 717 storefronts with the months:

| Kind | Storefronts | Block | Chōme / 大字 centroid | Unplaced |
|---|---|---|---|---|
| Barbers | 218 | 203 (93.1%) | 13 | 2 |
| Beauty | 423 | 394 (93.1%) | 25 | 4 |
| Laundries | 76 | 71 (93.4%) | 5 | 0 |
| **All** | **717** | **668 (93.2%)** | **43 (6.0%)** | **6 (0.8%)** |

- The chōme shift placed 330 rows; rule C (a known town as prefix) 2; one
  字 address took its 大字's centroid.
- **The 43 chōme-tier rows, by class**: **28 carry a number MLIT's 24.0a
  lacks in a town it has**: 地番 inside 大字 such as 五井 and 牛久, and a few
  in newer 住居表示 chōme (五井中央南・西1丁目) whose blocks the edition does not
  hold; **15 sit in rural 大字 with no block points at all in 24.0a** (朝生原,
  養老, 月崎, 高滝, 飯給 …, the south of the city): a 大字 centroid, which in a
  large rural 大字 can sit a kilometre or more from the shop.
- **The 6 unplaced, by class**: **3 write a 大字 and its 小字 without 字**
  (犬成 + 小字, 五井 + 川岸, 五井 + 梨ノ木) where the 大字 has two characters,
  below rule C's three-character floor; **3 write the town short** (白金 for
  MLIT's 白金町N丁目, 南国分寺 for 南国分寺台, 八幡海岸 for 八幡海岸通).
- ⚠️ **For staging and the owner**: 93.2% is below the built Chiba cities
  (Matsudo 98.3%, Ichikawa 99.5%). Whether that is "well below" (the trigger
  this brief set for going back to the owner before step 3) is the owner's
  call; the 43 centroid rows are 6% of the page, 15 of them rural. GSI's
  address search on a sample (`screen_japan_join.py`'s `gsi_check`, 150 rows,
  one request per second) gives their distance at build.

What the address shapes said before the join (717 storefronts with the
months, shapes counted after the city prefix, no value printed):

| Shape | Rows | Share |
|---|---|---|
| `町名1-2-3` (no 丁目: `join_city`'s chōme shift) | 307 | 42.8% |
| `町名1丁目2-3` | 48 | 6.7% |
| `町名123-4` (two parts: 地番 with a branch, or block-number) | 266 | 37.1% |
| `町名123` (one number: a 地番) | 94 | 13.1% |
| other | 2 | 0.3% |

- **156 distinct towns parsed** in a 367.9 km² city. Ichihara is a largely
  地番-addressed municipality outside its 住居表示 districts: **about half the
  rows (360) are in a shape that joins at the block only where MLIT's block
  edition carries 地番 points for that 大字**; otherwise they fall to the
  大字 centroid, which in a rural 大字 can sit a kilometre or more from the
  shop. Matsudo's chōme tier (1.5%) came wholly from such 大字 areas.
  **The block file is nearly twice Matsudo's** (504,111 B; 92,360 block keys
  against Matsudo's 39,921): MLIT numbers most of Ichihara's 地番 areas, which
  is why the 地番 half still joins at 93.2% overall (measured above).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (12219)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_12_GML.zip`, N03 code 12219
(367.9 km²; extent W 140.0098, S 35.2312, E 140.2602, N 35.5618). **21 station
records inside, 20 `N02_005g` groups**; no name in two groups. N02-24 and
N02-25 agree on every station here; use N02-25.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | First beyond the line |
|---|---|---|---|---|
| 小湊鐵道線 (小湊鐵道, 12) | Kominato Railway Line | **17 / 18** | 五井, 上総村上, 海士有木, 上総三又, 上総山田, 光風台, 馬立, 上総牛久, 上総川間, 上総鶴舞, 上総久保, 高滝, 里見, 飯給, 月崎, 上総大久保, 養老渓谷 | 上総中野 (大多喜町, 2.2 km) |
| 内房線 (東日本旅客鉄道, 11) | JR Uchibō Line | 3 / 30 | 八幡宿, 五井, 姉ヶ崎 | 浜野 (千葉市, 0.5 km), 長浦 (袖ケ浦市, 3.1 km) |
| 千原線 (京成電鉄, 12) | Keisei Chihara Line | **1 / 6** | ちはら台 (its terminus) | おゆみ野 (千葉市, 1.4 km) |

- **20 groups by operator**: Kominato 17, JR 3, Keisei 1; **五井 is one group
  holding JR and the Kominato** (MLIT's interchange). Median gap to the nearest
  group **1,811 m** (closest pair 1,312 m, 上総三又-上総山田; largest 5,653 m):
  rings by the spacing rule at build.
- ✅ **The Kominato line is drawn** (owner, 2026-10-06: no frequency floor for
  JR or private lines in Japan, call 46). 17 of its 18 stations are inside;
  the 18th, 上総中野, is Ōtaki's and goes to `excluded_stations.csv`. The
  房総里山トロッコ (a sightseeing train on specified days, March to December)
  runs on the same track and needs no line of its own.
- ✅ **Keisei's ちはら台 is a one-station stub, kept as cut** (owner,
  2026-10-06, and the standing call of 2026-09-27): a private commuter railway
  (class 12), not an urban line, so the one-station rule's leave-out does not
  reach it. Its terminus is inside the city; the five stations beyond are
  Chiba City's (Band R, not built), to `excluded_stations.csv`.
- **JR Uchibō**: 3 of 30, cut at the line both ways. N02's 内房線 is a legal
  line; which services run on it here (the locals, any through trains from
  the Keiyō or Sōbu lines) is not read: read it at build if JR is drawn as
  services, as Tokyo's routes (trap 2).
- **The Shinkansen**: no station inside.
- **The light-rail / rail test**: no subway, tram, monorail or light rail;
  every line is a railway (classes 11 and 12). `metro` on Kurume's precedent
  (above).
- **Frequency, READ** for the Kominato from its own timetable page
  (`https://www.kominato.co.jp/timetable/`, 「令和8年3月14日改正」, staging's
  probe copy of 2026-10-06; the PDF `kominato-timetable-2026.pdf` linked
  there): **五井 → 上総牛久 every 40 minutes through the day** (27 down
  departures from 五井 listed, 6:15 to 22:57, one of them the trolley); **⚠️
  上総牛久 → 養老渓谷 about 11 to 12 trains a day each way** (13 southbound
  columns from 上総牛久 and 12 northbound from 養老渓谷 listed, the table mixing
  weekday and weekend columns and counting the trolley and ◆ specified-day
  trains). **Named under call 86: this stretch is drawn, not left out.** The
  build re-counts it by train number from the weekday table and states the
  figure. 養老渓谷 → 上総中野 (5 a day) lies beyond the line. **JR Uchibō,
  READ** by staging's probe from JR East's 五井 timetable page: about 3 an
  hour. **ASSERTED, not read**: Keisei's Chihara Line at ちはら台, several an
  hour.
- **Gate 3**: the Kominato's own station pages list **18** stations on the line
  (五井 to 上総中野; its menu adds 安房小湊, a bus connection, not on the line),
  as N02 has 18. JR East's Uchibō list and Keisei's Chihara list at build.
- ⚠️ **OSM `name:en`** for the 20 groups at build (no Overpass at Step 0): one
  station query in the N03 box. Read every name: the 上総 prefix (Kazusa-),
  海士有木, 飯給, 馬立, 養老渓谷, 姉ヶ崎 (ヶ), 八幡宿.

## Scope

**Ichihara City (12219), one municipality, no wards.** The lines run on into
Chiba City (JR, Keisei), Sodegaura (JR) and Ōtaki (the Kominato); cut at the
line, the stations beyond named by N03 municipality at build
(`excluded_stations.csv`). The city is large and mostly rural: its premises
sit mainly along JR in the north (五井, 姉ヶ崎, 八幡宿), the Kominato's rings run
south through farmland and hills.

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
- The Kominato's timetable page was read for frequency only; nothing from it
  is published.

## Privacy

Read only the trade name, the type, the laundry kind and the premises address.
**No row value was printed or stored for this brief**: every count comes from
in-memory comparisons.

- **Operator columns**: **開設者名** (barber, beauty) and **営業者名** (laundry),
  both in `japan_register.OPERATOR_COLS`, filled on every Ichihara row. With no
  company or cooperative marker: **199 of 218 barber operators**, 318 of 414
  beauty, 33 of 75 laundry (mostly people's own names: a higher share than
  Matsudo's or Urayasu's).
- **The name rule, version 2** (`japan_register.name_is_operator` with
  `bare_personal_name`, on master): **8 of Ichihara's 717 rows flagged**
  (barbers 5, beauty 3; 0 in the months, 0 laundries), **every one by the
  bare-name form** (a common surname, a space, 1-3 kanji or kana); these pins
  show their category. ⚠️ The 5 barbers are flagged only once the barber sheet
  is read at all (the header trap above): **`check_personal_exposure.py` must
  see the 8**, and a build that silently reads 0 barbers would pass it with 3.
- **Never selected**: 施設電話番号; the operator columns beyond the rule's
  in-memory comparison. No operator address is published.
- 施設名称２ is filled on 0 barber, 5 beauty and 5 laundry rows; if the pin
  shows 名称１ + 名称２, the rule must compare what is shown.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map:
  it must print 0.

## Region

`"region": "Japan East"`, `"country": "Japan"`, `label_tier: "minor"`.
Project to **UTM 54N (EPSG:32654)**: the city's centroid lies at longitude
140.137 and its eastern edge at 140.2602, both inside the 138-144 band
(computed here, never copied).

**Scaffold**: `scaffold_city.py --slug ichihara --name Ichihara --system-name
"the Kominato Railway, JR East and Keisei" --taxonomy japan_eigyo --lat
35.425 --lon 140.137 --region "Japan East" --country Japan --mode metro
--page-number <N>` (`--dry-run` first; the coordinates are N03's centroid, in
the rural middle: the map's fit follows the drawn stations, check it with
`scripts/check_map_view.js`), with the page number claimed in
`docs/session_roles.md` at build, not here. A `japan.CITIES` entry:
`"ichihara": {"name": "市原市", "pref": "12", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["12219"]}`.

## Owner calls

**Made:** Band B, personal services only (owner, 2026-10-06, wave 5); **the
Kominato line drawn** (owner, 2026-10-06, call 46); **Keisei's ちはら台 kept as
cut** (owner, 2026-10-06, and the standing call); the prefecture's licence read
(2026-10-05); the standing Japanese calls above; the minor label tier and the
Japan sub-region (owner, 2026-10-02); `metro` by the owner's mode rule of
2026-10-02 (staging's reading, as Matsudo's); and, by Matsudo's and Ichikawa's
calls (2026-10-05), the barber list built as published with its own date (call
33), the beauty and laundry months to 2026-08 (call 34; barbers get no months),
and the two-date source sentence as a review-time proposal (call 35): "From
Chiba Prefecture's open-data registers of barbers (as of March 31, 2025) and
of beauty salons and laundries (as of March 31, 2026, with openings to August
31, 2026), which list only premises whose operators agreed to publication."

**Open:**

1. ✅ **MLIT ISJ 12219: approved by the owner (call 106, 2026-10-06)**,
   fetched and measured: 93.2% at the block, 6.0% at a chōme or 大字
   centroid (see "Coordinates"). ⚠️ What remains open is whether 93.2% is
   "well below" the built Chiba cities and goes back to the owner before step
   3. **Recommendation: build**, stating nothing new on the page; read the
   43 centroid rows' distance on the build's GSI sample and bring them back
   only if their median distance runs past about 500 m. Tradeoff:
   about one pin in seventeen sits at a town or 大字 centroid, mostly in the
   rural south.
2. **Laundries at about 80% of the census estimate** (76 of about 94).
   **Recommendation: Ichikawa's call 32, built and the share stated on the
   page as an estimate** (a review-time proposal in Ichikawa's words: "The
   prefecture's register lists 76 laundries in Ichihara, about four in five
   of the number the 2021 Economic Census suggests; the reason is not
   known."). Tradeoff: a second page carrying a modelled figure; the
   alternative, saying nothing, breaks the precedent.

## What the build must still measure

- **The block join** (measured at 93.2%, call 106): re-run it on the build's
  own rows, GSI on a sample with the 43 centroid rows' distance read (open
  call 1's remaining question), the 6 unplaced read.
- **The barber header** (city-local `source_rows` or shared `ADDR_COLS`,
  above), with a count guard of 218.
- Matsudo's config shape: `SOURCE_FILES` (three lists, ten months),
  `SOURCE_AS_OF` per kind, `MONTHLY`, `REQUIRED_COLUMNS` (a month holding only
  「…新規なし」 has no header and must not stop the check; 施設名称 or
  施設名称１ in the months), and the `source_rows` (sheet 市原, prefix
  `市原市`: 218 / 423 / 76, クリーニング種別１ as the laundry type).
- Resource 79's served name and bytes; the newest edition of each file.
- The Kominato's 上総牛久-養老渓谷 count by train number (weekday table) for
  the page's line note; gate 3 for three operators; OSM `name:en` for 20
  groups; line colours on both basemaps (3 lines).
- ⚠️ **The Economic Census control** (`scripts/japan_census_control.py`)
  measures 飲食店, which this page does not carry: the personal-services
  comparison above is the control; record it at build.

```brief-checks
[
  {
    "id": "ichihara-dataset6-package",
    "claim": "Chiba Prefecture's dataset 6 still declares PDL on its resources, still excludes Chiba, Funabashi and Kashiwa, still lists only consenting applicants, and still points at resources 79-81 under their 2026-03-31 titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["\"resource_license_id\":\"pdl\"", "千葉市、船橋市及び柏市の施設情報は含まれていません", "オープンデータ掲載に賛同", "【千葉県】理容所施設一覧（令和8年3月末時点）", "【千葉県】美容所施設一覧（令和8年3月末時点）", "【千葉県】クリーニング所施設一覧（令和8年3月末時点）", "resource_download/79", "resource_download/80", "resource_download/81"]
  },
  {
    "id": "ichihara-barber-size-mismatch",
    "claim": "The catalogue still declares 378,797 B for resource 79 while serving the 328,249 B 2025-03-31 file; a new size means the prefecture touched the barber file: re-read it, its 市原 header included, and re-measure",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=79",
    "present": ["\"size\":\"378797\"", "令和8年3月末時点"]
  },
  {
    "id": "ichihara-barber-live",
    "claim": "Resource 79 (barbers) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/79",
    "min_bytes": 300000
  },
  {
    "id": "ichihara-beauty-live",
    "claim": "Resource 80 (beauty salons, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/80",
    "min_bytes": 700000
  },
  {
    "id": "ichihara-laundry-live",
    "claim": "Resource 81 (laundries, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/81",
    "min_bytes": 200000
  },
  {
    "id": "ichihara-monthly-package",
    "claim": "Dataset 6 still lists the ten approved monthly files (beauty 99-103, laundry 111-115: 新規施設 令和8年4月 to 8月) under those titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["【千葉県】美容所新規施設（令和8年4月）", "【千葉県】美容所新規施設（令和8年8月）", "【千葉県】クリーニング所新規施設（令和8年4月）", "【千葉県】クリーニング所新規施設（令和8年8月）", "resource_download/99", "resource_download/103", "resource_download/111", "resource_download/115"]
  },
  {
    "id": "ichihara-beauty-aug-size",
    "claim": "The August beauty file (resource 99, shinki-biyou2608-2.xlsx, a second upload) still declares 70,264 B; a new size means a third upload: re-fetch and re-measure the month",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=99",
    "present": ["\"size\":\"70264\"", "美容所新規施設（令和8年8月）"]
  },
  {
    "id": "ichihara-laundry-jul-live",
    "claim": "The July laundry month (resource 112, the one month with an Ichihara laundry) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/112",
    "min_bytes": 30000
  },
  {
    "id": "ichihara-terms-pdl",
    "claim": "The catalogue's terms page still applies PDL 1.0 and prescribes the 加工 credit form",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/pages/terms",
    "present": ["PDL1.0", "千葉県オープンデータサイト", "を加工して作成"]
  },
  {
    "id": "ichihara-isj-block-live",
    "claim": "MLIT's block-level address file for Ichihara (12219, 24.0a, 504,111 B on 2026-10-06) answers keyless - the join target, fetched into data/ichihara/raw/isj/ on 2026-10-06 (owner call 106)",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12219-24.0a.zip",
    "min_bytes": 400000
  },
  {
    "id": "ichihara-isj-chome-live",
    "claim": "MLIT's town-chome address file for Ichihara (12219, 19.0b, 11,134 B on 2026-10-06) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/12219-19.0b.zip",
    "min_bytes": 2000
  },
  {
    "id": "ichihara-kominato-timetable",
    "claim": "The Kominato Railway's timetable page still carries the 2026-03-14 revision (令和8年3月14日改正) read for the 40-minute 五井-上総牛久 service and the 11-12 trains a day south of 上総牛久, and still runs to 養老渓谷 and 上総中野; a new revision means re-counting the call-86 stretch",
    "kind": "http_contains",
    "url": "https://www.kominato.co.jp/timetable/",
    "present": ["令和8年3月14日改正", "上総牛久", "養老渓谷", "上総中野", "kominato-timetable-2026.pdf"]
  },
  {
    "id": "ichihara-projected-crs",
    "claim": "Ichihara projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.137,
    "expect": "EPSG:32654"
  }
]
```
