# DECISIONS drafts - Czech kit (`worktree-czech-kit`, then `czech-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

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
