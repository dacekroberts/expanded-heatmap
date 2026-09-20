---
name: add-city
description: Add a new city to the expanded-heatmap project - live-verify its real data sources, scaffold its pipeline, build its transit/business heatmap, and wire it into the Streamlit app. Use whenever the task is "add city X" or "build out city X" for this project, not for edits to an already-built city.
---

# Adding a city to expanded-heatmap

Distilled from the three cities actually built (San Diego, San Francisco, Los
Angeles) - not a hypothetical plan. Every step either caught a real problem or is a
design decision already made (see `docs/project_context.md`; the reasoning
trail is in `DECISIONS.md`). If this is a fresh session, read those, plus
`docs/city_shortlist.md` and `PLAN.md`, first.

## Step 0 - Live-verify data BEFORE writing any code

**The step that matters most.** Denver and San Jose both looked viable from
search summaries and dataset titles, and both had no usable data on direct
schema verification. Do this for every candidate before scaffolding:

1. **Business data.** Find the real open-data portal and pull the *live*
   schema, not a description page. Socrata: `curl -s "<domain>/api/views/<id>.json"`
   for columns, then `<domain>/resource/<id>.json?$limit=3` for sample rows.
   ArcGIS FeatureServer: `<service-url>?f=json` for fields, then
   `<service-url>/query?where=1=1&outFields=*&resultRecordCount=3&f=json`.
   CKAN: `<domain>/api/3/action/package_search?q=<terms>`. Confirm, with
   real non-null sample values: (a) *some* classification field - NAICS or
   the city's own taxonomy, both fine; and (b) a street address and/or
   lat/long that actually has data, not merely a column that exists. Also
   note whether the data ships pre-geocoded (both San Diego and San
   Francisco do) and whether it has an "active" flag or an end date to
   filter on. Then check *validity*, not just population: count how many
   coordinates fall inside the city's bounds and look at the ones that
   don't. A populated field can still be corrupt - Los Angeles' registry had
   ~9% bad coordinates (longitude copied from latitude, (0,0), whole-degree
   placeholders), concentrated in recent registrations. And look at what the
   dataset's city field actually holds: LA's holds postal community names
   (Van Nuys, San Pedro...), so an exact match keeps about half the city;
   find the authoritative in-city marker (LA's `council_district`) instead.
2. **Transit data.** Find the real GTFS feed URL and confirm it downloads
   and unzips (`curl -sL <url> -o gtfs.zip`). A URL from search can still
   time out or 404 - San Francisco's official feed host timed out from this
   environment and a mirror linked from the agency's own page worked.
3. **City boundary polygon.** Find a real GIS boundary layer (a regional
   MPO/COG portal is often the source, e.g. SANDAG). Not optional: San
   Diego's Trolley serves six other cities and 16 of 63 stations were
   outside city limits, several not guessable by name. Eyeballing a station
   list is not a substitute for any system with several lines or one that
   plausibly crosses municipal borders.

Only proceed once all three are confirmed live. If a city fails, record the
real reason (cite the endpoint and response) in `docs/city_shortlist.md` and
a `DECISIONS.md` entry, and move to the next candidate.

If it passes but the build won't start right away (a usage limit, a new
session), turn what the probe found and left open into an ordered checklist
under that city's item in `PLAN.md` before stopping. Write it from the
findings, not from a template: it holds only what is specific to this city
(catch-all license types, adjunct licenses, scope decisions, checks still to
run), and points back to these steps for everything generic. Chicago's is the
model. Skip it when the probe and build happen in the same session.

## Step 1 - Taxonomy

- NAICS: nothing to build; `pipeline/taxonomies/naics.py` is complete.
- Local system: add `pipeline/taxonomies/<short_name>.py` exposing
  `classify(row) -> bucket | None`, `FIELD_LABEL`, `VALUE_COLUMN` and
  `legend_label(bucket)` (interface in `pipeline/taxonomies/__init__.py`),
  and register it in `TAXONOMY_MODULES`. Keep the honesty convention of the
  existing skeletons: map only values confirmed in Step 0's sample rows and
  mark the rest TODO - then, **before building the city**, do the full
  `SELECT DISTINCT <field>` pull and fill the mapping in properly, with a
  hand-sample of any catch-all categories.

## Step 2 - Scaffold

**Use `scripts/scaffold_city.py` (the `scaffold-city` skill)** to write the
folders below, `config.py`, the map script, the app page and the `cities.py`
entry (Steps 2, 3, 6 and 8's files) instead of creating them by hand; it also
scaffolds a new local taxonomy. Steps 4 and 5 (`step1`, `step2`) are still
copied from the nearest built city. What it produces:

```
data/<city_slug>/raw/          gitignored downloads
data/<city_slug>/processed/    gitignored intermediates
outputs/<city_slug>/           committed; the app only reads here
pipeline/<city_slug>/          config.py, step1_stations.py,
                               step2_clean_businesses.py, step3_map.py
```

Steps are 1 stations, 2 clean businesses, 3 map. If the city's data is not
pre-geocoded, insert a geocoding step and renumber the map step; nothing
hardcodes the numbers (`pipeline/drift_check.py` globs `step*.py`). Ring,
chain and ridership analyses are out of scope.

## Step 3 - `pipeline/<city_slug>/config.py`

Per-city, not shared, until more cities show the common shape (see
`PLAN.md`). Mirror San Diego's or San Francisco's names and shape. Include:

- Paths, plus `RAW_CLASSIFICATION_COLUMN` (the raw export's classification
  column; step 2 renames it to the taxonomy's `VALUE_COLUMN`).
- **The city's own projected CRS.** Look up the UTM zone from its
  longitude; never copy another city's. Comment how you derived it.
- Ring edges: reuse `[0.0, 0.1, 0.2, 0.3, 0.6]` miles unless station spacing
  is meaningfully different.
- Station scope: which lines count and why. Document the choice.
- How in-city rows are identified: `CITY_KEEP` (the exact string the dataset's
  city field uses; note any neighbourhood it undercounts - San Diego's La
  Jolla) or, better where the dataset has one, an authoritative district
  field (Los Angeles' `council_district` 1-15).
- `TAXONOMY_SYSTEM` (a key from `TAXONOMY_MODULES`) and a sanity bounding
  box for coordinates.

## Step 4 - `step1_stations.py`

GTFS -> station list -> **spatial filter against the real boundary polygon**,
never a hand-curated name list. Print the raw stop-name list first and
collapse platform-name duplicates via an alias dict. Print which stations
were excluded so a scope mistake is visible, not silent. Match routes by
exact `route_short_name`/`route_id` after printing the routes table - a
substring match once swept in a shuttle-bus route.

**Check the rail system's shape before assuming "keep every station."**
Uniformly sparse systems (San Diego's Trolley) keep every in-city station.
A system with a compact central corridor plus dense street-running
offshoots (San Francisco's Muni Metro: 147 stops, mostly every 1-2 blocks)
does not: keeping all makes the rings overlap continuously; keeping only the
central stations drops whole districts. For that shape use the
**sub-transit-line filters** (`docs/sub_transit_line_filters.md`): central
stations always kept, terminals always kept, surface stops thinned to a
target spacing measured along the real route, interchanges force-kept.
Document every cut station (name, line, reason, nearest kept station) to
`outputs/<city>/excluded_stations.csv`. Stations dropped by the boundary
filter deserve the same record, with the city each lies in (Los Angeles: 54
of 110 stations, across 23 other places) - use a multi-city boundary layer
so the city can be named.

**Measure inter-station distances against the 0.6 mi outer ring.** Where
several stations sit closer than that (downtown clusters), their rings
overlap. The map assigns each business to its nearest station so nothing is
double-counted, but the overlap is visible and should be a conscious
choice; it would matter directly if ring statistics are ever added.

**Stations excluded for lying in another city are a new project, not a
config change.** San Diego dropped 16 Trolley stations in neighbouring
cities; including them would need those cities' own business data, sourced
and verified separately (and geocoding coverage there may be worse). Log it
as a scoping decision rather than quietly widening a filter.

## Step 5 - `step2_clean_businesses.py`

Rename the raw classification column to the taxonomy's `VALUE_COLUMN`, then:
restrict to the city (`CITY_KEEP`), filter to storefront with
`pipeline.taxonomies.filter_to_storefront()` (never NAICS prefixes
directly), apply the active flag if there is one, drop rows without valid
coordinates, bounds-check them, and deduplicate on the dataset's real
primary key (not business name - chains share names). Rename to the shared
columns the map expects (`business_name`, `latitude`, `longitude`, plus the
`VALUE_COLUMN`). Read the printed row counts at every filter - that is how a
scope mistake surfaces, and they become the baseline in `DECISIONS.md`.

**Never silently drop a large share of rows.** If a filter drops more than a
few percent, find out why and whether the loss is uniform (by start year,
category, district) before accepting it. Los Angeles' coordinate check
dropped 9% of storefront rows, 22% of businesses started since 2020 versus
~1% of older ones; dropping them would have systematically under-counted new
openings. If the rows are recoverable (they still have street addresses),
flag them instead - blank the bad coordinates and set a `coord_status` - and
recover them in a geocoding step with `pipeline/census_geocoder.py` (US
only; responses cached by content hash so re-runs and drift checks stay
deterministic). Accept geocoded points only inside the city's bounds,
record `geocode_source` on every row, and report the residual loss and its
bias. Cross-check in-city identification against the boundary polygon.

**Only add a geocoding step if Step 0 found coordinates missing or unusable;**
when you do, it becomes step 3 and the map step 4 (LA is the worked
example).

## Step 6 - `step3_map.py`

Don't copy map code - call `render_heatmap()` from `pipeline/map_common.py`.
It owns everything generic (heat layers, rings, stations, clustered
per-category pins with the scaled cluster icon, line labels, legend). Copy a
built city's thin `step3_map.py` and change only what's city-specific: map
transit-line specs `{key: (shape_id, colour, real public name, label end)}`
for `load_line_shapes` (label end `None` = automatic), the city boundary for
`label_focus`, the config paths and the taxonomy name. Don't hand-pick a map
centre or zoom: the view is fitted to the stations and labels. Each line's `shape_id` is its single most-used trip shape - count trips
per shape for the route and take the mode. **Nothing in `map_common.py` may
name a taxonomy;** if a city needs behaviour it lacks, extend the module
rather than forking a per-city copy.

**Transit lines are a hard requirement:** draw each from real GTFS
`shapes.txt` geometry, and give every line BOTH a permanent on-map label
using its real public name (verify it - a GTFS short name is not
automatically what riders call it) AND a legend swatch. Label placement is
automatic: each label goes at its line's tail end (the end farthest from the
other lines), labels that would collide disperse along their lines, and they
sit above the pins. Always pass `label_focus` - the city's boundary geometry
- so tails are taken on the in-city stretch of lines that run far beyond it.
If a rendered map still shows a label landing badly, force that line's end
with `"start"`/`"end"` in its spec. The legend collapses by itself; check
both in the browser. If the
agency's official line colours are ambiguous or shared, use a palette of
your own that stays distinct from the business-category colours.

## Step 7 - Run it for real, then look at it

Run steps 1-3 and read the counts. Then open the rendered map in a browser
before calling it done: serve `outputs/<city_slug>/` (or use the
`deploy-verify` agent's `heatmap-static` config) and confirm the heat layer,
rings, line labels, legend and clustered pins render over real geography,
with no console errors. A pipeline that runs cleanly is not a map that looks
right.

## Step 8 - Wire into the app

- `app/pages/N_<City>_Heatmap.py`: the static-HTML-embed pattern
  (`st.components.v1.html()`, UTF-8 read, fixed size matching the map), not
  `streamlit-folium`. Call `components.set_base_font()`.
- Add the city to the `CITIES` list in `app/cities.py` (name, marker lat/lon,
  page path, blurb). That one entry feeds the clickable macro map on the
  Overview, its fallback link list, and every city page's switcher. In the
  new page, call `components.render_city_nav("<City name>")` (the name must
  match the entry) instead of a bare back-link. If a page file is ever
  renamed, update its `page` path in `cities.py`.
- **Grep the city page for hardcoded prose** - words like "six lines",
  station counts, "half mile" are literal text, not computed values, and go
  stale when the pipeline changes. Prefer wording that doesn't restate
  numbers; where it must, re-check it each time the city's pipeline changes.
- **Never let the city's name become the project's identity.**

Then run the `deploy-verify` agent (lean venv; the macro map shows every city,
clicking each marker opens its page, each switcher works, each map renders).

## Step 9 - Commit, log, plan

- Run `python pipeline/drift_check.py <city>` after committing the city, to
  confirm outputs regenerate identically.
- Add `DECISIONS.md` entries (see the `decisions-entry` skill): the city
  added with per-step row counts, every scoping decision and rejected
  alternative, workarounds (a mirror host, a hand-curated alias list), and
  known limitations. Counts go there, not in `project_context.md`.
- Update `docs/project_context.md` (current state only - which cities exist,
  what's distinctive; no counts), `docs/city_shortlist.md`, and tick or add
  items in `PLAN.md`.
- Keep the honesty convention: mark what's verified vs. still a skeleton.
