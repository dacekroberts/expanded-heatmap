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

### 2026-10-02 - Nottingham (Regional) built: NET's two lines from both directions' relations, gate 3 exact against NET and NaPTAN, halved rings, tram

- **Scope (owner, 2026-10-01):** the four councils NET serves (Nottingham
  City 899, Broxtowe 261, Rushcliffe 266, Ashfield 259); exactly four FSA
  codes asserted. The boundary is the union of OSM relations 123292 (the
  unitary city, admin_level 6), 154058, 77311 and 154043 (the districts,
  admin_level 8), 673.7 km² in UTM 30N, gated at 640-700; never
  Nottinghamshire (181040). Gedling (262) has no stop.
- **OSM's four relations are one per line per DIRECTION, each end to end**,
  not the brief's half-lines meeting in the centre: 170076 and 1984324 (Line
  1), 1984359 and 1984325 (Line 2), all `#003828`. All four are kept.
  - London's branch rule (300 m, 1,000 m) kept one direction per line and
    left Hyson Green's northbound one-way street (Noel Street, Beaconsfield
    Street, Shipstone Street) undrawn, Beaconsfield Street 232 m off its
    line. Beyond 30 m of the first direction the second adds 742 m in 8
    parts on each line, so `BRANCH_NEAR_M = 30`, `BRANCH_MIN_NEW_M = 500`
    (Birmingham's lowering): 2 of 2 relations per line, 23.3 km and 16.4 km.
- **Four OSM defects, handled in config (the shared fixes of e2452466):**
  - two northbound stop members that are no stop, skipped
    (`SKIP_MEMBERS`): 9243041864, a `railway=tram_crossing` about 30 m from
    Wilkinson Street, and 6711112153, an untagged node about 60 m from
    Bulwell; the southbound relations carry both real stops;
  - Highbury Vale's two branch platforms, "Highbury Vale A" and "B" in OSM,
    one stop to NET and NaPTAN (`STATION_RENAMES`, Newcastle's "St. James"
    precedent); 4 positions, 104 m across;
  - Bulwell Forest, on both Line 1 relations with an empty role, added by
    both its nodes (`STATION_ADD`);
  - David Lane, on no relation, which NET lists on both lines, added by both
    its nodes once the widened fetch cached them (`STATION_ADD`, lines 1
    and 2).
- **Stations:** 88 stop positions collapse to 50 by name, all inside the
  four council areas (City 35, Broxtowe 9, Rushcliffe 4, Ashfield 2). None
  is thinned or excluded.
- **Gate 3, exact on both sources:**
  - NET's timetables page (`thetram.net/timetables`, read 2026-10-02)
    lists 50 stops; each stop's direction headings give Line 1 36 and Line 2
    30, against the build's 36 and 30.
  - NaPTAN: 50 active MET records (prefix `9400ZZNO`, ATCO area 940) inside
    the scope, 50 of 50 names matched; NaPTAN's "NTU" read as Nottingham
    Trent University.
  - Before David Lane was added, both gates failed on it (35 and 29), the
    fault gate 3 exists to catch: OSM's relations skip a served stop.
- **Rings: halved** (0.05 to 0.3 mi). The median gap in scope is 432 m,
  under the spacing rule's 550 m; bounds 380-490.
- **The light-rail test:** the kept track is 100% `railway=tram` (57.0 km of
  route track, each way once), 5.5% in tunnel or on a bridge, a 432 m median
  gap. Trams every 7-10 minutes Monday to Saturday (NET), so the Hucknall
  and Clifton former-railway sections pass the frequency gate.
  **Recommended `mode`: `tram`**; the owner approves it with the build.
- **Colours:** OSM gives both lines one colour and NET's site shows none, so
  two project hues (Dijon's rule: two lines with one colour are refused).
  `scripts/line_colour_search.py nottingham`: Line 1 `#586818` (45.0 from the
  pins), Line 2 `#D85028` (45.6), the pair 70.8 apart, the dark-mode labels
  distinct.
- **Businesses, step by step:**
  - 5,755 register rows in 4 authorities, extracts of 2026-10-01 (City,
    Rushcliffe, Ashfield) and 2026-10-02 (Broxtowe).
  - 3,702 storefront rows, as the brief.
  - 4 at a "Flat" address and 1 childminder never placed.
  - 307 have no FSA point. Of those, 97 are placed at a Code-Point centroid
    and 210 (5.7%) are not placed: Rushcliffe 14.2%, Ashfield 7.2%,
    Broxtowe 5.9%, the City 2.8%. No row had an outward code only; 209 had
    no usable postcode.
  - **The sanity box was widened**: the scaffold's (lon_max -0.93, lat_max
    53.16) cut 15 Rushcliffe premises inside the district, which runs to
    -0.815 and 53.171. Now 52.74-53.22, -1.40 to -0.76. 2 fall outside it
    (Ashfield points in Scotland) and 7 outside the four council areas.
  - 7 trading-as names show the trade name.
  - **3,478 storefronts placed** (Food service 2,252, Food shops 1,226):
    97.2% at the FSA's point, 2.8% at a centroid.
  - **Point shares on the full files fall a little under the brief's
    samples**: Rushcliffe 79.6% (446 of 560) against 80.2%, the City 95.4%
    against 96.2%, Broxtowe 91.3% against 91.4%; Ashfield 90.7% against
    90.6%. Accepted by the lead (2026-10-02), with Rushcliffe's unplaced
    share disclosed in the city's What Is Excluded section.
  - 1,210 (34.8%) sit within a ring: Food service 828, Food shops 382.
  - Canteens by name are at least 4.3% of Restaurant/Cafe/Canteen, not
    separated (London's lower bound).
- **Personal exposure (`check_personal_exposure.py nottingham`):**
  - 1,210 pins and 1,108 distinct names. No fallback name exists.
  - 0 emails, phone numbers or c/o markers.
  - 0 surname-first names and 2 "person's name (trade name)" shapes.
  - The heuristic reads 299 (24.7%) as person-like, mostly cafés, shops and
    takeaways named for people.
  - **Verdict: publish**, London's, Newcastle's and Manchester's: the same
    register, the same structural guards.
- **CRS:** UTM 30N (EPSG:32630), as the built UK cities.
- **Notices:** 93 (FSA, Nottingham) and 94 (Ordnance Survey, Nottingham),
  Newcastle's 62 and 63 with the city and date changed; NaPTAN is notice 86.
- **Page:** `app/pages/160_Nottingham_Heatmap.py` (page 160). Newcastle's FSA
  bullets plus the tram template's bullets under **The trams**; two
  proposals are listed in the drafts file's proposals section.

### 2026-10-02 - Sheffield built: Supertram's three routes, the Tram-Train left out, gate 3 against NaPTAN only

- **Scope (owner, 2026-10-01):** the City of Sheffield, FSA authority 425
  only; Rotherham (420) is out with the Tram-Train. The boundary is OSM
  relation 106956 (admin_level 8, GSS E08000039), 368.0 km², gated at
  350-385. On the UK six's shared steps (`pipeline/countries/uk.py`), config
  only; no shared file edited. Re-run on e2452466 with no change: none of its
  new options is needed, and step 2's exact-duplicate rule removes no row.
- **The lines are OSM's three Supertram routes,** each a directional pair
  merged by London's branch rule (`LINE_OSM_REFS`): Blue (165857, 9701743)
  19.3 km, Yellow (165852, 9701823) 13.6 km, Purple (165858, 9701599)
  8.0 km. OSM's relations match the operator's routes one for one, so no
  routing (`LINE_STOPS`) is needed. Labels "Blue route", "Yellow route",
  "Purple route", with the ends in the legend (OSM's from/to tags). The
  operator's own naming could not be read (its site refuses scripts); the
  route names are the brief's.
- **The Tram-Train (ref TT, relations 9701871 and 9701872) is not drawn**
  (owner, 2026-10-01): every 30 minutes on Network Rail track beyond
  Tinsley, which fails the converted-railway frequency gate (Aarhus L1's
  precedent). Its stops in Sheffield are all on the Yellow route; its three
  in Rotherham go with it.
- **Purple is drawn at about hourly** (Buffalo's rule: purpose-built track,
  so disclosed, not disqualifying; owner, 2026-10-01). It alone serves 2 of
  the 48 stops (Herdings Park, Herdings / Leighton Road). The page states
  the wait.
- **Stations:** 91 stop positions collapse to 48 by name (the widest,
  Granville Road / The Sheffield College, 141 m across). OSM spells one stop
  two ways across Yellow's directions ("Carbrook/Ikea", "Carbrook/IKEA"),
  merged by `STATION_NAME_ALIASES`. All 48 are inside the city; none thinned,
  none excluded.
- **Gate 3, NaPTAN only.** supertram.com serves a Radware CAPTCHA to scripts
  and Stagecoach's page returns 403 (2026-10-02); neither was passed, so
  `OPERATOR_STATION_COUNTS = None` with `OPERATOR_COUNTS_GAP` (owner,
  2026-10-01: NaPTAN is the only independent source). NaPTAN holds 51 active
  MET records for `9400ZZSY`, 48 inside the city, matched name by name: 48 of
  48. Six NaPTAN names differ from OSM's and are paired by position in
  `NAPTAN_NAME_ALIASES` (1 to 72 m). One is a rename: NaPTAN's "Kelham
  Island" carries Shalesmoor's ATCO code (9400ZZSYSHL), stands 3 m from OSM's
  Shalesmoor, and was revised 2025-05-08. The map keeps OSM's name; showing
  "Kelham Island" goes to the owner.
- **The light-rail test:** the kept track is 100% `railway=tram` (56.7 km of
  route track, each way once), 4.3% in tunnel or on a bridge, with a 444 m
  median gap. **Recommended `mode`: `tram`** (Odense's precedent; Manchester's
  100% light_rail and 703 m is the contrast). The owner approves it with the
  build.
- **Rings: halved** (0.05 / 0.1 / 0.2 / 0.3 mi; Aarhus's). The median gap in
  scope is 444 m (min 145, Castle Square to Fitzalan Square / Ponds Forge,
  both in NaPTAN), under the spacing rule's 550 m; step 1 stops outside
  390-500.
- **Colours:** `scripts/line_colour_search.py sheffield` gives Blue #8018F8
  (OSM's #0000FF reads about 2.2:1 on the dark page), Yellow #989800 (OSM's
  #FFFF00 fails 3:1 on the light page; darkened as Tours and Dijon were) and
  Purple #A030A0. Every one is 45.4 or more from the pins; the closest pair
  is 55.1 (Blue, Purple); the dark-mode labels are distinct.
- **Businesses, step by step:**
  - 4,859 register rows in 1 authority, extract 2026-10-02.
  - 3,447 storefront rows (the brief's 3,447).
  - 4 at a "Flat" address are never placed; no childminders.
  - 163 have no FSA point. Of those, 70 are placed at a Code-Point centroid
    and 93 (2.7%) are not placed: 13 with a full postcode not in the edition,
    80 with no usable postcode, none with an outward code only.
  - 2 fall outside the sanity box (bad FSA points, one on the south coast,
    one north-east of the city) and 0 outside the city.
  - 8 trading-as names show the trade name.
  - **3,348 storefronts placed** (Food service 2,365, Food shops 983):
    97.9% at the FSA's point, 2.1% at a centroid. The FSA point share of
    storefront rows on the full file is 95.3%, under the brief's sample
    figure of 96.4%; 97.3% of storefront rows are placed, which the lead
    accepted (2026-10-02): the full file against the brief's sample.
  - 1,162 (34.7%) sit within a ring: Food service 869, Food shops 293.
  - Canteens by name are at least 1.5% of Restaurant/Cafe/Canteen, not
    separated (London's lower bound).
  - Excluded by type: other catering 529, hospitals/childcare/caring 336,
    schools 261, mobile caterers 142, manufacturers 68, distributors 37,
    hotels 29, farmers 7, importers 3.
- **Personal exposure (`check_personal_exposure.py sheffield`):** 1,162
  pins, 1,061 distinct names; no fallback name exists; 0 emails, phone
  numbers or c/o markers; 0 surname-first names and 1 "person's name (trade
  name)" shape; the heuristic reads 299 (25.7%) as person-like, mostly cafés
  and takeaways named for people. **Verdict: publish**, London's,
  Newcastle's and Manchester's on the same register and guards.
- **CRS:** UTM 30N (EPSG:32630), as the built UK cities.
- **Notices:** 91 (FSA, Sheffield) and 92 (Ordnance Survey, Sheffield),
  Newcastle's 62 and 63 with the city and date changed; NaPTAN's 86 covers
  gate 3.
- **Page:** `app/pages/159_Sheffield_Heatmap.py`, under the headings "The
  trams", "The businesses" and "Reading the map": Newcastle's FSA bullets
  with Sheffield's figures (one in thirty-seven unplaced; one in three in a
  ring) and the tram template's line bullets. Five proposals are listed for
  the owner.

### 2026-10-02 - Edinburgh built, third of the UK six: one tram line on OSM's two through relations, gate 3 exact against Edinburgh Trams and NaPTAN, the short register disclosed

- **Scope (owner, 2026-10-01):** the City of Edinburgh, FSA code 773 on Food
  Standards Scotland's FHIS (SchemeType 2); exactly one code asserted. The
  boundary is OSM relation 1920901 (admin_level 6, GSS S12000036), 272.9 km² in
  UTM 30N, gated at 240-300.
- **Config on Manchester's contract.** No shared module was edited.
- **The line is one, from OSM's two through relations.** The three tram
  relations carry no ref, network or operator tag.
  - Newhaven => Airport (2632877, 23 stops) and Airport => Newhaven (4116776,
    22, ending at Ocean Terminal) take the ref "Tram" through
    `REF_BY_RELATION` and are merged by London's branch rule (one direction
    drawn, 18.4 km).
  - The label is the operator's name, "Edinburgh Trams"; the legend adds
    "(Airport - Newhaven)", as the timetables page writes the ends.
  - No colour in OSM or from the operator, so the project's own hue
    `#b8860b` (Odense's and Kansas City's); `line_colour_search.py` gives
    `#B88810`, 73.6 from every pin, 5.86:1 dark and 3.20:1 light.
- **"Tram Extension to Newhaven" (11819309) is not drawn.** No stop members,
  `start_date` 2023-06-07, the council's extension page as its website, and
  100% of its 9.3 km within 15 m of both through relations' track: a leftover
  of the extension's construction mapping. It sits in `NOT_DRAWN` with that
  reason.
- **Stations:** 45 stop positions collapse to 23 by name (the widest, Port of
  Leith, 50 m across). All 23 are inside the city; none is thinned.
- **Gate 3, exact on both sources:**
  - Edinburgh Trams: the route map on `edinburghtrams.com/timetables` names
    23 stops (read 2026-10-02), a whole-network count for the one line. The
    page's timetable table lists only 13 timing points.
  - NaPTAN: 23 active MET records in area 940 inside the city, matched name by
    name. The eight Newhaven-extension stops (Picardy Place to Newhaven) are
    filed under the Tyne and Wear prefix `9400ZZTW`, the other 15 under
    `9400ZZED`. NaPTAN's "West End - Princes Street" is aliased to West End
    (`NAPTAN_NAME_ALIASES`), the name OSM and the operator use. Inactive York
    Place and the depot fall out on status.
- **Rings: standard.** The median gap in scope is 614 m (min 338, mean 645, max
  1,199), over the spacing rule's 550 m and clear of the 540-570 m owner band;
  `MEDIAN_GAP_BOUNDS_M` 570-700.
- **The light-rail test:** the kept track is 100% `railway=tram` (36.8 km of
  route track, each way once), 4.6% in tunnel or on a bridge, with a 614 m
  median gap. Trams run every 7 minutes by day, every 10 early and in the
  evenings, on purpose-built track. **`mode` is `tram`** (lead, 2026-10-02):
  Dublin's Luas, a street tram that clears the spacing at 575 m, and Riga's
  control (2%, 98% tram).
- **The placement share, against the brief's 96.6%.** The brief's figure was
  a first-page API sample, whose default order leans to 5-rated premises
  (Manchester's Tameside sample read off the same way). The full file gives
  93.9% at the FSA's point and 95.4% placed (4.6% unplaced), within the built
  cities' range (London 5.0%, Manchester 3.8%); settled by the lead
  2026-10-02 and disclosed on the page in Newcastle's words ("about one food
  storefront in twenty-two").
- **The centroid tier is kept (the kit), an open item for the owner.** It
  places 57 storefronts (1.5% of those placed): unplaced is 4.6% with it, 6.1%
  without. Glasgow's precedent is no centroids, at 1.2% without a point, where
  its 22 full postcodes would have added about 0.5%. Notice 90 stays while the
  tier does.
- **The register is short, disclosed rather than padded.** 5,144 premises
  against Glasgow's 6,632. It matches the FSA's published `EstablishmentCount`
  (5,144, last published 2026-10-02) and the file's ItemCount; FSS publishes no
  count, and its own copy of the council file is listed at 4.6 MB, in line with
  the FSA's 4,797,465 bytes. Four types are absent: Mobile caterer,
  Distributors/Transporters, Importers/Exporters and Farmers/growers (Glasgow
  425, 84, 23, 1), none a storefront type. Retailers - other (628 against
  1,150) and Takeaway/sandwich shop (680 against 1,109) are low against
  Glasgow's. Stated in Edinburgh's section of What Is Excluded as a limit.
- **Businesses, step by step:**
  - 5,144 register rows, extract 2026-10-02; 3,933 storefront rows.
  - 0 at a "Flat" address, 0 childminders.
  - 239 have no FSA point: 57 placed at a Code-Point centroid, 182 (4.6%) not
    placed (151 with no usable postcode, 149 of them blank; 31 with a full
    postcode Code-Point does not hold); no outward-code-only rows.
  - 0 outside the sanity box, 1 outside the city.
  - 5 trading-as names show the trade name.
  - **3,750 storefronts placed** (Food service 2,995, Food shops 755): 98.5%
    at the FSA's point, 1.5% at a centroid.
  - 2,226 (59.4%) sit within a ring: Food service 1,854, Food shops 372.
  - Canteens by name are at least 1.4% of Restaurant/Cafe/Canteen (26 of
    1,818), not separated (London's lower bound).
- **Personal exposure (`check_personal_exposure.py edinburgh`):**
  - 2,226 pins and 2,010 distinct names. No fallback name exists, since step
    2 never loads an owner column.
  - 0 emails, phone numbers or c/o markers; 0 surname-first names.
  - 6 (0.3%) "person's name (trade name)" shapes.
  - The heuristic reads 554 (24.9%) as person-like, which on this register is
    mostly cafés, takeaways and pubs named for people.
  - **Verdict: publish**, Glasgow's, London's, Newcastle's and Manchester's:
    the same register, the same structural guards.
- **CRS:** UTM 30N (EPSG:32630), as London, Glasgow and Newcastle.
- **Notices:** 89 (Food Standards Scotland, Edinburgh) is Glasgow's 61 with the
  city and date changed and Manchester's centroid clause added; 90 (Ordnance
  Survey, Edinburgh) is Newcastle's 63 with the city changed; NaPTAN is notice
  86, as for every UK city.
- **Page:** `app/pages/158_Edinburgh_Heatmap.py` (page 158). Glasgow's FHIS
  bullets, Newcastle's placement bullets and the tram template's line bullets
  under "The tram"; the proposals are listed above.

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
