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
    exists: `Overview_&_Introduction.py` still has literal `white` and
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
- [ ] Boston - **Step 0 PASSED 2026-09-21. Viable, and the thinnest and
  narrowest candidate in the project; whether to build it is an open decision.**
  Full findings and every endpoint are in `docs/data_sources.md`, "Boston -
  Step 0 findings". The shape: a **two-bucket** city like Philadelphia, with
  Food service 2,237 premises, Retail 385 unambiguous plus 306 overlapping
  package stores and 43 cannabis, and **Personal services absent** rather than
  thin. That is ~2,740 sites over 71 in-city stations - roughly 2.3x thinner
  per station than Philadelphia - and it is really *food* density, because
  Boston licenses food and alcohol and no other trade. If it is built:
  - Use the **902,651-row Food Establishment Inspections** history, filtered to
    `licstatus='Active'` and collapsed to one row per `property_id`. Do **not**
    use the official "Active Food Establishment Licenses" extract: it silently
    drops the `RF` Retail Food category, which is the entire Retail bucket.
  - `businessname` is the trade-name column, not `dbaname` - `dbaname` is blank
    on 99.0% of rows, the reverse of every other city. A copied step 2 will
    quietly produce almost nothing.
  - Dedup **across** sources on address: package stores hold both an `RF`
    licence and a `Retail All Alc.` licence at the same premises.
  - Decide the `FT+RF` premises (31 of them, e.g. "Hyde Park Market",
    "Shaw's Supermarkets No. 1208") - takeaway counter inside a grocer. Sample
    and record the verdict, as Chicago's catch-alls were.
  - `gpsx`/`gpsy` on the Licensing Board sets are **EPSG:2249** (Mass. State
    Plane, US survey feet), verified by transformation, not assumed. Boston's
    own projected CRS is **EPSG:32619** (UTM 19N), derived from longitude.
  - Green Line = 4 street-running branches on a shared central subway, San
    Francisco's exact shape, so `docs/sub_transit_line_filters.md` applies;
    Red/Orange/Blue are well spaced and need no thinning.
  - Get a **MassGIS multi-town boundary layer** as well as Boston's own outline,
    so the 54 out-of-city stations can be named by municipality and the four
    borderline ones (Boston College at 6.7 m is really in Boston) resolved.
  - Add MassDOT's acknowledgement to the required notices (already listed).
  - `Business Inventory` is recorded as available and **deliberately unused**;
    revisit only if the city extends the survey city-wide.
- [ ] **Washington D.C. - the strongest remaining candidate. Step 0 mostly
  done 2026-09-21;** full findings in `docs/city_shortlist.md`. 76,107 active
  licences and the first non-NAICS city with **all three buckets** from one
  registry (Food Services 4,901, Beauty and Grooming 486, ~1,550 real retail).
  What the probe settled, and what is left:
  - **Exclude `BUSINESSACTIVITY = 'General Business'` (14,770).** Sampled: it
    is the office/professional catch-all - Nossaman LLP, Gannett Fleming
    Engineers, Voith & Mactavish Architects, consultancies, tech firms - and it
    is 14,729 of the 16,282 rows in "General Sales and Services". Same role as
    LA's NAICS 812990. Record the sample in `DECISIONS.md` as LA's was.
  - **Drop the residential rentals: 49% of active rows.** One Family Rental
    25,587, Apartment 6,106, Two Family Rental 2,560, Short Term Rental 2,197,
    Vacation Rental 803, Rooming/Boarding House 65. The Philadelphia pattern.
  - **Ignore `LATITUDE`/`LONGITUDE` entirely** - they are literally `39` and
    `-77` on every row, 0 of 76,107 inside DC. Use `X_COORDINATE`/
    `Y_COORDINATE`, which are **EPSG:26985**, verified by transforming 312
    Pennsylvania Ave SE to (38.88715, -77.00153). Present on 77% of storefront
    rows; `MAR_ID` (Master Address Repository) should recover the rest without
    the Census geocoder.
  - **Trade name is missing on 49% of storefront rows** (11,079 of 21,669 have
    `ENTITYTRADENAME`). That is the Los Angeles trap at half LA's severity, so
    apply LA's answer, and never publish `BUSINESSOWNERFIRSTNAME`/
    `BUSINESSOWNERLASTNAME`/`AGENT*`, which are populated on ~34k rows.
  - Use `PREMISEINDC = 'Yes'` (61,329) for in-city scope, **not** `WARD` -
    `WARD` is null on 16,806 rows and mixes "Ward 2" with "2".
  - `SSL` (Square/Suffix/Lot) on 45,476 rows is the parcel join for the
    residence check, and `ENTITYTYPE = 'Sole Proprietorship'` is the
    sole-trader signal, as in San Diego.
  - **WMATA GTFS needs a free API key** - `api.wmata.com/gtfs/rail-gtfs-static.zip`
    returns **401** unauthenticated, the only feed in the project that does.
    A keyless Mobility Database mirror exists (`urls.latest` for mdb source
    1847, a GCS object needing `?alt=media`). Decide which, and **read
    `https://developer.wmata.com/license`** - unread, and the transit feeds
    have been the loosest end of every licence review.
  - Measure the in-city station share before committing: Metrorail is 98
    stations but reaches far into Virginia and Maryland, so expect an
    LA-scale boundary cut.
- [ ] **Miami - screened 2026-09-21, needs a real Step 0.** Miami-Dade "Local
  Business Tax" ArcGIS layer: 194,099 rows, `ACCSTATUS`, NAICS via
  `BUSNAICSCD` (so no new taxonomy module), `CLASSDESC`/`CATGRYNAME`/`OCCDESC`,
  real `LAT`/`LON`, and `FOLIO` parcel IDs for the residence check. Filter
  county-wide data to the city with `MUNBUSLOC = '01 - MIAMI'`. Left to do: the
  category distribution, the in-city count, the licence (its `licenseInfo` is
  an as-is disclaimer), and a privacy pass - `OWNERNAME` is present and some
  `BUSNAME` values are people ("LEON RAUL APRN").
- [ ] **New Orleans - screened 2026-09-21, needs a real Step 0.** `iqay-p646`
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
- [ ] **Find San Francisco's boundary-layer endpoint.** It is recorded nowhere,
  and the file is gitignored, so that city cannot currently be rebuilt from
  scratch (surfaced while writing `docs/data_sources.md`).

## Before deploying

- [ ] **Tile provider decision** - OpenStreetMap's usage policy is a risk
  for a live public map. The per-city maps use OSM raster tiles; the macro
  map uses Carto's public vector basemap. Decide both together.
- [ ] **Streamlit Cloud main-file path** - fixed at app creation and not
  editable afterward, so settle the entry-point filename first.
- [ ] **Project name** - "Expanded Heatmap" is a placeholder.
- [ ] `README.md`: first draft written; revise before deploying (add the
  deployed URL, a licence, and the final project name).

## Data quality follow-ups

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
- [ ] **Surface `docs/excluded_categories.md` AND `docs/data_sources.md` in the
  app**, together (a page each, or one "About the data" section, linked from
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

- [ ] Macro map at scale: with ~10+ cities, consider grouping nearby cities
  (markers already touch at phone width: Los Angeles and San Diego), and showing each city's mapped
  extent or a one-line summary in the tooltip.

- [ ] Non-US cities (NACE for the EU, national CRS such as EPSG:27700 for the
  UK) - one taxonomy module and a per-city CRS each.
- [ ] Ridership (out of scope; revisit only if asked).
- [ ] Adopt `safe-rename` (or fold its checklist into `add-city`) once a
  README, deployment or devcontainer exists to keep in sync.
