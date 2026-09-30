# What this map leaves out, and why

This project maps **storefront** commercial density around rapid-transit
stations: the kind of business you might walk into on your way from a station.

That sentence holds two separate scoping decisions, and this page is both of
them — **which stations** a map is drawn around, and **which businesses** are
counted near them. Each one leaves things out on purpose. Neither is visible
from the map itself, which is why they are written down here.

It is written to be published as-is alongside the maps. Business counts were
recorded when each city was built or last rebuilt; station counts are computed from the repository's
own `outputs/<city>/excluded_stations.csv` files each time this page is
rendered, so they cannot drift. The reasoning behind each decision, with sample
sizes, is in `DECISIONS.md`. Where each city's data comes from is in
`data_sources.md`.

Two principles run through the business half:

1. **Storefront means storefront.** A business you cannot walk into does not
   answer the question this map asks, however legitimately it is registered.
2. **Publish public commercial information, not personal information.** A trade
   name someone chose for their shop is commercial and deliberately public. A
   registrant's own name at what appears to be their home is not, even though
   the registry holding it is public.

Those two overlap more than you would expect: the categories that are not
really storefronts are the same ones full of people running a business from
home under their own name. Fixing the first mostly fixed the second.

## Which stations these maps are drawn around

**Every map here covers one city's rapid-transit network**, named in the title
of its own page and in the city list on the front page: Muni Metro in San
Francisco, the 'L' in Chicago, Metro de Madrid in Madrid. Anything else that
carries people around that city is not on the map, and the rings are drawn only
around the stations that are.

**That network is rail in every city but one.** Toulouse's Téléo is an aerial
cable car, and it is drawn - because Tisséo runs and tickets it exactly as it
does the métro, because it crosses the Garonne where no other line does, and
because one of its three stations is a Métro B interchange. It is the only
non-rail mode on this site, and its own section below has the reasoning. **So
the question a mode has to answer is not "does it run on rails" but "is it part
of the network this city's riders use as its rapid transit"** - which is the
same question the tram and commuter-rail paragraphs below are answering.

**Commuter rail is excluded unless it runs like rapid transit.** The ones named on the record are
BART and Caltrain in San Francisco, Metra in Chicago, Metrolink in Los Angeles,
the Coaster and Sprinter in San Diego, SEPTA's Regional Rail in Philadelphia,
the MBTA's Regional Rail in Boston, Tri-Rail in Miami, GO Transit in Toronto,
the West Coast Express in Vancouver, Cercanías in Madrid, the Passante and
Trenord's suburban services in Milan, and Iarnród Éireann's Commuter and
InterCity trains in Dublin, RER and Transilien in Paris, the TER services
in Marseille, CPTM's Linhas 7, 8 and 10 to 13 in São Paulo, SuperVia's Japeri,
Santa Cruz and Belford Roxo lines in Rio de Janeiro, Metrofor's three diesel
lines in Fortaleza, the two diesel VLTs in Recife, Vivi's suburban trains in Riga, and AREX and
GTX-A in Seoul.

**Trams are NOT excluded as a class. A tram is drawn where it is the
rapid-transit system, or where it reaches districts the metro does not; it is
left out where it only runs over the top of a metro.** Many of these maps draw light rail -
San Diego, San Francisco, Los Angeles, Edmonton, Calgary, Miami and Dublin
among them - Marseille draws its three Tramway lines beside its two Métro
lines, and Toulouse draws T1 beside Métro A and B. Where a tram network is left
out, the city already has a metro and the trams run over the top of it: Milan's
17 tram routes stop a block or two apart and the agency publishes no colour for
any of them, and Barcelona's tram falls outside the network-identity test that
picks out its metro. San Francisco's cable cars are out as a different mode. Its
F Market & Wharves streetcar, once left out as a separately branded service, is
drawn for its waterfront, as Rome's tram 8, Madrid's Metro Ligero line 1, Paris's
T3a and T3b and Montréal's REM are drawn for districts their metros do not reach.
Toulouse's cable car is the proof that "cable car" is not itself a reason. Riga has no metro at all, so its seven tram routes are the network, and all are drawn.

**The line is drawn by station spacing and service frequency, not by which
company runs the trains.** SEPTA is the clearest case — the Market–Frankford
and Broad Street Lines are on the Philadelphia map and Regional Rail is not,
and the same agency runs both. Dublin's DART is that judgment reached the other
way: a national-railway service on national-railway track, kept because its
city-centre stations sit about a kilometre apart, which is metro spacing. Both
are recorded in `DECISIONS.md` as decisions with a rejected alternative, rather
than as applications of a rule — because by the letter of the rule DART would
have been dropped.
Copenhagen's S-tog is the second such case: a suburban network on its own
tracks, drawn because inside the city its stations sit about a kilometre and
a quarter apart, every line runs every ten minutes, and most of its stations
there have no Metro station nearby.
Rome's Roma–Viterbo urban service, São Paulo's CPTM Linha 9 and Rio's SuperVia
Deodoro and Saracuruna lines were decided the same way, and Brazil made the
third part of the test explicit: how many of a line's stations have no drawn
station within walking distance.

### Stations left out of a network that IS mapped

Two things remove a station from a network this project maps. Both are recorded
station by station in `outputs/<city>/excluded_stations.csv`, committed to the
repository, and every one of them is counted in the table on this page.

- **It is outside the city.** Rail networks do not stop at municipal
  boundaries, and business registers do: one city's register cannot say what is
  around a station in the next city, so a ring drawn there would come out empty
  for a reason that has nothing to do with commerce. Washington D.C.'s
  Metrorail reaches Maryland and Virginia, Toronto's Line 1 ends past the city
  limit at Highway 407, and Mexico City's Línea B crosses into the State of
  México. **Several maps are deliberately regional instead** — among them
  Miami with its county, Vancouver with Surrey, Guadalajara with three
  neighbouring municipios, and Lille across eleven communes — because there one
  registry covers the whole area. Guadalajara
  goes one step further and leaves out a municipio it could have included:
  Tonalá has no Tren Ligero station, so its businesses could never fall inside
  a ring. **A station can also be outside the city by belonging to a
  neighbouring town's own network**: Marseille's feed carries a sixth line that
  is Aubagne's tram rather than Marseille's, and its seven stations are dropped
  on the same ground as a station across a boundary.
- **Its stops are too close together to draw rings around.** Street-running
  light rail can stop every block or two — far denser than the innermost ring,
  which is a tenth of a mile in most cities and half that in New York, the five
  French cities and Oslo — so
  unthinned, nearly every point in the west of San Francisco would read as
  "next to a station". Where that happens, surface stops are thinned to roughly
  one every half mile measured along the line's own route, while every
  underground station, every terminus and every interchange is kept. It applies
  to San Francisco's Muni Metro and F Market & Wharves, Philadelphia's
  trolleys, the Boston Green Line's surface branches, the trams of Amsterdam and
  Rotterdam, Rome's tram 8, and Hong Kong's Light Rail. The reasoning is in
  `docs/sub_transit_line_filters.md`.

**A thinned stop does not leave a hole in the map.** Stops are thinned to half a
mile apart and the outermost ring reaches 0.6 miles, so the stations that were
kept still cover the ground between them. A station left out for being in
another city is different: there the businesses are outside the register too,
which is the honest limit of a map built from one city's own data.

## Which businesses are counted

**Five kinds of business are left off every map, wherever a register names
them.** Funeral homes, crematoria and cemeteries, which are not places a
passer-by walks into. Food with no counter of its own: canteens inside schools,
offices, hospitals and care homes, event caterers, food trucks, and street and
market stalls. The "other personal services" catch-all that registers keep for
whatever fits nowhere else, which mostly holds people working from home or at
the customer's door, fortune-tellers and dating agencies among them. Adult and
hostess venues, left off for the sake of the people who work there; sex shops
are shops and stay. And gambling: betting shops, casinos, arcades and lottery
agencies. Where a register files one of these under the same label as ordinary
businesses, it cannot be separated and stays on the map; each city's section
says where. Newsstands and kiosks, pawnbrokers, karaoke bars and nightclubs are
kept, and car dealers count as shops everywhere except France.

The rest of this page is the other half — what is excluded from the business
side, city by city, and what is missing from it rather than excluded.

## Excluded everywhere

### Nonstore retailers (NAICS 454)

Electronic shopping and mail-order, direct selling, vending-machine operators,
fuel dealers. **NAICS itself calls these "nonstore"** — there is no shopfront to
walk into. They had been included only because the filter matched the broad
`45` retail prefix, which pulls in the whole family.

Removed: 10.1% of Los Angeles's mapped businesses, 9.0% of San Diego's, 1.7% of
San Francisco's. `454390` "Other direct selling establishments" was also the
single largest group of mapped names that looked like an individual's at a
residential address.

### Parking lots and garages (NAICS 81293)

Parking is a planned trip with a destination in mind, not the incidental foot
traffic near a station that this map is about. A parking structure next to a
station tells you about commuting, not about the retail character of the area.

Removed: 888 mapped businesses in Los Angeles, 637 in San Francisco, 104 in San
Diego.

## Excluded in one city

Registries differ, so some judgments are local. Each was sampled against that
city's own data.

### Los Angeles — All other personal services (NAICS 812990)

Since 2026-09-29 this catch-all is left out in every city.

A national catch-all code. An earlier sample of this code found roughly 90% of
it was not storefront at all: people working from home, professional offices,
and services that travel to the customer. Los Angeles's own data matched that
pattern, and the code supplied most of the map's personal names at residential
addresses.

It was a large exclusion: 31% of the city's otherwise-qualifying businesses.
Los Angeles is unusual in that 68% of its registry rows carry no trade name, so
those rows displayed the registrant's own name.

Also left out: funeral services (93) and food with no counter of its own —
mobile food (348), caterers (147) and food-service contractors (60). **Kept
because it cannot be split:** `722300` "special food services" (3,145 pins),
which this registry uses for caterers, concession stands and food trucks alike,
but also for taquerias and cafés; all of it counts as food service.

### San Diego - its own codes for massage parlours, cottage kitchens and kiosks

San Diego's registry extends NAICS with codes of its own, and four are left
out: `812193` massage parlours (144; massage therapy, `812198`, stays), `72234`
cottage-food operators (192, a licensed home kitchen), `81295`/`812959` kiosk
businesses (26, ecoATM phone-recycling machines), and `8129` "other personal
services" filed at group level (569; calibration labs, waste haulers,
remodellers). With the `81299` catch-all (585), caterers, mobile food and food
contractors (296) and funeral services (19), 1,831 pins leave the map. Pet care
and photofinishing stay.

### San Francisco — Solo massage establishments (NAICS 812990)

The same code number, but San Francisco's licence data labels it "solo massage
establishment" rather than the generic name, so it is a different decision. Of
414 mapped businesses in this category, 31 carried a person-like name at an
address with a residential indicator — the highest share of any category in the
city. A sole practitioner working from home is a sensitive thing to place on a
public map, and the category is a small part of the total, so it is excluded.

Also left out: funeral services (21); food with no counter of its own
(1,300) — food-service contractors (537), caterers (417) and mobile food (325);
and the remaining catch-all rows filed as `81299` (21). The contractor code
goes whole, although the city's own licences show it also holds 139 stadium
and convention-centre concession stands, 21 bars on San Francisco Bay ferries
and a few restaurants.

### New York — licences held by a person, and non-storefront trades

New York is a different case from the others. It has no general business
licence, so instead of filtering one registry down, this map builds its
coverage up from four: restaurant permits, retail food store licences, salon
and barber business licences, and the city's own consumer-protection licences.
The first three are included in full — everything in them is a storefront. The
exclusions are all in the fourth.

**Licences held by a person, not a premises.** The city's consumer-protection
file mixes the two, and roughly 8,900 active licences are held by an
individual: sightseeing guides, locksmiths, general vendors, pedicab drivers,
process servers, tow truck drivers. There is no shop attached to these, and the
address on them is often the licence-holder's home. All excluded.

**Trades that are not storefronts.** Largest by far is **home improvement
contractors** — 13,385 active licences, more than a third of the file. A
contractor works at the customer's house; there is nothing to walk into from a
station. The same reasoning excludes third-party food delivery services,
construction labour providers and general vendor distributors.

Also excluded, each for the reason given: parking lots and garages (1,761 —
parking everywhere on this map), debt collection agencies (1,354 — a back
office), appliance and electronics repair (1,447 — a repair trade, which none
of the three categories covers), hotels (420 — accommodation), pawnbrokers
(272 — lending rather than retail), self-storage (242), employment agencies
(238), tow truck companies (202), car washes (176), process serving agencies
(110), scrap metal processors, industrial laundries, storage warehouses, scale
dealers, and bingo and games-of-chance operators.

**Chair and room renters.** The state's salon and barber registry licenses both
businesses and individuals who rent a chair or a room inside someone else's
shop — about 5,000 of the latter statewide. They are not a separate storefront,
and counting them would both double-count the shop and put an individual on the
map. Only the business licences are used.

### Chicago — non-storefront licence types

Chicago classifies by licence type rather than NAICS, so its exclusions are
named differently but follow the same rule. Left out: home-based businesses
(the city marks these explicitly), peddlers and mobile vendors, temporary and
pop-up trading, shared kitchens, wholesale, parking operators, vehicle repair,
amusements, child care, and licences that merely attach to a business already
counted (an outdoor-patio or late-hour permit, for instance). A business holding
several licences is counted once.

Licences whose only listed activity is "Miscellaneous Personal Services", the
city's catch-all, are left out (133); a licence that also names a specific
service is counted by that service.

Chicago has no funeral licence type. Most funeral homes were licensed under the
"Miscellaneous Personal Services" catch-all and leave the map with it (35). The
29 pins that still carry funeral words sell funeral items, and stay as
funeral-goods shops do everywhere.

### Philadelphia — landlord registrations, and non-storefront permits

Philadelphia licenses activities rather than businesses, so its exclusions are
about separating premises-based trade from everything else the city happens to
license. Of the 50 licence types active in the register, 13 are mapped.

The one that matters most is **`Rental`, which is 79% of all active licences**
— 93,471 residential landlord registrations. These are not businesses and not
storefronts, and on those rows the registry's own business-name field holds
**the owner's personal name at their property address**, recorded as
`Individual`. Mapping active licences unfiltered would have published roughly
94,000 individuals at their homes. It is excluded as a scope error first: these
are not what this map is about. That it also removes the largest privacy
exposure in the dataset is a consequence, not the justification — the same
shape as the NAICS 454 exclusion. **`Limited Lodging Operator`** (short-let
hosts, also at their homes) is out for the same reason, as are the vacant-
property registrations.

Also left out: mobile and pavement trade of every kind (pushcarts, on-foot
vendors, sidewalk sales, and — despite its name — `Vendor - Motor Vehicle
Sales`, which licenses vending *from* a vehicle and whose holders are food
trucks); vehicle repair, towing, wrecking and parking; permits that attach to a
building rather than a business (dumpsters, hazardous materials, high-rise, hot
work); food manufacturing and wholesale; child care; assembly venues; games of
chance; handbill distribution; and event caterers (`Food Caterer`, 193) and
curb markets (10). Newsstands are kept, as small walk-in shops. A business
holding several licences is counted once, so a restaurant with pavement seating
appears as a restaurant rather than twice.

### Miami — offices, wholesale, and one very large service catch-all

Miami-Dade's Local Business Tax receipt is issued to every business of any
kind, so most of the file is not storefront trade. All 150 of its `CATGRYNAME`
values carry an explicit verdict in `pipeline/taxonomies/miami_catgryname.py`;
these are the ones worth naming.

**`SERVICE BUSINESS` (28,010 active rows) is excluded, and it is the largest
single judgment call in this city.** Sampling it found paralegals, management
consultancies, media and tech agencies, tour guides and dispatch services —
offices, not shops — alongside some genuine trade repair, and a number of
COTTAGE FOOD operators working from apartments. It fills the same role as Los
Angeles' NAICS 812990 and D.C.'s "General Business". Excluding it certainly
discards some real storefront repair shops; the honest alternative is
classifying 28,010 rows of free-text `OCCDESC`, which is a project of its own.
Said plainly because the direction of the error is knowable: this map
undercounts small repair and service premises in Miami.

Also excluded: **professional practice** (`PROFESSIONAL`, `ATTORNEY`,
`P.A./CORP/PARTNERSHIP/FIRM`, `CONSULTANT` — about 50,000 rows between them);
**`APARTMENTS`** and the rest of the lodging categories, which are residential;
**`TANGIBLE PERSONAL PROP DLR`** (12,623 rows), which reads like retail and is
not — its sampled holders are wholesale distributors, import/export and online
sellers, many at apartment addresses; contracting and the building trades;
automotive *service* (NAICS 811, where the other cities also draw the line,
while car *sales* are kept as NAICS 441); health, care and education; and
manufacturing and wholesale.

Two exclusions rest on a sample rather than a name, and would be wrong the
other way round without it. **`LAUNDRY MACHINE`** is a machine licence, not a
laundromat: its holders include Paradise Apartments, Camelot Court Apartments
("LAUNDRY ROOM") and Parque Apartments ("10 WASHERS / 10 DRYERS"), so counting
it would drop pins on apartment blocks — real laundries are in
`CLEANER/LAUNDRY/ALTERATIONS`, which is kept. **`UNCLASSIFIED BUSINESS`** is
infrastructure, not shops: Crown Castle and Pinnacle Towers cell sites, with
`OCCDESC` "OTHER MEMO".

Mobile and itinerant trade is out as everywhere else — `LUNCH WAGON / TRUCK`,
`ICE CREAM VENDOR`, `PEDDLER`, carnivals, and the machine licences (`A T M /
POINT OF SALE`, `VENDING MACHINE`). Fitness centres, cinemas and other
recreation venues (NAICS 713/711) are out because no bucket covers them in any
city here. `CATERING BUSINESS` (276) and `FUNERAL HOME` (62) are out too.
`NIGHT CLUB` and `DANCING OR ENTERTAINMENT` are kept as food service.

One category is kept on a cross-project consistency argument rather than a
local one, and is flagged so the choice is visible: **`AUTO / TRUCK / VAN
SALES`** (car dealers). A car lot is not a storefront in the walkable sense
this map is about, but NAICS 441 sits inside the 44/45 range every NAICS city
here counts as Retail, so excluding it in Miami alone would make the buckets
mean different things in different cities.

### Boston — everything that is not food, drink or a package store

Boston's three registries license food, alcohol and cannabis, so the exclusions
here are mostly about not double-counting rather than about scope.

**The Licensing Board's 2,578 Common Victualler licences are excluded, and they
are restaurants.** That is not a judgment about restaurants — they are already
in the Inspectional Services food data, which is the authoritative source for
them, so keeping both would count the same premises twice from two registries.
Only the off-premises retail types are taken from that register: `Retail All
Alc.` (238), `Retail Malt Wine` (68) and a single `Druggist`. 27 premises did
turn out to hold licences in more than one registry and are counted once.

Also excluded from it: **436 residential licences** (`Dormitory` 282, `Lodging
Houses (Frat/Dorm)` 154), which are not businesses — the same category of row
that is 79% of Philadelphia's register; **204 lodging and members' clubs**
(`Inn. All Alc.`, `Innholder No Liquor`, `Clb. All Alc.` and variants); and
about 90 recreation and production licences (`Billiards/Sippio` 38, `Bowling
Alley` 10, seven Farmer Brewery/Winery/Distillery pouring licences, and five
`Fortune Teller`), which are NAICS 713/312 territory that no bucket covers in
any city here.

From the food data, `MFW` (Mobile Food Walk On, 10 premises) is out as mobile
trade is everywhere else, and the cannabis register's one `Delivery (operator)`
is out for the same reason — neither has a shopfront.

### Washington D.C. — an office catch-all, and a register that is mostly homes

D.C.'s single register covers all three categories on its own, so the
exclusions here are about separating businesses from everything else a
"business licence" happens to cover in the District. Every one of the 95
licence categories present has a written verdict in
`pipeline/taxonomies/dc_businessactivity.py`; nothing is excluded by omission.

**61% of the active in-District register is residential rentals**, and they are
dropped before anything is downloaded: One Family Rental 25,557, Apartment
6,081, Two Family Rental 2,558, Short Term Rental 2,196, Vacation Rental 803 —
37,195 rows of 61,329. This is the Philadelphia pattern, where 79% of the
register was landlord registrations, and the reason a raw licence count for a
city means nothing until its distribution is read.

**`General Business` — 11,074 rows — is excluded, and it is the single largest
category exclusion in this project.** It is the District's default for offices
and professional practice: law firms, engineering consultancies, architects,
developers, healthcare and home-care agencies, a locksmith, a police relief
association. Same role as Los Angeles' NAICS 812990 and Chicago's "Limited
Business License".

That exclusion was checked rather than assumed, because a sample of it held a
Wawa and a Cava Mezze Grill next to the law firms. **692 of its rows (6%) share
a licensee with a kept storefront licence and 2,975 (27%) share a Master
Address Repository id** — so a shop that landed in this category keeps its pin
through its real activity licence. What the exclusion removes is offices.

**Three categories are food-adjacent and still excluded**, which is worth
stating plainly because each is a real business:

- **`School Cafeteria (DC)` (242) and `School Cafeteria` (5).** Every sampled
  row is a school — Janney, Marie Reed Elementary, a dozen charter schools. A
  cafeteria behind a school's doors is not premises a passer-by can enter, and
  including it would put a food-service pin on every school in the District.
  Only 3% share an address with a kept storefront, so these are 242 distinct
  school sites rather than shops counted twice.
- **`Caterers` (279).** The closest call here. The sample mixed real
  restaurants that also cater with commissary-kitchen tenants — four separate
  licensees at 2800 10th St NE alone. Measured: 54 (19%) share a licensee with
  a kept storefront licence and stay on the map through it. The rest are
  production kitchens with no counter, so they go the way mobile food goes in
  every other city here.
- **`Food Vending Machine` (60), `Street Vending Business` (273) and
  `Mobile Delicatessen` (1).** Unattended or mobile trade — the same call as
  Boston's `MFW` and the project-wide NAICS 454 "nonstore" carve-out.

**`Health Spa` (22) is gyms, not personal care.** The sampled rows are VIDA
Fitness, Equinox, Gold's Gym, Solidcore, CrossFit and New York Sports Club, so
it is NAICS 713940 and outside every bucket — the same verdict Boston's
Billiards and Bowling Alley licences got. `Health Spa Sales` (22), which is
selling gym memberships, goes with it, as do `Swimming Pool` (165+32), the
theatres and the one bowling alley.

Also excluded, each for the reason the NAICS cities already use: **lodging**
(Hotel 141, Bed and Breakfast 88, Inn and Motel 46, Rooming House 46, Boarding
House 19 — NAICS 721, as in Boston); **construction** (General
Contractor/Construction Manager 991, Home Improvement Salesperson 320, Home
Improvement Contractor 152 — NAICS 23); **vehicular services** (Parking
Facility 263 and its attendants, excluded project-wide; Consumer Goods (Auto
Repair) 78 and Auto Wash 17, because NAICS 811 is repair and only 812 is a
tracked bucket — the same reason Miami's `SERVICE BUSINESS` went);
**charitable and membership bodies** (Charitable Solicitation 1,683, Charitable
Exempt 440, Cooperative Association 176); **wholesale** (NAICS 42); and
**individual rather than premises licences** (Motor Vehicle Salesperson 263,
Auctioneer 15, Tour Guide 3 — a licence attached to a person, not a shopfront).
`Funeral Establishment` (29) is excluded, as funeral services are everywhere.

**One category is kept despite being ambiguous, and it is a large one.**
`Delicatessen` (1,065) is D.C.'s prepared-food catch-all, issued to sandwich
shops and cafés but also to corner shops and convenience stores: a sample of 25
held Julia's Empanadas and Call Your Mother Deli alongside a 7-Eleven, a
Safeway and a convenience store. It is counted as **Food service**, which fits
most of them, but about 180 premises hold it with no other descriptive licence
and could honestly read either way. Excluding it would have removed a fifth of
the city's food service; splitting it would need free-text work the source does
not support. So it is kept, counted as food, and said out loud on the city page.

**Three licence types are endorsements rather than descriptions**, and they are
kept as Retail for that reason: `Cigarette Sales (Retail)` (848),
`Patent Medicine` (610, D.C.'s term for over-the-counter drug sales) and
`Food Products` (656). The sampled Patent Medicine rows included CVS, Whole
Foods and Safeway; a sampled Food Products row was a hardware shop. Holding one
means selling goods over a counter, so Retail is right — but they are why the
premises dedup matters here: 121 licensees hold exactly those first and third
plus Patent Medicine, which is one corner shop and not three businesses.

### Vancouver and Surrey - mobile trade, a regional catch-all, and two cities of offices

The first regional pair here, and the first non-US entry. Vancouver's register
carries **89** business types that reach the map; Surrey's carries **210**
categories, newline-separated, several per licence. Every one of the 299 has an
explicit verdict in `pipeline/taxonomies/vancouver.py`, which **raises** on an
unknown value rather than defaulting to None. Buckets were anchored on
`naics.py` (Retail 44-45 less 454, Food service 722, Personal services 812 less
81293) so this city stays comparable with every city whose buckets are
anchored on `naics.py` instead of drawing its own line. **The anchor is named
rather than counted** - this sentence said "the five NAICS cities" until
2026-09-22, when there were four (San Diego, San Francisco, Los Angeles and
Montreal). What matters is that the boundaries come from the same module, not
how many cities currently use it.

**Mobile trade is not a storefront.** Vancouver's `Street Vendor` (116 mappable
rows) and Surrey's `Portable Food Vendor` (9), `Catering/Coffee Truck` (3),
`Vending Machine` (40), `Mail Order` (24), `Pedlar` and `Ice Cream Vendor` are
excluded, on the same reasoning as the project-wide NAICS 454 exclusion above:
NAICS itself calls these "nonstore". Street Vendor is the largest single
row-count given up to that consistency, and the category is genuinely mixed -
Vancouver licenses food carts and merchandise vendors under one label with no
subtype to separate them. Both registers' `Caterer` (148 and 49), Surrey's
`Concession Stand` (5) and `Flea Market` (1) are out too. Surrey's one
`Adult Entertainment Store` is a sex shop and stays.

**Surrey's catch-all is a regional permission, not a premises.**
`Inter-Municipal Business License Metro` (758) and `Inter-Municipal Business
License FV` (715) are **1,473 rows, 11.3% of Surrey's commercial licences**.
An IMBL lets a business trade ACROSS Metro Vancouver or the Fraser Valley and
is held mostly by contractors; the address on one is the holder's base, not a
shop. Chicago's "Limited Business License" is the same problem, excluded the
same way.

**Home occupations are excluded, and Surrey states them outright.** Surrey's
`LicenseType` reads `Home Occupation` on **14,015 of 27,082 rows (51.8%)**, and
those never enter the pipeline. This is the strongest home-business evidence
anywhere in this project, because the city asserts it rather than the pipeline
inferring it - contrast every US city, which infers it from a parcel join.
Vancouver publishes no equivalent flag, and its parcel-based substitute removes
nothing (see "Honest limits").

**Repair is excluded; personal care is not.** NAICS puts repair in 811 and
personal care in 812, and only 812 is a bucket here, so **a hairdresser counts
and a shoe repairer does not**. Out: Surrey's `Tailor`, `Dressmaker`,
`Upholstery`, `Locksmith`, `Sharpening Service`, `Repair Service`,
`Automotive Repair Service`, `Auto Body/Painting`,
`Automobile Cleaning/Car Wash/Detailing`; and Vancouver's
`General Repair and Maintenance` and
`Vehicle Repair Detailing and Washing Services`. This is the least intuitive
line on this page, and it is applied consistently to both cities.

**Offices, clinics and professional practice are the bulk of both registers.**
Vancouver's single largest category is `Health Care Professionals and Services`
at **4,544** mappable rows, with `Legal Services` (1,796),
`Business Support Services` (993), `Financial Services` (858),
`Consulting and Management Services` (797) and `Real Estate Services` (678)
adding most of the rest. Surrey's `Professional Practitioner-*` series,
`Administration Office`, `Consultant`, `Immigration Consultant` and its
headcount-banded `Real Estate` types are the same shape. Also excluded:
`Long-term Rental` (3,451 in Vancouver - the Philadelphia
`Rental` shape), wholesale, manufacturing, warehousing, construction trades,
education, `Fitness Centre` and the arts/recreation and accommodation groups,
and `Parking Area / Garage` (423) and Surrey's `Parking Lot` (103) under the
project-wide NAICS 81293 exclusion.

Four smaller calls worth naming, because each could reasonably have gone the
other way:

- **BC-regulated health professions are health care; unregulated body-care is a
  personal service.** Surrey's `Massage Therapy (RMT)` (155) and `Acupuncture`
  (56) are regulated professions in British Columbia and are excluded with the
  clinicians. `Holistic Health Care` (58), `Reflexology` (4), `Acupressure`
  (3), `Shiatsu Massage` (2), `Tanning Salon` (10) and `Tattoo Parlour` (13)
  are not regulated, read as NAICS 812199, and count. **Vancouver draws the
  same line itself**, between `Health Care Professionals and Services` and
  `Health Enhancement Services` (111, kept), which is why the rule is the
  registries' rather than this project's invention.
- **Neither a funeral parlour nor a cemetery counts.** Surrey's
  `Funeral Parlour` (4) and `Cemetery` (2) are left out: funeral services are
  off every map.
- **Licence applications are not businesses.** Vancouver's
  `Liquor License Application` (50), `Temp Liquor Licence Amendment` (30) and
  `Cannabis Licence Application` (1) are administrative rows, not premises.
- **`Printing Imaging and Photo Services` (80) is the least comfortable
  exclusion here.** It spans NAICS 323 printing (manufacturing) and 812921
  photofinishing (a personal service), and the label leads with the
  manufacturing reading. Left out rather than split on a guess; worth revisiting
  if the City ever publishes a subtype for it.

**A category that is mostly individuals is a scope error first**, and both
cities' exclusions were justified that way before any privacy argument -
consistent with how Los Angeles' and Philadelphia's were framed. Vancouver's
name-suppression policy is separate and is described under "Honest limits".

### Montréal - vacant units, which a survey can see and a register cannot

**Vacant ground-floor units are excluded, about 3,500 of them.** Montréal is
built from a field survey rather than a licence register - the Ville walks its
commercial streets each year and records what occupies each unit - so, like
Barcelona's census, its source states vacancy outright instead of leaving it to
be inferred. An empty shopfront is premises rather than commerce, and counting
it would measure the supply of retail space instead.

**What is left after that filter is a closer reading of the street than a
licence register can give.** Roughly 69% of surveyed units are storefronts,
against about 28% in a licence-register city, which is why this city's density
is not comparable with the registry cities on either side of it.

**The map is scoped to the agglomeration** - 15 related municipalities
alongside the 19 boroughs - and about a tenth of surveyed units fall in those
municipalities, two of which are not in the survey at all. The Métro does not
reach them, so almost none of this is drawn; read the island's edges as thinner
in the data, not necessarily on the ground.

**Caterers are kept here (107), unlike in every other NAICS city.** The survey
records premises a surveyor walked past, and they are traiteur shops with a
counter, as in France. Left out, as everywhere: funeral services (39) and the
"other personal services" catch-all (30).

### Calgary - endorsements, nonstore trade, and two categories left off on sensitivity

**Calgary's register does most of this page's work itself**, which makes its
exclusions unusually easy to state. Its 96 categories are suffixed with the
distinction most cities here have to infer: `- PREMISES` against `- NO
PREMISES`, plus `(MOBILE)`, `(HOME BASED)`, `(MAIL ORDER)` and `(DIRECT
SALES)`. So `RETAIL DEALER - PREMISES` (7,516 rows) and `RETAIL DEALER - NO
PREMISES` (7) are the same trade, split by the City into the thing this project
maps and the thing it does not. Every value's verdict is in
`pipeline/taxonomies/calgary_licencetype.py`, which raises on an unknown
category rather than defaulting to None.

**Endorsements are excluded, and they are the biggest group.** `ALCOHOL
BEVERAGE SALES (RESTAURANT)` (1,527), `OUTDOOR PATIO` (937), `ALCOHOL BEVERAGE
SALES (DRINKING EST/RESTAURANT)` (446), `(ACCESSORY)` (171) and `(DRINKING
ESTABLISHMENT)` (36) are permissions a premises holds, not premises in
themselves. A restaurant holding a food-service licence, an alcohol
endorsement and a patio endorsement is one restaurant; counting the
endorsements would triple it. This is D.C.'s endorsement problem, and it is
why two in five of Calgary's licences carry more than one category.

**Nonstore and mobile trade is excluded**, on the project-wide NAICS 454
reasoning. The City marks it: `RETAIL DEALER - NO PREMISES`, `MOTOR VEHICLE
DEALER - NO PREMISES` (42), `FOOD SERVICE - NO PREMISES` (27), `FULL SERVICE
FOOD VEHICLE` (50), `PERSONAL SERVICE (MOBILE)`, `MASSAGE CENTRE (HOME BASED)`
and the `(DIRECT SALES)` cleaning variants. **`RETAIL DEALER - PREMISES (MAIL
ORDER)` (59) is excluded despite saying PREMISES** - the suffix nearest the
actual trade wins, and mail order is nonstore. `MARKET` (27) is out: a market
is where stalls stand, not a shop.

**Repair is excluded and personal care is not**, the same NAICS 811-against-812
line Vancouver and Surrey draw: `MOTOR VEHICLE REPAIR AND SERVICE` (1,400
across its variants), `AUTO BODY SHOP` (232) and `FURNITURE REFINISHING` (17)
are out, while hairdressers, tattooists and dry cleaners count.

**The chair renter is excluded.** `PERSONAL SERVICE (INDEPENDENT CHAIR
OPERATOR)` (160) is a person renting a chair inside someone else's salon;
counting them double-counts the salon and puts an individual on the map. New
York drops its state salon registry's renter licence types for the same
reason.

**And two categories are excluded on sensitivity as well as scope**, which is
a departure worth stating plainly because a NAICS-only reading would keep the
first two:

- `BODY RUB CENTRE` (35) and `BODY RUB CENTRE (GRANDFATHERED MASSAGE CENTRE
  COMMERCIAL)` (45)
- `EXOTIC ENTERTAINMENT AGENCY` (8) and `DATING SERVICE OR ESCORT SERVICE` (1)

**89 rows in total.** These are licensed commercial premises at commercial
addresses, and NAICS would place the body rub centres in 812199 personal care
alongside the tattooists that this map does count. They are left off anyway,
on the same reasoning that excluded Vancouver's `Adult Services`: mapping
adult-services premises adds exposure for the people working there without
adding anything to the question this project asks, which is where storefront
commerce clusters around transit. **This is a judgment call, not a data
limitation** - the categories are mapped to None in the taxonomy rather than
deleted, so it is one line to reverse, and the owner confirmed it on
2026-09-21.

**One thing Calgary CANNOT tell us**, recorded here because its absence is
easy to mistake for a decision: `homeoccind` reads `N` on all 23,203 rows.
It is constant, not merely unreliable, so unlike Surrey (`Home Occupation`,
14,015 rows) and Edmonton (`licencetype`, 14,114) the City asserts nothing
about home occupation, and no inference is attempted - Vancouver's parcel
substitute, built for the same silence in its own register, removed nothing.

About 12 pins with funeral words in their names sit under the general retail
licence and stay.

### Edmonton - a register that sorts itself, and one merged category counted anyway

**Edmonton does more of this page's work than any register except Calgary's,
and it does a different part of it.** Calgary names *premises*; Edmonton names
*people*. Its `licencetype` field splits every licence into `Commercial`
(25,105), `Home Based` (14,114), `Non-Resident` (2,108), `Massage Practitioner`
(1,582) and `Adult Services` (763). Only `Commercial` is kept, and that single
filter removes 43% of the file before any category is read - no residence
inference, no name heuristic, no parcel join. `Non-Resident` is mobile trade;
the last two are licences held by a **person** rather than a premises, the New
York `Individual` distinction. Every one of the 60 remaining categories has an
explicit verdict in `pipeline/taxonomies/edmonton_licencecategory.py`, which
raises on an unknown rather than defaulting to None.

**FOUR of the judgment calls were settled by SAMPLING NAMES, and the sample
overrode the rule twice.** This project's merged-category rule - when one
category spans a trade this map counts and one it does not, and cannot be
split, leave it out, because the term nearest the actual trade wins - would
have got two of these wrong:

- **`General Business` (154) is excluded.** The catch-all. Sampling the 111
  rows carrying it alone found parking operators (IMPARK x4, IMPERIAL PARKING,
  two City Centre parkades), coach and scooter fleets (TRAXX COACHLINES, FIRST
  STUDENT, BIRD CANADA, LIME), home-care agencies (HOME INSTEAD, CAREPROS),
  shelters and churches (EDMONTON WOMEN'S SHELTER, HOPE MISSION), daycares and
  a market garden - and **zero storefront retail, food or personal services**.
  Parking is the clincher: NAICS 81293 is the one thing explicitly carved out
  of this project's personal-services anchor, so the largest identifiable group
  in the catch-all is excluded by the anchor itself.
- **`Vehicle Wash / Fueling Station` (336) is excluded**, although Vancouver
  counts its `Gas Station` as Retail. Vancouver's category is pure; Edmonton's
  merges a car wash (NAICS 811192, the repair family excluded everywhere here)
  with a fuel retailer (NAICS 457, which counts). The 40 rows carrying it alone
  are A1A CAR WASH, MILLCREEK CAR WASH, MINT SMARTWASH, CLEAN GETAWAY,
  KINGSWAY, DUGGAN, MINIT, BLUE SKY, KLARITY, ULTRA and a truck wash - against
  two COSTCO GASOLINE and one AFD PETROLEUM. And the genuinely retail ones are
  almost never alone: 248 of the 336 also carry `Retail Sales (Convenience
  Store)` and keep Retail from that. Cost of excluding it: about three fuel
  sites.
- **`Animal Breeding and Boarding Facility` (77) COUNTS, against the rule.**
  The leading term is animal breeding, NAICS 112 agriculture, so the rule would
  exclude it. The sample says otherwise: HOLLYWOOF, PAWS AT PLAY DOG DAYCARE,
  RUFFINGTON'S PALACE, COZY KITTY ACCOMODATIONS, THE PAMPERED PUPPY, POSH POOCH
  HOTEL AND DAYCARE, PETSMART #1202 - pet-care storefronts, NAICS 81291,
  roughly nine in ten. Calgary's `KENNEL SERVICE/PET DEALER` (68) counts for the
  same reason, and excluding Edmonton's because its category names breeding
  first would be an artefact of wording, not a difference in the cities.
- **The `Health Enhancement` family splits four ways, and only the accredited
  CENTRE counts.** Edmonton uses one phrase for four different things:
  `Health Enhancement Centre (Accredited)` (560) **counts**;
  `Health Enhancement Centre` (12) does **not**, because the non-accredited
  variant is pure NAICS 621 - LIFEMARK PHYSIOTHERAPY, WINDERMERE CHIROPRACTOR,
  REVIVE SPINE AND SPORT, HERITAGE LANE CHIROPRACTIC, and nothing else;
  `Health Enhancement Centre (Accredited / Independent)` (115) does **not**,
  being a practitioner working inside someone else's centre, which
  double-counts the centre and puts an individual on the map, as Calgary's
  `INDEPENDENT CHAIR OPERATOR` (160) and New York's `DOSAERENTER` would;
  and `Health Enhancement Practitioner (Accredited)` (25) does **not**, because
  it is a person - **all 25 rows carry `<REDACTED FOR PRIVACY>` as the address,
  which is the publisher's own verdict on what those records are.**

**The one counted against its own contamination, and disclosed for it.**
`Health Enhancement Centre (Accredited)` is 34.3% massage, 11.8% spa/nail/hair
and 4.1% acupuncture by business name - but also **26.4% physiotherapy or
chiropractic**, which is regulated health care and does not belong in a
personal-services bucket. The register cannot separate them. It is counted
anyway, because **Calgary's `MASSAGE CENTRE (COMMERCIAL)` (917) counts** on the
grounds that massage therapy is not a regulated health profession in Alberta -
it is in British Columbia, which is why Vancouver's `Massage Therapy (RMT)`
does not count - and excluding Edmonton's while counting Calgary's would make
the two Alberta cities non-comparable for no reason present in the data. The
effect is that roughly **one in sixteen of Edmonton's personal-services pins is
health care rather than a personal-services storefront**. The city page says
so. This is the one call on this page a reader might reasonably make the other
way, and reversing it is one line in the taxonomy.

**`Food Processing / Catering Service` (583) stays excluded**, which was the
open question Edmonton's build brief flagged as worth the most rows. It merges
NAICS 311 food manufacturing with 7223 catering, leads with processing, and has
no second field to split on - the treatment Vancouver's `Printing Imaging and
Photo Services` got. Reversing it is one line.

**Nonstore and mobile trade is excluded** on the project-wide NAICS 454
reasoning: `Public Market Vendor` (143), `Food Truck / Food Cart` (71),
`Travelling or Temporary Sales` (38), `Public Market Organizer` (32, which runs
the market rather than a stall), `Farmers' Market` (8, the market rather than
its vendors) and `Designated Driver Service` (1).

**Repair is excluded and personal care is not**, the same NAICS 811-against-812
line Vancouver, Surrey and Calgary draw: `Vehicle Repair, Maintenance, and
Modification` (1,174), `Light Duty Repair Service` (205) and `Industrial
Equipment Sales, Rental, and Repair` (373, NAICS 423/532 trade rather than
consumer) are out, while hairdressers, tattooists and dry cleaners count under
`Personal Service` (1,649, 57% spa/nail/hair by name).

**Endorsements are NOT a problem here, and Edmonton is the first Canadian city
where they are not.** Calgary emits one row per category, so its alcohol and
patio endorsements had to be dropped to avoid counting a restaurant three
times. Edmonton emits **one row per licence** with a `";"`-delimited category
list, so an endorsement is a second string on the same row and the pin exists
once either way. That is why `Alcohol Sales (Consumption On-Premises / *)`
(1,420 across both variants) is mapped to Food service here and to None in
Calgary: 1,159 of the larger variant's 1,165 rows also carry another category,
1,034 of them `Restaurant or Food Service`, which `BUCKET_PRIORITY` resolves to
Food service regardless - and the 6 rows standing alone are real drinking
places (NAICS 7224) that mapping the category keeps on the map. `Tobacco and
Vaping Product Sales` (742) and `Oleoresin Capsicum (OC) Spray Sales` (53) are
adjuncts treated the same way; the OC spray licence **never** stands alone, so
it is never decisive.

**And adult services and body rub centres are excluded on sensitivity as well
as scope**, as Calgary's are: `Body Rub Centre` (29), `Adult Service` (3),
`Erotic Entertainment Venue` (3) and `Erotic Entertainment Agency` (2) - **37
rows**, on top of the 763 `Adult Services` licences already removed by
`licencetype`. A NAICS-only reading would keep the body rub centres in 812199
beside the tattooists this map does count. The reasoning is the one the owner
confirmed for Calgary on 2026-09-21: mapping adult-services premises adds
exposure for the people working there without answering the question this
project asks. Mapped to None rather than deleted, so it is one line to reverse.

**Also excluded, without controversy:** offices and professional services
(2,701), construction and labour (2,635), residential rental long- and
short-term (4,187, Philadelphia's `Rental` problem), wholesale and storage
(1,518), manufacturing (1,385), delivery and logistics (510), financial
services (503, NAICS 52 as Vancouver's `Financial Institution`), participant
recreation (450, NAICS 713940 as Vancouver's `Fitness Centre` and Calgary's
`FITNESS CONDITIONING`), commercial schools (428, NAICS 611), exhibition halls
(183), spectator entertainment (148), amusement establishments (116), hotels
and motels (98, NAICS 721 not 722), independent laboratories (69), scrap metal
dealers (52), auctions (14, NAICS 425 agents and brokers - the sample is
livestock and salvage), bingo and casinos (11, NAICS 7132), cannabis processing
(6) and cultivation (3), event production (3) and carnivals (2).
`After Hours Dance Club` (1) counts as food service, as a nightclub does
everywhere here; that premises was already a pin through its retail licence.
`Funeral, Cremation, and Cemetery Service` (19 pins) is out.

### Toronto - endorsements, person-held licences, and a register that is mostly history

**Toronto's exclusions are unusually large in share and unusually dull in
substance**, because most of what its register contains is not premises at all.
Of 159,872 licence rows, **122,301 are already cancelled** - this is a term
history reaching back to 2005 rather than a snapshot - leaving 37,571 current
licences, of which 19,575 are storefronts. Every one of the 92 categories has
an explicit verdict in `pipeline/taxonomies/toronto_mlscategory.py`, which
raises on an unknown rather than defaulting to None.

**One row per licence, and `Category` is single-valued** - which is Calgary's
double-counting problem without Calgary's delimiter to resolve it. A restaurant
with a patio holds two licences and appears as two rows, so endorsements have
to be dropped by category and step 2 then deduplicates on address plus
normalised name.

**Endorsements are excluded, and `NOISE EXEMPTION` is the largest single one.**
`NOISE EXEMPTION` (4,960), `SIDEWALK CAFE` (2,473), `CURB LANE CAFE` (694),
`EXPANDED EATING/DRINKING ESTABLISHMENT` (388) and `EXPANDED ENTERTAINMENT
PLACE OF ASSEMBLY` (44) are permissions a premises holds, not premises. A
restaurant with a patio and a noise exemption is one restaurant. Same call as
Calgary's alcohol and patio endorsements and D.C.'s.

**Person-held and vehicle licences are excluded, and they are most of the
register's bulk**: `TAXICAB OWNER` (9,360), `TOW TRUCK OWNER` (4,959),
`DRIVING INSTRUCTOR (V)` (3,130), `LIMOUSINE OWNER` (2,329), plus the broker,
operator, pedicab and drive-self variants. These are the New York `Individual`
distinction, and they are also why the register's blank-name rate looks
alarming until it is read on the right subset: `Operating Name` is blank on
21.4% of active rows and on **0.5%** of storefront rows, because a taxicab
owner has no trade name and no shop.

**Trades are excluded**: `BUILDING RENOVATOR` (9,065), `MASTER PLUMBER`
(3,274), `PLUMBING CONTRACTOR` (2,365), `MASTER HEATING INSTALLER` (1,433) and
the drain, paving, insulation and chimney variants. **Repair is excluded and
personal care is not**, the NAICS 811-against-812 line every city here draws:
`PUBLIC GARAGE` (11,767) is out, while `PERSONAL SERVICES SETTINGS` (11,105)
and `LAUNDRY PREMISES` (2,247) count.

**Signage and collection permits are excluded** - `TEMPORARY SIGN - MOBILE`
(4,443), `CLOTHING DROP BOX LOCATION PERMIT` (1,246), `MARKETING DISPLAY` (765)
and their variants - as is **parking** (`COMMERCIAL PARKING LOT` 2,058, NAICS
81293, carved out of this project's personal-services anchor), and **nonstore
and mobile trade** on the NAICS 454 reasoning (`MOTORIZED REFRESHMENT VEHICLE
OWNER` 1,360, `HAWKER/PEDLAR` in three forms, `SIDEWALK VENDING` 212).

**`PERMANENT FIREWORKS VENDOR` (31) counts and the four temporary ones do
not**, because the City marks the distinction in the category name the way
Calgary marks `- PREMISES`: `TEMPORARY FIREWORKS VENDOR (OVER 25 KG)` (296),
`(UNDER 25 KG)` (167), `TEMPORARY MOBILE` (227) and `TEMPORARY LEASE` (57) are
seasonal stands. Only the permanent one is a shop.

**`HOLISTIC CENTRE` (2,051) counts, and Ontario's regulation of massage
therapy is why that is clean here.** Ontario DOES regulate massage therapy
(the College of Massage Therapists), so registered therapists are NAICS 621
health care and are licensed provincially rather than appearing in this
register. What Toronto licenses as a holistic centre is therefore the
non-registered remainder, NAICS 812199 personal care. **This is the tidy side
of a line Edmonton sits awkwardly across**: Alberta does not regulate the
profession, so Edmonton's `Health Enhancement Centre (Accredited)` mixes
physiotherapy and chiropractic clinics in and had to be counted with a
disclosed 26% contamination. Toronto needs no such caveat.

**`PET SHOP` (118) is Retail here, where Edmonton's `Animal Breeding and
Boarding Facility` (77) is a Personal service.** Not an inconsistency: a pet
shop sells animals and supplies (NAICS 459910 retail), while boarding and
daycare is NAICS 81291 pet *care*. Toronto licenses the shop; Edmonton licensed
the service.

**And adult-services premises are excluded on sensitivity as well as scope** -
`BODY RUB PARLOUR` (110), `ADULT ENTERTAINMENT CLUB` (51) and `BATH HOUSE`
(14), **175 rows**. The reasoning is Calgary's and Edmonton's, confirmed by the
owner on 2026-09-21: mapping adult-services premises adds exposure for the
people working there without answering the question this project asks. Mapped
to None rather than deleted, so it is one line to reverse.

**Also excluded, without controversy:** entertainment and recreation
(`ENTERTAINMENT PLACE OF ASSEMBLY` 445, `AMUSEMENT ESTABLISHMENT` 437,
`BILLIARD HALL` 177, `THEATRE` 73, `BOWLING HOUSE` 38, `CARNIVAL` 16, `CIRCUS`
5, `SWIMMING POOL` 3), `PAYDAY LOAN` (187, NAICS 522291), `SECOND HAND SALVAGE
YARD` (68, a yard rather than a shop), `AUCTIONEER` (251) and `COLLECTOR OF
SECOND HAND GOODS` (66) as people rather than premises, `SHORT TERM RENTAL
COMPANY` (5, NAICS 721), and `** Class record not on file. (138)` (4), which is
the register's own placeholder.

**Nightclubs count as food service** — 36 active premises, about 32 new pins
once geocoded — as in every other city. Adult entertainment clubs stay out.

### Mexico City - street stalls, a nonstore twin, and a heuristic that does not speak Spanish

**Semifijo premises are excluded — 20,586 of 462,732 economic units (4.45%),
of which 18,264 would otherwise have classified into a bucket.** DENUE records
`tipoUniEco` as `Fijo` or `Semifijo`; a semi-fixed unit is a stall or street
post rather than a storefront. This project maps storefronts, so the same
reasoning that excludes nonstore retail everywhere excludes these. It is a
scope decision, not a data-quality one: street commerce is a real and large
part of Mexico City's retail geography, and **this map does not show it.**
Owner's decision, 2026-09-22.

**SCIAN 469 — nonstore retail — is excluded**, the exact twin of NAICS 454
excluded in every US city: *"Comercio al por menor exclusivamente a través de
Internet, y catálogos impresos, televisión y similares"*. Small here, 90 units
in Mexico City against nonstore's 10.1% of Los Angeles' pins, and excluded on
the same reasoning regardless of size.

**SCIAN 812410 — parking — is excluded**, the twin of NAICS 81293. 2,230 units.
A parking trip is planned rather than incidental foot traffic from a station.

Also excluded: public toilets and shoe-shine stands (`812130`, 1,646), the
"other personal services" catch-all (`812990`, 977), funeral services (629),
event caterers (146), institutional canteens (82) and food trucks (61).

**Not excluded but absent by construction: 811 repair and 813 associations.**
Personal services is anchored on **812**, not the whole of 81, so auto repair
(27,216 units in Jalisco, the largest block inside 81) and civic, religious and
professional associations never enter. Food service is anchored on **722**, not
72, so 721 accommodation — hotels — never enters either. Both are the same
precision the NAICS cities use; a two-digit prefix would have been the
obvious-looking mistake.

**What is NOT excluded, and is worth stating because the number looks
alarming:** `scripts/check_personal_exposure.py` reports that 32.2% of Mexico
City's pins "look like a person". A hand-sample of 26 found **none** that were
a person presented as a person — every one was a shop sign in the Spanish
convention of trade type plus a given name or brand (`ABARROTES LIZ`,
`ESTETICA MARIFER`, `ZAPATERIA SOFI`), and `COCINA ECONOMICA` — two common
nouns — also trips it. The heuristic is tuned for English "SMITH JOHN" forms
and does not transfer; Mexico City is this project's first non-English city.
Nothing is filtered on that number.

### Guadalajara (Regional) - a municipio with no station, and the same Spanish-name artefact

**Everything excluded in Mexico City is excluded here, for the same reasons and
from the same register:** Semifijo premises (3,768 units, 1.9% - a smaller
share than Mexico City's 4.45%, and excluded on the same reasoning regardless),
SCIAN **469** nonstore retail, and SCIAN **812410** parking. Food service is
anchored on **722** and personal services on **812**, so 721 accommodation, 811
repair and 813 associations never enter. See the Mexico City section above for
the measurements behind each.

Also excluded: public toilets and shoe-shine stands (`812130`, 227), the
"other personal services" catch-all (`812990`, 238), funeral services (207),
event caterers (77), institutional canteens (34) and food trucks (14).

**Tonalá is excluded, and it is the only whole municipio this project has left
out of a region it could have included.** DENUE holds **19,897** economic units
there and they are already downloaded - entidad 14 is the whole of Jalisco. No
Tren Ligero line reaches Tonalá, and a municipio with no station contributes
businesses that no ring can ever contain, so including it would have inflated
the city total while changing no ring. The four municipios kept -
Guadalajara, Zapopan, San Pedro Tlaquepaque and Tlajomulco de Zúñiga - are the
ones SITEUR's own line descriptions name.

**An operating line is NOT excluded, and it nearly was.** The only GTFS feed
available for Guadalajara expired on 28 January 2023 and contains three of the
four lines - Línea 4 opened on 15 December 2025. Building from it would have
silently omitted that line, its 8 stations and 21 km of route. The geometry
comes from OpenStreetMap instead, which has all four. Recorded here because a
missing line is the most consequential kind of omission a map like this can
have, and this one was avoided rather than accepted.

**The person-like reading is an artefact here too.** 30.7% of pins trip
`scripts/check_personal_exposure.py`'s heuristic, against Mexico City's 32.2%,
and for the same reason: it is tuned for English "SMITH JOHN" forms and the
Spanish shop-sign convention pairs a trade type with a given name. Nothing is
filtered on that number.

### Monterrey (Regional) - four municipios by code, two lines under construction, and a whole-city layer

**Everything excluded in Mexico City and Guadalajara is excluded here, from the
same register:** Semifijo premises (3,269 units, 2.8%), SCIAN **469** nonstore
retail and **812410** parking. Food service is anchored on **722** and personal
services on **812**, so 721 accommodation, 811 repair and 813 associations never
enter. Repair is the largest of those here - 9,593 fixed premises at the
2026-09-27 screen, in an industrial city - and is most of why storefronts are a
smaller share of fixed premises than in the other two Mexican cities.

Also excluded: public toilets and shoe-shine stands (`812130`, 72), the
"other personal services" catch-all (`812990`, 125), funeral services (156),
event caterers (78), institutional canteens (51) and food trucks (33).

**No whole municipio is left out.** Monterrey, San Nicolás de los Garza,
Guadalupe and General Escobedo are exactly the municipios a station's 0.6-mile
ring reaches; no other municipio in Nuevo León has a Metrorrey station. They are
selected by INEGI's municipio code, the same key OpenStreetMap carries, so the
register and the boundaries cannot disagree about which municipio is which.

**Storefronts located outside those four municipios are dropped: 22, 0.04%.**
They are misplaced coordinates - some sit 550 km away - and the test is the
municipios' own boundaries rather than a bounding box, which would have dropped
about a hundred real storefronts in southern Monterrey.

**Two lines are not drawn because they do not carry passengers yet.** Líneas 4
and 6, a monorail network, are under construction; the operator's own map marks
them so, and OpenStreetMap already carries eleven of their stations. The
pipeline refuses to run if either appears in a Metrorrey route. Ecovía (bus
rapid transit), TransMetro and MetroEnlace are buses, not rail.

**The whole-city heat layer is ON here**, as it is again for the other two
Mexican cities (owner's call, 2026-09-27). At 58,564 points it keeps the map small, and it
loads on phones since heat data ships as `JSON.parse`.

**The person-like reading is an artefact here too.** 34.4% of pins trip the
heuristic; a hand-sample of 30 were all shop signs (a trade type with a name, or
a brand), none a person presented as a person. One pin is dropped by the
renderer's contact-detail scrub - a shop sign styled as an e-mail address.

### Madrid - accommodation, trades with no shopfront, and a zero where a location should be

**Hotels and tourist flats are excluded** - accommodation rather than food
service, the same carve-out Barcelona needs and for the same reason. So are
wholesale, vehicle repair, and premises with no shopfront at all, such as
online and vending sales. So are canteens in schools, care homes, social
centres, offices, sports grounds and hospitals (1,157), banquet halls and event
caterers (90), the register's "other personal services (astrology, contact
agencies)" catch-all (43) and funeral parlours (30). The three categories are
the register's own activity classification, not NAICS.

**About one storefront premises in eleven cannot be placed on the map.** The
register gives every premises a coordinate, and **9.2%** of those in these
three categories carry a literal zero instead of a location. They are left out
rather than guessed at. The loss is not even across the city - it falls hardest
on Barajas and the centre, and hardest of all on tourist flats and hostels,
which this map does not show anyway.

### Barcelona - empty shopfronts, accommodation filed under restaurants, and 458 rows that could not be classified

**One ground-floor unit in nine is empty, and those are excluded.** A tenth of
the premises surveyed are recorded as having no economic activity - vacant, for
sale or to let. Barcelona states vacancy outright where most registers leave it
to be inferred, so this is one of the few cities here where empty shopfronts
can be taken out rather than silently counted as businesses.

**Hotels, hostals and pensions are excluded**, although the census files them
in the same group as restaurants and bars: **720 accommodation rows** sit
inside a group whose own name says so, in Catalan. Offices, health, education,
finance, repair, storage and construction are excluded too.

**458 rows are dropped rather than assigned to Retail.** They sit in a sector
that explicitly mixes retail with wholesale, and the census's finer levels say
nothing more about them. "It is in a sector whose name contains retail" is not
evidence about a premises, so they are excluded and counted here instead of
being folded into the biggest bucket - which would have been a guess wearing a
number's clothes.

**Premises inside shopping centres, galleries and municipal markets ARE
counted.** The census flags them and this map deliberately ignores the flag: a
mall beside a station is commercial density a rider can reach.

**Kept, although part of it is clinics:** `Veterinaris / Mascotes` (395) puts
vets under one value with pet shops and groomers; about 160 read as veterinary
clinics by name, and the census cannot separate them.

### Dublin - a register of premises rather than of businesses

**Nothing here is excluded on the basis of what a business is called, because
no name is published at all.** Tailte Éireann's rateable valuation register
records *premises* rather than occupiers: no trade name, no occupier, no owner.
Each pin shows the address a valuation is filed against and the use recorded
against it. No business is named on this map, so the personal-name question
does not arise.

**Where a premises carries more than one use, the more specific trading use is
what it is counted as** - a shop with offices above it is a shop, a salon
behind a shopfront is a salon. A premises whose recorded uses are none of
retail, food service or personal service is not on the map.

**Betting shops are left out (175)**, with a casino and an amusement centre that
had reached the map through a "shop" use beside them. So are markets (4) and
funeral homes (38). Kiosks stay: a kiosk is a small walk-in shop.

### Milan - six registers kept apart, and a category the register cannot mark

**Milan's premises come from six separate registers and are deliberately not
merged.** The city licenses neighbourhood shops, bakers, artisan food makers,
bars and restaurants - inside and outside the commercial plan - and personal
services, each in its own register. A single Milan address routinely holds many
separate premises, so merging the registers on address would delete real ones.
Where one business holds two licences it is counted twice: these counts read
slightly high rather than slightly low, which is the deliberate direction to
err in and the opposite of New York's choice for the same problem.

**The register of premises licensed outside the commercial plan carries staff
canteens, private clubs and parish halls alongside ordinary bars.** Those that
identify themselves are filtered out, but the register does not mark them
reliably, so some remain. This is an exclusion that is incompletely applied
rather than a category left in on purpose, and it is the one limit on this
city's map worth knowing before reading its food-service colours.

Milan's registers carry no funeral code; about 29 funeral services reach the
non-food shop layer through the shop register, and they stay.

### Paris - four trades with no premises, and two catch-alls the publisher's own hierarchy settled

**The source is SIRENE, France's national register of établissements**, so the
exclusions below are French rather than Parisian and apply to Marseille too.
INSEE strips records it marks *non-diffusible* at source - name, address and
coordinates together - so that privacy work was done before the data arrived
rather than by a filter here.

**Four kinds of trade are excluded because their own official label says there
is no premises.** Distance selling (`47.91A`, `47.91B`), doorstep selling
(`47.99A`) and vending or other non-shop channels (`47.99B`) sit *inside* the
retail division and have no shopfront at all - together the single largest
correction the city needed. Market-stall trading (`47.81Z`, `47.82Z`,
`47.89Z`) is the publisher saying the trade happens on a pitch, which also
makes the registered address the trader's own. Contract catering (`56.29A`) is
a canteen inside someone else's institution. Wholesale laundry (`96.01A`) is
industrial - and its retail twin `96.01B` is **kept**, because INSEE itself
splits the pair *de gros* / *de détail*.

**Two of the five catch-alls are dropped and three are kept, decided by the
class label rather than by the word "autres".** `96.09Z` (9,349 rows) sits
under a class that asserts no premises at all, and `56.29B` (958) under
catering; both are excluded, and `96.09Z` is the direct French analogue of the
NAICS 812990 that Los Angeles excludes. But `47.19B` (5,359), `47.29Z` (1,413)
and `47.78C` (903) sit under classes whose official labels contain **en
magasin** - INSEE stating the premises exists - so they stay. This is
Barcelona's finding in French: the publisher's hierarchy settling a call that a
reading of the language would have got wrong.

**Funeral services (`96.03Z`) are excluded** — 261 here.

**Car dealers are not on the French maps, unlike every other city here.**
SIRENE files vehicle sales in their own division, not with retail. Four selling
codes would add about 9,500 pins across the five cities (5,384 in Paris), but
95% record no employees and about a quarter carry a premises name: mostly
one-person traders, probably registered at home. Left off on that ground
(owner, 2026-09-29).

**What is left is still more than a street survey would find, and that is
disclosed rather than filtered.** Against OpenStreetMap's mapped shops in the
same commune the map carries roughly **1.8 times** as many points after these
exclusions, down from about 2.0 before them. SIRENE records where a business is
*registered* and some registered establishments have no customer-facing
shopfront, with nothing in the data saying which. Tuning filters until the two
numbers agreed would be fitting to a number rather than measuring one.

### Marseille - the same register, and a ferry question left open on purpose

**Everything excluded in Paris is excluded here, from the same national
register and for the same reasons** - the four no-premises trades, the wholesale
laundry, funeral services, and the same two catch-alls `96.09Z` and `56.29B`.
The catch-all verdict was re-measured rather than inherited: the two cities'
compositions differ, which is why the shares were counted for Marseille instead
of Paris's being assumed.

**The gap against OpenStreetMap is wider here - about 2.6 times as many points -
and most of that is not the register.** OpenStreetMap covers Marseille far
less completely than it covers Paris. On restaurants, where the two schemes
mean nearly the same thing, the ratio falls to **1.7×**, close to Paris's 1.8×,
which is the comparison worth trusting.

**The harbour ferries are excluded, and this one is flagged rather than
settled.** The Vieux-Port shuttles and the Frioul islands service are genuine
urban transit - as Vancouver's SeaBus is, dropped on the same ground - and
they are left out because this project measures density around *rail* stations
and no built city draws a ferry. Recorded as an owner's decision on 2026-09-23 for possible
revisiting, not as an automatic application of a rule.

### Toulouse - the same register again, and the first mode drawn here that is not a train

**Everything excluded in Paris is excluded here, from the same national
register and for the same reasons** - the four no-premises trades, the
wholesale laundry, funeral services, and the same two catch-alls `96.09Z` and
`56.29B`. The verdict was measured a third time rather than inherited, and this
is the city that shows why that is not ceremony: `96.09Z` is **13.9%** of
Toulouse's bucket rows against roughly 9.7% in both Paris and Marseille. The
national argument transfers; the shares plainly do not.

**A fifth of this city's active establishments are withheld by INSEE, not by
this project.** `statutDiffusion` masks the name, the address **and** the
geolocation together on **20.2%** of active rows here - the highest of the six
French candidates and well over double Paris's 8.5%. That single upstream
exclusion is larger than every filter on this page put together, and nothing in
the data says which businesses it removed. **A street that looks thin in
Toulouse may be a quiet one or a private one**, and the map cannot tell them
apart.

**Twelve tram stations are excluded for being in another commune - more than
any other line in this project loses.** Tramway T1 runs out through Blagnac and
Beauzelle to the Airbus works and the exhibition centre, and this map covers the
commune of Toulouse, so those twelve stops and the rings around them are not
drawn. Métro A loses Balma-Gramont and Métro B loses Ramonville on the same
rule. All fourteen are listed, with the commune each lies in, at
`outputs/toulouse/excluded_stations.csv`. Blagnac's businesses are in the
same national register, so this is a scoping choice rather than a data limit -
the map keeps to the commune so that Toulouse, Paris and Marseille are drawn on
the same terms.

**Nothing is excluded here for being a cable car.** Téléo is drawn: three
stations, all inside the commune, and the first non-rail mode anywhere on this
site. It is included rather than excluded because Tisséo runs and tickets it
exactly as it does the métro, because it crosses the Garonne where no other line
does, and because one of its three stations is a Métro B interchange. The
reasoning, including the fact that the precedent originally cited for it turned
out not to exist, is recorded in `DECISIONS.md`.

### Lille (Regional) - the same register, eleven communes, and no station lost to a boundary

**Everything excluded in Paris is excluded here, for the same reasons** - the
four no-premises trades, the wholesale laundry, funeral services, and the two
catch-alls `96.09Z` and `56.29B`. They were measured again rather than
inherited: `96.09Z` is 11.2% here, between Marseille and Toulouse.

**No station is excluded for its location, because the boundary is drawn
around the stations.** This map covers the eleven communes the network serves,
so where every other French city lists stations lost to its commune line,
Lille has none. What the scope does leave out is the other 84 communes of the
Métropole Européenne de Lille, none of which has a station.

**About one active establishment in six is withheld by INSEE, not by this
project** - 16.6% across the eleven communes - with the name, the address and
the coordinates removed together, so those rows cannot reach the map.

**Two things tagged as trams in OpenStreetMap are not drawn**, because they are
not ilévia's: a heritage tourist tram in the Deûle valley, and a disused
railway.

### Rennes - the same register, and one line that leaves the commune at both ends

**Everything excluded in Paris is excluded here, for the same reasons** - the
four no-premises trades, the wholesale laundry, funeral services, and the two
catch-alls `96.09Z` and `56.29B`. They were measured again rather than
inherited: `96.09Z` is 14.0% here, level with Toulouse, and its rows show the same sign of sole traders
registered at home - rows with no employee band are 28.8% catch-all, against
9.8% for rows that record one.

**Four métro stations are excluded for being in another commune, all on Métro b
and including both of its ends.** Atalante and Cesson - Viasilva are in
Cesson-Sévigné; La Courrouze and Saint-Jacques - Gaîté are in
Saint-Jacques-de-la-Lande. The line is drawn to its ends, but no ring is drawn
around those four. They are listed, with the commune each lies in, at
`outputs/rennes/excluded_stations.csv`. Those communes' businesses are in the
same national register, so this is a scoping choice rather than a data limit.

**About one active establishment in six is withheld by INSEE, not by this
project** - 17.5% here - with the name, the address and the coordinates removed
together, so those rows cannot reach the map.

### Oslo - premises rather than companies, and a sole trader's name kept off the map

**Excluded by the classification itself, anywhere in Norway** - eight SN2025
codes whose own labels place the work away from a shop: the four intermediation
codes new in NACE Rev. 2.1 (agents arranging a sale or a service for someone
else), mobile food outlets, canteens and other catering, catering for events,
and personal services performed in the customer's home - 1,314 rows. Event
catering is excluded here and kept in France, deliberately: a French *traiteur*
is usually a shop, while Norway's label says the work happens at the event.

**Excluded as a catch-all, on Oslo's own numbers** - `96.990`, *other personal
services not elsewhere classified*: 811 rows, of which 5% record any employee
and 87% belong to a sole trader, the strongest home-based signature measured in
any city here. The five retail catch-alls are kept.

Funeral services are excluded too, as everywhere: 40 premises.

**Excluded because the business is ending** - 260 premises whose parent
company is bankrupt or being wound up.

**Left off because they could not be placed** - about 3% of premises whose
address did not match Kartverket's register, mostly entries whose address line
is a building name or a "c/o".

**What cannot be excluded: web shops.** Norway's classification follows NACE
Rev. 2.1, which abolished the separate codes for selling online or from market
stalls, so an online-only clothes seller carries the same code as a clothes
shop. France excludes distance selling by code; Oslo cannot, and the map
includes some businesses with no storefront.

**Shown, but not named: sole traders.** Every premises belonging to a sole
trader shows its address instead of its name, because in 89% of them the
business name is the owner's own. They remain on the map; only the name is
withheld.

**Twelve T-bane stations are excluded for being in Bærum**, on the western
branches of lines 2, 3 and 5, and are listed with their municipality in
`outputs/oslo/excluded_stations.csv`. **Ferries are not drawn**, as in
Marseille.

### Copenhagen - production units, two municipalities, and a personal owner's name kept off the map

**Excluded by the classification itself, anywhere in Denmark** - the same eight
kinds of work Oslo excludes, read against Denmark's DB25 labels: the four
intermediation classes new in NACE Rev. 2.1, mobile food stalls, event catering,
contract catering and canteens, and personal services in the client's home.
Denmark adds one split of its own, excluding industrial and institutional
laundries while the dry cleaner on the corner stays. 1,326 rows.

**Excluded as a catch-all, on Copenhagen's own numbers** - `969900`, *other
personal services not elsewhere classified*: 613 rows, 84% personally owned and
half above the ground floor, against 41% and 23% for storefronts overall. A
sample held coaching, healing, consulting and dog walking. It also held about
seventy tattoo studios and a few dog groomers, which are lost with it, and the
map's page says so. The six retail catch-alls and "other eating places" are
kept.

Funeral services are excluded too, as everywhere: 56 premises.

**Left off because they could not be placed** - 256 premises (under 2%) that
carry no address in Denmark's official address register, more of them
personally owned than the storefronts as a whole.

**What cannot be excluded: web shops.** As in Oslo, DB25 follows NACE Rev. 2.1,
so an online-only seller carries the code of the goods it sells.

**Shown, but not named: personally owned businesses.** Every premises of a sole
proprietorship, a small personally owned business or a partnership shows its
address instead of its name, as does any name carrying Denmark's sole-trader
marker "v/" ("by"). They remain on the map; only the name is withheld. Addresses
recorded "care of" another person are never read.

**Two municipalities, one map.** The map covers Copenhagen and Frederiksberg,
which Copenhagen entirely surrounds. Businesses in the surrounding
municipalities are not counted, although the national register holds them.

**Fifty-nine stations are excluded for being outside the two municipalities** -
fifty-seven S-tog stations on the lines' suburban reaches and the Metro's two
airport stations in Tårnby - and are listed with their municipality in
`outputs/copenhagen/excluded_stations.csv`. **Regional and InterCity trains are
not drawn, nor the Hovedstadens Letbane**, which has no stop in either
municipality.

### Prague - establishments rather than companies, and a sole trader's home kept off the map

**Excluded by the classification itself, anywhere in Czechia** - personal
services performed in the customer's home (439), catering and contract catering
(101), and retail intermediation (10): 550 rows, read against the Czech
Statistical Office's own CZ-NACE 2025 labels. So are funeral services (66).

**Excluded because it is probably a home** - 1,500 establishments of people
trading in their own name at their own registered address, which for a Czech
sole trader is usually where they live.

**The "other personal services" catch-all is excluded, as in every city — three
rows here**; the 2025 classification already sorts that work into specific
classes. Day spas, saunas and massage salons are a
specific class and are kept.

**Missing rather than excluded** - about 57,000 Prague establishments belong to
businesses whose main activity is something other than retail, food or personal
services, such as a brewery's pub or a wholesaler's shop, and are not shown. Each
establishment carries its owner's single main activity, and no open source
records its own.

**What cannot be excluded: web shops.** As in Oslo and Copenhagen, the
classification files an online seller under the goods it sells.

**Shown, but not named** - every establishment of a person trading in their own
name, or of a partnership, shows its address instead of its name.

**Left off because they could not be placed** - 2 establishments whose address
carries no coordinates.

**All 58 metro stations are inside the city.** Trams, which run as a dense
overlay on the metro, the Petřín funicular, ferries and suburban trains are not
drawn. Flora, closed for reconstruction, is drawn.

### Amsterdam - two registers, and a shop unit that is also a home kept off the map

**Two layers, two categories.** Food service is the city's register of
hospitality permits; everything else is the national buildings register's shop
units, which record what a unit is for rather than what trades there, so retail
and personal services are one category here, "Shops and services".

**Excluded from the permit register** - cafés and canteens inside another venue,
such as a sports club, community centre or theatre (318 permits), hotels (72),
hall hire (32), cultural venues (17), members-only societies (13), and 35
permits of unknown type whose own description is one of these.

**Excluded because it is probably a home** - 757 shop units also registered as
a dwelling.

**Removed as duplicates** - 486 shop units at the same address as a permit; the
permit, which names the business, is kept.

**Missing rather than excluded** - takeaways that need no hospitality permit,
and 22 permits whose address could not be placed.

**What cannot be excluded: empty shops.** About one shop unit in twenty stood
empty at the start of 2026, and no open source says which.

The building register records only a shop unit, so a funeral home there cannot
be identified or removed.

**Shown, but not named** - every shop unit shows its address.

**Stations.** GVB's metro lines 50 to 54 and sixteen tram lines are drawn. 22
stops outside the municipality are left out - 12 in Amstelveen, 5 in Diemen, 3
in Uithoorn, 2 in Ouder-Amstel - and 59 tram stops are thinned to about one per
half mile. Tram 3, which is not running, the museum tram, ferries and NS trains
are not drawn.

### Rome - a register of premises with no names and no closing dates

**Excluded by the register's own types** - online shops (8,995), storage and
display premises (5,150), wholesale (2,097), door-to-door (1,909) and mail-order
(644) selling, vehicle hire (1,776) and garages (1,086), private members' clubs
(1,144), phone centres (649), business agencies (627), arcades and gaming
machines (910), vending machines (289), internal company shops (230), festival
stalls (189) and farm stays (2).

**Workshops** - 17,086 workshops record no trade and are left out. Of those that
do, repairs, car work, tailoring, dental laboratories, metalwork and similar
trades (9,290) are left out; food makers count as food service, and laundries,
nail bars, tattoo studios and dog groomers as personal services.

**Missing rather than excluded** - 4,478 premises whose address could not be
matched to a house number (2,783 not found, 1,695 with no number), and any
premises registered since July 2025.

**What cannot be excluded: closed premises.** The register records no closing
date. It lists about 2.7 times as many restaurants, bars and cafés as
OpenStreetMap, and the oldest registrations match a mapped place most often, so
the excess is not old closures that a cut-off could remove.

**Not named** - the register has no business names; every dot shows its activity
and address.

**Stations.** Metro A, B, B1 and C and the Roma–Viterbo railway's urban service,
Flaminio to Montebello, are drawn; the urban service passes the
spacing-and-frequency test that Dublin's DART and Copenhagen's S-tog passed.
Monte Compatri – Pantano, in Monte Compatri, is left out. Not drawn: trams, which
run over the metro in the centre; the Roma–Lido railway (Metromare), whose
stations are about two kilometres apart and whose trains run every 15 to 20
minutes; the Roma–Viterbo railway beyond Montebello; and suburban trains.

### São Paulo - a census of establishments, read from free text

**Excluded by what the enumerator wrote** - offices and professional premises (52,407),
parking and storage (44,793), vehicle and repair workshops (40,992), industry and trades
(33,360), vacant premises (32,653), public, civic and education premises (16,201),
places of worship (9,154), events venues (2,306), accommodation (1,766) and other
non-premises (2,495); and 5,940 rows with no usable description.

**Funeral homes, wakes, crematoria and cemeteries are excluded** (558 across the nine
cities).

**Missing rather than excluded** - 108,311 establishments whose description no rule can
read, mostly bare brand or trade names: about a third of those that might be
storefronts, commoner near stations and in commercial districts. By hand-read samples,
roughly one storefront in ten to one in seven within the station rings is missing.

**What cannot be excluded: change since 2022.** The census recorded what was trading
during its fieldwork.

**Not excluded, because the census cannot say it:** food trucks, trailers, kiosks and
stalls. About 320 descriptions across the nine cities mention a trailer or food truck,
and about 1,400 start with quiosque, barraca or banca, but a beach kiosk is a fixed
premises and a trailer may stand in one spot for years. They count as whatever the rest
of the description names.

**Shown, but not named** - at an address that is also a home (37% of dots), the dot
shows its category, never the enumerator's description.

**One dot for many** - a shopping centre or gallery recorded as one entry is one dot.

**Stations.** Metrô Linhas 1–5 and 15 and CPTM Linha 9 are drawn; Linha 9's two
stations in Osasco are left out. Not drawn: CPTM Linhas 7, 8 and 10 to 13, whose
stations inside the city are 2 to 3.5 km apart; Linhas 6 and 17, under construction;
buses and bus corridors.

### Rio de Janeiro - the same census, and rail from two sources

**Excluded by what the enumerator wrote** - vacant premises (22,954), parking and storage (18,528), vehicle and repair workshops (15,286), offices and professional premises (14,669), industry and trades (9,827), public, civic and education premises (8,131), places of worship (6,692), events venues (2,526), accommodation (1,930) and other non-premises (1,657); and 4,155 rows with no
usable description.

**Funeral homes, wakes, crematoria and cemeteries are excluded**, as in São Paulo.

**Missing rather than excluded** - 51,532 establishments whose description no rule can
read, mostly bare brand or trade names: about a third of those that might be storefronts, a little more near the stations - about 35 in a hundred.

**What cannot be excluded: change since 2022.** The census recorded what was trading
during its fieldwork.

**Not excluded, because the census cannot say it:** food trucks, trailers, kiosks and
stalls, as in São Paulo.

**Shown, but not named** - at an address that is also a home (55% of dots), the dot
shows its category, never the enumerator's description.

**One dot for many** - a shopping centre or gallery recorded as one entry is one dot.

**Stations.** MetrôRio Linhas 1, 2 and 4, the VLT Carioca's four lines and SuperVia's
Deodoro and Saracuruna lines are drawn; the Saracuruna line's three stations in Duque de
Caxias are left out. Not drawn: SuperVia's Japeri, Santa Cruz and Belford Roxo lines,
with stations further apart or trains less often; the Santa Teresa tram; the Corcovado
railway; and the Complexo do Alemão cable car, closed since 2016.

### Belo Horizonte - the same census, and a line opened in July 2026

**Excluded by what the enumerator wrote** - vacant premises (12,939), vehicle and repair workshops (8,628), offices and professional premises (8,370), parking and storage (7,514), industry and trades (6,007), public, civic and education premises (3,767), places of worship (1,917), events venues (580), accommodation (246) and other non-premises (557); and 1,203 rows with no
usable description.

**Funeral homes, wakes, crematoria and cemeteries are excluded**, as in São Paulo.

**Missing rather than excluded** - 27,675 establishments whose description no rule can
read, mostly bare brand or trade names: about four in ten of those that might be storefronts, slightly more near the stations.

**What cannot be excluded: change since 2022.** The census recorded what was trading
during its fieldwork.

**Not excluded, because the census cannot say it:** food trucks, trailers, kiosks and
stalls, as in São Paulo.

**Shown, but not named** - at an address that is also a home (36% of dots), the dot
shows its category, never the enumerator's description.

**One dot for many** - a shopping centre or gallery recorded as one entry is one dot.

**Stations.** Metrô BH Linhas 1 and 2 are drawn, Linha 2 running at weekday peak hours
only since it opened on 3 July 2026; Linha 1's two stations in Contagem are left out.

### Brasília - the same census, where an address names a block

**Excluded by what the enumerator wrote** - vacant premises (6,925), vehicle and repair workshops (6,893), offices and professional premises (6,621), industry and trades (5,322), parking and storage (5,025), public, civic and education premises (3,347), places of worship (1,821), events venues (503), accommodation (269) and other non-premises (392); and 989 rows with no
usable description.

**Funeral homes, wakes, crematoria and cemeteries are excluded**, as in São Paulo.

**Missing rather than excluded** - 26,057 establishments whose description no rule can
read, mostly bare brand or trade names: about four in ten of those that might be storefronts.

**What cannot be excluded: change since 2022.** The census recorded what was trading
during its fieldwork.

**Not excluded, because the census cannot say it:** food trucks, trailers, kiosks and
stalls, as in São Paulo.

**Shown, but not named** - at an address that is also a home (69% of dots), the dot
shows its category, never the enumerator's description. Brasília's addresses name a block rather than a door, so
this is judged by the block's lot.

**One dot for many** - a shopping centre or gallery recorded as one entry is one dot.

**Stations.** Metrô-DF's Linha Verde and Linha Laranja are drawn, across the whole
Federal District. Not drawn: 104 Sul and Onoyama, still being built.

### Salvador - the same census, and one station over the boundary

**Excluded by what the enumerator wrote** - parking and storage (12,006), vehicle and repair workshops (7,241), vacant premises (5,999), industry and trades (4,290), offices and professional premises (4,207), public, civic and education premises (3,458), places of worship (2,570), events venues (468), accommodation (339) and other non-premises (282); and 2,631 rows with no
usable description.

**Funeral homes, wakes, crematoria and cemeteries are excluded**, as in São Paulo.

**Missing rather than excluded** - 25,502 establishments whose description no rule can
read, mostly bare brand or trade names: about a third of those that might be storefronts.

**What cannot be excluded: change since 2022.** The census recorded what was trading
during its fieldwork.

**Not excluded, because the census cannot say it:** food trucks, trailers, kiosks and
stalls, as in São Paulo.

**Shown, but not named** - at an address that is also a home (56% of dots), the dot
shows its category, never the enumerator's description.

**One dot for many** - a shopping centre or gallery recorded as one entry is one dot.

**Stations.** Linha 1-Vermelha and Linha 2-Azul are drawn; Linha 2's last station,
Aeroporto, in Lauro de Freitas, is left out.

### Fortaleza (Regional) - the same census, and a município with no station

**Excluded by what the enumerator wrote** - vacant premises (12,203), vehicle and repair workshops (11,021), parking and storage (10,972), industry and trades (8,994), offices and professional premises (7,306), public, civic and education premises (4,179), places of worship (2,247), events venues (607), accommodation (470) and other non-premises (482); and 2,143 rows with no
usable description.

**Funeral homes, wakes, crematoria and cemeteries are excluded**, as in São Paulo.

**Missing rather than excluded** - 42,506 establishments whose description no rule can
read, mostly bare brand or trade names: about four in ten of those that might be storefronts, slightly more near the stations.

**What cannot be excluded: change since 2022.** The census recorded what was trading
during its fieldwork.

**Not excluded, because the census cannot say it:** food trucks, trailers, kiosks and
stalls, as in São Paulo.

**Shown, but not named** - at an address that is also a home (54% of dots), the dot
shows its category, never the enumerator's description.

**One dot for many** - a shopping centre or gallery recorded as one entry is one dot.

**Stations.** Metrofor's Linha Sul is drawn. Not drawn: Metrofor's three diesel lines -
Linha Oeste, the Parangaba–Mucuripe VLT and the airport branch - which run every 30 to
60 minutes. Caucaia's only stations were Linha Oeste's, so its businesses are counted
with no station of its own.

### Porto Alegre (Regional) - the same census, six municípios along one line

**Excluded by what the enumerator wrote** - vacant premises (10,630), offices and professional premises (9,113), parking and storage (7,789), vehicle and repair workshops (7,170), industry and trades (5,530), public, civic and education premises (3,933), places of worship (1,609), events venues (584), accommodation (286) and other non-premises (376); and 1,026 rows with no
usable description.

**Funeral homes, wakes, crematoria and cemeteries are excluded**, as in São Paulo.

**Missing rather than excluded** - 31,465 establishments whose description no rule can
read, mostly bare brand or trade names: almost half of those that might be storefronts, and about half near the stations, so the station areas are the most under-drawn part of this map.

**What cannot be excluded: change since 2022.** The census recorded what was trading
during its fieldwork.

**Not excluded, because the census cannot say it:** food trucks, trailers, kiosks and
stalls, as in São Paulo.

**Shown, but not named** - at an address that is also a home (42% of dots), the dot
shows its category, never the enumerator's description.

**One dot for many** - a shopping centre or gallery recorded as one entry is one dot.

**Stations.** Trensurb's Linha 1 is drawn, Mercado to Novo Hamburgo, across the six
municípios it runs through. Not drawn: the airport people mover.

### Recife (Regional) - the same census, and a município with no station

**Excluded by what the enumerator wrote** - parking and storage (9,188), vehicle and repair workshops (7,452), vacant premises (7,387), offices and professional premises (5,653), industry and trades (4,992), public, civic and education premises (3,418), places of worship (1,677), events venues (416), accommodation (301) and other non-premises (550); and 2,568 rows with no
usable description.

**Funeral homes, wakes, crematoria and cemeteries are excluded**, as in São Paulo.

**Missing rather than excluded** - 33,903 establishments whose description no rule can
read, mostly bare brand or trade names: about four in ten of those that might be storefronts.

**What cannot be excluded: change since 2022.** The census recorded what was trading
during its fieldwork.

**Not excluded, because the census cannot say it:** food trucks, trailers, kiosks and
stalls, as in São Paulo.

**Shown, but not named** - at an address that is also a home (44% of dots), the dot
shows its category, never the enumerator's description.

**One dot for many** - a shopping centre or gallery recorded as one entry is one dot.

**Stations.** The Metrô do Recife's Linha Centro, on its Camaragibe and Jaboatão branches,
and Linha Sul are drawn. Not drawn: the diesel VLTs to Curado and Cabo, whose stations
are 3 to 4 km apart. Cabo's only stations were its VLT's, so its businesses are counted
with no station of its own.

### Santos (Regional) - the same census, two cities joined by a VLT

**Excluded by what the enumerator wrote** - vacant premises (2,521), offices and professional premises (2,328), parking and storage (2,240), vehicle and repair workshops (1,910), industry and trades (1,260), public, civic and education premises (1,190), places of worship (565), events venues (200), accommodation (99) and other non-premises (173); and 343 rows with no
usable description.

**Funeral homes, wakes, crematoria and cemeteries are excluded**, as in São Paulo.

**Missing rather than excluded** - 7,127 establishments whose description no rule can
read, mostly bare brand or trade names: almost four in ten of those that might be storefronts, slightly more near the stops.

**What cannot be excluded: change since 2022.** The census recorded what was trading
during its fieldwork.

**Not excluded, because the census cannot say it:** food trucks, trailers, kiosks and
stalls, as in São Paulo.

**Shown, but not named** - at an address that is also a home (35% of dots), the dot
shows its category, never the enumerator's description.

**One dot for many** - a shopping centre or gallery recorded as one entry is one dot.

**Stations.** The VLT's Linha 1 and Linha 2 are drawn across Santos and São Vicente,
Linha 2 running from 9 to 15h since it opened on 1 December 2025. Not drawn: the
heritage tourist tram.

### Rotterdam - a food layer rebuilt from permit notices, and a shop unit that is also a home kept off the map

**Rebuilt rather than read** - Rotterdam publishes no hospitality register. 3,223 exploitation,
provisional and coffeeshop permits granted inside their term, merged where they share a place,
give 1,939 premises.

**Left out of the notices** - alcohol licences (991), terrace permits (589), gaming-machine
permits (366), short-term event permits (27), sex-business permits (14), permits under other
bylaws (8), one refusal and one withdrawal, and 20 notices that are not permits; exploitation
permits older than five years and coffeeshop permits older than one.

**Excluded because it is probably a home** - 26 shop units also registered as a dwelling.

**Removed as duplicates** - 563 shop units within 3 m of a permit premises; the permit is kept.

**What cannot be excluded: closed premises and empty shops.** A premises that closed stays until
its permit would have run out (about one in seven, measured on Amsterdam); about 7% of shop units
were registered vacant on 1 January 2025 (CBS). The building register records only a shop unit,
so a funeral home there cannot be identified or removed.

**Not named** - no dot carries a business name; shop units show their address.

**Stations.** RET metro A-E and trams 1-8 and 11 are drawn, on the timetable after the works
that shorten trams 4, 6 and 8 until 22 November. 52 stops outside the gemeente are left out - 18
in Schiedam, 7 in Vlaardingen, 5 in Barendrecht, 4 in Den Haag, 3 each in Capelle aan den IJssel,
Maassluis, Pijnacker-Nootdorp and Nissewaard, 2 each in Lansingerland, Albrandswaard and
Leidschendam-Voorburg - and 23 tram stops are thinned by the spacing filter to about one per half
mile. Not drawn: tram 12 (event days), temporary trams 14 and 18 (during the works), ferries and
NS trains.

### Hong Kong - licensed food premises only, at FEHD's own points

**What the registers cannot show: general retail and personal services.** FEHD licenses
restaurants, food shops and a few specified trades; clothing, electronics and general shops, and
hair and beauty salons, need no FEHD licence and are simply absent. Read the balance between
categories as a fact about Hong Kong's licensing, not about its streets.

**Left out of the registers** - food factories (11,568), frozen confection factories (558),
factory canteens (444), cold stores (90) and milk factories (9); swimming pools (1,441),
undertakers (145), funeral parlours (7), offensive trades (4) and slaughterhouses (2); places of
public entertainment (262), cinemas and theatres (73) and karaoke establishments (62).

**Not placed** - 28 licences with no point yet on FEHD's CSDI layers; none is placed by guessing
from its address.

**Counted once** - 2 second licences held under the same shop sign at the same address.

**Named** - each dot carries the shop sign on its licence; the registers hold no licensee's name.
308 licences carry FEHD's "no record" placeholder and show "No shop sign on the licence".

**Stations.** MTR's Island, Tsuen Wan, Kwun Tong, Tseung Kwan O, South Island, Tung Chung, Tuen Ma
and East Rail lines and the Light Rail are drawn. Not drawn: the Airport Express (Airport and
AsiaWorld-Expo left out), the Disneyland Resort Line (Disneyland Resort), the high-speed rail, the
Peak Tram and Hong Kong Tramways. Racecourse, open on race days only, is left out, and 17 Light
Rail stops are thinned by the spacing filter to about one per half mile.

### Riga - food from the excise register, shops from the cadastre, vacancy measured only in the centre

**Two sources, two categories.** Food service is the premises licensed to sell alcohol or tobacco
whose place type is food service; a café that sells neither is missing, so that layer is a lower
bound. Shops and services is every trade premises in the cadastre whose name reads as a shop or a
service; the cadastre records use, not occupancy, so that layer is an upper bound.

**Left out of the excise register** - licences no longer in force or at a place that has closed;
shops, fuel stations, warehouses, offices and kiosks (the cadastre is the shop layer); hotels.
One premises per address and kind: a venue holds several licences, and the holder that would tell
two venues apart is never read.

**Left out of the cadastre** - trade premises named as fuel stations, wholesale or storage, food
service (the excise register is the food layer), gambling, offices, dwellings and ancillary rooms;
412 shops in buildings the city lists as degrading. The building register records only a shop
unit, so a funeral home there cannot be identified or removed.

**Not placed** - 48 food premises whose address matched no address point; 34 shops whose building
had no footprint.

**Not named** - food dots show the kind of place and the street address without its unit number;
shop dots show the premises' registered name. No licence holder is ever read.

**Vacancy.** 20.4% of 2,324 street-front ground-floor premises in the historic centre and its
protection zone (2024), 15% in the Old Town (2025); not measured elsewhere.

**Stations.** Rīgas satiksme's seven tram routes are drawn; 15 stops are thinned by the spacing
filter to about one per half mile. Not drawn: buses, trolleybuses and Vivi's suburban trains.

### Seoul - Korea's permit registers: the trades Korea licenses, not every shop

**Missing, not excluded.** Korea licenses food service, the personal-care trades and a set of
food and tobacco retail trades, not retail in general: a clothes shop, a bookshop or a phone
shop holds none of these permits, so the Retail category leans towards food and convenience
stores.

**Left out** - lodging (숙박업) and veterinary clinics (동물병원), whose registers only lend
building points; hostess bars and cabarets (유흥주점, the adult-services rule); food trucks,
caterers and mobile cooking; wholesale meat, milk and egg traders and meat importers (every
축산판매업 channel but butchers); health-food sellers who trade online, door to door or by phone
(every 건강기능식품 channel but in-store); closed, suspended and cancelled permits.

**Counted once** - a premises holding several permits at one building: retail by brand for
the five convenience-store chains and by name otherwise (58,514 retail permits to 51,663
premises), food and personal services by name.

**Not placed** - 4,875 open permits with no point of their own and none at their building
(3,258 food, 1,301 retail, 316 personal services).

**Names withheld** - 138 premises whose registered name is a bare personal name at an
address that reads as a home. The telephone column is never read.

**Stations.** Lines 1–9, the Shinbundang Line, the Ui LRT, the Sillim Line and three Korail
lines are drawn, with stations inside Seoul only: 223 stations of those lines outside the city
are left out. Not drawn: AREX, GTX-A, the Seohae Line, the Gimpo Goldline and intercity trains;
every station they serve in Seoul is also on a drawn line.

### Daegu - Korea's permit registers, as Seoul's, a year older than their label

**Missing, not excluded.** Korea licenses food service, the personal-care trades and a set of
food and tobacco retail trades, not retail in general: a clothes shop, a bookshop or a phone
shop holds none of these permits, so the Retail category leans towards food and convenience
stores.

**Left out** - hostess bars and cabarets (유흥주점, the adult-services rule); lodging (숙박업) and
veterinary clinics (동물병원), which are not read; food trucks, caterers and mobile cooking;
wholesale meat, milk and egg traders and meat importers (every 축산판매업 channel but butchers);
health-food sellers who trade online, door to door or by phone (every 건강기능식품 channel but
in-store); closed, suspended and cancelled permits.

**Counted once** - a premises holding several permits at one building: retail by brand for
the five convenience-store chains and by name otherwise (18,400 retail permits to 16,269
premises), food and personal services by name.

**Not placed** - 612 open permits with no point of their own and none at their building
(231 food, 335 retail, 46 personal services).

**Names withheld** - 113 premises whose registered name is a bare personal name at an
address that reads as a home. The telephone column is never read.

**Dated** - the files are published as the August 2026 edition, but their records end in late
August 2025 (the newest update is 2025-09-02), so the map shows Daegu as it stood then.

**Stations.** Lines 1–3 are drawn, with stations inside Daegu only: 5 stations of Lines 1 and 2
in Gyeongsan are left out. Not drawn: the Daegyeong Line (대경선), a Korail commuter line whose
stops in Daegu are about 4 km apart, and intercity trains. Seodaegu, served only by the
Daegyeong Line, has no ring.

### Busan - Korea's permit registers, as Seoul's, frozen at 15 April 2026

**Missing, not excluded.** Korea licenses food service, the personal-care trades and a set of
food and tobacco retail trades, not retail in general: a clothes shop, a bookshop or a phone
shop holds none of these permits, so the Retail category leans towards food and convenience
stores.

**Left out** - hostess bars and cabarets (유흥주점, the adult-services rule); lodging (숙박업) and
veterinary clinics (동물병원), which are not read; food trucks, caterers and mobile cooking;
wholesale meat, milk and egg traders and meat importers (every 축산판매업 channel but butchers);
health-food sellers who trade online, door to door or by phone (every 건강기능식품 channel but
in-store); closed, suspended and cancelled permits.

**Counted once** - a premises holding several permits at one building: retail by brand for
the five convenience-store chains and by name otherwise (22,571 retail permits to 20,140
premises), food and personal services by name.

**Not placed** - 810 open permits with no point of their own and none at their building
(279 food, 468 retail, 63 personal services).

**Names withheld** - 114 premises whose registered name is a bare personal name at an
address that reads as a home. The telephone field is never read.

**Dated** - the city's feed stopped updating on 15 April 2026, when the national licensing data
moved to a new service; permits granted or closed after early April 2026 are not shown.

**Stations.** Lines 1–4 and the Busan–Gimhae LRT are drawn, with stations inside Busan only: 5
stations of Line 2 in Yangsan and 12 of the LRT in Gimhae are left out. Not drawn: the Donghae
Line (동해선), a Korail commuter line whose stops in Busan are about 2.3 km apart, and intercity
trains. Ten stations served only by the Donghae Line, from Centum and Sinhaeundae to Gijang and
Ilgwang, have no ring.

### Taichung - Taiwan's national tax register, joined to the city's door plates

**Left out** - online shopping (industry code 487); funeral services (443); street and market
stalls (1,101) and caterers, banquet cooks and school-lunch contractors (266); the "other
personal services" catch-all, fortune-telling and marriage introduction (574); every industry
outside retail, food service and personal services; 1,521 company head-office rows on an upper
floor or in a numbered room, which read as offices (owner's rule; buildings with 20 or more
storefront rows exempt).

Drinking places and restaurants with shows are kept: their register names claim no hostess
service.

**Not placed** - 5,599 rows whose address matched no door plate: market and roadside stalls,
intersections, and rural addresses.

**Names not shown** - 11,907 sole proprietors whose registered name carries no business
marker are shown by their line of business (owner's rule; the register publishes no owner
column, and the Fiscal Information Agency declines to publish owners' names).

**Department stores** - brands trading inside one are generally not registered at its
address, so a department store tends to appear as a single point.

**Stations.** Taichung Metro's Green Line is drawn; every station is inside the city. Not
drawn: Taiwan Railway and high-speed rail.

### Taoyuan - the same register and rules as Taichung, on the Airport MRT

**Left out** - online shopping; funeral services (288); street and market stalls (553) and
caterers, banquet cooks and school-lunch contractors (182); the "other personal services"
catch-all, fortune-telling and marriage introduction (388); industries outside the three
buckets; 1,177 office-like company head-office rows (owner's rule).

Drinking places and restaurants with shows are kept: their register names claim no hostess
service.

**Not placed** - 3,097 rows whose address matched no door plate (rural addresses, stalls,
intersections).

**Names not shown** - 7,230 unmarked sole proprietors, shown by their line of business.

**Stations.** The Airport MRT is drawn to its ends; its 15 stations inside Taoyuan are
counted, and the seven in Taipei and New Taipei (A1-A6, A9) are left out. Not drawn: Taiwan
Railway and high-speed rail. The line does not reach Taoyuan District, the city's largest
centre, so most storefronts lie outside the rings.

### Taipei (Regional) - Taipei and New Taipei, the same register and rules

**Left out** - online shopping; funeral services (634); street and market stalls (2,669) and
caterers, banquet cooks and school-lunch contractors (272); the "other personal services"
catch-all, fortune-telling and marriage introduction (811); industries outside the three
buckets; 10,138 office-like company head-office rows (6,232 in Taipei, 3,906 in New Taipei;
owner's rule).

Drinking places and restaurants with shows are kept: their register names claim no hostess
service.

**Not placed** - 9,364 rows whose address matched no door plate: about 3,600 stalls in
Taipei's traditional markets and under viaducts (owner: left off rather than stacked on their
market's plate), rural addresses and intersections.

**Names not shown** - 17,890 unmarked sole proprietors, shown by their line of business.

**Stations.** Every metro and light-rail line in the two cities is drawn; the Airport MRT's
15 stations in Taoyuan are left out here and counted on Taoyuan's page. Not drawn: Taiwan
Railway, high-speed rail and the Maokong Gondola.

### Kobe - the city's food permits and 生活衛生 registers, joined to MLIT's address blocks

**Left out** - every shop that is not a food shop (Japan has no general business licence, so none
is published); food businesses that only notify the city (届出: many convenience stores and
greengrocers); food manufacturing other than bakeries and confectioners (菓子) and delis
(そうざい), 879 rows; 153 vending machines; 194 institutional caterers; 1,943 food trucks and
stalls registered to trade anywhere in the city (市内一円); storeless laundry pick-ups; mobile
salons.

**Counted, and measured** - 115 of the 2,362 bakery, confectioner and deli rows (4.9%) carry a
trade name that reads as a factory or central kitchen (工場, センター, 本社); they are kept (owner,
2026-09-27).

**Not placed** - 85 rows (0.3%): Rokkō-san's mountain addresses and a few hill and park
addresses. Another 684 are placed at their district's centre rather than their block.

**Names not shown** - 10 premises whose trade name is the operator's own name are shown by their
permit type (owner's rule).

**Closed premises** - the city's list may keep premises that have closed; a dot is a permit on
file, not a business open today.

**Stations.** Every line with a station in the city is drawn, cut at the city line: the stations
beyond it, in Akashi, Miki, Ashiya, Sanda, Takarazuka, Harima and Nishinomiya, are left out. Not
drawn: the Shinkansen (Shin-Kobe is kept as a subway station) and the Maya and Rokkō cable cars.

### Osaka - the city's food permits and 生活衛生 registers, joined to MLIT's address blocks

**Left out**
- Every shop that is not a food shop: Japan has no general business licence,
  so none is published.
- Food businesses that only notify the city (届出: many convenience stores and
  greengrocers).
- Food manufacturing other than bakeries and confectioners (菓子) and delis
  (そうざい): 1,502 rows.
- 138 vending machines.
- 2,157 food trucks, stalls and mobile salons registered to trade anywhere in
  the city (市内一円).
- 38 linen-supply laundries (リネンサプライ), industrial rather than counters
  (owner, 2026-09-27).

**Counted, and measured** - 151 of the 4,227 bakery, confectioner and deli rows
(3.6%) carry a trade name that reads as a factory or central kitchen; they are
kept (owner, 2026-09-24).

**Not placed** - 13 rows (0.02%): addresses in 上町's lettered blocks, and two
that name no real block. Another 637 are placed at their district's centre.
Against the coordinates the city publishes beside each permit, the block point
sits a median 38 m away, and 98.7% sit within 250 m.

**Names not shown** - 9 premises whose trade name is the operator's own name
are shown by their permit type. The owner's rule is applied to every permit at
the premises.

**The list against national statistics** - Osaka City's published list holds
about 70% of the restaurant permits Osaka reports to national statistics; the
page gives the owner-approved explanation.

**Closed premises** - the list may keep premises that have closed; a dot is a
permit on file, not a business open today.

**Stations.** Every line with a station in the city is drawn, cut at the city
line.
- Left out: the stations beyond it, in Sakai, Higashiōsaka, Suita, Yao,
  Moriguchi, Kadoma, Matsubara, Toyonaka, Settsu, Habikino, Daitō and
  Fujiidera.
- Kept: Taishibashi-Imaichi, whose Tanimachi Line platform is in the city and
  whose Imazatosuji Line platform is in Moriguchi (owner).
- Not drawn: the Shinkansen (Shin-Osaka is kept as a JR and Metro station), and
  the Umeda freight line's track from the Umekita platforms to Fukushima, which
  only limited expresses use.

### Sapporo - the city's food permits and 環境衛生 registers, joined to MLIT's address blocks

**Left out**
- Every shop that is not a food shop: Japan has no general business licence,
  so none is published.
- Food businesses that only notify the city (届出).
- Food manufacturing other than bakeries and confectioners (菓子) and delis
  (そうざい): 987 rows.
- 3 vending machines.
- 983 food trucks, stalls and storeless laundry pick-ups registered to trade
  anywhere in the city (市内一円) or with no counter.
- 14 linen-supply laundries (リネンサプライ), industrial rather than counters.
- 16 barbers and beauty salons inside hospitals and care homes (厚生施設),
  which serve their residents rather than the public.

**Counted** - coin laundries, as Personal services (owner, 2026-09-28: near
transit they draw steady short-term customers). And 157 of the 2,151 bakery,
confectioner and deli rows (7.3%) carry a trade name that reads as a factory
or central kitchen; they are kept (owner, 2026-09-24).

**Not placed** - 41 rows (0.1%), most of them premises the city registers at
addresses outside Sapporo. Another 4,101 are placed at their block group's
(条丁目) centre, which on Sapporo's grid is about one block.

**Names not shown** - 6 premises whose trade name is the operator's own name
are shown by their permit type. The owner's rule is applied to every permit at
the premises.

**Closed premises** - the list may keep premises that have closed; a dot is a
permit on file, not a business open today.

**Stations.** Every line with a station in the city is drawn, cut at the city
line.
- Left out: the stations beyond it, in Tōbetsu, Otaru and Ebetsu.
- No Shinkansen reaches Sapporo yet.

### Fukuoka - the city's food permits and registers and MHLW's online filings, joined to MLIT's address blocks

**Left out**
- Every shop that is not a food shop: Japan has no general business licence.
- Food shops that only notify (届出) and did not publish in MHLW's list: the
  Retail layer is partial.
- 11,768 MHLW filings published without an address, 4,203 of them restaurants
  (about one in five).
- 1,434 rows of food manufacturing and storage other than bakeries and
  confectioners (菓子) and delis (そうざい).
- 742 school, hospital, care-home and staff kitchens.
- 507 vending machines.
- 2,919 food trucks, festival and event stalls, on-train sales and other rows
  with no fixed counter.
- 58 restaurants inside hotels and inns.
- 62 mail-order and online sellers.
- 10 karaoke boxes.
- 103 snack bars (スナック).
- 39 caterers (仕出し).
- 111 filings MHLW marks as closed (廃業).

**Counted** - Fukuoka's 81 yatai (屋台, filed as ろ店), which trade nightly at
fixed street spots under the city's yatai ordinance (owner, 2026-09-28). Also,
74 of the 2,450 bakery, confectioner and deli rows (3.0%) have a trade name
that reads as a factory; they are kept (owner, 2026-09-24).

**One pin per premises** - 297 premises in both food lists are shown once, from
MHLW's newer filing.

**Not placed** - 88 rows (0.3%), mostly rural addresses and on-train sales.
Another 537 MHLW filings sit at MHLW's own coordinates, and 29 at their
town-chōme centre.

**Names not shown** - 4 trade names in the city's own lists are the operator's
own name; the 5 pins carrying them show their permit type. MHLW's list does not
say who the operator is, so the rule cannot run on its rows (owner,
2026-09-28).

**Closed premises** - a dot is a permit on file, not a business open today.

**Stations.** Every line with a station in the city is drawn, cut at the city
line.
- Left out: 22 stations beyond it, in Kasuya, Ōnojō, Sue, Shingū, Kasuga,
  Itoshima, Koga, Umi and Sasaguri.
- The JR Hakata-Minami line (only Hakata is inside the city).
- The Shinkansen does not count.

### Kyoto - a food register rebuilt from the city's monthly lists, and its registers, joined to MLIT's address blocks

**Left out**
- Every shop that is not a food shop: Japan has no general business licence.
- Shops that sell only packaged food: a notification since 2021, not in these
  lists.
- 1,993 food trucks and other permits with no fixed address.
- 62 permits for less than a year.
- 1,144 rows of food manufacturing other than bakeries and confectioners (菓子)
  and delis (そうざい).
- 166 vending machines.

**Counted** - permits still in their term on 31 July 2026. Closures are not
published, so this is an upper bound. 1,321 of them share an address and permit
type with a newer permit under another name; they are probably predecessors
that closed, but they are kept. Also, 126 of the 3,586 bakery, confectioner and
deli rows (3.5%) have a trade name that reads as a factory; they are kept
(owner, 2026-09-24).

**One pin per premises** - 523 repeat permits are shown once.

**Not placed** - 435 rows (1.3%), mostly in town names that occur twice in one
ward. Another 1,836 sit at their town's centre.

**Names not shown** - 8 pins whose trade name is the operator's own name show
their permit type.

**Stations.** Every line with a station in the city is drawn, cut at the city
line.
- Left out: 25 stations beyond it: 8 in Ōtsu (Shiga), 7 in Uji, 3 each in
  Mukō and Nagaokakyō, and 2 each in Yawata and Ōyamazaki.
- The Sagano Scenic Railway and the Eizan and Kurama cable cars are not drawn
  (owner, 2026-09-28).
- The Shinkansen does not count.

### Tokyo - eight wards' own food lists, national filings for four, and four wards' registers, joined to MLIT's address blocks

**Left out**
- The fifteen wards with no usable food-permit list: Chiyoda, Bunkyo, Sumida,
  Shinagawa, Ota, Nakano, Suginami, Toshima, Kita, Arakawa, Itabashi, Nerima,
  Adachi, Katsushika and Edogawa. Their stations are drawn hollow and nothing
  there is counted. Seven of them publish barber, beauty and laundry
  registers, which are not used: a ward's stations are not counted from those
  alone.
- Every shop that is not a food shop: Japan has no general business licence.
- Shops that sell only packaged food, except where a list includes
  notifications.
- 1,086 food trucks, stalls and other permits with no fixed address.
- 8,973 national filings whose applicants did not publish an address.
- 1,728 rows of food manufacturing other than bakeries and confectioners (菓子)
  and delis (そうざい).
- 1,718 vending machines, 1,042 school, hospital and staff canteens, 515
  temporary and mobile permits, 276 premises inside hotels and inns, 133
  entertainment venues, 71 mail-order businesses, 2 linen suppliers and 2
  salons inside welfare facilities.
- 2,536 bars and snack bars filed under the permit sub-types バー・キャバレー
  (bars and cabarets, one sub-type) and スナック (hostess-staffed snack bars)
- 83 caterers (仕出し)
- 22,368 closed premises, which Shibuya's list and the national filings keep,
  marked.

**Kept, though possibly the same sub-type:** Meguro abbreviates its bar permits
as 飲食バー (102), without the cabaret or snack detail.

**Counted** - each ward's list as the ward publishes it; the page gives each
one's share of the official count (9% to 101%). 114 of the 4,385 bakery,
confectioner and deli rows (2.6%) have a trade name that reads as a factory;
they are kept.

**One pin per premises** - 2,500 repeat permits are shown once, and 1,016
national filings for a premises already in its ward's list.

**Not placed** - 33 rows. Another 158 sit at their town's centre, and 35
national filings at their own coordinates.

**Names not shown** - 2 pins whose trade name is the operator's own name show
their permit type. Only the lists that name their operators can be checked.

**Stations.** Every line with a station in the 23 wards is drawn, cut at the
ward line.
- 293 stations in the fifteen wards without data are drawn hollow.
- Left out: 55 stations beyond the ward line: 40 in neighbouring prefectures,
  and 15 in the Tama area (5 in Nishitokyo, 4 in Chofu, 2 each in Mitaka and
  Komae, 1 each in Higashikurume and Musashino).
- The Narita Sky Access and the Saitama Railway are not drawn (one station each
  in the wards, served by other lines); the Tokaido and Shonan-Shinjuku lines
  are not drawn on their own.
- The Shinkansen does not count.

### Berlin - the chamber of commerce's members, with no names and no crafts

**Excluded by the classification itself** - catering and contract catering
(3,155), retail intermediation (331), personal services performed in the
customer's household (19), intermediation for personal services (25), mobile
food stalls (23) and food-service intermediation (1): 3,554 rows, read against
the register's own WZ 2025 labels.

**Excluded as catch-alls** - "other personal services" (10,210), which holds
trade-fair hosts, hospitality services, clearance firms, escort and
prostitution among much else, as in Oslo and Copenhagen; and general non-food
retail (12,194), the broad registration a trader takes to sell anything,
anywhere, which is mostly online and market trading. **Not a catch-all:**
department stores sit under the same heading in the register and are kept.

Funeral services are excluded too, as everywhere: 44 premises.

**Missing rather than excluded** - craft businesses belong to the Handwerks-
kammer, not the chamber of commerce, so hairdressers, laundries and dry
cleaners are almost entirely absent and bakers and butchers are thin.
Personal services on this map is beauty and nail salons, spas, saunas and
massage. Liberal professions are not members either.

**What cannot be excluded: web shops.** As in Oslo, Copenhagen and Prague, the
classification files an online seller under the goods it sells.

**Shown, but not named** - the register publishes no names at all; every dot
shows its kind of business. It also publishes no street address, so none is
shown.

**Left off because it is outside the city** - 1 business whose point lies
outside the Land of Berlin.

**Stations.** The U-Bahn and all sixteen S-Bahn lines are drawn, cut at the
Land's boundary.
- Left out: 36 S-Bahn stations in Brandenburg, where the register does not
  reach.
- Not drawn: the U6's five stations from Scharnweberstraße to Alt-Tegel,
  closed for rebuilding since November 2022 (replacement buses until about
  August 2027); the map follows the timetable.
- Trams, which run as an overlay on the U- and S-Bahn, regional trains and
  ferries are not drawn.

### London - the food hygiene register, food only

**Only food is on this map.** The Food Standards Agency's register lists the
premises boroughs inspect for food hygiene; no open register of other shops or
of personal services covers London, so clothes shops, hairdressers and the like
are missing rather than excluded. Food shops (grocers, off-licences, bakers,
butchers, newsagents selling food, supermarkets) are a category of their own.

**Excluded by type** - other catering premises (8,053), where home caterers and
event kitchens sit; mobile caterers (2,595); hospitals, childcare and care homes
(4,682); schools, colleges and universities (3,501); hotels and guest houses
(972); manufacturers and packers (1,136); distributors and transporters (669);
importers and exporters (278); farmers and growers (33).

**Not placed: flats** - 99 food storefronts registered at a flat address,
where home businesses register (the flat rule, owner 2026-09-28).

**Placed at their postcode's centre** - 2,344 food storefronts the register
gives no location but a full postcode (Ordnance Survey's postcode data).

**Not placed** - 3,000 food storefronts (5.0%) with neither a location nor a
full postcode, most in outer boroughs (23% of Redbridge's, 18% of Havering's).
A business run from a private address is published without a location or a
full postcode and is never placed.

**Shown under its trade name** - 188 businesses registered "trading as" another
name show the name on the shop.

**Left off because they are outside the city** - 19 whose location lies outside
Greater London, and 1 whose registered name holds contact details.

**Not measured: canteens.** Workplace canteens registered as restaurants or
cafés are shown; at least 2.5% of that type read as one by name.

**Stations.** The Underground's eleven lines, the DLR, the Elizabeth line and the
six London Overground lines are drawn, cut at Greater London's boundary.
- Left out: 32 stations beyond it, on the Metropolitan and Central lines, the
  Elizabeth line and the Overground.
- Eight stations missing from OpenStreetMap's route data are added from its
  station records (North Ealing, South Harrow, Woolwich Arsenal, Hatch End,
  Watford High Street, Upper Holloway, Wood Street, St James Street).
- Tramlink, National Rail services and river buses are not drawn.

### Buenos Aires - the city's land-use survey, placed at parcel centres

**Excluded by use** - car workshops, car washes and tyre repairers (3,951);
estate agents, banks, lottery agencies, bill-payment and money-transfer offices
and insurers (4,481); lawyers, printers, travel agents and copy shops (1,831);
health and veterinary practices (1,690); gyms, event halls and cultural centres
(1,353); other repair workshops (1,158); construction trades and workshops
making goods (802); party offices, places of worship and associations (658);
transport, courier and rental offices (609); schools and classes (403);
wholesalers (216); funeral homes and wake parlours (143); fortune-tellers and
astrologers (10).

**Left out because the survey cannot say** - 6,243 active shopfronts whose use
the surveyors could not identify (7.2%; 32% in Villa Riachuelo), and 593 malls,
arcades and markets, recorded as one row each with their shops not itemised.

**Homes are never shown** - 1,756 homes with a business inside are filed by the
survey as housing and excluded.

**Placed at a block's centre** - 93 whose parcel is not in the parcel layer; 3
not placed.

**Shown, but not named** - the survey records no names; each dot shows the
street address.

**Stations.** The Subte's six lines are drawn; all 89 stations lie in the city.
- Not drawn: the Premetro (18 stops in the south-west; it would add about 750
  storefronts, 1.2%, in Villa Lugano, Villa Soldati and Villa Riachuelo), the
  heritage tramway, and the commuter railways.

### Glasgow - the food hygiene register, food only

**Only food is on this map.** Glasgow City Council's entries in Scotland's Food
Hygiene Information Scheme list the premises the council inspects for food
hygiene; no open register of other shops or of personal services covers
Glasgow, so clothes shops, hairdressers and the like are missing rather than
excluded. Food shops (grocers, off-licences, bakers, butchers, newsagents
selling food, supermarkets) are a category of their own.

**Excluded by type** - mobile caterers (425); other catering premises (348),
where home caterers and event kitchens sit; hospitals, childcare and care homes
(342); schools, colleges and universities (202); manufacturers and packers
(139); hotels and guest houses (110); distributors and transporters (84);
importers and exporters (23); farmers and growers (1).

**Not placed: flats and childminders** - 185 food storefronts registered at a
flat, mostly home bakers and cooks listed as cafés (the flat rule, owner
2026-09-28), and 5 childminders listed as cafés, three under the childminder's
own name (the childminder rule, the same day).

**Not placed** - 55 food storefronts (1.2%) the register gives no location. 22
have a full postcode; they are not placed at its centre, which would add about
one storefront in two hundred at the cost of a second data source.

**Shown under its trade name** - 2 businesses registered "trading as" another
name show the name on the shop.

**Left off because they are outside the city** - 5 whose location lies outside
Glasgow City.

**Not measured: canteens.** Workplace canteens registered as restaurants or
cafés are shown; at least 1.7% of that type read as one by name.

**Stations.** The Glasgow Subway's 15 stations, all inside Glasgow City.
- Suburban and national rail (the Argyle and North Clyde lines and the rest) is
  not drawn.

### Newcastle (Regional) - the food hygiene register, food only

**Only food is on this map.** The Food Standards Agency's register lists the
premises the five Tyne and Wear councils inspect for food hygiene; no open
register of other shops or of personal services covers Tyne and Wear, so
clothes shops, hairdressers and the like are missing rather than excluded.
Food shops (grocers, off-licences, bakers, butchers, newsagents selling food,
supermarkets) are a category of their own.

**Excluded by type** - other catering premises (622), where home caterers and
event kitchens sit; mobile caterers (548); hospitals, childcare and care homes
(524); schools, colleges and universities (559); hotels and guest houses (75);
manufacturers and packers (125); distributors and transporters (78);
importers and exporters (8); farmers and growers (8).

**Not placed: flats** - 5 food storefronts registered at a flat address, where
home businesses register (the flat rule, owner 2026-09-28).

**Placed at their postcode's centre** - 634 food storefronts the register gives
no location but a full postcode (Ordnance Survey's postcode data).

**Not placed** - 489 food storefronts (7.3%) with neither a location nor a
usable full postcode, most in North Tyneside (9.7%) and Sunderland (9.2%). A
business run from a private address is published without a location or a full
postcode and is never placed.

**Shown under its trade name** - 7 businesses registered "trading as" another
name show the name on the shop.

**Left off because they are outside the area** - 2 whose register location lies
far outside Tyne and Wear (one in London, one in Lancashire).

**Not measured: canteens.** Workplace canteens registered as restaurants or
cafés are shown; at least 1.3% of that type read as one by name.

**Stations.** All 60 Tyne and Wear Metro stations, on the Green and Yellow
lines, the Sunderland branch included (owner, 2026-09-28): between Pelaw and
Sunderland it runs on track shared with national rail.
- Northern's national rail trains are not drawn.

### Sydney - the City of Sydney's floor-space survey, all three buckets

**One council, one survey year.** The City of Sydney's Floor Space and
Employment Survey counts every business establishment in the council area
every five years; the map shows the 2022 survey, the latest. The neighbouring
councils publish no comparable survey and are not on the map.

**No names.** The survey publishes an industry class and a point for each
establishment and nothing else: a dot is titled by its ANZSIC class. Points are
per building, so the shops of a shopping centre share one point (5,054 distinct
points for the storefronts, the largest holding 140).

**Excluded by class** (ANZSIC 2006, `pipeline/taxonomies/anzsic_fes.py`):
- Not storefronts: parking (72), non-store retail (14) and commission-based
  retail (1), as the NAICS cities exclude them.
- Organisations, not services sold over a counter: religious services (144),
  interest-group associations (137), business and professional associations
  (89), labour associations (23).
- The owner's calls (2026-09-28): licensed members' clubs (27, entered by
  sign-in), brothels (27), catering firms (21, the work happens at the event),
  funeral, crematorium and cemetery services (7).

**Excluded, a catch-all** - other personal services n.e.c. (254): kept at
first because the survey's rows have no names to sample, then excluded the same
day (owner, 2026-09-28) when Melbourne's census, which names them, showed the
class holds mostly consultancies in office suites.

**Kept, and named as a catch-all** - other store-based retailing n.e.c. (311).
Car and fuel retailers (64) are shops, as in the NAICS cities.

**Left off because they are outside the city** - 27 survey points that fall
just outside OpenStreetMap's outline of the council area.

**Stations.** Sydney Trains' T1, T2, T3, T4, T8 and T9 and Sydney Metro's M1,
cut at the council boundary: 16 stations inside it.
- Left out: 157 stations beyond the boundary, listed in
  `outputs/sydney/excluded_stations.csv`.
- **Light rail (L1, L2, L3; 22 stops in the area) is not drawn** (owner,
  2026-09-28); with it, about nine storefronts in ten would sit within a ring
  (93.0%, the brief's measure), against 83.4% without it.
- NSW TrainLink services and ferries are not drawn.

### Melbourne - the City of Melbourne's land-use census, all three buckets

**One council, one census year.** The City of Melbourne's Census of Land Use
and Employment records every business establishment in the council area with
its trading name; the map shows the 2024 census. The neighbouring councils
publish no comparable census and are not on the map.

**Points per property.** Every tenancy in a property shares its point, so a
shopping centre or an arcade is one point (1,840 distinct points for the
storefronts, the largest holding 219). Upper-floor and suite tenancies are
kept (434, 8.8%): the census does not say which face the street.

**Excluded by class** (ANZSIC 2006, the classes Sydney's decisions set,
`pipeline/taxonomies/anzsic_fes.py`):
- Other personal services n.e.c. (279; owner, 2026-09-28): 214 are upper-floor
  suites, mostly migration and education consultancies, with a few tattoo
  studios.
- Not storefronts: parking (146), non-store retail (17) and commission-based
  retail (1).
- Organisations: interest-group associations (161), religious services (93),
  business and professional associations (89), labour associations (33).
- The owner's calls for Sydney, applied here: catering firms (39), licensed
  members' clubs (15), brothels (9), funeral services (6).

**Kept, and named as a catch-all** - other store-based retailing n.e.c. The
census's finer classes (convenience stores; men's, women's and children's
clothing and footwear) are Retail.

**Stations.** Metro Trains' six line groups, cut at the council boundary: 17
stations inside it.
- Left out: 199 stations beyond the boundary, Richmond among them (its
  platforms' centre lies just outside, on Punt Road), listed in
  `outputs/melbourne/excluded_stations.csv`.
- **Trams (22 routes, 155 stops in the area) are not drawn** (owner,
  2026-09-28); with them, 99.1% of storefronts would sit within a ring (the
  brief's measure), against 96.0% without them.
- The event-day Flemington Racecourse line (with Showgrounds and Flemington
  Racecourse stations), the City Circle special service and V/Line are not
  drawn.

### Stockholm - the food inspection register, food only, frozen in October 2025

**Only food is on this map.** Stockholms stad's food inspection register lists
the premises its food control inspects; Sweden has no general business licence
and the city publishes no other commercial register, so clothes shops,
hairdressers and the like are missing rather than excluded. Food shops (from
kiosks to supermarkets) are a category of their own.

**Frozen.** The register holds inspections to 2025-10-21 and has not been
updated since. Each premises (8,146) is shown as it stood at its latest
inspection.

**Excluded by type** - 779 premises with no restaurant or retail type:
wholesale (300), the catch-all "Övrigt" (185, by name head offices, delivery
firms and distributors), food production (105), transport and storage (71),
water works (4), and 114 carrying two or more of these.

**Excluded by name** (owner, 2026-09-29) - 718 restaurant-typed premises that
are institutional kitchens: preschools (386), schools and gymnasia (206), care
homes, home care and day centres (78), staff canteens (11) and others such as
churches, prisons and associations (37). 12 retail-typed pharmacies.

**Excluded by name: food with no counter** (owner, 2026-09-29) - the
register's restaurant type is also its type for catering and mobile food
("Restaurang-, catering- och barverksamhet"), so these are read from the
name: 168 premises named as food trucks or mobile units, caterers, event
firms, food demonstrators or prep kitchens. 124 of them had no position,
most of them food trucks. A caterer whose name also names a restaurant,
café, bistro or bakery ("Chez Kny Bistro & Catering") stays.

**Not measured: office canteens.** About 20 staff restaurants registered under a
company name ("KPMG AB") remain; company names are too mixed to filter.

**Untyped premises** - the register began recording types in 2024, so 1,391
premises last inspected earlier carry none. **220 are shown** (owner,
2026-09-28; 225 before the caterers and mobile units above left): those whose name identifies a restaurant or food shop and that were
inspected in 2022 or 2023, marked "classified from its name". Left out: 26 such
names inspected before 2022 (likely closed), about 120 pharmacies, about 550
institutions by name, and about 470 whose name says nothing.

**Not placed** - 85 storefronts (1.6%) the register gives no position.

**Stations.** The Tunnelbana's three lines (seven routes), cut at the kommun
boundary: 82 stations inside it.
- Left out: 18 stations in Solna, Sundbyberg, Danderyd, Huddinge and Botkyrka,
  listed with their kommun in `outputs/stockholm/excluded_stations.csv`.
- Pendeltåg, Roslagsbanan, Saltsjöbanan and the trams are not drawn (owner,
  2026-09-28); with pendeltåg and the local railways, the brief measured 92.3%
  of storefronts in a ring against 88.7% without.
- The Yellow line (Gul linje), under construction, is not drawn.

### Bucharest - the sanitary-veterinary registers, food only, placed by address

**Only food is on this map.** DSVSA București registers the units that
handle food; Romania publishes no open register of other shops or of personal
services, so clothes shops, hairdressers and the like are missing rather than
excluded. Food shops (butchers, fishmongers, bakeries, confectioners, food
shops, supermarkets) are a category of their own.

**Cancelled registrations** - 10,316 rows below the files' ANULATE rows are
never read; 23,113 active rows are.

**Never fetched, by the owner's call (2026-09-28)** - canteens (file 21),
pastry labs (22), catering (31), local producers, internet-only sales, mobile
stalls, vending machines, warehouses, fairs, and the farm and processing
categories.

**Excluded within the files used** - 75 mobile units (Sector "U.M.", a food
truck with a number plate for an address); and by category, the owner's
exclusions applied to rows filed elsewhere: 13 in-house buffets ("bufet de
incintă", a canteen), 1 catering-only unit, 3 pastry labs, 8 kiosk carts and 2
vending machines.

**Merged** - one premises registered in several files (a supermarket's
butcher, fishmonger and food counter) is shown once: 23,014 rows are 20,821
premises.

**Names withheld** - a sole trader (II, PFA, IF, PF: 308) and a company named
only as a person (6) are shown by category, never by name (the owner's rules,
2026-09-28 and 2026-09-29). Other companies show their name without the legal
form.

**Not placed** - 5,228 premises (25.1%): the register gives an address but no
position, and each is placed by matching its street and number to
OpenStreetMap's address points in its own sector. Left off rather than guessed:
the street not found (1,855), the street without that number (1,726), the
number in two or more places (1,288), no number given (365). Even across the
sectors (73-76% placed); lowest for fishmongers (50%), many inside markets.

**Stations.** Metrorex M1-M5, 64 stations, every one inside the municipality.
- Suburban trains and trams are not drawn.

### Incheon - SEMAS's national storefront register, all three buckets

**One national register, every storefront with a point.** The Small Enterprise
and Market Service's 상가(상권)정보 (edition 2026-06-30) lists trading
storefronts across Korea with SEMAS's own three-level classification; the map
keys on its finest level (소분류), each of the 247 categories given a home
(`pipeline/taxonomies/korea_sbiz.py`, the owner's calls 2026-09-29, aligned with
`docs/category_rules.md`).

**Out by category** (Incheon's 136,995 rows):
- Not storefronts in this project's sense, whole groups: professional and
  technical offices (12,244), education (9,681), estate agents (5,569), lodging
  (3,423), health care (3,702), facility services and rentals (5,719),
  recreation (6,996: gyms, karaoke rooms, PC rooms, lottery sellers), repairs
  (vehicle, appliance, clothing), funeral services, wedding halls and
  matchmaking (5,205 in all within 수리·개인).
- Named: hostess bars (일반 유흥 주점, 1,010) and dance halls (53), staff
  canteens (612), household fuel dealers (110).

**Kept, and named here because other registers differ**: massage (commercial,
as in every other country), petrol and LPG stations, pharmacies, pubs.

**Names withheld** - 107 storefronts whose registered name is a bare personal
name at an address that reads residential (Seoul's rule).

**Placement** - every storefront sits at the register's own point.

**Stations.** Incheon Lines 1 and 2, Line 1, Line 7 and the Suin-Bundang Line:
79 stations inside Incheon.
- Left out: 151 stations of those lines in Seoul and Gyeonggi, listed in
  `outputs/incheon/excluded_stations.csv`; the lines are drawn to their ends.
- AREX, the suspended airport maglev and the Wolmi Sea Train are not drawn.

### Goyang, Seongnam and Yongin - SEMAS's national storefront register, all three buckets

**Incheon's source and rules** (the section above): SEMAS's 상가(상권)정보,
edition 2026-06-30, every storefront on its own point, classified by
`pipeline/taxonomies/korea_sbiz.py` and aligned with `docs/category_rules.md`.

**Out by name**, per city (Goyang / Seongnam / Yongin): hostess bars (110 /
273 / 188), dance halls (8 / 21 / 4), staff canteens (48 / 138 / 161),
household fuel dealers (24 / 16 / 65); and, as in Incheon, offices,
education, health, estate agents, lodging, recreation, repairs, funeral
services, wedding halls and matchmaking.

**Names withheld** - 9 / 30 / 16 storefronts whose registered name is a bare
personal name at an address that reads residential.

**Stations**, each city cut at its own boundary (the lines drawn to their
ends; stations outside in each city's `excluded_stations.csv`):
- Goyang: Line 3 and the Gyeongui-Jungang Line, 20 stations. The Seohae Line
  (on the Gyeongui-Jungang track through the same stations) and GTX-A (its
  Kintex stop) are not drawn.
- Seongnam: Line 8, the Suin-Bundang, Shinbundang and Gyeonggang Lines, 18
  stations. GTX-A is not drawn.
- Yongin: the EverLine, the Suin-Bundang and Shinbundang Lines, 24 stations.
  GTX-A (its Guseong stop) is not drawn.

## Kept, and why

- **Miscellaneous retail (NAICS 459999).** Another catch-all, but a sample found
  roughly 70% were plausible walk-in shops — niche independent retailers with no
  more specific code. Excluding it would lose real storefronts.
- **Businesses trading under a person's name.** A hairdresser or tailor whose
  shop is called after them is a genuine storefront, and the name is a trade
  name they chose to register publicly. Roughly a fifth of mapped names read
  like personal names for exactly this reason, and that is not a problem to fix.
- **San Diego's personal services, apart from its catch-alls.** Its registry
  always carries a trade name, so no registrant name was ever substituted. The
  two catch-all codes were left in on that ground until 2026-09-29, when the
  catch-all left every map.

## What is missing rather than excluded



Some things on this map are absent for a different reason, and they are worth
separating from everything above. Every exclusion so far was a choice. In **New
York**, **Philadelphia** and **Boston**, some of what is missing was never
available to choose.

Because the city has no general business licence, a shop is only in this map if
some regulator happens to license it. Restaurants are inspected, so they are
close to completely covered. Grocers, bodegas and delis hold state food store
licences, so they are covered. Salons and barbers hold state licences, so they
are covered. But a clothing shop, a bookshop, a hardware store or a florist
needs no licence from any of these four registries, and so does not appear at
all.

The practical effect is that New York's Retail category is thinner than its
Food service one, and thinner than Retail in the cities whose registries cover
all trades. **Read the balance between categories in
New York as a fact about the city's licensing, not about its high streets.**

**Vancouver loses about half its register to missing coordinates, and no
geocoder exists to recover it.** Of 58,346 current-year Issued licences, only
29,660 carry coordinates. Most of the remainder is categories excluded anyway -
long-term and short-term rentals, general and trade contractors, consulting,
which between them account for 20,915 of the unmappable rows - but **1,583 rows
have a real street address and no coordinates**, and they are simply absent.
There is no Canadian equivalent of the US Census bulk geocoder, which is what
recovers those rows in Los Angeles and Washington D.C. Vancouver does publish a
`property-addresses` layer that could serve the same purpose, but it has never
been match-tested, so the loss is recorded rather than quietly closed. A row
missing coordinates is not automatically a row needing geocoding.

**Surrey's four stations reach much less of their city than Vancouver's twenty
do**, and that is geography rather than data. 15% of Surrey's storefronts fall
within the outer ring, against 51% in Vancouver, because Surrey's commerce sits
along arterial roads the SkyTrain does not follow. Read the two cities on that
map as two measurements sharing a frame, not one continuous surface.

**Philadelphia is the same problem one step further: a whole category is
missing.** New York's four registries at least covered all three — its Retail
was thin, not absent. Philadelphia licenses no personal-service business of any
kind. There is no salon, barber, nail, cosmetology, massage or laundry licence
in the city's register, and Pennsylvania publishes its cosmetology licensees
only as **county totals with no addresses**, while the State Board's
verification system answers one licence at a time with no bulk export. Every
alternative was checked live and each failed for a different reason; they are
listed in `data_sources.md` so the search is not repeated from scratch.

So **Philadelphia's map has two categories, not three, and Personal services is
absent entirely.** Its Retail is narrow for New York's reason as well: what the
city licenses is *food* retail, so Retail there means bodegas, mini-markets and
beer distributors, plus a big-box tier (Target, CVS, Dollar Tree, Ross) that
appears only because those stores also sell packaged food. Pavement newsstands
are largely absent too — the register holds neither a coordinate nor a street
address for 60 of the 75 licensed. None of this is a choice this project made,
and the city page says so on its face rather than leaving a reader to infer
something about Philadelphia's high streets from a fact about its licensing.

**Boston is Philadelphia's case again, for the same structural reason and in
a narrower form.** It licenses food and alcohol and essentially no other
trade, so its map has two categories rather than three and Personal services
is absent entirely. The cause is identical: Massachusetts licenses cosmetology
and barbering at **state** level, through the Board of Registration of
Cosmetology and Barbering, whose register is a per-licence ePLACE/MADOL lookup
with no bulk export and no addresses. That was verified three independent ways
rather than assumed - Socrata's cross-domain discovery API returns no
Massachusetts source for cosmetology, barber, salon, hair, nail salon, body art
or tattoo; `data.mass.gov` is not a data portal at all, answering HTML 404 from
both the Socrata and CKAN entry points; and `opendata.mass.gov` does not
resolve.

Boston's Retail is narrower still than Philadelphia's. What exists is retail
**food** (groceries, convenience stores, bodegas), package stores and cannabis
dispensaries - so a clothes shop, a bookshop or a hardware store is absent for
New York's reason on top of Philadelphia's. The honest description of Boston's
map is **food-and-drink density with a retail-food edge**, not commercial
density, and its city page leads with that rather than burying it.

One source could have changed this and was deliberately not used. Boston's
`Business Inventory` is a summer-2025 field survey carrying exactly this
project's three buckets - 243 beauty services among them, plus clothing,
jewellery and tailoring. Its own notes give the reason it cannot be used: it
covers "every storefront in downtown Boston, as well as comprehensive data on
3 major commercial corridors in Mattapan, Jamaica Plain, and Allston", which is
37 grid cells of a city. A density surface built on a partial survey shows
where surveyors walked rather than where commerce is, and mixing it in would
have made four neighbourhoods read as three-bucket and the rest as two. It is
recorded in `data_sources.md` as available and unused, with the trigger for
revisiting it: a city-wide survey.


**Toronto's general retail is ABSENT, and it is the most severe coverage gap
on the site.** Everything else on this page was a choice; this was not.

Toronto licenses food and trades, and not general retail. There is no licence
category for a grocer, a clothing shop, a pharmacy, a hardware store or general
merchandise, so none of them exists in any register to map. What the Retail
bucket holds instead is the **regulated slice alone** - the trades a city
licenses because it wants to watch them: `VAPOUR PRODUCT RETAILER` (351),
`SECOND HAND SHOP` (219), `PRECIOUS METAL SHOP` (85), `PAWN SHOP` (41),
`SMOKE SHOP` (28), `PET SHOP` (20), `SECOND HAND SALVAGE SHOP` (10) and
`PERMANENT FIREWORKS VENDOR` (5).

Of the licences that reach the map, **759 of 18,186 (4.2%) are retail**,
against 13,385 food service and 4,042 personal services. So
**read Toronto's Retail layer as a narrow regulated slice of what is actually
on the street, and the balance between its three categories as a fact about
Toronto's licensing rather than about its high streets.** This is
`multi-source-city`'s "Retail - regulated slice" archetype, and unlike New York -
whose four registries at least covered all three buckets thinly - there is no
second source at any level of government that would fill Toronto's gap.

**The bucket is drawn rather than omitted**, decided by the owner on
2026-09-21. The rejected alternative was leaving Retail out and drawing two
buckets: it reads as a stronger statement but discards 870 real storefronts and
would have made Toronto's legend the odd one out among the fourteen cities
built by then. New York's page is the model for the disclosure.

**Toronto also loses about one storefront in sixteen to geocoding, and the loss
is NOT spread by district.** Its register carries no coordinates at all, so
every pin was placed by matching its address against the City's One Address
Repository - 93.8% matched. The missing 6.2% concentrates on plaza and mall
addresses the repository does not carry as a single string (`1571 SANDHURST
CIR`, 44 rows; `8 WESTMORE DR`, 25), so a handful of shopping centres are
under-counted rather than any district being missed. Checked on the axis that
would distort the map: across the wards holding at least 200 storefront rows
the match rate runs 75.4% to 99.3%, a **1.3x spread** with a standard deviation
of 5.7 points.

## Honest limits

- Whether a name belongs to a person is judged by pattern, not verified. The
  test spots "Jane Smith" and misses "J Smith Consulting", and it cannot
  distinguish a sole trader legitimately named after themselves from a
  registrant sitting at home. **Vancouver is one of the exceptions, where the
  registry answers this itself** - as D.C.'s entity type and the French
  register's legal form also do - and it answers in the name field: it wraps a
  sole proprietor's own name in PARENTHESES - "(Qi Liu)" - so the primary
  signal there is the City's own marking rather than a guess. The pattern test is still run alongside it,
  because each catches people the other misses: the parentheses find 63
  storefront rows the pattern misses, mostly three-part and non-Anglo names,
  and the pattern finds about 10 registrants who did not use parentheses.
  **88 pins across Vancouver and Surrey display their business type instead of
  a name.** No pin shows a name the pipeline substituted for a missing trade
  name.
- **Vancouver's residence filter finds nothing, and that is a measurement
  rather than a gap.** Its two-hop parcel join (business point to parcel to the
  tax roll's zoning) places 99.9% of points and reaches a zoning class for
  99.7%, but the pairing it exists for - residential zoning AND a substituted
  personal name - leaves **one row**, and that row is a false positive: a real
  corner grocery whose name reads as a surname plus a word. Zoning alone is
  deliberately NOT used, because the 146 residentially-zoned storefronts there
  are Restaurant 32, Limited Service Food 29, Retail Dealer 23 and so on -
  Vancouver's legal non-conforming corner shops and neighbourhood restaurants,
  which a zoning filter would delete wholesale. The join is kept because it is
  what justifies not filtering.
- **Vancouver's unit designators cannot indicate a residence at all**, so the
  usual APT/UNIT proxy must not be read there. The city uses "Unit" generically
  for commercial suites: 12,803 of 29,660 mappable rows say `Unit` against
  **two** that say `Apt`. `scripts/check_personal_exposure.py` therefore
  reports a 6.73% "person-like name at a residential unit" figure for Vancouver
  that is an artifact of the city's conventions - San Diego's measurement gap
  inverted, a false high rather than a false low. The zoning measure above is
  the one its verdict rests on.
- A residential address is inferred from indicators like "APT" or a space
  number. It is a proxy. In San Diego it cannot be measured at all: that
  registry stores unit values as bare numbers with no label, so the text gives
  nothing to match. New York is the one city where it can be measured properly,
  because its licence data records the unit type as its own field.
- In New York, where a business appears in two of the four registries it is
  counted once, matched on address and name. Two registries spelling the same
  name differently will leave it counted twice. That was the deliberate choice:
  one New York address often holds many separate shops, so merging on address
  alone would have deleted real businesses.
- A small residual remains in Los Angeles and San Francisco, spread thinly
  across ordinary storefront categories rather than concentrated in one.
- No individual business record was checked against any other source, and
  nobody was contacted.
- **Contact details are removed, not displayed.** A registry's business-name
  field occasionally holds an email address or phone number instead of a trade
  name. Any such row is dropped from every map, because it has no usable public
  name and an email address is a direct line to a person rather than a
  description of a business. This is enforced once in the shared renderer, so
  it applies to every city including ones added later. Three rows in New York
  were removed this way on 2026-09-21, and one in Monterrey on 2026-09-27.
- **Where a registry records a licence holder and a trading name in one field,
  the trading name is what is shown.** Philadelphia formats these as "LEGAL
  NAME (TRADE NAME)", so 456 pins that would have displayed a licence holder's
  own name now show the name above the shop instead. A person trading under
  their own name with no trading name recorded is still shown as they
  registered.
- These decisions concern what is *appropriate* to publish. What each dataset's
  licence *permits* is a separate question and is still open.

## If you believe a listing should not be here

Every business shown is drawn from a public municipal registry and is displayed
with its registered name and address location only. If you are the owner of a
listing and would like it removed, that is a reasonable request and it will be
honoured.

**You do not have to give a reason, and the request will not be argued.** The
listing comes down first; anything else is a separate conversation. The same
applies if you are not the owner but believe a particular pin identifies a
person rather than a business — raise it and it will be treated as a removal
request, not as a question to be debated first.

The same commitment is made to the agencies whose data this project uses: if a
publisher asks for its data to stop being displayed, it stops. That is written
out in full in `data_sources.md`, under "Commitment: removal requests are
honoured, not argued".

**And a city can come off for a reason nobody raised.** One city's terms
are unresolved, and it is Philadelphia. The dataset page there binds a reader
to the City's separate Terms of Use, which let residents print single pages of
the City's website and otherwise prohibit "distribution or republication in
any other form or for any other purpose ... and any modification whatsoever"
without the City's written permission. Applied to a dataset, that would not
permit this map, which filters and redraws what it publishes; read as terms
written for web pages - sitting beside a dataset licence containing no such
prohibition, under an Open Data Program meant for public reuse - it would.
**That has not been resolved in this project's favour, and if the City
confirms the restrictive reading, Philadelphia is removed without waiting for
a request.** The same statement appears in the footer of every page.

Two sibling questions were investigated at the same time and closed, which is
worth recording because both had been assumed to be the same shape:
**SEPTA** expressly licenses its datasets for use, reproduction and
redistribution, and claims only its Logo as a trademark - not line names, not
route colours. **Miami-Dade County** does publish a Terms of Use for its Open
Data Hub, contrary to an earlier note here that no document existed; it
contains an accuracy disclaimer and nothing about reuse, as do the dataset's
own licence field and the county-wide user agreement.
