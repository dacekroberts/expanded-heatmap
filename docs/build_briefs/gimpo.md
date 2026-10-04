# Gimpo - build brief

**Band A, owner-approved 2026-10-04** (`docs/decisions_drafts/staging.md`,
"The probe wave's first results: Korea and Europe banded; Korean regional
expansions marked (owner)": "approve all" on staging's recommendations).
**Gimpo returns from the Gyeonggi scope on the owner's call**: the
satellites' brief left it out on 2026-09-29 ("the smaller 시군", and the
Goldline screened as an edge network on 2026-09-28, not re-measured); the
2026-10-04 screen answered the edge question with the timetable. Step 0
screened 2026-10-04 (staging probe; counts only, nothing downloaded). Brief
written 2026-10-04. Run `python scripts/brief_check.py gimpo` before writing
any code.

Korean city: read `cjk-text` first, then Gyeonggi's and Gimhae's briefs
(`docs/build_briefs/gyeonggi.md`, `gimhae.md`). The business leg is
Incheon's source and module; the rail is one light metro, as Uijeongbu's U
Line and Yongin's EverLine. **Copy a Gyeonggi satellite's pipeline**
(Uijeongbu's: one 시 inside 경기도, a light metro as its main line).

---

## The one-line summary

**SEMAS's national storefront file, cached and keyless: 13,398 storefronts in
all three buckets, every one on the register's own point, 53.4% in a ring.
The Gimpo Goldline, 9 stations in Gimpo, every 6 minutes all day. A
light-rail-only page in the Seoul Capital Area view; the work is a config on
Incheon's module, one Overpass query, and the privacy pass.**

---

## Business leg - SEMAS 상가(상권)정보 (data.go.kr 15083033)

| | |
|---|---|
| **Source** | 소상공인시장진흥공단 (Small Enterprise and Market Service, SEMAS), 상가(상권)정보: a national file of trading storefronts, each with a WGS84 point, classified by SEMAS's own 대/중/소분류 |
| **File** | The national cache `data/korea/raw/sbiz_15083033.zip` (352.7 MB, edition **2026-06-30**), downloaded once by `pipeline/countries/korea_sbiz_fetch.py` for Incheon. The same edition every built SEMAS city uses: stay on it |
| **Cadence** | Quarterly. The dataset page reads 수정일 2026-08-05, next registration 2026-10-31 (read 2026-10-03). ⚠️ **The download's file id changes each quarter**: a newer edition is a fetch-script change and moves every SEMAS city at once |
| **Member** | 시도명 **경기도**, the Gyeonggi satellites' member |
| **Filter** | 시군구코드 **41570** 김포시 (one 시, no 구) |
| **Currency** | Active storefronts only, re-issued each quarter, so closures drop out (the currency rule passes) |
| **Module** | `pipeline/countries/korea_sbiz.py` (`storefronts()`), classified by `pipeline/taxonomies/korea_sbiz.py` (`bucket()`, keyed at 소분류, the owner's calls 2026-09-29) |

**Measured 2026-10-04** (the probe streamed the cached ZIP row by row, keyed
on 시군구코드, classified with the project's own `bucket()`, through
`heavy_job.py`, label `semas-city-screen`): 25,160 rows under 41570, no
duplicate 상가업소번호, **no 중분류 or 소분류 unknown to the taxonomy**, no
row without a point.

| Bucket | Storefronts |
|---|---|
| Food service | 6,112 |
| Retail | 5,512 |
| Personal services | 1,774 |
| **In-bucket** | **13,398** |

- **Placement: 100%.** Every in-bucket row has a point within 25 km of the
  code's median point (none farther). The register's rows span lat
  37.582-37.770, lon 126.524-126.800 (all rows, on a 0.002° grid). The
  businesses are the register's own rows for the city, as in every built
  SEMAS city; step 1's boundary decides only the station scope.
- **Ring share: 53.4%** (7,158 of 13,398 within 0.6 mi of the 9 stations;
  the probe's station points, from the built Korean cities' cached OSM
  route relations, 2026-09-25 to 09-29). Level with Namyangju's 54.9% and
  Yongin's 55.4%.
- The province portal's count on 2026-09-28 was 11,453 (the satellites'
  brief, with cafés, takeaway and barbers out); SEMAS supersedes it, as for
  every satellite.
- **Config:** `SEMAS_SIDO = "경기도"` and the code `41570`. **Key on the
  code.** The `sigungu_codes` filter is on the Korea build's branch
  `korea-sweep-build` (commit 8f0471c9, "korea_sbiz: a 시군구코드 filter, zero
  drift on the ten built SEMAS cities"), landing at review time. **A build
  waits for it to land, or carries that commit** and drift-checks the built
  SEMAS cities; never a second copy of the filter. The 시군구명 prefix
  `("김포시",)` is not measured against the code; the filter asserts that the
  code and the name agree.

### Privacy

- **Run `python scripts/check_personal_exposure.py gimpo`** after step 2;
  record the verdict in the drafts file and its row in
  `docs/privacy_verdicts.md`.
- **Keep `storefronts()`'s name withholding**: a Korean personal name at a
  residential address shows as "Name withheld" (`pipeline/korean_names.py`,
  Seoul's rule). Record the withheld count; the built SEMAS cities withheld
  9-107.
- SEMAS carries no phone or owner column; step 2 reads only the READ
  columns.

### License - already recorded (the Small Enterprise and Market Service's notice 68)

- **PERMITTED WITH CONDITIONS**: data.go.kr 15083033 declares 이용허락범위 제한
  없음, set by SEMAS as provider. Nothing in the terms is per-province or
  per-city, so the read of 2026-09-29 and the owner's reasoned position on
  SEMAS's website copyright policy (`docs/data_sources.md`,
  the Small Enterprise and Market Service's notice 68) cover Gimpo exactly as they
  cover Incheon. No new license read.
- **The SEMAS notice (68) names its cities.** Add Gimpo to its heading in
  `docs/data_sources.md` and to the `Notice(68, ...)` title and text in
  `app/components.py`, reusing the displayed wording unchanged otherwise:
  > Storefronts for ... are from the Small Enterprise and Market Service's
  > commercial-district register (소상공인시장진흥공단, 상가(상권)정보, via
  > 공공데이터포털 data.go.kr), 이용허락범위 제한 없음. Changes: filtered to
  > shops, food and drink and personal services, grouped into three
  > categories, and mapped by distance to stations; the categories and counts
  > are this project's, not SEMAS's. Not produced or endorsed by SEMAS.
- **A row in `docs/data_sources/south-korea.md`**, Goyang's shape (경기도's
  member, code 41570, the counts, the withheld names). The `app/` change
  waits for review time.

---

## Rail leg - the Gimpo Goldline

| | |
|---|---|
| **System** | The Gimpo Goldline (김포 골드라인, 김포도시철도), a driverless two-car light metro, 양촌 to 김포공항, underground (general knowledge: measure the tunnel share at step 1). Mode **light rail** |
| **Stations in Gimpo** | **9**: 양촌, 구래, 마산, 장기, 운양, 걸포북변, 사우, 풍무, 고촌 (the probe's route-relation stations, each placed in 41570 with a share of 1.00) |
| **Out of scope** | **김포공항**, the line's eastern terminus, in Seoul's 강서구: it goes in Gimpo's `excluded_stations.csv` as outside Gimpo's boundary. Seoul's map does not draw the Goldline ("one-station stubs in Seoul", `pipeline/seoul/config.py`) |
| **Headways** | Seoul Metro's cyber-station timetables (timetables posted 2026-09-01), 구래 and 사우: weekdays **every 6.0 min at midday 10-16, longest gap 6**, 258-260 trains a day each way, evening 19-22 longest gap 6. Trains run 양촌 or 구래 to 김포공항, a few from 장기 |
| **Light-rail test** | Passes. Track: purpose-built, underground; frequency far inside 15 min; median nearest-stop spacing **1,457 m** inside Gimpo, above the 550 m guide. The 2026-09-28 "edge network" tag is answered: a light metro on its own track, as the U Line, the EverLine and the Busan–Gimhae LRT, all drawn |
| **Not drawn** | Lines 5 and 9, AREX and the Seohae Line, which meet the Goldline at 김포공항 in Seoul: no station in Gimpo. Place any of their relations the query brings in `NOT_DRAWN`. GTX-A and intercity services, as everywhere in Korea |
| **Gate 3** | The whole line, termini to termini: 10 stations (general knowledge). Read the count from a named source at the build (the operator, or English Wikipedia's infobox as a secondary source, as Ansan read the Suin–Bundang Line's) |

- **Matched on the relation's `ref` `김포 골드라인`** (the satellites' brief's
  2026-09-28 OSM check found it as a `light_rail` relation), public name
  **"Gimpo Goldline"** (Seoul's `pipeline/seoul/config.py` maps the ref to
  that name), drawn to both ends. Labeled on the map and in the legend.
- **Color:** OSM's tag, checked against the bucket colors with
  `pipeline/linecolour.py` (Busan's Line 4 lesson).
- **Rail from OpenStreetMap**, as Seoul, Incheon and the Gyeonggi cities: no
  Korean agency publishes GTFS. Follow `osm-rail`: one Overpass query for
  the city (route relations matched on route type and `ref`, never
  `network`), the boundary relation fetched by id and area-gated, through
  `pipeline/osm.py`. **One query in flight per session**; after a 504 or 429
  wait at least 60 s. Nothing is cached for Gimpo; staging made no Overpass
  query.
- **Boundary:** 김포시, admin_level 6 in 경기도 (KR-41), resolved by name at
  the build. About 277 km² (general knowledge): set `BOUNDARY_AREA_KM2` from
  the fetched polygon.
- **Query box** (the register's extent plus about 2 km, taking in 김포공항 so
  the whole line arrives): `OSM_BBOX = (37.54, 126.50, 37.80, 126.83)`;
  step 1 checks the boundary lies inside.
- **Rings** by the spacing rule: 1,457 m median, so standard rings.
- **English names** from `name:en` first (`cjk-text`): the probe's stations
  all carry one (Yangchon ... Gochon); print the coverage at step 1.

---

## Scope, CRS, region

- **Scope:** Gimpo City (김포시), its OSM boundary.
- **CRS:** UTM 52N, **EPSG:32652** (longitude 126.716 falls in the 126-132
  band, and the register's western edge, 126.524, stays inside it; checked
  below). Never buffer in EPSG:4326.
- **Region:** `"Seoul Capital Area"` with `"in_default_view": False`, as
  every Gyeonggi satellite (owner, 2026-09-29). A new label in the region:
  run `check_macro_labels.py` at 375, 768 and 1200, set its `label_offset`
  from the result, and re-check the region's zoom, since Gimpo widens its
  western extent.
- **Scaffold:** `scaffold_city.py --slug gimpo --name Gimpo
  --system-name "Gimpo Goldline" --taxonomy korea_sbiz --lat 37.615
  --lon 126.716 --region "Seoul Capital Area" --country "South Korea"
  --mode light_rail --page-number <N>` (`--dry-run` first), with a page
  number claimed in `docs/session_roles.md` before scaffolding. No new notice
  number: the Small Enterprise and Market Service's notice 68 extends.

## Owner calls

- **Made:** Band A on SEMAS, Gimpo back from the Gyeonggi scope (owner,
  2026-10-04); the SEMAS taxonomy and license position (owner, 2026-09-29,
  for every SEMAS city); one page per satellite and the Seoul Capital Area
  view (owner, 2026-09-29); Korean rail from OSM.
- **Open:** none beyond the build's own gates (gate 3, the light-rail test
  re-measured at step 1, privacy, provenance, scope disclosure,
  `publish-city`). A page sentence no template covers (for example, that the
  line's tenth station is in Seoul) is a proposal in the drafts file, and
  does not stop the build.

## Downstream (`docs/session_roles.md`, "Downstream sessions")

The build records in its drafts file, for each notice, **card face or
caption only**, and any open terms question:
- **Notice 68, the Small Enterprise and Market Service's (SEMAS): caption.**
  The terms prescribe a source credit with no wording and no place, and the
  categories stated as this project's.
- **Notice 1 (OpenStreetMap): rail, boundary and station names are OSM**;
  recorded as for every OSM-railed city.
- ⚠️ **Open terms question, known: the SEMAS card hold.** The Visuals
  session's restrictions registry (`visuals/data/restrictions.json`,
  2026-10-02) holds the built SEMAS cities `off_cards`: "Korean permission
  scope (SEMAS): whether it reaches social posts is open." Gimpo inherits
  it, so it stays off cards and public pieces until the owner rules on
  SEMAS.

## What the build must still measure

- The withheld-name count and the privacy verdict.
- The boundary relation's id and area; the 9 stations by route membership,
  the tunnel share and the median spacing again (1,457 m at the screen).
- The whole line's station count for gate 3, from a named source.
- The share of storefronts in a ring, on step 1's stations (53.4% at the
  screen).

```brief-checks
[
  {
    "id": "gimpo-semas-dataset-page",
    "claim": "SEMAS's 상가(상권)정보 is still published on data.go.kr (15083033), quarterly, declared 이용허락범위 제한 없음",
    "kind": "http_contains",
    "url": "https://www.data.go.kr/data/15083033/fileData.do",
    "present": ["상가(상권)정보", "소상공인시장진흥공단", "이용허락범위", "제한 없음", "분기"]
  },
  {
    "id": "gimpo-goldline-timetable-gurae",
    "claim": "Seoul Metro's timetable for 구래 (the headway source) still carries the Goldline (김포도시철도), trains from 양촌 and 구래 to 김포공항",
    "kind": "http_contains",
    "url": "http://www.seoulmetro.co.kr/kr/getStationInfo.do?action=time&stationId=4921",
    "present": ["김포도시철도", "양촌 &gt; 김포공항", "구래 &gt; 김포공항", "김포공항 &gt; 양촌"]
  },
  {
    "id": "gimpo-goldline-timetable-sau",
    "claim": "Seoul Metro's timetable for 사우, the second headway station, still carries the Goldline between 양촌 and 김포공항",
    "kind": "http_contains",
    "url": "http://www.seoulmetro.co.kr/kr/getStationInfo.do?action=time&stationId=4926",
    "present": ["김포도시철도", "사우", "양촌 &gt; 김포공항", "김포공항 &gt; 양촌"]
  },
  {
    "id": "gimpo-projected-crs",
    "claim": "Gimpo's derived UTM zone is 52N (EPSG:32652)",
    "kind": "utm_zone_from_longitude",
    "lon": 126.716,
    "expect": "EPSG:32652"
  }
]
```
