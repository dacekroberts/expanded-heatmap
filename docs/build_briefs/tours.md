# Tours — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py tours` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only tours --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

One Fil Bleu tram line, 22 of 29 stops in Tours and the other 7 in Joué-lès-Tours.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 1,244 retail, 925 food, 492 personal in the commune (screen) |
| **Scope** | **Commune of Tours** | The worst line, A, keeps 22 of 29 stations (76%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram A | 1 line from Fil Bleu's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 377 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — Fil Bleu's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain et périurbain Fil Bleu` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/198b7602-5e74-4d88-b6bc-483af85a2430` (4,343,825 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | no `feed_info.txt` |
| `shapes.txt` | yes |
| Stations | 29 network-wide under the pure-extract rule; `parent_station` on 58 of 58 platforms |
| Route types | 0: 1, 3: 48 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram A (`A`) | `TTR:LINE:A` | BD074E | 29 | 22 (76%) |

**Left out by the commune boundary**: Joué-lès-Tours: Bulle D'o, Joué H. de Ville, Lycée J. Monnet, Pont Volant, Rabière, Rotière, République.


---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 1,244 / 925 / 492 | |
| Storefronts | 2,661 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 2,335 | |

Against OpenStreetMap in the commune: **1.52×** overall (retail 1.31×, food 1.65×, personal 2.08×). Masked at source (non-diffusible): **12.2%** of the screen's denominator; coordinates joined for 99.9%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 1 Fil Bleu line, **Tram A**.
- **Scope**: the **commune of Tours**; 7 stops left out, named above.
- **{Share} non-diffusible**: ~12% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.6× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **377 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **The feed ships `feed_infos.txt`** (sic), so for every tool it has no `feed_info.txt`: staleness from the NAP metadata at fetch.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "tours-nap-licence",
    "claim": "The NAP dataset `Réseau urbain et périurbain Fil Bleu` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/638157af7f6b7cd00e2908e1",
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
    "id": "tours-feed-files",
    "claim": "The feed carries shapes.txt, and no feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/198b7602-5e74-4d88-b6bc-483af85a2430",
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
    "id": "tours-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/198b7602-5e74-4d88-b6bc-483af85a2430",
    "expect": "absent"
  },
  {
    "id": "tours-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/198b7602-5e74-4d88-b6bc-483af85a2430",
    "expect": {
      "0": 1,
      "1": 0
    }
  },
  {
    "id": "tours-stations",
    "claim": "brief_check's own count for the kept route_ids today (1 routes; 58 platforms; parent_station populated: True; 29 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/198b7602-5e74-4d88-b6bc-483af85a2430",
    "route_ids": [
      "TTR:LINE:A"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 29,
    "expect_parent_station_populated": true
  },
  {
    "id": "tours-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 37261's real contour, 33.3 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/37261?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 33.0,
    "max": 33.7
  },
  {
    "id": "tours-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
