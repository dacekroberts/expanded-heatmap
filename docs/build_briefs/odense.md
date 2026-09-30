# Odense — build brief

**Step 0 measured 2026-09-27 (the Danish second-city screen) and 2026-09-30
(this brief, on live OpenStreetMap).** Run `python scripts/brief_check.py odense`
before writing code. T1 on the tram list: trams-only maps approved by the owner
on 2026-09-29. **Aarhus is the template**: the same CVR register, the same
placement through OSM's DAR address points, the same Letbane shape. Read
`docs/build_briefs/aarhus.md` and `pipeline/aarhus/config.py` first.

---

## The one-line summary

**Aarhus's modules with kommune 461 and one Letbane line, plus a station OSM's
routes leave out.** Odense Letbane is a single street-running line (Keolis
operates it), with no metro and no S-tog.

| | Aarhus (built) | **Odense** |
|---|---|---|
| Kommune (CVR, unpadded) | 751 | **461** (OSM relation 2178124, `ref` 461) |
| Rail | Letbane L1 and L2, light rail | **Letbane, one line, OSM ref `L`, `route=tram`** |
| Stations in scope | 20 | **25 in service**: 24 on OSM's routes, plus SDU Syd/Hospital Nord (below) |
| Median station gap | 499 m | **441 m**, so halved rings (0.05 / 0.1 / 0.2 / 0.3 mi) |
| Projected CRS | EPSG:25832 | **EPSG:25832** (UTM 32, 10.39° E; DAR's national CRS) |
| Storefronts (screen) | 5,283 | **2,890**: retail 1,629 · food 649 · personal services 612 |
| Placed (screen) | 97.0% | **98.4%** on OSM's DAR points (the owner's call, 2026-09-27) |

**Region: `"Europe"`.** **Macro legend (proposed)**: `mode` tram (OSM maps
it as `route=tram`, and it runs on street track), `coverage` full.

---

## Business leg — CVR, as Aarhus

The screen (`data/_staging_scratch_2026-09-27/second_cities/denmark/biz.py`,
`biz_out.txt`) ran Copenhagen's filters on the shared CVR cache, generation
505, 2026-09-24:
- **Premises:** 27,583 with a current beliggenhedsadresse in Odense; 3,208
  in divisions 47, 56 and 96; 2,998 after the structural exclusions.
- **The 969900 catch-all:** 108 rows (3.6%) dropped, 84% of them
  personally owned. That leaves **2,890 storefronts**.
- **Personally owned: 44.9%.** Their names are suppressed (forms 10, 15 and
  30), so 55.1% of dots show a name.
- **Placement:** DAR Husnummer id on 98.6% of rows. The join through OSM's
  `osak:identifier` places 98.4%: the owner's call on 2026-09-27, keyless,
  under ODbL, as Aarhus.
- **Currency:** CVR is maintained daily, and a premises that closes leaves
  with a cessation date. Build on the shared CVR cache; never refresh it
  from a city branch.

## Rail — OSM, never Rejseplanen

- **Rejseplanen's GTFS is not used** (the owner, 2026-09-29, for Aarhus:
  its usage terms do not permit this project). **Rail from OSM**
  (`osm-rail`): two `route=tram` relations, 14315475 and 14315476
  (Hjallese St. ⇄ Tarup Center), 24 stop names, operator Keolis. **No
  `colour` tag**: choose one, then run `check_map_markup.py`.
- ⚠️ **SDU Syd/Hospital Nord is missing from OSM's route relations** but is
  a `railway=tram_stop` node. It **opened on 2023-08-25** with SDU's new
  health-sciences building (Danish Wikipedia's station article; Odense
  Letbane's news item), so it is in service.
  - **Add it** as a station by its node, named in config: a
    `STATION_ADD`, since step 1 takes stations from route membership.
    Precedent: Brno's H4 and P1 are handled by name; here the opposite
    way, one station added.
- **Hospital Syd** is also a tagged stop, but **it opens with the new
  hospital in 2027**. Leave it out, and record it as a watch item.
- **The operator's 26 stops** are these 24, SDU Syd/Hospital Nord, and
  Hospital Syd. So 25 are in service on 2026-09-30.
- **Frequency** is disclosed, not gated, on street track: every 7.5 minutes
  by day (the screen). Read it from Odense Letbane's own timetable if the
  page states it; never from Rejseplanen.
- **Every station is inside the kommune.**

## Licences

- **CVR:** read for Copenhagen, permitted. Its notices are in
  `docs/data_sources.md`, as on Aarhus's page.
- **OSM** (DAR address points and the tram): ODbL, with the basemap's
  credit. Say that the line and stops come from OSM.

## Build-time calls

1. **SDU Syd/Hospital Nord added by name**, as above.
2. **The line colour.**
3. **The ring share.** The screen did not measure it for Odense; measure it
   at build on the register's points.

```brief-checks
[
  {
    "id": "odense-letbane-osm",
    "claim": "OSM carries Odense Letbane as two route=tram relations with ref L (operator Keolis), 24 stop names on the routes (2026-09-30)",
    "kind": "osm_route_refs",
    "bbox": [55.33, 10.28, 55.46, 10.47],
    "routes": ["tram"],
    "expect_relations": {"tram": 2},
    "require_refs": {"tram": ["L"]}
  },
  {
    "id": "odense-is-utm-32",
    "claim": "Odense (10.39 E) is in UTM zone 32, as Aarhus: EPSG:25832 for DAR, WGS84 twin 32632",
    "kind": "utm_zone_from_longitude",
    "lon": 10.39,
    "expect": "EPSG:32632"
  }
]
```
