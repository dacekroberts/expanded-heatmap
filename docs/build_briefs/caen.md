# Caen — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py caen` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only caen --dry-run` shows the config it writes.

**Builds APPROVED** (owner, 2026-09-30), in landing groups per `docs/review_time.md`; every call below was approved as this brief recommended it.

---

## The one-line summary

Twisto's three tram lines, 29 of 38 stops in the commune, from the Normandie aggregate: Caen has no feed of its own.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 986 retail, 833 food, 420 personal in the commune (screen) |
| **Scope** | **Commune of Caen** | The worst line, T1, keeps 19 of 25 stations (76%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram T1, Tram T2 and Tram T3 | 3 lines from Twisto's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 311 m, under ~550 m (`docs/ring_rules.md`) |
| **Owner call** | **approved** | Same place, spelt twice |

### Owner calls - APPROVED as recommended (owner, 2026-09-30)

- **Same place, spelt twice** (a Licence Ouverte feed): Presqu'île and Presqu'Ile, 12 m apart on T2. The same call as Bordeaux's: recommended, keep the first row of a same-name pair (case and accents ignored) within 150 m on LO feeds.

---

## Rail — Twisto's feed

| | |
|---|---|
| Source | the **Normandie regional aggregate**, filtered to one agency: `Agrégat des réseaux urbains et interurbains de Normandie` |
| Resource | `https://transport.data.gouv.fr/resources/81942/download` (48,130,399 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | `feed_info.txt` present but undated |
| `shapes.txt` | yes |
| Stations | 38 network-wide under the pure-extract rule; `parent_station` on 0 of 76 platforms |
| Route types | 0: 5, 1: 1, 2: 26, 3: 521, 4: 37, 7: 1 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram T1 (`T1`) | `ATOUMOD029:Line:T1:LOC` | 23A638 | 25 | 19 (76%) |
| Tram T2 (`T2`) | `ATOUMOD029:Line:T2:LOC` | E73132 | 18 | 17 (94%) |
| Tram T3 (`T3`) | `ATOUMOD029:Line:T3:LOC` | 009ADF | 15 | 13 (87%) |

**Left out by the commune boundary**: Fleury-sur-Orne: College Hawking, Hauts de l'Orne; Hérouville-Saint-Clair: CITIS, Café des Images, Château d'Eau, Place de l'Europe, Saint-Clair; Ifs: Jean Vilar, Modigliani.

**Station pairs under 150 m** (read by name, each one): Presqu'île / Presqu'Ile 12 m.

- The aggregate's `feed_info.txt` carries no dates; it runs to 2028-06-30 on the NAP.
- A real tram since 2019 (the guided TVR it replaced was retired).

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 986 / 833 / 420 | |
| Storefronts | 2,239 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 1,881 | |

Against OpenStreetMap in the commune: **1.47×** overall (retail 1.25×, food 1.67×, personal 1.83×). Masked at source (non-diffusible): **12.6%** of the screen's denominator; coordinates joined for 100.0%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **The aggregate's producer is the Région Normandie** (the NAP dataset's owner); the credit names it and the agency's network.
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 3 Twisto lines, **Tram T1, Tram T2 and Tram T3**.
- **Scope**: the **commune of Caen**; 9 stops left out, named above.
- **{Share} non-diffusible**: ~13% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.7× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **311 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **Filter the aggregate to agency `ATOUMOD029:Network:029:LOC`** (Twisto). The aggregate also carries Rouen's métro, LiA's trams and a funicular, and TER.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "caen-nap-licence",
    "claim": "The NAP dataset `Agrégat des réseaux urbains et interurbains de Normandie` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/5ced52ed8b4c4177b679d377",
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
    "id": "caen-feed-files",
    "claim": "The feed carries shapes.txt and feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://transport.data.gouv.fr/resources/81942/download",
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
    "id": "caen-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://transport.data.gouv.fr/resources/81942/download",
    "expect": "absent"
  },
  {
    "id": "caen-mode-flags",
    "claim": "What the feed types as tram (0), metro (1), funicular (7): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://transport.data.gouv.fr/resources/81942/download",
    "expect": {
      "0": 5,
      "1": 1,
      "7": 1
    }
  },
  {
    "id": "caen-stations",
    "claim": "brief_check's own count for the kept route_ids today (3 routes; 76 platforms; parent_station populated: False; 38 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://transport.data.gouv.fr/resources/81942/download",
    "route_ids": [
      "ATOUMOD029:Line:T1:LOC",
      "ATOUMOD029:Line:T2:LOC",
      "ATOUMOD029:Line:T3:LOC"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 38,
    "expect_parent_station_populated": false
  },
  {
    "id": "caen-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 14118's real contour, 25.7 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/14118?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 25.5,
    "max": 26.0
  },
  {
    "id": "caen-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
