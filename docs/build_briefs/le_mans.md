# Le Mans — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py le_mans` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only le_mans --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

Two SETRAM tram lines, every stop in the commune.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 901 retail, 632 food, 484 personal in the commune (screen) |
| **Scope** | **Commune of Le Mans** | The worst line, T1, keeps 24 of 24 stations (100%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram T1 and Tram T2 | 2 lines from SETRAM's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 437 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — SETRAM's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain SETRAM` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/dee9adc5-044c-4f68-9cd3-eefbdf7a6abd` (2,547,340 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | `feed_info.txt` self-attests: Mecatran, 2026-09-25 to **2026-11-11** |
| `shapes.txt` | yes |
| Stations | 35 network-wide under the pure-extract rule; `parent_station` on 70 of 70 platforms |
| Route types | 0: 2, 3: 61 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram T1 (`T1`) | `T1` | E4151E | 24 | 24 (100%) |
| Tram T2 (`T2`) | `T2` | 0D65AE | 18 | 18 (100%) |

**Every station is inside the commune.**

- `feed_info.txt` self-attests (Mecatran, 2026-09-25 to 2026-11-11).

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 901 / 632 / 484 | |
| Storefronts | 2,017 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 1,763 | |

Against OpenStreetMap in the commune: **1.54×** overall (retail 1.29×, food 1.79×, personal 1.87×). Masked at source (non-diffusible): **13.4%** of the screen's denominator; coordinates joined for 100.0%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 2 SETRAM lines, **Tram T1 and Tram T2**.
- **Scope**: the **commune of Le Mans**; no stop is left out.
- **{Share} non-diffusible**: ~13% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.8× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **437 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **Use the `gtfs_setram_lmm_auto` resource** (the one in the config); the `flex` resource has no tram.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "le_mans-nap-licence",
    "claim": "The NAP dataset `Réseau urbain SETRAM` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/5acb75f0c751df341652c886",
    "present": [
      "\"licence\":\"lov2\""
    ],
    "licence": "lov2",
    "scope": "commune",
    "mode": "tram",
    "coverage": "full",
    "vs_config": {
      "licence": "GTFS_LICENCE",
      "scope": "SCOPE",
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE"
    }
  },
  {
    "id": "le_mans-feed-files",
    "claim": "The feed carries shapes.txt and feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/dee9adc5-044c-4f68-9cd3-eefbdf7a6abd",
    "present": [
      "routes.txt",
      "trips.txt",
      "stop_times.txt",
      "stops.txt",
      "shapes.txt",
      "feed_info.txt"
    ],
    "absent": []
  },
  {
    "id": "le_mans-feed-window",
    "claim": "feed_info.txt declares a current window (ended 20261111 on 2026-09-30's copy; the feed rolls, so a failure means refetch, not alarm)",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/dee9adc5-044c-4f68-9cd3-eefbdf7a6abd",
    "expect": "current"
  },
  {
    "id": "le_mans-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/dee9adc5-044c-4f68-9cd3-eefbdf7a6abd",
    "expect": {
      "0": 2,
      "1": 0
    }
  },
  {
    "id": "le_mans-stations",
    "claim": "brief_check's own count for the kept route_ids today (2 routes; 70 platforms; parent_station populated: True; 35 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/dee9adc5-044c-4f68-9cd3-eefbdf7a6abd",
    "route_ids": [
      "T1",
      "T2"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 35,
    "expect_parent_station_populated": true
  },
  {
    "id": "le_mans-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 72181's real contour, 52.6 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/72181?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 52.0,
    "max": 53.1
  },
  {
    "id": "le_mans-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
