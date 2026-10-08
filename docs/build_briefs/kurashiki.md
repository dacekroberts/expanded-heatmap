# Kurashiki — build brief

**Band B, food only, owner-approved 2026-10-08 (call 226)**: Kurashiki from C
to B on the city's year-end PDF of food permits in force, an upper bound
(Shizuoka's shape), the MLIT block join measured here, the name rule on
営業者氏名 (`docs/decisions_drafts/staging.md`, "Kurashiki's year-end food PDF
holds the old-law permits..." and "Cluj-Napoca rides with Kansai-2..."; calls
222 to 226). Build in **Regional-2**, last, on **page 306 and notice 216**
(`docs/session_roles.md`; `docs/build_plan_2026-10-07.md`). **Step 0
measured 2026-10-08** (a brief agent for staging).

**On disk before this brief** (`data/kurashiki/raw/`, gitignored, not
re-downloaded):

- `r07nenndinatu_2026-03-31.pdf`, **8,034,340 B**, 243 pages: the city's
  「令和７年度末」 list (call 224), from
  `https://www.city.kurashiki.okayama.jp/_res/projects/default_project/_page_/001/004/977/r07nenndinatu.pdf`
  on page 1004977
  (`https://www.city.kurashiki.okayama.jp/business/health-safety/1004966/1004974/1004977.html`).
- `332020_food_business_all2026_standard.csv`, **791,423 B**, 3,172 rows: the
  catalogue's 2026-03 CSV (`https://kurashiki.dataeye.jp/resource_download/17772`,
  dataset 1446; 2026-10-04).

**Downloaded for this brief** (2026-10-08, the project user-agent, each HTTP
200, from its publisher's own host; Okayama's cache holds only 33101-33104):

- From `nlftp.mlit.go.jp`: `isj/33202-24.0a.zip` (**518,442 B**) and
  `isj/33202-19.0b.zip` (**10,875 B**), into `data/kurashiki/raw/isj/`.
- From `i2fas.mhlw.go.jp`: `33202_food_business_all.csv` (**518,644 B**),
  measured only (open call 2).

**1,047,961 B downloaded in all.** Read, not downloaded as data: page 1004977;
the Mizushima Rinkai Railway's timetable page and the Ibara Railway's
timetable page with its up-direction image (`ibara_up.png`, 818,757 B, into
the scratch folder only). No Overpass, no BODIK.

**Run `python scripts/brief_check.py kurashiki` before writing any code.** Then
the `japan-city` skill (its foundation and wave 2 sections bind: ALL_RULES,
`TERM_AS_OF`, the line registry, `label_offset`, `TEXT_WIDTH`), with
`address-join` and `cjk-text`. The business leg is **Kōchi's and Kyoto's
`source_rows` shape**: a config reader that turns the PDF into rows (below),
never a hand-written PDF decoder. Coordinates were measured with
`pipeline/countries/japan_register.py`'s own functions from scratch scripts
(`scripts/screen_japan_join.py` was copied, not edited; it has no Kurashiki
entry). Rail: MLIT N02-25 and N03 through `pipeline/countries/japan.py` with
an in-memory `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; 新倉敷 stays as a JR Sanyo Line station); (2) **lines served only
by limited expresses DO count** (2026-09-28); (3) **the city line only**:
only stations inside the city get rings, JR and the private lines are cut at
the line, **a JR or private one-station stub stays as cut** (2026-09-27); an
URBAN line cut to ONE station is left out (calls 54, 92; none here); (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept; (5) **the name rule**, version 2 (2026-10-06), the name spread
city-wide (`name_city`, call 205); (6) **no page says "currently operating"**.
Also: no frequency floor for JR or private lines (call 46), any stretch at
about 11 trains a day or fewer drawn and named (call 86; none here); fault-based
cost clauses accepted for all of Japan; English station names from OSM
`name:en`; **市内一円 rows are not premises** (Kobe's trap 6); tiers disclosed
where the block share is low (call 145); a new city reads `ALL_RULES` (leave
`"rules"` out of its `japan.CITIES` entry). Barber and beauty lists stay out,
possible with outreach (call 225).

**✅ Region, tier, mode:** `"region": "Chugoku"` (Okayama Prefecture, as
Okayama and Fukuyama), `"country": "Japan"`, `"label_tier": "minor"`, a
`label_offset` and a measured `TEXT_WIDTH`. **`mode`: `metro`** (the owner's
rule of 2026-10-02, Shizuoka's and Kurume's reading): no subway or tram, and JR
is not the largest network inside the city (8 station groups against the
Mizushima Rinkai Railway's 10), so the mode follows the railways.

---

## The one-line summary

**Food only, from the city's own year-end PDF of the food permits in force at
2026-03-31: 6,288 rows parsed whole, 4,727 飲食店営業, 4,619 distinct restaurant
permits once 108 old-law rows that a new-law permit of the same number
replaces are dropped = 99.3% of e-Stat's 4,653 in force (FY2024).** Old-law
permits ARE in it (飲食店営業 867 granted before 2021-06-01, 759 after the
pairs). **At fixed premises 3,998 distinct restaurant permits (85.9% of the
in-force count), every one placed: block 88.3%, town-chōme 11.7%, unplaced
0.** The catalogue CSV adds nothing (every one of its 3,172 permit numbers is
in the PDF). **Rail: 21 N02 station groups** (Mizushima Rinkai 10, JR West 8,
Ibara 3), six lines drawn, none at 11 trains a day or fewer by the operators'
own timetables (the thinnest read: 水島–三菱自工前, 13 and 15 a day).

---

## Business leg — the city's year-end PDF

| | 令和7年度末 食品営業許可一覧 |
|---|---|
| **File** | `r07nenndinatu.pdf`, **8,034,340 B**, 243 pages (242 with rows); the page lists it as 「令和7年度末（PDF 7.7MB）」. Title on every page: 「令和８年３月３１日現在　食品営業許可一覧」 |
| As of / cadence | **2026-03-31.** The page: 「年度末」 is the list of premises holding a permit at each fiscal year-end, updated 15 April; the monthly files (令和8年4月 to 8月 so far) are **new permits only** (「各月に倉敷市内で新規に営業許可を取得した店舗」), updated the 15th of the next month. No closure list. Page updated 2026-09-15 |
| Columns (11) | 営業者氏名, 営業者法人電話番号, **営業所所在地**, **営業所名称**, 営業所電話番号, **業種**, **形態**, **許可年月日**, **有効期限**, **初回許可年月日**, **許可番号** |
| Footer note (every page) | 「営業所名称が空欄もしくは＊＊＊の場合は、名称がない施設である。」 a blank or ＊＊＊ trade name means a premises without a name: the pin shows its permit type (11 blank, 66 ＊＊＊) |

### Reading the PDF into rows (measured)

`pdftotext -table` (xpdf 4.06, the machine's `pdftotext`; no pypdf is
installed) puts **each record on one line**, 6,288 lines matching three dates
and a permit number at the end; the only other lines are each page's title,
header and footer (2 per page). **Every page's header gives the column
offsets, and on all 6,288 records the address column starts exactly at the
header's offset** (0 misaligned). The reader used here (scratch `parse.py`):

1. cut each line at its page header's offsets (営業者氏名, 営業者法人電話番号,
   営業所所在地, 営業所名称, 営業所電話番号, 許可年月日);
2. read the three dates (令和/平成/昭和, 元 for 1) and the permit number from
   the right by regex;
3. take the form (6 values) and the type (38 values, below) off the right
   of the trade-name cell by vocabulary, then a trailing phone number.

Checks on the result: no row without a type, no operator-phone cell that is
not a phone number, no name or address overflowing its column, no blank
address; 13 blank operator names. `pdftotext -layout` splits a row's dates
from its type (staging's mention count); `-raw` breaks some records over two
lines. ⚠️ **The build's reader is `pdftotext -table` with the page header's
offsets**, in the config's `source_rows`, and stops if a record line fails
the tail regex or a page has no header.

### Counts

| 業種 | Rows | Old law (granted before 2021-06-01) | New law |
|---|---|---|---|
| **飲食店営業** | **4,727** | 867 | 3,860 |
| 菓子製造業 | 600 | 122 | 478 |
| 魚介類販売業 | 203 | 60 | 143 |
| 食肉販売業 | 180 | 52 | 128 |
| 喫茶店営業 (old law only) | 102 | 102 | 0 |
| 調理の機能を有する自動販売機 | 87 | 0 | 87 |
| そうざい製造業 | 81 | 13 | 68 |
| 乳類販売業 (old law only) | 63 | 63 | 0 |
| 30 other types (manufacturing; 33 to 1 rows each) | 245 | 43 | 202 |
| **All** | **6,288** | **1,322** | **4,966** |

- **Against e-Stat** (衛生行政報告例 FY2024, `japan_official`, 岡山県倉敷市, in
  force 2025-03-31): 飲食店営業 **4,653 = old law 1,586 + revised 3,067**; all
  permit types 6,040 (2,061 + 3,979). The PDF a year later: 4,727 restaurant
  rows (101.6%), 6,288 rows (104.1%); the old-law share falls as expected
  (1,586 to 867) while the revised law's grows (3,067 to 3,860).
- **Old-law vs new-law** by 許可年月日: the old forms (形態) sit on old-law rows
  only: 飲食店営業 普通形態 793, 特殊形態 71, 自動販売形態 3 = all 867.
  Grants run 2020-02-04 to 2026-03-31; 1,324 rows have a 初回許可年月日 before
  2021-06.
- **Expired before 2026-03-31: none.** Expiries run 2026-03-31 (244 rows) to
  2032-03-31. No permit starts after the as-of. `TERM_AS_OF` = 2026-03-31
  (call 161 drops nothing; call 172 sets nothing aside).
- **Old-law and new-law rows under one permit number: 127 pairs** (254 rows),
  each one old-law row and one new-law row, never on the same page; 121 differ
  only in their dates, 6 in type (喫茶店 to 飲食店 3); **107 are the same
  premises** (address and trade name), and every old row's expiry is in 2026,
  after its new row's grant. A premises renewed under the 2021 law while its
  old permit's term ran on. Restaurants: **108 pairs**, so **4,619 distinct
  restaurant permits = 99.3% of 4,653**. ⚠️ The build drops the old row where
  a new-law row carries its number (open call 3).
- **Duplicates otherwise**: (address, trade name, type) groups of 2+ rows 218
  (270 extra rows, the pairs among them); one pin per premises (trap 7) takes
  them.
- **Not a premises: 667 rows written area-wide** (every one contains 一円, so
  `permits_from_rows` marks them mobile): 「倉敷市(県内一円)」 565, 「倉敷市内一円」
  86, 「岡山県下一円」 7, 9 in rarer spellings. By type 飲食店営業 614, 魚介類販売業
  20, 菓子製造業 19, 喫茶店営業 10. Old-law 飲食店営業 特殊形態: 63 of 71 are
  area-wide. 5 more rows are `areawide` by 周辺 / 全域. Every other address
  starts 倉敷市 (6,274) or 岡山県 (11).
- **Vending**: 調理の機能を有する自動販売機 (87, out by type) and the old form
  **自動販売形態** (91: 喫茶店営業 75, 乳類販売業 13, 飲食店営業 3), which
  `japan_eigyo`'s vending rule (`自動販売機|自販機`) does NOT read: as the
  shared code stands the 75 cup-vending 喫茶店 rows land in Food service.
- **No 業態 column**: the new-law rows (3,860 restaurants) carry no form at
  all, so hostess venues, hotel restaurants and caterers cannot be set aside
  by form here (open call 4).

### Through `japan_eigyo` (fixed rows, ALL_RULES, before the shared-code items)

5,616 fixed rows: restaurant 4,109 (Food service), café 92 (Food service; 75
of them cup vending, above), confectioner / bakery 581, fishmonger 182,
butcher 178, deli 85, dairy 61 (Retail), no rule 241 and vending 87 (out).
**Storefront rows 5,288: Food service 4,201, Retail 1,087.** With the area-wide
rows, the 127 superseded old rows, 特殊形態 and 自動販売形態 set aside:
**about 3,933 distinct Food-service premises and 886 Retail** by (address,
trade name).

### The catalogue CSV adds nothing

`332020_food_business_all2026_standard.csv` (3,172 rows; 申請区分 blank on
every row; 法人名, 緯度 / 経度, 業態 and 許可開始日 empty): **all 3,172 permit
numbers are in the PDF**, and by (number, type) 3,171 of 3,171 keys match with
the same 許可年月日. It holds 3,171 of the PDF's 4,966 new-law rows and no
old-law permit (87 old-law PDF rows share a number with it: the pairs above).
**The PDF alone is the source**; the CSV is not built (no notice).

### MHLW's file for 33202 (measured, not proposed for the build)

1,549 rows (届出 1,300, 許可 244, closed 5); **149 open restaurant permits**
(cover 0.03, the universe CSV's figure), 117 addressed. Of 247 numbered
permits 225 are in the PDF; **24 were granted after 2026-03-31 (14
restaurants), 9 of them renewals already in the PDF under their number**; 7
granted by 2026-03-31 are not in the PDF (none closed or expired). Its 1,300
notifications: 738 addressed; cup vending 312, other vending 161, institutional
catering 153 among them. Open call 2.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards**: block `isj/33202-24.0a.zip` (**62,007 block
keys**), town-chōme `isj/33202-19.0b.zip` (**381 keys**). Read with
`japan_register.permits_from_rows(rows, "岡山県", "倉敷市", wardless=True,
ALL_RULES, others)` and `join_city`, the columns mapped as 営業所所在地 /
営業所名称 / 業種 / 形態 / 有効期限. **The Minato control reproduces** (2026-10-08:
`screen_japan_join.py minato` 98.0 / 0.2 / 1.8). `japan.CITIES` entry at
build: `"kurashiki": {"name": "倉敷市", "pref": "33", "epsg": 32653, "n02":
"25", "wardless": True, "wards": ["33202"]}`.

| Tier | All fixed rows (5,616) | 飲食店営業 fixed (4,109) | old law (803) | new law (3,306) | Storefronts (5,288) | Food service (4,201) | Retail (1,087) |
|---|---|---|---|---|---|---|---|
| Block | **87.6%** | **88.6%** | 91.5% | 87.9% | 87.8% | 88.6% | 84.7% |
| Town-chōme / 大字 | 12.4% | 11.4% | 8.5% | 12.1% | 12.2% | 11.4% | 15.3% |
| Unplaced | **0** | **0** | 0 | 0 | 0 | 0 | 0 |

- **The 70% bar**: every fixed restaurant row carries a real address (the 614
  area-wide restaurant rows are vehicles and stalls, set aside), and all are
  placed. **Distinct fixed restaurant permits (pairs dropped, 特殊形態 7 and
  自動販売形態 3 at an address set aside): 3,998 = 85.9% of e-Stat's 4,653,
  block 88.3%, town-chōme 11.7%, unplaced 0.** Far above Kure's 69.4%.
- **Tiers disclosed (call 145)**: about one premises in nine sits at its
  town's centroid. The chōme tier is the 大字 with 地番 addresses (平田 20,
  新田 17, 松島 16, 玉島 16, 酒津 15, 中島 14, 中庄 14, 西阿知町西原 14, 連島町西の浦 13,
  笹沖 13, 茶屋町 13, 玉島乙島 13, 児島駅前2丁目 13 ...). 3 rows carry no block
  number.
- **Independent check**: MHLW's own coordinates against the block point on the
  permits both hold: **133 rows, median 67 m, 83.5% within 250 m, 4 over 1 km**
  (Kure's 34 m and 96.1%: a coarser 地番 block here; read the 4 at build).
- **No GSI sample** was run; the build runs `gsi_check` on 150 rows (1 request a
  second) if the owner wants a second method beyond MHLW's points.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_33_GML.zip`, code 33202
(**355.9 km²**, extent W 133.602, S 34.417, E 133.882, N 34.669; centroid
133.746 E). 25 station records inside (Shinkansen out: 新倉敷 on the Sanyo
Shinkansen), **21 `N02_005g` groups**; no name in two groups; multi-record
groups 倉敷 (Sanyo + Hakubi), 茶屋町 (Uno + Honshi-Bisan), 児島 (JR West + JR
Shikoku). **Median nearest-group gap 1,523 m** (147 to 5,453): standard rings.
Station extent W 133.662, S 34.463, E 133.826, N 34.632.

| N02 line (operator, class) | Public name (as other maps draw it) | Inside / N02 total | Stations inside |
|---|---|---|---|
| 水島本線 (水島臨海鉄道, 12) | Mizushima Rinkai Railway Mizushima Main Line (水島本線) | **10 / 10** | 倉敷市, 球場前, 西富井, 福井, 浦田, 弥生, 栄, 常盤, 水島, 三菱自工前 |
| 山陽線 (西日本旅客鉄道, 11) | JR Sanyo Line (registry `jr-west-sanyo-line`) | 5 / 131 (4 groups) | 西阿知, 新倉敷, 倉敷, 中庄 |
| 本四備讃線 (西日本旅客鉄道 + 四国旅客鉄道, 11) | JR Seto-Ohashi Line (Okayama's `JB`) | 4 / 5 and 1 / 2 | 茶屋町, 木見, 上の町, 児島 |
| 井原線 (井原鉄道, 12) | Ibara Railway Ibara Line (Fukuyama's `IB`) | 3 / 15 | 川辺宿, 吉備真備, 備中呉妹 |
| 伯備線 (西日本旅客鉄道, 11) | JR Hakubi Line | 1 / 28 | 倉敷 (stub as cut) |
| 宇野線 (西日本旅客鉄道, 11) | JR Uno Minato Line (Okayama's `JU`) | 1 / 15 | 茶屋町 (stub as cut) |

- **Six lines drawn.** The Hakubi and Uno Minato lines are JR one-station
  stubs, drawn as cut (standing call 3; Okayama keeps 本四備讃線's one station,
  植松, the same way). **JR Shikoku's 本四備讃線 (児島 only, then the bridge)
  and JR West's are one public line, the JR Seto-Ohashi Line**, one identity
  under the registry's two-operator rule (the JR Sanyo Line's precedent).
- **Line identity (the owner's hard line)**: the JR Sanyo Line takes its
  registry colour; **the Uno Minato, Seto-Ohashi and Ibara lines are drawn by
  Okayama or Fukuyama, so each gets a `pipeline/line_registry.py` entry in the
  build branch** (moving Kurashiki's own lines only); the Hakubi Line and the
  Mizushima line are new to the site. `check_line_identity.py` decides it.
- **Cut at the line** (named by N03 municipality at build): 宇野線 to 久々原
  (**68 m** beyond), 彦崎 and 早島; 本四備讃線 to 植松 (130 m); 伯備線 and 井原線 to
  清音 (556 m) and 総社; 山陽線 to 金光 and 庭瀬. Check that 久々原 and 植松 fall
  outside at build (Okayama's map rings 植松).
- **The light-rail / rail test**: all railways (N02 classes 11 and 12); no
  tram, light rail, subway or AGT; no urban line cut to a stub.
- **Frequency, read 2026-10-08 from the operators' own pages (counts only):**
  - **Mizushima Rinkai Railway**
    (`https://www.mizurin.co.jp/contents/time_table.html`, 「2026年3月14日改正」,
    every day): **32 trains each way 倉敷市–水島**, of which **15 up and 13
    down run on to 三菱自工前**; about every 30 to 50 minutes at midday (9:40,
    10:20, 11:02, 11:47 ... from 三菱自工前 / 水島). The 水島–三菱自工前 stretch
    is the thinnest on the map, above "about 11".
  - **Ibara Railway** (`https://www.ibara-railway.co.jp/info/timeline/`,
    「2026年3月14日改正」, the timetable published as images): the up image lists
    **33 trains (1300D to 364D), one of them weekdays only, every one bound
    for 清音 or 総社**, so through the three in-city stations, which lie
    between 矢掛 and 清音 (ASSERTED from the destination row; the image's
    station column is not printed).
  - **JR West: not read** (Sanyo, Seto-Ohashi and Hakubi locals through 倉敷 and
    茶屋町; ASSERTED well above 11 a day). Read 木見 and 上の町 (Seto-Ohashi
    locals only) from `timetable.jr-odekake.net` at build.
- ⚠️ **Gate 3** at build: the Mizushima Rinkai Railway's 10 passenger stations
  (its timetable header lists the same 10), the Ibara Railway's, JR West's.
  **OSM `name:en`** for 21 groups (one station query at build, the only
  Overpass call); the closest pair (147 m) read from step 1's list.

## Scope

**Kurashiki City (33202).** The Sanyo Line runs on to Okayama and Kasaoka,
the Hakubi and Ibara lines to Sōja, the Uno Minato Line toward Okayama and
Tamano, the Seto-Ohashi Line across the bridge to Kagawa: all cut at the city
line. Food only: the barber and beauty lists stay out (call 225), and no
laundry list exists.

## Licences — the PDF READ 2026-10-08: PERMITTED WITH CONDITIONS

**The licence-read verdict** (staging's drafts, "Kurashiki to B and to
Regional-2"): CC BY 4.0 governs the PDF. The page's mark covers its body
content, the attachment included, and the site copyright page (1008316)
carves marked content out of its reservation. **Display:** the source and a
processed-data statement, no prescribed wording; for example "Source: Kurashiki
City, food-business permits in force at March 31, 2026 (page URL), CC BY 4.0
(link). Processed by this project: geocoded, categorized and filtered." **Do:**
nothing; no indemnity or reimbursement clause. Personal information: silent,
so the name rule decides. The bullets below are the read's starting point.

- **The year-end PDF and page 1004977, as read 2026-10-08**: the page carries
  a CC BY 4.0 image link (`creativecommons.org/licenses/by/4.0/`) and says
  「このページ（ページヘッダ及びフッタ部分除く）に掲載されたコンテンツは、クリエイティブ・コモンズ表示4.0日本語ライセンスの
  CC BY 表示（作品のクレジットを表示すること）の下で提供します。」 and
  「掲載データは、営利目的での二次利用（改変）も可能です。…編集・加工等した場合、出典を明記し、編集・加工等した旨を記載して、公表してください。」
  **The licence-read verdict is recorded above; the notice (216) is built
  from it.**
- **The catalogue CSV**: PDL 1.0 as stated on dataset 1446 (2026-10-04); not
  built.
- **MHLW**: PDL 1.0 as recorded in `docs/data_sources/japan.md` (only if open
  call 2 is taken).
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census: measurement
  sources. The operators' timetables: counts only.

## Privacy

The PDF carries **営業者氏名** (the operator: a company, or a person's own
name), **営業者法人電話番号** and **営業所電話番号** (phones). The reader keeps
営業者氏名 IN MEMORY for the name rule (already in `OPERATOR_COLS`, Tokyo's and
Fukuoka's spelling) and never writes it or either phone. **No value was printed
or stored for this brief beyond pdftotext's own text file in the scratch
folder, deleted at the end**; every figure is a count.

- **営業者氏名, classified in memory (version 2)**: a company or cooperative
  marker on **3,266** rows (2 with a title word as well), **3,009 with no
  marker** (mostly individuals), 13 blank.
- **The name rule flags 6 rows** (trade name equal to the individual operator's
  own name), **0 bare personal names**; among storefronts **4** (Food service
  3, Retail 1); `name_city` spreads to no further row (6 keys, 6 rows). 5 more
  trade names add a business word to the operator's name (shown, by the rule).
- Pins with no name: 35 storefronts (blank or ＊＊＊) show their permit type.
- Run `check_personal_exposure.py kurashiki` (`japan=True`) right after step 3;
  it must print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

`"region": "Chugoku"`, `label_tier: "minor"`. Project to **UTM 53N
(EPSG:32653)**: the city spans 133.602-133.882 E, inside zone 53 (132-138 E),
Okayama's zone by computation, not copied. OSM box from the N03 extent,
rounded out: (34.41, 133.60, 34.67, 133.89). Kurashiki's dot sits about 15 km
west of Okayama's: `check_macro_labels.py` (PROBLEMS 0 at 375, 768, 1200) and
the Chugoku view on a phone (a parked call for Cleanup if it does not fit).

**Scaffold**: `scaffold_city.py --slug kurashiki --name Kurashiki
--system-name "Mizushima Rinkai Railway, JR West and Ibara Railway" --taxonomy
japan_eigyo --lat 34.548 --lon 133.744 --region Chugoku --country Japan --mode
metro --page-number 306` (`--dry-run` first; the point is the centre of the
station extent).

## Page text (`docs/city_page_format.md`, the template)

- **The lines**: "6 lines are drawn, each labeled on the map and in the
  legend: the Mizushima Rinkai Railway's Mizushima Main Line, JR West's Sanyo,
  Seto-Ohashi, Uno Minato and Hakubi lines, and the Ibara Railway's Ibara
  Line."; the MLIT/OSM bullet; "Only stations inside Kurashiki City get rings,
  ... lines running on to Okayama, Soja, Asakuchi, Tamano and Kagawa are cut at
  the city line. The stations left out are listed below." (the list checked
  against `excluded_stations.csv`; Asakuchi for 金光 to confirm); "The
  Shinkansen is not drawn (Shin-Kurashiki appears as a JR Sanyo Line
  station)."
- **The businesses**: "**This map shows food businesses only.**"; "From
  Kurashiki City's list of food-business permits (as of 2026-03-31)."; the
  no-general-licence bullet; the notification bullet; the closed-premises
  bullet (the list is the year-end register; closures since are not shown).
- **Reading the map**: the MLIT join bullet, with the tier (about one in nine
  at the town's center, call 145); the name-rule bullet; the Japanese-names
  bullet.

## Owner calls

**Made (do not re-ask):** Band B, food only, from the PDF (call 226); the
PDF download (call 224); barber and beauty lists out (call 225); the
standing Japanese calls; `metro`; Chugoku and the minor tier; page 306 and
notice 216; tiers disclosed (call 145); no frequency floor (calls 46, 86).

**Open:**

1. **The monthly new-permit PDFs (令和8年4月 to 8月, 0.5 to 1.0 MB each, more
   monthly).** *Recommend: build from the year-end list alone, `as_of`
   2026-03-31*, and refresh when the 令和8年度末 list lands (2027-04-15).
   Tradeoff: the map is six months older than it could be; a rebuild (Shizuoka's
   and Kyoto's shape) adds about five months of openings with closures still
   invisible, so it overstates, and its renewals would need the same-number
   rule below. Nothing was downloaded.
2. **MHLW's 33202 file as a second source** (Fukuoka's two-source shape: its
   notifications as a partial Food-shops layer, as Okayama's and Kure's pages
   carry). *Recommend: leave it out at this build.* It adds 14 restaurant
   permits granted after 2026-03-31 and 1,300 opt-in notifications (738
   addressed; vending and institutional catering among them), against a second
   notice, a `SUPERSEDES` rule and a layer whose completeness is unknown.
   Tradeoff: the Food-shops layer stays permits only (bakeries, confectioners,
   fishmongers, butchers, delis, dairies) with no convenience stores or
   supermarkets, unlike Okayama's page next door.
3. **The 127 old/new pairs and the stated share.** *Recommend: drop the old-law
   row where a new-law row carries its permit number* (step 2 already makes 107
   of them one pin), *and state no share sentence beyond the upper-bound
   bullets*: the list is the register itself (99.3% of permits in force, 85.9%
   at fixed addresses). Tradeoff: a renewed premises whose address or trade
   name was respelled (20 pairs) would otherwise show twice; dropping by number
   could hide a genuine second premises under a reused number (none seen: every
   pair is one old and one new row).
4. **No 業態 on new-law rows; the census reading.** *Recommend: accept, and
   record the ratio*: about **3,933 distinct Food-service premises over the 2021
   census's 1,405 飲食店 establishments = 2.80** (built cities 1.56-1.92), with
   **3.31 in-force restaurant permits per establishment** (Kure's brief: the
   highest of 14 cities read), so the excess is permits the census does not
   count as establishments, not a join defect. Tradeoff: snack bars, hotel
   restaurants and caterers that a 業態 column would set aside elsewhere stay in
   Food service here, and the page says nothing about it.

## What the build must still measure

- ⚠️ **Shared code** (each with the Minato control and every city screen):
  **自動販売形態 as a vending form** (91 rows, 75 of them cup-vending 喫茶店 now
  in Food service); **特殊形態 as temporary / mobile** (Okayama's old-law form:
  63 of 71 restaurants with it are area-wide; 7 at an address, plus 菓子 19 and
  喫茶店 11): confirm the meaning in the prefecture's old 施行条例 before the
  rule lands; 簡易形態, 普通形態 and 卸販売及び小売販売形態 stay fixed premises.
- The PDF reader in `source_rows` (above), stopping on any line it cannot read;
  `SOURCE_AS_OF` and `TERM_AS_OF` 2026-03-31; the same-number rule (call 3).
- Expected after step 2: about 3,933 Food-service and 886 Retail pins; the
  factory share (菓子 / そうざい) printed; the census control
  (`japan_census_control.py`, add `kurashiki` to its run) near 2.8 with the
  3.31 reason beside it.
- MHLW's 4 points over 1 km; gate 3; OSM `name:en`; JR West's 木見 / 上の町
  counts; line colours and the three registry entries; the opening view
  (`map-view`, `scripts/check_map_view.js`); `check_provenance.py`,
  `check_scope_disclosure.py`, the notice from the licence read.

```brief-checks
[
  {
    "id": "kurashiki-page-year-end-pdf",
    "claim": "Page 1004977 still links the year-end list r07nenndinatu.pdf (7.7MB), the newest monthly file read (r08hatigatu.pdf) and the CC BY 4.0 mark. ASCII anchors only: the host sends text/html with no charset",
    "kind": "http_contains",
    "url": "https://www.city.kurashiki.okayama.jp/business/health-safety/1004966/1004974/1004977.html",
    "present": ["r07nenndinatu.pdf", "PDF 7.7MB", "r08hatigatu.pdf", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "kurashiki-year-end-pdf-live",
    "claim": "The year-end PDF answers keyless at its own URL, at least 8,000,000 B (8,034,340 B cached 2026-10-08)",
    "kind": "http_ok",
    "url": "https://www.city.kurashiki.okayama.jp/_res/projects/default_project/_page_/001/004/977/r07nenndinatu.pdf",
    "min_bytes": 8000000
  },
  {
    "id": "kurashiki-catalogue-csv-live",
    "claim": "The catalogue's 2026-03 CSV (resource 17772, 791,423 B), every permit of which is in the PDF, still answers",
    "kind": "http_ok",
    "url": "https://kurashiki.dataeye.jp/resource_download/17772",
    "min_bytes": 780000
  },
  {
    "id": "kurashiki-catalogue-csv-rows",
    "claim": "The cached catalogue CSV holds 3,172 permits (local file on the shared data folder)",
    "kind": "row_count",
    "path": "data/kurashiki/raw/332020_food_business_all2026_standard.csv",
    "expect": 3172
  },
  {
    "id": "kurashiki-isj-block-live",
    "claim": "MLIT's block file for Kurashiki (33202) answers keyless (518,442 B, 62,007 keys) - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/33202-24.0a.zip",
    "min_bytes": 450000
  },
  {
    "id": "kurashiki-isj-chome-live",
    "claim": "MLIT's town-chome file for Kurashiki (33202) answers keyless (10,875 B)",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/33202-19.0b.zip",
    "min_bytes": 8000
  },
  {
    "id": "kurashiki-mhlw-live",
    "claim": "MHLW's open-data file for 33202, the position check and open call 2, answers keyless (518,644 B on 2026-10-08)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=33202_food_business_all.csv",
    "min_bytes": 300000
  },
  {
    "id": "kurashiki-mizurin-timetable",
    "claim": "The Mizushima Rinkai Railway's timetable page is the 2026-03-14 revision read here (last up train 22:06 from Mizushima, 22:30 at Kurashiki-shi)",
    "kind": "http_contains",
    "url": "https://www.mizurin.co.jp/contents/time_table.html",
    "present": ["2026年3月14日改正", "三菱", "22:06", "22:30"]
  },
  {
    "id": "kurashiki-ibara-timetable",
    "claim": "The Ibara Railway's timetable page still shows the 2026-03-14 revision's two images read here",
    "kind": "http_contains",
    "url": "https://www.ibara-railway.co.jp/info/timeline/",
    "present": ["2026年3月14日改正", "timelinenoborisita-scaled.png", "timelinekudari-scaled.png"]
  },
  {
    "id": "kurashiki-projected-crs-west-edge",
    "claim": "Kurashiki's western edge (133.602 E, the N03 extent) projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 133.602,
    "expect": "EPSG:32653"
  },
  {
    "id": "kurashiki-projected-crs",
    "claim": "Kurashiki (centroid 133.746 E) projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 133.746,
    "expect": "EPSG:32653"
  }
]
```
