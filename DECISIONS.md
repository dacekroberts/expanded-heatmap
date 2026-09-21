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
