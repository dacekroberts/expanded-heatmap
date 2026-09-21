# Build brief — Vancouver

**For the session taking Vancouver.** Everything Step 0 asks for is below,
measured on 2026-09-21 and sourced from
[`canada_step0_endpoints.md`](../canada_step0_endpoints.md),
[`licenses/canada-privacy-regimes-note.md`](../licenses/canada-privacy-regimes-note.md)
and [`licenses/canada-required-notices.md`](../licenses/canada-required-notices.md).
Those remain the authority; this is the operational layer.

Claims are labelled **MEASURED** (a number and the check that produced it) or
**ASSERTED** (plausible, unchecked — verify before building on it), per
[`session_roles.md`](session_roles.md).

**Vancouver would be the first Canadian city in this project**, so it also
lands the two Canadian notices on the deploy gate. Read "Before you commit"
last, not first.

---

## Why this city

**MEASURED.** 861 storefront sites per in-city station — **the densest measured
anywhere in this project**, against D.C.'s ~173 and Boston's ~39. It keeps only
20 of 53 stations (38%), which looks alarming and is the least interesting
number, exactly as with D.C. Three buckets, all covered by one registry.

## Start here

```bash
python scripts/scaffold_city.py --dry-run \
  --slug vancouver --name "Vancouver" --system-name "SkyTrain" \
  --taxonomy vancouver_businesstype --new-taxonomy \
  --value-column businesstype --field-label "Business type" \
  --lat 49.2827 --lon -123.1207
```

Every argument is settled except the taxonomy name, which follows the
`<city>_<column>` convention of `chicago_license`, `phl_licensetype`,
`miami_catgryname` and `boston_licensecat`. `--map-step` stays at the default
3: **no geocoding step is needed** (see below).

## Sources

### Business — `business-licences`, Opendatasoft

| | |
|---|---|
| Portal | `opendata.vancouver.ca`, Opendatasoft Explore v2.1 |
| Dataset | `business-licences` |
| Export pattern | `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/<dataset>/exports/csv` |
| Licence | OGL – Vancouver (text stored in `docs/licenses/`) |
| `SOURCE_ENCODING` | `utf-8` |

**MEASURED:** 205,943 rows all years; **58,346** at `folderyear='26' AND
status='Issued'`; `geo_point_2d` populated on **50.8%**, giving **29,660
mappable** licences. `businesstype` is **single-valued** — 93 distinct values,
81 with ≥10 rows — so Vancouver avoids the multi-value delimiter trap that
Calgary, Edmonton and Surrey all carry.

**Two traps:**

- **Opendatasoft CSV exports are semicolon-delimited**, not comma. Pass
  `sep=";"`.
- **`businesstradename` is blank on 63.0%** — the Los Angeles trap (68%) at
  almost the same severity. See "The name problem", which is the largest open
  decision in this build.

**ASSERTED:** that `folderyear='26'` is still the right vintage. The year rolls;
re-check the current value before downloading rather than copying the filter.

### Transit — TransLink SkyTrain

**MEASURED:** Mobility Database id **1222**. Three subway lines — Expo,
Millennium, Canada — plus one commuter rail route (`route_type 2`, the West
Coast Express) **excluded as everywhere**. 53 stations system-wide, 20 inside
Vancouver.

TransLink's feed carries **no `feed_info.txt`**, so it declares no licence of
its own and no expiry. Prefer the agency's own feed over the catalogue mirror —
that is the lesson Toronto's three-months-stale mirror taught.

**ASSERTED:** which 20 stations are the in-city set. The count is measured; the
list was never written down. Regenerate it, do not reconstruct it.

### Boundary — `local-area-boundary`, dissolved

```
https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/local-area-boundary/exports/geojson
```

**Do NOT use `city-boundary`.** It returns a single **MultiLineString**, and a
point-in-polygon test against it matches nothing, silently — San Francisco's
nine-county problem in a new form.

**MEASURED:** the 22 local-area polygons union to **one** Polygon (not
multipart — the local areas tile the city with no gaps), **118.8 km²** against
the city's ~115. **29,613 of 29,660 businesses fall inside — 99.84%**, with 47
outside, a plausible waterfront/edge residue worth eyeballing at build time
rather than assuming away.

The area check is the load-bearing part: a dissolve that silently dropped a
local area would still return a valid Polygon, and only the km² and the
containment rate catch it.

### Projected CRS

**EPSG:32610** (UTM 10N), derived from longitude ≈ −123.1 per the project
invariant. Never EPSG:4326 for geometry or distance.

## Geocoding — not needed

**MEASURED.** Of 58,346 current-year Issued licences, 27,103 have **neither**
coordinates nor a house-and-street address, and they are overwhelmingly
categories this project excludes anyway: Long-term Rental 10,698, Short-term
Rental Operator 3,910, General Contractor 3,575, Trade Contractor 1,670,
Consulting 1,062.

Only **1,583 rows (2.7%)** have a real address and no coordinates. A row
missing coordinates is not automatically a row needing geocoding.

If those 1,583 ever become worth recovering, Vancouver publishes
`property-addresses` (99,744 records, `civic_number`, `std_street`,
`geo_point_2d`, OGL–Vancouver). **ASSERTED:** it would match. It has never been
match-tested.

## The residence filter — the one genuinely novel piece

Vancouver is **the only Canadian city of the six with no licence-level
home-business flag** (Surrey has `LicenseType`, Edmonton `<Home Based
Business>`, Calgary `homeoccind`). It needs the US-style inference, and no
Canadian province publishes owner-occupancy — BC Assessment is not open data.

**The address join is REJECTED. Do not retry it.** Tested 2026-09-21 against
the 29,660 mappable licences: **6.5% matched**. The formats are systematically
different — direction prefixed in licences (`W 8TH AV`) and suffixed in the tax
roll (`8TH AVE W`), `AV` against `AVE`, only 35% of street names appearing
verbatim, and civic numbers stored as **ranges** with nulls so exact matching
fails structurally.

**The spatial join works, and better than San Francisco's.** Two hops, in
EPSG:32610:

```
business point → property-parcel-polygons (99,701 parcels, spatial)
              → property-tax-report on tax_coord = land_coordinate
              → zoning_classification
```

| Step | MEASURED |
|---|---|
| Point inside a parcel | **29,642 of 29,660 — 99.9%** |
| + nearest parcel within 40 m | 18 more, median 0.0 m → **100.0%** |
| Parcel → zoning class | **29,549 — 99.6%** |

San Francisco reached 93.4% at a median 1.4 m; San Diego needed a buffered
nearest-centroid query per point. **Vancouver's coordinates sit on their
parcels.**

`property-tax-report` (1,553,448 records, OGL–Vancouver) carries
`zoning_classification` with clean values — One-Family Dwelling 202,740,
Two-Family Dwelling 48,300, Multiple Dwelling 87,557, Commercial 132,576 — plus
`legal_type` (LAND / STRATA).

**The filter it produces is small.** 2,947 rows (9.9%) are purely residential
zoning, 3,134 (10.6%) have a person-like name, and **both is 232 rows (0.78%)**
— of which **174 are `Long-term Rental`**, excluded as non-storefront anyway.
The residual after a storefront filter is on the order of **~58 pins**
(Restaurant 13, Retail Dealer - Food 7, Limited Service Food 6, Health Care 6).
That is Philadelphia's territory (8 pins), not San Francisco's (217).

### Two things already settled about it

**The blind spot is real and smaller than it looks.** `Comprehensive
Development` is the zoning on **11,935 mappable licences — 40%** — and being
mixed-use it never flags residential, so a home business on CD land is
invisible. CD covers exactly the dense central areas where a "home" is a condo.

**The obvious refinement was tested and REJECTED — do not retry it.**
`legal_type` STRATA on CD land looks like it should isolate the condo home
business. Of 11,935 CD licences: LAND 9,648, STRATA 2,271. Of the 1,183 with a
person-like name: LAND 928, STRATA 253 — a STRATA share of 21.4% against a
baseline of 19.0%, **1.12x enrichment, i.e. none**. A sample of 16 candidate
names returned *Tim Hortons, Taco Time, Kiku Sushi, Caffe Artigiano, Praxis
Legal, CoastKids Pediatrics* — not one a home business. STRATA on CD land means
"a commercial unit in a mixed-use building", which is what CD zoning is
designed to produce. A unit number does not separate them either (42% of
candidates have one, and so do commercial units).

## The name problem — the largest open decision

**MEASURED, and it is worse than the headline.** `businesstradename` is blank
on 63.0%, so the pipeline falls back to the legal name on nearly two-thirds of
rows. On the raw registry, **8.21%** of displayed names match the person
pattern (4,792), of which 1,182 sit at a unit address, and **1,467 rows take
the "Person (Trade Name)" form** — the New York pattern invisible to every
other test.

**Restricted to the categories this project actually maps, the rate rises to
16.94%**: Limited Service Food 22.3%, Restaurant 20.0%, Retail Dealer 18.6%,
Retail Dealer - Food 13.2%, Beauty Services 7.8%. **The storefront filter makes
this worse, not better** — which is the opposite of the usual direction and the
reason this is called out separately from the residence filter.

These are **raw-registry rates, not mapped-pin rates**, so they are not
comparable to the US figures in `DECISIONS.md`, which are measured after step 2.
They are indicative, and they are bad.

**The decision to make:** what does a pin display when the trade name is blank?
Los Angeles' answer was to exclude the catch-all category driving it; D.C.'s
was a structural `ENTITYTYPE` signal. Vancouver has neither. This is a project-
owner call, it should be made before the map renders rather than after, and it
belongs in `DECISIONS.md` either way.

## Classification

`businesstype`, 93 single-valued categories, 81 with ≥10 rows. In line with what
the project already handles (Miami's 150 `CATGRYNAME`, Philadelphia's 50 licence
types).

**ASSERTED — the whole of it.** No bucketing exists. The 93 values have never
been listed, let alone assigned to Retail / Food service / Personal services.
This is the real work of the build and none of it is done. Per the project's
convention, `classify()` **raises** on an unknown value rather than defaulting
to None.

The excluded categories are partly known from the geocoding measurement:
Long-term Rental, Short-term Rental Operator, General Contractor, Trade
Contractor, Consulting are all non-storefront and between them account for
20,915 of the unmappable rows.

## Scope — decide before building

Vancouver and **Surrey** share one transit system and one TransLink licence.
Surrey has no rail of its own, 4 in-city stations, and **549 sites/station**.
The notices file treats them as one regional build, and Miami is the precedent
for a deliberately regional city.

**Unresolved.** Build Vancouver alone, or Vancouver + Surrey as one regional
map? It changes the page label (Miami's is "Miami (Regional)" because a map
spanning six municipalities cannot honestly be called Miami), the boundary
handling, and whether Surrey's own OGL joins the gate. Not a Step 0 question —
a project-owner one.

If Surrey is included, note its boundary trap: `sur_b.geojson` **declares
EPSG:4326 while containing UTM 10N metres**, so use
`set_crs(32610, allow_override=True)`, never `to_crs`, and filter to
`NAME = 'SURREY'` because 9 of its 10 features are town centres.

## Before you commit

Vancouver is the first Canadian city, so it lands notices on the deploy gate.
**Promote these into `docs/data_sources.md`, "Notices this project MUST display
when published", in the same commit as the city** — that section is the gate
and it stays a list of things that actually apply.

**1. OGL – Vancouver, exact wording:**

> `Contains information licensed under the Open Government Licence – Vancouver.`

This licence **terminates automatically on breach** — "if you fail to comply
with any of them, the rights granted to you under this licence… will end
automatically." The notice is not cosmetic.

**2. The TransLink Legend, prominently displayed, in exactly this wording:**

> "Route and arrival data used in this product or service is provided by
> permission of TransLink. TransLink assumes no responsibility for the accuracy
> or currency of the Data used in this product or service."

**THE TRAP: TransLink has two mandated wordings and this is the GTFS one.** The
Open API terms mandate a different legend beginning "Some of the data used in
this product or service…", which **would not satisfy the GTFS terms**. This
project uses static GTFS. Both texts are stored in `docs/licenses/`;
`translink-gtfs-static-terms-of-use.txt` is the operative one.

**3. No TransLink marks beyond that legend** — satisfied by construction, since
the project draws its own geometry from `shapes.txt` and reproduces no roundel.
SkyTrain line names in plain text are the thing to keep an eye on.

Also standing: the OSM basemap attribution, and
`python scripts/check_personal_exposure.py vancouver` with the verdict recorded
in `DECISIONS.md` — which for this city is the check that matters most.

**Already decided, do not relitigate:** no prior contact with TransLink is
required. Their information obligation reads as responsive to a request, not a
precondition of use; the GTFS terms have no counterpart to the API terms'
"in its entire discretion, approves you as a user". Recorded in `DECISIONS.md`,
2026-09-21.

## Open questions, collected

1. **Trade-name fallback policy** — 63% blank, 16.94% person-pattern on
   storefront types. The biggest one.
2. **Scope** — Vancouver alone, or Vancouver + Surrey regional.
3. **The 93 `businesstype` values** — none bucketed yet.
4. **`folderyear`** — confirm the current vintage before downloading.
5. **The 47 businesses outside the dissolved boundary** — look, don't assume.
6. **The 20 in-city stations** — count measured, list never recorded.
7. **The 1,583 address-but-no-coordinates rows** — recover, or accept the loss.
