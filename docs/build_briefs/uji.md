# Uji — build brief

**Band A, food only, its own page (not Kyoto (Regional)), owner-approved
2026-10-06** (Japan wave 4, banded in staging's wave 5;
`docs/decisions_drafts/staging.md`, "Wave 5: the ranked queue and the
pre-verdicts screened": "Uji (food only, its own page, Gimhae's precedent)").
The Step 0 downloads were approved by the owner 2026-10-06 (call 67). **Step 0
measured 2026-10-06** (staging). Into `data/uji/raw/` (gitignored), each from
its publisher's own host, project user-agent, each HTTP 200:

- From `i2fas.mhlw.go.jp`: `26000_food_business_all.csv`, **Kyoto
  Prefecture's file** (8,824,655 B, the size approved).
- From `nlftp.mlit.go.jp`: `isj/26204-24.0a.zip` (122,551 B) and
  `isj/26204-19.0b.zip` (5,568 B). Kyoto's build caches only its 11 wards'
  zips (`data/kyoto/raw/isj/`, 26101-26111), so Uji's were fetched fresh.
  Nothing was written under `data/kyoto/`.
- Not fetched: Kyoto Prefecture's barber, beauty and laundry PDFs (not
  approved: the prefecture's site terms forbid copying without permission;
  a licence read decides, so they are a later bucket at most).

**Run `python scripts/brief_check.py uji` before writing any code.** Then the
`japan-city` skill, **Kurume's shape** (MHLW's open data alone, food only;
`docs/build_briefs/kurume.md`, `pipeline/kurume/config.py`), with one
difference that is new for a food page: **the file is the prefecture's**, so
every row is assigned to Uji by its address (below). Coordinates: the
`address-join` skill, measured with the shared
`pipeline/countries/japan_register.py` functions from scratch scripts
(`scripts/screen_japan_join.py` has no Uji entry; add one at build). Rail:
MLIT N02-25 cut at the N03 city line, measured through
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
(2026-10-06): MHLW's 法人名 is an operator column (2026-10-05) and a bare
personal name is withheld whatever it holds; (6) **no page says "currently
operating"**. Also: no frequency floor for JR or private lines in Japan
(owner, 2026-10-06, call 46), any stretch at about 11 trains a day or fewer
named and drawn (call 86); fault-based cost clauses accepted for all of Japan
(2026-09-24); English station names from OSM `name:en`; every Japanese city
reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Uji
carries `label_tier: "minor"` and goes in the **Japan West** view, as Kyoto,
Ōtsu and Nara do (`app/cities.py`; wave 4's first city to land retags Japan
into the eight regions, Uji into **Kansai**). Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye. Uji's
dot sits about 12 km south-southeast of Kyoto's (35.01, 135.77) and 11 km
southwest of Ōtsu's: measure its label against both.

**`mode`: `metro`** (the owner's rule of 2026-10-02, Dublin's precedent). No
subway is drawn (the Tōzai is left out, below), so the mode follows the JR
test: **JR West is the largest network inside the city line** (6 station
groups, against Keihan's 4 and Kintetsu's 3), "substantial JR reads as
metro" (Okayama, Kitakyushu). Keihan's Uji Line and Kintetsu's Kyoto Line are
conventional railways (N02 class 12), so nothing here reads as light rail.

---

## The one-line summary

**Food only, from ONE source: MHLW's 食品衛生申請等システム file for Kyoto
Prefecture (26000), cut to Uji by address.** **1,600 open restaurant permits
are addressed to 宇治市, but 691 of them are the prefecture's vehicles and
stalls (`京都府宇治市京都府内一円`), so 909 carry a real address.** Kyoto
Prefecture's file holds **91.6% of the prefecture's restaurants in force**
(9,801 of e-Stat's 10,702 outside Kyoto City); **85.9% of its fixed premises
publish an address**. Uji's storefronts: **Food service 782, Retail 520 pins
(1,302)**. Block join **92.7% with two new shared rules, 55.0% without
them** (⚠️ shared code at build), MHLW's own point for every other row. 12
station groups: JR 6, Keihan 4, Kintetsu 3, the Tōzai's one left out (its
station shared with JR). **No personal-services register usable now.**

---

## Business leg — MHLW's open data, alone

| | MHLW open data (26000, Kyoto Prefecture) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=26000_food_business_all.csv`: **8,824,655 B, 21,125 rows** (許可 13,788, 届出 7,285, 許可(廃業) 28, 届出(廃業) 24). UTF-8 CSV, the national schema |
| As of / cadence | Permits to **2026-08-31**; closures dated 2026-08-01 .. 08-31. Monthly (MHLW). `as_of` 2026-08-31 |
| Columns | 自治体コード, 行番号, 都道府県名, 市区町村名, 営業施設名称、屋号又は商号 (+ フリガナ), 営業の種類, **業態**, **営業施設所在地**, 営業施設方書, **緯度 / 経度**, 営業施設電話番号, 法人名, 法人番号, 法人住所, 許可番号, 初回許可年月日, 許可年月日, 許可開始日, 許可満了日, 廃業年月日, 申請区分, 許可条件, 備考 |
| **Municipality** | **None in the data.** 自治体コード is `026000` and 市区町村名 `京都市上京区` (the prefecture's own seat) on **every** row. The municipality is read from 営業施設所在地 |

### Cutting Uji out of the prefecture's file

- **The rule: an address that begins `京都府宇治市`** (after NFKC and spaces
  removed). **2,498 rows** (許可 1,949, 届出 548, 許可(廃業) 1). Every
  addressed row in the file begins `京都府` (0 without it), and every one
  parses to one of the prefecture's 25 municipalities outside Kyoto City (0
  unknown).
- **宇治田原町 is excluded by construction**: it is a separate town in 綴喜郡,
  and all **189** of its rows begin `京都府綴喜郡宇治田原町`, never `京都府宇治市`
  (0 rows contain 宇治市 without beginning with it; 0 begin `京都府宇治` other
  than these two). The build's `config.source_rows("mhlw")` yields the rows
  that begin `京都府宇治市` and **raises** on any row that mentions 宇治 and
  begins with neither prefix, so a re-spelled address stops the build rather
  than leaking a row in or out.
- **The prefecture's 4,050 unaddressed rows cannot be assigned to any town**
  (the 市区町村名 column does not say). They are the withheld share, measured
  prefecture-wide below. One unaddressed row has 宇治市 in its 法人住所, an
  operator's address, never read for placement.
- `permits_from_rows(rows, "京都府", "宇治市", wardless=True, WAVE2_RULES)`
  reads the cut rows as is; the city name is stripped once, from the start.

### Counts that matter

(Open restaurant permits: 許可, 飲食店営業, no 廃業年月日, 許可満了日 on or after
2026-08-31; 22 prefecture permits expire on that day and are kept.)

- **Coverage, prefecture-wide: 9,801 open 飲食店営業 permits = 91.6% of
  e-Stat's FY2024 in force for Kyoto Prefecture's own jurisdiction (10,702 =
  京都府 36,772 less 京都市 26,070; the prefecture row includes its designated
  city: the 46 prefecture rows sum to 1,424,296 of the national 1,434,613).**
  First permits from 2021 on (7 earlier): the prefecture enters every
  revised-law permit, and the gap is old-law permits still in term.
- **Uji's own coverage cannot be measured**: e-Stat's 衛生行政報告例 publishes
  prefectures, designated cities and core cities only, and Uji is none
  (`docs/coverage_sweep/japan_universe_mhlw.csv` has no official count for
  26204). The town-level check is the Economic Census control below.
- **Uji: 1,600 open restaurant permits addressed to the city** (19.1% of the
  prefecture's 8,359 addressed). **691 are not premises**: their address
  after 宇治市 is `京都府内一円` (564), `京都府内一円(京都市を除く。)` (121),
  `宇治京都府内一円` (4) or `京都府一円(京都市を除く。)` (2); 業態 露店 384
  (one spelled 露天), 自動車 291, キッチンカー 4, 屋台 2, one other, blank 9. They are vehicles and stalls licensed
  across the prefecture and filed under a base in Uji, on 5 shared points.
  `permits_from_rows` already flags `一円` as not a premises; no new rule.
- **A real address: 909** (908 with a fixed form). By first-permit year: 2021
  133 · 2022 367 · 2023 307 · 2024 280 · 2025 288 · 2026 225 (all 1,600).
  1,598 of 1,600 carry MHLW's own point.
- **Withheld addresses, measured prefecture-wide**: of 7,151 fixed open
  restaurants (no vehicle or stall 業態, not a 一円 address), **6,144 publish
  an address (85.9%)**; 1,007 do not (664 of them with a blank 業態). Uji's
  own share is unknowable from the file; at the prefecture's rate about 150
  fixed restaurants in Uji would be missing. **About one restaurant in seven**
  (page wording: open call 1).
- **Food shops (the standing call)**: open 菓子製造業 **168**, そうざい製造業
  **34** in Uji (165 and 33 + 1 複合型 on fixed premises after the
  taxonomy). **21 of 199** 菓子 / そうざい Retail rows are named 工場 / センター
  (10.6%), kept (the 2026-09-27 call).
- **Through `japan_eigyo`** (all 2,497 open rows, step 2's order): not a
  premises **742** (the 691 above and other 一円 rows); out by rule: no rule
  161 (製茶業 42, その他の食料品製造・加工業 29, packaging, health foods,
  coffee, pickles and the other manufacturing types), institutional catering
  51 + 46 by 業態, vending machines 55 + 4, hostess venues 8, entertainment
  venues 8, temporary or mobile 10, inside accommodation 2, event
  catering 2, mail order 2. **Storefront rows: Food service 782 (all 飲食店
  permits), Retail 624** (許可 338, **届出 286**: MHLW's notifications, a
  partial opt-in bucket as in Fukuoka, Okayama and Kurume, disclosed; 60
  飲食店 permits whose 業態 is a convenience store or supermarket go to Retail
  by `FORM_RULES`).
- **One pin per (address, trade name, bucket)**: 1,406 rows → **1,302 pins**
  (Food service 782, Retail 520).
- **Closed and duplicate checks**: one Uji row is 許可(廃業) (dropped); no
  open restaurant permit is past its 許可満了日. 1,561 distinct (address, trade
  name) pairs among the 1,600 open restaurant permits.
- **製茶業, 42 rows on fixed premises, stays out** by the taxonomy's
  manufacturing rule (`japan_eigyo`: "manufacturing, catch-alls: out, and
  measured"; `docs/category_rules.md` has no tea exception). Flagged only
  because Uji is a tea town: a tea maker's counter sales, where notified as
  その他の食料・飲料販売業, are in Retail already. The precedent applies; no
  owner call.

**Personal services: none usable now.** Uji's BODIK organization holds no
lists (the probe, 2026-10-06). Kyoto Prefecture publishes barber, beauty and
laundry PDFs (to 2025-03-31, monthly openings to 2026-08), but its site terms
(2008) forbid copying without permission: **a later bucket, after a licence
read and the owner's approval**, never at this build. **A food-only page,
Hiroshima's, Okayama's and Kurume's precedent.**

## Coordinates — a JOIN to MLIT 位置参照情報

One municipality (26204, **no wards**, `"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/26204-24.0a.zip` (122,551 B,
14,776 rows, **12,435 block keys** incl. the 大字 + 字 + 小字 keys), town-chōme
`.../19.0b/26204-19.0b.zip` (5,568 B, 55 keys).

| Tier (storefront rows, 1,406) | Shared code as is | With rules (a) + (b) | Food service, with both |
|---|---|---|---|
| Block | 55.0% | **92.7%** | 93.5% |
| Town-chōme / 大字 centroid | 1.4% | 3.9% | 3.6% |
| Unplaced | 43.7% | 3.4% | 2.9% |
| **Block or MHLW's own point** (`OWN_POINT_FALLBACK`) | | **100%** (all 103 non-block rows carry MHLW's point) | |

- ⚠️ **Shared code needed, rule (a): Uji's addresses leave out the 字
  between a 大字 and its 小字.** The permits write `宇治妙楽 55` where MLIT keys
  `宇治` + 小字 `妙楽` (`load_city_isj`'s Sendai key `宇治字妙楽`). Rule C
  (`known_town`) never tries a 2-character 大字 (宇治, 莵道, 木幡), so the row
  is unplaced. The scratch rule: where the parsed town is not a known town
  and some prefix of it is a 大字 that MLIT also keys with 小字, read it as
  prefix + 字 + rest when that key exists. **1,297 rows rewritten; block 55.0%
  → 88.5%.** Top misses before it: 宇治妙楽 79, 宇治壱番 34, 宇治蓮華 29, 莵道平町
  26, 宇治樋ノ尻 25, 宇治下居 22.
- ⚠️ **Rule (b): 蔵 for MLIT's 藏.** MLIT writes 六地藏, the permits 六地蔵
  (59 rows; 六地蔵奈良町 32, 六地蔵町並 25). One more pair in `VARIANTS`, both
  sides. **88.5% → 92.7%.**
- Both go into `japan_register` as opt-in rules (named for Uji, as
  `WAVE2_RULES` documents each), with **the Minato control re-run** (must stay
  98.0 / 0.2 / 1.8) and every built city's screen old against new.
- **Misses left (48)**: 宇治宇文字 18 (MLIT's spelling to read at build),
  槙島町一丁田 6, the 自衛隊 site, a few 小字 MLIT lacks; tails mostly `9-9`.
  All placed by MHLW's point.
- **Independent check**: MHLW's own coordinates against the block point,
  **median 51 m, 95.4% within 250 m** (1,303 rows; 1 over 1 km).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_26_GML.zip`, N03 code 26204
(67.5 km², extent W 135.7596, S 34.8579, E 135.8799, N 34.9574; centroid
34.903, 135.820). **N02-24 agrees** (14 records, 12 groups, no name
difference). No Shinkansen inside.

| N02 line (operator) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 奈良線 (西日本旅客鉄道, class 11) | JR Nara Line | **6 / 19** | 六地蔵, 木幡, 黄檗, 宇治, JR小倉, 新田 |
| 宇治線 (京阪電気鉄道, 12) | Keihan Uji Line | **4 / 8** | 木幡, 黄檗, 三室戸, 宇治 (its terminus) |
| 京都線 (近畿日本鉄道, 12) | Kintetsu Kyoto Line | **3 / 26** | 小倉, 伊勢田, 大久保 |
| 東西線 (京都市, 12) | Kyoto Municipal Subway Tōzai Line | **1 / 17** | 六地蔵 (its terminus): ⛔ **left out** |

- **12 station groups** (N02 `N02_005g`): JR 6, Keihan 4, Kintetsu 3, the
  Tōzai 1. Two groups are interchanges: **六地蔵 (006224: JR + the Tōzai,
  128 m)** and **黄檗 (006276: JR + Keihan, 146 m)**. **Kept apart, as N02
  keeps them** (trap 1): 宇治 (JR 006334, Keihan 006319) and 木幡 (JR 006254,
  Keihan 006247), each two stations of one name, so their English names take
  the operator (`LINES[...]["short"]`, Kobe's Mikage). Median gap to the
  nearest group **588 m** (closest 302 m, widest 1,329 m): the ring size by
  the spacing rule at build.
- ✅ **The Tōzai is left out, measured from N02** (the one-station rule,
  owner 2026-10-06, calls 54 and 92): its one station in Uji, 六地蔵, is in
  **the same N02 group as JR's 六地蔵 (006224), both inside Uji**, so the ring
  stays through the JR Nara Line. **Keihan's 六地蔵 is a different station in
  Kyoto's Fushimi Ward** (group 006231, 359 m from the Tōzai's platform),
  outside the city. Not Urayasu's or Esaka's exception (there no other line
  served the station). `config.LEFT_OUT_LINES` for N02's 京都市 東西線, with the
  page's bullet (Ichikawa's Toei Shinjuku Line, a review-time proposal);
  `check_scope_disclosure.py` decides whether its stations belong in
  `excluded_stations.csv`. Kyoto's own map already cuts the Tōzai at 六地蔵
  (16 of 17 drawn; `docs/build_briefs/kyoto.md`).
- **Stub test**: no other urban line; JR and the private lines are cut at the
  line. **Three lines are drawn.**
- **Frequency**: **JR Nara Line READ** (JR West's station timetable for 宇治
  toward 京都, weekday 2026-10-06, read by the wave-5 probe and re-counted
  here): 98 departures a day, 70 of them locals; 5 to 9 an hour from 07:00 to
  19:59, 6 most hours (locals about 4 an hour plus the みやこ路快速). **Keihan
  Uji Line ASSERTED** (about every 10 minutes): Keihan's station timetables
  are PDFs with no extractable text (the probe's 黄檗 weekday PDF; pdftotext
  returns nothing). **Kintetsu Kyoto Line ASSERTED** (locals about every 15
  minutes): `www.kintetsu.jp/tetsudo/` answers 404 and the timetable host
  `eki.kintetsu.co.jp` answers **403 to the project's user-agent** (recorded,
  not retried). No stretch near 11 trains a day is known on any line; no
  floor applies (call 46).
- **The light-rail / rail test** (the skill's mode rule): no tram or light
  rail; all three drawn lines are railways. `mode` `metro` by the JR test.
- **OSM `name:en`** (read from Kyoto's cache, `data/kyoto/raw/osm_station_names.json`,
  read only): every station has one. **木幡 is two spellings for two
  stations** (JR "Kohata", Keihan "Kowata": the operators read it
  differently, Kyoto's 西院 shape, but here they are separate N02 groups, so
  no tie is needed; keep both). 宇治: "Uji" twice → Uji (JR) / Uji (Keihan).
  JR小倉 is "JR-Ogura" (OSM's hyphen; settle the style in
  `OSM_NAME_EN_OVERRIDES` at build). The build fetches its own names (one
  Overpass query, the CLAUDE.md rule) for its `CITY_BBOX`.
- ⚠️ **Gate 3** (JR West's, Keihan's and Kintetsu's per-line station counts)
  and line colors on both basemaps at build.

## Scope

**Uji City.** All four lines run on into **Kyoto City's Fushimi Ward** to the
north (JR's 桃山, Keihan's 六地蔵, Kintetsu's 向島, the Tōzai's 石田) and JR and
Kintetsu into **Jōyō** to the south (城陽, 久津川); cut at the line, the
stations beyond named by N03 municipality at build. **Its own page**, not an
extension of Kyoto (Gimhae's precedent, owner 2026-10-06): Kyoto's page is
the city's rebuilt register; Uji's is MHLW's prefecture file.

## Licences

- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as recorded in
  `docs/data_sources/japan.md` and for every MHLW city built (Okayama,
  Kurume, Shimonoseki). No new read: the 26000 file is the same service and
  terms. **MUST DISPLAY**:
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; link the top page only. **MUST NOT**: present it as
  MHLW's own; MHLW's logo; claim completeness or accuracy. 免責 2)ウ the minor
  open point, fine while the site is non-commercial.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **N03**: CC BY 4.0, ⛔ never drawn.
- **Kyoto Prefecture's personal-services PDFs**: not used; the site terms
  (2008) as read by the probe forbid copying without permission. A licence
  read (the `licence-read` agent) before any later use; no verdict here.

## Privacy

MHLW's file carries **法人名, 法人番号, 法人住所 and phones**: never selected
for output. **The name rule, version 2, runs on 法人名** (in memory, yes or no
only):
- 法人名 filled on **2,077** of Uji's 2,497 open rows; **1,299** with a
  法人番号; **778** with neither a 法人番号 nor a company or cooperative
  marker (where a sole trader's own name can sit).
- **Flagged: 7 open rows** (trade name equals an individual's 法人名; 9
  without the `coop` rule, so 2 are cooperatives); **0 bare personal names**
  under the sign rule. **2 reach the storefronts (2 pins)**, shown by permit
  type. No value was printed or stored.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map:
  it must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md` at build.

## Region

`"region": "Japan West"` (Kansai after the retag), `"country": "Japan"`,
`label_tier: "minor"`, `coverage` narrowed (food only). Project to **UTM 53N
(EPSG:32653)**: the centroid lies at longitude 135.820, the extent 135.7596 to
135.8799, all inside the 132-138 band (computed here, never copied).

**Scaffold**: `scaffold_city.py --slug uji --name Uji --system-name "JR West,
Keihan and Kintetsu" --taxonomy japan_eigyo --lat 34.903 --lon 135.820
--region "Japan West" --country Japan --mode metro --page-number <N>`
(`--dry-run` first), with the page number claimed in `docs/session_roles.md`
at build, not here. A `japan.CITIES` entry: `"uji": {"name": "宇治市", "pref":
"26", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
"wards": ["26204"]}` (plus Uji's two new rules).

## Owner calls

**Made:** Band A, food only, its own page (owner, 2026-10-06); the Step 0
downloads (owner, 2026-10-06, call 67); MHLW alone, food only, the name rule
on 法人名 (Okayama's and Kurume's shape, 2026-10-02, 2026-10-05); the Tōzai
left out by the one-station rule (calls 54 and 92, measured above); no
frequency floor (call 46); 製茶業 out by the manufacturing precedent.

**Open:**
1. **The withheld-address sentence names a prefecture, not the city** (a
   review-time proposal, drafted at build). The template reads "About one
   restaurant in <n> in <City> chose not to publish its address…", but Uji's
   own share cannot be measured. **Recommendation**: "About one restaurant in
   seven in Kyoto Prefecture's filings (outside Kyoto City) chose not to
   publish its address in the national filing system, so some in Uji are not
   on this map. Where they are is not known." Tradeoff: one clause longer than
   the template, and honest about the unit it was measured on; the template's
   "in Uji" would state a number never measured for Uji.

## Still open — what the build must measure

- ⚠️ **Shared code**: rules (a) (字 omitted) and (b) (蔵 / 藏) in
  `japan_register`, opt-in; the Minato control and every built screen re-run.
- ⚠️ **`config.source_rows`**: the address prefix cut, raising on an
  ambiguous 宇治 row (above); state the 189 宇治田原町 rows in the drafts entry.
- ⚠️ **Economic Census join control**: the 2021 census counts **436** 飲食店
  establishments in 26204 (宇治田原町 12, apart); 782 Food-service pins is
  **1.79 per establishment**, inside the built cities' 1.56-1.92 (Kurume
  1.37). Re-run `scripts/japan_census_control.py` at build.
- ⚠️ Notifications as partial Retail (disclosed); the withheld share
  (open call 1); gate 3; OSM `name:en` styles; line colors on both basemaps;
  the macro label against Kyoto's and Ōtsu's.
- ⚠️ The Tōzai's page bullet and its `excluded_stations.csv` question
  (Ichikawa's handling).
- Later, not this build: Kyoto Prefecture's personal-services PDFs, only
  after a licence read and the owner's approval.

```brief-checks
[
  {
    "id": "uji-mhlw-live",
    "claim": "MHLW's open-data file for Kyoto Prefecture (26000), the file Uji is cut from, answers a plain keyless GET (8,824,655 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=26000_food_business_all.csv",
    "min_bytes": 8000000
  },
  {
    "id": "uji-isj-block-live",
    "claim": "MLIT's block-level address file for Uji (26204) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/26204-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "uji-isj-chome-live",
    "claim": "MLIT's town-chome address file for Uji (26204) answers keyless - the centroid tier",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/26204-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "uji-keihan-timetables-pdf",
    "claim": "Keihan's station page for Obaku offers its timetables only as PDFs (the reason the Keihan Uji Line's frequency is ASSERTED)",
    "kind": "http_contains",
    "url": "https://www.keihan.co.jp/traffic/station/312/info.html",
    "present": ["/traffic/station/assets/pdf/time/31211.pdf"]
  },
  {
    "id": "uji-kintetsu-timetable-refused",
    "claim": "Kintetsu's timetable host refuses the project's user-agent with 403 (the reason the Kintetsu Kyoto Line's frequency is ASSERTED)",
    "kind": "http_ok",
    "url": "https://eki.kintetsu.co.jp/",
    "expect_status": 403
  },
  {
    "id": "uji-projected-crs",
    "claim": "Uji projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.82,
    "expect": "EPSG:32653"
  }
]
```
