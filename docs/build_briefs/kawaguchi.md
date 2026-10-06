# Kawaguchi — build brief

**Band B, food only, owner-approved 2026-10-06** (Japan wave 4, banded in
staging's wave 5: `docs/decisions_drafts/staging.md`, "Wave 5, second half:
calls 95 to 141", call 104), **Hiroshima's shape** (food service plus a food
retail bucket, no personal services). Kawaguchi City (川口市, 11203, a core
city since 2018) runs its own health centre (川口市保健所), so e-Stat counts it
on its own row. **Personal services: the city's barber, beauty and laundry
lists are PDFs under the site's terms, which need the department's
permission: noted, not requested** (owner, call 104; outreach the last
resort).

The Step 0 downloads were approved by the owner 2026-10-06 (calls 104, 147).
**Step 0 measured 2026-10-06** (staging). Into `data/kawaguchi/raw/`
(gitignored), each from its publisher's own host with the project
user-agent, each HTTP 200, under each URL's own file name as
`japan_fetch.get` saves:

- From `www.city.kawaguchi.lg.jp` (保健所食品衛生課, listed on the city's
  open-data page): `food-business-license-notification.csv` (2,095,941 B,
  Last-Modified 2026-08-19).
- From `i2fas.mhlw.go.jp`: `11203_food_business_all.csv` (546,130 B), a
  control only.
- From `nlftp.mlit.go.jp`: `isj/11203-24.0a.zip` (280,300 B) and
  `isj/11203-19.0b.zip` (8,880 B).

**2,931,251 B in all.** Nothing else was downloaded. JR East's and Saitama
Railway's timetable pages were read for counts only (Rail).

**Run `python scripts/brief_check.py kawaguchi` before writing any code.**
Then the `japan-city` skill, **Hiroshima's shape** for the buckets and
**Ichinomiya's merge** (call 126: the full list kept whole plus the monthly
new premises) for the one CSV. Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py` from scratch scripts
only (`scripts/screen_japan_join.py` was not edited). Rail: MLIT N02-25 cut
at the N03 city line, through `pipeline/countries/japan.py` with a scratch
`CITIES` entry. The `cjk-text` skill for the source's private-use glyphs
(below).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none stops in Kawaguchi); (2) **lines served only by limited
expresses DO count** (2026-09-28); (3) **the city line only**: only stations
inside the city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27); an URBAN line cut to ONE
station is left out, its station kept through the other lines, and drawn cut
only where no other line serves that station (owner, 2026-10-06, calls 54
and 92); (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**,
version 2 (2026-10-06): a bare personal name is withheld whatever the
operator column holds; (6) **no page says "currently operating"**. Also: no
frequency floor for JR or private lines in Japan (owner, 2026-10-06, call
46), any stretch at about 11 trains a day or fewer named and drawn (call
86); fault-based cost clauses accepted for all of Japan (2026-09-24);
food-retail notifications count where a list publishes them, disclosed (the
`japan_eigyo` docstring, Tokyo's rule); English station names from OSM
`name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The precedents set 2026-10-06, applied here (do not re-ask):** the full
list kept whole plus its monthly files (call 126, Ichinomiya); MHLW's
permits missing from the source left out (126-127); MHLW's notifications
as a partial layer (127b) **do not apply**: the city's list carries its own
notifications; low-frequency stretches drawn and named (86: none); the
one-station rules (54, 92: the Musashino Line's 東川口, a JR stub kept as
cut). A stated food share (125) is not needed: the list holds about all of
the official count; what the page states is the address the city withholds
(Hiroshima's precedent, below).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Kawaguchi carries `label_tier: "minor"` and goes in the **Japan East** view
with the other Kantō cities (wave 4's first city to land retags Japan into
the eight regions, Kawaguchi into **Kanto**). Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 and Sōka's and
Kurume's precedent: the backbone is Saitama Railway's subway-type line (6 of
the 8 station groups, through-running with Tokyo Metro's Namboku Line); JR
holds 2 groups plus a one-station stub; no tram or light rail.

---

## The one-line summary

**Food from the city's own open-data CSV (CC BY as the page states it; the
licence read is pending, staging records it): the full list of 2026-03-31
plus the new premises of April, May and July 2026, 8,364 rows.** The March
list holds **4,281 restaurants (飲食店営業), 100.5% of e-Stat's 4,259 in
force** a year earlier, old-law permits included (not Kurashiki's trap).
**⚠️ June 2026 is missing from the CSV** (open call 1). **⚠️ The city
withholds the premises address on 1,316 rows (15.7%; 495 restaurants, 11.1%
of them)**, written as asterisks: not placeable, disclosed as Hiroshima's
14%. Through `japan_eigyo`, placed: **Food service 3,386, Retail 1,897**
pins. Block join **98.6%** with three private-use glyphs mapped (96.5%
without), 0.4% unplaced. MHLW's file holds about 5% of the city's permits: a
control. **Rail: 8 station groups**, read from the operators' own
timetables: Saitama Railway's Saitama Stadium Line 6 (every 12 minutes
midday), JR Keihin-Tōhoku 2 (10 to 12 an hour), JR Musashino 1 (東川口, a
stub kept as cut, every 10 minutes).

---

## Business leg — the city's open-data CSV

Host `https://www.city.kawaguchi.lg.jp` (the city's own CMS; no catalogue
API). The open-data page `/shiseijoho/ict_johoka/2/12182.html` (更新日
2026-08-20) lists 「食品等営業許可・届出一覧（R8年3月末データ～R8年7月新規施設）」, csv,
2026-08-20, 所管課 食品衛生課, and says the data is also on the prefecture's
open-data portal.

| File | Bytes | Rows | What it is |
|---|---|---|---|
| `/material/files/group/1/food-business-license-notification.csv` | **2,095,941** | **8,364** | the 食品衛生課 workbooks stacked into one CSV: the full list of permits and notifications on 2026-03-31, plus three monthly new-premises files |

- **UTF-8 with BOM, CRLF, 15 columns**: `Source.Name` (the workbook each row
  came from), **許可番号**, **業種**, **種目**, **屋号**, **営業所所在地**,
  営業所電話番号, **申請者名**, 代表者名（法人）, 申請者住所, 申請者電話番号,
  初回許可（届出）年月日, 最新許可年月日, 開始年月日, 終了年月日. Dates are
  `YYYY/M/D` (all read). **Drop at read**: both phone columns, 申請者住所 (the
  operator's own address) and 代表者名（法人） (a company representative,
  a person).
- **`Source.Name`, the editions inside the CSV**: `R0803全施設一覧 .xls` 8,034
  rows (a space before `.xls`), `R0804新規施設一覧（許可＆届出）.xls` 112,
  `R0805…` 104, `R0807…` 114. **No `R0806`**: June's new premises are not
  in the CSV, although its title says "to July" (open call 1). The months
  hold new premises only: every monthly row's first permit or notification
  is in 2026, and 最新許可年月日 runs April, May and July only (0 rows in
  June).
- **The section page carries the workbooks themselves**
  (`/soshiki/01090/027/shokuhin/oshirasetop/shisetsuichiran/index.html`,
  更新日 2026-09-29): `R0803zenshisetsuichiran.xls` (2.4 MB) and the months
  `R0804` to **`R0808`**`shinkishisetsuichiran.xls`, June and August
  included. That page names no licence; the site's terms reserve reuse
  (「…無断で転載することはできません」, permission from each page's department),
  so they sit with the personal-services PDFs (call 104's class). **Not
  downloaded.**
- **Against the shared tuples**: 営業所所在地 is in `ADDR_COLS`, 屋号 in
  `NAME_COLS`, 業種 in `TYPE_COLS`, 種目 in `FORM_COLS` (read under
  `form_cols`), 申請者名 in `OPERATOR_COLS`. No new column name is needed.
- **Types (業種)**, all 8,364 rows: 飲食店営業 4,479, その他の食料・飲料販売業
  1,080, 菓子製造業 368, コップ式自動販売機 277, コンビニエンスストア 257,
  集団給食施設 248, 乳類販売業 230, 百貨店、総合スーパー 165, 自動販売機による
  販売業 153, 食肉販売業 150, 魚介類販売業 120, 食肉販売業（包装済み…）107,
  野菜果物販売業 90, そうざい製造業 87, … 51 types. **種目** is filled on 542
  rows: 飲食店営業 自動車 345 (two spellings, one after NFKC), 給食・配食サービス
  172; 喫茶店営業 自動販売機 25.
- **Permits and notifications in one list**: 5,393 rows carry 開始 and 終了
  dates (permits), 2,971 carry neither (notifications: その他の食料・飲料販売業,
  konbini, supermarkets, dairy, packaged meat and fish, vending, institutional
  catering, …).

### The address the city withholds

- **1,316 rows (15.7%)** have 営業所所在地 written as **11 to 15 asterisks
  and nothing else**: 1,233 in the March list, 83 in the months. By type:
  restaurants 495, その他の食料・飲料販売業 310, vending 234, institutional
  catering 45, 菓子 41, … **1,283 of them have no company or cooperative
  marker on 申請者名** (33 do), and **106 of the 121 rows whose trade name
  equals an individual operator's name** are among them: the city withholds
  a sole trader's address. Without a rule they parse as a town of asterisks
  and fall to "unplaced".
- **Not placeable, disclosed** (Hiroshima's precedent, about 14% there):
  **495 restaurants of 4,479, 11.1%** (431 would be Food service, 456
  Retail, 429 out of every bucket). The page states it; the sentence is a
  proposal at review time.
- Separately, **434 rows have no address at all**: 411 restaurants (345
  vehicles, 種目 自動車, every one without an address; 66 with no 種目) and
  23 行商: not a premises, as everywhere.

### Old-law coverage (Kurashiki's trap) — not this list's problem

- **Old-law permits are in the file.** In the March list, **1,030 permits
  (828 restaurants) began before 2021-06-01**, from 2019-12-06, each ending
  2026-04-30 to 2027-05-31; 喫茶店営業 (an old-law type) 32 rows.
- **The March list is every permit in term on 2026-03-31**: no 終了年月日
  before that date (2026: 633 … 2032: 456 across the CSV).
- **e-Stat 衛生行政報告例 FY2024** (`japan_official.estat()`), 埼玉県川口市,
  飲食店営業 in force 2025-03-31: **4,259** (old law 1,381, revised 2,878).
  The March list's **4,281 restaurants are 100.5%** of it, vehicles included
  on both sides, a year apart. All permits: 5,145 in the March list against
  e-Stat's 5,106 (100.8%). Retail types: 菓子 353 against 367 (143 + 224),
  食肉販売 136 against 129, 魚介類販売 110 against 104, そうざい 80 (+1 複合型)
  against 69 (+1).

### The merge, closures and duplicates

- **Ichinomiya's merge (call 126)**: the March list kept whole plus the
  months, `as_of` **2026-03-31**, one row per (address, trade name, type)
  with the latest end (rows with no address or a withheld one kept as they
  stand). **8,228 rows, 4,395 restaurants.** The months are new premises
  only; renewals are not published, so 233 March permits (182 restaurants)
  that end April to July 2026 stay, as Ichinomiya's did. Filtering them
  against 2026-07-31 would drop about 130 restaurants that most likely
  renewed.
- `rebuilt_register` takes one path per edition; here the editions are one
  CSV told apart by `Source.Name`. The build splits it in a `source_rows`
  (config) or reads it rows-first; propose the shared form at build.
- **許可番号 is not a key**: 7,581 distinct of 8,364. Eight numbers are
  placeholders shared by 437 notification rows (乳類販売業 191, コップ式 113,
  packaged meat 66, packaged fish 52, …). (許可番号, 業種) repeats only in
  those eight and once between the March list and April. One exact duplicate
  row.
- **Closures are not marked** (no status column, no closure list). The page
  keeps "may include closed premises".

### Counts through `japan_eigyo` (merged, fixed premises)

Of 8,228 merged rows: **1,316 address withheld**, **437 not a premises**
(blank address, 一円, 自動車), **6,475 fixed and addressed**:

- **Food service 3,388** (restaurant 3,381, café 7).
- **Retail 2,261**: other food and drink sales 755, 菓子 317, konbini 239,
  dairy 226, butcher 224, fishmonger 170, supermarket 152, deli 73,
  greengrocer 67, bento 38; **1,636 of them notifications** (no term), by
  the module's standing rule.
- **Out 826**: institutional catering 310 (108 by 種目 給食・配食サービス),
  vending 240 (25 by 種目), mail order 12, temporary 2, **no rule 262**
  (manufacturing types, and **米殻類販売業 28**, below).
- ⚠️ **The city spells rice sellers 米殻類販売業** (殻, husk, for 穀, grain):
  `japan_eigyo`'s `^米穀類販売` misses 28 fixed rows (32 in all). A shared
  rule proposal (below).

**Economic Census control** (`scripts/japan_census_control.py` at build):
the 2021 census counts **1,384** 飲食店 establishments in 11203
(`docs/coverage_sweep/japan_universe_mhlw.csv`). The 3,386 placed
Food-service premises are **2.45 per establishment**, ⚠️ **above the built
cities' 1.56-1.92**; with the 431 withheld ones, 2.76. Kawaguchi's official
count is itself **3.08 per establishment**, the highest of the four Saitama
health-centre cities (2.46 to 3.08, Ageo (Regional)'s brief), so the list
follows the official count; the census is what runs low here. Record the
figure and the reading.

### MHLW's file (11203), a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11203_food_business_all.csv`:
**546,130 B, 1,537 rows** (届出 1,259, 許可 273, 許可(廃業) 3, 届出(廃業) 2),
UTF-8 with BOM, the national schema; its types carry a circled-number prefix
(`⑬ その他の食料・飲料販売業`). **Cover 0.05**: 220 open restaurant permits
(182 addressed, 180 with a point) of 4,259; permits 2021-06-10 to
2026-09-01.

- **Against the city's list**: the digits of its 許可番号
  (`指令川保衛食第NNNNNNN号`) find **203 of the 220 restaurants** (253 of 273
  permits) in the CSV. Of the 20 open permits not found, **11 were granted
  in June 2026**, 3 in August, 1 in July, 5 earlier: the June gap seen from
  outside. Under 126-127 MHLW's extras are left out.
- **Its own coordinates against the block point**: median **39 m**, 83.8%
  within 100 m, 98.6% within 250 m, 2 over 1 km (222 rows). With 0.4%
  unplaced, an own-point fallback is not needed.
- MHLW adds nothing the map needs.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`; Hatogaya merged in 2011
and is filed under 11203). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11203-24.0a.zip` (35,680 keys),
town-chōme `.../19.0b/11203-19.0b.zip` (273 towns). `japan.CITIES` entry at
build: `"kawaguchi": {"name": "川口市", "pref": "11", "epsg": 32654, "n02":
"25", "rules": WAVE2_RULES, "wardless": True, "wards": ["11203"]}`.

**⚠️ Three private-use glyphs in the addresses** (the section page warns
「一部外字を使用しているため…」): **139 address rows** carry U+E4AA (59),
U+F892 (52) or U+F7FE (28), inside town names. Read from the towns they sit
in and confirmed by the join (each mapped row then finds MLIT's block):
**U+E4AA = 塚** (戸塚, 戸塚東, 飯塚, 芝塚原), **U+F892 = 蓮** (蓮沼, 本蓮),
**U+F7FE = 樋** (芝樋ノ爪). A city-local translate table, Kyoto's
`KYOTO_GAIJI` precedent (a config `source_rows`, or a shared table keyed by
city).

| Tier, fixed rows in a bucket (5,649) | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| **With the three glyphs mapped** | **98.55%** | 1.08% | **0.37%** (21) |
| … Food service (3,388) / Retail (2,261) | 99.06% / 97.79% | 0.91 / 1.33 | 0.03 / 0.88 |
| Today's shared code, unmapped | 96.49% | 1.06% | 2.44% (138) |

**The misses, read** (towns and block numbers only): 12 rows addressed
outside the city (さいたま市 7, Tokyo's 台東区 and 荒川区, 狛江市, 越谷市; an
operator's office on a mail-order or vending-style filing, read at build); 8
area descriptions (`周辺` 6, `川口市全域` 2: not a premises, which the
`citywide` rule does not catch); 赤山 and 神戸東 地番 and one 戸塚 number MLIT
lacks. Town-tier rows sit in 芝, 安行領根岸, 戸塚南, 西新井宿, 安行 (大字 and
地番 areas).

**One pin per premises and bucket**: **5,283 pins** (Food service 3,386,
Retail 1,897) from 5,628 placed rows.

**Trade names**: 4 rows carry a private-use glyph in 屋号 (U+E4AA once,
U+E218, U+F223, U+E315 once each): they render as an empty box. The build
maps U+E4AA and reads the other three under `cjk-text` before publishing.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_11_GML.zip`, N03 code
11203 (**61.9 km²**, extent W 139.675, S 35.780, E 139.788, N 35.887). Read
with `stub_test()` and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 埼玉高速鉄道線 (埼玉高速鉄道, 12) | **Saitama Stadium Line** (埼玉スタジアム線, the operator's own name on its timetable pages) | **6 / 8** | 川口元郷, 南鳩ヶ谷, 鳩ヶ谷, 新井宿, 戸塚安行, 東川口 |
| 東北線 (JR East, 11) | **Keihin-Tōhoku Line** (JR East's 京浜東北線・根岸線) | **2 / 155** | 川口, 西川口 |
| 武蔵野線 (JR East, 11) | **Musashino Line** | **1 / 27** | 東川口 |

- **9 station records, 8 N02_005g groups**: 東川口 is one group for Saitama
  Railway and JR (165 m apart). No name in two groups; none under 600 m
  apart. **Median nearest-station gap 1,633 m** (1,144 to 2,070): rings by
  the spacing rule at build.
- **Cut at the line**: the Saitama Stadium Line runs on to 赤羽岩淵 (北区,
  Tokyo; through to the Namboku Line) and 浦和美園 (さいたま市); the
  Keihin-Tōhoku to 赤羽 and 蕨; the Musashino to 東浦和 (さいたま市) and 南越谷
  (越谷市). The Utsunomiya, Takasaki and Shōnan-Shinjuku trains share the
  Tōhoku tracks through Kawaguchi without stopping (川口 and 西川口 are
  Keihin-Tōhoku stations only).
- **The Musashino Line is a JR one-station stub (東川口), kept as cut**
  (standing call 3; 東川口 is served by Saitama Railway too). Not an urban
  line, so calls 54 and 92 do not remove it.
- **The light-rail/rail test**: all heavy rail (N02 classes 11 and 12).
  No Shinkansen, tram, monorail or AGT inside the city.
- **Frequencies, READ from the operators' weekday timetables** (2026-10-06,
  JR East's counted one departure per train, marked trains included; the
  page check matched departures to minute entries on every page):

  | Line, station | Weekday departures per direction | Midday (10-15h) |
  |---|---|---|
  | Keihin-Tōhoku, 川口 (`list0523`) | 250 south (快速 61 of them), 250 north | 10-12 an hour |
  | Keihin-Tōhoku, 西川口 (`list1153`) | 250 south, 250 north | 11-12 an hour |
  | Musashino, 東川口 (`list1277`) | 133 east, 133 west | 6 an hour |
  | Saitama Stadium Line, 鳩ヶ谷 (operator's timetable, revised 2026-03-14) | 156 toward 赤羽岩淵 (急行 33) | 5 an hour, **every 12 minutes** |

  **No stretch at about 11 trains a day or fewer** (call 86). No floor
  applies (call 46).
- ⚠️ **Gate 3** at build: Saitama Railway's 6 stations inside (its own
  station list: 浦和美園, 東川口, 戸塚安行, 新井宿, 鳩ヶ谷, 南鳩ヶ谷, 川口元郷,
  赤羽岩淵), JR East's 3. **OSM `name:en`** for 8 groups (one Overpass query
  at build; not queried here). The English line label (Saitama Stadium Line
  or Saitama Rapid Railway Line) follows the operator's current name; read
  OSM's at build and keep the operator's if they differ.

## Scope

**Kawaguchi City** (Hatogaya included since 2011). Every line runs on into
Tokyo's 北区 or Saitama City: cut at the line.

## Licences — as stated; the read is pending

- **The city's food CSV**: the open-data page states
  「ライセンス情報 クリエイティブコモンズ「表示」（CC BY）です。」 with **no version
  number**, beside its own conditions (the city keeps ownership; no
  warranty; no liability for damage; no use that infringes human rights or
  threatens safety; data may change without notice; disputes in the court
  for the city's area). **The licence read is pending** (not among the reads
  in `docs/decisions_drafts/staging.md`); staging records it. No verdict
  here. The credit form follows the read.
- **The section page's workbooks and the personal-services PDFs**: the site
  terms (「このサイトについて」, 2024-04-02) reserve reproduction beyond
  private use and quotation, with permission from each page's department.
  Not used (call 104).
- **MHLW** (control only) PDL 1.0; **MLIT ISJ and N02** PDL 1.0; **MLIT N03**
  CC BY 4.0, picks stations, ⛔ never drawn; **e-Stat** and the census:
  measurement only; JR East's and Saitama Railway's timetables read for
  counts only. The notice number is claimed at build.

## Privacy

- **申請者名** is filled on all 8,364 rows: a company or cooperative marker on
  4,210, none on 4,154 (the shape of a sole trader's own name). Read IN
  MEMORY for the name rule only, never written. **Both phone columns,
  申請者住所 and 代表者名（法人） are dropped at read.**
- **The name rule, measured in memory** (answers only): 121 rows whose trade
  name equals an individual operator's name, **106 of them with the address
  withheld by the city** (never placed); 2 bare personal names (sign rule);
  **2 flagged among the 5,283 pins**, shown as their permit type.
- MHLW's 法人名 (917 filled, 844 with a company marker), 法人番号, 法人住所
  and phones never selected (control).
- Run `check_personal_exposure.py kawaguchi` (`japan=True`) after step 2: it
  must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `label_tier: "minor"`,
`"country": "Japan"`. The city runs 139.675-139.788 E, centroid 139.733:
project to **UTM 54N (EPSG:32654)**. OSM box from the N03 extent, rounded
out: (35.77, 139.67, 35.89, 139.79). Scaffold with
`scripts/scaffold_city.py ... --page-number <N>`, the number claimed at
build from `docs/session_roles.md`.

## Owner calls

**Made (do not re-ask):** the standing Japanese calls; Band B, food only,
the personal-services PDFs noted and not requested (call 104); the
downloads (147); the merge (126); MHLW's extras left out (126-127); the
Musashino stub kept as cut (standing call 3); `mode: metro`; the minor tier
and Japan East (Kanto); no frequency floor (46).

**Open, with a recommendation:**

1. **June 2026 is missing from the CSV** (its title says "to July"; MHLW
   holds 11 June permits the CSV lacks). (a) **Build on the CSV as
   published**, its date stated as "2026-03-31 with new premises to July
   2026", June's gap named on the page, and re-read the CSV at build (a
   later edition may add June and August); (b) ask the owner to approve the
   section page's `R0806` and `R0808` workbooks (67.5 KB and 56 KB), which
   sit under the site's reserved terms, as the personal-services PDFs do;
   (c) fill June from MHLW. *Recommend (a)*: June is about 65 restaurants
   (the other months add 60 to 69), about 1.5% of the list, and (b) is call
   104's licence class, while (c) breaks 126-127. Tradeoff: one month of new
   premises missing until the city republishes.

**For review time (page text, not owner calls):** the withheld-address
sentence ("the city withholds the address of about one restaurant in nine,
so they are not on the map"), Hiroshima's wording as the model; the June
sentence if (a).

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): (1) an address of asterisks only is **withheld by the
  publisher**, counted apart from vehicles and from unplaced rows, never
  parsed as a town (1,316 rows here); (2) **Kawaguchi's three private-use
  glyphs** mapped before the join (block 96.5% to 98.6%), Kyoto's
  `KYOTO_GAIJI` shape; (3) **`米殻類販売` beside `米穀類販売`** in
  `japan_eigyo`'s rice rule (28 fixed rows); (4) optionally `周辺` and
  `全域` addresses as not a premises (8 rows). Proposals only; this brief
  edited no pipeline code.
- The merge from one CSV split by `Source.Name` (`as_of` 2026-03-31); the
  CSV re-read at build, its editions recorded (a June or August edition
  means re-measuring).
- The census ratio (2.45) and its reading; the 12 out-of-city addresses;
  the 4 private-use trade names; gate 3; OSM `name:en`; the line label; line
  colour on both basemaps; the opening view (`map-view`); the factory share;
  `check_provenance.py`; `check_scope_disclosure.py` (food only: personal
  services named as not published openly).

```brief-checks
[
  {
    "id": "kawaguchi-opendata-page",
    "claim": "The city's open-data page lists the food CSV and states CC BY. ASCII anchors only: the host sends no charset",
    "kind": "http_contains",
    "url": "https://www.city.kawaguchi.lg.jp/shiseijoho/ict_johoka/2/12182.html",
    "present": ["food-business-license-notification.csv", "CC BY"]
  },
  {
    "id": "kawaguchi-food-csv-live",
    "claim": "The food CSV (about 2 MB) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://www.city.kawaguchi.lg.jp/material/files/group/1/food-business-license-notification.csv",
    "min_bytes": 1500000
  },
  {
    "id": "kawaguchi-food-csv-editions",
    "claim": "The CSV stacks the March 2026 full list and the April, May and July months, with no June edition. A failure means a new edition: re-measure",
    "kind": "http_contains",
    "url": "https://www.city.kawaguchi.lg.jp/material/files/group/1/food-business-license-notification.csv",
    "present": ["Source.Name", "R0803", "R0804", "R0805", "R0807"],
    "absent": ["R0806", "R0808"]
  },
  {
    "id": "kawaguchi-food-section-page",
    "claim": "The food section's page carries the workbooks themselves, June and August included (site terms; not used)",
    "kind": "http_contains",
    "url": "https://www.city.kawaguchi.lg.jp/soshiki/01090/027/shokuhin/oshirasetop/shisetsuichiran/index.html",
    "present": ["R0803zenshisetsuichiran.xls", "R0806shinkishisetsuichiran.xls", "R0808shinkishisetsuichiran.xls"]
  },
  {
    "id": "kawaguchi-env-pdfs",
    "claim": "The barber, beauty and laundry lists are PDFs only (as of 2026-03-31), under the site terms: personal services not published openly (call 104)",
    "kind": "http_contains",
    "url": "https://www.city.kawaguchi.lg.jp/soshiki/01090/seikatueiseika/kankyo/22639.html",
    "present": ["riyo2025.pdf", "biyo2025.pdf", "cleaningtoritugi2025.pdf"]
  },
  {
    "id": "kawaguchi-mhlw-live",
    "claim": "MHLW's open-data file for Kawaguchi City (11203) answers a plain keyless GET (a control)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11203_food_business_all.csv",
    "min_bytes": 400000
  },
  {
    "id": "kawaguchi-isj-block-live",
    "claim": "MLIT's block-level address file for Kawaguchi (11203) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11203-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "kawaguchi-isj-chome-live",
    "claim": "MLIT's town-chome file for Kawaguchi (11203) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/11203-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "kawaguchi-jr-kawaguchi-timetable",
    "claim": "JR East's timetable list for Kawaguchi station (0523) links its two weekday Keihin-Tohoku pages",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0523.html",
    "present": ["tt0523/0523010.html", "tt0523/0523020.html"]
  },
  {
    "id": "kawaguchi-jr-higashikawaguchi-timetable",
    "claim": "JR East's timetable list for Higashi-Kawaguchi (1277, Musashino Line) links its two weekday pages",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1277.html",
    "present": ["tt1277/1277010.html", "tt1277/1277020.html"]
  },
  {
    "id": "kawaguchi-sr-hatogaya-timetable",
    "claim": "Saitama Railway's own timetable page for Hatogaya (SR22) answers",
    "kind": "http_contains",
    "url": "https://s-rail.ekitan.com/norikae/timetable/station/289-3/d1?dw=0",
    "present": ["SR22"]
  },
  {
    "id": "kawaguchi-projected-crs",
    "claim": "Kawaguchi projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.73,
    "expect": "EPSG:32654"
  }
]
```
