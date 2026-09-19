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

- [~] **Next city: Los Angeles** (ease rank 3). NAICS-based; Socrata
  `data.lacity.org` id `6rrh-rzua` (`naics`, `street_address`,
  `location_1`). Live-verify again first. Rail is larger (Metro heavy +
  light, ~110 stations): check whether it has the central-corridor plus
  surface-offshoot shape before choosing between "keep every station" and
  the sub-transit-line filters, and measure how close downtown stations
  sit relative to the 0.6 mi outer ring.

## Next cities, in ease order

- [ ] Chicago - needs `chicago_license` filled from a full distinct-value
  pull of `license_description` (Socrata `r5kz-chrr`); CTA 'L' is large.
- [ ] New York - needs `nyc_dca` filled (Socrata `w7w3-xahh`,
  `business_category`); the largest rail system, so station scope is the
  biggest decision.
- [ ] Philadelphia - needs `phl_licensetype` filled; data source is a Carto
  SQL API with WKB geometry, so it needs extra parsing.
- [ ] Boston - real NAICS+address but only a 978-row certified-vendor
  directory; decide whether that is enough data to be worth mapping.
- [ ] Washington D.C. - `LATITUDE`/`LONGITUDE` are truncated to whole
  degrees; needs address geocoding or the state-plane `X_COORDINATE`/
  `Y_COORDINATE` fields, and a taxonomy module.
- [ ] San Jose and Denver: ruled out (no usable dataset). Revisit only if a
  new source appears.

## Structure

- [ ] **Area-selector macro map.** The intended macro level is an area
  selector followed by per-city renders. Two cities now exist; the current
  Overview is a plain `st.map` marker view with page links. Build the real
  selector once the user confirms scope (must not put folium in the
  deployed runtime - see `DECISIONS.md`).
- [ ] **Shared `data/registry.yaml` and per-city config loader.** Deferred
  until more than two cities show the common shape (rule of three).
- [ ] Fill in the three local taxonomy skeletons before any of those cities
  is built (each needs a full `SELECT DISTINCT` of its classification
  field, plus a hand-sample of catch-all categories).

## Before deploying

- [ ] **Tile provider decision** - OpenStreetMap's usage policy is a risk
  for a live public map.
- [ ] **Streamlit Cloud main-file path** - fixed at app creation and not
  editable afterward, so settle the entry-point filename first.
- [ ] **Project name** - "Expanded Heatmap" is a placeholder.
- [ ] `README.md` (none yet).

## Data quality follow-ups

- [ ] San Diego: exact `address_city == "SAN DIEGO"` undercounts
  neighbourhoods recorded under their own name (La Jolla foremost); decide
  whether to include them.
- [ ] San Francisco: only ~37% of rows carry a NAICS code; consider whether
  the caveat needs to be visible on the city page.
- [ ] Catch-all classification codes (NAICS 812990, 459999, 812930) need a
  per-city hand-sample; not yet done for either built city.

## Later / maybe

- [ ] Non-US cities (NACE for the EU, national CRS such as EPSG:27700 for the
  UK) - one taxonomy module and a per-city CRS each.
- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
