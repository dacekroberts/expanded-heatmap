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
- ~~SacRT's timetable is unread~~ **read 2026-09-29** on SacRT's schedule
  pages: Blue and Gold every 15 minutes by day.

| | |
|---|---|
| Rail | SacRT light rail, Blue / Gold / Green: **39 stations inside the city** (Blue 26, Gold 18, Green 9; OSM), 765 m median gap |
| Register | the City's **Business Operation Tax Information** (ArcGIS item `f4ee567a…`): 63,904 rows, **no geometry** |
| Storefronts (Active, unexpired, `Location_City = SACRAMENTO`) | retail **~1,670** · food **~1,130** · personal services **~730** |
| Coordinates | **the US Census Bureau batch geocoder** (owner, 2026-09-29); the City's All Addresses layer (93.0% of a sample, but covered by no terms) is not used |
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
- **Frequency: READ 2026-09-29 on SacRT's own schedule pages**
  (`sacrt.com/routes-schedules/#533` and `#507`, now served as text tables;
  the GTFS on `apps.sacrt.com` still serves an expired certificate and was
  not fetched). Weekdays:
  - **Blue** (Watt/I-80 → CRC): every **15 min** from 05:03 to 17:48, then
    every 30 min to 22:48.
  - **Gold**: **4 an hour** at Sacramento Valley Station, the in-city end
    (every 15 min, 05:44 to 18:59), and 3 an hour from Historic Folsom;
    every 30 min in the evening.

  **Both clear 15 minutes by day**, so the question of whether frequency
  gates this track does not arise. The page states the 30-minute evenings.
- ⚠️ **The Green Line**: SacRT's schedule pages list **only Blue and Gold**.
  The Gold Line's stop list now ends at 8th & K, 8th & H and Sacramento
  Valley Station, and no schedule serves `7th & Richards / Township 9`.
  OSM's two Green relations (2379220, 2379221) may be **stale**. **At build,
  confirm on SacRT's site whether the Green Line runs.** If it does not,
  drop its relations and any station only it served, and re-count (39 inside
  includes Green's 9).

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

**⚠️ But no terms cover it, so it is NOT used: the owner chose the Census
geocoder, 2026-09-29.** It is a public ArcGIS item **not shared to the
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
  so the owner decides with that fact in view. **ACCEPTED by the owner,
  2026-09-29**, with that fact stated.
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

1. ✅ **The indemnity: ACCEPTED (owner, 2026-09-29)**, as Hong Kong's was.
   Recorded in `docs/data_sources.md` beside Hong Kong's.
2. ✅ **"Request permission to use" is Esri's label for an empty licence
   field, not a term (owner, 2026-09-29)**: the City's own Terms grant use.
3. ✅ **Address source: the US Census Bureau batch geocoder (owner,
   2026-09-29)**, `pipeline/census_geocoder.py`. The City's All Addresses
   layer is not used. Measure the match rate at build and apply the bounds
   check. The Census answer carries no home signal, so `MAILTYPE` is lost;
   the `ON FILE` rows and the excluded individual categories remain the home
   screen.
4. ✅ **Frequency: read 2026-09-29 on SacRT's schedule pages** (below).
   Blue and Gold both run every 15 minutes by day, so the gate question is
   moot.
5. The couplet aliases; pet supplies versus grooming; **the Green Line**
   (below).

**Flag for the cleanup role (held macro-map work)**: Sacramento takes the
light-rail network colour.

## ✅ Built 2026-09-29 — what the build settled

- **The Green Line is suspended** (since 2025-06-16; reopening expected
  mid-October 2026, sacrt.com/greenline): not drawn, Township 9 closed for
  works (owner; the cross-city rule is now in docs/category_rules.md).
- **OSM lags SacRT on Blue**: Morrison Creek's stop nodes are unnamed, and Dos
  Rios (opened 2026-09-28) is unmapped, placed from Wikidata (owner). Gate 3
  is exact against SacRT's own timetables: Blue 28, Gold 27.
- **The couplets merge** (owner): Capitol, County Center, K Street. 8th & O
  stays separate.
- **Location_City is postal**: 125 geocoded "Sacramento" addresses lie
  outside the City and are dropped by the polygon.
- **Names**: 525 that read as a person's show the description (owner); 4 at an
  apartment are left off. Caterers and clothing alterations are out, on
  docs/category_rules.md (R1; repairs).
- The Census geocoder matched 98.0%. 3,335 storefronts are placed; 1,378
  (41.3%) are in the rings.

## Still unknown

- Whether the Green Line still runs (build-time check, above).
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
