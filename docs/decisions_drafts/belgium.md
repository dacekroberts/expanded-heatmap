# DECISIONS drafts - Belgium build (`belgium-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then empties this file (owner, 2026-09-30).

### 2026-10-04 - Belgium: four more owner calls (privacy, the Brussels dots, Rotterdam's label, the broad query)

- **The owner: "1 yes 2 are these separate builds or can we combine 3 yes
  one placement pass 4 broad query okay".**
  1. **Brussels (Regional) publishes with one name withheld by key**: the
     name `check_personal_exposure.py` read as a person's at a residential
     unit, found and keyed by the check's own logic and never printed
     (`config.PERSON_NAMED`). Two units carry it; both show their activity.
     Re-run: 0 person-like names at a residential unit. Privacy row `publish`.
  2. **The two Brussels dots**: asked whether the pages could combine. The
     answer given: they are separate builds by the owner's earlier call (a
     street survey against the company register, two methods whose counts do
     not compare); the recommendation stays to move Brussels (Regional)'s dot
     inside its own communes. Awaiting the owner's yes.
  3. **One placement pass for Den Haag and Rotterdam** in the Europe view.
  4. **A broader Overpass query for Antwerp** (every tram route in the box),
     after the narrow one returned nothing.
- **Done, call 3**: of 144 offset pairs for Den Haag and Rotterdam in the
  Europe view scored by `check_macro_labels.py`, one has no problem at 375,
  768 and 1200 px: Rotterdam above-right ("start", 10, -12), Den Haag
  below-right ("start", 10, 12). Their labels cross (the dots are 3.0 px
  apart, a known stacked pair). Europe now scores 0; the Belgium view's
  Brussels pair (call 2) is the check's last 6 problems.
- **Done, call 4**: the broad query (`fetch_sources.py --all-tram-routes`,
  one query, overpass-api.de) returned 25 tram route relations: lines 1, 2,
  4, 6, 7, 8, 10, 11, 12, 24, A3 and A9, the feed's lines exactly, with
  notes for the works ("temporarily shortened" on 2, 4 and 12). No relation
  for 3, 9 or 15 under any ref: OpenStreetMap already mirrors the works
  service, so it cannot name the left-bank tram stops either. They stay
  unlisted, and the page and What Is Excluded already say no tram serves
  the left bank during the works. Only De Lijn's own notice could list
  them, and its terms bar republishing it.

### 2026-10-04 - Antwerp's left-bank query (call 5): no tram route relations returned; the closed stations stay unlisted

- **The approved query found nothing to list.** `fetch_sources.py
  --left-bank-trams` (route=tram relations with ref 3, 9 or 15 in Antwerp's
  rail box, their member nodes) was sent once and retried once after the
  owner's minute: overpass-api.de answered with no elements both times
  (`pipeline/osm.py` does not trust an empty 200), and overpass.kumi.systems
  answered 504 and then timed out. Either OSM's relations are tagged
  otherwise or were removed during the works; a second, broader query would
  be a new query and is the owner's call. The left-bank stations stay
  unlisted (config.CLOSED_FOR_WORKS_OPEN_QUESTION), as the page states.

### 2026-10-04 - Brussels (Regional) built: KBO on BeST-Address, companies only, two categories; STIB's whole network

- **Built Brussels (Regional) (page 201)**: the Brussels-Capital Region's 18
  communes outside the City of Brussels. Step 1 on STIB's feed (the City
  page's copy): metro 1, 2, 5, 6 and all 18 trams; 145 stations kept in the
  18 communes, 73 in the City (on the Brussels page) and 13 beyond the
  Region listed without rings, 72 tram stops thinned; the corridor is STIB's
  parent stations, 45 of the network's 70 (the City's 25 are its page's);
  median nearest-neighbour gap 437 m, so halved rings. Colors STIB's, with
  18, 39 and 44 shifted as the City's five were. Step 2 as recorded above;
  step 3: 10,006 of 13,680 storefronts in a ring (73%).
- **The near-City-station count**: 995 storefronts sit within 0.3 mi of a
  City station and of no station on this page, so neither page's rings count
  them; the page says so.
- **Sources**: KBO is never fetched by a script (the owner's login);
  `pipeline/brussels_regional/fetch_sources.py` checks the owner-placed zip
  against its sha256 and refuses otherwise, and re-fetches BeST only on
  `--refetch-best`. KBO's yearly download is due by **2027-10-02** (the
  license's 10.5, the owner's act). Notices 151 (KBO) and 152 (BeST) written.
- **Proposals (sentences outside the page template, for review time)**: the
  different-method bullet (after the brief's drafted paragraph), the
  companies-only bullet, the near-City-station sentence, the several-
  activities sentence, and the caption naming both dates.
- **Downstream, card face or caption**: KBO (151) caption (2.8 asks for the
  source and the update date, nothing on placement); BeST (152) caption (CC
  BY 4.0, any reasonable manner); STIB (148) caption, as Brussels. **Open
  terms question**: KBO's declared purpose (2.3) is the owner's
  registration; if it names a narrower purpose than a public map and its
  derived visuals, that becomes one.

### 2026-10-04 - Brussels (Regional): the privacy verdict, a call for the owner

- **Recommended: publish, with one pin's name withheld by key.**
  `check_personal_exposure.py brussels_regional` on the rendered map: 10,006
  in-ring pins, 9,424 distinct names. Step 2 keeps KBO's establishment units
  of companies (legal persons) only and never opens `contact.csv`, so no pin
  can fall back to a natural person; the dot's name is the unit's
  commercial name (10,981 of 13,680) or the company's (2,699). 3,010 pins
  (30.1%) match the person-name heuristic, the same share as the City's
  street survey (30.0%), as company and trade names in a European city do.
  1 pin carries a person-like name at an address the check reads as a
  residential unit; the recommendation withholds that name by key
  (`config.PERSON_NAMED`, the pin then shows its type) without reading it by
  eye, under the standing rule that no person's name is printed. The
  alternative, publishing all, rests on every name being a legal person's.
  `PERSON_NAMED` stays empty until the owner answers.

### 2026-10-04 - Brussels (Regional): KBO control re-based on brussels_hub, 1-point tolerance (owner)

- **The diagnostic confirmed half of call 6, and the owner approved the
  re-base anyway** ("1 point tolerance sounds acceptable"). On the same KBO
  units, the screen's survey typing gives Retail 78.1 / 76.0 (brief 78.2 /
  76.1) and Food service 83.9 / 84.1 (brief 84.4 / 84.0): the typing
  explains Retail's recall gap; Food's 0.5-point precision gap is not the
  typing. The join already reproduces (88.2% exact against 88.5, 97.2%
  placed against 97.2), so the address match was not expected to recover
  it. Targets are now this build's: Retail 78.2 / 75.4, Food service
  83.8 / 84.1, tolerance 1.0 point (was 0.5), in
  `pipeline/brussels_regional/config.py`.
- **Step 2 then ran to completion**: 13,680 storefronts in the 18 communes
  (Food service 4,972, Retail 8,708; Personal services' 973 off on this
  page); 0 dots without a name, 0 withheld as a person's own; 995 placed
  units within 482.8 m of a City station and of no regional one.

### 2026-10-04 - Antwerp and Ghent built on FAVV-AFSCA and VKBO

- **Built Antwerp (page 197) and Ghent (page 198) on FAVV-AFSCA's operator
  list, placed on Flanders' VKBO unit points, with De Lijn's GTFS for the
  trams.** FAVV's list carries no name or street column; VKBO is asked
  through its WFS for the unit number, type, NIS code, postcode and point
  only, and a page carrying any other property stops the fetch before
  anything is written. Every pin shows its type, so the privacy verdict is
  publish-structural.
- **Antwerp: 4,881 food premises placed**: food service 3,097 of 3,232
  (95.8%), food shops 1,784 as a Retail partial, Borsbeek's 44 included
  (the brief's 3,100 of 3,231 and 1,764 were a screen, before Borsbeek's
  postcode joined). 163 stations, 147 inside the scope; median gap 274 m,
  so halved rings; no thinning (owner).
- **Ghent: 2,730 placed** (food service 1,792, food shops 938); 50 stations,
  49 inside; median gap 273 m, halved rings.
- **A deviation from the brief's field list: UIDN and OIDN are asked for
  explicitly.** Both are mandatory in VKBO's feature type (minOccurs 1), so
  the server returns them whatever `propertyName` says; OIDN pages the fetch
  (sorted, so pages never overlap) and neither is stored.
- **Gate 3 is partial**, against De Lijn's line pages consulted privately
  (delijn.be's terms bar republishing them). De Merode, Havenhuis, Cadix and
  Bijlokehof, which those pages mark unserved but the feed serves from
  2026-10-15, keep their rings as the timetable runs (owner, the six calls
  below, item 4).

### 2026-10-04 - Six Belgian calls approved (owner)

- **The owner: "1-6 recommendations sound good"**, each as recommended:
  1. **Brussels' 46 cafeterias and food courts stay Food service**: the
     survey records street-level units, not staff canteens. The `pending`
     cell in `scripts/category_continuity_table.py` becomes an exception
     citing this entry.
  2. **Shop signs:** Brussels publishes every sign, with no by-eye read (verdict
     publish). Charleroi's 33 and Liège's 39 signs stay withheld by the
     name-shape test (keys only, brands at two or more points exempt), with
     no by-eye read, since this build prints no name.
  3. **Belgium gets a macro-map view of its own, on Czechia's mechanism**,
     holding all six Belgian cities, because their dots collide in Europe's view.
  4. **Antwerp's and Ghent's disputed stops stay as the timetable runs**:
     De Merode, Havenhuis, Cadix and Bijlokehof, which De Lijn's pages mark
     unserved but the feed serves from 2026-10-15, keep their rings.
  5. **One more Overpass query for Antwerp** (its tram route relations for
     lines 3, 9 and 15) to list the left-bank stations closed for works.
  6. **Brussels (Regional)'s agreement targets are re-based on
     `brussels_hub`** once the diagnostic confirms that the survey's typing
     explains the sub-point miss.

### 2026-10-04 - Brussels built: STIB's metro, premetro and thinned trams; hub.brussels's survey in three categories

- **Built the City of Brussels (page 196) on hub.brussels's inventory and
  STIB-MIVB's GTFS.** Step 1: STIB's feed (version 2_21_20261002_143730,
  window 2026-09-28 to 2026-10-25, fetched 2026-10-04 under the portal terms
  the owner accepted on 2026-10-03; the terms text's sha256 is pinned in
  `pipeline/brussels/config.py` so a re-fetch after the terms change stops
  and comes back to the owner) runs metro 1, 2, 5, 6 and 18 tram lines.
  Fifteen trams enter the commune on their regular route and are drawn whole
  (4, 7, 8, 9, 10, 19, 25, 35, 51, 55, 62, 81, 82, 92, 93); 18, 39 and 44
  never enter it. 268 stop places on the drawn lines, 73 inside the
  commune, 66 kept after thinning (7 tram stops cut by the half-mile rule,
  all on trams 10, 51 and 62 in the north), 195 outside listed by commune.
  Gate 3 exact on all four metro lines against fr.wikipedia's "Nb.
  d'arrêts" (21, 19, 28, 26, a secondary source; STIB publishes none). The
  corridor: all 25 underground stations of the City's entrances dataset.
  Median gap among the 66 kept: 377 m, so halved rings (0.05 / 0.1 / 0.2 /
  0.3 mi). Step 2: 6,880 units, one survey (2025-10-17), every unit inside
  the commune polygon; 1,068 vacant out, 743 out by type; **5,069
  storefronts: Food service 1,930, Retail 2,623, Personal services 516**
  (the screen's rough map gave 1,908 / 2,459 / 508); 4,762 inside a ring.
- **A line's regular route takes a trip-share floor as well as Amsterdam's
  day rule.** Metro 1 runs 34 of its 3,932 trips through to Erasme (the
  first and last runs, every day), which the day rule alone counted as nine
  more metro 1 stations (30 against the published 21). A stop now needs at
  least 10% of the line's trips too; metro 1 then reads 21. The alternative,
  an alias list of Erasme-branch stops, would fail silently when the
  timetable changes.
- **The corridor counts as inside the commune by name.** Botanique, Madou,
  Porte de Namur and Rogier lie under the Petite Ceinture, the commune's
  boundary with Saint-Josse and Ixelles: the mean of their platforms falls
  just outside the polygon, while the City's own entrances dataset files
  their entrances in Bruxelles and the brief names all 25 as the commune's.
  Without it the corridor read 21. Rogier being inside brings trams 25 and
  55 in (their premetro terminus), so they are drawn.
- **Elisabeth and Simonis stay two stations** (103 m apart, Koekelberg, both
  outside the commune): STIB's feed and the secondary source's per-line
  counts both count them apart; the source's network figure of 59 (dated
  2011) is one under the feed's 60 for that reason and is not used for gate 3.
- **Station names show French and Dutch** ("Gare Centrale / Centraal
  Station") from the feed's translations.txt where the two differ, as STIB
  signs them; one name where they agree. The feed's own names are upper case.
- **Line colors: STIB's own**, with five trams shifted in HSL lightness only
  to clear Delta-E 13 from every earlier line (Amsterdam's rule): 9, 35, 55,
  92, 93 (STIB gives 19 and 92 one red, 51 and 55 one yellow). Below the
  preferred 45 against a pin color and kept as STIB's: Tram 4 14.4 and Tram
  25 17.3 from Food service, Metro 6 21.0 from Retail, Metro 1 28.1.
- **The taxonomy, `brussels_hub`**: keyed on the single type (285 distinct
  once `type_fr` is split outside parentheses; 1,786 units carry two or
  more, against the screen's naive 1,817). Every type has a home; an unknown
  type raises. A unit takes the highest kept bucket among its types, Food
  service over Retail over Personal services (the screen's rule and the KBO
  measurement's); 175 kept units span two or more buckets. Departures from
  the screen's rough map, each by the category rules or the publisher's own
  filing (premises-taxonomy Step 6): art galleries Retail (precedent);
  "Tailleur - Costumes" Retail, filed by hub.brussels under personal
  equipment rather than Services (the screen had put it with alterations);
  the craft types hub.brussels files under home equipment (glass, mirror,
  crystal, wood, cabinetmaker, framer) Retail; a shisha bar, a board-game bar
  and an e-sport bar Food service as bars; "Comptoir-traiteur" Retail as a
  deli counter (France's traiteurs kept); heating fuel out (nonstore rule);
  photo studios, engravers, trophy shops and clothing rental out as services
  that are not personal care.

### 2026-10-04 - Brussels: calls for the owner (proposals, not yet decided)

- **Cafeterias and food courts (46 units typed "Cantine - Cafétéria -
  Food-court") kept as Food service, pending the owner.** R1 leaves staff and
  institutional canteens out; hub.brussels's survey records ground-floor units
  open to the street, so these read as public cafeterias and food courts.
  Recorded as `pending` in `scripts/category_continuity_table.py`. The
  alternative, out under R1, removes 46 Food-service dots.
- **The privacy verdict, recommended: every shop sign shown, none withheld.**
  `check_personal_exposure.py brussels`: no owner or registrant column
  exists, so no pin can fall back to a person; 0 contact details; 1,427 of
  4,762 pins (30.0%) match the person-name heuristic (restaurants, galleries
  and hairdressers top the list, as trade names in a European city do); 0 at
  an address with a unit marker. The source is a street survey of ground-floor
  commercial units, so every name is the sign on a shopfront, public
  commercial information by definition, and no unit is a home. The precedent
  that reads names by eye and withholds the ones that are only a person's
  (Göteborg's 13, Zurich's 12) was not run: the owner's standing rule for
  this build is never to print a person's name, and a by-eye read prints
  1,427 names. If the owner wants that read, it runs with the names kept off
  screen in a reviewed file. `PERSON_NAMED` is empty meanwhile.

### 2026-10-04 - Belgium: shared commune polygons from OpenStreetMap, one query per city

- **Commune polygons outside the Brussels-Capital Region come from
  OpenStreetMap**, one Overpass query per city (every `admin_level` 8
  relation in the rail box, keyed on `ref:INS`), run one at a time by the
  lead on 2026-10-04: Antwerp 208.0 km2 with Borsbeek (24 communes in the
  box), Ghent 157.6 km2 (12), Charleroi 102.8 km2 (22), Liège 68.5 km2 (18).
  The Brussels cities read the Region's own commune limits (PARADIGM, CC0,
  19 communes; the City 33.1 km2). Reader in `pipeline/countries/belgium.py`,
  fetch in `pipeline/countries/belgium_fetch.py`.
- **The TEC name (relayed by staging, 2026-10-04):** the owner approved
  staging's recommendation: notice 150 credits "LETEC", lines are labelled
  M2, M3, M4 and T1, and no "TEC" appears in legends or prose.
