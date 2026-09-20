# Project context

The stable briefing for this project: what it is, what's settled, how it's
built, and where things stand. Read it at the start of a session. It
describes the *current* state and is rewritten as things change; the dated
reasoning behind each decision is in [`DECISIONS.md`](../DECISIONS.md), open
work is in [`PLAN.md`](../PLAN.md), and working rules are in
[`CLAUDE.md`](../CLAUDE.md).

## The project

A multi-city map of commercial (storefront) density around rail-transit
stations. For each covered city, a station-centred heatmap shows where
retail, food-service and personal-service businesses cluster relative to
the transit lines, with toggleable distance rings, clustered per-business
pins, and every transit line drawn from real GTFS geometry with a
permanent label and legend entry. A macro-level area-selector page routes
into independent per-city maps. The audience is portfolio viewers; the
priority is map coverage and usable functionality, not written analysis.

It was generalized from an earlier single-city (Seattle) prototype. Nothing
in this repo depends on that prototype; where its lessons still apply they
are stated here.

## Read these, in order

1. [`CLAUDE.md`](../CLAUDE.md) - invariants and commands
2. this file
3. [`PLAN.md`](../PLAN.md) - what's open and what's next
4. [`DECISIONS.md`](../DECISIONS.md) - the reasoning trail and per-run baselines
5. [`city_shortlist.md`](city_shortlist.md) - which cities are viable and why
6. [`sub_transit_line_filters.md`](sub_transit_line_filters.md) - the station-thinning pattern
7. `.claude/skills/add-city/` - the process for adding a city

## Already decided - do not relitigate

Each has its rationale in `DECISIONS.md`.

- **Scope:** commercial density only. No ridership, no Findings/Methodology
  pages, no deep interpretive analysis, until asked. Flag scope additions
  rather than building them.
- **Architecture:** hybrid - an area-selector macro page, then independent
  per-city detail maps. No map instance ever holds more than one city's
  business points.
- **Pipeline/app split:** an offline pipeline writes small static files; the
  deployed app only reads `outputs/`. The app never runs the pipeline.
- **Maps are pre-rendered static HTML** embedded with
  `st.iframe()`, not `streamlit-folium`. The macro map is the one
  exception in kind: a pydeck map (bundled with Streamlit), so clicks can
  navigate without folium.
- **City viability is verified live**, against the real API/schema and
  sample rows, before any pipeline work. Titles and search summaries are
  not evidence.
- **Classification is pluggable:** NAICS or a city's own documented
  taxonomy, mapped into shared buckets. NAICS is not required.
- **Rail systems with a central corridor plus dense surface offshoots**
  use the sub-transit-line filters; uniformly sparse systems keep every
  station.
- **Every drawn transit line gets a permanent on-map label using its real
  public name AND a legend entry.**
- **Map rendering is shared** (`pipeline/map_common.py`) and never names a
  taxonomy.
- **The project is never named after a city.**
- **UI:** light theme, teal accent, Space Grotesk.
- **CRS is per-city.**

## Architecture

```
data/<city_slug>/raw/         downloads, gitignored, regenerable
data/<city_slug>/processed/   pipeline intermediates, gitignored
outputs/<city_slug>/          committed: heatmap.html (+ audit CSVs)
pipeline/
  map_common.py               shared rendering: render_heatmap() and helpers
  drift_check.py              re-run pipelines, diff outputs/ against git HEAD
  taxonomies/                 classification -> shared buckets, one module each
  <city_slug>/config.py       paths, CRS, rings, station scope, taxonomy name
  <city_slug>/step1_stations.py         GTFS -> station list (city-limits filtered)
  <city_slug>/step2_clean_businesses.py raw export -> clean, filtered CSV
  <city_slug>/step3_map.py              thin: centre, line specs, calls render_heatmap
  census_geocoder.py          shared: Census bulk geocoder with a content-hash cache
                              (for cities whose data lacks usable coordinates)
app/
  Overview_&_Introduction.py  macro page: clickable map of every city
  cities.py                   the app's city list (map, fallback list, switchers)
  pages/N_<City>_Heatmap.py   one embedded map per city
  components.py               shared styling (font)
docs/                         this file, city research, filter pattern
```

**Taxonomies.** `pipeline/taxonomies/__init__.py` defines the shared
buckets (Retail, Food service, Personal services, each with a colour) and
a registry of taxonomy modules. Each module exposes `classify(row)`,
`FIELD_LABEL`, `VALUE_COLUMN` and `legend_label(bucket)`. Step 2 filters
with `filter_to_storefront()` and the map groups, labels and builds its
legend through the module, so adding a taxonomy - including a non-US one
such as NACE - means adding one module. `naics.py` is complete. The three
local modules `nyc_dca` and `phl_licensetype` are **skeletons**: they map
only values seen in sample rows and need a full `SELECT DISTINCT` pull of the
city's classification field before use. `chicago_license` is complete; it is
the model for a taxonomy that classifies some values by a second field
(`EXTRA_COLUMNS`).

**Steps.** Each city has steps 1 (stations), 2 (clean businesses) and a
final map step. A city that needs geocoding inserts a step and renumbers;
nothing hardcodes the numbers. San Diego and San Francisco ship
pre-geocoded, so their map is step 3; Los Angeles needs a Census-geocoding
step 3, so its map is step 4.

**Config is per-city, generated from a template.** Each city has its own
`config.py`; `scripts/scaffold_city.py` (the `scaffold-city` skill) writes the
shared shape of a new one. A runtime `data/registry.yaml` loader is not built:
the scaffold covers what it was for (see `DECISIONS.md`).

## Current state

Cities built and running end to end (pipeline, map, app page):

- **San Diego** - MTS Trolley (Blue, Orange, Green, Copper, Silver). NAICS.
  Stations spatially filtered to city limits using a regional boundary
  layer. Data ships pre-geocoded.
- **San Francisco** - Muni Metro (J, K, L, M, N, T). NAICS. Stations
  thinned with the sub-transit-line filters; cut stations are documented in
  `outputs/san_francisco/excluded_stations.csv`. Data ships pre-geocoded.
- **Los Angeles** - Metro Rail (A, B, C, D, E, K Lines), only the stations
  inside the City of LA (the lines serve 23 other places). NAICS.
  Businesses are identified by the registry's own council-district field,
  not its postal-community `city` field. About 9% of rows had corrupt
  coordinates, concentrated in recent registrations; they are recovered by
  Census geocoding rather than dropped. Line colours are Metro's own.
- **Chicago** - CTA 'L' (Red, Blue, Brown, Green, Orange, Pink, Purple), only
  the stations inside the City of Chicago (Yellow is left out: its only
  in-city station is Howard); Metra is not included. First city on a local
  taxonomy (`chicago_license`, not NAICS): several license types are
  classified by their business activity, and a site holding several licenses
  counts once, the primary license deciding. The source is a license-term
  history, filtered to currently active licenses. Data ships pre-geocoded
  with valid coordinates, so its map is step 3.

Next by ease ranking: New York and Philadelphia; Boston and
Washington D.C. carry caveats. See `city_shortlist.md` and
`PLAN.md`. Row counts, station counts and per-run figures are in
`DECISIONS.md`.

**Navigation.** The Overview is the macro map: a pydeck map (pydeck ships
with Streamlit; no folium) with a labelled marker per city, where clicking a
marker opens that city's page (`st.switch_page`), plus a plain link list as a
fallback. In the map-only pilot (`MAP_ONLY_NAV` in `app/cities.py`) the sidebar page
list and the city switcher are hidden, and each city map has an "All cities"
button back to the macro map; with the flag off, every city page has a switcher
row to jump to another city or back to the map (see
`docs/navigation_sidebar_and_city_links.md`). The city list lives in `app/cities.py`.

Not built yet: a shared pipeline-side city registry, and deployment.

## Standing requirements for a city's map

- Transit lines drawn from real GTFS `shapes.txt` geometry, never straight
  lines between stations.
- Each line: permanent label with its real public name (verify it - a GTFS
  short name is not automatically what riders call it) plus a legend
  swatch. Labels sit at each line's tail end (the end farthest from other
  lines) and disperse along their lines if several would collide; force a
  line's end with `"start"`/`"end"` in its spec only if a rendered map shows
  it landing badly. The legend is collapsible (`<details>`).
- Stations always on, not toggleable; rings, heat layers and category pins
  toggleable. The whole-city heat layer is an opt-in; the default view is
  businesses within a ring.
- Line labels sit above the pins (a big cluster must not hide a label) and,
  for lines that run far beyond the city, are anchored on the in-city
  stretch (`label_focus`).
- Pin clusters use the scaled cluster icon; pin layers are wrapped in a
  `FeatureGroup` for `show`; free text in tooltips is HTML-escaped.
- Default view fitted automatically to the stations and every label; fixed
  pixel size.

## Lessons that apply to every city

- **CRS is per-city.** Buffer and measure only in the city's own projected
  CRS (metres), never EPSG:4326; project back for display. Look up the UTM
  zone from the city's longitude (San Diego 11N, San Francisco 10N; Chicago
  16N and NYC 18N; non-US cities may need a national system, e.g. UK
  EPSG:27700).
- **Coordinates that exist can still be wrong.** Los Angeles' registry had
  ~9% corrupt coordinates (longitude copied from latitude, (0,0), whole-
  degree placeholders), concentrated in recent registrations. Check values,
  not just non-null-ness; recover rather than drop when the loss is large or
  biased; when a filter drops more than a few percent, find out why and
  whether the loss is uniform before accepting it. The Census bulk geocoder
  (`pipeline/census_geocoder.py`, US-only) recovered 98.9%.
- **A city field may not mean "in the city".** LA's `city` holds postal
  community names; its `council_district` field is the reliable in-city
  marker. Look for an authoritative district/boundary field, and cross-check
  with the boundary polygon.
- **Classification isn't universal.** NAICS is US-specific; each non-NAICS
  city needs its taxonomy decided explicitly. Catch-all codes (e.g. NAICS
  812990 "All Other Personal Services", 459999 "All Other Miscellaneous
  Retailers") sweep in non-storefront businesses and deserve a per-city
  hand-sample before being trusted.
- **Tile policy is a scaling risk.** OpenStreetMap's tile usage policy
  blocked a downloaded copy of an earlier version of this map (403); a live public map
  with real traffic is likelier to hit it. Decide a tile provider
  deliberately before deploying (open in `PLAN.md`).
- **Leaflet.heat needs a fixed pixel-size map.** Percentage sizing can
  raise an uncaught IndexSizeError on init that silently stops every later
  layer (Leaflet.heat issue 95). `render_heatmap` uses a fixed 1000x650
  map; keep it fixed.
- **Leaflet.markercluster's default icon is a fixed 40x40px**, which blocks
  hover on nearby individual points; the scaled icon in `map_common.py`
  fixes it.
- **`st.markdown(..., unsafe_allow_html=True)` truncates raw HTML at the
  first blank line** (a CommonMark rule); embedded multi-element HTML must
  be one unbroken string.
- **`st.dataframe` headers can't be styled** (canvas-rendered).
- **Read generated HTML with `encoding="utf-8"`.** Folium saves UTF-8; on
  Windows `Path.read_text()` defaults to the OS codepage and mangles
  multi-byte characters.
- **Verify against the lean dependency set** (`.venv-lean`), not the full
  environment.

## Working preferences

- Draft interpretive or user-facing prose in chat before writing it to a
  file, when it's more than a one-line tweak.
- Record judgment calls in `DECISIONS.md` as they're made.
- Give recommendations without acting when asked to; act when asked to.
