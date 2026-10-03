# Yokkaichi — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live; the downloads are the city's BODIK files, MHLW's file and MLIT's ISJ
zips, each from its publisher). **Run `python scripts/brief_check.py
yokkaichi` before writing any code.** Then the `japan-city` skill. Proposed
**Band A: all three buckets** from the city's own lists. Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from a scratch script (`scripts/screen_japan_join.py` has no Yokkaichi entry;
its table is shared code and was not edited).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none in the city); (2) **lines served only by limited expresses
DO count** (2026-09-28); (3) **the city line only**: only stations inside the city
get rings, lines are cut at the line, **a one-station stub stays as cut**
(2026-09-27), and an URBAN line cut to a stub goes back to the owner; (4)
**菓子製造業 and そうざい製造業 count, in Retail**, the factory share measured
and kept; (5) **the name rule** (2026-09-27); (6) **no page says "currently
operating"**; fault-based cost clauses accepted (2026-09-24).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Yokkaichi
joins the 2026-10-01 batch's precedent: `label_tier: "minor"`, in the Japan
sub-region (by `check_macro_labels.py`, PROBLEMS 0 at 375, 768 and 1200).

**`mode`: `metro`** by the owner's rule of 2026-10-02. No subway and no tram;
JR has 5 station groups against Kintetsu's 15, so JR is not the largest
network. The backbone is Kintetsu's heavy-rail Nagoya and Yunoyama lines. The
Yokkaichi Asunarou Railway is a 762 mm narrow-gauge railway on its own right
of way, not a tram.

---

## The one-line summary

**The city publishes five standing lists as of 2026-08-31, all CC BY 4.0 on
its BODIK catalogue: food permits (3,725 rows), food notifications (1,247),
barbers (216), beauty salons (737) and laundries (106).** After the shared
taxonomy, 2,075 restaurants and cafés, 1,562 food shops (670 permit holders and
892 notified shops) and 1,050 personal-service premises remain. The block join
places 86.8% at the block and 8.3% at the town or 大字 centroid; 4.9% stay
unplaced (2.9% for the food lists with one shared address rule). **Rail: 35
station groups inside the city (Kintetsu 15, Asunarou 9, Sangi 7, JR 5, Ise
Railway 1).**

---

## Business leg — the city's BODIK catalogue (organisation 242021)

All five on `https://data.bodik.jp/dataset/…`, each resource named with its
as-of date and uploaded 2026-09-15. The catalogue states no cadence; the
resource names carry the month-end date.

| Dataset (package) | File | Bytes | Rows | Columns (the premises', and what is never selected) |
|---|---|---|---|---|
| 【三重県四日市市】食品営業許可施設一覧 (`242021_00131`) | `e5809d89-173d-40ea-9ee7-5bc4a61678a6/resource/ee120d14-40b8-4161-a650-9e8a3307dbeb/download/242021_food_business_all_20260831.xlsx` | **466,126** | **3,725** | 業種, **業態**, **営業施設屋号**, **営業施設住所**, 許可番号, 初許可日, 有効期間開始日, 有効期間終了日; operator: **申請者氏名**, **申請者代表者名**; never: 申請者住所, 申請者電話番号, 営業施設電話番号 |
| 食品営業届出施設一覧 (`242021_00136`) | `f6ff9f86-e225-4f53-982c-156f6d5be2c4/resource/c047f8a3-2602-4a81-8bfa-e7c6cdbc03f8/download/242021_eigyoutodokede_20260831.xlsx` | **160,808** | **1,247** | 業種, 営業施設屋号, 営業施設住所, 許可番号, 受付年月日; operator and never as above |
| 理容所一覧 (`242021_00111`) | `9fac6464-fcdc-45f0-91a8-fd766c1b3f39/resource/bb0550ed-b532-43f7-8e7e-3e14015496d0/download/242021_barber_20260831.xlsx` | **40,675** | **216** | 確認番号, 確認年月日, **施設住所**, **施設屋号**; operator: **開設者氏名**, **代表者氏名**; never: 開設者住所, 開設者電話番号, 施設電話番号 |
| 美容所一覧 (`242021_00112`) | `fb1ba35c-5541-4801-a63b-898b162a6ea1/resource/d90b0082-d04b-4fd7-8cfb-35d0c17dc3e8/download/242021_beauty_20260831.xlsx` | **98,590** | **737** | as barbers |
| クリーニング所一覧 (`242021_00113`) | `158b7658-dbe4-4d91-96b6-06d334fac978/resource/f40a0050-cb84-4b29-89d7-dc12b76f4516/download/242021_cleaning_20260831.xlsx` | **30,476** | **106** | as barbers, plus **区分** (取次店 70, 工場 31, 無店舗取次店 5) |

Each workbook is one sheet with its header on the first row (the first header
cell is blank). The food list's file name and schema (業態 beside 業種) are the
national 食品衛生申請等システム's: it is the city's full export from that
system, while MHLW's public file for 24202 carries only the opt-in filings
(below).

- **What the catalogue says each list leaves out**: permits 「（自動販売機、臨時・露店営業、自動車営業を除く）」;
  notifications 「（自動販売機、自動車営業、四日市市一円での営業を除く）」.
- **Standing registers, not streams.** Permits: 有効期間終了日 runs 2026-08-31
  to 2032-08-31 and no row ends before the as-of date; 初許可日 runs back to
  1928; 159 restaurant rows are old-law permits (飲食店営業（旧）). Notifications:
  受付年月日 2021-02-16 to 2026-08-25, the whole life of the 届出 system (the
  2021 law's transition required every existing notifiable business to file
  by 2021-11-30). Registers: 確認年月日 from 1951 (laundries) and 1957
  (barbers) to 2026.
- ⚠️ **Columns against `japan_register` (shared code, not edited here)**:
  `ADDR_COLS` lacks **営業施設住所** and `NAME_COLS` lacks **営業施設屋号** (the
  two food lists; without them `xlsx_rows` reads 0 rows, since it finds a
  header by its address column). The registers' 施設住所 and 施設屋号 are
  covered. `TYPE_COLS` covers 業種 but **not the laundry list's 区分**: without
  it the 5 無店舗取次店 rows are read as premises. `OPERATOR_COLS` covers
  申請者氏名, 開設者氏名 and 代表者氏名, and **lacks 申請者代表者名** (a company's
  representative, a person, as 代表者名). Add each and re-run the Minato
  control.

### Food by type, through `japan_eigyo` (measured)

| | Rows | Kept | Out (rule) |
|---|---|---|---|
| Restaurants (飲食店営業 2,696 + （旧） 159) | 2,855 | **2,074** Food service (and 1 old-law 喫茶店営業: 2,075) | **548 バー、キャバレー** (hostess, R3) · 104 委託給食 (institutional, R1) · 88 仕出屋、弁当屋 (仕出し, R1) · 41 旅館 |
| Food retail permits (菓子 351, そうざい 116, 魚介類販売 107, 食肉販売 96) | 670 | **670** Retail | |
| Other permit types (manufacturing, 添加物, 食肉処理 …) | 199 | 0 | "no rule" |
| Notifications | 1,247 | **892** Retail: その他の食料・飲料販売業 305, 乳類販売業 159, コンビニエンスストア 142, 百貨店、総合スーパー 79, 食肉販売業（包装）70, 野菜果物販売業 59, 魚介類販売業（包装）39, 米穀類販売業 30, 弁当販売業 10 … | 157 集団給食施設 · 193 manufacturing and other "no rule" · 4 mail order and 行商 |
| Barbers / beauty / laundries | 216 / 737 / 106 | 215 / 734 / 101 | 1 / 3 citywide (一円) salons; 5 無店舗取次店 |

- **The 業態 takes out 27% of restaurant rows, 19% as バー、キャバレー.** It
  is MHLW's national form list, so 「飲食店営業（バー、キャバレー）」 files plain bars with cabarets; Tokyo's
  バー・キャバレー went out whole under R3 (owner, 2026-09-29), and
  `FORM_RULES` already applies it. The precedent, not a new call.
- **The laundry 区分 工場 (31)**: a works that washes on site; kept as a
  laundry, as Hakodate's 一般 and Toyota's 洗場 (Osaka's リネンサプライ is the
  only laundry kind out).

### Completeness

Yokkaichi is neither a designated nor a core city, so e-Stat's 衛生行政報告例
city tables do not carry it; Mie Prefecture's figures include it unseparated.
**No official per-city count exists to measure against.** The Economic Census
control (below) is the check, and it reads normal.

### MHLW's file

`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=24202_food_business_all.csv`:
308,604 B, 948 rows (届出 833, 許可 114, closed 1): opt-in filings only. **Not
used**: the city's own lists are complete for permits and notifications
(Toyama's precedent for a city with a complete own list).

### Operator columns and the name rule

申請者氏名 is filled on every food row, **1,897 permit rows and 427
notification rows without a company marker**: the city publishes sole
traders' names. The rule runs: **6 permit rows and 4 notification rows
flagged**; the registers' 開設者氏名 (592 of 737 beauty salons without a company
marker) flag none. Counted in memory, nothing kept.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, 24202)

`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/24202-24.0a.zip` (415,673 B) and
`…/19.0b/24202-19.0b.zip` (11,830 B): 58,574 block keys, 438 town-chōme.
Ward-less (`"wardless": True`).

| Tier | Food service (2,075) | Permit retail (670) | Notified retail (892) | Personal services (1,050) | All (4,687) |
|---|---|---|---|---|---|
| Block | 88.6% | 86.1% | 83.0% | 86.9% | **86.8%** |
| Town-chōme / 大字 centroid | 7.3% | 8.1% | 11.7% | 7.7% | 8.3% |
| Unplaced | 4.1% | 5.8% | 5.4% | 5.4% | **4.9%** |

- **What misses**: MLIT writes **4,304 of Yokkaichi's block keys with a
  leading 大字** (大字羽津, 大字塩浜 …) that the city's lists omit (羽津甲, 塩浜,
  西阿倉川, 茂福, 日永). Stripping a leading 大字 on both sides, measured on the
  two food lists (3,637 rows): **block 86.7% → 88.3%, unplaced 4.8% → 2.9%**.
  The rest are 小字 written without 字 (大矢知町斎宮谷, 生桑町高田), left unplaced
  by design.
- ⚠️ **Recommended at build (shared code)**: a leading 大字 ignored in
  `norm_town`, with the Minato control and the built cities' screens re-run.
- **No publisher coordinates.** The independent check is GSI's address search
  on a sample at build (`screen_japan_join.gsi_check`'s method).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line (24202)

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_24_GML.zip`. N03
extent W 136.4135, S 34.9006, E 136.6886, N 35.0705. **40 station records, 35
N02_005g groups.**

| N02 line (operator) | Public name | In the city / total | Reading |
|---|---|---|---|
| 内部線 + 八王子線 (四日市あすなろう鉄道) | Asunarou Utsube Line and Hachiōji Line | **8 / 8** and **2 / 2** (日永 shared): 9 groups | wholly inside |
| 名古屋線 (近畿日本鉄道) | Kintetsu Nagoya Line | **10 / 44** | cut at the line (on to 桑名 and 鈴鹿) |
| 湯の山線 (近畿日本鉄道) | Kintetsu Yunoyama Line | **6 / 10** | cut at the line (on to 菰野) |
| 三岐線 + 近鉄連絡線 (三岐鉄道) | Sangi Line | **6 / 14** + **1 / 1** (近鉄富田) | N02 files the 近鉄富田 approach as its own legal line (trap 2): draw one public line; 15 in all, the operator's 近鉄富田–西藤原 |
| 関西線 (東海旅客鉄道) | JR Kansai Line | **5 / 19** (6 records) | cut at the line |
| 伊勢線 (伊勢鉄道) | Ise Railway | **1 / 10** (河原田) | a one-station stub: **stays as cut** (standing call); 河原田 is also JR's, and the line is regional, not urban |

- **The stub test passes**: the one stub is a regional third-sector line at an
  interchange; no urban line is cut to a stub.
- **Interchanges**: 近鉄四日市 (Nagoya and Yunoyama lines), 近鉄富田 (Kintetsu
  and Sangi), 日永, 河原田. **Close pairs kept apart**: 近鉄四日市 and
  あすなろう四日市 **33 m** (separate N02 groups, separate stations: Kobe's
  Tarumi / Sanyo Tarumi case); 富田 (JR) and 近鉄富田 390 m.
- **Median nearest-station gap 1,133 m**: standard rings.
- ⚠️ **Gate 3** at build: Asunarou (9 stations; its site did not answer from
  this machine), Sangi (15), Kintetsu and JR.
- ⚠️ **OSM `name:en`** for 35 groups at build (not queried for this brief).

## Scope

**Yokkaichi City (24202), one municipality, no wards.** Kintetsu, JR, Sangi
and the Ise Railway run on to the neighboring towns (桑名 and 鈴鹿 among
them); cut at the line.

## Licences — read 2026-10-02 (`licence-read`)

- **The city's five lists — PERMITTED WITH CONDITIONS (CC BY 4.0).** Every
  `package_show` records `license_id: cc-by-40-intl` (the food packages read by
  the licence agent, the three registers checked the same day). The city's
  catalogue terms, 四日市市オープンデータ利用規約 (`https://odcs.bodik.jp/242021/tos/`),
  第1条: 「本市等が著作権を有する著作物の利用（複製、公衆送信、翻訳・変形等の翻案等）については、クリエイティブ・コモンズ・ライセンス…の表示4.0国際（…legalcode.ja）によるものとします」;
  using the service is accepting them. The city's own page points readers to
  the catalogue; its copyright page covers web pages only. BODIK defers to
  each municipality's terms.
  - **MUST DISPLAY**: no form is prescribed, so CC BY 4.0's elements. Proposed:
    `出典：「食品営業許可施設一覧」「食品営業届出施設一覧」「理容所一覧」「美容所一覧」「クリーニング所一覧」（四日市市、2026-08-31、https://odcs.bodik.jp/242021/）を加工して作成`
    with the CC BY 4.0 link.
  - **MUST NOT**: use the city's logo or emblem without asking (第3条); imply
    endorsement (CC BY 4.0); clear third-party rights ourselves (第2条).
  - **Cost**: 第4条 settles complaints from the user's own breach or a
    third-party infringement 「利用者自身の費用と責任で解決」: the fault-based class,
    ✅ accepted for every Japanese source (2026-09-24).
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**: CC
  BY 4.0, picks stations, ⛔ never drawn.

## Privacy

Select 業種, 業態, 営業施設屋号, 営業施設住所 and the dates (food lists);
確認年月日, 施設住所, 施設屋号, 区分 (registers). 申請者氏名, 申請者代表者名,
開設者氏名 and 代表者氏名 are read in memory by the name rule and never kept.
**申請者住所 and 開設者住所 are operators' own addresses, and 申請者電話番号 and
開設者電話番号 their phones: never selected**, nor the premises' phones. Run
`check_personal_exposure.py` with `japan=True`.

## Region

The Japan sub-region (minor tier, above); until it lands, `"region": "East
Asia"`. `"country": "Japan"`. Project to **UTM 53N (EPSG:32653)**.

## Open items

- ⚠️ **The notification list as Food shops: count it** (the `japan_eigyo`
  rule: food-retail notifications count where a list publishes them, disclosed
  as partial; Tokyo's wards). It is the city's own complete list, unlike
  MHLW's opt-in filings. ⚠️ The template's standing bullet ("Food businesses
  that only notify the city … are not in the list") is then wrong for
  Yokkaichi: the replacement sentence is a proposal for the drafts file at
  build.
- ⚠️ **548 restaurant rows out as バー、キャバレー** (above): the precedent; the
  page's What Is Excluded section states the count.
- ⚠️ **Shared code**: `ADDR_COLS` + 営業施設住所, `NAME_COLS` + 営業施設屋号,
  `TYPE_COLS` + 区分, `OPERATOR_COLS` + 申請者代表者名, the leading-大字 rule,
  Yokkaichi's `japan.CITIES` entry (`"wardless": True`, `"n02": "25"`, EPSG
  32653). Each re-runs the Minato control.
- ⚠️ **The Economic Census join control** (`scripts/japan_census_control.py`,
  after step 2): the 2021 census counts **1,074** 飲食店 establishments in
  24202; 1,950 distinct placed Food-service premises (one per address and trade
  name) is **1.82 per establishment**, inside the built cities' 1.56–1.92
  (Okayama's brief). Run it on the built pins.
- ⚠️ The 菓子 / そうざい factory share, printed by step 2 (Yokkaichi is an
  industrial city).
- ⚠️ The 33 m pair, gate 3, OSM names, line colours on both basemaps.

```brief-checks
[
  {
    "id": "yokkaichi-food-live",
    "claim": "Yokkaichi's food-permit list (as of 2026-08-31) is keyless and live on BODIK",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/e5809d89-173d-40ea-9ee7-5bc4a61678a6/resource/ee120d14-40b8-4161-a650-9e8a3307dbeb/download/242021_food_business_all_20260831.xlsx",
    "min_bytes": 300000
  },
  {
    "id": "yokkaichi-notify-live",
    "claim": "Yokkaichi's food-notification list (as of 2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/f6ff9f86-e225-4f53-982c-156f6d5be2c4/resource/c047f8a3-2602-4a81-8bfa-e7c6cdbc03f8/download/242021_eigyoutodokede_20260831.xlsx",
    "min_bytes": 100000
  },
  {
    "id": "yokkaichi-barber-live",
    "claim": "Yokkaichi's barber list (as of 2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/9fac6464-fcdc-45f0-91a8-fd766c1b3f39/resource/bb0550ed-b532-43f7-8e7e-3e14015496d0/download/242021_barber_20260831.xlsx",
    "min_bytes": 25000
  },
  {
    "id": "yokkaichi-beauty-live",
    "claim": "Yokkaichi's beauty-salon list (as of 2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/fb1ba35c-5541-4801-a63b-898b162a6ea1/resource/d90b0082-d04b-4fd7-8cfb-35d0c17dc3e8/download/242021_beauty_20260831.xlsx",
    "min_bytes": 60000
  },
  {
    "id": "yokkaichi-laundry-live",
    "claim": "Yokkaichi's laundry list (as of 2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://data.bodik.jp/dataset/158b7658-dbe4-4d91-96b6-06d334fac978/resource/f40a0050-cb84-4b29-89d7-dc12b76f4516/download/242021_cleaning_20260831.xlsx",
    "min_bytes": 20000
  },
  {
    "id": "yokkaichi-food-ckan",
    "claim": "The food-permit dataset's record says CC BY 4.0 and points at the 2026-08-31 file",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=242021_00131",
    "present": ["\"license_id\": \"cc-by-40-intl\"", "242021_food_business_all_20260831.xlsx"]
  },
  {
    "id": "yokkaichi-notify-ckan",
    "claim": "The notification dataset's record says CC BY 4.0 and points at the 2026-08-31 file",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=242021_00136",
    "present": ["\"license_id\": \"cc-by-40-intl\"", "242021_eigyoutodokede_20260831.xlsx"]
  },
  {
    "id": "yokkaichi-barber-ckan",
    "claim": "The barber dataset's record says CC BY 4.0 and points at the 2026-08-31 file",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=242021_00111",
    "present": ["\"license_id\": \"cc-by-40-intl\"", "242021_barber_20260831.xlsx"]
  },
  {
    "id": "yokkaichi-beauty-ckan",
    "claim": "The beauty dataset's record says CC BY 4.0 and points at the 2026-08-31 file",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=242021_00112",
    "present": ["\"license_id\": \"cc-by-40-intl\"", "242021_beauty_20260831.xlsx"]
  },
  {
    "id": "yokkaichi-laundry-ckan",
    "claim": "The laundry dataset's record says CC BY 4.0 and points at the 2026-08-31 file",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=242021_00113",
    "present": ["\"license_id\": \"cc-by-40-intl\"", "242021_cleaning_20260831.xlsx"]
  },
  {
    "id": "yokkaichi-terms-cc-by-4",
    "claim": "四日市市オープンデータ利用規約 第1条 licenses CC BY 4.0 (the Japanese legal code linked)",
    "kind": "http_contains",
    "url": "https://odcs.bodik.jp/242021/tos/",
    "present": ["licenses/by/4.0/legalcode.ja"]
  },
  {
    "id": "yokkaichi-mhlw-live",
    "claim": "MHLW's open-data file for Yokkaichi (24202) answers keyless - opt-in filings only, not used",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=24202_food_business_all.csv",
    "min_bytes": 100000
  },
  {
    "id": "yokkaichi-isj-live",
    "claim": "MLIT's block-level address file for Yokkaichi (24202) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/24202-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "yokkaichi-projected-crs",
    "claim": "Yokkaichi projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 136.62,
    "expect": "EPSG:32653"
  }
]
```
