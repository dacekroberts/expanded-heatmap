# Decisions drafts: tram-rescope

Newest first. Cleanup folds these into `DECISIONS.md` at review time.

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
