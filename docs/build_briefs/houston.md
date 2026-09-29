# Houston — build brief

**Step 0 measured 2026-09-28 (wave 2's US screen), 2026-09-29 (the
light-rail test) and 2026-09-29 (this brief).** Run
`python scripts/brief_check.py houston` before writing code.

---

## The one-line summary

**A big, clean state register that needs an address join, three rail lines
in a 1,645 km² city, and the most diffuse map this project would publish:
about 7% of storefronts within 0.6 mi of a station.** The join is proven on a
sample (81% at the first pass). The address file is public domain. The rail
is best drawn from OSM, because METRO's data agreement is the heaviest this
project has read.

| | |
|---|---|
| Rail | METRORail Red, Green, Purple: **40 stations** after name normalisation, **all inside the city**; 657 m median gap; Red every 6 min, Green and Purple every 12 by day |
| Register | Texas Comptroller, **Active Sales Tax Permit Holders** (`jrea-zgmq`, data.texas.gov, public domain) |
| Storefronts (outlet city HOUSTON, inside city limits) | retail **~21,870** (after dropping 6,491 non-store) · food **11,867** · personal **~2,575** (after dropping 414 parking lots) |
| Coordinates | **an address join** to the City's **Site Addresses** (1,550,454 points, public domain): **81.0%** of a 300-row sample at the first pass |
| In the 0.6 mi ring | **~7.0%** (the 243 placed sample rows; 4.1% at 0.3 mi). **Taoyuan's 11.7% is the current lowest** |
| Rings | **standard 0.1 / 0.2 / 0.3 / 0.6 mi** (657 m) |
| Projected CRS | **EPSG:32615** (UTM 15N, 95.37° W) |
| Region | `"North America"` |

---

## 🟠 THE OWNER'S FLAG — a 7% map

At about 7%, Houston's rings would hold roughly **2,500 of ~36,000
storefronts**. The project scopes by municipality, and Houston's city limits
run from Kingwood to Clear Lake. That is the precedent, and nothing here
changes it. But a map where 93% of the pins sit outside every ring reads
differently from any published so far. **Build as scoped (recommended; the
page states the share, as San Diego's does at 24.4%)**, or the owner may
reconsider Houston's place in Band A. The sample is 243 placed rows, so the
share is ±~3 points.

---

## ✅ Business leg — the Comptroller's permit file

`jrea-zgmq`: 888,178 outlets statewide, rows updated 2026-09-26. **79,097**
have `outlet_city = HOUSTON` and `outlet_inside_outside_city_limits_indicator
= Y` (17,196 are `N`). **The flag says inside *a* city's limits; the join's
point-in-boundary settles *which*.** Of the sampled matches, 233 of 243 were
`municipality HOUSTON` in the address file.

**Columns a step may read**: `outlet_*` and `taxpayer_organization_type`
only. ⚠️ **`outlet_naics_code` is a NUMBER column**: a string prefix test
(`like '454%'`, `starts_with`) is a 400 on the server, and a local `str[:3]`
works only after reading it as text. ⚠️ **Never `taxpayer_name` or `taxpayer_address`**: for a sole owner
they are a person's name and home or mailing address.

### Buckets by `outlet_naics_code` (NAICS 2017; the US standard: 44–45, 722, 812)

| | Rows | Build rule |
|---|---|---|
| Retail 44–45 | 28,358 | **drop 454 non-store retailers: 6,491** (454110 electronic shopping 4,704; 454390 direct selling 1,396). NAICS keeps the store / non-store split, so online sellers leave **by code**. Oslo could not do this; France and Houston can. Car dealers (441) stay, R4 |
| Food 722 | 11,867 | keep |
| Personal 812 | 2,989 | **drop 812930 parking lots (414)**, as every US city on NAICS does; keep laundries, dry cleaning, hair and nail |

The screen's "28,368 / 11,870 / 2,057" is superseded: its personal-services
figure was a different cut.

### ⚠️ Home-based sellers and privacy

- **`taxpayer_organization_type = IS` (individual sole owner): 9,314 bucket
  rows (21.6%).** The screen said 14,879 across all codes. **Suppress
  `outlet_name` for `IS` and show the address**, Oslo's and Copenhagen's
  sole-trader rule. `check_personal_exposure.py houston` is load-bearing.
- Sales-tax permits cover any taxable seller, including home-based ones
  with a storefront-less address. The address file's `addrtype` was
  **blank on 65%** of the sample matches (Commercial 61, Residential 12
  of 243), so it cannot screen homes on its own. **Build-time call**: drop
  `IS` rows whose matched point is `Residential` (4 of 47 `IS` rows in the
  sample), or keep them with the name suppressed. Recommend the drop: it is a
  measured home signal, not a guess.
- Suites and units: **32.9%** of bucket addresses carry `STE`, `SUITE`,
  `UNIT`, `#`…. Strip them before the join, as the sample did.

---

## ✅ Coordinates — the City's Site Addresses, public domain

`https://services.arcgis.com/NummVBqZSIJKUeVR/arcgis/rest/services/COH_SiteAddresses/FeatureServer/0`
(also `MapServer/33` on `mycity2.houstontx.gov`), 1,550,454 points with
`fulladdr`, `addrnum`, `roadname`, `unitid`, `municipality` and `addrtype`,
compiled from City, HCAD, CenterPoint and 911 sources. A bulk copy is linked
as `Export_SiteAddresses.zip` (ArcGIS item 82f34877…; not downloaded).
**Take the bulk file at build, not the query API**: the API pages at 2,000.

**Licence: READ 2026-09-29 — PERMITTED.** The City's GIS open-data Hub, where
the item is published: *"COHGIS data is in the public domain and may be
copied without permission"*. The sibling items for the same data say
*"…citation of the source is appreciated."* Nothing must be displayed or
done; credit "City of Houston Planning & Development" as a courtesy. **One
low tension, recorded**: two sibling items put "© HITS-GIS. All rights
reserved" in their credits field beside the public-domain grant. Settle with
gis@houstontx.gov only if the owner wants it settled. **Fallback**: TxGIO's
**StratMap Address Points 2026** (acquired 2026-03-18, **CC0 1.0**), Harris
County `stratmap-2026-address-points_48201_ap.zip`, **118.6 MB**, not read
beyond its declared licence.

### The sample join (300 random bucket rows, 2026-09-29)

Exact `fulladdr` after stripping the unit tail: **243 matched (81.0%)**. The
misses are the kinds `address-join` says to read, not anticipate:
- letter suffixes on the number (`3901C BELLAIRE BLVD`, `1417A WESTHEIMER RD`);
- highway naming (`HIGHWAY 6 N`, `FM 1960 RD W`, `N SAM HOUSTON PKWY W`);
- airport terminals (`3950 S TERMINAL RD TERM E GATE E24`).

**Pick a control set before normalising** and re-run it after every parser
change (the skill's rule). The residue can go to
`pipeline/census_geocoder.py`, the US precedent (Los Angeles, New York,
D.C.), with its bounds check.

---

## Rail — draw it from OSM; METRO's data agreement is heavy

### What the feed says (METRO's GTFS, `August2026IVOMS_20260828`, 2026-08-30 → 2027-01-23)

Three `route_type 0` routes: 700 **METRORAIL RED LINE** `EF0000`, 800
**GREEN** `3E7E00`, 900 **PURPLE** `40007E`. **80 platforms, no
`parent_station`**, and names that need work:
- every platform name ends in a direction (`NB`, `SB`, `EB`, `WB`, `Eb`);
- spellings differ by direction (`Eado / Stadium Stn EB` / `Eado Stadium Stn
  WB`; `Coffee Plant /  2Nd Ward` with a double space);
- **three downtown couplets**, one station on two parallel streets:
  Central Station Capitol / Rusk (99 m), Theater District Capitol / Rusk
  (141 m), Convention District Capitol / Rusk (137 m).

80 platforms → **44 names** after stripping the direction and "Stn" →
**40 stations** with the couplets and Eado aliased. Per line: Red 25, Green 9,
Purple 13. **All 40 are inside the city.** Median gap 657 m (the test's OSM
read: 42 stops, 651 m). The couplet aliases are explicit, never a rule
(Oslo's).

### METRO's Data Use Agreement — READ 2026-09-29: usable, but the heaviest yet

The static feed is governed by the "Transit Data Files / DATA USE AGREEMENT"
(May 2025) on `ridemetro.org/about/news-media/digital-assets`. Using the data
is allowed, but it demands:
- **a verbatim credit** near the data ("Data is provided by permission of
  The Metropolitan Transit Authority of Harris County, Texas."), with a
  different wording on the API portal;
- **a modification notice**, and the agreement "made available" to recipients;
- **an asterisk and a trademark legend** wherever "METRO" appears; **only
  "METRO" is a licensed mark**, and names identifying METRO's services are
  claimed as marks (the third-party trademark agreement licenses news use
  only);
- **an indemnity with no limit** (§5(A)), citing "indemnification
  requirements" that could not be found;
- **compliance within 24 hours** of a written demand to limit use;
- **no deep links** into ridemetro.org (website terms §4).

**Recommended: draw the rail from OSM** (the `osm-rail` skill; Copenhagen's
and Aarhus's precedent, and Buffalo's recommendation). OSM's six relations
(1741729, 12356338 Red; 2728566, 12356337 Green; 2728567, 12356336 Purple)
carry the geometry, the stops and the public names under ODbL, and the
agreement never binds the map. OSM's colours are the words `red`, `green` and
`purple`. Choose hexes through `pipeline/linecolour.py`, and don't copy
METRO's. **Line labels: "Red Line", "Green Line", "Purple Line"**, the
lowest-risk option the licence read named. The legend may say "METRORail"
once, as the system's public name. **The label wording is the owner's call**,
and it is Buffalo's question in another form.

---

## Build-time calls

1. ✅ **Build as scoped at ~7% in-ring, with the share stated on the page
   (owner, 2026-09-29).**
2. ✅ **Rail from OSM (owner, 2026-09-29)**: METRO's feed and its Data Use
   Agreement stay out of the build. ✅ **Line labels "Red Line", "Green Line",
   "Purple Line" (owner, 2026-09-29).**
3. `IS` rows at a `Residential` point: drop (recommended) or keep with the
   name suppressed.
4. The address file: the City's bulk export (recommended; public domain) or
   TxGIO's CC0 points.

**Flag for the cleanup role (held macro-map work)**: Houston takes the
light-rail network colour.

## Still unknown

- The full join rate after normalisation, and the Census geocoder's share of
  the residue.
- The in-ring share on the whole register (the sample is 243 rows).

```brief-checks
[
  {
    "id": "comptroller-houston-inside-limits",
    "claim": "The Comptroller's active permit file lists about 79,097 outlets with outlet city HOUSTON flagged inside city limits (2026-09-29)",
    "kind": "socrata_count",
    "domain": "data.texas.gov",
    "view": "jrea-zgmq",
    "where": "upper(outlet_city)='HOUSTON' AND outlet_inside_outside_city_limits_indicator='Y'",
    "expect": 79097,
    "tolerance": 4000
  },
  {
    "id": "comptroller-houston-nonstore",
    "claim": "About 6,491 of them are NAICS 454 non-store retailers - online and direct sellers that leave by code",
    "kind": "socrata_count",
    "domain": "data.texas.gov",
    "view": "jrea-zgmq",
    "where": "upper(outlet_city)='HOUSTON' AND outlet_inside_outside_city_limits_indicator='Y' AND outlet_naics_code >= 454000 AND outlet_naics_code < 455000",
    "expect": 6491,
    "tolerance": 800
  },
  {
    "id": "coh-site-addresses-serves",
    "claim": "The City's Site Addresses layer (public domain via the COHGIS Hub) answers keyless with its point count, about 1.55 million",
    "kind": "http_contains",
    "url": "https://services.arcgis.com/NummVBqZSIJKUeVR/arcgis/rest/services/COH_SiteAddresses/FeatureServer/0/query?where=1%3D1&returnCountOnly=true&f=json",
    "present": ["count"]
  },
  {
    "id": "metrorail-osm-relations",
    "claim": "OSM carries METRORail as six light_rail relations in three refs, Red, Green and Purple - the recommended rail source",
    "kind": "osm_route_refs",
    "bbox": [29.6, -95.5, 29.9, -95.25],
    "routes": ["light_rail"],
    "expect_refs": {"light_rail": 3},
    "require_refs": {"light_rail": ["Red", "Green", "Purple"]}
  },
  {
    "id": "houston-is-utm-15",
    "claim": "Houston (95.37 W) is in UTM zone 15N",
    "kind": "utm_zone_from_longitude",
    "lon": -95.37,
    "expect": "EPSG:32615"
  }
]
```
