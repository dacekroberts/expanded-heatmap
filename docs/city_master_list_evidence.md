# Global city master list — evidence trail

**This is the evidence trail behind [`city_master_list.md`](city_master_list.md), moved out of it on 2026-09-27.** It holds the closed bands, the emptied open screening gap, the 2026-09-22 by-country tier view with the former Tier 5, and the screening write-ups of Band A cities that have since been built.

**It is append-mostly and it is NOT current state.** Each section was moved word for word under its original heading, so a count, a band letter or a "now" in it is true of the date it was written. For which cities are candidates, what stops each one, and every count, read `city_master_list.md`, whose counts `scripts/check_master_list_counts.py` enforces. When a band closes or a write-up stops describing the present, move it here and leave a one-line pointer in its place.

---

## 🟢 Band A — screening write-ups moved from beside the band's rows

<a id="band-a-taiwan"></a>

### ▲▲ Taiwan — three cities, one tax register, a door-plate JOIN (2026-09-23)

**Taiwan left the geocoding band the same way Brazil did: the address file
already carries the coordinate.** Each city publishes a keyless monthly
**door-plate coordinate file** (`門牌位置數值資料`), and the national **business
tax register** (Fiscal Information Agency, daily, one row per trading
location, branches as their own rows) joins to it by parsed street / lane /
alley / number. Full evidence: `global_country_shortlist.md`, "Taiwan
finished".

*[The band's table stood here; it stays in city_master_list.md.]*

**Taipei is REGIONAL, like Dublin and Lille:** New Taipei completely surrounds
it and the metro crosses the boundary on several lines, so a Taipei-only page
would cut the network where no rider notices.

**Decided by the owner, 2026-09-23:**
- **OGDL v1's fault-based liability clause — ACCEPTED for all of Taiwan** (one
  decision covers the door plates, the tax register and the agency rail).
- **Names: shown only when they are a TRADE name** — for companies and
  branches, and for sole proprietors only when the name carries a business
  marker (行/店/社/館/坊…); otherwise the category. The FIA itself refuses to
  publish owners' names, and for 4.9% of Taipei's storefronts the business
  name reads as the owner's.
- **The attribution statement is load-bearing**: OGDL v1 §三(二) voids the
  grant retroactively without it.

**For the build, measured, not decided:** company head-office rows — **38.7%
of Taipei's company rows sit on a 3rd floor or higher or carry a room
number**, against 7.1% of sole proprietors; market stalls — genuine premises
with no door plate, most of Taipei's retail misses; and **TDX is not used**
(key-gated since at least 2026-09-23; registration wants a Taiwanese mobile
number).

<a id="band-a-brazil"></a>

### ▲▲ Brazil — nine cities, one census file, no geocoder (2026-09-23)

**Brazil left the geocoding band by not needing a geocoder.** It was carried as
*"CNPJ plus geocoding past Toronto's scale"*. Two measurements replaced that:

- **CNPJ is unreachable from outside Brazil.** Receita moved it to a Nextcloud
  share in early 2026 and the host resets every non-Brazilian connection —
  **16 check nodes, the Brazilian one 200, the other 15 in 11 countries
  reset.** A publisher's access control, so this project does not route
  around it.
- **IBGE's CNEFE 2022 is a premises field survey.** The census address file
  records, for every non-residential address, `DSC_ESTABELECIMENTO` — the
  enumerator's identification of the establishment — with a **coordinate
  taken at the address**. National, keyless, one schema. Licence: **free use
  by federal law** (Decree 8.777 art. 4, Lei 14.129 art. 29), credit required,
  LGPD applies — see `docs/data_sources.md`.

Both cities' own portals were enumerated first and are **measured negative**:
São Paulo's 483 CKAN packages and 483 GeoSampa layers hold no business
register; Rio's `Estabelecimentos Abertos` is the **aggregate trap** — counts
per street × activity group × year of concession.

**Screened with `scripts/screen_cnefe.py`**, which classifies the free text
into the NAICS-bounded buckets (head-noun rules plus an edit-distance pass for
enumerator misspellings). Every figure is from the city's own file:

*[The band's table stood here; it stays in city_master_list.md.]*

**Four decisions taken by the owner the same day**, recorded in `DECISIONS.md`:
proceed on the federal-law grant with four restrictive readings recorded; at
any address that also holds a **dwelling, show the category, never the
description text**; accept the **2022 vintage** and disclose it (Barcelona's
precedent); and disclose that a **shopping centre collapses to one to a few
rows** (0.1–0.2% of mapped rows stand for more than 10 establishments).

⚠️ **The dropped share is not uniform, and every page must say so.** Bare
trade names with no category word (`MUNDO VERDE`, `RED CELL`) cannot be
bucketed honestly and are dropped — and **affluent commercial districts use
them far more**. The map therefore **under-draws its richest districts**, worst
in **Brasília's Asa Sul (48%)** and **Fortaleza's Meireles (43%)**. That is a
bias to state on the page, or to reduce with a better classifier; it is not a
reason to key everything to Retail, which is the guess `premises-taxonomy`
forbids.

⚠️ **Brasília's addresses name a block, not a door — MEASURED 2026-09-23.**
The 89.7% of its storefronts that "share an address with a dwelling" is the
key's artefact: 98.5% of those rows have no door number, and the unit is the
`LOTE` complement. **Keyed on the lot: 58.0%. On the identical coordinate:
18.8%** (Recife 20.3%);
**decided by the owner 2026-09-23: key on the lot where the number is blank** —
now in `screen_cnefe.py`, **68.9%**. **9%** of rows still stand for more than
one establishment.

*[The "Not carried forward" paragraph stood here; it stays in city_master_list.md as current state.]*

**Every question these cities carry is answerable inside the build**, not
before it. Nothing here needs a probe, a document or a decision first.

**▲ France's other five cities were added on 2026-09-22.** The Tier view had
said *"France — 6 cities"* since the country was resolved, while the band
view showed only Paris — **so this list understated France by five cities for
as long as both views existed.** They share one national register, one
licence and one filter with Paris, and their geolocation was measured per
commune rather than inherited.

> ⚠️ **Dublin's row was wrong in four places until 2026-09-22**, corrected
> from `docs/build_briefs/dublin.md` after Step 0 measured it live. All four
> errors share one root: **the screening probe reported the slice it happened
> to query as if it were the whole.** It queried **one** authority and **six**
> categories, then quoted the total as Dublin's; it quoted the length of the
> *national* category list as the number present in Dublin; it computed 100%
> coordinates over only the rows it had pulled; and it counted colours across
> all 42 OSM relations including the Commuter and InterCity services a build
> would drop. **Every number was true of the query and false of the city.**

*[The band's table stood here; it stays in city_master_list.md.]*

⇄ **Paris left Band A and came back the same day, measured both times.**
The demotion was right on the evidence then available (86.6% of the bucket are
sièges, i.e. largely home addresses); the return is right on evidence that did
not exist yet — an **OSM composition comparison**. ⚠️ **That comparison was later re-established and its headline figure withdrawn** (see Paris's row): the reversal was right, the number supporting it was not. The
reversal is recorded rather than tidied away, because the thing that changed
was the measurement, not the opinion. See "Paris / SIRENE" below. The architecture question it was holding ("national register vs
per-city") turned out to be **closed already**: Mexico shipped two cities from
the national DENUE on the same day, so `pipeline/countries/` is the answer and
national registers are fine. What fails is **SIRENE's composition**, which is
a different objection and a measured one.

▶ **Madrid's pipeline is DONE and on master; only its app wiring is held.**
As of 2026-09-22 `pipeline/madrid/`, `outputs/madrid/`, its taxonomy module and
its provenance rows are all merged, and `scripts/check_provenance.py` reports
it ready. What is not merged is `app/cities.py` and its page, deliberately:
they sit on `spain-app-wiring`, because Streamlit Cloud pulls master
automatically and landing an imported module there would publish the city and
serve it broken until a reboot. **It waits for Barcelona so the two ship
together** — see that branch's own commit message, which is the authority on
the hold.

So the next *unstarted* city is the question.
**Barcelona** is the obvious answer — same country, brief done, licence read,
and only owner decisions left. After that the screen has no city whose
"what remains" column is empty.

<a id="band-a-rome"></a>

### ▲ 🇮🇹 Rome — a premises register joined to Italy's house-number archive (2026-09-24)

**The open screening gap's last row, screened in one evening.** Roma Capitale's
SUAP register records **premises** — 155,448 establishments keyed on (office,
number), with the city's street code, civic number and an activity class — and
**ANNCSU**, the national house-number archive, carries the same street code
with WGS84 coordinates for all 516,337 of Roma's civic numbers. **No geocoder:
a join, 95.7% at civic level.** Brief: `docs/build_briefs/rome.md` (6/6).

*[The band's table stood here; it stays in city_master_list.md.]*

🚩 **Owner's call, 2026-09-24: Band A WITH A BUILD CHECK.** The food-and-drink
control reads **2.60×** OSM (19,223 vs 7,405), above France's 1.26–1.80× and
Prague's 1.63×, and cannot be sharpened (restaurants and bars are not
separated). The register has **no closure date**. The build compares SUAP with
OSM street by street, splits the excess by start year, and either sets an age
cut-off or states the over-count on the page.

<a id="band-a-amsterdam"></a>

### ▲ 🇳🇱 Amsterdam — two layers from the city's own API (2026-09-24)

**Moved here from Band C on 2026-09-24 (owner's call)**, the night it left the
discards. The BAG's **10,898 shop-class units in use** became a second layer
beside the **4,092 hospitality permits**, with the **4.6%** vacancy rate
disclosed on the page and retail and personal services in one category. Both
licences read: **BAG PERMITTED** (Kadaster, Public Domain Mark); **the permits
SILENT**, credited as **CC BY 4.0** on the owner's choice because that
satisfies both readings. Brief: `docs/build_briefs/amsterdam.md`, **8/8
checks**. Build-time calls: trams in or out, four permit categories, 1,061
mixed-use units, de-duplication by address.

#### From the discards to Band C, 2026-09-24 — the screening, as written

**Its discard rested on the top hits of one national search** (*"Aantal
vestigingen per buurt"* — neighbourhood counts). **The city's own API was
never asked**, and it answers: `api.data.amsterdam.nl/v1/` lists **100 datasets**
*(recorded as 383 at first — that was dataset and table paths, not datasets)*.

| | |
|---|---|
| **The full register** | 🚧 `hr_kvk` (the KvK Handelsregister, incl. `vestigingen`) and `standbedrijven` answer **HTTP 403** — authorised users only, not worked around. The published schema names the scopes: `hr_kvk` **`FP/MDW`** and **`HR/R`**, `standbedrijven` **`BSK/BEDRIJVEN`** — city-staff scopes, so asking for access is unlikely to land. KvK's own HVD open dataset (CC BY 4.0) **cuts every address to the first two postcode digits** and drops names and numbers — activities without a location, Colombia's shape |
| **The one bucket** | ✅ `horeca/exploitatievergunning` — **4,094 hospitality operating permits**, all granted, **every end date in 2026–2031 (a live register: expired permits leave it)**, 96.7% with a point (RD New). Restaurant 1,702 · café 870 · alcohol-free 327 · fast food 231 · coffeeshop 126 · eethuis 93 · hotels 72 (out) |
| **Control** | **0.89×** OSM restaurants (1,806 vs 2,040) and **0.95×** all food and drink — close to complete; **fast food is thin** (231 vs 712), probably exempt |
| **Licence** | **SILENT — read 2026-09-24.** The live API declares none (`license: null`, *"Licentie: -"*); a 2022 harvest of the city's retired catalogue on `data.overheid.nl` said CC BY 4.0 — **a conflict flagged, not resolved in the project's favour** |
| **Names** | trade names (*"Taco Lindo Albert Cuyp B.V."*) |
| **Rail** | 14 subway and 46 tram relations |
| **A second layer? (probed 2026-09-24)** | **BAG on the same API**: **10,898** units whose use class is *winkelfunctie* (shop) and whose status is *in gebruik*, all with a point, **90% shop-only** (9,837), the rest mixed. **1.77×** OSM's 6,150 shops (nonsense-term control: 0). But BAG records what a unit is **for**, not what is there: **no name, no activity, and `feitelijkGebruik` (actual use) empty on all 10,898** — a vacant shop counts, and so does a hairdresser. Restaurants and cafés sit mostly under *bijeenkomstfunctie* (6,717 units), which the permits already cover better. **Licence not read** |
| **How many are empty? (measured 2026-09-24)** | **No open source marks a unit empty** — the property snapshot (`standvastgoed`, 134 fields per address) has no occupancy field, energy use is published per neighbourhood only, and the per-unit sources (Locatus, KvK) are paid or staff-only. **But the rate is published**: the city's statistics (`bbga`, source **Locatus**, 1 January 2026) count **660 vacant of 14,314 sales points — 4.6%**, 0–7% by district, with a rate for all 110 *wijken* and 465 of 545 *buurten*. So empty shops are about one in twenty: disclosable, not filterable |
| **Nothing else** | The other 97 datasets were listed in full: shopping-area polygons (`winkelgebieden`, 142), terrace tariff zones (11), B&B and mooring permits, city-owned property — **none premises-shaped** |

**One bucket, and the best-maintained one in this band** — the only register
here that drops premises when their permit ends. It joined Stockholm, Göteborg
and Zurich under the same owner question — until the BAG gave it a second layer.

**✅ DECIDED (owner, 2026-09-24): BAG becomes the second layer**, with the
vacancy rate disclosed on the page (**4.6%** city-wide, Locatus via the city's
statistics — no open source filters it per unit). Retail and personal services
share one category, which the page says; takeaways that are both shop-class and
permit holders are de-duplicated by address at build. **Conditional on two
licence reads** (BAG; the permits' SILENT-with-conflict position) — if both
pass, a build brief follows and the band question returns to the owner. The
same answer carries to Rotterdam's re-probe, since BAG is national.

<a id="band-a-rotterdam"></a>

### ▲ 🇳🇱 Rotterdam — Amsterdam's shape, the food layer rebuilt (2026-09-24)

**Moved here from the open gap on 2026-09-24 (owner's call), after two licence
reads.** Rotterdam publishes no hospitality register, so the food layer is
**rebuilt from its Gemeenteblad exploitation-permit notices** (KOOP's SRU API,
a point on 99.75%). Permits run five years, so the grants since 2021-09-24 give
**1,937 premises**. The method recovers **97%** of Amsterdam's live register
and overcounts about 1.15×. Shops and services come from the BAG's **6,170**
shop-class units in use (2.16× OSM shops). Vacancy is disclosed: **about 7% of
shop units registered as vacant (CBS, 1 January 2025)**. Licences: the notices
**PERMITTED WITH CONDITIONS** (Auteurswet art. 11 and CC0; the conditions are
on the harvest only); CBS **PERMITTED WITH CONDITIONS** (CC BY 4.0); BAG Public
Domain Mark. Brief: `docs/build_briefs/rotterdam.md`, **6/6**. Build-time
calls: coffeeshop and sex-business permits inside the notices; RET metro and
Line E's scope.

<details><summary>Its open-gap row, kept</summary>

| What it rested on | Next probe, and the re-probes |
|---|---|
| One search of `data.overheid.nl` (top hits were neighbourhood counts). Amsterdam's own API later showed the KvK register gated (403) and KvK's open dataset cuts locations to two postcode digits | Rotterdam's own portal for a hospitality-permit register like Amsterdam's ▶ **Re-probed 2026-09-24 — PARTIAL: Amsterdam's second layer, not its first.** BAG via PDOK: **6,170 shop-class units in use** in 0599 (98.6% shop-only; the same query reproduces Amsterdam within 1.5%), **2.16× OSM shops**, Public Domain Mark. **No current hospitality register** on any city host (data.rotterdam.nl 1,434 datasets — its `q=` is silently ignored; the ArcGIS server's 1,104 layers; 2,741 public ArcGIS Online items) — only staff layers built from the city's business register (horeca 2,072 rows from 2018; all buckets 5,942 from 2020, names blank, licence field empty). The Locatus vacancy figures (`rotterdam.incijfers.nl`) are **geo-blocked** (NL and DE only). **RECOMMEND: leave in the gap** — a shops-only BAG map is weaker than any built city ▶ **Second re-probe 2026-09-24 (owner's call) — NEW FINDS: Amsterdam's shape is now reachable.** A hospitality layer REBUILT from the city's own permit notices: every exploitation-permit decision is published in the Gemeenteblad, and the national official-publications API (KOOP, CC0 declared) returns them with a point (99.75%); 6,045 notices since 2021 give **1,937 distinct premises** (permits run five years, read in 48 sampled notices). **Validated on Amsterdam**: the same method finds 97% of Amsterdam's live register within 10 m and overcounts about 1.15×. 1.12× OSM food (about 0.98× after that surplus; Amsterdam's register is 0.95×); 76% of OSM hospitality features have a permit premises within 25 m. No names, no sub-category, and closed premises stay until expiry. **Vacancy replaced**: CBS's 2025 vacancy monitor counts **7.1%** of Rotterdam's 6,060 shop units empty (CC BY 4.0; the same table gives Amsterdam 4.4% against its brief's 4.6% Locatus). Personal-service permits are almost absent, so retail and personal services stay one BAG category, as in Amsterdam. **RECOMMEND (owner): Band A as an Amsterdam-shaped city**, after two licence reads (KOOP notices, CBS) |

</details>

<a id="band-a-four-cities"></a>

### ▲ Four cities joined this band 2026-09-23, when the coordinates band closed

**Their coordinate route was the thing being measured, and all four now have it MEASURED and a brief written** — Prague 5/5, Oslo 5/5, Hong Kong 8/8, and Copenhagen's data in hand with its licence read. **A band whose condition stops being true of every member should close, not be re-captioned around them** — the same reasoning that closed the old Band D when Bucharest finished screening.

**Every route in this band was probed on 2026-09-22 and answered.** The band
used to say the method was "identified and cheap", which is a description of a
plan rather than of a measurement. It is now a hit rate per city, taken against
each register's **own** addresses rather than hand-typed landmarks.

**The band splits in two, and the split is the useful thing:**

- **A JOIN** — the whole address table downloads, and coordinates come from a
  dict lookup. No per-row requests, no rate limit, no geocoder to be wrong.
  **Prague and Copenhagen.**
- **A GEOCODE** — one request per distinct address, against a service that
  answers. **Oslo and Hong Kong**, both keyless. *(Singapore's geocode was
  measured here too, at 98.8%, before the city moved to the one-bucket band.)*

**Taiwan left this band** for the national-geocoding band: its route was the one claim here that did
**not** survive probing. **Bucharest's primary is down** but its fallback is
measured.

*[The band's table stood here; it stays in city_master_list.md.]*

**⚠️ Two facts here that are NOT about coordinates and change build scope:**

- **Oslo's register is not filtered by the address you read.** Bronnoysund's
  `?kommunenummer=0301` does **not** guarantee `beliggenhetsadresse` is in
  Oslo — a sample turned up Bergen, Copenhagen, Paris and Malmö, and
  `adresse` is a **list** whose first line is sometimes `c/o Osnordic AS`.
  **This is the registered-office trap in a third costume**, after ONRC, ACRA
  and SIRENE's *sièges*. The generalisation worth keeping: **a filter
  parameter and the field you read are two different addresses until proven
  otherwise.** How much of Oslo's 152,128 is physically in Oslo is **still
  unmeasured** — brreg's API stops paging past ~10,000, so both samples came
  from the alphabetical head and disagreed (24.5% vs 4.3%). **Settle it with
  the bulk download at build time, not with the API.**
- **Three of these services report their own confidence; Oslo's does not.**
  DAWA returns a `kategori` (A exact / B normalised / C ambiguous — it
  returned **B** for `Raadhuspladsen 1 1550 Kobenhavn` with the diacritics
  stripped, and **C with 30 results** for an ambiguous one) plus a
  per-address `nøjagtighed`; ALS returns a `Score`. **A geocoder that says
  when it is guessing is worth more than one with a higher raw hit rate** —
  which is exactly what Oslo's `fuzzy` lacked.

---

<a id="closed-band-b"></a>

## ✗ Band B — CLOSED 2026-09-24: Japan's coordinate step was a join (0 cities)

**Closed by succeeding, like the coordinates band before it (owner's calls, 2026-09-24).** Its caption was *geocoding at national scale*, and Japan's address work turned out to be a block-level join to MLIT's 位置参照情報 at 95–100%, so the condition stopped being true of all ten. **Where they went**: Band A takes Tokyo (8 wards), Osaka, Kobe, Sapporo and Fukuoka; the one-bucket band takes Hiroshima; the access-blocked band takes Sendai (the city's permission); the open gap takes Yokohama, Nagoya and Kyoto (no current food list). **Everything below is kept as evidence.**

**The investment tier.** These share one property that separates them from
the buildable band: the address work is a project rather than a step, and it is worth
doing only because the machinery, once written, is reused across many
cities. **Japan is ten cities from one schema, and since 2026-09-23 it is
the whole band.** Kaohsiung left for the access-blocked band (D) the same
night: it needs no geocoder, only a publisher who opens its file.

▲ **São Paulo and Rio left this band on 2026-09-23 — upward, to A — by not
needing a geocoder at all.** Brazil's census address file turned out to carry
every establishment with its own coordinate (see the Brazil section in Band
A). **The lesson for the two countries still here: before building a geocoder,
look for an address file that already carries the coordinate** — Prague's
RÚIAN, Copenhagen's DAWA and now Brazil's CNEFE were each that, and each
turned "a geocoding project" into a join or into nothing.

| Cities | Country | Business leg | The coordinate step |
|---|---|---|---|
| **Tokyo**, Osaka, Nagoya, Yokohama, Sapporo, Fukuoka, Kyoto, Kobe, Sendai, Hiroshima *(10)* | 🇯🇵 | Premises-level food permits, CC BY declared, one national schema; **personal services from the 生活衛生 registers (11 Tokyo wards)**; food retail only where a ward publishes 届出. No general retail | ✅ **SOLVED 2026-09-24 — a JOIN, not a geocode**: MLIT 位置参照情報, **99.3% at block level on 24,297 Tokyo food premises** (Minato control 99.8%), personal services 98.8–99.8%; independent check against publishers' own coordinates median 22–43 m. ⚠️ **What stops Japan now is COVERAGE**: food files for **4 of 23** Tokyo wards; central Chiyoda, Shibuya, Toshima absent from Tokyo's catalogue (one method — their own sites next). **RECOMMEND (owner's call):** this band's caption no longer describes Japan; re-band on coverage once the nine cities and the ward second pass are in |


*(A paragraph here said Bucharest's rail was uncounted and its licence unread.
**Both were done on 2026-09-22/23** — 13 relations counted, licence SILENT —
and Bucharest now sits in the one-bucket band, where its full record is. The
paragraph was removed from this band on 2026-09-23 because Bucharest is not
in it.)*

**Brazil was chosen as the next geocoding work on 2026-09-23 and left the band
the same afternoon** — CNPJ is geo-blocked, and CNEFE made the geocoder
unnecessary. **Taiwan was next, and its first probe the same evening found it
is a JOIN too** (Taipei 92.5%, see its row). If the other three cities
confirm, **this band will hold only Japan** — and Japan's own address
registries are the next thing to look for.

**Japan is ten cities from one schema** — the best marginal-city cost in the
screen — against the worst geocoding problem and a two-bucket ceiling.
**Still the biggest open decision in this list**, and a judgment call rather
than a probe.

📘 **Before starting Japan, read `docs/geocoding_retrospective.md`** (written
2026-09-23). Brazil and Taiwan both left this band because the address file
already carried the coordinate. **The retrospective predicts Japan is a
block-level JOIN too** — the permits split the address into municipality /
町字 / 番地以下 on 98% of rows, and MLIT's 位置参照情報 publishes those
components with a coordinate per block — **ASSERTED, not measured**, with the
order of work to test it.

<a id="open-screening-gap"></a>

## ⚠️ OPEN SCREENING GAP — rows that rest on an absence (0 cities — EMPTIED 2026-09-24)

✅ **Emptied 2026-09-24 (evening) by a final re-probe of its last eight, each given a
verdict on the owner's calls.** The owner asked for "an exhaustive final search on all open gap
cities" and "a definitive verdict on each". Four agents tried only the methods not yet tried:
- **Riga → Band A**: its rail was measured (trams pass; suburban rail fails on frequency), and
  the owner accepted the scoped vacancy disclosure.
- **Yokohama → Band C**: personal services only, and no page for now.
- **Lisbon → Band D**: DGAE's register needs a free account.
- **Helsinki and Tallinn → Band D**: geo-blocked. Their lookup-page harvests were declined.
- **Vienna, Santiago and Nagoya → the discards.**

**The rows below are kept as the evidence each verdict rests on**, not as a queue. A city
enters this section again only on a row resting on an absence.

**Not candidates yet and not discards — unscreened.** `global_country_shortlist.md`
records *"Italy stays a Milan-only country"*, but that rests on **Naples** and
**Messina** measuring out. **Rome and Turin appear nowhere in any list**, which
`add-country` is explicit about: a row whose reason is "not reached" is not a
discard.

**Run each re-probe through the `reprobe-city` skill** — the process that took
Amsterdam from a discard to Band A in one evening.

**▼ 2026-09-24 — twelve rows back from the discards**, in re-probe order (biggest
rail and clearest next probe first). Each rested on ONE method, and
Amsterdam — the same shape — turned out to have a current premises register
on its own host the night it was re-probed. The evidence each carried is kept.

**▼ 2026-09-24 — five more, when the discard table got evidence columns**
(owner's call). `scripts/check_discard_evidence.py` refused them: Naples and
Messina rested on one search; Santiago's and Lima's coverage verdicts never
asked the missing districts' own sites; Hyderabad's own host was blocked and
never diagnosed from inside India. They sit below the twelve, cheapest probe
first.

**▼ 2026-09-24 (morning) — six rows left on the owner's calls after their re-probes.** Kuala Lumpur, Athens, Poznań and Bratislava went to the discards (negative on two methods, the city's own host asked), and Hamburg too, on currency (a 2016 retail survey and nothing else). Warsaw went to Band D (its own catalogue is geo-blocked to Poland). **Vienna stays**, owner's call, although its two-method negative would pass the discard check.

**▼ Later the same morning, four more on the owner's calls after the last re-probe batch**: Naples, Lima and Messina to the discards, and Hyderabad to Band D (its own site is geo-blocked to India).

**▼ 2026-09-24 (late morning) — Rotterdam left for Band A, and Yokohama, Nagoya and Kyoto arrived from the closed Japan band** (owner's calls). Riga stays partial: its only vacancy figure covers about a third of the mapped shops (owner).

| City | What it rested on | Next probe |
|---|---|---|
| **Vienna 🇦🇹** ▼ *from the discards 2026-09-24* | GISA (national, 1,032,283 trade licences) strips the street address by design — national only | Enumerate `data.wien.gv.at` for a city-run premises / Gastgewerbe dataset. **Rail is the deepest in the screen: 35 subway and 185 tram relations** ▶ **Re-probed 2026-09-24 — PARTIAL (weak); no general register on the city's hosts, now on two methods.** City WFS enumerated (377 layers) and data.gv.at (Stadt Wien 781 / 2,296); the only premises rows are **outdoor-seating permits** (Schanigärten, 3,165 approved at 2,745 addresses, CC BY 4.0) — no name, no activity, **0.42× OSM food**. The BEV address register's building use class is whole-building (2,434 retail buildings, 0.19× OSM shops) — not a shop layer. **RECOMMEND (owner): discard as a general register** (the two-method rule now passes); the seating permits are not worth building on. Side find: Linz publishes trade licences (unprobed) |
| **Helsinki 🇫🇮** ▼ *from the discards 2026-09-24* | The national PRH register, a 500-company sample: 89.8% addressed, but 53% real estate and 4.8% retail — national only | Helsinki Region Infoshare (`hri.fi`) for a municipal food-control or premises register ▶ **Re-probed 2026-09-24 — PARTIAL; the city's catalogue is GEO-BLOCKED outside Europe.** `hri.fi` and `avoindata.fi` answer Finland and Germany, 403 to the US — so the city's own catalogue is still unasked. **Lead: Oiva**, the national food-inspection register — premises rows with name, sector, address; reached only through its site search (300-result cap, no count); its open channel is a Qlik dashboard; licence unknown; joinable to the city's 58,307 address points. The building register counts premises per building (30,759 in 7,220) but gives no use class per premises. **Next: two reads from inside Europe** (HRI's catalogue; whether Oiva is a bulk file on avoindata.fi) — cannot be discarded ▶ **Low-cost probe 2026-09-24 — still needs a read from inside Europe.** The national portal's new domain (`avoindata.suomi.fi`) is also 403 from here, the same block as `avoindata.fi`, and was not routed around. The Food Authority's own open-data pages answer, but their only surveillance-data link is the analytics portal (the Qlik dashboard found before). No bulk Oiva file is reachable from outside Europe. **Next unchanged: a read from inside Europe** (HRI's catalogue; whether Oiva is a bulk file on the national portal) |
| **Lisbon 🇵🇹** ▼ *from the discards 2026-09-24* | `dados.gov.pt`: 430 hits for *estabelecimentos*, all aggregate hotel statistics — national only | Lisboa Aberta, the city's own portal, for licensed establishments ▶ **Re-probed 2026-09-24 — PARTIAL (stale): the right data, last surveyed 2010.** The city's **commercial census** (Recenseamento Comercial, 14 waves 1991–2010): the 2010 wave has **17,200 rows** — 11,395 retail, 5,654 food and drink — with name, 154 activity types, address and a point; CC0; no personal services; some rows carry private individuals' names. Retail **2.0×** and food **1.22×** OSM. The city's CKAN (`dados.cm-lisboa.pt`) is behind a **Cloudflare challenge for every automated client** (not bypassed); its ArcGIS Hub (75) and Online (743) were enumerated, and the national portal holds 316 of the city's ~530 datasets. **Next (owner): ask the city whether the census continued or its licensing register can be published; or a person browses the CKAN** ▶ **Low-cost probe 2026-09-24 — a NATIONAL, GEOLOCATED establishment register exists, behind a free account.** The RJACSR law created DGAE's *cadastro comercial*, a database of commerce, services and restaurant establishments, and its public app **Mapa do Comércio, Serviços e Restauração** (`mapadocomercio.dgae.gov.pt`) places them on a map, searchable by area, sector and CAE code. The app's API (`cadastro.dgae.gov.pt/api`) has `/estabelecimentos` and `/estabelecimentos/exportar`, but **both return 401 anonymously**, and the app offers login through Autenticação.gov or a user registration. Only aggregate indicators and settings answer without one. **Not worked around**: no token requested, and a CMS key embedded in the app's JavaScript was not used. The France/Mexico shape (one national register for every city), so it would serve **Porto** too. Licence and row count unknown until someone logs in. **Next (owner): whether to register a free account** (`docs/gated_access.md` item 28), then measure rows, CAE fill, coordinates and terms |
| **Tallinn 🇪🇪** ▼ *from the discards 2026-09-24* | The national MTR downloaded whole (102 MB): full activity, no location field — national only | Tallinn's own open data for a premises register. Trams only ▶ **Re-probed 2026-09-24 — STILL THIN.** City's own host asked: `www.tallinn.ee` behind a Cloudflare challenge (not bypassed); the city's 49 datasets on andmed.eesti.ee (filter confirmed, nonsense 0) hold no premises register. **Two national candidates**: the food-handlers register (`Toidukaitlejad.xml`, daily, CC BY-SA 3.0) is **geo-blocked** — `avaandmed.agri.ee` answers Estonia and Germany, times out from the US and here, while `www.agri.ee` answers everywhere; and the **building register (EHR)** has unit use classes for all three buckets (12131 restaurant … 12331 personal services) but its data comes by `POST /reports` with an **e-mail address — the owner's act**. OSM: 1,255 food, 3,532 shops, 511 personal services. **Next (owner): one EHR order for Tallinn (`ehitis_kaos`)** |
| **Riga 🇱🇻** ▼ *from the discards 2026-09-24* | The national company register (`data.gov.lv`, 21 fields): addressed, no activity column, 60% terminated — national only | Riga's own portal for a premises or food register ▶ **Re-probed 2026-09-24 — PARTIAL: a real premises register, alcohol and tobacco only.** The State Revenue Service's excise-licence register (data.gov.lv, CC0, daily; latest 2026-09-22): **2,898 current Riga premises** at 2,193 addresses, with location and a type field (shop, café, bar, restaurant…) and opening hours — **food service 1,596 (1.10× OSM)**; retail 746, alcohol/tobacco sellers only (0.14× OSM shops); no personal services. Joined to Riga's own address points: **96.2%** exact. **Second shape**: the cadastre's premise groups (VZD, CC BY 4.0) — 7,169 retail/wholesale (1.32× OSM shops) and 5,207 hotel/catering, but only 35–41% carry an address code (placement via the building cadastre number unmeasured; vacancy, wholesale and hotels mixed in). The food-safety agency's register (`pakalpojumi.pvd.gov.lv`) is **geo-blocked** (LV and DE only). The city's own host `opendata.riga.lv` does not resolve; its 79 datasets on data.gov.lv hold no premises. **Next: place the premise groups through the building cadastre number, find a vacancy rate, then read three licences** ▶ **Follow-up 2026-09-24 (owner's call) — AMSTERDAM'S TWO-LAYER SHAPE, with a heavy vacancy caveat.** The cadastre premise groups place through the building cadastre number: retail/wholesale 7,133 of 7,169 (99.5%) on building outlines, catering class 100%; a second route (the building-address link to the address register) agrees at a median 3.6 m. Class 1230 by name: 4,816 named shops (67%, 84% on the ground floor; 0.93× OSM shops including hair and beauty), only 3.8% wholesale, storage or offices; 62% last surveyed before 2010. Class 1211 is 81% hotel rooms, so the excise register stays the food layer. **Vacancy: 20.4%** of 2,324 street-front ground-floor premises, from a 2024 municipal field survey of the historic centre only; no citywide figure (Amsterdam's 4.6% was citywide). **RECOMMEND (owner): Band A only if a centre-only 20% vacancy is accepted as the disclosure; otherwise keep it partial.** Rail not yet examined (trams, suburban rail) ▶ **Vacancy investigation 2026-09-24 (owner's call) — only a SCOPED disclosure is workable.** No citywide rate exists: CSP has no non-residential vacancy table, none of the cadastre's 57 building or 13 premise-group fields records occupancy, and market reports are silent, from 2012, or 403 (Colliers, left alone). A second municipal figure: the Old Town re-survey of summer 2025, 87 of 573 premises vacant (15%). An occupancy proxy (OSM or excise licences on the same building) matches the centre's overall level (64–68% against the survey's 67.4% occupied) but cannot rank streets (Spearman 0.23), so it stays internal. The cadastre does count the same premises the survey counts (street-by-street Spearman 0.96). **In the station rings (966 m, 243 tram stops, 39 rail stations): about 36% of named shops are on the surveyed streets (20.4% vacant, 2024), about 6% in the Old Town (15%, 2025), and about 64% are not measured.** Side find: 208 named shops (4.3%) sit in buildings the city lists as degrading (CC BY 4.0), and can be dropped. **Owner's call: publish the scoped disclosure (both figures, their areas and dates, 'not measured elsewhere'), or keep partial** |
| **Santiago 🇨🇱** ▼ *from the discards 2026-09-24, on the evidence check* | `datos.gob.cl`, searched and its 272 publishers enumerated: 5 of ~33 Metro comunas publish patentes. The Santiago comuna is not on the portal, and its own site was never asked | The Santiago, Providencia and Las Condes municipalities' own sites for a patentes register — the comunas the Metro converges on ▶ **Re-probed 2026-09-24 — STILL THIN on coverage; Providencia found.** Providencia publishes its current commercial licences monthly under the transparency law (`transparencia.providencia.cl`, a 31/08/2026 XLSX of 74,712 rows; name, address and activity text 100% filled; about 78% offices or tax addresses, and a first keyword pass leaves at least 6,309 storefronts: 2,034 food, 2,533 retail, 1,742 personal services; 2.07× OSM food, 2.56× shops) — no coordinates, no named address file, no licence declared. The Santiago comuna publishes patentes only as 2016–2019 lists and, since 2020, as decrees; its file host `transparencia.munistgo.cl` returns 403 to everyone, Chilean probes included; its observatory shows 2019 density classes only. Las Condes marks its Maestro Patentes unpublished. Coverage is now 6 of about 33 comunas, downtown still missing. **Next (owner): a transparency-law request to the Santiago comuna (a form with a name, so the owner's act); for Providencia, an address file and a licence read** ▶ **Downtown probe 2026-09-24 (owner's call) — PARTIAL, alcohol licences only; STAYS IN THE GAP.** The comuna's own document site (`documentos.munistgo.cl`, never asked before; its sitemap lists 396 posts, 37 on patentes) carries the semester decrees renewing ALCOHOL licences with full lists: Decreto N° 330, 1st semester 2025, 1,832 rows (about 2,084 across the semester's group decrees), with name, street address and licence class (restaurants day and night, cantinas, liquor stores, beer sellers). But they are scanned PDFs with no text layer, about 20 months old, food and liquor only — and the later decrees sit on `transparencia.munistgo.cl`, still 403 to everyone. Individuals appear by name and RUT (never published). A placement route exists: the comuna's own ArcGIS Enterprise (`gis.munistgo.cl`) has street centrelines with address ranges (3,967 of 4,479) and 74,506 house numbers — no licence declared, join unmeasured. Other routes negative: the transparency council's catalogue (8 datasets), the comuna's 429 ArcGIS Online items, its observatory hub, `datos.gob.cl` (neither the comuna nor the SII publishes there); the SII's property file with use classes is behind a taxpayer login. OSM (comuna): food 1,092, shops 3,400. **Next (owner's act only): a Ley 20.285 transparency request for the current commercial-licence list** |
| **Yokohama 🇯🇵** ▼ *from the Japan band 2026-09-24 (owner's call)* | The overnight screen found **no current food list** on the city's own hosts: city lists stop at the 2021 food-hygiene reform, which moved filing to MHLW's 食品衛生申請等システム. That system's open data is an **opt-in slice of online filings**: 2,912 restaurants here, and 1.9–8.1% of the restaurants on the complete lists it was measured against. The coordinate step is solved (the Japanese join), so only the list is missing | A `reprobe-city` pass of the city's own hosts and catalogue for a current list, or a request to the city — Fukuoka and Hiroshima show the own-list-plus-MHLW shape works where the city keeps its counter filings ▶ **Low-cost probe 2026-09-24 — food NEGATIVE on two methods; personal services only.** The city's CKAN (`data.city.yokohama.lg.jp`) has no food-permit dataset: 食品 returns 11 newsletters and statistics, 営業許可 6 statistics, nonsense 0. The overnight screen found no list on the city's own pages. Personal services are complete: 環境衛生関係施設一覧, barber, beauty and cleaning ZIPs split per ward, as of 2026-04-01, CC BY. MHLW's opt-in slice holds 2,912 restaurants. **A one-bucket city whose one bucket is personal services**, a shape no band holds yet. **RECOMMEND: stays in the gap**; a request to the city for its food list is the next step, and the owner's act |
| **Nagoya 🇯🇵** ▼ *from the Japan band 2026-09-24 (owner's call)* | The overnight screen found **no current food list** on the city's own hosts: city lists stop at the 2021 food-hygiene reform, which moved filing to MHLW's 食品衛生申請等システム. That system's open data is an **opt-in slice of online filings**: 1,058 restaurants here, and 1.9–8.1% of the restaurants on the complete lists it was measured against. The coordinate step is solved (the Japanese join), so only the list is missing | A `reprobe-city` pass of the city's own hosts and catalogue for a current list, or a request to the city — Fukuoka and Hiroshima show the own-list-plus-MHLW shape works where the city keeps its counter filings ▶ **Noted 2026-09-24 — not rebuildable.** BODIK keeps only 12 rolling months of new food permits (2025-09 to 2026-08), and the city publishes no full standing list, so Kyoto's stitch cannot be done. The beauty-salon list is current (city page, as of 2026-08-31, CC BY 4.0). **Next: a request to the city for its full list (the owner's act), or older monthly files from an archive** |

*▲ **Rome left this gap on 2026-09-24 for Band A** — see its section there.*

*▲ **Kyoto left this gap on 2026-09-24 for Band A**, its register rebuilt from the permit stream — see the Japan section there.*

*▼ **Turin and Cairo left this gap on 2026-09-24 for the discard table**, each measured by two methods — see there.*

*▲ **Prague left this gap on 2026-09-24, back to Band A**, the same day it arrived: the premises source it lacked turned out to be published as open data (ROS02). Its row is in Band A.*

**Neither Italian city changes the Italy profile answer** — Italy is bespoke per city, so
each would be its own Step 0 regardless. See `DECISIONS.md`, 2026-09-22.

### The sweep, 2026-09-23 — what else rests on an absence

**Audited the whole discard record** for rows whose stated reason is *"not
reached"*, *"unprobed"*, *ASSERTED*, or a regional pattern. `add-country` is
explicit that such a row **is not a discard**, and records that exact error
happening twice — once to a group including **Italy, which then passed**.

| Row | What its reason actually was | Probed 2026-09-23 |
|---|---|---|
| **Göteborg** 🇸🇪 | *"Unprobed candidate"* — named twice in this file and **placed in no band at all** | ✅ **REAL, and it is a candidate.** `catalog.goteborg.se/store/search?type=solr` — EntryStore, the same platform as Stockholm's. **`Livsmedelsverksamheter`** is *"Alla aktiva livsmedelsverksamheter"* — **active food BUSINESSES, not inspections**, so no dedupe, where Stockholm's 8,146 premises had to be distilled from 289,742 inspection rows. **`Restauranger med serveringstillstånd`** declares **CC ZERO** — stronger than Stockholm's SILENT. Rail is trams, not a metro: **better data, weaker map** |
| **Lisbon** 🇵🇹 | On *"Countries ruled out"* with **no parenthetical evidence at all** | ⚠️ **Discard now EVIDENCED, and it holds.** `dados.gov.pt` returns 430 for *estabelecimentos*, but they are **aggregate hotel statistics** (*"Proporção de estabelecimentos hoteleiros que utilizam computador (%)"*) and prison establishments. The aggregate trap |
| **Warsaw** 🇵🇱 | Same — **no evidence** | ⚠️ **Discard now EVIDENCED, and it mostly holds.** Control passes (`zzqqxx` → 0, so the search filters). `CEIDG` is company-level, as recorded elsewhere. **One premises-shaped lead survives**: *Wykaz punktów sprzedaży napojów alkoholowych* — licensed alcohol sales POINTS, the Singapore-tobacco shape. One bucket at best |
| **Cairo** 🇪🇬 | Same — **no evidence** | ⛔ **STILL UNPROBED.** Recorded as an absence rather than a finding — ▼ **and on 2026-09-23 moved OUT of the discard table onto the open screening gap**, where this finding says it belongs |
| **Zagreb** 🇭🇷 | *"identical 1,291-byte SPA shell at four paths"* | ~~⛔ **Confirmed BLOCKED, not negative.** Three more paths tried 2026-09-23, all shells~~ ⚠️ **SUPERSEDED — this row contradicted the discard table, and the discard is the measured one.** `data.gov.hr`'s CKAN lives at **`/ckan/api/3/...`**, not at the paths tried here; through it Grad Zagreb's **210 datasets** were enumerated on 2026-09-22 and the only commercial one is a grants list. **Three more shells at the wrong paths are not evidence of a block** — the discard stands |

**The generalisable result: a "ruled out" list is only as good as its weakest
row, and three of this one's rows carried no reason at all.** Two of those now
do. Göteborg was never ruled out — it was simply never placed anywhere, which
is how a candidate disappears without anyone deciding to drop it.

## 🔴 Band D — Kaohsiung's record from Band B

<a id="band-d-kaohsiung"></a>

<details><summary>Kaohsiung's full record while it sat in Band B (kept)</summary>

| Cities | Country | Business leg | The coordinate step |
|---|---|---|---|
| **Kaohsiung** *(1)* | 🇹🇼 | ▼ **The one Taiwanese city left here, 2026-09-23 — Taipei (Regional), Taoyuan and Taichung moved to Band A.** Kaohsiung's business side is measured (**72,550** storefronts in the national tax register) and its licence is the same OGDL v1; **its door-plate file (the 2026 edition, `高雄市115年門牌坐標資料-TWD97`, updated 2026-06-25) and its own metro station files sit on `data.kcg.gov.tw` / `openapi.kcg.gov.tw` / `api.kcg.gov.tw`.** 🚧 **GEO-BLOCKED, MEASURED 2026-09-23 (night)**: `data.kcg.gov.tw` answers **HTTP 200 to 3 of 3 Taiwanese probes** (two networks) and times out from Japan and the US, while `www.kcg.gov.tw` on the same network answers from everywhere — **a foreign-address filter on the data hosts, the publisher's access control, NOT routed around.** The national catalogue lists **no other host** for any Kaohsiung file. Moves to A only if the publisher opens it or publishes elsewhere — **the way through is asking the publisher**, an owner action. **The history of this row, kept:** ▲▲▲ **FINISHED 2026-09-23 (evening) — see "Taiwan finished" in `global_country_shortlist.md`.** Joins **Taipei 92.4% · Taoyuan 94.0% · Taichung 92.7%**; Kaohsiung's door-plate host unreachable, its business side measured at 72,550. **Rail needs no TDX** (now key-gated, and a Taiwanese mobile number to register): the agencies publish stations everywhere and Taipei's line geometry, keyless, under OGDL v1. **Taipei's door-plate licence: PERMITTED WITH CONDITIONS** (OGDL v1 — a prescribed attribution statement whose absence voids the grant, and a fault-based liability clause). **Head-office trap measured**: 38.7% of company rows look like offices, against 7.1% of sole proprietors. ⚠️ **Scope question: New Taipei** (76,320 storefronts) surrounds Taipei and its metro crosses the boundary — the Dublin/Lille regional shape. **The rows below are the earlier readings of the same day.** ▲▲ **2026-09-23: the national BUSINESS TAX REGISTER** (`全國營業(稅籍)登記資料集`, Fiscal Information Agency) — keyless, **refreshed daily**, one row per trading location with `營業地址` (the business address), a parent ID so **branches are their own rows**, a trade name, and a 6-digit industry code whose **47/48 · 56 · 96** are retail · food · personal services. **No personal-name column.** Taipei: **76,519 storefronts** after excluding 4,954 online-shopping rows (code 487, NAICS 454's twin) | ▲▲ **A JOIN, not a geocoder — MEASURED 2026-09-23 in Taipei at 92.5%** (food 95.1%, personal 99.0%, retail 90.0%) against the city's **door-plate coordinate file** (`門牌位置數值資料`, monthly, keyless, Open Government Data License v1.0). **Door-plate files exist for all four cities** on the national catalogue, which **exports whole and keyless** — the `ER0001` key error was one API endpoint, not the portal. Retail's misses are mostly **market stalls and under-viaduct stalls** with no door plate. ⚠️ **Still open before Band A:** the other three cities' joins (Kaohsiung's portal timed out from six nodes in five countries), the licence read, and whether company rows in the storefront codes are shops or head offices (Taipei's register is 104,489 有限公司 and 56,483 股份有限公司 against 69,156 sole proprietors). **Rail is NOT open**: TDX's metro endpoints answered unauthenticated on 2026-09-21 — 122 Taipei stations, line shapes and `LineColor` (see `global_country_shortlist.md`); re-verify at build. **The record below is the 2026-09-22 reading, superseded:** ⚠️ **MOVED HERE FROM BAND B 2026-09-22, on a probe rather than on a resemblance.** The row used to read *"moderate — NLSC's geocoder is keyless"*, and **that claim did not survive**: NLSC's API is alive and keyless, but the keyless endpoint is **reverse** geocoding (point → 村里) and administrative lists, not forward geocoding, and **no bulk 門牌 address-point file was reached**. `data.gov.tw`'s dataset API **requires an API key** (`ER0001:API Key錯誤`); its web pages are reachable, and `addr.tgos.tw` answers but has historically required registration. **Blocked, not negative** — and the Prague-shaped bulk join is still the thing to look for |

</details>

<a id="closed-bands"></a>

## ✗ Closed bands — kept in full as evidence, not as candidates

### ✗ CLOSED — access blocked (formerly Band G)

*▲ The condition is live again as **Band D** above since 2026-09-23 — Kaohsiung. This record is the band as it closed on 2026-09-22.*

**The band's premise was that the register exists and we cannot reach it, so
none of its members was a data negative.** That premise was correct and all
three left it in different directions. **Hong Kong** left upward: its bulk
export had been published on `data.gov.hk` all along and one `package_list`
call found it. **Hyderabad and Kochi** left downward: India's entire national
catalogue — **288,011 titles** — was walked, and every trade-licence dataset
in it is an aggregate. **A band for unreachable registers is only honest
while the reaching has not been exhausted.**

#### The band as it stood — access blocked, the register exists and we cannot reach it (2 cities)

> ⚠️ **▲▲▲ Hong Kong left this band on 2026-09-22, and it was never
> actually blocked.** It was recorded here as *"the portal is a measured
> negative (statistics only), but FEHD's register exists and is queryable —
> no bulk export found"*, and described as **the single most valuable open
> thread in the screen**. It was. **`data.gov.hk`'s CKAN `package_list`
> returns 3,821 datasets and nobody had pulled it** — the recorded negative
> was a search result. Enumerating found FEHD's own licensing system
> published as bulk XML: `LP_Restaurants_EN.XML`, `LP_OtherFood_EN.XML` and
> `LP_NonFood_EN.XML`, regenerated daily. **A negative from search is a
> statement about the search**, which Stockholm demonstrated the same morning
> and which cost this city several sessions of being called unreachable.

**None of these is a data negative, and the distinction is the whole point of
the band.** Rail is answered for all three. What is missing is a route to a
register that is known to exist — which is a different thing from a register
that was looked for and was not there.

**Five cities left this sub-tier on 2026-09-22** — Santiago, Kuala Lumpur,
Jakarta, Medellín and Lima — all to *discarded*, each with a measured reason.
What remains is the set whose business leg is genuinely still open.

⚠️ **Rio de Janeiro left too, and it was a FILING error rather than a new
measurement.** Its row read *"CNPJ, no coordinates → geocoding at São Paulo's
scale"* — which describes a **geocoding** blocker, while this sub-tier means
*the business leg is the blocker*. Rio's business leg is **CNPJ, the same
national register as São Paulo**, which sits in the coordinates band as
viable, and the Tier
view already paired them. **Rio had been banded by how it was DISCOVERED — the
OSM rail screen, which is what populated D-b — rather than by what is stopping
it**, and was never re-filed once the business leg resolved. That is the one
thing this band exists to encode, so the row was moved to the coordinates
band.

Rail screened via OSM. **Relation counts are upper bounds** — see the caveat
below.

> ⚠️ **None of these five is a discard candidate, and two rows were wrong.**
> Checked 2026-09-22 by fetching each host *and* asking the Internet Archive
> whether it has seen it recently — a recent snapshot behind a failing fetch
> means **the site is alive and the failure is ours**. That test has corrected
> this project three times in one session (Sevilla, Sofia, Bulgaria's 403).
> Here it found Hyderabad's portal recorded as "dead" when it is alive,
> Kochi's row describing a **live lead nobody had followed**, and Tel Aviv's
> city portal alive behind a block aimed at us. **Unreachable is not a
> finding.**

| City | Rail (OSM) | Business leg |
|---|---|---|
| ▲▲ **Tel Aviv** 🇮🇱 | *(later discarded — see the closed awaiting-permission band)* | **PROMOTED OUT OF BAND D 2026-09-22 — to Band B. Both legs measured.** The WAF-blocked portal was never the only host: `gisn.tel-aviv.gov.il` answers, and carries **22,176 licensed businesses** with activity *and* location. See the closed awaiting-permission band below |
| **Hyderabad** 🇮🇳 | 6 rel, all named + coloured | ⚠️ **RE-PROBED 2026-09-22; every remaining route is now closed too.** `ghmc.gov.in` — the licensing body — returns **403 in a real browser**, an F5 WAF page that names itself. `data.telangana.gov.in` resolves but is unroutable for us; it runs **DKAN**, and **the Archive holds ~200 URLs but not the dataset-list endpoint**, so the route that enumerated Romania does not work here. `tgbpass` is a false friend — *building* permits. And **`api.data.gov.in`'s `q` parameter is INERT**: `Telangana` and `zzqqxxnonsense` both return the identical **288,011**, so the national API cannot be filtered at all — only its website search can, and that was already measured negative. **Blocked, not negative** |
| **Kochi** 🇮🇳 | 2 rel, named + coloured | ⚠️ **PROBED 2026-09-22, and the lead was a FALSE FRIEND.** `go.lsgkerala.gov.in/pages/query.php?t=establishment` is a **Government Orders and Circulars search** — "establishment" matches 6,526 orders about *staffing*; Kochi's own `/establishment/396` is ജീവനക്കാര്യം, its **personnel** page. In Indian government usage "establishment" means staff posts, not premises. The real route is **K-SMART** (`tax.lsgkerala.gov.in` redirects to `ksmart.lsgkerala.gov.in`) and **Sanchaya** — both live, both **transactional citizen portals** for paying tax and renewing licences, **no bulk export found**. Kerala's local bodies do issue the licences, so the register exists. **The Hong Kong shape: blocked, not negative** |

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
not confirm", not "absent". It is no longer needed, but it would still be a
better source than a filtered register if it exists.

#### ✅ RESOLVED the same day: the filter works, and Paris is back in Band A

**The question was "can a NAF + siège + employee filter produce a defensible
storefront layer without mapping homes?" The answer is yes — and the siège
half of that question was the wrong lever.**

| Candidate filter, Paris NAF 47/56/96 | Rows |
|---|---|
| base | 148,633 |
| minus 47.91 online retail | 115,889 |
| **non-siège only** | **19,978 — far too aggressive** |
| not a sole trader, minus online | 79,359 |
| **A: `caractereemployeuretablissement = "Oui"`, minus online** | **50,156** |
| both employee and not-sole-trader | 47,833 |

**Filtering on siège is wrong and would have been a quiet disaster.** An
independent shop *is* its company's siège, so "non-siège only" keeps chain
branches and discards every independent — the exact inverse of what this map
is for. The **employee** filter is the right one: it keeps the boulangerie run
as an *entreprise individuelle* with staff, and drops the consultant
registered at home.

**Validated against OpenStreetMap**, which has no relationship to SIRENE:

| | OSM | SIRENE filtered | |
|---|---|---|---|
| One class — restaurants | **10,642** (`amenity=restaurant`) | **10,595** (56.10A + employer) | **0.4% apart** |
| Whole layer | **54,198** (`shop=*` 34,801 + food amenities 19,397) | **50,156** (candidate A) | **92.5% of OSM** |

Landing just *under* a volunteer map in a city as well-mapped as Paris is
where a register-derived layer should sit. The ~4,000 gap is the price of
dropping genuine zero-employee shops, and it is small next to the 65,733 rows
the filter removes.

**And there is no geocoding leg.** **148,576 of 148,633 (99.96%)** carry
`geolocetablissement` coordinates. France was being priced as if addresses
needed geocoding; they do not.

**What is still owed, and it is not a formality.** `employer = Oui` removes
home registrations **by proxy, not by proof** — a home-based business can
employ someone. So `check_personal_exposure.py` is load-bearing for Paris in a
way it is not for a municipal licence register, and a residential-address
check belongs in its Step 2. Separately, the Opendatasoft mirror used here
omits `enseigne1Etablissement` and `denominationusuelleEtablissement` — the
shop-sign fields, which are the strongest storefront signal available. INSEE's
own file carries them and would improve the filter further.

> **The relation counts are upper bounds.** The construction filter flagged
> unbuilt routes in Jakarta but returned **zero** for Tel Aviv, Bogotá and Rio —
> and Tel Aviv proves zero does not mean zero: its Green and Purple lines are
> under construction and OSM carries them as plain `light_rail` with no status
> marker. **A filter returning zero can mean "nothing to flag" or "this
> convention is not used here", and the result alone cannot tell you which.**


### ✗ CLOSED — awaiting permission (formerly Band B; Tel Aviv, discarded on terms)

**Band B held cities whose blocker was answerable at a desk.** Its last
member's desk work was done — the licence was read — and the answer was a
prohibition, which is not a desk problem. **The owner's call, 2026-09-22: a
written request made in advance and against explicit restrictive clauses is
not worth the effort.** That is a judgement about cost and likelihood, not
about the data, and the full measurement is kept below precisely so the
distinction survives.

**▲▲ Tel Aviv** 🇮🇱 — **promoted from Band D-b on 2026-09-22, and it is the
strongest unbuilt result outside Band A.** It had been carried as
*unreachable*: `opendata.tel-aviv.gov.il` and `www.tel-aviv.gov.il` both
return **HTTP 472**, Imperva's block code, and an earlier pass recorded the
host printing our own IP back — the one unambiguous IP-level refusal in this
project.

**The portal was never the only host.** `gisn.tel-aviv.gov.il` answers us
normally and serves `IView2`, the city's public map viewer — **254 layers**,
no key, no account. Third city in one day where the portal was walled and the
GIS service host was not.

| Layer | Rows | |
|---|---|---|
| **[964] `מאגר עסקים ברשיון או בהיתר`** | **22,176** | businesses holding a licence or permit — **the candidate** |
| [925] `עסקים` | **37,392** | businesses, with street + house number and floor area |
| [433] `רישיונות בביצוע` | 2,466 | licences in progress |
| [679] `מתחמי רישוי עסקים` | 29 | licensing zones (polygons) |

**Both halves of the location/activity split are present**, which is what
disqualified Tallinn, Colombia and Jakarta:

- **Activity** — `t_hesber_mahut_esek` in plain Hebrew (*grocery*, *building
  materials and paints*, *baking powder and pudding*) **plus** `mahuiot`,
  the numeric licensing-item code (406300, 407202, 1007200…).
- **Location** — `shem_rechov` (street), `ms_koma` (floor), and **point
  geometry in `wkid=2039`, Israeli TM — already projected in metres**, so
  no reprojection guesswork and no EPSG:4326 buffering trap.
- **Freshness** — `date_import` reads **20/09/2026**, two days old.

**Two questions, and both are owner decisions rather than probes:**

1. **Which business layer, and a privacy check.** [925] is larger (37,392)
   but carries **`shem_machzik_rashi` — "name of main holder"**, which is
   squarely the *registrant's own name* category this project's invariant
   excludes. [964] carries `t_shem_esek`, a **trade name**, which is the
   safe field. Recommendation: **build on [964]** and treat [925] as a
   cross-check only. `check_personal_exposure.py` must run either way.
2. **Licence — READ 2026-09-22, and it is the opposite of what "unread"
   suggested.** This was recorded as a gap to fill. It is filled, and what
   was behind it is a **prohibition**, not a silence.

   Read from the Internet Archive, because every page that carries terms is
   on the 472-blocked host — the same route that read Barcelona's and
   Sevilla's licences.

   | Source | What it says |
   |---|---|
   | **Municipal Terms of Use** (`/About/Pages/TermsofService.aspx`, captured 2026-04-21) | *"**אין להעתיק, לשחזר, לשנות, לעבד… להפיץ, לשכפל… לפרסם ו/או לאחסן את תוכן האתר**"* — do not copy, reproduce, modify, process, distribute, duplicate, publish and/or store the site's content |
   | The same document | *"**אין להשתמש בתוכן האתר ליצירת מאגר מידע ו/או לקט**"* — **do not use the content to create a database or compilation** |
   | The same document | forbids use on **other websites**, for any purpose, ***בין מסחרית ובין שאינה מסחרית*** — whether commercial or non-commercial — **without explicit prior written consent** |
   | Its definition of *"contents"* | explicitly includes **`מאגר נתונים`** — a database |
   | **`opendata.tel-aviv.gov.il`** footer (captured 2019-10-14) | ***כל הזכויות שמורות לעיריית תל-אביב-יפו*** — **All rights reserved** |
   | `data.gov.il` | Tel Aviv is **not** among its four municipal publishers — nothing to inherit |
   | ArcGIS server root, `/rest/info`, service | **no `licenseInfo`, no `copyrightText`** at any level |

   **The counter-reading, stated rather than resolved.** The Terms are titled
   *terms of use of the **website***, say *"תוכן האתר"* throughout, and the
   data sits on a **different host** (`gisn.tel-aviv.gov.il`). That is the
   **New York** situation from `read-licence`: an "All Rights Reserved"
   footer covering site content while the data itself was unrestricted.

   **But New York had an affirmative law — Local Law 11 of 2012 — forbidding
   the City to attach restrictions to its open data. Nothing equivalent is
   established for Tel Aviv**, the Terms explicitly name databases, and the
   open-data portal **asserts** rights rather than granting them. On the
   evidence the restrictive reading is materially stronger, and
   `read-licence` step 8 forbids resolving it in this project's favour.

   ⛔ **So Tel Aviv is not buildable on what is known.** The remedy is not
   more reading — it is **explicit prior written consent from the
   Municipality**, which the Terms name as the route. That is the
   **Philadelphia shape**, with one difference that matters: Philadelphia was
   already built and stands on a disclosed reasoned position, while Tel Aviv
   **has not been built and should not be** until permission exists. Tracked
   as `docs/gated_access.md` item 8.

**Rail is present but needs a scope decision, not a probe.** The city
publishes its own: Red Line stations **12**, Green **33**, Purple **19**,
with alignments. **Green and Purple are still under construction** — drawing
them would map lines that carry no passengers, the inverse of the
Guadalajara problem. Red is the operating line, and its 12 stations are the
in-city segment of a 34-station route that runs to Petah Tikva and Bat Yam,
so a boundary decision is needed too.

▼ **Valencia, Bilbao and Málaga left this band on 2026-09-22** — all three
probed, all three measured negative, all three now in *Discarded*. The
reasoning that put them here was *"two of the three Spanish cities probed have
had a register, which raises the prior sharply."* **The prior was wrong.**
Madrid and Barcelona are the exceptions in Spain, not the rule — see
"Spain is a two-city country" below.


**These two were sub-tiers of the former Band D**, which dissolved on
2026-09-22 when its live halves became Bands D and E. Both closed the same
day, and their contents are the evidence behind three discards — **Tallinn,
Sofia and Sevilla**. Kept whole, including the parts that turned out to be
wrong, because a superseded reading is how the corrected one gets checked.

### Former D-c — ✗ CLOSED (Tallinn and Sofia, both measured out)

**Finalised 2026-09-22.** These were "genuinely unreached, no finding either
way". All six are now reached and the sub-tier is closed out:

| | |
|---|---|
| ▲ **Stockholm** | promoted out — **now in the one-bucket band** |
| ▲ **Bucharest** | promoted out — **now in the coordinates band** |
| ✗ **Budapest** | **discarded** — both routes measured closed |
| ✗ **Zagreb** | **discarded** — 210 Grad Zagreb datasets, one commercial, and it is a grants list |
| ✗ **Sofia** | **discarded** — the block was routed around, and Sofia publishes no premises register |
| **Tallinn** | **parked on value**, with the äriregister half now measured |

**Sofia was the load-bearing example of "unreachable is not a negative" — and
it stopped being one.** Going around the 403 via the EU portal's SPARQL
endpoint turned it into a firm data negative, which is the outcome that
distinction exists to make possible: *reach it, then judge it.* **Tallinn is
now the only genuinely-unjudged city left in this band.**

| City | What the host actually does |
|---|---|
| ✗ **Tallinn** 🇪🇪 | **DISCARDED 2026-09-22 — MTR reached, downloaded whole, and measured.** No longer parked: the register that was going to be Tallinn's route has **no location data of any kind.** See below |
| ✗ **Sofia** 🇧🇬 | **DISCARDED 2026-09-22 — and on data, not on the block.** See the section below: the entire Bulgarian catalogue was enumerated from outside, and **Sofia does not publish a commercial-premises register.** The 403 was never what stopped it |

#### 🇪🇪 Tallinn: MTR reached and measured — 2026-09-22

The äriregister was already known to be company-shaped. **MTR**
(Majandustegevuse register) was the remaining hope, recorded as *"live HTML
with no API found, so it needs the browser"*. It needed no browser. Its
`andmed.eesti.ee` catalogue entry names a bulk export outright —
`mtr.ttja.ee/opendata/avaandmed_ettevotjad.xml`, `access: PUBLIC`,
`accrualPeriodicity: DAILY`, `applicableLegislation: ODD_LEGAL_ACT`.

**Note the recorded blocker was also wrong.** The search API was filed as
*"contract unpinned — 400 on empty `search` and on `limit=1000`"*.
`search=<term>&limit=5&page=1` answers fine; the contract simply rejects an
*empty* term. A parameter that refuses one value is not an unpinnable API.

The export is **102 MB**. It was downloaded in full and every element name
counted, rather than sampled — the head of the file is unrepresentative
(the first records are French and Polish cross-border filings, which would
have no Estonian premises anyway, and reading those two would have produced
the right answer by the wrong method).

| | |
|---|---|
| Undertakings | **56,401** |
| Licences | **100,431** |
| Estonian | **97.8%** (55,184) |
| Distinct element names in the whole file | **17** |
| **Elements naming a place** | **ZERO** |

The complete tag census is `ettevotja · registrikood · nimi · riik_kood ·
url · load · luba · tyyp · number · staatus · valdkond · tegevusala ·
emtak · emtak2025 · kood · kehtiv_alates · kehtiv_kuni`. No address, no
tegevuskoht, no coordinates. *(`vald` appears only inside `valdkond` —
a substring, not a field.)*

**This is the pure Colombia-RUES shape**: complete activity classification
(114 distinct `tegevusala`, plus EMTAK 2008 and 2025 codes) attached to no
location at all. And it fails the composition test independently — the
largest category is **`Teenindajakaart`, 25,130 service-worker cards**,
followed by freight-transport community licences and taxi vehicle cards.
**Personal and vehicle certifications, not premises.** Only `Toitlustamine`
(5,576) and `Jaekaubandus` (4,120) are storefront-shaped, and those are
Estonia-wide, not Tallinn.

Tallinn was parked on *value* — trams only, ~450k, the thinnest map in the
screen. It is now closed on *data*, which is the better reason.

#### 🇧🇬 Sofia resolved by going around the 403 entirely — 2026-09-22

`data.egov.bg` returns **403 in the browser as well as to curl**, resolves
fine via DoH (213.91.191.234), and the Internet Archive holds a 2026-04-02
snapshot — so the host is up and the refusal is **aimed at us**. That was
where this sat: *blocked, nothing learned.*

**`data.europa.eu`'s SPARQL endpoint harvests `data.egov.bg`, and it is a
different host.** Querying it recovered **11,635 Bulgarian datasets**
(ids 3–23,557) without ever touching the blocked origin. What they contain
settles Bulgaria:

| | Found | |
|---|---|---|
| `Регистър на търговските обекти` — commercial premises | **141** | across ~50 municipalities: Враца, Мадан, Костинброд, Карлово, Дупница, Тервел, Етрополе, Драгоман, Ихтиман… |
| `заведения за хранене и развлечения` — food & entertainment | **72** | the same shape again |
| **Столична община (Sofia)** | **76 datasets** | **neither register among them** |

Sofia publishes budgets, school and kindergarten lists, parking and
**taxi permits**, dams, war memorials, donations, municipal enterprises.
**No premises register of any kind.**

**So Bulgaria fails structurally, not administratively.** Its municipalities
publish exactly the register this project needs — routinely, ~50 of them —
but every one is a small town. **Sofia is the only Bulgarian city with a
metro.** The data exists where there is no rail; the rail exists where there
is no data. No amount of access changes that, which is why this is a
discard rather than a park.

**One limit on the technique, measured rather than assumed:** **0 of 20**
sampled records carry any `dcat:distribution`. The harvest is
**metadata-only** — titles and descriptions, no download URLs. The EU portal
is a **catalogue, not a bypass**: it can tell you what exists anywhere in the
EU, and the files stay behind whatever wall they were behind. That is enough
to *screen* a blocked country, and not enough to *build* one.

### Former D-d — ✗ CLOSED (Sevilla, reached and discarded)

**The whole sub-tier is closed.** Its single city was reached, measured and
discarded on the same day it was written up as unreachable. Read the section
below top-to-bottom: it is kept in full *because* the first two thirds are
wrong, and the correction at the end is the only part that stands.

▼ **Sevilla** 🇪🇸 — **downgraded 2026-09-22.** The rail half is unchanged
and still cheap: Spain's National Access Point answers **401**, the WMATA
shape, a free account. **The business half got worse.** Every route into the
city's own data failed:

| Route | Result |
|---|---|
| `www.sevilla.org`, `sevilla.org` | **do not resolve** — curl *and* browser |
| `datosabiertos.sevilla.org`, `.es` | do not resolve |
| `sevilla-ayuntamientodesevilla.opendata.arcgis.com` | live, but **"Can't access this content … Sign In"** — the Medellín shape |
| `datos.gob.es` federated catalogue | **no Ayuntamiento de Sevilla publisher exists.** The publishers returned for "Sevilla" are CIS (opinion surveys), **IGME (geological maps)** and the Junta de Andalucía |

**⚠️ DNS-over-HTTPS, 2026-09-22 — and it splits the failure in two:**

| Host | Cloudflare DoH | Meaning |
|---|---|---|
| `www.sevilla.org` / `sevilla.org` | **resolves → 94.198.88.169** | The host exists. Our 000 is a **routing failure on our side**, not DNS |
| **`datosabiertos.sevilla.org`** | **NXDOMAIN** | **The open-data subdomain genuinely no longer exists — for anyone.** The 521-dataset portal at that address has been retired |

**So Sevilla is two problems, not one.** The city's main site is reachable in
principle and blocked only to us; the open-data portal we were trying to reach
is **actually gone**. Whatever replaced it has not been found — and the ArcGIS
Hub, which is the obvious successor, is the sign-in-walled one. **That is the
thread to pull**, not the dead subdomain.

> ### ✅ RESOLVED 2026-09-22 — the thread was pulled, and it led all the way
>
> **Sevilla is now a measured negative on the business leg and a SOLVED rail
> leg.** Both halves above are superseded. How it opened:
>
> The last Archive capture of the dead portal (2024-04-25, already serving
> **503**) contains, in its own JavaScript, a KML link to
> `sevilla.idesevilla.opendata.arcgis.com/datasets/5df7320…_0.kml`. **A dead
> page named its successor** — that is the general lesson, and it cost one
> CDX query.
>
> **The sign-in wall was the HUB, not the DATA, and that reading was wrong.**
> Recorded above as "the Medellín shape", i.e. genuinely private. In fact
> `www.arcgis.com/sharing/rest` serves the city's public items **anonymously**,
> from org **`hcmP7kr0Cx3AcTJk`** on `services1.arcgis.com` — a host that
> answers us, while every `sevilla.org` address is retired or unroutable.
> Enumerating by owner returned **1,260 public items, 413 Feature Services.**
>
> **🚇 The rail leg is SOLVED, and the 401 is now irrelevant.** The city
> publishes its own metro:
>
> | Layer | Rows | |
> |---|---|---|
> | `METRO_Estacion` | **21** | `NOMBRE` — Ciudad Expo, Cavaleri, San Juan Alto… real named stations |
> | `METRO_Linea` | **20** | polylines with `ID_EST_INI`/`ID_EST_FIN` segment topology |
>
> No account, no NAP, no OSM. **Spain's National Access Point and its 401 are
> not on Sevilla's critical path at all.**
>
> **✗ The business leg is a firm negative**, and `Locales` is a **false
> friend** — the same trap as Kochi's "establishment", caught the same way,
> by opening it:
>
> | Layer | Rows | What it actually is |
> |---|---|---|
> | `Locales` + 10 district copies | **150** | `USO = VACÍO`, `ENTIDAD_CESIÓN_USO`, `ADSCRITO_A`, `Editor = 6_Empleo` — the city's own **vacant municipally-owned units offered for assignment**, published by the Employment directorate |
> | `BIENES INMUEBLES` × 11 districts, `Naves Industriales` | — | municipal **property holdings**, same family |
> | `APP_Mercados` / `Centros_Comerciales` | 18 / 120 | market *buildings* and shopping centres — **the Málaga shape**, `equipamientos` facility layers |
> | `Veladores_2023` | **389** licences (2,897 furniture items) | pavement-terrace occupation, EPSG:25830 |
>
> **Row count is what caught it.** `Locales` returns 150 city-wide and **1 for
> Triana**; Madrid's censo has 225,660. A name that matches Madrid's word for
> the right dataset, at 0.07% of the scale.
>
> All 413 Feature Services were scanned by title, not just keyword-filtered —
> the Bulgarian sweep's lesson about partial scopes applied to my own work.
> Nothing else is business-shaped. **Sevilla is DISCARDED on data.** The one
> real premises signal, 389 terrace licences, is a single narrow bucket far
> below Stockholm's 8,146 food premises, which is itself only a one-bucket
> city.

**And the Internet Archive confirms the portal was real while it lasted:**

| | |
|---|---|
| `www.sevilla.org` snapshot | **2026-09-12** — ten days old. **The site is alive** |
| `datosabiertos.sevilla.org` snapshot (2023) | **521 datasets, 1,345 distributions** — a real municipal portal |
| Enumerable from the archive? | **No.** The crawl is 347 URLs deep, 11 of them datasets, none commercial |

**This is unreachable, not a measured negative**, and the distinction is the
one this list's maintenance rule exists to protect. **Discarding Sevilla would
mean throwing away an unexamined 521-dataset catalogue because of our own
DNS.** Nothing has been learned about whether Sevilla licenses premises; only
that every route to asking is blocked on this side. **One attempt from a
different network settles it.**

**↑ That paragraph was right to refuse the discard and wrong about what it
would take.** It concluded a different *network* was needed; what it actually
took was a different *host* — `services1.arcgis.com`, reachable all along.
The rule held and protected the city from a premature discard; the cost
estimate attached to it was guesswork. **See the resolution above.**

<a id="tier-view-2026-09-22"></a>

## The 2026-09-22 tier view — RETAINED AS EVIDENCE, NOT CURRENT

The same 48 candidates, cut the other way. **Ordered by cities gained per unit
of work**, because that is what country-by-country optimises for, and it
reorders things sharply: Japan is mid-table by city and near the top by
country.

"Missing link" = the single thing that would move the country up a tier.

## Tier 1 — build now, nothing to discover (3 countries, 4 cities ready; ✅ Mexico DONE)

| Country | Cities | Source shape | Missing link |
|---|---|---|---|
| 🇲🇽 **Mexico** ✅ **COMPLETE** | **2** — Mexico City, Guadalajara (Regional) | **DENUE**, national, coordinates, SCIAN **is** NAICS — and the taxonomy **did** transfer from the US builds | **Nothing. Both cities are built and live in the app** (`pages/15_`, `pages/16_`, region *Mexico*), 2026-09-22. The ODbL share-alike decision was taken during the build |
| 🇪🇸 **Spain** ▶ **IN PROGRESS** | **2, not 6** — Madrid building now, Barcelona next | Bespoke **per city**, and the bespoke-ness cuts both ways | **Re-scoped 2026-09-22.** Valencia, Bilbao and Málaga all probed and all measured negative. Sevilla is unreachable. **Nothing left to find; Spain is a two-city country.** Both remaining cities have briefs and 9/9 checks |
| 🇰🇷 **South Korea** ✅ **BUILT 2026-09-25** | **1** — Seoul | 17 datasets, EPSG:5174, KOGL Type 1, daily | **Built.** Were build items, not probes: the register's own building points fill restaurants to 97.7%; a Korean-aware `check_personal_exposure.py` (113 premises sized). Owner's calls decided 2026-09-24 (`seoul.md`) |
| 🇮🇹 **Italy** | **1** — Milan | Bespoke per city. Naples and Messina measured out | **Step 0 schemas** for the two newly found Milan layers. Nothing to discover |

## Tier 2 — ⇄ France: demoted and restored the same day, measured both times (1 country)

| Country | Cities | Missing link |
|---|---|---|
| 🇫🇷 **France** ▲ | **6 cities, all six now MEASURED** — Paris, Lyon, Marseille, Toulouse, Lille, Rennes | **RESOLVED 2026-09-22, and it went in favour.** Mexico closed the architecture half; the composition half was closed by an **employee filter validated against OpenStreetMap** — 50,156 rows vs OSM's 54,198, and 10,595 vs 10,642 on restaurants alone. **No geocoding leg in any of the six** — see the per-city table below. Owed: `check_personal_exposure.py` is load-bearing here, since the filter removes homes by proxy, not proof |

#### 🇫🇷 The five non-Paris cities, measured 2026-09-22

The list had been carrying *"the filter is national, so it carries to all six
cities"*. **That was an inference from a one-city sample** — and it is the
same shape as the claim that collapsed Spain from six cities to two
(*"two of the three probed had a register, which raises the prior sharply"*).
France's risk was genuinely lower, because one national register covers every
commune where Spain was bespoke per city, but lower risk is not a measurement.

Source: `economicref-france-sirene-v3` on `public.opendatasoft.com` —
**43,896,818 records**, the same uncapped v3 stock this file already cites.
**Paris was run as a control first**, because a per-city rate from a query
that cannot reproduce a known answer only looks like evidence.

| City | Active | Geolocated | **Rate** | **Storefront layer** |
|---|---|---|---|---|
| **Paris** *(control)* | 1,335,566 | 1,335,333 | **99.98%** | **50,156** ✅ |
| **Marseille** | 239,997 | 239,781 | 99.91% | **8,065** |
| **Lyon** | 190,995 | 190,941 | 99.97% | **7,354** |
| **Toulouse** | 153,407 | 153,179 | 99.85% | **4,833** |
| **Lille** | 77,416 | 77,190 | **99.71%** | **3,272** |
| **Rennes** | 64,973 | 64,906 | 99.90% | **2,089** |

**The control reproduces the recorded 50,156 exactly**, so the storefront
column is the project's own filter (NAF 47/56/96, employer, minus 47.91
online) and the six numbers are directly comparable.

**Verdict: the inference held.** No city falls below **99.71%** geolocated,
so **France genuinely has no geocoding leg in any of its six cities** and
keeps its cities-per-unit-of-work ranking. Two caveats that are now visible
only because the cities were measured separately:

- **The OSM composition validation is still Paris-only.** Geolocation is
  confirmed everywhere; that the employee filter selects the *right rows* was
  checked against OpenStreetMap in Paris alone. Cheap to repeat per city, and
  worth doing for the first non-Paris build rather than all five.
- **Rennes at 2,089 and Lille at 3,272 are thin.** Not disqualifying — Rennes
  has a two-line metro and the density question is what the map exists to
  show — but these are an order of magnitude below Paris, and whether a
  ~2,000-point city earns a page is a scope call, not a data problem.

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

## Tier 4 — all four probed 2026-09-22; **Ireland passes** (4 countries, 4 cities)

| Country | City | State after the probe |
|---|---|---|
| 🇨🇿 **Czechia** ▲ | Prague | **Still the best probe left, and both its hosts had MOVED.** `rzp.cz` is 000 but **`www.rzp.cz` redirects to `rzp.gov.cz`**, which answers; `opendata.praha.eu` redirects to **`lkod.cz/catalog/praha`**. Two successor moves nobody had followed. **`data.gov.cz/sparql` answers SPARQL** — the Bulgarian technique applies directly. Next: enumerate for *provozovny* (premises) |
| 🇮🇪 **Ireland** ▲▲ **PASSES** | Dublin | **The probe was run on 2026-09-22 and Ireland passed — Dublin is now Band A.** `valoff.ie` was not down but **RETIRED**, and `api.valoff.ie` is **NXDOMAIN**; the API had moved twice, ending at **`opendata.tailte.ie`**, named on the *Valuation API Explorer* page and found by watching that JS page load its own link. **The deciding question is answered YES: the rateable register carries 16 use categories**, including `RETAIL (SHOPS)` and `HOSPITALITY`, plus a finer `Uses` string and `FloorUse` per floor. **Ireland is not the UK** — the NNDR's missing use category was never a property of rateable registers as such. Dublin City Council: **7,207 shops, 735 hospitality, 100% carrying Irish Transverse Mercator coordinates**, CC BY 4.0, no key |
| 🇨🇭 **Switzerland** ✗ | Zurich | **The second bucket is MEASURED ABSENT.** Control passes (`zzqqxxnonsense` → 0). Every commerce term returns noise or surveys: `detailhandel` **1** (a traffic count), `verkauf` 12 (tram ticket offices, apartment prices), `laden` 31 (a farm shop, population surveys), `gewerbe` 28 (zoning land, 3D roof models), `firmen` 16 — all **Firmenbefragung**, company *surveys* 2005–2025. Only `Gastwirtschaftsbetriebe` is real. **Zurich is a one-bucket food city — the Stockholm shape**, and it inherits Stockholm's open scope question rather than a data one |
| 🇸🇬 **Singapore** ⚠️ | Singapore | **The recorded description understated it: the search is not loose, it is INERT.** `zzqqxxnonsense` returns the **identical 10 datasets** as `licence`, `food establishment` and `business` — the query parameter is ignored entirely, and only the nonsense control tells that apart from a loose search. The catalogue is **4,628 datasets over 463 pages** and does page properly, so the route is **enumeration, not search** — the Montréal lesson, forced. Not yet done |

**Three of today's four probes hit the same thing: a host that had moved.**
`rzp.cz` → `rzp.gov.cz`, `opendata.praha.eu` → `lkod.cz`, `valoff.ie` →
`tailte.ie` — on top of Sevilla's `datosabiertos.sevilla.org` → an ArcGIS org.
**A 000 or a 404 is a question about the address, not an answer about the
data**, and this project has now spent retries on four corpses in one day.

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

## Tier 6 — reached; one promoted out, two closed, two left (4 countries, 4 cities)

Reached 2026-09-22; what each host actually does is recorded in Band D-c
above. **Bulgaria has since become a data finding** — enumerated around its
403 via the EU portal — so the "no finding either way" caveat now covers only
Estonia and Croatia.

| Country | City | Host state |
|---|---|---|
| 🇪🇪 **Estonia** | Tallinn | API found (`andmed.eesti.ee/api/datasets/search`), contract unpinned — **400** on empty `search` and on `limit=1000`. **MTR** is the likely real route, unprobed |
| 🇭🇷 **Croatia** | Zagreb | `data.gov.hr` — **identical 1,291-byte SPA shell** at four paths incl. `data.json` |
| 🇭🇺 **Hungary** ✗ **CLOSED** | Budapest | **Firm negative on both routes.** Portal: `kozadat.hu` is a search tool over data inventories. Food authority: FELIR is CAPTCHA-gated and lookup-only; approved-establishment lists are PDFs of processing plants |
| 🇧🇬 **Bulgaria** ✗ **CLOSED** | Sofia | **Firm negative, reached around the 403.** `data.europa.eu`'s SPARQL endpoint harvests `data.egov.bg`; **11,635** Bulgarian datasets enumerated from outside. **141** municipal premises registers exist — none of them Sofia's **76**. Bulgaria's registers are all small towns; Sofia is its only metro city |

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

### 🇪🇸 Spain is a TWO-city country — measured 2026-09-22

Spain had been carried as *"2 now, 6 total"* on the reasoning that it licenses
bespoke per city and **two of the three cities probed had a premises census**,
which *"raises the prior sharply"*. That prior is now measured, and it was
wrong: **Madrid and Barcelona are the exceptions, not the rule.**

| City | Portal | Enumerated | Verdict |
|---|---|---|---|
| **Valencia** | `opendata.vlci.valencia.es` (CKAN) | **290 packages** | ✗ The only commercial-adjacent names are container locations, noise stations, and *zones d'activitats* — **zoning polygons, not businesses** |
| **Málaga** | `datosabiertos.malaga.eu` (CKAN) | **1,377 packages** | ✗ `empresas-y-sectores` is explicitly businesses **in business parks**; `centros-comerciales` and `mercados` are `equipamientos` facility layers. CC **BY-SA** |
| **Bilbao** | own portal + `datos.gob.es` | 344 own / **600 federated** | ✗ Entire commercial holding is **"Barómetro del comercio minorista"** — retail-trade survey aggregates by employment stratum, sector, territory |
| **Sevilla** | ArcGIS org `hcmP7kr0Cx3AcTJk` | **1,260 items / 413 Feature Services** | ✗ **Measured negative** (was "unreachable" — the Hub's sign-in wall hid nothing; `sharing/rest` is public). `Locales` is **150 vacant municipally-owned units**, not businesses. Rail *is* solved: `METRO_Estacion` 21, `METRO_Linea` 20 |

**A method note worth carrying.** Bilbao's own portal holds 344 datasets across
35 pages and offers **no search** — its only form control is a sort order. Paging
it 35 times would have been the obvious move and the wrong one. Spain federates
every municipal portal into **`datos.gob.es`**, which speaks DCAT over a
documented API, so one publisher enumeration (`/catalog/dataset/publisher/<id>`)
covers any Spanish city at once. That is the primitive to reach for next time a
Spanish city comes up.

**And a caution about the national catalogue**: searching it by *title* returns
almost entirely **INE** (publisher `EA0042823`) aggregate statistical tables —
*Locales por provincia y condición jurídica*, hotel occupancy, and so on. Those
look like premises data and are not. Enumerate by **publisher**, not by title.

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

   > **⚠️ SUPERSEDED 2026-09-22 — the pointers were followed, and the conflict
   > mostly dissolves.** The paragraph above jumped to step 8 ("ask the
   > publisher") while steps 2, 3 and 5 were still undone: it treated a
   > **harvester's** metadata field as the last word and never opened the
   > documents that record names. What reading found:
   >
   > | Source | Says | Weight |
   > |---|---|---|
   > | `dataportal.se` (the **harvester**) | `accessRights: RESTRICTED`; `license:` the category **`otherlicense`**, not a licence | weakest — a third-party catalogue |
   > | **Miljöförvaltningen's own Hub DCAT feed** — `open-data-sthlm-miljo.hub.arcgis.com/api/feed/dcat-us/1.1.json`, **109 datasets** | **`accessLevel: public` on all 109**; `license` **CC0 on 8**, blank on 101 incl. this one | **strongest — the publisher asserting** |
   > | ArcGIS item `8447f7af…` | `access: public`; **no `licenseInfo` field at all** | publisher |
   > | FeatureServer root | `copyrightText: "Stockholms stad, miljöförvaltningen"`; `licenseInfo` empty | publisher |
   > | `dataportalen.stockholm.se` deep link | redirects to **`catalog.signin`** — walled, and this project does not create accounts | unread |
   >
   > **`read-licence` step 5 decides the contradiction: the publisher outranks
   > the catalogue**, and the publisher says *public* on all 109 datasets.
   > That the publisher **declares CC0 on 8 of them** matters too — it shows
   > the licence field is one they use and chose not to fill here, so the
   > blank is a genuine silence rather than a missing capability. Those 8 are
   > a single thematic cluster (ArtArken, biotopes, substrates, landscape),
   > which reads as one team licensing its own outputs.
   >
   > **One tempting over-reach, declined.** Stockholm's traffic office states
   > at `openstreetgs.stockholm.se`: *"Datainnehåll i dessa tjänster får
   > vidareutnyttjas fritt och tillhandahållas **'Licensfritt'** om inget
   > annat anges"* — freely reusable, licence-free unless otherwise stated.
   > **That is Trafikkontoret's statement about *dessa tjänster*, its own
   > services — not miljöförvaltningen's**, and extending one department's
   > terms to another's data is exactly the move this skill exists to stop.
   > It is evidence about the city's posture, not a licence for this dataset.
   >
   > **Position now: SILENT, not restricted** — the Miami-Dade shape, where
   > the authoritative pages were read and impose no reuse position. Still
   > genuinely unread: the **walled GeoNetwork record** (try the Internet
   > Archive, as Barcelona's and Sevilla's were read) and any city-wide open
   > data policy page. **A letter is no longer the next step, and never was
   > the first one.**

**A second Swedish city worth noting:** `dataportal.se` shows **Göteborgs
stad** publishing *both* `Livsmedelsverksamheter` ("alla aktiva
livsmedelsverksamheter", JSON + CSV) and `Restauranger med serveringstillstånd`
(CSV) — i.e. **two** food-adjacent registers where Stockholm has one, and
`Livsmedelsverksamheter` is a register of *businesses* rather than of
inspections, so it needs no dedupe. Gothenburg's rail is trams rather than a
metro, so it is a weaker map for a stronger dataset. Unprobed.

## The summary box's dated moves, to 2026-10-04

**Moved word for word from the summary box of `city_master_list.md` ("Current state — 2026-10-03") on 2026-10-04,** when its counts became generated (`scripts/check_master_list_counts.py --write`, the first change of `docs/efficiency_review_2026-10-04.md`). Two branches appending to these notes conflicted on every build merge. **Closed:** a later move goes to the session's decisions draft and `DECISIONS.md`, not here.

- **Built** *(Belgium's six, the new-cities build's three and the Korea sweep's three (Daejeon, Gwangju and Gimhae) built 2026-10-04; each city's build line is in the Built table below, and the dated moves in the archived list)*
- **Candidates** *(Gaziantep from C to D 2026-10-04 (owner): its data's origin unresolved, a question to the publisher; Daejeon, Gwangju and Gimhae built 2026-10-04; Belgium's six to Built 2026-10-04; Liverpool (Regional) built 2026-10-04, from B, and Tacoma and Mendoza from A (the new-cities build); the paused wave's answers, 2026-10-04 (owner): Thessaloniki to B; Macau, Quito, Cuenca and Gaziantep to C; the probe wave, 2026-10-04 (owner): Gimpo, Siheung and Geneva to A, Yangsan and Gyeongsan to C, Timișoara, Iași and Cluj-Napoca to D; Brussels (Regional) from D to C, then B, 2026-10-03: the owner's KBO file and a measured storefront filter; the coverage sweep's first group, banded 2026-10-03 (owner): Daejeon, Gwangju and Gimhae from R, Mendoza, the City of Brussels and Tacoma to A; Liverpool (Regional), Antwerp, Ghent, Charleroi and Liège to B; Brussels (Regional) to D, then C, then B; Band R counted apart from 2026-10-02 (owner); Japan wave 2 briefed 2026-10-02: 15 added, Wakayama discarded, Chiba to R (owner); Arlington (VA) to R 2026-10-02 as D.C.'s add-on, Richmond's precedent (owner); rebuilt 2026-10-01 from the post-review screens; R carried over with four new rows: Kraków, Brescia, Catania and Alicante, whose portals refuse this machine and a browser; Takaoka from Band C 2026-10-02, its list now unreachable (owner))*
- **Restricted (Band R)** *(Jerusalem, Almaty, Astana, Ahmedabad and Lahore to R 2026-10-04; Norrköping to R 2026-10-04, request only; Daejeon, Gwangju and Gimhae to A 2026-10-03, on SEMAS's keyless file; a band, not candidates (owner, 2026-10-02: "keep it as a Band but exclude it from the candidate counts"): each needs access the project does not use, or a request only the owner sends)*
- **Discarded** *(12 more 2026-10-04 from the paused wave; 21 added 2026-10-04 from the probe wave; Wakayama 2026-10-02, opt-in coverage; 100 carried over; 19 added 2026-10-01 from the post-review screens, confirmed by the owner the same day; Tempe from Band D the same day, no address in its list (owner); Brisbane from Band C the same day, commuter rail only (owner))*
