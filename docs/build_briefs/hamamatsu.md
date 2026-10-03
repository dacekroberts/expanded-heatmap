# Hamamatsu — build brief

> ✅ **Owner's calls (owner, 2026-10-02: "approve all recommendations"):** MHLW's 6,033 notifications are **NOT** added as a partial food-shops layer (Hakodate's shape).


**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live; the downloads are the city's open-data files, MHLW's file and MLIT's
ISJ zips, each from its publisher). **Run `python scripts/brief_check.py
hamamatsu` before writing any code.** Then the `japan-city` skill. Proposed
**Band B: personal services only, on Yokohama's and Hakodate's precedent**
("**This map shows personal services only: barbers, beauty salons and
laundries.**"; the page says no food register is published). Coordinates: the
`address-join` skill, measured with `pipeline/countries/japan_register.py`
from a scratch script (`scripts/screen_japan_join.py` has no Hamamatsu entry;
its table is shared code and was not edited).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; 浜松 on the Tōkaidō Shinkansen is dropped, the JR Tōkaidō Line's
浜松 stays); (2) **lines served only by limited expresses DO count**
(2026-09-28); (3) **the city line only**: only stations inside the city get
rings, JR and the private lines are cut at the line, **a one-station stub stays
as cut** (2026-09-27), and an URBAN line cut to a stub goes back to the owner;
(4) **菓子製造業 and そうざい製造業 count, in Retail** (no food bucket here);
(5) **the name rule** (2026-09-27); (6) **no page says "currently
operating"**; fault-based cost clauses accepted (2026-09-24).

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Hamamatsu
joins the 2026-10-01 batch's precedent: `label_tier: "minor"`, in the Japan
sub-region (one region or a split, by `check_macro_labels.py`, PROBLEMS 0 at
375, 768 and 1200). The eight built Japanese cities stay eligible.

**`mode`: `metro`** by the owner's rule of 2026-10-02. No subway, no tram;
JR has 18 station groups inside the city line against Tenhama's 19 and Enshū's
18, so JR is not the largest network. "Otherwise ... by the backbone": the
backbone is the Enshū Railway, an electrified heavy-rail commuter
line, neither tram nor light rail.

---

## The one-line summary

**Four standing registers (barbers 718, beauty salons 2,107, laundry pick-up
counters 239, general laundries 148) published 2026-08-18 under CC BY 2.1 JP:
3,212 premises, 101.5% of MHLW's official count, joined to MLIT's block files
at 94.9% and the rest at the town or 大字 centroid, nothing unplaced.** Each row
also carries the city's own 緯度 / 経度 (median 40 m from the block point).
**No food leg**: the city publishes only NEW food permits, and MHLW's file
holds notifications only. **Rail: 54 station groups inside the city (Enshū 18
of 18, Tenhama 19 of 39, JR Iida 13 of 94, JR Tōkaidō 5 of 89).**

---

## Business leg — the city's 生活衛生課 registers

Hamamatsu's own open-data portal (`/odpf/opendata/v1.html`, a JavaScript page
whose content comes from `https://www.city.hamamatsu.shizuoka.jp/api/odpf/opendata/v1?x=<id>`).
Each dataset offers Excel, CSV and JSON; the CSV is served from the portal's
storage, `https://prd-hmpf-s3-odpf-01.s3.ap-northeast-1.amazonaws.com/opendata/v01/<id>/<id>.csv`
(the portal's own links go through `opendata.hamamatsu.odpf.net/redir/<id>/csv?r=...`).

| Dataset (`x=`) | Title | File bytes | Rows | Edition | Kind |
|---|---|---|---|---|---|
| `riyoujyo` | 理容所台帳 | **94,141** | **718** | 第76版 | barbers |
| `biyoujyo` | 美容所台帳 | **277,265** | **2,107** | 第74版 | beauty salons |
| `cleaning_toritugi` | クリーニング所(取次)台帳 | **36,453** | **239** | 第69版 | laundry pick-up counters |
| `cleaning_ippan` | クリーニング所(一般)台帳 | **21,272** | **148** | 第70版 | general laundries |

- **As of: published 2026-08-18** (each dataset's 更新日 and the files'
  Last-Modified). The files carry no as-of line; the newest 確認通知年月日 is
  2026-06-08 (barbers), 2026-07-28 (beauty), 2026-06-26 (pick-up), 2025-03-31
  (general). The edition numbers (69 to 76) say the registers are reissued
  regularly; the cadence is not stated. Pin `as_of` to the publication date.
- **Encoding cp932**, header on the first line.
- **Columns** (all four the same): 業種 (理容所 / 美容所 / クリーニング所),
  **施設_名称**, **施設_所在地** (from 静岡県, ward included), 施設_方書 (building),
  施設_電話番号 (the premises' phone: never selected), 確認通知年月日,
  確認通知番号, **緯度**, **経度**, NO, **区** (the ward, new names).
- ⚠️ **Against `japan_register`'s tuples (shared code, not edited here):**
  `ADDR_COLS` lacks **施設_所在地** and `NAME_COLS` lacks **施設_名称** (the
  underscore), so `city_rows` reads them but `permits_from_rows` finds no
  address. Add both at build and re-run the Minato control. `TYPE_COLS` covers
  業種. **There is no operator column at all**, so `OPERATOR_COLS` has nothing
  to add and the name rule cannot run (below).
- **Standing registers, not a stream**: 確認通知年月日 runs from 1941 (barbers)
  and 1949 (beauty) to 2026; barbers by decade from the 1960s: 31 · 98 · 153 ·
  164 · 114 · 94 · 51.
- **Not a premises**: none (no 無店舗 or 一円 row).

**The official count settles completeness.** e-Stat 衛生行政報告例 FY2024,
生活衛生 第10表 (`statInfId=000040359178`) and 第11表
(`statInfId=000040359179`), the files Hakodate's brief fetched
(`data/hakodate/raw/estat_eisei_r6_*_by_city.csv`), row 静岡県浜松市, facilities
at 2025-03-31:

| | Official (FY2024 year end) | The city's files (2026-08-18) | Share |
|---|---|---|---|
| 理容所 | 726 | 718 | 98.9% |
| 美容所 | 2,042 | 2,107 | 103.2% |
| クリーニング所 (取次所 241 of it) | 396 | 387 (取次 239, 一般 148) | 97.7% |
| **All** | **3,164** | **3,212** | **101.5%** |

**What is missing: food.**
- The city's food data is **新規食品衛生台帳**, 「新規食品営業許可取得施設一覧」:
  NEW permits only, in two files, `x=syokuhineiseidaityou` (2017-04 to
  2023-12, 10,439 rows, frozen 2024-02-06) and `x=syokuhineiseidaityou202401`
  (2024-01 on, 5,352 rows, 676,996 B, updated 2026-09-17; 4,310 飲食店営業).
  No renewal and no closure is in either, so a premises permitted before
  2017-04 and still trading is absent: Toyohashi's discard reason (a permit
  stream), and no full baseline exists to rebuild from as Kyoto's 2021 list did.
- **MHLW's file** (`…param=22130_food_business_all.csv`, 1,997,856 B, 6,040
  rows) holds **notifications only**: 6,033 届出 (4,350 with an address), no
  permit. The official FY2024 count is 8,388 restaurant permits.

---

## ✅ Coordinates — a JOIN to MLIT 位置参照情報 (3 wards)

**The 2024 ward reorganisation checks out.** Hamamatsu went from 7 wards to 3
on 2024-01-01. MLIT's ISJ files are already keyed by the NEW codes (the old
codes 22131 and 22137 answer 404): block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/{22138,22139,22140}-24.0a.zip`
(998,517 B, 342,175 B, 30,923 B) and town-chōme `.../19.0b/{code}-19.0b.zip`
(10,660 B, 6,497 B, 6,053 B), each file's 市区町村名 浜松市中央区 / 浜名区 / 天竜区.
`load_city_isj` keys them as 中央区, 浜名区, 天竜区: 255,719 block keys, 549
town-chōme. The registers write the same new names: the ward parsed from every
one of the 3,212 addresses equals the file's own 区 column. N03 (2025-01-01)
carries the same three codes. `japan.CITIES`:
`"wards": ["22138", "22139", "22140"]`, not wardless.

| Tier | Barbers (718) | Beauty (2,107) | Pick-up (239) | General (148) | All (3,212) |
|---|---|---|---|---|---|
| Block | 92.6% | 95.5% | 96.2% | 94.6% | **94.9%** |
| Town-chōme / 大字 centroid | 7.4% | 4.5% | 3.8% | 5.4% | 5.1% |
| Unplaced | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |

**Independent check: the city's own 緯度 / 経度** (every row but one; 3,066
distinct points, none repeated more than 6 times, so no default point). At the
**block** tier it sits a **median 40 m** from MLIT's point (p90 102 m, 96.0%
within 250 m; 3,046 rows). At the **chōme** tier the centroid is a **median
741 m** away (165 rows, 22.4% within 250 m, 68 over 1 km): 164 of the 165 are
大字 with 地番 addresses (天竜区 71, 中央区 49, 浜名区 45).

⚠️ **Recommended at build (measured grounds)**: the city's own point for the
165 chōme-tier rows, Fukuoka's `OWN_POINT_FALLBACK` (which takes MHLW's point
for chōme-tier rows too). The page's standing bullet then needs no centroid
caveat for these rows.

---

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

Read from `data/japan/raw/N02-25_GML.zip` and `N03-20250101_22_GML.zip` (the
shared cache) with `stub_test()`'s method and wards 22138-22140 (a merged city
reaching from the coast into the mountains of 天竜区). N03 extent W 137.4868, S 34.6463, E 138.0587, N 35.3044.
**55 station records, 54 N02_005g groups.** Shinkansen: 浜松, dropped.

| N02 line (operator) | Public name | In the city / total | Reading |
|---|---|---|---|
| 鉄道線 (遠州鉄道) | Enshū Railway Line (新浜松–西鹿島) | **18 / 18** | wholly inside; operator's station index lists **18** (gate 3 exact) |
| 天竜浜名湖線 (天竜浜名湖鉄道) | Tenryū Hamanako Line | **19 / 39** | cut at the line (on to 湖西 and 掛川); operator's index lists **39** (gate 3 exact) |
| 飯田線 (東海旅客鉄道) | JR Iida Line | **13 / 94** | 中部天竜 to 大嵐, the mountain stretch in 天竜区: drawn as cut by the standing call, as Toyama's 立山線 fragment |
| 東海道線 (東海旅客鉄道) | JR Tōkaidō Line | **5 / 89** | 浜松, 高塚, 舞阪, 弁天島, 天竜川; cut at the line |

- **The stub test passes**: no line is cut to a stub; the one urban line
  (Enshū) is wholly inside.
- **Close pairs** (separate groups, kept apart): 浜松 (JR) and 新浜松 (Enshū)
  244 m; 遠州病院 and 第一通り 340 m. 西鹿島 is one group for Enshū and Tenhama.
- **Median nearest-station gap 1,158 m**: standard rings by the spacing rule
  (halved rings were for Hiroshima's 357 m).
- ⚠️ **32 of the 54 groups are on rural lines** (Tenhama 19, Iida 13), and the
  Iida Line's are in the mountains; their rings will be near-empty. The
  standing call draws them; the page's **The lines** bullet names the cut.
- ⚠️ **Gate 3 for JR** (Tōkaidō and Iida counts) at build from JR Central.
- ⚠️ **OSM `name:en`** for 54 groups at build (one station query, no tram
  stops; not queried for this brief). The N03 box is wide: check the opening
  view with `map-view`.

## Scope

**Hamamatsu City (3 wards).** JR Tōkaidō runs on to 湖西 and 磐田, the Iida
Line into Aichi and Nagano, Tenhama to 湖西 and 掛川; cut at the line.

## Licences — read 2026-10-02 (`licence-read`)

- **The city's registers — PERMITTED WITH CONDITIONS (CC BY 2.1 JP).** None of
  the four dataset records carries a licence field; the portal's top
  (`api/odpf/opendata/v1?m=top`) and the 「くらし」 category listing state
  「以下のデータはクリエイティブ・コモンズ表示2.1日本ライセンスの下、オープンデータとして提供しています。」
  and incorporate the terms 浜松市オープンデータ利用規約
  (`https://www.city.hamamatsu.shizuoka.jp/koho2/opendata/kiyaku.html`, updated
  2025-04-01): 「以下の条件の下、自由に利用できます。」, 第1条 pointing to the CC BY
  2.1 JP legal code. The site policy (`/policy/index.html`, no reuse without
  permission) covers web pages and gives way: the top calls the terms
  「本ホームページサイトポリシーとは別に定める利用規約」.
  - **MUST DISPLAY** (the terms' form for a modified work):
    `この地図は以下の著作物を改変して利用しています。理容所台帳、美容所台帳、クリーニング所(取次)台帳、クリーニング所(一般)台帳、浜松市、クリエイティブ・コモンズ・ライセンス 表示2.1（http://creativecommons.org/licenses/by/2.1/jp/）`;
    the URL may be a link on the licence words.
  - **MUST NOT**: present the map as the city's own (CC 2.1 JP); keep the credit
    off if the city asks (CC 4(b)); clear third-party rights (第2条).
  - **Cost**: none on the user (第3条 disclaims; 第5条 Japanese law, Shizuoka
    District Court, Hamamatsu Branch). Optional, not required: 「可能ならば…ご一報を」
    (phone, fax or post only).
- **MLIT 位置参照情報 and N02**: PDL 1.0, the shared credits. **MLIT N03**: CC
  BY 4.0, picks stations, ⛔ never drawn.
- **e-Stat** (政府統計の総合窓口): a measurement source, not drawn; credit in the
  build's provenance notes.

## Privacy

The registers name no operator (no operator column) and no operator address;
施設_電話番号 is the premises' phone and is never selected. Select 業種,
施設_名称, 施設_所在地, 施設_方書, 緯度, 経度, 区. Run `check_personal_exposure.py`
with `japan=True`.

## Region

The Japan sub-region (minor tier, above); until it lands, `"region": "East
Asia"`. `"country": "Japan"`. Project to **UTM 53N (EPSG:32653)**.

## Open items

- ✅ **MHLW's 6,033 notifications as a partial Food-shops layer: recommend
  LEAVE OUT.** Matsuyama, Fukuoka and Okayama show notifications as partial
  retail BESIDE a permit source. Here they would be the only food data: 4,350
  addressed rows of milk sellers, cup vending machines, packaged meat and fish,
  konbini and supermarkets, with no bakery, deli, butcher or restaurant (those
  hold permits). Hakodate's precedent is a personal-services page with no
  food leg; this keeps that shape. The tradeoff: a Food-shops layer of about
  3,400 notified shops is lost.
- ✅ **No name rule on any row: the precedent extends** (owner, 2026-10-02:
  Okayama, Nagasaki's MHLW rows). The registers carry no operator column, so
  the page takes Hiroshima's MHLW-style bullet ("the list does not say who
  the operator is, so this cannot be checked").
- ⚠️ **Shared code**: `ADDR_COLS` + 施設_所在地, `NAME_COLS` + 施設_名称; the
  three new ward codes in `japan.CITIES`; `OWN_POINT_FALLBACK` for the 165
  chōme-tier rows. Each re-runs the Minato control.
- ⚠️ **No Economic Census food control applies** (no food leg); the e-Stat
  table above and the city's own points are the checks.
- ⚠️ Rural rings (above), JR gate 3, OSM names, line colours on both basemaps,
  the opening view.

```brief-checks
[
  {
    "id": "hamamatsu-barber-live",
    "claim": "Hamamatsu's barber register (理容所台帳, published 2026-08-18) is keyless and live",
    "kind": "http_ok",
    "url": "https://prd-hmpf-s3-odpf-01.s3.ap-northeast-1.amazonaws.com/opendata/v01/riyoujyo/riyoujyo.csv",
    "min_bytes": 60000
  },
  {
    "id": "hamamatsu-beauty-live",
    "claim": "Hamamatsu's beauty-salon register (美容所台帳) is keyless and live",
    "kind": "http_ok",
    "url": "https://prd-hmpf-s3-odpf-01.s3.ap-northeast-1.amazonaws.com/opendata/v01/biyoujyo/biyoujyo.csv",
    "min_bytes": 200000
  },
  {
    "id": "hamamatsu-laundry-toritsugi-live",
    "claim": "Hamamatsu's laundry pick-up register (クリーニング所(取次)台帳) is keyless and live",
    "kind": "http_ok",
    "url": "https://prd-hmpf-s3-odpf-01.s3.ap-northeast-1.amazonaws.com/opendata/v01/cleaning_toritugi/cleaning_toritugi.csv",
    "min_bytes": 25000
  },
  {
    "id": "hamamatsu-laundry-ippan-live",
    "claim": "Hamamatsu's general-laundry register (クリーニング所(一般)台帳) is keyless and live",
    "kind": "http_ok",
    "url": "https://prd-hmpf-s3-odpf-01.s3.ap-northeast-1.amazonaws.com/opendata/v01/cleaning_ippan/cleaning_ippan.csv",
    "min_bytes": 15000
  },
  {
    "id": "hamamatsu-barber-dataset-record",
    "claim": "The portal's dataset record for the barber register still serves riyoujyo.csv",
    "kind": "http_contains",
    "url": "https://www.city.hamamatsu.shizuoka.jp/api/odpf/opendata/v1?x=riyoujyo",
    "present": ["riyoujyo.csv"]
  },
  {
    "id": "hamamatsu-portal-licence",
    "claim": "The portal's top states CC BY 2.1 JP (slashes JSON-escaped) and incorporates the terms page kiyaku.html",
    "kind": "http_contains",
    "url": "https://www.city.hamamatsu.shizuoka.jp/api/odpf/opendata/v1?m=top",
    "present": ["licenses\\/by\\/2.1\\/jp", "kiyaku.html"]
  },
  {
    "id": "hamamatsu-terms-cc-by-21",
    "claim": "浜松市オープンデータ利用規約 points to the CC BY 2.1 JP legal code",
    "kind": "http_contains",
    "url": "https://www.city.hamamatsu.shizuoka.jp/koho2/opendata/kiyaku.html",
    "present": ["licenses/by/2.1/jp/legalcode"]
  },
  {
    "id": "hamamatsu-food-new-permits-only",
    "claim": "Hamamatsu's food data is the new-permit ledger from 2024-01 (a stream, not a register) - the reason there is no food leg",
    "kind": "http_contains",
    "url": "https://www.city.hamamatsu.shizuoka.jp/api/odpf/opendata/v1?x=syokuhineiseidaityou202401",
    "present": ["syokuhineiseidaityou202401.csv"]
  },
  {
    "id": "hamamatsu-mhlw-live",
    "claim": "MHLW's open-data file for Hamamatsu (22130) answers keyless - notifications only, the food control",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=22130_food_business_all.csv",
    "min_bytes": 1000000
  },
  {
    "id": "hamamatsu-isj-chuo-live",
    "claim": "MLIT's block file for the NEW 中央区 (22138, since 2024-01-01) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/22138-24.0a.zip",
    "min_bytes": 500000
  },
  {
    "id": "hamamatsu-isj-hamana-live",
    "claim": "MLIT's block file for the NEW 浜名区 (22139) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/22139-24.0a.zip",
    "min_bytes": 200000
  },
  {
    "id": "hamamatsu-isj-tenryu-live",
    "claim": "MLIT's block file for 天竜区 under its NEW code (22140) answers keyless",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/22140-24.0a.zip",
    "min_bytes": 15000
  },
  {
    "id": "hamamatsu-isj-old-code-gone",
    "claim": "The pre-2024 ward code 22131 (old 中区) is gone from MLIT's ISJ - the build must use 22138-22140",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/22131-24.0a.zip",
    "expect_status": 404
  },
  {
    "id": "hamamatsu-estat-riyo-biyo",
    "claim": "e-Stat's 衛生行政報告例 FY2024 第10表 (barbers and beauty salons by designated city) answers keyless - the completeness control",
    "kind": "http_ok",
    "url": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359178&fileKind=1",
    "min_bytes": 5000
  },
  {
    "id": "hamamatsu-estat-cleaning",
    "claim": "e-Stat's 衛生行政報告例 FY2024 第11表 (laundries by designated city) answers keyless",
    "kind": "http_ok",
    "url": "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040359179&fileKind=1",
    "min_bytes": 5000
  },
  {
    "id": "hamamatsu-enshu-18-stations",
    "claim": "The Enshū Railway's station index lists 18 stations, 新浜松 to 西鹿島 (gate 3)",
    "kind": "http_contains",
    "url": "https://www.entetsu.co.jp/tetsudou/",
    "present": ["station/shinhamamatsu.html", "station/nishikajima.html", "station/daiichi-dori.html"]
  },
  {
    "id": "hamamatsu-tenhama-39-stations",
    "claim": "Tenryū Hamanako Railroad's site links its 39 station pages, 掛川 to 新所原 (gate 3)",
    "kind": "http_contains",
    "url": "https://www.tenhama.co.jp/",
    "present": ["about/station/kakegawa/", "about/station/shinjyohara/", "about/station/nishikajima/"]
  },
  {
    "id": "hamamatsu-projected-crs",
    "claim": "Hamamatsu projects to UTM 53N",
    "kind": "utm_zone_from_longitude",
    "lon": 137.73,
    "expect": "EPSG:32653"
  }
]
```
