# Shimonoseki — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live; downloads are MHLW's file and MLIT's ISJ zips). **Run
`python scripts/brief_check.py shimonoseki` before writing any code.** Then
the `japan-city` skill: Okayama's shape, **MHLW's open data alone, food
only**. Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from a scratch script
(`scripts/screen_japan_join.py` has no Shimonoseki entry; its table is shared
code).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; 新下関 stays as a JR station); (2) **lines served only by limited
expresses DO count** (2026-09-28); (3) **the city line only**: only stations
inside the city get rings, JR is cut at the line, **a one-station stub stays
as cut** (2026-09-27), and an URBAN line cut to a stub goes back to the owner;
(4) **菓子製造業 and そうざい製造業 count, in Retail**, the factory share
measured and kept; (5) **the name rule** where an operator column exists
(MHLW's rows have none: Hiroshima's MHLW bullet for the whole page, as
Okayama, owner 2026-10-02); (6) **no page says "currently operating"**.
Fault-based cost clauses are accepted for all of Japan.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).**
Shimonoseki carries `label_tier: "minor"` and joins the Japan sub-region the
2026-10-01 batch creates.

**✅ `mode`: `metro`** (owner's rule, 2026-10-02): every station inside the
city is JR's, so JR is the largest network and reads as metro.

---

## The one-line summary

**Food only, from ONE source: MHLW's 食品衛生申請等システム file for
Shimonoseki (2,632 open restaurant permits, 94% of the 2,802 in force), of
which 98.9% publish an address (98.8% of fixed premises).** Block join 79.8%
today, **88.1% with one new shared rule (大字)**, and 98.6% placed with MHLW's
own point. **No personal-services register.** **21 stations, all JR, spread
over 716 km² (median gap 2.7 km); 7 of them are on the San'in Line beyond
小串, a rural stretch at very low frequency (🚨 below).** **Band B, food
only.**

---

## Business leg — MHLW's open data, alone

| | MHLW open data (35201) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=35201_food_business_all.csv`: **1,872,212 B, 5,039 rows** (許可 3,610, 届出 1,408, 許可(廃業) 13, 届出(廃業) 8). UTF-8 CSV, the national schema. Same bytes as the scope's fetch |
| As of / cadence | Permits to **2026-08-31**; closures dated 2026-08-03 .. 08-31. Monthly (MHLW) |
| Columns | as Okayama's: trade name, 営業の種類, **業態**, **営業施設所在地**, 方書, **緯度 / 経度**, 法人名, 法人番号, 法人住所, phones, permit dates, 申請区分 |
| Operator column | **None for an individual**: the name rule cannot run (Okayama's precedent) |

**Counts that matter** (open restaurant permits):

- **2,632 open 飲食店営業 permits = 94% of e-Stat's FY2024 in force (2,802:
  old law 704, revised 2,098).** By first-permit year: 2021 172 · 2022 527 ·
  2023 557 · 2024 511 · 2025 496 · 2026 369. The city enters every permit;
  the gap is old-law permits still in term, which renew into MHLW.
- **Placement: 2,603 carry an address (98.9%, the scope's figure).** 270 of
  them are licensed citywide (一円, caught by `permits_from_rows`) and 182 are
  vehicles or stalls by 業態. **On fixed premises: 2,325 of 2,354, 98.8%**;
  2,316 distinct (address, trade name). Unlike most MHLW cities, Shimonoseki's
  filers almost all publish their address.
- **Through `japan_eigyo`** (all rows): **storefronts Food service 1,992,
  Retail 1,145** (Retail includes MHLW's notifications, partial and opt-in, as
  in Fukuoka and Okayama); out: manufacturing 655, institutional 208, hostess
  venues by 業態 129, vending 96, accommodation 30.
- **What is missing**: old-law permits still in term (about 6%). The city
  publishes no list of them (`/soshiki/49/3678.html` is guidance for old-law
  holders), and no food list of its own.

**Personal services: none.** The city's 理容所 / 美容所 / クリーニング所 pages
(`/soshiki/49/3634.html`, `3635`, `3636`) carry notification forms only, and
the city has no BODIK catalogue. **A food-only page, Hiroshima's precedent.**

## Coordinates — a JOIN to MLIT 位置参照情報

One municipality (35201, **no wards**, `"wardless": True`; the 2005 merger
brought in 菊川, 豊田, 豊浦 and 豊北, whose addresses are 大字 地番). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/35201-24.0a.zip` (330,271 B,
31,817 block keys), town-chōme `.../19.0b/35201-19.0b.zip` (639).

| Tier | MHLW storefronts, addressed, fixed (3,137): today | With the 大字 rule |
|---|---|---|
| Block | 79.8% | **88.1%** |
| Town-chōme / 大字 centroid | 1.4% | 11.3% |
| Unplaced | **18.8%** | **0.7%** |
| **Block or MHLW's own point** (`OWN_POINT_FALLBACK`) | 98.6% | ~100% |

- ⚠️ **Shared rule needed (大字)**: MHLW writes `豊浦町川棚…`, `豊北町神田…`
  where MLIT keys `豊浦町大字川棚`, `豊北町大字神田` (the merged towns' 大字).
  Dropping 大字 on both sides in `norm_town` (measured in memory, 3,194 rows):
  block 79.9% → 88.1%, unplaced 18.7% → 0.7%. It moved nothing in Takamatsu,
  Kurume or Sasebo. Re-run the Minato control and the built cities' screens
  with it.
- **Independent check**: MHLW's own coordinates against the block point,
  **median 38 m, 98.1% within 250 m** (2,504 rows; 6 over 1 km).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_35_GML.zip`, N03 code
35201 (716 km², extent W 130.775, S 33.911, E 131.173, N 34.375; 角島 is in
it). Use **N02-25**.

| N02 line (operator) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 山陽線 (JR西日本) | JR Sanyō Line | 5 / 131 | 下関, 幡生, 新下関, 長府, 小月 |
| 山陰線 (JR西日本) | JR San'in Line | **17 / 161** | 幡生, 綾羅木, 梶栗郷台地, 安岡, 福江, 吉見, 梅ヶ峠, 黒井村, 川棚温泉, 小串, then **湯玉, 宇賀本郷, 長門二見, 滝部, 特牛, 阿川, 長門粟野** |
| 山陽線 (JR九州) | JR Sanyō Line (下関-門司, the Kanmon Tunnel) | **1 / 2** (下関) | a one-station stub: **stays as cut**. Kitakyushu's brief draws the same N02 line from the other side (門司, 1 of 2) |

- **21 stations inside the city** (N02 station groups; 下関 one group for JR
  West and JR Kyushu, 幡生 for both JR West lines). Median gap to the nearest
  station **2,745 m**, the widest of any Japanese city so far: standard rings,
  and most rings will stand alone.
- **Stub test passes**: no urban line is cut to a stub. The JR Kyushu stub
  adds no station (下関 is JR West's too); draw its short in-city track under
  the same public name as JR West's Sanyō Line, or leave the label to JR
  West's line, and say which at build.
- **Frequency** (general knowledge, not read from JR West at Step 0; the
  operator's station pages are script-driven and did not yield a timetable):
  the Sanyō Line 下関-小月 runs several trains an hour; the San'in Line
  幡生-小串 roughly hourly or better toward 吉見; **beyond 小串 (湯玉 to 長門粟野,
  7 stations) only about 8-10 trains a day each way, with gaps of two hours
  or more.** Read JR West's timetable at build and put the exact figure in
  the drafts file.
- ⚠️ **Gate 3** (JR West's per-line counts) and **OSM `name:en`** at build.

## Scope

**Shimonoseki City.** JR runs on to 長門市 (San'in), 山陽小野田 (Sanyō) and,
under the strait, 北九州市 門司 (JR Kyushu); cut at the line.

## Licences — read 2026-10-02

- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as recorded in
  `docs/data_sources/japan.md` and `okayama.md`. **MUST DISPLAY**:
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; link the top page only. **MUST NOT**: present it as
  MHLW's own; MHLW's logo; claim completeness or accuracy. 免責 2)ウ the
  minor open point.
- No city source is used (the city's site default, 「Copyright © Shimonoseki
  City. All Rights Reserved.」, would not permit one).
- **MLIT 位置参照情報 and N02**: PDL 1.0. **N03**: CC BY 4.0, ⛔ never drawn.

## Privacy

MHLW's file carries **法人名, 法人番号, 法人住所 and phones**: never selected.
No individual's name is published, so the name rule has nothing to compare
(Okayama's position). Run `check_personal_exposure.py` (`japan=True`).

## Region

East Asia today, the Japan sub-region with the batch. Project to **UTM 52N
(EPSG:32652)**.

## Still open

- 🚨 **The San'in Line beyond 小串 (7 of the city's 21 stations, about 8-10
  trains a day).** The standing calls draw JR and set no frequency floor, and
  no built city has left a JR stretch out for frequency (Kitakyushu's
  日田彦山線 and Hakodate's JR are drawn whole to the city line). **Recommend:
  draw it, as the standing calls do; the page says nothing extra.** The
  alternative, leaving it out with a bullet under **The lines**, would be a
  new rule (a frequency floor) for every Japanese city, and would take every
  ring off the former 豊北町 (138 MHLW food storefronts) and northern 豊浦町
  (湯玉, 宇賀本郷).
- ⚠️ **Shared code**: `norm_town` drops 大字 on both sides. Re-run the Minato
  control.
- ⚠️ **Economic Census join control**: the 2021 census counts **1,056** 飲食店
  establishments in 35201; 1,986 distinct placed Food-service premises is
  **1.88 per establishment**, inside the built cities' 1.56-1.92.
- ⚠️ Notifications as partial retail (disclosed); the JR Kyushu stub's label;
  the frequency figure from JR West; gate 3; OSM `name:en`; line colours on
  both basemaps.

```brief-checks
[
  {
    "id": "shimonoseki-mhlw-live",
    "claim": "MHLW's open-data file for Shimonoseki (35201) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=35201_food_business_all.csv",
    "min_bytes": 1500000
  },
  {
    "id": "shimonoseki-barber-forms-only",
    "claim": "The city's barber page carries notification forms only (Word and PDF), no list file",
    "kind": "http_contains",
    "url": "https://www.city.shimonoseki.lg.jp/soshiki/49/3634.html",
    "present": [".pdf"],
    "absent": [".csv", ".xlsx"]
  },
  {
    "id": "shimonoseki-beauty-forms-only",
    "claim": "The city's beauty-salon page carries notification forms only (Word and PDF), no list file",
    "kind": "http_contains",
    "url": "https://www.city.shimonoseki.lg.jp/soshiki/49/3635.html",
    "present": [".pdf"],
    "absent": [".csv", ".xlsx"]
  },
  {
    "id": "shimonoseki-no-bodik",
    "claim": "Shimonoseki has no BODIK catalogue (organisation 352012 holds no dataset)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=organization:352012&rows=0",
    "present": ["\"count\": 0"]
  },
  {
    "id": "shimonoseki-isj-live",
    "claim": "MLIT's block-level address file for Shimonoseki (35201) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/35201-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "shimonoseki-projected-crs",
    "claim": "Shimonoseki projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 130.94,
    "expect": "EPSG:32652"
  }
]
```
