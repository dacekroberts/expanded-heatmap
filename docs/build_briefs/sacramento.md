# Sacramento — build brief

**Step 0 measured 2026-09-28 (wave 2's US screen), 2026-09-29 (the
light-rail test) and 2026-09-29 (this brief).** Run
`python scripts/brief_check.py sacramento` before writing code.

---

## The one-line summary

**A city business-tax register that needs an address join, three light-rail
lines, and three owner calls, all on terms rather than data.** The data
works: 93% of a sample joins, and 38% of storefronts sit within 0.6 mi. The
open questions:
- the register's terms carry an **uncapped indemnity accepted by use** (Hong
  Kong's shape, which the owner accepts source by source);
- the address layer that joins so well is **not covered by any terms at all**;
- **SacRT's timetable is still unread**. Under the light-rail test that is
  a disclosure, not a gate.

| | |
|---|---|
| Rail | SacRT light rail, Blue / Gold / Green: **39 stations inside the city** (Blue 26, Gold 18, Green 9; OSM), 765 m median gap |
| Register | the City's **Business Operation Tax Information** (ArcGIS item `f4ee567a…`): 63,904 rows, **no geometry** |
| Storefronts (Active, unexpired, `Location_City = SACRAMENTO`) | retail **~1,670** · food **~1,130** · personal services **~730** |
| Coordinates | an address join: **93.0%** of a 200-row sample against the City's All Addresses layer (but see the licence) |
| In the 0.6 mi ring | **~38.2%** (186 placed sample rows; 12.4% at 0.3 mi) |
| Rings | **standard 0.1 / 0.2 / 0.3 / 0.6 mi** (765 m) |
| Projected CRS | **EPSG:32610** (UTM 10N, 121.49° W) |
| Region | `"North America"` |

---

## Rail — OSM; the feed is unreachable and its timetable unread

- **SacRT's GTFS host serves an expired certificate** (2026-09-29). **Never
  bypass SSL.** The Mobility Database mirror (`mdb-2137`) is the **January
  2025** edition (2025-01-05 → 2025-04-05): expired, and no current read.
  Its route colours: Gold `EED211`, Green `008040`, Blue `0000FF`.
- **Draw the rail from OSM** (the `osm-rail` skill): six relations,
  2352701/2352702 Gold (`#ffba00`), 2378981/2378982 Blue (`#002666`),
  2379220/2379221 Green (`#006633`), each named ("Gold Line: Sacramento
  Valley Station => Historic Folsom"). City boundary: OSM relation 6232940,
  257 km².
- **Stations**: 53 names on the three lines, **39 inside the city**. Gold
  loses 12 of 30 to Rancho Cordova and Folsom, and Blue 2 of 28. The screen's
  41 was a count of unique names before the boundary test was redone. Step 1
  names each excluded station's city (the Los Angeles rule).
- ⚠️ **Downtown one-way couplets**: pairs such as `7th & Capitol` /
  `8th & Capitol`, `7th & I/County Center` / `8th & H/County Center`, and
  `8th & K` / `St. Rose of Lima Park` sit within ~250 m. Read each pair at
  build. An alias merges only what was looked at (Oslo's rule). Houston's
  Capitol / Rusk couplets were one station each; here the names differ
  more, so look before merging.
- **Frequency, the handoff's "read the timetable first"**: under the owner's
  light-rail test, frequency **gates only converted railway**, and SacRT's
  track was built as light rail (1987 onward; the Gold Line's Folsom
  extension runs on a former freight right-of-way, **built new as light-rail
  track**, not an operating railway converted in service like Aarhus's
  Odderbanen). **So the timetable is a page disclosure, not a gate.** That
  reading is a judgment and is flagged for the owner. The read itself:
  **from the owner's browser** (SacRT's schedule pages are images; the
  Priority 2 lane of reads from the owner's browser), or the feed once its
  certificate is renewed.

---

## Business leg — the City's Business Operation Tax register

`https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/account_data_with_header_NEW/FeatureServer/0`:
a table, **no geometry**, last edited 2026-09-28.

| | |
|---|---|
| Rows | 63,904: Active 24,040 · Closed 21,567 · Expired 14,489 · Pending 1,940 · Inactive 1,231 |
| **Active but past `Current_Expire_Date`** | **2,768 (11.5%)**, mostly 2025–26: **apply the expiry at the fetch date** (Chicago's rule, as Buffalo) |
| Active, unexpired, `Location_City = SACRAMENTO` | **11,927** |
| **`Location_City = "ON FILE"`** | **5,724 of the Active rows**: the address is withheld (online sellers 187, cottage food 109, bookkeepers…). **Unmappable by construction, and correctly so**: these are mostly home businesses |

### ⚠️ Columns never to load

`Principal_Owner_First_name`, `Principal_Owner_Last_Name`,
`Primary_Phone_number` and every `Mail_*` field. **Step 2 reads by an
explicit column list and asserts these are absent** (Norway's shape). Display
`Business_Name`; run `check_personal_exposure.py sacramento`, since a sole
proprietor's business name can be their own.

### Buckets — the City's own 148 descriptions, mapped by hand

| Bucket | Descriptions (in-city, Active, unexpired) | Rows |
|---|---|---|
| Retail | Retail Sales - General 965, Automobile Dealers 224 + 53, Convenience Store 124, Grocery/Supermarkets 107, Automotive - Parts 88, Liquor 38, Tobacco 36, Pharmacies 15, Secondhand 13, Department Store 3, Pawnbrokers 1 (+ Pet supplies 29, mixed with grooming: a call) | **~1,670** |
| Food | Restaurants 732, Food - Other 136, Cafes 122, Bars - Taverns 53, Catering 51, Bakery 36 | **~1,130** |
| Personal | Beauty - Parlors & Shops 382, Massage - Establishment 201, Barbershops 57, Tattoo 37, Laundry Services 30, Laundromats 13, Alterations/Tailors 11 | **~730** |
| **Excluded** | **Retail Sales - Online** 89; **Mobile / Sidewalk Vendor - Food** 48; **Cottage Food** 8 (a home kitchen); **Beauty - Independent Stylist** 200 and **Massage - Technician** 71 (a person, not a premises: New York's chair-renter rule, `docs/excluded_categories.md`) | |

`Service - General` (656) and `Other` (345) are catch-alls with no bucket.
Leave them out, and record the shares (`docs/category_rules.md`).

---

## Coordinates — the join works; its source is the problem

The City's **All Addresses** layer
(`https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/All_Addresses/FeatureServer/2`):
**260,455 parcel polygons** with `FULLADDRESS`, `APN` and a **`MAILTYPE`**
(Business / Resident / both). **93.0% of a 200-row bucket sample** matched on
number + street name. Of the matches: Business 120, Resident 26, both 20,
unknown 20. So `MAILTYPE` is a usable home signal, like Houston's `addrtype`
but better filled.

**⚠️ But no terms cover it.** It is a public ArcGIS item **not shared to the
City's Open Data portal** (`groupIds: []`), and every licence field is empty.
The portal's Terms define Data as what is "made available for download
through" data.cityofsacramento.org. **Alternatives, in order:**
1. **The US Census Bureau batch geocoder** (`pipeline/census_geocoder.py`;
   public domain; Los Angeles, New York, D.C.). Measure its rate at build.
2. Sacramento County's address points, after a licence read.
3. All Addresses, only if the owner accepts using an uncovered public layer.

---

## ✅ / 🟠 Licence — READ 2026-09-29 (the `licence-read` agent)

**The register: PERMITTED WITH CONDITIONS, with two owner calls.** The City's
**Open Data Terms of Use** (`cityofsacramento.gov/.../OpenDataTermsOfUse.pdf`,
the same text as the Open Data Policy's pp. 13–18) govern the layer: "access
to and use of the Data", including any "Derivative Work". There is no
attribution clause and nothing to display.
- 🟠 **An uncapped indemnity**, accepted by conduct: the user "will
  indemnify, defend at his/her sole cost and expense, and hold harmless the
  City … even if the claim may be groundless, false or fraudulent". **Hong
  Kong's shape; the owner accepted Hong Kong's on 2026-09-22 and the CSDI's on
  2026-09-24, one source at a time.** ⚠️ **Acceptance is "by machine-consuming,
  or downloading and using the Data"**, and **this brief's measurement pulled
  the 24,040 Active rows** (without the owner, phone or mailing columns) on
  2026-09-29. That may already count. It is recorded here and in `DECISIONS.md`
  so the owner decides with that fact in view.
- 🟠 **The Hub page shows "No License Provided / Request permission to use"**,
  Esri's label for an empty licence field. The Terms incorporate anything
  "stated … on the page from which the Data is accessed". Read permissively,
  it is boilerplate; read strictly, it asks for permission first (the City's
  Formstack feedback form is the only channel). **The owner's call.**
- California law, Sacramento County venue; the Terms change on posting, so
  re-read them before publishing.

**SacRT's GTFS**: not read (unreachable). OSM rail avoids it.

---

## Build-time calls

1. 🟠 **Owner: the indemnity** (accept, as for Hong Kong, or not build).
2. 🟠 **Owner: "Request permission to use"**, as boilerplate or as a term.
3. 🟠 **Owner: the address source**: Census geocoder (recommended), the
   county's points, or the uncovered City layer.
4. **Owner: frequency as a disclosure, not a gate** (the Gold Line's right of
   way), and the timetable read from the owner's browser.
5. The couplet aliases; pet supplies versus grooming; `MAILTYPE = Resident`
   rows (drop, as recommended for Houston's `IS` at a residential point).

**Flag for the cleanup role (held macro-map work)**: Sacramento takes the
light-rail network colour.

## Still unknown

- SacRT's current frequency.
- The Census geocoder's match rate on this register.

```brief-checks
[
  {
    "id": "sacramento-register-no-geometry-active",
    "claim": "The Business Operation Tax layer is a table of about 24,040 Active rows (63,904 in all), with no geometry - an address join is required",
    "kind": "http_contains",
    "url": "https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/account_data_with_header_NEW/FeatureServer/0?f=json",
    "present": ["Current_License_Status", "Current_Expire_Date", "Location_City", "Principal_Owner_Last_Name"]
  },
  {
    "id": "sacramento-owner-columns-present",
    "claim": "The layer carries the owner's name and phone - step 2 must read by an explicit column list and assert these never arrive",
    "kind": "http_contains",
    "url": "https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/account_data_with_header_NEW/FeatureServer/0?f=json",
    "present": ["Principal_Owner_First_name", "Primary_Phone_number", "Mail_Street_name"]
  },
  {
    "id": "sacramento-all-addresses-mailtype",
    "claim": "The City's All Addresses layer (parcel polygons, 260,455) carries FULLADDRESS and MAILTYPE - the join target and a home signal, but covered by no terms",
    "kind": "http_contains",
    "url": "https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/All_Addresses/FeatureServer/2?f=json",
    "present": ["FULLADDRESS", "MAILTYPE", "esriGeometryPolygon"]
  },
  {
    "id": "sacrt-osm-relations",
    "claim": "OSM carries SacRT light rail as six relations in three refs, Blue, Gold and Green - the rail source while SacRT's feed host serves an expired certificate",
    "kind": "osm_route_refs",
    "bbox": [38.45, -121.56, 38.70, -121.15],
    "routes": ["light_rail"],
    "expect_refs": {"light_rail": 3},
    "require_refs": {"light_rail": ["Blue", "Gold", "Green"]}
  },
  {
    "id": "sacramento-is-utm-10",
    "claim": "Sacramento (121.49 W) is in UTM zone 10N",
    "kind": "utm_zone_from_longitude",
    "lon": -121.49,
    "expect": "EPSG:32610"
  }
]
```
