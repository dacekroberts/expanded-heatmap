# Dublin — build brief

**Step 0 run 2026-09-22.** Every number below was measured against a live
source on that date, not read off a catalogue. Where something is asserted
rather than measured it says so.

Ireland has never been built in, so `add-country`'s national questions apply —
but Ireland yields exactly **one** candidate city, so the country profile and
the city's Step 0 are the same pass and are recorded here rather than in a
separate country file. That is the whole reason Dublin was picked ahead of
candidates with viable siblings: nothing else in the country waits on it.

## The one-line summary

The Irish rateable valuation register, published by **Tailte Éireann** through
a keyless JSON API, carries **38,265 premises across the four Dublin local
authorities**, of which **13,945 are storefront**, **99.87% already carry Irish
Transverse Mercator coordinates**, and **not one carries a business name**.
Dublin is the first city in this project with **no geocoding leg and no
reprojection leg at all**, and the first with **no name to put on a pin**.

## ✅ SETTLED 2026-09-22 — the owner's four calls

These were taken before the build, on the measurements below, and they are the
decisions that shape everything else.

| Decision | Call | Where the reasoning is |
|---|---|---|
| **Scope** | **All four Dublin local authorities**, not Dublin City alone | Below, "The scope costs 36% coverage" |
| **Pin label** | **Address + use** — `Address1` becomes `business_name`, `Uses` carries the category line | Below, "The register publishes no name" |
| **Lines drawn** | **Luas Red, Luas Green, DART** — commuter and InterCity dropped | Below, "Rail leg" |
| **Taxonomy level** | **`Uses`, not `Category`** | Below, "Taxonomy" — settled by measurement, not taste |

---

## Business leg — `opendata.tailte.ie`, MEASURED 2026-09-22

### The endpoint, and the two hosts that no longer exist

```
https://opendata.tailte.ie/api/Property/GetProperties
    ?Fields=*
    &LocalAuthority=<AUTHORITY>
    &Format=json
    &Download=false
```

No key, no account, no registration. The API states its own contract in its
error body, which is worth knowing because there is no documentation page
anywhere — `opendata.tailte.ie/` itself is a 404, and so are `/swagger`,
`/docs`, `/api` and `/robots.txt`:

```json
{"message":"Use either Property Number or Local Authority"}
```

**Two dead predecessors, and neither redirects.** `api.valoff.ie` is
**NXDOMAIN**; `www.valoff.ie` answers **000**. The API moved twice and left no
forwarding. A brief that recorded only "the Valuation Office API" would send
the next reader to a corpse, which is what happened here once already — the
first Irish probe recorded the country as *negative* on the strength of those
two dead hosts.

### The four authorities — and the exact strings, which are a trap

`LocalAuthority` is matched **exactly**. Dún Laoghaire–Rathdown's spelled-out
name returns **zero rows with HTTP 200** — a silent empty answer, not an error.

| `LocalAuthority` value (the REGISTER's spelling) | Rows | Storefront |
|---|---|---|
| `DUBLIN CITY COUNCIL` | 19,810 | 8,016 |
| `FINGAL COUNTY COUNCIL` | 6,528 | 2,057 |
| `SOUTH DUBLIN COUNTY COUNCIL` | 6,926 | 1,822 |
| `DUN LAOGHAIRE RATHDOWN CO CO` | 5,001 | 2,050 |
| **Region total** | **38,265** | **13,945** |

⚠️ **`DUN LAOGHAIRE RATHDOWN COUNTY COUNCIL` returns 0 rows.** The register
abbreviates to `CO CO` and uses no hyphen. The **boundary layer spells the same
place `DUN LAOGHAIRE-RATHDOWN COUNTY COUNCIL`**, with a hyphen and no
abbreviation. Two different strings for one authority, in the two sources that
must be joined to each other — so the join is by an explicit mapping table in
`config.py`, never by string equality.

### Schema — 19 fields, and one absence that shapes the build

Every one of the 38,265 rows carries all 19 keys.

| Field | Population | Notes |
|---|---|---|
| `PropertyNumber` | 100% | The real primary key; dedupe on this |
| `Address1`–`Address5` | 99.88% on `Address1` | `Address4`/`Address5` usually null |
| `Eircode` | 98.05% | ⚠️ See the licence flag — recommended **dropped** |
| `Xitm`, `Yitm` | **99.87%** | Irish Transverse Mercator, **already metres** |
| `Category` | 100% | 13 values region-wide; too coarse — see taxonomy |
| `Uses` | 100% | 963 distinct values; **this is the taxonomy** |
| `Valuation`, `ValuationDate`, `PublicationDate` | ~100% | Not used by the map |
| `ValuationReport[]` | see caveat | Per-floor `Area`/`Nav`/`FloorUse`/`Level` |
| `County`, `LocalAuthority` | 100% | |
| `CarPark`, `AdditionalItems` | 100% | Numeric, not used |

**51 rows of 38,265 have no coordinates** (0.13%). That is far below the
"never silently drop a large share" threshold and needs no geocoding step —
but print the count in step 2 anyway, because 46 of those 51 are pubs, which
is not a uniform loss.

### The register publishes no name — and that is two findings, not one

**There is no business-name column. There is no occupier, tenant, ratepayer or
owner column either.** Every key was checked against
`name|occupier|tenant|owner|ratepayer|proprietor|person|contact`: zero matches.
The register records **premises**, and the Irish valuation list is non-domestic
by statute.

**As a privacy position this is the strongest in the project.** New York can
only *assert* that a registrant-name column never arrives, because its source
has one and step 2 must exclude it. Dublin has none to exclude. Los Angeles'
failure mode — a blank trade name falling back to a person's name at what looks
like their home — **cannot occur here, structurally**. Run
`check_personal_exposure.py` anyway for the record, and expect it to have
nothing to measure; say so in `DECISIONS.md` rather than reporting a clean
number as though it were a result.

**As a map-design problem it is real.** Every other city's pins carry a trade
name. Dublin's cannot. ✅ **Settled: `Address1` becomes `business_name` and the
tooltip's category line carries `Uses`**, so a pin reads
`12 Camden Street` / `HAIRDRESSING SALON`. No change to `map_common.py`.

⚠️ **Say this on the city page.** A reader who knows the other twelve cities
will read unnamed pins as a pipeline failure. It is not: it is what an Irish
valuation register is. This is the New York disclosure pattern applied to a
different absence — state what the source does not contain, so the reader draws
a conclusion about Irish public records rather than about this map.

---

## Taxonomy — `Uses`, and it INVERTS the rule Barcelona set

`premises-taxonomy` says the deciding measurement is the catch-all share at
each level of the scheme. Measured region-wide:

| Level | Distinct values | Catch-all | Share |
|---|---|---|---|
| `Category` | 13 | `MISCELLANEOUS` | **3.2%** |
| `Uses` | 963 | `SHOP` / `STORE` / `-` variants | **16.4%** |

**Dublin keys on `Uses` — the level with the LARGER catch-all.** That is the
opposite of Barcelona, where the finer level won *because* its catch-all was
smaller (2.6% against 35.1%). The reason is that catch-all share is a
tiebreaker, not the criterion. **The criterion is whether the level can
separate this project's three buckets at all**, and `Category` cannot:

| | Rows | Where they sit in `Category` |
|---|---|---|
| **Food service** | 2,335 | `RETAIL (SHOPS)` **1,483** · `HOSPITALITY` 723 · `OFFICE` 74 · `CENTRAL VALUATION LIST` 46 · `INDUSTRIAL USES` 5 |
| **Personal services** | 744 | `RETAIL (SHOPS)` **677** · `OFFICE` 61 · `LEISURE` 2 · `INDUSTRIAL USES` 2 · `MISCELLANEOUS` 1 |

Keying on `Category` would put every hairdresser, beauty salon and launderette
in Retail, and split restaurants from pubs across two buckets. All three
buckets collapse. `Uses` names them individually — `HAIRDRESSING SALON`,
`BEAUTY SALON / MASSAGE`, `DRY CLEANERS / LAUNDERETTE`, `RESTAURANT`,
`TAKE AWAY`, `CAFE`, `PUB` — so it is the only usable level regardless of its
catch-all.

**Carry this back into `premises-taxonomy`:** measure the catch-all at every
level, *then* check bucket separability, and let separability win. Four cities
had a smaller catch-all at the level they chose; Dublin is the first where the
right level is the worse one on that number alone.

### `Uses` is multi-valued, and `-` is a null placeholder

Values are comma-separated with `-` standing in for an empty slot:

```
"SHOP, -"                       776   one use
"-, RESTAURANT"                 586   one use, in the second slot
"STORE, YARD"                         two real uses
"HAIRDRESSING SALON, OFFICE (OVER THE SHOP)"   two real uses
```

Region-wide: 18,385 rows have two segments, 1,417 one, 8 four. **1,869 rows
have both slots genuinely populated** — confirmed against `ValuationReport`,
where `STORE, YARD` resolves to floors `STORE` and `YARD`, so these are real
mixed-use premises rather than a formatting artefact.

**Step 2 must split on `", "`, drop every `-`, and classify the remainder.** A
naive exact-match mapping on the whole string would need 963 entries and would
still miss every new combination. Mixed-use rows need a priority order the way
Chicago's `LICENSE_PRIORITY` does — a premises that is `HAIRDRESSING SALON,
OFFICE (OVER THE SHOP)` is a salon on the map, not an office.

### Filters to apply, all measured inside the storefront categories

| Value | Rows | Why |
|---|---|---|
| `VACANT` | 117 | Not a trading storefront. Same call as Barcelona's vacancy filter |
| `RIGHT OF TRADING` | 150 | A trading right, not a premises |
| `ATM` | 88 | A machine in a wall, not a shop |

### ⚠️ The confidentiality caveat — MEASURED, and it does not bite

`tailte.ie/home/api/` warns the data "might not hold detailed information on
certain types of properties (e.g. Hotels, Pubs, Cinemas, Service Stations,
Guesthouses…), due to the confidential nature of the associated information."

Pubs are a large share of Dublin food service, so this had to be tested rather
than noted. It was, with a control:

| Type | Rows | `Uses` blank | `ValuationReport` empty |
|---|---|---|---|
| `PUB` | 767 | 0 | **767 (100%)** |
| `HOTEL` | 210 | 0 | **210 (100%)** |
| `SERVICE STATION` | 184 | 0 | **184 (100%)** |
| `GUESTHOUSE` / `HOSTEL` / `CINEMA` | 116 | 0 | **116 (100%)** |
| *control:* `HAIRDRESSING SALON` | 445 | 0 | 0 (0%) |
| *control:* `PHARMACY` | 232 | 0 | 0 (0%) |
| *control:* `CLOTHES SHOP` | 327 | 0 | 0 (0%) |

**What is withheld is the floor-level valuation detail, not the row and not its
classification.** Every named type arrives present and fully categorised, and
767 pubs across the four authorities sits inside the published 750–800 range
for Co. Dublin, so nothing was suppressed from the list itself.

**Consequence: none, for this build**, which reads `Category` and `Uses` and
never opens `ValuationReport`. **Consequence if the build ever weights by floor
area**: total, and concentrated exactly on food service. Recorded here so that
is a known constraint rather than a rediscovery.

---

## Scope — four authorities, and it costs 36% coverage

✅ **Settled 2026-09-22: all four.** Precedent is the Vancouver + Surrey
regional build. The cost was measured before the call, not after.

Storefronts within the project's 0.6 mi outer ring of a station, against the
100 Luas + DART stops and the 37 commuter stops they do not already serve:

| Authority | Storefronts | Luas/DART | Commuter-only | **No rail at all** |
|---|---|---|---|---|
| Dublin City | 8,016 | 6,139 (77%) | 150 | **1,727 (22%)** |
| Dún Laoghaire–Rathdown | 2,050 | 1,405 (69%) | 0 | **645 (31%)** |
| Fingal | 2,056 | 307 (15%) | 421 (20%) | **1,328 (65%)** |
| South Dublin | 1,822 | 508 (28%) | 48 | **1,266 (70%)** |
| **Region** | **13,944** | **8,359 (60%)** | **619 (4.4%)** | **4,966 (36%)** |

**36% of the region's storefronts are near no rail of any kind**, against 22%
for Dublin City alone. Fingal is the extreme: its largest town, **Swords
(~40,000 people), has no rail station of any type**, and South Dublin's
Clondalkin and Lucan are commuter-only.

**State this on the city page.** A regional map with honest empty areas is
defensible; a regional map that looks like a pipeline lost half its data is
not. The wording should make clear the emptiness is a fact about where Dublin
built rail, not about where Dublin has shops.

---

## Rail leg — Luas Red, Luas Green, DART

**42 route relations**, measured via `overpass-api.de`. ⚠️ `overpass.osm.ch`
returned an **empty 200** for the same query on the same day —
`brief_check.py`'s `_overpass_once` already rejects that, and the first attempt
here bypassed it and would have recorded "0 relations" against a real 42. Use
the project's own Overpass path, never a hand-rolled one.

| Group | Relations | Refs | Colour on OSM |
|---|---|---|---|
| **Luas** (tram, Transdev) | 6 | **2** | Red `#CD5C5C`, Green `#008531` |
| **DART** (train, Iarnród Éireann) | 4 | 1 (`DART`) | `#68C56B` |
| Commuter (Northern / Western / South Western) | 14 | mostly unref'd | none |
| InterCity (Cork, Galway, Sligo, Rosslare, Belfast) | 18 | mostly unref'd | none |

**All three drawn lines already carry a colour**, so nothing needs a hand-built
palette. The "32 relations lacking a colour" recorded in the master list was an
artefact of counting InterCity services that are not drawn.

### Commuter and InterCity are dropped — precedent, then measurement

Commuter rail is excluded in **every built city**, and eight record it
explicitly: Boston (`CR-*` Regional Rail), Chicago (Metra), Madrid (Cercanías),
Miami (Tri-Rail), Philadelphia (Regional Rail), Vancouver (West Coast Express),
and Montréal and Washington DC noting they have none to exclude.

Independently, it is worth **4.4% of this region** — 619 storefronts, and zero
in Dún Laoghaire–Rathdown. It does not solve the coverage gap; the gap is a
scope property, not a lines property.

InterCity has never arisen before. Dublin is the first city where intercity
services land in the same Overpass query as the urban network, because Iarnród
Éireann runs both and OSM tags both `route=train`. **Filter on
`network=Commuter` / `network=InterCity`, not on `route=`.**

### ⚠️ DART's inclusion is a JUDGMENT CALL, not an automatic one

By the letter of the rule above — national railway operator, OSM `route=train`,
GTFS `route_type 2` — **DART would be excluded with the rest.** It is kept on
functional grounds:

- **Philadelphia is the precedent.** SEPTA's Market–Frankford and Broad Street
  lines are drawn and Regional Rail is not, and the line between them is
  station spacing and frequency, not which company runs the trains.
- **Miami drew the same line**: Metrorail in, Tri-Rail out.
- DART's in-city spacing — Connolly, Tara Street, Pearse, Grand Canal Dock,
  Lansdowne Road, Sandymount — is about a kilometre. The Commuter services it
  shares track with run to Dundalk and Portlaoise.

Record this in `DECISIONS.md` as a decision with a rejected alternative, not as
an application of the existing rule. **If the rule is ever tightened to "no
`route_type 2`, no exceptions", Dublin loses its principal line** and the city
should be re-scoped rather than quietly shipped as a two-tram-line map.

---

## Boundary leg — Tailte Éireann via ArcGIS, EPSG:2157

**Use the FeatureServer, not the Hub download.** The `data.gov.ie` resource
list points at `data-osi.opendata.arcgis.com/api/download/v1/items/...`, which
is the async job endpoint that answers HTTP 202 (the Surrey trap in
`add-country`). The synchronous service behind it:

```
https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/
  National_Statutory_Boundaries_-_Local_Authorities__Ungeneralised_-_2026/
  FeatureServer/3
```

- Layer 3, `Local Authorities Ungen-2026`, `esriGeometryPolygon`, 65 fields.
- Authority name is **`ENG_NAME_VALUE`** (Irish is `GLE_NAME_VALUE`).
- **Spatial reference `wkid 2157`** — Irish Transverse Mercator.

| Authority (BOUNDARY spelling) | Polygons | Area |
|---|---|---|
| `DUBLIN CITY COUNCIL` | 1 | 130.1 km² |
| `DUN LAOGHAIRE-RATHDOWN COUNTY COUNCIL` | 42 | 126.5 km² |
| `FINGAL COUNTY COUNCIL` | 46 | 457.2 km² |
| `SOUTH DUBLIN COUNTY COUNCIL` | 1 | 223.4 km² |
| **Region** | **90** | **937.3 km²** |

⚠️ **The layer is multipart.** Fingal returns 46 polygons and Dún
Laoghaire–Rathdown 42 — islands and coastal outcrops, most under 0.1 km².
**Step 1 must dissolve by `ENG_NAME_VALUE` before any point-in-polygon test**,
or a station will be tested against Lambay Island. A query that takes the first
returned polygon per authority gets a rock.

### No reprojection, and no geocoding — a first for this project

The register publishes `Xitm`/`Yitm` and the boundary publishes `wkid 2157`.
Both are **EPSG:2157, Irish Transverse Mercator, in metres, covering all of
Ireland**. Buffering and distance work happen directly in the source CRS, and
the only transform needed is 2157 → 4326 for display.

This is a deliberate deviation from the "project to the city's own UTM zone"
invariant, and it is the stronger choice: Dublin's longitude (−6.26) puts it in
UTM 29N, but ITM is the national grid the data is already in, so using UTM
would mean two transforms to end up less accurate. **Record the deviation and
its reasoning in `config.py`**, per the invariant's own instruction to comment
how the CRS was derived.

---

## Licence — CC BY 4.0, PERMITTED WITH CONDITIONS

Established 2026-09-22 by the `licence-read` agent, which opened 13 documents
and probed 11 more that turned out not to exist.

**Declared licence**, machine-read from
`data.gov.ie/api/3/action/package_show?id=valuation-office-api`:
`license_id` **`CC-BY-4.0`**, `isopen` **true**.

This is a deliberate declaration rather than portal boilerplate: of Tailte
Éireann's datasets on `data.gov.ie`, only **3 of the first 100** carry
`CC-BY-4.0` and **97 carry no licence field at all**, so a blanket default
would have set all of them.

**Granting text** — Circular 12/2016 Annex 1, the instrument Tailte's own open
data page links:

> "The Information Provider grants the user a worldwide, royalty-free,
> perpetual, non-exclusive licence to use the Information, including for
> commercial purposes" · "Copy, modify, publish, translate, adapt, distribute
> or otherwise use the Information in any medium, mode or format for any lawful
> purpose."

### MUST DISPLAY

Add to `docs/data_sources.md` under "Notices this project MUST display when
published", and to `_NOTICES` in `app/components.py`:

> Contains Irish Public Sector Information licensed under a Creative Commons
> Attribution 4.0 International (CC BY 4.0) licence. Source: Tailte Éireann
> valuation data, via the Tailte Éireann Valuation open API. This map filters,
> re-categorises and aggregates that data into density measures; the filtering,
> categories and densities are this project's own interpretation and are not
> produced or endorsed by Tailte Éireann. The data is published "as is"; Tailte
> Éireann gives no warranty as to its accuracy, completeness or currency.

That single notice discharges four separate obligations: the PSI attribution
string, Tailte's own requirement to be named as content creator, **CC BY 4.0
§3(a)(1)'s duty to indicate modification** (which a bare source credit does not
satisfy — the Montréal/INEGI family), and the non-endorsement clause.

⚠️ **Three different attribution strings are live on Irish government sites**,
differing in one word — Circular 12/2016 says "Information", `data.gov.ie/license`
says "Data", `data.gov.ie/technical-framework` says "Government Data". The
wording above follows the **Circular**, because it is the instrument Tailte's
own page points to and the only one of the three that is a licence rather than
guidance. No document ranks them. **Recorded as a disclosed position.**

### MUST NOT SAY

- Nothing implying official status or Tailte endorsement (Circular Annex 1).
- **No claim that the data is accurate, complete or current** — Tailte
  disclaims all three, and `tailte.ie/home/api/` is explicit that the API "is
  not guaranteed to be complete". Same cross-city prose rule as MTA and WMATA.
- **No Tailte logo, crest or official symbol.** The PSI licence excludes them
  and CC BY 4.0 §2(b) does not license trademarks.

### MUST DO — nothing

**No affirmative act is owed.** No registration, no notification, no permission
request, no statistics return. Swept for the full step-6c phrase set across
every document: zero hits. **This is the clean negative Barcelona was not**,
and it is worth stating positively so nobody re-opens it.

Channels exist anyway, all live and none CAPTCHA-walled, so a correction
request has somewhere to go: **`opendataofficer@tailte.ie`** (data.gov.ie's
listed dataset owner) and `opendata@tailte.ie` (named on tailte.ie for X/Y and
Eircode corrections).

One page that looks alarming and is not: `tailte.ie/map-shop/map-licences-and-copyright/`
says users "must obtain prior permission from Tailte Éireann" — it governs the
paid Map Shop surveying products and mentions valuation, open data, API,
Eircode, PSI and Creative Commons **zero times each**. Read and inapplicable,
recorded so the next reader does not have to re-establish that.

### ⚠️ OPEN — the `Eircode` column

Tailte publishes `Eircode` on 98.05% of rows, but the Eircode database is
third-party IP (An Post / OSi via GeoDirectory, licensed commercially through
Capita), and both the PSI licence and `data.gov.ie/license` carve out "third
party rights … including … database rights" that the Information Provider is
not authorised to license.

- **Permits**: Tailte publishes them inside a dataset it declares CC BY 4.0.
- **Does not**: republishing ~38,000 Eircodes is a substantial extraction from
  a database whose *sui generis* right is held by someone else.

**Recommended: drop the column in step 2.** The build does not need it — it has
`Xitm`/`Yitm` and five address lines — so dropping removes the only
third-party-rights exposure in the source at zero cost to the map. **Owner's
call; not yet taken.**

---

## Privacy

`check_personal_exposure.py` should be run and will find nothing to measure,
because there is no name column of any kind to fall back to. Add Dublin to its
`REGISTRIES` table with the trade-name column set to `Address1` and **no**
fallback column, and record in `DECISIONS.md` that the clean result is
structural rather than a measurement — the distinction New York's entry draws.

The register is non-domestic by statute, so the residence-filter question that
LA, Philadelphia and San Diego all needed does not arise either.

---

## Still unknown — the honest list

1. **Which attribution string is canonical.** Three are live; the Circular's is
   used, as a disclosed position. Unresolvable from the documents.
2. **Whether the `Eircode` column is safe to republish.** Recommended dropped;
   owner's call outstanding.
3. **Whether Tailte's five superseded PSI conditions are live or stale.**
   `tailte.ie` still publishes "reproduce information accurately", "not use the
   information in a misleading way" and "not … for the principal purpose of
   advertising" — the wording of PSI General Licence 2005/08/01, which Circular
   12/2016 §6 expressly supersedes. **Not resolved, and does not need to be:**
   the notice above complies with both readings, and a commercial-density map
   is not advertising a product.
4. **What `CENTRAL VALUATION LIST` is doing with 46 pub rows.** All 46 of that
   category's rows region-wide mention `PUB`. Probably a centrally-valued
   chain; unexamined, and small enough not to block. Sample it in step 2.
5. **The mixed-use priority order.** 1,869 rows carry two real uses. The order
   is a build decision and has not been written.
6. **`route_type` for DART in any Irish GTFS.** The rail leg is OSM-only here;
   if a GTFS feed is ever used instead, DART's route type should be checked
   against the judgment call recorded above rather than assumed.

---

```brief-checks
[
  {
    "id": "tailte-api-dublin-city",
    "claim": "The Tailte valuation API answers for Dublin City Council with no key and no account, returning ~12.7 MB of JSON for 19,810 rows. If this fails the endpoint has moved for a THIRD time - api.valoff.ie and www.valoff.ie are both already dead",
    "kind": "http_ok",
    "url": "https://opendata.tailte.ie/api/Property/GetProperties?Fields=*&LocalAuthority=DUBLIN%20CITY%20COUNCIL&Format=json&Download=false",
    "min_bytes": 9000000
  },
  {
    "id": "tailte-api-dun-laoghaire-exact-string",
    "claim": "Dun Laoghaire-Rathdown answers ONLY to the abbreviated register spelling DUN LAOGHAIRE RATHDOWN CO CO, returning ~3.2 MB for 5,001 rows. This check guards the exact string, because the spelled-out name returns zero rows with HTTP 200 rather than an error",
    "kind": "http_ok",
    "url": "https://opendata.tailte.ie/api/Property/GetProperties?Fields=*&LocalAuthority=DUN%20LAOGHAIRE%20RATHDOWN%20CO%20CO&Format=json&Download=false",
    "min_bytes": 1500000
  },
  {
    "id": "valoff-is-retired",
    "claim": "The predecessor host is gone and does not redirect. When this check FAILS, valoff.ie has been revived and the endpoint above should be re-confirmed against it",
    "kind": "endpoint_absent",
    "url": "https://api.valoff.ie/api/Property/GetProperties"
  },
  {
    "id": "boundary-featureserver",
    "claim": "The local-authority boundary layer is a synchronous ArcGIS FeatureServer in EPSG:2157 carrying ENG_NAME_VALUE - NOT the async Hub download endpoint, which answers HTTP 202",
    "kind": "arcgis_layer",
    "url": "https://services-eu1.arcgis.com/FH5XCsx8rYXqnjF5/arcgis/rest/services/National_Statutory_Boundaries_-_Local_Authorities__Ungeneralised_-_2026/FeatureServer/3",
    "expect_geometry": "esriGeometryPolygon",
    "present": ["ENG_NAME_VALUE", "GLE_NAME_VALUE", "Shape__Area"]
  },
  {
    "id": "luas-two-refs",
    "claim": "Luas is 6 OSM relations collapsing to exactly 2 refs - Red and Green. Relations are directional pairs plus Red's two branches; refs are what gets drawn",
    "kind": "osm_route_refs",
    "bbox": [53.15, -6.55, 53.65, -6.02],
    "routes": ["tram"],
    "expect_relations": {"tram": 6},
    "expect_refs": {"tram": 2},
    "require_refs": {"tram": ["Luas Green Line", "Luas Red Line"]}
  },
  {
    "id": "dart-ref-exists",
    "claim": "DART is tagged as a ref on its relations, which is what makes it separable from the Commuter and InterCity services Iarnrod Eireann runs over the same track and OSM also tags route=train",
    "kind": "osm_route_refs",
    "bbox": [53.15, -6.55, 53.65, -6.02],
    "routes": ["train"],
    "require_refs": {"train": ["DART"]}
  }
]
```
