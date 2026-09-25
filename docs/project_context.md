# Project context

The stable briefing for this project: what it is, what's settled, how it's
built, and where things stand. Read it at the start of a session. It
describes the *current* state and is rewritten as things change; the dated
reasoning behind each decision is in [`DECISIONS.md`](../DECISIONS.md), open
work is in [`PLAN.md`](../PLAN.md), and working rules are in
[`CLAUDE.md`](../CLAUDE.md).

## The project

A multi-city map of commercial (storefront) density around rapid-transit
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
  Overview.py  macro page: clickable map of every city
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
such as NACE - means adding one module. `naics.py` is complete. The two
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

- **New York** - the MTA subway plus the Staten Island Railway, every station
  in the five boroughs (nothing excluded: the network does not leave its own
  city). Distinctive in four ways. It is the only city whose businesses come
  from **more than one registry** - New York has no general business licence,
  so Food service, grocery Retail and Personal services each come from their
  own source, and `pipeline/taxonomies/new_york.py` dispatches on a `source`
  column rather than reading one classification field. It draws **lines, not
  services**: 29 subway services grouped into the 11 trunks the MTA itself
  signs, so a trunk's geometry is several polylines under one label. It is the
  only city **not using the shared ring edges** (stations sit a median 482 m
  apart, so the rings are halved and start switched off, remaining in the
  layer control where they still read - the outer boroughs and Staten Island).
  And its **Retail bucket is knowingly less complete** than other cities': a
  shop needing no licence from any of the four registries is absent, while
  restaurants are near-complete. Its map is step 4 (a geocoding step recovers
  DCA's missing coordinates).

- **Philadelphia** - SEPTA Metro: the Market-Frankford and Broad Street Lines
  (with the Ridge Spur), the five subway-surface trolley branches and the
  Girard Avenue trolley, drawn as four line groups. Regional Rail is a separate
  feed and is not included; the Norristown and Media/Sharon Hill lines have no
  stations inside the city at all. Distinctive in three ways. It is the only
  **two-bucket** city: Philadelphia licenses no personal-service business and
  Pennsylvania publishes no licensee addresses, so Personal services is
  **absent rather than thin**, and the multi-source approach that rescued New
  York was tried here and found nothing to add. It is the first city needing
  **two station rules at once** - the grade-separated lines keep every in-city
  station, while the street-running trolleys (a 134 m median) take San
  Francisco's four-filter thinning. And it is the first registry whose
  business-name field is **"LEGAL NAME (TRADE NAME)"**, so step 2 chooses the
  trading half rather than copying the field, which keeps licence holders'
  own names off the pins. Its own `legalentitytype` field gives a structural
  Individual/corporate signal no other city has.

- **Miami** - Metrorail plus both Metromover loops, 42 stations. **The FIRST
  REGIONAL map here** - the working proof of the multi-jurisdiction idea
  Seattle is planned around, and the shape Vancouver, Guadalajara and Dublin
  each took later. Metrorail leaves the City
  of Miami, and everywhere else that ends the discussion - a station in another
  city needs that city's own business data, sourced separately. Miami is the
  exception because Miami-Dade County licenses all 34 of its municipalities in
  ONE file, one schema, one publisher, one set of terms, so full-line coverage
  needed no extra sources, no cross-source dedup and no second licence review.
  Six municipalities hold stations; the boundary layer NAMES where each station
  is rather than filtering any out, recorded in
  `outputs/miami/station_municipalities.csv`.

  Distinctive in four further ways. Its file **has a NAICS column that is null
  on every one of 194,099 rows**, so it runs on the county's own `CATGRYNAME`
  (`miami_catgryname`, all 150 values verified) - the first city where NAICS
  was present in the schema and unusable in fact. It is the first city needing
  a **premises dedup**: none of the obvious keys is a premises, because
  `RECEIPTNO` is per row, `ACCOUNTNO` per account and `FOLIO` per *parcel* (a
  mall is one parcel holding dozens of shops), so rows collapse on
  name-plus-address with the taxonomy's bucket priority deciding. It has the
  **best coordinate quality in the project** - 100% present, inside the county,
  no placeholders - and is the only registry whose trade name is *never* blank,
  so unlike Los Angeles and D.C. it never has to consider a registrant's name.
  And it needs **two station rules' worth of care from one lever**: Metrorail's
  stations are a median 1.1 km apart while the Metromover's nineteen are 235 m
  apart and all inside a neighbour's ring, so the shared ring edges are kept
  (Metrorail needs them) and the rings simply start switched off, as New York's
  do. Its map is step 3; its line colours are this project's own, because
  Miami-Dade's orange and two greens collide with the category colours.

- **Boston** - MBTA rapid transit: the Red, Orange and Blue Lines, the Green
  Line's four branches and the Mattapan Trolley, drawn as five line groups.
  Regional Rail and the ferries are not included. Distinctive in four ways.

  It is the **second two-bucket city**, and the narrowest map here: Boston
  licenses food and alcohol and essentially no other trade, so Personal
  services is **absent rather than thin** (Massachusetts licenses cosmetology
  at state level and publishes no address-bearing export, verified three ways)
  and Retail means retail *food*, package stores and cannabis. The city page
  leads with that rather than burying it. It assembles **three registries**,
  dispatched on a `source` column like New York's, and deduplicates ACROSS them
  as well as within - 27 premises held licences in more than one, mostly
  package stores that also hold a food licence. It needs **two station rules at
  once**, as Philadelphia does: the grade-separated heavy rail keeps every
  in-city station while the Green Line's street-running branches take San
  Francisco's four-filter thinning. And its two smaller sources publish
  **`gpsx`/`gpsy` in EPSG:2249** - state plane in US survey feet - which step 2
  reprojects; that is a different CRS from the city's own EPSG:32619.

  Its licensing is the cleanest of any city here (every source ODC-PDDL), and
  it is the first city to activate a transit notice: MassDOT requires that it
  be acknowledged as the provider, which takes the mandatory-notice count from
  four to five.

- **Washington D.C.** - WMATA Metrorail: the Red, Blue, Green, Yellow,
  Orange and Silver Lines, six lines drawn from six route_ids. Distinctive in
  four ways.

  It is the **first non-NAICS registry in the project to cover all three
  buckets on its own**. New York needed four sources and Boston three;
  Philadelphia and Boston each ended up with a category missing entirely.
  D.C.'s Basic Business License register licenses restaurants, shops and salons
  in one file, so there is no `source` column to dispatch on and no
  cross-source dedup. What it needs instead is a **verdict on all 95 licence
  categories**, because `classify()` raises rather than defaulting: 61% of the
  in-District register is residential rentals and a further 11,074 rows are
  `General Business`, the office catch-all.

  It is the **only feed behind an API key**, and the only one that **expires**:
  WMATA declares a ten-day validity window, so `fetch_sources.py` re-checks
  `feed_end_date` on every run, including runs that skip the download, and
  treats an expired copy as an error. The key is read from the environment and
  never printed.

  Its **published coordinates are useless** - `LATITUDE` is 39 and `LONGITUDE`
  is -77 on every row in the register - so step 2 reprojects
  `X_COORDINATE`/`Y_COORDINATE` from EPSG:26985 instead, a third CRS distinct
  from the city's own EPSG:32618. That leaves 6.9% of storefront rows with no
  coordinates at all, which makes this the second city after Los Angeles to
  need a **geocoding step**, so its map is step 4.

  And **58 of its 98 stations are outside the District** - the second-largest
  station exclusion here after San Diego's. The states they lie in are NAMED
  rather than merely counted, which is why a Census TIGERweb layer is
  downloaded alongside the District's own boundary.

- **Vancouver (Regional)** - TransLink SkyTrain: the Expo, Millennium and
  Canada Lines. **The first city outside the United States, and the first
  built from two municipalities' own registries.** Distinctive in five ways.

  It is **regional by choice, covering Vancouver AND Surrey**, because SkyTrain
  is regional and Surrey has no rail of its own. Miami is the precedent but the
  easy version of it: Miami-Dade licenses all 34 of its municipalities in one
  file, whereas Vancouver and Surrey are two publishers, two schemas and two
  licences. So the taxonomy dispatches on a `source` column, as New York's and
  Boston's do - but with **no cross-source dedup**, because the two registries
  cover disjoint municipalities and no premises can appear in both.

  Its **classification is two vocabularies at once**: Vancouver's 89
  single-valued `businesstype` values and Surrey's 210 `BusinessCategory`
  values, which are **newline-separated with several per licence**, so a
  premises holding more than one is resolved by `BUCKET_PRIORITY`. Buckets are
  anchored on `naics.py` rather than invented, which is what keeps this city
  comparable with every city sharing that anchor. (Named, not counted: this
  said "the five NAICS cities" until 2026-09-22, when there were four.
  `CLAUDE.md` asks this file to carry no counts, and that is why.)

  It is the only city whose **registry marks individual registrants itself**:
  Vancouver wraps a sole proprietor's own name in parentheses. That is a
  structural signal of D.C.'s `ENTITYTYPE` kind, and it is what the
  name-suppression policy runs on - where a licence has no trade name and the
  legal name reads as a person, the pin shows its business type instead.

  Its **residence filter was built and removes nothing**, which is a measured
  result: the parcel-to-zoning join works, but the pairing it exists for leaves
  one row and that row is a false positive. Zoning alone is unusable there
  because Vancouver has real corner shops on residentially-zoned land. Surrey
  needs no inference at all - it **states home occupation on the licence**,
  which is better evidence than any US city's parcel join, and that is half its
  register.

  And it is the **first city to add more than one required notice**: OGL -
  Vancouver, OGL - Surrey (whose wordings are not interchangeable) and
  TransLink's Legend, which has to be the GTFS text rather than the Open API
  one. Its boundary layer also has a **hole at Stanley Park**, so the boundary
  is a check rather than a filter.

- **Montréal** - the STM Métro: the Green, Orange, Yellow and Blue Lines, at
  agglomeration scope. Distinctive in three ways, and the cheapest build here.

  **Its source is a field survey rather than a licence register**, the only one
  in the project, and that changes what has to be filtered. A survey of
  commerce can contain an empty shop where a register of licences cannot, so
  vacancies are excluded - nobody had recorded that they were in there, and the
  obvious for-rent column turns out to be a strict subset of the vacancy flag,
  so filtering on that instead would have left most of them in. The
  classification is filtered by LENGTH rather than for nulls, because it is a
  one-character placeholder on a couple of hundred rows and a not-null test
  keeps codes that cannot be classified. What remains is a storefront share
  more than double any other city's, which is the whole story of the build.

  It **needed no taxonomy module at all**, which no other city here has
  managed: SCIAN is NAICS, so `naics.py` classified it unchanged and the only
  adaptation was renaming a column.

  And it takes **no address dedup, deliberately** - the opposite of Miami's and
  Vancouver's call, decided on the survey's own structure. Every row is one
  surveyed unit with its own identifier, and thousands of rows share an address
  legitimately: one shopping centre holds over a hundred and seventy units, so
  a name-plus-address dedup would have collapsed a mall to one shop. Step 2
  asserts that identifier's uniqueness instead. Its off-island cut is spatial
  per the project invariant and cross-checked against a structural marker - STM
  marks exactly the four off-island stations with a fare-zone suffix, and
  step 1 stops if the two ever disagree. No thinning, because the Métro is
  entirely underground and grade-separated, which is the structural test rather
  than the spacing.

- **Calgary** - Calgary Transit's CTrain: the Red and Blue Lines. Distinctive
  in four ways.

  Its **licence register names premises itself**, and no other city's does. The
  96 categories carry `- PREMISES`, `- NO PREMISES`, `(MOBILE)`,
  `(HOME BASED)`, `(MAIL ORDER)` and `(DIRECT SALES)` suffixes, so the question
  every other map infers is answered in the category string. 65.7% of active
  licences are storefronts, second only to Montréal's 69.4%.

  It is the **first city where nothing is excluded**: the CTrain never leaves
  Calgary, so `excluded_stations.csv` is written empty rather than skipped.

  Its feed publishes **83 platforms, not 83 stations** - a direction prefix on
  every stop name and no `parent_station` column - which collapse to **45**.
  The whole Canada ranking had recorded the platform count, so its density
  went from a published 75 per station to a measured **137**. Its `route_id`
  also embeds a feed version, so routes match on `route_short_name`.

  And it has **no home-business signal at all**: `homeoccind` is `N` on every
  row. Surrey and Edmonton state home occupation on the licence; Calgary
  asserts nothing, and no inference is attempted.

- **Edmonton** - Edmonton Transit Service's LRT: the Capital, Metro and Valley
  Lines. Distinctive in four ways, and the first city whose publisher did this
  project's privacy work for it.

  **Three of its 33 apparent stations are not stations, which is a NEW error
  class here.** Every rail trip touches two garage access points and a tail
  track, and `pickup_type` and `drop_off_type` are both 1 on every one of their
  stop_times - nobody can board. The platform check that caught Toronto and
  Calgary passes cleanly here (`parent_station` is populated on all 65 served
  stops, collapsing to 33 at a healthy 713 m median), so this needed a
  different test: **boardability**. Edmonton has **30** stations. Every city in
  this project should have had that check and none of them did.

  Its register **states premises-or-person and redacts the rest itself**.
  `licencetype` separates `Commercial` from `Home Based`, `Non-Resident` and two
  individual-held types, so no residence inference is needed; and
  `<REDACTED FOR PRIVACY>` replaces the address on 4,074 rows **and takes the
  coordinates with it**. It also publishes **no name column but the business's**
  - no registrant, owner or contact field exists - so its privacy position is
  structural: no pin *can* be a person's name.

  Its **line colours are this project's own, chosen by measurement**. ETS signs
  Capital blue and Valley green, which sit Delta-E 23.9 and 37.2 from the Retail
  and Personal services pin colours against a working threshold of ~45, so each
  line keeps its hue and is darkened until it clears. Colour separation is an
  **intra-city** constraint only: Edmonton's Metro red is deliberately the same
  as Calgary's Red Line.

  And its **Personal services bucket is knowably generous**: the accredited
  `Health Enhancement Centre` licence covers massage and spa premises alongside
  physiotherapy and chiropractic clinics, which are NAICS 621 health care, and
  the register does not distinguish them. About a quarter of that class reads
  as a clinic. Counted anyway, for Alberta comparability with Calgary, and
  disclosed on the city page.

- **Toronto** - the TTC's rapid transit: Lines 1, 2 and 4 of the subway and
  Lines 5 and 6 of the LRT, with its 18 streetcar routes out of scope.
  Distinctive in four ways, and the hardest build here.

  **General retail is ABSENT, not thin**, and it is the most severe coverage gap
  on the site. Toronto licenses no grocer, clothing shop, pharmacy or hardware
  store, so the Retail bucket holds the *regulated* slice alone - second-hand,
  pawn, precious metal, smoke, vape, pet, salvage and permanent fireworks - which
  is **870 of 19,575 storefront rows**. The bucket is drawn and disclosed rather
  than omitted (the owner's call, and New York's treatment); the city page and
  `excluded_categories.md` both say what it does and does not contain.

  **Its register carries NO coordinates - not one row**, so it is the only city
  of six Canadian candidates that genuinely needed a geocoder, and Canada has
  none. Step 3 joins against the City's own One Address Repository and the map
  is step 4. The normalisation that matters is one line and it is not street
  normalisation: the register writes the unit into the address and the
  repository carries none, so dropping everything after the first comma takes
  the match from 48.1% to **93.8%**.

  **Its station count was wrong twice before the build**, and it is why this
  project distrusts station counts at all. `parent_station` is populated on no
  stop, and **three platform-naming conventions live in one feed** - the subway
  hyphenates, the LRT does not, and Union Station names its destination. 234
  platforms collapse to 110 stations, 108 of them in-city, and every per-line
  count now matches the TTC's own published figures exactly. The two Line 1
  stations in York Region are recorded in `excluded_stations.csv`.

  And **`MUNICIPALITY_NAME` in the address repository is not a city filter**,
  despite looking like one: it holds the six pre-1998 municipalities, so
  matching "Toronto" would have kept 30% of the city. Los Angeles' `CITY_KEEP`
  trap, caught before it ran.

- **Mexico City** - Metro CDMX (Lineas 1-9, A, B, 12) and the STE Tren
  Ligero. SCIAN via `scian.py`. Businesses from INEGI's DENUE, an establishment
  CENSUS rather than a licence register. **Rail geometry from OpenStreetMap**,
  because every `*.cdmx.gob.mx` host is unreachable - an owner-approved
  per-city exception, stated on the page. Gate 3 unavailable for the same
  reason and recorded as unavailable.
- **Guadalajara (Regional)** - Tren Ligero Lineas 1-4, across Guadalajara,
  Zapopan, San Pedro Tlaquepaque and Tlajomulco de Zuniga. Miami's and
  Vancouver's regional shape. Rail from OpenStreetMap again, this time because
  the only GTFS feed expired 2023-01-28 and predates Linea 4. Gate 3 DOES run
  here and passes against SITEUR's published counts.

- **Madrid** - Metro de Madrid: Líneas 1-12 and the Ramal Ópera-Príncipe Pío.
  **The first city in Europe.** Distinctive in four ways.

  Its **rail comes from the operator's own feature services, and the reason is
  a licence clause rather than an absence.** CRTM publishes a Metro GTFS, it
  downloads cleanly, and it was rejected: the feed stopped being refreshed in
  May 2025 while CRTM's licence obliges a reuser to keep displayed information
  *siempre actualizada*. The ArcGIS layers carry the same network and are
  maintained. So `map_common.py` grew a third line-shape loader beside the GTFS
  and OpenStreetMap ones rather than a fork - the standing rule that a city
  extends the shared renderer, paid for and held a third time. OSM is the
  cross-check here, never the source.

  Its **line codes do not collapse uniformly into lines**, which is
  Guadalajara's lost-line trap in a third form. A naive distinct count would
  draw Madrid as an eighteen-line system: most codes are a line, three are
  lettered branch pairs whose case is inconsistent, so a case-sensitive
  collapse strands one branch as its own line, and two circular lines are
  published as two one-direction codes each. Three independent sources agree on
  the real number.

  Its **taxonomy keys near the top of its scheme** - one division per bucket,
  with a handful of epígrafes carved back out, which is `naics.py`'s
  groups-plus-exclusions shape. Barcelona keys at the opposite end of an
  identically-shaped scheme, and both were measured rather than inherited.
  `HOSTELERÍA` is the 72-versus-722 trap in Spanish, holding accommodation
  alongside food and drink; and NACE 47 is retail where NACE 46 is wholesale,
  the exact inverse of SCIAN, so a reader carrying the Mexican numbers across
  gets the wrong half of the register.

  And its **coordinates are fully populated and partly invalid**: a large block
  of rows carries a literal zero stored as a string, so an is-it-populated test
  passes them and the pin lands in the Atlantic. Unlike Los Angeles the loss is
  biased *away* from the mapped rows - it concentrates in tourist flats,
  hostales and offices, which this project does not map - so no geocoding step
  is needed. Station names are re-cased for display, because the register
  shouts in capitals and `.title()` is wrong in Spanish.

- **Barcelona** - Metro de Barcelona: L1-L12 across two operators, plus the
  Montjuïc and Vallvidrera funiculars. Distinctive in four ways.

  Its **rail geometry is OpenStreetMap's, and what counts as a line was settled
  by the operators' own `network` tag** rather than by a judgement about what a
  metro is. That test keeps TMB's and FGC's lines and both funiculars, and
  drops the Tibidabo funicular - run by the municipal parks company and
  carrying no network tag - along with the trams, without a separate decision.
  Deciding by mode would have been wrong in both directions: FGC's rack
  railways share a mode with a funicular and sit fifty and a hundred and fifty
  kilometres away.

  It found that **a route relation and a station node are different objects**,
  after a station query returned exactly zero: a relation holds stop positions
  while the station box hangs off a stop area. The step raised rather than
  writing an empty map. It is the third distinct station object in three OSM
  cities.

  It **collapsed two interchanges its two operators name differently**, which
  the shared spacing gate structurally cannot catch. FGC and TMB write
  Catalunya and Espanya under different names, metres apart, so two of the
  busiest stations in the city were drawn twice, with two markers and two
  overlapping ring sets. A median cannot see two bad names; the
  nearest-neighbour minimum did, and `pipeline/stations.py` now prints that
  minimum for every city as a prompt rather than a threshold, because Barcelona
  also has a genuine pair that close.

  And its **taxonomy keys at the finest level of its scheme** - the opposite of
  Madrid's, on measurement: the group level puts a third of active rows in
  `Altres` where the finest level puts a fortieth of that. The group holding
  restaurants also holds accommodation, so keying there would have published
  hotels as food service. `Altres` is then dispatched on two further columns,
  because it means five different things depending on its parent. Built on the
  survey year that is complete rather than the one that is fresher: the newer
  release is short by four fifths in the outer districts against a twentieth in
  the centre, so a map drawn from it would show the periphery as commercially
  dead - which is roughly what a reader expects, and would therefore not look
  broken.

- **Dublin** - the Luas Red and Green Lines and the DART, across four local
  authorities. Distinctive in four ways.

  **Its register carries no business name of any kind** - no trade name, no
  occupier, no ratepayer - so the address is the pin label. Los Angeles'
  failure mode cannot occur here structurally rather than by a filter, and
  step 2 exits if a name-like column ever appears. This is its own case rather
  than Milan's hybrid, and the build records which, because
  `check_personal_exposure.py`'s heuristics measure nothing when every label is
  an address: its person-like hits are Irish streets named after people, floor
  lists read as surname-first, and unit descriptors read as a person plus a
  trade name.

  **Its rail source was wrong in its brief and was reversed mid-build.** The
  brief recorded OpenStreetMap, which had never been measured: the agency's
  national feed is maintained a year ahead and carries a station that opened
  the previous year, and the agency also publishes a feature service. The rule
  that followed is now in `osm-rail` - a brief may not record OSM as the rail
  source without naming the agency endpoints that were tried. OSM is retained
  as a cross-check and runs on every build.

  **OpenStreetMap tags every DART relation as commuter rail**, so a network
  filter drops the line the city is built around, and the first step 1 did
  exactly that and exited naming DART as missing. The whitelist is on the line
  reference instead. Third measured instance of the rule that a network tag is
  a label rather than evidence, and the first where the mis-tagged line is the
  principal one.

  And it is the **first city here with neither a geocoding step nor a
  reprojection step**: both its sources publish in Irish Transverse Mercator,
  the project's first national grid, so the only transform is to draw. The
  per-city-UTM invariant was extended rather than relaxed - a national grid is
  admitted only where the city's own longitude falls inside that grid's domain,
  so a copied CRS still fails exactly as it did. Its line palette is measured
  rather than inherited, because feed and feature service both leave the route
  colours empty: nothing red or green clears the preferred separation from the
  category pins, and the DART moved off green entirely, which fixed a problem
  no number showed - the map had two green lines.

- **Milan** - Metro M1-M5; the seventeen tram routes are recorded as a costed
  extension rather than a discard. Distinctive in four ways.

  It assembles **six premises registers, the most of any city here**, and its
  **taxonomy is keyed on the register rather than on any classification
  field**, because every in-dataset classification is unusable: one carries
  sixty-odd distinct values for what should be three, half of them pure case
  variation and thousands of them two values concatenated, while the other two
  are more than half blank. The field naming each dataset's own remit is a
  single clean value at full population. Bucket equals source, dispatched
  through `EXTRA_COLUMNS` as New York's taxonomy does, with no change to the
  shared renderer. The one judgement inside it: a food shop is Retail, not Food
  service - the same line Dublin drew.

  It **deliberately does not deduplicate across its sources, which is the
  opposite of New York's call**, and the ground is measured rather than
  stylistic. The registers' identifier prefixes never collide between any pair,
  so they are demonstrably separate registers of different activities; and an
  address cannot be a key at all, because more than half the rows in the
  largest register already share one with another row inside it. A shop and a
  bar at one Milan address are two premises. Step 2 asserts the disjointness
  rather than merging, so a future overlap fails loudly, and the over-count
  where one business holds two licences is stated on the city page.

  Its pins take the **hybrid naming pattern the French cities later
  inherited**: the trade name where the register carries one, the address
  otherwise.

  And its **rail comes from the agency's own layers with both of `osm-rail`'s
  agency steps run**, hitting three traps that are each guarded in code rather
  than noted - a string identifier joined against an integer one, which matches
  nothing at all; a station layer whose features are not stations, with
  interchanges modelled two incompatible ways so that a distance threshold is
  wrong in both directions at once; and a `stops.txt` that cannot select metro
  stations, the columns that would do it being empty on every stop. Gate 3 runs
  against the agency's own join table and passes. Fixing it also fixed a gate
  that passed on zero: a check that cannot distinguish "no data" from "no
  answer" is not a check.

- **Paris** - the Métro: Lignes 1-14 plus 3bis and 7bis. **The first French
  city, and the first built on a national register.** Distinctive in four ways.

  SIRENE is one register for the whole country, so its classification module is
  the **first in `pipeline/taxonomies/` that belongs to a country rather than
  to a city**, keyed on the finest level of NAF on the same kind of measurement
  Barcelona used. It keeps two kinds of exclusion apart rather than merging
  them into one list: the structural ones are national, because the publisher's
  own label says the activity happens away from a shop, and so hold in
  Marseille too, while a catch-all's composition is a fact about a city,
  sampled per city and recorded in that city's config. Merging them would have
  let a national module silently make a per-city call.

  It projects to **Lambert-93, not the UTM zone the scaffold derived**, and
  that is the project's second national grid. Metropolitan France spans three
  UTM zones, so a per-city UTM rule would give several cities reading one
  national file three different projections. The invariant is metres derived
  per city and never copied; deriving from France's own grid satisfies it where
  copying a zone between French cities would not. The grid is admitted bounded
  to metropolitan longitudes, because the register's own CRS column also
  carries the overseas départements - an inherited hardcoded Lambert-93 would
  put every pin in the sea *without raising*, and those bounds are what raises.

  It is **scoped to the commune on a measurement**, not by default. Every métro
  line survives the boundary, and the two modes lying mostly outside it would
  not be drawn at any scope - the RER and Transilien are commuter rail,
  excluded in every city here, and trams are already excluded in Barcelona,
  Milan and Toronto. So regional scope buys Paris almost nothing, which is the
  opposite of Dublin, whose register is published per local authority and whose
  rail scope followed from that rather than the reverse.

  And it carries the **only notice in this project that prescribes markup**.
  Licence Mobilités requires the database name to hyperlink to the dataset and
  the licence name to the licence text, so `render_site_notices()` cannot carry
  it as plain text the way it carries LA Metro's. It is also the first
  revocable grant here - every other source is perpetual - and the response was
  decided in advance: if the grant lapses, the page comes off the site and the
  entry out of `app/cities.py` while the pipeline and the record stay, because
  a city coming down is not a city being deleted. The same licence requires the
  data's last-updated date and its update interval to be displayed, and neither
  exists inside the feed, so the national access point's metadata API is a
  load-bearing source in its own right rather than a convenience.

- **Marseille** - RTM's Métro 1-2 and Tramway 1-3. France's second city, and
  the one that turned the country's shared parts into shared code: the national
  extracts are the same bytes for every French city, so they moved to one
  country-level cache rather than a copy per city, and step 2 became a country
  module that Paris re-ran through at zero drift - which is what made it a
  refactor rather than a rewrite. Mexico is the deliberate counter-example and
  is left alone, its national register being partitioned per state, so its two
  cities read genuinely different files; the rule is "the same bytes", not "one
  national source". Its **scope was measured rather than inherited from
  Paris**, because its feed is the whole métropole: every RTM line sits inside
  the commune, and the fourth tram in that feed belongs to Aubagne and has no
  station inside it at all, so **the same spatial filter that scopes the city
  drops another operator's network as a side effect** - better than a
  hard-coded exclusion, which the next French city reading a multi-network feed
  would have had to remember. The ferries are dropped by the owner's decision
  and recorded as revisitable, because they are genuine urban transit here,
  which no other excluded mode in this project is.

- **Toulouse** - Tisséo's Métro A and B, Tramway T1, and the Téléo cable car.
  France's third city. Distinctive in three ways.

  It is the **first city here to draw a non-rail mode**. Téléo is an aerial
  lift, and the case for it is functional rather than technological: the
  operator runs and tickets it as it does the métro, every one of its stations
  is inside the commune, it crosses the river where no other line does, and one
  of them is a métro interchange. The owner's call, made after the argument in
  its own brief turned out to be false - it cited Paris's funicular as
  precedent, and Paris excludes its funicular - and the brief was corrected in
  place rather than left to mislead the next reader.

  **Commune-only scope costs Tramway T1 half its stations**, the whole airport
  branch, and that is the finding the obvious test cannot see: Marseille's rule
  was that every line survives the boundary, and every line survives here too.
  So the config now records the per-line split and step 1 exits if it moves.
  Commune-only was taken anyway, with both alternatives put to the owner and
  declined, because it keeps the French cities on one comparable scope.

  And its **gate 3 matches the operator exactly on all four lines** - the
  cleanest of any city here - where the layer that looks like the right one
  would have failed it: the obvious tram layer holds four extra stations, every
  one tagged with a service year still in the future, sitting beside the built
  ones and separated only by that column. That is `osm-rail`'s
  proposed-mixed-with-built trap found in a first-party agency layer rather
  than in OSM, so the whitelist rule it states is not an OSM rule. Its
  catch-all share diverged from both siblings and was measured rather than
  inherited; and a fifth of its active establishments are masked at source -
  name, address and location together - so a thin-looking street here may be a
  quiet one or a private one, and nothing in the data separates them. The page
  says so.

- **Lille (Regional)** - ilévia's Métro 1 and 2 and Tram R and T, across the
  eleven communes the network serves. France's fourth city and **its first
  regional one**: the commune of Lille alone would have kept fewer than half
  of Métro 2's stations and drawn the tram as a three-stop stub. Its rail comes
  from three sources, line by line in `osm-rail`'s order - the Métropole's own
  GIS for every station and the tram lines, OpenStreetMap for the métro lines
  that exist nowhere else, and the operator's feed not read at all. The served
  communes were derived by placing every station in the official contours, and
  the Métropole's own station labels would have missed one of them.

- **Rennes** - STAR's Métro a and b. France's fifth and last city, the smallest
  and the best-named. **Its brief's scope premise was wrong**: "the métro is
  city-contained" held for line a and not for line b, which leaves the commune
  at both ends. Commune-only was the owner's call on the corrected measurement,
  because line b keeps more of itself than Toulouse's T1 did - which made the
  worst line's survival the rule the French cities share. Its gate 3 matches
  the operator's own per-line stop layer exactly, and the operator's station
  layer names the same four stations as outside the commune - read the night
  after the build, because the portal's API was refusing every caller on a
  spent domain-wide daily quota. The feed is on a separate host and was never
  affected.

- **Oslo** - Ruter's T-bane lines 1-5 and six tram lines. Norway's first city,
  and the first built off a register of PREMISES rather than companies: the
  Brønnøysund register's sub-units carry each business's physical location
  address, kept apart from the company's registered one, which is the
  distinction Czechia's register lacked when Prague was paused. Three things
  are its own. **A sole trader's name is never shown** - the legal form lives
  on the parent unit, not the premises, so every premises is joined to its
  parent and an owner-named business shows its address instead. **The
  coordinates are a join, not a geocode** - Kartverket publishes each
  municipality's whole address register in bulk, which replaced a planned
  ~13,000 geocoder calls. And **its classification is NACE Rev. 2.1**, which
  moved car retail into the retail division and abolished the separate codes
  for selling online, so web shops cannot be excluded by code here the way
  France excludes them; the page says so. The feed colours every T-bane line
  alike and every tram alike, so the lines carry Ruter's own per-line colours
  from its network maps, two lightened to clear the colour check.

- **Copenhagen** - Metro M1-M4 and the S-tog's seven lines, across Copenhagen
  and Frederiksberg, the municipality it encloses. Denmark's first city, and
  the second built off a register of PREMISES: the business register's
  production units, each at its own location address. Four things are its
  own. **The register is a join of six national files**, one per entity -
  premises, address, activity, name, parent company, legal form - on an
  internal id rather than the public unit number. **The S-tog is drawn**
  although suburban rail is left out elsewhere, on the spacing-and-frequency
  test Dublin's DART passed. **The coordinates come from the national address
  register through the same account as the businesses**, because the keyless
  address service the brief relied on closes on 1 October 2026. And **the
  privacy guard is the parent's legal form**, extended past Oslo's to
  partnerships, with Denmark's "v/" sole-trader marker as a second guard. Rail
  is from OpenStreetMap: the national journey planner's GTFS is open but asks
  users not to change the data. The Datafordeler account is the owner's and
  closes after publish.

- **Prague** - Metro A, B and C, all inside the city. Czechia's first city, and
  the third built off a register of PREMISES - after its pause, when the
  business register it started from turned out to record where companies are
  seated rather than where they trade. Four things are its own. **Location and
  activity come from two different registers**: open-data establishments give
  where each business trades, and the Statistical Office's register gives the
  owner's single activity, which every establishment inherits. **Its
  classification is stored at ragged depth**, so the taxonomy matches on code
  PREFIXES rather than at a level - the first here to. **A sole trader's
  premises at their own registered address is left off the map**, not just
  unnamed - the first city where that could be detected. And **Flora station
  is drawn while closed for reconstruction**, with a guard that stops the build
  once the feed serves it again.

- **Amsterdam** - GVB's metro lines 50-54 and sixteen tram lines, inside the
  municipality. The Netherlands' first city, and the first built from two
  layers of different kinds rather than one register. Three things are its
  own. **Two categories, not three**: food service is the city's live register
  of hospitality permits, each under its permit name; everything else is the
  national buildings register's shop-class units in use, which record what a
  unit is for rather than who trades there, so retail and personal services
  are one "Shops and services" category and those dots show an address. **A
  line's stations are its regular route** - served on at least half the
  line's days - because GVB runs up to 30 shapes per line in the national
  feed; trams are thinned with the sub-transit-line filters. And **the tram
  colours are read from GVB's own network map**, since the feed carries none.
  Empty shops, about one unit in twenty, cannot be filtered per unit and are
  disclosed instead.

- **Rome** - Metro A, B, B1 and C and the Roma-Viterbo railway's urban
  service, inside the comune. Italy's second city, and built from nothing
  Milan used: Italy is bespoke per city. Three things are its own. **A
  register of premises with no names and no closing dates**: Roma
  Capitale's SUAP records each authorised premises by the city's street code
  and civic number, JOINED to ANNCSU, the national house-number archive,
  rather than geocoded; its food layer lists about 2.7 times OpenStreetMap's
  restaurants and bars and is stated as an upper bound, since the oldest
  registrations match a mapped place best and no age cut-off would help.
  **Its rail is OpenStreetMap's**, because the agency's timetable data is
  limited to travel information. And **it is the third city to draw
  suburban rail**, after Dublin and Copenhagen: the Roma-Viterbo urban
  service passed the spacing-and-frequency test, and Metromare, to Ostia,
  did not.

- **São Paulo, Rio de Janeiro, Belo Horizonte, Brasília and Salvador, and
  Fortaleza, Porto Alegre, Recife and Santos as regional pages** - Brazil,
  built as one batch from one national source. Four things are their own.
  **The register is a census, not a licence file**: IBGE's CNEFE 2022 records
  every establishment an enumerator walked past, with a coordinate taken at
  the address, so there is no geocoder and no join - and the pages say it is a
  2022 picture. **The classification is free text**: IBGE did not classify the
  establishments, so `pipeline/taxonomies/brazil_cnefe.py` reads the
  enumerator's own words with ordered keyword rules, an edit-distance pass for
  misspellings and a fallback list consulted only for rows nothing else
  matched; descriptions no rule can read - mostly bare trade names, commoner
  near stations - are dropped and disclosed, never guessed. **At an address
  that is also a home, a dot shows only its category**, a structural rule
  rather than a name list. And **commuter lines faced a three-part rail test**
  - spacing, frequency, and coverage of districts no drawn line reaches -
  which drew São Paulo's CPTM Linha 9 and Rio's SuperVia Deodoro and
  Saracuruna lines and left the rest out. Rail is OpenStreetMap's everywhere
  but Rio's metro, which is the city's own layer.

- **Rotterdam** - RET's metro A-E and nine tram lines, inside the gemeente. The
  Netherlands' second city: Amsterdam's shape, with the food layer REBUILT
  rather than read. Rotterdam publishes no hospitality register, but every
  exploitation permit it grants is a notice in its official gazette with a
  point, and a permit runs five years - so the premises are the places with a
  grant inside that term, sorted by each notice's own title (three title forms
  over five years) and merged where they share a place. Tested on Amsterdam's
  live register, the method finds almost every premises and overcounts about
  one in seven, and the page says so. Shops and services are BAG shop units,
  as in Amsterdam. **Its rail is measured on the timetable after a works
  period**: the national feed's window opened on works that shorten three tram
  lines, and two temporary lines that fill the gap had looked like permanent
  ones - neither of RET's own maps carries them.

- **Hong Kong** - MTR's eight urban lines and the Light Rail, across the SAR,
  and the first city in the **East Asia** region. The business leg is FEHD's
  licence registers, which cover food premises and a few specified trades but
  no general retail, so the map is mostly restaurants and the page says so.
  **It needed no geocoder after all**: the brief planned an address lookup for
  every licence, and reading that service's terms turned up FEHD's own points
  for the same registers on the Government's spatial data portal, joined by
  licence number. Rail is OpenStreetMap's, because MTR publishes station lists
  without locations; those lists are gate 3.

**Canada is closed at five built cities** - Vancouver (regional, with Surrey),
Montréal, Calgary, Edmonton and Toronto - out of six candidates screened. The
sixth, Surrey, is not pending: it shipped inside the Vancouver regional map.
Final per-station densities, all on one comparable basis: **Vancouver 206,
Montréal 151, Calgary 137, Surrey 135, Toronto 81, Edmonton 79.** Three of those
six numbers moved during the builds, two of them by more than 1.8x, every time
because a station count or a denominator was wrong rather than because the data
changed.

**Mexico is complete at two cities**, and it is the first country here built on
a NATIONAL register rather than municipal ones: INEGI's DENUE, downloaded per
entidad federativa, covering every city. That shape produced
`pipeline/countries/mexico.py` - the country/city config split, done at the
second city on purpose, because one city cannot show which of its settings are
national. What did NOT generalise between two cities in one country is the more
useful half: the projected CRS, the municipio scope, and the OSM station
tagging itself (Mexico City has 184 `railway=station` nodes; Guadalajara has
one, its stations being `railway=stop` positions).

**Neither Mexican city uses GTFS**, which makes OpenStreetMap a second rail
source rather than a one-off. `.claude/skills/osm-rail/` carries when that is
justified, how to derive stations from route-relation membership rather than
node tags, and the traps - entrances outnumbering stations, proposed stations
misspelled `prpopsed`, an unbounded name search matching Guadalajara, Spain.

**Spain is complete at two cities**, out of six screened - Valencia, Bilbao and
Málaga measured out and Sevilla unreachable - and it is the country that proves
a shared language and a shared classification family are not a shared build.
Madrid and Barcelona have different rail sources, different projected CRS, and
key identically-shaped four-level taxonomies at opposite ends, each decided by
measurement, which is why there is no default for the next city to inherit.
`docs/spain_retrospective.md` is what that cost. **Ireland and Italy are one
city each**, and Italy needed no country profile at all: its registers are
municipal, so what a profile would establish is per city anyway.

**France is complete at five cities: Paris, Marseille, Toulouse, Lille
(Regional) and Rennes.** It is the first country here where each city was materially cheaper
than the last - one national register, one national taxonomy module, one
national grid, one shared extract cache and one shared step 2, so Marseille's
own work was a scope measurement and a rail leg, and Toulouse downloaded
nothing but a feed and a boundary. What does NOT transfer is the more useful
half, and it is the same list each time: the scope decision, the ring edges,
the spacing floor, gate 3's source, and the catch-all's share. Lyon is
discarded on four independent blockers - an account required before any
download, an open-ended indemnity, a marks clause colliding with the invariant
that every drawn line carries its real public name, and a feed dead behind the
national access point - while Toulouse's and Rennes' terms were read the same
day and are clean, so those clauses are that métropole's own rather than a
French pattern. **Scope is the one thing decided city by city, on one
measure: the worst line's station survival inside the commune.** Lille's
tram kept 3 of 36 and it went regional; Toulouse's T1 kept 13 of 25 and
Rennes' Métro b 11 of 15, and both stayed commune-only. SIRENE is one
national file, so regional is a wider filter, never a new source. **All
five are deployed**; the city-scoped `deploy-verify` deferred to the last
French city ran before Rennes merged, and passed.

**The macro map is regional, and a region is whatever groups cities into one
readable view** - not a country. They are Global (the landing view, a
COMPOSITE of every leaf), United States (a composite of West and East), United
States West, United States East, Canada West, Canada East, Mexico, Europe and
South America. Each is fitted to its own cities, so switching region zooms as
well as re-centres - except Global, which opens on the United States frame. A
city carries exactly one region tag and a composite is resolved at lookup;
tagging a city with a composite is an error the validator names. A region
labels only its own cities, composites included - a parent drawing every
city's name is a collision class that grows with the map rather than with any
defect. **Global is the one exception, by the owner's decision**: it labels
every city, accepting that Europe and South America cluster at the edge of a
wide screen, and `check_macro_labels.py` holds it only to the cities in its
opening frame.

**Europe is one region, not one per country**, and it was briefly the other
way: three regions held four cities before they were collapsed, which is what
let France arrive without adding more. Note what this is not. North America is
split because those countries are thousands of kilometres wide and a single
frame shows a continent rather than a city; Europe's cities frame together at a
zoom where each is still distinguishable. Revisit it when a city appears far
enough east or south to force the frame open - that is a measurement
(`scripts/check_macro_labels.py` scores every city in every region at three
widths), not a judgement.

**The deployed app must be REBOOTED, not merely updated, after any push that
changes a module it imports.** Streamlit Cloud's "Updated app!" re-runs the
entry script and leaves `sys.modules` as it was at boot, so a new name in
`app/cities.py` breaks the live site until a reboot - it cost three hours of
downtime on 2026-09-22. `app/cities.py` changes with every city.
`python scripts/check_deploy_imports.py` tests a clean clone under the lean
venv before pushing; it cannot catch the stale-module case, and says so.

**Norway, Denmark and Czechia have one city each - Oslo, Copenhagen and
Prague - and each country's national modules** - the register facts, a
shared step 2, a NACE Rev. 2.1 taxonomy (SN2025, DB25, CZ-NACE 2025) and a
national cache for the register files - **are written for a second** on
France's pattern. Czechia is
paused at Prague, whose register records registered seats; the staging
session is measuring whether the trade register's establishments can
replace it.

**Brazil is built at nine cities, and it is the first country built as a
batch** - every city to drafts, one review of all the text, one deploy check
and one push. The national modules (`pipeline/countries/brazil*.py`) were
written with São Paulo; each further city was a config, its rail step and
three thin steps. What did not transfer is the usual list: the scope (four
regional pages, two of which keep a município with no drawn station because
its only line failed the rail test), gate 3's source (a stale agency layer or
Wikipedia table, corrected and recorded in three cities), and each city's
rail. The `brazil-city` skill carries the traps, and
`scripts/measure_rail_backbone.py` answers two of the rail test's three parts
from cached OSM.

Next is Taiwan, after Hong Kong (the owner built Hong Kong first on 2026-09-24
so the week's remaining budget held a whole city; the order before that was
Rotterdam, then Taiwan).
Taiwan and Japan each get a per-country skill written after their first city.
The two renderer fixes Brazil's deploy check found go first: the owner gated
the next deploy on them. New
Orleans and Seattle remain deferred, both needing decisions before code. Take
the candidate ordering from `docs/city_master_list.md`, which is current state;
`docs/global_country_shortlist.md` is its evidence trail, and the `add-country`
skill is the process.

**Briefs are now executable.** `scripts/brief_check.py <city>` re-runs a
brief's factual claims against the live sources, from a fenced
```brief-checks block beside the prose. It exists because Edmonton's build
inherited three wrong claims from its brief and the MEASURED/ASSERTED labels
did not stop it. Nearly every brief now carries a checks block, and the script
run with no city argument runs all of them. A failing check is a brief to
correct, not a check to relax.
**Check a candidate's registry actually covers all three buckets before
assuming one source is enough** - that assumption failed for New York, and in
Philadelphia a whole bucket had no source at any level of government. See
`city_shortlist.md`, `data_sources.md` (every source's endpoint and filter) and
`PLAN.md`. Row counts, station counts and per-run figures are in
`DECISIONS.md`.

**Published names are screened, not trusted.** `render_heatmap` drops any row
whose displayed name carries an email address or phone number - enforced in the
shared renderer so a city added later cannot reintroduce it - and
`scripts/check_personal_exposure.py` reports contact details, surname-first
names, person-plus-trade composites and `ATTN:`/`c/o` markers alongside the
person-name heuristic. Its one known blind spot is a sole trader at a detached
house, which carries no unit indicator to detect.

**Navigation.** The Overview is the macro map: a pydeck map (pydeck ships
with Streamlit; no folium) with a labelled marker per city, where clicking a
marker opens that city's page (`st.switch_page`), plus a plain link list as a
fallback. In the map-only pilot (`MAP_ONLY_NAV` in `app/cities.py`) the sidebar page
list and the city switcher are hidden, and each city map has a "Global View"
button back to the macro map; with the flag off, every city page has a switcher
row to jump to another city or back to the map (see
`docs/navigation_sidebar_and_city_links.md`). The city list lives in `app/cities.py`.

Not built yet: a shared pipeline-side city registry. The site is deployed, and
the reboot rule above is what keeps it up.

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
- **Publish commercial information, not personal information.** Each pin
  carries a business name at a precise coordinate, so a city whose registry
  lacks trade names will otherwise publish registrants' own names at what may
  be their homes. `scripts/check_personal_exposure.py` measures this per city;
  catch-all classification codes are the usual culprit (Los Angeles excludes
  NAICS 812990). A trade name is public commercial information and stays.
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
