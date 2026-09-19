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

- [~] **Next city: Chicago** (ease rank 4). Follow `add-city` from Step 0.
  Its taxonomy (`chicago_license`) is a skeleton: pull the full
  `SELECT DISTINCT license_description` (and `business_activity`) from
  Socrata `r5kz-chrr` and fill in the mapping, with a hand-sample of
  catch-all categories, before building the city. CTA 'L' is large (145
  stations) - check whether it has the central-plus-offshoot shape. Los
  Angeles' lessons apply: check what the city field holds, check
  coordinates for corruption (not just null-ness), and investigate any
  filter that drops more than a few percent.

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
- [ ] San Jose and Denver: ruled out (no usable dataset). Revisit only if a
  new source appears.

## Structure

- [ ] **Shared `data/registry.yaml` and per-city config loader.** Deferred
  until more than two cities show the common shape (rule of three).
- [ ] Fill in the three local taxonomy skeletons before any of those cities
  is built (each needs a full `SELECT DISTINCT` of its classification
  field, plus a hand-sample of catch-all categories).

## Before deploying

- [ ] **Tile provider decision** - OpenStreetMap's usage policy is a risk
  for a live public map. The per-city maps use OSM raster tiles; the macro
  map uses Carto's public vector basemap. Decide both together.
- [ ] **Streamlit Cloud main-file path** - fixed at app creation and not
  editable afterward, so settle the entry-point filename first.
- [ ] **Project name** - "Expanded Heatmap" is a placeholder.
- [ ] `README.md` (none yet).

## Data quality follow-ups

- [ ] San Diego: add an `excluded_stations.csv` audit file (16 stations in
  other cities), as San Francisco and Los Angeles have.
- [ ] Los Angeles map size (5.8 MB vs 2.6 MB for San Francisco): decide
  whether to shrink it (e.g. thin the whole-city heat layer, which holds all
  ~101k points) before deploying.
- [ ] Los Angeles: ~9% of registry rows have no NAICS code; consider whether
  the caveat needs to be visible on the city page.

- [ ] San Diego: exact `address_city == "SAN DIEGO"` undercounts
  neighbourhoods recorded under their own name (La Jolla foremost); decide
  whether to include them.
- [ ] San Francisco: only ~37% of rows carry a NAICS code; consider whether
  the caveat needs to be visible on the city page.
- [ ] Catch-all classification codes (NAICS 812990, 459999, 812930) need a
  per-city hand-sample; not yet done for either built city.

## Later / maybe

- [ ] Macro map at scale: with ~10+ cities, consider grouping nearby cities
  (markers will overlap at the fitted zoom), and showing each city's mapped
  extent or a one-line summary in the tooltip.

- [ ] Non-US cities (NACE for the EU, national CRS such as EPSG:27700 for the
  UK) - one taxonomy module and a per-city CRS each.
- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
