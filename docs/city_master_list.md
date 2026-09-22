# Global city master list — CURRENT STATE

**This is the operative list: which cities this project could build next, and
what is stopping each one.** It is rewritten as things change, like
`docs/project_context.md` and unlike `DECISIONS.md`.

**The evidence lives in [`docs/global_country_shortlist.md`](global_country_shortlist.md)** —
87 countries screened, every probe logged, every negative with the measurement
behind it. That file is the trail; this file is the answer. When they disagree,
the trail wins and this file is stale.

Last reordered **2026-09-22**, after the Band D and D5 probes.

---

## Built — 14

| Country | Cities |
|---|---|
| **United States** (9) | San Diego · San Francisco · Los Angeles · Chicago · New York · Philadelphia · Miami · Boston · Washington D.C. |
| **Canada** (5, complete) | Vancouver *(with Surrey)* · Montréal · Calgary · Edmonton · Toronto |

## Candidates — 48

| Band | What is stopping it | Cities |
|---|---|---|
| **A** | Nothing. Screening complete | **7** |
| **B** | One narrow question each | **3** |
| **C** | A geocoding leg — build work, not screening | **17** |
| **D** | Four sub-tiers, see below | **21** |
| *Discarded* | Measured negative, evidence named | *14* |

---

## Band A — screening COMPLETE (7 cities, 5 countries)

Ordered by how little stands in the way.

| # | City | Business leg | What remains |
|---|---|---|---|
| 1 | **Guadalajara** 🇲🇽 | DENUE, SCIAN = NAICS, INEGI licence cleared | **Nothing** |
| 2 | **Madrid** 🇪🇸 | 148,814 open premises, 119,070 with valid coordinates, three-level classification, EPSG:25830. CC BY 4.0 + binding general conditions | **Nothing** |
| 3 | **Seoul** 🇰🇷 | 197,276 active premises over 8 datasets, EPSG:5174, status field, KOGL Type 1 | Build work — partial geocoding for 일반음식점 (90.7%), Korean-aware `check_personal_exposure.py` |
| 4 | **Milan** 🇮🇹 | 28,131 premises 99.1% coords, `insegna`, `codice_ateco`, CC-BY. All three buckets confirmed | Step 0 schemas for the two newly found layers |
| 5 | **Mexico City** 🇲🇽 | Same DENUE. **Rail from OSM** — 195/195 stops exact, 6,468 geometry points | One licence decision: ODbL share-alike on the station extract |
| 6 | **Barcelona** 🇪🇸 | 68,024-premises ground-floor census, CC-BY-4.0 | One residual: the portal's general notice is CAPTCHA-walled and unread |
| 7 | **Paris** 🇫🇷 | SIRENE, établissement-level, geolocated, Licence Ouverte 2.0 | **An owner decision, not a probe** — a national register is not the per-city municipal shape this project is built around |

**Guadalajara and Madrid have nothing outstanding at all.**

## Band B — one narrow question each (3 cities)

**Valencia** 🇪🇸 *(subway 84, tram 37 — the largest Spanish system measured)* ·
**Bilbao** 🇪🇸 · **Málaga** 🇪🇸

Spain is bespoke per city, so each needs its own register — but **two of the
three Spanish cities probed have had one**, which raises the prior sharply.

## Band C — viable, each needs a GEOCODING LEG (17 cities)

Build work with a known cost. No further probing changes these.

| Cities | Country | Business leg | Geocoding |
|---|---|---|---|
| **Tokyo**, Osaka, Nagoya, Yokohama, Sapporo, Fukuoka, Kyoto, Kobe, Sendai, Hiroshima *(10)* | 🇯🇵 | Premises-level food permits, CC BY, one national schema. **Two buckets — no general retail** | **Hardest met** — chōme/ban/gō, full-width numerals, `町字ID` 0% populated |
| **Taipei**, Kaohsiung, Taoyuan, Taichung *(4)* | 🇹🇼 | 商業登記 — premises, active/closed status, per-category assembly | Moderate — **NLSC's geocoder is keyless** |
| **Oslo** *(1)* | 🇳🇴 | 152,060 sub-units, `beliggenhetsadresse` (physical, not registered), NACE, open API no key | Moderate |
| **Copenhagen** *(1)* | 🇩🇰 | CVR `productionunits` — P-enheder each with own `address`/`zipcode`/`city`, plus `industrycode` | Moderate — **plus a free account** (`distribution.virk.dk` 401) |
| **São Paulo** *(1)* | 🇧🇷 | CNPJ — trade name, address, CNAE | **Hard, past Toronto's scale** |

**Japan is ten cities from one schema** — the best marginal-city cost in the
screen — against the worst geocoding problem and a two-bucket ceiling.
**Still the biggest open decision in this list**, and a judgment call rather
than a probe.

## Band D — 21 cities, four sub-tiers

### D-a — one cheap question each (4)

| City | State |
|---|---|
| **Prague** 🇨🇿 | `rzp.cz`, the *živnostenský rejstřík* (**trade-licence** register), is live — the right shape, since Czech licences are issued per premises. Not ARES, the company register. **Best D lead after Copenhagen** |
| **Dublin** 🇮🇪 | `data.gov.ie` lists a **Valuation Office API**, but `api.valoff.ie` and `www.valoff.ie` both returned 000 twice — host down, so ASSERTED not measured. Does the Irish rateable register carry a **use category**, where the UK's NNDR did not? |
| **Zurich** 🇨🇭 | **Food confirmed** — `Gastwirtschaftsbetriebe`, premises-level, GeoJSON. No second bucket found; the national STATENT is aggregate |
| **Singapore** 🇸🇬 | API answers but its search is loose. One controlled query settles it. Suspected registered-office shaped |

### D-b — rail ANSWERED, business leg is the blocker (10)

Rail screened via OSM. **Relation counts are upper bounds** — see the caveat
below.

| City | Rail (OSM) | Business leg |
|---|---|---|
| **Hong Kong** 🇭🇰 | 126 rel, 125 named, 117 coloured | **MEASURED NEGATIVE** on `data.gov.hk` — statistics tables only. Route left: **FEHD's licensed food premises list** (a department, not a portal) |
| **Santiago** 🇨🇱 | 30 rel, all named + coloured | **MEASURED NEGATIVE** on `datos.gob.cl` — `patentes comerciales` returns nothing. Municipal portals remain |
| **Rio de Janeiro** 🇧🇷 | 20 rel, all named + coloured | CNPJ, no coordinates → geocoding at São Paulo's scale |
| **Kuala Lumpur** 🇲🇾 | 14 rel, all named + coloured | `data.gov.my` live, wrong endpoint; SSM is company-shaped |
| **Jakarta** 🇮🇩 | **9 operating** of 11 — two are the proposed MRT East-West Line | `satudata.jakarta.go.id` live; stack unidentified |
| **Medellín** 🇨🇴 | 6 rel, all named, **only 2 coloured** — colours need assigning by hand | ArcGIS — a shape this project handles |
| **Tel Aviv** 🇮🇱 | 6 rel, **realistically 1** — Green and Purple are under construction and OSM does not mark them | `data.gov.il/api` 14 bytes; city portal **HTTP 472**, the documented IP refusal |
| **Hyderabad** 🇮🇳 | 6 rel, all named + coloured | Trade licences are municipal; `data.telangana.gov.in` dead |
| **Lima** 🇵🇪 | 4 rel, all named + coloured | `www.datosabiertos.gob.pe` live, wrong endpoint |
| **Kochi** 🇮🇳 | 2 rel, named + coloured | Kerala LSG live |

> **The relation counts are upper bounds.** The construction filter flagged
> unbuilt routes in Jakarta but returned **zero** for Tel Aviv, Bogotá and Rio —
> and Tel Aviv proves zero does not mean zero: its Green and Purple lines are
> under construction and OSM carries them as plain `light_rail` with no status
> marker. **A filter returning zero can mean "nothing to flag" or "this
> convention is not used here", and the result alone cannot tell you which.**

### D-c — genuinely UNREACHED, no finding either way (6)

**Tallinn** 🇪🇪 *(ariregister's fields are company-shaped — suggestive, unmeasured)* ·
**Stockholm** 🇸🇪 · **Budapest** 🇭🇺 · **Zagreb** 🇭🇷 · **Bucharest** 🇷🇴 ·
**Sofia** 🇧🇬 *(the 403 is a stock Apache page, not an IP block — the browser is worth trying)*

### D-d — one cheap gate (1)

**Sevilla** 🇪🇸 — rail is **registration-gated, not absent**: Spain's National
Access Point answers 401. The WMATA shape, a free account. Its business leg
still needs its own Spanish source.

## DISCARDED — 14 cities, each naming its evidence

| City | Why |
|---|---|
| **Berlin** 🇩🇪 | `Gaststätten` → 0 on `datenregister.berlin.de`; the Gewerberegister is not open data |
| **Hamburg** 🇩🇪 | `Gewerberegister` → 7 irrelevant hits on `suche.transparenz.hamburg.de`; building-permit PDFs and planning polygons |
| **Naples** 🇮🇹 | Only commercial dataset is "per procedimento e Municipalità" — aggregate |
| **Messina** 🇮🇹 | SCIA/DIA are business-*start notifications* — a flow, not a stock |
| **Helsinki** 🇫🇮 | Addresses fine (89.8%) but composition is 53% real estate, 4.8% retail |
| **Bogotá** 🇨🇴 | **Fails on rail** — one unnamed-ref, zero-colour relation; its only mass transit is BRT |
| **Vienna** 🇦🇹 | GISA strips the street address by design |
| **Amsterdam / Rotterdam** 🇳🇱 | Register is aggregate |
| **Athens** 🇬🇷 | Sector-only |
| **Lisbon** 🇵🇹 | Specific negative |
| **Poznań** 🇵🇱 | Specific negative |
| **Riga** 🇱🇻 | Addressed but unclassified |
| **Bratislava** 🇸🇰 | No activity classification at all |
| **Cairo** 🇪🇬 | No open-data infrastructure |

Plus the no-urban-rail set (Winnipeg, Hamilton, Québec City, Halifax,
Mississauga, Ottawa, ~30 single-feed countries) and access-not-data
(Russia, Ukraine).

**Germany is a country-level negative**, on two cities measured independently
at two different portal hosts.

---

---

# BY COUNTRY — for country-by-country implementation

The same 48 candidates, cut the other way. **Ordered by cities gained per unit
of work**, because that is what country-by-country optimises for, and it
reorders things sharply: Japan is mid-table by city and near the top by
country.

"Missing link" = the single thing that would move the country up a tier.

## Tier 1 — build now, nothing to discover (4 countries, 5 cities ready)

| Country | Cities | Source shape | Missing link |
|---|---|---|---|
| 🇲🇽 **Mexico** ▶ **IN PROGRESS** | **2** — Guadalajara, Mexico City | **DENUE**, national, coordinates, SCIAN **is** NAICS so the taxonomy may transfer from the US builds | **Being built now.** CDMX still needs one decision: offer the station extract under **ODbL share-alike**, since its rail comes from OSM |
| 🇪🇸 **Spain** | **2 now, 6 total** — Madrid, Barcelona ready | Bespoke **per city**, but two of three probed had a premises census | Madrid and Barcelona are ready. Valencia, Bilbao and Málaga each need **their own register found**; Sevilla needs a **free NAP account** for rail |
| 🇰🇷 **South Korea** | **1** — Seoul | 8 datasets, EPSG:5174, KOGL Type 1, daily | **Two build items, not probes:** partial geocoding for 일반음식점 (90.7% coords) and a Korean-aware `check_personal_exposure.py` |
| 🇮🇹 **Italy** | **1** — Milan | Bespoke per city. Naples and Messina measured out | **Step 0 schemas** for the two newly found Milan layers. Nothing to discover |

## Tier 2 — one decision, not one probe (1 country)

| Country | Cities | Missing link |
|---|---|---|
| 🇫🇷 **France** | **1 built-ready, 6 rail-confirmed** — Paris, Lyon, Marseille, Lille, Toulouse, Rennes | **An architecture decision you own:** SIRENE is a *national* register, not the per-city municipal shape this project is built around. Settle that and France is a six-city country with one integration |

## Tier 3 — a geocoding leg buys several cities (5 countries, 18 cities)

The investment tier. Each needs pipeline work written once, then cities are
cheap.

| Country | Cities | Business leg | Missing link |
|---|---|---|---|
| 🇯🇵 **Japan** ⏸ **DECIDED — BUILD, BUT LAST** | **10** | Food permits, CC BY, **one national schema** | **Verdict taken 2026-09-22: do the hard geocode, but not yet.** Build the easier geocoding countries first and let the shared machinery accumulate. Its own obstacles are unchanged — chōme/ban/gō, full-width numerals, `町字ID` 0% populated, and a **two-bucket ceiling** with no general retail |
| 🇹🇼 **Taiwan** | **4** | 商業登記, per-category assembly | A geocoding pass. **NLSC's geocoder is keyless**, so this is the cheapest Tier 3 entry |
| 🇧🇷 **Brazil** | **2** — São Paulo, Rio | CNPJ, no coordinates | Geocoding **past Toronto's scale**. Rio's rail is confirmed (20 relations, all named and coloured) |
| 🇳🇴 **Norway** | **1** — Oslo | 152,060 sub-units, `beliggenhetsadresse`, open API no key | A geocoding pass. Nothing else |
| 🇩🇰 **Denmark** | **1** — Copenhagen | CVR **P-enheder** with their own address + `industrycode` | A geocoding pass **and a free account** (`distribution.virk.dk` 401) |

**If you write one geocoder, write Taiwan's** — keyless, systematic addresses,
four cities. Japan's is a research project by comparison.

### Japan's cost is not fixed — it falls as the others are built

**Decided 2026-09-22: Japan gets built, and it goes last.** The reasoning is
not "postpone the hard thing", it is that **the hard thing gets cheaper while
you do the others**, so the same work costs less later.

Geocoding machinery this project already owns, from **Toronto**
(`pipeline/toronto/step3_geocode.py`) — the only Canadian city of six that
needed it, because its register carries no coordinate field and **Canada has no
national bulk geocoder**:

- a geocode step that sits between clean and map, with its own processed output
- the join-against-a-published-address-layer pattern, used instead of a geocoder
- **match-rate measurement by row type**, which is what caught the brief's
  71.4% being the wrong denominator: storefront rows matched **92.8%** while
  person-held licences dragged the all-rows figure to 73.1%
- the lesson that **the normalisation that matters is rarely street
  normalisation** — Toronto's real obstacle was units written into the address
  line (`"280 SPADINA AVE, #308"`), not abbreviations

Each Tier 3 country adds to that pool before Japan needs it:

| Build | What it contributes to Japan |
|---|---|
| **Taiwan** | A **keyless third-party geocoder** integration — request shaping, caching, rate limiting, failure handling. Japan's GSI geocoder is the same shape |
| **Norway / Denmark** | European street addresses at national scale, and the **free-account** pattern for Denmark's CVR |
| **Brazil** | **Scale** — CNPJ is ~72M rows, well past anything attempted so far |

By the time Japan is reached, what is left that is genuinely Japan-specific is
**block-address parsing** (chōme/ban/gō), **NFKC normalisation** of full-width
numerals, and the **join on `町字` by name** because the `町字ID` that exists to
make it machine-clean is 0% populated. That is a real problem, but it is a
smaller one than "write geocoding for this project".

**The risk to watch:** deferring is only cheaper if the machinery is actually
built *shared* rather than per-city. Toronto's step is city-specific today. If
Taiwan, Norway and Brazil each grow their own private copy, Japan inherits
nothing and the argument collapses. **Whoever builds the second geocoding city
should lift the common parts into `pipeline/` rather than copying Toronto's
file** — that is the decision that makes this ordering pay.

## Tier 4 — one probe decides the country (4 countries, 4 cities)

| Country | City | Missing link |
|---|---|---|
| 🇨🇿 **Czechia** | Prague | **Confirm `rzp.cz` is premises-shaped.** It is the *trade-licence* register, not ARES the company register, so the prior is good. **Best single probe left** |
| 🇮🇪 **Ireland** | Dublin | `valoff.ie` was down on both hosts twice. **Retry, then ask whether the rateable register carries a use category** — the UK's NNDR did not, and that killed the UK |
| 🇨🇭 **Switzerland** | Zurich | **A second bucket.** Food is confirmed with GeoJSON; retail and personal services were not found, and the national STATENT is aggregate |
| 🇸🇬 **Singapore** | Singapore | **One controlled query.** Its API answers but the search is loose. Suspected registered-office shaped, which would be fatal |

## Tier 5 — rail is answered, the business leg is the hunt (7 countries, 8 cities)

Rail screened via OSM and passing. **Every one of these needs a premises
register found**, and two have already failed at the national portal.

| Country | City | Rail | Missing link |
|---|---|---|---|
| 🇭🇰 **Hong Kong** | Hong Kong | **126 relations**, 125 named | **The register EXISTS and is queryable — but no bulk export found.** See below |
| 🇨🇱 **Chile** ↓ **FAILS** | Santiago | **30 relations**, all named + coloured | **Coverage failure, measured.** Chile licenses per *comuna*; only **5 of ~33** Metro comunas publish patentes, and **the Santiago comuna itself is not on the portal at all**. See below |
| 🇲🇾 **Malaysia** | Kuala Lumpur | 14 relations, all named + coloured | The right `data.gov.my` endpoint. SSM is company-shaped, so expect a registered-office failure |
| 🇮🇩 **Indonesia** | Jakarta | 9 operating of 11 | Identify `satudata.jakarta.go.id`'s stack |
| 🇨🇴 **Colombia** | Medellín | 6 relations, **only 2 coloured** | An **ArcGIS** probe — a shape this project already handles. Note colours would need assigning by hand. Bogotá is out: it fails on rail |
| 🇮🇳 **India** ↓ | Hyderabad, Kochi | 6 and 2 relations | **National portal measured negative** — 288,011 resources searched, nothing premises-level. Municipal corporations (GHMC, Kochi) unprobed. See below |
| 🇵🇪 **Peru** | Lima | 4 relations, all named + coloured | The catalogue endpoint on `www.datosabiertos.gob.pe` |
| 🇮🇱 **Israel** | Tel Aviv | 6 relations but **realistically 1** — Green and Purple are under construction | **Two problems:** the city portal returns **HTTP 472**, the documented IP-level refusal, and one operating line is thin for this project |

### Hong Kong, chased to the department — 2026-09-22

The furthest any Tier 5 city has been taken, and the verdict changed twice.

**1. `data.gov.hk` is a measured negative, by the strongest available check.**
Keyword search had returned statistics tables, which proves little. The
provider route is decisive: `organization_list` shows **129 organisations and
`hk-fehd` is one of them**, and `organization_show?id=hk-fehd` returns
**`package_count: 1`** — a single dataset, *"Products exempted from nutrition
labelling"*. So the licensed-premises register is **definitively not on the
open-data portal**. Searching by *provider* rather than *keyword* is the
generalisable move here: a keyword search cannot distinguish "absent" from
"named differently", and an org listing can.

**2. The register does exist, on FEHD's own site.**
`fehd.gov.hk/english/licensing/list_licensed_premises.html` →
**Lists of Licensed / Permitted Premises**, and it covers **two buckets**:

- **Food premises** — searchable by Shopsign/Address and by Licence/Permit Type
- **Non-food premises** — the same two routes. This is the **Personal services**
  bucket, which the earlier "food-only ceiling" claim said did not exist

The by-type form carries exactly the selectors a bulk extract needs:
`Licence Type` (General Restaurants · Light Refreshment · Marine · Factory
Canteens), `Special Endorsement` including **"All Licensed General
Restaurants"**, and **`District` including "- All districts -"** across all 19.

**3. But it is a QUERY INTERFACE, not a download.** No CSV, XLS, PDF or JSON
link exists anywhere on those pages — checked. Extraction would mean iterating
the form across licence types and districts and **scraping HTML**.

**So the honest verdict is neither "no data" nor "buildable".** It is: *a real
two-bucket premises register, publicly queryable, with no bulk route found.*
That is the **Seoul shape** — Seoul's food register also looked closed until the
page's own JS revealed a keyless POST — so the next step is to watch what the
form actually submits rather than to conclude from the absence of a download
link. Not yet done: the submit is JS-driven and did not navigate on click.

**This upgrades Hong Kong's prior considerably.** It has the largest rail
system in Tier 5 by a wide margin (126 relations, 125 named, 117 coloured) and
now a confirmed two-bucket register. What it lacks is a *route*, which is a
smaller problem than lacking data.

### Santiago — the Daegu failure, third occurrence — 2026-09-22

Provider enumeration settled this outright, and it took one pass. Chile issues
commercial licences (`patentes comerciales`) **per comuna**, so the question was
never "does Chile publish" but "how many of the ~33 comunas the Metro serves do".

`datos.gob.cl` lists **272 organisations, 67 of them municipalities**. Of those,
**15 are Metro-area comunas**, and asking each what it holds:

| | |
|---|---|
| Publish patentes | **5** — Independencia, La Florida, La Reina, Pedro Aguirre Cerda, Peñalolén |
| Present but publish none | Maipú, Puente Alto (245 datasets, no patentes), Recoleta, San Bernardo, Pudahuel, Huechuraba |
| Present with **zero** datasets | El Bosque, Ñuñoa, Quinta Normal, San Miguel |
| **Absent from the portal entirely** | **Santiago comuna itself** — the downtown — plus Providencia, Las Condes, Estación Central |

**5 of ~33, and the central comuna is missing.** Santiago's Metro converges on
the Santiago and Providencia comunas; a commercial-density map without them is
not a map of Santiago.

**This is the third time this exact shape has appeared** — Busan (4 of 16
districts), Daegu (4 of 9, with 중구 the downtown absent), now Santiago. The
generalisable rule is already in `add-country` and this confirms it: **where
licensing is devolved below the city, ask how many sub-units publish AND
whether the central one is among them, before believing a country count.** The
capital-aggregates case — Seoul, 25 of 25 — is the exception, not the rule.

### The Tier 5 remainder — where each one now stands, 2026-09-22

| Country | Method that worked | Result |
|---|---|---|
| 🇮🇳 **India** | `api.data.gov.in/lists` **enumerates — 288,011 resources** | **MEASURED NEGATIVE.** Searched properly: `trade licence` 209, `shops and establishment` 112,346, `commercial establishment` 316, **`Kochi` 1** (port exports). Every premises-shaped hit is either **one city that is not ours** (*Shops And Establishment Licence : **Ahmedabad***) or **aggregate** (*Vyapar **District wise ULB wise** Trade License Details*). Hyderabad's 192 hits are all census tables. **The national portal does not carry it**; GHMC and Kochi Municipal Corporation are the remaining route |
| 🇲🇾 **Malaysia** ↓ | Catalogue read in the browser — 292 datasets | **MEASURED NEGATIVE, and a new trap.** `lookup_premise` is a *genuine* premises table — `premise`, `address`, `premise_type`, `state`, `district`, **100% populated**, direct CSV, no auth. And it holds **3,916 rows nationally, 372 in Kuala Lumpur.** See below |
| 🇨🇴 **Colombia** (Medellín) | — | ArcGIS Hub `data.json` **404**, `api/search/v1` **401**. The Hub search page is live HTML. **Needs the browser** to find the real service root |
| 🇵🇪 **Peru** (Lima) | — | `www.datosabiertos.gob.pe` is Drupal, not CKAN, at every path tried. **Needs the browser** |
| 🇮🇩 **Indonesia** (Jakarta) | — | `satudata.jakarta.go.id` API paths resolve nowhere; the site root is live. **Needs the browser** |
| 🇮🇱 **Israel** (Tel Aviv) | — | **Not reachable by either method.** HTTP 472 and the host printed our own IP back — an IP-level refusal, so the browser shares the blocked address |

> **NEW TRAP — a real premises table can still be a SAMPLE, not a register.**
> Malaysia's `lookup_premise` passes every structural test this project
> applies: rows are individual premises, not aggregates; `premise`, `address`,
> `premise_type`, `state` and `district` are **100% populated**; it downloads
> as CSV with no account. It is nonetheless unusable, because it exists to
> support **PriceCatcher**, a price-monitoring programme — so it lists the
> premises whose prices are *surveyed*, and there are **372 in Kuala Lumpur**.
>
> For scale, this project's built and Band A cities carry 80,110 (Toronto,
> storefront rows), 148,814 (Madrid) and 197,276 (Seoul). **372 is three
> orders of magnitude short.**
>
> This is not the aggregate trap — the rows genuinely are premises. It is a
> **coverage** trap: the right shape at the wrong scale, and **only the row
> count reveals it**. Schema inspection passes it cleanly. The check that
> catches it is the one this project already runs for a different reason —
> *count the rows and compare against the city's plausible premises count*
> — which until now was about spotting truncation. Add sampling to what that
> check is for. Malaysia's composition also gives it away on a second look:
> 131 supermarkets and 69 mini-markets in a city of 1.8 million.

**The method is doing its job, and the honest summary is that it mostly
closes things.** Of the eight Tier 5 countries, provider/API enumeration has
now produced **three firm negatives** (Hong Kong's portal, Chile, India) and
**one upgrade** (Hong Kong's department, which turned out to have *two*
buckets). Four still need the browser, and one cannot be reached at all.

**A parameter-encoding note that cost a pass:** India's API ignores
`filters[title]=x` with literal brackets and honours `filters%5Btitle%5D=x`.
The unencoded form returns **HTTP 200 with the full unfiltered 288,011** and no
error — the same silent-ignore failure as `data.seoul.go.kr`, and the reason a
control term is not optional. The first search read as "no results" when it was
actually "no filter".

## Tier 6 — never actually reached (6 countries, 6 cities)

**No finding either way.** These failed on hosts, not data, so they are not
negatives.

🇪🇪 **Estonia** *(Tallinn — ariregister is company-shaped, suggestive but unmeasured)* ·
🇸🇪 **Sweden** *(Stockholm)* · 🇭🇺 **Hungary** *(Budapest — both portals resolve nowhere)* ·
🇭🇷 **Croatia** *(Zagreb — SPA shell)* · 🇷🇴 **Romania** *(Bucharest — resolves nowhere)* ·
🇧🇬 **Bulgaria** *(Sofia — the 403 is a **stock Apache page**, not an IP block, so the browser is the cheap next step)*

## Countries ruled out

🇩🇪 **Germany** *(two cities measured at two hosts — the Gewerberegister is not open data)* ·
🇦🇹 **Austria** *(GISA strips the street address)* · 🇳🇱 **Netherlands** *(aggregate)* ·
🇬🇷 **Greece** *(sector-only)* · 🇵🇹 **Portugal** · 🇵🇱 **Poland** ·
🇱🇻 **Latvia** *(unclassified)* · 🇸🇰 **Slovakia** *(no classification)* ·
🇪🇬 **Egypt** · 🇬🇧 **UK** *(NNDR is a tax register with no category)* ·
🇦🇺 **Australia**, 🇳🇿 **New Zealand** *(licensing is not municipal)* ·
🇧🇪 **Belgium** *(bulk access paid)* · 🇦🇪 **Dubai** *(no agency feed)*

## The order, as decided

1. ▶ **Mexico** — **in progress.** Two cities, one source, nothing to discover.
2. **Spain** — Madrid and Barcelona ready *now*; the other three likely rather
   than speculative.
3. **Korea** and **Italy** — one city each, nothing to discover, both with
   named build work rather than open questions.
4. **Taiwan** — the first geocoding build, chosen because it is the cheapest:
   keyless geocoder, systematic addresses, four cities. **Lift the shared parts
   into `pipeline/` here**, not later.
5. **Norway**, **Denmark**, **Brazil** — the rest of Tier 3, in rising
   difficulty.
6. ⏸ **Japan** — **last, by decision.** Ten cities, and by then the geocoding
   machinery is built.

**France sits outside this order** because its blocker is an architecture
decision rather than work: settle national-vs-per-city and six cities arrive at
once.

Tier 4's four probes (**Czechia** strongest) are cheap enough to run alongside
any of the above rather than competing with them.

---

## Two rules this list is maintained by

**A row reading "not reached", "unprobed" or a regional pattern is not a
discard.** Eleven cities were once sitting in the discard list on exactly those
grounds, against evidence in the same document. Every discard row above names
the finding that disqualified it, so a contradiction is visible rather than
inferable.

**A country ruling needs two cities measured, not one asserted onto a region.**
Germany qualifies — Berlin and Hamburg, at two different portal hosts. Italy
does not fail merely because Naples did, which is why Milan sits in Band A.

## Before building any city on this list

- `docs/build_briefs/<city>.md` if one exists, then
  `python scripts/brief_check.py <city>` — a brief caches Step 0's mistakes as
  confidently as its findings.
- **The region switcher blocks the first non-North-American city** (`PLAN.md`).
  `REGION_ORDER` is currently `["United States", "Canada"]` and `app/cities.py`
  raises on any city outside it, so even the Mexican cities need a line added.
- `add-country` first for any country this project has never built in — which
  is every country on this list.
