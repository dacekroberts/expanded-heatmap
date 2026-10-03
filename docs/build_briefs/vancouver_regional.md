# Vancouver (Regional) — extension brief: Burnaby, New Westminster, Coquitlam

**Probed 2026-10-02 (staging; the owner: "probe the not-ready extensions
first then we can push these all at once").** Vancouver is built. This adds
**20 SkyTrain stations** now excluded:

| City | Stations |
|---|---|
| Burnaby | 11 |
| New Westminster | 5 |
| Coquitlam | 4 |

Two cities stay out:
- **Richmond's 8**: Band R; its site terms allow research and private use
  only.
- **Port Moody's 2**: its licence table has no address or geometry.

The build is HELD until the owner releases all five extensions together.

Read `multi-source-city`, `docs/canada_retrospective.md` and Vancouver's own
pipeline first. None of the three cities has a licence row yet in
`docs/data_sources/canada.md`. Each needs one, with its required statement.

## Burnaby

- **Source:** `gis.burnaby.ca` `OpenData/OpenData1/MapServer/17`, "Business
  Licences". It answered a plain scripted client with 200 on 2026-10-02 (an
  earlier probe was refused). There were 11 paged queries, no browser and no
  user-agent change. The cache is
  `data/burnaby/raw/burnaby_business_licences.csv`.
- **Rows:** 20,054 × 17, all `APPROVED`, with coverage ending 2026-10-31 to
  2027-09-30. The layer rolls monthly; its latest start is 2026-10-01.
- **Location:** a point on every row; all 20,054 fall inside Burnaby (the BC
  municipalities layer). **One placeholder point holds 2,179 contractor and
  mobile rows**, none in a bucket. Step 2 asserts no kept row sits on it.
- **Buckets** on `LICENCE_TYPE_NAME` (142 values, mapped by precedent),
  de-duplicated on licence and point:

  | Bucket | Rows |
  |---|---|
  | Retail | 964 |
  | Food | 746 |
  | Personal services | 433 |
  | **Total** | **2,143** |

  The busiest rings are Metrotown (641), Patterson (426) and Royal Oak
  (352).
- **Personal data:**
  - **`ACCOUNT_NAME` (the owner's name) is never fetched.**
  - `LEGAL_TYPE` is the PROPERTY's legal type (LAND, STRATA), not a business
    form. Do not read it as one.
  - The 2,946 home-based rows and the rentals all fall outside the buckets.
  - Trade name equals account name on 0 bucket rows.
- **Licence: PERMITTED WITH CONDITIONS.** Burnaby prints the BC default
  statement verbatim: "Contains information licensed under the Open
  Government Licence – British Columbia." It asks for a link to the licence
  where possible.

## New Westminster

- **Source:** `services3.arcgis.com/A7O8YnTNtzRPIn7T/.../BUSINESS_LICENSES_(RESIDENTS)/FeatureServer/0`,
  a table of 2,736 rows, last edited 2026-09-27.
- **Buckets:** 856 resident licences under today's rules (built
  2026-10-03): retail 379, food 294, personal services 183; 853 placed by
  the join. The probe's 907 (2026-09-30) predates `naics.py`'s 2026-09-29
  exclusions as applied: 9 caterers (72232) and 42 catch-all or funeral
  rows (81299, 8122); the layer is unchanged since 2026-09-27. Approved
  2025–2026, classified by NAICS. Drop `RESIDENT_STATUS` = NON-RESIDENT.
- **Placement:** join `CIVIC_ADDRESS` to the City's `Address_Point` layer;
  99.8% joined of 42,690 points.
- **Never fetch** `LICENCEE_NAME` or `MAILING_ADDRESS`.
- **Required statement:** "Contains information licenced under the Open
  Government Licence - City of New Westminster."

## Coquitlam

- **Source:** `services2.arcgis.com/Q6Lq3evZUGfPrN7o/.../Business_Licenses/FeatureServer/0`,
  12,008 rows, each licence listed twice. Last edited 2026-09-04; at most
  1,000 rows per query.
- **Classify** on `U_SUBCODEDESC`. Built 2026-10-03: 1,026 kept (retail
  454, food 332, personal services 240) of 6,002 licences, after collapsing
  the double listing; 10 mall kiosks out (9 by subtype, 1 by a "Kiosk"
  unit).
- **Status:** Issued, plus Renewal. Renewal confirmed current at build: the
  coming year's renewal folder, most businesses' only record.
- **Location:** `LAT`/`LONG` on each row hold **Web Mercator meters**
  (EPSG:3857), not degrees. One name field only, `COLBUSINESSNAME`.
  Licence: Open Government Licence – Coquitlam v1.0 (OGL-BC 2.0 with the
  City named).
- **Never fetch** `COL_BUSINESSPHONE` or `EMAILADDRESS`.
- **Required statement:** "Contains information licensed under the Open
  Government Licence – Coquitlam."

## The owner's calls (2026-10-02: "approve the three vancouver calls")

1. ✅ **Burnaby's credit:** show the BC wording as printed, credit "City of
   Burnaby" and link its licence page.
2. ✅ **`RETAIL SALE, RENTAL & REPAIR`** (32 rows): Retail, keeping the mixed
   type whole.
3. ✅ **Coquitlam's mall kiosks** (about 9): leave them out.

## Before publishing

Run `check_personal_exposure.py` and record the privacy verdict. Add the
three licence rows and their notices. The page becomes "Vancouver
(Regional)" if it is not already.

## Checks (added by the extensions build, 2026-10-03)

```brief-checks
[
  {
    "id": "burnaby-licence-layer",
    "claim": "Burnaby's Business Licences layer (MapServer 17) still publishes the fields step 2 reads, and ACCOUNT_NAME, which is never requested",
    "kind": "http_contains",
    "url": "https://gis.burnaby.ca/arcgis/rest/services/OpenData/OpenData1/MapServer/17?f=json",
    "present": ["TRADE_NAME", "LICENCE_TYPE_NAME", "LICENCE_NUMBER", "ACCOUNT_NAME"]
  },
  {
    "id": "coquitlam-licence-layer",
    "claim": "Coquitlam's Business_Licenses layer still publishes the subtype, status and Web Mercator LAT/LONG fields the loader reads",
    "kind": "http_contains",
    "url": "https://services2.arcgis.com/Q6Lq3evZUGfPrN7o/arcgis/rest/services/Business_Licenses/FeatureServer/0?f=json",
    "present": ["U_SUBCODEDESC", "U_STATUSCODEDESC", "COL_FOLDER", "COLBUSINESSNAME"]
  },
  {
    "id": "new-westminster-licence-table",
    "claim": "New Westminster's resident licence table still carries NAICS codes and a civic address to join",
    "kind": "http_contains",
    "url": "https://services3.arcgis.com/A7O8YnTNtzRPIn7T/ArcGIS/rest/services/BUSINESS_LICENSES_(RESIDENTS)/FeatureServer/0?f=json",
    "present": ["NAICS_CODE", "CIVIC_ADDRESS", "BUSINESS_NAME", "RESIDENT_STATUS"]
  },
  {
    "id": "new-westminster-address-points",
    "claim": "New Westminster's Address_Point layer, the join's address file, still carries ADDRESS, HOUSE and STREET",
    "kind": "http_contains",
    "url": "https://services3.arcgis.com/A7O8YnTNtzRPIn7T/ArcGIS/rest/services/Address_Point/FeatureServer/0?f=json",
    "present": ["ADDRESS", "HOUSE", "STREET"]
  }
]
```
