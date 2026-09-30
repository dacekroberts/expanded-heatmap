# Saint-Étienne — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py saint_etienne` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only saint_etienne --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

Three STAS tram lines, 35 of 40 stops in the commune, and the tightest spacing of the batch (321 m).

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 1,333 retail, 1,164 food, 531 personal in the commune (screen) |
| **Scope** | **Commune of Saint-Étienne** | The worst line, T1, keeps 22 of 27 stations (81%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram T1, Tram T2 and Tram T3 | 3 lines from STAS's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 321 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — STAS's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain STAS` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/fc66b270-658c-4678-9794-229a1a8a4938` (6,976,845 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | no `feed_info.txt` |
| `shapes.txt` | yes |
| Stations | 40 network-wide under the pure-extract rule; `parent_station` on 0 of 75 platforms |
| Route types | 0: 3, 11: 4, 3: 75 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram T1 (`T1`) | `50` | E30613 | 27 | 22 (81%) |
| Tram T2 (`T2`) | `51` | 02509E | 12 | 12 (100%) |
| Tram T3 (`T3`) | `52` | 009640 | 29 | 24 (83%) |

**Left out by the commune boundary**: Saint-Priest-en-Jarez: CITE AGRICULTURE, HOPITAL NORD, LYCEE S. WEIL, MUSEE ART MOD., PARC-CHAMPIROL.

**Station pairs under 150 m** (read by name, each one): PEUPLE LIBERAT. / PEUPLE FOY 50 m; PEUPLE GAMBETTA / PEUPLE LIBERAT. 103 m; PEUPLE FOY / PEUPLE GAMBETTA 109 m.

- No `feed_info.txt`: staleness from the NAP metadata at fetch.
- Four trolleybus routes (`route_type 11`) are excluded as bus.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 1,333 / 1,164 / 531 | |
| Storefronts | 3,028 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 2,523 | |

Against OpenStreetMap in the commune: **1.71×** overall (retail 1.43×, food 2.09×, personal 1.89×). Masked at source (non-diffusible): **10.7%** of the screen's denominator; coordinates joined for 99.7%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 3 STAS lines, **Tram T1, Tram T2 and Tram T3**.
- **Scope**: the **commune of Saint-Étienne**; 5 stops left out, named above.
- **{Share} non-diffusible**: ~11% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~2.1× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **321 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **No `parent_station` column**: first platform per unchanged name. The three PEUPLE stops (Foy, Gambetta, Libération, 50 to 109 m apart) are distinct stops and stay so.
- **`route_text_color` is blank**: the label colour is the renderer's choice.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "saint_etienne-nap-licence",
    "claim": "The NAP dataset `Réseau urbain STAS` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/5c34c93f8b4c4104b817fb3a",
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
    "id": "saint_etienne-feed-files",
    "claim": "The feed carries shapes.txt, and no feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/fc66b270-658c-4678-9794-229a1a8a4938",
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
    "id": "saint_etienne-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/fc66b270-658c-4678-9794-229a1a8a4938",
    "expect": "absent"
  },
  {
    "id": "saint_etienne-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/fc66b270-658c-4678-9794-229a1a8a4938",
    "expect": {
      "0": 3,
      "1": 0
    }
  },
  {
    "id": "saint_etienne-stations",
    "claim": "brief_check's own count for the kept route_ids today (3 routes; 75 platforms; parent_station populated: False; 40 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/fc66b270-658c-4678-9794-229a1a8a4938",
    "route_ids": [
      "50",
      "51",
      "52"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 40,
    "expect_parent_station_populated": false
  },
  {
    "id": "saint_etienne-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 42218's real contour, 79.9 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/42218?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 79.1,
    "max": 80.7
  },
  {
    "id": "saint_etienne-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
