# Plan

Open work only. Completed work and the reasoning behind it live in
[`DECISIONS.md`](DECISIONS.md); the settled state is in
[`docs/project_context.md`](docs/project_context.md).

Rules that make the rest work:

- **Commit after every green step.** A commit is the baseline
  `pipeline/drift_check.py` diffs against.
- **Log every judgment call in `DECISIONS.md` as it's made** (see the
  `decisions-entry` skill).
- **Live-verify a city's data before building it** (`add-city` Step 0).
- **Run `python pipeline/drift_check.py` after any pipeline change.**

Legend: `[ ]` open, `[x]` done (a done item stays only until its
`DECISIONS.md` entry exists), `[~]` in progress.

---

## Now

- [ ] **Next city** - pick from the list below. Start with the `add-city`
  Step 0, then `scripts/scaffold_city.py` (the `scaffold-city` skill). That
  build is also the first real test of the scaffold: record in `DECISIONS.md`
  whether it saved effort (estimated at about 10%) and fix any template that
  needed rewriting.

- [~] **Evaluate the map-only navigation pilot** (started 2026-09-20; see
  `DECISIONS.md` and `docs/navigation_sidebar_and_city_links.md`). The
  Overview's fallback link list is kept (decided 2026-09-21). The hop-between-cities
  gap is closed with a "Cities" dropdown on each city map (2026-09-21). Open: the
  final go/no-go. To revert, set `MAP_ONLY_NAV = False` in
  `app/cities.py`.
- [ ] **Dark Mode, remaining part: the surrounding Streamlit page** (background,
  text, switcher, sidebar). City maps and the macro map are done and share one
  stored choice (see `DECISIONS.md`). Deferred while a custom theme for the page
  is considered; a page-level toggle would also need to follow that stored
  choice. Notes: `docs/dark_mode_handoff.md`.

## Next cities, in ease order

- [x] **New York - built 2026-09-21.** The premise recorded here was wrong:
  DCWP `w7w3-xahh` is a regulated-activity licence list, not a business
  registry (no restaurants, grocery, clothing or salons in it at all), and New
  York has no general business licence. Coverage is assembled from four
  registries instead, the `nyc_dca` skeleton was retired, and 29 subway
  services are drawn as the 11 trunk lines MTA itself signs. See `DECISIONS.md`.
  Open follow-ups:
  - Its map is **10.3 MB**, against 3.5 MB for Los Angeles - 44,361 pins,
    because dense stations put 71% of businesses inside a ring (Los Angeles:
    24%). Measured levers: rounding coordinates to 5 dp saves 1.4 MB and loses
    nothing (Folium emits 17 significant digits for a 5-pixel dot, and it would
    re-baseline all five cities' committed outputs); indexing repeated station
    and ring strings saves ~1.2 MB; dropping the opt-in all-city heat layer
    saves 2.0 MB. Decide before the public deploy.
  - Retail is less complete here than elsewhere (a clothing shop needs no
    licence from any of the four registries). Said plainly on the city page;
    worth repeating in `docs/excluded_categories.md`.
- [ ] Philadelphia - needs `phl_licensetype` filled; data source is a Carto
  SQL API with WKB geometry, so it needs extra parsing.
- [ ] Boston - real NAICS+address but only a 978-row certified-vendor
  directory; decide whether that is enough data to be worth mapping.
- [ ] Washington D.C. - `LATITUDE`/`LONGITUDE` are truncated to whole
  degrees; use `pipeline/census_geocoder.py` on `PREMISEADDRESS` (or the
  state-plane `X_COORDINATE`/`Y_COORDINATE` fields), and add a taxonomy
  module.
- [ ] Dallas (marginal, unranked) - Socrata `9qet-qt9e` has `land_use` and
  coordinates, but the data ends 2022-11-15 and covers only 2018-2022
  certificates, so the city page must say it shows new occupancies. Needs a
  new taxonomy module. First check the Commercial Permits Activity Dashboard
  (`ync5-xnfn`) for something fresher.
- [ ] San Jose, Denver, Austin, Charlotte, Fort Worth: ruled out (no usable
  dataset, or too little rail). Revisit only if a new source appears; see
  `docs/city_shortlist.md`.

## Structure

- [ ] Fill in the remaining local taxonomy skeleton (`phl_licensetype`) before
  Philadelphia is built: it needs a full `SELECT DISTINCT` of `licensetype`,
  plus a hand-sample of catch-all categories. Chicago's `chicago_license` is
  the model. (`nyc_dca` was retired rather than filled - see `DECISIONS.md`,
  2026-09-21. Check Philadelphia's registry actually covers all three buckets
  before assuming one source is enough; that assumption failed for New York.)
- [x] **Record each data source's licence and terms of use** - done
  2026-09-21 in `docs/data_sources.md`, covering all 8 registries, all 5 GTFS
  feeds, the boundary layers and the basemap. Permissive terms were NOT the
  default they were expected to be. What came out of it:
  - [ ] **Display the required notices before publishing.** Chicago, SFMTA and
    LA Metro each require specific text; OSM's is already satisfied. Exact
    wording is in that file under "Notices this project MUST display when
    published". Part of the same app job as surfacing the two doc pages, and
    it **blocks the public deploy** - publishing without them breaches terms
    this project has now read.
  - [ ] **Establish NYC Open Data's reuse position** - the one source whose
    terms could not be established. It declares no licence and the general
    nyc.gov terms reserve all rights. Needs a direct enquiry to NYC Open Data,
    and it covers three datasets including New York's food-service backbone.
  - [ ] **Decide whether LA Metro's GTFS terms permit what this project does.**
    They forbid modifying the "Transport Information"; the project redraws its
    rail alignment from `shapes.txt`. Tightest licence in the project.
  - [ ] **Decide whether CTA's purpose limitation fits.** Its licence is for
    assisting riders or promoting public transport; this is an analysis and
    portfolio map.
- [ ] **Find San Francisco's boundary-layer endpoint.** It is recorded nowhere,
  and the file is gitignored, so that city cannot currently be rebuilt from
  scratch (surfaced while writing `docs/data_sources.md`).

## Before deploying

- [ ] **Tile provider decision** - OpenStreetMap's usage policy is a risk
  for a live public map. The per-city maps use OSM raster tiles; the macro
  map uses Carto's public vector basemap. Decide both together.
- [ ] **Streamlit Cloud main-file path** - fixed at app creation and not
  editable afterward, so settle the entry-point filename first.
- [ ] **Project name** - "Expanded Heatmap" is a placeholder.
- [ ] `README.md`: first draft written; revise before deploying (add the
  deployed URL, a licence, and the final project name).

## Data quality follow-ups

- [x] Los Angeles map size: **3.5 MB** after the 2026-09-21 exclusions (was
  5.8), against 2.4 MB for San Francisco. Largely resolved; revisit only if a
  deploy shows it is still slow.
- [ ] Los Angeles: ~9% of registry rows have no NAICS code; consider whether
  the caveat needs to be visible on the city page.

- [ ] San Diego: exact `address_city == "SAN DIEGO"` undercounts
  neighbourhoods recorded under their own name (La Jolla foremost); decide
  whether to include them.
- [ ] San Francisco: only ~37% of rows carry a NAICS code; consider whether
  the caveat needs to be visible on the city page.
- [ ] **Surface `docs/excluded_categories.md` AND `docs/data_sources.md` in the
  app**, together (a page each, or one "About the data" section, linked from
  every city page). Deliberately paired and deferred as one job (2026-09-21):
  both are external necessities for a live site rather than development work,
  both are already written to be published as-is, and surfacing the exclusions
  without the provenance would be half an answer. **Blocks the public deploy:**
  the legends were left broad, so "Retail - NAICS Code: 44/45" overstates what
  the maps contain until the exclusions page is reachable from them.
- [ ] **Phone-width city pages.** Found by `deploy-verify` 2026-09-21: at 375px
  the iframe shows ~343px of the 1000px map, so most line labels start outside
  the visible area (10 of 11 in New York, 7 of 7 in Chicago) and the reader has
  to scroll inside the iframe. Affects every city. Same root cause as the
  legend overlap - the map's fixed 1000px layout, which exists to dodge the
  Leaflet.heat `IndexSizeError` - but unlike the legend this needs a deliberate
  mobile approach, not a breakpoint. Options not yet weighed: a narrower
  phone-specific render, a scroll hint, or accepting it and saying so. **Blocks the public deploy:** the legends were deliberately left
  broad (2026-09-21), so "Retail - NAICS Code: 44/45" overstates what the map
  now contains until this page is reachable from it.
- [x] Catch-all and non-storefront classifications: swept 2026-09-21 and
  resolved. Excluded everywhere: NAICS `454` (nonstore retailers) and `81293`
  (parking). Excluded per city: 812990 in Los Angeles and in San Francisco (for
  different reasons - see `DECISIONS.md`). Kept: 459999 (~70% plausible
  storefronts). San Diego left in, with its measurement limit recorded. All
  listed in `docs/excluded_categories.md`. Remaining open questions:
  - A residual ~850 rows in Los Angeles and ~201 in San Francisco carry a
    person-like name at a residential address, spread across ordinary storefront
    categories. Probably sole traders named after themselves (legitimate), but
    unverified row by row.
  - San Diego has no usable residence signal in its address text; its
    `ownership_type` (1,298 SOLE of 3,117 mapped) is the better proxy if this is
    revisited.
- [ ] **Run `python scripts/check_personal_exposure.py` before publishing any
  city**, and after any change to a city's step 2 or taxonomy. It is a
  pre-publish gate in `CLAUDE.md` and `add-city` Step 7.

## Later / maybe

- [ ] Macro map at scale: with ~10+ cities, consider grouping nearby cities
  (markers already touch at phone width: Los Angeles and San Diego), and showing each city's mapped
  extent or a one-line summary in the tooltip.

- [ ] Non-US cities (NACE for the EU, national CRS such as EPSG:27700 for the
  UK) - one taxonomy module and a per-city CRS each.
- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
