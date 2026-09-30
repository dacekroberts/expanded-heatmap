# Tucson — build brief

**Screened 2026-09-28 (wave 2's US screen, owner); this brief 2026-09-30, on live OpenStreetMap.** Run
`python scripts/brief_check.py tucson` before writing code. T1 on the tram
list: trams-only maps approved by the owner on 2026-09-29. **Rings are sized by
the owner's spacing rule and no stop is thinned** (the tram batch's binding
decisions, `docs/handoff_tram_batch_2026-09-29.md`).

---

## The one-line summary

**Sun Link, one streetcar line of 21 stops, and the city's NAICS business-licence layer, read as permitted (owner, 2026-09-30).**

| | **Tucson** |
|---|---|
| Rail | **Sun Link streetcar**, one line (OSM relations 3920972 / 12426661), no OSM colour |
| Stations in scope | **21 stop names, all inside the city** (OSM relation 253824) |
| Median station gap | **265 m**, so halved rings |
| Projected CRS | **EPSG:32612** (UTM 12N, 110.97° W) |
| Register | BUSLIC, `gis.tucsonaz.gov/arcgis/rest/services/PublicMaps/OpenData_EconomicDevelopment/MapServer/3`, 93,483 rows, 34,764 active, points, NAICS |

**Region: `"North America"`.** **Macro legend (proposed)**: `mode` tram, `coverage` full.

---

## Business leg — BUSLIC (layer 3, never layer 1)

- **Scope:** active (`LIC_STATUS` Active; `Application` is padded with
  spaces, so strip before comparing) and `HOME_OCCUPATION` = F. That gives
  **4,056 retail, 2,011 food and 1,245 personal services** (the screen; 2.7×,
  2.2× and 6.3× OSM).
  - `naics.py` fits unchanged.
- **Privacy:** `ACC_NAME` is the only name, and it can be a person's for the
  personal ownership types. Active licences: Sole Proprietorship 4,395,
  Individual 1,857, Married 131. Withhold the name for those `OWN_TYPE`s
  (Houston's rule). `APT` on a home record is a residence signal. Run
  `check_personal_exposure.py`.
- **Currency:** the layer describes a daily batch job, and its newest
  `DT_START` is 2026-09-12. The hub's "Data Updated 2023-10-16" is stale;
  trust the layer.
- **Layer 1 (`ZZ_CPV_BUSLIC`, 27,792 rows) is a different table**, not to be
  used.

## Rail — OSM

- **Sun Link:** 21 stops, all inside. It runs every 10 minutes on weekdays
  07–18, and every 20 in the evenings and at weekends (the screen). Disclose
  the daytime-only 10-minute service.
- **No `colour`**: choose one.

## Licences

- **BUSLIC: READ 2026-09-30, SILENT.**
  - **The item's terms:** its `licenseInfo` is an accuracy disclaimer only.
    Nothing grants and nothing restricts. The hub invites building
    applications.
  - **The owner took the permissive reading (2026-09-30)** over two sibling
    City disclaimers (DTM Map Center, PDSD PRO) that add "for your personal
    use" and ask for acknowledgement. The item incorporates neither.
  - **The page credits, as a numbered notice: "Business licence data: City of
    Tucson."**
  - Never present the pins as complete ("should not be considered a complete
    listing of all active businesses in Tucson", the layer's own words).
- **A.R.S. 39-121.03** (commercial use of public records) does not reach a
  non-commercial portfolio. It would if the project ever became commercial.
- **OSM:** ODbL.

## Build-time calls

1. **The line colour.**
2. **The personal `OWN_TYPE`s withheld**, as above.

```brief-checks
[
  {
    "id": "tucson-buslic-layer",
    "claim": "Tucson's BUSLIC business-licence layer answers on gis.tucsonaz.gov (layer 3 of OpenData_EconomicDevelopment)",
    "kind": "http_contains",
    "url": "https://gis.tucsonaz.gov/arcgis/rest/services/PublicMaps/OpenData_EconomicDevelopment/MapServer/3?f=json",
    "present": [
      "BUSLIC",
      "NAIC_CODE"
    ]
  },
  {
    "id": "tucson-osm-tram-refs",
    "claim": "OSM carries the streetcar as route=tram relations by ref (ref Sun Link, 2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      32.2,
      -110.99,
      32.25,
      -110.93
    ],
    "routes": [
      "tram"
    ],
    "require_refs": {
      "tram": [
        "Sun Link"
      ]
    }
  },
  {
    "id": "tucson-projected-crs",
    "claim": "The derived UTM zone is EPSG:32612",
    "kind": "utm_zone_from_longitude",
    "lon": -110.97,
    "expect": "EPSG:32612"
  }
]
```
