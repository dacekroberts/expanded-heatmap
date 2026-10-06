# Tsu — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, calls 48 and 67; `docs/decisions_drafts/staging.md`, "Wave 5: the ranked
queue and the pre-verdicts screened": "**A:** Ichinomiya, Tsu, …"). The Step 0
downloads were approved by the owner the same day. **Step 0 measured
2026-10-06** (staging). Into `data/tsu/raw/` (gitignored), each from its
publisher's own host, project user-agent, each HTTP 200:

- From BODIK (`data.bodik.jp`, Mie Prefecture, organisation 240001), 25 s
  apart: the three resources, all three published as `…/download/202608.xlsx`,
  saved under distinct names as Toyota's are (`pipeline/toyota/config.py`):
  `food_202608.xlsx` (**1,563,961 B**), `riyo_202608.xlsx` (barbers,
  **131,279 B**), `biyo_202608.xlsx` (beauty, **331,813 B**).
- From `i2fas.mhlw.go.jp`: `24000_food_business_all.csv`, **Mie Prefecture's
  file** (1,271,314 B), the control.
- From `nlftp.mlit.go.jp`: `isj/24201-24.0a.zip` (425,115 B) and
  `isj/24201-19.0b.zip` (10,175 B).

3,733,657 B in all. Nothing else was downloaded. **There is no laundry list**
(Mie publishes none on BODIK: the catalogue search for `240001_cleaning`
returns nothing; the city's own organisation, 242012, holds no permit lists):
**a disclosed gap.**

**Run `python scripts/brief_check.py tsu` before writing any code.** Then the
`japan-city` skill, **Yokkaichi's shape** (a standing register per kind, one
municipality, no wards; `docs/build_briefs/yokkaichi.md`) with **Uji's one
difference: the files are the prefecture's**, so every row is assigned to Tsu
by its address (below). Coordinates: the `address-join` skill, measured with
the shared `pipeline/countries/japan_register.py` functions from scratch
scripts (`scripts/screen_japan_join.py` has no Tsu entry; its table is shared
code and was not edited). Rail: MLIT N02-25 cut at the N03 city line, through
`pipeline/countries/japan.py` with a scratch `CITIES` entry (none was added to
the shared module).

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
holds; (6) **no page says "currently operating"**. Also: no frequency floor for
JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at about
11 trains a day or fewer **named and drawn** (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Tsu
carries `label_tier: "minor"` and `"region": "Japan East"`, as Yokkaichi does
(`app/cities.py`); wave 4's first city to land retags Japan into the eight
regions, and **Mie is Kansai** (the `japan-city` skill), so Tsu moves with
Yokkaichi. Tsu's dot (34.719, 136.506) sits about 30 km south-southwest of
Yokkaichi's (34.9665, 136.6189): its label offset from `check_macro_labels.py`
(PROBLEMS 0 at 375, 768 and 1200), never by eye.

**`mode`: `metro`** by the owner's rule of 2026-10-02. No subway, tram or light
rail; all five lines are conventional railways (N02 class 11 or 12). JR
Central has 16 station groups against Kintetsu's 15 and the Ise Railway's 4
(津 is shared by all three), so JR is the largest network ("substantial JR
reads as metro": Okayama, Kitakyushu).

---

## The one-line summary

**All three buckets but laundry, from Mie Prefecture's monthly standing lists
on BODIK (CC BY 4.0 as stated), cut to Tsu by address, as of 2026-08-31:
2,924 food permits (2,166 restaurants, 209 of them old-law), 251 barbers and
701 beauty salons.** No per-city official count exists (Tsu is neither a
designated nor a core city); prefecture-wide, the list plus Yokkaichi's own
holds **83.0% of e-Stat's FY2024 restaurants in force** (17 months earlier,
across heavy old-law attrition), **97.6% of barbers and 102.0% of beauty
salons**. Through `japan_eigyo`: **Food service 1,806 rows (1,786 pins),
Retail 678 (562), Personal services 952 (949 pins; 2 premises sit in both
lists)**. Block join **78.4%** for food
(19.9% town or 大字 centroid, 1.7% unplaced), lower than the built cities
because MLIT's block file does not cover the 2006 merger's rural towns. The
Economic Census control reads **2.01**, above every built city (build item).
**Rail: 33 N02 station groups** (JR Meishō 12, Kintetsu Nagoya 10, Kintetsu
Ōsaka 5, JR Kisei 4, Ise Railway 4; 津 shared by three), the rural JR Meishō
Line drawn under call 86.

---

## Business leg — Mie Prefecture's lists on BODIK (organisation 240001)

Host `https://data.bodik.jp` (CKAN). Each package states CC BY 4.0
(`license_id: cc-by-40-intl`), covers **the prefecture except Yokkaichi**
(「三重県内（四日市市に所在する施設を除く）」: Yokkaichi publishes its own,
`docs/build_briefs/yokkaichi.md`), and is **updated about the 15th of each
month with the previous month's applications and notifications**
(「原則として、毎月15日頃に、前月に受付をした申請、届出等を反映し、施設の一覧を更新します」;
「※現在は令和８年８月末までのデータを掲載しています」). Every resource is
datastore-backed; all three uploaded 2026-09-15.

| Dataset (package) | Resource | Bytes | Rows (prefecture) | **Tsu** | Columns |
|---|---|---|---|---|---|
| 食品営業許可施設 (`240001_food_business_all`) | `796b84b4-…/resource/fc9fba2d-e6f7-4139-ba20-3e572ba99572/download/202608.xlsx` | **1,563,961** | **18,680** | **2,924** | 初許可日, **業種**, **業態**, operator **営業者氏名**, **営業所住所**, **営業所屋号**, 営業所電話番号 (never), 許可番号 |
| 理容所届出施設 (`240001_barbar`) | `b3d52d9a-…/resource/8a273176-3714-46de-ba68-aeb2b5742c09/download/202608.xlsx` | **131,279** | **1,523** | **251** | 確認年月日, operator **開設者氏名**, **施設住所**, **屋号**, 施設電話番号 (never), 確認番号 |
| 美容所届出施設 (`240001_hair_dressing`) | `824ac0dd-…/resource/2a625a1b-2efe-4876-9859-49ad35363608/download/202608.xlsx` | **331,813** | **3,853** | **701** | as barbers |

- Each workbook is one sheet (`【オープンデータ（県庁）】…`), header on row 1,
  every cell a string. **The food list carries no expiry and no status
  column**: only 初許可日 (the first permit, 1928 onwards; latest 2026-08-29).
  The registers' latest 確認年月日: barbers 2026-06-10, beauty 2026-08-19.
- **No vehicle, stall or vending row in the food list**: 0 of 18,680 rows
  carry a vehicle, stall, temporary or vending 業態, and 0 a `一円` / `県内`
  address (Yokkaichi's list states that exclusion; Mie's does not, but the
  list holds none). **196 food rows prefecture-wide have no address** (154
  restaurants, 26 菓子): unassignable to any town, and not in Tsu's count.
- ⚠️ **Columns against `japan_register` (shared code, not edited here)**:
  `NAME_COLS` lacks **営業所屋号** (without it every food row reads no trade
  name, so the name rule compares nothing and one pin per premises keys on the
  address alone). `ADDR_COLS` has 営業所住所 and 施設住所, `NAME_COLS` 屋号,
  `TYPE_COLS` 業種, `FORM_COLS` 業態, `OPERATOR_COLS` 営業者氏名 and 開設者氏名.
  The scratch measurement renamed 営業所屋号 in memory. Add it and re-run the
  Minato control.

### Cutting Tsu out of the prefecture's lists

- **The rule: an address that begins `津市` or `三重県津市`** (after NFKC and
  spaces removed). Food addresses carry no prefecture (all 2,924 begin
  `津市`); the registers mix both (barbers 235 + 16, beauty 219 + 482).
- **Nothing else reaches Tsu**: 0 rows in any file contain 津市 without
  beginning with it, and 0 rows parse to no municipality (barbers 3 and
  beauty 9 parse oddly, none starts with a Tsu town name of MLIT's file).
  No municipality code column exists; the build's `config.source_rows` cuts
  by the prefix and **raises** on any row that contains 津市 elsewhere.
- **The check that the cut is whole**: Tsu holds 16.1% of the list's
  restaurants (2,166 of 13,438) and 16.4% of the 2021 Economic Census's 飲食店
  outside Yokkaichi (872 of 5,307).
- **The probe's prefix counts were lower bounds** (2,924 food, 252 barbers,
  at least 482 beauty): by address, **2,924 food, 251 barbers, 701 beauty**
  (the probe's beauty count missed the 219 rows written `三重県津市`).

### Food by type, through `japan_eigyo` (measured)

| | Rows | Kept | Out (rule) |
|---|---|---|---|
| Restaurants (飲食店営業 1,957 + （旧） 209) | 2,166 | **1,805 Food service** (+ 1 old-law 喫茶店営業: 1,806) | **119 委託給食** (institutional) · **78 仕出し屋、弁当屋** (仕出し) · **66 バー、キャバレー** (hostess, R3) · 33 旅館、ホテル · 65 惣菜店 to Retail by 業態 |
| Food retail permits (菓子 344, そうざい 99, 魚介類販売 99, 食肉販売 71) | 613 | **678 Retail** with the 65 惣菜店 | |
| Other permit types (manufacturing, 食肉処理, 小分け …) | 144 | 0 | "no rule" |

- **業態 is MHLW's national form list**, as Yokkaichi's: 飲食店営業（その他）
  615 + 81 old-law is its catch-all, inside the restaurant bucket either way.
  The バー、キャバレー share is 3.0% of restaurants here (Yokkaichi 19%): the
  precedent applies, no new call.
- **Old law**: 266 rows (209 restaurants, 9.6% of Tsu's restaurants; 25 菓子,
  13 魚介類, 8 食肉 …), first permitted 1968 to 2021, numbered `津 保第 …
  号`; the 2,658 new-law permits `津NNNN-NNNN` (津 the health centre). New-law
  restaurants by first-permit year: 2021 213 · 2022 342 · 2023 372 · 2024
  425 · 2025 394 · 2026 211.
- **Factory share**: 26 of 443 菓子 / そうざい Retail rows (5.9%) are named 工場
  or センター, kept (the 2026-09-27 call).
- **Duplicates**: 2,924 distinct 許可番号. 31 (address, trade name, type)
  groups repeat under another number (69 rows); 2,557 distinct (address,
  trade name) premises. **One pin per (address, trade name, bucket): 2,348**
  (Food service 1,786, Retail 562).

### Completeness and closed premises

**No official per-city count**: e-Stat's 衛生行政報告例 carries prefectures,
designated cities and core cities only
(`docs/coverage_sweep/japan_universe_mhlw.csv` has no official count for
24201). Prefecture-wide, e-Stat FY2024 (2025-03-31) against Mie's list plus
Yokkaichi's own (both 2026-08-31; the 三重県 row includes Yokkaichi):

| | e-Stat in force | Mie (ex-Yokkaichi) + Yokkaichi | Share |
|---|---|---|---|
| Restaurants (飲食店営業) | **19,626** (old law 5,850, revised 13,776) | 13,438 + 2,855 = **16,293** (old law 1,051 + 159) | **83.0%** |
| Barbers (第10表) | **1,782** | 1,523 + 216 = 1,739 | **97.6%** |
| Beauty salons (第10表) | **4,500** | 3,853 + 737 = 4,590 | **102.0%** |

- **The restaurant gap is old-law attrition and churn over 17 months, plus
  the vehicles e-Stat counts and the list holds none of**: the revised-law
  count already exceeds e-Stat's (15,083, 109%), the old-law count is 20.7% of
  it, and in FY2024 alone Mie recorded **3,449 old-law closures** (of 8,516
  old-law premises; e-Stat's note says some systems count a conversion to the
  revised law as a closure) and 3,132 revised-law closures (第1表-2, 第3表-2).
  A like-for-like rate cannot be had; state the 83.0% with its dates.
- **Closures are not marked** and no control exists: no expiry, no status, and
  MHLW's Mie file holds no restaurant permits (below). The monthly update
  reflects notifications received, closures presumably among them; nothing
  verifies it. The census ratio (2.01, below) is the only signal.

### MHLW's file (24000), the control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=24000_food_business_all.csv`:
**1,271,314 B, 4,036 rows** (届出 3,558, 許可 473, 届出(廃業) 4, 許可(廃業) 1),
the national schema, permits 2021-07-01 to 2026-08-01.

- ⚠️ **Trap: 市区町村名 is `津市` and 自治体コード `024000` on every row**: the
  prefecture's seat, as Uji's file names `京都市上京区`. A build that read
  市区町村名 would take all 4,036 rows as Tsu's. Only 1,743 rows carry an
  address; **304 are addressed to Tsu** (届出 240, 許可 64).
- **Not a second source for food service: 0 open restaurant permits** in the
  whole file (the 473 permits are other types). **438 of MHLW's 455 numbered
  open permits are in Mie's list by 許可番号** (17 not, 2 of them Yokkaichi's):
  Mie's list is the complete one, MHLW the opt-in filings.
- **Its 240 Tsu notifications**: 159 reach Retail through the taxonomy (その他の
  食料・飲料販売業 75, supermarkets 54, konbini 8, rice 11 …; 50 vending, 10
  institutional out), **156 pins**, block 121 / chome 32 / unplaced 6, every
  one with MHLW's own point. A partial opt-in layer if the owner wants it
  (open call 1).
- **Independent check**: block point against MHLW's point for the same permit
  number, **median 85 m, 68.0% within 250 m, 2 over 1 km** (50 rows only; read
  more at build with GSI's address search, `screen_japan_join.gsi_check`'s
  method).

---

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 24201)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/24201-24.0a.zip` (425,115 B) and
`…/19.0b/24201-19.0b.zip` (10,175 B): **62,931 block keys** (with the 大字 +
字 + 小字 keys), **324 town-chōme keys**. Ward-less (`"wardless": True`).

| Tier (rows in a bucket) | Food service (1,806) | Retail (678) | Barbers (251) | Beauty (701) | Food, all (2,484) |
|---|---|---|---|---|---|
| Block | 79.7% | 74.8% | 66.9% | 78.0% | **78.4%** |
| Town-chōme / 大字 centroid | 18.4% | 23.9% | 28.3% | 16.8% | 19.9% |
| Unplaced | 1.8% | 1.3% | 4.8% | 5.1% | **1.7%** |

**The misses, read** (towns only):
- **Chōme tier, food (495)**: **279 sit in towns MLIT's block file does not
  carry at all**, the 地番 areas of the 2006 merger (美杉町, 白山町, 一志町,
  美里町, 芸濃町 and 榊原町: 榊原町 26, 美杉町八知 21, 白山町川口 20, 白山町南家城 14,
  稲葉町 11 …). They take the 大字 centroid by design. **216 sit in towns it
  carries, the number missing**: 羽所町 21 (MLIT keys 245 of its numbers; most
  of these rows write a floor straight after the number, `NNNF` / `NNN階`, so
  the number is misread), 芸濃町椋本 15, 博多町 10 (MLIT keys five numbers
  there), 一志町田尻 8.
- A digit-space-digit pre-step (`700 3F` read as `700-3F`, not `7003F` once
  spaces go) lifts food 78.4 → 78.7% and beauty 78.0 → 78.3%: **9 + 2 rows,
  not worth shared code on its own**; read at build.
- **Unplaced (42 food)**: 小字 written without 字 (久居明神町風早 4, 高茶屋小森町中山
  4; MLIT keys 久居明神町字風早), a few 小字 MLIT lacks, one 土地区画整理 address.
  Barbers and beauty: 12 and 36, the same shapes.
- **No publisher coordinates** in Mie's lists.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (24201)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_24_GML.zip`, N03 code 24201
(**710.9 km²**, extent W 136.1597, S 34.4474, E 136.5705, N 34.8445; polygon
centroid 34.660, 136.367, in the hills: the 2006 merger brought in 久居市,
河芸町, 芸濃町, 美里村, 安濃町, 香良洲町, 一志町, 白山町 and 美杉村). **N02-24
agrees** (35 records, 33 groups, no name difference). No Shinkansen.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside (north to south) |
|---|---|---|---|
| 名松線 (東海旅客鉄道, 11) | JR Meishō Line | **12 / 15** | 一志, 伊勢大井, 伊勢川口, 伊勢八太, 井関, 関ノ宮, 家城, 伊勢竹原, 伊勢鎌倉, 伊勢八知, 比津, 伊勢奥津 (its terminus) |
| 名古屋線 (近畿日本鉄道, 12) | Kintetsu Nagoya Line | **10 / 44** | 千里, 豊津上野, 白塚, 高田本山, 江戸橋, 津, 津新町, 南が丘, 久居, 桃園 |
| 大阪線 (近畿日本鉄道, 12) | Kintetsu Ōsaka Line | **5 / 49** | 東青山, 榊原温泉口, 大三, 伊勢石橋, 川合高岡 |
| 紀勢線 (東海旅客鉄道, 11) | JR Kisei Main Line | **4 / 41** | 一身田, 津, 阿漕, 高茶屋 |
| 伊勢線 (伊勢鉄道, 12) | Ise Railway Ise Line | **4 / 10** | 伊勢上野, 河芸, 東一身田, 津 (its terminus) |

- **35 station records, 33 `N02_005g` groups**: 津 (group 006905) holds JR,
  Kintetsu and the Ise Railway, spread 45 m. No name in two groups. JR 16,
  Kintetsu 15, Ise Railway 4.
- **Close pairs kept apart, as N02 keeps them** (trap 1): **川合高岡 (Kintetsu
  Ōsaka) and 一志 (JR Meishō) 179 m**, separate stations of different names
  (Kobe's Tarumi case); 東一身田 (Ise) and 高田本山 (Kintetsu) 561 m.
- **Median nearest-group gap 1,432 m** (179 to 3,120): standard rings by the
  spacing rule.
- **Cut at the line**: Kintetsu Nagoya on to 磯山 (Suzuka) and 伊勢中川
  (Matsusaka); Kintetsu Ōsaka on to 伊勢中川 and 西青山 (Iga); JR Kisei on to
  下庄 (Kameyama) and 六軒 (Matsusaka); JR Meishō on to 権現前 (Matsusaka); the
  Ise Railway on to 中瀬古 (Suzuka).
- **Stub test**: no urban line; every line is a regional railway, none cut to
  one station. **Five lines are drawn.**
- **Frequency.** **Kintetsu READ** by the wave-5 probe (Kintetsu's station
  timetables, `eki.kintetsu.co.jp`, weekday, departures per hour 10:00 to
  15:59, one direction): 津 9 an hour, 江戸橋 and 津新町 5, 久居 and 南が丘 3,
  豊津上野 2. **JR Central and the Ise Railway ASSERTED, not read** (JR
  Central's conventional-line station pages load their timetables by script;
  `www.isetetsu.co.jp` did not resolve from this machine, 2026-10-06):
  - **The JR Meishō Line (一志 to 伊勢奥津, 12 stations) is the rural
    stretch**: believed under 11 trains a day each way, fewest beyond 家城.
    **Drawn and named** under call 86, whatever the count; the build reads
    JR Central's timetable and the page names each stretch at about 11 a day
    or fewer with its count.
  - The **JR Kisei Main Line** (一身田, 阿漕, 高茶屋: locals, the 快速みえ and
    the 南紀 limited express pass) and the **Ise Railway** (伊勢上野, 河芸,
    東一身田), and Kintetsu Ōsaka's five rural stations (東青山 to 川合高岡), are
    believed roughly hourly or better at their stations; read all three at
    build and name any stretch the count puts at about 11 a day or fewer.
- **The light-rail / rail test**: no tram or light rail; `mode` `metro` by the
  JR test.
- ⚠️ **Gate 3** (JR Central, Kintetsu, the Ise Railway per-line station
  counts), OSM `name:en` for 33 groups (not queried for this brief; the build
  fetches its own, one Overpass query), line colours on both basemaps.

## Scope

**Tsu City (24201), one municipality, no wards.** Kintetsu, JR and the Ise
Railway run on into Suzuka, Kameyama, Matsusaka and Iga; cut at the line.
**Laundry is a disclosed gap** (no list); the page is narrowed to food and
barbers and beauty salons.

## Licences — as stated; the full read is pending

- **Mie Prefecture's three lists**: each package records **`license_id:
  cc-by-40-intl`**. The catalogue's terms, 三重県オープンデータ利用規約
  (`https://odcs.bodik.jp/240001/tos/`), 第１条 license the prefecture's works
  under CC BY 4.0 (linking `legalcode.ja`), a resource's own licence
  prevailing; 第３条 asks before using the prefecture's logo alone; 第４条 the
  fault-based cost clause (the class accepted for every Japanese source,
  2026-09-24); 第５条 these terms prevail over another site's for the same
  dataset. **A `licence-read` agent reads the source separately; staging
  records it. No verdict here.** Proposed credit, pending that read:
  `出典：「食品営業許可施設」「理容所届出施設」「美容所届出施設」（三重県、2026-08-31、https://odcs.bodik.jp/240001/）を加工して作成`
  with the CC BY 4.0 link.
- **MHLW open data (24000)**: the control; PDL 1.0 as recorded in
  `docs/data_sources/japan.md` if open call 1 uses it (its credit then joins
  the notice).
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn.

## Privacy

Select 業種, 業態, 営業所住所, 営業所屋号, 初許可日 (food) and 確認年月日,
施設住所, 屋号 (registers). **Never select 営業所電話番号 or 施設電話番号.**
The operator columns are read in memory by the name rule and never kept:

| | Operator column | Filled | Company or cooperative marker | Without a marker | Flagged (v2) |
|---|---|---|---|---|---|
| Food | 営業者氏名 | 2,924 of 2,924 | 1,425 (1,402 companies) | **1,499** | **0** (4 without the `coop` rule, all cooperatives) |
| Barbers | 開設者氏名 | 251 of 251 | 21 | **230** | **0** (1 without `coop`) |
| Beauty | 開設者氏名 | 701 of 701 | 108 | **593** | **1** (trade name equals an individual operator's name), 1 pin |

**0 bare personal names** under the sign rule in any file. The prefecture
publishes sole traders' own names in every operator column, as Yokkaichi's
lists do; nothing reads them for output. No value was printed or stored. Run
`check_personal_exposure.py` with `japan=True` on what reaches the map (it
must print 0) and record the verdict in the drafts file and
`docs/privacy_verdicts.md` at build.

## Region and CRS

`"region": "Japan East"` (Kansai after the retag), `"country": "Japan"`,
`label_tier: "minor"`, `coverage` narrowed (no laundry). Project to **UTM 53N
(EPSG:32653)**: the extent 136.1597 to 136.5705 lies inside the 132-138 band,
and so does the city centre (136.506), computed here, never copied.

**Scaffold**: `scaffold_city.py --slug tsu --name Tsu --system-name "JR
Central, Kintetsu and the Ise Railway" --taxonomy japan_eigyo --lat 34.719
--lon 136.506 --region "Japan East" --country Japan --mode metro
--page-number <N>` (`--dry-run` first; the city centre, not N03's centroid in
the hills), with the page number claimed in `docs/session_roles.md` at build,
not here. A `japan.CITIES` entry: `"tsu": {"name": "津市", "pref": "24",
"epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True, "wards":
["24201"]}`. `SOURCE_FILES` under the three names above; `SOURCE_AS_OF`
2026-08-31 for each (the dataset notes), never today.

## Owner calls

**Made:** Band A (owner, 2026-10-06, calls 48 and 67); the Step 0 downloads
(owner, 2026-10-06); laundry a disclosed gap (the band row); no frequency
floor (call 46) and the rural stretches drawn and named (call 86); the
standing Japanese calls above; バー、キャバレー out (R3, the precedent).

**Open:**
1. **MHLW's Tsu notifications as a partial, opt-in Food-shops layer** (240
   addressed to Tsu, **159 Retail rows, 156 pins**: supermarkets, konbini,
   other food sales), disclosed as partial as in Uji, Kurume and Matsuyama.
   *Recommend yes*: Mie's list holds permits only, so without it no
   supermarket or konbini that only notifies is on the map. Tradeoff: a
   bucket the page must call partial, MHLW's PDL credit added to the notice,
   and a source approved as a control becomes a source.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control,
  `screen_japan_join.py minato` 98.0 / 0.2 / 1.8, and every city screen):
  `NAME_COLS` + 営業所屋号; Tsu's `japan.CITIES` entry.
- ⚠️ **`config.source_rows`**: the `津市` / `三重県津市` prefix cut, raising
  on a row that contains 津市 elsewhere; state the 196 prefecture rows with no
  address in the drafts entry. Never 市区町村名 in MHLW's file.
- ⚠️ **The Economic Census control** (`scripts/japan_census_control.py`, after
  step 2): the 2021 census counts **872** 飲食店 establishments in 24201;
  1,753 placed Food-service pins is **2.01 per establishment, above the built
  cities' 1.56-1.92** (Yokkaichi's brief 1.82). Read why on the built pins
  (repeat permits at one premises, closures the monthly update kept, or a
  census undercount), and draft any closure sentence for the page as a
  review-time proposal; the page never says "currently operating".
- ⚠️ The JR Central and Ise Railway counts (call 86's names on the page), gate
  3, OSM `name:en` and the 179 m pair's labels, line colours on both basemaps,
  the macro label against Yokkaichi's, the opening view (`map-view`), the
  factory share printed by step 2, `check_provenance.py`,
  `check_scope_disclosure.py` (the laundry gap in
  `docs/excluded_categories.md`).

```brief-checks
[
  {
    "id": "tsu-bodik-packages",
    "claim": "Mie Prefecture's three BODIK packages (food, barbers, beauty) exist, record CC BY 4.0 and point at the 2026-08 edition of each resource; no 240001_cleaning package exists (the laundry gap)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=name:(240001_food_business_all%20OR%20240001_barbar%20OR%20240001_hair_dressing%20OR%20240001_cleaning)&rows=10",
    "present": ["\"count\": 3", "\"license_id\": \"cc-by-40-intl\"", "\"name\": \"240001_food_business_all\"", "\"name\": \"240001_barbar\"", "\"name\": \"240001_hair_dressing\"", "fc9fba2d-e6f7-4139-ba20-3e572ba99572/download/202608.xlsx", "8a273176-3714-46de-ba68-aeb2b5742c09/download/202608.xlsx", "2a625a1b-2efe-4876-9859-49ad35363608/download/202608.xlsx"],
    "absent": ["\"name\": \"240001_cleaning\""]
  },
  {
    "id": "tsu-mhlw-live",
    "claim": "MHLW's open-data file for Mie Prefecture (24000), the control, answers a plain keyless GET (1,271,314 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=24000_food_business_all.csv",
    "min_bytes": 1000000
  },
  {
    "id": "tsu-isj-block-live",
    "claim": "MLIT's block-level address file for Tsu (24201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/24201-24.0a.zip",
    "min_bytes": 300000
  },
  {
    "id": "tsu-isj-chome-live",
    "claim": "MLIT's town-chome address file for Tsu (24201) answers keyless - the centroid tier",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/24201-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "tsu-terms-cc-by-4",
    "claim": "三重県オープンデータ利用規約 第１条 licenses the prefecture's works under CC BY 4.0 (the Japanese legal code linked)",
    "kind": "http_contains",
    "url": "https://odcs.bodik.jp/240001/tos/",
    "present": ["三重県オープンデータ利用規約", "licenses/by/4.0/legalcode.ja"]
  },
  {
    "id": "tsu-projected-crs",
    "claim": "Tsu projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 136.506,
    "expect": "EPSG:32653"
  }
]
```
