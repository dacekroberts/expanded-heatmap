# Decisions drafts: tram-rescope

Newest first. Cleanup folds these into `DECISIONS.md` at review time.

### 2026-10-13 - Tram rescope: Milan built with all 17 tram lines (owner); page text and stop-name form are drafts

- **Owner, 2026-10-13: "i agree with your applications from precedent.
  project colors okay. all 17", then "build now and add the re-check to
  the future logs".** So: all 17 routes as "Tram N"; 7 and 33 drawn at
  exactly 15.0 minutes; the five routes on diversion drawn as the
  timetable ran them; 15 and 31 drawn whole with their stops outside the
  comune listed; half-mile thinning with the crossing-or-junction rule
  (Toronto's, approved there the same day).
- **Built on the branch** (`pipeline/milan/trams.py`, steps 1 and 3):
  22 lines, 193 stations (104 metro + 89 tram). 710 tram stop ids on
  regular patterns make 312 places; 46 are a drawn metro station, 19 are
  outside the comune, 158 are thinned. Keeping every stop shared by two
  or more lines would have kept 137 new stations instead of 89.
  Storefronts in a ring: 45,999 of 47,540 (41,510 before).
- **Colors** in `config.TRAM_COLOURS`: every tram 45 or more from every
  pin (closest 45.2, Tram 12 against Retail); `check_line_colours` passes
  at render. The search ran on each route's most-used shape.
- **Labels:** `scripts/check_map_labels.js` reports no problem at 1024,
  375 and 343 wide; 22 labels, 22 legend rows, the legend scrolls.
- **Judgment calls made in the build, for the owner at review time:**
  - *Stop names.* The feed writes them in lower case ("p.za ventiquattro
    maggio"). They are shown as "P.za Ventiquattro Maggio": a capital on
    each word, small Italian words and the second half of "p.za", "v.le",
    "c.so", "l.go", "p.ta", "p.le" left small. The metro stations keep
    ATM's upper-case names from its GIS layer, so the two forms sit side
    by side on one map.
  - *A stop the feed names for its metro lines* ("stazione centrale m2
    m3") is that metro station when one is within 400 m; otherwise 150 m.
  - *One stop id has no name* (17369) and is left out.
  - *"Via Curiel Via Maggi (Rozzano)"* is drawn: its point is inside the
    comune's polygon whatever its name says.
- **Page text is a draft** (The lines bullets of
  `app/pages/20_Milan_Heatmap.py`), as are the Milan sentences changed in
  `docs/excluded_categories.md`: Milan taken out of the "trams left out"
  example, added to the spacing-filter list, and a new Stations paragraph.
- **Re-check:** `docs/recheck_calendar.md`, action list and calendar row.
  Step 1 stops if the feed's surface dates or tram route list differ from
  the config, so a new edition cannot be drawn unread.
- **Branch-only paths:** `config.TRAM_DIR` is `processed/tram/`; at
  landing set it to `DATA_PROCESSED` and re-run steps 1 and 3.
  `baseline.json` is not updated and no drift check ran (step 2 writes
  the shared folder). Step 2 is untouched, so no privacy re-read is owed.
- **Owed later:** Toronto's and Milan's modules are near copies; a shared
  one belongs with Prague, the third use.

### 2026-10-13 - Tram rescope: Milan's 17 tram routes measured; the line list is with the owner (open, nothing built)

- **The feed.** `https://dati.comune.milano.it/gtfs.zip` re-pulled
  2026-10-13 as `data/milan/raw/gtfs_2026-10-13.zip`: byte-identical to the
  cache of 2026-09-22 (sha256 f0959217..., feed_version 423, the portal's
  resource last modified 2026-09-21). Its `feed_info.txt` says
  `surface_end_date` 20261002: every tram service runs 2026-09-14 to
  2026-10-02 and none after. No newer edition is published, so the tram
  timetable read here ended eleven days before the reading.
- **17 tram routes** (1, 2, 3, 4, 5, 7, 9, 10, 12, 14, 15, 16, 19, 24, 27,
  31, 33), no night routes, no replacement-bus trips under a tram id
  (headsigns read). Weekday 2026-09-30, 10:00 to 15:00, busier direction:
  headways 4.5 (14) to 15.0 minutes (7 and 33, 20 trips each way in five
  hours). All 17 pass the 15-minute test; 7 and 33 sit exactly on it.
- **Works in the feed's own route names:** 2 ("lav. torino"), 4 ("lavori
  testi"), 7 ("lavori prol per c.na gobba"), 14 ("lav. orefici"), 16
  ("lav. umbria - maj"). The precedent is drawn as the timetable runs.
- **Scope:** 722 tram stop ids, 341 stop names, 323 names inside the
  comune. Route 15 has 17 of 62 stop ids outside (Rozzano) and route 31
  has 18 of 31 outside (Cinisello Balsamo). No `parent_station`.
- **Colors (measured, `pipeline/linecolour.py`, most-used shape per
  route):** 17 project colors fit beside the five metro colors at a pin
  floor of 45; closest pair within 500 m 41.7 (M2 and tram 4); dark-mode
  labels separate; `check_line_colours` passes. A tram has 12.3 other
  lines within 500 m on average (18 at most). Label placement for 22
  lines is not measured.
- **Recommended to the owner, not decided:** all 17 as "Tram N", drawn as
  the timetable runs, stops outside the comune listed, half-mile thinning
  as in Toronto.

### 2026-10-13 - Tram rescope: Toronto's thinning rule, colors and page text approved (owner)

- **Owner, 2026-10-13: "1 yes sounds good. 2. approved. 3. concatenate if
  possible but content looks good".** (1) The crossing-or-junction form of
  the interchange filter stands for Toronto. (2) The eight streetcar
  colors are approved as recorded in `pipeline/toronto/config.py`. (3)
  The page bullets' content is approved; they were shortened the same day
  with no fact added or dropped (the lines bullet takes the labeling
  clause, the colors bullet loses its second explanation of Line 2, the
  not-drawn bullet takes the "listed below" pointer). The Overview blurb
  and the What Is Excluded additions went with them.

### 2026-10-13 - Tram rescope: the sources behind Toronto's closed routes (owner: "save sources")

Search results of 2026-10-13, none read in full; the feed, not these,
decided what is drawn. The same links are in `docs/recheck_calendar.md`.
- 507 Long Branch, bus-replaced from 2026-06-07 for the Long Branch Loop
  track renewal, phase 2 to 2026-10-31:
  https://www.ttc.ca/about-the-ttc/projects-and-plans/Long-Branch-Loop-Track-Renewal
  and
  https://www.ttc.ca/service-advisories/Service-Changes/501-301-507-508-Long-Branch-Loop-Streetcar-Track-Renewal-Work
- 512 St Clair, bus west of Lansdowne to 2026-10-31 for the rail bridge:
  https://www.ttc.ca/service-advisories/Service-Changes/512-312-Route-change-due-to-rail-bridge-construction
- 503 and 508 during about ten months of King Street West construction
  (news): https://www.blogto.com/city/2026/09/toronto-construction-busiest-ttc-routes-10-months/
  and the City's page, https://www.toronto.ca/kingwestconstruction
- The TTC's running list of streetcar changes, the page to re-read after
  2026-10-31: https://www.ttc.ca/service-advisories/Streetcar-Service-Changes
- The feed itself: the City's CKAN package `ttc-routes-and-schedules`
  (`config.GTFS_URL`), cached as `data/toronto/raw/gtfs.zip` (2026-09-21)
  and `gtfs_2026-10-13.zip`.

### 2026-10-13 - Tram rescope: Toronto built with eight streetcar lines; 503, 507 and 508 not drawn (owner)

- **Owner, 2026-10-13: "follow those rules (8 not 11) note the drops and
  reasoning".** Drawn: 501 Queen, 504 King, 505 Dundas, 506 Carlton, 509
  Harbourfront, 510 Spadina, 511 Bathurst, 512 St Clair, beside Lines 1,
  2, 4, 5 and 6 (13 lines).
- **The three drops and the rule behind each** (`docs/category_rules.md`,
  "Station scope"):
  - **503 Kingston Rd, 507 Long Branch: closed for works.** Every trip in
    the feed to 2026-10-31 is a replacement bus, so they are drawn as the
    timetable runs, which is not at all (Berlin's U6 Tegel branch,
    Prague's Flora). 15 and 31 stops of their own are listed as closed
    for works.
  - **512 St Clair west of Lansdowne: closed for works.** The line is
    drawn to Lansdowne; 10 stops west of it are listed.
  - **508 Lake Shore: the 15-minute test.** 35 weekday peak trips, none
    between 09:00 and 15:00 (Aarhus). Every stop it serves is on a drawn
    line, so it adds no row.
  - The seven night routes run their day routes' streets (owner's list).
- **They come back by themselves being noticed:** `streetcars.py` compares
  config's closed and infrequent sets with the feed and stops the build
  when a line returns, closes or changes frequency.
  `docs/recheck_calendar.md` carries the dates and what to do (owner,
  same day: "put in the timeline into the timetable documentation of
  future openings/updates i need to check"), with Mexico City's unopened
  cable lines beside them.
- **Stop selection** (`pipeline/toronto/streetcars.py`): replacement bus
  trips left out by headsign; 506 stop ids grouped into 237 places by
  distance (60 m, or 120 m when two stops share no line and direction; no
  merge past 200 m; same-named stops first). 15 places are a drawn
  rapid-transit station (within 150 m, or named for it within 400 m) and
  add nothing. The rest take the sub-transit-line filters at half a mile.
- **Judgment call, on a measurement:** filter 4 ("a stop shared by two or
  more lines is kept") is narrowed to the stop that has a line its
  neighbor lacks (a crossing, or the last shared stop before two lines
  part). With every shared stop kept: 82 new stations; with the narrower
  rule: 68, then 66 after two pairs closer than 150 m were merged.
- **Result:** 108 rapid-transit + 66 streetcar = 174 stations; 156 stops
  thinned, 56 closed for works, 2 outside the city. Storefronts in a ring
  8,749 -> 11,803 of 18,215. Labels pass at 1024 and 375 wide, 13 labels.
- **Colors: the project palette**, since the TTC gives every streetcar one
  red. From the color search with Lines 1 to 6 held: 501 #608000, 504
  #00A800, 505 #0050F8, 506 #886010, 509 #C870C8, 510 #F80028, 511
  #A000F8, 512 #00A0C0; every one at least 45 from the pins and 35 from
  every other line. **For the owner's eye; not yet approved.**
- **Page text is a draft for the owner:** the Toronto page's four new
  bullets, the Overview blurb, and the Stations paragraph and two list
  additions in What Is Excluded.
- **Left for landing (Cleanup):** `STATIONS_CSV` and
  `STREETCAR_SHAPES_JSON` point at `processed/tram/` on this branch; drop
  "tram" and re-run steps 1 and 4. `baseline.json` is not updated (step 1
  emits six new figures), and the drift check was not run from the branch
  because Toronto's step 2 writes the shared processed folder. Step 2 is
  untouched, so no new privacy read is owed. `check_all.py`: 72 of 73, the
  one failure Mexico City's search check, as agreed.

### 2026-10-13 - Tram rescope: Toronto's line list approved, then the feed shows three routes not running as streetcars (open, owner)

- **Owner, 2026-10-13: "yes"** to Toronto's list: Lines 1, 2, 4, 5 and 6
  unchanged, the 11 day streetcar routes 501 to 512 added ("Streetcar 501"
  on the map, "Streetcar 501 Queen" in the legend), the 7 night routes not
  drawn.
- **What the feed then showed (read-only, the cached feed of 2026-09-21 and
  a re-pull of 2026-10-13 under `gtfs_2026-10-13.zip`, window to
  2026-10-31; both agree):**
  - 503 Kingston Rd and 507 Long Branch run as replacement buses on every
    trip (1,098 of 1,098 and 1,603 of 1,603; headsign "Replacement Bus").
  - 506 Carlton and 512 St Clair run streetcars and a "B" replacement bus
    side by side (1,010 of 2,025 and 1,101 of 2,462 trips are buses).
  - 508 Lake Shore runs 35 trips, weekday peaks only: no weekday trip
    between 09:00 and 15:00, so it fails the 15-minute test
    (`docs/category_rules.md`, "Station scope").
- **The precedents:** a stretch closed for works is drawn as the timetable
  runs (Berlin's U6 Tegel branch, Prague's Flora, 2026-09-28/29), and a
  stretch under the 15-minute test is not drawn (Aarhus). Applied here that
  is 8 streetcar lines, not 11. The owner approved 11, so this goes back
  to the owner before anything is built.
- **In progress, uncommitted on the branch:** `pipeline/toronto/streetcars.py`
  and config constants. Stops are grouped into places by distance (the
  feed names stops per direction and has no parent stations), replacement
  bus trips are left out, and the sub-transit-line filters thin the rest
  (rapid-transit stations and terminals kept, one stop per half mile). The
  interchange filter is narrowed to crossings and junctions, because 503,
  504 and 508 share King Street for kilometres: with every shared stop
  kept the dry run gave 141 new stations, with the narrower rule 107
  (before the bus trips were taken out; to be re-measured).

### 2026-10-13 - Tram rescope: the many-route rule is per route (owner), and Prague's colors fit it (measured)

- **Owner, 2026-10-13: "yes per route sounds good".** Toronto, Milan and
  Prague take the rule the built tram maps already follow (Amsterdam's 16
  trams, Brussels, Zurich, Ostrava, Brno, Göteborg): one on-map label and
  one legend row per day route, named "Tram N" (Toronto: "Streetcar N").
  Night routes are not drawn, since they run the day routes' streets
  (Toronto's 301 to 312, Prague's 91 to 99), and the page says so. All
  three operators give every tram one color, so colors come from the
  project palette by the color search. Toronto's Lines 5 and 6 keep their
  own names and feed colors.
- **Not chosen: grouping by corridor (New York's trunks).** New York's
  groups are the operator's own; none of these three publishes tram
  trunks, so the groups would be the project's. Kept only as the fallback
  if Prague's labels cannot be placed.
- **Prague's colors, measured at the owner's request (read-only).** Each
  tram route's most-used GTFS shape, Metro A, B and C on their built
  colors, the sRGB cube in steps of 8, farthest-point greedy with the
  most-crowded line first. Rules: 3:1 on both pages, CIE76 18 from every
  line within 500 m, 10 from every other line, and a pin floor.
  - 25 day routes (1 to 13, 15 to 26), 28 lines: fits at pin floors 45, 30
    and 20. At 45: 3,817 colors available, closest pair within 500 m 27.1,
    closest tram to a pin 45.2.
  - With 31, 32 and 40 as well, 31 lines: fits at all three floors; at 45
    the closest pair within 500 m is 25.1.
  - A tram has 22 other lines within 500 m on average (most 27 of 27), so
    nearly every pair is held to 18. Dark-mode labels separate and
    `check_line_colours` passes in every run.
- **Limits:** the colors found are a feasibility result, not the palette a
  build would record. Label placement for 28 labels is not measured. Metro
  C stays 21.2 from the Food service pins, as built.

### 2026-10-13 - Tram rescope: Toronto, Milan and Prague pass the overlap test (measured, nothing built)

- **The test that left Barcelona's trams out, run on the three cities not
  yet started.** Tram stops are each city's cached GTFS stops served by
  `route_type` 0, collapsed on the stop name; distances in the city's own
  UTM zone; the storefronts are the built map's. Read-only.
- **Toronto:** 558 tram stops on 20 routes; 305 (55%) are beyond the 0.6
  mile outer ring of all 108 drawn stations (median 1,174 m). Storefronts
  beyond every ring: 9,466 of 18,215 (52.0%) now, 5,855 (32.1%) with the
  tram stops ringed; 3,611 gain a ring.
- **Milan:** 325 tram stops with a storefront in reach, on 17 routes; 66
  (20%) beyond every drawn station (median 408 m). Storefronts beyond every
  ring: 6,030 of 47,540 (12.7%) now, 1,467 (3.1%) with the trams; 4,563
  gain a ring.
- **Prague:** 285 tram stops on 37 routes; 95 (33%) beyond every drawn
  station (median 720 m). Storefronts beyond every ring: 7,657 of 25,185
  (30.4%) now, 3,678 (14.6%) with the trams; 3,979 gain a ring.
- **Reading:** none is Barcelona's case (0 of 28 stops beyond, 0
  storefronts gained). The trams reach storefronts the metro does not in
  all three, so the open question is the label and legend rule for 17 to
  37 routes on one map, not whether to draw them.
- **Limits:** the route lists include night routes (Toronto's 300s,
  Prague's 91 to 99) that repeat day routes' streets, and Toronto's
  `route_type` 0 includes Lines 5 and 6; neither changes the storefront
  counts. Stops are collapsed by name, not by the station rule a build
  would use.
- **Cleanup's sequencing for Mexico City (its message, same day):** the
  search rebuild waits for the second search rule batch on master and
  lands in the tram segment of the final group; `PLACE_AREA` and the place
  caches are not touched on this branch, and `check_place_search.py` stays
  failing here until then.

### 2026-10-13 - Mexico City (Regional): Tlalnepantla de Baz added, page text approved, the title names the cable cars (owner)

- **The owner: "1 add, 2 bullets looks good, Tlalnepantla added. 3. name
  cable cars"**, to three calls: add Tlalnepantla de Baz as a fifth
  municipio (against leaving Mexicable Línea 2's four stations out); the
  drafted page bullets for the cable cars, with the municipio added; and a
  map title that names the cable cars (against keeping "Metro CDMX:
  commercial density around stations"). The precedent stated for adding it:
  Naucalpan, kept for one station.
- **Scope now:** Ciudad de México and five municipios (`cve_mun` 104,
  relation 5606521, 80.3 km²; the union 494.2 km², gated at 410 to 600).
  The five boundaries are a new cache,
  `osm_municipios_15_2026-10-13.json` (overpass.kumi.systems, after a 504
  from overpass-api.de); master's four-municipio cache is untouched. No new
  download: the cached State of México register holds Tlalnepantla.
- **Figures:** 208 stations (204 plus the four), none left out, and no
  station's rings reach outside the scope. 427,123 storefronts written
  (407,629 before), 427,121 on the map after the contact scrub, 175,939 in a
  ring. Tlalnepantla brings 19,483 storefronts; 405 entidad 15 storefronts
  fall outside the scope polygon (416 before).
- **Privacy verdict: publish, the same structural position as before.**
  `check_personal_exposure.py mexico_city` over 175,939 pins: no
  registrant-name column is loaded, 0 e-mails and 0 phone numbers in a
  displayed name, the one c/o the same sign abbreviation, 33.1% on the
  person-name heuristic (32.2% before; the Spanish sign convention). The
  19,494 added rows were read for contact details: five long digit runs,
  all LICONSA outlet numbers, and one e-mail-shaped sign name, which the
  render's contact scrub drops. Cleanup: this needs its row in
  `docs/privacy_verdicts.md` when the entry is folded.
- **Wording (branch, for review):** the map title is "Metro CDMX, Cablebús
  and Mexicable: commercial density around stations" and the Overview blurb
  "Metro CDMX (Líneas 1–9, A, B and 12), the STE Tren Ligero and the
  Cablebús and Mexicable cable cars, with five State of México municipios";
  the owner asked for the cable cars to be named and did not see these
  exact strings. The page's regional bullet gained one sentence
  ("Mexicable runs through Ecatepec and Tlalnepantla.") and "four" became
  "five". `docs/excluded_categories.md`'s regional paragraphs carry the
  five-municipio counts, each recomputed by a script that first reproduced
  the published four-municipio figures exactly; its sentence on rings
  crossing the city line is replaced, since none now does.
- **Not done, and it blocks the drift check: the search index.**
  `step2b_place_index.py` refuses, as check H does: San Isidro has no
  indexed place within 1 km, because `PLACE_AREA` does not cover
  Tlalnepantla. It needs area id 3605606521 added, a place fetch under new
  cache names, the index rebuilt and the new rows read. Left to Cleanup
  with the search work (the handoff's rule). Until then
  `outputs/mexico_city/baseline.json` and `place_search.json` are not
  updated, and `check_all.py` fails on `check_place_search.py` alone (72 of
  73; `macro_facts.json` and Mexico City's row of `ring_shares.json` were
  rewritten). `check_deploy_imports.py` was not run: this worktree has no
  `.venv-lean`.

### 2026-10-13 - Mexico City (Regional): the cable cars built on the branch; colors and names (owner); Tlalnepantla open

- **The owner, on the Cablebús colors: "darker project shades sounds good,
  feel free to use other colors if we run into color similarity
  conflicts"**, to "three drawn lines, the system blue on Línea 1 and two
  darker project shades on the others, and the page saying so", against one
  legend entry for all three. **On the Mexicable names: "labels sound
  good"**, to "Mexicable Línea 1" and "Mexicable Línea 2" in a red and a
  green chosen by this project, against the operator's Línea Roja and Línea
  Verde.
- **Colors (branch, inside those calls; `pipeline/mexico_city/config.py`,
  `CABLE_COLOURS`):** Cablebús Línea 1 #4EC3E0 (es.wikipedia's system blue),
  Línea 2 #1f96b3 (16.4 from Línea 1), Línea 3 #135c6d (23.9 from Línea 2);
  the nearest Metro line to any of the three is Línea 4 at 23.5, the nearest
  pin Retail at 44.4. Mexicable Línea 1 #d85868, the color nearest
  Wikipedia's reds that clears every pin by 20 and every line by 18 (Food
  service 20.8, Línea 1 27.9, Línea 6 37.7). Mexicable Línea 2 #79a133,
  es.wikipedia's map green #95C344 darkened 10% for 3:1 on a white page
  (Línea 12 25.5, Línea 8 28.4, Personal services 38.5).
- **Built (commit bff95ea7), nothing on master's path touched.** Steps write
  `data/mexico_city/processed/regional/cable/` until landing; the landing
  commit removes the `cable` part of `DATA_PROCESSED` and re-runs steps 1 to
  3. Step 2 did not change, and its output was copied into that folder.
- **Stations: 180 to 204 in scope.** 33 cable station points give 28 new
  stations, 24 in scope and 4 outside. Gate 3 runs per cable line and
  matches: 6, 7, 6, 7, 7. Ecatepec goes from 5 stations to 13
  (`STATIONS_PER_MUNICIPIO`). Storefronts inside a ring: 149,980 to 172,362
  of 407,628.
- **Same-named interchanges attach, and no existing station moves**
  (asserted in step 1, and compared row by row: 0 of 180 moved). Indios
  Verdes (345 m at the farthest cable node), Constitución de 1917 (171 m)
  and Santa Marta (150 m) keep the Metro station's point and get no second
  station. Mexicable's two Hank González nodes, 30 m apart, are one station.
  Los Pinos / Constituyentes (Cablebús Línea 3) stays its own station 154 m
  from the Metro's Constituyentes: a different name, as Barcelona's Sant
  Gervasi and Plaça Molina are.
- **A name two places carry:** Mexicable's Periférico is 26 km from the Tren
  Ligero's Periférico; the attach check raised on it, and the Mexicable one
  is shown as "Periférico (Mexicable)".
- **Cablebús Línea 3's stations are named in config by OSM id** (three ways,
  three relations), since its relation holds no station member; its count
  of six is from es.wikipedia only. Re-measure if the relation gains
  members.
- **Shared code:** `map_common.load_osm_line_shapes` takes a relation id in
  place of a `ref`, because the five relations' refs are "1", "2", "3", "1",
  "2". No other map's output changes.
- **Checked:** line identity, no-fetch, em dashes, scope disclosure,
  provenance (names the city OK), map markup (237 maps, 0 problems); the 18
  labels by the label check's own tests at 1024 and 375 wide, 0 problems.
  Not yet run: the drift check, the privacy check (step 2 unchanged), the
  full `check_all.py`.
- **Open, the owner's: Tlalnepantla de Baz.** Mexicable Línea 2's four
  middle stations stand in its detached eastern part. Measured from the
  cached register: Tlalnepantla has 19,483 storefronts under this map's
  filter, 5,260 of them in the eastern part and 2,940 within 0.6 miles of
  the four stations. Precedent for adding it: Naucalpan, kept for one
  station (22,216 storefronts). Recommended: add it, in the same build. As
  built, the four are in `outputs/mexico_city/excluded_stations.csv` and
  the line is drawn through.
- **Owed before landing:** the page's bullets for the cable cars (a draft,
  the owner's to approve), `docs/excluded_categories.md` (it still says
  Mexicable is not drawn), `docs/map_inconsistencies.md` (the table row and
  item 12), `docs/data_sources/mexico.md`, the brief's line 24, the map
  title and `system_name` (they still read "Metro CDMX and Tren Ligero"),
  the search index rebuilt on the new stations (Cleanup).

### 2026-10-13 - Mexico City (Regional): Cablebus and Mexicable both drawn (owner)

- **The owner: "1. draw both"**, to "Draw both: one rule for cable cars on
  one page, and Ecatepec's hill districts get rings", against drawing
  Cablebus alone with a different stated reason for Mexicable. This
  supersedes the Mexicable half of the call of 2026-10-04 ("Out, the
  owner's call: ... Mexicable (a cable car)",
  `docs/build_briefs/mexico_city_regional.md`); the Tren Suburbano and El
  Insurgente stay out on commuter spacing. Toulouse's Téléo is the
  precedent for a drawn cable car.
- **Not yet verified, and the build checks each before drawing:** which
  Mexicable lines are in revenue service and which of their stations fall
  inside Ecatepec and Naucalpan; each system's own line names, colors and
  station counts; the cable geometry.
- **Measured later the same day; nothing built.** OSM, one Overpass query
  (overpass-api.de, after four failed attempts on both mirrors), cached as
  `data/mexico_city/raw/osm_aerialway_2026-10-13.json`, 80 elements: five
  `route=aerialway` relations (Cablebús Línea 1, 2, 3; Mexicable Línea 1,
  2), none with a `colour`. Cablebús Línea 3's relation holds one node and
  one way; its six stations are ways and relations, so step 1 cannot take
  that line from relation membership alone.
- **Five lines are in service; Mexicable Línea 3 (Naucalpan) is not** (OSM
  `construction=gondola`; press gives the first quarter of 2027), nor
  Cablebús Líneas 4 to 6. Operator station counts: Mexicable Línea 1 seven
  and Línea 2 seven, from the operator's own site script (mexicable.com,
  primary, read 2026-10-13); Cablebús Línea 1 six and Línea 2 seven from
  archived copies of STE's pages (primary, dated 2024 and 2026-05-23);
  Línea 3 six from es.wikipedia only (secondary). ste.cdmx.gob.mx refused
  every connection, as every cdmx.gob.mx host has.
- **Scope, by point in polygon:** all 19 Cablebús stations are in Ciudad de
  México. Mexicable Línea 1's seven are in Ecatepec. Of Línea 2's seven,
  Indios Verdes is in Ciudad de México, La Mesa and Hank González in
  Ecatepec, and four (Tanque de Agua, Periférico, San Isidro, Dr. Jorge
  Jiménez Cantú) are outside the map, in Tlalnepantla per the operator's
  postcodes: listed as left out, the line drawn to its ends.
- **Stations that are already on the map under the same name:** Indios
  Verdes (both systems), Constitución de 1917 and Santa Marta meet Metro
  stations 150 to 345 m away, and the two Hank González stations are 30 m
  apart. Step 1 averages same-named nodes today, which would move three
  Metro stations; the build must attach them without moving any.
- **Colors, for the owner:** STE uses one light blue for all three Cablebús
  lines, and the only hex found is es.wikipedia's #4EC3E0 (23.5 from Metro
  Línea 4, 49.3 from the nearest pin). Mexicable calls its lines Línea Roja
  and Línea Verde and publishes no hex; Wikipedia's reds sit 6.2 to 16.1
  from the Food service pin and 12.3 to 19.9 from Metro Línea 1; its greens
  19.9 to 33.3 from Metro Línea 3.

### 2026-10-13 - Tram rescope: Barcelona's trams stay out, the page to say why (owner); Cablebus measured

- **Barcelona, the owner: "2 leave it out" and "and state why"**, to the
  measurement in the entry below: none of the 28 tram stops inside the city
  is beyond the 0.6 mile outer ring of a drawn station (farthest 807 m), and
  rings on them would bring no storefront inside the rings (22 of 35,309
  beyond, before and after). This supersedes "two drawn lines" of the same
  day, which the owner chose before the overlap was measured; the shade
  #00524a is not used. It is Hong Kong Tramways' reason, measured.
- **Owed, as wording for the owner:** a "not drawn" bullet on Barcelona's
  page (it has none for the trams), and the sentence in
  `docs/excluded_categories.md` that gives the trams' reason as "falls
  outside the network-identity test that picks out its metro", which is how
  they were filtered, not why they are out. Drafted in chat 2026-10-13;
  nothing in `app/` or that file is changed until approved.
- **Kept:** `data/barcelona/raw/osm_tram_routes_2026-10-13.json`, the
  evidence. No Barcelona step ran; no index rebuild is owed.
- **Cablebus has coordinates now.** The watch list said "no official list or
  coordinates yet". All 19 stations are in the place-search cache of
  2026-10-12 (`data/mexico_city/raw/osm_places_2026-10-12.json`,
  `aerialway=station`): Línea 1 six (Indios Verdes to Cuautepec), Línea 2
  seven (Constitución de 1917 to Santa Marta), Línea 3 six (Los Pinos /
  Constituyentes to Vasco de Quiroga), all inside Ciudad de México. Línea 3
  held one stop in OSM on 2026-09-27. The cable geometry is not in that
  cache; one Overpass query for it failed on both mirrors the same day
  (overpass-api.de URLError, kumi.systems 504) and was not retried.
- **Cablebus passes the test Barcelona failed.** Measured against the 180
  drawn stations in `data/mexico_city/processed/stations.csv` as it stood:
  15 of the 19 are beyond the 966 m outer ring (5 on each line), the
  farthest 6,542 m (Cuautepec); the four within it are the interchanges
  (Indios Verdes 290 m, Constitución de 1917 171 m, Santa Marta 150 m, Los
  Pinos / Constituyentes 154 m). Station spacing: medians 1,727 m, 1,613 m
  and 1,011 m. With rings on the 19, storefronts beyond 0.6 mi go from
  257,649 of 407,629 (63.2%) to 239,866 (58.8%): 17,783 storefronts gain a
  ring. Not re-run; `heavy_job.py` measured the read at 0.35 GB.
- **Raised for the owner, not decided:** Mexicable is out of the regional
  page by the owner's call of 2026-10-04, recorded as "a cable car". Its
  Línea 1 has seven stations in Ecatepec, 3.3 to 7.7 km from any drawn
  station, and Línea 2 two more there. Drawing Cablebus while Mexicable is
  out for being a cable car needs either the same call for both or a
  different stated reason.

### 2026-10-13 - Tram rescope: Rome's trams parked as one decision after 2026-11-23; Barcelona drawn as two lines (owner)

- **Rome, the owner: "yes one rome decision sounds good as a parked
  item"**, to the recommendation below it: one decision on trams 2, 3, 5, 14
  and 19 after ATAC's network is back (due 2026-11-23), none drawn before.
  Rome's rail is final as it stands until then, so the rescope no longer
  holds Rome out of the search rollout; a later tram build rebuilds its
  index.
- **Barcelona, the owner, on the color call: "option sounds best, note the
  page shade add"**, to option 1: two drawn lines, "Trambaix (T1, T2, T3)"
  and "Trambesòs (T4, T5, T6)", one in TRAM's green and one in a shade of
  this project's, the page saying the shade is the project's. Rejected: one
  key over two disconnected pieces of track (this map split L9 and L10 for
  that reason); three keys, which needs two project shades.
- **The shade, measured, not yet approved:** TRAM's #007165 moved in HSL
  lightness only, the smallest 0.02 step that clears Delta-E 13 from it
  (Rome's and Oslo's rule): #00524a at -0.06, 13.3 from TRAM's green, 18.6
  from the Montjuïc funicular, 45.5 from the nearest pin (Personal
  services). The lighter side clears 13 only at +0.08 (#009a89) and sits
  22.0 from that pin.
- **Measured the same day, and it changes the case for drawing them: no
  tram stop inside Barcelona is beyond the metro's reach.** Of the 28
  stops, 0 are farther than the 966 m outer ring from a drawn metro or
  funicular station (median 302 m, farthest 807 m; 6 beyond 0.3 mi, 9
  within 0.1 mi). Rome's tram 8 had 15 of 16 beyond it. With rings on all
  28, the storefronts beyond 0.6 mi stay at 22 of 35,309; 2,341 storefronts
  (6.6%) change ring, all inward (0-0.1 mi 7,257 to 8,192; 0.3-0.6 mi 3,215
  to 2,093). Read from `data/barcelona/processed/` as it stood, not
  re-run. Stop spacing inside the city: Trambaix median 417 m, T4 527 m,
  T5 and T6 about 510 m. The estimate's reason ("reach districts beyond the
  metro") holds for the networks' outer ends, which are outside the city
  and off this map. Brought to the owner before any build.

### 2026-10-13 - Tram rescope: Rome's tram 3 not built on its own; Barcelona TRAM measured (branch)

- **Rome's tram 3 was offered as a go-ahead "if it's an overall small
  addition" (owner, 2026-10-13) and is NOT built: the session judged it not
  small overall, and brought it back.** Mechanically it is small: one
  relation pair fetched under a new file name, one more key beside tram 8,
  the same half-mile thinning. What makes it larger: tram 3 runs only
  Trastevere - Porta Maggiore today, with buses on Porta Maggiore - Valle
  Giulia; and ATAC's trams 2, 5, 14 and 19 return in phases with the whole
  network due by 2026-11-23 (`docs/recheck_calendar.md`, whose row already
  names drawing them as the owner's call). Drawing 3 alone now means a
  partial line redrawn in six weeks, and a map that shows one returned tram
  and not the four that follow. Recommended instead: one Rome tram decision
  after 2026-11-23, for all five. Not measured: tram 3's stop count, color
  and distance from the metro; no Rome query was run.
- **Barcelona TRAM, measured from OpenStreetMap** (one Overpass query,
  2026-10-13, overpass.kumi.systems, bbox `41.30,2.03,41.50,2.30`, cached
  as `data/barcelona/raw/osm_tram_routes_2026-10-13.json`; the metro cache
  is untouched): 12 route relations, two per line, networks `Trambaix` (T1,
  T2, T3) and `Trambesòs` (T4, T5, T6), operator TRAM. Distinct stop names
  inside the municipal boundary: T1, T2 and T3 the SAME 9 (Francesc Macià to
  Zona Universitària and Ernest Lluch); T4 10 (Verdaguer to El Maresme and
  Fòrum); T5 and T6 the SAME 10 (Ciutadella | Vila Olímpica to Besòs);
  Glòries is on T4 and on T5/T6, so 28 distinct stops. The count of
  2026-09-27 (9 to 10 each) stands.
- **Color:** all six carry `colour=#007165`. Against the 16 drawn lines the
  nearest is the Montjuïc funicular (#006847), Delta-E 13.9, over
  `pipeline/linecolour.py`'s floor of 10. Two tram keys in that one green
  would be Delta-E 0 from each other, which the check refuses. Whether TRAM
  itself publishes per-line colors was not checked.
- **Nothing built, no step run, no output changed.** The color rule and how
  many lines are drawn go to the owner.

### 2026-10-13 - Tram rescope: the light batch and Paris were already built; two docs corrected (branch)

- **The session's handoff named Montreal's REM as the first build. It is
  built, with the other four: all five landed on 2026-09-27.** Commits
  c8c1c53a (REM, 78 stations), eedeb329 (Rome tram 8, 94), 5f9106e5
  (Madrid ML1, 200), 821ca1a9 (Paris T3a and T3b, 280), f3e051d7 (San
  Francisco F Market & Wharves, 57), merged in be2e3713. Measured
  2026-10-13 on origin/master 1b5f4df8: `git log --since=2026-09-26
  --until=2026-09-29`, and each committed `outputs/<city>/heatmap.html`
  carries its line's label.
- **What that changes for place search** (sent to Cleanup the same day, the
  owner having approved the message): no index rebuild is owed for trams in
  Montreal, Paris or San Francisco. Paris's search area counts 280 stations.
  Montreal's counts 79 across five municipalities against 78 rows in
  `stations.csv`; the difference is not traced (lead: a station counted in
  two overlapping municipal polygons).
- **Corrected on this branch, at Cleanup's request:** a status block at the
  top of `docs/tram_rescope_estimate.md` and `docs/tram_rescope_specs.md`,
  and the "Trams left off built maps" item of
  `docs/plan_detail/city_watch.md`. `DECISIONS.md` and `PLAN.md` are
  Cleanup's.
- **Downstream inputs changed by this branch so far:** none.
