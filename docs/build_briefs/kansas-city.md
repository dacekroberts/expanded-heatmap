# Kansas City — build brief

**Screened 2026-09-27 (moved from the discards, owner: "Kansas City trams okay"); this brief 2026-09-30, on live OpenStreetMap.** Run
`python scripts/brief_check.py kansas-city` before writing code. T1 on the tram
list: trams-only maps approved by the owner on 2026-09-29. **Rings are sized by
the owner's spacing rule and no stop is thinned** (the tram batch's binding
decisions, `docs/handoff_tram_batch_2026-09-29.md`).

---

## The one-line summary

**One streetcar line and a public-domain licence register frozen at 2026-01-15, with the data date on the page** (owner, 2026-09-29, Stockholm's precedent).

| | **Kansas City, Missouri** |
|---|---|
| Rail | **KC Streetcar**, one line (OSM relations 7825409 / 7825410, ref 601; Riverfront – UMKC with the Main Street extension) |
| Stations in scope | **19 stop names, all inside the city** (OSM, 2026-09-30; 18 per direction) |
| Median station gap | **413 m**, so halved rings (0.05 / 0.1 / 0.2 / 0.3 mi) |
| Projected CRS | **EPSG:32615** (UTM 15N, 94.6° W) |
| Register | "KCMO Business License Holders", Socrata `kkhs-93m4`, **Public Domain**, 15,895 rows, geocoded |

**Region: `"North America"`.** **Macro legend (proposed)**: `mode` tram, `coverage` full.

---

## Business leg — `kkhs-93m4`

- **Frozen 2026-01-15** (`rowsUpdatedAt`): 13,058 of 15,895 rows are licences
  valid for 2025, 1,978 for 2024 and 859 for 2026 (the Phase 2 audit). **The page
  states the data date** (owner, 2026-09-29).
- **Classification is NAICS 2022 by title, not by code.** `business_type` holds
  titles such as Beauty Salons 662, Barber Shops 146, Supermarkets and Other
  Grocery Retailers 154, Clothing and Clothing Accessories Retailers 192, and
  Drinking Places 137, **mixed with fee codes** such as "Misc Rate 129" (328) and
  "Flat Rate 42" (91).
  - Map titles to codes with Census's 2022 NAICS title file, then use `naics.py`
    unchanged.
  - The fee codes cannot be classified: drop them and state the count.
- **Keep `valid_license_for` 2025 and 2026 only**, the licences current at the
  freeze.
- **Privacy:** `dba_name` is often a person ("HARRIS GREGORY J" form). Show
  `dba_name` only where it is not a personal name, else withhold it (Houston's
  sole-owner rule). Run `check_personal_exposure.py`.
- **Placement:** `location` points on the rows.

## Rail — OSM only (owner, 2026-09-30)

- **The line and stops come from OSM.** RideKC's GTFS is **not used** (owner):
  - its open-data page says "free for anyone to use", but ridekc.org's site
    terms claim to bind any download;
  - they name "schedules" as restricted content and require written consent to
    republish (Philadelphia's shape);
  - they carry an open-ended indemnity.
  The licence read was on 2026-09-30.
- **Frequency** is stated in prose as a fact: about every 10 minutes all day,
  seven days a week (the screen, 2026-09-27). Say it without citing or
  reproducing the schedule.
- **No `colour` in OSM.** Choose one. **Never use the KC Streetcar or RideKC
  logos** (the KC Streetcar Authority claims the logo and brand). The plain
  label "KC Streetcar" is the line's public name.
- The stub test passes: every stop is inside.

## Licences

- **`kkhs-93m4`: Public Domain**, as declared on the dataset. Record it in
  `docs/data_sources.md`.
- **OSM:** ODbL, with the basemap's credit.

## Build-time calls

1. **The line colour.**
2. **The NAICS title map**, and the count of fee-code rows dropped.
3. **The data-date sentence** (Stockholm's wording).

```brief-checks
[
  {
    "id": "kc-register-public-domain",
    "claim": "KCMO's business licence view kkhs-93m4 is Public Domain and last updated 2026-01-15 (rowsUpdatedAt 1768519845)",
    "kind": "http_contains",
    "url": "https://data.kcmo.org/api/views/kkhs-93m4.json",
    "present": [
      "Public Domain",
      "1768519845"
    ]
  },
  {
    "id": "kansas-city-osm-tram-refs",
    "claim": "OSM carries the streetcar as route=tram relations by ref (ref 601, KC Streetcar, 2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      39.02,
      -94.62,
      39.13,
      -94.54
    ],
    "routes": [
      "tram"
    ],
    "require_refs": {
      "tram": [
        "601"
      ]
    }
  },
  {
    "id": "kansas-city-projected-crs",
    "claim": "The derived UTM zone is EPSG:32615",
    "kind": "utm_zone_from_longitude",
    "lon": -94.58,
    "expect": "EPSG:32615"
  }
]
```
