# Minneapolis — build brief

**Step 0 measured 2026-09-28 (wave 2), 2026-09-29 (the light-rail test)
and 2026-09-29 (the Band C audit; this brief).** Band B, a reduced-bucket
page (owner, 2026-09-29): food plus grocery, **no personal services**. Run
`python scripts/brief_check.py minneapolis` before writing code.

| | |
|---|---|
| Rail | METRO **Blue** and **Green** light rail: **16 stations inside the city** (OSM), 618 m median gap; every 12–15 min. The airport's people mover (OSM `tram` CHCL) is not drawn |
| The worst line | Green keeps 10 of 24 stops (**42%**; its other half is in St. Paul, which has no register). Accepted by the owner, 2026-09-29 |
| Storefronts | **2,104**: restaurants 1,537 and caterers 35 (food); grocery 428, meat markets 90, markets 14 (retail, New York's precedent) |
| In the rings | **37.1%** within 0.6 mi, 23.1% within 0.3 mi (2,060 inside the city) |
| Rings | standard 0.1 / 0.2 / 0.3 / 0.6 mi |
| CRS | EPSG:32615 (UTM 15N) |
| Region | `"North America"` |

## Business leg — the city's Food Inspections

ArcGIS item `4eea8bf452e34f8c9d9ac07c54c0b4ab` (`Food_Inspections`, owner
City_of_Minneapolis; CC0 waiver declared, per the wave-2 screen). **47,959
rows, one per violation**, 2023-01-03 → 2026-09-18, all with
`Latitude`/`Longitude`.

- **De-duplicate on `HealthFacilityIDNumber`**: 2,916 facilities.
- **Keep a facility inspected since the fetch date minus two years**: the
  currency filter, since the table carries no status (1,537 of 1,544
  restaurants pass).
- **`FacilityCategory`**: keep RESTAURANT and CATERER as food, and GROCERY,
  MEAT MARKET and MARKET as retail. Drop INSTITUTION (451), BOARD AND
  LODGING, FOOD TRUCK, FOODSHELF, LIMITED MOBILE and FOOD CART (not
  storefronts).
- **Display `BusinessName`**. Run `check_personal_exposure.py`, because a
  sole proprietor's business name can be their own.
- **The page states**: no personal services (no salon, barber or laundry
  register exists for the city), and food shops appear as grocery only.

## Rail — OSM

Relations `route=light_rail`, operator Metro Transit: Blue Line (ref
`901`, `#0000ff`) and Green Line (ref `902`, `#008144`). Labels: "METRO
Blue Line", "METRO Green Line". The Green Line runs downtown to St. Paul, and
its stops beyond the city line are named in `excluded_stations.csv` (the Los
Angeles rule). Metro Transit's own GTFS licence is unread: OSM is the source,
the owner's rail choice for Buffalo and Houston applied again.

## Licences

| Source | Status |
|---|---|
| Food Inspections (City of Minneapolis) | CC0 waiver declared on the item. **Read it at build** with the `licence-read` agent |
| OSM | ODbL, notice 1 |

```brief-checks
[
  {
    "id": "mpls-food-inspections-schema",
    "claim": "The city's Food_Inspections layer carries the facility id, category, inspection date and coordinates this brief keys on",
    "kind": "http_contains",
    "url": "https://www.arcgis.com/sharing/rest/content/items/4eea8bf452e34f8c9d9ac07c54c0b4ab?f=json",
    "present": ["Food_Inspections"]
  },
  {
    "id": "mpls-light-rail-osm",
    "claim": "OSM carries METRO Blue (901) and Green (902) as light_rail relations",
    "kind": "osm_route_refs",
    "bbox": [44.85, -93.40, 45.10, -93.05],
    "routes": ["light_rail"],
    "require_refs": {"light_rail": ["901", "902"]}
  },
  {
    "id": "mpls-utm-15",
    "claim": "Minneapolis (93.27 W) is in UTM zone 15N",
    "kind": "utm_zone_from_longitude",
    "lon": -93.27,
    "expect": "EPSG:32615"
  }
]
```
