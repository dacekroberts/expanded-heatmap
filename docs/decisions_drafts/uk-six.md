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
