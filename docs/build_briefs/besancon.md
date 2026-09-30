# Besançon — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py besancon` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only besancon --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

Two Ginko tram lines, 29 of 31 stops in the commune; nothing unusual.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 1,012 retail, 676 food, 369 personal in the commune (screen) |
| **Scope** | **Commune of Besançon** | The worst line, T1, keeps 27 of 29 stations (93%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram T1 and Tram T2 | 2 lines from Ginko's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 361 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — Ginko's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain Ginko` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/e18e0aeb-8805-47fd-bcdb-c226d21c96fe` (4,360,706 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | `feed_info.txt` self-attests: Keolis Besançon Mobilités, 2026-09-10 to **2026-11-27** |
| `shapes.txt` | yes |
| Stations | 31 network-wide under the pure-extract rule; `parent_station` on 61 of 61 platforms |
| Route types | 0: 2, 3: 159, 715: 21 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram T1 (`T1`) | `101` | 00A5C2 | 29 | 27 (93%) |
| Tram T2 (`T2`) | `102` | 006D78 | 20 | 20 (100%) |

**Left out by the commune boundary**: Chalezeule: Chalezeule - Chalezeule, Chalezeule - Marnières.

- `feed_info.txt` self-attests (Keolis Besançon Mobilités, 2026-09-10 to 2026-11-27).
- 21 on-demand routes (`route_type 715`) are excluded as bus.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 1,012 / 676 / 369 | |
| Storefronts | 2,057 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 1,794 | |

Against OpenStreetMap in the commune: **1.56×** overall (retail 1.38×, food 1.77×, personal 1.81×). Masked at source (non-diffusible): **12.7%** of the screen's denominator; coordinates joined for 99.8%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 2 Ginko lines, **Tram T1 and Tram T2**.
- **Scope**: the **commune of Besançon**; 2 stops left out, named above.
- **{Share} non-diffusible**: ~13% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.8× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **361 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "besancon-nap-licence",
    "claim": "The NAP dataset `Réseau urbain Ginko` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/5b5b090988ee385b10198107",
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
    "id": "besancon-feed-files",
    "claim": "The feed carries shapes.txt and feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/e18e0aeb-8805-47fd-bcdb-c226d21c96fe",
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
    "id": "besancon-feed-window",
    "claim": "feed_info.txt declares a current window (ended 20261127 on 2026-09-30's copy; the feed rolls, so a failure means refetch, not alarm)",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/e18e0aeb-8805-47fd-bcdb-c226d21c96fe",
    "expect": "current"
  },
  {
    "id": "besancon-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/e18e0aeb-8805-47fd-bcdb-c226d21c96fe",
    "expect": {
      "0": 2,
      "1": 0
    }
  },
  {
    "id": "besancon-stations",
    "claim": "brief_check's own count for the kept route_ids today (2 routes; 61 platforms; parent_station populated: True; 31 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/e18e0aeb-8805-47fd-bcdb-c226d21c96fe",
    "route_ids": [
      "101",
      "102"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 31,
    "expect_parent_station_populated": true
  },
  {
    "id": "besancon-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 25056's real contour, 65.1 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/25056?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 64.4,
    "max": 65.7
  },
  {
    "id": "besancon-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
