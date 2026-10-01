# Florence — build brief

**Screened 2026-09-28 (wave 2's second group, owner); this brief 2026-09-30, on live OpenStreetMap.** Run
`python scripts/brief_check.py florence` before writing code. T1 on the tram
list: trams-only maps approved by the owner on 2026-09-29. **Rings are sized by
the owner's spacing rule and no stop is thinned** (the tram batch's binding
decisions, `docs/handoff_tram_batch_2026-09-29.md`).

---

## For the owner, with the build

**Approved (owner, 2026-09-30; the 24 calls in `docs/handoff_tram_kit_2026-09-30.md`, cdee504)**: every call below as recommended, and the page-text template. Builds wait for the owner's explicit go.

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams, no metro |
| **`coverage`** (macro dot fill) | **`full`** | All three buckets |
| **Scope** | **Comune di Firenze** | See the rail section |
| **Lines drawn** | T1 Leonardo and T2 Vespucci (OSM colours) | |
| **Rings** | halved: median gap 322 m | The owner's spacing rule (`docs/ring_rules.md`) |
| **Call (approved): 639 exempt food rows** | **In**, Milan's precedent (fuori piano included, non-public premises filtered by name, the gap disclosed) | |
| **Call (approved): T3** | not drawn until it opens | |

---

## The one-line summary

**Tramvia T1 and T2 inside the comune, and the Comune's four CC BY 4.0 activity layers with a point on every row but no names.**

| | **Firenze** |
|---|---|
| Rail | **Tramvia T1 Leonardo (`#254395`) and T2 Vespucci (`#5d3988`)**, OSM colours |
| Stations in scope | **39 stop names inside the comune** (OSM relation 42602). T1 keeps 20 of 24 (4 in Scandicci, 83%); T2 19 of 19 |
| Median station gap | **322 m**, so halved rings |
| Projected CRS | **EPSG:32632** (11.25° E); the layers come in EPSG:3003 (Monte Mario / Italy 1) |
| Register | The Comune's layers: commercio in sede fissa, pubblici esercizi, attività estetiche, tintolavanderie |

**Region: `"Europe"`.** **Macro legend (proposed)**: `mode` tram, `coverage` full.

---

## Business leg — the Comune's four layers

GeoJSON on `datigis.comune.fi.it/json/`: `commercio_sede_fissa_od.json`
(7,546), `pubblici_esercizi_od.json` (3,421), `attivita_estetiche_od.json`
(1,495) and `tintolavanderie_od.json` (179). All four were modified
2026-09-30; pubblici esercizi and tintolavanderie are updated daily.

- **The screen:** **7,355 retail, 3,024 food and 1,673 personal services**
  (2.49×, 1.45× and 4.62× OSM). That is after dropping private clubs, internal
  shops, e-commerce, vending and farmers. Coordinates on 100%.
- **No name or address field on any layer**: an id and a type code only. The
  dots show the type.
- ⚠️ **639 food rows are exempt categories** (464 "non soggetta a requisiti
  comunali", 175 art. 53). This is Milan's *fuori piano* question: without
  them, food is 2,385 (1.14×). **A build call**, with Milan's precedent.
- **3,424 rows share a point** (multi-unit buildings). Draw them as they are;
  the heat layer counts each.
- **Privacy:** no names are published. A beauty or laundry point can still be a
  sole trader's premises. The Comune's footer ties personal-data reuse to
  d.lgs. 36/2006; run `check_personal_exposure.py` and bring any doubt to the
  owner.

## Rail — OSM

- **Drawn:** T1 and T2, in their OSM colours. T1's four Scandicci stops are
  outside the comune: drawn to the line's end, not ringed.
- **Not drawn:** T3.2.1, T3.2.2, T2.2 and T4 have relations but no stops
  (under construction; T3 is due at the end of 2026). Place them as not drawn,
  and re-check when T3 opens.
- **GEST's GTFS** (in the Regione Toscana feed, CC BY 4.0 declared) is not
  needed for geometry. If it is used for frequency, read its licence first.

## Licences

- **The Comune's four layers: READ 2026-09-30, PERMITTED WITH CONDITIONS (CC BY
  4.0).**
  - **The grant is the Comune's own Note legali** ("I materiali Open data sono
    liberamente riutilizzabili…"), with CC BY 4.0 on every dataset and every
    distribution.
  - **Credit the Comune di Firenze** (Direzione Attività Economiche e
    Turismo). The Regione's dati.toscana.it only harvests the layers and is
    owed nothing.
  - Link CC BY 4.0.
  - **State the changes: filtered, categorised and aggregated.**
  - Never imply the Comune's endorsement, or use its logo or the giglio.
- **OSM:** ODbL.

## Build-time calls

1. **The 639 exempt food rows**: **in** (recommended), Milan's precedent (the owner included Milan's *fuori piano* register on 2026-09-22 and filtered the nameable non-public premises); say on the page that some non-public premises remain.
2. **T3**: check at the build whether it has opened.

```brief-checks
[
  {
    "id": "florence-pubblici-esercizi-cc-by",
    "claim": "dati.toscana.it lists the Comune's Pubblici Esercizi layer under cc-by-4.0",
    "kind": "http_contains",
    "url": "https://dati.toscana.it/api/3/action/package_show?id=5c136300-59a8-4637-a29b-2d53bcf09e4a",
    "present": [
      "cc-by-4.0"
    ]
  },
  {
    "id": "florence-geojson-serves",
    "claim": "The Comune's pubblici esercizi GeoJSON serves",
    "kind": "http_ok",
    "url": "https://datigis.comune.fi.it/json/pubblici_esercizi_od.json",
    "min_bytes": 100000
  },
  {
    "id": "florence-osm-tram-refs",
    "claim": "OSM carries the streetcar as route=tram relations by ref (T1 and T2, 2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      43.72,
      11.15,
      43.84,
      11.34
    ],
    "routes": [
      "tram"
    ],
    "require_refs": {
      "tram": [
        "T1",
        "T2"
      ]
    }
  },
  {
    "id": "florence-projected-crs",
    "claim": "The derived UTM zone is EPSG:32632",
    "kind": "utm_zone_from_longitude",
    "lon": 11.25,
    "expect": "EPSG:32632",
    "mode": "tram",
    "coverage": "full",
    "scope": "comune",
    "crs": "EPSG:32632",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
