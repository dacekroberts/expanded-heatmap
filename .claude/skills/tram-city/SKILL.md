---
name: tram-city
description: Build a trams-only city outside France and Czechia - the ten T1 cities in seven countries (Odense, Daugavpils, Liepāja, Kansas City, New Orleans, Tucson, Florence, Zurich, Göteborg, Den Haag) - with what every trams-only map shares - the owner's trams-only calls, rings by the spacing rule, no thinning but New Orleans's street-stop filter, the light-rail test, rolling feeds, OSM rail, the currency rule, one-bucket and narrowed pages, the macro map's mode and coverage keys, and the page-text shape - plus a sheet per city pointing at its country's built template. Read with the city's brief, add-city, osm-rail and publish-city, which it does not replace.
---

# Building a trams-only city (the ten non-French, non-Czech T1 cities)

Written 2026-09-30 by the tram kit session (`docs/handoff_tram_kit_2026-09-30.md`),
from the built trams-only and tram-heavy cities (Riga, Dublin, Aarhus and the
French five) and the owner's calls of 2026-09-27 to 09-30. **France has
`france-tram-city` and Czechia its own kit. These ten cities are spread over
seven countries, one or two per country**, so this skill carries only what they
share. Anything about one country is in that city's brief
(`docs/build_briefs/<slug>.md`, which staging writes) and in the built city the
brief names as its template. `japan-city`, `taiwan-city` and `brazil-city` stay
the model for a country skill. Write one only if a country here gets a third
city.

**Builds are HELD** (owner, 2026-09-30) until the owner gives the go after
the kit and the briefs' calls. Build on a branch, never on master: `app/` lands
at review time only (`docs/review_time.md`).

## Order of work for one city

1. `python scripts/brief_check.py <slug>`. A failing claim means the brief
   needs correcting. **Exception: "MIRRORS DISAGREE"** is an Overpass host
   problem, so re-run it (Liepāja, 2026-09-30).
2. Read the brief's **"For the owner, with the build"** table: `mode`,
   `coverage`, scope, lines, rings and each call with its recommendation. If
   the table is missing, ask staging for it before writing code.
3. **Zurich only: `add-country` first** (Switzerland is new; see its sheet).
4. `add-city` Step 0 is already in the brief. Go to `scaffold-city`:
   `scripts/scaffold_city.py ... --mode <mode> --dry-run`, then the real run.
   There is no batch scaffold (DECISIONS "The tram kit: no batch scaffold").
   Then copy the **template city's** config for everything `scaffold_city.py`
   leaves generic. The sheet below names each city's template.
5. Set the rings (section 3) by hand, and the CRS where section 3 says to.
   `scaffold_city.py` writes the standard rings and a WGS84 UTM zone.
6. Write `fetch_sources.py`, which **always downloads the feed** (section 4),
   then step 1, step 2 and the render. Then run "Before publishing".

## The owner's standing calls - do not re-ask

- **Trams-only maps are approved** (DECISIONS "Yes to trams-only maps",
  2026-09-29). With no metro, the trams are the rapid transit (Riga's
  precedent), and every tram stop gets rings.
- **No stop thinning on the tram list** (DECISIONS "Tram audit Phases 3-4",
  owner). Riga's 0.5 mi filter does not carry over, even to the two Latvian
  cities built on Riga's modules. **The single named exception is the
  street-stop filter where stops stand one or two blocks apart**: New
  Orleans at a 161 m median gap (section 2). Its spacing is still an owner
  call.
- **Rings follow the spacing rule** (DECISIONS "Tram cities use the existing
  spacing rule", owner, 2026-09-29), section 3.
- **The light-rail test** (`docs/tram_city_list.md`, owner, 2026-09-29) decides
  whether a system is a tram at all, and it decides `mode` (section 1).
- **Feeds are rolling**: fetch at build, never cache one across weeks.
- **The currency rule** (the master list's "Five rules", owner, 2026-09-29):
  the source drops closed businesses, its newest row is under five years old,
  and the data date goes on the page. **Kansas City** (frozen 2026-01-15) and
  **Göteborg** (undated rows) carry it in the page text (section 6).
- **Denmark's placement is OSM's DAR address points** (owner, 2026-09-27),
  keyless and under ODbL. The Datafordeler account is reopened only if a build
  proves it needs one.
- **Rejseplanen's GTFS is never used** (owner, 2026-09-29, for Aarhus).
- **Zurich's partial retail** is the alcohol-licensed shops, on the tobacco-
  retail precedent of Seoul and Gyeonggi, with the gap disclosed (owner,
  2026-09-30).
- **Den Haag's horeca layer is used on Amsterdam's precedent** (owner,
  2026-09-30): credit "Gemeente Den Haag", and never call the layer current or
  complete.
- **A GTFS feed that declares no licence is not used**: take OSM (Olomouc,
  owner, 2026-09-30). Daugavpils and Liepāja follow it.

## 1. Is it a tram, and what is its `mode`?

**The light-rail test** (`docs/tram_city_list.md`) has three parts, read
against San Diego, Calgary and Edmonton:
- **Track**: tunnel and bridge share, and OSM's `light_rail`/`tram` split.
- **Frequency**: every 15 minutes or better by day. This is a **gate only on
  converted railway** (Aarhus's L1). On purpose-built track a slower timetable
  is disclosed on the page (Buffalo's flat 20).
- **Spacing**: about 550 m or more. This supports the verdict but is not the
  gate.

A city that passes left the tram list on 2026-09-29. **All ten here stayed**,
so they are trams, and `mode` is `"tram"` unless step 1 keeps something of a
higher order. **`mode` is the highest-order mode the map DRAWS**, decided from
what step 1 keeps (GTFS `route_type`, OSM `route=`), never from a marketing
name. France's feeds showed that mode flags lie (Reims's tram is typed metro).
Here that means:

| City | Proposed `mode` | The question |
|---|---|---|
| Den Haag (EDGE) | `light_rail` if RandstadRail 3 and 4 are drawn as light rail; `metro` only if line E is drawn | **Line E keeps 4 of its 23 stops in the city.** That is a stub (Ostrava's line 5, Madrid's ML2 and ML3), so leaving it out is recommended |
| Zurich | `tram` | **The Forchbahn (S18) is OSM `route=light_rail`.** Inside the Stadt it runs on tram 11's track and stops. Drawing it would make the dot light-rail purple for no new rings, so leaving it out is recommended, named with the S-Bahn |
| Odense | `tram` | Aarhus, its template, is `light_rail` (its new tramway passed the test). Odense's Letbane is OSM `route=tram` and street-running, and it stayed on the list |
| the other seven | `tram` | none |

**A frequency floor for a route, not a system (Daugavpils).** Street trams
have no frequency gate, but no built city draws a route that runs **hourly**,
and Daugavpils's routes 2-4 did at the screen. The kit recommends drawing a
route only if it runs at least **every 20 minutes by day** (Buffalo, the
slowest drawn). A stop served only by slower routes goes to
`excluded_stations.csv` as **infrequent**, Aarhus's class
(`app/station_scope.py`). This is an owner call (the call list).

## 2. Stations - every stop, one exception

- **Every stop in scope gets a ring.** Collapse platforms to stations and
  thin nothing. `pipeline/stations.py`'s gates still run: spacing, per-line
  counts, and the boardable filter.
- **GTFS feeds**: take the feed's own `parent_station` row first. Without
  one, collapse by unchanged name as the template city does. **On an ODbL
  feed, France's pure-extract rule applies** (`france-tram-city` section 2):
  the first platform in `stops.txt` order, never a mean, rename nothing. The
  rule came from the French portal's ODbL conditions, so it does not reach
  a CC0, CC BY or public-domain feed. A rename or a merge of two differently
  named stops goes to the owner.
- **OSM rail: route-relation membership, never a tag search** (`osm-rail`).
  One Overpass query per city. Bound every name search with a bbox. Two
  relations per line, so draw the one with the most way geometry
  (`map_common.load_osm_line_shapes`). **The collapse is Aarhus's**
  (`pipeline/aarhus/step1_stations.py`): stop members collapsed by name at
  their mean within 200 m, exiting if a name spreads wider.
  - **A tagged stop missing from every route relation is added by its node,
    named in config** (`STATION_ADD`). Odense's SDU Syd/Hospital Nord
    (opened 2023-08-25) and Liepāja's Brīvības iela (the named terminus) and
    Klaipēdas iela are the cases. Check each against the operator's own stop
    list.
  - **A stop that is not yet open stays out** and becomes a watch item
    (Odense's Hospital Syd, 2027).
- **The street-stop filter is New Orleans's only.** Stops one or two blocks
  apart (161 m median) put every ring on top of the next.
  `docs/sub_transit_line_filters.md` applies through `pipeline/stations.py`
  `thin()`, never a new copy. Keep terminals and interchanges (filters 2 and
  4). Measure the thinning along each line's stop sequence, and write every
  cut stop to `excluded_stations.csv` with "spacing" in its reason. **The
  spacing is the owner's call**: the brief measures the in-ring share with
  every stop kept and at the proposed spacing (400 m suggested). No other
  city on this list is thinned.
- **A line mostly outside the scope is a stub question**, as for the Czech
  and French cities: Göteborg's 4 and 12 (Mölndal), Den Haag's E, Zurich's
  Glattalbahn, and Florence's T1 (4 of 26 stops in Scandicci). Keep the line
  and list the stops outside, or drop a stub. The brief recommends which.
  Where the business source covers the city only (Zurich, Göteborg, Den
  Haag's horeca layer, Florence), **the scope cannot go regional**, so
  France's scope rule does not apply.

## 3. Rings - the spacing rule

Measure the **median nearest-neighbour gap among the stations in scope**,
after collapse, with every stop kept (or after New Orleans's filter, if the
owner approves it).
- **About 550 m or less**: `RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]`,
  `RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]`
  (Aarhus's config). The config comment records the figure.
- **Over about 550 m**: the standard `[0.0, 0.1, 0.2, 0.3, 0.6]`. Drop the
  page's half-size sentence. **Kansas City** (about 560 m at the screen) is the
  only borderline city: measure at build on its step 1 stations and apply the
  rule as written. A figure between 540 and 570 m goes to the owner with both
  in-ring shares.
- Screen gaps (the tram list): Odense 440 m, Daugavpils 281-298, Liepāja
  309-329, Florence 322, Tucson 266, New Orleans 161; Zurich, Göteborg and
  Den Haag at build.
- **Riga is on the standard rings with thinning.** Its Latvian followers are
  NOT: no thinning and halved rings, as above.
- **Distance in a metre CRS, never EPSG:4326**, and the CRS is per city:
  Odense `EPSG:25832` (Aarhus's, DAR's own); Daugavpils `EPSG:32635`;
  **Liepāja `EPSG:32634`** (21.0° E, not Riga's 35N); **Zurich `EPSG:2056`**
  (LV95; the register's `ekoord`/`nkoord` are already in it). The US,
  Italian, Swedish and Dutch cities use their own WGS84 UTM zone, which
  `scaffold_city.py` derives from the longitude: **Göteborg is 32N, not
  Stockholm's 34N**. Override the scaffold only for Odense and Zurich.
- After the city lands: `python scripts/ring_rules_table.py --write`.

## 4. Feeds are rolling, and OSM is the fallback

- **`fetch_sources.py` always downloads the feed**, even when
  `data/<slug>/raw/` holds one. Record the fetch time and the feed's own
  `feed_info.txt` window (or the publisher's metadata) in
  `outputs/<slug>/provenance.json`, which the page's caption reads. A step
  never fetches (`check_no_fetch_in_steps.py`).
- **Read the licence before the feed is used**, with one `licence-read` per
  source (`read-licence`). Still unread on 2026-09-30: RideKC's GTFS
  (declared "free for anyone to use"), RTA's GTFS, GEST's in the Regione
  Toscana feed (declared CC BY 4.0), and whichever feed Zurich, Göteborg or
  Den Haag use.
- **OSM through `osm-rail`** where a feed is unlicensed, unreachable or barred:
  Odense (Rejseplanen barred), Daugavpils and Liepāja (the city GTFS declares
  no licence). Zurich and Göteborg were measured on OSM at the screen, and
  their briefs decide the source. OSM is already covered by the site's
  OpenStreetMap notice. Say on the page that the lines and stops come from
  OpenStreetMap.
- **Colours**: the feed's `route_color`, else OSM's `colour` (a CSS keyword
  is resolved through the named-colour table: Göteborg's line 11 is "black").
  Else the project's own palette, as Le Havre and Riga have: Odense, the two
  Latvian cities, probably Kansas City. Run `pipeline/linecolour.py`'s checks
  and `check_map_markup.py`. Two lines with one colour are refused (Dijon).
- **Every drawn line gets a permanent on-map label (its real public name) and
  a legend entry.**
- **Shared code where it pays: `pipeline/osm_tram.py`, one module for both
  kits** (agreed with the Czech kit, 2026-09-30). Three to five of these ten
  take OSM rail (Odense, Daugavpils, Liepāja, perhaps Zurich and Göteborg),
  and five of the six Czech cities do. **Use it. If it does not exist yet,
  the first OSM tram build writes it**, from Aarhus's `stop_rows()`
  generalised:
  - relations kept on `ref` and `route`, and on `operator` only where the
    config names one;
  - **`STATION_ADD` by node id** for a tagged stop on no route relation;
  - stop members tagged `public_transport=stop_position` **or**
    `railway=tram_stop`, exiting on an untagged or unnamed member and naming
    it (Daugavpils's Stropu ciemats is on the routes with no stop tag);
  - **every matching relation is kept or listed in `NOT_DRAWN`** by relation
    id with a reason, and the step exits on one that is neither (the Czech
    screens found zero-stop refs, unref'd variants and depot runs);
  - **several relations per ref**: a line's stops are the union of its kept
    relations, and `load_osm_line_shapes` draws the one with the most
    geometry;
  - **scope over a union of polygons** (Liberec + Jablonec), with stations
    outside named with the place they lie in, as Rennes names communes;
  - **a lines-only mode** that selects and validates relations for the line
    geometry without producing stations, for a feed with stations but no
    `shapes.txt` (Brno);
  - Aarhus's name collapse, and `pipeline/stations.py`'s gates.

  Its control: run on Aarhus's inputs, it reproduces Aarhus's
  `stations.csv`. Aarhus itself is not rewired, and the later OSM cities are
  wrappers. The same goes for **Latvia's step 2**: Daugavpils's build lifts Riga's step 2
  (226 lines) into `pipeline/countries/latvia_register.py`, and Riga's
  `drift_check.py` is the control (Riga's outputs must not move). Shared
  modules are the app/chrome role's paths (`docs/session_roles.md`), so tell
  that role before writing one.

## 5. Coverage - full, narrowed or one bucket

The macro map's **fill** (`coverage`) follows the `categories` value (owner,
2026-09-30; the add-city skill on `macro-legend`): "All three" is `full`;
"Two", "Merged" and either "thin" are `narrowed`; "Food premises only" is
`one_bucket`. **Food shops are food.** A token third layer does not lift a
city, and that is the owner's call per city (`ONE_BUCKET_BY_OWNER`).

| City | `categories` | `coverage` | Why |
|---|---|---|---|
| Odense | All three | `full` | CVR, as Aarhus |
| Daugavpils, Liepāja | Merged | `narrowed` | Riga's two layers (shops and services merged; food thin by construction) |
| Kansas City, New Orleans, Tucson | All three | `full` | City licence registers with all three |
| Florence | All three | `full` | The Comune's four layers |
| Zurich | Two | `narrowed` | Food plus partial retail (alcohol-licensed shops, kiosks, petrol stations); no personal services. Boston's precedent: retail that is not only food shops makes two |
| Göteborg | Food premises only | `one_bucket` | Food service plus food shops, which count as food |
| Den Haag | Merged | `narrowed` | **Rotterdam's shape** (BAG winkelfunctie plus the horeca layer), which is `narrowed`, "Merged". The tram list's "full" does not fit that precedent; staging was asked to confirm (2026-09-30) |

**A narrowed or one-bucket page says what is missing in its own paragraph**
(section 6), and `check_scope_disclosure.py` holds it to
`docs/excluded_categories.md`. The layer control names only the categories
the map has (Riga's "Shops and services, and Food service").

## 6. Page text

**The trams-only template was drafted in chat on 2026-09-30 for the owner's
approval and is not approved yet.** Until it is, bring each page's text to
the owner as a proposal, built from these parts in this order, which are the
built pages' own (Rennes, Aarhus, Riga):

1. The lines drawn and their source; "has no metro: its trams are its rapid
   transit, as Riga's are, so every tram stop gets rings"; any slow timetable
   disclosed; the rail left out (buses, suburban rail, Zurich's S-Bahn and
   Forchbahn).
2. The scope and any stops left out, named with where they lie.
3. The business source, in the template city's wording.
4. **Narrowed or one-bucket only**: what the map has and what it lacks.
5. **Currency only** (Kansas City, Göteborg): the data date, or that the rows
   carry none.
6. "Read the density as a register, not a street survey", with the source's
   own caveat.
7. Rings: the half-size sentence with the median gap, and the in-ring share.
8. The controls paragraph and the heat-layer caveat, **exactly as on the
   built pages**, with the category names this map has.

The transit caption comes from `provenance.json` with the operator's credit
and any notice its licence requires.

## 7. The macro map and the app entry

- **Two keys** (owner, 2026-09-30; `add-city` on `origin/macro-legend`, or on
  master once it lands): colour = `mode`, fill = `coverage`, as sections 1
  and 5. `scaffold_city.py --mode` arrives with that branch. Until it lands,
  set `mode` by hand in the `cities.py` entry. `cities.py` raises at import
  without it.
- Region: `"Europe"` for the seven European cities. `"United States West"`
  for Tucson; `"United States East"` for Kansas City and New Orleans, since
  Houston (−95.4°) is East. `--country` is spelled as `app/cities.py` spells
  it, and `"Switzerland"` is new.
- The label width is measured in a real browser for `check_macro_labels.py`.
  Landing is in groups at review time with a `city-added` deploy-verify per
  group. `app/` changes reboot the app.

## Before publishing (each city)

`python scripts/check_personal_exposure.py <slug>` (verdict in `DECISIONS.md`;
**the suspects are Kansas City's `dba_name`, New Orleans's `ownername`,
Tucson's individuals' licences and Den Haag's `AANVRAGER`**);
`check_provenance.py` names the city OK; `check_scope_disclosure.py` passes;
a `docs/data_sources.md` row for every new source, the join and address layers
included (VZD's `aw_eka.csv`); `drift_check.py <slug>`; no `TODO` left in
`pipeline/<slug>` or `app/`; a `DECISIONS.md` entry. Then `publish-city`.

**Heavy jobs** (announce to every live session first, `docs/session_roles.md`):
Odense's step 2 reads the national CVR cache, and the Latvian step 2 reads
the national excise file and VZD's 141.7 MB address file. The rest are
city-sized.

## The ten, one sheet each

Proposed values are the briefs' or, where a brief is not yet written, the
tram list's. The briefs are staging's. Where they differ, the brief wins, and
the call list in `docs/handoff_tram_kit_2026-09-30.md` collects the owner's
calls.

| City | Template (built) | Business leg | Rail source | CRS | Traps |
|---|---|---|---|---|---|
| **Odense** | **Aarhus** (`pipeline/aarhus/`, `countries/denmark*.py`, `taxonomies/denmark_db25.py`) | CVR, kommune 461; placed on OSM's DAR points (98.4%); personally owned rows show the address, as Aarhus | OSM, 2 `route=tram` relations, ref L; + SDU Syd/Hospital Nord by node | 25832 | No colour in OSM; Hospital Syd opens 2027; build on the shared CVR cache, never refresh it from a branch |
| **Daugavpils** | **Riga** (`pipeline/riga/`, `taxonomies/riga_source.py`) | VID excise (food, placed on VZD's `aw_eka.csv`) + VZD cadastre use class 1230 (shops and services), ATVK 0002000 | OSM, refs 1-4 (the screen said 1-5: check the operator's list) | 32635 | `aw_eka.csv`'s `KOORD_X` is the northing (EPSG:3059); use `DD_N`/`DD_E`; `STATUSS` = EKS; the VZD credit (notice 42 extended); hourly routes (section 1) |
| **Liepāja** | **Riga** | as Daugavpils, ATVK 0005000 | OSM, ref 1; + Brīvības iela and Klaipēdas iela by node | **32634** | as Daugavpils |
| **Kansas City** | a US register city (`naics.py` does not fit; `premises-taxonomy` on `business_type`) | Socrata `kkhs-93m4`, PUBLIC_DOMAIN, **frozen 2026-01-15** (2025's licences) | RideKC GTFS route 601, `route_type` 0 (licence unread); OSM as the cross-check | UTM 15N | The data date on the page; `dba_name` is often a person; `business_type` mixes fee codes with activities; rings borderline (~560 m) |
| **New Orleans** | Philadelphia and San Francisco for the filter | Socrata `iqay-p646`, CC0, a text taxonomy (no codes); drop "Special Events-Other (Vendor)" and "Home Based-Office Use Only" | RTA GTFS, streetcars 12, 47, 48, 2 (licence unread) | UTM 15N | The street-stop filter (owner's spacing); `ownername` through the exposure check |
| **Tucson** | a NAICS city (`naics.py` unchanged) | BUSLIC on `gis.tucsonaz.gov`, active and not home-based | Sun Link GTFS | UTM 12N | "As is" terms (a read); ~6,250 individuals' licences; 10 min weekdays, 20 evenings and weekends, disclosed |
| **Florence** | **Milan** and **Rome** (the Comune's layers; Milan's *fuori piano*) | Four Comune layers on dati.toscana.it, CC BY 4.0 declared, coordinates on 100%, no names | GEST in the Regione Toscana GTFS (CC BY 4.0 declared) | UTM 32N | 639 exempt food rows (an owner call); Scandicci's 4 stops; 3,424 rows share a point; a full licence read; T3 due end 2026 |
| **Zurich** | **Stockholm** (one register, city only), Seoul/Gyeonggi (partial retail) | `Gastwirtschaftsbetriebe` via the **WFS** (the CKAN downloads are an Angular shell), layer `gastwirtschaftsbetriebe`, CC0; `betriebsstatus` = `Offen` | OSM (18 tram refs, all coloured) or the national feed, the brief's call | **2056** | **`add-country` first**; the S-Bahn named as excluded (fails on coverage); the Forchbahn (section 1); the Glattalbahn stub test |
| **Göteborg** | **Stockholm** (`taxonomies/sweden_livsmedel.py`) | `Livsmedelsverksamheter`, CC0, daily: **take the CSV** (`utf-8-sig`, `;`), never the rowstore JSON (drops 279 rows, swaps x and y) | OSM (13 lines, 127 stops) or Västtrafik, the brief's call | **UTM 32N** (11.97° E; not Stockholm's 34N) | Undated rows (the page says so); 274 blank `typ` to classify or drop; lines 4 and 12 into Mölndal; heritage line out; line 11 "black" |
| **Den Haag** | **Rotterdam** (BAG, `taxonomies/rotterdam_source.py`); Amsterdam for the horeca precedent | BAG winkelfunctie units + the city's `Horeca_nieuw` layer (2,543 granted or notified) | HTM's lines, GTFS as Rotterdam's or OSM | UTM 31N, as Rotterdam | **Never fetch `AANVRAGER`, `KVKNUMMER` or `RECHTSVORM`**; the trade name is `OMSCHRIJVI`, double-encoded UTF-8 to repair; line E's stub; `mode`; tram 1 at 54% in the city |
