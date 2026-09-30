# Plzeň — build brief

**Step 0 measured 2026-09-27 (the Czech second-city screen) and 2026-09-30
(this brief, on live OpenStreetMap).** Run `python scripts/brief_check.py plzen`
before writing code. T1 on the tram list: trams-only maps approved by the owner
on 2026-09-29. Read `docs/build_briefs/brno.md` first: the Czech tram pattern,
built on Prague's modules.



---

## For the owner, with the build

**Approved (owner, 2026-09-30; DECISIONS "The Czech batch's calls and prose approved as recommended")**: every call below as recommended, and the prose. **Build order: Brno, Plzeň, Olomouc, Ostrava, Liberec, Most.** Builds wait for the owner's explicit go.

| | Proposed | Why |
|---|---|---|
| **`mode`** (macro dot colour) | **`tram`** | Street trams, no metro |
| **`coverage`** (macro dot fill) | **`full`** | All three buckets |
| **Scope** | **Obec Plzeň** | See the rail section |
| **Lines drawn** | Trams 1, 2 and 4 (OSM) | |
| **Rings** | halved: median gap 294 m | The owner's spacing rule (`docs/ring_rules.md`) |
| **Call (approved): Colours** | the project's palette, `line_colour_search.py`, evenly spaced hues | |

---

## The one-line summary

**Prague's modules with obec 554791, three tram lines, every stop inside the city.** The smallest-network Czech city after Olomouc, and the cleanest scope: nothing to cut.

| | **Plzeň** |
|---|---|
| Obec | **554791** |
| Rail | **Trams only**, PMDP: lines 1, 2 and 4 |
| Stations in scope | **53 stop names, all inside** (OSM, 2026-09-30); lines 1 · 2 · 4 keep 19 · 23 · 19 |
| Median station gap | **294 m**, so halved rings |
| Projected CRS | **EPSG:32633** (13.38° E) |
| Storefronts placed (screen) | **3,513**: retail 1,225 · food 863 · personal services 1,425 |

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

- 11,114 active establishments; 3,812 storefront rows, 3,513 after the own-seat exclusion. Natural persons 2,345 (61.5%); 299 at their own seat excluded.
- **The restaurant control:** 852 at NACE 5611, 1.99× OSM.
- **RÚIAN coordinate control, measured 2026-09-30:**

  ```python
  RUIAN_CRS_CONTROL = ("24570222", 49.74836, 13.37775, "Magistrát města Plzně, náměstí Republiky 1/1")
  ```

  RÚIAN transforms it to 49.74812, 13.37771 (0.0002° from OSM's node). File `20260831_OB_554791_ADR.csv.zip`, cached in `data/plzen/raw/`.

**The natural-person rule is Prague's**: an establishment at its owner's own
registered seat is excluded, and names are suppressed for the natural-person
forms (`NAME_SUPPRESSED_FORMS`).

---

## Rail — trams from OpenStreetMap

- **OSM** (`osm-rail`): lines 1, 2 and 4, plus relations with no stop members: 1X, 4X and a depot run from Vozovna Slovany. Place those three as not drawn.
- **PMDP's GTFS, READ 2026-09-30: PERMITTED** (the record contradicts itself, CC BY in the description against no-rights terms on the distribution; either permits use). It is `https://jizdnirady.pmdp.cz/jr/gtfs` (GET only; HEAD fails), valid 2026-09-22 to 2027-03-25, with trams as route_type 0, lines 1, 2 and 4. **But it has no `route_color` and no `shapes.txt`**, so it cannot draw the lines. Use it as the stop-name cross-check (gate 3) only, or not at all.

---

## Licences

- **ROS02, RES and RÚIAN**: read for Prague, CC BY 4.0, permitted with
  conditions. They carry Prague's display obligations and transformation
  notices (`docs/build_briefs/prague.md`, "Licence").
- **The trams, from OpenStreetMap** (`osm-rail`): ODbL. The basemap's
  credit is already on every page; say that the lines and stops come from
  OSM. If the PMDP feed is used as a cross-check, credit it too, meeting the stricter CC BY reading: "Plzeňské městské dopravní podniky, a.s. (PMDP), GTFS published by the Statutory City of Plzeň at opendata.plzen.eu, CC BY 4.0, modified by this project." Never the city's coat of arms or PMDP's logo.
- **Line colours: none in OSM** (every relation's `colour` is empty,
  2026-09-30). PMDP's feed carries none either. Choose a palette, Le Havre's precedent, and
  check contrast with `check_map_markup.py`. Never take colours from an
  operator's site without a licence read.

## Build-time calls

1. **OSM for lines and stops**, the feed as a cross-check (recommended).
2. **The palette** (approved, owner 2026-09-30): choose at the build with `scripts/line_colour_search.py` (3:1 contrast on both map pages, CIE76 45 or more from every pin), aiming at evenly spaced hues, since no operator hue is licensed.

```brief-checks
[
  {
    "id": "plzen-ruian-atom-554791",
    "claim": "ČÚZK's ATOM service resolves obec 554791's RÚIAN address file",
    "kind": "http_contains",
    "url": "https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_554791",
    "present": [
      "554791"
    ]
  },
  {
    "id": "plzen-osm-tram-refs",
    "claim": "OSM carries the drawn tram lines as route=tram relations by ref in the scope's box (lines 1, 2 and 4, 2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      49.68,
      13.27,
      49.81,
      13.48
    ],
    "routes": [
      "tram"
    ],
    "require_refs": {
      "tram": [
        "1",
        "2",
        "4"
      ]
    }
  },
  {
    "id": "plzen-projected-crs",
    "claim": "The derived UTM zone is 33N (EPSG:32633)",
    "kind": "utm_zone_from_longitude",
    "lon": 13.38,
    "expect": "EPSG:32633",
    "mode": "tram",
    "coverage": "full",
    "scope": "obec",
    "crs": "EPSG:32633",
    "obec_codes": [
      "554791"
    ],
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED",
      "obec_codes": "OBEC_CODES"
    }
  }
]
```
