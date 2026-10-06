# Maebashi — build brief

**Band A, owner-approved 2026-10-04** (Japan's third wave; the Step 0
downloads and the licence reads approved the same night,
`docs/decisions_drafts/staging.md`, "Band A's Japanese briefs: Step 0
downloads and licence reads approved"). **Step 0 measured 2026-10-04 and
2026-10-05** (staging). Downloaded, each from its publisher's own host, into
`data/maebashi/raw/` (gitignored), named as a build's `fetch_sources.py`
names them:

- 2026-10-04: MHLW's `10201_food_business_all.csv` (1,394,571 B) from
  `i2fas.mhlw.go.jp`; MLIT's `isj/10201-24.0a.zip` (406,956 B) and
  `isj/10201-19.0b.zip` (9,199 B) from `nlftp.mlit.go.jp`.
- 2026-10-05, from `data.bodik.jp` (one `package_show` per dataset, then
  each file once, 12 s or more between requests): `syokuhin20260630.xlsx`
  (193,851 B); `seikatueiseieigyousisetuitiranr8.3.31.zip` (67,038 B); the
  monthly `sinkiseikatueiseieigyousisetuitiran_r8.{4..8}.zip` (1,677 /
  1,453 / 1,472 / 2,813 / 980 B) and
  `haigyouseikatueiseieigyousisetuitiran_r8.{4..8}.zip` (3,166 / 2,580 /
  3,073 / 4,385 / 1,170 B). Every BODIK request answered 200.

✅ **BODIK's refusal is resolved.** On 2026-10-04 BODIK answered HTTP 403
(nginx) to every call from this machine (six `package_show` calls,
23:04-23:26 local, each retried once after 60 s), the rate block wave 3's
probes met that day; nothing was fetched and no other agent, host or mirror
was tried. The owner approved a retry once the block lapsed (staging's call
9, 2026-10-05), and BODIK answered 200 to the project's agent that day.

**Run `python scripts/brief_check.py maebashi` before writing any code.**
Then the `japan-city` skill: **Fukuoka's and Utsunomiya's two-source shape**
(MHLW's file plus the city's list of the permits MHLW lacks), plus the city's
生活衛生 registers rebuilt to 2026-08 from a base list and its monthly new
and closed files. Coordinates: the `address-join` skill, measured with the
shared `pipeline/countries/japan_register.py` functions from scratch scripts
(`scripts/screen_japan_join.py` has no Maebashi entry; its table is shared
code, so add `maebashi` entries there at the build). Rail: MLIT N02-25 cut at
the N03 city line, measured through `pipeline/countries/japan.py` with a
scratch `CITIES` entry (none was added to the shared module).

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; no Shinkansen station lies inside Maebashi, so nothing is
dropped); (2) **lines served only by limited expresses DO count**
(2026-09-28); (3) **the city line only**: only stations inside the city get
rings, JR and the private lines are cut at the line, **a one-station stub
stays as cut** (2026-09-27), and an URBAN line cut to a stub goes back to the
owner; (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**:
where the trade name IS the operator's own name, the pin shows its permit
type, the operator column read in memory only (2026-09-27), **MHLW's 法人名
included for every MHLW city** (Cleanup, master, 2026-10-05; DECISIONS
"MHLW's 法人名 joins the Japanese name rule"); (6) **no page says "currently
operating"**. Also: fault-based cost clauses accepted for all of Japan
(2026-09-24); yatai count but a 露店 form is a street stall (2026-09-28,
2026-09-29); English station names from OSM `name:en`, numerals as figures
before 丁目; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Maebashi carries `label_tier: "minor"` and goes in the **Japan East** view,
as Utsunomiya and the other Kantō cities do (`app/cities.py`). Its label
offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200),
never by eye.

**`mode`: `metro`** (the owner's rule of 2026-10-02, applied as for Kurume):
no subway or tram is drawn, and JR is not the largest network inside the
city (5 station groups against the Jōmō Electric Railway's 14), so the mode
follows the backbone, the Jōmō Line, a railway (N02 class 12).

---

## The one-line summary

**Food from two sources that split by date: MHLW's 食品衛生申請等システム
file holds every permit granted since 2023-04 (1,850 open restaurant
permits, 97.9% with an address), and the city's own file holds the permits
granted before then and still in term (1,622 restaurants, permits dated
2019-10 to 2023-03-31).** They overlap by 18 restaurant permits (1.3%), and
together hold **3,454 restaurants, 97.8% of the 3,533 in force**. Personal
services: the city's registers rebuilt exactly from the 2026-03-31 base and
five months of new and closed files (every closure matched by 整理番号):
**1,279 premises at 2026-08-31** (barbers 310, beauty 830, laundries 139),
98% of the official 1,306. Block join 89.7% (MHLW), 91.6% (city food),
91.8-95.5% (registers). Rail: 19 N02 station groups inside the city (Jōmō
Line 14, JR 5), the Jōmō Line every 30 minutes by its own timetable.

---

## Business leg — two food sources, plus the 生活衛生 registers

### MHLW open data (10201)

| | MHLW 食品衛生申請等システム, 前橋市 (10201) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=10201_food_business_all.csv`: **1,394,571 B, 4,133 rows** (許可 2,394, 届出 1,723, 許可(廃業) 13, 届出(廃業) 3). UTF-8 CSV, the national schema. A plain GET |
| As of / cadence | Newest 許可年月日 **2026-08-28**; closures dated 2026-08. Monthly (MHLW) |
| Columns | 自治体コード, 行番号, 都道府県名, 市区町村名, 営業施設名称、屋号又は商号, 営業施設名称、屋号又は商号（フリガナ）, 営業の種類, **業態**, **営業施設所在地**, 営業施設方書, **緯度 / 経度**, 営業施設電話番号, **法人名**, 法人番号, 法人住所, 許可番号, 初回許可年月日, 許可年月日, 許可開始日, 許可満了日, 廃業年月日, 申請区分, 許可条件, 備考 |
| What it holds | **Only permits first granted from 2023** (open restaurant permits by 初回許可年月日: 2023 483 · 2024 537 · 2025 513 · 2026 317), and notifications |

**Counts that matter** (open restaurant permits: 許可, no 廃業年月日,
許可満了日 not before 2026-08-31):

- **1,850 open 飲食店営業 permits**, **1,812 (97.9%) with an address**, 1,811
  with MHLW's own point. No address reads only `前橋市内` (Kurume's trap is
  absent). Expiries run 2026-09-22 to 2033-06-30.
- **Fixed premises** (業態 自動車営業 173 and 仮設 101 set aside): **1,576, of
  which 1,543 (97.9%) are addressed**; of the 33 without one, 12 are 給食.
- 業態 among open restaurants: 一般飲食店 476, 自動車営業 173, 喫茶 145,
  スナック 123, 大衆酒場 107, レストラン 106, 仮設 101, めん類 94,
  カフェ・バー・キャバレー 90, 給食 85, コンビニエンスストア 57, …
- **Through `japan_eigyo`** (all live rows, step 2's order): no address 635
  (mostly notifications), not a premises 118 (addressed vehicles and stalls),
  out by rule 1,025 (manufacturing 299; hostess venues by 業態 206; temporary
  or mobile 183; institutional catering 220; vending 75; inside accommodation
  23; 仕出し 12; mail order 7); **storefronts Food service 1,141, Retail
  1,198** (Retail includes MHLW's notifications, the PARTIAL opt-in
  food-retail bucket, disclosed as in Fukuoka and Utsunomiya).

### The city's food file (`102016_eiseikensa01`)

| | 前橋市 食品等営業許可・届出施設一覧 |
|---|---|
| **Dataset** | `https://data.bodik.jp/dataset/102016_eiseikensa01`, 「食品等営業許可・届出一覧」, organisation 前橋市 (`102016`), author 健康部衛生検査課, 「１月」; `package_show` metadata modified 2026-07-09 |
| **File** | `https://data.bodik.jp/dataset/be0e8464-4b96-41f6-901d-1aa4bf11bcc0/resource/6808f251-ce78-4c09-a5d8-24a871a5d7e9/download/syokuhin20260630.xlsx`: **193,851 B, 2,117 rows**, one sheet 「食品営業許可施設（既存システム分）R8.6.30現在」 (the permits from the city's former system, **as of 2026-06-30**). Datastore-backed: `datastore_search` total 2,117 |
| **Its notes** | Use MHLW's open data, but **some permitted premises are not in that system, and those are published here** (「許可施設については一部食品衛生申請等システムの登録がない施設があります。そちらについてはエクセルファイルで掲載しています。」) |
| **Columns** | 営業の種類, **業態**, **営業所名** (the trade name), **営業所所在地**, **営業者名** (the operator), 仮設区分 (常設 2,070 / 仮設 47), 許可番号 (the city's own numbering, 1,097 distinct; not MHLW's 第…号 form), 初回許可年月日, 許可年月日, 許可開始日, 許可満了日 |
| **Dates** | Era-letter form, `H01/08/18`, `R8/09/30`. 許可年月日 **2019-10-02 to 2023-03-31**; first permits from 1988 (2020 195, 2021 663, 2022 819). 許可満了日 **2026-09-30 to 2029-12-31**: none expired by 2026-08-31, but **179 rows (160 restaurants) expire on 2026-09-30** |
| **Types** | 飲食店営業 **1,622**, 菓子製造業 171 (+2 自動車), そうざい製造業 92, 食肉販売業 46 (+8 包装食肉), 魚介類販売業 34 (+14 調理加工する, +3 せず), 麺類製造業 16, 食肉処理業 15, 漬物 10, … 喫茶店営業 3 |
| **業態** | blank 495, 一般 182, 自動車営業 152, 喫茶 132, スナック 123, めん類 111, ｺﾝﾋﾞﾆｴﾝｽｽﾄｱ 105 (half-width kana), 給食 79, 一般飲食店 73, 弁当 72, … (normalised by `japan_eigyo`'s NFKC) |
| **Through `japan_eigyo`** | Food service **970**, Retail **511**, out 636 (hostess venues by 業態 201, temporary or mobile 198, manufacturing 110, institutional 79, accommodation 26, 仕出し 18, vending 4); after the mobile flag (212: blank address 21 and vehicle types) **storefronts 1,463: Food service 957, Retail 506**. Every 仮設 row falls out |

- **The split is by date, so the claim nearly holds, measured.** MHLW holds
  no permit granted before 2023 and the city's file none after 2023-03-31.
  At block level (same town, block and normalised trade name), **18 of the
  city's 1,431 block-tier restaurant permits (1.3%) also have an MHLW
  restaurant permit**, and 19 city rows share a premises and permit type
  with an MHLW row: renewals filed through the national system while the old
  permit runs. Fukuoka's 1.3% and Utsunomiya's 1.1%, by the same mechanism.
  `SUPERSEDES` keeps one. A permit-number join is impossible (the two
  numberings differ).
- **Other co-location is different permits at one shop, not double
  counting**: 116 city Retail rows share a premises with an MHLW Retail row
  and 64 city restaurants with an MHLW notification (a konbini's restaurant
  permit beside its コンビニエンスストア notification, 59). Step 2's one pin
  per (premises, bucket) decides those.
- **Against the official count** (e-Stat 衛生行政報告例 FY2024, year end
  2025-03-31: **3,533** = old law 1,081 + revised law 2,452; through
  `japan_official.restaurants`): MHLW 1,850 + the city 1,622 = 3,472
  (98.3%), **3,454 without the overlap (97.8%)**. MHLW alone is 52%.
- **The address the map loses**: 38 of MHLW's 1,850 restaurants publish none
  (by consent), and 21 of the city's 2,117 rows have a blank address. The
  template's "About one restaurant in <n> … chose not to publish its address
  in the national filing system" bullet reads **about one in 50** (MHLW's 38).
- ⚠️ **The 2026-09-30 expiries**: the file's as-of is 2026-06-30, and 179 of
  its rows expire on 2026-09-30 (the renewals reappear in MHLW's file). Fetch
  the newest edition at build and pin `as_of` to the date it states, never
  today (Kyoto's rule), then drop the expired rows with `in_term`.

### The 生活衛生 registers (`102016_eiseikensa02`) — rebuilt to 2026-08-31

| | |
|---|---|
| **Dataset** | `https://data.bodik.jp/dataset/102016_eiseikensa02`, 「生活衛生営業施設一覧」, author 健康部衛生検査課, 「月1回」; `package_show` metadata modified 2026-09-08; 11 resources (the base zip and ten monthly zips, 2026-04 to 2026-08) |
| **Its notes** | All five 生活衛生 trades, as of 2026-03-31, plus each month's new permits and notifications and each month's closures, updated around the 10th to 15th of the next month. **Some premises are left off at the operator's request** (「事業者の要望により、一部の施設情報は掲載されないことがあります。」) |
| **Base** | `…/dataset/d66b613e-d058-4074-a343-9d86bb20381f/resource/2bd28b54-0e08-497c-9c9a-2b708a84b8aa/download/seikatueiseieigyousisetuitiranr8.3.31.zip` (67,038 B): five cp932 CSVs, 「（令和8年3月末現在）」: **理容所 313, 美容所 828, クリーニング所 150**, 公衆浴場 42, 旅館業 121 (rows with a name or address; some CSVs pad with empty comma rows) |
| **Months** | `sinki…_r8.N.zip` (new) and `haigyou…_r8.N.zip` (closed), N = 4 to 8; a trade with nothing that month is named 「該当なし」 in the folder name and has no CSV |
| **Columns (base)** | №, **整理番号**, **施設名称**, **施設所在地**, 施設電話番号, **開設者氏名** (barber, beauty) or **営業者氏名** (laundry), **法人代表者氏名**, 開設者住所（法人のみ） / 営業者住所（法人のみ）, 確認年月日, 確認証番号, 業種; laundry adds **詳細業種** (取次 82, blank 68) and 特定洗濯物の取り扱い |
| **Columns (months)** | as the base, but the operator is **営業者氏名** and the representative **代表者** (barber, beauty) or **法人代表者名** (laundry); the closed files add 廃止届出年月日 |

**The rebuild** (base + new − closed, months 2026-04 to 2026-08, keyed on
**整理番号**, unique in every base list and never blank):

| Trade | Base 2026-03-31 | New | Closed | Closures matched by 整理番号 | **Rebuilt 2026-08-31** | Official FY2024 (2025-03-31) | Share |
|---|---|---|---|---|---|---|---|
| 理容所 | 313 | 3 | 6 | 6 of 6 | **310** | 320 | 97% |
| 美容所 | 828 | 12 | 10 | 10 of 10 | **830** | 816 | 102% |
| クリーニング所 | 150 | 1 | 12 | 12 of 12 | **139** (取次 74, other 65) | 170 (取次所 99) | 82% |
| **Personal services** | **1,291** | 16 | 28 | **28 of 28** | **1,279** | **1,306** | **98%** |

- **Every closure matches a base or new row by 整理番号; none needed the
  確認証番号 or address fallback, and no new row repeats a base key.** So the
  rebuild is exact, not an upper bound (unlike Kyoto's and Higashiōsaka's,
  which cannot see closures). The months run unbroken from 2026-04 to
  2026-08. 公衆浴場 and 旅館 are rebuilt too (40, 119) but are not storefront
  types.
- **Official counts**: e-Stat 衛生行政報告例 FY2024, 生活衛生 第10表 and 第11表
  (the national per-city tables already on disk,
  `data/hakodate/raw/estat_eisei_r6_riyo_biyo_by_city.csv` and
  `…_cleaning_by_city.csv`, read here, not downloaded), row 群馬県前橋市:
  理容所 320, 美容所 816 (重複開設 1), クリーニング所 170 (取次所 99), and 無店舗取次店
  10 (not premises). The base list's own date is FY2025's year end, so
  FY2025's tables, when published, are the exact control.
- ⚠️ **Laundries read 82% of the official count** (139 against 170; 取次 74
  against 取次所 99). Twelve closed in 2026-04 to 2026-07 alone (ten in May),
  and the dataset says some premises are left off at the operator's request.
  Disclose the gap on the page with its reason unknown, as a number.
- **Three beauty rows are mobile salons** (移動 in the address and the name):
  `permits_from_rows` flags 自動車 / 無店舗 by type only and `japan_eigyo`
  reads 移動 in the TYPE (Kobe's 移動美容室), so these reach the join (town
  `移動`, unplaced). Shared code: catch 移動 in the address or name.

---

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 10201)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/10201-24.0a.zip` (406,956 B)
and `https://nlftp.mlit.go.jp/isj/dls/data/19.0b/10201-19.0b.zip` (9,199 B):
**39,355 block keys, 278 town-chōme keys.** One municipality, no wards
(`"wardless": True`). Measured with `japan_register` and `WAVE2_RULES`
unchanged (no Minato re-run needed).

| Tier | MHLW storefronts (2,339) | City food storefronts (1,463) | Barbers (310) | Beauty (830) | Laundries (139) |
|---|---|---|---|---|---|
| Block | **89.7%** (Food service 93.3%) | **91.6%** (Food service 92.3%) | **95.5%** | **91.8%** | **92.1%** |
| Town-chōme / 大字 centroid | 10.3% | 8.3% | 4.2% | 7.8% | 6.5% |
| Unplaced | 0.0% (1) | 0.1% (1) | 0.3% (1) | 0.4% (3, the mobile salons) | 1.4% (2) |

- **MHLW's own point** where the block join misses (`OWN_POINT_FALLBACK`):
  239 of MHLW's 241 non-block rows carry one, so MHLW is about 100% placed.
  MHLW's point against the block point: **median 42 m**, **92.4% within
  250 m** (2,097 rows; 32 over 1 km). The city's lists have no coordinates,
  so their chōme share stands as district-centre dots.
- **The town-chōme tier** is 地番 country whose numbers MLIT's block edition
  does not carry: 田口町, 富士見町赤城山, 朝倉町, 元総社町, 川曲町, 前箱田町, 江木町, …
  Unplaced: 上小出町 (MHLW), 表町 (city food), 駒形町東高島 (barber), 駒形町増田境
  and 総社町桜ケ丘 (laundry). Read them at build.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (10201)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_10_GML.zip`, N03 code
10201 (311.6 km²; extent W 139.0019, S 36.3162, E 139.2301, N 36.5624).
**20 station records inside, 19 `N02_005g` groups.** N02-24 and N02-25 agree
on every station here; use N02-25 (the wave's default).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 上毛線 (上毛電気鉄道, 12) | Jōmō Line (Jōmō Electric Railway) | **14 / 23** (61%) | 中央前橋, 城東, 三俣, 片貝, 上泉, 赤坂, 心臓血管センター, 江木, 大胡, 樋越, 北原, 新屋, 粕川, 膳 |
| 両毛線 (東日本旅客鉄道, 11) | JR Ryōmō Line | 4 / 19 | 新前橋, 前橋, 前橋大島, 駒形 |
| 上越線 (東日本旅客鉄道, 11) | JR Jōetsu Line | 2 / 39 | 新前橋, 群馬総社 |

- **19 station groups inside the city** (Jōmō 14, JR 5: 新前橋 is one group
  on both JR lines, its two records 0 m apart). Median gap to the nearest
  station **1,000 m** (closest pair 454 m): standard rings.
- **Stub test passes**: the Jōmō Line keeps 14 of 23 (the rest run on into
  Kiryū and Midori); the two JR lines are cut at the line as intended. No
  urban line is cut to a stub.
- **Cut at the line** (the first stations beyond it, by N03 municipality):
  Jōmō → 新里 (桐生市, 0.7 km out), 新川, 東新川 (桐生市), 赤城 (みどり市);
  Ryōmō → 伊勢崎 (伊勢崎市, 2.7 km), 国定; Jōetsu → 井野 (高崎市, 1.7 km),
  八木原 (渋川市, 2.4 km). JR's 吾妻線 trains run through 群馬総社 on the
  Jōetsu Line, but N02 files that line from 渋川: no in-city station of its
  own, so it is not drawn.
- **The Shinkansen**: no station inside (the nearest is 高崎, outside).
- **The light-rail / rail test** (the `japan-city` skill's mode rule): no
  subway, tram or light rail; all three lines are railways (classes 11 and
  12). The test reduces to whether JR is the largest network by in-city
  station groups: no (5 against 14), so `metro` on Kurume's precedent.

**Frequency, read from the operators' own timetable pages by curl
(2026-10-04):**

- **Jōmō Line** (`https://jomorailway.com/chuomaebashi.html`, the station
  page's timetable: one table, no day type stated): **37 departures** from
  中央前橋 toward 西桐生, 5:25 to 23:05; **every 30 minutes** from 10:00 to
  21:45 (:15 and :45), three an hour at 7:00 and 9:00. The timetable index
  (`https://jomorailway.com/timetable.html`) lists **23 stations**, 中央前橋
  to 西桐生, as N02 does (gate 3, checked below).
- **JR Ryōmō Line** at 前橋 (`https://timetables.jreast.co.jp/2610/timetable/tt1417/1417010.html`
  and `…/1417020.html`, weekday, the site's October 2026 data): **42**
  departures toward 桐生・小山 and **54** toward 高崎; two an hour each way at
  midday, three to five at the peaks.
- **JR Jōetsu Line** at 新前橋 (`…/tt0881/0881020.html` and `…/0881040.html`,
  weekday): **21** toward 渋川・水上 (hourly), plus **18** 吾妻線 trains
  (`…/0881010.html`) over the same track through 群馬総社, so about two an
  hour there; **82** toward 高崎.
- Nothing inside the city runs less often than hourly. No frequency floor
  applies to JR or private lines in Japan (the master list's row).
- ⚠️ **Gate 3** for JR (JR East's own station lists) and **OSM `name:en`**
  for the 19 groups at build (no OSM was queried for this brief: no Overpass
  at Step 0). `心臓血管センター` is a name OSM may translate (Fukuoka's trap):
  read every name.

## Scope

**Maebashi City (10201), one municipality, no wards.** The Jōmō Line runs on
into Kiryū and Midori, the Ryōmō Line into Isesaki, the Jōetsu Line into
Takasaki and Shibukawa; cut at the line, the stations beyond named by N03
municipality at build (`excluded_stations.csv`).

## Licences — as declared (the full reads are separate)

- **The city's food file (`102016_eiseikensa01`)**: BODIK's `package_show`
  (2026-10-05) declares **`cc-by-40-intl`, Creative Commons Attribution 4.0
  International**; author and maintainer 健康部衛生検査課.
- **The city's 生活衛生 registers (`102016_eiseikensa02`)**: `package_show`
  declares **`cc-by-21-jp`, Creative Commons Attribution 2.1 JP**; author and
  maintainer 健康部衛生検査課.
- **MHLW open data**: PDL 1.0, PERMITTED WITH CONDITIONS, as recorded for the
  built Japanese cities (`docs/data_sources/japan.md`; `fukuoka.md`):
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  naming this project as the processor; no completeness or accuracy claim;
  no logo; the minor 免責 2)ウ point stays open.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **MLIT N03**: CC BY 4.0, ⛔ never
  drawn.
- **The full reads of the two BODIK datasets are a separate `licence-read`
  agent per source, running in parallel; staging records their verdicts.**
  This brief states only what the records declare; BODIK's terms and whether
  the city has its own open-data terms are for those reads.

## Privacy

Read only the trade name, the permit type (and 業態), the premises address
and MHLW's lat/lon. **No row value was printed or stored for this brief**:
every count below comes from in-memory comparisons.

- **MHLW's file**: in Maebashi's file **法人名 carries sole traders' own
  names**: of 4,117 live rows, 3,462 fill it, 1,957 with a company or
  cooperative marker, and 1,482 with neither a marker nor a 法人番号 (nearly
  all 3 to 5 characters, the shape of a personal name). **Answered**: MHLW's
  法人名 now joins the shared name rule for every MHLW city (Cleanup, master,
  2026-10-05). Here it flags **19 rows whose trade name equals 法人名, 5 of
  them open restaurants**. 法人番号, 法人住所 (filled on 270 rows) and the phone
  are never selected. So the page takes the standard name-rule bullet for
  both lists, not "the ministry's list does not say who the operator is".
- **The city's food file**: the operator column is **営業者名**, already in
  `japan_register.OPERATOR_COLS`; filled on 2,096 of 2,117 rows, 1,042 with a
  company or cooperative marker. The rule flags **3 rows (2 restaurants)**.
  ⚠️ Its trade-name column **営業所名** is NOT in `NAME_COLS` (which has
  営業所名称): add it at build, or every row reads with no name and the rule
  compares nothing; then the Minato control.
- **The registers**: operators in **開設者氏名** (barber, beauty base),
  **営業者氏名** (laundry base, all monthly files), with **法人代表者氏名**,
  **代表者** and **法人代表者名** for a company's representative; all already
  in `OPERATOR_COLS`. 開設者氏名 is filled on every row and mostly a person's
  own name (barbers: 295 of 313 without a company marker). The rule flags
  **0 rows** in the rebuilt registers. **開設者住所（法人のみ） and
  営業者住所（法人のみ）** (companies' addresses only, filled on 18 / 161 / 89
  rows) and every phone are never selected.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map:
  it must see the 19 MHLW, 3 food-file and any register rows the rule flags,
  per premises (step 2's spread rule) across both food lists and the
  registers.

## Region

`"region": "Japan East"`, `"country": "Japan"`, `label_tier: "minor"`.
Project to **UTM 54N (EPSG:32654)**: the city's centre lies at longitude
139.13 and its western edge at 139.0019, both inside the 138-144 band
(computed here, never copied).

**Scaffold**: `scaffold_city.py --slug maebashi --name Maebashi
--system-name "Jōmō Electric Railway and JR East" --taxonomy japan_eigyo
--lat 36.389 --lon 139.063 --region "Japan East" --country Japan --mode
metro --page-number <N>` (`--dry-run` first), with the page number claimed
in `docs/session_roles.md` at build, not here. A `japan.CITIES` entry:
`"maebashi": {"name": "前橋市", "pref": "10", "epsg": 32654, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["10201"]}`.

## Owner calls

**Made:** Band A (owner, 2026-10-04); the Step 0 downloads and the two
licence reads (owner, 2026-10-04); the BODIK retry once the rate block lapsed
(owner, staging's call 9, 2026-10-05: resolved, every file fetched); MHLW's
法人名 in the name rule for every MHLW city (Cleanup, master, 2026-10-05);
the standing Japanese calls above; the minor label tier and the Japan
sub-region (owner, 2026-10-02); `metro` by the owner's mode rule of
2026-10-02 (staging's reading, as Kurume's).

✅ **Answered (owner, 2026-10-05; `docs/decisions_drafts/staging.md`):**
build the laundries and state the share ("14. build and state"), citing the
dataset's own note that some premises are withheld at the operator's request
(「事業者の要望により、一部の施設情報は掲載されないことがあります」) as a stated
cause, never as the whole of the gap. **Licences** (read 2026-10-05, the
drafts): the food file CC BY 4.0 under the city's terms; the registers
labelled CC BY 2.1 JP against the terms' 4.0, so **one credit names both**
(owner, call 29); the 他者の権利 bullet on the city's open-data page binds and
the name rule meets it (call 21); on notice, remove the credit if the city
asks (2.1 JP 第5条). The address columns 住所（法人のみ） are never selected.

**Was open:**

1. **Laundries at 82% of the official count** (139 against FY2024's 170).
   Recommendation: build them as they stand and disclose the share on the
   page as a number ("the city's register lists 139 laundries; the national
   count a year earlier was 170"), with no reason given, since the dataset
   says some premises are withheld at the operator's request and the cause
   cannot be split from closures. Tradeoff: an honest but visibly thin
   laundry layer, against leaving laundries off and calling the bucket
   barbers and beauty salons only (Hiroshima-style narrowing), which hides a
   source that is otherwise exact. Barbers (97%) and beauty (102%) need no
   call.

## What the build must still measure

- The Fukuoka config shape: `SOURCES` (mhlw, food, barber, beauty,
  laundry), `SUPERSEDES` (the 18 restaurant permits in both lists),
  `OWN_POINT_FALLBACK` and `ADDRESS_BY_CONSENT` for MHLW, `SOURCE_AS_OF` per
  source (MHLW's month; the food file's stated date; the registers'
  2026-08-31), and a `source_rows` for the registers that applies base + new
  − closed by 整理番号 (shared code: `rebuilt_register` cannot apply closures;
  a closure-aware sibling, keyed by a declared column, with the unmatched
  closures counted and a nonzero count stopping the build).
- ⚠️ **Shared code**, each with the Minato control re-run: `NAME_COLS` +=
  営業所名; `wareki_date` (and so `in_term`) must read the era-letter form
  `R8/09/30` / `H01/08/18`, which it returns as None today (every one of the
  food file's 2,117 expiries), so `in_term` would keep everything; 移動 in an
  address or name as not a premises (3 beauty rows).
- The food file's newest edition at build (179 rows expire 2026-09-30), its
  as-of pinned to what it states.
- Gate 3 against JR East's station lists; OSM `name:en` for 19 groups;
  line colours on both basemaps.
- ⚠️ **The Economic Census join control** (`scripts/japan_census_control.py`,
  after step 2): the 2021 census has **1,299** 飲食店 establishments in 10201.
  Before de-duplication 2,098 Food service storefronts (MHLW 1,141, the city
  957), **1.62 per establishment**, inside the built cities' 1.56-1.92.
- The 菓子 / そうざい factory share, printed by step 2.
- FY2025's 衛生行政報告例 tables, when e-Stat publishes them, as the exact
  control for the registers' 2026-03-31 base.

```brief-checks
[
  {
    "id": "maebashi-mhlw-live",
    "claim": "MHLW's open-data file for Maebashi City (10201) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=10201_food_business_all.csv",
    "min_bytes": 1000000
  },
  {
    "id": "maebashi-food-package",
    "claim": "BODIK's record for the city's food dataset declares cc-by-40-intl and still points at syokuhin20260630.xlsx (the 2026-06-30 edition; a newer file name means re-measure)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=102016_eiseikensa01",
    "present": ["\"license_id\": \"cc-by-40-intl\"", "syokuhin20260630.xlsx", "6808f251-ce78-4c09-a5d8-24a871a5d7e9"]
  },
  {
    "id": "maebashi-mhlw-terms-pdl",
    "claim": "MHLW's site terms still apply PDL 1.0 to the open data",
    "kind": "http_contains",
    "url": "https://i2fas.mhlw.go.jp/termsofuse.htm",
    "present": ["PDL1.0"]
  },
  {
    "id": "maebashi-food-rows",
    "claim": "The city's food file (permits from its former system, as of 2026-06-30) holds 2,117 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "6808f251-ce78-4c09-a5d8-24a871a5d7e9",
    "expect": 2117
  },
  {
    "id": "maebashi-isj-live",
    "claim": "MLIT's block-level address file for Maebashi City (10201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/10201-24.0a.zip",
    "min_bytes": 300000
  },
  {
    "id": "maebashi-life-package",
    "claim": "BODIK's record for the 生活衛生 dataset declares cc-by-21-jp and lists the 2026-03-31 base zip and the new and closed files through 2026-08 (r8.8)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=102016_eiseikensa02",
    "present": ["\"license_id\": \"cc-by-21-jp\"", "seikatueiseieigyousisetuitiranr8.3.31.zip", "sinkiseikatueiseieigyousisetuitiran_r8.4.zip", "haigyouseikatueiseieigyousisetuitiran_r8.4.zip", "sinkiseikatueiseieigyousisetuitiran_r8.8.zip", "haigyouseikatueiseieigyousisetuitiran_r8.8.zip"]
  },
  {
    "id": "maebashi-jomo-23-stations",
    "claim": "The Jōmō Electric Railway's timetable index links all 23 station pages, 中央前橋 (chuomaebashi) to 西桐生 (nishikiryu), as N02 has 23 (gate 3), and its printable up and down timetables. ASCII strings only: the page sends no charset, so the check reads it as Latin-1 and cannot match Japanese text (the 30-minute frequency on chuomaebashi.html was read by curl, 2026-10-04)",
    "kind": "http_contains",
    "url": "https://jomorailway.com/timetable.html",
    "present": ["chuomaebashi.html", "joto.html", "mitumata.html", "katakai.html", "kamiizumi.html", "akasaka.html", "center.html", "egi.html", "oogo.html", "higoshi.html", "kitahara.html", "araya.html", "kasukawa.html", "zen.html", "niisato.html", "nikkawa.html", "higashinikkawa.html", "akagi.html", "kiryukyujo.html", "tennojuku.html", "fujiyamashita.html", "maruyamashita.html", "nishikiryu.html", "images/timetable/nobori02_1.pdf", "images/timetable/kudari02_1.pdf"]
  },
  {
    "id": "maebashi-jr-stations-indexed",
    "claim": "JR East's own timetable site indexes 新前橋's four directions (Agatsuma, Jōetsu down, Ryōmō down, Jōetsu up), where the JR frequencies were read; ASCII link paths only, as above",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list0881.html",
    "present": ["tt0881/0881010", "tt0881/0881020", "tt0881/0881030", "tt0881/0881040"]
  },
  {
    "id": "maebashi-projected-crs",
    "claim": "Maebashi projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.13,
    "expect": "EPSG:32654"
  }
]
```
