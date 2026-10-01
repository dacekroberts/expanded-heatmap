# Reims — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py reims` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only reims --dry-run` shows the config it writes.

**Builds APPROVED** (owner, 2026-09-30), in landing groups per `docs/review_time.md`; every call below was approved as this brief recommended it.

---

> **CORRECTED AT BUILD (2026-09-30): Reims has TWO public tram lines, T1 and
> T2, not one.** Since 2025-11-24 Grand Reims Mobilités runs T1 (Neufchâtel -
> Hôpital Debré, 21 stops) and T2 (Neufchâtel - Gare Champagne TGV, 22 stops),
> the former lines A and B (fr.wikipedia's "Tramway de Reims"; OpenStreetMap's
> relations agree). The feed still carries one route, `TRAM`, so the build
> splits its trips by terminus (`ROUTE_BRANCHES` in the config), and draws and
> labels T1 and T2. Gate 3 is exact against the published 21 and 22. The
> "one line in the legend" below is superseded. Build log:
> the France build entries in `DECISIONS.md` (folded 2026-10-01).

## The one-line summary

One tram line with two branches, 21 of 24 stops in the commune, and a feed that calls it a metro.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | The feed types it `route_type 1`, but it is a street tram |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 1,167 retail, 927 food, 598 personal in the commune (screen) |
| **Scope** | **Commune of Reims** | The worst line, TRAM, keeps 21 of 24 stations (88%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram | 1 line from Grand Reims Mobilités's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 370 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — Grand Reims Mobilités's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain Grand Reims Mobilités` |
| Resource | `https://transport.data.gouv.fr/resources/80594/download` (2,634,451 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | `feed_info.txt` self-attests: Grand Reims Mobilités, 2026-09-28 to **2026-11-01** |
| `shapes.txt` | yes |
| Stations | 24 network-wide under the pure-extract rule; `parent_station` on 46 of 46 platforms |
| Route types | 1: 1, 3: 27 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram (`TRAM`) | `TRAM` | E0001B | 24 | 21 (88%) |

**Left out by the commune boundary**: Bezannes: Gare de Champagne-Ardenne TGV, POLYCLINIQUE; Bétheny: NEUFCHATEL.

- `feed_info.txt` self-attests (Grand Reims Mobilités, 2026-09-28 to 2026-11-01).

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 1,167 / 927 / 598 | |
| Storefronts | 2,692 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 1,947 | |

Against OpenStreetMap in the commune: **2.25×** overall (retail 1.73×, food 2.58×, personal 3.67×). Masked at source (non-diffusible): **13.8%** of the screen's denominator; coordinates joined for 99.9%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 1 Grand Reims Mobilités line, **Tram**.
- **Scope**: the **commune of Reims**; 3 stops left out, named above.
- **{Share} non-diffusible**: ~14% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~2.6× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **370 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **The feed types the tram `route_type 1`**: mode is `tram`, decided from what step 1 keeps, never from the flag. Select on route_id `TRAM` with `ROUTE_TYPES_RAIL = ("1",)`.
- **One line, two branches** (Neufchâtel to Hôpital Debré and to Gare Champagne TGV): one line in the legend, as Rouen's métro.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "reims-nap-licence",
    "claim": "The NAP dataset `Réseau urbain Grand Reims Mobilités` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/63b4c3d200fbf8e5ed9dde9a",
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
    "id": "reims-feed-files",
    "claim": "The feed carries shapes.txt and feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://transport.data.gouv.fr/resources/80594/download",
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
    "id": "reims-feed-window",
    "claim": "feed_info.txt declares a current window (ended 20261101 on 2026-09-30's copy; the feed rolls, so a failure means refetch, not alarm)",
    "kind": "gtfs_feed_window",
    "url": "https://transport.data.gouv.fr/resources/80594/download",
    "expect": "current"
  },
  {
    "id": "reims-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://transport.data.gouv.fr/resources/80594/download",
    "expect": {
      "0": 0,
      "1": 1
    }
  },
  {
    "id": "reims-stations",
    "claim": "brief_check's own count for the kept route_ids today (1 routes; 46 platforms; parent_station populated: True; 24 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://transport.data.gouv.fr/resources/80594/download",
    "route_ids": [
      "TRAM"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 24,
    "expect_parent_station_populated": true
  },
  {
    "id": "reims-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 51454's real contour, 46.9 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/51454?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 46.4,
    "max": 47.4
  },
  {
    "id": "reims-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
