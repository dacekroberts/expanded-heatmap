# Le Havre — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py le_havre` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only le_havre --dry-run` shows the config it writes.

**Builds APPROVED** (owner, 2026-09-30), in landing groups per `docs/review_time.md`; every call below was approved as this brief recommended it.

---

## The one-line summary

Two LiA tram lines through the Jenner tunnel, 22 of 23 stops in the commune; an ODbL feed with no geometry and no colours.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 1,027 retail, 880 food, 552 personal in the commune (screen) |
| **Scope** | **Commune of Le Havre** | The worst line, A, keeps 14 of 15 stations (93%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram A and Tram B | 2 lines from LiA's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 434 m, under ~550 m (`docs/ring_rules.md`) |
| **Owner call** | **approved** | Line geometry source |

### Owner calls - APPROVED as recommended (owner, 2026-09-30)

- **Line geometry source**: LiA's feed has none. Found 2026-09-30: **the Normandie aggregate** (LO 2.0, the Région) carries LiA's lines A and B **with shapes** (`ATOUMOD003:Line:A:LOC`, `:B:LOC`). Recommended: a `licence-read` of the aggregate before use, because it republishes LiA's ODbL data under LO 2.0, and a notice must not rest on a relicensing the Région may not have been free to make. OpenStreetMap (already covered) is the fallback.

---

## Rail — LiA's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain LiA` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/2178bfa8-9fe0-4633-8223-8c151728ef28` (1,705,434 bytes on 2026-09-30) |
| Licence | **ODbL 1.0** (`odc-odbl`, declared on the NAP) |
| Validity | no `feed_info.txt` |
| `shapes.txt` | **NO** - geometry from another source |
| Stations | 23 network-wide under the pure-extract rule; `parent_station` on 0 of 46 platforms |
| Route types | 0: 4, 3: 65 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram A (`A`) | `7-A`, `8-A` | **none** | 15 | 14 (93%) |
| Tram B (`B`) | `7-B`, `8-B` | **none** | 15 | 15 (100%) |

**Left out by the commune boundary**: Octeville-sur-Mer: Grand Hameau.

**Station pairs under 150 m** (read by name, each one): Place Jenner A / Place Jenner B 94 m.

- No `feed_info.txt`: staleness from the NAP metadata at fetch.
- Place Jenner A and Place Jenner B, 94 m apart, are each line's own stop: two stations (ODbL).

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 1,027 / 880 / 552 | |
| Storefronts | 2,459 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 2,143 | |

Against OpenStreetMap in the commune: **1.95×** overall (retail 1.60×, food 2.03×, personal 3.03×). Masked at source (non-diffusible): **13.1%** of the screen's denominator; coordinates joined for 99.8%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: **ODbL 1.0 under the National Access Point's Conditions Particulières (read 2026-09-29)**: a §4.3 notice in `app/components.py` `_NOTICES` naming this database and its producer (Tisséo's and STAR's entries are the model; neither discharges this one), and the station table a **pure extract**: nothing renamed, nothing merged, no mean coordinate.
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 2 LiA lines, **Tram A and Tram B**.
- **Scope**: the **commune of Le Havre**; 1 stop left out, named above.
- **{Share} non-diffusible**: ~13% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~2.0× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **434 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **Colours are the project's own** (the licence read: LiA's website terms claim its colour scheme; Riga's precedent). The aggregate carries colours for A and B, but the read's reason covers them too: do not take them.
- **Two route_ids per line** (`7-A`/`8-A`, `7-B`/`8-B`: Rond-Point and La Plage variants) collapse onto the line.
- **The funicular is not in LiA's feed** (only the aggregate has it, `route_type 7`): not drawn, per the tram list.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "le_havre-nap-licence",
    "claim": "The NAP dataset `Réseau urbain LiA` declares `odc-odbl` (ODbL 1.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/617c12b7f9aaa6853cf6d303",
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
    "id": "le_havre-feed-files",
    "claim": "The feed has NO shapes.txt, so line geometry comes from another source, and no feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/2178bfa8-9fe0-4633-8223-8c151728ef28",
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
    "id": "le_havre-feed-window",
    "claim": "The zip declares no validity window of its own, so staleness is read from the NAP metadata at fetch",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/2178bfa8-9fe0-4633-8223-8c151728ef28",
    "expect": "absent"
  },
  {
    "id": "le_havre-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/2178bfa8-9fe0-4633-8223-8c151728ef28",
    "expect": {
      "0": 4,
      "1": 0
    }
  },
  {
    "id": "le_havre-stations",
    "claim": "brief_check's own count for the kept route_ids today (4 routes; 46 platforms; parent_station populated: False; 23 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/2178bfa8-9fe0-4633-8223-8c151728ef28",
    "route_ids": [
      "7-A",
      "7-B",
      "8-A",
      "8-B"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 23,
    "expect_parent_station_populated": false
  },
  {
    "id": "le_havre-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 76351's real contour, 53.2 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/76351?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 52.6,
    "max": 53.7
  },
  {
    "id": "le_havre-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
