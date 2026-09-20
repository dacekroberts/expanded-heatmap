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

- [~] **Chicago is built** (2026-09-20; see `DECISIONS.md`). Left: verify the
  macro map and the Chicago page with `deploy-verify`, then the post-commit
  `python pipeline/drift_check.py chicago`. Delete this item once both pass.
- [ ] **Next (requested): the city-scaffolding skill/script**, now that
  Chicago, the first local-taxonomy city, exists. It scaffolds a new city's
  `config.py`, map script, app page and `cities.py` entry, and docs stubs, and
  must account for custom taxonomies: what Chicago showed to be
  taxonomy-specific rather than universal is `EXTRA_COLUMNS` (a second field
  that classifies some values), activity-classified license types, a
  per-site license-priority list to dedupe multi-license sites
  (`LICENSE_PRIORITY`), a dated raw snapshot (`AS_OF_DATE`), station scope
  from GTFS parent stations (one boundary layer that holds only the city, so
  excluded stations cannot be named by suburb), and a per-city
  `RAW_CLASSIFICATION_COLUMN` that may already equal the taxonomy's
  `VALUE_COLUMN`. Scope stays config, map script and app wiring, not steps 1
  and 2 (they differ per city). Decide where it lives (a script, or an
  extension of the `add-city` skill), and fold in the shared
  `data/registry.yaml` question. Expected saving is modest (roughly 10% of a
  city's cost, an estimate).

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
