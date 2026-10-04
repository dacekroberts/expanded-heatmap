# DECISIONS drafts - new-cities build (`new-cities-build`)

Entries for `DECISIONS.md`, newest first, each written exactly as it should
land (the `decisions-entry` format). Cleanup folds them in when the owner
hands the drafts off, then deletes this file (owner, 2026-09-30). The build
is Liverpool (Regional), Tacoma and Mendoza
(`docs/handoff_new_cities_2026-10-03.md`).

### 2026-10-04 - Mendoza built: the Metrotranvía from OpenStreetMap drawn to both ends, the capital's open commercial accounts, one business type each

- **Argentina's second city, sharing no code or source with Buenos Aires**
  (`pipeline/mendoza/`, page 193): the capital alone (owner, 2026-10-03).
  Brief claims held (`brief_check.py mendoza`, 5 of 5). Mode `light_rail`
  (the brief's proposal; a converted railway) and coverage `full` (owner,
  2026-10-04: Personal services, 296, small but complete).
- **Rail, from the one Overpass query** (2026-10-04, overpass-api.de, 58
  elements): two `route=light_rail` relations, ref MTM, operator Sociedad de
  Transporte Mendoza (2119332 line 101, 3413331 line 100), each with all 25
  stops; 50 stop positions -> **25 stations**.
  - **Gate 3 against es.wikipedia's infobox, 25, the brief's named secondary
    fallback (owner, 2026-10-04).** The operator's own page says "dos
    Estaciones Principales, además de 21 paradores" (23), which no list
    reconciles, and its timetables carry 11 timing points only.
  - **Scope: OSM's Departamento Capital (relation 2204157), the owner's call
    over the portal's seccionales (2026-10-04)**: no new source, already in
    the one query, and it places exactly the 7 stations the city's own stop
    list files under the Ciudad de Mendoza (Pedro Molina inside; 25 de Mayo
    and José María Godoy outside, the brief's three border stops). 106.0 km²,
    gated at 95-115. The 18 stations outside are listed with their
    departments: Godoy Cruz 8, Las Heras 5, Maipú 5.
  - **The line drawn to both ends** (owner, 2026-10-03), its outside stations
    without rings (Florence's shape).
  - **Halved rings on the spacing rule**: the capital's 7 stations sit a
    median 412 m apart (min 336, max 731), under 550 m; the whole line's
    median is 556 m. MEDIAN_GAP_BOUNDS_M (360, 470).
  - **Color #CB2910**: OSM's "red" (#C62828 as drawn) sits 33.2 from the Food
    service pins; the nearest red clearing 45 from every pin and 3:1 on both
    page backgrounds, 45.4.
  - Frequency from STM's winter 2026 weekday timetable (its operator's own
    PDF): every 10 minutes at peak, 13 at midday.
- **Businesses ("Listado Comercios por Actividad 2025", the cached JSON,
  sha256 as approved):** 41,179 activity rows for 8,309 businesses; 151 with
  no business type out; by the taxonomy (the entry below) Retail 3,397, Food
  service 713, Personal services 296, out 3,752; every point present, read as
  EPSG:5344 and reprojected, and every one inside the capital: **4,406
  storefronts**. 641 (15%) within a ring: Retail 413, Food service 173,
  Personal services 55.
- **The name rule (Vancouver's, as the brief names it):** a trade name in
  the register's sole-trader form, surname first with a comma, no "&" or
  digit and no company or trade word, shows the business type: 144 of all
  8,309 names carry the form, 92 of them storefronts. The shown type is the
  register's own rama label.
- **Personal exposure (`check_personal_exposure.py mendoza`):** 641 pins,
  619 distinct names; one name column, no fallback; 0 emails, phone numbers
  or c/o markers; 0 surname-first names left; 1 "person's name (trade name)"
  shape; the heuristic reads 207 (32.3%) as person-like, within the built
  Spanish-language registers' range (Madrid 26.1%, Barcelona 27.6%,
  Guadalajara 30.7%, Mexico City 32.3%), where it reads shop names. No row
  was printed at any stage. **Verdict: publish.**
- **Notice 141, the Municipalidad's CC BY 4.0 credit**: the dataset's title
  linked to its page, the licence linked, the modifications stated and no
  endorsement. **A proposal**: no wording is prescribed and no template
  covers it.
- **For Visuals:** 141 on the card face or in the caption, as CC BY 4.0
  allows either ("in any reasonable manner based on the medium"; a caption
  linked from the card satisfies it); the rail and boundaries are
  OpenStreetMap's, so the OSM line goes on the face. No open terms question.
- **Macro map:** label width 61.8 px (browser pane); above its dot. **South
  America's zoom now leaves Mendoza out** (`REGION_ZOOM_WITHOUT`, Riga's
  mechanism): fitted to it, the zoom dropped and the Brazilian coast's labels
  collided (12 problems at every width, whatever Mendoza's own offset). Its
  centre still counts, so on a phone (375 px) Rio de Janeiro's pill clips 87
  px (42.5 before), Recife's 36, Porto Alegre's 8 and Mendoza's 9; PROBLEMS 0
  at 375, 768 and 1200. **For the owner at review time**: the phone clipping
  is the cost.
- **Proposals for review time:** the page's frequency, business, name-rule,
  data-date and confitería bullets; the "Mendoza" section of What Is
  Excluded; notice 141's wording.

### 2026-10-04 - Mendoza's taxonomy: the RAM level, one bucket per business, confiterias as Food service (owner)

- **`pipeline/taxonomies/mendoza_rama.py` keys on the register's RAM level**
  (the business type, `desc_full`), measured with the `premises-taxonomy`
  skill on the cached file (an agent's leg, counts only, no row printed):
  418 RAM values, all enumerated (179 Retail, 18 Food service, 7 Personal
  services, 214 out), an unknown one raises. At RAM 528 of 8,274 rows (6.4%)
  name no trade; SUB is not a finer level (fee lines for signage, scales and
  motors share it, and 14.6% of businesses have no SUB row naming a trade),
  so the RAM catch-alls (offices by their own SUB items) are dropped and
  disclosed rather than dispatched.
- **One bucket per business, by priority over every RAM row** (Food service,
  then Retail, then Personal services): Food service 713, Retail 3,397,
  Personal services 296, out 3,752, no RAM row 151 (out). The alternative,
  the first RAM row in file order, differs on 6 businesses and rests on an
  order nothing documents. 7 businesses carry ramas in two in-scope buckets,
  all Food service with Retail.
- **CONFITERIA (137) is Food service, a measured departure from Buenos Aires
  (owner, 2026-10-04, "Food service, a measured departure").** Buenos Aires
  files confiterias as Retail because its survey keeps cafe-tearooms under
  CAFE, leaving CONFITERIA as the pastry shop (owner, 2026-09-28). Mendoza's
  register does the opposite: its pastry and bread shops are PANADERIA (98%
  carry a pastry or bread item), while its confiterias carry sidewalk-table
  permits (69%) and alcohol service (45%) as CAFE BAR (77%, 77%) and
  RESTAURANT (64%, 91%) do, and the City's own fee and alcohol items group
  them with cafes ("CONFIT.CAFES,LECHE,CHOCOLATERIA" on 128 of 137,
  "ALCOHOL CONFITERIA, CAFE BAR" on 55). Matched by what the premises is,
  per `docs/category_rules.md`. Rejected: Retail, one reading of the word
  across both Argentine cities, which would draw about 137 seated cafes as
  shops.
- **The rest as drafted (owner, 2026-10-04, "Accept as drafted"):** street
  stands on the public way out (38 sidewalk newsstands, ESCAPARATE; 27 feria
  franca produce stands; 16 flower kiosks; 1 other), R1's food-stall rule
  carried to non-food stands; VETERINARIA (29) out by the vet rule, though
  some also sell pet food; GALERIA (10) and CENTRO COMERCIAL (2) out as an
  arcade's or mall's own row; INSTITUTO (111, mostly teaching and medical)
  out; the unclear abbreviations at their best reading, among them BAR
  AMERIC. (2) kept as Food service, since both businesses' other items are a
  restaurant's, a cafe's and sidewalk tables (an exception to R3 in
  `scripts/category_continuity_table.py`), MERCADO PERSA (9) and FOTOGRAFIA
  (9) Retail, LAVADERO (12) out as mostly car washes.
- **Pending for the owner:** T.OPTICA (1), a lens workshop, drafted out as a
  workshop rather than an optician's shop; listed as pending in the
  continuity table.

### 2026-10-04 - Tacoma built: the T Line from OpenStreetMap, gate 3 exact against Sound Transit, the City's active license accounts under its site-wide disclaimer

- **Built on Kansas City's template** (`pipeline/tacoma/`, page 194): a US
  register on the shared NAICS module, the shared OSM tram step 1, the TIGER
  place polygon. Brief claims held (`brief_check.py tacoma`, 6 of 6). Mode
  `tram` and coverage `full` as the brief proposes, for the owner with the
  build.
- **Rail, from the one Overpass query** (2026-10-04, overpass-api.de, 24
  elements): two `route=tram` relations, ref "T Line", operator Sound
  Transit, network Link, colour #F38B00 (5705256, 5705257), both kept, no
  other tram or light rail in the box. 22 stop positions -> **12 stations**,
  all inside the city.
  - **Gate 3 exact**: Sound Transit's own T Line page lists 12 stations,
    St Joseph to Tacoma Dome (read 2026-10-04). It writes "S 25th" where OSM
    writes "S 25th St"; the map shows OSM's name.
  - **Median gap 451 m** (min 349, max 755), so halved rings (0.05 / 0.1 /
    0.2 / 0.3 mi), as the brief measured on the feed; MEDIAN_GAP_BOUNDS_M
    (400, 500).
  - OSM's orange kept: 77.9 from the nearest pin color (Food service), every
    line label 4.5:1 in both themes (`check_map_markup.py`).
  - Frequency from the same page: every 12 minutes weekdays 7:00-20:00 and
    Saturdays, every 20 otherwise and on Sundays, stated as a fact.
- **Businesses ("Business Licenses - Map (Tacoma)", the point layer, last
  edited 2026-10-02), fetched with an explicit field list that leaves every
  `mailing_*` field out:**
  - 22,128 accounts; 11,812 in council districts 1-5; 2,931 in the buckets,
    the brief's counts exactly (Retail 1,520, Food service 600, Personal
    services 811); every one has a point and every one is inside the TIGER
    polygon.
  - 61 at an apartment, trailer or mobile-home space left off as homes
    (Kansas City's set, APT and TRLR, with `residence.py`'s SPC/SPACE: 59 and
    2); 19 duplicate accounts at one name and site address -> **2,851
    premises**.
  - 503 (18%) within a ring: Retail 183, Food service 135, Personal services
    185.
  - The catch-alls follow `naics.py` unchanged, as every NAICS city's do:
    459999 (264) and 455219 (71) kept, 812990 (194) out.
- **The name rule (Vancouver's, 2026-09-21, as the brief names it):** where
  the trade name is only the account holder's own name (697 of the storefront
  accounts), the holder carries no company form (164) and the name reads as a
  person's by `residence.looks_personal` or Kansas City's surname-first test
  (104), the pin shows the NAICS description. A trade name an owner chose is
  shown as chosen, the San Diego and Vancouver precedent: 775 storefront trade
  names are person-shaped by the same over-firing test, most of them shop
  names. **Rejected, for the owner to reopen**: Kansas City's further rule, a
  company trading only under a person's name shows its address, which there
  rested on reading every person-shaped name by eye; this build prints no
  name, so it is not applied.
- **Personal exposure (`check_personal_exposure.py tacoma`):** 503 pins, 493
  distinct names; 0 emails, phone numbers or c/o markers; 0 surname-first
  names; 2 "person's name (trade name)" shapes; the heuristic reads 86 (17.1%)
  as person-like, owner-chosen trade names; 1 person-shaped name at a UNIT,
  which the home rule does not read as a dwelling. **Verdict: publish**, on
  Vancouver's rule and the home rule.
- **Notice 142, the City of Tacoma's disclaimer**, word for word from the
  City's disclaimer item (115 words, its curly apostrophe kept), shown on
  every page as Chicago's (2) and Kansas City's (80) are: the owner accepted
  the licence "on Chicago's template" (2026-10-03). `check_provenance.py`'s
  EVERY_PAGE_APPROVED gains 142 on that acceptance; **for the owner to
  confirm** at review time, since that set is the owner's. The credit "City
  of Tacoma, Tax & License (data.tacoma.gov)" sits in the page's caption, not
  in a numbered notice; data.cityoftacoma.org is never cited.
- **For Visuals:** 142 in the caption, in full (Chicago's and Kansas City's
  full paragraphs must sit in the caption itself, owner 2026-10-02); about
  115 words fits a card face only in small type. **Open terms question**:
  the City may require any display or use to end, for any reason, and its
  disclaimer binds "applications"; whether a city card counts as one is
  Visuals' question to carry to the owner, so Tacoma stays off the cards until
  the owner rules. The rail is OpenStreetMap's, so the OSM line goes on the
  face.
- **Macro map:** label width 51.8 px (measured in the browser pane); minor
  tier, as the US tram cities are (Kansas City, Tucson, New Orleans): in the
  United States composite every side of its dot met Seattle's, Sacramento's
  or Minneapolis's pill. Below the dot in United States West, PROBLEMS 0 at
  375, 768 and 1200. Out of the landing frame, as Seattle (Regional) is.
- **Proposals for review time:** the page's Sounder clause ("Sounder's trains
  to Tacoma run mostly at rush hour"), the name-rule bullet, the home bullet
  and the account caveat under "Reading the density"; the word "tram" for a
  line Sound Transit markets as light rail (the brief's heading, the
  tram-city template); Tacoma's section of What Is Excluded.

### 2026-10-04 - Liverpool (Regional) built: Merseyrail's Northern and Wirral Lines as a commuter-rail exception, gate 3 exact against Merseytravel's booklets and NaPTAN's rail records, food only on the FSA register

- **Built on the UK six's shared steps as config** (`pipeline/liverpool/`,
  page 195), the first UK map on heavy rail: Merseyrail drawn as a
  commuter-rail exception (owner, 2026-10-03), map mode `metro` (owner,
  2026-10-03, "1. metro"), the scope Liverpool, Sefton, Knowsley and Wirral
  (owner, 2026-10-03). Brief claims held (`brief_check.py liverpool`, 5 of 5).
- **Rail, from the one Overpass query** (2026-10-04, overpass-api.de, 1,088
  elements; train routes of Merseyrail's network or operator only, and the
  four councils' boundaries by GSS code):
  - 13 relations: the Northern Line's 6 and the Wirral Line's 4 kept (ref,
    operator Merseyrail); the City Line's 3 (289382-289384, tagged
    `network=Merseyrail` but run by Northern Trains, one still tagged London
    Midland) named in NOT_DRAWN with the 15-minute reason.
  - 135 stop positions -> 69 stations by name (widest spread 182 m, Seaforth
    & Litherland's two platforms).
  - **Gate 3, the operator: exact.** Merseytravel's timetable booklets, the
    brief's named sources, read for the line diagram on each cover: the
    Northern Line (valid from 17 May 2026) 37 stations, the Wirral Line (from
    20 September 2026) 34 Merseyrail stations, the Bidston - Wrexham line's
    Upton and Heswall (Transport for Wales) not counted. The build: 37 and 34.
    Merseyrail's own site sits behind a bot challenge and was not tried.
  - **Gate 3, NaPTAN: 59 of 59 names match** against the active RLY records
    (ATCO area 910, prefix 9100) inside the four councils, three under
    NaPTAN's other names (NAPTAN_NAME_ALIASES: Birkenhead Hamilton Square;
    Liverpool Central's loop platforms and Lime Street's low-level station,
    each a record of its own). 13 NaPTAN-only stations are explained in
    NAPTAN_EXPLAINED as on lines not drawn: ten on the City Line (Broad Green,
    Edge Hill, Halewood, Huyton, Mossley Hill, Prescot, Roby, Wavertree
    Technology Park, West Allerton, Whiston), Upton and Heswall on TfW's
    Bidston - Wrexham line, Meols Cop on Northern's Southport - Wigan line.
  - The light-rail test's track print reads railway=rail 100%, 12.5% in tunnel
    or on a bridge: heavy rail, expected, drawn on the commuter-rail exception
    rather than on that test.
  - **Scope: 59 inside, 10 outside** (Ormskirk, Aughton Park, Town Green;
    Hooton, Capenhurst, Bache, Chester, Little Sutton, Overpool, Ellesmere
    Port), as the brief counted. Northern 34 and Wirral 27 in scope.
  - **Spacing: median 1,182 m in scope** (min 210, mean 1,149, max 3,100), so
    the standard rings (0.1 / 0.2 / 0.3 / 0.6 mi), well over the spacing
    rule's 550 m; MEDIAN_GAP_BOUNDS_M (1,000, 1,400).
  - Lines merged by London's branch rule: Northern 3 of 6 relations, 64.6 km;
    Wirral 4 of 4, 100.3 km, the one-way loop drawn once within the merge.
  - **Colors adjusted, on measurement:** OSM's #036ebc and #00a654 (the
    operator's blue and green) moved to #08A0C0 and #28A800 by
    `line_colour_search.py liverpool` (45.1 and 45.6 from the pins, 3:1 on
    both pages, the pair 94.8 apart).
- **The brief's two frequency checks, from the same booklets:** every
  Kirkby-branch train runs to Headbolt Lane (Fazakerley, Kirkby and Headbolt
  Lane share every column); and Bebington's autumn pattern (from 21 September
  2026, Chester and Ellesmere Port lines only) is minutes 19, 27, 34, 49, 57,
  04 towards Chester, gaps of 8, 7 and 15, so every Wirral station short of
  Hooton keeps 15 minutes or better by day.
- **Businesses (the FSA's four files, every extract 2026-10-02):**
  - 10,179 register rows; 7,400 storefront rows, the brief's figure exactly.
  - 4 at a "Flat" address never placed; no childminders.
  - 622 without the FSA's point: 399 placed at a Code-Point centroid, 223
    (3.0%) not placed (Sefton 3.8%, Wirral 3.7%, Knowsley 2.5%, Liverpool
    2.4%); no outward-only postcodes. **Sefton's full file places 94.1% at the
    FSA's own point**, so the brief's 75.3% all-type sample did not hold.
  - 1 outside the sanity box and 2 outside the councils; 11 trading-as names
    show the trade name.
  - **7,170 storefronts placed** (Food service 4,797, Food shops 2,373): 94.4%
    at the FSA's point, 5.6% at a centroid. 3,732 (52%) within a ring: Food
    service 2,625, Food shops 1,107.
  - Canteens by name are at least 1.9% of Restaurant/Cafe/Canteen (names
    with canteen, cafeteria, staff restaurant, a contract caterer's name or
    hospital), not separated (London's precedent).
- **Personal exposure (`check_personal_exposure.py liverpool`):** 3,732 pins,
  3,303 distinct names; no fallback name exists, since step 2 never loads an
  owner column; 0 emails, phone numbers or c/o markers; 0 surname-first
  names and 22 "person's name (trade name)" shapes (Manchester had 12); the
  heuristic reads 899 (24.1%) as person-like, which on the FSA register is
  mostly pubs and cafés named for people. **Verdict: publish**, London's,
  Newcastle's and the UK six's on the same register.
- **Notices (Staging's numbers):** 143 Food Standards Agency (Liverpool),
  Newcastle's notice 62 as Manchester's 84 with the city and date changed;
  **153** Ordnance Survey (Liverpool), Manchester's 85 with the city changed.
  The kit had reserved only 141-143; the centroid tier needs an Ordnance
  Survey notice of its own, so Staging assigned 153 (2026-10-04) after
  Belgium's 144-152. The Department for Transport, NaPTAN notice 86 takes the
  owner's reworded first sentence (2026-10-03) and Liverpool's page; notice
  1's rail sentence and `app/osm_notice.py` name Merseyrail.
- **For Visuals:** 143 and 153 in the caption only (the OGL's "including or
  linking to", as the eight Ordnance Survey cities and London's FSA notice);
  notice 86's new first sentence changes UK captions, not faces; the rail and
  boundaries are OpenStreetMap's, so the OSM line goes on the card face. No
  open terms question.
- **Macro map:** label width 135.0 px, measured in the browser pane with the
  Google Fonts face loaded (controls Blackpool (Regional) 139.7 and
  Nottingham (Regional) 151.7 reproduced). Liverpool's pill below its dot;
  **Manchester (Regional)'s United Kingdom pill raised 14 px** (("end", -10,
  0) to ("end", -10, -14)), because level with its dot it covered
  Liverpool's marker. A search over 64 pairs of offsets with
  `check_macro_labels.py`'s geometry found two with PROBLEMS 0 at all three
  widths, both needing Manchester's pill raised; the simpler was taken.
- **Proposals for review time (no template covers them):** on the page, the
  bullets "Merseyrail is suburban rail that runs as a metro ...", "In the
  evening and on Sundays most stations have a train every 30 minutes." and
  the City Line bullet; in What Is Excluded, the Merseyrail sentences in
  "Which stations these maps are drawn around" and Liverpool's Stations
  paragraph; the new row in `docs/commuter_rail_list.md`. The brief flagged
  the evening sentence and the City Line sentence as proposals too.
- **For the owner, one call:** `label_tier`. The UK rule is "tram and light
  rail against metro", which would make a metro city major, while the brief
  carries "minor, as the UK six". Set to minor (a pill only in the United
  Kingdom view) pending the owner; major would put a fourth UK pill in the
  Europe view beside London, Glasgow and Newcastle and needs that view
  re-scored.

### 2026-10-04 - The UK steps take heavy rail: a configurable NaPTAN stop type, a route filter and boundaries by GSS code; zero drift on the UK six

- **`pipeline/countries/uk.py`'s NaPTAN gate reads `config.NAPTAN_STOP_TYPE`,
  MET when unset; Liverpool (Regional) sets RLY.** Merseyrail's stations are
  rail access nodes (StopType RLY, ATCO area 910, prefix 9100), never the
  tram stops' MET in area 940, so the gate's hard-coded `"MET"` would have
  counted zero. The default keeps the six built UK cities on MET without a
  config edit. `norm_name` also drops NaPTAN's rail suffix "Rail Station" and
  a county qualifier left trailing once it is gone ("Walton (Merseyside) Rail
  Station"): area 910 names 95 of its 98 records in a Merseyside box that way
  (read 2026-10-04 from a scratch probe of the area file). The alternative, a
  per-city alias for every station, would have been 59 entries restating one
  suffix rule.
- **`pipeline/countries/uk_fetch.py` gains `config.OSM_ROUTE_FILTERS` and
  `config.BOUNDARY_GSS`, both fetch-only.** The first narrows a route mode to
  one network (tag filters, each its own selector, unioned), because every
  `route=train` in a Merseyside box would otherwise come back (the osm-rail
  skill's rule against box-wide train queries). The second selects the scope's
  admin relations by `ref:gss` when their relation ids are not yet known, so
  the city's one Overpass query also reads the ids, which the config then
  records; each code must match exactly one relation. `fetch_osm` now counts
  route relations by `type=route` rather than by not being a boundary id,
  the same set for every built city.
- **Proved at zero drift on the six built UK cities, twice**:
  `drift_check.py manchester birmingham edinburgh sheffield nottingham
  blackpool`, once after the stop-type change and once after `norm_name`'s,
  both "RESULT: zero drift", every baseline figure unchanged and every
  NaPTAN name match as before (Manchester 99, Birmingham 35, Edinburgh 23,
  Sheffield 48, Nottingham 50, Blackpool 40); measured peak 0.48 GB through
  `heavy_job.py`. The fetch change cannot be drift-checked (no step runs
  it), so the six cities' Overpass query strings were generated from git
  HEAD's `uk_fetch.py` and from the new one and compared: identical for all
  six. Cleanup confirmed the shape of the change before it landed
  (2026-10-03).
