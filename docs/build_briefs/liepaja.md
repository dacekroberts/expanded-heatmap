# Liepāja — build brief

**Step 0 measured 2026-09-27 (the Latvian second-city screen) and 2026-09-30
(this brief, on live OpenStreetMap).** Run `python scripts/brief_check.py liepaja`
before writing code. T1 on the tram list: trams-only maps approved by the owner
on 2026-09-29. **Riga is the template** (built 2026-09-24 on its trams, the
first trams-only city): read `pipeline/riga/config.py` and Riga's page first.

---

## The one-line summary

**Riga's two layers with ATVK 0005000, and one tram line whose OSM route relations miss both ends' newest stops.**

| | **Liepāja** |
|---|---|
| ATVK | **0005000** (OSM relation 13048685, 68 km²) |
| Rail | **one tram line, ref 1** (OSM) |
| Stations in scope | **18 stop names**: 15 on OSM's routes, plus Brīvības iela and Klaipēdas iela (below) |
| Median station gap | **329 m** over the 15, so halved rings |
| Projected CRS | ⚠️ **EPSG:32634 (UTM 34N)**: 21.0° E. Not Riga's 35N |
| Storefronts (screen) | food **131** (93.9% placed) + shops and services **583** (100%) |
| In a ring | **69.7%** within 483 m (the screen) |

**Region: `"Europe"`.** **Macro legend (proposed)**: `mode` tram, `coverage`
as Riga's (the same two layers, and the same thin food layer).

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
   placed on the building footprint by cadastre number (`0005000_kk_shp.zip`,
   cached in `data/liepaja/raw/`).

- **Food: 131** excise-licensed places, 93.9% placed on `aw_eka.csv` (to fetch into `data/liepaja/raw/`; Daugavpils's copy is the same national file).
- **Shops and services: 583**, 100% placed on the cadastre (`0005000_kk_shp.zip`, cached).

**Currency:** the excise register and the cadastre are updated daily
(2026-09-29 and 09-28, the Phase 2 audit), and an expired licence leaves by
its status. **The food layer is thin by construction.** It is places licensed
to sell alcohol, as on Riga's page; say so there as Riga's page does.

---

## Rail — trams from OpenStreetMap

- **OSM** (`osm-rail`): two route=tram relations, ref 1 ("Mirdzas Ķempes iela – Brīvības iela" each way), with 12 and 14 stop members and 15 stop names.
- ⚠️ **Two tagged tram stops are on no route relation: Brīvības iela, the line's named terminus, and Klaipēdas iela.** The relations are incomplete, not the service. **Add both by name** (Odense's SDU Syd/Hospital Nord precedent), which gives the screen's 18.
- **Frequency** about every 7 minutes (the screen), disclosed.
- **No `colour`**: choose one.

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

1. **Brīvības iela and Klaipēdas iela added by name.**
2. **The line colour.**
3. **UTM 34N**, set per city.
4. **The VZD credit.**

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
    "id": "liepaja-cadastre-0005000",
    "claim": "VZD's cadastral map dataset lists Liepāja's file (0005000_kk_shp.zip)",
    "kind": "http_contains",
    "url": "https://data.gov.lv/dati/api/3/action/package_show?id=b28f0eed-73b0-4e44-94e7-b04b11bf0b69",
    "present": [
      "0005000_kk_shp.zip"
    ]
  },
  {
    "id": "liepaja-osm-tram-ref",
    "claim": "OSM carries Liepāja's tram as route=tram relations with ref 1 (2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      56.47,
      20.96,
      56.61,
      21.11
    ],
    "routes": [
      "tram"
    ],
    "require_refs": {
      "tram": [
        "1"
      ]
    }
  },
  {
    "id": "liepaja-projected-crs",
    "claim": "Liepāja (21.0 E) is in UTM 34N (EPSG:32634), not Riga's 35N",
    "kind": "utm_zone_from_longitude",
    "lon": 21.01,
    "expect": "EPSG:32634"
  }
]
```
