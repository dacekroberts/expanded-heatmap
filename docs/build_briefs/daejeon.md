# Daejeon - build brief

**Band A, owner-approved 2026-10-03** (`docs/decisions_drafts/staging.md`,
"The sweep's first group banded: eleven cities on the owner's approval":
Band R to A on SEMAS's keyless file; and "Three build sessions for the twelve
candidates (owner)": built by the Korea session with Gwangju and Gimhae).
Step 0 screened 2026-10-03 (staging; counts only, nothing downloaded). Brief
written 2026-10-03. Run `python scripts/brief_check.py daejeon` before
writing any code.

Korean city: read `cjk-text` first, then Incheon's and Gyeonggi's briefs
(`docs/build_briefs/incheon.md`, `gyeonggi.md`): the same source, the same
module and the same rail route. **Copy Incheon's pipeline** (a whole
metropolitan city on one SEMAS member, `SEMAS_SIGUNGU = None`).

---

## The one-line summary

**SEMAS's national storefront file, cached and keyless: 50,939 storefronts in
all three buckets, every one on the register's own point. Daejeon Metro Line
1, 22 stations, every one inside the city. The work is a config on Incheon's
module, one Overpass query, and the privacy pass.**

---

## Business leg - SEMAS 상가(상권)정보 (data.go.kr 15083033)

| | |
|---|---|
| **Source** | 소상공인시장진흥공단 (Small Enterprise and Market Service, SEMAS), 상가(상권)정보: a national file of trading storefronts, each with a WGS84 point, classified by SEMAS's own 대/중/소분류 |
| **File** | The national cache `data/korea/raw/sbiz_15083033.zip` (352.7 MB, edition **2026-06-30**), downloaded once by `pipeline/countries/korea_sbiz_fetch.py` for Incheon. The same edition every built SEMAS city uses: stay on it |
| **Cadence** | Quarterly. The dataset page reads 수정일 2026-08-05, next registration 2026-10-31 (read 2026-10-03). ⚠️ **The download's file id changes each quarter**: a newer edition is a fetch-script change, not a step change, and moves every SEMAS city at once |
| **Member** | 시도명 **대전광역시** (a province's CSV is found by its first row's 시도명; the ZIP's member names are undecodable) |
| **Filter** | 시군구코드 **30110** 동구, **30140** 중구, **30170** 서구, **30200** 유성구, **30230** 대덕구: Daejeon's five 구, no 군. ⚠️ 동구, 서구 and 중구 recur in Busan, Daegu, Incheon and Ulsan, so never key on 시군구명 outside the fixed 시도명 |
| **Currency** | Active storefronts only, re-issued each quarter, so closures drop out (the currency rule passes) |
| **Module** | `pipeline/countries/korea_sbiz.py` (`storefronts()`), classified by `pipeline/taxonomies/korea_sbiz.py` (`bucket()`, keyed at 소분류, the owner's calls 2026-09-29) |

**Measured 2026-10-03** (the screen streamed the member and classified with
the project's own `bucket()`): 80,704 rows in the five codes, no duplicate
상가업소번호, **no 중분류 or 소분류 unknown to the taxonomy**. A second pass
the same day (staging, counts only, peak 0.03 GB) found **the whole
대전광역시 member is those 80,704 rows**: exactly the five code/name pairs,
동구 11,824, 중구 13,483, 서구 27,753, 유성구 19,141, 대덕구 8,503.

| Bucket | Storefronts |
|---|---|
| Food service | 23,402 |
| Retail | 20,100 |
| Personal services | 7,437 |
| **In-bucket** | **50,939** |

- **Placement: 100%.** Every in-bucket row has a parseable 경도/위도 inside
  a generous box of the city (extent lat 36.197-36.494, lon 127.249-127.538);
  4 points lie more than 15 km from their district's median point. The
  businesses are the register's own rows for the city, as in every built
  SEMAS city; step 1's boundary decides only the station scope.
- **By district** (food / retail / personal): 동구 3,380 / 3,386 / 986;
  중구 3,908 / 3,817 / 1,107; 서구 7,329 / 6,235 / 2,868; 유성구 6,145 /
  4,466 / 1,674; 대덕구 2,640 / 2,196 / 802.
- **Left out by the taxonomy's 소분류 overrides**: 구내식당 164, 일반 유흥
  주점 266, 무도 유흥 주점 18, 가정용 연료 소매업 114.
- **Config:** `SEMAS_SIDO = "대전광역시"` and the five codes, through the
  `sigungu_codes` argument Gwangju's brief recommends adding to
  `korea_sbiz.storefronts()` (with `시군구코드` added to `READ`; land it once,
  in whichever Korean city is built first, and drift-check the ten built
  SEMAS cities). Today the five codes select the whole member, so
  `SEMAS_SIGUNGU = None` (Incheon's shape) gives the same rows; the code
  filter makes a sixth district or a merger fail loudly instead of widening
  the page.

### Privacy

- **Run `python scripts/check_personal_exposure.py daejeon`** after step 2;
  record the verdict in the drafts file and its row in
  `docs/privacy_verdicts.md`.
- **Keep `storefronts()`'s name withholding**: a Korean personal name at a
  residential address shows as "Name withheld" (`pipeline/korean_names.py`,
  Seoul's rule). Record the withheld count; the built SEMAS cities withheld
  9-107.
- SEMAS carries no phone or owner column; step 2 reads only the READ
  columns.

### License - already recorded (notice 68)

- **PERMITTED WITH CONDITIONS**: data.go.kr 15083033 declares 이용허락범위 제한
  없음, set by SEMAS as provider. Nothing in the terms is per-province or
  per-city, so the read of 2026-09-29 and the owner's reasoned position on
  SEMAS's website copyright policy (`docs/data_sources.md`, notice 68) cover
  Daejeon exactly as they cover Incheon. No new license read.
- **Notice 68 names its cities.** Add Daejeon to its heading in
  `docs/data_sources.md` and to the `Notice(68, ...)` title and text in
  `app/components.py`, reusing the displayed wording unchanged otherwise:
  > Storefronts for ... are from the Small Enterprise and Market Service's
  > commercial-district register (소상공인시장진흥공단, 상가(상권)정보, via
  > 공공데이터포털 data.go.kr), 이용허락범위 제한 없음. Changes: filtered to
  > shops, food and drink and personal services, grouped into three
  > categories, and mapped by distance to stations; the categories and counts
  > are this project's, not SEMAS's. Not produced or endorsed by SEMAS.
- **A row in `docs/data_sources/south-korea.md`**, Goyang's shape
  ("the same national file as Incheon's (row above)", 대전광역시's member, the
  five codes, the counts, the withheld names). The `app/` change waits for
  review time.

---

## Rail leg - Daejeon Metro Line 1

| | |
|---|---|
| **System** | Daejeon Metro Line 1 (대전 도시철도 1호선), run by 대전교통공사 (Daejeon Transportation Corporation). Mode **metro** (mostly underground) |
| **Stations** | **22, all inside Daejeon**: 판암 (동구) to 반석 (유성구). The operator: 22.6 km, 판암동 to 외삼동, 22 정거장 (12 in phase 1, 10 in phase 2) |
| **Headways** | The operator's timetable for 탄방 (djtc.kr station page, station_code 1110, read through the page's own `ajaxFindStationInfo.do` call): weekdays every 10 min 10:00-16:00, 5-6 min in the 07-08 and 18 peaks, longest daytime gap 12 min; weekends every 10 min; service 05:33-23:58 |
| **Not drawn** | Line 2 (a tram, under construction, not open). Korail and KTX (대전, 서대전): intercity, as everywhere in Korea |
| **Gate 3** | 22 stations, against the operator's own count (`djtc.kr/kor/page.do?menuIdx=460`, 시설현황) |

- **Rail from OpenStreetMap**, as Incheon and the Gyeonggi cities: no Korean
  agency publishes GTFS, and the national station dataset has no geometry.
  Follow `osm-rail`: one Overpass query for the city (route relations
  matched on route type and `ref`, never `network`), the boundary relation
  fetched by id and area-gated, through `pipeline/osm.py`. **One query in
  flight per session**; after a 504 or 429 wait at least 60 s. Nothing is
  cached for Daejeon yet; staging made no Overpass query.
- ⚠️ **대전역 is both a Line 1 station and the Korail station.** Stations come
  from route-relation membership, so the Korail node never enters; check the
  drawn 대전 is the metro one.
- **Boundary:** 대전광역시, admin_level 4, resolved by name at the build.
  About 540 km² (general knowledge): set `BOUNDARY_AREA_KM2` from the fetched
  polygon, an inland city, so no territorial water.
- **Query box** (the screen's placed extent plus about 2 km):
  `OSM_BBOX = (36.17, 127.22, 36.52, 127.57)`.
- **Label and color:** the line's public name, labeled on the map and in the
  legend. OSM's color, checked against the bucket colors with
  `pipeline/linecolour.py` (Busan's Line 4 lesson).
- **Rings** by the spacing rule, measured at step 1 (a metro's spacing is
  expected above 550 m, so standard rings).
- **English names** from `name:en` first (`cjk-text`): print the coverage.

---

## Scope, CRS, region

- **Scope:** Daejeon Metropolitan City (대전광역시), its five 구.
- **CRS:** UTM 52N, **EPSG:32652** (longitude 127.385 falls in the
  126-132 band; checked below). Never buffer in EPSG:4326.
- **Region:** `"East Asia"`, with Seoul, Daegu and Busan. A new label in the
  region: run `check_macro_labels.py` at 375, 768 and 1200 and set its
  `label_offset` from the result.
- **Scaffold:** `scaffold_city.py --slug daejeon --name Daejeon
  --system-name "Daejeon Metro" --taxonomy korea_sbiz --lat 36.351
  --lon 127.385 --region "East Asia" --country "South Korea" --mode metro
  --page-number <the Korea kit's claim>` (`--dry-run` first). No new notice
  number: notice 68 extends, and OSM is notice 1.

## Owner calls

- **Made:** Band A on SEMAS (owner, 2026-10-03); the SEMAS taxonomy and
  license position (owner, 2026-09-29, for every SEMAS city); Korean rail
  from OSM (Seoul's, Incheon's and Gyeonggi's precedent).
- **Open:** none beyond the build's own gates (gate 3, privacy, provenance,
  scope disclosure, `publish-city`). A page sentence no template covers is a
  proposal in the drafts file, and does not stop the build.

## Downstream (`docs/session_roles.md`, "Downstream sessions")

The build records in its drafts file, for each notice, **card face or
caption only**, and any open terms question:
- **Notice 68 (SEMAS): caption.** The terms prescribe a source credit with
  no wording and no place, and the categories stated as this project's.
- **Notice 1 (OpenStreetMap): rail, boundary and station names are OSM**;
  recorded as for every OSM-railed city.
- ⚠️ **Open terms question, known:** the Visuals session's restrictions
  registry (`visuals/data/restrictions.json`, 2026-10-02) holds all ten
  built SEMAS cities `off_cards`: "Korean permission scope (SEMAS): whether
  it reaches social posts is open." Daejeon inherits it, so it stays off
  cards and public pieces until the owner rules on SEMAS.

## What the build must still measure

- The withheld-name count and the privacy verdict.
- Station count by route membership (expect 22) and the share of
  storefronts in a ring.
- The boundary relation's id and area.

```brief-checks
[
  {
    "id": "daejeon-semas-dataset-page",
    "claim": "SEMAS's 상가(상권)정보 is still published on data.go.kr (15083033), quarterly, declared 이용허락범위 제한 없음",
    "kind": "http_contains",
    "url": "https://www.data.go.kr/data/15083033/fileData.do",
    "present": ["상가(상권)정보", "소상공인시장진흥공단", "이용허락범위", "제한 없음", "분기"]
  },
  {
    "id": "daejeon-line1-operator-facts",
    "claim": "Daejeon Transportation Corporation's facilities page gives Line 1 as 22.6 km, 판암동 to 외삼동, with 22 stations (gate 3's count)",
    "kind": "http_contains",
    "url": "https://www.djtc.kr/kor/page.do?menuIdx=460",
    "present": ["22.6km", "판암동", "외삼동", "22개소"]
  },
  {
    "id": "daejeon-line1-station-pages",
    "claim": "The operator's station pages (the source of the 탄방 timetable) still list the line from 반석 to 판암",
    "kind": "http_contains",
    "url": "https://www.djtc.kr/kor/stationInfo.do?menuIdx=38",
    "present": ["반석역", "판암역", "탄방역", "대전역"]
  },
  {
    "id": "daejeon-projected-crs",
    "claim": "Daejeon's derived UTM zone is 52N (EPSG:32652)",
    "kind": "utm_zone_from_longitude",
    "lon": 127.385,
    "expect": "EPSG:32652"
  }
]
```
