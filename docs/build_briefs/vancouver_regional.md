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
- **Buckets:** 907 resident licences (2026-09-30): retail 379, food 303,
  personal services 225. Approved 2025–2026, classified by NAICS. Drop
  `RESIDENT_STATUS` = NON-RESIDENT.
- **Placement:** join `CIVIC_ADDRESS` to the City's `Address_Point` layer;
  99.8% joined of 42,690 points.
- **Never fetch** `LICENCEE_NAME` or `MAILING_ADDRESS`.
- **Required statement:** "Contains information licenced under the Open
  Government Licence - City of New Westminster."

## Coquitlam

- **Source:** `services2.arcgis.com/Q6Lq3evZUGfPrN7o/.../Business_Licenses/FeatureServer/0`,
  12,008 rows, each licence listed twice. Last edited 2026-09-04; at most
  1,000 rows per query.
- **Classify** on `U_SUBCODEDESC`. Estimated, with rows halved: retail about
  455, food 339, personal services about 243.
- **Status:** Issued, plus Renewal. Confirm Renewal as current at build.
- **Location:** lat/long on each row (OGL-BC 2.0).
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
