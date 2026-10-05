# Siheung - build brief

**Band A, owner-approved 2026-10-04** (`docs/decisions_drafts/staging.md`,
"The probe wave's first results: Korea and Europe banded; Korean regional
expansions marked (owner)": "approve all" on staging's recommendations).
**Siheung was never screened before 2026-10-04**: the satellites' briefs of
2026-09-28 and 09-29 did not list it. Step 0 screened 2026-10-04 (staging
probe; counts only, nothing downloaded). Brief written 2026-10-04; corrected the
same night (the 시군구코드 filter is on master, code and name measured to
agree). Run `python scripts/brief_check.py siheung` before writing any code.

Korean city: read `cjk-text` first, then Gyeonggi's brief
(`docs/build_briefs/gyeonggi.md`, "Ansan" and the Bucheon note). The business
leg is Incheon's source and module; the rail is Ansan's three lines.
**Copy Ansan's pipeline** (`pipeline/ansan/`: one 시 inside 경기도, Line 4,
the Suin–Bundang Line and the Seohae Line, its colors and its gate 3),
with Gimhae's code-keyed register config.

---

## The one-line summary

**SEMAS's national storefront file, cached and keyless: 15,206 storefronts in
all three buckets, every one on the register's own point, 41.2% in a ring.
Nine stations on three Korail lines Seoul's subway signs: Line 4 every 11-12
minutes, the Suin–Bundang and Seohae lines every 15 (borderline, drawn on
Ansan's and Bucheon's precedent). A page in the Seoul Capital Area view; the
work is Ansan's config with a new code and box, one Overpass query, and the
privacy pass.**

---

## Business leg - SEMAS 상가(상권)정보 (data.go.kr 15083033)

| | |
|---|---|
| **Source** | 소상공인시장진흥공단 (Small Enterprise and Market Service, SEMAS), 상가(상권)정보: a national file of trading storefronts, each with a WGS84 point, classified by SEMAS's own 대/중/소분류 |
| **File** | The national cache `data/korea/raw/sbiz_15083033.zip` (352.7 MB, edition **2026-06-30**), downloaded once by `pipeline/countries/korea_sbiz_fetch.py` for Incheon. The same edition every built SEMAS city uses: stay on it |
| **Cadence** | Quarterly. The dataset page reads 수정일 2026-08-05, next registration 2026-10-31 (read 2026-10-03). ⚠️ **The download's file id changes each quarter**: a newer edition is a fetch-script change and moves every SEMAS city at once |
| **Member** | 시도명 **경기도**, the Gyeonggi satellites' member |
| **Filter** | 시군구코드 **41390** 시흥시 (one 시, no 구) |
| **Currency** | Active storefronts only, re-issued each quarter, so closures drop out (the currency rule passes) |
| **Module** | `pipeline/countries/korea_sbiz.py` (`storefronts()`), classified by `pipeline/taxonomies/korea_sbiz.py` (`bucket()`, keyed at 소분류, the owner's calls 2026-09-29) |

**Measured 2026-10-04** (the probe streamed the cached ZIP row by row, keyed
on 시군구코드, classified with the project's own `bucket()`, through
`heavy_job.py`, label `semas-city-screen`): 25,119 rows under 41390, no
duplicate 상가업소번호, **no 중분류 or 소분류 unknown to the taxonomy**, no
row without a point.

| Bucket | Storefronts |
|---|---|
| Food service | 7,273 |
| Retail | 5,763 |
| Personal services | 2,170 |
| **In-bucket** | **15,206** |

- **Placement: 100%.** Every in-bucket row has a point within 25 km of the
  code's median point (none farther). The register's rows span lat
  37.312-37.472, lon 126.674-126.876 (all rows, on a 0.002° grid). The
  businesses are the register's own rows for the city, as in every built
  SEMAS city; step 1's boundary decides only the station scope.
- **Ring share: 41.2%** (6,263 of 15,206 within 0.6 mi of the 9 stations;
  the probe's station points, from the built Korean cities' cached OSM
  route relations, 2026-09-25 to 09-29). Below Ansan's 64.3% and Suwon's
  47.6%, above Hwaseong's 5.2% (left out); the build re-measures it on step
  1's stations.
- **Config, keyed on the code, as Gimhae's** (`pipeline/gimhae/config.py`):
  `SEMAS_SIDO = "경기도"`, `SEMAS_SIGUNGU = None`,
  `SEMAS_SIGUNGU_CODES = ("41390",)`, and step 2 passes
  `sigungu_codes=config.SEMAS_SIGUNGU_CODES` to `storefronts()`. Ansan's
  config keys on a prefix; take Ansan's rail and Gimhae's register config.
  The filter is on master (commit 8f0471c9, "korea_sbiz: a 시군구코드 filter,
  zero drift on the ten built SEMAS cities"; Daejeon, Gwangju and Gimhae
  build on it): nothing to wait for or carry, and never a second copy of the
  filter.
- **Code and name agree** (measured 2026-10-04 by staging through
  `korea_sbiz.province("경기도")`, edition 2026-06-30, `heavy_job.py` label
  `semas-city-screen`): `41390` and the 시군구명 prefix `시흥시` pick the
  **identical 25,119 rows**; the code carries only the name 시흥시 and the
  name only the code 41390. The prefix is redundant, so leave it `None`;
  `storefronts()` exits on an unknown code.

### Privacy

- **Run `python scripts/check_personal_exposure.py siheung`** after step 2;
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
  the Small Enterprise and Market Service's notice 68) cover Siheung exactly as they
  cover Incheon. No new license read.
- **The SEMAS notice (68) names its cities.** Add Siheung to its heading in
  `docs/data_sources.md` and to the `Notice(68, ...)` title and text in
  `app/components.py`, reusing the displayed wording unchanged otherwise:
  > Storefronts for ... are from the Small Enterprise and Market Service's
  > commercial-district register (소상공인시장진흥공단, 상가(상권)정보, via
  > 공공데이터포털 data.go.kr), 이용허락범위 제한 없음. Changes: filtered to
  > shops, food and drink and personal services, grouped into three
  > categories, and mapped by distance to stations; the categories and counts
  > are this project's, not SEMAS's. Not produced or endorsed by SEMAS.
- **A row in `docs/data_sources/south-korea.md`**, Goyang's shape (경기도's
  member, code 41390, the counts, the withheld names). The `app/` change
  waits for review time.

---

## Rail leg - Line 4, the Suin–Bundang Line and the Seohae Line

| | |
|---|---|
| **System** | Three Korail lines the metropolitan subway signs, as Ansan draws them. Mode **metro** |
| **Stations in Siheung** | **9** (the probe's route-relation stations, each placed in 41390 with a share of 1.00). **Seohae Line, 5**: 시흥대야, 신천, 신현, 시흥시청, 시흥능곡. **Suin–Bundang Line, 4**: 월곶, 달월, 오이도, 정왕. **Line 4, 2**: 오이도 (its southern terminus) and 정왕, both shared with the Suin–Bundang Line |
| **Out of scope** | The three lines' stations outside Siheung (Ansan's, Bucheon's, Incheon's and the rest) go in `excluded_stations.csv` as outside Siheung's boundary; their own pages count them |
| **Headways** | Seoul Metro's cyber-station timetables (timetables posted 2026-09-01; they cover the Korail lines), weekday 10-16: **Line 4** at 오이도 and 정왕 every 10.6-11.6 min (longest gap 16-18; evening 19-22 gap up to 29); **Suin–Bundang** at 월곶 and 달월 every **15.0** min (longest gap 20-22; evening gap 25); **Seohae** at 시흥시청 and 신천 every **15.0** min (longest gap 18-19; evening gap 20) |
| **Spacing** | Median nearest same-line station: Line 4 1,230 m, Suin–Bundang 1,270 m, Seohae 1,337 m (any line 1,316 m) |
| **The rail test** | Line 4 passes. **The Suin–Bundang and Seohae lines are borderline**: 15.0 min at midday sits on the 15-minute line of the strict test, with gaps beyond it. They pass on precedent: **Ansan** draws all three lines (Suin–Bundang with its 7 stations; the Seohae Line on Bucheon's precedent), and **Bucheon** draws the Seohae Line on its own track (owner, 2026-09-29). The Gyeonggi satellites applied Seoul's "signed as subway, subway spacing" call, never a frequency gate; the page discloses the 15-minute service |
| **Not drawn** | GTX-A and intercity services, as everywhere in Korea. The Sinansan Line (2028-12, the probe's line-status read) is not open. Ansan's `NOT_DRAWN` (Line 1, Incheon Line 1) for any relation the query box brings without a station in Siheung |
| **Gate 3** | Ansan's: the Suin–Bundang Line's whole 63 (English Wikipedia's infobox, a secondary source, as Seongnam, Suwon, Yongin and Ansan read it); Line 4 left out (the query brings only its service relations that touch the box) and the Seohae Line not gated whole, as in Bucheon and Ansan |

- **Lines, as Ansan's `LINES`** (`pipeline/ansan/config.py`): Line 4 `ref`
  `4`, `#009BCE`, "Line 4"; the Suin–Bundang Line `ref` `수인·분당`,
  `#ECA300`, "Suin–Bundang Line"; the Seohae Line `ref` `서해`, `#5EAC41`,
  "Seohae Line". Each labeled on the map and in the legend, drawn to its
  ends.
- ⚠️ **The Seohae Line in Siheung is Bucheon's shape**: five stations on its
  own track through the city's eastern half, meeting the other two lines
  nowhere in Siheung (it meets them at 초지 in Ansan). The Suin–Bundang Line
  runs the coast through 월곶 and 달월 to 오이도 and 정왕, where Line 4 joins
  it.
- **English names** from `name:en` first (`cjk-text`): two of the probe's
  station nodes, 시흥능곡 and 달월, carry none; take the station object's name
  first (Namyangju's lesson) and print the coverage at step 1.
- **Rail from OpenStreetMap**, as Seoul, Incheon and the Gyeonggi cities: no
  Korean agency publishes GTFS. Follow `osm-rail`: one Overpass query for
  the city (route relations matched on route type and `ref`, never
  `network`; Ansan's `OSM_TRAIN_REFS`), the boundary relation fetched by id
  and area-gated, through `pipeline/osm.py`. **One query in flight per
  session**; after a 504 or 429 wait at least 60 s. Nothing is cached for
  Siheung; staging made no Overpass query.
- **Boundary:** 시흥시, admin_level 6 in 경기도 (KR-41), resolved by name at
  the build. About 139 km² of land (general knowledge); the polygon may take
  in tidal flats and sea, as Ansan's does, so set `BOUNDARY_AREA_KM2` from
  the fetched polygon.
- **Query box** (the register's extent plus about 2 km):
  `OSM_BBOX = (37.29, 126.65, 37.49, 126.90)`; step 1 checks the boundary
  lies inside.
- **Rings** by the spacing rule: 1,316 m median, so standard rings.

---

## Scope, CRS, region

- **Scope:** Siheung City (시흥시), its OSM boundary.
- **CRS:** UTM 52N, **EPSG:32652** (longitude 126.803 falls in the 126-132
  band, as does the register's whole extent; checked below). Never buffer in
  EPSG:4326.
- **Region:** `"Seoul Capital Area"` with `"in_default_view": False`, as
  every Gyeonggi satellite (owner, 2026-09-29). Siheung's dot sits between
  Ansan's, Bucheon's and Incheon's: run `check_macro_labels.py` at 375, 768
  and 1200 and set its `label_offset` from the result, moving no built
  label unless the check leaves no choice.
- **Scaffold:** `scaffold_city.py --slug siheung --name Siheung
  --system-name "Seoul Metropolitan Subway" --taxonomy korea_sbiz
  --lat 37.380 --lon 126.803 --region "Seoul Capital Area"
  --country "South Korea" --mode metro --page-number <N>` (`--dry-run`
  first), with a page number claimed in `docs/session_roles.md` before
  scaffolding. No new notice number:
  the Small Enterprise and Market Service's notice 68 extends.

## Owner calls

- **Made:** Band A on SEMAS (owner, 2026-10-04), with the borderline lines
  passed on Ansan's and Bucheon's precedent as staging recommended; the
  SEMAS taxonomy and license position (owner, 2026-09-29, for every SEMAS
  city); the Seohae Line drawn on its own track (owner, Bucheon,
  2026-09-29); one page per satellite and the Seoul Capital Area view
  (owner, 2026-09-29); Korean rail from OSM.
- **Open:** none beyond the build's own gates (gate 3, privacy, provenance,
  scope disclosure, `publish-city`). The frequency questions raised with
  Cleanup on 2026-10-04 (Namyangju's Gyeongchun Line, Goyang's
  Gyeongui–Jungang Line) do not touch Siheung's lines. A page sentence no
  template covers (for example, the 15-minute service) is a proposal in the
  drafts file, and does not stop the build.

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
  scope (SEMAS): whether it reaches social posts is open." Siheung inherits
  it, so it stays off cards and public pieces until the owner rules on
  SEMAS.

## What the build must still measure

- The withheld-name count and the privacy verdict.
- The boundary relation's id and area; the 9 stations by route membership
  (5 Seohae, 4 Suin–Bundang, 2 Line 4, two shared) and the median spacing
  again (1,316 m at the screen).
- The share of storefronts in a ring, on step 1's stations (41.2% at the
  screen).

```brief-checks
[
  {
    "id": "siheung-semas-dataset-page",
    "claim": "SEMAS's 상가(상권)정보 is still published on data.go.kr (15083033), quarterly, declared 이용허락범위 제한 없음",
    "kind": "http_contains",
    "url": "https://www.data.go.kr/data/15083033/fileData.do",
    "present": ["상가(상권)정보", "소상공인시장진흥공단", "이용허락범위", "제한 없음", "분기"]
  },
  {
    "id": "siheung-seohae-timetable-city-hall",
    "claim": "Seoul Metro's timetable for 시흥시청 (the Seohae headway source) still carries the Seohae Line (서해선), between 원시 and 대곡 or 일산",
    "kind": "http_contains",
    "url": "http://www.seoulmetro.co.kr/kr/getStationInfo.do?action=time&stationId=4809",
    "present": ["서해선", "시흥시청", "대곡 &gt; 원시", "원시 &gt; 일산"]
  },
  {
    "id": "siheung-suin-bundang-timetable-wolgot",
    "claim": "Seoul Metro's timetable for 월곶 (the Suin-Bundang headway source) still carries the Suin-Bundang Line (수인분당선) through to 인천, with 오이도 short workings",
    "kind": "http_contains",
    "url": "http://www.seoulmetro.co.kr/kr/getStationInfo.do?action=time&stationId=1879",
    "present": ["수인분당선", "월곶", "인천 &gt; 왕십리", "오이도 &gt; 인천"]
  },
  {
    "id": "siheung-line4-timetable-oido",
    "claim": "Seoul Metro's timetable for 오이도 (the Line 4 headway source) still has Line 4 (04호선) starting there, to 진접",
    "kind": "http_contains",
    "url": "http://www.seoulmetro.co.kr/kr/getStationInfo.do?action=time&stationId=1762",
    "present": ["04호선", "오이도 &gt; 진접", "오이도 &gt; 사당"]
  },
  {
    "id": "siheung-projected-crs",
    "claim": "Siheung's derived UTM zone is 52N (EPSG:32652)",
    "kind": "utm_zone_from_longitude",
    "lon": 126.803,
    "expect": "EPSG:32652"
  }
]
```
