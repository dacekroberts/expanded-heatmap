---
name: add-city
description: Add a new city to the expanded-heatmap project - live-verify its real data sources, scaffold its pipeline, build its transit/business heatmap, and wire it into the Streamlit app. Use whenever the task is "add city X" or "build out city X" for this project, not for edits to an already-built city.
---

# Adding a city to expanded-heatmap

Distilled from the four cities actually built (San Diego, San Francisco, Los
Angeles, Chicago) - not a hypothetical plan. Every step either caught a real problem or is a
design decision already made (see `docs/project_context.md`; the reasoning
trail is in `DECISIONS.md`). If this is a fresh session, read those, plus
`docs/city_shortlist.md` and `PLAN.md`, first.

## Step 0 - Live-verify data BEFORE writing any code

**The step that matters most.** Denver and San Jose both looked viable from
search summaries and dataset titles, and both had no usable data on direct
schema verification. Do this for every candidate before scaffolding:

0. **Open the portal in a real browser first.** Before any `curl`, load the
   site and watch what its own UI calls. This is a standing rule, not a
   fallback for when fetching fails - see `add-country` §3, where five portals
   in one sweep each gave up in one page load what rounds of path-guessing had
   not: a sign-in wall (GeoMedellín), a server-rendered catalogue with no API
   at all (`data.gov.my`), a DKAN install whose CKAN path needed the `3`
   (Peru), and two real API roots read straight off the network panel (Seoul,
   Jakarta). Guessing tells you a path 404s; navigating tells you what the
   portal *is*.

1. **Business data.** Find the real open-data portal and pull the *live*
   schema, not a description page. Socrata: `curl -s "<domain>/api/views/<id>.json"`
   for columns, then `<domain>/resource/<id>.json?$limit=3` for sample rows.
   ArcGIS FeatureServer: `<service-url>?f=json` for fields, then
   `<service-url>/query?where=1=1&outFields=*&resultRecordCount=3&f=json`.
   CKAN: **`<domain>/api/3/action/package_list`, printed in full and read** -
   never `package_search?q=<terms>`, and never a keyword filter over the full
   list either. Search hits and keyword greps both miss the dataset that is
   named in the city's own vocabulary rather than yours. Boston proved the
   first half (48 packages from seven search terms; 247 from `package_list`,
   and the extra 199 held the boundary layer, the address points and the
   property roll). Montréal proved the second on 2026-09-21: a keyword scan of
   the full 447-name list wrongly concluded the city was food-only, because
   **`locaux-commerciaux`** - a 28,621-row, agglomeration-wide field survey of
   street-level commerce with NAICS (`SCIAN`) codes, 100% coordinates, trade
   names and a vacancy flag - contains none of the words *business*, *licence*,
   *permis*, *entreprise* or *commerce*. Nor does `unités d'évaluation
   foncière`, the property roll that would serve as its residence-check join.
   Printing ~450 names costs about a minute and ~3 KB of context. Read them.
   Also record the **source encoding** as `SOURCE_ENCODING` in the city's
   config (see `docs/data_sources.md`) - declared, never inferred. Confirm, with
   real non-null sample values: (a) *some* classification field - NAICS or
   the city's own taxonomy, both fine; and (b) a street address and/or
   lat/long that actually has data, not merely a column that exists. Also
   note whether the data ships pre-geocoded (both San Diego and San
   Francisco do) and whether it has an "active" flag or an end date to
   filter on. **Also check how often the trade-name column is blank**, and what
   the pipeline would fall back to: Los Angeles has no `dba_name` on 68% of rows,
   so it fell back to the registrant's own name and would have published ~4,000
   individuals' names at their premises (see Step 5 and `DECISIONS.md`,
   2026-09-21 "Privacy line"). A registry that nearly always carries a trade
   name (San Diego, San Francisco, Chicago) has no such problem. Then check *validity*, not just population: count how many
   coordinates fall inside the city's bounds and look at the ones that
   don't. A populated field can still be corrupt - Los Angeles' registry had
   ~9% bad coordinates (longitude copied from latitude, (0,0), whole-degree
   placeholders), concentrated in recent registrations. **Madrid's premises
   census is the second case and the worse one: `coordenada_x/y_local` are
   non-empty on 100% of rows and 20% of them are a literal `0`.** Two of the
   three pre-geocoded registries measured at this depth had the same defect, so
   run the bounding-box count **on every city, before quoting its density** -
   Madrid's headline would have been a fifth too high, and the bad rows vanish
   off-map rather than raising an error. And look at what the
   dataset's city field actually holds: LA's holds postal community names
   (Van Nuys, San Pedro...), so an exact match keeps about half the city;
   find the authoritative in-city marker (LA's `council_district`) instead.
2. **Transit data.** Find the real GTFS feed URL and confirm it downloads
   and unzips (`curl -sL <url> -o gtfs.zip`). A URL from search can still
   time out or 404 - San Francisco's official feed host timed out from this
   environment and a mirror linked from the agency's own page worked.
   **Screening several candidates at once? Run `scripts/screen_rail.py`
   first, before any business-data research.** Rail is the cheapest
   disqualifier here - a city with no urban rail is out however good its
   registry turns out to be - and the script reads `route_type` counts
   straight from each agency's live `routes.txt`. It removed 6 of 13
   Canadian cities in one pass on 2026-09-21, before a catalogue was opened.
   Feed URLs come from the Mobility Database catalogue (`bit.ly/catalogs-csv`),
   one CSV covering most of the world's feeds. Three traps it exists to catch.
   **A catalogue mirror can be STALE and silently missing an entire mode** -
   the Mobility Database copy of Toronto's TTC feed was three months expired
   (`feed_end_date 20260606`) and contained **no subway at all**, only 17 trams
   and the shuttle buses; the screen read that as "Toronto codes its subway as
   route_type 0", which is **false**. The agency's own feed has 3 subway lines
   as `route_type 1`. `screen_rail.py` now prints each feed's expiry and flags
   stale ones: heed it, and prefer the agency's own feed. Separately,
   **an agency may genuinely code its subway as `route_type 0`** (San
   Francisco's Muni Metro does, so a high type-0 count is a prompt to read the
   route names, never a finished answer), and **a regional feed covers cities
   with no rail of their own**
   (TransLink's carries Surrey's SkyTrain stations). Commuter rail
   (`route_type 2`) is not counted, matching every city built so far.

   **Check `feed_info.txt` for a validity window, on the feed you will
   actually use.** WMATA declares `feed_start_date`/`feed_end_date` **ten days
   apart** - the shortest here, short enough that a stored copy goes stale
   inside a fortnight. Where the window is short, that city's
   `fetch_sources.py` must re-check `feed_end_date` on EVERY run, including
   runs that skip the download, and treat an expired copy as an error rather
   than a warning. The failure mode is silent: an expired feed still parses,
   still has the right station count, and still builds a map - it is just not
   the current network. See `pipeline/washington_dc/fetch_sources.py`. (This is
   the same field `screen_rail.py` prints for staleness; the difference is that
   screening reads it once and a build must re-read it forever.)

   **If the feed needs a key** - WMATA is the only one so far, returning 401
   unauthenticated - read it from an environment variable, exit with
   registration instructions when absent, and **never echo it, not even in an
   error message**, so the 401 path prints "the key was rejected" rather than
   the key. It is the agency's property and stays out of the repo. Record in
   `docs/data_sources.md` that the city cannot be rebuilt from a clean checkout
   without it.
3. **City boundary polygon.** Find a real GIS boundary layer (a regional
   MPO/COG portal is often the source, e.g. SANDAG). Not optional: San
   Diego's Trolley serves six other cities and 16 of 63 stations were
   outside city limits, several not guessable by name. Eyeballing a station
   list is not a substitute for any system with several lines or one that
   plausibly crosses municipal borders.

Only proceed once all three are confirmed live. If a city fails, record the
real reason (cite the endpoint and response) in `docs/city_shortlist.md` and
a `DECISIONS.md` entry, and move to the next candidate.

**Give every probe an explicit output path under the session scratchpad.** The
commands above are `curl`/`requests` dumps, and `-o la.json` writes wherever
the shell happens to be: the 2026-09-18 screening left eight captures in the
home directory, including a saved 404 and a file named `.json` that was HTML.
Write probe output to the scratchpad (or a gitignored `data/<city>/raw/`), and
put the *findings* in `docs/data_sources.md` and `docs/city_shortlist.md` - a
raw capture is not a record, and it goes stale the moment the endpoint changes.

**Record every confirmed source in `docs/data_sources.md` as you verify it** -
endpoint, the server-side filter applied at download, and the date. That file
is the project's master provenance list and the only way a build can be
reproduced, because raw downloads are gitignored. Do it now, while the
endpoints are in front of you: recording them later is how San Francisco's
boundary layer ended up with no recorded URL at all. If an endpoint you tried
is dead, record that too, with its date - a replaced URL that leaves no trace
hides the fact that dataset IDs get retired.

4. **Licence and required notices, per source, in the same pass.** A city is
   not verified until this is recorded in `docs/data_sources.md` alongside its
   endpoint. **Use the `read-licence` skill** - it carries the procedure plus
   the three corrections that motivated it, each of which came from not opening
   a page an earlier review had merely cited. The two steps most easily skipped:
   grepping the dataset page for terms incorporated **by reference**
   ("constitutes acceptance of the license, **the City's terms of use** ..." is
   how Philadelphia's prohibition was hiding behind a licence that forbids
   nothing), and asking of every document whether its language describes **web
   pages or data**. "It's on a government open-data portal" is not an answer: the
   2026-09-21 review found terms ranging from public-domain dedications to a
   feed that forbids modifying its data, and both extremes inside Los Angeles
   (its business registry is CC0; its GTFS is the most restrictive licence in
   the project). For each source capture:
   - **The declared licence.** Socrata exposes it directly - fetch
     `<domain>/api/views/<id>.json` and read `license`, `licenseId`,
     `attribution` and `attributionLink`. `SEE_TERMS_OF_USE` means go read the
     terms page; a missing `license` does NOT mean permissive.
   - **The governing terms where no licence is declared.** Look for a portal
     terms document, not the parent site's general footer - that mistake made
     NYC look prohibited when Local Law 11 in fact *forbids* it from imposing
     a licence, while the nyc.gov footer's "All Rights Reserved" covers only
     that website's own content.
   - **The transit feed's own terms, separately.** `feed_info.txt` almost never
     carries a licence (LA Metro's has an empty `feed_license` column), so go
     to the agency's developer terms. Line geometry is redrawn from
     `shapes.txt` into the map, so these bear directly on what is published,
     and they were the loosest end of the whole review.
   - **Anything the project must DISPLAY.** This is the part that becomes work
     rather than a note: Chicago requires a verbatim disclaimer, SFMTA
     requires specific attribution wording, LA Metro requires acknowledgement
     as provider. Add any new one to the "Notices this project MUST display
     when published" section - that list gates the public deploy.
   - **Anything that needs a human decision**, such as a purpose limitation or
     a bar on modification. Raise it rather than reading the clause
     generously, record the verdict and its reasoning in `DECISIONS.md`, and
     attribute the call.

   If a page blocks automated fetching (Chicago's data terms return 403), use
   the browser rather than giving up or guessing - every item in that review
   was resolvable that way except one.

   The standing commitment in `docs/data_sources.md` - that removal requests
   are honoured without argument - covers new cities automatically. Do not
   weaken it for a source with tighter terms; the answer to tight terms is to
   record them and comply, not to hedge the commitment.

**THE DOWNLOAD BOUNDARY IS THE PRIVACY CONTROL, where the source lets you
choose columns.** Do not download a personal-name column and filter it later -
omit it from the request, so it is never on the machine to leak into a
processed file, a cache or a commit. Washington D.C.'s ArcGIS query names 16
`outFields` and omits eight that exist and are populated on tens of thousands
of rows: `BUSINESSOWNERFIRSTNAME`, `BUSINESSOWNERLASTNAME`,
`BUSINESSOWNERMIDDLENAME`, `AGENTFIRSTNAME`, `AGENTLASTNAME`,
`AGENTMIDDLENAME`, `AGENTENTITY` and **`BILLINGADDRESS`** - that last being a
mailing address, i.e. frequently a home. Boston does the same in SQL; Miami
omits `OWNERNAME` and every `MAIL*` field.

Then **assert in step 2 that they stayed absent**, and have the fetch script
exit if the server returns a column it did not ask for. The assertion is what
makes the omission a guarantee rather than an intention.

**One source need not be enough - and for most large US cities it is not.**
Pull the category *distribution* here, not just the schema, and read it against
the three buckets: could a reader find a restaurant, a grocer, a clothes shop
and a hairdresser in this data? New York's recorded source held zero
restaurants, grocery, clothing or salons; 79% of Philadelphia's active licences
are residential landlord registrations. Both passed a schema check and answered
a different question, and a big row count hid it in each case.

**Pull SEVERAL pages before concluding anything, and never judge a register by
its first record.** A register is ordered by identifier or registration date,
so page one is systematically the *oldest* entities - holding companies,
dormant shells, long-established corporates - and is the least representative
sample it can give you. Finland was ruled out of the 2026-09-21 country screen
on exactly one record, the first the API returned: a financial holding company
with an empty street, a PO box and a `c/o` accounting firm. Counted across 500
instead, **89.8% carried a real street address**. The ruling was reversed and
the reason for it had been false. The cost of doing this properly is one loop.

**If any bucket comes back empty or thin, use the `multi-source-city` skill**
(`.claude/skills/multi-source-city/`). It carries the diagnosis, the source
archetype per bucket, the dispatching-taxonomy architecture, the cross-source
dedup rules, and - the part most easily skipped - the licence and privacy
checks that every added source multiplies.

If it passes but the build won't start right away (a usage limit, a new
session), turn what the probe found and left open into an ordered checklist
under that city's item in `PLAN.md` before stopping. Write it from the
findings, not from a template: it holds only what is specific to this city
(catch-all license types, adjunct licenses, scope decisions, checks still to
run), and points back to these steps for everything generic. Chicago's is the
model. Skip it when the probe and build happen in the same session.

**If the city has a brief, run `python scripts/brief_check.py <city>` now** -
before Step 1, before any code. It re-runs the brief's factual claims against
the live sources and prints got-against-expected. It exists because Edmonton's
build inherited three wrong claims from its brief (a *recommended* GTFS path
that was stale, a `feed_info.txt` said to be absent that is present, and "no
required notice" where a redistribution clause applies) plus a station count
that was 33 where 30 was right. All four were cheap to check and none was
checked, because the brief's prose had already turned its own ASSERTED labels
into recommendations.

Add checks for whatever you newly verify in Step 0, in the brief's
```brief-checks block. The kinds that exist map onto this project's actual
failures - `gtfs_stations` measures platforms, the parent_station collapse, the
boardable count and the spacing median in one call; `socrata_distinct_split`
separates true categories from delimiter combinations; `geojson_area_km2`
catches a same-named stale boundary layer. A failing check is a brief to
correct, not a check to relax.

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

**AND MATCH ON `route_short_name` WHERE THE FEED VERSIONS ITS IDS.** Calgary's
`route_id` embeds the feed release: `201-20780` in the Mobility Database
mirror, `201-20786` in the agency's own feed. A config pinning the id matches
NOTHING after the next release, and matches nothing *silently*.

### A STATION COUNT IS THE MOST ERROR-PRONE NUMBER IN THIS PROJECT

**Five of the project's denominator errors have been station or percentage
counts, and two were platforms counted as stations.** Both survived review
because the wrong number was plausible:

- **Toronto**: the "234 stations" behind its ranking figure was 234
  PLATFORMS - 118 stations. Its density was 41 per platform, i.e. **81 per
  station**, which moved it from last of six to fourth.
- **Calgary**: "83 stations" was 83 PLATFORMS - 45 stations. 75 per platform
  is **138 per station**, moving it from fifth to third.

**THE CHECK THAT CATCHES IT IS THE SPACING MEASUREMENT, NOT A DUPLICATE-NAME
ASSERTION.** Calgary's step 1 asserted no two stations share a name and
PASSED, because `NB Banff Trail CTrain Station` and `SB Banff Trail CTrain
Station` are different strings. What caught it was the nearest-neighbour
median: **17 m, with a minimum of 8 m**, which is physically impossible for
rail stations.

So: **print the nearest-neighbour distribution before trusting any station
count, and treat a median under ~100 m as platforms until proven otherwise.**
For calibration, every real figure measured so far - San Francisco's thinned
street-running median was **134 m**, Montréal 728 m, Vancouver 841 m, D.C.
962 m, Calgary after collapsing 1,023 m.

**Four collapse mechanisms, in descending order of reliability:**

1. **`parent_station` is populated** - the clean case. Collapse on it and
   assert it is non-null on every served platform. D.C. 125 platforms -> 98,
   Montréal 72 -> 68, Edmonton 65 -> 33. **Take the DISPLAY name from the
   CHILD stop**: Montréal's parents are upper case (`STATION ANGRIGNON`) and
   its children mixed (`Station Angrignon`), and an all-caps label reads as
   shouting on a map.
2. **A regular suffix** - Vancouver's `<Station> @ Platform N`. Regex it, and
   **assert every name containing the marker actually matched**, so a new
   suffix form fails loudly instead of inventing stations.
3. **A direction PREFIX and no `parent_station`** - Calgary's `NB|SB|EB|WB`.
   This is the dangerous one, because each name is unique and nothing looks
   wrong.
4. **Nothing at all** - Toronto: 234 stops named `Finch Station - Southbound
   Platform`, no `parent_station` column. Normalise by hand and check the
   result against the operator's own published station count.

**Always sanity-check the collapsed count against the operator's published
figure.** Calgary collapsed to exactly 45, which is the CTrain's real station
count; that agreement is what turns a regex into evidence.

### Normalising station names: the traps, all of them real

- **A typo in the feed.** Calgary ships `CTrain Staion` alongside `CTrain
  Station`.
- **Several suffixes for one system.** Calgary uses `CTrain Station`, `CTrain
  Stn`, `Station (Free Fare Zone)` and bare `Station` in one file.
- **Inconsistent spelling BETWEEN THE TWO DIRECTIONS OF ONE STATION.**
  Calgary has `EB Downtown West-Kerby Station` and `WB Downtown-West Kerby
  Station` - the hyphen moves. Normalise hyphens to spaces before comparing.
- **Legitimately single-platform stations that must NOT be merged with a
  neighbour.** Calgary's 7 Avenue downtown is a ONE-WAY COUPLET: `EB 3 Street
  SW` and `WB 4 Street SW` are different places, one direction each. Seven of
  its 45 stations are like this. Collapsing by normalised name handles it
  correctly; collapsing by proximity would not.
- **The opposite error: over-stripping.** Boston's bug turned `North Station`
  into `North` by removing a trailing token. Strip a LEADING prefix in
  preference to a trailing one, and never strip a bare trailing word without
  checking the whole list first.

### Non-English and non-Latin names: what to expect next

The project has met three of these already and should expect more:

- **Dash variants are a silent join killer.** Montréal's commercial survey
  writes `Ahuntsic–Cartierville` with an EN DASH where the City's own boundary
  layer writes `Ahuntsic-Cartierville` with a hyphen. Six of its borough names
  differ this way, which made a 34-feature layer look like it covered only 32.
  **Normalise U+2013/U+2014 to U+002D before any join.**
- **Apostrophe variants likewise.** `L’Île-Bizard` (U+2019) against
  `L'Île-Bizard` (U+0027).
- **Case differs across sources for the same name.** `Baie-d'Urfé` against
  `Baie-D'Urfé`. Use `casefold()` rather than `.upper()`, which is wrong for
  some scripts, and apply **Unicode NFC** so that a precomposed `é` and an
  `e`-plus-combining-accent compare equal. Two files can look identical and
  not match.
- **Direction and platform words are language-specific.** A `NB|SB|EB|WB`
  regex is an English-feed assumption; expect `Direction`/`Sens` (French),
  `Richtung` (German), `Sentido`/`Andén` (Spanish), `Binario` (Italian).
  Derive the pattern from the printed name list, never from a template.
- **GTFS has `translations.txt`, and some feeds ship it.** TransLink's and
  STM's both do. Where a feed carries a non-Latin script, that file is where a
  romanised name lives - prefer it to transliterating by hand, and record
  which language the displayed name is in.
- **Business names stay in their own language, always** (an `add-country`
  rule). Only the bucket labels are translated, and those belong to the
  taxonomy module.

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

**Check whether the city has a property register you can join to, and read the
result carefully.** The residence test in `check_personal_exposure.py` only
fires on an `APT`/`FL`/`RM`/`#` indicator, so a sole trader at a detached house
reads as clean. Where the registry carries a parcel id (Philadelphia's
`opa_account_num`), an assessor/property layer usually carries the city's own
land-use category and an owner-occupancy flag, which tests directly for a
business at a home. Tested on Philadelphia 2026-09-21, with three lessons that
save repeating the work:

- **A mailing address matching the premises is NOT a signal.** It matched 41.9%
  of mapped pins - a shop's mailing address is normally its own premises.
- **Land use alone is not a signal either, and this is the important one.** In a
  dense city, shops sit inside residential buildings: "purely residential
  parcel" flagged 7.95% of Philadelphia's pins, including 147 thirty-plus-seat
  restaurants on `APARTMENTS > 4 UNITS` parcels. Filtering on it would delete
  hundreds of real storefronts. Mixed-use parcels in particular - the rowhouse
  with a shop below and a flat above - are the most characteristic storefront
  in some cities, and their owners often claim an owner-occupancy exemption on
  them.
- **Combine a name or entity-type signal with an occupancy one.** A person-like
  name AND an individual entity AND (a purely residential parcel OR an
  owner-occupancy exemption) gave 0.39%, against the 0.00% the unit indicator
  reported. Treat what it finds as a **scope** question first - a home food
  business is not a storefront - which is easier to justify and fixes both.

**Sample the catch-all classification codes for this city, and decide.**
`pipeline/taxonomies/naics.py` lists the NAICS catch-alls (812990, 812930,
459999) and why each needs a per-city verdict; a local taxonomy has its own
equivalents (Chicago's "Limited"/"Regulated Business License"). These codes sweep
in home-based sole proprietors, which is both a data-quality problem (not
storefronts) and a privacy one (a person's name at their home on a public map).
Put the verdict in the city's own config as `NAICS_EXCLUDE_CODES` (Los Angeles is
the worked example), applied as its own printed filter in step 2, and record the
sample and reasoning in `DECISIONS.md`.

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
both in the browser.

**Line colours: separate them WITHIN the city, and reuse freely across
cities.** If the agency's official colours are ambiguous, shared, or collide
with the three business-category pin colours, use your own palette. What has to
be distinct is (a) each line against the category colours that map spends, and
(b) each line against the other lines on the *same* map. **Nothing has to be
distinct across cities.** Each city renders its own map with its own legend and
its own on-map labels, so two cities sharing a red can never be confused;
Edmonton's Metro Line is deliberately the same red as Calgary's Red Line. Do
not spend effort keeping every line in every city unique — the usable palette
runs out long before the city list does, and the cost lands on later cities as
colours that read badly against their own pins, which is the constraint that
actually matters. Only the macro map shows every city at once, and it draws
city dots rather than transit lines.

The separation is **measurable, so measure it** rather than judging by eye.
This project's working threshold is a CIE76 Delta-E of about **45**, the figure
behind `#C2185B`'s selection (49.6) and `#FBB878`'s (44.8) in `map_common.py`.
Edmonton is the worked example: ETS signs Capital blue and Valley green, which
scored 23.9 against Retail's `#2a78d6` and 37.2 against Personal services'
`#1baf7a`, so each line kept its hue and was darkened until it cleared. Where
no combination clears the threshold — green-against-green is the hard pair, and
Edmonton's Valley Line settled at 44.2 — say so in the config as a tradeoff
rather than leaving it to look like an oversight. Worth knowing before trusting
an existing city: **Calgary's shipped Blue Line is Delta-E 3.3 from Retail
blue**, which is effectively the same colour and was never measured.

## Step 7 - Run it for real, then look at it

Run steps 1-3 and read the counts. Then **run
`python scripts/check_personal_exposure.py <city_slug>`** (add the city to its
`REGISTRIES` table first: the trade-name and fallback columns are per registry).
It reports how many pins show a registrant's name rather than a trade name, how
many look like an individual's name, and how many of those sit at an address with
a unit indicator. There is no pass mark - read the numbers, decide, and record the
verdict in `DECISIONS.md`. The project's line: publish public commercial
information, not personal information. Then open the rendered map in a browser
before calling it done: serve `outputs/<city_slug>/` (or use the
`deploy-verify` agent's `heatmap-static` config) and confirm the heat layer,
rings, line labels, legend and clustered pins render over real geography,
with no console errors. A pipeline that runs cleanly is not a map that looks
right.

## Step 8 - Wire into the app

- `app/pages/N_<City>_Heatmap.py`: the static-HTML-embed pattern
  (`st.iframe(HEATMAP_HTML, width=1000, height=650)`, fixed size matching the map; not the deprecated `st.components.v1.html`), not
  `streamlit-folium`. Call `components.set_base_font()`.
- Add the city to the `CITIES` list in `app/cities.py` (name, marker lat/lon,
  page path, blurb). That one entry feeds the clickable macro map on the
  Overview, its fallback link list, and every city page's switcher. In the
  new page, call `components.render_city_nav("<City name>")` (in the map-only
  pilot it renders only the hidden link the map's "All cities" button clicks, so
  never omit it) (the name must
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
- **Confirm the city's licence rows are actually in `docs/data_sources.md`**
  (Step 0 item 4) before calling the city done - endpoint, filter, retrieval
  date, licence, and any notice the source requires. A city whose data is
  mapped but whose terms are unrecorded is not finished, because the gap is
  invisible afterwards: it looks exactly like a city that was checked.
- Keep the honesty convention: mark what's verified vs. still a skeleton.
