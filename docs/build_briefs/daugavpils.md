# Daugavpils — build brief

**Step 0 measured 2026-09-27 (the Latvian second-city screen) and 2026-09-30
(this brief, on live OpenStreetMap).** Run `python scripts/brief_check.py daugavpils`
before writing code. T1 on the tram list: trams-only maps approved by the owner
on 2026-09-29. **Riga is the template** (built 2026-09-24 on its trams, the
first trams-only city): read `pipeline/riga/config.py` and Riga's page first.

---

## For the owner, with the build

**Approved (owner, 2026-09-30; the 24 calls in `docs/handoff_tram_kit_2026-09-30.md`, cdee504)**: every call below as recommended, and the page-text template. Builds wait for the owner's explicit go.

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams, no metro |
| **`coverage`** (macro dot fill) | **`narrowed`** | Riga's two layers, merged (Riga is `narrowed`) |
| **Scope** | **Daugavpils (ATVK 0002000)** | See the rail section |
| **Lines drawn** | Route 1 only (see the call); routes 2–5 on the owner's word | |
| **Rings** | halved: median gap 298 m over all 38 stops (recompute for the lines drawn) | The owner's spacing rule (`docs/ring_rules.md`) |
| **Call (approved): Routes drawn** | **Route 1 only** (every 10–15 min by day). Routes 3 and 5 (one loop, each direction every 20–30 min), 2 (gaps of an hour or more) and 4 (hourly) fail the kit's 20-minute rule (Buffalo's flat 20 is the slowest drawn); stops served only by them go to `excluded_stations.csv` as infrequent | |
| **Call (approved): Colours** | chosen at build | |

---

## The one-line summary

**Riga's two layers with ATVK 0002000, placed on VZD's address file, and five tram routes from OSM.** Latvia's second city; Daugavpils Satiksme runs its trams, and there is no other urban rail.

| | Riga (built) | **Daugavpils** |
|---|---|---|
| ATVK | 0001000 | **0002000** (OSM relation 13048683, 72 km²) |
| Rail | trams 1, 5, 7, 8, 10, 11 and 14 (GTFS) | **trams 1–4 (OSM)**, all inside the city |
| Stations in scope | Riga's | **38 stop names** |
| Median station gap | — | **298 m**, so halved rings |
| Projected CRS | EPSG:32635 | **EPSG:32635** (26.5° E) |
| Storefronts (screen) | Riga's | food **98** (95.9% placed) + shops and services **722** (100%) |
| In a ring | Riga 77.9% | **81.5%** within 483 m (the screen) |

**Region: `"Europe"`.** **Macro legend (proposed)**: `mode` tram, `coverage`
`narrowed`, as Riga (the same two layers, merged; the same thin food layer).

---

## Business leg — Riga's two layers

The screen (`data/_staging_scratch_2026-09-27/second_cities/latvia/lv_business.py`)
ran Riga's rules on the national files (`pipeline/riga/config.py`):

1. **Food: VID's excise register** (`pdb_akclicences_odata.csv`, cached
   nationally in the main checkout's `data/riga/raw/`). The rows kept are
   current licences (`Spēkā`) at a food place type, one per address and
   kind. **They are placed on VZD's national address file `aw_eka.csv`**,
   a new source for this city (below). The holder and tax-number columns
   are never read (`EXCISE_NEVER`, read by exact name and asserted).
2. **Shops and services: VZD's cadastre premise groups of use class 1230**
   in the city's ATVK. They are name-classified by Riga's `NAME_RULES` and
   placed on the building footprint by cadastre number (`0002000_kk_shp.zip`,
   cached in `data/daugavpils/raw/`).

- **Food: 98** excise-licensed places, 95.9% placed on `aw_eka.csv` (in `data/daugavpils/raw/`).
- **Shops and services: 722** premise groups, 100% placed on the cadastre.

**Currency:** the excise register and the cadastre are updated daily
(2026-09-29 and 09-28, the Phase 2 audit), and an expired licence leaves by
its status. **The food layer is thin by construction.** It is places licensed
to sell alcohol, as on Riga's page; say so there as Riga's page does.

---

## Rail — trams from OpenStreetMap

- **OSM** (`osm-rail`): route=tram relations for refs 1, 2, 3 and 4 (and a line 3 loop, Cietoksnis – Stropu ezers – Ķīmija – Cietoksnis), operator Daugavpils Satiksme. **Every stop is inside the city**: 38 stop names on the routes, and all but one (Stropu ciemats, on the routes but not tagged as a stop) are tagged tram stops.
- **Routes 1–5, of which 3 and 5 are one loop run in opposite directions** (Cietoksnis – Stropu ezers – Ķīmija): OSM tags both as ref 3.
- **Frequency, measured 2026-09-30** (the operator's timetable as published in its GTFS, read for the headway only, Wednesday 2026-10-07, 07–19h, worst hour one way at each route's busiest stop): **route 1 4–6 trams an hour**; **routes 3 and 5 2–3 each**; **route 2 0–3** (hours with none); **route 4 1**. An hourly street tram has no precedent; the tram kit recommends drawing a route only at every 20 minutes or better by day (Buffalo's flat 20 is the slowest drawn), so **route 1 only**, approved: the kit's call 6 draws routes 2–4 only at 20 minutes or better, and the timetable shows none do, so **route 1 only**.
- **No `colour`** on any relation: choose a palette (Le Havre's precedent).

---

## Licences

- **VID's excise register and VZD's cadastre:** read for Riga, as notices
  42 and 43 in `docs/data_sources.md`.
- **VZD's address file `aw_eka.csv`: READ 2026-09-30, PERMITTED WITH
  CONDITIONS (CC BY 4.0).**
  - **The grant is VZD's own open-data terms**
    (`vzd.gov.lv/lv/par-datu-izmantosanas-noteikumiem`): no permission
    needed.
  - **Must display, even as a join layer**, since the dots' coordinates
    come from it:
    - the source, VZD's wording "Izmantoti Valsts adrešu reģistra
      informācijas sistēmas dati" (recommended: add the year, "…dati,
      2026. gads", which also satisfies the permit regime's wording);
    - Valsts zemes dienests, named;
    - a link to CC BY 4.0;
    - **a description of the changes**: addresses matched to VZD
      points, the address file not shown, points aggregated around
      stops.
  - **Must not:** say that VZD approved the changes or the map, or use
    VZD's logo.
  - **The address register's permit regime** (Cabinet Regulation 455,
    point 71; `vzd.gov.lv/lv/datu-izmantosanas-noteikumi`) covers data
    issued on request. VZD's own open-data page resolves that in favour
    of the open file.
  - **Likely path:** extend notice 42 to name the address register.
- **The file:** 141.7 MB, UTF-8 with BOM (the CSVW metadata wrongly says
  ISO-8859-1), daily. Keep `STATUSS` = EKS. ⚠️ **`KOORD_X` is the
  northing and `KOORD_Y` the easting** (EPSG:3059, swapped axes). Prefer
  `DD_N`/`DD_E`, which are degrees.
- **The trams from OSM:** ODbL. The city's GTFS declares no licence, so
  it is not used (Olomouc's case; the owner chose OSM there, 2026-09-30).

## Build-time calls

1. **Routes 1–4 or 1–5**: confirm against the operator's own list.
2. **The palette.**
3. **The VZD credit** (notice 42 extended).

```brief-checks
[
  {
    "id": "vzd-aw-eka-cc-by",
    "claim": "VZD's address register open data (aw_eka.csv) is on data.gov.lv, declared CC-BY-4.0",
    "kind": "http_contains",
    "url": "https://data.gov.lv/dati/api/3/action/package_show?id=varis-atvertie-dati",
    "present": [
      "CC-BY-4.0",
      "aw_eka.csv"
    ]
  },
  {
    "id": "daugavpils-cadastre-0002000",
    "claim": "VZD's cadastral map dataset lists Daugavpils's file (0002000_kk_shp.zip)",
    "kind": "http_contains",
    "url": "https://data.gov.lv/dati/api/3/action/package_show?id=b28f0eed-73b0-4e44-94e7-b04b11bf0b69",
    "present": [
      "0002000_kk_shp.zip"
    ]
  },
  {
    "id": "daugavpils-osm-tram-refs",
    "claim": "OSM carries Daugavpils's trams as route=tram relations with refs 1-4 (2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      55.83,
      26.44,
      55.96,
      26.63
    ],
    "routes": [
      "tram"
    ],
    "require_refs": {
      "tram": [
        "1",
        "2",
        "3",
        "4"
      ]
    }
  },
  {
    "id": "daugavpils-projected-crs",
    "claim": "Daugavpils (26.5 E) is in UTM 35N (EPSG:32635), as Riga",
    "kind": "utm_zone_from_longitude",
    "lon": 26.53,
    "expect": "EPSG:32635",
    "mode": "tram",
    "coverage": "narrowed",
    "scope": "city",
    "crs": "EPSG:32635",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
