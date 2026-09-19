# Decisions log

Every judgment call, recorded with the numbers that were true when it was
made. **Append-only**: a superseded decision gets a new entry that says what
changed and why - the old entry stays. `docs/project_context.md` describes
the *current* state and is rewritten as things change; this file is the
trail behind it. Format and voice: see the `decisions-entry` skill (neutral
past tense; entries were reconstructed from session context).

Newest first. All dates below are from the project's first working day,
2026-09-18, split by phase.

---

## Changes

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
