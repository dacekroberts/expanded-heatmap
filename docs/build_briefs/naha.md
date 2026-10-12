# Naha — build brief

**Band B, Food plus Personal services (owner, call S38, 2026-10-12: "food plus personal services for naha", "s38 yes"): food from the rebuilt register (Kyoto's shape), barbers and beauty salons from the city's two registers, no laundries (none published).** Banded B, food only, earlier the same day (call S30, on this brief's Step 0; C until then); wherever a section below still says "food only until O8", O8 is answered yes. **Page 307, notice 217** (reserved in `docs/session_roles.md`). **Naha joins phase 2** (owner, 2026-10-12): Cleanup lands the shared-code items 1 to 5 below on master before the build starts. The owner
approved **a brief and the two licence reads** on 2026-10-11 (call S13: "yes
brief and license reads for two packages"), accepted the city's
cost-recovery clause on 2026-10-12 (call S15) and approved the two MLIT
address downloads the same day (call S29). The build session's prompt is in `docs/build_plan_2026-10-07.md` ("Naha"). The
calls this brief first listed as open (O1 to O7 below) were answered the
same day as S30 to S36; each is marked where it stands. **Step 0 measured
2026-10-12** (staging), from files already on disk and nothing else:

- `data/naha/raw/shinki/`: **140** monthly new-permit workbooks (50 `.xls`, 90
  `.xlsx`, 5,675,149 B), 2015-04 to 2026-08, BODIK package `shinki_syokuhin`,
  fetched by Kansai-2 on 2026-10-11 (one GET every 21 s, every one HTTP 200).
- `data/naha/raw/keizoku/`: **73** monthly renewal workbooks (2,963,215 B),
  2015-04 to 2021-05 (2019-05 absent), package `472018_keizoku_syokuhin`.
- `data/naha/raw/isj/47201-24.0a.zip` (**162,904 B**, block level) and
  `47201-19.0b.zip` (**8,025 B**, town-chōme), from `nlftp.mlit.go.jp` with
  the project user-agent, each HTTP 200 (staging, call S29).
- `data/naha/raw/ribiyou/r080904biyou.xlsx` (**113,145 B**, beauty salons)
  and `r080904riyou.xlsx` (**37,114 B**, barbers), BODIK package
  `472018_ribiyou`, fetched by staging from `data.bodik.jp` on 2026-10-12
  (owner call S37). Measured the same day; the package's licence was read the
  same day (PERMITTED WITH CONDITIONS, the Licences section).
- The shared cache: `data/japan/raw/N02-25_GML.zip`,
  `N03-20250101_47_GML.zip`, e-Stat's 衛生行政報告例 tables and the 2021
  Economic Census table; e-Stat's barber and beauty table (第10表) in
  `data/hamamatsu/raw/estat_eisei_r6_riyo_biyo_by_city.csv`.

**Measured**: the rebuilt register (Kansai-2's control reproduced to one
row), the storefront counts through `japan_eigyo`, the MLIT join, the name
rule, the rail cut, the official counts, and the barber and beauty registers
(shape, dates, official shares, join, name rule). **Not measured, and why**:
train frequency (not re-read; the master list's READ of 2026-10-06 stands),
gate 3 against the operator, OSM `name:en`, and an independent check of the
join (the files carry no coordinates). **Nothing was fetched by the Step 0
scripts**; staging fetched the files named above on the owner's calls.

**Run `python scripts/brief_check.py naha` before writing any code.** Then
the `japan-city` skill, **Kyoto's shape** (`docs/build_briefs/kyoto.md`: a
register REBUILT from monthly permit files,
`japan_register.rebuilt_register`, closures invisible, the count an upper
bound) on a food-only page (Kurume's, Hiroshima's, Yao's). Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from scratch scripts only. Rail: MLIT N02-25 cut at the N03 city line through
`pipeline/countries/japan.py` with an in-memory `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count** (none
runs here); (2) **the city line only**: only stations inside the city get
rings, a line is drawn and cut at the line (2026-09-24); (3) **菓子製造業 and
そうざい製造業 count, in Retail**, the factory share measured and kept; (4)
**the name rule**, version 2 (2026-10-06): 申請者名 and 代表者名 are operator
columns, read in memory, and a bare personal name is withheld whatever they
hold; the rule crosses premises (call 205, `name_city`); (5) **no page says
"currently operating"**; (6) **市内一円 rows are not premises** (Kobe's trap
6; here 那覇市内 and 沖縄県全域); (7) hostess venues, vending machines, event
caterers and institutional kitchens are out by `FORM_RULES`; (8) fault-based
and use-triggered cost clauses accepted (2026-09-24; Naha's 第5項 by call
S15); (9) English station names from OSM `name:en`, numerals as figures; (10)
a new city reads `ALL_RULES` (leave `"rules"` out of its `japan.CITIES`
entry); (11) one color per line site-wide (`pipeline/line_registry.py`),
clear of the pins by CIE76 20; (12) `as_of` is the last day the newest list
covers, never today (Kyoto, 2026-09-28): **2026-08-31**; (13) a stated food
share where a list is incomplete (call 125). Not in play here: limited
expresses, JR's frequency floor, funiculars, one-station stubs.

**✅ A monorail counts as rail**, by precedent: the Tama Toshi Monorail is
drawn on Tachikawa's and Higashiyamato's maps, the Kitakyushu Monorail on
Kitakyushu's, and the owner counted the Maihama Resort Line as rail (call 53,
2026-10-06). The Yui Rail is the same kind (a straddle monorail on its own
viaduct). **`mode` for a city whose ONLY line is a monorail has no
precedent** (Open calls, O4).

---

## The one-line summary

**Naha publishes no full food-permit list, only each month's new permits
(and, to 2021-05, each month's renewals). Rebuilt Kyoto's way and kept while
in term on 2026-08-31, the new-permit files give 10,000 permits, 8,429 of
them restaurants: 98.8% of e-Stat's 8,530 in force** (103.0% with the
renewals). ⚠️ **Closures are invisible**, so the count is an upper bound, and
a high one: 2.77 placed restaurant premises per Economic Census establishment
against 1.56 to 1.92 on the built cities. **Storefront rows: Food service
7,390, Food shops 1,358; 8,450 pins** after one pin per premises. **The MLIT
join places 99.9%** (block 98.9%, town-chōme 1.0%, 9 rows unplaced), far over
the 70% bar. **Rail: the Yui Rail, 16 of its 19 stations inside the city**
(3 in Urasoe, the separate add-on row), median gap 733 m, standard rings.
**Personal services: the city's barber and beauty registers, complete lists
as of 2026-09-04: 287 barbers and 1,069 beauty salons (101.8% and 104.1% of
e-Stat's 282 and 1,027 in force at 2025-03-31), 1,353 pins, every row placed
(block 95.1%, town-chōme 4.9%), no name withheld.** No laundry list is
published. So the page would be **Food plus Personal services (barbers and
beauty salons, no laundries)** once the package's licence is read and the
owner widens S30's food-only band (Open calls, O8); food only until then.

---

## Business leg — a register rebuilt from monthly permit files

| | New permits | Renewals |
|---|---|---|
| **Package** (BODIK, `data.bodik.jp`, organization 那覇市 472018) | `shinki_syokuhin`, （新規）食品営業許可施設 | `472018_keizoku_syokuhin`, （継続）食品営業許可施設 |
| Files | **140**, 2015-04 to 2026-08, every month present; three months published twice (2025-03, 2025-12, 2026-08: two resources each, identical rows, 394 repeats) | **73**, 2015-04 to 2021-05; 2019-05 absent. Renewals from 2021-06 are inside the new-permit package (the package's own note, READ by the licence agent) |
| Rows (MEASURED 2026-10-12) | **17,289**, of them 8 repeated header rows: **17,281** permits, 16,885 distinct by permit number, type and expiry | **4,337**, of them 2 repeated header rows: **4,335** |
| Format | One sheet a workbook, the header in row 1 (row 2 in two files). 50 old BIFF `.xls`, 90 `.xlsx` | 52 `.xls`, 21 `.xlsx` |
| As of / cadence | Monthly. Pin `as_of` to **2026-08-31** | Closed series |

**Columns, and how they vary** (29 distinct header rows in the new-permit
files, 21 in the renewals; column names only):

| Role | Spellings seen |
|---|---|
| Trade name | 営業所名称 (all but four files), **営業所名所** (2020-08, a typing slip, 86 rows), 施設_名称 (2026-01 to 03) |
| Address | 営業所所在地 (所在地１ in 2026-01), then a second column: headed **気付** to 2018, unnamed from 2019, 所在地２ in 2026-01. The first column is the whole address (town and number); the second is the building and floor (filled on 9,462 rows; where it starts with a digit, 1,944 rows, it is a room or floor, never the lot number) |
| Permit type | 営業の種類 (most), **業種** (2025-08 on), **営業所種類** (2022-12), **営業の種目** (2018-03, 2018-06) |
| Form (業態) | To 2018 inside the type's brackets (飲食店(バー)); from 2019 in an **unnamed column** beside 営業の種類 (3,405 rows); headed 種目 from 2025-08 (206 rows) |
| Expiry | 有効期限 or **有効期間** (a single date either way), 許可終了日 (2022-07, 2022-08, 2026-01 to 03). Wareki text (R08.09.30, H30. 9.30) on all but 5 rows, which are Excel serials; `wareki_date` reads every one |
| Granted | 許可日, 許可年月日 (one renewal file), 許可開始日 |
| Operator (never selected) | **申請者名** (申請者_氏名 in 2026-01 to 03), **代表者役職 and 代表者名** (2015-04 to 2021-05 only), **法人** (2026-02, 2026-03: a one-or-two-character mark on 128 rows, each beside a company's 申請者名; a flag, not a name), 申請者住所 / 申請者所在地 / 申請者住所１, ２ (one to three columns), 申請者電話 / 申請者電話番号, 営業所電話; 管理番号 in three files |

**The control (MEASURED 2026-10-12).** Kansai-2's figure is reproduced to one
row: **8,939** restaurant permits (type 飲食店営業) in term from the
new-permit files against its 8,938; 10,581 food permits against 10,580; the
renewals' 375 and 536 exactly; every grant year identical but 2024 (1,439
against 1,438). The one row is a 2024 grant whose expiry is an Excel serial
number, which the shared `wareki_date` reads (21,616 dated rows here, 21,615
there). **A correction to that measurement**: 346 of the 8,939 are the three
twice-published months, so the files hold **8,593 distinct restaurant permits
in term (100.7% by permit)**, not 104.8%; by premises nothing moves (8,430
distinct address and name here, 8,429 there).

**The stitch**, through `japan_register.rebuilt_register` itself (its
`city_rows` swapped in the scratch process for a reader of Naha's columns;
see ⚠️ Shared code), `as_of` 2026-08-31, key (address, trade name, type),
the permit ending latest wins:

| | New-permit files alone | With the renewals |
|---|---|---|
| Permits in term | **10,000** | 10,515 |
| of them 飲食店営業 | **8,429** = **98.8%** of 8,530 | 8,786 = 103.0% |
| Storefront rows | **8,748** (Food service 7,390, Retail 1,358) | 9,164 (7,659, 1,505) |
| Pins (placed, one per premises and bucket) | **8,450** (Food service 7,382, Retail 1,068) | 8,799 (7,650, 1,149) |

- **No renewal trap** (Kansai-2, confirmed): in-term restaurant permits by
  grant year run 2020 360 · 2021 1,198 · 2022 1,506 · 2023 1,645 · 2024
  1,439 · 2025 1,619 · 2026 (to August) 1,166. Terms are 6 years (8,103), 5
  (823) or 7 (13). No permit in term runs under a year, none starts after the
  as-of, none ends before it was granted.
- **What the rules set aside** (new-permit files, of the 10,000 in term):
  **769** addressed only 那覇市内 (every one 種目 臨時営業, stalls licensed
  citywide on multi-year terms; the `citywide` rule); **171** area-wide
  (沖縄県全域 166, 県内一円 3, two others: 種目 自動車営業, vehicles; the
  `areawide` rule); **312** not a storefront: no rule 199 (all manufacturing
  or wholesale: 漬物 30, 清涼飲料水 23, 密封包装食品 23, 食品の小分け 19, 麺類
  15, 豆腐 14, 酒類 13 …), hostess venues by 種目 54, vending 51 (38 by 種目,
  13 by type), event caterers 7, temporary 1. No row is addressed in another
  municipality; none has a blank address or a blank trade name.
- **Storefronts by rule**: restaurant 7,384, café 6; confectioner or bakery
  501, deli 317 by type and 77 by 種目 (a restaurant permit filed as
  そうざい), butcher 217, fishmonger 207, dairy 39.
- **Catch-all share: none.** The scheme is the national permit types; "no
  rule" is 199 of 10,000 (2.0%), every one a manufacturing or wholesale type.
  What IS thin is the form: 種目 is filled on **20.0%** of in-term restaurant
  permits (all of 2019-20, 40% of 2021, about 13% since), so a bar or snack
  bar granted since 2021-06 mostly reads as plain 飲食店営業 and the hostess
  rule reaches only the 54 that say so (MHLW's optional 業態 is the same
  shape in every MHLW city).
- **One premises, several permits**: 289 repeat rows fall to one pin per
  (address, trade name, bucket), nearly all Retail (a bakery holding 菓子 and
  そうざい): Retail 1,358 rows, 1,068 pins. 8,120 distinct (address, trade
  name) pairs. The stitch itself folds the 394 twice-published rows and every
  re-permit of one premises under one name and type.
- ⚠️ **Same-address successors** (Kyoto's open item): the same full address
  (with the building column) and type under two or more trade names, 451
  groups, **693 extra rows (7.9%)** against Kyoto's 4.3%. An upper reading:
  3,151 storefront rows have no building column, and one lot holds several
  units. Kept, measured, as Kyoto's.
- ⚠️ **Economic Census control**: the 2021 census counts **2,669** 飲食店
  establishments in 47201 (the cached table, READ 2026-10-12); 7,382 placed
  Food-service premises is **2.77 per establishment**, far above the built
  cities' 1.56 to 1.92 (the range Yao's brief quotes; not re-derived here).
  e-Stat's in-force count is as high (3.20 permits per establishment), so
  the register matches the official count and both run well ahead of the
  census: closed bars and stalls whose permits have not lapsed, on the
  evidence to hand. Open calls, O3.
- **菓子 / そうざい factory share**: 31 of 770 pins (4.0%) have a trade name
  reading as a factory or central kitchen; kept, measured.

### The renewals package: use it (recommendation; Open calls, O2)

Kansai-2 counted 375 renewal restaurant permits still in term and proposed
the new-permit files alone. Measured through the rules, the renewals add
**515 permits in term, 416 storefront rows and 349 pins** (Food service 268,
Retail 81): premises that renewed between 2020-04 and 2021-05 under six-year
terms and have not yet re-permitted into the new-permit files. They are real
in-force permits of long-standing premises, the licence is the same read, and
the gap closes by itself by 2027-05. Leaving them out drops about 4% of the
map's pins for a tidier ratio (98.8% against 103.0%).

### Coverage, stated honestly

- **8,530** restaurant permits in force is the master-list row's figure:
  **re-derived 2026-10-12** from the cached e-Stat tables through
  `japan_official.restaurants("沖縄県", "那覇市")` (MHLW 衛生行政報告例
  FY2024, tables 5-2-1 + 5-4-1, old law plus revised law, at 2025-03-31).
- The rebuild's 98.8% (103.0%) is **an upper bound, not coverage**: a
  premises that closed stays until its permit expires, five to seven years
  after the grant. The page says so in Kyoto's words.
- MHLW's own file for Naha holds 97 restaurant permits (1%; the master list,
  READ 2026-10-06): it adds nothing and carries no usable point.
- **Food retail is by permit type only** (菓子, そうざい, 食肉, 魚介類, the
  40 乳類 still in term). Packaged-only sale has been a notification since
  2021-06 and is in neither package.

### Personal services: the city's barber and beauty registers (no laundries)

Found by the probe of 2026-10-12 (owner call S34: a city-probe agent, 3 BODIK
calls 22 to 24 s apart), downloaded on call S37 and **MEASURED 2026-10-12**.
BODIK package `472018_ribiyou` (理容所・美容所新規開設施設情報,
`https://data.bodik.jp/dataset/472018_ribiyou`), CC BY 4.0 as STATED at
package level, monthly by its stated frequency.

| | Beauty salons | Barbers |
|---|---|---|
| File | `r080904biyou.xlsx`, 113,145 B | `r080904riyou.xlsx`, 37,114 B |
| Sheet and title | one sheet (`Sheet1`); row 1 reads `美容所開設施設一覧（令和8年9月4日時点）` | one sheet; row 1 reads `理容所開設施設一覧（令和8年9月4日時点）` |
| Header (row 2) | No, 業種, 確認番号, 確認年月日, 施設名称, 施設住所, 開設者氏名 | the same seven |
| Rows | **1,069**, every cell filled, 業種 美容所 on all | **287**, every cell filled, 業種 理容所 on all |
| 確認年月日 | **1958-08-08 to 2026-09-04**, every row a readable wareki date, listed oldest first | **1958-08-12 to 2026-05-28**, likewise |
| By decade confirmed | 1950s 1 · 1960s 11 · 1970s 66 · 1980s 95 · 1990s 101 · 2000s 195 · 2010s 283 · 2020s 317 | 1 · 6 · 29 · 46 · 53 · 68 · 38 · 46 |
| e-Stat in force (READ 2026-10-12: 衛生行政報告例 FY2024, 生活衛生 第10表, row 沖縄県那覇市, at 2025-03-31) | **1,027**: the list is **104.1%** | **282**: the list is **101.8%** |

- **A full register of open premises, not a list of openings** (settled by
  the data, despite the package title's 新規開設): the files are titled "as
  of 2026-09-04", reach back to 1958, and match the official in-force counts
  within the 17 months between the two dates (e-Stat counts 37 beauty and 2
  barber confirmations in FY2024; the lists hold 86 beauty and 12 barber
  rows confirmed in 2025 and 2026). **Closed premises are removed**: No runs
  1 to 1,069 and 1 to 287 with no gap (a row number, renumbered each
  edition), while 確認番号 does not run continuously (three formats: 中S…,
  中H… and, from 2013, 第…号 with a yearly prefix; 26 to 56 beauty rows
  survive from each year since 2012 against far wider number ranges), and
  the older decades thin out as a pruned register's would. Not an upper
  bound of the food rebuild's kind.
- No note, licence or consent wording in any cell, comment or page header;
  the title row is the only text outside the table.
- **Through `japan_eigyo` and `filter_to_storefront()`** (step 2's order,
  `kind` barber and beauty): **1,356 storefront rows, all Personal services**
  (barber 287, beauty 1,069). Nothing is set aside: no blank or area-wide
  address, no 移動 or 出張 salon, no welfare-facility salon, no storeless
  row. One pin per (address, name, bucket) drops 3 (two beauty repeats and
  **1 premises in both files**, the one 重複開設 e-Stat counts): **1,353
  pins** (beauty 1,067, barber 286). Fifteen addresses appear in both files
  under different names (neighbors in one building). Possible successors
  (one address, two names): 10 beauty rows, 2 barber rows.
- **The join** (the two MLIT files above, `ALL_RULES`, wardless):

  | Tier | All (1,356) | Beauty (1,069) | Barbers (287) |
  |---|---|---|---|
  | Block | **95.1%** (1,290) | 95.6% (1,022) | 93.4% (268) |
  | Town-chōme | 4.9% (66) | 4.4% (47) | 6.6% (19) |
  | Unplaced | **0** | 0 | 0 |

  Every address starts 那覇市 and carries a number (丁目 written out in 302,
  番地 in 61, 字 in 28). Town tier, by town: 字安里 11, 字古島 7, 真嘉比 7,
  古波蔵 5, 字宇栄原 4, 壷川 4, 字小禄 4, 字松川 4, 字高良 2, 字与儀 2, and
  sixteen towns with one each (地番 MLIT's block file does not key). No
  independent check: the files carry no coordinates.
- **No laundry list is published**: none among the organization's 38
  datasets, and the health center's クリーニング所 pages hold procedure PDFs
  only (the probe, READ 2026-10-12).
- ⛔ **BODIK copies only**, as for the food packages: the city's own copies
  sit under its reserved-rights site terms.
- **No shared-code change is needed for these two files.** `city_rows` finds
  the header under the title row; 施設住所, 施設名称 and 業種 are in
  `ADDR_COLS`, `NAME_COLS` and `TYPE_COLS`; 開設者氏名 is in `OPERATOR_COLS`;
  there is no term column, so no `TERM_AS_OF` entry. Config only: two
  `SOURCES` keys (`barber`, `beauty`) reading the files as they are, and
  `SHARE_DATES = {"barber": "確認年月日", "beauty": "確認年月日"}` if the
  page states a share at e-Stat's date. One gap, not a blocker:
  `japan_official.registers()` reads Tokyo's yearbook only, so the e-Stat
  shares above come from the cached 第10表 by hand (Hakodate's and
  Hamamatsu's configs name that file).

**So the page would be Food plus Personal services (barbers and beauty
salons, no laundries)**, a reduced Personal services bucket disclosed as
such, once the package's licence read returns and the owner widens the band
(Open calls, O8). Until then it stays food only ("**This map shows food
businesses only.**").

### ⚠️ Shared code

Nothing was edited. What a build needs from shared code, or must do in its
own config, each measured on the unchanged readers:

1. **`rebuilt_register` reads paths through `city_rows` only**; it has no
   way to take rows or a city's reader. Naha's workbooks need a reader of
   their own (items 2 to 4), so the build needs a `rows=` or `reader=`
   argument there. Kyoto's `config.source_rows` covers step 2, not the
   stitch, and the skill forbids copying the stitch into a city.
2. **Unnamed header columns.** `xlsx_rows` zips header to cells, so every
   unnamed column lands on the one key `""` and the last one wins;
   `workbook_tables` names them `_colN`. The 種目 beside 営業の種類 is unnamed
   in the 2019 to 2025 files (3,405 rows; only the 206 under a 種目 header
   are read). Without it, in term: 54 hostess venues, 38 vending machines, 7
   caterers and 1 temporary stall read as restaurants, and 77 delis read as
   Food service. The same key can end up holding the applicant's address
   continuation: never selected, but it sits in the row dict.
3. **`NAME_COLS` lacks 営業所名所** (the 2020-08 file: 86 rows read no trade
   name, so the name rule compares nothing on them).
4. **`TYPE_COLS` lacks 営業所種類** (the 2022-12 file: 84 in-term rows read
   no type and fall to "no rule") **and 営業の種目** (2018-03, 2018-06; out
   of term today).
5. **`VARIANTS` lacks 壼 (U+58FC) for 壺**: 2 rows of 壺屋 unplaced. Kyoto's
   rule B has 壷/壺 only.
6. Not shared code, but config: `end_col=("有効期限", "有効期間",
   "許可終了日")` (END_COLS lacks 有効期間: with END_COLS alone the stitch
   keeps 2,573 permits, not 10,002) and `granted_col=("許可日",
   "許可年月日", "許可開始日")`; `config.NOT_OPERATOR = {"法人": "a
   one-character company mark, not a name"}` (step 2's operator-like test
   does not match a bare 法人, so nothing stops on it); `TERM_AS_OF`.

The unchanged readers do read every file (no file returns 0 rows), every
address and every grant date; the join needs no new rule.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`; MLIT keys every town
under an empty ward). Block `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/47201-24.0a.zip`
(162,904 B, **17,689 block keys**), town-chōme `.../19.0b/47201-19.0b.zip`
(8,025 B, **219 keys**: 184 丁目 towns, 26 with 字). Downloaded 2026-10-12
(owner call S29). `japan.CITIES` entry at build: `"naha": {"name": "那覇市",
"pref": "47", "epsg": 32652, "n02": "25", "wardless": True, "wards":
["47201"]}` (no `"rules"`: a new city reads `ALL_RULES`).

| Tier (storefront rows, `ALL_RULES`; MEASURED 2026-10-12) | All (8,748) | Food service (7,390) | Retail (1,358) |
|---|---|---|---|
| Block | **98.9%** (8,654) | 99.0% (7,315) | 98.6% (1,339) |
| Town-chōme | 1.0% (85) | 0.9% (69) | 1.2% (16) |
| Unplaced | 0.1% (9) | 0.1% (6) | 0.2% (3) |

With the renewals: 9,067 / 87 / 10 of 9,164, the same shares.

- **Placed: 99.9%, against the owner's bar of about 70%** (rule 5 of the
  reduced-bucket bar; Kure's 69.4% the one city let through under it). No
  address is withheld: every in-term row carries one, and the only rows
  without a number are the 940 citywide and area-wide ones set aside above.
- **Naha's files carry no coordinates**, so there is no publisher's point to
  fall back on and none to check against. Internal checks only: all 8,739
  placed points lie inside the N03 city polygon; 8,455 of the 8,654 block
  points sit within 500 m of a centroid of their own town, 198 between 500 m
  and 1 km, 1 beyond.
- **Address shapes** (storefront rows): 沖縄県那覇市 leads 2,015 and 那覇市
  6,733; town-N-N-N (住居表示) 7,123, town-N-N 1,208, a single 地番 403; 字
  written in 190, 番地 in 15, 丁目 in 8. **字 and 地番 join as they are**: of
  the 190 字 rows 173 reach the block tier, 14 the town and 3 nothing; of the
  403 one-number rows 375 reach the block.
- **The misses, read** (towns only). Unplaced 9: 壼屋 2 (⚠️ Shared code 5),
  鏡水崎原地先 2 (reclaimed land by the airport, one of them the free trade
  zone), 字金城, 字旭町, 字古波蔵, 首里当蔵, 上間東原, one each. Town tier 85:
  字安里 43, 字松川 8, 楚辺1丁目 4, 字小禄 4, 樋川2丁目 3, 牧志3丁目 3,
  松尾1丁目 3, 具志 3 … (地番 MLIT's block file does not key; 84 of the 85
  carry a number).
- ⚠️ **Dense blocks.** A block point is one point: 8,654 rows fall on 1,556
  points (median 2 rows a point); 20 points hold 50 or more rows (1,438 rows
  in all), the entertainment blocks of 松山1丁目 and 2丁目, 牧志3丁目,
  松尾2丁目 and 港町1丁目. **One 字安里 lot stem holds 246 rows**: 地番 388
  and the like, split into sub-lots the block key does not carry (a market
  arcade, ASSERTED; read at build). Honest at block precision, but the
  map's densest dot is one lot.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_47_GML.zip`, N03 code
47201 (**41.4 km²**, seven polygon parts with the offshore islets; extent W
127.630, S 26.176, E 127.739, N 26.253). MEASURED 2026-10-12.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 沖縄都市モノレール線 (沖縄都市モノレール; class 23, a straddle monorail; operator type 5, third sector) | Okinawa Urban Monorail, the Yui Rail (ゆいレール) | **16 / 19** | 那覇空港, 赤嶺, 小禄, 奥武山公園, 壺川, 旭橋, 県庁前, 美栄橋, 牧志, 安里, おもろまち, 古島, 市立病院前, 儀保, 首里, 石嶺 |

- **19 station records, 19 `N02_005g` groups; 16 inside, each its own
  group.** No name in two groups. It is Okinawa's only N02 line: 37
  sections, 17.1 km, 14.7 km of it inside Naha. N02-24 holds the same 19.
- **In Urasoe (浦添市, 47208), cut at the line**: 経塚, 浦添前田, てだこ浦西,
  the last three stations. 経塚 is 180 m outside the line. Not a stub: the
  line keeps 16 of 19. Nearest inside stations to the line: 旭橋 328 m (the
  coast), 古島 334 m, 石嶺 417 m.
- **Median nearest-group gap 733 m** (319 m 牧志 to 安里; 469 m 旭橋 to
  県庁前; 1,704 m 那覇空港 to 赤嶺): over the spacing rule's 550 m, so
  **standard rings** (`[0.0, 0.1, 0.2, 0.3, 0.6]`); recompute on the
  stations drawn.
- **The light-rail/rail test**: a straddle monorail on its own viaduct
  counts as rail (the Tama Toshi Monorail on Tachikawa's and Higashiyamato's
  maps, the Kitakyushu Monorail, the Maihama Resort Line by call 53). No JR,
  no private railway, no tram, no funicular in Okinawa.
- **Frequency**: READ 2026-10-06 by the wave-4 probe at Urasoe's stations,
  every 7 to 9 minutes, about 150 trains a day each way (the master list's
  row). **Not re-read here.** No stretch is near 11 trains a day.
- ⚠️ **Gate 3** at build: the operator's own station count (19 on the line,
  16 in Naha: ASSERTED from N02, to be read from the operator). **OSM
  `name:en`** for 16 groups (one Overpass query at build; not queried here).
  One line, new to the site: a `pipeline/line_registry.py` entry in the
  build branch, since the Urasoe add-on will draw it too.

## Scope

**Naha City (47201) only.** The Yui Rail runs on to てだこ浦西 in Urasoe; cut
at the line, the three stations written to `excluded_stations.csv` under 浦添市
and named on the page. **Urasoe's three stations are the separate add-on row**
("Naha (Regional) + Urasoe", owner 2026-10-06): only once Naha is built, on
Okinawa Prefecture's own BODIK food list, by the `regional-extension` skill.

## Licences — READ 2026-10-11 (two agents, one per package)

- **Naha City's two BODIK packages — PERMITTED WITH CONDITIONS** (staging's
  drafts, 2026-10-12 bullet). Both declare `cc-by-40-intl`; no resource
  carries terms of its own; both link the city's open-data terms at
  `odcs.bodik.jp/472018/tos/`: **CC BY 4.0 unless annotated** (第3項).
  - **MUST DISPLAY**: a credit to 那覇市 with the dataset names and source,
    the CC BY 4.0 link, and **a statement that the data was modified**. No
    wording is prescribed: the notice is this project's wording, a proposal
    at build.
  - **MUST NOT**: present modified data as the city's own; imply
    endorsement; say "currently operating".
  - **MUST DO**: nothing; no notification is owed. Governing court: Naha
    District Court (第6項).
  - **第5項, the cost-recovery clause** (the city bills the user for costs,
    damages included, arising from the user's own breach or infringement of
    a third party's rights, no cap): **accepted by the owner, call S15**, on
    the precedent of calls 206, 207 and 214.
  - ⛔ **BODIK copies only.** The city's own site hosts the same monthly
    lists with no licence, under website terms that reserve all rights and
    forbid reuse without permission. Fetch from `data.bodik.jp`, never from
    the city's site. The cache matches the packages' resource counts (140,
    73).
  - **The applicant columns are not licensed** (CC BY 4.0 s.2(b)(1): name,
    address and phone of a person) and are never selected.
  - **A note inside a workbook: checked 2026-10-12, none exists.** All 213
    workbooks: no licence, source or consent wording in any title row,
    lone-cell row or cell comment; the page headers and footers of the
    `.xlsx` files hold the month's date range and a page number only. Still
    not established: the page setup of the 102 old `.xls` files (not read).
- **The barber and beauty package (`472018_ribiyou`) — PERMITTED WITH
  CONDITIONS, READ 2026-10-12** (staging's licence-read agent; two BODIK
  calls 29 s apart, no data file opened): `cc-by-40-intl` at package level,
  no licence, rights or description on either resource, the same city terms
  linked (`odcs.bodik.jp/472018/tos/`) and nothing that annotates them, so
  the conditions are the food packages' (credit, a statement of
  modification, not presented as the city's, 第5項 accepted by call S15).
  No wording is prescribed; **one notice can name all three packages**
  (one publisher, one set of terms), the build claiming one notice number.
  The city's own page for the lists (page 1006638) states no terms, sits
  under the reserved-rights site terms and carries files named
  `r080914...` against BODIK's `r080904...`: **BODIK copies only**. The
  package note calls the lists new openings tallied monthly; the files'
  own title rows and dates show full registers as of 2026-09-04 (the
  Personal services section). Checked here, 2026-10-12: neither workbook carries a note,
  licence or consent wording (the title row gives the as-of date only).
  開設者氏名 is a person's name on about five rows in six: not licensed by
  CC BY (s.2(b)(1)) and never selected.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census:
  measurement sources.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here. `docs/data_sources/japan.md` gets the
  rows at build; none is written by this brief.

## Privacy

- The files carry **申請者名, 代表者役職, 代表者名, the applicant's address
  (one to three columns) and two phone columns**: never selected into an
  output. 申請者名 and 代表者名 are read IN MEMORY for the name rule only;
  the stitch carries the rule's yes or no, never a name.
- **The name rule, version 2, measured in memory** (answers only, never a
  value; MEASURED 2026-10-12, the 8,748 storefront rows of the new-permit
  files): a company marker on the operator on **3,427**, **none on 5,321**;
  **4** rows whose trade name IS an individual operator's own name
  (withheld, shown as their permit type; 5 among all 10,000 in term, 9 trade
  names across every month's file); **8** more whose trade name contains the
  operator's name beside other words (shown, by the owner's rule: a name
  plus a business word); **0** bare personal names. A fifth storefront row
  equals an operator the rule does not read as a person (the `coop` switch;
  not looked at further). The winning row of each stitched key carries the
  yes wherever any row of that key says it (4 of 4). With the renewals the
  counts are the same.
- **The barber and beauty registers carry 開設者氏名**, the operator's name
  (an individual on 1,139 of 1,356 rows; a company marker on 217: beauty 200,
  barbers 17): never selected, read IN MEMORY for the name rule only
  (already in `OPERATOR_COLS`). **Measured in memory, answers only
  (MEASURED 2026-10-12, 1,356 rows): 0 rows whose 施設名称 equals the
  operator's name, 0 that contain the whole name, 0 bare personal names: the
  withheld share is 0%**, in both trades, before and after the premises and
  city-wide spread. Naha's salons trade under shop names. A surname alone
  inside a longer shop name: 2 rows where the operator cell separates
  surname and given name (530 of the 1,139 do), and at most 14 more by a
  first-two-characters test on the rest (an upper reading); these are shown,
  by the owner's rule (a name plus a business word). No trade name is blank.
- Run `check_personal_exposure.py naha` (`japan=True`) after step 3; it must
  print 0. Record the verdict in the drafts file and
  `docs/privacy_verdicts.md`.

## Region

By the standing rule a city outside the five prefecture views tags its
traditional region: `"region": "Kyushu-Okinawa"` (in `JAPAN_REGIONS`,
`app/cities.py`), `"label_tier": "minor"`, `"country": "Japan"`. ⚠️ **Open**:
no built city is in Okinawa. Naha lies about 650 km southwest of Kagoshima,
so it would stretch the Kyushu-Okinawa view's fit and East Asia's (trap 11);
whether it joins the fit or is held out of it (`REGION_ZOOM_WITHOUT`) is
Cleanup's, measured with `scripts/stress_overview.py --planned 2` (Open
calls, O6). The city runs 127.630 to 127.739 E, centroid **127.684 E,
26.2105 N**: project to **UTM 52N (EPSG:32652)**, from the longitude
(Fukuoka's zone by coincidence, not by copying). OSM box from the N03
extent, rounded out: (26.17, 127.62, 26.26, 127.74).

**Scaffold** (once a build is approved): `scaffold_city.py --slug naha
--name Naha --system-name "Yui Rail" --taxonomy japan_eigyo --lat 26.2105
--lon 127.684 --region "Kyushu-Okinawa" --country Japan --mode light_rail
--page-number 307` (`--dry-run` first).

## Owner calls

**Made (do not re-ask):** a brief and the two licence reads (S13); the
cost-recovery clause 第5項 (S15); the two MLIT downloads (S29); the standing
Japanese calls above; a monorail as rail (call 53 and three built maps);
the city line only, Urasoe as the add-on row (2026-10-06); citywide and
area-wide rows out (Kobe's trap 6); 菓子 and そうざい in Retail; hostess
venues out where the form says so (2026-09-29); the name rule, version 2;
`as_of` the newest list's last day; standard rings by the spacing rule.

**ANSWERED by the owner on 2026-10-12 (calls S30 to S36), each as first put
with its recommendation and tradeoff:**

- **O1 = S30: Band B** ("s30 b").
- **O2 = S31: use both packages** ("s31 yes").
- **O3 = S32: the recommendation** (the upper-bound sentence with the
  measured figure, no trimming).
- **O4 = S33: `mode` is `light_rail`, not the recommended `metro`** ("light
  rail feels more appropriate due to size"). Scaffold with `--mode
  light_rail`.
- **O5 = S34: the probe runs** ("yes, do probe"); its finding is recorded in
  `docs/decisions_drafts/staging.md` and decides one bucket or two.
- **O6 = S35: the recommendation** (tag Kyushu-Okinawa; the fit is Cleanup's
  at landing).
- **O7 = S36: left for review time.**

**As first put:**

- **O1. The band.** *Recommend Band B, food only, on the rebuilt register
  with Kyoto's disclosures.* The one measurement the row waited on is met
  (98.8% by premises), the licence is read and placement is 99.9%. Tradeoff:
  an upper bound whose excess is larger than Kyoto's (O3), on one bucket.
- **O2. The renewals package.** *Recommend using both packages.* It adds 349
  pins of long-standing premises under the same licence and notice.
  Tradeoff: the restaurant count passes the in-force figure (103.0%), which
  the upper-bound sentence already explains; leaving it out loses about 4%
  of pins until 2027-05.
- **O3. How far above the census the map may sit.** 2.77 placed restaurant
  premises per census establishment against 1.56 to 1.92 built; possible
  successors 7.9%. *Recommend publishing with Kyoto's upper-bound sentence
  plus the measured figure against the in-force count, and no trimming*: no
  field separates a closed bar from an open one, and the official count is
  as high. Tradeoff: the densest blocks (松山, 牧志) will show more pins than
  a visitor finds open. The alternative, dropping the older name where one
  address and type carries two, removes at most 693 rows and some real
  neighbors with them; Kyoto kept them.
- **O4. `mode` for a monorail-only city.** *Recommend `metro`*: a
  grade-separated urban line every 7 to 9 minutes, and Higashiyamato's call
  170 read a monorail-led map as `metro`. Tradeoff: that map also drew JR
  and Seibu; here the monorail stands alone, and `light_rail` is the other
  reading.
- **O5. A personal-services probe before the build.** *Recommend one
  `city-probe` of BODIK's Naha organization (calls 20 s apart, BODIK's
  spacing) before banding*: a barber, beauty or laundry list would make it a
  two-bucket page. Tradeoff: about half an hour, and a licence read per list
  found; skipping it fixes the page as food only.
- **O6. The macro view.** *Recommend tagging Kyushu-Okinawa and letting
  Cleanup decide the fit at landing* (held out of the zoom fit if the view
  loses its other labels). Tradeoff: a dot that may sit off the pinned
  canvas on a phone until then; a view of its own is the owner's call.
- **O7. Three sentences no template covers**, proposals for review time: the
  twice-published months and the stitch; "stalls licensed citywide (769) and
  vehicles (171) are left out"; the dense-block note for 字安里.

**OPEN, put 2026-10-12 after the barber and beauty measurement:**

- **O8 = S38: ANSWERED YES by the owner, 2026-10-12** (the licence read returned PERMITTED WITH CONDITIONS the same day). As first put: **Widen S30's food-only band to Food plus Personal services (barbers
  and beauty salons, no laundries).** *Recommend yes, conditional on the
  package's licence read returning PERMITTED*: the two registers are
  complete (101.8% and 104.1% of the in-force counts), every row places, no
  name is withheld, and no shared code changes. Tradeoff: a Personal
  services bucket without laundries, disclosed as reduced (Kōchi's page is
  personal services only; a bucket missing one trade needs its own sentence
  at review time), and a second notice or a longer one. Not open: register
  or openings, which the data settles (a pruned register as of 2026-09-04).

## What the build must still measure

- The reader (⚠️ Shared code 1 to 4) landed first, by Cleanup or as the
  owner rules; then `config.source_rows` yielding the stitch, `as_of`
  **2026-08-31**. Expect about 8,748 storefront rows and 8,450 pins from the
  new-permit files (9,164 and 8,799 with the renewals).
- A newer month: BODIK adds a file a month; a build after September's file
  moves `as_of` and every count here.
- The Economic Census control (`scripts/japan_census_control.py`; 2.77
  expected, with the reason); the factory share (31 of 770); same-address
  successors; the 字安里 lot.
- An independent check of the join: GSI's address search on a sample of
  block-tier and 字 rows (Kyoto's method), since the files carry no point.
- Gate 3 against the operator; OSM `name:en` for 16 groups (one Overpass
  query); the Yui Rail's registry color on both basemaps, clear of the olive,
  magenta and green pins; the opening view (`map-view`);
  `check_provenance.py`; `check_scope_disclosure.py` (Urasoe's three
  stations; food only; the exclusions above).
- **If O8 is a yes and the licence read permits**: the two registers as
  `barber` and `beauty` sources, read as they are. Expect 1,356 rows and
  about 1,353 pins (beauty 1,067, barbers 286), block 95.1%, none unplaced,
  0 names withheld. A newer monthly edition replaces both files whole
  (re-measure the counts and the as-of in the title row; 2026-09-04 here).
  The shares against e-Stat's 第10表 (282 and 1,027) restated at its date
  with `SHARE_DATES`; the page's sentence that laundries are not published.
- The frequency, re-read from the operator's timetable (counts only).
- The page's businesses bullet and What Is Excluded: a rebuilt register,
  closures not published, an upper bound; food only; food retail by permit
  type; citywide stalls and vehicles out; hostess venues out only where the
  permit names its form.

```brief-checks
[
  {
    "id": "naha-bodik-shinki-package",
    "claim": "BODIK's record for Naha's new-permit package (shinki_syokuhin; 140 resources, cc-by-40-intl on 2026-10-11) answers a plain GET - metadata only; BODIK wants calls about 20 seconds apart",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=shinki_syokuhin",
    "min_bytes": 2000
  },
  {
    "id": "naha-bodik-keizoku-package",
    "claim": "BODIK's record for Naha's renewals package (472018_keizoku_syokuhin; 73 resources, cc-by-40-intl on 2026-10-11) answers a plain GET - metadata only; BODIK wants calls about 20 seconds apart",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=472018_keizoku_syokuhin",
    "min_bytes": 2000
  },
  {
    "id": "naha-bodik-ribiyou-package",
    "claim": "BODIK's record for Naha's barber and beauty package (472018_ribiyou; two XLSX resources named for 2026-09-04, CC BY 4.0 as stated on 2026-10-12) answers a plain GET - metadata only; BODIK wants calls about 20 seconds apart",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=472018_ribiyou",
    "min_bytes": 1000
  },
  {
    "id": "naha-isj-block-live",
    "claim": "MLIT's block-level address file for Naha (47201) answers keyless - the join target (162,904 B, downloaded 2026-10-12, owner call S29)",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/47201-24.0a.zip",
    "min_bytes": 120000
  },
  {
    "id": "naha-isj-chome-live",
    "claim": "MLIT's town-chome file for Naha (47201) answers keyless (8,025 B, downloaded 2026-10-12, owner call S29)",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/47201-19.0b.zip",
    "min_bytes": 6000
  },
  {
    "id": "naha-projected-crs",
    "claim": "Naha (centroid 127.684 E) projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 127.684,
    "expect": "EPSG:32652"
  }
]
```
