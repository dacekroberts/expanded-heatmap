# Kitchener–Waterloo (Regional) — build brief

**Step 0 measured 2026-09-28 (wave 2), 2026-09-29 (the light-rail test)
and 2026-09-29 (the Band C audit; this brief).** Band B, a reduced-bucket
page (owner, 2026-09-29): **food and personal services, no retail**. Run
`python scripts/brief_check.py kitchener-waterloo` before writing code.

> **Measured at the build (2026-09-30), where it corrects the text below.**
> **Three buckets on the map, two categories on the legend** (owner,
> 2026-09-30): the bulk zips' `SUBCATEGORY` splits "Food, General" into food
> service and food shops, drawn as their own layer; food shops count as food,
> so the macro dot is narrowed ("Two"). The layers are joined to the zips on
> the facility id (3,650 of 3,750 food, 963 of 998 personal); the layers are
> newer, so 61 kept premises have no type yet and stay in their layer's
> default bucket (owner). Currency: inspected within two years of the zips'
> date, 2026-07-03 (134 left out). By type: institutional, mobile and
> processing categories, caterers, community and church kitchens, cafeterias,
> banquet halls, warehouses, vending; by name: campus and hospital outlets,
> venue stands and clubs, cinemas, hotels, 23 pharmacies, mobile units and the
> Kitchener Market's Saturday stalls (its labelled upper-level counters stay).
> **2,086 storefronts** (food service 1,143, food shops 388, personal services
> 555), 41.5% within the rings; 18 personal-services names that read as a
> person's show their type. Rail: 19 stops (Waterloo 8, Kitchener 11), gate 3
> exact against the Region's own ION Stops layer, 565 m median (the downtown
> direction splits count as stops, as the Region counts them). ION's OSM
> colour #244895 moved to #12164b (ΔE 20.9 from the Retail pins). Boundary:
> the Region's Cities and Towns layer, not OSM. **Licence**: credit is
> optional (the wording below is what the licence prescribes if one is
> given, and it is displayed); **the bulk zips name no licence** on their item
> pages, and the owner read the portal's "By downloading the data on the
> portal, you are agreeing to the Open Data License" as covering them
> (2026-09-30). The zip host fails Python's TLS (curl works); the CSVs are
> cp1252.

| | |
|---|---|
| Scope | **Kitchener and Waterloo together** (Regional): either city alone is a stub (Kitchener 11 ION stops, Waterloo 8) |
| Rail | **ION** light rail (GRT route 301), **19 stops**, 613 m median gap; every 10 min, 06:00–22:00 weekdays |
| Storefronts | food "General" **2,008** + personal services **~636** in the two cities (the screen); **3,750** and **998** region-wide |
| Placed | 100% (the layers are points) |
| In the rings | region-wide 28.6% (food) and 23.0% (personal) within 0.6 mi. Higher inside the two cities; measure at build |
| Rings | standard 0.1 / 0.2 / 0.3 / 0.6 mi |
| CRS | EPSG:32617 (UTM 17N, 80.49° W) |
| Region | `"North America"` |

## Business leg — the Region of Waterloo's inspection layers

| Layer | Service | Rows (region) |
|---|---|---|
| **Food Inspection Facilities** | `https://utility.arcgis.com/usrsvcs/servers/61a7a8d8775e4da381d9718658c0d842/rest/services/OpenData/OpenData/MapServer/17` | 3,750 |
| **Personal Services Inspection Facilities** | `…/d96eeb0cd02e4b45ba52bc1a918c6218/rest/services/OpenData/OpenData/MapServer/18` | 998 |

Fields: `FacilityMasterID`, `FacilityName`, `Category`, `CategoryStyle`,
`SiteStreet`, `SiteCity`, `SiteTelephone`, `WorkArea`. The bulk tables are
also published as zips (`webapps.regionofwaterloo.ca/open-data-downloads/SSIS/Hedgehog/Inspections.zip`,
`Inspections_PS.zip`).

- **Scope by the two cities' boundary polygons, not `SiteCity`**: about 60
  spellings (the screen).
- **Food: category "General" only**, which is 2,008 in the two cities.
  Grocery and convenience stores sit inside it with no field to split them,
  so **there is no retail bucket and the page says so**.
- **Personal services hold home-based operators**: run
  `check_personal_exposure.py` first and suppress names at residential
  addresses, the Oslo and Houston rule.
- **Never display `SiteTelephone`.**

## Rail — the Region's GTFS or OSM

ION is GRT route 301. OSM has two relations (to Fairway, to Conestoga),
`#244895`, operator Grand River Transit. GRT's GTFS is under the Region of
Waterloo Open Data Licence v2.0 (declared), so either source works; OSM
matches the other light-rail builds.

## Licences

| Source | Status |
|---|---|
| Region of Waterloo inspection layers and GTFS | **Region of Waterloo Open Data Licence v2.0** (declared). Required wording: *"Contains information provided by the Regional Municipality of Waterloo under licence."* Read in full at build |
| OSM | ODbL, notice 1 (OpenStreetMap) |

```brief-checks
[
  {
    "id": "kw-food-layer",
    "claim": "The Region's Food Inspection Facilities layer answers keyless with FacilityName, Category and SiteCity",
    "kind": "http_contains",
    "url": "https://utility.arcgis.com/usrsvcs/servers/61a7a8d8775e4da381d9718658c0d842/rest/services/OpenData/OpenData/MapServer/17?f=json",
    "present": ["FacilityName", "Category", "SiteCity"]
  },
  {
    "id": "kw-personal-layer",
    "claim": "The Region's Personal Services Inspection Facilities layer answers keyless",
    "kind": "http_contains",
    "url": "https://utility.arcgis.com/usrsvcs/servers/d96eeb0cd02e4b45ba52bc1a918c6218/rest/services/OpenData/OpenData/MapServer/18?f=json",
    "present": ["FacilityName", "Category"]
  },
  {
    "id": "kw-ion-osm",
    "claim": "OSM carries ION as route 301 light_rail relations",
    "kind": "osm_route_refs",
    "bbox": [43.38, -80.60, 43.52, -80.40],
    "routes": ["light_rail"],
    "require_refs": {"light_rail": ["301"]}
  },
  {
    "id": "kw-utm-17",
    "claim": "Kitchener-Waterloo (80.49 W) is in UTM zone 17N",
    "kind": "utm_zone_from_longitude",
    "lon": -80.49,
    "expect": "EPSG:32617"
  }
]
```
