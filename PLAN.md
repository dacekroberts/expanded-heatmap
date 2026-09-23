# Plan


Open work only. Completed work and the reasoning behind it live in
[`DECISIONS.md`](DECISIONS.md); the settled state is in
[`docs/project_context.md`](docs/project_context.md).

Rules that make the rest work:

- **Commit after every green step.** A commit is the baseline
  `pipeline/drift_check.py` diffs against.
- **Log every judgment call in `DECISIONS.md` as it's made** (see the
  `decisions-entry` skill).
- **Live-verify a city's data before building it** (`add-city` Step 0).
- **Run `python pipeline/drift_check.py` after any pipeline change.**

Legend: `[ ]` open, `[x]` done (a done item stays only until its
`DECISIONS.md` entry exists), `[~]` in progress.

---

## Now

- [x] **Region switcher on the macro map — DONE 2026-09-22 (`2121ada`).**

The macro map opens on the United States and re-centres on any other region,
which is what `docs/scaling_thresholds.md` required before a city outside North
America. `app/cities.py` carries the region model (`f80d04b`); `app/Overview.py`
carries the radio, the region-aware caption and the fix.

**The fix was `st.session_state.pop("macro_map", None)` on a region change.**
`st.pydeck_chart(on_select="rerun")` persists the viewer's view under its widget
key and restores it on rerun, ignoring `initial_view_state`. A per-region key
was tried and rejected: Streamlit restores the previous key's state when the
viewer switches back.

**The constraint held and was measured:** zoom 1.4525 in both regions, centre
34.067N to 48.599N. Re-fitting on Canada's cities would give 1.5048 and
invalidate all fourteen pixel `label_offset` values.

**Keep this warning for anyone editing the macro map's view:** that same
persistence makes a changed `initial_view_state` invisible in a browser session
that has already rendered the page, across server restarts included. Test in a
fresh session (a new query string is enough) or you will debug correct code.

- [x] **`deploy-verify` on the switcher — steps 1, 2, 3, 6, 7, 8, 9, run
2026-09-22.** No named scope fitted: the change is the Streamlit macro map plus
an import under `app/`, where `map-chrome` covers overlays inside the per-city
rendered map HTML and says the app is usually not needed. Passed: lean-venv
start with no import error, all 14 cities in the DOM, the real click path
through a name pill to a city page in BOTH regions (`st.switch_page` survives
the new widget), caption flipping, zoom pinned, attribution present, dark mode
inverting the basemap with the radio still legible. The only console errors
were two `ERR_CONNECTION_REFUSED` on `/_stcore/health`, bracketed by `200 OK`
either side — the stop/start gap, not the running server.

- [ ] **"Vancouver (Regional)" is clipped at the left edge at 375px — in the
Canada region as well as the US one.** Found during the run above. NOT a
regression: `fit_view` is byte-identical to the pre-switcher commit and frames
`IN_DEFAULT_VIEW` (US only), so Vancouver was never in the fitted box. But the
switcher makes it newly user-facing, because it now invites a viewer to look at
Canada and Canada still does not frame its own westernmost city. This is the
direct cost of RE-CENTRE-NEVER-RE-ZOOM: centring on Canada's midpoint leaves a
long label 25 degrees west of centre.
Options, in increasing cost: shorten the label to "Vancouver"; give that city a
right-side anchor; or set `REGIONS[i]["zoom"]` for Canada, which exists for
exactly this and costs a re-measure of that region's `label_offset` values.
Desktop is unaffected — the label is fully visible there.


- [ ] **Next city** - pick from the list below. Start with the `add-city`
  Step 0, then `scripts/scaffold_city.py` (the `scaffold-city` skill). That
  build is also the first real test of the scaffold: record in `DECISIONS.md`
  whether it saved effort (estimated at about 10%) and fix any template that
  needed rewriting.
  **Vancouver has a build brief ready** - `docs/build_briefs/vancouver.md`
  banks Step 0's answers (all three endpoints with their traps, EPSG:32610,
  the rejected address join against the spatial one that works, both required
  notices with exact wording), so that build starts at the scaffold command
  rather than at Step 0. **One of its seven open questions is an owner
  decision rather than a build one:** `businesstradename` is blank on 63% of
  rows, and restricted to the categories this project maps, 16.94% of
  displayed names match the person pattern - the storefront filter makes it
  worse, not better. What a pin displays on that fallback wants settling
  before the map renders, not after.
  - [x] **DONE 2026-09-21 — two clause families added to `read-licence`**
    (step 6's third adjacent category, and a new step 6b). Landed once
    Vancouver was built, and timely: **Montréal is one of the two worked
    examples**, and its build had just started.
    Original item, kept until its `DECISIONS.md` entry exists:
    **After the Vancouver build lands: add two clause families to the
    `read-licence` skill.** Deferred deliberately so the skill settles first
    (it was written 2026-09-21). Both recur and both were found by the global
    country screen. **(a) Licences that require disclosing TRANSFORMATION, not
    just crediting the source** - INEGI demands you "notificar al usuario final
    de cualquier análisis o transformación que haga a la información", and
    Montréal requires stating whether modifications were made *or
    interpretations drawn*. This project always triggers these (ring density,
    bucketing, storefront filtering), so a bare source credit does not comply.
    **(b) Registers that do the privacy work upstream** - France masks
    non-diffusible records including geolocation, Edmonton publishes
    `<REDACTED FOR PRIVACY>` on 9.3% of rows, Austria's GISA strips personal
    data before release. Worth checking before building a residence filter,
    because the work may already be done. Evidence for both is in
    `docs/global_country_shortlist.md`.

- [~] **Evaluate the map-only navigation pilot** (started 2026-09-20; see
  `DECISIONS.md` and `docs/navigation_sidebar_and_city_links.md`). The
  Overview's fallback link list is kept (decided 2026-09-21). The hop-between-cities
  gap is closed with a "Cities" dropdown on each city map (2026-09-21). Open: the
  final go/no-go. To revert, set `MAP_ONLY_NAV = False` in
  `app/cities.py`.
- [ ] **Midnight slate theme: the Streamlit page AND the map palette, as one
  change.** No longer deferred - the blocker was the assumption that an
  explicit theme forces the site dark-only, and separate
  `[theme.light]`/`[theme.dark]` blocks keep the toggle (tested). Decided
  2026-09-21 to stay on Streamlit rather than go static; see `DECISIONS.md` for
  why, and for the measurement showing a map-chrome reskin alone is not worth
  doing (it is ~15% of a city page's pixels; the tiles are filtered and the
  data colours are fixed, so no `--dm-*` variable touches them).
  **Everything needed to build it - palette, both value sets, the traps, the
  verification checklist - is in `docs/theming.md`.**
  - [x] `.streamlit/config.toml` with both light and dark blocks; the chooser
    Streamlit had been suppressing is back (System / Light / Dark).
  - [x] The map's `--dm-*` values swapped to slate, the macro map's duplicate
    copy removed, and everything sourced from the new `pipeline/theme.py`.
    `scripts/check_theme_sync.py` guards the one unavoidable TOML duplicate.
  - [x] **Two theme controls reconciled (option A, 2026-09-21).** With no
    stored choice a map follows the page it is embedded in; an explicit click
    wins from then on; a standalone map follows the OS preference. Verified
    all three: ambient-dark page gives a dark map (`storedTheme: null`), a
    click stores `light`, and that survives a reload on a dark page. Options B
    (our button drives the page, overriding Streamlit's widget CSS by hand)
    and C (remove the in-map button when embedded) were rejected - see
    `DECISIONS.md`.
  - [ ] Sweep the remaining hardcoded colours in `app/` now that a dark page
    exists: `Overview.py` still has literal `white` and
    `#1c2b2a` (lines ~90, ~139) for the macro map's markers and labels. Check
    contrast numerically against `#0B1220`, not by eye - a 1.01:1 label looks
    like empty space rather than a bug.
  - [x] Reconciled the two overlapping handoffs into `docs/theming.md`
    (2026-09-21). Both originals are in git history.

## Next cities, in ease order

- [x] **New York - built 2026-09-21.** The premise recorded here was wrong:
  DCWP `w7w3-xahh` is a regulated-activity licence list, not a business
  registry (no restaurants, grocery, clothing or salons in it at all), and New
  York has no general business licence. Coverage is assembled from four
  registries instead, the `nyc_dca` skeleton was retired, and 29 subway
  services are drawn as the 11 trunk lines MTA itself signs. See `DECISIONS.md`.
  Open follow-ups:
  - Its map is **10.3 MB**, against 3.5 MB for Los Angeles - 44,361 pins,
    because dense stations put 71% of businesses inside a ring (Los Angeles:
    24%). Measured levers: rounding coordinates to 5 dp saves 1.4 MB and loses
    nothing (Folium emits 17 significant digits for a 5-pixel dot, and it would
    re-baseline all five cities' committed outputs) — **and as of 2026-09-21
    this is now safe to do, but only for business points.** Transit coordinates
    are exempt from `COORD_DP` (see `pipeline/map_common.py` and
    `DECISIONS.md`): at 5 dp the old behaviour would have started modifying
    MTA's and LA Metro's geometry as a silent side effect of a size tweak,
    which their terms restrict. Keep the exemption if you lower `COORD_DP`; indexing repeated station
    and ring strings saves ~1.2 MB; dropping the opt-in all-city heat layer
    saves 2.0 MB. Decide before the public deploy.
  - Retail is less complete here than elsewhere (a clothing shop needs no
    licence from any of the four registries). Said plainly on the city page;
    worth repeating in `docs/excluded_categories.md`.
- [x] **Philadelphia - built 2026-09-21.** The WKB parsing this item predicted
  was never needed (the Carto SQL API evaluates `ST_X`/`ST_Y` server-side), and
  `phl_licensetype` is filled from the full 50-type pull. What it left behind:
  - Two open licence questions, both to settle before the public deploy:
    SEPTA's trademark/commercial clause, and the "City of Philadelphia
    License", which reserves all database rights while granting nothing
    explicitly. See `docs/data_sources.md`.
  - Personal services is **absent**, not thin - the only such city. Stated on
    the city page and in `docs/excluded_categories.md`.
  - Regional Rail (52 well-spaced in-city stations, no thinning needed) is the
    obvious later addition if the commuter-rail exclusion is revisited.
  - The Girard Avenue Trolley's label uses SEPTA's own `#FFD700`, which is the
    lowest-contrast of the four over the orange heat wash. Cosmetic; swap for a
    darker gold if it reads badly on a real screen.
- [x] **Boston - BUILT 2026-09-21.** 3,164 premises, 2,410 within a ring
  across 57 in-city stations; see `DECISIONS.md`. What it left behind:
  - **MassDOT's acknowledgement notice is now ACTIVE**, not conditional, which
    takes the mandatory-notice count from four to five. The city page carries
    "Rail alignment data provided by MassDOT/MBTA"; the site-level placement is
    part of the same job as the other four.
  - **The residence check is blind here and the 0.00% reading is a measurement
    gap, not a clean result.** Boston's addresses carry no unit designators at
    all, so there is nothing for it to read - the same shape as San Diego's old
    0.03%, which became 2.80% once a parcel join replaced address text. What
    limits the real exposure is that a food-service or package-store licence
    requires commercial premises. The ISD table's `property_id` IS Boston's
    assessing parcel id, so a parcel join against the city's Property
    Assessment data (ODC-PDDL) is available if that is ever not enough.
  - `Business Inventory` stays recorded as available and deliberately unused;
    revisit only if the city extends that survey city-wide.
  - Regional Rail (52 well-spaced in-city stations) is the obvious later
    addition if the commuter-rail exclusion is ever revisited - the same
    follow-up Philadelphia has.
- [x] **Washington D.C. - BUILT 2026-09-21** as the ninth city; see
  `DECISIONS.md`. 5,230 premises, 3,860 within a ring across the 40 in-District
  stations - the highest ring coverage in the project at 73.8%. The first
  non-NAICS registry here to cover all three buckets on its own. Follow-ups it
  leaves behind:
  - **Three Step 0 findings recorded in this file were wrong, and the
    corrections are the useful part.** (a) "Trade name is missing on 49% of
    storefront rows ... the Los Angeles trap at half LA's severity" was
    measured before the category exclusions; on the rows that reach the map the
    gap is **26.9%**, 85.6% of those carry a company-shaped `ENTITYNAME`, and
    the residual is **14 pins / 0.36%**. (b) "`MAR_ID` should recover the rest"
    was wrong - the 452 rows with no coordinates are the **same rows** that
    lack `MAR_ID`, because they are what the District's own geocoder failed on,
    so a Census geocoding step was needed after all (it recovered 387). (c) The
    catch-all count was 14,770 for `General Business`; scoped to active and
    in-District it is **11,074**. The lesson is the one this file keeps
    relearning: a Step 0 percentage measured on the wrong denominator is worse
    than no percentage.
  - **`Delicatessen` is ambiguous in the source and stays ambiguous.** D.C.
    issues it to sandwich shops and to corner shops alike, so ~180 premises
    could honestly read as Food service or Retail. Recoverable only by
    classifying trade names, which is a project of its own - the same shape as
    Miami's `SERVICE BUSINESS`. Stated on the city page rather than hidden.
  - **A parcel-based residence rule is available and unused.** `SSL` is on
    **91.1%** of mapped rows - better coverage than Miami's `FOLIO` at 45.7%
    and comparable to what Philadelphia joins against. D.C.'s addresses carry
    almost no unit designators, so the address-text residence check reports
    0.00% and that is a measurement gap, exactly as in Boston. The structural
    signal that partly replaces it is `ENTITYTYPE`: 14 pins are a sole
    proprietorship with a person-like displayed name. Do the parcel join if
    that ever stops being enough.
  - **The feed expires in ten days and the key is not in the repo**, so this
    city cannot be rebuilt from a clean checkout without `WMATA_API_KEY` set
    and a fresh download. `outputs/washington_dc/` is committed, so the app
    does not care; `drift_check.py` does, and will report a missing raw input
    rather than drift. Worth deciding whether the drift check should say so
    more clearly for key-gated cities.
  - **The Silver Line is harder to trace in LIGHT mode than the other five**,
    and that is accepted rather than engineered around. See `config.py`'s
    `LINE_NAMES` comment for the measurements in both modes and the two
    alternatives that were rejected.
- [x] **Miami - BUILT 2026-09-21** as the project's first regional city; see
  `DECISIONS.md`. 3,775 within-ring pins across 42 stations in six
  municipalities. Follow-ups it left behind:
  - **Its licence position is not established** - Miami-Dade's `licenseInfo` is
    purely an accuracy disclaimer and says nothing about reuse, and its GTFS has
    no `feed_info.txt` and no developer terms were found. Same shape as the
    Philadelphia and NYC questions. Settle before the public deploy.
  - **`SERVICE BUSINESS` (28,010 rows) is excluded and contains some genuine
    repair shops**, so the map undercounts small repair and service premises.
    Recoverable only by classifying free-text `OCCDESC` - a project of its own.
  - A **parcel-based residence rule is available but unused**: `FOLIO` is on
    100% of City of Miami rows and only 45.7% of the regional set, so it would
    apply to half the map. Revisit if the coverage improves.
  - Ring coverage is 12.6%, the lowest here, because the business set is
    county-wide while the rail is one line plus a loop. Consider whether the
    all-businesses toggle should be scoped to station municipalities.
- [x] **Mexico - BUILT 2026-09-22, two cities.** Mexico City (city 15) and
  Guadalajara (Regional) (city 16). Monterrey remains out: it matches no feed
  under `monterrey`, `metrorrey` or `nuevo leon`. What the build produced
  beyond the two cities:
  - **`pipeline/taxonomies/scian.py`**, because SCIAN is NOT NAICS where it
    matters - retail is 46 against NAICS's 44-45, so `naics.py` would have left
    ~46% of a DENUE file unclassified. Food 722 and personal 812 do transfer.
  - **`pipeline/countries/`**, the country/city config split, done at the
    SECOND city as scheduled and proven behaviour-neutral by zero drift.
  - **`.claude/skills/osm-rail/`**, because neither city could use GTFS: Mexico
    City's agency hosts are unreachable and Guadalajara's only feed expired
    2023-01-28 and predates an operating line. Taipei, Sao Paulo and Israel are
    non-GTFS too, so this stops being an exception.
  - Gate 3 ran for Guadalajara and passed against SITEUR's published counts; it
    is UNAVAILABLE for Mexico City and recorded as such rather than faked.
  - Densities are 818 and 659 per station and are **not comparable** with the
    licence-register cities: DENUE is an establishment census. Said on both
    pages.

- [ ] **New Orleans - DEFERRED POST-DEPLOY by the owner (2026-09-21),
  alongside Seattle.** The pre-deploy city scope is the nine that are
  built; this and Seattle's multi-municipality build come after. Findings
  kept so returning costs nothing. Screened 2026-09-21, needs a real
  Step 0.** `iqay-p646`
  "Active Occupational Licenses", 16,396 rows, and the **cleanest licence of
  any candidate: CC0 1.0, explicitly declared**. Has `businesstype`,
  `businessaddress`, `the_geom`. Two sibling datasets exist (`abc4-h3u3`, an
  application-workflow file that also carries `naics`, `category` and an
  `ishome` flag; `hjcd-grvu`, 37,902 rows) - pick one deliberately rather than
  merging them. Rail is streetcar-only, which is a **scope** question for the
  owner, not a data one. Privacy flags: `ownername` and `businessphone`
  columns, and the name fields are inverted on some rows (blank `businessname`
  with the trade name sitting in `ownername`) - Boston's trap again.
- [ ] **Seattle - deferred by the owner 2026-09-21, and scoped as the project's
  first MULTI-MUNICIPALITY city.** Do not re-probe the Seattle registry itself;
  the findings are in `docs/city_shortlist.md`. On that evidence Seattle's own
  data is the best-equipped of any candidate - an official nightly export,
  **active-only by construction**, 54,604 rows with real NAICS (no new taxonomy
  module), a trade name, and point geometry (no geocoding step). It is on
  ArcGIS rather than Socrata, which is why earlier screens missed it.

  **The owner's intent (2026-09-21): full line coverage, not just the city.**
  This is deliberately the first test of merging several jurisdictions'
  business data into one map, and it **supersedes the standing rule that
  stations in another city are a new project rather than a config change** -
  for Seattle specifically, by the owner's decision. The named jurisdictions
  are Seattle, Shoreline, Lynnwood, Tukwila, Federal Way, Bellevue and
  Redmond. What to check before scoping the work:
  - **The station list is wider than seven jurisdictions.** Link also stops in
    **Mountlake Terrace** and **SeaTac** on the 1 Line and **Mercer Island** on
    the 2 Line; if Federal Way is in scope then the extension also runs through
    **Des Moines** and **Kent**. So plan for roughly ten to twelve, and settle
    the list from the real GTFS stop set against a Washington municipal
    boundary layer rather than from memory - the same discipline that caught
    16 Trolley stations in San Diego and 54 in Los Angeles.
  - **Each jurisdiction is an independent Step 0**, with its own registry,
    schema, classification, coordinate quality, licence and privacy profile.
    Seattle's own data says nothing about Lynnwood's. Expect some to have no
    usable registry at all, and decide up front what the map does where data is
    missing - a gap in coverage is the failure mode that made Boston's
    `Business Inventory` unusable, and it would appear here as whole
    suburbs reading as empty rather than as unsurveyed.
  - **The architecture already supports the taxonomy side.** Taxonomy plurality
    means each jurisdiction can carry its own module mapping into the shared
    three buckets, and `map_common.py` never names a taxonomy, so the map layer
    needs no fork. If several use NAICS (likely in Washington), they share
    `naics` and the merge is mostly plumbing.
  - **What genuinely does not exist yet** is multi-polygon scope: `CITY_KEEP`
    and the boundary filter assume one city. A multi-jurisdiction build needs a
    boundary *set*, per-jurisdiction row provenance on every business (so the
    map can say which registry a pin came from, and so a single city's data
    going stale is visible), and a cross-registry dedup rule for businesses
    licensed in more than one jurisdiction.
  - **Naming stays neutral**: this would be a region, and the project is never
    named after a city - so the page name needs deciding too ("Link light rail"
    rather than "Seattle" may be the honest label if it spans twelve cities).
- [ ] San Jose, Denver, Austin, Charlotte, Fort Worth, **Dallas, Houston**:
  ruled out. Dallas was ruled out 2026-09-21 on **currency** - its
  certificate-of-occupancy feed froze on 2022-11-15 and the dashboard this plan
  pointed to is not a dataset at all (HTTP 403, 0 columns). See
  `docs/city_shortlist.md`.
- [ ] **Fifteen further rail cities were screened shallowly and nothing
  surfaced - that is NOT a disqualification.** Atlanta, Baltimore, Portland OR,
  Phoenix, Minneapolis, St. Louis, Cleveland, Pittsburgh, Detroit, Jersey City,
  Tucson, Sacramento, Salt Lake City, Honolulu, Buffalo. Twelve of those
  returned HTTP 404 from Socrata's discovery API, which means "not a Socrata
  domain", and the ArcGIS pass searched titles only. **Seattle proves the
  point**: it came back "no matching datasets" on Socrata and has a 54,604-row
  official layer on ArcGIS. Any of these needs a proper per-portal check before
  being written off.

## Structure

- [x] ~~Move GUADALAJARA's and MADRID's fetching out of their step files~~ -
  **done 2026-09-22; all three exceptions are closed.** Mexico City first as
  the worked pattern, Madrid by its own session on the unmerged
  `spain-app-wiring` branch, Guadalajara last -
  `pipeline/guadalajara/fetch_sources.py`, which took the three Overpass
  queries with it because each one's comment is addressed to whoever edits
  the query, and that is no longer the step. Proved both ways: zero drift
  with the cache present, and step 1 and step 2 both exiting 1 with "Run
  pipeline/guadalajara/fetch_sources.py first" with `data/guadalajara/raw/`
  moved aside. **Guadalajara's two-pass retry was kept rather than unified
  with Mexico City's single pass** - neither has been measured against the
  other, and a refactor is a bad moment to quietly change a retry policy. At
  the `spain-app-wiring` merge the two sessions' Guadalajara fetchers were
  resolved in the BRANCH's favour, because that one goes through the shared
  `pipeline/osm.py` (which rejects a `remark` and a partial 200, not only an
  empty one, and still retries twice) while master's repeated the logic in the
  city; its two step files were taken from MASTER, so both Mexican cities name
  the reader `read_cached`. **The rule is now a check rather than a
  convention:** `scripts/check_no_fetch_in_steps.py`. Madrid was listed there
  under `KNOWN_GAPS` until `spain-app-wiring` landed, and the check fails on a
  gap that has silently been fixed, so landing the branch forced both entries
  out - which is what that failure mode is for.

  The original finding: move the fetching into a `fetch_*.py`, as the other
  fourteen cities do.
  Demonstrated 2026-09-22: `python pipeline/drift_check.py` in a worktree with
  no `data/<city>/raw/` **fetched over the network for all three** - a 39 MB
  DENUE zip, a Madrid census CSV, Overpass responses and CRTM layers - and
  then reported zero drift. Toronto, by contrast, stopped with "no
  data/<city>/raw/ - nothing to run against", which is the correct behaviour.
  The calls are cache-guarded, so this is invisible on a machine that already
  has the data. **It changes what a passing drift check means:** for those
  three it asks "does the current upstream still produce the committed output"
  rather than "does the committed code". Build-session work - each city's
  context is needed.
- [x] ~~Three `step3_geocode.py` files still reach the network, one import
  deep~~ - **closed 2026-09-22, by moving the boundary rather than the code.**
  Los Angeles, New York and Washington DC import `geocode_addresses` from
  `pipeline/census_geocoder.py`, which POSTs address batches to the US Census
  geocoder on a cache miss; `drift_check.py` globs `step*.py`, so it ran them
  like any other step and a fresh checkout geocoded over the network inside a
  drift check. That module's docstring gave it away: "off the network **after
  the first run**".

  The recorded plan was to hoist the download into `fetch_sources.py` as the
  four cities did, and **that was the wrong fix.** There is no URL to hoist:
  the batch is derived from the step's own filtering, so moving it means
  moving the address preparation with it. What was actually wrong is narrower
  - **a step may fetch when a person runs it; a drift check may never fetch**
  - so `pipeline/offline.py` puts the guard at that boundary, `drift_check.py`
  sets `HEATMAP_NO_NETWORK` for every step it runs, and an uncached batch
  under that flag refuses instead of requesting. Proved three ways: refuses
  uncached, still serves a cached batch, and is inert when the flag is unset,
  so a person running step 3 is unaffected. `check_no_fetch_in_steps.py`
  reports such a module as **guarded** - a third answer, not a pass in
  disguise - and fails if `drift_check.py` stops arming the guard.
- [x] ~~Wire Toronto's `STATIONS_COLLAPSED_EXPECTED`~~ - **done 2026-09-22,
  and it was a mis-wiring rather than a missing check.** Step 1 compared the
  COLLAPSED count (110) against `IN_CITY_STATIONS_EXPECTED` (108), printing a
  NOTE every run while the right constant sat unread. Both now guard what they
  name, an in-city check was added after the boundary filter, and the docstring
  no longer claims `excluded_stations.csv` is empty (it has two rows). Verified
  by running step 1: 234 -> 110 -> 108, two excluded, zero NOTEs.
- [x] ~~Have Guadalajara's step 2 import `DENUE_STATE_COLUMN` and
  `DENUE_MUNICIPIO_COLUMN`~~ - **done 2026-09-22, and it was BOTH Mexican
  cities.** Zero drift on both after the substitution. The `municipio` in each
  city's output-column list is left as a literal on purpose: that is this
  project's output schema, not DENUE's input column, and both sites say so.

- [x] ~~Finish the `check_stale_claims.py` category-B pass~~ - **done
  2026-09-22**, seven passes, **74 flagged counts to 35**, files scanned 39 to
  27 as dated records were recognised. Stopped at the floor rather than at
  zero: what remains is correctly scoped facts ("all five boroughs", "the six
  pre-1998 municipalities"), dated evidence in the two country trails, and
  three false positives from single-line quote matching. **Continuing would
  mean tuning the checker to silence rather than finding defects.** Real finds
  are listed in that day's `DECISIONS.md` entries. If a future pass wants more
  signal, the lever is a new detector - not a narrower category B.

- [x] ~~Write `scripts/check_stale_claims.py`~~ - **done 2026-09-22.**
  Reports and always exits 0. On its first real run it found three notices in
  the deploy gate marked NOT YET DISPLAYED - Chicago, SFMTA and LA Metro - that
  were all in `_NOTICES` and had been displayed for some time, so the list that
  gates the public deploy was understating this project's compliance. Tuning
  history is in the module docstring and the sweep skill: digits matched 1,012
  measurements, undetermined counts 265 mostly-correct scoped facts, and
  requiring a determiner cut it to 74. **Known blind spot:** category A matches
  on built CITY names, so agency names miss - two of the three notices above
  were found by a follow-up grep rather than by the tool.

- [x] ~~Fill in the remaining local taxonomy skeleton (`phl_licensetype`)~~ -
  **done 2026-09-21** from the full `SELECT DISTINCT licensetype` pull; all 50
  active types carry an explicit verdict. No taxonomy skeletons remain.
  (`nyc_dca` was retired rather than filled - see `DECISIONS.md`, 2026-09-21.)
  The check this item asked for paid off twice: New York needed four sources,
  and Philadelphia turned out to have **no source at all** for one bucket.
- [ ] **Close the residence blind spot in `check_personal_exposure.py`.** It
  detects a home only by an `APT`/`FL`/`RM`/`#` indicator, so a sole trader at
  a detached house reads as clean - which is why Philadelphia scores 0.00%.
  **Tested both candidate signals against Philadelphia's property register on
  2026-09-21, and the results corrected this item** (see `DECISIONS.md`):
  - **Mailing address == premises does NOT work. Do not build it.** It matches
    41.9% of mapped pins, because a shop's mailing address is normally its own
    premises. No discriminating power at all.
  - **Parcel land use works, but only combined with owner-occupancy.** Joining
    `opa_account_num` to `opa_properties_public` succeeds on 94% of licences
    and is a real signal - but "residential parcel" alone flags 7.95% of pins,
    including **147 thirty-plus-seat restaurants on `APARTMENTS > 4 UNITS`
    parcels**. In a dense city, shops sit in residential buildings; land use
    alone would delete hundreds of real storefronts.
  - **The best signal was one not listed here: a homestead exemption**, which
    Philadelphia grants only on an owner's primary residence. Also over-fires
    alone (162 of its 189 hits are `MIXED USE`, the rowhouse-with-a-shop where
    the owner lives upstairs), so it needs pairing too.
  - **Usable rule: a person-like name AND an Individual entity AND (a purely
    residential parcel OR a homestead exemption)** - 33 pins, 0.39%. The
    corrected exposure for Philadelphia is ~0.2-0.5%, not the 0.00% the unit
    test reported.
  - **Done for Philadelphia 2026-09-21.** The parcel join is folded into the
    existing Carto query rather than being a separate download, step 2 removes
    the 8 pins that are a person-like name at a purely residential parcel, and
    `check_personal_exposure.py` reports the land-use and owner-occupancy
    signals. The homestead exemption is reported but **not** filtered on - it
    over-fires on mixed-use rowhouses.
  - **All six cities checked 2026-09-21. Three are settled; three are scoped
    work for the pre-deploy batch.** Per-city status:
    - [x] **Philadelphia** - parcel join built, 8 pins filtered.
    - [x] **New York** - measured via `bbl` -> PLUTO (`64uk-42ks`), a key join
      because DOHMH and DCWP both carry a BBL. **0.02%** (10 pins of 62,444 on
      a One & Two Family lot with a person-like name). **No filter needed**, and
      it confirmed that only 1 of the 161 surname-first DCWP names is on a
      residential lot.
    - [x] **Chicago** - nothing to do: `business_activity` marks home-based
      businesses and the taxonomy already drops all of them (zero reach the
      map). Verified, not assumed.
    - [ ] **San Diego - filter BUILT and applied 2026-09-21, but its number is
      a floor.** It removes 42 pins (0.37%), against San Francisco's 1.19% and
      Los Angeles' 2.05%, and the gap is a method artifact rather than a fact
      about the city. This city's coordinates sit systematically 5-15 m from
      their own parcel (exact point-in-parcel matched 1 of 30 sampled pins; a
      25 m buffer matched 30 of 30) because they are placed at the street
      frontage and SanGIS parcels exclude road right-of-way. So 2,227 of 2,454
      lookups fall back to the buffer, where the conservative "every parcel
      within 25 m" test quietly clears any home with a rental next door.
      **RESOLVED 2026-09-21 - and the bulk-download advice this item used to
      give is wrong; do not follow it.** Paginating the layer costs ~26 s per
      2,000-row page, because `orderByFields` sorts 664,662 rows and
      `resultOffset` deep-pages through them: about two hours, abandoned at
      2.7%. The working method is `pipeline/san_diego/fetch_parcels.py` -
      **one buffered query per point with `returnCentroid=true`** (this layer
      supports centroid-only responses), picking the nearest centroid locally.
      That gives true nearest semantics in 2,463 requests rather than ~5,000.
      - **Rate limit, measured:** SANDAG's gateway sustains roughly 2
        requests/second for a run this long. ~7 req/s completed once; slightly
        faster was refused after ~500. Defaults are now 1 worker at 0.4 s,
        about 20 minutes. A refusal aborts and writes nothing.
      Original Step 0 notes, all still valid:
      Better placed than expected: it has all three signals after all.
      - Layer: `https://geo.sandag.org/server/rest/services/Hosted/Parcels/
        FeatureServer/0` - **one countywide layer, 1,089,758 polygons**, so the
        geographically split `Parcels_South`/`_North`/`_East` siblings are not
        needed.
      - **`ownerocc`** is an owner-occupancy flag (`'Y'` on 472,498 parcels,
        null otherwise) - the occupancy signal this city was thought to lack.
      - Land use is `asr_landuse` (numeric) with **no coded-value domain**, so
        the codes were verified empirically rather than guessed:
        **`11` = single-family detached** (571,236 parcels, `nucleus_use_cd`
        110/111, `unitqty` 1, mostly `ownerocc='Y'`) and **`17` = condominium**
        (199,972, `nucleus_use_cd` 171). Use **11 only**; exclude 17 for the
        same reason as San Francisco's Multi-Family and New York's
        multi-family lots.
      - Also available: `apn`, `unitqty`, `situs_community`,
        `nucleus_use_cd` (225 types, more granular if ever needed).
      - The registry adds a fourth condition for free: `ownership_type='SOLE'`
        (24,974 rows), the same kind of structural signal as Philadelphia's
        `legalentitytype`. Requiring person-like name + SOLE + `asr_landuse=11`
        + `ownerocc='Y'` makes this the most conservative of the three filters.
      - Use the buffered-point approach from Los Angeles
        (`fetch_parcel_residence.py`): an exact point-in-parcel test misses
        pins whose coordinates sit on a street centreline.
    - [ ] **San Francisco - MEASURED 2026-09-21, and it is the real one: 217
      pins (1.19%) to remove.** A person-like name on a Single Family
      Residential parcel that claims a homeowner's exemption. Mostly home
      caterers and home beauty/nail/pet-care businesses (NAICS 722320, 812112,
      812910, 812199). **This is required pre-deploy work, not optional** - it
      is 27x Philadelphia's 8 pins and the largest exposure in the project.
      Method that works, so it need not be rediscovered:
      - Source: "Assessor Historical Secured Property Tax Rolls"
        (`wv5m-vpq2`, PDDL), `closed_roll_year = '2025'`, selecting
        `use_definition`, `number_of_units`, `homeowner_exemption_value` and
        **`the_geom`**.
      - **Use the domain `data.sf.gov`.** `data.sfgov.org` returns 403 on
        `/resource/` while `/api/views/` works, which makes the data look
        unavailable.
      - **Join spatially, not by address.** `the_geom` is a point, so a
        nearest-parcel join in EPSG:32610 with a 40 m tolerance matches 93.4%
        at a median 1.4 m. An address join reaches only 43.8%, because
        `property_location` is a fixed-width composite
        (`'0000 2801 LEAVENWORTH         ST0000'`) and because stripping
        direction words breaks "North Point" and "South Van Ness".
      - Exclude **Multi-Family Residential** from the residential set (5,733
        pins - ground-floor retail in residential buildings).
      - Do NOT use the Land Use layer `fdfd-xptc` - it is **[ARCHIVED]**.
    - [ ] **Los Angeles - MEASURED 2026-09-21 and the largest of the three:
      ~1,000-2,000 pins.** The earlier note here was wrong: the MapServer layer
      `public.gis.lacounty.gov/public/rest/services/LACounty_Cache/
      LACounty_Parcel/MapServer/0` **does** carry `UseType`, `UseDescription`,
      `Roll_HomeOwnersExemp`, `Units1` and `Bedrooms1` - 92 fields - so no
      second dataset is needed. Method:
      - Query point-in-parcel per pin with `returnGeometry=false`; a batched
        multipoint query returns polygons and is far too slow.
      - A 400-point sample put 7.2% of person-like pins on a Residential parcel
        with a homeowner's exemption (13.6% of the 53.2% that matched).
      - **Expect a ~47% non-match** and investigate it before filtering: the ~9%
        of LA coordinates recovered by Census geocoding sit on street
        centrelines, outside any parcel. Filtering only matched rows would be
        the same partial-coverage mistake San Francisco's address join nearly
        caused.
    - **Carry the mixed-use lesson into each.** New York's largest land-use
      category is Mixed Residential & Commercial at 20,257 pins, ahead of
      Commercial & Office. Counting mixed use as residential would delete a
      third of that map.
- [x] **Record each data source's licence and terms of use** - done
  2026-09-21 in `docs/data_sources.md`, covering all 8 registries, all 5 GTFS
  feeds, the boundary layers and the basemap. Permissive terms were NOT the
  default they were expected to be. What came out of it:
  - [ ] **Display the required notices before publishing.** Chicago, SFMTA and
    LA Metro each require specific text; OSM's is already satisfied. Exact
    wording is in that file under "Notices this project MUST display when
    published". Part of the same app job as surfacing the two doc pages, and
    it **blocks the public deploy** - publishing without them breaches terms
    this project has now read.
  - [x] **Store the transit licence texts locally** - done 2026-09-21. All six
    are in `docs/licenses/` with source URLs, retrieval dates and SHA-256 in
    that directory's `README.md`. The stated position (unaltered,
    non-commercial, for compliance) is in `DECISIONS.md`.
  - [ ] **DECIDE: does this project satisfy MTA's "You will not modify or
    delete any of the data"?** Found 2026-09-21 while storing the texts, and it
    **blocks the public deploy** because New York is already built. The terms at
    `mta.info/developers/terms-and-conditions` were never read - `data_sources.md`
    recorded the landing page's "Our data feeds are free to use" instead - and
    they are substantive. Three clauses to weigh:
    - **"You will not modify or delete any of the data."** Same shape as LA
      Metro's clause, which the owner decided 2026-09-21 this project does not
      breach because it draws `shapes.txt` geometry unaltered. The argument is
      *stronger* here: MTA's very next sentence says "You may, however, create
      an app that uses some but not all of the data", which is exactly the
      29-services-drawn-as-11-trunk-lines choice. Likely the same verdict, but
      it needs to be stated rather than assumed.
    - **"You will not state or imply that the data is accurate, complete, or
      timely."** Check the New York page's prose against this before deploying.
    - **"You will not state or imply in any manner that your app is licensed by
      MTA."** Satisfied by construction, but note it when writing the notice.
    Also confirm the non-MTA-server requirement, which this project satisfies
    trivially: `outputs/` is committed and the app never fetches from MTA.
  - [x] **NYC Open Data's reuse position** - resolved 2026-09-21 from the
    primary source. Local Law 11 of 2012 "requires that data sets must be
    available without registration requirement, license requirement, or usage
    restrictions", so the absent licence field is compliance rather than an
    omission. One condition attaches (identify source, version and
    modifications when republishing), which this project already satisfies in
    substance via `data_sources.md` and `excluded_categories.md`.
  - [x] **LA Metro's "modification" clause and CTA's purpose limitation** -
    both decided 2026-09-21 by the project owner; reasoning recorded in
    `docs/data_sources.md` and `DECISIONS.md`.
- [x] ~~**Find San Francisco's boundary-layer endpoint.**~~ **Found - it was
  recorded all along, and this item was stale.** `wamw-vt4s` is in
  `pipeline/san_francisco/config.py` with a full comment block and in
  `docs/data_sources.md` in three places, all added 2026-09-21. But re-checking
  it 2026-09-21 found the recorded command **does not work**, so San Francisco
  still could not be rebuilt - the item was closed by identifying the dataset,
  never by running the command end to end:
  - **`data.sfgov.org` now 301-redirects**, and the documented `curl -sG` has
    no `-L`. It writes a **654-byte HTML redirect stub** into
    `sf_county_boundary.geojson` and exits 0. The failure surfaces much later
    as a confusing geopandas parse error.
  - **Fixed 2026-09-21** to `data.sf.gov`, which returns 200 and reproduces the
    stored file byte-for-byte (38,822 bytes, sha256 `ecf625b5…`). Changed in
    `config.py` (`COUNTY_BOUNDARY_URL` and its comment) and in
    `docs/data_sources.md`.
  - **The general lesson, now true twice for this city:** use `data.sf.gov`,
    not `data.sfgov.org`. The assessor roll hits the same host with a different
    symptom (403 on `/resource/`, recorded in `docs/data_sources.md`). Treat it
    as one rule for San Francisco rather than two separate gotchas.
  - **Worth generalising:** an endpoint recorded but never re-run is not
    verified. Consider a smoke check that re-fetches every recorded endpoint
    and asserts a plausible content type, rather than trusting the rows.

## Before deploying

- [x] **Sweep every city page for "accurate, complete, or timely" claims** -
  DONE 2026-09-21. Two real hits, both on the New York page (the MTA city):
  it called its restaurant coverage "close to fully covered", and said Retail
  was "less complete ... than in the other cities", which implied the other
  eight WERE complete. Both reworded, and a note in that page's docstring
  says why. Everything else was clean: the only "accurate" left in a
  rendered map is a pharmacy called Accurate Pharmacy, and the remaining
  matches are code comments. A positive statement now appears site-wide via
  `components.render_site_notices()` - every map is "a snapshot of a public
  register as it stood on the retrieval date". Original item:
- [x] (reference) The rule this implements:
  **Two** transit licences now forbid it in nearly identical words - MTA's
  "You will not state or imply that the data you provide through your
  Application is accurate, complete, or timely" and WMATA §6's - so this is a
  cross-city prose rule, not a per-city footnote. New York and **Washington
  D.C.** are both built and affected today. Check the city pages, the Overview
  and the map legends, and prefer "as recorded by <agency> on <date>" phrasings over
  anything implying completeness. Both texts are in `docs/licenses/`.
- [x] **Agency branding - DECIDED 2026-09-21 by the owner: keep the official
  route colours AND the real line names, and state non-affiliation plainly.**
  What those clauses actually prohibit is stating or implying affiliation,
  sponsorship or endorsement, which `components._NON_AFFILIATION` now does
  head-on on every page; nothing in the project reproduces a logo, wordmark
  or route-bullet artwork, and for WMATA the colour IS the line's name. No
  re-render was needed. Original item:
- [x] (reference) **The branding question: official route colours, AND the
  line names beside them.** Now **six** of the nine built cities, since D.C.
  draws WMATA's six published `route_color` values - and WMATA's is the clause
  that names "confusingly similar variants", which also rules out the obvious
  workaround of shifting a colour slightly. Full detail and the clause wording per agency are
  in `docs/data_sources.md` (item 5c, and the table under the GTFS notes).
  Recorded here because it is a permission question, not implementation work,
  and it was previously visible only in the provenance doc.
  - **It affects five of the seven built cities**, not the two first assumed:
    San Diego (MTS), Los Angeles (LA Metro), Chicago (CTA), New York (MTA) and
    Philadelphia (SEPTA). San Francisco and Miami are out of scope - both
    already draw this project's own palette.
  - **Start with MTS, not MTA.** MTS's is the tightest wording in the project -
    its trademarks "may not be used in association with GTFS Data", a flat
    prohibition rather than an application process - while MTA's merely needs a
    free application. The first agency found is not the strictest.
  - **Two halves, and only one is cheap.** Colours are a free choice: each
    city's values live in one dict, and the project has already departed from an
    official palette twice on its own initiative (San Francisco throughout,
    Staten Island Railway for contrast). **Line names are not** - a standing
    invariant requires every drawn line to carry its real public name on the map
    and in the legend, so an answer covering names as well as colours is a
    materially harder change than a palette swap. Know that before asking.
  - Nothing in the project reproduces a logo, wordmark or route-bullet artwork,
    which is the part every one of these clauses most clearly covers.
- [ ] **Settle the three "what does silence mean?" licence questions** -
  still open with the publishers, but **no longer a deploy blocker as of
  2026-09-21.** The owner's decision was to disclose the gap on the site
  rather than wait on third parties: `components._UNSETTLED_TERMS` names
  Miami-Dade and Philadelphia in the footer of every page, says plainly
  that nothing found in either forbids what is displayed, and commits to
  removing a city **without waiting to be asked** if its publisher states
  a position that does not permit this use. That is a BROADER trigger than
  the standing commitment, which fires on a publisher asking, and the same
  wording is now in `docs/data_sources.md` and `docs/excluded_categories.md`
  so all three agree. What remains is the underlying enquiry:
  - [ ] Ask Miami-Dade County directly - it is the only one of the three
    with **no document to read**, so this cannot be resolved by reading.
  - [ ] SEPTA: whether line names and official colours count as trademarks
    being "used", and whether a portfolio site is "commercial or
    profit-making". Overlaps the branding decision, which the owner settled
    on 2026-09-21 by keeping both and stating non-affiliation.
  - [ ] The City of Philadelphia License's rights reservation.
  - **Miami-Dade is the weakest paperwork in the project and should go first.**
    Its business registry and boundary layer carry an `licenseInfo` that is
    purely an accuracy disclaimer, and its GTFS ships **no `feed_info.txt` at
    all** with no locatable developer terms. It is also the only one of the
    three where **no agency document exists to read**, so settling it likely
    means asking the County rather than reading anything - which makes it the
    longest lead time, not the smallest job.
  - **SEPTA's trademark clause** - whether line names and official colours
    count as trademarks being "used", and whether a portfolio site is
    "commercial or profit-making". Overlaps the branding item above.
  - **The "City of Philadelphia License"** reserves all database rights while
    granting nothing explicitly and requiring no notice. Same shape as the NYC
    question with the opposite paperwork: NYC is *forbidden* from imposing a
    licence, Philadelphia has imposed one that says only "we keep our rights".
  - **THAT CLAIM WAS TESTED ON 2026-09-21 AND IS NO LONGER TRUE OF ALL
    THREE.** It read: "nothing found in any of the three forbids what this
    project does ... questions about the absence of permission, not about a
    prohibition". Reading the documents settled two of the three and made the
    third worse than silence:
    - **SEPTA: RESOLVED, and it was never really a silence question.** Its
      licence expressly grants "a non-exclusive, non-assignable,
      non-transferable, limited and revocable right to **use, reproduce and
      redistribute** the datasets". The trademark sentence carves out
      "SEPTA's trademarks and copyrighted materials", not the data - and
      SEPTA's own Trademark Notice claims exactly one thing: "**The SEPTA Logo**
      is a registered trademark". Line names and route colours are not claimed
      anywhere in it, and this project reproduces no logo. The
      "informational and non-commercial purposes only" wording sits in the
      Copyright Notice's *Web Contents and Materials* section, governing
      documents and graphics from septa.org - the same site-footer-versus-
      dataset distinction NYC already taught. Nothing to ask anyone.
    - **Miami-Dade: RESOLVED by reading, not by asking**, which corrects this
      file's claim that "no agency document exists to read". One does:
      `opendata.miamidade.gov/pages/terms-of-use`, the Open Data Hub's own
      designated Terms of Use. Its entire substance is the accuracy
      disclaimer. Three documents now read - the dataset `licenseInfo`, that
      Terms of Use page, and the county-wide "Liability Disclaimer and User
      Agreement" - and **not one of them says anything about reuse,
      redistribution, modification or attribution.** That is a definitive
      absence of restriction from the County's own authoritative pages, which
      is a stronger position than an unexamined gap.
    - **Philadelphia: NOT resolved, and sharper than recorded.** See below.
  - [x] SEPTA - settled 2026-09-21, no action needed.
  - [x] Miami-Dade - settled 2026-09-21 by reading the County's own Terms of
    Use. No enquiry to the County is needed after all.
  - [ ] **Philadelphia - the one real question, and it is a PROHIBITION rather
    than a silence.** The dataset page says "Browsing City data on this site
    constitutes acceptance of the license, **the City's terms of use** and
    your agreement to be bound by them", which incorporates
    `phila.gov/terms-of-use` by reference. Those terms grant permission only
    "to residents and citizens of the City of Philadelphia to copy
    electronically and to print single pages from the Website ... exactly as
    presented ... without any addition or modification", and then state:
    "**Distribution or republication in any other form or for any other
    purpose, including any commercial purpose or use, and any modification
    whatsoever, are strictly prohibited without the prior written permission
    of the City.**" A separate sentence adds "Commercial use is prohibited
    without the prior written permission of the City."
    Read literally and applied to the datasets, that does not permit this
    project's Philadelphia map, which filters and redraws what it publishes.
    Read as what it appears to be - terms drafted for web pages ("print single
    pages", "exactly as presented on the Website"), sitting beside a
    dataset-specific licence that contains no such prohibition, under an Open
    Data Program established by executive order in 2012 whose purpose is
    public reuse, and beside a City boundary dataset marked "Usage: Public
    use; Free" - it does. **This project has NOT resolved it in its own
    favour.** **DECIDED 2026-09-21: ask for written permission, and keep the
    map live under a reasoned position while that is outstanding** - the
    dataset licence governs, the Terms of Use are web-page terms, and the
    footer discloses the question either way. See `DECISIONS.md` for the
    position and for what makes it a position rather than a conclusion.
    - [x] **Request SENT 2026-09-21** by the owner, to **`maps@phila.gov`**
      (the City's own Open Data Program contact) copying
      **`LIGISTEAM@phila.gov`** (the Business Licenses custodian). Text kept at
      `docs/licenses/phila-permission-request.md`. An earlier draft addressed
      the custodian alone - the right address for the wrong desk, since a
      dataset maintainer cannot speak to what the City's terms cover.
    - [ ] **Follow up on 2026-09-28** (one week), at the owner's request. No
      reply as of 2026-09-21. If still silent: wait, chase once, or ring the Open
      Data Program. **Silence is not consent** - the interim position holds on
      the reasoned reading and the disclosure, not on the absence of an
      objection, and it does not strengthen with time. Sending it is the owner's to do. **Nothing in this project may
      claim a request is outstanding until it has actually been sent**, and
      silence must never harden into a claim that permission was given.
    - [ ] On a reply, follow the branch already written into that file: on
      permission the footer clause loses its only live subject and comes out
      entirely; on refusal Philadelphia comes off the site, and the remaining
      eastern cities' macro-map label offsets need re-checking at 854 and
      1200 px, because removing a marker moves `fit_view`'s bounds.
- [x] **Repo visibility - DECIDED 2026-09-21: it stays PUBLIC**, accepting a
  real but unlikely residual. Nothing found in any licence forbids what the
  project displays, the browsable code is much of a portfolio's value, and
  the standing commitment (a removal request is honoured, not argued) is
  the answer if a revocation ever comes. The reasoning against, kept
  because it is still true:
  Raised 2026-09-21 on survivability grounds, not compliance alone: four
  transit licences (WMATA §9, LA Metro, SEPTA, MassDOT) are revocable without
  notice and carry removal obligations, and **a public repo cannot be
  un-published** - forks and history survive deletion, so a revocation could
  not be complied with in good faith. Private keeps the deployed map as the
  only distribution surface, which is the "within your Application" scope each
  licence actually grants. **Verified it does not block deployment:** Streamlit
  Community Cloud supports private repos on the free tier, though it needs the
  broader `repo` OAuth scope plus a deploy key, and the one-private-app limit
  should be checked against "app from a private repo" specifically, since that
  likely means restricted *viewers* rather than a private source. **No middle
  path** - `outputs/` must stay committed, because the deployed app never runs
  the pipeline. Cost: the code stops being browsable, which matters for a
  portfolio piece. Interacts with the `outputs/`-in-git ceiling in
  `docs/scaling_thresholds.md`, since Git LFS quotas apply either way.
- [x] **Tile provider - DECIDED 2026-09-21: change nothing, and the research
  reversed the original recommendation.** Both policies were read rather
  than assumed:
  - **OSM raster** (the nine city maps) is keyless, has no stated volume
    cap, and explicitly permits "normal interactive viewing by a human".
    Its requirements are attribution (already in every map corner), a valid
    User-Agent and Referer - and the policy itself notes "modern browsers,
    with default settings, already satisfy these technical requirements".
    It forbids prefetch, bulk download and offline use, none of which this
    project does. Best-effort, no SLA, may be blocked without notice.
  - **Carto** (the macro map only) is the one with a wall: free to a fair
    use limit of **5 million tile requests a month**, and "all you need is
    an API key" - so a key is now expected, with non-commercial projects
    "usually just get a higher limit" and commercial use needing an
    Enterprise licence.
  So moving the city maps onto Carto - the earlier recommendation - would
  have moved nine maps from the keyless, quota-free service onto the metered
  one. Reversed. **Residual risk, accepted:** the macro map uses Carto's
  keyless CDN, which that policy no longer documents. If it is withdrawn the
  macro basemap goes blank while the markers, name pills, clicks and the
  text-link list all keep working. `pydeck` 0.9.3 does accept
  `api_keys={"carto": ...}` (env `CARTO_API_KEY`), so requesting the free
  key is a one-minute owner task if that degradation is ever unwelcome -
  it needs the owner's own account, so it is not something this project can
  do on their behalf.
  - [ ] Optional: request a free Carto API key and set `CARTO_API_KEY` in
    the Streamlit Cloud secrets.
- [x] **Streamlit Cloud main-file path - SETTLED 2026-09-21.** The entry
  point was `app/Overview_&_Introduction.py`; an `&` in a path that Cloud
  fixes permanently at app creation is a live hazard in URLs and shells, so
  it is now **`app/Overview.py`**. Renamed with `git mv` and every reference
  updated - `components.OVERVIEW_PAGE`, all eleven page docstrings,
  `pipeline/theme.py`, `scripts/scaffold_city.py` (it generates new pages,
  so it had to follow), `.claude/launch.json`, the deploy-verify agent,
  CLAUDE.md, README and project_context. `DECISIONS.md` and
  `docs/passover_opus5.md` keep the old name: they are history.
- [x] **Project name - DECIDED 2026-09-21: "Storefronts Near Transit".**
  The owner kept `expanded-heatmap` as the repository and directory name and
  took the new name as the site title only, so nothing about the checkout,
  the remote or any path changes. It lives in `components.SITE_NAME` and
  feeds the Overview title and every page's browser tab.
- [x] `README.md` - revised 2026-09-21: the new name, all nine cities, the
  snapshot-not-a-census caveat, the non-affiliation statement, and D.C.'s
  API key and ten-day feed window.
  - [x] **Code licence: MIT, added 2026-09-21** (`LICENSE`), with an
    explicit scope section stating what it does NOT cover. A bare MIT file
    at the repo root would have purported to license the 19 MB of
    third-party-derived content in `outputs/` - redrawn GTFS geometry and
    register-derived business records - which this project cannot
    sublicense: WMATA prohibits third-party redistribution and LA Metro
    forbids modifying its data. The carve-out points at
    `docs/data_sources.md` for terms and `docs/excluded_categories.md` for
    the modifications half that some of those terms require a re-publisher
    to state. The copyright line reads `dacekroberts`, the identity this
    project commits under - change it if a legal name is wanted.
  - [x] **Deployed URL - LIVE 2026-09-21:**
    <https://expanded-heatmap-daceroberts.streamlit.app>, in `README.md`.
    Note the subdomain carries the REPOSITORY name while the site is titled
    "Storefronts Near Transit". Unlike the main-file path, a Streamlit Cloud
    app's URL CAN be changed later from the app's settings, so this is
    reversible if the mismatch ever grates.

## Data quality follow-ups

- [x] **Rings start switched off on every city (2026-09-21, owner's call)** for a
  cleaner first view. `rings_shown` defaults to False in `map_common.py`; New
  York's and Miami's explicit overrides are removed as redundant. The counts
  are unaffected - businesses are assigned to their nearest station whatever
  the rings show - and the rings remain in each map's layer control.

- [x] Los Angeles map size: **3.5 MB** after the 2026-09-21 exclusions (was
  5.8), against 2.4 MB for San Francisco. Largely resolved; revisit only if a
  deploy shows it is still slow.
- [ ] Los Angeles: ~9% of registry rows have no NAICS code; consider whether
  the caveat needs to be visible on the city page.

- [ ] San Diego: exact `address_city == "SAN DIEGO"` undercounts
  neighbourhoods recorded under their own name (La Jolla foremost); decide
  whether to include them.
- [ ] San Francisco: only ~37% of rows carry a NAICS code; consider whether
  the caveat needs to be visible on the city page.
- [x] **Surface `docs/excluded_categories.md` AND `docs/data_sources.md` in
  the app - DONE 2026-09-21**, as `pages/10_About_the_Data.py` and
  `pages/11_What_Is_Excluded.py`, each rendering its document as committed
  rather than a hand-maintained web copy that would drift. Both are linked
  from the footer on every page, which is also where the required notices
  now render. Original item:
- [x] (reference) Surface both docs, together (a page each, or one "About the data" section, linked from
  every city page). Deliberately paired and deferred as one job (2026-09-21):
  both are external necessities for a live site rather than development work,
  both are already written to be published as-is, and surfacing the exclusions
  without the provenance would be half an answer. **Blocks the public deploy:**
  the legends were left broad, so "Retail - NAICS Code: 44/45" overstates what
  the maps contain until the exclusions page is reachable from them.
- [ ] **Carry into the mandatory `full` `deploy-verify` run before deploy:** the
  three fixes made after the 2026-09-21 scoped `map-chrome` run (legend
  breakpoint dead on a wide load, container ~15px short, fit bounds excluding
  label anchors) are verified by screenshot on four cities but not by an agent
  pass. Confirmed 2026-09-21 to batch them into that run rather than spend
  another scoped one - which is the batching the scope policy encourages.
- [x] **Phone-width city pages** - largely fixed 2026-09-21. The map keeps its
  fixed 1000px layout for initialisation (which is what dodges the Leaflet.heat
  `IndexSizeError`) and is resized to the frame immediately afterwards, then
  re-fitted to the station bounds. At 375px: New York went from 1 of 11 line
  labels visible to **9 of 11 fully visible, 0 off-screen**, Chicago from 0 of 7
  to 6 of 7, and the horizontal scroll inside the iframe is gone. Desktop is
  unchanged (11 of 11, original view). What remains:
  - [ ] **Label placement is still computed for a 1000x650 canvas**, so at phone
    width labels can crowd each other and the cluster badges, and one or two
    clip at an edge (New York: "Lexington Av (4/5/6)" right, "Staten Island
    Railway" left). Laying them out correctly for a phone needs a **second
    render at phone dimensions** - a per-city phone HTML plus viewport
    selection in the page. That roughly doubles `outputs/` and render time, so
    it is worth doing only if phone traffic matters. Not started. **Blocks the public deploy:** the legends were deliberately left
  broad (2026-09-21), so "Retail - NAICS Code: 44/45" overstates what the map
  now contains until this page is reachable from it.
- [x] Catch-all and non-storefront classifications: swept 2026-09-21 and
  resolved. Excluded everywhere: NAICS `454` (nonstore retailers) and `81293`
  (parking). Excluded per city: 812990 in Los Angeles and in San Francisco (for
  different reasons - see `DECISIONS.md`). Kept: 459999 (~70% plausible
  storefronts). San Diego left in, with its measurement limit recorded. All
  listed in `docs/excluded_categories.md`. Remaining open questions:
  - A residual ~850 rows in Los Angeles and ~201 in San Francisco carry a
    person-like name at a residential address, spread across ordinary storefront
    categories. Probably sole traders named after themselves (legitimate), but
    unverified row by row.
  - San Diego has no usable residence signal in its address text; its
    `ownership_type` (1,298 SOLE of 3,117 mapped) is the better proxy if this is
    revisited.
- [ ] **Run `python scripts/check_personal_exposure.py` before publishing any
  city**, and after any change to a city's step 2 or taxonomy. It is a
  pre-publish gate in `CLAUDE.md` and `add-city` Step 7.

## Later / maybe

- [ ] Macro map at scale: with ~10+ cities, consider grouping nearby cities,
  and showing each city's mapped extent or a one-line summary in the tooltip.
  **Both halves were done on 2026-09-21.** The labels got per-city pixel
  `label_offset`s in `cities.py` (11 collisions to 0), and the markers were
  shrunk from radius 6 with a 2 px ring to radius 4 with a 1 px ring - outer
  diameter 16 px to 10 px - which separates New York/Boston and New York/D.C.
  outright and cuts the worst overlap, New York/Philadelphia, from 10 px to
  4 px. Radius 3 was tried and rejected as too faint.
  **What cannot be fixed, with the arithmetic so nobody retries it:** at the
  fitted zoom 1 px is about 21.7 km at New York's latitude, so displacing New
  York enough to clear Philadelphia would take **217 km** and put its dot west
  of Pittsburgh. The separations are also width-independent, because `fit_view`
  pins the zoom to a 320 px reference and spends extra width as margin. The
  residual touching is cosmetic only: the name pills are pickable, so clicking
  never depends on hitting a dot.
  - **Known issue, accepted rather than fixed:** scrolling the page with the
    cursor over the macro map zooms the MAP instead of scrolling the page, and
    that view then persists across reloads via the widget key. The fix is to
    lock the controller, which the owner declined on 2026-09-21 because
    non-US cities would then need continent-specific maps and extra pages.
  - Its label offsets are in PIXELS and the map zooms, so any new city in the
    eastern cluster needs its offset checked at 854 and 1200 px AND at a
    zoomed-in level - see `cities.py`'s docstring for the measurements.
  **`docs/scaling_thresholds.md` holds the full list of what breaks at what
  city count** (written 2026-09-21 at 7 cities): this macro map at ~10, the
  committed `outputs/` in git at ~20 — the real ceiling — and hosting at 40+.
  Two entries there are already settled: `drift_check.py` went incremental on
  2026-09-21, and page-number ordering was verified *not* to be a problem
  (Streamlit sorts the prefix numerically), so neither needs re-raising.

- [x] **RE-RANKED on storefront counts, 2026-09-21** (was: do this before
  choosing the next city).
  `scripts/rank_canada_storefront_density.py` is committed so it is
  reproducible. Result, storefronts in the 0.6 mi ring per in-city station:
  **Vancouver 206, Montreal 151, Surrey 135, Edmonton 76, Calgary 75,
  Toronto 41** - against D.C. ~173 and Boston ~39. **TORONTO'S 41 WAS
  CORRECTED TWICE on 2026-09-21, to 81 and then to 86**, after its 234
  "stations" turned out to be PLATFORMS (`parent_station` never populated).
  **The second correction came from `scripts/brief_check.py`**: the first pass
  wrote a collapse pattern for the subway's hyphenated
  `X Station - Southbound Platform` and missed that the LRT omits the hyphen
  (`X Station Eastbound Platform`), leaving all 86 LRT platforms uncollapsed,
  and missed three stations appearing twice via a `- Subway` suffix. The real
  figures are **148 platforms / 72 stations** on the subway and **234 / 111**
  with the two LRT lines, which agree with the operator's own counts (38 + 31 +
  5 less 3 interchanges = 71) where 77 and 118 agree with nothing. So the
  corrected order is **Vancouver 206, Montreal 151, Calgary 137, Surrey 135,
  Toronto 86, Edmonton 79**. **Toronto's open question 1 is also closed**
  (2026-09-21): the unmatched addresses are NOT materially biased - storefront
  coverage is **92.8%**, not the 71.4% its brief quoted, because that figure
  counted person-licences with no premises address to match; the ward spread is
  1.3x and there is no temporal bias. Its category count is **92, not the 72
  recorded here**. It does NOT change which city to build next: Toronto is a
  two-bucket city with no general-retail source - **measured, Retail is 2.3% of
  its storefronts and consists of the single category `SECOND HAND SHOP`** -
  which is a coverage problem no denominator fixes. See `docs/build_briefs/toronto.md`. Published inflation ran
  1.0x-4.2x and was NOT uniform, so **Montreal and Surrey swap** and
  Edmonton/Calgary become a tie. Toronto stays last. **Next build: MONTREAL** -
  densest remaining, cheapest (SCIAN is NAICS, so no taxonomy module at all),
  and the best-matched source in the project at 69.4% storefront. Five further
  corrections to the profile are in `DECISIONS.md`, including that Edmonton has
  a licence-level home flag and that two of three catalogue feeds are stale.
  The original, non-comparable figures are left in place below rather than
  edited, since `docs/` belongs to the staging role.

- [x] Vancouver + Surrey, built 2026-09-21 at REGIONAL scope. 11,724
  storefronts on 24 stations (20 Vancouver, 4 Surrey), two registries
  dispatched on a `source` column. The residence filter below was built and
  **drops nothing**, which is a measured result rather than a shortcut - see
  `DECISIONS.md`. Three required notices went onto the deploy gate, the first
  city to add more than one.

- [~] Non-US cities. **Canada is screened and ready to build - see
  `docs/canada_step0_endpoints.md` and the 2026-09-21 `DECISIONS.md` entry.**
  Six viable cities, Step 0 complete on all three legs, licences and privacy
  documented in `docs/licenses/`. Ranked by sites per in-city station:
  **Vancouver 861** (densest measured anywhere in this project), **Surrey 549**
  (a regional pair with Vancouver - it has no rail of its own), **Montreal
  252**, **Edmonton 153**, **Calgary 103**, **Toronto 41** (a two-bucket city,
  Boston's shape, weakest despite being largest). Decided already: Montreal at
  agglomeration scope; TransLink needs no prior contact. Build-time work that
  remains, per city rather than in general:
  - **Taxonomy modules.** Calgary 173 real categories, Surrey 210, Vancouver
    93, Edmonton 67, Toronto 72 - and **three of the six store several
    categories per row**, with a different delimiter each (Calgary `,\n`,
    Edmonton `;`, Surrey `\n`). Splitting is not optional and a multi-licence
    premises needs a dispatch rule, as Boston's `FT+RF` did.
  - **Montreal:** decide `SCIAN` (NAICS, 99.6%) versus the 10-value `USAGE1`.
    Keying off SCIAN may need **no new taxonomy module at all**.
  - **Vancouver: DONE, and the filter turned out to be empty.** The two-hop
    join works (99.9% point-in-parcel, 99.7% to a zoning class), but the
    conjunction it was built for - residential zoning AND a substituted
    personal name - leaves **1 row**, and that row is a false positive (a real
    corner grocery). The predicted ~232/0.78% was measured across all mappable
    rows rather than the storefront set. Zoning alone is NOT usable: the 146
    residentially-zoned storefronts are Vancouver's legal non-conforming corner
    shops and neighbourhood restaurants. Also: Vancouver DOES have a structural
    name signal, contrary to the brief - the registry parenthesises a sole
    proprietor's own name.
  - **Toronto:** geocode against the City's own 525,440-point address
    repository (71.4% on exact match, no normalisation) rather than any
    external geocoder.
  Beyond Canada, the EU/UK remain unscreened - NACE, and a national CRS such
  as EPSG:27700 for the UK.
- [x] ~~**Korea: register for a `data.go.kr` API key** (owner action).~~
  **CANCELLED 2026-09-22 - do not attempt this. It is not possible, and it is
  not needed.**
  - **Not possible:** every `data.go.kr` member type requires a Korean resident
    ID (내국인) or a Korean business number, and Seoul's 외국인회원 route is for
    foreigners *residing in* Korea. This is a **residency** wall, not a
    registration one, so the WMATA precedent does not apply. The old item read
    "Free" and "This is WMATA's gate, already cleared once" - both wrong. A
    **401 says the endpoint wants a key; it says nothing about who is allowed to
    hold one.**
  - **Not needed:** `data.seoul.go.kr` serves the same shape of data with **no
    account**, via the SHEET CSV export (`ssUserId=SAMPLE_VIEW` is the
    logged-out identity the page itself sends). **Eight datasets, 197,276 active
    premises, EPSG:5174 coordinates, `영업상태명` for active filtering, cp949,
    refreshed daily.** `infId`s and per-file measurements are in
    `docs/data_sources.md`; the download mechanism is in
    `docs/global_country_shortlist.md`.
  - **Licence differs from what this item claimed.** Not `제한 없음` but
    **공공누리 제1유형 (KOGL Type 1)**: attribution required - including a
    **hyperlink** where one is possible online - no implied endorsement, and a
    moral-rights clause meaning the per-station counts must be described as this
    project's derivation. One notice covers all of Seoul.
  - **Scope shrank: Seoul only, not six cities.** Korea licenses at the 자치구,
    so registers are published per district; Seoul aggregates and no other
    Korean city does. Busan has 4 of 16 districts and its national-portal
    download ids are stale behind a CAPTCHA rate limiter; Daegu's route works
    but 중구 - the downtown where all three metro lines converge - publishes no
    premises register at all.
  - [x] ~~**Korea has no line geometry yet.**~~ Resolved: dataset `15013203`
    (전국도시철도노선정보표준데이터) is the line standard dataset, alongside
    `15013205` for stations.
  - [ ] **Still open, and build work rather than screening:** a **partial**
    geocoding fallback for `OA-16094` 일반음식점 only - it is the one file below
    97% on coordinates, at **90.7%**, so ~11,000 active restaurants have a road
    address (99.2%) but no point. And a **Korean-aware pass in
    `scripts/check_personal_exposure.py`**: no file carries a proprietor-name
    column, but salon trade names routinely contain a personal name (`김은미장`)
    and ~30% of `사업장명` are a bare 2-4 hangul token.

- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
