# Hiroshima — build brief

**Step 0 measured 2026-09-24 (MHLW's viewer approved by the owner, question
10).** Run `python scripts/brief_check.py hiroshima` before writing any code.
Coordinates: the `address-join` skill, measured by
`scripts/screen_japan_join.py hiroshima` and `hiroshima-mhlw`.

**✅ Decided by the owner, 2026-09-24, for every Japanese city:** (1) **the Shinkansen does not count**, since it is long-distance travel between cities; (2) **the city line only**: only stations inside the city get rings, matching the city-only permit list, with a per-line stub test at build (any urban line cut to a stub goes back to the owner); (3) **菓子製造業 and そうざい製造業 count**, in the Retail bucket (bakeries, confectioners and delis sell over a counter), with the factory and central-kitchen share measured from trade names before publishing. Open items below that ask these questions are answered.

---

## The one-line summary

**Food comes from TWO lists that split by filing channel: the city's own list
of counter applications (7,479 restaurants), and MHLW's 食品衛生申請等システム
open data for online filings (5,195 restaurants). They overlap by 1.2%, and
together make 10.7 restaurants per 1,000 residents, beside Sendai's 9.5.**
⚠️ About 14% of the total withholds its address, so about 86% can be placed.
⚠️ **No personal-services data**: the city publishes new openings as PDFs only.
So this is food service plus a partial food-retail bucket, **the Band C shape**.

---

## Business leg — two food sources, one filing split

| | City's own list | MHLW open data |
|---|---|---|
| **File** | `https://www.city.hiroshima.lg.jp/_res/projects/default_project/_page_/001/014/315/5080331-2.xlsx`: **13,880,348 B**, two sheets (個人 / 法人), **9,247 rows**, as of 2026-03-31, with monthly additions. Page `/business/shokuhin-eisei/1051268/1051957.html`; catalogued on `hiroshima-opendata.dataeye.jp` (id 5672) | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=34100_food_business_all.csv`: **4,094,641 B**, 11,940 live rows (6,674 permits), as of 2026-08 end |
| **What it holds** | **Counter (窓口) applications.** Since 2023-08 the page excludes facilities that applied online, and sends users to MHLW | **Online filings where the applicant agreed to open-data publication**, field by field |
| Columns | **営業の種類**, **施設名称**, 施設名称_カナ, **営業所所在地（所在地_連結標記）** (個人) / **施設所在地（所在地_連結標記）** (法人), 自動車登録番号, permit dates | as Fukuoka's: trade name, 営業の種類, 業態, address, **緯度 / 経度**, 申請区分 |
| Restaurants (飲食店営業, fixed) | **7,479** (① 飲食店営業 5,788 + 飲食店営業 1,690: new and old type names) | **5,195**, of which **3,419 (66%) carry an address** |

- **Overlap, measured at block level**: 40 of MHLW's addressed restaurants
  (**1.2%**). Disjoint by filing channel.
- **MHLW's restaurant permits by year**: 2021 1,178 · 2022 2,223 · 2023 1,425,
  then **114 · 143 · 112** for 2024–2026. Online filing fell away after 2023,
  so most recent permits sit in the city's own list.
- **Combined**: 12,674 restaurants, **10.7 per 1,000 residents**. **Placeable**:
  10,898, **9.2 per 1,000**.
- **Food retail**: MHLW's notifications are a PARTIAL, opt-in bucket, as in
  Fukuoka.
- ⚠️ **Personal services: none usable.** 理容所 / 美容所 are published as
  six-monthly PDFs of new openings only (`/business/seikatsu-eisei/1026699/1013502.html`),
  with no full list and no クリーニング list.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報, ward by ward

MLIT files for the **8 wards** (34101 中, 34102 東, 34103 南, 34104 西,
34105 安佐南, 34106 安佐北, 34107 安芸, 34108 佐伯).

| Tier | Own list (9,235 fixed) | MHLW, addressed (7,397) |
|---|---|---|
| Block | **95.9%** | **94.7%** |
| Town-chōme / 大字 centroid | 1.5% | 1.5% |
| Unplaced | 2.6% | 3.7% |

**Independent check**: MHLW's own coordinates against the block point sit a
**median 35 m** apart, **96.3% within 250 m** (7,006 rows).

## 🚇 Rail — MLIT N02, commuter rail INCLUDED (owner, 2026-09-24)

By general knowledge (not yet read from N02): the Astram Line, **Hiroden's
streetcars** (the network's backbone), and JR West (Sanyō Main Line, Kabe,
Geibi, Kure). ⚠️ Whether trams count here, as in Amsterdam and Oslo, is the
owner's call. ⚠️ Stations are LineStrings, so centroid them. ⚠️ Open: the
Shinkansen.

## Scope

**Hiroshima City (8 wards).** Hiroden's Miyajima line and JR run on to
Hatsukaichi and Kaita. Check at build.

## Licences — MHLW READ 2026-09-24; the city's pending

- **MHLW open data — PERMITTED WITH CONDITIONS** (PDL 1.0), exactly as in
  `fukuoka.md`: a processed-by credit naming the processor, no
  completeness or accuracy claims, no MHLW logo, and the minor OPEN point on
  免責 2) ウ (commercial reuse). That point is fine for a non-commercial site.
- **The city's own list — PERMITTED WITH CONDITIONS (PDL 1.0), read
  2026-09-24, with one OPEN point.**
  - **The grant**: the city's own open-data list names PDL 1.0 for this
    dataset (DataEye resource 12464, row 36: `食品営業許可一覧 … datasets/5672, 有, PDL1.0`),
    and the city sends licence questions to DataEye. DataEye's terms say
    「権利表記の記載がない限り「公共データ利用規約（第1.0版）」（PDL1.0）が適用」.
    The 基本方針 defines open data as data published 「二次利用可能なルールの下で」.
  - **The site default GIVES WAY, unlike Sendai's**: the website terms reserve
    reuse (「…無断で使用・複製・転載・販売・改変・印刷配布することはできません」)
    but add 「…利用規約等、特別な規定がある場合は、この取り扱いに優先する」.
  - ⚠️ **OPEN (owner)**: DataEye's only per-file entry (resource 25502)
    names the MONTHLY series and says the full list is viewable elsewhere. The
    市内全て file has no entry of its own, and it sits on the city's page,
    which declares no licence. The permitting reading is the city's
    dataset-level PDL 1.0 plus the page calling the list open data
    (「…オープンデータの非公開を申し出た施設の情報…は掲載していません」), and it is
    much better supported. The restrictive reading puts it in Sendai's
    position. **The workbook itself carries no notice**: its document
    properties and header/footer are empty, and no cell contains a licence
    word. The only route to certainty is one question to 食品指導課食品監視係
    (082-241-7404, `shokuhin-s@city.hiroshima.lg.jp`).
  - **MUST DISPLAY** (DataEye's prescribed pattern, filled in):
    `出典：「食品営業許可一覧」（広島広域都市圏・広島県オープンデータポータルサイト）（https://hiroshima-opendata.dataeye.jp/datasets/5672）を加工して作成`,
    and, per PDL 1.1, who did the processing.
  - **MUST NOT**: present processed data as the city's own; use city logos
    or symbols. **Cost**: under the city's 利用規約 第3条, claims from our
    own breach are resolved at our own cost. There is no indemnity.
  - 「適切に使用してください」 defines nothing and points to nothing. Reading only
    premises columns fits any reading of it.
- **MLIT 位置参照情報 and N02**: PDL 1.0.

## Privacy

The own list's 個人 sheet is individual operators: read only 施設名称, 営業の種類
and the address, never any operator column. MHLW's file carries 法人名,
法人住所 and phones: never read. Run `check_personal_exposure.py`.

## Region

`"region": "East Asia"`. Project to **UTM 53N (EPSG:32653)**.

## Still unknown

- ⚠️ **Whether the city's dataset-level PDL 1.0 covers the full-list file**: the owner's call, or one question to the city (both licences are read: PERMITTED WITH CONDITIONS).
- ⚠️ **Band**: food service plus partial food retail, with no personal services. Band C's shape: the owner's call.
- ⚠️ The ~14% with no published address; whether trams count. (✅ decided 2026-09-24 (owner): see the block at the top: city line only; Shinkansen out.)
- ⚠️ The Economic Census food control.

```brief-checks
[
  {
    "id": "hiroshima-own-food-live",
    "claim": "Hiroshima City's own food-permit list (counter applications, XLSX) is keyless and live",
    "kind": "http_ok",
    "url": "https://www.city.hiroshima.lg.jp/_res/projects/default_project/_page_/001/014/315/5080331-2.xlsx",
    "min_bytes": 5000000
  },
  {
    "id": "hiroshima-mhlw-live",
    "claim": "MHLW's open-data file for Hiroshima City (34100) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=34100_food_business_all.csv",
    "min_bytes": 1000000
  },
  {
    "id": "hiroshima-isj-naka-live",
    "claim": "MLIT's block-level address file for Naka ward (34101) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/34101-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "hiroshima-projected-crs",
    "claim": "Hiroshima projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 132.46,
    "expect": "EPSG:32653"
  }
]
```
