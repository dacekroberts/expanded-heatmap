# Nara — build brief

> ✅ **Owner's calls (owner, 2026-10-02: "approve all recommendations"):** **Built despite thin rail** (14 station groups), Band A.


**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live; the downloads are the city's own files, MHLW's file and MLIT's ISJ
zips). **Run `python scripts/brief_check.py nara` before writing any code.**
Then the `japan-city` skill: Kitakyushu's shape (MHLW's filings plus the
city's own list of pre-2021-law permits still in term) with three registers.
Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from a scratch script
(`scripts/screen_japan_join.py` has no Nara entry; its table is shared code).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none here); (2) **lines served only by limited expresses DO
count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27), and an URBAN line cut to a stub goes back to
the owner; (4) **菓子製造業 and そうざい製造業 count, in Retail**, factory share
measured and kept (2026-09-24, 2026-09-27); (5) **the name rule**: where the
trade name IS the operator's own name, the pin shows its permit type
(2026-09-27); MHLW's rows have no operator column (Fukuoka's precedent,
accepted); (6) **no page says "currently operating"**: the lists keep closed
premises; fault-based cost clauses are accepted (2026-09-24).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Nara
carries `label_tier: "minor"`, in the Japan sub-region the 2026-10-02 batch
creates (wave 2 only joins it).

**`mode`: `metro`.** No tram and no subway; JR has 4 station groups against
Kintetsu's 10, so the Dublin precedent applies and the backbone decides:
Kintetsu's heavy-rail commuter lines (N02 class 12), as Sakai's and
Okayama's `metro`.

---

## The one-line summary

**Food from TWO lists split by permit law: MHLW's 食品衛生申請等システム file
(4,074 open restaurant permits, 90% of the official 4,531; 78.0% publish an
address, 79.6% of fixed premises) and the city's list of pre-2021 permits (1,341
rows as of 2025-11-01; 820 still in term on 2026-08-31, about 470 of them
restaurants).** Personal services from three city registers (barbers 213,
beauty salons 837, laundries 213, as of 2026-04-01; 96-103% of the official
counts). Block join 89.6% (MHLW), 89.2% (old list), 83-92% (registers).
**Rail is thin: 14 station groups** (Kintetsu 10, JR 4), median gap 1,108 m;
no line is cut to a stub. ✅ below.

---

## Business leg

| | MHLW open data (29201) | Old-law list (city) | Barbers (city) | Beauty salons (city) | Laundries (city) |
|---|---|---|---|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=29201_food_business_all.csv` | `https://www.city.nara.lg.jp/uploaded/attachment/203480.csv` (page `/soshiki/97/10411.html`) | `https://www.city.nara.lg.jp/uploaded/attachment/209465.csv` (page `/soshiki/97/9688.html`) | `…/attachment/209467.csv` | `…/attachment/209463.csv` |
| Bytes | **2,248,456** | **163,509** | **18,472** | **78,907** | **21,109** |
| Rows | **7,157** (許可 5,152 · 届出 1,983 · 許可(廃業) 18 · 届出(廃業) 4) | **1,341** | **213** | **837** | **213** |
| As of | **2026-08 end** (newest 許可年月日 2026-08-31) | **2025-11-01** (「令和7年11月1日時点」; Last-Modified 2025-11-27) | **2026-04-01** (「令和8年4月1日更新」) | 2026-04-01 | 2026-04-01 |
| Cadence | monthly (MHLW) | irregular; holds only permits granted to 2021-05-31, so it shrinks as they expire | yearly full list, plus monthly XLSX lists of new premises | as barbers | as barbers |
| Encoding | UTF-8 CSV, BOM | UTF-8 CSV, BOM | cp932 CSV | cp932 CSV | cp932 CSV |

The city also posts each list as XLSX beside the CSV; use the CSVs.

**Columns.**
- MHLW: the national schema (as Kitakyushu's and Okayama's): 営業施設名称、屋号又は商号,
  営業の種類, 業態, 営業施設所在地, 緯度 / 経度, 法人名, 法人番号, 法人住所, 営業施設電話番号,
  the dates, 申請区分. No individual operator column.
- Old-law list: 許可番号, **申請者_氏名**, **営業所_住所１**, **営業所名称**, **業種**,
  許可年月日 (2019-02-06 to 2021-05-31), **許可有効期限** (2026-01-30 to
  2028-07-31).
- Registers: **理容所名称 / 美容所名称 / クリーニング名称**, **理容所所在地 / 美容所所在地 /
  クリーニング所在地**, **開設者氏名** (barbers: **開設者名**), **開設者代表者**,
  確認年月日 (blank on most rows). No type column: the source decides the bucket.

**Against `japan_register`'s column tuples (shared code, not edited here):**
- `ADDR_COLS` lacks **営業所_住所１**, **理容所所在地**, **美容所所在地**,
  **クリーニング所在地**: without them `city_rows` finds no header and step 2
  reads no address from the old-law list or any register.
- `NAME_COLS` covers 営業所名称; it lacks **理容所名称**, **美容所名称**,
  **クリーニング名称**.
- `OPERATOR_COLS` covers 開設者氏名 and 開設者名; it lacks **申請者_氏名** (the
  old-law list) and **開設者代表者** (a company's representative, a person, as
  代表者名).
- Measured with those spellings renamed in memory: name-rule hits 0 in the
  old-law list and 0 in each register.

**`japan_eigyo` (shared code): the old-law list files a restaurant by its
SUB-TYPE**, never as 飲食店営業: 軽飲食 145, 一般食堂 70, 居酒屋 43, めん類食堂 23,
弁当屋 22, そうざい屋 18, レストラン 17, お好焼屋 17, 焼肉屋 10, and combinations
(軽飲食・弁当屋, 居酒屋・ふぐ …) among the 820 in term. Today they fall to "no
rule": **455 restaurants lost**. Add the sub-type spellings to the restaurant
rule (スナック and 仕出し屋 are already out by their own rules: 32 and 43);
簡易菓子製造業 (3) misses `^菓子`. The 2 簡易宿所 rows are lodging, out.

**Counts that matter.**

| Bucket | MHLW (open) | Old-law list (in term on 2026-08-31) | Note |
|---|---|---|---|
| Restaurants (飲食店営業) | **4,074**, of which **3,178 (78.0%)** carry an address; fixed premises (no 一円, no vehicle or stall 業態) **3,200**, of which **2,546 (79.6%)** addressed | about **590** restaurant sub-types; **472** in Food service after the taxonomy (snack bars, catering, inns and stalls out) | e-Stat 衛生行政報告例 FY2024 in force: **4,531**. MHLW plus the old list, before any overlap: about 103% |
| First-permit years (MHLW restaurants) | 2021 391 · 2022 816 · 2023 738 · 2024 766 · 2025 756 · 2026 607 | | the city enters every new permit |
| After `japan_eigyo`, fixed, addressed | Food service **2,040**, Retail **1,316** (with notifications) | Food service 472, Retail 183 (菓子 106, 食肉 42, 魚介 19, そうざい 16) | MHLW's 業態 takes out 988 vehicles and stalls (キッチンカー 460, 露店 380 …), 120 snack bars, 86 hotels |
| 理容 / 美容 / クリーニング | | | **213 / 837 / 213**; official FY2024 year end (e-Stat 第10表 / 第11表) **218 / 809 / 217** |

- **Old-law list: drop rows past 許可有効期限** against the pinned `as_of`
  (MHLW's month end, never today; Kyoto's rule): 820 in term on 2026-08-31, 653
  on 2026-10-02. `in_term()` is on master.
- **MHLW's notifications (届出)** as a partial food-retail bucket, disclosed
  (Fukuoka's, Hiroshima's, Kitakyushu's precedent).
- **What is missing**: about 20% of MHLW's fixed restaurants withhold their
  address (by consent; the skill's MHLW bullet, "About one restaurant in five").

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 29201)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/29201-24.0a.zip` (379,711 B) and
`…/19.0b/29201-19.0b.zip` (15,061 B): 54,788 block keys, 641 town-chōme. Nara
has no wards: `"wardless": True`.

| Tier | MHLW, in a bucket, fixed, addressed (3,356) | Old-law list, in term, fixed (650) | Barbers (213) | Beauty (837) | Laundries (213) |
|---|---|---|---|---|---|
| Block | **89.6%** | **89.2%** | **84.5%** | **91.5%** | **83.1%** |
| Town-chōme / 大字 centroid | 10.3% | 10.8% | 8.5% | 7.0% | 11.7% |
| Unplaced | 0.1% | 0.0% | 7.0% | 1.4% | 5.2% |

**Independent check**: MHLW's own 緯度 / 経度 against the block point, 3,007
rows: **median 40 m, 95.1% within 250 m**, 26 over 1 km. At the chōme tier
(345 rows) a median **387 m** (37.7% within 250 m): use **MHLW's own point
for its chōme-tier rows** (`OWN_POINT_FALLBACK`, Fukuoka's call; 349 non-block
rows have one). The city's lists carry no coordinates.

⚠️ **The registers' misses are town spellings** (140 rows off the block
tier across the three, 38 of them unplaced):
ケ in the register where MLIT writes ヶ or the reverse (杉ケ中町, 秋篠梅ケ丘町), a
town without its 町 (北京終, 宝来, 三碓), 紀寺 and 西木辻 sub-towns, and the
merged eastern villages (都祁, 月ヶ瀬) at the 大字 centroid. Read them at build
against MLIT's town list; any rule goes into `japan_register` with the Minato
control re-run.

---

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (29201)

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_29_GML.zip`. N03
extent W 135.7131, S 34.5580, E 136.0711, N 34.7577 (the 2005 merger brought
in 月ヶ瀬 and 都祁, with no rail). No Shinkansen.

| N02 line (operator, class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 奈良線 (近畿日本鉄道, 12) | Kintetsu Nara Line | **6 / 19** | 大和西大寺, 菖蒲池, 学園前, 富雄, 新大宮, 近鉄奈良 |
| 京都線 (近畿日本鉄道, 12) | Kintetsu Kyoto Line | **3 / 26** | 高の原, 平城, 大和西大寺 |
| 橿原線 (近畿日本鉄道, 12) | Kintetsu Kashihara Line | **3 / 17** | 大和西大寺, 尼ヶ辻, 西ノ京 |
| 関西線 (JR西日本, 11) | JR Yamatoji Line (大和路線) | **2 / 34** | 奈良, 平城山 |
| 桜井線 (JR西日本, 11) | JR Man-yō Mahoroba Line (万葉まほろば線) | **3 / 14** | 奈良, 京終, 帯解 |

- **14 station groups inside** (17 records; 大和西大寺 is one group over three
  Kintetsu lines, 奈良 one over two JR lines). Median nearest-group gap
  **1,108 m** (min 879 m): **standard rings**.
- **Stub test, applied strictly**: no line is cut to one station. The two
  most cut are the Yamatoji Line (2 of 34) and the Kyoto Line (3 of 26); both
  are radial lines whose city stretch is short because the city's built-up
  area is small, not because the line stops: Sakai's Midōsuji (3 stations,
  drawn cut) is the precedent. Passes as cut.
- ⚠️ **学研奈良登美ヶ丘** (Kintetsu Keihanna Line) lies **105 m outside** N03's
  line, in Ikoma; it stays out under the city-line rule. 九条 (Kashihara Line)
  is 208 m outside, in Yamatokōriyama.
- ⚠️ **Names**: N02 files the public names under legal ones (関西線 is the
  Yamatoji Line, 桜井線 the Man-yō Mahoroba Line; trap 2).
- ⚠️ **Gate 3** against Kintetsu's and JR West's own station lists at build;
  **OSM `name:en`** a build-time read (no Overpass for this brief).

## Scope

**Nara City (29201), one municipality.** Kintetsu runs on to Ikoma, Kyoto
Prefecture and Yamatokōriyama, JR to Kizugawa, Yamatokōriyama and Tenri; cut
at the line.

## Licences — read 2026-10-02

- **The city's four lists — PERMITTED WITH CONDITIONS (CC BY 2.1 JP).** Each
  page (`/soshiki/97/10411.html`, `/soshiki/97/9688.html`) states 「このページに
  掲載されているデータは、クリエイティブ・コモンズ表示2.1日本ライセンスの下に提供されて
  います」 and points to the catalogue's terms (奈良市オープンデータカタログ利用規約
  第1.2版, `https://www.city.nara.lg.jp/uploaded/attachment/169004.pdf`,
  linked from `/soshiki/6/9651.html`).
  - **MUST DISPLAY** (terms ３, for edited works):
    `この地図は以下の著作物を改変して利用しています。食品営業許可施設オープンデータ、奈良市、クリエイティブ・コモンズ・ライセンス 表示 2.1（https://creativecommons.org/licenses/by/2.1/jp/）`,
    and likewise `理容所検査確認施設一覧`, `美容所検査確認施設一覧`,
    `クリーニング所検査確認施設一覧`.
  - **Cost** (５): claims from our own breach at our own cost; the fault-based
    class, accepted for all of Japan (2026-09-24). Japanese law, 奈良地方裁判所
    (７).
- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as in
  `okayama.md`: `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; no completeness claim, no logo; the open minor point 2)ウ.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **MLIT N03**: CC BY 4.0, ⛔ never drawn.

## Privacy

MHLW's file carries 法人名, 法人番号, 法人住所 and phones: never select them. The
old-law list carries **申請者_氏名** and the registers **開設者氏名 / 開設者名** and
**開設者代表者**: read in memory for the name rule only, never kept. Run
`check_personal_exposure.py` (`japan=True`). No row value was printed for this
brief.

## Region

The Japan sub-region (minor tier, above); `"country": "Japan"`. Project to
**UTM 53N (EPSG:32653)**.

## Open items

- ✅ **Thin rail: 14 station groups.** Recommendation: **build it, Band A.**
  The 14 cover the city's built-up west (Kintetsu Nara, JR Nara, Saidaiji,
  Gakuenmae, Takanohara) on five lines of two operators, no line is a stub,
  and all three buckets are full (about 3,000 placed restaurants). The
  project's "too thin" cases (Milwaukee 13, Tampa 11, Aubagne 7) were each one
  short line with one bucket. The alternative is to hold it until a second
  Nara-area city makes a regional map worth it.
- ⚠️ **Shared code** (each re-runs the Minato control and the built cities'
  screens): `ADDR_COLS` + 営業所_住所１, 理容所所在地, 美容所所在地, クリーニング所在地;
  `NAME_COLS` + 理容所名称, 美容所名称, クリーニング名称; `OPERATOR_COLS` + 申請者_氏名,
  開設者代表者; `japan_eigyo`'s old-law sub-types (455 restaurants) and
  簡易菓子製造業; the registers' town spellings. `japan.CITIES` gains
  `"nara": {"name": "奈良市", "pref": "29", "epsg": 32653, "n02": "25",
  "wardless": True, "wards": ["29201"]}`.
- ⚠️ **Old-law expiries** by 許可有効期限 against the pinned `as_of`;
  `SUPERSEDES` / one pin per premises for a renewed permit in both lists.
- ⚠️ **Economic Census join control** (`scripts/japan_census_control.py`): the
  2021 census counts **1,258** 飲食店 establishments in 29201; about 2,510 Food
  service rows is **about 2.0 per establishment**, a little above the built
  cities' 1.56-1.92; read it on the built pins.
- ⚠️ Three dates on one page: MHLW 2026-08 end, the registers 2026-04-01, the
  old-law list 2025-11-01 (filtered to the MHLW date); the page dates each.
- ⚠️ Gate 3, OSM `name:en`, the public line names, line colours on both
  basemaps; the 菓子 / そうざい factory share printed by step 2.

```brief-checks
[
  {
    "id": "nara-mhlw-live",
    "claim": "MHLW's open-data file for Nara City (29201) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=29201_food_business_all.csv",
    "min_bytes": 1500000
  },
  {
    "id": "nara-oldlaw-live",
    "claim": "The city's list of pre-2021-law food permits (2025-11-01) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.nara.lg.jp/uploaded/attachment/203480.csv",
    "min_bytes": 100000
  },
  {
    "id": "nara-food-page",
    "claim": "The food open-data page links the 2025-11-01 CSV and the CC BY 2.1 JP licence (ASCII markers: no charset sent)",
    "kind": "http_contains",
    "url": "https://www.city.nara.lg.jp/soshiki/97/10411.html",
    "present": ["203480.csv", "creativecommons.org/licenses/by/2.1/jp", "i2fas.mhlw.go.jp"]
  },
  {
    "id": "nara-registers-page",
    "claim": "The hygiene open-data page links the 2026-04-01 barber, beauty and laundry CSVs and the CC BY 2.1 JP licence",
    "kind": "http_contains",
    "url": "https://www.city.nara.lg.jp/soshiki/97/9688.html",
    "present": ["209463.csv", "209465.csv", "209467.csv", "creativecommons.org/licenses/by/2.1/jp"]
  },
  {
    "id": "nara-barber-live",
    "claim": "The barber register (2026-04-01) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.nara.lg.jp/uploaded/attachment/209465.csv",
    "min_bytes": 10000
  },
  {
    "id": "nara-beauty-live",
    "claim": "The beauty-salon register (2026-04-01) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.nara.lg.jp/uploaded/attachment/209467.csv",
    "min_bytes": 50000
  },
  {
    "id": "nara-laundry-live",
    "claim": "The laundry register (2026-04-01) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.nara.lg.jp/uploaded/attachment/209463.csv",
    "min_bytes": 10000
  },
  {
    "id": "nara-terms-pdf",
    "claim": "The catalogue's terms (利用規約 第1.2版, CC BY 2.1) are live as a PDF",
    "kind": "http_ok",
    "url": "https://www.city.nara.lg.jp/uploaded/attachment/169004.pdf",
    "min_bytes": 100000,
    "content_type_contains": "pdf"
  },
  {
    "id": "nara-isj-live",
    "claim": "MLIT's block-level address file for Nara (29201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/29201-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "nara-projected-crs",
    "claim": "Nara projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.80,
    "expect": "EPSG:32653"
  }
]
```
