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
| 4 | Chicago | CTA 'L' (145 stations, 8 lines) + Metra | Business Licenses (Socrata `r5kz-chrr`): address, `latitude`/`longitude` | `chicago_license` (skeleton) | Needs `license_description` distinct-value pull. No NAICS field exists on the portal |
| 5 | New York | Subway (472 stations) + LIRR/Metro-North | DCA Issued Licenses (Socrata `w7w3-xahh`): address, `latitude`/`longitude` | `nyc_dca` (skeleton) | Needs `business_category` distinct-value pull. Largest system - biggest station-scope decision |
| 6 | Philadelphia | SEPTA Metro + Regional Rail | L&I Business Licenses (Carto SQL API `phl.carto.com`, table `business_licenses`): address, `the_geom` (WKB), `geocode_x`/`geocode_y` | `phl_licensetype` (skeleton) | Needs `licensetype` pull, plus Carto queries and WKB parsing |
| - | Boston | MBTA (subway, Green Line, commuter rail) | Certified Business Directory (CKAN, `data.boston.gov`): `naics_codes1`, address | `naics` | **Caveat:** 978 rows of certified vendors only, not a general registry. Decide whether that is enough data |
| - | Washington D.C. | WMATA Metrorail, 6 lines, 98 stations | Basic Business Licenses (`maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/DCRA/FeatureServer/0`): `PREMISEADDRESS`, `BUSINESSACTIVITY`, `CATEGORYSERVICETYPE` | new module needed | **Caveat:** no NAICS field, and `LATITUDE`/`LONGITUDE` are truncated to whole degrees (use address geocoding or the state-plane `X_COORDINATE`/`Y_COORDINATE`) |

## Ruled out on data

| City | Reason |
|---|---|
| San Jose | No bulk business-tax dataset on either official portal (CKAN `data.sanjoseca.gov`, ArcGIS `gisdata-csj.opendata.arcgis.com`). The only source found, `opendatasanjose.com`, is a third-party lookup tool with no export. |
| Denver | "Active Business Licenses" (Denver ArcGIS hub and its Colorado Information Marketplace mirror) has no address, no classification and no geometry: only `License_Num, License_Type, License_Sub_Type, License_Status, Entity_Name, Trade_Name, Expiration_Date`. All 347 datasets in Denver's catalog were searched for an alternative; none qualified. |

Revisit either only if a new source appears.

## Screened out on rail (search-level, not live-verified)

Houston (minimal light rail; no general city business license), Phoenix
(two light-rail lines; no general city business license), San Antonio (no
rail), Columbus (no rail), Oklahoma City and El Paso (streetcar only),
Nashville (one commuter line), Indianapolis (bus rapid transit only),
Jacksonville (a 2.5-mile people mover), Las Vegas (a short private
monorail).

## Not yet live-verified

Dallas (extensive rail; its Certificates of Occupancy dataset appears to
lack a classification field), Austin (one commuter line, light rail
planned), Charlotte (light rail plus streetcar; no single countywide
license dataset found), and Fort Worth (one commuter line) scored
medium-or-below on search results only. They are candidates for a later
pass, verified live first.
