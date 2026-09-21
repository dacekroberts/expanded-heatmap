# City shortlist

Which US cities are viable for this project, and in what order to build
them. The history of how this list was produced and corrected is in
[`DECISIONS.md`](../DECISIONS.md) (2026-09-18, "City selection").

## Criteria

A city is viable if it has:

1. **Rail transit** worth mapping (light rail, subway, commuter rail; not
   buses alone).
2. **Public transit open data** - a working GTFS feed at minimum.
3. **A real, live, geocoded business dataset** with *some* usable
   classification field - NAICS or the city's own documented taxonomy - plus
   a street address and/or lat/long that is actually populated.

Criterion 3 must be **verified live** against the real API/schema and sample
rows. Dataset titles and search summaries proved unreliable: Denver and
San Jose both looked viable and were not.

The 25 largest US cities were screened on search results; the ten strongest
were then live-verified. Only those ten have live evidence below.

## Viable, in build order (ease of implementation)

Ease reflects: taxonomy already built (NAICS) or still a skeleton, API
simplicity, geocoding completeness, and the size of the rail system (a
bigger system means a bigger station-scope decision).

| # | City | Rail | Business data (live-verified) | Taxonomy | Status / notes |
|---|---|---|---|---|---|
| 1 | San Diego | MTS Trolley, 5 lines | City Business Tax Certificates CSV (`seshat.datasd.org`): `naics_code`, address fields, `lat`/`lng` | `naics` | **Built** |
| 2 | San Francisco | Muni Metro, 6 lines | DataSF Registered Business Locations (Socrata `g8m3-pdis`, `data.sf.gov`): `self_reported_naics_code`, `full_business_address`, `location` | `naics` | **Built** |
| 3 | Los Angeles | Metro Rail (A, B, C, D, E, K), 110 stations, 56 in the city | Listing of Active Businesses (Socrata `6rrh-rzua`, `data.lacity.org`): `naics`, `street_address`, `location_1`, `council_district` | `naics` | **Built.** ~9% of coordinates were corrupt (recovered by Census geocoding); in-city rows identified by `council_district`, not `city` |
| 4 | Chicago | CTA 'L' (7 lines drawn, 123 in-city stations; Metra not included) | Business Licenses (Socrata `r5kz-chrr`): address, `latitude`/`longitude` | `chicago_license` | **Built 2026-09-20.** No NAICS field: own license taxonomy, with catch-all license types classified by business activity; the source is a license-term history, filtered to active licenses and one row per site. Metra is a possible later addition |
| 5 | New York | Subway + Staten Island Railway (496 parent stations, drawn as 11 trunk lines; LIRR/Metro-North not included) | **Four** registries, because the city has no general business licence: DOHMH restaurant inspections (`43nn-pn8j`), NYS Retail Food Stores (`9a8c-vfzj`), NYS Appearance Enhancement & Barber businesses (`y3u4-jbgh`), DCWP premises licences (`w7w3-xahh`) | `new_york` (dispatches per source) | **Built 2026-09-21.** The DCA-only plan recorded here was wrong: that file is a regulated-activity licence list with no restaurants, grocery, clothing or salons in it. Only city needing multiple sources, and the only one not using the shared ring edges (496 stations, median 482 m apart). Retail is less complete than elsewhere |
| 6 | Philadelphia | SEPTA Metro: L, B, T and G (94 in-city stations, 4 lines drawn; Regional Rail not included) | L&I Business Licenses (Carto SQL API `phl.carto.com`, table `business_licenses`): 435,143 rows, 118,535 Active, 48 fields | `phl_licensetype` (verified, all 50 types) | **Built 2026-09-21.** The only **two-bucket** city: no personal-service licence exists in Philadelphia and Pennsylvania publishes none with addresses, so Personal services is absent rather than thin. The multi-source hunt came back empty — one registry, two buckets. First city needing two station rules at once (subway/el kept whole, street-running trolleys thinned) |
| - | Boston | MBTA rapid transit: Red, Orange, Blue, Mattapan, Green B/C/D/E (**71 of 125 stations in-city**; 14 `CR-*` Regional Rail lines not counted) | Food Establishment Inspections (CKAN `4582bec6`, 902,651 rows -> 2,628 active premises, 99.9% with coordinates), + Licensing Board `04dc653b` and Cannabis `e395fd88` for package stores | new module needed (`licensecat`: FS/FT/RF/MFW) | **Step 0 PASSED 2026-09-21, not built.** A **two-bucket** city like Philadelphia: Food service 2,237, Retail 385 unambiguous (+306 package stores and 43 cannabis that *overlap* it), **Personal services absent** - Massachusetts licenses cosmetology at state level with no address-bearing export. The thinnest candidate yet: ~2,740 sites over 71 stations, ~2.3x thinner per station than Philadelphia, and genuinely *food* density rather than commercial density. Do NOT use the official "Active Food Establishment Licenses" extract - it drops the `RF` Retail Food category entirely. Green Line is 4 street-running branches on a shared subway, San Francisco's shape, so it needs the sub-transit-line filters. All sources ODC-PDDL; MBTA needs one acknowledgement notice. See `docs/data_sources.md`, "Boston - Step 0 findings" |
| - | Washington D.C. | WMATA Metrorail, 6 lines, 98 stations (in-city share not yet measured; much of the system is in Virginia and Maryland) | Basic Business Licenses (`maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/DCRA/FeatureServer/0`): 278,747 rows, **76,107 Active**, 40 fields. `BUSINESSACTIVITY` (102 values), `CATEGORYSERVICETYPE` (17), `ENTITYTRADENAME`, `ENTITYTYPE`, `PREMISEINDC`, `WARD`, `SSL` (parcel), `MAR_ID` | new module needed | **Step 0 mostly done 2026-09-21; the strongest remaining candidate.** The only non-NAICS city so far with **all three buckets** from one registry: Food Services 4,901, Beauty and Grooming 486, and ~1,550 real retail. Three things settled: 49% of active rows are **residential rentals** (One Family Rental 25,587, Apartment 6,106 …) and must go; **`General Business` (14,770) is an office/professional catch-all** — law firms, engineering, consultancies — and must be excluded like LA's NAICS 812990; `LATITUDE`/`LONGITUDE` are **literally `39` and `-77` on every row** (0 rows in DC bounds), but `X_COORDINATE`/`Y_COORDINATE` are real **EPSG:26985**, verified by transformation, on 77% of storefront rows, with `MAR_ID` to recover the rest. Watch: trade name missing on 49% of storefront rows (the LA trap), and `BUSINESSOWNER*`/`AGENT*` name columns must never be published. **WMATA GTFS needs a free API key** (`api.wmata.com` returns 401); a keyless Mobility Database mirror exists |
| - | Seattle | Sound Transit Link (1 Line + 2 Line) | "Seattle Business License" (ArcGIS `services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Seattle_Business_License/FeatureServer/0`, layer "Business Locations (Active)"): **54,604 rows**, point geometry, `BUSLIC_NAICS_CODE` + `BUSLIC_NAICS_DESC`, `BUSLIC_SIC_CODE` + `BUSLIC_SIC_DESC`, `BUSLIC_TRADE_NAME`, `BUSLIC_LEGAL_NAME`, `BUSLIC_LOCATION_ADRS_TEXT` | `naics` (already built) | **DEFERRED by the owner 2026-09-21 — to be implemented later, not excluded.** Findings kept so returning to it costs nothing. On the evidence it is the **best-equipped candidate found**: an official nightly export from Finance & Administrative Services that is **active-only by construction**, carries real NAICS (so no new taxonomy module), a trade name, and point geometry — no geocoding step. Not on Socrata, which is why earlier screens missed it; it lives on ArcGIS under owner `SeattleData`. Still to do: the category distribution, the in-city check, `BUSLIC_LOCATION_TYPE` (values include "HEADER QUARTER" — headquarters vs branch needs a verdict), and the licence, whose `licenseInfo` is an as-is accuracy disclaimer rather than a grant. Privacy flags: `BUSLIC_CONTACT_NAME` is a person and `BUSLIC_PHONE_NUM` a phone number — both must stay unpublished (`drop_contact_details()` already covers the phone). Note this project's original prototype was Seattle's Link light rail |
| - | Miami | Metrorail (2 lines, 23 stations) + Metromover | Miami-Dade "Local Business Tax" (ArcGIS `services.arcgis.com/8Pc9XBTAsYuxx9Ny/.../Local_Business_Tax_Feature_Layer_View/FeatureServer/0`): **194,099 rows**, `ACCSTATUS`, `BUSNAICSCD` (NAICS), `CLASSDESC`, `CATGRYNAME`, `OCCDESC`, `BUSNAME`, `LAT`/`LON`, `FOLIO` (parcel), `MUNBUSLOC` | `naics` (already built) | **Screened 2026-09-21, not yet a full Step 0.** Promising: real NAICS, real coordinates, parcel IDs for the residence check, and `MUNBUSLOC` to cut county-wide data down to "01 - MIAMI". Needs the category distribution, the in-city count and a licence read. Privacy flag: `OWNERNAME` is present and some `BUSNAME` values are people ("LEON RAUL APRN") |
| - | New Orleans | RTA streetcars (5 lines, dense in the core) | "Active Occupational Licenses" (Socrata `iqay-p646`, `data.nola.gov`): 16,396 rows, `businesstype`, `businessname`, `businessaddress`, `the_geom`. Also `abc4-h3u3` (20,956 application-workflow rows, has `naics`, `category`, `ishome`) and `hjcd-grvu` (37,902) | new module needed (`businesstype`) | **Screened 2026-09-21, not yet a full Step 0.** `iqay-p646` carries the cleanest licence of any candidate — **CC0 1.0**, explicitly declared. Rail is streetcar-only, which is a scope question rather than a data one. Privacy flags: `ownername` and `businessphone` columns, and the name fields are **inverted on some rows** (blank `businessname` with the trade name in `ownername`), the same trap as Boston |
| - | Kansas City | KC Streetcar only (~1 line) | "KCMO Business License Holders" (Socrata `kkhs-93m4`): 15,895 rows, `business_type` (readable NAICS-style: Beauty Salons 662, Barber Shops 146, Clothing Retailers 192, Supermarkets 154), `location`, `business_name`, `dba_name` | `naics`-like, new module | **Screened 2026-09-21. Good data, too little rail.** Licence is explicitly **PUBLIC_DOMAIN**, and all three buckets are clearly present — the best data-to-effort ratio found. But the rail is one short streetcar line, well below the bar the other cities set, so it is recommended for exclusion on **rail**, not data. Revisit if the streetcar network expands. Watch: `dba_name` is often a person ("HARRIS GREGORY J"), and `business_type` includes fee codes ("Flat Rate 16", "Misc Rate 129") rather than activities |

## Ruled out

| City | Reason |
|---|---|
| San Jose | No bulk business-tax dataset on either official portal (CKAN `data.sanjoseca.gov`, ArcGIS `gisdata-csj.opendata.arcgis.com`). The only source found, `opendatasanjose.com`, is a third-party lookup tool with no export. |
| Fort Worth | Live-verified 2026-09-18. Data is workable but rail is not: TEXRail plus the Trinity Railway Express, both small (their GTFS not checked). Certificates of Occupancy (ArcGIS `CFW_Open_Data_Certificates_of_Occupancy_Table_view`, table 0): 72,065 rows since ~2002 with `Occupant`, `JobUse` (48 values), `Latitude`/`Longitude`, and current through 2026. But 13,343 rows (~19%) have no coordinates, city and address fields are null on most rows, and it is a running history of certificates (a relocated business appears more than once). Revisit if rail expands or a thin-network map is acceptable. |
| Austin | Live-verified 2026-09-18. The dataset titled "Certificates Of Occupancy" (Socrata `f9mz-m6dy`, 291,759 rows) is construction permits with a yes/no flag: no business name or classification. The business sets found are small (Active Credit Access Business Licenses `3buj-7jze`, 64 rows; vendor lists). Rail is one MetroRail line (from memory, not checked). |
| Charlotte | Live-verified 2026-09-18. The city hub (`data.charlottenc.gov`) holds zoning, permit-review and planning layers plus hand-curated point sets (grocery stores, pharmacies, medical facilities) and no general business or license dataset; Mecklenburg County's GIS open-data page listed none either. Rail is the LYNX Blue Line plus a streetcar (from memory, not checked). |
| Denver | "Active Business Licenses" (Denver ArcGIS hub and its Colorado Information Marketplace mirror) has no address, no classification and no geometry: only `License_Num, License_Type, License_Sub_Type, License_Status, Entity_Name, Trade_Name, Expiration_Date`. All 347 datasets in Denver's catalog were searched for an alternative; none qualified. |
| **Dallas** | **Ruled out 2026-09-21 on currency, not schema** — a different reason from the caveat recorded on 2026-09-18, and the schema itself was fine. Its only source with a classification, a business name and coordinates, Certificates of Occupancy (`9qet-qt9e`, PDDL, 23,731 rows, `land_use`), is **frozen**: `date_issued` runs 2018-01-02 to **2022-11-15** and the rows last changed 2022-11-16. `ync5-xnfn`, the "Commercial Permits Activity Dashboard" that `PLAN.md` said to check for something fresher, is **not a dataset** — it returns HTTP 403 "no row or column access to non-tabular tables" and reports 0 columns. The fresher food file (`dri5-wcct`) is named "October 2016 to January 2024", declares **no licence**, has no business-name column, and is also stale. Of 1,087 assets on the domain, nothing business-classified is current. Texas requires no general city business licence, so the certificate of occupancy *is* Dallas's registry — and it stopped. Putting a 4-year-old snapshot beside six current cities is a worse comparability problem than any thinness. |
| Houston | Live-screened 2026-09-21. **Zero** ArcGIS Online results for a Houston business licence or certificate-of-occupancy dataset, and no Socrata domain. Same structural cause as Dallas: Texas has no general city business licence. |
| Kansas City | **Not a data failure — a rail failure.** "KCMO Business License Holders" (`kkhs-93m4`) is explicitly PUBLIC_DOMAIN, 15,895 rows, geocoded, with all three buckets in readable categories. But the rail is a single short streetcar line, well under the bar every built city meets. Kept in the viable table above with this reasoning; revisit if the streetcar network expands. |

Revisit San Jose and Denver only if a new source appears. Dallas needs its
certificate-of-occupancy feed to resume publishing, which is a change on the
city's side rather than a new source to find.

## Screened and not found, which is NOT the same as verified absent

Live-screened 2026-09-21 in a **shallow** pass — Socrata's cross-domain
discovery API, then an ArcGIS Online title search. Nothing usable surfaced for:
**Atlanta, Baltimore** (liquor licences only), **Portland OR, Phoenix,
Minneapolis, St. Louis, Cleveland, Pittsburgh, Detroit, Jersey City, Tucson,
Sacramento, Salt Lake City, Honolulu, Buffalo** (contractor licences only, no
locations).

Read that list carefully. Twelve of those domains returned **HTTP 404 from
Socrata's discovery API, which means "not a Socrata domain" — not "no data"**,
and the ArcGIS pass searched dataset *titles* only. Seattle is the warning:
it returned "no matching datasets" on Socrata and then turned out to have an
official 54,604-row active business-licence layer on ArcGIS. So these cities
are **unscreened at depth**, not disqualified, and none of them should be
written off on the strength of this pass. That is the Denver and San Jose
lesson pointing the other way: a shallow check is as unreliable for ruling a
city *out* as it is for ruling one *in*.

## Screened out on rail (search-level, not live-verified)

Houston (minimal light rail; no general city business license), Phoenix
(two light-rail lines; no general city business license), San Antonio (no
rail), Columbus (no rail), Oklahoma City and El Paso (streetcar only),
Nashville (one commuter line), Indianapolis (bus rapid transit only),
Jacksonville (a 2.5-mile people mover), Las Vegas (a short private
monorail).

## Not yet live-verified

None. Dallas, Austin, Charlotte and Fort Worth were verified live on
2026-09-18 (see the tables above). The search-level guess that Dallas's
Certificates of Occupancy lacked a classification field was wrong: it has
`land_use`. Still unchecked: Dallas's Commercial Permits Activity Dashboard
(Socrata `ync5-xnfn`), and the GTFS feeds for Trinity Metro, Austin and
Charlotte.

## Philadelphia - Step 0 findings (2026-09-21)

Probed live against the Carto SQL API before writing any pipeline code.

**Easier than `PLAN.md` assumed.** It recorded "needs Carto queries and WKB
parsing"; no WKB parsing is needed. `the_geom` is populated on **all** 118,535
active licences, and the Carto SQL API evaluates PostGIS server-side, so
`SELECT ST_X(the_geom) AS lon, ST_Y(the_geom) AS lat` returns plain
coordinates. There is also a `geocode_x`/`geocode_y` pair (state plane) on
116,243 of them, which is not needed.

**Harder than assumed on categories, and in the way New York was.**
`licensetype` is activity-specific permits, not a general business register:

- **79% of active licences are `Rental`** - 93,471 residential landlord
  registrations. Not businesses, and not storefronts.
- Food service is well covered: ~9,059 across five types (`Food Preparing and
  Serving`, `... (30+ SEATS)`, `Food Establishment, Retail Permanent
  Location`, `... Non-Permanent`, `... (Large)`).
- **General retail and personal services are essentially absent** from the top
  30 types. There is no "retail store" or "salon/barber" licence. The nearest
  are `Tire Dealer` (83), `Precious Metal Dealer` (78), `Vendor - Newsstand`
  (75).

So Philadelphia is either a food-service-dominated map or a multi-source city
like New York. That decision comes before any build.

**RESOLVED 2026-09-21: neither.** The full 50-type pull and a source hunt for
each missing bucket settled it:

- **Multi-source was attempted and failed.** Every archetype in the
  `multi-source-city` skill was checked live and none works here — PA's
  professional-licensee file is county aggregates with no addresses, PA
  Agriculture's food inspections just relay the city's own, the Commercial
  Activity License file has **zero** geometry and no classification, and
  `li_business_licenses` is a stale copy of the same table. All four are
  recorded in `data_sources.md` so the search is not repeated.
- **It is not food-dominated either, because of a distinction the top-30 view
  hid.** Philadelphia separates `Food Preparing and Serving` (restaurants) from
  `Food Establishment, Retail` (shops that sell food) — the grocery slice New
  York needed a whole state registry for is already in this one file. And
  `Food Establishment, Retail Perm Location (Large)` turned out to be the
  general-retail tier: Target, CVS, Dollar Tree, **Staples, Ross Dress For
  Less**, which hold a food licence because they sell packaged food.

Final shape: **one registry, two buckets** — Food service 7,485 and Retail
1,715 of 9,200 downloaded rows, collapsing to 8,512 sites. Personal services
has no source at all, which is stated on the city page and in
`excluded_categories.md` under what is *missing* rather than *excluded*.

Two corrections to record, both cases of a licence type's name being
misleading:

- **`Vendor - Motor Vehicle Sales` is not car dealers.** It licenses vending
  *from* a vehicle; sampled holders are "CHA CHA LUNCH TRUCK", "FOOD TRUCK
  COLLECTIVE LLC". Mobile, so excluded.
- **"100% geometry" was wrong.** The Step 0 probe counted `the_geom IS NOT
  NULL`, but 218 rows hold an *empty* point geometry on which `ST_X` returns
  NULL. Real usable-coordinate rate is 97.6%, and the 2.4% loss is not uniform
  — it takes 61 of the 75 newsstands, 60 of which have no street address
  either, so geocoding cannot recover them.

**Excluding `Rental` is a privacy fix as well as a scope fix** - the same
shape as the national NAICS 454 exclusion. `business_name` is never blank
(0 of 118,535), but on rental licences it holds the *owner's own name*:
sampled rows returned "ROY E EGNER", "PETER MIRABELLI", "HOA THUY QUACH" at
their property addresses, with `legalentitytype = 'Individual'`. Mapping
active licences unfiltered would publish ~93k individuals at their addresses.

**A better privacy signal than any other city has so far:**
`legalentitytype` distinguishes `Individual` from corporate entities
structurally, so the person-like-name heuristic is a cross-check here rather
than the primary measure. Worth wiring into
`scripts/check_personal_exposure.py` for this city.

~~Still to do before building: the full `SELECT DISTINCT licensetype` pull, a
bucket mapping, the SEPTA GTFS feed, and a city boundary layer.~~ **All done
2026-09-21.** The SEPTA feed is a zip of zips whose *bus* member holds the
subway, el and trolleys (the "rail" one is Regional Rail); the boundary is
OpenDataPhilly's City Limits. Both are recorded in `data_sources.md`.
