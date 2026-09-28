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
- Every other jurisdiction on Link's 1 and 2 Lines. Each is its own Step 0,
  and Seattle's data says nothing about any of them.
- The rail leg: the Link GTFS has not been read for this brief.
