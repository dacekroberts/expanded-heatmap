# What this map leaves out, and why

This project maps **storefront** commercial density around rail-transit
stations: the kind of business you might walk into on your way from a station.
Business registries are broader than that, so some registered businesses are
deliberately excluded. This page lists every exclusion and the reason for it.

It is written to be published as-is alongside the maps. Counts are from the
2026-09-21 rebuild; the reasoning behind each decision, with sample sizes, is in
`DECISIONS.md`. Where each city's data comes from is in `data_sources.md`.

Two principles run through all of it:

1. **Storefront means storefront.** A business you cannot walk into does not
   answer the question this map asks, however legitimately it is registered.
2. **Publish public commercial information, not personal information.** A trade
   name someone chose for their shop is commercial and deliberately public. A
   registrant's own name at what appears to be their home is not, even though
   the registry holding it is public.

Those two overlap more than you would expect: the categories that are not
really storefronts are the same ones full of people running a business from
home under their own name. Fixing the first mostly fixed the second.

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

## Honest limits

- Whether a name belongs to a person is judged by pattern, not verified. The
  test spots "Jane Smith" and misses "J Smith Consulting", and it cannot
  distinguish a sole trader legitimately named after themselves from a
  registrant sitting at home.
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
