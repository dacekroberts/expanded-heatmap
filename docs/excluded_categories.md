# What this map leaves out, and why

This project maps **storefront** commercial density around rail-transit
stations: the kind of business you might walk into on your way from a station.
Business registries are broader than that, so some registered businesses are
deliberately excluded. This page lists every exclusion and the reason for it.

It is written to be published as-is alongside the maps. Counts are from the
2026-09-21 rebuild; the reasoning behind each decision, with sample sizes, is in
`DECISIONS.md`.

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

### Chicago — non-storefront licence types

Chicago classifies by licence type rather than NAICS, so its exclusions are
named differently but follow the same rule. Left out: home-based businesses
(the city marks these explicitly), peddlers and mobile vendors, temporary and
pop-up trading, shared kitchens, wholesale, parking operators, vehicle repair,
amusements, child care, and licences that merely attach to a business already
counted (an outdoor-patio or late-hour permit, for instance). A business holding
several licences is counted once.

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

## Honest limits

- Whether a name belongs to a person is judged by pattern, not verified. The
  test spots "Jane Smith" and misses "J Smith Consulting", and it cannot
  distinguish a sole trader legitimately named after themselves from a
  registrant sitting at home.
- A residential address is inferred from indicators like "APT" or a space
  number. It is a proxy. In San Diego it cannot be measured at all: that
  registry stores unit values as bare numbers with no label, so the text gives
  nothing to match.
- A small residual remains in Los Angeles and San Francisco, spread thinly
  across ordinary storefront categories rather than concentrated in one.
- No individual business record was checked against any other source, and
  nobody was contacted.
- These decisions concern what is *appropriate* to publish. What each dataset's
  licence *permits* is a separate question and is still open.

## If you believe a listing should not be here

Every business shown is drawn from a public municipal registry and is displayed
with its registered name and address location only. If you are the owner of a
listing and would like it removed, that is a reasonable request and it will be
honoured.
