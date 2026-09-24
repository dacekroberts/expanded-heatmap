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
`scripts/screen_rail.py` against real `routes.txt`, or `scripts/probe_geodata.py`
against the publisher's own layer. All 2026-09-21.

### Final standings — every viable candidate, and its one remaining blocker

The useful summary. Each row below Tier 1 has **exactly one** thing standing in
its way, and the column says what.

| | Country / city | Rail | Business | The single blocker |
|---|---|---|---|---|
| **1** | **France** / Paris | subway 16, tram 17, funicular 1 | SIRENE, établissement-level, geolocated, Licence Ouverte 2.0 | **None evidential** — an architectural choice about national vs per-city scope |
| **2** | **Spain** / Barcelona + 5 more | **6 metro cities**: Madrid 13, Barcelona FGC 4, Bilbao, Málaga, Valencia, Sevilla | Barcelona's 68,024-premises ground-floor census | **One unread licence** |
| **1=** | **South Korea** / **Seoul only** ↑↑ | **1,099 stations**, WGS84, English names, transfer data | **197,276 active premises** across 8 datasets, no account: EPSG:5174 coords, status field, **KOGL Type 1**, daily, cp949 | **None evidential** — screening is complete; a geocoding fallback for 일반음식점 alone (90.7%) is build work, not a blocker |
| **2** | **Taiwan** / Taipei | **complete and unauthenticated**: 122 stations + **5 lines as MULTILINESTRING** + line colours + English | `商業登記`: premises addresses, active/closed status | **No coordinates** → geocoding, and per-category assembly |
| **2** | **Mexico** / Guadalajara | Guadalajara LRT 3 verified | **DENUE**, 6M+ establishments, **SCIAN = NAICS**, INEGI licence clears | **CDMX is domain-wide unreachable**; Guadalajara carries it meanwhile |
| **1=** | **Italy** / **Milan** ↑↑ | **subway 5, tram 17** (ATM) — M1–M5 | **28,131 premises, 99.1% with coordinates**, `insegna` (shop sign), `codice_ateco`, `settore_merceologico`, floor area, **CC-BY** | **Whether Personal services is reachable** — two buckets confirmed, the third not |
| **2** | **Brazil** / São Paulo | **94 stations + 6 lines**, EPSG:31983 already correct, metro/trem discriminator, built/planned separate | CNPJ, ~72M, trade name + address + CNAE | **No coordinates** → geocoding past Toronto's scale |
| **3** | **Norway** / Oslo | metro 5, tram 9 | **MEASURED premises-level** — 152,060 Oslo sub-units, `beliggenhetsadresse`, NACE, open API no key | No coordinates → geocoding |
| **3** | **Japan** / Tokyo | **solved**: 10,235 stations + 21,932 line segments, PDL 1.0 | Premises-level food permits, CC BY, national standard schema — but **coordinates are 0% populated** (see the correction below) | **A geocoding leg against Japanese BLOCK addresses**, plus a two-bucket ceiling. Density unmeasurable until geocoded |

**Israel and Peru moved to Tier 4** (2026-09-21) — see below.

### Tier 3 business probes, 2026-09-21 — and the distinction that decides them

Probing the Tier 3 registers produced one pass, two clear failures, and a
structural point that disposes of most of the rest.

**The point: a COMPANY register lists companies, so a chain appears ONCE, at
its head office.** This project maps shops. That is not a data-quality
complaint — it is a category error, and it is why "the register is open and
has addresses" is not sufficient.

| Country | Verdict | Evidence |
|---|---|---|
| **Norway** | **PASSES** | `underenheter` with **`beliggenhetsadresse`** — the physical location address, kept distinct from the registered one. 152,060 Oslo sub-units, open API, no key. NACE codes. **No coordinates** → geocoding |
| **Finland** | **NOT RULED OUT — see the correction below** | PRH `avoindata` v3, open, no key, **89,816 companies in Helsinki**, NACE with English descriptions. **89.8% carry a real street address.** The obstacle is composition, not addressing |
| **Austria** | **FAILS — no street** | GISA, 1,032,283 active licences, but location is NUTS/LAU/postcode/town. No street address |
| **Chile** | **WEAK** | *Patentes comerciales* are the right model but published per municipality, unevenly, and **Santiago's national-portal copy is active licences as of May 2016** |
| **Denmark** | **UNPROBED** | `datacvr.virk.dk` returns **403** behind bot protection; the third-party API is quota-limited. CVR *produktionsenheder* remain the right object to chase |
| **Singapore** | **UNPROBED** | `data.gov.sg` API requires an auth token |
| **Netherlands, Portugal** | **UNPROBED** | Catalogues reachable (`data.overheid.nl` returns 64 hits for *bedrijven vestigingen*; `dados.gov.pt` answers) but no dataset inspected |
| **Czechia, Estonia** | **UNPROBED** | Endpoint guesses returned 404; both have establishment concepts (`provozovny`, e-Business Register) worth a proper look |
| **Germany, Sweden, Italy, Greece, Romania, Bulgaria, Hungary, Poland, Latvia, Croatia, Slovakia, Thailand, India, Egypt** | **UNPROBED** | None probed. The EU default is a company register, which the point above disqualifies — but that is a **pattern, not a probe**, and this file's own rule says a pattern deprioritises and never rules out |

### FULL Tier 3 business sweep, 2026-09-21 — all 20 countries

Every remaining Tier 3 country plus the six previously attempted, run to a
hard line. **One country passed outright and it was not one anybody expected.**

#### The method error this exposed first

A discovery pass across 20 national portals reported "no API" for **17 of
them**. A second pass with corrected endpoints found working APIs for **at
least seven of those seventeen**. The portal URLs in the first pass were
guesses, and guessing produced false negatives at scale — the same class of
mistake as Peru's missing `www.`, and at eight times the volume.

**Recorded because it is the most likely way this screen goes wrong again:**
an unverified endpoint is not evidence about a country.

#### ITALY PASSES — and the city was wrong in our own list

Italy sat in Tier 3 on **Naples** (subway 3, tram 3, funicular 3). Naples
publishes only *Controlli su commercio e ambulantato* — commerce inspections,
not a register. **Milan does, and Milan is the answer.**

`dati.comune.milano.it` (CKAN, no key), `Attività commerciali: esercizi di
vicinato in sede fissa` — fixed-premises neighbourhood shops — as CSV, JSON
**and GeoJSON**, under **Creative Commons Attribution**:

| | MEASURED |
|---|---|
| Rows | **28,131**, of which **27,886 carry a Point geometry (99.1%)**, EPSG:4326 |
| **`insegna`** | **the shop sign** — the trading name, which is exactly what this project displays, and it is the *sign* rather than the legal entity |
| **`codice_ateco`** | ATECO, Italy's NACE implementation |
| **`settore_merceologico`** | merchandise sector — a **second, independent** classification |
| `superficie_vendita` | sales floor area |
| `Civico`, `DescrizioneVia`, `CAP`, `MUNICIPIO`, `NIL` | street number, street, postcode, borough, neighbourhood |
| `LONG_X_4326` / `LAT_Y_4326` | explicit coordinates alongside the geometry |

**Rail, screened the same day: Milan ATM gives subway 5, tram 17** — M1–M5
exactly, current feed, 45 MB.

**So Italy has both legs measured.** On field richness this is the best
business source in the screen: it carries a trade name, two classifications
and a floor area, where Barcelona's census carries premises and use. Companion
datasets on the same portal and licence cover *pubblici esercizi* (bars and
restaurants, the Food service bucket) in and out of the commercial plan.

**The one open question:** whether Personal services is reachable — either
inside `settore_merceologico` or as a separate acconciatori/estetisti dataset.
Two buckets are confirmed; the third is not.

#### Every other country, with what actually happened

| Country | Route found | Verdict |
|---|---|---|
| **Latvia** | `data.gov.lv`, *Uzņēmumu reģistrs*, **CC0-1.0**, 122 MB CSV | **FAILS.** 100% carry an address — and there is **no activity or industry column at all** in its 21 fields, so the three buckets cannot be derived. The UK's exact defect. Also **60% terminated**, and it mixes 36,197 farms and 19,860 associations |
| **Finland** | `avoindata.prh.fi` v3, open | **UNRESOLVED** — see the correction below. 89.8% have streets; **53% are real estate** |
| **Germany** | **`ckan.govdata.de`** works — 6,058 hits for *gewerbe*, some GeoJSON | **UNRESOLVED.** Hits are municipal and statistical; no national premises register surfaced |
| **Czechia** | **ARES works** — `/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/{ico}` returns name plus a structured `sidlo` | **Company register**, registered seat. The `provozovny` (establishment) side of RŽP is the thing to chase and was not reached |
| **Singapore** | **`api-production.data.gov.sg/v2/public/api/datasets`** answers unauthenticated | Route open, **register unprobed** |
| **Netherlands** | `data.overheid.nl`, 258 hits for *vestigingen* | **AGGREGATE trap** — the top hits are *"Aantal vestigingen per buurt"*, counts per neighbourhood |
| **Greece** | `data.gov.gr`, 343 hits | **Sector-specific only** — shipyards, wineries. No general register surfaced |
| **Portugal** | `dados.gov.pt` udata API works | Statistical and sector-specific hits; no register |
| **Poland** | **`api.dane.gov.pl/1.4/datasets`** works | Hits are statistical — REGON *territorial nomenclature*, not the register itself |
| **Thailand** | `data.go.th` | **HTTP 403** — blocked |
| **Bulgaria** | `data.egov.bg` | **HTTP 403** — blocked |
| **Croatia** | `data.gov.hr` | Returns **HTML** — a single-page front end; the real API path was not found |
| **Slovakia** | `data.slovensko.sk` | Returns **HTML** — same |
| **Romania** | `data.gov.ro` | Connection failed on both http and https |
| **Denmark** | `datacvr.virk.dk` **403** behind bot protection; `distribution.virk.dk` failed | **UNPROBED.** CVR *produktionsenheder* remain the right object |
| **Estonia** | The `ariregister` bulk CSV URL **404s** | **UNPROBED** |
| **Sweden, Hungary** | No CKAN at the obvious base | **UNPROBED** |
| **India** | `data.gov.in` requires an API key | **UNPROBED** |
| **Egypt** | No open API found at CAPMAS | **UNPROBED** |

#### HARD-LINE RE-RUN of the unreached 15, multiple strategies

The nine never-reached plus the four route-only countries, re-probed with
strategies chosen against what had already failed: full browser headers with a
`Referer` for the 403s, `www.`/bare and http/https variants, alternative API
shapes (CKAN alt paths, udata, Entryscape, keyless back ends), and the
**direct register host** instead of the national portal.

**Six countries gained a working route that did not exist before.** None of
them gained a usable register.

| Country | What the strategies found | Verdict |
|---|---|---|
| **Slovakia** | **Route opened** — `api.statistics.sk/rpo/v1/search` returns **500 records** per query, each with `addresses` (street, buildingNumber, postalCode, municipality + code) and `fullNames` carrying validity history | **FAILS — no activity classification.** Record keys are `id`, `identifiers`, `fullNames`, `addresses`, `establishment`, `sourceRegister`. **Latvia's defect exactly**: addressed and unclassifiable |
| **Czechia** | **RZP opened** — `/ekonomicke-subjekty-rzp/{ico}` returns `adresySubjektu`, `zivnostiStav` counts, and **`zivnosti` with `predmetPodnikani`** — an activity description per licence | **Closest near-miss.** It *has* classification. But it is **per-ICO lookup with no bulk export**, the address is the registered seat, and the `provozovny` (establishment) side is not in the response |
| **Denmark** | **Route opened** — `admin.opendata.dk` CKAN, and **the DAWA national address API works and returns coordinates** (a free national geocoder) | **Copenhagen is absent.** The only CVR *produktionsenheder* dataset published is **Aarhus Kommune's** (XML/XLSX/ODS). Production units are published voluntarily per municipality, and the metro city does not |
| **India** | **Keyless catalogue opened** — `api.data.gov.in/lists` exposes **288,011 resources** with no API key | **Aggregate, and the wrong cities.** Hits are *"Shops And Establishment Licence : Ahmedabad : 2015-16 to 2018-19"* and *"Shop and Esta Statistical Details : Rajkot"* — multi-year statistical summaries for cities with no metro, not premises registers for Hyderabad or Kochi |
| **Croatia** | **Route opened** — the working path is `/ckan/api/3/action/`, not `/api/3/action/` | **Statistics only** — *Trgovina na malo* (retail trade) as HTML and XLSX |
| **Poland** | `api.dane.gov.pl/1.4/datasets` works | **No register.** Queries fuzzy-match to tourist organisations, vaccination points and financial statements. CEIDG and REGON both require keys |
| **Germany** | `ckan.govdata.de` **and** Berlin's `datenregister.berlin.de` both work | **No premises register.** 18 Berlin hits for *Gewerbe* are all statistical XLS — turnover, broadband, load profiles |
| **Singapore** | v2 API works | **Inconclusive** — page 1 of the catalogue holds 10 datasets, none business-related. Not paginated through |
| **Estonia** | `avaandmed.eesti.ee/api/datasets` answers | Returns **0 results**; the ariregister bulk CSV **404s** on two URL forms. Unresolved |
| **Thailand** | **403 on every strategy** — including browser headers with a `Referer`, and the DBD register directly | **BLOCKED.** Consistent across paths; consistent with geo-blocking |
| **Bulgaria** | **403**, and the registry agency refuses connections | ~~**BLOCKED**~~ → **CLOSED 2026-09-22 on data**, enumerated around the block via `data.europa.eu` SPARQL: 141 municipal premises registers nationally, **none of them Sofia's**. See the superseding note below |
| **Romania** | **ConnectTimeout** on `www.`/bare, https/http, and the ONRC portal | **UNREACHABLE** |
| **Sweden** | Entryscape 404, Stockholm 500, Göteborg HTML | **NO ROUTE FOUND** |
| **Hungary** | `kozadat.hu` 404, Budapest refuses connections | **NO ROUTE FOUND** |
| **Egypt** | CAPMAS serves HTML only | **NO OPEN API** |

**The pattern across all fifteen:** the obstacle was never that a country
lacks business data. It is that the data is **statistical rather than
premises** (India, Croatia, Germany, Poland), **unclassified** (Slovakia,
Latvia), **published for the wrong city** (Denmark's Aarhus, India's
Ahmedabad), or **unreachable from here** (Thailand, Bulgaria, Romania).

**One genuinely useful by-product:** Denmark's **DAWA** address API is a free
national geocoder returning coordinates — the thing Norway, Taiwan and Brazil
all need and Canada had to solve city by city.

#### What the sweep actually settled

- **1 passes both legs:** Italy, via Milan.
- **1 fails on evidence:** Latvia — addressed, unclassified.
- **1 unresolved with numbers:** Finland.
- **4 have a working route and an unprobed register:** Germany, Czechia,
  Singapore, Poland.
- **4 produced a specific negative:** Netherlands (aggregate), Greece
  (sector-only), Portugal, Poland.
- **9 were not reached at all:** Thailand and Bulgaria blocked (403), Croatia
  and Slovakia behind SPA front ends, Romania, Denmark, Estonia, Sweden,
  Hungary, India, Egypt.

**Nine of twenty were never actually probed**, and that is the honest headline.
None of them belongs in Tier 4 on this evidence.

#### CORRECTION — Finland was ruled out on a sample of ONE

Recorded first as "fails, company-level", on the strength of **the first
record the API returned**: a financial holding company (`NACE 66190`) with an
empty street, a PO box and `c/o Suomen Säätiötilipalvelu Oy`. That is n=1, not
a random one, and the note even observed that a visiting-address type existed
before dismissing it anyway.

**Measured properly across 500 Helsinki companies:**

| | |
|---|---|
| Carry a real street address | **449 of 500 — 89.8%** |
| Address **type 1** (visiting) | 298 records, **298 with a street — 100%** |
| Address type 2 (postal) | 499 records, 379 with a street |
| PO box present | 109 records |

**So the stated reason for ruling Finland out was false.** Addresses are there.

**The real obstacle is composition, and it is a different objection:**

| NACE | of 500 |
|---|---|
| **68 — real estate** | **265 (53%)** |
| 46 — wholesale | 51 |
| **47 — retail** | **24 (4.8%)** |
| **56 — food & beverage** | not in the top 12 |
| **96 — personal services** | not in the top 12 |

Over half the register is property companies — `Kiinteistö Oy Espoon
Aallonrivi`, `Heiset Oy` — because in Finland every apartment building is
registered as a *Kiinteistö Oy* or *Asunto Oy*. **This is Philadelphia's
landlord-registration problem (79%) and D.C.'s residential-rental problem
(61%) in a third form**, and this project already filters both away by
category.

**Finland therefore stays in Tier 3 as UNRESOLVED, not Tier 4.** The open
question is whether filtering to NACE 47/56/96 yields **shop premises or head
offices** — the company-versus-premises question, which the composition
measurement does not answer either way. That is one probe, not a verdict.

**The lesson, which is this file's own rule turned on itself:** a negative
from a single non-random record is not a finding. The evidence-discipline
section demands two differently-shaped probes before recording a negative, and
this one had one record.

**Tier 3 continues** with rail measured and business unprobed: Vienna
(subway 35, tram 185 — deepest in the screen), Amsterdam/Rotterdam (14/46),
Singapore (13), Lisbon (10), Berlin (9/48), Stockholm (7/21), Santiago (7),
Bucharest (5/15), Sofia (4/24), Copenhagen (4/4), Bangkok (4/5), Helsinki
(4/26), Budapest (4/42), Hamburg (4), Prague (3/40), Athens (3), Naples
(3/3/3), Hyderabad (3), Kochi (1), Cairo (2) — plus tram-only Riga, Tallinn,
Zagreb, Bratislava, Poznań, Messina.

## MULTI-CITY candidate lists, and the Tier 2b rail screen — 2026-09-21

With ~80 page slots free and no RAM constraint (see
`scaling_thresholds.md`), slots are not scarce. **Verification is.** So each
passing country's *whole* set of rail cities is listed, not one representative.

### Countries by marginal-city cost

**One national source covers every city** — the second city costs a boundary
file and a rail check:

| Country | Rail cities | Source | Buckets |
|---|---|---|---|
| **Japan** | **10 confirmed** | 推奨データセット standard schema | 2 — no retail |
| **South Korea** | 6 have rail, **1 has data** — Seoul | 인허가 정보 (Seoul's portal) + 표준데이터 | 3, with coordinates |
| **France** | **6 confirmed** | SIRENE, Licence Ouverte 2.0 | 3 |
| **Taiwan** | 4 | 商業登記 by category | 3, no coordinates |
| **Mexico** | 3 | DENUE, SCIAN = NAICS | 3 |
| **Brazil** | **1 confirmed** (not 6) | CNPJ | 3, no coordinates |

**Multiple cities but bespoke per city** — each is its own integration:
**Spain** 6 · **Italy** ~4 (Milan verified) · **Canada** 3 remaining

**Single-city:** Singapore · Norway (Oslo) · Czechia (Prague) · Finland
(Helsinki) · Denmark (Copenhagen) · Israel (Tel Aviv) · Peru (Lima) · Chile
(Santiago) · Colombia (Bogotá/Medellín) · Thailand (Bangkok) · Bulgaria
(Sofia) · Romania (Bucharest) · **Ireland (Dublin) and Switzerland (Zurich),
both unprobed**

### The batched screen, run 2026-09-21

**Japan and Korea needed no GTFS at all** — their rail is one national file
each, already downloaded, so per-city counts came free:

| Japan | Stations | | Korea | Stations |
|---|---|---|---|---|
| **Tokyo** | **330** (Metro 181 + Toei 149) | | **Seoul** | **407** |
| **Osaka** | 133 | | **Busan** | 126 |
| **Nagoya** | 102 | | **Incheon** | 102 |
| **Sapporo** | 49 | | **Daegu** | 94 |
| **Yokohama** | 43 | | **Daejeon** | 22 |
| **Fukuoka** | 38 | | **Gwangju** | 20 |
| **Kyoto** | 32 | | | |
| **Kobe** / **Sendai** | 30 each | | | |
| **Hiroshima** | 22 (Astram) | | | |

Japan's municipal figures *understate* each metro area, because the private
railways are separate operators — Kintetsu 309, Meitetsu 295, Tobu 218,
Tokyu 110, Hankyu 104, Keio 75.

**France: all five remaining cities confirmed, so France has SIX.**

| City | Measured |
|---|---|
| **Lyon** | **subway 12, tram 18, funicular 4** |
| Marseille | subway 2, tram 3 |
| Lille | subway 2, tram 1 |
| Toulouse | subway 2, tram 1 |
| Rennes | subway 2 — *feed expired 20250629* |

**Spain: Valencia is large** — **subway 84, tram 37**. Sevilla's screen matched
the wrong operator (a Dos Hermanas bus company, 404) and is unresolved.

**Brazil collapses from 6 to 1.** Rio, Belo Horizonte and Porto Alegre all
return **bus only**, and Brasília, Recife and Monterrey matched no feed at all.
That is consistent with MetrôRio having been confirmed absent from the
catalogue earlier: **Brazil's metro operators are not in it.** São Paulo, whose
data came from GeoSampa rather than the catalogue, remains the only confirmed
Brazilian city — and the lesson repeats, since GeoSampa is a *city GIS portal*,
not a transit catalogue.

**Two parsing lessons from the national files.** Korea's per-city grouping by
address token **missed Daegu entirely** — its rows carry district names
(수성구, 달서구) rather than the city name, and only operator grouping found
its 94 stations. And the first Korean count was silently wrong because **XLSX
omits empty cells**: appending cells in document order shifted dates into the
address column. Read the cell `r` reference, not the order.

## MASTER CITY LIST — reordered 2026-09-22 after the Band D and D5 probes

> **The canonical copy now lives in
> [`docs/city_master_list.md`](city_master_list.md).** That file is current
> state and is rewritten as things change; **this file is the evidence trail**
> and is appended to. If the two disagree, this one wins and the list is stale.
> The copy below is kept in place so the evidence sections that follow have
> their summary beside them.

**14 built.** US (9): San Diego, San Francisco, Los Angeles, Chicago, New York,
Philadelphia, Miami, Boston, Washington D.C. Canada (5, complete): Vancouver
*(with Surrey)*, Montréal, Calgary, Edmonton, Toronto.

**48 candidates**, down from 54 — six were discarded on measured evidence this
round. Banded by **what is actually stopping each one.**

| Band | What is stopping it | Cities | Change this round |
|---|---|---|---|
| **A** | Nothing. Screening complete | **7** | — |
| **B** | One narrow question each | **3** | — |
| **C** | A geocoding leg — build work, not screening | **17** | **+1** Copenhagen promoted |
| **D** | Probed and ranked; see the four sub-tiers | **21** | **−7** |
| *Discarded* | Measured negative, each naming its evidence | *14* | **+6** |

### Band A — screening COMPLETE (7 cities, 5 countries)

Ordered by how little stands in the way.

| # | City | Business leg | What remains |
|---|---|---|---|
| 1 | **Guadalajara** 🇲🇽 | DENUE, SCIAN = NAICS, licence cleared | **Nothing** |
| 2 | **Madrid** 🇪🇸 | 148,814 open premises, 119,070 valid coords, CC BY 4.0 + binding general conditions | **Nothing** |
| 3 | **Seoul** 🇰🇷 | 197,276 premises, EPSG:5174, KOGL Type 1 | Build work — partial geocoding, Korean privacy pass |
| 4 | **Milan** 🇮🇹 | 28,131 premises 99.1% coords, all three buckets | Step 0 schemas for two new layers |
| 5 | **Mexico City** 🇲🇽 | Same DENUE | One licence call — ODbL share-alike on the station extract |
| 6 | **Barcelona** 🇪🇸 | 68,024 premises, CC-BY-4.0 | One residual — CAPTCHA-walled general notice |
| 7 | **Paris** 🇫🇷 | SIRENE, geolocated, LO 2.0 | Your architecture decision — national vs per-city |

### Band B — one narrow question each (3 cities)

**Valencia** 🇪🇸 (subway 84, tram 37 — the largest Spanish system measured) ·
**Bilbao** 🇪🇸 · **Málaga** 🇪🇸

Each needs its own register, since Spain is bespoke per city — but **two of the
three Spanish cities probed have had one**, which raises the prior sharply.

### Band C — viable, each needs a GEOCODING LEG (17 cities)

| Cities | Country | Business leg | Geocoding |
|---|---|---|---|
| **Tokyo**, Osaka, Nagoya, Yokohama, Sapporo, Fukuoka, Kyoto, Kobe, Sendai, Hiroshima *(10)* | 🇯🇵 | Premises-level food permits, CC BY, one national schema. **Two buckets — no general retail** | **Hardest met** — chōme/ban/gō, full-width numerals, `町字ID` 0% populated |
| **Taipei**, Kaohsiung, Taoyuan, Taichung *(4)* | 🇹🇼 | 商業登記 — premises, active/closed status, per-category assembly | Moderate — **NLSC geocoder is keyless** |
| **Oslo** *(1)* | 🇳🇴 | **152,060 sub-units**, `beliggenhetsadresse` (physical, not registered), NACE, open API no key | Moderate |
| **Copenhagen** *(1)* ↑ **new** | 🇩🇰 | **CVR `productionunits` — P-enheder each with their own `address`/`zipcode`/`city`**, plus `industrycode`/`industrydesc` on a NACE-style scheme (e.g. `475220 Detailhandel med byggematerialer`). Norway's shape, measured via `cvrapi.dk` | Moderate — **plus a free account**: `distribution.virk.dk` 401, `datacvr.virk.dk` 403, and `cvrapi.dk` itself is unofficial and search-by-name |
| **São Paulo** *(1)* | 🇧🇷 | CNPJ — trade name, address, CNAE | **Hard, past Toronto's scale** |

Japan is **ten cities from one schema** — the best marginal-city cost in the
screen — against the worst geocoding problem and a two-bucket ceiling. **Still
the biggest open decision in this list**, and a judgment call rather than a
probe.

### Band D — 21 cities, in four sub-tiers

#### D-a — one cheap question each (4)

| City | State |
|---|---|
| **Prague** 🇨🇿 ↑ | **`rzp.cz`, the *živnostenský rejstřík* (TRADE-licence register), is live** — the right shape, since Czech trade licences are issued per premises. Not ARES, which is the company register. **Best D lead after Copenhagen** |
| **Dublin** 🇮🇪 | `data.gov.ie` lists a **Valuation Office API**, but `api.valoff.ie` and `www.valoff.ie` both returned **000 across two attempts** — host down, so ASSERTED not measured. Question: does the Irish rateable register carry a **use category**, where the UK's NNDR did not? |
| **Zurich** 🇨🇭 | **Food confirmed** — `Gastwirtschaftsbetriebe`, premises-level, **GeoJSON**. No second bucket found; the national STATENT is aggregate |
| **Singapore** 🇸🇬 | API answers but its search is loose (*food establishment* → rainfall). Needs one controlled query. Suspected registered-office shaped |

#### D-b — rail ANSWERED, the business leg is the blocker (10)

Rail screened via OSM 2026-09-22. The `name`/`colour` rates are the invariant
that matters; **relation counts are upper bounds** — see the construction-filter
note below.

| City | Rail (OSM) | Business leg |
|---|---|---|
| **Hong Kong** 🇭🇰 | **126 rel**, 125 named, 117 coloured | **MEASURED NEGATIVE** on `data.gov.hk` — statistics tables only. Route left: **FEHD's licensed food premises list** (a department, not a portal) |
| **Santiago** 🇨🇱 | **30 rel**, all named + coloured, L1–L6 + L4A | **MEASURED NEGATIVE** on `datos.gob.cl` — `patentes comerciales` returns nothing at all. Municipal portals remain |
| **Rio de Janeiro** 🇧🇷 | **20 rel**, all named + coloured | Known: **CNPJ, no coordinates** → geocoding at São Paulo's scale |
| **Kuala Lumpur** 🇲🇾 | **14 rel**, all named + coloured | `data.gov.my` live but wrong endpoint; SSM is company-shaped |
| **Jakarta** 🇮🇩 | **9 operating** of 11 — the 2 `TB` relations are the **proposed** MRT East-West Line | `satudata.jakarta.go.id` live; stack unidentified |
| **Medellín** 🇨🇴 | 6 rel, all named, **only 2 coloured** — colours would need assigning by hand | ArcGIS stack — a shape this project handles |
| **Tel Aviv** 🇮🇱 | 6 rel — **but Green and Purple are under construction and OSM does not mark them**, so realistically **1** | `data.gov.il/api` 14 bytes; city portal **HTTP 472**, the documented IP refusal |
| **Hyderabad** 🇮🇳 | 6 rel, all named + coloured | India's trade licences are municipal; `data.telangana.gov.in` dead |
| **Lima** 🇵🇪 | 4 rel, all named + coloured | `www.datosabiertos.gob.pe` live, wrong endpoint |
| **Kochi** 🇮🇳 | 2 rel, named + coloured | Kerala LSG live (139 KB) |

#### D-c — genuinely UNREACHED, no finding either way (6)

**Tallinn** 🇪🇪 *(ariregister's fields are company-shaped — suggestive, unmeasured)* ·
**Stockholm** 🇸🇪 · **Budapest** 🇭🇺 *(both `adatportal.budapest.hu` and `opendata.budapest.hu` resolve nowhere)* ·
**Zagreb** 🇭🇷 · **Bucharest** 🇷🇴 ·
**Sofia** 🇧🇬 *(the 403 is a **stock Apache page**, not an IP block — so the browser is worth trying, a cheaper next step than it had)*

#### D-d — one cheap gate (1)

**Sevilla** 🇪🇸 — rail is **registration-gated, not absent**: Spain's National
Access Point answers **401**. The WMATA shape, a free account. Its business leg
still needs its own Spanish source.

### DISCARDED — 14 cities, each naming its evidence

| City | Why |
|---|---|
| **Berlin** 🇩🇪 ↓ **new** | CKAN on `datenregister.berlin.de`; **`Gaststätten` → 0**; the Gewerberegister is not open data |
| **Hamburg** 🇩🇪 ↓ **new** | Real CKAN is `suche.transparenz.hamburg.de` (9,145 datasets); `Gewerberegister` → 7 irrelevant hits; building-permit PDFs and planning polygons |
| **Naples** 🇮🇹 ↓ **new** | Only commercial dataset is **"per procedimento e Municipalità"** — aggregate |
| **Messina** 🇮🇹 ↓ **new** | SCIA/DIA ship GeoJSON but are business-*start notifications* — a flow, not a stock |
| **Helsinki** 🇫🇮 ↓ **new** | Addresses fine (89.8%) but composition is **53% real estate, 4.8% retail** |
| **Bogotá** 🇨🇴 ↓ **new** | **Fails on rail** — one unnamed-ref, zero-colour relation; its only mass transit is BRT |
| **Vienna** 🇦🇹 | GISA strips the street address by design |
| **Amsterdam / Rotterdam** 🇳🇱 | Register is aggregate |
| **Athens** 🇬🇷 | Sector-only |
| **Lisbon** 🇵🇹 | Specific negative |
| **Poznań** 🇵🇱 | Specific negative |
| **Riga** 🇱🇻 | Addressed but unclassified |
| **Bratislava** 🇸🇰 | No activity classification at all |
| **Cairo** 🇪🇬 | No open-data infrastructure |

Plus the no-urban-rail set (Winnipeg, Hamilton, Québec City, Halifax,
Mississauga, Ottawa, ~30 single-feed countries) and access-not-data (Russia,
Ukraine).

**GERMANY is a country-level negative**, on two cities measured independently at
two different portal hosts. **A row reading "not reached", "unprobed" or a
regional pattern is not a discard** — that rule went into `add-country` after
eleven cities were found sitting here on exactly those grounds.

#### D4 — the corrected-target re-probe

**D4 re-probed 2026-09-22 at the register each country actually keeps**, rather
than at a guessed open-data portal — which is where the previous pass failed.

| Country | Corrected target | Result |
|---|---|---|
| **Czechia** | **`rzp.cz`** — the *živnostenský rejstřík* (**trade-licence** register), not ARES the company register | **LIVE.** This is the right *shape*: Czech trade licences are issued per premises. The most promising D4 lead after Denmark. `api.golemio.cz` needs a key (401); `opendata.praha.eu` still serves HTML at its CKAN path |
| **Bulgaria** | `data.egov.bg`, body read rather than just the code | **403 is a plain Apache "Forbidden"** — no IP named, no Cloudflare Ray ID, no WAF marker |
| **Hungary** | `nyilvantarto.hu` | Live (3.1 KB). `data.gov.hu` resolves nowhere |
| **Croatia** | `pretrazivac-obrta.gov.hr` (obrtni registar) | Live but a 244-byte SPA shell. `opendata.zagreb.hr` dead |
| **Sweden** | `dataportal.se/api/datasets` | 404 — still the wrong path |
| **Romania** | `portal.onrc.ro` | Resolves nowhere |
| **Estonia** | `ariregister` `/en/open-data` | 404 — the working path is `/en/downloading-open-data`, already read: fields are **Registry code, Legal form, VAT number, Status, Address**, i.e. company-shaped |

> **CORRECTION — Bulgaria was lumped with the IP-refused hosts and should not
> have been.** This file's own rule is that an IP-level refusal **names your
> address or shows a WAF request id**, the way `data.go.th` and
> `opendata.tel-aviv.gov.il` both printed `50.47.238.226` back. Bulgaria's 403
> does neither: it is a stock Apache `403 Forbidden` page, 199 bytes, which is
> the **client-signature** case — exactly the one where *the browser is worth
> trying*. Untested in a browser, so Sofia stays open with a cheaper next step
> than it had. Two sessions recorded "403, consistent, plausibly IP" without
> reading the 199 bytes.

> **SUPERSEDED 2026-09-22 — the browser was tried, and the inference above was
> wrong.** `data.egov.bg` returns **the same 403 in a real browser**, and
> DNS-over-HTTPS resolves it fine (213.91.191.234), so the host is up and
> refusing us deliberately. **The 199 bytes were a red herring: a refusal's
> cosmetics say nothing about its cause.** The correction above was right
> that the earlier sessions had not read the body, and wrong to read a
> diagnosis out of it — replacing one unread assumption with one over-read
> one. Only trying it settled it.
>
> **🇧🇬 BULGARIA IS NOW CLOSED, and on data rather than on access.**
> `data.europa.eu`'s SPARQL endpoint harvests `data.egov.bg` from a different
> host, so **11,635 Bulgarian datasets** (ids 3–23,557) were enumerated
> without touching the blocked origin. **141 municipal
> `Регистър на търговските обекти`** — the exact premises register this
> project needs — exist across ~50 municipalities, plus **72** food-and-
> entertainment registers. **Sofia's 76 datasets include neither.**
>
> The structural finding is the durable one: **every Bulgarian municipality
> publishing this register is a small town, and Sofia is the country's only
> metro city.** The data exists where there is no rail; the rail exists where
> there is no data. Full details, including the Virtuoso timeout ladder and
> the `dct:spatial`-means-coverage trap, are in `add-country` §3 and in
> `docs/city_master_list.md`'s Sofia section.

#### D5 — rail/GIS group: REACHABILITY ONLY, no layer probed (11 cities)

**Hong Kong · Jakarta · Kuala Lumpur · Rio de Janeiro · Tel Aviv · Lima ·
Bogotá · Medellín · Santiago · Hyderabad · Kochi**

All were originally ruled out against a *transit catalogue*, which is the wrong
source. 20 of 22 national-mapping-agency hosts answered — **and every one
returned a landing page**, which `probe_geodata.py` labels a route rather than
a finding. Only `ign.gob.pe` (TLS) and `geoportal.regionlima.gob.pe` failed.
`jupem.gov.my` needed the curl fallback after a `requests` SSLError, **the
fourth time Python's TLS has reported a live government host as dead**.

Two of these carry known business legs already, so only rail is open:
**Rio** (Brazil, CNPJ — no coordinates, so a geocoding leg) and **Tel Aviv**
(Israel's register, previously IP-refused).

#### D5 RAIL SCREENED VIA OSM, 2026-09-22 — all 11, and the method transfers

Rather than hunt eleven mapping-agency portals for a layer, the rail question
was put to **OSM**, the route CDMX validated at 195/195 stops exact. Route
relations per city, all four urban modes, control-free because an empty result
is unambiguous:

| City | Relations | named | colour | Modes | Refs |
|---|---|---|---|---|---|
| **Hong Kong** 🇭🇰 | **126** | 125 | 117 | subway 82, light_rail 31, tram 12, monorail 1 | 1–14 … |
| **Santiago** 🇨🇱 | **30** | 30 | 30 | subway 30 | L1 L2 L3 L4 L4A L5 L6 |
| **Rio de Janeiro** 🇧🇷 | **20** | 20 | 20 | subway 6, light_rail 2, tram 12 | 1 2 3 4, ESFECO |
| **Kuala Lumpur** 🇲🇾 | **14** | 14 | 14 | light_rail 8, subway 4, monorail 2 | AG KJ MR SP … |
| **Jakarta** 🇮🇩 | **11** | 11 | 10 | light_rail 6, subway 4, tram 1 | BK CB LRT M TB |
| **Medellín** 🇨🇴 | 6 | 6 | **2** | subway 4, tram 2 | A B T-A |
| **Tel Aviv** 🇮🇱 | 6 | 6 | 6 | light_rail 6 | R1 R2 R3 |
| **Hyderabad** 🇮🇳 | 6 | 6 | 6 | subway 6 | 1 2 3 |
| **Lima** 🇵🇪 | 4 | 4 | 4 | subway 4 | L1 L2 |
| **Kochi** 🇮🇳 | 2 | 2 | 2 | subway 2 | I |
| **Bogotá** 🇨🇴 | **1** | 1 | **0** | subway 1 | *(none)* |

> **THESE ARE UPPER BOUNDS, NOT OPERATING-LINE COUNTS** — and the filter that
> was supposed to fix that only half works. See "The construction filter" below.
> Treat every row as "at most this many".

**What the screen does settle**, because these are robust to the caveat:

- **Hong Kong, Santiago, Kuala Lumpur and Rio have large, mature, well-tagged
  systems** — near-100% `name` and `colour`, which is the invariant that
  matters. Hong Kong's 126 relations and Santiago's 30 are not construction
  artefacts at that scale.
- **Bogotá fails on rail** and can leave D5 — one unnamed relation, no colour,
  and its only mass transit is BRT.
- **Medellín is the one with a tagging gap**: 6 relations, all named, but only
  **2 carry a colour**. This project draws every line with a legend entry, so
  Medellín would need colours assigned by hand rather than taken from source —
  the opposite of CDMX, where the real livery came free.

**So D5's rail leg is largely answered and the business leg is now the
binding question for all of them** — which is where the next pass should go,
not back to the mapping agencies.

#### The construction filter — RAN, and its failure mode is the finding

Ran against the four suspect cities. **It flagged unbuilt routes in one of
four, and returned zero in the other three — including two where unbuilt lines
are known to exist.**

| City | Total | Flagged | Result |
|---|---|---|---|
| **Jakarta** 🇮🇩 | 11 | **2** | Both `TB`, *"East-West Line (Tomang → Medan Satria)"*, tagged **`proposed`**. **9 operating**, refs `BK` `CB` `LRT` `M` |
| **Tel Aviv** 🇮🇱 | 6 | **0** | `R1 R2 R3` all tagged as ordinary `light_rail` |
| **Bogotá** 🇨🇴 | 1 | **0** | Its one relation is not construction-tagged either |
| **Rio** 🇧🇷 | 20 | **0** | refs `1 2 3 4 ESFECO`, none flagged |

> **A filter returning zero does not mean "nothing to flag" — it can mean "this
> convention is not used here", and the two are indistinguishable from the
> result alone.** Tel Aviv is the proof: its Red Line opened in 2023 and the
> Green and Purple lines are **still under construction**, yet OSM carries all
> three as plain `light_rail` with no status marker. The filter passed them
> silently. Same for Bogotá, whose Línea 1 is years from opening.
>
> So **Tel Aviv and Bogotá keep their upper-bound label** despite a clean
> filter run. Rio's zero is probably honest — Lines 1, 2 and 4 plus the VLT and
> the Santa Teresa tram is a plausible 20 — but it is *unconfirmed* for exactly
> the same reason. Resolving these needs a different signal: whether each
> route's member **ways** are `railway=construction` rather than `railway=subway`,
> which is a heavier query, or simply real-world knowledge.

**One guess corrected by running it:** I had recorded Jakarta's `TB` as
"plausibly TransJakarta, i.e. BRT". It is not — it is the **proposed MRT
East-West Line**. Right conclusion (exclude it), wrong reason, and only the
probe distinguished them.

**Two transport lessons, both mine:**

- **`overpass-api.de` returns HTTP 406 to every request from here** — not busy,
  *rejecting*. It fronts on `lambert.openstreetmap.de`, and something in that
  proxy dislikes this client. I read the failures as "mirrors busy" twice while
  `/api/status` reported free slots on both hosts. **kumi.systems has done all
  the work in this session**, and the fix was mirror order, not waiting.
  `overpass.osm.jp` is worse: its TLS certificate is **expired**.
- **`PYTHONIOENCODING=utf-8` is not optional on this machine.** Jakarta's result
  arrived correctly and then crashed the print on the `→` in a route name, under
  cp1252. Fourth time this session.

#### D5 BUSINESS LEG — first pass on all eleven, 2026-09-22

**No D5 city has a confirmed premises-level register yet.** Two produced
measured negatives; the rest have live portals on the wrong endpoint, which is
a fact about the probe, not the data. Recorded so the next pass starts in the
right place per city rather than re-deriving it.

| City | Portal state | Verdict |
|---|---|---|
| **Hong Kong** 🇭🇰 | `data.gov.hk` **is CKAN, control 0** | **MEASURED NEGATIVE on this portal.** `restaurant` returns *Restaurant Receipts and Purchases — Table 625-68003*, `licence` returns *Municipal services licences — Table 990-92201*, `shop` returns public housing estates. All **statistics tables**, the aggregate trap. Note this does not even support the earlier "food-only ceiling" claim — there is no food *premises* register here either. **Unprobed route: FEHD's licensed food premises list**, which is where HK's actual register lives |
| **Santiago** 🇨🇱 | `datos.gob.cl` **is CKAN, control 0** | **MEASURED NEGATIVE so far.** `establecimientos` (115) returns health and educational establishments; **`patentes comerciales` — the correct Chilean term for a commercial licence — returns no answer at all.** Municipal portals still the route, and `datos.santiago.cl` resolves nowhere |
| **Bogotá** 🇨🇴 | CKAN, control 0 | `establecimientos` 88 — pharmacies, tourist lodging, universities. One lead: ***Dinámica empresarial. Bogotá D.C.*** in DXF/ESRI REST/GPKG. **Moot: Bogotá fails on rail** |
| **Kuala Lumpur** 🇲🇾 | `data.gov.my` live, 150 KB, **not CKAN** | Wrong endpoint. SSM (the companies commission) is live at 422 KB and is the likely register — company-shaped, so expect the registered-office failure |
| **Rio** 🇧🇷 | `data.rio` live, 96 KB, **not CKAN** | Brazil's leg is already known: **CNPJ, premises-level, no coordinates** → geocoding at a scale past Toronto's |
| **Jakarta** 🇮🇩 | `satudata.jakarta.go.id` live (19 KB); `data.jakarta.go.id` **dead** | Stack unidentified |
| **Lima** 🇵🇪 | `www.datosabiertos.gob.pe` live, 88 KB, **not CKAN at that path** | The `www.` lesson already applied; now needs the catalogue endpoint |
| **Medellín** 🇨🇴 | `medellin.gov.co/mapas` → **ArcGIS** | ArcGIS REST is a known shape for this project; cheap next probe |
| **Hyderabad / Kochi** 🇮🇳 | `data.gov.in` live but 1.2 MB and **not CKAN at that path**; `data.telangana.gov.in` **dead**; Kerala LSG live (139 KB) | India's trade-licence registers are municipal, so the state/city portals are the route |
| **Tel Aviv** 🇮🇱 | `data.gov.il/api` returns **14 bytes**; `opendata.tel-aviv.gov.il` returns **HTTP 472** | 472 is the same non-standard status recorded earlier when that host **printed our IP back** — consistent with the IP-level refusal already documented. **The browser will not help** |

**The pattern worth carrying:** two CKAN portals answered cleanly with working
controls and both returned **statistics tables rather than registers**. That is
the aggregate trap appearing at *national* portals specifically — the same
reason `datos.gob.cl` and `data.gov.hk` look rich and yield nothing. The
city-first lesson applies again, and for Hong Kong the named next step (FEHD)
is a *department*, not a portal.

#### Band D after ranking

| | Cities |
|---|---|
| Promote to a real candidate | **1** — Copenhagen |
| One cheap question | **4** — Dublin, Singapore, Sevilla, Zurich |
| Measured negative → discard | **5** — Berlin, Hamburg, Naples, Messina, Helsinki |
| Genuinely unreached | **7** |
| Rail/GIS, reachability only | **11** |

**The honest headline: Band D yielded one real candidate.** That is a low
strike rate, and it is the expected one — Bands A to C already hold everything
that screened well. The value of the pass was mostly in *closing* things:
Germany retired on evidence, and five cities moved from "unprobed" to
"measured negative", which is what stops them being re-probed a third time.

### THE NINE-ITEM SWEEP, run 2026-09-22 — three resolved, three negative, three partial

Every open probe from the banding above, run as one pass. **Headline: Madrid
and Milan both promote to Band A, which makes Spain and Italy real multi-city
countries rather than one-city ones.**

| # | Item | Verdict |
|---|---|---|
| 1 | Barcelona's licence | ✅ **CC-BY-4.0** |
| 2 | Sevilla's feed | ❌ dead at all six addresses |
| 3 | Milan Personal services | ✅ **reachable, with GeoJSON** |
| 4 | Germany / Czechia / Singapore | ❌ Berlin measured negative; CZ + SG need another route |
| 5 | Madrid's own source | ✅ **148,814 open premises, all three buckets** |
| 6 | Dublin / Zurich | ⚠️ Dublin negative so far; Zurich one bucket only |
| 7 | Naples / Messina | ❌ Naples aggregate; Messina flow-shaped |
| 8 | Seven never reached | ⚠️ still not reached — wrong hosts, 403s |
| 9 | Seven mapping agencies | ⚠️ 20/22 hosts live, but all landing pages |

#### Item 5 — MADRID PASSES, and it is bigger than Barcelona

`datos.madrid.es` **is** CKAN, at the bare host — the earlier "unreachable"
was a wrong path (`/egob`), i.e. a fact about the guess. Dataset
**`200085-0-censo-locales`**, *Censo de locales, sus actividades y terrazas de
hostelería y restauración*, downloaded and counted:

| | MEASURED |
|---|---|
| Rows (resource `200085-5`, the locales+actividades join) | **225,667**, 47 columns |
| `desc_situacion_local` | **100%** — Abierto 159,835 · Cerrado 40,407 · Baja 12,557 · Uso vivienda 8,486 · Baja Reunificación 4,382 |
| Open + classified + coordinates | **148,814** (93.1% of Abierto) |
| `rotulo` (shop sign) on those | **100%** |
| Classification | **three levels** — `desc_seccion` → `desc_division` → `desc_epigrafe` |
| Districts | **22**, i.e. all of them |
| CRS | **EPSG:25830** (ETRS89 / UTM 30N) |
| Encoding / delimiter | UTF-8 BOM, **semicolon** |

**All three buckets, in one file:** COMERCIO 45,951 (Retail) · HOSTELERÍA
27,932 (Food) · OTROS SERVICIOS 14,887 (Personal services — SERVICIO DE
PELUQUERIA 6,012, CENTRO DE ESTETICA 3,058). Madrid is **2.2× Barcelona's
68,024** and needs no geocoding.

> **A coordinate column can be 100% populated and still invalid.**
> `coordenada_x_local` and `coordenada_y_local` are non-empty on every one of
> the 148,814 rows — and **29,744 of them (19.99%) are a literal `0`.**
> Projected from EPSG:25830 that is a point in the Atlantic off West Africa,
> which on a station-radius map would silently vanish rather than error.
> **Genuinely mappable: 119,070.**
>
> **`add-city` Step 0 already requires this check, and it named this exact
> failure** — *"A populated field can still be corrupt - Los Angeles' registry
> had ~9% bad coordinates (longitude copied from latitude, (0,0), whole-degree
> placeholders)"*. So this is corroboration, not a new rule: **Madrid is the
> second city with literal `(0,0)` rows, at 20% against LA's 9%.** Worth
> recording because it shifts the prior — two of the three pre-geocoded
> registries measured at this depth had the same defect, so a bounding-box
> count belongs in every Step 0 rather than being reserved for suspicion. The
> one thing to carry forward that the LA note does not say: at 20% this would
> have moved Madrid's headline number by a fifth, so the check has to run
> **before** a city's density is quoted, not after.

#### Item 3 — MILAN'S THIRD BUCKET EXISTS

`dati.comune.milano.it`, control-verified (nonsense term = 0):

| Dataset | Bucket | Formats |
|---|---|---|
| **Attività artigianali: servizi alla persona** (parrucchieri, estetisti…) | **Personal services** | CSV, **GEOJSON**, JSON |
| **Attività commerciali: esercizi di vicinato in sede fissa** | **Retail** | CSV, **GEOJSON**, JSON |
| Attività artigianali: settore alimentare · panificatori | Food | CSV, **GEOJSON**, JSON |

GeoJSON means coordinates ship with it. **Milan's one blocker is closed and it
is a three-bucket city.** Schemas not yet counted — that is `add-city` Step 0,
not screening.

#### Item 1 — BARCELONA IS CC-BY-4.0, read from the API because the portal is CAPTCHA-walled

`opendata-ajuntament.barcelona.cat` serves **hCaptcha** to the browser on
`/en/avis-legal`, `/ca/avis-legal` and `/es/aviso-legal` alike (11,769 b,
"PLEASE PROVE THAT YOU ARE HUMAN"). This project does not defeat CAPTCHAs, so
the legal notice was not read that way. **Its CKAN API is not walled**, and it
declares the licence per dataset:

```
"Census of premises on the ground floor intended for economic activity"
  license_id  = "CC-BY-4.0"
  license_url = "https://creativecommons.org/licenses/by/4.0/"
```

Same on the activity-code lookup table. **And it is a deliberate choice, not a
portal default:** `license_list` offers CC-BY-ND and CC-BY-NC — the two that
would forbid this project — so Barcelona picked the permissive one from a menu
that contained restrictive options.

**One residual, and it is the step this project most often skips:** what the
dataset page incorporates **by reference** is exactly what hid Philadelphia's
prohibition, and the general `avis-legal` page is the thing behind the CAPTCHA.
The per-dataset declaration is MEASURED; the general notice is UNREAD. Reading
it needs a human solving one challenge — an owner action, not a Claude one.

#### Item 2 — Sevilla is dead at every address a feed has

Six tried, applying the CDMX rule that a feed has at least three:

| Address | Result |
|---|---|
| `files.mobilitydatabase.org/mdb-2781/…` | **403** (XML error body) |
| `files.mobilitydatabase.org/mdb-latest/mdb-2781.zip` | **403** |
| `storage.googleapis.com/…mdb-latest…2781.zip` | **404** |
| `metro-sevilla.es/sites/default/files/gtfs/google_transit.zip` | **404** (HTML) |
| `metrodesevilla.es/gtfs/google_transit.zip` | **000** |
| `metro-sevilla.es/gtfs.zip` | **000** |

The two **403s are new information**: previously recorded as "the mirror 404s",
but `files.mobilitydatabase.org` now *refuses* rather than missing.

> **FOLLOWED UP the same day, and the first framing was too broad.** See
> "The Mobility Database moved its files" below. `files.mobilitydatabase.org`
> is 403 **host-wide** — but the `mdb-latest` bucket on
> `storage.googleapis.com` is a **different host and still public**, so
> "every feed sourced that way" was wrong. And Sevilla is **not dead**: the
> catalogue's own record gives a route never tried here — Spain's National
> Access Point — which answers **401**, i.e. registration-gated rather than
> missing.

#### Items 4, 6, 7 — the negatives, each with a working control

- **Berlin — MEASURED NEGATIVE.** `daten.berlin.de`'s CKAN API is on
  **`datenregister.berlin.de`** (the public site is not the API host).
  Control = 0. `Gewerbe` returns 18 hits, all broadband coverage and
  electricity standard-load profiles; **`Gaststätten` returns 0**; `Betriebe`
  returns 107, being swimming pools and parliamentary papers. Berlin does not
  publish its Gewerberegister as open data. Germany's route existed; the
  register is not on it.
- **Naples — MEASURED NEGATIVE, the aggregate trap.** `dati.comune.napoli.it`
  is CKAN, control 0. Its only commercial dataset is *Apertura e cessazione
  attività commerciali* — **"per procedimento e Municipalità"**, i.e. counts
  per procedure per district. Everything else is Polizia Locale enforcement
  activity.
- **Messina — flow, not stock.** *Segnalazione Certificata Inizio Attività
  (SCIA)* and *Denuncia Inizio Attività (DIA)* ship **GEOJSON/KML** — but they
  are business-*start notifications*, a flow. Mapping them shows where
  businesses opened, not what is there now. *Elenco imprese Messina* is
  company-level (share capital). Italy stays a Milan-only country.
- **Dublin — negative so far.** `data.gov.ie` control 0. `valuation` 76 →
  Valuation Office API plus census tables; `commercial rates` 122 → PSRA
  *Commercial Leases* register (leases), Local Property Tax statistics
  (aggregate); `retail` 55 → Core Retail *Area* polygons and central-bank
  interest rates. `data.smartdublin.ie` adds nothing premises-shaped. **The
  Valuation Office API is the one live lead** and is the Irish analogue of the
  UK's NNDR, which this project already rejected for carrying no category —
  so the single question is whether the Irish one has a use category. Unprobed.
- **Zurich — one bucket, and one false friend.** `Gastwirtschaftsbetriebe`
  (hospitality licensed by the Stadtpolizei) is genuine premises data with a
  **GeoJSON** endpoint — Food only. **`Betriebliche Bestandeskarten` is NOT a
  business inventory**: read its description and it is *forest stand maps*
  (Bestockung, Waldgesellschaften). A title-level read would have recorded a
  three-bucket pass. And **Switzerland's national route is aggregate** —
  opendata.swiss's STATENT / Betriebszählung / Arbeitsstätten are all "nach
  Branche / Grössenklasse / Kanton / Gemeinde / Quartier". So the city-first
  lesson pays off a **fifth** time, but only to one bucket.

#### Items 8 and 9 — still open, and honestly so

**Item 8: the seven were still not reached**, and mostly because my hosts were
wrong, which is not a finding about the data. `data.kk.dk`,
`opendata.budapest.hu` and `data.gov.ro` resolve nowhere; `data.egov.bg`
returns **403** (the same refusal recorded before); `dataportalen.stockholm.se`,
`avaandmed.eesti.ee` and `data.gov.hr` are live but not CKAN at the guessed
path — Estonia's API answers *"There is an API here!"* without documentation at
that URL. `opendata.praha.eu` serves HTML at its CKAN path, so Prague needs its
real API. **None of these is a negative. They stay in Band D unchanged.**

**Item 9: 20 of 22 mapping-agency hosts are reachable and every one returned a
landing page.** That is a *route*, not a finding — `probe_geodata.py` says so
in its own output. Only two failed: `ign.gob.pe` (TLS, curl rc=60) and
`geoportal.regionlima.gob.pe` (connection refused). Notably **`jupem.gov.my`
needed the curl fallback** (requests SSLError, 232 KB via curl) — the fourth
time Python's TLS has reported a live government host as dead. Finding the
actual layer on each portal is the next pass.

### THE MOBILITY DATABASE MOVED ITS FILES — and the catalogue repo is the durable route

Followed up 2026-09-22 because "the mirror 404s" turned out to be a 403. The
result corrects **three** things, one of them a Band A entry.

**What is actually broken.** `files.mobilitydatabase.org` returns
`<Error><Code>AccessDenied</Code></Error>` for **every** path tried — the host
root, `mdb-<id>/...` and `mdb-latest/...`, across CDMX, Guadalajara, Sevilla
and Toronto alike. That is an object-store ACL denial, **not** an IP block: the
body names no IP and carries no WAF id, which by this file's own rule (a block
page that prints your address is IP-level) makes it an authentication wall.
`api.mobilitydatabase.org` answers **413 Request Entity Too Large** on every
path including bare GETs, which is its own kind of broken.

**What still works, and why "every feed sourced that way" was wrong.** The
`mdb-latest` mirror this project used to unblock CDMX is on
**`storage.googleapis.com`**, a different host, and it is **still public** —
Guadalajara downloaded from it cleanly (2,542,046 b). The earlier 404 there was
a **wrong filename guess** (`es-andalusia-metro-de-sevilla…` for the real
`es-andalusia-seville-metro-de-sevilla…`), i.e. a fact about the guess again.

**The durable route is the catalogue's GitHub repo, which nobody here had
used.** `MobilityData/mobility-database-catalogs` is public, and each feed's
JSON carries the **agency's own** `urls.direct_download` plus the GCS
`urls.latest`. Reading the repo tree (3,555 blobs) is one request and gives
every feed's real addresses without touching the files host at all. **This
should be the first stop in the next rail screen**, not the files host.

| Feed | Route | Result |
|---|---|---|
| **Guadalajara** `mdb-2366` | GCS `mdb-latest` | ✅ **200, 2.54 MB** |
| Guadalajara | agency `datos.jalisco.gob.mx` | 000 |
| **CDMX** `mdb-3126` (SEMOVI, the *combined* feed) | GCS `mdb-latest` | **404** |
| CDMX `mdb-3126` | agency `datos.cdmx.gob.mx` | **000** |
| CDMX `mdb-1099` | agency `s3.amazonaws.com/setravi` | **403** |
| **Sevilla** `mdb-2781` | **`nap.transportes.gob.es/api/Fichero/download/1583`** | **401 — gated, not absent** |

**Correction 1 — CDMX drops OUT of Band A.** Every one of its four routes is
dead: the city portal, the S3 bucket, the GCS mirror and the files host. The
"MEXICO CITY IS UNBLOCKED" finding above was true when made and is **no longer
true**. Mexico is a one-city country again until a route reappears.

**Correction 2 — Guadalajara is confirmed, with line geometry.** Screened from
the downloaded feed: **3 urban-rail routes** at `route_type 0` — *Línea 1
Periférico Sur–Auditorio*, *Línea 2 Juárez–Tetlán*, *Línea 3 Arcos Zapopan–
Central Camionera* — **12,231 stops, 100% with coordinates, and `shapes.txt`
present**, so this project's every-line-gets-drawn-and-labelled invariant is
satisfiable. Guadalajara stands alone in Band A for Mexico.

**Correction 3 — Sevilla was recorded dead and is actually registration-gated.**
Spain's **National Access Point** (`nap.transportes.gob.es`) is the publisher
of record for `mdb-2781` and answers 401. That is the WMATA shape — a free
account the owner can create — rather than an absence. It moves from "out" back
to Band D with a named, cheap blocker.

**A note on `mdb-3126` worth carrying forward.** The catalogue lists a CDMX feed
this project had never seen, covering *Metro, Metrobús, Tren Ligero,
Ferrocarriles Suburbanos, Trolebús, Cablebus and Pumabús* together — a better
feed than `mdb-1099` (*corredores concesionados*, i.e. bus corridors) which is
what the earlier "subway 12" screen actually used. **If CDMX comes back, use
3126.** Worth re-checking `datos.cdmx.gob.mx` periodically, since the whole
domain has been intermittent rather than permanently dead.

### MEXICO NATIONWIDE PROBE, 2026-09-22 — the business leg is national, the rail leg is the wall

Run as a **GIS** probe rather than a feed probe, since that framing flipped
Japan, Korea and Taiwan, and since DENUE already covers every Mexican city with
coordinates and a cleared licence. **Only rail geometry is missing — and it is
missing for every Mexican city except Guadalajara.**

**Mexican cities with actual urban rail** (BRT excluded, which rules out Puebla,
Mérida and León): **CDMX** — Metro 12, Tren Ligero, Trolebús, Cablebús,
Suburbano; **Guadalajara** — Tren Ligero 3, *already confirmed*; **Monterrey** —
Metrorrey 3.

| Route | Result |
|---|---|
| **INEGI** (portal, mapas, datos abiertos, RNC, temas) | All reachable. Its site search returned 108 results for *vías férreas* that were all **public-security censuses** — the term was not applied, and no rail layer was surfaced by this route |
| `gaia.inegi.org.mx` (Mapa Digital web services) | 200 but **0 bytes** |
| **SICT / ARTF** | Portals answer with ~1 KB shells; `geoportal.sct.gob.mx` **unreachable** |
| `datos.gob.mx` | Live, but **not CKAN** at `/busca/api/3/...` |
| **Every `*.cdmx.gob.mx`** — datos, portal, sig, adip, metro, semovi | **All time out** |
| **`ecobici.cdmx.gob.mx`** | **200, 152 KB** |
| `datos.nl.gob.mx` (Nuevo León) | Live — and a **WordPress brochure site** (`wp-content`, `portfolio_page`, `comments/feed`). Not a data portal |
| `datos.monterrey.gob.mx` | 200, **1 KB** shell |
| Internet Archive (for an archived CDMX `gtfs.zip`) | **429, then "Temporarily Offline"** — the archive itself is down |
| GitHub, official CDMX orgs | `SEMOVI-CDMX`, `datos-cdmx`, `LabCDMX` **do not exist**; `CDMX-ADIP` and `adip-cdmx` have **0 repos** |

**The `ecobici` result is the useful one.** It is the single host on
`cdmx.gob.mx` that answers, which means **the network path from here is fine and
the other hosts are individually down** — not a domain-wide block, not an
IP-level refusal. That makes CDMX a *retry* candidate rather than a permanent
loss, and it corrects the earlier "every `*.cdmx.gob.mx` host times out, which
is a more durable finding than one portal being down" — the domain is not
uniformly dead.

**Monterrey is a real negative and a cheap one.** The state's "open data"
portal is a WordPress site publishing PDFs and statistics pages; there is no
catalogue, no API, and no Metrorrey data publication. Monterrey was previously
recorded only as "not in the catalogue under any of `monterrey`, `metrorrey`,
`nuevo león`" — this is the stronger finding, reached at the publisher.

**Third-party GTFS mirrors exist and are not acceptable.** A GitHub search finds
`CarlosGiles/gtfs-cdmx`, `CelesteBJ/gtfs_cdmx` and others. These are the same
shape as **Dubai's catalogue entry — "an anonymous personal GitLab job
artefact" — which this project already rejected.** Using one would mean
publishing a city's transit geometry on the authority of an individual's
untracked repository, with no licence and no provenance. Consistency says no.

#### What is actually left, and one of the three is a decision rather than a probe

1. **Retry CDMX's hosts.** They are individually down, not blocked, and this
   project has already been wrong once by recording a transient outage as a
   durable finding (`data.go.kr`, 21 s timeouts from two networks, 200 an hour
   later). Cheap, and it is the route that yields `mdb-3126` — the SEMOVI feed
   covering Metro, Metrobús, Tren Ligero, Suburbanos, Trolebús and Cablebús
   together.
2. **Retry the Internet Archive** for the archived `gtfs.zip`, once the archive
   is back up. Untested rather than ruled out.
3. **Decide whether OpenStreetMap is an acceptable source for rail geometry.**
   **This is an owner decision, not a measurement**, and it is the only one that
   unblocks CDMX *and* Monterrey *and* every future city at once.

   For: CDMX's Metro and Monterrey's Metrorrey are both comprehensively mapped;
   the data is ODbL, and **this project already displays OSM attribution on
   every map**, so the licence adds no new obligation. Against: it is community
   rather than agency data, so it is not authoritative in the way a published
   feed is, and this project's invariant that **every drawn line carries its
   real public name** would need verifying per city rather than being taken from
   `routes.txt`.

   It is a genuine change of sourcing practice — agency data for the transit
   leg had been the rule for every city built to that point — so it is flagged
   here rather than assumed either way.

   **UPDATE 2026-09-22: the change happened.** Mexico City and Guadalajara
   draw their rail from OpenStreetMap, and Madrid from CRTM's ArcGIS feature
   services rather than its feed. So this is no longer a proposal to weigh but
   a practice with three instances and its own skill (`.claude/skills/osm-rail/`)
   and its own subsection in `data_sources.md`. Noted because the paragraph
   above reads as a live question and is a settled one; it said "all fourteen
   built cities" while there were sixteen.

### CDMX FROM OSM — approved as a per-city exception, and it PASSES the invariants

Owner decision 2026-09-22: use OpenStreetMap for CDMX's rail leg specifically,
**keep agency data as the default**, and treat this as a documented per-city
exception rather than a new rule. Measured the same day.

**Scope, by this project's own mode rules.** Metro (subway) and Tren Ligero
(light_rail) count. **Metrobús is BRT, Trolebús is a trolleybus, Cablebús is an
aerial gondola, and Tren Suburbano is commuter rail** — all excluded, the same
way route_type 109 / S-Bahn was excluded for Berlin.

**Invariant 1 — every drawn line carries its real public name.** PASS, and
better than most GTFS feeds:

| | MEASURED |
|---|---|
| Route relations | **26** = 12 Metro lines × 2 directions + Tren Ligero × 2 |
| Metro line refs | **1–9, A, B, 12** — exactly Metro CDMX's twelve |
| `name` | **100%** — e.g. `Línea 1 (Pantitlán → Observatorio)` |
| `ref` | **100%** |
| **`colour`** | **100%**, and they are the real livery — `#F04E98` L1 pink, `#005EB8` L2 blue, `#FFD100` L5 yellow |
| `operator` | `Sistema de Transporte Colectivo` |

**Invariant 2 — line geometry exists.** PASS. **26/26 relations carry geometry,
6,468 coordinate points**, from 131 (Línea 4) to 543 (Tren Ligero).

**The decisive validation — stop counts against Metro CDMX's published figures,
line by line:**

| Línea | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | 12 | **Total** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OSM | 20 | 24 | 21 | 10 | 13 | 11 | 14 | 19 | 12 | 10 | 21 | 20 | **195** |
| Official | 20 | 24 | 21 | 10 | 13 | 11 | 14 | 19 | 12 | 10 | 21 | 20 | **195** |
| Δ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

**Exact, every line, zero deltas.** The station layer is 177 nodes (159 subway +
18 light rail), **100% named and 100% coordinated**. An earlier read of "159 vs
163 official" was comparing distinct *nodes* against Metro's distinct-station
count; the like-for-like comparison is stop memberships per route, and it is
perfect.

> **TRAP, and it would cost a quarter of the system: 42 of the 159
> `station=subway` nodes carry NO `operator` tag.** Filtering stations by
> `operator="Sistema de Transporte Colectivo"` returns 117, silently dropping
> 42 — Gómez Farías, Zaragoza, Merced, Sevilla, Universidad and 37 others.
> **Filter on `station=subway`, never on `operator`.** This is the community-data
> risk in its concrete form: the tagging is complete but not uniform, so a
> filter that would be safe against an agency feed is not safe here. Also
> present in the bbox: 12 `railway=station` nodes with no `station=` tag at all,
> and 2 tagged `monorail`.

#### The licence catch, which is NOT the one expected

OSM is ODbL, and this project **already displays OSM attribution on every map**,
so attribution adds nothing new. The real question is share-alike, and it turns
on what gets committed:

- **`heatmap.html` is a Produced Work.** ODbL asks for attribution on it, which
  is already satisfied. No share-alike.
- **`outputs/<city>/excluded_stations.csv` is not.** It commits
  `station,latitude,longitude,lines` — a structured extract of the database, so
  it is plausibly a **Derivative Database**, and ODbL's share-alike then applies
  to it.

The repository is **already structurally ready for this**: `LICENSE` disclaims
MIT over everything in `outputs/` and says in terms that it "could not" license
that data, because it is derived from third-party sources. But a disclaimer is
not an offer, and **ODbL requires the derivative database to be offered under
ODbL** — a positive obligation the agency-sourced cities do not carry. (Named,
not counted: "the fourteen agency-sourced cities" happened to be right on
2026-09-22 — sixteen built, two from OpenStreetMap — and would have been wrong
on the next build either way.)

**Not resolved here, per `read-licence`'s rule not to settle an ambiguity in
this project's favour.** The practical shape is small: one added line in
`LICENSE` and in `docs/data_sources.md` offering CDMX's station extract under
ODbL 1.0. Flagged as an owner decision, because it is the first share-alike
obligation this project would take on.

### The ceiling is no longer the binding constraint

An earlier version of this section argued for trimming, on
`docs/scaling_thresholds.md`'s 20–25 ceiling and a count of ≈23 already
specified. **That reasoning is superseded.** Measuring the architecture showed
RAM is not count-sensitive (no caching, no cross-city data, ceiling = New York
at 7.43 MB ≈ 0.7% of 1 GB) and roughly **80 page slots** are free. The real
limiter was the `drift_check` sweep, and `--jobs N` addressed it.

So slots are not scarce — **verification is**. The constraint is research and
build hours per city, which is exactly what the banding above measures. The
conclusion flips: there is no reason to trim the list, and good reason to
finish Band A first because it costs almost nothing per city.

### Tier 2c closed out, 2026-09-21

**Taiwan is complete — four systems across three cities, all unauthenticated,
all with points AND line geometry:**

| System | Stations | Lines | English names |
|---|---|---|---|
| Taipei TRTC | 122 | 5 (MULTILINESTRING) | ✓ |
| **Kaohsiung KRTC** | **39** | 2 (MULTILINESTRING) | ✓ *Hamasen* |
| **Kaohsiung LRT** | **38** | 1 (LINESTRING) | ✓ *Lizihnei* |
| **Taoyuan TYMC** | **22** | 1 (MULTILINESTRING) | ✓ |
| **Taichung TMRT** | **18** | 1 (LINESTRING) | ✓ *Beitun Main Station* |

**MEXICO CITY IS UNBLOCKED — subway 12**, exactly Metro CDMX's line count,
from a current feed with no expiry warning.

**And the route matters more than the number.** `datos.cdmx.gob.mx` and
`metro.cdmx.gob.mx` both time out — eight attempts across the session — and
feed 1099's `urls.direct_download` on S3 returns **403**. What worked was the
**Mobility Database's own `mdb-latest` mirror**, which had never been tried for
that feed.

That is the **inverse of the Toronto lesson**. There, the mirror was three
months stale and missing an entire mode, and the agency's own feed was right.
Here the agency host is unreachable and **the mirror is the only route**. So
the rule is not "prefer the agency" or "prefer the mirror" — it is **try
both, and treat either failing as a fact about that host rather than about the
city.** A feed has at least three addresses: the agency's, `urls.latest`, and
`urls.direct_download`.

Still open: **Sevilla** — the real `Metro de Sevilla` feed exists at mdb 2781
but its mirror **404s**. **Monterrey** — not in the catalogue under any of
`monterrey`, `metrorrey`, `nuevo león`, so Mexico's third city has no feed.

**Mexico therefore has two confirmed cities**, CDMX and Guadalajara, both
covered by DENUE and its cleared licence — and CDMX was the prize.

### Geocoders and API keys for the Asian set — probed 2026-09-21

The question was whether to settle API keys before building geocoding. **They
are independent — and as of 2026-09-22 no candidate needs a key at all.**

| | Data needs a key | Needs geocoding | Geocoder gated? |
|---|---|---|---|
| **Korea** | **No** — corrected 2026-09-22. Seoul's 인허가 정보 SHEET export is the logged-out path (`ssUserId=SAMPLE_VIEW`) | **No** — `좌표정보(X/Y)` on 99.5% of active premises | n/a |
| **Japan** | No — MLIT, the ward CSVs and ODPT are plain downloads | **Yes** | **No** |
| **Taiwan** | No — TDX and `data.gov.tw` GET-by-id are keyless | **Yes** | **No** |

**Japan's geocoder is keyless and verified on the real format.** GSI's
`msearch.gsi.go.jp/address-search/AddressSearch?q=…` resolved
`東京都港区赤坂一丁目1番12号` to `[139.744003, 35.670933]`. Two properties worth
knowing: it returns **block level** (`一丁目１番`, dropping the 号), which is
ample for a 966 m ring; and it **accepted ASCII digits and matched full-width
itself**, so it does the NFKC normalisation internally rather than requiring it
upfront. MLIT's 位置参照情報 (`nlftp.mlit.go.jp/isj/`) is the bulk alternative.
Digital Agency's Address Base Registry refused connections.

**Taiwan's is keyless too, via NLSC rather than TGOS** — and this only showed
up by applying this file's own TLS lesson. All three Taiwanese hosts threw
`SSLError` under `requests`; with curl, `www.tgos.tw` returns **403** (the
official geocoder is gated) while **`api.nlsc.gov.tw` returns 200**, including
a working keyless point query. **Third time that Python's TLS stack has
reported a reachable Taiwanese government host as unreachable.**

**So the ordering is: Korea first**, and after 2026-09-22 the reasoning is
stronger rather than weaker. Korea is still the only one of the three needing
**neither a geocoding leg nor any new pipeline code** — coordinates on both
legs — and the "single free registration" blocker turned out not to exist.
What *did* shrink is the prize: **Seoul alone, not six cities**, because Busan
and Daegu both fail (per-district licensing, incomplete coverage, and a
CAPTCHA-gated national download). Japan and Taiwan each need a geocoding pass
written, which is build work rather than screening; Toronto's is the precedent.

### KEEP

**Superseded 2026-09-22 by the MASTER CITY LIST above**, which bands these by
what actually blocks each one rather than asserting one blocker apiece. Kept
for the trail: France (Paris) · **Italy (Milan)** · Spain (6 metro cities) ·
South Korea (Seoul) · Taiwan (Taipei) · Mexico (Guadalajara) · Brazil (São
Paulo). Two rows of that line were wrong — **Seoul now has no blocker at all**,
and **Mexico has two cities, not one**, since CDMX was unblocked.

#### CORRECTION — Japan's coordinates, English names and closure dates are ALL EMPTY

**Three claims made about Japan in this file were wrong, and all three came
from reading the CSV header instead of counting the values.** Counted across
Minato Ward's 5,722 rows on 2026-09-21:

| Column | Claimed here | Actually populated |
|---|---|---|
| **`緯度` / `経度`** | "premises-level **with coordinates**" | **0 of 5,722 — 0.0%** |
| **`施設名称_英字`** | "an English name field… an unplanned win" | **0 of 5,722 — 0.0%** |
| **`町字ID`** | the machine join key | **0 of 5,722 — 0.0%** |
| `法人番号` | "corporate number" | **0%** (though `法人名`, the corporate *name*, is 97.8%) |
| `廃業年月日` | "permit **and closure** dates" | **0%** — so inactive premises cannot be filtered out |

**This is the project's first invariant, broken by the person who wrote the
rule into `add-city` Step 0 the same day**: *"a street address and/or lat/long
that actually has data, not merely a column that exists."* The header was
taken as the schema.

**What IS populated, and it is still a real source:**

| | |
|---|---|
| `施設名称` (name) · `営業の種類` (type) · `許可番号` + all four permit dates · `申請区分` | **100%** |
| `所在地_連結表記` (concatenated address) | **100%** |
| Split components — `都道府県` / `市区町村` / `町字` / `番地以下` | **98%** |
| `施設方書` (building and floor) | 95% |
| `法人名` (corporate name) | 97.8% |

And `営業の種類` carries genuine categories: 飲食店営業 4,781 (restaurants),
菓子製造業 320 (confectionery), そうざい製造業 258 (prepared food),
**食肉販売業 105 and 魚介類販売業 47 — meat and fish retail**, so a narrow
slice of food retail does exist even though general retail does not.

**The consequence: Japan needs a GEOCODING LEG, and its addresses are the
hardest format met so far.** Not street-based — Japanese block addressing,
`東京都港区赤坂一丁目１番１２号　溜池明産ビル１階` (chōme / ban / gō), in
full-width numerals. Toronto's problem was street-address normalisation
against a city address-point file; this is a different addressing *system*.
The route would be Digital Agency's **アドレス・ベース・レジストリ** joined on
the 町字 *name*, since the `町字ID` that exists to make that join machine-clean
is empty. **The NFKC rule added to `add-country` today is a prerequisite**, not
an optimisation.

**And therefore Tokyo's station-density figure could NOT be computed**, which
was the highest-value open probe. It needs geocoded premises, and there are
none. Japan's rank stays unmeasured and is now known to be further from
measurable than this file previously implied.

**Japan is a MULTI-CITY country, and its second bucket is now confirmed**
(probed 2026-09-21). Because the permit data follows a **national standard
schema**, coverage is a question of which municipalities publish — not of
parsing each one differently.

| Portal | Found |
|---|---|
| **`catalog.data.metro.tokyo.lg.jp`** | **食品営業許可 279 datasets**, **理容所 916**, **美容所 917**, 公衆浴場 127 — all CSV |
| **Minato Ward** | `理容所一覧` and `美容所一覧` in **CSV *and* GeoJSON** |
| **Sapporo** (`ckan.pf-sapporo.jp`) | `札幌市内の食品営業許可施設一覧` **and** `札幌市内の環境衛生営業施設一覧` — a subway city |
| **Yokohama** | `環境衛生関係施設一覧` (CSV/XLSX/ZIP) — a subway city |
| **Kyoto** | `食品営業許可施設一覧`, confirmed earlier — a subway city |
| Osaka, Nagoya, Kobe | **No CKAN at the guessed URLs — unresolved, not absent** |

**Two things this settles.** First, **Personal services is real, not assumed** —
理容所 (barbers) and 美容所 (beauty salons) are published at scale, 916 and 917
datasets respectively across Tokyo's municipalities. This file previously
recorded that bucket as "the likely source, unprobed". Second, Japan has
**roughly nine subway cities** — Tokyo, Osaka, Nagoya, Yokohama, Kobe, Kyoto,
Fukuoka, Sapporo, Sendai — which is **more than Spain's six**, and the
standard schema means the marginal city is cheap.

**The cap is unchanged and is specifically RETAIL.** Food service and personal
services are both confirmed; Japan licenses no general retail, so the third
bucket is structurally absent. That is Boston's shape — replicated across many
cities rather than one.

**Buildable but CAPPED — a fourth category, added for Japan**
**Japan (Tokyo).** Rail solved and verified (10,235 stations, 21,932 line
segments, PDL 1.0); business premises-level with coordinates on the national
standard schema, CC BY. **The cap is two buckets** — Japan licenses no general
retail. **Precedent exists:** Boston and Toronto are both built at two buckets.
**The deciding number has never been measured** — Tokyo's food-plus-personal
density per in-city station. Toronto's two buckets gave 41; Minato Ward alone
holds 5,723 food premises, so Tokyo plausibly runs to 80–100k across 23 wards
and could exceed Vancouver's 861. **Measure it before ranking Japan.**

**One probe from resolution**
Singapore (catalogue not paginated) · Finland (does NACE 47/56/96 yield shops
or head offices?) · Estonia (bulk CSV URL) · Czechia (a bulk export for a
register that *does* carry classification)

**Keep warm — the blocker is timing or access, with a named trigger**
Bogotá (Metro Line 1 opens) · Brampton (Hurontario LRT, mid-2027) · Denmark
(Copenhagen publishing *produktionsenheder*, as Aarhus already does — and
**DAWA is a free national geocoder worth having regardless**) · Peru (Line 2
refresh) · **Israel, Thailand, Bulgaria — see the IP-block finding below; the
trigger is a different NETWORK, not a different client** · Romania (host
answers nothing at all)

#### Bot-protection is not one thing, and the browser does not defeat it

Recorded because a wrong claim was made here and then tested. This file had
Israel kept warm on the grounds that its portal was "behind bot protection
rather than absent" and that **the browser could get in** — reasoning borrowed
from `read-licence`, which correctly says to use the browser when a page 403s a
plain fetch (Chicago's data terms do exactly that).

**Tested in the browser on 2026-09-21. Both refused it.**

| Host | Result in the browser |
|---|---|
| `data.go.th` | *"Access Denied — your request has been blocked by our security systems"*, with a Cloudflare **Ray ID** and **`IP Address: 50.47.238.226`** printed on the page |
| `opendata.tel-aviv.gov.il` | *"Access Denied"*, **`Client IP: 50.47.238.226`**, `Status Code: 472` |

**The same IP, named back on both pages.** These are **IP-level blocks**, not
client-signature blocks, so changing the client changes nothing — the browser
shares the address.

**So the refusal splits in two, and the tell is on the page:**

- **Client-signature refusal** — a bare `requests` user agent is rejected and a
  real browser is not. `read-licence`'s advice applies; use the browser. Chicago.
- **IP-level refusal** — the block page **names your IP** or shows a WAF request
  ID. The browser is useless. The trigger is a **different network or region**,
  most likely in-country, which is plausibly geo-blocking of a US address by a
  Thai and an Israeli government portal.

**And a third case that is neither:** `ConnectTimeout` / `ConnectionError`, as
with Romania and every `*.cdmx.gob.mx` host. Nothing answered at all, so there
is no block page and no signal — a browser will not help there either.

**The correction to carry:** "bot-protected, so try the browser" was applied
from the licence workflow to data portals without testing it. It holds for
licence pages and fails for these portals. **Read the block page: if it prints
your IP, the client is not the problem.**

**UNPROBED and therefore undecided — not dropped**
**Ireland** (50 feeds; Dublin Luas and DART; the CRO is a company register but
was never business-probed) and **Switzerland** (5 feeds; Zurich trams; never
probed at all). Both appeared in an early "EU company registers" grouping and
**neither was in the hard-line run** — they were lost to a pattern, which is
the exact error this file forbids.

### DISCARD

**Structural data defect — will not change**
**UK** (NNDR is a tax register and will never gain a category) · **Austria**
(GISA strips the street address by design) · **Latvia**, **Slovakia** (no
activity classification at all) · **Belgium** (bulk access paid) · **Hong
Kong** (food-only ceiling *and* no MTR feed) · **Dubai** (no agency feed
exists) · **Egypt** (no open-data infrastructure) · **Australia**, **New
Zealand** (licensing is not municipal)

**Mode mismatch**
Manila (rail typed as commuter rail) · Jakarta (MRT absent; portal refuses)

**Rail measured, and the COUNTRY's business leg genuinely failed on evidence**
Vienna (Austria: GISA strips the street address by design) ·
Amsterdam/Rotterdam (Netherlands: aggregate) · Athens (Greece: sector-only) ·
Lisbon (Portugal: specific negative) · Poznań (Poland: specific negative) ·
Riga (Latvia: addressed but unclassified) · Bratislava (Slovakia: no activity
classification at all) · Cairo (Egypt: no open-data infrastructure)

#### CORRECTION 2026-09-22 — eleven cities were discarded on a reason this file contradicts

**The two-tiers-at-once error repeated, and this time against the document's
own sweep results.** The list above previously also contained Berlin, Hamburg,
Stockholm, Budapest, Naples, Messina, Hyderabad, Kochi, Tallinn, Zagreb and
Santiago, all under the heading "the COUNTRY's business leg failed". Checked
against "What the sweep actually settled", higher in this same file:

| City | Discard said | The sweep actually said |
|---|---|---|
| **Naples, Messina** | country's business leg failed | **"1 passes both legs: Italy, via Milan"** — Italy *passed* |
| **Berlin, Hamburg** | country's business leg failed | "4 have a working route and an **unprobed** register: **Germany**, …" |
| **Stockholm** | country's business leg failed | "9 were not reached at all: … **Sweden** …" |
| **Budapest** | country's business leg failed | "… not reached at all: … **Hungary**" |
| **Tallinn** | country's business leg failed | "… not reached at all: … **Estonia**" |
| **Zagreb** | country's business leg failed | "… **Croatia** … behind SPA front ends" — not reached |
| **Hyderabad, Kochi** | country's business leg failed | "… not reached at all: … **India**" |
| **Santiago** | country's business leg failed | National copy a decade stale; **municipal portals never probed** |

The sweep section even states the correct conclusion in bold — *"Nine of twenty
were never actually probed, and that is the honest headline. None of them
belongs in Tier 4 on this evidence"* — and the discard list was written as
though it said the opposite.

**All eleven move to Band D.** Naples and Messina are the sharpest: they were
discarded for their country failing, in a file whose headline finding is that
their country is the one country that passed.

**Why this happened twice.** The first instance (Germany, Italy, Sweden,
Portugal asserted out from a regional pattern while Berlin, Naples, Stockholm
and Lisbon were being rail-confirmed into the tier above) was caught by
rebuilding the table by hand. This one survived because the discard list is
**prose in a different section from the evidence**, so nothing forced the two to
agree. The lesson for `add-country` is already recorded as "a pattern justifies
deprioritising, never ruling out" — what it needed was the mechanical half:
**a discard list must name its evidence per row**, which the corrected list
above now does, so a contradiction is visible rather than inferable.

**No urban rail at all** (from the original 13-country and 87-country screens)
Winnipeg, Hamilton, Québec City, Halifax, Mississauga, Ottawa · Lithuania,
Cyprus, Slovenia, Luxembourg, North Macedonia, Moldova, Montenegro, Georgia,
Bosnia, Serbia, Greenland · and the single-feed tail: Cameroon, Morocco,
Nicaragua, Ethiopia, Albania, Ghana, Côte d'Ivoire, Tunisia, Rwanda, DR Congo,
South Africa, Costa Rica, Bolivia, Algeria, Mali, Sierra Leone, Uganda, Kenya,
Dominican Republic, Zimbabwe, Nigeria, Uruguay, Sri Lanka

**Access and geopolitics, not data**
Russia · Ukraine

### The asymmetry this exposed in our own screening

**Vienna was discarded for having unusable data behind the best rail in the
screen. Japan was nearly discarded for having *usable* data behind a category
gap. Those are not the same failure, and a three-way drop/keep/dead-weight
split collapsed them.**

Austria's register has no street address, so nothing can be mapped at any
density. Japan's has coordinates, names and classification — it simply omits
one of three buckets, which this project has already shipped twice.

**The rule:** separate **unusable data** from **incomplete coverage**. The
first is fatal at any scale; the second is a labelled caveat on a city page,
and the project's own precedent says so. Conflating them discards working data.

**All of them sit under GDPR** except Santiago, Bangkok, the Indian cities and
Cairo, and that is the expensive half of any European profile.

### Tier 1 — both legs measured. Ready for a country profile.

| | Rail (MEASURED) | Business (MEASURED) | The open question |
|---|---|---|---|
| **France** / Paris | **subway 16, tram 17, funicular 1** (IDFM) | SIRENE, établissement-level, geolocated, **Licence Ouverte 2.0**, non-diffusible masked at source | **Design, not data:** a national register is not the per-city municipal shape this project is built around |

France is the only candidate with no *evidential* gap. What it has instead is
an architectural one, and that is a decision to take before a profile rather
than a fact to discover during one.

### Tier 2 — one leg excellent, the other genuinely open

| | Data | Rail | What is missing |
|---|---|---|---|
| **Spain** | **MEASURED** — Barcelona's 68,024-premises ground-floor census | **MEASURED** — Madrid subway 13, Barcelona FGC subway 4 + funicular 3, plus Bilbao, Málaga, Valencia, Sevilla: **six metro cities, more than any other candidate** | **The licence.** Open Data Barcelona's terms have not been read. That is the only gap, and it is one document |
| **Mexico** | **MEASURED** — DENUE, 6M+ establishments, coordinates, **SCIAN = NAICS** so the taxonomy may transfer | **Partial** — Guadalajara LRT 3 measured and current; **Mexico City unreachable** (S3 403, city portal refuses connections) | A working CDMX feed. Viable through Guadalajara regardless |
| **South Korea** — ~~Tier 2~~ **now Band A, see the master list** | This row described `상가(상권)정보`, which is **unobtainable** (the API needs a Korean-resident account). Superseded 2026-09-22: Seoul's 인허가 정보 datasets give **197,276 active premises with EPSG:5174 coordinates, KOGL Type 1, no account** — one city rather than six | **MEASURED** — national urban-railway **station** and **line** standard datasets on `data.go.kr` (15013205 / 15013203) | ~~Verify the schema live~~ **Done.** No open question |

**Spain overtook Mexico this round.** Its business leg was already the
Montréal model and its rail leg is now the deepest measured anywhere in this
screen — six metro cities in one country, against Canada's six *candidate*
cities of which only two had a metro. What stands between Spain and Tier 1 is
a single unread licence, not a data question.

### Tier 3 — rail measured, business data unknown

All confirmed to have real urban rail; none has had its business register
probed. These are cheap to advance and could move up or out quickly.

**The widened re-probe added ten European capitals to this tier**, several of
which were initially and wrongly reported rail-free: **Vienna** (subway 35,
tram 185 — the largest measured anywhere in this screen), **Amsterdam /
Rotterdam** (subway 14, tram 46), **Berlin** (urban rail 9, tram 48),
**Stockholm** (metro 7, tram 21), **Copenhagen** (subway 4, tram 4),
**Oslo** (metro 5, tram 9), **Prague** (subway 3, tram 40), **Helsinki**
(subway 4, tram 26), **Lisbon** (subway 10) and **Naples** (subway 3, tram 3,
funicular 3). Each still needs its business register probed, and **each sits
under GDPR**, which is the expensive half.

| City | Country | Rail (MEASURED) |
|---|---|---|
| **Vienna** | AT | **subway 35**, tram 185 — the deepest measured in this screen |
| **Amsterdam / Rotterdam** | NL | subway 14, tram 46 |
| **Berlin** | DE | urban rail 9, tram 48 |
| **Stockholm** | SE | metro 7, tram 21 |
| **Santiago** | CL | **subway 7**, tram 2 |
| **São Paulo** | BR | **subway 6** |
| **Bucharest** | RO | subway 5, tram 15 |
| **Oslo** | NO | metro 5, tram 9 |
| **Lisbon** | PT | **subway 10** |
| **Singapore** | SG | **subway 13** — but a city-state, and its register is likely registered-office shaped |
| **Sofia** | BG | subway 4, tram 24 |
| **Copenhagen** | DK | **subway 4** — ⚠️ **"tram 4" was WRONG, corrected 2026-09-23**: OSM returns **ZERO** tram relations in Københavns Kommune AND zero in Region Hovedstaden, and no Letbane relation exists either. Copenhagen's tram closed in 1972. Metro is M1–M4, 8 relations, all named and all coloured; S-tog is 7 refs and is excluded as S-Bahn |
| **Bangkok** | TH | subway 4, LRT 5 |
| **Helsinki** | FI | subway 4, tram 26 — *feed expired* |
| **Budapest** | HU | subway 4, tram 42 — *feed expired* |
| **Hamburg** | DE | underground 4 — *feed expired* |
| **Prague** | CZ | subway 3, tram 40 — *feed expired* |
| **Athens** | GR | subway 3 |
| **Naples** | IT | subway 3, tram 3, funicular 3 |
| **Hyderabad / Kochi** | IN | subway 3 / subway 1 |
| **Cairo** | EG | subway 2 — *feed 11 months expired* |
| **Tokyo** | JP | **subway 4, tram 1** (Toei) — rail is fine; **Japan's blocker is its business data** |
| Tram-only | — | Riga 7, Tallinn 5, Zagreb 19, Bratislava 6, Poznań 22, Messina 1 |

#### Tier 3 business probes — started 2026-09-21

Two countries moved materially; the rest are still asserted.

**Norway — MEASURED, and it is premises-level.** The Brønnøysund open API
answers with **no key, no login, no registration**:

```
https://data.brreg.no/enhetsregisteret/api/underenheter?kommunenummer=0301
```

**152,060 sub-units in Oslo alone.** Each record carries `navn`,
`naeringskode1` (NACE code *and* description), `organisasjonsform`,
`oppstartsdato`, and critically **`beliggenhetsadresse`** — the *physical
location* address, which the register keeps distinct from the registered
business address. That distinction is the whole filter-3 question, and Norway
answers it the right way.

**No coordinates**, so a geocoding leg would be needed. Kartverket publishes an
open national address register, untested. Oslo measures metro 5, tram 9.
GDPR applies, and the sample already shows the familiar shape — a law firm
named after a person, at what reads like a house.

**Austria — a strong lead, not yet a finding.** GISA
(*Gewerbeinformationssystem Austria*) is a national **business licence**
register — the US/Canada model, not a company register — carrying the name,
**the location**, and the wording of each licence. Reportedly published on
`data.gv.at` as **open data in CSV and JSON, with personal data removed at
source**, free and without registration. That combination, paired with
**Vienna's subway 35 / tram 185 — the deepest rail in this screen** — would
make Austria a Tier 1 candidate.

**ASSERTED: the dataset URL guessed for it returned 404.** Find the real
resource before believing any of this.

**Still asserted, unprobed:** Denmark's CVR *produktionsenheder*, Czechia's
ARES (3.4M subjects, open, NACE — but subjects, not premises), Poland's
CEIDG/REGON, Sweden's Bolagsverket (company-level), Germany, Italy, Portugal,
Greece, Finland, the Netherlands.

**Germany, Italy, Sweden and Portugal were moved here from Tier 4.** They had
been ruled out on the EU-default company-register pattern — which was
**ASSERTED and never probed for any of them** — while Berlin, Naples,
Stockholm and Lisbon were simultaneously being rail-confirmed into this tier.
They were in two tiers at once. Ruling a country out on a pattern rather than
a probe is exactly the error this file exists to avoid.

### RE-ANALYSIS under the corrected framework — most of Tier 4 is not safe

Applying the rules that came out of this screen to the screen itself. Korea is
the proof: it sat in Tier 2 on "**zero feeds in the catalogue**", and the
national standard dataset turned out to hold **1,099 stations with WGS84
coordinates, free and unrestricted**. The catalogue was simply the wrong place
to look.

**Every Tier 4 entry ruled out on "no feed anywhere in the catalogue" was
tested against a transit catalogue — the wrong source for a GIS question.**
Those rulings are therefore **ASSERTED, not measured**, and the countries below
move back into the running pending a national-mapping-agency probe:

| Country | Ruled out on | Where to actually look |
|---|---|---|
| **Hong Kong** | no MTR feed | Lands Department **iB1000** topographic map (transport layer), CSDI portal |
| **Taiwan** | no Taipei/Kaohsiung feed | **NLSC**, and **TDX** (MOTC) |
| **Indonesia** | no MRT Jakarta feed | Badan Informasi Geospasial |
| **Brazil / Rio** | no MetrôRio feed | IBGE |
| **Malaysia** | no Prasarana feed | JUPEM |
| **Israel** | no Tel Aviv feed | Survey of Israel, `data.gov.il` |
| **Peru, Colombia** | no Lima/Medellín/Bogotá feed | IGN, IGAC |

**None of these has been probed at its national mapping agency.** Given Japan
and Korea both flipped on exactly this, the prior should be that several of
them flip too.

#### Sweep status, 2026-09-21 — routing established, schemas not yet

Reachability tested; **no schema has been verified for any of the eight**, so
every row below is a *route*, not a finding.

| Host | Result |
|---|---|
| `tdx.transportdata.tw` | **200** — Taiwan's transport exchange is live |
| `data.gov.tw` (and dataset `102985`) | **200** |
| `www.csdi.gov.hk` | **200** — Hong Kong's official spatial data infrastructure, "free download, machine-readable" |
| `data.gov.hk` | 302 |
| `portal.nlsc.gov.tw` | **000** — down; TDX is the route for Taiwan, not NLSC |

**Taiwan is the one worth doing first**, and the reason is business data rather
than transit: it is **the only one of the eight with plausible premises-level
business data *and* a metro**. `data.gov.tw` carries 商業登記 (commercial
registration) exports with business addresses, so a transit flip there could
move a whole country rather than just correcting a table. Expect TDX to be
registration-gated, like Korea's and WMATA's.

**Hong Kong is the opposite case and should be deprioritised despite CSDI being
live.** Its business data is the FEHD food-licence register — **food only**,
so Hong Kong is a two-bucket city at best whatever its rail data shows. Fixing
its transit would not fix its ceiling.

**Still entirely unprobed:** Indonesia (BIG), Malaysia (JUPEM).

#### Israel — transit MEASURED, and it passes both halves

`data.gov.il` is CKAN and answers `package_search` without a key. It publishes
a full light-rail set under **Creative Commons Attribution**: stations, lines,
tunnels and depots, each as SHP, KMZ and CSV.

| Layer | MEASURED |
|---|---|
| `LRT_STAT.shp` | **332 Points**, **EPSG:2039** (Israeli TM Grid), columns `STAT_NAME`, `LINE`, `TYPE`, `STATUS`, `COMP`, `MTR_AREA` |
| `LRT_LINE.shp` | **27 LineStrings**, EPSG:2039, columns `NAME`, **`LINE_EG`** (English name), `FREQ`, `STATUS`, `START_`, `DESTNATION`, `LENGT` |

Stations *and* line geometry, which is the check Korea fails. Reprojection
would be EPSG:2039 → UTM 36N (**EPSG:32636**) for Tel Aviv.

**TWO TRAPS, both visible only in the columns:**

- **The "stations" layer is station ENTRANCES.** `ENTRC_EXIT`, `ACSBL_ENTR`,
  `ENTRC_TYPE` and `ENTRC_LBL` give it away: **332 points against Tel Aviv's
  ~34 Red Line stops.** Buffering every entrance would multiply rings per
  station and inflate any density measure severalfold. Dissolve to one point
  per `STAT_NAME` before use.
- **`STATUS` means some of this is not built.** Tel Aviv's Red Line opened in
  2023; the Purple and Green lines are under construction. A layer that
  includes planned stations would draw rings around building sites — the
  inverse of Brampton, where the project correctly waited for the Hurontario
  LRT.

Neither is a defect in the data; both are defects in reading it without
looking at the columns.

**Israel's business register is the deciding leg, and there is a mismatch.**
Searched `data.gov.il` for רישוי עסקים (business licensing): the only such
register is published by **עיריית באר שבע — Be'er Sheva**, which has no light
rail. **The city with the rail is not on the national portal.** Tel Aviv runs
its own portal (`opendata.tel-aviv.gov.il`), unprobed — the city-first lesson
for a third time. Until that is checked, Israel has transit and no matching
business data.

#### São Paulo — MEASURED, and the cleanest transit data found in this screen

GeoSampa's WFS answers unauthenticated. `GetCapabilities` lists **484 layers**,
of which the relevant ones are `estacao_metro`, `linha_metro`,
`area_influencia_metro`, `estacao_transbordo`, and — separately —
`estacao_metro_projetada` and `linha_metro_projetada`.

| Layer | MEASURED |
|---|---|
| `geoportal:estacao_metro` | **94 Points**, **EPSG:31983**, columns `nm_estacao_metro_trem`, `nm_linha_metro_trem`, `nm_empresa_metro_trem`, `tx_situacao_metro_trem`, **`cd_tipo_transporte`** |
| `geoportal:linha_metro` | **6 LineStrings**, EPSG:31983, columns `nr_nome_linha`, `nm_linha_metro_trem`, `nm_empresa_metro_trem` |

Three things make this the best-shaped transit source in the screen:

- **EPSG:31983 is SIRGAS 2000 / UTM 23S** — already the correct metre-based
  projected CRS for São Paulo, so the project's per-city CRS derivation agrees
  with the publisher and no reprojection is needed for distance work.
- **`cd_tipo_transporte` separates metro from *trem*** (CPTM commuter rail),
  which this project excludes everywhere. The discriminator is in the data
  rather than inferred from route names.
- **Built and planned are SEPARATE LAYERS**, not a status flag. That avoids
  Israel's trap by construction — a build simply does not request
  `*_projetada`.

**Brazil's cost is the business leg, as recorded earlier:** CNPJ has ~72M
establishments with trade name, full address and CNAE, monthly and open — but
**no coordinates**, so geocoding at a scale beyond Toronto's 159,872, and the
*sócios* names must never be downloaded.

**São Paulo is now the strongest Latin American candidate after Mexico**, and
unlike Mexico City its transit host actually answers.

#### Peru — NOT blocked. The hostname was wrong.

Recorded earlier as "portal refused connection". **That was wrong, and the
cause is embarrassing and worth keeping:** `datosabiertos.gob.pe` fails, while
**`www.datosabiertos.gob.pe` answers 200**. A vhost that exists only with the
`www.` prefix — and a whole country was nearly written off over it.

**Add to the reachability drill: try `www.` before recording a host as down.**

With the right hostname, `package_show` returns the dataset:

| | MEASURED |
|---|---|
| Title | `MTC - AATE ESTACIONES DE METRO DE LIMA - LINEA 1` |
| Author | MTC – AATE (Autoridad Autónoma del Tren Eléctrico) |
| Licence | **ODC-BY** (`opendefinition.org/licenses/odc-by/`) |
| Resource | `https://www.datosabiertos.gob.pe/sites/default/files/estaciones2018.xlsx` |

**Two limits, both real:** `metadata_modified` is **March 2018**, and it covers
**Line 1 only**. Station positions on a line that opened in 2011–14 are
unlikely to have moved, so the staleness is survivable — but **Lima Line 2 has
been opening since 2023 and is absent**, so this source alone understates the
city. Peru is viable and incomplete, not blocked.

#### The last of the sweep — reachability, 2026-09-21

| Target | Result |
|---|---|
| **Tel Aviv** `opendata.tel-aviv.gov.il` | **HTTP 472** — a non-standard code, i.e. bot protection. Not down; refusing automated requests. Needs the browser, not a script |
| **Jakarta** `data.jakarta.go.id` | Connection refused |
| **Malaysia** `data.gov.my`, `developer.data.gov.my` | **200** — reachable; `api.data.gov.my/data-catalogue` returns 400, so the API needs its documented parameters. Unfinished rather than failed |
| **Mexico City** `datos.` / `metro.` / `sig.cdmx.gob.mx` | **All three time out.** This is **domain-wide**, not one portal — which is a different and more durable finding than "a portal is down" |
| **Mexico national** `datos.gob.mx` | 200 |
| **ArcGIS Hub** | 200, and the likeliest route to the CDMX metro layer; the v3 `filter[q]` parameter was rejected, so the query form still needs working out |

**Mexico City's layer is not lost** — `Líneas y Estaciones de STC Metro` is
named and catalogued. Every `cdmx.gob.mx` host is unreachable from here, so it
needs either a different network or a mirror on `datos.gob.mx` or ArcGIS Hub.
Guadalajara continues to carry Mexico meanwhile.

#### Latin America, probed 2026-09-21 — and the national agencies were the wrong place

The national mapping agencies (IGAC, IGN/IDEP, IBGE) were the obvious target
after Japan. **The layers are at city level instead**, which is the Mexico and
Korea pattern again: national portal blocked or irrelevant, city portal
serving.

**Bogotá — good data, wrong mode.** `datosabiertos-transmilenio.hub.arcgis.com`
serves GeoJSON unauthenticated: **153 stations, all `Point`, EPSG:4326**, with
`longitud`/`latitud` and station names. But these are **TransMilenio BRT**
stations, and BRT is not urban rail here. Bogotá's Metro Line 1 is still under
construction, so Colombia is out **on mode, not on data** — and worth
revisiting when Line 1 opens, because the publishing infrastructure is
evidently good.

**Mexico City — unreachable, and this is now durable.** The metro's own
`Líneas y Estaciones de STC Metro (SHP)` sits on `datos.cdmx.gob.mx`, which
failed again **after the prober's retry** — roughly the sixth failure across
the session, while `inegi.org.mx` answered instantly throughout. Recorded as a
fact about the host, not the data: **the layer exists and is named**, and
Guadalajara continues to carry Mexico meanwhile.

**Located but not yet probed:**

- **Lima** — `MTC - AATE ESTACIONES DE METRO DE LIMA - LINEA 1` on
  `datosabiertos.gob.pe`, JSON and Excel, under an **Open Data Commons
  Attribution** licence. Line 1 is genuine urban rail.
- **São Paulo** — GeoSampa (`download.geosampa.prefeitura.sp.gov.br`) publishes
  the operating stations of Metrô and its concessionaires as shapefiles. Brazil
  already has the CNPJ business register, so São Paulo is the strongest Latin
  American candidate after Mexico.

#### Taiwan, probed 2026-09-21 — business leg MEASURED

`data.gov.tw`'s catalogue API answers **GET by dataset id without a key**;
only search needs one (`ER0001: API Key錯誤`).

**`商業登記(依營業項目別)`** (dataset `102985`, Ministry of Economic Affairs),
downloaded and parsed — **45,819 rows for the single category 其他餐飲 (other
food service)**, monthly updates:

| Column | Content |
|---|---|
| `統一編號` | unified business number |
| `商業名稱` | business name |
| **`商業地址`** | **premises address**, e.g. `高雄市鼓山區濱海一路２３號１樓` — down to floor |
| `登記狀態` | `核准設立` (approved) / `歇業／撤銷` (closed or revoked) — so active filtering works |

**It is premises-level.** 商業登記 registers sole proprietorships and
partnerships **at their operating address**, unlike 公司登記 (dataset `13861`),
which is a company register with the registered-office defect.

**Three costs, none fatal:**

- **No coordinates.** Address only, so Taiwan needs a geocoding leg — the
  Toronto problem. TGOS (內政部) is the candidate; NLSC is down.
- **Split one dataset per category** (`依營業項目別`), so coverage is an
  assembly job — `multi-source-city`, at national scale.
- **Full-width numerals** in addresses (`２３號`) will need normalising before
  any geocode match. A quiet trap of exactly the kind Toronto's title-case
  `ADDRESS_FULL` was.

**Transit leg — MEASURED, complete, and NOT registration-gated.** TDX's
`v2/Rail/Metro/*` endpoints answered plain unauthenticated requests:

| Endpoint | MEASURED |
|---|---|
| `Station/TRTC` | **122 stations**, each with `StationPosition.PositionLat/Lon` (WGS84), `StationAddress`, city and town codes, and `StationName` in **Zh_tw, En, Ja and Ko** |
| **`Shape/TRTC`** | **5 lines as `MULTILINESTRING` WKT**, plus `EncodedPolyline` |
| `Line/TRTC` | 5 lines with `LineName`, `LineSectionName`, `IsBranch` and **`LineColor`** |
| `StationOfLine/TRTC` | station-to-line mapping |
| `Network/TRTC` | operator and network metadata |

**This passes both halves of the points-and-lines check**, and gives more than
GTFS would: official **line colours**, which this project otherwise researches
by hand per city, and English station names, which removes the label-language
question exactly as Korea's `영문역사명` did.

**So Taiwan's ruling is reversed.** It was in Tier 4 on "the 9 Taiwanese feeds
are all rural bus operators" — true of the catalogue, and irrelevant, because
the national transport exchange publishes a first-class rail API that the
catalogue does not mirror. **Taiwan's only real cost is the business leg:
geocoding, and per-category assembly.**

Taiwan's food-hygiene register (`食品業者登錄資料集`, dataset `8938`) is
separately available as CSV/JSON/XML from `data.fda.gov.tw`.

#### ▲▲ 2026-09-23 — Taiwan's "geocoding leg" is a JOIN, measured at 92.5% in Taipei

**Both costs above were overstated, and the method that found it was the one
that found Brazil's: look for an address file that already carries the
coordinate before building a geocoder.**

1. **The whole catalogue enumerates without a key.** `data.gov.tw/datasets/export/csv`
   returns all **52,436 datasets** (67.8 MB) with each one's download URL,
   licence and field list. `ER0001` was the search API only — a statement
   about one endpoint.
2. **Door-plate coordinate files exist for every city this project wants.**
   117 `門牌` datasets; for the four cities plus New Taipei: **Taipei**
   `門牌位置數值資料` (monthly, 124.5 MB, TWD97 x/y), **New Taipei** (monthly,
   **1,989,458** door plates, `x_3826`/`y_3826`), **Taoyuan** (monthly, TWD97
   TM2), **Taichung** (monthly 2026 releases via Google Drive links),
   **Kaohsiung** (2025 edition, TWD97 — its host **timed out from six check
   nodes in five countries**, Hong Kong, Japan and Singapore included; no
   Taiwanese node was available, so recorded as unreachable, not negative).
   All under **政府資料開放授權條款-第1版** (Open Government Data License v1.0,
   not yet read). Each row is street / lane / alley / number / coordinate.
3. **A better business register than 商業登記: the national BUSINESS TAX
   REGISTER.** `全國營業(稅籍)登記資料集` (Fiscal Information Agency,
   `eip.fia.gov.tw/data/BGMOPEN1.zip`, 66.3 MB, **refreshed daily** — the file
   self-attests its date). **1,713,627 operating rows nationally.** One row
   per trading location: `營業地址`, `總機構統一編號` (a parent ID, so
   **company branches are their own rows** — 商業登記 omits companies
   altogether), trade name, organisation type, and a 6-digit industry code
   with its own name. **No personal-name column** — unlike New Taipei's own
   商業登記清冊, which carries `res_name` (the responsible person).
4. **Composition, Taipei (255,699 rows, 14.9% of the country):** the codes
   read from the register's own names put **47/48 = retail, 56 = food service,
   96 = personal services**, ISIC's divisions. Storefronts: retail **44,634**,
   food **23,684**, personal **8,201** = **76,519**, after excluding **4,954**
   rows of **487 `經營網路購物`** (online shopping — NAICS 454's twin).
   Organisation types: 有限公司 104,489 · 獨資 69,156 · 股份有限公司 56,483
   · branches 10,568 — **whether company rows in the storefront codes are
   shops or head offices is the registered-office question, still open.**
5. **The join, Taipei:** parse `營業地址` into street / lane / alley / number
   (NFKC for full-width digits; Chinese section numerals to digits;
   `之` `－` `―` as one sub-number separator; floors dropped) and match the
   door-plate keys — **251,607 distinct**. **Food 95.1%, personal services
   99.0%, retail 90.0% — 92.5% overall.** The first pass read 89.1%; the
   difference was one character, `―` (U+2015), used as a sub-number dash.
   Retail's misses are mostly **market stalls** (`環南市場１樓…攤位`) and
   **stalls under the viaduct** (`建國南路１段高架橋下`) — real premises with no
   door plate.

⚠️ **Certificates:** Python's bundled store lacks Taiwan's government root
(GRCA), so `data.taipei` fails verification there; **curl on Windows verifies
it** against the OS store. A build uses the OS store — never switches
verification off. *(Two scratch probes that did switch it off for header peeks
were deleted the same day; nothing in the repository ever did.)*

#### ▲▲ 2026-09-23, later — Taiwan finished: three cities join, rail needs no TDX

**The join, three cities, one parser** — with **Taipei as the control**, which
had to reproduce its first measurement before the others counted. A
generalised parser first read Taipei at 91.7%, because its street pattern
forbade `市`, `鎮` and `里` — the characters stripped as district and village —
and so failed every street that CONTAINS one (`市民大道`, `鎮三街`). Fixed, the
control read 92.4% against 92.5%:

| City | Storefronts | **Joined** | Door-plate file |
|---|---|---|---|
| **Taipei** | 76,519 | **92.4%** | monthly, 2026-09-02, 251,607 keys |
| **Taoyuan** | 49,282 | **94.0%** | `TGOS_A68000_11508.CSV`, 2026-08, 516,049 keys |
| **Taichung** | 73,227 | **92.7%** | 2026-08 GIS release (city's Google Drive), 719,446 keys, **TWD97 and WGS84** both |
| **Kaohsiung** | 72,550 | ⛔ **unmeasured** — `data.kcg.gov.tw` and `openapi.kcg.gov.tw` time out from six nodes in five countries and on two later tries | — |
| **New Taipei** | **76,320** | **95.5%** — the best of the five | monthly, 192.9 MB, 422,048 keys, columns in English |
| **Taipei (Regional)** = Taipei + New Taipei | **152,839** | **93.9%** | New Taipei surrounds Taipei and the metro crosses the boundary: the Dublin/Lille regional shape, decided 2026-09-23 |

**No registration still carries the pre-upgrade county names** (`桃園縣`,
`臺中縣`) — the trap was checked and is empty. **Taichung's numbers chain
sub-numbers** (`２之３之２號`), which the parser now handles.

**The head-office question, MEASURED on Taipei's 76,519:** company rows (head
office or single site) are **19,491**, and **38.7% of them sit on a 3rd floor or
higher or carry a room number (`室`)** — against **7.1% for sole proprietors**,
the control, and 8.2% for branches. **The registered-office trap is real and
confined to company rows** — about 7,500 in Taipei. Clustering found the
opposite of a registered-office service: the most-shared addresses are
**traditional markets** (環南市場 893 rows, 士林市場 513).

**Person names, MEASURED:** **3,763 Taipei storefronts (4.9%) are registered
under what reads as a person's name** — all sole proprietors, **63% of them
market stalls**, 1,282 at street level, **119 on an upper floor**. A
build-time rule, recorded in the brief when one is written.

**Rail: TDX is now key-gated, and not needed.** Every operator returns `401
Valid API Key Required` to a script; TDX's terms (read 2026-09-23) allow
keyless access only as a browser-only visitor mode capped at 20 calls a day,
and scripted use needs a member key whose registration wants a Taiwanese
mobile number or manual review. The server now tells browsers from scripts,
which is why the 2026-09-21 probe worked and today's does not. **The agencies
publish their own, keyless, under OGDL v1:** Taipei's network map
(`臺北都會區大眾捷運系統路網圖`, GeoJSON `MultiLineString` with `RouteName`,
EPSG:3826) and station points; Taipei Metro's station and route tables;
Taichung's Green Line stations with lat/lon; the national land-survey centre's
`捷運車站` / `輕軌捷運車站` layers (2026-04); Taoyuan Metro's network XML.
Kaohsiung's station files sit on the unreachable host, and the railway
bureau's airport-MRT file is behind an **Incapsula bot challenge** — not worked
around; the national layer covers those stations.

#### ▲▲ 2026-09-23, night — Kaohsiung is GEO-BLOCKED, not down

Measured layer by layer from here: every Kaohsiung data host — `data.kcg.gov.tw` (223.200.100.11), `openapi.kcg.gov.tw` and `api.kcg.gov.tw` (both 223.200.91.113), `kcgdg`, `sports` — **resolves in DNS and drops the TCP connection attempt on ports 443 AND 80**, while `www.kcg.gov.tw` (223.200.91.227, same /16) connects in 0.16 s with a valid `*.kcg.gov.tw` certificate. Then from **Globalping**'s probe network, which has Taiwanese probes where check-host.net has none: `data.kcg.gov.tw` answered **HTTP 200 to 3 of 3 Taiwanese probes** (Taichung and Taipei, AS3462 and AS4780) and **timed out from Tokyo and Los Angeles**; `www.kcg.gov.tw` answered all five. **A foreign-address filter on the data hosts — the publisher's access control, not routed around.** One `HEAD` per probe, diagnosis only; nothing was fetched through a probe.

The national catalogue (the on-disk export, 52,436 datasets) lists **3,342 Kaohsiung-published datasets and no other host** for any of its files: 6,951 URLs on `data.kcg.gov.tw`, 6,932 on `openapi.kcg.gov.tw`, 9 on `api.kcg.gov.tw`. The door-plate file exists in a **2026 edition** (`高雄市115年門牌坐標資料-TWD97`, dataset 177859, six resources, updated 2026-06-25) with the same street / lane / alley / number / TWD97 columns as the other cities. Kaohsiung's metro station coordinates (`高雄紅橘線捷運車站中心座標`, `高雄輕軌車站中心座標`) sit behind the same filter. `openapi.kcg.gov.tw`'s root redirects to `/Account/Login` even from Taiwan. **No national door-plate file** exists in the catalogue — MOI publishes only counts of what the cities supply.

**The way through is the publisher, not the network**: 高雄市政府民政局 could publish the file on data.gov.tw or lift the filter for it. Until then Kaohsiung waits on the publisher *(placed in the access-blocked band, 2026-09-23)*.

#### ▲ 2026-09-24 — Czechia: RŽP's *provozovny* ARE reachable in bulk, as a batched search

Asked by the build session after Prague paused on RES (a register of seats). **NKOD**'s SPARQL endpoint timed out on a full-text query over titles and descriptions — a cost failure, not an answer. `rzp.gov.cz` and ARES's developer page are JavaScript apps that a plain fetch sees empty. **ARES v3's own OpenAPI spec** (`/ekonomicke-subjekty-v-be/rest/v3/api-docs`, 132,958 B) answered it: besides the per-IČO `GET /ekonomicke-subjekty-rzp/{ico}` there is **`POST /ekonomicke-subjekty-rzp/vyhledat`**, whose filter accepts paging and — as a live call showed, since an empty filter is refused with `VSTUP_PRAZDNY` — **a list of IČOs**. Its schema `ProvozovnaZaklad` carries `icp` (the establishment's own number), `nazev`, `typProvozovny`, `platnostOd`/`platnostDo`, and `sidloProvozovny`, a full address **with `kodAdresnihoMista`** — the RÚIAN address-point code Prague's join already matches at 99.8%.

**One call, two retail chains** (Billa 00685976, Albert 44012373): HTTP 200, both full records (1.2 MB and 1.4 MB), **1,258 and 1,723 establishment entries carrying `kodAdresnihoMista`**, of which Praha 259 and 398; `typProvozovny` codes 1 (the large majority), 0 and 6. Entries repeat per licence and include ended establishments, so a count needs `icp` de-duplication and a `platnostDo` filter.

**So the provozovny exist in bulk, but as a batched search rather than a dump.** Open before Prague resumes: the list-size cap per call; **ARES's terms and rate limits** (unread); the IČO universe — a Praha shop can belong to a subject seated anywhere, so the RES seat filter under-covers and the national CZ-NACE 47/56/96 set is the honest universe; the `TypProvozovny` code list; and the restaurant control against OSM, re-run on establishments instead of seats.

#### ▲▲ 2026-09-24 — Czechia: Prague's establishments are OPEN DATA (ROS02); back to Band A

The batched RŽP route above was measured and then **set aside**. Measured: 100 IČOs a call (the API's own error: *"Limit je maximálně 100"*), 500 calls a minute, a national universe of **403,793** active 47/56/96 subjects (4,038 calls); a 5,000-subject sample estimated ~28,970 active Praha establishments. Read: ARES's terms permit querying; the Trade Licensing Act § 60(6) bans publishing a *sestava*, and its legislative history shows Parliament **struck** a second ban aimed at the online public part (zákon 289/2017, tisk 1014, committee resolution 386); but **ÚOOÚ fined a site mirroring sole traders' RŽP data in 2019** (UOOU-10201/18-31), because RŽP is not open data.

**The research that read the fine also found the way round it**: the Digitální a informační agentura publishes **ROS02, *Registr osob – aktivní provozovny***, under zákon 106/1999 § 5a — ICP, IČO, dates and the RÚIAN code of every establishment, 58.5 MB, declared no copyright, no database right, **no personal data**, CC0 match; read in full 2026-09-24, **PERMITTED**. Joined to RES by IČO: **27,065** Praha storefront establishments (9,492 / 8,037 / 9,536), **5,057** of them owned from outside Praha, and the restaurant control at **1.63x** against a like-for-like OSM count of **4,652**. **That control was mis-specified when it paused Prague**: all of NACE 5610 against `amenity=restaurant` alone, where France had compared NAF 56.10A — like-for-like, RES's seats read 4.48x, still a fail.

**The generalisable lesson: a register's establishments may be published by a DIFFERENT agency than the register.** RŽP owns the provozovny; the basic-registers agency publishes them as open data. Asking only the owner's API found a legal problem the open copy does not have.

#### ▲ 2026-09-24 — the open screening gap probed: Rome reached, Turin and Cairo measured out

**Rome**: the SUAP register's host verifies with the OS trust store (the recorded TLS failure was ours). Premises-level, CC BY declared, monthly to July 2025: `NUMERO_ESERCIZIO`, `CODICE_VIA` + street + `CIVICO` (95.8%), `DESCRIZIONE_MACRO_ATTIVITA` (99.2%), `DESCRIZIONE`. No coordinates and no house-number layer on the city's portal (its one *civici* hit is a polling-station list). **ANNCSU**, the national house-number archive (Agenzia delle Entrate + ISTAT, open data under the EU HVD regulation), publishes monthly regional files — `getds.php?INDIR_LAZI`, 24,573,936 B compressed / 156,609,050 B, dated 2026-09-15, which answers `403` to `HEAD` and `200` to `GET` — with `CODICE_COMUNALE`, `CIVICO`, `ESPONENTE`, `COORD_X_COMUNE`, `COORD_Y_COMUNE`; empty for the first comune in the file. ▲▲ **Measured for Roma the same night: 516,337 civic numbers, street code and WGS84 coordinates on 100%, the code identical to SUAP's `CODICE_VIA`; the Municipio I sample joins at 92.4% civic-level** (91.6% exact). **"Italy is a Milan-only country" no longer holds** — ▲▲▲ **and the full register measured the same night put Rome in Band A**: 168,255 rows → 155,448 establishments → 95,493 in the three buckets, joined at **95.7% civic-level** (every municipio ≥ 90.9%); both licences CC BY 4.0; food-and-drink control 2.60× (no closure date in the register) — Band A with a build check, owner's call. Brief `docs/build_briefs/rome.md`, and ANNCSU's coverage of other comuni is per-comune — check each city's own rows.

**Turin** and **Cairo**: discarded, two methods each — see the master list's discard table.

**Japan**: `data.go.jp` **ignores `q`** (the nonsense term returned all 18,140 datasets); enumerated whole, it holds **no food-business dataset at all** — the national catalogue does not harvest municipal open data, so each city's own portal is the route (Tokyo's metropolitan CKAN lists ward files: Minato, Chuo, Koto, Shinjuku, Nakano).

#### ▲ 2026-09-24 — the discard audit, and Amsterdam re-probed on its own host

**Amsterdam** had been discarded as *"register is aggregate"* on the top hits of one `data.overheid.nl` search. Its own DSO API (`api.data.amsterdam.nl/v1/`, 100 datasets — first recorded as 383, which was dataset and table paths) holds the KvK register (`hr_kvk`, gated 403) and **`horeca/exploitatievergunning`: 4,094 live hospitality permits with points** — 0.89× OSM restaurants; licence SILENT. KvK's national HVD open dataset truncates addresses to two postcode digits. → Band C.

**The audit** read all 34 discard rows against this trail: 21 rest on two methods, a measured register, or their terms; **12 rested on one method** — Vienna, Rotterdam, Helsinki, Lisbon, Kuala Lumpur, Tallinn, Warsaw, Hamburg, Riga, Athens, Poznań, Bratislava — and moved to the open gap with their next probe named. **The lesson: an early sweep checked discard rows for the words "unprobed" and "not reached", and a one-search negative worded as a finding ("aggregate") passed it.** A discard needs its method count, not its wording.

**Later the same night — the evidence columns.** Filling *Kind / Methods / City host asked?* from this trail failed **5 of the 21** the audit had passed: **Naples** and **Messina** (one search of the city's portal each), **Santiago** and **Lima** (coverage verdicts that never asked the missing comunas' or districts' own sites), **Hyderabad** (GHMC's own host blocked, 403 F5 WAF, never diagnosed from inside India). Owner's call: all five to the open gap. **The audit sorted on wording a second time**; columns a script reads (`scripts/check_discard_evidence.py`) are what caught it. Discards now 16, open gap 17.

**Amsterdam, other routes (same night).** All 100 datasets listed. The gated two are city-staff scopes in the published schema — `hr_kvk` `FP/MDW` + `HR/R`, `standbedrijven` `BSK/BEDRIJVEN` — so a request is unlikely to land. **BAG** on the same API: 10,898 *winkelfunctie* units in use (90% shop-only), 1.77× OSM's 6,150 shops, nonsense control 0 — but no name, no activity, and `feitelijkGebruik` empty on every one, so vacancies count. Nothing else is premises-shaped. Band C stands; whether a use-class layer may stand in for a retail register is OPEN for the owner.

**Amsterdam, how many BAG shops are empty.** Not filterable per unit from open data: `standvastgoed/gebouwen` (134 fields per address, BAG-keyed) has no occupancy field; `energieverbruik_mra` is per neighbourhood; Locatus and KvK hold it per unit but are paid or staff-only. **The rate is published**: `bbga` indicator `BHLOCVKPLEEGSTAND` (source Locatus, 1 January 2026) — **660 vacant of 14,314 sales points, 4.6%**; by district 0–7% (Centrum 4.0%, 208 of 5,001); rates for 110/110 *wijken* and 465/545 *buurten*.

**Amsterdam, licences and band (same night).** Owner's call: the BAG becomes the second layer, vacancy disclosed. **BAG — PERMITTED**: the Kadaster's *"Creative Commons Public Domain Mark v1.0"*, PDOK's record *"Geen beperkingen"*; Amsterdam's copy SILENT. **Permits — SILENT**: no `license` key in the live schema (55 of the city's 141 schemas carry one); the CC BY statement lived in a retired catalogue record (live 2023-09-26, 404 by 2026-01-18); Databankenwet art. 8(2) puts government databases outside database right. Owner's call: credit it as CC BY 4.0, which satisfies both readings. **Amsterdam → Band A**, brief `docs/build_briefs/amsterdam.md` 8/8.

#### A refinement the Korea probe produced: stations are not lines

Japan's N02 carries **both** — 10,235 station points *and* 21,932 line
segments. Korea's station standard dataset carries **stations only**, and this
project draws and labels every transit line, which is an invariant.

So the national-GIS check is **two questions, not one**:

1. Does the layer carry **station points** with coordinates?
2. Does it carry **line geometry**?

A country can pass the first and fail the second, and a screen that asks only
the first will record a false pass. Add the line question to `add-country`
before the next country is profiled.

### Tier 4 — ruled out, with the evidence

| | Why | Basis |
|---|---|---|
| **United Kingdom** | **Re-checked 2026-09-21 and still out, for a sharper reason.** Beyond VOA (property without names), Companies House (registered offices) and the FSA (food only), councils publish **NNDR business-rates** data under the Local Government Transparency Code — premises address, rateable value, property description and ratepayer name. It fails on three counts: **names are given only for limited companies and redacted for sole traders and partnerships under GDPR**; the only classification is a property description (`shop`) which **cannot produce this project's three buckets**; and it is published **per council across 300+ authorities** in separate bespoke spreadsheets. The best UK source is premises without a usable category | MEASURED |
| **Israel** | Transit measured and good — 332 points, 27 lines, CC-BY — but **the business leg has no route**. The national portal's only business-licensing register is Be'er Sheva's, a city with no rail; Tel Aviv's own portal returns **HTTP 472**, refusing automated requests. Moved here 2026-09-21: good rail with no reachable matching business data is not a candidate | MEASURED |
| **Peru** | The Lima Line 1 station set is real and ODC-BY, but **dated March 2018 and Line 1 only** — Line 2 has been opening since 2023 and is absent, so the source understates the city and is seven years stale. Moved here 2026-09-21 | MEASURED |
| ~~**Japan**~~ | **MOVED UP to Tier 3, 2026-09-21.** The earlier ruling rested on the Economic Census being aggregate — true, and the wrong source. Japanese municipalities publish **食品営業許可 (food business permits) as premises-level open data with coordinates**: Minato Ward alone is **5,723 premises**, CC BY, carrying `施設名称`, **`施設名称_英字`** (English name), `営業の種類`, a full address plus split components, **`緯度`/`経度`**, `法人番号`, and permit and closure dates. Crucially it follows Japan's **national 推奨データセット standard schema** (`全国地方公共団体コード`, `町字ID`), so every municipality publishing it uses identical columns and the per-ward assembly is mechanical rather than bespoke. **The real ceiling is two buckets** — Japan has no general retail permit, so retail would be absent, which is Toronto's and Boston's shape. 生活衛生関係営業 permits (理容所, 美容所) are the likely Personal services source and are unprobed | MEASURED |
| **Taiwan** | **Nothing for Taipei, Kaohsiung, Taoyuan or TDX anywhere in the catalogue.** The 9 Taiwanese feeds are rural bus operators | MEASURED |
| **Hong Kong** | **No MTR feed anywhere in the catalogue.** The Transport Department feed carries tram/LRT 7 and no subway | MEASURED |
| **Jakarta** | **No MRT Jakarta or LRT Jakarta feed anywhere.** Transjakarta is BRT | MEASURED |
| **Rio de Janeiro** | **No MetrôRio or SuperVia feed anywhere** | MEASURED |
| **Kuala Lumpur, Tel Aviv, Lima, Medellín, Bogotá** | No metro operator feed anywhere in the catalogue | MEASURED |
| **Dubai** | The catalogue's feed is an **anonymous personal GitLab job artefact** returning a non-zip; the transitland fallback 404s | MEASURED |
| **Manila** | The LRTA feed codes its four rail lines as **commuter rail (type 2)**, which this project excludes. A coding question, but it fails as published | MEASURED |
| **Belgium** | Establishment units exist; **bulk access requires application and payment** | MEASURED |
| **Australia, New Zealand** | Auckland is commuter-only. **Melbourne's PTV feed is a nested zip** the screen cannot read, so its rail is *unverified rather than absent*. Business licensing is not municipal — **ASSERTED** | MIXED |
| **Russia, Ukraine** | Access and conflict, not data | — |

### Japan's rail data is solved, and not by GTFS

Worth stating separately because it breaks the screen's own assumption. This
project needs **station coordinates and line geometry**, not timetables, and
GTFS is only one vehicle for those. Japan publishes a better one.

**国土数値情報 N02 鉄道データ** (MLIT National Land Numerical Information,
railway data), verified by download 2026-09-21:

| | MEASURED |
|---|---|
| Endpoint | `https://nlftp.mlit.go.jp/ksj/gml/data/N02/N02-24/N02-24_GML.zip` (12.4 MB; 2020–2024 all return `application/zip`) |
| Stations | **10,235**, across **178 operators** |
| Line segments | **21,932**, across 179 operators |
| JR coverage | JR East **1,803 stations**, JR West 1,264, JR Kyushu 621, JR Central 439, JR Hokkaido 343, JR Shikoku — **all six JR companies** |
| Also | Tokyo Metro, Toei, Osaka Metro, Kintetsu, Meitetsu, Tobu |
| Attributes | `N02_001` rail class, `N02_002` operator category, `N02_003` line name, `N02_004` operating company, `N02_005` station name |
| CRS | **EPSG:6668** (JGD2011) |
| Formats | Shapefile **and GeoJSON**, supplied in **both Shift-JIS and UTF-8** — so no encoding trap |
| Licence | **PDL 1.0**, the Japanese Government Standard Terms — commercial use, redistribution and derived works all permitted |

Attribution: `出典：国土交通省国土数値情報ダウンロードサイト`, and for a derived
work `「国土数値情報（鉄道データ）」（国土交通省）をもとに作成`.

**THE TRAP: station geometry is `LineString`, not `Point`** — all 10,235 of
them. A Japanese station record is the platform centreline, so it must be
centroided before any ring buffer. A pipeline that assumed points would fail
or, worse, silently buffer from a line end.

ODPT (`api-public.odpt.org`) is the second route and also works — Toei's feed
downloaded without a key — but N02 is national, covers JR, and needs no
registration.

**So Japan is ruled out on business data alone.** Only the Economic Census was
checked, and it is aggregate. Japanese municipalities publish
食品関係営業許可施設 (food-business permit premises) as open data, which would
be a one-bucket source at best — worth a probe before the ruling is final.

### THE METHOD THIS SCREEN GOT WRONG: transit data is not GTFS

The single most useful thing to come out of this screen, and it invalidates
part of the screen itself.

**This project uses no timetables.** It needs **station coordinates and line
geometry**. GTFS carries those, but so does any national railway GIS layer —
and national mapping agencies publish those routinely, at better quality, with
national coverage and clearer licences.

Every country ruled out above for "no readable feed" was ruled out on a
**GTFS** question, when the real question is a **GIS** one. Japan proves the
gap is real and large: the Mobility Database has 18 Japanese feeds, almost all
volunteer-run village buses, and **no JR at all** — while MLIT publishes every
railway station in the country, JR included, for free.

**So the probe order for transit should be:**

1. The national mapping or statistics agency's railway layer — MLIT in Japan,
   and its equivalent elsewhere. Usually shapefile/GeoJSON, usually a clear
   government licence, usually national.
2. The national open-data portal's transit standard datasets.
3. The city or agency's own GTFS.
4. The Mobility Database catalogue — **last**, being a mirror of a mirror,
   and demonstrably incomplete and stale.

The screen ran that list backwards.

#### Countries this reopens

| Blocked on GTFS | The GIS route to check |
|---|---|
| **South Korea** | `data.go.kr` carries **전국도시철도역사정보표준데이터** (national urban railway *station* standard data, ID 15013205) and **전국도시철도노선정보표준데이터** (*line* standard data, ID 15013203) |
| **Hong Kong** | Lands Department **iB1000** digital topographic map, which includes a transportation layer, via the CSDI portal and `data.gov.hk` |
| **Taiwan** | NLSC and TDX, neither in the catalogue |
| Jakarta, Kuala Lumpur, Rio, Lima, Bogotá, Medellín, Tel Aviv | National spatial agencies, all unchecked |

#### Reachability is its own finding — and a transient outage is not one

Three government portals refused connections, tested from **two independent
networks** on 2026-09-21 to separate "site is down" from "this path is
blocked". **One of those readings was wrong within the hour**, and the
correction matters more than the original table.

| Host | First reading | Retested ~1h later |
|---|---|---|
| `www.data.go.kr` | unreachable, 21s timeout, both networks | **HTTP 200 in 1.15s** |
| `apis.data.go.kr` | not tested | HTTP 400 — live, wants parameters |
| `datos.cdmx.gob.mx` | unreachable, 21s timeout | **still 000 at 21s** — four attempts over two hours |
| `s3.amazonaws.com/setravi/…` | 403 | still 403 |
| `www.inegi.org.mx` | — | HTTP 200 |
| `data.seoul.go.kr` | HTTP 200 | HTTP 200 |
| `nlftp.mlit.go.jp` | HTTP 200 | HTTP 200 |

**Korea's national portal was suffering a transient outage and is fine.** It
was recorded here as a hard finding, on evidence from two networks, and it was
wrong about an hour later.

**Mexico City's is not transient** — four failures across two hours, while
INEGI on the same day answered instantly. That one is a durable finding *as of
2026-09-21*, and still not a permanent one.

**The lesson, and it is the same one this file keeps producing.** A negative
result is a measurement of *one moment* as well as one method. Two networks
agreeing says nothing about two *times*. The evidence-discipline rule in
`add-country` — treat a negative as ASSERTED until a second differently-shaped
probe agrees — needs "differently-*timed*" alongside "differently-shaped", and
an infrastructure failure should never be written down as a property of the
data.

**Do not record a country as "no data" on the strength of an unreachable
portal.** Retry it, and try the city portal, which is this project's scope
anyway.

### What in these tables is an artefact rather than a finding

Kept visible so nobody reads the tables as settled fact:

- **Resolved.** Barcelona and Madrid were first tested against *bus* operators.
  Both have since been measured properly — Madrid subway 13, Barcelona FGC
  subway 4. **TMB's own feed still 404s**, so Barcelona is understated.
- **Resolved.** Berlin, Hamburg, Stockholm and Oslo were reported rail-free by
  a tool that could not read extended route types. Fixed.
- **Still open.** Mexico City's feed exists and will not download.
  Buenos Aires' SUBTE feed exists at the city's own CDN and **contains no
  `routes.txt`**. Melbourne's is a nested zip. Istanbul's IETT URL is a
  landing page, not a file.
- **Still open.** Manila's rail exists and is typed 2; Hong Kong's MTR exists
  and is published nowhere the catalogue reaches.

Every one is the Toronto lesson: **what a catalogue says about a city is not
what the city runs** — and, added this round, **what a screening tool cannot
parse, it reports as absent.**

## What screening 87 countries showed — five patterns

Synthesis rather than findings. Each is drawn from the measurements above and
each changes how the next screen should be run.

### 1. The transit catalogue has a Western bias, and it distorted this screen

**US 1,180 feeds. South Korea 0.** That is not a fact about transit.

Korea runs one of the world's best metro systems and publishes **1,099
stations with WGS84 coordinates, free and unrestricted**, from its own
government, the whole time. Japan shows 18 feeds of volunteer-run village
buses while MLIT publishes **10,235 stations and 21,932 line segments**.

The Mobility Database measures **GTFS adoption**, which tracks Anglophone and
European open-transit advocacy culture — not transit, and not data
availability. Screening on it **systematically underrates exactly those
countries with the strongest state data infrastructure**.

The screen opened on an instinct that Europe and East Asia were the targets.
That instinct was right; the catalogue made it look wrong.

### 2. The best business registers are national, not municipal

This project's US and Canadian experience taught "municipal licence register"
as the shape to look for. The three strongest sources found globally are all
**national statistical or small-business agencies**: **DENUE** (INEGI),
**SIRENE** (INSEE), **상가(상권)정보** (소상공인시장진흥공단).

All three come from states that run a serious economic census. **The
municipal-licensing model is a North American peculiarity rather than the
norm**, which is why `add-country`'s question 2 mis-sorted half the world
until it was rewritten.

### 3. Licence burden correlates with nothing predictable

| | |
|---|---|
| **Korea** | **이용허락범위 제한 없음** — no restriction at all |
| **Mexico** | attribution **and** disclosure of any transformation |
| **Canada** | OGL, **automatic termination on breach** |
| **UK, much of the EU** | fee-gated registers |

All comparable democracies with strong open-data programmes. Licence looseness
is a **policy choice, not a development indicator**, so it cannot be predicted
from region or wealth — only read. That is the entire case for the
`read-licence` skill.

### 4. The aggregate trap is the most common single failure

Istanbul (counts per district), Japan's Economic Census (counts per area),
Seoul's 상권분석서비스 (per commercial district per quarter), the UK's VOA
(property without names). **Every one looked viable from its title and
description.**

Seoul's was the best disguised, because its categories split into **외식업 10
/ 서비스업 47 / 소매업 43** — this project's own three buckets, exactly.

**The tell is always the same question: is a row a premises, or a summary?**

### 5. Screening cost is highest where the payoff is highest

The cheapest countries to screen — the UK, Australia — **failed**. The richest
— Korea, Japan, Mexico — cost the most, because their data sits outside the
channels the screen knew about and often behind another language.

That argues directly against breadth-first screening and reinforces the
existing depth-per-country rule: the marginal country is expensive precisely
when it is worth having.

## Probe log — every city rail-screened, 2026-09-21

`scripts/screen_rail.py` against real `routes.txt`. **77 feeds fetched across
40 countries.** Counts are route counts in the feed, not stations. Commuter
rail (basic type 2, extended 109) is excluded throughout, as in every built
city.

### Urban rail confirmed

| City | Country | Measured | Feed health |
|---|---|---|---|
| **Paris** | FR | subway 16, tram 17, funicular 1 | current |
| **Vienna** | AT | **subway 35**, tram 185 | current |
| **Madrid** | ES | **subway 13** | current |
| **Singapore** | SG | **subway 13** | current |
| **Lisbon** | PT | subway 10 | current |
| **Amsterdam / Rotterdam** | NL | subway 14, tram 46 | current |
| **Berlin** | DE | urban rail 9, tram 48 | current |
| **Stockholm** | SE | metro 7, tram 21 | current |
| **Santiago** | CL | subway 7, tram 2 | current |
| **São Paulo** | BR | subway 6 | current |
| **Bucharest** | RO | subway 5, tram 15 | current |
| **Oslo** | NO | metro 5, tram 9 | current |
| **Barcelona** | ES | **FGC subway 4, funicular 3** | current — *TMB 404s* |
| **Sofia** | BG | subway 4, tram 24 | current |
| **Hamburg** | DE | underground 4 | **expired 20251213** |
| **Helsinki** | FI | subway 4, tram 26 | **expired 20260731** |
| **Copenhagen** | DK | **subway 4** — ⚠️ **"tram 4" was WRONG, corrected 2026-09-23**: OSM returns **ZERO** tram relations in Københavns Kommune AND zero in Region Hovedstaden, and no Letbane relation exists either. Copenhagen's tram closed in 1972. Metro is M1–M4, 8 relations, all named and all coloured; S-tog is 7 refs and is excluded as S-Bahn | current |
| **Budapest** | HU | subway 4, tram 42 | **expired 20260704** |
| **Bangkok** | TH | subway 4, LRT 5 | current |
| **Prague** | CZ | subway 3, tram 40 | **expired 20260616** |
| **Athens** | GR | subway 3 | current |
| **Naples** | IT | subway 3, tram 3, funicular 3 | current |
| **Hyderabad** | IN | subway 3 | current |
| **Málaga** | ES | subway 2 | **expired 20250226** |
| **Cairo** | EG | subway 2 | **expired 20251027** |
| **Bilbao** | ES | subway 1 | current |
| **Kochi** | IN | subway 1 | current |
| **Guadalajara** | MX | tram/LRT 3 | current |
| **Zagreb** | HR | tram 19 | **expired 20190616** |
| **Poznań** | PL | tram 22 | **expired 20260605** |
| **Riga** | LV | tram 7 | current |
| **Bratislava** | SK | tram 6 | **expired 20221231** |
| **Tallinn** | EE | tram 5 | **expired 20260831** |
| **Hong Kong** | HK | tram/LRT 7, funicular 1 | current — **no MTR in feed** |
| **Messina** | IT | tram 1 | current |

### No urban rail in the feed tested

| City | Country | What came back |
|---|---|---|
| **Manila** | PH | **commuter rail 4** — the LRT/MRT lines, typed as commuter and so excluded |
| **Rio de Janeiro** | BR | bus only — MetrôRio is a separate operator, absent |
| **Auckland** | NZ | commuter rail 5, bus 194 |
| **Jakarta** | ID | bus 252 — Transjakarta is BRT; the MRT is absent |
| **Bogotá** | CO | bus 1000, aerial 1 |
| **Buenos Aires** | AR | bus 1052 — *and the Subte feed has no `routes.txt` at all* |
| **Vilnius, Ljubljana, Belgrade** | LT/SI/RS | bus and trolleybus |

### Fetch failed

**TMB Barcelona**, **MetroValencia**, **Metro de Sevilla**, **SL Stockholm**,
**Istanbul IETT**, **Kyiv**, **Casablanca**, **Mexico City** (403 on S3;
`datos.cdmx.gob.mx` **would not connect**, twice, 21s each), **Dubai RTA**
(the catalogue URL is an anonymous personal GitLab job artefact returning a
non-zip).

### The tool was wrong, and is now fixed

Berlin, Hamburg, Stockholm and Oslo first came back **"no urban rail"**.
They publish **GTFS Extended Route Types** — the TPEG-derived 3- and 4-digit
set where a metro is `401`, an underground `402` and a tram `900` — and
`screen_rail.py` knew only the basic 0–12 values, so it silently discarded
them into "other".

Decoded, the counts matched the real networks exactly: Berlin `400:9` against
9 U-Bahn lines, Hamburg `402:4` against 4, Stockholm `401:7` against 7
tunnelbana lines, Oslo `401:5` against 5 T-bane lines. Four European capitals
were one dictionary away from being wrongly ruled out.

`screen_rail.py` now handles both sets, and treats extended `109` (Suburban
Railway, the S-Bahn family) as commuter rail — excluded, for the same reason
basic type 2 is.

**Wrong-feed selection is the other recurring fault.** Barcelona and Madrid
were first tested against bus operators; Dublin against two airport coach
services; Malaysia against a bus company in Kuala Terengganu rather than
anything in Kuala Lumpur; Australia against Magnetic Island and Maryborough.
Picking "a feed that names the city" is not the same as picking the rail
operator, and in a country with 169 feeds it is close to random.

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

**MEASURED 2026-09-23, when Paris was built — the structural worry above is now
evidenced rather than asserted.** Against OpenStreetMap's mapped shops inside
the same commune:

| | OSM | SIRENE | ratio |
|---|---|---|---|
| Total | 48,973 | 87,164 | **1.78×** |
| Personal services | 4,866 | 12,099 | 2.49× |
| `amenity=restaurant` vs NAF `56.10A` | 9,058 | 16,280 | 1.80× |

Some of that is OSM being incomplete and some is the register including
premises a passer-by would never see; **nothing in the data separates them**,
which is precisely the "wrong shape" cost, quantified. Two catch-all codes
asserting no premises were excluded on INSEE's own class labels, which moved
personal services from 4.40× to 2.49× and left retail untouched. The residual
is disclosed on the city page rather than filtered away.

⚠️ **This supersedes the figure France was originally approved on.** An earlier
pass recorded "50,156 storefronts, 92.5% of OSM" and attributed the filter to
`trancheEffectifsEtablissement`. That number is **not reproducible**: `NN` is
77.3% of Paris's bucket rows, so every banded row together is 33,918 and no
predicate on that column reaches 50,156. France is still a build — register,
join, coverage and licence are untouched — but a 0.93× match was never real.

**Carry this to the next national register rather than re-learning it.** Mexico's
DENUE and Norway's `beliggenhetsadresse` are the same shape, and the lesson is
that a national establishment register over-counts storefronts by a factor no
filter in the register itself can remove.

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

**MEASURED 2026-09-22** (was ASSERTED from documentation of the *closed*
system): coordinates **are** published in EPSG:5174 (Korea Central Belt TM),
and Seoul's own dataset pages say so in as many words — *"좌표안내 :
중부원점TM(EPSG:5174) 좌표계에 따른 해당위치의 좌표정보이며 위경도 좌표는
제공하고 있지 않음"*. Two files downloaded and their coordinate ranges checked;
see "Seoul's 인허가 정보 family" below. The project reprojects to per-city UTM
regardless — Seoul ≈ 127°E is UTM 52N, EPSG:32652.

#### SEOUL'S FOOD REGISTER IS OBTAINABLE WITH NO ACCOUNT — downloaded 2026-09-21

The scrub's real payoff. `data.seoul.go.kr` dataset **`OA-13663`**
(`서울시 식품위생업소 현황`) publishes per-year CSVs on a **FILE** tab, and the
download needs **no login, no key, no registration**:

```
POST https://datafile.seoul.go.kr/bigfile/iot/inf/nio_download.do?&useCache=false
     infId=OA-13663   seq=11   infSeq=3        # seq 11 = the 2025 file
```

Files run 2019 through 2025 — 12.98 MB for 2025, ~13–14 MB per year back to
2021, plus a 57 MB zip for everything to 2019. Downloaded and parsed:

| | MEASURED |
|---|---|
| Rows | **39,590**, of which **24,824 are still open** (no `폐업일자`) |
| Encoding | **cp949** — so `SOURCE_ENCODING = "cp949"`, not UTF-8 |
| `업소명` / `업종명` / `업태명` | **100%** |
| **`소재지도로명`** (road address) | **99.3%** |
| `소재지지번` (lot address) / `행정동명` | 100% |
| `폐업일자` / `폐업구분` / `폐업사유` | 37.3% — **so inactive premises CAN be filtered**, unlike Japan's ward file |
| `영업장면적(㎡)` | **3.5%** — floor area is effectively absent |
| `법인명` | 36.5% |
| **Coordinates** | **NONE.** Checked for 위도/경도/좌표 — no such column |

Open-premises categories: 일반음식점 10,778, **건강기능식품일반판매업 5,112**
(health-food *retail*), 휴게음식점 3,931, 즉석판매제조가공업 1,649,
유통전문판매업 1,180, 제과점영업 547.

**So Korea needs a geocoding leg after all — but the easiest of the three.**
Addresses are Korean **road-name** format, e.g.
`서울특별시 종로구 자하문로 55, 지상1층 107호 (통인동, 효자아파트)`. That is a
systematic national scheme with public geocoders, and far more tractable than
Japan's chōme/ban/gō blocks.

**What this changes.** Seoul is buildable **without any account**, so the
residency wall on `data.go.kr` and Seoul's own signup is no longer a blocker
for the food bucket. What is lost by not having `상가(상권)정보` is real
though: that register carries **coordinates already**, covers **all six
cities**, and spans **all three buckets**. This route gives one city, one
bucket, and a geocoding job.

**The sibling dataset for Personal services is 공중위생업소** (이·미용, 숙박,
목욕업) on the same portal and presumably the same download mechanism —
probed 2026-09-22. It is **not** published that way, and the probe found a
better route than `OA-13663` instead: see
"Seoul's 인허가 정보 family" below, which **supersedes this section** as the
recommended source. `OA-13663` remains correct and usable; it is simply the
worse of the two, because it carries no coordinates.

#### Seoul's 인허가 정보 family — the LOCALDATA schema, keyless, WITH COORDINATES

MEASURED 2026-09-22. Probing the Personal-services sibling found something
better than the thing it was looking for. **`data.seoul.go.kr` republishes the
LOCALDATA licensing register per business type, citywide, and its SHEET tab
exports CSV with no account:**

```
POST https://datafile.seoul.go.kr/bigfile/iot/sheet/csv/download.do
     srvType=S  infId=<OA-id>  serviceKind=1  pageNo=1
     gridTotalCnt=999999  ssUserId=SAMPLE_VIEW  strWhere=  strOrderby=
```

`ssUserId=SAMPLE_VIEW` is the anonymous identity **the page itself sends when
nobody is logged in** — it is not a bypass, it is the logged-out path. Read out
of `doAction()` on any `datasetView.do` page. `json` substitutes for `csv` in
the URL. The catalogue holds **3,063** `인허가 정보` datasets.

The schema is the full LOCALDATA one, 24 columns:

```
개방자치단체코드, 관리번호, 인허가일자, 영업상태코드, 영업상태명,
상세영업상태코드, 상세영업상태명, 폐업일자, 휴업시작일자, 휴업종료일자,
재개업일자, 전화번호, 소재지우편번호, 지번주소, 도로명주소, 도로명우편번호,
사업장명, 최종수정일자, 데이터갱신구분, 데이터갱신일자,
좌표정보(X), 좌표정보(Y), 사무소전화번호, 사업장전화번호
```

Two downloaded and measured. **The coverage figures that matter are the ones
for `영업상태명 == 영업/정상` (active)** — the whole-file rates look mediocre
only because closed premises are missing their geometry:

| | `OA-16044` 숙박업 | `OA-16007` 동물병원 |
|---|---|---|
| Rows | 7,157 | 2,235 |
| **Active** (`영업/정상`) | **2,788** | **981** |
| Closed (`폐업`) | 4,369 | 1,239 |
| `좌표정보(X/Y)` — whole file | 86.2% | 88.1% |
| **`좌표정보(X/Y)` — active only** | **99.5%** | **99.0%** |
| **`도로명주소` — active only** | **99.7%** | **100%** |
| Either, active only | **100%** | **100%** |
| `사업장명` / `영업상태명` | 100% | 100% |
| Encoding | cp949 | cp949 |

Coordinate ranges X 182,525–213,646 / Y 438,573–464,745 — consistent with
EPSG:5174 over Seoul. `위생업태명` subdivides 숙박업 into 여관업 1,341,
관광호텔 478, 숙박업(생활) 395, 일반호텔 255, 여인숙업 237.

**Why this supersedes `OA-13663`.** It carries coordinates, so **Korea needs no
geocoding leg at all** — which reverses the previous section's conclusion. It
also filters on a status *field* rather than on the presence of a closure date.
The trade is that one dataset is one business type, so a city needs several,
which is the `multi-source-city` shape the US cities already use.

Confirmed citywide (no district prefix): `OA-16044` 숙박업, `OA-16043`
관광숙박업, `OA-16007` 동물병원, `OA-16106` 계량기제조업, `OA-16067` 집단급식소,
plus 통신판매업, 위탁급식영업, 무료·유료직업소개소. **Per-district** (25 datasets
each, because 보건소 licenses them): 병원, 의원, 부속의료기관, 산후조리업, 안경업.

**RESOLVED 2026-09-22 — all six core types found, downloaded and measured.**
The OA-id sweep missed them because the citywide entries are scattered through
OA-160xx rather than contiguous; they came from driving the search box. Note
that a `fetch` POST of the *fully serialized* form still returns the unfiltered
8,258 — even for the nonsense control — because `searchSend()` records the
keyword server-side first. **Only a real form submit filters.**

| `infId` | Type | Bucket | Rows | **Active** | coord % | addr % |
|---|---|---|---|---|---|---|
| `OA-16094` | 일반음식점 | Food | 537,906 | **120,182** | 90.7% | 99.2% |
| `OA-16095` | 휴게음식점 | Food | 147,582 | **37,113** | 97.6% | 98.6% |
| `OA-16063` | 미용업 | Personal services | 99,802 | **33,679** | 98.7% | 99.9% |
| `OA-16065` | 세탁업 | Personal services | 15,360 | **3,263** | 99.3% | 99.4% |
| `OA-16044` | 숙박업 | Personal services | 7,157 | **2,788** | 99.5% | 99.7% |
| `OA-16064` | 이용업 | Personal services | 15,635 | **2,366** | 99.0% | 99.2% |
| `OA-16007` | 동물병원 | Personal services | 2,235 | **981** | 99.0% | 100% |
| `OA-16146` | 목욕장업 | Personal services | 3,991 | **673** | 99.4% | 100% |

Percentages are over **active** rows (`영업상태명 == 영업/정상`); `사업장명` is
100% on every one. **197,276 active premises — Food 157,295, Personal services
39,981.** For scale, that is more than New York's four sources produced.

**One soft spot, and it is the biggest file.** 일반음식점 is the only one below
97% on coordinates, at **90.7%** — about 11,000 active restaurants with an
address but no point. Its road address is 99.2%, so those are geocodable rather
than lost, but a Seoul build should expect a small geocoding fallback for the
Food bucket specifically rather than none at all. Everything else is
essentially complete.

Also found, citywide and on the same route: `OA-16043` 관광숙박업, `OA-16091`
관광식당, `OA-16067` 집단급식소, `OA-16106` 계량기제조업, plus 통신판매업 and
위탁급식영업. **Per-district** (25 datasets each): 병원, 의원, 부속의료기관,
산후조리업, 안경업, and a 일반음식점 set at OA-18652+ duplicating the citywide
one.

**The licence is read: 공공누리 제1유형 (KOGL Type 1)** — attribution,
commercial use and derivative works all permitted, `제3저작권자: 없음` on all
eight, daily refresh. Full terms, the three obligations it imposes (including
a *mandatory hyperlink*) and the privacy verification are in
`docs/data_sources.md`. **Retail remains the unaddressed bucket** — 건강기능식품
appears inside the food files as a category rather than as its own register,
which is the same shape as Seoul's `OA-13663`.

#### Seoul's 공중위생업소 is NOT published as a file — and the first probe of this was wrong

Two findings, the second more useful than the first.

**The answer.** `data.seoul.go.kr` holds **251** datasets matching 공중위생, and
the site's own facet panel reads:

```
제공유형    SHEET (182)    OPENAPI (180)    LINK (71)    CHART (27)
```

**No FILE row at all** — so zero of the 251 offer the `nio_download.do` route
that `OA-13663` uses. `OA-10184` (`서울시 중구 위생처리업 공중위생업소 현황`)
is **중구 only**, one of 25 districts, SHEET/OpenAPI. The citywide ones
(`서울시 위생처리업 현황`, `서울시 숙박업 인허가 정보`) are SHEET/OpenAPI too —
which is exactly why the SHEET export above matters. For scale: Seoul has
**1,179** FILE datasets overall, 137 of them tagged 좌표. The FILE route is
broad; hygiene is simply excluded from it.

**The method error, worth more than the answer.** The first pass concluded
"only `OA-13663` has a FILE tab" from a search that **silently ignored the
search term**. Both `GET ?srchDetailWord=` and `POST searchKeyword=` return the
unfiltered default listing — and a nonsense control term returned a
**byte-identical** page (91,928 b, then 84,955 b) with the same ten dataset
ids. The ten looked like plausible hygiene results because the catalogue's
default ordering happens to surface hygiene datasets. Nothing about the
response said "your filter was dropped."

> **Rule.** Before believing a search result list — or a zero — send a
> **nonsense term** and confirm the response differs. A parameter a server
> ignores produces a confident, plausible, wrong answer, and neither the status
> code nor the page shape reveals it. This is how a whole country nearly got
> written off, the same way the `www.` vhost nearly lost Peru.

A second-order lesson: **a site's own facet counts beat sampling.** One read of
"SHEET (182) OPENAPI (180) LINK (71) CHART (27)" settles what paging through
251 results would not, because it is the publisher's own count over the whole
result set rather than an inference from page one.

#### Busan and Daegu, probed individually 2026-09-22 — both fail, for different reasons

Requested as "real work, may yield two cities." It yielded neither, but the
reasons are worth keeping because they are the shape of every Korean
non-capital city.

**The structural fact behind both.** In Korea the licensing authority is the
**자치구/군**, not the city. So the register is published per district, in
whatever schema and on whatever schedule that district chose. Seoul is the
exception, not the rule: it aggregates. Verified — `OA-13663` covers **all 25
districts**, 강남구 4,744 down to 도봉구 794.

**Busan — NO, on two independent grounds.**

Its search is browser-only (curl gets a nav-only shell from
`/bdip/srh/getPublicDataListSearch.do`). Driven properly, 식품위생업소 returns
**59 공공데이터** — but the portal **federates `data.go.kr`**, so Seoul
datasets appear among Busan's results. Busan's own, from the rendered list:

| District | What it actually is |
|---|---|
| 중구, 사상구, 동래구, 수영구 | real premises registers |
| 연제구 | 식품소분업 only |
| 기장군 | 식품제조가공업 only |
| 북구 | 위탁급식영업 only |
| 사상구 | 행정처분현황 — *enforcement actions*, not premises |

That is **4 of 16 districts** with a usable register. Coverage fails on its own.

Access fails too. Busan does not host the files: the FILE button's own
`onclick` points at
`https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003705859&fileDetailSn=3`.
Fetched: `fileDetailSn` 1 and 2 return **0 bytes**, 3 returns an **87,693-byte
PNG** (`nexroutine_wordmark_720.png`) and 4 a **203,559-byte JPEG**. Busan's
cached `atchFileId` has gone stale and now resolves to somebody else's images.
Asking `data.go.kr` itself, logged out, returns `status: true` but
**`atchFileId: null`**, so `fn_fileDataDownload` cannot fire. And the path runs
through `/cmm/cmm/check-limit.json` → `needCaptcha` → `showLimitCaptcha`: a
**CAPTCHA rate-limiter**, which this project does not attempt to defeat. Even
with an account, 16 districts × an interactive gate is not a pipeline.

**Daegu — NO on coverage, but the download route works.**

Daegu's search *does* honour `searchWrd` (nonsense control returned 0 ids).
Its `dataView.do` is a Vue app over eGovFrame; `/data/rest/*` refuses curl even
with a warmed cookie, so the live app was read instead — `portalDataCheck:
false` on every dataset, with `dataUrl` pointing at the same
`www.data.go.kr/cmm/cmm/fileDownload.do`. **Unlike Busan's, Daegu's ids are
current**, and `fileDetailSn=1` works. Five downloaded keylessly:

| Dataset | Rows | 도로명 | Coordinates |
|---|---|---|---|
| 남구 식품위생업소 | 4,060 | 94% | — |
| 서구 식품위생업소 | 4,122 | 100% | — |
| 북구 식품접객업 | 6,432 | 100% | — |
| **달서구 식품관련업소** | **11,089** | 100% | **위도/경도, 99.9% inside Daegu's bbox** |
| 수성구 공중위생업 | 2,523 | 100% | — |

달서구's mix is right: 일반음식점 5,738, 휴게음식점 1,733, 건강기능식품 918,
제과점영업 167. **None of the five carries `폐업일자`**, so closed premises
cannot be filtered — Japan's problem, not Seoul's.

**What kills it: 중구 publishes no premises register at all.** Daegu's downtown
district offers **9 datasets** — libraries, festivals, 평생학습강좌, 노동조합 —
and a 중구 + 위생 search returns nothing. Daegu Metro Lines 1, 2 and 3 all
converge in 중구 (반월당, 중앙로, 대구역). **The densest station areas in the
city would be blank**, which is not a commercial-density map of Daegu. 4 of 9
districts obtainable, and the missing one is the one that matters most.

#### Exhaustive Korean domain scrub, 2026-09-21 — 21 hosts

Run instead of emailing the agency. **11 of 21 reachable.**

| Dead | Alive |
|---|---|
| `bigdata.sbiz.or.kr` (**3 tests**, sub-second refusal) | **`semas.or.kr`** — the agency's own site |
| `sg.sbiz.or.kr` — the 상권정보 system | **`sbiz.or.kr` → redirects to `sbiz24.kr`**, both 200 |
| **`nsdi.go.kr` and `data.nsdi.go.kr`** — the national spatial infrastructure | `data.seoul.go.kr`, `golmok.seoul.go.kr` |
| **`vworld.kr`** — the national GIS platform | **`data.busan.go.kr`**, **`data.daegu.go.kr`**, **`data.incheon.go.kr`** |
| `localdata.kr` and `localdata.go.kr` | **`data.gg.go.kr`** (Gyeonggi) |
| `openapi.seoul.go.kr`, `bigdata.busan.go.kr` | `kosis.kr`, `mdis.kostat.go.kr` |
| `data.daejeon.go.kr`, `data.gwangju.go.kr` | |

**Three of the six Korean metro cities run their own reachable portals** —
Busan, Daegu and Incheon — plus Gyeonggi, which is the Seoul metropolitan
province. **None is CKAN**, so there is no quick API route:

- **Busan** and **Daegu** are file-based portals (`dataSet`, `파일` markers),
  so a direct download may exist per dataset. Each needs its own probe.
- **Incheon** answered `{"code":"257","msg":"NOT_EXIST_TOKEN"}` — a real JSON
  API, token-gated.
- **Gyeonggi** is a large portal with `인증키` / `회원가입`, so key-gated too.

**The most useful finding is about the agency, and it argues FOR the enquiry
rather than against it.** `sbiz.or.kr` redirects to `sbiz24.kr` and both answer
200, so 소상공인시장진흥공단 is plainly operating — **only the `bigdata`
subdomain that `data.go.kr` officially points at is broken.** That is a
reportable fault on their side, not a policy, which makes "your published
download link is dead, how should a non-resident obtain the file" a
straightforward request rather than a favour.

**Also worth recording as a method note:** the first run of this probe
reported all four city portals as "not CKAN, no markers", which was **a
`subprocess(text=True)` call decoding Korean bytes as cp1252 on Windows** —
an invalid read presented as a negative finding. Same family as the XLSX
empty-cell bug earlier the same day. Decode explicitly.

#### Seoul's own portal, probed 2026-09-21 — the route around the blocker

With `data.go.kr` unreachable, **`data.seoul.go.kr` answers 200** and carries
both legs. MEASURED:

| | |
|---|---|
| Catalogue size | **8,258 datasets** (6,479 data, 1,779 statistics) |
| Direct file downloads | **1,179** carry a `FILE` tab; 5,646 offer `OPENAPI` |
| Freshness | The licensing datasets were updated **2026-09-21**; the subway dataset **2026-09-22** |
| Publisher | Seoul Metropolitan Government, © *Some Rights Reserved* |

**Transit — exists, but API-gated.** `서울교통공사_노선별 지하철역 정보`
(Seoul Transportation Corporation, stations by line, `OA-15442`) covers **lines
1–8 plus line 9 stages 2–3**, published 2018 and updated 2026-09-22. Its file
tab reads **파일이 없습니다** — *no file* — so it is **Open API only, with a
free key**. That is WMATA's gate exactly, which this project has cleared once
before. Note the scope: Seoul Transportation Corporation runs lines 1–9, not
the Korail and Shinbundang lines that also serve the metropolitan network.

**Business — present, and it is a MULTI-SOURCE city.** The national "195 permit
types" resolve at city level into separate per-category datasets, not one
register:

- `서울시 식품위생업소 현황` — food service premises, **and it has a `FILE`
  tab**, the one bucket that is directly downloadable
- `서울시 공중위생업소 현황` — 이·미용 (hair and beauty), 숙박 (lodging),
  목욕업 (bath houses): **the Personal services bucket**
- `서울시 위생처리업`, `세척제 제조업`, `기타 위생용품 제조업`, `대부업체`
  and others

**So at Seoul-portal scope this is Boston's and New York's shape** — coverage
assembled from several registers via `multi-source-city`. But the Retail probe
below found something better, and something worse.

#### The Retail probe — one trap avoided, one source found, and it is out of reach

**REJECTED: `서울시 우리마을가게 상권분석서비스`.** It looks perfect — a
100-category taxonomy split natively into **외식업 10 (food service),
서비스업 47 (services), 소매업 43 (retail)**, the project's own three buckets,
with GRS80TM coordinates. It is **aggregate**: "aggregated by commercial
district (상권) per quarter, not individual store-level data… **no individual
store coordinates**", and its spatial unit changed again in 2024. Seoul's
portal also carries a 소상공인시장진흥공단 extract at **행정동 단위**
(administrative-dong level) — aggregate for the same reason.

That is Istanbul's defect and Japan's Economic Census defect, and this one was
better disguised than either, because the category split matched what this
project needs exactly.

**FOUND: `소상공인시장진흥공단_상가(상권)정보`** — the Small Enterprise and
Market Service's store register, and it is premises-level:

| Field | |
|---|---|
| `상호명` | business name |
| `업종코드` / `업종명` | category code and name |
| `지번주소` / `도로명주소` | lot address and road address |
| **`위도` / `경도`** | **latitude / longitude** |
| `표준산업분류명` | KSIC standard industrial classification |

Nationwide, CSV in UTF-8, on a **10 major / 75 middle / 247 subcategory**
hierarchy. That is one register covering all three buckets with real
coordinates — **comparable to Mexico's DENUE**, and far better than assembling
Seoul's per-category hygiene registers.

**Dataset `15083033` on `data.go.kr` — and the portal came back up, so this is
now MEASURED from the source page rather than from search results:**

| | |
|---|---|
| Title | `소상공인시장진흥공단_상가(상권)정보_20260630` |
| Scope | **영업 중인 전국 상가업소** — active commercial premises, nationwide |
| Classification | KSIC-based (표준산업분류 10th revision), **대분류 10 / 중분류 75 / 소분류 247** |
| Update cycle | **분기** — quarterly. Registered 2026-08-05 |
| Format | **CSV, UTF-8**, explicitly stated, with reading instructions shipped in the zip |
| Legal basis | 소상공인 보호 및 지원에 관한 법률 제13조 |
| Cost | **무료** — free |
| **이용허락범위** | **제한 없음 — no restriction on use** |

**That is the strongest business source found anywhere in this screen.** It is
premises-level with real coordinates, nationally complete, classified on a
247-subcategory standard, refreshed quarterly, and its stated licence scope is
*unrestricted* — which is a lighter obligation than Mexico's DENUE, whose terms
require attribution **and** disclosure of any transformation.

It also **collapses the multi-source problem**: one register covers all three
buckets, so Seoul does not need `multi-source-city` after all, and the
per-category hygiene registers become a cross-check rather than the plan.

**Third-party mirrors exist** (a Seoul extract dated 202506 is on Hugging
Face), and the licence permits them — `제한 없음` places no restriction on
redistribution, unlike WMATA, which forbids it outright.

**Do not build on this one** — but the reason is NOT "mirrors are bad", and an
earlier version of this file got that wrong. See the rule below.

#### CORRECTED — the mirror rule was stated too broadly

This file said, twice and inconsistently: *"a mirror is acceptable to confirm a
schema, never to source a build"* — and then, for Mexico City, that **the
mirror was the only working route** and the rule is to try every address. Both
claims sat in the same document.

**The two cases genuinely differ, and not in the way "mirror" suggests:**

| | Toronto | Mexico City |
|---|---|---|
| Agency feed | correct | **host times out** |
| S3 `direct_download` | — | **403** |
| Mobility Database mirror | **3 months expired, zero subway routes** | **current, no expiry flag — the only route that worked** |

**What distinguishes them is whether the artifact SELF-ATTESTS:**

- **GTFS does.** `feed_info.txt` carries `feed_end_date`, so staleness is
  machine-checkable, and mode counts are checkable against a known network —
  "Toronto has a subway and this file has zero type-1 routes" is detectable.
- **A business-register CSV does not.** There is no embedded validity date, and
  the Hugging Face file's `202506` lives in its *filename* — the mirror's word,
  not the data's. Completeness is worse: 28,000 rows against a true 31,000 is
  **invisible**.

**And this reframes the Toronto failure.** It was not "a mirror was used". It
was **a stale mirror used without reading the expiry field that was already in
the file.** The fix built in response was `screen_rail.py`'s expiry check — not
abstinence — and that same check is what let Mexico City's mirror be trusted.

**THE RULE, restated:** *a mirror is usable when the artifact self-attests to
its own freshness and completeness; it is not when you must take the mirror's
word for both.* That keeps Mexico City, rules out the Korean CSV, and says why
rather than gesturing at a precedent.

**How to actually get it, traced 2026-09-21.** `data.go.kr` *catalogues* this
dataset but does not host the file — its own metadata says `atachFileYn = N`,
and the bulk CSV lives on **`bigdata.sbiz.or.kr`, which is down** (connection
refused in 0.65s, twice, an hour apart, while `www.sbiz.or.kr` answers 302).

The **Open API is live**:
`apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong` returns **401**, i.e.
the endpoint exists and wants a key. `B553077` is 소상공인시장진흥공단's
institution code, matching the `insttCode` in the dataset's own metadata.

So the business leg needs **a free API key** — WMATA's gate, already cleared
once by this project — not a bulk download.

> **SUPERSEDED 2026-09-22, twice over.** The key is **not free to this project**:
> every `data.go.kr` account type requires a Korean resident ID or a Korean
> business number, so the gate is a **residency** wall, not a registration
> one. And it is moot — Seoul's own `인허가 정보` datasets provide the same
> shape of data with **no account at all**. This paragraph is kept because the
> reasoning "401 means it wants a key, and a key is cheap" was wrong in both
> halves, and that is the instructive part: a 401 says nothing about who is
> *allowed* to hold the key.

#### Korea's transit leg — MEASURED, and it is excellent

`전국도시철도역사정보표준데이터` (dataset **15013205**), from
**국가철도공단** under MOLIT, legal basis 도시철도법:

| | |
|---|---|
| Rows | **1,073 stations** |
| Scope | Urban railway nationwide, **including 광역철도** (metropolitan rail), so beyond Seoul Metro's own lines |
| Fields | 역번호, 역사명, 노선번호, 노선명, English and Hanja names, **환승역 여부 및 환승 노선** (transfer flag and lines), **역의 위도·경도**, 운영기관명, 도로명주소, 데이터기준일자 |
| Format | XLSX |
| Update | 연간 (annual) |
| Cost / licence | **무료**, **이용허락범위 제한 없음** |
| Host | `data.kric.go.kr` — **HTTP 200**, and the dataset page `id=32` also 200 |

**Downloaded and parsed 2026-09-21** — `전체_도시철도역사정보_20260630`, via
`data.kric.go.kr/rips/dataset/download.file?type=filedata&id=32&operation=1`
(313 KB XLSX, no key, no login):

**1,099 stations.** Columns exactly as advertised:

| Column | Verified content |
|---|---|
| `역위도` / `역경도` | **WGS84 to 15 dp** — e.g. `37.516125263312901, 127.019760916726` |
| `역사명` / **`영문역사명`** / `한자역사명` | Korean, **English** and Hanja names |
| `노선번호` / `노선명` | line number and name |
| `환승역구분` / `환승노선번호` / `환승노선명` | transfer flag and the lines transferred to |
| `운영기관명` | operating body |
| `역사도로명주소` | road address |

Sample rows are 신분당선 (Shinbundang) stations tagged 수도권 광역철도, so
coverage extends past Seoul Metro to private and metropolitan operators, as
the metadata claimed.

**`영문역사명` is an unplanned win.** It answers the foreign-language label
question for free — Montréal needed a taxonomy decision about label language,
and Korea ships English station names in the file.

**THE REMAINING GAP: this is stations only, with no line geometry.** This
project *draws* every transit line and labels it — an invariant — and in a
GTFS city that geometry comes from `shapes.txt`. A companion dataset
(**15013203**) supplies line *information*, but whether it carries geometry or
only attributes is **unverified**. If it does not, Korea needs a line-shape
source before a build, most likely from 국가공간정보포털. That is the one
open question on this leg, and it is a build blocker rather than a screening
one.

**So both Korean legs are reachable and unrestricted**, and the only gate left
is a free API key for the business register. That moves Korea into Tier 1
contention: premises-level business data with coordinates and a 247-category
standard, national station points with coordinates and transfer information,
and **"제한 없음" on both** — a lighter licence position than any other
candidate in this screen.

> **SUPERSEDED 2026-09-22.** The conclusion held — Korea *is* Band A — but by a
> different route, and one city instead of six. The API key is unobtainable
> (residency-gated) and unnecessary: Seoul's `인허가 정보` SHEET export needs no
> account, and its licence is **KOGL Type 1** rather than 제한 없음, so
> attribution *is* required. Busan and Daegu fail on district-level coverage.

**Two corrections to the earlier Tier 2 entry.** Korea was recorded as having
"the ideal single-register shape"; at the scope this project actually works at,
it is multi-source. And its transit leg is reachable but key-gated rather than
absent.

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

#### ▲▲ 2026-09-23 — Brazil re-screened: CNPJ is geo-blocked, and IBGE's census address file replaces it

**Both findings above were superseded the same afternoon, by measurement.**

1. **CNPJ moved and is geo-blocked.** The `dados_abertos_cnpj/` directory
   returned **404 to the Internet Archive from 2026-01-30** (last capture
   2026-09-02); the host became a Nextcloud server and the files sit in the
   public share `index.php/s/YggdBLfdninEJX9` (its capture's `og:title` is
   "CNPJ"). From here every client — curl/schannel, Python/OpenSSL and the
   browser — is **reset during the TLS handshake**, while the Archive's crawler
   got through. `check-host.net` settled it: **16 nodes, `br1` 200, all 15
   others in 11 countries reset, including four in the US.** **A geo-block, and
   a publisher's choice** — this project does not route around it. The
   four-cause check (transient / wrong host / refusal / dead) was worked in
   order: the answer was *moved* AND *refused*, two causes at once.
2. **City registers: measured negative in both cities.** São Paulo's CKAN
   (**483 packages**, read by eye in full) and GeoSampa (**483 WFS layers**)
   carry building and industrial licences, markets, fairs and shopping centres,
   and no business register (`aprovacao-de-alvaras` is building permits,
   discontinued 2019). Rio's ArcGIS org (**9,879 public items**) led to
   `Fazenda/ISSQN` — whose four tables are **counts per street × activity
   group × year of concession**, the aggregate trap, and a FLOW not a stock.
3. **IBGE's CNEFE 2022 is a premises field survey with coordinates.**
   *"O CNEFE oriundo do Censo Demográfico 2022 foi a primeira oportunidade na
   qual o IBGE coletou a localização precisa para todos os endereços em campo,
   resultando em um cadastro 100% georreferenciado pela primeira vez."* Rows
   with `COD_ESPECIE = 6` carry `DSC_ESTABELECIMENTO`, *"identificação do
   estabelecimento"* — free text written by the enumerator. `NV_GEO_COORD = 1`
   is the census's own coordinate at the address. **One row per use-type per
   address**, with `COD_INDICADOR_ESTAB_ENDERECO` flagging multiples.
   Keyless, national, one schema — so **every Brazilian city with rail is
   screenable from the same file**, which is what reopened the five cities
   this file had collapsed on transit-catalogue grounds.

**Measured per city** with `scripts/screen_cnefe.py` — never inferred from one
city, which is the France lesson:

| City | Establishment rows | **Mapped** | Unclassifiable | Coord level 1 | Name at a dwelling |
|---|---|---|---|---|---|
| São Paulo | 570,229 | **216,037** | 19.7% | 98.5% | 1.1% |
| Rio de Janeiro | 264,714 | **105,350** | 20.0% | 95.1% | 2.1% |
| Fortaleza | 132,638 | **49,503** | 25.9% | 98.5% | 1.0% |
| Belo Horizonte | 125,268 | **44,923** | 22.8% | 98.8% | 1.4% |
| Salvador | 122,120 | **52,258** | 21.6% | 97.3% | 1.4% |
| Brasília | 100,889 | **35,824** | 26.7% | 99.9% | 2.3% |
| Recife | 72,760 | **25,212** | 29.2% | 99.0% | 1.2% |
| Porto Alegre | 61,068 | **18,798** | 27.9% | 98.1% | 0.9% |
| Santos | 18,641 | **6,021** | 25.0% | 98.1% | 0.8% |

**Rail, one Overpass query per city** (Curitiba as negative control — it
returned only a tourist train; Cuiabá, whose VLT was abandoned, returned 0):
Brasília, Recife, Porto Alegre, Fortaleza, Belo Horizonte, Salvador and Santos
carry metro or modern light rail. **Teresina, Maceió, João Pessoa and Natal**
carry single diesel lines or CBTU suburban trains tagged `light_rail` —
**ASSERTED commuter-shaped, not downloaded, not discarded.**

**Licence: free use by federal law**, credit required, LGPD applies; four
restrictive readings recorded in `docs/data_sources.md`. **Brazil moves from
"geocoding at national scale" to buildable: nine cities, one source.**

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
4. ~~**South Korea's transit data**, from the national source rather than the
   catalogue.~~ ~~**Find the OA ids for the six core business types.**~~
   ~~**Read `이용허락범위`.**~~ **All done, 2026-09-21/22. Seoul has no open
   screening question left** — transit measured, eight datasets downloaded and
   measured (197,276 active premises with coordinates), licence read as KOGL
   Type 1. It is a **build** candidate now, not a screening one: next step is
   `add-country` for Korea and a Seoul build brief, not more probing.

   Two things the build will have to handle, both known and neither a blocker:
   a **small geocoding fallback for 일반음식점 only** (90.7% coordinates against
   97–99.5% everywhere else), and a **Korean-aware pass in
   `check_personal_exposure.py`**, since salon trade names routinely contain a
   personal name.

   **Busan and Daegu are closed, not open** — see their section. Korea is a
   one-city country for this project.
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


---

## Tier 5 closed by browser navigation - 2026-09-22

Every probe below used the same two moves: **navigate the site in a real
browser before concluding anything about it**, then **enumerate providers
rather than search keywords**. Four countries had been recorded as *"needs the
browser"*; all four resolved, and the browser's answer differed from the
guessed one every time.

### 🇨🇴 Colombia - MEASURED NEGATIVE

| Probe | Result |
|---|---|
| `geomedellin-m-medellin.opendata.arcgis.com` in the browser | **"Please sign in. This site requires credentials to access."** The Hub is **private** - hence the earlier `data.json` 404 and `api/search/v1` 401. No account will be created |
| `www.datos.gov.co` (Socrata) control | `zzqqxx_nonsense_zzqq` -> **0 results**. The search filters; result lists are trustworthy |
| Cámara de Comercio de Medellín para Antioquia - the register-holder | **9 distinct datasets**, every commercial one an aggregate. `pb3w-3vmc` *Estructura empresarial Medellín según comunas y actividad económica*: **2,349 rows**, the 16 comunas as **columns**, CIIU as rows. CC BY-**SA** 4.0 |
| RUES `nb3d-v3n7`, *Establecimientos - Agencias - Sucursales* (Confecámaras) | **6,369,877 rows.** Right entity - `categoria_matricula = ESTABLECIMIENTO DE COMERCIO`. **25 columns, none of them an address, a municipality or a city.** Finest geography is `camara_comercio`, a multi-province chamber region. Also carries owner `CEDULA DE CIUDADANIA` numbers |
| Alcaldía de Medellín as a publisher | **No business-licence dataset** on the national portal, where Ley 1712 requires publication |

### 🇵🇪 Peru - MEASURED NEGATIVE on coverage

The browser identified the platform in one load: the site serves
`/profiles/dkan/*`, so it is **DKAN**, which speaks CKAN at `/api/3/action/*`.
Earlier passes had tried `/api/action/*` and concluded "Drupal, not CKAN".
`package_search` 404s but **`package_list` returns 4,687 dataset names** - the
enumeration primitive, and local filtering sidesteps the silent-ignore question
entirely.

- **203** commercial-looking names; **78** mention *licencia* or *funcionamiento*
- Licence: **ODC-BY** (`http://opendefinition.org/licenses/odc-by/`) - attribution only, no share-alike
- Resources are **direct CSVs** under `sites/default/files/`, no account

Coverage against Línea 1's nine districts:

| District | Rows | Address | Note |
|---|---|---|---|
| La Victoria | **135,982** | **100%** | Real register. `Giros` 54.3%, licence type, status. Gamarra's garment trade dominates the activity mix |
| Cercado (Mun. Metropolitana de Lima) | 5,613 | **none** | Administrative columns only - no address, no trade name. Found only by opening a dataset whose slug names no municipality |
| San Borja | 20 x 3 cols | - | A **metadata sheet**, not data |
| Surco, S.J. Miraflores, V.M. Triunfo, Villa El Salvador, El Agustino, S.J. Lurigancho | - | - | Nothing |

Off-line but published: **Chorrillos** 9,767 rows with `LOCAL_DIRECCION` 100%
populated; **Ate** 1,546 rows with no address column and a `NroDNI` field.

Two parsing notes for any future attempt: the CSVs are **wrapped per record in
quotes with `;;` terminators**, needing a two-stage parse (split on `;`, take
field 0, then parse as CSV); and `Nombre` carries **sole traders' personal
names**, making `check_personal_exposure.py` load-bearing rather than a
formality.

### 🇮🇩 Indonesia - MEASURED NEGATIVE

`satudata.jakarta.go.id` is a JS app whose API was read straight off its own
network panel: **`/backend/api/v2/satudata/*`** (`search-v2`,
`searchautocomplete`, `detail`, `get-komponen-dataset/<hash>`), plus a fully
parameterised search URL carrying `q`, `organisasi`, `status` and `page_no`.

| Probe | Result |
|---|---|
| Control | `q=zzqqxx` -> **0 datasets**. The search filters |
| Catalogue size | **5,267 datasets** |
| `q=izin usaha` | 5 hits, all **SIUP issuance logs from 2017-2018**, and **three of five marked `Terbatas`** (restricted) |
| `q=restoran` | 7 hits - *Jumlah Restoran per Kelurahan* (counts per sub-district), tax realisations, and a 2014 table. All aggregate |
| `q=izin` | 100 hits |
| **The live candidate** - *Daftar Perusahaan/Perizinan Usaha ... Online Single Submission (OSS)*, DPMPTSP, `Sifat Data: Terbuka`, metadata updated 25 May 2026 | **53,827 rows**, real street addresses |

The OSS register's schema, confirmed against the portal's own component list
(**9 of 9**) rather than the rendered table:

`periode_data` - `wilayah` - `kecamatan` - `kelurahan` - `nama_perusahaan` -
`alamat` - `nib` - `uraian_jenis_perusahaan` - `skala_perusahaan`

`uraian_jenis_perusahaan` is *"Kategori perusahaan"* - the **legal form**
(KOPERASI, PT) - and `skala_perusahaan` is *"Besaran usaha"* - the **size**
(USAHA MIKRO, USAHA KECIL). **Nothing records what the business sells**, so
`filter_to_storefront()` has nothing to act on. Scale is a second concern:
53,827 for a province of 10.6 million against Seoul's 197,276 for 9.4 million,
with `periode_data = 2025` and the visible rows dominated by cooperatives.

### 🇮🇱 Israel - unreachable, unchanged

HTTP 472 with our own IP echoed back is an IP-level refusal. The browser shares
the address, so it is not a route.

### What this closes

**Tier 5: eight countries, seven firm negatives, one unreachable, no
survivors.** Hong Kong's department (FEHD) remains the only open thread - the
register exists and is queryable, with no bulk route found.
