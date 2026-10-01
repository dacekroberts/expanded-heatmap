# DECISIONS drafts - tram kit (`worktree-tram-kit`, then `tram-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30).

### 2026-09-30 - Zurich built on tram-build: VBZ's trams, and the city's food and alcohol licences

- **Zurich, the project's first Swiss city, built on Stockholm's template** (one city
  register, the city only), Seoul's and Gyeonggi's precedent for partial retail, and the
  shared `osm_tram.py`. 180 stations, 3,363 storefronts (2,335 Food service, 1,028
  Licensed shops), 3,099 of them (92.1%) in a ring; the page says "about nine storefronts
  in ten".
- **`add-country` for Switzerland, kept to what one build established**:
  `docs/data_sources/switzerland.md`. Commerce is licensed and published municipally and
  by trade; the Stadt's CKAN geodata downloads are an Angular page, so the WFS is the
  route; CC0; LV95 (EPSG:2056) is the national grid and the register's own. No other Swiss
  city was probed.
- **The register: `Gastwirtschaftsbetriebe`, 3,487 rows through the WFS, every one
  `Offen` and `jahr` 2026** (the publisher: only open premises are published), last
  updated 2026-09-28. Every row has an LV95 point; the WFS's WGS84 point agrees to
  0.07 m at most, and step 2 gates it. All 3,363 storefronts lie in the Stadt. The second
  CKAN hit (`sid_wipo_...od1111`) is the same register's year-end counts, not a source.
- **The taxonomy: `pipeline/taxonomies/zurich_gastwirtschaft.py`**, keyed on
  `betriebsart`, 14 values each with a home (the publisher documents 11), an unknown one
  raising; a continuity column (handed over).
  - Food service: Gastwirtschaft, Nebenwirtschaft, Kleinwirtschaft, Take Away, the one
    seasonal outdoor restaurant, and **Dancing / Disco (10) - FLAGGED: the brief's screen
    had dance halls out (food 2,325); the standing rule keeps nightclubs not named as
    adult (category_rules R5), so the build follows the rule (2,335).** Owner to confirm.
  - Licensed shops (the Retail bucket, partial): Kleinverkaufsstelle 954, Kiosk 53,
    Tankstelle 21 (owner, 2026-09-30).
  - Out: Ausgabestelle 56 (the city files caterers, kiosks with seating and food trucks
    there; R1), Kantine / Mensa 31 (R1), Patentbefreit 25 (a catch-all, read by name),
    Cabaret / Nachtclub 6 (R3), Veranstaltungsraum 6.
  - **Non-storefront share: 3.6% out by type, plus about 79 institutional kitchens
    licensed as ordinary restaurants (3.4% of food; care homes, staff restaurants,
    hospitals, clubhouses, by a name pattern with a few false hits such as "Noerd
    Kantine").** Göteborg's equivalent was 26.5%. Not filtered: Stockholm's name rule was
    the owner's call on 13% of its register; here the page says they remain. **FLAGGED for
    the owner.** A few Kleinverkaufsstelle licences are offices and online sellers; the
    page says so.
- **Names.** The dot shows `betriebsname` and the licence type in English with the
  register's word ("Shop licensed to sell alcohol (Kleinverkaufsstelle)"). 12 trade names
  read by eye as a person's own show the address (`config.PERSON_NAMED`, Kansas City's and
  New Orleans's rule); kiosk signs with a surname stay. Privacy verdict: publishable
  (the read in place of `check_personal_exposure.py`, which needs the registry entry).
- **The trams.** 36 `route=tram` relations kept (refs 2-11, 13-15, 17, 50, 51), eight
  judged out in `NOT_DRAWN`: tram 12 (1 of 18 stops in the Stadt; the brief's screen said
  2; still a stub, call 19), tram 20 (4 of 26, call 25; Bahnhof Altstetten and Seidelhof
  are on no drawn line and get no ring) and the Forchbahn S18 (call 18; its four city
  stops are all tram stops).
  - **Trams 50 and 51 drawn - FLAGGED.** They are VBZ's construction lines for the 2026
    timetable (14 Dec 2025 - 12 Dec 2026, Bahnhofquai/HB rebuilt): they replace the
    northern halves of 4, 11, 13 and 14 and are the only trams at their outer stops (31
    and 27 stops in the city). Call 2's floor: Transit's published VBZ timetable shows
    trips every 15 minutes (a secondary source; VBZ's own pages read did not state a
    headway). Dropping them would leave Seebach, Auzelg, Frankental and Altstetten Nord
    unringed. **The map is a 2026 map: when the Bahnhofquai reopens, 4, 11, 13 and 14
    change back and Zurich must be rebuilt** (a PLAN item for December 2026; step 1 stops
    once OSM drops refs 50 and 51).
  - 417 stop positions -> 195 stations; Waffenplatzstrasse's two directions sit 233 m
    apart under one stop code (uic_ref 8591415), so the collapse limit is 240 m for this
    city. 180 in the Stadt, 15 outside (trams 2, 4, 10, 50: Schlieren, Zollikon, Opfikon,
    Kloten, Rümlang), drawn and listed. The variant runs (9's peak run to Triemli, 8's
    Sunday run to the Zoo) add no stop of their own.
  - **Median gap 282 m** (brief 283), halved rings, gated at 240-330 m.
  - **Colours - FLAGGED, outside OSM's.** VBZ gives 2/15, 3/11 and 4/9 one colour each
    and 7/50/51 black; two lines with one colour are refused, so the lower number keeps
    VBZ's and the other moves (Den Haag's "one moves"): 15 `#F07A86`, 11 `#005A25`, 9
    `#8A4FA8`, 50 `#4D4D4D`, 51 `#858585`. Tram 10's `#CE1F75` was Delta-E 11.9 from the
    Food service pins and is darkened to `#8E1450` (20.2; Seoul's line 8). Tram 7's
    `#000000` raises in `linecolour.dark_label` (a colour darker than the dark halo is
    moved darker), so it is drawn `#262626` (London drew the Northern's black as a grey).
    Step 3 asserts OSM still records VBZ's colours.
- **CRS: EPSG:2056 (LV95)**, overriding the scaffold's UTM 32N (the tram-city skill).
  At integration, 2056 was added to `check_provenance.py`'s NATIONAL_GRIDS (5.9-10.5 E)
  and the brief's `zurich-projected-crs` check now carries `crs` EPSG:2056 (its derived
  UTM zone claim is unchanged and still true).
- **Page.** The template, filled from the build. **Sentences outside the template,
  FLAGGED**: the colour clause; "Trams 50 and 51 run only while the Bahnhofquai stop is
  rebuilt ..."; the not-drawn sentence (buses, the S-Bahn, the Forchbahn and why; trams 12
  and 20 and the two unringed stops); the person-name clause; the "Read the density"
  caveats (institutional kitchens, offices and online sellers, shared addresses). No
  frequency sentence: no operator timetable was read for one.
- **Licence read: PERMITTED (CC0)**; no notice required; the caption credits "Stadt
  Zürich" as the city recommends. The OSM rail notice gains a Zurich clause.
- **Rejected:** keeping the brief's food count by leaving clubs out (breaks R5); a
  name filter on institutional kitchens without the owner (Stockholm's was an owner
  call); leaving 50 and 51 out (would unring the city's north and west ends for the
  whole of 2026); drawing duplicate colours (refused at render).

### 2026-09-30 - Göteborg built on tram-build: trams 1-13, and the city's food register by its own types

- **Göteborg built on Stockholm's template and `osm_tram.py`.** 127 stations,
  2,987 storefronts (2,110 Food service, 877 Food shops), and 2,255 of them
  (75.5%) in a ring. The page says "about three storefronts in four".
  `coverage` is `narrowed` on tram-build, as Stockholm's is here; the
  owner's `one_bucket` for "Food premises only" (2026-09-30) is on
  origin/macro-legend, whose checks it needs, and Göteborg moves with
  Stockholm when that branch lands (the coordinator, at integration: the
  agent wrote `one_bucket`, which both of this branch's checks refuse).
- **The bucket question raised in the brief needed no new call.** The brief's
  refreshed table and the tram-city skill settle it: food shops count as food.
  The register holds food premises only.
- **The trams.** 26 relations, two per line except 13. Lisebergslinjen
  (444922, heritage) is not drawn.
  - **305 stop positions collapse to 132 stations**; 127 are in Göteborgs Stad
    (OSM 935611, 1,030.4 km² with the sea).
  - **4 and 12 drawn to their ends** (owner, call 21). The stub test passes: 4
    keeps 15 of 20 (75%), 12 keeps 13 of 18 (72%). Their 5 Mölndal stops are
    listed, not ringed. Step 1 re-runs the test each build.
  - **Median gap 390 m** (brief 378), so the rings are halved, gated at
    320-430 m.
  - **Colours: OSM's.** Where a line's two relations differ (5, 6, 7, 8, 10),
    the drawn relation's colour is taken. Where it is a CSS word (4 "green", 11
    "black"), the other's hex.
  - **Line 4 lightened** to `#00BB70`. OSM's `#00A261` was 8.8 from the
    Personal services pins; +0.05 lightness gives 13.3 (Prague's precedent for
    the same green). Rejected: darkening, for Lille's dark-basemap reason.
  - **Line 1 is OSM's white.** Its label passes on a dark halo (18.7:1), so it
    is kept.
  - Labels "Tram 1" to "Tram 13", Riga's form (Västtrafik's own is "Spårvagn
    1").
- **The register: Livsmedelsverksamheter's CSV** (CC0 on the distribution
  node), 5,066 rows, no dates.
  - **`sweden_livsmedel.py` is unchanged.** Göteborg's `typ` is its own local
    vocabulary (47 values), not Stockholm's national groups. So step 2 maps the
    10 storefront types to the module's two groups and excludes the other 37
    with a reason (1,819 rows). A new type stops the step. The pin shows the
    national group.
  - **Out, by type, with some public premises among them**:
    - "RESTAURANG - mottagning" (13): 11 are staff restaurants;
    - FRUKOSTSERVERING (26): hotel breakfast rooms;
    - FARTYG (20): ships, 3 cafés among them;
    - KAFFEROSTERI (8): production;
    - APOTEK (61): `category_rules.md`.
  - **Bakeries and ice-cream makers with a shop are Food shops**;
    ice-cream kiosks are Food service.
  - **Blank `typ` (274)**: classified by the module's name rules (owner, call
    20). 92 kept, 182 dropped. "24SJU" (2) is dropped because the module does
    not know it. A Göteborg-only rule would not survive step 3, which
    re-classifies from the name.
  - **The module's name test drops 47 typed premises.** Among them are public
    cafés at two hospitals, a children's hospital, Trädgårdsföreningen and a
    gym. That is Stockholm's rule, and changing it moves Stockholm.
  - **Vending machines out by name (2)**: category rule.
- **The fallback point: 29 storefronts (1.0%) not placed.** The distribution's
  description says premises with no correct address, or mobile, are placed at
  the Environment Administration's address point.
  - 135 register rows sit within 16.5 m of the AMBULERANDE rows' median, then
    none within 42 m.
  - Florida Pizzeria's own address is Väderlekstorget 6.
  - New Orleans's 0,0 precedent. Rejected: keeping them, which would pile 29
    restaurants and shops on one Majorna street corner.
- **Privacy verdict: publishable.** The register names premises. 13 of the 738
  person-shaped names read as a person's own and show their street address
  (Kansas City's rule). No placed storefront is at an apartment.
- **No notice for the register** (CC0). The OSM rail notice names Göteborg's
  lines and the kommun boundaries.
- **Page: the tram-city template with Stockholm's business wording.** No
  frequency sentence (no timetable read). PROPOSALS outside the template,
  flagged for review time:
  - "in OpenStreetMap's own colours, line 4's made a little lighter so it
    stands apart from the dots";
  - "Buses, ferries and commuter trains are not drawn, and neither is
    Lisebergslinjen, the heritage tram line.";
  - the Mölndal sentence in the plural ("Trams 4 and 12 run on into Mölndal,
    so their 5 stops ... The lines are still drawn to their ends");
  - the business-source paragraph, including "Where a premises is registered
    under a person's name alone, its dot shows the street address instead" and
    "Premises the register has no correct address for are placed at the
    Administration's own address, so they are not shown: about one storefront
    in a hundred";
  - the one-bucket paragraph's list of what is left out, and "It holds food
    premises only". Stockholm's "No open register of other shops ... covers"
    was not reused: no second-source probe has been run for Göteborg
    (reprobe-city);
  - the register caveat: "A food registration is not always a food business:
    gyms, cinemas, bingo halls and general stores that sell some food are
    registered as cafés or food shops and are counted, and a few staff
    restaurants registered under a company name remain";
  - the title "Göteborg: food businesses around tram stops" (Stockholm's
    form).
- **Pending for review time**:
  - `coverage`: flip Göteborg to `one_bucket` with Stockholm when
    macro-legend lands;
  - `sweden_livsmedel.layer_label` would make both Swedish layer menus say
    "Food shops", and `24sju`/vending words in its name rules; each moves
    Stockholm, so drift-check Stockholm if applied.
- **Macro labels, settled with Zurich's and Den Haag's** (the coordinator):
  a grid search over the six crowded Europe labels, PROBLEMS 0 at 375, 768
  and 1200. Göteborg stays above its dot (the scaffold's value); Oslo moves
  left of its dot (below it met Göteborg's, and no Göteborg offset cleared
  both Oslo and Copenhagen); Prague moves left and up (`("end", -11, -8)`;
  above, it met Den Haag's); Milan and Zurich go right of their dots
  (Milan's pill covered Zurich's marker); Den Haag keeps `("start", 11, 0)`.
  The checker models the theme button that once hid Oslo's label.

### 2026-09-30 - Den Haag built on tram-build: HTM's 14 tram lines, the city's permit layer and the BAG

- **Den Haag built on Rotterdam's template and `osm_tram.py`, with Amsterdam's
  precedent for the city's own permit layer.** 166 stations, 6,213 storefronts
  (Shops and services 4,071, Food service 2,142), and 5,781 (93%) in a ring.
  The page says "about nine storefronts in ten".
- **The trams.** Trams 1, 2, 6, 9, 10, 11, 12, 15, 16, 17 and 19 and
  RandstadRail 3, 4 and 34, two OSM relations each, operator HTM, every one
  `route=tram`, so `mode` is `tram`. RandstadRail E (OSM `route=subway`) is out
  as a stub (owner, call 22).
  - **489 stop positions collapse to 231 stations**; 167 are in the Gemeente
    Den Haag (OSM 192736, 98.1 km²). 64 on ten lines are outside and listed,
    not ringed (owner, call 26, for tram 1: 20 of its 37 inside here, 54%,
    against the brief's 19 of 37).
  - **Six stop names belong to two stops each** (Oosteinde 8.8 km apart,
    Beresteinlaan 1.0 km, Fahrenheitstraat 905 m, Weimarstraat 568 m,
    Loosduinseweg 520 m, Duinstraat 351 m). Name collapse would have averaged
    each pair into one point between them. Step 1 groups a name's positions at
    300 m single linkage and labels a split name by its lines
    ("Weimarstraat (line 11)"). No name's groups fall between 230 and 350 m.
    Rejected: renaming by street or place, which would be this project's
    words, not HTM's.
  - **The collapse's spread gate is 250 m, not the shared 200 m**, for two
    stops whose platforms stand apart after the split: Station Hollands Spoor
    (A/B and C/D, 206 m) and Mozartlaan (228 m, staggered).
  - **Median gap 324 m** (brief 335; 322 before the merge below), so the
    rings are halved, gated at 280-400 m.
  - **Leidschenveen (RandstadRail 3, 4, 34) and Leidschenveen Centrum (19),
    10 m apart, merged by explicit alias** at integration (the coordinator,
    2026-09-30): one interchange, one ring set - Houston's couplet and New
    Orleans's Canal Street pairs, Oslo's rule. The agent had left them apart
    as an owner question; the precedent settles it. 166 stations in the
    gemeente.
  - **Not drawn:** 9S (two relations, a short working of 9) and RET's
    Rotterdam tram 8 (in the fetch box only), both in `NOT_DRAWN`.
  - **Colours.** OSM's own, with three changes, each by the smallest HSL step
    that clears 13 from every other line (Rotterdam's rule): 19 darkened to
    `#9f0e11` (it shared `#c01115` with 1); 16 lightened to `#fb8540` (it was
    Delta-E 2.9 from 4's `#fc751c`, a pair the brief did not list); 10 amber
    `#fbc02d` and 34 brown `#5d4037` from the palette (no OSM colour). Tram
    15's `#e63a6b` is 11.9 from Food service's pins, recorded, not changed.
    Label contrast passes.
- **The taxonomy: `pipeline/taxonomies/den_haag_source.py`**, Rotterdam's
  two-source shape with Amsterdam's permit mapping, keyed on the repaired
  `TYPEBEDRIJ` (73 values, each with a home; an unknown one raises), with a new continuity column.
  `rotterdam_source` could not be used: it classifies gazette notice kinds.
  - **In:** restaurants, cafés, lunchrooms, takeaways, snack bars, beach
    pavilions (70 on the map), coffeeshops (32, Amsterdam's and Rotterdam's call),
    nightclubs, sports bars, bakeries' cafés, and six `attractiecentrum`
    permits that are each a restaurant by their own description.
  - **Out (331):** canteens and club houses, community and youth centres,
    theatre and cinema foyers, event sites, party centres, hall hire, cooking
    studios, members' clubs, hotels and their restaurants (Florence's rule),
    the department store (Amsterdam's `Warenhuis`), caterers, sex businesses,
    gaming, recreation, and blank types (26 blank and 1 "niet van
    toepassing", as the brief).
  - **39 food-typed permits re-typed by their own description**: care-home
    and school canteens 9, club canteens, sports halls and a stadium 9,
    museum and theatre cafés 4, hotel and hostel bars and restaurants 15, an
    "erotic entertainment" disco 1, an association's meeting room 1.
- **The permit layer.** 158 pending applications out (owner, call 24).
  - **Fetched by named field**; `AANVRAGER`, `KVKNUMMER` and `RECHTSVORM` are
    never requested, and the fetch stops if one arrives.
  - **Double-encoded UTF-8 repaired** in 1,145 fields (`cafÃ©` -> `café`);
    the step stops if any description is still garbled.
  - **28 permits whose own description records the business gone are left
    out** ("opgeheven", "uit KvK", "ingetrokken", "vervallen", "historisch",
    "vertrokken" ...). Kept: a closure order that ran out in 2024, and an
    operator trading under a notification after giving up the permit. The
    brief had read the layer as dropping closures by removal; it mostly does.
  - **42 older permits at an address with a newer one are counted once**,
    the newest kept.
  - **The trade name** is the description with the city's bracketed staff
    notes, "MELDING" and the leading lower-case type words removed. 39 that
    are only a type word show the type.
- **The BAG.** 6,560 shop-class units in use (PDOK, Rotterdam's query, 4.9 MB,
  no heavy job needed). **1,928 also registered as a dwelling are left off**
  (Amsterdam's owner call), 29% of Den Haag's units against Rotterdam's 26 and
  Amsterdam's 757. 561 at a kept permit's address are de-duplicated by address
  (Amsterdam's rule; Rotterdam's notices had no address and used 3 m).
- **Privacy verdict: publishable.** 643 shown names match residence.py's
  shape test; read by eye, five are only a person's name and show the type
  (`PERSON_NAMED`). The descriptions' staff notes, which name people, are
  stripped. No applicant column is downloaded.
- **Vacancy: CBS, Landelijke Monitor Leegstand 2025, table 1**: 180 of 4,480
  shop units in scope (4%), 1 January 2025; "about one in twenty-five".
- **Page sentences outside the template, flagged:** the colour sentence
  (10 and 34 coloured by this project, 1/19 and 4/16 a shade apart);
  "Den Haag has no metro of its own" (the template's "has no metro", adapted
  for RandstadRail E); RandstadRail E's sentence; the business paragraph
  (Amsterdam's wording, adapted); the vacancy and permit-scope caveats. No
  frequency sentence: no timetable was read.
- **Notice 72 "Gemeente Den Haag"**: proposed text, for review time. Notice 40
  (CBS) now names Den Haag too. The OSM rail notice names Den Haag's lines and
  the gemeente boundaries.

### 2026-09-30 - Florence built on tram-build: T1 and T2, and the Comune's four layers

- **Florence built on Milan's and Rome's template and `osm_tram.py`.** It
  has 39 stations, 12,052 storefronts (exactly the brief's screen: 7,355
  retail, 3,024 food, 1,673 personal), and 4,435 of them (36.8%) in a ring.
  The page says "about three storefronts in eight".
- **The trams.** T1 Leonardo and T2 Vespucci, two relations each, operator
  Autolinee Toscane, in OSM's own colours.
  - **79 stop positions collapse to 43 stations.** 39 are in the Comune di
    Firenze (OSM relation 42602, ISTAT 048017).
  - **T1's four Scandicci stops** (Villa Costanza, De André, Resistenza, Aldo
    Moro) are drawn with the line and listed, not ringed (owner, call 17).
    Step 1 gates 39 inside and 4 outside.
  - **Median gap 323 m**, so the rings are halved, gated at 270-380 m.
  - **Not drawn: eight relations with track and no stops**, all under
    construction: T3.2.1, T3.2.2 (no ref), T4 and T2.2. The Comune says
    T3.2.1 Libertà - Bagno a Ripoli opens about January 2027; re-check then.
    T2's San Marco extension opened on 2026-01-25 and is already on OSM's
    T2.
  - **Colours.** T1 `#254395` scores 22.5 against Retail's pin and T2
    `#5d3988` 33.7. Both are recorded, not changed, because they are the
    source's. Label contrast passes.
- **The taxonomy: `pipeline/taxonomies/florence_attivita.py`**, keyed on
  layer + `tipologiaattivita`, 36 pairs each with a home, with a new
  continuity column.
  - **In:** the exempt food service (owner, call 16; Milan's precedent).
    That is 464 "non soggetta a requisiti comunali" and 175 art. 53; the
    type does not say which are not open to the public, so the page says
    some remain.
  - **Bakers are Retail**, Milan's call: NACE 10.71 sits in the pubblici
    esercizi layer here but sells bread.
  - **Tattoo, piercing and permanent make-up are Personal services.**
  - **Out**, as the screen dropped them:
    - clubs (186);
    - internal shops (128);
    - nonstore sellers (123);
    - farmers (49);
    - wholesale (2);
    - catering and home restaurants (31);
    - temporary service (6);
    - sports-ground bars (33);
    - hotel restaurants (12);
    - rows with no type in the shop and food layers (19).

    A row with no type in the beauty and laundry layers takes its layer's
    bucket.
  - **Kept, flagged:** "CENTRO COMMERCIALE" (7) as Retail. A shopping centre
    row may overlap the shops licensed inside it.
- **No name, no address on any layer.** A dot shows its type in English
  ("Shop", "Restaurant or bar", "Hairdresser").
  - 3,423 rows share a point with another; they are drawn as they are (the
    brief).
  - **Privacy verdict: publishable.** 4,435 pins and 16 distinct labels;
    nothing here can be a person.
- **Notice 71, "Comune di Firenze"**: CC BY 4.0, linked, crediting the
  Direzione Attività Economiche e Turismo and stating the changes. Milan's
  notice is the model, and the text is the project's own. The OSM rail
  notice names Florence's lines and the comune boundaries.
- **Macro label: Florence is 58.1 px** (Houston, Odense, Kansas City and
  Daugavpils reproduced first, after the tab had drifted to another site and
  read Houston 50.6). It sits right of the dot at ("start", 11, -3).
  - **Rome's label moved from above its dot to the right, at ("start", 11,
    2).** Above, it covered Florence's marker in Europe at all three widths.
    The in-process grid passes Rome at -6 to +10 and Florence at -12 to +6.
  - **A front-page change for deploy-verify.**
- **Page: no frequency sentence**, flagged. GEST's timetable was not read.

### 2026-09-30 - New Orleans built on tram-build: the five lines RTA runs, and a new taxonomy

- **New Orleans built on `osm_tram.py` and a new text taxonomy.** It has 106
  stations, 4,689 storefronts, and 2,131 of them (45%) in a ring. The page
  says "about nine storefronts in twenty". The brief screened 38.1% over
  its 110 stops.
- **The brief's lines were out of date; the owner re-took the call at build
  ("draw what runs", 2026-09-30).**
  - The brief drew 12, 47, 48 and OSM's "2", with 46 and 49 out "unless in
    service".
  - RTA's service-changes page (Fall '26 schedules, effective 2026-09-20)
    says 46 Rampart/UPT "will officially reopen for service" (Summer '25).
    It also says 49 Riverfront "will now run along the river from the
    French Market to Julia Street" and "will no longer service Canal
    Street, Loyola Avenue, or Union Passenger Terminal".
  - **Drawn: 12, 46, 47, 48, 49.** OSM's two ref-2 relations are the old
    Riverfront routing via Canal Street, and are `NOT_DRAWN`, superseded.
  - **Rejected:** the Riverfront alone, without 46, which drops a line that
    runs; and the brief as written, which draws a routing RTA no longer
    runs.
- **46's and 49's stops come from OSM's own tram-stop nodes.** 46's are
  relation members with no role, and 49's stand beside its track. 32 nodes
  were assigned to their line by distance to its track (0-10 m) and added
  by node. John Churchill Chase Street, 260 m off 49's new track, is not
  served.
- **Stop names.**
  - **46 shares three Loyola Avenue stations with 47**: OSM's 47 runs
    Loyola to the terminal, so Tulane, Poydras Street and Julia Street merge
    as 46/47.
  - **The riverfront's own Poydras Street and Julia Street**, 600 m away,
    are renamed "Riverfront at Poydras" and "Riverfront at Julia".
  - **Four one-stop-two-names pairs are merged by explicit alias**, 6-26 m
    apart, each direction named for its own side's cross street: Canal at
    Basin / Elk Place, Canal at LaSalle / Marais, St. Charles at MLK /
    Melpomene, Canal at North / South Claiborne. That is Houston's couplet
    rule.
  - The result is 192 stop positions, 110 names and 106 stations.
- **`osm_tram.py`, two backward-compatible changes.** The Czech kit takes
  the same file. The Aarhus control passes, and drift checks for the five
  earlier tram cities are below.
  - **`station_add` takes an optional third element, the shown name**, for
    one node. A name alias renames every node of a spelling, so it could
    not separate the two Poydras stops.
  - **The gap check is per line.** An add is stale when its own line already
    has the stop. A stop of that name on another line is a shared station.
    Before, any route stop of the name refused the add.
- **Rings: median gap 186 m** (the brief read 164 m over its 110), so the
  rings are halved, step 1 gates the median at 120-220 m, and no stop is
  thinned (call 13). The page carries the template's band sentence.
- **Colours: OSM's own**, with the CSS keywords resolved by their CSS
  definitions:
  - 12 `green` #008000 scores 37.2;
  - 47 `red` #FF0000 scores 62.3;
  - 48 #90EE90 scores 30.5;
  - 49 #5C2E86 scores 37.8;
  - 46 has no colour in OSM and takes the project's #b8860b, 74.8.

  Three are under the preferred 45. They are recorded, not changed, because
  they are the source's colours. `check_map_markup` passes, and every label
  reads at 4.5:1.
- **The taxonomy: `pipeline/taxonomies/nola_businesstype.py`**, a new
  continuity column, and a brief check.
  - **Method.** `businesstype` is one level with 486 values: NAICS-era
    titles with no codes, often inverted and misspelt, plus a dozen of the
    City's own permit types. 187 match a NAICS 2017 or 2022 title exactly,
    and 341 do once the inversion and the typos are undone. 17 storefront
    and edge types were coded by hand. Each value maps to the NAICS code its
    title names, so `naics.py` decides the bucket and every shared carve-out
    holds.
  - **The trap:** "Personal Services, Other" (249) title-matches the
    4-digit group 8129, which keeps rows. It is the 812990 catch-all (R2),
    coded so and asserted at import.
  - **Catch-all share, declared in the brief:** 676 of 16,521 (4.1%).
  - **Out, not NAICS:**
    - the brief's two types;
    - festival and Carnival vendors;
    - **flea-market stalls (344)**, on category_rules R1: a market's stalls
      and stands are out;
    - street artists (281), video poker (261) and short-term rentals.
  - **Kept:** pawnshops (7) stay Retail by R5, though NAICS files them as
    lenders.
  - Buckets: Food 1,808, Retail 2,452, Personal 710 licences.
- **The register, step by step** (`iqay-p646`, CC0, daily). `ownername` and
  `businessphone` are never downloaded, and the step asserts it.
  - 4,970 licences are storefront types.
  - **219 sit at the register's 0,0**, ungeocoded, and are counted as
    unplaced; the page says "about one in twenty-three". One more point lies
    outside the parish.
  - 4,750 collapse to 4,689 premises.
  - Two care-of or attention tails are cut from names: "HANGER PROST & ORTH
    C/O GREG MYERS" put a person's name on a pin.
  - **808 show the address**: 783 with no business name, and 25 whose name
    is only a person's (`config.PERSON_NAMED`). All 697 person-shaped
    names were read by eye, and ambiguous ones are listed. Brands and bars
    are kept ("KATE SPADE", "ERIN ROSE").
- **Privacy verdict: publishable.** 2,131 pins:
  - 0 contact details after the tail cut;
  - 0 surname-first names;
  - 2 person-like names at a unit, both restaurants (Johnny Sanchez, Willa
    Jean) in commercial units;
  - one bracketed name, "OTHER PLACE (THE)", a bar.
- **Page: no frequency sentence**, flagged. The brief's "about every 10
  minutes" was search-level, and RTA's schedules were not read for it.
- **Macro label: New Orleans is 82.8 px, right of the dot at ("start", 11,
  4).** **Houston's label rose from level to dy -22.** Level, it covered New
  Orleans's marker at the Global zoom; lower, it covers Miami's; left, it
  meets Los Angeles's and Tucson's.
  - The search was an in-process grid over Houston × New Orleans, about 160
    sets. Houston passes start 11 at dy -30 to -18, and New Orleans 0 to +8.
  - **A front-page change for deploy-verify at review.**

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
- **Licence read (2026-09-30): PERMITTED WITH CONDITIONS; the one owner
  decision it raised is made (below), and Kansas City is cleared to land.**
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
    - **Decided by the owner (2026-09-30): the ordinance controls; land
      Kansas City.** The dataset is declared public domain, KCMO Code
      § 2-2134(a) backs it, and the terms page is undated, with no
      acceptance step, so the indemnity is read as binding nothing.
    - **Rejected:** asking data@kcmo.org first, and dropping the city.
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
