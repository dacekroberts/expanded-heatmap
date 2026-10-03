# Nishinomiya — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live). Run `python scripts/brief_check.py nishinomiya` before writing any
code. Then the `japan-city` skill. Coordinates: the `address-join` skill,
measured with `pipeline/countries/japan_register.py`'s own functions from a
scratch script (`scripts/screen_japan_join.py` has no Nishinomiya entry; its
table is shared code and was not edited). Rail: MLIT N02-25 cut at the N03
city line, from the shared cache.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; no Shinkansen station is inside); (2) **lines served only by
limited expresses DO count** (2026-09-28); (3) **the city line only**: only
stations inside the city get rings, JR and the private lines are cut at the
line, a one-station stub stays as cut, and an URBAN line cut to a stub goes
back to the owner (2026-09-24, 2026-09-27); (4) **菓子製造業 and そうざい製造業
count, in Retail**, the factory share measured and kept (2026-09-24,
2026-09-27); (5) **the name rule**: where the trade name IS the operator's own
name, the pin shows its permit type, the operator column read in memory only
(2026-09-27); (6) **no page says "currently operating"**. Fault-based cost
clauses are accepted for all of Japan (2026-09-24); English station names from
OSM `name:en`, numerals as figures before 丁目.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02):**
Nishinomiya joins them as the 2026-10-01 batch did: `label_tier: "minor"`
(dot and tooltip in every view, pill only in its own region), in the Japan
sub-region that batch creates. It sits about 15 km from built Kobe's centre
and 15 km from Osaka's, so its macro label is placed by
`check_macro_labels.py`, never by eye.

**✅ `mode`: `metro`.** The owner's rule (2026-10-02): Dublin's precedent
unless JR is the city's largest rail network. Here JR has 5 station groups
against Hanshin's 10 and Hankyu's 8, and there is no tram or light rail: the
backbone is two private heavy-rail networks, which reads `metro`.

---

## The one-line summary

**All three buckets from the city's own portal (にしのみやオープンデータ, PDL 1.0):
a full food-permit list (5,648 rows as of 2026-08-31; 4,677 restaurant rows,
104% of the official 4,505) and barber (204), beauty (875) and laundry (147)
registers as of 2026-09-30.** The block join places **98.8%** of fixed food
premises and **99.7%** of the registers at the block; nothing material is
unplaced. Rail: Hanshin, Hankyu and JR West, 22 station groups, **three urban
lines cut to two or three stations** (🚨 below). ⚠️ The laundry register holds
62% of the official count. **Band A recommended.**

---

## Business leg — the city's portal (`opendata.nishi.or.jp`)

A portal of its own (no CKAN). Each dataset is a detail page,
`https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=<n>` (a plain GET
answers), whose download buttons name files under
`https://opendata.nishi.or.jp/opendata/files/<n>/<file>`; **each file answers a
plain keyless GET**. The file names change each month (the food list
`R8.8ichiran_syokuhin.xlsx`, the registers `2026.9.xlsx`), so the build pins
the current names, and a later edition is a brief to correct. Publisher:
生活衛生課.

| | Food (id 9, 食品営業許可施設) | Barbers and beauty (ids 49 理容所情報, 50 美容所情報) | Laundries (ids 67 クリーニング所（一般）情報, 68 クリーニング所（取次）情報) |
|---|---|---|---|
| **File** | `https://opendata.nishi.or.jp/opendata/files/9/R8.8ichiran_syokuhin.xlsx` | `https://opendata.nishi.or.jp/opendata/files/49/2026.9.xlsx` (and `…/files/50/2026.9.xlsx`, the same workbook) | `https://opendata.nishi.or.jp/opendata/files/67/2026.9cleaning.xlsx` (and `…/files/68/2026.9cleaning.xlsx`, the same workbook) |
| Bytes | **465,220** | **140,626** (id 50: 140,621) | **35,412** (id 68: 35,397) |
| Rows | **5,648** (one sheet; two title rows above the header) | sheet `理容` **204**, sheet `美容` **875** | sheet `一般` **40**, sheet `取次` **107** |
| As of | **2026-08-31** (title 「食品営業許可施設一覧（令和8年8月末　施設一覧）」; newest 施行日 2026-08-31; page updated 2026-09-08) | **2026-09** (file name; newest 確認年月日 2026-09-29; registered and updated 2026-10-01 / 10-02) | 2026-09 (as barbers) |
| Cadence | monthly (the full list plus each month's new permits, `R8.<m>shinki_syokuhin.xlsx`) | new on the portal 2026-10-01; cadence not stated | as barbers |
| Columns | 許可番号, 申請者氏名, **営業所所在地**, **営業所名称**, 営業所電話番号, **業種**, 施行日, 有効期限 | 確認番号, **開設者住所**, 開設者電話番号, 開設者法人名称, 開設者役職, 開設者氏名, **施設所在地**, **施設名称**, 施設電話番号, **業種**, 確認年月日 | as barbers, plus 詳細業種 (一般 / 取次) |

- **Every column the build reads is already in `japan_register`'s tuples**
  (営業所所在地 / 施設所在地, 営業所名称 / 施設名称, 業種; operators 申請者氏名 and
  開設者氏名). `xlsx_rows` finds the food header below its title rows.
- **The register workbooks hold two kinds each**: ids 49 and 50 serve one
  workbook with sheets 理容 and 美容, ids 67 and 68 one with 一般 and 取次.
  Read each source by sheet (`xlsx_rows`' `sheet`, Fukui's) through
  `config.source_rows`, so the source key still decides the bucket.
- The food list's own note: premises already closed when the file is made are
  left out (「データ作成時点で既に廃業している施設は除きます」).

**Counts that matter** (`japan_eigyo` as it stands, fixed premises):

| Bucket | Types | Rows |
|---|---|---|
| Food service | 飲食店営業, 喫茶店営業 | **3,708** fixed; **4,677** restaurant rows in all, of which **901** are 市内一円 vehicles and stalls and 68 have no address |
| Retail | 菓子製造業 441, 食肉販売業 141, そうざい製造業 98, 魚介類販売業 88 | **763** fixed |
| Personal services | 理容所 204, 美容所 875, クリーニング所 147 (一般 40, 取次 107) | **1,226** |
| Out | manufacturing, cooking vending machines (34) | 200 fixed rows |

- **Not a premises**: the list's type never marks a vehicle or stall; the
  address does (「西宮市内一円」, 901 rows, many followed by the vehicle's
  registration plate in brackets: never selected or shown). Kobe's trap 6,
  caught by `permits_from_rows` as it stands.
- **Official counts** (e-Stat 衛生行政報告例 FY2024, year end 2025-03-31): 飲食店営業
  **4,505** (old law 1,548 + new law 2,957): the list's 4,677 restaurant rows
  are **104%**. 理容所 **225** (list 91%), 美容所 **956** (92%), クリーニング所
  **237** of which 取次所 180 (**list 62%**: 一般 40 of 57, 取次 107 of 180).
- **Expiry**: 有効期限 runs 2026-11-30 to 2033-08-31; none is past on the
  list's date. Pin `as_of` to it (Kyoto's rule).

### MHLW's file — not needed

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=28204_food_business_all.csv`:
405,585 B, 1,264 rows (許可 158, 届出 1,095, closed 11); **134 open
restaurant permits, 3% of the official count**, and **all 104 it places are
already in the city's list** (same town, block and trade name). The city's
list is the food source; MHLW's notifications left out as Toyama's, so no
MHLW credit.

### Operator columns and the name rule

- Food: **申請者氏名** (filled on 5,562 of 5,648; company markers on 2,743).
  Registers: **開設者氏名** on every row (an individual, or a company's
  representative, with the company in 開設者法人名称). Both are in
  `OPERATOR_COLS` already.
- Measured in memory: **2 food rows** whose trade name is the operator's own
  name; registers 0.
- **開設者住所 and 開設者電話番号 are an operator's own address and phone**
  (filled on 35 barbers, 282 beauty salons, 99 laundries): never selected.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 28204)

Block `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28204-24.0a.zip`
(154,130 B; 7,473 block keys) and town-chōme `…/19.0b/28204-19.0b.zip`
(11,801 B; 435). **Ward-less** (`"wardless": True`): Nishinomiya has no wards.

| Tier | Food (4,671 fixed) | Barbers (204) | Beauty (875) | Laundries (147) |
|---|---|---|---|---|
| Block | **98.8%** | **100.0%** | **99.7%** | **99.3%** |
| Town-chōme / 大字 centroid | 1.2% | 0.0% | 0.2% | 0.7% |
| Unplaced | 0.0% | 0.0% | 0.1% (1) | 0.0% |

The centroid tier is the mountain north (山口町, 塩瀬町名塩 with its 字) and
浜松原町. **Independent check**: the city's lists carry no coordinates; MHLW's
own points for its Nishinomiya rows against the block point: **median 51 m,
97.1% within 250 m** (556 rows, 4 over 1 km).

---

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (28204)

N03 extent S 34.6722, W 135.2297, N 34.8613, E 135.3843 (100 km²: the
coastal city and, beyond the Rokkō hills, 山口町 and 塩瀬町). **27 station
records inside, 22 N02_005g groups** (widest 140 m). No Shinkansen.

| Operator | N02 line (class) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|---|
| 阪神電気鉄道 | 本線 (12) | Hanshin Main Line | 7 / 33 | 武庫川, 鳴尾・武庫川女子大前, 甲子園, 久寿川, 今津, 西宮, 香櫨園 |
| 阪神電気鉄道 | 武庫川線 (12) | Hanshin Mukogawa Line | **4 / 4** | 武庫川, 東鳴尾, 洲先, 武庫川団地前 |
| 阪急電鉄 | 今津線 (12) | Hankyu Imazu Line | 6 records / 11 (5 stations) | 今津, 阪神国道, 西宮北口 (twice: the line's north and south halves meet there), 門戸厄神, 甲東園 |
| 阪急電鉄 | 甲陽線 (12) | Hankyu Kōyō Line | **3 / 3** | 夙川, 苦楽園口, 甲陽園 |
| 阪急電鉄 | 神戸線 (12) | Hankyu Kobe Line | **2 / 17** | 西宮北口, 夙川 |
| 西日本旅客鉄道 | 東海道線 (11) | JR Kobe Line | **3 / 59** | 甲子園口, 西宮, さくら夙川 |
| 西日本旅客鉄道 | 福知山線 (11) | JR Takarazuka Line | **2 / 30** | 生瀬, 西宮名塩 (the north, beyond the hills) |

- **22 groups: Hanshin 10, Hankyu 8, JR West 5** (an interchange counts for
  each operator; 今津 is one group for Hankyu and Hanshin). Interchanges:
  西宮北口 (Kobe / Imazu), 夙川 (Kobe / Kōyō), 武庫川 (Hanshin Main /
  Mukogawa), 今津.
- **Two different stations share a name**: JR 西宮 and Hanshin 西宮 (21
  names, 22 groups). Kobe's trap 9: operators appended to the English names.
- **Median gap to the nearest station 684 m** (closest 427 m): standard rings
  (0.6 mi outer) on the spacing rule.
- **Gate 3**: Hanshin's and Hankyu's station indexes (checks below name the
  Mukogawa and Kōyō lines' stations); JR West's per-line counts at build.
- ⚠️ The Imazu Line is two services meeting at 西宮北口 (宝塚–西宮北口 and
  西宮北口–今津); N02 files it as one line. Draw it as one public line, the
  Hankyu Imazu Line, unless `stub_test()`'s table says otherwise at build.
- ⚠️ **OSM `name:en`** for every station at build (one Overpass query, the
  session's single slot; none was run for this brief).

### 🚨 Three urban lines cut to two or three stations

Nishinomiya is a narrow strip between Amagasaki and Ashiya, so the city line
cuts the three east-west main lines and the JR Takarazuka Line short: **Hankyu
Kobe Line 2 of 17, JR Kobe Line 3 of 59, JR Takarazuka Line 2 of 30.** By the
standing call an URBAN line cut to a stub goes back to the owner.
**Recommendation: draw all three as cut**, on Sakai's precedent (the Midōsuji
Line, 3 of 20, "drawn as cut", owner 2026-10-02): each in-city station has
the city's own permits around it, both Hankyu Kobe Line stations are
interchanges (西宮北口 with the Imazu Line, 夙川 with the Kōyō Line), and the
alternative (a regional scope with Amagasaki and Ashiya) has no permit list
for those cities. The Hanshin Main Line keeps 7 of 33: cut, not a stub.

## Scope

**Nishinomiya City (28204), one municipality, no wards.** Hanshin, Hankyu and
JR run on to Amagasaki, Ashiya, Kobe and Takarazuka (the Takarazuka Line on
to Sanda); cut at the line. Kobe's map is a separate page;
nothing is shared between the two.

## Licences — read 2026-10-02

- **Nishinomiya City's five datasets — PERMITTED WITH CONDITIONS (PDL 1.0).**
  - **The grant**: the portal's terms, 西宮市オープンデータ利用規約 第2.0版
    (`https://opendata.nishi.or.jp/opendata/kiyaku.pdf`, revised 2026-06-15),
    第1: content on the portal is the city's, and PDL 1.0 applies unless a
    rights notice says otherwise. Each dataset page links these terms and
    states no other licence.
  - **MUST DISPLAY** (the terms' 1.1, filled in, per dataset): the source,
    that it was processed, **and by whom** (「編集・加工等を行ったこと及びその主体」):
    `出典：「食品営業許可施設」（西宮市）（https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=9）を加工して作成`,
    and likewise 「理容所情報」 (id=49), 「美容所情報」 (id=50),
    「クリーニング所（一般）情報」 (id=67), 「クリーニング所（取次）情報」 (id=68), with
    the project named as the processor.
  - **MUST NOT** present processed data as if the city made it unprocessed
    (1.1); the city's symbols, logos and characters are outside the licence
    (1.4 (1)).
  - **Disclaimers** (第2): no warranty of completeness or accuracy; the city
    bears no liability for use. **No cost or indemnity clause.**
- **MLIT 位置参照情報 and N02**: PDL 1.0 (the skill's notice lines). **MLIT
  N03**: CC BY 4.0, picks stations, ⛔ never drawn.

## Privacy

The food list carries **申請者氏名** and 営業所電話番号; the registers
**開設者住所, 開設者電話番号, 開設者役職, 開設者氏名** and 施設電話番号. Select only
the premises name, type and address; read the operator's name in memory for
the name rule; **never select 開設者住所 or any phone**. The 市内一円 rows'
addresses carry vehicle plates: they are not premises and never reach the
map. Run `check_personal_exposure.py` with `japan=True`. No row value was
printed for this brief.

## Region

The Japan sub-region (minor tier, above); `"country": "Japan"`. Project to
**UTM 53N (EPSG:32653)**.

## Open items

- 🚨 **The Hankyu Kobe Line (2 of 17), JR Kobe Line (3 of 59) and JR
  Takarazuka Line (2 of 30) cut short by the city line.** Recommendation: draw
  them as cut, on Sakai's Midōsuji precedent (above).
- 🚨 **The laundry register holds 147 of the official 237 (62%; FY2024 year
  end against 2026-09), where barbers and beauty hold 91% and 92%.** The
  portal published these registers for the first time on 2026-10-01.
  Recommendation: keep laundries in Personal services and say so on the page
  in one bullet (a proposal for the drafts file: "The city's laundry list
  holds about six in ten of the laundries it reported in 2025."), on the
  precedent that a partial bucket can pass when it is disclosed (Tokyo's
  per-ward shares, Kitakyushu's missing laundries). Alternative: leave
  laundries out as Kitakyushu has none.
- ⚠️ **Shared code**: a `japan.CITIES` entry only (`"pref": "28"`, `"n02":
  "25"`, `"wardless": True`, wards `["28204"]`, EPSG 32653). The register
  sheets go through `config.source_rows`; no column spelling is new.
- ⚠️ **Fetch**: the file names change monthly; pin them in
  `SOURCE_FILES`, and a renamed file is a brief to correct (the checks below
  fail on it).
- ⚠️ **The Economic Census join control** (`scripts/japan_census_control.py`):
  the 2021 census counts **1,567** 飲食店 establishments in 28204; **3,641**
  distinct placed restaurant premises is **2.32 per establishment**, inside
  the complete lists' band (2.0 to 3.3; Kobe 2.38).
- ⚠️ The 菓子 / そうざい factory share, printed by step 2.
- ⚠️ OSM `name:en` (西宮 twice), gate 3 for JR, the Imazu Line drawn as one,
  line colours on both basemaps (four operators near Kobe's palette).

```brief-checks
[
  {
    "id": "nishinomiya-food-live",
    "claim": "Nishinomiya's full food-permit list (as of 2026-08-31) is keyless and live on the city's portal",
    "kind": "http_ok",
    "url": "https://opendata.nishi.or.jp/opendata/files/9/R8.8ichiran_syokuhin.xlsx",
    "min_bytes": 300000
  },
  {
    "id": "nishinomiya-food-page",
    "claim": "The food dataset's page still offers the 2026-08 full list and links the portal's terms",
    "kind": "http_contains",
    "url": "https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=9",
    "present": ["files/9/R8.8ichiran_syokuhin.xlsx", "kiyaku.pdf"]
  },
  {
    "id": "nishinomiya-barber-beauty-live",
    "claim": "The barber and beauty workbook (2026-09) is keyless and live",
    "kind": "http_ok",
    "url": "https://opendata.nishi.or.jp/opendata/files/49/2026.9.xlsx",
    "min_bytes": 100000
  },
  {
    "id": "nishinomiya-barber-page",
    "claim": "The barber dataset's page offers the 2026-09 workbook and links the portal's terms",
    "kind": "http_contains",
    "url": "https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=49",
    "present": ["files/49/2026.9.xlsx", "kiyaku.pdf"]
  },
  {
    "id": "nishinomiya-beauty-page",
    "claim": "The beauty dataset's page offers the 2026-09 workbook",
    "kind": "http_contains",
    "url": "https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=50",
    "present": ["files/50/2026.9.xlsx", "kiyaku.pdf"]
  },
  {
    "id": "nishinomiya-laundry-live",
    "claim": "The laundry workbook (2026-09, 一般 and 取次 sheets) is keyless and live",
    "kind": "http_ok",
    "url": "https://opendata.nishi.or.jp/opendata/files/67/2026.9cleaning.xlsx",
    "min_bytes": 20000
  },
  {
    "id": "nishinomiya-laundry-pages",
    "claim": "Both laundry datasets' pages offer the 2026-09 workbook",
    "kind": "http_contains",
    "url": "https://opendata.nishi.or.jp/opendata/ResultDetail.php?id=68",
    "present": ["files/68/2026.9cleaning.xlsx", "kiyaku.pdf"]
  },
  {
    "id": "nishinomiya-terms",
    "claim": "The portal's terms of use (第2.0版, PDL 1.0) are live",
    "kind": "http_ok",
    "url": "https://opendata.nishi.or.jp/opendata/kiyaku.pdf",
    "min_bytes": 100000,
    "content_type_contains": "pdf"
  },
  {
    "id": "nishinomiya-mhlw",
    "claim": "MHLW's open-data file for Nishinomiya (28204) answers a plain keyless GET (the count control; 134 open restaurant permits on 2026-10-02)",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=28204_food_business_all.csv",
    "min_bytes": 200000
  },
  {
    "id": "nishinomiya-hanshin-stations",
    "claim": "Hanshin's station index links the Mukogawa Line's and the Main Line's in-city stations (gate 3; ASCII page names, as the server sends no charset)",
    "kind": "http_contains",
    "url": "https://www.hanshin.co.jp/station/",
    "present": ["/station/suzaki.html", "/station/higashinaruo.html", "/station/danchimae.html", "/station/kusugawa.html", "/station/koroen.html", "/station/naruo.html"]
  },
  {
    "id": "nishinomiya-hankyu-stations",
    "claim": "Hankyu's station index lists the Kōyō and Imazu lines' in-city stations (gate 3)",
    "kind": "http_contains",
    "url": "https://www.hankyu.co.jp/station/",
    "present": ["苦楽園口", "甲陽園", "門戸厄神", "甲東園", "阪神国道"]
  },
  {
    "id": "nishinomiya-isj-live",
    "claim": "MLIT's block-level address file for Nishinomiya (28204) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/28204-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "nishinomiya-projected-crs",
    "claim": "Nishinomiya projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.34,
    "expect": "EPSG:32653"
  }
]
```
