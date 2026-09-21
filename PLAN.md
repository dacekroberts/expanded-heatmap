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

- [ ] New York - needs `nyc_dca` filled (Socrata `w7w3-xahh`,
  `business_category`); the largest rail system, so station scope is the
  biggest decision.
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

- [ ] Fill in the two remaining local taxonomy skeletons (`nyc_dca`,
  `phl_licensetype`) before those cities are built (each needs a full
  `SELECT DISTINCT` of its classification field, plus a hand-sample of
  catch-all categories). Chicago's `chicago_license` is the model.

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
- [ ] **Surface `docs/excluded_categories.md` in the app** (a page, or a link
  from each city page). It is written to be published as-is; right now it is
  only in the repository. Also decide whether each city page should name its own
  exclusions.
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
