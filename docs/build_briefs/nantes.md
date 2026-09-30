# Nantes (Regional) — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py nantes` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only nantes --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

Three Naolib tram lines; the batch's closest scope call, line 3 keeping 16 of 33 stations (48.5%) in the commune.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 2,105 retail, 1,844 food, 852 personal in the commune (screen) |
| **Scope** | **Regional**, 6 communes | The worst line, 3, keeps 16 of 33 stations (48%) in the commune. Under half goes regional (Lille); half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram 1, Tram 2 and Tram 3 | 3 lines from Naolib's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 401 m, under ~550 m (`docs/ring_rules.md`) |
| **Owner call** | see below | Scope |

### Owner calls

- **Scope**: recommended **regional** (6 communes), on the rule this kit proposes, *under half of the worst line inside goes regional*, which fits both precedents: Toulouse's T1 at 52% stayed commune-only, Lille's Métro 2 at 43% (and its tram at 8%) went regional. Commune-only keeps 56 stations and the three French comparators' scope; regional keeps all 84.

---

## Rail — Naolib's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain Naolib` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/65bdd7e4-a8e7-4a54-893a-808e71c34d68` (26,905,122 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | no `feed_info.txt` |
| `shapes.txt` | yes |
| Stations | 84 network-wide under the pure-extract rule; `parent_station` on 169 of 169 platforms |
| Route types | 0: 3, 3: 91, 4: 3 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram 1 (`1`) | `FR_NAOLIB:Line:1` | 007A45 | 35 | 26 (74%) |
| Tram 2 (`2`) | `FR_NAOLIB:Line:2` | E53138 | 34 | 22 (65%) |
| Tram 3 (`3`) | `FR_NAOLIB:Line:3` | 0079BC | 33 | 16 (48%) |

**Served communes** (6, every one holding a kept station): Nantes (56), Saint-Herblain (10), Orvault (7), Rezé (7), Bouguenais (3), La Chapelle-sur-Erdre (1).

**Station pairs under 150 m** (read by name, each one): Place du Cirque / Bretagne 117 m; Gare de Pont Rousseau / Pont Rousseau - Martyrs 138 m.

- No `feed_info.txt`: staleness from the NAP metadata at fetch.
- `stop_times.txt` is 579 MB uncompressed: read it in chunks filtered by trip (brief_check does since 2026-09-30).
- Three ferry routes (`route_type 4`, Navibus) are excluded by the Marseille ferry precedent.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune | Served communes |
|---|---|---|
| Retail / Food / Personal | 2,105 / 1,844 / 852 | 3,038 / 2,353 / 1,234 |
| Storefronts | 4,801 | 6,625 |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 4,341 | 5,383 |

Against OpenStreetMap in the commune: **1.39×** overall (retail 1.18×, food 1.49×, personal 1.91×). Masked at source (non-diffusible): **16.0%** of the screen's denominator; coordinates joined for 99.9%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 3 Naolib lines, **Tram 1, Tram 2 and Tram 3**.
- **Scope**: the **6 communes of Nantes Métropole** that the trams serve.
- **{Share} non-diffusible**: ~16% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.5× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **401 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "nantes-nap-licence",
    "claim": "The NAP dataset `Réseau urbain Naolib` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/685d9000ec5a7481ab634360",
    "present": [
      "\"licence\":\"lov2\""
    ],
    "licence": "lov2",
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
    "id": "nantes-feed-files",
    "claim": "The feed carries shapes.txt, and no feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/65bdd7e4-a8e7-4a54-893a-808e71c34d68",
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
    "id": "nantes-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/65bdd7e4-a8e7-4a54-893a-808e71c34d68",
    "expect": "absent"
  },
  {
    "id": "nantes-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/65bdd7e4-a8e7-4a54-893a-808e71c34d68",
    "expect": {
      "0": 3,
      "1": 0
    }
  },
  {
    "id": "nantes-stations",
    "claim": "brief_check's own count for the kept route_ids today (3 routes; 169 platforms; parent_station populated: True; 84 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/65bdd7e4-a8e7-4a54-893a-808e71c34d68",
    "route_ids": [
      "FR_NAOLIB:Line:1",
      "FR_NAOLIB:Line:2",
      "FR_NAOLIB:Line:3"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 84,
    "expect_parent_station_populated": true
  },
  {
    "id": "nantes-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 44109's real contour, 65.6 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/44109?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 65.0,
    "max": 66.3
  },
  {
    "id": "nantes-epci-244400404",
    "claim": "EPCI 244400404 still holds the served communes the regional scope asserts (6 of them)",
    "kind": "http_contains",
    "url": "https://geo.api.gouv.fr/epcis/244400404/communes?fields=nom,code",
    "present": [
      "44020",
      "44035",
      "44109",
      "44114",
      "44143",
      "44162"
    ]
  },
  {
    "id": "nantes-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
