# Dijon — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py dijon` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only dijon --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

Two Divia tram lines, 28 of 34 stops in the commune, one colour between them.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 1,192 retail, 968 food, 532 personal in the commune (screen) |
| **Scope** | **Commune of Dijon** | The worst line, T1, keeps 14 of 17 stations (82%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram T1 and Tram T2 | 2 lines from Divia's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 411 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — Divia's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain DiviaMobilités` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/e0dbd217-15cd-4e28-9459-211a27511a34` (4,255,533 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | no `feed_info.txt` |
| `shapes.txt` | yes |
| Stations | 34 network-wide under the pure-extract rule; `parent_station` on 0 of 71 platforms |
| Route types | 0: 2, 3: 57 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram T1 (`T1`) | `4-T1` | AB0672 | 17 | 14 (82%) |
| Tram T2 (`T2`) | `4-T2` | AB0672 | 21 | 18 (86%) |

**Left out by the commune boundary**: Quetigny: Cap Vert, Grand Marché, QUETIGNY Centre La Parenthèse; Chenôve: CHENÔVE Centre, Le Mail, Valendons.

- No `feed_info.txt`: staleness from the NAP metadata at fetch.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 1,192 / 968 / 532 | |
| Storefronts | 2,692 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 2,358 | |

Against OpenStreetMap in the commune: **1.50×** overall (retail 1.23×, food 1.64×, personal 2.30×). Masked at source (non-diffusible): **14.6%** of the screen's denominator; coordinates joined for 99.9%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 2 Divia lines, **Tram T1 and Tram T2**.
- **Scope**: the **commune of Dijon**; 6 stops left out, named above.
- **{Share} non-diffusible**: ~15% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.6× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **411 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **T1 and T2 share one `route_color`** (AB0672): `pipeline/linecolour.py` refuses two drawn lines at ΔE 0. Lille's precedent: one keeps the operator's colour and the other takes the same hue darkened.
- **No `parent_station` column, and no pickup or drop-off columns**: first platform per unchanged name, and no boardability test is possible.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "dijon-nap-licence",
    "claim": "The NAP dataset `Réseau urbain DiviaMobilités` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/5d31d8b69ce2e703da90b699",
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
    "id": "dijon-feed-files",
    "claim": "The feed carries shapes.txt, and no feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/e0dbd217-15cd-4e28-9459-211a27511a34",
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
    "id": "dijon-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/e0dbd217-15cd-4e28-9459-211a27511a34",
    "expect": "absent"
  },
  {
    "id": "dijon-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/e0dbd217-15cd-4e28-9459-211a27511a34",
    "expect": {
      "0": 2,
      "1": 0
    }
  },
  {
    "id": "dijon-stations",
    "claim": "brief_check's own count for the kept route_ids today (2 routes; 71 platforms; no pickup_type/drop_off_type columns; parent_station populated: False; 34 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/e0dbd217-15cd-4e28-9459-211a27511a34",
    "route_ids": [
      "4-T1",
      "4-T2"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 34,
    "expect_parent_station_populated": false
  },
  {
    "id": "dijon-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 21231's real contour, 41.7 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/21231?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 41.2,
    "max": 42.1
  },
  {
    "id": "dijon-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
