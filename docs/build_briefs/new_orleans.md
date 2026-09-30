# New Orleans — build brief

**Screened 2026-09-28 (wave 2's US screen, owner); this brief 2026-09-30, on live OpenStreetMap.** Run
`python scripts/brief_check.py new_orleans` before writing code. T1 on the tram
list: trams-only maps approved by the owner on 2026-09-29. **Rings are sized by
the owner's spacing rule and no stop is thinned** (the tram batch's binding
decisions, `docs/handoff_tram_batch_2026-09-29.md`).

---

## For the owner, with the build

**Approved (owner, 2026-09-30; the 24 calls in `docs/handoff_tram_kit_2026-09-30.md`, cdee504)**: every call below as recommended, and the page-text template. Builds wait for the owner's explicit go.

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams, no metro |
| **`coverage`** (macro dot fill) | **`full`** | All three buckets |
| **Scope** | **City of New Orleans** | See the rail section |
| **Lines drawn** | Streetcars 12, 47, 48 and 2 (OSM colours, mapped to hex) | |
| **Rings** | halved: median gap 164 m; **no thinning** | The owner's spacing rule (`docs/ring_rules.md`) |
| **Call (approved): Thinning** | **None**: 38.1% of licences within 0.3 mi with every stop, 37.2% thinned at 400 m (48 stops); the filter's own test fails for a uniformly dense system | |
| **Call (approved): Lines 49 and 46** | not drawn unless in service | |

---

## The one-line summary

**Four RTA streetcar lines, 110 stops at a 164 m median gap (the densest on the tram list), and a CC0 occupational licence register with a point on every row.**

| | **New Orleans** |
|---|---|
| Rail | **RTA streetcars 12 (St. Charles), 47 and 48 (Canal), 2 (Riverfront)**, OSM, each with an OSM colour |
| Stations in scope | **110 stop names, all inside the city** (OSM relation 131885) |
| Median station gap | **164 m**, so halved rings; **no thinning** (owner) |
| Projected CRS | **EPSG:32615** (90.07° W) |
| Register | "Active Occupational Licenses", Socrata `iqay-p646`, **CC0**, about 16,507 rows (updated 2026-09-29) |

**Region: `"United States East"`** (Houston, at 95.4° W, is East). **Macro legend (proposed)**: `mode` tram, `coverage` full.

---

## Business leg — `iqay-p646`

- **The screen (2026-09-28):** about **2,411 retail, 1,934 food and 1,057
  personal services** (3.4×, 1.9× and 20× OSM). Points on 100%.
- **Classification:** a small text taxonomy (NAICS-style descriptions, no
  codes), to be keyed with `premises-taxonomy`.
  - Drop "Special Events-Other (Vendor)" (1,258) and "Home Based-Office Use
    Only" (357).
  - Measure the catch-all share first.
- **Privacy:** `ownername` is never shown. Run `check_personal_exposure.py`.
- **Currency:** active licences, updated daily (2026-09-29). It passes.

## Rail — OSM

- **Drawn:** 12, 47, 48 and 2, each line whole inside the city: 53–54, 20–23,
  20 and 12 stops.
  - Their OSM colours are named, not hex (`green`, `red`, `#90EE90`, `blue`).
    Map them to hex and check contrast.
- ⚠️ **Refs 49 (colour `#5C2E86`) and 46 have relations but no stop members.**
  Read whether they run, which is the Rampart–St. Claude service's history.
  Place them as not drawn unless they do; step 1 refuses an unplaced
  relation.
- **Measured 2026-09-30** (iqay-p646's 14,900 points, less the two dropped types): with every stop kept, **38.1% within 0.3 mi** (53.0% within 0.6); San Francisco's `thin()` at 400 m, terminals and interchanges kept, leaves 48 stops and **37.2%**; at 800 m, 34.1%. Thinning moves the share by under a point.
- **The 110 stops are kept, and the owner's no-thinning rule replaces** the
  tram list's older note ("thin 110 street stops, Philadelphia's and San
  Francisco's filter").
- **Frequency:** about every 10 minutes, varying by line (search-level).
  Disclose it. RTA's GTFS is not read; if it is used, it needs a licence read
  first.

## Licences

- **`iqay-p646`: CC0**, as declared. Record it in `docs/data_sources.md`.
- **OSM:** ODbL.

## Build-time calls

1. **Lines 49 and 46**: in service or not.
2. **The taxonomy** and its catch-all.
3. **Hex colours** for the four lines.

```brief-checks
[
  {
    "id": "new-orleans-osm-tram-refs",
    "claim": "OSM carries the streetcar as route=tram relations by ref (lines 12, 47, 48 and 2, 2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      29.9,
      -90.14,
      30.0,
      -90.03
    ],
    "routes": [
      "tram"
    ],
    "require_refs": {
      "tram": [
        "12",
        "47",
        "48",
        "2"
      ]
    }
  },
  {
    "id": "new-orleans-projected-crs",
    "claim": "The derived UTM zone is EPSG:32615",
    "kind": "utm_zone_from_longitude",
    "lon": -90.07,
    "expect": "EPSG:32615",
    "mode": "tram",
    "coverage": "full",
    "scope": "city",
    "crs": "EPSG:32615",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
