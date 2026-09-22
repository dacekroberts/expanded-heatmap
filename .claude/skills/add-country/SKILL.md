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

Each one can end the profile.

**Which one is cheapest depends on the region, so choose the order rather than
inheriting it.** In Canada, rail-first removed 6 of 13 cities for the cost of
reading `routes.txt`. In Europe and East Asia it removes almost nothing,
because every candidate city has rail - there, **question 2 is the cheapest
disqualifier and should run first**, and rail becomes a confirmation step. The
2026-09-21 global screen ran rail first out of habit and wasted the step.

## Evidence discipline - three rules that cost a day to learn

**Build the exhaustive base before filtering.** Start from the full universe -
the 2026-09-21 screen began with every country in the Mobility Database
catalogue, 87 of them - so a candidate can be **ruled out but never missed by
omission**. Istanbul, Sofia, Bucharest and Santiago all surfaced that way, and
none was on the original Europe-and-East-Asia guess the screen started from.

**A negative from one method is not a finding.** Positives are cheap to trust;
a negative silently ends a line of inquiry, so it earns a second,
differently-shaped probe before it is recorded. Re-testing the ruled-out group
by **operator name across the whole catalogue with no country filter** - a
different method from the country-then-guess passes - found Tokyo's Toei feed
and Buenos Aires' SUBTE, both missed the first time. Mark a negative
**ASSERTED** until two methods agree.

**A pattern justifies deprioritising, never ruling out.** Germany, Italy,
Sweden and Portugal were put in the "ruled out" tier as EU company registers -
asserted from the regional pattern, **never probed for any of them** - while
Berlin, Naples, Stockholm and Lisbon were simultaneously being rail-confirmed
into the tier above. They sat in two tiers at once, and it was caught only by
rebuilding the table by hand. If a country has not been probed, it stays in
the running with an ASSERTED label on it.

**The FIRST record an API returns is not a random one, and n=1 is not a
measurement.** Finland was ruled out on a single record - the first the PRH
API returned, a financial holding company with an empty street, a PO box and a
`c/o` accounting firm. Measured across 500 companies instead, **89.8% carry a
real street address**, and the visiting-address type is populated on 100% of
the records that have one. The stated reason for ruling out a whole country
was false.

Registers are ordered by identifier or registration date, so the first page is
systematically the **oldest** entities - holding companies, dormant shells,
long-established corporates. It is the least representative sample available.
**Pull several pages and count.** The cost is one loop.

**Send a nonsense search term before you believe any result list - or any
zero.** A server that ignores your search parameter returns HTTP 200 and a
full, plausible page of results, and nothing in the response says the filter
was dropped. `data.seoul.go.kr` ignored both `GET ?srchDetailWord=` and
`POST searchKeyword=`: a real hygiene term and the term `zzzzqqq` returned
**byte-identical** pages, and the ten datasets on them looked like hygiene
results because the catalogue's default ordering happens to surface hygiene
datasets. The conclusion drawn from it - "only one dataset has a downloadable
file" - was wrong, and the correct answer (a keyless CSV export covering 3,063
datasets) was two facets away. Cost: one extra request per endpoint.

Corollary: **prefer the site's own facet counts to your own sampling.** Seoul's
`제공유형 SHEET (182) OPENAPI (180) LINK (71) CHART (27)`, with no FILE row,
settled in one read what paging through 251 results would not - it is the
publisher's count over the whole result set, not an inference from page one.

### 1. Does urban rail exist, in DATA YOU CAN READ - which is not the same as a GTFS feed

**Read this before touching the Mobility Database.** The 2026-09-21 global
screen got this backwards and had to be corrected.

**This project uses no timetables.** It needs **station coordinates and line
geometry**. GTFS carries those, but so does any national railway GIS layer,
and national mapping agencies publish those routinely - national coverage,
better quality, clearer licence.

Japan is the proof. The Mobility Database holds **18 Japanese feeds, almost
all volunteer-run village buses, and no JR at all**. MLIT's National Land
Numerical Information `N02` layer holds **10,235 stations and 21,932 line
segments across 178 operators**, every JR company included, shapefile *and*
GeoJSON, Shift-JIS *and* UTF-8, under PDL 1.0 with commercial use permitted.
Same country, opposite answers, because the wrong source was asked.

**Probe in this order. The catalogue is LAST.**

1. **The national mapping or statistics agency's railway layer** - MLIT in
   Japan, and its equivalent elsewhere. **Ask TWO questions of it, not one:**
   does it carry **station points with coordinates**, and does it carry **line
   geometry**? This project draws and labels every transit line, so stations
   alone are not enough. Japan's N02 has both - 10,235 stations and 21,932
   line segments. Korea's station standard dataset has **1,099 stations with
   WGS84 coordinates and no lines at all**, which passes the first question and
   fails the second. A screen that asks only about stations records a false
   pass.
2. **The national open-data portal's transit standard datasets** - Korea
   publishes nationwide urban-railway *station* and *line* standard datasets.
3. **The agency's own GTFS**, where one is published.
4. **The Mobility Database catalogue** - a mirror of a mirror, demonstrably
   stale and incomplete. Useful for breadth, not for a verdict.

Commuter rail is not urban rail here, matching every built city: basic
`route_type 2`, and extended `109` (Suburban Railway, the S-Bahn family).

**Rail-first is right for a country already known to publish transit data,
and wrong as a global filter.** In Canada it removed 6 of 13 cities before a
catalogue was opened. Across Europe and East Asia it removes almost nothing,
because every candidate city has rail - so the business-data question does the
work instead, and should run first.

#### Four ways this step returns a confident wrong answer

All four happened in one day.

- **Extended route types.** An agency may publish only the TPEG-derived 3- and
  4-digit set, where a metro is `401`, an underground `402`, a tram `900`.
  Reading only basic 0-12 reported **Berlin, Hamburg, Stockholm and Oslo as
  having no urban rail**. `screen_rail.py` handles both sets now.
- **Wrong-feed selection.** Picking "a feed that names the city" is not
  picking the rail operator. Barcelona and Madrid were tested against bus
  companies, Dublin against airport coaches, Malaysia against a bus operator
  in Kuala Terengganu. In a country with 169 feeds that is close to random -
  **search by operator name across the whole catalogue, with no country
  filter**, which is also how two feeds missed by country-filtered passes were
  found.
- **A national portal that is unreachable.** Before writing that down, work
  through all four causes, because three of the four have bitten:
  1. **A transient outage.** `data.go.kr` timed out from two independent
     networks and answered 200 an hour later. Retry before recording.
  2. **The wrong hostname.** `datosabiertos.gob.pe` fails; **`www.`
     datosabiertos.gob.pe answers**. Peru was nearly written off over a vhost.
     **Always try `www.`**
  3. **A refusal, which is TWO different things - read the block page.**
     - **Client-signature refusal:** a bare `requests` user agent is rejected
       where a real browser is not. Chicago's data terms do this. **Use the
       browser**, as `read-licence` says.
     - **IP-level refusal:** the block page **names your IP address** or shows
       a WAF request ID. **The browser is useless** - it shares the address.
       Tested 2026-09-21: `data.go.th` and `opendata.tel-aviv.gov.il` both
       refused the browser pane and printed `50.47.238.226` back, the same IP,
       one with a Cloudflare Ray ID and one as `Status Code: 472`. The trigger
       is a **different network or region**, plausibly in-country.

     This distinction was got wrong first: "bot-protected, so try the browser"
     was carried over from the licence workflow without testing it, and a
     country was kept warm on a false rationale. **If the block page prints
     your IP, the client is not the problem.**
  4. **A genuinely dead host.** Only after the first three. And note whether it
     is one host or a **whole domain**: every `*.cdmx.gob.mx` host times out,
     which is a more durable finding than one portal being down.

  **Then try the CITY's own portal, which is the scope this project works at
  anyway.** This has now paid off three times - Mexico via Guadalajara, Korea
  via `data.seoul.go.kr`, and Israel, whose national portal carries a business
  register for Be'er Sheva, a city with no rail, while Tel Aviv publishes its
  own. **A national portal is the wrong default for a city-scoped project.**
- **A feed that exists and is broken.** Buenos Aires' SUBTE feed is published
  on the city's own CDN and contains no `routes.txt`; Melbourne's PTV feed is
  a nested zip; Dubai's catalogue entry is an anonymous personal GitLab job
  artefact. Absent and broken are different findings.
- **A download button that delegates to another portal.** Check where the file
  actually lives before concluding a city portal publishes it. Busan's and
  Daegu's FILE buttons both point at
  `www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=…&fileDetailSn=…`, so
  neither city hosts its own data. Two consequences, both measured 2026-09-22:
  - **The delegated id goes stale silently.** Daegu's resolved correctly.
    Busan's returned **0 bytes** at `fileDetailSn` 1 and 2, an unrelated
    **PNG** at 3 and a **JPEG** at 4 - a wordmark image from some other
    dataset. `Content-Disposition` named the PNG honestly; had the header been
    trusted instead of the magic bytes, the file would have been recorded as
    downloaded. **Check magic bytes, not the filename the server claims.**
  - **A CAPTCHA on the download path disqualifies the source**, however open
    the licence. `data.go.kr` routes downloads through
    `/cmm/cmm/check-limit.json` → `needCaptcha` → `showLimitCaptcha`, a rate
    limiter. This project does not defeat CAPTCHAs, so a source needing one
    download per district per refresh is not a pipeline - record it as closed
    and say why.

### 2. Does the country record WHERE COMMERCE HAPPENS, or only where companies are REGISTERED?

The biggest structural discriminator, and the sharp form of the question. An
earlier version of this skill asked "does the country license businesses
*municipally*", which is Canada's framing and mis-sorts half the world:
municipal-vs-national turns out to be an unreliable *proxy* for the question
that actually decides things.

A **company register** publishes a **registered office** - frequently an
accountant's address or a holding company's mailbox. Mapping those produces a
map of bookkeepers. Companies House, Australia's ABN, Japan's corporate-number
system and most of the EU's registers are this, and they fail here however
open they are.

Four shapes qualify. Sort a candidate into one before going further:

| Shape | Examples | Notes |
|---|---|---|
| **Municipal licence register** | US, Canada, **South Korea** (195 permit types) | The shape this project is built for |
| **National establishment register** | **France** SIRET, **Mexico** DENUE, **Norway** `beliggenhetsadresse` | One source covering every city - see the caveat below |
| **Premises field survey** | Montréal `locaux-commerciaux`, **Barcelona** `cens de locals` | Records what is on the street rather than who registered; arguably the best answer to this project's premise |
| **Sector inspection register** | UK FSA food hygiene | **One bucket only** - Boston's shape, and a ceiling not a floor |

**Look for the field name that proves it.** Norway's register keeps
`beliggenhetsadresse` (location address) deliberately distinct from the
registered business address; that distinction *is* the answer. France's
`établissement` is not the same object as its `unité légale`.

**The caveat on national registers.** One source covering every city is a
different and possibly better shape, but it is **not** the shape this project
is built for: scoping and taxonomy were both designed around per-city
municipal registers, and a national register includes every office, depot and
administrative site alongside the shopfronts. That is a design decision to take
before a profile, not a fact to discover during one.

#### Measure COMPOSITION, not just presence - most registers are mostly not shops

"Does it have addresses" is the easy half and rarely the deciding one. The
deciding question is **what the register is actually made of**, and the answer
is reliably worse than the dataset title suggests:

| Register | Share that is NOT a storefront |
|---|---|
| **Philadelphia** L&I | **79%** landlord registrations |
| **Washington D.C.** | **61%** residential rentals, plus 11,074 `General Business` office catch-all |
| **Finland** PRH, Helsinki | **53%** NACE 68 real estate - every apartment building is a *Kiinteistö Oy* or *Asunto Oy* |
| **Vancouver** | 10,698 Long-term Rental, 3,910 Short-term Rental Operator, 3,575 General Contractor |
| **Toronto** | Taxicab Owner 4,212, Public Garage 3,023, Building Renovator 1,461 |

This is a **family, not a series of one-offs**: a business register records who
*registered*, and in most countries that is dominated by property-holding
entities and non-premises trades. The project already filters all of these by
category, successfully - so a high share is a cost, not a disqualifier.

**The three numbers to produce for any candidate register**, from several
pages rather than one:

1. **Address presence rate** - what fraction carry a real street, not a PO box
   or a `c/o`.
2. **Category composition, top 10-12** - what the register is mostly made of.
3. **The share in the project's three buckets** - retail, food service,
   personal services. Finland's retail is **4.8%**, and food and beverage and
   personal services do not reach its top twelve. That is the number that
   decides whether a country is worth a profile.

**And then the question that composition does NOT answer:** once filtered to
the storefront categories, are those rows **shop premises or head offices**? A
company register can pass all three tests above and still map one pin per
chain rather than one per shop. That needs its own probe.

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
- **NORMALISE DASHES, APOSTROPHES AND UNICODE FORM BEFORE ANY JOIN.** This has
  already cost time once: Montréal's commercial survey writes
  `Ahuntsic–Cartierville` with an EN DASH where the City's own boundary layer
  uses a hyphen, across six borough names, which made a 34-feature layer look
  like it covered 32. Same class: `L’Île` (U+2019) against `L'Île` (U+0027),
  and `Baie-d'Urfé` against `Baie-D'Urfé`. Map U+2013/U+2014 to U+002D,
  U+2018/U+2019 to U+0027, apply **NFC**, and compare with `casefold()` rather
  than `.upper()`. Two files can look identical on screen and fail to match.
- **Check whether the feed ships `translations.txt`** before transliterating a
  non-Latin name by hand - TransLink's and STM's both do.
- **Column names in another language are already solved** - each city's config
  names its own columns and step 2 renames to the taxonomy's `VALUE_COLUMN`.
  `NOM_ETAB` is no harder than `dbaname`.
- **Category labels belong to the taxonomy module**, which the project's own
  invariant already makes the single owner of tooltip and legend text. Decide
  there whether to translate; prefer English bucket labels with the source
  value in the tooltip, so cross-city comparison survives without hiding the
  source.
- **Business names stay in their own language, always.**
- **NORMALISE FOR JOIN KEYS, NEVER FOR DISPLAY.** The stdlib does all of this;
  no package is needed, which matters because `requirements.txt` has to stay
  lean for Streamlit Cloud.
  - `unicodedata.normalize("NFKC", s)` fixes the **full-width numerals** in
    Taiwanese addresses - `濱海一路２３號１樓` becomes `濱海一路23號1樓`, which
    is the difference between a geocode match and a miss. It also folds
    Japanese half-width katakana (`ﾏｸﾄﾞﾅﾙﾄﾞ` to `マクドナルド`) and leaves
    Korean untouched.
  - Accent folding for a join key is NFD plus a combining-mark filter:
    `"".join(c for c in normalize("NFD", s) if not combining(c))` turns
    `Montréal` into `Montreal`, `Plzeň` into `Plzen`, `Rīgas` into `Rigas`.
  - **THE TRAP: NFKC CHANGES DISPLAY TEXT.** `Ⅳ号店` becomes `IV号店`,
    `㈱丸井` becomes `(株)丸井`, `Ｃａｆｅ` becomes `Cafe`. Every one of those
    is a shop's actual name being quietly rewritten. Normalise a *copy* used
    for matching and keep the original for the tooltip - which is the rule
    above, stated mechanically.

- **The map's font stack is in `pipeline/theme.py` as `FONT_STACK`, and it
  matters for non-Latin names.** A bare `sans-serif` lets the browser choose:
  missing glyphs render as tofu boxes, and a substituted face changes line
  metrics so a tooltip outgrows its box. The order is deliberate - browsers
  fall through **per glyph**, so Latin/Greek/Cyrillic faces come first and CJK
  after, because Segoe UI and Noto Sans carry no CJK glyphs and a Japanese
  name therefore falls past them to Yu Gothic or Hiragino. Putting a CJK face
  first would restyle every Latin name on every map.
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

## Rank ALSO on cost per marginal city - it decides how far a budget goes

Station density (below) measures **value per city**. This measures **cost per
additional city**, and the two are independent. A fixed research budget goes
several times further in a country where the second city is nearly free.

**Ask: is the business data NATIONAL, STANDARDISED, or BESPOKE per city?**

| Shape | Marginal city costs | Examples |
|---|---|---|
| **One national register** | A boundary file and a rail check. The data is already downloaded | **France** SIRENE · **Korea** `상가(상권)정보` · **Mexico** DENUE · **Taiwan** 商業登記 · **Brazil** CNPJ |
| **National STANDARD schema, per-municipality publication** | A download per city, but **identical columns**, so one parser serves all | **Japan** 推奨データセット · **Korea** 표준데이터 |
| **Bespoke per city** | A full integration each time | **US** · **Canada** · **Spain** · **Italy** |

**The 2026-09-21 screen got this wrong by omission**, and it distorted the
ranking. Each country was assessed as though it were one city - France as
"Paris", Korea as "Seoul", Mexico as "Guadalajara", Taiwan as "Taipei". In
fact:

| Country | Metro cities reachable from the SAME source |
|---|---|
| **Japan** | ~9 - Tokyo, Osaka, Nagoya, Yokohama, Kobe, Kyoto, Fukuoka, Sapporo, Sendai |
| **France** | 6+ - Paris, Lyon, Marseille, Lille, Toulouse, Rennes |
| **Korea** | ~~6~~ **1 - Seoul only.** Corrected 2026-09-22, see below |
| **Brazil** | 6+ - São Paulo, Rio, Belo Horizonte, Brasília, Recife, Porto Alegre |
| **Taiwan** | 4 - Taipei, Kaohsiung, Taichung, Taoyuan |
| **Mexico** | 3 - CDMX, Guadalajara, Monterrey |

**Canada is the worked counter-example and explains its cost.** Six cities
needed **four different portal types** - Toronto CKAN, Vancouver Opendatasoft,
Calgary and Edmonton Socrata, Surrey ArcGIS Hub, Montréal CKAN - so six cities
meant six integrations. That is why the Canadian screen cost a day, and it is
not a fact about Canada's data quality.

**Ask WHICH TIER OF GOVERNMENT LICENSES, not which one publishes - and check
one non-capital city before believing a country count.** Korea's "6 cities from
one source" was the single largest error in the 2026-09-21 screen, and it
survived because only Seoul was probed. In Korea the licensing authority is the
**district** (자치구/군), so the register is published per district, in whatever
schema and on whatever schedule that district chose:

| | Districts publishing a usable premises register |
|---|---|
| **Seoul** | **25 of 25** - the city aggregates. Verified: 강남구 4,744 → 도봉구 794 |
| **Busan** | **4 of 16.** Others are single-sector (식품소분업 only) or *enforcement actions*, which is a violations list, not a register |
| **Daegu** | **4 of 9** - and the missing one is **중구, the downtown**, where all three metro lines converge |

So **the capital was the exception and was mistaken for the rule.** A single
aggregating city says nothing about the other five. The generalisable check:
**probe the second city, and probe its central district specifically** - a
country count built from the capital alone is a guess wearing a number. Partial
district coverage is also not a partial city: a commercial-density map missing
the downtown is not a map of that city, however good the other districts are.

**The consequence for ordering:** where two countries are otherwise close,
**prefer the national-register one.** On this axis **Korea outranks Spain** -
Spain's six metro cities are six separate integrations, Korea's six are one
download plus six boundary files - even though Spain's per-city data is
excellent.

**And check this BEFORE the station-density ranking**, because it changes what
you are ranking: a country's entry is a *set* of cities, not one.

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

  **But do NOT generalise that into "never use a mirror" - the 2026-09-21
  screen did, and contradicted itself within the hour.** Mexico City is the
  opposite case: `datos.cdmx.gob.mx` times out, the S3 `direct_download`
  returns 403, and **the Mobility Database mirror is the only route that
  works** - serving a current feed that screens as subway 12, the correct line
  count.

  **The distinction is whether the artifact SELF-ATTESTS, not whether it came
  from a mirror.** GTFS does: `feed_info.txt` carries `feed_end_date`, and mode
  counts are checkable against a known network, so "Toronto has a subway and
  this has zero type-1 routes" is detectable. A business-register CSV does not:
  no embedded validity date, its date living in a filename, and a short row
  count invisible - 28,000 against a true 31,000 looks fine.

  So the Toronto failure was not "a mirror was used". It was **a stale mirror
  used without reading the expiry field already in the file**, and the fix was
  the expiry check rather than abstinence.

  **The rule: a mirror is usable when the artifact self-attests to its own
  freshness and completeness; it is not when you must take the mirror's word
  for both.** And a feed has at least three addresses - the agency's,
  `urls.latest` and `urls.direct_download` - so try all of them before
  recording a city as unreachable.
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

- **Asking the wrong SOURCE, not just the wrong question.** A transit
  catalogue answers "is there a GTFS feed", which is not what this project
  needs. Japan looked feed-poor and is data-rich. Check the national mapping
  agency before believing any transit verdict - see question 1.
- **A screening tool reporting what it cannot parse as absent.** Extended
  route types cost four European capitals; a nested zip cost Melbourne; a
  `LineString` where a `Point` was expected would have cost Japan, whose
  10,235 station records are platform centrelines needing centroids.

- **Sampling the first record and calling it a measurement.** It cost Finland
  a whole-country ruling. See the evidence-discipline section.
- **Answering "are there addresses?" and skipping "what is this register made
  of?"** Presence is the easy half. Composition decides.

The single recurring cause: **asserting from a column's existence, a dataset
title, or a plausible-looking flag instead of measuring.** Five separate
conclusions in the Canada profile had to be reversed for exactly that reason.
The project's first invariant already says this; a country profile is where it
is easiest to forget, because the volume is high and each individual check
feels small.
