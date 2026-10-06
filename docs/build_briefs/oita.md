# Ōita — build brief

**Band A, owner-approved 2026-10-06** (Japan wave 5, calls 95 and 106:
`docs/decisions_drafts/staging.md`, "Wave 5"; the master list's Ōita row).
The Step 0 downloads were approved by the owner the same day. **Step 0
measured 2026-10-06** (staging). Into `data/oita/raw/` (gitignored), each from
its publisher's own host with the project user-agent, each HTTP 200, under
each URL's own file name as `japan_fetch.get` saves:

- From `data.bodik.jp` (organisation 442011, 大分市; four calls 22 s apart):
  `r080901allkyoka.csv` (1,311,758 B, every food permit as of 2026-09-01),
  `20260331riyousyo.csv` (34,503 B), `20260331biyousyo.csv` (127,669 B),
  `20260331kuriningu.csv` (19,780 B).
- From `i2fas.mhlw.go.jp`: `44201_food_business_all.csv` (515,890 B), a
  control only.
- From `nlftp.mlit.go.jp`: `isj/44201-24.0a.zip` (656,100 B) and
  `isj/44201-19.0b.zip` (16,126 B).

**2,681,826 B in all.** Nothing else was downloaded. Not fetched (not
approved): the city's notification list (`442011_licensed_facility`, open
call 2), the monthly new-premises files (`442011_new_facility`,
`442011_beauty_salon_new`, `442011_cleaning_new`; open call 3), the XLSX and
PDF twins, and the bath, inn and theatre lists.

**Run `python scripts/brief_check.py oita` before writing any code.** Five of
its checks call BODIK, which wants at least 20 s between calls; run it
through a pacer (staging's was a scratch wrapper holding each
`data.bodik.jp` request 21 s after the last) or space the BODIK checks by
hand. Then the `japan-city` skill, **Matsuyama's shape** (one complete city
list beside MHLW's file), Hamamatsu's for the registers, Fukuoka's
`ADDRESS_BY_CONSENT` for the rows whose address the city withholds.
Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from scratch scripts only
(`scripts/screen_japan_join.py` has no Ōita entry; its table is shared code
and was not edited). Rail: MLIT N02-25 cut at the N03 city line, measured
through `pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none reaches Ōita); (2) **lines served only by limited
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
English station names from OSM `name:en`; every Japanese city reads
`WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):** Ōita
carries `label_tier: "minor"` and goes in the **Japan West** view, as Kurume
and Kumamoto do (`app/cities.py`); wave 4's first city to land retags Japan
into the eight regions, Ōita into **Kyushu-Okinawa**. Its label offset comes
from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and 1200), never by eye.

**`mode`: `metro`** (the owner's rule of 2026-10-02, "unless there is
substantial JR, JR reads as metro"): all 17 station groups are JR Kyushu's;
no subway, tram or private railway. Okayama's and Fukuyama's precedent.

---

## The one-line summary

**All three buckets from the city's own BODIK lists (CC BY 4.0 as stated; a
licence read is pending).** One food file, **every permit in term on
2026-09-01: 6,199 rows, 5,053 restaurants (飲食店営業), 101.6% of e-Stat's
4,971 in force** (FY2024); no expired permit (the earliest expiry is
2026-11-30), old-law permits carried until they end (121 rows). **The city
withholds 301 rows' address** (and on most of them the trade name and the
operator), shown as asterisks: 250 restaurants, counted apart (open call 1).
Barbers **391** (100% of e-Stat's 391), beauty salons **1,308** (103.6% of
1,262), laundries **186** (83.0% of 224), as of 2026-03-31. MHLW's file holds
only 85 permits, every one in the city's file by number: a control, nothing
to add. Block join **84.9%** of the bucketed fixed premises with a visible
address, unplaced 2.9%. **Rail: 17 station groups**, all JR Kyushu (Nippō 8,
Hōhi 6, Kyūdai 5, 大分 shared by all three), read from JR Kyushu's own
timetables: the thinnest stretch, the Hōhi Line's 中判田 to 竹中, runs 25 to
26 trains a day each way, nowhere near 11.

---

## Business leg — the city's 衛生課 lists on BODIK

Host `https://data.bodik.jp` (CKAN; organisation **442011**, 大分市; author
福祉保健部衛生課). Each resource carries `resourceurl`, the same file on the
city's own site (`www.city.oita.oita.jp/o095/...`); the build fetches from
BODIK as staging did. **Never call `datastore_search_sql`** (it answers 403);
at least 20 s between calls.

### Food: `442011_permitted_facility` 許可施設, すべての許可施設一覧

| File (resource) | Bytes | Rows | What it is |
|---|---|---|---|
| `…/dataset/b03c9bdb-a1cc-4d7a-8891-bc7980ec693e/resource/02ed0f35-9a57-4025-ab5b-e274150f3381/download/r080901allkyoka.csv` | **1,311,758** | **6,199** | every food permit in term, 「データ時点日付：2026-09-01」; not datastore-backed (no `ckan_rows`); XLSX twin 1,025,997 B, PDF 10.9 MB |

- **Encoding cp932, no BOM**, header on line 1. Columns: **営業許可№**
  (6,199 distinct, shape `R99-9999`), **業種名**, **業態**, **営業所屋号**,
  営業所カナ屋号, 営業所郵便番号, **営業所住所１** (the address with its block
  number), 営業所住所２ (the building, 2,944 filled), 営業所電話番号,
  **申請者氏名**, 申請者カナ氏名, **代表者氏名**, 申請者住所１ / ２,
  申請者電話番号, 初回許可日, **許可開始日**, **許可満了日**. Dates 和暦
  (`R8.9.1`); `wareki_date` reads every 許可開始日 and 許可満了日 (初回許可日:
  182 unreadable, not needed).
- **Two type spellings.** New law: a number, a space, the type (`1 飲食店営業`,
  `11 菓子製造業`), 6,078 rows. **224 rows carry `?` where the number was**
  (a circled number above ⑳, lost in the cp932 export: `? そうざい製造業` 116,
  `? 漬物製造業` 38 and eight more): `japan_eigyo.normalise` strips a leading
  digit but not `?`, so **the 116 delis fall to "no rule"** against the
  standing call (4). Old law: the type and its sub-type after two spaces, no
  number (`飲食店営業  一般食堂・レストラン`), 121 rows, which the taxonomy
  already reads (restaurants Food service, そうざい Retail, vending out).
- **Type split** (base type): 飲食店営業 **5,053**, 菓子製造業 474, 魚介類販売業
  168, 食肉販売業 164, そうざい製造業 116, 漬物製造業 38, 調理機能を有する自動販売機
  24, 喫茶店営業 21 (old law), 18 more manufacturing types at 16 or fewer.
- **業態 on restaurants**: 一般食堂・レストラン 2,025, **スナック 957**, 軽食喫茶
  487, そうざい 459, 特殊形態 223, めん類食堂 206, 弁当屋 187, 寿司 132,
  キャバレー・ナイトクラブ 73, キッチンカー (40/80/200L) 88, 実演販売 32, other
  smaller.
- **346 rows are addressed 大分市内一円** (特殊形態 202, キッチンカー 80, 実演販売
  32, 特殊形態 自動車 16, 移動販売車 14, 仮設移動 2): vehicles and stalls,
  `mobile` by the shared 一円 rule, none reaches the join.

**Against `japan_register`'s tuples (shared code, not edited here):**
`ADDR_COLS` lacks **営業所住所１** and `NAME_COLS` lacks **営業所屋号**; without
them the shared step reads no address and no name. `OPERATOR_COLS` has
申請者氏名 and 代表者氏名; `TYPE_COLS` has 業種名; `FORM_COLS` has 業態. The
scratch measurement renamed the two columns in memory and stripped the
leading `?`.

### The withheld rows (the city's masking)

- **301 rows show asterisks** (`**********`) in 営業所住所１, 営業所住所２ and
  営業所郵便番号; on 267 of them the trade name is masked too, on 277 the
  operator, on 291 the phone. 292 of the 301 carry no company marker on the
  operator (sole traders), and they skew recent (permits started 2025: 87,
  2026: 91). Types: 飲食店営業 250, 菓子製造業 30, 食肉販売業 7, 魚介類販売業 5,
  vending 4, そうざい 4. In the buckets: Food service 164, Retail 58 (79 leave
  by type or 業態). None is citywide.
- Elsewhere the city masks the operator on 651 rows, its address on 3,267
  and the premises phone on 1,221; three rows mask the trade name but show
  the address.
- **Trap for the build**: the 301 rows share seven (address, type) keys, so
  `rebuilt_register` or one pin per premises would fold them into seven
  phantom premises. Drop them first, by the asterisks, and count them apart
  (`ADDRESS_BY_CONSENT`, Fukuoka's; open call 1). The three masked trade
  names with a visible address take the name rule's fallback (the pin shows
  the permit type), never the asterisks.
- The city's reason for the masking was not read (the BODIK notes say only
  「大分市の許可施設の情報です。」): read the city's own page at build.

### Duplicates, expiry, closures and the old law

- **Repeats**: 6,199 distinct permit numbers. Among the 5,898 rows with a
  visible address, **76 repeat an (address, trade name, type)** in 63 groups
  (70 restaurants): one pin per premises (trap 7) takes them. 5,415 distinct
  (address, trade name) premises.
- **Expired permits: none.** Every 許可満了日 falls on or after **2026-11-30**
  (2026: 61, 2027: 735, 2028: 1,063, 2029: 1,114, 2030: 1,224, 2031: 1,154,
  2032: 716, 2033: 108, 2034: 24); the city ends its permits at quarter ends
  and the file holds only those in term on its date. Starts run 2020-09-15 to
  2026-09-01. `in_term(..., as_of=2026-09-01)` drops nothing; no
  `rebuilt_register` is needed (one complete list, no months).
- **Closures within term are not marked** (no 廃業 column, no closure files).
  **MHLW cannot act as a closure filter here** (Fukuyama's call 6): its file
  holds 85 permits, all granted 2023-03 to 2026-08, every one in the city's
  file by number. So the page says the list may include closed premises.
- **Old-law coverage**: **121 permits started before 2021-06-01** (84
  restaurants, 21 喫茶店, 9 菓子, 7 others), every one under the old-law
  spelling and every old-law spelling among them; all end 2026-11 to 2027.
  The earliest start, 2020-09-15, says every older old-law permit has ended
  (e-Stat's old-law restaurants stood at 1,116 on 2025-03-31 and have been
  converting since). The old law is covered as far as it is still in force.

### Counts against the official stock

e-Stat 衛生行政報告例 FY2024 (`japan_official.estat()`), 大分県大分市, 飲食店営業
in force 2025-03-31: **4,971** (old law 1,116, revised 3,855).

| | Restaurants (飲食店営業) | Share of 4,971 |
|---|---|---|
| The file, 2026-09-01 (vehicles and stalls included, the official measure) | **5,053** | **101.6%** |
| … with the 21 old-law 喫茶店営業 | 5,074 | 102.1% |
| … fixed, address visible (346 citywide and 250 withheld out) | 4,457 | 89.7% |
| MHLW's open restaurant permits (control) | 71 (59 addressed) | 1.4% |

Through `japan_eigyo` (`?` stripped, fixed premises): Food service 3,153,
Retail 1,382; **with the withheld rows out, Food service 2,989, Retail
1,324**. Retail is 菓子 474, restaurants with そうざい as 業態 460, 魚介類 168,
食肉 164, そうざい製造業 116. Restaurants leaving the buckets: **hostess venues
1,030** (スナック, キャバレー; `FORM_RULES`, the standing rule; 都町 is the
city's nightlife district, 1,133 rows), temporary or mobile 業態 121,
accommodation 36, event catering 20, institutional 2.
**Economic Census control** (`scripts/japan_census_control.py` at build):
the 2021 census counts **1,723** 飲食店 establishments in 44201; **2,893**
distinct placed Food-service premises is **1.68 per establishment**, inside
the built cities' 1.56-1.92.

### MHLW's file (44201), a control only

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=44201_food_business_all.csv`:
**515,890 B, 1,602 rows** (届出 1,517, 許可 85; no closure rows), UTF-8 with
BOM, the national schema. The 85 permits: 飲食店営業 71, 食肉 5, 魚介類 4, 菓子
3, vending 2; **all 85 in the city's file by number** (47 also by address and
name). MHLW adds no permit and no closure signal. Its 1,517 notifications
(802 addressed; cup vending 343, その他の食料・飲料販売業 287, vending 178,
集団給食 162, 百貨店・総合スーパー 159, コンビニ 51 …) are the only food-shop
notifications fetched (open call 2). Its own point against the block point
for the same address: **median 40 m, 94.7% within 250 m** (684 rows; 11 over
1 km).

### Personal services: `442011_barber_shop`, `442011_beauty_salon`, `442011_cleaning`

| File (resource) | Bytes | Rows | Official (e-Stat FY2024) | Share |
|---|---|---|---|---|
| `…/dataset/68c0d0a8-7b2c-4217-ba83-90fd8accca19/resource/fcde9e81-40a5-4da8-bdbd-a9b882074224/download/20260331riyousyo.csv` 理容所届出施設一覧 | **34,503** | **391** | 391 | **100.0%** |
| `…/dataset/38ee3063-3b34-4a32-bff3-2ad92611b7a4/resource/66130b2d-f2d2-4be2-b163-c0e41f5a33d0/download/20260331biyousyo.csv` 美容所届出施設一覧 | **127,669** | **1,308** | 1,262 | **103.6%** |
| `…/dataset/1ab16997-d139-4bba-84e9-e819df58675f/resource/a10fb2da-35e7-4e9e-866b-2e19769b7300/download/20260331kuriningu.csv` クリーニング所届出施設一覧 | **19,780** | **186** | 224 (取次所 171) | **83.0%** |

- **As of 2026-03-31** (「令和8年3月31日現在」, データ時点日付 2026-04-01;
  datastore-backed, the row counts in the check block). cp932, no BOM.
  Columns: **施設名称**, **施設所在地**, **開設者** (the operator), 施設電話番号,
  確認年月日 (和暦; 129, 158 and 34 unreadable, `(不明)` and Shōwa forms; not
  needed), 指令番号; the laundry list adds 確認番号 and **種別**.
- **Laundry 種別**: 取次店 128, 工場 54, **無店舗取次店 4** (not premises; the
  shared 無店舗 rule takes them, matching e-Stat's 4 storeless operators).
  The gap to e-Stat is the pick-up shops: 128 against 取次所 171 (74.9%);
  the 54 工場 against e-Stat's 53 other facilities.
- **Standing registers**: 確認年月日 runs from Shōwa to Reiwa; no closure
  column, no closure files. Closed premises may remain; no control.
- Repeats: barbers 0, beauty 1, laundry 2 (address, name); 11 premises are
  in both the barber and the beauty list (one pin per premises and bucket).
  No 一円, 移動 or 無店舗 row in the barber or beauty list.
- **Shared code**: `NAME_COLS` has 施設名称, `ADDR_COLS` 施設所在地,
  `OPERATOR_COLS` 開設者, `TYPE_COLS` 種別. The kind per file comes from the
  source (`SOURCE_KIND` or one source per file), as Hamamatsu's.

## Coordinates — a JOIN to MLIT 位置参照情報 (wardless)

One municipality, **no wards** (`"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/44201-24.0a.zip` (656,100 B,
114,305 rows, **103,726 block keys**), town-chōme
`.../19.0b/44201-19.0b.zip` (16,126 B, **715**). `japan.CITIES` entry at
build: `"oita": {"name": "大分市", "pref": "44", "epsg": 32652, "n02": "25",
"rules": WAVE2_RULES, "wardless": True, "wards": ["44201"]}`.

| Tier (fixed premises in a bucket) | Food, address visible (4,313) | Food service (2,989) | Retail (1,324) | Food, withheld included (4,535) |
|---|---|---|---|---|
| Block | **84.9%** | 87.1% | 80.1% | 80.7% |
| Town-chōme / 大字 centroid | 12.2% | 10.0% | 17.2% | 11.6% |
| Unplaced | **2.9%** | 2.9% | 2.7% | 7.6% (the 222 withheld) |

| Registers | Barbers (391) | Beauty (1,308) | Laundry (182 fixed) |
|---|---|---|---|
| Block / chōme / unplaced | 84.7 / 10.0 / 5.4 | 89.8 / 6.9 / 3.3 | 77.5 / 16.5 / 6.0 |

MHLW's addressed rows join the same way (850 fixed: 80.5 / 15.9 / 3.6). Its
own point (`OWN_POINT_FALLBACK`) would move almost nothing: 85 permits.

**The misses, read** (towns only, scratch `analyse2.py` and `towns.py`):
- **Chōme tier (528 food)**: mostly the 地番 areas of the 大字 (306 towns carry
  字, 287 addresses 大字): 玉沢字楠本 22, 野津原 17, 今市 12, 下原 9, 廻栖野 8,
  佐賀関 8, 本神崎 7, 森字六反田 7, 羽屋 7, 古国府 7, 田尻 7. Some sit in
  numbered chōme whose block number MLIT lacks (都町3丁目 10, 都町2丁目 7,
  中央町2丁目 6, 金池南2丁目 6): read them at build.
- **Unplaced (123 food)**: towns in neither MLIT file. 庄の原 9, 北下郡 5, 津留
  5, 大石町5丁目 5, 椎迫 4, 志手 3, 光吉新町 2 are absent outright (MLIT has
  大字光吉, 大字大津留, not these); 横田字辻 8 (MLIT: 横田 and 横田1/2丁目),
  明磧1丁目 5 (MLIT: 明磧町1丁目), 上白木 3 (大字白木), 城原尾崎 3 (大字城原) and
  梅ケ丘 (MLIT: 梅が丘, chōme file only) are spelling gaps a shared rule might
  close; each followed by the Minato control.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_44_GML.zip`, N03 code 44201
(**502.7 km²**, extent W 131.419, S 33.070, E 131.963, N 33.290). Read with
`stub_test()`'s method and an in-memory `CITIES` entry (scratch `rail.py`).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 日豊線 (九州旅客鉄道, 11) | JR Nippō Main Line | **8 / 113** | 西大分, 大分, 牧, 高城, 鶴崎, 大在, 坂ノ市, 幸崎 |
| 豊肥線 (九州旅客鉄道, 11) | JR Hōhi Main Line | **6 / 37** | 大分, 滝尾, 敷戸, 大分大学前, 中判田, 竹中 |
| 久大線 (九州旅客鉄道, 11) | JR Kyūdai Main Line | **5 / 37** | 大分, 古国府, 南大分, 賀来, 豊後国分 |

- **19 station records, 17 N02_005g groups** (大分 one group for all three
  lines, spread 0 m), matching the master list's 17. No name in two groups;
  no close pair under 600 m. **Median nearest-station gap 2,209 m** (1,318 to
  4,831): standard rings by the spacing rule.
- **Shinkansen**: none in Ōita Prefecture.
- **Cut at the line** (named by N03 municipality at build): the Nippō Line
  105 beyond (other prefectures 68, 佐伯市 9, 宇佐市 6, 臼杵市 5, 別府市 4, 杵築市
  4, 日出町 4, 中津市 3, 津久見市 2), the Kyūdai Line 32 (other prefecture 11,
  由布市 8, 日田市 7, 九重町 4, 玖珠町 2), the Hōhi Line 31 (other prefecture 22,
  豊後大野市 6, 竹田市 3).
- **The light-rail/rail test**: all three are heavy rail (N02 class 11, JR
  conventional). No tram, light rail, subway or private railway.
- **The stub test passes.** No line is cut to one station; no urban line
  runs here. 西大分 sits 259 m inside the city line toward 別府, 坂ノ市 514 m.
- **Frequency, read 2026-10-06 from JR Kyushu's own station timetables** by
  plain GET with the project user-agent (`www.jrkyushu-timetable.jp`,
  `cgi-bin/sp/sp-tt_list.cgi/<station>/` and its `sp-tt_dep.cgi` pages,
  weekday Wednesday 2026-10-07; station codes from `sp/railway_list.html`):

  | Station (line, direction) | Weekday departures | Per hour 10-15 | Longest gap 09-17 |
  |---|---|---|---|
  | 大分 (Nippō, to 別府, locals and rapids) | 43 (+37 limited express) | 1-3 | 50 min |
  | 大分 (Nippō, to 佐伯) | 49 | 2-3 | 49 min |
  | 西大分 28784 (Nippō, each way) | 43 / 44 | 2-3 | 49 min |
  | 坂ノ市 28761 (Nippō, each way) | 36 / 37 | 1-2 | 48 min |
  | 幸崎 28759 (Nippō, to 佐伯, beyond the city) | 27 | 0-2 | 102 min |
  | 中判田 28782 (Hōhi, to 豊後竹田 / to 大分) | 25 / 36 | 0-3 | 98 min |
  | **竹中 28772 (Hōhi, each way)** | **25 / 26** | 0-2 | 109 min |
  | 豊後国分 28798 (Kyūdai, each way) | 28 / 29 | 0-2 | 100 min |
  | 賀来 28751 (Kyūdai, each way) | 29 / 29 | 0-2 | 101 min |

  **The thinnest stretch inside the city is the Hōhi Line from 中判田 to 竹中,
  25 to 26 trains a day each way** (hours with no train at 10 and 13); the
  Kyūdai Line carries 28 to 29. **No stretch is near 11 a day**, so nothing
  is named under call 86. The master list's "Nippō locals 2 an hour, Hōhi
  1-3, Kyūdai about hourly" holds. The page carries no reproduction notice;
  only counts are recorded, never a timetable on the page.
- ⚠️ **Gate 3** at build: JR Kyushu's station counts per line inside the city
  (Nippō 8, Hōhi 6, Kyūdai 5). **OSM `name:en`** for 17 groups (one Overpass
  query at build, in the box below; not queried here). Line colours on both
  basemaps; three JR lines need three distinguishable hues.

## Scope

**Ōita City.** The Nippō Line runs on to 別府 and 臼杵, the Hōhi Line to
豊後大野, the Kyūdai Line to 由布; cut at the line.

## Licences — as stated; the full read is pending

**As stated on BODIK**: each of the four datasets (`442011_permitted_facility`,
`442011_barber_shop`, `442011_beauty_salon`, `442011_cleaning`) declares
`license_id` **cc-by-40-intl**, "Creative Commons Attribution 4.0
International", linked to `creativecommons.org/licenses/by/4.0/deed.ja`. The
full read (BODIK's own terms, the city's open-data terms and any prescribed
credit) is a separate `licence-read` agent's, pending; **staging records its
verdict and conditions**. No verdict is written in this brief; take any
credit wording from staging's record.

- **MHLW open data** (a control; if open call 2 takes its notifications):
  PDL 1.0 as recorded in `docs/data_sources/japan.md`, its 出典 line and who
  processed it.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **N03**: CC BY
  4.0, picks stations, ⛔ never drawn. **e-Stat**: a measurement source, not
  drawn. **JR Kyushu's timetable**: read for counts only, never reproduced.
- The notice number is claimed at build (next free per
  `docs/session_roles.md`), not here.

## Privacy

- **The food list carries the operator block**: **申請者氏名** (2,916 rows
  carry a company or cooperative marker, 3,283 none, 651 of those masked by
  the city), 申請者カナ氏名, **代表者氏名** (3,583 filled, 667 where the
  operator has no marker), **申請者住所１ / ２** (the operator's own address;
  masked on 3,267 rows), 申請者電話番号, and 営業所電話番号. Step 2 never reads
  any of them into an output; 申請者氏名 and 代表者氏名 are read IN MEMORY for
  the name rule only (both already in `OPERATOR_COLS`). On 298 sole-trader
  rows the operator's address equals the premises: a trade name there is the
  sign of a home-run business.
- **The registers carry 開設者**: no company marker on 366 of 391 barbers, 998
  of 1,308 beauty salons, 79 of 186 laundries. Select 施設名称, 施設所在地 and
  種別 only; never 施設電話番号.
- **The name rule, version 2, measured in memory** (answers only, never a
  value): food **261** rows by `name_is_operator`, of which **259 are rows
  where the city masked both the trade name and the operator** (the
  asterisks compare equal; all withheld anyway), so **2 real rows** whose
  trade name is the operator's own name; **0 bare personal names**. Barbers
  0, **beauty salons 1** (0 bare), laundries 0. No value was printed or
  stored.
- MHLW's 法人名, 法人番号, 法人住所 and phones are never selected.
- Run `check_personal_exposure.py oita` (`japan=True`) after step 2: the rows
  that matter are the sole traders' trade names; it must print 0, and no
  asterisk string may reach the map. Record the verdict in the drafts file
  and `docs/privacy_verdicts.md`.

## Region

`"region": "Japan West"` (Kyushu-Okinawa after the retag), `"country":
"Japan"`, `label_tier: "minor"`. Project to **UTM 52N (EPSG:32652)**: the N03
centroid lies at longitude 131.641, the extent 131.419 to 131.963, all inside
the 126-132 band (computed here, never copied; Fukuoka's 52N is the
precedent for the band, not the source). OSM box from the N03 extent, rounded
out: (33.06, 131.41, 33.30, 131.97).

**Scaffold**: `scaffold_city.py --slug oita --name "Ōita" --system-name "JR
Kyushu" --taxonomy japan_eigyo --lat 33.180 --lon 131.641 --region "Japan
West" --country Japan --mode metro --page-number <N>` (`--dry-run` first),
with the page number claimed in `docs/session_roles.md` at build, not here
(check `docs/staged_cities.json` for an entry first).

## Owner calls

**Made (do not re-ask):** Band A (owner, 2026-10-06, calls 95 and 106); the
Step 0 downloads; the standing Japanese calls above; `mode: metro`; the
minor tier and Japan West (Kyushu-Okinawa after the retag); no frequency
floor (call 46), no stretch at 11 trains a day or fewer (call 86 has nothing
to name); the three JR lines drawn as cut (standing call, no stub); the
hostess-venue rule (`FORM_RULES`, standing).

**Open, each with a recommendation:**

1. **The 301 withheld rows** (250 restaurants; 222 in a bucket, 164 Food
   service). *Recommend* Fukuoka's precedent: drop them before any
   de-duplication and count them apart (`ADDRESS_BY_CONSENT`), the page
   saying the city withholds some premises' addresses. The tradeoff: about
   5% of restaurants are counted but not drawn; there is no town to place
   them by, so the only alternative is leaving them out silently.
2. **A food-shops layer.** (a) **The city's own notification list**
   (`442011_licensed_facility`, すべての営業届出施設一覧 as of 2026-09-01, CSV
   287,712 B, same publisher and licence statement; not approved, not
   fetched). *Recommend approving it at build*: it is the city's complete
   list, where MHLW's is opt-in. (b) Failing that, **MHLW's 1,517
   notifications** (802 addressed) as a partial, opt-in layer, Fukuyama's
   (call 5) and Matsuyama's precedent. The tradeoff: (a) costs one approval
   and a schema read, (b) a bucket the page must call partial and MHLW's
   credit on the notice; with neither, Retail is the permit-holding shops
   only (1,324).
3. **The registers' months** (`442011_beauty_salon_new`, new beauty salons
   2026-04 to 08, five CSVs of 240 to 713 B; `442011_cleaning_new`; no barber
   set was found; closures are never published): not approved, not fetched.
   *Recommend approving them at build* (Ichinomiya's call 4) so the
   registers reach 2026-08-31; the tradeoff is a few dozen salons for one
   more approval, and openings without closures (an upper bound). Without
   them the registers' date is 2026-03-31 (`SOURCE_AS_OF` per source).

## What the build must still measure

- ⚠️ **Shared code** (each followed by the Minato control, `screen_japan_join.py
  minato` 98.0 / 0.2 / 1.8, and every city screen): `ADDR_COLS` +
  営業所住所１, `NAME_COLS` + 営業所屋号; `japan_eigyo.normalise` strips a
  leading `?` (the lost circled number; 224 rows, 116 delis); asterisk rows
  out before de-duplication; the spelling gaps above (明磧 / 明磧町, 梅ケ丘 /
  梅が丘, 字 forms).
- `as_of` pinned to **2026-09-01** (the file's date), never today;
  `SOURCE_AS_OF` 2026-03-31 for the registers unless open call 3 is taken.
- The city's own page for the reason it masks rows; the 3 masked trade names
  with a visible address.
- Gate 3 (JR Kyushu), OSM `name:en`, line colours on both basemaps, the
  opening view (`map-view`), the factory share (菓子 and そうざい in Retail),
  the Economic Census control (estimated 1.68), `check_personal_exposure.py`,
  `check_provenance.py`, `check_scope_disclosure.py`.

```brief-checks
[
  {
    "id": "oita-food-package",
    "claim": "BODIK's record for the city's permits dataset (442011_permitted_facility) declares cc-by-40-intl and still offers the 2026-09-01 all-permits CSV (resource 02ed0f35, r080901allkyoka.csv; a newer file name means re-measure). ASCII strings only. One BODIK call",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=442011_permitted_facility",
    "present": ["cc-by-40-intl", "02ed0f35-9a57-4025-ab5b-e274150f3381", "r080901allkyoka.csv", "2026-09-01"]
  },
  {
    "id": "oita-mhlw-live",
    "claim": "MHLW's open-data file for Ōita (44201), the control, answers a plain keyless GET (515,890 B, 1,602 rows on 2026-10-06)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=44201_food_business_all.csv",
    "min_bytes": 400000
  },
  {
    "id": "oita-barber-rows",
    "claim": "The barber list (as of 2026-03-31) has 391 rows in BODIK's datastore. One BODIK call",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "fcde9e81-40a5-4da8-bdbd-a9b882074224",
    "expect": 391
  },
  {
    "id": "oita-isj-block-live",
    "claim": "MLIT's block-level address file for Ōita (44201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/44201-24.0a.zip",
    "min_bytes": 600000
  },
  {
    "id": "oita-isj-chome-live",
    "claim": "MLIT's town-chōme file for Ōita (44201) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/19.0b/44201-19.0b.zip",
    "min_bytes": 15000
  },
  {
    "id": "oita-beauty-rows",
    "claim": "The beauty-salon list (as of 2026-03-31) has 1,308 rows in BODIK's datastore. One BODIK call",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "66130b2d-f2d2-4be2-b163-c0e41f5a33d0",
    "expect": 1308
  },
  {
    "id": "oita-jr-takenaka-timetable",
    "claim": "JR Kyushu's timetable index for 竹中 (28772) lists the Hōhi Main Line both ways - the thinnest in-city stretch's frequency source (25 to 26 a day each way on 2026-10-07)",
    "kind": "http_contains",
    "url": "https://www.jrkyushu-timetable.jp/cgi-bin/sp/sp-tt_list.cgi/28772/",
    "present": ["豊肥本線 豊後竹田・宮地・肥後大津・熊本方面", "豊肥本線 大分方面"]
  },
  {
    "id": "oita-jr-koozaki-timetable",
    "claim": "JR Kyushu's timetable index for 幸崎 (28759) lists the Nippō Main Line both ways",
    "kind": "http_contains",
    "url": "https://www.jrkyushu-timetable.jp/cgi-bin/sp/sp-tt_list.cgi/28759/",
    "present": ["日豊本線 大分・別府・行橋・小倉・門司港方面", "日豊本線 佐伯方面"]
  },
  {
    "id": "oita-laundry-rows",
    "claim": "The laundry list (as of 2026-03-31) has 186 rows in BODIK's datastore. One BODIK call",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "a10fb2da-35e7-4e9e-866b-2e19769b7300",
    "expect": 186
  },
  {
    "id": "oita-jr-bungokokubu-timetable",
    "claim": "JR Kyushu's timetable index for 豊後国分 (28798) lists the Kyūdai Main Line both ways",
    "kind": "http_contains",
    "url": "https://www.jrkyushu-timetable.jp/cgi-bin/sp/sp-tt_list.cgi/28798/",
    "present": ["久大本線 由布院・豊後森・日田・久留米方面", "久大本線 大分方面"]
  },
  {
    "id": "oita-projected-crs",
    "claim": "Ōita projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 131.641,
    "expect": "EPSG:32652"
  },
  {
    "id": "oita-laundry-fields",
    "claim": "The laundry register's columns: the premises fields step 2 selects, its kind column (種別), and the operator name never selected. One BODIK call",
    "kind": "ckan_fields",
    "domain": "data.bodik.jp",
    "resource_id": "a10fb2da-35e7-4e9e-866b-2e19769b7300",
    "present": ["施設名称", "施設所在地", "開設者", "種別"]
  }
]
```
