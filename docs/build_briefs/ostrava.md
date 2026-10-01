# Ostrava — build brief

**Step 0 measured 2026-09-27 (the Czech second-city screen) and 2026-09-30
(this brief, on live OpenStreetMap).** Run `python scripts/brief_check.py ostrava`
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
| **Scope** | **Obec Ostrava** | See the rail section |
| **Lines drawn** | Trams 1–4, 6–8, 10–12, 14, 15, 17 and 18 (OSM) | |
| **Rings** | halved: median gap 424 m | The owner's spacing rule (`docs/ring_rules.md`) |
| **Call (approved): Line 5** | **Out**: a suburban stub, 3 of 10 stops inside (30%); costs two stops | |
| **Call (approved): Lines 9 and 19** | **Not drawn**: relations with no stop members | |
| **Call (approved): Colours** | the project's palette, `line_colour_search.py`, evenly spaced hues | |

---

## The one-line summary

**Prague's modules with obec 554821, trams from OSM, and one line to leave out.** Ostrava has no metro. Its tram network is one of the country's largest, and the business leg is the national chain.

| | **Ostrava** |
|---|---|
| Obec (RÚIAN / ROS02 `PKODADM`) | **554821** |
| Rail | **Trams only**, Dopravní podnik Ostrava: lines 1–4, 6–8, 10–12, 14, 15, 17, 18 (OSM), plus line 5 (below) |
| Stations in scope | **96 stop names inside the city** (OSM, 2026-09-30) |
| Median station gap | **424 m**, so halved rings (0.05 / 0.1 / 0.2 / 0.3 mi) |
| Projected CRS | ⚠️ **EPSG:32634 (UTM 34N)**: Ostrava is at 18.29° E, past the 18° line. Not Prague's or Brno's 33N |
| Storefronts placed (screen) | **3,971**: retail 1,309 · food 1,101 · personal services 1,561 |

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

- 13,340 active establishments in the obec; 4,178 storefront rows, and 3,971 after the own-seat exclusion. Natural persons: 2,334 (55.9%); 207 at their own seat excluded (5.0%).
- **The restaurant control:** 1,092 at NACE 5611 is 2.23× OSM's restaurants, high against Prague's 1.6×, because OSM is thin here. Read the ratio as OSM's gap, not the register's.
- **RÚIAN coordinate control, measured 2026-09-30** (OSM's town-hall node, a position independent of the file):

  ```python
  RUIAN_CRS_CONTROL = ("3182860", 49.84130, 18.28927, "Magistrát města Ostravy, 30. dubna 635/35")
  ```

  RÚIAN transforms it to 49.84131, 18.28926. The file is `20260831_OB_554821_ADR.csv.zip`, cached in `data/ostrava/raw/`.

**The natural-person rule is Prague's**: an establishment at its owner's own
registered seat is excluded, and names are suppressed for the natural-person
forms (`NAME_SUPPRESSED_FORMS`).

---

## Rail — trams from OpenStreetMap

- **No GTFS used.** The screen found no reachable feed, so the lines come from OSM (`osm-rail`): 33–34 route=tram relations in the box (34 on 2026-09-30 here, 33 with 18 refs on the kit's check the same day) (overpass-api.de, 2026-09-30), every one tagged `operator` Dopravní podnik Ostrava.
- **Every regular line keeps all its stops inside the city**, 15 to 28 stop names each.
- ⚠️ **Line 5 is the suburban line to Budišovice**: 3 of its 10 stops inside (30%), below every stub precedent (Toulouse 52%; Minneapolis and Pittsburgh 42%, owner). One of the three, Poruba,Vřesinská, is on other lines. The other two are Poruba,koupaliště and Krásné Pole.
- **Lines 9 and 19** have relations but no stop members in OSM (special or peak services). Place them as not drawn, or read their stops at the build; step 1 refuses an unplaced relation.
- One relation, "Tram 11: Poruba,vozovna → Zábřeh", carries no ref: a line 11 variant. Place it by name, as not drawn.

---

## Licences

- **ROS02, RES and RÚIAN**: read for Prague, CC BY 4.0, permitted with
  conditions. They carry Prague's display obligations and transformation
  notices (`docs/build_briefs/prague.md`, "Licence").
- **The trams, from OpenStreetMap** (`osm-rail`): ODbL. The basemap's
  credit is already on every page; say that the lines and stops come from
  OSM. 
- **Line colours: none in OSM** (every relation's `colour` is empty,
  2026-09-30). Dopravní podnik Ostrava's printed network plan uses line colours, but it is not a licensed source. Choose a palette, Le Havre's precedent, and
  check contrast with `check_map_markup.py`. Never take colours from an
  operator's site without a licence read.

## Build-time calls

1. **Line 5: recommend leaving it out**, as a suburban stub at 30% inside. That loses two stops (Poruba,koupaliště, Krásné Pole); the alternative is to draw it to its end and ring its three stops.
2. **Lines 9 and 19**: out, unless their stops are read.
3. **The palette** (approved, owner 2026-09-30): choose at the build with `scripts/line_colour_search.py` (3:1 contrast on both map pages, CIE76 45 or more from every pin), aiming at evenly spaced hues, since no operator hue is licensed.
4. **The UTM zone is 34N**, set per city and never copied.

```brief-checks
[
  {
    "id": "ostrava-ruian-atom-554821",
    "claim": "ČÚZK's ATOM service resolves obec 554821's RÚIAN address file",
    "kind": "http_contains",
    "url": "https://atom.cuzk.gov.cz/get.ashx?theme=RUIAN-CSV-ADR-OB&spatial_dataset_identifier_code=CZ-00025712-CUZK_RUIAN-CSV-ADR-OB_554821",
    "present": [
      "554821"
    ]
  },
  {
    "id": "ostrava-osm-tram-refs",
    "claim": "OSM carries the drawn tram lines as route=tram relations by ref in the scope's box (15 refs with stops, 2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      49.73,
      18.1,
      49.91,
      18.38
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
        "7",
        "8",
        "10",
        "11",
        "12",
        "14",
        "15",
        "17",
        "18"
      ]
    }
  },
  {
    "id": "ostrava-projected-crs",
    "claim": "The derived UTM zone is 34N (EPSG:32634)",
    "kind": "utm_zone_from_longitude",
    "lon": 18.29,
    "expect": "EPSG:32634",
    "mode": "tram",
    "coverage": "full",
    "scope": "obec",
    "crs": "EPSG:32634",
    "obec_codes": [
      "554821"
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
