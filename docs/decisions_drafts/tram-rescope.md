# Decisions drafts: tram-rescope

Newest first. Cleanup folds these into `DECISIONS.md` at review time.

### 2026-10-13 - Landing slice: the station rules (search-rules-8) merged and the 20 indexes rebuilt; 58 reviews no row needs removed (Cleanup agent, nothing pushed, no render)

- **Merged:** 8d45eae5 (7de6f364) and then 0321cbb0 (b1a0f32f), no conflict;
  selftest 326 of 326. The 20 indexes were rebuilt after each. The second
  commit moved no row in any of the 20.
- **Only station rows moved, in seven cities, and the full rebuild gives the
  rules lane's measured counts exactly:** Barcelona +2 -8 and 5 renamed,
  Brussels -5, London -8 and 7 renamed, Marseille -1, Paris -3, Prague -42
  and 7 renamed, Tokyo one row under a new id. The other thirteen, Mexico
  City and Milan among them, are byte-for-row unchanged in every kind.
- **Prague is mended.** 42 tram stop rows fold (Palmovka 4, Želivského 4,
  Nádraží Holešovice 3). No station name has three rows any more; 26 names
  have two within 250 m, a metro row and a tram row each.
- **London as intended:** Blackfriars, Cannon Street, Liverpool Street,
  Marylebone and Victoria each fold their "London ..." rail row, the
  prefixed spelling kept as an alternate; Paddington's three rows are one;
  the two National Rail nodes of St Pancras International are one row,
  still apart from "King's Cross St Pancras"; "Stratford International" and
  its DLR row are untouched.
- **Barcelona:** six "Barcelona-..." rail halls fold onto the metro row of
  their entry (Arc de Triomf, El Clot, Fabra i Puig, Passeig de Gràcia, Sant
  Andreu, Torre Baró | Vallbona). **Doubtful, for the rules lane:**
  "Barcelona-Plaça Catalunya" (node 13671950492) and "Barcelona-Plaça
  Espanya" stay rows of their own beside "Catalunya" (which already carries
  the alias "Barcelona-Plaça de Catalunya") and "Espanya"; "Barcelona-La
  Sagrera-Meridiana" and "Barcelona-Estació de França" stay too, the last
  rightly (no metro row of its name).
- **Brussels, Paris, Marseille:** each departed row is a tram stop folded
  into the other tram stop of its name (the builder's log: merged_platform),
  leaving the metro row and one tram row. Tokyo's 熊野前 is one row under
  the tram stop's id.
- **Tokyo, Kyoto, Seoul, Busan: the local-name guard returned nothing.** No
  station row was added in any of the four, so there is no entrance, depot
  or freight yard to flag. If the guard was meant to bring rows back, it did
  not on these caches.
- **58 `PLACE_REVIEWED` entries removed** as listed in
  `data/_search_rollout/live_rules56/reviewed_not_needed.tsv` (Seoul 36,
  Paris 18, Busan 2, Brussels 1, Marseille 1), by a script that proves
  nothing else in each config changed. Check E passes for the five cities.
- **Same-name round, stations:** Milan, Seattle, Tbilisi and Vancouver have
  no repeated station name; Paris has 29 names with two rows within 250 m,
  Prague 26, London 17, Tokyo 15 (interchanges of two modes or networks,
  not read one by one here).
- **Milan, two more by id (relayed by Cleanup, 2026-10-13):** the other seven
  "Casa a Igloo" houses (ways 40500644, 59171470 to 59171473, 59171476,
  59171477; eight identically tagged houses, and each single drop had
  promoted the next to the row), under the first one's reason; and "Recinto
  di San Vittore al Corpo" (way 421310870), a part 36 m from the mausoleum's
  row. Each id matched its cached name first. No "Casa a Igloo" row remains;
  rows 6,097 to 6,095. Milan's map is stale again until the one render pass.
- **Checks:** `check_place_search.py` fails only on rule A (all 20 maps, not
  rendered on their final index). Scope OK for 20; unopened
  stations OK; index drift OK for 20.

### 2026-10-13 - Tram rescope becomes the first landing slice's branch; renders thinned to one a map (Cleanup agent, nothing pushed)

- **Owner (relayed by Cleanup, 2026-10-13):** `tram-rescope` carries the
  first landing slice (the 17 live searched cities, Mexico City, Prague,
  Milan, and Toronto's rescoped map); the search script is final at
  7c3cb2a4. Then "thin the re-render": each map is rendered once, when its
  index is final.
- **Merged:** search-integration c56c8fb5 (26eaad38), no conflict; selftest
  311 of 311; `check_place_index_drift.py` names all 20 indexes OK.
- **No render was started for the 17 live cities or Mexico City**: the
  change of plan arrived before the pool ran. Rendered so far, both on the
  final search script: Milan (8 s wall with the gate's start, peak 0.20 GB,
  6.4 MB, 45,999 points) and Prague (15 s, 0.52 GB, 3.3 MB, 21,462 points).
  Prague's index is due to change with the station rules, so its map will be
  rendered once more; Milan's is expected to stand.
- **On the two rendered maps:** `check_map_search.js` finds 193 of 193 and
  196 of 196 stations and 22 of 22 and 13 of 13 lines.
  `check_map_attribution.js` (its body, run in the browser pane from a
  temporary static server on 127.0.0.1, stopped and its launch entry
  removed): no problem at 1280x650 and 1280x812 on both, nor at 375x812 on
  Milan; the credit is clear at five of five points and the legend clamp is
  in force. Only two maps exist to test, not three.
- `check_render_current.py`: 18 maps stale (the 17 and Mexico City), as
  expected until their one render; Toronto is not among them.
- **Size against master:** Milan 5,312,979 to 6,445,039 bytes; Prague
  2,268,788 to 3,292,656. Both carry the tram rescope as well as the search
  block, so they do not measure the search block alone.

### 2026-10-13 - Place search script: a dotted abbreviation in a name is found by its word; Milan rendered again and Prague rendered as the second trial (Cleanup agent, nothing pushed)

- **Owner (relayed by Cleanup, 2026-10-13):** build the fix reported in the
  entry below; this lane owns `pipeline/map_common.py` for the change.
- **The change (7c3cb2a4, `pipeline/map_common.py` only).** In the search
  script's `prep()`, a name holding letters joined by dots ("V.le", "P.za",
  "P.ta") gains two tokens: the letters joined ("vle") and the word `ABBR`
  holds for them ("viale"). Where the joined letters are no abbreviation,
  the part before the first dot is tried alone ("S.LEONARDO" gains "san").
  Nothing is added unless the page's languages list it in `ABBR`. Italian
  `abbr` gains "pta": "porta".
- **Milan, re-rendered.** The 49 abbreviated station names typed in full:
  the map's own station is returned for 49 of 49 (4 before). The six that
  found no station before (P.TA GENOVA F.S., P.ta Lodovica, P.za 5 Giornate,
  P.za Ventiquattro Maggio, V.le Certosa Via Giorgini, V.le Certosa Via
  Tibullo) each return their own station. The dotted and undotted typed
  forms ("V.le Tunisia", "Vle Tunisia", "P.le Baracca") return the same
  station first as before. `check_map_search.js milan`: 193 of 193 stations,
  22 of 22 lines.
- **Prague, rendered once** (15 s wall with the gate's start, peak 0.52 GB,
  3.3 MB of HTML, 21,462 points, 196 stations). `check_map_search.js
  prague`: 196 of 196 stations, 13 of 13 lines. **The change is a no-op
  there by construction:** counted on the index and the map's stations,
  Prague's names hold 5 dotted groups ("hl.n", "F.V.Veselého") and the rule
  acts on none, since the Czech `abbr` table is empty. Its abbreviations end
  in a dot instead: "sv." 48 names, "nám." 15, "ul." 13.
- **Not covered, measured on Prague:** "nám." and "náměstí" find each other
  already (one is the start of the other). "Kaple svaté Anny" does not find
  "Kaple sv. Anny", and "ulice Bolzanova" does not find the stop whose alias
  holds "(ul. Bolzanova)": a trailing-dot abbreviation whose table has no
  word. Entries "sv" and "ul" in the Czech `abbr`, read from the name as
  well as from the typed word, would cover them; not built, since it is a
  second mechanism and a word list for the language's owner.
- **Not covered in Milan:** "Sant'Agostino" does not return the map's
  "S.AGOSTINO" ("s" gives "san", and "sant" is another word); the
  OpenStreetMap station row of that name stands in. "VILLA S.G." is found
  only as written. An OpenStreetMap station is still not LINKED to a map
  station whose name differs by an abbreviation, so both rows show.
- The search script has no self-test of its own; `check_map_search.js` is
  its check. `check_no_em_dashes.py` OK.

### 2026-10-13 - Tram rescope: Milan's map rendered once as the rollout's trial render, and its search tested in a browser (Cleanup agent, nothing pushed)

- **Owner (relayed by Cleanup, 2026-10-13):** renders on branches are
  approved, landing is not; Milan is the trial. `search-words-it` (acf21e2e,
  six more Italian street words in the search script) was merged first
  (2acffea2). Prague and Mexico City are NOT rendered: `map_common.py` may
  change once more.
- **The render.** `pipeline/milan/step3_map.py` through the gate: 8 s wall
  with the gate's own start, peak 0.20 GB, 6.4 MB of HTML, 45,999 points,
  193 stations. `check_place_search.py` names Milan OK.
- **`scripts/check_map_search.js milan`:** 193 of 193 drawn stations and 22
  of 22 lines found by the map's own search.
- **Dotted abbreviations fail one way.** 49 of the map's station names hold
  "V.le", "P.le", "P.za", "L.go", "C.so" or "P.ta". Typed as written, or
  without the dot ("Vle Tunisia"), the map's station is first. Typed with
  the word in full ("Viale Tunisia"), the map's own station is returned for
  4 of 49; for 39 more an OpenStreetMap station row of the full name stands
  in; **6 find no station at all** (P.TA GENOVA F.S., P.ta Lodovica, P.za 5
  Giornate, P.za Ventiquattro Maggio, V.le Certosa Via Giorgini, V.le
  Certosa Via Tibullo). Cause: `words()` splits "V.le" into "v" and "le",
  and `ABBR` is read from the typed word to the name, never from the name
  to the typed word. The fix is reported to the owner of `map_common.py`,
  not made here.
- **The six new street words work.** Typed in full, a street under each of
  galleria, piazzetta, passaggio, cavalcavia, alzaia and bastioni is the
  first result; without the lead word, "Giovanni Malagodi", "Naviglio
  Pavese", "Naviglio Grande", "Porta Volta" and "Porta Nuova" each return
  their passaggio, alzaia or bastioni street.
- **Not tested:** the box itself on a phone, an intersection search (the
  intersections file is not loaded by the harness; "Corso Buenos Aires e Via
  Vitruvio" returned nothing and that is not a finding), the outline.
- The queries went through the page's real `search()` from a scratch copy
  of the check with a fixed query list; the repository's script is
  unchanged.

### 2026-10-13 - Tram rescope: the final shared rules merged in; Mexico City, Prague and Milan rebuilt (Cleanup agent, nothing pushed)

- **Merge.** search-integration 73f025df into `tram-rescope` (2c72a02d), no
  conflict; `KNOWN_GAPS` stays empty; selftest 311 of 311.
- **Rows.** Mexico City 67,338 to 67,336; Prague 10,435 to 10,431; Milan
  6,119 to 6,097. The full account, with names, is
  `data/_search_rollout/tram_rules56/final_rebuild.md`.
- **Milan's 527-id platform tuple is removed.** Built in memory with the ids
  and without, the index is the same 6,099 rows: the shared rule takes every
  one, so none is kept by id. The rule takes 17 more stop names the list did
  not hold.
- **Owner, 2026-10-13, three Milan items:** the second "Ultima Cena" (node
  3446474994) and "Chiesa parrocchiale di Santa Maria Assunta in Quintosole"
  (way 360192664) dropped by id; both "Cascina Melghera" rows kept.
- **Prague's 18 boroughs are rows again.** 24 street names leave, each a
  stop platform by its tags.
- **A fault for the rule's owner, not mended here:** in Prague 31 station
  names have two to six rows within 250 m (Palmovka 6, Želivského 6), and
  this build added 12. The same-name merge tests the whole 250 m cluster
  with `_one_railway`; a cluster holding a metro station and tram stops is
  mixed, so the tram stops no longer fold with each other.
- **Judgment call: "twin round" was read as a same-name round**, every pair
  of non-street rows of one kind and one name with its distance. Milan is
  clean within 1 km.
- **Checks.** E and H pass for the three; scope, index drift and unopened
  checks OK. Rule A fails for all 20 searched maps: the merged matcher
  changes the script every map carries.

### 2026-10-13 - Tram rescope: master merged in; place search rebuilt for Mexico City and Prague and built for Milan (Cleanup agent, nothing pushed, no map rendered)

- **Merge.** `origin/master` (e0138000) into `tram-rescope`, 788ae80c. No
  conflict: both configs merged by git, each side's settings kept.
  `app/ring_shares.json` regenerated. The four cities then showed zero drift
  with the index step left out (the scratch wrapper of the entry below).
  `check_macro_facts.py` passes; Mexico City (Regional) reads 427,121.
- **Mexico City (adb4c5c1).** `PLACE_AREA` gains Tlalnepantla de Baz
  (relation 5606521; 4 drawn stations). The six-area caches read earlier the
  same day from the held extract (mexico-261012, data 2026-10-12T20:21:35Z)
  were adopted by copy under new names, `osm_places_2026-10-13.json` and
  `osm_places_extra_2026-10-13.json`, and recorded in provenance by the
  extract route's own recorder; the script's kept-cache area check passes.
  The five-area outline is kept as
  `osm_place_outline_v1_five_areas_2026-10-12.json`. No refetch.
  - **Judgment call: the Wikidata cache was copied to
    `wikidata_articles_2026-10-13.json` before the lookup**, since the cache
    name follows the place cache's and a fresh name would have asked every
    id again. One request, one new id.
  - Rows 61,199 to 67,345 (streets 55,682 to 61,711, places 2,986 to 3,023,
    landmarks 2,290 to 2,391, stations 240 to 219, junction 1). The index
    was last built before the rule passes of 2026-10-13, so the change
    mixes the area and the rules.
  - Check H passes on its own; `KNOWN_GAPS` is empty again. San Isidro is a
    Mexicable terminal, so it is no station row by rule; it is covered by
    the places around it and found from the map's own station list.
  - 223 non-street rows are new to the cache (182 landmarks, 39 places, 2
    stations). Seven dropped by id under the bare-type and description
    rulings of 2026-10-11 (Glorieta, Explanada, obelisco, CANCHAS
    DEPORTIVAS with two spaces, Parque Para Perros, Parque con fuente, Area
    Comun/Canchas de Basquetball). Two street names reviewed for the leak
    word "s.a." (Avenida A.N.D.S.A. and its alternate Calle 2 de Abril).
  - **For the owner, 14 rows** in `data/_search_rollout/tram_rules56/mexico_city.tsv`
    (verdict unsure), each with a recommendation.
- **Prague (ef1e64eb).** Rebuilt from the caches of 2026-10-08 on the 196
  stations; no request. Rows 10,790 to 10,435. Check H passes: no tram stop
  is without an indexed place within 1 km, and no quiet station is listed.
  Station rows are OpenStreetMap's (431 to 429, two merges), not the map's
  196: the map's stations reach the box from the map itself.
  - Every departure is a landed rule of 2026-10-13: 292 works of public art
    with no article, 36 boundary relations repeating another row's entry,
    11 libraries, 5 street ways as landmarks, 4 halls named by denomination,
    4 segment merges, 3 private living streets, the city's own boundary.
  - **For the owner: 18 boroughs now have no row under their own name**
    (Praha 1, 3, 4, 7, 9, 10, 14, 16, 18, 20, 22 and seven "Praha-X"). The
    row that keeps each one's Wikidata entry is its TOWN HALL, a landmark,
    not a place node. Recommendation: the site-relation rule should fold a
    boundary only into a place row; a rule change, so the protocol's.
- **Milan (e1ed8d65).** No built Italian city gave an admin level, so the
  area lookup left it for a person. **Judgment call, by the scope rule: the
  Comune di Milano, relation 44915 (admin_level 8)**, the boundary the
  businesses are cut to; all 193 stations sit in it. One extract download
  (nord-ovest-261013, 593 MB), no Overpass request, two Wikidata requests
  for 64 ids.
  - 6,149 rows: 4,378 streets, 996 landmarks, 482 stations, 293 places;
    8,798 intersections. Italian 100%. Check H passes.
  - **Judgment call: 527 ways dropped by id as stop platforms.** Milan draws
    stop platforms as `highway=footway` with `public_transport=platform`,
    named for the stop ("V.le Sarca Via Chiese"), and the street pass read
    372 such names as streets. A platform is no street by the first row of
    the exclusions record; the rule reads `highway=platform` only. Prague
    has 20 such names, Mexico City none; other cities were not measured.
    Recommendation: a rule on the platform tag, which would replace the
    list.
  - Also by id: three descriptions, ten places of worship named only by
    their body or denomination (the Italian list does not hold them), one
    locality named as a person's house. "Albergo diurno Venezia" reviewed
    as a place.
  - Street coverage 84.0% of named-way names after the platform drop
    (91.1% before); the names left out are footways (514, the platforms
    among them), platforms (134), service roads (92).
  - The eye read: the `place-read` agent read all 1,006 landmark and 295
    place rows line by line; the caller read the 482 station rows; streets
    were screened by pattern, not read. 102 rows are with the owner in
    `data/_search_rollout/tram_rules56/milan.tsv`: 33 "Casa X" historic
    buildings (no Italian house lead in the lists), 26 farmsteads and mills
    tagged places, 4 tram stops closed in 1978, 14 second rows, others.
  - **Owed before Milan's map is rendered:** `map_common.LANG_WORDS` has no
    Italian entry on this branch (the matcher words are on another branch).
  - The scaffold set `search='milan'` on the page; the bullet is the
    template's. No other page text is needed (flag for review time).
- **Owner, 2026-10-13 ("all approved"), relayed by Cleanup and applied by
  id, each id checked against its cached name:**
  - Milan's search area is approved (relation 44915). The 527 platform ways
    stay by id until the shared rule on the platform tag replaces them. The
    street names flagged by pattern are left alone.
  - Mexico City, 7 dropped: the park "Alcoholicos Anonimos", Center Park
    and FUNO Center, "IJSUD", the street altar, the second cathedral node,
    the locality "Jardines del Recuerdo". The other seven stay. Rows 67,345
    to 67,338.
  - Milan, 31 ids dropped: six "Casa X" buildings with no article of their
    own (Castini, Cicchieri, Pirovano, Rovida, del Cedro, and Casa a Igloo,
    whose article is the Maggiolina quarter's); the four tram stops closed
    in 1978; East Garden, La Viridiana, Giunglabuca, EuroMilano; Milano 2
    and Pero; Armenia Films, Hayabusa Reiki Dojo, Lanciatore Vega,
    PalaSharp, Tranvia Milano-Lodi, Precotto (Interno deposito); the grotto
    under a church's name; and eight true duplicates (Cassina Triulza,
    Ronchetto Sul Naviglio, the census area Parco Sempione, Stadio San Siro
    Milano, Giardino Gonin Giordani, Giardino Mario Capponi, Parco di via
    Dezza, the node Circo Romano). Rows 6,149 to 6,119: 30 rows for 31 ids,
    one id's row having been its twin's.
  - Kept: the 27 "Casa X" with an article, the 26 farmsteads and mills, the
    census-area names (Ticinese, Adriano, Comasina among them), "Ultima
    Cena" (node 304775593).
  - **Judgment call, two pairs left as they are:** "Cascina Melghera" (two
    nodes 2.6 km apart, which one is misplaced is not known from the tags)
    and the two Quintosole church rows 20 m apart under different names.
    Neither is a duplicate the tags settle.
  - Check H, check E, the scope check and the index drift check pass for
    both cities. The verdict lists in `data/_search_rollout/tram_rules56/`
    are the read as it stood before these rulings.
- **Checks.** `check_all.py`: one failure, `check_place_search.py` rule A for
  the three maps not rendered since their index step. Scope check OK (20
  cities), index drift OK, provenance names the three OK.

### 2026-10-13 - Tram rescope: landing preparation, the four cities back on their normal processed paths (Cleanup, nothing pushed)

- **Owner, 2026-10-13:** approved starting the landing preparation. Done on
  the branch by a Cleanup agent; nothing pushed, master not merged in.
- **Flipped:** Toronto's `STATIONS_CSV` and `STREETCAR_SHAPES_JSON`, Milan's
  and Prague's `TRAM_DIR`, and the `cable` part of Mexico City's
  `DATA_PROCESSED`. Each city's steps were then re-run and write the shared
  `data/<city>/processed/` (Mexico City: `processed/regional/`).
- **Re-run, against the approved figures (all match):**
  - Toronto, steps 1 to 4: 174 stations (108 + 66), 11,803 of 18,215
    storefronts in a ring.
  - Milan, steps 1 to 3: 193 stations (104 + 89), 22 lines, 45,999 of 47,540.
  - Prague, steps 1 to 3: 196 stations (57 + 139), 21,462 of 25,185.
  - Mexico City, steps 1 to 3: 208 stations, 427,123 storefronts written,
    427,121 on the map, 175,939 in a ring.
- **Drift:** zero in all four; every `outputs/<city>/` file is identical to
  the committed one (the maps after Folium-id normalization). Each new
  station and shape file is byte-identical to the branch-only copy it
  replaces.
- **Baselines updated:** Toronto five new figures, Milan six, Prague six and
  `stations_excluded` 1 to 109 (the 108 thinned tram stops), Mexico City
  twelve figures moved to the five-municipio counts.
- **Judgment call: Prague's and Mexico City's drift check ran without
  `step2b_place_index.py`.** The search rebuild waits for a rule landing, and
  the full check would have rebuilt both indexes on the new stations. The
  other steps ran through `drift_check.py`'s own functions (offline guard,
  output and baseline comparison) from a scratch wrapper. Neither index was
  touched.
- **Judgment call: Prague's feed was not refetched.** The entry of the same
  day already recorded the re-pull in `provenance.json` from the cached
  file; its bytes and SHA-256 were re-measured and match. A refetch would
  have had to change `TRAM_GTFS_ZIP` and could have moved the approved
  station set for no gain.
- **Left in place:** `data/<city>/processed/tram/` (three cities) and
  `data/mexico_city/processed/regional/cable/`, now unused copies. The
  dry-run blocks at the foot of `streetcars.py` and both `trams.py` read
  `stations.csv` as the metro-only set and are stale since the flip; each
  carries a comment saying so.
- **Checks:** line identity 0 problems; provenance names all four OK;
  `check_all.py` 72 of 73, the one failure Mexico City's check H (San
  Isidro, the stale search index, as before).
- **Until the branch lands, master's code reads the new station files**
  from the shared folder: a master drift check or index step for these four
  cities sees 174, 193, 196 and 208 stations.

### 2026-10-13 - Tram rescope: the owner signs off Prague's page text and label form, and Toronto's and Mexico City's page text

- **Owner, 2026-10-13:** "i sign off on all the waiting on you items
  (unless my version of label comma is grammatically incorrect)". The
  items put to the owner were: Prague's page text (The lines bullets, the
  "more than eight storefronts in ten" sentence, the Overview blurb), the
  label comma, and the page text of Toronto and Mexico City.
- **The label comma stays as built**, "Trams 2, 18, & 24". A comma before
  an ampersand is not a grammatical error; it is a style choice (the
  Chicago Manual drops it, "2, 18 & 24"). Reported to the owner as that,
  with the one-line change in `config.tram_group_name` if they prefer the
  other.
- With Milan approved earlier the same day, all four rescoped cities'
  page text is approved. Landing is Cleanup's, at review time.

### 2026-10-13 - Tram rescope: Prague's trams are drawn in ten groups (owner), built on the branch; the page text is a draft

- **Owner, 2026-10-13:** "1 yes" to the ten groups of the entry below, and
  the label form: "label should be Trams 1 & 25 unless that is confusing.
  commas before final number for groups larger than 2".
- **Label form as built (this session's reading of that sentence):** two
  routes "Trams 1 & 25"; three or more with a comma before the ampersand,
  "Trams 2, 18, & 24". If the owner meant "Trams 2, 18 & 24" it is one line
  in `config.tram_group_name`.
- **Built.** `config.TRAM_GROUPS` holds the groups and their colors (the
  trial's, pin floor 45, closest pair within 500 m 41.9). 13 lines, 196
  stations, 21,462 of 25,185 storefronts in a ring (85.2%; 69.6% before).
  Station rows and excluded reasons still name the single route ("Tram 5"),
  which is the public name of the service.
- **Labels (`scripts/check_map_labels.js` on the built map):** no problem
  at 1024, 375 or 343.
- **The four wide stop names** (Vinice, Palmovka, Nádraží Holešovice,
  Želivského) were read from the feed's platform coordinates: each is one
  junction with platforms on its different arms. Kept as one place each.
- **Provenance.** `provenance.json` now records the re-pull (`gtfs_trams`,
  bytes and SHA-256 computed from the file, retrieved time from its
  modification time) and `fetch_sources.py` fetches `TRAM_GTFS_ZIP` beside
  the metro's copy. The fetch script was not run.
- **Drafts for the owner (not approved):** The lines bullets and the ring
  share sentence on `app/pages/28_Prague_Heatmap.py`, the blurb in
  `app/cities.py`, the Stations paragraph in `docs/excluded_categories.md`.
- **For landing:** set `TRAM_DIR = DATA_PROCESSED`, re-run steps 1 and 3,
  update `baseline.json`; the place-search index needs a rebuild (139 new
  stations). No drift check was run from the branch. check_all 72 of 73
  (Mexico City's search area, known).
- **Re-check:** `docs/recheck_calendar.md`, 10-26, when the feed window
  ends; why 30, 31, 32, 37 and 40 run and 14 and 16 do not was never read.

### 2026-10-13 - Tram rescope: Prague built with 28 tram routes (owner); per-route labels fail on phones, and a ten-group trial passes (the grouping is with the owner)

- **Owner, 2026-10-13:** all 28 day routes ("yes your recommendations"),
  tram 37 drawn ("draw"), and corridor grouping if label overlaps remain
  ("corridor grouping").
- **Built on the branch, per route.** `pipeline/prague/trams.py` (the
  Toronto and Milan rules; a place is a stop name, since PID's node 1040
  holds both Anděl and Na Knížecí), steps 1 and 3, config. Steps write and
  read `data/prague/processed/tram/`. The trams read the re-pull
  `pid_gtfs_2026-10-13.zip` (`TRAM_GTFS_ZIP`, window asserted); the metro
  still reads the cache of 2026-09-24. `provenance.json` does not record
  the re-pull yet: owed at landing, with a refetch.
- **Measured:** 281 tram places, none outside the city; 34 are a drawn
  metro station; 108 thinned to one per half mile; 139 new stations. 57
  metro + 139 tram = 196 stations, nearest-neighbor median 477 m, closest
  pair 153 m. 21,462 of 25,185 storefronts in a ring (17,528 before).
  Midday headways 4.5 to 10.0 minutes; tram 23 at 30.0, not drawn.
  Four stop names have platforms more than 200 m apart and are kept as one
  place each (`TRAM_WIDE_PLACES`), on the names alone, not a map read.
  Flora's tram stop is a tram station while the metro station stays listed
  as closed for works.
- **Per-route labels (`scripts/check_map_labels.js`, 31 labels):** no
  problem at 1024; five overlaps at 375; sixteen at 343. At 343 the phone
  fit shows the whole network at zoom 10.25 in about 175 by 170 px, less
  room than 31 labels need, so moving label ends cannot clear it (not
  tried, on that measurement).
- **Grouping trial (session scratchpad, nothing in the repo).** Routes
  merged by average shared track (track within 40 m, over the shorter
  route). Ten groups: 1+25; 2+18+24; 3+17+20+40; 4+22; 5+12+15+21+32;
  6+7+19; 8+26; 9+10; 11+13; 30+31+37. Labels "Trams 1, 25" and so on, one
  color per group at pin floor 45 (closest pair within 500 m 41.9). 13
  labels: no problem at 1024, 375 or 343. Eight groups leave one label
  under the legend at 1024; twelve leave one there and one overlap at 343.
- **The limit:** these are the project's groups, not PID's. Two routes in
  a group share as little as 26% of their track (2 and 24), so a group's
  color follows several streets, not one corridor.
- **Not decided:** grouped or per route with overlaps. The owner's.

### 2026-10-13 - Tram rescope: Prague's 23 regular routes alone leave six stops with no drawn tram; the recommendation moves to all 28 day routes (open, nothing built)

- **Measured** on the feed of 2026-10-13, weekday 2026-10-14, by stop name:
  276 of 284 tram stop names have one of the 23 regular day routes.
  - Strážní, Chmelnice, Kněžská luka and Spojovací (the Spojovací branch)
    have only 30, 31 and 37.
  - Třebenická has only 30. Smíchovské nádraží has only 32 and 40.
  - Královka and Hládkov have only 23, every 30 minutes, which fails the
    15-minute test whichever set is drawn.
- **Route ends in the feed:** 30 Sídliště Ďáblice to Spojovací, 31 to
  Spojovací, 37 Lehovec to Spojovací, 32 to Slivenec, 40 to Sídliště
  Modřany. Why the regular routes are off those stops was not read.
- **What it changes.** The earlier recommendation (23 routes) would leave
  running track undrawn. Milan and Zurich draw the timetable as it runs, so
  the recommendation to the owner is now all 28 day routes at 15 minutes or
  better; 23 routes plus 30 and 32 (25 lines) is the smallest set that
  covers the six stops. 37 adds no stop that 30 and 31 lack.
- **Not decided:** the set, and what to do if label overlaps remain on
  phones after label-end overrides. Both are the owner's.

### 2026-10-13 - Tram rescope: Prague's tram routes and label placement measured; the line list is with the owner (open, nothing built)

- **The feed.** `https://data.pid.cz/PID_GTFS.zip` re-pulled 2026-10-13 as
  `data/prague/raw/pid_gtfs_2026-10-13.zip` (feed_info 2026-10-13 to
  2026-10-26). The cache of 2026-09-24 is untouched.
- **39 tram routes** (route_type 0). Read on Wednesday 2026-10-14, 10:00 to
  15:00, the busier direction:
  - 23 numbered day routes at 4.8 to 10.0 minutes: 1 to 13, 15, 17 to 22,
    24, 25, 26. There is no 14 and no 16 in this feed.
  - Four more day routes at 4.5 to 10.0 minutes: 30, 31, 32 and 40. Why
    they run was not read; the numbers are outside the regular 1 to 26.
  - 37 at 9.7 minutes, the only tram the feed flags
    `is_substitute_transport`.
  - 23 at 30.0 minutes, 07:27 to 18:51: fails the 15-minute test.
  - Ten night routes, 90 to 99 (`is_night`): not drawn, on the per-route
    rule.
- **Colors (measured, the method of the Milan entry):** 28 trams beside
  the three metro colors fit at a pin floor of 45, closest pair within
  500 m 27.1 (trams 6 and 9); the 23 regular routes alone fit at 29.2
  (trams 2 and 8). A tram has 18.6 other lines within 500 m on average.
- **Label placement (measured, a trial render to the session scratchpad,
  each route on its most-used shape, the metro-only station set,
  `scripts/check_map_labels.js`):**
  - 28 trams, 31 lines: no problem at 1024; three label overlaps at 375
    (13/15, 18/21, 22/26); five at 343 (Metro A/9, 1/25, 4/5, 6/18, 12/13).
  - 23 trams, 26 lines: no problem at 1024 or 375; two overlaps at 343
    (8/12, 11/13).
  - No per-line label end was set; whether overrides clear the overlaps is
    not measured.
- **Nothing built, no step run, no output changed.** Prague has a place
  search index, so a new station set owes Cleanup a rebuild.

### 2026-10-13 - Tram rescope: Milan approved as built (owner)

- **Owner, 2026-10-13, after the four items put for approval (the stop-name
  form, The lines bullets, the What Is Excluded sentences, the 17 colors):
  "milan looks great".** Read by the session as approving all four as
  built in 1dadd89c; no item was singled out. Nothing changed after it.

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
