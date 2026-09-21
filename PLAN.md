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
- [ ] **Midnight slate theme: the Streamlit page AND the map palette, as one
  change.** No longer deferred - the blocker was the assumption that an
  explicit theme forces the site dark-only, and separate
  `[theme.light]`/`[theme.dark]` blocks keep the toggle (tested). Decided
  2026-09-21 to stay on Streamlit rather than go static; see `DECISIONS.md` for
  why, and for the measurement showing a map-chrome reskin alone is not worth
  doing (it is ~15% of a city page's pixels; the tiles are filtered and the
  data colours are fixed, so no `--dm-*` variable touches them).
  **Everything needed to build it - palette, both value sets, the traps, the
  verification checklist - is in `docs/theming.md`.**
  - [x] `.streamlit/config.toml` with both light and dark blocks; the chooser
    Streamlit had been suppressing is back (System / Light / Dark).
  - [x] The map's `--dm-*` values swapped to slate, the macro map's duplicate
    copy removed, and everything sourced from the new `pipeline/theme.py`.
    `scripts/check_theme_sync.py` guards the one unavoidable TOML duplicate.
  - [x] **Two theme controls reconciled (option A, 2026-09-21).** With no
    stored choice a map follows the page it is embedded in; an explicit click
    wins from then on; a standalone map follows the OS preference. Verified
    all three: ambient-dark page gives a dark map (`storedTheme: null`), a
    click stores `light`, and that survives a reload on a dark page. Options B
    (our button drives the page, overriding Streamlit's widget CSS by hand)
    and C (remove the in-map button when embedded) were rejected - see
    `DECISIONS.md`.
  - [ ] Sweep the remaining hardcoded colours in `app/` now that a dark page
    exists: `Overview_&_Introduction.py` still has literal `white` and
    `#1c2b2a` (lines ~90, ~139) for the macro map's markers and labels. Check
    contrast numerically against `#0B1220`, not by eye - a 1.01:1 label looks
    like empty space rather than a bug.
  - [x] Reconciled the two overlapping handoffs into `docs/theming.md`
    (2026-09-21). Both originals are in git history.

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
- [x] **Philadelphia - built 2026-09-21.** The WKB parsing this item predicted
  was never needed (the Carto SQL API evaluates `ST_X`/`ST_Y` server-side), and
  `phl_licensetype` is filled from the full 50-type pull. What it left behind:
  - Two open licence questions, both to settle before the public deploy:
    SEPTA's trademark/commercial clause, and the "City of Philadelphia
    License", which reserves all database rights while granting nothing
    explicitly. See `docs/data_sources.md`.
  - Personal services is **absent**, not thin - the only such city. Stated on
    the city page and in `docs/excluded_categories.md`.
  - Regional Rail (52 well-spaced in-city stations, no thinning needed) is the
    obvious later addition if the commuter-rail exclusion is revisited.
  - The Girard Avenue Trolley's label uses SEPTA's own `#FFD700`, which is the
    lowest-contrast of the four over the orange heat wash. Cosmetic; swap for a
    darker gold if it reads badly on a real screen.
- [ ] Boston - **re-probed 2026-09-21 and no longer ruled thin.** The 978-row
  certified-vendor directory is not the only option: `data.boston.gov` also has
  "Licensing Board Licenses", "Active Food Establishment Licenses" and
  "Annual Entertainment Licenses". Needs a proper Step 0 on those - whether
  they cover Retail and Personal services, and whether they carry coordinates.
  Expect the `multi-source-city` path.
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

- [x] ~~Fill in the remaining local taxonomy skeleton (`phl_licensetype`)~~ -
  **done 2026-09-21** from the full `SELECT DISTINCT licensetype` pull; all 50
  active types carry an explicit verdict. No taxonomy skeletons remain.
  (`nyc_dca` was retired rather than filled - see `DECISIONS.md`, 2026-09-21.)
  The check this item asked for paid off twice: New York needed four sources,
  and Philadelphia turned out to have **no source at all** for one bucket.
- [ ] **Close the residence blind spot in `check_personal_exposure.py`.** It
  detects a home only by an `APT`/`FL`/`RM`/`#` indicator, so a sole trader at
  a detached house reads as clean - which is why Philadelphia scores 0.00%.
  Two unused signals could close it: the licence's mailing address matching its
  premises address (Philadelphia has `business_mailing_address`, not currently
  downloaded), and parcel land-use via a parcel id such as `opa_account_num`.
  Worth doing before the deploy, since it applies to every city.
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
  - [x] **NYC Open Data's reuse position** - resolved 2026-09-21 from the
    primary source. Local Law 11 of 2012 "requires that data sets must be
    available without registration requirement, license requirement, or usage
    restrictions", so the absent licence field is compliance rather than an
    omission. One condition attaches (identify source, version and
    modifications when republishing), which this project already satisfies in
    substance via `data_sources.md` and `excluded_categories.md`.
  - [x] **LA Metro's "modification" clause and CTA's purpose limitation** -
    both decided 2026-09-21 by the project owner; reasoning recorded in
    `docs/data_sources.md` and `DECISIONS.md`.
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
- [ ] **Carry into the mandatory `full` `deploy-verify` run before deploy:** the
  three fixes made after the 2026-09-21 scoped `map-chrome` run (legend
  breakpoint dead on a wide load, container ~15px short, fit bounds excluding
  label anchors) are verified by screenshot on four cities but not by an agent
  pass. Confirmed 2026-09-21 to batch them into that run rather than spend
  another scoped one - which is the batching the scope policy encourages.
- [x] **Phone-width city pages** - largely fixed 2026-09-21. The map keeps its
  fixed 1000px layout for initialisation (which is what dodges the Leaflet.heat
  `IndexSizeError`) and is resized to the frame immediately afterwards, then
  re-fitted to the station bounds. At 375px: New York went from 1 of 11 line
  labels visible to **9 of 11 fully visible, 0 off-screen**, Chicago from 0 of 7
  to 6 of 7, and the horizontal scroll inside the iframe is gone. Desktop is
  unchanged (11 of 11, original view). What remains:
  - [ ] **Label placement is still computed for a 1000x650 canvas**, so at phone
    width labels can crowd each other and the cluster badges, and one or two
    clip at an edge (New York: "Lexington Av (4/5/6)" right, "Staten Island
    Railway" left). Laying them out correctly for a phone needs a **second
    render at phone dimensions** - a per-city phone HTML plus viewport
    selection in the page. That roughly doubles `outputs/` and render time, so
    it is worth doing only if phone traffic matters. Not started. **Blocks the public deploy:** the legends were deliberately left
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
