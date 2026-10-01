# Seattle — build brief

**Step 0 NOT complete. This brief covers the City of Seattle's own registry
only.** Seattle was screened on 2026-09-21 and deferred by the owner the same
day, then scoped as the project's first **multi-municipality** city: full line
coverage of Link's 1 and 2 Lines, which means ten to twelve jurisdictions, each
needing its own Step 0. The scope, the jurisdiction list and the architecture
gaps are in `PLAN.md` (the Seattle item) and in `docs/decisions/2026-09-20.md`,
"Seattle: deferred, then scoped as the first multi-municipality city". They are
not repeated here.

Run `python scripts/brief_check.py seattle` before relying on anything below.
**Do not re-probe the Seattle registry from scratch.** The findings below were
kept so that coming back to Seattle costs nothing. They were moved here from
`docs/city_shortlist.md` on 2026-09-27, and three of them were re-read live
that day (marked MEASURED 2026-09-27).

---

## The one-line summary

**The best-equipped registry the US screen found, and the one earlier screens
missed.** It is an official nightly export, active licences only by
construction, with real NAICS (so no new taxonomy module), a trade name and a
point on every row (so no geocoding step). It is on ArcGIS rather than
Socrata, which is why a Socrata-only screen returned "no matching datasets".

---

## Business leg — "Seattle Business License" (ArcGIS)

- **Layer:** `https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Seattle_Business_License/FeatureServer/0`,
  named **"Business Locations (Active)"**.
- **Item owner:** `SeattleData`, in ArcGIS org `ZOyb2t4B0UYuYNYH`. The item's
  access information reads "City of Seattle, Enterprise Data".
- **Publisher:** the item describes itself as "a nightly export of the business
  license database maintained by Seattle's Department of Finance &
  Administrative Services", containing "only … ACTIVE business licensees". The
  layer's own description names the source system as SLIM, the Seattle
  Licensing Information System.
- **Rows:** 54,604 on 2026-09-21. **MEASURED 2026-09-27: 54,635**, last edited
  2026-09-25.
- **Geometry:** points. **MEASURED 2026-09-27:** served in EPSG:2926
  (Washington North, US feet). The build still projects to the city's own UTM
  zone for any distance work, per the invariant.
- **Taxonomy:** `naics` (already built), from `BUSLIC_NAICS_CODE` and
  `BUSLIC_NAICS_DESC`. SIC is also carried (`BUSLIC_SIC_CODE`,
  `BUSLIC_SIC_DESC`).
- **Name and address:** `BUSLIC_TRADE_NAME`, `BUSLIC_LEGAL_NAME` and
  `BUSLIC_LOCATION_ADRS_TEXT`.

### Privacy — columns that must never be published

- `BUSLIC_CONTACT_NAME` holds a person's name.
- `BUSLIC_PHONE_NUM` holds a phone number. `drop_contact_details()` in
  `pipeline/map_common.py` already drops phone columns.
- **MEASURED 2026-09-27, not in the 2026-09-21 findings:** the layer also
  carries `BUSLIC_MAIL_ADRS_TEXT`, a mailing address, which could be a home
  address. Treat it the way `BUSLIC_CONTACT_NAME` is treated.

### Licence — read, and NOT a grant

The item's `licenseInfo` is an as-is accuracy disclaimer ("The City of Seattle
makes no representation or warranty as to its accuracy …"). It grants nothing.
**The licence position is therefore unresolved.** It needs a `read-licence`
pass (the `licence-read` agent) before any build, looking for the city's
open-data terms by reference, as in Philadelphia's case.

---

## Still to do before building (from the 2026-09-21 screen)

1. **The category distribution:** what share of active rows falls in each
   bucket, and which catch-all NAICS codes need the Los Angeles
   personal-exposure treatment.
2. **The in-city check.** Does every row fall inside the City of Seattle?
   Rows elsewhere would matter more here than in most cities, because the
   neighbouring jurisdictions are a planned part of the build.
3. **`BUSLIC_LOCATION_TYPE`, headquarters vs branch. MEASURED 2026-09-27:**
   it has exactly two values, `BRANCH` and `HEADER QUARTER`. Whether a
   headquarters row is a storefront needs a verdict. Taichung's head-office
   rule is the nearest precedent.
4. **The licence** (above).

Then the multi-municipality work in `PLAN.md`, which is most of the cost.

---

## Machine checks

```brief-checks
[
  {
    "id": "seattle-active-layer",
    "claim": "The Business Locations (Active) layer is a point layer of about 54,604 active licences (2026-09-21), carrying NAICS, SIC, trade and legal names, the location address and type, and the two contact columns that must never be published - and it is still refreshed (nightly, per its item)",
    "kind": "arcgis_layer",
    "url": "https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Seattle_Business_License/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 54604,
    "tolerance": 1000,
    "present": ["BUSLIC_NAICS_CODE", "BUSLIC_NAICS_DESC", "BUSLIC_SIC_CODE", "BUSLIC_SIC_DESC", "BUSLIC_TRADE_NAME", "BUSLIC_LEGAL_NAME", "BUSLIC_LOCATION_ADRS_TEXT", "BUSLIC_LOCATION_TYPE", "BUSLIC_CONTACT_NAME", "BUSLIC_PHONE_NUM", "BUSLIC_MAIL_ADRS_TEXT"],
    "max_age_days": 14
  },
  {
    "id": "seattle-layer-name",
    "claim": "Layer 0 is the ACTIVE-locations layer, not a history",
    "kind": "http_contains",
    "url": "https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Seattle_Business_License/FeatureServer/0?f=json",
    "present": ["Business Locations (Active)"]
  },
  {
    "id": "seattle-item-owner-and-licence",
    "claim": "The item is owned by SeattleData, describes itself as a nightly export of Finance & Administrative Services' licence database holding only active licensees, and its licenseInfo is an as-is accuracy disclaimer - not a grant",
    "kind": "http_contains",
    "url": "https://www.arcgis.com/sharing/rest/content/items/2b2fcf14f20c4e66a3c2c6ed538054ef?f=json",
    "present": ["\"owner\":\"SeattleData\"", "nightly export", "Finance & Administrative Services", "ACTIVE business licensees", "makes no representation or warranty"],
    "absent": ["creativecommons", "public domain", "open data commons"]
  },
  {
    "id": "seattle-location-type-values",
    "claim": "BUSLIC_LOCATION_TYPE distinguishes HEADER QUARTER from BRANCH - the headquarters-vs-branch verdict is still owed",
    "kind": "http_contains",
    "url": "https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Seattle_Business_License/FeatureServer/0/query?where=1%3D1&returnDistinctValues=true&outFields=BUSLIC_LOCATION_TYPE&returnGeometry=false&f=json",
    "present": ["HEADER QUARTER", "BRANCH"]
  }
]
```

## Still unknown

- Everything in "Still to do" above.
- ~~Every other jurisdiction on Link's 1 and 2 Lines.~~ Screened 2026-10-01:
  see the next section.
- The rail leg: the Link GTFS has not been read for this brief. The OSM
  station set below stands in until it is.

---

## The regional screen - every jurisdiction on the 1 and 2 Lines (2026-10-01)

The owner's scope (2026-10-01): **a regional build with multiple city
registers**, held as before. This section is what that build has to pull. It
comes from staging, using one Overpass query and four metadata-only screens.
Nothing was downloaded in bulk and no request was sent. The scratch output is
in that session's scratchpad.

### Stations: 37, in 11 cities

From OSM's four Link route relations (1 Line 3494092 and 5517060; 2 Line
17499739 and 17499740), each stop placed in its OSM admin_level 8 city:

| City | Stations |
|---|---|
| Seattle | 17: Northgate to Rainier Beach on the 1 Line, plus Judkins Park on the 2 Line |
| Bellevue | 6: South Bellevue, East Main, Bellevue Downtown, Wilburton, Spring District, BelRed |
| Redmond | 4: Overlake Village, Redmond Technology, Marymoor Village, Downtown Redmond |
| Shoreline | 2: Shoreline South/148th, Shoreline North/185th |
| SeaTac | 2: SeaTac/Airport, Angle Lake |
| Kent | 2: Kent Des Moines, Star Lake |
| Lynnwood | 1: Lynnwood City Center |
| Mountlake Terrace | 1 |
| Tukwila | 1: Tukwila International Boulevard |
| Federal Way | 1: Federal Way Downtown |
| Mercer Island | 1 |

The cross-lake 2 Line (Mercer Island, Judkins Park) opened on 2026-03-28,
per Sound Transit's news release.

**The 0.6 mi rings reach beyond the station cities.** Measured in UTM 10N
against King County's city polygons:
- **Des Moines:** 42% of Kent Des Moines' ring and 3% of Star Lake's. It has
  no station.
- **Unincorporated King County:** about 33% of Marymoor Village's ring, 15%
  of Downtown Redmond's and about 16% of Star Lake's.
- **Bellevue:** 41% of Overlake Village's ring, which is in Redmond.
- **SeaTac:** 53% of Tukwila International Boulevard's ring.
- **Federal Way:** 29% of Star Lake's ring.
- **Slivers:** Beaux Arts (5% of South Bellevue's ring) and Lake Forest Park
  (at the edge of Shoreline North's ring).
- **No ring reaches** Burien, Renton, Normandy Park, Auburn, Kirkland, Clyde
  Hill, Medina, Edmonds or Brier.

### What each jurisdiction publishes

| Jurisdiction | Licensed by | Retail | Food | Personal services |
|---|---|---|---|---|
| **Seattle** | the city (SLIM) | **own register** (above) | own register + King County food | own register |
| **Bellevue** | the city (applied for through FileLocal) | **own register**: "Business Licenses (All)", 82,155 rows, NAICS, lat/long, daily; 1,770 in-city active rows in the buckets | own + King County food | own |
| **Redmond** | state BLS since 2021 | own layer **frozen about 2020** (1,902 rows; no dates) | King County food | frozen layer only |
| **Federal Way** | state BLS | shopping-centre extract, 2024 snapshot (1,048 points, no classification) | King County food | the same extract |
| **Shoreline** | the city (own licence) | lookup tool only (`business.shorelinewa.gov`, capped at 100) | King County food | none |
| **Kent, Des Moines** | the cities, through FileLocal | none published | King County food | none |
| **Tukwila, SeaTac, Mercer Island** | state BLS | none | King County food | none |
| **Lynnwood, Mountlake Terrace** | state BLS | none | **no current source** (below) | none |
| **Unincorporated King County** | the county | none | King County food | none |

### The regional sources

- **Food, King County: Public Health – Seattle & King County, "Food
  Establishment Inspection Data"** (`data.kingcounty.gov`, Socrata
  `r878-4sxa`).
  - 12,296 businesses across 108,905 rows, covering 2021-01-04 to
    2026-09-29.
  - **No coordinates**, but `parcel_number` is filled for 12,131. They join
    to King County's public parcels (`PIN`, `LAT`/`LON`) or to its address
    points (674,254, carrying `CTYNAME`).
  - It behaves as a current-permit snapshot: 12,119 businesses were last
    inspected in 2025 or 2026.
  - It also covers grocery, meat/fish and bakery retail.
  - The `city` field is the **postal** city, so scope by point-in-boundary.
  - **Licence: conflicting.** The Socrata field says Public Domain. The
    ArcGIS copy (`EPL_BusinessPoint`, which carries `Business_Status` and
    points) says no redistribution without written authorization.
    `licence-read` decides.
- **Food, Snohomish County (Lynnwood, Mountlake Terrace).**
  - The only layer is "Food Service Establishments (2025)": 3,699 points,
    598 of them in Lynnwood and 92 in Mountlake Terrace. It has **no date,
    status or licence field**, so it fails the currency rule.
  - The county health department's portal is per-search only.
- **Statewide: WA Liquor and Cannabis Board on- and off-premise lists**
  (XLSX, dated 2026-09-29).
  - The only source spanning both counties: food (on-premise) and
    grocery/convenience (off-premise).
  - **Not downloaded**: that needs the owner's OK.
  - Its terms say records "may not be used for commercial purposes".
- **No bulk source exists** for:
  - **the state's business licences** (DOR BLS: lookup only; a bulk list
    needs a Declaration of Non-Commercial Purpose);
  - **personal-services licences** (DOL: counts only).
- **Use-class fallbacks** (assessor present use per parcel; Snohomish
  address points' `USECODE`):
  - Parcel-level, with no names and no personal-services class in King
    County.
  - A cross-check only.

### What the build has to pull

1. **Seattle's register**: its licence read is still owed.
2. **Bellevue's register**:
   - It carries a "commercial use … prohibited" disclaimer, so it needs a
     licence read.
   - Licences never expire, so closed businesses linger (2,938 in-city
     active rows were issued before 2015).
   - 1,174 sole proprietorships, and 4,185 rows in residential zones.
     `check_personal_exposure.py` is essential.
3. **King County food inspections**, joined to the parcels: food for every
   King County city and the unincorporated rings. Licence read first.
4. **Lynnwood and Mountlake Terrace food**: the owner's call. One of:
   - the LCB list (a download and a terms read);
   - the 2025 Snohomish layer with its date on the page (it fails part 1 of
     the currency rule);
   - leave both cities' stations hollow, Tokyo's precedent.
5. **Retail and personal services outside Seattle and Bellevue**: none
   published.
   - The routes are public-records requests: Shoreline, Kent and Des Moines
     to the city; the BLS cities through DOR, which needs a non-commercial
     declaration.
   - That is outreach, the owner's last resort.
   - Without it, those cities are food-only beside two full cities, and the
     page states each city's coverage (the Tokyo and Band B precedents).
6. **Rings that cross a city line** take the neighbour's data or are stated
   as unmapped: Des Moines and unincorporated King County have King County
   food only.
