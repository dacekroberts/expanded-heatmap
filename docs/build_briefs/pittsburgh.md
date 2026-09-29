# Pittsburgh — build brief

**Step 0 measured 2026-09-28 (wave 2), 2026-09-29 (the light-rail test)
and 2026-09-29 (the Band C audit; this brief).** Band B, a reduced-bucket
page (owner, 2026-09-29): food plus convenience and packaged-food retail,
**no personal services**. Run `python scripts/brief_check.py pittsburgh`
before writing code.

| | |
|---|---|
| Rail | PRT's **Blue, Red and Silver** light rail (the T), with the downtown subway: **20 stations inside the city** (OSM) |
| Spacing | **445 m median gap** → **halved rings 0.05 / 0.1 / 0.2 / 0.3 mi** (the spacing rule, `docs/ring_rules.md`) |
| The worst line | Silver keeps 13 of 31 stops (**42%**), Red 48%, Blue 54%; the rest run into the South Hills suburbs. Accepted by the owner, 2026-09-29 |
| Frequency | Red every 20 min; Blue and Silver part-day. Disclose it on the page (the light-rail test's rule for purpose-built track) |
| Storefronts | **2,086** active: restaurants 1,633 (with or without liquor, chain or not); convenience, retail and packaged-food shops 453 |
| In the rings | **26.8% within 0.3 mi** (the outer edge), 33.8% within 0.6 mi (2,043 inside the city) |
| CRS | EPSG:32617 (UTM 17N) |
| Region | `"North America"` |

## Business leg — Allegheny County's Geocoded Food Facilities

WPRDC, package `allegheny-county-restaurant-food-facility-inspection-violations`,
resource **"Geocoded Food Facilities (as of 2025)"**
(`112a3821-334d-4f3f-ab40-4de1220b1a0a`, CC0, last modified 2025-08-27):
32,245 facilities county-wide, **11,197 in Pittsburgh's wards**
(`municipal` = `Pittsburgh-NNN`), `x`/`y` in WGS84 on 98% of active rows.

- **Active = `status` 1 and no `bus_cl_date`**: 3,217 rows. ⚠️ **Status 7**
  holds 3,855 rows with no closing date. Its meaning is undocumented in the
  file: **read WPRDC's data dictionary before the build**, since it could
  nearly double the page if it means open.
- **Categories kept** (`category_cd`): 201, 202, 211 and 212 (restaurants,
  chain or not, with or without liquor) as food; 113, 114, 115 and 116
  (retail/convenience and packaged food, chain or not) as retail. Out:
  mobile tiers (119, 123), institutional kitchens (4xx, 6xx), commissaries,
  processors, temporary and seasonal.
- **Currency**: the file is 13 months old, within the one clock. The
  inspections resource (updated 2026-08-05) can confirm recency per facility
  if status 7 needs it.
- Display `facility_name`; run `check_personal_exposure.py`.
- **The page states**: no personal services (the city's own licences are
  signs, amusements and peddlers).

## Rail — OSM

`route=light_rail` relations, operator Pittsburgh Regional Transit: Blue
`#77b6e4`, Red `#ec1b24`, Silver `#BCBDC0`. Labels "PRT Blue Line", "Red
Line", "Silver Line". PRT's GTFS licence is unread: OSM is the source, the
owner's rail choice for Buffalo and Houston applied again. Stations outside
the city are named in `excluded_stations.csv`.

## Licences

| Source | Status |
|---|---|
| WPRDC / Allegheny County Health Department | **CC0** declared on the package (CKAN `license_title`). Read at build |
| OSM | ODbL, notice 1 |

```brief-checks
[
  {
    "id": "pgh-geocoded-food-facilities",
    "claim": "WPRDC serves the Geocoded Food Facilities dump keyless (about 6.6 MB, 32,245 rows county-wide)",
    "kind": "http_ok",
    "url": "https://data.wprdc.org/datastore/dump/112a3821-334d-4f3f-ab40-4de1220b1a0a",
    "min_bytes": 3000000
  },
  {
    "id": "pgh-light-rail-osm",
    "claim": "OSM carries PRT's Blue, Red and Silver as light_rail relations",
    "kind": "osm_route_refs",
    "bbox": [40.30, -80.15, 40.55, -79.85],
    "routes": ["light_rail"],
    "require_refs": {"light_rail": ["Blue", "Red", "Silver"]}
  },
  {
    "id": "pgh-utm-17",
    "claim": "Pittsburgh (79.99 W) is in UTM zone 17N",
    "kind": "utm_zone_from_longitude",
    "lon": -79.99,
    "expect": "EPSG:32617"
  }
]
```
