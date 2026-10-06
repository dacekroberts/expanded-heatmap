# Koshigaya — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5: `docs/decisions_drafts/staging.md`, "Wave 5, second half: calls 95 to
141", call 103), on the city's own 保健所 lists. **Koshigaya City (越谷市,
11222) is a core city with its own health centre**: Saitama Prefecture's
food layers and 生活衛生 lists (Tokorozawa's, Kasukabe's, Sōka's and Ageo
(Regional)'s sources) do not cover it, and the master list row says so.

The Step 0 downloads were approved by the owner 2026-10-06 (calls 106, 141,
147). **Step 0 measured 2026-10-06** (staging). Into `data/koshigaya/raw/`
(gitignored), each from its publisher's own host with the project
user-agent through `japan_fetch.get`, each HTTP 200, under each URL's own
file name:

- From `www.city.koshigaya.saitama.jp` (保健医療部 生活衛生課), page
  `/kurashi_shisei/fukushi/hokenjo/shokuhin/20160401.html` (食品関係営業施設一覧,
  ページ番号 8077, 更新日 2026-09-10): the full food list
  `r8.3.31koukai.xls` (**1,362,944 B**) and the monthly files
  `r8.apr.syokuhin.xls` (53,248 B), `r8.may.syokuhin.xls` (49,664 B),
  `r8.june.syokuhin.xls` (52,736 B) and `r8.aug.syokuhin.xls` (40,960 B).
  ⚠️ **The page's July link (令和8年7月分) serves August's file**: both links
  point at `r8.aug.syokuhin.xls`, whose 26 permits are all granted in
  2026-08. **No July 2026 file was obtainable** (open call 2).
- From the same host, page `/kurashi_shisei/fukushi/hokenjo/kankyo/jouhouteikyou.html`
  (営業施設一覧, ページ番号 7235): `riyou.xls` (80,896 B), `biyou.xls`
  (192,000 B), `kurini.xls` (59,392 B). Not the inn, theatre or bath lists.
- From `i2fas.mhlw.go.jp`: `11222_food_business_all.csv` (397,550 B), a
  control.
- From `nlftp.mlit.go.jp`: `isj/11222-24.0a.zip` (290,262 B) and
  `isj/11222-19.0b.zip` (7,755 B).

**2,587,407 B in all, 11 files.** Nothing else was downloaded. Timetable
pages were read for counts only (Rail).

**Run `python scripts/brief_check.py koshigaya` before writing any code.**
Then the `japan-city` skill, **Fukuyama's shape** (a city's own full food list
plus the months since, `rebuilt_register`; `docs/build_briefs/fukuyama.md`)
with **Ichinomiya's merge** (the full list kept whole plus the months, owner
2026-10-06, call 126; `docs/build_briefs/ichinomiya.md`), Hamamatsu's for the
registers. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Koshigaya entry and was not edited).
Rail: MLIT N02-25 cut at the N03 city line, through
`pipeline/countries/japan.py` with an in-memory `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none runs here); (2) **lines served only by limited expresses
DO count** (2026-09-28); (3) **the city line only**: only stations inside the
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
clauses accepted for all of Japan (2026-09-24); food-retail notifications
count where a list publishes them, disclosed (the `japan_eigyo` docstring,
Tokyo's rule); English station names from OSM `name:en`; every Japanese city
reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ The precedents set 2026-10-06, applied here (do not re-ask):** the full
list kept whole plus its monthly files (call 126); MHLW's permits missing
from the city's files left out (126-127); MHLW's own point where the block
join misses (127c, `OWN_POINT_FALLBACK`); low-frequency stretches drawn and
named (86: none here); tiers disclosed where the block share is low (145: not
needed, 96.0%).

**✅ Licence (owner, 2026-10-06, call 142):** the PDL 1.0 record on Saitama
Prefecture's portal for these exact pages is relied on over the city site's
copyright page (Hiroshima's shape). See Licences.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Koshigaya carries `label_tier: "minor"` and goes in the **Japan East** view
with the other Kantō cities (wave 4's first city to land retags Japan into
the eight regions, Koshigaya into **Kanto**). Its label offset comes from
`check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`** by the owner's rule of 2026-10-02 and Sōka's and
Kasukabe's precedent: the backbone is one private heavy-rail line (Tōbu, N02
class 12, 6 of 8 groups), with JR East's Musashino Line (2 groups); no
subway, tram or light rail.

---

## The one-line summary

**Food and personal services from the city's own XLS lists (PDL 1.0 on the
prefecture portal's records, relied on, call 142).** The food list of permits
and notifications on 2026-03-31 holds **4,567 rows: 3,095 permits and 1,472
notifications**; **2,493 restaurants (飲食店営業), 92.7% of e-Stat's 2,690 in
force**, old-law permits included (554 restaurants; not Kurashiki's trap).
The monthly files carry new permits AND renewals (97 of their 166 restaurant
rows renew a full-list premises), July 2026 is missing (the link serves
August), and the full list kept whole plus the months gives **2,562
restaurant rows (95.2%)**, 2,524 once a renewal replaces its premises' old
row. Barbers 225, beauty salons 645 and laundries 124 as of 2026-10-02:
**99.1%, 103.9% and 91.9% of official**. Block join **96.0%** (food), 96.0 to
97.7% (registers); unplaced 0.2 to 0.8%. MHLW holds 209 of the city's
permits (cover 0.06): a control and a point source, nothing added. **Rail: 8
station groups** (Tōbu Skytree Line 6, JR Musashino Line 2), frequencies
read from both operators: the thinnest station, 大袋, has 111 and 115
weekday departures (about 6 an hour midday); no stretch near 11 a day.

---

## Business leg — the city's 保健所 lists

Host `https://www.city.koshigaya.saitama.jp` (the city's own CMS; no
catalogue API; **sends no charset**, so checks use ASCII anchors). Every file
is a plain GET under each page's `files/` folder. Both pages say the
operators' own addresses and phones are removed for individuals
(「個人の申請者住所・申請者電話番号等は削除」), so the operator NAME columns remain
(Privacy).

### Food: 食品関係営業施設一覧

| File | Bytes | Rows | What it is |
|---|---|---|---|
| `r8.3.31koukai.xls` 令和8年3月31日現在営業許可（届出）を受けている施設 | **1,362,944** | **4,567** | permits in term and notifications on 2026-03-31 (one sheet, `Sheet1`; an empty `Sheet3`) |
| `r8.apr.syokuhin.xls` (2026-04) | 53,248 | 70 (50 restaurants) | the month's new permits, renewals and notifications |
| `r8.may.syokuhin.xls` (2026-05) | 49,664 | 58 (38) | |
| `r8.june.syokuhin.xls` (2026-06) | 52,736 | 73 (60) | |
| `r8.aug.syokuhin.xls` (2026-08; also behind the 7月分 link) | 40,960 | 34 (18) | |

- **Old BIFF `.xls`** (`city_rows` reads it through xlrd; header on row 1).
  Dates are wareki with padding (`R 8. 3.31`, `R8. 4. 1`), which
  `wareki_date` reads; **30 grant dates and 105 first-application dates in
  Shōwa (`S6x. …`) do not parse**, all on out-of-bucket types (給食施設 and
  その他の製造業) for the grant date, so nothing in a bucket depends on them.
- **One schema** (all five files): **許可番号**, **業種**, **種目**, **屋号**,
  **営業所所在地**, 営業所電話番号, **申請者名**, **代表者名（法人）**, 申請者住所,
  申請者電話番号, 初回申請（届出）月日 (年月日 in the months), **許可年月日**,
  **終了年月日**.
- **Permits and notifications in one list**: 3,095 rows carry a 許可番号 (all
  with a grant date), 1,472 do not. The unnumbered rows are the notification
  types: その他の食料・飲料販売業 503, 集団給食施設 188, cup vending 176,
  コンビニエンスストア 149, 百貨店、総合スーパー 80, 乳類販売業 61, 野菜果物販売業 48,
  other vending 44, 給食施設 40, 包装食肉 21, 弁当販売業 18, 米穀類販売業 6 …;
  they have no end date. By the module's standing rule the food-retail
  notifications count, in Retail (907 rows after de-duplication).
- **種目** is the form: その他 1,135, 一般食堂・レストラン 653, 自動車 229, 菓子製造
  225, 各種食料品小売業 219, 集団給食施設 188, cup vending 176, **カフェバーキャバレー
  160**, 菓子小売業 154, コンビニエンスストア 149, 中華料理屋 102, 特定の食品 83 …
  `WAVE2_RULES`' `form_cols` reads it (`FORM_COLS` holds 種目), so vehicles,
  catering, hotel restaurants and the hostess sub-type leave through
  `FORM_RULES`.
- **Addresses**: 4,197 start 埼玉県越谷市; **366 read 市内一円** (vehicles 229,
  特定の食品 83, 各種食料品小売業 13, 行商 9 …: `mobile` takes them by 一円);
  4 are blank (無店舗小売業 3). None outside the city.
- **The page's notes**: some premises are not listed at the operator's
  request (「事業者の要望により、一部の施設情報は掲載されていません」); new
  permits and notifications appear on the 10th to 15th of the next month. It
  says nothing about closed premises.
- **許可番号 is not unique**: 928 distinct numbers among 3,095 permits, a
  short serial reused by type and year; (number, grant date) gives 2,884.
  Never key on the number alone.

**Against `japan_register`'s tuples (shared code, not edited here):**
`ADDR_COLS` 営業所所在地, `NAME_COLS` 屋号, `TYPE_COLS` 業種, `FORM_COLS` 種目
under `form_cols`, `OPERATOR_COLS` 申請者名 are read; **代表者名（法人）** is not
in `OPERATOR_COLS` (it holds 代表者名). `rebuilt_register` takes
`end_col="終了年月日"`, `granted_col="許可年月日"` (not its defaults), and **drops
every row with no end date** (it keeps `(end or 1900-01-01) >= as_of`): the
1,472 notifications and 76 numbered rows (old-law 給食施設 60, その他の製造業 14,
器具 2) would vanish. See What the build must still measure.

### Old law, duplicates, renewals and closed premises

- **The list carries every old-law permit still in term** (Kurashiki's trap
  is absent): 783 numbered rows (**554 restaurants**) granted before
  2021-06-01, ending 2026 (395) and 2027 (312), 76 with no end (給食施設 and
  manufacturing). e-Stat counted 884 old-law restaurants on 2025-03-31;
  those ending in FY2025 have left the list or renewed under the revised
  law. Old-law types appear (喫茶店営業 14).
- **Only permits in term on its date**: one permit ends before 2026-03-31
  (2025-09-30); 253 (201 restaurants) end before 2026-08-31.
- **Repeats**: 105 rows repeat an (address, trade name, type) in 50 groups;
  3,762 distinct (address, trade name) premises. One pin per premises (trap
  7) takes them.
- **The monthly files carry renewals as well as new permits** (unlike
  Iwaki's): of their 235 rows, **118 sit at a full-list premises of the same
  type, and that premises' full-list permit ends by 2026-10-31** (115; 3 have
  no end); none repeats a full-list (number, grant date), so a renewal takes
  a new number. Restaurants: 69 at new premises, 97 renewals. Renewals arrive
  in the month the old permit ends or the month before (April 26 of 27 and
  so on).
- **The July gap shows in the renewals**: of the full-list permits ending in
  each month of 2026, a month file renews April 27 of 52, May 24 of 60, June
  39 of 76, **July 9 of 64** (all nine renewed early, in June), August 13 of
  35. July's renewals (and July's new permits) are in no file.
- **Closures since 2026-03-31 are invisible**: no closure file and no status
  column. MHLW cannot test them (its 209 permits are 7% of the city's).

### Counts against the official stock

e-Stat 衛生行政報告例 FY2024 (`japan_official.estat()`; the `…_5-2-1_oldlaw`
and `…_5-4-1_newlaw` tables), 埼玉県越谷市, 飲食店営業 in force 2025-03-31:
**2,690** (old law 884, revised 1,806).

| | Restaurants (飲食店営業) | Share of 2,690 |
|---|---|---|
| Full list, 2026-03-31 (rows) | **2,493** | 92.7% |
| (a) Full list whole plus the months' new premises (rows; renewals replace) | **2,562** | 95.2% |
| (a) as `rebuilt_register` keys it (one row per address, name, type; `as_of` 2026-03-31) | 2,524 | 93.8% |
| (b) Fukuyama's: in term on 2026-08-31 | 2,415 | 89.8% |
| MHLW's open restaurant permits (control) | 170 | 6.3% |

Through `japan_eigyo` (merge (a), the notifications kept, `WAVE2_RULES`):
**Food service 2,059, Retail 1,330** (of it 907 notifications), out 1,240;
fixed premises in a bucket **3,265 (Food service 1,977, Retail 1,288)**.
Restaurant permits out by rule: **temporary or mobile 221** (種目 自動車, 市内一円),
**the hostess rule 177** (種目 カフェバーキャバレー), 仕出し 60, inside
accommodation 16. Other out rows: institutional catering 290, vending 252,
manufacturing types with no rule 207, mail order 5. **Economic Census
control** (`japan_official.census()`, 2021): **1,095** 飲食店 establishments
in 11222; 1,975 distinct Food-service premises is **1.80 per
establishment**, inside the built cities' 1.56-1.92. Factory proxy: 32 of
1,288 Retail trade names contain 工場 or センター (2.5%, Kobe's 4.9%); step 2
measures it properly.

### MHLW's file (11222), the control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11222_food_business_all.csv`:
**397,550 B, 1,111 rows** (届出 899, 許可 209, closed 3), the national
schema; permits granted 2021-09-10 to 2026-08-18. The coverage sweep's
cover is **0.06** (`docs/coverage_sweep/japan_universe_mhlw.csv`: 170 open
restaurants).

- **144 of its 209 permits are city permits** by the number's digits and the
  grant date. The other 65 (52 restaurants, granted 2021-11 to 2026-08) are
  in no city file: left out (calls 126-127).
- **Nine permits granted in July 2026** (8 restaurants, all with MHLW's own
  point), 3 at a city premises by (address, name). Too few to stand in for
  the missing July file (open call 2).
- **Its own coordinates**: block point against MHLW's point, **median 56 m,
  95.8% within 250 m** (595 rows; 1 over 1 km). Its addressed rows join
  90.0 / 4.1 / 5.9 (block / chōme / none).
- **899 notifications, 492 addressed** (Retail 463 by type): the city's own
  list already publishes notifications (1,472 rows), so they are not a
  missing layer here (open call 3).

### Personal services: 営業施設一覧, as of 2026-10-02

| File | Bytes | Rows | Kinds | Official (FY2024) | Share |
|---|---|---|---|---|---|
| `riyou.xls` 理容所営業施設一覧 | **80,896** | **225** | 理容 | 227 | **99.1%** |
| `biyou.xls` 美容所営業施設一覧 | **192,000** | **645** | 美容 | 621 | **103.9%** |
| `kurini.xls` クリーニング所営業施設一覧 | **59,392** | **124** | 取次 91 · 一般 33 | 135 (取次所 98, 指定洗濯物 7) | **91.9%** |

(Official from `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
`…_cleaning_by_city.csv`, 埼玉県越谷市; 無店舗取次店 operators none.)

- **The page's heading**: 「営業施設一覧(令和8年10月2日現在)」 (its 更新日 reads
  2026-09-02; the beauty list holds a 2026-09-14 date, so the files postdate
  that). New permits appear by the end of the next month. No monthly files.
- **Columns**: 業態, (laundry only) **種別**, 確認年月日 (ISO, slashes),
  **施設_名称**, **施設_所在地**, 施設_電話番号, **申請者_氏名**, 代表者_氏名,
  申請者_所在地. One sheet each.
- **A standing register**: 確認年月日 runs 1964 to 2026 (barbers 1965-2026,
  beauty to 2026-09-14, laundries to 2025-09-18). No closure note, no status
  column. 2 premises appear in both the barber and beauty lists; 1 beauty
  premises repeats.
- **Laundries 91.9%**: 一般 33 of 37, 取次 91 of 98. Built and stated as
  elsewhere above 90% (Ichihara's 81% built and stated, call 123); the gap
  is the list's (operator requests are noted only on the food page).
- **Shared code**: `NAME_COLS` 施設_名称, `ADDR_COLS` 施設_所在地, `TYPE_COLS`
  種別 (laundry); `OPERATOR_COLS` holds 申請者_氏名 but **not 代表者_氏名**. One
  file per kind: `source_rows` per file so `japan_eigyo`'s source decides
  (Fukuyama's). 取次 is a counter, not 無店舗: it counts.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11222-24.0a.zip` (290,262 B,
50,216 rows, **46,358 block keys**), town-chōme `.../19.0b/11222-19.0b.zip`
(7,755 B, **199**). `japan.CITIES` entry at build: `"koshigaya": {"name":
"越谷市", "pref": "11", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES,
"wardless": True, "wards": ["11222"]}`.

| Tier (merge (a), fixed premises in a bucket) | All (3,265) | Food service (1,977) | Retail (1,288) |
|---|---|---|---|
| Block | **96.0%** | 95.9% | 96.3% |
| Town-chōme / 大字 centroid | 3.7% | 4.0% | 3.3% |
| Unplaced | **0.2%** | 0.1% | 0.5% |

| Registers | Barbers (225) | Beauty (645) | Laundries (124) |
|---|---|---|---|
| Block / chōme / unplaced | 96.9 / 2.7 / 0.4 | 97.7 / 1.6 / 0.8 | 96.0 / 3.2 / 0.8 |

**The misses, read** (towns only, by `measure.py` in the scratchpad):
- **Chōme tier**: 弥生町 26 (MLIT keys 24 points there; the rows' block
  numbers are not among them), 大竹 12, レイクタウン八丁目 8 and 二丁目 8 (a
  new district; MLIT's 24.0a lacks some of its blocks), 南越谷四丁目 5, the
  大字 増森, 大里 and 大泊 (字 塚田) 5 each: 地番 MLIT does not list.
- **Unplaced (7 food rows)**: 増林城ノ上 4 (a 小字 written without 字), 川柳 2,
  千間台東 1; registers 七左町 4, 相模町 2, 大間野 1.
- MHLW's own point (127c) covers the matched permits among the chōme and
  unplaced rows; nothing more is needed at 96%.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_11_GML.zip`, N03 code 11222
(**60.2 km²**, extent W 139.745, S 35.855, E 139.840, N 35.959). Read with
`stub_test()` and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 伊勢崎線 (東武鉄道, 12) | **Tōbu Skytree Line** | **6 / 55** | 蒲生, 新越谷, 越谷, 北越谷, 大袋, せんげん台 (south to north) |
| 武蔵野線 (東日本旅客鉄道, 11) | **JR Musashino Line** | **2 / 27** | 南越谷, 越谷レイクタウン (west to east) |

- **8 station records, 8 N02_005g groups**; none shared. **南越谷 (JR) and
  新越谷 (Tōbu) are separate groups 132 m apart**: different names, an
  interchange by footway, kept apart as MLIT keeps them (the skill's trap 1,
  Tarumi / Sanyo Tarumi); their rings overlap. No other pair under 700 m.
  **Median nearest-station gap 1,295 m** (132 to 2,809): rings by the spacing
  rule at build.
- **Shinkansen**: none in the city.
- **Cut at the line**: the Skytree Line south at 新田 (草加市) and north at 武里
  (春日部市); the Musashino Line west at 東川口 (川口市) and east at 吉川 (吉川市).
  N02 files the Skytree Line as 伊勢崎線; the public name inside Koshigaya is
  the Tōbu Skytree Line (浅草 / 押上 to 東武動物公園).
- **The light-rail/rail test**: both heavy rail (N02 classes 12 and 11). No
  subway, tram, monorail or light rail.
- **The stub test passes**: the Musashino Line has 2 stations inside (unlike
  Tokorozawa's one-station stub).
- **Frequency, read 2026-10-06 from each operator's own timetable** by plain
  GET, every departure counted (marked trains included):

  | Station (line, direction) | Weekday departures | Per hour 10:00-15:59 |
  |---|---|---|
  | 新越谷 (Skytree, to 浅草 / to 伊勢崎) | 282 / 296 | 11-13 / 12 |
  | 越谷 (Skytree, each way) | 280 / 296 | 12 |
  | せんげん台 (Skytree, to 浅草 / to 伊勢崎) | 211 / 213 | 12 |
  | 北越谷 (Skytree, to 浅草 / to 伊勢崎) | 182 / 115 | 6 |
  | 蒲生 (Skytree, to 浅草 / to 伊勢崎) | 130 / 138 | 6 |
  | **大袋** (Skytree, to 浅草 / to 伊勢崎) | **111 / 115** | 5-6 |
  | 南越谷 (Musashino, to 西船橋 / to 府中本町) | 132 / 134 | 6 |
  | 越谷レイクタウン (Musashino, each way) | 131 | 6 |

  Tōbu's counts from its NAVITIME-hosted timetable
  (`transfer-internal.navitime.biz/tobu/pc/diagram/BusDiagram?linkId=00000798&nodeId=…`;
  node ids 蒲生 00001273, 新越谷 00004178, 越谷 00000721, 北越谷 00008280,
  大袋 00005686, せんげん台 00000072, from the service's own station index);
  JR East's from `timetables.jreast.co.jp` (南越谷 1482, 越谷レイクタウン 1722,
  the 2610 edition; one 特急 鎌倉 and three しもうさ号 among 南越谷's). **No stretch
  comes near about 11 trains a day** (call 86). Only counts are recorded,
  never a timetable on the page. **Staging's correction**: the master list
  row's Tōbu figure (about 6 an hour at local stations, ASSERTED from 谷塚) is
  now READ at 大袋, 蒲生 and 北越谷.
- ⚠️ **Gate 3** at build: Tōbu's 6 and JR East's 2 stations inside. **OSM
  `name:en`** for 8 groups (one Overpass query at build; not queried here).

## Scope

**Koshigaya City.** The Skytree Line runs on to 草加, 北千住 and 浅草 south
(through-running to the Hibiya and Hanzōmon lines) and to 春日部 north; the
Musashino Line to 府中本町 and to 西船橋 and 東京: cut at the line. Personal
services carries all three registers. The inn, theatre and bath lists on the
same page are not taken (no built Japanese city carries them).

## Licences — read 2026-10-06 (staging records)

As staging recorded the read (`docs/decisions_drafts/staging.md`, "Wave 5,
second half" and the briefs entry, call 142): **PERMITTED WITH CONDITIONS**.
Saitama Prefecture's open-data portal carries PDL 1.0 records for these exact
pages: dataset 530 【越谷市】食品営業許可・届出一覧 (resource 2715, linking the food
page) and dataset 2004 【越谷市】営業施設一覧 (resource 6312, linking the
registers page), each 「公共データ利用規約第1.0版（PDL1.0）」. The city site's
copyright page reads differently; **the portal record is relied on** (owner,
call 142, Hiroshima's shape). Conditions as read: **the portal's
processed-use credit**, naming the creator section (越谷市 保健医療部
生活衛生課), the resource names and their URLs, and saying the data was
processed; a **fault-based own-cost clause** (accepted for all of Japan,
2026-09-24). Staging words the credit from its record; this brief does not.

- **MHLW open data** (control and the 127c point): PDL 1.0 as recorded in
  `docs/data_sources/japan.md`, its 出典 line and who processed it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census: measurement
  sources, not drawn. **Tōbu's and JR East's timetables**: read for counts
  only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The food lists carry the operator block**: **申請者名** (no company or co-op
  marker on **1,592 of 4,567** full-list rows, the shape of a sole trader's own
  name; 108 of 235 monthly rows), **代表者名（法人）**, 申請者住所, 申請者電話番号
  and 営業所電話番号. As the page says, the operator's address and phone are
  blank for individuals: 32 rows with no known marker keep one (30 of them
  also name a 代表者 under 法人, so they read as organisations). Step 2 never
  reads any of them into an output; 申請者名 and 代表者名（法人） are read IN
  MEMORY for the name rule only (add the second to `OPERATOR_COLS`).
- **The registers carry 申請者_氏名** (no marker on barbers 189 of 225, beauty
  406 of 645, laundries 72 of 124), 代表者_氏名, 申請者_所在地 (blank for
  individuals but 1) and 施設_電話番号. Select 施設_名称, 施設_所在地 and 種別
  only.
- **The name rule, version 2, measured in memory** (answers only, never a
  value): full list **5** rows whose trade name is the operator's own name
  (shared `OPERATOR_COLS`; **7** with 代表者名（法人） compared too), **1** bare
  personal name; months 1; merge (a) **2 flagged among fixed premises in a
  bucket**, 0 of them bare; registers **0** (0 bare); MHLW's 法人名 1. No
  value was printed or stored.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected.
- Run `check_personal_exposure.py koshigaya` (`japan=True`) after step 2: the
  rows that matter are the sole traders' trade names; it must print 0. Record
  the verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kanto after the retag), `"country": "Japan"`,
`label_tier: "minor"`. Project to **UTM 54N (EPSG:32654)**: the N03 centroid
lies at longitude 139.790, the extent 139.745 to 139.840, inside the 138-144
band (computed here, never copied). OSM box from the N03 extent, rounded out:
(35.85, 139.74, 35.96, 139.85).

**Scaffold**: `scaffold_city.py --slug koshigaya --name Koshigaya
--system-name "Tōbu Railway and JR East" --taxonomy japan_eigyo --lat 35.901
--lon 139.790 --region "Japan East" --country Japan --mode metro
--page-number <N>` (`--dry-run` first), the page number claimed at build from
`docs/session_roles.md`, not here.

## Owner calls

**Made (do not re-ask):** Band A (owner, 2026-10-06, call 103); the PDL
record relied on (call 142); the Step 0 downloads (calls 106, 141, 147); the
standing Japanese calls above; `mode: metro`; the minor tier and Japan East
(Kanto); no frequency floor (call 46); the full list kept whole plus the
months (126); MHLW's extra permits left out (126-127); MHLW's own point
where the join misses (127c); notifications in Retail (the module's standing
rule). **By precedent, noted for its size**: 種目 カフェバーキャバレー is a
combined sub-type naming cabarets, out whole as Tokyo's バー・キャバレー is
(owner, 2026-09-29; `docs/category_rules.md`, adult and hostess venues): 177
restaurant permits, 7% of them.

**Weighed, each with a recommendation:**

1. **The food share on the page** (call 125's question). The list holds
   92.7% of e-Stat's restaurants (95.2% with the months), and the city says
   some premises are withheld at the operator's request. *Recommend no share
   sentence*, on Hirakata's reading (call 125 is for a list below about
   90%): name the withholding in the businesses bullet, as the page's own
   note. Tradeoff: the 5-7% gap stays unquantified on the page; if the owner
   wants it, Ichinomiya's sentence shape carries "about 19 restaurants in 20
   of the official count".
2. **The missing July 2026 file.** (a) **Re-read the food page at build**: if
   a July file is linked by then, fetch it (it is on the approved page) and
   merge it; if not, state the months as "April to June and August 2026".
   (b) Take MHLW's nine July permits in its place. *Recommend (a)*: MHLW
   holds 7% of the city's permits, so its July is not the city's July, and
   call 126-127 leaves MHLW's extra permits out. Tradeoff: under (a) July's
   new premises (about 20 to 40, from the other months' 34-73 rows) are
   missing until the city fixes its link, and the July-ending permits stay on
   the map on their March row (merge (a) keeps them; the method (b) of
   Fukuyama would wrongly drop about 55 of them).
3. **MHLW's notifications** (precedent 127b, re-weighed). *Recommend leaving
   them out*: the city's own list already publishes notifications (1,472
   rows, Retail 907), so MHLW's 492 addressed notifications would mostly
   double them; 127b answered cities whose lists have none. Tradeoff: any
   notification MHLW holds and the city omits is lost (not measurable here
   beyond 169 of 899 matching by exact address and name).

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `OPERATOR_COLS` + 代表者名（法人） and 代表者_氏名; **`rebuilt_register`
  keeping rows with no end date** (`in_term`'s rule, "a row with no readable
  expiry is kept"), opt-in, or the notifications given their own source key
  by blank 許可番号 so they bypass it (either way the 907 Retail notifications
  must reach step 2; measure Higashiōsaka's drift if the shared rule
  changes); `end_col` / `granted_col` passed from the config; optionally
  `wareki_date` for Shōwa `S` (not needed here).
- `as_of` pinned to **2026-03-31** for merge (a), never today; no key on
  許可番号 alone; the food list's date stated as 2026-03-31 with new permits
  and renewals to 2026-08-31 (open call 2 decides the months' wording).
- The registers' date stated as 2026-10-02 (the page's heading).
- Gate 3 (Tōbu 6, JR East 2), OSM `name:en`, line colours on both basemaps
  (Tōbu's Skytree Line and the Musashino Line's orange), the 南越谷 / 新越谷
  ring overlap read on the render, the opening view (`map-view`), the
  factory share, the Economic Census control (estimated 1.80),
  `check_provenance.py`, `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "koshigaya-food-page",
    "claim": "The food page offers the 2026-03-31 full list and the April, May, June and August 2026 monthly files, and no July or September file (the July link serves r8.aug.syokuhin.xls). ASCII anchors only: the host sends no charset. A failure on an absent string means a July or a newer month appeared: fetch and re-measure",
    "kind": "http_contains",
    "url": "https://www.city.koshigaya.saitama.jp/kurashi_shisei/fukushi/hokenjo/shokuhin/20160401.html",
    "present": ["r8.3.31koukai.xls", "r8.apr.syokuhin.xls", "r8.may.syokuhin.xls", "r8.june.syokuhin.xls", "r8.aug.syokuhin.xls"],
    "absent": ["r8.jul", "r8.sep"]
  },
  {
    "id": "koshigaya-env-page",
    "claim": "The 営業施設一覧 page offers the barber, beauty and laundry lists (as of 2026-10-02). ASCII anchors only (no charset sent)",
    "kind": "http_contains",
    "url": "https://www.city.koshigaya.saitama.jp/kurashi_shisei/fukushi/hokenjo/kankyo/jouhouteikyou.html",
    "present": ["files/riyou.xls", "files/biyou.xls", "files/kurini.xls"]
  },
  {
    "id": "koshigaya-food-full-live",
    "claim": "The full food list (1,362,944 B, 4,567 rows on 2026-10-06) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://www.city.koshigaya.saitama.jp/kurashi_shisei/fukushi/hokenjo/shokuhin/files/r8.3.31koukai.xls",
    "min_bytes": 1300000
  },
  {
    "id": "koshigaya-food-aug-live",
    "claim": "The August 2026 monthly food file (40,960 B, 34 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.koshigaya.saitama.jp/kurashi_shisei/fukushi/hokenjo/shokuhin/files/r8.aug.syokuhin.xls",
    "min_bytes": 30000
  },
  {
    "id": "koshigaya-barber-live",
    "claim": "The barber list (80,896 B, 225 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.koshigaya.saitama.jp/kurashi_shisei/fukushi/hokenjo/kankyo/files/riyou.xls",
    "min_bytes": 60000
  },
  {
    "id": "koshigaya-beauty-live",
    "claim": "The beauty list (192,000 B, 645 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.koshigaya.saitama.jp/kurashi_shisei/fukushi/hokenjo/kankyo/files/biyou.xls",
    "min_bytes": 150000
  },
  {
    "id": "koshigaya-laundry-live",
    "claim": "The laundry list (59,392 B, 124 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.koshigaya.saitama.jp/kurashi_shisei/fukushi/hokenjo/kankyo/files/kurini.xls",
    "min_bytes": 40000
  },
  {
    "id": "koshigaya-portal-food-record",
    "claim": "Saitama Prefecture's portal resource 2715 (dataset 530) records the city's food page under PDL 1.0: the record relied on (owner, call 142)",
    "kind": "http_contains",
    "url": "https://opendata.pref.saitama.lg.jp/resources/2715",
    "present": ["PDL1.0", "hokenjo/shokuhin/20160401.html"]
  },
  {
    "id": "koshigaya-portal-env-record",
    "claim": "Saitama Prefecture's portal resource 6312 (dataset 2004) records the city's registers page under PDL 1.0 (call 142)",
    "kind": "http_contains",
    "url": "https://opendata.pref.saitama.lg.jp/resources/6312",
    "present": ["PDL1.0", "hokenjo/kankyo/jouhouteikyou.html"]
  },
  {
    "id": "koshigaya-mhlw-live",
    "claim": "MHLW's open-data file for Koshigaya (11222), the control, answers a plain keyless GET (397,550 B, 1,111 rows on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=11222_food_business_all.csv",
    "min_bytes": 300000
  },
  {
    "id": "koshigaya-isj-block-live",
    "claim": "MLIT's block-level address file for Koshigaya (11222) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/11222-24.0a.zip",
    "min_bytes": 250000
  },
  {
    "id": "koshigaya-isj-chome-live",
    "claim": "MLIT's town-chōme file for Koshigaya (11222) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/11222-19.0b.zip",
    "min_bytes": 6000
  },
  {
    "id": "koshigaya-tobu-ofukuro",
    "claim": "Tōbu's timetable for 大袋, Skytree Line toward 浅草 (111 weekday departures on 2026-10-06), the thinnest station in the city",
    "kind": "http_contains",
    "url": "https://transfer-internal.navitime.biz/tobu/pc/diagram/BusDiagram?linkId=00000798&nodeId=00005686&updown=0",
    "present": ["大袋", "スカイツリーライン"]
  },
  {
    "id": "koshigaya-jr-minamikoshigaya",
    "claim": "JR East's timetable index for 南越谷 (1482) links its two weekday Musashino Line pages (132 and 134 departures on 2026-10-06). ASCII anchors only",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1482.html",
    "present": ["tt1482/1482010.html", "tt1482/1482020.html"]
  },
  {
    "id": "koshigaya-jr-laketown",
    "claim": "JR East's timetable index for 越谷レイクタウン (1722) links its two weekday Musashino Line pages (131 each way). ASCII anchors only",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1722.html",
    "present": ["tt1722/1722010.html", "tt1722/1722020.html"]
  },
  {
    "id": "koshigaya-projected-crs",
    "claim": "Koshigaya projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.790,
    "expect": "EPSG:32654"
  }
]
```
