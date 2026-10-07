# Kure — build brief

**Band B, food only (Kurume's shape), with the food share stated,
owner-approved 2026-10-06** (Japan wave 5, call 185, "185 yes, B with share
stated": `docs/decisions_drafts/staging.md`, "Kure (call 185 ...)"; moved from
C on call 139's bar). The Step 0 downloads were approved by the owner
2026-10-06 (call 141). **Step 0 measured 2026-10-06** (staging). Into
`data/kure/raw/` (gitignored), each from its publisher's own host with the
project user-agent, each HTTP 200, under each URL's own file name as
`japan_fetch.get` saves:

- From `i2fas.mhlw.go.jp`: `34202_food_business_all.csv` (**1,149,444 B**),
  the only business source.
- From `nlftp.mlit.go.jp`: `isj/34202-24.0a.zip` (201,697 B) and
  `isj/34202-19.0b.zip` (13,410 B).

**1,364,551 B in all.** Nothing else was downloaded. JR West's station
timetable pages (`timetable.jr-odekake.net`) were read by plain GET for
departure counts (pages, not data files).

**Run `python scripts/brief_check.py kure` before writing any code.** Then the
`japan-city` skill, **Kurume's shape** (`docs/build_briefs/kurume.md`: MHLW's
open data alone, food only, the fixed-premises measure) with Okayama's and
Hiroshima's food-only page; `docs/build_briefs/yao.md` and `takatsuki.md` are
the same build, measured the same day by the same scripts. Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only (`scripts/screen_japan_join.py` has no Kure entry;
its table is shared code and was not edited). Rail: MLIT N02-25 cut at the N03
city line, through `pipeline/countries/japan.py` with an in-memory `CITIES`
entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27); an URBAN line cut to ONE station is left
out, its station kept through the other lines, and drawn cut only where no
other line serves that station (owner, 2026-10-06, calls 54, 92, 163, 165 and
167; no urban line here); (4) **菓子製造業 and そうざい製造業 count, in
Retail**, the factory share measured and kept (2026-09-24, 2026-09-27); (5)
**the name rule**, version 2 (2026-10-06): 法人名 is an operator column
(2026-10-05) and a bare personal name is withheld whatever it holds; (6) **no
page says "currently operating"**. Also: no frequency floor for JR or private
lines in Japan (owner, 2026-10-06, call 46), any stretch at about 11 trains a
day or fewer named and drawn (call 86; none here); fault-based cost clauses
accepted for all of Japan (2026-09-24); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04);
**市内一円 rows are not premises** (Kobe's trap 6, 2026-09-27); MHLW's
notifications as a partial Food-shops layer (call 127b, Kurume's and
Okayama's Retail); MHLW's own point where the block join misses (call 127c);
**the block-join tiers disclosed** where the block share is low (call 145,
Kakogawa's precedent); a stated food share where a list is incomplete (call
125, Ichinomiya's sentence shape). **The shared-code rules for the build
(owner, 2026-10-06):** combined-form restaurant cells stay in Food service
unless the cell names 給食 or 旅館 (158); permits past their term are dropped
(161); an address of the city name alone is not a premises (162); a permit
that starts after the as-of waits (172); 自動車以外 is not a vehicle; an
asterisk-only address is withheld.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
`label_tier: "minor"`, the **Japan West** view today and **Chūgoku** after
wave 4's retag. Its label offset comes from `check_macro_labels.py` (PROBLEMS
0 at 375, 768 and 1200), never by eye: Kure's dot (呉, 34.245 N 132.558 E)
sits about 19 km south-east of Hiroshima's (`app/cities.py`, 34.396 N
132.460 E).

**✅ `mode`: `metro`** (the owner's rule of 2026-10-02, "unless there is
substantial JR, JR reads as metro"): JR West holds all 13 station groups; no
subway, tram or light rail. Tottori's, Aomori's and Fukuyama's precedent.

---

## The one-line summary

**Food only, from ONE source: MHLW's 食品衛生申請等システム file for Kure (PDL
1.0, as recorded): 1,543 open restaurant permits in term on 2026-08-31, 88.1%
of e-Stat's 1,752 in force.** **On fixed premises 1,022 of 1,474 (69.3%) carry
a real address** (the owner's call 185 took the same reading, 1,025 of 1,477,
69.4%, before call 172 set three not-yet-started permits aside: below);
**58.3% of the in-force count**, stated on the page. Block join **88.1%** of
storefronts (Food service 89.7%), the town-chōme centroid for 11.7%, mostly
on the islands (tiers disclosed, call 145), MHLW's own point for the 0.2%
left. Storefronts: **Food service 808, Retail 960** (448 permits, 512
notifications). **Rail: 13 station groups, all on the JR Kure Line**, read
from JR West's own timetables: 20 to 57 trains a day each way, hourly east of
広 and every 20 to 45 minutes west of it.

---

## Business leg — MHLW's open data, alone

| | MHLW open data (34202) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=34202_food_business_all.csv`: **1,149,444 B, 3,538 rows** (届出 1,286, 許可 2,246, 許可(廃業) 3, 届出(廃業) 3). UTF-8 with BOM, CRLF, the national schema |
| As of / cadence | Permits **2021-06-01 to 2026-08-28**; closures dated 2026-08-20 and 08-31 (the file keeps a closed row for its last month only). Monthly (MHLW). Pin `as_of` to **2026-08-31** |
| Columns | 25, as Yao's and Kurume's: 自治体コード, 行番号, 都道府県名, 市区町村名, **営業施設名称、屋号又は商号** (and its フリガナ), **営業の種類**, **業態**, **営業施設所在地**, 営業施設方書, **緯度 / 経度**, 営業施設電話番号, **法人名**, 法人番号, 法人住所, 許可番号, 初回許可年月日, **許可年月日**, **許可開始日**, **許可満了日**, **廃業年月日**, **申請区分**, **許可条件**, 備考 |
| Shared code | reads every column already (`ADDR_COLS`, `NAME_COLS`, `TYPE_COLS`, `FORM_COLS`, `OPERATOR_COLS`); the type cell carries a circled number (`① 飲食店営業` on every restaurant row), which `japan_eigyo.normalise` strips |

**Kure licenses its own food premises** (a core city with its own health
centre; MHLW's file is keyed 34202, and e-Stat reports 広島県呉市 on its own
row). The city publishes no food list of its own: its 生活衛生課 pages
(`/soshiki/62/`) carry procedures and forms, its open-data page
(`/soshiki/36/opendata-index.html`) points to the city's platform on
`expolis.cloud`, which is script-rendered, and the hygiene division's pages
were enumerated with no list found (staging's wave-5 probe; the master list's
row).

### Counts that matter

Open restaurant permits: 許可, 飲食店営業, no 廃業年月日, 許可満了日 on or after
2026-08-31 (none listed has expired, call 161), 許可開始日 on or before
2026-08-31 (call 172: **3 restaurant permits start on 2026-09-01 or
2026-10-01 and wait**, with 4 other rows; 1,546 before that rule).

- **1,543 open 飲食店営業 permits = 88.1% of e-Stat's FY2024 in force
  (1,752: old law 604, revised 1,148).** By grant year: 2021 199 · 2022 285
  · 2023 265 · 2024 260 · 2025 325 · 2026 209. Every 初回許可年月日 is on or
  after 2021-06-01; terms run mostly 6 years (981 of the 1,546 listed) or 5
  (479), 7 on 85.
- **Old-law coverage (Kurashiki's trap): absent, as in every MHLW file.**
  MHLW holds permits granted from 2021-06 only; the 209 missing are about the
  old law's permits still in term, which renew into MHLW as they expire.
  Permits granted by 2025-03-31 still open: **1,082 = 94.3%** of e-Stat's
  1,148 revised-law restaurants at that date.
- **Today's address rules, measured**: no address of the city name alone
  (162), no asterisk-only address, no 自動車以外 in any 業態 or 許可条件, no
  combined-form restaurant cell (158; every restaurant row reads `①
  飲食店営業`). The citywide test (一円) takes 9 restaurant permits (業態
  キッチンカー 3, 屋台 80ℓ 3, 露店 2, 屋台 1) and 26 rows in all.
- 🔎 **Addresses.** 1,056 of 1,543 (68.4%) carry a non-blank 営業施設所在地;
  **a real address (citywide rows out): 1,047, 67.9% of all open restaurant
  permits.**
- **On fixed premises** (Kurume's measure: every citywide row and every
  vehicle or stall set aside): **1,022 of 1,474, 69.3%**, about the
  reduced-bucket bar's 70% (call 185). Vehicles and stalls: **65**, of which
  30 addressed: 57 by `FORM_RULES`' temporary/mobile words in 業態
  (キッチンカー 10, 露店 6, 移動販売車 4, キッチンカー 広島県一円 and its variants
  …; 24 addressed) and **8 more by the permit condition alone** (below). The
  452 fixed, unaddressed permits: 業態 blank 52, スタンド 23, テイクアウトあり
  16, 食堂 14, 喫茶店 14, スタンドバー 14, バー 13, スナック 12, 居酒屋 7, 社員食堂 7
  …; 許可条件 on none of them names a vehicle or stall. Bars, snacks, stands,
  izakaya and light meals withhold no more than the rest (69.2% addressed
  against 69.4%). Upper bound, were the 52 blank-業態 rows all vehicles:
  71.9%. 1,019 distinct (address, trade name) pairs.
- ⚖️ **The two figure sets, settled.** Staging's first pass
  (`measure.txt`: **1,031 of 1,485**) set vehicles and stalls aside by 業態
  alone; the refinement (**1,025 of 1,477**, the figure call 185 accepted)
  also reads 許可条件, where the health centre classes the permit itself.
  **The refinement is right**: 8 permits are vehicles or stalls by their
  condition while their 業態 is blank or free text: **3 read 自動車(…)**
  (the revised law's vehicle classes, 業態 blank; 1 addressed) and **5
  read 露店による営業** (業態 屋台 2, 蔵本通屋台, 屋台（朝市）, 露天営業; all
  addressed). Kurume's measure sets every vehicle or stall aside, and 露店 is
  among the temporary words since the owner's 2026-09-29 call; the 業態-only
  pass counted these 8 as fixed premises (6 of them addressed, hence 1,031 −
  6 and 1,485 − 8). Both read 69.4%. **Call 172 then sets aside 3 fixed,
  addressed permits that start after the as-of: 1,022 of 1,474, 69.3%**, the
  figure the build will reproduce; the owner's reading is unchanged.
- **Of the in-force count: 1,022 fixed, addressed permits = 58.3% of
  e-Stat's 1,752** (stated on the page, call 125; 58.5% before call 172).
- **Through `japan_eigyo`** (every open row, step 2's order, call 172
  applied; 3,525 rows, 2,239 permits and 1,286 notifications): **not a
  premises 1,195** (blank address 1,169, 一円 26; `permits_from_rows` flags
  every one), no rule 228 (manufacturing), institutional catering 145 (36 by
  業態), temporary or mobile by 業態 38, hostess venues by 業態 36, vending 33,
  entertainment by 業態 28, accommodation by 業態 27, mail order 11, 仕出し 9.
  **Storefronts: Food service 808, Retail 960** (permits 448,
  **notifications 512**, a partial opt-in bucket as in Kurume, Fukuoka and
  Okayama, call 127b: 803 open notifications carry a real address). By rule:
  restaurants 796, **yatai by 業態 12** (Fukuoka's rule; the 蔵本通屋台 row
  among them), other food sales 247, 菓子 137, konbini 139, supermarkets 109,
  fishmongers 84, dairy 77, deli 75, greengrocers 47, butchers 30.
- **Closed premises**: MHLW keeps a closed row for the last month only
  (許可(廃業) 3, all restaurants; 届出(廃業) 3), dated 2026-08-20 and 08-31.
  **Repeats**: 12 extra rows in 12 (address, trade name, type) groups among
  open addressed rows; one pin per premises (trap 7) takes them.
- ⚠️ **The map and the measure differ on the 8 condition-only rows**: step 2
  reads 業態, not 許可条件, so the 4 屋台 rows go to Food service by Fukuoka's
  yatai rule (fixed street stalls, which count), 露天営業 (天, not 店: the
  temporary words miss it) and the addressed 自動車 row go to Food service as
  restaurants. **Proposed shared code** (each with the Minato control): read
  a 許可条件 of `自動車(` as a vehicle (1 addressed row here), and add 露天 to
  the temporary words (1 row). The 屋台 rows stay on Fukuoka's rule; no owner
  question.

### ⚠️ Economic Census control: 0.96, a coverage reading

`scripts/japan_census_control.py` at build (Kure is wardless, so one
citywide figure). The 2021 census counts **848** 飲食店 establishments in
34202; the **810** distinct placed Food-service premises measured are **0.96
per establishment** (808 and 0.95 with call 172), against **1.32 in Yao, 1.16
in Takatsuki and 1.56-1.92 in the built cities** (Kurume 1.37). This is not a
join failure (every storefront is placed) and not a thin file:

- **Per in-force permit, Kure's file places as much as its neighbours**:
  808 placed Food-service premises over e-Stat's 1,752 is **0.46**, between
  Yao's 0.48 (1,202 / 2,499) and Takatsuki's 0.41 (1,116 / 2,747).
- **What is low is Kure's permits per establishment**: e-Stat's 1,752
  in-force restaurant permits over the census's 848 is **2.07**, the lowest
  of the cities read (Hiroshima 2.31, Tottori 2.38, Fukuyama 2.48, Sasebo
  2.51, Mito 2.63, Shimonoseki 2.65, Matsumoto 2.67, Yao 2.75, Okayama 2.79,
  Takatsuki 2.85, Matsuyama 2.91, Kurume 3.17, Kurashiki 3.31). Fewer
  restaurant permits stand behind each establishment, so any file holding 88%
  of permits and about seven fixed addresses in ten lands below one placed
  premises per establishment.
- **So the reading is coverage, stated as such**: the map holds about 58% of
  the in-force count (the stated share), the old law's 209 permits are
  missing, and about three fixed restaurants in ten withhold their address;
  the census figure adds no defect beyond those, and the page claims no more.

**What the build must re-measure**: the control on the built
`businesses_clean.csv` (add `kure` to the script's run, never to its default
list without a landing), after the shared-code changes above, expecting about
0.95; the in-force-per-establishment ratio (2.07) printed beside it, so the
figure is read with its reason; and, if the built figure falls under 0.9 or
the in-force share moves by more than a point, the brief and the page's share
sentence go back to staging before review time.

### Personal services: none published

The city's 理容所・美容所に関すること page (`/soshiki/62/ribiyou.html`,
updated 2023-12-13) carries procedures and forms (PDFs), no list; the probe
enumerated the 生活衛生課 pages (laundry included) and found none; nothing on
the open-data page (above). **A
food-only page**, Kurume's and Hiroshima's precedent: "**This map shows food
businesses only.**"

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/34202-24.0a.zip` (201,697 B,
**9,289 block keys**), town-chōme `.../19.0b/34202-19.0b.zip` (13,410 B,
**534**). `japan.CITIES` entry at build: `"kure": {"name": "呉市", "pref":
"34", "epsg": 32653, "n02": "25", "rules": WAVE2_RULES, "wardless": True,
"wards": ["34202"]}`.

| Tier (storefronts, `WAVE2_RULES`, call 172 applied) | All (1,768) | Food service (808) | Retail permits (448) | Notifications (512) |
|---|---|---|---|---|
| Block | **88.1%** (1,557) | 89.7% | 87.3% | 86.1% |
| Town-chōme / 大字 | 11.7% (207) | 10.1% | 12.5% | 13.5% |
| Unplaced | 0.2% (4) | 0.1% | 0.2% | 0.4% |
| **Block, chōme or MHLW's own point** (`OWN_POINT_FALLBACK`) | **100%** | | | |

- **Tiers disclosed (call 145)**: the page's coordinates bullet says that
  about one premises in nine (11.7%) sits at its town's centroid, Kakogawa's and
  Tsu's way; nothing is dropped for it.
- **Independent check**: MHLW's own coordinates against the block point,
  **median 34 m, 96.1% within 250 m** (1,557 rows; 18 over 1 km).
- **The misses, read** (towns only): **170 of the 207 chōme-tier rows are on
  the islands** (倉橋町 51, 蒲刈町大浦 22, 豊町大長 18, 豊浜町豊島 17, 豊町御手洗 16,
  下蒲刈町下島 12 …; 241 storefronts on 倉橋, 蒲刈, 下蒲刈, 豊, 豊浜 and 音戸),
  where addresses are lot numbers (地番) MLIT's block file keys only in part;
  the town centroid is the honest point. Mainland: 中央3丁目 8, 苗代町 2, 郷原町 2
  …. **Unplaced (4)**: 郷原町笹原, 郷原町一ノ松光山 and 川尻町川尻野呂山 (hill 字
  MLIT does not key), each with MHLW's own point; and **one notification
  whose address reads `未選択`** (a form's unselected default), whose MHLW
  point is the city-hall geocode (9 m from 呉市役所, shared by 14 rows).
- ⚠️ **Proposed shared code**: read an address of `未選択` as no address (call
  162's spirit: it names no premises), so the row is not pinned at city hall
  (1 Retail notification). With the Minato control.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_34_GML.zip`, N03 code
34202 (**352.2 km²**, extent W 132.446, S 34.028, E 132.869, N 34.333; the
islands of 倉橋, 蒲刈, 豊 and 豊浜 to the south and east carry no rail).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 呉線 (西日本旅客鉄道, 11) | JR Kure Line (呉線) | **13 / 28** | 呉ポートピア, 天応, かるが浜, 吉浦, 川原石, 呉, 安芸阿賀, 新広, 広, 仁方, 安芸川尻, 安登, 安浦 |

- **13 station records, 13 `N02_005g` groups**, one contiguous stretch along
  the coast. No name in two groups; no two groups closer than 600 m. **Median
  nearest-group gap 1,442 m** (1,170, かるが浜 to 吉浦, to 3,845, 安浦): standard
  rings by the spacing rule. Station extent W 132.513, S 34.222, E 132.744, N
  34.292.
- **Cut at the line** (named by N03 municipality at build): 15 beyond (竹原市
  5, 三原市 3, 坂町 3, 東広島市 2, 広島市 1, 海田町 1), the line running on to
  海田市 (for Hiroshima) and 三原. No station of another line within 500 m
  outside the city line. The distances to the city line printed by the
  scratch script (50 to 1,478 m) are mostly to the coast, which N03 draws as
  the line.
- **The stub test passes**: JR keeps 13 of 28; no urban line, so the
  one-station rules (54, 92, 163, 165, 167) do not arise.
- **The light-rail/rail test**: a railway (N02 class 11). No tram, light rail
  or subway; no Shinkansen inside.
- **Frequency, READ 2026-10-06** (JR West's own station timetables,
  `timetable.jr-odekake.net/station-timetable/<id>?date=20261007`, a
  Wednesday; ids from the `mydia_sp.cgi` index, 呉 `EID=0801515`, 安浦
  `0801509`; counts only, never a timetable on the page):

  | Station (direction; id) | All day | 10:00-15:59 |
  |---|---|---|
  | 呉 (to 広島 / to 三原; `3951049001` / `002`) | 57 / 48 | **3.3 / 2 an hour** (快速安芸路ライナー every 30 minutes, locals to 広島) |
  | 吉浦 (to 広島; `3953049001`) | 53 | **3.3** |
  | 呉ポートピア (to 広島 / to 呉; `3958049001` / `002`) | 40 / 34 | **1.3** (locals) |
  | 天応, 川原石 (to 広島; `3954…`, `3952…`) | 40, 40 | **1.3** |
  | 安芸阿賀 (to 広島; `3950049001`) | 48 | **2** (the liner) |
  | 新広 (to 三原; `3962049002`) | 48 | **2** |
  | 広 (to 広島 / to 三原; `3949049001` / `002`) | 48 / 25 | **2 / 1** |
  | 仁方, 安芸川尻 (to 広島; `3948…`, `3947…`) | 27, 27 | **1** |
  | 安浦 (to 広島 / to 三原; `3945049001` / `002`) | 27 / 20 | **1 / 1** |

  **Not read**: 安登 (between 安芸川尻 and 安浦, the same service) and かるが浜
  (between 呉ポートピア and 吉浦). **No stretch is at or under about 11 trains
  a day** (call 86): the fewest read is 20 (安浦 toward 三原). East of 広 the
  line runs about hourly, where the liner and many locals turn.
- **The master list's row says "JR Kure Line 34-57 a day"**: the read gives
  **20 to 57** (the probe read 呉, 呉ポートピア and 新広 only). A correction for
  staging, not an owner question.
- ⚠️ **Gate 3** at build: JR West's station count inside the city (13).
  **OSM `name:en`** for 13 groups (one Overpass query at build; not queried
  here).

## Scope

**Kure City (34202).** The Kure Line runs on to 海田市 and Hiroshima in the
west and to 竹原 and 三原 in the east; cut at the line. The islands are inside
the city and their premises are on the map; they have no station.

## Licences — MHLW as recorded

- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as recorded in
  `docs/data_sources/japan.md` (read 2026-10-02 for Okayama and Kurume; no new
  read). **MUST DISPLAY**:
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; link the top page only. **MUST NOT**: present it as
  MHLW's own; MHLW's logo; claim completeness or accuracy.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census: measurement
  sources. **JR West's timetables**: counts only.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- MHLW's file carries **法人名, 法人番号, 法人住所 and 営業施設電話番号**: never
  selected into an output; the measurement dropped address and phone columns
  from every print and read 法人名 IN MEMORY for the name rule only (in
  `OPERATOR_COLS` since 2026-10-05).
- **The name rule, version 2, measured in memory** (answers only, never a
  value): 法人名 filled on **907 of 1,768** storefront rows, a company marker
  on 781, **none on 126**; **0** rows whose trade name is the operator's own
  name, **0** bare personal names.
- 許可条件 is a condition, not a person: the measurement printed it only with
  digits and everything after a 市, 町, 区, 丁目 or 番 masked.
- Run `check_personal_exposure.py kure` (`japan=True`) after step 2; it must
  print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Chūgoku after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 132.446-132.869 E, centroid 132.630:
project to **UTM 53N (EPSG:32653)** (zone 53 begins at 132 E; the whole city
lies inside it). OSM box from the N03 extent, rounded out: (34.02, 132.44,
34.34, 132.87).

**Scaffold**: `scaffold_city.py --slug kure --name Kure --system-name "JR
West" --taxonomy japan_eigyo --lat 34.257 --lon 132.629 --region "Japan West"
--country Japan --mode metro --page-number <N>` (`--dry-run` first; the point
is the centre of the station extent, not the N03 centroid out among the
islands), the number claimed in `docs/session_roles.md` at build.

## Owner calls

**Made (do not re-ask):** the downloads (call 141); the standing Japanese
calls; `mode: metro`; the minor tier, Japan West now and Chūgoku after the
retag; no frequency floor (call 46); MHLW's notifications as partial Retail
(call 127b); MHLW's own point where the join misses (call 127c); the tiers
disclosed (call 145); the food share stated in Ichinomiya's sentence shape
(call 125); the shared-code rules (158, 161, 162, 172).

**Answered by the owner on 2026-10-06:** call 185, **"185 yes, B with share
stated"**: Kure goes from C to **Band B, food only, with the food share
stated**, on call 139's bar ("About 70% or more gives B (food only); less
gives a coverage discard"). Kure measured 69.4% of fixed premises with a real
address (1,025 of 1,477), which the owner accepted as about 70%. Not
re-opened: call 172's three late starters move it to 69.3% (1,022 of 1,474),
the same reading.

**Open:** none for the owner. Three shared-code proposals go to the build
(自動車 in 許可条件 as a vehicle; 露天 among the temporary words; `未選択` as no
address), each with the Minato control. The page's share sentence is a
page-text proposal for review time (below).

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control,
  `screen_japan_join.py minato`, and every city screen): call 172's late
  starters (3 restaurants here), 自動車 in 許可条件, 露天, `未選択`.
- `config.source_rows`: MHLW's file alone; `as_of` pinned to **2026-08-31**,
  never today. Expect about 808 Food-service and 960 Retail storefronts.
- **The stated food share** (call 125, Ichinomiya's sentence shape; drafted in
  the drafts file at build, flagged at review time): *proposed* "MHLW's file
  places about three restaurants in five of the official count: it holds
  permits granted since June 2021, leaves out vehicles and stalls, and about
  three fixed restaurants in ten do not publish their address." (58.3% of the
  in-force count; 30.7% of fixed premises withhold.)
- **The tiers** as built (the coordinates bullet, call 145).
- The Economic Census control (above: about 0.95, with the 2.07 reason); the
  factory share; gate 3; OSM `name:en`; the Kure Line's colour on both
  basemaps; **the opening view** (`map-view`: the islands stretch the N03
  extent south and east, so read the fit against the station line);
  `check_provenance.py`; `check_scope_disclosure.py`.
- The page's businesses bullet and What Is Excluded: food only, no personal
  services list, old-law permits and withheld addresses missing.
- **Corrections for staging** (not owner questions): the master list's row
  reads 1,546 open (88.2%), 1,025 of 1,477 and "34-57 a day"; after call 172
  and the timetable read, 1,543 (88.1%), 1,022 of 1,474 (69.3%) and 20-57.
  The drafts file's Tama entry calls Kure's share 58.5%; it is 58.3% with
  call 172 (Fuchū's 57.6% is then 0.7 points under, not 0.9).

```brief-checks
[
  {
    "id": "kure-mhlw-live",
    "claim": "MHLW's open-data file for Kure (34202) answers a plain keyless GET (1,149,444 B on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=34202_food_business_all.csv",
    "min_bytes": 1000000
  },
  {
    "id": "kure-isj-block-live",
    "claim": "MLIT's block-level address file for Kure (34202) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/34202-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "kure-isj-chome-live",
    "claim": "MLIT's town-chome file for Kure (34202) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/34202-19.0b.zip",
    "min_bytes": 10000
  },
  {
    "id": "kure-open-data-points-to-platform",
    "claim": "Kure's open-data page points to the city's expolis platform and offers no CSV of its own",
    "kind": "http_contains",
    "url": "https://www.city.kure.lg.jp/soshiki/36/opendata-index.html",
    "present": ["expolis.cloud/guides/opendata/t/kure"],
    "absent": [".csv", ".xlsx"]
  },
  {
    "id": "kure-barber-beauty-forms-only",
    "claim": "Kure's barber and beauty page carries procedure PDFs (63150.pdf among them) and no CSV or workbook list",
    "kind": "http_contains",
    "url": "https://www.city.kure.lg.jp/soshiki/62/ribiyou.html",
    "present": ["63150.pdf"],
    "absent": [".csv", ".xlsx"]
  },
  {
    "id": "kure-jr-kure-timetable",
    "claim": "JR West's timetable index for 呉 (EID 0801515) links the Kure Line's two weekday pages (3951049001, 3951049002) - a frequency source; ASCII anchors",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/cgi-bin/mydia_sp.cgi?MD=3&FN=0&EID=0801515",
    "present": ["3951049001", "3951049002"]
  },
  {
    "id": "kure-jr-yasuura-timetable",
    "claim": "JR West's timetable index for 安浦 (EID 0801509), the thinnest stretch read (20 a day toward 三原), links its two pages (3945049001, 3945049002)",
    "kind": "http_contains",
    "url": "https://timetable.jr-odekake.net/cgi-bin/mydia_sp.cgi?MD=3&FN=0&EID=0801509",
    "present": ["3945049001", "3945049002"]
  },
  {
    "id": "kure-projected-crs",
    "claim": "Kure projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 132.630,
    "expect": "EPSG:32653"
  }
]
```
