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
