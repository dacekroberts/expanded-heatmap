# DECISIONS drafts - tram kit (`worktree-tram-kit`, then `tram-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-09-30 - Tucson built on tram-build: Sun Link and the City's BUSLIC layer

- **Tucson built on Houston's rules and `osm_tram.py`.** It has 21
  stations, 5,243 storefronts, and 340 of them (6.5%) in a ring. The page
  says "about one storefront in fifteen".
- **Sun Link.** OSM relations 3920972 and 12426661, ref "Sun Link". Their 23
  stop positions collapse to the brief's 21 stations; downtown runs on
  one-way couplets, so each direction's stops keep their own names. All are
  inside the City as TIGER draws it (place 0477000, 629.4 km²).
  - **Median gap 265 m**, exactly the brief's, so the rings are halved, and
    step 1 gates the median at 200-340 m. No gate 3.
  - **Colour `#e65100`, deep orange, 59.7 against Food service.** Teal
    `#00838f` was tried first and scored 42.3 against Personal services.
  - The page states the frequency: 10 minutes on weekdays 07-18, and 20
    otherwise.
- **Scope: TIGER, not the brief's OSM relation 253824.** This is Houston's
  layer, and it costs no Overpass query while both mirrors were 504ing.
  Every stop is inside either way.
- **BUSLIC (layer 3), step by step.**
  - The server filter is `LIC_STATUS = 'Active' AND HOME_OCCUPATION = 'F'`,
    asserted again in step 2. That is 24,191 licences; the 10,573 active
    home occupations are never downloaded.
  - **7,120 storefront licences** by NAICS: Retail 4,049, Food 1,779,
    Personal 1,292. The brief screened 4,056, 2,011 and 1,245.
    - 539 (7.6%) have no point. The page says "about one licence in
      thirteen".
    - 23 lie outside the city.
    - 19 have APT in the `APT` field and are left off as homes. The field is
      otherwise shop suites ("STE 101"), so only APT, APARTMENT and TRLR
      count.
  - **6,539 licences collapse to 5,243 premises.** A business holds a
    business licence, a tobacco licence and a liquor licence at one
    address, so rows collapse on name and address.
- **Names (call 15).** The address is shown for 748 premises:
  - **692 with a personal OWN_TYPE**: Sole Proprietorship 525, Individual
    151, Married 16;
  - **45 whose account name is only a person's**, Kansas City's rule. All
    642 distinct shown names that `residence.looks_personal` reads as a
    person's were read by eye. The 45 are listed in `config.PERSON_NAMED`,
    and step 2 stops if one disappears. The rest are shop names ("RATHER
    KEEN", "BLIND PIG") or brands ("SONNY ANGEL").
  - **11 with no account name.**

  2,040 storefronts have no OWN_TYPE at all. Their account names are trade
  names apart from those in the list.
- **Privacy verdict: publishable.** 340 pins:
  - 0 contact details;
  - 0 surname-first names;
  - 0 person-like names at a residential unit;
  - 69 person-like by the heuristic, all shop names from the list read by
    eye (22% of them at an STE suite).
- **Licence: SILENT, read as permitted by the owner.** Notice 70, "Business
  licence data: City of Tucson.", is the owner's wording. The page quotes the
  layer's own words: the list "should not be considered a complete listing".
  The OSM rail notice now names Kansas City's and Tucson's streetcars. It had
  missed Kansas City's in the first commit.
- **Macro label: Tucson is 48.6 px, right of the dot at ("start", 11, -5).**
  - **San Diego's label moved from east of its dot to west, over the
    Pacific, at ("end", -11, -2).** East of its dot it covered Tucson's
    marker at the Global and United States zooms. The scan: San Diego
    passes dy -5 to +1, and Tucson -7 to -2.
  - **Tucson is left out of United States West's zoom fit**
    (`REGION_ZOOM_WITHOUT`), as Riga is out of Europe's. Fitted to Tucson,
    the zoom dropped and San Francisco's pill covered Sacramento's marker.
    - **Rejected: moving San Francisco's and Los Angeles's labels west too.**
      It also scores PROBLEMS 0, but San Francisco's pill then clips 26-37%
      off the left edge at 375 px.
    - Left out of the fit, California keeps its zoom, and the centre moves
      about 3° east.
  - **Two front-page changes for deploy-verify at review:** San Diego's
    label, and United States West's centre.
- **Notice numbering.** Notices 69 (Kansas City) and 70 (Tucson) clash with
  France's 69-71, so they are renumbered at landing.

### 2026-09-30 - Kansas City built on tram-build: the KC Streetcar and KCMO's frozen licence register

- **Kansas City built on Houston's rules and `osm_tram.py`.** It has 19
  stations, 3,561 storefronts, and 451 of them (12.7%) in a ring. The page
  says "about one storefront in eight".
- **The streetcar.** OSM relations 7825409 and 7825410, ref 601, operator
  "Kansas City Streetcar Authority". Their 35 stop positions collapse to the
  brief's 19 stations, all inside the City as TIGER draws it (place 2938000,
  824.8 km²). RideKC's GTFS was not fetched (owner).
  - **Median gap 384 m, not the brief's 413 m**, so the rings are halved, and
    step 1 gates the median at 350-480 m.
  - No gate 3: RideKC's count is barred, and the brief's 19 is OSM's own
    count, which step 1 checks.
  - Colour `#b8860b`, Odense's, scoring 74.8 against the nearest pin. OSM
    records none, and no logo is used.
  - The frequency, "about every 10 minutes by day, seven days a week", is
    stated as a fact, as the brief says.
- **Found: the brief misread the register's name columns.** `dba_name` is
  filled on all 15,895 rows and holds the LICENCE HOLDER: "HARRIS GREGORY J"
  for a person, "MANREET INC" for a company. `business_name`, filled on
  5,835 rows, is the trade name ("7 ELEVEN STORE NO 18711C" over MANREET INC).
  - **Decided: call 11 (Houston's sole-owner rule) is read on the holder.**
    Where the holder reads as a person (surname first, letters only, no
    organisation word; it is meant to over-fire), the pin shows the address
    and no name at all, not even the trade name. That is Houston's rule,
    which withholds a person's trade name too. This covers 684 storefronts.
  - **Otherwise the pin shows the trade name, else the holder company.**
    That is 1,385 trade names and 1,466 holder companies. Showing the trade
    name departs from the brief's "show `dba_name`", which assumed
    `dba_name` was the trade name. **Flagged for the owner.**
  - **A company named only as a person shows the address too.** This
    follows Bucharest's precedent ("Caranica Mihai SRL") and Denmark's. All
    587 shown names that `residence.looks_personal` reads as a person's
    were read by eye: 271 trade names and 316 holder companies with the
    legal form stripped. 26 are people ("ALYSSA BULLIS LLC", "NEVA J
    WILLIAMS"), listed in `config.PERSON_NAMED`. The rest are shop names
    ("CROWS COFFEE") or chains named for a founder ("KENDRA SCOTT",
    "JOHNNY WAS"), and are kept as brands. Step 2 stops if a listed name
    disappears. The register is frozen, so the list is measured rather
    than guessed.
- **Privacy verdict: publishable.** 451 pins:
  - 0 contact details;
  - 0 surname-first names;
  - 0 at a residential unit, because the register's addresses carry no unit
    at all, so Houston's apartment test cannot fire;
  - 39 person-like names by the heuristic, all shop names (Akoya Omakase,
    Midtown Tavern, Hotel Indigo);
  - 163 holder-company fallbacks, read by eye in the ring: 169 names, all
    companies once the 26 above were withheld.
- **The register, step by step.** Of the 15,895 rows:
  - 13,917 are licences valid for 2025 or 2026 (owner, call 10). The 1,978
    valid for 2024 had lapsed by the freeze.
  - **1,095 carry only a fee code** ("Misc Rate 129", "Flat Rate 42A"). They
    were dropped, and the page states the count (call 12). The brief's
    1,200 counted all years. No restaurant hides under a fee code: one
    fee-code name of 1,095 reads as food.
  - **615 NAICS 2022 titles map to codes through the Census title file**
    (a new support source with a row; federal, public domain), compared on
    letters and digits. One truncated title, "Freight Transportation
    Arrangemen", maps by unique prefix. Every title maps.
  - 3,612 are in the buckets; 11 points lie outside the city; 40 are
    duplicates by name and address. That leaves 3,561.
  - **NAICS 2022 has no "nonstore" code (454)**, so online sellers are NOT
    left out by code here. The page says a web shop is filed under its
    goods, Odense's caveat, rather than Houston's "online sellers are left
    out". Vending machines (23) and fuel dealers (1) are left out.
- **Found: Food service is thin.** 175 premises in the whole city, 52 in a
  ring; only 26 full-service restaurants citywide. The licence register
  holds few restaurants and bars.
  - **Kept `coverage` "full"**, on Houston's precedent: its personal
    services were 94 of 2,223 in-ring pins and it stayed "All three". KC's
    food is 52 of 451.
  - The page says "It holds few restaurants and bars, about 175 across the
    whole city". **That sentence is outside the template: flagged.**
  - **The owner's call, if it is wanted:** `narrowed` with "Food thin"
    instead, or a city food-permit source (none is in the brief).
- **Page sentences outside the template, flagged:**
  - the register caveat, "a licence is issued to a business at an address
    ...";
  - the web-shop sentence;
  - the thin-food sentence;
  - "and so it does where a company trades under a person's own name".
- **Macro label: Kansas City is 79.3 px, measured with Houston, Odense,
  Daugavpils and Riga reproduced. It sits left of the dot at ("end", -11,
  8).**
  - **Chicago's label moved from below its dot to the left, ("end", -11,
    -2).** Below its dot it covered Kansas City's marker at the Global and
    United States zooms, at all three widths, and no offset of Kansas
    City's own label can fix that. The scan:
    - Chicago passes dy -8 to +5;
    - Kansas City passes dy +2 to +13;
    - PROBLEMS 0.
  - **A front-page change to a published city, for deploy-verify at
    review.**
  - At 375 px in United States East, Kansas City's pill runs 17.3 px (19%)
    off the left edge. It is reported as clipped, not a problem.
- **Licence read (2026-09-30): PERMITTED WITH CONDITIONS, and one OWNER
  DECISION. Kansas City does not land until it is made.**
  - **The grant.** KCMO Code § 2-2134(a) requires portal datasets to be public
    domain with "no restrictions or requirements placed on use".
    `kkhs-93m4` and its parent `pnm4-68wg` declare Public Domain, and that is
    the City's choice, not a portal default.
  - **The disclaimer.** The portal's undated Data Terms of Use prescribe a
    disclaimer for any derivative application. It is Chicago's wording on
    the same portal template, so it is displayed site-wide as **notice 69**,
    verbatim, including the dead host `www.data.kcmo.gov`.
  - **The indemnity.** The same terms claim an open-ended indemnity from
    "any user of the data". RideKC's GTFS was barred partly over one.
    - **Recommended: read the ordinance as controlling and land.** The
      dataset is declared public domain, a City ordinance backs it, and
      the terms page is undated, with no acceptance step.
    - **Or:** ask data@kcmo.org, or drop the city.
  - **Notice numbering.** France also numbered notices 69-71 on its branch,
    so renumber at landing.

### 2026-09-30 - Daugavpils built on tram-build: all five routes, 37 stations

- **Daugavpils built on Riga's layers through `latvia_register.py`.** It
  has 37 stations, 819 storefronts, and 80.1% of them in a ring (the
  screen: 81.5%).
- **All nine OSM relations, refs 1-4, were kept: all five routes are drawn**
  (the owner's overrule of call 28). Ref 3 carries three relations:
  - route 3, Cietoksnis-Stropu ezers, one relation each way;
  - the loop the operator's own linked page calls route 5. OSM tags it 3.

  Their stops are unioned. Route 3 adds Balvu iela and Stropu ciemats.
  Route 3's track lies almost wholly on the loop's (0.07-0.09 km off it), so
  the loop is drawn once, labelled "Trams 3 and 5". The page states each
  route's wait, from the brief: 1 every 10-15 min, 3 and 5 every 20-30, 2
  and 4 about hourly.
- **37 stations, not the brief's 38.** The brief counted "Lokomotīvju demo",
  one direction's misspelling of Lokomotīvju depo on routes 2 and 4, as a
  stop of its own. It is aliased.
- **Stropu ciemats is a stop member of both route-3 relations**, but it is
  tagged only highway=bus_stop and public_transport=platform. It was
  accepted by node through osm_tram's new `accept_members`.
- **There is no operator whitelist.** The relations spell the operator
  "Daugavpils Satiksme AS" and, on route 2, "SIA". Every tram relation in
  the box is one of the nine.
- **Median gap 291 m: the rings are halved.** No gate 3: no operator count
  was read.
- **Businesses.** Food: 98 premises, 94 placed (95.9%) on VZD's address
  register (15,221 existing addresses in the city). Shops and services: 725
  of 956 premise groups, all placed. The screen's 722 predates the
  2026-09-29 rule changes. Step 2's measured peak was 0.30 GB.
- **Colours.** Riga's orange, brown and gold for 1, 2 and 4. Deep purple
  `#4a148c` for 3 and 5: Riga's cyan scored 40.9 against Personal services,
  and the purple scores 47.1 against the nearest pin and 78+ against the
  other lines.
- **Privacy verdict: publishable.** 656 pins, 0 person-like names, 0
  contact details; no holder column is ever read.
- **Daugavpils was also left out of Europe's zoom fit.** At 26.5° E it is
  the easternmost European city, 0.4° east of Bucharest, so it moves
  Europe's centre that far east. That is a front-page change that
  deploy-verify should look at in the review batch. Its label is 73.7 px,
  right of the dot (dy -12 to 12 pass): PROBLEMS 0.
- **Notice 42 now reads "VZD (Riga, Liepāja, Daugavpils)"**, and the OSM
  notice names Daugavpils's trams. Both are for the owner's approval at
  review time.
- **`osm_tram.py` gained two backward-compatible options** (commit 97ba25a).
  The Czech kit takes the same file.
  - `station_add` accepts a tuple of refs. This was the Czech kit's
    request, for Plzeň's Jízdecká and U Synagogy, which lines 1, 2 and 4
    all serve.
  - `accept_members` accepts a named stop member that has no stop tag.

  The Aarhus control passes, and Odense's and Liepāja's figures are
  unchanged.

### 2026-09-30 - Liepāja built on tram-build; Riga's step 2 lifted into latvia_register.py

- **Riga's step 2 was lifted into `pipeline/countries/latvia_register.py`,
  and Riga's output did not move.** Riga's step 2 is now a thin call into
  the module.
  - **The control** is `scripts/latvia_register_control.py`. It rebuilds
    Riga's frame through the module and compares it with Riga's
    `businesses_clean.csv`. All 6,725 rows are identical, and all 11 step 2
    figures match `outputs/riga/baseline.json`.
  - **Rejected: running `drift_check.py riga` as the control**, which the
    skill had named. It would re-run Riga's steps from a branch into the
    shared `data/` junction, and the in-memory control answers the same
    question without writing.
  - **The classification stays in `pipeline/riga/config.py`**, and later
    Latvian configs import it from there. `category_continuity_table.py`
    reads those rules by their text in Riga's config, so moving them would
    break that check. One set of rules for the country, decided once.
  - **Measured peak: 0.34 GB.**
- **Liepāja built: 18 stations, 702 storefronts, 69.7% in a ring** (the
  screen's figure).
  - **Stations: the 15 stop names on OSM's two ref-1 relations, plus three
    added by node.** All three lie on the relations' own track:
    - Brīvības iela, the terminus, is a platform member whose stop
      position carries no name;
    - Klaipēdas iela, between Tukuma iela and Ventas iela, has a stop
      position each way but is on neither relation;
    - Rožu laukums, between Pētertirgus and Koncertzāle, is a platform
      member each way with no stop position.
  - **The approved call named only Brīvības iela and Klaipēdas iela**, but
    the brief's own count of 18 needs Rožu laukums too. So it was read as
    the brief's prose missing one stop, not as a new call.
  - **`osm_tram`'s `station_add` now accepts a named platform node**, for
    an add only, and refuses an add whose name is already a route stop. The
    Aarhus control still passes, and Odense still has zero drift.
  - **Spacing and frequency.** The median gap is 313 m (the brief: 329 over
    15). No gate 3: no operator count was read. The approved call's "about
    every 7 minutes" is stated on the page.
  - **Food** comes from the excise register (Riga's national cache), placed
    on VZD's address register `aw_eka.csv` (fetched 2026-09-30, 7,839
    existing addresses in Liepāja): 131 premises, 123 placed (93.9%: 110
    exact, 13 with the unit dropped). This matches the screen.
  - **Shops and services** come from the premise groups in ATVK 0005000:
    771 premise groups, 579 kept, all placed. The screen counted 583 before
    the 2026-09-29 name-rule changes (fuel stations kept, repair and stands
    dropped).
  - **Step 2's measured peak was 0.30 GB.**
- **Liepāja privacy verdict: publishable.** 489 pins, 0 contact details and
  0 person-like names. No holder column is ever read: food shows the kind
  and street address, shops show the cadastre's own word.
- **Notice 42 widened to "VZD (Riga, Liepāja)", FOR THE OWNER'S APPROVAL AT
  REVIEW TIME.** It names Liepāja's cadastral map and VZD's State Address
  Register, with the elements the brief requires:
  - VZD's own source wording and the year, "Izmantoti Valsts adrešu
    reģistra informācijas sistēmas dati, 2026. gads";
  - VZD named, and CC BY 4.0 linked;
  - the changes described: addresses matched and points used to place each
    premises, and the file not shown;
  - "VZD has not approved these changes or this map."

  The OpenStreetMap rail-geometry notice now names Liepāja's tram, its
  stops and the city boundary.
- **Liepāja is left out of Europe's zoom fit (`REGION_ZOOM_WITHOUT`), as
  Riga, Stockholm and Bucharest are.** Fitted to it, the zoom dropped and 57
  label problems appeared at every width, whatever Liepāja's own offset. It
  lies inside the frame Riga and Bucharest already set, so the centre does
  not move. Its label is 48.2 px, measured, placed below the dot (dy 14-34
  pass): PROBLEMS 0.
- **The template's "{this city's ratio to OpenStreetMap}" is left unfilled
  for Odense and Liepāja.** Neither template city's page has one: Aarhus's
  CVR wording and Riga's two-layer wording are what section 6 says to
  reuse. Measuring one is an Overpass count of shops and food per city, with
  its own caveats about OSM's tagging. **For the owner: fill it per city, or
  drop it from the template?**

### 2026-09-30 - Odense built on tram-build; osm_tram.py written, its Aarhus control passing

- **`pipeline/osm_tram.py` written to the tram-city skill's section 4
  contract (commit 17f906c on `tram-build`), and its control passes:
  `scripts/osm_tram_control.py` reproduces Aarhus's `stations.csv` exactly**
  on Aarhus's cache: 20 stations, the same names, lines and kommune, and
  coordinates within 1e-9 degrees. It is Aarhus's `stop_rows()` generalised:
  - `select_relations` keeps relations on ref + route (+ operator), and exits
    on any relation that is neither kept nor in `not_drawn`, on a stale
    `not_drawn` id, and on a ref with no kept relation. It is also the
    lines-only mode.
  - `stop_rows` takes stop members tagged `stop_position` or `tram_stop`,
    unions a ref's relations, takes `station_add` by node with its expected
    name, and applies aliases whose two spellings must both be present.
  - `collapse` is Aarhus's name collapse at 200 m.
  - `split_by_places` scopes over a union of polygons.

  Aarhus's own step 1 was not rewired: its output is the independent answer
  the control compares against. The signature, return shape and branch went
  to the Czech kit (which was waiting on them) and to the France build
  session. Staging, the app/chrome owner while no third window runs, was told
  before the file was written.
- **Odense built: 25 stations, 2,834 storefronts placed (98.4%).**
  - **Rail.** OSM's two `route=tram` relations (ref L, operator Keolis)
    carry 24 stop names on 48 stop positions. SDU Syd/Hospital Nord was added
    by its two direction nodes (7942163365, 7942163366), as the approved
    call. Gate 3 ran against the operator's figure: 25 against 25, the
    operator's 26 stops less Hospital Syd. Every station is in Odense Kommune
    (304.7 km² as OSM draws it). The line is drawn whole with
    `load_osm_line_shapes`.
  - **Spacing.** The median gap measured 430 m, not the brief's 441, and
    holds the halved rings; step 1 stops outside 380-500 m.
  - **Stray node.** Idrætsparken's node 9034508024 is also on no relation.
    It is a second stop position 10 m from Idrætsparken's member node, not a
    station, so it was left alone.
  - **Businesses.** CVR generation 505 through Aarhus's chain: 3,208 rows in
    divisions 47/56/96 and 221 structurally excluded, leaving 2,987. `969900`
    was dropped (108 rows, 3.6%, 84% personally owned against 46%), leaving
    2,879, of which 2,834 were placed. The screen of 2026-09-27 counted 210
    structural exclusions and 2,998 storefronts. The build's filter is the
    shared one, so the build's figure stands.
  - **Rings.** 1,154 storefronts sit within a ring (40.7%), in-ring
    R/F/P 603/343/208.
- **Hospital Syd is a watch item, not a row in `excluded_stations.csv`.**
  The approved call was "out until it opens in 2027". Listing it failed
  `check_scope_disclosure.py`: What Is Excluded has no category for a stop
  not yet in service, and adding one is an `app/station_scope.py` change and
  an owner call. A stop that is not yet in service is not part of the
  network, so no category is needed. Step 1's `check_not_yet_open` stops the
  build when OSM puts Hospital Syd on a route or drops its tag. The page does
  not mention it. **For PLAN.md: add Hospital Syd when the new OUH opens
  (due 2027).** Rejected: a new "not yet open" category, which is new public
  wording for one stop.
- **The frequency sentence is left out of Odense's page.** It is optional in
  the template (braces). Odense Letbane's own køreplan page, valid from
  10 August 2026, states Saturday (7.5 min), Sunday (10 min) and Friday
  evening (10 min), but no weekday figure. The brief's 7.5 minutes came from
  the screen, so it is not stated. Rejseplanen is never read. The owner's
  per-city interval value (sent to cleanup) can carry it later.
- **Line colour `#b8860b` (dark goldenrod)**, this project's own, since OSM
  records none. CIE76 74.8 from the nearest pin (Personal services);
  `check_map_markup.py` PROBLEMS 0. Aarhus's `#30556E` was tried first and
  scored 42.7 against Retail, under the preferred 45.
- **Macro label.** The width measured 50.6 px in a browser tab with Google
  Fonts' Space Grotesk. Seven built cities' widths reproduced exactly:
  Aarhus 46.9, Prague 47.3, Oslo 29.0, Riga 29.5, Bergen 48.3, Boston 48.4
  and Chicago 55.0. The offset is `("start", 11, 6)`: only dy 5-8 on the
  right passes. Above the dot, the label covered Aarhus's marker and
  overlapped Copenhagen's label; below, it overlapped Amsterdam's and
  Berlin's. `check_macro_labels.py` PROBLEMS 0.
- **Odense privacy verdict: publishable**, on Aarhus's precedent.
  `check_personal_exposure.py odense` found 1,154 pins, 0 contact details
  and 0 person-like names at a residential unit. The heuristic's 170
  distinct person-like names were read in full: brands and chains (Arnold
  Busck, Harald Nyborg, Magasin, ZARA) and company-form shops, cafés and
  salons trading under a founder's name (HENRIK GUNDTOFT, Ingvard
  Christensen, Nadja Holst). Personally owned forms are already shown by
  address. The one bracketed hit, "GreenMind Odense (Kongensgade)", is a
  chain branch.
- **Three displayed notices widened to name Odense, FOR THE OWNER'S APPROVAL
  AT REVIEW TIME** (Aarhus's were owner-approved on 2026-09-29):
  - CVR, notice 30: "(Copenhagen, Aarhus, Odense)", "Copenhagen's, Aarhus's
    and Odense's business premises";
  - Klimadatastyrelsen, notice 31: "in Aarhus and Odense the points are
    OpenStreetMap's copies of them";
  - OpenStreetMap (rail geometry): "Odense's Letbane line and its stops, the
    municipal boundary used to select them and the address points used to
    place its businesses".

  They sit on `tram-build` and ship only when `app/` lands.
- **Step 2 is not a heavy job: measured peak 0.70 GB.**
  - The gate (`scripts/heavy_job.py`) refused it first at the 5.5 GB
    declared from Aarhus's brief: 6.9 GB available, against 5.5 + 2. That
    "about 5 GB" was the size of the files read, not memory.
  - It was re-run under `HEATMAP_MEMCAP_TEST_GB=4.5`, a hard cap that can
    only lower the per-process limit. The declared 4.5 GB peak was then true
    by construction, and was admitted.
  - A Danish step 2 can be declared at 1 GB from now on.
- **Page numbers by block**, agreed between sessions so the landings don't
  collide:
  - Band B: 76-86;
  - France: 100-119;
  - tram kit: 130-139 (Odense 130);
  - Czech: 150-155.
- **Left for the landing, not done on the branch**:
  - README's city list (`readme_cities.py`);
  - the master list's built counts;
  - `map_inconsistencies.md`'s prose counts (section 6, "half the size in
    seven cities").

  Each is a shared count that every concurrent build would change on its
  own branch, so each is set once, at landing.

### 2026-09-30 - All builds activated, with six working rules for concurrent sessions (owner)

- **The owner gave the go for every build session**: Band B, the France
  builds, the Czech builds and the tram kit. The go was relayed by the tram
  kit to each live session. The Czech kit asked the owner to confirm it in
  its own session, which is the right behaviour for a relayed permission.
- **The six rules, in the owner's words where given:**
  1. **Heavy jobs**: "If two heavy jobs go under the memory thresholds we
     established, run those concurrently." The relay first set the budget at
     12 GB summed over two jobs (the 12 GB with-children cap). A measurement
     minutes later disproved it: only 2.3 GB of 15.9 was available, with
     eight Claude sessions taking 6.3 GB, Opera 1.8, and an orphaned
     staging grep 4.7 (PID 17392, started 13:54, a
     `.{0,30000}` pattern over a licence page, its parent gone). The tram
     kit was not permitted to stop another session's process, so that was
     left for the owner. **Corrected rule**: at most two heavy jobs, each
     started only when available memory is at least its peak plus 2 GB; an
     unknown peak counts as 8 GB.
  2. **Priority**: the tram kit goes before the Czech builds. So the tram
     kit writes `pipeline/osm_tram.py` first, starting with Odense.
  3. **DECISIONS.md drafts per session**: "keep drafts for decisions.md for
     each build session and pass off all at once for cleanup to implement".
     Each session writes `docs/decisions_drafts/<session>.md`, and cleanup
     folds them all in at once. That ends the append-only merge conflicts,
     four of which fell on this session's pushes on 2026-09-30 alone.
  4. **Overpass**: "stagger osm requests": one query in flight per session,
     and at least 60 s after a 504 or 429. Both mirrors were 504ing under
     several sessions' load that day.
  5. **Plan**: the owner is no longer on Pro.
  6. **Downloads and prose are pre-permitted**: the sources a brief names,
     and page text written from an approved template. A departure from a
     template is flagged, and does not stop the build.
- **Memory monitoring: a start gate, not a monitor.** The owner asked
  cleanup to "monitor all sessions for memory. Or whatever reactive protocol
  is efficient and safe". The tram kit recommended a gate,
  `scripts/heavy_job.py`, with a ledger in the shared `data/` junction that
  admits a job only if it fits in available memory, drops dead pids, and
  lists any process over 1.5 GB. Polling spends tokens all day and still
  reacts after the damage; a gate costs one call per heavy job. It was handed
  to the multi-city cleanup session to build. A second session named
  "Cleanup Session" belongs to another project (link-station-commercial),
  received the broadcast by mistake, and declined it.
- **Rejected**: a fixed summed budget (disproved by measurement above), and
  a polling monitor session.
