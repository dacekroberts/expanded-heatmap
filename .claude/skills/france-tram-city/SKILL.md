---
name: france-tram-city
description: Build a French tram city - the 21-city France batch (Angers built mark-free) - on what Paris, Marseille, Toulouse, Lille and Rennes built - the SIRENE chain and its traps, the tram leg from each city's own rolling feed (mode flags lie), the owner's pure-extract station rule, the commune-or-regional scope call, 0.3 mi rings, the notices per licence, the page text the owner approved word for word, and a sheet per city. Use for any French city after Rennes, with scripts/scaffold_france_batch.py and the city's brief; read with add-city, osm-rail and publish-city, which it does not replace.
---

# Building a French tram city

Written 2026-09-30 by the France kit session, from the five French cities
already built (Paris, Marseille, Toulouse, Lille, Rennes: `DECISIONS.md`
2026-09-22 to 09-24) and from a live read of the batch's 20 feeds that day.
France is **Mexico's shape**: one national register (SIRENE), one national
geolocation file, one national boundary API. So a French city costs its rail
leg, a scope call and its notices. Everything else is shared code.

**The batch** is the 20 French T1 cities in `docs/tram_city_list.md`:
Montpellier, Nice, Strasbourg, Bordeaux, Nantes, Grenoble, Rouen,
Saint-Étienne, Dijon, Tours, Le Havre, Mulhouse, Reims, Caen, Brest, Besançon,
Orléans, Le Mans, Avignon and Valenciennes. **Angers, the 21st, is built
MARK-FREE** (owner, 2026-09-30). It was held until the other 20 were built,
because its Métropole's terms bar the network brand "and any other mark"
without consent. So:
- every surface the app shows names **Angers Loire Métropole**: the page, the
  macro label, the city entry, the caption (`france_page.py`'s
  `PRODUCER_ONLY`) and notice 77;
- the lines are **Tram A, B and C**;
- the feed's publisher and agency fields are never shown;
- notice 77 names the database by producer and NAP id, because the title and
  the page slug carry the brand.

Grep `app/`, `outputs/angers/` AND the docs the app renders - `docs/data_sources/`,
`docs/data_sources.md`, `docs/excluded_categories.md` - for the brand after any
rebuild: the About the Data page shows `docs/data_sources/france.md` verbatim,
and its Angers row named the brand until review lanes 1 and 4 caught it
(2026-09-30). Only `provenance.json`, the fetch record, may carry it.

**Builds are APPROVED** (owner, 2026-09-30), in landing groups per
`docs/review_time.md`, with every brief's calls approved as recommended.
Build on a branch, never on master: `app/` lands at review time only.

## Order of work for one city

1. `python scripts/brief_check.py <slug>`. A failing claim is a brief to
   correct. The GTFS cache refetches after 7 days, so this reads the
   build-day feed.
2. Read `docs/build_briefs/<slug>.md`. Its "For the owner" table is what the
   owner approves with the build: `mode`, `coverage`, scope, lines and any
   owner call. Bring the calls to the owner before writing code.
3. `python scripts/scaffold_france_batch.py --only <slug> --dry-run`, then
   `--go`. This writes the French `config.py`, three-line `fetch_sources.py`,
   step 1, step 2 and step 3 over the shared module, and (through
   `scaffold_city.py`) `__init__.py`, the app page and the `app/cities.py`
   entry.
4. `python pipeline/<slug>/fetch_sources.py` (always a fresh feed; one
   Overpass query), then `python scripts/france_fill_build_day.py <slug>
   --write`. That fills `GTFS_SELF_ATTESTS`, the route_ids, the colours and
   gate 3 from the fresh feed and OpenStreetMap, and prints every value. Read
   what it wrote, settle the public names, and clear every remaining to-do.
5. Steps 1, 2 and 3. A French step 2 peaks at about 0.4 GB (measured): light
   work, no notice needed. Then `python scripts/france_page.py <slug>
   --write` writes the page from the approved template, with every brace from
   the build. `python scripts/france_source_rows.py <slug> --write` adds the
   source rows, and `python scripts/france_excluded_section.py` rewrites the
   batch's section of `docs/excluded_categories.md`. Then the checks under
   "Before publishing".

## What already exists - reuse it, do not rewrite it

| Module | What it does |
|---|---|
| `pipeline/countries/france.py` | The national facts: column names, `STATE_ACTIVE_VALUE = "A"`, the diffusion mask, the geolocation schema, the SHARED cache paths (`data/france/raw/`, 3 GB for the pair, downloaded once for every French city). Imported by every French `config.py`, so it must stay lean-venv importable |
| `pipeline/countries/france_register.py` | **THE step 2**: SIRENE -> the city's storefronts. A city's step 2 is `build_storefronts(config, name, bbox)` and nothing else |
| `pipeline/taxonomies/france_naf.py` | NAF rév. 2 at the sous-classe; national. It deliberately does not decide the catch-alls |
| `scripts/scaffold_france_batch.py` | The batch scaffold: one French config per city from the screen's inputs and the kit's station tables |
| `data/_staging_scratch_2026-09-27/second_cities/france/` | The screen (gitignored): `cities.py`, `gtfs_urls.py`, `bounds/<slug>.geojson` (every commune of the EPCI, with contours), `screen_results.csv`, and `stations_pure_2026-09-30/`, the kit's station tables under the owner's rule |
| `pipeline/rennes/`, `pipeline/lille/` | The nearest built shapes: Rennes for a commune-only city with a boundary that cuts a line, Lille for a regional one |

## The owner's standing calls - do not re-ask

- **Trams-only maps are approved** (DECISIONS "Yes to trams-only maps",
  2026-09-29). With no metro, the trams are the rapid transit (Riga's
  precedent), and every tram stop gets rings.
- **Ring size by the spacing rule**: 0.3 mi outer where the median station
  gap is about 550 m or less. Every city in the batch measured 321 to 510 m.
  **No stop thinning**; Riga's 0.5 mi filter does not carry over.
- **Station tables are pure extracts for every French ODbL feed**: the feed's
  own `parent_station` and coordinates; without one, the first platform's
  coordinates, never a mean; names unchanged. **No data.gouv.fr account.**
- **The currency rule**: the source drops closed businesses (SIRENE's `A`
  does), its newest row is under five years old, and the data date goes on
  the page.
- **The page text is approved word for word** (below).
- **Every French city tags `"region": "Europe"`** today. A France North /
  France South split at latitude 46.5 is recommended and HELD with the
  app/chrome role (handoff section 4). It is not this skill's to make.
- **TER is excluded in every French city; ferries are excluded** (Marseille,
  2026-09-23, recorded as revisitable). **Aerial lifts are drawn**:
  Toulouse's Téléo (owner, 2026-09-23), and Brest's cable car on that
  precedent (owner, 2026-09-30).
- **Approved with the briefs (owner, 2026-09-30, "all eight as
  recommended")**:
  - the scope rule in section 3, which makes Nantes regional;
  - Rouen's `mode` is `light_rail`, with its one page sentence (section 6);
  - the Licence Ouverte same-name rule (section 2);
  - Brest's cable car and Nice's route B are drawn;
  - Le Havre's geometry comes from the Normandie aggregate after a licence
    read, with OpenStreetMap as the fallback. The read found the aggregate's
    shapes stop-to-stop, so it is OpenStreetMap;
  - Valenciennes is built last;
  - builds proceed in landing groups.

## 1. The SIRENE chain - `france_register.py`, with its traps

It reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen, which
is the control. Change nothing in it without re-running one of the two.

- **Active is the letter `A`, never the label `Actif`.** "Actif" returned
  zero rows for every city. The step exits on zero active rows.
- **`codeCommuneEtablissement` is not always the boundary API's code.**
  Paris (`751xx` against `75056`) and Marseille (`132xx` against `13055`)
  are arrondissement prefixes; no batch city has arrondissements. But
  **legacy codes survive**: Lille keeps 59355 (Lomme, 22 rows) and 59298
  (Hellemmes, 2), communes associées folded into 59350. At step 2, count
  every code in scope and look for legacy codes inside the contours;
  `COMMUNE_PREFIXES` holds EXACT codes.
- **The CRS is per row** (`epsg`: 2154 in metropolitan France; 2975, 5490
  and 2972 in the DOM). The step keeps 2154 and drops the rest loudly.
- **`qualite_xy` 33 is commune-centroid grade** and is dropped: those rows
  are not at a street address.
- **Non-diffusible rows arrive hollowed out** (name, address and coordinates
  withheld by INSEE). They are dropped; the share is on the page. The
  briefs' screen shares ran low in Rennes and Toulouse, so publish step 2's
  figure, never the brief's.
- **No employee filter.** `NN` is the sole trader's band (77% of Paris's
  bucket rows); the "50,156" Paris figure was tuned, not measured.
- **Naming is the Milan hybrid**: enseigne, else the usual name, else the
  address. **No legal-name column is ever loaded** (asserted), because a sole
  trader's legal name is a person's name.
- **Catch-alls are per city**: `CATCH_ALL_EXCLUDE = ("96.09Z", "56.29B")` is
  the precedent in all five (96.09Z ran 9.6 to 14.0%). Step 2 prints this
  city's shares; one far outside that range goes to the owner.
- **Step 2 streams the 2.2 GB parquet a row group at a time.** It fits in
  memory, but it is the build's long job. Run one French step 2 at a time on
  the machine and announce it (`docs/session_roles.md`). Twenty of them are
  twenty full scans; if the batch runs back to back, one pass that keeps
  every batch commune is worth writing (a change to `france_register.py`,
  with its control re-run).

## 2. The tram leg - each city's own feed, fetched fresh

**Feeds are rolling** (Avignon's ends 2026-10-18; most run four to twelve
weeks). So:

- **`fetch_sources.py` always downloads the feed**, even when
  `data/<slug>/raw/gtfs.zip` exists. ⚠ **The screen left 2026-09-27 copies
  there for most batch cities.** Rennes's fetch skips a cached zip; do not
  copy that behaviour for the batch.
- It records the fetch time and either the feed's own `feed_info.txt` window
  (`GTFS_SELF_ATTESTS = True`) or the NAP's metadata about the feed (Paris's
  and Toulouse's pattern) in `outputs/<slug>/provenance.json`, which the page
  reads.

**Mode flags lie, so the mode is decided per city from what step 1 keeps:**

| Feed says | What it is | City |
|---|---|---|
| `route_type 1` (metro) | a street tram | **Reims** (route `TRAM`) |
| `route_type 1` (metro) | light rail with a central tunnel | **Rouen** (the "Métro") |
| `route_type 0` (tram) | a tram-train, dropped on the rail test | **Mulhouse** `TT` |
| `route_type 0` (tram) | a sixth route, an owner call | **Nice** `B` |
| `route_type 6` (aerial lift) | a cable car, an owner call | **Brest** `C` |
| `route_type 7` (funicular) | not drawn | Le Havre's, only in the Normandie aggregate |

So select by **`route_short_name` AND `route_type`** (`LINE_KEYS`,
`ROUTE_TYPES_RAIL`), and read the route_ids fresh (`ROUTE_IDS`, a TODO in
every config). Several route_ids may share a key: Le Havre has two per line
and Valenciennes up to three. **Caen and Rouen come from the Normandie
aggregate**, filtered to one agency (`GTFS_AGENCY_ID`). Caen has no feed of
its own. Astuce's own host (`api.mrn.cityway.fr`) refused connections on
2026-09-27 and again on 2026-09-30; try it first at build.

**Stations - the pure-extract rule, exactly:**

1. Take the stops served by the kept routes' trips, and drop the
   non-boardable ones (`pipeline/stations.py`'s `boardable_stop_ids`:
   Strasbourg's `WACKE_T1`). Drop **fictitious stops**, the `FIC_` ids
   (Brest's two "Aiguillage" track switches, boardable on 40 of 1,038
   stop_times).
2. A platform with a `parent_station` becomes **the parent's own row**: its
   id, name and coordinates, untouched.
3. A platform without one is grouped with the other parentless platforms of
   the **same unchanged `stop_name`**, and the group becomes **the first
   platform in `stops.txt` order**: its id, name and coordinates. Never a
   mean. Rennes's step 1 averages a name group (`"latitude": "mean"`), which
   was fine for Rennes and is **wrong for the batch**. Do not copy it.
4. Nothing is renamed. Two stops with different names 50 m apart stay two
   (Montpellier's interchanges, Saint-Étienne's PEUPLE stops, Le Havre's
   Place Jenner A and B).

Nine of the twenty cities have no parent stations at all. Strasbourg,
Saint-Étienne, Dijon and Avignon ship no `parent_station` column;
Montpellier, Le Havre, Brest, and the Normandie aggregate (Caen, Rouen) leave
it empty. Orléans fills it on 9 of 103 platforms.

5. **On a Licence Ouverte feed only** (owner, 2026-09-30), a same-name pair
   (case and accents ignored) within 150 m keeps its **first** row. No mean,
   no rename. That covers Bordeaux's PESSAC CENTRE / Pessac Centre at 3 m and
   four same-name parent pairs, and Caen's Presqu'île / Presqu'Ile at 12 m.
   **On an ODbL feed, never.**

**Geometry**: `shapes.txt`, each line's most-used shape, **after checking
that it is track**. Compare its point count with the trip's stop count: when
the shape's points are exactly the stops, it is straight lines between stops.

- **Three feeds have no shapes: Montpellier, Strasbourg and Le Havre.**
- **The Normandie aggregate's tram shapes are all stop-to-stop**
  (`TCAR:AUTO_*`, `TWISTO:AUTO_*` and `LIA:AUTO_*`; measured on
  2026-09-30's copy, 20 of 20 points at stops on Rouen's métro and 25 of
  25 on Caen's T1). So **Caen, Rouen and Le Havre also take their geometry
  from OpenStreetMap**. The aggregate still supplies Caen's and Rouen's
  stations. Le Havre uses nothing from it: its LiA stops equal LiA's own
  ODbL feed to 5 decimals, and that makes the ambiguity over LiA's licence
  inside the aggregate (LO 2.0 declared, ODbL at source) moot.

Use OpenStreetMap's route relations through `osm-rail`, already covered by
the OpenStreetMap notice. Any other layer needs a `licence-read` first.

**Colours**: the feed's `route_color`. **Dijon's two lines share one colour**
(AB0672), which `pipeline/linecolour.py` refuses; Lille's precedent darkens
one. **Le Havre's colours are the project's own** (LiA's website claims its
scheme; Riga's precedent), even though the aggregate carries some.
Valenciennes's route_ids per line differ in colour: take the most-used
route_id's.

**The shared module (written with Le Mans, 2026-09-30).**
`pipeline/countries/france_tram.py` holds steps 1 and 3, and
`france_tram_fetch.py` the downloads; no step imports the network code. It
covers:
- `LINE_KEYS` with several route_ids per key, and `GTFS_AGENCY_ID`;
- the pure-extract rule above;
- `EXPECTED_INSIDE_PER_LINE` (commune) or `EXPECTED_SERVED_COMMUNES`
  (regional), with excluded stations named by commune;
- `EXCLUDED_STATION_PLACES` for a stop outside France;
- gate 3 from OpenStreetMap;
- either geometry source;
- baseline emits.

**`ROUTE_BRANCHES`** is for a feed route that riders know as several lines.
Reims's one route `TRAM` is two public lines, T1 and T2, since 2025-11-24. The
module splits the trips by the terminus each serves (the platform's name). A
short working goes by its branch's own stops, and a trip on shared stops only
counts for both.

**Gate 3 from OpenStreetMap** counts the distinct stop positions in each
ref's most complete relation. It is exact for most cities. It reads low where
a line branches, because each relation covers one branch (Brest's A), and
where OSM's positions sit far from the feed's (Saint-Étienne, Nice). Record
it as OSM has it, and trace any mismatch by name
(the France build entries in `DECISIONS.md`). Never count a union of relations:
it over-counted exactly where the single-relation count was right.

## 3. The scope call - commune or regional

Scope is the owner's call per city, and the owner approved this rule on
2026-09-30. It fits both precedents: **when the worst line keeps under half its stations in the
commune, go regional; at half or more, stay commune-only.** Toulouse's T1 at
52% stayed commune-only; Rennes's line b at 73% the same. Lille's Métro 2 at
43% (and its tram at 8%) went regional. SIRENE is one national file, so
regional costs only a wider commune filter; data availability is never the
reason.

- **Commune-only**: the boundary is `geo.api.gouv.fr/communes/<code>?geometry=contour`.
  ⚠ Use `geometry=contour`, never `fields=contour`, which returns a 120-byte
  POINT with no error. Step 1 asserts `EXPECTED_INSIDE_PER_LINE`; a change
  is a decision re-taken. Excluded stations are named with their commune
  from the EPCI's contours (Rennes). **Strasbourg's line D runs to Kehl,
  Germany**: no French file covers those three stops, so name them "in
  Kehl, Germany" by hand.
- **Regional**: scope to the communes that hold a kept station (Lille's
  pattern). Record them in `served_communes.csv`; their union is the map's
  boundary. `COMMUNE_PREFIXES` is those exact codes plus any legacy ones.
  Valenciennes spans two EPCIs (245901160 and 200042190), so both commune
  files are fetched.
- The display name takes " (Regional)", as Lille's does. The page file stem
  comes from the slug.

Approved from 2026-09-30's measurement: regional for **Bordeaux** (A 36%),
**Grenoble** (D 32%), **Rouen** (32%), **Valenciennes** (T2 24%) and
**Nantes** (line 3, 48.5%, the closest call). Every other city is
commune-only, the nearest being Strasbourg (B 52%) and Montpellier (line 2
54%).

## 4. Rings - 0.05 / 0.1 / 0.2 / 0.3 mi

Lambert-93 (`EPSG:2154`) for every French city, never UTM: one national grid
for one national register, and never EPSG:4326 for distance. Measure the
median nearest-neighbour gap among the stations in scope. At about 550 m or
less, use the half-size edges `[0.0, 0.05, 0.1, 0.2, 0.3]`; the config
comment records the figure, and `scripts/ring_rules_table.py --write`
regenerates `docs/ring_rules.md` after the city lands. Above 550 m, keep the
standard edges and drop the page's half-size sentence (none in the batch
measured over 510 m).

## 5. Notices - by the feed's licence

| Licence | Cities | What the page must carry |
|---|---|---|
| **Licence Ouverte 2.0** (`lov2`) | 16 of 20, Caen and Rouen through the Normandie aggregate | The producer and the data's date in the transit caption (Marseille's and Toulouse's pattern). No `_NOTICES` entry. For the aggregate, credit its Concédant, **Syndicat mixte Atoumod** (not the Région, not the exporter Cityway: the licence read 2026-09-30), the agency's network, and the resource's `last_modified` date captured at fetch; `feed_info.txt` has no date |
| **Licence Ouverte 1.0** (`fr-lo`) | Bordeaux | Credit **Bordeaux Métropole** (not TBM, Keolis or the exporter Mecatran) and the feed's own date, captured at fetch; nothing implying endorsement; nothing from infotbm.com (read 2026-09-29) |
| **ODbL 1.0** (`odc-odbl`) under the NAP's Conditions Particulières | Montpellier (TaM, Montpellier Méditerranée Métropole), Grenoble (SMMAG, "M"), Le Havre (Le Havre Seine Métropole) | A §4.3 notice in `app/components.py` `_NOTICES`, one per database, on Tisséo's and STAR's model ("Contains information from <database>, which is made available here under the Open Database License (ODbL). …"). Neither existing notice discharges a new one. Station tables are pure extracts. No TaM logo (read 2026-09-29) |

For every city, also:
- **`Source : Insee`**, verbatim, with the SIRENE edition's date
  (`docs/licenses/france-licence-ouverte-2.0.md`: the only prescribed string);
- © OpenStreetMap contributors on the render, plus the OpenStreetMap
  notice where OSM supplies geometry;
- a row per new source in `docs/data_sources/france.md`: the feed, the
  commune contour or EPCI file, and any geometry source. Write it before the
  page exists.

## 6. Page text - approved by the owner, word for word (2026-09-29)

Braces are per-city facts, filled from this city's own measurements (step 1,
step 2 and the rendered map), never from the brief's screen figures. The
controls paragraph and the heat-layer caveat stay exactly as on Rennes's
page (`app/pages/25_Rennes_Heatmap.py`), and so does the transit caption
(from `provenance.json`), with the operator's credit and any notice its
licence read requires.

> {N} {operator} tram lines are drawn, **{lines}**, each labelled on the map
> and in the legend, from the operator's own published timetable feed. {City}
> has no metro, so its trams are its rapid transit, as in Riga. Every tram
> stop here gets rings.
>
> The map covers the **{commune of City / N communes of the Métropole}**.
> {Where a line runs past it: which stops are left out and why, as Rennes's
> page does.}
>
> Businesses come from **SIRENE**, France's national register of
> établissements, joined to INSEE's geolocation file, the same sources as
> Paris, Marseille, Toulouse, Lille and Rennes. {Share} of active
> establishments here are marked non-diffusible by INSEE, which withholds
> their name, address and coordinates together, so they never reach this map.
> Where SIRENE records no shop sign or trading name, the dot shows the address
> instead.
>
> **Read the density as a register, not a street survey.** {Same paragraph as
> Rennes, with this city's ratio to OpenStreetMap's restaurants.}
>
> **Tram stops sit closer together than metro stations**, a median of
> {spacing} m here, so the rings are drawn at half the usual size (0.05 to
> 0.3 mi), as on the other French maps. **About {share} of storefronts sit
> within a ring.**

A city whose median stop gap is over about 550 m keeps the standard rings and
drops the last paragraph's first sentence.

**Departures are owner calls, never edits.** Three are approved
(2026-09-30):

- **Rouen**: the first paragraph's second sentence reads "Rouen's métro is a
  light rail running mostly on the street, so every stop gets rings."
- **Brest**: "two tram lines and the cable car".
- **Nice**: its line count includes route B.

Anything else that does not fit the template goes to the owner as a
proposed sentence.

## 7. The macro map and the app entry

- **Two keys** (owner, 2026-09-30, the macro-legend branch): `mode` is the
  dot colour, the highest-order mode drawn (`metro` > `light_rail` >
  `tram`); `coverage` is the fill. SIRENE carries all three buckets, so
  every French city is `"full"`. `mode` is `"tram"` for 19 cities and
  `"light_rail"` is approved for Rouen. `scaffold_city.py --mode` arrives
  with that branch; until it lands, the batch script prints the values to
  set by hand from `MAP_MODE` and `MAP_COVERAGE`.
- The label width is measured in a real browser for `check_macro_labels.py`
  (`scaffold_city.py`'s step 5), and the France view is the app/chrome
  role's question.
- Landing: in groups, one sitting each, per `docs/review_time.md` ("Landing
  the tram batch"), with one `city-added` deploy-verify per group.
  Approvals and `app/` landings wait for review time.

## Before publishing (each city)

`python scripts/check_personal_exposure.py <slug>` (verdict in
`DECISIONS.md`); `python scripts/check_provenance.py` names the city OK;
`python scripts/check_scope_disclosure.py` passes, with the excluded
categories in `docs/excluded_categories.md` and the rail scope on the page;
`python pipeline/drift_check.py <slug>`; `grep -rn TODO pipeline/<slug> app`
is empty; a `DECISIONS.md` entry (`decisions-entry`). Then `publish-city`.

## The batch, one line each

Scope, mode and every call were approved as the briefs recommended them
(owner, 2026-09-30). Station counts are 2026-09-30's, under the pure-extract rule.

| City | Lines | Stations (in commune) | Scope | Mode | Calls and traps |
|---|---|---|---|---|---|
| Montpellier | TaM 1-5 | 112 (88) | commune | tram | ODbL; **no shapes**; no parent_station |
| Nice | L1-L3, B | 47 (47) | commune | tram | route B drawn; L2 tunnel |
| Strasbourg | CTS A-F | 94 (65) | commune | tram | **no shapes**; no parent_station; Kehl (Germany) |
| Bordeaux (Regional) | TBM A-F | 140 | regional, 14 communes | tram | LO 1.0; LO same-name pairs keep the first row |
| Nantes (Regional) | Naolib 1-3 | 84 | **regional, 6: the closest call** | tram | 579 MB stop_times |
| Grenoble (Regional) | M réso A-E | 81 | regional, 12 | tram | ODbL (SMMAG); undated feed_info |
| Rouen (Regional) | Astuce Métro | 31 | regional, 5 | **light_rail** | Normandie aggregate, OSM geometry; its own page sentence |
| Saint-Étienne | STAS T1-T3 | 40 (35) | commune | tram | no parent_station |
| Dijon | Divia T1-T2 | 34 (28) | commune | tram | one colour for both lines |
| Tours | Fil Bleu A | 29 (22) | commune | tram | `feed_infos.txt` (sic) |
| Le Havre | LiA A-B | 23 (22) | commune | tram | ODbL; OSM geometry (the aggregate's are stop-to-stop); own colours |
| Mulhouse | Soléa 1-3 | 29 (28) | commune | tram | tram-train `TT` dropped |
| Reims | Tram T1 and T2 (one feed route, split) | 24 (21) | commune | tram | typed `route_type 1`; two public lines since 2025-11-24 |
| Caen | Twisto T1-T3 | 38 (29) | commune | tram | Normandie aggregate, OSM geometry; Presqu'île pair keeps the first row |
| Brest | Bibus A-B, Téléphérique | 41 (39) | commune | tram | cable car drawn; `FIC_` switch stops |
| Besançon | Ginko T1-T2 | 31 (29) | commune | tram | none |
| Orléans | TAO A-B | 51 (32) | commune | tram | partial parent_station |
| Le Mans | SETRAM T1-T2 | 35 (35) | commune | tram | the `lmm_auto` resource |
| Avignon | Orizo T1 | 10 (10) | commune | tram | earliest feed end |
| Valenciennes (Regional) | Transvilles T1-T2 | 48 | regional, 13, two EPCIs | tram | built last |
| Angers | Tram A-C (mark-free) | 42 (36) | commune | tram | ODbL; no parent_station; **the brand never shown**; notice 77 by producer and NAP id |
