# Global city master list — CURRENT STATE

**This is the operative list: which cities this project could build next, and
what is stopping each one.** It is rewritten as things change, like
`docs/project_context.md` and unlike `DECISIONS.md`.

**The evidence lives in [`docs/global_country_shortlist.md`](global_country_shortlist.md)** —
87 countries screened, every probe logged, every negative with the measurement
behind it. That file is the trail; this file is the answer. When they disagree,
the trail wins and this file is stale.

Last reordered **2026-09-22**, after the browser sweep — Tier 5 closed
(7 negatives, no survivors), Tier 6 reached for the first time, and three
food-authority probes run. **Stockholm** and **Bucharest** were promoted out
of the band that used to read *"never actually reached"*; five cities moved to
discarded on measurement.

**The method that produced all of it:** open the portal in a real browser
*before* concluding anything about it, then enumerate providers rather than
search keywords. Both are written up in `.claude/skills/add-country/`
(§3 and §2) and `add-city` Step 0.

---

## Built — 16

| Country | Cities |
|---|---|
| **United States** (9) | San Diego · San Francisco · Los Angeles · Chicago · New York · Philadelphia · Miami · Boston · Washington D.C. |
| **Canada** (5, complete) | Vancouver *(with Surrey)* · Montréal · Calgary · Edmonton · Toronto |
| **Mexico** (2) ✅ | **Mexico City** · **Guadalajara (Regional)** — built 2026-09-22, live in the app |

✅ **Mexico is the first country built outside North America's anglophone
pair**, and the first where the rail leg came from **OpenStreetMap** rather
than an agency feed — the per-city exception approved for CDMX, which
validated at 195/195 stops exact.

## Candidates — 41

Re-tiered 2026-09-22 after the browser sweep closed Tier 5 and reached Tier 6.
**Five cities moved to discarded on measurement** and **one was upgraded**.

| Band | What is stopping it | Cities | Change |
|---|---|---|---|
| **A** | Nothing. Screening complete | **4** | ✅ −2 built, ▼ −1 Paris |
| **B** | One narrow question each | **4** | ▲ **+Stockholm** |
| **C** | A geocoding leg — build work, not screening | **18** | ▲ **+Bucharest** |
| **D** | Four sub-tiers, see below | **14** | ▼ −7 |
| *Discarded* | Measured negative, evidence named | *19* | ▼ **+5** |

✅ **Guadalajara and Mexico City left Band A by being built**, not by being
ruled out. Their rows are kept below, marked, because a built city's Band A
entry is the only place the screening promise and the delivered build sit
side by side.

**Net: the screen got smaller and more honest.** Nothing was lost that was
ever measured as viable — the five drops were all cities whose business leg
had never been tested, and testing it is what removed them.

**Two cities were promoted the same day**, both by the same method and both
out of the band that used to read "never actually reached": **Stockholm** to B
and **Bucharest** to C. The tier that looked deadest produced the two best new
results in the sweep.

---

## Band A — screening COMPLETE (4 remaining + 2 ✅ BUILT)

Ordered by how little stands in the way. **Built cities keep their row**,
struck through and marked ✅, so the band still shows what screening promised
and whether it held.

| # | City | Business leg | What remains |
|---|---|---|---|
| ✅ | ~~**Guadalajara**~~ 🇲🇽 | DENUE, SCIAN = NAICS, INEGI licence cleared | **BUILT 2026-09-22** — `pages/16_Guadalajara_Heatmap.py`, region *Mexico*. Screening said "nothing outstanding" and that held |
| 1 | **Madrid** 🇪🇸 | 148,814 open premises, 119,070 with valid coordinates, three-level classification, EPSG:25830. CC BY 4.0 + binding general conditions | **Nothing** |
| 2 | **Seoul** 🇰🇷 | 197,276 active premises over 8 datasets, EPSG:5174, status field, KOGL Type 1 | Build work — partial geocoding for 일반음식점 (90.7%), Korean-aware `check_personal_exposure.py` |
| 3 | **Milan** 🇮🇹 | 28,131 premises 99.1% coords, `insegna`, `codice_ateco`, CC-BY. All three buckets confirmed | Step 0 schemas for the two newly found layers |
| ✅ | ~~**Mexico City**~~ 🇲🇽 | Same DENUE. **Rail from OSM** — 195/195 stops exact, 6,468 geometry points | **BUILT 2026-09-22** — `pages/15_Mexico_City_Heatmap.py`. The ODbL share-alike decision was taken during the build; see `DECISIONS.md` |
| 4 | **Barcelona** 🇪🇸 | 68,024-premises ground-floor census, CC-BY-4.0 | One residual: the portal's general notice is CAPTCHA-walled and unread |

▼ **Paris left Band A on 2026-09-22**, measured rather than decided — see
Band D-a. The architecture question it was holding ("national register vs
per-city") turned out to be **closed already**: Mexico shipped two cities from
the national DENUE on the same day, so `pipeline/countries/` is the answer and
national registers are fine. What fails is **SIRENE's composition**, which is
a different objection and a measured one.

**Madrid now has nothing outstanding at all** — it is the only unbuilt city
in the screen with an empty "what remains" column, which makes it the next
city if nothing else is prioritised.

## Band B — one narrow question each (4 cities)

**Valencia** 🇪🇸 *(subway 84, tram 37 — the largest Spanish system measured)* ·
**Bilbao** 🇪🇸 · **Málaga** 🇪🇸

Spain is bespoke per city, so each needs its own register — but **two of the
three Spanish cities probed have had one**, which raises the prior sharply.

**▲ Stockholm** 🇸🇪 — **upgraded from D-c on 2026-09-22.** Screening is
DONE: a public ArcGIS FeatureServer carrying **8,146 distinct food premises**
with WGS84 points, 100% trade names and 96.9% addresses, updated daily. It
carries **two questions rather than one, and both are owner decisions, not
probes**:

1. **Scope.** It is **one bucket** — food. Stockholms stad has 291 datasets
   and exactly one commercial register; `restaurang` and `företag` both
   return **0** inside its own catalogue, and Sweden has no general business
   licence. A Stockholm page would be a food-density map.
2. **Licence.** `dataportal.se` says `Åtkomsträttigheter: Begränsad`
   (restricted); the ArcGIS item says `access: public` and serves without
   credentials; `licenseInfo` is empty. **Ambiguous in a way that matters** —
   `read-licence` step 8 — so it needs the publisher asked. That it fetches is
   not a finding that it is licensed.

## Band C — viable, each needs a GEOCODING LEG (18 cities)

Build work with a known cost. No further probing changes these.

| Cities | Country | Business leg | Geocoding |
|---|---|---|---|
| **Tokyo**, Osaka, Nagoya, Yokohama, Sapporo, Fukuoka, Kyoto, Kobe, Sendai, Hiroshima *(10)* | 🇯🇵 | Premises-level food permits, CC BY, one national schema. **Two buckets — no general retail** | **Hardest met** — chōme/ban/gō, full-width numerals, `町字ID` 0% populated |
| **Taipei**, Kaohsiung, Taoyuan, Taichung *(4)* | 🇹🇼 | 商業登記 — premises, active/closed status, per-category assembly | Moderate — **NLSC's geocoder is keyless** |
| **Oslo** *(1)* | 🇳🇴 | 152,060 sub-units, `beliggenhetsadresse` (physical, not registered), NACE, open API no key | Moderate |
| **Copenhagen** *(1)* | 🇩🇰 | CVR `productionunits` — P-enheder each with own `address`/`zipcode`/`city`, plus `industrycode` | Moderate — **plus a free account** (`distribution.virk.dk` 401) |
| **São Paulo** *(1)* | 🇧🇷 | CNPJ — trade name, address, CNAE | **Hard, past Toronto's scale** |
| **Bucharest** 🇷🇴 ▲ *(1)* | 🇷🇴 | **DSVSA's registered-premises lists — 31,299 premises across 14 of 34 categories**, name + `Adresa` + `Sector` + `Categorie unitate`, refreshed 25/08/2026. Food bucket, but a WIDE one: 13,279 catering, 10,488 food shops, 709 hyper/supermarkets | **Unmeasured** — no coordinates, Romanian addresses |

**▲ Bucharest was promoted out of Tier 6 on 2026-09-22** by the food-authority
probe. **Two cheap checks are still outstanding and are screening, not build
work:** its rail has never been counted in OSM (M1–M5, ~63 stations claimed,
unverified), and its licence is unread. A third item is operational rather than
legal: `ansvsa.ro` and `bucuresti.dsvsa.ro` sit behind a **"Verifying your
browser" JS challenge**, so the pipeline's fetch step needs a route through it
that is not a bot-detection bypass.

**Japan is ten cities from one schema** — the best marginal-city cost in the
screen — against the worst geocoding problem and a two-bucket ceiling.
**Still the biggest open decision in this list**, and a judgment call rather
than a probe.

## Band D — 14 cities, four sub-tiers

### D-a — one cheap question each (5)

| City | State |
|---|---|
| **Prague** 🇨🇿 | `rzp.cz`, the *živnostenský rejstřík* (**trade-licence** register), is live — the right shape, since Czech licences are issued per premises. Not ARES, the company register. **Best D lead after Copenhagen** |
| **Dublin** 🇮🇪 | `data.gov.ie` lists a **Valuation Office API**, but `api.valoff.ie` and `www.valoff.ie` both returned 000 twice — host down, so ASSERTED not measured. Does the Irish rateable register carry a **use category**, where the UK's NNDR did not? |
| **Zurich** 🇨🇭 | **Food confirmed** — `Gastwirtschaftsbetriebe`, premises-level, GeoJSON. No second bucket found; the national STATENT is aggregate |
| **Singapore** 🇸🇬 | API answers but its search is loose. One controlled query settles it. Suspected registered-office shaped |
| **Paris** 🇫🇷 ▼ | **Demoted from Band A, 2026-09-22.** SIRENE is legally clean and établissement-level, and **fails on composition**: of 148,633 active Paris rows in NAF 47/56/96, **128,655 (86.6%) are *sièges***, and a French sole trader's siège is typically the home address. **20,542** carry NAF **47.91B, online retail** — no storefront by definition. The open question is narrow: **can a NAF + siège + employee filter produce a defensible storefront layer without mapping homes?** See below |

### D-b — rail ANSWERED, business leg is the blocker (5)

**Five cities left this sub-tier on 2026-09-22** — Santiago, Kuala Lumpur,
Jakarta, Medellín and Lima — all to *discarded*, each with a measured reason.
What remains is the set whose business leg is genuinely still open.

Rail screened via OSM. **Relation counts are upper bounds** — see the caveat
below.

| City | Rail (OSM) | Business leg |
|---|---|---|
| **Hong Kong** 🇭🇰 | 126 rel, 125 named, 117 coloured | **BLOCKED, not negative.** The portal is a measured negative (statistics only), but **FEHD's register exists and is queryable** — no bulk export found. The single most valuable open thread in Band D |
| **Rio de Janeiro** 🇧🇷 | 20 rel, all named + coloured | CNPJ, no coordinates → geocoding at São Paulo's scale |
| **Tel Aviv** 🇮🇱 | 6 rel, **realistically 1** — Green and Purple are under construction and OSM does not mark them | **UNREACHABLE.** `data.gov.il/api` 14 bytes; city portal **HTTP 472** with our own IP echoed back — IP-level, so the browser shares the block. One operating line is thin regardless |
| **Hyderabad** 🇮🇳 | 6 rel, all named + coloured | Trade licences are municipal; `data.telangana.gov.in` dead |
| **Kochi** 🇮🇳 | 2 rel, named + coloured | Kerala LSG live |

#### Paris / SIRENE — the measurement, 2026-09-22

**The architecture question was answered by Mexico, not by argument.**
`pipeline/countries/mexico.py` holds the national facts and the two city
configs differ by one line (`DENUE_STATE_CODE`). Milan is already in Band A on
`codice_ateco`, the same NACE family as France's NAF. So "a national register
is not the shape this project is built around" is **no longer true**, and the
France entry had been carrying an objection the project had outgrown.

**What Mexico does NOT answer is the kind of source.** DENUE is a **field
survey** — INEGI enumerators visit, so a row is a place that exists. SIRENE is
an **administrative register** — a row is a declaration. Measured on Paris
(commune codes 751xx, `etatadministratifetablissement = Actif`), via the
uncapped SIRENE v3 établissement stock (43,896,818 rows):

| | |
|---|---|
| All active établissements | **1,335,566** — one per 1.6 residents. Not premises |
| ...of which **sièges** | **1,231,822 (92.2%)** |
| NAF 47+56+96 buckets | **148,633** |
| ...of which sièges | **128,655 (86.6%)** |
| ...non-siège secondary premises | **19,978** |
| NAF **47.91B**, online retail | **20,542** — 24% of the whole retail division |
| Masked (`statut P`) | **176,404 (13.2%)** |

**The 148,633 is a trap.** It sits almost exactly on Madrid's 148,814, which
makes it read as a pass — but that is a coincidence of magnitude, not of
shape. 86.6% of it is sièges, and this project's invariant is explicit that
*a registrant's own name at what looks like their home* is not publishable
**even from a public registry**. This is the registered-office trap that
disqualified Germany, Austria, Latvia and Slovakia, arriving through a source
that passes every legal and access test.

**Paris has no municipal premises survey to substitute.** `opendata.paris.fr`
enumerated in full — **490 datasets** — and the closest things to a commerce
layer are `terrasses-autorisations` (24,287 terrace and display permits),
`commerces-eau-de-paris` (1,500 shops stocking the water utility's product),
`commerces-semaest` (311 units owned by a city property company) and
`plub_protcom` (5,107 **zoning** protections on commercial frontages). None is
a register of businesses. Note `marchés` here is a false friend — it means
public procurement.

**UNRESOLVED, and recorded as such:** whether APUR's **BDCom** — the Paris
commercial-premises survey, the Montréal `locaux-commerciaux` shape — is
published anywhere. `apur.org`'s site search **silently ignores the query
term**: `BDCom` returns **131 pages** of unrelated studies. So this is "could
not confirm", not "absent", and it is the single check that would put Paris
back in Band A.

> **The relation counts are upper bounds.** The construction filter flagged
> unbuilt routes in Jakarta but returned **zero** for Tel Aviv, Bogotá and Rio —
> and Tel Aviv proves zero does not mean zero: its Green and Purple lines are
> under construction and OSM carries them as plain `light_rail` with no status
> marker. **A filter returning zero can mean "nothing to flag" or "this
> convention is not used here", and the result alone cannot tell you which.**

### D-c — REACHED; one promoted, two parked, two walls (4)

Retitled 2026-09-22: these were "genuinely unreached, no finding either way".
**All six have now been reached, and two of them paid off** — **Stockholm**
was promoted to Band B and **Bucharest** to Band C. Of the four left, one is a
firm negative and three are host or value decisions, not data negatives.

| City | What the host actually does |
|---|---|
| **Tallinn** 🇪🇪 ⏸ | **PARKED ON VALUE, not viability — 2026-09-22.** Trams only, ~450k; even a success is a thin map. API found (`andmed.eesti.ee/api/datasets/search`) but returns **400** to an empty `search` and to `limit=1000`, so the contract is unpinned; `toitlustus` gives 16 datasets, all school-catering statistics. **MTR** is the likely route, unprobed. Revisit only if a method makes it cheap |
| **Zagreb** 🇭🇷 ⏸ | **PARKED ON VALUE, not viability — 2026-09-22.** Trams only, ~770k. `data.gov.hr` answers 200 at **four** paths — including `data.json` — with the **identical 1,291-byte** body, an SPA shell. Still reachable by browser if it is ever worth the hour |
| **Budapest** 🇭🇺 ✗ | **FIRM NEGATIVE — the food-authority route is closed too.** Nébih's FELIR is **CAPTCHA-gated** (`service.mtcaptcha.com`) and is a one-customer-at-a-time lookup, not a register. Its *Approved Establishments* list is **two PDFs of processing plants** — the page names them: slaughterhouses, meat-cutting plants, dairies, egg packers, fish and game processors, cold stores. Retail and catering are only *registered*, by county offices, unpublished. Separately, `kozadat.hu` is a search tool over data inventories, not a portal |
| **Sofia** 🇧🇬 | **UNREACHABLE, still not a negative.** `data.egov.bg` returns **403 in the browser too**, correcting the earlier client-signature reading. The food authority (**BABH**) does not resolve at **any** domain tried — `babh.government.bg`, `www.babh.government.bg`, `babh.bg`, `bfsa.bg`, `babh.egov.bg` — and its parent ministry, which IS live, links no register. `www.sofia.bg` and `portal.registryagency.bg` remain live and unprobed |

### D-d — one cheap gate (1)

**Sevilla** 🇪🇸 — rail is **registration-gated, not absent**: Spain's National
Access Point answers 401. The WMATA shape, a free account. Its business leg
still needs its own Spanish source.

## DISCARDED — 19 cities, each naming its evidence

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
| **Santiago** 🇨🇱 ↓ | **Coverage.** Chile licenses per *comuna*; **5 of ~33** Metro comunas publish patentes and the **Santiago comuna is absent from the portal entirely**. The Daegu shape, 3rd occurrence |
| **Kuala Lumpur** 🇲🇾 ↓ | **Sample, not register.** `lookup_premise` passes every structural test — premises rows, 100% populated, keyless CSV — and holds **3,916 rows nationally, 372 in KL**. It is PriceCatcher's survey frame |
| **Medellín** 🇨🇴 ↓ | **Three closed doors.** The city's ArcGIS Hub is **credential-walled**; the chamber of commerce publishes comuna×CIIU **crosstabs**; RUES has **6,369,877** premises rows and **no address, municipality or city column at all** |
| **Lima** 🇵🇪 ↓ | **Coverage.** 78 licence datasets under ODC-BY, keyless CSV — but licensing is per *distrito* and **1 of Línea 1's 9** publishes usable data. La Victoria's 135,982 rows are excellent and alone |
| **Jakarta** 🇮🇩 ↓ | **No activity field.** The live OSS register has 53,827 rows and full street addresses across **exactly 9 columns**; the two that look like classification are legal form and business size |

Plus the no-urban-rail set (Winnipeg, Hamilton, Québec City, Halifax,
Mississauga, Ottawa, ~30 single-feed countries) and access-not-data
(Russia, Ukraine).

**Germany is a country-level negative**, on two cities measured independently
at two different portal hosts.

**The five added on 2026-09-22 each failed differently**, which is the useful
part: coverage (Santiago, Lima), sampling (Kuala Lumpur), no location column
(Medellín), no activity column (Jakarta). Four distinct ways for a
premises-shaped table to be unusable, and **not one of them is visible from a
dataset title**.

---

---

# BY COUNTRY — for country-by-country implementation

The same 48 candidates, cut the other way. **Ordered by cities gained per unit
of work**, because that is what country-by-country optimises for, and it
reorders things sharply: Japan is mid-table by city and near the top by
country.

"Missing link" = the single thing that would move the country up a tier.

## Tier 1 — build now, nothing to discover (3 countries, 4 cities ready; ✅ Mexico DONE)

| Country | Cities | Source shape | Missing link |
|---|---|---|---|
| 🇲🇽 **Mexico** ✅ **COMPLETE** | **2** — Mexico City, Guadalajara (Regional) | **DENUE**, national, coordinates, SCIAN **is** NAICS — and the taxonomy **did** transfer from the US builds | **Nothing. Both cities are built and live in the app** (`pages/15_`, `pages/16_`, region *Mexico*), 2026-09-22. The ODbL share-alike decision was taken during the build |
| 🇪🇸 **Spain** | **2 now, 6 total** — Madrid, Barcelona ready | Bespoke **per city**, but two of three probed had a premises census | Madrid and Barcelona are ready. Valencia, Bilbao and Málaga each need **their own register found**; Sevilla needs a **free NAP account** for rail |
| 🇰🇷 **South Korea** | **1** — Seoul | 8 datasets, EPSG:5174, KOGL Type 1, daily | **Two build items, not probes:** partial geocoding for 일반음식점 (90.7% coords) and a Korean-aware `check_personal_exposure.py` |
| 🇮🇹 **Italy** | **1** — Milan | Bespoke per city. Naples and Messina measured out | **Step 0 schemas** for the two newly found Milan layers. Nothing to discover |

## Tier 2 — ▼ DEMOTED 2026-09-22: the decision was made, and it went against (1 country)

| Country | Cities | Missing link |
|---|---|---|
| 🇫🇷 **France** ▼ | **0 built-ready, 6 rail-confirmed** — Paris, Lyon, Marseille, Lille, Toulouse, Rennes | **The decision was taken on measurement, not taste, and it went against.** The architecture half is fine — Mexico proved national registers work. **SIRENE fails on composition:** 86.6% of Paris NAF 47/56/96 are *sièges*, i.e. largely home addresses, and 20,542 are online-retail. France is still a six-city prize, but it is now a **storefront-filter and privacy problem at national scale**, not a single integration. The one check that would reopen it: whether APUR **BDCom** is published |

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

## Tier 5 — 🇸🇪 Sweden: screening done, two owner decisions (1 country, 1–2 cities)

**New tier, 2026-09-22.** Sweden was in the old Tier 6 ("never actually
reached"). It is the only country that came out of that sweep alive, and it
sits here rather than higher because what it yields is **one city with one
bucket** — not because anything remains to probe.

| Country | City | Rail | State |
|---|---|---|---|
| 🇸🇪 **Sweden** ▲ | **Stockholm** | T-bana, ~100 stations — the strongest rail in the unbuilt set after Hong Kong | **Screening COMPLETE.** Public ArcGIS FeatureServer, **8,146 distinct food premises**, WGS84 points, trade names 100%, addresses 96.9%, daily refresh |
| 🇸🇪 Sweden | *Göteborg* | Trams | **Unprobed candidate.** Publishes **two** registers to Stockholm's one — `Livsmedelsverksamheter` (businesses, not inspections, so no dedupe) and `Restauranger med serveringstillstånd`. Better data, weaker map |

**Neither remaining question is a probe.** (1) **Scope** — food only; Sweden
has no general business licence and Stockholms stad's own catalogue returns 0
for `restaurang` and `företag`. (2) **Licence** — `dataportal.se` says
`Begränsad`, ArcGIS says `access: public`, `licenseInfo` is empty; ambiguous
in a way that matters, so the publisher gets asked.

**Cost per marginal city is poor** — one city, maybe two, and the second needs
its own probe. Ranked below Tier 4 for that reason, despite being further
along than any of Tier 4's four.

## Tier 6 — reached; one promoted out, one closed, three left (4 countries, 4 cities)

**No data finding either way**, so none of these is a negative. Reached
2026-09-22; what each host actually does is recorded in Band D-c above.

| Country | City | Host state |
|---|---|---|
| 🇪🇪 **Estonia** | Tallinn | API found (`andmed.eesti.ee/api/datasets/search`), contract unpinned — **400** on empty `search` and on `limit=1000`. **MTR** is the likely real route, unprobed |
| 🇭🇷 **Croatia** | Zagreb | `data.gov.hr` — **identical 1,291-byte SPA shell** at four paths incl. `data.json` |
| 🇭🇺 **Hungary** ✗ **CLOSED** | Budapest | **Firm negative on both routes.** Portal: `kozadat.hu` is a search tool over data inventories. Food authority: FELIR is CAPTCHA-gated and lookup-only; approved-establishment lists are PDFs of processing plants |
| 🇧🇬 **Bulgaria** | Sofia | **403 in the browser too** — correcting the earlier client-signature reading. `www.sofia.bg` and `portal.registryagency.bg` live, unprobed |

## CLOSED — the former Tier 5 (8 countries, 9 cities)

**Kept in full below as evidence, not as candidates.** This was "rail is
answered, the business leg is the hunt". The hunt finished on 2026-09-22:
**seven firm negatives, one blocked, one unreachable, no survivors.**

| | Country | Outcome |
|---|---|---|
| ⏸ | 🇭🇰 **Hong Kong** | **BLOCKED, not negative** — FEHD's register exists and is queryable, no bulk export found. **The one worth returning to** |
| ✗ | 🇨🇱 **Chile** | Coverage — 5 of ~33 comunas, Santiago absent |
| ✗ | 🇮🇳 **India** | 288,011 resources searched; nothing premises-level. GHMC and Kochi Municipal Corporation unprobed |
| ✗ | 🇲🇾 **Malaysia** | Sample, not register — 372 rows in KL |
| ✗ | 🇨🇴 **Colombia** | Hub credential-walled; crosstabs; 6.4M rows with no address column |
| ✗ | 🇵🇪 **Peru** | Coverage — 1 of Línea 1's 9 districts |
| ✗ | 🇮🇩 **Indonesia** | No activity field in a 53,827-row addressed register |
| — | 🇮🇱 **Israel** | Unreachable — IP-level refusal, browser shares the block |

The full evidence for each is below and in
`docs/global_country_shortlist.md`.

### The evidence — retained

| Country | City | Rail | Missing link |
|---|---|---|---|
| 🇭🇰 **Hong Kong** | Hong Kong | **126 relations**, 125 named | **The register EXISTS and is queryable — but no bulk export found.** See below |
| 🇨🇱 **Chile** ↓ **FAILS** | Santiago | **30 relations**, all named + coloured | **Coverage failure, measured.** Chile licenses per *comuna*; only **5 of ~33** Metro comunas publish patentes, and **the Santiago comuna itself is not on the portal at all**. See below |
| 🇲🇾 **Malaysia** ↓ **FAILS** | Kuala Lumpur | 14 relations, all named + coloured | **Sample, not register.** `lookup_premise` is a genuine premises table with **372 rows in KL** — it serves a price survey. See below |
| 🇮🇩 **Indonesia** ↓ **FAILS** | Jakarta | 9 operating of 11 | **No activity field.** The live OSS register has 53,827 rows and full addresses across exactly 9 columns, none of which says what a business sells. See below |
| 🇨🇴 **Colombia** ↓ **FAILS** | Medellín | 6 relations, **only 2 coloured** | **Three closed doors:** the city's Hub requires credentials, the chamber publishes comuna×CIIU crosstabs, and the 6.4M-row national register has **no address column**. See below |
| 🇮🇳 **India** ↓ | Hyderabad, Kochi | 6 and 2 relations | **National portal measured negative** — 288,011 resources searched, nothing premises-level. Municipal corporations (GHMC, Kochi) unprobed. See below |
| 🇵🇪 **Peru** ↓ **FAILS** | Lima | 4 relations, all named + coloured | **Coverage, not existence.** 78 licence datasets under ODC-BY, but licensing is per *distrito* and **1 of Línea 1's 9** publishes usable data. See below |
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
| 🇨🇴 **Colombia** (Medellín) ↓ | Browser, then provider enumeration on `www.datos.gov.co` | **MEASURED NEGATIVE, and a new trap.** The Hub is **private** — it renders *"Please sign in. This site requires credentials to access."*, which is why `data.json` 404'd and `api/search/v1` 401'd. The register-holder publishes **crosstabs**; the national register has **no address column at all**. See below |
| 🇵🇪 **Peru** (Lima) ↓ | Browser identified **DKAN**; `package_list` enumerated 4,687 datasets | **MEASURED NEGATIVE on coverage — the Daegu shape, 4th occurrence.** 78 licence datasets exist, keyless CSV, **ODC-BY**. But licensing is per *distrito*, and of Línea 1's **nine** districts exactly **one** publishes usable data. See below |
| 🇮🇩 **Indonesia** (Jakarta) ↓ | Browser read its own API off the network panel | **MEASURED NEGATIVE, and the other half of the new trap.** The live OSS register has **53,827 rows and full street addresses** — and **no activity field**, so there is nothing to filter storefronts on. See below |
| 🇮🇱 **Israel** (Tel Aviv) | — | **Not reachable by either method.** HTTP 472 and the host printed our own IP back — an IP-level refusal, so the browser shares the blocked address |

**Tier 5 is now closed: seven firm negatives, one unreachable, zero survivors.**

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

> **NEW TRAP, second half — a located register with nothing to classify, and
> a classified register with nothing to locate.** A premises table needs *two*
> columns to be a map: **where** and **what**. Both halves failed on the same
> day, in different countries, and each looked like a pass right up to the
> column list:
>
> | | Rows | Location | Activity |
> |---|---|---|---|
> | Colombia, RUES `nb3d-v3n7` | **6,369,877** | **nothing** — not even a city | CIIU codes |
> | Jakarta, OSS register | 53,827 | full street `ALAMAT` | **nothing** usable |
>
> Colombia's is the harder one to catch, because *6.4 million premises* reads
> as a decisive pass. The rows are the right entity — `ESTABLECIMIENTO DE
> COMERCIO`, the shop, expressly distinct from the company that owns it — and
> there is no address, no municipality, no city name. The finest unit in the
> file is `camara_comercio`, a chamber-of-commerce region spanning provinces.
> (It also carries owner `CEDULA DE CIUDADANIA` numbers, which this project
> would not publish in any case.)
>
> Jakarta's has exactly **9 columns**, checked against the portal's own
> component list rather than the rendered table: `periode_data`, `wilayah`,
> `kecamatan`, `kelurahan`, `nama_perusahaan`, `alamat`, `nib`,
> `uraian_jenis_perusahaan`, `skala_perusahaan`. The last two are **legal
> form** (KOPERASI, PT) and **size** (USAHA MIKRO) — neither says what the
> business sells, so `filter_to_storefront()` has nothing to act on.
>
> **Ask the two questions separately.** "Is it premises-level?" does not imply
> either one.

#### Colombia — three doors, all closed

1. **GeoMedellín's ArcGIS Hub is private.** The browser settled in one load
   what two HTTP codes had left ambiguous. No path exists to find, and this
   project does not create accounts.
2. **The register-holder publishes crosstabs.** The *Cámara de Comercio de
   Medellín para Antioquia* has nine distinct datasets on `datos.gov.co` and
   every commercial one is an *Estructura empresarial* table with the **16
   comunas as columns** and CIIU as rows — 2,349 rows of counts. Textbook
   aggregate, and CC BY-**SA** into the bargain.
3. **The national register has no location.** RUES, above.

No *Alcaldía de Medellín* business-licence dataset exists on the national
portal, which is where Ley 1712 requires publication.

#### Peru — excellent data, in one district out of nine

Peru's portal is the best-run of the group: **4,687 datasets**, keyless CSVs,
**ODC-BY** (attribution only, no share-alike). **78** carry *licencia* or
*funcionamiento*. It fails on coverage alone.

| Línea 1 district | State |
|---|---|
| **La Victoria** | **135,982 rows**, `Direccion` **100%** populated, `Giros` 54.3%, licence type and status. A genuine register — and the Gamarra garment district shows plainly in its composition |
| Cercado de Lima (Mun. Metropolitana) | 5,613 rows — **no address column, no trade name**. Administrative fields only |
| San Borja | Publishes a **metadata sheet**, not data: 20 rows × 3 columns |
| Surco · S.J. de Miraflores · V.M. del Triunfo · Villa El Salvador · El Agustino · San Juan de Lurigancho | **Nothing** |

**One of nine.** The southern four districts and the northern two — more than
half the line's stations — would be blank. Chorrillos does publish a good file
(9,767 rows, addresses) and Ate publishes a poor one (1,546 rows, no address),
but neither is on Línea 1.

Two notes for any future attempt: the CSVs are **double-quoted with `;;`
record terminators**, needing a two-stage parse; and `Nombre` carries
**sole traders' personal names**, so the project's personal-exposure check
would be load-bearing here rather than a formality.

**The method is doing its job, and the honest summary is that it mostly
closes things.** All eight Tier 5 countries are now settled: **seven firm
negatives** — Hong Kong's portal, Chile, India, Malaysia, Colombia, Peru,
Indonesia — **one upgrade** (Hong Kong's department, which turned out to have
*two* buckets but no bulk route), and **one unreachable** (Tel Aviv).
**No survivors.**

**A parameter-encoding note that cost a pass:** India's API ignores
`filters[title]=x` with literal brackets and honours `filters%5Btitle%5D=x`.
The unencoded form returns **HTTP 200 with the full unfiltered 288,011** and no
error — the same silent-ignore failure as `data.seoul.go.kr`, and the reason a
control term is not optional. The first search read as "no results" when it was
actually "no filter".

### The old Tier 6, reached — the evidence, 2026-09-22

**This is the evidence behind the new Tier 5 (Sweden) and Tier 6 (host
failures) above**, retained in full. It was "never actually reached"; the
browser sweep reached all six. One is a **partial pass** and was promoted; the
rest are host failures of varying finality.

| Country | City | State after the browser |
|---|---|---|
| 🇸🇪 **Sweden** ▲ | **Stockholm** | **PARTIAL PASS — best unbuilt result outside Band A.** A public ArcGIS FeatureServer with **8,146 distinct food premises**, real WGS84 coordinates, trade names, addresses and a usable activity field. **One bucket only** (food), and one licence conflict to resolve. See below |
| 🇪🇪 **Estonia** | Tallinn | API **found** — `andmed.eesti.ee/api/datasets/search?page&limit&search&type&sortBy&sortOrder&lang` — but it rejects an empty `search` and a large `limit` with **HTTP 400**, so the parameter contract is not pinned. `toitlustus` returns 16 datasets, all school-catering statistics. The real route is almost certainly **MTR** (Majandustegevuse register), which is unprobed. Lowest-value city in the tier: trams only, ~450k |
| 🇭🇷 **Croatia** | Zagreb | `data.gov.hr` answers 200 at **every** path with the **identical 1,291-byte** body — an SPA shell. Confirmed by four paths including `data.json`. **Still needs the browser** |
| 🇭🇺 **Hungary** | Budapest | **Misidentified until now.** `kozadat.hu` is not a data portal — it is a *search tool over public bodies' data inventories*. `budapest.hu` loads 425 KB with **two** data-ish links, one of them a privacy PDF. No catalogue found |
| 🇷🇴 **Romania** | Bucharest | `data.gov.ro` **times out** at the connection (21 s, both root and API); `portal.onrc.ro` does not resolve; `www.pmb.ro` is a 2,483-byte shell |
| 🇧🇬 **Bulgaria** | Sofia | **CORRECTION: the browser fails too.** `data.egov.bg` returns the same **403** in a real browser as to curl, so the earlier reading — that a stock Apache page implied a *client-signature* refusal worth retrying — was wrong. `data.sofia.bg` and `opendata.sofia.bg` **do not resolve**. `www.sofia.bg` and `portal.registryagency.bg` are live and unprobed |

### 🇸🇪 Stockholm — a real register, found four hops deep

The route is the argument for navigating rather than guessing; no step of it
was predictable from the outside:

`dataportal.se` → organisation **Stockholms stad** (291 datasets, 101 open,
190 *skyddade*) → the **one** commercial hit, *Tillsynsverksamheter -
Livsmedel* → its page links the miljöförvaltning's ArcGIS Hub → the Hub item
id resolves through `arcgis.com/sharing/rest` to a **public** FeatureServer.

| Measured | |
|---|---|
| Rows | **289,742** — but a row is an **inspection**, carrying `TillsynsDatum` and `Anmarkning`. "Nyko Kitchen, Nybrogatan 61" repeats across dozens |
| **Distinct premises** (`ObjektId`) | **8,146** |
| Geometry | `esriGeometryPoint`, real WGS84 — `(18.0804, 59.3388)` — plus SWEREF99 northings/eastings |
| `Adress` | 280,760 of 289,742 rows non-empty (**96.9%**) |
| `AnlaggningsNamn` | **100%** — trade names |
| `VerksamhetsTyp` | 22 values, **29.5%** of rows non-null: *Restaurang-, catering- och barverksamhet* 65,858 · *Detaljhandel* 11,103 · *Partihandel* 2,810 |
| `AnlaggningsTyp` | **0% — entirely `'None'`.** The field exists and is empty |
| Update | daily/weekly, from Ecos 2 |

**The row-count discipline cuts both ways.** Malaysia's count was too *small*
to be a register; Stockholm's is too *large*. Both are answered by asking what
a row **is** before trusting the number — and here the answer is good news,
because 8,146 premises with coordinates is a real city leg.

**The activity field is recoverable but not free.** `VerksamhetsTyp` is null on
70.5% of rows because it describes the *inspection*, not the premises — so it
has to be lifted to premises level by taking any non-null value per `ObjektId`
during dedupe. That is ordinary work, not a blocker, but it is work, and it is
the difference between this and Jakarta, where no activity field existed at all.

**Two open questions before Stockholm could be built:**

1. **One bucket.** This is food only. Stockholms stad has **291 datasets and
   exactly one** commercial register — `restaurang` and `företag` both return
   **0** within its catalogue. Sweden has no general business licence, so
   retail and personal services have no municipal source to find. This is the
   Hong Kong shape, improved: a real bulk route exists, but a Stockholm page
   would be a **food-density map**, not the three-bucket map the built cities
   carry. That is a scope call, not a data problem, and it belongs to the
   owner. `multi-source-city` is the relevant process if a second source is
   ever found.
2. **A licence conflict that must not be resolved in this project's favour.**
   The `dataportal.se` metadata record says `Åtkomsträttigheter: **Begränsad**`
   (restricted); the ArcGIS item says `access: **public**` and serves the data
   without credentials. `licenseInfo` is **empty**; `accessInformation` reads
   only *"Stockholms stad, miljöförvaltningen"*. Per `read-licence` step 8 this
   is **ambiguous in a way that matters** and needs the publisher asked — the
   fact that it fetches is not a finding that it is licensed.

**A second Swedish city worth noting:** `dataportal.se` shows **Göteborgs
stad** publishing *both* `Livsmedelsverksamheter` ("alla aktiva
livsmedelsverksamheter", JSON + CSV) and `Restauranger med serveringstillstånd`
(CSV) — i.e. **two** food-adjacent registers where Stockholm has one, and
`Livsmedelsverksamheter` is a register of *businesses* rather than of
inspections, so it needs no dedupe. Gothenburg's rail is trams rather than a
metro, so it is a weaker map for a stronger dataset. Unprobed.

## Countries ruled out

🇩🇪 **Germany** *(two cities measured at two hosts — the Gewerberegister is not open data)* ·
🇦🇹 **Austria** *(GISA strips the street address)* · 🇳🇱 **Netherlands** *(aggregate)* ·
🇬🇷 **Greece** *(sector-only)* · 🇵🇹 **Portugal** · 🇵🇱 **Poland** ·
🇱🇻 **Latvia** *(unclassified)* · 🇸🇰 **Slovakia** *(no classification)* ·
🇪🇬 **Egypt** · 🇬🇧 **UK** *(NNDR is a tax register with no category)* ·
🇦🇺 **Australia**, 🇳🇿 **New Zealand** *(licensing is not municipal)* ·
🇧🇪 **Belgium** *(bulk access paid)* · 🇦🇪 **Dubai** *(no agency feed)*

## The order, as decided

1. ✅ **Mexico** — **DONE, 2026-09-22.** Two cities from one source, as
   predicted. It was also the project's first country outside anglophone North
   America and its first OSM-sourced rail leg, so it proved two things the
   screen had only asserted.
2. ▶ **Spain — NEXT.** Madrid and Barcelona ready *now*; the other three
   likely rather than speculative. Madrid is the only unbuilt city in the whole
   screen whose "what remains" column is empty — and since Paris left Band A on
   2026-09-22, it is also the clearest next build by some distance.
3. **Korea** and **Italy** — one city each, nothing to discover, both with
   named build work rather than open questions.
4. **Taiwan** — the first geocoding build, chosen because it is the cheapest:
   keyless geocoder, systematic addresses, four cities. **Lift the shared parts
   into `pipeline/` here**, not later.
5. **Norway**, **Denmark**, **Brazil** — the rest of Tier 3, in rising
   difficulty.
6. ⏸ **Japan** — **last, by decision.** Ten cities, and by then the geocoding
   machinery is built.

**France no longer sits outside this order awaiting a decision** — the
decision was made on 2026-09-22 and it went against SIRENE as a primary
source. France re-enters only if APUR BDCom turns out to be published, or if a
NAF + siège + employee filter is shown to yield a defensible storefront layer.
Recorded in Band D-a with the measurement.

Tier 4's four probes (**Czechia** strongest) are cheap enough to run alongside
any of the above rather than competing with them.

**Sweden sits outside the numbered order too**, for the opposite reason to
France: its work is not architecture but a **scope call** — whether a
one-bucket, food-only city page belongs in this project at all. Settle that and
Stockholm is close to ready; leave it unsettled and there is nothing to build.
**Hong Kong is the one closed country worth reopening**, since its register is
known to exist and only the bulk route is missing.

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
