# DECISIONS drafts - the UK six build (`uk-six-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

## For the owner at review time

**Answered early by the owner, 2026-10-02 (in chat):** "1. light rail, 2.
accepted and note this 3. display 4. accepted" - calls 1 to 3 below as
recommended, and the prose proposals below accepted. The entry "The owner's
first four UK six calls" records them.

**Calls to approve with the builds** (each is a recommendation, with the
precedent it follows):

1. **Manchester's `mode` is `light_rail`**, not `tram`. On the light-rail
   test, OSM maps 100% of the kept track `railway=light_rail`, 10.2% in
   tunnel or on a bridge, with a 703 m median gap: San Diego's figures (13%,
   87%, 851 m). Its three converted-railway branches meet the frequency
   gate at TfGM's 15 minutes.
2. **Manchester's lines are TfGM's nine, routed over OSM's track** (below).
   It follows the "real public name" invariant. No precedent draws lines
   from an operator's stop list rather than OSM's own relations.
3. **Notice 86 (NaPTAN)**: displaying the OGL's default statement is
   recommended, the cautious reading of whether a checked count is "use".
   The wording is new.

**Prose proposals** (sentences no template covers; the build did not stop
for them):

- `app/pages/156_Manchester_Heatmap.py`: "Each line follows OpenStreetMap's
  track through its stops as TfGM lists them." Why: the lines are routed,
  not OSM's relations, and the tram template's "redrawn from OpenStreetMap's
  route geometry" would not be true.
- `app/pages/156_Manchester_Heatmap.py`: "Trams run about every 15 minutes on
  each line by day." It is the tram template's frequency bullet with "on each
  line" added.
- Notice 86's text (`app/components.py`): "Stop counts on the UK's tram and
  light-rail maps are checked against NaPTAN, the National Public Transport
  Access Nodes dataset published by the Department for Transport. Contains
  public sector information licensed under the Open Government Licence v3.0.
  The Department for Transport does not endorse this map."

**For Cleanup and staging (not this build's files):**

- The briefs say British National Grid (EPSG:27700) "as London" for
  distances. London's, Glasgow's and Newcastle's `CRS_PROJECTED` is UTM 30N
  (EPSG:32630), and the six follow them. EPSG:27700 is only Code-Point's own
  CRS. This is staging's to correct in the briefs.
- Newcastle's legend rows read "Green line Green line (Tyne and Wear Metro)",
  because `build_legend` writes the label and then the legend name. Its
  notice 63 also still says "centre" twice. Both are Cleanup's.
- `scripts/check_stray_downloads.py` names the main checkout's own `data/`
  as a stray. It is the shared folder every worktree's `data/` junction
  points at, and its date moved to 12:29 when this session created
  `data/manchester/`. Cleanup should teach the check, never remove the folder.
  It also names `neutral-comment-style.md` (2026-10-01), which is not this
  session's.

---

### 2026-10-02 - Birmingham (Regional) built: West Midlands Metro's one line, gate 3 exact against the operator and NaPTAN, Line 2 not yet open

- **Scope (owner, 2026-10-01):** the three districts West Midlands Metro
  serves (Birmingham 402, Sandwell 423, Wolverhampton 436). Exactly three FSA
  codes are asserted. The boundary is the union of OSM relations 162378,
  162485 and 173722, 422.8 km², gated at 400-445.
- **Line 2 and Dudley are not on the map (the lead, 2026-10-02).** The
  operator's maps page (`westmidlandsmetro.com/maps/`, read 2026-10-02) lists
  35 stops, none on Line 2. The opening missed its 28 August 2026 date, and
  Dudley Council's leader gives 1 November 2026. Relation 17248967 sits in
  `NOT_DRAWN`, and the brief's pre-approved Dudley branch does not apply.
  Watch item for PLAN: Line 2 with Dudley (FSA 409), about 1 November 2026.
- **One drawn line, West Midlands Metro.** OSM's 6 ref-1 relations are
  service patterns of one line: Wolverhampton Station or Wolverhampton St
  Georges to Edgbaston Village each way, and the Millennium Point branch each
  way. The operator's page names no line ("the Metro"), so the label is the
  system's name, as the one-line precedents (Odense Letbane, Sun Link, KC
  Streetcar). The legend adds "(Wolverhampton - Edgbaston Village)".
- **The branch rule takes Birmingham's thresholds** (`BRANCH_NEAR_M` 30,
  `BRANCH_MIN_NEW_M` 50; shared change e2452466). The Eastside branch adds
  about 415 m of track beyond 30 m of the main relation, and the St Georges
  stub adds 72 m. Under London's defaults (300 m, 1,000 m), Millennium Point
  sat 397 m, Albert Street 220 m and Wolverhampton St Georges 100 m off the
  drawn line. At 30 m and 50 m, 3 of the 6 relations are drawn (23.8 km), and
  every station is within 4 m of the line.
- **Role-less stop members** (shared change e2452466). The four Wolverhampton
  - Edgbaston Village relations list their stops with an empty role, 118
  memberships. `ROLELESS_STOP_RELATIONS` reads them as stops, and the step
  stops once OSM gives them roles. Rejected: 49 `STATION_ADD` entries by node,
  the build's first draft.
- **Stations:** 67 stop positions collapse to 35 by name (the widest, Bilston
  Central, 46 m across). "Dudley Street, Guns Village" is aliased to "Dudley
  Street Guns Village". All 35 are inside the three districts, and none is
  thinned. The closest pair is Pipers Row and Wolverhampton St Georges, 173 m
  apart, two stops the operator lists.
- **Gate 3, exact on both sources:**
  - The operator's maps page lists 35 stops (its stop links and zone list),
    all on Line 1, Albert Street and Millennium Point included. The build has
    35.
  - NaPTAN holds 43 active MET records (prefix `9400ZZWM`, ATCO area 940)
    inside the scope, and 35 match name by name. NaPTAN's "Centenary Square"
    is Library (6 m), and its "Wednesbury Central" is Wednesbury, Great
    Western Street (98 m; the next stop is 537 m away).
  - Eight records are explained: Line 2's five in Sandwell (Birmingham New
    Road, Dudley Port, Great Bridge, Horseley Road, Sedgley Road), and three
    Eastside stops beyond Millennium Point that the operator does not list yet
    (Curzon Street, Digbeth High Street, Meriden Street). Watch item for PLAN:
    the Eastside stops, when they open.
- **Rings: halved.** The median gap in scope is 442 m, under the spacing
  rule's 550 m, so the rings are 0.05 to 0.3 mi, with bounds of 390-500 m.
- **The light-rail test:** the kept track is 100% `railway=tram` (47.6 km of
  route track, each way once), 7.1% in tunnel or on a bridge, with a 442 m
  median gap. Frequency is every 4-11 minutes by day (the operator's maps
  page), which meets the converted-railway gate on the former Great Western
  trackbed from Snow Hill to Priestfield. **`mode`: `tram`**, on Riga's tram
  control (2%, 0/98%, 360 m) and Santa Cruz-La Laguna's tram verdict (the
  lead accepted it, 2026-10-02).
- **Colour:** `scripts/line_colour_search.py birmingham` gives `#F000B8`, the
  nearest feasible colour to OSM's `#ec008c`: 45.2 from every pin, 4.81:1 and
  3.89:1 on the two pages.
- **A duplicated register row** (shared change e2452466). Sandwell's file
  lists FHRSID 372079 twice, identical on every field read. It is kept once,
  and an FHRSID whose rows differ still stops the step.
- **Businesses, step by step:**
  - 15,215 register rows in 3 authorities, with extracts all of 2026-10-02;
    1 duplicate row kept once.
  - 9,816 storefront rows (the brief's API count was 9,827 a day earlier).
  - 53 at a "Flat" address are never placed; no childminders.
  - 802 have no FSA point. Of those, 433 are placed at a Code-Point centroid
    and 369 (3.8%) are not placed: Sandwell 4.2%, Birmingham 4.1%,
    Wolverhampton 1.9%. No row had an outward code only, 331 had no usable
    postcode, and 38 had a full postcode that is not in Code-Point.
  - 2 fall outside the sanity box and 8 outside the districts.
  - 45 trading-as names show the trade name.
  - **9,384 storefronts placed** (Food service 5,796, Food shops 3,588):
    95.4% at the FSA's point, 4.6% at a centroid. The FSA-point share is
    96.4% in Birmingham, 91.2% in Sandwell and 96.0% in Wolverhampton, each
    above the brief's sample.
  - The render's contact-detail scrub drops 1 more (9,383). 1,642 (17.5%)
    sit within a ring: Food service 1,162, Food shops 480.
  - Canteens by name are at least 1.9% of Restaurant/Cafe/Canteen, not
    separated (London's lower bound).
- **Personal exposure (`check_personal_exposure.py birmingham`):**
  - 1,642 pins and 1,512 distinct names. No fallback name exists.
  - 0 emails or phone numbers. 1 "c/o" marker, a contract caterer at a
    company site.
  - 1 surname-first name and 8 "person's name (trade name)" shapes.
  - The heuristic reads 370 (22.5%) as person-like, mostly cafés and shops
    named for people.
  - **Verdict: publish**, London's, Newcastle's and Manchester's: the same
    register and the same structural guards.
- **CRS:** UTM 30N (EPSG:32630), as the built UK cities.
- **Notices:** 87 (FSA, Birmingham) and 88 (Ordnance Survey, Birmingham) are
  Manchester's 84 and 85 with the city and figures changed. NaPTAN is notice 86.
- **Page:** `app/pages/157_Birmingham_Heatmap.py`. Newcastle's FSA bullets
  plus the tram template's line bullets; the proposals are listed in the
  owner's section.

### 2026-10-02 - The owner's first four UK six calls: Manchester is light rail, its lines are TfGM's routed over OSM's track, NaPTAN's notice is displayed, the proposals accepted (owner)

- **The owner, answering ahead of review time:** "1. light rail, 2.
  accepted and note this 3. display 4. accepted".
- **1. Manchester (Regional)'s `mode` is `light_rail`**, on the light-rail
  test (100% `railway=light_rail`, 10.2% tunnel or bridge, a 703 m median
  gap; San Diego's precedent).
- **2. A city's lines may be the operator's own, routed over OSM's track**
  through the operator's stop sequences, where OSM's service relations no
  longer match the operator's lines (Manchester: five of TfGM's nine lines
  have no relation since 14 September 2026). "Note this": the rule goes
  where the next OSM city passes through it, in `pipeline/countries/uk.py`
  (`LINE_STOPS`, `routed_lines`) and the `osm-rail` skill.
- **3. Notice 86 (NaPTAN, United Kingdom) is displayed**, the OGL's default
  statement with the licence linked, on the cautious reading that a count
  checked against the data is use of it.
- **4. The prose proposals are accepted:** Manchester's two sentences ("Each
  line follows OpenStreetMap's track through its stops as TfGM lists them";
  "Trams run about every 15 minutes on each line by day") and notice 86's
  wording.

### 2026-10-02 - Manchester (Regional) built, the pilot of the UK six: TfGM's nine lines routed over OSM's track, gate 3 against TfGM and NaPTAN

- **Scope (owner, 2026-10-01):** the seven districts Metrolink serves
  (Bury 405, Manchester 415, Oldham 418, Rochdale 419, Salford 422, Tameside
  430, Trafford 431). Exactly seven FSA codes are asserted. The boundary is
  the union of OSM relations 146656, 146657, 146675, 146925, 146926, 146927
  and 146655, 822.0 km² in UTM 30N, gated at 790-850.
- **Shared code, written here for the five after it:**
  `pipeline/countries/uk.py` holds the steps and `uk_fetch.py` the
  downloads, split as Czechia's are so a step imports nothing that fetches.
  - The fetch makes ONE Overpass query per city: routes and boundaries with
    geometry, the member ways' tags and the member nodes.
  - Step 1 runs on `osm_tram` and gate 3 runs twice.
  - Step 2 is Newcastle's, unchanged in method.
  - No existing shared module was edited. London's and Newcastle's drift
    checks are the control (recorded below once run).
- **The lines are TfGM's, not OSM's.** OSM's 23 relations carry 11 service
  refs from before TfGM's 14 September 2026 change. TfGM's network map
  (`tfgm.com/public-transport/tram/network-map`, read 2026-10-02) names nine
  lines by colour, each with its stops in order.
  - Four match an OSM service: Green, Pink, Anthracite and Navy.
  - Five run where no OSM relation does: Purple (Altrincham - Etihad
    Campus), Yellow (Eccles - Piccadilly), Burgundy (MediaCityUK -
    Piccadilly), Blue (Ashton-under-Lyne - Bury) and Red (The Trafford
    Centre - Crumpsall).
  - Each line is routed over the kept relations' track, stop to stop, by
    the shortest track path. Double track is one way per direction, so each
    stop anchors on every track vertex within 40 m of its nearest one.
  - Drawn lengths run from Burgundy's 5.4 km to Pink's 35.8 km.
  - Rejected: drawing OSM's services under their own refs (no longer the
    operator's lines), and drawing them under TfGM's names (the geometry
    would contradict the names).
- **TfGM's two slips, handled in config.** Its Red line lists "Abramham
  Moss", aliased to Abraham Moss. It also skips St Peter's Square between
  Deansgate-Castlefield and Exchange Square, where the only track runs
  through it.
- **The ECL relation (16749012) is not drawn.** It has ref "ECL", network
  "Metrolink" and operator "TfGM", and no stop members. 99.4% of its 6.8 km
  lies within 30 m of the Ashton-under-Lyne - Eccles via MediaCityUK track,
  so it duplicates the Eccles line. It sits in `NOT_DRAWN` with that reason.
- **Stations:** 192 stop positions collapse to 99 by name (the widest,
  Robinswood Road, 174 m across). All 99 are inside the seven districts, and
  none is thinned. The median gap is 703 m, so the rings are standard.
- **Gate 3, exact on both sources:**
  - TfGM's stop list (`tfgm.com/public-transport/tram/stops`) holds 99 stops,
    a whole-network count. A per-line count would be circular, since the
    lines are TfGM's own sequences.
  - NaPTAN holds 99 active MET records (prefix `9400ZZMA`, ATCO area 940)
    inside the scope, matched name by name. The one spelling difference,
    "Besses o'th'Barn", falls away under the punctuation-blind match.
  - NaPTAN files every tram stop under ATCO area 940, the national tram and
    metro area; Greater Manchester's area 180 holds none.
- **The light-rail test:** the kept track is 100% `railway=light_rail`
  (195.7 km of route track, each way once), 10.2% in tunnel or on a bridge,
  with a 703 m median gap. Frequency is 15 minutes per line since 14
  September 2026 (TfGM), which meets the converted-railway gate on the Bury,
  Altrincham and Oldham-Rochdale branches. **Recommended `mode`:
  `light_rail`** (the owner approves it with the build).
- **Colours:** `scripts/line_colour_search.py manchester` gives each TfGM
  hue's nearest feasible colour, every one 45.1 or more from the pins. The
  closest pair within 500 m is 18.1 (Burgundy and Purple), and the nine
  dark-mode labels are distinct. The legend row reads "<Colour> line (<ends>)".
- **Businesses, step by step:**
  - 17,642 register rows in 7 authorities, with extracts all of 2026-10-02.
  - 12,461 storefront rows (the brief's API count was 12,451 a day earlier).
  - 10 at a "Flat" address are never placed; no childminders.
  - 1,151 have no FSA point. Of those, 673 are placed at a Code-Point
    centroid and 478 (3.8%) are not placed: Bury 7.2%, Tameside 6.2%. No row
    had an outward code only, and 350 had no usable postcode.
  - 4 fall outside the sanity box and 6 outside the districts.
  - 51 trading-as names show the trade name.
  - **11,963 storefronts placed** (Food service 8,085, Food shops 3,878):
    94.4% at the FSA's point, 5.6% at a centroid. Tameside's low sample
    share (78.9%) did not hold on the full file.
  - 6,202 (51.8%) sit within a ring: Food service 4,359, Food shops 1,843.
  - Canteens by name are at least 2.5% of Restaurant/Cafe/Canteen, not
    separated (London's lower bound).
- **Personal exposure (`check_personal_exposure.py manchester`):**
  - 6,202 pins and 5,319 distinct names. No fallback name exists, since step
    2 never loads an owner column.
  - 0 emails, phone numbers or c/o markers.
  - 1 surname-first name and 12 "person's name (trade name)" shapes.
  - The heuristic reads 1,600 (25.8%) as person-like, which on the FSA
    register is mostly pubs and cafés named for people.
  - **Verdict: publish**, London's and Newcastle's: the same register, the
    same structural guards (the FSA's private-address rule, the flat,
    childminder and trading-as rules).
- **CRS:** UTM 30N (EPSG:32630), as London, Glasgow and Newcastle. The
  brief's British National Grid is Code-Point's source CRS only.
- **Notices:** 84 (FSA, Manchester) and 85 (Ordnance Survey, Manchester) are
  Newcastle's 62 and 63 with the city and date changed. 86 (NaPTAN, United
  Kingdom) is new, from the `licence-read` of 2026-10-02: OGL v3.0, no
  attribution of the Department's own, no API terms. Display the OGL's
  default statement with the licence linked; never imply DfT's endorsement
  or use its logo.
- **Page:** `app/pages/156_Manchester_Heatmap.py` (page 156, staging's pre-assignment in
  `docs/session_roles.md`). Newcastle's FSA bullets plus the tram template's
  line bullets; two proposals are listed above.
