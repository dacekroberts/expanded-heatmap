# Den Haag — build brief

**Screened 2026-09-27 (as a T2 city); the horeca permit layer found and the tier closed 2026-09-30; this brief 2026-09-30, on live
OpenStreetMap.** Run `python scripts/brief_check.py den_haag` before writing code. T1 on the tram list. **Rotterdam is the template**
(`docs/build_briefs/rotterdam.md`, `pipeline/rotterdam/`): the BAG shop units as the second layer, with vacancy disclosed.

---

## For the owner, with the build

**Approved before this brief (owner, 2026-09-30; `docs/handoff_tram_kit_2026-09-30.md`, cdee504)**: the calls below as recommended, and the page-text template. The measurements here confirm the facts behind each call; where one differs, it says so. Builds wait for the owner's explicit go.

| | Proposed | Why |
|---|---|---|
| **`mode`** | **`tram`** | With RandstadRail E out, every drawn line is OSM `route=tram` (RandstadRail 3 and 4 included; EDGE flag kept) |
| **`coverage`** | **`narrowed`** ("Merged") | Rotterdam's shape: horeca permits for food, and BAG shop units that merge retail and personal services |
| **Scope** | **Gemeente Den Haag** (OSM 192736) | The permit layer is the city's; Rijswijk and Delft are discarded |
| **Lines drawn** | Trams 1, 2, 3, 4, 6, 9, 10, 11, 12, 15, 16, 17, 19 and 34 | 9S (4 stops, a short working) is not drawn separately |
| **Rings** | halved: **161 stop names, median gap 335 m** | The owner's spacing rule |
| **Call (approved): RandstadRail E** | **Out**, as a stub: 4 of 23 stops inside (17%) | RET's metro line; its Den Haag stops are served by trams 3 and 4 |
| **Call (approved): the 158 pending permits** | **Out** | In behandeling 125, Ingekomen 31, Advies aangevraagd 2: not granted |
| **Call (approved, call 26): tram 1** | **Drawn**: 19 of 37 inside (51%) | The owner, 2026-09-30 (over the 42% accepted for Minneapolis and Pittsburgh) |
| **Call (approved, call 27): the data date** | The page carries: "The permit data runs to 2025. The city last edited its permit layer on 23 May 2025, so premises that opened or closed since then may be missing or still shown." | The owner, 2026-09-30 |

---

## The one-line summary

**The city's own horeca permit layer (found 2026-09-30) plus the BAG's shop units: Rotterdam's two layers, on 14 tram lines.**

## Business leg

1. **Food: `Horeca_nieuw` layer 2 "Horecavergunningen"**, ArcGIS Online, owner GemeenteDenHaagIntern, displayed by the
   denhaag.nl permit map (web map `4db75a73…`, modified 2026-07-02):
   `https://services7.arcgis.com/b8OtZx5E96LVMxxJ/arcgis/rest/services/Horeca_nieuw/FeatureServer/2`. 2,701 permits, a point on
   every one; **2,543 granted or notified** (Actueel 1,581, Verleend 566, Melding 396); **about 2,352 food premises** after the
   exclusions (event sites, sports canteens, clubhouses, theatre foyers, coffeeshops, party centres, sex businesses, blank types).
   **Currency:** rows run to 2025 (`JAAR`), the layer was last edited 2025-05-23; the page gives the date. It drops a closed
   business by removal (no closed statuses remain).
   - **Fetch only these fields**: never `AANVRAGER`, `KVKNUMMER` or `RECHTSVORM` (34% are one-person firms; the city's own map
     hides all three). **The trade name is `OMSCHRIJVI`** ("restaurant Pex", "MELDING lunchroom …"): strip the type word and
     "MELDING", and repair the double-encoded UTF-8 ("cafÃ©" → "café"). `check_personal_exposure.py` still runs.
2. **Shops and services: the BAG's shop-class units in use** (PDOK), **6,560** (1.75× OSM shops; the 2026-09-27 screen), Rotterdam's
   query and its vacancy disclosure (CBS). Public Domain Mark.

## Rail — OSM

- **14 lines drawn** (Rail Haaglanden / HTM): 1 (19 of 37 inside), 2 (21/29), 3 (25/40), 4 (21/33), 6 (21/27), 9 (27/27), 10 (33/33),
  11 (17/17), 12 (19/19), 15 (14/18), 16 (22/23), 17 (20/33), 19 (10/18) and 34 (19/31). Lines 10 and 34 carry no OSM colour:
  choose them (palette); the others' OSM colours are hex (1 and 19 share `#c01115`, so one moves).
- **Out:** RandstadRail E (above); 9S not separately.

## Licences

- **The permit layer: READ 2026-09-30, SILENT and ambiguous; the owner proceeds on Amsterdam's precedent (2026-09-30).**
  Databankenwet art. 8(2): a public body's database is unprotected unless the right is expressly reserved, and nothing on the layer,
  its web map or app reserves it; against that, denhaag.nl's site terms name database rights, and the portal's own horeca
  placeholder is "in onderzoek". **Credit "Gemeente Den Haag"**; never call the layer current or complete; nothing implying the
  city's endorsement.
- **BAG:** Public Domain Mark (Rotterdam's row). **CBS vacancy:** CC BY 4.0 (Rotterdam's row). **OSM:** ODbL.

## Build-time calls

1. **Tram 1 at 51%**: drawn (approved, call 26).
2. **Colours for 10 and 34**, and one of 1/19 moved.

```brief-checks
[
  {
    "id": "den-haag-horeca-layer",
    "claim": "Den Haag's horeca permit layer answers (Horeca_nieuw layer 2, Horecavergunningen)",
    "kind": "http_contains",
    "url": "https://services7.arcgis.com/b8OtZx5E96LVMxxJ/arcgis/rest/services/Horeca_nieuw/FeatureServer/2?f=json",
    "present": [
      "Horecavergunningen",
      "OMSCHRIJVI"
    ]
  },
  {
    "id": "den-haag-osm-tram-refs",
    "claim": "OSM carries Den Haag's 14 drawn tram lines by ref (2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [
      52.0,
      4.2,
      52.12,
      4.42
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
        "6",
        "9",
        "10",
        "11",
        "12",
        "15",
        "16",
        "17",
        "19",
        "34"
      ]
    }
  },
  {
    "id": "den_haag-projected-crs",
    "claim": "The derived UTM zone is EPSG:32631",
    "kind": "utm_zone_from_longitude",
    "lon": 4.3,
    "expect": "EPSG:32631",
    "mode": "tram",
    "coverage": "narrowed",
    "scope": "city",
    "crs": "EPSG:32631",
    "vs_config": {
      "mode": "MAP_MODE",
      "coverage": "MAP_COVERAGE",
      "scope": "SCOPE",
      "crs": "CRS_PROJECTED"
    }
  }
]
```
