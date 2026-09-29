# Buffalo — build brief

**Step 0 measured 2026-09-28 (wave 2's US screen), 2026-09-29 (the
light-rail test) and 2026-09-29 (this brief).** Run
`python scripts/brief_check.py buffalo` before writing code.

---

## The one-line summary

**One light-rail line, New York's multi-source pattern, and a licence file
whose "Active" means nothing.** Every one of the city's 12,131 licences says
`Active`, and **42.8% of the rows in the bucket codes are past their expiry
date**. Chicago's precedent, dropping expired rows at the fetch date, halves
the screen's food figure. What is left is a thin map, with an honest 22% of
storefronts inside the rings. No blocker: one owner call, the rail source, has a recommended way round.

| | |
|---|---|
| Rail | NFTA **Metro Rail**, one line, **14 stations, all inside the city**; 80% tunnel or bridge; **every 20 min, flat 06–23** (disclosed, the light-rail test's rule for purpose-built track) |
| Storefronts inside the city (before cross-source dedupe) | **~1,670**: retail ~909 · food ~462 · personal services ~298 |
| In the 0.6 mi ring | **22.4%** (374), between Edmonton (22.2%) and San Diego (24.4%) |
| Rings | **standard 0.1 / 0.2 / 0.3 / 0.6 mi** (594 m median gap) |
| Projected CRS | **EPSG:32617** (UTM 17N, 78.87° W) |
| Region | `"North America"` |

---

## ✅ Rail — NFTA's rail GTFS

`https://metro.nfta.com/__googletransit/rail/google_transit.zip`: a small
rail-only feed. `feed_info` declares **2026-08-27 to 2026-12-05** (version
`26FALL`), so **fetch fresh at build**. It will have rolled to a winter
feed by then.

| | |
|---|---|
| Route | one, `route_id 145`, "Metro Rail", **`route_type 0`**, no `route_color` |
| Platforms | 28 stop rows, **no `parent_station`, no `location_type`** → collapse by name |
| Stations | **14**, all inside the city boundary: DL&W, Canalside, Seneca, Church St, Lafayette, Fountain Plaza, Allen-Medical Campus, Summer-Best, Utica, Delavan-Canisius College, Humboldt, Amherst, LaSalle, University |
| Median gap | **594 m** by name (the test's OSM read: 609 m) |
| Shapes | present |
| Frequency | 3 trips an hour each way, 07–19 and 19–22 (the audit's read of this feed) |

- **Colour**: OSM's two route relations (3517747, 11364343) carry
  **`#004990`** (network NFTA, ref `Metro`). Use it, through
  `pipeline/linecolour.py`.
- **Name**: "Metro Rail" is its public name. The legend and label read
  **"NFTA Metro Rail"**, and the page calls it light rail, never metro or
  subway, **with the 20-minute service disclosed** (owner, 2026-09-29).
- **Licence: READ 2026-09-29 (the `licence-read` agent) — PERMITTED WITH
  CONDITIONS, and one condition is an owner call.** NFTA's "General Transit
  Feed Specification (GTFS) License Agreement" at
  `https://metro.nfta.com/about/developer-tools` grants "non-exclusive,
  limited, and revocable rights to use, reproduce, and redistribute NFTA
  Data". It is accepted by use, with no click-through. **Nothing must be
  displayed and nothing must be done.** It has an as-is disclaimer,
  revocable-at-any-time and entire-agreement clauses, and New York law.
  `feed_info` declares no licence; the Mobility Database (tld-6748) and
  Transitland both point back to this page.
  - 🟠 **The trademark clause**: *"NFTA trademarks and copyrighted
    materials, including any confusingly similar variants, may not be used
    in association with the Data."* It names no marks. **The reading that
    permits us**: the line's public name and NFTA as the credited source are
    the Data's own text (`route_long_name` "Metro Rail", `agency_name` "NFTA -
    Metro"), not branding, so no logos and no official look. **The reading
    that does not**: if "NFTA" or "Metro Rail" are marks, a permanent
    "NFTA Metro Rail" label beside the drawn Data is literally that use, and
    the project's invariant requires that label. The agent did not settle
    which marks NFTA claims (no USPTO search; the unincorporated
    `branding_guidelines.pdf` was not opened). **This is Angers's shape, in a
    milder form.**
  - **The way around it: draw the rail from OpenStreetMap** (the `osm-rail`
    skill; Copenhagen's and Aarhus's precedent). OSM's two relations
    (3517747, 11364343) carry the geometry, the 14 stops (609 m median, the
    light-rail test's read) and the name "NFTA Metro Rail" under ODbL, so the
    NFTA agreement never binds the map. The feed is then only the frequency
    source for the page's 20-minute disclosure. **Recommended**: it removes
    the call rather than deciding it. The owner may instead accept the
    permissive reading and use the feed.
  - Re-read the page before each republish: the agreement is revocable and
    can change "at any time".
- **Boundary**: the city's own `p4ak-r4fg` "City Boundary" (Socrata, public
  domain), one feature, **104.6 km²** in UTM 17N.

---

## ✅ Business leg — three registers, New York's pattern

### 1. The city's Business Licenses — `qcyy-feh8`, data.buffalony.gov, public domain

12,131 rows, rows updated 2026-09-25, `latitude` / `longitude` on 100%.
**It is a regulated-activity list** (elevators 2,935, fuel devices 1,182,
amusement shows 1,004), so the keep-list is short:

| Bucket | Codes (`descript`) | Rows | **Unexpired** |
|---|---|---|---|
| Food | Restaurant 908, Restaurant Take Out 460, Restaurant / Dance 71, Bakers and Confectioners 45, Caterer 40 | 1,524 | **763** |
| Retail | Food Store 628, Used Car Dealer 177, Second Hand Dealer 97, Meat Fish & Poultry 81, Tobacco Hookah Vaping 16, Pawnbroker 6, Pet Shop 4 | 1,009 | **645** |
| Personal | Self-Srv Laundry / Dry Cleaner 25, Clothes-Dry Cleaners Permit 1 | 26 | **21** |
| *adjunct, never a pin* | Sidewalk Cafe 178 (a restaurant's permit, not a premises) | | |

Car dealers are kept as retail (`docs/category_rules.md` R4). Pawnbrokers
and second-hand dealers are shops.

### 🚨 `licstatus` is `Active` on 12,131 of 12,131 rows — use `expdttm`

| Expired before 2026-09-29, bucket codes | 1,171 of 2,737 (**42.8%**) |
|---|---|
| …by expiry year | 2026: 605 · 2025: 240 · 2024: 192 · 2023: 83 · 2022 and earlier: 51 |

The field exists and is complete, but it answers nothing. The oldest
"Active" restaurant expired in 2013. **Build rule: `expdttm >= fetch date`,
applied in step 2 as well as at download: Chicago's precedent**
(`pipeline/chicago/config.py`). The 605 lapsed during 2026 include renewals
in progress. A grace window would be a departure from Chicago's rule and
needs the owner. This is the leak PLAN's date-fix item (e) names for five
built cities, caught before the build.

**One premises holds several licences** (Restaurant + Sidewalk Cafe + Music).
The 1,429 unexpired rows sit on **968 distinct coordinates**. Dedupe on the
parcel (`prclid`) or the point, with food winning.

### ⚠️ The name columns are the other way round

| `businessname` | `dbaname` |
|---|---|
| DOLLAR GENERAL STORE #14886 | DOLGENCORP OF NEW YORK INC |
| GIACOBBI'S CUCINA CITTA' | JACOBBI ENTERPRISES INC. |
| DAILY FOODS HALAL MARKET | US AWESOME PRODUCTS INC. |

**`businessname` is the trade name** (blank on 0%), and **`dbaname` is
usually the legal entity** (blank on 55%). Display `businessname`. Run
`check_personal_exposure.py buffalo` at build as usual. The file has no
licensee-person column: its fields are ids, the two names, the code and
description, four dates, the parcel, the address and the coordinates, plus
census and district fields.

### 2. NYS Retail Food Stores — `9a8c-vfzj`, data.ny.gov (read for New York)

596 rows with postal city BUFFALO; **98.0% carry a `georeference` point, and
only 421 fall inside the city**. Postal "Buffalo" reaches into Cheektowaga
and Amherst. **Scope by point-in-boundary, never by `city`**: New York's rule
for its salon file, needed here for both NYS files. The file is undatable
(no date column, last refreshed 2025-09-30). That is the open owner call
PLAN item (c) raises for New York's page, and Buffalo's page states it the
same way.

### 3. NYS Appearance Enhancement and Barber businesses — `y3u4-jbgh` (read for New York)

440 postal-Buffalo rows, 99.8% georeferenced, **325 inside the city**: 199
`DOSAEBUSINESS`, 81 `DOSBARSHOPOWNER`, and **45 renters, excluded** (an
individual renting a chair; New York's rule, `docs/excluded_categories.md`).
**280 kept.** Never select `license_holder_name`.

### Totals inside the city

| | Retail | Food | Personal | All |
|---|---|---|---|---|
| City sites (unexpired, one per point) + NYS stores + NYS salons | ~909 | ~462 | ~298 | **~1,670** |

**Cross-source dedupe is still to do at build**: a city Food Store and an
NYS retail food store at one address are one shop. New York's
`SOURCE_PRIORITY` is the model. Expect retail to fall, probably by a few
hundred. The screen's "~900 / ~1,500 / 374" counted expired licences and
renters, and it is superseded by this table.

---

## Rings and share

**594 m median gap → the standard rings.** Over the ~1,670 points inside the
city:

| Within | Storefronts | Share |
|---|---|---|
| 0.1 mi | 74 | 4.4% |
| 0.2 mi | 157 | 9.4% |
| 0.3 mi | 211 | 12.6% |
| **0.6 mi** | **374** | **22.4%** |

One line up Main Street through a 105 km² city. The share is what it is, and
the page says so.

---

## Build-time calls

0. 🟠 **The owner's, before step 1: rail from OSM (recommended) or from
   NFTA's feed** under the permissive reading of its trademark clause (above).
1. **Expiry at the fetch date** (Chicago's rule, recommended), or a grace
   window (a departure; the owner's call).
2. **The dedupe key** across the three sources.
3. **The page's statements**: the 20-minute service, and the undatable NYS
   food file (whatever wording the owner settles for New York).

**Flag for the cleanup role (held macro-map work)**: Buffalo takes the
light-rail network colour.

## Still unknown

- Which marks NFTA claims (only if the owner prefers the feed to OSM).
- OSM storefront density, queued since wave 2, is no longer needed: the
  registers answer every bucket.

```brief-checks
[
  {
    "id": "buffalo-licstatus-is-uninformative",
    "claim": "Every row of the city's Business Licenses says Active - the status field cannot drop a closed business, so step 2 filters on expdttm (Chicago's rule)",
    "kind": "socrata_count",
    "domain": "data.buffalony.gov",
    "view": "qcyy-feh8",
    "where": "licstatus != 'Active'",
    "expect": 0
  },
  {
    "id": "buffalo-expired-active-bucket-rows",
    "claim": "About 1,171 bucket-code rows marked Active are past their expiry date (42.8% of 2,737 on 2026-09-29). The count grows as dates pass and shrinks as renewals land, hence the tolerance",
    "kind": "socrata_count",
    "domain": "data.buffalony.gov",
    "view": "qcyy-feh8",
    "where": "descript in('Restaurant','Restaurant Take Out','Restaurant / Dance','Caterer','Bakers and Confectioners','Food Store','Meat Fish & Poultry','Second Hand Dealer','Used Car Dealer','Pet Shop','Pawnbroker','Tobacco Hookah Vaping','Self-Srv Laundry / Dry Cleaner','Clothes-Dry Cleaners Permit','Sidewalk Cafe') AND expdttm < '2026-09-29T00:00:00'",
    "expect": 1171,
    "tolerance": 400
  },
  {
    "id": "nys-food-buffalo-postal-city-overreaches",
    "claim": "596 NYS retail food stores carry postal city BUFFALO, but only 421 lie inside the city - scope by point-in-boundary, never by the city column",
    "kind": "socrata_count",
    "domain": "data.ny.gov",
    "view": "9a8c-vfzj",
    "where": "upper(city)='BUFFALO'",
    "expect": 596,
    "tolerance": 60
  },
  {
    "id": "nfta-rail-route-type-0",
    "claim": "NFTA's rail feed has one route, Metro Rail, route_type 0",
    "kind": "gtfs_route_type_counts",
    "url": "https://metro.nfta.com/__googletransit/rail/google_transit.zip",
    "expect": {"0": 1}
  },
  {
    "id": "nfta-rail-stations",
    "claim": "28 platforms, no parent_station, 14 stations by name, median gap over 550 m (standard rings)",
    "kind": "gtfs_stations",
    "url": "https://metro.nfta.com/__googletransit/rail/google_transit.zip",
    "route_types": ["0"],
    "expect_parent_station_populated": false,
    "expect_platforms": 28,
    "expect_stations": 14,
    "crs": "EPSG:32617",
    "station_spacing_median_m_min": 550
  },
  {
    "id": "nfta-rail-feed-current",
    "claim": "The rail feed declares a current window (2026-08-27 to 2026-12-05 when read) - fetch fresh at build",
    "kind": "gtfs_feed_window",
    "url": "https://metro.nfta.com/__googletransit/rail/google_transit.zip",
    "expect": "current"
  },
  {
    "id": "buffalo-is-utm-17",
    "claim": "Buffalo (78.87 W) is in UTM zone 17N",
    "kind": "utm_zone_from_longitude",
    "lon": -78.87,
    "expect": "EPSG:32617"
  },
  {
    "id": "buffalo-city-boundary",
    "claim": "The city's own boundary layer p4ak-r4fg (public domain) serves one polygon, about 105 km2",
    "kind": "geojson_area_km2",
    "url": "https://data.buffalony.gov/resource/p4ak-r4fg.geojson",
    "crs": "EPSG:32617",
    "min": 100,
    "max": 110
  }
]
```
