# Kanazawa — build brief

**Band B, owner-approved 2026-10-04**: food from the city's dated snapshot,
the snapshot's date disclosed, no personal services (Japan's third wave;
`docs/decisions_drafts/staging.md`, "Japan's third wave, Germany south and
Poland banded"). The Step 0 downloads approved 2026-10-05 (staging's call 10,
"Band B's licence terms accepted, the briefs' calls made …"). **Step 0
measured 2026-10-05** (staging). Downloaded, each from its publisher's own
host, into `data/kanazawa/raw/` (gitignored), named as a build's
`fetch_sources.py` would name them:

- `172014-syokuhineisei-kyokashisetsu.csv` (**2,756,283 B**) from
  `catalog-data.city.kanazawa.ishikawa.jp`: the CKAN datastore dump
  (`/datastore/dump/09a49521-cabf-40b4-978b-bd61ef02f650?bom=true`, the
  resource page's own download link). CKAN records the upload as 2,568,426 B;
  the dump adds a BOM and an `_id` column. The resource's `url` is empty and
  its `/download/…csv` path answers **HTTP 500** to a GET (not retried
  elsewhere), so the dump is the only route.
- MHLW's `17201_food_business_all.csv` (574,826 B) from `i2fas.mhlw.go.jp`,
  as a control.
- MLIT's `isj/17201-24.0a.zip` (567,791 B) and `isj/17201-19.0b.zip`
  (19,231 B) from `nlftp.mlit.go.jp`, to check the rows' coordinates.

Every request answered 200 except the one 500 above. Operator pages read by
curl for rail (HTML only; no timetable PDF fetched).

**Run `python scripts/brief_check.py kanazawa` before writing any code.**
Then the `japan-city` skill: a **single city list that carries its own
coordinates** (Toyama's complete-own-list shape, with Fukuoka's
`OWN_POINT_FALLBACK` taken from the list itself), **food only** (Hiroshima's
one-bucket page). Coordinates: the `address-join` skill, measured with the
shared `pipeline/countries/japan_register.py` functions from scratch scripts
(`scripts/screen_japan_join.py` has no Kanazawa entry; add one at the
build). Rail: MLIT N02-25 cut at the N03 city line, measured through
`pipeline/countries/japan.py` with a scratch `CITIES` entry.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; 金沢 on the Hokuriku Shinkansen is dropped, and stays as an IR
Ishikawa station); (2) **lines served only by limited expresses DO count**
(2026-09-28); (3) **the city line only**: only stations inside the city get
rings, JR and the private lines are cut at the line, **a one-station stub
stays as cut** (2026-09-27), and an URBAN line cut to a stub goes back to the
owner; (4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory
share measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**:
where the trade name IS the operator's own name, the pin shows its permit
type, the operator column read in memory only (2026-09-27), **法人名
included** (Cleanup, master, 2026-10-05; DECISIONS "MHLW's 法人名 joins the
Japanese name rule"); (6) **no page says "currently operating"**. Also:
fault-based cost clauses accepted for all of Japan (2026-09-24); yatai count
but a 露店 form is a street stall (2026-09-28, 2026-09-29); English station
names from OSM `name:en`, numerals as figures before 丁目; every Japanese
city reads `WAVE2_RULES` (owner, 2026-10-04).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Kanazawa carries `label_tier: "minor"` and goes in the **Japan East** view,
as the two built Hokuriku cities do (Toyama and Fukui, `app/cities.py`). Its
label offset comes from `check_macro_labels.py` (PROBLEMS 0 at 375, 768 and
1200), never by eye. If a wave-4 city lands first, the eight-region retag
(owner, 2026-10-04) moves Kanazawa with the rest (Hokuriku is Chubu).

**`mode`: `metro`** (the owner's rule of 2026-10-02, applied as for Kurume
and Maebashi): no subway or tram is drawn and **no JR line has a station
inside the city** (JR West's Hokuriku Line here passed to IR Ishikawa
Railway), so the mode follows the backbone, Hokutetsu's two lines, railways
(N02 class 12): 17 station groups against IR Ishikawa's 4.

---

## The one-line summary

**Food only, from ONE source: the city catalogue's 食品衛生関係営業許可施設一覧,
a snapshot of every food permit in term in early April 2024 (8,842 rows, the
newest permit 2024-04-01), with the city's own coordinates on every row.**
It holds **6,478 restaurant permits (飲食店営業 in every form), 100.9% of the
6,420 in force at FY2023's year end (2024-03-31)** and 100.6% of FY2024's
6,438. Through `japan_eigyo`: **7,844 storefront rows (Food service 5,839,
Retail 2,005), 7,389 pins** after one per premises. Block join **91.8%**, the
city's own point for the rest (640 of 647). ⚠️ **43% of the storefront rows'
permits have reached their expiry date since** (old-law permits, 79% of them,
nearly all renewed by the official stock): see open call 1. Rail: **21 N02
station groups** (Hokutetsu Asanogawa 10, Ishikawa 7, IR Ishikawa 4).

🔎 **The master list's "5,412 restaurants, 84%" undercounts.** 5,412 is plain
飲食店営業 plus its subtypes （１）（２）（３）; it leaves out **飲食店営業（４）
(1,066 rows: bars 550, そうざい店 205, yakiniku 182, vehicles 62, …)**, also
a restaurant permit under the old-law subdivision the list uses. The row
needs correcting to 6,478 (101% of the official count at the snapshot's
date); staging's edit, not this brief's.

---

## Business leg — the city's catalogue snapshot

| | 金沢市 食品衛生関係営業許可施設一覧 |
|---|---|
| **Dataset** | `https://catalog-data.city.kanazawa.ishikawa.jp/dataset/172014-syokuhineisei-kyokashisetsu` (CKAN 2.9, the city's 金沢市オープンデータポータル catalogue); `package_show` title 「金沢市 食品衛生関係営業許可施設一覧」 (the page heading drops 「金沢市 」); author 衛生指導課; `license_id: cc-by`, 「クリエイティブ・コモンズ 表示」; created 2021-12-27, **last modified 2024-07-16** (package and resource); no notes, no stated as-of date |
| **Resource** | `09a49521-cabf-40b4-978b-bd61ef02f650`, `172014-syokuhineisei-kyokashisetsu.csv`, datastore-active, `size` 2,568,426; `datastore_search` total **8,842** |
| **File** | the dump above: **8,842 rows**, UTF-8 with BOM, one municipality (172014 / 石川県 / 金沢市 on every row) |
| **As of** | **early April 2024**: newest 許可年月日 **2024-04-01**, earliest 許可満了日 **2024-04-15** (so extracted between those dates); permits granted 2017-10-01 to 2024-04-01 |
| **Columns** | the national recommended schema: 都道府県コード又は市区町村コード, NO, 都道府県名, 市区町村名, **営業所名称**, 営業所名称カナ, **営業の種類**, **業態**, **営業所所在地**, 営業所方書 (empty), **緯度 / 経度**, 営業所電話番号, **法人名**, 法人番号 (empty), 許可番号, 初回許可年月日 (empty), 許可年月日, 開始年月日, **許可満了日**, 廃業年月日 (empty), 申請区分 (empty), 許可条件 (empty), 備考, 画像 (**never read**) |
| **Dates** | `2027/5/31` (8,077 expiries), `R8.10.31` (686) and, for grants, `H30.4.1` (78): the shared `wareki_date` reads all 8,842 grant and expiry dates |

**Types** (all rows): 飲食店営業 **3,172** (the revised law, granted
2021-04-16 to 2024-04-01) · 飲食店営業（１） **2,020** · （４） **1,066** ·
（２） 145 · （３） 75 (the old law's subdivision, granted 2018-01 to
2021-06-01) · 菓子製造業 976 · そうざい製造業 325 · 魚介類販売業 270 ·
食肉販売業 243 · 喫茶店営業 100 · アイスクリーム類製造業 95 · 27 other
manufacturing and processing types (439 rows) · 調理の機能を有する自動販売機営業 10.

**業態** carries the old law's form (軽食堂 619, バー 550, 料理店 504,
一般食堂 320, レストラン 215, そうざい店 205, 焼肉 182, 中華料理店 141, すし屋
116, 弁当屋 113, めん類食堂 90, 旅館 75, 仕出し屋 32, 自動販売機 46) and
for the revised law only 飲食店営業 2,865, 自動車営業 205, 露店営業 99,
臨時営業 3. Old-law subtypes by 業態: （１） diners and restaurants, （２）
弁当屋 and 仕出し屋, （３） 旅館, （４） bars, そうざい店, yakiniku,
okonomiyaki, takoyaki, oden, ryōtei and vehicles.

**Through `japan_eigyo`** (step 2's order, `WAVE2_RULES`, the city as
`wardless`):

- Closed 0 (no 廃業年月日 anywhere: the snapshot holds permits in term).
- **Not a premises 323** (addresses reading 一円 / 市内 284, blank 41; all
  vehicles and stalls).
- **Out by rule 675**: no rule 439 (manufacturing, processing, 競り売り),
  inside accommodation 75 (業態 旅館), temporary or mobile 73, vending 56,
  event catering (仕出し) 32.
- **Storefronts 7,844: Food service 5,839** (restaurant 5,791, café 48) and
  **Retail 2,005** (菓子 961, deli 531 = そうざい製造業 325 + そうざい店 205 by
  業態 + 1, fishmonger 270, butcher 243).
- **One pin per premises and bucket** (step 2's key): 455 repeat rows
  dropped, **7,389 pins: Food service 5,820, Retail 1,569**.
- 菓子 / そうざい pins 1,225, factory-like names **54 (4.4%)**: kept and
  measured (owner, 2026-09-24).

**Against the official count** (e-Stat 衛生行政報告例, tables 5-2-1 + 5-4-1,
row 石川県金沢市; `data/japan/raw/estat_eisei_r5_…` and `…_r6_…`, read, not
downloaded):

| | Old law | Revised law | 飲食店営業 in force |
|---|---|---|---|
| FY2023, 2024-03-31 (the snapshot's date) | 3,353 | 3,067 | **6,420** |
| **The snapshot, early April 2024** | **3,306** (98.6%) | **3,172** (103.4%, a few more weeks of grants) | **6,478 (100.9%)** |
| FY2024, 2025-03-31 (`japan_official.restaurants`) | 2,184 | 4,254 | **6,438** (the snapshot 100.6%) |

**The snapshot is a complete register at its date.** Between the two years
the old-law stock fell by 1,169 and the revised-law stock rose by 1,187: the
old-law permits that expire are renewed under the revised law, almost one
for one.

**Expiry against the snapshot and today** (`許可満了日`):

- At the snapshot (2024-04-01): every row in term.
- **By 2026-08-31**: 3,163 storefront rows have expired; **by 2026-10-05
  (today)**: **3,360 of 7,844 storefront rows (43%)**, 3,146 of 7,389 pins;
  of the 6,478 restaurant permits, **2,713 (42%)**: old law **2,623 of 3,306
  (79%)** (（１） 1,586, （４） 866, （２） 110, （３） 61), revised law **90 of
  3,172 (3%)**. 喫茶店営業 86 of 100.
- The renewals are not in any open source (the city's current list is all
  rights reserved; MHLW's file holds few, below). So whether an expired row's
  premises renewed or closed cannot be seen row by row; the official stock
  says nearly all renewed. Open call 1.

**Duplicates**: 2 rows identical in every field but `_id` / `NO`; 2 許可番号
repeat (8,840 distinct of 8,842; three numbering shapes, `9999-99999` 4,746,
`99999999` 2,851, `99999` 1,245); 30 rows repeat an (address, trade name,
type). Step 2's one pin per premises takes them.

### The city's own coordinates

- **Every row has 緯度 / 経度**, decimal degrees, all inside the city's N03
  extent (lat 36.452 to 36.649, lon 136.569 to 136.796): JGD2011 / WGS84
  (indistinguishable at this scale; no old Tokyo Datum offset, below).
  4,788 distinct points. The datastore types them `numeric`, so the dump's
  decimal places (2 to 8) are not evidence of precision.
- **One default point: 389 rows sit at a single point at the city hall**,
  every one a vehicle or stall (業態 自動車営業 226, 露店 99, 大型車 50, 小型車
  12; 41 with no address), and those 389 are the only rows with a 備考: one
  fixed 24-character note. All 389 fall out before the join (not a premises,
  or temporary / mobile by 業態).
- **Against MLIT's block point** (storefronts at the block tier): **median
  33 m, 96.6% within 250 m**, 94 over 1 km (7,197 rows); against the
  town-chōme centroid, median 127 m (445 rows). The built publishers measure
  32-51 m (`japan_step2.DATUM_OFFSET_M`).
- **Default points** (`shared_points`, 3+ towns): 8 among storefront rows;
  `OWN_POINT_FALLBACK` would refuse 7 non-block rows on them and place 640.

### MHLW's file (17201) — the control

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=17201_food_business_all.csv`:
**574,826 B, 1,430 rows** (届出 1,128, 許可 302; no closures), permits
2021-09-01 to **2026-08-01**. **Kanazawa enters few permits there**: **189
open restaurant permits (3% of the official count)**, 150 with an address and
a point; by 許可 year 2021 10 · 2022 24 · 2023 36 · 2024 49 · 2025 37 · 2026
33. **111 were granted after the snapshot**; 48 of those share a trade name
with a snapshot row (renewals of a listed premises), so about 60 are new
restaurants. Most live rows are notifications (コップ式自動販売機 336, その他の
食料・飲料販売業 290, vending 200, 百貨店・総合スーパー 103). 法人名 filled on
1,173 (1,140 with a company or cooperative marker, 31 with neither a marker
nor a 法人番号); the name rule flags 2 rows. **MHLW adds no current register
worth building on**: open call 2.

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 17201)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/17201-24.0a.zip` (567,791 B)
and `https://nlftp.mlit.go.jp/isj/dls/data/19.0b/17201-19.0b.zip` (19,231 B):
**97,088 block keys, 920 town-chōme keys.** One municipality, no wards
(`"wardless": True`). Measured with `japan_register` and `WAVE2_RULES`
unchanged (no Minato re-run needed).

| Tier | Storefronts (7,844) | Food service (5,839) | Retail (2,005) |
|---|---|---|---|
| Block | **91.8%** | 92.5% | 89.5% |
| Town-chōme / 大字 centroid | 5.7% | 5.2% | 6.9% |
| Unplaced | 2.6% (202) | 2.2% | 3.6% |
| **Block or the city's own point** (`OWN_POINT_FALLBACK`) | **~99.9%** (7 refused as default points) | | |

- **The town-chōme tier** is mostly newer 区画整理 districts whose blocks
  MLIT's block edition lacks: 昭和町, 戸板西1丁目, 無量寺4丁目, 田上さくら2-3丁目,
  八日市出町, 田上本町4丁目, 広岡3丁目, 畝田西3丁目, … (Fukuoka's call: the
  publisher's point for chōme-tier rows too).
- **The unplaced rows are Kanazawa's イロハ sections**, a katakana letter
  after the town: 無量寺町ヲ (14), 沖町イ, 桂町イ, 若松町セ, 示野町ロ, 福久町ホ,
  高柳町ニ, plus 打木町東, 諸江町上丁 / 中丁, 下本多町, 池田町. Every one carries
  the city's own point, so the fallback places them; a join rule for the
  letter is optional shared code (read MLIT's 小字 for these towns first).
- The block join stays primary (every Japanese build's order); the city's
  point is the fallback, as MHLW's is in Fukuoka.

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (17201)

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_17_GML.zip`, N03 code
17201 (468.7 km²; extent W 136.5571, S 36.3382, E 136.8172, N 36.6742).
**21 station records inside, 21 `N02_005g` groups.** N02-24 and N02-25 agree
on every station here; use N02-25 (the wave's default).

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 浅野川線 (北陸鉄道, 12) | Hokutetsu Asanogawa Line | **10 / 12** (83%) | 北鉄金沢, 七ツ屋, 上諸江, 磯部, 割出, 三口, 三ツ屋, 大河端, 北間, 蚊爪 |
| 石川線 (北陸鉄道, 12) | Hokutetsu Ishikawa Line | **7 / 17** (41%) | 野町, 西泉, 新西金沢 · (押野, 野々市, 野々市工大前 in 野々市市) · 馬替, 額住宅前, 乙丸, 四十万 |
| IRいしかわ鉄道線 (IRいしかわ鉄道, 12, third sector) | IR Ishikawa Railway Line | 4 / 19 (21%) | 金沢, 東金沢, 森本, 西金沢 |

- **21 station groups inside the city** (Hokutetsu 17, IR Ishikawa 4). Every
  group holds one record. **Two interchange pairs are separate groups of
  different names**: 北鉄金沢 / 金沢 (135 m) and 新西金沢 / 西金沢 (140 m). MLIT
  keeps them apart and so does step 1 (Kobe's trap 1: Tarumi / Sanyo Tarumi);
  their rings overlap. Median gap to the nearest station **561 m**.
- **Stub test passes**: Asanogawa keeps 10 of 12 (the last two, 粟ヶ崎 and
  内灘, are in 内灘町, 0.1 and 0.5 km out); Ishikawa keeps 7 of 17 in **two
  runs**: it leaves the city after 新西金沢, crosses 野々市市 (押野, 野々市,
  野々市工大前, each 0.1 km out), comes back for 馬替 to 四十万, then runs on
  into 白山市 (陽羽里 to 鶴来). Step 1 draws track within 3 km of the city
  (`DRAW_BEYOND_M`), so the Nonoichi stretch is drawn and only its three
  stations go to `excluded_stations.csv`. IR keeps 4 of 19, cut at the line
  (野々市 in 野々市市 0.5 km out, 津幡 in 津幡町 1.6 km, 松任 in 白山市
  2.6 km). No urban line is cut to a stub.
- **The Shinkansen**: 金沢 (北陸新幹線) is inside; dropped by the standing
  call, and 金沢 stays as an IR station. JR West's Nanao Line and limited
  expresses reach 金沢 over IR's track; N02 files no JR line inside.
- **The light-rail / rail test** (the `japan-city` skill's mode rule): no
  subway, tram or light rail; all three lines are railways (class 12). No JR
  network inside, so `metro` on Kurume's and Maebashi's precedent.

**Gate 3, read by curl from the operators' own pages (2026-10-05): passes.**
Hokutetsu's line pages list **12** Asanogawa stations
(`https://www.hokutetsu.co.jp/railway/asanogawasen/`) and **17** Ishikawa
stations (`…/railway/ishikawasen/`); IR Ishikawa's timetable index lists
**19** station pages (`https://www.ishikawa-railway.jp/timetable/index.html`).
Each matches N02.

**Frequency, read from the operators' HTML station timetables by curl
(2026-10-05):**

- **Asanogawa Line** at 北鉄金沢
  (`https://www.hokutetsu.co.jp/railway/asanogawasen/hokutetsukanazawa/`,
  「全日」, the page states 「令和3年4月1日改正」): **37 departures** toward
  内灘, 6:00 to 23:00; **every 30 minutes** from 9:00 to 16:30 and 19:00 to
  21:30, every 22 to 24 minutes at 7:00-8:00 and 17:00-18:00.
- **Ishikawa Line** at 野町 (`…/railway/ishikawasen/nomachi/`, 「全日」,
  「令和6年3月16日改正」): **29 departures** toward 鶴来, 6:23 to 22:04; about
  **every 40 minutes** at midday (longest gap 54 minutes, 10:49 to 11:43), two
  to three an hour at the peaks.
- ⚠️ Both line pages also link timetable PDFs dated **2026-04-29**
  (`asanogawa-line_timetable_weekday_20260429.pdf`,
  `ishikawa-line_timetable_weekday_20260429.pdf`), newer than the revisions
  the station pages state; not fetched. Read them at build.
- **IR Ishikawa**: timetables are PDFs only (`timetable/pdf/20260314*.pdf`,
  the 2026-03-14 timetable); **not read**. ASSERTED, by general knowledge: two
  to four trains an hour through 金沢 by day. Read at build.
- Nothing read runs less often than hourly. No frequency floor applies to
  JR or private lines in Japan (the master list's row).
- ⚠️ **OSM `name:en`** for the 21 groups at build (no Overpass at Step 0).
  Read every name: 額住宅前, 四十万 (Shijima), 蚊爪 (Kagatsume), 割出 and
  北鉄金沢 (Hokutetsu-Kanazawa beside 金沢) are the ones OSM may romanise or
  translate unevenly.

## Scope

**Kanazawa City (17201), one municipality, no wards.** The Asanogawa Line
runs on into Uchinada, the Ishikawa Line into Nonoichi and Hakusan, IR
Ishikawa into Nonoichi, Hakusan and Tsubata; cut at the line, the stations
beyond named by N03 municipality at build (`excluded_stations.csv`).

## Licences — as read (the read is recorded, not repeated here)

- **The catalogue dataset (`172014-syokuhineisei-kyokashisetsu`)**: read
  2026-10-05 by a `licence-read` agent, recorded in
  `docs/decisions_drafts/staging.md`, "Band B's Japanese sources read",
  Kanazawa bullet: **PERMITTED WITH CONDITIONS.** `license_id: cc-by`, no
  version; 金沢市オープンデータ利用規約 (revised 2024-09-17; the PDF the
  portal links, `https://portal-data.city.kanazawa.ishikawa.jp/pdf/opendata_rule.pdf`)
  2(1) applies each dataset's label. **MUST DISPLAY** 2(2)'s four items in
  the form 「「…」（金沢市）（URL）を加工して作成」 and the licence title as the
  city writes it, 「クリエイティブ・コモンズ 表示」, no version. **MUST NOT**
  claim it complete, accurate or current. **Clause 5 (reimbursement of the
  city's costs arising from the user's own breach) is ACCEPTED by the owner,
  2026-10-05** (call 12, the fault-based class). **The CSV's 画像 column is
  never read.** This brief writes no verdict of its own.
- ⚠️ **Which title the credit names**: `package_show` says 「金沢市
  食品衛生関係営業許可施設一覧」, the dataset page's heading
  「食品衛生関係営業許可施設一覧」. Decide at build (the page's heading is
  what a reader following the URL sees).
- **The city site's current lists** (food 2026-04-01; barber, beauty and
  laundry 2026-03-31): all rights reserved, **not used, never fetched**.
- **MHLW open data** (control only, not drawn): PDL 1.0, as recorded for the
  built Japanese cities (`docs/data_sources/japan.md`). No notice unless open
  call 2 is reversed.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **MLIT N03**: CC BY 4.0, ⛔ never
  drawn.

## Privacy

Read only the trade name (営業所名称), the permit type and 業態, the
premises address and the row's lat/lon. **No row value was printed or
stored for this brief**: every count comes from in-memory comparisons.

- **The operator column is 法人名** (already in
  `japan_register.OPERATOR_COLS`): filled on 4,590 of 8,842 rows, **4,570
  with a company or cooperative marker** and 20 with neither (法人番号 is
  empty on every row; 7 of the 20 are 3 to 5 characters, the shape of a
  personal name). **The city names an operator almost only where it is a
  company**, Toyama's position (owner accepted it 2026-10-02): the rule
  compares what is there and cannot see a sole trader's own name elsewhere.
  It flags **3 rows (2 restaurants)**, all storefronts. The page takes
  Toyama's built bullet ("the city's lists name an operator only where it is
  a company, so this cannot be checked for the rest"), in the singular.
- **Never selected**: 営業所電話番号 (filled on 6,696 rows), 法人番号
  (empty), 備考 (one fixed note), **画像 (never read)**.
- Run `check_personal_exposure.py` with `japan=True` on what reaches the map:
  it must see the 3 flagged rows, per premises (step 2's spread rule).

## Region

`"region": "Japan East"`, `"country": "Japan"`, `label_tier: "minor"`.
Project to **UTM 53N (EPSG:32653)**: the city's centre lies at longitude
136.66 and its extent runs 136.56 to 136.82, inside the 132-138 band
(computed here, never copied).

**Scaffold**: `scaffold_city.py --slug kanazawa --name Kanazawa
--system-name "Hokuriku Railroad and IR Ishikawa Railway" --taxonomy
japan_eigyo --lat 36.561 --lon 136.656 --region "Japan East" --country Japan
--mode metro --page-number <N>` (`--dry-run` first), with the page number
claimed in `docs/session_roles.md` at build, not here. A `japan.CITIES`
entry: `"kanazawa": {"name": "金沢市", "pref": "17", "epsg": 32653, "n02":
"25", "rules": WAVE2_RULES, "wardless": True, "wards": ["17201"]}`.

## Owner calls

**Made:** Band B, food from the snapshot, its date disclosed, no personal
services (owner, 2026-10-04); the Step 0 downloads (owner, 2026-10-05, call
10); the licence read and clause 5 accepted (owner, 2026-10-05, call 12);
the standing Japanese calls above; the minor label tier and the Japan
sub-region (owner, 2026-10-02), Japan East on Toyama's and Fukui's
precedent; `metro` by the owner's mode rule of 2026-10-02 (staging's
reading, as Kurume's); the name rule on a list that names companies only
(Toyama's position, owner, 2026-10-02).

**Open:**

1. **Keep the whole snapshot, or drop the permits that have expired since.**
   43% of the storefront rows (79% of the old-law restaurant permits) have
   passed their 許可満了日 by today. Recommendation: **keep the snapshot
   whole, `FOOD_AS_OF` pinned to 2024-04-01** (Kyoto's rule: the list's own
   date, never today), and the page says "as of April 2024". The official
   stock held flat (6,420 to 6,438) while 1,169 old-law permits gave way to
   1,187 revised-law ones, so the expired rows are overwhelmingly premises
   that renewed; dropping them would erase most long-established shops and
   keep the newest. Tradeoff: some dots are premises that closed after April
   2024, which the dated caption and the standing "a permit on file, not a
   business open today" bullet cover, against a map that is 43% thinner and
   biased to permits granted after 2021.
2. **MHLW's post-snapshot permits.** Recommendation: **leave MHLW out**
   (control only, no notice). It holds 111 restaurant permits granted after
   the snapshot, about 60 of them new premises (3% of the official count;
   Kanazawa does not file its permits there). Tradeoff: about 1% more
   restaurants, current, against a second date and credit on a page whose
   one claim is "as of April 2024", and a layer that would place new
   restaurants but never the renewals of old ones.
3. **A page sentence no template covers** (a proposal for review time, if
   call 1 is answered as recommended): "About four in ten of these permits
   have reached their expiry date since April 2024; renewals are not in the
   list." Its number is computed by step 2 at build (today 43% of storefront
   rows).

**For staging (not an owner call):** correct the master list row's
restaurant count (6,478, not 5,412; 101% of the official count at the
snapshot's date, not 84%).

## What the build must still measure

- The config: `SOURCES` (`food`), `SOURCE_FILES` pinned to the datastore
  dump (the resource's own download path answers 500), `REQUIRED_COLUMNS`
  (営業所名称, 営業の種類, 業態, 営業所所在地, 緯度, 経度, 法人名, 許可満了日),
  `OWN_POINT_FALLBACK = {"food"}` (640 of 647 non-block rows; the datum
  guard passes at 33 m), `FOOD_AS_OF` per open call 1, `OFFICIAL_SHARES`
  (note it reads FY2024, a year after the snapshot; FY2023's 6,420 is the
  like-for-like count). Every column is already in `NAME_COLS`, `ADDR_COLS`,
  `TYPE_COLS`, `FORM_COLS` and `OPERATOR_COLS`; no shared-code change is
  needed to read the file.
- Whether the dataset has been replaced (`package_show`'s
  `metadata_modified` 2024-07-16; the checks below watch it). A newer
  edition would be a different, current source: re-measure, never merge.
- ⚠️ **The Economic Census join control** (`scripts/japan_census_control.py`,
  after step 2): the 2021 census has **2,664** 飲食店 establishments in
  17201. 5,820 Food service pins is **2.18 per establishment**, above the
  built cities' 1.56-1.92 (Toyama's brief predicted 2.4 before
  de-duplication). Report it with whatever the control finds; the snapshot
  itself reproduces the official permit count.
- The イロハ-section misses (above), and the 7 rows refused at default
  points.
- Gate 3 passed on the operators' pages; OSM `name:en` for 21 groups; the
  2026-04-29 Hokutetsu PDFs and IR's 2026-03-14 PDFs for the frequency; line
  colours on both basemaps.
- The 菓子 / そうざい factory share, printed by step 2 (Step 0: 54 of 1,225
  pins, 4.4%).

```brief-checks
[
  {
    "id": "kanazawa-package",
    "claim": "The catalogue record for 172014-syokuhineisei-kyokashisetsu still declares cc-by, still dates its last change 2024-07-16 (a newer date means a new edition: re-measure) and still lists resource 09a49521 at 2,568,426 B",
    "kind": "http_contains",
    "url": "https://catalog-data.city.kanazawa.ishikawa.jp/api/3/action/package_show?id=172014-syokuhineisei-kyokashisetsu",
    "present": ["\"license_id\": \"cc-by\"", "\"metadata_modified\": \"2024-07-16T03:00:00\"", "09a49521-cabf-40b4-978b-bd61ef02f650", "\"size\": 2568426"]
  },
  {
    "id": "kanazawa-rows",
    "claim": "The snapshot (permits in term in early April 2024) holds 8,842 rows",
    "kind": "ckan_rows",
    "domain": "catalog-data.city.kanazawa.ishikawa.jp",
    "resource_id": "09a49521-cabf-40b4-978b-bd61ef02f650",
    "expect": 8842
  },
  {
    "id": "kanazawa-fields",
    "claim": "The resource exposes the columns the build reads, its own coordinates and the operator column 法人名",
    "kind": "ckan_fields",
    "domain": "catalog-data.city.kanazawa.ishikawa.jp",
    "resource_id": "09a49521-cabf-40b4-978b-bd61ef02f650",
    "present": ["営業所名称", "営業の種類", "業態", "営業所所在地", "緯度", "経度", "法人名", "許可年月日", "許可満了日"]
  },
  {
    "id": "kanazawa-dump-live",
    "claim": "The datastore dump, the resource page's own download link (its upload path answers 500), serves the CSV keyless",
    "kind": "http_ok",
    "url": "https://catalog-data.city.kanazawa.ishikawa.jp/datastore/dump/09a49521-cabf-40b4-978b-bd61ef02f650?bom=true",
    "min_bytes": 2500000
  },
  {
    "id": "kanazawa-terms-linked",
    "claim": "The portal still links its open-data terms PDF (金沢市オープンデータ利用規約, read 2026-10-05)",
    "kind": "http_contains",
    "url": "https://portal-data.city.kanazawa.ishikawa.jp/",
    "present": ["pdf/opendata_rule.pdf"]
  },
  {
    "id": "kanazawa-mhlw-live",
    "claim": "MHLW's open-data file for Kanazawa (17201), the control, answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=17201_food_business_all.csv",
    "min_bytes": 400000
  },
  {
    "id": "kanazawa-isj-live",
    "claim": "MLIT's block-level address file for Kanazawa (17201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/17201-24.0a.zip",
    "min_bytes": 400000
  },
  {
    "id": "kanazawa-asanogawa-12-stations",
    "claim": "Hokutetsu's Asanogawa Line page links its 12 station pages, as N02 has 12 (gate 3), and the 2026-04-29 weekday timetable PDF",
    "kind": "http_contains",
    "url": "https://www.hokutetsu.co.jp/railway/asanogawasen/",
    "present": ["/asanogawasen/hokutetsukanazawa/", "/asanogawasen/nanatsuya/", "/asanogawasen/kamimoroe/", "/asanogawasen/isobe/", "/asanogawasen/waridashi/", "/asanogawasen/mitsukuchi/", "/asanogawasen/mitsuya/", "/asanogawasen/okobata/", "/asanogawasen/kitama/", "/asanogawasen/kagatsume/", "/asanogawasen/awagasaki/", "/asanogawasen/uchinada/", "asanogawa-line_timetable_weekday_20260429.pdf"]
  },
  {
    "id": "kanazawa-ishikawa-17-stations",
    "claim": "Hokutetsu's Ishikawa Line page links its 17 station pages, as N02 has 17 (gate 3), and the 2026-04-29 weekday timetable PDF",
    "kind": "http_contains",
    "url": "https://www.hokutetsu.co.jp/railway/ishikawasen/",
    "present": ["/ishikawasen/nomachi/", "/ishikawasen/nishiizumi/", "/ishikawasen/shinnishikanazawa/", "/ishikawasen/otomaru/", "/ishikawasen/magae/", "/ishikawasen/nukajyutakumae/", "/ishikawasen/shijima/", "/ishikawasen/oshino/", "/ishikawasen/nonoichi/", "/ishikawasen/nonoichikoudaimae/", "/ishikawasen/hibari/", "/ishikawasen/douhouji/", "/ishikawasen/inokuchi/", "/ishikawasen/sodani/", "/ishikawasen/hinomiko/", "/ishikawasen/oyanagi/", "/ishikawasen/tsurugi/", "ishikawa-line_timetable_weekday_20260429.pdf"]
  },
  {
    "id": "kanazawa-ir-19-stations",
    "claim": "IR Ishikawa Railway's timetable index links all 19 station pages, as N02 has 19 (gate 3), and the 2026-03-14 Kanazawa station timetable PDF",
    "kind": "http_contains",
    "url": "https://www.ishikawa-railway.jp/timetable/index.html",
    "present": ["station/kurikara/", "station/tsubata/", "station/morimoto/", "station/higashi_kanazawa/", "station/kanazawa/", "station/nishi_kanazawa/", "station/nonoichi/", "station/matto/", "station/kaga_kasama/", "station/nishi_matto/", "station/mikawa/", "station/komaiko/", "station/nomi_neagari/", "station/meiho/", "station/komatsu/", "station/awazu/", "station/iburihashi/", "station/kaga_onsen/", "station/daishoji/", "pdf/20260314kanazawa1.pdf"]
  },
  {
    "id": "kanazawa-asanogawa-frequency-page",
    "claim": "The Hokutetsu-Kanazawa station timetable read for the Asanogawa frequency (37 departures, every 30 minutes by day) still states its 2021-04-01 revision; a change means re-reading it",
    "kind": "http_contains",
    "url": "https://www.hokutetsu.co.jp/railway/asanogawasen/hokutetsukanazawa/",
    "present": ["令和3年4月1日改正", "内灘方面"]
  },
  {
    "id": "kanazawa-ishikawa-frequency-page",
    "claim": "The Nomachi station timetable read for the Ishikawa Line frequency (29 departures, about every 40 minutes by day) still states its 2024-03-16 revision",
    "kind": "http_contains",
    "url": "https://www.hokutetsu.co.jp/railway/ishikawasen/nomachi/",
    "present": ["令和6年3月16日改正", "鶴来方面"]
  },
  {
    "id": "kanazawa-projected-crs",
    "claim": "Kanazawa projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 136.66,
    "expect": "EPSG:32653"
  }
]
```
