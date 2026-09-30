# Valenciennes (Regional) — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py valenciennes` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only valenciennes --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

Two Transvilles tram lines across two EPCIs; 12 of 48 stops are in the commune, so regional, and low interest.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 514 retail, 412 food, 192 personal in the commune (screen) |
| **Scope** | **Regional**, 13 communes | The worst line, T2, keeps 9 of 37 stations (24%) in the commune. Under half goes regional (Lille); half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram T1 and Tram T2 | 2 lines from Transvilles's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 510 m, under ~550 m (`docs/ring_rules.md`) |
| **Owner call** | see below | Build it at all? |

### Owner calls

- **Build it at all?** The tram list marks it low interest (1,027 storefronts near stations in the commune, 1,984 regionally). Recommended: build it last, regional, with the rest of the batch, since the kit makes it cheap.

---

## Rail — Transvilles's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain Transvilles` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/982e0826-4118-42d9-9b73-c3d3b455cd4f` (4,528,960 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | no `feed_info.txt` |
| `shapes.txt` | yes |
| Stations | 48 network-wide under the pure-extract rule; `parent_station` on 95 of 95 platforms |
| Route types | 0: 5, 3: 83 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram T1 (`T1`) | `190-28440`, `190-28449` | E62655, E7345F | 28 | 12 (43%) |
| Tram T2 (`T2`) | `191-28440`, `191-28449`, `191-28453` | 08608D, E06143 | 37 | 9 (24%) |

**Served communes** (13, every one holding a kept station): Valenciennes (12), Bruay-sur-l'Escaut (6), Denain (6), Anzin (6), Condé-sur-l'Escaut (4), Aulnoy-lez-Valenciennes (3), Escautpont (3), Fresnes-sur-Escaut (2), Famars (2), Hérin (1), Marly (1), La Sentinelle (1), Vieux-Condé (1).

- No `feed_info.txt`: staleness from the NAP metadata at fetch.
- Network-wide median gap 510 m, the widest of the batch but under 550: half-size rings.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune | Served communes |
|---|---|---|
| Retail / Food / Personal | 514 / 412 / 192 | 1,099 / 771 / 491 |
| Storefronts | 1,118 | 2,361 |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 1,027 | 1,984 |

Against OpenStreetMap in the commune: **2.02×** overall (retail 1.72×, food 2.04×, personal 3.62×). Masked at source (non-diffusible): **9.6%** of the screen's denominator; coordinates joined for 99.6%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 2 Transvilles lines, **Tram T1 and Tram T2**.
- **Scope**: the **13 communes of Valenciennes Métropole and the Porte du Hainaut** that the trams serve.
- **{Share} non-diffusible**: ~10% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~2.0× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **510 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **Two or three route_ids per line with differing colours** (T1 e62655 / E7345F; T2 e06143 / 08608D): the line's colour is the most-used route_id's, recorded in config.
- **Two EPCIs**: Valenciennes Métropole (245901160) and the Porte du Hainaut (200042190, Denain's side); both commune files are fetched.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "valenciennes-nap-licence",
    "claim": "The NAP dataset `Réseau urbain Transvilles` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/63eb6d550f2b31a8efe618fe",
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
    "id": "valenciennes-feed-files",
    "claim": "The feed carries shapes.txt, and no feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/982e0826-4118-42d9-9b73-c3d3b455cd4f",
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
    "id": "valenciennes-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/982e0826-4118-42d9-9b73-c3d3b455cd4f",
    "expect": "absent"
  },
  {
    "id": "valenciennes-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/982e0826-4118-42d9-9b73-c3d3b455cd4f",
    "expect": {
      "0": 5,
      "1": 0
    }
  },
  {
    "id": "valenciennes-stations",
    "claim": "brief_check's own count for the kept route_ids today (5 routes; 95 platforms; parent_station populated: True; 48 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/982e0826-4118-42d9-9b73-c3d3b455cd4f",
    "route_ids": [
      "190-28440",
      "190-28449",
      "191-28440",
      "191-28449",
      "191-28453"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 48,
    "expect_parent_station_populated": true
  },
  {
    "id": "valenciennes-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 59606's real contour, 13.9 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/59606?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 13.7,
    "max": 14.0
  },
  {
    "id": "valenciennes-epci-200042190",
    "claim": "EPCI 200042190 still holds the served communes the regional scope asserts (4 of them)",
    "kind": "http_contains",
    "url": "https://geo.api.gouv.fr/epcis/200042190/communes?fields=nom,code",
    "present": [
      "59172",
      "59207",
      "59302",
      "59564"
    ]
  },
  {
    "id": "valenciennes-epci-245901160",
    "claim": "EPCI 245901160 still holds the served communes the regional scope asserts (9 of them)",
    "kind": "http_contains",
    "url": "https://geo.api.gouv.fr/epcis/245901160/communes?fields=nom,code",
    "present": [
      "59014",
      "59032",
      "59112",
      "59153",
      "59221",
      "59253",
      "59383",
      "59606",
      "59616"
    ]
  },
  {
    "id": "valenciennes-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
