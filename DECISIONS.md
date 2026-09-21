# Decisions log

Every judgment call, recorded with the numbers that were true when it was
made. **Append-only**: a superseded decision gets a new entry that says what
changed and why - the old entry stays. `docs/project_context.md` describes
the *current* state and is rewritten as things change; this file is the
trail behind it. Format and voice: see the `decisions-entry` skill (neutral
past tense; entries were reconstructed from session context).

Newest first. Entries run from the project's first working day, 2026-09-18,
onwards; the early ones are split by phase rather than by hour.

---

## Changes

### 2026-09-21 - Canada re-ranked on storefront counts: Montreal is next, not Surrey

- **Done on the owner's instruction, after the Vancouver build showed the
  published ranking was not internally comparable.** Recomputed by
  `scripts/rank_canada_storefront_density.py`, which is committed so the
  measurement is reproducible rather than a one-off. Every figure is
  storefronts - buckets anchored on `naics.py` - inside the UNION of the
  0.6 mi rings, divided by in-city stations, which is the basis D.C.'s ~173
  and Boston's ~39 use.

      | city      | in ring | stations | per station | published | inflation |
      | Vancouver |   4,129 |       20 |     **206** |       861 |     4.2x  |
      | Montreal  |   9,695 |       64 |     **151** |       252 |     1.7x  |
      | Surrey    |     539 |        4 |     **135** |       549 |     4.1x  |
      | Edmonton  |   2,520 |       33 |      **76** |       153 |     2.0x  |
      | Calgary   |   6,243 |       83 |      **75** |       103 |     1.4x  |
      | Toronto   |       - |      234 |      **41** |        41 |     1.0x  |

- **The inflation is NOT uniform, and that is the whole problem.** It runs from
  1.0x to 4.2x, because it depends on how much of each register is not
  storefront: Vancouver's and Surrey's licence files are full of residential
  rentals and contractors, while Montreal's source is a commerce survey. The
  published ranking therefore flattered licence-register cities against
  Montreal by roughly 2.5x.
- **One position actually changes: Montreal and Surrey swap.** Published,
  Surrey (549) sat well above Montreal (252); measured, **Montreal 151 beats
  Surrey 135**. Edmonton and Calgary also collapse from 153-vs-103 into a tie
  at 76 and 75.
- **A correction to my own earlier claim.** I had said Toronto's last place was
  "the least trustworthy number in the table" and that a common basis would
  narrow the gap "substantially". It narrows - Calgary/Toronto goes from 2.5x
  to 1.8x - but **Toronto stays last, clearly**, because its 41 was already
  storefront-filtered. The order was directionally right all along; the
  magnitudes were not.
- **Only Vancouver beats D.C. (~173).** Montreal lands just under it, Surrey
  below that, and Calgary and Edmonton at roughly twice Boston.
- **Montreal is the recommended next build, on three grounds that agree.** It
  is the densest remaining (151); it is the **cheapest**, because its `SCIAN`
  IS NAICS so `naics.py` applies unchanged and it needs **no taxonomy module
  at all** - against Calgary's 96 categories and Edmonton's 60; and its source
  is the **best-matched in the project**, a street-level commerce survey where
  **69.4% of non-vacant rows are storefronts** against Vancouver's 28.2%. Its
  agglomeration scope was already decided.

### 2026-09-21 - Five more corrections to the Canada profile, found while re-ranking

- **Montreal publishes 3,500 VACANT units and nobody had recorded it.**
  `USAGE1 = 'VACANT'` on 3,500 of 28,621 survey rows, plus a separate
  `VACANT_A_LOUER` flag (Oui on 712). An empty shopfront is not a business and
  they are excluded. Also `SCIAN` is a **1-character placeholder on 294 of the
  non-vacant rows**, so usable 6-digit codes cover 98.8% of them rather than
  the recorded 99.6% of everything.
- **Calgary has 96 real categories, not 173.** The recorded figure came from
  splitting `licencetypes` on a bare `"\n"` when the delimiter is `",\n"`,
  which shreds each value and counts the fragments. Edmonton is the same
  mistake: **60 real categories, not 67**, on `";"`. Both are far smaller and
  cleaner than recorded, which makes both cheaper than the profile suggests.
- **Edmonton HAS a licence-level home-business flag, which the profile missed.**
  `licencetype` splits Commercial 25,105 / Home Based 14,114 / Non-Resident
  2,108 / Massage Practitioner 1,582 / Adult Services 763. That is Surrey's
  shape - the city STATES it - so Edmonton needs no residence inference either.
  The profile had recorded only the `<Home Based Business>` address
  placeholder, which is the same fact seen through a weaker signal.
- **Edmonton's coordinate coverage is 92.7% where it matters, not 53.3%.** The
  53.3% was measured across the whole file including the Home Based rows,
  whose addresses are placeholders. On the Commercial rows this project would
  actually map, 23,265 of 25,105 carry coordinates, and of its storefront
  subset 99.3% do. **The denominator error again**, now the fourth instance in
  this project.
- **Two of the three catalogue feeds are STALE.** Montreal's Mobility Database
  mirror is 29 days expired and Edmonton's is **93 days** expired; Calgary's
  carries no `feed_info.txt` at all. Station counts still reproduced exactly
  (68 / 83 / 33), so the ranking stands - but Edmonton's Valley Line is
  actively extending, and a 93-day-old feed is exactly how the Toronto mirror
  hid an entire mode. **Any build must take the agency's own feed.** The
  committed script prints each feed's expiry for this reason.
- **A bug in my own first measurement, recorded because the number was
  plausible.** Summing per-station counts gave Montreal **440** per station.
  The correct figure is **151**: the Metro's stations are close enough that one
  business sits inside several rings, so the sum counts it repeatedly. Only the
  UNION of the rings is the number of distinct businesses near rail, and it is
  what every other figure in this project means. The script now does the union
  and says why in its docstring.

### 2026-09-21 - The macro map's opening view frames the US instead of every city

- **The owner's call, made mid-build and it retires a problem rather than
  tuning it**: "we can focus in on a region that's already well distributed
  like the US and just state there are more global cities around the map if you
  zoom out and scroll around", to "make sure we aren't wasting extra effort
  re-drawing labels and maps trying to get all cities to fit in one view".
- **The problem was real and measured, not hypothetical.** `fit_view` framed
  every entry in `cities.py`, so any city outside the existing box re-fitted
  the whole map. Adding Vancouver alone took the longitude span from 57.55 to
  58.31 degrees and the zoom from **1.4525 to 1.4336**, pulling the east-coast
  cluster tighter - New York to Philadelphia from 5.95 px to 5.87 px. Since
  every label offset in that file is a PIXEL offset measured at the old zoom,
  each new non-US city would have meant re-measuring all of them at three
  widths. A European city would have forced continent-specific maps and a
  layer of extra pages, which is the cost the zoomable-map decision was taken
  to avoid in the first place.
- **The fix is one flag.** A city carries `in_default_view: False` and
  `cities.IN_DEFAULT_VIEW` filters the list `fit_view` is given. US cities need
  no flag and nothing changed for them: the default zoom is **1.4525 exactly**,
  and all five documented separations reproduce (5.95 / 8.99 / 14.32 / 14.93 /
  7.66 px against the recorded 6.0 / 9.0 / 14.4 / 15.0 / 7.7). So no label was
  re-drawn, which was the point.
- **A correction to my own first attempt at the caption.** It said the other
  cities sit "outside" the opening view. They do not, necessarily: `fit_view`
  is computed for a 320 px reference and spends extra width as MARGIN, so at
  854 px the canvas covers far more latitude than the US box and Vancouver's
  dot is visible at x=336, y=150 - on canvas at 400, 854 and 1200 px alike.
  Whether a city falls just inside or just beyond the edge depends on container
  width, so the wording now covers both and names the text-link list as the
  guarantee. The list has always held every city, which is why the view can be
  a framing choice rather than a completeness requirement.
- **`app/Overview.py` and `app/cities.py` belong to the app/chrome role under
  `session_roles.md`** and were edited by this build session on the owner's
  direct instruction. Recorded so the ownership departure is visible rather
  than inferred.

### 2026-09-21 - Vancouver + Surrey built: 11,724 storefronts, 24 stations

- **The ninth build and the first outside the US.** 11,724 storefronts -
  Vancouver 8,133, Surrey 3,591 - across Retail 4,848, Food service 4,400 and
  Personal services 2,476, on 24 stations (20 Vancouver, 4 Surrey). 4,668 fall
  within the 0.6 mi outer ring. Per-step counts: Vancouver 58,346 current-year
  Issued -> 29,660 with coordinates -> 8,415 storefront; Surrey 27,082 ->
  13,066 Commercial/Industrial -> 3,654 storefront; 345 duplicate licences at
  one premises removed.
- **All three buckets are well covered in both cities**, so unlike New York and
  Boston there is no thin bucket to disclose. Both municipalities license
  general retail, which is what most large US cities do not.
- **The taxonomy is a dispatching module over two registries** - Vancouver's 89
  single-valued `businesstype` values and Surrey's 210 newline-separated
  `BusinessCategory` values, all 299 mapped with no unmapped value and no dead
  entry. Buckets were anchored on `naics.py` (Retail 44-45 less 454, Food
  service 722, Personal services 812 less 81293) rather than invented, so this
  city stays comparable with the five NAICS cities. Five judgment calls are
  recorded in the module: mobile trade excluded as nonstore (Vancouver's 116
  Street Vendor rows are the largest single sacrifice to that consistency);
  Surrey's 1,473 Inter-Municipal Business Licences excluded as its catch-all;
  BC-regulated health professions treated as health care while unregulated
  body-care counts; a funeral parlour counts and a cemetery does not; and
  NAICS 811 repair excluded throughout, so a hairdresser counts and a shoe
  repairer does not.
- **`businesssubtype` was tested as a disambiguator and REJECTED.** It looked
  like Chicago's `business_activity` and is empty on every row of the largest
  categories - all 4,544 Health Care, all 651 Retail Dealer - Food, all 116
  Street Vendor. It splits only Limited Service Food Establishment into
  With/Without Liquor, which changes no bucket.
- **THE BRIEF SAID VANCOUVER HAS NO STRUCTURAL NAME SIGNAL. IT HAS ONE.** The
  registry wraps a sole proprietor's own name in PARENTHESES -
  "(Christopher Colonia)", "(Qi Liu)" - on 4,383 of 29,660 mappable rows and
  750 of the storefront set. That is the City's own marking of an individual
  registrant, this city's equivalent of D.C.'s `ENTITYTYPE`, and it is used as
  the primary signal with `residence.looks_personal` unioned in because they
  catch different people: the parentheses find 63 storefront rows the regex
  misses (three-part and non-Anglo names), the regex finds ~10 registrants who
  did not use parentheses. `looks_organisational` vetoes both.
- **Only 88 pins display a business type instead of a name**, because 665 of
  the 750 parenthesised rows already carry a trade name. Every storefront
  stays on the map and no individual's name is published.
- **THE RESIDENCE FILTER DROPS NOTHING, AND THAT IS A MEASURED RESULT.** Built
  because `unittype` failed (see the earlier entry) and zoning was the only
  signal left. The two-hop join works as the brief promised - 99.9% of points
  inside a parcel, 99.7% reaching a zoning class. But the conjunction it was
  built to find - residential zoning AND a substituted personal name - leaves
  **1 row**: "Mcgill Groceries" at 2691 McGill St, a false positive of
  `looks_personal` (a surname followed by a word) and a real corner grocery.
  Meanwhile the 146 residentially-zoned storefronts are Restaurant 32, Limited
  Service Food 29, Retail Dealer - Food 25, Retail Dealer 23, Liquor
  Establishment 10 - Vancouver's legal non-conforming corner shops and
  neighbourhood restaurants. A zoning filter would have deleted them wholesale.
  **An intermediate version of step 2 did exactly that**, dropping 32 rows
  because it omitted the no-trade-name condition and so acted on trade names
  that merely looked personal. Caught by inspecting the rows instead of the
  count - the San Diego "42 pins became 315" lesson, arriving from the
  opposite direction. The join is kept because it is the measurement that
  JUSTIFIES not filtering; delete it and this becomes an assumption again.
- **Stanley Park is a hole in the local-area boundary layer.** A containment
  filter dropped 12 real storefronts - the Teahouse, Prospect Point, the
  Rowing Club, the Brew Pub, the Lawn Bowling Club and the Vancouver Aquarium -
  because the 22 local areas are neighbourhoods and none of them covers the
  park. The 118.8 km2 area check passes regardless. So the boundary is a CHECK
  here, not a filter, which is defensible independently: Vancouver's `city`
  column reads 'Vancouver' on all 29,660 mappable rows and Surrey's file is
  Surrey's own, so both registries are already scoped by their publishers.
  Miami uses its boundary the same way.
- **No cross-source dedup, deliberately.** The two registries cover disjoint
  municipalities, so no premises can appear in both; dedup is per source.
  Recorded because an absent dedup step is otherwise indistinguishable from a
  forgotten one.
- **Two lines needed a TUPLE of shape_ids.** The Canada Line branches for
  YVR-Airport and Richmond-Brighouse, the Expo Line for King George and
  Production Way-University, so the single most-used shape would have drawn one
  branch and silently dropped the other. Verified to cover every station on
  each line: Expo 24, Millennium 17, Canada 17.
- **No colour disclosure is needed, unlike D.C.** Official TransLink colours
  measured in both modes, dark first, as minimum CIE76 Delta-E from OSM's land
  and road fills with `map_common`'s own filter chains applied: Expo 98.0 dark
  / 99.6 light, Millennium 127.2 / 82.8, Canada 76.2 / **57.5**. The weakest is
  the Canada Line's teal in light mode, still 1.8x D.C.'s Silver Line at 31.4.
  **Caveat recorded rather than hidden:** this method reproduces D.C.'s
  published LIGHT figures exactly (Silver 31.4 land, darkened 51.0 land) but
  NOT its dark ones, whose model was never written down - offsets of +9.3,
  +9.1 and -10.2 on the three scale colours, so not a constant. Two sessions
  now cannot reproduce each other's dark numbers, which is an argument for the
  `check_colour_contrast.py` the retrospective dropped.

### 2026-09-21 - Vancouver privacy verdict: the shared check reads HIGH here, and why

- **`python scripts/check_personal_exposure.py vancouver`, run on the rendered
  map** (4,668 pins, 4,262 distinct names), as `CLAUDE.md` requires. Verdict:
  **publishable**, and the headline number it prints is an artifact.
- **It reports "PERSON-LIKE NAME AT A RESIDENTIAL UNIT: 314 of 4,668 pins
  (6.73%)" - higher than San Francisco's 217 and far above Philadelphia's 8.
  That figure should not be read as this project's other cities' are.** It
  counts an APT/UNIT/PH/SPC token in the address, and **Vancouver uses "Unit"
  as its generic designator for commercial suites**: 12,803 of 29,660 mappable
  rows say 'Unit' against **2** that say 'Apt'. So the token separates nothing
  here. This is San Diego's and Boston's measurement gap INVERTED - a false
  high rather than a false low - and it is the second time this check's address
  heuristic has been wrong about a city in a direction the city's own
  conventions explain.
- **The better measure exists for this city and was used instead:** the parcel
  zoning join. Of the storefront set, 146 sit on residentially-zoned land and
  exactly **1** of those has a substituted personal name - and that one is a
  false positive. That is the number this verdict rests on.
- **0 email addresses, 0 phone numbers, 0 "c/o" markers, 0 surname-first
  names** in any displayed name. `PhoneNumber` exists in Surrey's export and is
  dropped at load with an assertion that it stays absent; neither registry
  publishes a registrant-name column at all, so unlike New York there was
  nothing to omit at the download boundary.
- **The 30 names of the form "X (Y)" were inspected individually** - the check
  flags them as invisible to its heuristic. About 14 are a person's name
  registered as the TRADE name ("Mandy Y C Tsung (Mandy Tsung)", "Patricia
  Dawn Amey (Patricia Amey)", mostly Beauty Services) and about 16 are company
  names with a branch qualifier ("Regency Toyota (Vancouver)", "Sula Indian
  Restaurant (Main St)"). The first group is left as published on **San
  Diego's precedent**: a trade name the owner chose to register under their own
  name is a deliberate public commercial act, not a fallback this pipeline
  substituted. No change made; recorded so a future reader has the verdict
  rather than the flag.
- **`scripts/check_personal_exposure.py` gained a per-registry `sep`**, because
  Opendatasoft exports semicolon-delimited CSV and `read_csv`'s default comma
  parsed Vancouver's raw file as a single column.

### 2026-09-21 - The Canada ranking table is not internally comparable

- **Found while building Vancouver, and it affects which city is built next,
  so it is recorded separately from the build.** `docs/canada_step0_endpoints.md`
  ranks the six Canadian candidates on "businesses within the outermost 0.6 mi
  ring, divided by in-city stations": Vancouver 861, Surrey 549, Montreal 252,
  Edmonton 153, Calgary 103, **Toronto 41**. Only Toronto's is labelled
  "41 **storefront**".
- **That label is the whole problem: Toronto's number is storefront-filtered
  and the other five are not.** Re-measured on the built pipeline, Vancouver's
  ring holds **17,233 of all mappable licences across its 20 stations = 862 per
  station**, which reproduces the brief's 861 to within one. On the
  **storefront** set - the same basis as D.C.'s ~173 and Boston's ~39 - it is
  **206 per station**. The published figure was inflated **4.2x** by counting
  licences this project never maps: rentals, contractors, consultants, offices.
- **Surrey moves much further.** Its published 549 becomes **135 per station**
  on the storefront set, so it sits BELOW D.C. rather than second in the
  country. Its 4 stations reach only 15% of its own storefronts, against
  Vancouver's 51% - Surrey's commerce is spread along arterials the SkyTrain
  does not follow.
- **Vancouver's ranking survives; the margin does not.** At 206 it is still the
  densest storefront city in this project, ahead of D.C.'s ~173 - so the
  decision to build it first was right, for a reason 4x weaker than stated.
- **What this does NOT establish: that Toronto is the weakest.** Toronto's 41
  was already storefront-filtered, so it was being compared against five
  numbers roughly 4x too large. On a common basis the gap narrows
  substantially, and the profile's conclusion that "the largest city came last"
  rests on a comparison that was never like-for-like. **The remaining Canadian
  cities should be re-ranked on storefront counts before the next one is
  chosen.** Left for the session that owns `docs/` rather than edited here;
  noted in `PLAN.md`.
- **The cause is the denominator rule this project already wrote down** after
  D.C. (see the `add-city` amendment of 2026-09-21: "every percentage Step 0
  records must name the set it was measured on, and that set must be the one
  that reaches the map"). The rule was about percentages; this is a rate, and
  it went wrong the same way. The rule should say "every percentage OR RATE".

### 2026-09-21 - Vancouver Step 0 verified: six claims held, five were wrong

- **The build brief's ASSERTED claims were re-measured rather than trusted,
  per `session_roles.md`.** Six reproduced exactly: `folderyear='26'` is still
  the current vintage (73,075 rows against 69,889 for '25'), 58,346 current-year
  Issued, 29,660 with coordinates, 63.0% trade-name blank, the 22 local-area
  polygons dissolving to ONE Polygon of 118.8 km2, and **20 in-city stations** -
  a count the brief held but a list it had never written down. Surrey's leg
  reproduced to the unit: 27,082 rows, 628 naive categories against 210 true
  distinct on `\n`, 13,066 Commercial/Industrial, and **1,444 of those within
  0.6 mi of its 4 stations - 361 per station**.
- **Five were wrong, and two of them would have changed the pipeline.**
  - **TransLink's feed DOES carry `feed_info.txt`** - `feed_start_date`
    20260907, `feed_end_date` **20270103**, version `26SEP_20260918`. The brief
    said it carries none, so the city "declares no expiry". It has a 118-day
    validity window, so D.C.'s `feed_end_date` check applies here too. The
    brief's claim was almost certainly measured on the Mobility Database
    mirror; the agency's own feed has the file. **This is the Toronto stale-
    mirror lesson recurring in a new form** - not staleness this time, but a
    mirror missing a file the source has. The "declares no licence of its own"
    half stands: there is no `feed_license` column.
  - **`zoning_classification` has been re-coded and the brief's values no
    longer exist.** It recorded One-Family Dwelling 202,740, Two-Family
    Dwelling 48,300, Multiple Dwelling 87,557, Commercial 132,576. On
    `report_year='2026'` the classes are Comprehensive Development 84,292,
    Residential Inclusive 65,706, Residential 51,152, Commercial 19,782,
    Industrial 5,122, Historical Area 2,621. The old labels are Vancouver's
    pre-2024 scheme, and the brief's counts were taken across all seven years
    in the file at once - **the D.C. denominator error, in a new place.** Every
    residence-filter number derived from them has to be re-measured.
  - **89 `businesstype` values reach the map, not 93.** 93 is the whole-dataset
    count; 89 is the count on current-year Issued rows with coordinates, which
    is the set that gets bucketed.
  - **Trade-name blank is 49.6% on mappable rows, not 63.0%.** The 63%
    includes the rentals and contractors that carry no coordinates and are
    excluded anyway. Same denominator lesson, on the number the brief calls its
    largest open decision.
  - **54 stations system-wide, not 53.** Capstan, in Richmond, is the extra - a
    recent Canada Line addition.
- **Two facts the brief did not carry, both load-bearing.** Surrey's `x`/`y`
  arrive only in the CSV export (the layer's attribute schema has neither) and
  are **EPSG:26910 metres**, the service's native SR - reading them as degrees
  would place Surrey in the Gulf of Guinea. And `route_short_name` is **empty
  on all three rail lines**, so routes must be matched by `route_id`; the
  public names live in `route_long_name`.
- **The boundary CRS trap the brief warns about is avoidable, not inevitable.**
  Querying Surrey's FeatureServer with `f=geojson` returns real degrees
  (-122.96..-122.68, 49.00..49.22), correctly reprojected from its native
  EPSG:26910. The declared-4326-containing-UTM-metres problem belongs to the
  Hub's *file* export, not the service, so this build reads the service and
  needs no `set_crs(..., allow_override=True)` anywhere.
- **The 34 excluded stations were named from a boundary layer, not guessed**
  (`add-city` Step 4): Burnaby 11, Richmond 8, New Westminster 5, Coquitlam 4,
  Surrey 4, Port Moody 2, via the BC ABMS municipalities layer. That WFS
  returned zero features until its bbox was given in **lat,lon** order - a
  `urn:ogc:def:crs:EPSG::4326` CRS means axis order is the authority's, not
  lon,lat.
- **SkyTrain needs no sub-transit-line filters.** It is fully grade-separated
  with no street-running stops, so all 20 in-city stations are kept - the same
  verdict as D.C. and for the same reason. Downtown spacing is tight (median
  nearest-neighbour 841 m, minimum 201 m between Granville and Vancouver City
  Centre, 17 of 20 inside the 965 m outer ring), so rings overlap visibly;
  nearest-station assignment means nothing is double-counted.

### 2026-09-21 - Vancouver is built at REGIONAL scope, with Surrey

- **The owner's call, taking the Miami precedent deliberately** - "let's attempt
  2 since we built the infrastructure to accommodate it. if we run into trouble
  we can rescope to 1". Surrey has no rail of its own, shares SkyTrain and
  therefore shares one TransLink licence, and contributes 4 stations at 361
  Commercial/Industrial sites each.
- **But it is a harder case than Miami, and the difference matters.**
  Miami-Dade publishes all 34 of its municipalities in ONE file, with one
  schema, one publisher and one set of terms, so its regional map needed no
  extra source, no cross-source dedup and no second licence review. Vancouver
  and Surrey are **two publishers, two schemas and two licences** - the
  `multi-source-city` shape applied across municipalities rather than across
  buckets.
- **Cross-source dedup is nevertheless unnecessary, which is the one way this
  is easier than New York.** The two registries cover disjoint municipalities,
  so no premises can appear in both. Dedup is per-source only. Recorded because
  the absence of a dedup step is otherwise indistinguishable from a forgotten
  one.
- **The page is labelled "Vancouver (Regional)"**, on Miami's reasoning: a map
  spanning two municipalities cannot honestly be called Vancouver. The slug
  and directory stay `vancouver`.
- **Both licences' notices are required, and their wording is not
  interchangeable.** Vancouver's is `Contains information licensed under the
  Open Government Licence - Vancouver.` (en dash, British "Licence"); Surrey's
  is `Contains information licensed under the Open Government License - City of
  Surrey.` (hyphen, American "License"). Both terminate automatically on
  breach, as does Toronto's and Calgary's. The TransLink Legend is inherited
  once, in its **GTFS** wording, and the position that no prior contact is
  required was already recorded earlier today.
- **The rescope path is kept open.** Surrey enters through a `SOURCES` table
  and its own taxonomy branch, so dropping back to Vancouver alone means
  removing one table entry and one boundary, not unpicking the pipeline.

### 2026-09-21 - A blank trade name yields a neutral label, never a person's name

- **The owner's call on the brief's largest open question.** Vancouver's
  `businesstradename` is blank on 49.6% of mappable rows, so the pin label
  falls back to `businessname` - which for a sole proprietor IS a person's
  name. Los Angeles met this at 68% and answered by excluding the category
  driving it; D.C. answered with a structural `ENTITYTYPE` signal. **Vancouver
  has neither**, so the answer is at the label: fall back to the legal name,
  but where that name matches `residence.looks_personal`, display the row's
  business type instead. Every storefront stays on the map; no individual's
  name is published.
- **Rejected: always falling back to the legal name** (what LA declined, and
  it would publish thousands of individuals at their premises); **showing the
  business type for every blank trade name** (discards real information on
  about half of mappable pins, including firms that simply registered under
  their legal name); and **dropping pins with no trade name** (loses ~50% of
  the mappable set and biases the density map wherever registering under a
  legal name is common).
- **`unittype` was tested as a second signal and REJECTED.** It looked like
  NYC's `unit_type`, which separates APT from STE and FL. Vancouver's is 'Unit'
  on 12,803 of 29,660 rows - one generic designator covering strip-mall suites,
  office floors and flats alike - against 'Apt' on **2**. It cannot separate a
  dwelling from a commercial unit, which is San Diego's measurement-gap result
  rather than a clean one. **So zoning is Vancouver's only residence signal**,
  and that is the justification for building the two-hop parcel join rather
  than treating it as optional.
- **The registry helps here in one structural way worth recording**: it
  publishes no registrant-name column at all. `businessname` and
  `businesstradename` are the only name fields, so unlike New York there is no
  column to omit at the download boundary - the exposure is confined to sole
  proprietors registering under their own name, which is exactly what the
  person-pattern check addresses.
### 2026-09-21 - The scaling ceiling, measured: 20-25 cities, and storage is not the limit

- **The previously recorded ceiling was wrong by about 3x, and it was an
  estimate presented as a finding.** `docs/scaling_thresholds.md` had put
  `outputs/` in git as "the real ceiling" at ~20 cities, on an assumed 3-10 MB
  per city. Measured across all nine built cities: **19 MB total, mean 2.1 MB,
  median 1.2 MB** - New York 7.4 MB (itself down from 10.3 MB since the
  coordinate-rounding lever was applied), Los Angeles 2.7, Chicago 2.2, San
  Francisco 1.7, Miami 1.2, Philadelphia 1.1, Washington D.C. 0.7, San Diego
  0.7, Boston 0.5. History growth measured too: **32 of 108 commits touch
  `outputs/`**, about 3.5 per city, and Folium HTML compresses roughly 3-5x.
  Projected at 50 cities that is ~75-125 MB packed against GitHub's 1 GB soft
  limit - **about 8x headroom, reached somewhere past 150 cities**, which the
  research process will never approach.
- **The owner's stated allowance: 20-25 cities as the planning ceiling, ~40 as
  the architectural line.** Nothing in the stack forces 20-25; it is set by the
  Overview macro map and by research cost per city. Past ~40, Streamlit
  Community Cloud's ~1 GB memory, sleep-on-inactivity and repo-clone time on
  deploy start arguing for vector tiles rather than per-city static HTML, which
  would revisit the pre-rendered-HTML invariant itself. Rejected: treating
  storage as the governing limit, which the measurements do not support.
- **Per-page weight does not scale with city count and this keeps being the
  wrong worry.** Each page embeds exactly one city's map, so a visitor's cost
  is bounded by the largest city, not by how many exist. A 50-city site loads
  identically to this nine-city one.
- **The macro map's answer is to stop fitting the whole world.** Decided: open
  on a default region rather than a fitted global view, and make global
  coverage obvious in the UI. This supersedes the earlier suggestion of
  clustering markers, which does not help once the map spans continents - and
  it follows the arithmetic recorded the same day showing displacement is
  impossible at continental zoom (1 px is ~21.7 km; separating New York from
  Philadelphia would need 217 km). Two conditions attach: the other regions
  must be visible at a glance, and the default must **not** be a geolocated
  per-visitor guess, which would add a privacy surface for no benefit.

### 2026-09-21 - The tenth city had nowhere to go, behind a "verified not a problem"

- **`app/pages/` had no free slot for city ten, and the earlier all-clear
  concealed it.** A 2026-09-21 entry recorded that `10_*.py` does *not* sort
  before `2_*.py` - true, verified against Streamlit's `page_sort_key`, and it
  answered the wrong question. The two info pages **occupied** `10_` and `11_`,
  while `scripts/scaffold_city.py`'s `next_page_number()` globs `*_Heatmap.py`
  only and so never counted them. At nine cities it would have generated
  `10_<Name>_Heatmap.py` directly into `10_About_the_Data.py`'s slot.
- **Fixed by renumbering the info pages to 90 and 91**, leaving 10-89 free for
  cities and keeping them last in the sidebar, which is where they belong.
  `next_page_number()` needed no change. `app/components.py`'s
  `ABOUT_DATA_PAGE` and `EXCLUSIONS_PAGE` were updated with it, and the
  docstring cross-reference in `91_What_Is_Excluded.py`. Rejected:
  zero-padding the city pages, which solves a sort problem that does not
  exist.
- **The lesson, which is the reason this is logged separately:** "verified NOT
  a problem" was accurate about the question asked and hid a real defect one
  layer down. A negative result answers only the question actually put to it.

### 2026-09-21 - Macro-map markers shrunk; displacing them is arithmetically dead

- **The last item in the deferred macro-map pass, and the only one that was
  still genuinely open.** The label half was fixed earlier the same day (11
  collisions to 0) and the clicking half was fixed by making the name pills
  pickable. What remained was purely visual: at the fitted continental zoom the
  eastern dots merged into one teal blob.
- **Radius 6 with a 2 px ring becomes radius 4 with a 1 px ring** - outer
  diameter 16 px down to 10 px. That separates New York/Boston and New
  York/Washington D.C. outright and cuts the worst overlap, New
  York/Philadelphia, from 10 px to 4 px, so the cluster reads as distinct dots
  instead of a smear. Verified by screenshot at 1000 px.
- **Radius 3 was tried and rejected.** It separates one more pair
  (Philadelphia/D.C.) but the dots stop functioning as position indicators -
  for the isolated cities they read as specks. The measured separations are
  unchanged by width, because `fit_view` pins the zoom to a 320 px reference
  and spends extra screen width as margin: New York/Philadelphia 6.0 px,
  Philadelphia/D.C. 9.0 px, New York/Boston 14.4 px, New York/D.C. 15.0 px,
  San Diego/Los Angeles 7.7 px, identical at 340 px and 1200 px.
- **MOVING THE MARKERS IS ARITHMETICALLY IMPOSSIBLE, and this is the number
  worth keeping.** At the fitted zoom the world is 1,401 px wide, so 1 px is
  0.257 degrees of longitude - about **21.7 km** at New York's latitude.
  Separating New York from Philadelphia would therefore need **217 km** of
  displacement, putting New York's dot west of Pittsburgh. Philadelphia/D.C.
  would need 152 km and San Diego/Los Angeles 180 km. Dot displacement is a
  real cartographic technique and it is simply not available at a continental
  zoom. Recorded in `app/Overview.py` beside the radius so the idea is not
  revived.
- **A note on how this came up, because the misremembering is instructive.**
  The owner asked to tackle the marker overlap believing it had already been
  solved "when we moved east coast coordinates to atlantic ocean". Nothing was
  ever moved into the Atlantic: that was a proposal about where to put the
  *labels*, withdrawn the same day because the Atlantic space only exists at
  desktop width (315 px there against 58 px on a phone). What shipped was
  labels placed 14 px EAST of their own dots, and the markers were never
  touched - as the report at the time said: "five marker overlaps remain that
  labels can't fix". Two adjacent decisions about the same cluster, one
  adopted and one withdrawn, are easy to merge in memory; the arithmetic above
  is the durable answer either way.
- **Clicking re-verified after shrinking**, because a smaller dot is a smaller
  target: San Francisco's 4 px dot still opens its page, and Boston's name pill
  still opens Boston. The pills remain the reliable target inside the cluster,
  which is why shrinking the dots costs nothing functionally.

### 2026-09-21 - Concurrent sessions split by role and by path, not by window

- **Two sessions sharing one working tree was ended in favour of a worktree
  per session.** The shared tree had a measurable cost: commit `38d4bd0` swept
  one session's uncommitted work in via a broad `git add -A`, every commit
  needed explicit-path staging plus an authorship check on each diff, and work
  was held at least five times waiting for a build or deploy to land. Each
  non-primary session now takes `.claude/worktrees/<role>` on its own branch
  and merges at natural boundaries. Git refuses to check out `master` twice,
  so the branch is forced - and that is the gain, since the merge becomes an
  explicit review step instead of an implicit race. Rejected: keeping one tree
  and relying on discipline, which is what had just failed.
- **Roles are claimed, not assigned to a window, and ownership is by PATH.**
  A session declares its role in its first message and gains a path set -
  staging/research owns `docs/`, `.claude/skills/` and screening `scripts/`;
  a build session owns `pipeline/<city>/`, `outputs/<city>/` and that city's
  app page and taxonomy module; an app/chrome session owns `app/`,
  `map_common.py` and `theme.py`. Path ownership was chosen over naming
  specific windows because it survives a restart and scales: two build
  sessions can run concurrently provided they hold different cities.
  `DECISIONS.md`, `PLAN.md` and `CLAUDE.md` stay unowned and append-only, so
  same-day conflicts resolve as "keep both" - a visible conflict being a
  better failure than the silent overwrite the shared tree produced.
- **Written so a single session ignores all of it.** `docs/session_roles.md`
  opens with the solo case, because the real risk in a process document of
  this kind is that a lone session reads a coordination convention as a
  capability limit and stalls waiting for a staging session that does not
  exist. For the same reason a build brief is defined as a cache of Step 0,
  never a prerequisite.
- **Claims handed between sessions are now labelled MEASURED or ASSERTED.**
  The Canada screen reversed five conclusions, every one of them asserted from
  a column's existence, a dataset title or a plausible-looking flag rather
  than measured, and a receiving session cannot tell the two apart by reading.
  MEASURED carries a number and the check that produced it; ASSERTED is
  verified before being built on. An open-questions section is mandatory in a
  handoff - a brief with no unknowns listed is one that has not been audited.
- **`docs/build_briefs/vancouver.md` is the first instance**, handing the
  densest city measured in this project (861 sites/station) to a build
  session: scaffold arguments settled, all three endpoints with their traps,
  EPSG:32610, the rejected address join (6.5%) against the two-hop spatial
  join that works (99.9%), the rejected STRATA refinement, both required
  notices with exact wording, and seven open questions - of which the
  trade-name fallback (blank on 63%, person-pattern 16.94% on storefront
  types) is flagged as the largest and as an owner decision rather than a
  build one. Files: `docs/session_roles.md`, `docs/build_briefs/vancouver.md`,
  `CLAUDE.md`, `.gitignore`.

### 2026-09-21 - Philadelphia: ask for permission, stay up on a reasoned position meanwhile

- **The owner's decision**, taken after reading the prohibition in the City's
  incorporated Terms of Use: **ask the City for written permission, and keep
  the Philadelphia map live under a reasoned position while that is
  outstanding.** Both halves matter, and the second is only defensible because
  of the first and because the footer already discloses the question.
- **The reasoned position, stated so it can be judged rather than assumed.**
  The "City of Philadelphia License" is the dataset-specific instrument and
  contains no prohibition on reuse. The phila.gov Terms of Use, which the
  dataset page incorporates by reference, are drafted from beginning to end for
  web pages: they permit residents "to copy electronically and to print single
  pages from the Website" and require that pages be shared "exactly as
  presented on the Website". That language cannot sensibly be applied to a CSV
  or a GeoJSON feed, and the prohibition sits in the same paragraph as the
  permission it qualifies. Alongside it: the City Limits dataset is marked
  "Usage: Public use; Free", and the Open Data Program was established by
  executive order in 2012 for public reuse. **On that reading the dataset
  licence governs and the map is permitted.**
- **What makes this a position rather than a conclusion.** It is a reading of
  an ambiguous instrument, reached by the party that benefits from it. The
  project does not claim the City agrees, does not claim a request is
  outstanding until one is sent, and does not treat silence as consent. The
  footer names Philadelphia, quotes the prohibition, and says the question "has
  not been resolved in this project's favour" - which stays true under this
  position.
- **The request is drafted but NOT SENT**, at
  `docs/licenses/phila-permission-request.md`. It goes to `ligisteam@phila.gov`,
  the maintainer contact on the L&I Business Licenses dataset, and asks the two
  questions that actually decide it: whether the phila.gov Terms of Use apply
  to OpenDataPhilly datasets at all, and if they do, whether the City will
  permit this non-commercial use in writing. It describes exactly what the
  project does with the data - filters, classifies, drops non-storefronts,
  publishes a derived map with trade names at mapped locations, commits the
  generated output to a public repository - because a permission granted
  against a vague description would be worth little. It commits in the letter
  itself to removing Philadelphia promptly if the answer is no.
  Drafted with placeholders rather than the owner's name, email and links:
  those are the owner's to fill in, and this file is in a public repository.
- **Sending it is the owner's to do, not this project's.** Correspondence on
  someone's behalf is theirs to send.
- **What happens on each reply is written down in advance**, in that same file,
  so the answer does not have to be re-litigated under time pressure: on
  permission, the footer clause loses its only live subject and comes out
  entirely; on refusal, Philadelphia's page, `cities.py` entry,
  `outputs/philadelphia/` and macro-map marker all go, and the remaining
  eastern cities' label offsets need re-checking at 854 and 1200 px because
  removing a marker moves `fit_view`'s bounds.

### 2026-09-21 - The three licence questions, read: two close, one gets worse

- **The framing they were recorded under was wrong, and that is the finding.**
  All three had been grouped as "what does silence mean?" - sources that
  neither grant nor forbid - with the summary "nothing found in any of the
  three forbids what this project does. These are questions about the absence
  of permission, not about a prohibition." Reading the actual documents
  settled two and inverted the third.
- **SEPTA: CLOSED, and it was never a silence question at all.** Its licence
  expressly grants "a non-exclusive, non-assignable, non-transferable, limited
  and revocable right to **use, reproduce and redistribute** the datasets".
  The dataset was licensed all along; the open question was only ever about the
  trademark sentence beside it, "Licensee may not use SEPTA's trademarks and
  copyrighted materials for any commercial or profit-making use". That sentence
  points at SEPTA's Copyright and Trademark Notice, which **had never been
  read**. Its entire Trademark Notice is one sentence: "**The SEPTA Logo** is a
  registered trademark of featured words or symbols, used to identify the
  source of its goods and services." Line names are not claimed. Route colours
  are not claimed. This project reproduces no logo, so the clause has nothing
  to bite on, and the fallback held in reserve - swap in an own palette and
  descriptive names - is recorded as considered and unnecessary.
  The "informational and non-commercial purposes only" wording that had made
  the portfolio-site question look live turns out to sit in the same notice's
  "Web Contents and Materials" section, scoped to "documents and related
  graphics from this ... Server" - septa.org's own pages. **It never reached
  the datasets.** Exactly the distinction NYC taught, where the nyc.gov "All
  Rights Reserved" footer covered the website and not the open data.
- **Miami-Dade: CLOSED by reading, not by asking - and the note saying that
  was impossible was wrong.** This project had recorded Miami-Dade as "the
  only one of the three where no agency document exists to read, so settling it
  likely means asking the County". A document does exist: the Open Data Hub's
  own designated Terms of Use at
  `opendata.miamidade.gov/pages/terms-of-use`, reachable in two clicks from the
  portal footer. Its entire substance is the accuracy disclaimer. The
  county-wide "Liability Disclaimer and User Agreement" was read too and is
  liability terms only, with no copyright claim and no reuse restriction. So
  **three County documents now say nothing whatever about reuse,
  redistribution, modification or attribution** - which is a definitive
  absence of restriction from the County's authoritative pages rather than an
  unexamined gap, and a materially stronger position than "we could not find
  anything". No enquiry to the County is needed.
- **PHILADELPHIA: NOT CLOSED, AND IT IS NOW A PROHIBITION QUESTION RATHER THAN
  A SILENCE ONE.** The "City of Philadelphia License" still grants nothing and
  forbids nothing. What had not been read is the sentence its dataset page
  opens with: "Browsing City data on this site constitutes acceptance of the
  license, **the City's terms of use** and your agreement to be bound by
  them." That incorporates `phila.gov/terms-of-use` by reference, and those
  terms are emphatically not silent. They grant permission only "to residents
  and citizens of the City of Philadelphia to copy electronically and to print
  single pages from the Website ... exactly as presented on the Website,
  without any addition or modification", and then state: "**Distribution or
  republication in any other form or for any other purpose, including any
  commercial purpose or use, and any modification whatsoever, are strictly
  prohibited without the prior written permission of the City.**" A separate
  sentence adds "Commercial use is prohibited without the prior written
  permission of the City."
  Read literally and applied to the datasets, **that does not permit this
  project's Philadelphia map**, which filters the register and redraws it -
  modification and republication both. The contrary reading is strong but it
  is a reading, not a grant: the terms are drafted throughout for web pages
  ("print single pages", "exactly as presented on the Website"); the
  dataset-specific licence beside them contains no such prohibition; the
  boundary dataset is marked "Usage: Public use; Free"; and the Open Data
  Program was established by executive order in 2012 for public reuse.
- **The site's own neutrality statement was corrected the same day, because it
  had become false.** `components._UNSETTLED_TERMS` said "Nothing found in any
  of them forbids what these maps show" and named Miami-Dade and Philadelphia
  as a matched pair. It now names Philadelphia alone, quotes the prohibition,
  says plainly that the question "has not been resolved in this project's
  favour", and keeps the commitment: if the City confirms the restrictive
  reading, Philadelphia comes off the site. Leaving the old wording up would
  have been a false claim on a live public page - which is why this was fixed
  before anything else, rather than waiting on a decision.
- **Three ways forward on Philadelphia, all the owner's to choose:** ask the
  City for written permission, which its own terms name as the route; remove
  Philadelphia; or record a reasoned position that the dataset licence governs
  and accept the residual. Recorded as open in `PLAN.md`, with SEPTA's and
  Miami-Dade's sub-items closed.
- **The general lesson, which has now cost three separate corrections in this
  project:** a dataset's terms are not the publishing body's website terms, and
  neither is necessarily the whole instrument. NYC's licence turned out to be
  forbidden by statute; SEPTA's "non-commercial" wording turned out to belong
  to its website; Philadelphia's dataset page turned out to incorporate a
  second document by reference. **Follow every pointer a licence makes before
  calling the position established** - all three of these were resolved by
  opening a page the earlier review had merely cited.

### 2026-09-21 - Canada screened end to end: six viable cities, and the largest is the weakest

Screened in parallel with the Boston, D.C. and deploy work, writing only to
`docs/licenses/` and `docs/canada_step0_endpoints.md` so nothing collided. No
Canadian city is built; this is Step 0 evidence, not a build.

- **Rail first, and it removed 6 of 13 before a catalogue was opened.** The
  order matters: rail is the cheapest disqualifier, so a city with no urban
  rail is out however good its registry is. Out on rail, live-verified from
  each agency's own `routes.txt`: Winnipeg, Hamilton, Quebec City, Halifax,
  **Mississauga and Brampton**. The last two matter because Miami's regional
  precedent does *not* rescue them - Metrorail physically extends into Hialeah,
  whereas TTC Line 2 stops at Kipling inside Toronto and the only rail reaching
  Brampton is GO commuter rail, excluded everywhere. Brampton's data is
  excellent (6,059 businesses, NAICS on 97.3%, X/Y on 100%) and unusable until
  the Hurontario LRT opens; recorded in `docs/city_shortlist.md` with a
  mid-2027 revisit asking "has an opening date been announced?" rather than "is
  it open?".
- **Montreal was nearly lost to a keyword filter, and is the best-documented
  source in the project.** A keyword scan of the full 447-package list
  concluded "food-only". Wrong: **`locaux-commerciaux`** contains none of the
  words *business*, *licence*, *permis*, *entreprise* or *commerce*. It is an
  agglomeration-wide field survey of street-level commerce - 28,621 premises,
  **100% coordinates**, `NOM_ETAB` 100%, **`SCIAN` (NAICS) 99.6%**, plus a
  vacancy flag - and it passes the exact coverage test Boston's survey failed:
  **441 occupied 0.01-degree cells against Boston's 37**, with Ville-Marie at
  4,316 premises and Senneville at 1. Nobody surveys a village of 900 as part
  of a sample. The rule that followed is now in `add-city` Step 0: read a new
  city's whole catalogue, never grep it.
- **Station density decided the ranking, as it did for D.C. against Boston.**
  Sites within the outermost ring per in-city station: **Vancouver 861**
  (the densest measured anywhere in this project), **Surrey 549**, **Montreal
  252**, **Edmonton 153**, **Calgary 103**, **Toronto 41**. Vancouver keeps only
  20 of 53 stations in-city - 38%, which looks alarming and is the least
  interesting number, exactly as with D.C.
- **Toronto is the weakest of the six despite being the largest, and that is
  worth stating before anyone picks it on population.** After geocoding, 41
  storefront sites per station - Boston's 39 - because **it is a two-bucket
  city**: within a ring, Food service 7,249, Personal services 1,973, **Retail
  357**. Toronto licenses food, personal services and specific trades, not
  general retail; its biggest categories are Taxicab Owner 4,212, Public Garage
  3,023, Building Renovator 1,461.
- **No Canadian geocoder is needed, and only one city needed geocoding at
  all.** Montreal, Surrey and Calgary are 100% coordinates; Edmonton has 111
  rows with an address and no coordinates (its 47% "missing" are placeholders -
  `<Home Based Business>` 14,114, `<REDACTED FOR PRIVACY>` 4,074,
  `<Non-Resident Business>` 2,108); Vancouver has 1,583, the rest having no
  address either and being rentals and contractors this project excludes.
  Toronto has none, and is solved by **a local join against the City's own
  525,440-point address repository - 71.4% on exact match with no street
  normalisation**, which also returns `MUNICIPALITY_NAME` and so doubles as the
  in-city filter.

### 2026-09-21 - A stale catalogue mirror produced a false finding about Toronto

- **The claim "Toronto codes its subway as `route_type 0`" was wrong, and it
  reached three files before it was caught.** `scripts/screen_rail.py`, the
  `add-city` skill and `docs/city_shortlist.md` all carried it; all three are
  corrected.
- **The cause is worse than a misreading.** The Mobility Database mirror of the
  TTC feed had `feed_end_date 20260606` - **three months expired** when read on
  2026-09-21 - and contained **no subway at all**: 209 bus, 17 tram, 2 ferry,
  zero `route_type 1`, the only subway-named entries being shuttle *buses*. The
  17 trams are the streetcars. The agency's own feed, from Toronto's CKAN
  package `ttc-routes-and-schedules`, has **3 subway lines as `route_type 1`**
  plus **Line 5 Eglinton and Line 6 Finch West** LRT among 20 type-0 routes.
  Toronto's system is richer than the screen said and separating rail from
  streetcar is trivial.
- **`screen_rail.py` now reads `feed_info.txt` and flags expiry**, printing
  `[FEED EXPIRED yyyymmdd]` per feed and a `STALE FEEDS` block at the end.
  Verified against the feed that caused this: it fires on Toronto's mirror and
  stays silent on Calgary's live one. **A mirror can be missing an entire mode
  and the screen had no way to tell** - that is the lesson, not the date.

### 2026-09-21 - Montreal will be built at AGGLOMERATION scope

- **The owner's call, and the first argument for it was wrong.** The initial
  case - that the Metro "serves Westmount and Mont-Royal directly", so city
  scope would strand stations whose commerce was filtered away - is false on
  its facts. **Westmount has no Metro station**; Mont-Royal has one. Measured:
  63 of 68 stations sit in arrondissements, 1 in a ville liee (Acadie), and 4
  outside the agglomeration entirely (three in Laval, one in Longueuil, which
  are excluded under *either* scope).
- **The real argument is the reverse of the first, and it survives.** Buffering
  every in-agglomeration station by the 0.6 mi ring, **659 of the 2,827
  linked-city premises (23.3%) fall inside a ring drawn around Montreal's own
  stations** - Westmount 399, Mont-Royal 214, Cote-Saint-Luc 46. The failure is
  not stations outside the city; it is **commerce immediately across the city
  line sitting inside rings drawn from stations inside it**. City scope would
  cut a visible hole beside Atwater, Vendome and Guy-Concordia while keeping
  the stations, which reads as a bug rather than a scope choice.
- **Cost, stated plainly:** the city page must say it maps the agglomeration,
  not the city. Miami is the precedent. The three Laval stations are a second,
  larger regional question left open behind this one.

### 2026-09-21 - TransLink's static GTFS terms read as not requiring prior approval

- **The owner's stated position, in the same family as LA Metro's modification
  clause and CTA's purpose limitation**, both decided the same way earlier.
  TransLink publishes the static GTFS under a **different document** from its
  Open API terms. The API terms gate on "In the event that TransLink, **in its
  entire discretion**, approves you as a user of the Data" - the GTFS terms
  have no counterpart to that sentence, no API key, no 1,000-requests-per-day
  cap and no ten-day termination clause. Their information obligation - "You
  must provide TransLink sufficient information as TransLink may request" -
  reads as responsive to a request, not a precondition of use. **Decided: no
  prior contact is required**; contacting them would be a courtesy, not a gate.
- **Three obligations if Vancouver or Surrey is built**, and one is a trap: the
  Legend must use the **GTFS wording** ("Route and arrival data used in this
  product or service...") and **not** the API wording ("Some of the data..."),
  which would not satisfy these terms. Plus no TransLink marks beyond that
  legend, and responsiveness if asked. Surrey inherits all three, having no
  rail of its own - one regional build, one Legend.

### 2026-09-21 - Concentric rings start switched OFF for every city

- **The owner's call, for a cleaner first view.** `map_common.render_heatmap`'s
  `rings_shown` default flips from True to False, so all nine maps now open
  without the four ring layers drawn. They stay in the layer control, one click
  away, and every city page still says so.
- **Nothing about the numbers changes.** Each business is assigned to its
  NEAREST station regardless of what the rings display, so the within-ring
  counts, the per-bucket totals and the "all businesses" toggle are all
  identical - the within-ring figures in every step's output are unchanged
  after the re-render, which is the check that confirms it.
- **It generalised two per-city exceptions into the default, and that is the
  interesting part.** New York and Miami already passed `rings_shown=False` on
  measured grounds: New York's 496 stations sit a median 482 m apart and
  Miami's nineteen Metromover stations a median 235 m, so in both the rings
  merged into one indistinct wash downtown. Every city has a downtown cluster
  that does some of this - Washington D.C. has 20 of 40 stations closer to a
  neighbour than the 966 m outer ring, Boston kept its rings only because the
  Green Line was thinned first - so what looked like two special cases was
  really the general one. The two explicit overrides are now removed as
  redundant, with their measurements kept as comments because they are why the
  toggle exists at all.
- **Two city pages described rings-off as a local quirk and were wrong after
  this.** New York's said "The station rings are smaller here, and start
  switched off" and Miami's "The concentric rings start switched off, which is
  unusual here." Both reworded: New York's now leads on the rings being
  SMALLER (0.3 mi rather than 0.6), which is still true and still unique to it,
  and Miami's on the rings being worth turning on selectively, since its
  Metrorail corridor reads cleanly with them while its Metromover loops do not.
- **Verified after re-rendering all nine:** each map's layer control lists four
  `Concentric Ring` entries and every one is unchecked on load, while the heat
  layer, the within-station density layer and the three business-category
  layers stay checked. The label checker reports an empty `problems` list on
  New York, Chicago, Boston and Washington D.C. at 854px, so the re-render did
  not disturb line-label placement.

### 2026-09-21 - Code licence, and disclosing the unsettled licence positions on the page

- **The code is MIT; the data explicitly is not.** `LICENSE` carries the MIT
  text verbatim, then a separate scope section - kept separate so the licence
  body is unmodified - stating what the grant does NOT cover. This mattered:
  a bare MIT file at the repo root would have purported to license the 19 MB
  of third-party-derived content in `outputs/`, which this project cannot
  sublicense. WMATA prohibits redistributing its transit data to third
  parties, LA Metro forbids modifying its data, and the business records come
  from registers whose terms run from CC0 to a licence that reserves every
  right. The carve-out names the three categories of embedded material
  (redrawn `shapes.txt` geometry, station names and positions, business trade
  names and coordinates) and points at `docs/data_sources.md` for terms and
  `docs/excluded_categories.md` for the modifications half that some of those
  terms require a re-publisher to state. Copyright line: `dacekroberts`, the
  identity this project commits under; flagged to the owner in case a legal
  name is preferred.
- **The deployed URL is a marked placeholder, not an omission.** Streamlit
  Cloud fixes the subdomain at app creation, so it cannot be derived in
  advance; `README.md` carries a `TODO` line and `PLAN.md` the matching item,
  and those are deliberately the only two places that need it.
- **THE THREE "WHAT DOES SILENCE MEAN?" QUESTIONS ARE NOW DISCLOSED ON THE
  SITE RATHER THAN BLOCKING IT.** The owner's decision: write the neutrality
  into the page beside the attributions instead of waiting on third parties
  who may never answer. `components._UNSETTLED_TERMS` renders in the footer of
  every page and does four things - names Miami-Dade and Philadelphia rather
  than gesturing at "some sources"; distinguishes their opposite shapes
  (Miami-Dade publishes no reuse position at all, while Philadelphia's licence
  reserves every right and grants none, with SEPTA's trademark clause of
  unclear reach alongside); states plainly that nothing found in either forbids
  what the maps show, because these are questions about the absence of
  permission rather than a prohibition; and commits to removal.
- **The removal commitment gained a SECOND, BROADER TRIGGER.** The standing
  one fires when a publisher *asks*. This one fires on finding out: **if either
  publisher states a position that does not permit this use, that city comes
  off the site without waiting to be asked.** Recorded in all three places
  that carry this promise - the page footer, `docs/data_sources.md`'s
  commitment section, and `docs/excluded_categories.md`'s reader-facing
  version - because CLAUDE.md requires the last two to stay consistent with
  each other, and the footer is now a third copy of the same sentence.
- **New Orleans is deferred post-deploy**, with Seattle's multi-municipality
  build. The owner's call: the pre-deploy city scope is the nine that are
  built. New Orleans was screened (CC0, the cleanest licence of any candidate)
  but still needs a real Step 0, and its streetcar-only network is a scope
  question rather than a data one.

### 2026-09-21 - Pre-deploy gate: name, branding, tiles, notices, and the two data pages

- **Project name: "Storefronts Near Transit"**, decided by the owner. The
  repository, directory and git remote stay `expanded-heatmap` - the new name
  is the SITE title only, so no path, checkout or remote changes. It lives in
  `components.SITE_NAME` and feeds the Overview heading and every browser tab.
  The standing invariant that the project is never named after a city is why
  the name describes the measurement instead.
- **Agency branding: keep the official route colours AND the real line names,
  and state non-affiliation plainly.** The owner's call, on the reading that
  what those clauses actually prohibit is stating or implying affiliation,
  sponsorship or endorsement - which `components._NON_AFFILIATION` now does
  head-on on every page. Nothing in the project reproduces a logo, wordmark or
  route-bullet artwork, which is the part every one of those clauses most
  clearly covers, and for WMATA the colour IS the line's name. Affects six of
  nine cities (MTS, LA Metro, CTA, MTA, SEPTA, WMATA); no re-render needed.
  The alternative - swapping all six to this project's own palette - was
  costed at one dict per city plus a re-render of all nine maps, and would
  have removed the weaker half of the exposure while leaving the line names,
  which a standing invariant requires.
- **TILE PROVIDER: change nothing, and the research REVERSED the
  recommendation I had given.** I had recommended moving the nine city maps
  from OSM raster onto Carto, to match the macro map. The owner asked whether
  Carto runs into API or paid walls - flagged in a sibling project - and both
  policies were then read rather than assumed:
  - **OSM raster** (`tile.openstreetmap.org`, the nine city maps): keyless, no
    stated volume cap, and it explicitly permits "normal interactive viewing
    by a human where the client requests only the tiles needed for the current
    viewport". Requires attribution (already in every map corner), a valid
    User-Agent and a Referer - and the policy itself notes that "modern
    browsers, with default settings, already satisfy these technical
    requirements". Forbids prefetch, bulk download and offline use, none of
    which this project does. Best-effort, no SLA, may be blocked without
    notice.
  - **Carto** (the macro map only): free to a fair-use limit of **5 million
    tile requests a month**, and "all you need is an API key" - so a key is
    now expected. Above the limit, non-commercial projects "usually just get a
    higher limit" and commercial use needs an Enterprise licence.
  So the owner's instinct was right and my recommendation was backwards on
  exactly the axis they flagged: it would have moved nine maps off the
  keyless, quota-free service onto the metered one. **Residual risk, recorded
  and accepted:** the macro map uses Carto's keyless CDN, which that policy no
  longer documents. If it is withdrawn, the macro basemap goes blank while the
  markers, name pills, clicks and the text-link list all keep working -
  degraded, not broken. `pydeck` 0.9.3 does accept `api_keys={"carto": ...}`
  (env `CARTO_API_KEY`), so requesting the free key is available as an owner
  task; it needs their own account, so it is not something to do on their
  behalf.
- **Repository stays PUBLIC.** The owner's call, accepting a real but unlikely
  residual: four transit licences (WMATA section 9, LA Metro, SEPTA, MassDOT)
  are revocable without notice and a public repo cannot be un-published.
  Nothing found in any licence forbids what the project displays, and the
  standing commitment - a removal request is honoured, not argued - is the
  answer if a revocation ever comes.
- **Entry point renamed `app/Overview_&_Introduction.py` to `app/Overview.py`.**
  Streamlit Cloud fixes the main-file path permanently at app creation, and an
  `&` in a path is a live hazard in URLs and shell commands. Renamed with
  `git mv`; every reference updated, including `scripts/scaffold_city.py`,
  which GENERATES new city pages and so would have propagated the old name to
  every future city. `DECISIONS.md` and `docs/passover_opus5.md` keep the old
  spelling deliberately: they are history, not configuration.
- **The five required notices are now DISPLAYED, site-wide.** This was the one
  item that actually blocked publishing. `components.render_site_notices()` is
  called from all twelve pages and renders Chicago's and SFMTA's paragraphs
  **verbatim** (their terms prescribe exact wording), LA Metro's and MassDOT's
  acknowledgements in this project's own words (they prescribe none), CTA's
  encouraged credit, and OSM's basemap credit alongside Carto's.
- **A MISTAKE WORTH NAMING: I first put those notices inside a collapsed
  `st.expander`.** Streamlit keeps a collapsed expander's contents out of the
  DOM, so the notices were not merely small - they were absent until a reader
  clicked. Chicago's terms require its paragraph "at the site where the
  software application ... can be accessed", and this project's own rule for
  the OSM attribution is that it must not sit "beneath UI, behind toggles, or
  off-screen". A required notice behind a toggle is not displayed. Caught by
  probing the rendered DOM for each notice's text rather than eyeballing the
  page; they now render inline, always, in small type. The comment in
  `components.py` says so, to stop the expander coming back as a tidiness
  improvement.
- **`data_sources.md` and `excluded_categories.md` are now reachable in the
  app**, as `pages/10_About_the_Data.py` and `pages/11_What_Is_Excluded.py`.
  Each renders its document AS COMMITTED rather than as a hand-maintained web
  copy, which would drift from the file the pipeline's authors actually read.
  Both are linked from the footer on every page. This closes three obligations
  at once: New York's "source, version, and modifications" condition, the
  site-level placement of the four agency notices, and the fact that a legend
  reading "Retail - NAICS Code: 44/45" overstates its own contents until the
  exclusions are reachable from it.
- **The accuracy sweep found two real claims, both on the New York page - the
  MTA city.** It described its restaurant coverage as "close to fully
  covered", and said Retail was "less complete ... than in the other cities",
  which implied the other eight WERE complete. Both reworded; a note in that
  page's docstring records why, as D.C.'s already did. Everything else was
  clean - the only "accurate" left in a rendered map belongs to a pharmacy
  called Accurate Pharmacy, and the remaining matches are code comments. The
  positive form now appears site-wide: every map is "a snapshot of a public
  register as it stood on the retrieval date", not a census of what is open.
- **Still open, and all of them are the owner's to settle with third parties:**
  the three "what does silence mean?" questions (Miami-Dade, SEPTA's trademark
  clause, the City of Philadelphia License), a licence for this project's own
  code, the deployed URL in the README, and the optional Carto key.

### 2026-09-21 - Macro-map labels: per-city pixel offsets, and the pills made clickable

- **The deferred macro-map polish pass, done because D.C.'s marker forced it.**
  It had been held deliberately until D.C. existed so the east-coast cluster
  could be fixed once. With nine cities there were **11 label collisions**, the
  worst being "Philadelphia" and "Washington D.C." overlapping by 102x13 px -
  one unreadable smear. Now **zero** at 854 and 1200 px.
- **The three-sided "top"/"left"/"right" enum is gone**, replaced by an explicit
  per-city `label_offset` of `(anchor, dx, dy)` in pixels. Three sides at a
  ~20 px offset cannot separate four dots that sit 6-15 px apart carrying pills
  56-126 px wide, which is the east-coast cluster's actual geometry.
- **An east pad on `fit_view` was proposed and withdrawn as counterproductive.**
  This view is LONGITUDE-bound (z_lon 1.453 against z_lat 3.499), so widening
  the bounding box lowers the zoom and pulls the cluster TIGHTER: an east pad
  of 0.30 would take the New York/Philadelphia dots from 6.0 px apart to 4.7.
  The rule recorded in `cities.py` is to move the label, never the box.
- **The first fix was a vertical stack, and the owner's screenshot killed it.**
  The four eastern names were stacked at dy -130/-102/-74/-46 in latitude
  order: collision-free at every width including phones, and wrong the moment
  anyone zoomed in, because **the offsets are in pixels and the map is
  zoomable** - the dots spread apart on zoom while the names stay put, leaving
  "Boston" adrift 130 px from a dot that had moved.
- **The owner's fix was better: east of the dot, y-axis parallel.** Measured,
  the minimum collision-free spread is `dx +14, dy -24/-8/+8/+24`, which cuts
  worst-case drift from **130 px to 24 px** - 5.4x - because the dots' own
  6-15 px of vertical spread adds to the offsets. Verified by zooming the live
  map: each name now sits beside its own dot at every zoom level tested.
- **The map stays zoomable, which is what settled the layout.** The owner's
  reasoning (2026-09-21): non-US cities are a real possibility, and a fixed
  view would force continent-specific maps and a layer of extra pages. Locking
  the view was the alternative and would have allowed the vertical stack,
  since nothing could then drift. That trade was declined, so the layout has
  to survive zooming.
- **The accepted cost is phone-width clipping.** At 340-390 px the two widest
  eastern names are cut by the right edge ("Washington", "Philadelph" - still
  recognisable; Boston and New York fit whole). This is structural, not
  tuning: "Washington D.C." is a 126 px pill whose dot sits ~69 px from the
  right edge, so no `dx` fits it, "middle" is the only anchor that would (which
  is what the stack was doing), and west placement collides with Chicago. The
  clipped pills stay clickable and the Overview lists every city as a text link
  directly beneath the map.
- **THE REAL PRIZE WAS PICKING, NOT TIDINESS.** The `TextLayer` is now
  `pickable` and the selection handler reads `city-labels` as well as
  `cities`. This map is the app's ONLY navigation (`MAP_ONLY_NAV`), and the
  dots are a 12 px target whose centres are **6.0 px** apart for New
  York/Philadelphia and **9.0 px** for Philadelphia/Washington D.C. - they
  physically overlap, so a click there could not reliably say which city was
  meant. A name pill is 56-133 px wide and never overlaps another, so it is an
  unambiguous target. Verified by clicking: the "Washington D.C." pill opens
  D.C., the "Philadelphia" pill opens Philadelphia, and the San Francisco dot
  still opens San Francisco.
- **Markers stay at radius 6.** Shrinking them was considered and rejected:
  once the pill is the click target the dot is a position indicator, so a
  smaller dot would only make the true locations harder to see.
- **Chicago's label went back to the default.** It had to move west while the
  vertical stack reached across it; with the eastern four beside their own dots
  it is unremarkable again. One fewer special case.
- **A known issue this leaves standing:** with the controller enabled,
  scrolling the page while the cursor is over the macro map zooms the MAP
  instead of scrolling the page, and the resulting view persists across
  reloads via the widget key. Found by doing it accidentally. Recorded in
  `PLAN.md` rather than fixed, because fixing it means locking the view, which
  the owner declined for the reason above.
- **Leader lines are no longer planned.** They were the next step while the
  names sat 130 px from their dots; at 14 px east and 24 px of vertical drift
  each name is visually adjacent to its own dot, so a leader would add clutter
  for very little gain.

### 2026-09-21 - Washington D.C. built: one register, three buckets, a feed that expires

- **Ninth city, and the first non-NAICS registry in the project that covers all
  three buckets on its own.** 5,230 premises (Food service 3,285, Retail 1,415,
  Personal services 530) of which **3,860 fall within a ring across the 40
  in-District stations** - **73.8% ring coverage, the highest here**, against
  Miami's 12.6% and Boston's 76%. New York needed four registries and Boston
  three; Philadelphia and Boston each lost a whole category. D.C.'s Basic
  Business License register licenses restaurants, shops and salons in one file,
  so there is no `source` column to dispatch on and no cross-source dedup.
- **Every one of the 95 licence categories has a written verdict, and
  `classify()` RAISES on an unknown one** rather than defaulting to None. A new
  licence category appearing upstream is a thing to look at, not to drop
  silently, and step 2 reports the whole unseen set at once rather than
  surfacing them one exception at a time.
- **Most of the register is not a business, and that is the Philadelphia
  lesson applied.** 37,195 of the 61,329 active in-District rows (61%) are
  residential rentals - One Family Rental 25,557, Apartment 6,081, Two Family
  Rental 2,558, Short Term Rental 2,196, Vacation Rental 803 - dropped
  server-side at download. A further **11,074 are `General Business`**, the
  office and professional catch-all: law firms, engineering practices,
  architects, developers, home-care agencies. That is the single largest
  category exclusion in the project.
- **The `General Business` exclusion was checked, not assumed.** A sample of it
  held a Wawa and a Cava Mezze Grill alongside the law firms, which looked like
  evidence against excluding it. Measured instead: **692 of its rows (6%) share
  a licensee with a kept storefront licence and 2,975 (27%) share a MAR_ID**, so
  a shop that landed in this category keeps its pin through its real activity
  licence. What the exclusion removes is offices.
- **THREE STEP 0 FINDINGS WERE WRONG, and the corrections are the useful part
  of this build.**
  - *"Trade name is missing on 49% of storefront rows ... the Los Angeles trap
    at half LA's severity."* That 49% was measured before the category
    exclusions, and `General Business` - 11,074 office rows, mostly with no
    trade name - is most of it. On the rows that reach the map the gap is
    **26.9%**, and **85.6% of those carry a company-shaped `ENTITYNAME`**. The
    person-like residual is **75 rows, of which 72 are incorporated entities**
    (LLC, corporation, LP) registered under a founder's name - San Diego's case
    exactly, a deliberate public commercial act rather than a fallback the
    pipeline substituted. **Three** are sole proprietorships, and each holds a
    licence (Grocery Store, Barber Shop, Delicatessen) that requires commercial
    premises. The LA trap does not materialise here.
  - *"`MAR_ID` should recover the rest [of the missing coordinates] without the
    Census geocoder."* It cannot: **the 452 rows with no coordinates are the
    same rows that lack `MAR_ID`**, because both are what the District's own
    geocoder failed on - which is also why 409 of them have a blank `WARD`. So
    a geocoding step was needed after all, and this is the second city after
    Los Angeles whose map is step **4**.
  - *"`General Business` (14,770)."* Scoped to active and in-District it is
    **11,074**. Three wrong numbers from one probe, all from measuring on a
    different denominator than the build uses.
- **The geocoding recovery, and its bias check.** 451 premises had no
  coordinates (8.5% after dedup); the Census geocoder matched **387 (85.8%)**,
  and **all 387 fell inside the District polygon**, not merely its bounding box.
  The residual loss is **64 rows, 1.2%**, spread evenly (Food service 0.9%,
  Retail 2.1%, Personal services 0.6%) - so it distorts nothing. Different in
  kind from Los Angeles', where the flagged rows had CORRUPT coordinates biased
  towards recent registrations; D.C.'s simply have none.
- **`LATITUDE` and `LONGITUDE` are ignored entirely.** They are literally `39`
  and `-77` on all 76,107 active rows - 0 inside the District. The real
  coordinates are `X_COORDINATE`/`Y_COORDINATE` in **EPSG:26985**, NAD83
  Maryland state plane in METRES (not the US-survey-feet variant Boston's
  sources use), verified by transformation rather than assumed. That is a
  **third** CRS in one city, distinct from the city's own EPSG:32618. 6,052 of
  6,052 reprojected points land inside the District's bounds, which is the check
  that would catch a wrong EPSG.
- **The premises key is a real address id for once.** `MAR_ID` is the
  District's Master Address Repository identifier, paired with `CUSTOMERNUMBER`,
  the register's own per-licensee id - better than Boston's and Miami's
  name-plus-address fallback. 812 licensees hold more than one kept licence
  type; **121 hold exactly Cigarette Sales + Food Products + Patent Medicine**,
  which is one corner shop and not three businesses. Rows with no `MAR_ID` key
  on their own `record_id` so they cannot collapse into one another.
- **The bucket tie-break was chosen by measuring the alternative.** 345
  premises hold licences in more than one bucket, and every one of them crosses
  Food service <-> Retail: **no licensee anywhere in the register mixes Personal
  services with another bucket**, so that entry in `BUCKET_PRIORITY` never
  decides anything. Food service first, consistent with Boston. A more
  elaborate rule ranking a licence that names what the premises IS
  ("Restaurant", "Grocery Store") above an endorsement it merely holds
  ("Cigarette Sales", "Patent Medicine") produces an **identical** split, so
  the simple rule costs nothing; Retail-first would move 368 premises (7%).
- **`Delicatessen` is ambiguous in the source, and stays ambiguous.** D.C.
  issues it to sandwich shops and cafés AND to corner shops: a sample of 25 held
  Julia's Empanadas and Call Your Mother Deli next to a 7-Eleven, a Safeway and
  a convenience store. Counted as Food service, which fits the plurality, but
  **~180 premises hold it with no other descriptive licence and could honestly
  read either way**. Excluding it would remove a fifth of the city's food
  service; splitting it needs trade-name classification the source does not
  support. Kept, counted as food, and said out loud on the city page.
- **THE SILVER LINE COLOUR WAS DECIDED TWICE, AND THE FIRST MEASUREMENT WAS
  AGAINST THE WRONG BASEMAP.** WMATA's `#919D9D` is grey, and against the LIGHT
  basemap it is the weakest colour in the project: Delta-E 31.4 from OSM's land
  fill, 36.5 from road fill, 22.0 from unpaved track. On that measurement it was
  darkened to `#5F6A6A` (51.0 / 56.3 / 41.0) - the treatment New York's Staten
  Island Railway and Boston's Mattapan Trolley already carry - and **the owner
  approved that change on those numbers**.
  The numbers were incomplete. **This map opens in DARK mode**, where
  `map_common.py` does not invert the line strokes but BRIGHTENS them
  (`brightness(1.55) saturate(0.9)`) while inverting the tiles underneath. Both
  sides of the comparison move, in opposite directions:

      | colour            | dark mode (default) | light mode (toggle) |
      | #919D9D official  |        75.4         |        22.0         |
      | #5F6A6A darkened  |        47.2         |        41.0         |
      | for scale: Blue   |        81.7         |        54.3         |

  So darkening made the Silver Line the **worst-contrast line in the city in
  the mode every reader sees first**, to fix the mode they have to ask for -
  and in the render it was untraceable, legend swatch included. Eight
  hue-shifted slates were measured too; the ones beating `#5F6A6A`'s worst case
  did it by drifting towards the Blue Line's hue (Delta-E 30.7 from Blue against
  the official colour's 42.0), trading one confusion for a worse one. **All six
  colours are therefore WMATA's own, as published**, and the residual is
  recorded rather than engineered around: in light mode the Silver Line is
  harder to trace than the other five. Reported to the owner as a correction to
  an approved decision.
- **58 of 98 stations are outside the District, and they are NAMED.** 32 in
  Virginia, 26 in Maryland - the second-largest station exclusion here after
  San Diego's 25%. D.C.'s own boundary layer can say "outside" and nothing more,
  so a **Census TIGERweb states layer** (three polygons, requested by name) was
  added for the naming alone. At that scale the exclusion has to be citable, as
  San Diego's 16 and Los Angeles' 54 are. Census TIGER products are US federal
  works and carry no copyright.
- **No multi-jurisdiction disambiguation was needed, which is the contrast with
  Boston.** Only one station is even arguably marginal - Southern Av at 40.1 m
  outside - and the next two are Capitol Heights at 111.2 m and Arlington
  Cemetery at 130.0 m. Boston needed MassGIS because four of its stations sat
  within 60 m of the line.
- **No thinning, on a measurement rather than a label.** Metrorail is
  grade-separated end to end, and the in-District stations sit a **median 962 m**
  apart against a 966 m outer ring (min 212 m at the Farragut West/North pair,
  max 3,020 m). That is New York's and San Diego's shape, not San Francisco's
  134 m. 20 of 40 stations are closer to a neighbour than the outer ring, all in
  the downtown cluster, and each business is assigned to its nearest station so
  nothing is double-counted. Rings stay ON, as in Boston. `step1_stations.py`
  exits if `THINNED_GROUPS` is ever set, rather than leaving the setting inert.
- **The only feed in the project behind an API key, and the only one that
  expires.** `api.wmata.com` returns 401 unauthenticated. The key is the
  owner's, is WMATA's property under §5, is read from `WMATA_API_KEY` and is
  **never echoed - not even in the 401 error message**. `feed_info.txt` declares
  a **ten-day** window (`20260915`-`20260925`), so `fetch_sources.py` re-checks
  `feed_end_date` on EVERY run including runs that skip the download, and treats
  an expired copy as an error rather than a warning: a stale feed still parses,
  still has 98 stations and still builds a map, so nothing downstream would
  catch it.
- **Shape selection needed care no other feed has.** WMATA publishes 26 to 101
  shapes per route, so "the most-used shape" could easily be a short turn - the
  Yellow Line's second-most-used stops at Mt Vernon Square, **nine stations
  short of Greenbelt**. Each drawn shape is the most-used among those serving
  the route's full stop count, checked rather than assumed.
- **Privacy: the download boundary is the control.** `BUSINESSOWNERFIRSTNAME`,
  `BUSINESSOWNERLASTNAME`, `BUSINESSOWNERMIDDLENAME`, `AGENTFIRSTNAME`,
  `AGENTLASTNAME`, `AGENTMIDDLENAME`, `AGENTENTITY` and **`BILLINGADDRESS`**
  all exist in this layer, populated on tens of thousands of rows. None is
  requested in `outFields`, so none is ever on this machine; step 2 asserts all
  eight stay absent, and `fetch_sources.py` exits if the server returns any
  column it did not ask for.
  The screening reports **0 emails, 0 phone numbers, 0 care-of markers**, 560
  pins (14.5%) whose displayed name reads as a person's, and **0.00%
  person-like-name-at-a-residential-unit**. That last figure is a **MEASUREMENT
  GAP**, as Boston's was: D.C.'s addresses carry almost no unit designators
  (4 commercial, 0 residential across 581 matching rows). What replaces it here
  is a structural signal Boston lacked - `ENTITYTYPE` - giving **14 pins
  (0.36%) that are a sole proprietorship displaying a person-like name**, each
  holding a licence that requires commercial premises. `SSL` is on **91.1%** of
  mapped rows, better than Miami's `FOLIO` at 45.7%, so a Philadelphia-style
  parcel join is available if that ever stops being enough.
  `check_personal_exposure.py` gained one small capability for this city:
  `entity_individual` now accepts a tuple, because D.C. spells sole trading two
  ways ("Sole Proprietorship", "Domestic Sole Proprietor") and matching one
  would have undercounted.
- **WMATA adds NO mandatory notice, correcting a prediction in
  `docs/data_sources.md`.** That file said a sixth notice "would come with
  WMATA if D.C. is [built]". It does not: WMATA requires no attribution and no
  acknowledgement of any kind. The mandatory count stays at **five** (MassDOT's
  became active with Boston). What D.C. does add is a second copy of MTA's §6
  accuracy clause - so the city page deliberately avoids "accurate",
  "complete", "current", "up to date" and "official", and its docstring says
  why - and a sixth agency to the branding question, whose wording is the one
  that names "confusingly similar variants".
- **Verified:** no console errors, all six lines carrying a permanent on-map
  label AND a legend entry, three buckets in the legend, OSM attribution
  intact, no TODOs shipped.

### 2026-09-21 - Boston built: two buckets, three registries, two station rules

- **Eighth city, and the narrowest map here.** 3,164 premises (Food service
  2,373, Retail 791) of which **2,410 fall within a ring across 57 in-city
  stations**. Built after being parked: it passed Step 0 on 2026-09-21 and was
  then superseded in the queue rather than rejected, and the owner returned to
  it before D.C. with the instruction to state its limitations on the city page.
- **Better than Step 0 predicted, because of the cross-source dedup.** Step 0
  estimated ~2,740 sites with Retail at 385 unambiguous plus overlaps. The
  build gets **791 Retail**, because deduplicating the three registries against
  each other preserved more distinct package stores than the overlap estimate
  assumed - 27 premises appeared in more than one registry, not the hundreds a
  naive reading of the overlap would imply.
- **Three registries, dispatched on a `source` column like New York's**, and
  deduplicated ACROSS sources as well as within them. The overlap this exists
  for is package stores: a shop can hold both an ISD `RF` food licence and a
  Licensing Board `Retail All Alc.` licence, as "Go Fresh 365" / "Ming's
  Supermarket" does at 1102 Washington St. The Licensing Board's 2,578 Common
  Victualler licences are **excluded** - they are the same restaurants as the
  ISD source, so keeping them would double-count from a second registry.
- **Address normalisation was load-bearing, not cosmetic.** ISD writes "1102
  WASHINGTON ST" and the Licensing Board writes "1102-  WASHINGTON ST" for the
  same premises. Without collapsing the trailing hyphen and padding, no package
  store would ever have matched its own food licence and every one would have
  been counted twice - the dedup would have reported zero cross-registry
  duplicates and looked like it was working.
- **Two buckets. Personal services is ABSENT, not thin**, and that was verified
  three ways rather than assumed: Socrata's cross-domain discovery API returns
  no Massachusetts source for cosmetology, barber, salon, hair, nail salon,
  body art or tattoo; `data.mass.gov` is not a data portal at all (HTML 404
  from both the Socrata and CKAN entry points); `opendata.mass.gov` does not
  resolve. Massachusetts licenses cosmetology at state level through a
  per-licence lookup with no bulk export. Second city with a whole category
  missing, after Philadelphia, for the identical structural reason.
- **The trap that would have made this a one-bucket city, avoided.** Boston
  publishes an "Active Food Establishment Licenses" extract that looks like the
  obvious source and holds only `FS` + `FT` - no `RF` (Retail Food) at all,
  which is the entire Retail bucket. The 902,651-row inspection history carries
  the same `licensecat` field including RF's 504 premises, and has better
  coordinates too (99.9% of active premises against 93.8%). The history is used,
  collapsed to one row per premises **in SQL** via CKAN's `datastore_search_sql`
  so the download is ~2,900 rows rather than ~900,000.
- **Two station rules at once, as in Philadelphia.** Red, Orange and Blue are
  grade-separated heavy rail and keep every in-city station. The Green Line is
  a central subway plus four street-running branches - San Francisco's exact
  shape - and takes the four sub-transit-line filters: 93 stops across its four
  branch shapes down to 68, with the 13 central-subway stations, each branch's
  terminals and all 7 interchanges force-kept.
- **Mattapan was NOT thinned, and that is a measurement rather than a
  judgment.** It is a street-running trolley, so the obvious guess was that it
  needed the same treatment. Measured instead: its 8 stops sit 433-804 m apart,
  **median 518 m** - comparable to New York's 482 m and nowhere near San
  Francisco's 134 m trolley median. Left whole on the number rather than on the
  street-running label.
- **57 of 100 stations are in Boston.** The 43 dropped are in Newton (8),
  Brookline (7), Cambridge (6), Somerville (5), Milton (4), Quincy (4), Medford
  (3), Revere (3), Malden (2) and Braintree (1). `excluded_stations.csv`
  therefore carries **two kinds of exclusion** and names which is which - 43
  out-of-town and 25 thinned - which no other city's does.
- **A config bug caught by validating the config against the feed, not by
  reading it.** `STATION_SUFFIX_PATTERN` stripped a trailing " Station", which
  turned **"North Station" into "North"** - so filter 1 stopped recognising one
  of the Green Line's own central-subway stations and would have silently
  thinned it as a surface stop. "North Station" is the station's name, not a
  name plus a suffix. Step 1 now ASSERTS every configured subway station exists
  in the feed and exits if one does not, which is what surfaced it. A second,
  smaller error surfaced the same way: "South Station" had been added to that
  list speculatively and is a Red Line station, so it would never have matched.
- **A Step 0 assertion of mine was wrong, and two independent layers settled
  it.** Step 0 recorded four stations as marginally outside Boston's own
  water-excluded outline and asserted that **Boston College at 6.7 m "is really
  a Boston station"**, concluding that a distance tolerance could not separate
  the four. MassGIS places Boston College in **NEWTON**, 6.6 m outside - two
  independent boundary layers agreeing on the same distance and one of them
  naming the town. Four of the 43 out-of-town stations do sit within 100 m of
  Boston, but every one is unambiguously *named*, so no tolerance is needed at
  all. **Naming beat measuring**, which is why the multi-town layer was the
  right choice.
- **One boundary layer rather than two, against the Step 0 plan.** Step 0 said
  to fetch Boston's own outline for filtering plus a MassGIS layer for naming.
  MassGIS's municipalities layer does both - filter on `TOWN='BOSTON'`, name
  every other station's town from the same join - so Boston's own outline is
  recorded as considered and unused. Downloaded with a spatial envelope around
  the network rather than all 351 towns statewide: 61 polygons.
- **`gpsx`/`gpsy` are EPSG:2249**, state plane in US survey feet, reprojected
  in step 2. Verified by transformation during Step 0, not assumed - the
  metre-based sibling EPSG:26986 lands every point near 60 degrees north, and
  the coordinate bounds check in step 2 is what would catch that mistake if the
  CRS were ever changed.
- **`businessname`, not `dbaname`.** In the ISD table `dbaname` is blank on
  99.0% of rows while `businessname` always holds the trade name - the reverse
  of every other city here, so a step 2 copied from elsewhere would have
  produced almost nothing without failing. The two smaller sources use the
  normal convention, so step 2 reads a different column per source.
- **Privacy: no personal-name column is ever loaded, and the residual reading
  is a MEASUREMENT GAP rather than a clean result.** The ISD table carries
  `legalowner`, `namelast` and `namefirst`; the Licensing Board table carries
  `applicant`, `manager` and two phone columns. None is selected and step 2
  asserts all eight stay absent. The screening reports 0 emails, 0 phone
  numbers, 0 care-of markers, and 0.00% person-like-name-at-a-dwelling - but
  **565 of 2,410 pins (23.4%) read as a person's name, the highest share of any
  city**, and 0 of them carry any unit designator because Boston's addresses
  contain none at all. So the 0.00% is the check having nothing to read, the
  same shape as San Diego's old 0.03% that became 2.80% once a parcel join
  replaced address text. What actually limits the exposure is the sources: a
  food-service licence and a package-store licence both require commercial
  premises, so a home cannot hold one. `property_id` IS Boston's assessing
  parcel id, so the Philadelphia-style parcel join is available if that ever
  stops being enough. Recorded in the check script and in `PLAN.md` rather than
  reported as a win.
- **MassDOT's notice is now ACTIVE, taking the mandatory count from four to
  five.** It had been recorded as conditional on Boston being built. The city
  page carries "Rail alignment data provided by MassDOT/MBTA"; the outstanding
  part is the same as for Chicago, SFMTA and LA Metro - it must appear where the
  site is accessed, not only on one city page. Every Boston data source is
  ODC-PDDL, the cleanest licensing of any city here.
- **Rings stay ON here**, unlike New York's and Miami's. That is the payoff for
  having thinned the Green Line rather than reaching for the rings-off lever:
  the kept stations are grade-separated heavy rail plus a thinned surface line,
  so they are separated enough to read individually.

### 2026-09-21 - Canada screened live: five viable cities, and Montreal nearly lost to a keyword filter

- **The rail screen killed half the list before any data question was asked,
  which is why it ran first.** `routes.txt` was read from each agency's live
  GTFS via the Mobility Database catalogue. Urban rail (route_type 0/1/5/7/12,
  excluding 2 = commuter): **Toronto** 17, **Montreal** 4 subway, **Vancouver**
  3 subway, **Ottawa** 6 LRT, **Edmonton** 3, **Calgary** 2. **None at all**:
  Winnipeg, Mississauga, Brampton, Hamilton, Quebec City, Halifax - bus only.
  **Toronto codes its subway as route_type 0, not 1**, so its 4 subway lines
  and ~13 streetcar routes are indistinguishable by type: San Francisco's exact
  shape, needing `docs/sub_transit_line_filters.md` and route-id selection.
  Cheap to know now, expensive to discover at Step 3.
- **Montreal was nearly ruled out by a keyword filter, and is instead probably
  the best data in the project.** A first pass over the full 447-package list
  filtered by keywords concluded "food-only". Wrong: **`locaux-commerciaux`**
  contains none of the words *business*, *licence*, *permis*, *entreprise* or
  *commerce*. It is a 2025 field survey of street-level commerce across the
  agglomeration, CC-BY 4.0, annual since 2021: **28,621 premises, 100%
  coordinates** (both `LAT`/`LONG` and projected), **`NOM_ETAB` on 100%**,
  **`SCIAN` - NAICS in French - on 99.6%**, plus a vacancy flag. Buckets are
  present twice over: `USAGE1` gives Food 6,565 / Retail 8,421 / Personal
  services 2,453, while SCIAN gives 72 -> 6,301, 44+45 -> 8,283, 81 -> 4,343 -
  **the prefixes `pipeline/taxonomies/naics.py` already uses**, so Montreal may
  need no new taxonomy module.
- **It passes the exact coverage test Boston's own survey failed.** Boston's
  Business Inventory was rejected for occupying 37 cells of 0.01 degrees;
  Montreal's occupies **441**, spanning the whole island. The clinching detail
  is the bottom of the distribution, not the top: Ville-Marie has 4,316
  premises and **Senneville has 1**. A partial survey does not walk a village
  of 900 people. So this is a census - and a field survey of actual storefronts
  is arguably a *better* answer to this project's premise than a licence
  register, which records who registered rather than what is on the street.
- **Verified schemas for the rest.** **Vancouver** 205,943 rows with
  `geo_point_2d`, `businesstype`/`businesssubtype`, both legal and trade names,
  OGL-Vancouver, updated the same day - the strongest licence register.
  **Calgary** and **Edmonton** both ship coordinates; Calgary additionally has
  **`homeoccind`**, a home-occupation flag handed over directly, the signal
  this project derives by hand elsewhere (as Chicago's `business_activity`
  does). **Toronto** 159,872 rows but **no coordinates at all** - addresses
  only, so it needs a geocoding pass like D.C. - and its licence field reads
  **"not specified"**, which by `docs/data_sources.md`'s own rule means go read
  the terms. Toronto's `bodysafe` (personal services) and `dinesafe` (food) are
  a two-bucket fallback if geocoding proves painful. **Ottawa is out**: 697
  catalogue entries scanned on a wide net, and the only address-level
  commercial data is food-safety inspections.
- **Brampton is blocked on rail, not on data, and the Miami regional precedent
  does not rescue it.** Its directory is an employer census of brick-and-mortar
  businesses: 6,059 rows, **X/Y on 100%**, **`NAICS_DETAIL` on 97.3%** across
  614 six-digit codes, plus an `OPERATIONAL` flag and floor area - better than
  most US cities here. But Metrorail physically extends into Hialeah and Coral
  Gables, whereas TTC Line 2 terminates at Kipling *inside* Toronto, and the
  only rail serving Brampton is GO commuter rail, excluded everywhere. Recorded
  in `docs/city_shortlist.md` with a mid-2027 revisit tied to the Hurontario
  LRT, asking "has an opening date been announced?" rather than "is it open?".
  Mississauga would arrive with it, but needs a different source: its Business
  Directory lists **only businesses that agreed to be included**, which would
  map who filled in a form rather than where commerce is.

### 2026-09-21 - Source encoding declared per city, and the catalogue rule tightened

- **Read a new city's whole catalogue, never grep it.**
  Boston already proved search hits are not the catalogue (48 vs 247 packages);
  Montreal proves a keyword filter over the full list reintroduces the same
  bias. ~450 names costs about a minute and ~3 KB. Written into `add-city`
  Step 0 and `docs/data_sources.md`. The evidence behind it is a live screen
  logged separately.
- **`SOURCE_ENCODING` is now declared per city rather than inferred**, and
  passed at all 11 raw third-party reads (one each for Chicago, Los Angeles,
  Miami, Philadelphia, San Diego; four for New York's registries; two for San
  Francisco). Scoped deliberately to third-party bytes - reads of this
  project's own processed CSVs and of GTFS members inside zips are untouched,
  since those are bytes we wrote or a spec that mandates UTF-8. **The earlier
  justification was overstated and is corrected here:** pandas does not
  silently guess latin-1, it defaults to UTF-8 and *raises*. The real hazard is
  one step later - the `UnicodeDecodeError` lands on whoever adds the next
  city, and reaching for `latin-1` to silence it corrupts accented characters
  **without failing**, so nothing downstream catches it. Declaring the encoding
  makes that a reviewable decision instead of a silent patch. All seven cities
  are `utf-8`; Quebec is where this will first bite. Passing the default
  explicitly is behaviourally a no-op, and **`drift_check --changed` confirmed
  it**: the change touched all seven cities' configs, the filter correctly
  escalated to 7 of 7, and every city came back zero drift.

### 2026-09-21 - WMATA's terms read in full, and San Francisco's recorded endpoint found broken

- **WMATA needs no written authorization, and the summary that said otherwise
  was mis-scoped.** A third-party summary of the Transit Data Terms of Use
  presented §8's conditions - prior written authorization, commingling data,
  exposing user data to WMATA for statistical research, a third-party
  kill-switch - as standing obligations. They are not. §8(b) triggers only "In
  the event you desire to re-use the Transit Data for the purpose of providing
  that data to third parties **through your own application programming
  interface**", and this project has no API: it downloads a static zip once and
  renders HTML. §7 expressly grants a licence to "download, use, reproduce, and
  redistribute WMATA's Transit Data **within your Application**", and §8(a)
  carves out sharing "(except with your Application's users)". Read in full
  rather than trusted second-hand, which is the same discipline that caught
  MTA's landing page earlier the same day.
- **Two WMATA clauses do bite, and one of them is now a cross-city rule.** §6
  forbids stating or implying that the data an Application provides "is
  accurate, complete, or timely" - **identical in substance to MTA's**, making
  it the second feed to constrain city-page prose that way, so it is a sweep
  across every page rather than a D.C. footnote, and New York is already built.
  §9 is the sharpest termination clause in the project: on termination "you
  must permanently delete all Transit Data or other data which you stored", and
  "WMATA may request that you certify in writing your compliance". LA Metro
  requires removal; only WMATA asks for written certification.
- **WMATA is also the first feed in the project behind an API key**, obtained by
  the project owner (a free developer account; the key is WMATA's property,
  cannot be sold or transferred, and stays out of the repo). The correct
  operation is **`Rail GTFS Static`**, not `Rail & Bus Combined GTFS Static`
  and not any `RT` feed. Verified on download: 6 routes, all `route_type 1`,
  `network_id Metrorail`; **98 parent stations, all with coordinates**; 270,784
  `stop_times` rows; 340 shape_ids; no bus contamination. `feed_info.txt`
  declares `feed_end_date 20260925` - a **ten-day validity window**, the
  shortest of any feed here, so a rebuild must re-download rather than reuse a
  stored copy.
- **D.C. keeps 40 of 98 Metrorail stations (40.8%) - a deeper cut than
  predicted, and it does not matter.** Second only to San Diego's 25% (Boston
  57%, Los Angeles 51%), because Metrorail is a regional system that passes
  through the District. But all six lines keep real in-city presence (Red 16,
  Silver 15, Orange 14, Blue 13, Green 13, Yellow 9), and at roughly 6,900
  sites across the three buckets that is **~173 sites per in-city station
  against Boston's ~39**. The share is the least interesting thing about D.C.'s
  viability. The boundary is also clean, unlike Boston's: one arguably marginal
  station (Southern Av, 40.1 m out), then a jump to 111 m and 130 m, so no
  multi-town layer is needed. Measured in EPSG:32618, derived from longitude.
- **An endpoint that is recorded but never re-run is not verified - San
  Francisco proved it.** `PLAN.md` carried "Find San Francisco's boundary-layer
  endpoint - it is recorded nowhere" as open; it had in fact been recorded in
  three places on 2026-09-21. But running the recorded command found
  `data.sfgov.org` now **301-redirects**, and the documented `curl -sG` has no
  `-L`: it writes a **654-byte HTML stub** into `sf_county_boundary.geojson`
  and exits 0, so San Francisco still could not be rebuilt. The earlier item was
  closed by identifying the dataset, never by running the command. Fixed to
  `data.sf.gov`, which reproduces the stored file byte-for-byte (38,822 bytes,
  sha256 `ecf625b5…`). This is the **second** symptom of one host rule for this
  city - the assessor roll 403s on `/resource/` at the same old host - so it is
  now recorded as a single rule rather than two gotchas.

### 2026-09-21 - drift_check goes incremental, and the scaling ceilings are written down

- **`drift_check.py` grew `--changed`, because the full sweep is O(cities) on
  a gate the project runs constantly.** It maps changed files to the cities
  they can actually reach: `pipeline/<city>/**` and `outputs/<city>/**` to that
  city, `pipeline/taxonomies/<t>.py` to every city whose config declares
  `TAXONOMY_SYSTEM = "<t>"`, and anything else under `pipeline/` to every city.
  Verified against synthetic paths: a Philadelphia step file resolves to 1 of 7
  cities, `taxonomies/naics.py` to exactly the 3 bound to NAICS (Los Angeles,
  San Diego, San Francisco), `map_common.py` to all 7, and doc or app changes
  to none. **Deliberately conservative**: a shared file still triggers the full
  sweep, because a wrong "nothing to do" is invisible until a deploy serves
  stale output, and a filtered run prints a `PARTIAL:` line naming what it
  skipped. The unfiltered sweep remains what runs before a deploy and when
  recording a baseline. Also added `--since REF` and `--list`, and a fallback
  to `HEAD~1` when nothing uncommitted touches the pipeline - the common case
  right after "commit after each green step". Verified end to end on
  Philadelphia: zero drift, 8,512 -> 8,504 rows, 4,954 points across 94
  stations, same as the committed baseline.
- **The page-numbering fear is unfounded, and is recorded so it is not raised
  again.** `app/pages/10_*.py` does *not* sort before `2_*.py`: Streamlit's
  `source_util.page_sort_key` applies `PAGE_FILENAME_REGEX` and returns
  `(float(number), label)`, a numeric sort. Checked against the Streamlit
  installed in `.venv-lean`. No zero-padding is needed at ten cities. This
  corrects an earlier claim made in this session before it was checked.
- **Wrote `docs/scaling_thresholds.md`** at 7 cities, after the owner asked how
  far the project could scale. The finding that reframes the question: **per-page
  rendering does not scale with city count at all** - each page embeds one
  city's map, so the cost is bounded by the largest city (New York, 10.3 MB)
  rather than by how many exist. What does break, in order: the Overview macro
  map at ~10, **committed `outputs/` in git at ~20 - the real ceiling**, and
  hosting at 40+. The escape from the `outputs/` problem is closed by two
  existing invariants at once (the app never runs the pipeline; geopandas
  breaks the lean deploy), so the answer has to be storage-side, probably LFS.
- **The binding constraint is none of those: it is the per-city research
  cost.** Seven cities took about four days, and the expensive parts were Step
  0, taxonomy modules, privacy checks and licence review - one agency's terms
  consumed much of one session today and turned up a clause affecting an
  already-built city. So "more cities" is a cost-per-city problem, not a
  frontend one, which argues for depth per country over breadth across
  countries: the portal licence, privacy regime and often the classification
  amortise across a country's cities.
- **Measured the cost of a no-op re-render, which is the `outputs/` ceiling in
  miniature.** Re-running Philadelphia for the end-to-end test rewrote
  `outputs/philadelphia/heatmap.html` with fresh Folium element ids: a
  1,149,401-byte file showing **1,120 changed lines** against HEAD with no
  semantic difference at all. Reverted rather than committed. Every such run is
  a megabyte of history for nothing, which is precisely why the threshold doc
  puts committed outputs at ~20 cities.

### 2026-09-21 - Miami built, as the project's first REGIONAL city

- **Seventh city. Regional scope, decided by the owner**, and the first working
  proof of the multi-jurisdiction idea Seattle is planned around. Metrorail
  leaves the City of Miami - 13 of its 42 stations are in Hialeah, Medley,
  Coral Gables, South Miami or unincorporated Miami-Dade - and the standing
  rule says a station in another city is a new project, because it needs that
  city's own business data sourced and verified separately. **Miami is the
  exception because that cost is absent: Miami-Dade County licenses all 34 of
  its municipalities in ONE file**, one schema, one publisher, one set of
  terms. So full-line coverage needed no extra sources, no cross-source dedup
  and no second licence review. Where Seattle will cost 10-12 registries, this
  cost none.
- **Consequences carried through rather than left implicit.** There is no
  `CITY_KEEP`; the boundary layer NAMES each station's municipality instead of
  filtering (recorded in `outputs/miami/station_municipalities.csv`, with
  `excluded_stations.csv` kept and empty because the network never leaves the
  county); and the page is labelled **"Miami (Regional)"** in `app/cities.py`
  and its title, because a map spanning six municipalities cannot honestly be
  called Miami. The owner asked for that label explicitly.
- **Final figures.** 175,982 active rows -> 32,398 storefront -> 29,979
  premises after dedup -> **29,878 after the residence filter**. Rendered:
  **3,775 within-ring pins across 42 stations** (Retail 1,960, Food service
  1,254, Personal services 561), with 29,878 available on the all-Miami-Dade
  toggle. Buckets before ring assignment: Retail 15,750, Food service 8,061,
  Personal services 6,067. Map is 1.2 MB.
- **The file has a NAICS column and it is NULL on all 194,099 rows.** Checked
  county-wide, not sampled. This is the first city where NAICS was present in
  the schema and unusable in fact, and it is why the Step 0 screen's claim that
  Miami needed no taxonomy module was wrong. `miami_catgryname` maps the
  county's own `CATGRYNAME` instead - all 150 active values given an explicit
  verdict, verified against the full distinct pull, with step 2 reporting any
  value it has never seen so an upstream rename surfaces instead of silently
  dropping rows.
- **Five taxonomy findings that the category NAMES do not give you**, each from
  hand-sampling:
  - **`SERVICE BUSINESS` (28,010 rows) is excluded, and it is the largest
    single judgment call here.** Sampled: paralegals, management consultancies,
    media and tech agencies, tour guides, dispatch services - offices, not
    shops - plus some genuine trade repair and a number of COTTAGE FOOD
    operators working from apartments. Same role as LA's NAICS 812990 and
    D.C.'s "General Business". **Stated as a known bias rather than hidden:
    this map undercounts small repair and service premises in Miami.**
  - **`DANCING OR ENTERTAINMENT` is not venues, it is bars and restaurants**
    holding an entertainment endorsement (Gramps, Neme Gastro Bar, Biscayne Bay
    Brewing, "BAR WITH ENTERTAINMENT"). Food service.
  - **`LAUNDRY MACHINE` is a machine licence, not a laundromat.** Its holders
    include Paradise Apartments, Camelot Court Apartments ("LAUNDRY ROOM") and
    Parque Apartments ("10 WASHERS / 10 DRYERS") alongside real coin laundries,
    so counting it would have put pins on apartment blocks. Excluded;
    `CLEANER/LAUNDRY/ALTERATIONS` covers the real premises.
  - **`TANGIBLE PERSONAL PROP DLR` (12,623 rows) reads like retail and is
    not**: wholesale distributors, export/import and online sellers, many at
    apartment addresses.
  - **`UNCLASSIFIED BUSINESS` is infrastructure**: Crown Castle and Pinnacle
    Towers cell sites, `OCCDESC` "OTHER MEMO".
- **One category kept on a cross-project consistency argument, flagged so the
  choice is visible.** `AUTO / TRUCK / VAN SALES` (car dealers - Braman
  Cadillac, used-car lots) is not a storefront in the walkable sense this map
  is about, but NAICS 441 sits inside the 44/45 range every NAICS city here
  counts as Retail. Excluding it in Miami alone would make the buckets mean
  different things in different cities.
- **First city needing a PREMISES dedup, because none of the obvious keys is
  one.** `RECEIPTNO` is unique per row (6,631 rows = 6,631 receipts),
  `ACCOUNTNO` is per account (6,167), and **`FOLIO` is the PARCEL** - those
  6,631 rows shared only 1,849 folios, because a mall or an office tower is one
  parcel holding dozens of businesses. So rows collapse on name-plus-address,
  and 1,944 premises held licences in more than one category. Bucket priority
  is **Food service > Personal services > Retail**, because `RETAIL SALES` is
  the category a premises picks up SECONDARILY (a restaurant selling
  merchandise, a salon selling product) - letting it win would relabel
  restaurants and salons as shops.
- **Station scope: all 42 kept, no thinning, decided on measurement.** The
  owner's instruction was to keep every station unless density was a concern.
  Measured: Metrorail's 23 sit a median 1,149 m apart (min 260 m) with only
  6/23 inside the 966 m outer ring - fine. The Metromover's 19 sit a median
  235 m apart and **all 19** are inside a neighbour's ring. That is San
  Francisco's shape, but thinning it would discard ~12 of 19 stations in the
  densest commercial district on the map. **Chosen instead: keep every station
  and start the rings switched OFF**, as New York does, keeping the shared ring
  edges because Metrorail needs them. Each business is assigned to its nearest
  station either way, so the cost of the overlap was never double-counting -
  only legibility, and the rings lever fixes exactly that.
- **Two phantom stations found by MEASUREMENT, not by reading names.** Metrorail
  has **no `parent_station` at all**, so its 46 stop_ids are 23 stations x 2
  directions, spelled four different ways. After collapsing, two pairs still
  sat absurdly close: "Government Ctr." (Metrorail) and "Government Center"
  (Metromover) at 20.1 m, and "BISCAYNE BD@E FLAGLER ST" at **0.0 m** from
  Bayfront Park. The first is one interchange under two spellings. The second
  settled a question the config had recorded as unanswerable - MDT labels that
  inner-loop stop by its cross-streets, and rather than guess which station it
  was, the 0.0 m distance proved it IS Bayfront Park. 44 stations became 42.
- **Metrorail is drawn once, though MDT signs it as two lines.** Green and
  Orange share the trunk and split north of Earlington Heights, but the GTFS
  publishes a single route ("REGULAR METRORAIL SERVICE") for both, so there is
  no route_id per line. Inventing a split the feed does not contain is worse
  than using the name every station sign carries. This is the mirror image of
  New York, where 29 GTFS services had to be grouped into 11 signed trunks.
  Nine shapes exist because the line branches and MDT ships single-track
  working variants; the drawn pair is the Green trunk plus the airport spur,
  which together are the whole physical network.
- **Line colours are this project's own, which is the documented fallback
  rather than a departure.** MDT publishes Metrorail as `FF8040` (orange,
  against Food service's `#eb6834`) and the two Metromover loops as `008080`
  and `008000` (both against Personal services' `#1baf7a`, and barely
  distinguishable from each other). Purple / teal / brown are distinct from the
  category colours and from one another. Incidentally this also sidesteps the
  open route-colour trademark question for one city.
- **Privacy: two real exposures found by the screening and fixed, not just
  reported.** First run: 6 displayed names carried a person via a `C/O` or
  `ATTN` clause, and **28 of 3,797 pins (0.74%) were a person-like name at a
  residential unit** - second-worst in the project after Los Angeles. After
  fixing: **0 care-of markers and 0.00% person-like-name-at-a-dwelling**, level
  with Philadelphia as the best. `OWNERNAME` is populated on 100% of rows and
  is frequently a person, so `fetch_sources.py` never downloads it and step 2
  asserts it and all seven `MAIL*` columns stay absent; `BUSNAME` is present on
  every row, so unlike Los Angeles (68% blank) and D.C. (49%) this city never
  has to consider a registrant's name at all.
- **Only ONE residence rule, because only one signal is trustworthy at this
  scope.** San Francisco and Los Angeles run two, joining a parcel roll for
  land use and a homeowner's exemption. Miami-Dade's `FOLIO` would allow the
  same and is present on 100% of active City of Miami rows - but on only
  **45.7% of the regional storefront set**. A parcel rule would therefore apply
  to half the map and not the other half, which is worse than not running it,
  so the address rule (person-like name + a dwelling-unit designator) runs
  alone and removed 101 rows (0.34%). The parcel route is recorded in
  `config.PARCEL_COLUMN` as available, with the coverage caveat attached.
- **Three bugs written and caught in one small function, all by reading its
  actual output rather than trusting it.** The care-of scrubber:
  1. A `C.?\s?O.?`-style pattern matched a bare "CO" and turned "STARBUCKS
     COFFEE CO 9699" into "9699" - **the same bare-CO mistake
     `check_personal_exposure.py` made in this project once already**, where it
     matched 567 company names. Now only "C/O", a fully-dotted "C.O." and
     ATTN/ATTENTION are accepted.
  2. "keep the longest side that is not a person" inverted the intent on real
     rows, turning "EL PATIO DE LOS JUGOS USA CORP C/O YOEL HERNANDEZ / ILEANA
     MARTINEZ" into the two people's names - `looks_personal()` does not flag a
     slash-joined pair, and that side was two characters longer.
  3. "keep the first side that is not a person" then kept the trustee in
     "ANDREW L LEWIS TRS C/O MARRIOT HOTEL SERVICES LLC", because a TRS suffix
     defeats the two-token shape test.
  The rule that works ranks sides by a POSITIVE organisation signal and only
  falls back to position, which needed a new shared helper,
  `residence.looks_organisational()` - deliberately **not** the inverse of
  `looks_personal()`, since a name can fail both tests.
- **Ring coverage is the lowest in the project, and that is a scope
  consequence, not a fault.** 3,775 of 29,878 businesses (12.6%) fall inside a
  ring, against New York's 71% and Chicago's 57%. The reason is that the
  regional business set spans all of Miami-Dade - Homestead to Aventura - while
  the rail is one north-south line plus a downtown loop. The within-ring figure
  is the map's real content; the all-businesses toggle is county-wide and
  labelled as such.

### 2026-09-21 - Licence texts now kept in the repo

- **Started storing licence agreements locally, beginning with MassDOT's.** The
  MassDOT Developers License Agreement (4 pages, dated 2009-11-13, 87 KB) was
  moved from the repository root to `docs/licenses/`. It is the first licence
  text the project stores - `git ls-files "*.pdf"` returned nothing before this,
  and the transit licences in `docs/data_sources.md` were quoted from sources
  the file did not even record: grepping the whole licences section for URLs
  returned **one**, MassDOT's, for six agreements. A quote cannot be re-read
  against a source that changed - still less against one with no address -
  and this agreement's §5.1 lets MassDOT "alter the Terms of this License
  Agreement at any time without notice" while §8 reserves the right to "modify
  or revoke this Agreement at any time" - so the URL alone does not preserve
  what was actually agreed to. Re-fetching is not routine either: `mass.gov`
  returns 403 to automated fetches, which is why reading it needed the browser
  and a local PDF extraction. Rejected leaving it at the repository root, and
  rejected converting it to Markdown, which would make the stored copy a
  transcription rather than the document. Changes no compliance state: the
  MassDOT acknowledgement is still required only if Boston is built (required
  notice 7 in `docs/data_sources.md`), and no Boston pipeline code exists.
- **Stated position on storing third-party licence texts: unaltered,
  non-commercial, for compliance reference.** Decided by the project owner
  2026-09-21, because the grant each agency makes covers *the Data* and says
  nothing about its own agreement document, which is a separate copyrighted
  work - SEPTA's explicitly so ("Licensee may not use SEPTA's trademarks and
  copyrighted materials for any commercial or profit-making use and may not
  alter them in any way"). Keeping an unaltered copy for compliance satisfies
  both halves of that clause, and nothing is republished: the repository is the
  archive, not a distribution channel. Rejected the safer alternative of storing
  only SHA-256 hashes and retrieval dates - it detects that an agreement changed
  but leaves you without the wording you actually agreed to, which is the whole
  point. Hashes are recorded *as well*, in `docs/licenses/README.md`.
- **All six texts retrieved and stored the same day, and three retrieval facts
  were wrong in `docs/data_sources.md`.** `docs/licenses/` now holds MassDOT
  (PDF, 87 KB), SFMTA, LA Metro, CTA and SEPTA (whole HTML pages, 37-233 KB)
  and MTA (4.6 KB rendered text). Corrections found in the process: **SEPTA's
  host really is `wwww.septa.org` with four w's** - not the repo README's typo
  the file called it, since `www` and `wwww` each return 200 independently with
  no redirect between them; **SFMTA's licence page is `/reports/gtfs-transit-
  data`**, with the agreement inline above the download link and no separate
  document (`/reports-documents/...` is a 404); and **`mta.info` returns 403 to
  curl even with full browser headers**, so its terms were captured from the
  browser pane as text, the same way the MassDOT PDF needed the browser.
- **The exercise immediately paid for itself: MTA's actual terms had never been
  read, and they are not permissive.** `docs/data_sources.md` recorded New York
  as "Our data feeds are free to use ... Not specified for the GTFS data",
  which is the blurb on `mta.info/developers` - not the agreement at
  `/developers/terms-and-conditions`, which was never opened. That agreement
  carries real obligations, including **"You will not modify or delete any of
  the data"** - the same shape as LA Metro's clause, the one the project treated
  as its tightest - plus "You will not state or imply that the data is accurate,
  complete, or timely" and a prohibition on implying MTA licensed the app. New
  York is a **built** city, so this is not hypothetical. Recorded as an open
  decision in `PLAN.md` rather than settled here; the fact that the terms say
  what they say is not a judgment call, but whether this project satisfies them
  is.

### 2026-09-21 - Transit geometry no longer rounded; the clause it was meant to satisfy turned out to be moot

- **Where this came from.** A concurrent session read MTA's actual terms and
  found **"You will not modify or delete any of the data"** (with a carve-out:
  "You may, however, create an app that uses some but not all of the data") -
  where this project had previously recorded only the "free to use" line from
  MTA's landing page. That raised a real question, because
  `map_common.COORD_DP` rounded **every** coordinate to 6 decimal places
  (0.11 m) before it reached the HTML, transit geometry included.
- **The question was wider than MTA.** The same rounding applied to **LA
  Metro's** `shapes.txt`, and LA Metro's clause is the tighter one - "not
  change, tamper, dismantle, augment, misrepresent or otherwise modify the
  Transport Information". The verdict recorded earlier on 2026-09-21 said the
  project "does not modify it" because "the rail alignment is drawn from the
  feed's own `shapes.txt` geometry and displayed as that line", and rounding
  would have made that sentence true only with an asterisk.
- **Decision: stop rounding transit coordinates; keep rounding business
  coordinates.** Station points, ring centres, line-label anchors and every
  `shapes.txt` vertex now go out at full source precision, via a
  `_transit_coord()` helper that exists so the reason sits at each call site
  rather than only in a comment. `COORD_DP` still applies to business pins and
  both heat layers, which is where the size saving actually is: heat layers are
  33-57% of a rendered map, line geometry 4-6%.
- **MTA's clause, which prompted all of this, turned out to be moot - and a
  first measurement of LA Metro's was wrong in the other direction.** An
  initial check sampled the first few thousand characters of each city's line
  geometry and concluded that MTA, LA Metro, SFMTA and SEPTA all published at
  6 dp, making the rounding a no-op for every restrictive feed. Measuring
  **every vertex** instead:

  | Feed | Max dp | Coords over 6 dp | Was the rounding altering it? |
  |---|---|---|---|
  | **LA Metro** | **10** | **2,606 of 12,426 (21.0%)** | **Yes** |
  | MTS (San Diego) | 8 | 2,499 of 2,518 (99.2%) | Yes |
  | CTA (Chicago) | 8 | 6,359 of 6,410 (99.2%) | Yes |
  | MTA (New York) | 6 | 0 (0.0%) | No - no-op |
  | SFMTA | 6 | 0 (0.0%) | No - no-op |
  | SEPTA | 6 | 0 (0.0%) | No - no-op |

  **So the change was necessary rather than merely prudent, for LA Metro
  specifically** - the tightest licence in the project, being altered on a
  fifth of its vertices. The recorded LA Metro verdict was *not* literally true
  before this; it is now. MTA's feed is genuinely already 6 dp, so the clause
  that triggered the investigation never bit. MTS and CTA were being altered
  too, and neither restricts modification - CTA expressly permits "create
  derivative works" and MTS has no modification clause.
- **Sampling is what produced the wrong first answer, and it is worth naming:**
  LA Metro's feed is mixed-precision, 6 dp for the first stretch of its
  geometry and up to 10 dp later, so any check that reads the beginning of the
  file gets a clean-looking result. The same trap as Philadelphia's "100%
  geometry" reading, which counted non-null values and missed 218 empty ones.
- **Scope was corrected mid-implementation, after the first attempt exempted
  too much.** Exempting *station* coordinates as well made them emit **15
  decimal places** of floating-point noise - because most cities derive a
  station's position by averaging its platform stops
  (`.agg(latitude=("stop_lat", "mean"))`), so those are the project's own
  computed values, not agency data. Station points, ring centres and line
  labels are therefore still rounded; **only the `shapes.txt` vertices are
  exempt**, which is the one place an agency's data is reproduced verbatim.
  That narrowing also removed most of the size cost.
- **Cost, measured after the correction: +23,788 bytes across 16.5 MB
  (0.14%).** New York, San Francisco and Philadelphia are **byte-identical**
  to before; San Diego +5,012, Chicago +12,879, Los Angeles +5,897.
- **Verified before and after implementing, as the owner required:** visually a
  no-op (0.11 m is half a pixel at OSM zoom 19), and structurally a no-op - the
  unrounded vertices also feed the label-placement geometry, where a 0.11 m
  perturbation cannot flip a tail-end choice between line ends kilometres
  apart. Every city re-rendered with **identical row counts and station
  counts**, so only coordinate precision moved. All six committed outputs were
  re-baselined.
- **Also keeps a future foot-gun closed.** `PLAN.md` carries a live
  optimisation for New York's oversized map: "rounding coordinates to 5 dp
  saves 1.4 MB". At 5 dp the old behaviour would have begun altering MTA's
  geometry too, silently, as a side effect of a size tweak by someone not
  thinking about licences. With the exemption in place that optimisation is
  safe to adopt for business points only.
- **One incidental discovery while checking the diffs:** the five
  `excluded_stations.csv` files show as modified in `git status` after a
  re-render but have **zero content change** - it is purely CRLF-vs-LF, which
  git normalises on commit. `drift_check.py` already handles both that and
  Folium's random 32-hex element ids (which change every save, and are why a
  raw diff of `heatmap.html` is meaningless). Neither is drift.
- **The route-colour question is recorded as OPEN, by the owner's decision**,
  rather than resolved by substituting a palette. Three agencies' terms bear on
  it: MTA ("logos, maps and symbols need a separate licence application", free
  but must be applied for), SEPTA (the trademark clause already open), and -
  for a future D.C. - WMATA ("prohibited from using WMATA Intellectual
  Property, including any confusingly similar variants, in association with the
  Transit Data or API unless you have entered into a separate, written license
  agreement"). The project currently uses each agency's own `route_color`
  values for line strokes and labels, with one deliberate exception already
  recorded: Staten Island Railway, lightened for contrast. It joins the
  pre-deploy licence list rather than blocking anything now.

### 2026-09-21 - WMATA's licence read: it does not rule out D.C., but it does rule out the mirror

- **Why it was read now.** WMATA is the first transit feed in the project that
  cannot simply be downloaded - `api.wmata.com/gtfs/rail-gtfs-static.zip`
  returns **401** without a registered key - and the owner asked whether the
  licence might disqualify D.C. on its own before any effort went into getting
  access.
- **It does not. It is more permissive than LA Metro's on the point that
  matters most.** The grant is "a limited, non-exclusive, non-assignable,
  non-transferrable, non-sublicensable, revocable license to download, use,
  reproduce, and redistribute WMATA's Transit Data within your Application",
  there is **no modification clause at all**, and **no attribution is
  required** - unlike MassDOT, SFMTA and LA Metro.
- **But it rules out the Mobility Database mirror, which reverses the easier of
  the two options originally offered.** Redistribution is restricted:
  "prohibited from: sharing (except with your Application's users),
  transferring, sublicensing, selling or leasing any Transit Data, directly or
  indirectly...to any other person", with an exception needing prior written
  authorisation and data "inseparably commingled" with your own. Publishing a
  map to the site's own visitors is sharing with the Application's users and is
  fine. Taking the feed from a third-party mirror is not the safe shortcut it
  looked like: it relies on a redistribution the terms appear to prohibit, and
  it means obtaining the data **outside** the licence rather than accepting it.
  **The key is the correct route; the mirror is the worse one.**
- **The "secret in the pipeline" objection was overstated and is withdrawn.**
  GTFS fetching already lives in non-`step*.py` scripts so that
  `drift_check.py` stays offline and deterministic, so a WMATA key would be a
  local environment variable used for an occasional manual refresh. It never
  reaches Streamlit Cloud, which only reads `outputs/`. That is a much smaller
  change than first described.
- **What remains true and worth knowing:** keys "remain WMATA's property and
  may be revoked or otherwise limited at any time", cannot be sold,
  transferred or sublicensed, and "enable WMATA to associate your API activity
  with your Application". Registration is the owner's action - an account
  cannot be created on their behalf.

### 2026-09-21 - Screened every remaining candidate city, and found three the shortlist never had

- **Why this happened before the next build**, rather than building Boston: the
  owner chose to screen the whole remaining list for licensing and viability
  dealbreakers first, then decide which cities to build and which to exclude.
  That ordering paid for itself immediately - Dallas fell, and three candidates
  appeared that were not on the list at all.
- **Washington D.C. is the strongest remaining candidate, and the first
  non-NAICS city with all three buckets from one registry.** 76,107 active
  licences: Food Services 4,901, Beauty and Grooming 486, and ~1,550 real
  retail once the catch-all is removed. Three findings decide how it must be
  built, and all three came from the distribution check the 2026-09-18 pass
  never ran:
  - **`BUSINESSACTIVITY = 'General Business'` (14,770 rows) is an
    office/professional catch-all and must be excluded.** Sampled 40 rows:
    Nossaman LLP, Gannett Fleming Engineers and Architects, Voith & Mactavish
    Architects, Brown and Caldwell, consultancies, investment and tech firms.
    It is 14,729 of the 16,282 rows in "General Sales and Services", so
    including it would have inflated D.C.'s retail roughly tenfold with law
    offices. Same role as Los Angeles' NAICS 812990.
  - **49% of active rows are residential rentals** - One Family Rental 25,587,
    Apartment 6,106, Two Family Rental 2,560, Short Term Rental 2,197, Vacation
    Rental 803. Philadelphia's landlord-registration pattern, at half the share.
  - **The recorded "truncated to whole degrees" caveat is worse than recorded,
    and also harmless.** `LATITUDE` is literally `39` and `LONGITUDE` `-77` on
    every row: **0 of 76,107 fall inside D.C.** But `X_COORDINATE`/
    `Y_COORDINATE` are real, present on 77% of storefront rows, and are
    **EPSG:26985** - verified by transforming 312 Pennsylvania Ave SE to
    (38.88715, -77.00153), with the three plausible datum variants agreeing to
    sub-metre. `MAR_ID` should recover the remaining 23% without the Census
    geocoder, so the old caveat's "use address geocoding" is now the fallback
    rather than the plan.
  - Also measured: trade name missing on **49%** of storefront rows (the Los
    Angeles trap at half severity), `PREMISEINDC='Yes'` on 61,329 rows as a
    better in-city marker than `WARD` (null on 16,806 and mixing "Ward 2" with
    "2"), `SSL` parcel IDs on 45,476 for the residence check, and
    `BUSINESSOWNER*`/`AGENT*` person-name columns on ~34k rows that must never
    be published.
- **WMATA is the first transit feed in the project that cannot simply be
  downloaded.** `api.wmata.com/gtfs/rail-gtfs-static.zip` returns **401**
  without a registered API key. That is an access question rather than a
  licence one, and it has two answers: a free key from
  `developer.wmata.com/signup` (which would put a secret in the pipeline,
  something no other city needs) or the keyless Mobility Database mirror. Not
  decided here. `developer.wmata.com/license` is **unread**, and transit terms
  have been the loosest end of every licence review, so it is flagged rather
  than assumed.
- **Dallas ruled out, on currency rather than schema - a different reason from
  the one recorded on 2026-09-18.** Its only source with a classification, a
  business name and coordinates (`9qet-qt9e`, PDDL, 23,731 rows, `land_use`) is
  frozen: `date_issued` spans 2018-01-02 to **2022-11-15**, rows last changed
  2022-11-16. `ync5-xnfn`, the dashboard `PLAN.md` told us to check for
  something fresher, **is not a dataset** - HTTP 403 "no row or column access
  to non-tabular tables", 0 columns - which closes that open question with a
  negative. The fresher food file (`dri5-wcct`) is named "October 2016 to
  January 2024", declares no licence, and has no business-name column. Of 1,087
  assets on the domain, nothing business-classified is current. Texas requires
  no general city business licence, so the certificate of occupancy *is*
  Dallas's registry and it stopped publishing. **Reasoning: a four-year-old
  snapshot beside six current cities is a worse comparability problem than any
  thinness**, and unlike thinness it cannot be disclosed away on a city page.
  Houston fails the same way and for the same structural reason (zero results).
- **Three candidates found that were never on the list**, all from widening the
  screen past the "25 largest cities" frame to rail cities of any size:
  - **Miami** - Miami-Dade "Local Business Tax" ArcGIS layer, **194,099 rows**,
    `ACCSTATUS`, NAICS via `BUSNAICSCD` (so no new taxonomy module), real
    `LAT`/`LON`, `FOLIO` parcel IDs, and `MUNBUSLOC` to cut county data down to
    "01 - MIAMI". Needs a real Step 0.
  - **New Orleans** - `iqay-p646` "Active Occupational Licenses", 16,396 rows,
    and **CC0 1.0, the cleanest declared licence of any candidate**. Rail is
    streetcar-only, which is a scope question for the owner rather than a data
    one.
  - **Kansas City** - explicitly PUBLIC_DOMAIN, 15,895 rows, geocoded, all
    three buckets in readable categories (Beauty Salons 662, Barber Shops 146,
    Clothing Retailers 192, Supermarkets 154): the best data-to-effort ratio
    found. **Recommended for exclusion on rail, not data** - one short
    streetcar line, well under the bar every built city meets. Recorded that
    way deliberately, because "no usable data" and "not enough rail" are
    different verdicts and only one of them can be reversed by a better dataset.
- **Recorded fifteen cities as "screened and not found", explicitly NOT as
  disqualified.** Atlanta, Baltimore, Portland OR, Phoenix, Minneapolis, St.
  Louis, Cleveland, Pittsburgh, Detroit, Jersey City, Tucson, Sacramento, Salt
  Lake City, Honolulu and Buffalo. Twelve of those domains returned HTTP 404
  from Socrata's discovery API, which means **"not a Socrata domain", not "no
  data"**, and the ArcGIS pass searched dataset titles only. **Seattle is the
  proof that the distinction matters**: it returned "no matching datasets" on
  Socrata and then turned out to have an official 54,604-row active
  business-licence layer on ArcGIS. This is the Denver and San Jose lesson
  pointing the other way - a shallow check is as unreliable for ruling a city
  *out* as for ruling one *in* - so the list is kept as a to-check queue rather
  than a rejection pile.
- **Method note worth keeping: Socrata's cross-domain discovery API
  (`api.us.socrata.com/api/catalog/v1`) answers "does any public portal publish
  this" in one request**, including the declared licence and the last-updated
  date. It is what established that no Massachusetts salon source exists
  anywhere, and what surfaced New Orleans and Kansas City. Its blind spot is
  everything not on Socrata - which is most cities, and which is why the ArcGIS
  Online search API (`arcgis.com/sharing/rest/search`) is a necessary second
  pass.

### 2026-09-21 - Seattle: deferred, then scoped as the first multi-municipality city

- **Sequence, because it changed twice in one session.** Seattle was first
  "ignored" during the candidate screen, then clarified to "we will return to
  implementing Seattle later on", then scoped by the owner as the project's
  first test of merging several jurisdictions' business data into one map, with
  **full line coverage** of Link's 1 and 2 Lines. Its own registry findings
  were kept rather than discarded, so returning to it costs no re-probe.
- **This supersedes the standing rule that stations in another city are a new
  project rather than a config change.** That rule was set when San Diego
  dropped 16 Trolley stations in neighbouring cities, on the grounds that
  including them would need those cities' own business data sourced and
  verified separately. The rule stands for every other city - Seattle is an
  owner-decided exception, and the deliberate test of whether the multi-source
  idea works.
- **The jurisdiction list is wider than the seven named**, which is a sizing
  fact rather than a change of intent. The owner named Seattle, Shoreline,
  Lynnwood, Tukwila, Federal Way, Bellevue and Redmond. Link also stops in
  **Mountlake Terrace** and **SeaTac** on the 1 Line and **Mercer Island** on
  the 2 Line, and a Federal Way scope brings the extension through **Des
  Moines** and **Kent** - about **ten to twelve** jurisdictions. To be settled
  from the real GTFS stop set against a Washington municipal boundary layer
  rather than from memory, which is the discipline that caught San Diego's 16
  and Los Angeles' 54. The corrected list is written into the probe script so
  it is not re-derived.
- **What the architecture already supports, and what it does not.** Supported:
  per-jurisdiction taxonomy modules mapping into the shared three buckets,
  because `map_common.py` never names a taxonomy; if several Washington cities
  use NAICS they share the existing module. Not yet existing: multi-polygon
  scope (`CITY_KEEP` and the boundary filter assume one city),
  per-jurisdiction provenance on each business row (so the map can say which
  registry a pin came from, and so one city's data going stale is visible), and
  a cross-registry dedup rule for businesses licensed in more than one
  jurisdiction.
- **Two risks recorded now.** A jurisdiction with no usable registry would
  render as an empty suburb rather than an unsurveyed one - the same failure
  that made Boston's `Business Inventory` unusable as a heat layer, so decide
  up front what the map does where data is missing. And the page name needs a
  decision: the project is never named after a city, and a map spanning twelve
  of them is honestly "Link light rail" rather than "Seattle".

### 2026-09-21 - Boston Step 0: passed, and narrower than the shortlist assumed

- **Verdict: viable, two buckets, not built.** Boston passes all three Step 0
  requirements - business data, transit, boundary - and is the thinnest and
  narrowest candidate the project has evaluated. Recorded rather than built:
  the project owner chose to probe the remaining candidates (D.C., Dallas and
  the rest of the list) for licensing and viability dealbreakers first, then
  decide which to build and which to exclude. No pipeline code was written.
- **The whole catalogue matters, not the search hits.** Seven search terms
  against CKAN's `package_search` returned 48 packages; `package_list` returns
  **247**. The extra 199 held the city boundary layer, the SAM address points
  and the Property Assessment roll - all three directly relevant, none of them
  surfaced by the obvious queries. Pull the full list.
- **Boston licenses food and alcohol, and no other trade.** Inspectional
  Services covers food; the Licensing Board covers alcohol, lodging, billiards
  and bowling. Deduplicated to premises: Food service 2,237, Retail 385
  unambiguous (`RF`-only), plus 306 package stores and 43 cannabis shops that
  *overlap* the `RF` set. So a "commercial density" map of Boston built from
  licences is really a **food density** map - a narrowing of the project's
  premise that had to be named rather than absorbed.
- **The official "Active" extract is the wrong file, and the reason is a
  silently missing category.** `Active Food Establishment Licenses` (3,345
  rows) is exactly `FS` 1,762 + `FT` 1,583 licences and contains no `RF`
  (Retail Food) at all - which would have made Boston a **one-bucket** city and
  probably disqualified it. The 902,651-row inspections history carries the
  same `licensecat` field including `RF`'s 504 active premises, and has better
  coordinates too: 99.9% of active premises versus 93.8%. Found by asking the
  history for `SELECT DISTINCT licensecat` rather than trusting the extract's
  own two values - the same move that filled Philadelphia's taxonomy.
- **Personal services is absent, not thin - and that was verified, not
  inferred.** Massachusetts licenses cosmetology and barbering at state level
  and publishes no address-bearing export; its register is a per-licence
  ePLACE/MADOL lookup. Checked three independent ways: Socrata's cross-domain
  discovery API returns **no Massachusetts source** for cosmetology, barber,
  salon, hair, nail salon, body art or tattoo (the only MA domains indexed are
  an education portal and state spending); `data.mass.gov` is not a data portal
  at all, returning HTML 404 from both Socrata and CKAN entry points; and
  `opendata.mass.gov` does not resolve. Same structural cause as Philadelphia,
  and the second city where a bucket has no source in the entire jurisdiction.
- **Rejected the one source that would have made Boston a three-bucket city,
  on coverage grounds.** `Business Inventory` is a summer-2025 field census
  with almost exactly this project's taxonomy - `Beauty_Services` 243
  (Hair_Salon 101, Barber_Shop 46, Nail_Salon 32), Clothing_Store,
  Jewelry_Store, Laundry, Tailor - carrying WGS84 coordinates on 99.8% of rows
  and even a vacancy flag. Its own notes state the limit: "every storefront in
  downtown Boston, as well as comprehensive data on 3 major commercial
  corridors in Mattapan, Jamaica Plain, and Allston." Measured: 37 occupied
  0.01-degree cells, 18 ZIPs, 14 rows in Brookline. **A heat surface built on a
  partial survey shows where surveyors walked, not where commerce is**, and
  mixing it into the heat layer would make four areas read as three-bucket and
  the rest as two. Recorded in `docs/data_sources.md` as available and
  deliberately unused, with the trigger for revisiting it (a city-wide survey).
  It is also the only dataset on the portal whose licence is `notspecified`, so
  using it would require establishing terms first.
- **Trade-name convention is inverted here, which would have broken a copied
  step 2 quietly.** In the food data `dbaname` is blank on **99.0%** of rows
  while `businessname` is never blank and holds the trade name. Every built
  city prefers the `dba` column, so a copied step 2 would have fallen back to
  near-nothing rather than failing loudly. Measured because the `add-city`
  skill requires checking the trade-name blank rate - the check that caught Los
  Angeles' 68% and ~4,000 individuals' names. (The Licensing Board sets use the
  normal convention, so the two cannot share one rule.)
- **CRS verified by transformation, not by inspection.** `gpsx`/`gpsy` look
  like Massachusetts State Plane and are: EPSG:2249 puts Copley Square at
  (42.3486, -71.0788) and Brighton Avenue in Allston, while EPSG:26986 - the
  metre-based sibling of the same state plane, the plausible wrong answer -
  lands everything near 60 degrees north. Boston's own projected CRS would be
  EPSG:32619 (UTM 19N), derived from longitude rather than copied.
- **71 of 125 rapid-transit stations are inside Boston.** The other 54 lie in
  Brookline, Cambridge, Somerville, Newton, Medford, Malden, Quincy, Revere and
  Milton - the entire Green Line C corridor is Brookline. Consistent with San
  Diego's 16 of 63 and Los Angeles' 54 of 110: the boundary filter is not
  optional. Four stations fall marginally outside because the boundary layer
  excludes water, and they do not all resolve the same way - Boston College at
  6.7 m is genuinely a Boston station, Central Avenue at 29.7 m is genuinely
  Milton - so a distance tolerance cannot separate them and a MassGIS multi-town
  layer is needed to name the municipality. Green Line is four street-running
  branches on a shared central subway: San Francisco's shape, so
  `docs/sub_transit_line_filters.md` would apply. The 14 `CR-*` Regional Rail
  lines would be excluded, as commuter rail has been in every built city.
- **Licences: the cleanest city so far, with one obligation.** Every source
  used is **ODC-PDDL**, a public-domain dedication declared per dataset. The
  MBTA feed declares no licence in `feed_info.txt`, so the MassDOT Developers
  License Agreement was read in full: it grants use, reproduction and
  redistribution, **expressly permits combining the data with other data**
  (§4.2), and contains **no restriction on modification** - the direct opposite
  of LA Metro's clause, the tightest in the project. It requires one notice,
  "Clearly acknowledge MassDOT as the provider of the Data" (§4.1), and forbids
  reproducing MBTA logos or trademarks, which this project satisfies by
  construction since it draws its own geometry and reproduces no roundel. Added
  to the required-notices list as conditional on Boston actually being built,
  so it is not mistaken for an outstanding compliance item today. Reading it
  needed the browser and then a local PDF extraction, because `mass.gov`
  returns 403 to automated fetches and the agreement is a PDF the browser
  downloads rather than renders.
- **Corrected a stale count in `docs/data_sources.md`.** The required-notices
  preamble said "three sources require specific text, and one of the three is
  already satisfied", which had not matched its own list since LA Metro was
  added as item 4. Now states four required with one satisfied, and separates
  the conditional ones (New York, MassDOT) from the encouraged one (CTA).

### 2026-09-21 - San Diego, done properly: 315 pins, not 42

- **The 42 was a method artifact, as suspected, and the corrected figure is
  315 (2.80%)** - 7.5x higher, and in line with San Francisco's 1.19% and Los
  Angeles' 2.05% for a city that is far more suburban and single-family than
  either.
- **The right question here is "which parcel is NEAREST", not "which parcel
  contains this point".** San Diego's business coordinates sit 5-15 m outside
  their own lot - placed at the street frontage, and SanGIS parcels exclude
  road right-of-way - so a point-in-parcel test matched 1 of 30 sampled pins.
  The earlier filter fell back to "every parcel within 25 m must be
  residential and owner-occupied", which is a different question and clears
  any home with a rental next door.
- **Two wrong turns before the working method, both recorded in
  `fetch_parcels.py` so they are not retried.** `PLAN.md`'s own advice - bulk
  download the parcel centroids - was wrong in practice: `orderByFields`
  sorts 664,662 rows and `resultOffset` deep-pages through them, costing ~26 s
  per 2,000-row page, about two hours. Abandoned at 2.7%. The advice has been
  corrected in place rather than left to mislead.
- **What works: `returnCentroid=true` on a per-point BUFFERED query.** This
  layer supports centroid-only responses, so one request per point returns the
  candidate parcels' centroids and the nearest is chosen locally - true
  nearest semantics in 2,463 requests rather than ~5,000, with no deep paging.
  95.5% found a parcel, zero failures.
- **Checked the obvious flaw in that shortcut rather than assuming it away.**
  The query buffer measures to the parcel BOUNDARY while ranking uses the
  CENTROID, so a large parcel whose edge is within 25 m can have a centroid
  hundreds of metres away - which could misattribute a business to a small
  neighbouring house. Measured: every one of the 315 flagged rows has its
  chosen centroid within **39.1 m** (mean 22.2, median 21.6), because
  single-family lots are small. The 1,406 m outlier in the overall
  distribution belongs to *unflagged* rows on large non-residential parcels -
  the harmless direction.
- **The removed rows validate the filter by their own classifications**, which
  is stronger evidence than any distance statistic: 286 of 315 carry no
  suite or unit, and the NAICS descriptions include **23 "COTTAGE FOOD
  OPERATOR"** - California's licence category for food produced in a *home
  kitchen*, definitionally a home business - plus 20 "BEAUTY SHOPS - BOOTH
  RENTAL" (a chair renter, not a premises, the same pattern the
  `multi-source-city` skill flags for New York's `DOSAERENTER`), 66 "other
  personal services" and 20 beauty salons.
- **Rate limit measured rather than guessed.** SANDAG's gateway sustains
  roughly 2 requests/second for a run this long: ~7 req/s completed once, a
  marginally faster attempt was refused after ~500. The script now defaults to
  1 worker at 0.4 s (~20 minutes) and **aborts after 25 refusals writing
  nothing** - which it did, once, costing only time. A partial cache is the
  one outcome worth avoiding, because it filters only where the lookup
  happened to succeed.
- **Reintroduced and then re-fixed the prefilter bug**, an hour after fixing
  it in Los Angeles. When the bulk fetcher stopped reading business data the
  prefilter snapshot looked like dead code and was deleted; the per-point
  version then read step 2's *filtered* output, on the reasoning that "the
  filter only removes rows, so the candidate set can only shrink". True, and
  beside the point: the shrinkage is exactly the rows that must stay removed,
  and without cache entries they return. Restored, with the reason stated in
  all three files.
- **No apartment rule for this city**, stated in the code rather than left
  looking like an omission: that rule reads a dwelling-unit designator out of
  the address, and this registry's `address_suite` holds bare values ("A",
  "101") with no APT/UNIT token. Residual: 1 pin (0.04%).

### 2026-09-21 - Los Angeles filtered; two of my own bugs, and a WAF block

- **Los Angeles: 1,252 pins removed** (61,208 -> 59,956, 2.05%), the largest of
  the three. NAICS 453990 misc retail (120), 452000 general merchandise (87),
  812112 beauty (86), 812111 barber (75), 812190 other personal care (72).
  Lookup coverage 99.9%, zero request failures.
- **Bug 1: a buffer changed the question, not just the coverage.** An exact
  point-in-parcel test matches only 49% of LA's pins, because the 9% of
  coordinates recovered by Census geocoding land on street centrelines. I
  buffered to 25 m to fix that - but a buffer returns SEVERAL parcels, and
  requiring all of them to be owner-occupied means one rented neighbour clears
  a genuine home. It removed **95** rows where the exact test implied ~1,000.
  Corrected to use the containing parcel where there is one (8,433 pins) and
  the buffer only otherwise (6,474), which is 1,252. **Caught only because the
  sample measurement and the implementation disagreed tenfold** - which is the
  argument for measuring before building, not after.
- **Bug 2: the fetcher read its own consumer's output.** It loaded step 3's
  filtered file, so the cache would have omitted the rows already removed and
  they would have silently returned on the next run. Step 3 now always writes
  an unfiltered `businesses_geocoded_prefilter.csv` that the fetcher reads, so
  the two cannot get out of order whatever someone runs first. Same pattern
  added to San Diego.
- **A real bug in `scripts/check_personal_exposure.py`, corrected.** Its
  residential/commercial unit lists contradicted their own source write-up,
  `docs/passover_name_filtering_skill.md`, on three designators: FL/FLOOR and
  RM/ROOM were residential here and commercial there, and SPC was reversed. An
  office floor is not a dwelling, so **every city's residential share was
  overstated in the same direction**. Corrected shares: LA 5.81%, SF 1.55%,
  Chicago 0.20%, NY 0.09%, San Diego 0.04%, Philadelphia 0.00%. A bare `LOT`
  is deliberately NOT adopted as residential despite the source listing it: in
  these registries it is at least as likely to be a parking lot, and it could
  not be verified either way, so adopting it would trade a known error for an
  unknown one.
- **San Diego: blocked by SANDAG's WAF, and nothing was shipped.** An 8-worker
  run drew HTTP 403 from an Azure Application Gateway after ~750 requests. The
  lookup swallowed every exception alike, so it reported "1,706 failures"
  rather than "we are blocked", and wrote a 757-row cache covering 31% of the
  population. **That cache was discarded rather than used**: a filter built on
  it would have removed home businesses only where the lookup happened to
  succeed - the same partial-coverage error already rejected for San
  Francisco's 43.8% address join. The fetcher now treats 403/429 as their own
  signal, defaults to 2 workers with a delay, and aborts after 25 refusals
  writing nothing. San Diego's map is unchanged and its filter is inert until
  a complete lookup exists.
- **Still outstanding: the apartment population.** The parcel filters catch
  people at *houses*. A person-like name at an APT/UNIT address in a
  multi-family building is a different population the single-family test
  cannot reach, and after the parcel filters it is still 844 pins in Los
  Angeles (5.81%) and 194 in San Francisco (1.55%).

### 2026-09-21 - Home-business filters built, starting with San Francisco

- **Decided to fix the already-mapped cities before adding Boston**, at the
  project owner's direction, rather than carry a known live exposure on a
  public repository while the city list grows.
- **San Francisco: 217 pins removed** (18,242 -> 18,025), exactly matching the
  measurement. A person-like displayed name at a parcel the Assessor calls
  Single Family Residential which also claims a homeowner's exemption. Mostly
  NAICS 722320 caterers, 812112 beauty, 812910 pet care, 458110 clothing.
- **Shared logic now lives in `pipeline/residence.py`** rather than being
  written three times. It holds the person-name test - which was already
  duplicated between Philadelphia's step 2 and
  `scripts/check_personal_exposure.py` - plus `flag_home_based()`, which takes
  each city's own residential / owner-occupied / individual columns and
  requires all supplied conditions together. The module docstring carries the
  measured counts from every city, because the mistake it exists to prevent
  (treating land use alone as a privacy signal) is the one a future reader is
  most likely to make.
- **Each city's property download lives in a non-`step*.py` script** writing
  into gitignored `raw/`, so `drift_check.py` stays offline and deterministic.
  San Francisco's `fetch_sources.py` deliberately fetches ONLY the new
  Assessor roll: re-downloading its business export would change every count
  recorded in this file and should be a deliberate act, not a side effect.
- **Two things recorded so they are not rediscovered.** San Francisco's roll
  must be fetched from `data.sf.gov` - `data.sfgov.org` returns 403 on
  `/resource/` while `/api/views/` succeeds, which makes the dataset look
  unavailable. And the join must be spatial: an address join reaches 43.8%,
  which was rejected outright rather than used, because a filter running off a
  partial join removes home businesses only where the address text happened to
  match - arbitrary while appearing complete.

### 2026-09-21 - The California cities have a systemic home-business exposure

- **Los Angeles is worse than San Francisco, and this is now a workstream
  rather than a footnote.** A random sample of 400 of its person-like pins
  (seed 20260921) put **7.2% on a Residential parcel claiming a homeowner's
  exemption**, which extrapolates to **~1,081 of 14,921 person-like pins
  (~1.77% of 61,208)**. Only 53.2% of the sample matched a parcel at all, and
  among those that did the rate is 13.6%, so the honest range is **~1,000-2,000
  pins**. The unmatched are expected to be the ~9% of LA coordinates recovered
  by Census geocoding, which land on street centrelines rather than inside a
  parcel.
- **The same signature as San Francisco**: NAICS 812111/812112 barber and
  beauty, 812910 pet care, 812190, 722320 caterers, 453220 gift shops, 452000
  general merchandise - with `UseDescription` "Single" on 27 of the 29 hits.
- **Both cities already excluded NAICS 812990 on 2026-09-21 for this exact
  reason.** That exclusion worked on the code that *names* itself a catch-all;
  what is left is the same home-based pattern hiding under codes that are
  entirely legitimate for a real storefront, which is why no blanket NAICS
  exclusion can reach it and a property join is the only way to see it.
- **So the unit-indicator test was not slightly optimistic, it was blind in the
  two largest NAICS cities.** Philadelphia's 8 pins made this look like a
  rounding error; California's two cities put it at four orders of magnitude
  more. San Diego - also California, also NAICS, with 24,974 SOLE
  proprietorships and no residence signal of any kind - is now the most likely
  to be worse still, and remains unmeasured.
- **Recommended sequencing change: fix these before adding Boston.** Each new
  city otherwise adds to a known, live exposure on a public repository, and the
  method is now proven on three cities. Raised for the project owner rather
  than acted on, because it re-orders the agreed roadmap.

### 2026-09-21 - San Francisco has a real home-business exposure: 217 pins

- **Checked San Francisco "just to be sure" and it is the one city where the
  answer changed.** 217 pins (1.19% of 18,242) display a person-like name at a
  parcel the Assessor classifies **Single Family Residential** *and* which
  claims a **homeowner's exemption** - California's homestead analogue, granted
  only on an owner-occupied primary residence. That is 27x Philadelphia's 8,
  and the largest personal-data exposure found anywhere in this project.
- **What they are leaves little doubt**, from the NAICS of the affected rows:
  722320 caterers (16), 812112 beauty salons (15), 812910 pet care (10),
  812199 other personal care (8), 458110 clothing (11), 722511 restaurants
  (11). Home caterers, home hairdressers, home nail technicians - exactly the
  pattern that got NAICS 812990 excluded in this city and in Los Angeles on
  2026-09-21, reappearing under codes that are perfectly legitimate for a
  storefront and so were never candidates for a blanket exclusion.
- **The measurement took three attempts, and the first two were wrong in ways
  worth recording.** v1 joined on `data.sfgov.org`, which returns 403 on
  `/resource/` while `/api/views/` works - it looked as though the datasets
  were unavailable when the project's own recorded domain is `data.sf.gov`. v2
  joined by address and reached only 43.8%, because the Assessor's
  `property_location` is a **fixed-width composite**
  (`'0000 2801 LEAVENWORTH         ST0000'` is
  `<secondary> <house no> <padded street> <type><4 digits>`), and because
  stripping direction words destroyed "North Point" and "South Van Ness" on
  both sides. v3 abandoned addresses entirely: the roll carries `the_geom` as a
  **point**, so a nearest-parcel join in EPSG:32610 matched **93.4% at a median
  distance of 1.4 m**.
- **43.8% was not good enough to filter on, and that mattered.** A filter
  running off a partial address join would have removed home businesses only
  where the address text happened to match - arbitrary in a way that is worse
  than not filtering, because it looks complete.
- **The mixed-use lesson held for a third city.** San Francisco's largest
  category under its pins is **Multi-Family Residential at 5,733** - ground-
  floor retail in residential buildings - so it is excluded from the filter
  exactly as Philadelphia's `APARTMENTS > 4 UNITS` and New York's
  `Multi-Family` were.
- **Not yet filtered.** The fix needs the Assessor roll added as a San
  Francisco source and a spatial join in its step 2, which is a real change to
  a built city rather than a line of config. Raised with the measured numbers
  rather than actioned in passing; see `PLAN.md`.

### 2026-09-21 - Residence exposure checked across all six cities

- **Philadelphia's finding made every other city's residence figure suspect, so
  all five were checked before moving on.** Result: **three are now settled and
  need nothing, and none of the three needed a filter except Philadelphia.** The
  work was worth doing mainly for what it ruled out.
- **New York: measured 0.02%, no filter needed.** Two of its four registries
  carry `bbl` (NYC's tax-lot id) - DOHMH on 99.4% of rows, DCWP on 80.8% - so
  PLUTO (`64uk-42ks`, 858,284 lots) joins **by key rather than spatially**,
  which is far cheaper than Philadelphia's. 62.6% of mapped rows joined (the
  two NYS state registries carry no BBL). Of 62,444 rows, only **115 sit on a
  "One & Two Family" lot (0.18%)**, and just **10 of those display a
  person-like name (0.02%)** - all with `units_res=2` and all ordinary trades
  (Pizza, Coffee/Tea, Caribbean, Electronics Store, Secondhand Dealer), i.e.
  shops in two-family rowhouses.
- **That also turned the decision to keep New York's 161 surname-first DCWP
  names from a precedent-based call into an evidence-based one: exactly ONE of
  them is on a residential lot.** The earlier entry justified keeping them by
  analogy to San Diego; this measures it.
- **The mixed-use trap reproduced at scale.** New York's single largest
  land-use category is `4 Mixed Residential & Commercial` with **20,257 pins**,
  ahead of `5 Commercial & Office` at 14,251. Had the Philadelphia filter used
  land use alone, or counted mixed use as residential, it would have removed a
  third of New York's map.
- **Chicago: already clean, and the recorded claim verified.** Its
  `business_activity` field marks home-based businesses explicitly ("Other Home
  Based Businesses", "Home Repair Services (Home Based Business)" - 4,207 raw
  rows mention home or residential), and **zero** survive into
  `businesses_clean.csv`: the `chicago_license` taxonomy already drops them.
  The 20 residual mentions are "Home Repair Services" as a *service offered* by
  merchandise retailers, which are real storefronts.
- **Signals found but not yet built, with endpoints recorded** so the work is
  scoped rather than researched again:
  - **San Francisco** - "Assessor Historical Secured Property Tax Rolls"
    (`wv5m-vpq2`, PDDL) carries `use_definition`, `property_class_code`,
    `number_of_units` and `exemption_code_definition`, the homeowner's
    exemption that is California's homestead analogue. Its registry has no
    block/lot, so it needs a spatial join via Parcels (`acdm-wktn`, PDDL)
    first. The standalone Land Use layer (`fdfd-xptc`) is **[ARCHIVED]** and
    should not be the primary source.
  - **Los Angeles** - `public.gis.lacounty.gov/public/rest/services/
    LACounty_Cache/LACounty_Parcel/MapServer/0` exposes AIN/APN and address but
    not owner data (restricted by California Government Code s7928.205), and
    the use-type attribute lives in the separate Assessor Parcels tabular
    dataset, joinable by AIN. Two steps, so medium effort.
  - **San Diego** - the weakest position and the one with no signal at all
    today. SANDAG/SanGIS parcels carry `ASR_LANDUSE` (91 types) and
    `NUCLEUS_USE_CD` (225 types), but the hosted layers are split
    geographically (`Parcels_South` and siblings) and the registry has no
    parcel id, so it needs a spatial join across several layers.
- **Decided: leave those three to the pre-deploy batch, San Diego first.** The
  measured prior across the three cities that could be checked is 0.02%, 0.00%
  and 8 pins, so the expected exposure elsewhere is small - but San Diego is
  ranked first because its residence figure is not merely low, it is
  **unmeasurable**: its `address_suite` holds bare values ("A", "101") with no
  APT/STE token, and 903 of its pins display a name identical to the owner's.
  A low number and no number are different things, and only San Diego has the
  latter.

### 2026-09-21 - Testing the residence signals: one works, one is worthless

- **Tested the two signals the previous entry proposed, instead of trusting
  them.** The unit-indicator residence test can only fire on an
  `APT`/`FL`/`RM`/`#`, so a sole trader at a detached house reads as clean -
  which is why Philadelphia measured 0.00%. Both candidates were checked
  against the City's own property register (`opa_properties_public`, 583,779
  rows, joined on `opa_account_num`, matching 94% of licences).
- **A mailing address matching the premises is worthless as a signal: 41.9% of
  mapped pins.** A shop's mailing address is normally its own premises. It was
  removed from `PLAN.md` as a thing to build rather than left there to mislead
  someone later, and Philadelphia's pipeline downloads no mailing address at
  all.
- **Parcel land use works, but is NOT a privacy signal on its own, and this is
  the generalisable part.** In a dense city, shops sit inside residential
  buildings: "purely residential parcel" flags 7.95% of pins, including **147
  thirty-plus-seat restaurants on `APARTMENTS > 4 UNITS` parcels** and 92 on
  `MULTI FAMILY`. Acting on land use alone would have deleted hundreds of real
  storefronts to remove a few dozen homes.
- **The best signal was one not proposed: the homestead exemption**, which
  Philadelphia grants only on an owner's primary residence - a claim the owner
  made to the City, not an inference. It also over-fires alone (2.22% of pins,
  of which 162 are `MIXED USE`).
- **So 0.00% was a false negative, and the corrected figure is ~0.1-0.5%.** The
  model's *conclusion* survived - the exposure is still negligible and every
  affected row is a licensed food premises - but its *precision* did not, and
  the number it reported was wrong.
- **Filtered the narrow, defensible set: 8 pins.** A person-like displayed name
  AND an `Individual` entity AND a parcel the City classifies as purely
  residential. All 8 are `SINGLE FAMILY`; 5 are "Food Preparing and Serving"
  and 2 are caterers, i.e. home kitchens. Framed as **scope first** - a food
  licence at a house the owner lives in is not a storefront - which is the same
  framing as `Rental` and the project-wide NAICS 454 exclusion.
- **Reversed course on including the homestead exemption as a filter
  condition.** An earlier version used it as an alternative to the land-use
  test and removed 17 rows - but 8 of those sat on `MIXED USE` parcels, the
  rowhouse with a shop below and the owner's flat above, which is a real
  storefront and arguably Philadelphia's most characteristic one. Deleting
  those contradicted both the filter's own justification and the reasoning that
  kept San Diego's sole proprietorships. The exemption is now **reported by
  `check_personal_exposure.py`, not acted on**: it names 11 person-like pins on
  owner-occupied parcels and says in the output why they are kept.
- **`MIXED USE` and `APARTMENTS > 4 UNITS` are deliberately absent from
  `PARCEL_RESIDENTIAL`**, with the counts that justify it in the config
  comment, because that is the mistake a future reader is most likely to
  "correct".
- **Written into the `add-city` skill's Step 0**, since it applies to every
  city: check for a joinable property register, and pair an occupancy signal
  with a name or entity-type test rather than acting on either alone.

### 2026-09-21 - One published email address, and a gap in the exposure check

- **Found exactly one email address published across all six maps**, in New
  York: a DCWP "Tobacco Retail Dealer" pin whose registered business name *is*
  a personal Gmail address, displayed at a mapped coordinate. Found while
  grepping the repo for an unrelated reason, not by any check the project runs.
- **`scripts/check_personal_exposure.py` could not have caught it.** It tests
  whether a displayed name looks like a *person's name* and whether the address
  carries a unit indicator. An email address matches neither test: it fails the
  `PERSON` regex and contains an `@`, which `NOT_A_NAME` does not list. So the
  check reported this city as clean on its own terms and was right to - the
  terms were incomplete. Contact details are a different exposure from names,
  and arguably a worse one: a name at a commercial address identifies a
  business, while an email address is a direct line to a person.
- **Counted first, across every city, before deciding anything**: 1 email and
  0 phone numbers in 91,000 pins. So this is one row, not a pattern - which is
  why it is recorded as its own decision rather than folded into a sweep.
- **Decided: scrub contact details in shared code.** A displayed name holding
  an email address or phone number is treated as a row with no usable public
  trade name and dropped, the way a blank one would be - masking to
  `JO***@GMAIL.COM` would still leak a partial. Implemented as
  `drop_contact_details()` in `pipeline/map_common.py` and applied inside
  `render_heatmap`, deliberately **not** in the step 2 of the city that
  happened to have the problem: that is the one place every city's pins pass
  through, so a city added later cannot reintroduce it by forgetting.
- **It was 3 rows, not 1.** The first count came from scanning the rendered
  pin arrays, which hold only the within-ring layer; two more sat in the
  all-city toggle set. New York went from 44,361 to 44,360 within-ring pins and
  62,444 to 62,441 available. Every other city dropped nothing, so the
  shared-code placement cost five cities a re-render and changed none of them.
- **Decided: keep New York's 161 surname-first names.** They are DCWP licence
  holders - Newsstand 92, Tobacco Retail Dealer 35, Secondhand Dealer 16 -
  trading at licensed commercial premises where the registry holds no separate
  trade name, which is the situation San Diego's 903 sole proprietorships were
  kept for. Removing them would delete real licensed businesses from an
  already-thin Retail category. Recorded rather than actioned.
- **Extended `scripts/check_personal_exposure.py` to screen four things it
  could not see before**, at the project owner's instruction: contact details
  (email, phone), surname-first names, a person's name followed by a trade name
  in brackets, and `ATTN:`/`c/o` markers naming a person. Each is reported as
  its own line rather than folded into the existing person-name percentage, so
  the figures quoted in earlier entries stay comparable.
- **The first version of the `c/o` pattern was wrong, and measuring caught
  it.** `\bC[/.]?O\b` makes the separator optional, so it matched the bare
  abbreviation "CO" and flagged 567 company names across five cities
  ("ROMANIAN KOSHER SAUSAGE CO", "GRAMERCY TYPEWRITER CO"). Requiring the
  separator took it to 6 genuine hits. A privacy check that cries wolf 567
  times is worse than none, because the real hit is unfindable in the noise.

### 2026-09-21 - Philadelphia built: two buckets, one registry, two station rules

- **Built Philadelphia as the sixth city, and the first with only two of the
  three buckets.** One registry (L&I Business Licenses via the Carto SQL API),
  94 in-city SEPTA Metro stations across 4 drawn lines, 8,512 mapped sites -
  Food service 7,485 and Retail 1,715 - from 9,200 downloaded rows. Rendered
  map 1.19 MB.
- **Personal services is absent, and no source exists to add.** Philadelphia
  licenses no salon, barber, nail, cosmetology, massage or laundry business:
  an `ILIKE` sweep across both Carto licence tables returns nothing.
  Pennsylvania publishes professional licensees only as county aggregates
  (`fwj2-whnj`, no addresses) and its PALS system answers one licence at a time
  with no bulk export. **Decided: build the city and state the gap** on its
  page and in `docs/excluded_categories.md` under what is *missing* rather than
  *excluded*, because everything else on that page was a choice and this was
  not. The alternative considered and rejected was skipping the city to keep
  every built city at three buckets.
- **The multi-source approach was attempted and failed, which is the finding.**
  All four candidates were checked live and each is recorded in
  `docs/data_sources.md` so the search is not repeated: PA Agriculture's food
  inspections relay the city's own data (`organization_name` is "City of
  Philadelphia"); the Commercial Activity License file - the general licence
  every city business needs - has **0 of 528,413 active rows with geometry**,
  no business address, and `licensetype` fixed at the single value "Activity";
  `li_business_licenses` is a stale copy of the registry used (360,192 rows vs
  435,143). So the `multi-source-city` skill's conclusion for this city was
  "there is no second source", which is a valid answer to its Step 1.
- **Two licence types were misread from their names, and sampling caught both.**
  `Vendor - Motor Vehicle Sales` is not car dealers - it licenses vending
  *from* a vehicle, and its holders are food trucks ("CHA CHA LUNCH TRUCK",
  "FOOD TRUCK COLLECTIVE LLC"), so it is excluded as mobile rather than counted
  as Retail. Conversely `Food Establishment, Retail Perm Location (Large)` is
  not supermarkets only but the general-retail tier - Target, CVS, Dollar Tree,
  Staples, Ross Dress For Less - which hold a food licence because they sell
  packaged food, and are the only way this city's data sees a chain clothing or
  office-supply store at all. All 50 active types now carry an explicit verdict
  in `pipeline/taxonomies/phl_licensetype.py`.
- **Excluded `Rental`, 79% of the file, as a scope error first.** 93,471
  residential landlord registrations, on which the registry's business-name
  field holds the owner's own name at their property with
  `legalentitytype='Individual'`. Mapping active licences unfiltered would have
  published ~94,000 individuals at their homes. Framed as scope (not
  businesses, not storefronts) because that is the easier call to justify and
  it fixes the privacy problem as a consequence - the same shape as the
  project-wide NAICS 454 exclusion. `Limited Lodging Operator` (589) went with
  it.
- **Corrected a Step 0 measurement error: coverage is 97.6%, not 100%.** The
  probe counted `the_geom IS NOT NULL` and got every row, but 218 rows hold an
  *empty* point geometry, on which `ST_X`/`ST_Y` return NULL. **Decided: drop
  them without a geocoding step.** The loss is not uniform - it takes 61 of the
  75 newsstands - but geocoding cannot fix that bias, because 60 of those 61
  carry no street address either; the 79 rows that are recoverable are 0.86% of
  the file, which does not justify a geocoder, a cache and a step renumber.
  Step 2 prints the drop by licence type so the bias is visible in every run
  rather than only in this entry.
- **Line scope: L, B, T and G; Regional Rail excluded.** M1 (Norristown High
  Speed Line) and D1/D2 (routes 101/102) needed no decision - both begin at
  69th Street in Upper Darby and have **zero** in-city stops. Regional Rail has
  52 well-spaced in-city stations (857 m median) and was still excluded, to
  match Chicago leaving out Metra and New York leaving out the LIRR and
  Metro-North; SEPTA's own branding separates it from SEPTA Metro. It is the
  obvious later addition, and needs no thinning if that call changes. The
  rejected alternative was L + B alone (47 stations), which would have drawn
  only two lines and left West Philadelphia and Girard Avenue blank.
- **First city needing two station rules at once.** L and B are grade-separated
  at 711 m and 681 m median spacing, so every in-city station is kept, as in
  San Diego. T (five trolley branches) and G (Girard) are street-running at
  134-137 m median with a 10th percentile of 17-19 m - San Francisco's shape -
  so they take the four-filter thinning in `docs/sub_transit_line_filters.md`.
  Result: 261 trolley stops to 90, T1-T5 keeping 13/14/15/16/17 of 38/29/39/46/42
  and G 15 of 57. All 167 cut or out-of-city stops are documented in
  `outputs/philadelphia/excluded_stations.csv`.
- **Generalised filter 4 from routes to line groups, which changed the
  result.** San Francisco's version force-keeps any stop shared by 2+ routes as
  a transfer point; there, every route was its own line, so the two readings
  were identical. In Philadelphia all five T branches share the Center City
  tunnel and T4/T5 additionally share the whole Woodland Avenue segment, so the
  route-level reading force-kept five consecutive stops inside 400 m and
  quietly defeated the thinning. Group-level interchange (2+ of L/B/T/G) gives
  6 real transfer points and drops T4/T5 from 20/21 kept to 16/17.
- **The near-duplicate distance check earned its place.** It flagged
  `Girard Av & Front St` 6.7 m from `Front-Girard` and `Girard Av & Broad St`
  18.4 m from `Broad-Girard` - a trolley stop sitting on top of the
  rapid-transit station it interchanges with, under names sharing no detectable
  suffix pattern. Both are now hand-curated aliases, exactly the residue
  `docs/sub_transit_line_filters.md` predicted would be left after the regex
  pass.
- **Deduplicated on address AND name, adjunct licences ranked last.** One
  storefront can hold several licences, so there is one row per normalised
  address + business name with the most specific licence deciding: 8,982 rows
  to 8,512 sites. Of 317 adjunct rows (sidewalk cafe, streetery, outdoor
  seating), 243 collapsed into the restaurant that also holds a primary licence
  and 74 survive as the only licence at their site. All 8,512 fall inside the
  city polygon.
- **Display the trading name, not the licence holder.** This registry formats
  `business_name` as "LEGAL NAME (TRADE NAME)", so where the legal entity is an
  individual the raw field publishes their own name in full: "BRIAN WANG (FOUR
  SEASON JUICE BAR #89)", "Andrew Polhemus (Molto Bene Ravioli Co)", and
  "CVS PHARMACY INC (ATTN: JOANNE P. AMITRANO)" naming a corporate employee.
  Step 2 now chooses the displayed name instead of copying it: prefer a
  bracketed name that is neither a contact nor a person, else the text outside
  the brackets, else the registered name as it stands. Rewrote 2,900 of 8,512
  rows, **456 of which removed a licence holder's own name from a pin.** It is
  also the better label - "AZAAN GROCERY STORE" beats "A AND A II INC" - which
  is why the bracket is preferred rather than merely stripped.
  - **A bare personal name with no alternative is still published** ("Amanda
    Girard"): that is the trade name the owner registered, a deliberate public
    commercial act, per the San Diego reasoning in `naics.py`.
  - **The person-shape regex alone was not enough**, and getting it wrong was
    instructive: "STARBUCKS CORPORATION" is two alphabetic words, so without an
    organisation-token guard the rule classed it a person and preferred the
    bracket. That inflated the rewrite rate before the guard was added.
- **Privacy verdict: publish.** `scripts/check_personal_exposure.py` (with
  Philadelphia added, and extended to read a structured entity-type column):
  4,958 pins, no registrant-name fallback *possible* - six name-bearing columns
  are never downloaded and step 2 asserts their absence, and `business_name` is
  never blank in this registry. 296 pins (6.0%) read as a person's name and
  **all sit in food-service categories**, i.e. premises that must be inspected,
  with no catch-all sweeping in home-based sole traders. 1,270 of 8,512 rows
  are `legalentitytype='Individual'` (14.9%), 190 pins are both Individual and
  person-like (3.83%), and **0.00% sit at a residential unit indicator**.
- **That person-like count went UP after the rename, from 207 to 296, and the
  increase is honest rather than a regression.** A composite string like
  "Brian Wang (…)" always displayed a person's name; the bracket simply
  defeated the heuristic, which rejects any string containing punctuation.
  Removing the bracket let the check see what was already on the map. The
  measured exposure rose because the measurement improved, and the structural
  facts did not move: no residential units, no registrant fallback, all
  inspected premises.
- **One blind spot named rather than closed:** the residence test only fires on
  an `APT`/`FL`/`RM`/`#` indicator, so a sole trader at a *detached house* reads
  as clean - which is part of why this city scores 0.00%. Two unused signals
  could close it, both available here: `business_mailing_address` matching the
  premises address (not currently downloaded), and parcel land-use via
  `opa_account_num`. Logged as future work, not claimed as done.
- **Wired `legalentitytype` into the exposure check as a general mechanism.**
  Philadelphia is the first city whose registry records entity type
  structurally, so for it the name heuristic is the cross-check and the
  publisher's own field is the measure - the reverse of every city before it.
  Added as `entity_type`/`entity_individual` keys in `REGISTRIES` so a later
  city with the same signal needs no new code.
- **Two licence questions raised and left open**, per the `multi-source-city`
  skill's instruction not to read a clause generously: SEPTA's bar on using its
  "trademarks and copyrighted materials for any commercial or profit-making
  use" (the map uses its real line names and official `route_color` values, and
  no logo or route-bullet artwork), and the "City of Philadelphia License",
  which reserves all database rights, grants nothing explicitly, forbids
  nothing explicitly and requires no notice. Neither blocks the build; both
  should be settled before the public deploy. Philadelphia added **no new
  mandatory notice**, so that count stays at four.

### 2026-09-21 - Probe output belongs in the scratchpad, not the home directory

- **Deleted eight Step 0 research captures from the home directory**, left
  there by the 2026-09-18 city screening: `la.json`, `la_sample.json`,
  `phila_sample.json` (raw WKB hex for geometry that turned out not to need
  parsing), `phila_tables.json` (41 bytes of
  `{"error":["system tables are forbidden"]}`), `phila_search.json` (HTML under
  a `.json` name), and three saved OpenDataPhilly pages including a 404 and a
  283 KB dataset listing.
- **Decided not to integrate them into the repo.** They are raw API and HTML
  captures - the category this project already gitignores as
  `data/<city>/raw/` - and every finding in them is superseded and now recorded
  properly in `docs/data_sources.md` and `docs/city_shortlist.md`. Committing a
  saved 404 and a misnamed file to a public repository would be worse than
  having nothing.
- **Added the rule that prevents a repeat** to `CLAUDE.md`'s working rules and
  the `add-city` skill's Step 0: every probe gets an explicit output path under
  the session scratchpad or a gitignored raw folder, because `curl -o la.json`
  writes wherever the shell happens to be. Two unrelated personal files in the
  same directory were identified, left untouched, and deliberately not read.

### 2026-09-21 - Overview colour sweep: one real fix, two non-defects

- **Swept the last hardcoded colours in `app/`.** All seven literals in
  `Overview_&_Introduction.py` now derive from `pipeline/theme.py` via a new
  `rgb_list()` helper (pydeck takes channel lists, not CSS), so the macro map
  cannot drift from the rest of the chrome. The only literal deliberately left
  outside the palette is the amber hover highlight, which exists to differ from
  both the teal marker and the category colours.
- **One real inconsistency fixed: the macro map's tooltip.** It was baked at
  `#1c2b2a` on white - the light theme's *text* colour used as a background -
  so in dark mode it stayed green-grey while every city map's tooltip was
  slate. It is the one macro-map element CSS can reach, because deck.gl renders
  it as an HTML overlay (`.deck-tooltip`) rather than in WebGL, so
  `app/components.py` now overrides it under `body.dark-base`. Verified it
  beats pydeck's inline styles: measured `#131C2E` / `#E6EDF7` / `#23304A`
  against a synthetic tooltip carrying the inline values.
- **The constraint that shapes the whole macro map, now written down.** Marker
  and label layers are WebGL, so CSS cannot restyle them, and one colour set
  must serve both basemaps. The light basemap's land is `#f2efe9` and the
  inverted dark one `#191c22` - opposite ends of the luminance range - so **no
  single colour can clear 3:1 against both.** That is why each city name gets
  an opaque pill: the pill supplies its own background, and the text only needs
  contrast against the pill (14.7:1). It is a design answer to a hard limit,
  not a stylistic choice, and it should not be "simplified" away.
- **Two flagged failures were my measurement criterion being wrong, and are
  recorded so a later pass does not chase them.** The pill reads 1.15 against
  the light basemap, but a text background does not need to contrast with what
  is behind it - its text does. The marker's white ring is likewise decorative
  on the light basemap and load-bearing on the dark one, with the marker
  discernible either way through its fill. Checking contrast numerically was
  right; applying a text criterion to a background was not.
- **One accepted weakness, stated rather than hidden:** the amber hover
  highlight is 1.45 against the light basemap. Unfixable within a single colour
  set for the reason above, and hover also enlarges the marker and opens a
  tooltip, with amber differing from teal by hue rather than luminance - which
  a WCAG ratio does not capture.
- **What to re-check if the palette ever changes:** the teal marker fill is the
  only element that clears 3:1 on both basemaps (3.26 light, 4.56 dark), and
  its margin on the light side is thin. A darker or lighter teal breaks one end.

### 2026-09-21 - Maps follow the page's theme; an explicit click still wins

- **Closes the two-controls gap** opened by giving the page a theme. Chosen
  from three options (recorded in the previous entry's `PLAN.md` note):
  **maps default to the ambient theme, a manual click wins from then on.**
  - Rejected **(B)**, letting our button drive the page and styling Streamlit's
    chrome from `body.dark-base`: it means overriding framework widget colours
    by hand, which is exactly the cost the handoff measured as the real work,
    and it would have meant throwing away the theme chooser we had just
    recovered.
  - Rejected **(C)**, removing the in-map button when embedded: conceptually
    the cleanest - one control per context - but it discards the in-map toggle
    the `#map-actions` group is built around, and standalone maps would still
    need their own, so the mechanism was needed either way.
- **Detection reads the host page's background brightness, not a framework
  API, because there is no API.** Streamlit exposes no theme signal: no
  `data-theme` on `<html>` or `<body>`, no CSS custom property. The page
  background does reflect whichever of System / Light / Dark the visitor chose,
  and a map iframe is same-origin with its host, so one luminance read covers
  all three. `prefers-color-scheme` alone was rejected as the primary signal -
  it only matches the default System case and is wrong the moment someone picks
  Light or Dark explicitly - but it is the fallback for a standalone map, which
  has no host to read.
- **The rule lives once**, as `AMBIENT_THEME_JS` in `pipeline/theme.py`, used
  by both the city maps and the macro map, consistent with that module already
  being the single source for colours.
- **Verified all three behaviours**, not just the happy path: with no stored
  choice on a dark page the embedded map opens dark and its body background
  matches the page exactly (`#0B1220`, `storedTheme: null`); a click stores
  `light` and flips the map; and after a reload on a still-dark page the map
  stays light. The macro map behaves the same way from its 1px script frame.
- **A debugging lesson worth more than the feature.** The first test showed the
  code apparently not working - maps stayed light on a dark page. The code was
  correct; **Streamlit was serving a cached `components.py`**, and the live
  iframe's `srcdoc` did not contain the new function at all. Editing an
  imported module and reloading the page is not enough: stop the server, clear
  `__pycache__`, restart. The `deploy-verify` agent's procedure already says
  this, which is why it clears caches at step 1 - the instruction existed and
  was not followed. Now also in `docs/theming.md`, with the two-second check
  that would have caught it immediately: assert the injected script is present
  in the rendered `srcdoc` before debugging its behaviour.

### 2026-09-21 - Midnight slate: page themed, palette unified, one gap left

- **The page theme is in, and Streamlit's theme chooser is back.** Verified
  empirically rather than assumed, because the handoff's warning was written
  about another project: with the previous bare `[theme]` block the main menu
  offered only Rerun / Auto rerun / Clear cache / Print / Record screen - **no
  Settings item at all**, so the old comment in `config.toml` claiming visitors
  could switch via the hamburger menu was **already false before this change**,
  not made false by it. Defining `[theme.light]` and `[theme.dark]` restored a
  System / Light / Dark chooser, and the page now renders `#0B1220`.
- **The palette had a second, undocumented home.** `app/components.py` carried
  its own literal copies of `#182322`, `#e6efee`, `#2e403e`, `#1f2d2c`,
  `#8fa3a1`, `#5eead4` and `rgba(15,23,22,0.8)` for the macro map's chrome,
  mirroring `map_common.py` with no shared source - so a reskin of one would
  have produced a navy city map beside a teal macro map. Found by grepping for
  hardcoded colour before editing, which is what the handoff said the real work
  would be.
- **`pipeline/theme.py` is now the single source** for every chrome colour,
  light and dark. It imports nothing, so `app/` can read it under the lean
  deploy venv, the same rule the city pages' config imports already follow.
  Both the map CSS and the macro-map CSS build from it, with an assertion that
  no placeholder is left unresolved. Business-category and transit-line colours
  are deliberately NOT in it: those are data, not chrome.
- **Two selector traps made structurally impossible.** The dark rules match on
  `[stroke="#2c3e50"]` (rings) and `[stroke="#1a5490"]` (stations), which only
  works because each colour is used nowhere else - and `docs/theming.md`
  records that changing either light value silently breaks its dark rule. The
  selector and the drawing code now read the same `LIGHT` entry, so they cannot
  drift. The dark label halo and attribution strip also stopped re-typing the
  page colour as literal channel values (`rgba(15,23,22,0.8)`); they derive it.
- **`scripts/check_theme_sync.py`** exists because TOML cannot import, making
  `.streamlit/config.toml` the one unavoidable duplicate. It compares both
  variants against `pipeline/theme.py` and fails on a mismatch, a missing
  variant, or a colour set on the bare `[theme]` table where it would silently
  apply to both. Currently: 10 values in sync.
- **The gap, stated plainly: there are now two independent theme controls on
  one page.** Streamlit's chooser drives the page; our own button drives the
  maps. Measured immediately after the change: page background `#0B1220`
  (dark), `body.dark-base` absent (maps light), and a white map button on a
  dark page. Nothing is broken - no error blocks - but it is visibly
  incoherent, and it is a direct consequence of giving the page a theme at all.
  Options and a recommendation are in `PLAN.md`; not resolved unilaterally
  because it changes visitor-facing behaviour.
- Useful finding for whichever option is chosen: **Streamlit exposes no theme
  signal** - no `data-theme` attribute on `<html>` or `<body>`, no CSS custom
  property. But the page background reflects whichever of System / Light / Dark
  the visitor picked, and the map iframes are same-origin, so a luminance read
  of the parent's background detects all three. `prefers-color-scheme` alone
  would only match the default System case.

### 2026-09-21 - Two theme handoffs merged into docs/theming.md

- **Decision: one theming document, not two.** `dark_mode_handoff.md` and
  `midnight_slate_theme_handoff.md` described the same surface from different
  moments and disagreed in places - the older one still specified a
  base-layer-radio toggle that was never built, while the newer one referenced
  its `--dm-*` table as if it were current. That is the same
  two-sources-of-truth failure that left San Francisco's boundary endpoint
  recorded nowhere: harmless until someone needs it, then actively misleading.
- **`docs/theming.md` is now the single reference**, ordered by usefulness
  rather than chronology: current implemented state, the decided palette,
  what is not yet built, the traps, the verification checklist, and
  superseded designs last and explicitly labelled "provenance only, do not
  implement".
- **The superseded design is summarised, not deleted, and its code is not
  reproduced.** The base-layer approach and *why the fixed button beat it* are
  worth keeping - the map is 1000px wide while Streamlit's column is often
  narrower, so a control anchored to Leaflet's top-right corner can sit
  off-screen, which is the same root cause as the legend and phone-width work.
  The code itself lives in git history rather than in a file that reads like
  instructions.
- **What the merge preserved from the older document**, because it was still
  true and would have been lost: `dark-base` belongs on `<body>` not the map
  container (the legend is outside it); the legend's light styling is inline so
  dark rules need `!important`; ring outlines are the only `#2c3e50` and
  station dots the only `#1a5490`, which is what makes the attribute selectors
  work and means changing either light colour silently breaks its dark rule;
  and the script-ordering trap - Folium renders body HTML before the figure's
  script block, so a script added there runs before the map object exists. That
  last one is the same class of bug as this session's `toggle`-event defect and
  is why `PHONE_FIT_SCRIPT` polls.
- **Both originals were committed before being merged** (`d4c3095`), so the
  received form of the midnight-slate handoff is in history exactly as handed
  over, including the two corrections made on receipt.
- **Also confirmed:** the three post-`map-chrome` fixes are verified by
  screenshot on four cities but not by an agent pass. Rather than spend another
  scoped run, they fold into the mandatory `full` run before deploy - which is
  the batching the scope policy was written to encourage.

### 2026-09-21 - Staying on Streamlit, and theming it as one palette

- **Decision: keep Streamlit.** The question was raised because a theme
  implementation was wanted and Streamlit looked like the obstacle - the
  page-level dark mode has been deferred in `PLAN.md` precisely because of it.
  Three things settled it:
  - The handoff's item 1, which it marks as *tested rather than assumed*:
    separate `[theme.light]` and `[theme.dark]` blocks keep Streamlit's own
    toggle. So an explicit theme does NOT force the site dark-only, which was
    the assumed penalty.
  - The biggest trap the handoff names - "a light Folium map on a slate page is
    a white box" - is already solved here. The maps carry their own theme and
    share one `localStorage` key.
  - Three of its seven implementation notes are already closed in this project
    (the `st.components.v1.html` migration, the `streamlit>=1.64,<2` bound, and
    the map-iframe problem above).
- **Rejected for now: replacing Streamlit with a static site.** Measured
  coupling is small - `app/` is 693 lines including comments, the API surface
  is `st.iframe`/`markdown`/`title`/`page_link`/`switch_page`/`pydeck_chart`,
  and the pipeline imports Streamlit zero times. The maps are pre-rendered
  standalone HTML and were tested all session on a plain `http.server` with no
  Streamlit running. So the rewrite is feasible and its only real work is the
  pydeck macro map. It was rejected because **it is not required for the
  theme**, and because the dependency runs one way only - the app reads
  `outputs/`, `outputs/` depends on nothing - so going static later costs
  exactly what going static now costs. No lock-in was accepted by deciding
  this way.
- **The evidence that redirected the work.** Rendering the candidate palette on
  New York and comparing it against the current one from an identical view
  showed the difference is confined to the legend, buttons, controls and the
  background strip. The map body is essentially unchanged, for structural
  reasons: the dark basemap comes from a CSS filter
  (`invert(1) hue-rotate(180deg)`) that no `--dm-*` variable touches, and the
  pin and line colours are fixed category values deliberately outside the
  theme. The eleven variables drive roughly 15% of a city page's pixels.
  **So a map-chrome reskin on its own is not worth doing**, and the payoff is
  page-level - which is the tier that needs Streamlit.
- **Therefore: one palette, landed together.** `.streamlit/config.toml` with
  both light and dark blocks, and the map's `--dm-*` values swapped to the
  matching slate values in the same change. An earlier framing offered "map
  palette now, or wait for the page" as a choice; that was wrong. The handoff
  supplies both sets from a single palette, `#0B1220` page against `#131C2E`
  surface is a designed relationship, and the map surface can only be judged
  against the page behind it. Page first, so there is something to match.
- **Two deviations from the handoff, both measured rather than preferred:**
  - **Keep our teal accent `#5eead4`** (12.7:1 on the new page) rather than its
    `#4C9AFF`, which the file itself calls a placeholder that "reads as another
    project's look".
  - **Do not use `#4A5A78` for `--dm-disabled-text`** - it measures 2.7:1 on
    page and 2.5:1 on surface, below the 3:1 non-text floor. It is one of the
    four values the file marked "(suggested)" rather than designed, so its own
    caveat flagged the right one. The preview used `#5A6B8C`.
  - Every contrast figure the handoff states was recomputed and matched to the
    stated decimal, which is why its untested palette was trusted this far.
- **Still to decide when this is built:** whether to follow the visitor's
  system theme (`prefers-color-scheme`) with a manual override winning once
  used, which the handoff reports as implemented and verified elsewhere. This
  project is manual-only today. Its trap comes free with it: devtools
  colour-scheme emulation updates `matchMedia().matches` without dispatching
  `change` inside an iframe, so it cannot be tested that way.

### 2026-09-21 - Three fixes from a scoped verify, and a measurement lesson

- **The legend breakpoint was broken on a wide load - my bug, found by the
  first scoped `map-chrome` run.** Chrome queues a `toggle` event for a
  `<details open>` element that lands *after* an inline script attaches its
  listener. On a narrow load `fit()` had already set the guard flag, so the
  stray event was consumed; on a wide load `fit()` returned early without
  setting it, the stray event hit the "user touched it" branch, and the
  breakpoint was dead for the life of the page. A reader who loaded wide and
  then narrowed still got four of New York's labels covered - the original
  defect, reachable by a different route.
  **Fix:** detect reader ownership from a `click` on the `<summary>`, not from
  `toggle`. `toggle` fires for programmatic changes too, which was the whole
  ambiguity; a click is unambiguous and keyboard activation dispatches one.
  Verified: load at 1200 (legend open, 403px) -> narrow to 854 -> collapsed to
  37px, zero labels under it.
- **The container landed ~15px short of the frame.** At load the 1000px map
  forces a horizontal scrollbar, which costs enough height to force a vertical
  one, so `clientWidth` reads short - and nothing dispatches a resize event
  afterwards to correct it once the scrollbars go away. Fixed by applying the
  fit more than once (rAF plus 120/400/1200ms); `apply()` returns immediately
  when the width already matches, so the extra passes cost nothing. Container
  now reaches the full frame width on every city.
- **Line labels were cropped off narrow frames because the fit used STATION
  bounds.** A label sits beyond its line's tip, outside those bounds.
  `_choose_view` already fits the desktop view to stations *and* labels
  together; the phone fit now does the same, with padding raised to [26, 18]
  because the emitted bounds hold label anchors and a label's text box extends
  past its anchor.
- **The measurement lesson, which is the most reusable part.**
  `getBoundingClientRect()` on a line label is unreliable in the browser pane
  and produces convincing false failures: a marker element reported a rect at
  x=490 while its own `style.transform` said 212px, with the map pane at
  identity and no page scaling. The scoped run reported "three of San
  Francisco's six labels entirely off screen" and "two of Los Angeles' six" on
  that basis; screenshots of the same frames show **every** label on every
  city rendered and legible, a few clipped at an edge. The rects were stale
  because the pane was not compositing.
  So: screenshots are the authority for label geometry, rect-derived counts are
  a hint, and properties (`details.open`, computed colour, `style.width`,
  cluster leaf counts) are reliable where a check can be expressed that way.
  Written into the `deploy-verify` agent, because it is the opposite of that
  file's usual DOM-over-screenshots advice and would otherwise keep generating
  false findings. It also means the earlier "1 of 11 visible" reading that
  nearly went into a report was the same artifact twice over.

### 2026-09-21 - Phone-width maps fixed by resizing after init, not before

- **The problem `deploy-verify` found:** at 375px the iframe showed a ~343px
  slice of a 1000px map, so the reader had to scroll inside the iframe to find
  anything. 1 of New York's 11 line labels was visible, 0 of Chicago's 7.
- **The fixed 1000px width could not simply be dropped** - it is what avoids
  Leaflet.heat's uncaught `IndexSizeError` on init with an unresolved container
  size, which silently kills every layer added afterwards. The insight is that
  the bug is about an *unresolved* size at construction, not a *small* one: the
  container can keep its fixed size through initialisation and be resized
  immediately afterwards via Leaflet's own `invalidateSize()`, then re-fitted to
  the station bounds. Prototyped in the browser on a rendered map before writing
  any code, which is how the approach was confirmed rather than assumed.
- **Result at 375px:** New York 1 -> **9 of 11 labels fully visible, 0
  off-screen**; Chicago 0 -> 6 of 7; horizontal scroll inside the iframe gone;
  heat layer intact. Desktop unchanged - at 1200px the container is still
  1000px, the view is the original, and all 11 labels show. The station bounds
  come from Python rather than the script sniffing marker colours.
- **What it does not fix, stated rather than glossed:** `_layout_labels` picks
  label positions server-side against a 1000x650 canvas, so at phone width
  labels can crowd each other and the cluster badges, and one or two clip at an
  edge. Correct phone layout needs a second render at phone dimensions, which
  would roughly double `outputs/` and render time - logged in `PLAN.md`, not
  started, and worth doing only if phone traffic matters.
- A measurement note, since it nearly produced a wrong report: label counts
  taken in the same batch as the page load read 1 of 11, because the fit script
  polls and had not settled. The settled figure is 9. Measure after the state
  settles, not in the same round trip.

### 2026-09-21 - Licence checking is now part of adding a city

- **The review was retrospective; this makes it routine.** Recording endpoints
  was already an `add-city` Step 0 requirement, but recording *licences* was
  not, so the next city would have repeated the same gap the 2026-09-21 review
  had to close for five cities at once.
- Step 0 gained a fourth item covering, per source: the declared licence (and
  where Socrata exposes it), the governing terms when none is declared, the
  transit feed's terms *separately* (they were the loosest end of the review,
  and `feed_info.txt` almost never carries a licence), anything the project
  must display, and anything needing a human decision. Step 9 re-checks that
  the rows actually landed.
- Two traps from the review are written into the skill so they are not
  repeated: a missing Socrata `license` field does not mean permissive, and a
  parent site's general footer is not the data's terms - reading nyc.gov's
  "All Rights Reserved" as governing NYC Open Data produced exactly the wrong
  conclusion, when Local Law 11 in fact forbids the city from imposing a
  licence at all.
- The standing removal-request commitment covers new cities automatically, and
  the skill says not to weaken it for a source with tighter terms: the answer
  to tight terms is to record and comply, not to hedge the commitment.

### 2026-09-21 - A standing commitment to honour removal requests

- **Checked whether the agencies showcase third-party work, and they do not.**
  The idea was to find positive precedent for how publishers interpret their
  own terms - stronger evidence than the absence of takedowns, which proves
  nothing because every licence here enforces by private written notice and
  small projects do not publicise receiving one. It was close to a dead end:
  the MTA's apps page lists only its own two apps, LA Metro's developer site
  shows only its own experimental tools, and CTA has no gallery. What the
  search did yield is each agency's own framing of intent - Metro "invite[s]
  you to use this information to help us improve *your* system"; CTA's
  Developer Center launch describes enabling third parties to build
  applications "designed to improve travel". Supportive context, not evidence,
  and recorded as such.
- **The useful conclusion was about the shape of the risk, not the precedent.**
  Every licence reviewed contemplates the same remedy: a request to stop
  displaying the data. Not damages - removal. That bounds the realistic
  downside of this project to an email asking for a layer to come down.
- **So the protection is a commitment rather than a search for reassurance.**
  Published in `docs/data_sources.md` and, in the form that speaks to business
  owners, in `docs/excluded_categories.md`: a removal request from a
  publisher, a business owner, or anyone raising a privacy concern about a
  specific pin is honoured without argument and without the requester having
  to give a reason; the pin, layer or city comes down first and the reasoning
  is recorded afterwards. Explicitly including the case where the project
  believes it is in the right - "being permitted to display something is not a
  reason to insist on displaying it" - because that is the case where a
  commitment made in advance actually does work. Also a `CLAUDE.md` invariant,
  so it binds future sessions rather than living only in published prose.

### 2026-09-21 - Licence review closed: every source established but one

- **Source-by-source review of all 19 inputs** (8 business registries, 5 GTFS
  feeds, 5 boundary layers, the geocoder) recorded in
  `docs/data_sources.md`. The working assumption going in - that a government
  open-data portal implies permissive terms - did not survive: terms ranged
  from public-domain dedications to a feed that forbids modifying its data,
  and the two extremes are the *same city* (Los Angeles' business registry is
  CC0; its GTFS is the tightest licence in the project).
- **New York City: the absent licence is required by law, not an oversight.**
  Its three datasets declare no licence, and the only terms link on the portal
  points at the general nyc.gov footer, which reserves all rights - so the
  first reading was that no reuse grant existed. The primary source settles it
  the other way: NYC's Open Data Technical Standards Manual states that Local
  Law 11 of 2012 "requires that data sets must be available without
  registration requirement, license requirement, or usage restrictions". The
  city cannot attach a licence. The nyc.gov "All Rights Reserved" notice
  covers that website's own content, not datasets published under the Open
  Data Law. One condition does attach: DoITT "may require third party entities
  such as application developers to explicitly identify the source, version,
  and modifications made to a public data set" when republishing - which this
  project already produces (`data_sources.md` for source and version,
  `excluded_categories.md` for modifications).
- **Two clauses were judgment calls, decided by the project owner** after
  being raised rather than read generously:
  - **LA Metro forbids modifying the "Transport Information".** Decided: this
    project does not modify it. The alignment is drawn from the feed's own
    `shapes.txt` and displayed as that line; nothing is altered, augmented or
    misrepresented, and the clause reads as protecting against passing off
    changed route or schedule data as Metro's. Revisit if Metro clarifies.
  - **CTA licenses its data to "assist mass transit riders or promote public
    transportation".** Decided: the project falls within that purpose - it
    shows people what businesses are near their station, which is
    rider-facing information about using the system. It is also not sold, not
    advertising, and claims no affiliation, which are the clauses the purpose
    limitation sits beside.
- **The operative finding is four notices the site must display**, now listed
  with exact wording in `docs/data_sources.md`. OpenStreetMap's is already
  satisfied by the maps' tile attribution; Chicago's verbatim disclaimer,
  SFMTA's permission notice and an acknowledgement of LA Metro as provider are
  not yet shown. Keeping the OSM attribution is now a `CLAUDE.md` invariant,
  including the point that changing tile provider swaps that attribution
  rather than removing it.
- **Only the Census geocoder's terms remain unread**, and it is used only to
  derive coordinates into this project's own outputs.
- **What this changes about the deploy:** the remaining licence work is no
  longer a permission question but an implementation one - display four
  notices - which is why it was folded into the same deferred app job as
  surfacing `excluded_categories.md` and `data_sources.md`.

### 2026-09-21 - The legend collapses itself when the frame is too narrow for the map

- **Found by the `deploy-verify` agent**, not by looking at a map at desktop
  width. Below roughly a 1130 px browser window the legend slid over the map
  and covered line labels: at a 1024 px window the app's column gives the
  iframe 854 px, and at that width four of New York's eleven labels were
  hidden (Flushing, Shuttles, Nassau St, 14 St-Canarsie).
- **The cause is the interaction of two earlier decisions, each still right.**
  The map lays out at a fixed 1000 px because Leaflet.heat throws an uncaught
  `IndexSizeError` when its container size is unresolved
  (github.com/Leaflet/Leaflet.heat/issues/95), which silently kills every
  later layer. The overlay controls are `position: fixed` so they stay visible
  while the map scrolls inside its iframe. But "fixed" anchors to the frame's
  *visible* width, whereas `_layout_labels` reserves the legend's obstacle at
  the bottom-right of the full 1000 px. Narrow the frame and the legend moves
  off the space reserved for it and onto space given to labels.
- **Fix: collapse the legend exactly when the frame is narrower than the map**
  (`LEGEND_AUTOFIT_SCRIPT`, threshold read from `_MAP_W` so there is one
  source of truth). Collapsed it is a 76x37 px "Legend" tab that covers
  nothing and is one click from open. Chosen over the alternatives: making the
  legend `position: absolute` would put it back in its reserved corner but
  require scrolling right to see it at all on a narrow frame; widening the
  label obstacle to cover every possible legend position would permanently
  spend space that is only contested sometimes.
- **A reader who opens or closes the legend owns it from then on** - the
  breakpoint stops adjusting it, so it never fights a deliberate click.
- **Verified at three widths, on two cities, and for the manual override.**
  At an 839 px frame: New York's legend auto-collapses to 37 px and covers
  **0** labels (was 4), Chicago's likewise with its 7 labels. At 1200 px it is
  open at its full 403 px and covers 0. After a hand-close at a wide width it
  stays closed across a resize event. Label positions are untouched - the
  Python-side obstacle maths did not change - so this is a script-only change
  to the rendered HTML.
- Still open, and NOT addressed here: at phone width the frame shows ~343 px of
  the 1000 px map, so most labels start outside the visible area and the reader
  must scroll inside the iframe. That is the same fixed-width cause but needs a
  deliberate mobile approach, not a breakpoint (`PLAN.md`).
- Also noted while in this code, not changed: the label layout treats only the
  legend and the top-LEFT zoom/layer controls as obstacles. The top-RIGHT
  button group (Cities / All cities / theme) is not an obstacle, so a label
  could in principle land under it; no rendered map currently shows this, and
  adding it would move labels in all five cities.

### 2026-09-21 - Staten Island Railway drawn in a lighter blue than the MTA's own

- **The one line on any city map not using its agency's official colour.**
  Every other New York trunk uses the MTA's `route_color` from the feed, which
  is the project's rule because those colours are unambiguous and what riders
  recognise. SIR's is `#08179C`, a navy at roughly L* 17. Because a line's
  permanent on-map label takes the line's own colour, that made the "Staten
  Island Railway" label hard to read on the light basemap and nearly invisible
  in dark mode, where the basemap inverts and the label does not.
- **Changed to `#4358D4`**, lightened within the same navy family so it still
  reads as SIR rather than becoming a different line. Kept violet enough to
  separate from 8 Av's azure `#0062CF` in the legend, where the two sit near
  each other; on the map itself they never appear together, Staten Island being
  a physically separate system. Checked rendered in both themes before
  committing.
- Alternatives considered and rejected: giving the label its own colour
  independent of the line (keeps MTA's navy authentic, but adds a second
  colour concept to `map_common.py` for one line), and moving SIR to a
  distinct hue such as teal (too close to the Personal services bucket's
  `#1baf7a`).

### 2026-09-21 - Map files cut ~28% by removing emitted waste, not content

- **Every city's map shrank, and no city lost anything from it.** New York's
  10.33 MB was the trigger (44,361 pins, because dense stations put 71% of its
  businesses inside a ring against Los Angeles' 24%), but both fixes were
  waste in the shared renderer rather than anything New York-specific:
  New York 10.33 -> **7.42 MB**, Los Angeles 3.49 -> **2.79**, Chicago
  2.90 -> **2.14**, San Francisco 2.40 -> **1.74**, San Diego 0.90 -> **0.69**.
- **Coordinates are rounded before they reach the HTML** (`COORD_DP` in
  `map_common.py`). Folium emits a float's full repr - `40.76248502732357`, 17
  significant digits - for something drawn as a 5-pixel dot, once per pin, per
  heat point, per ring and per line vertex. **Six** decimal places, not the
  five originally proposed: six is 0.11 m, half a pixel at OpenStreetMap's
  deepest zoom (19), so nothing is visibly moved, whereas five is 1.1 m and
  about 5 px there - a pin could sit visibly off its building. The extra digit
  costs ~0.2 MB and makes "loses nothing" literally true.
- **Station and ring-band strings are emitted once and referenced by index.**
  They repeated per pin: 44,361 pins over 496 stations and 4 bands in New
  York. The callback became an IIFE returning the marker function, so the two
  lookup tables are built once at `var callback = ...` rather than once per
  pin - FastMarkerCluster injects the callback as a statement and then calls
  it in a loop, so a naive array literal inside the function would have been
  re-evaluated 44,361 times. The business name is deliberately NOT indexed:
  at 38,167 distinct values of 44,361 a lookup table would just add a second
  copy. The raw category also stays a string, because
  `scripts/check_personal_exposure.py` parses these arrays out of the rendered
  HTML and reads that field directly.
- **Verified rather than assumed.** After the change New York's map reports 3
  cluster layers and exactly 44,361 pins with no console errors, a sampled
  tooltip resolves its station and ring correctly through the index tables,
  and the exposure check re-parses the rewritten arrays to the same numbers
  (7,431 person-like names, 84 at a residential unit, 0.19%).
- **The committed outputs of all five cities were re-baselined** in one
  commit, since the renderer is shared. The all-city heat layer was kept: it
  would have saved another 2.0 MB but is a feature the other cities have.
  Further size work, if New York still loads slowly on the deploy, would have
  to reduce what is shown rather than how it is written.

### 2026-09-21 - New York added: the first city assembled from four registries

- **Step 0 disproved the plan's premise for this city.** `PLAN.md` and
  `docs/city_shortlist.md` both had New York down as "needs `nyc_dca` filled
  (Socrata `w7w3-xahh`, `business_category`)". Live verification showed DCWP's
  "Issued Licenses" file is a **regulated-activity licence list, not a business
  registry**: of 35,245 active premises licences, 13,385 (38%) are home
  improvement contractors, and the file contains zero restaurants, zero grocery
  stores, zero clothing shops, zero pharmacies and zero salons. New York City
  has no general business licence, so there is nothing for a
  one-registry pipeline to read. Built on DCA alone the map would have shown
  ~15k tobacco shops, secondhand dealers and electronics stores with two of the
  three legend buckets empty. The `nyc_dca` taxonomy skeleton was retired
  (removed from `TAXONOMY_MODULES`; it had never been used by a build).
- **Coverage is assembled from four public registries**, each authoritative for
  one bucket, live-verified the same day: DOHMH restaurant inspections
  (`43nn-pn8j`) for Food service; NYS Retail Food Stores (`9a8c-vfzj`) for
  grocery Retail; NYS Appearance Enhancement & Barber *business* licences
  (`y3u4-jbgh`) for Personal services; and DCWP premises licences for a narrow
  regulated Retail slice. Rejected alternatives: two registries only (drops
  Personal services entirely), and DCA alone (a misleading map of New York).
- **The architecture absorbed this without touching the shared map code.**
  `pipeline/taxonomies/new_york.py` dispatches `classify()` on a `source`
  column carried through `EXTRA_COLUMNS` - the same mechanism Chicago already
  used for `business_activity` - so `map_common.py` needed no change for
  multi-source. Category verdicts followed `chicago_license.py`'s stated
  standard (buckets track NAICS 44/45, 722, 812, so cities stay comparable)
  rather than fresh per-category judgment: that is what excluded pawnbrokers,
  appliance repair, car washes and hotels, each of which Chicago already
  excludes by name.
- **DCA's 8,854 active `Individual` licences are excluded wholesale** by
  filtering to `license_type='Premises'`. They are licences held by a person -
  sightseeing guides, locksmiths, pedicab drivers, process servers - not
  storefronts, and frequently at the licensee's home. Same reasoning as the
  national NAICS 454 exclusion. The three DCA adjunct categories (tobacco,
  e-cigarette, stoop line stand) are a permission a business holds rather than
  the business, so they are ranked last in the dedup and add a pin only where
  no other registry names that site - the treatment Chicago gives its own
  TOBACCO licence.
- **Lines, not services, and the legend obstacle forced it.** The feed carries
  29 routes, which are service patterns over ~11 physical lines. The label
  layout treats the legend as an obstacle `178 + 19*n_lines` px tall in a 650 px
  map, so 29 lines gives a 729 px obstacle - taller than the map, leaving no
  clear space, and every label collides. MTA's own `route_color` groups the 29
  into exactly the trunks it signs and prints, which is both the fix and the
  more honest geography (the 4, 5 and 6 are one line up Lexington Avenue).
  11 entries -> a 387 px obstacle, and all 11 labels placed without collision
  on the first render. Two deliberate departures from the colour grouping: the
  L is split from the three shuttles (MTA paints all four grey, but the
  14 St-Canarsie line is a full line), and the shuttles share one entry rather
  than three legend rows for 2, 4 and 5 stations.
- **One shared-code change**, generic rather than New York-specific: a line's
  geometry may now be several polylines under one label, colour and legend
  entry (`load_line_shapes` accepts a tuple of shape_ids and returns segments,
  longest first; the label anchors to the longest). A trunk is one line through
  the core and branches outside it. All four existing cities re-rendered
  **byte-identical**, which is how the change was verified non-breaking.
- **New York is the only city that does not use the shared ring edges.**
  Stations sit a median 482 m apart - almost exactly the 0.6 mi outer ring used
  elsewhere - so those rings would reach past the next two stations in every
  direction. Edges halved to `[0, 0.05, 0.1, 0.2, 0.3]` mi, which is what the
  add-city skill's "unless station spacing is meaningfully different" clause
  was written for. Stations were **not** thinned: unlike San Francisco's
  street-running Muni stops, every NYC subway station is a full station, so the
  sub-transit-line filters do not apply.
- **Rings start switched off here, rather than being removed.** Even halved,
  253 of 496 stations are closer together than the outer ring, and a rendered
  check showed the rings merging into an indistinct wash over Manhattan - but
  reading cleanly around the outer-borough and Staten Island stations. So
  `render_heatmap` gained a `rings_shown` flag (default True, False for New
  York) and the rings stay in the layer control. Preferred over dropping them,
  which would have lost real information for ~243 stations.
- **Staten Island Railway included**, on the condition that it be properly
  covered by data: it is, across all four registries (1,114 DOHMH
  establishments, 2,078 DCA premises licences, 654 salon licences, 520 retail
  food stores - more businesses than San Diego's entire mapped set), with 21
  clean GTFS stations and full shape geometry.
- **Two coordinate problems that looked like one.** 16,692 rows had source
  coordinates outside the city's bounding box, and the first pass wrongly sent
  all of them to the geocoder. They are two populations: 16,073 are valid New
  York State points that are simply not in the city (15,387 of them upstate
  salons in Watertown, Buffalo, Utica - the two NYS registries are statewide
  and carry no NYC marker), and 619 are not valid New York points at all, 409
  of them exactly (0,0), belonging to real New York businesses. The first are
  dropped as out of scope; only the second are geocoded. Conflating them would
  have wasted ~16k geocoder calls and risked placing an upstate salon back
  inside the city on a same-named street. `NY_STATE_BBOX` is the discriminator.
- **Cross-source dedup merges on address AND name, not address alone.** One
  New York address routinely holds many distinct storefronts, so address-only
  merging would delete real businesses; 14,830 rows share an address with
  another row. Keying on address plus a normalised name under-merges instead -
  a spelling difference between two registries leaves a business counted twice -
  which inflates density slightly rather than erasing storefronts. Both numbers
  are printed by step 2 so the trade-off stays visible, and the city page says
  so.
- **Counts.** 104,366 rows across four registries -> 84,331 storefront rows
  with a name -> 15,454 dropped as out of scope -> 64,092 after one-row-per-site
  -> 63,311 inside the borough polygons. Step 3 recovered 582 of 1,449 missing
  coordinates by Census geocoding (57.6% match rate on 1,390 geocodable rows,
  161 rejected as out of bounds, 57 more dropped as outside the boroughs) and
  lost 867 rows (1.4%), spread evenly across sources (0.3%-2.2%) and all three
  buckets - no systematic bias. Final: **62,444 businesses, 44,361 pins within
  a ring, 496 stations, 11 trunk lines, 24 shapes drawn.** Buckets: Food
  service 29,910, Retail 22,614, Personal services 10,787.
- **Exposure check: the cleanest large city so far, and the first where the
  measurement is real.** `scripts/check_personal_exposure.py` reports 84 pins
  (0.19%) with a person-like name at a residential unit, against Los Angeles
  5.67%, San Francisco 1.95%, Chicago 0.09%. Two reasons, both structural
  rather than lucky: **no registrant-name column is ever loaded** (the salon
  registry's `license_holder_name` is not even downloaded, and step 2 asserts
  it never arrives), so no pin can be one; and DCA supplies a **structured**
  `unit_type` (APT, STE, FL, RM as separate values), which is carried into the
  processed file as a `unit` column. That last point matters because San
  Diego's 0.04% was a measurement gap - its unit values are bare ("A", "101")
  with no token to match - whereas New York's number is measured. The 16.8%
  person-like-name rate sits at the documented false-positive floor and is
  concentrated in restaurants, coffee shops and grocers: the benign shape.
  The exposure script also now reports residential and commercial unit
  designators separately for every city, which revised the recorded figures
  slightly (Los Angeles 5.49% -> 5.67%, San Francisco 1.48% -> 1.95%) because
  FL/RM/PH/BSMT had not previously been counted as residential; the ranking is
  unchanged and the script's output is now the canonical measure.
- **Stated as a limitation on the city's page, not buried: New York's Retail
  bucket is less complete than the other cities'.** A clothing shop or bookshop
  needs no licence from any of the four registries and is therefore absent,
  while restaurants are close to fully covered because every one is inspected.
  The balance between categories here is a fact about New York's licensing, not
  about its high streets.
- **`docs/data_sources.md` created** as the master provenance list for all five
  cities - 8 business registries, 5 GTFS feeds, 5 boundary layers and the
  geocoder, each with its endpoint, download filter and retrieval date - and
  recording sources was added to the `add-city` skill. Two findings from
  writing it: `tqmj-j8zm`, the New York borough-boundary dataset ID in wide
  circulation, now returns 404 (`gthc-hcne` is live), and MTA's
  `web.mta.info/developers` GTFS path is dead (an S3 bucket replaced it). It
  also surfaced that **San Francisco's boundary layer has no recorded endpoint
  anywhere**, so that city cannot currently be rebuilt from scratch; logged as
  a gap in that file.

### 2026-09-21 - Legend stays broad; the exclusions page carries the detail

- **The map legends keep their broad labels** ("Retail - NAICS Code: 44/45",
  "Personal services - NAICS Code: 812") even though `454` and `81293` are now
  carved out of those prefixes. Precise labels were drafted and rejected as
  clutter on the map itself: "Retail - NAICS 44/45 (excl. 454 nonstore)" reads
  badly in a legend and would need re-editing every time a verdict changes.
- **`docs/excluded_categories.md` is the single place the detail lives**, and it
  is written to be published as prose. Surfacing it in the app (a page, or a
  link from each city page) is deliberately deferred - open in `PLAN.md`.
- **The gap this leaves, stated plainly:** until that page is surfaced in the
  app, a visitor reading the legend would infer the map covers all of NAICS
  44/45 and 812, which it no longer does. That is acceptable while the site is
  unpublished and is a blocker for the public deploy, not for development.

### 2026-09-21 - Nonstore retailers and parking excluded everywhere; solo massage in SF

- **A full sweep of every city's mapped categories found the remaining problem
  was definitional, not a privacy carve-out.** Ranking every classification by
  personal-name-plus-residential-address signal (rather than only checking the
  three codes already named) surfaced NAICS **454 "Nonstore retailers"** -
  electronic shopping, mail-order, direct selling, vending operators, fuel
  dealers. NAICS itself calls these nonstore; the `45` retail prefix in
  `NAICS_GROUPS` had been pulling in the whole family. They were 10.1% of Los
  Angeles's pins, 9.0% of San Diego's and 1.7% of San Francisco's, and `454390`
  (direct selling) was the largest remaining group of mapped personal names at
  residential addresses. Excluding it makes the project more correct about its
  own subject and removes the exposure as a side effect - an easier thing to
  justify than a privacy exception.
- **Two national exclusions, as `NAICS_EXCLUDE_PREFIXES` in `naics.py`, applied
  inside `naics_group()` so they win over `NAICS_GROUPS`:** `454` (above) and
  `81293` parking lots and garages. Parking was a **scope** call, not a privacy
  one (~4% residential): a parking trip is planned rather than incidental
  station foot traffic, so it sits outside this project's question. A sibling
  project had already excluded parking on the same reasoning, which the user
  confirmed. It was 888 pins in Los Angeles, 637 in San Francisco, 104 in San
  Diego.
- **San Francisco: 812990 excluded** (`NAICS_EXCLUDE_CODES` in its config, same
  printed-filter pattern as Los Angeles). Same code number as LA's exclusion but
  a different decision: San Francisco's licence data labels it "SOLO MASSAGE
  ESTABLISHMENT", not the generic "All Other Personal Services". 414 mapped
  pins, 31 (7%) with a person-like name at a residential address - the highest
  residential share of any category there, and a sensitive category (a sole
  operator working from home). Small share of the total, so the loss is marginal.
- **Counts after the rebuild.** San Diego 12,886 -> 11,270 available,
  2,971 -> 2,600 pins, map 1.0 -> 0.9 MB. San Francisco 20,067 -> 18,242
  available, 13,874 -> 12,625 pins, map 2.6 -> 2.4 MB. Los Angeles 70,168 ->
  61,208 available, 17,257 -> 14,632 pins, map 4.0 -> 3.5 MB (5.6 MB before any
  of this work, so the open map-size item is largely resolved). Chicago is
  untouched: it uses its own licence taxonomy. Los Angeles geocoding re-ran on
  4,594 addresses, 98.6% matched, 77 unrecovered (0.1%).
- **Exposure after:** person-like name at a residential address fell to 850
  (5.49% of mapped rows) in Los Angeles from 1,070, and to 201 (1.48%) in San
  Francisco from 249. Chicago 12 (0.09%) and San Diego 1 unchanged. The residual
  is now spread thinly across ordinary storefront categories (general
  merchandise, restaurants, beauty salons) rather than concentrated in one code,
  which is the shape expected from sole traders legitimately trading under their
  own names.
- **Two measurement corrections worth recording, because the first pass was
  wrong.** (1) The "looks like a person" regex flags 17-23% of pins in *every*
  city and *every* category, including full-service restaurants and taverns -
  that is the heuristic's false-positive floor (trade names that read like
  people), not exposure, and it must only be used intersected with a residential
  signal. (2) The residential test originally counted `STE`/`SUITE` alongside
  `APT`, which reported Los Angeles jewellery stores at 42% "residential"; they
  are downtown suites in the jewellery district. Splitting commercial from
  residential indicators dropped that category to 6% and moved the real offender
  to the top of the list.
- **San Diego, checked as asked and left in.** Its address text cannot carry the
  signal: `address_suite` is populated on 1,356 of 3,117 mapped rows but holds
  bare values ("A", "101") with no APT/STE token, so the 0.04% reading is a
  measurement gap, not a clean bill of health. Its better signal is
  `ownership_type`: 1,298 of 3,117 mapped rows are SOLE proprietorships, and 903
  (29%) display a name identical to the owner's. That is materially different
  from Los Angeles: San Diego's `dba_name` is never blank, so nothing was
  substituted by the pipeline - those owners chose to register their own name as
  the trading name, a deliberate public commercial act. Left in on that basis;
  revisit if a better residence signal appears.
- **`docs/excluded_categories.md`** now lists every exclusion, per city, in
  plain prose written to be published alongside the maps, including what is kept
  and why, the honest limits of the method, and an offer to remove a listing on
  the owner's request. Still open: the dataset licences and terms of use.

### 2026-09-21 - Privacy line: excluded NAICS 812990 in Los Angeles, and a standing exposure check

- **The principle, decided here and standing for every city: publish public
  commercial information, not personal information.** A trade name someone chose
  for their shop is commercial and deliberately public, and mapping it is the
  point of this project. A registrant's own name at what looks like their home is
  not, even when the registry that holds it is public. "It is in a public dataset"
  settles the licence question, not the publishing question: this project
  re-publishes the data in a new, more usable form (a searchable map pin at a
  precise coordinate), which is a different act from the registry's own listing.
  Where the two conflict, the map loses the row.
- **Why it came up.** A verification pass over the committed
  `outputs/<city>/heatmap.html` files (they are committed to a public repository
  and meant to be served publicly) measured what each pin actually exposes: a
  business NAME at a mapped COORDINATE. Los Angeles was the outlier. 68.1% of its
  raw rows carry no `dba_name`, so `step2_clean_businesses.py` fell back to the
  registry's `business_name` (the registrant) for 12,465 of 23,839 pins (52.3%);
  about 3,998 of those matched a conservative personal-name pattern, and 37% of
  the sampled rows had an APT/UNIT/STE/# in the street address. San Diego (0
  fallback pins), San Francisco (7) and Chicago (3) had no equivalent problem -
  their registries almost always carry a trade name.
- **The mechanism was already designed, and this is its first use.**
  `pipeline/taxonomies/naics.py` had recorded since the start that 812990 "All
  Other Personal Services" is a national catch-all, that a prior single-city
  hand-sample found **~90% non-storefront (home-based sole proprietors)**, that the
  verdict must be re-sampled per city, and that a city's verdict belongs in its
  own step 2. The privacy finding and that open data-quality item turned out to be
  the same rows: 812990 supplied 2,255 of the ~4,100 person-like pins. So one
  exclusion fixes both.
- **The change.** `NAICS_EXCLUDE_CODES = {"812990"}` in
  `pipeline/los_angeles/config.py`, applied as its own printed filter in that
  city's step 2 (visible in the run output, not hidden inside `classify()`), with
  the reasoning and sample recorded beside it and in `naics.py`. Scoped to Los
  Angeles: San Diego and San Francisco keep 812990 (unsampled; San Diego's codes
  are variable length, so a check there must match the `81299` prefix, not the
  6-digit code), and Chicago uses its own license taxonomy. Rejected as heavier
  than needed: dropping the registrant fallback everywhere (loses real storefronts
  whose registry simply has no dba), and removing names from tooltips entirely
  (guts the map's usefulness).
- **Effect, re-run 2026-09-21.** Step 2: 463,356 in-city rows -> 101,436
  storefront -> **70,257 after the exclusion (31,179 rows, 30.7%, removed)**.
  Geocoding: 5,986 addresses to recover (was 9,166), 5,910 matched (98.7%), 5,897
  inside the bounds, 89 unrecovered and dropped (0.1%; 0.2% among businesses
  started 2020 or later - the residual bias). Final: 70,168 rows available,
  **17,257 within-ring pins (was 23,839)**, map **4.0 MB (was 5.6 MB)**, which also
  reduces the open map-size item. Exposure: person-like pins traceable to the
  fallback **3,998 -> 1,803**; person-like pins overall **6,436 -> 3,948**; the
  APT/UNIT share of those 37.0% -> 33.9%. The other three cities are untouched and
  byte-identical (drift check re-run).
- **A standing check, not a one-off:** `scripts/check_personal_exposure.py` runs
  over any city's rendered map and reports the fallback-only pins (joined back to
  the raw trade-name column - the authoritative measure), the person-like names (a
  heuristic), their classifications, and how many sit at an address with a unit
  indicator. A new city must be added to its `REGISTRIES` table. It is wired into
  `add-city` and `CLAUDE.md` as a pre-publish gate. It deliberately prints numbers
  rather than a pass/fail: the judgment is per city and belongs in this log.
- **Honest limits of what was done.** The personal-name test is a regex heuristic:
  it flags "Jane Smith" and misses "J Smith Consulting", and it cannot tell a sole
  proprietor trading under their own name (a real storefront) from a registrant at
  home. The APT/UNIT indicator is a proxy for a residence, not proof. No row was
  individually verified against any other source, and no individual was contacted.
  The dataset licences and terms of use are **still unread** (open in `PLAN.md`) -
  this entry is about what is appropriate to publish, not about what the licences
  permit.
- **Left open, and now visible.** After the exclusion, Los Angeles's largest
  person-like group is NAICS **454390 "Other Direct Selling Establishments" (419
  pins)** - direct selling is inherently not a storefront and often home-based, so
  it is the obvious next candidate, along with the still-unsampled 812930 (parking)
  and 459999. San Francisco retains 113 person-like 812990 pins and a 14.7%
  unit-indicator share; San Diego 27 (`81299` prefix) and 0.1%. Chicago's
  person-like pins are trade names in storefront license types (Retail Food
  Establishment, Tavern) with a 0.8% unit share, which is the benign shape.

### 2026-09-21 - A "Cities" dropdown on each city map (closing the hop gap)

- **Added a city menu next to the "All cities" button on every city map, so a
  visitor can go straight from one city to another.** Decided with the user from
  the options laid out for the pilot's one recorded gap (two steps through the
  macro map to change city): a small dropdown, top-right, listing the other
  cities, keeping the map-only look. Alternatives not taken: previous/next arrows
  (an arbitrary order) and restoring the switcher on city pages (brings back the
  city links the pilot removes).
- **Built as a native `<select>`** in the shared renderer's control group
  (`THEME_TOGGLE_HTML`), so it is keyboard-accessible and uses the phone's own
  picker; a placeholder "Cities" is shown until one is chosen. It lists the
  other three cities and leaves out the current one, and it is hidden outside the
  app like the "All cities" button.
- **The city names come from the page, not the map.** The city page's hidden
  container (`map-only-nav`, renamed from `map-only-back-link`) now holds a link to
  the Overview and one per city, all generated from `app/cities.py`; the menu
  reads those links and clicks the chosen one, exactly as "All cities" does.
  Because the static map HTML does not embed the city list, **adding a city
  needs no map regenerated to appear in every menu**. The current city is worked
  out from the page URL (`/Chicago_Heatmap` -> Chicago), which relies on the
  `<Name>_Heatmap` page naming already used by every city and the scaffold. The
  menu is filled when the map loads, again after 0.8 s and 2.5 s (the page's links
  can render just after the frame), and when it is opened.
- **Light/dark travels with it**, as with the back button: the current mode is
  saved before navigating.
- **Layout.** The three controls form one right-aligned group that wraps and is
  capped to leave the zoom control clear (`max-width: calc(100% - 56px)`); at
  480 px or narrower the buttons are a little smaller.
- **Checked in a browser** (lean venv, clean tree). Chicago's menu lists San Diego,
  San Francisco and Los Angeles; the three controls sit side by side without
  overlapping (x 690-774, 782-878, 886-990 in a 1000 px frame). With Chicago in
  dark, choosing San Francisco opened it in place (the browser window object
  survived) and in dark, with a menu of the other three including Chicago; light
  from there to Los Angeles, then "All cities", stayed in place and in light. At
  375 px (343 px frame): one row at x 75-333, clear of the zoom control at
  x 10-44, no sideways scroll. All four standalone maps: no label problems, the
  menu hidden, no console errors. The closed dropdown is dark in dark mode (its
  computed colours and colour scheme); the open native list was not inspected.
- **A slip fixed on the way.** My first edit script updated the map renderer but
  aborted before the app page (a comment I matched had been wrapped differently),
  so for a moment the maps carried a menu with no links to read. Caught because
  I tested the running app before anything was committed; the page edit was then
  redone against the exact text.
- **Known gaps.** The open dropdown list is the browser's native one, so its look
  varies by browser (Opera GX, not tested, should match Chromium). If the app's
  page ever renders the hidden links late, the menu waits for them (2.5 s) and
  otherwise stays hidden. `deploy-verify` was not run.

### 2026-09-21 - Keep the Overview's fallback link list in the map-only pilot

- **Decided to keep the list of city links under the macro map for now.** It was
  the one open question from the map-only pilot (see the previous entry). The
  user viewed the running build (`8c59cb4`, `MAP_ONLY_NAV` on) and judged the
  list worth keeping. It stays the keyboard and screen-reader route to a city,
  and the route if the map fails to load.
- **Still open:** the pilot's overall go/no-go and whether visitors need a way to
  hop from one city to another without returning to the map. The list can be
  revisited (it is one block at the bottom of the Overview page) if the pilot
  is judged on how intuitive the map alone is.

### 2026-09-20 - "All cities" button and a map-only navigation pilot

- **Added an "All cities" button to every city map, and started a pilot that makes
  the macro map the only navigation.** The button (top-right, left of the Dark
  Mode button, in the shared renderer `pipeline/map_common.py`) takes a visitor
  back to the macro map. With it in place, the sidebar page list and the city
  switcher are hidden on every city page (`MAP_ONLY_NAV = True` in
  `app/cities.py`). Requested by the user, who wants to see whether a map-only
  site can work ("more novel"); the sidebar and city-link code is **kept** and
  documented in `docs/navigation_sidebar_and_city_links.md`, so reverting is one
  line.
- **How the button navigates.** The map is a sandboxed `st.iframe` (scripts and
  same-origin access allowed, top-level navigation not), so it cannot set the
  parent's location. It clicks the parent page's own link to the Overview, and
  Streamlit navigates in place. In map-only mode `render_city_nav()` therefore
  still renders that one link, inside a CSS-hidden `st.container(key=...)`; the
  sidebar is hidden with CSS rather than switched off in `config.toml`, so the
  link stays reachable and the change stays reversible from Python. The button
  shows only when the map is embedded (`window.parent !== window`), so a map
  opened on its own has no dead button.
- **The light/dark mode travels both ways.** The shared `localStorage` key
  already carried it; the button also saves the current mode before navigating.
  Checked: Dark on a city map, then "All cities", opens the macro map dark;
  from the dark macro map, a real click on the Chicago marker opens Chicago dark,
  Light there, then "All cities", opens the macro map light.
- **Kept: the Overview's fallback link list** (one link per city under the map).
  It is the keyboard and no-map route to a city (see the "Macro map and city
  navigation" entry). "Only keeping the main page" could also mean dropping it;
  that is left as an open question for the user rather than assumed.
- **Checked in a browser** (lean venv, clean tree). City page at 1024 px: sidebar
  hidden (`display: none`), no visible switcher, the two buttons side by side
  inside the map iframe with no overlap; navigating with the button left the
  browser window object intact (in-place, no reload) and the Overview showed the
  updated intro sentence. At 375 px: both buttons fit inside the 343 px frame
  (x 125-221 and 229-333), no sideways page scroll, sidebar hidden. All four
  standalone maps: `problems` empty, the back button hidden, no console errors.
  Not run: the independent `deploy-verify` agent (the user chose not to for now).
- **A slip fixed on the way:** the map-only CSS was first appended inside the
  existing indented Markdown block, where it rendered as a code block and hid
  nothing; it is now emitted in its own `st.markdown` call. And a JS regex in the
  button script used `\/` inside a non-raw Python string (an invalid escape
  warning); rewritten with string methods.
- **Known gaps.** A visitor arriving by URL sees only the map's button, with no
  way to hop city to city except through the macro map. The button does nothing
  if the hidden link was not rendered (the scaffold template includes the call).
  `deploy-verify`'s switcher check applies only when `MAP_ONLY_NAV` is False; its
  instructions now say what to check instead.

### 2026-09-20 - Migrated from st.components.v1.html to st.iframe

- **Replaced the deprecated `st.components.v1.html` with `st.iframe` in all four
  city pages, the macro map's Dark Mode script and the scaffold template.** The
  deploy-verify startup log had flagged that `components.v1.html` is deprecated
  in favor of `st.iframe` with a removal date (2026-06-01) already past; it still
  worked in Streamlit 1.64 and only logged a warning, but `requirements.txt` had
  no upper bound, so Streamlit Cloud installing a newer release could have removed
  it and broken every city page at deploy time. The dependency predated the Dark
  Mode work.
- **What `st.iframe` does, read from the installed source (1.64).** An HTML string
  or a `.html` `Path` is embedded as a same-origin iframe that allows scripts (the
  sandbox includes `allow-same-origin` and `allow-scripts`), read as UTF-8, and
  always scrollable. That is exactly what the pages needed, so each page now
  passes the map's `Path` (`st.iframe(HEATMAP_HTML, width=1000, height=650)`)
  and the manual `read_text(encoding="utf-8")` is gone. A fixed width is capped
  to the column, as before. The one difference: `st.iframe` rejects a height of 0,
  so the macro map's script-only frame is 1 px tall (it renders with a 1 px
  element container, no border).
- **Also added an upper bound: `streamlit>=1.64,<2`.** A cheap guard against a
  major release; it does not protect against a minor release removing an API
  (that is what the migration is for), so `deploy-verify` should still be run on
  each Streamlit upgrade.
- **A slip while migrating:** one script edit matched three pages but not San
  Diego's (its comments differ), so that page was briefly left calling the
  removed import; caught by grepping for leftovers before the first run and
  fixed by hand.
- **Checked in a browser** (lean venv, clean tree): all four city pages show the
  map in a 554x650 iframe (the column's width; fixed 1000 px map inside, as
  before), same-origin access holds, the maps and their Dark Mode buttons are
  present (line labels 5, 6, 6 and Chicago's page loads; no exception blocks);
  the macro map's button works from the 1 px iframe; Dark on the macro map opens
  Chicago dark, and Light on Chicago's map makes the macro map open light; the
  server log shows no deprecation warning on any page.

### 2026-09-20 - Dark Mode on the macro map

- **Added Dark Mode to the macro map, sharing the city maps' choice.** Decided
  with the user after a side-by-side comparison (real deck.gl renders of the
  four cities, opened in the browser pane): the button top-right, offset left of
  the zoom controls; a white pill behind each city name; and the same filtered
  basemap look as the city maps rather than Carto's native dark style.
  `components.render_macro_map_theme()` is called once from the Overview page.
- **Mechanism.** The pydeck chart is two canvases (`.mapboxgl-canvas`, the
  basemap, and `#deckgl-overlay`, the markers and labels), so the same dark
  filter is applied to the basemap canvas only, by page CSS scoped to the chart
  (`body.dark-base [data-testid="stDeckGlJsonChart"] ...`). A small script, run
  from a zero-height `components.html` iframe, adds the button to the chart's
  frame and toggles `dark-base` on the page `<body>`; a MutationObserver re-adds
  the button if Streamlit re-renders the chart. The choice is stored under the
  same `localStorage` key as the city maps (all are same-origin), so it works in
  both directions: verified that Dark on the macro map opens Chicago's map dark,
  and Light on Chicago's map makes the macro map open light. If the chart
  container is missing there is no button and the map stays light. It depends on
  Streamlit's `stDeckGlJsonChart` test id (stable in 1.64, an internal name), so
  re-check with `deploy-verify` on a Streamlit upgrade.
- **Findings from the comparison and testing.** A white halo around the labels
  (my first pick) smeared the letters at 14 px; the pill was crisp on both
  themes, so it was used, with slightly larger label offsets so pills do not
  touch their markers. Inverting only the zoom buttons' icon also inverted their
  background (the glyph is the button's own image), so the whole zoom group is
  inverted instead. At phone width the west-side "Los Angeles" pill was clipped,
  so the fitted view is padded 12% on the west. `components.py` is served
  stale by a running Streamlit after an edit (a known issue), so the server was
  restarted from a clean tree before each check.
- **Checked in a browser.** Desktop: the button is inside the frame with a 10 px
  gap to the zoom controls; clicking flips the class, label, `aria-pressed`,
  stored value, basemap filter and zoom styling, and does not touch the marker
  canvas; the choice survives a reload; a real marker click in dark mode still
  opens the city. Phone width (375 px): everything fits, no sideways scroll, all
  four names fully visible. No exception on the page.
- **Not done / limitations.** The surrounding Streamlit page stays light (deferred
  while a custom theme is considered). The page keeps the `dark-base` class on
  `<body>` after navigating to a city page (harmless: nothing there uses it) and
  resets it when the macro page loads again. Not tested: widths between 375 and
  1024 px, and the (i) attribution icon is only lightly restyled.

### 2026-09-20 - Dark Mode on the city maps (top-right button, persisted)

- **Added a Dark Mode toggle to every city map, through the shared renderer
  (`THEME_TOGGLE_HTML` in `pipeline/map_common.py`); all four maps
  regenerated.** Decided with the user: a separate top-right button (not the
  layer control), remembered between maps, city maps first. The macro map and
  the surrounding Streamlit page are not done (see below).
- **Why the button is `position: fixed`, not a Leaflet control.** The map is a
  fixed 1000 px wide (the Leaflet.heat init workaround) and Streamlit's content
  area is often narrower, which pushes anything anchored to the map's own
  corners off-screen. Measured in the running app: at 1024 px the iframe is 554
  px wide and Leaflet's top-right corner sits at x=1000, off-screen; a fixed
  element stays inside the visible frame, as the legend already does. At 375 px
  (iframe 343 px) the button spans x=293-333, visible. This is why an earlier
  sister project's top-right placement had been avoided.
- **Mechanism.** A `<button>` toggles a `dark-base` class on `<body>`; the
  choice is saved in `localStorage` under one key, so it carries from one city
  to another (the embedded map iframes share the app's origin; checked:
  opening San Francisco after choosing Dark on Chicago came up dark with no
  click, and switching back restored every style). Only the tile pane is
  filtered (`invert` plus `hue-rotate`, so water stays blue), so no second base
  layer and no new tile provider or key. Recoloured: legend, zoom and layer
  controls, attribution, tooltips, ring outlines (lightened), station dots
  (lightened), transit lines (brightened), line-name labels (brightened, with
  a dark halo) and the legend's line swatches. The palette is one CSS
  variable block, tinted toward the teal theme. The legend gained a
  `map-legend` class.
- **Checked in a browser.** In the embedded Chicago map at 1024 px: the button
  is visible in the narrow iframe; clicking flips the class, label,
  `aria-pressed`, stored value, legend, tiles, rings, station dots and the
  button itself. All four standalone maps pass `scripts/check_map_labels.js`
  in light mode (labels in view, no overlaps, none under the legend or the
  button); Chicago and Los Angeles were also viewed in dark; no console
  errors. Not viewed in dark: San Diego and San Francisco (same code).
- **Known limitations.** The Brown and Purple lines are brightened, not
  swapped for a dark-mode palette, so they read but are not ideal. The
  legend's category dots keep their light-mode colours. The toggle does not
  follow the operating system's dark preference (every visitor starts light
  until they choose). The button text is not translated or localized. The
  macro map (pydeck) and the Streamlit page stay light: the map's basemap has
  a `dark` style but the choice would have to be shared between Streamlit's
  Python state and the browser's `localStorage`, which needs its own design;
  the page chrome is deferred because a custom theme may replace it.
- **Verification script.** `scripts/check_map_labels.js` now also checks the
  button is in view, not over a label, and flips and restores the theme.

### 2026-09-20 - City scaffolding skill built

- **Built `scripts/scaffold_city.py` and the `scaffold-city` skill.** This was
  deferred until after Chicago so the shared fields could be chosen with a
  local-taxonomy city in hand (see "City scaffolding: threshold met, build
  deferred"). The script writes what is identical in every built city: the
  `pipeline/<slug>/` package with `config.py` and the map script, the
  `data/` and `outputs/` folders, the app page (next free number), and the
  `app/cities.py` entry. The projected CRS is derived from the marker longitude
  and its derivation written into the config (Dallas 32614, New York 32618,
  Boston 32619 in tests; Chicago's 32616 matches). Every value only the city's
  data can supply is a `TODO`, including the page prose and the blurb, and the
  map script refuses to run while `LINE_SHAPES` is empty, so a drawn line cannot
  lack a label and legend entry.
- **Custom taxonomies are handled three ways.** A NAICS city leaves the raw
  column as a `TODO`. A built local taxonomy is reused: the config takes its
  `VALUE_COLUMN` and, if it defines `EXTRA_COLUMNS`, notes that those columns
  must survive step 2. A new local taxonomy is scaffolded with `--new-taxonomy`
  as an empty, registered skeleton module. What Chicago showed to be
  taxonomy-specific rather than universal (a second classifying field,
  one-row-per-site with a license priority list, a dated snapshot of a term
  history) is written up in the skill as guidance, not generated.
- **Scope, as planned: not steps 1 and 2.** `step1_stations.py` and
  `step2_clean_businesses.py` differ per city (a spatial boundary filter,
  sub-transit-line filters, a cities-boundary join plus geocoding, per-site
  logic) and hold most of the effort, so the skill maps each situation to the
  built city to copy (San Diego, Los Angeles, San Francisco, Chicago) rather
  than generating a stub that would be mostly rewritten.
- **Shared `data/registry.yaml` still not built.** The scaffold delivers what
  the registry was for (one place a new city's shared fields come from) as
  generated files, so nothing needs a runtime loader; the deployed app must
  stay free of pipeline dependencies, and a loader would have meant rewriting
  four cities' configs. Revisit only if something has to read city settings at
  run time.
- **Tested against a scratch copy of the repo structure, not the real repo.**
  Dry run, real run and re-run (a first version created a duplicate page on
  re-run; fixed so an existing city's page is kept); a two-word name with
  `--map-step 4`; a reused local taxonomy with `EXTRA_COLUMNS`; a new
  taxonomy skeleton, importable and registered; an unknown taxonomy is
  refused; all generated files compile and every generated `config.py`
  imports; the map script exits with its message while `LINE_SHAPES` is empty.
  A dry run against the real repo for Chicago skips every existing file.
  Not tested: a full city built end to end from the scaffold (the next
  city build is that test).
- **Saving.** Expected to be modest, roughly 10% of a city's cost (an estimate,
  not measured); the next city build should record whether it held.

### 2026-09-20 - Macro map and switcher adjusted for a fourth, distant city

- **Adding Chicago broke the macro map on a phone and clipped the switcher; both
  fixed.** The `deploy-verify` run on the Chicago commit found: (1) at 375 px
  wide, San Francisco and Chicago fell outside the map, because the fitted
  view's zoom floor (3.0) was tighter than the 2.3 that Chicago plus California
  need; (2) at the fitted zoom the Los Angeles and San Diego markers, about 180
  km apart, touched, and their names collided; (3) at 1024 px wide the city
  switcher's fixed columns clipped "San Francisco" and "Los Angeles".
- **Changes.** The zoom floor is now 1.0 and the fit assumes a 320 px canvas.
  Markers shrank from radius 11 to 6 pixels. Each city may set an optional
  `label` side in `app/cities.py` ("top" by default; San Diego "right", Los
  Angeles "left"), so the three California names read cleanly. The switcher is
  a wrapping horizontal container (`st.container(horizontal=True)`, available
  in the minimum Streamlit, 1.64) instead of fixed columns, so a long name
  wraps to a second line instead of being cut.
- **Checked in a browser** (lean venv): all four cities visible and named on
  desktop and at 375 px; real clicks on the San Diego, San Francisco, Los
  Angeles and Chicago markers each open their own page; no switcher item clipped
  at 1024 px (Chicago wraps to a second line).
- **Known limitation.** On a phone-width map the Los Angeles and San Diego dots
  still touch (about 7 px apart), so tapping the right one is fiddly; the
  fallback link list below the map is the reliable route. Grouping nearby
  cities on the macro map (already in `PLAN.md` under "Later") would remove it.
  The dark theme and widths between 375 and 1024 px were not tested.

### 2026-09-20 - Chicago built

- **Added Chicago: the CTA 'L', City of Chicago stations only, on the city's
  own license taxonomy.** Pipeline `pipeline/chicago/` (config, step 1
  stations, step 2 clean businesses, step 3 map), page `app/pages/
  4_Chicago_Heatmap.py`, `app/cities.py` entry, and `outputs/chicago/`.
  Verified in a browser: 7 line labels in view with none overlapping, legend
  collapses, no console errors. Baseline counts, run 2026-09-20 against the
  raw snapshot taken that day:
  - Step 1: 141 stations across the seven lines; 123 in the city, 18
    suburban stops excluded (Austin, Cicero, Davis, Dempster, Forest Park,
    Foster, both Harlems, Central, Linden, Main, Noyes, both Oak Parks,
    Ridgeland, Rosemont, South Boulevard, 54th/Cermak), listed in
    `excluded_stations.csv` as "Outside Chicago city limits" (the boundary
    layer holds Chicago only, so the suburb is not named). In-city stations
    per line: Red 33, Brown 26, Blue 28, Green 27, Pink 19, Purple 17, Orange
    15. Spacing: median nearest-neighbour distance 740 m, 10th percentile 284
    m, minimum 137 m; 11 stations are within 250 m of another (the Loop area).
  - Step 2: 53,039 active rows (server-filtered, snapshot 2026-09-20) ->
    49,066 with `city = CHICAGO` -> 24,612 storefront -> 24,504 with
    coordinates (108 without, none of them redacted) -> 24,504 inside the
    bounding box -> 20,686 after one row per site. Boundary cross-check:
    20,671 of the 20,686 fall inside the Chicago polygon (15 outside, kept).
    Buckets: Retail 10,321, Food service 6,573, Personal services 3,792.
  - Step 3: 123 stations; 11,796 businesses within a ring, 8,890 beyond; map
    file about 3.0 MB.
- **Transit scope, as decided: CTA only, Metra deferred** (see the "Chicago
  transit scope" entry). Yellow Line dropped, following the chopping-block
  rule: it has 3 stations and its only in-city one, Howard, is also served by
  Red and Purple.
- **Corrections to the earlier expectations, from the GTFS.** Purple is not a
  near-empty line: it has 17 in-city stations (its rush-hour Loop express runs
  on Brown's stations). But its most-used trip shapes are the Linden-Howard
  stub in Evanston (1% inside the city), so the drawn shape is the Loop-express
  shape (shape 309200024, 58 trips, 40% inside), the only one reaching the
  city; it overlaps Red and Brown between Howard and the Loop. Every other
  line uses its single most-used shape. The feed has 143 parent stations
  against CTA's stated 145. There are only 55 active license descriptions,
  not the 150 in the full history.
- **'L' shape: uniformly sparse, so no spacing filter,** as expected. The
  Loop and Loop subway are the exception: Jackson and Monroe each have a Blue
  and a Red station about 140 m apart, and LaSalle and LaSalle/Van Buren are
  137 m apart. CTA counts them as separate stations and they were kept as CTA
  counts them; their rings overlap, a conscious choice (each business is
  assigned to its nearest station, so nothing is double-counted). A station
  is a GTFS parent station, so no name-alias list was needed.
- **Full license mapping** (approved before writing; `pipeline/taxonomies/
  chicago_license.py`, 21 test cases pass). Direct: Tavern is Food service;
  Package Goods, Filling Station, Secondhand Dealer and Tobacco are Retail.
  By business activity: Limited and Regulated Business License (rules in the
  "catch-all license types" entry); Retail Food Establishment (11,100 active
  rows) is Food service when any part prepares or serves food (6,295) and
  Retail otherwise (4,802), and the 949 mixed rows (a grocery with a deli) go
  to Food service, a rule that does not depend on the order the city lists
  activities; Animal Care License (395) is Personal services for grooming and
  Retail for retail sales, with veterinary hospitals, boarding and shelters
  excluded. Excluded outright: the adjunct licenses Consumption on Premises
  (2,820 rows), Outdoor Patio (731), Late Hour (119) and Music and Dance (46),
  because they attach to a business already counted (only 110, 15, 3 and 3
  sites respectively have no primary license, a trivial loss); Motor Vehicle
  Services (1,536, body and repair shops) and Commercial Garage (581, parking
  operators); and Pawnbroker, Pop-Up Retail User, shared kitchens, mobile and
  event food, Peddler, Public Place of Amusement, Children's Services,
  Manufacturing, Wholesale Food, Raffles, Valet, Shared Housing and the
  remaining long tail.
- **One row per site, primary license first.** A site (account number plus
  site number) can hold several licenses, so after classification the rows
  are reduced to one per site, taking the license earliest in
  `LICENSE_PRIORITY` (Retail Food Establishment, Tavern, Limited, Regulated,
  Package Goods, Filling Station, Secondhand Dealer, Tobacco). This collapsed
  24,504 rows to 20,686. Tobacco therefore counts only where a site has no
  primary license: 222 sites, real smoke shops and dollar stores.
- **No geocoding step.** Coordinates are valid (all 48,614 active in-city rows
  with coordinates were inside the bounding box, unlike Los Angeles), and 108
  storefront rows (0.4%) have none; their addresses are not redacted. That
  loss is small, but its bias was not analyzed (by start year, category or
  area), so the loss is recorded as a known limitation and not dismissed. If
  it matters later, add a Census-geocoding step as Los Angeles did.
- **Shared-code change.** `pipeline/map_common.py` now passes a taxonomy's
  `EXTRA_COLUMNS` to `classify()` when grouping pins by category, as
  `filter_to_storefront()` already did; without it Chicago's activity-classified
  rows would have matched no bucket. Drift check on San Diego, San Francisco
  and Los Angeles: zero drift.
- **Known limitations.** The `raw` file is a dated snapshot (`AS_OF_DATE` in
  config), and re-downloading it changes the counts. Chicago's Retail and Food
  service buckets come from local license types and activity text, so they
  are comparable to the NAICS cities' 44/45 and 722 only approximately; the
  mixed grocery-with-deli rule and the exclusion of gyms and fitness (NAICS
  713940 and 611620 are outside the three buckets) are the main judgment
  calls. Home-based businesses are excluded as not being storefronts. Tooltips
  show the license type ("Retail Food Establishment"), not the activity.

### 2026-09-19 - Pin line endings with .gitattributes

- **Added `.gitattributes` (`* text=auto eol=lf`) to stop the recurring
  "LF will be replaced by CRLF" warnings.** The repository already stores LF
  in every tracked file; the warnings came from `core.autocrlf=true` on the
  Windows machine converting to CRLF in the working copy (37 tracked files
  were CRLF on disk). Pinning LF removes the mismatch without changing what
  is committed. Checked: `git status` showed only the new file, and the drift
  check across the three cities still shows zero drift (it already normalizes
  CRLF to LF at byte level, so it was unaffected either way). Git config was
  not touched.

### 2026-09-19 - Chicago transit scope: CTA only, Metra deferred

- **The first Chicago build maps the CTA 'L' only; Metra is recorded as a
  possible later addition.** Each built city maps one agency's rail-transit
  system (the San Diego Trolley without the Coaster or Sprinter, Muni Metro
  without Caltrain or BART, LA Metro Rail without Metrolink), and Metra would
  break that. It would also add a second agency and feed, 11 more lines (about
  19 in the legend and label layout), low-frequency and rush-hour-only
  stations, and Metra Electric's closely spaced South Side stops, which could
  reopen the spacing-filter question. The extra effort was estimated at
  roughly 40-50% (a guess).
- **Expected 'L' shape (from general knowledge, not yet checked against the
  GTFS): uniformly sparse, so no San Francisco-style spacing filter.** All
  lines are grade-separated with stops roughly a half to a mile apart and no
  street-level streetcar offshoots. Instead, five lines share the downtown
  Loop (their polylines overlap and the station rings overlap heavily there),
  and the Purple and Yellow lines run mostly outside Chicago (Evanston,
  Wilmette, Skokie), as do stops on Green, Pink and Blue (Oak Park, Cicero,
  Forest Park). To be verified in the build by computing stop spacing per
  line and counting stations inside the city boundary.
- **Chopping-block order if the map is too much:** Yellow and possibly Purple
  first (a line with essentially no in-city stations is dropped rather than
  drawn, since every drawn line needs a label and a legend entry), then
  suburban stops (removed automatically by the boundary filter). The core six
  lines (Red, Blue, Brown, Green, Orange, Pink) stay.

### 2026-09-19 - Chicago catch-all license types classified by activity

- **Classified Chicago's two catch-all license types by `business_activity`,
  in `pipeline/taxonomies/chicago_license.py`.** "Limited Business License"
  and "Regulated Business License" (about 39% of active licenses) say nothing
  about the business, so they use the activity text. Rules, approved before
  writing: Retail = retail sales activities (general merchandise, clothing,
  jewelry, cell phones, flowers, furniture, art, vehicle parts, funeral items)
  plus vehicle sales; Personal services = hair, nail, skincare, waxing, massage,
  tattoo, laundromat, dry-cleaning drop-off, clothing alterations and
  "Miscellaneous Personal Services". The buckets follow what the `naics`
  taxonomy counts (44/45 and 812), so cities stay comparable. A multi-activity
  value (parts joined by " | ") takes the first part that matches a bucket.
- **Exclusions and the calls behind them.** Anything marked "(Home Based
  Business)" is excluded (not a storefront). A catch-all row with no activity
  (2,678 rows) is excluded: nothing shows what it is. Gyms, yoga and fitness
  classes are excluded because NAICS puts them outside the three buckets
  (713940, 611620), though they are visible storefronts. Also excluded:
  administrative and financial offices, consulting, tax preparation,
  wholesale, staffing, travel, shipping and printing, car washes, hotels and
  vacation rentals, hazardous-materials storage, scavenger vehicles, and
  "Miscellaneous Commercial Services". The activity rules apply to both
  catch-alls, so the Regulated bucket keeps its few storefront services
  (massage, tattoo, laundromat, alterations) instead of being dropped whole.
- **Checked against live data.** Applied to the 20,727 active Chicago
  catch-all rows with coordinates (pulled 2026-09-19): 3,739 Personal
  services, 5,104 Retail, 11,884 excluded (Limited: 2,916 / 4,837 / 7,419;
  Regulated: 823 / 267 / 4,465). The largest excluded activities were the
  null activity, administrative offices (1,098), "Miscellaneous Commercial
  Services" (721), home-based businesses, and tax preparation (309), as
  intended. Nine spot cases (multi-activity, null, home-based, health club)
  all classified as expected.
- **The taxonomy is still incomplete.** The other ~148 `license_description`
  values (Retail Food Establishment, Tavern, Tobacco, Package Goods and the
  rest) are unmapped and still need their own mapping before Chicago is built.
  Revisit as part of the Chicago build.
- **Shared-code change.** `filter_to_storefront()` now also passes any
  columns a taxonomy lists in an optional `EXTRA_COLUMNS` attribute to
  `classify()`, because Chicago's rule needs two fields; single-column
  taxonomies (`naics`) are unaffected. Drift check across San Diego, San
  Francisco and Los Angeles: zero drift.

### 2026-09-19 - Chicago Step 0 probe (schema and counts only; no pipeline code)

- **Ran the Step 0 live check on Chicago's Business Licenses (Socrata
  `r5kz-chrr`, `data.cityofchicago.org`), capped at schema, null rates and
  category counts, to lower the cost of the build.** Nothing was built.
- **The dataset is every license term since 2002, not a current registry.**
  1,207,156 rows, `date_issued` 2002-01-02 to 2026-09-18, and
  `expiration_date` values that include junk (year 0206 and 9999). Of those,
  1,126,817 have status `AAI` (issued). Filtering to status `AAI` with
  `expiration_date` on or after 2026-09-19 leaves 53,043 rows; with
  `city = 'CHICAGO'` and coordinates present, 48,617. Those 53,043-row
  filters were checked with counts only; the expiration junk still has to be
  handled in the real filter. One account can hold several licenses at a
  site (32,875 distinct active accounts in the city against 48,617 rows),
  so the build must dedupe by account and site, as the earlier cities
  deduped.
- **Coordinates and city.** 93,098 of the 1,207,156 rows (about 8%) have a
  null `latitude`. 1,116,247 rows say `CHICAGO`; the rest are suburbs
  (Cicero, Skokie, Des Plaines and others), so the `city` field is usable
  as a first filter. Addresses are redacted (`[REDACTED FOR PRIVACY]`) on
  2,417 active Chicago rows (home-based licenses). Not yet checked, per the
  Los Angeles lesson: whether coordinates are corrupt (bounding-box test)
  and whether any in-city rows carry a different `city` value.
- **Classification is the hard part, and it is smaller than feared but
  trickier.** There are 150 distinct `license_description` values and 4,120
  distinct `business_activity` values. The biggest active buckets are
  "Limited Business License" (15,245), "Retail Food Establishment" (11,150),
  "Regulated Business License" (5,573), "Consumption on Premises - Incidental
  Activity" (2,845), "Tobacco" (1,834), and "Motor Vehicle Services License"
  (1,537). "Limited Business License" and "Regulated Business License" are
  catch-alls, together about 39% of active rows, so `license_description`
  alone would misclassify the largest groups; the `chicago_license`
  mapping will need `business_activity` for those two, with a hand-sample.
  Many other descriptions (Peddler, Raffles, Valet Parking Operator,
  Pharmaceutical Representative, Shared Housing Unit Operator) are not
  storefronts and will be excluded.
- **Transit data.** CTA's GTFS downloads (HTTP 200, 68.7 MB). Metra's feed
  did not respond at `gtfs.metrarail.com` but downloads at
  `schedules.metrarail.com/gtfs/schedule.zip` (HTTP 200, 705 KB); it was not
  opened. Whether to include Metra, and whether the 'L' (145 stations, 8
  lines) has a central-plus-offshoot shape, are still decisions for the
  build. The city boundary is Socrata "Boundaries - City - Map" (`ewy2-6yfk`),
  not yet downloaded or checked.
- **Not done:** the `chicago_license` mapping, any pipeline code, station
  selection, and the coordinate-quality check.

### 2026-09-18 - City scaffolding: threshold met, build deferred

- **The rule-of-three condition for a shared config loader is met, but the
  scaffold is deferred until after the first non-NAICS city (Chicago).** The
  earlier deferral in `PLAN.md` was "until more than two cities show the
  common shape"; three cities now exist. Comparing them: `config.py`, the
  map script and the app wiring share a shape (paths, CRS, rings, taxonomy
  name, thin call into `render_heatmap()`, a `cities.py` entry and page),
  while `step1_stations.py` (spatial filter, sub-line spacing filter, or
  cities-boundary join plus Census geocoding) and `step2_clean_businesses.py`
  differ per city and hold most of the per-city effort.
- **Why wait rather than build now.** All three built cities have GTFS and
  NAICS, so the shared fields were drawn from cases that resemble each
  other; Chicago is the first with a local taxonomy and possibly commuter
  rail, and would show which config fields are truly universal. Building it
  also needed budget that was not available in the session. Expected saving
  is modest, roughly 10% of a city's cost (an estimate, not measured), so it
  is medium priority. Scope is config, the map script and app wiring only,
  not steps 1 and 2.

### 2026-09-18 - San Diego excluded-stations audit file

- **San Diego now writes `outputs/san_diego/excluded_stations.csv`, as San
  Francisco and Los Angeles already did.** It lists the 16 Trolley stations
  outside city limits with the municipality each is in (La Mesa 5, Chula
  Vista 3, El Cajon 3, Lemon Grove 2, National City 2, Santee 1). The city
  filter now joins against every municipality in the SANDAG layer once, so
  the same join both keeps San Diego and labels the excluded stations; the
  kept set is unchanged (47 of 63). Drift check: only the new file differs.
  The file has the same columns as Los Angeles's (`station`, `latitude`,
  `longitude`, `located_in`).

### 2026-09-18 - Live check of Dallas, Austin, Charlotte and Fort Worth

- **Checked the four cities left "not yet live-verified" against their real
  APIs, to widen the pool beyond the ranked list.** Search summaries were not
  treated as evidence (the Denver and San Jose lesson); schemas, counts,
  date ranges and null rates were pulled directly.
- **Dallas: marginal, kept as an unranked candidate.** Certificates of
  Occupancy (Socrata `9qet-qt9e`) has a real classification (`land_use`, 143
  values, plus an `occupancy` code), business names, and coordinates (2 of
  23,731 rows null), and DART's GTFS downloads. But the data ends 2022-11-15
  and covers only certificates issued 2018-2022, so it shows new occupancies,
  not a registry; a city page would have to say so. This corrects the earlier
  search-level note that the dataset lacked a classification field. Its
  effort rank sits after Boston (needs a new taxonomy module) and would be
  set when it is built.
- **Fort Worth: ruled out on rail, though the data is workable.** The
  certificate table (72,065 rows since ~2002, `JobUse` with 48 values,
  coordinates, current through 2026) has ~19% of rows without coordinates,
  null city and address fields on most rows, and repeats a business when it
  relocates. With only TEXRail and the Trinity Railway Express, the map would
  have few stations. Revisit if rail expands.
- **Austin: ruled out.** The dataset named "Certificates Of Occupancy" is
  291,759 construction permits with a yes/no flag and no business name or
  classification; the business datasets found are small (64-row credit-access
  list, vendor lists). One MetroRail line.
- **Charlotte: ruled out.** The city hub has no business or license dataset
  (zoning, permit-review, and hand-curated grocery/pharmacy/medical points
  only), and Mecklenburg County's GIS page listed none. Rail is small.
- **Not checked:** Dallas's Commercial Permits Activity Dashboard
  (`ync5-xnfn`), and Trinity Metro, Austin and Charlotte GTFS. The Austin and
  Charlotte rail sizes are from memory.

### 2026-09-18 - Line labels at tail ends, auto-fitted view, collapsible legend

- **Line labels now sit at each line's tail end, chosen automatically.** The
  end used is the one farthest from every other line, measured on the stretch
  inside the city (`label_focus`, now passed by all three cities). This
  replaced the per-line degree offsets (San Diego's Silver Line at 0.016, Los
  Angeles's D Line at -0.012), which had been hand-tuned against one rendering
  each and could not be reused for a new city. The label is offset in pixels
  by its own box size along the line's outward direction, so it clears the
  line at any angle and stays put at any zoom. The line spec's fourth element
  changed from an offset to a label end (`None` = automatic, or `"start"` /
  `"end"` to force).
- **Labels that would land on the same spot disperse along their lines.**
  The first version put Muni's J Church, K Ingleside and M Ocean View at the
  same south end, where they overlapped. A layout pass now tries, per label,
  the tail tip pointing out (and swung up to 80 degrees either way), then
  spots further along the line from that tail with the label beside the line,
  taking the first that clears the other labels, the open legend, the map
  controls and the map edge. Longest names are placed first.
- **The default view is now fitted rather than hand-picked.** The same layout
  pass picks centre and zoom to show every station and every label, zooming
  out in quarter steps and shifting away from the legend only if labels
  cannot otherwise be separated. Hand-picked centre/zoom constants were
  removed from the three city scripts; `center`/`zoom` can still be passed to
  override. Checked on all three maps in a browser: no line label overlaps
  another, hides under the legend, or falls out of view (labels do draw over
  cluster badges by design).
- **The legend is collapsible.** It is a native `<details open>`, so it
  starts open, collapses to a small "Legend" tab with a click, and needs no
  script. Rejected: a custom JavaScript toggle (more code, no benefit).

### 2026-09-18 - Macro map and city navigation

- **Built the macro map: the Overview is now a clickable map of every mapped
  city, and clicking a marker opens that city's page.** This is the
  area-selector macro level of the hybrid architecture (see the "Project
  origin" entry), built now that three cities exist. It uses `st.pydeck_chart`
  with `on_select="rerun"` and `st.switch_page`. pydeck ships with Streamlit,
  so it adds no dependency and keeps folium out of the deployed runtime, the
  same constraint that ruled out `streamlit-folium`. Rejected alternatives:
  a pre-rendered static folium map with links (a click would have to
  navigate the parent page from inside the sandboxed iframe, causing a full
  reload and losing the session) and keeping the plain `st.map` (no
  click-to-navigate). Markers have permanent name labels, a hover tooltip
  with the city's line names, and a plain list of page links below the map as
  a fallback (keyboard access, or if the map fails to load).
- **Added a city switcher to every city page** (`components.render_city_nav`):
  a link back to the map, then every city, with the current one shown as
  plain bold text, so a visitor can hop city to city without returning to
  the map. On a phone-width screen the row stacks vertically.
- **Moved the city list to `app/cities.py`, one source for the map, the
  fallback list and every switcher.** It had been inline on the Overview
  page; with the switcher it had three consumers. Adding a city now means
  one entry there plus its page. It stays app-side and tiny on purpose: the
  fuller per-city registry (map centre, CRS, taxonomy, data sources) is still
  open in `PLAN.md` and would live with the pipeline, since the deployed app
  must not depend on pipeline code.
- **Fixed three real bugs found by looking at the running map, not by
  reading the code.** (1) pydeck serialized `radius_units="pixels"` as the
  expression `"@@=pixels"` (an undefined variable), so markers rendered as a
  wrong-sized fill across the map; passing `pdk.types.String("pixels")`
  fixes it (the same applies to the label font). (2) pydeck's `compute_view`
  chose a zoom that cropped San Diego and San Francisco out of the same view;
  replaced with a small Web-Mercator fit (`fit_view`) that works for any
  number of cities, and corrected it once for 512 px world tiles (the first
  version was one zoom level too tight). (3) On a 375 px viewport the map
  cropped the outer cities and the fallback links were clipped; the fit is now
  sized for a phone width and city descriptions are wrapping captions.
- **Raised the tested minimum to `streamlit>=1.64`.** Click selection and
  `switch_page` exist in 1.40 (checked in a clean venv), but 1.40 needs the
  now-deprecated `use_container_width` for full width, which Streamlit
  warns will be removed; 1.64 defaults to full width, so the argument is
  dropped instead.
- **Verified against the lean venv, desktop and phone width.** A real click
  on the San Diego marker navigated to its page; the switcher moved San Diego
  to Los Angeles; the map link returned to the Overview and stayed there over
  8 seconds with an empty selection (no bounce back from a stale click); no
  sideways scroll at 375 px. Two earlier failed click attempts were my own
  pixel-mapping errors (the screenshot is scaled relative to the page), not
  app bugs: a synthetic hover at the computed position showed the correct
  tooltip.
- **Basemap: Carto's public vector style (`positron`) for the macro map.**
  pydeck's default style needs a Mapbox token. This adds Carto's tile
  service to the tile-provider decision already open in `PLAN.md` (the
  per-city maps use OpenStreetMap's raster tiles).

### 2026-09-18 - Remote

- **Pointed the repository at https://github.com/dacekroberts/expanded-heatmap
  (`origin`) and pushed all seven existing commits on `master`.** The
  remote was empty, so nothing was overwritten. This confirms the GitHub
  account behind the commit identity (`dacekroberts`, noreply address)
  chosen earlier; the branch was kept as `master` rather than renamed to
  `main`. Future commits go to this remote.

### 2026-09-18 - Los Angeles (third city)

- **Added Los Angeles: 565,498 raw rows with coordinates -> 463,356 in-city
  -> 101,436 storefront -> 92,270 with usable coordinates + 9,166 flagged
  -> 9,039 recovered by geocoding -> 101,309 final (127 dropped); 56
  stations; 23,839 of 101,309 businesses within a ring.** Source: LA Office
  of Finance "Listing of Active Businesses" (Socrata `6rrh-rzua`,
  `data.lacity.org`), downloaded server-filtered to rows with coordinates
  and only the columns step 2 uses, ordered by `location_account` so the
  file is reproducible (the full dataset is 631,925 rows). About 9% of rows
  carry no NAICS code and so are excluded from the storefront filter - a
  floor on density, like San Francisco's.
- **Found that ~9% of in-city storefront rows have corrupt coordinates,
  that the loss is heavily biased toward recent registrations, and
  recovered nearly all of them by geocoding instead of dropping them.** The
  first version of step 2 dropped everything outside the city's coordinate
  bounds and lost 9,166 of 101,436 rows (9.0%) - too many to accept
  unexamined. They were: 8,657 rows whose longitude is a copy of the
  latitude (e.g. 34.0468, 34.0468), 470 at (0, 0) or whole-degree
  placeholders, and 39 elsewhere outside the city. The loss is even across
  council districts (8.2-9.9%) and moderately uneven across categories
  (Retail 8.4%, Personal services 9.0%, Food service 11.4%), but very
  uneven by age: 22.5% of businesses that started in 2020 or later were
  affected versus 0.7-1.5% of older ones, so dropping them would have
  systematically under-counted new openings. Each row still has a street
  address, so step 2 now flags them (`coord_status = needs_geocode`,
  coordinates blanked) and a new step 3 geocodes them with the Census
  bulk geocoder: 9,066 of 9,166 matched (98.9%; 4,869 exact, 4,197
  non-exact), 27 rejected for landing outside the city's bounds, and 99.5%
  of the 9,039 accepted points fall inside the City of LA polygon.
  Residual loss is 127 rows (0.1%), 80 of them among the 37,066 businesses
  started 2020+ (0.2%). Every output row records its source
  (`geocode_source` = source | census). Rejected alternative: keep dropping
  them and document the bias - a 9% loss concentrated in new businesses is
  too large and too systematic to leave in.
- **Identified in-city businesses by `council_district` 1-15, not by the
  `city` field.** `city` holds postal community names (Van Nuys, North
  Hollywood, San Pedro, ...), all part of the City of LA; only 295,738 of
  631,925 rows say "LOS ANGELES", so an exact match would have kept about
  half the city. `council_district` is the city's own field: 1-15 are the
  council districts and 0 (151,427 rows) marks businesses registered with
  LA but located elsewhere. Independent check against the boundary
  polygon: 99.9% (92,169 of 92,270) of source-coordinate points fall inside.
- **Inserted geocoding as step 3, making the map step 4, and built
  `pipeline/census_geocoder.py` as a shared module.** This is the renumbering
  the `add-city` skill describes; `drift_check.py` needed no change. The
  module caches Census responses under `data/<city>/raw/geocode_cache/`
  keyed by a hash of each batch's contents (not just the batch number), so a
  changed input can never be served a stale answer and re-runs (and drift
  checks) stay deterministic and off the network. `requests` returned to
  `requirements-pipeline.txt`. First tested on 200 rows (95% matched)
  before the full run.
- **Kept every in-city station; the sub-transit-line filters were not
  needed.** Median spacing between in-city stations is ~0.55 mi with no
  dense street-running offshoots (unlike Muni Metro), measured before
  collapsing duplicate complex names.
- **Scoped to the City of LA: 56 of 110 stations kept, 54 excluded across 23
  other places.** Metro Rail serves Long Beach (8 stations), Pasadena (6),
  El Segundo, Hawthorne, Inglewood and Santa Monica (3 each), Azusa and
  Compton (2 each), 15 more cities with 1 each, and 10 stations in
  unincorporated areas. Covering them would need those cities' own business
  registries, sourced and verified separately - a new project, not a
  config change. All 54 are listed with the city they are in in
  `outputs/los_angeles/excluded_stations.csv`. Four per-line complex names
  (8 feed names) were collapsed into single stations after a pairwise
  distance check (Metro Center, Union Station, Expo/Crenshaw,
  Willowbrook/Rosa Parks): 114 feed names -> 110 stations.
- **Used LA County Planning's incorporated-city boundary layer and Metro's
  own rail GTFS.** The City of LA's own boundary service (`maps.lacity.org`)
  was unreachable from this environment (connection failure, other hosts
  fine), so the county layer on `services.arcgis.com` (88 incorporated
  cities, LA = the `LOS ANGELES` record) was used; it also let step 1 name
  the city of every excluded station. The GTFS is Metro's official
  rail-only feed (gitlab.com/LACMTA/gtfs_rail), current as of this run
  (calendar to 2026-10-02; includes the 2026 D Line extension shape).
- **Named lines by Metro's letters (A, B, C, D, E, K Line) and used Metro's
  official colours from the feed's `route_color`.** Names verified against
  Metro's own line-letters post and Wikipedia; the feed's "Metro A Line" has
  the brand prefix dropped, as San Diego's "Blue Line" lacks "MTS". Unlike
  San Francisco's, LA's official colours are unambiguous, so they are used.
- **Fixed line labels being hidden under big cluster badges, in the shared
  code.** Downtown LA's clusters (3,796 and 5,222 businesses) were drawn over
  the B and D Line labels, defeating a "permanent" label; San Diego's Silver
  Line had hit the same problem earlier and was worked around with a larger
  offset. Root-cause fix: label markers get `zIndexOffset=1000` in
  `map_common.add_line_label`. San Diego and San Francisco were regenerated
  (only the z-index and Folium IDs changed).
- **Added `label_focus` to `render_heatmap` so labels anchor on the in-city
  stretch of each line.** LA's lines run far beyond the city (the A Line to
  Azusa and Long Beach), so the midpoint of the whole route would fall
  off-screen in the default view. Other cities pass nothing and are
  unchanged. The B and D Lines share a subway corridor, so their labels
  landed 9 px apart; the D Line's label takes a -0.012 offset to the other
  side of the track (now 32 px apart).
- **Centred the default view on the in-city station spread at zoom 11**
  (34.05, -118.31): LA is huge and mostly not on a rail line.
- **Known limitations:** the source rounds coordinates to 4 decimals (~11 m),
  fine for ring bands of 160 m and up; recovered points are Census
  interpolations (about half non-exact); ~9% of rows have no NAICS and are
  invisible to the storefront filter; the LA map is 5.8 MB (San Francisco
  2.6 MB) - it embeds and renders correctly under the lean venv but is worth
  watching before deployment (open in `PLAN.md`).
- **Ran the drift check across all three cities after committing: zero
  drift, every count unchanged** (San Diego and San Francisco exactly as in
  the earlier baseline entry below; Los Angeles as listed above). LA's
  geocoding step replayed from its content-hash cache rather than the
  network, and the excluded-stations files were byte-identical. All three
  `heatmap.html` files differed from HEAD only in Folium's random IDs, and
  those cosmetic diffs were reverted. This is the current three-city
  baseline.
- **Verified all three cities against the lean venv:** Overview lists all
  three; each city page loads its map iframe with Leaflet, that city's full
  legend and every line label, no Streamlit exception blocks, clean console.

### 2026-09-18 - Hygiene: shared modules, tooling, and making the project standalone

- **Ran the full pipeline from scratch for both cities against the first
  commit: zero drift. This is the row-count baseline for
  `pipeline/drift_check.py`.** San Diego: 59,684 raw -> 43,563 in-city ->
  12,988 storefront -> 12,886 with coordinates -> 12,886 after bounds ->
  12,886 after dedup; 47 stations; 2,971 of 12,886 businesses within a ring.
  San Francisco: 295,151 raw -> 260,103 active -> 20,562 storefront ->
  20,093 with coordinates -> 20,067 after bounds -> 20,067 after dedup (8
  blank business names filled from the owner name); 147 line-stops thinned
  to 49 stations (J 12 of 23, K 14 of 20, L 14 of 24, M 16 of 26, N 15 of
  32, T 11 of 22 kept), 65 stops cut; 13,874 of 20,067 businesses within a
  ring. Both raw inputs were unchanged since download (2026-09-18), so
  this is a code-drift result. Both `heatmap.html` files differed only in
  Folium's random element IDs; those cosmetic diffs were reverted rather
  than committed.
- **Fixed a false positive in the new drift check: line endings.** The first
  run flagged `excluded_stations.csv` as drift. Cause: on Windows with
  `core.autocrlf=true`, pandas writes CRLF while git stores LF, so a
  regenerated CSV always differed from `HEAD` - confirmed by comparing 66
  CRLFs on disk against 0 in `HEAD` and byte-identical content after
  normalizing. `drift_check.py` now normalizes CRLF to LF at byte level on
  both sides, matching what git does on commit; still never decodes text.
  The check earned its keep on its first run by finding a real
  environment-dependent bug in itself.
- **Made the repo standalone: nothing depends on, or needs to be read
  alongside, the earlier prototype.** Removed
  `docs/starting_briefing.md` (the hand-off document; its architecture
  tradeoff reasoning is preserved in the "Project origin" entry below, its
  lessons in `project_context.md`), `pipeline/map_helpers.py` (a hand-off
  from the prototype's window that duplicated `map_common.py`; its one
  non-duplicate, the Leaflet.heat fixed-pixel-size explanation, moved into
  `map_common.py` as a comment), and the `docs/seattle_skills_for_review/`
  staging copies (byte-identical to the originals). Reworded every code,
  config and doc comment that said "the source project" to say what it
  means directly; the only remaining mentions of Seattle are as evidence
  (the catch-all NAICS hand-sample in `naics.py`, this log). Also removed:
  unused pipeline requirements (`usaddress`, `rapidfuzz`, `jupyterlab`,
  `requests`) and `altair` from the deploy requirements (the app draws no
  charts), the Altair-only CSS reset in `components.py`, the redundant
  `NAICS_STOREFRONT_PREFIXES` (duplicated `NAICS_GROUPS`) and the unused
  `load_taxonomy()` wrapper. A scan found no unused config constants or
  imports. `docs/city_shortlist.md` was rewritten as current state (its
  "update" paragraphs and struck-through table are history that lives
  here). Session tags ("Session 2") were stripped from code comments.
- **Committed skills and the subagent to the repo, and gitignored
  `.claude/launch.json` and `.venv-lean/`.** The prototype kept all of
  `.claude/` out of git as local workflow tooling. Here `CLAUDE.md` and
  `PLAN.md` name the skills and agent as part of the documented process,
  so they are committed; `launch.json` holds machine-specific ports and
  paths, so it is not (the `deploy-verify` agent recreates it).
- **Created the first git commits.** No git identity was configured
  (neither global nor repo-local), so commits pass the identity per command
  rather than writing config: `dacekroberts` /
  `49654908+dacekroberts@users.noreply.github.com`, the identity the
  owner's earlier project documented for the same GitHub account. Change it
  if that is wrong.
- **Named the log `DECISIONS.md` (uppercase), matching `CLAUDE.md` and
  `PLAN.md`,** rather than the lowercase `decisions.md` used in the
  request; case matters in git and the adopted skill refers to the
  uppercase name.

- **Split documentation three ways: `docs/project_context.md` (current
  state, rewritten in place), `DECISIONS.md` (this file, append-only),
  `PLAN.md` (open work).** Previously `project_context.md` carried all
  three, including "updated ... superseded same day" notes and per-run row
  counts inline, which made the current state hard to read and the history
  easy to lose. The layout follows the earlier single-city prototype's
  briefing / plan / decisions split. Superseded reasoning and every count
  moved here; nothing was dropped.
- **Renamed each city's `step5_map.py` to `step3_map.py`.** The `5` was a
  leftover from the prototype's pipeline, which ran two further analysis
  steps (ring/chain/ridership statistics) before rendering the map. Those
  analyses are out of this project's scope, so a city's steps are now
  1 stations, 2 clean businesses, 3 map. A city that needs an extra step
  (geocoding, say) inserts it and renumbers; `pipeline/drift_check.py`
  globs `step*.py` in sorted order, so nothing else hardcodes the numbers.
- **Decoupled step 2 from NAICS.** Both cities' `step2_clean_businesses.py`
  filtered on NAICS prefixes directly, which would have forced a rewrite
  for New York, Chicago and Philadelphia. Added
  `pipeline.taxonomies.filter_to_storefront()` (keeps rows where the
  taxonomy's `classify()` is not None); each city's config now names only
  its raw classification column (`RAW_CLASSIFICATION_COLUMN`), which step 2
  renames to the taxonomy's `VALUE_COLUMN` before filtering. Verified
  neutral: San Diego 43,563 -> 12,988 and San Francisco 260,103 -> 20,562
  storefront rows as before, and both `businesses_clean.csv` files
  byte-identical to the pre-change versions.
- **Extracted `pipeline/map_common.py` from the two near-identical city map
  scripts** (~90% duplicated once the second city existed). Fixed while
  extracting: the legend text, tooltip label ("NAICS code:") and category
  grouping were hard-wired to NAICS, so a local-taxonomy city would have
  shown wrong labels - taxonomy modules now expose `FIELD_LABEL`,
  `VALUE_COLUMN` and `legend_label()`, and a synthetic Philadelphia-style
  render contained no "NAICS" text; business and station names went into
  tooltip HTML unescaped (`<`/`&` broke or injected markup; "Park & Market"
  was affected in both cities) - now escaped; the reason for wrapping
  `FastMarkerCluster` in a `FeatureGroup` (its own `show=` doesn't hide at
  load) is commented in code. Verified by a normalized-Folium-ID diff
  against the old maps: only the escaped names and re-indented templates
  differed; point counts unchanged; browser render identical, no console
  errors.
- **Reviewed the earlier prototype's four skills and one subagent and
  adopted three, folded one, skipped one.** Adopted, adapted:
  `deploy-verify` (agent), `pipeline-drift-check` (skill, backed by a new
  `pipeline/drift_check.py`), `decisions-entry` (skill). Folded three ideas
  from `new-transit-line` into `add-city` instead of adopting it (check how
  close stations sit relative to the outer ring; grep city pages for
  hardcoded prose like "six lines"; stations excluded for lying in other
  cities are a new data-sourcing project, not a config change), because
  `add-city` already covers the same ground for this project's per-city
  layout. Skipped `safe-rename` for now (no README/devcontainer/deployment
  for it to keep in sync), leaving a one-line note in `add-city` about
  updating the Overview's `CITIES` page path on a rename.
- **Adapted the drift check for live data.** The prototype's check assumed
  a static raw snapshot. Here raw files come from live portals (the San
  Francisco dataset carries a daily `data_as_of`), so `drift_check.py`
  re-runs against the raw files on disk without re-downloading and prints
  each raw input's size and modified time, letting a reader separate code
  drift from source drift. The Folium random-ID normalization is kept.
- **Verified the app against a lean venv for the first time.** All earlier
  browser checks ran under a global Python that had folium and geopandas
  installed - exactly what a lean check exists to avoid. Built
  `.venv-lean` from `requirements.txt` alone (streamlit 1.64.0, pandas
  3.0.6; confirmed `import folium` and `import geopandas` fail there) and
  ran the `deploy-verify` procedure by hand against it: the server started
  with a clean log; the Overview listed both cities; both city pages loaded
  their map iframe with Leaflet present, all of that city's transit lines in
  the legend, and no Streamlit exception blocks; the console was clean
  except for two 404s on a *direct URL* load of a city page, which are
  Streamlit's own `_stcore/health` and `host-config` probes at the
  page-relative path (they succeed at the root path) - framework behaviour,
  not app code, and absent when navigating in-app.

### 2026-09-18 - San Francisco (second city)

- **Added San Francisco: 295,151 rows -> 260,103 active -> 20,562 storefront
  -> 20,093 with coordinates -> 20,067 after bounds/dedup; 49 stations.**
  Source: DataSF Registered Business Locations (`data.sf.gov`, Socrata id
  `g8m3-pdis`), downloaded pre-filtered server-side to
  `city='San Francisco'` (the full dataset is ~356k rows including
  out-of-city registrants). Pre-geocoded via a WKT `location` point, so no
  geocoding step. Active = `administratively_closed` blank. Only ~37% of
  San Francisco rows carry a NAICS code (self-reported), so density is a
  floor, not a count.
- **Scoped rail to Muni Metro (J/K/L/M/N/T, route_type 0); excluded the F
  heritage streetcar, the cable cars, and BART.** F is a separately
  branded service with different rolling stock; cable cars are a different
  mode; BART is regional and crosses county lines, which would have
  reintroduced the cross-boundary scoping problem San Diego needed.
- **Thinned Muni Metro's stations from 147 stops to 49 using four ordered
  filters** ("sub-transit-line filters", `docs/sub_transit_line_filters.md`):
  subway stations always kept; each line's two terminals always kept;
  surface stops thinned to ~1 per 0.5 mi measured along the line's real
  stop-to-stop path from the most recently kept stop; stops shared by 2+
  lines force-kept. Rejected: keeping all 147 (rings overlap continuously,
  flattening the distance gradient) and subway-only (~12 stations; a real
  check found 74% of the 125 surface stops are more than 0.6 mi - the
  outermost ring - from the nearest subway station, median just over 1 mi,
  so it would have dropped the Sunset, Bayview/Visitacion Valley and
  Ingleside districts entirely). The four-filter design was specified by
  the owner. 65 cut stops are documented (line, reason, nearest kept
  station, distance) in `outputs/san_francisco/excluded_stations.csv`.
- **Hand-curated 4 station-name aliases after the direction-suffix regex.**
  A pairwise physical-distance check of the selected stations found four
  pairs under 200 ft apart that the regex could not merge because
  different lines' trips named the same platform inconsistently ("Van Ness
  Station" vs "Metro Van Ness Station", "Church St & Market St" vs "Metro
  Church Station", "Forest Hill Station" vs "Metro Forest Hill Station",
  "King St & 4th St" vs "4th St & King St"). 53 stations before, 49 after.
- **Used the mirror `muni-gtfs.apps.sfmta.com` for the GTFS feed.**
  `gtfs.sfmta.com` timed out at TCP connect from this environment (other
  hosts fine, DNS resolved); the mirror is linked from sfmta.com's own GTFS
  page.
- **Used this project's own six-colour line palette, not SFMTA's.**
  SFMTA's map colours have changed across revisions and some lines
  currently share a colour to signal combined service, which defeats a map
  needing six distinct lines; the palette also stays clear of the
  blue/orange/green business-category colours.
- **Centered the default map view on the station centroid at zoom 13**
  (37.7509, -122.4414) rather than the city's geographic centre; the
  city's compact diagonal shape left too much open water at zoom 12.

### 2026-09-18 - San Diego (first city) and the app

- **Ruled out Denver, then built San Diego first.** See the city-selection
  entries below for why; San Diego ranked easiest of the verified cities.
- **Added San Diego: 59,684 rows -> 43,563 in-city -> 12,988 storefront ->
  12,886 with valid coordinates (0 dropped on bounds, 0 duplicates);
  47 stations.** Source: City of San Diego Business Tax Certificates
  (`seshat.datasd.org`, active file). Pre-geocoded (`lat`/`lng`, 98.4%
  populated), so no geocoding step.
- **Filtered Trolley stations to city limits with a real boundary polygon
  (SANDAG `Municipal_Boundaries.geojson`), not a hand-curated name list.**
  63 distinct station names collapsed to 47 in San Diego, 16 outside
  (El Cajon, La Mesa, Lemon Grove, Santee, National City, Chula Vista).
  Several were not guessable by name - 24th Street and 8th Street Stations
  are in National City; Palm Avenue and Beyer Blvd are in San Diego.
  One alias was needed ("12th & Imperial Station (Bayside)" merged into
  its twin); the MTG Event Line shuttle was excluded as non-regular
  service.
- **Matched businesses with an exact `address_city == "SAN DIEGO"`.**
  Known limitation: neighbourhoods recorded under their own name (La Jolla
  foremost) are undercounted. Kept exact-match for consistency with the
  prototype's approach; recorded as open work in `PLAN.md`.
- **Made permanent on-map line labels AND legend entries a standing
  requirement for every transit line in every city.** Labels use the
  line's real public name, verified rather than taken from GTFS
  (`route_short_name` "Blue" vs the real "Blue Line"). Placement is
  automatic (perpendicular offset from the line's shape midpoint) with a
  per-line override; the legend entry exists so line identification
  survives an imperfectly placed label. San Diego's Silver Line needed a
  larger offset (0.016 vs 0.006 deg) to clear the dense downtown cluster.
  In-ring plotting: 2,971 of 12,886 businesses fall within a 0.6 mi ring
  and are plotted by default.
- **Embedded maps as pre-rendered static HTML (`st.components.v1.html`),
  not `streamlit-folium`.** `streamlit-folium` would put folium into the
  deployed runtime, which the lean/heavy requirements split exists to
  avoid. This resolved a question that had been open since the start.
  The Overview picker uses Streamlit's native `st.map` plus `st.page_link`
  buttons - one picker feel with no folium and no bidirectional component.
- **Gave the app a UI scheme deliberately different from the prototype's:**
  light base, teal accent `#0d9488` (`.streamlit/config.toml`), Space
  Grotesk (`app/components.py`), versus the prototype's dark theme, default
  red accent and Inter - so the two portfolio projects read as distinct
  products.
- **Decided the project is never named after a city.** "Expanded Heatmap"
  (a placeholder until a proper name is chosen) is the only macro-level
  identity; a city name labels only that city's own page. Matches the
  hybrid architecture: an area-selector page, then per-city renders.
- **Created the `add-city` skill and a root `CLAUDE.md`** from what actually
  worked for San Diego, so later cities follow a process rather than
  re-deriving it.

### 2026-09-18 - City selection, live verification, taxonomy plurality

- **Researched the 25 largest US cities against three criteria and
  shortlisted 10.** Criteria: expansive rail transit; public transit open
  data; public business-license data with a classification field plus
  address/geometry. Initial ranking: New York, Chicago, Los Angeles,
  Philadelphia, San Diego, San Francisco, San Jose, Denver, Boston,
  Washington D.C. Seattle - the prototype's city and the only one with a
  known-good pipeline - was swapped out for D.C. by explicit decision, and
  D.C. placed 10th; Seattle's code patterns carry over but its dataset does
  not. Full rationale and per-city findings: `docs/city_shortlist.md`.
- **Ruled out Denver on live-verified data, not the shortlist pass.** Its
  "Active Business Licenses" dataset (checked on both the Denver ArcGIS hub
  and the Colorado Information Marketplace mirror) has no address, no
  classification and no geometry - only `License_Num, License_Type,
  License_Sub_Type, License_Status, Entity_Name, Trade_Name,
  Expiration_Date`. All 347 datasets in Denver's catalog were searched for
  an alternative; none qualified. A "Business License Data Explorer" the
  first-pass research cited turned out to be Anaheim's (owner account and
  map extent), not Denver's. **Lesson made a rule (CLAUDE.md, `add-city`
  Step 0): live-verify a city's actual field schema before any pipeline
  work; dataset titles and search summaries are not evidence.**
- **Re-verified all 10 shortlisted cities live (schema pulls plus sample
  rows).** Against the original NAICS-required criterion: pass - Los
  Angeles, San Diego, San Francisco; pass with caveats - Boston (its only
  NAICS+address dataset is a 978-row certified-vendor directory, not a
  general registry) and Washington D.C. (no NAICS, and its lat/long
  fields are truncated to whole degrees, so it needs address geocoding);
  fail on NAICS alone - New York, Chicago, Philadelphia (each has real
  geocoded license data under its own taxonomy); fail outright - San Jose
  (no bulk business-tax dataset on either official portal; the only source
  is a third-party lookup tool with no export) and Denver.
- **Dropped the requirement that a city's classification be NAICS
  ("taxonomy plurality"). Supersedes the same-day plan to use NAICS as the
  single shared national classification layer.** That plan assumed every US
  city self-reports NAICS at licensing; verification showed three of ten do
  not. Rather than disqualify real cities over a naming difference, each
  city now names a taxonomy system and a module in `pipeline/taxonomies/`
  maps it into the shared buckets (Retail / Food service / Personal
  services). This also sets up non-US cities (the EU's NACE was the
  concrete example) as one more module rather than a rewrite. The
  bucket-based design from the superseded plan survived intact - it is why
  adding taxonomies was cheap. The three local modules (`nyc_dca`,
  `chicago_license`, `phl_licensetype`) are skeletons mapping only values
  seen in sample rows; each needs a full `SELECT DISTINCT` pull before use.
  Reclassified New York, Chicago and Philadelphia from fail to pass.
- **Ranked passing cities by ease of implementation: San Diego, San
  Francisco, Los Angeles, Chicago, New York, Philadelphia; Boston and
  D.C. caveated.** Factors: taxonomy already built (NAICS) vs skeleton,
  API simplicity, geocoding completeness, size of the rail system
  (station-scope decision), Philadelphia's Carto API and WKB geometry.
  Continue down this order.

### 2026-09-18 - Project origin and architecture

- **Scope: the heatmap only, commercial density only.** Generalized from an
  earlier single-city prototype (Seattle's Link light rail). Carried over
  the heatmap page's concept and lessons; not its Findings/Methodology
  pages and not its ridership axis. Priority is map coverage and user
  functionality. Ridership and deep interpretive analysis are out of scope
  until asked.
- **Chose a hybrid map architecture: an area-selector macro page routing
  to independent per-city detail maps.** Option A (one global map with
  city checkpoints) risks a real performance ceiling - the prototype needed
  marker clustering for 11,409 points in one city, plus a custom
  cluster-icon fix and a fixed-pixel map to work around a Leaflet.heat init
  bug (Leaflet.heat issue 95: an uncaught IndexSizeError on init when the
  container size isn't resolved silently stops every later `.addTo(map)`),
  and those problems would compound across cities in one instance.
  Option B (independent maps only) is the mechanical extension but has no
  "zoom out and see everything" feel. The hybrid gives the single-map
  navigation feel without loading more than one city's business points at
  once. Each city map is its own Leaflet instance with its own bounds.
- **Kept the pipeline/app split: a heavy offline pipeline writes small
  static files; the deployed app only reads `outputs/`.** Geopandas can't
  be a runtime dependency on Streamlit Cloud. `requirements.txt` stays
  lean (streamlit, pandas, altair); geo dependencies live in
  `requirements-pipeline.txt`.
- **Per-city folders and per-city config instead of a shared registry
  loader, for now.** `data/<city>/{raw,processed}` (gitignored),
  `outputs/<city>/` (committed), `pipeline/<city>/`. A shared
  `data/registry.yaml` was deliberately not built with one, or even two,
  cities - generalize once the common shape is visible (open in `PLAN.md`).
- **Made the projected CRS a per-city value.** The prototype hardcoded UTM
  10N; a wrong zone is the degrees-vs-metres bug one level deeper. San
  Diego is EPSG:32611 (11N); San Francisco EPSG:32610 (10N), independently
  derived from longitude, not copied.
