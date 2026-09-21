# Global country shortlist — which country to profile after Canada

**Worldwide in scope.** Every country on earth is in scope here, not a
shortlist of guesses: the screen starts from the full Mobility Database
catalogue — **87 countries, 2,476 static GTFS feeds** — so a candidate can be
ruled out, but not missed by omission. The United States and Canada are
excluded throughout as already built or screened.

The layer above [`add-country`](../.claude/skills/add-country/SKILL.md), as
[`city_shortlist.md`](city_shortlist.md) is the layer above `add-city`. This
file decides *which country is worth a profile*; the profile itself is a
separate and much larger job.

Started 2026-09-21. **No country here has been profiled and nothing has been
built.** Canada remains the only country screened end to end — see
[`canada_retrospective.md`](canada_retrospective.md) for what that cost.

Claims are labelled **MEASURED** (a number and the check that produced it) or
**ASSERTED** (plausible, unchecked — verify before acting), per
[`session_roles.md`](session_roles.md).

## The filter order, and two that were dropped

The screen was originally posed as: map coverage → transit → business data →
legal. Reordered on 2026-09-21, before running, because the first two do not
discriminate:

1. **Map coverage is free.** This project uses OpenStreetMap only as a
   basemap, and those tiles render for every populated place on earth. Tile
   quality varies; nothing is disqualified by it. **Skipped.**
2. **Rail existence barely discriminates** outside North America. Every
   candidate city in Europe and East Asia has urban rail. Rail-first was
   correct *inside* Canada, where it killed 6 of 13 candidates; globally it
   kills almost nothing.

So the order actually run was:

1. **Premises-level business data** — the real discriminator, below.
2. **Licence and privacy regime.**
3. **A readable transit feed** — confirm only. Note this is *not* the same
   question as "is there rail", and the difference turned out to matter.
4. Map coverage — free, skipped.

### The sharper form of the business-data question

> Does the country record **where commerce physically happens** — premises —
> or only where companies are **registered**?

This is the whole game, and it is what splits the world. A national company
register (Companies House, Registro Imprese, Handelsregister, Bolagsverket,
Australia's ABN) publishes a **registered office**, which is frequently an
accountant's address or a holding company's mailbox. Mapping those produces a
map of bookkeepers. A municipal licence register, a national *establishment*
register, or a commercial-premises survey records the actual shopfront.

Four shapes qualify:

| Shape | Example |
|---|---|
| Municipal licence register | US, Canada, **South Korea** |
| National **establishment** register | **France** (SIRET), **Mexico** (DENUE) |
| Commercial premises field survey | Montréal, **Barcelona** |
| Sector inspection register | UK FSA — **one bucket only**, Boston's shape |

## Master ranking, by tier

Tiers rather than a numbered order: the candidates differ in *which leg is
unproven*, which is not a thing a single score can express. Rail figures are
`scripts/screen_rail.py` output against real `routes.txt`, run 2026-09-21.

### Tier 1 — both legs measured. Ready for a country profile.

| | Rail (MEASURED) | Business (MEASURED) | The open question |
|---|---|---|---|
| **France** / Paris | **subway 16, tram 17, funicular 1** (IDFM) | SIRENE, établissement-level, geolocated, **Licence Ouverte 2.0**, non-diffusible masked at source | **Design, not data:** a national register is not the per-city municipal shape this project is built around |

France is the only candidate with no *evidential* gap. What it has instead is
an architectural one, and that is a decision to take before a profile rather
than a fact to discover during one.

### Tier 2 — one leg excellent, the other genuinely open

| | Status |
|---|---|
| **Mexico** | **The best business data found anywhere** — DENUE, 6M+ establishments, coordinates, **SCIAN = NAICS** so the taxonomy may transfer — and **a licence that clears** (INEGI, commercial use explicit). **But Mexico City's feed is unreachable:** the S3 mirror returns **403** and the city portal **times out**. **Guadalajara works** — *Mi Tren* / SITEUR, **3 LRT lines**, measured — so Mexico is viable through its second city even if CDMX stays shut. |
| **Spain** / Barcelona | Business **MEASURED and excellent** — the 68,024-premises ground-floor census. **Rail not yet properly tested:** the catalogue's Barcelona entry is a *bus* operator (Autos Castellbisbal, feed expired), not TMB, so the bus-only result is a feed-selection artefact and says nothing about the metro. |
| **South Korea** | Business **MEASURED and ideal** — 195 municipal permit types, KOGL Type 1. **Zero transit feeds in the catalogue.** Everything rests on whether the national transport source serves something readable. |

### Tier 3 — rail measured, business data unknown

All confirmed to have real urban rail; none has had its business register
probed. These are cheap to advance and could move up or out quickly.

| City | Rail (MEASURED) |
|---|---|
| **Santiago**, Chile | **subway 7**, tram 2, bus 418 — current DTPM feed |
| **Sofia**, Bulgaria | **subway 4**, tram 24, trolleybus 30 |
| **Bucharest**, Romania | **subway 5**, tram 15, trolleybus 16 |
| **Bangkok**, Thailand | **subway 4**, LRT 5 (+189 commuter, excluded) |
| **Athens**, Greece | **subway 3**, tram 2 — a dedicated rail feed on `data.gov.gr` |
| **Budapest**, Hungary | **subway 4**, tram 42 — but **feed expired 20260704**, so treat as unconfirmed |
| **Singapore** | **subway 13** — but a city-state, and its business data is likely registered-office shaped |
| **Hyderabad / Kochi**, India | **subway 3 / subway 1** — real metro feeds |
| **Cairo**, Egypt | **subway 2** — but **feed expired 20251027**, eleven months stale |

### Tier 4 — ruled out, with the reason

| | Why |
|---|---|
| **United Kingdom** | Business data is the wrong object — VOA is property without names, Companies House is registered offices, FSA is food-only |
| **Japan** | Business data is **aggregate counts**; and JR/Tokyo Metro absent from the catalogue |
| **Dubai** | **The catalogue's Dubai feed is an anonymous personal GitLab repository**, not an agency publication, and it does not return a valid zip. The transitland fallback 404s. No usable official feed found |
| **Hong Kong** | The Transport Department feed has **tram/LRT 7 and no subway** — the MTR is absent |
| **Manila** | The LRTA feed codes its four rail lines as **commuter rail (type 2)**, which this project excludes. A coding question rather than an absence, but it fails as published |
| **Jakarta** | Transjakarta is BRT; the MRT is not in the catalogue |
| **Belgium** | Establishment units exist but bulk access **requires application and payment** |
| **Germany, Italy, Sweden, Ireland, Portugal** | Company registers, mostly behind a fee |
| **Australia, New Zealand** | Good feeds; business licensing is not municipal in the US/Canada sense |
| **Russia, Ukraine** | Excluded on access and conflict grounds, not on data |

### Four results here are feed artefacts, not findings

Recorded so nobody re-reads the table as fact:

- **Barcelona and Madrid** were tested against *bus* operators, because a
  keyword match picked the first feed naming the city. TMB and Metro de Madrid
  were never tested.
- **Manila's** rail exists and is typed 2.
- **Hong Kong's** MTR exists and is not in that feed.
- **Mexico City's** feed exists and would not download today.

Every one is the Toronto lesson again: **what a catalogue says about a city is
not what the city runs.**

## Filter 3 — transit feeds, MEASURED 2026-09-21

One fetch of the Mobility Database catalogue (`bit.ly/catalogs-csv`), **3,511
feeds**. Counts are static GTFS feeds registered per country.

| Region | Counts |
|---|---|
| Americas | US 1,180 · CA 156 · BR 16 · MX 12 · CL 9 · CO 7 · AR 4 |
| Europe | **ES 169** · FR 123 · IT 77 · SE 61 · DE 60 · PL 54 · IE 50 · GB 46 · PT 35 · EE 26 · FI 22 · RO 19 · LV 17 · HU 11 · BE 10 · LT 10 · CZ 8 · CH 5 · **NL 2 · AT 2 · DK 1 · NO 1** |
| Asia-Pacific | AU 53 · TR 24 · IN 19 · JP 18 · NZ 10 · TH 10 · MY 10 · TW 9 · SG 4 · AE 3 · HK 2 · IL 2 · **KR 0** |

**A feed count is not a rail count.** Spain's 169 are mostly regional bus.
Per-city rail confirmation is still owed for every candidate below.

### The finding that inverted the working assumption

East Asian *transit* and East Asian *transit data* are different things:

| Country | Feeds | What is actually in them |
|---|---|---|
| **South Korea** | **0** | Nothing. Not one feed in the catalogue. |
| **Taiwan** | 9 | **All rural bus** — Changhua, Nantou, Taichung, Miaoli, Yunlin. No Taipei MRT. |
| **Japan** | 18 | Almost all **local bus and ferry** — Aomori city bus, volunteer-run buses across Shizuoka, an island ferry. Only Kobe Subway and Tokyo's municipal bureau are urban rail; **JR East, Tokyo Metro and the private railways are absent**. |
| **Singapore** | 4 | **SMRT / SBS Transit / LTA** — the MRT is there. |
| **Hong Kong** | 2 | Transport Department. |

**Absence from the Mobility Database is not absence of a feed.** This measures
*catalogue coverage*, which is precisely the trap that produced the Toronto
error — a mirror three months stale and silently missing an entire mode. Korea,
Taiwan and Japan are **catalogue-blind, not ruled out**; each needs a direct
national-source probe, listed at the end.

## The candidates

### Mexico — the strongest shape found anywhere

**MEASURED.** INEGI's **DENUE** (Directorio Estadístico Nacional de Unidades
Económicas), 2024 Economic Census edition: **over 6 million establishments**
with identification, location, economic activity and size, and **geographic
coordinates explicitly published for display on cartography**. Classified by
**SCIAN**, which *is* NAICS — the trilateral US/Canada/Mexico standard.
Available as bulk download and API.

What makes it stronger than France or Korea is the third leg:
`pipeline/taxonomies/naics.py` may transfer largely unchanged, the same
argument that makes Montréal cheap. National coverage, real coordinates **and**
the classification this project already implements is a combination nothing
else here has.

**The licence clears — MEASURED 2026-09-21.** INEGI's terms permit copying,
distributing, publishing, adapting, reordering and extracting its information,
and **commercial exploitation is explicitly allowed**. Three conditions:

- **Attribution in prescribed form:** `Fuente: INEGI, <name of the product the
  information is taken from>`, with the update date where applicable — the
  example INEGI itself gives is `Fuente: INEGI, Censos Económicos 2009`.
- **Derived works must notify the end user of any analysis or transformation
  applied** (*"notificar al usuario final de cualquier análisis o
  transformación que haga a la información"*). This is **Montréal's
  interpretation clause in another language**, and this project plainly
  triggers it — ring density, category buckets, storefront filtering. A bare
  source credit would not satisfy it.
- **No suggestion that INEGI made the modifications or endorses the result.**

No restriction on republishing or on displaying the data on a map.

So Mexico now passes filters 3 and 4 on measured evidence. **What remains is
the transit leg:** 12 catalogue feeds, and whether Metro CDMX is among them is
**unverified**.

### France — strongest at scale, wrong shape

**MEASURED.** SIRENE publishes *établissements* — SIRET is per establishment,
not per company — with addresses and a monthly geolocated file carrying SIRET,
X/Y, commune code and geolocation quality variables, under **Licence Ouverte /
Open Licence version 2.0**. 123 catalogue feeds.

**Its privacy problem is solved upstream.** Establishments with diffusion
status `P` have the entrepreneur's name, commune address **and geolocation
masked** by INSEE. That is Edmonton's `<REDACTED FOR PRIVACY>` at national
scale. Reuse still requires GDPR and *Loi CNIL* compliance and respect for
individual opposition declarations.

**The catch is structural, not legal**, and `add-country` already names it: a
national register covering every city at once is *not* the shape this project
is built for. Scoping and taxonomy were both designed around per-city municipal
registers, and SIRENE includes every office, depot and administrative site
alongside the shopfronts. That is a design question to settle **before** a
screen, not after.

### South Korea — ideal data, no catalogued feed

**MEASURED.** **195 local-government permit types** consolidated onto
`data.go.kr` by the Ministry of the Interior and Safety, including a national
standard dataset (`전국 일반음식점 표준데이터`, ID 15096283) and per-category
ministry files. Carries operating / suspended / closed status, licence and
closure dates, business-type classification, and road-name **and** lot-number
addresses. Licence is **KOGL Type 1** — commercial use and derived works
permitted, attribution required (source, year, institution, URL).

This is the US/Canada municipal-licence model, nationally standardised — the
best structural match to what this project already does.

**Two blockers:**

- **Zero transit feeds in the catalogue**, above. Unresolved.
- **The portal moved on 2026-04-16.** LOCALDATA (`localdata.go.kr`) was closed
  and everything consolidated into `data.go.kr`. The old host **refuses
  connections** (verified). Every endpoint is five months old and all
  documentation written against LOCALDATA is stale.

**ASSERTED:** that coordinates are published in EPSG:5174 (Korea Central Belt
TM). This came from documentation of the *closed* system. The project would
reproject to per-city UTM regardless — Seoul ≈ 127°E is UTM 52N, EPSG:32652.

### Spain / Barcelona — the strongest single city

**MEASURED.** The *Cens de locals en planta baixa* — a census of **ground-floor
premises intended for economic activity** — **68,024 premises**, of which
**61,875 active**, split **21,167 retail / 33,740 services**, a 90.9%
occupancy rate, run by the City Council for about ten years and published on
Open Data Barcelona.

This is Montréal's `locaux-commerciaux` exactly, and the Canada retrospective's
argument applies unchanged: a field survey of actual storefronts is arguably a
*better* answer to this project's premise than a licence register, because it
records what is on the street rather than who registered. Spain also leads
Europe on feed count at 169.

**ASSERTED:** that Madrid's *censo de locales y actividades* is the same shape.
Not checked.

### Brazil — real, and expensive

**MEASURED.** CNPJ open data from Receita Federal, published monthly:
**~72 million establishments** with company name, **trade name**, full address,
postcode and **CNAE** classification. 16 catalogue feeds.

Two costs that no city in this project has yet paid:

- **No coordinates.** Geocoding at a scale far beyond Toronto's 159,872.
- **The *sócios* (partner) list is personal data** — names, qualification, age
  range — and must never be downloaded. Toronto's `Client Name` problem at
  national scale.

### Newly surfaced by the exhaustive sweep

The catalogue sweep put 60 further countries on the table. Three were probed;
the rest are listed below rather than silently dropped.

**Dubai (UAE) — the best of the new ones.** **MEASURED:** Dubai Pulse
publishes `ded_license_master` (described as the primary reference for
business licences in **mainland Dubai, excluding the Free Zones**),
`ded_license_activities`, `ded_business_activities` and `ded_commerce_registry`
— CSV plus an API-key-gated API, updated into 2026. That is a municipal
licence register with an activity taxonomy, the US/Canada shape. Dubai Metro
has 3 catalogue feeds.
**Unverified and decisive:** whether the licence records carry **addresses or
coordinates** at all, and what the reuse terms are. A register without a
location is not mappable.

**Chile — right model, fragmented and stale.** **MEASURED:** `datos.gob.cl`
carries *Patentes Comerciales* — municipal commercial licences, exactly the
model this project is built on, since a *patente municipal* is required for any
commercial activity at a fixed location. But it is published **per
municipality** (La Reina, San Antonio and others) rather than as a national
standard, availability is uneven, and **Santiago's own directory is active
licences as of May 2016** — a decade stale. Santiago's metro is excellent and
Chile has 9 feeds, so this is worth a second look at the *current* municipal
portals rather than the national aggregator.

**Istanbul — fails on the data, despite everything else fitting.**
**MEASURED:** İBB runs a real open data portal (`data.ibb.gov.tr`) under its
own Open Data Licence, granting a worldwide, royalty-free, permanent,
non-exclusive right to reuse. But the business-licence dataset is **"the number
of first-class non-food establishments … on a district and sector basis"** —
**aggregate counts per district**, not premises records. Same defect as Japan's
Economic Census: a statistic, not a register. Turkey has 24 feeds and Istanbul
has one of the largest metro networks in Europe, so if a premises-level source
exists elsewhere on that portal this flips — **ASSERTED that it does not**,
based on one dataset.

**Has a metro and feeds, business data unprobed:**

| Country | Feeds | Cities in the catalogue |
|---|---|---|
| India | 19 | Delhi, Mumbai, Bengaluru, Hyderabad, Kochi |
| Romania | 19 | București, Brașov, Constanța, Oradea, Sibiu |
| Hungary | 11 | Budapest, Pécs, Szeged, Miskolc |
| Thailand | 10 | Bangkok, Chiang Mai |
| Malaysia | 10 | (municipality not recorded) |
| Greece | 4 | Athens, Thessaloniki |
| Bulgaria | 4 | Sofia, Pleven |
| Egypt | 5 | Cairo, Port Said |
| Indonesia | 3 | Jakarta, Bogor, Bali |
| Philippines | 3 | Manila |
| Israel | 2 | (municipality not recorded) |
| Ukraine | 7 | Kyiv, Lviv, Odesa — **excluded for now**, active war |
| Russia | 2 | Moscow Oblast, St Petersburg — **excluded**, sanctions and access |

**Has feeds but no urban rail**, so out on filter 2 regardless of data quality:
Estonia (26 — Tallinn is trams only), Latvia (17), Lithuania (10), Cyprus (6),
Slovenia (6), Slovakia (5), Croatia (4), Serbia (7), Luxembourg (3),
North Macedonia (2), Moldova (2), Montenegro, Georgia, Bosnia, Greenland (2).
Several of these run tram networks that would qualify as `route_type 0`, so
"no urban rail" here means **no metro or light-rail system of the scale this
project maps** — worth revisiting only if the project ever takes tram-only
cities.

**Thin coverage, mostly single-city bus feeds**, no further work proposed:
Cameroon (4), Morocco (4), Nicaragua (3), Ethiopia (3), Albania (3), Ghana (2),
Côte d'Ivoire (2), Tunisia (2), Rwanda (2), DR Congo (2), South Africa (2),
Peru (2), Costa Rica (2), Bolivia (2), and fifteen countries with a single
feed each — Algeria, Mali, Sierra Leone, Uganda, Kenya, Dominican Republic,
Zimbabwe, Nigeria, Uruguay, Sri Lanka among them. Addis Ababa, Abidjan, Lagos
and Lima all have rail that the catalogue does not carry, so these are
**catalogue-blind in the same way Korea is** — but none has a known open
premises-level business register, so the business leg would fail first.

### Ruled weak

| Country | Why |
|---|---|
| **United Kingdom** | **MEASURED:** VOA's rating list "records property, not people: an address, a description, a floor area and a value" — premises-level but **no trade name and no category**. Companies House gives registered offices. The FSA food-hygiene register would work and is **food only** — Boston's two-bucket shape. |
| **Japan** (data) | **MEASURED:** the Economic Census publishes **aggregate counts by area**, not an establishment register with addresses. |
| **Belgium** | **MEASURED:** KBO/BCE does carry *vestigingseenheden* at specific addresses, but **full bulk data and API access require formal application and payment**. |
| **Germany, Italy, Sweden, Ireland, Portugal, Austria, Switzerland, Czechia** | **ASSERTED**, none individually probed: the EU default is a *company* register — Handelsregister, Registro Imprese, Bolagsverket, CRO — recording registered offices, usually behind a fee. |
| **Australia** | **ASSERTED:** 53 feeds, but business licensing is not municipal in the US/Canada sense, so filter 3 likely fails despite the good feed coverage. |

Everything else the catalogue knows about is covered under "Newly surfaced by
the exhaustive sweep" above, including the countries ruled out on rail and the
long tail of single-feed coverage. **New Zealand** (10 feeds — Auckland,
Wellington, Christchurch) belongs with Australia: good feeds, and business
licensing that is not municipal in the US/Canada sense. **Colombia** (7 —
Bogotá, Cali) runs BRT rather than metro in Bogotá; Medellín's metro is not in
the catalogue.

## GDPR is filter 4 for all of Europe, and it is the expensive half

The live question is whether **a sole trader's business address is personal
data**. Ontario answered its version explicitly — business-capacity information
is excluded *even when the business is run from a dwelling* — and the Canadian
screen still cost days across four provinces that **did not agree with each
other**.

France answers it *structurally*, by masking non-diffusible records at source,
which is why France is cheap here. No other European candidate is known to.
Expect per-country statutory reading rather than one EU-wide answer, and expect
it to dominate the cost of any European profile.

## Open probes, cheapest decisive first

1. ~~INEGI's licence terms for DENUE.~~ **Done 2026-09-21 — it passes.** The
   remaining Mexican question is the transit leg: **is Metro CDMX in the
   catalogue, and does a readable feed exist?** That is now the single check
   standing between this project and its strongest candidate.
2. **Taiwan → TDX** (Transport Data eXchange, MOTC). Does it serve **static
   GTFS for Taipei Metro and Kaohsiung MRT**, and under what licence?
   Registration-gated, like WMATA — a known cost, not a new one.
3. **Japan → ODPT** (Open Data Platform for Transportation) and the GTFS-JP
   standard. Does it serve static GTFS-JP for **Tokyo Metro, Toei and JR
   East**? The catalogue holds neither the private railways nor JR, which is
   where most of Tokyo's ridership is.
4. **South Korea's transit data**, from the national source rather than the
   catalogue. This single question decides whether the best-matched business
   data in the world for this project is reachable at all.
5. **Barcelona's census schema, live** — columns, coordinates, licence,
   and whether the activity codes resolve to the project's three buckets.
6. **Re-verify Korea's endpoints on `data.go.kr`**, since everything predates
   the April 2026 migration.
7. ~~Dubai's `ded_license_master`.~~ **Moot for now — Dubai fails on transit
   first.** The catalogue's Dubai feed is an anonymous personal GitLab
   repository returning a non-zip, and the transitland fallback 404s. The
   business register may well be excellent; there is no agency feed to pair it
   with until one is found.
7b. **Barcelona's real rail feed.** TMB was never tested — the catalogue's
   Barcelona entry is a bus operator. This is the single cheapest check that
   could promote Spain to Tier 1, since its business leg is already measured.
7c. **Mexico City's feed, retried.** `datos.cdmx.gob.mx` timed out and the S3
   mirror returns 403 with an XML error body. Worth one retry from a different
   network before concluding anything: Guadalajara already carries Mexico on
   its own, but CDMX is the prize.
8. **Istanbul, second look.** One dataset was aggregate; İBB's portal is large
   enough that a premises-level source may exist, and Istanbul's metro would
   make it a strong candidate if one does.
9. **Chile's municipal portals directly**, rather than the national
   aggregator — Santiago's national-portal copy is a decade stale, which says
   nothing about what the municipality publishes today.

## Two framings this screen reversed

Recorded because the pattern matters more than the individual errors, and both
were mine.

| Asserted | Actually |
|---|---|
| Rail is the cheapest disqualifier, so screen it first | True in Canada, false globally — every candidate city has rail. **The readable-feed question is the real one**, and it is a different question |
| East Asia is the obvious target, being transit-rich | Transit-rich and **open-transit-data-poor**. Korea has 0 catalogued feeds, Taiwan's 9 are all rural bus, Japan's 18 are mostly volunteer-run village services |

The second is the more useful lesson: **"has good public transit" and "publishes
a feed this project can read" are independent properties**, and conflating them
would have pointed the whole effort at the wrong continent.
