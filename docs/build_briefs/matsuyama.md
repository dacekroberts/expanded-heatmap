# Matsuyama — build brief

**Step 0 measured 2026-10-02.** Run `python scripts/brief_check.py matsuyama`
before writing any code. Coordinates: the `address-join` skill, measured with
`japan_register.py`'s own functions from a scratch config (the shared
`scripts/screen_japan_join.py` table was not edited). Build with the
`japan-city` skill.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls):** (1) **the Shinkansen does not count** (2026-09-24; none
runs here); (2) **lines served only by limited expresses count** (2026-09-28);
(3) **the city line only**: only stations inside the city get rings, a
one-station stub stays as cut, and an URBAN line cut to a stub goes back to the
owner (2026-09-24, 2026-09-27); (4) **菓子製造業 and そうざい製造業 count, in
Retail**, the factory share measured and kept (2026-09-24, 2026-09-27); (5)
**the name rule**: where the trade name IS the operator's own name, the pin
shows its permit type (2026-09-27); (6) **no page says "currently
operating"**: the lists keep closed premises. Fault-based cost clauses are
accepted for all of Japan (2026-09-24).

**✅ Minor label tier (owner, 2026-10-02):** Matsuyama carries
`label_tier: "minor"`, in a Japan sub-region per the `japan-city` skill's
standing calls (one region or a split, decided by `check_macro_labels.py`;
every Japanese city moves into it; `REGION_LABELS_ALSO["East Asia"]` gains
it). The eight built Japanese cities stay eligible for pills.

---

## The one-line summary

**All three buckets from the city's own CC BY 4.0 lists: food permits in two
CSVs (577 old-law + 7,110 new-law rows, every permit in force on 2026-03-31;
6,114 restaurants, 103% of the official 5,924), and full lists of barbers
(485), beauty salons (1,364) and laundries (245).** The join places 81.9% of
fixed food rows at block level and 99.1% at block or chōme; MHLW's own points
for the same premises would lift block-or-own to 92.7%.
⚠️ **Correction to the screen**: the food CSVs' 緯度 / 経度 columns are
declared and **EMPTY** (0 of 7,687 rows). The list carries no coordinates;
MHLW's file does, for 3,782 of its restaurants.

---

## Business leg — the city's own lists (Matsuyama Open Data)

| | Food (two CSVs) | Personal services (three XLS) |
|---|---|---|
| **Files** | `https://www.city.matsuyama.ehime.jp/shisei/opendata/metadata/shokuhin.files/382019_food_business_all_2026031.csv`: **187,839 B, 577 rows**, permits granted to 2021-05-31 (old law). `…/382019_food_business_all_2026032.csv`: **1,944,965 B, 7,110 rows**, permits from 2021-06-01 (new law). Page `/shisei/opendata/metadata/shokuhin.html` | `…/metadata/riyoushozensisetu.files/riyou.zen.xls` **210,432 B, 485 rows**; `…/biyoushozensisetu.files/biyou.zen.xls` **450,048 B, 1,364 rows**; `…/cleaningzensisetu.files/clean.zen.xls` **150,016 B, 245 rows** (取次所 168, 一般クリーニング所 77). Pages `/shisei/opendata/metadata/<name>.html` |
| As of / cadence | 令和8年3月31日時点 (2026-03-31); **年1回** (yearly). Page updated 2026-06-19; files Last-Modified 2026-05-07 | 2026-03-31; 年1回. Pages updated 2026-09-25; files 2026-04-06 |
| Format | UTF-8 CSV, the national schema (推奨データセット). The new-law file opens with an **empty line** before the header and has a trailing empty column; the old-law file's header is line 1 | **Old `.xls` (BIFF)**: `city_rows()` does not read it; `workbook_tables()` (xlrd) does |
| Columns | 全国地方公共団体コード, ID, 地方公共団体名, **施設名称1**, 施設名称2, 施設名称＿ｶﾅ, 施設名称＿英字, **営業の種類**, 業態, 所在地＿全国地方公共団体コード, 町字ID, **所在地＿連結表記**, 施設所在地＿都道府県/市区町村/町字/番地以下 (all empty), 施設方書 (empty), **緯度, 経度 (empty)**, 施設電話番号, 連絡先メールアドレス, 連絡先FormURL, 連絡先備考, 郵便番号, **申請者個人名**, 法人名, 法人番号, **法人代表者氏名**, 許可番号, 初回許可年月日, 許可年月日, 許可開始日, 許可満了日, 廃業年月日 (empty), 申請区分 (empty), 許可条件, 備考 | **施設名称１**, 施設郵便番号, **施設所在地１** (from the town: `松山市…`), 施設所在地２ (building), 施設電話番号, 開設者法人名, 開設者役職名, **開設者氏名** (laundry: 営業者法人名, 営業者役職名, **営業者氏名**), 検査確認番号記号, 検査確認番号, 許可交付日, クリーニング種別１ (laundry) |
| Dates | Old law: 許可年月日 2020-03-19 .. 2021-05-31, wareki (`R03.05.31`); new law 2021-06-01 .. 2026-03-31. **Every row's 許可満了日 is on or after 2026-03-31**: the files are the permits in force | 許可交付日 1952 .. 2026-03-27 |

**Counts that matter** (both food files; permits, not yet one pin per premises):

| Bucket | Types | Rows |
|---|---|---|
| Food service | 飲食店営業 438 + 5,642, 喫茶店営業 34 (old law) | **6,114** = 103% of e-Stat's FY2024 in force (**5,924**, 衛生行政報告例) |
| Food retail | 菓子製造業 45 + 553, そうざい製造業 15 + 207 (+ 複合型 2), 魚介類販売業 10 + 208, 食肉販売業 10 + 133 | 1,183 |
| Out | 食肉処理業, 冷凍食品 / 水産製品 / 漬物 / 密封包装 / 麺類 / 清涼飲料水 and other manufacturing, 食品の冷凍又は冷蔵業, 食品の小分け業, 調理機能を有する自動販売機, 魚介類競り売り営業 | the rest |
| Personal services | 理容所 485, 美容所 1,364, クリーニング所 245 (取次所 168 included, as Sendai's) | **2,094** |

- ⚠️ **Not a premises: 277 food rows at `保健所管内` / `保健所管轄内`** ("within the
  health center's area": 263 飲食店営業, 14 魚介類販売業), the vehicles and
  stalls. `permits_from_rows` catches `一円`, not this wording, so they fall
  to the unplaced tier today.
- **業態** is filled on the old-law file only (旅館 8, 自動販売機 32, 事業場食堂
  22 among them); the new-law file's is empty, so `FORM_RULES` sees nothing
  there.
- **One premises, several permits**: 6,114 restaurant rows, 5,851 fixed, are
  **5,656 distinct (address, trade name)** pairs.
- **The name rule**: 申請者個人名 is filled on 3,646 of 7,110 new-law rows
  (51%) and 305 of 577 old. Compared in memory, the trade name equals the
  operator's own name on **4** new-law rows (0 old), and on **1** laundry
  row. ⚠️ **`OPERATOR_COLS` does not hold 申請者個人名 or 開設者氏名**: with
  the shared columns alone the rule finds 0 food rows. Add both (and re-run
  the Minato control).
- The page warns the list may include premises closed, paused or moved to a
  notification since it was made: 「本一覧には、作成時点で休止中、廃業している…施設が含まれている場合があります」.

**MHLW's open data for Matsuyama** (`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=38201_food_business_all.csv`:
**3,770,926 B, 11,575 rows**, permits 2021-06 .. 2026-08-31): **5,800 open
restaurant permits, 3,784 (65%) with an address, 3,782 with MHLW's own
point**, plus 4,202 open notifications (届出; 1,993 with an address).
- **It duplicates the city's new-law list, not complements it**: 5,800 MHLW
  restaurants against the city's 5,642 new-law; 3,630 of MHLW's 3,784
  addressed restaurants match a city row on (town, block number, trade name).
  Permit numbers cannot be joined (the city's `第999号`, MHLW's
  `松保（生衛）第9999号`; the digits repeat across years).
- What it could add: **its own points** where the city's row joins only to
  chōme (Fukuoka's `OWN_POINT_FALLBACK`), and **notifications as a partial,
  opt-in food-retail bucket** (Fukuoka and Hiroshima). Both decided: see
  Open items.

**Missing**: no general retail (Japan's ceiling). Nothing missing within the
three buckets.

---

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, no wards)

MLIT files for **38201**: block `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/38201-24.0a.zip`
(287,763 B; 21,969 block keys) and town-chōme `…/19.0b/38201-19.0b.zip`
(15,291 B; 661 town-chōme). Matsuyama has no wards: the parsed ward is empty
on every row, and `load_city_isj` keys `松山市` to the same empty ward.

| Tier | Food, fixed (7,410) | Restaurants, new law (5,642) | Personal services (2,094) |
|---|---|---|---|
| Block | **81.9%** | 80.2% | **78.7%** |
| Town-chōme / 大字 centroid | 17.2% | 14.3% | 18.1% |
| Unplaced | 0.9% | 5.5% (the 保健所管内 rows) | 3.2% |

(The food column is both lists with the 277 保健所管内 rows set aside; the
restaurant column still counts them.) By list: barbers 72.6 / 21.6 / 5.8,
beauty 81.5 / 16.2 / 2.3, laundries 74.7 / 21.6 / 3.7.

- **Why the block tier is lower than Hiroshima's 96%**: 909 of the 1,273
  chōme-tier food rows sit in towns that DO have blocks in MLIT's file, but
  not that block number - MLIT's block file is incomplete in the 地番 areas
  (南吉田町, 堀江町, 久万ノ台, 北条辻). The rest: 甲 / 乙 地番 (夏目甲, 末町乙 on
  the 中島 islands), and 3 rows of katakana ニ for 二 (ニ番町).
- **Independent check, MHLW's own coordinates**: matched by unique trade name,
  the city's **block** hits sit a **median 34 m** from MHLW's point, **98.5%
  within 250 m** (2,759); its chōme-tier rows a median 272 m (494).
- **MHLW's own point as the fallback** (Fukuoka's `OWN_POINT_FALLBACK`): 751
  chōme-tier and 46 unplaced food rows have MHLW's point for the same
  premises, which takes block-or-own to **92.7%** (still chōme 522, unplaced
  19).

## 🚇 Rail — MLIT N02 cut at the N03 city line

Read from N02-25 (N02-24 gives the same stations), cut at N03 38201's union
(extent S 33.687, W 132.491, N 34.074, E 132.927, the 中島 islands included).
**60 stations inside** (N02_005g groups; widest 本町六丁目, 67 m; no name in two
groups). No Shinkansen.

| Operator | N02 line | Class | Inside / N02 total | Public name |
|---|---|---|---|---|
| 伊予鉄道 | 城北線 | 12 | 9 / 9 | city tram |
| 伊予鉄道 | 城南線 | 21 | 12 / 12 | city tram |
| 伊予鉄道 | 大手町線 | 21 | 5 / 5 | city tram |
| 伊予鉄道 | 本町線 | 21 | 5 / 5 | city tram (route 6) |
| 伊予鉄道 | 花園線 | 21 | 2 / 2 | city tram |
| 伊予鉄道 | 連絡線 | 21 | 2 / 2 | city tram |
| 伊予鉄道 | 高浜線 | 12 | 10 / 10 | Takahama Line |
| 伊予鉄道 | 横河原線 | 12 | 9 / 15 | Yokogawara Line (6 beyond, in Tōon) |
| 伊予鉄道 | 郡中線 | 12 | 5 / 12 | Gunchū Line (7 beyond, in Masaki and Iyo) |
| 四国旅客鉄道 | 予讃線 | 11 | 11 / 95 | JR Yosan Line |

- **The city tram is 28 distinct stops** over six N02 legal lines; 古町 is
  one group with the Takahama Line's station. The operator runs it as **routes
  1 and 2 (環状線, the loop, opposite ways), 3 (松山市駅線), 5 (JR松山駅前線) and
  6 (本町線)**, plus the **坊っちゃん列車**, a heritage service over the same
  track (iyotetsu.co.jp's route map lists six). ⚠️ `config.LINES` is the
  operator's routes over the legal lines (Tokyo's `route`), or the legal lines
  merged; decide at build. The Botchan train adds no track.
- **Stub test passes**: no line is cut to one station. The Gunchū Line keeps 5
  of 12 and the Yokogawara Line 9 of 15, neither a stub.
- Close pairs of DIFFERENT names stay apart (trap 1): 松山市 / 松山市駅,
  大手町 / 大手町駅前, 松山 / JR松山駅前. Read the list step 1 prints.
- ⚠️ **Gate 3**: Iyotetsu's route-map page lists the routes but no stop
  counts; read the operator's own maps at build. Third-party lists give the
  loop 21 to 22 stops and 本町線 5 (N02: 5).
- ⚠️ **OSM `name:en`**: not queried (no Overpass at Step 0). At build: one
  station query and one `railway=tram_stop` query (`TRAM_OSM_JSON`) in the
  N03 box above; read every name, numerals as figures (本町六丁目's English name
  ends "-6-Chome").

## Scope

**Matsuyama City (38201)**, which since 2005 includes 北条 and the 中島
islands. The Yokogawara and Gunchū lines run on to 東温市, 松前町 and 伊予市,
and JR to 今治 and 伊予市: their stations beyond the line are excluded.

## Licences — read 2026-10-02

- **The city's lists — PERMITTED WITH CONDITIONS (CC BY 4.0).**
  - **The grant**: each metadata page's ライセンス row reads `CC-BY` and
    points to the open-data site's 利用規約 (`https://www.city.matsuyama.ehime.jp/shisei/opendata/top.html#cms58510`;
    PDF `…/top.files/kiyakuR4.pdf`, 令和4年4月1日). 第2条: 「…クリエイティブ・コモンズ・ライセンス
    表示４．０国際…の下でライセンスされています」; the site says CC-BY content
    may be used 「商用も含めて自由に」.
  - **The site default gives way**: 「当ライセンスは、オープンデータサイト内の対象データのみに適用されます」;
    these lists are on that site.
  - **MUST DISPLAY** (the site's 出典表示の方法, the "modified" form):
    `この地図は以下の著作物を改変して利用しています。食品営業許可全施設一覧、理容所全施設一覧、美容所全施設一覧、クリーニング所全施設一覧、松山市、クリエイティブ・コモンズ・ライセンス 表示 4.0（https://creativecommons.org/licenses/by/4.0/）`
    ("CC BY 4.0" may replace the long form; the link may sit on the words).
    The city's open-data logo may NOT stand in for the credit.
  - **MUST NOT**: uses against public order or national security (第4条).
  - **Cost**: 第5条 puts claims from the user's own breach or third-party
    infringement at the user's cost, and asks the user to reimburse the city's
    costs from them (弁償). Fault-based, the class accepted for all of Japan
    on 2026-09-24; ⚠️ the 弁償 wording is the furthest any Japanese source has
    gone, so name it in the licence row.
- **MHLW open data** (only if the owner takes it, below): PDL 1.0, as in
  `docs/data_sources/japan.md`: `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  processed by whom, no completeness claim.
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**:
  CC BY 4.0, picks stations, ⛔ never drawn.

## Privacy

The food CSVs carry **申請者個人名** (a person, on half the rows), 法人代表者氏名,
法人名, 法人番号, 施設電話番号, 連絡先メールアドレス and 郵便番号; the XLS carry
**開設者氏名 / 営業者氏名**, 役職名, 法人名 and phones. Select 施設名称1 / 施設名称１,
営業の種類, 業態, 所在地＿連結表記 / 施設所在地１ (+２), クリーニング種別１ and the
dates only; the operator columns are read in memory for the name rule, never
kept. Run `check_personal_exposure.py` with `japan=True`.

## Region

`"region": "East Asia"` until the Japan sub-region lands (minor tier, above).
Project to **UTM 53N (EPSG:32653)**.

## Open items

- ✅ **`mode`: `tram` (owner, 2026-10-02).** JR Yosan 11 stations against the city tram's 35 and Iyotetsu's suburban lines. The owner's rule (2026-10-02): Dublin's precedent, so commuter rail drawn beside a tram does not make a city `metro`, "unless there is substantial JR, JR reads as metro". Staging read substantial as JR being the city's largest rail network by stations inside the city line..
- ✅ **MHLW as a second source: DECIDED, both uses (owner, 2026-10-02,
  "approve all recommendations").** The city's list is complete and carries
  every address, so MHLW adds no restaurant. Two uses, both with precedent:
  (a) its own point for the 797 rows the block join misses (block-or-own 81.9%
  → 92.7%); (b) its 4,202 notifications as a partial, opt-in food-retail
  bucket (konbini, supermarkets, greengrocers; Fukuoka, Hiroshima). Either adds
  MHLW's PDL credit and `SUPERSEDES` for the 3,630 duplicates. Decided: (a)
  yes; (b) yes, as Fukuoka and Hiroshima, disclosed as partial.
- ⚠️ **Master list correction**: the row's "7,110 new-law rows with 緯度/経度"
  is wrong; the columns are empty.
- ⚠️ Shared code at build, each followed by the Minato control
  (`screen_japan_join.py minato`, 98.0 / 0.2 / 1.8) and every city screen:
  `ADDR_COLS` += `所在地＿連結表記` (full-width low line) and `施設所在地１`;
  `NAME_COLS` += `施設名称1` and `施設名称１`; `OPERATOR_COLS` += `申請者個人名` and
  `開設者氏名`; not-a-premises += `保健所管内` / `保健所管轄内`; `.xls` sources
  through `workbook_tables`; the new-law CSV's leading empty line (header
  found by its columns); wareki dates (`R03.05.31`) if a date is read.
- ⚠️ **Economic Census join control** (`scripts/japan_census_control.py`):
  the 2021 census counts **2,038** 飲食店 establishments in 38201; 5,656
  distinct restaurant premises is **2.78 per establishment**, against the
  built cities' 1.56–1.92. The list matches the official permit count
  (103%), so the gap is the permit-to-establishment ratio; explain it at
  build before publishing.
- ⚠️ 菓子 / そうざい factory share: measured by step 2, kept.
- ⚠️ OSM `name:en` and gate 3 (above). The 坊っちゃん列車 adds no line.

```brief-checks
[
  {
    "id": "matsuyama-food-old-live",
    "claim": "Matsuyama's old-law food-permit list (permits to 2021-05, as of 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.matsuyama.ehime.jp/shisei/opendata/metadata/shokuhin.files/382019_food_business_all_2026031.csv",
    "min_bytes": 150000
  },
  {
    "id": "matsuyama-food-new-live",
    "claim": "Matsuyama's new-law food-permit list (permits from 2021-06, as of 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.matsuyama.ehime.jp/shisei/opendata/metadata/shokuhin.files/382019_food_business_all_2026032.csv",
    "min_bytes": 1500000
  },
  {
    "id": "matsuyama-food-page-cc-by",
    "claim": "The food metadata page links both 2026-03-31 CSVs and states CC-BY",
    "kind": "http_contains",
    "url": "https://www.city.matsuyama.ehime.jp/shisei/opendata/metadata/shokuhin.html",
    "present": ["382019_food_business_all_2026031.csv", "382019_food_business_all_2026032.csv", "CC-BY"]
  },
  {
    "id": "matsuyama-barber-live",
    "claim": "Matsuyama's full barber list (XLS, 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.matsuyama.ehime.jp/shisei/opendata/metadata/riyoushozensisetu.files/riyou.zen.xls",
    "min_bytes": 150000
  },
  {
    "id": "matsuyama-beauty-live",
    "claim": "Matsuyama's full beauty-salon list (XLS, 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.matsuyama.ehime.jp/shisei/opendata/metadata/biyoushozensisetu.files/biyou.zen.xls",
    "min_bytes": 350000
  },
  {
    "id": "matsuyama-laundry-live",
    "claim": "Matsuyama's full laundry list (XLS, 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.matsuyama.ehime.jp/shisei/opendata/metadata/cleaningzensisetu.files/clean.zen.xls",
    "min_bytes": 100000
  },
  {
    "id": "matsuyama-terms-cc-by-4",
    "claim": "The open-data site's terms name CC BY 4.0 and link the 令和4 terms PDF",
    "kind": "http_contains",
    "url": "https://www.city.matsuyama.ehime.jp/shisei/opendata/top.html",
    "present": ["creativecommons.org/licenses/by/4.0", "kiyakuR4.pdf"]
  },
  {
    "id": "matsuyama-mhlw-live",
    "claim": "MHLW's open-data file for Matsuyama (38201) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=38201_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "matsuyama-isj-live",
    "claim": "MLIT's block-level address file for Matsuyama (38201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/38201-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "matsuyama-projected-crs",
    "claim": "Matsuyama projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 132.77,
    "expect": "EPSG:32653"
  }
]
```
