# Kurume — build brief

**Step 0 measured 2026-10-02** (Japan wave 2; the scope's figures re-verified
live; downloads are MHLW's file and MLIT's ISJ zips). **Run
`python scripts/brief_check.py kurume` before writing any code.** Then the
`japan-city` skill: Okayama's shape, **MHLW's open data alone, food only**.
Coordinates: the `address-join` skill, measured with
`pipeline/countries/japan_register.py` from a scratch script
(`scripts/screen_japan_join.py` has no Kurume entry; its table is shared
code).

**✅ Decided by the owner, for every Japanese city (the `japan-city` skill's
standing calls; do not re-ask):** (1) **the Shinkansen does not count**
(2026-09-24; 久留米 stays as a JR station); (2) **lines served only by limited
expresses DO count** (2026-09-28); (3) **the city line only**: only stations
inside the city get rings, JR and the private lines are cut at the line, **a
one-station stub stays as cut** (2026-09-27), and an URBAN line cut to a stub
goes back to the owner; (4) **菓子製造業 and そうざい製造業 count, in Retail**,
the factory share measured and kept; (5) **the name rule** where an operator
column exists (MHLW's rows have none: Hiroshima's MHLW bullet for the whole
page, as Okayama, owner 2026-10-02); (6) **no page says "currently
operating"**. Fault-based cost clauses are accepted for all of Japan.

**✅ Minor label tier and the Japan sub-region (owner, 2026-10-02).** Kurume
carries `label_tier: "minor"` and joins the Japan sub-region the 2026-10-01
batch creates.

**✅ `mode`: `metro`** (owner's rule, 2026-10-02). JR is not the largest
network inside the city (9 stations against Nishitetsu's 16), and no subway
or tram is drawn, so the mode follows the backbone: Nishitetsu's 天神大牟田線
and 甘木線 are railways (N02 class 12).

---

## The one-line summary

**Food only, from ONE source: MHLW's 食品衛生申請等システム file for Kurume
(3,861 open restaurant permits, 89% of the 4,343 in force). 670 of the 2,997
"addressed" permits give only 久留米市内 (vehicles and temporary stalls), so
2,327 carry a real address; on fixed premises 2,315 of 2,907 (79.6%) can be
placed.** Block join 87.4% of placeable storefronts, MHLW's own point for the
rest. **No personal-services register** (the city posts only each month's new
barbers and salons). 25 stations: Nishitetsu 16, JR 9. **Band B, food only.**

---

## Business leg — MHLW's open data, alone

| | MHLW open data (40203) |
|---|---|
| **File** | `https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=40203_food_business_all.csv`: **2,476,551 B, 7,491 rows** (許可 4,990, 届出 2,486, 許可(廃業) 14, 届出(廃業) 1). UTF-8 CSV, the national schema. Same bytes as the scope's fetch |
| As of / cadence | Permits to **2026-08-31**; closures dated 2026-08-10 .. 08-28. Monthly (MHLW) |
| Columns | as Okayama's: 営業施設名称、屋号又は商号, 営業の種類, **業態**, **営業施設所在地**, 営業施設方書, **緯度 / 経度**, 法人名, 法人番号, 法人住所, phones, permit dates, 申請区分 |
| Operator column | **None for an individual** (法人名 is a company's): the name rule cannot run (Okayama's precedent) |

**Counts that matter** (open restaurant permits: 許可, no 廃業年月日, 許可満了日
not past):

- **3,861 open 飲食店営業 permits = 89% of e-Stat's FY2024 in force (4,343:
  old law 1,373, revised 2,970).** By first-permit year: 2021 410 · 2022 791
  · 2023 748 · 2024 695 · 2025 781 · 2026 436. The city enters every new
  permit; the gap is old-law permits still in term, which renew into MHLW.
- 🔎 **The scope's 77.6% "with an address" overstates it.** 670 of the 2,997
  non-blank addresses read only `福岡県久留米市内`: 業態 自動車営業 365,
  仮設営業 275, 飲食仮設 20, 仮設 8, blank 2. They are vehicles and stalls
  licensed citywide, and all 1,022 such rows in the file (restaurants and
  notifications) carry ONE shared point. **A real address: 2,327, 60.3% of
  all open restaurant permits.**
- **On fixed premises** (Okayama's measure: every citywide row and every
  vehicle or stall 業態 set aside): **2,315 of 2,907, 79.6%**, above the
  reduced-bucket bar. 業態 is published even where the address is withheld
  (only 5 fixed, unaddressed permits lack it), so the split is measured, not
  guessed. 2,285 distinct (address, trade name) pairs.
- **Through `japan_eigyo`** (all rows, step 2's order): out by 業態 as
  temporary or mobile 714, hostess venues 187, institutional 171, other
  rules; **storefronts Food service 1,904, Retail 1,763** (Retail includes
  MHLW's notifications, a partial opt-in bucket as in Fukuoka and Okayama, and
  247 notification rows addressed `久留米市内`, below).
- **What is missing**: old-law permits still in term (the city's own monthly
  new-permit stream on BODIK, `402036_0001500_00001`, runs 2017-03 to 2021-05
  and stops there, pointing to MHLW; it carries no renewals or closures, so it
  cannot rebuild them), and the ~20% of fixed premises that withhold their
  address.

**Personal services: none usable.** BODIK's 理容所検査確認済施設一覧
(`402036_0001500_00010`) and 美容所検査確認済施設一覧 (`…_00020`) are
**each month's NEW confirmations** (「新たに理容所検査を確認した施設一覧です。」),
114 monthly CSVs from 2017-03 to 2026-08 (CC BY), with no closures: not a
register (official year-end counts 286 barbers, 825 salons). No laundry
dataset; the city's 生活衛生 pages carry guidance only. **A food-only page,
Hiroshima's and Okayama's precedent.**

## Coordinates — a JOIN to MLIT 位置参照情報

One municipality (40203, **no wards**, `"wardless": True`). Block
`https://nlftp.mlit.go.jp/isj/dls/data/24.0a/40203-24.0a.zip` (367,131 B,
57,790 block keys), town-chōme `.../19.0b/40203-19.0b.zip` (229).

| Tier | Storefronts with a real address (3,423) | Food service |
|---|---|---|
| Block | **87.4%** | 90.4% |
| Town-chōme / 大字 centroid | 11.8% | 8.8% |
| Unplaced | 0.8% | 0.8% |
| **Block or MHLW's own point** (`OWN_POINT_FALLBACK`) | **~100%** | |

**Independent check**: MHLW's own coordinates against the block point,
**median 48 m, 93.7% within 250 m** (2,992 rows; 79 over 1 km).

- ⚠️ **Shared code needed: an address that is only `<city>内` is not a
  premises.** `permits_from_rows` flags 一円 and 保健所管 but not
  `久留米市内`, so those rows reach the join (town `内`, unplaced), and
  `OWN_POINT_FALLBACK` would then place 247 Retail notification rows at their
  one shared point: the default-point guard does not refuse it, because the
  rows share one town, not many. Flag them `mobile` (Sasebo's file has one
  `佐世保市内` row too).

## 🚇 Rail — MLIT N02-25 cut at the N03 city line

`data/japan/raw/N02-25_GML.zip` and `N03-20250101_40_GML.zip`, N03 code
40203 (230 km², extent W 130.385, S 33.224, E 130.732, N 33.368; the 2005
mergers brought in 田主丸, 北野, 城島 and 三潴). Use **N02-25**.

| N02 line (operator) | Public name | Inside / N02 total | Stations inside |
|---|---|---|---|
| 天神大牟田線 (西日本鉄道) | Nishitetsu Tenjin Ōmuta Line | **10 / 50** | 宮の陣, 櫛原, 西鉄久留米, 花畑, 聖マリア病院前, 津福, 安武, 大善寺, 三潴, 犬塚 |
| 甘木線 (西日本鉄道) | Nishitetsu Amagi Line | **7 / 12** | 宮の陣, 五郎丸, 学校前, 古賀茶屋, 北野, 大城, 金島 |
| 久大線 (JR九州) | JR Kyūdai Line | 8 / 37 | 久留米, 久留米高校前, 南久留米, 久留米大学前, 御井, 善導寺, 筑後草野, 田主丸 |
| 鹿児島線 (JR九州) | JR Kagoshima Line | 2 / 99 | 久留米, 荒木 |

- **25 stations inside the city** (N02 station groups; Nishitetsu 16, JR 9).
  Widest group 宮の陣 (46 m); no name in two groups. Median gap to the
  nearest station **1,418 m**: standard rings.
- **Stub test passes**: no urban line is cut to a stub (鹿児島線 keeps two).
- **Frequency** (general knowledge, not read from the operators at Step 0):
  Nishitetsu's main line is the city's backbone; the 甘木線 and JR's 久大線
  are suburban to rural (the 久大線 roughly hourly plus the ゆふ limited
  expresses, which count by the standing call). Nothing below an hourly
  service; read the timetables at build.
- ⚠️ **Gate 3** (Nishitetsu's and JR Kyushu's per-line counts) and **OSM
  `name:en`** at build.

## Scope

**Kurume City.** Nishitetsu and JR run on into the neighboring
municipalities (鳥栖, 小郡 and うきは among them); cut at the line, the
stations beyond named by N03 municipality at build.

## Licences — read 2026-10-02

- **MHLW open data — PERMITTED WITH CONDITIONS (PDL 1.0)**, as recorded in
  `docs/data_sources/japan.md` and `okayama.md`. **MUST DISPLAY**:
  `出典：「食品衛生申請等システム」（厚生労働省）（https://i2fas.mhlw.go.jp/）の「食品等営業許可・届出一覧」を加工して作成`,
  who processed it; link the top page only. **MUST NOT**: present it as
  MHLW's own; MHLW's logo; claim completeness or accuracy. 免責 2)ウ the
  minor open point, fine while the site is non-commercial.
- The city's BODIK datasets (CC BY) are not used.
- **MLIT 位置参照情報 and N02**: PDL 1.0. **N03**: CC BY 4.0, ⛔ never drawn.

## Privacy

MHLW's file carries **法人名, 法人番号, 法人住所 and phones**: never selected.
No individual's name is published, so the name rule has nothing to compare
(Okayama's position). Run `check_personal_exposure.py` (`japan=True`).

## Region

East Asia today, the Japan sub-region with the batch. Project to **UTM 52N
(EPSG:32652)**.

## Still open

- No 🚨 owner item: food only from MHLW alone is Okayama's decided shape
  (owner, 2026-10-02), and its whole-page name-rule bullet applies.
- ⚠️ **Shared code**: `<city>内` as not a premises (above). Re-run the Minato
  control.
- ⚠️ **Placement disclosure**: about one fixed restaurant in five withholds
  its address (Hiroshima's wording, "About one restaurant in five…").
- ⚠️ **Economic Census join control**: the 2021 census counts **1,368** 飲食店
  establishments in 40203; 1,875 distinct placed Food-service premises is
  **1.37 per establishment**, below the built cities' 1.56-1.92, as expected
  for a file that holds 89% of permits and withholds a fifth of fixed
  addresses. Report it with that reason.
- ⚠️ Notifications as partial retail (disclosed); gate 3; OSM `name:en`; line
  colours on both basemaps.

```brief-checks
[
  {
    "id": "kurume-mhlw-live",
    "claim": "MHLW's open-data file for Kurume (40203) answers a plain keyless GET",
    "kind": "http_ok",
    "url": "https://i2fas.mhlw.go.jp/faspub/page/opendatadownload.jsp?param=40203_food_business_all.csv",
    "min_bytes": 2000000
  },
  {
    "id": "kurume-own-food-stream-ends",
    "claim": "The city's own new-food-permit stream on BODIK stops at May 2021 and its notes send readers to MHLW from June 2021 (resource names carry the month in full-width brackets; the notes say 令和3年6月分以降)",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/dataset/402036_0001500_00001",
    "present": ["（令和3年5月分）", "令和3年6月分以降"],
    "absent": ["（令和3年6月分）"]
  },
  {
    "id": "kurume-barber-new-only",
    "claim": "The city's barber dataset is a monthly list of NEW confirmations (to August 2026), not a register",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/dataset/402036_0001500_00010",
    "present": ["新たに", "令和8年8月分"]
  },
  {
    "id": "kurume-beauty-new-only",
    "claim": "The city's beauty-salon dataset is a monthly list of NEW confirmations (to August 2026), not a register",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/dataset/402036_0001500_00020",
    "present": ["新たに", "令和8年8月分"]
  },
  {
    "id": "kurume-no-laundry-list",
    "claim": "BODIK org 402036 has no laundry (クリーニング) dataset",
    "kind": "http_contains",
    "url": "https://data.bodik.jp/api/3/action/package_search?fq=organization:402036&q=%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0&rows=0",
    "present": ["\"count\": 0"]
  },
  {
    "id": "kurume-isj-live",
    "claim": "MLIT's block-level address file for Kurume (40203) answers keyless - the join target",
    "kind": "http_ok",
    "url": "https://nlftp.mlit.go.jp/isj/dls/data/24.0a/40203-24.0a.zip",
    "min_bytes": 100000
  },
  {
    "id": "kurume-projected-crs",
    "claim": "Kurume projects to UTM 52N",
    "kind": "utm_zone_from_longitude",
    "lon": 130.51,
    "expect": "EPSG:32652"
  }
]
```
