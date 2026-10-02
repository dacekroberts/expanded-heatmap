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
counts cover pins **inside the rings only**, per `pipeline/map_common.py` `add_pin_layer()`),
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
  Chicago, Philadelphia, Miami, Washington D.C., Sacramento, Houston (state sales-tax permits), Vancouver/Surrey, Calgary, Edmonton,
  Toronto, Milan (six premises registers), Rome (SUAP authorisations).
- **Assembled from several activity-specific registers:** New York (4), Boston (3), Buffalo (3),
  and the Korean permit registers: Seoul (17 types), Daegu (14), Busan (14). The
  Japanese cities too: Kobe, Osaka, Sapporo, Fukuoka and Kyoto each join the city's
  food-permit list to its barber, beauty-salon and laundry registers (4; Sapporo 5,
  with coin laundries). Fukuoka adds MHLW's national online food filings, because
  the city's own list holds only permits from before June 2021; Kyoto's food list
  is rebuilt from its 2021 list and every monthly list since. Tokyo has no
  city-wide list: each of the 23 wards publishes its own list or none, and eight
  are used (eight food lists, MHLW's filings added for four of them, and the
  barber, beauty and laundry registers of four), so the other fifteen have no data
  at all.
- **Street surveys or censuses of premises:** Montréal, Madrid, Barcelona, the
  nine Brazilian cities (IBGE's 2022 census walk), Buenos Aires (the city's
  2022–2024 land-use survey, every ground floor on every block), Sydney (the City of
  Sydney's 2022 floor-space survey, one council only) and Melbourne (the City
  of Melbourne's 2024 land-use census, one council only).
- **National statistical or establishment registers:** Incheon, Goyang, Seongnam,
  Yongin, Suwon and Bucheon (SEMAS's national storefront register, 상가(상권)정보), Mexico City, Guadalajara and
  Monterrey (INEGI DENUE), the five French cities (SIRENE), Oslo and Bergen (Enhetsregisteret sub-units),
  Copenhagen and Aarhus (CVR production units), Prague (ROS02 with RES); Taichung, Taoyuan
  and Taipei (the national business tax register, FIA).
- **Excise licences plus a cadastre:** Riga (VID's alcohol and tobacco licences for
  food; VZD's premise groups for shops and services).
- **A food hygiene register:** London and Newcastle (Regional) (the Food Standards
  Agency's FHRS), every food premises a borough or council inspects, and nothing
  else; Glasgow the same on Scotland's scheme (Food Standards Scotland's FHIS),
  every premises the council inspects. Stockholm's is the city's own food
  inspection register (Livsmedelstillsyn), one row per inspection reduced to one
  per premises, and frozen since October 2025. Bucharest's is the sanitary-veterinary
  directorate's register of food units (DSVSA București), active registrations only.
- **A chamber of commerce's membership:** Berlin (IHK Berlin's Gewerbedaten), each
  member's premises as a point. Membership, not licensing, decides who is in it:
  the crafts belong to a different chamber and are absent.
- **Property or building registers:** Dublin (rateable valuation list); Amsterdam
  and Rotterdam for shops (BAG shop-use units).
- **Permit lists:** Amsterdam's food layer (hospitality permits); Rotterdam's food
  layer, rebuilt from permit notices in the official gazette.
- **A food-premises licence register only:** Hong Kong (FEHD's registers, which
  license restaurants and food shops and nothing else a storefront needs).
- **Reason:** each country and city publishes what it publishes. The pages for
  Mexico City, Guadalajara, Monterrey, Madrid and Barcelona already say their density
  is "not comparable" with licence-register cities; Montréal's makes the point without
  those words (checked 2026-09-28). Buenos Aires's page says to read its
  density "as a survey, not a register"; London's, Glasgow's and Newcastle
  (Regional)'s "as a register, not a street survey" (checked 2026-09-29).

### 2. Some maps have only two categories, and some have a thin one
**Reader sentence:** Most maps colour businesses as Retail, Food service and Personal
services. A few cannot, because the local records never cover that trade.
- **No Personal services at all:** Philadelphia, Boston, London, Glasgow, Newcastle (Regional), Stockholm, Bucharest.
- **No Retail or Personal services at all:** Hong Kong. Its three categories are
  Food service, Food shops and Bathhouses, because FEHD licenses nothing else.
- **Retail limited to food retail (plus a few extras):** Philadelphia (bodegas and
  big-box stores that sell packaged food), Boston (grocers, package stores, cannabis),
  London, Glasgow and Newcastle (Regional) (grocers, off-licences, bakers,
  butchers, newsagents with food and supermarkets, named "Food shops" as in the
  Japanese cities); Stockholm the same, kiosks to supermarkets;
  Bucharest the same, butchers and bakeries to supermarkets.
- **Retail thin:** New York and Buffalo (food stores plus a regulated slice of trades). Toronto:
  Retail is only the regulated trades (second-hand, pawn, smoke/vape, pet shops,
  fireworks), 328 pins inside the rings against 6,474 Food service (nightclubs
  count as Food service since 2026-09-29). Seoul: Retail is
  only the licensed trades (bakeries, butchers, food shops, tobacco, marts, health food),
  47,933 pins inside the rings against 139,802 Food service. Daegu and Busan: the same
  licensed trades (11,031 and 14,330 Retail pins against 27,271 and 39,487 Food service).
  Kobe: Retail is food retail only (bakeries and confectioners, delis, butchers,
  fishmongers), because Japan licenses no other shop - 2,619 pins inside the rings
  against 16,980 Food service; food businesses that only notify the city are absent too.
  Osaka, Sapporo, Kyoto and Tokyo the same: 6,418, 2,111, 3,736 and 11,952 Retail
  pins inside the rings against 50,109, 16,222, 19,318 and 39,380 Food service
  (Tokyo's Food service without its caterers and the bar and snack-bar permit
  types, 2026-09-29).
  Fukuoka: 5,185 against 14,764 (without its caterers and snack bars), with the
  food shops that only notify present where they published in MHLW's opt-in list. On all six Japanese maps the layer is named
  "Food shops", not "Retail".
- **Personal services thin:** Berlin. Hairdressers and laundries are crafts,
  members of the Handwerkskammer rather than the chamber of commerce whose register
  the map uses, so the layer is beauty and nail salons, spas, saunas and massage
  (3,121 pins inside the rings against 30,800 Retail and 15,472 Food service;
  funeral services left it on 2026-09-29). The
  legend says "(partial)".
- **Retail and Personal services merged into "Shops and services":** Amsterdam,
  Rotterdam, Riga. The building register records a unit's intended use, not its trade.
- **Reason:** the city does not license that trade, or the source cannot tell the two
  apart. It is a gap in the data, not a choice about what to show.

### 3. A few maps include suburban rail, most do not
**Reader sentence:** Commuter and suburban trains are left off except where, inside
the city, they run like a metro: stations about a kilometre apart, frequent trains,
and districts no metro reaches.
- **Included:** Dublin (DART), Copenhagen (S-tog, 7 lines), Rome (the Roma–Viterbo
  line's urban section), São Paulo (CPTM Linha 9), Rio de Janeiro (SuperVia's Deodoro
  and Saracuruna lines), the six Japanese cities (JR and the private railways, cut
  at the city line: Kobe, Osaka, Sapporo (JR only), Fukuoka (JR and Nishitetsu),
  Kyoto, and Tokyo (JR East's nine services, seven private railways, and the
  Hokuso, Tsukuba Express and Rinkai lines, cut at the line of the 23 wards); an
  owner call of 2026-09-24, recorded in the `japan-city`
  skill, not the line-by-line test below), Berlin (the S-Bahn's 16 lines, the
  Ring among them, cut at the Land boundary), London (the Elizabeth line and the
  six London Overground lines, cut at Greater London), Sydney (Sydney Trains'
  six lines through the City of Sydney, where they run as a metro) and
  Melbourne (Metro Trains' six line groups through the City Loop and the Metro
  Tunnel).
- **Excluded by name:** BART and Caltrain, Metra, Metrolink, Coaster/Sprinter, SEPTA
  Regional Rail, MBTA Commuter Rail, Tri-Rail, GO Transit, West Coast Express,
  Cercanías, Milan's Passante and Trenord, Iarnród Éireann Commuter/InterCity, RER and
  Transilien, the TER around Marseille, CPTM Linhas 7, 8 and 10–13, SuperVia's other
  three lines, Fortaleza's and Recife's diesel lines, Korail's Daegyeong Line (Daegu)
  and Donghae Line (Busan), National Rail in London, Glasgow's suburban lines
  (the Argyle and North Clyde lines and the rest), Northern's trains in Tyne and
  Wear, Buenos Aires's commuter railways, NSW TrainLink (Sydney), and V/Line and
  the event-day Flemington Racecourse line (Melbourne).
- **Not mentioned either way:** Montréal (exo), Mexico City (Tren Suburbano).
  Montréal's REM is drawn from 2026-09-27 (the tram rescope).
- **Reason:** a spacing, frequency and coverage test, applied line by line (EC
  "Which stations these maps are drawn around").

### 4. Trams are on some maps and not others
**Reader sentence:** Trams and light rail are drawn where they are the city's rapid
transit, or where they reach areas the metro does not. They are left off where they
run on top of a metro network.
- **Trams or light rail drawn:** San Diego, San Francisco (Muni Metro; the F Market &
  Wharves from 2026-09-27), Los Angeles,
  Philadelphia (trolleys), Boston (Green Line, Mattapan), Calgary, Edmonton, Toronto
  (Lines 5 and 6 only), Mexico City (Tren Ligero), Guadalajara, Dublin (Luas),
  Marseille, Toulouse, Lille, Oslo, Amsterdam, Rotterdam, Rio (VLT), Santos (VLT),
  Hong Kong (Light Rail), Riga (its trams are the whole network), Montréal (the
  REM, an automated light metro), Rome (tram 8, thinned), Madrid (Metro Ligero
  ML1), Paris (T3a and T3b); these last four from 2026-09-27. Osaka (the Hankai
  tram, Hankai and Uemachi lines), Sapporo (the streetcar loop), Kyoto (the
  Randen's two lines and the Keihan Keishin Line, tramways in MLIT's data), Tokyo
  (the Tokyo Sakura Tram and the Tokyu Setagaya Line).
- **Trams not drawn:** Hong Kong Tramways (it runs beside the Island Line), Toronto's 18 streetcar routes, Milan (17 routes), Barcelona,
  Paris (all but T3a and T3b; T2 and T9 are stubs), Prague, Rome (all but tram
  8), Madrid (Metro Ligero ML2 and ML3, stubs), Copenhagen (the Letbane has no stop in
  scope), Berlin (BVG's 22 lines, an overlay on the U- and S-Bahn: they would add
  518 stops for about 7 more points of storefronts in the rings; owner,
  2026-09-28),
  London (Tramlink: about one more point of storefronts in the rings;
  owner, 2026-09-28), Buenos Aires (the Premetro, a surface light-rail line from
  Línea E's southern end, and the heritage tramway), Sydney (light rail L1–L3,
  22 stops in the council area: about ten more points, 83.2% to 93.0% on the
  brief's measure; owner, 2026-09-28), Melbourne (22 tram routes, 155 stops in
  the council area: about three more points, 96.0% to 99.1%; owner,
  2026-09-28). The Sydney and Melbourne pages state the effect.
- **Other modes on the map:** Toulouse's Téléo cable car, Barcelona's two
  funiculars, São Paulo's Linha 15 monorail, Miami's Metromover (automated people
  mover), Daegu's Line 3 monorail, Busan's Line 4 (a rubber-tyred light metro, which
  OSM tags `route=monorail`) and the Busan–Gimhae LRT (an automated light metro),
  Kobe's Port Liner and Rokkō Liner, Osaka's New Tram, and Tokyo's Yurikamome and
  Nippori-Toneri Liner (automated guideway lines), and the Tokyo Monorail.
  Kobe's Maya and Rokkō cable cars and Kyoto's Eizan and Kurama cable cars are not
  drawn (funiculars left out in every Japanese city, owner).
- **Reason:** "is the tram the rapid-transit system, or an overlay on one?", later
  widened to "does it serve corridors the metro does not?" (DEC, Oslo and Rotterdam
  entries). See Open questions 9 and 10: the stated reasons differ between cities.

### 5. Some maps cover one city, others a whole region
**Reader sentence:** Most maps stop at the city boundary, and the stations beyond it
are drawn on the line but get no ring. Some cover several municipalities because one
register covers them all, or because the rail network only makes sense that way.
- **Labelled "(Regional)":** Miami (Miami-Dade County), Vancouver (with Surrey),
  Guadalajara (4 municipios), Monterrey (4 municipios), Lille (11 communes), Fortaleza (4), Porto Alegre (6),
  Recife (4), Santos (with São Vicente), Taipei (with New Taipei), Newcastle
  (Regional) (the five Tyne and Wear districts).
- **Cover more than one municipality but are not labelled:** Montréal (the
  agglomeration: 19 boroughs and 15 related municipalities), Dublin (four local
  authorities), Copenhagen (with Frederiksberg), Tokyo (the 23 special wards, each
  its own municipality).
- **Business data for only part of the area drawn:** Tokyo. The rail is drawn
  across all 23 wards, but only 8 publish a usable food-permit list; the 293
  stations in the other 15 are drawn hollow, with no rings, and nothing there is
  counted (a business near a ward edge counts to the nearest station in a ward with
  data).
- **Regional maps that count a municipality with no station:** Fortaleza (Caucaia),
  Recife (Cabo de Santo Agostinho). Guadalajara leaves out Tonalá for having none.
- **Lose the most stations to the boundary:** Seoul (227), Melbourne (199),
  Sydney (157; both keep to one council's area), Paris (76), Osaka (76),
  Copenhagen (59), Washington
  D.C. (58), Tokyo (55), Los Angeles (54), Rotterdam (52), Barcelona (50), Madrid (49), Boston (43).
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

### 7. The share of storefronts near a station ranges from about one in thirteen to nearly all
**Reader sentence:** On some maps nearly every shop is inside a station ring; on
others most of the city is beyond walking distance of the network. That depends on
how far the network reaches, not on the data.
- **90% or more inside the rings:** Barcelona 100%, Paris 98%, Osaka 98%, Tokyo 98%
  (of the eight wards with data), Melbourne 96%, Amsterdam 96%, Madrid 95%, Copenhagen 94%, Seoul 94%, Rotterdam 93%, Hong Kong 91%.
- **Under 25%:** Houston 7%, Taoyuan 12%, Miami 13%, Brasília 14%, Fortaleza 14%, Belo Horizonte
  18%, Salvador 19%, Taichung 19%, Porto Alegre 20%, Edmonton 22%, São Paulo 23%,
  Recife 23%, Los Angeles 24%, San Diego 24%.
- **Reason:** network extent against the area in scope. Share = in-ring heat points ÷
  all-storefront heat points in each committed map.

### 8. Some maps show no business names
**Reader sentence:** On some maps a dot shows an address or a type of business rather
than a name, either because the source records no names or to avoid showing a person's
name at their home.
- **No names at all:** Dublin (address and recorded use), Rome (activity and address),
  Rotterdam, Riga (the kind of place, or the premises' registered name), Berlin (the
  chamber's own label for the kind of business; the register has neither names nor
  street addresses), Sydney (the ANZSIC class; the survey publishes neither names
  nor addresses), Buenos Aires (street address and the surveyed use; the survey
  records uses, not who runs them).
- **Mostly addresses:** Milan (a shop sign on about 1 pin in 7), Amsterdam's shop
  layer, the French cities where SIRENE has no sign or usual name (only about 40% of
  Paris rows and 43% of Marseille rows are named, per the Marseille brief).
- **Address in place of a sole trader's name:** Oslo, Bergen, Copenhagen, Aarhus (and a franchisee's own name with a store number, Denmark's two cities), Prague, Houston (sole
  owners and partnerships of individuals, by the permit's organisation type).
- **Brazil:** the census enumerator's description, not a trade name; only the category
  where the address is also a home (35–69% of dots, by city).
- **Type in place of a personal name:** Vancouver/Surrey (88 pins). Buffalo (42 salons licensed under a person's own name show the licence type). Sacramento (525 businesses whose name reads as a person's show their description). Kobe (10 pins: a
  trade name that is the operator's own name shows its permit type). Osaka (9 pins,
  the same rule, applied to every permit at the premises), Sapporo (7), Kyoto (8),
  Fukuoka (5, on the city's lists only: MHLW publishes no operator column to test),
  Tokyo (2, on the lists that name their operators only: most name only companies,
  and two wards withhold individuals' names themselves).
- **"Name withheld" in place of a personal name:** Seoul (138 pins), Daegu (113),
  Busan (114).
- **Line of business in place of an unmarked sole proprietor's name:** Taichung
  (11,907 pins), Taoyuan (7,230), Taipei (17,890).
- **"No shop sign":** Hong Kong (308 pins, where the licence records none).
- **Reason:** the source has no name column, or a privacy rule.

### 9. The data dates from different years, and not every page says when
**Reader sentence:** Most maps were built from data downloaded in September 2026, but
a few sources are older: a 2022 census, a 2022 street survey, a July 2025 register.
- **Older as-of dates:** the nine Brazilian cities (2022 census fieldwork), Barcelona
  (2022 survey; the 2024 survey is incomplete), Montréal (2025 survey), Rome (July
  2025 file, the newest published), Prague (establishments as of 2026-08-31), Daegu
  (a 2026-08 edition whose rows end 2025-08-31), Busan (the feed froze 2026-04-15),
  Kobe (permits in force 2026-03-31), Osaka (food permits 2026-06-30, the other
  registers 2026-03-31), Sapporo (food permits 2026-03-31), Fukuoka (laundries
  2026-03-31), Kyoto (registers 2026-03-31 plus the months since; food permits
  rebuilt to 2026-07-31), Tokyo (each ward's list has its own date: Chuo's and
  Koto's hold only permits from June 2021 to late 2022, Shinjuku's is a 1 January
  2023 snapshot, the other five run to 2026; `pipeline/tokyo/config.py`
  `_FOOD_AS_OF`), Buenos Aires (each block surveyed once, 2022 to 2024), Sydney
  (the 2022 survey, taken every five years), Melbourne (the 2024 census),
  Stockholm (the register froze at its 2025-10-21 inspections; premises
  last inspected in 2022-23 are shown as they stood then).
- **Date of the business data shown on the page:** Barcelona, Copenhagen, Prague,
  Amsterdam, Rome, the Brazilian cities, Rotterdam, Hong Kong, Riga, Seoul, Daegu,
  Busan, Taichung, Taoyuan, Taipei, the six Japanese cities, Berlin (the register's monthly
  date, 2026-09-01), London (each borough's extract date, 2026-09-09
  to 2026-09-16), Glasgow (the council's extract date, 2026-09-14), Newcastle
  (Regional) (each council's, 2026-09-09 to 2026-09-16), Buenos Aires (the
  survey years, in the prose), Sydney (the survey year) and Melbourne (the
  census year), Stockholm (the register's last edit, 2025-10-22) and
  Bucharest (the registers' date, 2026-08-25).
- **Only the transit date shown:** Paris, Marseille, Toulouse, Lille, Rennes, Oslo.
- **No date shown:** the nine US cities, the five Canadian, the three Mexican, Madrid,
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
  (4.3% unmatched); Riga's food layer (only premises licensed to sell alcohol or tobacco); Prague (about 57,000 establishments whose owner's main activity is
  something else); Miami (repair and service premises); Mexico City, Guadalajara and
  Monterrey (street stalls); Copenhagen (tattoo studios); Chicago (licences with no
  coordinates); Kobe, Osaka, Sapporo and Kyoto (food businesses that only notify
  the city hold no permit and are absent; Osaka's list holds about 70% of the
  restaurant permits Osaka reports nationally); Fukuoka (notifying food shops
  appear only where they published in MHLW's opt-in list, and about one restaurant
  in five withheld its address and is unplaced); Tokyo (fifteen of the 23 wards have
  no data, and the eight lists run from 9% to 101% of each ward's official
  restaurant count, each ward's share on the page; notifying food shops absent
  except where a list includes notifications); Berlin (the crafts - hairdressers,
  laundries, many bakers and butchers - are not chamber-of-commerce members);
  London (about one food storefront in
  twenty has no location and no full postcode and is not placed, a quarter in
  Redbridge and a fifth in Havering); Glasgow (about one food storefront in a
  hundred has no map point and is not placed); Newcastle (Regional) (about one
  in fourteen unplaced, most in North Tyneside and Sunderland); Buenos Aires
  (shopfronts whose use the surveyors could not identify, 7.2% and 32% in Villa
  Riachuelo, are dropped, and shops inside malls and arcades are not itemised).
- **Overcounts, or best read as upper bounds:** Milan (the six registers are not
  merged, so a business can count twice); Rome and Rotterdam (no closing dates, or a
  five-year permit window); Riga's shops (the cadastre records use, not occupancy); the SIRENE, Oslo, Copenhagen and Prague registers
  (registered premises that may have no shopfront, including web shops); Edmonton
  (about 1 in 16 Personal services pins is a clinic); Amsterdam and Rotterdam (empty
  shop units cannot be removed); Kobe, Osaka, Sapporo and Fukuoka's city list
  (closed premises may remain listed); Kyoto (an upper bound: the city publishes no
  closures, so a permit still in term counts); Tokyo (the page says a dot is "a
  permit on file, not a business open today"; Shibuya's list and MHLW's filings
  mark closures, and those are left out); Berlin (closures and moves reach the
  register late; registered premises may have no shopfront, including web shops and
  business centres; about 1.2 to 1.5 times OpenStreetMap's restaurants, cafés and
  bars at four station areas); London, Glasgow and Newcastle (Regional) (a
  premises stays listed until the council removes it, as each page says).
- **Undisclosed on the city page:** San Francisco (only about 37% of rows carry a
  NAICS code) and Los Angeles (about 9% carry none), so both are floors. San Diego
  undercounts neighbourhoods registered under their own name. All three are open
  `PLAN.md` items.
- **Reason:** how each source is compiled.

### 11. What falls inside a category differs at the edges
**Reader sentence:** The three categories are meant to mean the same thing
everywhere, but a few businesses land differently depending on how a country
classifies or licenses them.
- **RESOLVED 2026-09-29 by one rule (owner):** five kinds of business are left off
  every map wherever a register names them - funeral services (funeral homes,
  crematoria, cemeteries); food with no counter of its own (institutional canteens,
  event caterers, food trucks, street and market stalls); the "other personal
  services" catch-all; adult and hostess venues (sex shops are shops and stay); and
  gambling (betting shops, casinos, arcades, lottery agencies). Newsstands and
  kiosks, pawnbrokers, karaoke bars and nightclubs are kept everywhere. The 41 maps
  affected were re-rendered the same day. What still differs
  is where a register files one of these under the same label as ordinary
  businesses; those cases are below, and each is disclosed in its EC city section.
- **Car dealers:** counted as Retail everywhere a register names them: the NAICS
  cities and Montréal, Chicago, Miami, Washington D.C., Vancouver/Surrey, Calgary,
  Edmonton, Mexico City, Guadalajara, Monterrey, Madrid, Barcelona, Dublin, Oslo,
  Copenhagen, Prague and Berlin (NACE Rev. 2.1 moved car retail into 47.81-47.83),
  Buenos Aires, the nine Brazilian cities, Taichung, Taoyuan, Taipei, Sydney and
  Melbourne (ANZSIC 39, with fuel retail; the Sydney page says so). **France is the
  one exception** (owner, 2026-09-29): SIRENE files vehicle sales in their own
  division (NAF 45), and its four selling codes would add about 9,500 pins across
  the five cities (5,384 in Paris), but about 95% record no employees and about a
  quarter carry a premises name - mostly one-person traders, probably registered
  at home. `france_naf.py` keys on 47, 56 and 96 only and gives that reason; the
  Paris page's approved sentence saying so lands with the batch. Toronto, Philadelphia, Boston, Hong Kong and the Korean,
  Japanese and UK maps license or inspect no car dealer, so none appears.
- **Funeral services:** off every map where a code or licence type names them
  (Brazil by keyword: 558 pins removed across the nine cities). They remain where
  the register cannot separate them: **Chicago** has no funeral licence type; most
  funeral homes were under the "Miscellaneous Personal Services" catch-all and
  left with it (35), and the 29 funeral-word pins that remain sell funeral items.
  **Calgary:** about 12 funeral-word pins under the general retail licence stay.
  **Milan:** no funeral code; about 29 funeral services reach the non-food shop
  layer through the shop register and stay. **Amsterdam, Rotterdam, Riga:** the
  building register records only a shop unit, so a funeral home cannot be
  identified.
- **Food with no counter of its own:** canteens, event caterers, food trucks and
  stalls are excluded wherever coded. Remaining differences: **Montréal keeps its
  caterers** (107), because the survey records walk-in traiteur shops, as France
  keeps its traiteurs (56.21Z; only 56.29 contract and institutional catering
  leaves). **Los Angeles** keeps `722300` "special food services" (3,145 pins),
  which the registry uses for caterers, concession stands and food trucks alike
  but also for taquerias and cafés. **San Francisco** drops its food-service
  contractor code whole, although it also holds stadium and convention-centre
  concession stands, Bay ferry bars and a few restaurants. **Brazil:** food
  trucks, trailers, kiosks and stalls cannot be told from fixed premises in the
  census's descriptions and count as whatever the rest of the description names.
  **London, Glasgow, Newcastle (Regional):** a workplace canteen registered as a
  restaurant or café cannot be told apart; not measured.
- **Street and market stalls:** excluded in Mexico City, Guadalajara and Monterrey;
  by code in France (47.8x) and Taiwan (street and market stalls, e.g. 2,669 in
  Taipei); food trucks and stalls (permits valid city-wide) in the six Japanese
  cities, but Fukuoka's yatai (屋台, fixed street stalls on long-term permits) are
  counted as Food service (owner); markets in Philadelphia (curb markets), Calgary,
  Dublin and Surrey (flea market). Not separable in Brazil (above).
- **The "other personal services" catch-all:** excluded in every city since
  2026-09-29. Until then San Diego (`81299` and its group-level `8129`), San
  Francisco's residual `81299` rows, Chicago's "Miscellaneous Personal Services",
  Prague (three rows) and the Taiwanese cities kept it. It takes fortune-tellers
  and dating or marriage agencies with it (Madrid, Buenos Aires, Taiwan).
  Copenhagen's tattoo studios leave with it (table B).
- **Massage:** a Personal service in Calgary and Edmonton, where Alberta does not
  regulate it, and in Toronto's non-registered "holistic centres"; excluded as health
  care in Vancouver/Surrey, where British Columbia regulates it. San Diego's own
  massage-parlour code (`812193`) is excluded; massage therapy (`812198`) stays.
- **Adult and hostess venues:** excluded wherever a register names them (owner,
  2026-09-29). Body-rub and similar premises in Calgary, Edmonton, Toronto (adult
  entertainment clubs too) and Vancouver; escort and prostitution with Berlin's
  catch-all, while non-medical massage (a class of its own) is kept; brothels
  (ANZSIC 9534) by class in Sydney and Melbourne; hostess bars in Seoul, Daegu and
  Busan; Tokyo's bar-and-cabaret and snack-bar permit sub-types (バー・キャバレー,
  スナック; 2,536) and Fukuoka's snack bars (103). Sex shops stay (Surrey's one
  `Adult Entertainment Store`). **Kept, though possibly the same thing:** Meguro
  lists its bar permits as 飲食バー (102), without the cabaret or snack detail; the
  Taiwanese drinking places and restaurants with shows, whose register names claim
  no hostess service. No code separates such venues in the NAICS, SCIAN, NAF, NACE
  or CNEFE cities; whether those maps hold any is UNKNOWN (open question 15).
- **Gambling:** excluded wherever a register files it among storefront uses:
  Dublin's betting shops (175, with a casino and an amusement centre that had
  reached the map through a "shop" use beside them), Rome's arcades and gaming
  machines, Rotterdam's gaming permits, Calgary's arcades, Edmonton's and
  Vancouver's bingo halls and casinos, Buenos Aires's and Brazil's lottery
  agencies. In the NAICS, SCIAN, NAF and NACE cities gambling sits outside the
  retail, food and personal-service codes and was never mapped.
- **Nightclubs, karaoke, pawnbrokers, newsstands and kiosks:** kept everywhere.
  Toronto's nightclubs (36 active premises, about 32 new pins), Edmonton's
  after-hours dance club and Miami's `NIGHT CLUB` and `DANCING OR ENTERTAINMENT`
  count as Food service; Philadelphia's newsstands and Dublin's kiosks as Retail.
  San Diego's "kiosk businesses" (`81295`/`812959`, ecoATM phone-recycling
  machines) are machines, not kiosks, and are excluded.
- **Vets:** excluded as health care where coded (the Korean cities, Buenos Aires);
  Barcelona's `Veterinaris / Mascotes` (395) puts vets under one value with pet
  shops and groomers, about 160 read as clinics by name, and all are kept.
- **Web shops:** excluded by code in France, and by class in Sydney and Melbourne
  (ANZSIC 4310, non-store retailing); cannot be excluded in Oslo, Copenhagen,
  Prague or Berlin (Berlin leaves out general non-food retail, the broad registration
  most online and market traders take).
- **One premises with several licences:** counted once almost everywhere; counted
  twice in Milan; and in Calgary a premises with both retail and food licences counts
  as Food.
- **Legend labels:** show code prefixes in the NAICS, SCIAN, NAF, SN2025, DB25 and
  CZ-NACE cities ("Retail — NAICS Code: 44/45", "Retail - NAF 47"); plain names
  in the cities with a local taxonomy, and in Sydney and Melbourne although
  ANZSIC is a national classification.
- **Reason:** national classifications and provincial or state regulation, and,
  since the common rule, registers that file an excluded kind under the same
  label as ordinary businesses.

### 12. RESOLVED 2026-09-27 - every map now has a whole-city heat layer
Kept as a numbered heading so references to theme 12 still resolve. Mexico City
and Guadalajara lacked the layer (dropped 2026-09-22 for file size, Guadalajara to
match); Seoul lost it 2026-09-25 for phones. All three were restored 2026-09-27 once
the map data shipped as JSON.parse and the full maps loaded on an iPhone (DECISIONS
2026-09-27). No reader-facing difference remains.

### 13. RESOLVED 2026-09-30 - which stops count as a station: request stops
A station-related discrepancy in the code, found before it reached a map. A
transit feed marks each scheduled stop as boardable or not, and the GTFS
standard has four codes: 0 regular, 1 not available, 2 phone ahead, 3 tell the
driver (a request stop). Until 2026-09-30 `pipeline/stations.py`
`boardable_stop_ids()` counted only 0 as a stop a reader can use, so a stop
served only on request was dropped as if it were depot track. Brno's feed codes
every request stop 3, and 25 of its 149 tram stations would have vanished
(found by the Czech builds). Nothing would have flagged a station that is
simply absent.
- **Built maps: none affected.** All ten built cities that read a feed's
  boardable codes were scanned (Amsterdam, Rotterdam, Berlin, Paris, Marseille,
  Toulouse, Rennes, Oslo, Bergen, Prague). Codes 2 and 3 appear only on lines
  those maps do not draw: Prague's buses, trams, regional rail, trolleybuses
  and ferries (its map draws the metro); the Dutch buses and international
  trains; Paris's demand-responsive and evening buses. Oslo, Bergen, Berlin,
  Rennes, Toulouse and Marseille have no stop the old rule dropped, so the
  function returns the identical set. The other eight cities' drift checks are
  zero drift.
- **Now:** codes 0, 2 and 3 count (owner, 2026-09-30), so a tram or
  light-rail city with request stops keeps them. Cities that build their
  stations from OpenStreetMap or a published list never read these codes.

---

## City by city

In-ring pins are the per-category counts in each map's layer menu (inside the rings
only). "Out / thinned" is taken from `outputs/<slug>/excluded_stations.csv`: stations
left out as outside the scope / surface stops dropped by the spacing filter.

### A. Rail (dimensions 1–3)

| City | Drawn | Notably not drawn | Rail source | Station scope | Out / thinned |
|---|---|---|---|---|---|
| **United States** | | | | | |
| San Diego | Trolley (light rail), 5 lines | Coaster, Sprinter | MTS GTFS; gate 3 exact | City | 16 / 0 |
| San Francisco | Muni Metro J K L M N T + F Market & Wharves | BART, Caltrain, cable cars | SFMTA GTFS (mirror); gate 3 exact | City and County | 0 / 85 |
| Los Angeles | Metro Rail A B C D E K (heavy + light) | Metrolink | LA Metro rail GTFS; gate 3 exact | City | 54 / 0 |
| Chicago | 'L', 7 lines | Metra; Yellow Line | CTA GTFS; gate 3 exact, less State/Lake (closed) | City | 18 / 0 |
| New York | Subway (11 trunk groups) + Staten Island Rwy | LIRR | MTA GTFS; gate 3 against the MTA's station register | Five boroughs | 0 / 0 |
| Philadelphia | MFL, BSL + subway-surface and Girard trolleys | Regional Rail; NHSL, Media–Sharon Hill (outside city) | SEPTA GTFS; gate 3 exact on the L, B, G and the tunnel; T branches not gated | City | 7 / 162 |
| Miami (Regional) | Metrorail + 2 Metromover loops | Tri-Rail; MIA people mover | Miami-Dade Transit GTFS; gate 3 exact | County (6 municipalities have stations) | 0 / 0 |
| Boston | Red, Orange, Blue + Green, Mattapan | Commuter Rail, ferries | MBTA GTFS; gate 3 exact (MBTA) | City | 43 / 25 |
| Washington D.C. | Metrorail, 6 lines | DC Streetcar no longer operating (ended 2026-03-31); MARC/VRE are separate systems | WMATA GTFS (API key); gate 3 exact | District | 58 / 0 |
| Buffalo | NFTA Metro Rail (light rail, one line) | NFTA's GTFS not used (OSM) | OpenStreetMap route relations; gate 3 exact on 14 | City | 0 / 0 |
| Sacramento | SacRT light rail, Blue and Gold | Green Line (suspended; its one station closed for works) | OpenStreetMap route relations (+ Wikidata for Dos Rios); gate 3 exact on SacRT's timetables | City | 15 / 0 |
| Houston | METRORail light rail, Red, Green and Purple | — | OpenStreetMap route relations (METRO's data agreement kept out); gate 3 exact | City (TIGER) | 0 / 0 |
| Minneapolis | METRO Blue and Green light rail | Northstar commuter rail; the Como-Harriet heritage streetcar (a museum ride) | OpenStreetMap route relations (Metro Transit's GTFS licence unread); gate 3 exact on 19 and 23 | City (TIGER) | 22 / 0 |
| Pittsburgh | PRT light rail (the T), Red, Blue and Silver, with the downtown subway | Buses, the inclines | OpenStreetMap route relations (PRT's GTFS licence unread); gate 3 exact on 31, 24 and 31 | City (TIGER); halved rings | 31 / 0 |
| Dallas | DART Light Rail, Red, Blue, Green and Orange | Dallas Streetcar, M-Line trolley (owner); Silver Line and TRE (commuter rail) | OpenStreetMap route relations (Houston's route); gate 3 exact | City (TIGER) | 20 / 0 |
| Kansas City | KC Streetcar, one line | Buses | OpenStreetMap route relations (RideKC's GTFS barred, owner); gate 3 exact | City (TIGER) | 0 / 0 |
| Tucson | Sun Link streetcar, one line | Buses | OpenStreetMap route relations; gate 3 exact | City (TIGER) | 0 / 0 |
| New Orleans | RTA streetcars 12, 46, 47, 48, 49 | Buses, ferries; OSM's stale ref 2 | OpenStreetMap route relations; 46 and 49 stops by node; gate 3 exact (RTA) | City (TIGER; Orleans Parish) | 0 / 0 |
| **Canada** | | | | | |
| Vancouver (Regional) | SkyTrain Expo, Millennium, Canada | West Coast Express, SeaBus | TransLink GTFS; gate 3 exact | Vancouver + Surrey | 30 / 0 |
| Montréal | Métro, 4 lines + REM (A1, A3, A4) | not stated (exo) | STM GTFS + the REM's own GTFS; gate 3 exact | Agglomeration (island) | 11 / 0 |
| Calgary | CTrain Red, Blue (light rail) | — | Calgary Transit GTFS | City | 0 / 0 |
| Edmonton | LRT Capital, Metro, Valley | 3 non-revenue stops | ETS GTFS; gate 3 exact | City | 0 / 0 |
| Kitchener–Waterloo (Regional) | ION light rail (GRT route 301) | GO Transit's Kitchener line (suburban rail); ION's bus to Cambridge | OpenStreetMap route relations (the light-rail builds' source); gate 3 exact against the Region's ION Stops layer | Two cities (the Region's Kitchener and Waterloo polygons) | 0 / 0 |
| Toronto | Subway 1, 2, 4 + LRT 5, 6 | 18 streetcar routes; GO | TTC GTFS (City CKAN) | City | 2 / 0 |
| Ottawa | O-Train Lines 1, 2 and 4 (light rail) | Buses, the Transitway | OpenStreetMap route relations (OC Transpo's GTFS licence unread); gate 3 exact against Wikipedia | City (its own wards) | 0 / 0 |
| **Mexico** | | | | | |
| Mexico City | Metro, 12 lines + Tren Ligero | not stated (Tren Suburbano, Cablebús) | OpenStreetMap | CDMX | 10 / 0 |
| Guadalajara (Regional) | Tren Ligero L1–L4 | — | OpenStreetMap (only GTFS expired 2023, lacks L4) | 4 municipios; Tonalá out | no CSV (all in scope) / 0 |
| Monterrey (Regional) | Metrorrey L1–L3 | Líneas 4 and 6 (monorail, under construction) | OpenStreetMap (no agency data published); L3 in the operator's red | 4 municipios, by INEGI code | no CSV (all in scope) / 0 |
| **Spain** | | | | | |
| Madrid | Metro L1–L12 + Ramal + Metro Ligero ML1 | Cercanías; Metro Ligero ML2, ML3 (stubs), ML4 (Parla) | CRTM ArcGIS layers; gate 3 exact (CRTM's line pages) | Municipio | 49 / 0 |
| Barcelona | Metro L1–L12 (TMB+FGC) + 2 funiculars | Trams | OpenStreetMap | Municipi | 50 / 0 |
| Palma | Metro de Palma M1 (10 stations) | SFM's trains T1–T3 (suburban rail); M2, no longer a metro service | OpenStreetMap route relations; gate 3 exact against TIB's stop list | Municipality (OSM) | 0 / 0 |
| **Ireland** | | | | | |
| Dublin | Luas Red, Green + DART | Commuter, InterCity | NTA national GTFS; gate 3 exact | 4 local authorities | 2 / 0 |
| **Italy** | | | | | |
| Milan | Metro M1–M5 | 17 trams; Passante, Trenord | ATM GIS layers (+GTFS colours) | Comune | 21 / 0 |
| Rome | Metro A, B, B1, C + Roma–Viterbo (urban) + Tram 8 | Other trams (2, 3, 5, 14, 19 bus-replaced); 8 prolungato; Roma–Lido; suburban | OpenStreetMap | Comune | 1 / 9 |
| Florence | Tramvia T1 and T2 | Buses, trains; T3 and T4 (building) | OpenStreetMap; gate 3 exact | Comune | 4 / 0 |
| **France** | | | | | |
| Paris | Métro, 16 lines + Trams T3a, T3b | RER, Transilien, other trams (T2 and T9 stubs) | IDFM GTFS | Commune | 76 / 0 |
| Marseille | Métro 1–2 + Tramway 1–3 | TER; ferries; Aubagne tram | Métropole AMP GTFS (RTM) | Commune | 7 (Aubagne tram) / 0 |
| Toulouse | Métro A–B + Tram T1 + Téléo cable car | — | Tisséo GTFS | Commune | 14 / 0 |
| Lille (Regional) | Métro 1–2 + Tram R, T | heritage tram, disused line | MEL GIS + OpenStreetMap (métro lines) | 11 communes | no CSV (none lost) / 0 |
| Rennes | Métro a, b | — | STAR GTFS | Commune | 4 / 0 |
| Le Mans | Tram T1, Tram T2 | — | SETRAM GTFS | Commune | 0 / 0 |
| Besançon | Tram T1, Tram T2 | — | Ginko GTFS | Commune | 2 / 0 |
| Avignon | Tram T1 | — | Orizo GTFS | Commune | 0 / 0 |
| Tours | Tram A | — | Fil Bleu GTFS | Commune | 7 / 0 |
| Dijon | Tram T1, Tram T2 | — | Divia GTFS | Commune | 6 / 0 |
| Reims | Tram T1, Tram T2 | — | Grand Reims Mobilités GTFS | Commune | 3 / 0 |
| Orléans | Tram A, Tram B | — | TAO GTFS | Commune | 19 / 0 |
| Mulhouse | Tram 1, Tram 2, Tram 3 | TT (tram-train) | Soléa GTFS | Commune | 1 / 0 |
| Brest | Tram A, Tram B, Téléphérique | — | Bibus GTFS | Commune | 2 / 0 |
| Saint-Étienne | Tram T1, Tram T2, Tram T3 | — | STAS GTFS | Commune | 5 / 0 |
| Nice | Tram 1, Tram 2, Tram 3, Tram B | — | Lignes d'Azur GTFS | Commune | 0 / 0 |
| Montpellier | Tram 1, Tram 2, Tram 3, Tram 4, Tram 5 | — | TaM GTFS (geometry OSM) | Commune | 24 / 0 |
| Strasbourg | Tram A, Tram B, Tram C, Tram D, Tram E, Tram F | — | CTS GTFS (geometry OSM) | Commune | 29 / 0 |
| Le Havre | Tram A, Tram B | — | LiA GTFS (geometry OSM) | Commune | 1 / 0 |
| Caen | Tram T1, Tram T2, Tram T3 | — | Twisto GTFS (geometry OSM) | Commune | 9 / 0 |
| Rouen (Regional) | Métro | — | Astuce GTFS (geometry OSM) | 5 communes served | 0 / 0 |
| Bordeaux (Regional) | Tram A, Tram B, Tram C, Tram D, Tram E, Tram F | — | TBM GTFS | 14 communes served | 0 / 0 |
| Nantes (Regional) | Tram 1, Tram 2, Tram 3 | — | Naolib GTFS | 6 communes served | 0 / 0 |
| Grenoble (Regional) | Tram A, Tram B, Tram C, Tram D, Tram E | — | M réso GTFS | 12 communes served | 0 / 0 |
| Valenciennes (Regional) | Tram T1, Tram T2 | — | Transvilles GTFS | 13 communes served | 0 / 0 |
| Angers | Tram A, Tram B, Tram C | — | Angers Loire Métropole GTFS | Commune | 6 / 0 |
| **Norway** | | | | | |
| Oslo | T-bane 1–5 + trams 12, 13, 15, 17, 18, 19 | Ferries | Ruter via Entur GTFS | Kommune | 12 / 0 |
| Bergen | Bybanen 1 and 2 (light rail) | Ferries | Skyss via Entur GTFS | Kommune | 0 / 0 |
| **Romania** | | | | | |
| Bucharest | Metrorex M1–M5 | Suburban trains, trams | OpenStreetMap route relations; gate 3 exact on 64 (network) | Municipality (six sectors) | 0 / 0 |
| **Sweden** | | | | | |
| Stockholm | Tunnelbana: Gröna, Röda and Blå linjen (routes T10–T19), one label per line | Pendeltåg, Roslagsbanan, Saltsjöbanan, trams; the unopened Yellow line | OpenStreetMap route relations (SL's GTFS needs a key); gate 3 exact on 100 | Kommune | 18 / 0 |
| Göteborg | Göteborgs Spårvägar trams 1–13 | Buses, ferries, commuter trains; Lisebergslinjen (heritage) | OpenStreetMap route relations; gate 3 exact (Västtrafik) | Kommun | 5 / 0 |
| **Denmark** | | | | | |
| Copenhagen | Metro M1–M4 + S-tog (7 lines) | Regional/InterCity; Letbane | OpenStreetMap | Copenhagen + Frederiksberg | 59 / 0 |
| Aarhus | Letbane L2 on the city tramway (light rail) | Odderbanen and Grenaabanen (under the 15-minute test); L1 not drawn | OpenStreetMap | Kommune | 30 / 0 |
| Odense | Odense Letbane, one tram line | Buses and regional trains | OpenStreetMap | Kommune | 0 / 0 |
| **Czechia** | | | | | |
| Prague | Metro A, B, C | Trams, funicular, ferries, suburban | PID GTFS | City | 0 / 0 |
| Brno | Trams 1–10, 12 | Heritage tram H4, shuttle P1; S-trains, trolleybuses, ferry | KORDIS JMK GTFS (geometry OSM); gate 3 vs OSM agrees on 9 of 11 lines | City | 2 / 0 |
| Plzeň | Trams 1, 2, 4 | Relief and depot runs 1X, 4X; trolleybuses | OpenStreetMap route relations; gate 3 vs PMDP GTFS (depot only) | City | 0 / 0 |
| Olomouc | Trams 1–7 | — | OpenStreetMap route relations; gate 3 exact (IDOS) | City | 0 / 0 |
| Ostrava | Trams 1–4, 6–8, 10–12, 14, 15, 17, 18 | Line 5 (suburban, 2 in-city stops); lines 9, 19 (no stops in OSM); trolleybuses | OpenStreetMap route relations; gate 3 partial (IDOS, diversion) | City | 7 / 0 |
| Liberec (Regional) | Trams 2, 3, 5, 11 | — | OpenStreetMap route relations (+3 stops); gate 3 exact (IDOS) | Liberec + Jablonec nad Nisou | 0 / 0 |
| Most (Regional) | Trams 1–4 | — | OpenStreetMap route relations (+1 stop); gate 3 exact (IDOS) | Most + Litvínov | 0 / 0 |
| **Netherlands** | | | | | |
| Amsterdam | Metro 50–54 + 16 trams | Tram 3, museum tram, ferries, NS | OVapi national GTFS (GVB) | Gemeente (with Weesp) | 22 / 59 |
| Rotterdam | RET metro A–E + 9 trams | Trams 12, 14, 18; ferries; NS | OVapi national GTFS (RET) | Gemeente | 52 / 23 |
| Den Haag | HTM trams 1, 2, 6, 9, 10, 11, 12, 15, 16, 17, 19 and RandstadRail 3, 4, 34 (14 lines) | RandstadRail E (RET metro, a stub: 4 of 23 stops inside), the 9S short working, buses, NS | OpenStreetMap route relations; gate 3 exact (HTM) | Gemeente | 64 / 0 |
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
| **Latvia** | | | | | |
| Riga | Rīgas satiksme trams, 7 routes | Buses, trolleybuses, Vivi suburban rail | Rīgas satiksme GTFS; gate 3 exact before thinning | City (58 neighbourhoods) | 0 / 15 |
| Liepāja | Tram 1, the one line | Buses and suburban trains | OpenStreetMap; gate 3 exact | City | 0 / 0 |
| Daugavpils | Trams 1-5 (3 and 5 one loop) | Buses and suburban trains | OpenStreetMap; gate 3 exact | City | 0 / 0 |
| **South Korea** | | | | | |
| Seoul | Seoul Metropolitan Subway: Lines 1–9, Shinbundang, Ui LRT, Sillim + 3 Korail lines | AREX, GTX-A, Seohae Line, Gimpo Goldline | OpenStreetMap (gate 3 exact on all 15 lines) | City | 227 / 0 |
| Daegu | Daegu Metro Lines 1–3 (Line 3 a monorail) | 대경선 (Korail, on spacing) | OpenStreetMap (gate 3 against Korean Wikipedia; operator unreachable) | City | 5 / 0 |
| Busan | Busan Metro Lines 1–4 (Line 4 a rubber-tyred light metro) and the Busan–Gimhae LRT | 동해선 (Korail, on spacing) | OpenStreetMap (gate 3 against Korean Wikipedia) | City | 17 / 0 |
| Incheon | Incheon Lines 1 and 2, Line 1, Line 7, Suin–Bundang Line | AREX, the airport maglev, the Wolmi Sea Train | OpenStreetMap (gate 3 against English Wikipedia; Line 1 not gated) | City | 151 / 0 |
| Goyang | Line 3, Gyeongui–Jungang Line | Seohae Line (same track), GTX-A | OpenStreetMap (gate 3 on Line 3) | City | 76 / 0 |
| Seongnam | Line 8, Suin–Bundang, Shinbundang, Gyeonggang Lines | GTX-A | OpenStreetMap (gate 3 on two lines) | City | 91 / 0 |
| Yongin | EverLine, Suin–Bundang, Shinbundang Lines | GTX-A | OpenStreetMap (gate 3 on all three) | City | 67 / 0 |
| Suwon | Line 1, Suin–Bundang, Shinbundang Lines | — | OpenStreetMap (gate 3 on two lines; Line 1 not gated) | City | 129 / 0 |
| Bucheon | Line 1, Line 7, Seohae Line | — | OpenStreetMap (gate 3 on Line 7; Line 1 and Seohae not gated) | City | 121 / 0 |
| Namyangju | Line 4, Line 8, Gyeongui–Jungang Line, Gyeongchun Line | — | OpenStreetMap (no whole-line gate; each line's in-city stations read against its line table) | City | 105 / 0 |
| Ansan | Line 4, Suin–Bundang Line, Seohae Line | — | OpenStreetMap (gate 3 on the Suin–Bundang Line; Line 4 and Seohae not gated) | City | 110 / 0 |
| Uijeongbu | U Line, Line 1, Line 7 | — | OpenStreetMap (gate 3 on the U Line and Line 7; Line 1 not gated) | City | 126 / 0 |
| Anyang | Line 1, Line 4 | — | OpenStreetMap (no whole-line gate; each line's in-city stations read against its line table) | City | 106 / 0 |
| **Taiwan** | | | | | |
| Taichung | Taichung Metro Green Line | Taiwan Railway, high-speed rail | Operator's station table + OpenStreetMap route (gate 3 exact) | City | 0 / 0 |
| Taoyuan | Taoyuan Airport MRT (line A) | Taiwan Railway, high-speed rail | National station layer + OSM route (gate 3 exact, one dated addition) | City | 7 / 0 |
| Taipei (Regional) | Taipei Metro 5 lines + 2 branches, Circular, Sanying, Danhai and Ankeng LRT, Airport MRT | Taiwan Railway, high-speed rail, Maokong Gondola | OpenStreetMap (gate 3 exact on Taipei Metro's lines) | Two cities | 15 / 0 |
| **Japan** | | | | | |
| Kobe | Subway (Seishin-Yamate, Hokushin, Kaigan), Port Liner, Rokkō Liner, JR Kobe / Wadamisaki / Takarazuka, Hankyu Kobe, Hanshin Main, Sanyō Main, Kobe Kōsoku, Kobe Electric Arima / Sanda / Ao (15 lines) | Shinkansen, Maya and Rokkō cable cars | MLIT N02 railway data, collapsed on its station-group code; English names from OSM (gate 3 exact on the six in-city lines) | City (JR and private railways cut at the city line) | 32 / 0 |
| Osaka | Osaka Metro (Midōsuji, Tanimachi, Yotsubashi, Chūō, Sennichimae, Sakaisuji, Nagahori Tsurumi-ryokuchi, Imazatosuji), New Tram, JR Osaka Loop / Kyoto / Kobe / Tōzai / Gakkentoshi / Osaka Higashi / Yumesaki / Yamatoji / Hanwa, Hankyu Kobe / Takarazuka / Kyoto / Senri, Hanshin Main / Namba, Keihan Main / Nakanoshima, Kintetsu Namba / Osaka / Minami-Osaka, Nankai Main / Kōya / Shiomibashi, Hankai tram Hankai / Uemachi (34 lines) | Shinkansen; the Umeda freight track from Umekita to Fukushima (limited expresses only) | MLIT N02 railway data, collapsed on its station-group code and split into public lines by branch walks; English names from OSM, two from the operators' signs (gate 3 exact on ten lines) | City (JR and private railways cut at the city line; a station straddling it counts if any platform is inside) | 76 / 0 |
| Sapporo | Sapporo Municipal Subway (Namboku, Tōzai, Tōhō), the Sapporo Streetcar loop, JR Hakodate Main / Chitose / Gakuen Toshi (7 lines) | No Shinkansen reaches Sapporo yet | MLIT N02 railway data, collapsed on its station-group code, the streetcar's four N02 sections drawn as one loop; English names from OSM, 29 rewritten in one style with block numbers as figures (gate 3 exact on the three subway lines) | City (JR cut at the city line) | 4 / 0 |
| Fukuoka | Fukuoka City Subway (Kūkō, Hakozaki, Nanakuma), JR Kagoshima Main / Chikuhi / Fukuhoku Yutaka / Kashii, Nishitetsu Tenjin Ōmuta / Kaizuka (9 lines) | The Shinkansen; the JR Hakata-Minami line (only Hakata inside the city) | MLIT N02 railway data, collapsed on its station-group code; English names from OSM, 20 rewritten in one style (gate 3 exact on the three subway lines) | City (JR and Nishitetsu cut at the city line) | 22 / 0 |
| Kyoto | Kyoto Municipal Subway (Karasuma, Tōzai), JR Kyoto / Biwako / Sagano / Nara / Kosei, Keihan Main / Ōtō / Uji / Keishin, Hankyu Kyoto / Arashiyama, Kintetsu Kyoto, Randen Arashiyama Main / Kitano, Eiden Eizan Main / Kurama (18 lines) | The Shinkansen; the Sagano scenic line and the Eizan and Kurama funiculars (sightseeing) | MLIT N02 railway data, collapsed on its station-group code, 東海道線 split at Kyoto; English names from OSM, 41 rewritten in one style (gate 3 exact on five lines) | City (JR and the private lines cut at the city line) | 25 / 0 |
| Tokyo | JR East (Yamanote, Keihin-Tohoku, Chuo Rapid, Chuo-Sobu, Yokosuka / Sobu Rapid, Keiyo, Joban, Saikyo, Utsunomiya / Takasaki), Tokyo Metro (Ginza, Marunouchi, Hibiya, Tozai, Chiyoda, Yurakucho, Hanzomon, Namboku, Fukutoshin), Toei (Asakusa, Mita, Shinjuku, Oedo, Sakura Tram, Nippori-Toneri Liner), Tokyu (7), Keio (2), Odakyu, Seibu (4), Tobu (4), Keisei (3), Keikyu (2), Hokuso, Tsukuba Express, Rinkai, Yurikamome, Tokyo Monorail (52 lines, labelled on the map by line code) | The Shinkansen; the Narita Sky Access and the Saitama Railway (one station each in the wards, served by other lines); the Tokaido and Shonan-Shinjuku lines not drawn on their own | MLIT N02 railway data, collapsed on its station-group code; JR East drawn as nine services over its legal lines; English names from OSM in the operators' signage style (gate 3 exact on fifteen lines) | The 23 wards (lines cut at the ward line); 293 stations in the 15 wards without data drawn hollow | 55 / 0 |
| Yokohama | Subway (Blue, Green), JR East (Keihin-Tohoku / Negishi, Tokaido, Yokosuka, Sotetsu-JR Link, Yokohama, Nambu, Tsurumi), Keikyu (Main, Zushi), Tokyu (Toyoko, Den-en-toshi, Kodomonokuni, Shin-yokohama), Minatomirai, Sotetsu (Main, Izumino, Shin-yokohama), Kanazawa Seaside Line (20 lines) | The Shinkansen | MLIT N02 railway data, collapsed on its station-group code; JR East's 東海道線 drawn as four services over its legal lines; English names from OSM in the operators' signage style (gate 3 exact on seven lines) | City (JR and private railways cut at the city line) | 41 / 0 |
| Hiroshima | Astram Line, JR Sanyo / Kabe / Geibi / Kure, Hiroden streetcars (Main, Ujina, Eba, Yokogawa, Hakushima, Minami) and the Hiroden Miyajima Line (12 lines) | The Shinkansen | MLIT N02 railway data in its 2025 edition (the 2024 one predates Hiroden's 2025 route into Hiroshima Station), collapsed on its station-group code; English names from OSM in the operators' signage style (gate 3 exact on Astram and the Kabe Line) | City (JR and the Miyajima Line cut at the city line) | 13 / 0 |
| Matsuyama | Iyotetsu's city tram (one line over six legal sections), its Takahama, Yokogawara and Gunchu lines, and JR's Yosan Line (5 lines) | — (no Shinkansen runs here) | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM in Hiroshima's style (gate 3 exact on the Takahama Line) | City (the Yokogawara and Gunchu lines and JR cut at the city line) | 11 / 0 |
| Toyama | Chitetsu's city tram (one line over six legal sections) and Toyamako Line (Portram), its Main, Fujikoshi, Kamidaki and Tateyama lines, the Ainokaze Toyama Railway and JR West's Takayama Line (8 lines) | The Shinkansen; JR Central's Takayama Line (only Inotani inside) | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM and the tram operator's English line map in Hiroshima's style (gate 3 exact: tram 25, Portram 15) | City (Chitetsu's Main, Kamidaki and Tateyama lines and Ainokaze cut at the city line) | 22 / 0 |
| Kumamoto | The city tram (one line over five legal sections), Kumamoto Electric's Kikuchi and Fujisaki lines, JR Kyushu's Kagoshima Main and Hohi lines (5 lines) | The Shinkansen | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM in Hiroshima's style (gate 3 exact on the tram, 35) | City (Kumaden's Kikuchi Line and JR cut at the city line) | 10 / 0 |
| Fukui | Fukui Railway's Fukubu Line (street and railway, one line), Echizen Railway's Mikuni Awara and Katsuyama Eiheiji lines, the Hapi-line Fukui and JR's Etsumi-Hoku Line (5 lines) | The Shinkansen | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM in Hiroshima's style (no line wholly inside: gate 3 has no in-city count) | City (every line cut at the city line) | 14 / 0 |
| Nagasaki | Nagasaki Electric Tramway (one line over five legal sections) and JR Kyushu's Nagasaki Main Line (2 lines) | The Shinkansen | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM in Hiroshima's style (gate 3 exact on the tram, 38) | City (JR cut at the city line) | 6 / 0 |
| Utsunomiya | Utsunomiya Light Rail, Tobu Utsunomiya Line, JR Utsunomiya and Nikko lines (4 lines) | The Shinkansen | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM in Hiroshima's style (gate 3 exact on the light rail's 15 in-city stops) | City (the light rail, Tobu and JR cut at the city line) | 11 / 0 |
| Kitakyushu | Kitakyushu Monorail, Chikuho Electric Railroad, JR Kagoshima Main / Nippo Main / Hitahikosan / Wakamatsu / Fukuhoku Yutaka / Sanyo (8 lines) | The Shinkansen; the Sarakurayama cable car and the Mojiko Retro sightseeing train; Nishi-Kurosaki (closed 2026-07-31) | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM in Hiroshima's style (gate 3 exact on the Monorail) | City (JR and the Chikuho line cut at the city line) | 19 / 0 |
| Sakai | The Hankai tram, Osaka Metro's Midōsuji Line, Nankai (Main, Kōya, Semboku) and JR Hanwa (6 lines) | — (no Shinkansen runs here) | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM in Hiroshima's style (gate 3 exact on the Hankai tram and the Midōsuji) | City (every line cut at the city line; the Midōsuji keeps 3 stations and the Hankai tram 15 of 31 stops, Osaka's map drawing the rest) | 31 / 0 |
| Hakodate | The Hakodate City Tram (one line over four legal sections), JR's Hakodate Line and the South Hokkaido Railway (3 lines) | — (no Shinkansen station in the city) | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM in Hiroshima's style (gate 3 exact on the city tram) | City (JR and the South Hokkaido Railway cut at the city line, the latter to one station) | 4 / 0 |
| Kagoshima | The Kagoshima City Tram (one line over four legal sections), JR Ibusuki Makurazaki / Kagoshima Main / Nippo Main (4 lines) | The Shinkansen | MLIT N02 railway data in its 2025 edition (the 2024 one lacks Sengan-en), collapsed on its station-group code; English names from OSM in Hiroshima's style (gate 3 exact on the tram, 35) | City (JR cut at the city line) | 3 / 0 |
| Okayama | Okaden Higashiyama / Seikibashi, JR Sanyo / Ako / Momotaro / Tsuyama / Uno Minato / Seto-Ohashi (8 lines) | The Shinkansen | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM in Hiroshima's style (gate 3 exact on both Okaden lines, from its timetables) | City (JR cut at the city line) | 14 / 0 |
| Kōchi | Tosaden's Ino, Gomen, Sanbashi and Ekimae tram lines and JR's Dosan Line (5 lines) | — (no Shinkansen runs here) | MLIT N02 railway data in its 2025 edition, collapsed on its station-group code; English names from OSM in Hiroshima's style (gate 3 exact on the Sanbashi and Ekimae lines) | City (the Ino and Gomen lines and JR cut at the city line) | 19 / 0 |
| **Germany** | | | | | |
| Berlin | U-Bahn U1–U9 and the S-Bahn's 16 lines (the Ring S41/S42 among them) | Trams, regional trains, ferries; the U6's Tegel branch (closed for works until about August 2027) | VBB GTFS (gate 3 exact: U-Bahn 170 = 175 less 5 closed, S-Bahn 168) | Land of Berlin (lines cut at the Land boundary) | 41 / 0 (36 in Brandenburg, 5 closed for works) |
| **United Kingdom** | | | | | |
| London | Underground (11 lines), DLR, Elizabeth line and the six London Overground lines (19 lines, short names on the map, full names in the legend) | Tramlink, National Rail, river buses | OpenStreetMap route relations (TfL publishes no GTFS; its API's line strings are straight lines between stations); 8 stations OSM's relations omit added from its station nodes; gate 3 exact on 14 counts | Greater London (lines cut at the boundary) | 32 / 0 |
| Glasgow | Glasgow Subway (one 15-station loop, its two tunnels drawn as one line) | Suburban and national rail (the Argyle and North Clyde lines and the rest) | OpenStreetMap route relations (SPT publishes no GTFS for the Subway); gate 3 exact on 15 | Glasgow City (the loop lies wholly inside) | 0 / 0 |
| Newcastle (Regional) | Tyne and Wear Metro, Green and Yellow lines (the Sunderland branch included) | Northern's national rail trains | OpenStreetMap route relations; gate 3 exact on 60 | The five Tyne and Wear districts | 0 / 0 |
| **Argentina** | | | | | |
| Buenos Aires | Subte Líneas A–E and H | Premetro, heritage tramway, commuter railways | SBASE's station and track layers (BA Data); names from OpenStreetMap; gate 3 exact on six lines against SBASE and OSM | Ciudad Autónoma (all 89 stations inside) | 0 / 0 |
| **Australia** | | | | | |
| Sydney | Sydney Trains T1, T2, T3, T4, T8 and T9 and Sydney Metro M1 (7 lines, refs on the map, full names in the legend) | Light rail L1-L3 (22 stops in the LGA), NSW TrainLink, ferries | OpenStreetMap route relations (Transport for NSW's GTFS needs an API key); gate 3 exact on the 16 stations inside the LGA | The City of Sydney LGA (lines cut at the boundary) | 157 / 0 |
| Melbourne | Metro Trains Melbourne by line group: Burnley, Clifton Hill, Northern, Cross City, Frankston, Metro Tunnel (6 lines, the group on the map, its lines in the legend) | Trams (22 routes, 155 stops in the LGA), the event-day Flemington Racecourse line, the City Circle, V/Line | OpenStreetMap route relations (119, assigned to groups by line name); gate 3 exact on the 17 stations inside the LGA | The City of Melbourne LGA (lines cut at the boundary) | 199 / 0 |
| **Switzerland** | | | | | |
| Zurich | VBZ trams 2–11, 13–15, 17 and the 2026 construction lines 50 and 51 | S-Bahn; Forchbahn S18; trams 12 (Glattalbahn) and 20 (Limmattalbahn), stubs | OpenStreetMap route relations; gate 3 exact (ZVV) | City (Stadt Zürich) | 15 / 0 |

### B. Business data (dimensions 4–6)

The in-ring pin counts were re-read from each committed map's layer menu on
2026-09-29, after the exclusions batch re-rendered 41 maps.

| City | Source kind | Source | Classification | In-ring pins R / F / P | Missing or thin |
|---|---|---|---|---|---|
| **United States** | | | | | |
| San Diego | Tax register | Business Tax Certificates | NAICS | 1,079 / 551 / 598 | Undercount: neighbourhoods registered under own name (PLAN) |
| San Francisco | License register | Registered Business Locations | NAICS | 5,038 / 4,591 / 2,091 | Floor: about 37% of rows have NAICS (DEC) |
| Los Angeles | Tax register | Listing of Active Businesses | NAICS | 8,069 / 3,817 / 2,014 | Floor: about 9% of rows lack NAICS (DEC) |
| Chicago | License register | Business Licenses | Own licence types | 5,476 / 4,196 / 2,049 | — |
| New York | 4 activity registers | DOHMH, NYS food stores, NYS salons, DCWP | Per-source dispatch | 14,822 / 22,060 / 7,478 | Retail thin |
| Philadelphia | License register (activities) | L&I Business Licenses | Own licence types | 770 / 4,081 / — | No Personal services; Retail = food retail |
| Miami (Regional) | Tax register | Local Business Tax (county) | Own CATGRYNAME (NAICS column empty) | 1,961 / 1,215 / 557 | Repair and service premises under-counted |
| Boston | 3 activity registers | Food inspections, Licensing Board, cannabis | Per-source dispatch | 530 / 1,880 / — | No Personal services; Retail = food, package, cannabis |
| Washington D.C. | License register | Basic Business License | Own BUSINESSACTIVITY | 899 / 2,603 / 345 | "Delicatessen" (1,065) ambiguous, counted as Food |
| Buffalo | 3 activity registers | City Business Licenses, NYS food stores, NYS salons | Per-source dispatch | 113 / 188 / 75 | Retail thin |
| Sacramento | Tax register | Business Operation Tax Information | Own Business_Description | 625 / 510 / 243 | — |
| Houston | Tax register | Texas Comptroller, Active Sales Tax Permit Holders (state) | NAICS | 1,077 / 1,052 / 94 | Personal services thin: a sales-tax permit is held by sellers of taxable goods and services |
| Minneapolis | Food hygiene register | City of Minneapolis Food Inspections, one row per violation | Its own FacilityCategory, plus a name test | 115 / 526 / — | No Personal services; Retail = food shops only ("Grocery and food shops") |
| Pittsburgh | Food hygiene register | Allegheny County Health Department's Geocoded Food Facilities (as of 2025), one row per facility | Its own category_cd, plus a name test | 48 / 268 / — | No Personal services; Retail = food shops only ("Food-selling shops") |
| Dallas | Tax register | Texas Comptroller, Active Sales Tax Permit Holders (state) | NAICS | 2,501 / 1,492 / 204 | Personal services thin: a sales-tax permit is held by sellers of taxable goods and services |
| Kansas City | License register | KCMO Business License Holders (frozen 2026-01-15) | NAICS (2022 titles mapped to codes) | 273 / 52 / 126 | Food service thin: about 175 restaurants and bars in the whole register; 1,095 fee-code licences unclassifiable |
| Tucson | License register | City of Tucson BUSLIC (active licences, rebuilt daily) | NAICS | 125 / 149 / 66 | Not a complete listing, in the City's own words |
| New Orleans | License register | City of New Orleans Active Occupational Licenses (daily, CC0) | Own text taxonomy, mapped to NAICS codes | 935 / 978 / 218 | Personal services thin |
| **Canada** | | | | | |
| Vancouver (Regional) | 2 licence registers | Vancouver licences; Surrey directory | Own types (both) | 1,847 / 1,818 / 953 | — |
| Montréal | Street survey | Locaux commerciaux (annual) | NAICS (SCIAN = NAICS) | 4,852 / 4,070 / 1,464 | Edge municipalities thinner in the survey |
| Calgary | License register | Business Licences | Own licencetypes | 1,962 / 2,869 / 1,325 | Food over Retail (dual-licence rule) |
| Edmonton | License register | Business Licences | Own licence categories | 1,038 / 925 / 411 | Personal services overstated (clinics) |
| Kitchener–Waterloo (Regional) | Health inspection register | Region of Waterloo Public Health's food and personal-services inspection layers, typed from its bulk tables | Its own inspection types (SUBCATEGORY), plus a name test | 143 / 545 / 177 | Retail = food shops only ("Food shops"); no general-retail register |
| Toronto | License register | MLS licences | Own MLS category | 328 / 6,471 / 1,950 | Retail = regulated slice only |
| Ottawa | Food hygiene register | Ottawa Public Health's food-safety inspection data (LIVES), one record per premises | None: a premises kind from the name | — / 1,586 / — | No Personal services; no Retail layer: food shops sit inside the one layer, labelled "Restaurants and food shops" |
| **Mexico** | | | | | |
| Mexico City | National statistical register | INEGI DENUE | SCIAN | 94,642 / 24,798 / 12,018 | Street stalls excluded |
| Guadalajara (Regional) | National statistical register | INEGI DENUE | SCIAN | 26,341 / 6,698 / 3,623 | Street stalls excluded |
| Monterrey (Regional) | National statistical register | INEGI DENUE | SCIAN | 10,164 / 3,057 / 1,343 | Street stalls excluded |
| **Spain** | | | | | |
| Madrid | Premises census | Censo de locales | Own epígrafe | 26,197 / 15,171 / 8,032 | — |
| Barcelona | Street survey (2022) | Cens de locals en planta baixa | Own 4-level scheme (finest level) | 20,287 / 9,976 / 5,673 | 458 mixed retail/wholesale rows dropped |
| Palma | License register | The Consell de Mallorca's register of restaurant and entertainment establishments (GOIB catalogue) | Its own types (Grup), plus a name test | — / 1,187 / — | No Retail; No Personal services |
| **Ireland** | | | | | |
| Dublin | Property register | Rateable valuation list | Register's own "Uses" | 5,225 / 1,703 / 532 | — |
| **Italy** | | | | | |
| Milan | 6 licence registers | Comune di Milano premises registers | Register = category | 24,793 / 11,738 / 4,979 | Canteens and clubs partly left in Food |
| Rome | Authorisation register | SUAP | Own authorisation types | 38,121 / 14,534 / 8,084 | Workshops with no trade missing |
| Florence | Permit registers | Comune di Firenze's four activity layers (CC BY 4.0) | Layer and type | 2,676 / 1,086 / 673 | Exempt food service kept: some not open to the public |
| **France** | | | | | |
| Paris | National establishment register | SIRENE + INSEE geolocation | NAF rév. 2 (sous-classe) | 40,771 / 32,871 / 11,605 | — |
| Marseille | same | same | same | 4,558 / 3,852 / 1,537 | — |
| Toulouse | same | same | same | 2,438 / 2,162 / 933 | — |
| Lille (Regional) | same | same | same | 3,166 / 2,942 / 1,057 | — |
| Rennes | same | same | same | 1,105 / 906 / 343 | — |
| Le Mans | same | same | same | 693 / 475 / 294 | — |
| Besançon | same | same | same | 657 / 445 / 198 | — |
| Avignon | same | same | same | 284 / 233 / 105 | — |
| Tours | same | same | same | 875 / 577 / 289 | — |
| Dijon | same | same | same | 848 / 632 / 297 | — |
| Reims | same | same | same | 683 / 520 / 254 | — |
| Orléans | same | same | same | 788 / 522 / 258 | — |
| Mulhouse | same | same | same | 769 / 585 / 350 | — |
| Brest | same | same | same | 774 / 499 / 244 | — |
| Saint-Étienne | same | same | same | 1,020 / 914 / 342 | — |
| Nice | same | same | same | 3,397 / 2,980 / 1,709 | — |
| Montpellier | same | same | same | 2,209 / 2,234 / 1,000 | — |
| Strasbourg | same | same | same | 2,076 / 1,900 / 803 | — |
| Le Havre | same | same | same | 680 / 502 / 279 | — |
| Caen | same | same | same | 733 / 610 / 224 | — |
| Rouen (Regional) | same | same | same | 1,256 / 867 / 461 | — |
| Bordeaux (Regional) | same | same | same | 3,626 / 3,308 / 1,447 | — |
| Nantes (Regional) | same | same | same | 1,916 / 1,576 / 654 | — |
| Grenoble (Regional) | same | same | same | 1,913 / 1,868 / 753 | — |
| Valenciennes (Regional) | same | same | same | 790 / 549 / 270 | — |
| Angers | same | same | same | 843 / 715 / 349 | — |
| **Norway** | | | | | |
| Oslo | National establishment register | Enhetsregisteret sub-units | SN2025 (NACE Rev. 2.1) | 4,197 / 2,082 / 1,801 | — |
| Bergen | National establishment register | Enhetsregisteret sub-units | SN2025 (NACE Rev. 2.1) | 1,204 / 484 / 418 | — |
| **Sweden** | | | | | |
| Stockholm | Food hygiene register | Stockholms stad's food inspection register (Livsmedelstillsyn), one record per premises | Its own activity types (VerksamhetsTyp), plus a name test | 943 / 3,759 / — | No Personal services; Retail = food shops only ("Food shops"); frozen since 2025-10-21 |
| Göteborg | Food hygiene register | Göteborgs Stad's register of food businesses (Livsmedelsverksamheter, CC0, refreshed daily), one row per premises | Its own local types (`typ`), mapped to the national groups, plus a name test | 609 / 1,646 / — | No Personal services; Retail = food shops only ("Food shops"); the register carries no dates |
| **Romania** | | | | | |
| Bucharest | Food hygiene register | DSVSA București's registers of food units (17 category files, active rows only) | The file (the unit category), with the category text for exceptions | 5,250 / 5,994 / — | No Personal services; Retail = food shops only ("Food shops"); a quarter of premises unplaced |
| **Denmark** | | | | | |
| Copenhagen | National establishment register | CVR production units | DB25 (NACE Rev. 2.1) | 7,061 / 4,333 / 2,708 | Tattoo studios lost with the catch-all |
| Aarhus | National establishment register | CVR production units | DB25 (NACE Rev. 2.1) | 636 / 450 / 214 | Tattoo studios lost with the catch-all |
| Odense | National establishment register | CVR production units | DB25 (NACE Rev. 2.1) | 603 / 343 / 208 | Tattoo studios lost with the catch-all |
| **Czechia** | | | | | |
| Prague | National registers (location + activity) | ROS02 + RES | CZ-NACE 2025 (owner's activity) | 6,027 / 5,464 / 6,122 | About 57,000 establishments of other-activity owners missing |
| Brno | same | same | same | 1,955 / 1,773 / 2,204 | About 18,800 establishments of other-activity owners missing |
| Plzeň | same | same | same | 783 / 608 / 1,117 | About 7,200 establishments of other-activity owners missing |
| Olomouc | same | same | same | 587 / 483 / 672 | About 4,800 establishments of other-activity owners missing |
| Ostrava | same | same | same | 956 / 773 / 1,212 | About 9,000 establishments of other-activity owners missing |
| Liberec (Regional) | same | same | same | 449 / 352 / 604 | About 6,200 establishments of other-activity owners missing |
| Most (Regional) | same | same | same | 299 / 153 / 212 | About 2,000 establishments of other-activity owners missing |
| **Netherlands** | | | | | |
| Amsterdam | Permit list + building register | Horeca permits; BAG shop units | Per-source (2 buckets) | Shops & services 9,215 / Food 3,433 | Retail and Personal merged |
| Rotterdam | Gazette notices + building register | Permit notices; BAG shop units | Per-source (2 buckets) | Shops & services 5,211 / Food 1,771 | Retail and Personal merged |
| Den Haag | Permit layer + building register | The Gemeente's Horecavergunningen layer; BAG shop units | Per-source (2 buckets) | Shops & services 3,813 / Food 1,968 | Retail and Personal merged |
| **Brazil** (all nine) | Census of addresses (2022) | IBGE CNEFE | Free-text keyword rules | see below | A third to a half of plausible storefronts unreadable |
| São Paulo | | | | 25,968 / 15,331 / 8,256 | about 1/3 unreadable |
| Rio de Janeiro | | | | 15,085 / 10,364 / 4,784 | about 1/3 |
| Belo Horizonte | | | | 4,634 / 2,355 / 1,404 | about 4 in 10 |
| Brasília | | | | 2,808 / 1,246 / 1,009 | about 4 in 10 |
| Salvador | | | | 5,131 / 3,312 / 1,613 | about 1/3 |
| Fortaleza (Regional) | | | | 5,255 / 1,964 / 1,295 | about 4 in 10 |
| Porto Alegre (Regional) | | | | 4,660 / 1,516 / 1,224 | almost half; about half near stations |
| Recife (Regional) | | | | 6,547 / 2,058 / 1,753 | about 4 in 10 |
| Santos (Regional) | | | | 3,113 / 1,482 / 790 | almost 4 in 10 |
| **Hong Kong** | | | | | |
| Hong Kong | License registers (food premises) | FEHD licence registers | Local (licence type) | Food service 15,833 / Food shops 3,408 / Bathhouses 34 | No general retail or personal services: FEHD does not license them |
| **Latvia** | | | | | |
| Riga | Excise licences + cadastre | VID excise-licence register; VZD premise groups | Per-source (2 buckets) | Shops & services 4,027 / Food 1,214 | Retail and Personal merged; food only where alcohol or tobacco is licensed |
| Liepāja | Excise licences + cadastre | VID excise-licence register; VZD premise groups | Per-source (2 buckets) | Shops & services 397 / Food 92 | Retail and Personal merged; food only where alcohol or tobacco is licensed |
| Daugavpils | Excise licences + cadastre | VID excise-licence register; VZD premise groups | Per-source (2 buckets) | Shops & services 581 / Food 75 | Retail and Personal merged; food only where alcohol or tobacco is licensed |
| **South Korea** | | | | | |
| Seoul | Permit registers (17 types) | Seoul's LOCALDATA permit registers | Local (permit type) | 47,933 / 139,802 / 36,646 | Retail only the licensed trades; no general retail |
| Daegu | Permit registers (14 types) | Daegu's republication of the national LOCALDATA registers (D-데이터허브) | Local (permit type) | 11,031 / 27,271 / 9,422 | Retail only the licensed trades; no general retail |
| Busan | Permit registers (14 types) | Busan's LOCALDATA API (the national permit registers) | Local (permit type) | 14,330 / 39,487 / 12,531 | Retail only the licensed trades; no general retail |
| Incheon | National register | SEMAS's 상가(상권)정보 (the national storefront register) | SEMAS's own (소분류) | 21,719 / 25,983 / 8,724 | — |
| Goyang | National register | SEMAS's 상가(상권)정보 | SEMAS's own (소분류) | 7,358 / 8,243 / 2,918 | — |
| Seongnam | National register | SEMAS's 상가(상권)정보 | SEMAS's own (소분류) | 7,487 / 8,982 / 2,949 | — |
| Yongin | National register | SEMAS's 상가(상권)정보 | SEMAS's own (소분류) | 4,991 / 6,052 / 1,960 | — |
| Suwon | National register | SEMAS's 상가(상권)정보 | SEMAS's own (소분류) | 5,816 / 7,541 / 2,571 | — |
| Bucheon | National register | SEMAS's 상가(상권)정보 | SEMAS's own (소분류) | 6,999 / 8,087 / 3,007 | — |
| Namyangju | National register | SEMAS's 상가(상권)정보 | SEMAS's own (소분류) | 4,008 / 4,436 / 1,623 | — |
| Ansan | National register | SEMAS's 상가(상권)정보 | SEMAS's own (소분류) | 4,833 / 5,760 / 1,982 | — |
| Uijeongbu | National register | SEMAS's 상가(상권)정보 | SEMAS's own (소분류) | 4,445 / 4,928 / 1,805 | — |
| Anyang | National register | SEMAS's 상가(상권)정보 | SEMAS's own (소분류) | 3,811 / 4,453 / 1,483 | — |
| **Taiwan** | | | | | |
| Taichung | National tax register | FIA business tax register | Industry code division | 6,283 / 3,970 / 1,932 | One line in a large city: 19% of storefronts in a ring |
| Taoyuan | National tax register | FIA business tax register | Industry code division | 2,455 / 1,813 / 821 | The airport line misses the city's largest centre: 12% in a ring |
| Taipei (Regional) | National tax register | FIA business tax register | Industry code division | 54,595 / 33,575 / 12,069 | Market stalls unplaced (about 3,600) |
| **Japan** | | | | | |
| Kobe | Permit register | City food-permit list + barber, beauty and laundry registers | Permit type (営業の種類) | 2,619 / 16,980 / 4,186 | Retail is food only (no general licence in Japan); notification-only food businesses (届出) absent |
| Osaka | Permit register | City food-permit list + barber, beauty and laundry registers | Permit type (業種分類) | 6,418 / 50,109 / 15,145 | Retail is food only (no general licence in Japan); notification-only food businesses (届出) absent; the list holds about 70% of the restaurant permits Osaka reports nationally (disclosed, owner-approved wording) |
| Sapporo | Permit register | City food-permit list + barber, beauty, laundry and coin-laundry registers | Permit type (業種名) | 2,111 / 16,222 / 4,668 | Retail is food only (no general licence in Japan); notification-only food businesses (届出) absent; coin laundries counted as Personal services (owner) |
| Fukuoka | Permit register | City food-permit list (pre-2021-06 permits) + MHLW's online filings + barber, beauty and laundry registers | Permit type (業種 / 営業の種類), read with the form of business (業態) | 5,185 / 14,764 / 4,670 | Retail is food only (no general licence in Japan) and partial: notification-only food shops appear only where they published in MHLW's opt-in list; about one restaurant in five withheld its address (disclosed) |
| Kyoto | Permit register, REBUILT | The 2021 food list + every monthly list since, in term on 2026-07-31; barber, beauty and laundry lists + their months | Permit type (業種) | 3,736 / 19,318 / 4,926 | An upper bound: closures are not published; Retail is food only, and packaged-only sale (a notification since 2021) absent |
| Tokyo | Permit lists, per ward (8 of 23) | Eight wards' own food lists + MHLW's filings for four; the barber, beauty and laundry registers of four | Permit type (業種) | 11,952 / 39,380 / 8,557 | Business data for 8 of 23 wards only (15 hollow); the lists run 9% to 101% of the official count; Retail = food only |
| Yokohama | Permit registers (personal services) | City barber, beauty and laundry registers | Register (理容所 / 美容所 / クリーニング所) | — / — / 6,540 | No food or retail list published: Personal services only |
| Hiroshima | Permit register | City food-permit list (counter applications) + MHLW's online filings | Permit type (営業の種類), read with the form of business (業態, 許可条件) | 1,889 / 7,245 / — | No Personal services (the city publishes new openings only); Retail = food retail, and partial: notification-only food shops appear only where they published in MHLW's opt-in list; about one restaurant in seven withheld its address (disclosed) |
| Matsuyama | Permit register | City food-permit lists (old and new law) and barber, beauty and laundry lists + MHLW's notifications | Permit type (営業の種類), read with the form of business (業態) | 674 / 3,595 / 867 | Retail = food retail, and partial: notification-only food shops appear only where they published in MHLW's opt-in list |
| Toyama | Permit register | City food-permit list and barber, beauty and laundry registers (MHLW's file a point source only) | Permit type (営業の種類) | 329 / 2,212 / 509 | Retail = food retail permits only; notification-only food shops absent |
| Kumamoto | Permit register | City restaurant list (counter applications) + MHLW's online filings + city barber, beauty and laundry lists | Permit type (業種 / 営業の種類), read with the form of business (業態) | 218 / 4,289 / 983 | Retail = MHLW's opt-in food retail only; about 76% of restaurants in force are in the two lists |
| Fukui | Permit register | City month-end food-permit list (fixed premises) and barber, beauty and laundry lists | Permit type (業種) | 373 / 1,916 / 693 | Retail = food retail permits only; notification-only food shops absent; food trucks and stalls not in the list |
| Nagasaki | Permit register | City BODIK lists (a 2023 snapshot: food, barber, beauty, laundry) + MHLW's current online filings | Permit type (営業の種類), read with the form of business (業態) | 776 / 2,731 / 704 | Retail = food retail, and partial (MHLW's opt-in notifications); personal services frozen at 2023-03-31 |
| Utsunomiya | Permit register | City old-law food list and barber, beauty and laundry lists + MHLW's filings | Permit type (業種名 / 営業の種類), read with the form of business (業態) | 695 / 2,424 / 670 | Retail = food retail, and partial: notification-only food shops appear only where they published in MHLW's opt-in list; about one restaurant in 130 withheld its address |
| Kitakyushu | Permit register | City old-law food list (in term on 2026-08-31) and barber and beauty registers + MHLW's filings | Permit type (営業の種類), read with the form of business (業態) | 2,297 / 6,264 / 2,026 | No laundries (no list); Retail = food retail, and partial; about one restaurant in seven withheld its address (disclosed) |
| Sakai | Permit register | City food-permit list, rebuilt to 2026-08-31 from its monthly new permits and closures + MHLW's notifications | Permit type (営業の種類), read with the form of business (業態) | 1,591 / 4,455 / — | No Personal services (the city's lists are PDFs); Retail = food retail, and partial: notification-only food shops appear only where they published in MHLW's opt-in list |
| Hakodate | Permit registers (personal services) | City barber, beauty and laundry registers | Register (理容所 / 美容所 / クリーニング所) | — / — / 331 | No food register published (new permits only): Personal services only |
| Kagoshima | Permit register | City old-law food list + MHLW's filings | Permit type (営業の種類), read with the form of business (業態) | 695 / 3,280 / — | No Personal services (new openings only); Retail = food retail, and partial; about one restaurant in four withheld its address (disclosed) |
| Okayama | Permit register | MHLW's filings only | Permit type (営業の種類), read with the form of business (業態) | 972 / 3,202 / — | No Personal services (PDF lists, not reusable); Retail = food retail, and partial; about one restaurant in four withheld its address (disclosed); permits from before 2021-06 absent |
| Kōchi | Permit registers (personal services) | City barber and beauty-salon lists + monthly additions | Register (理容所 / 美容所) | — / — / 677 | No food (MHLW's list publishes about half the restaurants' addresses) and no laundry list: barbers and beauty salons only |
| **Germany** | | | | | |
| Berlin | Chamber of commerce register | IHK Berlin's Gewerbedaten (members' premises; no names) | WZ 2025 (NACE Rev. 2.1) | 30,800 / 15,472 / 3,121 | No hairdressers or laundries: crafts are not IHK members, so Personal services is thin by construction |
| **United Kingdom** | | | | | |
| London | Food hygiene register | The Food Standards Agency's FHRS files, 33 boroughs | FSA business type | 12,360 / 29,214 / — | No Personal services; Retail = food shops only ("Food shops") |
| Glasgow | Food hygiene register | Glasgow City Council's entries in Scotland's FHIS (Food Standards Scotland), from the FSA's open-data file | FSA business type | 405 / 1,588 / — | No Personal services; Retail = food shops only ("Food shops") |
| Newcastle (Regional) | Food hygiene register | The Food Standards Agency's FHRS files, 5 councils | FSA business type | 989 / 2,369 / — | No Personal services; Retail = food shops only ("Food shops") |
| **Argentina** | | | | | |
| Buenos Aires | Street survey (2022–2024) | The city's Relevamiento Usos del Suelo (BA Data; no names) | Survey's own use subtypes (385, enumerated) | 30,586 / 6,987 / 4,612 | Malls and arcades not itemised (593 left out); unidentified shopfronts (6,243, 7.2%) dropped |
| **Australia** | | | | | |
| Sydney | Street survey or census | The City of Sydney's Floor Space and Employment Survey, 2022 (FES Industry of occupation; no names) | ANZSIC 2006 class | 2,490 / 2,769 / 642 | One council, the City of Sydney; points per building; religious and membership organisations, parking, clubs, catering, funerals, brothels and other personal services n.e.c. excluded by class |
| Melbourne | Street survey or census | The City of Melbourne's Census of Land Use and Employment, 2024 (CLUE; trading names) | ANZSIC 2006 class | 1,768 / 2,546 / 446 | One council, the City of Melbourne; points per property; the same class exclusions as Sydney |
| **Switzerland** | | | | | |
| Zurich | License register | Stadt Zürich's Gastwirtschaftsbetriebe (CC0), food-and-drink and alcohol-retail licences | Its own licence types (betriebsart) | 926 / 2,173 / — | No Personal services; Retail = shops licensed to sell alcohol only ("Licensed shops") |

### C. Location, coverage and city-specific exclusions (dimensions 7–9)

| City | Location method (rate) | Coverage gaps disclosed | City-specific exclusions (privacy / other) |
|---|---|---|---|
| **United States** | | | |
| San Diego | Source coordinates (98.4% populated) | None on page | Nonstore 454, parking (project-wide) |
| San Francisco | Source point | Surface stops thinned | 812990 "solo massage"; individual practitioner licences (tattoo, massage), 2026-10-01 |
| Los Angeles | Source + Census geocoder for corrupt points (98.7% recovered) | Corrupt coordinates geocoded | 812990 catch-all (30.7% of storefronts) |
| Chicago | Source coordinates | Licences without coordinates left off | Home-based, peddlers, endorsements, Limited Business |
| New York | Source + Census geocoder (582 of 1,449 recovered; 1.4% lost) | Retail thin; possible double counts | Person-held licences, contractors, chair renters |
| Philadelphia | Source geometry | Newsstands mostly absent | Rental (79% of register), short-let hosts |
| Miami (Regional) | Source coordinates | Repair/service undercount | SERVICE BUSINESS, professional, apartments, LAUNDRY MACHINE |
| Boston | Source coordinates (state plane) | Residence check reads zero by construction | Dormitories, lodging, Common Victualler (counted via food data) |
| Washington D.C. | Register X/Y + Census geocoder (387 of 451, 85.8%; 64 lost) | Delicatessen ambiguity | Residential rentals (61%), General Business, school cafeterias, caterers |
| Buffalo | Register coordinates (14 rows without a point lost) | Retail thin; possible double counts | Expired licences, caterers, sidewalk cafés, chair renters, salons at an apartment; person-named salons shown by type |
| Sacramento | Census geocoder (98.0% of addresses matched; 125 outside the city by postal address) | "ON FILE" addresses withheld and unplaceable | Expired licences, two catch-alls, online, mobile and cottage food, individual stylists and massage technicians, repairs, apartments; person-like names shown by type |
| Houston | Address join to the City's Site Addresses (83.9%) + Census geocoder (12.4%); 3.7% unplaced, 608 outside the city | Only taxable sellers hold a permit | Non-store sellers, caterers, mobile food, parking; apartments, trailers and a person's permit at a Residential point; address shown for a person's permit |
| Minneapolis | Register coordinates (97.8%); 42 not placed | Food only; 3 uncategorised facilities left out | Institutions, caterers, mobile units, stalls, food shelves and wholesale by type; contract and institutional kitchens, vending, hotels, venues, pharmacies and named cabarets by name; a grocer's second licence for one counter folded |
| Pittsburgh | Register coordinates (98.7%); 22 not placed, 3 outside the city | Food only; a list dated 2025-08-27 | Institutional, mobile, school, processing, boarding, commissary, caterer, social-club and banquet types; venue stands, workplace micro-markets, hospital and campus outlets, hotel back of house, pharmacies, dark stores and named adult venues by name |
| Dallas | Address join to the City's Address Points (89.8%) + Census geocoder (7.9%); 2.3% unplaced, 770 outside the city | Only taxable sellers hold a permit | Non-store sellers, caterers, mobile food, parking; apartments and trailers; address shown for a person's permit (Houston's Residential-point test cannot run: the address type codes are undocumented) |
| Kansas City | Register coordinates (100%); 11 outside the city | Food service thin; a licence is not a shopfront | Non-store sellers, caterers, mobile food, parking; fee-code licences (1,095); licences that lapsed in 2024; address shown for a person's licence or a person-named trade name |
| Tucson | Register coordinates (92.4%); 539 not geocoded, 23 outside the city | The City calls its list not complete | Home occupations; non-store sellers, caterers, mobile food, parking; apartments (19); address shown for a person's licence or a business named only as a person |
| New Orleans | Register coordinates (95.6%); 219 at the register's 0,0, 1 outside the city | A licence is not a shopfront | Event and festival vendors, home offices, flea-market stalls, street artists, video poker; caterers, mobile food, parking; address shown where no business name or a person's |
| **Canada** | | | |
| Vancouver (Regional) | Source coordinates | About half of Vancouver's register has none; 1,583 address rows lost | Surrey Home Occupation (51.8%), IMBL, RMT massage |
| Montréal | Source LAT/LONG (100%) | Two municipalities not surveyed | Vacant units (about 3,500) |
| Calgary | Source point | No home-business flag | Endorsements; body rub / escort (sensitivity) |
| Edmonton | Source coordinates | Personal services overstated | Non-commercial licence types (43%); adult services (sensitivity) |
| Kitchener–Waterloo (Regional) | Register coordinates (100% of kept premises) | Food and personal services only, no general-retail register; current by inspection within two years; 61 premises newer than the typed tables kept by default | Institutional kitchens, caterers, banquet halls and warehouses by type; campus and hospital outlets, venue stands, clubs, cinemas, hotels, pharmacies, mobile units and the Kitchener Market's Saturday stalls by name; a studio under a person's name shows its type |
| Toronto | Address join to One Address Repository (93.8%) | Retail absent; plazas under-counted | Cancelled licences; endorsements; person-held; adult premises (sensitivity) |
| Ottawa | Feed coordinates (99.6% of kept premises); 14 not placed, 8 outside the City | Food only; no type field, so restaurants and food shops are one layer; current by inspection within two years | Institutional kitchens, event caterers, clubs and arenas, mobile vendors, hotels and funeral homes by name |
| **Mexico** | | | |
| Mexico City | Source coordinates (100%) | Street stalls not shown | Semifijo units, SCIAN 469, 812410 |
| Guadalajara (Regional) | Source coordinates | Street stalls not shown | Same as Mexico City; Tonalá |
| Monterrey (Regional) | Source coordinates | Street stalls not shown | Same as Mexico City; 22 located outside the four municipios dropped |
| **Spain** | | | |
| Madrid | Source coordinates; 9.2% zero, dropped | 1 premises in 11 cannot be placed | Accommodation, wholesale, repair, no-shopfront |
| Barcelona | Source coordinates; no zero-coordinate rows (`baseline.json`: 0 of 58,908) | Survey is 2022 | Vacant units (1 in 9), hotels, 458 mixed rows |
| Palma | Register coordinates (13.2%) and joined by address to Catastro's points (66.4%); 20.4% unplaced | Food only; a premises with no street number, or on a street the two sources spell differently, is unplaced | Caterers by type; sports, golf and nautical clubs, cinemas, bingo halls, casinos, parish, school and clinic bars, bare hotel names and adult venues by name |
| **Ireland** | | | |
| Dublin | Source coordinates (ITM) | Large areas with no rail | No names published at all |
| **Italy** | | | |
| Milan | Source coordinates (loss count UNKNOWN) | Canteens/clubs partly remain; double counts | Registers not merged |
| Rome | Address join to ANNCSU (95.7%) | Food an upper bound (no closing dates) | Online, wholesale, storage types; workshops with no trade |
| Florence | Source coordinates (100%) | Some exempt food service not open to the public; no names or addresses | Private clubs, internal shops, nonstore, farmers, catering, hotel restaurants |
| **France** | | | |
| Paris | Join to INSEE geolocation (99.96%) | 1.8× OSM shop count; INSEE masking 8.5% (EC) | 47.91/47.99/47.8x, 56.29, 96.01A, 96.09Z |
| Marseille | same (99.94%) | 2.6× OSM (1.7× on restaurants); masking 12.2% (brief, sample) | Same codes |
| Toulouse | same (99.93%) | Masking 20.2%; 14 stations out | Same codes |
| Lille (Regional) | same (99.98%) | Masking 16.6% | Same codes |
| Rennes | same (99.97%) | Masking 17.5% | Same codes |
| Le Mans | same (100.00%) | Masking 15.8% | Same codes |
| Besançon | same (100.00%) | Masking 15.9%; 2 stops out | Same codes |
| Avignon | same (99.96%) | Masking 14.5% | Same codes |
| Tours | same (100.00%) | Masking 19.0%; 7 stops out | Same codes |
| Dijon | same (100.00%) | Masking 18.7%; 6 stops out | Same codes |
| Reims | same (100.00%) | Masking 17.7%; 3 stops out | Same codes |
| Orléans | same (99.95%) | Masking 19.8%; 19 stops out | Same codes |
| Mulhouse | same (100.00%) | Masking 12.7%; 1 stops out | Same codes |
| Brest | same (100.00%) | Masking 18.2%; 2 stops out | Same codes |
| Saint-Étienne | same (100.00%) | Masking 16.8%; 5 stops out | Same codes |
| Nice | same (99.96%) | Masking 15.9% | Same codes |
| Montpellier | same (99.97%) | Masking 18.7%; 24 stops out | Same codes |
| Strasbourg | same (99.93%) | Masking 15.9%; 29 stops out | Same codes |
| Le Havre | same (99.84%) | Masking 15.8%; 1 stops out | Same codes |
| Caen | same (100.00%) | Masking 17.5%; 9 stops out | Same codes |
| Rouen (Regional) | same (99.95%) | Masking 17.3% | Same codes |
| Bordeaux (Regional) | same (99.95%) | Masking 17.5% | Same codes |
| Nantes (Regional) | same (99.98%) | Masking 19.1% | Same codes |
| Grenoble (Regional) | same (99.93%) | Masking 18.4% | Same codes |
| Valenciennes (Regional) | same (99.96%) | Masking 16.0% | Same codes |
| Angers | same (99.96%) | Masking 19.3%; 6 stops out | Same codes |
| **Norway** | | | |
| Oslo | Address join to Matrikkelen (96.8%) | Web shops cannot be excluded | 8 no-premises codes, 96.990, bankrupt parents; sole-trader names withheld |
| Bergen | Address join to Matrikkelen (96.2%) | Web shops cannot be excluded | Oslo's; 96.990 on Bergen's own numbers; sole-trader names withheld |
| **Romania** | | | |
| Bucharest | Address join to OpenStreetMap's address points, in the premises' own sector (74.9%) | About one storefront in four unplaced, even across sectors; fishmongers in markets lowest | Cancelled registrations, mobile units, kiosk carts, vending machines, pastry labs, in-house buffets, catering; sole traders' and person-named companies' names withheld (category shown) |
| **Sweden** | | | |
| Stockholm | Register coordinates (98.4%); 85 not placed | Food only; frozen register; untyped premises before 2024 recovered by name only for 2022-23 (flagged); office canteens under company names not separated | Institutional kitchens (preschools, schools, care), caterers, event firms, food trucks and pharmacies by name; wholesale, production and "Övrigt" by type |
| Göteborg | Register coordinates (99.0%); 29 at the register's fallback point not placed | Food only; no dates; untyped premises recovered by name only (flagged); gyms, cinemas, bingo halls and general stores registered as food premises are counted; office canteens under company names not separated | Institutional kitchens, staff restaurants, hotel breakfast rooms, caterers, mobile units, ships, vending machines and pharmacies by type or name; wholesale, production and transport by type; address shown for a premises named only as a person |
| **Denmark** | | | |
| Copenhagen | Address join to DAR (98.3%) | Tattoo studios lost; web shops | Same 8 kinds + laundries, 969900; personal owners' names withheld |
| Aarhus | Address join to DAR, points from OpenStreetMap's copy (97.1%) | Tattoo studios lost; web shops | Same 8 kinds + laundries, 969900; personal owners' and franchisees' names withheld |
| Odense | Address join to DAR, points from OpenStreetMap's copy (98.4%) | Tattoo studios lost; web shops | Same 8 kinds + laundries, 969900; personal owners' and franchisees' names withheld |
| **Czechia** | | | |
| Prague | Address join to RÚIAN (99.99%) | Owner's activity only; web shops | Home-address sole traders (1,500) dropped; names withheld |
| Brno | Address join to RÚIAN (100%) | Owner's activity only; web shops | Home-address sole traders (591) dropped; names withheld |
| Plzeň | Address join to RÚIAN (100%) | Owner's activity only; web shops | Home-address sole traders (299) dropped; names withheld |
| Olomouc | Address join to RÚIAN (100%) | Owner's activity only; web shops | Home-address sole traders (223) dropped; names withheld |
| Ostrava | Address join to RÚIAN (100%) | Owner's activity only; web shops | Home-address sole traders (207) dropped; names withheld |
| Liberec (Regional) | Address join to RÚIAN, two obce (100%) | Owner's activity only; web shops; surrounding municipalities not counted | Home-address sole traders (283) dropped; names withheld |
| Most (Regional) | Address join to RÚIAN, two obce (100%) | Owner's activity only; web shops; surrounding municipalities not counted | Home-address sole traders (104) dropped; names withheld |
| **Netherlands** | | | |
| Amsterdam | Source points (22 permits unplaced) | Empty shop units about 5%; takeaways thin | Shop units also dwellings (757); canteens in venues, hotels |
| Rotterdam | Source points | Closed premises stay up to 5 years; about 7% vacant | Dwelling units (26); alcohol, terrace, gaming permits |
| Den Haag | Source points | Permit layer last edited 2025-05-23; about 4% of shop units vacant | Shop units also dwellings (1,928); pending permits (158); canteens, venues, hotels; trade names that are only a person's (5) |
| **Brazil** | | | |
| All nine | Source points (census) | Unreadable descriptions (see B); change since 2022 | Offices, parking, workshops, vacant, worship etc.; dwelling addresses show category only |
| **Hong Kong** | | | |
| Hong Kong | Source points: FEHD's own CSDI points, matched by licence number (28 unplaced) | Mostly restaurants; premises on different floors share one point | Food factories, canteens, cold stores, pools, entertainment and funeral trades; 2 duplicate licences counted once |
| **Latvia** | | | |
| Riga | Address join to the city's address points (96.8%); building footprints (99.4%) | Food a lower bound (licensed premises only); shops an upper bound (vacancy measured only in the centre) | Holder never read and unit numbers dropped (owner); 412 shops in degrading buildings |
| Liepāja | Address join to VZD's address register (93.9%); building footprints (100%) | Food a lower bound (licensed premises only); shops an upper bound (no vacancy figure) | Holder never read and unit numbers dropped |
| Daugavpils | Address join to VZD's address register (95.9%); building footprints (100%) | Food a lower bound (licensed premises only); shops an upper bound (no vacancy figure) | Holder never read and unit numbers dropped |
| **South Korea** | | | |
| Seoul | Source building points, gaps filled from other permits at the same building (98% placed; 4,875 unplaced) | Retail thin (licensed trades only) | Lodging, vets, hostess bars, food trucks, wholesale and online sellers; 138 personal names withheld; phone never read |
| Daegu | Source building points, gaps filled from other permits at the same building (99% placed; 612 unplaced) | Retail thin (licensed trades only) | Lodging, vets, hostess bars, food trucks, wholesale and online sellers; 113 personal names withheld; phone never read; health-food addresses masked by the publisher |
| Busan | Source building points, gaps filled from other permits at the same building (99% placed; 810 unplaced) | Retail thin (licensed trades only) | Lodging, vets, hostess bars, food trucks, wholesale and online sellers; 114 personal names withheld; phone never read; health-food addresses masked by the publisher |
| Incheon | Register coordinates (100%) | None: the register holds every storefront with a point | Offices, education, health, estate agents, lodging, recreation, repairs, funeral, wedding halls, hostess bars, staff canteens, fuel dealers; 107 personal names withheld |
| Goyang | Register coordinates (100%) | None | Incheon's; 9 personal names withheld |
| Seongnam | Register coordinates (100%) | None | Incheon's; 30 personal names withheld |
| Yongin | Register coordinates (100%) | None | Incheon's; 16 personal names withheld |
| Suwon | Register coordinates (100%) | None | Incheon's; 37 personal names withheld |
| Bucheon | Register coordinates (100%) | None | Incheon's; 28 personal names withheld |
| Namyangju | Register coordinates (100%) | None | Incheon's; 37 personal names withheld |
| Ansan | Register coordinates (100%) | None | Incheon's; 17 personal names withheld |
| Uijeongbu | Register coordinates (100%) | None | Incheon's; 11 personal names withheld |
| Anyang | Register coordinates (100%) | None | Incheon's; 28 personal names withheld |
| **Taiwan** | | | |
| Taichung | Address join to the city's door plates (92.2%; 5,599 unplaced) | Stalls unplaced; a department store is one point | Online shopping; office-like head offices; unmarked sole proprietors shown by industry |
| Taoyuan | Address join to the city's door plates (93.6%; 3,097 unplaced) | Stalls and rural addresses unplaced | Online shopping; office-like head offices; unmarked sole proprietors shown by industry |
| Taipei (Regional) | Address join to each city's door plates (Taipei 91.8%, New Taipei 95.0%) | Market and viaduct stalls unplaced | Online shopping; office-like head offices; unmarked sole proprietors shown by industry |
| **Japan** | | | |
| Kobe | Address join to MLIT's address blocks (97.3% block, 2.4% district centre; 85 unplaced) | Rokkō-san mountain addresses unplaced; closed premises may remain listed | Food trucks and stalls (市内一円); manufacturing except 菓子 / そうざい; vending; institutional catering; a trade name that is the operator's own name shown by permit type |
| Osaka | Address join to MLIT's address blocks (99.1% block, 0.8% district centre; 13 unplaced), checked against the list's own coordinates (median 38 m) | 上町's lettered blocks unplaced; closed premises may remain listed | Food trucks and stalls (市内一円); manufacturing except 菓子 / そうざい; vending; linen-supply laundries; a trade name that is the operator's own name shown by permit type, per premises |
| Sapporo | Address join to MLIT's address blocks (86.0% block, 13.9% block-group centre, about one block on the 条 grid; 41 unplaced) | Premises the city registers outside Sapporo unplaced; closed premises may remain listed | Food trucks, stalls and storeless pick-ups (市内一円); manufacturing except 菓子 / そうざい; vending; linen-supply laundries; salons inside hospitals and care homes (厚生施設); a trade name that is the operator's own name shown by permit type, per premises |
| Fukuoka | Address join to MLIT's address blocks, MHLW's own point where the block join misses (98.1% block, 1.8% MHLW's point, 0.1% town-chōme centre; 88 unplaced) | 11,768 MHLW filings published without an address (4,203 restaurants) unplaced; closed premises may remain listed in the city's list | Food trucks, stalls and on-train sales; school, hospital and staff kitchens; hotel restaurants; manufacturing except 菓子 / そうざい; vending; yatai (屋台) counted; a trade name that is the operator's own name shown by permit type, per premises (city lists only: MHLW's rows cannot be tested) |
| Kyoto | Address join to MLIT's address blocks (93.2% block, 5.5% town centre; 435 unplaced), the street-corner prefix read past | Twin-named towns left unplaced; closures invisible (an upper bound, disclosed) | Food trucks and permits under a year; manufacturing except 菓子 / そうざい; vending; a trade name that is the operator's own name shown by permit type, per premises |
| Tokyo | Address join to MLIT's address blocks (99.7% block, 158 at the town centre, 35 at MHLW's own point; 33 unplaced) | Fifteen wards without data (hollow stations); partial lists, each ward's share on the page; MHLW's filings by consent (8,973 without an address) | Food trucks, stalls and temporary permits; manufacturing except 菓子 / そうざい; vending; a trade name that is the operator's own name shown by permit type, where a list names its operators |
| Yokohama | Address join to MLIT's address blocks (98.0% block, 156 at the town centre; 4 unplaced) | Personal services only; closed premises may remain listed | Salons in vehicles and laundries with no fixed place (市内一円, 無店舗); a trade name that is the operator's own name shown by register type (none) |
| Hiroshima | Address join to MLIT's address blocks, MHLW's own point where the block join misses (96.4% block, 1.7% MHLW's point, 0.9% town-chōme centre; 150 unplaced) | 4,584 MHLW filings published without an address (1,779 restaurants) unplaced; closed premises may remain listed in the city's list | Food trucks, street and festival stalls (許可条件 露店, vehicle registrations); school, hospital and staff kitchens; hotel restaurants; manufacturing except 菓子 / そうざい; vending; a trade name that is the operator's own name shown by permit type (city list only) |
| Matsuyama | Address join to MLIT's address blocks, MHLW's own point for the same premises where the block join misses (80.8% block, 10.2% MHLW's point, 8.2% town-chōme centre; 84 unplaced) | 2,209 MHLW notifications published without an address unplaced; closed premises may remain listed in the city's lists | Food trucks and stalls (保健所管内); school, hospital and staff kitchens (事業場食堂); hotel restaurants; manufacturing except 菓子 / そうざい; vending; a trade name that is the operator's own name shown by permit type (city lists only) |
| Toyama | Address join to MLIT's address blocks, MHLW's own point for the same premises where the block join misses (85.5% block, 7.2% MHLW's point, 5.7% town-chōme centre; 104 unplaced) | The list names operators only where they are companies; closed premises may remain listed | Food trucks and stalls (市内一円); storeless laundry pick-ups; manufacturing except 菓子 / そうざい; vending; a trade name that is the operator's own name shown by permit type (where an operator is named) |
| Kumamoto | Address join to MLIT's address blocks, MHLW's own point where the block join misses (96.4% block, 0.8% MHLW's point, 2.2% town-chōme centre; 62 unplaced) | 736 MHLW filings published without an address (40 restaurants) unplaced; the city list's opt-outs; closed premises may remain listed | Vehicles and event permits (by the city); stalls and vehicles (業態); school, hospital and staff kitchens; hotel restaurants; hostess bars; manufacturing except 菓子 / そうざい; vending; a trade name that is the operator's own name shown by permit type (city lists only) |
| Fukui | Address join to MLIT's address blocks (87.9% block, 10.7% town-chōme centre; 75 unplaced) | The list names operators only where they are companies; closed premises removed monthly by the city | Food trucks and stalls (not listed); manufacturing except 菓子 / そうざい; a trade name that is the operator's own name shown by permit type (where an operator is named) |
| Nagasaki | Address join to MLIT's address blocks, MHLW's own point where the block join misses (89.2% block, 3.8% MHLW's point, 6.9% town-chōme centre; 5 unplaced) | 3,623 MHLW filings published without an address (2,090 restaurants) unplaced; the 2023 snapshot keeps premises closed since | Vehicles and stalls (業態); snack bars; school, hospital and staff kitchens; hotel restaurants; manufacturing except 菓子 / そうざい; vending; the name rule cannot run (no operator column) |
| Utsunomiya | Address join to MLIT's address blocks, MHLW's own point where the block join misses (95.8% block, 2.6% MHLW's point, 1.4% town-chōme centre; 17 unplaced) | 426 MHLW filings published without an address (37 restaurants) unplaced; closed premises may remain listed | Food trucks and stalls (業態); school, hospital and staff kitchens; hotel restaurants; snack bars; manufacturing except 菓子 / そうざい; vending; a trade name that is the operator's own name shown by permit type (city lists only) |
| Kitakyushu | Address join to MLIT's address blocks, MHLW's own point where the block join misses (98.5% block, 1.3% MHLW's point, 0.2% town-chōme centre; 2 unplaced) | 4,719 MHLW filings published without an address (1,484 restaurants) unplaced; closed premises may remain listed | Food trucks and stalls; school, hospital and staff kitchens; hotel restaurants; snack bars; manufacturing except 菓子 / そうざい; vending; yatai counted; the name rule finds no sole trader (the city names company operators only) |
| Sakai | Address join to MLIT's address blocks, MHLW's own point where the block join misses (95.2% block, 1.1% MHLW's point, 3.6% town-chōme centre; 2 unplaced) | 1,825 MHLW notifications published without an address unplaced; a closed premises stays listed until a closure is filed or its permit expires | Food trucks, street and festival stalls (市内一円, 自動車, 露店); school, hospital and staff kitchens; hotel restaurants; snack bars and cabarets; manufacturing except 菓子 / そうざい; vending; a trade name that is the operator's own name shown by permit type (city list only) |
| Hakodate | Address join to MLIT's address blocks (94.0% block, 66 at the town centre; none unplaced) | Personal services only; closed premises may remain listed | Laundry pick-ups with no shop (無店舗); a trade name that is the operator's own name shown by register type (1) |
| Kagoshima | Address join to MLIT's address blocks, MHLW's own point where the block join misses (94.9% block, 4.0% MHLW's point, 1.0% town-chōme centre; 8 unplaced) | 2,664 MHLW filings published without an address (1,397 restaurants) unplaced; closed premises may remain listed | Food trucks and stalls; school, hospital and staff kitchens; manufacturing except 菓子 / そうざい; vending; a trade name that is the operator's own name shown by permit type (city list only) |
| Okayama | Address join to MLIT's address blocks, MHLW's own point where the block join misses (91.2% block, 8.5% MHLW's point, 2 at the town-chōme centre; 16 unplaced) | 3,379 MHLW filings published without an address (1,976 restaurants) unplaced; closed premises may remain listed | Food trucks and stalls (一円); school, hospital and staff kitchens; hotel restaurants; snack bars; manufacturing except 菓子 / そうざい; vending; yatai counted; the name rule cannot run (no operator column) |
| Kōchi | Address join to MLIT's address blocks (95.8% block, 59 at the town centre; none unplaced) | Barbers and beauty salons only (no laundry list); closures since 2026-03-31 unpublished (an upper bound) | Salons registered anywhere in the city (一円); a trade name that is the operator's own name shown by register type (none) |
| **Germany** | | | |
| Berlin | Register coordinates (60,313 of 60,314 inside the Land) | Crafts missing; web shops cannot be excluded; registered offices stack at arcade and business-centre addresses | Catering, intermediation, mobile food, household services; "other personal services" (96.99) and general non-food retail (IHK 47122) as catch-alls; employee band and business type read, never shown |
| **United Kingdom** | | | |
| London | Register coordinates (91%) and postcode centres (4%, OS postcode centroids for a full postcode with no register point; a median 11 m from the register's own point where both exist); 3,000 not placed | Food only; about one storefront in twenty unplaced, most in outer boroughs; canteens not separated | Home and mobile caterers, institutional kitchens, hotels, manufacturers and distributors by type; a private address or a flat address never placed; the name after "trading as" shown |
| Glasgow | Register coordinates (99%); 55 not placed | Food only; about one storefront in a hundred unplaced; canteens not separated | Home and mobile caterers, institutional kitchens, hotels, manufacturers and distributors by type; a flat address or a childminder never placed; the name after "trading as" shown |
| Newcastle (Regional) | Register coordinates (90%) and postcode centres (10%, OS postcode centroids for a full postcode with no register point); 489 not placed | Food only; about one storefront in fourteen unplaced, most in North Tyneside and Sunderland; canteens not separated | Home and mobile caterers, institutional kitchens, hotels, manufacturers and distributors by type; a private address or a flat address never placed; the name after "trading as" shown |
| **Argentina** | | | |
| Buenos Aires | Parcel centres (99.8%) and block centres (0.1%), a join to the city's Parcelas on the survey's parcel key; 3 not placed | Each block surveyed once, 2022–2024; unidentified shopfronts 7.2% (32% in Villa Riachuelo); malls not itemised; businesses in one building share a point | Homes with a business inside (filed as housing); car repair, finance, lottery, health and veterinary, offices, wholesale by use |
| **Australia** | | | |
| Sydney | Census coordinates (per building; 5,054 distinct points for 7,074 storefronts) | The City of Sydney LGA only; a five-yearly survey (2022); no names | Parking, non-store retail, organisations, licensed members' clubs, catering, funerals, brothels and other personal services n.e.c. by class; one n.e.c. catch-all kept |
| Melbourne | Census coordinates (per property; 1,840 distinct points for 4,959 storefronts) | The City of Melbourne LGA; upper-floor tenancies kept | Parking, non-store retail, organisations, licensed members' clubs, catering, funerals, brothels and other personal services n.e.c. by class; one n.e.c. catch-all kept |
| **Switzerland** | | | |
| Zurich | Register coordinates, LV95 (100%) | Retail only where alcohol is licensed; institutional kitchens licensed as restaurants not separated (about 1 in 30 food licences) | Canteens, cabarets, event rooms, food stands and caterers, licence-exempt premises by type; address shown for a person-named trade name (12) |

### D. Vintage and map features (dimensions 10–11, plus two added)

"Date on page": B = business data date shown, T = transit date only, — = none.
In-ring share = in-ring heat points ÷ all-storefront heat points.

| City | Business data as-of (fetched) | Date on page | Rings (outer) | Whole-city heat layer | In-ring share | Pin label |
|---|---|---|---|---|---|---|
| **United States** | | | | | | |
| San Diego | UNKNOWN (2026-09-18) | — | 0.6 mi | Yes | 24% | Trade name |
| San Francisco | UNKNOWN (≈2026-09-19) | — | 0.6 mi | Yes | 72% | Name |
| Los Angeles | UNKNOWN (≈2026-09-19) | — | 0.6 mi | Yes | 24% | Trade name, else registrant |
| Chicago | Active licences (2026-09-20) | — | 0.6 mi | Yes | 57% | Name |
| New York | UNKNOWN (2026-09-21) | — | 0.3 mi | Yes | 71% | Name |
| Philadelphia | Active licences (2026-09-21) | — | 0.6 mi | Yes | 58% | Trade name (from "LEGAL (TRADE)") |
| Miami (Regional) | Tax year 2026 (2026-09-21) | — | 0.6 mi | Yes | 13% | Name |
| Boston | UNKNOWN (2026-09-21) | — | 0.6 mi | Yes | 76% | Name |
| Washington D.C. | Active licences (2026-09-21) | — | 0.6 mi | Yes | 74% | Name |
| Buffalo | Licences unexpired on 2026-09-29 (2026-09-29) | B | 0.6 mi | Yes | 24% | Trade name; licence type for person-named salons |
| Sacramento | Licences unexpired on 2026-09-29 (2026-09-29) | B | 0.6 mi | Yes | 41% | Name; description for names that read as a person's |
| Houston | Active permits (2026-09-29) | B | 0.6 mi | Yes | 7% | Name; address for a person's permit |
| Minneapolis | Inspected within two years of 2026-09-30 (2026-09-30) | B | 0.6 mi | Yes | 36% | Trade name |
| Pittsburgh | Active on the County's list of 2025-08-27 (2026-09-30) | B | 0.3 mi | Yes | 18% | Trade name |
| Dallas | Active permits (2026-09-30) | B | 0.6 mi | Yes | 26% | Name; address for a person's permit |
| Kansas City | Frozen 2026-01-15, licences valid 2025-26 (2026-09-30) | B | 0.3 mi | Yes | 13% | Trade name, else holder company; address for a person's licence |
| Tucson | Active licences (2026-09-30) | B | 0.3 mi | Yes | 6% | Account name; address for a person's licence |
| New Orleans | Active licences, daily (2026-09-30) | B | 0.3 mi | Yes | 45% | Business name, never the owner's; address where none |
| **Canada** | | | | | | |
| Vancouver (Regional) | Current-year licences (2026-09-21) | — | 0.6 mi | Yes | 40% | Name; type on 88 pins |
| Montréal | 2025 survey (2026-09-21) | — | 0.6 mi | Yes | 60% | Establishment name |
| Calgary | UNKNOWN (2026-09-21) | — | 0.6 mi | Yes | 41% | Trade name |
| Edmonton | UNKNOWN (2026-09-21) | — | 0.6 mi | Yes | 22% | Business name |
| Kitchener–Waterloo (Regional) | Inspected since 2024-07-03 (typed tables 2026-07-03; layers fetched 2026-09-30) | B | 0.6 mi | Yes | 41% | Premises name; type for a person's name (personal services) |
| Toronto | Current licences (2026-09-21) | — | 0.6 mi | Yes | 48% | Operating name |
| Ottawa | Inspected since 2024-09-29 (feed 2026-09-29) | B | 0.6 mi | Yes | 32% | Premises name |
| **Mexico** | | | | | | |
| Mexico City | DENUE 05_2026 (2026-09-22) | — | 0.6 mi | Yes (restored 2026-09-27) | 47% | Shop sign |
| Guadalajara (Regional) | DENUE 05_2026 (2026-09-22) | — | 0.6 mi | Yes (restored 2026-09-27) | 31% | Shop sign |
| Monterrey (Regional) | DENUE 05_2026 (2026-09-27) | — | 0.6 mi | Yes | 25% | Shop sign |
| **Spain** | | | | | | |
| Madrid | Portal refreshed daily (2026-09-22) | — | 0.6 mi | Yes | 95% | Trade name |
| Barcelona | 2022 survey (2026-09-22) | B (prose) | 0.6 mi | Yes | 100% | Unit name |
| Palma | Register of 2026-09-07 (fetched 2026-09-28) | B | 0.6 mi | Yes | 35% | Trade name |
| **Ireland** | | | | | | |
| Dublin | UNKNOWN (2026-09-22) | — | 0.6 mi | Yes | 58% | Address + use |
| **Italy** | | | | | | |
| Milan | UNKNOWN (2026-09-22) | — | 0.6 mi | Yes | 87% | Sign on about 1 in 7; else address |
| Rome | July 2025 (2026-09-24) | B | 0.6 mi | Yes | 61% | Activity + address |
| Florence | Updated daily (2026-09-30) | B | 0.3 mi | Yes | 37% | Type only (no name or address) |
| **France** | | | | | | |
| Paris | SIRENE monthly; month UNKNOWN (2026-09-22) | T | 0.3 mi | Yes | 98% | Sign/usual name (about 40%), else address |
| Marseille | same (2026-09-23) | T | 0.3 mi | Yes | 55% | same (43% named) |
| Toulouse | same (2026-09-23) | T | 0.3 mi | Yes | 64% | same (about half show an address, per the page) |
| Lille (Regional) | same (2026-09-23) | T | 0.3 mi | Yes | 61% | same (about half show an address, per the page) |
| Rennes | same (2026-09-23) | T | 0.3 mi | Yes | 68% | same (about two in five show an address, per the page) |
| Le Mans | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 73% | Sign/usual name (about 60%), else address |
| Besançon | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 64% | Sign/usual name (about 57%), else address |
| Avignon | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 26% | Sign/usual name (about 47%), else address |
| Tours | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 66% | Sign/usual name (about 61%), else address |
| Dijon | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 67% | Sign/usual name (about 60%), else address |
| Reims | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 55% | Sign/usual name (about 55%), else address |
| Orléans | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 85% | Sign/usual name (about 56%), else address |
| Mulhouse | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 79% | Sign/usual name (about 51%), else address |
| Brest | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 77% | Sign/usual name (about 59%), else address |
| Saint-Étienne | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 76% | Sign/usual name (about 54%), else address |
| Nice | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 80% | Sign/usual name (about 49%), else address |
| Montpellier | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 87% | Sign/usual name (about 49%), else address |
| Strasbourg | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 85% | Sign/usual name (about 53%), else address |
| Le Havre | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 60% | Sign/usual name (about 56%), else address |
| Caen | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 71% | Sign/usual name (about 60%), else address |
| Rouen (Regional) | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 62% | Sign/usual name (about 54%), else address |
| Bordeaux (Regional) | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 65% | Sign/usual name (about 51%), else address |
| Nantes (Regional) | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 63% | Sign/usual name (about 57%), else address |
| Grenoble (Regional) | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 78% | Sign/usual name (about 56%), else address |
| Valenciennes (Regional) | SIRENE 01 septembre 2026 (2026-09-30) | B | 0.3 mi | Yes | 69% | Sign/usual name (about 51%), else address |
| Angers | SIRENE 01 septembre 2026 (2026-10-01) | B | 0.3 mi | Yes | 75% | Sign/usual name (about 60%), else address |
| **Norway** | | | | | | |
| Oslo | UNKNOWN (2026-09-24) | T | 0.3 mi | Yes | 76% | Name; address for sole traders |
| Bergen | Register downloaded 2026-09-24 (Norway's date; 2026-09-23 in Pacific time); transit 2026-09-27 | B | 0.6 mi | Yes | 59% | Name; address for sole traders |
| **Romania** | | | | | | |
| Bucharest | Registers of 2026-08-25 (fetched by the owner 2026-09-28) | B | 0.6 mi | Yes | 72% | Company name without its legal form; category for sole traders and person-named companies |
| **Sweden** | | | | | | |
| Stockholm | Inspections to 2025-10-21, layer edited 2025-10-22 (fetched 2026-09-29) | B | 0.6 mi | Yes | 89% | Premises name |
| Göteborg | No dates; the premises active on the day fetched (2026-10-01) | B | 0.3 mi | Yes | 75% | Premises name; address for a premises named only as a person |
| **Denmark** | | | | | | |
| Copenhagen | Weekly extract (2026-09-24) | B | 0.6 mi | Yes | 94% | Name; address for personal owners |
| Aarhus | Weekly extract (2026-09-24) | B | 0.3 mi | Yes | 25% | Name; address for personal owners and franchisees |
| Odense | Weekly extract (2026-09-24) | B | 0.3 mi | Yes | 41% | Name; address for personal owners and franchisees |
| **Czechia** | | | | | | |
| Prague | 2026-08-31 (ROS02) | B | 0.6 mi | Yes | 70% | Name; address for persons/partnerships |
| Brno | 2026-08-31 (ROS02) | B | 0.3 mi | Yes | 82% | Name; address for persons/partnerships |
| Plzeň | 2026-08-31 (ROS02) | B | 0.3 mi | Yes | 71% | Name; address for persons/partnerships |
| Olomouc | 2026-08-31 (ROS02) | B | 0.3 mi | Yes | 78% | Name; address for persons/partnerships |
| Ostrava | 2026-08-31 (ROS02) | B | 0.3 mi | Yes | 74% | Name; address for persons/partnerships |
| Liberec (Regional) | 2026-08-31 (ROS02) | B | 0.3 mi | Yes | 56% | Name; address for persons/partnerships |
| Most (Regional) | 2026-08-31 (ROS02) | B | 0.3 mi | Yes | 65% | Name; address for persons/partnerships |
| **Netherlands** | | | | | | |
| Amsterdam | Live register (2026-09-24) | B | 0.6 mi | Yes | 96% | Permit name (food); address (shops) |
| Rotterdam | Notices to 2026-09-24 (5-yr window) | B | 0.6 mi | Yes | 93% | No names; address (shops) |
| Den Haag | Permit layer edited 2025-05-23 (2026-10-01) | B | 0.3 mi | Yes | 93% | Permit trade name (food); address (shops) |
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
| **Latvia** | | | | | | |
| Riga | Excise daily; cadastre prepared 2026-09-20 (fetched 2026-09-25) | B | 0.6 mi | Yes | 78% | No names; the kind (food) or the premises' registered name (shops) |
| Liepāja | Excise daily; cadastre prepared 2026-09-20 (Riga's cache) | B | 0.3 mi | Yes | 70% | No names; the kind (food) or the premises' registered name (shops) |
| Daugavpils | Excise daily; cadastre prepared 2026-09-20 (Riga's cache) | B | 0.3 mi | Yes | 80% | No names; the kind (food) or the premises' registered name (shops) |
| **South Korea** | | | | | | |
| Seoul | Registers daily, updated to 2026-09-24 (fetched 2026-09-25) | Yes (snapshot caption) | 0.6 mi | Yes (restored 2026-09-27; dropped 2026-09-25 for phones) | 94% | Trade name in Korean (138 show "Name withheld") |
| Daegu | Edition 2026-08, but its rows end 2025-08-31 (fetched 2026-09-27) | Yes (snapshot caption, the rows' own date) | 0.6 mi | Yes | 71% | Trade name in Korean (113 show "Name withheld") |
| Busan | Frozen 2026-04-15, the rows agree (fetched 2026-09-27) | Yes (snapshot caption) | 0.6 mi | Yes | 74% | Trade name in Korean (114 show "Name withheld") |
| Incheon | SEMAS edition of 2026-06-30 (fetched 2026-09-29) | B | 0.6 mi | Yes | 68% | Trade name in Korean, with the branch (107 show "Name withheld") |
| Goyang | SEMAS edition of 2026-06-30 (fetched 2026-09-29) | B | 0.6 mi | Yes | 67% | Trade name in Korean, with the branch |
| Seongnam | SEMAS edition of 2026-06-30 (fetched 2026-09-29) | B | 0.6 mi | Yes | 76% | Trade name in Korean, with the branch |
| Yongin | SEMAS edition of 2026-06-30 (fetched 2026-09-29) | B | 0.6 mi | Yes | 55% | Trade name in Korean, with the branch |
| Suwon | SEMAS edition of 2026-06-30 (fetched 2026-09-29) | B | 0.6 mi | Yes | 48% | Trade name in Korean, with the branch |
| Bucheon | SEMAS edition of 2026-06-30 (fetched 2026-09-29) | B | 0.6 mi | Yes | 80% | Trade name in Korean, with the branch |
| Namyangju | SEMAS edition of 2026-06-30 (fetched 2026-09-29) | B | 0.6 mi | Yes | 55% | Trade name in Korean, with the branch |
| Ansan | SEMAS edition of 2026-06-30 (fetched 2026-09-29) | B | 0.6 mi | Yes | 64% | Trade name in Korean, with the branch |
| Uijeongbu | SEMAS edition of 2026-06-30 (fetched 2026-09-29) | B | 0.6 mi | Yes | 85% | Trade name in Korean, with the branch |
| Anyang | SEMAS edition of 2026-06-30 (fetched 2026-09-29) | B | 0.6 mi | Yes | 64% | Trade name in Korean, with the branch |
| **Taiwan** | | | | | | |
| Taichung | Register daily, dated 2026-09-25; door plates August 2026 (fetched 2026-09-25) | Yes (snapshot caption) | 0.6 mi | Yes | 19% | Trade name in Chinese, or the line of business (11,907) |
| Taoyuan | Register daily, dated 2026-09-25; door plates August 2026 (fetched 2026-09-25) | Yes (snapshot caption) | 0.6 mi | Yes | 12% | Trade name in Chinese, or the line of business (7,230) |
| Taipei (Regional) | Register daily, dated 2026-09-25; door plates 2026-09 editions (fetched 2026-09-25) | Yes (snapshot caption) | 0.6 mi | Yes | 78% | Trade name in Chinese, or the line of business (17,890) |
| **Japan** | | | | | | |
| Kobe | Permits in force 2026-03-31 (fetched 2026-09-24) | B (in the prose) | 0.6 mi | Yes | 87% | Trade name in Japanese, or the permit type (10) |
| Osaka | Food permits as of 2026-06-30, registers 2026-03-31 (fetched 2026-09-24) | B (in the prose) | 0.6 mi | Yes | 98% | Trade name in Japanese, or the permit type (9) |
| Sapporo | Food permits as of 2026-03-31, registers 2026-07-31 (fetched 2026-09-24) | B (in the prose) | 0.6 mi | Yes | 80% | Trade name in Japanese, or the permit type (7) |
| Fukuoka | City food list and barber / beauty registers as of 2026-08-31, laundry 2026-03-31; MHLW's filings downloaded 2026-09-27 (fetched 2026-09-24 to 09-27) | B (in the prose) | 0.6 mi | Yes | 82% | Trade name in Japanese, or the permit type (5) |
| Kyoto | Food permits rebuilt as of 2026-07-31, registers 2026-03-31 plus new premises to 2026-07 (fetched 2026-09-24) | B (in the prose) | 0.6 mi | Yes | 86% | Trade name in Japanese, or the permit type (8) |
| Tokyo | Ward lists dated 2022-11-30 to 2026-09-02, registers undated or 2026-03-31 (fetched 2026-09-24) | B (in the prose) | 0.6 mi | Yes | 98% | Trade name in Japanese, or the permit type (2) |
| Yokohama | Registers as of 2026-04-01 (fetched 2026-09-24, unchanged 2026-09-30) | B (in the prose) | 0.6 mi | Yes | 83% | Trade name in Japanese |
| Hiroshima | City food list as of 2026-03-31 (permits in force); MHLW's filings downloaded 2026-09-30 (fetched 2026-09-24 to 09-30) | B (in the prose) | 0.3 mi | Yes | 67% | Trade name in Japanese, or the permit type (1) |
| Matsuyama | City lists as of 2026-03-31 (permits in force; full registers); MHLW's notifications downloaded 2026-10-02 | B (in the prose) | 0.3 mi | Yes | 55% | Trade name in Japanese, or the permit type (3) |
| Toyama | City food list as of 2026-06-30 (permits in force); registers 2026-03 (fetched 2026-10-02) | B (in the prose) | 0.3 mi | Yes | 46% | Trade name in Japanese, or the permit type (5) |
| Kumamoto | City lists as of 2026-03-31; MHLW's filings downloaded 2026-10-02 | B (in the prose) | 0.3 mi | Yes | 54% | Trade name in Japanese, or the permit type (3) |
| Fukui | City lists as of 2026-08-31 (the newest month-end sheet; fetched 2026-10-02) | B (in the prose) | 0.6 mi | Yes | 60% | Trade name in Japanese, or the permit type (6) |
| Nagasaki | City food list as of 2023-06-30, registers 2023-03-31; MHLW's filings downloaded 2026-10-02 | B (in the prose) | 0.3 mi | Yes | 58% | Trade name in Japanese |
| Utsunomiya | City lists as of July 2026 (old-law permits in term; full registers); MHLW's filings downloaded 2026-10-02 | B (in the prose) | 0.6 mi | Yes | 47% | Trade name in Japanese, or the permit type (1) |
| Kitakyushu | Old-law list as of 2026-03-31 (in term on 2026-08-31), registers 2026-08-31; MHLW's filings downloaded 2026-10-02 | B (in the prose) | 0.6 mi | Yes | 71% | Trade name in Japanese |
| Sakai | City list rebuilt to 2026-08-31 (the 2026-04-01 list plus monthly new permits and closures); MHLW's notifications downloaded 2026-10-02 | B (in the prose) | 0.6 mi | Yes | 75% | Trade name in Japanese, or the permit type (1) |
| Hakodate | Registers as of 2026-08-31 (fetched 2026-10-02) | B (in the prose) | 0.3 mi | Yes | 31% | Trade name in Japanese, or the register type (1) |
| Kagoshima | City list as of 2026-06-30; MHLW's filings downloaded 2026-10-02 | B (in the prose) | 0.3 mi | Yes | 60% | Trade name in Japanese |
| Okayama | MHLW's filings downloaded 2026-10-02 | B (in the prose) | 0.6 mi | Yes | 63% | Trade name in Japanese |
| Kōchi | Lists as of 2026-03-31 plus monthly additions to 2026-08-31 (fetched 2026-10-02) | B (in the prose) | 0.3 mi | Yes | 48% | Trade name in Japanese |
| **Germany** | | | | | | |
| Berlin | 2026-09-01, monthly (IHK's own commit date; fetched 2026-09-28) | B | 0.6 mi | Yes | 82% | Kind of business (the register has no names) |
| **United Kingdom** | | | | | | |
| London | Extracts of 2026-09-09 to 2026-09-16, per borough (fetched 2026-09-28) | B | 0.6 mi | Yes | 74% | Registered name; the trade name where registered "trading as" |
| Glasgow | Extract of 2026-09-14 (fetched 2026-09-28) | B | 0.6 mi | Yes | 42% | Registered name; the trade name where registered "trading as" |
| Newcastle (Regional) | Extracts of 2026-09-09 to 2026-09-16, per council (fetched 2026-09-28) | B | 0.6 mi | Yes | 54% | Registered name; the trade name where registered "trading as" |
| **Argentina** | | | | | | |
| Buenos Aires | Surveyed 2022–2024, published October 2025 (2026-09-28) | B (prose) | 0.6 mi | Yes | 66% | Street address + use (the survey has no names) |
| **Australia** | | | | | | |
| Sydney | Survey of 2022 (layer last edited 2025-02-12; fetched 2026-09-28) | B | 0.6 mi | Yes | 83% | Kind of business (the survey has no names) |
| Melbourne | Census of 2024 (dataset modified 2021-11-02 per its metadata; fetched 2026-09-28) | B | 0.6 mi | Yes | 96% | Registered name (the trading name) |
| **Switzerland** | | | | | | |
| Zurich | Open licences, kept current; last updated 2026-09-28 (fetched 2026-09-30) | B | 0.3 mi | Yes | 92% | Trade name and licence type; address for a person-named trade name |

Features every map shares, so not a difference: permanent line labels and a legend
entry for every line; rings start switched off; OSM basemap credit; the site-wide
notices footer (`app/components.py` `render_site_notices`). Required notices are
page-level, not on-map, and apply to every page.

**Line colours not the agency's** (a smaller visual difference): Miami (all
project-chosen), Edmonton (darkened), Toronto (Line 2 darkened), Oslo (two lightened;
tram 15 assigned), Copenhagen (A and F lightened), Prague (A lightened), Amsterdam
(5 tram lines adjusted), Rome (B1 lightened), Lille (Tram T darkened), Rio (a few
lightened), Rotterdam (trams 1 and 11 separated), Salvador (colours from line names;
OSM has none), Paris (T3a and T3b lightened), the six Japanese cities (all
project-chosen; Tokyo's by a spatial search, `scripts/line_colour_search.py`).

**Line labels by code, not name:** Tokyo only. Its 52 full names do not fit
(9 unplaceable at 1000 px), so the map labels each line with its operator's line
code (JY, G, A...) and the legend gives code and full name; several lines share a
code (Seibu's SI, Tobu's TS, Keisei's KS, Keikyu's KK) and are told apart by
colour and the legend
(DEC 2026-09-28, "Tokyo's rail" and "Tokyo's review time").
Source: each page's prose.

---

## Open questions

Contradictions between files, and claims that have gone stale, which the owner
would need to settle before this becomes a page.

**Resolved 2026-09-24** (owner-approved wording, see DECISIONS): 1, 3, 4, 5, 6,
7, 8 and 17 (each French page now states its measured share of address-only
dots). Also resolved: in 2, the ring wording in EC and on the New York page;
in 19, the stale "2026-09-21 rebuild" header and "the other four cities". The
rest of 2 (the NY config's "THE ONE CITY" comment) and everything from 9 on
remain open.

**Resolved 2026-09-27** (owner-approved wording, see DECISIONS): 18; the
wording lands at review time.

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
   and Montréal (an agglomeration of 15 municipalities and 19 boroughs), and Tokyo
   (23 special wards, each its own municipality, though read together as the city
   of Tokyo). None is labelled; Santos, with two municipalities, is. Also, DEC (around line 1099) says
   the regional pages drop "(Regional)" from their headings, but Lille's heading
   includes it.
10. **The tram test.** EC (lines 59–70) states only "the rapid-transit system or an
    overlay on one". The Oslo and Rotterdam decisions add "serves corridors the metro
    does not". Toronto's page excludes the streetcars because they "run in traffic
    every block or two", which is the problem Amsterdam and Rotterdam solve with the
    spacing filter. Should one sentence govern all three?
11. **Madrid's Metro Ligero** is left out "so the city ships one agency's rail
    system" (`pipeline/madrid/config.py:92–96`). That is not the tram test, and it
    appears neither on the Madrid page nor in EC. *(2026-09-27: ML1 is now drawn;
    ML2 and ML3 are left out as stubs, owner's call. The page now says so;
    checked 2026-09-28, EC still does not name ML2 or ML3.)*
12. **Cable cars and unmentioned systems.** Toulouse establishes that "cable car" is
    not a reason to exclude. Mexico City's Cablebús and Tren Suburbano, and
    Montréal's REM and exo, are not mentioned in any file read. Unknown whether they
    were considered. *(2026-09-27: the REM is now drawn; exo, Cablebús and the
    Tren Suburbano remain open.)*
13. **Undisclosed floors in the first US cities.** San Francisco (about 37% of rows
    have NAICS) and Los Angeles (about 9% have none), from DEC's 2026-09-18/19
    entries, and San Diego's neighbourhood undercount (La Jolla). All three are open
    in `PLAN.md` (around lines 1675–1682) and absent from the pages. It is also
    unknown whether the SF and LA figures still hold after later rebuilds.
14. **Car dealers.** `madrid_epigrafe.py:60` and `norway_sn2025.py:17` justify
    counting car dealers because "every other city in this project already counts a
    car dealer as retail". `france_naf.py` maps division 47 only, so the five French
    cities do not (NAF puts car sales in 45). Either the justification or the French
    mapping needs a note. *(2026-09-29: settled by the owner - France is the one
    disclosed exception, with its reason in `france_naf.py` and EC's Paris
    section (theme 11). The Madrid and Norway comments' "every other city" still
    reads as if France were not one.)*
15. **Adult-premises exclusions** are recorded for Calgary, Edmonton, Toronto and
    Vancouver. No file says whether the NAICS, SIRENE, NACE or CNEFE cities contain
    or exclude comparable premises. *(2026-09-29: adult and hostess venues are now
    left off wherever a register names them (theme 11); the question stands for
    the classification cities, where no code names them.)*
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
    **Settled 2026-09-27:** step 2 counts its buckets (lines 116-120) before
    it drops nameless, addressless and duplicate rows (126-156), so
    `baseline.json`'s buckets do not sum to its own `storefront_rows`. EC now
    quotes the pins the map draws (`businesses_geocoded.csv`): 759 of 18,186
    retail (4.2%), 13,385 food service, 4,042 personal services. The 4.2% in
    `__init__.py` is a third stage (before cancelled licences were dropped)
    that happens to agree. EC's per-category counts just above that sentence
    (`SECOND HAND SHOP` 1,806 and so on, summing to 3,475) were from that
    pre-cancellation stage too; they now come from the drawn pins and sum to
    759. Both EC changes are now on master (EC quotes 759 of 18,186; checked
    2026-09-28).
19. **Stale counts in EC:** the header says "Business counts are from the 2026-09-21
    rebuild", but more than half the cities were built from 2026-09-22 to 09-24; line
    1540 compares New York with "the other four cities".
20. **Data dates on pages.** Twenty pages show no date for their business data
    (theme 9; Monterrey was added). Is a uniform "data as of" line wanted? Several
    sources' own as-of dates are not recorded anywhere read: the SIRENE release month,
    Dublin's valuation list date, Milan's registers. (The DENUE edition is 05_2026,
    `docs/data_sources/mexico.md`, found 2026-09-28; `app/cities.py` `data_age` still
    says "no source date" for Mexico City and Guadalajara, queued for review time.)
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
- **Theme 11 (category edges):** `pipeline/taxonomies/france_naf.py:223–273`
  (the car-dealer reason at 237–244); `madrid_epigrafe.py:58–65`;
  `norway_sn2025.py:15–18`; the dealer entries in `dc_businessactivity.py`,
  `vancouver.py`, `calgary_licencetype.py`, `edmonton_licencecategory.py`,
  `dublin_uses.py`, `barcelona_activitat.py`, `ba_usos_suelo.py`,
  `brazil_cnefe.py`, `czech_nace2025.py`, `anzsic_fes.py` and
  `pipeline/countries/taiwan.py` (division 48 is Retail apart from 486 and 487,
  so 484 car retail - 全新汽車零售 in Taichung's data - is kept); the
  approved wording and counts in `docs/handoff_exclusions_2026-09-29.md`; EC city
  sections; legend rows in each `heatmap.html`.
- **Theme 12 (whole-city layer, resolved):** no city passes `all_city_heat=False`
  since 2026-09-27; DECISIONS of that date.
- **Location rates:** DS Business registries rows (Toronto, Paris to Rennes, Oslo,
  Copenhagen, Prague, Rome); DEC around 18511 (LA), 16168 (D.C.), 18345 (NY), 19528
  (SD); the city configs' coordinate comments (Montréal, Calgary, Dublin, Madrid).
