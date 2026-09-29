# Sydney (City of Sydney) — build brief

**Re-probed and screened 2026-09-28 (staging); Band B, scoped to the City of
Sydney (owner). Brief written the same day, with the licence read.** Run
`python scripts/brief_check.py sydney` before writing any code. The trail:
`DECISIONS.md` 2026-09-28 "Moved Sydney into Band B, scoped to the City of
Sydney", and "Melbourne and Sydney briefs written".

> **Measured at the build, 2026-09-28 (build session, `worktree-sydney`)** -
> these supersede the screen's figures below where they differ:
> - **Five more classes sit in the storefront divisions** than the brief's
>   prefixes reached: religious services (9540, 144), interest-group,
>   professional and labour associations (955x, 249) - excluded as
>   organisations, NAICS 813's precedent - and licensed members' clubs (4530,
>   27, owner: out). The taxonomy lists every class; a new one stops step 2.
> - **Owner's calls**: catering (4513) and funeral services (9520) out,
>   the two n.e.c. catch-alls kept, light rail left out but disclosed, region
>   "Oceania", the licence read's credit as notice 64.
> - **7,328 storefronts** (Retail 3,091, Food service 3,234, Personal services
>   1,003) after 27 points outside OSM's LGA polygon; 5,218 distinct points.
>   **83.5% within a ring** (6,120).
> - **Superseded the same day (owner, on Melbourne's evidence)**: 9539 other
>   personal services n.e.c. excluded, so **7,074 storefronts** (Personal
>   services 749), **83.4% within a ring**.
> - **Stations**: OSM's stop names spell the platform three ways ("Central,
>   Platform 16", "Campbelltown Platform 2", "Gadigal 1"); normalised, the
>   route-membership stations inside the LGA are exactly the brief's 16.

⚠️ **All three buckets, one LGA, and no names.** The page covers the City of
Sydney only (the CBD, Central, Redfern, Green Square, Kings Cross,
Pyrmont), disclosed. Pins carry a business class, never a name: the survey
publishes none.

---

## The one-line summary

**A council floor-space survey with one point per business establishment
and an ANZSIC class, CC BY 4.0: about 7,400-7,500 storefronts in 2022, 83.2%
within 0.6 mi of the 16 train and Metro stations in the LGA. The work is the
taxonomy, points stacked per building, a 2022 snapshot, and the light-rail
call.**

---

## Business leg — FES "Industry of occupation"

| | |
|---|---|
| **Source** | City of Sydney, Floor Space and Employment Survey (FES), ArcGIS item `77ac8aa96bd34bacb881cfe8e5358ba0`: `services1.arcgis.com/cNVyNtjGVZybOQWZ/arcgis/rest/services/FES_Industry_of_occupation/FeatureServer/0` |
| **Rows, 2022** | **21,618** (equal to the FES2022 block total); 2007, 2012 and 2017 are in the same layer, filter `Year='2022'` |
| **Storefronts** | the screen's split: retail **3,110**, food **3,304** (cafés and restaurants 2,227, takeaway 650, pubs 379), personal services **980** (hair and beauty 644, laundry 82) = 7,394. The prefix filter ANZSIC 39-43, 451-452, 951-953 gives **7,497**; the taxonomy settles the 103 between them (below) |
| **Fields** | `OBJECTID`, `ID`, `Key_`, `DivisionCode`/`Name`, `SubDivisionCode`/`Name`, `GroupCode`/`Name`, `ClassificationCode`/`Name`, `IndustryCode`/`Name`, `CityBasedIndustry`, `Year`, `Village` |
| **Names, addresses** | **None**: stripped by the publisher |
| **Currency** | A survey every five years; 2022 is the latest. The page states the year |

**The download** is paged queries of the feature service (2,000 rows a page;
the 2022 rows are about 11 pages). It is not a file, but it is still a
fetch: `fetch_sources.py`, with the owner's OK.

### ⚠️ Points are per building, not per shop

21,618 points on **12,334 distinct coordinates** (to 1 m): 47.9% alone,
27.4% in stacks of 10 or more, the largest 163 (99 of them retail: a
shopping centre). The storefront classes: 7,497 on 5,426 coordinates. Ring
counts are unaffected; the map display is Melbourne's question too.

### ⚠️ Traps to settle in the taxonomy (`premises-taxonomy`)

- **Brothel keeping (ANZSIC 9534, 27 in 2022) is excluded (owner,
  2026-09-28)**, and the exclusion goes in `docs/excluded_categories.md` at
  the build.
- **Classes inside the prefixes that may not be storefronts**: motor vehicle
  retail (39), fuel (400), funeral services (952) and parking (9533). These
  are the likely source of the 103 between 7,394 and 7,497. Decide each one,
  then measure.
- **The n.e.c. catch-alls** (9539 and each group's 9 class) first, with
  `taxonomy_catchall`, then `check_personal_exposure.py sydney`. With no
  names, exposure is low: a class at a building. Home businesses are the
  question to check.

---

## Licence — read 2026-09-28 (`licence-read`): PERMITTED WITH CONDITIONS, CC BY 4.0

- **The grant**: the item's `licenseInfo` links CC BY 4.0, and
  `accessInformation` reads "City of Sydney". The data hub's Disclaimer says
  data products are "published under Creative Commons licences" with the
  licence "specified in the 'Licence' section of the data description".
  Data.NSW's harvested copy says "License Not Specified", a harvester
  failure; the publisher's item governs.
- **Must display** (CC BY §3(a)(1)): "City of Sydney" as creator and
  copyright holder, the licence with a link, a link to the dataset, a note
  that the data was modified, and the warranty disclaimer. **No wording is
  prescribed.** The read's draft, for the owner: "Business establishment
  locations: City of Sydney, Floor Space and Employment Survey (FES Industry
  of occupation), © City of Sydney, CC BY 4.0 [links]. Modified by this
  project (filtered and grouped by category); provided as is, without
  warranty."
- **Must not**: imply endorsement or official status (CC BY §2(a)(6));
  present the data as accurate, current or complete on the City's authority
  (the Disclaimer: "as is", no warranty of "accuracy, timeliness,
  completeness").
- **Must do**: nothing. Emailing opendata@cityofsydney.nsw.gov.au is an
  invitation.
- 🟡 **One flag for the owner**: the main website's terms
  (`cityofsydney.nsw.gov.au/terms-conditions`) say content "must not be …
  republished except with the written authorisation of the City", and use
  the word "data". The read judged them **not applicable**. They are written
  for that website's pages, the data is served from other hosts, and nothing
  on the data hub links to or incorporates them, while the hub assigns
  Creative Commons licences to data. This is not Philadelphia's shape (terms
  incorporated by reference). Noted, not a blocker.

A `docs/data_sources/australia.md` file is created by whichever of Melbourne
and Sydney is built first.

---

## Rail — OpenStreetMap, measured 2026-09-28

**16 train and Metro stations inside the City of Sydney** (OSM
`railway=station` inside relation 1251066): Central, Town Hall, Wynyard,
Circular Quay, St James, Museum, Martin Place, Kings Cross, Redfern, Green
Square, Erskineville, Macdonaldtown, Newtown, and the Metro's Barangaroo,
Gadigal and Waterloo (Central and Martin Place are shared).

- **Networks**: Sydney Trains **T1, T2, T3, T4, T8, T9** (20 relations), and
  Sydney Metro **M1** (2 relations; the City section opened 2024). NSW
  TrainLink and interstate services stay out.
- 🚨 **The rail-shape call: Sydney Trains is suburban rail**, Berlin's S-Bahn
  test again. Through the CBD (the City Circle, the Eastern Suburbs line) it
  runs as a metro. **The recommendation is every Sydney Trains and Metro
  station in the LGA**, lines drawn to the boundary.
- ⚠️ **Edge stations**: Newtown, Macdonaldtown and Erskineville sit near the
  Inner West boundary. They are inside by OSM's centre; the boundary rule
  decides.
- **Light rail: L1, L2, L3 (6 relations), 22 stops in the LGA.** They add
  9.8 points (83.2% → 93.0%), more than Melbourne's trams (2.6). **The
  recommendation is still to leave them out**, Berlin's precedent (it left
  out 6.9 points). The L2/L3 George Street line is a modern light rail on
  street, and this call is the owner's.
- **Colours**: `line_colour_search.py sydney`, with Transport for NSW's line
  colours as hues.

**Ring coverage** (0.6 mi, the 7,497 storefront-class points, EPSG:32756):
trains + Metro **83.2%** (6,240) · + light rail 93.0% (6,972).

Rail from OSM needs no further licence. Transport for NSW's GTFS needs an API
key (a free account, the owner's to hold) and is not needed.

---

## Scope, CRS, region

- **Scope:** City of Sydney LGA, OSM relation **1251066** (`admin_level=6`,
  Wikidata Q1094194), disclosed on the page.
- **CRS:** GDA2020 / MGA zone 56 (EPSG:7856; the layer's own points are
  MGA56), or UTM 56S (EPSG:32756).
- **Region:** a new value, `"Oceania"` (owner call, with Melbourne).

## Still unknown

- 🚨 **Owner calls**: light rail in or out (out recommended); the credit
  wording; the website-terms flag noted.
- ⚠️ **The taxonomy**: the four classes above and the catch-alls.
- ⚠️ **Stacked pins**: the display.
- ⚠️ **Placement check**: the points are the publisher's; spot-check a few
  against OSM buildings.
- ⚠️ **The fetch OK** (paged service queries, about 11 pages).

```brief-checks
[
  {
    "id": "sydney-fes-layer",
    "claim": "The FES Industry of occupation layer is a point layer carrying ANZSIC class codes, the survey year and the village",
    "kind": "arcgis_layer",
    "url": "https://services1.arcgis.com/cNVyNtjGVZybOQWZ/arcgis/rest/services/FES_Industry_of_occupation/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "present": ["ClassificationCode", "ClassificationName", "Year", "Village"]
  },
  {
    "id": "sydney-fes-2022-rows",
    "claim": "The 2022 survey holds 21,618 business establishments in the layer",
    "kind": "http_contains",
    "url": "https://services1.arcgis.com/cNVyNtjGVZybOQWZ/arcgis/rest/services/FES_Industry_of_occupation/FeatureServer/0/query?where=Year%3D%272022%27&returnCountOnly=true&f=json",
    "present": ["\"count\":21618"]
  },
  {
    "id": "sydney-fes-licence",
    "claim": "THE LICENCE POSITION RESTS ON THIS ITEM: its licenseInfo links CC BY 4.0 and its credit is City of Sydney. If it changes, re-read before publishing",
    "kind": "http_contains",
    "url": "https://www.arcgis.com/sharing/rest/content/items/77ac8aa96bd34bacb881cfe8e5358ba0?f=json",
    "present": ["creativecommons.org/licenses/by/4.0", "City of Sydney"]
  },
  {
    "id": "sydney-osm-metro-and-light-rail",
    "claim": "OSM carries Sydney Metro M1 and light rail L1-L3 in the City of Sydney bbox",
    "kind": "osm_route_refs",
    "bbox": [-33.925, 151.170, -33.855, 151.235],
    "routes": ["subway", "light_rail"],
    "require_refs": {"subway": ["M1"], "light_rail": ["L1", "L2", "L3"]}
  },
  {
    "id": "sydney-projected-crs",
    "claim": "Sydney's derived UTM zone is 56S (EPSG:32756)",
    "kind": "utm_zone_from_longitude",
    "lon": 151.2093,
    "north": false,
    "expect": "EPSG:32756"
  }
]
```
