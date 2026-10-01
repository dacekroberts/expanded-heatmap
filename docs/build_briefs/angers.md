# Angers — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py angers` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only angers --dry-run` shows the config it writes.

**Builds APPROVED** (owner, 2026-09-30), in landing groups per `docs/review_time.md`; every call below was approved as this brief recommended it.

---

## The one-line summary

Three tram lines, A, B and C, 36 of 42 stops in the commune, built mark-free: the Métropole's terms bar its network brand from anything built from the data.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 1,183 retail, 876 food, 493 personal in the commune (screen) |
| **Scope** | **Commune of Angers** | The worst line, A, keeps 19 of 25 stations (76%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram A, Tram B and Tram C | 3 lines from Angers Loire Métropole's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 390 m, under ~550 m (`docs/ring_rules.md`) |
| **Owner call** | **approved** | Build mark-free |

### Owner calls - APPROVED as recommended (owner, 2026-09-30)

- **Build mark-free** (owner, 2026-09-30: "build angers mark-free as recommended"). The Métropole's terms (licence read 2026-09-29, DECISIONS "French tram feeds read") say the network's marks "and any other mark" of the service may not be used or mentioned in anything built from the data without its prior agreement. So the page, the macro label, the city entry, the transit caption and the §4.3 notice name **Angers Loire Métropole**, never the brand; the lines are **Tram A, Tram B and Tram C**, their letters, which are not marks; and the feed's `feed_publisher_name` and `agency_name` (both the brand) are never shown. The §4.3 notice names the database by its producer and links its NAP page. If the Métropole objects, the removal rule applies: take Angers down first, record who asked. Rejected: seeking consent first (the owner's to send through a reCAPTCHA form, open-ended, and outreach is the last resort); holding Angers indefinitely.

---

## Rail — Angers Loire Métropole's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain Irigo` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/32f30b64-33f7-43bb-9b6f-34c21c2f83a3` (4,292,573 bytes on 2026-09-30) |
| Licence | **ODbL 1.0** (`odc-odbl`, declared on the NAP) |
| Validity | `feed_info.txt` self-attests: IRIGO, 2026-09-29 to **2026-12-28** |
| `shapes.txt` | yes |
| Stations | 42 network-wide under the pure-extract rule; `parent_station` on 0 of 85 platforms |
| Route types | 0: 3, 3: 101 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram A (`A`) | `A` | E30613 | 25 | 19 (76%) |
| Tram B (`B`) | `B` | 00569D | 18 | 18 (100%) |
| Tram C (`C`) | `C` | 379E32 | 19 | 19 (100%) |

**Left out by the commune boundary**: Avrillé: Acacias, Avrillé-Ardenne, Bascule, Bois du Roy, Plateau Mayenne, St-Gilles.

- `feed_info.txt` self-attests; its publisher field carries the brand and is never quoted on the page.
- Line A runs north out of the commune to Avrillé (6 stops); B and C stay inside.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 1,183 / 876 / 493 | |
| Storefronts | 2,552 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 2,380 | |

Against OpenStreetMap in the commune: **1.48×** overall (retail 1.24×, food 1.66×, personal 2.08×). Masked at source (non-diffusible): **13.5%** of the screen's denominator; coordinates joined for 99.8%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: **ODbL 1.0 under the National Access Point's Conditions Particulières (read 2026-09-29)**: a §4.3 notice in `app/components.py` `_NOTICES` naming this database and its producer (Tisséo's and STAR's entries are the model; neither discharges this one), and the station table a **pure extract**: nothing renamed, nothing merged, no mean coordinate.
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 3 Angers Loire Métropole lines, **Tram A, Tram B and Tram C**.
- **Scope**: the **commune of Angers**; 6 stops left out, named above.
- **{Share} non-diffusible**: ~14% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.7× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **390 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **No `parent_station` column**: stations are the first platform per unchanged name (85 platforms, 42 stations). ODbL: nothing merged, nothing renamed.
- **Colours are the feed's `route_color`** (A E30613, B 00569D, C 379E32): data under the ODbL, not a mark; nothing is taken from the network's website.
- **After step 3, grep the outputs and the page for the brand** (case-insensitive): it must appear nowhere the app shows. `provenance.json` keeps the NAP dataset's own title and the feed's publisher field as records; the page reads only dates from it.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "angers-nap-licence",
    "claim": "The NAP dataset `Réseau urbain Irigo` declares `odc-odbl` (ODbL 1.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/6178cee254e3b3f0744a1318",
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
    "id": "angers-feed-files",
    "claim": "The feed carries shapes.txt and feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/32f30b64-33f7-43bb-9b6f-34c21c2f83a3",
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
    "id": "angers-feed-window",
    "claim": "feed_info.txt declares a current window (ended 20261228 on 2026-09-30's copy; the feed rolls, so a failure means refetch, not alarm)",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/32f30b64-33f7-43bb-9b6f-34c21c2f83a3",
    "expect": "current"
  },
  {
    "id": "angers-mode-flags",
    "claim": "What the feed types as tram (0), metro (1): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/32f30b64-33f7-43bb-9b6f-34c21c2f83a3",
    "expect": {
      "0": 3,
      "1": 0
    }
  },
  {
    "id": "angers-stations",
    "claim": "brief_check's own count for the kept route_ids today (3 routes; 85 platforms; parent_station populated: False; 42 stations). The pure-extract table in the brief can differ where parents are partial or share names",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/32f30b64-33f7-43bb-9b6f-34c21c2f83a3",
    "route_ids": [
      "A",
      "B",
      "C"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 42,
    "expect_parent_station_populated": false
  },
  {
    "id": "angers-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 49007's real contour, 44.4 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/49007?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 44.0,
    "max": 44.9
  },
  {
    "id": "angers-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
