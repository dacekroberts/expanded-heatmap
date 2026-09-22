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
| **Bulgaria** | **403**, and the registry agency refuses connections | **BLOCKED** |
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

## MASTER CITY LIST — refreshed 2026-09-22

**14 built:** San Diego, San Francisco, Los Angeles, Chicago, New York,
Philadelphia, Miami, Boston, Washington D.C., Vancouver (with Surrey),
Montréal, Calgary, Edmonton, Toronto. Canada is finished.

Candidates are banded by **what is actually stopping each one**, because that
is the only thing that decides what to do next. Three of the four bands are not
waiting on research at all.

### Band A — screening COMPLETE, no evidential gap (4 cities)

| City | Rail | Business | What remains |
|---|---|---|---|
| **Seoul** 🇰🇷 | 407 stations (1,099 national), WGS84, English, line geometry | **197,276 active premises**, 8 datasets, EPSG:5174 coords, status field, **KOGL Type 1** | Build work only: partial geocoding for 일반음식점 (90.7%) and a Korean-aware `check_personal_exposure.py` |
| **Paris** 🇫🇷 | subway 16, tram 17, funicular 1 | SIRENE, établissement-level, geolocated, Licence Ouverte 2.0, non-diffusible masked at source | **An owner decision, not a probe:** a national register is not the per-city municipal shape this project is built around |
| **Mexico City** 🇲🇽 | subway 12, via `mdb-latest` | DENUE, 6M+ establishments, coordinates, **SCIAN = NAICS**, INEGI licence cleared | Nothing |
| **Guadalajara** 🇲🇽 | LRT 3, current feed | Same DENUE source | Nothing |

**Mexico is the cheapest unbuilt country in the screen**: two cities, one
national source, a cleared licence, coordinates included, and a taxonomy that
may transfer from the US builds because SCIAN *is* NAICS.

### Band B — one narrow question each

| City | What is measured | The one question |
|---|---|---|
| **Barcelona** 🇪🇸 | 68,024-premises ground-floor census; FGC subway 4 + funicular 3 | **The licence.** One document, unread |
| **Milan** 🇮🇹 | 28,131 premises, **99.1% with coordinates**, `insegna`, `codice_ateco`, floor area, **CC-BY**; subway 5, tram 17 | **Is Personal services reachable?** Two buckets confirmed, the third not |
| **Madrid** 🇪🇸 | subway 13 | **Its own business source.** Barcelona's census is Barcelona's — Spain is bespoke per city, so Madrid's register is unprobed |
| **Valencia** 🇪🇸 | subway 84, tram 37 — the largest Spanish system measured | Same: its own source, unprobed |
| **Bilbao / Málaga** 🇪🇸 | rail confirmed | Same |
| **Sevilla** 🇪🇸 | Metro de Sevilla exists at mdb 2781 | **Its mirror 404s.** One retry from the agency host |

### Band C — viable, but each needs a GEOCODING LEG (build work, not screening)

No further probing will change these. They are real candidates whose cost is
known and front-loaded.

| City / group | Business leg | Geocoding difficulty |
|---|---|---|
| **Taipei, Kaohsiung, Taoyuan, Taichung** 🇹🇼 | 商業登記: premises addresses, active/closed status, per-category assembly | Moderate — Taiwanese addresses are systematic; **NLSC's geocoder is keyless** |
| **Oslo** 🇳🇴 | **152,060 Oslo sub-units**, `beliggenhetsadresse` (physical, not registered), NACE, open API no key | Moderate — Norwegian street addresses |
| **São Paulo** 🇧🇷 | CNPJ, ~72M, trade name + address + CNAE | **Hard — at a scale past Toronto's** |
| **Tokyo** + Osaka, Nagoya, Yokohama, Sapporo, Fukuoka, Kyoto, Kobe, Sendai, Hiroshima 🇯🇵 | Premises-level food permits, CC BY, national standard schema. **Two buckets — no general retail** | **Hardest met so far** — chōme/ban/gō block addressing, full-width numerals, and the `町字ID` join key is 0% populated |

Japan is ten cities from one schema, which is the best marginal-city cost in
the screen — against the worst geocoding problem and a two-bucket ceiling.
**That trade is the single biggest open decision in this list**, and it is a
judgment call rather than a probe.

### Band D — genuinely unprobed, and cheap to settle

This is the only band where more screening changes anything. See the corrected
discard list below: **several of these were written off on a reason this
document itself contradicts.**

| City | Country status |
|---|---|
| **Dublin** 🇮🇪, **Zurich** 🇨🇭 | **Neither leg ever probed.** The two remaining blanks in Western Europe |
| **Berlin**, **Hamburg** 🇩🇪 | Germany: "working route, **unprobed** register" — *not* a failure |
| **Prague** 🇨🇿 | Czechia: working route, unprobed register |
| **Singapore** 🇸🇬 | Working route, unprobed; suspected registered-office shaped, which would be fatal — one probe settles it |
| **Naples**, **Messina** 🇮🇹 | **Italy PASSES.** Their own comune sources are simply unprobed |
| **Stockholm** 🇸🇪, **Copenhagen** 🇩🇰, **Budapest** 🇭🇺, **Tallinn** 🇪🇪, **Zagreb** 🇭🇷, **Bucharest** 🇷🇴, **Sofia** 🇧🇬 | **Never reached.** Blocked, behind SPA front ends, or not attempted |
| **Helsinki** 🇫🇮 | Measured: 89.8% carry street addresses, but composition is **53% real estate and 4.8% retail**. A real objection, unlike the n=1 one it replaced |
| **Santiago** 🇨🇱 | National portal's copy is a decade stale; **municipal portals unprobed** |
| **Hong Kong**, **Jakarta**, **Kuala Lumpur**, **Rio**, **Tel Aviv**, **Lima**, **Bogotá / Medellín** | Ruled out against a *transit catalogue*, which is the wrong source. **National mapping agency unprobed for all seven** |

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
| **Copenhagen** | DK | subway 4, tram 4 |
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
| **Copenhagen** | DK | subway 4, tram 4 | current |
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
