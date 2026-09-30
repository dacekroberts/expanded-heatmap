# Nice — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py nice` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only nice --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

Every Lignes d'Azur tram stop is inside the commune, so scope costs nothing; the calls are a sixth route and a tunnel.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 4,230 retail, 3,544 food, 2,372 personal in the commune (screen) |
| **Scope** | **Commune of Nice** | The worst line, L1, keeps 22 of 22 stations (100%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram 1, Tram 2, Tram 3 and TODO: route B's public name (Aéroport Terminal 2 - CADAM, 6 stops; an owner call to draw it) | 4 lines from Lignes d'Azur's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 415 m, under ~550 m (`docs/ring_rules.md`) |
| **Owner call** | see below | Route B |

### Owner calls

- **Route B** (`Aéroport Terminal 2 - CADAM / Centre Administratif`, 6 stops, all in Nice, coloured FFDD00): the feed types it tram and it runs on tram track. Recommended: **draw it** under its public name, verified at build. It adds one line to the page's count.

---

## Rail — Lignes d'Azur's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain Lignes d'Azur` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/f5678ab2-c863-4b48-ba1f-9021c7d97634` (7,629,355 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | `feed_info.txt` self-attests: Lignes d'Azur, 2026-09-18 to **2026-10-28** |
| `shapes.txt` | yes |
| Stations | 47 network-wide under the pure-extract rule; `parent_station` on 94 of 94 platforms |
| Route types | 0: 4, 3: 99, 715: 9 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram 1 (`L1`) | `L1` | D20A11 | 22 | 22 (100%) |
| Tram 2 (`L2`) | `L2` | 1F488F | 17 | 17 (100%) |
| Tram 3 (`L3`) | `L3` | 00853E | 24 | 24 (100%) |
| TODO (`B`) | `B` | FFDD00 | 6 | 6 (100%) |

**Every station is inside the commune.**

- `feed_info.txt` self-attests (Lignes d'Azur, 2026-09-18 to 2026-10-28).
- Route types also carry 9 on-demand routes (715), excluded as bus.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 4,230 / 3,544 / 2,372 | |
| Storefronts | 10,146 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 9,379 | |

Against OpenStreetMap in the commune: **2.85×** overall (retail 2.57×, food 2.31×, personal 6.38×). Masked at source (non-diffusible): **12.1%** of the screen's denominator; coordinates joined for 99.7%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 4 Lignes d'Azur lines, **Tram 1, Tram 2, Tram 3 and TODO: route B's public name (Aéroport Terminal 2 - CADAM, 6 stops; an owner call to draw it)**.
- **Scope**: the **commune of Nice**; no stop is left out.
- **{Share} non-diffusible**: ~12% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~2.3× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **415 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **L2 in a tunnel** (the tram list: 6.4 km, an EDGE): the underground stations get rings like any other (Rennes's and Toulouse's métro precedent). Nothing to decide unless the owner wants the page to say so.
- **Personal services lean on beauty** (screen: 96.02B 1,026 over 810 hairdressers, personal services 6.4× OpenStreetMap). A composition check at step 2 and `check_personal_exposure.py` before publishing, as every French city.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "nice-nap-licence",
    "claim": "The NAP dataset `Réseau urbain Lignes d'Azur` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/685181f3733800e180c475fa",
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
    "id": "nice-feed-files",
    "claim": "The feed carries shapes.txt and feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/f5678ab2-c863-4b48-ba1f-9021c7d97634",
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
    "id": "nice-feed-window",
    "claim": "feed_info.txt declares a current window (ended 20261028 on 2026-09-30's copy; the feed rolls, so a failure means refetch, not alarm)",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/f5678ab2-c863-4b48-ba1f-9021c7d97634",
    "expect": "current"
  },
  {
    "id": "nice-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/f5678ab2-c863-4b48-ba1f-9021c7d97634",
    "expect": {
      "0": 4,
      "1": 0
    }
  },
  {
    "id": "nice-stations",
    "claim": "brief_check's own count for the kept route_ids today (4 routes; 94 platforms; parent_station populated: True; 47 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/f5678ab2-c863-4b48-ba1f-9021c7d97634",
    "route_ids": [
      "L1",
      "L2",
      "L3",
      "B"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 47,
    "expect_parent_station_populated": true
  },
  {
    "id": "nice-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 06088's real contour, 73.8 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/06088?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 73.1,
    "max": 74.6
  },
  {
    "id": "nice-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
