# Avignon — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py avignon` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only avignon --dry-run` shows the config it writes.

**Builds APPROVED** (owner, 2026-09-30), in landing groups per `docs/review_time.md`; every call below was approved as this brief recommended it.

---

## The one-line summary

One Orizo tram line, 10 stops, all in the commune: the smallest network in the batch.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 1,146 retail, 896 food, 408 personal in the commune (screen) |
| **Scope** | **Commune of Avignon** | The worst line, T1, keeps 10 of 10 stations (100%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram T1 | 1 line from Orizo's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 482 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — Orizo's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain Orizo` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/40b26c33-9be2-47ea-a46c-8bda9f63273e` (2,409,192 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | no `feed_info.txt` |
| `shapes.txt` | yes |
| Stations | 10 network-wide under the pure-extract rule; `parent_station` on 0 of 20 platforms |
| Route types | 0: 1, 3: 66 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram T1 (`T1`) | `T1` | 363C42 | 10 | 10 (100%) |

**Every station is inside the commune.**

- No `feed_info.txt`: staleness from the NAP metadata at fetch.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 1,146 / 896 / 408 | |
| Storefronts | 2,450 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 1,684 | |

Against OpenStreetMap in the commune: **1.86×** overall (retail 1.56×, food 1.94×, personal 3.43×). Masked at source (non-diffusible): **10.6%** of the screen's denominator; coordinates joined for 99.9%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 1 Orizo line, **Tram T1**.
- **Scope**: the **commune of Avignon**; no stop is left out.
- **{Share} non-diffusible**: ~11% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.9× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **482 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **No `parent_station` column**: first platform per unchanged name.
- **The earliest feed end in the batch** (2026-10-18 on the NAP, the tram list): refetch at build.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "avignon-nap-licence",
    "claim": "The NAP dataset `Réseau urbain Orizo` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/5ae2e01d88ee381811e691b5",
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
    "id": "avignon-feed-files",
    "claim": "The feed carries shapes.txt, and no feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/40b26c33-9be2-47ea-a46c-8bda9f63273e",
    "present": [
      "routes.txt",
      "trips.txt",
      "stop_times.txt",
      "stops.txt",
      "shapes.txt"
    ],
    "absent": [
      "feed_info.txt"
    ]
  },
  {
    "id": "avignon-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/40b26c33-9be2-47ea-a46c-8bda9f63273e",
    "expect": "absent"
  },
  {
    "id": "avignon-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/40b26c33-9be2-47ea-a46c-8bda9f63273e",
    "expect": {
      "0": 1,
      "1": 0
    }
  },
  {
    "id": "avignon-stations",
    "claim": "brief_check's own count for the kept route_ids today (1 routes; 20 platforms; parent_station populated: False; 10 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/40b26c33-9be2-47ea-a46c-8bda9f63273e",
    "route_ids": [
      "T1"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 10,
    "expect_parent_station_populated": false
  },
  {
    "id": "avignon-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 84007's real contour, 65.1 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/84007?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 64.4,
    "max": 65.7
  },
  {
    "id": "avignon-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
