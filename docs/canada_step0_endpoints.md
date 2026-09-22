# Canada — Step 0 endpoints, verified live 2026-09-21

Companion to the Canada section of [`city_shortlist.md`](city_shortlist.md)
and the licence store in [`licenses/`](licenses/). **This is now the EVIDENCE
TRAIL, not the provenance record.** Six Canadian municipalities are built, as
five maps — Vancouver and Surrey together as one regional map, then Montréal,
Calgary, Toronto and Edmonton — and every endpoint they use is in
[`data_sources.md`](data_sources.md), promoted 2026-09-22 as that file's
"adding a city adds its rows here, in the same commit" rule requires.
**Where this file and `data_sources.md` disagree, `data_sources.md` wins:** it
was written from each city's own `config.py` after the build, and three
findings below did not survive it — Surrey's wrong-CRS trap turned out to
belong to the Hub's file export rather than to the service the build reads,
Calgary's real category count is 96 rather than 173, and TransLink's feed does
carry `feed_info.txt` (it is the Mobility Database mirror that does not). Read
this file for how each source was found and what was tried; read
`data_sources.md` for what a rebuild should call.

Every endpoint below was fetched, not inferred.

## Business registries

| City | Source | Endpoint | Rows | Verified |
|---|---|---|---|---|
| **Montréal** | `locaux-commerciaux` — a 2025 field survey of street-level commerce, annual since 2021 | CKAN `donnees.montreal.ca`, package `locaux-commerciaux`, CSV resource `01ded48e-f982-4703-975e-4be0769ef3ee` (`occupation-commerciale-2025.csv`) | **28,621** | `LAT`/`LONG` **100%**, `NOM_ETAB` **100%**, `SCIAN` (NAICS) **99.6%**, `VACANT_A_LOUER` flag, `USAGE1` 10 values. **Plain curl gets `RBAC: access denied`** — browser headers required |
| **Vancouver** | `business-licences` | Opendatasoft `opendata.vancouver.ca`, dataset `business-licences`, `/exports/csv` | 205,943 all years; **58,346** at `folderyear='26' AND status='Issued'` | `geo_point_2d` **50.8%**; `businesstradename` **blank on 63%** — the Los Angeles fallback trap |
| **Calgary** | `vdjc-pybd` Calgary Business Licenses | Socrata `https://data.calgary.ca/resource/vdjc-pybd.csv` | **23,203** | `point` **100%**, `tradename` **0% blank**, `licencetypes` taxonomy. `homeoccind` is `N` on every row — not a usable discriminator |
| **Edmonton** | `qhi4-bdpu` Business Licences | Socrata `https://data.edmonton.ca/resource/qhi4-bdpu.csv` | **43,672** | `latitude`/`longitude` 53.3%. **No trade-name column.** `business_address` has three placeholders: `<Home Based Business>` 14,114, `<REDACTED FOR PRIVACY>` 4,074, `<Non-Resident Business>` 2,108 |
| **Toronto** | Municipal Licensing & Standards business licences | CKAN datastore resource `169e90ba-3ae0-43dd-8b2f-919e87002f50` | **159,872** | **No coordinates at all.** `Operating Name` blank on only 0.8%; **`Client Name` is a person column** (395 surname-first forms per 32k sample) and must never be downloaded |
| **Surrey** | Surrey Business Directory — licence-derived despite the name | ArcGIS Hub item `468ff5ff67354da5be095a9bce006137`, `/csv?layers=0` | **27,082** | `x`/`y` **100%**, `BusinessCategory` 628 values, `LicenseType` splits Home Occupation 14,015 / Commercial-Industrial 13,066. Some category values contain embedded newlines |

**Surrey's download is asynchronous.** The ArcGIS Hub `/csv` endpoint returns
HTTP **202** with a JSON job status on first call and the CSV on a later one.
The 202 body usefully carries `recordCount`.

## Transit feeds

All read live from the Mobility Database catalogue (`bit.ly/catalogs-csv`) by
`scripts/screen_rail.py`. Counts are `route_type` values in each feed's own
`routes.txt`; `route_type 2` is commuter rail and is excluded, as everywhere.

| City | Agency | Mobility Database id | Urban rail found |
|---|---|---|---|
| **Montréal** | STM | 2126 | **4 subway** — the Métro lines exactly |
| **Toronto** | TTC | 2253 | **17 route_type 0** — see the warning below |
| **Vancouver** | TransLink | 1222 | **3 subway** (Expo, Millennium, Canada) + 1 commuter rail, excluded |
| **Surrey** | TransLink | 1222 | *same feed as Vancouver* — Surrey has no agency of its own |
| **Calgary** | Calgary Transit | 712 | **2 LRT** (CTrain) |
| **Edmonton** | Edmonton Transit | 714 | **3 LRT** |

STM's feed carries **no `feed_info.txt`**, and neither does TransLink's, so
neither declares a licence of its own.

### CORRECTION — "Toronto codes its subway as route_type 0" is WRONG

That claim was made during the rail screen, propagated into
`scripts/screen_rail.py`, the `add-city` skill and `docs/city_shortlist.md`,
and is **false**. Toronto codes its subway as `route_type 1`, correctly.

The cause is worse than a misreading: **the Mobility Database mirror for TTC
(`mdb 2253`) is stale and incomplete.** Its `feed_info.txt` gives
`feed_end_date 20260606` — expired three months before it was read on
2026-09-21 — and it contains **no subway at all**: 209 bus, 17 tram, 2 ferry,
zero `route_type 1`. The only subway-named entries are *shuttle buses*
("LINE 1 SHUTTLE BUS"). The 17 tram routes are the streetcars, 301–312 and
501–512.

The **official** feed, from Toronto's own CKAN package `ttc-routes-and-
schedules` (36 MB, OGL–Toronto), is a different system entirely:

| route_type | Count | What |
|---|---|---|
| **1** | **3** | Line 1 (Yonge-University), Line 2 (Bloor-Danforth), Line 4 (Sheppard) |
| **0** | **20** | 13 streetcars **plus Line 5 Eglinton and Line 6 Finch West** (LRT) |
| 3 | 213 | bus |

So Toronto is richer than the screen suggested — three subway lines *and* two
new LRT lines — and separating rail from streetcar is trivial, not the San
Francisco problem it was described as.

**The lesson for `scripts/screen_rail.py`: check `feed_end_date`.** A mirror
can be months stale and silently missing a whole mode, and the screen has no
way to tell. Prefer the agency's own feed wherever the catalogue names one.

## Station density — measured 2026-09-21

The measure that decided D.C. (40 of 98 stations, but ~173 sites each) against
Boston (71 stations, ~39 sites each). Businesses within the outermost 0.6 mi
ring, divided by in-city stations.

| City | Rail | Stations | In city | Sites/station |
|---|---|---|---|---|
| **Vancouver** | 3 SkyTrain | 53 | **20 (38%)** | **861** |
| **Surrey** | same 3 | 53 | **4** | **549** — 361 counting Commercial/Industrial only |
| **Montréal** | 4 Métro | 68 | 64 in agglomeration | **252** |
| **Edmonton** | 3 LRT | 33 | **33 (100%)** | **153** |
| **Calgary** | 2 CTrain | 83 | **83 (100%)** | **103** |
| **Toronto** | 3 subway + Lines 5/6 LRT | **234** | all (TTC is city-only) | **41 storefront** — see below |

**Four Canadian candidates beat D.C. (~173) or come close. Toronto does not:
at 41 it is Boston's twin (~39).**

Vancouver is the densest measured anywhere in this project at 861 — and its
38% in-city share, which looks alarming, is the D.C. lesson repeating: the
share is the least interesting number. Calgary is thinnest of the four at 103,
still 2.6x Boston, with 83 in-city stations to Boston's 71 — a bigger map, not
a sparser one.

### Toronto — geocoded, and it demotes the city

The geocoding pass works (below), but what it reveals changes Toronto's rank.

- 159,872 licences → **37,563 not cancelled (23.5%)**
- **Geocoded 26,828 of 37,563 — 71.4%** by exact match against the City's own
  address points, stripping only the unit suffix. No street normalisation, no
  fuzzy matching; both would raise it.
- The join doubles as the in-city filter, returning former Toronto 12,012,
  North York 5,039, Scarborough 4,860, Etobicoke 3,031, York 1,127, East York
  759.
- **234 stations** across Line 1, 2, 4 and the Line 5 Eglinton / Line 6 Finch
  West LRT.
- 12,074 geocoded licences fall in a ring; **9,579 of them are storefront**.
- **41 storefront sites per station.**

**Toronto is a two-bucket city, and retail is effectively absent.** Of 72
active licence categories, the bucket split within a ring is **Food service
7,249, Personal services 1,973, Retail 357** — retail is 3.7%. The city
licenses food, personal services and specific trades; it does not license
general retail. The largest non-storefront categories are Taxicab Owner 4,212,
Public Garage 3,023, Building Renovator 1,461, Commercial Parking Lot 1,009,
Master Plumber 969.

That is Boston's shape exactly — food-and-drink density rather than commercial
density — at Boston's density. `bodysafe` and `dinesafe` do not help: they are
inspection programmes covering the same premises, not a retail source.

**So the largest Canadian city is the weakest candidate of the six**, which is
the opposite of where the screen started and worth stating plainly before
anyone picks it on population.

### Coordinate validity — the other Step 0 gap, now closed

Presence was already measured; this is containment in each city's own
boundary, the check that caught Los Angeles' ~9% corrupt coordinates.

| City | Coordinates inside the city boundary |
|---|---|
| Calgary | **100.0%** |
| Edmonton | **100.0%** |
| Surrey | **100.0%** |
| Vancouver | **99.8%** |

No Los Angeles-style corruption anywhere.

### Trap — Surrey's boundary GeoJSON declares the WRONG CRS

`sur_b.geojson` from ArcGIS Hub reports `EPSG:4326` in its CRS field while its
coordinates are **UTM 10N metres** (503148, 5427696 — not degrees). Reprojecting
from the declared CRS silently produces a polygon millions of metres away, and
every containment test returns **zero**. It cost a full wrong run here.

Fix: `set_crs(32610, allow_override=True)`, not `to_crs`. An earlier check in
this file confirmed the layer was a polygon with the right feature count — it
never checked *where* the polygon was, which is why this survived.

Note also that the `NAME = 'SURREY'` feature measures **364.5 km²** against the
city's ~316 km², so it may include water or a broader administrative extent.
Worth eyeballing at build time; coordinate validity is 100% regardless.

## Classification fields — THREE OF SIX ARE MULTI-VALUED

Pulled in full on 2026-09-21, per Boston's lesson that a complete
`SELECT DISTINCT` finds what a top-N does not. It found something else: **the
classification column holds several categories per row in three cities, each
with a different delimiter**, so a naive `value_counts()` returns
*combinations* rather than categories.

| City | Column | Naive distinct | Delimiter | **True distinct** | ≥10 rows |
|---|---|---|---|---|---|
| **Calgary** | `licencetypes` | 1,169 | **`,\n`** (9,136 rows affected) | **173** | 111 |
| **Edmonton** | `business_licence_category` | 1,534 | **`;`** (7,444 rows) | **67** | 54 |
| **Surrey** | `BusinessCategory` | 628 | **`\n`** (4,837 rows) | **210** | 148 |
| **Vancouver** | `businesstype` | 93 | none — single-valued | 93 | 81 |
| **Toronto** | `Category` | 72 | none — single-valued | 72 | 30 |
| **Montréal** | `USAGE1` (+`SCIAN`) | 10 | none | 10 | 10 |

**A taxonomy module built on the naive counts would be nonsense** — 1,169
Calgary "categories" are mostly one-off combinations. The real figures are
tractable and in line with what the project already handles: Miami's 150
`CATGRYNAME` values, Philadelphia's 50 licence types.

Two consequences for a build:

- **Calgary's delimiter is `,\n`, not `\n`.** Splitting on the newline alone
  leaves trailing commas and splits one category into two — "RETAIL DEALER -
  PREMISES" (4,598) and "RETAIL DEALER - PREMISES," (2,918) are the same
  category. Strip the trailing comma after splitting.
- **A premises with several licence types needs a dispatch rule.** Which
  bucket wins when a row is both "Retail Dealer" and "Food Service"? This is
  Boston's `FT+RF` question and New York's cross-source dedup in a new form,
  and it has to be decided per city rather than inherited.

## Projected CRS, derived per city from longitude

Per the project invariant — derived, never copied.

| City | Longitude | Zone | EPSG |
|---|---|---|---|
| Montréal | ≈ −73.6 | UTM 18N | **32618** |
| Toronto | ≈ −79.4 | UTM 17N | **32617** |
| Calgary | ≈ −114.1 | UTM 11N | **32611** |
| Edmonton | ≈ −113.5 | UTM 12N | **32612** |
| Vancouver | ≈ −123.1 | UTM 10N | **32610** |
| Surrey | ≈ −122.8 | UTM 10N | **32610** |

## Boundary layers — the third Step 0 requirement

`add-city` Step 0 needs business data, transit **and** boundary. The first two
were verified during the screen; these close the third. **Three of the five
carry a trap that would not show up until a build failed or, worse, silently
produced a wrong map.**

| City | Layer | Endpoint | Verified |
|---|---|---|---|
| **Montréal** | Limites administratives de l'agglomération (arrondissements + villes liées) | `donnees.montreal.ca` CKAN package `limites-administratives-agglomeration`, GeoJSON resource | **34 features**, CC-BY 4.0. Native CRS **EPSG:32188** (MTM zone 8) |
| **Vancouver** | **`local-area-boundary`, dissolved** — *not* `city-boundary`, see trap 1 | `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/local-area-boundary/exports/geojson` | 22 polygons dissolving to **one** Polygon, **118.8 km²** (the city is ~115 km²). **99.84%** of Vancouver's 29,660 geocoded businesses fall inside; 47 outside |
| **Calgary** | City Boundary | `https://data.calgary.ca/resource/erra-cqp9.geojson` | 1 MultiPolygon — **but see trap 2** |
| **Surrey** | Surrey City Boundaries | ArcGIS Hub item `dbc1656bb9fb49df9c10d446dd8c8574`, GeoJSON | 10 features — **but see trap 3** |
| **Toronto** | Regional Municipal Boundary | Toronto CKAN package `regional-municipal-boundary` | **SHP only, no GeoJSON.** Its `AREA_NAME` is documented as "Name of the former municipality", so confirm whether it is the amalgamated outline or the six pre-1998 municipalities before use |
| **Edmonton** | **City of Edmonton - Corporate Boundary (current)** | `https://data.edmonton.ca/resource/qqvh-dp5m.geojson` | 1 MultiPolygon. **100.00%** of Edmonton's 23,265 geocoded businesses fall inside it, 0 outside. **Found only on the second attempt: Edmonton calls it a *corporate* boundary, so a "city boundary" search returns nothing but Forward Sortation Areas.** The same vocabulary miss that nearly lost Montréal's `locaux-commerciaux` |

### Trap 1 — Vancouver's `city-boundary` is a LINE, not an area

`city-boundary` returns a single **MultiLineString**, not a Polygon. A
point-in-polygon test against it matches nothing, silently — the same class of
problem as San Francisco's nine-county layer, which is right only once
filtered.

**Resolved 2026-09-21: use `local-area-boundary` and dissolve it.** Its 22
polygons (Downtown, Fairview, Grandview-Woodland, Kitsilano …) union to a
single Polygon — not a multipart one, so the local areas tile the city with no
gaps — covering 118.8 km² against the city's ~115 km². Verified against real
data rather than by inspection: 29,613 of 29,660 geocoded businesses fall
inside (99.84%), with 47 outside, a plausible edge/waterfront residue worth
looking at during a build rather than assuming away.

**The area check is the part that matters.** A dissolve that silently dropped
a local area would still return a perfectly valid Polygon; only the km² and the
containment rate catch that.

### Trap 2 — Calgary publishes two datasets called "City Boundary", one broken

A Socrata search returns both `7t9h-2z9s` and `erra-cqp9`. **`7t9h-2z9s`
returns a single feature with `"geometry": null`** — 184 bytes, valid GeoJSON,
completely useless, and it fails only when you try to use the geometry.
**Use `erra-cqp9`**, which returns a real MultiPolygon.

### Trap 3 — Surrey's layer is mostly town centres

10 features, of which **9 are town centres** (Grandview, Clayton, Cloverdale,
South Surrey, City Centre, Fleetwood, Guildford, Whalley, Newton) and **1 is
the city**. Filter to `NAME = 'SURREY'` (equivalently `BOUNDARY_TYPE = 2`).
Dissolving all ten would also work but is fragile if the town-centre set
changes.

## Montréal's scope decision, now quantified

`locaux-commerciaux` covers the **agglomeration**, not the city. The boundary
layer splits cleanly: **19 arrondissements** (which together are the Ville de
Montréal) and **15 villes liées** (separate municipalities on the island —
Westmount, Mont-Royal, Pointe-Claire, Dorval, Côte-Saint-Luc, Beaconsfield,
Senneville and the rest).

Joined on 2026-09-21 in EPSG:32188:

| Scope | Premises | Occupied only |
|---|---|---|
| **Ville de Montréal** (19 arrondissements) | **25,794** | 25,131 |
| **Villes liées** (15, of which 13 have premises) | **2,827** | 2,778 |
| **Agglomeration** (all 34) | **28,621** | 27,909 |

So the linked cities are **9.9%** of the data. The decision is real but not
large: city scope loses a tenth of the premises, and the largest losses are
Pointe-Claire (586), Dollard-des-Ormeaux (415), Mont-Royal (413) and Westmount
(405).

**Both patterns already exist in this project**, so either is defensible:
Miami was built deliberately regional (13 of 42 stations outside the City of
Miami), while every other city is scoped to its own boundary. The cleanest
argument for the agglomeration here is that the STM Métro serves Westmount and
Mont-Royal directly, and a city-scoped map would draw stations whose
surrounding commerce is filtered out — the failure mode the boundary filter
exists to prevent, inverted.

### Where the Métro stations actually fall — measured 2026-09-21

68 parent stations across the four lines (Verte, Orange, Jaune, Bleue):

| | Stations |
|---|---|
| **Arrondissements** (Ville de Montréal) | **63** |
| **Villes liées** | **1** — Acadie, in Mont-Royal |
| **Outside the agglomeration entirely** | **4** — Cartier, De la Concorde and Montmorency (Laval), Longueuil–U. de Sherbrooke |

**On the station side the scope decision is worth exactly one station.** An
argument made earlier in the screen — that the Métro "serves Westmount and
Mont-Royal directly", so city scope would strand stations whose commerce was
filtered away — is **wrong on its facts**. Westmount has no Métro station at
all, and Mont-Royal has one.

The 4 off-island stations are excluded under *either* scope, since neither the
city nor the agglomeration includes Laval or Longueuil. The three Laval
stations are the Orange Line's northern terminus and would be a separate
regional question, of the kind Miami settled affirmatively.

### But the business side says the opposite, and it is the number that matters

Buffering every in-agglomeration station by the outermost ring (0.6 mi = 966 m,
EPSG:32618) and testing the premises against it:

| Scope | Premises in a ring | Premises outside every ring |
|---|---|---|
| Arrondissements | 15,460 | 10,334 |
| **Villes liées** | **659** | 2,168 |

**659 of the 2,827 linked-city premises (23.3%) sit inside a ring drawn around
Montréal's own stations** — Westmount 399, Mont-Royal 214, Côte-Saint-Luc 46.
That is 4.1% of all in-ring premises.

So the original instinct was right and its mechanism was wrong. The failure is
not that stations sit outside the city; it is that **commerce immediately
across the city line sits inside rings drawn from stations inside it**.
Westmount's commercial strips are a few hundred metres from Atwater, Vendôme
and Guy-Concordia, and city scope would cut a visible hole in the map beside
three downtown stations while keeping the stations themselves.

**Recommendation: build Montréal at agglomeration scope**, for that reason
rather than the one first given. Miami is the precedent, and the cost is
honest — the page has to say it maps the agglomeration, not the city. A
project-owner decision; record it in `DECISIONS.md` when made.

## Geocoding — only ONE city actually needs it

Measured 2026-09-21, after two wrong statements were made earlier in the screen
and are corrected here. The Step 0 rule that matters: a coordinate column
existing is not a coordinate column populated, and a row *missing* coordinates
is not automatically a row that *needs geocoding* — it may have no address at
all, in which case nothing can recover it and nothing needs to.

| City | Coordinates present | Real address but NO coordinates | Needs geocoding? |
|---|---|---|---|
| **Montréal** | 100% | 0 | No |
| **Surrey** | 100% | 0 | No |
| **Calgary** | **100%** (23,203 of 23,203) | 0 | No |
| **Edmonton** | 53.3% | **111** (0.25%) | Effectively no |
| **Vancouver** | 50.8% | **1,583** (2.7%) | Marginal |
| **Toronto** | **0%** | 159,872 | **Yes — the only real case** |

**Correction 1 — Edmonton does not need a geocoder.** An earlier claim that it
"needs geocoding for roughly 47% of its rows" was wrong. Its `business_address`
carries **three placeholder values**, not one:

- `<Home Based Business>` — 14,114 (32.3%)
- `<REDACTED FOR PRIVACY>` — 4,074 (9.3%), the City redacting addresses itself
- `<Non-Resident Business>` — 2,108 (4.8%)

23,349 rows (53.5%) carry a real street address, and **23,265 of those already
have coordinates**. Only **111 rows** have an address and no coordinates.

`<REDACTED FOR PRIVACY>` is worth noting on its own: Edmonton does part of this
project's privacy work at source, on 9.3% of rows.

**Correction 2 — Vancouver does not meaningfully need one either.** Of 58,346
current-year Issued licences, 27,103 have **neither** coordinates nor a
house-and-street address, and they are overwhelmingly categories this project
excludes anyway: Long-term Rental 10,698, Short-term Rental Operator 3,910,
General Contractor 3,575, Trade Contractor 1,670, Consulting 1,062. Only
**1,583 rows** have an address without coordinates.

### Toronto — resolved, and the answer is not a geocoder

Toronto has 159,872 licences and **zero** coordinates, so it is the only city
where this is load-bearing. It does not need an external geocoder, because the
City publishes its own address points:

**Address Points (Municipal) — Toronto One Address Repository**, CKAN package
`address-points-municipal-toronto-one-address-repository`, datastore resource
`0b3756af-9caf-4f0f-ac28-9c6617adede4`. **525,440 points**, CSV/GeoJSON/SHP/GPKG
in EPSG:4326 and 2952, under the same OGL–Toronto as the business data.

Tested on 2026-09-21 against 150 distinct licence addresses, normalising only
by stripping the unit suffix after the comma: **120 matched exactly (80.0%)**,
with no street-name normalisation or fuzzy matching. The matched points return
`MUNICIPALITY_NAME` of *former Toronto, Scarborough, North York, Etobicoke*, so
**the join doubles as the in-city filter** Toronto would otherwise need a
boundary layer for. Several misses are correct: `1 Bartley Bull Pky` is in
Brampton and `1 Convair Dr` in Mississauga — Toronto licenses businesses based
outside the city.

**Two gotchas, both of which produced a confidently wrong answer first:**

- **`ADDRESS_FULL` is title case** (`32 Nineteenth St`), and CKAN's `filters`
  matches exactly. Querying it uppercased returns **0 of 150**, silently.
- **The CKAN SQL endpoint 404s** on this portal. Use `datastore_search` with
  `filters`, not `datastore_search_sql`.

**Local equivalents exist for the other two**, if their small remainders are
ever worth recovering: Edmonton `Parcel Addresses` (Socrata `ut27-nrpn`, with
`house_number`, `street_name`, `latitude`, `longitude`) and Vancouver
`property-addresses` (99,744 records, `civic_number`, `std_street`,
`geo_point_2d`, OGL–Vancouver). Neither has been match-tested.

## CRS note

Montréal's own boundary layer publishes in **EPSG:32188** (MTM zone 8), the
Québec standard, not a UTM zone. This project's invariant is to derive the
projected CRS per city from longitude, which for Montréal (≈ −73.6°) gives
**EPSG:32618** (UTM 18N). Both are metre-based and either is defensible; the
invariant points at 32618, and the measurement above used the layer's native
32188 because it was a one-off join. Decide and record it at build time rather
than letting the two drift.
