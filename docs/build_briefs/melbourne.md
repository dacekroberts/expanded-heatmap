# Melbourne (City of Melbourne) — build brief

**Screened 2026-09-28 (staging, the large-transit gap's re-screen); Band B,
scoped to the City of Melbourne (owner). Brief written the same day, with
the licence read.** Run `python scripts/brief_check.py melbourne` before
writing any code. The trail: `DECISIONS.md` 2026-09-28 "Moved Melbourne into
Band B, scoped to the City of Melbourne", and "Melbourne and Sydney briefs
written".

⚠️ **All three buckets, one municipality.** No other Victorian council
publishes a register, so the page covers the City of Melbourne only (the CBD,
Docklands, Southbank, Carlton, North Melbourne, Parkville, Kensington), and
says so the way Tokyo's page names its wards.

---

## The one-line summary

**A council census with trading names, ANZSIC classes and coordinates under
CC BY 4.0: 5,456 storefronts in 2024, 96.5% of them within 0.6 mi of the 20
train stations inside the municipality. The work is the taxonomy (ANZSIC,
catch-alls), points that are per building rather than per shop, and the
trams call.**

---

## Business leg — CLUE, "Business establishments location and industry classification"

| | |
|---|---|
| **Source** | City of Melbourne, Census of Land Use and Employment (CLUE), on `data.melbourne.vic.gov.au` (Opendatasoft), dataset `business-establishments-with-address-and-industry-classification` |
| **Rows, 2024** | **19,672** establishments (all industries; the census runs 2002-2024 in one table, filter `census_year=date'2024'`) |
| **Storefronts** | **5,456**: retail (ANZSIC 39-43) 1,870 · food (451-452) 2,685 · personal services (951-953) 901, of which hair and beauty 425 and laundry 32 |
| **Fields** | `census_year`, `block_id`, `property_id`, `base_property_id`, `clue_small_area`, `trading_name`, `business_address`, `industry_anzsic4_code`, `industry_anzsic4_description`, `longitude`, `latitude`, `point` |
| **Names** | `trading_name` on every row |

**The download** is one CSV export of the whole table (every year). It is
unmeasured and **needs the owner's OK**. A `where` on 2024 through the API
export would take only the year the page uses.

### ⚠️ Points are per building, not per shop

Grouped server-side by coordinate (2026-09-28):

| | Rows | Distinct points | Alone | In stacks of 10+ | Largest stack |
|---|---|---|---|---|---|
| All 2024 | 19,672 | 4,418 | 13.3% | 61.6% | 260 |
| Storefront classes | 5,456 | 1,919 | 22.3% | 39.8% | 221 |

The point is the property's, shared by every tenancy in it (grouping by
`property_id` gives nearly the same result). Ring counts are unaffected at
966 m. **The map is**: a shopping centre renders as one pin with 221
storefronts under it. Sydney has the same shape; the build decides the
display (a stacked-pin note, or a jitter that the page discloses).

### ⚠️ Traps to settle in the taxonomy (`premises-taxonomy`)

- **Measure the catch-all share first** (`brief_check.py`'s
  `taxonomy_catchall`). **9539 "other personal services n.e.c." (279 rows)**
  is the personal-exposure check's first target.
- **Upper-floor suites** (legal, consulting) fall outside 39-43, 451-452 and
  951-953, so they filter out on ANZSIC. No floor field is needed.
- **Questions inside the prefixes**: motor vehicle retail (39), fuel (400),
  funeral services (952), parking (9533) and brothels (9534) are not obvious
  storefronts. Brothel keeping is excluded in Sydney (owner, 2026-09-28), and
  the same exclusion belongs here.
- **Vacancies**: the screen found 27% of 2024 tenancies vacant. Whether any
  vacant tenancy appears in this table (a vacancy class, or a blank trading
  name) is unmeasured; check it in step 2.

---

## Licence — read 2026-09-28 (`licence-read`): PERMITTED WITH CONDITIONS, CC BY 4.0

- **The grant**: the portal's "About our data" says the open data is under a
  Creative Commons licence, "free to share and adapt our data for any
  purpose, provided you give the appropriate credit", linked to CC BY 4.0.
  The dataset metadata says `license: "CC BY"`, with the 4.0 legal code.
- **DataVic's "other-open" is not a conflict.** It is CKAN's generic bucket,
  and the same DataVic record carries `custom_licence_text = "CC BY"` with
  the 4.0 link. The council's portal governs.
- **Nothing is incorporated by reference.** The portal's terms page reads
  "The Terms and Conditions of this domain have not been defined yet."
  `melbourne.vic.gov.au/copyright` covers the website, not the data portal.
- **Must display**: a credit, the licence with a link, a link to the
  dataset, and **a note that the data was modified** (required by CC BY
  §3(a); filtering and bucketing are modifications). **No wording is
  prescribed** (`attributions: null`). The read's draft, for the owner:
  "Business establishments: City of Melbourne, Census of Land Use and
  Employment (CLUE) [dataset link], CC BY 4.0 [link]. Filtered, categorised
  and aggregated by this project."
- **Must not**: imply endorsement (CC BY §2(a)(6)); use DataVic's "©
  Copyright State Government of Victoria", which is for DataVic's own
  material.
- **Must do**: nothing. "#melbdata" is an invitation, not a condition.
- **Privacy is not licensed** (CC BY §2(b)(1)), so the project's rule still
  applies. The council promised census respondents that published data would
  not give "any details about individual businesses other than what is
  publicly available". DataVic flags `personal_information = "no"`. Neither
  replaces `check_personal_exposure.py`.
- **Not opened** (files, by the no-download rule): `CLUE_Definitions.pdf`, the
  council's privacy policy PDF, the Open Data Principles DOC.

A `docs/data_sources/australia.md` file does not exist yet. The build creates
it (first Australian city), with this read's result.

---

## Rail — OpenStreetMap, measured 2026-09-28

**20 train stations inside the City of Melbourne** (OSM `railway=station`
inside relation 2404870): Flinders Street, Southern Cross, Flagstaff,
Melbourne Central, Parliament, Jolimont, North Melbourne, Macaulay,
Flemington Bridge, Royal Park, Kensington, South Kensington, Showgrounds,
Flemington Racecourse, Richmond, and the Metro Tunnel's Arden, Parkville,
State Library, Town Hall and Anzac. The screen said about 12-15; the Metro
Tunnel accounts for most of the difference.

- **Network**: `PTV - Metropolitan Trains`, 111 relations touching these
  stations, with refs that are line codes and direction strings (`SUY =>
  EPH`, `CBE => WFY`; 32 distinct). Collapse them to the named lines (about 16
  by general knowledge, unmeasured). **Colours and names need `line_colour_search.py`** and PTV's
  public line names.
- 🚨 **The rail-shape call: this is suburban rail**, the Berlin S-Bahn test's
  case. Inside the municipality it runs as a metro (the City Loop, the Metro
  Tunnel), so **the recommendation is to keep every train station in scope**,
  cut at the municipal boundary, with the lines drawn only as far as the
  boundary.
- ⚠️ **Richmond** sits on the boundary (Punt Road); OSM's station centre falls
  inside. It changes coverage by 0.0 points; keep or drop on the boundary
  rule the build writes.
- **Trams: 22 routes, 155 stop names (279 nodes) in the municipality.**
  Adding them raises coverage from 96.5% to 99.1%. **The recommendation is to
  leave them out**, Berlin's and London's precedent: +2.6 points for 155
  stops. Regional (V/Line) and interstate services stay out.

**Ring coverage** (0.6 mi, the 5,456 storefront-class points, EPSG:32755):
trains **96.5%** (5,266) · trains + trams 99.1%.

Rail from OSM needs no further licence (ODbL, already credited on every
map). PTV's GTFS (DataVic, CC BY 4.0) is the alternative if OSM's line
geometry proves messy.

---

## Scope, CRS, region

- **Scope:** City of Melbourne LGA, OSM relation **2404870** (`admin_level=6`,
  Wikidata Q1919098), disclosed on the page.
- **CRS:** GDA2020 / MGA zone 55 (EPSG:7855), or UTM 55S (EPSG:32755),
  derived from the longitude. Never buffer in 4326.
- **Region:** a new value, since no Oceania city exists yet: `"Oceania"`
  (owner call, with Sydney).

## Still unknown

- 🚨 **Two owner calls**: trains only (recommended) or with trams; the credit
  wording.
- ⚠️ **The download**: size, and whether to take 2024 only.
- ⚠️ **The taxonomy**: catch-alls, and the classes inside the prefixes above.
- ⚠️ **Stacked pins**: how the map shows 221 storefronts at one point.
- ⚠️ **Personal exposure**: `check_personal_exposure.py melbourne` after
  step 2, 9539 first.
- ⚠️ **The page region value** (above).

```brief-checks
[
  {
    "id": "melbourne-clue-licence-and-fields",
    "claim": "THE LICENCE POSITION RESTS ON THIS METADATA: the CLUE business-establishments dataset declares CC BY (4.0 legal code) and carries trading names and ANZSIC4 codes. If it stops declaring CC BY, re-read before publishing",
    "kind": "http_contains",
    "url": "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/business-establishments-with-address-and-industry-classification",
    "present": ["CC BY", "licenses/by/4.0", "trading_name", "industry_anzsic4_code", "census_year"]
  },
  {
    "id": "melbourne-clue-2024-rows",
    "claim": "The 2024 census year holds 19,672 establishments, all industries",
    "kind": "http_contains",
    "url": "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/business-establishments-with-address-and-industry-classification/records?where=census_year%3Ddate%272024%27&limit=0",
    "present": ["\"total_count\": 19672"]
  },
  {
    "id": "melbourne-osm-trams",
    "claim": "OSM carries Melbourne's tram network as route=tram relations in the City of Melbourne bbox (the trams call rests on it)",
    "kind": "osm_route_refs",
    "bbox": [-37.851, 144.897, -37.775, 144.991],
    "routes": ["tram"],
    "require_refs": {"tram": ["1", "11", "19", "35", "86", "96", "109"]}
  },
  {
    "id": "melbourne-projected-crs",
    "claim": "Melbourne's derived UTM zone is 55S (EPSG:32755)",
    "kind": "utm_zone_from_longitude",
    "lon": 144.9631,
    "north": false,
    "expect": "EPSG:32755"
  }
]
```
