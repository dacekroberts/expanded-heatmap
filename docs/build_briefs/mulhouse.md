# Mulhouse — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py mulhouse` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only mulhouse --dry-run` shows the config it writes.

**Builds APPROVED** (owner, 2026-09-30), in landing groups per `docs/review_time.md`; every call below was approved as this brief recommended it.

---

## The one-line summary

Three Soléa tram lines, 28 of 29 stops in the commune; the tram-train is not drawn.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 969 retail, 748 food, 456 personal in the commune (screen) |
| **Scope** | **Commune of Mulhouse** | The worst line, 3, keeps 10 of 11 stations (91%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram 1, Tram 2 and Tram 3 | 3 lines from Soléa's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 384 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — Soléa's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain Soléa` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/7db50c2d-3fe4-4d3d-9942-57ac37c93a8d` (4,226,104 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | no `feed_info.txt` |
| `shapes.txt` | yes |
| Stations | 29 network-wide under the pure-extract rule; `parent_station` on 58 of 60 platforms |
| Route types | 0: 4, 3: 51 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram 1 (`1`) | `91-775` | BE0013 | 12 | 12 (100%) |
| Tram 2 (`2`) | `92-775` | FFD910 | 14 | 14 (100%) |
| Tram 3 (`3`) | `94-775` | 009234 | 11 | 10 (91%) |
| ~~TT~~ | | | | not drawn: tram-train: fails the rail test (30-minute midday headway, the screen) |

**Left out by the commune boundary**: Lutterbach: LUTTERBACH GARE.

- No `feed_info.txt`: staleness from the NAP metadata at fetch.
- OpenStreetMap is thin here (3.66× in the screen; personal services 11.4×), so the page's ratio to OSM restaurants will read high.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 969 / 748 / 456 | |
| Storefronts | 2,173 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 2,121 | |

Against OpenStreetMap in the commune: **3.66×** overall (retail 2.80×, food 3.61×, personal 11.40×). Masked at source (non-diffusible): **9.2%** of the screen's denominator; coordinates joined for 100.0%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 3 Soléa lines, **Tram 1, Tram 2 and Tram 3**.
- **Scope**: the **commune of Mulhouse**; 1 stop left out, named above.
- **{Share} non-diffusible**: ~9% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~3.6× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **384 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **The tram-train `TT` is dropped** (the screen: 30-minute midday headway fails the rail test). It shares the tram's `route_type 0`, so it is excluded by line, never by type.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "mulhouse-nap-licence",
    "claim": "The NAP dataset `Réseau urbain Soléa` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/63c02bbf4059d43863de0c81",
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
    "id": "mulhouse-feed-files",
    "claim": "The feed carries shapes.txt, and no feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/7db50c2d-3fe4-4d3d-9942-57ac37c93a8d",
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
    "id": "mulhouse-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/7db50c2d-3fe4-4d3d-9942-57ac37c93a8d",
    "expect": "absent"
  },
  {
    "id": "mulhouse-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/7db50c2d-3fe4-4d3d-9942-57ac37c93a8d",
    "expect": {
      "0": 4,
      "1": 0
    }
  },
  {
    "id": "mulhouse-stations",
    "claim": "brief_check's own count for the kept route_ids today (3 routes; 60 platforms; parent_station populated: True; 32 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/7db50c2d-3fe4-4d3d-9942-57ac37c93a8d",
    "route_ids": [
      "91-775",
      "92-775",
      "94-775"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 32,
    "expect_parent_station_populated": true
  },
  {
    "id": "mulhouse-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 68224's real contour, 22.4 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/68224?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 22.2,
    "max": 22.6
  },
  {
    "id": "mulhouse-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
