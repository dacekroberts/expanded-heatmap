---
name: tram-city
description: Build a trams-only city outside France and Czechia - the ten T1 cities in seven countries (Odense, Daugavpils, Liepāja, Kansas City, New Orleans, Tucson, Florence, Zurich, Göteborg, Den Haag) - with what every trams-only map shares - the owner's trams-only calls, rings by the spacing rule, no stop thinning anywhere (New Orleans included), the light-rail test, the shared OSM tram step 1, rolling feeds, OSM rail, the currency rule, one-bucket and narrowed pages, the macro map's mode and coverage keys, and the page text the owner approved - plus a sheet per city pointing at its country's built template. Read with the city's brief, add-city, osm-rail and publish-city, which it does not replace.
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

**Builds are HELD** (owner, 2026-09-30) until the owner gives the go. The
kit's 24 calls were approved on 2026-09-30, but that is not the go. Build on a branch, never on master: `app/` lands
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
  cities built on Riga's modules. **New Orleans keeps every stop too**
  (owner, 2026-09-30, call 13), so no city on this list is thinned.
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
- **RideKC's GTFS is not used** (owner, 2026-09-30): Kansas City's rail is
  OSM.
- **The kit's 24 calls, approved as recommended** (owner, 2026-09-30: "Agree
  with recommended options for all"; the numbers are the handoff's):
  1. the page-text template (section 6);
  2. a route is drawn only if it runs at least every 20 minutes by day, and
     a stop served only by slower routes is listed as infrequent (section 1);
  3. the project's own colours where the source has none (Odense, Daugavpils,
     Liepāja, Kansas City, Tucson);
  4. Odense's SDU Syd/Hospital Nord added by node, and Hospital Syd out until
     it opens;
  5. Odense's `mode` is `tram`;
  6. Daugavpils's routes under the call 2 floor (**superseded by call 28**:
     every route is drawn);
  7. Daugavpils and Liepāja are `narrowed`, "Merged";
  8. notice 42 extended to name VZD's address register, in VZD's wording
     with the year;
  9. Liepāja's Brīvības iela and Klaipēdas iela added by node;
  10. Kansas City keeps licences valid for 2025 and 2026 only;
  11. Kansas City's `dba_name` withheld where it reads as a person (Houston's
      rule);
  12. Kansas City's fee-code types dropped, with the count on the page;
  13. New Orleans keeps all 110 stops;
  14. New Orleans drops "Special Events-Other (Vendor)" and "Home
      Based-Office Use Only";
  15. Tucson's `ACC_NAME` withheld for Sole Proprietorship, Individual and
      Married;
  16. Florence keeps its 639 exempt food rows, filtering what the type code
      names as non-public, on Milan's *fuori piano* precedent;
  17. Florence is commune-only, with T1's 4 Scandicci stops listed as
      outside;
  18. Zurich's Forchbahn is left out and named on the page;
  19. Zurich's Glattalbahn lines each take the stub test, and a stub is
      dropped;
  20. Göteborg's blank-`typ` rows are classified by name where the name
      shows a counter, and the rest dropped;
  21. Göteborg's lines 4 and 12 are drawn to their ends, with the Mölndal
      stops listed as outside, unless the stub test fails;
  22. Den Haag's RandstadRail E is left out as a stub;
  23. Den Haag is `narrowed`, "Merged";
  24. Den Haag's 158 pending horeca permits are left out.

  **Calls 18-24 were approved before their briefs landed.** If a brief's
  measurement changes the facts behind one (a Glattalbahn line that is not
  a stub, a Mölndal line that is), the call goes back to the owner.
- **The four calls from the last briefs** (owner, 2026-09-30):
  25. Zurich's tram 20 (Limmattalbahn, 4 of 26 stops inside) is left out as
      a stub;
  26. Den Haag's tram 1 (19 of 37 inside, 51%) is drawn to its end, with the
      stops outside listed;
  27. Den Haag's page carries the permit layer's date (section 6);
  28. **Daugavpils draws its whole network, routes 1-5, and the page states
      the waits.** In the owner's words: "like with buffalo 50% of network
      shouldn't fall if the norm is longer waits." Call 2's floor would have
      kept only route 1, 19 of the 38 stops.

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

| City | `mode` | Why |
|---|---|---|
| Den Haag (EDGE) | `tram` (the brief, 2026-09-30: every drawn line, RandstadRail 3 and 4 included, is OSM `route=tram`) | **Line E is left out as a stub** (owner, call 22): 4 of its 23 stops are in the city, as Ostrava's line 5 and Madrid's ML2 and ML3 were. So `metro` is never drawn |
| Zurich | `tram` | **The Forchbahn (S18, OSM `route=light_rail`) is left out** (owner, call 18) and named on the page with the S-Bahn. Inside the Stadt it runs on tram 11's track and stops, so drawing it would add no rings |
| Odense | `tram` (owner, call 5) | Aarhus, its template, is `light_rail` (its new tramway passed the test). Odense's Letbane is OSM `route=tram` and street-running, and it stayed on the list |
| the other seven | `tram` | none |

**Frequency: disclose the network's norm, drop only an outlier** (owner,
calls 2 and 28). Street trams have no frequency gate. Read each route's
daytime headway from the operator's own timetable.
- **Where longer waits are the network's norm, every route is drawn and the
  page states the waits** (call 28, Buffalo's precedent). Daugavpils is the
  case: route 1 every 10-15 minutes, the Stropu loop (3 and 5) every 20-30
  minutes each way, routes 2 and 4 about hourly. All five are drawn, because
  dropping the slower routes would take half the network (19 of 38 stops).
- **Call 2's 20-minute floor (Buffalo, the slowest drawn) is for an outlier
  route**: a slow route on a network that otherwise meets it, such as
  Zurich's 50 and 51 if they turn out not to run by day. Its stops, if no
  other route serves them, go to `excluded_stations.csv` as **infrequent**,
  Aarhus's class (`app/station_scope.py`), and the page says so.
- **The line between the two is the owner's.** When a slow route is more
  than an outlier, bring the share of stops it alone serves.

## 2. Stations - every stop

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
- **New Orleans keeps every stop** (owner, 2026-09-30, call 13). Its
  streetcar stops stand a block or two apart (164 m median), so the rings
  merge into a band along each line. The kit's handoff had named it the one
  exception for the street-stop filter, but the filter's own shape test
  (`docs/sub_transit_line_filters.md`, "When this applies") fails. That
  filter is for a central corridor with sparse stations plus dense surface
  branches (Muni Metro, Boston's Green Line). **New Orleans is uniformly
  dense, with no corridor**, the case the doc says not to thin. Thinning
  would also leave a business a block from a stop outside the rings. The
  band is a true reading of distance from the line, and the page says so
  (section 6).
- **A line mostly outside the scope is a stub question**, as for the Czech
  and French cities. Decided (owner, 2026-09-30):
  - Florence's T1 is drawn to its end, with its 4 Scandicci stops listed as
    outside (call 17);
  - Den Haag's E is left out as a stub (call 22);
  - Zurich's Glattalbahn lines take the stub test one by one, and a stub is
    dropped (call 19);
  - Göteborg's 4 and 12 are drawn to their ends, with the Mölndal stops
    listed as outside, unless the stub test fails (call 21).
  Where the business source covers the city only (Zurich, Göteborg, Den
  Haag's horeca layer, Florence), **the scope cannot go regional**, so
  France's scope rule does not apply.

## 3. Rings - the spacing rule

Measure the **median nearest-neighbour gap among the stations in scope**,
after collapse, with every stop kept.
- **About 550 m or less**: `RING_EDGES_MILES = [0.0, 0.05, 0.1, 0.2, 0.3]`,
  `RING_LABELS = ["0-0.05 mi", "0.05-0.1 mi", "0.1-0.2 mi", "0.2-0.3 mi"]`
  (Aarhus's config). The config comment records the figure.
- **Over about 550 m**: the standard `[0.0, 0.1, 0.2, 0.3, 0.6]`. Drop the
  page's half-size sentence. A build figure between 540 and 570 m goes to the
  owner with both in-ring shares. Kansas City read about 560 m as a mean at the
  screen, but **413 m as a median over OSM's 19 stops in its brief**, so it
  takes halved rings.
- The briefs' gaps (2026-09-30): Odense 441 m, Daugavpils 298, Liepāja 329,
  Kansas City 413, Florence 322, Tucson 265, New Orleans 164, Zurich 283,
  Göteborg 378, Den Haag 335. **All ten take halved rings**; recompute on the
  stations actually drawn.
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
- **Read the licence before a feed is used**, with one `licence-read` per
  source (`read-licence`). RTA's and GEST's GTFS are unread, and neither
  brief uses them. **RideKC's GTFS is barred (owner, 2026-09-30)**: ridekc.org's
  site terms restrict schedules and require written consent, Philadelphia's
  shape. So Kansas City's frequency is stated as a fact, without citing the
  schedule, and the KC Streetcar and RideKC logos are never used.
- **OSM through `osm-rail` is the rail source for every brief so far.** It
  is used where a feed is unlicensed, barred, or simply not needed for
  geometry: Odense (Rejseplanen barred), Daugavpils and Liepāja (no declared
  licence), Kansas City (barred), New Orleans, Tucson and Florence. Zurich,
  Göteborg and Den Haag were measured on OSM at their screens. OSM is covered
  by the site's OpenStreetMap notice. Say on the page that the lines and
  stops come from OpenStreetMap.
- **Relations with no stop members are placed in `NOT_DRAWN` with a reason**,
  never dropped silently: New Orleans's 46 and 49 (read whether they run),
  and Florence's T3.2.1, T3.2.2, T2.2 and T4 (under construction; re-check
  when T3 opens, due end of 2026).
- **Colours**: the feed's `route_color`, else OSM's `colour`. A CSS keyword is
  resolved through the named-colour table: New Orleans's `green`, `red` and
  `blue`, Göteborg's line 11 "black". Otherwise use the project's own
  palette, as Le Havre and Riga have: Odense, Daugavpils, Liepāja, Kansas
  City and Tucson. Run `pipeline/linecolour.py`'s checks and
  `check_map_markup.py`. Two lines with one colour are refused (Dijon).
- **Every drawn line gets a permanent on-map label (its real public name) and
  a legend entry.**
- **Shared code where it pays: `pipeline/osm_tram.py`, one module for both
  kits** (agreed with the Czech kit, 2026-09-30). Seven of these ten briefs
  take OSM rail, the other three were measured on it, and five of the six
  Czech cities do too. **Use it. If it does not exist yet,
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
| Den Haag | Merged | `narrowed` | **Rotterdam's shape** (BAG winkelfunctie plus the horeca layer), which is `narrowed`, "Merged". Approved `narrowed` over the tram list's "full" (owner, call 23) |

**A narrowed or one-bucket page says what is missing in its own paragraph**
(section 6), and `check_scope_disclosure.py` holds it to
`docs/excluded_categories.md`. The layer control names only the categories
the map has (Riga's "Shops and services, and Food service").

## 6. Page text - approved by the owner, word for word (2026-09-30)

Braces are per-city facts, filled from this city's own measurements (step 1,
step 2 and the rendered map), never from the brief's screen figures. A
paragraph in braces appears only where it applies. The controls paragraph and
the heat-layer caveat stay exactly as on the built pages (Aarhus's and Riga's),
with the category names this map has. The transit caption comes from
`provenance.json`, with the operator's credit and any notice its licence
requires.

> {N} {operator} tram lines are drawn, **{lines}**, each labelled on the map
> and in the legend, redrawn from {OpenStreetMap's route geometry}{, in
> colours this project chose, since the source records none}. {City} has no
> metro: its trams are its rapid transit, as Riga's are, so every tram stop
> gets rings. {Trams run about every {n} minutes by day{; less often in the
> evenings}.} {Buses{ and suburban trains} are not drawn{: why}.}
>
> The map covers the **{city unit}**. {Where a line runs past it: "{Line}
> runs on into {place}, so its {k} stops there are left out. The line is
> still drawn to its end, but those stops get no ring and their businesses
> are not counted. They are listed in `outputs/{slug}/excluded_stations.csv`."}
>
> {The business source, in the template city's wording: which register, how
> the dots are placed, and whether a dot shows a name, a type or an address.}
>
> {Narrowed or one-bucket only: "**This map has {one category / two
> categories}, not three.** {What the source holds, and what is missing.}"}
>
> {Kansas City: "**The licence data dates from 15 January 2026**, and holds
> licences valid for 2025 and 2026. Businesses that opened or closed since
> then are not shown." Göteborg: "**The register carries no dates.** It lists
> the food businesses active on the day it was fetched ({date}), and says
> nothing about when each opened." Den Haag (owner, call 27): "**The permit
> data runs to 2025.** The city last edited its permit layer on 23 May 2025,
> so premises that opened or closed since then may be missing or still
> shown."}
>
> **Read the density as a register, not a street survey.** {The source's own
> caveat, and this city's ratio to OpenStreetMap.}
>
> **Tram stops sit closer together than metro stations**, a median of
> {spacing} m here, so the rings are drawn at half the usual size (0.05 to
> 0.3 mi). **About {share} of storefronts sit within a ring.** {New Orleans:
> "Streetcar stops here stand a block or two apart, so the rings join into a
> band along each line. Read them as distance from the line."}
>
> {The controls paragraph and heat-layer caveat, word for word as on the
> built pages, with this map's category names.}

A city whose median stop gap is over about 550 m keeps the standard rings
and drops the last paragraph's first sentence. Where the rail comes from a
feed rather than OpenStreetMap, the first sentence names the feed ("from
{operator}'s own published timetable feed"), as France's template does.

**Departures are owner calls, never edits.** Anything that does not fit the
template goes to the owner as a proposed sentence.

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
Tucson's `ACC_NAME` on personal ownership types, Florence's beauty and
laundry points (no names, but sole traders' premises) and Den Haag's
`AANVRAGER`**);
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
| **Daugavpils** | **Riga** (`pipeline/riga/`, `taxonomies/riga_source.py`) | VID excise (food, placed on VZD's `aw_eka.csv`) + VZD cadastre use class 1230 (shops and services), ATVK 0002000 | OSM, **routes 1-5, all drawn** (owner, call 28): 38 stop names; the page states the waits (route 1 every 10-15 min, the Stropu loop 20-30, routes 2 and 4 about hourly) | 32635 | `aw_eka.csv`'s `KOORD_X` is the northing (EPSG:3059); use `DD_N`/`DD_E`; `STATUSS` = EKS; the VZD credit (notice 42 extended); hourly routes (section 1) |
| **Liepāja** | **Riga** | as Daugavpils, ATVK 0005000 | OSM, ref 1; + Brīvības iela and Klaipēdas iela by node | **32634** | as Daugavpils |
| **Kansas City** | **Houston** (a US register, the sole-owner name rule); `naics.py` through a NAICS 2022 **title** map | Socrata `kkhs-93m4`, Public Domain, **frozen 2026-01-15**; `valid_license_for` 2025 and 2026 only; fee-code types ("Misc Rate 129") dropped and counted | **OSM** (RideKC's GTFS barred, owner), ref 601, 19 stops, all inside; 413 m | 32615 | The data date on the page; `dba_name` withheld where it is a person; no logos; frequency as a fact, not a cited schedule |
| **New Orleans** | Philadelphia (a US text taxonomy, `premises-taxonomy`) | Socrata `iqay-p646`, CC0, daily; drop "Special Events-Other (Vendor)" and "Home Based-Office Use Only"; `ownername` never shown | **OSM**, streetcars 12, 47, 48 and 2, 110 stops, all inside; 164 m | 32615 | Every stop kept (owner, call 13); 46 and 49 have no stops (`NOT_DRAWN` unless they run); CSS-keyword colours |
| **Tucson** | **Houston** (the sole-owner name rule); `naics.py` unchanged | BUSLIC **layer 3** (never layer 1), active (strip `LIC_STATUS`) and `HOME_OCCUPATION` = F; licence SILENT, permissive reading (owner, 2026-09-30) | **OSM**, Sun Link, 21 stops, all inside; 265 m | 32612 | Notice "Business licence data: City of Tucson"; never call the pins complete; `ACC_NAME` withheld for Sole Proprietorship, Individual and Married; 10 min weekdays 07-18, 20 otherwise, disclosed |
| **Florence** | **Milan** and **Rome** (the Comune's layers; Milan's *fuori piano*) | Four Comune GeoJSON layers (`datigis.comune.fi.it/json/`), EPSG:3003, no names or addresses (the dots show the type); licence read: CC BY 4.0, credit the Comune di Firenze and state the changes | **OSM**, T1 and T2 in OSM colours, 39 stops in the comune (T1 20 of 24); 322 m | 32632 | 639 exempt food rows kept, non-public ones filtered (owner, call 16); Scandicci's 4 stops outside; 3,424 rows share a point; T3 under construction (`NOT_DRAWN`); no giglio or logo |
| **Zurich** | **Stockholm** (one register, city only), Seoul/Gyeonggi (partial retail) | `Gastwirtschaftsbetriebe` via the **WFS** (the CKAN downloads are an Angular shell), layer `gastwirtschaftsbetriebe`, CC0, 3,487 rows all `Offen` and 2026: food 2,325 + partial retail 1,028 (Kleinverkaufsstelle, Kiosk, Tankstelle) | **OSM**: trams 2-11, 13-15, 17, 182 stops; 283 m. Out as stubs: Forchbahn S18 (20%), Glattalbahn 12 (11%), Limmattalbahn 20 (15%); 50 and 51 only if they meet the 20-minute floor | **2056** | **`add-country` first**; the S-Bahn and Forchbahn named as excluded |
| **Göteborg** | **Stockholm** (`taxonomies/sweden_livsmedel.py`) | `Livsmedelsverksamheter`, CC0, daily: **take the CSV** (`utf-8-sig`, `;`), never the rowstore JSON; 5,066 rows: food service 2,167, food shops 906; 274 blank `typ` classified by name (about 74 kept) or dropped | **OSM**: trams 1-13, 127 stops; 378 m; 4 (75%) and 12 (72%) drawn to their ends with five Mölndal stops outside; Lisebergslinjen out | **UTM 32N** (11.97° E; not Stockholm's 34N) | Undated rows (the page says so); line 1's OSM colour is white (check contrast; Lille's darkening if it fails); take the hex where a relation has two colour values |
| **Den Haag** | **Rotterdam** (BAG, `taxonomies/rotterdam_source.py`); Amsterdam for the horeca precedent | BAG winkelfunctie units (6,560) + `Horeca_nieuw` layer 2 (2,543 granted or notified, about 2,352 food after exclusions; edited 2025-05-23) | **OSM**: 14 HTM lines, 161 stops; 335 m; RandstadRail E out; tram 1 keeps 19 of 37 (51%) | UTM 31N, as Rotterdam | **Never fetch `AANVRAGER`, `KVKNUMMER` or `RECHTSVORM`**; the trade name is `OMSCHRIJVI`, double-encoded UTF-8 to repair; 1 and 19 share `#c01115` (one moves); 10 and 34 need colours; the layer's date on the page |
