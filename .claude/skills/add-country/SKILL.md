---
name: add-country
description: Profile a whole country before screening any of its cities - does it license businesses municipally, publish open portals, run urban rail, carve personal information out of its licences, and have a geocoder. Use when the task is "can we add <country>" or "what other countries could this project cover", or before the first city in a country this project has never built in. Not for adding a city in a country already profiled - that is add-city.
---

# Profiling a country before screening its cities

Distilled from Canada, the first country profiled this way (2026-09-21), which
took 13 candidate cities down to 6 viable ones. Read `add-city` first: this
sits **above** its Step 0, not inside it.

**Why country-level first.** A city screen re-derives the same national facts
every time - the licence template, the privacy statute, whether a geocoder
exists, whether business registration is municipal at all. Those are per
*country*, and some of them disqualify every city at once. Canada's screen
cost roughly a day and covered six cities; the per-city marginal cost
afterwards is small because the licences rhyme, the privacy regime is shared,
and the portal software repeats.

**This argues for depth per country over breadth across countries.** Five
cities in one country is cheaper than five countries with one city each.

## Run the questions in this order - cheapest disqualifier first

Each one can end the profile. Do not research business data before rail.

### 1. Does urban rail exist, in a feed you can read?

`scripts/screen_rail.py` against the Mobility Database catalogue
(`bit.ly/catalogs-csv`). **In Canada this removed 6 of 13 cities before a
single data catalogue was opened**, which is the whole argument for the
ordering.

Commuter rail (`route_type 2`) is not urban rail here, matching every built
city. A country whose only rail is intercity is out.

### 2. Does the country license businesses MUNICIPALLY, and publish it?

This is the biggest structural discriminator and it splits the world unevenly.
North America and Australia: yes. Much of Europe: business registration is
national, and address-level openness varies enormously.

A country where registration is national but *open with addresses* (France's
SIRENE is the candidate) is a different and possibly better shape - one source
covering every city - but it is **not** the shape this project is built for,
and the taxonomy and scoping would need rethinking rather than copying.

### 3. What portal software, and does it refuse automated fetches?

Canada used **all four** of CKAN, Socrata, Opendatasoft and ArcGIS Hub. The
existing fetch code speaks all four, so this is usually cheap - but check for
refusals early, because they are silent:

| Portal | What bit |
|---|---|
| `donnees.montreal.ca` | `RBAC: access denied` to plain curl; browser headers work |
| ArcGIS Hub (Surrey) | `/csv` returns **HTTP 202** with an async job, CSV on a later call |
| Toronto CKAN | `datastore_search_sql` **404s**; use `datastore_search` with `filters` |
| Opendatasoft | CSV exports are **semicolon-delimited**, not comma |

### 4. How does the country define PERSONAL INFORMATION, and does its licence carve it out?

**Do this before any city's privacy work, because the answer may be a licence
condition rather than a policy choice.** Every Canadian Open Government Licence
excludes Personal Information from the grant and defines it by pointing at the
province's own statute - so the carve-out cannot be read without the statute,
and **the provinces did not agree with each other**.

What to establish:

- Is information about an individual **in a business capacity** excluded from
  the definition? (Ontario: yes, explicitly, *even when the business is run
  from a dwelling*. BC: yes for "an individual **at a place of business**",
  which does not clearly reach a dwelling. Québec: **no** - it narrows the
  Act's reach rather than excluding the information, and frames the exemption
  around "une fonction au sein d'une entreprise", which does not obviously
  cover a sole trader who *is* the business.)
- Is the regulator's interpretation published? Ontario's IPC bulletin is
  stored in `docs/licenses/` because it is load-bearing.

**Expect to be wrong here.** An early reading during the Canada profile
concluded that publishing a sole trader's name would breach the licence. The
statute says the opposite for Ontario. Read the definition, never infer it
from the carve-out.

### 5. Is there a residence / owner-occupancy signal, and where does it live?

Every US city in this project infers "is this someone's home?" from a parcel
join - assessor land use plus an owner-occupancy or homestead flag. **That
chain does not exist in Canada: no province publishes owner-occupancy.** BC
Assessment is not open data.

Canada compensates with something **more direct, at the licence level**:

- Surrey: `LicenseType = 'Home Occupation'` (14,015 of 27,082)
- Edmonton: `business_address = '<Home Based Business>'` (and those rows carry
  no coordinates, so they cannot be mapped at all)
- Calgary: `homeoccind`
- Vancouver: **nothing** - the only one needing the US-style parcel join

So ask: *does the licensing authority state that a business is home-based?*
That is better evidence than a parcel inference, because the city asserts it.
If not, find the zoning/assessment layer and plan a **spatial** join.

### 6. Is there a national geocoder, or must it be per-city?

The US Census bulk geocoder is free, national and keyless. **There is no
Canadian equivalent**, and that sounds like a blocker until you check what
actually needs geocoding:

| City | Coordinates | Real address, none | Needed? |
|---|---|---|---|
| Montréal, Surrey, Calgary | 100% | 0 | No |
| Edmonton | 53.3% | **111** | No - the rest are placeholders |
| Vancouver | 50.8% | **1,583** | Marginal |
| Toronto | **0%** | 159,872 | **Yes** |

Only one city of six genuinely needed it, and the answer was not a geocoder:
**join against the city's own address-point layer.** Toronto's One Address
Repository (525,440 points, same licence as the business data) matched **71.4%
on exact string match** with no street normalisation, and returns
`MUNICIPALITY_NAME`, so it doubles as the in-city filter.

**A row missing coordinates is not automatically a row needing geocoding.** It
may have no address either - Edmonton's placeholders, Vancouver's rentals and
contractors.

### 7. What classification standard, and is the field single-valued?

Canada uses NAICS (it is a trilateral US/Canada/Mexico standard, so
`pipeline/taxonomies/naics.py` may transfer unchanged - Montréal's `SCIAN` is
NAICS in French, populated on 99.6%). Municipal licence registers mostly use
local taxonomies instead, which the per-city module pattern already handles.

**The trap that is not in the US playbook: three of six Canadian registers
store SEVERAL categories per row, each with a different delimiter.**

| City | Naive distinct | Delimiter | True distinct |
|---|---|---|---|
| Calgary | 1,169 | `,\n` | **173** |
| Edmonton | 1,534 | `;` | **67** |
| Surrey | 628 | `\n` | **210** |

A `value_counts()` on the raw column returns *combinations*. A taxonomy module
built on 1,169 Calgary "categories" would be nonsense. Split first, then a
multi-licence premises needs a dispatch rule - Boston's `FT+RF` question again.

### 8. Language and encoding

- **Declare `SOURCE_ENCODING` per city** (already an `add-city` requirement).
  All six Canadian sources are UTF-8; Québec data is often `latin-1`.
- **Mojibake in a terminal is usually the console codepage, not the file.**
  Set `PYTHONIOENCODING=utf-8` before blaming the data.
- **Column names in another language are already solved** - each city's config
  names its own columns and step 2 renames to the taxonomy's `VALUE_COLUMN`.
  `NOM_ETAB` is no harder than `dbaname`.
- **Category labels belong to the taxonomy module**, which the project's own
  invariant already makes the single owner of tooltip and legend text. Decide
  there whether to translate; prefer English bucket labels with the source
  value in the tooltip, so cross-city comparison survives without hiding the
  source.
- **Business names stay in their own language, always.**
- **Search the catalogue in the local vocabulary.** Montréal was almost ruled
  out because `locaux-commerciaux` - a 28,621-premises survey that is the best
  source in the project - contains none of the words *business*, *licence*,
  *permis*, *entreprise* or *commerce*. Which is why `add-city` Step 0 now
  requires reading the whole catalogue rather than grepping it.

## How a country's cities differ from the US ones

Carry this table into the first build; it is what actually changed.

| | US pattern | Canada |
|---|---|---|
| Licence regime | Heterogeneous - PDDL through to MTA forbidding modification | **One OGL template**, 4 of 6 near-identical |
| Attribution | Varies; several require none | **Prescribed wording**, 5 of 6 |
| Breach | Usually unspecified | **Automatic termination** in 3 of 4 OGLs |
| Personal information | Project chose its own line | **Carved out of the licence grant** |
| Home signal | Inferred: parcel land use + owner-occupancy | **Stated on the licence** |
| Owner-occupancy data | Open (assessor rolls) | **Not open anywhere** |
| Geocoding | Census bulk geocoder, national | **None** - city address points |
| Classification | NAICS usually | Local, and often **multi-valued** |
| Coordinate quality | LA had ~9% corrupt | **99.8-100% clean** in all six |
| Transit licence | The loosest end of every review | Mostly the city's own OGL |

## What to produce

1. **`docs/<country>_step0_endpoints.md`** - every endpoint fetched, per leg
   (business, transit, boundary), with the traps. Merge into
   `docs/data_sources.md` only when a city is actually built.
2. **Licence texts in `docs/licenses/`**, one per publisher, with source URL,
   retrieval date and SHA-256 in that directory's README.
3. **A privacy note** working through each jurisdiction's definition.
4. **A required-notices file** with exact wording per city, to be promoted into
   `data_sources.md`'s numbered gate when a city is committed - not before, so
   the deploy gate stays a list of things that actually apply.
5. **A `DECISIONS.md` entry** with the ranking and its evidence.
6. **`docs/city_shortlist.md`** gains the country's section.

## Rank on station density, not on population or city count

The number that decides whether a city is worth building is **businesses within
the outermost ring per in-city station** - the measure that made D.C. strong
(~173) despite keeping only 40 of 98 stations, and Boston weak (~39).

Canada's result, and why it matters that population was not the guide:

| City | Sites/station |
|---|---|
| Vancouver | **861** |
| Surrey | 549 |
| Montréal | 252 |
| Edmonton | 153 |
| Calgary | 103 |
| **Toronto** | **41** |

**The largest city came last**, because it licenses food and trades but not
general retail - two buckets, Boston's shape. Anyone choosing on population
would have built the worst of the six first.

## Failure modes seen in one country profile

All of these produced a confidently wrong answer that survived until something
was measured. Expect them.

- **A catalogue mirror three months stale and missing an entire mode.**
  Toronto's TTC feed on the Mobility Database had no subway at all; the screen
  concluded Toronto mis-codes its subway. `screen_rail.py` now flags expiry.
- **A boundary GeoJSON declaring the wrong CRS.** Surrey's says EPSG:4326 and
  contains UTM metres; reprojecting silently puts it millions of metres away
  and every containment test returns zero.
- **Two datasets with the same name, one returning null geometry.** Calgary
  publishes two "City Boundary" layers; one is 184 bytes of valid, useless
  GeoJSON.
- **A boundary layer that is a LINE.** Vancouver's `city-boundary` is a
  MultiLineString; point-in-polygon matches nothing.
- **A boundary layer that is mostly something else.** Surrey's has 10 features,
  9 of them town centres.
- **Case-sensitive join keys.** Toronto's `ADDRESS_FULL` is title case and
  CKAN's `filters` matches exactly: uppercase matched 0 of 150.
- **A dataset named in a vocabulary you did not search.** Edmonton's boundary
  is a *corporate* boundary; Montréal's best source is *locaux commerciaux*.
- **An opt-in dataset presented as a directory.** Mississauga's lists "only the
  businesses that agreed to be included" - the Boston survey problem, which
  maps who filled in a form rather than where commerce is.

The single recurring cause: **asserting from a column's existence, a dataset
title, or a plausible-looking flag instead of measuring.** Five separate
conclusions in the Canada profile had to be reversed for exactly that reason.
The project's first invariant already says this; a country profile is where it
is easiest to forget, because the volume is high and each individual check
feels small.
