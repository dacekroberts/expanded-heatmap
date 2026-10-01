# Dallas — build brief

**Screened 2026-09-30 (the wave-2 follow-up; from the discards to Band A, owner).**
Run `python scripts/brief_check.py dallas` before writing code. **Houston is the
template** (`docs/build_briefs/houston.md`, `pipeline/houston/`): the same
Comptroller register, the same privacy rules, a city address layer for placement.
**Queued for the Band B build session, last in its queue (owner, 2026-09-30).**

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** | **`light_rail`** | DART light rail, no metro (San Diego's class) |
| **`coverage`** | **`full`** | All three buckets from the Comptroller's NAICS codes |
| **Scope** | **City of Dallas** (OSM relation 6571629, 1,018 km²) | Permits flagged inside city limits, then point-in-boundary |
| **Lines drawn** | DART Red, Blue, Green and Orange | Silver Line and TRE are commuter rail, not drawn; the Dallas Streetcar and the M-Line trolley are a build call |
| **Rings** | standard 0.1 / 0.2 / 0.3 / 0.6 mi | Median gap 1,397 m |
| **Settled** | The address layer's indemnity **accepted** (owner, 2026-09-30) | `docs/data_sources.md`, "Dallas's indemnity" |
| **Call** | Dallas Streetcar (tram, 6 stops) and M-Line trolley: recommend **out** | Houston draws its METRORail only; the M-Line is a heritage trolley |

---

## Business leg — the Comptroller's `jrea-zgmq`

- **Active Sales Tax Permit Holders** (data.texas.gov, public domain; Houston's
  register): 44,760 outlets with `outlet_city` DALLAS flagged inside city limits,
  permits to 2026-09-26.
- **Buckets by `outlet_naics_code` (a NUMBER column):** retail 44–45 less
  non-store 454 (4,350 dropped), food 722, personal 812 less parking 812930
  (256 dropped). That gives **19,557 storefronts**: retail about 11,900, food
  6,310, personal about 1,360.
- **Houston's rules:**
  - read `outlet_*` and `taxpayer_organization_type` only;
  - never `taxpayer_name`, `taxpayer_address` or `taxpayer_number`;
  - suppress `outlet_name` for individual owners (`IS`);
  - strip suites before the join (38.6% of rows carry one);
  - run `check_personal_exposure.py`.

## Coordinates — the City's Address Points

- **The layer:** `services2.arcgis.com/rwnOSbfKSwyTBcwN/arcgis/rest/services/AddressPoints/FeatureServer`,
  layer 0 "Main Address" (395,893 points; `HOUSENUMBER`, `FULLSTREETNAME`,
  `ZIPCODE`), in Texas North Central state plane feet.
- **The sample join:** 300 random bucket rows gave **90.0% placed**, exact
  88.3% and nearest same-side number within 10 at 1.7%. The misses are mostly
  addresses outside the city: DFW airport, LBJ Freeway in Farmers Branch.
- **Pull it in bulk** (pages of 2,000), never per address.
- **Licence:** silent on reuse, with the City's GIS disclaimer's open-ended
  indemnity accepted by the owner. Optional credit: "City of Dallas
  Development Services GIS". Never call the pins surveyed or exact.

## Rail — OSM (Houston's route)

- DART's light-rail relations, refs RED, BLUE, GREEN and ORANGE, give **44
  stations inside the city**.
- **The stub test passes:** Blue keeps 19 of 22 (86%), Green 20 of 24 (83%),
  Red 18 of 25 (72%) and Orange 17 of 30 (57%). The worst, Orange, is above
  Toulouse's 52%.
- **Frequency:** purpose-built track, so frequency is disclosed, not gated.
- **Ring share:** 24.4% of storefronts within 0.6 mi (a 400-row sample).
- **Region:** `"United States East"`, as Houston.

```brief-checks
[
  {
    "id": "dallas-comptroller-outlets",
    "claim": "The Comptroller's active permit file answers for outlets flagged DALLAS inside city limits (44,760 on 2026-09-30)",
    "kind": "http_contains",
    "url": "https://data.texas.gov/resource/jrea-zgmq.json?$select=count(*)&$where=upper(outlet_city)='DALLAS'%20AND%20outlet_inside_outside_city_limits_indicator='Y'",
    "present": ["count"]
  },
  {
    "id": "dallas-address-points",
    "claim": "The City's Address Points layer answers (layer 0, Main Address)",
    "kind": "http_contains",
    "url": "https://services2.arcgis.com/rwnOSbfKSwyTBcwN/arcgis/rest/services/AddressPoints/FeatureServer/0?f=json",
    "present": ["HOUSENUMBER", "FULLSTREETNAME"]
  },
  {
    "id": "dallas-dart-refs",
    "claim": "OSM carries DART's four light-rail lines by ref (2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [32.62, -96.98, 33.02, -96.55],
    "routes": ["light_rail"],
    "require_refs": {"light_rail": ["RED", "BLUE", "GREEN", "ORANGE"]}
  },
  {
    "id": "dallas-projected-crs",
    "claim": "Dallas (96.8 W) is in UTM 14N (EPSG:32614)",
    "kind": "utm_zone_from_longitude",
    "lon": -96.8,
    "expect": "EPSG:32614",
    "mode": "light_rail",
    "coverage": "full",
    "scope": "city",
    "crs": "EPSG:32614",
    "vs_config": {"mode": "MAP_MODE", "coverage": "MAP_COVERAGE", "scope": "SCOPE", "crs": "CRS_PROJECTED"}
  }
]
```
