# Liverpool (Regional) — build brief

**Screened 2026-10-03 (staging, the coverage sweep's first group); Band B,
food only (owner, 2026-10-03). Scope approved by the owner the same day:
Liverpool, Sefton, Knowsley and Wirral. Merseyrail is drawn as a
commuter-rail exception (owner, 2026-10-03). Brief written the same day.**
Run `python scripts/brief_check.py liverpool` before writing any code. The
trail: `docs/decisions_drafts/staging.md`, 2026-10-03 "The sweep's first
group banded: eleven cities on the owner's approval", and the master list's
Band B row (`docs/city_master_list.md`).

⚠️ **One-bucket city on the UK six's shared steps.** Read
`docs/build_briefs/manchester.md` (the pilot) and
`docs/build_briefs/newcastle.md` (several authorities by code, Code-Point
centroids, two notices) first. The FSA leg is theirs unchanged:
`pipeline/fsa.py` (the read list, the flat, childminder and trading-as
rules), London's storefront filter (`pipeline/taxonomies/fsa_businesstype.py`),
and `pipeline/countries/uk.py` with `pipeline/countries/uk_fetch.py` for
steps 1 to 3 and the downloads. **What is new is the rail leg**: the first
UK map drawn on heavy rail (`route=train`), which the UK six's tram and
light-rail step 1 was not written for (below).

---

## The one-line summary

**The FSA register across the four councils Merseyrail serves: 7,400 food
storefronts, keyless, under the OGL. Merseyrail's Northern and Wirral Lines,
59 stations, drawn as the project's seventh commuter-rail exception. The work
is the rail leg on shared code built for trams, the City Line kept off the
map, and a page honest about evenings and Sundays.**

---

## Scope — four councils (owner, 2026-10-03)

| Council | FSA code | FSA API id | GSS (confirm at build) | Merseyrail stations |
|---|---|---|---|---|
| Liverpool | 414 | 179 | E08000012 | **17** |
| Sefton | 424 | 185 | E08000014 | **17** (Aintree included) |
| Knowsley | 412 | 178 | E08000011 | **2** (Kirkby, Headbolt Lane) |
| Wirral | 435 | 190 | E08000015 | **23** |
| **Four councils** | | | | **59** |

- **Out:** St Helens (FSA 421) and Halton (FSA 889) have no Merseyrail
  station (Guadalajara left out Tonalá on the same ground). The ten network
  stations outside Merseyside (Ormskirk, Aughton Park and Town Green in West
  Lancashire; Hooton to Chester and Ellesmere Port in Cheshire West and
  Chester) are cut at the boundary.
- **Select by code, assert exactly four.** The FSA files all four under its
  wider North West region (Manchester's precedent): `LocalAuthorityIdCode`
  414, 424, 412, 435. Code-Point Open keeps exactly the four GSS codes above;
  read them off the OSM boundaries' `ref:gss` in the one Overpass query and
  correct this table if they differ.
- **The API ids** are the screen's (the Authorities list, header
  `x-api-version: 2`), used only for the API's per-type counts; the build
  keys on the codes. `brief_check.py` cannot send that header (the API
  answers HTTP 404 without it, even for `/Authorities/basic`), so no check
  stands behind the ids; the codes are checked on the open-data page.
- **Boundaries:** the union of the four councils' `admin_level=8` relations,
  ids read at build from the cached query (not measured here; no OSM query
  was made for this brief). Merseyside is a ceremonial and metropolitan
  county, as Tyne and Wear is: use the four districts, never a county
  relation.
- **The scope alternative, recorded: Liverpool City Council only**, 17
  stations (the Wirral Line reduced to its four-station loop) and 3,451
  storefronts. It drops every Wirral branch and the Southport line past Bank
  Hall, which is why the owner took the regional scope, the UK six's
  precedent where a network spans districts (Newcastle, Manchester,
  Nottingham, Birmingham, Blackpool).
- **Page name "Liverpool (Regional)"** (the master list's row, Lille's and
  the UK six's precedent).
- **CRS:** UTM 30N **EPSG:32630**, the UK six's `CRS_PROJECTED`; EPSG:27700
  is only Code-Point Open's source CRS.
- **Region:** `"United Kingdom"`, `label_tier: "minor"`, as the UK six.
- **Mode: `metro` (owner, 2026-10-03, "1. metro").** `scaffold_city.py` takes metro,
  light_rail or tram, and has no commuter-rail value. Copenhagen, whose
  S-tog is drawn beside a metro, is `metro`; Dublin, with DART drawn beside
  the Luas, is `tram`. Liverpool has only Merseyrail. Recommend `metro` (an
  underground city-centre loop, trunks every 2-6 minutes); the build asks.

---

## Rail — Merseyrail, the commuter-rail exception

### The owner's call (2026-10-03)

**Merseyrail's Northern and Wirral Lines are drawn**, on the "every 15
minutes or better by day" reading of the test (`add-city`, the 15-minute
test; `docs/commuter_rail_list.md`, decided on spacing and frequency inside
the area, not on who runs the trains). London's Overground and Elizabeth line
are the nearest precedent: drawn because they run like Berlin's S-Bahn
inside London (owner, 2026-09-28). Copenhagen's S-tog and Dublin's DART are
the earlier ones. Brisbane failed because its timetable is 30 minutes off-peak
by day; Merseyrail's is not.

- **Disclosed on the page:** every branch drops to every 30 minutes after
  about 20:00 and on Sundays (Buffalo's page discloses its timetable the same
  way). That sentence is not in the approved template: a proposal, flagged in
  the drafts file.
- **The alternative, recorded:** without the exception Liverpool has no rail
  this project draws (no metro, no tram) and no page. Inside the exception,
  the scope alternative is Liverpool City Council alone, 17 stations (above).
- **A consistency question for the owner, not a blocker:** Glasgow's page
  leaves out its electric suburban rail as national rail without a recorded
  frequency test, and Newcastle leaves out Northern to the MetroCentre.
  Drawing Merseyrail may prompt a look at Glasgow's Argyle line.

### Frequency by section

Read 2026-10-03 from National Rail's journey planner (the industry
timetable; cookies rejected) for Tuesday 2026-10-06. Merseyrail's own site
and Realtime Trains sit behind a bot challenge (not attempted).
Merseytravel's timetables are PDF booklets (Northern Line from 17 May 2026,
about 203 KB; Wirral Line from 20 September 2026, about 288 KB), named here
and not read; the build may read them to confirm, as sources this brief
names.

| Section (station read) | Mon-Sat daytime | Evening | Sunday |
|---|---|---|---|
| Hunts Cross branch, Liverpool (Aigburth to Central) | every 15 | 15 until 20:44, then 30 | not read (replacement buses that day) |
| Southport line, Liverpool (Bank Hall to Moorfields) | every 15 | - | 30 |
| Ormskirk branch, Liverpool (Walton to Moorfields) | every 15 | - | - |
| Kirkby and Headbolt Lane branch (Rice Lane to Moorfields) | every 15 (still 15 at 18:04-19:49) | 30 from 19:49 | - |
| Northern Line trunk (Sandhills to Moorfields) | 12 an hour, every 4-6 | - | - |
| Wirral Line loop (James Street to Hamilton Square) | 10-12 an hour, every 2-6 | about 8 an hour at 21:00 | - |
| Wirral, New Brighton branch (Wallasey Grove Road) | every 15 | - | - |
| Wirral, West Kirby branch (Hoylake) | every 15 | - | - |
| Wirral, Chester and Ellesmere Port branches (Bebington) | 6 an hour (gaps of 7, 8 and 15) | - | - |
| Sefton, Southport line (Formby) | every 15 | - | - |
| **City Line (Wavertree Technology Park to Lime Street)** | **3 an hour, gaps of 33, 11 and 16** | - | - |
| **City Line (Mossley Hill to Lime Street)** | **3 an hour, gaps of 18, 11 and 31** | - | - |

Secondary sources agree on 15 minutes by day and 30 in the evening and on
Sunday per route. A 2025 press line that Southport to Hunts Cross runs every
15 "start to end of service" is not what the October 2026 timetable shows.
**Check at build** that Headbolt Lane gets every Kirkby-branch train (Rice
Lane's pattern was read, not the terminus) and that the Bebington pattern
holds for Wirral stations short of Hooton.

### Not drawn — named on the page

- **The City Line** (Northern Trains, Lime Street high level to Wigan and
  Warrington): 3 trains an hour, uneven, gaps of 31-33 minutes measured.
  Lime Street high level, Edge Hill, Wavertree Technology Park, Broad Green,
  Mossley Hill and West Allerton are not drawn, nor the high-level platforms
  at Liverpool South Parkway and Hunts Cross (those two stations are drawn
  as Merseyrail stations). The exclusion reason carries `15-minute`.
- **Intercity and regional services** (Avanti, TfW, EMR, Northern's other
  routes): not drawn.
- **No other urban rail in the area**: no tram, no metro. Coverage, the
  third part of the rail test, passes trivially: Merseyrail is the network
  (Porto Alegre's Trensurb shape).

### Spacing — asserted, measure at build

General-knowledge distances, not measured: nearest-station gaps of about
0.5 km on the loop, 0.6-1.0 km on the Kirkdale, Walton, Orrell Park, Rice
Lane and Bank Hall cluster, 1.0-1.6 km on the Hunts Cross branch, about 2 km
at Fazakerley. A city median of about 0.9-1.0 km (DART's and Copenhagen's
territory); the regional median likely 1.2-1.5 km, the widest stretch
Hightown to Formby. **Measure it at step 1** (`uk.py` prints the median gap
against `config.MEDIAN_GAP_BOUNDS_M`), record it with the exception's row in
`docs/commuter_rail_list.md`, and take the ring edges from
`docs/ring_rules.md` (standard rings at these gaps).

### Stations

- **Liverpool (17):** Northern Line: Hunts Cross, Liverpool South Parkway,
  Cressington, Aigburth, St Michaels, Brunswick, Liverpool Central,
  Moorfields, Sandhills, Bank Hall, Kirkdale, Walton, Orrell Park, Rice Lane,
  Fazakerley. Wirral Line: James Street and Lime Street (low level), with
  Moorfields and Central shared.
- **Sefton (17):** Bootle Oriel Road, Bootle New Strand, and the Southport
  line from Seaforth and Litherland to Southport; Aintree, Old Roan, Maghull
  and Maghull North on the Ormskirk branch. **Aintree is in Sefton**, not
  Liverpool.
- **Knowsley (2):** Kirkby and Headbolt Lane (opened 2023: check OSM carries
  it).
- **Wirral (23):** the screen's count, by general knowledge; gate 3 confirms
  it.

### Building it on `pipeline/countries/uk.py`

The shared step 1 was written for trams and light rail. What changes, on
measurable grounds (the build session's call, as Manchester's pilot was);
the six built UK cities' drift check must stay clean afterwards:

- **Selection:** `config.OSM_ROUTES = ("train",)`, and the one Overpass query
  keyed on the network (likely `network=Merseyrail`; verify the tagging) or
  the two lines by name, **never every `route=train` in the box** (the
  `osm-rail` skill, Taichung's lesson; London's: Overground and Elizabeth
  relations are tagged `network=National Rail`, so select by name where the
  network tag fails). Every train relation the query does return is KEPT or
  named in `config.NOT_DRAWN` with a reason (uk.py exits otherwise); the City
  Line's relations go there with `15-minute`.
- **Lines:** two drawn lines, "Northern Line" and "Wirral Line", each with a
  permanent label and a legend entry; colours from OSM checked against
  Merseyrail's own map. Branch relations collapse by London's branch rule
  (`config.LINE_OSM_REFS`). **The Wirral Line's city-centre loop is one-way**
  (James Street, Moorfields, Lime Street, Central): check it is drawn once.
  The Northern Line trunk carries three branches: drawn once.
- **Gate 3, twice:** Merseyrail's station count (operator page, or the
  timetable booklets) and **NaPTAN**. Merseyrail's stations are rail access
  nodes, **stop type RLY in ATCO area 910**, not MET in 940: `uk.py`'s
  `naptan_gate` filters `StopType == "MET"`, so the stop type becomes config.
  The Department for Transport, NaPTAN licence row (notice 86) covers the same dataset; its rendered text
  says "the UK's tram and light-rail maps", so extending it to Liverpool is
  a wording proposal for the owner (or a notice of its own).
- **The light-rail track print** (share tagged light_rail or tram) will read
  near zero on heavy rail: expected, not a failure. Say so in config.
- **The exception is recorded** in `docs/commuter_rail_list.md` (a new row,
  with spacing, frequency and coverage) and in the rail section of
  `docs/excluded_categories.md`, so `check_scope_disclosure.py` sees both
  halves.

---

## Business leg — the FSA register (FHRS), four councils

Measured 2026-10-03 on the FSA API (`api.ratings.food.gov.uk`, header
`x-api-version: 2`, the Authorities list and the Establishments paging
counts); file sizes from a HEAD request the same day.

| Council | Code | Total | Restaurant/Cafe | Takeaway | Pub/bar | Retailers - other | Supermarkets | **Storefronts** | Bulk XML | Published |
|---|---|---|---|---|---|---|---|---|---|---|
| Liverpool | 414 | 4,621 | 1,043 | 759 | 523 | 996 | 130 | **3,451** | 4,469,803 B | 2026-10-02 |
| Sefton | 424 | 2,394 | 542 | 267 | 255 | 550 | 68 | **1,682** | 2,300,580 B | 2026-10-02 |
| Knowsley | 412 | 822 | 154 | 109 | 60 | 172 | 22 | **517** | 823,485 B | 2026-10-02 |
| Wirral | 435 | 2,342 | 590 | 341 | 220 | 503 | 96 | **1,750** | 2,353,672 B | 2026-10-02 |
| **Four councils** | | **10,179** | | | | | | **7,400** | **9,947,540 B** | |

Out of scope by type, as everywhere on the FSA register (Liverpool's
figures): Other catering 436, Hospitals/Childcare/Caring 232,
School/college/university 198, Mobile caterer 160, Hotel/B&B 88,
Manufacturers/packers 27, Distributors/Transporters 25, Importers/Exporters 4.

- **Download:** four XMLs,
  `https://ratings.food.gov.uk/OpenDataFiles/FHRS<code>en-GB.xml` for 414,
  424, 412 and 435, 9,947,540 bytes, keyless. Named here, so the build
  fetches them without asking (CLAUDE.md, 2026-09-30), with their licence row
  and notice.
- **Currency:** every file republished 2026-10-02; the register lists
  premises currently registered, so the one-clock rule passes. About half the
  sampled rating dates are 2023 or later.
- **Placement:** 94.3% of Liverpool's storefronts carry the FSA's point (a
  930-row sample, one 200-row page per storefront type, the API's default
  order, not random: takeaways 99.5%, cafes 95.5%, retail 92.5%, pubs 92.0%,
  supermarkets 90.8%), in the UK six's 94-98% band. **Sefton's all-type
  sample is lower (75.3%)**: measure its storefronts from the full file.
  Rows without a point but with a full postcode go to Code-Point centroids;
  outward-code-only rows are private addresses and are never placed.
- **Code-Point Open:** London's file, edition 2026-08, copied from
  `data/london/raw/codepo_gb.zip`, not downloaded again (the UK six's
  `uk_fetch.copy_codepoint`), units kept to the four GSS codes.
- **The flat and childminder rules** apply unchanged: 0 flat addresses in the
  930 sampled storefront rows.
- **Count check:** Liverpool's 3,451 storefronts sit beside Sheffield's 3,447
  (similar populations).

### Licence and notices — nothing new to read

- **FSA register:** OGL v3 with the FSA's conditions, London's reading
  (notice 58) and the UK six's: a notice of its own per city with London's
  credit, "Food Standards Agency, UK food hygiene rating data" (Newcastle's
  precedent, notice 62). Its row in `docs/data_sources/united-kingdom.md`
  and its entry in `docs/data_sources.md`, as Manchester's notice 84.
- **The notice's wording**: Newcastle's notice 62 as rendered for Manchester
  (notice 84), with the city and the extract date changed:
  "Liverpool's food businesses are from the Food Standards Agency, UK food
  hygiene rating data, extracted on `<date>`. Contains public sector
  information licensed under the Open Government Licence v3.0. Modified by
  this project: storefront types selected, premises at a flat address left
  out, premises without a location placed at their postcode's center, or
  left out where they have no full postcode, and trade names shown where a
  business is registered under another name. No hygiene rating is shown.
  The Food Standards Agency does not endorse this map." (the licence title
  linked to the OGL v3 page, as in notice 84).
- **Code-Point Open:** OGL v3, London's three statements verbatim, a notice
  of its own (Manchester's notice 85 with the city changed): "Contains
  Ordnance Survey data © Crown copyright and database right 2026. Contains
  Royal Mail data © Royal Mail copyright and database right 2026. Contains
  National Statistics data © Crown copyright and database right 2026."
- **NaPTAN:** the Department for Transport, NaPTAN notice 86 (OGL v3.0), the wording question above.
- **OpenStreetMap:** the rail is OSM data (ODbL, notice 1).

### No second bucket

Enumerated at the screen, 2026-10-03:

- **data.gov.uk** (`organization:liverpool-city-council`): 21 datasets in
  full, planning and GIS layers (Main Retail Core, alcohol zone, Article 4,
  sites for business development); no premises list.
- **Data Mill North** (publisher Liverpool City Council): 10 datasets,
  transparency-code items (spending, contracts, land and building assets,
  2017); no premises list.
- **liverpool.gov.uk:** transparency (spending only) and key statistics
  (aggregates). **The Licensing Act premises register is a search page
  only**, no bulk list (Westminster's lookup-only shape), and alcohol-only in
  any case.
- **Business rates:** no published list (old FOI responses only). The VOA
  rating list is out on its terms (London, 2026-09-28).
- **Not enumerated:** Sefton's, Knowsley's and Wirral's own catalogues. A
  second bucket missing from the core city decides the page either way; the
  page says food only, as the UK six's do.

---

## Downstream

When the build pushes, Visuals and Analytics are told
(`docs/session_roles.md`, "Downstream sessions"). **For each notice it adds**
(the FSA's, Code-Point Open's, and NaPTAN's if extended), **the build
records in its drafts file whether the notice belongs on a card's face or in
a caption only**, decided by the licence's own words on where it must
appear, and **any open terms question** (none known: the FSA, OS and NaPTAN
readings are settled). It also names the downstream inputs the branch
changes: a new city, its `outputs/liverpool/`, the city registry, the
notices, a licence row, and, if `uk.py` changes, shared pipeline code.

## What remains for the build

- 🚨 **`uk.py` on heavy rail**: the `route=train` selection, NaPTAN's RLY
  stop type in area 910, and the six built UK cities still clean in the
  drift check.
- ⚠️ **Gate 3's operator count** (the screen's 59 rests partly on general
  knowledge: Wirral's 23 especially) and Headbolt Lane in OSM.
- ⚠️ **Spacing and the regional median**, at step 1; the ring edges from it.
- ⚠️ **OSM tagging** of Merseyrail (network, refs, colours) in the one
  Overpass query; the GSS codes and boundary ids from the same query.
- ⚠️ **Placement from the full files**, Sefton first.
- ✅ **Mode** `metro` (owner); the NaPTAN notice is reworded (owner), its sentence
  passed on by staging once approved.
- ⚠️ **Page text:** to `docs/city_page_format.md`. The FSA bullets are
  approved (London's, Newcastle's, the UK six's); the exception's evening
  and Sunday sentence and the City Line sentence are proposals for the
  drafts file.
- ⚠️ **Personal exposure:** `check_personal_exposure.py liverpool` after
  step 2, a row in `docs/privacy_verdicts.md`, the verdict in the drafts
  file.
- `check_provenance.py` names Liverpool OK; `check_scope_disclosure.py`
  passes with the exception on both pages.

```brief-checks
[
  {
    "id": "liverpool-fsa-open-data-files",
    "claim": "The FSA's open-data page lists a bulk XML for each of the four councils Merseyrail serves (414 Liverpool, 424 Sefton, 412 Knowsley, 435 Wirral). The build downloads these, not the API",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["FHRS414en-GB.xml", "FHRS424en-GB.xml", "FHRS412en-GB.xml", "FHRS435en-GB.xml"]
  },
  {
    "id": "liverpool-fsa-terms-name-ogl",
    "claim": "THE LICENCE POSITION RESTS ON THIS PAGE, as London's does: the FHRS terms name the Open Government Licence. If it stops naming the OGL, re-read before publishing",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/terms-and-conditions",
    "present": ["Open Government Licence"]
  },
  {
    "id": "liverpool-fsa-open-data-names-region",
    "claim": "The same page names the four councils and the North West region the FSA files them under, which is why the scope is selected by code, never by region",
    "kind": "http_contains",
    "url": "https://ratings.food.gov.uk/open-data",
    "present": ["Liverpool", "Sefton", "Knowsley", "Wirral", "North West"]
  },
  {
    "id": "liverpool-fsa-knowsley-file",
    "claim": "The smallest of the four bulk files, Knowsley's (code 412), resolves keyless at the named URL as XML of about 823,485 bytes (HEAD, 2026-10-03)",
    "kind": "http_ok",
    "url": "https://ratings.food.gov.uk/OpenDataFiles/FHRS412en-GB.xml",
    "min_bytes": 700000,
    "content_type_contains": "xml"
  },
  {
    "id": "liverpool-projected-crs",
    "claim": "Liverpool's projected CRS is UTM 30N (EPSG:32630), as the built UK cities'",
    "kind": "utm_zone_from_longitude",
    "lon": -2.9916,
    "expect": "EPSG:32630"
  }
]
```
