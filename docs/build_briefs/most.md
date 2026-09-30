# Most and Litvínov (Regional) — build brief

**Step 0 measured 2026-09-27 (the Czech second-city screen) and 2026-09-30
(this brief, on live OpenStreetMap).** Run `python scripts/brief_check.py most`
before writing code. T1 on the tram list: trams-only maps approved by the owner
on 2026-09-29. Read `docs/build_briefs/brno.md` first: the Czech tram pattern,
built on Prague's modules.



---

## The one-line summary

**The joint scope is required: Most alone fails the stub test.** Four lines run between the two towns; together every line is whole. Small: about 1,030 storefronts.

| | Most alone | **Most + Litvínov (required)** |
|---|---|---|
| Obce | 567027 | **567027 + 567256** |
| Rail | Trams 1–4 (DPmML) | same |
| Stop names in scope | lines keep 12 of 24, 6 of 18, 9 of 21 | **27, every line whole** |
| Median station gap | — | **514 m**, so halved rings (under 550) |
| Storefronts placed (screen) | 789 | **1,030** (Litvínov 241) |
| Projected CRS | **EPSG:32633** (13.64° E) | same |

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

- **Most:** 2,388 active establishments; 789 placed (retail 326 · food 212 · personal 251). Natural persons 62.7%. **Litvínov:** 241 placed (103 · 55 · 83); 44 at their own seat excluded (15.4%).
- **The restaurant control:** 212 + 55 at NACE 5611, 3.71× OSM, which is thin here.
- **RÚIAN coordinate control (Most), measured 2026-09-30:**

  ```python
  RUIAN_CRS_CONTROL = ("25298429", 50.50284, 13.64078, "Most Town Hall (Magistrát), Radniční 1/2")
  ```

  RÚIAN transforms it to 50.50287, 13.64052. ⚠️ **Litvínov's control is still to measure** at the build.
- ⚠️ **Two obce**: as Liberec (Regional), call `czechia_register` per obec.

**The natural-person rule is Prague's**: an establishment at its owner's own
registered seat is excluded, and names are suppressed for the natural-person
forms (`NAME_SUPPRESSED_FORMS`).

---

## Rail — trams from OpenStreetMap

- **OSM** (`osm-rail`): lines 1–4, 8 relations. Per town: line 1 12 + 12, line 2 11 + 0, line 3 6 + 12, line 4 9 + 12.
- **The spacing is the widest on the Czech list** (514 m), a tram line running between two towns, just under the 550 m line.

---

## Licences

- **ROS02, RES and RÚIAN**: read for Prague, CC BY 4.0, permitted with
  conditions. They carry Prague's display obligations and transformation
  notices (`docs/build_briefs/prague.md`, "Licence").
- **The trams, from OpenStreetMap** (`osm-rail`): ODbL. The basemap's
  credit is already on every page; say that the lines and stops come from
  OSM. 
- **Line colours: none in OSM** (every relation's `colour` is empty,
  2026-09-30).  Choose a palette, Le Havre's precedent, and
  check contrast with `check_map_markup.py`. Never take colours from an
  operator's site without a licence read.

## Build-time calls

1. **Build it at all?** It is T1 and passes, but it is **the smallest Czech page** (1,030 storefronts, 27 stops), and the screen marked it low value. Recommend building it last of the six, or asking the owner then.
2. **Litvínov's RÚIAN control** at the build.
3. **The palette** (below).

```brief-checks
[
  {
    "id": "most-ruian-atom-567027",
    "claim": "ČÚZK's ATOM service resolves obec 567027's RÚIAN address file",
    "kind": "http_contains",
    "url": "https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_567027",
    "present": [
      "567027"
    ]
  },
  {
    "id": "most-ruian-atom-567256",
    "claim": "ČÚZK's ATOM service resolves obec 567256's RÚIAN address file",
    "kind": "http_contains",
    "url": "https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_567256",
    "present": [
      "567256"
    ]
  },
  {
    "id": "most-osm-tram-refs",
    "claim": "OSM carries the drawn tram lines as route=tram relations by ref in the scope's box (lines 1–4, 2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      50.46,
      13.49,
      50.62,
      13.71
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
    "id": "most-projected-crs",
    "claim": "The derived UTM zone is 33N (EPSG:32633)",
    "kind": "utm_zone_from_longitude",
    "lon": 13.64,
    "expect": "EPSG:32633"
  }
]
```
