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

- [ ] **Next city: Chicago** (ease rank 4). Step 0 probe done 2026-09-19
  (see `DECISIONS.md`); build it after the weekly reset (Sunday
  2026-09-20 18:59 UTC), following `add-city` from Step 1. Its taxonomy
  (`chicago_license`) is partly done: the two catch-alls ("Limited
  Business License", "Regulated Business License", about 39% of active rows)
  are classified by `business_activity`. Still to map: the other ~148
  `license_description` values (Retail Food Establishment, Tavern, Tobacco,
  Package Goods and so on), with a hand-sample. Filter the
  1.2M-row history to status `AAI` and unexpired licenses (the expiry field
  has junk dates), then dedupe by account and site. CTA 'L' is large (145
  stations) - check its shape from the GTFS (stop spacing per line, stations
  inside the boundary; expected uniformly sparse, so no SF-style spacing
  filter). **Decided: CTA only for the first build** (one agency's rail
  system per city, as in the built cities); Metra
  (`schedules.metrarail.com/gtfs/schedule.zip`) is a possible later
  addition. Chopping-block order if the map is too much: Yellow and possibly
  Purple (drop a line with essentially no in-city stations), then suburban
  stops (the boundary filter removes them); the core six lines stay.
  Still to check, per the Los Angeles lessons: coordinate corruption (not
  just nulls; about 8% are null) and any in-city rows with another `city`
  value.

  **Start-up checklist for the Chicago build** (Socrata `r5kz-chrr` on
  `data.cityofchicago.org`; active filter used so far:
  `license_status='AAI' AND expiration_date >= <today> AND city='CHICAGO' AND
  latitude IS NOT NULL`):
  1. Pull active row counts per `license_description` (about 150 values,
     one grouped query). Map the top ~30 by hand and default the tail to
     excluded (the top 25 hold about 92% of active rows).
  2. Sample `business_activity` for "Retail Food Establishment" (11,150
     rows, another catch-all): split Food service (dining, food preparation)
     from Retail (selling packaged food and groceries). Add it to
     `chicago_license.py` alongside the two done catch-alls.
  3. Decide the adjunct-license rule (Consumption on Premises, Outdoor Patio,
     Tobacco, Package Goods): the primary license sets the bucket, adjuncts
     count only where the site has no primary license; dedupe by account and
     site after classifying. Open calls: Commercial Garage (589), Motor
     Vehicle Services (1,537), Shared Kitchen User (540).
  4. Coordinate quality: bounding-box test on latitude/longitude (LA had
     corrupt coordinates hidden behind non-null values), and check for
     in-city rows carrying another `city` value.
  5. Download the CTA GTFS (`transitchicago.com/downloads/sch_data/
     google_transit.zip`, 68.7 MB) and the city boundary (Socrata
     "Boundaries - City - Map", `ewy2-6yfk`). Compute stop spacing per line
     and stations inside the boundary; confirm the expected uniformly sparse
     shape, then apply the chopping-block order above if needed.
  6. Then follow `add-city` from Step 1 (config, step files, map, app page),
     run `python pipeline/drift_check.py`, verify with `deploy-verify`,
     and log each judgment call in `DECISIONS.md`.

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

- [ ] **Scaffold a new city's `config.py`, map script and app wiring** (the
  `cities.py` entry, page file and docs stubs), and with it the shared
  `data/registry.yaml` / config loader. The rule of three is met (three
  cities), but build it after the first non-NAICS city (Chicago), so the
  shared fields are chosen from a case that differs from the three built
  ones. Scope: not `step1_stations.py` or `step2_clean_businesses.py`, which
  differ per city and hold most of the per-city effort. Expected saving is
  modest (roughly 10% of a city's cost, an estimate).
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
