# Kagoshima — build brief

**Step 0 measured 2026-10-02.** Run `python scripts/brief_check.py kagoshima`
before writing any code. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py`'s own functions from a scratch config
(`scripts/screen_japan_join.py`'s table is shared code and was not edited).
Band B on the master list, food only (MHLW's file counted 2026-10-01); every
figure below is re-measured.

**✅ The owner's standing calls for every Japanese city (the `japan-city`
skill) are DECIDED:** (1) **the Shinkansen does not count**; (2) **lines served
only by limited expresses DO count**; (3) **the city line only**, a per-line
stub test at build, a one-station stub stays as cut, an urban line cut to a
stub goes back to the owner; (4) **菓子製造業 and そうざい製造業 count, in
Retail**, the factory share measured and kept; (5) **the name rule**: where the
trade name IS the operator's own name, the pin shows its permit type; (6) **no
page says "currently operating"**. **Kagoshima is the minor label tier (owner,
2026-10-02)**: a Japan sub-region per the skill's standing calls, every
Japanese city moved into it, `REGION_LABELS_ALSO["East Asia"]` naming it; the
eight built Japanese cities stay eligible.

---

## The one-line summary

**Food only, from two lists split by the 2021 reform**: MHLW's
食品衛生申請等システム file carries every permit since 2021-06 (5,914 open
restaurant permits, 87% of the 6,823 in force, **76% with an address**), and
the city's own list carries the old-law permits still held (1,106 restaurants,
2026-06-30, CC BY 4.0). They overlap by 3.2% at block level. Among fixed
premises **80.5% can be placed**, above the reduced-bucket bar's 70%. Both join
to MLIT's block file at 94-96%. **No personal services**: the barber and salon
lists are a 12-month stream of new openings, with no laundry list. Rail: the
city tram (35 stops) and three JR Kyushu lines, 55 station groups.

---

## Business leg — two food sources, one split by date

| | MHLW open data (46201) | The city's old-law list |
|---|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=46201_food_business_all.csv`: **3,800,043 B**, UTF-8 with BOM, **10,132 rows** (7,629 permits, 2,483 notifications, 20 closed), latest permit **2026-08-31**; the city's page: 「更新頻度：毎月15日（食品衛生申請等システムで更新）」 | `https://www.city.kagoshima.lg.jp/kenkofukushi/hokenjo/seiei-shoku/kenko/ese/sekatsu/shoku/documents/opendetar8_6matsu.csv`: **173,060 B**, **cp932**, comma, **1,376 rows**, as of **2026-06-30** (令和8年6月末), updated quarterly (「1月、4月、7月、10月の15日」). Page `…/shoku/shokuopendata.html`, 「飲食店営業などの食品営業許可施設一覧（オープンデータ）」 |
| **What it holds** | Every permit since 2021-06 (the city's page sends all post-reform permits there); each field published only with the filer's consent | Permits granted **before 2021-06-01** and still held. Excludes 「副食、移動、仮設、短期、自動販売機」; withholds 「携帯電話番号、営業者住所及び営業者電話番号」 |
| Columns | the MHLW schema: `営業施設名称、屋号又は商号`, `営業の種類` (circled-number prefix), **`業態`**, `営業施設所在地`, `営業施設方書`, **`緯度` / `経度`**, `法人名`, `法人番号`, `法人住所`, `営業施設電話番号`, permit dates, `廃業年月日`, `申請区分` | `No.`, **`営業者氏名`** (operator), **`営業所の名称、屋号又は商号`**, **`営業所の所在地`** (`鹿児島県鹿児島市…`), `営業所の電話番号`, `営業許可番号`, `許可年月日` (wareki, `R020601`), `営業の種類`, and one empty trailing column |
| Restaurants | **5,914** open 飲食店営業 permits (2021-06-03 to 2026-08-31), **4,517 (76.4%) with an address**. Vehicles and stalls by `業態`: 仮設 388, 自動車 349 (+2); 567 of the addressed rows are at 市内一円. Fixed premises about 5,175, **3,950 addressed (76.3%)**. Through `japan_eigyo`, addressed fixed rows: **Food service 3,880** | **1,106** 飲食店営業 (+ 喫茶店営業 7). Through `japan_eigyo`: **Food service 1,113** |
| Food retail | open permits 菓子 570, そうざい 451, 魚介類 175, 食肉 151 (1,486 together, 1,060 addressed), plus notifications (その他の食料・飲料販売業 449, コンビニ 272, 野菜果物 179, 百貨店・総合スーパー 154, …). Through `japan_eigyo`, addressed fixed rows: **Retail 1,926** | 菓子 89, 食肉 40, そうざい 34, 魚介類 31: **Retail 194**; out 69 (manufacturing types) |

- **Overlap, measured at block level** (same town and block AND the same
  normalised trade name): **123 of MHLW's 3,794 block-placed restaurants
  (3.2%)** are in the old-law list; 2,272 share a block only. Disjoint by date,
  as expected; the 123 are likely renewals the quarterly list has not yet
  dropped (`SUPERSEDES` keeps one).
- **Against the official count**: e-Stat FY2024, **6,823** restaurants in
  force. MHLW 5,914 + old law 1,106 = 7,020 (103%; the official count is the
  end of FY2024 and the lists run to 2026).
- **Placement among fixed premises**: (3,950 + 1,106) / (5,175 + 1,106) =
  **80.5%**. **About one MHLW restaurant permit in four** (1,225 of 5,175
  fixed) withholds its address: Fukuoka's ADDRESS_BY_CONSENT bullet.
- **Personal services: none usable.** `…/seiei-shoku/opendate2.html`:
  「鹿児島市内で新たに届出を受けた理容所・美容所の情報を月ごとに集計し1年間公開しています」
  (monthly XLSX of new barbers and salons, kept 12 months); no laundry list.
  A stream of openings cannot rebuild a register (Five rules, rule 1).
- A stale BODIK copy of the old-law list exists (`462012_syokuhineigyoukyokasisetsu`,
  resource 2023-12-07, 608,092 B): read the city's quarterly file, not it.
- **What is missing**: personal services; non-food retail (Japan's ceiling);
  MHLW's consent-withheld addresses; the old-law list's own exclusions.

### Column coverage in the shared code (`japan_register`)

| Column | Covered? |
|---|---|
| Old-law `営業者氏名` (operator) | ✅ in `OPERATOR_COLS` |
| Old-law `営業所の所在地` | ❌ **not in `ADDR_COLS`**: every row would read as "not a premises" (no address). Add it, Kagoshima named |
| Old-law `営業所の名称、屋号又は商号` | ❌ **not in `NAME_COLS`** (MHLW's `営業施設名称、屋号又は商号` is): add it, or the name rule and the pins have no name |
| Old-law `営業の種類` | ✅ `TYPE_COLS` |
| MHLW | as Fukuoka's: no individual operator column (name rule cannot run, accepted) |

Then re-run the Minato control (98.0 / 0.2 / 1.8). **The name rule, counted in
memory** (yes/no only): old-law list 0 of 1,376.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (one municipality, no wards)

MLIT files for **46201**: block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/46201-24.0a.zip` (469,414 B),
town-chōme `.../19.0b/46201-19.0b.zip` (10,503 B). 57,146 block keys, 361
town-chōme keys.

| Tier | Old-law list, all (1,376) | Old-law restaurants (1,106) | MHLW, addressed restaurants (3,950 fixed) | MHLW, addressed food-retail permits (1,050 fixed) |
|---|---|---|---|---|
| Block | **93.7%** | **94.6%** | **96.1%** | **92.3%** |
| Town-chōme / 大字 centroid | 5.9% | 5.1% | 3.6% | 7.3% |
| Unplaced | 0.4% | 0.4% | 0.3% | 0.4% |

**Independent check**: MHLW's own coordinates against the block point, a
**median 37 m** apart, **94.8% within 250 m**, 50 beyond 1 km (3,792
restaurants); food retail median 42 m, 90.0%, 23 beyond 1 km. Read the far
ones at build (Kobe's hill 字 addresses were the cause there).

## 🚇 Rail — MLIT N02 cut at the N03 city line

**Read from N02-25**: N02-24 lacks 仙巌園 on the 日豊線 (2 of 112 inside there,
3 of 113 in N02-25). N03: `N03-20250101_46_GML.zip` (19,056,116 B), code 46201.
61 station records inside, **55 `N02_005g` groups**. The Shinkansen is dropped
(鹿児島中央 is also a JR conventional station).

| Line (N02 legal name) | Operator | Inside / network | Stub test |
|---|---|---|---|
| 第一期線 | 鹿児島市 (tram, class 21) | 11 / 11 | whole |
| 第二期線 | 鹿児島市 | 4 / 4 | whole |
| 唐湊線 | 鹿児島市 | 10 / 10 | whole |
| 谷山線 | 鹿児島市 | 14 / 14 | whole |
| 指宿枕崎線 | 九州旅客鉄道 | 14 / 36 | passes (the city runs south to 喜入) |
| 鹿児島線 | 九州旅客鉄道 | 5 / 99 (鹿児島中央, 鹿児島, 薩摩松元, 上伊集院, 広木) | a trunk cut at the line |
| 日豊線 | 九州旅客鉄道 | 3 / 113 (鹿児島, 仙巌園, 竜ヶ水) | a trunk cut at the line; not an urban line, stays as cut |

- **The tram: 35 distinct stops** (39 records; 郡元, 鹿児島中央駅前, 高見馬場
  and 武之橋 shared between legal lines). The public routes are **1系統**
  (鹿児島駅前-谷山, 24 stops) and **2系統** (鹿児島駅前-郡元 via
  鹿児島中央駅前, 20 stops). The operator's own 2022 stop table
  (`https://www.kotsu-city-kagoshima.jp/wp/wp-content/uploads/2022/04/09d0f2bcee270a4cedad2b194bfa1aa1.pdf`,
  a naming-rights list) numbers 37 rows, with 高見馬場 (1系統) / (2系統) and
  郡元 / 郡元(南側) apart: 35 once each pair is one stop. ⚠️ Gate 3 at build.
- ⚠️ **Same name, different stations**: tram 郡元 and JR 郡元, tram 谷山 and JR
  谷山 are separate N02 groups. Their English names collide: append the
  operator (trap 9, Mikage (Hankyu) / Mikage (Hanshin)).
- ⚠️ **Labels**: legal lines or routes 1 / 2 (Tokyo's `route`), as Kumamoto's
  and Nagasaki's: choose at build.
- English names: OSM `name:en` (station and `tram_stop` queries) at build.
  **No Overpass query was run for this brief.**

## Scope

**Kagoshima City (one municipality).** JR runs on to 日置市 (鹿児島線), 姶良市
(日豊線) and 指宿市.

## Licences — read 2026-10-02

- **The city's old-law list — PERMITTED WITH CONDITIONS (CC BY 4.0).** The
  page is titled as open data and sends users to the city's terms; the
  「鹿児島市オープンデータ利用規約」 (`https://www.city.kagoshima.lg.jp/ict/documents/riyoukiyaku.pdf`,
  in force 2016-07-01, linked from `https://www.city.kagoshima.lg.jp/ict/opendata.html`)
  license the city's works under CC BY 4.0 and **prescribe the credit for a
  processed work**:
  `この[データベース]は以下の著作物を改変して利用しています。「食品営業許可全施設一覧」、鹿児島市、CCBY4.0（https://creativecommons.org/licenses/by/4.0/deed.ja）`.
  **MUST NOT** present the processed work as the city's own; logos need the
  owner's permission. **Cost**: 5(2) claims from the user's own breach at the
  user's cost, and 5(3) the user reimburses the city's costs of such claims
  (damages included): breach-triggered, the fault-based class accepted for
  all of Japan (2026-09-24). BODIK's copy is CC BY 4.0 too.
- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, re-read 2026-10-02
  (`https://i2fas.mhlw.go.jp/termsofuse.htm`): **MUST DISPLAY**
  `「食品衛生申請等システム」（厚生労働省）（<page URL>）を加工して作成` and who
  processed it; no completeness or accuracy claim; no logo. The minor open point
  (免責 2) ウ) stands.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **N03**: CC BY 4.0, never drawn.

## Privacy

Read only the trade name, `営業の種類`, `業態` and the premises address.
`営業者氏名` is read in memory for the name rule only. **Never select**
`営業所の電話番号`, `営業許可番号`, or MHLW's `法人名` / `法人番号` /
`法人住所` / phones. Run `check_personal_exposure.py` with `japan=True`.

## Region

Japan sub-region (minor tier, above). Project to **UTM 52N (EPSG:32652)**.

## Open items

- ✅ **`mode`: `tram` (owner, 2026-10-02).** JR about 20 stations (Ibusuki-Makurazaki, Kagoshima, Nippō, sharing 鹿児島中央 and 鹿児島) against the tram's 35. The nearest call of the twelve. The owner's rule (2026-10-02): Dublin's precedent, so commuter rail drawn beside a tram does not make a city `metro`, "unless there is substantial JR, JR reads as metro". Staging read substantial as JR being the city's largest rail network by stations inside the city line..
- ✅ **Band B, food only, holds**: 80.5% placeable among fixed premises; the
  personal lists are a stream of openings (re-read 2026-10-02).
- ⚠️ **The two shared-code additions** (`ADDR_COLS` 営業所の所在地, `NAME_COLS`
  営業所の名称、屋号又は商号), then the Minato control and every city screen.
- ⚠️ **The old-law file is renamed each quarter** (`opendetar8_6matsu.csv` is
  2026-06-30's; the October 15 update will replace it). Read the link from the
  page at fetch; a failing `http_ok` below means a new quarter, not a dead
  source.
- ⚠️ **Food retail is partial**: MHLW's permits (菓子, そうざい, 食肉, 魚介類)
  are complete since 2021-06 but only 71% addressed, and its notifications
  (konbini, supermarkets) are opt-in; the page says so, as Fukuoka's.
- ⚠️ **The Economic Census join control** at build: the 2021 census holds
  **2,613** 飲食店 establishments in 46201; about 4,870 food-service pins would
  be **about 1.9 per establishment** (Hiroshima 1.80).
- ⚠️ MHLW's 50 restaurants more than 1 km from their own point; gate 3 against
  the operator; colliding English names; tram labels; OSM `name:en`.

```brief-checks
[
  {
    "id": "kagoshima-mhlw-live",
    "claim": "MHLW's open-data file for Kagoshima City (46201) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=46201_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "kagoshima-mhlw-terms-pdl",
    "claim": "MHLW's system site applies PDL 1.0 (ASCII only: the page's Japanese text is not matchable by this check)",
    "kind": "http_contains",
    "url": "https://i2fas.mhlw.go.jp/termsofuse.htm",
    "present": ["PDL1.0"]
  },
  {
    "id": "kagoshima-oldlaw-live",
    "claim": "The city's old-law food list for 2026-06-30 is keyless and live (renamed each quarter: a failure may mean a new file)",
    "kind": "http_ok",
    "url": "https://www.city.kagoshima.lg.jp/kenkofukushi/hokenjo/seiei-shoku/kenko/ese/sekatsu/shoku/documents/opendetar8_6matsu.csv",
    "min_bytes": 100000
  },
  {
    "id": "kagoshima-oldlaw-page",
    "claim": "The list page links the current quarter's file and MHLW's system",
    "kind": "http_contains",
    "url": "https://www.city.kagoshima.lg.jp/kenkofukushi/hokenjo/seiei-shoku/kenko/ese/sekatsu/shoku/shokuopendata.html",
    "present": ["opendetar8_6matsu.csv", "i2fas.mhlw.go.jp"]
  },
  {
    "id": "kagoshima-terms-linked",
    "claim": "The city's open-data page links the terms of use (CC BY 4.0, read from the PDF)",
    "kind": "http_contains",
    "url": "https://www.city.kagoshima.lg.jp/ict/opendata.html",
    "present": ["riyoukiyaku.pdf"]
  },
  {
    "id": "kagoshima-terms-pdf-live",
    "claim": "The open-data terms PDF answers",
    "kind": "http_ok",
    "url": "https://www.city.kagoshima.lg.jp/ict/documents/riyoukiyaku.pdf",
    "min_bytes": 100000
  },
  {
    "id": "kagoshima-personal-new-only",
    "claim": "The barber and salon page publishes new openings only (monthly files), no full register",
    "kind": "http_contains",
    "url": "https://www.city.kagoshima.lg.jp/kenkofukushi/hokenjo/seiei-shoku/opendate2.html",
    "present": ["r0808biyou.xlsx"],
    "absent": ["cleaning"]
  },
  {
    "id": "kagoshima-isj-live",
    "claim": "MLIT's block-level address file for Kagoshima City (46201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/46201-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "kagoshima-projected-crs",
    "claim": "Kagoshima projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 130.56,
    "expect": "EPSG:32652"
  }
]
```
