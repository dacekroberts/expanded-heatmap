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

- [ ] **Next city** - pick from the list below. Start with the `add-city`
  Step 0, then `scripts/scaffold_city.py` (the `scaffold-city` skill). That
  build is also the first real test of the scaffold: record in `DECISIONS.md`
  whether it saved effort (estimated at about 10%) and fix any template that
  needed rewriting.

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
  - Worth stating plainly: **nothing found in any of the three forbids what
    this project does.** These are questions about the absence of permission,
    not about a prohibition, which is why they gate a public deploy rather than
    the builds.
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
  **The label half of this was done on 2026-09-21** - per-city pixel
  `label_offset`s in `cities.py`, 11 collisions to 0 - but the MARKERS still
  overlap and no label placement can fix that: New York/Philadelphia dots sit
  6.0 px apart and Philadelphia/Washington D.C. 9.0 px, against a 6 px radius,
  and because `fit_view` pins the zoom to a 320 px reference those separations
  are identical at 340 px and 1200 px. Extra screen width becomes margin, not
  separation. Clicking is no longer blocked by it (the name pills are pickable
  now), so what remains is cosmetic.
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

- [ ] Non-US cities (NACE for the EU, national CRS such as EPSG:27700 for the
  UK) - one taxonomy module and a per-city CRS each.
- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
