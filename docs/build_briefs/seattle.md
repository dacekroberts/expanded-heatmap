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
  2026-09-25. **MEASURED 2026-10-02: 54,689**, last edited 2026-10-02, every
  row `BUSLIC_STATUS_TYPE = ACTIVE` and every row with a point.
- **Licence year. MEASURED 2026-10-02, not in the earlier findings:** the layer
  carries `BUSLIC_YEAR_NUM` and `BUSLIC_EXPIRATION_DATE` (always 31 December
  of that year). "Active" includes licences that lapsed without renewal:
  44,096 rows are on 2026 licences, 5,379 on 2025, 3,023 on 2024 and 2,185
  on 2023. `BUSLIC_OPENDATE` is filled on every row. See "Still to do",
  item 5.
- **Seattle-only build.** The owner's separate Seattle-only build is its own
  repository, `C:\Users\dacek\Documents\Portfolio\link-station-commercial`
  (GitHub `dacekroberts/link-station-commercial`): the sixteen 1 Line
  stations inside Seattle, from the Socrata licence table `wnbq-64tb` with
  this layer as its geometry donor. It is not a branch or worktree of this
  project, and nothing here touches it.
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

1. ~~**The category distribution.**~~ **DONE 2026-10-02** (all 54,689 rows,
   `pipeline/taxonomies/naics.py` as it stands, carve-outs included):
   - **Retail 4,850, Food service 3,084, Personal services 2,114**: 10,048
     rows, 18% of the layer. The other 44,641 are outside the buckets.
   - All codes are six digits; none is blank.
   - **Already carved out nationally:** 81299 (2,165), 81293 parking (756),
     72233 mobile food (352), 72232 caterers (190), 72231 (90), 8122 (18),
     445132 (14), 454 (3).
   - **Catch-alls to hand-sample at build:** 459999 all other miscellaneous
     retailers (**1,063**, the largest Retail code; the earlier Seattle
     sample kept it at about 70% walk-in) and 812199 other personal care
     (381).
   - **The Los Angeles treatment.** The trade name is never blank, so no
     pin falls back silently. But it equals the legal name on 2,044 bucket
     rows, and on **about 470** the legal name carries no company marker
     (LLC, INC and the like) and may be a person's own name; **about 157** of
     those have APT, UNIT or # in the address. The largest are 812112
     beauty salons (87), 459999 (70), 458110 clothing (39) and 812199 (28).
     A heuristic, not a verdict: `check_personal_exposure.py` decides it.
2. ~~**The in-city check.**~~ **DONE 2026-10-02**, every point against King
   County's city polygons (`CITY_KC_AREA_446`):
   - **53,677 rows (98.1%) are inside Seattle; 1,012 are not**, although
     every address reads "SEATTLE": 836 in unincorporated King County
     (White Center, Skyway and the like), 141 in Burien, 15 in Tukwila, 11
     in Shoreline, 5 in Renton, 2 in SeaTac, 2 in Lake Forest Park.
   - **Bucket rows: 9,880 inside, 168 outside** (151 unincorporated, 12
     Burien, 3 Tukwila, 1 Renton, 1 Shoreline).
   - So scope by point-in-boundary, and do not use the outside rows for the
     neighbours: a Seattle licence held by a business outside the city is a
     partial, accidental cover of that place.
3. ~~**`BUSLIC_LOCATION_TYPE`, headquarters vs branch.**~~ **MEASURED
   2026-10-02; the verdict is the owner's** (below):
   - **`HEADER QUARTER` means a business's primary location, not a head
     office.** 48,992 businesses (`BUSLIC_BUSINESS_ID`) have exactly one;
     136 have only branches.
   - Bucket rows: **9,142 HEADER QUARTER, 906 BRANCH.** Dropping
     headquarters would drop 91% of the storefronts.
   - Only **378** bucket headquarters rows belong to a business that also
     has a branch row (Retail 166, Food 162, Personal 50): the only rows that
     could be a chain's office.
   - **Taichung's head-office rule does not transfer.** It drops a company
     head office on the third floor or higher or in a room, unless the
     building holds 20+ storefront rows (DECISIONS archive
     `docs/decisions/2026-09-20.md`, "The head-office rule (owner, as
     measured on Taipei)"). Seattle's addresses carry floors and rooms so
     rarely that the same test flags **9** headquarters rows and 2 branch
     rows.
4. ~~**The licence.**~~ **DONE 2026-10-01:** permitted with conditions
   ("What the build has to pull", item 1).
5. **NEW 2026-10-02: lapsed licences in the active layer.** Bucket rows by
   licence year: 2026 8,003 (and 1 on 2027); 2025 1,058; 2024 571; 2023 415.
   **2,044 bucket rows (20%) hold a licence that expired on 31 December 2025
   or earlier.**
   - **Control: King County food inspections.** Seattle food-service rows
     matched to a business inspected in 2025 or 2026, by trade name or by
     street address:

     | Licence year | Rows | Name match | Address match | Either |
     |---|---|---|---|---|
     | 2026 | 2,550 | 65% | 85% | 90% |
     | 2025 | 292 | 48% | 74% | 78% |
     | 2024 | 147 | 35% | 73% | 75% |
     | 2023 | 95 | 38% | 73% | 79% |

   - So lapsed rows are staler, but not dead: about half to three-quarters of
     the current-year rate. A licence-year filter goes to the owner (below).

Then the multi-municipality work in `PLAN.md`, which is most of the cost.

---

## Machine checks

```brief-checks
[
  {
    "id": "seattle-active-layer",
    "claim": "The Business Locations (Active) layer is a point layer of about 54,689 active licences (2026-10-02), carrying NAICS, SIC, trade and legal names, the location address and type, the business id, the licence year and expiry, and the three contact columns that must never be published - and it is still refreshed (nightly, per its item)",
    "kind": "arcgis_layer",
    "url": "https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Seattle_Business_License/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 54689,
    "tolerance": 1000,
    "present": ["BUSLIC_NAICS_CODE", "BUSLIC_NAICS_DESC", "BUSLIC_SIC_CODE", "BUSLIC_SIC_DESC", "BUSLIC_TRADE_NAME", "BUSLIC_LEGAL_NAME", "BUSLIC_LOCATION_ADRS_TEXT", "BUSLIC_LOCATION_TYPE", "BUSLIC_CONTACT_NAME", "BUSLIC_PHONE_NUM", "BUSLIC_MAIL_ADRS_TEXT", "BUSLIC_BUSINESS_ID", "BUSLIC_YEAR_NUM", "BUSLIC_EXPIRATION_DATE", "BUSLIC_STATUS_TYPE"],
    "max_age_days": 14
  },
  {
    "id": "seattle-lapsed-licence-years",
    "claim": "The active layer still holds licences whose year lapsed (2023 and 2025 among the distinct licence years) - the licence-year filter is the owner's call",
    "kind": "http_contains",
    "url": "https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Seattle_Business_License/FeatureServer/0/query?where=1%3D1&returnDistinctValues=true&outFields=BUSLIC_YEAR_NUM&returnGeometry=false&f=json",
    "present": ["\"BUSLIC_YEAR_NUM\":2023", "\"BUSLIC_YEAR_NUM\":2025", "\"BUSLIC_YEAR_NUM\":2026"]
  },
  {
    "id": "kc-city-polygons",
    "claim": "King County's city polygons (CITY_KC_AREA_446), used for the in-city check and the ring shares, are a polygon layer carrying CITYNAME and JURIS",
    "kind": "arcgis_layer",
    "url": "https://services.arcgis.com/Ej0PsM5Aw677QF1W/arcgis/rest/services/CITY_KC_AREA_446/FeatureServer/0",
    "expect_geometry": "esriGeometryPolygon",
    "present": ["CITYNAME", "JURIS"]
  },
  {
    "id": "bellevue-licences-layer",
    "claim": "Bellevue's Business Licenses (All) is about 82,155 rows with NAICS, a trade name, issue and cancel dates, entity type, neighbourhood and planning zone, lat/long, and a SysChangeDate that is a load stamp - still refreshed",
    "kind": "arcgis_layer",
    "url": "https://services1.arcgis.com/EYzEZbDhXZjURPbP/arcgis/rest/services/Business_Licenses_(All)/FeatureServer/3",
    "expect_rows": 82155,
    "tolerance": 2000,
    "present": ["Naic", "Dba", "IssueDate", "CancelDate", "FirstActivityDate", "LegalEntityType", "NeighborhoodArea", "PlanningZone", "Latitude", "Longitude", "SysChangeDate"],
    "max_age_days": 14
  },
  {
    "id": "kc-food-inspections",
    "claim": "Public Health - Seattle & King County's food inspection data (r878-4sxa) has about 108,905 inspection rows (2026-10-01) and keeps growing",
    "kind": "socrata_count",
    "domain": "data.kingcounty.gov",
    "view": "r878-4sxa",
    "expect": 108905,
    "tolerance": 3000
  },
  {
    "id": "snohomish-food-layer",
    "claim": "Snohomish County's Food Service Establishments layer is a static point layer of 3,699 permits (3,131 facilities), with postal city, jurisdiction, permit type, facility and record ids, and no date or status field",
    "kind": "arcgis_layer",
    "url": "https://services6.arcgis.com/z6WYi9VRHfgwgtyW/arcgis/rest/services/Food_Service_Establishments/FeatureServer/0",
    "expect_geometry": "esriGeometryPoint",
    "expect_rows": 3699,
    "tolerance": 0,
    "present": ["USER_City", "User_Fld", "USER_Program_Element", "USER_Facility_ID", "USER_Record_ID", "Icon"]
  },
  {
    "id": "snohomish-food-service-static-2025",
    "claim": "The service calls itself 'Establishments serving food (2025)' and declares its data static",
    "kind": "http_contains",
    "url": "https://services6.arcgis.com/z6WYi9VRHfgwgtyW/arcgis/rest/services/Food_Service_Establishments/FeatureServer?f=json",
    "present": ["Establishments serving food (2025)", "\"hasStaticData\":true"]
  },
  {
    "id": "snohomish-food-lynnwood-jurisdiction",
    "claim": "398 of the layer's points are in the City of Lynnwood by its jurisdiction field (598 by postal city)",
    "kind": "http_contains",
    "url": "https://services6.arcgis.com/z6WYi9VRHfgwgtyW/arcgis/rest/services/Food_Service_Establishments/FeatureServer/0/query?where=User_Fld%3D%27LYNNWOOD%27&returnCountOnly=true&f=json",
    "present": ["\"count\":398"]
  },
  {
    "id": "snohomish-food-mlt-jurisdiction",
    "claim": "74 of the layer's points are in the City of Mountlake Terrace by its jurisdiction field (92 by postal city)",
    "kind": "http_contains",
    "url": "https://services6.arcgis.com/z6WYi9VRHfgwgtyW/arcgis/rest/services/Food_Service_Establishments/FeatureServer/0/query?where=User_Fld%3D%27MOUNTLAKE%20TERRACE%27&returnCountOnly=true&f=json",
    "present": ["\"count\":74"]
  },
  {
    "id": "lcb-on-premise-list",
    "claim": "The Liquor Board's on-premise list dated 2026-09-29 is published as an XLSX of about 1.9 MB",
    "kind": "http_ok",
    "url": "https://lcb.wa.gov/sites/default/files/2026-09/On%20Premise09292026.xlsx",
    "min_bytes": 1000000
  },
  {
    "id": "st-gtfs-window",
    "claim": "Sound Transit's rail GTFS (soundtransit.org, served from gtfs.sound.obaweb.org) is current: feed_info 2026-09-01 to 2027-03-26",
    "kind": "gtfs_feed_window",
    "url": "https://www.soundtransit.org/GTFS-rail/40_gtfs.zip",
    "expect": "current"
  },
  {
    "id": "st-gtfs-route-types",
    "claim": "The feed holds three light-rail routes (1 Line, 2 Line, T Line) as route_type 0, two Sounder lines as 2 and two shuttle-bus routes as 3",
    "kind": "gtfs_route_type_counts",
    "url": "https://www.soundtransit.org/GTFS-rail/40_gtfs.zip",
    "expect": {"0": 3, "2": 2, "3": 2}
  },
  {
    "id": "st-gtfs-link-stations",
    "claim": "The 1 Line (Lynnwood - Federal Way) and 2 Line (Lynnwood - Downtown Redmond) serve 39 stations between them, collapsed on parent_station, spaced like stations",
    "kind": "gtfs_stations",
    "url": "https://www.soundtransit.org/GTFS-rail/40_gtfs.zip",
    "route_types": [0],
    "route_name_regex": "^Lynnwood - ",
    "expect_parent_station_populated": true,
    "expect_stations": 39,
    "crs": "EPSG:32610",
    "station_spacing_median_m_min": 300
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
- ~~The rail leg: the Link GTFS has not been read for this brief.~~ Read
  2026-10-02: **39 stations**, not 37 (see "Stations" below). Sound
  Transit's own feed terms (the Open Transit Data terms of use) have not
  been read: a `licence-read` is owed before the build.
- **Licence verdicts (`licence-read`, 2026-10-02):**
  - **Liquor Board on- and off-premise lists: PERMITTED WITH CONDITIONS.**
    - No licence and no terms of use exist. The one rule is the lists
      page's note: "Per RCW 42.56.070(8), records received through the
      Public Records Act may not be used for commercial purposes."
    - **Owner (2026-10-02): "yes non-commercial"**, a free portfolio map
      with nothing sold.
    - **Owner: "yes"**, the page discloses the Board's notice that its list
      reports "contain possible errors due to a known data transfer issue",
      if it is still up at build.
    - The page states the list's date and never calls it complete or
      current. No wording is prescribed, and nothing is owed. The removal
      contact is publicrecords@lcb.wa.gov.
  - **Snohomish County's "Food Service Establishments (2025)" layer: SILENT.**
    - Item `75bf161b46ba484a97e6d7f1c63f21a4`, published by Public Works
      Solid Waste and not in the county's open-data catalogue. Its
      `licenseInfo`, description and metadata use limits are all empty.
    - The county's GIS "Terms of Use and Data Disclaimer" covers data
      "acquired from this site", which does not strictly reach this item.
      It requires non-commercial use of lists of individuals, the usual
      accuracy caveats, and a hold-harmless for errors in the data.
    - The website's footer reads "All rights reserved".
    - **The owner decides** between the permissive reading (King County's
      shape, with the removal rule as the safety net) and treating the layer
      as unlicensed, which would mean asking gis@snoco.org.
      🚨 OPEN.
- **The Snohomish layer's real date.** Nothing in it is dated finer than
  "on or before 2025-11-19" (see item 4 below).
- **Bellevue's issue-date cutoff and Seattle's licence-year filter**: the
  owner's calls (below).

---

## The regional screen - every jurisdiction on the 1 and 2 Lines (2026-10-01)

The owner's scope (2026-10-01): **a regional build with multiple city
registers**, held as before. This section is what that build has to pull. It
comes from staging, using one Overpass query and four metadata-only screens.
Nothing was downloaded in bulk and no request was sent. The scratch output is
in that session's scratchpad.

### Stations: 39, in 11 cities (Sound Transit GTFS, 2026-10-02)

**The rail source is Sound Transit's GTFS**, `https://www.soundtransit.org/GTFS-rail/40_gtfs.zip`
(it redirects to Sound Transit's `gtfs.sound.obaweb.org/prod/40_gtfs.zip`),
release `SC-Fall-2026.3`, `feed_info` 2026-09-01 to 2027-03-26.
- **Routes:** 1 Line "Lynnwood - Federal Way" (`100479`) and 2 Line
  "Lynnwood - Downtown Redmond" (`2LINE`) are `route_type` 0, beside the
  T Line in Tacoma (0, out of scope), two Sounder lines (2) and two shuttle
  buses (3). Match on the names: the 1 Line's id is a bare number.
- **The 2 Line now runs to Lynnwood**, sharing the 1 Line's track from
  Lynnwood to International District/Chinatown: 14 stations are on both.
- **Stations:** 78 platforms, `parent_station` filled on every one, 39
  stations, median nearest-neighbour 1,346 m.
- **By city** (point in King County's city polygons; the two Snohomish
  stations by name): Seattle **18**, Bellevue 6, Redmond 4, Shoreline 2,
  SeaTac 2, Kent 2, Tukwila 1, Federal Way 1, Mercer Island 1, Lynnwood 1,
  Mountlake Terrace 1.
- **Against the OSM set below:** the same stations, plus **Pinehurst**
  (Seattle, between Northgate and Shoreline South), which opened on
  2026-09-30 per the feed's own `modifications.txt` and which the OSM
  relations did not yet carry. The OSM table also sums to 38, not 37: the
  "37" was a miscount.
- **No `pickup_type`/`drop_off_type` columns**, so the boardable test has
  nothing to read; every station is a public stop.

The 2026-10-01 OSM set, kept as the cross-check. From OSM's four Link route relations (1 Line 3494092 and 5517060; 2 Line
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
    598 of them in Lynnwood and 92 in Mountlake Terrace **by postal city**
    (398 and 74 by the city itself; item 4 below). It has **no date,
    status or licence field**, so it fails the currency rule.
  - The county health department's portal is per-search only.
  - **MEASURED 2026-10-02:** the layer is owned by a county Public Works
    account and tagged "Food, Solid Waste" (its other fields are waste
    haulers and the nearest yard-waste site), so it is a solid-waste
    product built from the Health Department's permit list, not the Health
    Department's own publication. Its permit types and `PR`/`FA` ids are
    the Health Department's.
- **Statewide: WA Liquor and Cannabis Board on- and off-premise lists**
  (XLSX, dated 2026-09-29).
  - The only source spanning both counties: food (on-premise) and
    grocery/convenience (off-premise).
  - ~~**Not downloaded**: that needs the owner's OK.~~ The on-premise list
    was downloaded on 2026-10-02 (`data/seattle/raw/`, 9,993 rows) for the
    Snohomish check in item 4; the off-premise list was not.
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

1. **Seattle's register: PERMITTED WITH CONDITIONS** (`licence-read`,
   2026-10-01).
   - **Why it is permitted.** The layer is federated on data.seattle.gov
     (`wmtg-dzy4`), whose Open Data Terms of Use and Open Data Policy V1.0
     support reuse. No attribution is required, though crediting "City of
     Seattle" is recommended, and nothing is owed.
   - **The condition.** Data that can be "configured as a list of
     individuals … is not to be used for a commercial purpose". The owner
     confirmed the project is non-commercial ("no commercial, nothing sold",
     2026-10-01), and it must stay so: no ads, no paid tier, no client use.
   - **What is never published:** contact names, phones, mailing addresses,
     and person-named trade names.
2. **Bellevue's register: read as permitted (owner, 2026-10-01, option 1:
   "defensible").**
   - **The licence read found it ambiguous.** The data's licence field bars
     only "commercial use or sale … without express written authorization".
     The portal's linked Terms of Use allow only "own personal,
     non-commercial use", with all other rights reserved.
   - **The owner's reading.** The data's own licence field governs the
     data, and a free, non-commercial map falls outside its one
     prohibition. Credit the City of Bellevue.
   - **The safety net** is the removal rule: if Bellevue objects, the layer
     comes down first.
   - **Data quality.** Licences never expire, so closed businesses linger
     (2,938 in-city active rows were issued before 2015). An issue-date
     cutoff is measured at build and brought to the owner (4c).
   - **MEASURED 2026-10-02 for 4c** (82,155 rows, last edited 2026-09-27;
     "in-city" is a filled `NeighborhoodArea`, which every active in-city
     row has with `PhysicalCity` BELLEVUE):
     - **1,632 active in-city rows in the buckets** under today's NAICS
       carve-outs (Retail 863, Personal services 401, Food service 368).
       The 2026-10-01 figure of 1,770 used the older prefix set.
     - **Issue years:** 1 to 15 a year before 2000, 10 to 58 a year from
       2000 to 2017, then 74, 66, 57, 90, 80, and 150 to 181 a year from
       2023 (148 so far in 2026).
     - **Share issued before each candidate cutoff:** 2010: 325 (19.9%);
       2015: 504 (30.9%); 2018: 633 (38.8%); 2020: 773 (47.4%).
     - **No field signals closure except `CancelDate`.** `SysChangeDate` is
       2026-09-27 on every row (a load stamp); `FirstActivityDate` tracks
       the issue date (median difference 0 years); there is no status,
       renewal or tax-filing date.
     - **Cancellations are recorded, but fewer lately:** 154 to 339 bucket
       rows a year from 2009 to 2022, 408 in 2023, then 96 in 2024, 111 in
       2025 and 26 so far in 2026. So recent closures may linger longest.
     - **The trade name is missing on old rows.** `Dba` is blank on 324 of
       the 325 pre-2010 rows and 157 of the 179 from 2010-14, against 39% in
       2015-17, 18% in 2018-19 and 7 to 11% since. Overall 623 of 1,632
       bucket rows have no trade name, and 98 of those are sole
       proprietorships, whose legal name is a person's.
     - **Control: King County food inspections** (postal Bellevue, 832
       businesses inspected in 2025 or 2026). Share of Bellevue's active
       food-service rows with a currently inspected food business at the
       same street address: before 2010, 42% (66 rows); 2010-14, 77% (39);
       2015-17, 93%; 2018-19, 87%; 2020-22, 89%; 2023-26, 81%. Names cannot
       be compared before 2015, because the old rows have none.
   - **Privacy.** 1,174 sole proprietorships, and 4,185 rows in residential
     zones. `check_personal_exposure.py` is essential. **MEASURED
     2026-10-02, bucket rows only:** 217 sole proprietorships, 392 in
     residential (`R-`) zones.
3. **King County food inspections**, joined to the parcels: food for every
   King County city and the unincorporated rings. **Read as permitted
   (owner, 2026-10-01, option 1).**
   - **The licence read found it ambiguous.** The Socrata dataset is
     declared Public Domain, and the portal's linked data terms (the Open
     Data T&C, now a 404, last archived 2023) granted reuse. The live
     site-wide kingcounty.gov Terms forbid publishing without written
     permission.
   - **The owner's reading.** The dataset's declaration and the data terms
     govern.
   - **Display** the publisher's attribution, "Public Health – Seattle &
     King County". Display the Open Data T&C's required legend, "Data
     provided by permission of King County", since the permissive reading
     rests on those terms.
   - **Do not** use King County's logo or marks, and do not imply
     endorsement.
   - **From the address points, take only the geometry and the County's
     own fields (PIN, address).** `CTYNAME`, `POSTALCTYNAME` and the ZIP
     fields come from the USPS ZIP+4 product. Scope cities by
     point-in-boundary.
   - **The safety net** is the removal rule.
4. **Lynnwood and Mountlake Terrace food: the 2025 Snohomish layer
   (owner, 2026-10-01, 4a)**, "Food Service Establishments (2025)": 598 and
   92 points.
   - **The rule:** a frozen part beside a current whole, its date on the
     page (Tokyo's precedent).
   - **Two checks at build, or the stations go hollow:**
     - **It is a complete snapshot.** Compare it with the county's
       published count of permitted establishments, and with the Liquor
       Board's on-premise rows (Lynnwood 113, Mountlake Terrace 24).
     - **Its date comes from more than the catalogue's "(2025)" label.**
   - **Both checks MEASURED 2026-10-02.**
   - **Points are permits, not places:** 3,699 permits at 3,131 facilities
     (`USER_Facility_ID`). Permit types are the Health Department's own
     (seating and risk classes, school kitchens, mobile food, catering,
     donated-food distributors, vending). The `Icon` field sorts them:
     Restaurant 2,669, Grocery 476, School 269, Food Truck 122, Donation
     Center 73, Catering 68, Vending 14, Concession 8.
   - **598 and 92 are postal cities.** By the layer's own jurisdiction
     field (`User_Fld`), the City of Lynnwood has **398 points at 345
     facilities** and Mountlake Terrace **74 points at 66 facilities**.
     Postal Lynnwood also holds 167 unincorporated points. Scope by
     point-in-boundary, as for King County.
   - **Complete snapshot: yes, as far as two controls can see.**
     - **The county's published count:** only a county total exists. The
       Health Department's Food Safety Program page says "about 3,500
       permitted retail food establishments"; there is no per-city count
       and no annual report with one. The layer's 3,699 permits at 3,131
       facilities sit either side of it.
     - **The Liquor Board's on-premise list** (2026-09-29): of the active
       rows (Lynnwood 102 of the 113; Mountlake Terrace all 24), the layer
       holds **97 of 102 (95%)** and **22 of 24 (92%)** by trade name or
       street address, postal city against postal city. A miss can be a
       name the two registers spell differently.
   - **Its date: the data are no newer than 2025-11-19.**
     - The feature service and its service definition were created on
       2025-11-19; the service declares `hasStaticData`.
     - The layer's `lastEditDate` is 2026-05-28, and its web map and
       dashboard were saved that day. But `OBJECTID` runs 1 to 3,700 with
       one gap (3,132): one feature was deleted, nothing was reloaded. A
       reload would have renumbered or appended above 3,700.
     - No field carries a date. The Liquor Board's start dates cannot date
       it: every licensee that started after mid-2025 and is in the layer
       is an ASSUMPTION, an existing business under a new owner, often under
       the old trade name.
     - **So the page date is "2025"**, read as a list taken on or before
       2025-11-19: 10 to 11 months old at build, inside the five-year
       currency window as a frozen part.
   - **Licence:** its `licenseInfo` is empty. A licence read is owed at
     build. _Verdict pending (another agent, 2026-10-02)._
5. **A partial retail layer in every city outside Seattle and Bellevue:
   the Liquor Board's off-premise licences (owner, 2026-10-01).**
   - **What it is:** "Off Premise" list, `lcb.wa.gov/records/frequently-requested-lists`,
     dated 2026-09-29.
   - **Active rows only.** These are grocery stores (beer/wine), spirits
     retailers, beer/wine specialty shops and wine resellers.
   - **Disclosed as "shops licensed to sell alcohol only"**, Zurich's
     precedent for a partial retail layer.
   - **Location:** premises addresses, joined to the county address points.
     There are no coordinates.
   - **Never published:** `Licensee`, phone and mailing columns. Trade name
     only.
   - **Terms:** RCW 42.56.070(8), "not for commercial purposes", met by the
     owner's non-commercial confirmation. A formal licence read is owed at
     build.
   - **Counts (all statuses):** Lynnwood 133, Kent 134, Federal Way 106,
     Shoreline 66, Redmond 64, Tukwila 48, SeaTac 40, Mountlake Terrace 25,
     Des Moines 24, Mercer Island 16.
   - **On premise (9,993 rows)** is a check on the Snohomish layer, not a
     layer.
6. **Personal services outside Seattle and Bellevue: none published,
   disclosed per city** (owner, 4b). The only routes are public-records
   requests, which are outreach and not taken.
7. **Rings that cross a city line** take the neighbour's data or are stated
   as unmapped. Des Moines and unincorporated King County have King County
   food and the off-premise layer only.

---

## Open for the owner (2026-10-02)

Recommendations from the 2026-10-02 measurements. None is decided.

1. **Bellevue's issue-date cutoff (4c). Recommend 2010-01-01**, with every
   row that has no trade name shown by its category, never by its legal
   name.
   - **Why 2010:** it is where the food control breaks. Before 2010 only 42%
     of active food rows have a currently inspected food business at their
     address; from 2010-14 it is 77%, level with the 81-93% of later years.
     It drops 325 of 1,632 bucket rows (19.9%).
   - **The trade-off:** a cutoff is blunt. It drops long-standing shops that
     are still open, perhaps two in five of those 325 by the food control,
     and keeps whatever closed after 2010 without a cancellation (only 26
     cancellations so far in 2026).
   - **Why not 2015:** it drops another 179 rows that look as live as recent
     ones by address. Their real problem is the missing trade name (157 of
     179), which the name rule handles without dropping them.
   - **An alternative to weigh:** take Bellevue's food from King County's
     inspections, as for every other King County city, and Bellevue's
     register for retail and personal services only. Food would then be
     current by construction, at the cost of a source split inside one
     city.
2. **Seattle's headquarters rows. Recommend keeping both `HEADER QUARTER`
   and `BRANCH`, with no head-office rule.** `HEADER QUARTER` is a
   business's primary location (91% of the storefront rows), not an office.
   Taichung's rule would flag 9 rows here. If a check is wanted,
   hand-sample 40 of the 378 headquarters rows whose business also has
   branches at build, and bring the result back.
3. **Seattle's lapsed licences (new). Recommend keeping licence years 2025
   and 2026 and dropping 2023 and 2024** (986 bucket rows, 9.8%).
   - Seattle's licences all fall due on 31 December, so a 2025 licence is
     nine months late, not necessarily closed: its food rows still match a
     current inspected business by name at 48%, against 65% for 2026.
   - **The trade-off:** the 2023 and 2024 rows still match by name at 35 to
     38%, so roughly half of the dropped rows may be open businesses that
     never renewed. The stricter option (2026 only) drops 2,044 rows (20%).
4. **Snohomish layer: what to keep.** Recommend the Restaurant and Grocery
   points only, which follows the owner's rule on canteens, caterers and
   mobile food (R1, 2026-09-29): school kitchens, donated-food
   distributors, food trucks, catering, vending and concessions are out.
   In the City of Lynnwood that leaves 310 facilities, in Mountlake Terrace
   56. The page date is "2025".
5. **Following precedent, not for a call:** scope Seattle's register to the
   city polygon (drops 1,012 rows, 168 in the buckets); draw Pinehurst,
   which the current feed serves; read Sound Transit's Open Transit Data
   terms before the build.
