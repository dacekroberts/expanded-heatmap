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
| 6 | Philadelphia | SEPTA Metro + Regional Rail | L&I Business Licenses (Carto SQL API `phl.carto.com`, table `business_licenses`): 435,143 rows, 118,535 Active, 48 fields | `phl_licensetype` (skeleton) | **Step 0 done 2026-09-21, see notes below.** Easier than expected on geometry, harder on categories |
| - | Boston | MBTA (subway, Green Line, commuter rail) | **Not just the certified directory** - `data.boston.gov` also has "Licensing Board Licenses" (CSV/XLSX), "Active Food Establishment Licenses" (CSV), "Annual Entertainment Licenses", "Food Establishment Inspections" | TBD | **Re-probed 2026-09-21 and no longer ruled thin.** The 978-row certified-vendor set is NOT the only option; real licence registries exist. Needs a proper Step 0 on those (coverage of Retail / Personal services, and whether they carry coordinates) |
| - | Dallas | DART light rail (GTFS downloads, HTTP 200) | Building Inspection Certificates of Occupancy (Socrata `9qet-qt9e`, `dallasopendata.com`): `business_name`, `address`, `land_use` (143 values), `occupancy`, `geolocation` (2 of 23,731 rows null) | new module needed (`land_use`) | **Caveat:** the data ends 2022-11-15 and holds only certificates issued 2018-2022 (~4-5.6k a year), so it shows new occupancies, not a registry. A city page would need that stated. Other Dallas CO sets are archived FY2015-17 copies |
| - | Washington D.C. | WMATA Metrorail, 6 lines, 98 stations | Basic Business Licenses (`maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/DCRA/FeatureServer/0`): `PREMISEADDRESS`, `BUSINESSACTIVITY`, `CATEGORYSERVICETYPE` | new module needed | **Caveat:** no NAICS field, and `LATITUDE`/`LONGITUDE` are truncated to whole degrees (use address geocoding or the state-plane `X_COORDINATE`/`Y_COORDINATE`) |

## Ruled out

| City | Reason |
|---|---|
| San Jose | No bulk business-tax dataset on either official portal (CKAN `data.sanjoseca.gov`, ArcGIS `gisdata-csj.opendata.arcgis.com`). The only source found, `opendatasanjose.com`, is a third-party lookup tool with no export. |
| Fort Worth | Live-verified 2026-09-18. Data is workable but rail is not: TEXRail plus the Trinity Railway Express, both small (their GTFS not checked). Certificates of Occupancy (ArcGIS `CFW_Open_Data_Certificates_of_Occupancy_Table_view`, table 0): 72,065 rows since ~2002 with `Occupant`, `JobUse` (48 values), `Latitude`/`Longitude`, and current through 2026. But 13,343 rows (~19%) have no coordinates, city and address fields are null on most rows, and it is a running history of certificates (a relocated business appears more than once). Revisit if rail expands or a thin-network map is acceptable. |
| Austin | Live-verified 2026-09-18. The dataset titled "Certificates Of Occupancy" (Socrata `f9mz-m6dy`, 291,759 rows) is construction permits with a yes/no flag: no business name or classification. The business sets found are small (Active Credit Access Business Licenses `3buj-7jze`, 64 rows; vendor lists). Rail is one MetroRail line (from memory, not checked). |
| Charlotte | Live-verified 2026-09-18. The city hub (`data.charlottenc.gov`) holds zoning, permit-review and planning layers plus hand-curated point sets (grocery stores, pharmacies, medical facilities) and no general business or license dataset; Mecklenburg County's GIS open-data page listed none either. Rail is the LYNX Blue Line plus a streetcar (from memory, not checked). |
| Denver | "Active Business Licenses" (Denver ArcGIS hub and its Colorado Information Marketplace mirror) has no address, no classification and no geometry: only `License_Num, License_Type, License_Sub_Type, License_Status, Entity_Name, Trade_Name, Expiration_Date`. All 347 datasets in Denver's catalog were searched for an alternative; none qualified. |

Revisit San Jose and Denver only if a new source appears.

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

Still to do before building: the full `SELECT DISTINCT licensetype` pull, a
bucket mapping, the SEPTA GTFS feed, and a city boundary layer.
