# Gimhae - build brief

**Band A, owner-approved 2026-10-03** (`docs/decisions_drafts/staging.md`,
"The sweep's first group banded: eleven cities on the owner's approval":
Band R to A on SEMAS's keyless file, and **Gimhae is its own page**, the
Gyeonggi satellites' precedent, since a Busan regional map would change a
live page; and "Three build sessions for the twelve candidates (owner)":
built by the Korea session with Daejeon and Gwangju). Step 0 screened
2026-10-03 (staging; counts only, nothing downloaded). Brief written
2026-10-03. Run `python scripts/brief_check.py gimhae` before writing any
code.

Korean city: read `cjk-text` first, then Incheon's, Gyeonggi's and Busan's
briefs (`docs/build_briefs/incheon.md`, `gyeonggi.md`, `busan.md`). The
business leg is Incheon's source and module; the rail is Busan's
Busan–Gimhae LRT, already drawn on Busan's map. **Copy a Gyeonggi
satellite's pipeline** (Goyang's: one 시 inside a province member) and
Busan's LRT entry. Busan's brief calls Gimhae Band D (no reachable
register): superseded by SEMAS, 2026-10-03.

---

## The one-line summary

**SEMAS's national storefront file, cached and keyless: 17,879 storefronts in
all three buckets, every one on the register's own point. The Busan–Gimhae
LRT, 12 stations in Gimhae, every 5-6 minutes all day on its own elevated
track. A light-rail-only page; the work is a config on Incheon's module, one
Overpass query, and the privacy pass.**

---

## Business leg - SEMAS 상가(상권)정보 (data.go.kr 15083033)

| | |
|---|---|
| **Source** | 소상공인시장진흥공단 (Small Enterprise and Market Service, SEMAS), 상가(상권)정보: a national file of trading storefronts, each with a WGS84 point, classified by SEMAS's own 대/중/소분류 |
| **File** | The national cache `data/korea/raw/sbiz_15083033.zip` (352.7 MB, edition **2026-06-30**), downloaded once by `pipeline/countries/korea_sbiz_fetch.py` for Incheon. The same edition every built SEMAS city uses: stay on it |
| **Cadence** | Quarterly. The dataset page reads 수정일 2026-08-05, next registration 2026-10-31 (read 2026-10-03). ⚠️ **The download's file id changes each quarter**: a newer edition is a fetch-script change and moves every SEMAS city at once |
| **Member** | 시도명 **경상남도**: 172,887 rows in 22 시/군 code/name pairs |
| **Filter** | 시군구코드 **48250** 김해시 (one 시, no 구) |
| **Currency** | Active storefronts only, re-issued each quarter, so closures drop out (the currency rule passes) |
| **Module** | `pipeline/countries/korea_sbiz.py` (`storefronts()`), classified by `pipeline/taxonomies/korea_sbiz.py` (`bucket()`, keyed at 소분류, the owner's calls 2026-09-29) |

**Measured 2026-10-03** (the screen streamed the member and classified with
the project's own `bucket()`): 26,700 rows under 48250, no duplicate
상가업소번호, **no 중분류 or 소분류 unknown to the taxonomy**. A second pass
the same day (staging, counts only) found the 시군구명 prefix 김해시 selects
exactly the same 26,700 rows as the code.

| Bucket | Storefronts |
|---|---|
| Food service | 8,558 |
| Retail | 6,662 |
| Personal services | 2,659 |
| **In-bucket** | **17,879** |

- **Placement: 100%.** Every in-bucket row has a parseable 경도/위도 inside
  a generous box of the city (extent lat 35.156-35.381, lon 128.707-129.003).
  222 points lie more than 15 km from the city's median point, which is the
  city's own size (one district of about 460 km²), not a defect. The
  businesses are the register's own rows for the city, as in every built
  SEMAS city; step 1's boundary decides only the station scope.
- **Left out by the taxonomy's 소분류 overrides**: 구내식당 155, 일반 유흥
  주점 503, 무도 유흥 주점 9, 가정용 연료 소매업 89.
- **Config:** `SEMAS_SIDO = "경상남도"` and the code `48250`, through the
  `sigungu_codes` argument Gwangju's brief recommends adding to
  `korea_sbiz.storefronts()` (with `시군구코드` added to `READ`; land it once,
  in whichever Korean city is built first, and drift-check the ten built
  SEMAS cities). The prefix `("김해시",)` gives the same rows today.
- **Busan's business source is different** (the city's own permit API
  through Daegu's module), so Gimhae's page stands alone and never sums
  with Busan's counts.

### Privacy

- **Run `python scripts/check_personal_exposure.py gimhae`** after step 2;
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
  Gimhae exactly as they cover Incheon. No new license read.
- **Notice 68 names its cities.** Add Gimhae to its heading in
  `docs/data_sources.md` and to the `Notice(68, ...)` title and text in
  `app/components.py`, reusing the displayed wording unchanged otherwise:
  > Storefronts for ... are from the Small Enterprise and Market Service's
  > commercial-district register (소상공인시장진흥공단, 상가(상권)정보, via
  > 공공데이터포털 data.go.kr), 이용허락범위 제한 없음. Changes: filtered to
  > shops, food and drink and personal services, grouped into three
  > categories, and mapped by distance to stations; the categories and counts
  > are this project's, not SEMAS's. Not produced or endorsed by SEMAS.
- **A row in `docs/data_sources/south-korea.md`**, Goyang's shape (경상남도's
  member, code 48250, the counts, the withheld names). The `app/` change
  waits for review time.

---

## Rail leg - the Busan–Gimhae LRT

| | |
|---|---|
| **System** | The Busan–Gimhae LRT (부산김해경전철), driverless, grade-separated, mostly elevated; 21 stations, 사상 (Busan) to 가야대 (Gimhae). Mode **light rail** |
| **Stations in Gimhae** | **12**: 불암, 지내, 김해대학, 인제대, 김해시청, 부원, 봉황, 수로왕릉, 박물관, 연지공원, 장신대, 가야대. Busan's committed `outputs/busan/excluded_stations.csv` lists exactly these 12 as "outside Busan's boundary" |
| **Out of scope** | **The 9 in Busan**: 사상, 괘법르네시떼, 서부산유통지구, 공항, 덕두, 등구, 대저, 평강, 대사. They go in Gimhae's `excluded_stations.csv` as outside Gimhae's boundary; Busan's page already counts them |
| **Headways** | The operator's timetable for 부원 (`bglrt.com/00011/00149.web?scode=915`): weekdays every 5-6 min all day 07-21 (longest gap 6), Saturdays and holidays 6-7 min; 197 weekday trains each way; service 05:11-00:09 (first and last trains, `bglrt.com/00014/00161/00364.web`) |
| **Light-rail test** | Passes: purpose-built elevated track, frequency far inside 15 min, median nearest-stop spacing **729 m** inside Gimhae (minimum 595), above the 550 m guide. Precedent: Busan draws it |
| **Not drawn** | Busan Lines 2 and 3, which meet the LRT at 사상 and 대저 in Busan: no station in Gimhae. Korail (진영, the 경전선): intercity, as everywhere in Korea |
| **Gate 3** | The whole line, 21 stations, termini to termini: the operator's station list (21 names on the 부원 page) and Busan's `LINE_STATION_COUNTS` agree |

- **Drawn as Busan's map draws it** (`pipeline/busan/config.py`): matched on
  the relation's route type `light_rail` and `ref` **`BGL`**, color
  **`#8652A1`**, public name **"Busan–Gimhae LRT"** (with the en dash), to
  both ends. Labeled on the map and in the legend.
- **Rail from OpenStreetMap**, as Busan, Incheon and the Gyeonggi cities:
  no Korean agency publishes GTFS. Follow `osm-rail`: one Overpass query for
  the city, the boundary relation fetched by id and area-gated, through
  `pipeline/osm.py`. The BGL relation sits in Busan's cached
  `data/busan/raw/osm_rail_routes.json`, but **Gimhae fetches its own** (one
  query per city; every worktree shares one `data/` folder, so Busan's
  cache is read, never rewritten, by another city's build).
  **One query in flight per session**; after a 504 or 429 wait at least
  60 s. Staging made no Overpass query.
- **Boundary:** 김해시, admin_level 6 in 경상남도 (KR-48), resolved by name at
  the build. About 463 km² (general knowledge): set `BOUNDARY_AREA_KM2` from
  the fetched polygon.
- **Query box** (Gimhae plus about 2 km, taken east to 사상 so the whole
  line arrives): `OSM_BBOX = (35.13, 128.68, 35.41, 129.03)`.
- **Rings** by the spacing rule: 729 m median, so standard rings.
- **English names** from `name:en` first (`cjk-text`); Busan's excluded list
  already carries English names for the 12 (Buram ... Kaya University), a
  cross-check, never a source.

---

## Scope, CRS, region

- **Scope:** Gimhae City (김해시), its OSM boundary.
- **CRS:** UTM 52N, **EPSG:32652** (longitude 128.889 falls in the
  126-132 band; checked below). Never buffer in EPSG:4326.
- **Region:** `"East Asia"`. Gimhae's dot sits about 17 km from Busan's,
  whose label was moved to the lower left on 2026-09-28 after its pill
  covered Fukuoka's marker. Run `check_macro_labels.py` at 375, 768 and 1200 and set
  Gimhae's `label_offset` from the result, moving no built label unless the
  check leaves no choice.
- **Scaffold:** `scaffold_city.py --slug gimhae --name Gimhae
  --system-name "Busan–Gimhae LRT" --taxonomy korea_sbiz --lat 35.228
  --lon 128.889 --region "East Asia" --country "South Korea"
  --mode light_rail --page-number 192` (`--dry-run`
  first). No new notice number: the Small Enterprise and Market Service's notice 68 extends.

## Owner calls

- **Made:** Band A on SEMAS, and **its own page** (owner, 2026-10-03); the
  SEMAS taxonomy and license position (owner, 2026-09-29, for every SEMAS
  city); the LRT drawn as Busan draws it (owner, 2026-09-27, Busan's
  calls); Korean rail from OSM.
- **Open:** none beyond the build's own gates (gate 3, the light-rail test
  re-measured at step 1, privacy, provenance, scope disclosure,
  `publish-city`). Busan's page is not touched. A page sentence no template
  covers (for example, that the line's other nine stations are on Busan's
  map) is a proposal in the drafts file, and does not stop the build.

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
  it reaches social posts is open." Gimhae inherits it, so it stays off
  cards and public pieces until the owner rules on SEMAS.

## What the build must still measure

- The withheld-name count and the privacy verdict.
- The boundary relation's id and area; the 12 stations by route membership
  and the median spacing again (729 m at the screen).
- The share of storefronts in a ring.

```brief-checks
[
  {
    "id": "gimhae-semas-dataset-page",
    "claim": "SEMAS's 상가(상권)정보 is still published on data.go.kr (15083033), quarterly, declared 이용허락범위 제한 없음",
    "kind": "http_contains",
    "url": "https://www.data.go.kr/data/15083033/fileData.do",
    "present": ["상가(상권)정보", "소상공인시장진흥공단", "이용허락범위", "제한 없음", "분기"]
  },
  {
    "id": "gimhae-bgl-operator-station-page",
    "claim": "The operator's station page for 부원 (the headway source) still lists the line from 사상 to 가야대, through 불암",
    "kind": "http_contains",
    "url": "https://www.bglrt.com/00011/00149.web?scode=915",
    "present": ["사상", "불암", "부원", "가야대"]
  },
  {
    "id": "gimhae-bgl-first-last-trains",
    "claim": "The operator's first- and last-train page for the line is still published",
    "kind": "http_contains",
    "url": "https://www.bglrt.com/00014/00161/00364.web",
    "present": ["첫차", "막차", "가야대", "사상"]
  },
  {
    "id": "gimhae-busan-excluded-lrt-stations",
    "claim": "Busan's committed map excludes exactly 12 Busan-Gimhae LRT stations as outside Busan: the 12 this page draws",
    "kind": "row_count",
    "path": "outputs/busan/excluded_stations.csv",
    "column": "lines",
    "equals": "Busan–Gimhae LRT",
    "expect": 12
  },
  {
    "id": "gimhae-projected-crs",
    "claim": "Gimhae's derived UTM zone is 52N (EPSG:32652)",
    "kind": "utm_zone_from_longitude",
    "lon": 128.889,
    "expect": "EPSG:32652"
  }
]
```
