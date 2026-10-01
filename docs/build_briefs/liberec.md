# Liberec (Regional) — build brief

**Step 0 measured 2026-09-27 (the Czech second-city screen) and 2026-09-30
(this brief, on live OpenStreetMap).** Run `python scripts/brief_check.py liberec`
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
| **Scope** | **Liberec (Regional): Liberec + Jablonec nad Nisou** | See the rail section |
| **Lines drawn** | Trams 2, 3, 5 and 11 (OSM) | |
| **Rings** | halved: median gap 378 m | The owner's spacing rule (`docs/ring_rules.md`) |
| **Call (approved): Scope** | **Regional, with Jablonec**: every line whole, +618 storefronts; Liberec alone passes at 67% | |
| **Call (approved): Colours** | the project's palette, `line_colour_search.py`, evenly spaced hues | |

---

## The one-line summary

**Prague's modules over two obce, Liberec and Jablonec nad Nisou, joined by the interurban tram line 11.** Liberec alone passes too; the scope is the owner's call.

| | Liberec alone | **With Jablonec nad Nisou (recommended)** |
|---|---|---|
| Obce | 563889 | **563889 + 563510** |
| Rail | Trams 2, 3, 5 and 11 (DPMLJ) | same |
| Stop names in scope | 32 | **39** (line 11 adds 7 in Jablonec) |
| Worst line | 11: 14 of 21 (67%) | **every line whole** |
| Median station gap | — | **378 m**, so halved rings |
| Storefronts placed (screen) | 1,880 | **2,498** (Jablonec 618) |
| Projected CRS | **EPSG:32633** (15.06° E) | same |

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

- **Liberec:** 6,220 active establishments; 1,880 placed (retail 693 · food 458 · personal 729). Natural persons 57.9%; 162 at their own seat excluded. **Jablonec:** 618 placed (retail 244 · food 141 · personal 233); 121 at their own seat excluded (16.4%).
- **The restaurant control:** 448 + 139 at NACE 5611, 2.45× OSM.
- **RÚIAN coordinate controls, one per obec** (the config takes one; a regional build reads two files, so declare the control per file):

  ```python
  RUIAN_CRS_CONTROL = ("23653124", 50.77000, 15.05845, "Liberec Town Hall, nám. Dr. E. Beneše 1/1")
  ```

  Liberec's transforms within 0.0004° of OSM's square. **Jablonec's, measured 2026-09-30** (its town hall, against OSM's square): `("12188018", 50.72452, 15.17128, "Jablonec Town Hall, Mírové náměstí 3100/19")`, within 0.0005° of the square's OSM points. Files `20260831_OB_563889_ADR.csv.zip` (`data/liberec/raw/`) and `20260831_OB_563510_ADR.csv.zip` (fetched to scratch 2026-09-30; the build fetches its own).
- ⚠️ **`czechia_register` reads ONE obec.** A two-obec scope means calling it per obec and concatenating: Monterrey's and Kitchener–Waterloo's regional precedent, in shared code, not a fork.

**The natural-person rule is Prague's**: an establishment at its owner's own
registered seat is excluded, and names are suppressed for the natural-person
forms (`NAME_SUPPRESSED_FORMS`).

---

## Rail — trams from OpenStreetMap

- **DPMLJ's GTFS reset the connection** on the screen, so OSM (`osm-rail`): lines 2, 3, 5 and 11, 8 relations.
- **Line 11** is the Liberec–Jablonec interurban: 21 stop names, 14 in Liberec and 7 in Jablonec.

---

## Licences

- **ROS02, RES and RÚIAN**: read for Prague, CC BY 4.0, permitted with
  conditions. They carry Prague's display obligations and transformation
  notices (`docs/build_briefs/prague.md`, "Licence").
- **The trams, from OpenStreetMap** (`osm-rail`): ODbL. The basemap's
  credit is already on every page; say that the lines and stops come from
  OSM. 
- **Line colours: none in OSM** (every relation's `colour` is empty,
  2026-09-30). DPMLJ's network plan is not a licensed source. Choose a palette, Le Havre's precedent, and
  check contrast with `check_map_markup.py`. Never take colours from an
  operator's site without a licence read.

## Build-time calls

1. **The scope: recommend Liberec (Regional) with Jablonec.** Every line whole, 618 more storefronts, one more line end ringed. Liberec alone passes (67%) if the owner prefers one obec.
2. **Jablonec's RÚIAN control**: measured (above).
3. **The palette** (approved, owner 2026-09-30): choose at the build with `scripts/line_colour_search.py` (3:1 contrast on both map pages, CIE76 45 or more from every pin), aiming at evenly spaced hues, since no operator hue is licensed.

```brief-checks
[
  {
    "id": "liberec-ruian-atom-563889",
    "claim": "ČÚZK's ATOM service resolves obec 563889's RÚIAN address file",
    "kind": "http_contains",
    "url": "https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_563889",
    "present": [
      "563889"
    ]
  },
  {
    "id": "liberec-ruian-atom-563510",
    "claim": "ČÚZK's ATOM service resolves obec 563510's RÚIAN address file",
    "kind": "http_contains",
    "url": "https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_563510",
    "present": [
      "563510"
    ]
  },
  {
    "id": "liberec-osm-tram-refs",
    "claim": "OSM carries the drawn tram lines as route=tram relations by ref in the scope's box (lines 2, 3, 5 and 11, 2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      50.69,
      14.95,
      50.82,
      15.22
    ],
    "routes": [
      "tram"
    ],
    "require_refs": {
      "tram": [
        "2",
        "3",
        "5",
        "11"
      ]
    }
  },
  {
    "id": "liberec-projected-crs",
    "claim": "The derived UTM zone is 33N (EPSG:32633)",
    "kind": "utm_zone_from_longitude",
    "lon": 15.06,
    "expect": "EPSG:32633",
    "mode": "tram",
    "coverage": "full",
    "scope": "regional",
    "crs": "EPSG:32633",
    "obec_codes": [
      "563889",
      "563510"
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
