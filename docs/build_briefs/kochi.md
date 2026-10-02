# Kōchi — build brief

**Step 0 measured 2026-10-02.** Run `python scripts/brief_check.py kochi`
before writing any code. Coordinates: the `address-join` skill, measured with
`japan_register.py`'s own functions from a scratch config (the shared
`scripts/screen_japan_join.py` table was not edited). Build with the
`japan-city` skill. The slug is `kochi`; the name is spelled **Kōchi** with its
macron, because "Kochi" is India's discard row on the master list.

**✅ Decided by the owner for every Japanese city (the `japan-city` skill's
standing calls):** (1) **the Shinkansen does not count** (2026-09-24; none
runs here); (2) **lines served only by limited expresses count** (2026-09-28);
(3) **the city line only**: only stations inside the city get rings, a
one-station stub stays as cut, and an URBAN line cut to a stub goes back to the
owner (2026-09-24, 2026-09-27); (4) **菓子製造業 and そうざい製造業 count, in
Retail** (2026-09-24; moot on a personal-services page); (5) **the name rule**:
where the trade name IS the operator's own name, the pin shows its permit type
(2026-09-27); (6) **no page says "currently operating"**. Fault-based cost
clauses are accepted for all of Japan (2026-09-24).

**✅ Minor label tier (owner, 2026-10-02):** Kōchi carries
`label_tier: "minor"`, in a Japan sub-region per the `japan-city` skill's
standing calls (one region or a split, decided by `check_macro_labels.py`;
every Japanese city moves into it; `REGION_LABELS_ALSO["East Asia"]` gains
it). The eight built Japanese cities stay eligible for pills.

---

## The one-line summary

**Personal services only, from the city's own CC BY 4.0 lists: barbers (321)
and beauty salons (1,074) as of 2026-03-31, plus monthly additions since (2
and 18), 1,415 premises, joined at 95.4% block.** No laundry list. **Band B,
personal services only, confirmed** (Yokohama's page shape). Food stays off:
MHLW's file holds 4,564 open restaurant permits (91% of the 4,999 in force)
but only **2,459 (53.9%) publish an address**, under the bar's ~70%; on fixed
premises only it is 57.1%.

---

## Business leg — the city's 生活衛生 lists (生活食品課)

Page: `https://www.city.kochi.kochi.jp/soshiki/36/opendata.html`
(「生活衛生営業施設情報（高知市オープンデータ）」, updated 2026-08-01). The full
lists are as of 2026-03-31; **since 2026-04 the city adds only new openings**
(「令和8年4月以降、新規開設があった情報のみ追加します」), one file per month and
kind. Closures after 2026-03-31 are invisible, and the page warns the lists
may include premises paused or closed when made.

| File (all under `https://www.city.kochi.kochi.jp/uploaded/life/`) | Bytes | Rows | As of |
|---|---|---|---|
| `269801_1162162_misc.xlsx` 理容所一覧 (full) | 37,719 | **321** | 2026-03-31 |
| `269801_1162161_misc.xlsx` 美容所一覧 (full) | 103,110 | **1,074** | 2026-03-31 |
| `269801_1162163_misc.xlsx` 理容所 (new) | 10,670 | 1 | 2026-04-30 |
| `269801_1162164_misc.xlsx` 美容所 (new) | 11,405 | 7 | 2026-04-30 |
| `269801_1162165_misc.xlsx` 美容所 (new) | 10,687 | 2 | 2026-05-31 |
| `269801_1162167_misc.xlsx` 理容所 (new) | 10,643 | 1 | 2026-06-30 |
| `269801_1162168_misc.xlsx` 美容所 (new) | 11,832 | 4 | 2026-06-30 |
| `269801_1162170_misc.xlsx` 美容所 (new) | 10,282 | 1 | 2026-07-31 |
| `269801_1162171_misc.xlsx` 美容所 (new) | 11,037 | 4 | 2026-08-31 |

(The page's 旅館業 files are out of scope.) No new barber file for May, July
or August: none opened, or none published.

- **Full lists' columns** (title row, then the header): 施設番号, **施設名称**,
  **施設住所名称** (from the town: `帯屋町…`, no city name), 施設方書,
  施設電話番号, **営業者氏名**, 確認年月日 (1948 .. 2026-03-12).
- **Monthly files' columns** (a different schema): 許可番号, **営業所名称**,
  **営業所所在地** (from the prefecture: `高知県高知市…`), 営業所電話番号,
  申請者法人名, 申請者役職, **申請者名**, 許可日.
- **The name rule**: 営業者氏名 and 申請者名 are both in `OPERATOR_COLS`;
  compared in memory, **0** trade names equal the operator's own name.
- **Counts that matter**: barbers **323**, beauty salons **1,092** (after the
  additions; none repeats a full-list row), **1,415** in all; 3 beauty rows
  are not a premises.
- **Missing**: ⚠️ **no クリーニング所 list** (neither this page nor the city's
  open-data portal, `/soshiki/80/kochicity-opendata.html`, has one), as
  Kitakyushu: disclosed on the page.
- **Food, not used**: the page itself sends food readers to MHLW
  (「食品営業施設の情報（個人情報を除く）については、厚生労働省の食品衛生申請等システムで閲覧することができます」).
  MHLW's file (`https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=39201_food_business_all.csv`:
  **2,860,026 B, 9,276 rows**, permits 2021-06-01 .. 2026-08-31; the same
  bytes as the 2026-10-01 screen) has 4,564 open restaurant permits, 2,459
  with an address (53.9%). 業態 marks **687 of the restaurants 屋台** and 134
  キッチンカー; set aside every 一円 row and every vehicle or stall form and
  **2,108 of 3,693 fixed premises (57.1%)** publish an address. Where an address IS
  published the join is good (block 93.4%, MHLW's point median 33 m off, 97.6%
  within 250 m), so the gap is consent, not geocoding. **Food fails placement:
  confirmed.**

## Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, no wards)

MLIT files for **39201**: block `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/39201-24.0a.zip`
(317,357 B; 40,790 block keys) and town-chōme `…/19.0b/39201-19.0b.zip`
(11,541 B; 416 town-chōme). Kōchi has no wards: the parsed ward is empty on
every row, matching `load_city_isj`'s key for `高知市`.

| Tier | Barbers (323) | Beauty salons (1,089 fixed) | Both (1,412) |
|---|---|---|---|
| Block | 95.4% | 95.4% | **95.4%** |
| Town-chōme / 大字 centroid | 4.3% | 4.1% | 4.2% |
| Unplaced | 0.3% | 0.5% | 0.4% |

- The chōme tier is mostly 大字 + 甲 / 乙 / 丙 地番 (介良乙 18, 朝倉乙, 大津乙).
- **Unplaced: 6, all at `高埇`** (埇 is outside JIS X 0208; MHLW writes the same
  town 高そね). Mapping it is one cited variant rule in `japan_register`.
- **Independent check**: the lists carry no coordinates and MHLW has no salons.
  Run GSI's address search on a sample at build (`screen_japan_join.py`'s
  `gsi_check`, as Sendai: 150 rows, 1 request per second).

## 🚇 Rail — MLIT N02 cut at the N03 city line

Read from N02-25 (N02-24 gives the same stations), cut at N03 39201 (extent
S 33.458, W 133.394, N 33.682, E 133.626). **67 stations inside** (N02_005g
groups); widest group **朝倉, 275 m** (JR 朝倉 and the tram's 朝倉, which MLIT
groups); no name in two groups. No Shinkansen.

| Operator | N02 line | Class | Inside / N02 total | Cut |
|---|---|---|---|---|
| とさでん交通 | 伊野線 | 21 | **24 / 34** | 10 beyond, in Ino (伊野 terminus) |
| とさでん交通 | 後免線 | 21 | **25 / 33** | 8 beyond, in Nankoku (後免町 terminus) |
| とさでん交通 | 桟橋線 | 21 | 8 / 8 | |
| とさでん交通 | 駅前線 | 21 | 4 / 4 | |
| 四国旅客鉄道 | 土讃線 | 11 | 10 / 61 | on to Nankoku and Ino |

- **Tosaden is 58 distinct stops in the city** (はりまや橋 shared by all four
  legal lines). The operator runs the east-west pair as one 東西線 service
  (伊野 – はりまや橋 – 後免町) and the north-south pair (高知駅前 – はりまや橋 –
  桟橋通五丁目); decide `config.LINES` as legal lines or services at build.
- **Stub test passes**: the two longest lines keep 71% and 76% of their stops.
- The Tosa Kuroshio ごめん・なはり線 starts at 後免, outside the city: not drawn.
- ⚠️ **Gate 3**: the operator's own stop counts were not read at Step 0.
  Third-party lists give 伊野線 32 and 後免線 33 stops (N02: 34 and 33); read
  Tosaden's own route map at build and explain any difference (N02 may count
  はりまや橋 or a closed stop).
- ⚠️ **OSM `name:en`**: not queried (no Overpass at Step 0). At build: one
  station query and one `railway=tram_stop` query (`TRAM_OSM_JSON`) in the N03
  box above; numerals as figures (知寄町一丁目, 桟橋通五丁目).

## Scope

**Kōchi City (39201).** The tram runs on to Ino and Nankoku, JR to Nankoku
and Ino; their stations are excluded.

## Licences — read 2026-10-02

- **The city's lists — PERMITTED WITH CONDITIONS (CC BY 4.0).**
  - **The grant**: the page's 【オープンデータ利用ルール】:
    「本ページで公開されているデータは、Cc By（クリエイティブ・コモンズ・ライセンスの表示4.0国際）を適用します」,
    and the 高知市オープンデータ利用規約 (`/uploaded/life/269801_1162152_misc.pdf`,
    made 令和２年12月25日, following 政府標準利用規約 第2.0版 and stated
    compatible with CC BY 4.0): reuse, adaptation and commercial use allowed.
  - **MUST DISPLAY** (第1, the processed form):
    `出典：「理容所一覧」「美容所一覧」（高知市）（https://www.city.kochi.kochi.jp/soshiki/36/opendata.html）を加工して作成`
    (the as-is form adds the date of use; a processed credit may say who
    processed it).
  - **MUST NOT**: present processed data 「あたかも高知市が作成したかのような態様」;
    use the city's symbols, logos or characters (outside the terms, 第3);
    uses against law, ordinance, public order or national security (第4).
  - **Cost**: none. 第7 limits the city's own liability only.
- **MHLW open data**: not used (food is off).
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**:
  CC BY 4.0, picks stations, ⛔ never drawn.

## Privacy

The full lists carry **営業者氏名** (a person or a company) and phones; the
monthly files **申請者名**, 申請者役職, 申請者法人名 and phones. Select
施設名称 / 営業所名称 and 施設住所名称 / 営業所所在地 (+ 施設方書) only; the operator
columns are read in memory for the name rule, never kept. Run
`check_personal_exposure.py` with `japan=True`.

## Region

`"region": "East Asia"` until the Japan sub-region lands (minor tier, above).
Project to **UTM 53N (EPSG:32653)**.

## Open items

- ✅ **`mode`: `tram` (owner, 2026-10-02).** JR Dosan 10 stations against Tosaden's 58. The owner's rule (2026-10-02): Dublin's precedent, so commuter rail drawn beside a tram does not make a city `metro`, "unless there is substantial JR, JR reads as metro". Staging read substantial as JR being the city's largest rail network by stations inside the city line..
- ⚠️ **Page wording**: the approved one-bucket line is Yokohama's ("barbers,
  beauty salons and laundries"); Kōchi has no laundry list, so "barbers and
  beauty salons" is a sentence outside the template, a proposal for the drafts
  file (as Kitakyushu's).
- ⚠️ **The register after 2026-03-31 is an upper bound**: openings are added
  monthly, closures are not. Pin `as_of` to the last month read (Kyoto's call),
  never the download date.
- ⚠️ Shared code at build, each followed by the Minato control
  (`screen_japan_join.py minato`, 98.0 / 0.2 / 1.8) and every city screen:
  `ADDR_COLS` += `施設住所名称`; `NAME_COLS` += `営業所名称`; a `高埇` / `高そね`
  variant; the full lists' header sits under a title row (`xlsx_rows` finds it
  by the address column once `施設住所名称` is known).
- ⚠️ **Economic Census join control**: the shared control measures 飲食店, which
  this page does not carry. Measure the personal-services lists against the
  census's 理容業 / 美容業 establishments for 39201 instead, if the national
  table carries them; otherwise record that no control ran.
- ⚠️ Gate 3 and OSM names (above).

```brief-checks
[
  {
    "id": "kochi-barber-full-live",
    "claim": "Kōchi's full barber list (XLSX, 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kochi.kochi.jp/uploaded/life/269801_1162162_misc.xlsx",
    "min_bytes": 30000
  },
  {
    "id": "kochi-beauty-full-live",
    "claim": "Kōchi's full beauty-salon list (XLSX, 2026-03-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kochi.kochi.jp/uploaded/life/269801_1162161_misc.xlsx",
    "min_bytes": 80000
  },
  {
    "id": "kochi-beauty-newest-live",
    "claim": "The newest monthly beauty-salon addition (2026-08-31) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.kochi.kochi.jp/uploaded/life/269801_1162171_misc.xlsx",
    "min_bytes": 5000
  },
  {
    "id": "kochi-page-cc-by",
    "claim": "The 生活衛生 open-data page links the full lists and the terms PDF, and names CC BY 4.0",
    "kind": "http_contains",
    "url": "https://www.city.kochi.kochi.jp/soshiki/36/opendata.html",
    "present": ["269801_1162162_misc.xlsx", "269801_1162161_misc.xlsx", "269801_1162152_misc.pdf", "creativecommons.org/licenses/by/4.0"]
  },
  {
    "id": "kochi-mhlw-live",
    "claim": "MHLW's open-data file for Kōchi City (39201), the food source that fails placement, answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=39201_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "kochi-isj-live",
    "claim": "MLIT's block-level address file for Kōchi (39201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/39201-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "kochi-projected-crs",
    "claim": "Kōchi projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 133.53,
    "expect": "EPSG:32653"
  }
]
```
