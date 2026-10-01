# DECISIONS drafts - Czech kit (`worktree-czech-kit`, then `czech-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-09-30 - Ostrava's in-city line 5 stops disclosed in prose, not listed, following Kyoto and Madrid (owner); the boardable default flipped on master (owner)

- **Owner: "B, follow the precedent."** This supersedes the recommendation
  in the entry below. A new station-scope category, "left out with a stub
  line", would have served two stops in 81 cities, and the precedent runs
  the other way: Kyoto's Sagano Scenic Railway and Madrid's Metro Ligero ML2
  and ML3 were left out as stubs, and their stops were never listed in an
  excluded-stations file, only disclosed in prose.
  - **What changed:** `czechia_osm_tram._not_drawn_stops` now lists a
    not-drawn line's stops only when they lie beyond the map's obce, as
    outside. Ostrava's file has gone from 9 rows to 7.
  - **Disclosed in prose:** Poruba,koupaliště and Krásné Pole, in Ostrava's
    section of `docs/excluded_categories.md`. The page says line 5 is not
    drawn, with 3 of its 10 stops in the city.
  - **No app change.** `check_scope_disclosure.py` passes for all 81 cities.
    Ostrava's baseline is rewritten (`stations_excluded` 9 to 7, intended).
- **The boardable default was flipped by the cleanup session** (owner,
  2026-09-30, approved in both sessions): `boardable_stop_ids` defaults to
  ("0", "2", "3") on master since `d928f50`, with cleanup's proof that no
  built map moved (theme 13 of `docs/map_inconsistencies.md`).
  - **On `czech-build`:** master was merged and `pipeline/stations.py`
    resolved to master's version, byte-identical.
  - **Brno:** its explicit argument now restates the default and stays, to
    say why Brno depends on it. Brno re-ran with zero drift.

### 2026-09-30 - Master's new rules merged into czech-build; Ostrava's two in-city line 5 stops need a station-scope category (owner call open)

- **`origin/master` merged into `czech-build`.** It brought the heavy-job gate
  (`scripts/heavy_job.py`), the drafts rule and a stricter
  `check_scope_disclosure.py`, which now refuses an excluded station whose
  reason `app/station_scope.py` reads as "Other".
- **Ostrava's nine line 5 rows were split by place.** The seven beyond the
  city now say "outside obec 554821 (Ostrava), on a line not drawn: …", and
  station_scope counts them as outside. The two inside the city,
  Poruba,koupaliště and Krásné Pole, still carry line 5's reason, because no
  existing category is true of them. **The check fails for those two on
  `czech-build`.**
- **An owner call, recommended: a new category, "left out with a stub
  line".** It would mean teaching `app/station_scope.py` the category, adding
  a column to the excluded-stations page (`201_What_Is_Excluded.py`) and a
  sentence there, and describing the category in
  `docs/excluded_categories.md`. The other shapes are worse:
  - calling them "outside" is false;
  - dropping them from the CSV loses the station table's record of them
    (the page text and the exclusions doc name them either way).
  The category is shared app code and new page text, so it goes to the
  owner, not this session.
- **Regenerated on the branch:** `app/ring_shares.json` (the six Czech
  cities added, no other row moved) and README's city list.
- **Left for the lander, all landing-time work:**
  - `check_macro_facts.py --write`, which reads every city's shared processed
    files;
  - the `map_inconsistencies.md` rows (cleanup's city-landed sweep);
  - the measured macro-label widths (a real browser in the app);
  - notice numbering, where 69-71 are France's and must land with 72 and 73;
  - the master-list counts.

### 2026-09-30 - Plzeň built: 53 stations; the "two missing stops" were a one-day diversion (supersedes the entry below on Plzeň's gate 3)

- **Plzeň's two "missing" stops were not stops.** The entry below reported
  that gate 3 against PMDP's feed found Jízdecká and U Synagogy missing
  from OSM's relations, to be added. That was a counting error. Both are
  served only by service 44, which has no weekday flags and runs on
  2026-10-10 alone (`calendar_dates`): a one-day diversion. No trip calls at
  both U Synagogy and Sady Pětatřicátníků, 58 m apart; a trip uses one or
  the other. The 10% trip share had been counted over the whole six-month
  feed, with no weighting for the days a trip runs.
- **Gate 3 by service day.** These are the stop names each line serves on
  Wednesday 2026-10-07, at the 10% rule.
  - Line 2 has 23, and OSM 23.
  - Line 1 has 20, OSM 19; the extra is the Vozovna Slovany depot stop.
  - Line 4 has 29, OSM 19. Every extra is a station already in the set,
    reached by a depot-bound variant over line 1's track, except the depot.
  - **So the station SET matches PMDP's but for the depot**, which is left
    out as Brno's Vozovna Medlánky is. The same pattern held on 2026-10-14
    and 11-11.
  - The counts sit in the config with that reason; gate 3 prints the two
    per-line mismatches, as Prague's did.
- **Not added:** the `STATION_ADD` entries were removed before any map was
  rendered with them. The tram kit's tuple-of-refs extension (97ba25a, taken
  whole onto `czech-build`) stays, harmless and useful. The shared tram query
  (`czechia_fetch.osm_trams`) now also fetches every tagged tram stop in the
  box, which a future add needs; steps read relation members only, so no
  station moves.
- **Built:** 53 stations, all inside, at a 306 m median gap. 2,508 of 3,508
  storefronts (71%) sit in a ring, and the restaurant ratio is 2.0 (1.99, so
  no OpenStreetMap-gaps sentence).
  - **Checks:** `check_map_view.js` at 1280 and 375 px, and the attribution
    check at 1000x650 and 1280x900, all pass with no corrections.
  - **Privacy verdict:** publish. No contact details, no person-like name at
    a residential unit, and 6.2% heuristic flags, all company names.
- **PMDP is credited as notice 73**, on the stricter CC BY reading, since its
  counts were used.
  - **The credit** is the brief's (owner-approved).
  - **The framing around it is this session's and is flagged for review:**
    "Plzeň's tram stops are checked against …: only its stop counts per line
    are used, and nothing from it is drawn. Not produced or endorsed by PMDP
    or the City of Plzeň."
- **The lesson is in the skill**: count a feed by service day, never over the
  whole file.

### 2026-09-30 - Olomouc, Ostrava, Liberec (Regional) and Most (Regional) built on osm_tram.py; Plzeň's gate 3 finds two stops OSM's relations lack

- **The four built on the tram kit's `pipeline/osm_tram.py`**, taken
  unchanged from `tram-build` so both branches carry one file; its Aarhus
  control passes on `czech-build`. A shared Czech wrapper,
  `pipeline/countries/czechia_osm_tram.py`, runs step 1 and step 3, and each
  city's step files are a few lines. Step 1 writes the kept relations'
  geometry (each ref's relation with the most track, platform outlines left
  out, Aarhus's rule) to `lines.geojson`. Step 3 draws that file, and
  `line_colour_search.py` reads it, so what is drawn is exactly what was
  kept.

  | City | Stations | Lines | Median gap | In a ring |
  |---|---|---|---|---|
  | Olomouc | 36 | 7 | 316 m | 1,742 / 2,235 (78%) |
  | Ostrava | 92 | 14 | 431 m | 2,941 / 3,960 (74%) |
  | Liberec (Regional) | 39 (Liberec 33, Jablonec 6) | 4 | 355 m | 1,396 / 2,488 (56%) |
  | Most (Regional) | 27 (Most 15, Litvínov 12) | 4 | 522 m | 664 / 1,025 (65%) |

  Every median is under 550 m, so all keep the halved rings. Most's is 28 m
  under the line.
- **Ostrava's three judgments:**
  - **NOT_DRAWN.** It names line 5's two relations (owner), lines 9 and 19
    (no stop members) and an unref'd line 11 depot variant. Line 5's stops
    are listed in `excluded_stations.csv` with the reason (9 rows).
  - **A 330 m collapse instead of 200.** Two names are interchanges whose
    stops sit on different arms of a junction: Sport Aréna at 321 m (lines
    2/7 on one arm, 11/12 on the other) and Mariánské náměstí at 223 m.
    That is within Riga's 300 m and Osaka's 400 m; the next widest name is
    173 m.
  - **Two stand pairs folded by name alias.** The station gate's close-pair
    note found them: Hranečník (St. 1) into (St. 5), 120 m apart, and Nová
    Huť hlavní brána 1 into 2, 61 m apart. One station under two names
    would have taken two sets of rings. Each folds into the spelling more
    lines carry, because `osm_tram` never invents a bare name.
  - **Result:** 94 stations became 92, and the closest pair is now 168 m.
- **The palettes are the project's own** (owner), from
  `line_colour_search.py` with target hues spaced evenly round the wheel in
  line order, HSL (h, 70%, 45%). Every line is 3:1 on both map pages and 45
  or more from every pin. The closest pairs: Olomouc 19.4; Ostrava 18.3
  within 500 m and 15.8 anywhere (lines 10 and 11, never near each other);
  Liberec and Most 88.3; Plzeň 124.7. `check_map_markup.py` passes on all 80
  maps.
- **Checks on the four maps:** `check_map_view.js` passes at 1280 and 375
  px, with no corrections, and the attribution check passes at 1000x650 and
  1280x900. **Privacy verdicts, from `check_personal_exposure.py`: publish,
  for all four.** No contact details, and no person-like name at a
  residential unit. The heuristic flags 7.7 to 9.4%, all of them company
  names, as in Prague and Brno.
- **Pages written from the approved template**, with no departure from it.
  Ostrava, Liberec and Most carry the OpenStreetMap-gaps sentence (ratios
  2.3, 2.5 and 3.3). "{City} has no metro" names the core town on the two
  regional pages ("Liberec", "Most").
- **Gate 3 runs only in Plzeň, and there it found a gap.** PMDP's feed (the
  approved cross-check) serves Jízdecká and U Synagogy on lines 1, 2 and 4.
  OSM tags both as tram stops (nodes 10314072849 and 10315344302) but puts
  them on no route relation. The feed also runs line 4 via Hlavní pošta and
  Náměstí Republiky, while OSM does not; the abbreviation "Nám. Generála
  Píky" is a spelling difference only.
  - **What OSM gives:** 53 stations from the route relations, the brief's
    figure exactly, and a set the feed shows to be two short.
  - **The fix:** `osm_tram`'s `STATION_ADD`. It takes one line per node, so
    a backward-compatible change (a tuple of refs) was put to the tram kit,
    who own the module. Plzeň's page waits for it.
  - **Two untagged directions:** two line 4 relations carry no operator tag
    in OSM, and are named in `NOT_DRAWN`; their reverse directions are kept.
    No stop is lost, and the excluded list is empty.
- **Gate 3 is not run for Olomouc, Ostrava, Liberec or Most**, and is
  recorded as an open gap in each config. Olomouc's DPMO feed is excluded by
  the owner's call. Ostrava's and Liberec's feeds were unreachable at the
  screen, and Most has none. Plzeň shows what OSM's relations can miss.
  Reading each operator's published stop lists would close the gap; that
  belongs at review time.

### 2026-09-30 - Brno rendered and checked: 146 stations, 11 lines, 82.4% of storefronts in a ring; privacy verdict publish

- **Brno's map is rendered on `czech-build`.**
  - **What it shows:** 146 stations and 11 lines drawn from OSM by `ref` in
    the feed's colours, with 7,200 storefronts. 5,932 of them (82.4%) sit
    inside the 0.05 / 0.1 / 0.2 / 0.3 mi rings; the brief's OSM stand-in
    read about 83%.
  - **Checks:** `check_map_markup.py` and `check_inline_arrays.py` pass on
    all 76 maps. `check_map_view.js` passes at 1280 px (zoom 12 against 12)
    and at 375 px (11.25 against 11.25), with no corrections. The OSM
    credit is clear and the legend clamp in force at 1000x650 and
    1280x900.
  - **How it was served:** the preview read the launch folder's own
    `.claude/launch.json`, so a temporary `czech-static-tmp` entry was
    written there. The main checkout's file was not touched; a hook refused
    the edit.
- **Privacy verdict for Brno, from `check_personal_exposure.py brno`:
  publish.** The figures: 0 e-mails, 0 phone numbers, 0 c/o markers, and 1
  person-like name at a residential unit (0.02%). The heuristic flags 602
  names (10.1%), and every one is a company's registered name, because
  natural persons and partnerships show their address. That is Prague's
  verdict (1,991 flagged, 1 at a residential unit) on the same structural
  guarantee. The six cities were added to the check's table in Prague's
  shape, and the other five get their verdicts once their maps exist.
- **The restaurant control, measured for all six as Prague's was.**
  CZ-NACE 2025 5611 storefronts against OSM's restaurant, fast_food, cafe,
  food_court and ice_cream features, node and way, inside each city's own
  polygon (2026-09-30):

  | City | Register | OSM | Ratio |
  |---|---|---|---|
  | Brno | 2,110 | 1,315 | 1.60 |
  | Plzeň | 852 | 429 | 1.99 |
  | Olomouc | 616 | 342 | 1.80 |
  | Ostrava | 1,092 | 482 | 2.27 |
  | Liberec (Regional) | 587 | 237 | 2.48 |
  | Most (Regional) | 267 | 80 | 3.34 |

  Ostrava, Liberec and Most are over 2, so their pages carry the approved
  sentence on OpenStreetMap's gaps.
- **Brno's page is written from the approved template**, with no departure
  from it. Brno's own notice is number 72 (France holds 69-71 on
  `france-build-2`). The ČSÚ and ČÚZK notice titles now list the six Czech
  cities, and items 32 and 33 in `data_sources.md` match. The "OpenStreetMap
  (rail geometry)" notice names the Czech tram lines.
- **Rows written:** `docs/data_sources/czechia.md` has rows for all six
  (registries, transit, OSM geometry, boundaries), and
  `docs/excluded_categories.md` has a section per city.
  `check_provenance.py` names all six OK. `check_scope_disclosure.py` passes
  for 81 cities. `check_provenance.py` gained the Czech display-name
  overrides (Plzeň, Liberec (Regional), Most (Regional)).
- **For the lander, at landing:**
  - Notices 69-71 must land before or with 72, or the contiguity check
    fails.
  - The ČSÚ/ČÚZK titles and the OSM notice name all six cities, so a
    partial landing trims them to the cities that land.
  - `macro_facts.json` (`check_macro_facts.py --write`), the
    `map_inconsistencies.md` rows (cleanup's city-landed sweep), the
    master-list counts and each city's measured macro-label width are all
    landing-time work.
  - The `mode` key waits for the macro-legend branch.

### 2026-09-30 - The six Czech business legs built; Brno's stations from the feed, with request stops kept and depot runs dropped

- **All six business legs ran on the shared chain, each RÚIAN control
  passing, and 100% of storefronts were placed.** Brno has 7,200. Plzeň
  has 3,508, Olomouc 2,235 and Ostrava 3,960. Liberec (Regional) has
  2,488, of which Liberec 1,873 and Jablonec 615. Most (Regional) has
  1,025, of which Most 787 and Litvínov 238. Each is slightly under the
  screen's 2026-09-27 figure (Brno 7,229, Liberec 2,498, Most 1,030).
  - **Why lower:** the screen ran before the owner's 2026-09-29 catch-all
    call (96990 and the bare 969), and the taxonomy now structurally
    excludes 963 (funeral services).
  - **Which to publish:** the pages use step 2's figures, never the
    screen's.
  - **The two-obec path's first real use** is Liberec and Most: every file
    ran its own control, and each obec's count was printed.
- **Two shared modules for the Czech tram cities, beside Prague's own
  files, which stay as they are:**
  - **`pipeline/countries/czechia_fetch.py`** is imported only by the
    `fetch_sources.py` scripts. It checks the shared national files and
    never fetches them. It always fetches the rolling sources: KORDIS's
    feed, each obec's RÚIAN file named through ATOM, and the two OSM
    queries. OSM goes one query at a time, with a 60-second wait before its
    one retry (the owner's staggering rule). Both mirrors 504'd once on
    Brno's boundary, and the retry answered.
  - **`pipeline/countries/czechia_boundary.py`** turns each obec's OSM
    relation into a polygon, checks that its `ref` ends in the RÚIAN obec
    code, and gates the union on the Czech Statistical Office's area. Brno
    measured 230.1 km².
  - `check_no_fetch_in_steps.py` passes.
- **Request stops are stops: 25 of Brno's 149 stations were being dropped
  as "non-revenue".** KORDIS codes every request stop (*na znamení*)
  `pickup_type`/`drop_off_type` 3, "coordinate with the driver", which GTFS
  counts as boardable. `pipeline/stations.py`'s `boardable_stop_ids` accepted
  only 0. Among the stops lost were Stránská skála and Líšeňská.
  - **The fix:** a `boardable` parameter, which Brno passes as
    `("0", "2", "3")`. The default is unchanged, so no built city's output
    moves unannounced.
  - **Rejected:** changing the default. It is the correct reading of the
    GTFS spec, but it could move other cities' station tables, and the
    module is the app/chrome role's.
  - **Handed to cleanup:** checking whether any built city's feed carries
    2 or 3.
- **A line serves a Brno station when it calls there on at least 10% of its
  trips in one direction.** The feed runs about 2.5 months of timetable, and
  the union of every trip gave line 4 54 stations where its route has 24.
  - **The rule:** Riga's `PATTERN_MIN_SHARE` (10%), taken per station
    rather than per exact stopping pattern. Line 10 splits its Líšeň branch
    over patterns that are each under 10%; the branch holds 8% of the line's
    trips, and other lines serve it.
  - **The effect:** 148 stations, of which only the Vozovna Medlánky depot
    is dropped, since no line calls there on more than 2 to 5% of its trips.
    146 are inside the city at a 336 m median gap, so the rings stay halved.
    Line 2's two Modřice stops are excluded.
  - **Gate 3 against OSM's route relations** agrees on 9 of 11 lines. Line
    1 has 47 stations in the feed against OSM's 36, and line 10 has 38
    against 27. OSM carries only their main routes, while the feed runs
    line 1 via Tábor and line 10 to Technologický park and Bystrc on 12 to
    21% of their trips, every sampled weekday from 2026-10-01 to 12-02.
    This is recorded rather than "fixed": the feed is the operator's.
  - **Station-spacing floor:** 200 m, Riga's and Aarhus's, instead of the
    shared 400 m metro default. It still refuses Brno's uncollapsed
    platforms (42 m median).
- **The six Czech pages are numbered 150-155**, in build order, so they do
  not collide at landing with France's 76-95 or the other build branches.
  The other build sessions were told. `scaffold_city.py` numbers from the
  highest page in its own tree, so each page was scaffolded and then its
  `app/cities.py` path pointed at the block.
- **Not yet done:** the rail steps for the five OSM cities wait for
  `pipeline/osm_tram.py` on the tram build branch (the owner's priority
  rule). Brno's station step was built now because it depends only on
  KORDIS's feed. Brno's step 3 draws OSM geometry by ref and is next.

### 2026-09-30 - czechia_register reads several obce and RES in chunks; Prague reproduced byte for byte at a 0.37 GB peak

- **The Czech builds have the owner's go, confirmed in this session**
  ("Go ahead", 2026-09-30). The tram kit relayed it with six working rules,
  and this session asked the owner to confirm before scaffolding anything.
  The builds follow the rules: business legs first, and the Czech rail steps
  once `pipeline/osm_tram.py` is on the tram build branch. Every entry goes
  here, not in `DECISIONS.md`.
- **`pipeline/countries/czechia_register.py` now reads one RÚIAN file per
  obec.** A city that spans two obce (Liberec with Jablonec, Most with
  Litvínov) declares `OBEC_CODES`, `RUIAN_ZIPS` and `RUIAN_CRS_CONTROLS`,
  each keyed by obec. Every file runs its own coordinate control, and the
  files concatenate, with an exit if an address code repeats. Such a city's
  output gains an `obec` column and a per-obec count for its page. Prague's
  one-obec config (`OBEC`, `RUIAN_ZIP`, `RUIAN_CRS_CONTROL`) takes the same
  path as a single entry, so its output is unchanged. **Rejected:** a
  regional step 2 per city that calls the module twice and concatenates.
  That would put the obec loop in two city folders instead of one shared
  place.
- **RES is read in 500,000-row chunks, keeping only the owners the city's
  establishments point to**, rather than the whole 543 MB file at once.
  Filtering before the dedupe keeps each ICO's first row in file order, as
  the whole-file dedupe did.
- **The control: Prague, run from the build branch into the scratchpad.**
  The shared `data/prague/processed/` was not touched (the shared-junction
  rule). The output's SHA-256 matched the saved baseline (`9153d4d0…`), and
  all five baseline counts matched `outputs/prague/baseline.json`:
  84,192 in obec, 27,327 bucket rows, 26,711 storefront rows, 25,185 placed
  and 12,932 named. **Measured peak 0.37 GB RSS in 17 s**, so a Czech step 2
  is not a heavy job under the owner's 2 GB margin rule. The Czech step 2s
  run one at a time, each announced as a 0.5 GB job. `drift_check.py prague`
  was not run, because it would rewrite the shared processed files from a
  branch; the byte-identical step 2 output is the same test for this change,
  and the lander re-runs it at merge.
