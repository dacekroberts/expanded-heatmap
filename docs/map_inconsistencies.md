# Why the city maps differ: a cross-city list (DRAFT)

**Status:** a working draft for the owner, first compiled 2026-09-24. It is not
yet on the site, and its placement is deliberately undecided until the last
viable city is built (PLAN.md, "AFTER THE LAST VIABLE BUILD"). Keep it current
as cities land. Its figures were read from the repository on 2026-09-24, so
re-check them before publishing any of it.
**Scope:** every city in `app/cities.py` `CITIES`, in `SWITCHER_ORDER`
(grouped by country). `python scripts/check_inconsistency_list.py` fails when a
built city has no row in any of the four tables, so a city is added here as part
of landing it (the `add-city` and `publish-city` skills say so).
**Method:** read-only. Each city's page prose (`app/pages/*_Heatmap.py`), config and
step files, `docs/excluded_categories.md` (EC), `docs/data_sources.md` (DS), the
build briefs, a grep of `DECISIONS.md` (DEC), and the committed maps. Several
columns come from parsing each committed `outputs/<slug>/heatmap.html`: the legend
rows, the layer-control names (the ring edges and the per-bucket pin counts; those
counts cover pins **inside the rings only**, per `pipeline/map_common.py:2026-2042`),
and the two heat layers' point arrays (inside the rings, and all mapped
storefronts). Where no file says something, the cell reads **UNKNOWN**. Where a
dimension does not apply, it reads **—**.

---

## Differences a reader will notice

### 1. The businesses come from different kinds of record, so density is not comparable between some cities
**Reader sentence:** Some maps are built from licence registers, which record who
applied for permission to trade. Others come from street surveys, which record what
was actually in each shopfront, or from national registers or property records. A
dense-looking city may simply have more complete records.
- **Municipal licence or tax registers:** San Diego, San Francisco, Los Angeles,
  Chicago, Philadelphia, Miami, Washington D.C., Vancouver/Surrey, Calgary, Edmonton,
  Toronto, Milan (six premises registers), Rome (SUAP authorisations).
- **Assembled from several activity-specific registers:** New York (4), Boston (3).
- **Street surveys or censuses of premises:** Montréal, Madrid, Barcelona, and the
  nine Brazilian cities (IBGE's 2022 census walk).
- **National statistical or establishment registers:** Mexico City and Guadalajara
  (INEGI DENUE), the five French cities (SIRENE), Oslo (Enhetsregisteret sub-units),
  Copenhagen (CVR production units), Prague (ROS02 with RES).
- **Property or building registers:** Dublin (rateable valuation list); Amsterdam
  and Rotterdam for shops (BAG shop-use units).
- **Permit lists:** Amsterdam's food layer (hospitality permits); Rotterdam's food
  layer, rebuilt from permit notices in the official gazette.
- **A food-premises licence register only:** Hong Kong (FEHD's registers, which
  license restaurants and food shops and nothing else a storefront needs).
- **Reason:** each country and city publishes what it publishes. The pages for
  Montréal, Mexico City, Guadalajara, Madrid and Barcelona already say their density
  is "not comparable" with licence-register cities.

### 2. Some maps have only two categories, and some have a thin one
**Reader sentence:** Most maps colour businesses as Retail, Food service and Personal
services. A few cannot, because the local records never cover that trade.
- **No Personal services at all:** Philadelphia, Boston.
- **No Retail or Personal services at all:** Hong Kong. Its three categories are
  Food service, Food shops and Bathhouses, because FEHD licenses nothing else.
- **Retail limited to food retail (plus a few extras):** Philadelphia (bodegas and
  big-box stores that sell packaged food), Boston (grocers, package stores, cannabis).
- **Retail thin:** New York (food stores plus a regulated slice of trades). Toronto:
  Retail is only the regulated trades (second-hand, pawn, smoke/vape, pet shops,
  fireworks), 328 pins inside the rings against 6,461 Food service.
- **Retail and Personal services merged into "Shops and services":** Amsterdam,
  Rotterdam. The building register records a unit's intended use, not its trade.
- **Reason:** the city does not license that trade, or the source cannot tell the two
  apart. It is a gap in the data, not a choice about what to show.

### 3. A few maps include suburban rail, most do not
**Reader sentence:** Commuter and suburban trains are left off except where, inside
the city, they run like a metro: stations about a kilometre apart, frequent trains,
and districts no metro reaches.
- **Included:** Dublin (DART), Copenhagen (S-tog, 7 lines), Rome (the Roma–Viterbo
  line's urban section), São Paulo (CPTM Linha 9), Rio de Janeiro (SuperVia's Deodoro
  and Saracuruna lines).
- **Excluded by name:** BART and Caltrain, Metra, Metrolink, Coaster/Sprinter, SEPTA
  Regional Rail, MBTA Commuter Rail, Tri-Rail, GO Transit, West Coast Express,
  Cercanías, Milan's Passante and Trenord, Iarnród Éireann Commuter/InterCity, RER and
  Transilien, the TER around Marseille, CPTM Linhas 7, 8 and 10–13, SuperVia's other
  three lines, Fortaleza's and Recife's diesel lines.
- **Not mentioned either way:** Montréal (REM, exo), Mexico City (Tren Suburbano).
- **Reason:** a spacing, frequency and coverage test, applied line by line (EC
  "Which stations these maps are drawn around").

### 4. Trams are on some maps and not others
**Reader sentence:** Trams and light rail are drawn where they are the city's rapid
transit, or where they reach areas the metro does not. They are left off where they
run on top of a metro network.
- **Trams or light rail drawn:** San Diego, San Francisco (Muni Metro), Los Angeles,
  Philadelphia (trolleys), Boston (Green Line, Mattapan), Calgary, Edmonton, Toronto
  (Lines 5 and 6 only), Mexico City (Tren Ligero), Guadalajara, Dublin (Luas),
  Marseille, Toulouse, Lille, Oslo, Amsterdam, Rotterdam, Rio (VLT), Santos (VLT),
  Hong Kong (Light Rail).
- **Trams not drawn:** Hong Kong Tramways (it runs beside the Island Line), Toronto's 18 streetcar routes, Milan (17 routes), Barcelona,
  Paris, Prague, Rome, Madrid (Metro Ligero), Copenhagen (the Letbane has no stop in
  scope).
- **Other modes on the map:** Toulouse's Téléo cable car, Barcelona's two
  funiculars, São Paulo's Linha 15 monorail, Miami's Metromover (automated people
  mover).
- **Reason:** "is the tram the rapid-transit system, or an overlay on one?", later
  widened to "does it serve corridors the metro does not?" (DEC, Oslo and Rotterdam
  entries). See Open questions 9 and 10: the stated reasons differ between cities.

### 5. Some maps cover one city, others a whole region
**Reader sentence:** Most maps stop at the city boundary, and the stations beyond it
are drawn on the line but get no ring. Some cover several municipalities because one
register covers them all, or because the rail network only makes sense that way.
- **Labelled "(Regional)":** Miami (Miami-Dade County), Vancouver (with Surrey),
  Guadalajara (4 municipios), Lille (11 communes), Fortaleza (4), Porto Alegre (6),
  Recife (4), Santos (with São Vicente).
- **Cover more than one municipality but are not labelled:** Montréal (the
  agglomeration: 19 boroughs and 15 related municipalities), Dublin (four local
  authorities), Copenhagen (with Frederiksberg).
- **Regional maps that count a municipality with no station:** Fortaleza (Caucaia),
  Recife (Cabo de Santo Agostinho). Guadalajara leaves out Tonalá for having none.
- **Lose the most stations to the boundary:** Paris (76), Copenhagen (59), Washington
  D.C. (58), Los Angeles (54), Rotterdam (52), Barcelona (50), Madrid (49), Boston (43).
- **Reason:** a register covers one jurisdiction, so rings outside it would read as
  empty. The French cities keep to the commune so that they stay comparable with one
  another, although SIRENE covers the neighbouring communes too.

### 6. The rings are half the size in seven cities, so ring counts do not compare
**Reader sentence:** In cities where stations are very close together, the rings are
drawn at half size, so the pin counts in the layer menu cover a smaller area than in
other cities.
- **Rings 0.05 / 0.1 / 0.2 / 0.3 mi:** New York, Paris, Marseille, Toulouse, Lille,
  Rennes, Oslo.
- **Rings 0.1 / 0.2 / 0.3 / 0.6 mi:** every other city.
- **Reason:** where stations are a median 340–540 m apart, a 0.6 mi ring reaches past
  the next stations (city configs, `RING_EDGES_MILES`).

### 7. The share of storefronts near a station ranges from about one in eight to nearly all
**Reader sentence:** On some maps nearly every shop is inside a station ring; on
others most of the city is beyond walking distance of the network. That depends on
how far the network reaches, not on the data.
- **90% or more inside the rings:** Barcelona 100%, Paris 97%, Amsterdam 96%, Madrid
  94%, Copenhagen 94%, Rotterdam 93%.
- **Under 25%:** Miami 13%, Brasília 14%, Fortaleza 14%, Belo Horizonte 18%, Salvador
  19%, Porto Alegre 20%, Edmonton 22%, São Paulo 23%, Recife 23%, Los Angeles 24%,
  San Diego 24%.
- **Cannot be measured on the map:** Mexico City and Guadalajara, which have no
  whole-city layer (EC gives Mexico City as 133,362 of 283,345, about 47%).
- **Reason:** network extent against the area in scope. Share = in-ring heat points ÷
  all-storefront heat points in each committed map.

### 8. Some maps show no business names
**Reader sentence:** On some maps a dot shows an address or a type of business rather
than a name, either because the source records no names or to avoid showing a person's
name at their home.
- **No names at all:** Dublin (address and recorded use), Rome (activity and address),
  Rotterdam.
- **Mostly addresses:** Milan (a shop sign on about 1 pin in 7), Amsterdam's shop
  layer, the French cities where SIRENE has no sign or usual name (only about 40% of
  Paris rows and 43% of Marseille rows are named, per the Marseille brief).
- **Address in place of a sole trader's name:** Oslo, Copenhagen, Prague.
- **Brazil:** the census enumerator's description, not a trade name; only the category
  where the address is also a home (35–69% of dots, by city).
- **Type in place of a personal name:** Vancouver/Surrey (88 pins).
- **Reason:** the source has no name column, or a privacy rule.

### 9. The data dates from different years, and not every page says when
**Reader sentence:** Most maps were built from data downloaded in September 2026, but
a few sources are older: a 2022 census, a 2022 street survey, a July 2025 register.
- **Older as-of dates:** the nine Brazilian cities (2022 census fieldwork), Barcelona
  (2022 survey; the 2024 survey is incomplete), Montréal (2025 survey), Rome (July
  2025 file, the newest published), Prague (establishments as of 2026-08-31).
- **Date of the business data shown on the page:** Barcelona, Copenhagen, Prague,
  Amsterdam, Rome, the Brazilian cities, Rotterdam.
- **Only the transit date shown:** Paris, Marseille, Toulouse, Lille, Rennes, Oslo.
- **No date shown:** the nine US cities, the five Canadian, the two Mexican, Madrid,
  Dublin, Milan.
- **Reason:** what each source publishes. France's licence requires a snapshot date,
  so the French pages show one for the rail data.

### 10. Some maps undercount and some overcount, in known directions
**Reader sentence:** Every source misses some shops or includes some that are not
really shopfronts. Several pages say which way their map leans.
- **Undercounts:** Brazil (a third to a half of plausible storefronts have
  descriptions no rule can read; Porto Alegre is worst near the stations); France
  (INSEE withholds 8.5% of Paris's establishments and 16.6–20.2% of Toulouse's,
  Lille's and Rennes's); Vancouver (1,583 licences with a real address but no
  coordinates);
  Madrid (9.2% have a zero coordinate); Toronto (6.2% unmatched addresses); Rome
  (4.3% unmatched); Prague (about 57,000 establishments whose owner's main activity is
  something else); Miami (repair and service premises); Mexico City and Guadalajara
  (street stalls); Copenhagen (tattoo studios); Chicago (licences with no
  coordinates).
- **Overcounts, or best read as upper bounds:** Milan (the six registers are not
  merged, so a business can count twice); Rome and Rotterdam (no closing dates, or a
  five-year permit window); the SIRENE, Oslo, Copenhagen and Prague registers
  (registered premises that may have no shopfront, including web shops); Edmonton
  (about 1 in 16 Personal services pins is a clinic); Amsterdam and Rotterdam (empty
  shop units cannot be removed).
- **Undisclosed on the city page:** San Francisco (only about 37% of rows carry a
  NAICS code) and Los Angeles (about 9% carry none), so both are floors. San Diego
  undercounts neighbourhoods registered under their own name. All three are open
  `PLAN.md` items.
- **Reason:** how each source is compiled.

### 11. What falls inside a category differs at the edges
**Reader sentence:** The three categories are meant to mean the same thing
everywhere, but a few businesses land differently depending on how a country
classifies or licenses them.
- **Car dealers:** counted as Retail in the NAICS cities, Mexico, Madrid, Oslo,
  Copenhagen and Miami. Not counted in France: NAF puts them in division 45, and
  `france_naf.py` keys on 47, 56 and 96 only.
- **Massage:** a Personal service in Calgary and Edmonton, where Alberta does not
  regulate it, and in Toronto's non-registered "holistic centres"; excluded as health
  care in Vancouver/Surrey, where British Columbia regulates it.
- **Adult premises:** body-rub and similar premises are excluded on sensitivity in
  Calgary, Edmonton, Toronto and Vancouver. UNKNOWN for other cities.
- **Street stalls:** excluded in Mexico City and Guadalajara; market-stall trading is
  excluded by code in France.
- **Web shops:** excluded by code in France; cannot be excluded in Oslo, Copenhagen or
  Prague.
- **One premises with several licences:** counted once almost everywhere; counted
  twice in Milan; and in Calgary a premises with both retail and food licences counts
  as Food.
- **Legend labels:** show code prefixes in the NAICS, SCIAN, NAF, SN2025, DB25 and
  CZ-NACE cities ("Retail — NAICS Code: 44/45", "Retail - NAF 47"); plain names
  in the cities with a local taxonomy.
- **Reason:** national classifications and provincial or state regulation.

### 12. Mexico City and Guadalajara have no whole-city heat layer
**Reader sentence:** On every other map you can switch on a heat layer of all the
city's storefronts; on these two, the heat layer covers only businesses near a
station.
- **Cities:** Mexico City, Guadalajara.
- **Reason:** file size. Mexico City's layer would have carried 283,345 points, and
  dropping it took the file from 25.7 MB to 19.0 MB (EC, Mexico City section).

---

## City by city

In-ring pins are the per-category counts in each map's layer menu (inside the rings
only). "Out / thinned" is taken from `outputs/<slug>/excluded_stations.csv`: stations
left out as outside the scope / surface stops dropped by the spacing filter.

### A. Rail (dimensions 1–3)

| City | Drawn | Notably not drawn | Rail source | Station scope | Out / thinned |
|---|---|---|---|---|---|
| **United States** | | | | | |
| San Diego | Trolley (light rail), 5 lines | Coaster, Sprinter | MTS GTFS | City | 16 / 0 |
| San Francisco | Muni Metro J K L M N T | BART, Caltrain, F Market, cable cars | SFMTA GTFS (mirror) | City and County | 0 / 65 |
| Los Angeles | Metro Rail A B C D E K (heavy + light) | Metrolink | LA Metro rail GTFS | City | 54 / 0 |
| Chicago | 'L', 7 lines | Metra; Yellow Line | CTA GTFS | City | 18 / 0 |
| New York | Subway (11 trunk groups) + Staten Island Rwy | LIRR | MTA GTFS | Five boroughs | 0 / 0 |
| Philadelphia | MFL, BSL + subway-surface and Girard trolleys | Regional Rail; NHSL, Media–Sharon Hill (outside city) | SEPTA GTFS | City | 6 / 161 |
| Miami (Regional) | Metrorail + 2 Metromover loops | Tri-Rail; MIA people mover | Miami-Dade Transit GTFS | County (6 municipalities have stations) | 0 / 0 |
| Boston | Red, Orange, Blue + Green, Mattapan | Commuter Rail, ferries | MBTA GTFS | City | 43 / 25 |
| Washington D.C. | Metrorail, 6 lines | — (MARC/VRE are separate systems) | WMATA GTFS (API key) | District | 58 / 0 |
| **Canada** | | | | | |
| Vancouver (Regional) | SkyTrain Expo, Millennium, Canada | West Coast Express, SeaBus | TransLink GTFS | Vancouver + Surrey | 30 / 0 |
| Montréal | Métro, 4 lines | not stated (REM, exo) | STM GTFS | Agglomeration (island) | 4 / 0 |
| Calgary | CTrain Red, Blue (light rail) | — | Calgary Transit GTFS | City | 0 / 0 |
| Edmonton | LRT Capital, Metro, Valley | 3 non-revenue stops | ETS GTFS | City | 0 / 0 |
| Toronto | Subway 1, 2, 4 + LRT 5, 6 | 18 streetcar routes; GO | TTC GTFS (City CKAN) | City | 2 / 0 |
| **Mexico** | | | | | |
| Mexico City | Metro, 12 lines + Tren Ligero | not stated (Tren Suburbano, Cablebús) | OpenStreetMap | CDMX | 10 / 0 |
| Guadalajara (Regional) | Tren Ligero L1–L4 | — | OpenStreetMap (only GTFS expired 2023, lacks L4) | 4 municipios; Tonalá out | no CSV (all in scope) / 0 |
| **Spain** | | | | | |
| Madrid | Metro L1–L12 + Ramal | Cercanías; Metro Ligero | CRTM ArcGIS layers | Municipio | 49 / 0 |
| Barcelona | Metro L1–L12 (TMB+FGC) + 2 funiculars | Trams | OpenStreetMap | Municipi | 50 / 0 |
| **Ireland** | | | | | |
| Dublin | Luas Red, Green + DART | Commuter, InterCity | NTA national GTFS | 4 local authorities | 2 / 0 |
| **Italy** | | | | | |
| Milan | Metro M1–M5 | 17 trams; Passante, Trenord | ATM GIS layers (+GTFS colours) | Comune | 21 / 0 |
| Rome | Metro A, B, B1, C + Roma–Viterbo (urban) | Trams; Roma–Lido; suburban | OpenStreetMap | Comune | 1 / 0 |
| **France** | | | | | |
| Paris | Métro, 16 lines | RER, Transilien, trams | IDFM GTFS | Commune | 76 / 0 |
| Marseille | Métro 1–2 + Tramway 1–3 | TER; ferries; Aubagne tram | Métropole AMP GTFS (RTM) | Commune | 7 (Aubagne tram) / 0 |
| Toulouse | Métro A–B + Tram T1 + Téléo cable car | — | Tisséo GTFS | Commune | 14 / 0 |
| Lille (Regional) | Métro 1–2 + Tram R, T | heritage tram, disused line | MEL GIS + OpenStreetMap (métro lines) | 11 communes | no CSV (none lost) / 0 |
| Rennes | Métro a, b | — | STAR GTFS | Commune | 4 / 0 |
| **Norway** | | | | | |
| Oslo | T-bane 1–5 + trams 12, 13, 15, 17, 18, 19 | Ferries | Ruter via Entur GTFS | Kommune | 12 / 0 |
| **Denmark** | | | | | |
| Copenhagen | Metro M1–M4 + S-tog (7 lines) | Regional/InterCity; Letbane | OpenStreetMap | Copenhagen + Frederiksberg | 59 / 0 |
| **Czechia** | | | | | |
| Prague | Metro A, B, C | Trams, funicular, ferries, suburban | PID GTFS | City | 0 / 0 |
| **Netherlands** | | | | | |
| Amsterdam | Metro 50–54 + 16 trams | Tram 3, museum tram, ferries, NS | OVapi national GTFS (GVB) | Gemeente (with Weesp) | 22 / 59 |
| Rotterdam | RET metro A–E + 9 trams | Trams 12, 14, 18; ferries; NS | OVapi national GTFS (RET) | Gemeente | 52 / 23 |
| **Brazil** | | | | | |
| São Paulo | Metrô L1–5, L15 (monorail) + CPTM L9 | CPTM 7, 8, 10–13; L6, L17 (building) | OpenStreetMap (GeoSampa for status) | Município | 2 / 0 |
| Rio de Janeiro | MetrôRio 1, 2, 4 + VLT (4) + SuperVia Deodoro, Saracuruna | Other SuperVia lines; Santa Teresa tram; Corcovado | DATA.RIO (metro) + OpenStreetMap | Município | 3 / 0 |
| Belo Horizonte | Metrô L1, L2 | Vitória-Minas (intercity) | OpenStreetMap | Município | 2 / 0 |
| Brasília | Metrô Verde, Laranja | 2 stations under construction | OpenStreetMap (IPEDF for status) | Federal District | 0 / 0 |
| Salvador | Metrô L1, L2 | — | OpenStreetMap | Município | 1 / 0 |
| Fortaleza (Regional) | Metrofor Linha Sul | 3 diesel lines | OpenStreetMap | 4 municípios | 0 / 0 |
| Porto Alegre (Regional) | Trensurb Linha 1 | Aeromóvel | OpenStreetMap | 6 municípios | 0 / 0 |
| Recife (Regional) | Metrô Centro (2 branches) + Sul | 2 diesel VLTs | OpenStreetMap | 4 municípios | 0 / 0 |
| Santos (Regional) | VLT L1, L2 | Heritage tram | OpenStreetMap | Santos + São Vicente | 0 / 0 |
| **Hong Kong** | | | | | |
| Hong Kong | MTR, 8 lines + Light Rail | Airport Express, Disneyland Resort Line, high-speed rail, Peak Tram, Hong Kong Tramways | OpenStreetMap (station counts checked against MTR's own lists) | Territory | 0 / 17 (Racecourse left out: race days only) |

### B. Business data (dimensions 4–6)

| City | Source kind | Source | Classification | In-ring pins R / F / P | Missing or thin |
|---|---|---|---|---|---|
| **United States** | | | | | |
| San Diego | Tax register | Business Tax Certificates | NAICS | 1,079 / 655 / 843 | Undercount: neighbourhoods registered under own name (PLAN) |
| San Francisco | Licence register | Registered Business Locations | NAICS | 4,855 / 5,403 / 2,118 | Floor: about 37% of rows have NAICS (DEC) |
| Los Angeles | Tax register | Listing of Active Businesses | NAICS | 8,069 / 3,922 / 2,028 | Floor: about 9% of rows lack NAICS (DEC) |
| Chicago | Licence register | Business Licenses | Own licence types | 5,461 / 4,196 / 2,139 | — |
| New York | 4 activity registers | DOHMH, NYS food stores, NYS salons, DCWP | Per-source dispatch | 14,822 / 22,060 / 7,478 | Retail thin |
| Philadelphia | Licence register (activities) | L&I Business Licenses | Own licence types | 780 / 4,174 / — | No Personal services; Retail = food retail |
| Miami (Regional) | Tax register | Local Business Tax (county) | Own CATGRYNAME (NAICS column empty) | 1,960 / 1,254 / 561 | Repair and service premises under-counted |
| Boston | 3 activity registers | Food inspections, Licensing Board, cannabis | Per-source dispatch | 530 / 1,880 / — | No Personal services; Retail = food, package, cannabis |
| Washington D.C. | Licence register | Basic Business License | Own BUSINESSACTIVITY | 897 / 2,603 / 360 | "Delicatessen" (1,065) ambiguous, counted as Food |
| **Canada** | | | | | |
| Vancouver (Regional) | 2 licence registers | Vancouver licences; Surrey directory | Own types (both) | 1,847 / 1,867 / 954 | — |
| Montréal | Street survey | Locaux commerciaux (annual) | NAICS (SCIAN = NAICS) | 4,481 / 3,856 / 1,396 | Edge municipalities thinner in the survey |
| Calgary | Licence register | Business Licences | Own licencetypes | 1,977 / 2,869 / 1,325 | Food over Retail (dual-licence rule) |
| Edmonton | Licence register | Business Licences | Own licence categories | 1,034 / 922 / 416 | Personal services overstated (clinics) |
| Toronto | Licence register | MLS licences | Own MLS category | 328 / 6,461 / 1,950 | Retail = regulated slice only |
| **Mexico** | | | | | |
| Mexico City | National statistical register | INEGI DENUE | SCIAN | 94,642 / 24,938 / 13,782 | Street stalls excluded |
| Guadalajara (Regional) | National statistical register | INEGI DENUE | SCIAN | 26,341 / 6,723 / 3,861 | Street stalls excluded |
| **Spain** | | | | | |
| Madrid | Premises census | Censo de locales | Own epígrafe | 26,109 / 16,151 / 8,032 | — |
| Barcelona | Street survey (2022) | Cens de locals en planta baixa | Own 4-level scheme (finest level) | 20,287 / 9,976 / 5,673 | 458 mixed retail/wholesale rows dropped |
| **Ireland** | | | | | |
| Dublin | Property register | Rateable valuation list | Register's own "Uses" | 5,338 / 1,703 / 554 | — |
| **Italy** | | | | | |
| Milan | 6 licence registers | Comune di Milano premises registers | Register = category | 24,793 / 11,738 / 4,979 | Canteens and clubs partly left in Food |
| Rome | Authorisation register | SUAP | Own authorisation types | 32,915 / 12,690 / 7,290 | Workshops with no trade missing |
| **France** | | | | | |
| Paris | National establishment register | SIRENE + INSEE geolocation | NAF rév. 2 (sous-classe) | 40,233 / 32,281 / 11,611 | — |
| Marseille | same | same | same | 4,558 / 3,852 / 1,603 | — |
| Toulouse | same | same | same | 2,438 / 2,162 / 953 | — |
| Lille (Regional) | same | same | same | 3,166 / 2,942 / 1,097 | — |
| Rennes | same | same | same | 1,105 / 906 / 354 | — |
| **Norway** | | | | | |
| Oslo | National establishment register | Enhetsregisteret sub-units | SN2025 (NACE Rev. 2.1) | 4,197 / 2,082 / 1,828 | — |
| **Denmark** | | | | | |
| Copenhagen | National establishment register | CVR production units | DB25 (NACE Rev. 2.1) | 7,061 / 4,333 / 2,760 | Tattoo studios lost with the catch-all |
| **Czechia** | | | | | |
| Prague | National registers (location + activity) | ROS02 + RES | CZ-NACE 2025 (owner's activity) | 6,027 / 5,464 / 6,157 | About 57,000 establishments of other-activity owners missing |
| **Netherlands** | | | | | |
| Amsterdam | Permit list + building register | Horeca permits; BAG shop units | Per-source (2 buckets) | Shops & services 9,215 / Food 3,433 | Retail and Personal merged |
| Rotterdam | Gazette notices + building register | Permit notices; BAG shop units | Per-source (2 buckets) | Shops & services 5,211 / Food 1,771 | Retail and Personal merged |
| **Brazil** (all nine) | Census of addresses (2022) | IBGE CNEFE | Free-text keyword rules | see below | A third to a half of plausible storefronts unreadable |
| São Paulo | | | | 25,969 / 15,331 / 8,291 | about 1/3 unreadable |
| Rio de Janeiro | | | | 15,085 / 10,364 / 4,820 | about 1/3 |
| Belo Horizonte | | | | 4,634 / 2,355 / 1,439 | about 4 in 10 |
| Brasília | | | | 2,808 / 1,246 / 1,012 | about 4 in 10 |
| Salvador | | | | 5,131 / 3,312 / 1,625 | about 1/3 |
| Fortaleza (Regional) | | | | 5,255 / 1,964 / 1,324 | about 4 in 10 |
| Porto Alegre (Regional) | | | | 4,660 / 1,516 / 1,244 | almost half; about half near stations |
| Recife (Regional) | | | | 6,547 / 2,058 / 1,783 | about 4 in 10 |
| Santos (Regional) | | | | 3,113 / 1,482 / 792 | almost 4 in 10 |
| **Hong Kong** | | | | | |
| Hong Kong | Licence registers (food premises) | FEHD licence registers | Local (licence type) | Food service 15,833 / Food shops 3,408 / Bathhouses 34 | No general retail or personal services: FEHD does not license them |

### C. Location, coverage and city-specific exclusions (dimensions 7–9)

| City | Location method (rate) | Coverage gaps disclosed | City-specific exclusions (privacy / other) |
|---|---|---|---|
| **United States** | | | |
| San Diego | Source coordinates (98.4% populated) | None on page | Nonstore 454, parking (project-wide) |
| San Francisco | Source point | Surface stops thinned | 812990 "solo massage" |
| Los Angeles | Source + Census geocoder for corrupt points (98.7% recovered) | Corrupt coordinates geocoded | 812990 catch-all (30.7% of storefronts) |
| Chicago | Source coordinates | Licences without coordinates left off | Home-based, peddlers, endorsements, Limited Business |
| New York | Source + Census geocoder (582 of 1,449 recovered; 1.4% lost) | Retail thin; possible double counts | Person-held licences, contractors, chair renters |
| Philadelphia | Source geometry | Newsstands mostly absent | Rental (79% of register), short-let hosts |
| Miami (Regional) | Source coordinates | Repair/service undercount | SERVICE BUSINESS, professional, apartments, LAUNDRY MACHINE |
| Boston | Source coordinates (state plane) | Residence check reads zero by construction | Dormitories, lodging, Common Victualler (counted via food data) |
| Washington D.C. | Register X/Y + Census geocoder (387 of 451, 85.8%; 64 lost) | Delicatessen ambiguity | Residential rentals (61%), General Business, school cafeterias, caterers |
| **Canada** | | | |
| Vancouver (Regional) | Source coordinates | About half of Vancouver's register has none; 1,583 address rows lost | Surrey Home Occupation (51.8%), IMBL, RMT massage |
| Montréal | Source LAT/LONG (100%) | Two municipalities not surveyed | Vacant units (about 3,500) |
| Calgary | Source point | No home-business flag | Endorsements; body rub / escort (sensitivity) |
| Edmonton | Source coordinates | Personal services overstated | Non-commercial licence types (43%); adult services (sensitivity) |
| Toronto | Address join to One Address Repository (93.8%) | Retail absent; plazas under-counted | Cancelled licences; endorsements; person-held; adult premises (sensitivity) |
| **Mexico** | | | |
| Mexico City | Source coordinates (100%) | Street stalls not shown | Semifijo units, SCIAN 469, 812410 |
| Guadalajara (Regional) | Source coordinates | Street stalls not shown | Same as Mexico City; Tonalá |
| **Spain** | | | |
| Madrid | Source coordinates; 9.2% zero, dropped | 1 premises in 11 cannot be placed | Accommodation, wholesale, repair, no-shopfront |
| Barcelona | Source coordinates; zeros dropped (count UNKNOWN) | Survey is 2022 | Vacant units (1 in 9), hotels, 458 mixed rows |
| **Ireland** | | | |
| Dublin | Source coordinates (ITM) | Large areas with no rail | No names published at all |
| **Italy** | | | |
| Milan | Source coordinates (loss count UNKNOWN) | Canteens/clubs partly remain; double counts | Registers not merged |
| Rome | Address join to ANNCSU (95.7%) | Food an upper bound (no closing dates) | Online, wholesale, storage types; workshops with no trade |
| **France** | | | |
| Paris | Join to INSEE geolocation (99.96%) | 1.8× OSM shop count; INSEE masking 8.5% (EC) | 47.91/47.99/47.8x, 56.29, 96.01A, 96.09Z |
| Marseille | same (99.94%) | 2.6× OSM (1.7× on restaurants); masking 12.2% (brief, sample) | Same codes |
| Toulouse | same (99.93%) | Masking 20.2%; 14 stations out | Same codes |
| Lille (Regional) | same (99.98%) | Masking 16.6% | Same codes |
| Rennes | same (99.97%) | Masking 17.5% | Same codes |
| **Norway** | | | |
| Oslo | Address join to Matrikkelen (96.8%) | Web shops cannot be excluded | 8 no-premises codes, 96.990, bankrupt parents; sole-trader names withheld |
| **Denmark** | | | |
| Copenhagen | Address join to DAR (98.3%) | Tattoo studios lost; web shops | Same 8 kinds + laundries, 969900; personal owners' names withheld |
| **Czechia** | | | |
| Prague | Address join to RÚIAN (99.99%) | Owner's activity only; web shops | Home-address sole traders (1,500) dropped; names withheld |
| **Netherlands** | | | |
| Amsterdam | Source points (22 permits unplaced) | Empty shop units about 5%; takeaways thin | Shop units also dwellings (757); canteens in venues, hotels |
| Rotterdam | Source points | Closed premises stay up to 5 years; about 7% vacant | Dwelling units (26); alcohol, terrace, gaming permits |
| **Brazil** | | | |
| All nine | Source points (census) | Unreadable descriptions (see B); change since 2022 | Offices, parking, workshops, vacant, worship etc.; dwelling addresses show category only |
| **Hong Kong** | | | |
| Hong Kong | Source points: FEHD's own CSDI points, matched by licence number (28 unplaced) | Mostly restaurants; premises on different floors share one point | Food factories, canteens, cold stores, pools, entertainment and funeral trades; 2 duplicate licences counted once |

### D. Vintage and map features (dimensions 10–11, plus two added)

"Date on page": B = business data date shown, T = transit date only, — = none.
In-ring share = in-ring heat points ÷ all-storefront heat points.

| City | Business data as-of (fetched) | Date on page | Rings (outer) | Whole-city heat layer | In-ring share | Pin label |
|---|---|---|---|---|---|---|
| **United States** | | | | | | |
| San Diego | UNKNOWN (2026-09-18) | — | 0.6 mi | Yes | 24% | Trade name |
| San Francisco | UNKNOWN (≈2026-09-19) | — | 0.6 mi | Yes | 69% | Name |
| Los Angeles | UNKNOWN (≈2026-09-19) | — | 0.6 mi | Yes | 24% | Trade name, else registrant |
| Chicago | Active licences (2026-09-20) | — | 0.6 mi | Yes | 57% | Name |
| New York | UNKNOWN (2026-09-21) | — | 0.3 mi | Yes | 71% | Name |
| Philadelphia | Active licences (2026-09-21) | — | 0.6 mi | Yes | 58% | Trade name (from "LEGAL (TRADE)") |
| Miami (Regional) | Tax year 2026 (2026-09-21) | — | 0.6 mi | Yes | 13% | Name |
| Boston | UNKNOWN (2026-09-21) | — | 0.6 mi | Yes | 76% | Name |
| Washington D.C. | Active licences (2026-09-21) | — | 0.6 mi | Yes | 74% | Name |
| **Canada** | | | | | | |
| Vancouver (Regional) | Current-year licences (2026-09-21) | — | 0.6 mi | Yes | 40% | Name; type on 88 pins |
| Montréal | 2025 survey (2026-09-21) | — | 0.6 mi | Yes | 56% | Establishment name |
| Calgary | UNKNOWN (2026-09-21) | — | 0.6 mi | Yes | 41% | Trade name |
| Edmonton | UNKNOWN (2026-09-21) | — | 0.6 mi | Yes | 22% | Business name |
| Toronto | Current licences (2026-09-21) | — | 0.6 mi | Yes | 48% | Operating name |
| **Mexico** | | | | | | |
| Mexico City | UNKNOWN edition (2026-09-22) | — | 0.6 mi | **No** | — (about 47% per EC) | Shop sign |
| Guadalajara (Regional) | UNKNOWN edition (2026-09-22) | — | 0.6 mi | **No** | — | Shop sign |
| **Spain** | | | | | | |
| Madrid | Portal refreshed daily (2026-09-22) | — | 0.6 mi | Yes | 94% | Trade name |
| Barcelona | 2022 survey (2026-09-22) | B (prose) | 0.6 mi | Yes | 100% | Unit name |
| **Ireland** | | | | | | |
| Dublin | UNKNOWN (2026-09-22) | — | 0.6 mi | Yes | 58% | Address + use |
| **Italy** | | | | | | |
| Milan | UNKNOWN (2026-09-22) | — | 0.6 mi | Yes | 87% | Sign on about 1 in 7; else address |
| Rome | July 2025 (2026-09-24) | B | 0.6 mi | Yes | 53% | Activity + address |
| **France** | | | | | | |
| Paris | SIRENE monthly; month UNKNOWN (2026-09-22) | T | 0.3 mi | Yes | 97% | Sign/usual name (about 40%), else address |
| Marseille | same (2026-09-23) | T | 0.3 mi | Yes | 55% | same (43% named) |
| Toulouse | same (2026-09-23) | T | 0.3 mi | Yes | 64% | same (share UNKNOWN) |
| Lille (Regional) | same (2026-09-23) | T | 0.3 mi | Yes | 61% | same (share UNKNOWN) |
| Rennes | same (2026-09-23) | T | 0.3 mi | Yes | 68% | same (share UNKNOWN) |
| **Norway** | | | | | | |
| Oslo | UNKNOWN (2026-09-24) | T | 0.3 mi | Yes | 76% | Name; address for sole traders |
| **Denmark** | | | | | | |
| Copenhagen | Weekly extract (2026-09-24) | B | 0.6 mi | Yes | 94% | Name; address for personal owners |
| **Czechia** | | | | | | |
| Prague | 2026-08-31 (ROS02) | B | 0.6 mi | Yes | 70% | Name; address for persons/partnerships |
| **Netherlands** | | | | | | |
| Amsterdam | Live register (2026-09-24) | B | 0.6 mi | Yes | 96% | Permit name (food); address (shops) |
| Rotterdam | Notices to 2026-09-24 (5-yr window) | B | 0.6 mi | Yes | 93% | No names; address (shops) |
| **Brazil** | | | | | | |
| São Paulo | 2022 census (file 2024-05-20) | B | 0.6 mi | Yes | 23% | Enumerator's description; category only at homes (37%) |
| Rio de Janeiro | same | B | 0.6 mi | Yes | 28% | same (55%) |
| Belo Horizonte | same | B | 0.6 mi | Yes | 18% | same (36%) |
| Brasília | same | B | 0.6 mi | Yes | 14% | same (69%) |
| Salvador | same | B | 0.6 mi | Yes | 19% | same (56%) |
| Fortaleza (Regional) | same | B | 0.6 mi | Yes | 14% | same (54%) |
| Porto Alegre (Regional) | same | B | 0.6 mi | Yes | 20% | same (42%) |
| Recife (Regional) | same | B | 0.6 mi | Yes | 23% | same (44%) |
| Santos (Regional) | same | B | 0.6 mi | Yes | 46% | same (35%) |
| **Hong Kong** | | | | | | |
| Hong Kong | Registers generated 2026-09-25, points to 2026-09-23 (fetched 2026-09-25) | Yes (snapshot caption) | 0.6 mi | Yes | 91% | Shop sign, Chinese or English (308 show "No shop sign") |

Features every map shares, so not a difference: permanent line labels and a legend
entry for every line; rings start switched off; OSM basemap credit; the site-wide
notices footer (`app/components.py` `render_site_notices`). Required notices are
page-level, not on-map, and apply to every page.

**Line colours not the agency's** (a smaller visual difference): Miami (all
project-chosen), Edmonton (darkened), Toronto (Line 2 darkened), Oslo (two lightened;
tram 15 assigned), Copenhagen (A and F lightened), Prague (A lightened), Amsterdam
(5 tram lines adjusted), Rome (B1 lightened), Lille (Tram T darkened), Rio (a few
lightened), Rotterdam (trams 1 and 11 separated), Salvador (colours from line names;
OSM has none). Source: each page's prose.

---

## Open questions

Contradictions between files, and claims that have gone stale, which the owner
would need to settle before this becomes a page.

**Resolved 2026-09-24** (owner-approved wording, see DECISIONS): 1, 3, 4, 5, 6,
7 and 8. Also resolved: in 2, the ring wording in EC and on the New York page;
in 19, the stale "2026-09-21 rebuild" header and "the other four cities". The
rest of 2 (the NY config's "THE ONE CITY" comment) and everything from 9 on
remain open.

1. **The spacing filter "applies to three cities"** (EC, lines 118–121: SF,
   Philadelphia, Boston). Amsterdam (59 stops) and Rotterdam (23) now use it too,
   per their `excluded_stations.csv` and EC's own Amsterdam and Rotterdam sections.
2. **Ring sizes.** EC line 113 says the innermost ring is "a tenth of a mile in most
   cities and finer in New York"; `pipeline/new_york/config.py:131` says NY is "THE
   ONE CITY THAT DOES NOT USE THE SHARED EDGES". Six more cities (the five French and
   Oslo) now use the half-size edges. The NY page also calls the other cities' rings
   "half-mile rings", but their outer ring is 0.6 mi.
3. **Miami page:** "This is the only regional map here". DEC (around line 4916)
   records the superlative being converted to "the first regional map" elsewhere, but
   `app/pages/7_Miami_Heatmap.py` still says "only"; seven other maps are labelled
   (Regional).
4. **San Francisco page:** "commuter rail is left out of every city map on this
   site". Dublin, Copenhagen, Rome, São Paulo and Rio each draw a suburban line.
5. **Mexico City page:** "the one city here whose rail geometry does not come from its
   operator". Twelve other cities draw wholly from OpenStreetMap and two partly
   (Lille, Rio), per DS's transit tables.
6. **Dublin page and EC (Dublin section):** "the one city here that names no
   businesses". Rome and Rotterdam also show no business names (EC, their sections).
7. **Paris page:** "seven maps on this site do draw light rail". DEC's 2026-09-23
   correction counted seven then; since then Oslo, Amsterdam, Rotterdam, Rio (VLT)
   and Santos (VLT) have added trams. The current count depends on a definition that
   is not written down.
8. **New York page:** "unlike the other cities here, the network does not leave its
   own city". Calgary, Edmonton, Prague, Brasília, Miami, Lille and others also lose
   no station to a boundary.
9. **When a map is labelled "(Regional)".** Vancouver's reasoning (DEC around line
   15422: "a map spanning two municipalities cannot honestly be called Vancouver")
   would also cover Copenhagen (with Frederiksberg), Dublin (four local authorities)
   and Montréal (an agglomeration of 15 municipalities and 19 boroughs). None is
   labelled; Santos, with two municipalities, is. Also, DEC (around line 1099) says
   the regional pages drop "(Regional)" from their headings, but Lille's heading
   includes it.
10. **The tram test.** EC (lines 59–70) states only "the rapid-transit system or an
    overlay on one". The Oslo and Rotterdam decisions add "serves corridors the metro
    does not". Toronto's page excludes the streetcars because they "run in traffic
    every block or two", which is the problem Amsterdam and Rotterdam solve with the
    spacing filter. Should one sentence govern all three?
11. **Madrid's Metro Ligero** is left out "so the city ships one agency's rail
    system" (`pipeline/madrid/config.py:92–96`). That is not the tram test, and it
    appears neither on the Madrid page nor in EC.
12. **Cable cars and unmentioned systems.** Toulouse establishes that "cable car" is
    not a reason to exclude. Mexico City's Cablebús and Tren Suburbano, and
    Montréal's REM and exo, are not mentioned in any file read. Unknown whether they
    were considered.
13. **Undisclosed floors in the first US cities.** San Francisco (about 37% of rows
    have NAICS) and Los Angeles (about 9% have none), from DEC's 2026-09-18/19
    entries, and San Diego's neighbourhood undercount (La Jolla). All three are open
    in `PLAN.md` (around lines 1675–1682) and absent from the pages. It is also
    unknown whether the SF and LA figures still hold after later rebuilds.
14. **Car dealers.** `madrid_epigrafe.py:60` and `norway_sn2025.py:17` justify
    counting car dealers because "every other city in this project already counts a
    car dealer as retail". `france_naf.py` maps division 47 only, so the five French
    cities do not (NAF puts car sales in 45). Either the justification or the French
    mapping needs a note.
15. **Adult-premises exclusions** are recorded for Calgary, Edmonton, Toronto and
    Vancouver. No file says whether the NAICS, SIRENE, NACE or CNEFE cities contain
    or exclude comparable premises.
16. **INSEE masking shares are uneven on the pages.** Toulouse, Lille and Rennes state
    theirs; the Paris and Marseille pages do not. Marseille's only figure (12.2%) comes
    from a partial sample in `docs/build_briefs/marseille.md`.
17. **French pins that show an address.** `france_register.py:251–255` falls back to
    the address when SIRENE has no sign or usual name (about 60% of Paris rows, per the
    Marseille brief). No French page says so, while the Oslo, Copenhagen, Prague,
    Milan and Amsterdam pages do explain their address-only pins.
18. **Toronto's retail share:** EC gives 870 of 19,575 storefront rows (4.4%);
    `pipeline/taxonomies/__init__.py` gives 4.2%. **Measured 2026-09-24: both
    are real, from two stages of one build.** `outputs/toronto/baseline.json`
    records buckets 870 / 14,408 / 4,297 (summing to EC's 19,575), while
    `businesses_clean.csv`, which the map is drawn from, has 19,384 rows
    classifying as 814 / 14,289 / 4,281 (4.2%). Which figure the page should
    quote depends on where step 2 counts its buckets; to be settled by reading
    Toronto's step 2, not by editing either number.
19. **Stale counts in EC:** the header says "Business counts are from the 2026-09-21
    rebuild", but more than half the cities were built from 2026-09-22 to 09-24; line
    1540 compares New York with "the other four cities".
20. **Data dates on pages.** Nineteen pages show no date for their business data
    (theme 9). Is a uniform "data as of" line wanted? Several sources' own as-of dates
    are not recorded anywhere read: the DENUE edition, the SIRENE release month,
    Dublin's valuation list date, Milan's registers.
21. **Guadalajara and Lille have no `excluded_stations.csv`.** They carry
    `station_municipios.csv` and `served_communes.csv` instead. Check that the
    generated station table on the "What is excluded" page renders them rather than
    showing an empty row (CLAUDE.md's `check_scope_disclosure.py` invariant).

---

## Evidence notes

- **Theme 1 (source kinds):** DS "Business registries" table (lines 66–127); EC city
  sections; pages 11, 15, 16, 17, 18 ("not comparable").
- **Theme 2 (missing buckets):** EC "What is missing rather than excluded" (lines
  1521–1650); pages 5, 6, 8, 14, 29, 40; legend rows and layer counts in each
  `heatmap.html`.
- **Theme 3 (commuter rail):** EC lines 48–88; pages 2, 19, 27, 30, 31, 32, 36, 38;
  EC Rome, São Paulo and Rio sections.
- **Theme 4 (trams):** EC lines 59–70; DEC "Owner's calls: Oslo kommune only, trams
  drawn" (around line 3438) and the Rotterdam rail entry (around line 681); pages 14,
  20, 21, 23, 26, 29, 40; `pipeline/madrid/config.py:92–96`;
  `pipeline/barcelona/config.py:140–141`.
- **Theme 5 (scope):** `app/cities.py` names; EC lines 96–111; every
  `outputs/*/excluded_stations.csv` (reason columns tallied); pages 7, 10, 11, 16, 19,
  24, 27, 36–39.
- **Theme 6 (rings):** `RING_EDGES_MILES` in each `pipeline/<slug>/config.py`
  (reasoning at paris:159, marseille:125, toulouse:137, lille:157, rennes:138,
  oslo:89, new_york:130); layer names in each `heatmap.html`.
- **Theme 7 (in-ring share):** HeatMap point arrays in each `heatmap.html`; matches
  page statements where given (e.g. Copenhagen "nineteen in twenty" = 94%, São Paulo
  "one in five" = 23%).
- **Theme 8 (names):** EC Dublin, Rome, Rotterdam, Oslo, Copenhagen, Prague and Brazil
  sections; `pipeline/countries/france_register.py:251–255`;
  `docs/build_briefs/marseille.md` (named 43.4%, Paris 39.6%);
  `pipeline/countries/brazil_register.py:136`; page 20 (Milan); EC "Honest limits"
  (Vancouver 88 pins).
- **Theme 9 (vintage):** DS "Retrieved" column; `outputs/*/provenance.json`;
  `pipeline/rome/config.py:39`; `pipeline/montreal/config.py:55`;
  `pipeline/countries/france.py:44–45`; page captions (the `_bits` in pages 28–40;
  transit captions in 21–26).
- **Theme 10 (under/over counts):** EC sections for Brazil, France, Madrid, Toronto,
  Rome, Prague, Miami, Mexico, Copenhagen, Milan and Edmonton; EC line 1543
  (Vancouver); DEC around line 19480 (SF) and around 19229 (LA); `PLAN.md` around
  lines 1675–1682.
- **Theme 11 (category edges):** `pipeline/taxonomies/france_naf.py:223–273`;
  `madrid_epigrafe.py:58–65`; `norway_sn2025.py:15–18`; EC Vancouver, Calgary,
  Edmonton and Toronto sections; legend rows in each `heatmap.html`.
- **Theme 12 (whole-city layer):** `all_city_heat=False` in
  `pipeline/mexico_city/step3_map.py:93` and `pipeline/guadalajara/step3_map.py:71`;
  EC lines 848–853.
- **Location rates:** DS Business registries rows (Toronto, Paris to Rennes, Oslo,
  Copenhagen, Prague, Rome); DEC around 18511 (LA), 16168 (D.C.), 18345 (NY), 19528
  (SD); the city configs' coordinate comments (Montréal, Calgary, Dublin, Madrid).
