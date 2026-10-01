# Strasbourg — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py strasbourg` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only strasbourg --dry-run` shows the config it writes.

**Builds APPROVED** (owner, 2026-09-30), in landing groups per `docs/review_time.md`; every call below was approved as this brief recommended it.

---

## The one-line summary

Six CTS tram lines, commune-only by a whisker (line B 52%, Toulouse's exact line), and a feed with no line geometry and no parent stations, both unrecorded until today.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 2,385 retail, 2,244 food, 1,020 personal in the commune (screen) |
| **Scope** | **Commune of Strasbourg** | The worst line, B, keeps 14 of 27 stations (52%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram A, Tram B, Tram C, Tram D, Tram E and Tram F | 6 lines from CTS's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 393 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — CTS's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain CTS` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/eeea9e52-4f8a-459e-aef5-a093a3b05356` (6,106,048 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | no `feed_info.txt` |
| `shapes.txt` | **NO** - geometry from another source |
| Stations | 94 network-wide under the pure-extract rule; `parent_station` on 0 of 188 platforms |
| Route types | 0: 6, 3: 43 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram A (`A`) | `A` | E10D19 | 28 | 20 (71%) |
| Tram B (`B`) | `B` | 009EE0 | 27 | 14 (52%) |
| Tram C (`C`) | `C` | F29400 | 18 | 18 (100%) |
| Tram D (`D`) | `D` | 009933 | 24 | 20 (83%) |
| Tram E (`E`) | `E` | 9085BA | 27 | 23 (85%) |
| Tram F (`F`) | `F` | 97BF0D | 20 | 15 (75%) |

**Left out by the commune boundary**: Lingolsheim: Lingolsheim Alouettes, Lingolsheim Tiergaertel; Illkirch-Graffenstaden: Baggersee, Campus d'Illkirch, Colonne, Cours de l'Illiade, Graffenstaden, Illkirch Lixenbuhl, Leclerc, Parc Malraux; Ostwald: Bohrie, Ostwald Hôtel de Ville, Wihrel; Eckbolsheim: Bois Romain, Eckelse, Parc d'activités d'Eckbolsheim Zénith, Poteries, Wolfisheim Henri Rendu; Schiltigheim: Futura Glacière, Le Marais, Lycée Marc Bloch, Pont Phario, Rives de l'Aar; Hœnheim: Général de Gaulle, Hoenheim Gare, Le Ried; outside France's commune files: Hochschule / Läger, Kehl Bahnhof, Kehl Rathaus.

- No `feed_info.txt`: staleness from the NAP metadata at fetch.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 2,385 / 2,244 / 1,020 | |
| Storefronts | 5,649 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 5,482 | |

Against OpenStreetMap in the commune: **2.11×** overall (retail 1.84×, food 2.03×, personal 3.58×). Masked at source (non-diffusible): **10.4%** of the screen's denominator; coordinates joined for 99.8%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 6 CTS lines, **Tram A, Tram B, Tram C, Tram D, Tram E and Tram F**.
- **Scope**: the **commune of Strasbourg**; 29 stops left out, named above.
- **{Share} non-diffusible**: ~10% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~2.0× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **393 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **Line geometry**: ⚠ **the feed has no `shapes.txt`**, which the tram list did not record. Recommended: OpenStreetMap's route relations through `osm-rail` (covered by the OpenStreetMap notice); a CTS or Eurométropole layer would need a `licence-read` first.
- **No `parent_station` column**: stations are the first platform per unchanged name.
- **Line D crosses into Germany**: Hochschule / Läger, Kehl Bahnhof and Kehl Rathaus lie outside every French commune file. Commune scope leaves them out; `excluded_stations.csv` names them as "in Kehl, Germany" by hand, since no EPCI contour covers them.
- **Wacken's `WACKE_T1` platform is non-revenue** (drop-off and pickup refused on every stop_time); the shared gate drops it, as Edmonton's garages.

---

## Still unknown

- Whether the short Rotonde and Halles tunnels need anything on the page (the brief's guess: no).
- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "strasbourg-nap-licence",
    "claim": "The NAP dataset `Réseau urbain CTS` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/5ae1715488ee384c8ba0342b",
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
    "id": "strasbourg-feed-files",
    "claim": "The feed has NO shapes.txt, so line geometry comes from another source, and no feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/eeea9e52-4f8a-459e-aef5-a093a3b05356",
    "present": [
      "routes.txt",
      "trips.txt",
      "stop_times.txt",
      "stops.txt"
    ],
    "absent": [
      "shapes.txt",
      "feed_info.txt"
    ]
  },
  {
    "id": "strasbourg-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/eeea9e52-4f8a-459e-aef5-a093a3b05356",
    "expect": "absent"
  },
  {
    "id": "strasbourg-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/eeea9e52-4f8a-459e-aef5-a093a3b05356",
    "expect": {
      "0": 6,
      "1": 0
    }
  },
  {
    "id": "strasbourg-stations",
    "claim": "brief_check's own count for the kept route_ids today (6 routes; 189 platforms; parent_station populated: False; 94 stations; 1 NON-REVENUE platforms -> 94 boardable stations (Wacken)). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/eeea9e52-4f8a-459e-aef5-a093a3b05356",
    "route_ids": [
      "A",
      "B",
      "C",
      "D",
      "E",
      "F"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 94,
    "expect_parent_station_populated": false,
    "expect_boardable_stations": 94
  },
  {
    "id": "strasbourg-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 67482's real contour, 78.2 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/67482?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 77.4,
    "max": 79.0
  },
  {
    "id": "strasbourg-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
