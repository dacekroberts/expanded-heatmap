# Daegu (Regional) - build brief

**A regional extension of a built page, marked by the owner on 2026-10-04**
(`docs/city_master_list.md`, "Add-ons to built cities", "Potential Korean
regional expansions": "Daegu (Regional) + Gyeongsan (Daegu Lines 1 and 2, 5
stations; Band C until chosen)"). Gyeongsan's Band C row (line 140) reads "A
page of its own, or Daegu (Regional), as Yangsan". Released for briefing on
2026-10-06; **the build stays paused**. Brief written 2026-10-06 by staging
from cached files only (nothing downloaded, no Overpass query). Run
`python scripts/brief_check.py daegu_regional` before writing any code.

Read `regional-extension`, `multi-source-city`, `korea-city` and `cjk-text`;
then Daegu's brief (`docs/build_briefs/daegu.md`) and `seoul_regional.md`,
which sets out the same two-register join at more length.

---

## The one-line summary

**Daegu keeps its LOCALDATA permit files; Gyeongsan joins on SEMAS's national
storefront file, code 47290: 8,943 storefronts and the 5 stations Lines 1 and
2 already reach, 35.0% of them in a ring. Every station Daegu's map lists as
outside comes in, so the page lists none. The registers count Retail
differently (SEMAS about 1.9 times Daegu's permits), and Daegu would take on
notice 68 and the Visuals card hold. The owner's first call is the shape.**

---

## Step 0 - is it an extension? (`regional-extension` Step 0)

1. **Lines already drawn: yes.** Line 1's Hayang extension and Line 2's
   eastern end run into Gyeongsan, drawn to their ends on Daegu's map; the 5
   are the whole of Daegu's committed `outputs/daegu/excluded_stations.csv`.
2. **No bucket at a few stations only: yes.**
3. **Five stations**: an add-on count (Anyang, the fewest on a Korean page at
   7, was briefed on a 64.2% ring share).
4. **Terms: accepted** (SEMAS, 2026-09-29).
5. **Extension or a page: the owner's call, still open** (call 1).

## What joins - stations, measured from cached files

Placed by the codes of the SEMAS storefronts within 300 m (each at a share of
1.00); the build places them by the OSM boundary.

| 시 | Code | Stations (Daegu's English names) | Lines |
|---|---|---|---|
| 경산 Gyeongsan | 47290 | Buho, Hayang (Line 1); Imdang, Jeongpyeong, Yeungnam University (Line 2) (**5**) | Line 1, Line 2 |

- **Daegu's page: 86 stations kept, 5 listed outside; regional: 91 kept, 0
  listed** (`baseline.json`: `stations_kept` 86, `stations_outside` 5). With
  nothing left outside, the page's **Stations.** line and
  `excluded_stations.csv` change shape; `check_scope_disclosure.py`
  (property E) decides whether an empty list is accepted *(not tested here)*.
- **Headways unread**: Daegu's site answers a cookie challenge (Gyeongsan's
  Band C row). Read Line 1's Hayang extension and Line 2's eastern end from a
  named source at the build; a wait beyond 15 minutes is stated on the page.
- **대경선 stays undrawn** (owner, on spacing; `south-korea.md`): it serves
  경산 station (general knowledge), which no drawn line reaches.

## Business leg - two registers, disjoint by municipality

### Daegu: unchanged

Daegu's LOCALDATA files (fourteen types, `dg_*_202608.xlsx`, "a year older
than their label", Daegu's What Is Excluded section) through
`pipeline/countries/korea.py`: **67,212 premises** (Food service 38,468,
Retail 16,269, Personal services 12,475; `baseline.json`). `REGIONAL =
False` reproduces it byte for byte.

### Gyeongsan: SEMAS 상가(상권)정보 (data.go.kr 15083033)

The national cache (edition **2026-06-30**), member 시도명 **경상북도**
(144,967 rows, 23 code/name pairs), `storefronts("경상북도", None,
sigungu_codes=("47290",))`. A new member for the project: no built city
reads 경상북도 yet.

**Measured 2026-10-06** (staging, `heavy_job.py` label `korea-ext-measure`):

| 시 | 시군구코드 | Rows | Food service | Retail | Personal services | **In-bucket** | Names withheld |
|---|---|---|---|---|---|---|---|
| 경산 Gyeongsan | 47290 | 13,217 | 4,476 | 3,223 | 1,244 | **8,943** | 5 |

- No duplicate 상가업소번호, **no category unknown to the taxonomy**, every
  in-bucket row with a point; the master list's 8,943 (4,476 / 3,223 /
  1,244) reproduces.
- **Code and name agree**: 47290 carries only 경산시, the prefix only 47290,
  identical rows. Codes only.
- **Left out by name**: 일반 유흥 주점 87, 가정용 연료 소매업 55, 구내식당 47,
  무도 유흥 주점 2.
- **Extent**: lat 35.722-35.986, lon 128.709-**128.939**. **Gyeongsan
  passes Daegu's box** (`OSM_BBOX` east edge 128.85; `DAEGU_BBOX` derives
  from it): widen the sanity box under `REGIONAL`, or apply it to the
  LOCALDATA rows only.
- **Ring share: 35.0%** to its own 5 stations (3,130 of 8,943), **35.3%** to
  any station on the regional page (3,160). Gyeongsan is about 411 km²
  (general knowledge).

### The join

- **Disjoint by construction**: Daegu's files are Daegu's own 구·군 (with
  군위군); SEMAS is cut to 47290. Measured proxy: **1 of Daegu's 67,212
  premises** has its nearest SEMAS storefront both within 50 m and under
  47290 (a border premises or a point off by a street; the build tests it
  against the polygons). No cross-source dedup; record that.
- 🚨 **Retail is counted differently**: Daegu's whole SEMAS member against
  Daegu's LOCALDATA premises: Food service 38,468 against 36,347 (0.94),
  **Retail 16,269 against 30,205 (1.86)**, Personal services 12,475 against
  11,290 (0.91). Trap 4 again (call 2).
- **Taxonomy dispatch on `source`**, shared with Seoul (Regional) and Busan
  (Regional) (`seoul_regional.md`).

## Licenses and notices - already recorded, no new verdict

- **Daegu**: notice 48, Daegu Metropolitan City (`docs/data_sources.md` line
  1793; `docs/data_sources/south-korea.md`, "Daegu and Busan", line 167).
- **SEMAS**: notice 68, Small Enterprise and Market Service
  (`docs/data_sources.md` line 2246), no new read; its heading and the
  Small Enterprise and Market Service notice gain Gyeongsan on Daegu
  (Regional)'s page (a drafts proposal for the wording). Notice 1,
  OpenStreetMap, gains Gyeongsan's boundary.
- A registry row (경상북도's member, 47290) and a boundary row in
  `docs/data_sources/south-korea.md`.
- ⚠️ **The Visuals hold reaches Daegu**: notice 68 is held off cards
  automatically while SEMAS's social-post scope is open (call 3).

## Privacy

- SEMAS has **no operator or phone column** (the cached 39-column header,
  read 2026-10-06; `READ` loads 13). Daegu's files have no operator field;
  `소재지전화` is never read.
- Withheld by the Korean name rule: **5** in Gyeongsan; Daegu's 113
  unchanged.
- **Run `python scripts/check_personal_exposure.py daegu`** on the regional
  file; verdict in the drafts file and `docs/privacy_verdicts.md`.

## Rail and scope

- No line added. **One Overpass query for 경산시's boundary** (admin_level 6
  in KR-47, resolved by name, area-gated), under a new file name. One query
  in flight per session.
- **Scope**: Daegu's relation 2395674 (with 군위군) plus 경산시. **CRS** UTM
  52N, EPSG:32652. **Rings** standard.

## Steps, in order

1. **The city alone at zero drift**: `REGIONAL = False` in
   `pipeline/daegu/config.py` (`NAME`, `DATA_PROCESSED` to
   `data/daegu/processed/regional/`, `TAXONOMY_SYSTEM`), committed off;
   `pipeline/drift_check.py daegu` under `heavy_job.py`: no drift.
2. **Fetch** Gyeongsan's boundary (`pipeline/daegu/fetch_sources.py`).
3. **Switch on**; only the extension moves (86 → 91 stations, 8,943 SEMAS
   rows); re-record the baseline.
4. **Page**: `app/pages/48_Daegu_Heatmap.py` stays; **"Daegu (Regional)"**;
   `data_age` with both dates; macro label re-scored at 375, 768 and 1200.
5. **What Is Excluded**: Daegu's section renamed, a Gyeongsan section in
   Daejeon's shape, the Stations line rewritten for an empty outside list.
   `docs/map_inconsistencies.md`: the Retail step.
6. **Gates** as `seoul_regional.md`; review time only; **reboot: yes**;
   deploy-verify `city-added`.

## Owner calls - open, each with a recommendation

1. **The shape: Daegu (Regional), Gyeongsan's own page, or neither.**
   *Recommend:* Daegu (Regional), as marked: it closes Daegu's whole outside
   list, and 5 stations at 35.0% make a weak page of their own. *Tradeoff:*
   a live page changes and calls 2 and 3 follow; a page of its own leaves
   Daegu untouched on 5 stations.
2. **The Retail step.** *Recommend:* disclosed, counts per source, as
   `seoul_regional.md` call 1. *Tradeoff:* retail heat about 1.9 times
   denser across the line.
3. **The Visuals hold.** *Recommend:* rule on SEMAS's social-post scope
   first. *Tradeoff:* landing first takes Daegu off cards.

## What the build must still measure

- 경산시's relation id and area; the 5 stations inside it by route
  membership.
- The midday headways at the 5 stations, from a named source.
- The one border premises, and SEMAS rows inside Daegu's polygon.
- Whether `check_scope_disclosure.py` accepts an empty outside list.
- The withheld count and verdict on the regional file; the ring share on
  step 1's stations.

```brief-checks
[
  {"id": "daegu-regional-excluded-total", "claim": "Daegu's committed map lists exactly 5 stations outside Daegu, all 5 in Gyeongsan", "kind": "row_count", "path": "outputs/daegu/excluded_stations.csv", "expect": 5},
  {"id": "daegu-regional-line1", "claim": "Two of them are Line 1's (Buho, Hayang)", "kind": "row_count", "path": "outputs/daegu/excluded_stations.csv", "column": "lines", "equals": "Line 1", "expect": 2},
  {"id": "daegu-regional-line2", "claim": "Three of them are Line 2's (Imdang, Jeongpyeong, Yeungnam University)", "kind": "row_count", "path": "outputs/daegu/excluded_stations.csv", "column": "lines", "equals": "Line 2", "expect": 3},
  {"id": "daegu-regional-yeungnam", "claim": "Yeungnam University, Line 2's eastern terminus, is outside Daegu's map today", "kind": "row_count", "path": "outputs/daegu/excluded_stations.csv", "column": "station", "equals": "Yeungnam University", "expect": 1},
  {"id": "daegu-regional-projected-crs", "claim": "Daegu (Regional) projects to UTM 52N, Gyeongsan's eastern edge included", "kind": "utm_zone_from_longitude", "lon": 128.939, "expect": "EPSG:32652"}
]
```
