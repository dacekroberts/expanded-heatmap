# Yachiyo — build brief

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
  and **copied byte for byte into `data/yachiyo/raw/`**, as a build's
  `fetch_sources.py` would fetch them into the city's own `raw/`:
  `ichiran-riyou202503.xlsx` (328,249 B), `ichiran-biyou202603.xlsx`
  (765,694 B), `ichiran-clean202603.xlsx` (254,290 B), `shinki-biyou2604.xlsx`
  to `shinki-biyou2608-2.xlsx` and `shinki-clean2604.xlsx` to
  `shinki-clean2608.xlsx`.
- ⚠️ **Not on disk and not fetched: MLIT's address blocks for Yachiyo
  (12221)**. The cached `data/matsudo/raw/isj/` holds Matsudo's 12207 only,
  and the wave-5 approval covers the downloads a task names, which these were
  not. A HEAD request (no body) confirmed both answer:
  `isj/dls/data/24.0a/12221-24.0a.zip` (HTTP 200, 163,101 B, Last-Modified
  2026-05-19) and `…/19.0b/12221-19.0b.zip` (HTTP 200, 6,358 B). **The block
  join is therefore unmeasured** (open call 1).
- Not fetched: MHLW's prefecture file (food is off); the barber months
  (barbers get no months, Matsudo's call 34).

**Run `python scripts/brief_check.py yachiyo` before writing any code.** Then
the `japan-city` skill in **Matsudo's shape** (`docs/build_briefs/matsudo.md`;
Kōchi's config, `pipeline/kochi/config.py`): personal services only, the
publisher is the prefecture, every row assigned to Yachiyo by its sheet AND its
address. Coordinates: the `address-join` skill with the shared
`pipeline/countries/japan_register.py` (`scripts/screen_japan_join.py` has no
Yachiyo entry; add one at build). Rail: MLIT N02-25 cut at the N03 city line,
measured through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a JR or
private one-station stub stays as cut** (2026-09-27; restated for wave 5), and
an urban line (subway, monorail, AGT) with one station in the city is left out
(none here); (4) **菓子製造業 and そうざい製造業 count, in Retail** (moot here);
(5) **the name rule, version 2** (`japan_register.name_is_operator`, on master
2026-10-06): a trade name that IS the operator's own name, or is written as a
bare personal name, shows its permit type, the operator column read in memory
only; (6) **no page says "currently operating"**. Also: fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`, numerals as figures before 丁目; every Japanese city reads
`WAVE2_RULES` (owner, 2026-10-04); **no frequency floor for JR or private
lines** (call 46), and any stretch with about 11 trains a day or fewer is drawn
and named (call 86).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Yachiyo
carries `label_tier: "minor"` and goes in the **Japan East** view as the other
Kantō cities (wave 4's first city retags Japan into the eight regions, Yachiyo
into Kanto). Its label offset comes from `check_macro_labels.py` (PROBLEMS 0
at 375, 768 and 1200), never by eye. **Yachiyo borders Sakura and Funabashi**
(centroids about 10 km from Sakura's): measure the labels together if they land
in one batch.

**`mode`: `metro`** (the owner's rule of 2026-10-02, applied as for Matsudo,
Kurume and Maebashi; staging's reading): no subway, AGT or tram is drawn and no
JR runs here, so the mode follows the backbone, the Tōyō Rapid Line (4 groups,
a railway, N02 class 12, its trains running through onto Tokyo Metro's Tōzai
Line), with the Keisei Main Line (3).

---

## The one-line summary

**Personal services only, from Chiba Prefecture's open-data lists of barbers,
beauty salons and laundries (dataset 6, PDL 1.0), cut to Yachiyo by the 習志野
sheet and the address: 130 barbers (the 2025-03-31 list, built as published
with its own date, Matsudo's call 33), 353 beauty salons (352 premises) and 77
laundry rows (70 premises; 7 have no shop) rebuilt to 2026-08-31 (an upper
bound: closures are not published); 553 storefronts, 551 pins.** The block join
is not measured yet (MLIT's 12221 files are not on disk; open call 1); every
address carries a parseable number. Against a census-based estimate the lists
hold about 108%, 112% (115% rebuilt) and 97%. One barber's trade name is a
bare personal name: the name rule's version 2 shows its category. Rail: **7 N02
station groups** (Tōyō Rapid 4, Keisei 3), two lines drawn.

---

## Business leg — Chiba Prefecture's 環境衛生関係施設一覧 (dataset 6)

The dataset, its notes, files, layout, columns and dates are recorded in
`matsudo.md` (the same files): resource 79 (barbers, served as the 2025-03-31
list although titled 令和8年3月末), 80 (beauty) and 81 (laundries), both
2026-03-31; the monthly 新規施設 files 99-103 (beauty) and 111-115 (laundry),
2026-04 to 2026-08; one sheet per health centre; only applicants who agreed to
open publication are listed; Chiba, Funabashi and Kashiwa are not included.
What differs for Yachiyo:

- **Yachiyo's rows sit in the 習志野 sheet**, the 習志野健康福祉センター's area:
  **習志野市, 八千代市 and 鎌ケ谷市**. Rows name their municipality first, with
  no prefecture (`八千代市…`): barbers 130 of 285, beauty 344 of 722, laundries
  77 of 151. **No row naming 八千代市 sits in any other sheet** of any file (all
  13 read), so the filter is exact: sheet 習志野 and 施設所在地１ starting
  `八千代市`. Nothing straddles the city line; no ward exists.
- **One laundry row of the sheet names no municipality** (a 洗い場). Its town
  matches none of the towns parsed from Yachiyo's, Narashino's or Kamagaya's
  rows, so it stays out; re-check it against MLIT's 12221 towns once the files
  are on disk (Ichikawa's five such rows, the precedent).
- **The beauty workbook's 海匝 sheet is an exact copy of 印旛** (staging,
  2026-10-06): it does not touch the 習志野 sheet, but it is the reason the
  build filters on the city's sheet and its address, never a sum of sheets.
- ⚠️ **The 習志野 sheets of the beauty and laundry lists end in a column with an
  empty header** (`''`): harmless to `xlsx_rows`, but `REQUIRED_COLUMNS` must
  name columns, never count them.
- ⚠️ **The May, June and July beauty months name the trade name 施設名称** (no
  １) and carry no 施設名称２ on the 習志野 sheet; `NAME_COLS` reads 施設名称
  first, so the name is found, but `REQUIRED_COLUMNS` must accept either.
- The address is 施設所在地１ (`ADDR_COLS`). 施設所在地２ is filled on 19 / 137
  / 5 Yachiyo rows; every 所在地１ carries a digit, and three beauty rows'
  所在地２ begin with a digit (read them at build: a floor or a second
  number).

### Counts that matter (Yachiyo's rows)

| Kind | Rows | Not a premises | Storefronts | Newest 検査確認日 | 検査確認番号 repeated | Shōwa (S) dates `wareki_date` cannot read |
|---|---|---|---|---|---|---|
| 理容所 (barbers) | **130** | 0 | 130 | 2025-03-04 | 0 | 34 |
| 美容所 (beauty) | **344** | 0 | 344 | 2026-03-27 | 0 | 36 |
| クリーニング所 (laundries) | **77** | **7 無店舗取次店** | **70** (取次所 43, 洗い+仕上場 25, 仕上場 2) | 2024-09-27 | 0 | 6 |
| **Personal services (2026-03-31 lists)** | **551** | 7 | **544** | | | |

- **One pin per premises**: among the storefronts 2 (address, trade name)
  pairs repeat, **1 a barber and a beauty salon at one premises** and 1 inside
  the beauty list, so the base lists draw **542 pins**. (The laundry list's 3
  repeated pairs are all among the 7 無店舗 rows, which never reach the map.)
- **No closed rows** (no closure column) and **no mobile salons** (no 移動,
  一円, 訪問 or 出張 in any Yachiyo address or name).
- ⚠️ **The laundry kind is in クリーニング種別１**, which `TYPE_COLS` does not
  read: map it into the type in `source_rows` (Matsudo's build item), or the
  **7 無店舗取次店** (9% of Yachiyo's laundry rows; Matsudo's had 2 of 186)
  reach the map as premises. クリーニング種別２: 無し 61, 特定洗濯物 9,
  リネン+特定 7.
- `japan_eigyo` buckets every remaining type as Personal services; nothing
  falls out by rule.

### The rebuild to 2026-08-31 (Matsudo's shape: the beauty and laundry months)

| Month | Beauty: 習志野 sheet rows | Yachiyo's | 検査確認日 range | Repeats a base row | Laundry: Yachiyo's |
|---|---|---|---|---|---|
| 2026-04 | 6 | 2 | 04-17 .. 04-21 | 0 | 0 (no 習志野 header: 「…新規なし」) |
| 2026-05 | 4 | 3 | 05-12 .. 05-29 | 0 | 0 (1 row, 習志野市) |
| 2026-06 | 3 | 2 | 06-23 | 0 | 0 |
| 2026-07 | 4 | 2 | 07-22 .. 07-31 | 0 | 0 |
| 2026-08 | 1 | 0 | | | 0 |
| **Total** | 18 | **9** | | **0** | **0** |

- **Beauty: 344 + 9 = 353 rows, 352 premises** (the base list's one repeat).
  No addition repeats a base 検査確認番号 or (address, trade name), nor another
  addition. 開設者名 filled on all 9, 3 with a company marker; the name rule
  flags 0; none a vehicle or 無店舗; all 9 parse to a block number.
- **No new laundry in Yachiyo** in any month: laundries stay 77 rows, 70
  premises.
- **Rebuilt totals at 2026-08-31**: barbers 130 (their own 2025-03-31),
  beauty 353, laundries 77 rows; **553 storefronts** (7 laundries not
  premises), **551 pins**. De-duplicate by 検査確認番号 first (Sakura's April
  repeat shows a month can repeat its base), then one pin per premises. Pin
  `as_of` per kind (`SOURCE_AS_OF`): barbers 2025-03-31, beauty and laundry
  2026-08-31, an upper bound.

### Coverage — against e-Stat and the Economic Census

**e-Stat has no Yachiyo row** (衛生行政報告例 lists prefectures, 指定都市 and
中核市 only); the prefecture-level control is `matsudo.md`'s (barbers 99.6% on
the same date; beauty 92.3% with the 海匝 copy taken out; laundries 95.0%).
**Per city, an estimate only** (never for the page unless the owner asks, as
Ichikawa's call 32): the 2021 Economic Census
(`data/japan/raw/estat_census_r3_b1_009_1a.xlsx`, 第9-1A表; 12221: 理容業 108,
美容業 193, 洗濯業 56) scaled by `matsudo.md`'s licensed-to-census ratios
(barbers 1.118, beauty 1.595, laundries 1.294; the script reproduces Matsudo's
306 / 735 / 190):

| Kind | Estimate | The lists | Share |
|---|---|---|---|
| Barbers | about 121 | 130 | **108%** |
| Beauty | about 308 | 344 (353 rebuilt) | **112%** (**115%** rebuilt) |
| Laundries | about 72 | 70 premises | **97%** |

Yachiyo is not thinner than the prefecture's average in any kind. A modelled
figure, recorded as a measurement.

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 12221): ⚠️ NOT MEASURED

The join target is `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12221-24.0a.zip`
and `…/19.0b/12221-19.0b.zip` (both HTTP 200 by HEAD, above). One municipality,
no wards (`"wardless": True`). **Unmeasured until the two files are approved
and fetched** (open call 1). What can be said from the lists alone:

- **Every one of the 553 storefronts (544 + 9 additions) parses to a block
  number** with `permits_from_rows` (`WAVE2_RULES`), across 35 / 43 / 25
  distinct towns.
- **Address shapes** (base rows): `町名1-2-3` 327, `町名1-2` 150, written 丁目
  36, a bare number 29, 番地 9. The dashed three-part form (59%) takes
  `join_city`'s shifted-chōme rule, as in Matsudo and Ichikawa (99.5% at the
  block there). The two-part and bare-number forms (179 rows) are the likely
  大字 + 地番 rows; read the chōme tier by town.
- **At build**: the join with `japan_register` and `WAVE2_RULES` unchanged,
  tiers per kind, the misses read by town; GSI's address search on a sample
  (`screen_japan_join.py`'s `gsi_check`, 150 rows, one request per second).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (12221)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_12_GML.zip`, N03 code 12221
(51.4 km²; extent W 140.0629, S 35.6924, E 140.1519, N 35.7840; centroid
140.105, 35.739). **7 station records inside, 7 `N02_005g` groups**; no name in
two groups. N02-24 and N02-25 agree on every station here; use N02-25.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | First beyond the line |
|---|---|---|---|---|
| 東葉高速線 (東葉高速鉄道, 12) | Tōyō Rapid Line | **4 / 9** | 八千代緑が丘, 八千代中央, 村上, 東葉勝田台 (its eastern terminus) | 船橋日大前 (船橋市, 0.4 km) |
| 本線 (京成電鉄, 12) | Keisei Main Line | 3 / 42 | 八千代台, 京成大和田, 勝田台 | 志津 (佐倉市, 0.7 km), 実籾 (習志野市, 1.3 km) |

- **7 groups by operator**: Tōyō Rapid 4, Keisei 3. **Kept apart, as N02
  keeps them** (trap 1): Keisei's 勝田台 and Tōyō's 東葉勝田台, **149 m apart**,
  a walking interchange under two names, so their rings overlap almost
  wholly. Median gap to the nearest group **1,459 m** (closest 149 m, widest
  2,725 m): standard rings, by the spacing rule at build.
- **Stub test**: no urban line; Tōyō keeps 4 of 9 (44%), Keisei 3 of 42 (7%),
  both railways cut at the line by the standing call. Nothing goes back to the
  owner.
- **The Tōyō Rapid Line's trains run through onto Tokyo Metro's Tōzai Line
  beyond 西船橋** (ASSERTED; outside the city). Ichikawa's map draws the
  Tōzai (`ichikawa.md`); name the Tōyō line by its own public name here, and
  read N02's sections to its terminus at 東葉勝田台.
- **The Shinkansen and JR**: no station inside.
- **The light-rail / rail test**: both lines are railways (class 12); no
  subway, AGT, monorail or tram is drawn, and JR is absent: `metro` by the
  backbone (above).
- **Frequency** (no floor applies, call 46): **Keisei READ by the wave-5 probe
  (2026-10-06)** from `keisei.ekitan.com`, Keisei's own timetable service:
  **6 to 10 an hour** at Yachiyo's three stations. **Tōyō Rapid: ASSERTED**,
  about every 10 to 12 minutes off-peak: its station timetables are
  image-only PDFs (村上's page links `TR08_murakami20260314.pdf`, the
  2026-03-14 timetable; the probe's text extraction returned nothing). **No
  stretch runs about 11 trains a day or fewer** (call 86).
- **Gate 3** at build: Tōyō's 9 stations (西船橋 to 東葉勝田台; N02 has 9) and
  Keisei's list.
- ⚠️ **OSM `name:en`** for the 7 groups at build (no Overpass at Step 0; one
  station query in the N03 box): 八千代緑が丘 (Yachiyo-Midorigaoka), 東葉勝田台
  (Tōyō-Katsutadai) beside 勝田台 (Katsutadai), 京成大和田, 村上.

## Scope

**Yachiyo City (12221), one municipality, no wards.** The lines run on into
Funabashi, Narashino and Sakura; cut at the line, the stations beyond named by
N03 municipality at build (`excluded_stations.csv`). **Sakura is its own page**
(`docs/build_briefs/sakura.md`): Keisei's 志津 and ユーカリが丘 belong there;
Funabashi's brief (`funabashi.md`) covers 船橋日大前 and the Tōyō stations
west of the line. The 習志野 sheet's other two municipalities are not this
page.

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
  both in `japan_register.OPERATOR_COLS`, filled on every Yachiyo row. A
  company or cooperative marker on 15 of 130 barber operators, 114 of 344
  beauty and 55 of 77 laundry: the rest are mostly people's own names.
- **The name rule, version 2, flags 1 of Yachiyo's 560 rows** (551 base, 9
  additions): **one barber whose trade name is a bare personal name**
  (`bare_personal_name`; its pin shows its category). `same_person` flags 0,
  whether it compares 施設名称１ alone or 名称１ + 名称２ (filled on 0 / 1 / 6
  rows); the 9 additions flag 0. `check_personal_exposure.py` must see the 1
  withheld.
- **Never selected**: 施設電話番号; 開設者名 / 営業者名 beyond the rule's
  in-memory comparison. The lists carry no operator address.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map:
  it must print 0.

## Region

`"region": "Japan East"` (Kanto after wave 4's retag), `"country": "Japan"`,
`label_tier: "minor"`. Project to **UTM 54N (EPSG:32654)**: the city's
centroid lies at longitude 140.105, its extent 140.0629 to 140.1519, inside the
138-144 band (computed here, never copied).

**Scaffold**: `scaffold_city.py --slug yachiyo --name Yachiyo --system-name
"Tōyō Rapid and Keisei" --taxonomy japan_eigyo --lat 35.739 --lon 140.105
--region "Japan East" --country Japan --mode metro --page-number <N>`
(`--dry-run` first), with the page number claimed in `docs/session_roles.md`
at build, not here. A `japan.CITIES` entry: `"yachiyo": {"name": "八千代市",
"pref": "12", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["12221"]}`.

## Owner calls

**Made:** Band B, personal services only (owner, 2026-10-06, "Matsudo's
shape"); the prefecture's licence read (2026-10-05); the standing Japanese
calls above; the minor label tier and the Japan sub-region (2026-10-02); by
Matsudo's shape, which the band names: the barber list built as published with
its own date (Matsudo's call 33), the beauty and laundry months to 2026-08
(call 34's resources 99-103 and 111-115, already on disk), the two-date
source sentence as a review-time proposal (call 35); `metro` by the owner's
mode rule of 2026-10-02 (staging's reading, as Matsudo's); Tōyō's frequency
ASSERTED, which decides nothing under call 46.

**Open:**

1. **MLIT's address blocks for 12221 are not on disk** (the task expected
   them in `data/matsudo/raw/isj/`, which holds 12207 only). **Recommendation:
   approve the two files** (`12221-24.0a.zip`, 163,101 B, and
   `12221-19.0b.zip`, 6,358 B, from `nlftp.mlit.go.jp`, the download every
   Japanese brief has made), then measure the join with this brief's scratch
   script (`…/scratchpad/wave5/brief_sakura_yachiyo/`, Matsudo's `m4_join.py`
   shape). Tradeoff: without it the brief carries no block share; Yachiyo's
   addresses are mostly the dashed form that joined at 98-99.5% in Matsudo and
   Ichikawa, so the risk is small, but the number is not measured.

## What the build must still measure

- **The block join** (call 1): tiers per kind, the chōme-tier towns, misses
  read, the no-municipality laundry row against 12221's towns; GSI on a
  sample.
- Matsudo's config shape: `SOURCE_FILES` for the three lists and the ten
  months (the city's own `fetch_sources.py`, the publisher's file names),
  `SOURCE_AS_OF` per kind (barbers 2025-03-31; beauty and laundry
  2026-08-31), `MONTHLY`, `REQUIRED_COLUMNS` (施設名称１ or 施設名称,
  施設所在地１, 業務種別, 開設者名 / 営業者名, クリーニング種別１; a month's sheet
  holding only 「…新規なし」 has no header and must not stop the check; the
  trailing empty header is not a column to require), and a **`source_rows`**
  that reads sheet **習志野** of each file, keeps rows whose 施設所在地１ starts
  `八千代市` (130 / 353 / 77), de-duplicates by 検査確認番号, and carries
  クリーニング種別１ as the laundry type so the 7 無店舗取次店 drop out.
- Resource 79's served name and bytes (the barber file may be replaced); the
  newest edition of each file.
- Gate 3 against Tōyō Rapid's and Keisei's lists; Tōyō's frequency if a
  text timetable turns up; OSM `name:en` for 7 groups; line colours on both
  basemaps (2 lines).
- ⚠️ **The Economic Census control** (`scripts/japan_census_control.py`)
  measures 飲食店, which this page does not carry: the personal-services
  estimate above is the control; record it at build.

```brief-checks
[
  {
    "id": "yachiyo-dataset6-package",
    "claim": "Chiba Prefecture's dataset 6 still declares PDL on its resources, still excludes Chiba, Funabashi and Kashiwa, still lists only consenting applicants, and still points at resources 79-81 under their 2026-03-31 titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["\"resource_license_id\":\"pdl\"", "千葉市、船橋市及び柏市の施設情報は含まれていません", "オープンデータ掲載に賛同", "【千葉県】理容所施設一覧（令和8年3月末時点）", "【千葉県】美容所施設一覧（令和8年3月末時点）", "【千葉県】クリーニング所施設一覧（令和8年3月末時点）", "resource_download/79", "resource_download/80", "resource_download/81"]
  },
  {
    "id": "yachiyo-barber-size-mismatch",
    "claim": "The catalogue still declares 378,797 B for resource 79 while serving the 328,249 B 2025-03-31 file; if this size changes, the prefecture has touched the barber file: re-read it and re-measure Yachiyo's 130",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=79",
    "present": ["\"size\":\"378797\"", "令和8年3月末時点"]
  },
  {
    "id": "yachiyo-laundry-size",
    "claim": "Resource 81 (laundries, 2026-03-31, Yachiyo's 77 rows with 7 無店舗取次店) still declares 254,290 B; a new size means a new file: re-measure",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=81",
    "present": ["\"size\":\"254290\"", "クリーニング所施設一覧（令和8年3月末時点）"]
  },
  {
    "id": "yachiyo-barber-live",
    "claim": "Resource 79 (barbers) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/79",
    "min_bytes": 300000
  },
  {
    "id": "yachiyo-beauty-live",
    "claim": "Resource 80 (beauty salons, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/80",
    "min_bytes": 700000
  },
  {
    "id": "yachiyo-laundry-live",
    "claim": "Resource 81 (laundries, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/81",
    "min_bytes": 200000
  },
  {
    "id": "yachiyo-monthly-package",
    "claim": "Dataset 6 still lists the ten monthly files of Matsudo's shape (beauty 99-103, laundry 111-115: 新規施設 令和8年4月 to 8月) under those titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["【千葉県】美容所新規施設（令和8年4月）", "【千葉県】美容所新規施設（令和8年5月）", "【千葉県】美容所新規施設（令和8年6月）", "【千葉県】美容所新規施設（令和8年7月）", "【千葉県】美容所新規施設（令和8年8月）", "【千葉県】クリーニング所新規施設（令和8年4月）", "【千葉県】クリーニング所新規施設（令和8年8月）", "resource_download/99", "resource_download/103", "resource_download/111", "resource_download/115"]
  },
  {
    "id": "yachiyo-beauty-aug-size",
    "claim": "The August beauty file (resource 99, a second upload) still declares 70,264 B; a new size means a third upload: re-fetch and re-measure the month",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=99",
    "present": ["\"size\":\"70264\"", "美容所新規施設（令和8年8月）"]
  },
  {
    "id": "yachiyo-terms-pdl",
    "claim": "The catalogue's terms page still applies PDL 1.0 and prescribes the 加工 credit form",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/pages/terms",
    "present": ["PDL1.0", "千葉県オープンデータサイト", "を加工して作成"]
  },
  {
    "id": "yachiyo-toyo-timetable",
    "claim": "Tōyō Rapid's 村上 station page still links the 2026-03-14 timetable PDF (image-only, why the line's frequency is ASSERTED); a new file means a new timetable: try to read it",
    "kind": "http_contains",
    "url": "https://www.toyokosoku.co.jp/station/murakami",
    "present": ["TR08_murakami20260314.pdf"]
  },
  {
    "id": "yachiyo-projected-crs",
    "claim": "Yachiyo projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 140.105,
    "expect": "EPSG:32654"
  }
]
```
