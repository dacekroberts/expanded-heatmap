# Seoul (Regional) - build brief

**A regional extension of a built page, marked by the owner on 2026-10-04**
(`docs/city_master_list.md`, "Add-ons to built cities", "Potential Korean
regional expansions": "Seoul (Regional) + Gwacheon (Line 4, 5 stations),
Gwangmyeong (Line 7, 2), Hanam (Line 5, 4) and Guri (Line 8, 4): left out as
standalone pages on the owner's Gyeonggi scope"). Released for briefing on
2026-10-06; **the build stays paused** until the owner schedules it. Brief
written 2026-10-06 by staging from cached files only (nothing downloaded, no
Overpass query). Run `python scripts/brief_check.py seoul_regional` before
writing any code.

Read `regional-extension` (the steps this brief follows), `multi-source-city`
(two registers on one page, Los Angeles + Long Beach's shape), `korea-city`
(the SEMAS module, the name rule, notice 68 and the Visuals hold) and
`cjk-text`; then Seoul's, Gyeonggi's and Gimpo's briefs
(`docs/build_briefs/seoul.md`, `gyeonggi.md`, `gimpo.md`).

---

## The one-line summary

**Seoul keeps its LOCALDATA permit registers; Gwacheon, Gwangmyeong, Hanam
and Guri join on SEMAS's national storefront file, cut by 시군구코드: 22,676
storefronts and 16 stations on lines Seoul already draws (the master list
says 15: Gwangmyeong has a third, the Line 1 shuttle's terminus). Two
registers that count Retail differently meet at the city line (SEMAS lists
about twice the retail Seoul's permits do), and Seoul would take on SEMAS's
notice 68 and with it the Visuals card hold. Three owner calls before the
build.**

---

## Step 0 - is it an extension? (`regional-extension` Step 0)

1. **Lines already drawn: yes.** Every added station is on a line Seoul's
   map draws (Line 1, 4, 5, 7, 8, the Gyeongui–Jungang and Gyeongchun Lines);
   each is in Seoul's committed `outputs/seoul/excluded_stations.csv` today.
2. **No bucket at a few stations only: yes.** SEMAS gives the four all three
   buckets.
3. **Station counts:** 2 to 5 per municipality, add-on counts, not page
   counts; the owner's Gyeonggi scope gave these 시 no page of their own
   (`gyeonggi.md`, "Left out, with the reason").
4. **Terms: accepted.** SEMAS's position is the owner's (2026-09-29), for
   every SEMAS city.
5. **Extension, not a page: the owner's mark** (2026-10-04).

## What joins - stations, measured from cached files

Each station in Seoul's committed excluded list was placed in a 시군구 by the
시군구코드 of the SEMAS storefronts within 300 m of it (the cached 2026-06-30
edition; every one of the 16 came back one code at a share of 1.00). The
build places them by the OSM boundaries; a station that lands elsewhere is a
brief to correct.

| 시 | Code | Stations (Seoul's English names) | Lines | Master list |
|---|---|---|---|---|
| 과천 Gwacheon | 41290 | Seonbawi, Seoul Racecourse Park, Seoul Grand Park, Gwacheon, Government Complex Gwacheon (**5**) | Line 4 | 5 |
| 광명 Gwangmyeong | 41210 | Cheolsan, Gwangmyeongsageori (Line 7); **Gwangmyeong** (Line 1, the 광명셔틀 shuttle's terminus at the KTX station) (**3**) | Line 7, Line 1 | **2** (call 3) |
| 하남 Hanam | 41450 | Misa, 하남풍산 (Hanam Pungsan), Hanam City Hall (Deokpung·Sinjang), Hanam Geomdansan (**4**) | Line 5 | 4 |
| 구리 Guri | 41310 | Jangja Lake Park, Guri, Donggureung (Line 8; Guri shared with the Gyeongui–Jungang Line); Galmae (Gyeongchun Line) (**4**) | Line 8, Gyeongui–Jungang, Gyeongchun | 4 ("Line 8") |

- **Seoul's page: 308 stations kept, 227 listed outside; regional: 324 kept,
  211 listed** (Seoul's `baseline.json`: `stations_kept` 308,
  `stations_outside` 227).
- **The 광명셔틀 is drawn by Seoul today**: two `ref=1` relations named
  "수도권 전철 1호선 광명셔틀" (광명 ↔ 영등포, 7 stops each) are in Seoul's
  cached `data/seoul/raw/osm_rail_routes.json` (OSM base 2026-09-25), so
  route membership keeps Gwangmyeong station once Gwangmyeong is in scope.
- **하남풍산 has no English name** in Seoul's output (the only Korean label in
  the 16): take the station object's `name:en` first, else
  `OSM_NAME_EN_OVERRIDES` to the operator's signed form (Siheung's 달월 and
  시흥능곡 lesson).
- **Headways at the added stations are unread.** The Line 5 Hanam branch,
  the Line 1 shuttle and the Gyeongchun Line at Galmae each need a midday
  read from Seoul Metro's or Korail's timetables (Gimpo's source,
  `seoulmetro.co.kr` cyber-station pages). A wait beyond 15 minutes on a
  line already drawn is stated on the page, Namyangju's Gyeongchun precedent
  (DECISIONS.md, "Namyangju's Gyeongchun Line stays drawn").

## Business leg - two registers, disjoint by municipality

### Seoul: unchanged

Seoul's seventeen LOCALDATA `인허가 정보` files and its own step 2
(`pipeline/seoul/step2_clean_businesses.py`), **239,410 premises** (Food
service 148,256, Retail 51,663, Personal services 39,491; `baseline.json`).
Nothing in Seoul's leg changes; with `REGIONAL = False` it reproduces byte
for byte.

### The four 시: SEMAS 상가(상권)정보 (data.go.kr 15083033)

The national cache `data/korea/raw/sbiz_15083033.zip` (352.7 MB, edition
**2026-06-30**, the edition every SEMAS city uses), member 시도명 **경기도**
(672,680 rows, 47 code/name pairs), read through
`pipeline/countries/korea_sbiz.py`'s `storefronts("경기도", None,
sigungu_codes=(...))` and classified by `pipeline/taxonomies/korea_sbiz.py`.

**Measured 2026-10-06** (staging, `heavy_job.py` label `korea-ext-measure`,
measured peak 0.99 GB for six province members in turn): no duplicate
상가업소번호, **no 중분류 or 소분류 unknown to the taxonomy**, every in-bucket
row with a point.

| 시 | 시군구코드 | Rows | Food service | Retail | Personal services | **In-bucket** | Names withheld |
|---|---|---|---|---|---|---|---|
| 과천 Gwacheon | 41290 | 2,931 | 742 | 657 | 176 | **1,575** | 0 |
| 광명 Gwangmyeong | 41210 | 12,547 | 2,968 | 2,829 | 1,060 | **6,857** | 2 |
| 하남 Hanam | 41450 | 16,977 | 3,555 | 3,633 | 1,208 | **8,396** | 9 |
| 구리 Guri | 41310 | 11,452 | 2,484 | 2,509 | 855 | **5,848** | 9 |
| **Four** | | **43,907** | **9,749** | **9,628** | **3,299** | **22,676** | **20** |

- **Code and name agree**, gimpo.md's test: each code carries exactly one
  시군구명 (과천시, 광명시, 하남시, 구리시), each name prefix exactly one code,
  and the prefix and the code pick identical rows. Configure on codes only:
  `SEMAS_SIGUNGU = None`, `SEMAS_SIGUNGU_CODES = ("41290", "41210", "41450",
  "41310")`; `storefronts()` exits on an unknown code.
- **Left out by the taxonomy's 소분류 overrides**: 일반 유흥 주점 377 (Gwangmyeong
  155, Hanam 45, Guri 177), 구내식당 56 (Gwacheon 17, Gwangmyeong 19, Hanam 11, Guri 9), 가정용 연료 소매업 29
  (Gwangmyeong 8, Hanam 14, Guri 7), 무도 유흥 주점 8 (Gwangmyeong 2, Hanam 2, Guri 4).
- **Extents** (in-bucket points): Gwacheon lat 37.404-37.464, lon
  126.973-127.035; Gwangmyeong 37.402-37.493, 126.831-126.899; Hanam
  37.474-37.580, **127.140-127.277**; Guri 37.560-37.644, 127.107-127.166.
  **Hanam passes Seoul's box** (`OSM_BBOX` east edge 127.20, and `SEOUL_BBOX`
  is derived from it): widen the sanity box under `REGIONAL`, not the city's
  fetch box (Belo Horizonte's `_SANITY`, `pipeline/belo_horizonte/config.py`
  line 55), or apply it to the LOCALDATA rows only.

### Ring shares (0.6 mi, measured on the stations above)

| 시 | To its own stations | To any station on the regional page |
|---|---|---|
| Gwacheon | 69.1% (1,088) | **69.5%** (1,095 of 1,575) |
| Gwangmyeong | 59.0% (4,049) | **68.0%** (4,662 of 6,857); **52.1%** (3,570) without Gwangmyeong station |
| Hanam | 66.9% (5,614) | **70.0%** (5,876 of 8,396) |
| Guri | 87.4% (5,110) | **87.4%** (5,111 of 5,848) |
| **Four** | | **73.8%** (16,744 of 22,676) |

### The join: no cross-source de-duplication, and the Retail step

- **Disjoint by construction.** Seoul's LOCALDATA files are Seoul's 25 구'
  permits; the SEMAS rows are cut to four codes outside Seoul. A premises
  cannot be in both unless a point stands in the other municipality.
  Measured proxy: **0 of Seoul's 239,410 premises** have their nearest SEMAS
  storefront both within 50 m and under one of the four codes.
  Record "no cross-source dedup" in the drafts file, since a missing step
  looks like a forgotten one (Vancouver's precedent, `regional-extension`
  Step 2). Dedup stays per source.
- 🚨 **The two registers count Retail differently.** Seoul's whole SEMAS
  member, classified by the same `korea_sbiz` taxonomy, against Seoul's
  LOCALDATA premises:

  | Bucket | Seoul, LOCALDATA (the page) | Seoul, SEMAS (not used) | Ratio |
  |---|---|---|---|
  | Food service | 148,256 | 137,743 | 0.93 |
  | Retail | 51,663 | **111,069** | **2.15** |
  | Personal services | 39,491 | 39,053 | 0.99 |

  Food and personal services agree within 7%; **SEMAS lists about twice the
  retail**, because Korea licenses food and tobacco retail, not retail in
  general (Seoul's own What Is Excluded section says so). On one page the
  Retail heat steps up at Seoul's boundary. `korea-city` trap 4 ("SEMAS and
  LOCALDATA counts never compare or sum") is the rule this page would
  break; call 1.
- **Taxonomy dispatch on `source`**, Los Angeles' pattern
  (`TAXONOMY_SYSTEM = "los_angeles" if REGIONAL else "naics"`,
  `pipeline/los_angeles/config.py` line 172): a module that routes
  LOCALDATA rows to `korea_localdata` and SEMAS rows to `korea_sbiz`, Seoul's
  rows classifying exactly as before. Busan (Regional) and Daegu (Regional)
  have the same shape, so one shared Korean dispatching module serves all
  three *(recommendation to the build session; the first of the three
  writes it)*.

## Licenses and notices - all already recorded, no new verdict

- **Seoul**: KOGL Type 1, notice 18, Seoul Metropolitan Government
  (`docs/data_sources.md` line 1113; `docs/data_sources/south-korea.md`
  line 80). Unchanged.
- **SEMAS**: PERMITTED WITH CONDITIONS, 이용허락범위 제한 없음, notice 68,
  Small Enterprise and Market Service
  (`docs/data_sources.md` line 2246; the owner's reasoned position,
  2026-09-29). Nothing is per-province or per-city, so no new read
  (`gimpo.md`, "License").
- **The Small Enterprise and Market Service notice (68) names its cities**:
  its heading in `docs/data_sources.md` and its title and text in
  `app/components.py` (line 2495)
  gain the four 시 on Seoul (Regional)'s page, wording otherwise unchanged.
  Naming four municipalities inside a city entry is a sentence no template
  covers: a drafts-file proposal.
- Notice 1, OpenStreetMap, gains the four boundaries.
- **A row per source in `docs/data_sources/south-korea.md`**: the four 시 in
  the SEMAS registry table (Goyang's shape, the codes, counts and withheld
  names), and the four boundary relations in the boundary table.
- ⚠️ **The Visuals hold reaches Seoul.** The Visuals registry holds every
  notice-68 city off cards and public pieces automatically while whether
  SEMAS's permission reaches social posts is open (DECISIONS.md, "Daejeon
  built", Downstream; `gimpo.md`, Downstream). Seoul carries no notice 68
  today; Seoul (Regional) would. Call 2.

## Privacy

- SEMAS has **no operator or phone column**: the cached file's header
  (39 columns, read 2026-10-06) carries 상호명 and 지점명 (trade and branch
  names), classification, administrative codes, addresses, 동/층/호 unit
  fields and the point; `korea_sbiz.READ` loads 13 of them and none of the
  unit fields. Seoul's LOCALDATA files have no operator field either; their
  telephone column is never read.
- **Names withheld by the Korean name rule** (`pipeline/korean_names.py`):
  20 in the four, measured; Seoul's 138 unchanged.
- **Run `python scripts/check_personal_exposure.py seoul`** on the regional
  file (the `korean=True` entry reads `businesses_clean.csv`; point it at
  `processed/regional/` while the switch is on) and record the verdict in the
  drafts file and `docs/privacy_verdicts.md`.

## Rail and scope

- **Rail from OpenStreetMap, as Seoul's.** No line is added; the four only
  change which stations are in scope. **One Overpass query for the four
  boundary relations** (과천시, 광명시, 하남시, 구리시, admin_level 6 in KR-41,
  resolved by name at the build, area-gated from the fetched polygons:
  about 36, 39, 93 and 33 km² by general knowledge). One query in flight per
  session; after a 504 or 429 wait at least 60 s.
- **New file names for every regional fetch** (`osm_boundary_regional.json`
  or similar): `data/` is one junction shared by every worktree, and Seoul's
  `osm_boundary.json` and rail cache must stay as they are for `REGIONAL =
  False` to reproduce Seoul.
- **Scope**: Seoul's relation 2297418 plus the four, stations inside the
  union. **CRS** UTM 52N, EPSG:32652 (Hanam's eastern edge, 127.277, stays in
  the 126-132 band). **Rings** standard, as Seoul's.

## Steps, in order

1. **The city alone at zero drift.** Add `REGIONAL = False` to
   `pipeline/seoul/config.py` (`NAME`, `DATA_PROCESSED` to
   `data/seoul/processed/regional/` and `TAXONOMY_SYSTEM` following it, Los
   Angeles' and Belo Horizonte's configs), commit it off, run
   `python scripts/heavy_job.py run --label "seoul drift" ... --
   python pipeline/drift_check.py seoul`: no drift, then
   `git checkout -- outputs/` if files show modified.
2. **Fetch** the four boundaries (`pipeline/seoul/fetch_sources.py`, under
   new names). The SEMAS file is cached; nothing else to download.
3. **Switch on**: steps 1-3 with `REGIONAL = True`; the drift check reports
   only the extension's changes (stations 308 → 324, the SEMAS rows, the
   ring counts); re-record the baseline deliberately.
4. **Page**: the same page file and slug (`app/pages/43_Seoul_Heatmap.py`);
   the name becomes **"Seoul (Regional)"** in `app/cities.py` and the
   config's `NAME`; `blurb`, `data_age` (LOCALDATA's fetch date and SEMAS's
   2026-06-30 edition); macro label re-scored at 375, 768 and 1200. Text in
   `docs/city_page_format.md`'s format; the two-source sentence is a drafts
   proposal.
5. **What Is Excluded**: rename Seoul's section to "Seoul (Regional)" and add
   one for the four (Daejeon's shape: Out by name counts above, Names
   withheld 20, a **Stations.** line naming the 16); 211 stations stay
   listed outside. `docs/map_inconsistencies.md`: the Retail step at the
   boundary, and theme 5's "(Regional)" list.
6. **Gates**: `check_personal_exposure.py seoul`, `check_provenance.py`,
   `check_scope_disclosure.py`, `check_ring_shares.py --write` (Seoul's row
   only), `check_deploy_imports.py`. Land at review time only; **reboot:
   yes** (`app/cities.py` changes); deploy-verify `city-added`.

## Owner calls - open, each with a recommendation

1. **Two registers on one page, with a Retail step at the city line.**
   *Recommend:* build as marked (LOCALDATA for Seoul, SEMAS for the four),
   with the step stated on the page, in What Is Excluded and in
   `docs/map_inconsistencies.md`, and the page's counts given per source,
   never as one comparable total. *Tradeoff:* the heatmap shows about twice
   the retail per comparable street outside Seoul, which a reader may take
   as real, and it departs from trap 4. *Alternatives:* (a) narrow the four's
   Retail to the 소분류 matching Seoul's licensed trades (a taxonomy branch,
   unmeasured, and a departure from the owner's 2026-09-29 SEMAS scope); (b)
   leave the four unbuilt.
2. **The Visuals hold.** Seoul (Regional) carries notice 68, so the Visuals
   registry holds Seoul off cards and public pieces automatically.
   *Recommend:* rule on SEMAS's social-post scope before this lands, and
   build behind the switch meanwhile. *Tradeoff:* landing first takes Seoul
   off every card until the ruling; ruling first delays the extension.
3. **Gwangmyeong station, the Line 1 shuttle's terminus.** *Recommend:* keep
   it (Seoul draws the shuttle today, and the station rule is route
   membership inside the scope), read its midday service at the build and
   state the wait on the page if beyond 15 minutes. *Tradeoff:* it rings
   1,092 of Gwangmyeong's storefronts (68.0% in a ring with it, 52.1%
   without) around a station whose service may be thin; dropping it is a
   station rule Seoul does not have.

## What the build must still measure

- The four boundary relations' ids and areas; the 16 stations by route
  membership inside them (16 here by the storefront-code proxy).
- LOCALDATA premises inside the four polygons and SEMAS rows inside Seoul's
  (0 here by the 50 m proxy, which is not a polygon test).
- The midday headways at the added stations (calls 3 and the Line 5 branch).
- The withheld count and privacy verdict on the regional file; ring shares
  on step 1's stations.

```brief-checks
[
  {"id": "seoul-regional-excluded-total", "claim": "Seoul's committed map lists 227 stations of drawn lines outside Seoul, the list the 16 added stations were taken from", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "expect": 227},
  {"id": "seoul-regional-line5-hanam", "claim": "Exactly 4 Line 5 stations lie outside Seoul, all four in Hanam", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "lines", "equals": "Line 5", "expect": 4},
  {"id": "seoul-regional-gwacheon-1", "claim": "Seonbawi (Gwacheon) is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Seonbawi", "expect": 1},
  {"id": "seoul-regional-gwacheon-2", "claim": "Seoul Racecourse Park (Gwacheon) is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Seoul Racecourse Park", "expect": 1},
  {"id": "seoul-regional-gwacheon-3", "claim": "Seoul Grand Park (Gwacheon) is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Seoul Grand Park", "expect": 1},
  {"id": "seoul-regional-gwacheon-4", "claim": "Gwacheon station is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Gwacheon", "expect": 1},
  {"id": "seoul-regional-gwacheon-5", "claim": "Government Complex Gwacheon is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Government Complex Gwacheon", "expect": 1},
  {"id": "seoul-regional-gwangmyeong-1", "claim": "Cheolsan (Gwangmyeong, Line 7) is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Cheolsan", "expect": 1},
  {"id": "seoul-regional-gwangmyeong-2", "claim": "Gwangmyeongsageori (Gwangmyeong, Line 7) is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Gwangmyeongsageori", "expect": 1},
  {"id": "seoul-regional-gwangmyeong-shuttle", "claim": "Gwangmyeong station, the Line 1 shuttle's terminus, is on Seoul's drawn Line 1 and outside Seoul (call 3)", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Gwangmyeong", "expect": 1},
  {"id": "seoul-regional-hanam-1", "claim": "Misa (Hanam) is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Misa", "expect": 1},
  {"id": "seoul-regional-hanam-2", "claim": "하남풍산 (Hanam) is outside Seoul's map today, with no English name", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "하남풍산", "expect": 1},
  {"id": "seoul-regional-hanam-3", "claim": "Hanam City Hall is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Hanam City Hall (Deokpung·Sinjang)", "expect": 1},
  {"id": "seoul-regional-hanam-4", "claim": "Hanam Geomdansan is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Hanam Geomdansan", "expect": 1},
  {"id": "seoul-regional-guri-1", "claim": "Jangja Lake Park (Guri, Line 8) is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Jangja Lake Park", "expect": 1},
  {"id": "seoul-regional-guri-2", "claim": "Guri (Line 8 and the Gyeongui-Jungang Line) is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Guri", "expect": 1},
  {"id": "seoul-regional-guri-3", "claim": "Donggureung (Guri, Line 8) is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Donggureung", "expect": 1},
  {"id": "seoul-regional-guri-4", "claim": "Galmae (Guri, Gyeongchun Line) is outside Seoul's map today", "kind": "row_count", "path": "outputs/seoul/excluded_stations.csv", "column": "station", "equals": "Galmae", "expect": 1},
  {"id": "seoul-regional-projected-crs", "claim": "Seoul (Regional) projects to UTM 52N, Hanam's eastern edge included", "kind": "utm_zone_from_longitude", "lon": 127.277, "expect": "EPSG:32652"}
]
```
