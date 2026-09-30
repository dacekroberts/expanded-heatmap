# Rouen (Regional) — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py rouen` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only rouen --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

Astuce's "Métro" is a light rail with a central tunnel, one line with two branches, and 10 of its 31 stations are in the commune: regional, from the Normandie aggregate.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`light_rail`** | Street-running light rail with a central tunnel; the feed's `route_type 1` is a flag, not the mode |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 1,505 retail, 1,190 food, 512 personal in the commune (screen) |
| **Scope** | **Regional**, 5 communes | The worst line, Métro, keeps 10 of 31 stations (32%) in the commune. Under half goes regional (Lille); half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Métro | 1 line from Astuce's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 382 m, under ~550 m (`docs/ring_rules.md`) |
| **Owner call** | see below | Mode |
| **Owner call** | see below | Page wording |

### Owner calls

- **Mode**: recommended **`light_rail`**, not `tram` and not `metro`. The feed types it `route_type 1`, but the rule is what step 1 keeps, not the flag: street-running light rail with a central tunnel, Calgary's and Houston's class.
- **Page wording**: the approved template says "{City} has no metro: its trams are its rapid transit", and the line's public name is "Métro". Recommended: "Rouen's métro is a light rail running mostly on the street, so every stop gets rings", one sentence changed for this city only. Otherwise the template stands.

---

## Rail — Astuce's feed

| | |
|---|---|
| Source | the **Normandie regional aggregate**, filtered to one agency: `Agrégat des réseaux urbains et interurbains de Normandie` |
| Resource | `https://transport.data.gouv.fr/resources/81942/download` (48,130,399 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | `feed_info.txt` present but undated |
| `shapes.txt` | yes |
| Stations | 31 network-wide under the pure-extract rule; `parent_station` on 0 of 61 platforms |
| Route types | 0: 5, 1: 1, 2: 26, 3: 521, 4: 37, 7: 1 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Métro (`Métro`) | `ATOUMOD001:Line:TCARx90:LOC` | 123E8B | 31 | 10 (32%) |

**Served communes** (5, every one holding a kept station): Rouen (10), Sotteville-lès-Rouen (6), Le Grand-Quevilly (5), Le Petit-Quevilly (5), Saint-Étienne-du-Rouvray (5).

- The aggregate's `feed_info.txt` names CITYWAY and carries no dates; it runs to 2028-06-30 on the NAP.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune | Served communes |
|---|---|---|
| Retail / Food / Personal | 1,505 / 1,190 / 512 | 1,911 / 1,511 / 777 |
| Storefronts | 3,207 | 4,199 |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 2,868 | 3,634 |

Against OpenStreetMap in the commune: **1.73×** overall (retail 1.52×, food 1.84×, personal 2.35×). Masked at source (non-diffusible): **10.5%** of the screen's denominator; coordinates joined for 99.9%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

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

- **{N} {operator} tram lines … {lines}**: 1 Astuce line, **Métro**.
- **Scope**: the **5 communes of the Métropole Rouen Normandie** that the métro serves.
- **{Share} non-diffusible**: ~10% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.8× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **382 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **The feed is the Normandie regional aggregate**, filtered to agency `ATOUMOD001:Network:001:LOC` (Astuce): Astuce's own resource redirects to `api.mrn.cityway.fr`, which refused connections at the screen and again on 2026-09-30. Try it first at build; the aggregate is the fallback, and its licence (LO 2.0, the Région) is what the credit then names.
- **No `parent_station` in the aggregate**: first platform per unchanged name.

---

## Still unknown

- Astuce's own feed, if its host answers at build: its licence is LO 2.0 on the NAP and was not read one by one.
- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "rouen-nap-licence",
    "claim": "The NAP dataset `Agrégat des réseaux urbains et interurbains de Normandie` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/5ced52ed8b4c4177b679d377",
    "present": [
      "\"licence\":\"lov2\""
    ],
    "licence": "lov2",
    "scope": "regional",
    "mode": "light_rail",
    "coverage": "full",
    "vs_config": {
      "licence": "GTFS_LICENCE",
      "scope": "SCOPE",
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE"
    }
  },
  {
    "id": "rouen-feed-files",
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
    "id": "rouen-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://transport.data.gouv.fr/resources/81942/download",
    "expect": "absent"
  },
  {
    "id": "rouen-mode-flags",
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
    "id": "rouen-stations",
    "claim": "brief_check's own count for the kept route_ids today (1 routes; 61 platforms; parent_station populated: False; 31 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://transport.data.gouv.fr/resources/81942/download",
    "route_ids": [
      "ATOUMOD001:Line:TCARx90:LOC"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 31,
    "expect_parent_station_populated": false
  },
  {
    "id": "rouen-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 76540's real contour, 21.4 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/76540?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 21.2,
    "max": 21.6
  },
  {
    "id": "rouen-epci-200023414",
    "claim": "EPCI 200023414 still holds the served communes the regional scope asserts (5 of them)",
    "kind": "http_contains",
    "url": "https://geo.api.gouv.fr/epcis/200023414/communes?fields=nom,code",
    "present": [
      "76322",
      "76498",
      "76540",
      "76575",
      "76681"
    ]
  },
  {
    "id": "rouen-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
