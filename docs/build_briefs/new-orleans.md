# New Orleans — build brief

**Screened 2026-09-28 (wave 2's US screen, owner); this brief 2026-09-30, on live OpenStreetMap.** Run
`python scripts/brief_check.py new-orleans` before writing code. T1 on the tram
list: trams-only maps approved by the owner on 2026-09-29. **Rings are sized by
the owner's spacing rule and no stop is thinned** (the tram batch's binding
decisions, `docs/handoff_tram_batch_2026-09-29.md`).

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

**Region: `"North America"`.** **Macro legend (proposed)**: `mode` tram, `coverage` full.

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
    "expect": "EPSG:32615"
  }
]
```
