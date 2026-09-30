# Olomouc — build brief

**Step 0 measured 2026-09-27 (the Czech second-city screen) and 2026-09-30
(this brief, on live OpenStreetMap).** Run `python scripts/brief_check.py olomouc`
before writing code. T1 on the tram list: trams-only maps approved by the owner
on 2026-09-29. Read `docs/build_briefs/brno.md` first: the Czech tram pattern,
built on Prague's modules.



---

## The one-line summary

**Prague's modules with obec 500496, seven tram lines wholly inside the city, drawn from OSM (owner, 2026-09-30).**

| | **Olomouc** |
|---|---|
| Obec | **500496** |
| Rail | **Trams only**, DPMO: lines 1–7 |
| Stations in scope | **36 stop names, all inside** (OSM, 2026-09-30) |
| Median station gap | **318 m**, so halved rings |
| Projected CRS | **EPSG:32633** (17.25° E) |
| Storefronts placed (screen) | **2,246**: retail 811 · food 620 · personal services 815 |

**Region: `"Europe"`.** **Macro legend (proposed)**: `mode` tram, `coverage` full.

---

## Business leg — the national chain, unchanged

Screened 2026-09-27 with `czechia_register.build_storefronts` on a stub config
(`data/_staging_scratch_2026-09-27/second_cities/czechia/business_leg.py`,
`business_results.json`). The register is ROS02's establishments with RES's
activity and legal form, joined to RÚIAN's obec file. **Placement is 100% in
every Czech city screened.** Currency: ROS02's `DATPLAT` is 2026-08-31, and
closed establishments leave by `DATUKON`. The national files are cached once
in the main checkout's `data/czechia/raw/`, shared with Prague and Brno; never
refresh them from a city branch.

- 7,283 active establishments; 2,469 storefront rows, 2,246 after the own-seat exclusion. Natural persons 1,408 (57.0%); 223 at their own seat excluded.
- **The restaurant control:** 616 at NACE 5611, 1.80× OSM.
- **RÚIAN coordinate control, measured 2026-09-30** (OSM's house point through Nominatim):

  ```python
  RUIAN_CRS_CONTROL = ("25321960", 49.59393, 17.25164, "Olomouc Town Hall, Horní náměstí 583")
  ```

  File `20260831_OB_500496_ADR.csv.zip`, cached in `data/olomouc/raw/`.

**The natural-person rule is Prague's**: an establishment at its owner's own
registered seat is excluded, and names are suppressed for the natural-person
forms (`NAME_SUPPRESSED_FORMS`).

---

## Rail — trams from OpenStreetMap

- **OSM, by the owner's call (2026-09-30).** DPMO's GTFS (`dpmo.cz/doc/dpmo-olomouc-cz.zip`) was read the same day. The publisher states nothing, and permission would rest only on a reading of zákon 106/1999 §4b. Its `route_color` is FFFFFF on every route anyway. OSM avoids the question.
- **Lines 1–7 each keep every stop inside the city**: 11, 14, 16, 20, 10, 14 and 14 stop names.

---

## Licences

- **ROS02, RES and RÚIAN**: read for Prague, CC BY 4.0, permitted with
  conditions. They carry Prague's display obligations and transformation
  notices (`docs/build_briefs/prague.md`, "Licence").
- **The trams, from OpenStreetMap** (`osm-rail`): ODbL. The basemap's
  credit is already on every page; say that the lines and stops come from
  OSM. DPMO's feed is not used, so there is no feed credit.
- **Line colours: none in OSM** (every relation's `colour` is empty,
  2026-09-30). DPMO's feed carries only white. Choose a palette, Le Havre's precedent, and
  check contrast with `check_map_markup.py`. Never take colours from an
  operator's site without a licence read.

## Build-time calls

1. **The palette** (below).

```brief-checks
[
  {
    "id": "olomouc-ruian-atom-500496",
    "claim": "ČÚZK's ATOM service resolves obec 500496's RÚIAN address file",
    "kind": "http_contains",
    "url": "https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_500496",
    "present": [
      "500496"
    ]
  },
  {
    "id": "olomouc-osm-tram-refs",
    "claim": "OSM carries the drawn tram lines as route=tram relations by ref in the scope's box (lines 1–7, 2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      49.53,
      17.16,
      49.66,
      17.4
    ],
    "routes": [
      "tram"
    ],
    "require_refs": {
      "tram": [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7"
      ]
    }
  },
  {
    "id": "olomouc-projected-crs",
    "claim": "The derived UTM zone is 33N (EPSG:32633)",
    "kind": "utm_zone_from_longitude",
    "lon": 17.25,
    "expect": "EPSG:32633"
  }
]
```
