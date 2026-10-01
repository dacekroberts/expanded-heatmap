# Ottawa — build brief

**Step 0 measured 2026-09-21 (the Canada screen), 2026-09-29 (the light-rail
test) and 2026-09-29 (the Band C audit; this brief).** Band B, a
reduced-bucket page (owner, 2026-09-29): **food only**. Run
`python scripts/brief_check.py ottawa` before writing code.

> **Measured at the build, 2026-09-29 (branch `ottawa`)** - these supersede
> the figures below:
> - **4,896 food premises**, not ~5,300: of 5,747 inspected since 2024-09-29,
>   597 institutional kitchens (event caterers included, R1), 83 clubs and
>   arenas, 110 mobile and event vendors and 39 hotels, B&Bs and funeral
>   homes are left out by name (owner, 2026-09-29), 14 have no point and 8 a
>   point outside the City. The brief's single-word list over-caught (SCHOOL
>   HOUSE PIZZA, UNIVERSITY TAVERN); the rules are phrases, in
>   `pipeline/taxonomies/ottawa_inspection.py`.
> - **Food shops and pharmacies stay in the one layer** (owner), labelled
>   "Restaurants and food shops".
> - **32.4% in a ring**. 25 stations, gate 3 exact against Wikipedia's
>   infoboxes (octranspo.com refuses scripted clients).
> - **The feed host challenges a client with no user agent** (Imperva, HTTP
>   200 HTML); the project's identifying agent is served the zip.
> - **Boundary**: the City's 2022-2026 wards dissolved, 2,892.4 km2.
> - **Line colours**: Line 1 `#D41F11`, Line 2 `#739C0D` (OC Transpo's red and
>   green moved to clear 45 Delta-E), Line 4 `#F2A900`.
> - **Region `Canada East`**, not "North America".

| | |
|---|---|
| Rail | O-Train **Lines 1, 2 and 4** (light rail): **25 stations** (the screen's count, platforms within 150 m merged), 884 m median gap; every 6–12 min |
| Storefronts | **~5,300 food premises**: 5,747 inspected since 2024-09-29, less ~7.2% institutional kitchens by name |
| Placed | **99.8%** (the feed's own `latitude`/`longitude`) |
| In the rings | **30.8%** within 0.6 mi, 16.4% within 0.3 mi |
| Rings | standard 0.1 / 0.2 / 0.3 / 0.6 mi |
| CRS | EPSG:32618 (UTM 18N, 75.70° W) |
| Region | `"North America"` |

## Business leg — Ottawa Public Health's inspection feed (Yelp LIVES)

`https://opendata.ottawa.ca/inspections/yelp_ottawa_healthscores_FoodSafety.zip`
(ArcGIS item `7e5a6428ed674d66a500f87c3ab0b2a1`), `feed_info` dated
2026-09-29. Files: `businesses.csv` (12,961), `inspections.csv` (96,739,
2000 → 2026-09-28), `violations.csv` and the rest.

- **Currency**: keep a business inspected within two years of the fetch date
  (5,747). The feed has no status field; the inspection date is the clock.
- **Institutional kitchens by name** (schools, écoles, daycares, garderies,
  hospitals, residences, churches, arenas, universities, camps: about 7.2%):
  an explicit word list, bilingual. Read the misses at build, since a name
  rule both over- and under-catches.
- **No type field**: food shops (groceries, pharmacies, convenience stores)
  sit in the same file, as in Kitchener–Waterloo. **The page states it.**
- **Never display `phone_number`.** Display `name`; run
  `check_personal_exposure.py`.
- Inspection results and violations are not mapped.
- `date` is `YYYYMMDDThh:mm:ss…`: parse the first eight characters.

## Rail — OSM (or OC Transpo)

`route=light_rail` relations, operator OC Transpo: Line 1 (Blair ↔ Tunney's
Pasture, 13), Line 2 (Bayview ↔ Limebank, 11), Line 4 (South Keys ↔
Airport, 3). **Platform names differ by direction**, so collapse by
proximity (within 150 m, the screen's rule), then name. The raw name
count is 38 at a 12 m median gap. OSM carries no colour tags: take OC
Transpo's line colours through `linecolour.py`. OSM rail follows the owner's
choice for the US cities; OC Transpo's GTFS licence is unread.

## Licences

| Source | Status |
|---|---|
| The inspection feed (City of Ottawa / Ottawa Public Health) | **READ 2026-09-29: PERMITTED WITH CONDITIONS** under the **Open Government Licence – City of Ottawa v2.0** (the item's `licenseInfo`). **Display, verbatim**: *"Contains information licensed under the Open Government Licence – City of Ottawa."* Link it to the licence where possible, and credit "Ottawa Public Health / City of Ottawa". **Must not**: suggest official status or endorsement, or use the City's or OPH's names as marks. Personal information is outside the grant (MFIPPA), so `check_personal_exposure.py` matters for home-based premises named for a person. Nothing to *do* |
| OpenStreetMap | ODbL, notice 1 (OpenStreetMap) |

⚠️ **The item says "This dataset will be retired in Q1 2026"**, yet the feed
is still updated daily (Last-Modified 2026-09-29). **Fetch early and cache**:
the source may disappear without notice. The licence ties rights to the
version in force when the data was accessed, so a retirement would not
withdraw them. The zip holds only the LIVES files (businesses, inspections,
violations, feed_info, legend, canned_comments), with no licence file of its
own.

```brief-checks
[
  {
    "id": "ottawa-inspection-feed",
    "claim": "Ottawa publishes its food-safety inspection feed as a keyless LIVES zip (businesses, inspections, violations, feed_info)",
    "kind": "http_ok",
    "url": "https://opendata.ottawa.ca/inspections/yelp_ottawa_healthscores_FoodSafety.zip",
    "min_bytes": 1000000
  },
  {
    "id": "ottawa-otrain-osm",
    "claim": "OSM carries O-Train Lines 1, 2 and 4 as light_rail relations",
    "kind": "osm_route_refs",
    "bbox": [45.20, -76.00, 45.55, -75.40],
    "routes": ["light_rail"],
    "require_refs": {"light_rail": ["1", "2", "4"]}
  },
  {
    "id": "ottawa-utm-18",
    "claim": "Ottawa (75.70 W) is in UTM zone 18N",
    "kind": "utm_zone_from_longitude",
    "lon": -75.70,
    "expect": "EPSG:32618"
  }
]
```
