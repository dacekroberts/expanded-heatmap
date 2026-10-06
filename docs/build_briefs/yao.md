# Yao — build brief

**Band B, food only (Kurume's shape), owner-approved 2026-10-06** (Japan wave
4, a pre-verdict converted in staging's wave 5, call 137:
`docs/decisions_drafts/staging.md`, "Wave 5, second half": "Tottori,
Yamagata, Yao, Takatsuki (food only)"). The Step 0 downloads were approved by
the owner 2026-10-06 (call 141). **Step 0 measured 2026-10-06** (staging).
Into `data/yao/raw/` (gitignored), each from its publisher's own host with
the project user-agent, each HTTP 200, under each URL's own file name as
`japan_fetch.get` saves:

- From `i2fas.mhlw.go.jp`: `27212_food_business_all.csv` (**1,611,859 B**,
  the size approved), the only business source.
- From `nlftp.mlit.go.jp`: `isj/27212-24.0a.zip` (214,122 B) and
  `isj/27212-19.0b.zip` (14,021 B).

**1,840,002 B in all.** Nothing else was downloaded. Kintetsu's, Hankyu's and
JR West's station timetable pages were read by plain GET for frequency
(pages, not data files).

**Run `python scripts/brief_check.py yao` before writing any code.** Then the
`japan-city` skill, **Kurume's shape** (`docs/build_briefs/kurume.md`: MHLW's
open data alone, food only, the fixed-premises measure) with Okayama's and
Hiroshima's food-only page. Coordinates: the `address-join` skill, measured
with `pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Yao entry; its table is shared code
and was not edited). Rail: MLIT N02-25 cut at the N03 city line, through
`pipeline/countries/japan.py` with an in-memory `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left
out, its station kept through the other lines, and **drawn cut where no other
line serves that station** (owner, 2026-10-06, calls 54 and 92: **八尾南
here**); (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**,
version 2 (2026-10-06): 法人名 is an operator column (2026-10-05) and a bare
personal name is withheld whatever it holds; (6) **no page says "currently
operating"**. Also: no frequency floor for JR or private lines in Japan
(owner, 2026-10-06, call 46), any stretch at about 11 trains a day or fewer
named and drawn (call 86; none here); **sightseeing funiculars are left out**
(Kobe's rule, 2026-09-27: the 西信貴鋼索線 here); fault-based cost clauses
accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04);
**市内一円 rows are not premises** (Kobe's trap 6, 2026-09-27); MHLW's
notifications as a partial Food-shops layer (call 127b, Kurume's and
Okayama's Retail); a stated food share where a list is incomplete (call
125).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
`label_tier: "minor"`, the **Japan West** view today and **Osaka Prefecture**
after wave 4's retag. Its label offset comes from `check_macro_labels.py`
(PROBLEMS 0 at 375, 768 and 1200), never by eye: Yao's dot sits about 7 km
south of Higashiōsaka's (`app/cities.py`, 34.680 N 135.601 E).

**✅ `mode`: `metro`.** Osaka Metro's Tanimachi Line is drawn (cut, at
八尾南), and Kintetsu holds most of the network (7 of 11 groups); no tram or
light rail. Higashiōsaka's precedent.

---

## The one-line summary

**Food only, from ONE source: MHLW's 食品衛生申請等システム file for Yao
(PDL 1.0, as recorded): 2,180 open restaurant permits, 87.2% of e-Stat's
2,499 in force.** 220 of the 1,598 "addressed" permits give only
`大阪府八尾市内一円` or the like (露店 and 自動車 permits, not premises), so
1,378 carry a real address; **on fixed premises 1,378 of 1,883 (73.2%) can
be placed**, Okayama's 73.3% the precedent; **55.1% of the in-force count**.
Block join **96.8%** of storefronts, MHLW's own point for the 0.1% left.
Storefronts: **Food service 1,204, Retail 981** (467 permits, 514
notifications). **Rail: 11 station groups** (Kintetsu 7, JR West 3, Osaka
Metro 1), **八尾南 drawn cut**; Kintetsu and JR read from the operators'
own timetables: 2 to 10 trains an hour, 58 a day at the fewest.

---

## Business leg — MHLW's open data, alone

| | MHLW open data (27212) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27212_food_business_all.csv`: **1,611,859 B, 4,282 rows** (届出 1,558, 許可 2,711, 許可(廃業) 10, 届出(廃業) 3). UTF-8 with BOM, CRLF, the national schema |
| As of / cadence | Permits **2021-06-08 to 2026-08-31**; closures dated 2026-08-03 .. 08-31 (the file keeps a closed row for its last month only). Monthly (MHLW). Pin `as_of` to **2026-08-31** |
| Columns | 自治体コード, 行番号, 都道府県名, 市区町村名, **営業施設名称、屋号又は商号** (and its フリガナ), **営業の種類**, **業態**, **営業施設所在地**, 営業施設方書, **緯度 / 経度**, 営業施設電話番号, **法人名**, 法人番号, 法人住所, 許可番号, 初回許可年月日, **許可年月日**, 許可開始日, **許可満了日**, **廃業年月日**, **申請区分**, 許可条件, 備考 |
| Shared code | reads every column already (`ADDR_COLS` 営業施設所在地, `NAME_COLS`, `TYPE_COLS` 営業の種類, `FORM_COLS` 業態, `OPERATOR_COLS` 法人名) |

**Yao licenses its own food premises** (a core city since 2018; MHLW's file
is keyed 27212, the city's own health centre). The city publishes no food
list of its own: its open-data page (`/shisei/seisaku_keikaku_zaisei/1009689/1007459.html`,
ページID 1007459) holds two datasets (AED sites, population), and it is not
on BODIK (staging's probe; the master list's row).

### Counts that matter

Open restaurant permits: 許可, 飲食店営業, no 廃業年月日, 許可満了日 on or after
2026-08-31 (none listed has expired).

- **2,180 open 飲食店営業 permits = 87.2% of e-Stat's FY2024 in force
  (2,499: old law 865, revised 1,634).** By grant year: 2021 190 · 2022 414
  · 2023 457 · 2024 384 · 2025 435 · 2026 300. Every 初回許可年月日 is on or
  after 2021-06-01; terms run 5 years (298) or 6 (1,882).
- **Old-law coverage (Kurashiki's trap): absent, as in every MHLW file.**
  MHLW holds permits granted from 2021-06 only; the 319 missing are the old
  law's permits still in term, which renew into MHLW as they expire. Permits granted by 2025-03-31 still open: **1,549 = 94.8%**
  of e-Stat's 1,634 revised-law restaurants at that date (the rest closed
  since, as MHLW drops a closure after its month).
- 🔎 **Addresses.** 1,598 of 2,180 (73.3%) carry a non-blank 営業施設所在地.
  **220 read only `大阪府八尾市内一円`** (one spelling on every restaurant row;
  the notifications add `八尾市八尾市内一円` and `八尾市一円`, which the shared
  一円 test also takes): 業態 露店 142, 自動車 (types I to III) 78. **A real address: 1,378, 63.2%
  of all open restaurant permits.** The 220 share 5 points, MHLW's stand-ins.
- **On fixed premises** (Kurume's measure: every citywide row and every
  vehicle or stall 業態 set aside, `FORM_RULES`' temporary/mobile words: 露店
  204, 自動車 93, of which 77 unaddressed): **1,378 of 1,883, 73.2%**, above
  the reduced-bucket bar's 70%. 業態 is published even where the address is
  withheld (1 of the 505 fixed, unaddressed permits lacks it; 許可条件 on all
  505 names no vehicle or stall), so the split is measured, not guessed. The
  505 withheld: バー 87, 軽食 78, 居酒屋 76, 食堂 66, 高齢者施設 35, テイクアウト
  33 … Bars, snacks and stands withhold more (68.5% addressed against 74.0%
  for the rest). 1,360 distinct (address, trade name) pairs.
- **Of the in-force count: 1,378 fixed, addressed permits = 55.1% of
  e-Stat's 2,499** (stated on the page, call 125).
- **Through `japan_eigyo`** (every open row, step 2's order; 4,269 rows):
  **not a premises 1,589** (blank address 1,265, 一円 324; `permits_from_rows`
  flags every one, no shared-code change), no rule 176 (manufacturing),
  institutional catering 185, vending 88, 仕出し 21, mail order 8, temporary
  9. **Storefronts: Food service 1,204, Retail 981** (permits 467,
  **notifications 514**, a partial opt-in bucket as in Kurume, Fukuoka and
  Okayama; by rule across both: supermarkets by 業態 173, konbini by 業態 161,
  dairy 162, 菓子 156, other food sales 108, butchers 60 …).
- **Closed premises**: MHLW keeps a closed row for the last month only
  (許可(廃業) 10, 6 restaurants, all August 2026); earlier closures leave the
  file. **Repeats**: 25 extra rows in 21 (address, trade name, type) groups
  among open addressed rows; one pin per premises (trap 7) takes them.
- ⚠️ **Economic Census control** (`scripts/japan_census_control.py` at
  build): the 2021 census counts **908** 飲食店 establishments in 27212; 1,202
  distinct placed Food-service premises is **1.32 per establishment**, below
  the built cities' 1.56-1.92 and beside Kurume's 1.37, as expected for a file
  that holds 87% of permits and withholds a quarter of fixed addresses. Report
  it with that reason.

### Personal services: none published

The city's 理容所・美容所 and クリーニング所 pages (`/kenkou_fukushi/shokuhinneisei/1008560/…`,
更新日 令和8年3月31日) carry notification forms only (PDFs), no list; the
open-data page holds no 生活衛生 dataset (staging's probe). **A food-only
page**, Kurume's and Hiroshima's precedent: "**This map shows food
businesses only.**"

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27212-24.0a.zip` (214,122 B,
**39,622 block keys**), town-chōme `.../19.0b/27212-19.0b.zip` (14,021 B,
**634**). `japan.CITIES` entry at build: `"yao": {"name": "八尾市", "pref":
"27", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
"wards": ["27212"]}`.

| Tier (storefronts, `WAVE2_RULES`) | All (2,185) | Food service (1,204) | Retail permits (467) | Notifications (514) |
|---|---|---|---|---|
| Block | **96.8%** | 96.8% | 97.0% | 96.5% |
| Town-chōme | 3.1% | 3.2% | 3.0% | 3.1% |
| Unplaced | 0.1% (3) | 0.1% | 0.0% | 0.4% |
| **Block, chōme or MHLW's own point** (`OWN_POINT_FALLBACK`) | **100%** | | | |

- **Independent check**: MHLW's own coordinates against the block point,
  **median 41 m, 97.3% within 250 m** (2,114 rows; 5 over 1 km).
- **The misses, read** (towns only): unplaced 小畑町, 山本北8丁目 (MLIT's town is
  山本町北), 高町1丁目, one each, all with MHLW's own point. Chōme tier: 北本町2丁目
  6, 佐堂町3丁目 5, 大窪 4, 志紀町2丁目 3 … (地番 MLIT's block file does not key).
- **No shared-code change is needed** for Yao.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_27_GML.zip`, N03 code
27212 (**41.7 km²**, extent W 135.562, S 34.583, E 135.664, N 34.651; the
east rises to the Ikoma hills).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 大阪線 (近畿日本鉄道, 12) | Kintetsu Osaka Line | **5 / 49** | 久宝寺口, 近鉄八尾, 河内山本, 高安, 恩智 |
| 信貴線 (近畿日本鉄道, 12) | Kintetsu Shigi Line | **3 / 3** | 河内山本, 服部川, 信貴山口 |
| 関西線 (西日本旅客鉄道, 11) | JR Yamatoji Line (大和路線) | **3 / 34** | 久宝寺, 八尾, 志紀 |
| おおさか東線 (西日本旅客鉄道, 11) | JR Osaka Higashi Line | **1 / 14** | 久宝寺 (its terminus) |
| 2号線(谷町線) (大阪市高速電気軌道, 21) | Osaka Metro Tanimachi Line | **1 / 26** | 八尾南 (its terminus) |
| 西信貴鋼索線 (近畿日本鉄道, 13) | Nishi-Shigi Cable (funicular) | 2 / 2 | 信貴山口, 高安山: **left out** |

- **15 station records, 12 `N02_005g` groups; 11 drawn** (高安山, the
  funicular's top station, out by Kobe's rule; 信貴山口 stays on the Shigi
  Line). 河内山本 (Osaka and Shigi lines), 久宝寺 (Yamatoji and Osaka Higashi)
  and 信貴山口 are each one group. No name in two groups; no two groups closer
  than 600 m (nearest 714 m, 服部川 to 信貴山口). **Median nearest-group gap
  1,283 m** (714 to 2,574): standard rings by the spacing rule.
- **The master list's row says "Kintetsu 8, JR 3"**: N02 gives **Kintetsu 7,
  JR 3 and Osaka Metro 1** for the same 11 (the universe CSV agrees:
  `docs/coverage_sweep/japan_universe_mhlw.csv`, Kintetsu 7, JR 3, subway
  1). A correction for staging, not an owner question.
- **The one-station rules (calls 54 and 92)**: the **Tanimachi Line** is an
  urban subway with ONE station here, and no other line serves 八尾南 (the
  nearest other station, 志紀, is 2.6 km away): **drawn cut** (Urayasu's
  Tōzai, Suita's Esaka). The **Osaka Higashi Line** is JR, its one station the
  terminus 久宝寺, shared with the Yamatoji Line: **a JR one-station stub stays
  as cut** (standing call 3). The Shigi Line lies wholly inside.
- **Cut at the line** (named by N03 municipality at build): Tanimachi 25
  beyond (大阪市 23, 守口市 2); Osaka Higashi 13 (大阪市 7, 東大阪市 5, 吹田市 1);
  Yamatoji 31 (大阪市 8, 柏原市 3, Nara and beyond 20); Osaka Line 44 (大阪市 4,
  東大阪市 4, 柏原市 5, Nara and Mie 31). Near the line but outside: 弥刀
  (Osaka Line, 282 m, on Higashiōsaka's page) and 法善寺 (Kashiwara, 353 m).
  Inside but near: 久宝寺口 88 m, 八尾南 260 m, 志紀 473 m from the line.
- **The light-rail/rail test**: Kintetsu and JR are railways (N02 class 11 and
  12), the Tanimachi Line a subway (21). No tram or light rail.
- **Frequency, READ 2026-10-06** (weekday departures; counts only, never a
  timetable on the page). Kintetsu from its own timetable host
  (`eki.kintetsu.co.jp/norikae/T5`, line-direction codes from `T2`: 近鉄八尾
  356-8, 恩智 356-11, 服部川 358-1); JR West from the wave-5 probe's cached
  `timetable.jr-odekake.net/station-timetable/<id>` pages, re-counted here:

  | Station (line, direction) | All day | 10:00-15:59 |
  |---|---|---|
  | 近鉄八尾 (Osaka Line, to 大阪上本町 / to 河内国分・名張) | 162 / 159 | **8-10 an hour** |
  | 恩智 (Osaka Line, both ways; beyond 高安, where locals turn) | 82 / 79 | **4** |
  | 服部川 (Shigi Line, both ways) | 58 / 58 | **2** (3 at the peaks) |
  | 八尾 (Yamatoji, to 天王寺; `2989062002`) | 87 | **4** |
  | 志紀 (Yamatoji, to 天王寺; `2988062002`) | 86 | **4** |
  | 久宝寺 (Yamatoji, to 天王寺; `2990062002`) | 164 | **8** (4 locals, 4 大和路快速) |

  **ASSERTED, not read**: the Tanimachi Line at 八尾南 (its terminus; Osaka
  Metro's page was not read; believed every 7 to 8 minutes midday) and the
  Osaka Higashi Line at 久宝寺 (its own direction page was not read). **No
  stretch is at or under about 11 trains a day** (call 86); the Shigi Line's
  58 is the fewest read.
- ⚠️ **Gate 3** at build: Kintetsu's, JR West's and Osaka Metro's station
  counts inside the city (7, 3, 1). **OSM `name:en`** for 11 groups (one
  Overpass query at build; not queried here).

## Scope

**Yao City (27212).** Kintetsu runs on to 大阪上本町 and Nara, the Yamatoji
Line to 天王寺 and Nara, the Osaka Higashi Line to 新大阪, the Tanimachi Line
to 大日; cut at the line. The funicular is left out, its stations not written
to `excluded_stations.csv` (the page says so under **The lines**).

## Licences — MHLW as recorded

- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as recorded in
  `docs/data_sources/japan.md` (read 2026-10-02 for Okayama and Kurume; no new
  read). **MUST DISPLAY**:
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; link the top page only. **MUST NOT**: present it as
  MHLW's own; MHLW's logo; claim completeness or accuracy.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census: measurement
  sources. **Operators' timetables**: counts only.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- MHLW's file carries **法人名, 法人番号, 法人住所 and 営業施設電話番号**: never
  selected into an output. 法人名 is read IN MEMORY for the name rule only (in
  `OPERATOR_COLS` since 2026-10-05).
- **The name rule, version 2, measured in memory** (answers only, never a
  value): 法人名 filled on **1,562 of 2,185** storefront rows, a company marker
  on 1,171, **none on 391**; **0** rows whose trade name is the operator's own
  name, **0** bare personal names.
- Run `check_personal_exposure.py yao` (`japan=True`) after step 2; it must
  print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Osaka Prefecture after the retag), `label_tier:
"minor"`, `"country": "Japan"`. The city runs 135.562-135.664 E, centroid
135.616: project to **UTM 53N (EPSG:32653)**. OSM box from the N03 extent,
rounded out: (34.58, 135.56, 34.66, 135.67).

**Scaffold**: `scaffold_city.py --slug yao --name Yao --system-name
"Kintetsu, JR West and Osaka Metro" --taxonomy japan_eigyo --lat 34.620
--lon 135.616 --region "Japan West" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), the number claimed in
`docs/session_roles.md` at build.

## Owner calls

**Made (do not re-ask):** Band B, food only, Kurume's shape (call 137); the
downloads (call 141); the standing Japanese calls; 八尾南 drawn cut (calls 54
and 92); the Osaka Higashi Line's one station as cut (standing call 3); the
funicular out (Kobe's rule); `mode: metro`; the minor tier, Japan West now
and Osaka Prefecture after the retag; no frequency floor (call 46); MHLW's
notifications as partial Retail (call 127b); the food share stated (call
125); MHLW's own point where the join misses (call 127c).

**Open:** none. The fixed-premises share (73.2%) clears the 70% bar on the
measure the task named.

## What the build must still measure

- `config.source_rows`: MHLW's file alone; `as_of` pinned to **2026-08-31**,
  never today. Expect about 1,204 Food-service and 981 Retail storefronts.
- **Placement disclosure** (Hiroshima's and Kurume's wording): about one fixed
  restaurant in four withholds its address (26.8%); the page states the food
  share against the in-force count (55.1%, call 125).
- The Economic Census control (1.32, below the built range, with the reason);
  the factory share; gate 3; OSM `name:en`; line colours on both basemaps
  (the Tanimachi Line's purple); the opening view (`map-view`);
  `check_provenance.py`; `check_scope_disclosure.py`.
- The page's businesses bullet and What Is Excluded: food only, no personal
  services list, old-law permits and withheld addresses missing, the
  funicular left out.

```brief-checks
[
  {
    "id": "yao-mhlw-live",
    "claim": "MHLW's open-data file for Yao (27212) answers a plain keyless GET (1,611,859 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=27212_food_business_all.csv",
    "min_bytes": 1400000
  },
  {
    "id": "yao-isj-block-live",
    "claim": "MLIT's block-level address file for Yao (27212) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27212-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "yao-isj-chome-live",
    "claim": "MLIT's town-chome file for Yao (27212) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/27212-19.0b.zip",
    "min_bytes": 10000
  },
  {
    "id": "yao-open-data-two-datasets",
    "claim": "Yao's open-data page offers two dataset files (AED sites, population) and no CSV or food list (the site menu links the food-hygiene section, so its path is no anchor)",
    "kind": "http_contains",
    "url": "https://www.city.yao.osaka.jp/shisei/seisaku_keikaku_zaisei/1009689/1007459.html",
    "present": ["aedjoukyou.xlsx", "272124_population.xlsx"],
    "absent": [".csv", "food_business"]
  },
  {
    "id": "yao-kintetsu-yao-timetable",
    "claim": "Kintetsu's timetable host lists both Osaka Line directions for 近鉄八尾 (line-direction code 356-8) - a frequency source; ASCII anchors (the page is Shift_JIS)",
    "kind": "http_contains",
    "url": "https://eki.kintetsu.co.jp/norikae/T2?USR=PC&sf=%8B%DF%93S%94%AA%94%F6&dw=0",
    "present": ["356-8,1", "356-8,2"]
  },
  {
    "id": "yao-jr-yao-timetable",
    "claim": "JR West's timetable index for 八尾 (EID 0620824) links the Yamatoji Line's two weekday pages (2989062001, 2989062002)",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/cgi-bin/mydia_sp.cgi?MD=3&FN=0&EID=0620824",
    "present": ["2989062001", "2989062002"]
  },
  {
    "id": "yao-projected-crs",
    "claim": "Yao projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.616,
    "expect": "EPSG:32653"
  }
]
```
