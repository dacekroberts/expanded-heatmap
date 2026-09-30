# Montpellier — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py montpellier` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only montpellier --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

Five TaM tram lines and the largest tram network in the batch outside Bordeaux; commune-only on Toulouse's line, with an ODbL feed that has no line geometry.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 2,484 retail, 2,622 food, 1,193 personal in the commune (screen) |
| **Scope** | **Commune of Montpellier** | The worst line, 2, keeps 15 of 28 stations (54%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram 1, Tram 2, Tram 3, Tram 4 and Tram 5 | 5 lines from TaM's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 416 m, under ~550 m (`docs/ring_rules.md`) |

---

## Rail — TaM's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain TaM` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/93a29ce2-cfc8-44ff-b712-bcfd814b7f00` (4,449,383 bytes on 2026-09-30) |
| Licence | **ODbL 1.0** (`odc-odbl`, declared on the NAP) |
| Validity | no `feed_info.txt` |
| `shapes.txt` | **NO** - geometry from another source |
| Stations | 112 network-wide under the pure-extract rule; `parent_station` on 0 of 220 platforms |
| Route types | 0: 5, 3: 39 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram 1 (`1`) | `1` | 005CA9 | 31 | 31 (100%) |
| Tram 2 (`2`) | `2` | EF7D00 | 28 | 15 (54%) |
| Tram 3 (`3`) | `3` | C8D400 | 29 | 20 (69%) |
| Tram 4 (`4`) | `4` | 4B2A0E | 18 | 18 (100%) |
| Tram 5 (`5`) | `5` | 287431 | 27 | 25 (93%) |

**Left out by the commune boundary**: Saint-Jean-de-Védas: La Condamine, Saint-Jean de Védas Centre, Saint-Jean le Sec, Victoire 2; Castelnau-le-Lez: Aube Rouge, Centurions, Charles de Gaulle, Clairval, Georges Pompidou, La Galine, Notre-Dame de Sablassou, Via Domitia; Jacou: Jacou; Juvignac: Juvignac; Lattes: Boirargues, Cougourlude, Lattes Centre, Soriech; Pérols: EcoPôle, Parc Expo, Pérols Centre, Pérols Étang de l'Or; Clapiers: Clapiers; Montferrier-sur-Lez: Montferrier-sur-Lez.

**Station pairs under 150 m** (read by name, each one): Gare Saint-Roch / Gare Saint-Roch - République 69 m; Gambetta - Saint-Denis / Gambetta 71 m; Rives du Lez / Rives du Lez - Consuls de Mer 78 m; Saint-Eloi - Docteur Pezet / Saint-Éloi 81 m; Georges Frêche - Hôtel de Ville / Moularès (Hôtel de Ville) 135 m; Gambetta / Gambetta - Chaptal 136 m.

- Line 3 counts 29 stations today against the screen's 36: the screen grouped differently. The kit's table is the pure extract.
- No `feed_info.txt`: staleness comes from the NAP metadata at fetch (Paris's and Toulouse's pattern).

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 2,484 / 2,622 / 1,193 | |
| Storefronts | 6,299 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 6,179 | |

Against OpenStreetMap in the commune: **1.93×** overall (retail 1.53×, food 2.08×, personal 3.19×). Masked at source (non-diffusible): **14.5%** of the screen's denominator; coordinates joined for 99.8%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: **ODbL 1.0 under the National Access Point's Conditions Particulières (read 2026-09-29)**: a §4.3 notice in `app/components.py` `_NOTICES` naming this database and its producer (Tisséo's and STAR's entries are the model; neither discharges this one), and the station table a **pure extract**: nothing renamed, nothing merged, no mean coordinate.
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 5 TaM lines, **Tram 1, Tram 2, Tram 3, Tram 4 and Tram 5**.
- **Scope**: the **commune of Montpellier**; 24 stops left out, named above.
- **{Share} non-diffusible**: ~14% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~2.1× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **416 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **Line geometry**: the feed has no `shapes.txt` (the licence read found it). Recommended: OpenStreetMap's route relations through `osm-rail`, already covered by the OpenStreetMap notice; a Métropole GIS layer would need its own `licence-read` first.
- **No `parent_station` on any platform**: stations are the first platform per unchanged name. Several interchanges carry a different name per line (Gare Saint-Roch and Gare Saint-Roch - République, 69 m; Rives du Lez and Rives du Lez - Consuls de Mer, 78 m; Saint-Eloi - Docteur Pezet and Saint-Éloi, 81 m). ODbL: they stay two stations each; never merged.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "montpellier-nap-licence",
    "claim": "The NAP dataset `Réseau urbain TaM` declares `odc-odbl` (ODbL 1.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/662ba9a3f7d9ff84a3060d0a",
    "present": [
      "\"licence\":\"odc-odbl\""
    ],
    "licence": "odc-odbl",
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
    "id": "montpellier-feed-files",
    "claim": "The feed has NO shapes.txt, so line geometry comes from another source, and no feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/93a29ce2-cfc8-44ff-b712-bcfd814b7f00",
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
    "id": "montpellier-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/93a29ce2-cfc8-44ff-b712-bcfd814b7f00",
    "expect": "absent"
  },
  {
    "id": "montpellier-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/93a29ce2-cfc8-44ff-b712-bcfd814b7f00",
    "expect": {
      "0": 5,
      "1": 0
    }
  },
  {
    "id": "montpellier-stations",
    "claim": "brief_check's own count for the kept route_ids today (5 routes; 220 platforms; parent_station populated: False; 112 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/93a29ce2-cfc8-44ff-b712-bcfd814b7f00",
    "route_ids": [
      "1",
      "2",
      "3",
      "4",
      "5"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 112,
    "expect_parent_station_populated": false
  },
  {
    "id": "montpellier-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 34172's real contour, 57.1 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/34172?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 56.5,
    "max": 57.7
  },
  {
    "id": "montpellier-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
