# Fujisawa — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 4, banded in staging's wave
5, call 113: `docs/decisions_drafts/staging.md`, "Wave 5, second half"). The
Step 0 downloads were approved by the owner 2026-10-06 (call 147). **Step 0
measured 2026-10-06** (staging). Into `data/fujisawa/raw/` (gitignored), each
from its publisher's own host with the project user-agent, each HTTP 200,
under each URL's own file name as `japan_fetch.get` saves:

- From `www.city.fujisawa.kanagawa.jp` (健康医療部 生活衛生課, 藤沢市保健所),
  page 28905: the full food list in two files, **companies**
  `zende-ta202606houjin.csv` (606,748 B) and **individual operators**
  `zende-ta202606kojin.csv` (341,236 B), as of 2026-06-30; the six monthly
  CSVs `shokuhin2026{06,07,08}{houjin,kojin}.csv` (37,496 B together). Page
  32931: the barber, beauty and laundry lists as of 2026-06-30,
  `20260713103834.csv` (21,889 B), `20260713104008.csv` (101,611 B),
  `20260713104127.csv` (18,338 B).
- From `i2fas.mhlw.go.jp`: `14205_food_business_all.csv` (480,077 B), the
  control.
- From `nlftp.mlit.go.jp`: `isj/14205-24.0a.zip` (174,323 B) and
  `isj/14205-19.0b.zip` (7,896 B).

**1,789,614 B in all, 14 files.** Nothing else was downloaded: not the PDF
twins, not the registers' monthly CSVs (five files of 1 to 3 KB, not named in
the approval; the next quarterly list carries them). **Added 2026-10-06
under call 160**: the 統計年報 2025's health chapter,
`11roudoushakaihoshouhokeneisei_r7.pdf` (1,924,927 B, the same host), for the
official counts ("Counts against the official stock").

**Run `python scripts/brief_check.py fujisawa` before writing any code.** Then
the `japan-city` skill, **Yokosuka's shape** (the same Kanagawa permit system:
業種 with 詳細業種 as the form; `docs/build_briefs/yokosuka.md`) with
**Ichinomiya's merge** (the full list kept whole plus the months, owner
2026-10-06, call 126; `docs/build_briefs/ichinomiya.md`), Hamamatsu's for the
registers (one file per kind). Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Fujisawa entry; its table is shared
code and was not edited). Rail: MLIT N02-25 cut at the N03 city line, read
from the cached zips with a scratch script.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none stops in the city); (2) **lines served only by limited
expresses DO count** (2026-09-28); (3) **the city line only**: only stations
inside the city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27); an URBAN line cut to ONE station
is left out, its station kept through the other lines, and drawn cut only
where no other line serves that station (owner, 2026-10-06, calls 54 and 92);
(4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory share
measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**, version 2
(2026-10-06): a bare personal name is withheld whatever the operator column
holds; (6) **no page says "currently operating"**. Also: no frequency floor
for JR or private lines in Japan (owner, 2026-10-06, call 46), any stretch at
about 11 trains a day or fewer named and drawn (call 86); fault-based cost
clauses accepted for all of Japan (2026-09-24); English station names from
OSM `name:en`; every Japanese city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Rail scope (owner, 2026-10-06, call 113, the band row):** Odakyū 9,
Enoden 6, JR Tōkaidō 2 and the Shōnan Monorail 2 (drawn cut); **Sōtetsu's
one-station stub at 湘南台 kept as cut** (a private line, standing call 3);
**the Blue Line's one station (湘南台) left out**, its station kept through
Odakyū and Sōtetsu (an urban line, calls 54 and 92).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Fujisawa carries `label_tier: "minor"` and goes in the **Japan East** view;
wave 4's first city to land retags Japan into the eight regions, Fujisawa
into **Kantō**. Its label offset comes from `check_macro_labels.py` (PROBLEMS
0 at 375, 768 and 1200), never by eye.

**✅ `mode`: `metro`** on Yokosuka's precedent (owner, 2026-10-02, "a
private-heavy-railway backbone"): Odakyū's Enoshima Line holds 9 of the 17
groups, with JR East's Tōkaidō Line and Enoden (N02 class 12, a railway, not
a tramway); no subway station is drawn (the Blue Line is left out) and no
tram.

---

## The one-line summary

**All three buckets from the city's own CSVs (CC BY 4.0 by the city's
open-data terms, use counting as acceptance, as stated; the licence read is
pending, staging records it).** The food list of every permit held on
**2026-06-30** comes in two files, companies 2,629 rows and **individual
operators 1,897** (no operator name in that file at all); **4,526 permits,
3,611 restaurants (飲食店営業) plus 179 vehicles**, old-law permits included
(826 rows granted 2019-07 to 2021-08: not Kurashiki's trap). The monthly files
carry renewals as well as new permits; the full list kept whole plus July and
August (call 126): **4,579 permits, 3,654 restaurants**. **No per-city
official count exists** (Fujisawa is neither a designated nor a core city):
3,790 restaurant permits per 2021 census establishment is **2.54**, the
bottom of the four e-Stat-listed Kanagawa cities' **2.52-2.87** (an estimate,
not a share; the city's 統計年報 2025 carries no food-permit table, measured
2026-10-06). Barbers 203, beauty salons 821, laundries 140 (+2 storeless) as
of 2026-06-30, **102.0%, 104.3% and 94.7%** of the city's official counts at
2025-03-31 (199, 787, 150; 統計年報 2025, table 135). Through `japan_eigyo`: **Food service 2,887, Retail 638**
fixed premises; census control **1.90**. Block join **98.6%** (food), 99.5%
(barbers, beauty), 96.4% (laundry), **unplaced 0**. MHLW holds 272 of the
city's open permits (271 in its files) and 979 notifications (592 addressed).
**Rail: 17 station groups** (Odakyū 9, Enoden 6, JR 2, the Monorail 2, 湘南台
and 藤沢 shared); JR every 8-9 minutes and Enoden every 14 (read), Odakyū
ASSERTED: nothing near 11 trains a day.

---

## Business leg — the city's 生活衛生課 lists

Host `https://www.city.fujisawa.kanagawa.jp` (the city's own CMS; no
catalogue API). Every file is a plain GET under `/documents/<page id>/`. The
host sends `text/html` with no charset (checks use ASCII anchors). The city's
open-data library (page 13230, `kyoso/shise/kekaku/kakushu/datalibrary.html`)
lists both pages under 掲載データ一覧.

### Food: 食品衛生法に基づく営業許可施設情報, page 28905

Page `https://www.city.fujisawa.kanagawa.jp/seiei/shokuhineisei/opendatabase.html`
(更新日 2026-09-18): 「食品衛生法に基づく営業許可施設（短期許可を除く）の一覧を掲載しています。」
Two sections: 営業許可を取得した施設（毎月更新・直近3ヵ月分）, with
「前回の許可から継続して同一許可を受けた施設も含みます。」, and
営業許可を取得している全施設（3ヵ月ごと更新）.

| File (under `/documents/28905/`) | Bytes | Rows | What it is |
|---|---|---|---|
| `zende-ta202606houjin.csv` 2026年6月末現在（法人） | **606,748** | **2,629** | every permit a company holds on 2026-06-30; quarterly |
| `zende-ta202606kojin.csv` 2026年6月末現在（個人） | **341,236** | **1,897** | every permit an individual holds on 2026-06-30; quarterly |
| `shokuhin202606{houjin,kojin}.csv` | 15,246 | 42 + 30 | June's permits; all 72 already in the full list by number |
| `shokuhin202607{houjin,kojin}.csv` | 11,148 | 27 + 29 | July's permits, new and renewed |
| `shokuhin202608{houjin,kojin}.csv` | 11,102 | 30 + 23 | August's permits (施行日 to 2026-08-31) |

- **Encoding**: cp932, no BOM, LF line ends; header on line 1. Dates
  `YYYY/MM/DD 0:00:00`. Last-Modified 2026-07-15 (full lists), 2026-07-15 to
  2026-09-18 (months).
- **Columns, companies**: **営業所名1**, **営業所所在地1**, 営業所所在地2 (the
  building), 営業所電話番号1, **申請者法人名**, **申請者名**, **業種**,
  **詳細業種**, **許可番号**, **施行日**. **Individuals**: the same without
  申請者法人名 and 申請者名: **no operator column at all**. No expiry column
  and no status column.
- **業種 carries the law**: revised-law types are numbered (`１飲食店営業`,
  `１１ 菓子製造業`, `１飲食店営業（自動車）`), old-law types are not
  (`飲食店営業`, `喫茶店営業`); `japan_eigyo.normalise` strips the number.
  **詳細業種 is the form** (full lists: 飲食店 1,911, 屋台型臨時営業 301,
  簡易な営業 211, 給食 182 among companies …), read as the form by `WAVE2_RULES`' `form_cols` (`FORM_COLS`
  holds 詳細業種), Yokosuka's shape.
- ⚠️ **Combined forms**: unlike Yokosuka's, a 詳細業種 cell can join several
  forms with 、 (`飲食店、仕出し屋、弁当屋`). 312 fixed restaurant rows carry
  one; the first-match FORM rules decide them (open call 1).
- **許可番号** `第YYYY-NNN-NNNN`, unique across both files (4,526 distinct);
  its year agrees with 施行日's on 3,387 rows. A renewal takes a new number.
- **Against the shared tuples:** 営業所所在地1 is in `ADDR_COLS`, 業種 in
  `TYPE_COLS`, 詳細業種 in `FORM_COLS`, 申請者名 in `OPERATOR_COLS`. **`NAME_COLS`
  lacks 営業所名1** (and the registers' 営業所名): without it every trade name
  reads empty and the name rule compares nothing. The scratch measurement
  renamed it in memory; the build adds both to the shared tuple (or a
  `source_rows` in the config) and re-runs the Minato control.
- **The files are renamed each edition** (`zende-taYYYYMM…`,
  `shokuhinYYYYMM…`), and the page keeps only the latest three months:
  `japan_fetch.current_url` takes a `SOURCE_LINKS` regex per key (Kawasaki's
  and Otsu's precedent); `as_of` is the date in the link text, never today.

### Old law, duplicates and closed premises

- **Old-law permits are in the list** (Kurashiki's trap is absent): 826 rows
  (691 restaurants, 8 喫茶店営業, 60 菓子, 23 魚介類販売, 19 食肉販売 …),
  施行日 **2019-07-09 to 2021-08-29** (2019 108, 2020 392, 2021 326; the
  months to 2021-08 are applications made before the law changed). None
  begins before 2019-07-09, seven years before the list's date: permits
  granted earlier have run out, as a list of permits held should show.
  Revised-law 施行日 run 2021-06-01 to 2026-06-30.
- **Renewals take a new number at the same premises**: of July's and August's
  109 rows, **55 sit at a full-list (address, trade name, type)**, 50 of them
  replacing an old-law permit granted 2019-2020; none keeps its number. 54
  are new premises (44 restaurants).
- **Repeats**: 134 rows repeat an (address, trade name, type) in 59 groups (9
  of them vehicles or stalls; 17 an old-law and a revised-law permit side by
  side, a renewal overlapping its predecessor; 29 of the 50 fixed groups
  differ in 詳細業種). 4,077 distinct (address, trade name). One pin per
  premises and bucket (trap 7) takes them.
- **Closures are not marked**; the full list says 営業許可を取得している全施設 and
  appears quarterly, so a closed premises presumably leaves at the next
  edition. **MHLW marks 6 permits closed in August 2026; all 6 are in the June
  list** (open call 2). The page keeps "may include closed premises".

### The merge (Ichinomiya's, call 126)

The full list kept whole; a July or August row at a full-list (address,
trade name, type) replaces the older row, any other is added; June's rows are
already in. **4,579 permits** (56 replaced): **3,654 restaurants + 184
vehicles**, 8 喫茶店営業 (656 old-law restaurant and café permits left).

### Counts against the official stock

**No per-city official count**: e-Stat's 衛生行政報告例 carries prefectures,
designated cities and core cities only, and Fujisawa (a 保健所政令市) is
neither (`docs/coverage_sweep/japan_universe_mhlw.csv` has no official count
for 14205). The Kanagawa row includes every health-centre city, so no
prefecture-wide sum can be built from one city's list either.

**An estimate from the census and four Kanagawa peers** (e-Stat FY2024 in
force, vehicles included, per 2021 Economic Census 飲食店 establishment,
`japan_official.estat()` and `census()`):

| | Restaurant permits | Census establishments | Per establishment |
|---|---|---|---|
| Yokosuka (core city) | 3,461 | 1,373 | 2.52 |
| Yokohama | 29,358 | 11,021 | 2.66 |
| Sagamihara | 5,100 | 1,850 | 2.76 |
| Kawasaki | 12,073 | 4,212 | 2.87 |
| **Fujisawa, the list on 2026-06-30** | **3,790** (3,611 + 179 vehicles) | **1,495** | **2.54** |

Fujisawa's list sits at the bottom of the peers' range: at the peers' rates
it would hold **88% to 101%** of the city's stock. An estimate, not a share;
the page states no coverage percentage.

**The yearly report (call 160), read 2026-10-06: no food count.** The city
host publishes no 保健所 事業年報 or 保健所年報 (the five 健康医療部 section
pages, the food-inspection page, the sitemap and a web search, 2026-10-06).
Its equivalent, the city's 統計年報 2025年版 (page
`/bunsho/shise/toke/nenpo/2025.html`, 更新日 2026-03-27), splits by chapter;
chapter 11 (労働・社会保障・保健・衛生) was fetched as the one approved file:
`/documents/35832/11roudoushakaihoshouhokeneisei_r7.pdf`, **1,924,927 B**,
HTTP 200, Last-Modified 2026-03-27, into `data/fujisawa/raw/`. Its
health-centre tables are 135 環境衛生施設の状況 (below) and vital
statistics; **it has no food-permit table**, so the merge's 3,654 restaurants
(2026-08-31) and the June list's 3,611 have no official count to divide by,
and the estimate above stands. Leads, each a further document the owner
would approve: the health centre's food-inspection plan and results
(`/documents/9695/keikaku_1.pdf`, 令和8年度監視指導計画, and
`/documents/9695/r7jissikekka.pdf`, 令和7年度実施結果), which commonly state
the permitted-premises count; Kanagawa's 衛生統計年報 (the yearbook's source
for its vital statistics), on the prefecture's host.

### Counts through `japan_eigyo` (merge, fixed premises)

**Food service 2,887** (restaurant 2,879, café 8), **Retail 638** (菓子 336,
deli 156 (153 by 詳細業種), fishmonger 77, butcher 69). Out 1,054: temporary
or mobile 498 (stalls 屋台型臨時営業 and vehicles; the full list's 484 rows
addressed 藤沢市内一円 are all among them), institutional catering 218 (給食),
event catering (仕出し) 107, **snack bars 51** (詳細業種 スナック), inside
accommodation 31, vending 26, manufacturing with no rule 123. 詳細業種
簡易な営業 (221 restaurant permits after the merge, the simplified permit for
light service) stays Food service as a restaurant.

- **One pin per (address, trade name, bucket): 3,396** (Food service 2,846,
  Retail 550).
- **Economic Census control** (`scripts/japan_census_control.py` at build):
  2,846 distinct placed Food-service premises against **1,495** 飲食店
  establishments is **1.90 per establishment**, inside the built cities'
  1.56-1.92, at its top.
- **Factory proxy**: 14 of 638 Retail trade names contain 工場 or センター
  (2.2%, under Kobe's 4.9%); step 2 measures it properly.
- **No konbini or supermarket** in the city's list: their notifications are
  MHLW's (below).

### MHLW's file (14205), the control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=14205_food_business_all.csv`:
**480,077 B, 1,267 rows** (届出 979, 許可 272, 届出(廃業) 10, 許可(廃業) 6), UTF-8
with BOM, the national schema; every row 自治体コード 014205, 市区町村名 藤沢市.
Permits granted 2021-07-05 to 2026-08-26. The coverage sweep's
`placeable_of_official` reads **0.11**: MHLW holds about 6% of the city's
permits.

- **Its permits are the city's**: 271 of 272 open permits match a city file
  by number (the dashes normalized); the one that does not is a restaurant
  granted in August 2026 (read it at build). 208 open restaurant permits, 166
  addressed.
- **Its 6 closed permits** (all closed 2026-08) are all in the June list
  (open call 2).
- **Its own coordinates against the block point**: median **39 m**, 94.2%
  within 250 m (773 rows; 19 over 1 km). Its 825 addressed rows join 93.7 /
  3.9 / 2.4 (block / chōme / none).
- **979 open notifications, 592 addressed**: by `japan_eigyo` **Retail 372**
  (その他の食料・飲料販売業 243, 百貨店・総合スーパー 62, 乳類販売 47,
  コンビニ 21, 弁当販売 18, 野菜果物 16 …), out 220 (集団給食 89, vending 46,
  coffee roasting 18 …). Hundreds of addressed rows: **the partial Food-shops
  layer applies on precedent** (call 127b), with MHLW's own point where the
  block join misses (call 127c).

### Personal services: 環境営業施設, page 32931

Page `https://www.city.fujisawa.kanagawa.jp/seiei/kankyouopendate.html`
(更新日 2026-09-29): 営業している全施設（3ヵ月ごと更新）, with the published
items listed (営業所名, 営業所所在地, 営業所電話番号（携帯電話番号を除く）,
申請者名（法人にあっては、申請者名及び代表者名）, 種目（クリーニング所のみ）,
確認番号, 確認年月日), and the months' newly confirmed premises (直近3ヵ月分,
not fetched).

| File (under `/documents/32931/`) | Bytes | Rows | Kind |
|---|---|---|---|
| `20260713103834.csv` 理容所一覧 2026年6月末現在 | **21,889** | **203** | barbers |
| `20260713104008.csv` 美容所一覧 2026年6月末現在 | **101,611** | **821** | beauty salons |
| `20260713104127.csv` クリーニング所一覧 2026年6月末現在 | **18,338** | **142** | 種目 取次 93 · 一般 47 · 無店舗 2 |

- **cp932, CRLF**, header on line 1. Columns: No., **営業所名**,
  **営業所所在地**, 営業所電話番号, **申請者名**, **代表者名**, (laundry:
  **種目**), 確認番号, 確認年月日 (`YYYY年M月D日`). File names are timestamps,
  so `SOURCE_LINKS` must find each file by its section and link text, not a
  name pattern (build item).
- **Standing registers**: 確認年月日 run 1940s to 2026 (beauty: 328 in the
  2020s, 269 in the 2010s). The page calls them premises in business,
  refreshed quarterly; no closure note, no status column.
- **No repeat within a kind** (barber 0, beauty 0, laundry 2 rows); **19
  premises in both the barber and beauty lists**: one pin per premises and
  bucket.
- **Shared code**: 営業所所在地 is in `ADDR_COLS`; **営業所名 is not in
  `NAME_COLS`** (above); no type column, so the config names the kind per
  file (`SOURCE_KIND`). **The laundry list's 種目 must reach the type**
  (`japan_eigyo` reads 無店舗 from the type for personal sources, and
  `permits_from_rows`' mobile test reads `TYPE_COLS` only): a `source_rows`
  mapping, or the 2 無店舗 rows show as premises.
- **Against the census and the peers** (no per-city official count; e-Stat
  FY2024 第10表 and 第11表, per 2021 census `78_洗濯・理容・美容・浴場業`
  establishment: Yokosuka 897, Sagamihara 1,437, Fujisawa 862):

  | | Yokosuka | Sagamihara | Fujisawa (list) |
  |---|---|---|---|
  | Barbers | 259 (0.29) | 477 (0.33) | 203 (0.24) |
  | Beauty salons | 736 (0.82) | 1,073 (0.75) | 821 (0.95) |
  | Barbers + beauty | 995 (1.11) | 1,550 (1.08) | 1,024 (1.19) |
  | Laundries (取次 included) | 148 (0.17) | 238 (0.17) | 142 (0.16) |

  Together and for laundry, Fujisawa sits with its peers; the split leans to
  beauty salons. Nothing suggests a thin list.
- **Against the city's official counts** (統計年報 2025年版, table 135
  環境衛生施設の状況, 各年度末現在, source 藤沢市保健所 生活衛生課; the
  latest year is FY2024, so **2025-03-31**, fifteen months before the lists'
  2026-06-30):

  | | Official, 2025-03-31 | List, 2026-06-30 | Share |
  |---|---|---|---|
  | Barbers | 199 | 203 | **102.0%** |
  | Beauty salons | 787 | 821 | **104.3%** |
  | Laundries (取次 included) | 150 (取次 99) | 142 (取次 93); 140 without the 2 無店舗 | **94.7%** (93.3% fixed) |

  The prior years: barbers 201 and 198, salons 767 and 795, laundries 167
  and 161 (FY2022, FY2023). Shares over 100% are the date gap (salons grew
  by 28 and fell by 8 in the two years shown), not a list wider than the
  register.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/14205-24.0a.zip` (174,323 B,
**14,596 block keys**), town-chōme `.../19.0b/14205-19.0b.zip` (7,896 B,
**209**). `japan.CITIES` entry at build: `"fujisawa": {"name": "藤沢市",
"pref": "14", "epsg": 32654, "n02": "25", "rules": WAVE2_RULES, "wardless":
True, "wards": ["14205"]}`.

| Tier, today's shared code | Block | Town-chōme / 大字 | Unplaced |
|---|---|---|---|
| Food, merge, fixed premises in a bucket (3,525) | **98.6%** | 1.4% | **0.0%** |
| … Food service (2,887) / Retail (638) | 98.7 / 98.3 | 1.3 / 1.7 | 0 / 0 |
| … the individual operators' rows (1,534) | 99.5 | 0.5 | 0 |
| Barbers (203) | **99.5%** | 0.5% | 0 |
| Beauty salons (821) | **99.5%** | 0.5% | 0 |
| Laundries (140, storeless out) | **96.4%** | 3.6% | 0 |

**The misses, read** (towns only): the chōme tier is 大字 addresses whose
地番 MLIT lacks (藤沢 12, 片瀬 5, 石川 4, 高倉 4, 菖蒲沢 3, 長後 3, 遠藤 3, 用田
2, 葛原 2), the rural north and the old village cores; they take the 大字's
centroid. **No row is unplaced**, and no shared join rule is needed. The block
share is high, so call 145's tier disclosure does not arise.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_14_GML.zip`, N03 code 14205
(**69.5 km²**, extent W 139.394, S 35.296, E 139.517, N 35.429). Read with a
scratch `rail.py` (stations within the polygon, Shinkansen operator class
out).

| N02 line (operator; railway class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 江ノ島線 (小田急電鉄; 12) | Odakyū Enoshima Line | **9 / 17** | 湘南台, 長後, 六会日大前, 善行, 藤沢本町, 藤沢, 本鵠沼, 鵠沼海岸, 片瀬江ノ島 |
| 江ノ島電鉄線 (江ノ島電鉄; 12) | Enoshima Electric Railway (Enoden) | **6 / 15** | 藤沢, 石上, 柳小路, 鵠沼, 湘南海岸公園, 江ノ島 |
| 東海道線 (東日本旅客鉄道; 11) | JR Tōkaidō Line | **2 / 46** | 藤沢, 辻堂 |
| 江の島線 (湘南モノレール; 14) | Shōnan Monorail | **2 / 8** | 目白山下, 湘南江の島 |
| 相鉄いずみ野線 (相模鉄道; 12) | Sōtetsu Izumino Line | **1 / 8** | 湘南台 |
| 1号線 (横浜市; 12) | Yokohama Municipal Subway Blue Line | **1 / 17** | 湘南台 (left out) |

- **21 station records, 17 N02_005g groups**: 湘南台 (Odakyū, Sōtetsu, Blue
  Line; spread 46 m) and 藤沢 (Odakyū, JR, Enoden; 191 m). No name in two
  groups. **Median nearest-group gap 690 m** (96 to 2,749); **7 pairs under
  600 m**, all at the coast (江ノ島 Enoden and 湘南江の島 Monorail **96 m**,
  separate N02 groups; 片瀬江ノ島 468 m from 江ノ島; 石上 and 柳小路 574 m):
  rings by the spacing rule at build.
- **Shinkansen**: none in the city.
- **Cut at the line** (named by N03 municipality at build): Odakyū 8 beyond
  (大和市 6, 相模原市 2); Enoden 9 (鎌倉市); the Monorail 6 (鎌倉市, to 大船);
  JR 44 (Yokohama, Kawasaki, 平塚, 小田原 and beyond); Sōtetsu 7 (横浜市).
- **The light-rail/rail test**: Odakyū, Enoden and Sōtetsu are N02 class 12
  (railways), JR class 11; Enoden is a railway by law and by N02 class, not a
  tramway (no class-21 track). The Monorail is class 14 (suspended monorail).
  No tram or light rail.
- **The stub test**: **Sōtetsu keeps 1 station of 8**, 湘南台, its terminus,
  1.18 km of track inside: a private line, so it stays as cut (standing call
  3, the band row). **The Blue Line keeps 1 of 17**, 湘南台, its terminus,
  1.18 km inside: an urban line, so it is left out and 湘南台 keeps its ring
  through Odakyū and Sōtetsu (calls 54 and 92, the band row); the page names
  it under The lines. **The Monorail keeps 2 of 8** (0.99 km inside; 目白山下
  48 m from the city line): not a one-station stub, **drawn cut** (the band
  row). Odakyū, Enoden and JR are lines cut at the line, not stubs.
- **Frequency, read 2026-10-06** by plain GET with the project user-agent
  (only counts recorded, never a timetable on the page):

  | Station (line, direction) | Weekday departures | 10:00-15:59 |
  |---|---|---|
  | 辻堂 (JR Tōkaidō, toward 小田原, `tt1008/1008010`) | 162 | 7 an hour (every 8-9 min) |
  | 辻堂 (JR Tōkaidō, toward 東京, `tt1008/1008020`) | 157 | 7 an hour |
  | 石上 (Enoden, to 藤沢 / to 鎌倉) | 76 / 76 | 25 / 26 (every 14 min) |

  JR East's pages (`timetables.jreast.co.jp/timetable/list1008.html` and its
  2610 weekday pages, cached by the wave-5 probe) were read whole, every
  departure cell counted (marked trains included: here every cell carries a
  minute span, so the probe's reader and a whole-page reader agree). Enoden's
  station page (`enoden.co.jp/train/station/ishigami/time-table/`, the first
  timetable block). **The Monorail** (every 7-8 minutes) was read by the
  wave-5 probe from the operator's 西鎌倉 PDF; its minutes carry no text
  layer, so it is not re-counted here. **Odakyū and Sōtetsu: ASSERTED** (both
  serve station timetables through `transfer.navitime.biz`, which answered
  403 to the project agent; Odakyū's station PDF carries no text layer).
  **No stretch is near 11 trains a day** (call 86).
- ⚠️ **Gate 3** at build: each operator's own station count inside the city
  (Odakyū 9, Enoden 6, JR 2, the Monorail 2, Sōtetsu 1). **OSM `name:en`** for
  17 groups (one Overpass query at build, in the box below; not queried
  here).

## Scope

**Fujisawa City.** Odakyū runs on to 大和 and 相模大野, Enoden and the
Monorail to 鎌倉 and 大船, the Tōkaidō Line to 横浜 and 小田原, Sōtetsu to
横浜; cut at the line. The Blue Line is not drawn (its one station's ring
comes from Odakyū and Sōtetsu).

## Licences — as stated; the read is pending (`licence-read`, staging records it)

**As stated**: neither dataset page carries a licence line. The city's
open-data library (page 13230, 更新日 2026-06-09) lists both pages and says
「データの利用をもって本規約の内容を承諾したものとみなします。」; its terms,
`https://www.city.fujisawa.kanagawa.jp/documents/13230/riyoukiyaku20250401.pdf`
(156,986 B), §3(2): 「本サイトで公開しているデータの著作権は、クリエイティブ・コモンズ・ライセンス 表示 4.0のもとでライセンスされています。」;
§3(3) prescribes the credit (title, 藤沢市, the licence, linked); §4 a
disclaimer; §5 a reimbursement clause for costs arising from a user's breach
or a third party's rights infringed by the user. **A licence-read agent reads
the terms separately (pending); staging records its verdict and the credit
wording.** No verdict is written in this brief.

- **MHLW open data** (the notifications layer and the own-point fallback):
  PDL 1.0 as recorded in `docs/data_sources/japan.md`, its 出典 line and who
  processed it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat** and the census: measurement
  sources, not drawn. **Operators' timetables**: read for counts only, never
  reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The individual operators' food file** (1,897 rows; 1,534 fixed premises
  in a bucket after the merge, Food service 1,340, Retail 194) **carries no
  operator column**: the city publishes only the premises' trade name,
  address and phone for a sole trader. The name rule has only its version 2
  sign test there: **0** bare personal names. The comparison half cannot run,
  so the page carries **Kawasaki's bullet** ("…names an operator only where
  it is a company, so this cannot be checked for the rest"), Sagamihara's
  wording for every layer. Its vehicles and stalls (addressed 藤沢市内一円)
  are never placed.
- **The companies' file carries 申請者法人名** (a company marker on 2,597 of
  2,629; the other 32 each name a cooperative, school, hospital, association
  or public body) and **申請者名, the representative's own name** (no company
  marker on any row, never equal to 申請者法人名). Step 2 reads 申請者名 IN
  MEMORY for the name rule only (`OPERATOR_COLS` holds it) and never writes
  either column. The rule flags **0** rows (the sign test 0, the comparison
  0); the months 0.
- **The registers' 申請者名 and 代表者名 are filled only for companies** (34
  of 203 barbers, 335 of 821 salons, 86 of 142 laundries, every one with a
  company marker) and blank for sole traders: the city withholds them. The
  sign test flags **1 beauty salon** (withheld by the rule); 0 elsewhere.
- **Every phone column** (営業所電話番号1, 営業所電話番号) is never selected;
  select the trade name, the address, 業種 / 詳細業種 and, for laundry, 種目.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected; its 法人名
  joins the name rule (owner, 2026-10-05): **1** MHLW row flagged.
- No row value was printed or stored while measuring. Run
  `check_personal_exposure.py fujisawa` (`japan=True`) after step 2: the rows
  that matter are the individual operators' trade names; it must print 0.
  Record the verdict in the drafts file and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan East"` (Kantō after the retag), `"country": "Japan"`,
`label_tier: "minor"`. Project to **UTM 54N (EPSG:32654)**: the N03 centroid
lies at longitude 139.459, the extent 139.394 to 139.517, all inside the
138-144 band (computed here, never copied). OSM box from the N03 extent,
rounded out: (35.29, 139.39, 35.43, 139.52).

**Scaffold**: `scaffold_city.py --slug fujisawa --name Fujisawa --system-name
"Odakyu, Enoden, JR East and the Shonan Monorail" --taxonomy japan_eigyo --lat
35.3382 --lon 139.4869 --region "Japan East" --country Japan --mode metro
--page-number <N>` (`--dry-run` first; the marker is 藤沢 station's N02 group
point), with the page number claimed in `docs/session_roles.md` at build, not
here.

## Owner calls

**Made (do not re-ask):** Band A (owner, 2026-10-06, call 113); the Step 0
downloads (call 147); the standing Japanese calls above; the rail scope (the
band row: the Monorail drawn cut, Sōtetsu's stub kept as cut, the Blue Line
left out); `mode: metro` (Yokosuka's precedent); the minor tier and Japan East
(Kantō after the retag); no frequency floor (call 46). **On today's
precedents:** the full list kept whole plus the months (call 126); MHLW's 372
addressed Retail notifications as a partial Food-shops layer (call 127b) and
its own point where the block join misses (127c); Kawasaki's name bullet for
every layer.

**Answered by the owner on 2026-10-06:** call 158, **restaurant rows with combined forms stay in Food service unless the cell names 給食 or 旅館** (a shared-code change for the build session: it applies to every Japanese city); call 159, **MHLW's 6 August closures dropped**; call 160, **the city health centre's yearly report approved** for the official restaurant count (read 2026-10-06: no such report on the city host; its equivalent, the 統計年報 2025's health chapter, gives the registers' counts but no food count, "Counts against the official stock"). The recommendations below are kept as the record.

**Weighed, each with a recommendation:**

1. **Combined 詳細業種 cells.** Of 312 fixed restaurant rows with several
   forms in one cell, 263 name a public restaurant form (飲食店, 一般食堂,
   レストラン, 軽飲食店, 中華料理店, 大衆酒場 …); the first-match rules keep 141 in
   Food service and send **122 elsewhere**: event catering 69
   (`飲食店、仕出し屋` 24, `飲食店、仕出し屋、弁当屋` 22, `一般食堂、仕出し屋` 6 …),
   deli in Retail 27 (`軽飲食店、弁当屋、そうざい屋` 7 …), institutional catering
   19 (`飲食店、給食` 9 …), inside accommodation 7. **The precedent** (Yokosuka,
   the same system) had single-form cells only, so it does not speak to these.
   *Recommend* (b): **a cell that names a public restaurant form stays Food
   service, unless it also names 給食 or 旅館** (those keep leaving: a
   canteen or an in-hotel restaurant is not reliably open to the public).
   That returns **96 rows** (69 + 27) to Food service (+3.3%), as a shared
   rule that splits the cell on 、 (no built city changes: Yokosuka's cells
   are single). Tradeoff: (a), today's code, leaves out restaurants that also
   cater or sell bentō, though they seat diners; (b) needs one shared-code
   change and its Minato control.
2. **MHLW's 6 closed permits** (closed in August 2026, all in the June list).
   *Recommend dropping them* (Fukuyama's closure filter where MHLW knows):
   six known closures. Tradeoff: only MHLW-filed premises can be filtered so
   (272 of the city's permits), so the page's "may include closed premises"
   stays either way.

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control and every city
  screen): `NAME_COLS` + 営業所名1 and 営業所名; open call 1's cell split if
  taken; laundry's 種目 passed as the type (`source_rows`).
- `SOURCE_LINKS` for each renamed file (the quarterly food lists, the monthly
  food CSVs, the registers found by section and link text); **the page keeps
  only three months**, so a build after mid-October takes the 2026-09-30 full
  list (due quarterly) plus the months after it and re-measures; `as_of` from
  the link text (2026-06-30 here, with the months to 2026-08-31), never today.
- **The official count**: the registers' are measured (統計年報 2025, table
  135, 2025-03-31: 102.0%, 104.3%, 94.7%); **the food count is still
  missing** (the yearbook has no food table; call 160's one file is spent).
  The leads under "Counts against the official stock" each need the owner;
  without one the page states no food coverage figure.
- The one MHLW permit in no city file; the 6 closed (open call 2).
- Gate 3 (each operator), OSM `name:en`, line colours on both basemaps, the
  labels on the Sōtetsu and Monorail stubs (1.18 and 0.99 km inside), the
  coastal ring overlap (江ノ島 / 湘南江の島 96 m apart), the opening view
  (`map-view`), the factory share, the Economic Census control (estimated
  1.90), `check_provenance.py`, `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "fujisawa-food-page",
    "claim": "The food page (28905) offers the 2026-06-30 full lists for companies and individuals and the June and August 2026 monthly CSVs. ASCII strings only: the host sends no charset, so the Japanese text (2026年6月末現在) cannot be matched; a newer full list or month means re-measure",
    "kind": "http_contains",
    "url": "https://www.city.fujisawa.kanagawa.jp/seiei/shokuhineisei/opendatabase.html",
    "present": ["zende-ta202606houjin.csv", "zende-ta202606kojin.csv", "shokuhin202606houjin.csv", "shokuhin202608houjin.csv", "shokuhin202608kojin.csv"]
  },
  {
    "id": "fujisawa-env-page",
    "claim": "The barber, beauty and laundry page (32931) offers the three 2026-06-30 lists measured here (timestamp-named files; a new name means a new edition: re-measure). ASCII strings only",
    "kind": "http_contains",
    "url": "https://www.city.fujisawa.kanagawa.jp/seiei/kankyouopendate.html",
    "present": ["20260713103834.csv", "20260713104008.csv", "20260713104127.csv"]
  },
  {
    "id": "fujisawa-library-terms",
    "claim": "The city's open-data library (13230) lists both dataset pages and links the terms PDF (CC BY 4.0, use counts as acceptance). ASCII strings only",
    "kind": "http_contains",
    "url": "https://www.city.fujisawa.kanagawa.jp/kyoso/shise/kekaku/kakushu/datalibrary.html",
    "present": ["riyoukiyaku20250401.pdf", "seiei/shokuhineisei/opendatabase.html", "seiei/kankyouopendate.html"]
  },
  {
    "id": "fujisawa-terms-pdf",
    "claim": "The open-data terms (riyoukiyaku20250401.pdf, 156,986 B on 2026-10-06) answer a plain GET",
    "kind": "http_ok",
    "url": "https://www.city.fujisawa.kanagawa.jp/documents/13230/riyoukiyaku20250401.pdf",
    "min_bytes": 140000
  },
  {
    "id": "fujisawa-yearbook-health-chapter",
    "claim": "The 統計年報 2025年版 health chapter (1,924,927 B on 2026-10-06), source of the official barber, beauty and laundry counts at 2025-03-31 (table 135: 199, 787, 150), answers a plain GET; it carries no food-permit table",
    "kind": "http_ok",
    "url": "https://www.city.fujisawa.kanagawa.jp/documents/35832/11roudoushakaihoshouhokeneisei_r7.pdf",
    "min_bytes": 1700000
  },
  {
    "id": "fujisawa-food-houjin-live",
    "claim": "The companies' full food list (606,748 B, 2,629 rows on 2026-10-06) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://www.city.fujisawa.kanagawa.jp/documents/28905/zende-ta202606houjin.csv",
    "min_bytes": 550000
  },
  {
    "id": "fujisawa-food-kojin-live",
    "claim": "The individual operators' full food list (341,236 B, 1,897 rows) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://www.city.fujisawa.kanagawa.jp/documents/28905/zende-ta202606kojin.csv",
    "min_bytes": 300000
  },
  {
    "id": "fujisawa-food-aug-live",
    "claim": "The August 2026 monthly food file for companies (6,914 B, 30 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.fujisawa.kanagawa.jp/documents/28905/shokuhin202608houjin.csv",
    "min_bytes": 5000
  },
  {
    "id": "fujisawa-barber-live",
    "claim": "The barber list (21,889 B, 203 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.fujisawa.kanagawa.jp/documents/32931/20260713103834.csv",
    "min_bytes": 18000
  },
  {
    "id": "fujisawa-beauty-live",
    "claim": "The beauty-salon list (101,611 B, 821 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.fujisawa.kanagawa.jp/documents/32931/20260713104008.csv",
    "min_bytes": 90000
  },
  {
    "id": "fujisawa-laundry-live",
    "claim": "The laundry list (18,338 B, 142 rows) answers",
    "kind": "http_ok",
    "url": "https://www.city.fujisawa.kanagawa.jp/documents/32931/20260713104127.csv",
    "min_bytes": 15000
  },
  {
    "id": "fujisawa-mhlw-live",
    "claim": "MHLW's open-data file for Fujisawa (14205), the control, answers a plain keyless GET (480,077 B, 1,267 rows on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=14205_food_business_all.csv",
    "min_bytes": 400000
  },
  {
    "id": "fujisawa-isj-block-live",
    "claim": "MLIT's block-level address file for Fujisawa (14205) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/14205-24.0a.zip",
    "min_bytes": 150000
  },
  {
    "id": "fujisawa-isj-chome-live",
    "claim": "MLIT's town-chōme file for Fujisawa (14205) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/14205-19.0b.zip",
    "min_bytes": 5000
  },
  {
    "id": "fujisawa-jr-tsujido-timetable",
    "claim": "JR East's timetable index for 辻堂 (1008) still links its two weekday Tōkaidō pages (010, 020) - the JR frequency source (162 and 157 departures on 2026-10-06). ASCII strings only (no charset sent)",
    "kind": "http_contains",
    "url": "https://timetables.jreast.co.jp/timetable/list1008.html",
    "present": ["tt1008/1008010.html", "tt1008/1008020.html"]
  },
  {
    "id": "fujisawa-enoden-ishigami-timetable",
    "claim": "Enoden's 石上 station timetable page still shows both directions (76 departures each way on 2026-10-06, every 14 minutes midday)",
    "kind": "http_contains",
    "url": "https://www.enoden.co.jp/train/station/ishigami/time-table/",
    "present": ["藤沢行き", "鎌倉行き"]
  },
  {
    "id": "fujisawa-monorail-timetable",
    "claim": "The Shōnan Monorail's 西鎌倉 timetable PDF, the probe's frequency source (every 7-8 minutes), answers",
    "kind": "http_ok",
    "url": "https://www.shonan-monorail.co.jp/ticket/pdf/nishikamakura_n.pdf?ver210322_01",
    "min_bytes": 100000
  },
  {
    "id": "fujisawa-projected-crs",
    "claim": "Fujisawa projects to UTM 54N",
    "kind": "utm_zone_from_longitude",
    "lon": 139.459,
    "expect": "EPSG:32654"
  }
]
```
