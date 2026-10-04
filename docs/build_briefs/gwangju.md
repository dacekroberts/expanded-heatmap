# Gwangju - build brief

**Band A, owner-approved 2026-10-03** (`docs/decisions_drafts/staging.md`,
"The sweep's first group banded: eleven cities on the owner's approval":
Band R to A on SEMAS's keyless file, keyed on the new district codes; and
"Three build sessions for the twelve candidates (owner)": built by the Korea
session with Daejeon and Gimhae). Step 0 screened 2026-10-03 (staging;
counts only, nothing downloaded). Brief written 2026-10-03. Run
`python scripts/brief_check.py gwangju` before writing any code.

Korean city: read `cjk-text` first, then Incheon's and Gyeonggi's briefs
(`docs/build_briefs/incheon.md`, `gyeonggi.md`): the same source, the same
module and the same rail route. **Copy a Gyeonggi satellite's pipeline**
(Goyang's: part of one SEMAS member), with the code filter below.

🚨 **"Gwangju" names two cities, and its districts' names recur
nationwide.** This page is the five 구 of the former Gwangju Metropolitan
City (광주광역시), now inside **전남광주통합특별시** after the 2026 merger.
**경기도 광주시** (Gyeonggi's Gwangju) is a different city in another member;
동구, 서구, 남구 and 북구 also exist in Busan, Daegu, Incheon, Ulsan and
Daejeon. **Key on 시도명 + 시군구코드, never on names.**

---

## The one-line summary

**SEMAS's national storefront file, cached and keyless: 47,214 storefronts in
all three buckets, every one on the register's own point, filtered by the
five post-merger district codes. Gwangju Metro Line 1, 20 stations, every one
inside the city. The work is a code filter on Incheon's module, one Overpass
query with a boundary check, and the privacy pass.**

---

## Business leg - SEMAS 상가(상권)정보 (data.go.kr 15083033)

| | |
|---|---|
| **Source** | 소상공인시장진흥공단 (Small Enterprise and Market Service, SEMAS), 상가(상권)정보: a national file of trading storefronts, each with a WGS84 point, classified by SEMAS's own 대/중/소분류 |
| **File** | The national cache `data/korea/raw/sbiz_15083033.zip` (352.7 MB, edition **2026-06-30**), downloaded once by `pipeline/countries/korea_sbiz_fetch.py` for Incheon. The same edition every built SEMAS city uses: stay on it |
| **Cadence** | Quarterly. The dataset page reads 수정일 2026-08-05, next registration 2026-10-31 (read 2026-10-03). ⚠️ **The download's file id changes each quarter**: a newer edition is a fetch-script change and moves every SEMAS city at once |
| **Member** | 시도명 **전남광주통합특별시** (시도코드 12): 175,276 rows, Gwangju's five 구 and the 22 Jeonnam 시/군 (12110-12870) |
| **Filter** | 시군구코드 **12210** 동구, **12240** 서구, **12270** 남구, **12300** 북구, **12330** 광산구. The old 광주광역시 29xxx codes are gone; 법정동코드 and 행정동코드 share the new five-digit prefixes, so the file is internally consistent |
| **Currency** | Active storefronts only, re-issued each quarter, so closures drop out (the currency rule passes) |
| **Module** | `pipeline/countries/korea_sbiz.py` (`storefronts()`), classified by `pipeline/taxonomies/korea_sbiz.py` (`bucket()`, keyed at 소분류, the owner's calls 2026-09-29) |

**Measured 2026-10-03** (the screen streamed the member and classified with
the project's own `bucket()`): 75,324 rows in the five codes, no duplicate
상가업소번호, **no 중분류 or 소분류 unknown to the taxonomy**.

| Bucket | Storefronts |
|---|---|
| Food service | 20,701 |
| Retail | 18,706 |
| Personal services | 7,807 |
| **In-bucket** | **47,214** |

- **Placement: 100%.** Every in-bucket row has a parseable 경도/위도 inside
  a generous box of the city (extent lat 35.054-35.251, lon 126.656-127.013);
  none lies more than 15 km from its district's median point. The
  businesses are the register's own rows for the city, as in every built
  SEMAS city; step 1's boundary decides only the station scope.
- **By district** (food / retail / personal): 동구 2,575 / 2,836 / 640;
  서구 4,455 / 4,311 / 1,874; 남구 2,513 / 2,211 / 979; 북구 5,599 / 4,884 /
  2,174; 광산구 5,559 / 4,464 / 2,140.
- **Left out by the taxonomy's 소분류 overrides**: 구내식당 173, 일반 유흥
  주점 571, 무도 유흥 주점 38, 가정용 연료 소매업 70.

### 🚨 The code filter - a change to the shared module

`korea_sbiz.storefronts(sido, sigungu_prefixes)` filters on a 시군구명
**prefix** inside one 시도명, and `READ` does not carry 시군구코드. Measured
2026-10-03 (staging, counts only): inside 전남광주통합특별시 the prefixes
동구/서구/남구/북구/광산구 select **exactly** the same 75,324 rows as the five
codes, because no other 시/군 in the member carries those names. So prefixes
would work today, but only because the 시도명 is fixed first; a name filter is
what the owner's call rules out.

**Recommended:** add `시군구코드` to `READ` and an optional `sigungu_codes`
argument to `storefronts()` (the selected code set asserted equal to the
requested one). The ten built SEMAS cities keep passing prefixes and their
output columns do not change; **run `pipeline/drift_check.py` on all ten**
after the module change (it is shared). Config:
`SEMAS_SIDO = "전남광주통합특별시"`,
`SEMAS_SIGUNGU_CODES = ("12210", "12240", "12270", "12300", "12330")`.
Daejeon's and Gimhae's builds use the same argument; land the change once,
in whichever of the three is built first. This is a measurable-grounds adaptation of a
shared pattern, logged in the drafts file, not an owner call.

### Privacy

- **Run `python scripts/check_personal_exposure.py gwangju`** after step 2;
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
  Gwangju exactly as they cover Incheon. No new license read.
- **Notice 68 names its cities.** Add Gwangju to its heading in
  `docs/data_sources.md` and to the `Notice(68, ...)` title and text in
  `app/components.py`, reusing the displayed wording unchanged otherwise:
  > Storefronts for ... are from the Small Enterprise and Market Service's
  > commercial-district register (소상공인시장진흥공단, 상가(상권)정보, via
  > 공공데이터포털 data.go.kr), 이용허락범위 제한 없음. Changes: filtered to
  > shops, food and drink and personal services, grouped into three
  > categories, and mapped by distance to stations; the categories and counts
  > are this project's, not SEMAS's. Not produced or endorsed by SEMAS.
- **A row in `docs/data_sources/south-korea.md`**, Goyang's shape, naming
  the member 전남광주통합특별시 and the five codes (the reader must see why
  the province is not "광주광역시"). The `app/` change waits for review time.

---

## Rail leg - Gwangju Metro Line 1

| | |
|---|---|
| **System** | Gwangju Metro Line 1 (광주 도시철도 1호선), run by 광주교통공사 (Gwangju Transportation Corporation). Mode **metro** |
| **Stations** | **20, all inside the city**: 녹동 (동구) to 평동 (광산구); 20.5 km. The operator: 20개역 |
| **Headways** | The operator's 운행현황 page (`grtc.co.kr/subway/contents/operationStatus`): 출퇴근 every 5-7 min, 평시 every 10 min; 240 weekday runs, 206 Saturday, 202 holiday. Most trains turn at 소태 |
| **녹동** | One stop beyond 소태, with a thinner service (secondary sources say about hourly). The build reads the operator's 녹동행 table (`/subway/contents/directionOfNokdong`) and records it. Recommended: keep 녹동 as a station of the drawn line, as every station on a drawn metro line is kept, and say on the page that most trains end at 소태 if its service is under the frequency test (a proposal sentence) |
| **Not drawn** | **Line 2 is not open**: phase 1 (시청-광주역, 17 km, 20 stations) moved from 2027-12 to **2028-12**, phase 2 to 2035 (press, 2026-10-02; the operator's own route page still says 2026). Korail and KTX (광주송정): intercity, as everywhere in Korea |
| **Gate 3** | 20 stations, against the operator's own count (운행현황, 역수 20개역) |

- **Rail from OpenStreetMap**, as Incheon and the Gyeonggi cities: no Korean
  agency publishes GTFS, and the national station dataset has no geometry.
  Follow `osm-rail`: one Overpass query for the city (route relations
  matched on route type and `ref`, never `network`), the boundary relation
  fetched by id and area-gated, through `pipeline/osm.py`. **One query in
  flight per session**; after a 504 or 429 wait at least 60 s. Nothing is
  cached for Gwangju yet; staging made no Overpass query.
- ⚠️ **광주송정 is both a Line 1 station and the KTX station.** Stations come
  from route-relation membership, so the Korail node never enters; check the
  drawn one is the metro station.
- 🚨 **The boundary may have moved with the merger.** OSM's 광주광역시
  relation (admin_level 4 before 2026) may have been renamed, demoted or
  replaced by a 전남광주통합특별시 relation. **Resolve it by name and check
  its area** (about 501 km² for the five 구, general knowledge): an area
  near Jeonnam's would be the merged province, not the city. If no relation
  covers exactly the five 구, union the five district relations (동구, 서구,
  남구, 북구, 광산구, each checked to sit inside the old city's extent,
  never matched by name alone) and record that in the drafts file.
- **Query box** (the screen's placed extent plus about 2 km):
  `OSM_BBOX = (35.03, 126.63, 35.27, 127.04)`.
- **Label and color:** the line's public name, labeled on the map and in the
  legend. OSM's color, checked against the bucket colors with
  `pipeline/linecolour.py`.
- **Rings** by the spacing rule, measured at step 1 (a metro's spacing is
  expected above 550 m, so standard rings).
- **English names** from `name:en` first (`cjk-text`): print the coverage.

---

## Scope, CRS, region

- **Scope:** the five 구 of the former 광주광역시, by their codes and the
  checked boundary. The page names the city "Gwangju"; a sentence that the
  districts now sit in 전남광주통합특별시 is not in a template, so it is a
  proposal in the drafts file.
- **CRS:** UTM 52N, **EPSG:32652** (longitude 126.852 falls in the
  126-132 band; checked below). Never buffer in EPSG:4326.
- **Region:** `"East Asia"`. A new label in the region: run
  `check_macro_labels.py` at 375, 768 and 1200 and set its `label_offset`
  from the result.
- **Scaffold:** `scaffold_city.py --slug gwangju --name Gwangju
  --system-name "Gwangju Metro" --taxonomy korea_sbiz --lat 35.160
  --lon 126.852 --region "East Asia" --country "South Korea" --mode metro
  --page-number 191` (`--dry-run` first). No new notice
  number: the Small Enterprise and Market Service's notice 68 extends.

## Owner calls

- **Made:** Band A on SEMAS, keyed on codes, never names (owner,
  2026-10-03); the SEMAS taxonomy and license position (owner, 2026-09-29,
  for every SEMAS city); Korean rail from OSM (Seoul's, Incheon's and
  Gyeonggi's precedent).
- **Open:** none beyond the build's own gates (gate 3, privacy, provenance,
  scope disclosure, `publish-city`). 녹동's sentence and the merger sentence
  are proposals in the drafts file and do not stop the build.

## Downstream (`docs/session_roles.md`, "Downstream sessions")

The build records in its drafts file, for each notice, **card face or
caption only**, and any open terms question:
- **Notice 68, the Small Enterprise and Market Service's (SEMAS): caption.** The terms prescribe a source credit with
  no wording and no place, and the categories stated as this project's.
- **Notice 1 (OpenStreetMap): rail, boundary and station names are OSM**;
  recorded as for every OSM-railed city.
- ⚠️ **Open terms question, known:** the Visuals session's restrictions
  registry (`visuals/data/restrictions.json`, 2026-10-02) holds all ten
  built SEMAS cities `off_cards`: "Korean permission scope (SEMAS): whether
  it reaches social posts is open." Gwangju inherits it, so it stays off
  cards and public pieces until the owner rules on SEMAS.

## What the build must still measure

- The withheld-name count and the privacy verdict.
- The boundary relation (id, name, area) after the merger.
- 녹동's service, station count by route membership (expect 20) and the
  share of storefronts in a ring.

```brief-checks
[
  {
    "id": "gwangju-semas-dataset-page",
    "claim": "SEMAS's 상가(상권)정보 is still published on data.go.kr (15083033), quarterly, declared 이용허락범위 제한 없음",
    "kind": "http_contains",
    "url": "https://www.data.go.kr/data/15083033/fileData.do",
    "present": ["상가(상권)정보", "소상공인시장진흥공단", "이용허락범위", "제한 없음", "분기"]
  },
  {
    "id": "gwangju-line1-operations",
    "claim": "Gwangju Transportation Corporation's 운행현황 page gives Line 1 20 stations (gate 3's count), 평시 headways and 240 weekday runs",
    "kind": "http_contains",
    "url": "https://www.grtc.co.kr/subway/contents/operationStatus",
    "present": ["20개역", "운행시격", "<td>평시</td>", "<td>10분</td>", "240회"]
  },
  {
    "id": "gwangju-nokdong-timetable",
    "claim": "The operator's 녹동행 timetable page, which the build reads for 녹동's thinner service, is still published",
    "kind": "http_contains",
    "url": "https://www.grtc.co.kr/subway/contents/directionOfNokdong",
    "present": ["녹동행", "첫차", "막차"]
  },
  {
    "id": "gwangju-projected-crs",
    "claim": "Gwangju's derived UTM zone is 52N (EPSG:32652)",
    "kind": "utm_zone_from_longitude",
    "lon": 126.852,
    "expect": "EPSG:32652"
  }
]
```
