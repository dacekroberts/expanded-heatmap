# Grenoble (Regional) — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py grenoble` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only grenoble --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

Five M réso tram lines, regional without argument: lines C, D and E keep a third of their stations in the commune.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 1,541 retail, 1,601 food, 598 personal in the commune (screen) |
| **Scope** | **Regional**, 12 communes | The worst line, D, keeps 7 of 22 stations (32%) in the commune. Under half goes regional (Lille); half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram A, Tram B, Tram C, Tram D and Tram E | 5 lines from M réso's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 365 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — M réso's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain TAG` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/b6ec7ba4-09bc-46df-b9a1-79a2c2668cf2` (4,483,537 bytes on 2026-09-30) |
| Licence | **ODbL 1.0** (`odc-odbl`, declared on the NAP) |
| Validity | `feed_info.txt` present but undated |
| `shapes.txt` | yes |
| Stations | 81 network-wide under the pure-extract rule; `parent_station` on 168 of 168 platforms |
| Route types | 0: 5, 3: 51 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram A (`A`) | `91` | 3376B8 | 31 | 16 (52%) |
| Tram B (`B`) | `92` | 479A45 | 22 | 12 (55%) |
| Tram C (`C`) | `93` | C20078 | 22 | 8 (36%) |
| Tram D (`D`) | `94` | DE9917 | 22 | 7 (32%) |
| Tram E (`E`) | `95` | 533786 | 31 | 12 (39%) |

**Served communes** (12, every one holding a kept station): Grenoble (35), Saint-Martin-d'Hères (11), Échirolles (8), Fontaine (5), Saint-Égrève (5), Seyssinet-Pariset (3), La Tronche (3), Saint-Martin-le-Vinoux (3), Gières (2), Fontanil-Cornillon (2), Le Pont-de-Claix (2), Seyssins (2).

- `feed_info.txt` exists but carries no dates: staleness from the NAP metadata at fetch.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune | Served communes |
|---|---|---|
| Retail / Food / Personal | 1,541 / 1,601 / 598 | 2,526 / 2,256 / 1,029 |
| Storefronts | 3,740 | 5,811 |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 3,716 | 5,455 |

Against OpenStreetMap in the commune: **1.51×** overall (retail 1.29×, food 1.72×, personal 1.69×). Masked at source (non-diffusible): **10.5%** of the screen's denominator; coordinates joined for 100.0%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: **ODbL 1.0 under the National Access Point's Conditions Particulières (read 2026-09-29)**: a §4.3 notice in `app/components.py` `_NOTICES` naming this database and its producer (Tisséo's and STAR's entries are the model; neither discharges this one), and the station table a **pure extract**: nothing renamed, nothing merged, no mean coordinate.
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 5 M réso lines, **Tram A, Tram B, Tram C, Tram D and Tram E**.
- **Scope**: the **12 communes of Grenoble-Alpes Métropole** that the trams serve.
- **{Share} non-diffusible**: ~10% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.7× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **365 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **The §4.3 notice names SMMAG** ("M"), the licence read's finding; SMMAG's own licence page is now empty and was read from its Wayback copy of 2025-03-15.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "grenoble-nap-licence",
    "claim": "The NAP dataset `Réseau urbain TAG` declares `odc-odbl` (ODbL 1.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/5af03701b595081c1880a8a4",
    "present": [
      "\"licence\":\"odc-odbl\""
    ],
    "licence": "odc-odbl",
    "scope": "regional",
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
    "id": "grenoble-feed-files",
    "claim": "The feed carries shapes.txt and feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/b6ec7ba4-09bc-46df-b9a1-79a2c2668cf2",
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
    "id": "grenoble-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/b6ec7ba4-09bc-46df-b9a1-79a2c2668cf2",
    "expect": "absent"
  },
  {
    "id": "grenoble-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/b6ec7ba4-09bc-46df-b9a1-79a2c2668cf2",
    "expect": {
      "0": 5,
      "1": 0
    }
  },
  {
    "id": "grenoble-stations",
    "claim": "brief_check's own count for the kept route_ids today (5 routes; 168 platforms; parent_station populated: True; 81 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/b6ec7ba4-09bc-46df-b9a1-79a2c2668cf2",
    "route_ids": [
      "91",
      "92",
      "93",
      "94",
      "95"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 81,
    "expect_parent_station_populated": true
  },
  {
    "id": "grenoble-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 38185's real contour, 18.4 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/38185?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 18.2,
    "max": 18.6
  },
  {
    "id": "grenoble-epci-200040715",
    "claim": "EPCI 200040715 still holds the served communes the regional scope asserts (12 of them)",
    "kind": "http_contains",
    "url": "https://geo.api.gouv.fr/epcis/200040715/communes?fields=nom,code",
    "present": [
      "38151",
      "38169",
      "38170",
      "38179",
      "38185",
      "38317",
      "38382",
      "38421",
      "38423",
      "38485",
      "38486",
      "38516"
    ]
  },
  {
    "id": "grenoble-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
