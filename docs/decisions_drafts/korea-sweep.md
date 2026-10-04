# DECISIONS drafts - Korea sweep (`korea-sweep-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-10-04 - A South Korea view on the macro map: Daegu, Busan, Daejeon, Gwangju and Gimhae (owner)

- **The problem, measured**: with the three new cities in East Asia,
  `check_macro_labels.py` reported 54 problems at 375, 768 and 1200: Busan's
  and Gimhae's dots 2.6 px apart, Daejeon's pill over every Seoul Capital Area
  dot, Daegu's pill over Daejeon's dot, Gwangju's and Gimhae's pills
  overlapping. No offset separates two dots 2.6 px apart.
- **The recommendation**, on Japan's precedent (2026-10-02, Osaka's and
  Sakai's dots 2.6 px apart in one view): a country view holding Daegu, Busan
  and the three new cities, the three on the minor label tier, East Asia
  still labelling Daegu and Busan through `REGION_LABELS_ALSO`. Scored in a
  throwaway edit first: **PROBLEMS 0** in all 20 regions at the three widths,
  every label at its default offset, no built label moved.
- **The owner: "New view (Recommended)"**, named **"South Korea"** (chosen over
  "Korea South" and "Southern Korea", knowing Seoul and its satellites keep
  their own view). Built as recommended: `REGION_ORDER` after the Seoul
  Capital Area, `COUNTRY_VIEWS`, `REGION_LABELS_ALSO["East Asia"]`,
  `country_sections.REGION_GROUP` (grouped under East Asia), and Daegu's and
  Busan's `region`. The master list's Built table gains a "South Korea view"
  row.
- **Label widths** (canvas `measureText` after `document.fonts.load`, 600 14px
  Space Grotesk, 2026-10-04): Daejeon 54.4, Gwangju 58.2, Gimhae 49.5;
  controls Goyang 52.1, Uijeongbu 68.6, Anyang 51.6, Busan 41.9 and Daegu 42.9
  reproduced to 0.1 px.
- **Downstream**: Daegu and Busan change region, which moves them in the
  macro map's region menu and its city list; the Visuals session should hear
  it with the landing.

### 2026-10-04 - Gimhae built: the Busan–Gimhae LRT on SEMAS's register, its own page

**Built** on branch `korea-sweep-build`, page 192, region East Asia, from
Daejeon's files (Incheon's module); its own page, not a Busan regional map
(owner, 2026-10-03). Downloads and page prose under the owner's pre-approval
(2026-09-30); the page is Bucheon's and Incheon's approved text with Gimhae's
line. **17,879 storefronts** (food service 8,558, retail 6,662, personal
services 2,659), exactly the brief's, from 26,700 SEMAS rows under 48250;
**6,736 within the rings (37.7%)**. **12 stations** inside Gimhae, a 729 m
median gap (minimum 596 m, Gimhae City Hall / Buwon), the brief's figure:
standard rings. `mode` light_rail (the brief's, for the owner's approval with
the build), `rail_extra` "—" (a grade-separated driverless light metro, as
Busan, Uijeongbu and Yongin record theirs), `coverage` full, `categories`
"All three".

- **The LRT drawn as Busan draws it**: `ref=BGL`, light_rail, #8652A1,
  "Busan–Gimhae LRT", to both ends; Gimhae's own Overpass query (one, first
  try), Busan's cache never read. Busan Lines 2 and 3 reach the box with no
  station in Gimhae: placed as not drawn.
- **Gate 3 exact** on the whole line (21, the operator's station list and
  Busan's `LINE_STATION_COUNTS`). The 12 inside Gimhae are **the same 12
  names** Busan's committed `excluded_stations.csv` lists as outside Busan;
  Gimhae's lists Busan's 9 as outside Gimhae.
- **The light-rail test passes**, re-measured: 729 m median spacing, every
  5-6 minutes all day (the operator's 부원 timetable, the brief).
- **Boundary**: OSM relation 7224485 (김해시, admin_level 6), **460 km²**,
  gated at 450-470.
- **Line color**: #8652A1, Delta-E 33.8 from Retail, kept as Busan's.
- **Personal exposure: PASS.** 0 of 17,879 rows show a Korean personal name
  at a residential address; 12 withheld by step 2 (5 of them in-ring pins).
- **Licence**: notice 68 and notice 1 gain Gimhae; no new notice.
- **Page prose proposal**: "Not drawn: Korail's intercity line. No other rail
  line has a station in the city." (Uijeongbu's "No other rail line" sentence
  with Korail named.)
- **Downstream**: notice 68 a caption, notice 1 rail, boundary and names;
  the known SEMAS card hold applies (notice 68 only).
- **Master list**: Gimhae's Band A row marked built; South Korea has no
  candidate left.

### 2026-10-04 - Gwangju built: Gwangju Metro Line 1 on SEMAS's register, the merged member's codes and a five-district boundary

**Built** on branch `korea-sweep-build`, page 191, region East Asia, from
Daejeon's files (Incheon's module). Downloads and page prose under the owner's
pre-approval (2026-09-30); the page is Bucheon's approved text with Gwangju's
line, and three proposal sentences (below). **47,214 storefronts** (food
service 20,701, retail 18,706, personal services 7,807), exactly the brief's,
from 75,324 rows in the five codes of the member 전남광주통합특별시;
**14,077 within the rings (29.8%)**. **20 stations** on Line 1, every one
inside the city, a 770 m median gap (minimum 535 m, Geumnamno 4-ga / 5-ga):
standard rings. `coverage` full, `categories` "All three", `mode` metro.

- **Step 2 keys on 시군구코드** 12210, 12240, 12270, 12300 and 12330 inside
  the member 전남광주통합특별시 (owner, 2026-10-03: codes, never names).
- **Boundary: the union of the five 구 relations** (4162635 동구, 7348759 서구,
  7348741 남구, 7348583 북구, 7348758 광산구; admin_level 6), each taken by
  id, checked by name and required to lie inside the city's query box:
  **500 km²**, gated at 490-510 (the brief expected about 501). The one
  query asked for any relation named 광주광역시 at any level and returned
  none: after the 2026 merger OSM no longer holds the city's own relation.
  This is the brief's prescribed fallback, not a new call.
- **Rail: one Overpass query**, answered first try. Line 1's two direction
  relations (`ref=1`, subway, #009088); **Line 2's two circle relations**
  (`ref=2`, light_rail, 36 planned stops each) **placed as not drawn**, under
  construction (phase 1 reported for 2028-12). Gate 3 exact: 20 against the
  operator's 운행현황 (역수 20개역), a primary source. 광주송정 is the Line 1
  stop (route membership).
- **One English name overridden**: OSM's "Geumnamro 5-ga" for 금남로5가 to
  "Geumnamno 5-ga", matching OSM's own 금남로4가 ("Geumnamno 4(sa)-ga") and the
  operator's English station list (Geumnamno5-ga); the operator's English
  timetable page itself writes "Geumnamro 5 Ga", so the operator is
  inconsistent. Ansan's override mechanism, copied into Gwangju's step 1.
- **녹동 (Nokdong) kept** as a station of the drawn metro line (the brief's
  recommendation; the 15-minute test is light rail's). The operator's
  녹동행 page gives first and last trains only (녹동 06:14-22:17 toward 평동,
  the same span as 소태), and its 운행현황 page gives 소태-평동 33 minutes and
  녹동-평동 38 minutes with separate 소태행 and 녹동행 tables; the per-station
  timetables load only through the site's route finder, so 녹동's daily count
  was **not read**. Recorded as unmeasured, not as a pass.
- **Line color**: #009088, Delta-E 28.6 from Personal services, kept as
  Daejeon's.
- **Personal exposure: PASS.** 0 of 47,214 rows show a Korean personal name
  at a residential address; 82 withheld by step 2 (8 of them in-ring pins).
- **Licence**: notice 68 and notice 1 gain Gwangju; no new notice.
- **Page prose proposals** (not covered by the template): "Most trains turn
  back at Sotae, one stop short of Nokdong."; "Not drawn: Line 2, still under
  construction, and Korail's intercity lines."; "The whole city is included:
  its five districts, which since 2026 sit within the merged
  전남광주통합특별시."
- **Downstream**: notice 68 a caption, notice 1 rail, boundary and names;
  the known SEMAS card hold applies (notice 68 only).

### 2026-10-04 - Daejeon built: Daejeon Metro Line 1 on SEMAS's register

**Built** on branch `korea-sweep-build` (cut from `origin/master` at
`fafec401`), page 190, region East Asia, from Incheon's files
(`docs/handoff_korea_sweep_2026-10-03.md`; Band A, owner 2026-10-03).
Downloads and page prose under the owner's pre-approval (2026-09-30); the page
is Bucheon's approved text with Daejeon's line. **50,939 storefronts** (food
service 23,402, retail 20,100, personal services 7,437), exactly the brief's,
from 80,704 SEMAS rows in the five 시군구코드 (the whole 대전광역시 member);
**21,252 within the rings (41.7%)**. **22 stations** on Line 1, every one
inside the city, an 846 m median gap (minimum 626 m, City Hall / Tanbang):
standard rings. `coverage` full, `categories` "All three", `mode` metro,
`rail_extra` "—", as the built SEMAS cities.

- **Step 2 keys on 시군구코드** (30110, 30140, 30170, 30200, 30230) through the
  new `sigungu_codes` argument; on this edition the codes select the whole
  member, so a sixth district or a merger stops the step instead of widening
  the page.
- **Rail: one Overpass query for the city** (routes, station names and
  boundary together, split by `fetch_sources.py` into Incheon's three files;
  osm-rail's one-query rule), answered first try by overpass-api.de. Line 1's
  two direction relations (`ref=1`, route=subway); **Line 2's relation**
  (`ref=2`, route=tram, no stop members) **placed as not drawn**, under
  construction. Korail and KTX are never queried (route=train is not asked
  for), as everywhere in Korea.
- **Gate 3 exact**: 22 stations against the operator's own count (Daejeon
  Transportation Corporation, 시설현황; brief check
  `daejeon-line1-operator-facts`), a primary source where Incheon's and the
  satellites' gates read Wikipedia. English names from the station objects'
  `name:en` on all 22. 대전역 is the Line 1 stop (route membership), not
  Korail's node.
- **Boundary**: OSM relation 2349984 (대전광역시, admin_level 4, KR-30),
  resolved by name and admin level, **536 km²**, gated at 525-545. The drawn
  line is 20.7 km station to station (the operator's 22.6 km runs 판암동 to
  외삼동, track beyond the end stations).
- **Line color**: the operator's green as OSM tags it (#007448), **Delta-E 23.1
  from Personal services**: above the floor of 10, below the preferred 45,
  kept on the owner's real-route-colors decision (2026-09-21) as Seoul's
  Line 8 (18.0) and Goyang's Gyeongui-Jungang Line (27.6) were.
- **Personal exposure: PASS.** `check_personal_exposure.py daejeon` (the
  Korean pass): a Korean personal name at a residential address still shown on
  0 of 50,939 rows; 79 withheld by step 2 (44 of them in-ring pins).
- **Licence**: notice 68 (SEMAS) gains Daejeon in its heading and text; notice
  1 and `app/osm_notice.py` name Daejeon's lines, stations and boundary as
  OSM's. No new notice.
- **Page prose proposal** (not covered by the template): the bullet "Not
  drawn: Line 2, a tram still under construction, and Korail's intercity
  lines."
- **Downstream**: notice 68 is a **caption** (a source credit, no wording
  prescribed; the categories and counts stated as this project's); notice 1
  covers rail, boundary and station names. **Open terms question, known**:
  the Visuals registry holds every notice-68 city off the cards while whether
  SEMAS's permission reaches social posts is open; Daejeon carries notice 68
  only, so it inherits the hold (the Visuals session confirmed the rule by message).
- **Master list**: Daejeon's Band A row marked built; the Built table, the
  East Asia row and South Korea's country row count it.

### 2026-10-04 - korea_sbiz: a 시군구코드 filter beside the 시군구명 prefix, zero drift on the ten built SEMAS cities

- **The change** (`docs/handoff_korea_sweep_2026-10-03.md`, Phase 1):
  `pipeline/countries/korea_sbiz.py` now reads `시군구코드` and
  `storefronts()` takes `sigungu_codes`. Given codes, they decide the rows;
  given prefixes as well, the two must pick identical rows or the step
  exits. An unknown code exits rather than silently matching nothing. The
  built cities pass prefixes only and are read exactly as before; the output
  columns are unchanged (the code is read, never written).
- **Why:** 시군구명 is not unique within a SEMAS member. Gwangju's 동구,
  서구, 남구 and 북구 recur in other metropolitan cities, and 경기도 광주시
  is another city; the 2026 merger put Gwangju in the member
  전남광주통합특별시 with all of South Jeolla. A code is unambiguous.
- **Verified:** `python pipeline/drift_check.py` over the ten built SEMAS
  cities (Incheon, Goyang, Suwon, Yongin, Seongnam, Bucheon, Ansan, Anyang,
  Namyangju, Uijeongbu), under `heavy_job.py`: **zero drift** in every
  output, and the four cities with a `baseline.json` (Ansan, Anyang,
  Namyangju, Uijeongbu) report 10 figures unchanged. Measured peaks: Goyang
  alone 0.38 GB, the other nine two at a time 0.75 GB.
- **Session setup, 2026-10-03:** branch 0 behind `origin/master` at
  `fafec401`; registered in `docs/session_roles.md`; `brief_check.py
  daejeon gwangju gimhae` 13/13 claims hold.
