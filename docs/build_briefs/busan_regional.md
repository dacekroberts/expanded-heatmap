# Busan (Regional) - build brief

**A regional extension of a built page, marked by the owner on 2026-10-04**
(`docs/city_master_list.md`, "Add-ons to built cities", "Potential Korean
regional expansions": "Busan (Regional) + Yangsan (Busan Line 2, 5 stations;
Yangsan is Band C until chosen). Gimhae is its own page (owner,
2026-10-03)."). Yangsan's Band C row (line 139) reads "A page of its own, or
Busan (Regional)". Released for briefing on 2026-10-06; **the build stays
paused**. Brief written 2026-10-06 by staging from cached files only (nothing
downloaded, no Overpass query). Run `python scripts/brief_check.py
busan_regional` before writing any code.

Read `regional-extension`, `multi-source-city` (Los Angeles + Long Beach's
shape), `korea-city` and `cjk-text`; then Busan's and Gimhae's briefs
(`docs/build_briefs/busan.md`, `gimhae.md`) and `seoul_regional.md`, which
sets out the same two-register join at more length.

---

## The one-line summary

**Busan keeps its LOCALDATA permit API; Yangsan joins on SEMAS's national
storefront file, code 48330: 11,202 storefronts and Line 2's 5 stations,
26.4% of them in a ring. The registers count Retail differently (SEMAS lists
about 1.9 times the retail Busan's permits do), and Busan would take on
notice 68 and the Visuals card hold. The owner's first call is the shape:
this page, Yangsan's own, or neither.**

---

## Step 0 - is it an extension? (`regional-extension` Step 0)

1. **Lines already drawn: yes.** Line 2 runs 5 stations into Yangsan, drawn
   to its end on Busan's map, the 5 listed in Busan's committed
   `outputs/busan/excluded_stations.csv`.
2. **No bucket at a few stations only: yes**, SEMAS gives all three.
3. **Five stations**: an add-on count. As a page of its own it would be the
   thinnest Korean page by stations and by ring share (Anyang, the fewest at
   7, was briefed past the station test on a 64.2% ring share).
4. **Terms: accepted** (SEMAS, the owner's position of 2026-09-29).
5. **Extension or a page: the owner's call, still open** (call 1).
   Gimhae, on the same city's other line, became its own page because "a
   Busan regional map would change a live page" (staging drafts, 2026-10-03).

## What joins - stations, measured from cached files

Placed in a 시군구 by the codes of the SEMAS storefronts within 300 m (the
2026-06-30 edition; each at a share of 1.00); the build places them by the
OSM boundary.

| 시 | Code | Stations (Busan's English names) | Line |
|---|---|---|---|
| 양산 Yangsan | 48330 | Hopo, Jeungsan, Pusan Nat'l Univ. Yangsan Campus, Namyangsan, Yangsan (**5**) | Line 2 |

- **Busan's page: 110 stations kept, 17 listed outside; regional: 115 kept,
  12 listed** (the Busan–Gimhae LRT's 12 in Gimhae, which Gimhae's own page
  draws; `baseline.json`: `stations_kept` 110, `stations_outside` 17).
- **Headway unread**: Busan's operator pages refuse scripts (Yangsan's Band C
  row). Read Line 2's midday service at Yangsan's stations from a named
  source at the build, including whether trains short-turn before 양산; a
  wait beyond 15 minutes is stated on the page (Namyangju's precedent).

## Business leg - two registers, disjoint by municipality

### Busan: unchanged

Busan's keyless `LocalDataService` API pulls (fourteen permit types, frozen
at 2026-04-15) through `pipeline/countries/korea.py`: **89,798 premises**
(Food service 53,152, Retail 20,140, Personal services 16,506;
`baseline.json`). `REGIONAL = False` reproduces it byte for byte.

### Yangsan: SEMAS 상가(상권)정보 (data.go.kr 15083033)

The national cache `data/korea/raw/sbiz_15083033.zip` (edition
**2026-06-30**), member 시도명 **경상남도** (172,887 rows, 22 code/name
pairs, Gimhae's member), `storefronts("경상남도", None,
sigungu_codes=("48330",))`.

**Measured 2026-10-06** (staging, `heavy_job.py` label `korea-ext-measure`):

| 시 | 시군구코드 | Rows | Food service | Retail | Personal services | **In-bucket** | Names withheld |
|---|---|---|---|---|---|---|---|
| 양산 Yangsan | 48330 | 16,790 | 5,710 | 3,826 | 1,666 | **11,202** | 9 |

- No duplicate 상가업소번호, **no category unknown to the taxonomy**, every
  in-bucket row with a point. The master list's 11,202 (5,710 / 3,826 /
  1,666) reproduces.
- **Code and name agree**: 48330 carries only 양산시, the prefix 양산시 only
  48330, identical rows. `SEMAS_SIGUNGU = None`, codes only.
- **Left out by name**: 일반 유흥 주점 270, 구내식당 70, 가정용 연료 소매업 35,
  무도 유흥 주점 7.
- **Extent** (in-bucket points): lat 35.277-**35.524**, lon 128.888-129.212.
  **Yangsan passes Busan's box** (`OSM_BBOX` north edge 35.45; `BUSAN_BBOX`
  derives from it): widen the sanity box under `REGIONAL` (Belo Horizonte's
  `_SANITY`), or apply it to the LOCALDATA rows only.
- **Ring share: 26.4%** (2,958 of 11,202 within 0.6 mi of the 5 stations;
  Busan's own stations add none). Line 2 serves Yangsan's southern new town;
  the city is about 485 km² (general knowledge).

### The join

- **Disjoint by construction**: Busan's API is Busan's 16 구·군; SEMAS is cut
  to 48330. Measured proxy: **0 of Busan's 89,798 premises** have their
  nearest SEMAS storefront both within 50 m and under 48330. No cross-source
  dedup; record that in the drafts file.
- 🚨 **Retail is counted differently.** Busan's whole SEMAS member through
  the same taxonomy, against Busan's LOCALDATA premises: Food service 53,152
  against 50,726 (0.95), **Retail 20,140 against 38,570 (1.92)**, Personal
  services 16,506 against 15,378 (0.93). The Retail heat steps up at the
  city line; `korea-city` trap 4 says the two never compare or sum (call 2).
- **Taxonomy dispatch on `source`** (Los Angeles' pattern), shared with
  Seoul (Regional) and Daegu (Regional) (`seoul_regional.md`).
- **Gimhae stays its own page.** Busan (Regional) adds no Gimhae rows; the
  LRT's 12 Gimhae stations stay listed outside, as now.

## Licenses and notices - already recorded, no new verdict

- **Busan**: PERMITTED WITH CONDITIONS, a credit, notice 49, Busan
  Metropolitan City (`docs/data_sources.md` line 1805;
  `docs/data_sources/south-korea.md`, "Daegu and Busan", line 167).
  Unchanged.
- **SEMAS**: notice 68 (`docs/data_sources.md` line 2246), no new read.
  Its heading and `Notice(68, ...)` in `app/components.py` gain Yangsan on
  Busan (Regional)'s page (wording beyond the template: a drafts proposal).
  Notice 1 gains Yangsan's boundary.
- A registry row (경상남도's member, 48330, the counts, the withheld names)
  and a boundary row in `docs/data_sources/south-korea.md`.
- ⚠️ **The Visuals hold reaches Busan**: a notice-68 page is held off cards
  automatically while SEMAS's social-post scope is open (DECISIONS.md,
  "Daejeon built", Downstream). Busan carries no notice 68 today (call 3).

## Privacy

- SEMAS has **no operator or phone column** (the cached file's 39-column
  header, read 2026-10-06; `korea_sbiz.READ` loads 13, no unit field).
  Busan's API has no operator field, and `sitetel` is never read.
- Withheld by the Korean name rule: **9** in Yangsan, measured; Busan's 114
  unchanged.
- **Run `python scripts/check_personal_exposure.py busan`** on the regional
  file (`processed/regional/` while the switch is on); record the verdict in
  the drafts file and `docs/privacy_verdicts.md`.

## Rail and scope

- No line added. **One Overpass query for 양산시's boundary** (admin_level 6
  in KR-48, resolved by name, area-gated from the fetched polygon), written
  under a new file name so Busan's cache stays as it is. One query in flight
  per session.
- **Scope**: Busan's relation 2396450 plus 양산시. **CRS** UTM 52N,
  EPSG:32652. **Rings** standard, as Busan's.

## Steps, in order

1. **The city alone at zero drift**: `REGIONAL = False` in
   `pipeline/busan/config.py` (`NAME`, `DATA_PROCESSED` to
   `data/busan/processed/regional/`, `TAXONOMY_SYSTEM`), committed off;
   `pipeline/drift_check.py busan` under `heavy_job.py`: no drift.
2. **Fetch** Yangsan's boundary (`pipeline/busan/fetch_sources.py`, new name).
3. **Switch on**; the drift check shows only the extension (110 → 115
   stations, 11,202 SEMAS rows); re-record the baseline deliberately.
4. **Page**: `app/pages/49_Busan_Heatmap.py` stays; the name becomes
   **"Busan (Regional)"** (`app/cities.py`, config `NAME`), `data_age` gives
   both dates (2026-04-15 and 2026-06-30); macro label re-scored at 375, 768
   and 1200 (Busan's label already sits lower left, beside Gimhae's).
5. **What Is Excluded**: Busan's section renamed, a Yangsan section in
   Daejeon's shape (the counts above), 12 stations still listed outside.
   `docs/map_inconsistencies.md`: the Retail step.
6. **Gates** as `seoul_regional.md`; review time only; **reboot: yes**;
   deploy-verify `city-added`.

## Owner calls - open, each with a recommendation

1. **The shape: Busan (Regional), Yangsan's own page, or neither.**
   *Recommend:* Busan (Regional), as marked: 5 stations at a 26.4% ring
   share make the weakest page of any Korean city, and an add-on is the
   pattern for a neighbor with too few stations. *Tradeoff:* it changes a
   live page and brings calls 2 and 3; Yangsan's own page would leave Busan
   untouched (Gimhae's reasoning) but stand on 5 stations. Leaving it
   unbuilt costs nothing live.
2. **The Retail step** (if the extension). *Recommend:* build with the step
   disclosed and counts per source, as `seoul_regional.md` call 1.
   *Tradeoff:* retail heat about 1.9 times denser across the line.
3. **The Visuals hold.** *Recommend:* rule on SEMAS's social-post scope
   before this lands. *Tradeoff:* landing first takes Busan off cards.

## What the build must still measure

- 양산시's relation id and area; the 5 stations inside it by route
  membership.
- Line 2's midday headway at Yangsan's stations, from a named source.
- LOCALDATA premises inside Yangsan's polygon and SEMAS rows inside Busan's
  (0 by the 50 m proxy).
- The withheld count and verdict on the regional file; the ring share on
  step 1's stations.

```brief-checks
[
  {"id": "busan-regional-excluded-total", "claim": "Busan's committed map lists 17 stations outside Busan: Line 2's 5 in Yangsan and the LRT's 12 in Gimhae", "kind": "row_count", "path": "outputs/busan/excluded_stations.csv", "expect": 17},
  {"id": "busan-regional-line2-yangsan", "claim": "Exactly 5 Line 2 stations lie outside Busan, the 5 in Yangsan this page adds", "kind": "row_count", "path": "outputs/busan/excluded_stations.csv", "column": "lines", "equals": "Line 2", "expect": 5},
  {"id": "busan-regional-lrt-stays-out", "claim": "The Busan-Gimhae LRT's 12 Gimhae stations stay outside; Gimhae is its own page", "kind": "row_count", "path": "outputs/busan/excluded_stations.csv", "column": "lines", "equals": "Busan–Gimhae LRT", "expect": 12},
  {"id": "busan-regional-yangsan-station", "claim": "Yangsan station, Line 2's terminus, is outside Busan's map today", "kind": "row_count", "path": "outputs/busan/excluded_stations.csv", "column": "station", "equals": "Yangsan", "expect": 1},
  {"id": "busan-regional-hopo", "claim": "Hopo, the first Line 2 station past Busan's boundary, is outside Busan's map today", "kind": "row_count", "path": "outputs/busan/excluded_stations.csv", "column": "station", "equals": "Hopo", "expect": 1},
  {"id": "busan-regional-projected-crs", "claim": "Busan (Regional) projects to UTM 52N, Yangsan's eastern edge included", "kind": "utm_zone_from_longitude", "lon": 129.212, "expect": "EPSG:32652"}
]
```
