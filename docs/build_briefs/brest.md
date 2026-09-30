# Brest — build brief

**Step 0 measured 2026-09-30** by the France kit session: the rail leg from the feed as fetched that day, the business leg from the 2026-09-27 screen (`data/_staging_scratch_2026-09-27/second_cities/france/`). **Run `python scripts/brief_check.py brest` before writing any code**, and build with the `france-tram-city` skill; `python scripts/scaffold_france_batch.py --only brest --dry-run` shows the config it writes.

**Builds APPROVED** (owner, 2026-09-30), in landing groups per `docs/review_time.md`; every call below was approved as this brief recommended it.

---

## The one-line summary

Two Bibus tram lines and the Téléphérique cable car, 39 of 41 stations in the commune; two stops in the feed are track switches.

---

## For the owner, with the build

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams only, no metro (Dublin's and Riga's class) |
| **`coverage`** (macro dot fill) | **`full`** | SIRENE carries all three buckets: 952 retail, 679 food, 360 personal in the commune (screen) |
| **Scope** | **Commune of Brest** | The worst line, A, keeps 28 of 30 stations (93%) in the commune: half or more stays commune-only (Toulouse 52%, Rennes 73%) |
| **Lines drawn** | Tram A, Tram B and Téléphérique | 3 lines from Bibus's feed; public names verified at build |
| **Rings** | 0.05 / 0.1 / 0.2 / 0.3 mi | Median gap between in-scope stations 425 m, under ~550 m (`docs/ring_rules.md`) |
| **Owner call** | **approved** | The cable car |

### Owner calls - APPROVED as recommended (owner, 2026-09-30)

- **The cable car** (route C, `route_type 6`, Jean Moulin - Ateliers across the Penfeld): Toulouse's Téléo is the precedent, drawn by the owner's call 2026-09-23. **Approved: draw it** (owner, 2026-09-30), and the page says "two tram lines and the cable car", one clause added to the template.

---

## Rail — Bibus's feed

| | |
|---|---|
| Source | the operator's own feed on the National Access Point: `Réseau urbain Bibus` |
| Resource | `https://www.data.gouv.fr/api/1/datasets/r/583d1419-058b-481b-b378-449cab744c82` (2,123,683 bytes on 2026-09-30) |
| Licence | **Licence Ouverte 2.0** (`lov2`, declared on the NAP) |
| Validity | `feed_info.txt` self-attests: RD Brest, 2026-09-28 to **2026-12-20** |
| `shapes.txt` | yes |
| Stations | 41 network-wide under the pure-extract rule (the 2 fictitious `FIC_` track-switch stops excluded); `parent_station` on 0 of 76 platforms |
| Route types | 0: 2, 3: 66, 6: 1 |

| Line | route_id(s) today | Colour | Stations | In the commune |
|---|---|---|---|---|
| Tram A (`A`) | `A` | DE007E | 30 | 28 (93%) |
| Tram B (`B`) | `B` | 004F9E | 11 | 11 (100%) |
| Téléphérique (`C`) | `C` | EA6758 | 2 | 2 (100%) |

**Left out by the commune boundary**: Gouesnou: Porte de Gouesnou; Guipavas: Porte de Guipavas.

**Station pairs under 150 m** (read by name, each one): Liberté Quartz / Liberté 49 m; Jean Moulin / Château 100 m.

- `feed_info.txt` self-attests (RD Brest, 2026-09-28 to 2026-12-20).
- Liberté and Liberté Quartz, 49 m apart, are two stops.

---

## Business leg — SIRENE (the 2026-09-27 screen)

| | Commune |
|---|---|
| Retail / Food / Personal | 952 / 679 / 360 | |
| Storefronts | 1,991 | |
| Within 966 m of a station (the screen's measure; the build recounts at 483 m) | 1,845 | |

Against OpenStreetMap in the commune: **1.47×** overall (retail 1.33×, food 1.55×, personal 1.85×). Masked at source (non-diffusible): **10.9%** of the screen's denominator; coordinates joined for 99.9%. Step 2 re-measures all of it: Rennes's and Toulouse's briefs were low on the masked share.

The chain is the five built cities' (`france_register.py`), which reproduced Rennes (3,479) and Toulouse (8,635) exactly at the screen: active is the letter `A`, the per-row `epsg`, `qualite_xy` 33 dropped, both catch-alls (96.09Z, 56.29B) excluded on the French precedent unless this city's shares depart from it.

---

## Notices

- **Transit**: Licence Ouverte 2.0: credit the producer and the data's date in the transit caption, Marseille's and Toulouse's pattern (`Transit data © <producer>, via <portal>` plus the feed window or snapshot date from `provenance.json`). No `_NOTICES` entry is needed. The LO 2.0 feeds were not read one by one; the batch relies on the licence's own text (`docs/licenses/france-licence-ouverte-2.0.md`).
- **Business**: `Source : Insee` verbatim with the SIRENE edition's date, as every French page.
- **Basemap**: © OpenStreetMap contributors, and the OpenStreetMap notice if OSM supplies any geometry.

---

## Page text — the approved template, this city's braces

The owner approved the French tram-city text word for word on 2026-09-29 (the `france-tram-city` skill carries it). This city's braces, as measured so far:

- **{N} {operator} tram lines … {lines}**: 3 Bibus lines, **Tram A, Tram B and Téléphérique**.
- **Scope**: the **commune of Brest**; 2 stops left out, named above.
- **{Share} non-diffusible**: ~11% at the screen; step 2's figure goes on the page.
- **Ratio to OpenStreetMap's restaurants**: ~1.6× at the screen; the build's figure goes on the page.
- **{spacing}**: a median of **425 m** (in scope, 2026-09-30); step 1's figure goes on the page.
- **{share} within a ring**: measured on the rendered map.

---

## Build-time calls, with the recommended answer

- **Two stops are track switches**: `FIC_LIB1` "Aiguillage Ligne A vers B" and `FIC_LIB2` "Aiguillage Ligne B vers A" (fictitious stops, pickup and drop-off refused on 998 of 1,038 stop_times). Not stations: excluded by stop_id, Edmonton's garage precedent. The real count is 39, not 41.

---

## Still unknown

- **Gate 3's independent per-line count** (the operator's stop list or OpenStreetMap's route relations): not taken yet.
- **The build-day feed's route_ids and colours**: feeds are rolling; read them fresh.
- **Legacy INSEE codes** inside the scope's contours (Lille's Lomme and Hellemmes): counted at step 2.

```brief-checks
[
  {
    "id": "brest-nap-licence",
    "claim": "The NAP dataset `Réseau urbain Bibus` declares `lov2` (Licence Ouverte 2.0). The fields beside the check are the brief's proposals, which --vs-config diffs against the built config",
    "kind": "http_contains",
    "url": "https://transport.data.gouv.fr/api/datasets/55ffbe0888ee387348ccb97d",
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
    "id": "brest-feed-files",
    "claim": "The feed carries shapes.txt and feed_info.txt",
    "kind": "gtfs_files",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/583d1419-058b-481b-b378-449cab744c82",
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
    "id": "brest-feed-window",
    "claim": "feed_info.txt declares a current window (ended 20261220 on 2026-09-30's copy; the feed rolls, so a failure means refetch, not alarm)",
    "kind": "gtfs_feed_window",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/583d1419-058b-481b-b378-449cab744c82",
    "expect": "current"
  },
  {
    "id": "brest-mode-flags",
    "claim": "What the feed types as tram (0), metro (1), aerial lift (6): the flags this brief's line selection was read against",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/583d1419-058b-481b-b378-449cab744c82",
    "expect": {
      "0": 2,
      "1": 0,
      "6": 1
    }
  },
  {
    "id": "brest-stations",
    "claim": "brief_check's own count for the kept route_ids today (3 routes; 78 platforms; parent_station populated: False; 43 stations). The pure-extract table in the brief can differ where parents are partial or share names; Brest's 43 includes the two FIC_ track-switch stops",
    "kind": "gtfs_stations",
    "url": "https://www.data.gouv.fr/api/1/datasets/r/583d1419-058b-481b-b378-449cab744c82",
    "route_ids": [
      "A",
      "B",
      "C"
    ],
    "crs": "EPSG:2154",
    "station_spacing_median_m_min": 250,
    "expect_stations": 43,
    "expect_parent_station_populated": false
  },
  {
    "id": "brest-commune-contour",
    "claim": "geo.api.gouv.fr returns commune 29019's real contour, 49.2 km2 (the `geometry=contour` form; `fields=contour` returns a POINT)",
    "kind": "geojson_area_km2",
    "url": "https://geo.api.gouv.fr/communes/29019?geometry=contour&format=geojson",
    "crs": "EPSG:2154",
    "min": 48.7,
    "max": 49.7
  },
  {
    "id": "brest-sirene-published",
    "claim": "The SIRENE establishment dataset is still published (the national parquet every French city reads)",
    "kind": "http_ok",
    "url": "https://www.data.gouv.fr/api/1/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/"
  }
]
```
