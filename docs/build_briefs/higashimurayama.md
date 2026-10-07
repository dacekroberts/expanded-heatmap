# Higashimurayama — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5: `docs/decisions_drafts/staging.md`, "Wave 5, second half", call 109: the
ledgers' skew disclosed). The Step 0 downloads were approved by the owner
2026-10-06 (calls 106, 141, 147). **Step 0 measured 2026-10-06** (staging).
Each file from its publisher's own host with the project user-agent:

- **Cached before this brief**, in `data/tokyo_tama/raw/` (gitignored; one
  copy for the four Tama cities in Band A), from
  `www.hokeniryo.metro.tokyo.lg.jp` (東京都保健医療局), as of 2026-08-31:
  `shokuhin-kyoka-7.csv` (4,486,267 B), `shokuhin-todokede-1-7.csv`
  (1,956,304 B), `kankyo-riyoujo-5.csv` (165,277 B), `kankyo-biyoujo-5.csv`
  (608,582 B), `kankyo-cleaning-5.csv` (173,591 B); in
  `data/tokyo_tama/raw/isj/`, from `nlftp.mlit.go.jp`: `13213-24.0a.zip`
  (60,204 B) and `13213-19.0b.zip` (5,423 B).
- **Downloaded for this brief**, into `data/higashimurayama/raw/`, from
  `www.opendata.metro.tokyo.lg.jp` (the Tokyo catalogue's file host, the
  city's own entry): `20240619_food_business_all.csv`, **566,940 B** (HTTP 200,
  `text/csv`; the catalogue states 567,296 B), approved **as a cross-check
  only** (owner, 2026-10-06, call 147).

MHLW has **no file for 13213**: the per-code request answers HTTP 404 (an error
page, not saved), because the city is licensed by the prefecture's health
centre (below). **566,940 B downloaded in all.**

**Run `python scripts/brief_check.py higashimurayama` before writing any
code.** Then the `japan-city` skill, with the `tokyo-ward` skill for Tokyo's
sources and credits. Shape: **Fukuyama's** for a complete list
(`docs/build_briefs/fukuyama.md`), but one source, no MHLW control and no months
to merge: each ledger is ONE file of every premises on it at its date,
refreshed monthly. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no entry and was not edited). Rail: MLIT
N02-25 cut at the N03 city line, measured through `pipeline/countries/japan.py`
with an in-memory `CITIES` entry. **Tama's brief (`docs/build_briefs/tama.md`)
measures the same ledgers**; its ledger section holds for both.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
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

**✅ The skew is disclosed on the page (owner, 2026-10-06, call 109)**: about
20% of rows opened after the control date (**23.0% here**); the ledger misses
long-standing premises (new permits only from 2019-08; at the control date the
share is 58-75% across the eight Tama cities, **68.9% here**); laundry about
half; opt-outs and closures left out. **法人代表者氏名, the operator's address
and phone are dropped at read** (call 109).

**✅ Licence: the catalogue route, relied on (owner, 2026-10-06, call 108;
Taitō's precedent).** The page links the catalogue entries only (Licence,
below).

**✅ The city's own 2024 snapshot is a cross-check, not a source** (owner,
2026-10-06, call 147). How it compares is below; making it a second source
would be an owner call (open call 2).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Higashimurayama carries `label_tier: "minor"` and goes in the **Japan East**
view (`app/cities.py`); wave 4's first city to land retags Japan into the eight
regions, Higashimurayama into **Kanto**. Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`**: Seibu's private heavy railways hold 7 of the 8 station
groups (JR East 1), no subway, tram or light rail once the Yamaguchi Line is
left out; Yokosuka's precedent for a private-heavy-railway backbone (owner,
2026-10-02).

---

## The one-line summary

**All three buckets from the Tokyo Metropolitan Government's Tama ledgers (CC
BY 4.0 by the Tokyo Open Data Terms, the catalogue route relied on).** The
permit ledger as of **2026-08-31** holds **1,113 Higashimurayama rows, 916
restaurants (飲食店営業), 89.5% of the 1,023 in Tokyo's yearbook (FY2024)**,
flattered: 211 (23.0%) were first permitted after the yearbook's date, so **at
the control date the ledger holds 68.9%**. The notification ledger adds 371
rows (konbini 47 against the yearbook's 48, supermarkets 32 against 36).
Barbers 54, beauty salons 148, laundries 50: **about 84%, 73% and 52%** of
estimates scaled from the 2021 census. Through `japan_eigyo`: **Food service
771, Retail 416** (188 permits + 228 notifications), **Personal services
252**. Block join **99.9%** of 1,439 bucketed rows (2 unplaced). The city's
own 2024-06-18 snapshot holds 970 restaurant rows; 689 premises are on both
lists. **Rail: 8 station groups**, Seibu's five lines and JR East's Musashino
Line, the Seibu Yamaguchi Line's one station left out (its station kept by the
Tamako Line); every stretch read from the operators: **at least 3 trains an
hour 07-18, nothing at or under 11 trains a day**.

---

## Business leg — Tokyo's Tama ledgers

Host `https://www.hokeniryo.metro.tokyo.lg.jp`, ledger page
`/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho` (更新日 2026-09-14).
Higashimurayama is in the **多摩小平保健所** area (小平市、東村山市、清瀬市、東久留米市、西東京市).
The files, their columns, encoding, monthly cycle, the closure and opt-out
rule and the shared-tuple fit are as **Tama's brief, "Business leg"**; in
short: cp932 CSVs, cut to the city by address, no shared-code change needed,
the barber and beauty registers' kind named per file, **法人代表者氏名, 営業者住所,
営業者ビル名 and every phone column dropped at read**, `SOURCE_LINKS` for the
CMS suffixes, `as_of` 2026-08-31.

| Ledger | Higashimurayama rows | Notes |
|---|---|---|
| Permits 食品関係営業台帳（許可） | **1,113** | 新規 1,017 · 更新 96; 37 types |
| Notifications 食品関係営業台帳（届出） | **371** | from 2021-06, 14 rows older |
| 理容所台帳 | **54** | 確認年月日 from 1965 |
| 美容所台帳 | **148** | from 1964 |
| クリーニング所台帳 | **50** | 取次所 33, 一般 17; from 1963 |

### Permits: types, dates and the share

- **Types (37)**: 飲食店営業(一般飲食店) 675, (集団給食) 70, 菓子製造業(その他の菓子製造業)
  40, 飲食店営業(弁当屋) 40, 菓子製造業(生菓子製造業) 32, 飲食店営業(そうざい店) 31,
  (バー・キャバレー) 31, 食肉販売業(一般) 28, 飲食店営業(すし屋) 26,
  菓子製造業(パン製造業) 23, 魚介類販売業(一般) 20, 飲食店営業(そば屋) 20, …
- **The control: Tokyo's yearbook table 19-8** (`data/tokyo/raw/tn24qv190800.csv`,
  令和6, 2025-03-31): 東村山市 飲食店営業 **1,023**. e-Stat counts the Tama area
  only within Tokyo Prefecture, so the yearbook is the official count.
- **916 restaurant rows = 89.5%** of 1,023. **211 (23.0%) were first
  permitted after 2025-03-31**: **at the control date the ledger holds 705,
  68.9%**.
- **The gap, measured on the dates** (as Tama's): 新規 first permits **2019-09-17
  to 2026-08-28** (3, 40, 147, 173, 178, 169, 181, 126 a year from 2019);
  更新 first permits **1965-11-16 to 2015-05-29** (all 76 restaurant renewals
  first permitted before 2017-04). Ledger-wide only 32 of 28,093 rows carry a
  first permit between 2015-06 and 2019-08. The city's snapshot shows what that
  window holds (below).
- **Duplicates**: 11 exact repeats of (address, trade name, type); 992
  distinct (address, trade name) of 1,113. One pin per premises and bucket.
  Every row has a 屋号.

### Notifications (届出): the Retail side

371 rows: その他の食料・飲料販売業(店舗) 67, コンビニエンスストア 47,
その他の食料・飲料販売業(包装) 34, 百貨店、総合スーパー 32, 弁当販売業(自動車以外) 28,
野菜果物販売業(自動車以外) 22, その他の食料・飲料販売業(電子申請（未区分）) 21,
集団給食施設 (several kinds, 54), … 届出年月日: 161 in 2021, then 29-49 a year.
**Against the yearbook**: konbini **47 of 48**, supermarkets **32 of 36**,
野菜果物 22 of 23. Whether to read it is open call 1 (as Tama's).

### Counts through `japan_eigyo`

**Permits: Food service 771, Retail 188** (菓子 95, 食肉 28, 魚介 20,
そうざい製造 14, …). Left out: institutional catering 70, hostess venues 31
(バー・キャバレー), event catering 12 (仕出し屋), inside accommodation 3, and 38
rows of manufacturing types with no rule. **Not a premises: 0.** **Notifications:
Retail 228**; left out: institutional catering 58, not a premises 50, no rule
34, mail order 1.

**Economic Census control** (`scripts/japan_census_control.py` at build): the
2021 census counts **404** 飲食店 establishments in 13213
(`docs/coverage_sweep/japan_universe_mhlw.csv`); 761 distinct placed
Food-service premises is **1.88 per establishment**, inside the built cities'
1.56-1.92.

### Personal services: the registers

| Register | Rows | Census 2021 (9-1A) | Estimate (Hachiōji's licensed/census) | Share | (Tokyo's ratio) |
|---|---|---|---|---|---|
| 理容所 barbers | **54** | 57 | 64 | **84%** | 79% |
| 美容所 beauty salons | **148** | 130 | 204 | **73%** | 54% |
| クリーニング所 laundries | **50** (取次所 33, 一般 17) | 55 | 96 | **52%** | 57% |

The estimates and their two ratios are Tama's brief's (e-Stat lists no
Tama-area city but Hachiōji). **Standing registers** (確認年月日 back to the
1960s): the permits' skew does not reach them. Laundry "about half" is
disclosed (call 109). No repeats.

## The city's own snapshot (2024-06-18): a cross-check only (call 147)

Catalogue entry **`t132136d3100000018`** 東村山市食品等営業許可・届出一覧 (CC-BY-4.0;
resource last modified 2024-06-18), file
`https://www.opendata.metro.tokyo.lg.jp/higashimurayama/20240619_food_business_all.csv`.

- **The national schema, 34 columns** (全国地方公共団体コード, ID, 施設名称,
  営業の種類, 業態 (empty), 所在地_連結表記, 町字 split columns, 緯度, 経度,
  施設電話番号, 郵便番号, 法人名, 法人番号 (empty), 初回許可年月日, 廃業年月日
  (empty), 申請区分, …). UTF-8 with BOM; `city_rows` reads it as it stands.
  **1,563 rows**, every address in 東村山市; 申請区分 新規 758, 更新 470, blank 335
  (the notifications); first permits 1965-11-16 to 2023-04-28. No closure is
  marked: closed premises are out, as in the ledger.
- **970 open restaurant rows**, 94.8% of FY2024's 1,023, against the ledger's
  916 (89.5%) 26 months later.
- **Premises on both**, keyed on (town, chōme, block, trade name) for
  restaurants: **689 on both, 206 only in the ledger** (126 of them first
  permitted after the snapshot's date), **262 only in the snapshot**: closed
  since, renamed, or premises the ledger misses. **133 of the 262 were first
  permitted in 2017-2022, 74 of them in 2017-2019**, the window the ledger
  lacks; the rest are older. So the snapshot confirms the disclosed skew is
  real at street level, not an artefact of the yearbook.
- **Its own coordinates check the join**: the block join on the snapshot's
  own 1,540 premises rows lands **a median 38 m** from the city's point (p90 82
  m, 99.0% within 250 m, none over 1 km; 1,539 at block tier).
- **Privacy, if it is ever read**: 法人名 filled on 869 rows (832 with a
  company marker), phone on 1,309; neither is selected. It is not read by the
  build under call 147.

## MHLW: no file for 13213, so no control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13213_food_business_all.csv`
answers **HTTP 404** (not saved). The prefecture's file (13000) holds the Tama
area's rows; the scoping measured **0 addressed open restaurants** for
Higashimurayama in it (`japan_universe_mhlw.csv`). Not downloaded, not needed.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13213-24.0a.zip` (60,204 B,
**1,819 block keys**), town-chōme `.../19.0b/13213-19.0b.zip` (5,423 B,
**53**). `japan.CITIES` entry at build: `"higashimurayama": {"name": "東村山市",
"pref": "13", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["13213"]}`. ⚠️ **One ISJ directory per city**
(`data/higashimurayama/raw/isj/`): `data/tokyo_tama/raw/isj/` holds four
municipalities keyed under ward "" (Tama's brief).

| Tier, today's shared code (all buckets, 1,439 rows) | Block | Town-chōme | Unplaced |
|---|---|---|---|
| **All** | **99.9%** | 0.0% | **0.1%** (2) |
| Food service, permits (771) / Retail, permits (188) | 100% / 100% | 0 | 0 |
| Retail, notifications (228) | 99.1% | 0 | 0.9% (2) |
| Barbers (54) / beauty (148) / laundry (50) | 100% | 0 | 0 |

Staging's permits-and-registers measurement gave 100% on 1,211 rows. **The
two misses**: notifications whose address is a town written "…周辺" (around)
with no number, or no town at all. No rule is proposed.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_13_GML.zip`, N03 code 13213
(**17.13 km²**, extent W 139.440, S 35.735, E 139.505, N 35.782; centroid
139.472, 35.759). Scratch `rail.py`.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 新宿線 (西武鉄道, 12) | Seibu Shinjuku Line | **2 / 29** | 東村山, 久米川 |
| 国分寺線 (西武鉄道, 12) | Seibu Kokubunji Line | **1 / 5** | 東村山 |
| 西武園線 (西武鉄道, 12) | Seibu Seibu-en Line | **2 / 2** | 東村山, 西武園 |
| 多摩湖線 (西武鉄道, 12) | Seibu Tamako Line | **4 / 7** | 萩山, 八坂, 武蔵大和, 多摩湖 |
| 拝島線 (西武鉄道, 12) | Seibu Haijima Line | **1 / 8** | 萩山 |
| 武蔵野線 (東日本旅客鉄道, 11) | JR Musashino Line | **1 / 27** | 新秋津 |
| 山口線 (西武鉄道, 16) | Seibu Yamaguchi Line (Leo Liner) | **1 / 3** | 多摩湖 (**left out**) |

- **12 station records, 8 N02_005g groups**: 東村山 (Shinjuku, Kokubunji,
  Seibu-en), 萩山 (Tamako, Haijima), 多摩湖 (Tamako, Yamaguchi), 久米川, 八坂,
  武蔵大和, 西武園, 新秋津; each group's records 0 m apart. Nearest-group gaps 599
  m (西武園 to 多摩湖) to 3,241 m (新秋津 to 東村山): rings by the spacing rule
  at build.
- **The Yamaguchi Line's one station, left out (calls 54, 92).** The Leo Liner
  (AGT, class 16, an urban line) keeps 1 of its 3 stations here, 多摩湖, in the
  SAME N02 group as the Tamako Line's 多摩湖; the other two (遊園地西, 西武球場前)
  are in Saitama (Tokorozawa's page draws the line cut). The Tamako Line keeps
  the station, so the Leo Liner is left out (`config.LEFT_OUT_LINES`), printed
  by step 1, never written to `excluded_stations.csv`, and named in a bullet
  under **The lines** (the wording: Urayasu's and Suita's built bullet, or a
  proposal in the drafts file).
- **Stubs kept as cut (standing call 3)**, each a JR or private line, so no
  owner question: the **Musashino Line** keeps 1 of 27 (新秋津; Kobe's JR
  Takarazuka Line); the **Kokubunji Line** 1 of 5 (東村山, its terminus) and
  the **Haijima Line** 1 of 8 (萩山, its junction), both stations also served
  by other lines. ⚠️ At build: each stub's permanent label and legend entry on
  its short drawn length (Akita's Oga Line note).
- **秋津 (Seibu Ikebukuro Line) is not a station of the city**: N02-25 puts its
  platform **12 m outside** the city line, in 清瀬市, 285 m from 新秋津. Not
  inside, so no ring and the Ikebukuro Line is not drawn (the standing
  city-line rule); a premises near it goes to 新秋津. The build checks it in the
  scratch render.
- **Cut at the line** (named by N03 municipality at build): the Shinjuku Line
  27 beyond (Saitama 8, 中野区 5, 新宿区 4, 杉並区 3, 西東京市 3, 練馬区 2, 小平市 2,
  …), the Musashino Line 26 (other prefectures 22, 府中市 2, 小平市 1, 国分寺市 1),
  the Haijima Line 7 (立川市 3, 小平市 2, 昭島市 1, 東大和市 1), the Kokubunji Line
  4 (小平市 2, 国分寺市 2), the Tamako Line 3 (小平市 2, 国分寺市 1). The Seibu-en
  Line lies wholly inside.
- **The light-rail/rail test**: every drawn line is heavy rail (classes 11,
  12). The Leo Liner (16) is the only urban line, and it is left out.
- **Frequency, read 2026-10-06 from the operators' own timetables** by plain
  GET with the project user-agent: Seibu's (`seibu.ekitan.com/norikae/timetable/station/<code>/d1|d2?dw=0`,
  the station-line codes from the timetable page's own script, linked from
  `seiburailway.jp`) and JR East's (`timetables.jreast.co.jp`, index
  `timetable/list0855.html`, weekday pages `2610/timetable/tt0855/0855010.html`
  and `0855020.html`). Every departure on each page counted, marked trains
  included:

  | Station (line, direction) | Weekday departures | Per hour 07-18 | 10-16, longest gap |
  |---|---|---|---|
  | 東村山 (Shinjuku, to 西武新宿 / to 本川越) | 160 / 161 | 7-13 | 10-11 min |
  | 久米川 (Shinjuku, both ways) | 130 / 135 | 6-10 | 11 min |
  | 東村山 (Kokubunji, to 国分寺) | 110 | 6-8 | 11 min |
  | 東村山 → 西武園 / 西武園 → 東村山 (Seibu-en) | 65 / 64 | 3-5 | 21-22 min |
  | 萩山 (Haijima, to 西武新宿 / to 拝島) | 114 / 113 | 5-9 | 10 min |
  | 萩山 (Tamako, to 国分寺 / to 多摩湖) | 109 / 83 | 3-6 | 10 / 20 min |
  | 八坂, 武蔵大和 (Tamako, both ways) | 82-83 | 3-6 | 20 min |
  | 多摩湖 (Tamako, to 国分寺) | 82 | 3-6 | 20 min |
  | 新秋津 (Musashino, to 西船橋 / to 府中本町) | 122 / 127 | 5-12 | 12-14 min |
  | *(多摩湖, Yamaguchi, left out)* | *42* | *2-3* | *20 min* |

  **No stretch is at or under about 11 trains a day** (call 86): the
  thinnest drawn stretches, the Seibu-en Line and the Tamako Line, run every
  20 minutes midday. ⚠️ **Seibu's pages mark some departures** (`ekptime
  underline`, trains starting at that station): a reader matching only
  `class="ekptime"` reads the Seibu-en and Tamako termini as 0 (it did here
  first). The counts above match every `ekptime` class. JR East's are counted
  per `timetable_time` cell (the jre.py trap). Only counts are recorded, never
  a timetable on the page.
- ⚠️ **Gate 3** at build: Seibu's and JR East's own station counts inside the
  city (Seibu 7 groups, JR 1). **OSM `name:en`** for 8 groups (one Overpass
  query at build, in the box below; not queried here).

## Scope

**Higashimurayama City.** The Shinjuku Line runs on to 所沢 and 西武新宿, the
Kokubunji and Tamako Lines to 国分寺, the Haijima Line to 小平 and 拝島, the
Musashino Line to 府中本町 and 西船橋; cut at the line. The Leo Liner and the
Ikebukuro Line are not drawn.

## Licences — as read by staging

- **Tokyo's Tama ledgers: PERMITTED WITH CONDITIONS through the catalogue
  route, relied on** (licence-read agent, recorded by staging in
  `docs/decisions_drafts/staging.md`, "Wave 5, second half"; owner, call 108,
  Taitō's precedent). Catalogue entries **`t000055d0000000361`** (food) and
  **`t000055d0000000614`** (barber, beauty, laundry), `CC-BY-4.0`, the Tokyo
  Open Data Terms. **The page links the catalogue entries only**
  (`https://catalog.data.metro.tokyo.lg.jp/dataset/t000055d0000000361`,
  `…/t000055d0000000614`), never the host site below its top page. **The
  credit**: the Terms' §2(1)イ modified-use form; take the exact wording from
  staging's record. **MUST NOT** present the map as made by Tokyo or the city.
- **The city's snapshot** (`t132136d3100000018`): CC BY 4.0 as the catalogue
  declares, the Tokyo Open Data Terms (the Tokyo catalogue's row in
  `docs/data_sources/japan.md`, read 2026-09-24). Read for a cross-check only:
  at build it gets a measurement-source row (not drawn), as e-Stat has; no
  credit on the map unless open call 2 makes it a source.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **Tokyo's yearbook, e-Stat's census,
  Seibu's and JR East's timetables**: read for counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **営業者氏名 is read IN MEMORY for the name rule only**, never written.
  Permits fill it on 583 of 1,113 rows (**566 with a company marker, 17
  without**), notifications 259 of 371 (246, 13); the registers only for
  companies (9, 51, 26, all marked).
- **The name rule, measured in memory** (answers only): **1 permit row**
  withheld, by the sign rule (a bare personal name as the trade name); 0 in
  the notifications and registers. **Dropping 法人代表者氏名 costs 0** (526
  permit rows fill it).
- **Never selected**: 法人代表者氏名, 営業者住所, 営業者ビル名, every phone column.
- Run `check_personal_exposure.py higashimurayama` (`japan=True`) after step
  2: it must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.440-139.505 E, centroid 139.472:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded
out: (35.73, 139.44, 35.79, 139.51). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at build
from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls above; Band A with the
skew disclosed (call 109); the catalogue route (call 108); 法人代表者氏名,
addresses and phones dropped at read; the snapshot as a cross-check only (call
147); `mode: metro`; the minor tier and Japan East (Kanto after the retag); the
Leo Liner left out (calls 54, 92); the Musashino, Kokubunji and Haijima stubs
drawn as cut (standing call); no frequency floor.

**Answered by the owner on 2026-10-06:** call 169, **MHLW's rows the ledgers lack added** for all four Tama cities (Tokyo wards' precedent of 2026-09-24: the ledger's row kept where both hold a premises, `SUPERSEDES`; MHLW's PDL 1.0 notice line added; the share the page states stays without MHLW's rows). The recommendations below are kept as the record.

**Weighed, with a recommendation:**

1. **Read the notification ledger into Retail** (228 bucketed rows). *Recommend
   yes*, decided once for the four Tama cities (Tama's open call 1: the same
   catalogue entry and licence, the Tokyo wards' 許可・届出 precedent; konbini 47
   of 48, supermarkets 32 of 36). Tradeoff: a complete notification stream
   beside a skewed permit stream, said on the page.
2. **The 2024 snapshot as a second source?** *Recommend no, keep it a
   cross-check* (call 147). It would bring back up to 262 restaurant premises
   the ledger lacks (74 first permitted 2017-2019), but it is 26 months old,
   marks no closure, and no other Tama city has one, so the four pages would
   stop being comparable. Tradeoff: a share nearer the yearbook (the snapshot
   alone reaches 94.8%) against stale rows the page could not date, and a
   second credit.

## What the build must still measure

- The per-city ISJ directory; `SOURCE_LINKS` for the monthly files and their
  suffixes; `as_of` 2026-08-31 from the page, never today.
- The share every build (`OFFICIAL_SHARES`, the yearbook through
  `japan_official.py`): 916 of 1,023, and the at-control-date share the page
  states (68.9%), measured, never typed.
- Gate 3; OSM `name:en`; the three stubs' labels; 秋津 in the render; line
  colours on both basemaps; the opening view (`map-view`); the factory share;
  the census ratio (1.88); `check_provenance.py`; `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "higashimurayama-ledger-page",
    "claim": "The ledger page names Higashimurayama in the 多摩小平保健所 area, the 2026-08-31 date, the permits' windows and the opt-out and closure rule",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["多摩小平保健所（小平市、東村山市、清瀬市、東久留米市、西東京市）", "令和8年8月31日現在", "平成29年1月から令和8年8月までの新規許可施設", "廃止・休止している施設は除いて公表"]
  },
  {
    "id": "higashimurayama-ledger-edition",
    "claim": "The edition measured here: the five CSVs under these names (a failure means a new edition or new suffixes: re-measure)",
    "kind": "http_contains",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/kenkou/hokenjo_daicho/shokuhineigyokyokadaicho",
    "present": ["shokuhin-kyoka-7", "shokuhin-todokede-1-7", "kankyo-riyoujo-5", "kankyo-biyoujo-5", "kankyo-cleaning-5"]
  },
  {
    "id": "higashimurayama-permits-file",
    "claim": "The permit ledger (4,486,267 B) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/shokuhin-kyoka-7",
    "min_bytes": 4000000
  },
  {
    "id": "higashimurayama-registers-file",
    "claim": "The beauty register (608,582 B) answers a plain GET (the barber and laundry files sit beside it: tama.md checks all three)",
    "kind": "http_ok",
    "url": "https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/kankyo-biyoujo-5",
    "min_bytes": 450000
  },
  {
    "id": "higashimurayama-catalogue-food",
    "claim": "The catalogue entry the page links for the food ledgers declares CC-BY-4.0",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000361",
    "present": ["CC-BY-4.0", "t000055d0000000361", "shokuhineigyokyokadaicho"]
  },
  {
    "id": "higashimurayama-catalogue-registers",
    "claim": "The catalogue entry the page links for the barber, beauty and laundry ledgers declares CC-BY-4.0",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000055d0000000614",
    "present": ["CC-BY-4.0", "t000055d0000000614"]
  },
  {
    "id": "higashimurayama-snapshot-entry",
    "claim": "The city's own catalogue entry still offers the 2024-06-19 snapshot (the cross-check, call 147) under CC-BY-4.0",
    "kind": "http_contains",
    "url": "https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t132136d3100000018",
    "present": ["CC-BY-4.0", "20240619_food_business_all.csv"]
  },
  {
    "id": "higashimurayama-snapshot-file",
    "claim": "The snapshot (566,940 B served) answers a plain GET",
    "kind": "http_ok",
    "url": "https://www.opendata.metro.tokyo.lg.jp/higashimurayama/20240619_food_business_all.csv",
    "min_bytes": 500000
  },
  {
    "id": "higashimurayama-no-mhlw-file",
    "claim": "MHLW has no per-city file for 13213 (HTTP 404): the prefecture licenses the city, so no MHLW control",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=13213_food_business_all.csv",
    "expect_status": 404
  },
  {
    "id": "higashimurayama-isj-block-live",
    "claim": "MLIT's block-level address file for Higashimurayama (13213) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/13213-24.0a.zip",
    "min_bytes": 50000
  },
  {
    "id": "higashimurayama-isj-chome-live",
    "claim": "MLIT's town-chōme file for Higashimurayama (13213) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/13213-19.0b.zip",
    "min_bytes": 4000
  },
  {
    "id": "higashimurayama-seibu-shinjuku-timetable",
    "claim": "Seibu's weekday timetable for 東村山 on the Shinjuku Line toward 西武新宿 (238-20/d1), one of the pages counted",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/238-20/d1?dw=0",
    "present": ["東村山", "新宿線", "平日", "ekptime"]
  },
  {
    "id": "higashimurayama-seibu-tamako-timetable",
    "claim": "Seibu's weekday timetable for 八坂 on the Tamako Line (234-0/d1), the thinnest drawn line (every 20 minutes midday)",
    "kind": "http_contains",
    "url": "https://seibu.ekitan.com/norikae/timetable/station/234-0/d1?dw=0",
    "present": ["八坂", "多摩湖線", "平日", "ekptime"]
  },
  {
    "id": "higashimurayama-jr-shin-akitsu-timetable",
    "claim": "JR East's timetable index for 新秋津 (list0855) links the two weekday Musashino Line pages counted. ASCII ids only: the host sends no charset",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0855.html",
    "present": ["tt0855/0855010.html", "tt0855/0855020.html"]
  },
  {
    "id": "higashimurayama-projected-crs",
    "claim": "Higashimurayama projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.47,
    "expect": "EPSG:32654"
  }
]
```
