# Sakai — build brief

**Step 0 measured 2026-10-02** (the 2026-10-01 screen's figures re-verified
live; the downloads are the master list's named sources, MHLW's file and MLIT's
ISJ zips). **Run `python scripts/brief_check.py sakai` before writing any
code.** Then the `japan-city` skill. Band B (owner, 2026-10-01): **food only,
Hiroshima's page** ("**This map shows food businesses only.**"). Coordinates:
the `address-join` skill, measured with `pipeline/countries/japan_register.py`
from a scratch script (`scripts/screen_japan_join.py` has no Sakai entry; its
table is shared code).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; none reaches Sakai); (2) **lines served only by limited expresses
DO count** (2026-09-28); (3) **the city line only**: only stations inside the
city get rings, JR and the private lines are cut at the line, **a one-station
stub stays as cut** (2026-09-27), and an URBAN line cut to a stub goes back to
the owner; (4) **菓子製造業 and そうざい製造業 count, in Retail**, factory share
measured and kept; (5) **the name rule**: where the trade name IS the
operator's own name, the pin shows its permit type (2026-09-27); (6) **no page
says "currently operating"**: the lists keep closed premises; fault-based cost
clauses are accepted (2026-09-24).

**✅ Minor label tier (owner, 2026-10-02).** Sakai carries
`label_tier: "minor"`: dot and tooltip in every view, pill only in its own
region. Per the `japan-city` skill: a Japan sub-region (one or split, by
`check_macro_labels.py`, PROBLEMS 0 at 375, 768 and 1200), every Japanese city
moved into it, `REGION_LABELS_ALSO["East Asia"]` gaining it. **The eight built
Japanese cities stay eligible.** ⚠️ **Sakai's dot sits beside built Osaka's**
(Sakai's city hall is about 10 km south of Namba): measure both labels in the macro
views; Osaka keeps its pill.

---

## The one-line summary

**One city-wide food-permit CSV (10,123 permits at 2026-04-01; CC BY 4.0),
with monthly new and closure files that bring it to 2026-08-31 (10,470).
8,285 restaurant permits, 101% of the official in-force count (8,229).** The
block join reaches **95.8%** only with one new normalisation rule (Sakai
writes `翁橋町1丁1‐1`; MLIT writes `翁橋町一丁`): without it, 33.7%.
Personal services are PDFs outside the catalogue (the city's permission), so
the page is food only. **42 stations inside the city.**

---

## Business leg — the city's 食品営業許可施設一覧

| | Standing list | Monthly new or renewed | Monthly closures |
|---|---|---|---|
| **File** | `https://www.city.sakai.lg.jp/kenko/shokuhineisei/anzenjoho/kyokashisetsuichiran/R8kyokaichiran.files/R80401.csv`; the same bytes on BODIK as `…/resource/1714357c-0ded-41aa-bdc4-2f3b527067c7/download/r8.csv` (dataset `271403__sakai_food_business_all_r8`) | `R0804.csv` … `R0808.csv` (same folder) | `R0804haigyou.csv` … `R0808haigyou.csv` (same folder) |
| Bytes | **2,564,651** (city and BODIK identical) | 48,769 / 38,777 / 33,630 / 35,996 / 35,333 | 26,246 / 17,709 / 22,200 / 18,270 / 11,188 |
| Rows | **10,123** (申請区分 新規 9,266 · 更新 857) | **777** (Apr-Aug) | **434** (Apr-Aug; 300 marked 期限切れ廃業, expired) |
| As of | **2026-04-01** (「令和8年4月1日現在で許可を受けている施設」) | each month to 2026-08 | each month to 2026-08 |
| Cadence | yearly (R6, R7, R8 snapshots on BODIK) | monthly, about the 25th of the next month; page updated 2026-09-24 | monthly, as new |
| Encoding | UTF-8 with BOM | UTF-8 with BOM | **cp932** |

**Columns** (standing list and new): 許可番号, **営業所の名称**, **営業所所在地**,
営業所方書, 営業所電話番号, 許可年月日, 許可開始日, **許可満了日**, 営業者名, 代表者名,
**営業者住所**, **営業者方書**, 申請区分, **営業の種類**, **業態**. Closures: 許可番号 …
許可満了日, 営業者名, **廃業届出日**, 営業の種類, 業態. Dates are 和暦 strings
(`wareki_date()` reads them).

**Against `japan_register`'s column tuples (shared code, not edited here):**
- `OPERATOR_COLS` covers **営業者名** and **代表者名**. Name-rule hits in memory:
  5 in the rebuilt register.
- `NAME_COLS` does NOT cover **営業所の名称**: without it step 2 reads no trade
  name for any row. Add it.
- ⛔ **営業者住所 / 営業者方書 are an operator's own address** (filled on 4,854
  rebuilt rows): never select them, and never 営業所電話番号.

**Counts that matter.**

| | Standing list (2026-04-01) | Rebuilt (2026-08-31) |
|---|---|---|
| Restaurants (飲食店営業, any form) | **8,285** (fixed type 7,373 + 喫茶店営業 24; 露店 479; 自動車 409) | |
| After `japan_eigyo`, fixed premises | Food service **5,872**, Retail **1,887** | Food service **6,109**, Retail **1,948** |
| 菓子 / そうざい / 食肉販売 / 魚介類販売 | 825 / 156 / 299 / 182 | |

- **Official count**: e-Stat 衛生行政報告例 FY2024, 飲食店営業 in force **8,229**
  (`japan_official.estat()`): the list holds **101%**. Complete, unlike
  Hiroshima's counter-only list.
- **The rebuild** (Kyoto's `source_rows` shape): 10,123 + 777 new − 430
  matched closures (of 434) = **10,470**. No new row reuses a standing
  permit number, so a renewal arrives under a new number: one pin per
  premises (trap 7) de-duplicates it, and **383 rebuilt rows past their
  許可満了日 with no closure row** are dropped by date against the pinned
  `as_of` (2026-08-31), never today.
- **Not premises**: 894 rows at 市内一円 (stalls and vehicles), plus 業態 forms
  `FORM_RULES` already reads (露店 425, キッチンカー 336, 集団給食 371).
- **MHLW's file (27140)** carries only Sakai's online filings: **252** open
  restaurant permits and 4,267 notifications, 1,586,897 B, 4,591 rows, as of
  2026-08 end. ⚠️ Its notifications as a partial food-retail bucket follow
  Fukuoka's and Hiroshima's precedent (1,273 fixed premises with an address,
  1,098 of them Retail); measure the overlap with the city's list at build.

**What is missing: personal services.** The city publishes 理容所 / 美容所 /
クリーニング所 as PDFs only (`/kenko/kankyoeisei/taisaku/sisetuitiran.html`:
`R80331riyousho.pdf` 6,149 KB, `R80331biyousho.pdf` 17,262 KB,
`R80331kuri-ninngusho.pdf` 5,939 KB, as of 2026-03-31, with monthly new and
closure PDFs). Not in the catalogue (BODIK org 271403's 56 datasets hold only
the three food snapshots), and the page carries no open-data notice, so the
site default applies: the city's permission. Hence food only.

---

## Coordinates — a JOIN to MLIT 位置参照情報, with one new rule

MLIT files for the **7 wards** (27141 堺, 27142 中, 27143 東, 27144 西, 27145 南,
27146 北, 27147 美原): block `https://nlftp.mlit.go.jp/isj/dls/data/24.0a/<code>-24.0a.zip`,
town-chōme `.../19.0b/<code>-19.0b.zip`. 62,884 block keys, 951 town-chōme.

**⚠️ Sakai writes the chōme as `N丁` with no 目** (`翁橋町1丁1‐1`, 5,010 of the
misses), and MLIT names those towns `翁橋町一丁`. The shared `norm_town` reads
only `丁目` and `条`, so the 丁 number was taken as the block. The candidate
rule, `N丁` not followed by 目 read as `N丁目` on BOTH sides, was tried by
patching `norm_town` in a scratch process only:

| Tier (fixed premises in a bucket) | Shared code as it stands | With the 丁 rule: standing list (7,759) | With the rule: rebuilt (8,057) | With the rule: MHLW addressed (1,273) |
|---|---|---|---|---|
| Block | 33.7% | **95.8%** | **95.8%** (Food service 96.3%) | 90.7% |
| Town-chōme / 大字 centroid | 4.3% | 4.2% | 4.2% | 8.5% |
| Unplaced | **62.0%** | 0.0% | 0.0% | 0.9% |

- What stays at the chōme tier: 大字 addresses with 番地 (美原区 黒山 87, 東区
  北野田 26) and a few blocks missing from the file.
- **Independent check**: MHLW's own 緯度 / 経度 against the block point, 1,150
  block hits: **median 50 m, 95.0% within 250 m**.
- ⚠️ **The rule is a shared-code change** in `japan_register.norm_town` (and the
  address side in `permits_from_rows`), named for Sakai: re-run the Minato
  control (block 98.0 / chōme 0.2 / none 1.8) and every city screen, old
  against new, and record the diff in `DECISIONS.md`.

---

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_27_GML.zip` (the
shared cache), with `stub_test()`'s method and the 7 wards above (150 km²).
**Use N02-25** (`"n02": "25"`): N02-24 still files the Semboku line under
泉北高速鉄道, merged into Nankai on 2025-04-01. No Shinkansen.

| N02 line (operator) | Public name | In the city / total | Note |
|---|---|---|---|
| 阪堺線 (阪堺電気軌道) | Hankai Line (tram) | **15 / 31** stops | Operator lists 31 (N02 32 records: 住吉 twice). Osaka's map draws the other 16; half a line, not a stub (Osaka's sheet) |
| 1号線(御堂筋線) (Osaka Metro) | Midōsuji Line | **3 / 20** (北花田, 新金岡, 中百舌鳥) | ✅ an urban line cut to a stub: **drawn as cut** (owner, 2026-10-02). The master list says 2; N02 says 3 |
| 泉北線 (南海電気鉄道) | Nankai Semboku Line | 5 / 6 | 和泉中央 is in Izumi |
| 高野線 (南海電気鉄道) | Nankai Kōya Line | 9 / 43 | cut at the line |
| 南海本線 (南海電気鉄道) | Nankai Main Line | 6 / 44 | cut at the line |
| 阪和線 (JR西日本) | JR Hanwa Line | 7 stations (8 records: 鳳 twice) / 37 | ⚠️ the Hagoromo branch (鳳–東羽衣, 東羽衣 in Takaishi) hides inside 阪和線 (trap 3): `BRANCHES`; inside the city it is 鳳 only, a one-station stub that **stays as cut** |

- **42 stations inside the city** (N02 station groups). Median gap to the
  nearest station **611 m**: standard rings on the spacing rule (just above its
  ~550 m line; step 1 measures it).
- **Gate 3**: Hankai 31 stops (operator's 停留場一覧) = N02's 31 names; the
  Midōsuji's 20 (M11-M30) = N02 20. Nankai and JR counts at build.
- ⚠️ **OSM `name:en`** for every in-city station and tram stop is a build-time
  read (one Overpass query; not run for this brief). The tram stops need
  `osm_tram_stop_query` (Osaka's 22 Hankai stops).

## Scope

**Sakai City (7 wards).** The Hankai tram and the Midōsuji continue into
Osaka, the Nankai lines and JR to Takaishi, Izumi and Ōsakasayama; cut at the
line.

## Licences — read 2026-10-02

- **The city's food list — PERMITTED WITH CONDITIONS (CC BY 4.0).** BODIK
  records `license_id: cc-by-40-intl`. The list page ends with
  「オープンデータの利用にあたって … 本利用規約に従っていただく」 and links the 堺市オープンデータ
  利用規約 (`https://www.city.sakai.lg.jp/shisei/gyosei/open_data/index.files/riyoukiyaku210121.pdf`),
  whose 3-2 licenses the data 「クリエイティブ・コモンズ・ライセンス…表示 4.0 国際」. The
  site default 「無断で複製・転用することはできません」 yields to it (the screen).
  - **MUST DISPLAY** (3-3, the modified-use form, filled in):
    `この地図は以下の著作物を改変して利用しています。堺市 食品営業許可施設一覧（令和8年4月1日現在）、堺市、クリエイティブ・コモンズ・ライセンス 表示 4.0 国際（https://creativecommons.org/licenses/by/4.0/deed.ja）`,
    and the monthly files' titles if used.
  - **Cost**: 5, claims from our own breach at our own cost; **8, 本市への弁償**:
    costs the city incurs from our breach are ours to repay. Both fault-based,
    accepted for all of Japan (2026-09-24). Use is deemed acceptance (1).
  - ✅ **The monthly new and closure CSVs are on the city's page only, not on
    BODIK.** The page's own open-data paragraph and link cover them (owner,
    2026-10-02, on the reading accepted for Hiroshima on 2026-09-24).
- **MHLW open data** (only if its notifications are used): PDL 1.0, as
  `fukuoka.md`.
- **MLIT 位置参照情報 and N02**: PDL 1.0 (the skill's notice lines). **N03**: CC
  BY 4.0, ⛔ never drawn.

## Privacy

The list carries 営業者名, 代表者名, **営業者住所 and 営業者方書 (an operator's
own address)** and 営業所電話番号. Select only 営業所の名称, 営業所所在地 (+ 方書),
営業の種類, 業態, 許可番号 and the dates; read 営業者名 / 代表者名 in memory for the
name rule only. Run `check_personal_exposure.py` (`japan=True`).

## Region

East Asia today, moving to the Japan sub-region with the batch. Project to
**UTM 53N (EPSG:32653)**.

## Still open

- ✅ **`mode`: `metro` (owner, 2026-10-02).** the Midōsuji subway is drawn (3 stations); JR Hanwa has 7. The owner's rule (2026-10-02): Dublin's precedent, so commuter rail drawn beside a tram does not make a city `metro`, "unless there is substantial JR, JR reads as metro". Staging read substantial as JR being the city's largest rail network by stations inside the city line..
- ✅ **The Midōsuji is drawn, cut at the city line: 3 stations** (北花田,
  新金岡, 中百舌鳥) (owner, 2026-10-02). All three are Sakai's own, with the
  city's permits around them; Osaka's page draws the other 16, as the Hankai
  is split.
- ✅ **The monthly new and closure files are covered by the list page's own
  open-data notice** (owner, 2026-10-02; Hiroshima's precedent), so the map
  is the rebuilt register as of 2026-08-31.
- ⚠️ **Shared code, made at build**: the 1丁 rule (`norm_town` and the address
  side in `permits_from_rows`), proven on Minato's control (block 98.0 /
  chōme 0.2 / none 1.8) and every city screen, old against new;
  `NAME_COLS` + 営業所の名称.
- ⚠️ The Hagoromo branch split from 阪和線; N02-25.
- ⚠️ **Economic Census join control at build** (`scripts/japan_census_control.py`):
  the 2021 census counts **2,626** 飲食店 establishments (堺 915, 中 334, 東 204,
  西 399, 南 243, 北 462, 美原 69).
- ⚠️ OSM `name:en`; line colours on both basemaps; Sakai's pill beside
  Osaka's in the macro views.
- **Master list corrections** (for the cleanup session): the Midōsuji has 3
  stations in Sakai, not 2; the Hankai keeps 15 of 31 stops, not 16.

```brief-checks
[
  {
    "id": "sakai-food-list-live",
    "claim": "Sakai's standing food-permit CSV (2026-04-01) is keyless and live on the city's site",
    "kind": "http_ok",
    "url": "https://www.city.sakai.lg.jp/kenko/shokuhineisei/anzenjoho/kyokashisetsuichiran/R8kyokaichiran.files/R80401.csv",
    "min_bytes": 2000000
  },
  {
    "id": "sakai-food-list-rows",
    "claim": "The BODIK copy of the standing list holds 10,123 rows",
    "kind": "ckan_rows",
    "domain": "data.bodik.jp",
    "resource_id": "1714357c-0ded-41aa-bdc4-2f3b527067c7",
    "expect": 10123
  },
  {
    "id": "sakai-food-list-licence",
    "claim": "BODIK records the standing list under CC BY 4.0",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_show?id=271403__sakai_food_business_all_r8",
    "present": ["cc-by-40-intl"]
  },
  {
    "id": "sakai-monthly-closures-live",
    "claim": "The August 2026 closures CSV is live beside the standing list",
    "kind": "http_ok",
    "url": "https://www.city.sakai.lg.jp/kenko/shokuhineisei/anzenjoho/kyokashisetsuichiran/R8kyokaichiran.files/R0808haigyou.csv",
    "min_bytes": 5000
  },
  {
    "id": "sakai-list-page",
    "claim": "The list page still offers the 2026-04-01 list, monthly closures and the open-data terms link",
    "kind": "http_contains",
    "url": "https://www.city.sakai.lg.jp/kenko/shokuhineisei/anzenjoho/kyokashisetsuichiran/R8kyokaichiran.html",
    "present": ["R80401.csv", "R0808haigyou.csv", "/shisei/gyosei/open_data/index.html"]
  },
  {
    "id": "sakai-personal-pdf-only",
    "claim": "Sakai's barber, beauty and laundry lists are PDFs only",
    "kind": "http_contains",
    "url": "https://www.city.sakai.lg.jp/kenko/kankyoeisei/taisaku/sisetuitiran.html",
    "present": ["R80331riyousho.pdf", "R80331biyousho.pdf", "R80331kuri-ninngusho.pdf"],
    "absent": [".csv", ".xlsx"]
  },
  {
    "id": "sakai-terms-pdf-live",
    "claim": "The 堺市オープンデータ利用規約 PDF (CC BY 4.0 in 3-2) is live",
    "kind": "http_ok",
    "url": "https://www.city.sakai.lg.jp/shisei/gyosei/open_data/index.files/riyoukiyaku210121.pdf",
    "min_bytes": 100000
  },
  {
    "id": "sakai-isj-sakaiku-live",
    "claim": "MLIT's block-level address file for Sakai ward (27141) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/27141-24.0a.zip",
    "min_bytes": 10000
  },
  {
    "id": "sakai-projected-crs",
    "claim": "Sakai projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 135.48,
    "expect": "EPSG:32653"
  }
]
```
