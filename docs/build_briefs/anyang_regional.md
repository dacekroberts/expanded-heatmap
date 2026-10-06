# Anyang (Regional) - build brief

**A regional extension of a built page, marked by the owner on 2026-10-04**
(`docs/city_master_list.md`, "Add-ons to built cities", "Potential Korean
regional expansions": "Anyang (Regional) + Gunpo (Lines 4 and 1, 6
stations) and Uiwang (1): the same scope", that is the owner's Gyeonggi
scope, which gave "the smaller 시군" no page of their own). Uiwang's one
station was discarded as a city and marked an Anyang (Regional) add-on
(`city_master_list.md` line 674). Released for briefing on 2026-10-06; **the
build stays paused**. Brief written 2026-10-06 by staging from cached files
only (nothing downloaded, no Overpass query). Run `python
scripts/brief_check.py anyang_regional` before writing any code.

Read `regional-extension` and `korea-city` (with `cjk-text`); then
Gyeonggi's brief (`docs/build_briefs/gyeonggi.md`, "Anyang") and Gimpo's for
the code-keyed register config.

---

## The one-line summary

**One register, one source, one notice: Anyang is a SEMAS city already, so
the regional page is a longer 시군구코드 list (41171, 41173, 41410, 41430).
Gunpo and Uiwang add 8,822 storefronts and 7 stations on the two lines
Anyang draws, taking the page from 7 stations and 15,177 storefronts to 14
and 23,999. No new license row, notice or Visuals change; no owner call
open.**

---

## Step 0 - is it an extension? (`regional-extension` Step 0)

1. **Lines already drawn: yes.** All 7 stations are on Line 1 or Line 4,
   Anyang's two lines, and are in Anyang's committed
   `outputs/anyang/excluded_stations.csv` today.
2. **No bucket at a few stations only: yes**, the same register.
3. **One station is enough for an add-on** (Uiwang's own precedent,
   `regional-extension` Step 0 item 3).
4. **Terms: the city's own.** "CNEFE and OSM are the city's own, so no
   licence row and no notice" (Belo Horizonte's precedent, the one-register
   shape).
5. **Extension: the owner's mark** (2026-10-04).

## What joins - stations, measured from cached files

Placed by the codes of the SEMAS storefronts within 300 m (the 2026-06-30
edition; six at a share of 1.00, Geumjeong at 0.99); the build places them by
the OSM boundaries.

| 시 | Code | Stations (Anyang's English names) | Lines |
|---|---|---|---|
| 군포 Gunpo | 41410 | Geumjeong (Line 1 and Line 4), Sanbon, Surisan, Daeyami (Line 4); Gunpo, Dangjeong (Line 1) (**6**) | Line 1, Line 4 |
| 의왕 Uiwang | 41430 | Uiwang (**1**) | Line 1 |

- **Anyang's page: 7 kept, 106 listed outside; regional: 14 kept, 99
  listed** (`baseline.json`: `stations_kept` 7, `stations_outside` 106).
  The master list's counts (6 and 1) reproduce.
- **By line on the regional page**: Line 1 eight (Gwanak, Seoksu, Anyang,
  Myeonghak, Geumjeong, Gunpo, Dangjeong, Uiwang), Line 4 seven (Indeogwon,
  Pyeongchon, Beomgye, Geumjeong, Sanbon, Surisan, Daeyami); Geumjeong
  shared.
- **Gate 3 as Anyang's**: no whole-line gate (`LINE_STATION_COUNTS = {}`,
  `pipeline/anyang/config.py`); read each line's in-scope stations against
  its line table (English Wikipedia, a secondary source) and record the
  agreement, now over three municipalities.
- **English names**: every station object in Anyang has one (the brief);
  check the coverage for the 7 at step 1.
- **Headways**: Line 1 and Line 4 are Seoul's drawn lines; Line 4's service
  south of Geumjeong and Line 1's at Uiwang are not read here. A wait beyond
  15 minutes is stated on the page.

## Business leg - SEMAS 상가(상권)정보, a longer code list

The national cache `data/korea/raw/sbiz_15083033.zip` (edition
**2026-06-30**), member 시도명 **경기도** (672,680 rows, 47 code/name pairs),
through `pipeline/countries/korea_sbiz.py` and `pipeline/taxonomies/korea_sbiz.py`.

**Measured 2026-10-06** (staging, `heavy_job.py` label `korea-ext-measure`,
measured peak 0.99 GB for six members in turn):

| 시군구 | 시군구코드 | Rows | Food service | Retail | Personal services | **In-bucket** | Names withheld |
|---|---|---|---|---|---|---|---|
| 안양시 만안구 + 동안구 (the city) | 41171 + 41173 | 10,493 + 17,712 = 28,205 | 7,010 | 5,853 | 2,314 | **15,177** | 28 |
| 군포 Gunpo | 41410 | 10,235 | 2,885 | 1,992 | 991 | **5,868** | 5 |
| 의왕 Uiwang | 41430 | 5,252 | 1,436 | 1,148 | 370 | **2,954** | 9 |
| **Added** | | **15,487** | **4,321** | **3,140** | **1,361** | **8,822** | **14** |
| **Anyang (Regional)** | | 43,692 | 11,331 | 8,993 | 3,675 | **23,999** | 42 |

- The city's row reproduces Anyang's `baseline.json` (`semas_rows` 28,205,
  `storefronts` 15,177, `names_withheld` 28) on the codes, so the measure
  and the build agree.
- No duplicate 상가업소번호, **no category unknown to the taxonomy**, every
  in-bucket row with a point.
- **Code and name agree**, gimpo.md's test, for all four codes: 41171 is
  only 안양시 만안구 and 41173 only 안양시 동안구 (the prefix 안양시 picks the
  two codes' rows exactly), 41410 only 군포시, 41430 only 의왕시.
- **Left out by name** (added): 일반 유흥 주점 126 (Gunpo 106, Uiwang 20),
  구내식당 42 (23 / 19), 가정용 연료 소매업 19 (13 / 6), 무도 유흥 주점 4 (Gunpo).
- **Extents**: Gunpo lat 37.312-37.378, lon 126.877-126.962; Uiwang
  37.302-37.407, 126.932-127.030. Both pass Anyang's `OSM_BBOX` (37.34,
  126.86, 37.46, 127.01) to the south, Uiwang to the east too; SEMAS rows
  take no box, so only step 1's boundary check needs the wider box.

### Ring shares (0.6 mi)

| 시 | To its own stations | To any station on the regional page |
|---|---|---|
| Gunpo | 84.1% (4,933) | **86.6%** (5,082 of 5,868) |
| Uiwang | 18.7% (552) | **23.3%** (688 of 2,954) |
| **Added** | | **65.4%** (5,770 of 8,822) |

Uiwang's one station rings little of the city (19% at its 2026-10-04
discard); the add-on precedent stands and the share is stated.

## Config: the switch

- **`REGIONAL = False` keeps `SEMAS_SIGUNGU = ("안양시",)`** exactly as now,
  so the city alone reproduces byte for byte.
- **`REGIONAL = True`**: `SEMAS_SIGUNGU = None`, `SEMAS_SIGUNGU_CODES =
  ("41171", "41173", "41410", "41430")` (Gimhae's and Gimpo's code-keyed
  config); step 2 passes `sigungu_codes=` to `storefronts()`, which exits on
  an unknown code. `NAME`, `DATA_PROCESSED` (`data/anyang/processed/regional/`)
  and `CITY_PREFIX` follow the switch.
- One taxonomy, `korea_sbiz`, unchanged: no dispatch.

## Licenses and notices - the city's own

- **SEMAS**: notice 68 (`docs/data_sources.md` line 2246), already Anyang's;
  no new read, no new row in the license table. Its heading and
  `Notice(68, ...)` (`app/components.py` line 2495) carry "Anyang" today:
  the regional name and the two 시 replace it (the wording is a drafts
  proposal).
- **Anyang's registry row** in `docs/data_sources/south-korea.md` (line 25)
  becomes Anyang (Regional)'s: the four codes, the counts, the withheld
  names. Two boundary rows (군포시, 의왕시) join the boundary table; notice 1
  gains them.
- **The Visuals hold is unchanged**: Anyang is a notice-68 city and already
  held off cards while SEMAS's social-post scope is open (DECISIONS.md,
  "Daejeon built", Downstream). The rename is a downstream note.

## Privacy

- SEMAS has **no operator or phone column**: the cached file's 39-column
  header (read 2026-10-06) carries trade and branch names, classification,
  codes, addresses, 동/층/호 unit fields and the point; `korea_sbiz.READ`
  loads 13 and none of the unit fields.
- Withheld by the Korean name rule: **14** added (Gunpo 5, Uiwang 9);
  Anyang's 28 unchanged.
- **Run `python scripts/check_personal_exposure.py anyang`** on the regional
  file (`processed/regional/` while the switch is on); record the verdict in
  the drafts file and `docs/privacy_verdicts.md`.

## Rail and scope

- **One Overpass query for 군포시 and 의왕시** (admin_level 6 in KR-41,
  resolved by name, area-gated from the fetched polygons, about 36 and 54
  km² by general knowledge), written under new file names so Anyang's cache
  (`osm_boundary.json`, `osm_rail_routes.json`, OSM base 2026-07-15) stays as
  it is. The rail relations already arrive whole (the 7 stations are in
  Anyang's excluded list from that cache). One query in flight per session.
- **Box for the regional boundary check**: about (37.28, 126.85, 37.47,
  127.05), the three cities plus about 2 km.
- **Scope**: relation 2409161 (안양시) plus the two. **CRS** UTM 52N,
  EPSG:32652. **Rings** standard (Anyang's 1,487 m median gap; re-measure
  over 14 stations).

## Steps, in order

1. **The city alone at zero drift**: `REGIONAL = False` committed;
   `pipeline/drift_check.py anyang` under `heavy_job.py`: no drift.
2. **Fetch** the two boundaries (`pipeline/anyang/fetch_sources.py`, new
   names).
3. **Switch on**; only the extension moves (7 → 14 stations, 15,177 →
   23,999 storefronts); re-record the baseline deliberately.
4. **Page**: `app/pages/87_Anyang_Heatmap.py` stays; **"Anyang
   (Regional)"** in `app/cities.py` and `NAME`; the Seoul Capital Area
   region's label re-scored at 375, 768 and 1200.
5. **What Is Excluded**: "### Anyang - SEMAS's national storefront register,
   all three buckets" renamed to Anyang (Regional), naming Gunpo and Uiwang,
   the out-by-name counts and withheld names above, and a **Stations.** line
   (14 drawn and ringed, 99 listed outside). `docs/map_inconsistencies.md`
   theme 5.
6. **Gates**: `check_personal_exposure.py anyang`, `check_provenance.py`,
   `check_scope_disclosure.py`, `check_ring_shares.py --write` (Anyang's row
   only); review time only; **reboot: yes**; deploy-verify `city-added`.

## Owner calls

- **Made**: the extension (2026-10-04); SEMAS, its taxonomy and license
  position (2026-09-29); codes, never names (2026-10-03).
- **Open**: none. Uiwang's 23.3% ring share is stated, not a call (its
  precedent was set at the discard).

## What the build must still measure

- The two boundary relations' ids and areas; the 7 stations inside them by
  route membership.
- Each line's in-scope stations against its line table (gate 3's stand-in).
- The withheld count and privacy verdict on the regional file; ring shares
  on step 1's stations.

```brief-checks
[
  {"id": "anyang-regional-excluded-total", "claim": "Anyang's committed map lists 106 stations of its two lines outside Anyang, the list the 7 added stations come from", "kind": "row_count", "path": "outputs/anyang/excluded_stations.csv", "expect": 106},
  {"id": "anyang-regional-gunpo-geumjeong", "claim": "Geumjeong (Gunpo; Line 1 and Line 4) is outside Anyang's map today", "kind": "row_count", "path": "outputs/anyang/excluded_stations.csv", "column": "station", "equals": "Geumjeong", "expect": 1},
  {"id": "anyang-regional-gunpo-sanbon", "claim": "Sanbon (Gunpo, Line 4) is outside Anyang's map today", "kind": "row_count", "path": "outputs/anyang/excluded_stations.csv", "column": "station", "equals": "Sanbon", "expect": 1},
  {"id": "anyang-regional-gunpo-surisan", "claim": "Surisan (Gunpo, Line 4) is outside Anyang's map today", "kind": "row_count", "path": "outputs/anyang/excluded_stations.csv", "column": "station", "equals": "Surisan", "expect": 1},
  {"id": "anyang-regional-gunpo-daeyami", "claim": "Daeyami (Gunpo, Line 4) is outside Anyang's map today", "kind": "row_count", "path": "outputs/anyang/excluded_stations.csv", "column": "station", "equals": "Daeyami", "expect": 1},
  {"id": "anyang-regional-gunpo-gunpo", "claim": "Gunpo station (Line 1) is outside Anyang's map today", "kind": "row_count", "path": "outputs/anyang/excluded_stations.csv", "column": "station", "equals": "Gunpo", "expect": 1},
  {"id": "anyang-regional-gunpo-dangjeong", "claim": "Dangjeong (Gunpo, Line 1) is outside Anyang's map today", "kind": "row_count", "path": "outputs/anyang/excluded_stations.csv", "column": "station", "equals": "Dangjeong", "expect": 1},
  {"id": "anyang-regional-uiwang", "claim": "Uiwang station (Line 1), the one-station add-on, is outside Anyang's map today", "kind": "row_count", "path": "outputs/anyang/excluded_stations.csv", "column": "station", "equals": "Uiwang", "expect": 1},
  {"id": "anyang-regional-projected-crs", "claim": "Anyang (Regional) projects to UTM 52N, Uiwang's eastern edge included", "kind": "utm_zone_from_longitude", "lon": 127.03, "expect": "EPSG:32652"}
]
```
