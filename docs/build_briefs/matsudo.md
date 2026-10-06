# Matsudo — build brief

**Band B, personal services only, owner-approved 2026-10-04** (Japan's third
wave; the Step 0 downloads approved 2026-10-05, staging's call 10,
`docs/decisions_drafts/staging.md`, "Band B's licence terms accepted, the
briefs' calls made, the Japanese Band B briefs and a Hamburg re-check
approved"). **Step 0 measured 2026-10-05** (staging). Downloaded, each from
its publisher's own host, into `data/matsudo/raw/` (gitignored), named as the
publisher serves them:

- From `opendata.pref.chiba.lg.jp` (the catalogue's own API is
  `/ckan_api/package_show?id=6`, not `/api/3/` and not
  `/ckan_api/action/package_show`, which answered 404; then each file once,
  5 s apart, each HTTP 200): resource 79 → `ichiran-riyou202503.xlsx`
  (328,249 B), resource 80 → `ichiran-biyou202603.xlsx` (765,694 B), resource
  81 → `ichiran-clean202603.xlsx` (254,290 B). The same three files serve
  Ichikawa (copied to `data/ichikawa/raw/`; `docs/build_briefs/ichikawa.md`).
- From `nlftp.mlit.go.jp`: `isj/12207-24.0a.zip` (269,856 B) and
  `isj/12207-19.0b.zip` (8,546 B).
- Not fetched: MHLW's prefecture file (12000), since food is off and no
  control needed it; the dataset's monthly new-premises files (resources
  83-130), which were not on the approved list (open call 2).

**Run `python scripts/brief_check.py matsudo` before writing any code.** Then
the `japan-city` skill, **Kōchi's shape** (personal services only, a full
list per kind; `docs/build_briefs/kochi.md`, `pipeline/kochi/config.py`),
with one difference that is new: **the publisher is the prefecture, not the
city**, so every row is assigned to Matsudo by its address (below).
Coordinates: the `address-join` skill, measured with the shared
`pipeline/countries/japan_register.py` functions from scratch scripts
(`scripts/screen_japan_join.py` has no Matsudo entry; add one at build). Rail:
MLIT N02-25 cut at the N03 city line, measured through
`pipeline/countries/japan.py` with a scratch `CITIES` entry (none was added to
the shared module).

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27), and an URBAN line cut to a stub goes back to
the owner; (4) **菓子製造業 and そうざい製造業 count, in Retail** (2026-09-24;
moot on a personal-services page); (5) **the name rule**: where the trade name
IS the operator's own name, the pin shows its permit type, the operator column
read in memory only (2026-09-27); MHLW's 法人名 joins it for every MHLW city
(2026-10-05; moot here, no MHLW source); (6) **no page says "currently
operating"**. Also: fault-based cost clauses accepted for all of Japan
(2026-09-24); English station names from OSM `name:en`, numerals as figures
before 丁目; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Matsudo
carries `label_tier: "minor"` and goes in the **Japan East** view, as
Utsunomiya, Maebashi and the other Kantō cities do (`app/cities.py`; wave 4's
first city retags Japan into the eight regions, Matsudo into Kanto). Its label
offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200),
never by eye. Matsudo and Ichikawa sit about 9 km apart: measure both labels
together if they land in one batch.

**`mode`: `metro`** (the owner's rule of 2026-10-02, applied as for Kurume and
Maebashi): no subway or tram is drawn, and JR is not the largest network
inside the city (7 station groups against Keisei's 9), so the mode follows the
backbone, the Keisei Matsudo Line, a railway (N02 class 12).

---

## The one-line summary

**Personal services only, from Chiba Prefecture's open-data lists of barbers,
beauty salons and laundries (dataset 6, PDL 1.0), cut to Matsudo by address:
304 barbers (⚠️ the list is as of 2025-03-31, not 2026-03-31 as the catalogue
title says), 759 beauty salons and 186 laundries (184 premises) as of
2026-03-31; 1,247 storefronts, 1,241 pins, placed at the block 98.4%.** No
per-city official count exists (e-Stat counts the prefecture's jurisdiction as
one); prefecture-wide, the barber list is 99.6% of the official count on the
same date. Food stays off (the master list: the prefecture's food set is
old-law only; MHLW's prefecture file is 62.7% addressed, 1,193 addressed rows
here). Rail: 20 N02 station groups (Keisei 9, JR 7, Hokusō 4, Ryūtetsu 3,
Tōbu 1).

---

## Business leg — Chiba Prefecture's 環境衛生関係施設一覧 (dataset 6)

| | |
|---|---|
| **Dataset** | `https://opendata.pref.chiba.lg.jp/datasets/6`, 「【千葉県】環境衛生関係施設一覧」, organisation 衛生指導課 (contact 健康福祉部衛生指導課：生活衛生推進班), 「毎月」; `package_show` metadata modified 2026-09-29; 52 resources, every one `resource_license_id: pdl` |
| **Its notes** | 「施設一覧は令和7年3月末時点の情報について掲載されています。」 (the lists are as of 2025-03-31: stale for two of the three files, right for the barber file, below); new premises added monthly around the 20th-25th; **only applicants who agreed to open publication are listed** (「申請者にオープンデータ掲載に賛同いただいているものに限定して掲載」); **Chiba, Funabashi and Kashiwa are not included** (their own health centres) |
| **Files used** | resource 79 「【千葉県】理容所施設一覧（令和8年3月末時点）」, 80 美容所, 81 クリーニング所 (`https://opendata.pref.chiba.lg.jp/resource_download/<id>`); 82 (旅館・ホテル) is out of scope |
| **Monthly files (not fetched)** | 新規施設 for each kind, 令和7年9月 to 令和8年8月: barbers 83-94, beauty 95-106, laundries 107-118 (open call 2). No closure files |
| **Layout** | One workbook per kind, **one sheet per health centre** (習志野, 市川, 松戸, 野田, 印旛, 香取, 海匝, 山武, 長生, 夷隅, 安房, 君津, 市原); the header is row 1, no title rows |
| **Columns** | barber, beauty: **開設者名** (the operator), **施設名称１**, 施設名称２, **施設所在地１**, 施設所在地２, 施設電話番号, **業務種別**, 検査確認番号, 検査確認日. Laundry: **営業者名** in place of 開設者名, plus **クリーニング種別１** (取次所, 洗い+仕上場, 仕上場, 洗い場, 無店舗取次店) and クリーニング種別２ (特定洗濯物, リネンサプライ, 無し). The 印旛 barber sheet and the 海匝 laundry sheet order or name theirs differently; neither is read for Matsudo |
| **Dates** | 検査確認日 in the era-letter dot form (`H01.03.03`, `R07.01.30`, `S64.01.07`); `japan_register.wareki_date` reads H and R but returns None for every S (Shōwa) date. Nothing in the build reads it (no expiry on a 生活衛生 confirmation); say so if a step ever does |

### ⚠️ The barber file is the 2025-03-31 list (the check the master list asked for)

Settled from inside the file, as the master list asked:

| | Barbers (79) | Beauty (80) | Laundries (81) |
|---|---|---|---|
| Catalogue title | 令和8年3月末時点 | 令和8年3月末時点 | 令和8年3月末時点 |
| Served file name | `ichiran-riyou`**`202503`**`.xlsx` | `ichiran-biyou202603.xlsx` | `ichiran-clean202603.xlsx` |
| Catalogue `size` / served bytes | **378,797 / 328,249** | 765,694 / 765,694 | 254,290 / 254,290 |
| HTTP Last-Modified | 2026-03-04 | 2026-04-30 | 2026-04-30 |
| Workbook created / modified (`docProps/core.xml`) | **2025-04-23 / 2025-04-23** | 2025-04-23 / 2026-04-27 | 2025-04-23 / 2026-04-30 |
| Newest 検査確認日, every sheet | **2025-03-07** | 2026-04-06 | 2026-03-30 |
| Rows confirmed after 2025-03-31, every sheet | **0** | 221 | 14 |

**The barber file is the list as of 2025-03-31** (令和7年3月末, as the
dataset's own note says), saved 2025-04-23 and uploaded on 2026-03-04, before
the date its title claims. The other two are the 2026-03-31 lists. The
catalogue's size for 79 (378,797) does not match the file it serves, so a
2026-03-31 barber file probably exists and was not uploaded. **At build:
re-read resource 79's served name and bytes** (the brief check pins the
catalogue's 378,797 and the served file's minimum); if a `…202603.xlsx` is
served by then, use it and re-measure. Until then the barber layer carries its
own as-of (`SOURCE_AS_OF`), 2025-03-31.

### Assigning rows to Matsudo (the address filter)

- **Matsudo's rows sit in the 松戸 sheet**, which is the 松戸健康福祉センター's
  area: **松戸市, 流山市 and 我孫子市**. Every row of that sheet in all three
  files starts its 施設所在地１ with its municipality, with no prefecture
  (`松戸市…`): barbers 304 Matsudo / 82 Nagareyama / 71 Abiko (457), beauty
  759 / 319 / 166 (1,244), laundries 186 / 63 / 39 (288). **No row lacks a
  municipality, and no row naming 松戸市 sits in any other sheet** (all 13
  sheets read). So the filter is exact: sheet 松戸 and 施設所在地１ starting
  `松戸市`. Nothing straddles the city line; no ward exists.
- `japan_register` today reads every sheet with an address column and keeps
  every row: **step 2 needs a `source_rows`** (Kōchi's hook) that reads
  `city_rows(path, sheet="松戸")` and keeps the rows starting `松戸市`, failing
  if that count drifts from the brief's without a new file. Without it, the
  other municipalities' rows reach the join, parse 流山市 as a town, and fall
  unplaced (or worse, a shared town name places them in Matsudo).
- The address is 施設所在地１ (`ADDR_COLS` has it, from Matsuyama); 施設所在地２
  is the building, filled on 68 / 571 / 48 rows of the sheet. **No Matsudo
  row keeps its number in 所在地２** (every 所在地１ has a digit), so reading
  所在地１ alone loses no placement.

### Counts that matter (Matsudo's rows)

| Kind | Rows | Not a premises | Storefronts | Newest 検査確認日 (松戸 sheet) | 検査確認番号 repeated in Matsudo's rows |
|---|---|---|---|---|---|
| 理容所 (barbers) | **304** | 0 | 304 | 2025-01-30 | 0 |
| 美容所 (beauty) | **759** | 0 | 759 | 2026-03-16 | 0 |
| クリーニング所 (laundries) | **186** | **2 無店舗取次店** | **184** (取次所 114, 洗い+仕上場 65, 仕上場 4, 洗い場 1) | 2026-01-22 | 0 |
| **Personal services** | **1,249** | 2 | **1,247** | | |

- **One pin per premises**: 6 (address, trade name) pairs repeat, 4 a barber
  and a beauty salon at one premises under one name (e-Stat's 重複開設) and 2
  inside the beauty list, so **step 2 draws 1,241 pins** (one per premises and
  bucket).
- **No closed rows**: the lists carry no closure column; each is a snapshot of
  premises on file at its date. After it, closures are invisible.
- **No mobile salons**: no 移動, 一円 or 訪問 in any Matsudo address or name.
- ⚠️ **The laundry kind is in クリーニング種別１**, which `TYPE_COLS` does not
  read: the type reads `クリーニング所` from 業務種別 for every row, so the two
  無店舗取次店 (no shop: not premises, `japan_eigyo`'s assert) would reach the
  map. The scratch measure passed クリーニング種別１ as the type. At build: the
  `source_rows` maps it into the type, or add `クリーニング種別１` to
  `TYPE_COLS` ahead of 業務種別 (no built city carries that column; then the
  Minato control).
- `japan_eigyo` buckets every remaining type (理容所, 美容所, 取次所, 洗い+仕上場,
  仕上場, 洗い場) as Personal services; nothing falls out by rule.

### Coverage — against e-Stat and the Economic Census

**e-Stat has no Matsudo row.** 衛生行政報告例 FY2024 第10表 (理容・美容) and
第11表 (クリーニング) (`data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv`
and `…_cleaning_by_city.csv`, on disk, read here) list prefectures, 指定都市 and
中核市 only. Matsudo falls in the prefecture's own jurisdiction, which is
千葉県 less 千葉市, 船橋市 and 柏市, exactly the lists' coverage:

| Kind | Official FY2024 (2025-03-31), prefecture's jurisdiction | The prefecture's list, every sheet | Share | Same date? |
|---|---|---|---|---|
| 理容所 | 4,350 − 600 − 331 − 238 = **3,181** | **3,168** (2025-03-31) | **99.6%** | yes |
| 美容所 | 10,486 − 1,701 − 960 − 758 = **7,067** | **7,607** (2026-03-31) | 107.6% | a year later |
| クリーニング所 (施設) | 2,366 − 428 − 220 − 129 = **1,589** (取次所 986) | **1,509** premises (取次所 928) + 22 無店舗 | 95.0% | a year later |

- **The consent filter is thin**: barbers at 99.6% of the official count on the
  same date, although the dataset lists only applicants who agreed. Disclose it
  as the coverage reason (the licence read's condition), with no number of
  withheld premises, since none is published.
- **Per-city, an estimate only** (never for the page): the 2021 Economic Census
  (`data/japan/raw/estat_census_r3_b1_009_1a.xlsx`, 第9-1A表) counts
  establishments, not premises on file. Scaled by the jurisdiction's licensed
  to census ratio (barbers 3,181 / 2,846 = 1.118; beauty 7,067 / 4,430 = 1.595;
  laundries 1,589 / 1,228 = 1.294), Matsudo's census counts (理容業 274, 美容業
  461, 洗濯業 147) give about **306 barbers, 735 salons and 190 laundries**:
  the lists hold **304 (99%), 759 (103%) and 184 (97%)**. Matsudo is not
  thinner than the prefecture's average. A modelled figure, recorded as a
  measurement and never stated on the page.

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 12207)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12207-24.0a.zip` and
`…/19.0b/12207-19.0b.zip`: **39,921 block keys, 247 town-chōme keys.** One
municipality, no wards (`"wardless": True`). Measured with `japan_register`
and `WAVE2_RULES` unchanged (no Minato re-run needed), on the 1,247
storefronts:

| Tier | Barbers (304) | Beauty (759) | Laundries (184) | All (1,247) |
|---|---|---|---|---|
| Block | **97.7%** | **98.8%** | **97.8%** | **98.4%** |
| Town-chōme / 大字 centroid | 2.3% (7) | 1.1% (8) | 1.6% (3) | 1.4% (18) |
| Unplaced | 0 | 0.1% (1) | 0.5% (1) | 0.2% (2) |

- **The shifted-chōme rule carries most of it**: the lists write `町名4-5-6`
  without 丁目 (571 of 1,247 rows take `join_city`'s chōme shift). 5 rows use
  rule C's affix.
- **Chōme tier**: 大字 地番 areas MLIT's block edition does not number
  (五香六実, 高塚新田, 日暮, 幸田, 牧の原, 岩瀬, 小根本, 上本郷, 殿平賀, 松戸) and three
  chōme (栄町, 六高台7丁目, 古ケ崎3丁目). **Unplaced**: one row parsed to
  `本町4丁目` and one to `松戸3丁目`; Matsudo's 本町 and 松戸 carry no such chōme
  in MLIT's files. Read both at build.
- **Independent check**: the lists carry no coordinates and MHLW has no
  salons. Run GSI's address search on a sample at build
  (`screen_japan_join.py`'s `gsi_check`, as Sendai: 150 rows, one request per
  second).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (12207)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_12_GML.zip`, N03 code 12207
(61.3 km²; extent W 139.8794, S 35.7467, E 140.0014, N 35.8498). **25 station
records inside, 20 `N02_005g` groups**; no name in two groups. N02-24 and
N02-25 agree on every station here; use N02-25.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside | First beyond the line |
|---|---|---|---|---|
| 松戸線 (京成電鉄, 12) | Keisei Matsudo Line | **8 / 24** | 松戸, 上本郷, 松戸新田, みのり台, 八柱, 常盤平, 五香, 元山 | くぬぎ山 (鎌ケ谷市, 0.3 km) |
| 常磐線 (東日本旅客鉄道, 11) | JR Jōban Line | 5 / 81 | 松戸, 北松戸, 馬橋, 新松戸, 北小金 | 金町 (Tokyo, 0.8 km), 南柏 (柏市) |
| 北総線 (北総鉄道, 12) | Hokusō Line | 4 / 15 | 矢切, 秋山, 東松戸, 松飛台 | 北国分, 大町 (市川市, 0.1 / 0.0 km), 新柴又 (Tokyo) |
| 武蔵野線 (東日本旅客鉄道, 11) | JR Musashino Line | 3 / 27 | 新松戸, 新八柱, 東松戸 | 南流山 (流山市, 0.3 km), 市川大野 (市川市) |
| 流山線 (流鉄, 12) | Ryūtetsu Nagareyama Line | 3 / 6 | 馬橋, 幸谷, 小金城趾 | 鰭ヶ崎 (流山市, 0.5 km) |
| 成田空港線 (京成電鉄, 12) | Keisei Narita Sky Access | **1 / 8** | 東松戸 | 新鎌ヶ谷 (鎌ケ谷市), 京成高砂 (Tokyo) |
| 野田線 (東武鉄道, 12) | Tōbu Urban Park Line | **1 / 35** | 六実 | 高柳 (柏市, 0.4 km) |

- **20 groups by operator**: Keisei 9 (the Matsudo Line's 8 and 東松戸 on the
  Sky Access), JR 7 (新松戸 on both JR lines), Hokusō 4, Ryūtetsu 3, Tōbu 1. The
  master list's "Keisei Matsudo 8, JR 8" counts the Matsudo Line alone and JR
  per line; the total, 20, is the same.
- **Interchanges N02 groups**: 松戸 (JR, Keisei; 29 m), 馬橋 (JR, Ryūtetsu;
  52 m), 新松戸 (JR's two lines; 23 m), 東松戸 (JR, Hokusō, Keisei; 97 m).
  **Kept apart, as N02 keeps them** (trap 1): 新松戸 and Ryūtetsu's 幸谷, and
  Keisei's 八柱 and JR's 新八柱, each a walking interchange under two names.
  Median gap to the nearest group **1,182 m** (closest pair 93 m): standard
  rings, by the spacing rule at build.
- **One-station stubs, kept as cut (standing call)**: the Tōbu Urban Park Line
  (六実, 1 of 35) and **the Keisei Narita Sky Access (東松戸, 1 of 8), which the
  master list did not name**. Both are commuter railways (class 12), not urban
  lines, so neither goes back to the owner. ⚠️ The Sky Access runs on the
  Hokusō Line's track through Matsudo (矢切, 秋山 and 松飛台 passed without a
  stop): read how N02 files 成田空港線's sections at build. If they overlay the
  Hokusō track, draw it as its own line over that track (Tokyo's overlapping
  services) or name it in the Hokusō Line's legend entry (trap 4); either way
  東松戸 is already a ring through JR and Hokusō.
- **Stub test**: no urban line here; the Keisei Matsudo Line keeps 8 of 24
  (33%), the rest running on through Kamagaya to 京成津田沼. Nothing goes back
  to the owner.
- ⚠️ **Services over N02's legal lines (trap 2)**: N02's 常磐線 carries both
  the Jōban Line Rapid (stops at 松戸 only here) and the local (all five, the
  Chiyoda Line's through trains). **Tokyo built JR East's Jōban services as
  routes; reuse them.**
- **The Shinkansen**: no station inside.
- **The light-rail / rail test**: no subway, tram or light rail; every line is
  a railway (classes 11 and 12). JR is not the largest network by in-city
  groups (7 against Keisei's 9), so `metro` on Kurume's precedent.
- **Frequency** (no floor applies to JR or private lines in Japan): read for
  the line most likely to raise the question, the **Ryūtetsu**, from its own
  timetable page by curl (`http://ryutetsu.jp/timetable.html`, 流山 → 馬橋,
  「2024年3月16日改正」): **64 departures on weekdays** (4:53 to 23:50), 59 at
  weekends; **every 20 minutes from 10:00 to 16:58** both days (:18, :38,
  :58), every 15 minutes from 7:00 to 9:00 and 17:00 to 21:45 on weekdays. `https://ryutetsu.jp/`
  failed TLS (SEC_E_WRONG_PRINCIPAL, the certificate names another host); the
  plain-HTTP page is the operator's own. **ASSERTED, not read**: JR, Keisei,
  Hokusō and Tōbu run several trains an hour through Matsudo.
- **Gate 3**: the Ryūtetsu's page lists its **6 stations** (流山 to 馬橋), as
  N02 has 6. JR East, Keisei, Hokusō and Tōbu at build.
- ⚠️ **OSM `name:en`** for the 20 groups at build (no Overpass at Step 0): one
  station query in the N03 box. Read every name: 小金城趾 (趾), みのり台, 常盤平,
  and the Keisei Matsudo Line's stations, renamed from Shin-Keisei in 2025 (OSM
  may still carry the old operator or line name).

## Scope

**Matsudo City (12207), one municipality, no wards.** The lines run on into
Kamagaya, Kashiwa, Nagareyama, Ichikawa and Tokyo's Katsushika; cut at the
line, the stations beyond named by N03 municipality at build
(`excluded_stations.csv`). Ichikawa is its own page (`ichikawa.md`): the
Hokusō Line's 北国分 and 大町 and JR's 市川大野 belong there.

## Licences — as read (the full read is recorded)

- **Chiba Prefecture, dataset 6**: read 2026-10-05 (`docs/decisions_drafts/
  staging.md`, "Band B's Japanese sources read: Kanazawa, Chiba Prefecture and
  Shizuoka permitted with conditions", the Chiba Prefecture bullet; that entry
  is the verdict, this brief only cites it). As declared: every resource
  `resource_license_id: pdl`; the catalogue's terms page
  (`https://opendata.pref.chiba.lg.jp/pages/terms`) applies 公共データ利用規約
  （第1.0版） (PDL 1.0) where no other note is given. What it requires of the
  build, as recorded there:
  - **Cite and build from `opendata.pref.chiba.lg.jp` only**, never a
    `pref.chiba.lg.jp` page (the prefecture's website default covers those).
  - **MUST DISPLAY** the catalogue's 加工 form,
    `「…」（千葉県オープンデータサイト）（URL）を加工して作成`, naming this project as
    the processor, as PDL 1.0 requires. Proposed, for the notice:
    `出典：「【千葉県】環境衛生関係施設一覧」（千葉県オープンデータサイト）（https://opendata.pref.chiba.lg.jp/datasets/6）を加工して作成`
    (or the three resource titles; settle it with the notice at build).
  - **MUST NOT** present it as the prefecture's own or use its logos. No
    indemnity.
  - **The lists hold only applicants who agreed to open publication**:
    disclosed as a coverage reason.
- **Chiba City's Band R** rests on the city's own site licence, not on the
  prefecture's host, so it does not reach these lists (master list row).
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**: CC
  BY 4.0, picks stations, ⛔ never drawn.
- **MHLW open data**: not used (food is off).

## Privacy

Read only the trade name, the type, the laundry kind and the premises address.
**No row value was printed or stored for this brief**: every count comes from
in-memory comparisons.

- **Operator columns**: **開設者名** (barber, beauty) and **営業者名** (laundry),
  both already in `japan_register.OPERATOR_COLS`; filled on every row. In the
  松戸 sheet, 407 of 457 barber operators, 814 of 1,244 beauty and 107 of 288
  laundry carry no company or cooperative marker: mostly people's own names.
- **The name rule flags 0 rows** in Matsudo's 1,249, whether it compares
  施設名称１ alone (what `NAME_COLS` reads) or 施設名称１ + 施設名称２.
- **Never selected**: 施設電話番号; 開設者名 / 営業者名 beyond the rule's
  in-memory comparison. The lists carry no operator address.
- 施設名称２ (a second line of the name) is filled on 4 barber, 35 beauty and 20
  laundry rows of the sheet. Whether the pin shows 名称１ alone or both is a
  build choice; the rule must compare what is shown.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map:
  it must print 0.

## Region

`"region": "Japan East"`, `"country": "Japan"`, `label_tier: "minor"`.
Project to **UTM 54N (EPSG:32654)**: the city's centroid lies at longitude
139.929 and its western edge at 139.8794, both inside the 138-144 band
(computed here, never copied).

**Scaffold**: `scaffold_city.py --slug matsudo --name Matsudo --system-name
"Keisei, JR East, Hokusō, Ryūtetsu and Tōbu" --taxonomy japan_eigyo --lat
35.796 --lon 139.929 --region "Japan East" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), with the page number claimed in
`docs/session_roles.md` at build, not here. A `japan.CITIES` entry:
`"matsudo": {"name": "松戸市", "pref": "12", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["12207"]}`.

## Owner calls

**Made:** Band B, personal services only (owner, 2026-10-04); the Step 0
downloads (owner, 2026-10-05, call 10); the prefecture's licence read
(2026-10-05); the standing Japanese calls above; the minor label tier and the
Japan sub-region (owner, 2026-10-02); `metro` by the owner's mode rule of
2026-10-02 (staging's reading, as Kurume's and Maebashi's); the two
one-station stubs (Tōbu, Keisei Sky Access) kept as cut by the standing call.

**Open:**

1. **The barber list is a year older than the other two** (2025-03-31 against
   2026-03-31). Recommendation: build it as published with its own as-of
   (`SOURCE_AS_OF`), the page naming both dates, and re-check resource 79 at
   build in case the prefecture replaces it (the catalogue's size says a
   different file was meant). Tradeoff: a page with two dates, against leaving
   barbers off (304 pins, a quarter of the page) or waiting for the
   prefecture. Shared with Ichikawa.
2. **The monthly new-premises files** (dataset 6, resources 83-118:
   2025-09 to 2026-08 per kind), the way Kōchi carries its monthly additions.
   Not fetched (not on the approved list). Recommendation: approve beauty's and
   laundry's 2026-04 to 2026-08 files (five months each, unbroken after the
   2026-03-31 lists), pin `as_of` to 2026-08-31 and call the register an upper
   bound (closures are invisible, Kyoto's and Kōchi's disclosure); leave the
   barber months out, because the catalogue has none for 2025-04 to 2025-08 and
   adding later months would hide that gap. Tradeoff: a fresher map with an
   upper-bound caveat, against the plain 2026-03-31 snapshot (no caveat beyond
   "may include closed premises"). Same host and licence (PDL 1.0 per
   resource); shared with Ichikawa.
3. **Page wording**: the approved one-bucket line is Yokohama's ("barbers,
   beauty salons and laundries"), but the source sentence names the
   prefecture, not the city, and carries two dates: a sentence outside the
   template, a proposal for the drafts file at build. Recommendation: "From
   Chiba Prefecture's open-data registers of barbers (as of March 31, 2025),
   beauty salons and laundries (as of March 31, 2026), which list only
   premises whose operators agreed to publication." No per-city share on the
   page (no official per-city count exists).

## What the build must still measure

- The Kōchi config shape: `SOURCE_FILES` for the three resources (one download
  each, shared with Ichikawa through the same file names; each city's
  `fetch_sources.py` fetches into its own `raw/`), `SOURCE_AS_OF` per kind,
  `REQUIRED_COLUMNS` naming 施設名称１, 施設所在地１, 業務種別 and 開設者名 /
  営業者名 (and クリーニング種別１ for laundries), and a **`source_rows`** that
  reads sheet 松戸, keeps rows whose 施設所在地１ starts `松戸市` (304 / 759 /
  186 on these files), and carries クリーニング種別１ as the laundry type.
- ⚠️ **Shared code**, if the build prefers it to `source_rows`: `TYPE_COLS` +=
  クリーニング種別１ ahead of 業務種別, then the Minato control
  (`screen_japan_join.py minato`, 98.0 / 0.2 / 1.8) and every city screen.
- Resource 79's served name and bytes (above); the newest edition of each file.
- The two unplaced rows (本町4丁目, 松戸3丁目) and the 18 chōme-tier rows; GSI
  on a sample.
- Gate 3 against JR East's, Keisei's, Hokusō's and Tōbu's station lists; how
  N02 files the Sky Access; JR's Jōban services as Tokyo's routes; OSM
  `name:en` for 20 groups; line colours on both basemaps (7 lines, two pairs
  sharing track).
- ⚠️ **The Economic Census control** (`scripts/japan_census_control.py`)
  measures 飲食店, which this page does not carry. The personal-services
  comparison above (理容業 274, 美容業 461, 洗濯業 147 in 12207) is the control;
  record it at build, not a new download.
- FY2025's 衛生行政報告例 tables, when e-Stat publishes them, as the exact
  prefecture-level control for the 2026-03-31 beauty and laundry lists.

```brief-checks
[
  {
    "id": "matsudo-dataset6-package",
    "claim": "Chiba Prefecture's dataset 6 still declares PDL on its resources, still excludes Chiba, Funabashi and Kashiwa, still lists only consenting applicants, and still points at resources 79-81 under their 2026-03-31 titles",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/package_show?id=6",
    "present": ["\"resource_license_id\":\"pdl\"", "千葉市、船橋市及び柏市の施設情報は含まれていません", "オープンデータ掲載に賛同", "【千葉県】理容所施設一覧（令和8年3月末時点）", "【千葉県】美容所施設一覧（令和8年3月末時点）", "【千葉県】クリーニング所施設一覧（令和8年3月末時点）", "resource_download/79", "resource_download/80", "resource_download/81"]
  },
  {
    "id": "matsudo-barber-size-mismatch",
    "claim": "The catalogue still declares 378,797 B for resource 79 while serving the 328,249 B 2025-03-31 file (ichiran-riyou202503.xlsx); if this size changes, the prefecture has touched the barber file: re-read it and re-measure",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/ckan_api/resource_show?id=79",
    "present": ["\"size\":\"378797\"", "令和8年3月末時点"]
  },
  {
    "id": "matsudo-barber-live",
    "claim": "Resource 79 (barbers) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/79",
    "min_bytes": 300000
  },
  {
    "id": "matsudo-beauty-live",
    "claim": "Resource 80 (beauty salons, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/80",
    "min_bytes": 700000
  },
  {
    "id": "matsudo-laundry-live",
    "claim": "Resource 81 (laundries, 2026-03-31) answers a keyless GET",
    "kind": "http_ok",
    "url": "https://opendata.pref.chiba.lg.jp/resource_download/81",
    "min_bytes": 200000
  },
  {
    "id": "matsudo-terms-pdl",
    "claim": "The catalogue's terms page still applies PDL 1.0 and prescribes the 加工 credit form",
    "kind": "http_contains",
    "url": "https://opendata.pref.chiba.lg.jp/pages/terms",
    "present": ["PDL1.0", "千葉県オープンデータサイト", "を加工して作成"]
  },
  {
    "id": "matsudo-isj-live",
    "claim": "MLIT's block-level address file for Matsudo (12207) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/12207-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "matsudo-ryutetsu-timetable",
    "claim": "The Ryūtetsu's own timetable page (流山's, where the 20-minute midday frequency was read, 2026-10-05) still links the other five stations' timetables, six in all as N02 has 6 (gate 3). ASCII strings only: the page sends no charset, so the check reads it as Latin-1 and cannot match Japanese text (Maebashi's Jōmō check, the same trap)",
    "kind": "http_contains",
    "url": "http://ryutetsu.jp/timetable.html",
    "present": ["timetable/mabashi.html", "timetable/koya.html", "timetable/koganejoshi.html", "timetable/hiregasaki.html", "timetable/heiwadai.html", "class=\"holiday\""]
  },
  {
    "id": "matsudo-projected-crs",
    "claim": "Matsudo projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.929,
    "expect": "EPSG:32654"
  }
]
```
