# Zurich — build brief

**Step 0 measured 2026-09-23.** Run `python scripts/brief_check.py zurich`
before writing any code.

⚠️ **One-bucket city.** It shares a single owner decision with **Stockholm**
and **Göteborg** — *does a food-density page belong in a project whose other
cities carry three buckets?* **Answer it once and three cities move.**

---

## The one-line summary

**The cleanest licence and the smallest register — and its trams are its
rapid transit, not an overlay.** 3,488 food premises, CC Zero, coordinates
already in metres, and **zero metro**, which is not the blocker it first
looked like.

---

## Business leg — `Gastwirtschaftsbetriebe`, MEASURED

| | |
|---|---|
| Rows | **3,488** |
| Source | **WFS** — `ogd.stadt-zuerich.ch/wfs/geoportal/Gastwirtschaftsbetriebe` |
| Licence | ✅ **CC Zero** (`cc-zero`) |
| Updated | **2026-09-23** — the day it was measured |
| Bucket | **Food service only** |

### 🚨 The advertised downloads are an Angular SPA — use the WFS

CKAN lists CSV, GeoJSON, SHP, GPKG and DXF resources under
`stadt-zuerich.ch/geodaten/download/Gastwirtschaftsbetriebe?format=…`.
**Every one of them returns `text/html`** — a 35 KB Angular shell with
`<app-root ng-version="10…">`. **That is Zagreb's SPA-shell shape**, and a
fetch script taking the CKAN resource URL gets a web page that parses as a
13-row CSV whose single column is `<!DOCTYPE html>`.

✅ **The WFS is a real OGC service and works with a plain client.** Its
capabilities advertise `resultType=hits` and
`outputFormat=application/vnd.geo+json`, both verified.

```
GetFeature?typeName=gastwirtschaftsbetriebe&resultType=hits      -> 3488
GetFeature?typeName=gastwirtschaftsbetriebe&outputFormat=application/vnd.geo+json
```

⚠️ **The layer name is lower-case `gastwirtschaftsbetriebe`**, read from
`FeatureTypeList`. The dataset's *title* is capitalised; the layer is not.

### The columns — 19, and three matter

| Column | Example | Role |
|---|---|---|
| **`betriebsname`** | `Gasthof Löwen/Meadra Cafe & Bar` | ✅ **trade name** |
| **`betriebsart`** | `Gastwirtschaft` | the activity type |
| **`betriebsstatus`** | **`Offen`** | 🚨 **a status filter — do not skip it** |
| `strasselang` + `hnr` + `plz` + `ort` | `Wehntalerstrasse 544, 8046 Zürich` | address |
| `ekoord` / `nkoord` | `2680564.045 / 1252613.69` | coordinates |
| `kreislang` / `quarlang` | `Kreis 11` / `Affoltern` | district / quarter |

✅ **`ekoord`/`nkoord` are CH1903+ / LV95 — EPSG:2056, already in METRES.**
So the ring geometry needs no reprojection to measure, only to display. That
is the project's invariant satisfied by the source.

⚠️ **`betriebsstatus` is a status field and 3,488 is the UNFILTERED count.**
The active share has not been measured. Every register this project has
touched carried closed or lapsed rows.

---

## 🚨 Rail — no metro, 42 trams, and that is NOT a blocker

Counted 2026-09-23 inside OSM relation **1682248** (Stadt Zürich):

| | |
|---|---|
| `route=subway` | **0** |
| **`route=tram`** | **42 relations, 18 refs, ALL named, ALL coloured** |
| `route=light_rail` | 4 relations, ref **S18** (Forchbahn) |

**Refs**: `2 3 4 5 6 7 8 9 10 11 12 13 14 15 17 20 50 51`

### Why the tram exclusion does not apply here

**`route_type 0` is DRAWN in at least seven built cities** — San Diego, San
Francisco, Los Angeles, Edmonton, Calgary, Miami, Dublin. **Every tram
EXCLUSION is a city that also has a metro**, where the trams are a
street-running overlay. Milan's own config calls its exclusion **"a costed
extension, not a discard"** and **"reversible"**; Barcelona's is a
*network-identity* test (`Trambaix`/`Trambesos`, *"neither a metro"*) used to
**select** the metro.

**Zurich has no metro for a tram to overlay. Its trams ARE the rapid-transit
system.**

✅ **And all 42 carry a `colour`**, which removes Milan's *other* objection
outright — it would have needed **17 invented colours** because `route_color`
was metro-only. **Zurich needs none.**

### ⚠️ The one open rail question — the Muni Metro spacing test

Milan's real test was **stop spacing**: *"stops sit one or two blocks apart:
San Francisco's Muni Metro shape, which needs
`docs/sub_transit_line_filters.md` rather than a line list."*

**That test has NOT been run for Zurich.** An attempt on 2026-09-23 **failed
its own control** — the San Francisco reference returned 0 route relations,
which is wrong, so the method was broken rather than the answer. **It is
unmeasured, and it is a COST rather than a disqualification**: the outcome is
either "draw the lines" or "draw them with a sub-line filter."

---

## Region

Zurich needs a **map region**; it is in Europe's macro-region per the standing
rule for all European cities.

---

## Still unknown

- ⚠️ **The active share** — `betriebsstatus` is unfiltered in the 3,488.
- ⚠️ **The stop-spacing test** — above. Needs a method whose control passes.
- ⚠️ **`betriebsart`'s distribution** — how many values, and whether any are
  non-storefront. Göteborg's equivalent turned out to be **26.5%** schools,
  wholesalers and head offices.
- ⚠️ **Whether `sid_wipo_gastwirtschaftsbetriebe_od1111`** — the second CKAN
  hit — is a different cut of the same register or a statistical aggregate.

```brief-checks
[
  {
    "id": "zurich-wfs-serves-the-register",
    "claim": "The WFS is the route that works. Its capabilities advertise the lower-case layer gastwirtschaftsbetriebe, resultType=hits and GeoJSON output - all verified 2026-09-23 at 3,488 features. The CKAN-advertised CSV/GeoJSON/SHP download URLs are an Angular SPA returning text/html, so a fetch script taking the CKAN resource URL gets a web page",
    "kind": "http_contains",
    "url": "https://www.ogd.stadt-zuerich.ch/wfs/geoportal/Gastwirtschaftsbetriebe?SERVICE=WFS&REQUEST=GetCapabilities&VERSION=1.1.0",
    "present": ["gastwirtschaftsbetriebe"]
  },
  {
    "id": "zurich-licence-is-cc-zero",
    "claim": "Gastwirtschaftsbetriebe declares Creative Commons CCZero on the city's own CKAN. The strongest licence position of the three one-bucket cities - Goteborg is also CC0 and Stockholm is SILENT",
    "kind": "http_contains",
    "url": "https://data.stadt-zuerich.ch/api/3/action/package_show?id=geo_gastwirtschaftsbetriebe",
    "present": ["cc-zero"]
  }
]
```
