# DECISIONS drafts - Korea sweep (`korea-sweep-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

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
