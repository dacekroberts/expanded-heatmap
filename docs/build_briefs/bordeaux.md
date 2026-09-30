# Bordeaux (Regional) — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py bordeaux` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only bordeaux --dry-run` shows the config it writes.

**Builds are HELD** (owner, 2026-09-29): this brief is ready for the owner's go, not a go.

---

## The one-line summary

The biggest tram network in the batch and the clearest regional case: line A keeps 17 of 47 stations in the commune.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 3,167 retail, 3,018 food, 1,224 personal in the commune (screen) |
| **Scope** | **Regional**, 14 communes | The worst line, A, keeps 17 of 47 stations (36%) in the commune. Under half goes regional (Lille); half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram A, Tram B, Tram C, Tram D, Tram E and Tram F | 6 lines from TBM's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 425 m, under ~550 m (`docs/ring_rules.md`) |
| **Owner call** | see below | Same place, same name, twice |

### Owner calls

- **Same place, same name, twice** (a Licence Ouverte feed, so the ODbL pure-extract rule does not bind it): PESSAC CENTRE and Pessac Centre 3 m apart, Les Aubiers 10 m, Porte de Bourgogne 11 m, Hôtel de Ville 73 m and Stade Chaban Delmas 104 m. Recommended for every **LO** feed: keep the first row of a same-name pair (case and accents ignored) within 150 m, no mean coordinate and no rename; on ODbL feeds, never. The alternative is the pure extract everywhere, which draws five doubled stations here.

---

## Rail — TBM's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain et scolaire TBM` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/10b87ffe-e6bb-494d-93df-bb6019e223d9` (24,110,060 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 1.0** (`fr-lo`, declared on the NAP) |
| Validity | `feed_info.txt` self-attests: Mecatran, 2026-09-30 to **2026-12-29** |
| `shapes.txt` | yes |
| Stations | 140 network-wide under the pure-extract rule; `parent_station` on 270 of 271 platforms |
| Route types | 0: 6, 3: 193, 4: 3 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram A (`A`) | `59` | 831F82 | 47 | 17 (36%) |
| Tram B (`B`) | `60` | E50040 | 38 | 18 (47%) |
| Tram C (`C`) | `61` | D35098 | 33 | 21 (64%) |
| Tram D (`D`) | `62` | 9262A3 | 25 | 13 (52%) |
| Tram E (`E`) | `163` | 967651 | 42 | 20 (48%) |
| Tram F (`F`) | `164` | F08700 | 36 | 20 (56%) |

**Served communes** (14, every one holding a kept station): Bordeaux (57), Mérignac (17), Pessac (14), Lormont (8), Cenon (8), Le Bouscat (8), Bègles (7), Talence (6), Eysines (5), Bruges (4), Blanquefort (2), Villenave-d'Ornon (2), Le Haillan (1), Floirac (1).

**Station pairs under 150 m** (read by name, each one): PESSAC CENTRE / Pessac Centre 3 m; Les Aubiers / Les Aubiers 10 m; Porte de Bourgogne / Porte de Bourgogne 11 m; Hôtel de Ville / Hôtel de Ville 73 m; Stade Chaban Delmas / Stade Chaban Delmas 104 m.

- `feed_info.txt` self-attests (Mecatran, 2026-09-30 to 2026-12-29).
- Three ferry routes (`route_type 4`, the BAT3 river shuttle) are excluded by the Marseille ferry precedent.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune | Served communes |
|---|---|---|
| Retail / Food / Personal | 3,167 / 3,018 / 1,224 | 5,483 / 4,716 / 2,706 |
| Storefronts | 7,409 | 12,905 |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 6,889 | 10,754 |

Against OpenStreetMap in the commune: **1.84×** overall (retail 1.57×, food 1.94×, personal 2.64×). Masked at source (non-diffusible): **13.8%** of the screen's denominator; coordinates joined for 99.8%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: **Licence Ouverte 1.0 (read 2026-09-29)**: credit **Bordeaux Métropole** as producer (not TBM, Keolis or the exporter Mecatran) with the feed's own last-update date, captured at fetch. Nothing that implies endorsement; take nothing from infotbm.com, whose terms claim its marks. Colours may be restyled.
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 6 TBM lines, **Tram A, Tram B, Tram C, Tram D, Tram E and Tram F**.
- **Scope**: the **14 communes of Bordeaux Métropole** that the trams serve.
- **{Share} non-diffusible**: ~14% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.9× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **425 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **Credit Bordeaux Métropole, not Mecatran**: `feed_info.txt`'s publisher is the exporter.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "bordeaux-nap-licence",
    "claim": "The NAP dataset `Réseau urbain et scolaire TBM` declares `fr-lo` (Licence Ouverte 1.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/67f5bad303325228295b7dff",
    "present": [
      "\"licence\":\"fr-lo\""
    ],
    "licence": "fr-lo",
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
    "id": "bordeaux-feed-files",
    "claim": "The feed carries shapes.txt and feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/10b87ffe-e6bb-494d-93df-bb6019e223d9",
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
    "id": "bordeaux-feed-window",
    "claim": "feed_info.txt declares a current window (ended 20261229 on 2026-09-30's copy; the feed rolls, so a failure means refetch, not alarm)",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/10b87ffe-e6bb-494d-93df-bb6019e223d9",
    "expect": "current"
  },
  {
    "id": "bordeaux-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/10b87ffe-e6bb-494d-93df-bb6019e223d9",
    "expect": {
      "0": 6,
      "1": 0
    }
  },
  {
    "id": "bordeaux-stations",
    "claim": "brief_check's own count for the kept route_ids today (6 routes; 271 platforms; parent_station populated: True; 141 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/10b87ffe-e6bb-494d-93df-bb6019e223d9",
    "route_ids": [
      "59",
      "60",
      "61",
      "62",
      "163",
      "164"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 141,
    "expect_parent_station_populated": true
  },
  {
    "id": "bordeaux-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 33063's real contour, 49.7 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/33063?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 49.2,
    "max": 50.2
  },
  {
    "id": "bordeaux-epci-243300316",
    "claim": "EPCI 243300316 still holds the served communes the regional scope asserts (14 of them)",
    "kind": "http_contains",
    "url": "https://geo.api.gouv.fr/epcis/243300316/communes?fields=nom,code",
    "present": [
      "33039",
      "33056",
      "33063",
      "33069",
      "33075",
      "33119",
      "33162",
      "33167",
      "33200",
      "33249",
      "33281",
      "33318",
      "33522",
      "33550"
    ]
  },
  {
    "id": "bordeaux-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
