# Coverage sweep - the Americas and Oceania (2026-10-03)

Desk work only. No Overpass/OSM API, no downloads, no portal probing beyond
confirming a portal exists. Repository read at `worktree-staging` (3ce25226).

## Method

- **Universe** from Wikipedia: "List of tram and light rail transit systems"
  (North America, South America, Oceania sections, read through the
  MediaWiki parse API because the page truncates), "List of metro systems",
  "Streetcars in North America" (modern, heritage-regular and tourist-heritage
  tables, under construction), plus searches for 2025-2026 openings (Campeche,
  OC Streetcar, Monterrey L4/L6, El Insurgente, Auckland CRL).
- **Check** of 230 names and spellings (accents stripped, satellites
  included) against `docs/city_master_list.md` (ML), `city_master_list_evidence.md`,
  `city_master_list_2026-09-30.md` (ARC), `global_country_shortlist.md` (SL),
  `commuter_rail_list.md` (CR), the tram docs (TL), `global_transit_gap.md`
  (GTG), `app/cities.py`, then every other `docs/**/*.md` as a fallback.
  Grep output kept at `scratchpad/sweep/grep_out.txt` (my run, before another
  agent reused `grep_cities.py`).
- **Streetcar precedent** (checked as asked): a short US streetcar is NOT
  disqualifying by itself. Kansas City (one line, 18 stops) and Tucson were
  built; Milwaukee, Detroit and Tampa were discarded as "too thin, a judgement
  and reversible" because their data was food-only or unplaced, not because the
  line was short (ML:361-363, TL:334-337). Cincinnati failed on frequency
  (20-25 min). Tourist-only heritage lines (seasonal, weekends) are treated
  here as out of scope by service, not flagged.

Status key: **BUILT** · **R** (Band R) · **ADD-ON** (recorded extension of a
built map) · **DISCARDED** · **RECORDED, NO ROW** (screened, negative, no row by
rule) · **COUNTRY-ONLY** (covered only by a country-level verdict) ·
**SIBLING-ONLY** (covered only by a sibling or core city's verdict; its own
host never asked) · **NEVER RECORDED** · **OUT** (not rail, not open by end of
2026, or tourist-only service).

---

## 1. Full classified table

### United States

| City | System | Status | Evidence |
|---|---|---|---|
| New York | Subway, SIR | BUILT | ML:47 |
| Washington D.C. | Metrorail (DC Streetcar closed 2026-03-31) | BUILT | ML:47; tram_rescope_specs.md:41 |
| Chicago | 'L' | BUILT | ML:47 |
| Boston | MBTA subway, Green Line, Mattapan | BUILT | ML:47 |
| Philadelphia | SEPTA Metro (L, B, T, G) | BUILT | ML:47 |
| San Francisco | Muni Metro, F/E heritage | BUILT | ML:47 |
| Los Angeles | Metro Rail A-K | BUILT | ML:47 |
| Miami (Regional) | Metrorail, Metromover | BUILT | ML:47 |
| San Diego | Trolley | BUILT | ML:47 |
| Buffalo | Metro Rail | BUILT | ML:47 |
| Sacramento | SacRT light rail | BUILT | ML:47 |
| Houston | METRORail | BUILT | ML:47 |
| Dallas | DART (Streetcar and M-Line not drawn) | BUILT | ML:47; excluded_categories.md:302 |
| Kansas City | KC Streetcar | BUILT | ML:47 |
| Tucson | Sun Link | BUILT | ML:47 |
| New Orleans | RTA streetcars | BUILT | ML:47 |
| Minneapolis | METRO Blue, Green | BUILT | ML:47 |
| Pittsburgh | PRT light rail | BUILT | ML:47 |
| Seattle (Regional) | Link 1 and 2 Lines, 11 cities | BUILT | ML:47 |
| Arlington (VA) | Metrorail (D.C. add-on) | R | ML:175 |
| Long Beach | A Line (LA add-on) | ADD-ON | ML:203 |
| Atlanta | MARTA, Atlanta Streetcar | DISCARDED (terms) | ML:359 |
| Baltimore | SubwayLink, Light RailLink | DISCARDED (currency) | ML:391 |
| Honolulu | Skyline | DISCARDED (no register) | ML:355 |
| Cleveland | Red, Blue, Green | DISCARDED (no register) | ML:351 |
| Charlotte | LYNX Blue, CityLYNX Gold | DISCARDED (no dataset) | ML:384 |
| Denver | RTD light rail | DISCARDED (no address/class) | ML:385 |
| Norfolk | The Tide | DISCARDED (a stream) | ML:360 |
| Phoenix | Valley Metro Rail | DISCARDED (no register) | ML:353 |
| Mesa | Valley Metro Rail | DISCARDED (no register) | ML:354 |
| Tempe | Valley Metro Rail, Tempe Streetcar | DISCARDED (no address) | ML:498 |
| Portland | MAX, Streetcar | DISCARDED (no classified register) | ML:350 |
| St. Louis | MetroLink | DISCARDED (a stream) | ML:392 |
| Salt Lake City | TRAX, S Line | DISCARDED (no register) | ML:352 |
| San Jose | VTA light rail | DISCARDED (no business-tax dataset) | ML:381 |
| Austin | Red Line | DISCARDED (rail) | ML:383 |
| Fort Worth | TEXRail | DISCARDED (rail) | ML:382 |
| Cincinnati | Connector | DISCARDED (frequency) | ML:364 |
| Detroit | QLine (+ People Mover) | DISCARDED (thin, reversible) | ML:362 |
| Milwaukee | The Hop | DISCARDED (thin, reversible) | ML:361 |
| Tampa | TECO Line | DISCARDED (thin, reversible) | ML:363 |
| Oklahoma City | OKC Streetcar | DISCARDED (no register) | ML:357 |
| El Paso | El Paso Streetcar | DISCARDED (no register) | ML:358 |
| St. Paul | METRO Green | DISCARDED (no register) | ML:356 |
| Berkeley | BART | DISCARDED (3 stations) | ML:365 |
| Newark, Jersey City, Hoboken, Camden, Oakland, Evanston, Pasadena, Santa Monica, Alexandria | NLR/PATH/HBLR, PATCO/River Line, BART, 'L', LA Metro, Metrorail | RECORDED, NO ROW (no register on two methods) | ML:421-423 |
| Cambridge, Somerville | MBTA | RECORDED, NO ROW (food only) | ML:423 |
| Hialeah, Coral Gables | Metrorail | BUILT (inside Miami Regional) | ML:424 |
| **Tacoma** | Sound Transit T Line (12 stops since 2023) | **NEVER RECORDED** as a city (the line is only named as out of Seattle's scope) | build_briefs/seattle.md:366; excluded_categories.md:563 |
| **Memphis** | MATA Main Street trolley (suspended Aug 2024, return targeted fall 2026) | **NEVER RECORDED** | none |
| **Little Rock / North Little Rock** | Metro Streetcar (heritage) | **NEVER RECORDED** | none |
| **Trenton** | NJ Transit River Line (diesel LRT, Camden-Trenton) | **NEVER RECORDED** (Camden screened, no row) | ML:422 for Camden only |
| **Oceanside / Escondido** | NCTD Sprinter (DMU) | **NEVER RECORDED** as cities (Sprinter named only as excluded from San Diego) | CR:22 |
| Santa Ana / Garden Grove | OC Streetcar | OUT: revenue service slipped to March 2027 | none |
| Omaha | Omaha Streetcar | OUT: 2026-2027, not open | none |
| Kenosha, Galveston, Lowell, Fort Collins, Astoria, Loop Trolley (St. Louis), El Reno, Fort Smith, Willamette Shore | heritage | OUT: seasonal or weekend tourist service | none |
| Morgantown | WVU PRT | OUT: people mover | none |
| San Antonio, Columbus, Nashville, Indianapolis, Jacksonville, Las Vegas | none / commuter / BRT / people mover | recorded no-rail set (search level) | ML:447-453 |

### Canada

| City | System | Status | Evidence |
|---|---|---|---|
| Toronto | Subway, streetcar, Lines 5 and 6 | BUILT | ML:48 |
| Montréal (agglomeration) | Métro, REM | BUILT | ML:48; tram_rescope_specs.md:47-52 |
| Vancouver (with Surrey) | SkyTrain | BUILT | ML:48 |
| Calgary | CTrain | BUILT | ML:48 |
| Edmonton | LRT | BUILT | ML:48 |
| Ottawa | O-Train | BUILT | ML:48 |
| Kitchener-Waterloo | ION | BUILT | ML:48 |
| Burnaby, New Westminster, Coquitlam | SkyTrain | ADD-ON (ready) | ML:192 |
| Port Moody | SkyTrain | RECORDED, NO ROW (licence table has no address) | build_briefs/vancouver_regional.md:16 |
| Richmond (BC) | Canada Line | R | ML:174 |
| Laval | Métro, REM | DISCARDED | ML:326 |
| Longueuil | Métro | DISCARDED | ML:327 |
| Brossard | REM | DISCARDED | ML:328 |
| Vaughan | TTC Line 1 | DISCARDED | ML:329 |
| Brampton | (Hurontario LRT, 2028) | DISCARDED, revisit | ML:325 |
| Mississauga, Hamilton, Québec City, Winnipeg, Halifax | none open | recorded no-rail | ML:402-405 |
| Deux-Montagnes (QC) | REM terminus | outside Montréal's agglomeration, its stops drawn as excluded | tram_rescope_specs.md:50 |

### Mexico, Central America, Caribbean

| City | System | Status | Evidence |
|---|---|---|---|
| Mexico City | Metro, Tren Ligero | BUILT | ML:49 |
| Guadalajara (Regional, with Zapopan, Tlaquepaque, Tlajomulco) | SITEUR | BUILT | ML:49; app/cities.py:509 |
| Monterrey (Regional) | Metrorrey (L4/L6 due Dec 2026 or later) | BUILT | ML:49 |
| **State of México municipios** (Ecatepec, Nezahualcóyotl, La Paz, Naucalpan) | Metro Líneas A, B, 2 | **NEVER RECORDED** as candidates; noted only generically ("Línea B crosses into the State of México") | excluded_categories.md:103 |
| **Toluca (with Metepec, Lerma, Zinacantepec)** | El Insurgente interurban (full line to Observatorio Jan 2026) | **NEVER RECORDED** | none |
| Campeche | "Tren Ligero" (opened 2025-07-20) | OUT: a rubber-tyred guided bus (CRRC DRT), Clermont-Ferrand's rule | ML:323 for the rule |
| Puebla, Mérida, León | BRT | recorded BRT-only | SL:981 |
| Panama City | Metro L1, L2 | DISCARDED | ML:284 |
| San Miguelito (PA) | Metro L1, L2 | SIBLING-ONLY (national portal enumerated for Panama City) | ML:284 |
| Santo Domingo | Metro L1, L2 | DISCARDED | ML:490 |
| Santo Domingo Este / Norte | Metro | SIBLING-ONLY (national portal enumerated) | ML:490 |
| **San Juan, Puerto Rico (with Bayamón, Guaynabo)** | Tren Urbano | **NEVER RECORDED** (grep hits are Manila's and Lima's "San Juan") | none |
| **Oranjestad, Aruba** | Oranjestad streetcar | **NEVER RECORDED** | none |
| San José, Costa Rica | Tren Interurbano (diesel commuter) | COUNTRY-ONLY ("no urban rail" single-feed list; correct on rail) | SL:1445 |

### South America

| City | System | Status | Evidence |
|---|---|---|---|
| Buenos Aires | Subte, Premetro | BUILT | ML:54 |
| São Paulo (Osasco's two Linha 9 stations out of scope) | Metrô, CPTM 9 | BUILT | ML:54; CR:20 |
| Rio de Janeiro | Metrô, VLT, SuperVia two branches | BUILT | ML:54 |
| Belo Horizonte | Metrô | BUILT | ML:54 |
| Brasília | Metrô-DF | BUILT | ML:54 |
| Salvador | Metrô (VLT a watch item) | BUILT | ML:54, ML:210 |
| Fortaleza (Regional) | Metrofor | BUILT | ML:54 |
| Porto Alegre (Regional) | Trensurb | BUILT | ML:54 |
| Recife (Regional) | Metrô | BUILT | ML:54 |
| Santos (Regional) | VLT | BUILT | ML:54 |
| Contagem, Duque de Caxias | Metrô BH, SuperVia | ADD-ON | ML:204 |
| Teresina, Maceió, João Pessoa, Natal, Sobral, Juazeiro/Crato | suburban / diesel VLT | DISCARDED (frequency) | ML:331-336 |
| Cuiabá | VLT never ran | recorded no-rail | ML:401 |
| Santiago | Metro | DISCARDED (coverage) | ML:317 |
| Lima | Metro L1, L2 | DISCARDED (coverage) | ML:314 |
| Medellín | Metro, Ayacucho tram | DISCARDED | ML:299 |
| Bello, Itagüí, Envigado, Sabaneta, La Estrella | Medellín Metro Line A | SIBLING-ONLY (RUES and chamber are national/regional; own hosts never asked) | ML:299 |
| Bogotá | (Metro L1 2028) | DISCARDED (rail) | ML:298 |
| Caracas | Metro | DISCARDED (no portal) | ML:285 |
| **Maracaibo, Valencia (VE), Los Teques** | Metro de Maracaibo, Metro de Valencia, Metro Los Teques | SIBLING-ONLY (Caracas's national-host failures) | ML:285; SL:2112 |
| **Mendoza (Capital, Godoy Cruz, Las Heras, Maipú)** | Metrotranvía Mendoza | **NEVER RECORDED** | none |
| **Quito** | Metro de Quito (2023) | **NEVER RECORDED** (named in staging's sweep entry as never recorded) | decisions_drafts/staging.md:17 |
| **Cuenca (EC)** | Tranvía de Cuenca (2020) | **NEVER RECORDED** | none |
| **Valparaíso / Viña del Mar** | Metro Valparaíso (Merval) | **NEVER RECORDED** | none |
| **Concepción (CL)** | Biotrén | **NEVER RECORDED** | none |
| **Cochabamba** | Mi Tren (2022) | COUNTRY-ONLY: Bolivia sits in the "no urban rail" single-feed list, a misfiling like Algeria's | SL:1445 |
| Tren de la Costa (Vicente López to Tigre, BA province) | light rail on ex-railway | **NEVER RECORDED** | none |
| São Luís | VLT (inactive) | OUT | none |

### Oceania

| City | System | Status | Evidence |
|---|---|---|---|
| Sydney (City of Sydney LGA) | Sydney Trains T1-T4/T8/T9, Metro M1; light rail left out (owner) | BUILT | ML:58 |
| Melbourne (City of Melbourne LGA) | Metro Trains; trams left out (owner) | BUILT | ML:58 |
| Brisbane | Citytrain | DISCARDED (commuter frequency) | ML:499 |
| Gold Coast | G:link | DISCARDED (no register) | ML:486 |
| Adelaide | Glenelg tram | DISCARDED (land use per property) | ML:485 |
| Perth | Transperth | DISCARDED (land use per property) | ML:389 |
| Canberra | Light rail | DISCARDED (liquor/tobacco only) | ML:487 |
| **Parramatta** | Parramatta Light Rail (opened Dec 2024), Sydney Trains, Metro NW (Epping) | **NEVER RECORDED** | none |
| **Newcastle (NSW)** | Newcastle Light Rail (2019) | **NEVER RECORDED** (every "Newcastle" hit is Tyne and Wear) | none |
| Randwick, Inner West (Sydney L1-L3), Melbourne tram LGAs (Port Phillip, Yarra, Stonnington, Merri-bek, Darebin, Boroondara, Glen Eira...) | Sydney LR, Melbourne trams | satellites; only Yarra and Merri-bek touched, by assertion ("none publishes the register") | SL:2103 |
| Auckland | Auckland rail (City Rail Link opened 2026-09-13) | COUNTRY RULED OUT (NZ: "licensing is not municipal") | ML:595; GTG:64 |
| Wellington | Metlink rail | COUNTRY RULED OUT | ML:595; SL:3252 |
| Christchurch | heritage tram loop | COUNTRY RULED OUT; also OUT (tourist service) | ML:595 |
| Bendigo, Ballarat | heritage trams | OUT (tourist) | none |

---

## 2. Never recorded and country/sibling-only, ranked by promise

Station counts are approximate, from Wikipedia and operator or press pages.

1. **Mendoza (AR)** - NEVER RECORDED. Metrotranvía, one line, 25 stations over
   about 17 km from Las Heras through the Ciudad de Mendoza and Godoy Cruz to
   Maipú (airport/Luján extension under way), about 7 min at peak. Business
   route: the Ciudad de Mendoza's own CKAN has a "Comercios" dataset with
   points, activity type and status (2022, 2023) and a "Listado Comercios por
   Actividad 2025", CC BY 4.0 (`datos.ciudaddemendoza.gob.ar`). Only the
   capital department publishes it as far as seen, so scope and currency are
   the questions.
2. **Tacoma (US)** - NEVER RECORDED as a city. T Line, 12 stops, all in Tacoma,
   about every 10-12 min by day. The City publishes "Business Licenses
   (Tacoma)" on `data.tacoma.gov` (ArcGIS Hub; older Socrata
   `data.cityoftacoma.org`): about 22,241 active tax-and-licence accounts,
   daily, with site address and industry code. Caveats: the publisher says it
   does not show whether the current-year licence is held, and it carries
   mailing addresses (privacy check).
3. **Mexico City (Regional) add-on: State of México municipios** - noted only
   generically. Ecatepec and Nezahualcóyotl (Línea B), La Paz (Línea A),
   Naucalpan (Línea 2, Cuatro Caminos), about 12-15 stations. DENUE already
   covers them with coordinates under the built national modules, so this is a
   scope change, not a screen.
4. **San Jose (US) and the VTA cities via Santa Clara County** - SIBLING-ONLY
   in effect. San Jose's discard (ML:381) asked the city's portals for a
   business-tax dataset; the County's Department of Environmental Health food
   facility data on `data.sccgov.org` (SCC_DEH_Food_Data, updated to
   2026-09-30) was never asked. A food-only page in Ottawa's or Stockholm's
   shape could cover San Jose, Santa Clara, Sunnyvale, Mountain View, Milpitas
   and Campbell. Unverified (fields not read).
5. **Quito (EC)** - NEVER RECORDED. Metro de Quito, 15 stations, all inside the
   Distrito Metropolitano, about 5-6 min. Every establishment needs a LUAE
   licence; whether a register is published is unknown. Portal:
   `gobiernoabierto.quito.gob.ec` (catalogue at `datosabiertos.quito.gob.ec`).
6. **Valparaíso / Viña del Mar (CL)** - NEVER RECORDED. Merval, 20 stations,
   about 10 in the two comunas at roughly 1 km spacing; 6 min peak, 10 min
   midday, 12 min evening, so the commuter-rail exception could pass. Business
   route: comuna patentes (Santiago's row records five Metro comunas
   publishing on `datos.gob.cl`); Viña's transparency portal is
   `transparencia.munivina.cl`. Unknown whether either publishes a list.
7. **Cuenca (EC)** - NEVER RECORDED. Tram, 27 stops in the cantón, 6-10 min.
   Portal: `cuencaendatos.cuenca.gob.ec` (CKAN; transit stops seen). No
   business dataset seen.
8. **San Juan, Puerto Rico** - NEVER RECORDED. Tren Urbano, 16 stations (San
   Juan most, Guaynabo, Bayamón), 8 min peak to 16 min off-peak. Only
   statistics portals found (`datos.estadisticas.pr`); patentes are
   municipal, no list seen. Low to medium.
9. **D.C. add-on: Montgomery and Prince George's Counties (MD)** - satellites
   never recorded. About 25 Metrorail stations. Both counties publish daily
   food inspection data (`data.montgomerycountymd.gov`,
   `data.princegeorgescountymd.gov`). Note: Arlington went to R and
   Alexandria had no register (ML:175, ML:422).
10. **Parramatta (AU)** - NEVER RECORDED. Parramatta Light Rail, 16 stops,
    7.5-10 min, plus Sydney Trains and Metro at Epping. No floor-space or
    establishment census found for the City of Parramatta (the FES is the City
    of Sydney's), so likely Perth's and Adelaide's shape.
11. **Auckland / Wellington (NZ)** - COUNTRY RULED OUT on "licensing is not
    municipal", which the shortlist marks ASSERTED (SL:3252) and which was
    overturned for Australia on 2026-09-28 (SL:2103). Rail is commuter; the
    City Rail Link opened 2026-09-13 on a transitional timetable, so the
    frequency test would decide it first. Worth a one-line re-check of the
    country ruling rather than a screen.
12. **Newcastle (AU)** - NEVER RECORDED. Light rail, 6 stops over 2.7 km, about
    every 7.5-10 min. Thin (Aubagne's shape), and no council register seen.
13. **Concepción (CL)** - NEVER RECORDED. Biotrén, two lines on railway track;
    frequency not read (likely 15-30 min, so likely fails). Low.
14. **Cochabamba (BO)** - COUNTRY-ONLY, misfiled as "no urban rail". Mi Tren,
    two lines on the old railway, 12-25 min, so the railway-track frequency
    gate likely fails. Bolivia has no known open register. Low.
15. **Toluca (MX)** - NEVER RECORDED. El Insurgente, 4 State of México stations
    over about 40 km: commuter spacing, so it fails the exception even though
    DENUE would place everything. Its 3 CDMX stations (Observatorio, Vasco de
    Quiroga, Santa Fe) are a watch item for the built Mexico City map.
16. **Maracaibo, Valencia (VE), Los Teques** - SIBLING-ONLY. Small systems
    (6, 9 and about 4 stations) with irregular service; Venezuela's national
    hosts fail (Caracas). Low.
17. **Medellín's satellites (Bello, Itagüí, Envigado, Sabaneta, La Estrella),
    San Miguelito (PA), Santo Domingo Este/Norte (DO)** - SIBLING-ONLY; each
    core's discard enumerated the national route. Low.
18. **Trenton (River Line), Oceanside/Escondido (Sprinter)** - NEVER RECORDED.
    Diesel light rail on railway track at about 15-30 and 30 min; the
    light-rail test's frequency gate fails. Low.
19. **Memphis, Little Rock** - NEVER RECORDED. Heritage streetcars at about
    20-30 min (Memphis suspended since 2024); fail frequency. Low.
20. **Tren de la Costa (AR), Oranjestad (AW)** - NEVER RECORDED. A largely
    tourist ex-railway line in the Buenos Aires suburbs, and a short free
    downtown streetcar. Low.

## 3. Satellites never screened (add-on routes, not ranked above)

- **Los Angeles**: Culver City, Inglewood, the A Line foothill cities to
  Pomona, Norwalk, El Segundo and others. Only Long Beach (add-on), Pasadena
  and Santa Monica (no register) are recorded. LA County Public Health's food
  inventory covers most of them (Pasadena, Long Beach and Vernon run their
  own); not verified.
- **Hudson-Bergen Light Rail**: Bayonne, Union City, Weehawken, North Bergen.
- **BART beyond Oakland and Berkeley** (Fremont, Hayward, Daly City, Walnut
  Creek, Concord and others): no built map's satellite, since San Francisco
  draws Muni only (ML:365).
- **Satellites of discarded cores, own hosts never asked**: Portland's
  (Gresham, Beaverton, Hillsboro, Milwaukie), Denver's (Aurora, Lakewood,
  Englewood, Littleton, Centennial), Salt Lake's (West Valley City, South Salt
  Lake, Murray, Sandy, West Jordan, South Jordan, Draper), Atlanta's
  (Decatur, East Point, College Park, Doraville, Sandy Springs, Brookhaven),
  St. Louis's (Clayton, University City, East St. Louis, Belleville),
  Cleveland's (Shaker Heights, East Cleveland), Baltimore County's.
- **Satellites of built maps recorded only as excluded-station counts**:
  Boston's (Brookline, Newton, Quincy, Medford, Malden, Revere, Milton;
  decisions/2026-09-20.md:18655), Chicago's (Oak Park, Skokie, Cicero, Forest
  Park, Wilmette; decisions/2026-09-13.md:68), Dallas's (Plano, Richardson,
  Garland, Irving, Carrollton; excluded_categories.md:300), Minneapolis's
  Bloomington (excluded_categories.md:432), San Diego's (Chula Vista, National
  City, La Mesa, El Cajon, Santee; decisions/2026-09-13.md:632),
  Philadelphia's Upper Darby and Norristown (decisions/2026-09-20.md:19113),
  Sacramento's Rancho Cordova and Folsom, Pittsburgh's Mt. Lebanon.
- **Sydney and Melbourne LGAs** beyond the two built ones (section 1, Oceania).

## 4. Counts

Core rows of section 1 (a grouped row such as "Newark, Jersey City, ..."
counts each city once):

| Status | Count |
|---|---|
| BUILT | 41 (US 19, Canada 7, Mexico 3, South America 10, Oceania 2) |
| R | 2 (Arlington VA, Richmond BC) |
| ADD-ON | 6 (Burnaby, New Westminster, Coquitlam, Long Beach, Contagem, Duque de Caxias) |
| DISCARDED | 47 (US 24, Canada 5, Central America/Caribbean 2, South America 11, Oceania 5) |
| RECORDED, NO ROW | 12 (nine US suburbs on two methods, Cambridge, Somerville, Port Moody) |
| COUNTRY-ONLY | 5 (Auckland, Wellington, Christchurch, Cochabamba, San José CR) |
| SIBLING-ONLY | 11 (Maracaibo, Valencia VE, Los Teques, Bello, Itagüí, Envigado, Sabaneta, La Estrella, San Miguelito, Santo Domingo Este/Norte, and San Jose's VTA cities via Santa Clara County as one group) |
| NEVER RECORDED | 17 (Tacoma, Memphis, Little Rock, Trenton, Oceanside/Escondido, Edomex municipios as one group, Toluca, San Juan PR, Oranjestad, Mendoza, Quito, Cuenca, Valparaíso/Viña, Concepción, Tren de la Costa, Parramatta, Newcastle NSW; Edomex is an add-on in effect) |
| OUT | about 15 (OC Streetcar, Omaha, Campeche, Morgantown, São Luís, tourist heritage lines) |

Sources read for the universe and notes (Wikipedia and web, 2026-10-03):
Wikipedia's tram/light rail list (sections 7, 9, 10 via the parse API),
List of metro systems, Streetcars in North America (sections 15, 19, 22, 24);
OCTA/LAist (OC Streetcar to March 2027); Tren Maya and Milenio (Campeche,
DRT guided bus); 1News and OurAuckland (CRL opened 2026-09-13); data.tacoma.gov;
datos.ciudaddemendoza.gob.ar; Mendoza government press (7 min peak);
gobiernoabierto.quito.gob.ec; metrodevalparaiso.cl timetables; Tren Urbano
pages (8-16 min); Los Tiempos (Mi Tren); Wikipedia and press on Cuenca's
tram; Daily Memphian (trolley suspension); data.sccgov.org,
data.montgomerycountymd.gov, data.princegeorgescountymd.gov.
