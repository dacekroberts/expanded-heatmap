# Data sources — United States

<!-- internal -->Part of [`data_sources.md`](../data_sources.md), the project's provenance
record, split by country on 2026-09-27: this file holds the United States rows
of its tables and the sections about this country's sources. The numbered
notices this project must display, the removal-request commitment and the
deploy gate are in the main file, not here.<!-- /internal -->

## Business registries

| City | Source | Provides | Endpoint | Filter at download | Retrieved |
|---|---|---|---|---|---|
| San Diego | City Business Tax Certificates | All three buckets, via NAICS | `https://seshat.datasd.org/business_tax_certificates/` (`sd_businesses_active_datasd.csv`) | none (whole file) | 2026-09-18 |
| San Diego | **SanGIS countywide tax parcels** (hosted by SANDAG) (ArcGIS FeatureServer, 1,089,758 polygons) | Not businesses — **joined** to the above for the residence check. San Diego was recorded as the city with NO residence signal, on a 0.03% reading that was a MEASUREMENT GAP rather than a clean result; `ownerocc` is `Y` on 472,498 parcels and is the genuine owner-occupancy flag it was thought to lack | `https://geo.sandag.org/server/rest/services/Hosted/Parcels/FeatureServer/0/query` | **One buffered query PER PERSON-LIKE PIN, not a bulk download** — `where=1=1`, a point `geometry` with `distance` in meters, `outFields=apn,asr_landuse,ownerocc`, `returnGeometry=false` and **`returnCentroid=true`**, then the nearest centroid is chosen locally. Only pins whose displayed name reads as a person's are queried (2,463 of them): the filter cannot fire on anything else and this is a shared public service. **The bulk alternative was tried and abandoned** — `orderByFields` forces a sort over 664,662 rows and `resultOffset` deep-pages at ~26 s per 2,000-row page, about two hours — so `PARCEL_QUERY_BBOX` and `PARCEL_PAGE_SIZE` survive in `config.py` as dead constants that no script reads. **Nearest, not containing:** these coordinates sit 5-15 m outside their own parcel because they are placed at the street frontage and SanGIS parcels exclude road right-of-way, so on 30 sampled pins an exact point-in-parcel test matched 1 and a 25 m buffer matched 30. `asr_landuse` has no published coded-value domain, so `11` = single-family detached was established empirically; `17` = condominium is deliberately excluded, as a unit in a shared building may be ground-floor retail | 2026-09-21 |
| San Francisco | DataSF Registered Business Locations (Socrata `g8m3-pdis`) | All three buckets, via NAICS | `https://data.sf.gov/resource/g8m3-pdis.csv` | San Francisco only | ≈2026-09-19 |
| San Francisco | **Assessor Historical Secured Property Tax Rolls** (Socrata `wv5m-vpq2`) | Not businesses — **joined** to the above for the residence check. 217 pins (1.19%) displayed a person's name at a parcel the Assessor calls Single Family Residential *and* claiming a homeowner's exemption, California's homestead analogue, granted only on an owner-occupied primary residence | `https://data.sf.gov/resource/wv5m-vpq2.csv` | `$where=closed_roll_year = '2025' AND the_geom IS NOT NULL`, `$select=block, lot, use_definition, number_of_units, homeowner_exemption_value, the_geom`, `$limit=400000`. **`the_geom` is a POINT per parcel, and selecting it is what makes this a SPATIAL join rather than an address one** — an address join reaches only 43.8%, because `property_location` is a fixed-width composite (`'0000 2801 LEAVENWORTH         ST0000'`) and stripping direction words destroys "North Point" and "South Van Ness" on both sides. 43.8% is not enough to filter on: it would remove home businesses only where the address text happened to match, which is arbitrary but looks complete. Nearest-parcel tolerance 40 m (93.4% matched, median 1.4 m). **"Multi-Family Residential" is deliberately NOT treated as residential** although it is the largest category under this city's pins (5,733) — San Francisco puts ground-floor retail in residential buildings. Same host rule as the boundary layer: `data.sf.gov`, never `data.sfgov.org`, which 403s on `/resource/` | 2026-09-21 |
| Los Angeles (Regional) | Listing of Active Businesses (Socrata `6rrh-rzua`) | All three buckets, via NAICS | `https://data.lacity.org/resource/6rrh-rzua.csv` | `$where=location_1 IS NOT NULL`, selected columns, `$order=location_account` | ≈2026-09-19 |
| Los Angeles (Regional) | **LA County Assessor parcels** (ArcGIS MapServer, 92 fields) | Not businesses — **joined** to the above for the residence check. A 400-point sample put **7.2%** of this city's person-like pins on a Residential parcel claiming a homeowner's exemption — roughly 1,000-2,000 pins, **the largest such exposure in the project** | `https://public.gis.lacounty.gov/public/rest/services/LACounty_Cache/LACounty_Parcel/MapServer/0/query` | One query per person-like pin: `f=json`, point `geometry` with `inSR=4326`, `spatialRel=esriSpatialRelIntersects`, and `outFields=UseType,UseDescription,Roll_HomeOwnersExemp` — three fields of the 92. **Containing parcel first, 25 m buffer only as a fallback** for points inside no parcel at all: an exact point-in-parcel test matches only ~49% of these pins, because the 9% of LA coordinates recovered by Census geocoding sit on street centrelines. Filtering on the unbuffered 49% would have been San Francisco's 43.8% mistake. **Owner names are absent by law** (Cal. Gov. Code §7928.205), so there is nothing here to publish by accident — a structural privacy position rather than a column omission | 2026-09-21 |
| Los Angeles (Regional) | City of Long Beach **Business Licenses Public View** (MapsLB; ArcGIS item 54d45ca9c4554062a02df49ec1ea2b2a, refreshed nightly from the City's licensing system) | All three buckets in Long Beach, via the City's own license categories (`pipeline/taxonomies/los_angeles.py`; chair, booth and practitioner licenses out) | `https://services6.arcgis.com/yCArG7wGXGyWLqav/arcgis/rest/services/Business_Licenses_Public_View/FeatureServer/0/query`, paged at 2,000 | `LICSTATUS='Active' AND OUTSIDECITY='No' AND HOMEBASED='No'` (20,204) and an **explicit `outFields`**: ⚠️ `FULLNAME` (the license holder's name) is never requested, and fetch and step 2 both assert it. 4,078 in the buckets -> 3,264 one per license -> **3,246 inside the City of Long Beach** (18 placeholder points in the Pacific dropped). 520 with no trade name show the street address. License: the MapsLB Terms of Use, PERMITTED WITH CONDITIONS - never suggest the City's endorsement; the breach-only indemnity accepted (owner, 2026-09-30); notice 129 | 2026-10-03 |
| Chicago | Business Licenses (Socrata `r5kz-chrr`) | All three buckets, via its own license taxonomy | `https://data.cityofchicago.org/resource/r5kz-chrr.csv` | `license_status='AAI' AND expiration_date >= '2026-09-20'`, `$order=id` | 2026-09-20 |
| Washington D.C. | **Basic Business License** (DCRA/DLCP, ArcGIS FeatureServer) | **All three buckets, via its own `BUSINESSACTIVITY` taxonomy** — the first non-NAICS source here that covers all three on its own | `https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/DCRA/FeatureServer/0/query` (`outSR` not needed — `returnGeometry=false`, `orderByFields=OBJECTID ASC`, paged at 2,000) | `LICENSESTATUS='Active' AND PREMISEINDC='Yes' AND BUSINESSACTIVITY NOT IN (<the five residential rental types>)`, and an explicit 16-column `outFields` list that omits every owner/agent name and the billing address | 2026-09-21 |
| New York | DOHMH Restaurant Inspection Results (Socrata `43nn-pn8j`) | **Food service** | `https://data.cityofnewyork.us/resource/43nn-pn8j.csv` | selected columns, `$limit=500000` (unfiltered: it is an inspection history, collapsed to one row per establishment in step 2) | 2026-09-21 |
| New York | NYS Retail Food Stores (Socrata `9a8c-vfzj`, data.ny.gov) | **Retail** — grocery, bodegas, delis, supermarkets | `https://data.ny.gov/resource/9a8c-vfzj.csv` | `county in('KINGS','QUEENS','BRONX','NEW YORK','RICHMOND')` | 2026-09-21 |
| New York | NYS Active Appearance Enhancement & Barber *Business* Licensees (Socrata `y3u4-jbgh`, data.ny.gov) | **Personal services** — salons, nail, skin care, barbers | `https://data.ny.gov/resource/y3u4-jbgh.csv` | selected columns; **`license_holder_name` deliberately not selected** (it is an individual's name) | 2026-09-21 |
| New York | DCWP Issued Licenses (Socrata `w7w3-xahh`) | **Retail**, a narrow regulated slice | `https://data.cityofnewyork.us/resource/w7w3-xahh.csv` | `license_status='Active' AND license_type='Premises'` | 2026-09-21 |
| Philadelphia | L&I Business Licenses (Carto SQL API, table `business_licenses`) | **Food service** and **Retail** only — see below | `https://phl.carto.com/api/v2/sql` (`format=csv`) | `licensestatus='Active' AND licensetype IN (…13 types…)`, built from `config.KEPT_LICENSETYPES`; selected columns, **no registrant-name column** (`legalfirstname`, `legallastname`, `legalname`, `opa_owner`, `ownercontact*name` are all deliberately unselected and asserted absent in step 2) | 2026-09-21 |
| Philadelphia | OPA Property Assessments (Carto SQL API, table `opa_properties_public`, 583,779 rows) | Not businesses — **joined** to the above for the residence check | `https://phl.carto.com/api/v2/sql` (`format=csv`) — the same endpoint as the license data | `LEFT JOIN opa_properties_public p ON b.opa_account_num = p.parcel_number`, which matches 94% of licenses. Only two derived values are selected — the City's own `category_code_description` land-use category and a boolean for whether a homestead exemption is claimed. The exemption AMOUNT is not downloaded and no mailing address is downloaded at all | 2026-09-21 |
| Philadelphia | **OpenStreetMap** node 5372090220 (11th Street station, `railway=station`, network SEPTA) - a SUPPORT source<!-- internal --> (CLAUDE.md `[#support-sources]`)<!-- /internal --> | Not businesses - one station's coordinate, for the L's 11th St, which SEPTA closed for works from 2026-09-05 to 2027-08-30 (SEPTA news, 2026-08-06) and which SEPTA's feed therefore no longer carries. Not drawn: the position only places its row in the stations left out, listed on the city's page<!-- internal --> (docs/category_rules.md, "Station scope")<!-- /internal --> | read once through Nominatim (`nominatim.openstreetmap.org/search`), copied into `config.CLOSED_FOR_WORKS`; never fetched by a step | the one node; step 1 exits once the feed's L stops there again. OpenStreetMap, ODbL 1.0 - notice 1, already displayed | 2026-10-01 |
| Miami | Miami-Dade County **Local Business Tax** (ArcGIS FeatureServer, 194,099 rows, all `YEAR`=2026) | All three buckets, via the county's own `CATGRYNAME` (150 values). **Its `BUSNAICSCD` column is NULL on all 194,099 rows**, so NAICS is unavailable despite being in the schema | `https://services.arcgis.com/8Pc9XBTAsYuxx9Ny/arcgis/rest/services/Local_Business_Tax_Feature_Layer_View/FeatureServer/0/query` | `ACCSTATUS='Active'` (175,982 rows), selected columns, `orderByFields=OBJECTID` for stable deep paging. **`OWNERNAME` and every `MAIL*` column are deliberately NOT downloaded** — `OWNERNAME` is populated on 100% of rows and is frequently a person; step 2 asserts all eight stay absent | 2026-09-21 |
| Boston | Food Establishment Inspections (CKAN resource `4582bec6-2b4f-4f9e-bc55-cbaa73117f4c`, 902,651 rows) | **Food service** (`FS`, `FT`) and **Retail** (`RF`) — see below | `https://data.boston.gov/api/3/action/datastore_search_sql` | `licstatus='Active'`, **collapsed to one row per `property_id` + `licensecat` in SQL** with `GROUP BY`, so the download is ~2,900 rows rather than ~900,000. `legalowner`, `namelast` and `namefirst` exist in this table and are deliberately NOT selected; step 2 asserts they and five more stay absent | 2026-09-21 |
| Boston | Licensing Board Licenses (CKAN resource `04dc653b-1789-4374-9669-b07df7233344`, 3,587 rows) | **Retail** — package stores only | same endpoint | `status='Active' AND (license_type LIKE 'Retail%' OR license_type = 'Druggist')` → 307 rows. Its 2,578 Common Victualler licenses are the same restaurants as the ISD source and are excluded to avoid double-counting. Coordinates are `gpsx`/`gpsy` in **EPSG:2249** (state plane, US survey feet), reprojected in step 2 — not lat/lon. `applicant`, `manager`, `day_phone` and `evening_phone` are NOT selected | 2026-09-21 |
| Boston | Cannabis Active Licenses (CKAN resource `e395fd88-0f81-4399-a57a-3e94a74b145c`, 43 rows) | **Retail** — dispensaries | same endpoint | `status='Active'`; same `gpsx`/`gpsy` convention as the Licensing Board set. The one `Delivery (operator)` row is excluded — no shopfront | 2026-09-21 |
| Boston — **recorded, deliberately NOT used** | Business Inventory (CKAN resource `47bd8208-f648-4309-8f65-de7416d63157`, 2,634 rows) | Would cover **all three buckets**, and is the only Boston source that reaches Personal services | same endpoint | — | 2026-09-21 |
| Buffalo | City of Buffalo **Business Licenses** (Socrata `qcyy-feh8`, data.buffalony.gov, 12,131 rows) | **Food service**, a regulated **Retail** slice and laundries, by `descript` (`pipeline/taxonomies/buffalo.py`) | `https://data.buffalony.gov/resource/qcyy-feh8.csv` | explicit `$select` (no person column exists), the 15 storefront `descript` codes. ⚠️ **`licstatus` is Active on every row**, so step 2 keeps `expdttm >= 2026-09-29` (Chicago's rule): 1,564 of 2,737. ⚠️ `businessname` is the trade name and `dbaname` usually the legal entity, the reverse of the dataset's own column notes (DOLLAR GENERAL STORE #14886 / DOLGENCORP OF NEW YORK INC); businessname is displayed (owner). Caterer (23) and Sidewalk Cafe (137) downloaded but never a pin. License: public domain on the portal's own statement - see below | 2026-09-29 |
| Buffalo | NYS Retail Food Stores (`9a8c-vfzj`), New York's row | **Retail** - grocery | `https://data.ny.gov/resource/9a8c-vfzj.csv` | `upper(city)='BUFFALO'`: 596 rows, 584 with a point, **422 inside the city** by point-in-boundary. 186 of the City's grocery licenses at the same house number and street merged into these rows. No date column; rows last updated 2025-09-30 | 2026-09-29 |
| Buffalo | NYS Appearance Enhancement & Barber *Business* Licensees (`y3u4-jbgh`), New York's row | **Personal services** | `https://data.ny.gov/resource/y3u4-jbgh.csv` | `upper(business_city)='BUFFALO'`, `license_holder_name` never selected: 440 rows, renters (65) and 3 at an apartment unit dropped, **277 inside the city**. 42 names that read as a person's show the license type (owner, 2026-09-29) | 2026-09-29 |
| Sacramento | City of Sacramento **Business Operation Tax Information** (ArcGIS table `account_data_with_header_NEW`, item f4ee567a…, 63,904 rows, **no geometry**) | All three buckets, via the City's own `Business_Description` (`pipeline/taxonomies/sacramento.py`<!-- internal -->, hand-mapped on docs/category_rules.md<!-- /internal -->) | `https://services5.arcgis.com/54falWtcpty3V47Z/arcgis/rest/services/account_data_with_header_NEW/FeatureServer/0/query`, paged at 2,000 | `Current_License_Status = 'Active'` (24,040) and an **explicit `outFields`**: ⚠️ `Principal_Owner_*`, `Primary_Phone_number` and every `Mail_*` are never requested, and fetch and step 2 both assert it. Step 2 keeps `Current_Expire_Date >= 2026-09-29` (2,768 Active rows had expired) and `Location_City = SACRAMENTO` (4,935 "ON FILE" withheld). 3,534 storefront premises -> Census geocoder 98.0% -> **3,335 inside the city** by point-in-boundary (125 Sacramento postal addresses outside it). 525 names that read as a person's show the description (owner). License: the City's Open Data Terms, indemnity accepted (owner) - see `data_sources.md` | 2026-09-29 |
| Sacramento | **US Census Bureau batch geocoder** (`pipeline/census_geocoder.py`), Los Angeles' and D.C.'s module | Not businesses - the storefronts' coordinates: 3,465 of 3,534 matched (3,298 Exact) | `https://geocoding.geo.census.gov/geocoder/locations/addressbatch`, benchmark Public_AR_Current | street, city, state and ZIP only - never a name; cached by batch hash under `data/sacramento/raw/geocode_cache/`. The City's All Addresses layer was NOT used: no terms cover it (owner). Federal, public domain | 2026-09-29 |
| Sacramento | **Wikidata** item Q107175168 (Dos Rios station) - a SUPPORT source<!-- internal --> (CLAUDE.md `[#support-sources]`)<!-- /internal --> | Not businesses - one station's coordinate (P625), for a Blue Line station SacRT opened 2026-09-28 that OpenStreetMap has not mapped (owner: "Wikidata for now, replace with OSM when we can") | `https://www.wikidata.org/wiki/Special:EntityData/Q107175168.json` | the one item; step 1 exits once OSM's Blue relations carry the station. **CC0 1.0** (Wikidata's structured data): nothing to display | 2026-09-29 |
| Houston | Texas Comptroller **Active Sales Tax Permit Holders** (Socrata `jrea-zgmq`, data.texas.gov, 888,178 outlets statewide, updated 2026-09-26, **no geometry**) | All three buckets, by `outlet_naics_code` (the shared NAICS module) | `https://data.texas.gov/resource/jrea-zgmq.json`, paged at 50,000 | `upper(outlet_city)='HOUSTON' AND outlet_inside_outside_city_limits_indicator='Y'` (79,097) and an **explicit `$select`**: ⚠️ `taxpayer_name`, `taxpayer_address` and **`taxpayer_number`** (for an individual, built from their Social Security number) are never requested, and fetch and step 2 both assert it; only `outlet_*` and `taxpayer_organization_type`. `outlet_naics_code` is a NUMBER column. 33,613 in the buckets -> 32,025 premises -> **29,912 placed inside the city**. A person's permit (IS, PI, ES) shows its address; one at a Residential point is left off (owner) | 2026-09-29 |
| Dallas | Texas Comptroller **Active Sales Tax Permit Holders** (Socrata `jrea-zgmq`, Houston's register, **no geometry**) | Retail and Food service; Personal services thin (a sales-tax permit is held by sellers of taxable goods and services; owner, 2026-09-30: narrowed, as Houston) | `https://data.texas.gov/resource/jrea-zgmq.json`, paged at 50,000 | `upper(outlet_city)='DALLAS' AND outlet_inside_outside_city_limits_indicator='Y'` (44,760) and Houston's **explicit `$select`**: ⚠️ `taxpayer_name`, `taxpayer_address` and **`taxpayer_number`** are never requested, and fetch and step 2 both assert it. 18,275 in the buckets -> 17,049 premises -> **15,885 placed inside the city**. A person's permit (IS, PI) shows its address | 2026-09-30 |
| Houston | City of Houston **Site Addresses** (COHGIS, `Export_SiteAddresses.zip`, ArcGIS item 82f3487741d84516ae6f64680474344a, layer `SiteAddresses_20251112`, 1,547,147 points, EPSG:2278) - a SUPPORT source<!-- internal --> (CLAUDE.md `[#support-sources]`)<!-- /internal --> | Not businesses - the storefronts' coordinates by address join: 26,877 of 32,025 (83.9%), and the `addrtype` that marks a Residential point | `https://mycity.houstontx.gov/mycitydocs/download/Export_SiteAddresses.zip` (166 MB file geodatabase, Last-Modified 2025-11-12) | the street as filed with its unit cut, within its ZIP, then a canonical form, then a street address unique across ZIPs. **Public domain** (COHGIS Hub: "COHGIS data is in the public domain and may be copied without permission"; license read 2026-09-29<!-- internal -->, the brief<!-- /internal -->); courtesy credit "City of Houston Planning & Development", nothing required | 2026-09-29 |
| Dallas | City of Dallas **Address Points** (Development Services GIS, layer 0 "Main Address", 395,893 points) - a SUPPORT source<!-- internal --> (CLAUDE.md `[#support-sources]`)<!-- /internal --> | Not businesses - the storefronts' coordinates by address join: 15,081 of 17,049 exactly or in canonical form (88.5%), 225 at the nearest listed number on the same side within 10 | `https://services2.arcgis.com/rwnOSbfKSwyTBcwN/arcgis/rest/services/AddressPoints/FeatureServer/0/query`, paged at 2,000 (the layer's limit), WGS84 asked of the server; only HOUSENUMBER, HOUSESUFFIX, FULLSTREETNAME, ZIPCODE and ADDRESSTYPE read (its type codes undocumented, so not used) | Houston's passes plus the nearest-number tier. **License: silent on reuse; the City's GIS disclaimer's open-ended indemnity ACCEPTED by the owner (2026-09-30)** (`docs/data_sources.md`, "Dallas's indemnity"); optional credit "City of Dallas Development Services GIS"; never call the pins surveyed or exact | 2026-09-30 |
| Houston | **US Census Bureau batch geocoder** (`pipeline/census_geocoder.py`) | Not businesses - the join's residue: 3,979 of 5,148 matched | `https://geocoding.geo.census.gov/geocoder/locations/addressbatch`, benchmark Public_AR_Current | street, city, state and ZIP only - never a name; cached by batch hash under `data/houston/raw/geocode_cache/`. Federal, public domain | 2026-09-29 |
| Minneapolis | City of Minneapolis **Food Inspections** (ArcGIS item `4eea8bf452e34f8c9d9ac07c54c0b4ab`, `Food_Inspections` FeatureServer layer 0, owner City_of_Minneapolis; 47,959 rows, one per violation, 2023-01-03 to 2026-09-18, 2,916 facilities) | Food service (RESTAURANT) and food shops (GROCERY, MEAT MARKET, MARKET, LIQOFFSALE) by `FacilityCategory`, with a name test inside them (`pipeline/taxonomies/minneapolis_inspection.py`); no personal services | `https://services.arcgis.com/afSMGVsC7QlRK1kZ/arcgis/rest/services/Food_Inspections/FeatureServer/0/query`, paged at 16,000 by OBJECTID | `where=1=1` and **named fields only**: ⚠️ `InspectorComments`, `FoodCodeText` (inspectors' free text) and `APN` are never requested. One facility per `HealthFacilityIDNumber`, from its latest inspection; inspected within two years (2,861); 1,793 placed inside the city | 2026-09-30 |
| Pittsburgh | Allegheny County Health Department **Geocoded Food Facilities (as of 2025)** on WPRDC (package `allegheny-county-restaurant-food-facility-inspection-violations`, resource `112a3821-334d-4f3f-ab40-4de1220b1a0a`, last modified 2025-08-27; 32,245 facilities county-wide, one row each, `x`/`y` in WGS84) | Food service (201, 202, 211, 212) and food-selling shops (111-118: supermarkets, retail/convenience, packaged food, bakeries) by `category_cd`, with a name test inside them (`pipeline/taxonomies/pittsburgh_inspection.py`); no personal services | `https://data.wprdc.org/datastore/dump/112a3821-334d-4f3f-ab40-4de1220b1a0a` | `municipal` Pittsburgh-NNN (11,144) and **active = `status` 1 with no `bus_cl_date`** (3,204): the resource's own description, "1 indicates that the facility is active and 7 indicates that the facility is out of business" (its data dictionary's text values - Active, Complete, Pending, Expired - do not match the numbers; the resource note is the specific one). Named columns only; the file has no person column. 1,730 placed inside the city | 2026-09-30 |
| Seattle (Regional) | City of Seattle **Business Locations (Active)** (ArcGIS `Seattle_Business_License` layer 0, owner SeattleData: a nightly export of Finance & Administrative Services' license database; 54,689 rows on 2026-10-02, every one ACTIVE and with a point) | All three buckets in Seattle, by `BUSLIC_NAICS_CODE` (the shared NAICS module) | `https://services.arcgis.com/ZOyb2t4B0UYuYNYH/arcgis/rest/services/Seattle_Business_License/FeatureServer/0`, paged by objectid | named fields only: ⚠️ `BUSLIC_CONTACT_NAME`, `BUSLIC_PHONE_NUM`, `BUSLIC_MAIL_ADRS_TEXT` and `BUSLIC_LEGAL_NAME` are never requested, and step 2 asserts it. A second request, `where=BUSLIC_TRADE_NAME = BUSLIC_LEGAL_NAME`, returns location ids only (20,519): such a trade name that reads as a person's shows its category (90). 1,246 exact duplicate rows dropped, one row per location at its latest license, 988 outside the city by point-in-polygon dropped. Every license year kept; a lapsed food row (2025 or earlier) only where King County inspected a business of the same trade name in 2025 or 2026, a street match alone not enough (owner; 331 dropped). The head-office rule dropped 1. **9,198 storefronts** | 2026-10-02 |
| Seattle (Regional) | City of Bellevue **Business Licenses (All)** (ArcGIS layer 3, 82,155 rows, refreshed daily; licenses never expire) | Retail and Personal services in Bellevue, by `Naic` (NAICS); Bellevue's food comes from King County's inspections (owner) | `https://services1.arcgis.com/EYzEZbDhXZjURPbP/arcgis/rest/services/Business_Licenses_(All)/FeatureServer/3`, paged by OBJECTID | named fields only: ⚠️ `LegalEntityName`, `Ubi` and every `Mailing*` field are never requested. Not cancelled on 2026-10-02 (24,566), inside the city (12,593), in the two buckets (1,819), **issued 2010-01-01 or later** (the owner's cutoff; 322 dropped). A row with no trade name (260), or a sole proprietor's trade name that reads as a person's (50), shows its category. **1,415 storefronts** | 2026-10-02 |
| Seattle (Regional) | Public Health – Seattle & King County **Food Establishment Inspection Data** (Socrata `r878-4sxa`, data.kingcounty.gov; 109,078 rows, one per inspection and violation, 2021-01-04 to 2026-10-01, 12,305 businesses) | Food service, and food shops as Retail (grocery stores, meat and fish markets, bakeries), in every King County city; in Seattle, the inspected businesses the license register lacks by trade name and street address | `https://data.kingcounty.gov/resource/r878-4sxa.csv` | explicit `$select` (no violation text). One business per `business_id`, inspected in 2025 or 2026 (12,130). Out by class: mobile units, school lunch programs, catering operations, nonprofit institutions, commissaries, donated-food distributors, bed and breakfasts. Out by name: workplace cafeterias and contract caterers (499), hotel kitchens (146), vending routes (62), members' clubs, theaters and airline lounges (36), pharmacies (9). Placed by parcel through King County's address points: 99.1%. **3,245 storefronts** | 2026-10-02 |
| Seattle (Regional) | King County **Address Points** (`ADDRESS_POINT_642`, 674,254 points) - a SUPPORT source | Not businesses - the food inspections' businesses placed by parcel (`PIN`), and the Liquor Board's King County premises by street address; Pinehurst station at its street address | `https://services.arcgis.com/Ej0PsM5Aw677QF1W/arcgis/rest/services/ADDRESS_POINT_642/FeatureServer/0`, paged by OBJECTID | the geometry and the County's own fields only (`PIN`, `ADDR_*`, `PRIM_ADDR`, `SITETYPE`). ⚠️ `CTYNAME`, `POSTALCTYNAME` and the ZIP fields come from the USPS ZIP+4 product and are never requested (owner). Food placement: 9,372 on the parcel at the business's own address, 2,455 at the parcel's primary point, 196 by an address naming one place, 107 unplaced | 2026-10-02 |
| Seattle (Regional) | Snohomish County **Food Service Establishments (2025)** (ArcGIS item `75bf161b46ba484a97e6d7f1c63f21a4`, 3,699 permits at 3,131 facilities; static, its data no newer than 2025-11-19) | Food service and grocers in Lynnwood and Mountlake Terrace, by `Icon` (Restaurant, Grocery) | `https://services6.arcgis.com/z6WYi9VRHfgwgtyW/arcgis/rest/services/Food_Service_Establishments/FeatureServer/0` | named fields only (none of the layer's waste-hauler fields). Restaurant and Grocery points only: school kitchens, donated-food distributors, food trucks, catering, vending and concessions out (owner). Cities by the layer's jurisdiction field `User_Fld`, never the postal city, and the 32 whose field is blank by the place their point falls in (owner): Lynnwood 329 and Mountlake Terrace 70 facilities, and unincorporated county inside Lynnwood City Center's ring. One row per facility; a store holding grocery and deli permits is a grocer. The same name layer as King County's. **382 storefronts** | 2026-10-02 |
| Seattle (Regional) | Snohomish County **Building Address Points** (SnocoGIS E911 addressing; 73,836 points in the Lynnwood and Mountlake Terrace box) - a SUPPORT source | Not businesses - the Liquor Board's Snohomish premises placed by street address | `https://services6.arcgis.com/z6WYi9VRHfgwgtyW/arcgis/rest/services/Building_Address_Points/FeatureServer/0`, bounded to `47.76,-122.36,47.87,-122.24` | the geometry and the address fields only | 2026-10-02 |
| Seattle (Regional) | Washington State Liquor and Cannabis Board **Off Premise** licensee list (XLSX dated 2026-09-29, from the Board's frequently requested lists; 8,793 privilege rows statewide) | Retail outside Seattle and Bellevue: **shops licensed to sell alcohol only** (grocery stores, spirits retailers, beer and wine specialty shops) | `https://lcb.wa.gov/sites/default/files/2026-09/Off%20Premise09292026.xlsx` | ⚠️ `Licensee`, `ID Number`, `Phone` and the four mailing columns are never read, and step 2 asserts it. King and Snohomish County premises, license ACTIVE (ISSUED) with a current privilege; wine-reseller and gift-delivery privileges out; one row per premises (1,837). Placed by street address on the county address points, never geocoded: 1,409 placed (King County 96.0%). The Board's own note: these list reports "contain possible errors due to a known data transfer issue". **191 storefronts** after a grocer at the same address in a food register is counted once | 2026-10-02 |
| Dallas | **US Census Bureau batch geocoder** (`pipeline/census_geocoder.py`) | Not businesses - the join's residue: 1,349 of 1,743 matched, 579 of them inside the city | `https://geocoding.geo.census.gov/geocoder/locations/addressbatch`, benchmark Public_AR_Current | street, city, state and ZIP only - never a name; cached by batch hash under `data/dallas/raw/geocode_cache/`. Federal, public domain | 2026-09-30 |
| Kansas City | KCMO **Business License Holders** (Socrata `kkhs-93m4`, data.kcmo.org, 15,895 licenses, `rowsUpdatedAt` 1768519845 = **2026-01-15, frozen**; a `location` point on every row) | All three buckets, by NAICS 2022 **title** in `business_type`, mapped to its code through the Census title file (row below) and then the shared NAICS module | `https://data.kcmo.org/resource/kkhs-93m4.json`, one page, explicit `$select`; `https://data.kcmo.org/api/views/kkhs-93m4.json` read first, and fetch stops if the license is no longer Public Domain or `rowsUpdatedAt` has moved | every row; step 2 keeps `valid_license_for` 2025 and 2026 (13,917; owner), drops 1,095 fee-code types (owner), maps 615 titles (one truncated, "Freight Transportation Arrangemen", by unique prefix) -> 3,612 in the buckets -> 3,601 inside the city (TIGER) -> **3,561 premises**. **`dba_name` is the license HOLDER, `business_name` the trade name** (measured 2026-09-30<!-- internal -->, against the brief's reading<!-- /internal -->): a person-held license, or a company named only as a person, shows its address (710) | 2026-09-30 |
| Kansas City | US Census Bureau **2022 NAICS titles** (`2-6 digit_2022_Codes.xlsx`) - a SUPPORT source<!-- internal --> (CLAUDE.md `[#support-sources]`)<!-- /internal --> | Not businesses - the title-to-code map for `business_type` | `https://www.census.gov/naics/2022NAICS/2-6%20digit_2022_Codes.xlsx` (82,460 bytes) | titles compared on letters and digits (the register drops commas; the file marks trilateral titles with a trailing T); the 6-digit code where a 5- and 6-digit code share a title. A US federal government work, public domain; nothing required | 2026-09-30 |
| Tucson | City of Tucson **BUSLIC**, "All current, active business licenses" (ArcGIS MapServer `PublicMaps/OpenData_EconomicDevelopment/MapServer/3`, gis.tucsonaz.gov; **never layer 1**, `ZZ_CPV_BUSLIC`, a different table), 93,483 rows, 34,764 active, rebuilt by a daily batch job (newest `DT_START` 2026-09-12<!-- internal --> at the brief<!-- /internal -->) | All three buckets, by `NAIC_CODE` (the shared NAICS module, unchanged) | `https://gis.tucsonaz.gov/arcgis/rest/services/PublicMaps/OpenData_EconomicDevelopment/MapServer/3/query`, paged at the layer's 2,000, `outSR=4326`, an explicit field list | `LIC_STATUS = 'Active' AND HOME_OCCUPATION = 'F'` (24,191) -> 7,120 in the buckets -> 6,581 geocoded -> 6,558 inside the city (TIGER) -> 6,539 not at an apartment -> **5,243 premises**. `ACC_NAME` withheld (the address shown) for OWN_TYPE Sole Proprietorship, Individual and Married (owner) and for 45 names read as a person's | 2026-09-30 |
| Tacoma | City of Tacoma **"Business Licenses - Map (Tacoma)"** (ArcGIS item `2fa3b14b4de44c16b44893fee2cadefd`, the POINT layer `BusinessLicenses_Map/FeatureServer/0`, data.tacoma.gov; **never the table item** `8efa2724e88a44a286894d33cb5fb331`, the same rows without geometry), "Directory of businesses with an active Tacoma Tax & License business account", 22,128 rows, refreshed daily (last edited 2026-10-02) | All three buckets, by `naics_code` (NAICS 2022, the shared NAICS module, unchanged) | `https://services3.arcgis.com/SCwJH1pD8WSn5T5y/arcgis/rest/services/BusinessLicenses_Map/FeatureServer/0/query`, paged at 2,000, `outSR=4326`, an explicit field list that leaves every `mailing_*` field out (never fetched) | every row; step 2 keeps `council_district` 1-5, the register's in-city marker (11,812) -> 2,931 in the buckets -> 2,931 inside the city (TIGER) -> 2,870 not at an apartment, trailer or mobile-home space -> **2,851 premises**. Where the trade name is only the entity's own name, the entity carries no legal form and the name reads as a person's, the pin shows the NAICS description (104; Vancouver's rule) | 2026-10-04 |
| New Orleans | City of New Orleans **Active Occupational Licenses** (Socrata `iqay-p646`, data.nola.gov, 16,521 licenses, updated daily; a point on every row, 0,0 where ungeocoded) | All three buckets, by `businesstype` - the City's own text taxonomy, 486 values, each mapped to the NAICS code its title names (`pipeline/taxonomies/nola_businesstype.py`) | `https://data.nola.gov/resource/iqay-p646.json`, explicit `$select`; `https://data.nola.gov/api/views/iqay-p646.json` read first (fetch stops if the license is no longer CC0) | every row; ⚠️ `ownername` and `businessphone` are never requested, and fetch and step 2 both assert it. 4,970 in the buckets -> 4,751 placed -> 4,750 inside the city (TIGER) -> **4,689 premises**; 808 show the address (no business name, or a person's) | 2026-09-30 |

The Philadelphia parcel join exists to answer one privacy question the address
text cannot: **is this "business" someone's home?** It selects only the two
derived values in the row above (Philadelphia grants a homestead exemption only
on an owner's primary residence), and neither is ever published: the rendered
map emits only name, category, station and ring. Same "City of Philadelphia
License" as the license data, recorded below.

New York needs four sources because it has **no general business license**.
Most cities here need one.

Philadelphia is the opposite lesson: a **multi-source hunt that came back
empty**, which is why it maps two of the three business categories from one
registry rather than all three from several. Each kind of second source was
checked live on 2026-09-21 and failed, and each is recorded here so it is not
checked again from scratch:

| Candidate for Philadelphia's missing buckets | Why it is unusable |
|---|---|
| PA Professional Licensee Data (Socrata `fwj2-whnj`, data.pa.gov) | Aggregate `active_count` **by county**, with no addresses. Pennsylvania does not publish licensee locations; the State Board of Cosmetology's PALS system is a per-license lookup with no bulk export |
| PA Agriculture food inspections (Socrata `etb6-jzdg`, data.pa.gov) | Does reach Philadelphia, but `organization_name` is "City of Philadelphia" — it relays the city's own inspections, so it duplicates the registry above rather than adding to it |
| Philadelphia Commercial Activity Licenses (Carto `com_act_licenses`) | The general license every city business needs, and unusable on three counts: **0 of 528,413 active rows have geometry**, there is no business address at all (only the owner's *mailing* address), and `licensetype` is the single value "Activity" with no classification. It also carries `legalfirstname`/`legallastname` |
| Carto `li_business_licenses` | A **stale copy** of the registry above — 360,192 rows vs 435,143, "Towing" where the current table says "Tow Truck", and missing `unit_type`. Not a second source |

A text search for hair / barber / salon / nail / cosmet / massage / tattoo /
laundry across both Carto license tables returns nothing, so **Personal
services has no source in Philadelphia at all**. The What Is Excluded page
records that as *missing* rather than *excluded*.

<!-- internal -->
### Boston — Step 0 findings, 2026-09-21

Probed before Boston was built (it has since been built from the sources
above). Four things here are worth not rediscovering.

**Boston licenses food, and almost nothing else.** Inspectional Services
licenses food; the Licensing Board licenses alcohol, lodging, billiards and
bowling. There is no general business license and no personal-service license.
Deduplicated to premises: **Food service 2,237**, **Retail 385** unambiguous
(`RF`-only), plus 306 package stores and 43 cannabis shops that *overlap* the
`RF` set — "Go Fresh 365 / Ming's Supermarket" holds both an `RF` license and a
`Retail All Alc.` license at 1102 Washington St, so cross-source dedup is
mandatory rather than optional.

**The official "Active Food Establishment Licenses" extract silently drops a
category, so do not use it.** Resource `f1e13724-284d-478c-b8bc-ef042aa5b70b`
(3,345 rows) is exactly `FS` 1,762 + `FT` 1,583 licenses and contains no `RF`
(Retail Food) at all — which would make Boston a one-bucket city. The
902,651-row inspections history carries the same `licensecat` field, including
`RF`'s 504 active premises, and has better coordinates: **99.9%** of active
premises carry a usable `location` versus 93.8% in the extract. There are no
*corrupt* coordinates in either, unlike Los Angeles' ~9% — the only bad rows
are honest NULLs.

**`dbaname` is blank on 99.0% of the food rows and `businessname` is never
blank and holds the trade name** — the reverse of every other city's
convention. A step 2 that prefers the `dba` column, as every built city's does,
would get almost nothing here. (The Licensing Board sets use the normal
convention: `dba_name` is the trade name, `business_name` the legal entity.)

| Candidate for Boston's missing Personal services | Why it is unusable |
|---|---|
| Massachusetts Board of Registration of Cosmetology and Barbering | The state licenses salons, barbershops and manicuring shops, and publishes **no address-bearing export**. Its register is the ePLACE / MADOL portal (`occupationallicensingandpermitting.mass.gov/madol/s/license-search-page`), a per-license lookup with no bulk download — the same shape as San Jose's rejected third-party tool and Pennsylvania's PALS |
| Any Socrata-hosted Massachusetts dataset | Checked via Socrata's cross-domain discovery API (`api.us.socrata.com/api/catalog/v1`) for cosmetology / barber / salon / hair / nail salon / body art / tattoo. **No Massachusetts source appears for any of them**; the only MA domains indexed at all are `educationtocareer.data.mass.gov` and `cthru.data.socrata.com` (state spending). New York's equivalent (`y3u4-jbgh`) has no Massachusetts counterpart |
| `data.mass.gov` as a portal | Not a data portal. Both the Socrata (`/api/views/metadata/v1`) and CKAN (`/api/3/action/package_list`) entry points return an HTML 404; `opendata.mass.gov` does not resolve |
| Boston "Certified Business Directory" (979 rows) | The source the shortlist originally recorded, and correctly ruled out: a **vendor certification** directory (MBE/WBE/veteran), not a storefront list. Its addresses are regional rather than in-city (the first sampled row is in Milton), and it carries `contact_name`, `phone`, `fax` and `email` — personal contact details this project strips |

**The one source that would cover all three buckets is a partial survey.**
`Business Inventory` is a summer-2025 field census with exactly this project's
taxonomy — `Beauty_Services` 243 (Hair_Salon 101, Barber_Shop 46, Nail_Salon
32), plus Clothing_Store, Jewelry_Store, Laundry, Tailor — with WGS84
`x_coord`/`y_coord` on 99.8% of rows and even a `vacant` flag. Its own notes
give the limit: "every storefront in downtown Boston, as well as comprehensive
data on 3 major commercial corridors in Mattapan, Jamaica Plain, and Allston."
Measured: 37 occupied 0.01° cells, 18 ZIPs, and 14 rows in **Brookline**, a
different municipality. A heat surface built on it would show where surveyors
walked rather than where commerce is, so it is recorded as available and
deliberately unused. Its license is also the only "not specified" one on the
portal.
<!-- /internal -->

## Transit feeds

| City | Agency / system | Endpoint | Retrieved | Note |
|---|---|---|---|---|
| San Diego | MTS Trolley | `https://www.sdmts.com/google_transit_files/google_transit.zip` | 2026-09-18 | |
| San Francisco | SFMTA Muni Metro | `https://muni-gtfs.apps.sfmta.com/data/muni_gtfs-current.zip` | ≈2026-09-19 | **Mirror.** The official host (`sfmta.com/reports/gtfs-transit-data`) timed out from this environment; this URL is linked from the agency's own page |
| Los Angeles (Regional) | LA Metro Rail | `https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip` | ≈2026-09-19 | Metro's rail-only feed |
| Chicago | CTA | `https://www.transitchicago.com/downloads/sch_data/google_transit.zip` | 2026-09-20 | |
| New York | MTA subway + Staten Island Railway | `https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip` | 2026-09-21 | The `web.mta.info/developers/data/nyct/subway/google_transit.zip` path is **dead** |
| Boston | MBTA rapid transit | `https://cdn.mbta.com/MBTA_GTFS.zip` | 2026-09-21 | 24.9 MB, 32 files. Drawn: `Red`, `Orange`, `Blue`, `Mattapan` and `Green-B`/`-C`/`-D`/`-E` as five line groups; the 14 `CR-*` Regional Rail routes and the ferries are not. `feed_info.txt` declares **no license field at all**, so the terms are the MassDOT agreement — which requires a notice, now ACTIVE. Branching lines need several shapes each (Red splits to Ashmont and Braintree; Green is four branches), and `parent_station` is populated so platforms collapse cleanly |
| Washington D.C. | WMATA Metrorail | `https://api.wmata.com/gtfs/rail-gtfs-static.zip` | 2026-09-21 | **The only feed in this project behind an API key** — 401 unauthenticated. Free developer account at `developer.wmata.com`, subscribe to the **GTFS** product, key sent as an `api_key` header. Take the **`Rail GTFS Static`** operation, *not* `Rail & Bus Combined GTFS Static` (bus routes this project never draws) and not any `RT` feed. Verified 2026-09-21: 6 routes (Red, Blue, Green, Yellow, Orange, Silver, all `route_type 1`, `network_id Metrorail`), **98 parent stations, all with coordinates**, 270,784 `stop_times` rows, 340 shape_ids, no bus contamination. **`feed_info.txt` declares `feed_start_date 20260915`, `feed_end_date 20260925` — a ten-day validity window, the shortest of any feed here, so a rebuild must re-download rather than reuse a stored copy.** Terms are the WMATA Transit Data Terms of Use, stored at `docs/licenses/wmata-transit-data-terms-of-use.html`; the key is WMATA's property, must stay out of the repo, and cannot be sold, transferred or sublicensed (§5). **Built 2026-09-21.** `fetch_sources.py` reads the key from a `WMATA_API_KEY` environment variable, never echoes it (not even in the 401 message), and re-checks `feed_end_date` on EVERY run including runs that skip the download — an expired copy is an error, not a warning, because a stale feed still parses, still has 98 stations and still builds a map. Shape selection needed care this feed alone required: WMATA publishes 26-101 shapes per route, so "the most-used shape" could be a short turn (the Yellow Line's second-most-used stops at Mt Vernon Square, nine stations short of Greenbelt). Each drawn shape is the most-used among those serving the route's full stop count |
| Miami | Miami-Dade Transit (Metrorail + Metromover) | `https://www.miamidade.gov/transit/googletransit/current/google_transit.zip` | 2026-09-21 | 8.4 MB. **Note the host**: `transitdata.miamidade.gov` does not resolve; this URL is also the one the Mobility Database lists as official. Four rail routes; three are drawn (`31009` Metrorail, `14457`/`14456` the Metromover loops) and the MIA Airport People Mover `14458` is not. **No `feed_info.txt` at all**, so no license is declared in the feed. Metrorail publishes NINE shapes because the line branches, and has **no `parent_station`** — its 46 stop_ids are 23 stations x 2 directions |
| Philadelphia | SEPTA Metro | `https://github.com/septadev/GTFS/releases/latest/download/gtfs_public.zip` | 2026-09-21 | **A zip of zips.** Contains `google_bus.zip` and `google_rail.zip`; `fetch_sources.py` extracts the **bus** one, because SEPTA's City Transit Division — and therefore the Market-Frankford Line, Broad Street Line and every trolley — is in that feed, not the "rail" one. `google_rail.zip` is Regional Rail, which this project does not draw. The naming is not guessable; both route tables were read to establish it |
| Buffalo | **OpenStreetMap** - NFTA Metro Rail, relations 3517747 and 11364343 (`route=light_rail`, network NFTA, ref Metro, `#004990`) | The Overpass mirrors in `pipeline/osm.py`, bbox `42.82,-78.95,42.97,-78.79`, `out geom` and `node(r)` | 2026-09-29 | **Why not the agency: NFTA's rail GTFS is current** (`metro.nfta.com/__googletransit/rail/google_transit.zip`, 26FALL, 2026-08-27 to 2026-12-05) **and is not fetched**: its license bars NFTA marks "in association with the Data", and the invariant's permanent "NFTA Metro Rail" label beside NFTA's own Data would be that use if NFTA claims the name (owner, 2026-09-29). 28 stop positions -> 14 stations by name, **gate 3 exact** against the feed's 14<!-- internal --> (read by the brief)<!-- /internal -->, 608 m median gap, all inside the city. Line drawn from track ways only (each relation also lists 6 `platform` ways). OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| Sacramento | **OpenStreetMap** - SacRT light rail, Blue (2378981, 2378982) and Gold (2352701, 2352702); Green (2379220, 2379221) read but **not drawn** | The Overpass mirrors in `pipeline/osm.py`, bbox `38.45,-121.58,38.72,-121.10`, `out geom` and `node(r)` | 2026-09-29 | **Why not the agency**: SacRT's GTFS host (`apps.sacrt.com`) serves an expired certificate, and SSL is never bypassed; SacRT's data license also carries NFTA's trademark clause. **Green Line suspended** since 2025-06-16 (Railyards works), reopening expected mid-October 2026 (sacrt.com/greenline): not drawn, 7th & Richards/Township 9 recorded as closed for works<!-- internal --> (docs/category_rules.md, "Station scope")<!-- /internal -->. **OSM lags SacRT on Blue twice**: two stop nodes unnamed (Morrison Creek, named from config) and Dos Rios (opened 2026-09-28) unmapped (placed from Wikidata); both retire themselves. Three downtown couplets merged (owner). **Gate 3 exact** against SacRT's own timetables: Blue 28, Gold 27. 37 stations inside the city, 796 m median. OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| Houston | **OpenStreetMap** - METRORail Red (1741729, 12356338), Green (2728566, 12356337), Purple (2728567, 12356336), `route=light_rail`, network `Metro` | The Overpass mirrors in `pipeline/osm.py`, bbox `29.60,-95.50,29.90,-95.25`, `out geom` and `node(r)` | 2026-09-29 | **Why not the agency**: METRO's static feed is governed by a Data Use Agreement (May 2025) demanding a verbatim credit, a trademark legend at every "METRO", an unlimited indemnity and 24-hour compliance with any demand<!-- internal --> (the brief)<!-- /internal -->; rail from OSM (owner, 2026-09-29), and the feed is never fetched. Labels "Red Line", "Green Line", "Purple Line" (owner); colors chosen through `linecolour.py`, not METRO's. 80 stop positions -> **40 stations, gate 3 exact** (Red 25, Green 9, Purple 10), 659 m median; Central Station's Capitol / Rusk couplet merged by alias. OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| Minneapolis | **OpenStreetMap** - METRO Blue Line (2440419, 2440420, ref `901`) and Green Line (3817120, 3817130, ref `902`), `route=light_rail`, operator `Metro Transit` | The Overpass mirrors in `pipeline/osm.py`, bbox `44.80,-93.40,45.10,-93.05`, `out geom` and `node(r)` | 2026-09-30 | **Why not the agency**: Metro Transit's GTFS license is unread; rail from OSM, the owner's choice for Buffalo and Houston applied again. Labels "METRO Blue Line", "METRO Green Line"; OSM's colors #0000ff and #008144 kept. 76 stop positions -> **37 stations, gate 3 exact** (Blue 19, Green 23, Wikipedia; Metro Transit's pages state no count); "US Bank Stadium" folded into "U.S. Bank Stadium" by alias. **15 inside the city** (Blue 11, Green 9), 661 m median; the other 22 listed on the city's page with their municipality (St. Paul 14, Bloomington 4, Fort Snelling Unorganized Territory 4). The box's `tram` relation 6736496 is the Minnesota Streetcar Museum's Como-Harriet heritage line, not drawn. OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| Pittsburgh | **OpenStreetMap** - PRT Red (7574878, 7574879, 7575523, 7575524: the Overbrook short working and the full run), Blue (7575515, 7575517) and Silver (7572383, 7572384), `route=light_rail`, network `Pittsburgh Regional Transit` (the Red relations' operator tag says "PRT") | The Overpass mirrors in `pipeline/osm.py`, bbox `40.28,-80.15,40.50,-79.90`, `out geom` and `node(r)` | 2026-09-30 | **Why not the agency**: PRT's GTFS license is unread; rail from OSM, the owner's choice for Buffalo, Houston and Minneapolis applied again. Labels "PRT Red Line", "PRT Blue Line", "PRT Silver Line"; OSM's colors, except Blue moved from #77b6e4 to #59bcde (ΔE 37.8 from the Retail pins). 102 stop positions -> **51 stations, gate 3 exact** (Red 31, Blue 24, Silver 31, Wikipedia). **20 inside the city** (Red 15, Blue 13, Silver 13), 452 m median, so the halved rings; the other 31 listed on the city's page with their municipality (Bethel Park 17, Castle Shannon 7, Dormont 3, Mount Lebanon 3, South Park 1). OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| Seattle (Regional) | **OpenStreetMap** - Link 1 Line (3494092, 5517060) and 2 Line (17499739, 17499740), `route=light_rail`, network `Link`, refs `1 Line` and `2 Line`; **not drawn**: the Seattle Streetcar (4748655, 4748656, 4755830, 4755831) and the airport's SEA Underground (6495673, 6495674, 6495675, 10077846) | The Overpass mirrors in `pipeline/osm.py`, bbox `47.28,-122.42,47.84,-122.08`, `out geom` and `node(r)` | 2026-10-02 | **Why not the agency: Sound Transit's rail GTFS is current** (SC-Fall-2026.3, 2026-09-01 to 2027-03-26) **and is not used**: its Transit Data Terms add a "No Changes" clause, a duty to pass the terms on, an open indemnity, registration by email and usage metrics on request (owner, 2026-10-02). Labels "1 Line" and "2 Line"; Sound Transit's colors moved just clear of the pins (#46C831, #00B6DF). 76 stop positions -> 38 stations by name; **Pinehurst** (opened 2026-09-30, not yet in the relations) placed at King County's address point for the address on Sound Transit's station page. **39 stations, gate 3 exact** against Sound Transit's 1 Line and 2 Line pages (27 and 26), 1,350 m median, all in the 11 station cities. OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| Dallas | **OpenStreetMap** - DART Light Rail Red, Blue, Green and Orange (27 relations), `route=light_rail`, network `DART` | The Overpass mirrors in `pipeline/osm.py`, bbox `32.62,-96.98,33.02,-96.55`, `out geom` and `node(r)` | 2026-09-30 | DART's GTFS is not read: Houston's route (owner). Not drawn (owner, 2026-09-30): the Dallas Streetcar (`tram`, ref 620) and the M-Line heritage trolley (`tram`, MATA); the Silver Line and the TRE are commuter rail, outside the query. Labels "Red Line", "Blue Line", "Green Line", "Orange Line"; colors the project's own (Houston's Red and Green). 128 stop positions -> 64 stations, **44 inside the city**; **gate 3 exact** against Wikipedia's line infoboxes less Convention Center (closed, role `inactive` in OSM) and Hidden Ridge (Irving, not yet in OSM): Red 25, Blue 22, Green 24, Orange 30. OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| Kansas City | **OpenStreetMap** - KC Streetcar, `route=tram` relations 7825409 and 7825410, ref 601 (operator "Kansas City Streetcar Authority", network RideKC) | The Overpass mirrors in `pipeline/osm.py`, bbox `39.02,-94.62,39.13,-94.54`, `out geom`, the relations' nodes and every `railway=tram_stop` in the box; re-fetched on every `fetch_sources.py` run | 2026-09-30 | **Why not the agency**: RideKC's GTFS is barred (owner, 2026-09-30) - ridekc.org's site terms restrict schedules and require written consent to republish, with an open-ended indemnity<!-- internal --> (the brief)<!-- /internal -->. Label "KC Streetcar", the line's public name; no KC Streetcar or RideKC logo (the Authority claims the brand); color `#b8860b`, the project's own (OSM records none). 35 stop positions -> **19 stations** by `pipeline/osm_tram.py`, all inside the city, 384 m median; gate 3 not run (no operator count read). Frequency stated as a fact, never cited from a schedule. OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| Tucson | **OpenStreetMap** - Sun Link, `route=tram` relations 3920972 and 12426661, ref "Sun Link" | The Overpass mirrors in `pipeline/osm.py`, bbox `32.20,-110.99,32.25,-110.93`, `out geom`, the relations' nodes and every `railway=tram_stop` in the box; re-fetched on every `fetch_sources.py` run | 2026-09-30 | No agency feed used: <!-- internal -->the brief measured on OSM, and <!-- /internal -->Sun Link's GTFS is unread. Label "Sun Link"; color `#e65100`, the project's own (OSM records none; teal `#00838f` scored 42.3 against Personal services). 23 stop positions -> **21 stations** by `pipeline/osm_tram.py` (one-way couplets downtown, so each direction's stops keep their own names), all inside the city, 265 m median; gate 3 not run. Frequency<!-- internal --> (the brief's screen)<!-- /internal -->: every 10 minutes weekdays 07-18, every 20 otherwise, disclosed. OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| Tacoma | **OpenStreetMap** - the T Line, `route=tram` relations 5705256 and 5705257, ref "T Line" (operator Sound Transit, network Link, colour `#F38B00`) | The Overpass mirrors in `pipeline/osm.py`, bbox `47.22,-122.48,47.28,-122.41`, `out geom` on the box's tram and light-rail relations, their nodes and every `railway=tram_stop` in the box | 2026-10-04 | **Why not the agency**: Sound Transit's GTFS is not used (owner, 2026-10-02, for Seattle: its Transit Data Terms). Label "T Line", the line's public name, in OSM's orange `#F38B00` (77.9 from the nearest pin color); no Sound Transit logo. 22 stop positions -> **12 stations** by `pipeline/osm_tram.py`, all inside the city, 451 m median, so halved rings. Gate 3 exact against Sound Transit's own T Line page (12 stations, read 2026-10-04; it writes "S 25th" where OSM writes "S 25th St"). Frequency stated as a fact: every 12 minutes on weekdays from 7:00 to 20:00 and on Saturdays, every 20 minutes otherwise and on Sundays. OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |
| New Orleans | **OpenStreetMap** - RTA streetcars 12 (1809578, 12340017), 46 (19791963, 19791964), 47 (1809579, 12340016), 48 (1809580, 12340015), 49 (19790175); **not drawn**: ref 2 (1809582, 12340018), the Riverfront's old routing | The Overpass mirrors in `pipeline/osm.py`, bbox `29.90,-90.14,30.00,-90.03`, `out geom`, the relations' nodes and every `railway=tram_stop` in the box; re-fetched on every run | 2026-09-30 | RTA's GTFS unread and not used. **The lines are what RTA runs** (owner, 2026-09-30): its service-changes page (Fall '26 schedules) reopened 46 Rampart/UPT in Summer 2025 and moved the Riverfront to 49, French Market - Julia Street. 46 and 49 carry no stop members in OSM: 32 tagged RTA tram stops added by node (`config.STATION_ADD`), the riverfront's Poydras and Julia renamed "Riverfront at" (Loyola Avenue has its own); four one-stop-two-names pairs merged by alias. **Corrected to RTA's own stop lists** (gate 3, 2026-10-01): 47 and 48 run down Canal to the ferry terminal - ten more OSM `tram_stop` nodes there added by node (the Ferry Terminal is OSM's "Harrah's Casino", shown under RTA's name) and 47's Cemeteries node, four more pairs merged by alias (seven now); 47's Loyola stops moved to 46 and Canal at Basin / Elk Place, where no line RTA runs stops, dropped with its alias (`config.STOP_LINE_FIXES`), 47's Loyola ways not drawn (`config.LINE_WAYS_NOT_DRAWN`); S. Carrollton at Sycamore, which OSM does not map, placed at the vertex of each direction's OSM track way nearest RTA's pin (`config.TRACK_STOPS`). 202 stop positions -> **110 stations**, 186 m median, all inside. OSM's colors (12 `green`, 47 `red`, 48 `#90EE90`, 49 `#5C2E86`), 46 the project's `#b8860b`. OpenStreetMap, ODbL 1.0 - notice 1 and the rail-geometry notice |

## Boundary layers

| City | Layer | Endpoint | Filtered to |
|---|---|---|---|
| San Diego | **SanGIS** municipal boundaries (published by SanGIS; SANDAG only hosts the file on `geo.sandag.org`) | `https://geo.sandag.org/server/rest/directories/downloads/Municipal_Boundaries.geojson` | `SAN DIEGO` |
| San Francisco | Socrata "Bay Area County Polygons" (`wamw-vt4s`) | `https://data.sf.gov/resource/wamw-vt4s.geojson?$where=county='San Francisco'&$limit=10` | `San Francisco` |
| Los Angeles (Regional) | LA County Planning, incorporated cities | `https://services.arcgis.com/RmCCgQtiZLDCtblq/arcgis/rest/services/admin_dist_SDE_DIST_DRP_CITY_COMM_BDY/FeatureServer/0/query` (`JURISDICTION='INCORPORATED CITY'`, `outSR=4326`, `f=geojson`) | `LOS ANGELES` and `LONG BEACH` (the stations kept and the map's frame; Long Beach's outline also drops its layer's placeholder points) |
| Chicago | Socrata "Boundaries - City" (`qqq8-j68g`) | `https://data.cityofchicago.org/resource/qqq8-j68g.geojson?$limit=10` | whole city |
| New York | Borough Boundaries (`gthc-hcne`) | `https://data.cityofnewyork.us/resource/gthc-hcne.geojson?$limit=10` | all five boroughs = the city |
| Philadelphia | OpenDataPhilly "City Limits" (Dept of Planning and Development) | `https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/City_Limits/FeatureServer/0/query` (`where=1=1`, `outSR=4326`, `f=geojson`) | whole city (one polygon, 2,957 vertices) |
| Boston | **MassGIS Massachusetts Municipalities**, layer 1 ("Areas") — 351 town polygons statewide, with a `TOWN` field | `https://services1.arcgis.com/hGdibHYSPO59RG1h/arcgis/rest/services/Massachusetts_Municipalities/FeatureServer/1/query` (`outFields=TOWN`, `outSR=4326`, `f=geojson`) | a spatial **envelope** around the rapid-transit network rather than all 351 towns → 61 polygons. Used both to filter to `TOWN='BOSTON'` and to NAME the 43 out-of-town stations |
| Boston — **considered, not used** | "City of Boston Outline Boundary (Water Excluded)" | `https://data.boston.gov/dataset/a70595d2-fd38-4bcb-8a81-6f7807621d38/resource/dade0744-a486-44c7-be7d-07240a89dca4/download/city_of_boston_outline_boundary_water_excluded.geojson` | whole city, one polygon. Would filter but could not NAME the other towns, which is the bigger job here — see the note below |
| Washington D.C. | **DC Boundary**, layer 10 of the District's administrative-boundaries service — a single clean polygon | `https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Administrative_Other_Boundaries_WebMercator/MapServer/10/query` (`where=1=1`, `outFields=*`, `outSR=4326`, `f=geojson`) | whole District, one polygon. Used to filter: 40 of 98 Metrorail stations are inside it |
| Washington D.C. — **naming layer** | **Census TIGERweb states** — three polygons, so an excluded station can be NAMED and not merely counted | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/0/query` (`NAME IN ('Maryland','Virginia','District of Columbia')`, `outSR=4326`, `f=geojson`) | the three jurisdictions Metrorail runs through. 58 stations are outside the District — 32 Virginia, 26 Maryland — more than Los Angeles' 54 or San Diego's 16, which is why it has to be citable. Census TIGER products are US federal works and carry no copyright |
| Miami | Miami-Dade County **municipal boundaries** (same publisher as its business data) | `https://services.arcgis.com/8Pc9XBTAsYuxx9Ny/arcgis/rest/services/Municipalitypoly_gdb/FeatureServer/0/query` (`outFields=MUNICID,NAME`, `outSR=4326`, `f=geojson`) | **not filtered — used to NAME, not to exclude.** 77 polygons across 34 municipalities; `MUNICID` joins to the business file's `MUNBUSLOC` prefix |
| Buffalo | **Census TIGERweb place polygon**, current Incorporated Places, GEOID 3611000 ("Buffalo city") | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=GEOID='3611000'` | the city: 135.9 km², of which 31.3 km² is Lake Erie and Niagara River water, gated at 130-142. Scopes the two State files and checks the stations. A US federal government work, public domain (Washington D.C.'s TIGERweb row) |
| Buffalo - **recorded, deliberately NOT used** | Open Data Buffalo "City Boundary" (Socrata `p4ak-r4fg`), labeled "U.S. Census Bureau", "Public Domain U.S. Government" | `https://data.buffalony.gov/resource/p4ak-r4fg.geojson` | **Not a Census product** (license read 2026-09-29): its vertices sit on Erie County's municipal-boundary layer (median 0.0 m), it carries Erie's schema, and the City's GIS server hosts it as "Managed/Owned by Erie County". The City's public-domain dedication may not reach a County work and the County states no terms, so the owner took TIGER's clean title instead (2026-09-29) |
| Sacramento | **OpenStreetMap** city and county relations (admin_level 8 and 6) - City of Sacramento is relation 6232940 | The Overpass mirrors, the rail bbox, `out geom` - 11 relations | **the City**, 256.7 km², gated at 245-270. Scopes the stations AND the geocoded storefronts (the register's `Location_City` is a postal city); names the 14 stations outside it (Rancho Cordova, Folsom, unincorporated Sacramento County). OpenStreetMap, ODbL 1.0 - notice 1 |
| Houston | **Census TIGERweb place polygon**, current Incorporated Places, GEOID 4835000 ("Houston city") | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=GEOID='4835000'` | the city: 1,741.5 km² (land 1,659.7, water 80.9), gated at 1,700-1,780. Scopes the stations and the placed storefronts (the permits' city is a postal one). **Not OSM's relation 2688911**: it draws 1,589.5 km² and lacks 156 km² of TIGER's polygon in annexed pieces on the west and north edges (measured 2026-09-29). A US federal government work, public domain (Buffalo's and Washington D.C.'s TIGERweb rows) |
| Minneapolis | **Census TIGERweb place polygon**, current Incorporated Places, GEOID 2743000 ("Minneapolis city"); and TIGERweb **County Subdivisions** (layer 1) in the rail box, which name the municipality of each station outside the city | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=GEOID='2743000'`; `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/1/query` by envelope | the city: 148.8 km² (land 139.9, water 9.1), gated at 143-155. Scopes the stations and the placed storefronts. A US federal government work, public domain (Buffalo's and Houston's TIGERweb rows) |
| Pittsburgh | **Census TIGERweb place polygon**, current Incorporated Places, GEOID 4261000 ("Pittsburgh city"); and TIGERweb **County Subdivisions** (layer 1) in the rail box, naming each outside station's municipality | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=GEOID='4261000'`; `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/1/query` by envelope | the city: 151.0 km² (land 143.4, water 7.7), gated at 145-157. Scopes the stations, and with the County's `municipal` the placed storefronts. A US federal government work, public domain |
| Seattle (Regional) | King County **city polygons** (`CITY_KC_AREA_446`, 98 features with CITYNAME and JURIS) | `https://services.arcgis.com/Ej0PsM5Aw677QF1W/arcgis/rest/services/CITY_KC_AREA_446/FeatureServer/0/query?where=1=1` | every King County station city, Des Moines, Beaux Arts and unincorporated King County (CITYNAME "King County"): names each station's city and scopes every source by point-in-polygon. King County's GIS data, read as permitted with the food inspections (owner) |
| Seattle (Regional) | **Census TIGERweb place polygons**, current Incorporated Places, Lynnwood (GEOID 5340840) and Mountlake Terrace | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=STATE='53' AND BASENAME IN ('Lynnwood','Mountlake Terrace')` | the two Snohomish County station cities, outside King County's layer. The 0.34 km² of Lynnwood City Center's ring beyond the city is unincorporated Snohomish County. A US federal government work, public domain |
| Dallas | **Census TIGERweb place polygon**, current Incorporated Places, GEOID 4819000 ("Dallas city") | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=GEOID='4819000'` | the city: 993.8 km², gated at 950-1,050. Scopes the stations and the placed storefronts (the permits' city is a postal one: 770 placed points lie outside it). Houston's rule, not OSM's relation 6571629. A US federal government work, public domain |
| Kansas City | **Census TIGERweb place polygon**, current Incorporated Places, GEOID 2938000 (Kansas City, Missouri) | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=GEOID='2938000'` | the city: 824.8 km², gated at 790-860. Scopes the stations and the register's points (11 fall outside). Houston's layer, the legal boundary the City reports to the Census. A US federal government work, public domain |
| Tucson | **Census TIGERweb place polygon**, current Incorporated Places, GEOID 0477000 (Tucson city) | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=GEOID='0477000'` | the city: 629.4 km², gated at 600-660. Scopes the stations and the layer's points (the layer's `CITY` is a postal or jurisdiction name: "PIMA COUNTY", "MARANA"). Houston's layer, chosen over the <!-- internal -->brief's <!-- /internal -->OSM relation 253824 so the city's scope costs no Overpass query. A US federal government work, public domain |
| Tacoma | **Census TIGERweb place polygon**, current Incorporated Places, GEOID 5370000 (Tacoma city) | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=GEOID='5370000'` | the city: 161.7 km² (128.9 land, 32.9 water), gated at 150-175. Checks the register's council districts (every storefront in a district is inside) and scopes the stations. Kansas City's and Tucson's layer. A US federal government work, public domain |
| New Orleans | **Census TIGERweb place polygon**, current Incorporated Places, GEOID 2255000 (New Orleans city, coextensive with Orleans Parish) | `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4/query?where=GEOID='2255000'` | the city: 907.3 km² with its water, gated at 860-950. Scopes the stations and the register's points. A US federal government work, public domain |

Chicago note: the sibling asset `ewy2-6yfk` ("Boundaries - City - Map") has
null geometry; `qqq8-j68g` is the usable one.
New York note: `tqmj-j8zm`, the borough-boundary ID still in wide circulation,
now returns 404.
Boston note: **MassGIS's multi-town layer is used rather than Boston's own outline**, because naming the other towns is the bigger job here — the network is regional and 43 of 100 stations are in another municipality, a scale of exclusion that has to be citable as it is for San Diego's 16 and Los Angeles' 54. One layer then does both jobs.
This also settled a question the first survey of Boston's sources had left open. Boston's own water-excluded outline put four stations marginally outside the city (Boston College 6.7 m, Central Avenue 29.7 m, Longwood 51.8 m, Saint Mary's Street 58.4 m), and that survey called **Boston College "really a Boston station"**, so that no distance tolerance could separate them. That was wrong: MassGIS places Boston College in **NEWTON**, 6.6 m outside Boston, two independent boundary layers agreeing on the same ~6.6 m. Four of the 43 out-of-town stations sit within 100 m of Boston, but each is named, so no tolerance is needed. Naming beat measuring.
Washington D.C. note: **the boundary needed no multi-jurisdiction layer to disambiguate, which is the contrast with Boston.** Only one station is even arguably marginal — Southern Av, 40.1 m outside — and the next two are Capitol Heights at 111.2 m and Arlington Cemetery at 130.0 m, both unambiguous. Boston needed MassGIS because four of its stations sat within 60 m of the line and a tolerance could not separate them. Here the states layer is for NAMING only; the District's own single polygon does the filtering.
San Francisco note: **use the host `data.sf.gov`, never `data.sfgov.org`.**
This row recorded the old host until 2026-09-21, when a re-run showed that it
**301-redirects** and that the recorded `curl -sG` command does not follow
redirects: it silently saved a 654-byte HTML redirect page as
`sf_county_boundary.geojson`, exited 0, and failed only later when the file
was read. The assessor roll needs the same host for a different symptom (403
on `/resource/`), so it is one rule for this city. Unfiltered, the same
request returns 989,873 bytes of all nine counties.

`wamw-vt4s` is a **nine-county** Bay Area layer, so the
`county` filter is not optional — unfiltered it would scope the city to the
whole region. This endpoint was recovered on 2026-09-21 (it had been recorded
nowhere) by identifying the raw file from its own fields, `objectid` /
`fipsstco` / `county` with FIPS `06075`; the endpoint reproduces the file
byte-for-byte at 38,822 bytes with identical geometry, so it is the confirmed
original source and not a lookalike.

## Geocoding

| Service | Used by | Endpoint | Note |
|---|---|---|---|
| US Census Bureau bulk geocoder | Los Angeles, New York, Washington D.C., Sacramento, Houston, Dallas | `https://geocoding.geo.census.gov/geocoder/locations/addressbatch` | Free, no API key, US addresses only. Benchmark `Public_AR_Current`. Responses cached by batch content hash, so re-runs and drift checks stay offline and deterministic. D.C.'s use is different in kind from Los Angeles': LA's flagged rows had CORRUPT coordinates, D.C.'s have none at all, and Step 0's expectation that `MAR_ID` would recover them was wrong — the same 452 rows lack both. 387 of 451 were matched and every one fell inside the District polygon |

## Licenses and terms of use

### Explicit and permissive — confirmed

| Source | License | Attribution declared |
|---|---|---|
| San Francisco businesses (`g8m3-pdis`) | **Open Data Commons PDDL 1.0** (public domain dedication) | "City and County of San Francisco" |
| **Texas Comptroller, Active Sales Tax Permit Holders (`jrea-zgmq`)** - Houston, Dallas | **PERMITTED WITH CONDITIONS, nothing to display or do** (license read 2026-09-29). The Socrata label "Public Domain" is the Comptroller's own choice, and its Privacy and Security Policy (linked from the dataset, "Revised February 2025") grants it: "Information on CPA's sites is public domain and may be copied and used as permitted by law, with the exception of pictures, official symbols, and registered service marked names and logos." "As permitted by law" was followed: Tax Code §151.027(a) makes permit information public, and nothing in Tax Code ch. 151, §111.006, or Gov't Code chs. 552 and 2054 restricts reuse. Conditions: never use the Comptroller's or the State's seals or marks. No Texas statute restricts this list's use for solicitation. Re-read the policy before a republish | courtesy only: "Texas Comptroller of Public Accounts" |
| **City of Houston Site Addresses (COHGIS)** - Houston's address join | **Public domain** (<!-- internal -->the brief's read, <!-- /internal -->2026-09-29): the COHGIS Hub, "COHGIS data is in the public domain and may be copied without permission"; sibling items add "citation of the source is appreciated". Two sibling items put "© HITS-GIS. All rights reserved" in their credits field beside the grant, a low tension<!-- internal --> recorded in the brief<!-- /internal --> | courtesy only: "City of Houston Planning & Development" |
| **City of Minneapolis, Food Inspections** (ArcGIS item 4eea8bf452e34f8c9d9ac07c54c0b4ab) - Minneapolis | **PERMITTED, nothing to display or do** (license read 2026-09-30). A CC0 1.0 waiver on the dataset itself: the item's licenseInfo and its ISO metadata, "To the extent possible under law, City of Minneapolis has waived all copyright and related or neighboring rights to Open Data", and the Hub record's structured license CC0-1.0. The rest is the City disclaiming warranty and liability (Minn. Stat. 466.03 subd. 21). CC0 s.4(a) leaves the City's marks unwaived (not used), and s.4(c) leaves third parties' rights, a sole trader's own name among them, to the reuser<!-- internal -->: `check_personal_exposure.py` still applies<!-- /internal -->. The minneapolismn.gov terms of use govern that website's text and images, and neither the dataset page nor the portal incorporates them | courtesy only: "City of Minneapolis Open Data" |
| **Allegheny County Health Department, Geocoded Food Facilities (WPRDC)** - Pittsburgh | **PERMITTED WITH CONDITIONS, nothing to display** (license read 2026-09-30). CC0 on the package and the resource page (`license_id: cc-zero`), and WPRDC's Data Use Agreement defers to it ("pursuant to the license terms ... placed upon the Data by the Data owner"). The DUA binds by use ("By using the data ... you agree") and adds: an **uncapped indemnity** of the University of Pittsburgh, UCSUR, the City and the County for claims from our use - **accepted by the owner 2026-09-30** for this source, as for Hong Kong, Sacramento and Palma; a duty to **notify WPRDC's project manager** (rmg44@pitt.edu) and stop using any Non-Public Information found in the data<!-- internal --> (a trigger for `check_personal_exposure.py` findings)<!-- /internal -->; compliance with law. The County website's disclaimer governs its web pages, not this WPRDC-hosted resource. CC0 s.4(a): the County's seal and ACHD's marks are not used | courtesy only: "Allegheny County Health Department, via the Western Pennsylvania Regional Data Center (CC0)" |
| **City of Dallas Address Points** - Dallas's address join | **Silent on reuse; the City's Standard GIS Data Disclaimer of Liability, with its open-ended indemnity, ACCEPTED by the owner (2026-09-30)** - `docs/data_sources.md`, "Dallas's indemnity". Never call the pins surveyed or exact | optional: "City of Dallas Development Services GIS" |
| **KCMO Business License Holders (`kkhs-93m4`)** - Kansas City | **PERMITTED WITH CONDITIONS** (<!-- internal -->license-read 2026-09-30; <!-- /internal -->the indemnity settled by the owner the same day). Public Domain on the dataset and its parent `pnm4-68wg`, as KCMO Code § 2-2134(a) requires ("no restrictions or requirements placed on use"). The portal's undated Data Terms of Use (`data.kcmo.org/terms`) still prescribe a disclaimer for any derivative application (notice 80, City of Kansas City, Missouri; displayed) and claim an open-ended **indemnity** from "any user of the data" - the owner decided (2026-09-30) that the ordinance controls, so the indemnity binds nothing and Kansas City is cleared to land. KCMO Code § 40-33 lets the City release licensees' names and their place of business or residence; it binds the City, not reusers, and confirms that some addresses are homes. No commercial-use or solicitation restriction found | the disclaimer, verbatim (notice 80, City of Kansas City, Missouri); courtesy: "Revenue Division of KCMO Finance" (the dataset's own attribution field) |
| **City of Tucson BUSLIC (layer 3)** - Tucson | **SILENT, read as permitted by the owner (2026-09-30)**: the item's `licenseInfo` is an accuracy disclaimer only; nothing grants and nothing restricts, and the hub invites building applications. The owner took the permissive reading over two sibling City disclaimers (DTM Map Center, PDSD PRO) that add "for your personal use" and ask for acknowledgement, which the item does not incorporate. Never present the pins as complete ("should not be considered a complete listing of all active businesses in Tucson"). A.R.S. 39-121.03 does not reach a non-commercial portfolio | "Business licence data: City of Tucson." (notice 81) |
| **City of Tacoma "Business Licenses - Map (Tacoma)"** - Tacoma | **PERMITTED WITH CONDITIONS** (<!-- internal -->licence read 2026-10-03; <!-- /internal -->accepted by the owner on Chicago's template, 2026-10-03): Resolution 39378 (2016) and the City's open-data page place no restriction on reuse. The City's disclaimer must be displayed with any application using the data, so it is displayed site-wide, as Chicago's and Kansas City's are; the City may require any display or use to end, for any reason, which the removal rule honors. Cite data.tacoma.gov, never data.cityoftacoma.org (the item's `licenseInfo` still links that dead host). The pins are "active business license accounts", never "currently licensed" | The City's disclaimer, word for word (notice 142); "City of Tacoma, Tax & License (data.tacoma.gov)" in the page's caption |
| **City of New Orleans Active Occupational Licenses (`iqay-p646`)** - New Orleans | **CC0 1.0** (Creative Commons Public Domain Dedication), as the dataset declares (<!-- internal -->the brief; <!-- /internal -->`fetch_sources.py` checks it on every run). Nothing to display; `ownername` is never read, by choice | courtesy only: "City of New Orleans" (the page's caption) |
| San Francisco boundary (`wamw-vt4s`) | **Open Data Commons PDDL 1.0** | none declared |
| Los Angeles businesses (`6rrh-rzua`) | **CC0 1.0 Universal** (public domain dedication) | "Office of Finance" |
| **City of Long Beach, Business Licenses Public View (MapsLB)** - Los Angeles (Regional) | **PERMITTED WITH CONDITIONS, nothing required to display** (license read 2026-10-03, as on 2026-09-30). The layer's `licenseInfo` incorporates the MapsLB Terms of Use: "you are granted a license to copy, publish, distribute and/or transmit the Data, to adapt the Data and to exploit the Data for commercial and/or personal use"; the license "does not grant you any right to use the Data in any way that suggests City's endorsement of your use" and ends without notice on a breach. Indemnity on breach only, accepted by the owner (2026-09-30). The City may "change, restrict or discontinue access at any time" | "City of Long Beach, CA"; credited by choice, with a no-endorsement sentence (notice 129) |
| San Diego businesses | Portal terms explicitly permit use and **"Derivative Work"**, defined as "a work that is based in any way or to any extent on the Data". No attribution requirement stated | — |
| Boston — every source used above (food inspections, Licensing Board, cannabis, city boundary, plus the neighborhood, SAM address and Property Assessment layers) | **Open Data Commons PDDL** (public domain dedication), declared per-dataset in CKAN's `license_id` as `odc-pddl` | none declared |
| San Francisco assessor roll (`wv5m-vpq2`) — the residence-filter join | **Open Data Commons PDDL 1.0** (public domain dedication), declared in the dataset's own `license` field as "Open Data Commons Public Domain Dedication and License" | none declared |
| **LA County Assessor parcels** (`public.gis.lacounty.gov`) — the residence-filter join | **Explicit grant**, read 2026-09-22 from the County's Enterprise GIS Terms of Use: "you are granted a license to **copy, publish, distribute and/or transmit the Data, to adapt the Data and to exploit the Data for commercial and/or personal use**". Automatically voided on violation. Grants "no right to use the Data in any way that suggests County's endorsement of your use" | **Recommended, not required** — a citation format is offered as "the recommeded citation format", so this adds no notice. The service's `copyrightText` is "Los Angeles County Office of the Assessor" |
| **D.C. Basic Business Licenses** (ArcGIS item `85bf98d3915f412c8a4de706f2d13513`) - Washington D.C.'s register | **PERMITTED WITH CONDITIONS, CC BY 4.0** (licence read 2026-10-02, staging): the item's `licenseInfo` and metadata `useLimit`, "This work is licensed under a Creative Commons Attribution 4.0 International License." The District's data terms and Mayor's Order 2017-115 §X give CC0 "unless otherwise noted"; the item notes otherwise, and complying with CC BY 4.0 satisfies both. Nothing else owed | **Required**: credit the Department of Licensing and Consumer Protection, link the licence and the item, say the data was modified - notice 137 |
| **DC Boundary** (ArcGIS item `7241f6d500b44288ad983f0942b39663`, "Washington DC Administrative Boundary") - Washington D.C.'s scope | **PERMITTED WITH CONDITIONS, CC BY 4.0** (licence read 2026-10-02, staging), the same note over the same CC0 default. Reprojected and used to select stations and businesses; never drawn | **Required**: credit the Office of the Chief Technology Officer (DC GIS), link the licence and the item, say "reprojected" - notice 137 |
| **MassGIS Massachusetts Municipalities** (ArcGIS item `379e355b00244170a067eedde1f90417`) - Boston's boundary and naming layer | **PERMITTED, nothing required** (licence read 2026-10-02, staging; the FAQ re-read 2026-10-03). The item's use constraints: "These data are public records. Authoritative determination of municipal boundary locations can only be provided by a licensed land surveyor." MassGIS's FAQ: "the data are in the public domain and therefore can be used by anyone for any purpose." MUST NOT present the outline as an authoritative boundary location | **Requested, not required**, and shown: "MassGIS (Bureau of Geographic Information), Commonwealth of Massachusetts EOTSS" (the FAQ's words for maps and applications) - notice 140 |
| **LA County Planning, incorporated city boundaries** (`admin_dist_SDE_DIST_DRP_CITY_COMM_BDY`) - Los Angeles's scope and naming layer | **PERMITTED WITH CONDITIONS** (licence read 2026-10-02, staging): the County's Enterprise GIS Terms of Use, as for the Assessor parcels below, grant a licence to copy, publish and distribute the Data; an indemnity for breach only; the licence ends automatically on breach; no use that suggests the County's endorsement. MUST NOT call the outline a legal boundary | **None required**, and none shown |
| **SanGIS municipal boundaries** (`geo.sandag.org/server/rest/directories/downloads/Municipal_Boundaries.geojson`) - San Diego's scope | **PERMITTED WITH CONDITIONS** (licence read 2026-10-02, staging): the same *SanGIS GIS Data End User Use Agreement* as the tax parcels, with its uncapped indemnity and general release (a Civil Code §1542 waiver), **accepted by the owner 2026-10-02 for both SanGIS layers** (`docs/data_sources.md`, "San Diego's SanGIS indemnity"). SanGIS publishes it; SANDAG only hosts it, and its own "should not be redistributed" is read as deferring to SanGIS's terms. Never presented as an original SanGIS product | **PROHIBITED at this project's scale**, as for the parcels below: no SanGIS credit is shown, deliberately |
| **SanGIS tax parcels** (published by SanGIS, hosted by SANDAG on `geo.sandag.org`) — San Diego's residence-filter join | **Permitted with conditions**, and the conditions are unlike any other source here — see below. Redistribution is "discouraged, but **not** prohibited". Read 2026-09-22 from the layer item's own `licenseInfo`, which carries the full *SanGIS GIS Data End User Use Agreement* | **PROHIBITED at this project's scale** — see below. "Copyright SanGIS 2015 - All Rights Reserved" |

**SanGIS is the only source in this project that forbids being credited, and
the clause is easy to read backwards.** Its End User Use Agreement says:

> "End users should be aware that the data does not meet National Map Accuracy
> Standards at scales finer than 1:24,000... **SanGIS shall not be attributed
> as the source of the data when representing the data at scales below
> 1:24,000 absolute scale.** An exemption to the attribution prohibition is
> provided to the end user if the GIS data released to them from SanGIS is
> specifically identified as capable of performing at absolute scales below
> 1:24,000."

This project's rings are 0.1-0.6 miles, far finer than 1:24,000, and the parcel
layer is not identified as certified below that scale — so **adding a SanGIS
credit would breach the terms rather than satisfy them.** Every other source
here is the other way round, which is exactly why this one is worth stating:
the absence of a SanGIS notice is a deliberate compliance position, not an
oversight, and a future reviewer tidying up "missing" attributions must not
add one. It is also why the project's provenance check compares the notices recorded
here with the notices the site displays, rather than requiring a notice for
every source.

Two further clauses, neither of which this project triggers. **"UNDER NO
CIRCUMSTANCES SHALL THE END USER MODIFY OR ALTER THE SANGIS SOURCE DATA IN ANY
WAY AND REDISTRIBUTE IT AS AN ORIGINAL SANGIS PRODUCT. IF THE SANGIS SOURCE
DATA IS ALTERED SANGIS MAY BE CITED AS A REFERNCE BUT SHALL NOT BE IDENTIFED
AS THE SOLE DATA SOURCE"** (the typos are the document's). Nothing from this
layer is redistributed at all: it is read, used to decide whether a licence is
somebody's home, and discarded — no parcel geometry, APN or land-use code
reaches `outputs/`. And the agreement offers citation wording for derived
products, "GIS data derived, modified, reduced, and/or processed from SanGIS
downloadable data", which would be the right form if anything derived from it
were ever published.

**Read on its own, not assumed (2026-10-02):** San Diego's municipal
**boundary** layer sits on the same `geo.sandag.org` host but is a different
service (`rest/directories/downloads/Municipal_Boundaries.geojson`). Its own
reading found the same SanGIS agreement governing it, so the same no-credit
position holds; its row is in the table above. Extending the parcel agreement
to it by proximity would have been the Philadelphia mistake, where a licence
on one page turned out not to govern the dataset beside it, which is why it
was read separately.


PDDL and CC0 are both public-domain dedications, so neither compels
attribution; the maps credit these agencies anyway, which is good practice.

San Diego's terms carry a strong disclaimer worth knowing about: the data is
"as is" and "as available", the city "makes no representation or warranty that
the information contained in the Data is accurate, true or correct", and the
user indemnifies the city for claims arising from their use of it.

### Permissive on reading the terms themselves

| Source | What its terms say |
|---|---|
| **NYS retail food (`9a8c-vfzj`), NYS salons (`y3u4-jbgh`)** | The datasets declare no licence field, but the portal's "OPEN-NY Terms of Use" (dataset `77gx-ii52`, last modified 2013-03-08) is explicit: "At their core, the OPEN-NY Terms of Service are among the least restrictive of any terms of service … The OPEN-NY Terms of Service do **not** contain restrictions requiring members of the public to use attribution, to re-post the license terms with any re-uses of the data, to impose share-alike or technical restrictions, nor require the public to obtain pre-approval before re-use of the data." And: "So long as you are not doing anything malicious with NYS data, you may use it as you wish, subject to no other requirements." Conditions: lawful use; the State may require you in writing to stop displaying its content if it believes you are in breach. |
| **Chicago businesses (`r5kz-chrr`), Chicago boundary (`qqq8-j68g`)** | Reuse and derivative applications are contemplated, but **conditionally** — see the required notice below. The city "may require a user of this data to terminate any and all display, distribution or other use … for any reason", reserves all intellectual-property rights, and requires the user to indemnify it. |
| **Philadelphia businesses (`business_licenses`), Philadelphia boundary (`City_Limits`)** | Both carry a **named licence, "City of Philadelphia License"**, whose text is a rights reservation and disclaimer rather than a grant: the City "reserves all rights in the database and any data contained therein", the data is "as is" without warranty, the user "will assume complete responsibility for any and all occurrences resulting from its use or display" and holds the City harmless, and "browsing City data on this site constitutes acceptance". Its own text forbids nothing and requires no notice — **but the dataset page also binds a reader to the City's separate Terms of Use, which DO prohibit republication and modification without written permission (read 2026-09-21; see the open question below). This is the one source in the project whose terms, read literally, do not permit what is built here.** The clearest affirmative signal is on the boundary dataset, which states **"Usage: Public use; Free"**; the business-licence dataset's page carries no such field, so that statement covers the boundary layer specifically. Both sit in the City's Open Data Program, whose stated purpose is public reuse. **One judgment call follows — see below.** |
| **NYC DOHMH (`43nn-pn8j`), NYC DCWP (`w7w3-xahh`), NYC boroughs (`gthc-hcne`)** | **The absent licence field is required by law, not an oversight.** NYC's Open Data Technical Standards Manual states that Local Law 11 of 2012 "requires that data sets must be available **without registration requirement, license requirement, or usage restrictions**". The city therefore cannot attach a licence to these datasets. The "All Rights Reserved" notice in the nyc.gov footer covers nyc.gov's own website content, not datasets published under the Open Data Law. One condition does attach — see the notice below. |
| **Census TIGERweb state polygons** (used by Washington D.C. to name the 58 excluded stations' state) | A **US federal government work**, so not copyrightable — the Census Bureau's own terms say its data are in the public domain and may be used freely, asking only that the Bureau not be cited as endorsing a derived product. No attribution required, none claimed here beyond the endpoint record above. |
| **Open Data Buffalo: Business Licenses (`qcyy-feh8`)** | **PERMITTED, nothing to display or do** (licence read 2026-09-29). The declared "Public Domain U.S. Government" label is wrong for a City work (usa.gov: the designation "does not apply to works of state and local governments"), but the portal's own FAQ grants it: "All data available on the portal is licensed in the public domain, and there are no restrictions on the use of our published data", backed by the 2017 Open Data Policy ("without any licensing fees or restrictions on use or reuse"). Nothing incorporated by reference. MUST NOT SAY: the dataset's disclaimer says the data are not "the official records of the City of Buffalo"; the page never calls them that. The FAQ's invitation to email a project to opendatabuffalo@buffalony.gov is optional |
| **City of Seattle: Business Locations (Active)** | **PERMITTED WITH CONDITIONS.** The layer is federated on data.seattle.gov (`wmtg-dzy4`), whose Open Data Terms of Use and Open Data Policy V1.0 support reuse; no attribution is required, and "City of Seattle" is credited (notice 113). The condition: data that can be "configured as a list of individuals" may not be used "for a commercial purpose". This project is non-commercial, with nothing sold (owner, 2026-10-01), and must stay so. Contact names, phones, mailing addresses and person-named trade names are never published |
| **City of Bellevue: Business Licenses (All)** | **Read as permitted (owner, 2026-10-01).** The data's own license field bars only "commercial use or sale … without express written authorization"; the portal's linked Terms of Use allow only "own personal, non-commercial use", with all other rights reserved. The owner reads the data's own field as governing it: a free, non-commercial map falls outside its one prohibition. The City of Bellevue is credited (notice 112), and if Bellevue objects, the layer comes down first |
| **King County: Food Establishment Inspection Data, Address Points and city polygons** | **Read as permitted (owner, 2026-10-01).** The inspection dataset is declared Public Domain, and the portal's Open Data terms (archived 2023, now a 404) granted reuse; the live site-wide kingcounty.gov terms forbid publishing without written permission. The owner reads the dataset's declaration and the data terms as governing. MUST DISPLAY "Public Health – Seattle & King County" and "Data provided by permission of King County" (notice 109). MUST NOT use King County's logo or marks or imply endorsement, or take the address points' USPS-derived fields |
| **Snohomish County: Food Service Establishments (2025)** | **SILENT, read permissively (owner, 2026-10-02).** The item's license, description and use limits are empty. The County's GIS "Terms of Use and Data Disclaimer" (accuracy caveats, a hold-harmless for errors in the data, non-commercial use of lists of individuals) is read as its governing position, and the website's "All rights reserved" as a web-page footer. MUST DISPLAY the credit "Snohomish County, Food Service Establishments (2025)" (notice 111), never the health department, whose authorship is unconfirmed. MUST NOT call the layer current, complete or official |
| **Snohomish County: Building Address Points** (item `3c07edee19f142d2926dc1f7e4efc474`, owner SnocoGIS, credited to the County's Enhanced Emergency Services Communication System) | **SILENT on reuse, with the same conditions as the food layer** (license read 2026-10-02). The item sits in the County's open-data portal catalogue, and its own license field carries the County's disclaimer: illustrative data, no warranty, a hold-harmless for errors, and no commercial use of lists of individuals. It grants and forbids nothing else and prescribes no credit. Used only to place licensed shops by street address; no address point is shown, and the placement is never described as exact |
| **Washington State Liquor and Cannabis Board: Off Premise licensee list** | **PERMITTED WITH CONDITIONS.** No license and no terms of use exist. The lists page notes: "Per RCW 42.56.070(8), records received through the Public Records Act may not be used for commercial purposes", met by this project's non-commercial use (owner, 2026-10-02). The page states the list's date, never calls it complete or current, and repeats the Board's data-transfer notice while it stands on the lists page (notice 110). Removal contact: publicrecords@lcb.wa.gov |

### Still not established

| Source | Status |
|---|---|
| **US Census bulk geocoder** | Terms page not read. A US federal government work, used only to derive coordinates stored in this project's own outputs. Low priority. |
| **Boston "Business Inventory" (`47bd8208`)** | The one dataset on `data.boston.gov` whose `license_id` is `notspecified` rather than `odc-pddl`. Not established, and not pursued, because the source is deliberately unused (its coverage is downtown plus three corridors). **If it is ever used, the governing terms must be established first** — the portal's own "Open and Protected Data Policy" and the 2014 open-data executive order are the documents to read, not the boston.gov site footer. That is the NYC lesson: the parent site's notice covers the website, not the datasets. |
| **Miami-Dade Local Business Tax, its municipal boundary layer, and Miami-Dade Transit's GTFS** | All three carry a disclaimer and no grant. The ArcGIS items' `licenseInfo` is purely about ACCURACY — “Miami-Dade County provides this data for use 'as is'… not accurate to surveying or engineering standards… assumes no responsibility for errors or omissions” — and says nothing whatever about reuse, redistribution, modification or attribution. The GTFS has no `feed_info.txt`, and no separate MDT developer terms were located. **Established 2026-09-21 by reading, not by asking.** The Open Data Hub's own designated Terms of Use, at `https://opendata.miamidade.gov/pages/terms-of-use`, consist of the accuracy disclaimer quoted above, and the county-wide "Liability Disclaimer and User Agreement" at `miamidade.gov/global/disclaimer/disclaimer.page` is liability terms only, with no copyright claim and no reuse restriction. So three County documents say nothing whatever about reuse, redistribution, modification or attribution: a **definitive absence of restriction from the County's own authoritative pages**, not an unexamined gap. No enquiry to the County is needed. The affirmative signals stand: all three sources are published by the County's own ITD Geospatial group on its public open-data portal, in formats meant for reuse. |

Note the shape of this. **The business registries are mostly permissive and the
transit feeds are mostly not** — and the two are inverted within Los Angeles,
whose business data is CC0 while its GTFS terms are the most restrictive of
anything here. Canada inverts it again: there the registries almost all
prescribe their own sentence and the feeds mostly ride on the same municipal
licence.

**New York's position is established, not open.** Local Law 11 of 2012 forbids
the City attaching a licence at all, which is why it sits under *Permissive on
reading the terms themselves* two tables up. An established absence is not an
unestablished position, and conflating the two is how a source gets
re-investigated every time somebody reads this section.

The durable point: **an unread source and a source read to silence look
identical in a summary and are completely different in kind.** This table is
only for the first. Anything read and found to impose no restriction belongs
above, named, with the pages that were read. Miami-Dade is the worked example,
and it moved up here after the reading rather than before.

### Transit feeds (GTFS) — checked 2026-09-21

| Agency | Redistribution | Attribution | Other conditions |
|---|---|---|---|
| **MTS** (San Diego) | Permitted: "non-exclusive, limited and revocable rights to use, reproduce, and redistribute" | Not required | MTS trademarks "may not be used in association with GTFS Data". As-is, no liability; may withdraw the data at any time |
| **SFMTA** | Permitted: "use, reproduce, and redistribute" | **Required, in specific wording**: clause 12's notice, both paragraphs (four sentences), verbatim - notice 3 | Clause 4's liability disclaimer is to be displayed "or" included in a use agreement; the site has none, so it is displayed, verbatim (notice 3; re-read 2026-10-03 on SFMTA's page, updated 2024-10-01). A §5 indemnity; only SFMTA may alter the Data (clause 10); no trademarks or logos without written permission |
| **LA Metro** | **Restricted** — prohibits "unauthorized redistribution and publication" and requires you "not change, tamper, dismantle, augment, misrepresent or otherwise modify the Transport Information" | **Required** — must "acknowledge Metro as the provider of the Transport Information" and not claim ownership | No Metro trademark; must not "integrate Transport Information as part of any advertisement"; on termination you "shall immediately remove the Transport Information and all references to it" |
| **CTA** | Permitted: "use, reproduce, distribute, display, process and create derivative works" | Optional but encouraged: "Data provided by Chicago Transit Authority", "Data provided by CTA" or "Powered by CTA data" | **Purpose-limited** — the licence is granted to "assist mass transit riders or promote public transportation"; may not sell CTA Data separate from the application; may not imply affiliation or endorsement |
| **MTA** (New York) | Permitted: the feeds are "provided without charge", and the agreement "authorizes you to download and host the data on a non-MTA server ... and to make the data available to others who will access that non-MTA server". No API key needed for the static subway feed | Not required, but you "will not state or imply in any manner that your app is licensed by MTA"; you may state the data was obtained from MTA and is redistributed from your own server | **Corrected 2026-09-21 — this row previously recorded only the "Our data feeds are free to use" line from `mta.info/developers`, which is the landing page, not the terms.** The actual agreement (`https://new.mta.info/developers/terms-and-conditions`, page dated 2024-03-13) says **"You will not modify or delete any of the data"**, though its next sentence permits "an app that uses some but not all of the data". Also: must not "state or imply that the data is accurate, complete, or timely"; must serve the data from a non-MTA server and never directly from MTA's; MTA may change or terminate the agreement at any time without notice. Logos, maps and symbols need a separate licence application (free of charge but must be applied for). **An open decision, not a settled one<!-- internal --> — see `PLAN.md`<!-- /internal -->.** Local copy: `docs/licenses/mta-terms-and-conditions.txt` |
| **MBTA / MassDOT** (Boston) | Permitted: §3.1 grants "non-exclusive, limited, and revocable rights to use, reproduce, and redistribute the Data" | **Required** — §4.1 "Clearly acknowledge MassDOT as the provider of the Data" | §4.2 **expressly permits** combining the Data with other data. §4.1 forbids reproducing "MassDOT or any of its agencies or authorities logos or trademarks in connection with the Data", misrepresenting the Data, claiming ownership of it, or representing yourself as MassDOT or its agent. As-is with "all faults"; MassDOT may alter the terms or revoke the Data at any time without notice; Massachusetts law, venue Suffolk County. Document dated 2009-11-13, at `https://cdn.mbta.com/sites/default/files/2023-08/mbta-massdot-develop-license-agreement.pdf` — reachable from `mbta.com/developers/gtfs`, and the only route to the terms, since `feed_info.txt` declares none. **A local copy is kept at `docs/licenses/mbta-massdot-develop-license-agreement.pdf`**, because MassDOT may alter or revoke the terms without notice (§5.1, §8) and `mass.gov` returns 403 to automated fetches |
| **SEPTA** (Philadelphia) | Permitted: a "non-exclusive, non-assignable, non-transferable, limited and **revocable** right to use, reproduce and redistribute the datasets" | **Not required** — no attribution or notice clause anywhere in the agreement | "Licensee may not use SEPTA's trademarks and copyrighted materials for any commercial or profit-making use and may not alter them in any way." SEPTA "maintains title, ownership, rights and interest in and to the datasets", may revoke or modify the agreement at any time, and "reserves the right to institute a license fee at any time". As-is, no warranty, indemnification required; governed by Pennsylvania law, venue Philadelphia County. At `https://wwww.septa.org/license-agreement/` — the four-w host is **SEPTA's real domain, not the repo-README typo this row previously called it**: `www.septa.org` and `wwww.septa.org` each return 200 independently, with no redirect between them (checked 2026-09-21). Local copy: `docs/licenses/septa-license-agreement.html` |
| **WMATA** (Washington D.C. — **BUILT 2026-09-21**) | Permitted within your own app: "a limited, non-exclusive, non-assignable, non-transferrable, non-sublicensable, revocable license to download, use, reproduce, and redistribute WMATA's Transit Data within your Application". **Third-party redistribution is prohibited** — "sharing (except with your Application's users), transferring, sublicensing, selling or leasing any Transit Data, directly or indirectly...to any other person", unless authorised in writing and "inseparably commingled with or supplemented by additional data that you have provided" | **Not required** — no attribution or notice clause | **No modification clause at all**, which makes it more permissive than LA Metro's on the point that matters most. Access is gated: `api.wmata.com/gtfs/rail-gtfs-static.zip` returns **401** without a registered key from `developer.wmata.com/signup`; keys "remain WMATA's property and may be revoked or otherwise limited at any time", cannot be sold, transferred or sublicensed, and "enable WMATA to associate your API activity with your Application". Trademarks: "prohibited from using WMATA Intellectual Property, including any confusingly similar variants, in association with the Transit Data or API unless you have entered into a separate, written license agreement", and must not "state or imply affiliation, sponsorship or endorsement". **§6 additionally forbids stating or implying that the data your Application provides "is accurate, complete, or timely"** — the identical clause MTA carries, making this the **second** feed to constrain city-page prose that way, so it is a cross-city sweep rather than a D.C. footnote. **§9 termination is the sharpest in the project:** on termination "you must permanently delete all Transit Data or other data which you stored pursuant to your use of the API or GTFS", and "WMATA may request that you certify in writing your compliance with this section" — LA Metro requires removal, but only WMATA asks for written certification. Read 2026-09-21 from `https://developer.wmata.com/license`; local copy at `docs/licenses/wmata-transit-data-terms-of-use.html` |

<!-- internal -->
### The owner's API-account practice, and what it interacts with

**Stated 2026-09-21: the owner registers an API account, takes the data, and
then immediately terminates the account and revokes its keys.** This was done
for WMATA and is the intended approach for Korea's `data.go.kr` key.

**Why it is sound.** A key that no longer exists cannot leak, cannot be found
in a shell history or an environment file, and cannot be used against the
owner's identity. It is a stronger position than storing a live key carefully.

**Two consequences to plan around, neither of them a problem but both real:**

1. **A rebuild requires re-registering.** The city cannot be regenerated from a
   clean checkout, or after a crash, or to refresh stale data, without creating
   a new account and key first. For D.C. this is sharper than elsewhere because
   **WMATA's `feed_end_date` window is ten days** — so any rebuild is
   necessarily a fresh download, never a reuse. Budget the registration step
   into any D.C. or Korea re-run, and do not treat those pages as
   self-regenerating.
2. **Terminating the account ends the LICENCE, and that is the point — not the
   deletion clause.** Read from the stored copy rather than inferred. §9:
   "Upon termination of these Terms **(i) all rights and licenses granted to
   you will terminate immediately**; … and (iv) … you must permanently delete
   all Transit Data **or other data which you stored pursuant to your use of
   the API or GTFS**. WMATA may request that you certify in writing your
   compliance."

   "Termination of these Terms" is the **data licence**, nothing else — these
   are API terms of use. Deleting the account ends the agreement.

   **(i) is the operative clause.** The grant this project relies on is "a
   limited… license to download, use, reproduce, and **redistribute** WMATA's
   Transit Data **within your Application**". If that has terminated, the
   question is not whether a rendered map counts as stored Transit Data — it is
   that **the right to publish the page has lapsed.**

   **The resolution is simple and the owner's stated plan already does it:
   re-register.** A new account creates a new agreement with a fresh grant, and
   while that licence is live, redistribution within the Application is
   expressly permitted — no grey area at all.

   **So: hold a live WMATA account before the public deploy, and keep it alive
   while the D.C. page is published.** This costs nothing extra, because the
   ten-day `feed_end_date` window already means any rebuild needs a live
   account. On (iv), the clearest obligation is met regardless:
   `data/washington_dc/raw/` is gitignored and never committed.

   **RESOLVED 2026-09-21: a valid WMATA account has been re-established**, so
   the licence grant in §2 is live again and the D.C. page rests on a current
   licence rather than a lapsed one. Nothing further is owed.

   **The standing obligation this creates, and it is the only part that
   outlives today:** the account must stay live for as long as the D.C. page is
   published. Do not terminate it while the site is up. If it is terminated
   later — deliberately or by WMATA, which "may revoke or otherwise limit"
   keys at any time — then §9(i) applies again and **the D.C. page must come
   down until a new account is registered.** That is now a deploy-gate
   condition, not a background note.

   **Korea raises none of this** — `이용허락범위 제한 없음`, no restriction and
   no termination clause, so terminating that key has no licensing
   consequence at all.

**Do not take WMATA's feed from a third-party mirror.** The Mobility Database
carries a keyless copy, and using it would be the worse option rather than the
convenient one: it relies on a redistribution these terms appear to prohibit,
and it means obtaining the data *outside* the licence instead of accepting it.
The registered key is the compliant route. Because GTFS fetching lives in
non-`step*.py` scripts, that key is a local environment variable for an
occasional manual refresh — it never reaches the deployed app, which reads only
`outputs/`.
<!-- /internal -->

**Two of these needed a judgment call rather than just a notice. Both were
decided by the project owner on 2026-09-21**, and the reasoning is recorded so
the position is a stated one rather than an assumption:

- **LA Metro** forbids modifying the "Transport Information". **Decided: this
  project does not modify it.** The rail alignment is drawn from the feed's
  own `shapes.txt` geometry and displayed as that line; nothing in the
  transport information is altered, augmented or misrepresented. The clause
  reads as protecting against passing off changed schedule or route data as
  Metro's, which is not what happens here. Metro is credited as the provider
  per the notice below. This remains the tightest licence in the project, so
  revisit it if Metro clarifies the clause.
  **Checked in detail on 2026-09-21, and the statement above did NOT hold
  literally until a fix was made that day.** `map_common.COORD_DP` rounded
  every coordinate to 6 decimal places before it reached the HTML, transit
  geometry included. Measured over every vertex, **LA Metro's `shapes.txt`
  reaches 10 dp and 21.0% of its coordinates (2,606 of 12,426) exceed 6 dp** —
  so the published alignment genuinely differed from the feed, on a fifth of
  its points, for the tightest licence in the project. An initial check that
  sampled only the start of the geometry reported a clean 6 dp and was wrong:
  the feed is mixed-precision, 6 dp early and finer later.
  **Fixed:** `shapes.txt` vertices are now emitted unrounded, so the alignment
  is the feed's own geometry as stated. Station points stay rounded on purpose
  — most cities derive them by averaging a parent station's platform stops, so
  they are this project's own computed values rather than Metro's data. The same check clears MTA's "you will not modify or
  delete any of the data": its feed is already 6 dp throughout, so that clause
  was never engaged.
- **CTA**'s licence is granted for assisting riders or promoting public
  transport. **Decided: the project falls within that purpose.** It shows
  people in the city what businesses are near their station, which is
  rider-facing information about using the system, not merely an abstract
  analysis. It is also not sold, not advertising, and claims no affiliation —
  the clauses the purpose limitation sits beside.

**MassDOT needed no judgment call, which is worth stating positively.** Its
agreement is the same family as MTS's and SEPTA's — a revocable grant to use,
reproduce and redistribute — but it is the only transit licence here that
*expressly permits* combining the data with other data (§4.2), and it contains
**no restriction on modification at all**. That is the direct opposite of LA
Metro's clause, the tightest in the project, and it means redrawing
`shapes.txt` into a map raises no question. The obligations are mechanical: one
acknowledgement notice, and no MBTA logos or trademarks. Since this project
draws its own line geometry and labels lines with their real public names while
reproducing no roundel or T mark, the trademark clause is satisfied by
construction rather than by interpretation.

**Three permission questions were raised on 2026-09-21** — two from
Philadelphia and one from Miami. SEPTA's and Miami-Dade's were settled the same
day (below); **Philadelphia's is still open**, and the footer of every page says
so. They are the same question in three forms: **what does silence mean?**

- **SEPTA's trademark clause — ANSWERED 2026-09-21 by reading the notice it
  points to, and it is not a question any more.** The clause is "Licensee may
  not use SEPTA's trademarks and copyrighted materials for any commercial or
  profit-making use and may not alter them in any way", and it points to
  SEPTA's Copyright and Trademark Notice at `www.septa.org/copyright/`. That
  notice had never been read. Its **entire Trademark Notice is one sentence**:
  "**The SEPTA Logo** is a registered trademark of featured words or symbols,
  used to identify the source of its goods and services." Line names are not
  claimed; route colours are not claimed; this project reproduces no logo, so
  the clause has nothing to bite on.
  The same page's Copyright Notice, and its "Web Contents and Materials"
  permission — "for informational and non-commercial purposes only" — are
  scoped to "this World Wide website" and "documents and related graphics from
  this ... Server", i.e. septa.org's own pages. That is the septa.org footer,
  not the Open Data Portal's terms: the identical distinction NYC taught, where
  the nyc.gov "All Rights Reserved" notice covered the website and not the
  datasets. **So the non-commercial wording never reached the datasets**, which
  have their own express grant.
  What the sentence *does* cover: the datasets are separately and expressly
  licensed by the paragraph above it. The map uses SEPTA's real
  public line names ("Market-Frankford Line") and its own `route_color`
  values from `routes.txt`, and reproduces no SEPTA logo, wordmark or route
  bullet artwork. **No longer an open question** — the Trademark Notice claims
  only the Logo, so there is nothing here to substitute. The fallback that was
  held in reserve (keep the geometry, swap in this project's own palette and
  descriptive names) is recorded as considered and unnecessary.
- **The "City of Philadelphia License" reserves all rights in the database —
  and on 2026-09-21 this stopped being a silence question and became a
  PROHIBITION question.** The licence itself still grants nothing explicitly
  and requires no notice. What had not been read is the sentence the dataset
  page opens with: "Browsing City data on this site constitutes acceptance of
  the license, **the City's terms of use** and your agreement to be bound by
  them." That incorporates `phila.gov/terms-of-use` by reference, and those
  terms are not silent. They grant permission only "to residents and citizens
  of the City of Philadelphia to copy electronically and to print single pages
  from the Website ... exactly as presented on the Website, without any
  addition or modification", and then say: "**Distribution or republication in
  any other form or for any other purpose, including any commercial purpose or
  use, and any modification whatsoever, are strictly prohibited without the
  prior written permission of the City.**" A separate sentence adds
  "Commercial use is prohibited without the prior written permission of the
  City."
  **Applied to the datasets, read literally, that does not permit this
  project's Philadelphia map**, which filters the register and redraws it —
  modification and republication both. The contrary reading is strong but it
  is a reading: the terms are drafted throughout for web pages ("print single
  pages", "exactly as presented on the Website"), the dataset-specific licence
  beside them contains no such prohibition, the boundary dataset is marked
  "Usage: Public use; Free", and the Open Data Program was established by
  executive order in 2012 for public reuse. **This project has not resolved it
  in its own favour, and the footer on every page says so.**
  **A factor was raised here and withdrawn the same day; the withdrawal is
  worth keeping.** The sentence that does the incorporating appears on an
  **OpenDataPhilly** page, and OpenDataPhilly is not the City - it is "built by
  Azavea, a Philadelphia-based geospatial software firm". That looked like it
  weakened the hook. **It does not: the City runs its own catalogue at
  `metadata.phila.gov`, on a phila.gov subdomain, and that catalogue's own
  "Terms of use" link points straight at `www.phila.gov/terms-of-use/`** - the
  document with the prohibition in it. The City makes the connection in its own
  voice, on its own property. The third-party-portal argument is dead.
  **Which way the wider probe points, stated plainly, because it was tested
  hopefully and came back the other way:** the only unambiguous permission
  anywhere in Philadelphia's paperwork is the "Usage: Public use; Free" field on
  **City Limits** - the boundary layer. The Business Licenses dataset, which is
  the one carrying trade names at mapped addresses, has **no Usage field at
  all**. So the permissive signal covers the harmless half of what this project
  takes and not the sensitive half, and the City's own catalogue points at the
  restrictive terms. **Asking is more warranted after the check than before
  it.**
  **DECIDED 2026-09-21 (the owner):** ask the City for written permission - its
  terms name that as the route - and keep the map live under the reasoned
  position meanwhile, with the footer disclosing the question. The request,
  addressed to `maps@phila.gov` copying `LIGISTEAM@phila.gov`, was **SENT
  2026-09-21**.
  No reply as of the one-week follow-up on 2026-09-28. Silence will not be
  treated as consent - the interim position rests on the reasoned reading and
  the disclosure, not on the City having failed to object.
  For contrast, this is the same shape as the NYC question but with the opposite
  paperwork — NYC is *forbidden* from imposing a licence, whereas Philadelphia
  has imposed one that says only "we keep our rights".
- **Miami-Dade states no reuse position at all, for all three of its sources.**
  Added 2026-09-21 with the Miami build. The business registry and the
  municipal boundary layer carry an `licenseInfo` that is purely about
  ACCURACY — data provided "as is", "not accurate to surveying or engineering
  standards", the County "assumes no responsibility for errors or omissions" —
  and say nothing whatever about reuse, redistribution, modification or
  attribution. Miami-Dade Transit's GTFS is worse served: it ships **no
  `feed_info.txt` at all**, and no separate MDT developer terms could be
  located. **Open question:** whether a disclaimer with no grant and no
  prohibition is a sufficient basis to publish a derived map. The affirmative
  signals are that all three are published by the County's own ITD Geospatial
  group on its public open-data portal, in reuse-ready formats (GeoJSON, a
  queryable FeatureServer, a GTFS zip).

  This is the **weakest paperwork of any city in the project**, and worth
  distinguishing from the two above. Philadelphia at least names a licence and
  reserves rights under it; NYC's silence is legally *required*. Miami-Dade
  simply never addresses the question — which is not the same as permitting it.
  Two things reduce the exposure meanwhile: the map already uses this project's
  own line colours rather than MDT's, so the trademark half of the question
  does not arise for Miami, and nothing in the rendered output reproduces
  County branding.

**A fourth open question: agency branding — official route colours, and the
line names beside them.** This was first written up as affecting three
agencies. **Corrected 2026-09-21 after checking every city's config: it is
FIVE**, and the two that were missing have the strictest wording of the set.
The maps draw each line in the agency's own `route_color` from `routes.txt` and
label it with the agency's own public line name, and most of these agencies
treat their marks as protected:

| Agency | City | What its terms say about marks |
|---|---|---|
| **MTS** | San Diego | MTS trademarks **"may not be used in association with GTFS Data"** — a flat prohibition, not an application process, and the tightest wording here |
| **LA Metro** | Los Angeles | **"No Metro trademark"**, alongside the modification clause already decided |
| **CTA** | Chicago | May not imply affiliation or endorsement |
| **MTA** | New York | Logos, maps and symbols need a separate licence application — free of charge, but it must be applied for |
| **SEPTA** | Philadelphia | **Answered 2026-09-21:** its Trademark Notice claims only "The SEPTA Logo", so neither the line names nor the route colours are trademarks it asserts, and no logo is reproduced here |
| **WMATA** | Washington D.C. | "prohibited from using WMATA Intellectual Property, including any confusingly similar variants, in association with the Transit Data or API unless you have entered into a separate, written license agreement" |

Two cities are **out of scope** because they already draw their own palette:
San Francisco (a custom six-colour set, not Muni's) and Miami (purple/teal/
brown, because Miami-Dade's orange and two greens collide with the
business-category colours). So the question touches five of the seven built
cities, not two.

**It has two halves, and only one of them is optional.** The colours are a free
choice — the project has already departed from an official value twice on its
own initiative (San Francisco throughout, and Staten Island Railway's `#08179C`
lightened for legibility). The **names are not**: a standing invariant requires
every drawn line to carry its real public name on the map and in the legend, so
"Red Line", "Market-Frankford Line" and "Metrorail" cannot simply be
substituted without changing what the project promises a reader. If an
agency's answer covers names as well as colours, that is a harder change than
a palette swap.

**Decided by the owner on 2026-09-21: keep the official colours and record this
as an open question**, rather than pre-emptively substituting a palette. It
blocks nothing now. What makes it cheap to reverse on the colour side is that
each city's colours sit in one setting in
its own code, and nothing in the rendering depends on them being the agency's.
Nothing in the project reproduces a logo, wordmark or route-bullet artwork from
any agency, which is the part every one of these clauses most clearly covers.
