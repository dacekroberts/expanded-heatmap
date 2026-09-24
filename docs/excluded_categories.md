# What this map leaves out, and why

This project maps **storefront** commercial density around rapid-transit
stations: the kind of business you might walk into on your way from a station.

That sentence holds two separate scoping decisions, and this page is both of
them — **which stations** a map is drawn around, and **which businesses** are
counted near them. Each one leaves things out on purpose. Neither is visible
from the map itself, which is why they are written down here.

It is written to be published as-is alongside the maps. Business counts are
from the 2026-09-21 rebuild; station counts are computed from the repository's
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

**Commuter rail is excluded in every city.** The ones named on the record are
BART and Caltrain in San Francisco, Metra in Chicago, Metrolink in Los Angeles,
the Coaster and Sprinter in San Diego, SEPTA's Regional Rail in Philadelphia,
the MBTA's Regional Rail in Boston, Tri-Rail in Miami, GO Transit in Toronto,
the West Coast Express in Vancouver, Cercanías in Madrid, the Passante and
Trenord's suburban services in Milan, and Iarnród Éireann's Commuter and
InterCity trains in Dublin, RER and Transilien in Paris, and the TER services
in Marseille.

**Trams are NOT excluded as a class, and the test is whether the tram is the
rapid-transit system or an overlay on one.** Many of these maps draw light rail
- San Diego, San Francisco, Los Angeles, Edmonton, Calgary, Miami and Dublin
among them - Marseille draws its three Tramway lines beside its two Métro
lines, and Toulouse draws T1 beside Métro A and B. Where a tram network is left
out, the city already has a metro and the trams run over the top of it: Milan's
17 tram routes stop a block or two apart and the agency publishes no colour for
any of them, and Barcelona's tram falls outside the network-identity test that
picks out its metro. San Francisco's F Market heritage streetcar and its cable
cars are out on that same ground rather than on any question of mode: both are
separately branded services running beside Muni Metro rather than part of it.
Toulouse's cable car is the proof that "cable car" is not itself a reason.

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
  which is a tenth of a mile in most cities and finer in New York — so
  unthinned, nearly every point in the west of San Francisco would read as
  "next to a station". Where that happens, surface stops are thinned to roughly
  one every half mile measured along the line's own route, while every
  underground station, every terminus and every interchange is kept. It applies
  to three cities: San Francisco's Muni Metro, Philadelphia's trolleys, and the
  Boston Green Line's surface branches. The reasoning is in
  `docs/sub_transit_line_filters.md`.

**A thinned stop does not leave a hole in the map.** Stops are thinned to half a
mile apart and the outermost ring reaches 0.6 miles, so the stations that were
kept still cover the ground between them. A station left out for being in
another city is different: there the businesses are outside the register too,
which is the honest limit of a map built from one city's own data.

## Which businesses are counted

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

A national catch-all code. An earlier sample of this code found roughly 90% of
it was not storefront at all: people working from home, professional offices,
and services that travel to the customer. Los Angeles's own data matched that
pattern, and the code supplied most of the map's personal names at residential
addresses.

It was a large exclusion: 31% of the city's otherwise-qualifying businesses.
Los Angeles is unusual in that 68% of its registry rows carry no trade name, so
those rows displayed the registrant's own name.

### San Francisco — Solo massage establishments (NAICS 812990)

The same code number, but San Francisco's licence data labels it "solo massage
establishment" rather than the generic name, so it is a different decision. Of
414 mapped businesses in this category, 31 carried a person-like name at an
address with a residential indicator — the highest share of any category in the
city. A sole practitioner working from home is a sensitive thing to place on a
public map, and the category is a small part of the total, so it is excluded.

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
chance; and handbill distribution. A business holding several licences is
counted once, so a restaurant with pavement seating appears as a restaurant
rather than twice.

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
city here.

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
subtype to separate them.

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
headcount-banded `Real Estate` types are the same shape. Also excluded, as in
every city here: `Long-term Rental` (3,451 in Vancouver - the Philadelphia
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
- **A funeral parlour counts; a cemetery does not.** Both are NAICS 812, so the
  prefix alone would keep both. Surrey's `Funeral Parlour` (4) is a walk-in
  commercial premises; `Cemetery` (2) is land. A deliberate departure from the
  prefix, on storefront grounds.
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
actual trade wins, and mail order is nonstore.

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
(6) and cultivation (3), event production (3), carnivals (2) and one
after-hours dance club that holds no alcohol category.

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
`BILLIARD HALL` 177, `ENTERTAINMENT ESTABLISHMENT/NIGHTCLUB` 170 - merged and
leading with entertainment, so the same treatment as Edmonton's after-hours
dance club - `THEATRE` 73, `BOWLING HOUSE` 38, `CARNIVAL` 16, `CIRCUS` 5,
`SWIMMING POOL` 3), `PAYDAY LOAN` (187, NAICS 522291), `SECOND HAND SALVAGE
YARD` (68, a yard rather than a shop), `AUCTIONEER` (251) and `COLLECTOR OF
SECOND HAND GOODS` (66) as people rather than premises, `SHORT TERM RENTAL
COMPANY` (5, NAICS 721), and `** Class record not on file. (138)` (4), which is
the register's own placeholder.

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

**Not excluded but absent by construction: 811 repair and 813 associations.**
Personal services is anchored on **812**, not the whole of 81, so auto repair
(27,216 units in Jalisco, the largest block inside 81) and civic, religious and
professional associations never enter. Food service is anchored on **722**, not
72, so 721 accommodation — hotels — never enters either. Both are the same
precision the NAICS cities use; a two-digit prefix would have been the
obvious-looking mistake.

**The whole-city heat layer is OFF for this city**, as it is for Guadalajara,
built from the same census. Most cities here offer an opt-in layer showing all
of their businesses, not only those within a station ring. Mexico City's would
carry 283,345 points against 133,362 in the default layer, and dropping it cut
the rendered file from 25.7 MB to 19.0 MB. So the map shows density **around
stations** and does not offer the whole-city comparison most other cities do.

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

**Tonalá is excluded, and it is the only whole municipio this project has left
out of a region it could have included.** DENUE holds **19,897** economic units
there and they are already downloaded - entidad 14 is the whole of Jalisco. No
Tren Ligero line reaches Tonalá, and a municipio with no station contributes
businesses that no ring can ever contain, so including it would have inflated
the city total while changing no ring. The four municipios kept -
Guadalajara, Zapopan, San Pedro Tlaquepaque and Tlajomulco de Zúñiga - are the
ones SITEUR's own line descriptions name.

**The whole-city heat layer is OFF, as Mexico City's is.** The rings and the
three categories toggle from the layer control; there is no option to show
every business in the region at once.

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

### Madrid - accommodation, trades with no shopfront, and a zero where a location should be

**Hotels and tourist flats are excluded** - accommodation rather than food
service, the same carve-out Barcelona needs and for the same reason. So are
wholesale, vehicle repair, and premises with no shopfront at all, such as
online and vending sales. The three categories are the register's own activity
classification, not NAICS.

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

### Dublin - a register of premises rather than of businesses

**Nothing here is excluded on the basis of what a business is called, because
no name is published at all.** Tailte Éireann's rateable valuation register
records *premises* rather than occupiers: no trade name, no occupier, no owner.
Each pin shows the address a valuation is filed against and the use recorded
against it. This is the only city on the site that names no businesses, and the
only one where the personal-name question does not arise.

**Where a premises carries more than one use, the more specific trading use is
what it is counted as** - a shop with offices above it is a shop, a salon
behind a shopfront is a salon. A premises whose recorded uses are none of
retail, food service or personal service is not on the map.

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
laundry, and the same two catch-alls `96.09Z` and `56.29B`. The catch-all
verdict was re-measured rather than inherited: the two cities' compositions
differ, which is why the shares were counted for Marseille instead of Paris's
being assumed.

**The gap against OpenStreetMap is wider here - about 2.6 times as many points
- and most of that is not the register.** OpenStreetMap covers Marseille far
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
wholesale laundry, and the same two catch-alls `96.09Z` and `56.29B`. The
verdict was measured a third time rather than inherited, and this is the city
that shows why that is not ceremony: `96.09Z` is **13.9%** of Toulouse's bucket
rows against roughly 9.7% in both Paris and Marseille. The national argument
transfers; the shares plainly do not.

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
four no-premises trades, the wholesale laundry, and the two catch-alls
`96.09Z` and `56.29B`. They were measured again rather than inherited:
`96.09Z` is 11.2% here, between Marseille and Toulouse.

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
four no-premises trades, the wholesale laundry, and the two catch-alls `96.09Z`
and `56.29B`. They were measured again rather than inherited: `96.09Z` is 14.0%
here, level with Toulouse, and its rows show the same sign of sole traders
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

## Kept, and why

- **Miscellaneous retail (NAICS 459999).** Another catch-all, but a sample found
  roughly 70% were plausible walk-in shops — niche independent retailers with no
  more specific code. Excluding it would lose real storefronts.
- **Businesses trading under a person's name.** A hairdresser or tailor whose
  shop is called after them is a genuine storefront, and the name is a trade
  name they chose to register publicly. Roughly a fifth of mapped names read
  like personal names for exactly this reason, and that is not a problem to fix.
- **San Diego's personal services.** San Diego shows no comparable exposure: its
  registry always carries a trade name, so no registrant name was ever
  substituted. Its residual is small and it was left in.

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
Food service one, and thinner than Retail in the other four cities, which draw
on registries that cover all trades. **Read the balance between categories in
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
licenses because it wants to watch them: `SECOND HAND SHOP` (1,806),
`VAPOUR PRODUCT RETAILER` (539), `PRECIOUS METAL SHOP` (413), `SMOKE SHOP`
(317), `PAWN SHOP` (218), `PET SHOP` (118), `SECOND HAND SALVAGE SHOP` (33) and
`PERMANENT FIREWORKS VENDOR` (31).

On the current licences that reach the map that is **870 of 19,575 storefront
rows, 4.4%**, against 14,408 food service and 4,297 personal services. So
**read Toronto's Retail layer as a narrow regulated slice of what is actually
on the street, and the balance between its three categories as a fact about
Toronto's licensing rather than about its high streets.** This is
`multi-source-city`'s "Retail - regulated slice" archetype, and unlike New York
- whose four registries at least covered all three buckets thinly - there is no
second source at any level of government that would fill Toronto's gap.

**The bucket is drawn rather than omitted**, decided by the owner on
2026-09-21. The rejected alternative was leaving Retail out and drawing two
buckets: it reads as a stronger statement but discards 870 real storefronts and
would make Toronto the only city on the site whose legend differs from the
other thirteen. New York's page is the model for the disclosure.

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
  were removed this way on 2026-09-21; no other city had any.
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
